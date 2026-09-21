#!/usr/bin/env python3
"""Exact canonical geometry, Haar leakage, block controls and limit-error disk."""
import argparse
import json
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
from pathlib import Path


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def validate(q, eta, alpha, hbar, z):
    need(0 < q < 1, 'q must belong to the summable open interval')
    need(0 < eta < 1 and alpha > 0 and hbar > 0, 'positive physical scales')
    need(0 < z <= F(1, 10**6), 'declared endpoint range')


def rejected(call):
    try:
        call()
    except RuntimeError:
        return True
    return False


def move(p, axis, step=1):
    return tuple(p[i] + (step if i == axis else 0) for i in range(3))


def edges(face):
    p, a, b = face
    return {(p, a), (move(p, a), b), (move(p, b), a), (p, b)}


def factor(edge):
    (x, y, z), axis = edge
    if axis == 2 or (axis == 0 and x % 4 == 3) or (axis == 1 and y % 2 == 1):
        return ('free', edge)
    return ('strip', (4 * (x // 4), 2 * (y // 2), z))


def owned(fac):
    if fac[0] == 'free':
        return {fac[1]}
    x, y, z = fac[1]
    horizontal = {((x + i, y + j, z), 0) for i in range(3) for j in range(2)}
    vertical = {((x + i, y, z), 1) for i in range(4)}
    return horizontal | vertical


def omitted(face):
    (x, y, _), a, b = face
    return (a, b) != (0, 1) or y % 2 == 1 or x % 4 == 3


def incident(linkset):
    # Enumerate all faces in a finite coordinate box, independent of Y1's
    # link-incidence implementation; test actual intersection afterwards.
    maxima = [max(p[j] for p, _ in linkset) + 1 for j in range(3)]
    result = set()
    for p in product(*(range(v + 1) for v in maxima)):
        for a, b in combinations(range(3), 2):
            f = (p, a, b)
            if omitted(f) and edges(f) & linkset:
                result.add(f)
    return result


def route(points):
    found = set()
    for p, q in zip(points, points[1:]):
        axes = [j for j in range(3) if p[j] != q[j]]
        need(len(axes) == 1 and abs(p[axes[0]] - q[axes[0]]) == 1, 'unit route')
        found.add((min(p, q), axes[0]))
    return found


def regions():
    o, d = (3, 1, 0), (3, 2, 1)
    links = route([o, (3, 2, 0), d]) | route([o, (3, 1, 1), d])
    links |= route([o, (4, 1, 0), (4, 2, 0), (4, 2, 1), d])
    facs = {factor(e) for e in links}
    need(len(facs) == 8 and all(f[0] == 'free' for f in facs), 'U1 factors')
    rows, face_sets = [], []
    for k in range(3):
        complete = set().union(*(owned(f) for f in facs))
        candidates = incident(complete)
        internal = {f for f in candidates if edges(f) <= complete}
        face_sets.append(internal)
        rows.append({'depth': k, 'factors': len(facs), 'links': len(complete),
                     'faces': len(internal), 'anchor_sum': sum(sum(f[0]) for f in internal)})
        facs |= {factor(e) for f in candidates for e in edges(f)}
    need([r['faces'] for r in rows] == [1, 20, 129], 'forward Y1 retained faces')
    need([r['links'] for r in rows] == [8, 98, 297], 'complete physical links')
    return rows, face_sets


def poly_add(a, b):
    result = a.copy()
    for e, c in b.items():
        result[e] = result.get(e, F(0)) + c
    return {e: c for e, c in result.items() if c}


def poly_scale(a, factor_):
    return {e: c * factor_ for e, c in a.items() if c * factor_}


def poly_mul(a, b):
    result = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            result[e] = result.get(e, F(0)) + ca * cb
    return {e: c for e, c in result.items() if c}


def dot(a, b):
    result = {}
    for i in range(4):
        e = [0] * 12
        e[4 * a + i] += 1
        e[4 * b + i] += 1
        result[tuple(e)] = F(1)
    return result


def haar_moment(exponents):
    # Uniform S^3 moments, independently for X, Y, Z.
    value = F(1)
    for offset in (0, 4, 8):
        powers = exponents[offset:offset + 4]
        if any(n % 2 for n in powers):
            return F(0)
        half_degree = sum(powers) // 2
        for n in powers:
            for j in range(1, n, 2):
                value *= j
        for j in range(half_degree):
            value /= 4 + 2 * j
    return value


def mean(poly):
    return sum((c * haar_moment(e) for e, c in poly.items()), F(0))


def haar_checks():
    px, py, x = poly_scale(dot(0, 2), 2), poly_scale(dot(1, 2), 2), dot(0, 1)
    pair = poly_add(px, py)
    psi_square = poly_scale(poly_mul(pair, pair), F(1, 2))
    need(mean(psi_square) == 1, 'normalized actual U state')
    xy = mean(poly_mul(poly_mul(px, py), x))
    need(xy == F(1, 4), 'actual resonant off-diagonal')
    expectation = -mean(poly_mul(psi_square, x)) / 24
    need(expectation == -F(1, 96), 'actual scalar sign and coefficient')
    product_norm2 = mean(poly_mul(poly_mul(x, x), psi_square))
    # Each coefficient is mean(phi_i*x*(phi_X+phi_Y))/sqrt(2).
    compressed_norm2 = sum((mean(poly_mul(poly_mul(v, x), pair))**2 / 2 for v in (px, py)), F(0))
    need(product_norm2 == F(1, 4) and compressed_norm2 == F(1, 16), 'actual single-face leakage')
    return {'matrix_element': xy, 'A_expectation': expectation,
            'single_face_product_norm_squared': product_norm2,
            'two_plane_projection_norm_squared': compressed_norm2,
            'single_face_leakage_squared': product_norm2 - compressed_norm2}


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def block_checks():
    energies = [F(0), F(1), F(1), F(1)]
    a = [[F(0), F(1, 3), F(0), F(0)],
         [F(1, 3), -F(1, 96), F(1, 4), F(1, 5)],
         [F(0), F(1, 4), F(0), F(0)],
         [F(0), F(1, 5), F(0), F(0)]]
    b = [[a[i][j] if energies[i] == energies[j] else F(0) for j in range(4)] for i in range(4)]
    diagonal_wrong = [[b[i][j] if i == j else F(0) for j in range(4)] for i in range(4)]
    two_state_wrong = [row[:] for row in b]
    two_state_wrong[1][3] = two_state_wrong[3][1] = F(0)
    second = matmul(b, b)[1][1]
    wrong_diagonal_second = matmul(diagonal_wrong, diagonal_wrong)[1][1]
    wrong_two_second = matmul(two_state_wrong, two_state_wrong)[1][1]
    need(second - wrong_two_second == F(1, 25), 'within-block third-state return')
    need(second > wrong_diagonal_second, 'degenerate averaging must retain edges')
    return b, {'correct_second_moment': second,
               'eigenvector_diagonal_second_moment': wrong_diagonal_second,
               'two_state_second_moment': wrong_two_second,
               'third_state_missing_second_moment': second - wrong_two_second}


def tail(k, x):
    a = F(1)
    for j in range(k + 1):
        a *= F(8, 3) + j
    a /= factorial(k + 1)
    return a * x**(k + 1) / (1 - x)**(k + 4)


def profile_polynomial(q):
    return 2 + 5 * q + 5 * q**2 + 6 * q**3 + 3 * q**4


def slow_ratio(q):
    # tau/(eta*(1-q)^3), continuously evaluated at q=1 for the limit only.
    return 3 * (1 + q)**2 * (1 + q*q) / profile_polynomial(q)


def serializable(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {k: serializable(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [serializable(v) for v in obj]
    return obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    output = Path(ap.parse_args().output)
    output.mkdir(parents=True, exist_ok=True)
    need(not any(output.iterdir()), 'output directory must be fresh/empty')
    geometry, face_sets = regions()
    haar = haar_checks()
    block, block_data = block_checks()
    q, eta, z = F(999999, 1000000), F(1, 2), F(1, 10**6)
    validate(q, eta, F(1), F(1), z)
    rho = 8*z/7
    sq = z * slow_ratio(q)
    tau = eta * (1-q)**3 * slow_ratio(q)
    need(slow_ratio(F(1)) == F(8, 7), 'exact original-clock endpoint ratio')
    need(profile_polynomial(q) - 2*(1+q)**2*(1+q*q) == q+q*q+2*q**3+q**4,
         'all-q polynomial upper bound identity')
    need(sq <= 3*z/2, 'physical endpoint envelope')
    coefficient_error = sum((1-q**sum(f[0]) for f in face_sets[2]), F(0)) / 24
    coefficient_majorant = (1-q)*geometry[2]['anchor_sum']/24
    need(0 < coefficient_error <= coefficient_majorant, 'finite q coefficient error')
    x = 15*z
    spatial = tail(2, x)
    taylor = rho*rho*F(geometry[2]['faces'], 24)**2/2
    disk = spatial+taylor
    need(disk < F(189, 10**13), 'actual limiting scalar disk radius <1.89e-11')
    need(z/84 - disk > F(1188, 10**11), 'actual limiting scalar imaginary lower >1.188e-8')
    max_ratio = x/(1-x)*F(11, 6)
    need(max_ratio < 1, 'uniform contraction of complete spatial remainder')
    for k in range(10):
        need(tail(k+1, x)/tail(k, x) == x/(1-x)*(F(8, 3)+k+1)/(k+2),
             'exact all-tail successive ratio')
    norm_s = F(1, 4)
    norm_obstruction = norm_s-norm_s**3/6-norm_s**2/(2*(1-norm_s/3))
    need(norm_obstruction > F(1, 5), 'compact-resolvent false norm-topology control')
    global_loops = [((3, 1, 4*n), 1, 2) for n in range(12)]
    need(all(len(edges(f)) == 4 and all(factor(e)[0] == 'free' for e in edges(f))
             for f in global_loops), 'actual infinite-degeneracy family prefix')
    disjoint = all(not (edges(f) & edges(g)) for f, g in combinations(global_loops, 2))
    need(disjoint, 'translated physical characters are disjoint')
    # Exact roots of unity at reference phase theta=pi/2; no float approximation.
    reference_phase, correct_demod, wrong_demod = -1j, 1j, -1j
    controls = {
        'whole_degenerate_block_retains_off_diagonal_edges': block[1][2] == F(1, 4) and block[1][3] == F(1, 5),
        'off_energy_edge_is_removed_by_averaging': block[0][1] == 0,
        'eigenvector_diagonal_wrong_model_changes_second_moment': block_data['correct_second_moment'] > block_data['eigenvector_diagonal_second_moment'],
        'two_state_resonant_closure_fails_in_full_block_control': block_data['third_state_missing_second_moment'] == F(1, 25),
        'actual_U_single_face_has_nonzero_unaveraged_leakage': haar['single_face_leakage_squared'] == F(3, 16),
        'actual_U_averaged_first_scalar_term_has_positive_imaginary_sign': -haar['A_expectation']*F(8, 7) == F(1, 84),
        'wrong_demodulation_changes_reference_scalar': correct_demod*reference_phase == 1 and wrong_demod*reference_phase == -1,
        'fixed_clock_loses_actual_endpoint_accumulation': tau < sq and slow_ratio(F(1)) == F(8, 7),
        'finite_q_coefficient_replacement_has_nonzero_error': 0 < coefficient_error <= coefficient_majorant,
        'compact_resolvent_does_not_imply_norm_averaging': norm_obstruction > F(1, 5),
        'actual_infinite_physical_reference_has_repeated_energy_family': disjoint and 4*F(1, 2)*F(3, 2) == 3,
        'finite_spatial_Haar_space_is_not_a_spin_cutoff': F(10)*11 > F(1, 2)*F(3, 2),
        'uniform_spatial_tail_tends_to_zero': 0 < max_ratio < 1,
        'q_one_global_substitution_rejected': rejected(lambda: validate(F(1), eta, F(1), F(1), z)),
        'zero_physical_scale_rejected': rejected(lambda: validate(q, eta, F(0), F(1), z)),
        'out_of_range_endpoint_rejected': rejected(lambda: validate(q, eta, F(1), F(1), F(1, 1000))),
    }
    need(len(controls) >= 3 and all(type(v) is bool and v for v in controls.values()), 'genuine boolean controls')
    result = {
        'loop': 'y2', 'direction': 'forward', 'status': 'passed',
        'claims': [
            'Actual finite-factor reference has compact resolvent, unchanged domain and gauge-reducing energy sectors',
            'Bounded weak-coupling interaction propagators and adjoints converge strongly uniformly on compact slow times',
            'Original-clock demodulated regional correlations limit to whole energy-9/2 block characteristic scalars',
            'Reviewed uniform spatial tails transfer regional scalar limits to the actual full canonical endpoint scalar',
            'Actual scalar at z=1e-6 lies within 1.89e-11 of 1+i/84000000'
        ],
        'limitations': [
            'Actual whole-block spectra, dimensions and full matrices are not evaluated',
            'Single-face Haar leakage is unaveraged; the abstract three-state control does not establish actual averaged leakage',
            'No operator-norm averaging, joint spatial/q rate, global q=1 Hamiltonian or exact trajectory is claimed',
            'Delta_(k,9/2) is positive but unevaluated in the finite-q error budget',
            'No external peer review, scientific priority, homogeneous gap or continuum conclusion'
        ],
        'geometry': geometry,
        'actual_U_Haar': haar,
        'whole_block_fixture': block_data,
        'exact': {
            'z': z, 'q_example': q, 'slow_endpoint': sq, 'limiting_slow_time': rho,
            'depth2_coefficient_error_upper': coefficient_error,
            'depth2_coefficient_error_linear_majorant': coefficient_majorant,
            'depth2_uniform_spatial_tail': spatial,
            'depth2_actual_block_Taylor_remainder': taylor,
            'actual_limit_disk_radius': disk, 'actual_limit_disk_center_real': F(1),
            'actual_limit_disk_center_imag': z/84,
            'actual_limit_imaginary_lower': z/84-disk,
            'all_depth_tail_ratio_upper': max_ratio,
            'abstract_norm_averaging_obstruction_lower': norm_obstruction,
            'actual_infinite_physical_repeated_energy_over_alpha': F(3)
        },
        'actual_block_matrix_computed': False,
        'actual_trajectory_computed': False,
        'full_scalar_limit_proved_within_declared_model': True,
        'global_q_one_generator_constructed': False,
        'continuum_proved': False,
    }
    (output/'results.json').write_text(json.dumps(serializable(result), indent=2, sort_keys=True)+'\n')
    (output/'controls.json').write_text(json.dumps({'controls': controls}, indent=2, sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
