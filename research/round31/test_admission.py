#!/usr/bin/env python3
"""Damaging evidence controls for the trusted Round31 admission specification."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
from reproduce import ROOT, digest, load, validate


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def rebind(root, loop):
    r = root / 'research/round31'
    gate_path = r / f'advisor/{loop}-gate.json'
    gate = load(gate_path)
    for side in ('forward', 'reverse'):
        p = r / side / loop
        result_hash = digest(p / 'output/results.json')
        for manifest in (p / 'output').glob('*manifest*.json'):
            data = load(manifest)
            for key in ('outputs', 'files'):
                if 'results.json' in data.get(key, {}):
                    data[key]['results.json'] = result_hash
            write(manifest, data)
        freeze_path = p / 'freeze.json'
        freeze = load(freeze_path)
        freeze['sources'] = {name: digest(root / name) for name in freeze['sources'] if (root / name).is_file()}
        write(freeze_path, freeze)
    review_path = r / f'skeptic/{loop}.json'
    review = load(review_path)
    if 'bindings' in review:
        review['bindings'] = {name: digest(root / name) for name in review['bindings'] if (root / name).is_file()}
    write(review_path, review)
    gate['bindings'] = {name: digest(root / name) for name in gate['bindings'] if (root / name).is_file()}
    write(gate_path, gate)


def main():
    original = validate(complete=True)
    inherited = set()
    for row in original['loops']:
        gate = load(ROOT / f"research/round31/advisor/{row['id'].lower()}-gate.json")
        inherited.update(name for name in gate['bindings']
                         if not name.startswith('research/round31/'))
        contract = load(ROOT / f"research/round31/contracts/{row['id'].lower()}.json")
        inherited.update(name for name in contract['shared_premises']
                         if not name.startswith('research/round31/'))
    expected_reasons = {
        'removed-control': 'Removed or changed reviewed controls',
        'expanded-claim': 'Changed claim: continuum_claim',
        'omitted-counterpart': 'Missing required producer source',
        'expanded-gate': 'Changed reviewed semantics: accepted',
        'stripped-control-status': 'Missing or failed executed control status',
        'symlink-parent': 'Symlink evidence component',
        'missing-declared-snapshot': 'Missing or escaping evidence',
    }
    results = []
    for row in original['loops']:
        loop = row['id'].lower()
        mutations = ['removed-control', 'expanded-claim', 'omitted-counterpart',
                     'expanded-gate', 'stripped-control-status']
        if loop == 'at6':
            mutations.extend(['symlink-parent', 'missing-declared-snapshot'])
        for mutation in mutations:
            with tempfile.TemporaryDirectory(prefix='hnm-r31-bad-evidence-') as tmp:
                root = Path(tmp)
                r = root / 'research/round31'
                shutil.copytree(ROOT / 'research/round31', r, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                for name in sorted(inherited):
                    target = root / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / name, target)
                # The unmodified control must pass in this exact temporary
                # environment, so a missing inherited file cannot masquerade
                # as rejection of the intended damaging change.
                validate(root, complete=True)
                if mutation in ('removed-control', 'expanded-claim', 'stripped-control-status'):
                    p = r / f'forward/{loop}/output/results.json'
                    data = load(p)
                    if mutation == 'removed-control':
                        data['checks'].pop()
                    elif mutation == 'expanded-claim':
                        data['continuum_claim'] = True
                    else:
                        data['checks'] = [entry['id'] for entry in data['checks']]
                    write(p, data)
                    rebind(root, loop)
                elif mutation == 'omitted-counterpart':
                    (r / f'reverse/{loop}/report.md').unlink()
                    rebind(root, loop)
                elif mutation == 'missing-declared-snapshot':
                    contract = load(r / f'contracts/{loop}.json')
                    premise = next(x for x in contract['shared_premises'] if x != 'AGENTS.md')
                    (r / f'forward/{loop}/inputs' / premise).unlink()
                    rebind(root, loop)
                elif mutation == 'symlink-parent':
                    original_skeptic = r / 'skeptic'
                    relocated = r / 'skeptic-actual'
                    original_skeptic.rename(relocated)
                    original_skeptic.symlink_to(relocated.name, target_is_directory=True)
                else:
                    path = r / f'advisor/{loop}-gate.json'
                    gate = load(path)
                    gate['accepted'] += ' The continuum problem is also solved.'
                    write(path, gate)
                    findings = load(r / 'advisor/findings.json')
                    for entry in findings['loops']:
                        if entry['id'].lower() == loop:
                            entry['accepted'] = gate['accepted']
                    write(r / 'advisor/findings.json', findings)
                try:
                    validate(root, complete=True)
                except (ValueError, KeyError, FileNotFoundError) as error:
                    if expected_reasons[mutation] not in str(error):
                        raise RuntimeError('Rejected for an unrelated reason: ' + str(error)) from error
                    results.append({'loop': loop, 'mutation': mutation, 'rejected': True, 'reason': str(error)})
                else:
                    raise RuntimeError('Admitted damaging evidence: ' + loop + '/' + mutation)
    print(json.dumps({'status': 'passed', 'rejected': len(results), 'controls': results}, indent=2))


if __name__ == '__main__':
    main()
