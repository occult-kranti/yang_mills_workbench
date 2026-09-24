#!/usr/bin/env python3
"""Validate source-bound Round33 records and replay their executed controls.

This verifies provenance, reviewed scope and executed fixtures, not mathematical
truth by hashes. The analytic reports and separate review remain necessary.

Round33 is a four-sub-round, eight-investigation cycle: three research
sub-rounds (BA1/BA2, BB1/BB2, BC1/BC2) and an applications stage (BD1/BD2).
Each investigation declares one direction in its frozen contract:

  paired             forward and reverse producers;
  single+skeptic     one forward producer and an independent skeptic replay;
  statement+skeptic  one forward statement producer and an independent skeptic replay;
  statement-only     one forward statement producer.

Every single-direction loop (forward producer only) must declare
single_direction_independent_replay in the trusted admission specification and
bind skeptic/<loop>-independent-derivation.md in its gate. --validate-only
passes with zero gated loops while the cycle is in progress; --complete
requires all eight loops and advisor/plan.json with its four sub-rounds in order.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
REL = Path('research/round33')
AUTHOR = 'Hruday N M (BUNZEEY)'
LOOP_IDS = ('ba1', 'ba2', 'bb1', 'bb2', 'bc1', 'bc2', 'bd1', 'bd2')
PLANNED = len(LOOP_IDS)
SUBROUNDS = 4
DIRECTIONS = {
    'paired': ['forward', 'reverse'],
    'single+skeptic': ['forward'],
    'statement+skeptic': ['forward'],
    'statement-only': ['forward'],
}


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
    require(findings.get('human_author') == AUTHOR, 'Wrong findings author')
    require(findings.get('requested') == PLANNED, 'Findings do not request eight investigations')
    rows = findings['loops']
    require(isinstance(rows, list) and findings['completed'] == len(rows), 'Wrong execution count')
    require(len(rows) == PLANNED if complete else 0 <= len(rows) <= PLANNED, 'Eight-loop stop boundary')
    require(len({x['id'] for x in rows}) == len(rows), 'Duplicate loop')
    spec = load(r / 'advisor/admission-spec.json')
    require(isinstance(spec.get('loops'), dict), 'Invalid admission specification')
    for sequence, row in enumerate(rows, 1):
        loop = row['id'].lower()
        require(loop == LOOP_IDS[sequence - 1], 'Wrong loop identifier for sequence ' + str(sequence))
        gate = load(r / f'advisor/{loop}-gate.json')
        require(gate['sequence'] == sequence == row['sequence'], 'Wrong adaptive sequence')
        require(gate['subround'] == row['subround'] == (sequence + 1) // 2, 'Wrong sub-round')
        require(gate['accepted'] == row['accepted'] and gate['limitations'] == row['limitations'],
                'Presentation expands gate')
        require(gate['verdict'] in ('accepted_within_scope', 'limited', 'insufficient'), 'Unknown verdict')
        require(gate['accepted'] and gate['limitations'], 'Missing scope')
        require(loop in spec['loops'], 'Admission specification omits gated loop ' + loop)
        fixed = spec['loops'][loop]
        for key in ('accepted', 'limitations', 'verdict', 'producers'):
            require(gate[key] == fixed[key], 'Changed reviewed semantics: ' + key)
        producers = gate['producers']
        require(producers in (['forward', 'reverse'], ['forward']), 'Unknown producer set')
        contract_path = r / f'contracts/{loop}.json'
        contract_now = load(contract_path)
        direction = contract_now.get('direction')
        require(direction in DIRECTIONS, 'Unknown direction: ' + str(direction))
        require(row.get('direction') == direction, 'Findings direction differs from the frozen contract')
        require(DIRECTIONS[direction] == producers and contract_now.get('producers') == producers,
                'Direction and producer set disagree')
        required = {str(REL / f'contracts/{loop}.json'),
                    str(REL / f'skeptic/{loop}.json'),
                    str(REL / f'skeptic/{loop}.md')}
        if producers == ['forward']:
            require(fixed.get('single_direction_independent_replay') is True,
                    'Single-direction loop lacks declared independent skeptic replay')
            require(str(REL / f'skeptic/{loop}-independent-derivation.md') in gate['bindings'],
                    'Single-direction loop lacks independent skeptic derivation')
        for side in producers:
            p = r / side / loop
            require(not any('__pycache__' in q.parts or q.suffix == '.pyc'
                            for q in p.rglob('*')), 'Interpreter cache in producer closure')
            freeze = load(p / 'freeze.json')
            require(freeze['loop'].lower() == loop and freeze['direction'] == side, 'Bad freeze identity')
            actual_files = {str(q.relative_to(root)) for q in p.rglob('*') if q.is_file()
                            and q != p / 'freeze.json' and '__pycache__' not in q.parts}
            require(actual_files == set(freeze['sources']), 'Incomplete freeze inventory')
            required_producer = {str(REL / side / loop / name)
                                 for name in ('report.md', 'check.py', 'output/results.json', 'inputs/AGENTS.md')}
            require(required_producer <= set(freeze['sources']), 'Missing required producer source')
            for name, sha in freeze['sources'].items():
                require(digest(local(root, name)) == sha, 'Changed frozen source: ' + name)
            required |= required_producer | set(freeze['sources']) | {str(REL / side / loop / 'freeze.json')}
            expected_contract = p / 'inputs' / REL / 'contracts' / (loop + '.json')
            require(expected_contract.is_file() and expected_contract.read_bytes() == contract_path.read_bytes(),
                    'Missing or changed prospective contract snapshot')
            contract = load(expected_contract)
            require(contract.get('status') == 'frozen_before_production', 'Unfrozen contract')
            require(freeze['contract_sha256'] == digest(contract_path), 'Freeze bound to a different contract')
            for premise in contract.get('shared_premises', []):
                original = local(root, premise)
                snapshot_name = str(REL / side / loop / 'inputs' / premise)
                snapshot = local(root, snapshot_name)
                require(snapshot.read_bytes() == original.read_bytes(),
                        'Missing or changed declared premise snapshot: ' + premise)
                require(snapshot_name in freeze['sources'], 'Unbound premise snapshot')
            if side == 'reverse' and contract.get('reverse_premise_isolation'):
                allowed = {'AGENTS.md', str(REL / f'contracts/{loop}.json')} | set(contract.get('shared_premises', []))
                actual_inputs = {q.relative_to(p / 'inputs').as_posix() for q in (p / 'inputs').rglob('*') if q.is_file()}
                require(actual_inputs == allowed, 'Reverse premise isolation violated: ' + str(sorted(actual_inputs ^ allowed)[:6]))
            if side == 'forward':
                for premise in contract.get('forward_additional_premises', []):
                    snapshot_name = str(REL / side / loop / 'inputs' / premise)
                    require(local(root, snapshot_name).read_bytes() == local(root, premise).read_bytes(),
                            'Missing or changed forward additional premise snapshot: ' + premise)
                    require(snapshot_name in freeze['sources'], 'Unbound premise snapshot')
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
        for side in producers:
            report_name = str(REL / side / loop / 'report.md')
            require(report_name in json.dumps(review), 'Review omits a counterpart')
    if complete:
        subrounds = load(r / 'advisor/plan.json')['subrounds']
        require(len(subrounds) == SUBROUNDS
                and [x.get('id') for x in subrounds] == list(range(1, SUBROUNDS + 1))
                and [x['id'].lower() for x in rows] ==
                [lid.lower() for s in subrounds for lid in s['loops']], 'Plan and findings disagree')
    return findings


def replay(root, findings, output, optimized=False):
    require(output.is_absolute() and not output.exists(), 'Use fresh absolute replay output')
    require(not output.resolve().is_relative_to(root.resolve()), 'Replay outside source tree')
    output.mkdir(parents=True)
    runs = []
    spec = load(root / REL / 'advisor/admission-spec.json')
    for row in findings['loops']:
        loop = row['id'].lower()
        for side in spec['loops'][loop]['producers']:
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
        print(json.dumps({'status': 'passed', 'validated_loops': len(findings['loops']),
                          'planned_loops': PLANNED, 'complete': len(findings['loops']) == PLANNED}))
    else:
        require(args.output is not None, '--output required')
        receipt = replay(ROOT, findings, args.output, args.optimized)
        print(json.dumps({k: v for k, v in receipt.items() if k != 'runs'}))


if __name__ == '__main__':
    main()
