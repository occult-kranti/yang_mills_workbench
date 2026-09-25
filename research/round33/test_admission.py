#!/usr/bin/env python3
"""Damaging evidence controls for the trusted Round33 admission specification.

Structural controls (execution count, stop boundary, plan requirement) run at
every stage of the cycle. Per-loop mutations run once at least one loop is
gated; with zero gated loops they are reported as skipped, never as passed
evidence about a loop.
"""
import json
from pathlib import Path
import shutil
import tempfile
from reproduce import LOOP_IDS, PLANNED, ROOT, digest, load, validate

REL = 'research/round33'


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def rebind(root, loop):
    r = root / REL
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


def inherited_files(rows):
    inherited = set()
    for row in rows:
        loop = row['id'].lower()
        gate = load(ROOT / f'{REL}/advisor/{loop}-gate.json')
        inherited.update(name for name in gate['bindings'] if not name.startswith(REL + '/'))
        contract = load(ROOT / f'{REL}/contracts/{loop}.json')
        inherited.update(name for name in contract['shared_premises'] if not name.startswith(REL + '/'))
        inherited.update(name for name in contract.get('forward_additional_premises', []) if not name.startswith(REL + '/'))
    return inherited


def copy_tree(tmp, inherited):
    root = Path(tmp)
    shutil.copytree(ROOT / REL, root / REL, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for name in sorted(inherited):
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    return root


def expect_rejection(root, complete, reason, label):
    try:
        validate(root, complete=complete)
    except (ValueError, KeyError, FileNotFoundError) as error:
        if reason not in str(error):
            raise RuntimeError('Rejected for an unrelated reason: ' + label + ': ' + str(error)) from error
        return str(error)
    raise RuntimeError('Admitted damaging evidence: ' + label)


def structural_controls(complete, inherited):
    """Controls that need no gated loop: counts, stop boundary and the plan."""
    results = []
    cases = {
        'count-mismatch': 'Wrong execution count',
        'over-stop-boundary': 'Eight-loop stop boundary',
        'wrong-requested': 'Findings do not request eight investigations',
        'wrong-author': 'Wrong findings author',
    }
    if not complete:
        cases['premature-complete'] = 'Eight-loop stop boundary'
    for mutation, reason in cases.items():
        with tempfile.TemporaryDirectory(prefix='hnm-r33-bad-structure-') as tmp:
            root = copy_tree(tmp, inherited)
            r = root / REL
            validate(root, complete=complete)
            path = r / 'advisor/findings.json'
            findings = load(path)
            check_complete = complete
            if mutation == 'count-mismatch':
                findings['completed'] = len(findings['loops']) + 1
            elif mutation == 'over-stop-boundary':
                extra = [dict(findings['loops'][0]) if findings['loops'] else {'id': 'bz9'}
                         for _ in range(PLANNED + 1 - len(findings['loops']))]
                findings['loops'] = findings['loops'] + extra
                findings['completed'] = len(findings['loops'])
                for index, row in enumerate(findings['loops']):
                    row['id'] = 'extra-' + str(index)
            elif mutation == 'wrong-requested':
                findings['requested'] = PLANNED + 2
            elif mutation == 'wrong-author':
                findings['human_author'] = 'Someone else'
            else:
                check_complete = True
            write(path, findings)
            reason_text = expect_rejection(root, check_complete, reason, 'structure/' + mutation)
            results.append({'loop': None, 'mutation': mutation, 'rejected': True, 'reason': reason_text})
    return results


def loop_controls(loops, complete, inherited):
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
        'changed-direction': 'Findings direction differs from the frozen contract',
        'missing-independent-derivation': 'Single-direction loop lacks independent skeptic derivation',
        'reverse-extra-premise': 'Reverse premise isolation violated',
    }
    gates = {loop: load(ROOT / f'{REL}/advisor/{loop}-gate.json') for loop in loops}
    contracts = {loop: load(ROOT / f'{REL}/contracts/{loop}.json') for loop in loops}
    plan = {loop: ['removed-control', 'expanded-claim', 'omitted-counterpart',
                   'expanded-gate', 'stripped-control-status', 'changed-direction'] for loop in loops}
    last = loops[-1]
    plan[last] += ['symlink-parent', 'changed-contract', 'reordered-subround']
    with_premise = [loop for loop in loops if any(x != 'AGENTS.md' for x in contracts[loop]['shared_premises'])]
    if with_premise:
        plan[with_premise[-1]].append('missing-declared-snapshot')
    single = [loop for loop in loops if gates[loop]['producers'] == ['forward']]
    if single:
        plan[single[-1]].append('missing-independent-derivation')
    isolated = [loop for loop in loops if gates[loop]['producers'] == ['forward', 'reverse']
                and contracts[loop].get('reverse_premise_isolation')]
    if isolated:
        plan[isolated[-1]].append('reverse-extra-premise')
    results = []
    for loop in loops:
        for mutation in plan[loop]:
            with tempfile.TemporaryDirectory(prefix='hnm-r33-bad-evidence-') as tmp:
                root = copy_tree(tmp, inherited)
                r = root / REL
                # The unmodified control must pass in this exact temporary
                # environment, so a missing inherited file cannot masquerade
                # as rejection of the intended damaging change.
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
                elif mutation == 'changed-direction':
                    findings = load(r / 'advisor/findings.json')
                    for entry in findings['loops']:
                        if entry['id'].lower() == loop:
                            entry['direction'] = ('statement-only' if entry.get('direction') != 'statement-only'
                                                  else 'single+skeptic')
                    write(r / 'advisor/findings.json', findings)
                elif mutation == 'missing-independent-derivation':
                    name = f'{REL}/skeptic/{loop}-independent-derivation.md'
                    (root / name).unlink(missing_ok=True)
                    rebind(root, loop)
                elif mutation == 'reverse-extra-premise':
                    p = r / f'reverse/{loop}'
                    extra = p / 'inputs' / REL / 'forward' / loop / 'report.md'
                    extra.parent.mkdir(parents=True, exist_ok=True)
                    extra.write_text('A forward report copied into the reverse inputs.\n')
                    name = extra.relative_to(root).as_posix()
                    freeze = load(p / 'freeze.json')
                    freeze['sources'][name] = digest(extra)
                    write(p / 'freeze.json', freeze)
                    gate['bindings'][name] = digest(extra)
                    write(r / f'advisor/{loop}-gate.json', gate)
                    rebind(root, loop)
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
                reason = expect_rejection(root, complete, expected_reasons[mutation], loop + '/' + mutation)
                results.append({'loop': loop, 'mutation': mutation, 'rejected': True, 'reason': reason})
    return results


def main():
    findings = load(ROOT / f'{REL}/advisor/findings.json')
    complete = findings['completed'] == PLANNED
    original = validate(complete=complete)
    loops = [row['id'].lower() for row in original['loops']]
    inherited = inherited_files(original['loops'])
    results = structural_controls(complete, inherited)
    if loops:
        results += loop_controls(loops, complete, inherited)
        per_loop = 'executed for ' + ', '.join(x.upper() for x in loops)
    else:
        per_loop = 'skipped: 0 of %d Round33 loops gated; no loop evidence exists to damage yet' % PLANNED
    print(json.dumps({'status': 'passed', 'gated_loops': len(loops), 'planned_loops': PLANNED,
                      'planned_ids': list(LOOP_IDS), 'per_loop_controls': per_loop,
                      'rejected': len(results), 'controls': results}, indent=2))


if __name__ == '__main__':
    main()
