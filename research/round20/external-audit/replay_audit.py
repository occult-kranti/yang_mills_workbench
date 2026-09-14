#!/usr/bin/env python3
"""Reproduce ten admitted loops and compare independent audit calculations.

Run only after all ten gates exist. The output is an arithmetic/source audit,
not certification of the operator-theoretic arguments reviewed in report.md.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ROUND = HERE.parent
LOOPS = ['d1', 'd2', 'e1', 'e2', 'f1', 'f2', 'g1', 'g2', 'h1', 'h2']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(cmd):
    run = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if run.returncode:
        raise RuntimeError(run.stdout + run.stderr)
    return run.stdout.strip()


def compare_external_rays(independent):
    audit_rows = independent['two_witness_variance_audit']['ray_fixtures']
    expected = {(F(v['q']), F(v['eta'])): v for v in audit_rows}
    counts = {}
    for direction in ('forward', 'reverse'):
        data = json.loads((ROUND/direction/'h2/output/results.json').read_text())
        rows = data['ray_fixtures' if direction == 'forward' else 'rows']
        count = 0
        for actual in rows:
            key = F(actual['q']), F(actual['eta'])
            if key not in expected:
                continue
            wanted = expected[key]
            pairs = [(actual['tau'], wanted['tau'])]
            if direction == 'forward':
                pairs += [(actual['variance_over_alpha_squared'], wanted['variance_over_alpha_squared']),
                          (actual['projector_error_squared'], wanted['projector_distance_squared_bound']),
                          (-F(actual['energy_lower_over_alpha']), wanted['ground_energy_magnitude_bound_over_alpha']),
                          (actual['operator_norm_over_alpha'], wanted['constant_operator_norm_over_alpha'])]
            else:
                # Reverse uses alpha/E_star=2; external exact values use alpha units.
                pairs += [(F(actual['exact_sigma_squared_over_E_star_squared'])/4, wanted['variance_over_alpha_squared']),
                          (actual['projector_norm_squared_upper'], wanted['projector_distance_squared_bound']),
                          (F(actual['negative_ground_energy_bound_over_E_star'])/2, wanted['ground_energy_magnitude_bound_over_alpha']),
                          (F(actual['operator_norm_over_E_star'])/2, wanted['constant_operator_norm_over_alpha'])]
            if any(F(a) != F(b) for a, b in pairs):
                raise ValueError('independent H2 ray disagreement: '+direction+' '+str(key))
            count += 1
        counts[direction] = count
    if counts != {'forward': 10, 'reverse': 15}:
        raise ValueError('unexpected H2 shared fixture inventory')
    return {'shared_ray_rows':counts, 'exact_quantities_per_row':5,
            'scale_conversion':'reverse alpha/E_star=2 checked explicitly',
            'expected_values_origin':'external checker; no producer implementation imported'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True,
                        help='Fresh scratch directory outside the repository')
    parser.add_argument('--evidence', type=Path, required=True,
                        help='File receiving durable audit metadata')
    args = parser.parse_args()
    scratch = args.output.resolve()
    if scratch.exists() or ROOT == scratch or ROOT in scratch.parents:
        raise ValueError('fresh scratch directory outside repository required')
    for loop in LOOPS:
        if not (ROUND/'advisor'/f'{loop}-gate.json').is_file():
            raise ValueError('loop gate not available: '+loop)
    scratch.mkdir(parents=True)
    replays = {}
    for mode in ('ordinary', 'optimized'):
        target = scratch/mode
        cmd = [sys.executable, '-B', str(ROUND/'reproduce.py'), '--output', str(target), '--loops', *LOOPS]
        if mode == 'optimized':
            cmd.append('--optimized')
        execute(cmd)
        replays[mode] = json.loads((target/'reproduction.json').read_text())
        independent_target = scratch/f'independent-{mode}.json'
        cmd = [sys.executable, '-B'] + (['-O'] if mode == 'optimized' else [])
        execute(cmd + [str(HERE/'check_independent.py'), '--output', str(independent_target)])
    ordinary = scratch/'independent-ordinary.json'
    optimized = scratch/'independent-optimized.json'
    if ordinary.read_bytes() != optimized.read_bytes():
        raise ValueError('external checker ordinary/optimized drift')
    if ordinary.read_bytes() != (HERE/'independent-results.json').read_bytes():
        raise ValueError('external checker saved result drift')
    independent = json.loads(ordinary.read_text())
    comparison = compare_external_rays(independent)
    sources = [HERE/'report.md', HERE/'check_independent.py', HERE/'replay_audit.py',
               HERE/'independent-results.json', ROUND/'reproduce.py',
               ROUND/'advisor/f-conditional-space-clarification.md']
    sources += [ROUND/'advisor'/f'{loop}-gate.json' for loop in LOOPS]
    result = {'status':'completed', 'accepted_research_loops':LOOPS,
              'replays':replays, 'executions':40, 'additional_research_loops_from_replays':0,
              'independent_checker_ordinary_optimized_identical':True,
              'external_H2_comparison':comparison,
              'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in sources},
              'assessment':'No unresolved implication error found within the reviewed narrowed claims; see report.md',
              'not_supplied':['human peer review', 'proof-assistant formalization',
                              'exhaustive literature-priority audit', 'continuum Yang-Mills construction']}
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status':'completed', 'research_loops':10,
                      'producer_executions':40, 'external_ray_comparison':comparison['shared_ray_rows']}))


if __name__ == '__main__':
    main()
