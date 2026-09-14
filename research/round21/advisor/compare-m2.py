#!/usr/bin/env python3
"""Compare the independently reviewed M2 invariants and reject altered claims.

The written proof and its scope are admitted separately by the advisor gate.
These constants were reconstructed by the advisor from trace distance, the
complete-factor Duhamel bound, the exact profile and the variance transfer.
"""
import argparse
import copy
import json
from pathlib import Path

EXPECTED = {
    'connected_error_projector_coefficient': '6',
    'fixed_time_error_exponent': '3/2',
    'homogeneous_limit_obtained': False,
    'physical_sector_rechecked': True,
    'time_window_endpoint_included': False,
    'time_window_exponent_upper': '3/2',
    'variance_floor_fixture': '7/64',
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def validate(forward, reverse):
    for direction, data in [('forward', forward), ('reverse', reverse)]:
        if data.get('loop') != 'm2' or data.get('direction') != direction:
            raise ValueError('result identity mismatch')
        if data.get('passed') is not True or data.get('status') is not None:
            raise ValueError('execution status mismatch')
        if canonical(data.get('comparison')) != canonical(EXPECTED):
            raise ValueError('reviewed scientific invariant mismatch')
    if canonical(forward['comparison']) != canonical(reverse['comparison']):
        raise ValueError('independent directions disagree')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--forward', type=Path, required=True)
    parser.add_argument('--reverse', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    originals = [json.loads(args.forward.read_text()), json.loads(args.reverse.read_text())]
    validate(*originals)
    controls = []

    def rejection(side, name, mutation):
        pair = copy.deepcopy(originals)
        mutation(pair[side])
        try:
            validate(*pair)
        except ValueError:
            controls.append({'side': side, 'name': name, 'rejected': True})
        else:
            raise ValueError('altered claim was admitted: ' + name)

    for side in range(2):
        for key, value in EXPECTED.items():
            wrong = not value if type(value) is bool else value + '_wrong'
            rejection(side, key, lambda row, k=key, v=wrong: row['comparison'].__setitem__(k, v))
        rejection(side, 'empty_comparison', lambda row: row.update(comparison={}))
        rejection(side, 'numeric_boolean_pass', lambda row: row.update(passed=1))
        rejection(side, 'unexecuted_status', lambda row: row.update(passed=False))
        rejection(side, 'numeric_boolean_scope', lambda row: row['comparison'].update(physical_sector_rechecked=1))
        rejection(side, 'incorrect_direction', lambda row: row.update(direction='other'))
    result = {
        'loop': 'm2', 'status': 'accepted', 'comparison': EXPECTED,
        'mutation_controls': controls,
        'scope': 'Exact reviewed invariants and independent output agreement; theorem proof and target limits remain in the advisor gate.'
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'm2', 'status': 'accepted', 'mutation_controls': len(controls)}))


if __name__ == '__main__':
    main()
