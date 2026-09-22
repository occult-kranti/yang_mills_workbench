#!/usr/bin/env python3
"""Validate source-bound Round30 records and replay their executed controls.

This verifies provenance, reviewed scope and executed fixtures, not mathematical
truth by hashes. The analytic reports and separate review remain necessary.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
REL = Path('research/round30')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def inventory(directory):
    return {p.relative_to(directory).as_posix(): digest(p)
            for p in sorted(directory.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}


def local(root, name):
    p = root / name
    require(not Path(name).is_absolute() and '..' not in Path(name).parts,
            'Unsafe evidence path')
    component = root
    for part in Path(name).parts:
        component = component / part
        require(not component.is_symlink(), 'Symlink evidence component: ' + str(component))
    require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root.resolve()),
            'Missing or escaping evidence: ' + name)
    return p


def validate(root=ROOT, complete=False):
    r = root / REL
    findings = load(r / 'advisor/findings.json')
    rows = findings['loops']
    require(findings['completed'] == len(rows), 'Wrong execution count')
    require(len(rows) == 3 if complete else 0 < len(rows) <= 3, 'Three-loop stop boundary')
    require(len({x['id'] for x in rows}) == len(rows), 'Duplicate loop')
    spec = load(r / 'advisor/admission-spec.json')
    for sequence, row in enumerate(rows, 1):
        loop = row['id'].lower()
        gate = load(r / f'advisor/{loop}-gate.json')
        require(gate['sequence'] == sequence == row['sequence'], 'Wrong adaptive sequence')
        require(gate['accepted'] == row['accepted'] and gate['limitations'] == row['limitations'],
                'Presentation expands gate')
        require(gate['verdict'] in ('accepted_within_scope', 'limited', 'insufficient'), 'Unknown verdict')
        require(gate['accepted'] and gate['limitations'], 'Missing scope')
        fixed = spec['loops'][loop]
        for key in ('accepted', 'limitations', 'verdict'):
            require(gate[key] == fixed[key], 'Changed reviewed semantics: ' + key)
        required = {str(REL / f'contracts/{loop}.json'),
                    str(REL / f'skeptic/{loop}.json'),
                    str(REL / f'skeptic/{loop}.md')}
        for side in ('forward', 'reverse'):
            p = r / side / loop
            require(not any('__pycache__' in q.parts or q.suffix == '.pyc'
                            for q in p.rglob('*')), 'Interpreter cache in producer closure')
            freeze = load(p / 'freeze.json')
            require(freeze['loop'].lower() == loop and freeze['direction'] == side, 'Bad freeze identity')
            actual_files = {str(q.relative_to(root)) for q in p.rglob('*') if q.is_file()
                            and q.name != 'freeze.json' and '__pycache__' not in q.parts}
            require(actual_files == set(freeze['sources']), 'Incomplete freeze inventory')
            required_producer = {str(REL / side / loop / name)
                                 for name in ('report.md', 'check.py', 'output/results.json', 'inputs/AGENTS.md')}
            require(required_producer <= set(freeze['sources']), 'Missing required producer source')
            for name, sha in freeze['sources'].items():
                require(digest(local(root, name)) == sha, 'Changed frozen source: ' + name)
            required |= required_producer | set(freeze['sources']) | {str(REL / side / loop / 'freeze.json')}
            expected_contract = p / 'inputs' / REL / 'contracts' / (loop + '.json')
            require(expected_contract.is_file() and expected_contract.read_bytes() == (r / f'contracts/{loop}.json').read_bytes(),
                    'Missing or changed prospective contract snapshot')
            result = load(p / 'output/results.json')
            checks = result['checks']
            require(all(isinstance(x, dict) and x.get('passed') is True
                        and isinstance(x.get('id'), str) for x in checks),
                    'Missing or failed executed control status')
            ids = [x['id'] for x in checks]
            require(ids and len(ids) == len(set(ids)), 'Empty or duplicate executed checks')
            require(ids == fixed[side]['check_ids'], 'Removed or changed reviewed controls')
            for key, value in fixed[side]['claims'].items():
                require(result.get(key) == value, 'Changed claim: ' + key)
        require(required <= set(gate['bindings']), 'Gate omits required evidence')
        for name, sha in gate['bindings'].items():
            require(digest(local(root, name)) == sha, 'Changed admitted evidence: ' + name)
        review = load(r / f'skeptic/{loop}.json')
        require(review.get('blocking_issues') == [], 'Missing or blocking skeptical review')
        require(review.get('supported_statement') == gate['accepted']
                and review.get('limitations') == gate['limitations'],
                'Admission differs from reviewed scientific scope')
        for side in ('forward', 'reverse'):
            report_name = str(REL / side / loop / 'report.md')
            require(report_name in json.dumps(review), 'Review omits a counterpart')
    return findings


def replay(root, findings, output, optimized=False):
    require(output.is_absolute() and not output.exists(), 'Use fresh absolute replay output')
    require(not output.resolve().is_relative_to(root.resolve()), 'Replay outside source tree')
    output.mkdir(parents=True)
    runs = []
    for row in findings['loops']:
        loop = row['id'].lower()
        for side in ('forward', 'reverse'):
            p = root / REL / side / loop
            target = output / side / loop
            cmd = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(p / 'check.py'), '--output', str(target)]
            done = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
            require(done.returncode == 0, f'{side}/{loop}: {done.stderr}')
            require(inventory(target) == inventory(p / 'output'), 'Changed replay bytes: ' + side + '/' + loop)
            runs.append({'loop': loop, 'side': side, 'output': inventory(target)})
    receipt = {'status': 'passed', 'research_loops': len(findings['loops']),
               'optimized': optimized, 'producer_replays': len(runs), 'runs': runs}
    (output / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return receipt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--complete', action='store_true')
    ap.add_argument('--validate-only', action='store_true')
    ap.add_argument('--optimized', action='store_true')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    findings = validate(complete=args.complete)
    if args.validate_only:
        print(json.dumps({'status': 'passed', 'validated_loops': len(findings['loops'])}))
    else:
        require(args.output is not None, '--output required')
        receipt = replay(ROOT, findings, args.output, args.optimized)
        print(json.dumps({k: v for k, v in receipt.items() if k != 'runs'}))


if __name__ == '__main__':
    main()
