#!/usr/bin/env python3
"""Damaging evidence controls for the trusted Round32 admission specification."""
import json
from pathlib import Path
import shutil
import tempfile
from reproduce import ROOT, digest, load, validate


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def rebind(root, loop):
    r = root / 'research/round32'
    gate_path = r / f'advisor/{loop}-gate.json'
    gate = load(gate_path)
    for side in gate['producers']:
        p = r / side / loop
        for manifest in (p / 'output').glob('*manifest*.json'):
            data = load(manifest)
            result_hash = digest(p / 'output/results.json')
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
    complete = load(ROOT / 'research/round32/advisor/findings.json')['completed'] == 10
    original = validate(complete=complete)
    inherited = set()
    for row in original['loops']:
        gate = load(ROOT / f"research/round32/advisor/{row['id'].lower()}-gate.json")
        inherited.update(name for name in gate['bindings'] if not name.startswith('research/round32/'))
        contract = load(ROOT / f"research/round32/contracts/{row['id'].lower()}.json")
        inherited.update(name for name in contract['shared_premises'] if not name.startswith('research/round32/'))
    expected_reasons = {
        'removed-control': 'Removed or changed reviewed controls',
        'expanded-claim': 'Changed claim: continuum_claim',
        'omitted-counterpart': 'Missing required producer source',
        'expanded-gate': 'Changed reviewed semantics: accepted',
        'stripped-control-status': 'Missing or failed executed control status',
        'symlink-parent': 'Symlink evidence component',
        'missing-declared-snapshot': 'Missing or escaping evidence',
        'changed-contract': 'Missing or changed prospective contract snapshot',
        'reordered-subround': 'Wrong sub-round',
    }
    results = []
    loops = [row['id'].lower() for row in original['loops']]
    for loop in loops:
        mutations = ['removed-control', 'expanded-claim', 'omitted-counterpart',
                     'expanded-gate', 'stripped-control-status']
        if loop == loops[-1]:
            mutations.extend(['symlink-parent', 'missing-declared-snapshot', 'changed-contract', 'reordered-subround'])
        for mutation in mutations:
            with tempfile.TemporaryDirectory(prefix='hnm-r32-bad-evidence-') as tmp:
                root = Path(tmp)
                r = root / 'research/round32'
                shutil.copytree(ROOT / 'research/round32', r, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                for name in sorted(inherited):
                    target = root / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / name, target)
                validate(root, complete=complete)
                gate = load(r / f'advisor/{loop}-gate.json')
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
                    side = gate['producers'][-1]
                    (r / f'{side}/{loop}/report.md').unlink()
                    rebind(root, loop)
                elif mutation == 'missing-declared-snapshot':
                    contract = load(r / f'contracts/{loop}.json')
                    premise = next(x for x in contract['shared_premises'] if x != 'AGENTS.md')
                    (r / f'forward/{loop}/inputs' / premise).unlink()
                    rebind(root, loop)
                elif mutation == 'changed-contract':
                    path = r / f'contracts/{loop}.json'
                    contract = load(path)
                    contract['claim_exclusions'] = []
                    write(path, contract)
                    rebind(root, loop)
                elif mutation == 'reordered-subround':
                    path = r / f'advisor/{loop}-gate.json'
                    gate['subround'] = 99
                    write(path, gate)
                    findings = load(r / 'advisor/findings.json')
                    for entry in findings['loops']:
                        if entry['id'].lower() == loop:
                            entry['subround'] = 99
                    write(r / 'advisor/findings.json', findings)
                elif mutation == 'symlink-parent':
                    original_skeptic = r / 'skeptic'
                    relocated = r / 'skeptic-actual'
                    original_skeptic.rename(relocated)
                    original_skeptic.symlink_to(relocated.name, target_is_directory=True)
                else:
                    path = r / f'advisor/{loop}-gate.json'
                    gate['accepted'] += ' The continuum problem is also solved.'
                    write(path, gate)
                    findings = load(r / 'advisor/findings.json')
                    for entry in findings['loops']:
                        if entry['id'].lower() == loop:
                            entry['accepted'] = gate['accepted']
                    write(r / 'advisor/findings.json', findings)
                try:
                    validate(root, complete=complete)
                except (ValueError, KeyError, FileNotFoundError) as error:
                    if expected_reasons[mutation] not in str(error):
                        raise RuntimeError('Rejected for an unrelated reason: ' + str(error)) from error
                    results.append({'loop': loop, 'mutation': mutation, 'rejected': True, 'reason': str(error)})
                else:
                    raise RuntimeError('Admitted damaging evidence: ' + loop + '/' + mutation)
    print(json.dumps({'status': 'passed', 'rejected': len(results), 'controls': results}, indent=2))


if __name__ == '__main__':
    main()
