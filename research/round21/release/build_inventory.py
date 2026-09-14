#!/usr/bin/env python3
"""Generate a CANDIDATE inventory for separate review; never validate/admit it.

This command cannot update the validator's trust anchor. Review the candidate
and deliberately pin its digest in replay_c2.py before performing validation.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R19 = 'research/round19/'
LOOPS = ('a1', 'a2', 'b1', 'b2', 'c1', 'c2')
EXCLUDED = R19 + 'backward/c2/history/pre-round20-validator-audit/__pycache__/compare.cpython-312.pyc'
EXCLUDED_SHA = 'ca7c11234bc4224161caa1eb442e1cacb731c109a832e208025c5a184bee6cca'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise ValueError('candidate destination must be new')
    files = {}
    missing = {}
    gates = {}
    for loop in LOOPS:
        name = R19 + 'advisor/' + loop + '-gate.json'
        gate = json.loads((ROOT/name).read_text())
        if gate['loop'] != loop or gate['status'] not in ('accepted', 'limited'):
            raise ValueError('unexpected historical gate')
        gates[name] = digest(ROOT/name)
        for rel, expected in gate['files'].items():
            name = R19 + rel
            if name in files and files[name] != expected:
                raise ValueError('conflicting historical expected hashes')
            p = ROOT/name
            if not p.is_file():
                missing[name] = expected
            elif digest(p) != expected:
                raise ValueError('historical drift: ' + name)
            files[name] = expected
    if missing != {EXCLUDED: EXCLUDED_SHA}:
        raise ValueError('historical defect differs from reviewed single cache omission')
    del files[EXCLUDED]
    files.update(gates)
    for name in (R19+'execution.json', R19+'reproduce.py'):
        files[name] = digest(ROOT/name)
    # Actual C2 imports and every producer-declared scientific input must occur.
    required = [R19 + role + '/c1/check.py' for role in ('forward', 'backward')]
    for role in ('forward', 'backward'):
        m = json.loads((ROOT/(R19+role+'/c2/output/source-manifest.json')).read_text())
        required += list(m['source_inputs'])
    if not set(required) <= files.keys():
        raise ValueError('scientific dependency absent from candidate inventory')
    spec = json.loads((ROOT/(R19+'execution.json')).read_text())['loops']['c2']['tasks']
    outputs = {}
    for task in spec[:2]:
        outputs[task['name']] = {name: files[R19+task['accepted_output']+'/'+name]
                                for name in task['identical_files']}
    result = {
        'schema': 'ym21-c2-reviewed-inventory-v1',
        'purpose': 'new C2 admission inventory; historical gates unchanged; zero new research loops',
        'files': dict(sorted(files.items())),
        'historical_gates': gates,
        'required_scientific_inputs': sorted(set(required)),
        'excluded': {EXCLUDED: {
            'historical_expected_sha256': EXCLUDED_SHA,
            'reason': 'Untracked CPython 3.12 interpreter cache of an archived comparator. The current comparator and both archived .py sources remain bound; C2 imports neither this cache nor its archived module. Exclusion applies only to this new inventory.'}},
        'expected_outputs': outputs,
        'comparison_expected': R19+'backward/c2/comparison/comparison.json',
        'comparison_volatile_fields': ['producer_source', 'producer_evidence'],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'candidate_sha256': digest(args.output), 'bound_files': len(files),
                      'excluded_files': 1, 'admitted': False}))


if __name__ == '__main__':
    main()
