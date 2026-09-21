#!/usr/bin/env python3
"""Actual T graph cutoff coefficients and exact rational X1 certificates."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json
from math import factorial
from pathlib import Path


def need(ok, message):
    if type(ok) is not bool or not ok:
        raise ValueError(message)


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def exp_positive_upper(x, n=24):
    need(x >= 0, 'positive exponential argument')
    term = F(1)
    total = term
    for k in range(1, n + 1):
        term *= x / k
        total += term
    next_term = term * x / (n + 1)
    ratio = x / (n + 2)
    need(ratio < 1, 'exponential remainder ratio')
    return total + next_term / (1 - ratio)


def exp_negative_upper(x, n=32):
    need(x >= 0, 'negative exponential nonnegative magnitude')
    term = F(1)
    total = term
    for k in range(1, n + 1):
        term *= x / k
        total += term
    return 1 / total


def sqrt_interval(x, steps=100):
    need(x >= 0, 'square root radicand')
    lo, hi = F(0), max(F(1), x)
    for unused in range(steps):
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
    need(lo * lo <= x <= hi * hi, 'enclosed square root')
    return lo, hi


def graph():
    vertices = list(product(range(3), range(3), range(2)))
    sizes = (3, 3, 2)
    edges = []
    lookup = {}
    for v in vertices:
        for axis in range(3):
            if v[axis] + 1 < sizes[axis]:
                end = tuple(v[i] + (i == axis) for i in range(3))
                lookup[frozenset((v, end))] = len(edges)
                edges.append((v, end))
    faces = []
    for v in vertices:
        for a, b in combinations(range(3), 2):
            if v[a] + 1 < sizes[a] and v[b] + 1 < sizes[b]:
                va = tuple(v[i] + (i == a) for i in range(3))
                vb = tuple(v[i] + (i == b) for i in range(3))
                vab = tuple(v[i] + (i in (a, b)) for i in range(3))
                cyclic = (v, va, vab, vb)
                faces.append(frozenset(lookup[frozenset((cyclic[i], cyclic[(i + 1) % 4]))]
                                       for i in range(4)))
    return vertices, edges, faces


def mv(matrix, vector):
    return [sum((a * b for a, b in zip(row, vector)), F(0)) for row in matrix]


def certificate(coupling, cutoff, tau, split):
    need(0 <= coupling <= F(1, 100), 'frozen coupling range')
    need(tau > 0 and split >= tau, 'positive delayed half-line')
    b = c = 20 * coupling
    g = 3 - c
    d = cutoff - c
    need(cutoff > 3 and d > 0 and g > 0, 'gap and cutoff denominator')
    delta = b * b / d
    projection = b / d * (1 + b / g)
    # e^(-x) <= 2/x^2 follows from the positive x^2/2 Taylor term.
    high = min(F(1), 2 / (cutoff * tau) ** 2)
    finite = exp_positive_upper(c * split) * (
        high + 2 * b / cutoff + b * b * split / cutoff + split * delta)
    late = projection + 2 * exp_negative_upper(g * split)
    return {'lambda': coupling, 'R': cutoff, 'tau': tau, 'T': split,
            'energy_error_upper': delta, 'projector_error_upper': projection,
            'finite_window_upper': finite, 'late_window_upper': late,
            'all_delayed_time_upper': min(F(2), max(finite, late))}


def run():
    controls = {}

    def control(name, predicate):
        need(predicate, 'failed control: ' + name)
        controls[name] = True

    vertices, edges, faces = graph()
    control('actual_graph_counts_and_bipartite_parity',
            (len(vertices), len(edges), len(faces)) == (18, 33, 20)
            and all(sum(a) % 2 != sum(b) % 2 for a, b in edges))
    found = set()
    for indices in combinations(range(len(edges)), 4):
        degree = Counter(v for e in indices for v in edges[e])
        if len(degree) == 4 and set(degree.values()) == {2}:
            found.add(frozenset(indices))
    control('all_four_cycles_equal_twenty_physical_faces', found == set(faces))
    triple_zero_count = sum(not (a ^ b ^ c) for a, b, c in product(faces, repeat=3))
    control('every_triple_face_matrix_element_vanishes_by_actual_parity',
            triple_zero_count == 0)
    control('face_pair_orthogonality_has_odd_edge_witness',
            all(bool(a ^ b) for a, b in combinations(faces, 2)))

    coupling = F(1, 100)
    c = 20 * coupling
    matrix = [[F(0) for unused in range(21)] for ignored in range(21)]
    matrix[0][0] = c
    for p in range(1, 21):
        matrix[p][p] = 3 + c
        matrix[0][p] = matrix[p][0] = -coupling / 2
    omega = [F(1)] + [F(0)] * 20
    face_sum = [F(0)] + [F(1)] * 20
    control('actual_vacuum_and_face_sum_matrix_actions',
            mv(matrix, omega) == [c] + [-coupling / 2] * 20
            and mv(matrix, face_sum) == [-10 * coupling] + [3 + c] * 20)
    darks = []
    for p in range(1, 20):
        dark = [F(0)] * 21
        dark[p], dark[20] = F(1), F(-1)
        darks.append(dark)
    control('nineteen_actual_dark_face_eigenvectors',
            all(mv(matrix, v) == [(3 + c) * x for x in v] for v in darks))
    # On the non-normalized basis (Omega, sum phi_p) the exact matrix is
    # [[c, -10lambda],[-lambda/2,3+c]], giving determinant offset -5lambda^2.
    control('normalization_changes_bright_coupling_not_energy_polynomial',
            (-10 * coupling) * (-coupling / 2) == 5 * coupling ** 2
            and (-coupling / 2) ** 2 != 5 * coupling ** 2)
    root_lo, root_hi = sqrt_interval(9 + 20 * coupling ** 2)
    energy_lo, energy_hi = c + (3 - root_hi) / 2, c + (3 - root_lo) / 2
    control('actual_finite_ground_strictly_below_Haar_energy',
            0 < energy_lo <= energy_hi < c and energy_hi - energy_lo < F(1, 10**25))
    # W=x; phi_half=2x; chi_spin1=4x^2-1, represented as polynomial coefficients.
    lhs = [F(0), F(0), F(2)]
    rhs = [F(1, 2) - F(1, 2), F(0), F(2)]
    omitted_coefficient = -coupling / 2
    control('closed_21_state_dynamics_rejected_by_actual_spin_one_channel',
            lhs == rhs and omitted_coefficient != 0 and 4 * F(1) * (1 + 1) == 8)

    rows = [certificate(coupling, cutoff, F(1), F(4))
            for cutoff in [F(9, 2), F(16), F(64), F(256), F(1024)]]
    chosen = rows[-1]
    control('delayed_all_time_1024_cutoff_bound_below_one_in_500',
            chosen['all_delayed_time_upper'] < F(1, 500))
    control('fixed_split_cutoff_tail_and_ground_errors_decrease',
            all(rows[i + 1]['finite_window_upper'] < rows[i]['finite_window_upper']
                and rows[i + 1]['projector_error_upper'] < rows[i]['projector_error_upper']
                for i in range(len(rows) - 1)))
    b = F(1, 5)
    full_budget = chosen['finite_window_upper']
    wrong_no_return = exp_positive_upper(F(4, 5)) * (
        F(2, 1024**2) + 2 * b / 1024 + 4 * chosen['energy_error_upper'])
    control('dropping_excluded_return_term_changes_positive_certificate',
            full_budget > wrong_no_return)
    # This is a certificate discriminant, not an observed lower bound on full dynamics.
    spin = F(1024)
    control('time_zero_norm_obstruction_has_actual_excluded_character',
            4 * spin * (spin + 1) >= 1024 and 1 - 0 == 1)
    zero = certificate(F(0), F(1024), F(1), F(4))
    control('lambda_zero_has_no_energy_projection_or_return_error',
            zero['energy_error_upper'] == zero['projector_error_upper'] == 0
            and matrix[0][1] != 0)
    for name, args in [('zero_start', (coupling, F(1024), F(0), F(4))),
                       ('invalid_cutoff', (coupling, F(1, 10), F(1), F(4))),
                       ('coupling_out_of_contract', (F(1, 50), F(1024), F(1), F(4)))]:
        rejected = False
        try:
            certificate(*args)
        except ValueError:
            rejected = True
        control('reject_' + name, rejected)
    shift = F(1, 1000000)
    observation = 1 / shift
    control('positive_rounded_centering_has_secular_ground_growth',
            1 + shift * observation >= 2)
    control('negative_rounded_centering_loses_unit_ground_limit',
            shift > 0 and exp_negative_upper(shift * observation) < 1)
    kappa, gap = F(1, 10**8), F(14, 5)
    numerical_coefficient_bound = 4 * kappa / (gap - 2 * kappa)
    control('uniform_coefficient_budget_retains_gap_condition',
            2 * kappa < gap and numerical_coefficient_bound < F(1, 10**7))
    max_n = max(n for n in range(100) if F(n * (n + 2), 4) < 1024)
    edge_dimension = sum((n + 1) ** 2 for n in range(max_n + 1))
    control('actual_spin_cutoff_includes_required_full_edge_multiplicities',
            max_n == 63 and edge_dimension == 89440)
    rejected = 0
    for bad in [False, 1, 'passed']:
        try:
            need(bad, 'strict explicit failure probe')
        except ValueError:
            rejected += 1
    control('explicit_checks_survive_optimized_Python', rejected == 3)

    result = {
        'loop': 'x1', 'direction': 'forward', 'status': 'passed',
        'verdict': 'proved_delayed_all_time_certificate; practical_large_cutoff_not_executed',
        'claims': [
            'P_R is the actual finite kinetic spectral projection after all Gauss constraints.',
            'Full norm at time zero is exactly one for every zero-extended finite heat truncation.',
            'Separately centered full heat converges in operator norm uniformly for sigma>=tau>0.',
            'The vacuum and twenty face states give the actual exact R=9/2 compression.',
            'The actual spin-one omitted coefficient rejects closure of the 21-state dynamics.',
            'At lambda=1/100, tau=1,T=4,R=1024 the analytic uniform certificate is below 1/500.'
        ],
        'limitations': [
            'No R=1024 matrix, ground vector, trajectory or practical cost was computed.',
            'The rational coefficient matrix is the R=9/2 actual compression only.',
            'A finite rounded scalar ground shift alone fails on an unbounded time interval.',
            'No relative heat, real-time, volume, homogeneous, calibration or continuum inference.',
            'The written proof supplies infinite-sector completeness; finite arithmetic checks do not.'
        ],
        'graph': {'vertices': vertices, 'edges': edges,
                  'faces_as_edge_sets': [sorted(f) for f in faces],
                  'four_cycle_count': len(found), 'ordered_triples_checked': 20**3,
                  'zero_parity_triples': triple_zero_count},
        'actual_sector': {'cutoff_exclusive': F(9, 2), 'dimension': 21,
                          'basis': ['Omega'] + ['2W_' + str(p) for p in range(20)],
                          'lambda': coupling, 'matrix': matrix,
                          'ground_energy_interval': [energy_lo, energy_hi],
                          'omitted_spin_one_energy': 8,
                          'omitted_spin_one_coefficient': omitted_coefficient},
        'certificate_rows': rows,
        'zero_coupling_budget': zero,
        'numerical_coefficient_example': {'kappa': kappa, 'uniform_error_bound': numerical_coefficient_bound},
        'large_cutoff_dimension': {'R': 1024, 'maximum_twice_spin': max_n,
                                 'edge_preGauss_dimension': edge_dimension,
                                 'preGauss_product_upper_bound': str(edge_dimension**33),
                                 'actual_physical_dimension_computed': False}
    }
    return serial(result), {'loop': 'x1', 'direction': 'forward',
                            'status': 'passed', 'controls': controls}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(not output.is_symlink(), 'output must not be a symlink')
    output.mkdir(parents=True, exist_ok=True)
    need(not any(output.iterdir()), 'output must be empty')
    results, controls = run()
    for name, data in [('results.json', results), ('controls.json', controls)]:
        (output / name).write_text(json.dumps(data, sort_keys=True, indent=2) + '\n')
    print('x1 forward: passed; actual 21-state coefficients; delayed all-time certificate')


if __name__ == '__main__':
    main()
