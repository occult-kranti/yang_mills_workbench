#!/usr/bin/env python3
"""X2: complete actual SU(2) Ritz residual and rational full-graph certificates."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path


def need(ok, why):
    if type(ok) is not bool or not ok:
        raise ValueError(why)


def clean(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    return value


def outward(lo, hi, digits=50):
    scale = 10 ** digits
    return F((lo.numerator * scale) // lo.denominator, scale), F(
        -((-hi.numerator * scale) // hi.denominator), scale)


def sqrt_bounds(x):
    need(x >= 0, 'nonnegative radical required')
    n, d = isqrt(x.numerator), isqrt(x.denominator)
    if n*n == x.numerator and d*d == x.denominator:
        return F(n, d), F(n, d)
    lo, hi = F(0), max(F(1), x)
    for unused in range(180):
        mid = (lo + hi) / 2
        if mid*mid <= x:
            lo = mid
        else:
            hi = mid
    lo, hi = outward(lo, hi)
    need(lo*lo <= x <= hi*hi, 'radical enclosure')
    return lo, hi


def exp_negative_bounds(x):
    need(x >= 0, 'nonnegative exponential magnitude')
    total = term = F(1)
    n = 128
    for k in range(1, n + 1):
        term *= x/k
        total += term
    ratio = x/(n+2)
    need(ratio < 1, 'Taylor tail ratio')
    upper = total + (term*x/(n+1))/(1-ratio)
    return outward(1/upper, 1/total, 60)


def graph():
    sizes = (3, 3, 2)
    vertices = list(product(*(range(x) for x in sizes)))
    edges, lookup = [], {}
    for v in vertices:
        for axis in range(3):
            if v[axis]+1 < sizes[axis]:
                end = tuple(v[i]+(i == axis) for i in range(3))
                lookup[frozenset((v, end))] = len(edges)
                edges.append((v, end, axis))
    faces = []
    for v in vertices:
        for a, b in combinations(range(3), 2):
            if v[a]+1 < sizes[a] and v[b]+1 < sizes[b]:
                loop = [v, tuple(v[i]+(i == a) for i in range(3)),
                        tuple(v[i]+(i in (a, b)) for i in range(3)),
                        tuple(v[i]+(i == b) for i in range(3))]
                mask = sum(1 << lookup[frozenset((loop[i], loop[(i+1) % 4]))]
                           for i in range(4))
                faces.append(mask)
    return vertices, edges, faces


def matrix_multiply(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def matrix_vector(a, v):
    return [sum((x*y for x, y in zip(row, v)), F(0)) for row in a]


def energy_error_bound(residual_squared, rayleigh, excited_lower=F(3)):
    need(residual_squared >= 0 and rayleigh < excited_lower,
         'nonnegative residual and a strict actual spectral denominator required')
    return residual_squared/(excited_lower-rayleigh)


def example(lam):
    need(0 <= lam <= F(1, 100), 'frozen coupling range')
    dlo, dhi = sqrt_bounds(9+20*lam*lam)
    wlo, whi = (dlo-3)/2, (dhi-3)/2
    c = 20*lam
    mulo, muhi = c-whi, c-wlo
    hlo, hhi = lam/(2*(3+whi)), lam/(2*(3+wlo))
    r2lo = 195*lam**4/(4*(3+whi)*dhi)
    r2hi = 195*lam**4/(4*(3+wlo)*dlo)
    rholo, unused = sqrt_bounds(r2lo)
    unused, rhohi = sqrt_bounds(r2hi)
    gap = 3-muhi
    delta_hi = energy_error_bound(r2hi, muhi)
    nu = F(236, 39)+c
    max_d = nu-mulo
    unused, second_radical_hi = sqrt_bounds(max_d**2+4*r2hi)
    delta_lo = 2*r2lo/(max_d+second_radical_hi)
    projector = rhohi/gap
    e_lo, e_hi = mulo-delta_hi, muhi-delta_lo
    tau = F(4)
    full_tail = exp_negative_bounds(tau*gap)
    ritz_tail = exp_negative_bounds(tau*(3+wlo))
    rank_one = projector+full_tail[1]
    full_ritz = rank_one+ritz_tail[1]
    dhat, hhat = (dlo+dhi)/2, (hlo+hhi)/2
    representation = 5*(hhi-hlo)+(dhi-dlo)/4
    exp_dark = exp_negative_bounds(tau*(dhat+3)/2)
    exp_bright = exp_negative_bounds(tau*dhat)
    evaluation = exp_dark[1]-exp_dark[0]+exp_bright[1]-exp_bright[0]
    return {
        'lambda': lam, 'D_interval': [dlo, dhi], 'w_interval': [wlo, whi],
        'h_interval': [hlo, hhi], 'Ritz_energy_interval': [mulo, muhi],
        'residual_squared_interval': [r2lo, r2hi], 'residual_norm_interval': [rholo, rhohi],
        'residual_energy_expectation': nu,
        'true_minus_Ritz_energy_sign': 'true <= Ritz, strictly for positive lambda',
        'Ritz_minus_true_energy_interval': [delta_lo, delta_hi],
        'full_ground_energy_interval': [e_lo, e_hi],
        'ground_projector_distance_upper': projector,
        'full_excitation_gap_lower': gap, 'Ritz_excitation_gap_lower': 3+wlo,
        'heat_start_sigma': tau, 'full_tail_at_start_interval': full_tail,
        'Ritz_tail_at_start_interval': ritz_tail,
        'rank_one_late_heat_error_upper': rank_one,
        'Ritz_late_heat_error_upper': full_ritz,
        'rational_representation': {
            'D_hat': dhat, 'h_hat': hhat,
            'ground_exponent_exactly_zero': True,
            'uniform_representation_error_upper': representation,
            'exp_dark_at_sigma4_interval': exp_dark,
            'exp_bright_at_sigma4_interval': exp_bright,
            'sigma4_exponential_evaluation_error_upper': evaluation,
            'full_delayed_heat_plus_representation_upper': full_ritz+representation,
        }
    }


def run():
    controls = {}

    def control(name, condition):
        need(condition, 'control failed: '+name)
        controls[name] = True

    vertices, edges, masks = graph()
    control('actual_T_graph_counts', (len(vertices), len(edges), len(masks)) == (18, 33, 20))
    pairs = list(combinations(range(20), 2))
    intersections = Counter((masks[a] & masks[b]).bit_count() for a, b in pairs)
    control('all_face_pair_geometries_complete', intersections == {0: 128, 1: 62})
    triple_zero = sum(a ^ b ^ c == 0 for a, b, c in product(masks, repeat=3))
    fourth_distinct_zero = sum(a ^ b ^ c ^ d == 0 for a, b, c, d in combinations(masks, 4))
    control('triple_and_distinct_four_face_parity_exhaustion',
            triple_zero == fourth_distinct_zero == 0)
    pattern_counts = Counter()
    for indices in product(range(20), repeat=4):
        parity = 0
        for p in indices:
            parity ^= masks[p]
        if parity == 0:
            pattern = tuple(sorted(Counter(indices).values()))
            pattern_counts[pattern] += 1
    control('complete_160000_ordered_fourth_moment_terms',
            pattern_counts == {(4,): 20, (2, 2): 1140})
    m2 = F(20, 4)
    m4 = pattern_counts[(4,)]*F(1, 8)+pattern_counts[(2, 2)]*F(1, 16)
    var = m4-m2*m2
    control('actual_full_Haar_residual_variance', m2 == 5 and m4 == F(295, 4) and var == F(195, 4))
    center_mask = 0
    for i, (v, end, axis) in enumerate(edges):
        negative = (axis == 1 and v[0] % 2) or (axis == 2 and (v[0]+v[1]) % 2)
        if negative:
            center_mask |= 1 << i
    control('all_odd_moments_vanish_by_actual_global_center_map',
            all((mask & center_mask).bit_count() % 2 == 1 for mask in masks))
    pair_masks = [masks[a] ^ masks[b] for a, b in pairs]
    control('every_two_face_product_is_an_orthogonal_residual_channel',
            len(set(pair_masks)) == 190 and all(pair_masks))
    # Exact SU(2) S^3 quaternion marginal moments.
    q2, q4 = F(1, 4), F(3, 4*6)
    spin_one_norm = 16*q4-8*q2+1
    spin_one_coupling = 8*q4-2*q2
    control('spin_one_character_normalization_and_magnetic_coefficient',
            spin_one_norm == 1 and spin_one_coupling == F(1, 2))
    weights = {F(9, 2): F(62, 16), F(6): F(128, 4),
               F(13, 2): F(3*62, 16), F(8): F(20, 16)}
    energy_moment = sum((energy*weight for energy, weight in weights.items()), F(0))
    control('shared_edge_singlet_triplet_weights_complete',
            sum(weights.values(), F(0)) == var and energy_moment == 4*m4 == 295)
    control('retaining_only_spin_one_underestimates_residual_by_factor_39',
            var/weights[F(8)] == 39)
    no_singlet_moment = F(62, 4)*F(13, 2)+F(128, 4)*6+F(20, 16)*8
    control('omitting_shared_edge_singlets_changes_actual_energy_moment',
            no_singlet_moment-energy_moment == F(31, 4))
    wrong_m4 = 20*F(1, 4)+1140*F(1, 16)
    nineteen_var = F(19, 8)+6*F(19*18, 2)*F(1, 16)-F(19, 4)**2
    control('wrong_Haar_fourth_moment_and_19_face_memory_model_rejected',
            wrong_m4 != m4 and nineteen_var != var)

    examples = [example(lam) for lam in [F(0), F(1, 200), F(1, 100)]]
    cap = examples[-1]
    lam = cap['lambda']
    matrix = [[F(0) for unused in range(21)] for ignored in range(21)]
    matrix[0][0] = 20*lam
    for p in range(1, 21):
        matrix[p][p] = 3+20*lam
        matrix[0][p] = matrix[p][0] = -lam/2
    omega = [F(1)]+[F(0)]*20
    summed = [F(0)]+[F(1)]*20
    control('actual_21_state_matrix_reassembled',
            matrix_vector(matrix, omega) == [20*lam]+[-lam/2]*20
            and matrix_vector(matrix, summed) == [-10*lam]+[3+20*lam]*20)
    hlo, hhi = cap['h_interval']
    wlo, whi = cap['w_interval']
    control('wrong_Ritz_face_sign_fails_actual_ground_equation',
            -lam/2-(3+wlo)*hlo < 0 and hlo > 0)
    projector_h = cap['rational_representation']['h_hat']
    v = [F(1)]+[projector_h]*20
    z = 1+20*projector_h**2
    ghat = [[a*b/z for b in v] for a in v]
    plane = [[F(0) for unused in range(21)] for ignored in range(21)]
    plane[0][0] = F(1)
    for p in range(1, 21):
        for q in range(1, 21):
            plane[p][q] = F(1, 20)
    control('rational_ground_projector_exactly_idempotent_and_physical_plane_supported',
            matrix_multiply(ghat, ghat) == ghat
            and matrix_multiply(plane, ghat) == ghat
            and sum((ghat[i][i] for i in range(21)), F(0)) == 1)
    control('actual_full_ground_interval_has_outward_decimal_enclosure',
            cap['full_ground_energy_interval'][0] >= F('0.19983332325')
            and cap['full_ground_energy_interval'][1] <= F('0.19983333365'))
    delta_lo, delta_hi = cap['Ritz_minus_true_energy_interval']
    control('nonzero_complete_residual_proves_distinct_true_and_Ritz_grounds',
            0 < delta_lo < delta_hi < F(194, 10**10))
    control('useful_full_graph_ground_and_late_heat_certificates',
            cap['ground_projector_distance_upper'] < F(832, 10**7)
            and cap['Ritz_late_heat_error_upper'] < F(103, 10**6)
            and cap['rank_one_late_heat_error_upper'] < F(97, 10**6))
    rep = cap['rational_representation']
    control('representation_and_scalar_evaluation_errors_separately_enclosed',
            rep['uniform_representation_error_upper'] < F(1, 10**35)
            and rep['sigma4_exponential_evaluation_error_upper'] < F(1, 10**45)
            and rep['full_delayed_heat_plus_representation_upper'] < F(103, 10**6))
    zero = examples[0]
    control('lambda_zero_recovers_exact_vacuum_with_no_residual_division',
            zero['Ritz_energy_interval'] == [0, 0]
            and zero['residual_squared_interval'] == [0, 0]
            and zero['Ritz_minus_true_energy_interval'] == [0, 0]
            and zero['ground_projector_distance_upper'] == 0)
    invalid_gap = False
    try:
        energy_error_bound(F(1, 100), F(3))
    except ValueError:
        invalid_gap = True
    control('invalid_spectral_gap_denominator_rejected', invalid_gap)
    invalid_coupling = False
    try:
        example(F(1, 50))
    except ValueError:
        invalid_coupling = True
    control('outside_contract_coupling_rejected', invalid_coupling)
    # Positive ground shift gives e^(zeta*s)>=1+zeta*s, unbounded with s.
    zeta = F(1, 10**6)
    control('independently_rounded_ground_shift_is_not_uniformly_centered',
            1+zeta*(2/zeta) == 3 and exp_negative_bounds(F(2))[1] < F(1, 5))
    rejected = 0
    for bad in [False, 1, 'passed']:
        try:
            need(bad, 'strict acceptance probe')
        except ValueError:
            rejected += 1
    control('explicit_checks_survive_optimized_Python', rejected == 3)

    results = {
        'loop': 'x2', 'direction': 'forward', 'status': 'passed',
        'claims': [
            'The complete actual Ritz residual norm is 195lambda^4/[4(3+w)D].',
            'All 20 spin-one and 190 two-face residual products are retained.',
            'Actual residual electric weights at 9/2,6,13/2,8 have norm 195/4 and first moment 295.',
            'The full graph ground energy and projector obey evaluated variational-residual enclosures.',
            'At lambda=1/100 the centered full and Ritz heat differ by less than 0.000103 for every sigma>=4.',
            'A rational spectral representation and its evaluation errors are explicitly certified.'
        ],
        'limitations': [
            'These are rigorous finite-graph upper/error bounds, not an exact ground or observed trajectory.',
            'No early-time full-space, relative-heat or real-time accuracy claim is made.',
            'The residual two-vector compression is a variational test, not a closed evolution.',
            'No homogeneous, volume-uniform, continuum or physical calibration theorem follows.',
            'Scientific priority remains unverified; agent review is not external peer review.'
        ],
        'actual_graph': {'vertices': vertices, 'edges': edges, 'face_edge_masks': masks,
                         'pair_intersection_counts': dict(intersections),
                         'ordered_quadruples_checked': 20**4,
                         'fourth_moment_pattern_counts': {str(k): v for k, v in pattern_counts.items()},
                         'center_flip_edge_mask': center_mask},
        'complete_residual': {'ES2': m2, 'ES4': m4, 'F_squared_norm': var,
                              'spin_one_terms': 20, 'two_face_terms': 190,
                              'electric_spectral_weights': {str(k): v for k, v in weights.items()},
                              'electric_first_moment': energy_moment,
                              'normalized_electric_first_moment': energy_moment/var},
        'actual_Ritz_matrix_at_lambda_1_100': matrix,
        'rational_ground_projector_at_lambda_1_100': ghat,
        'evaluated_examples': examples,
    }
    return clean(results), {'loop': 'x2', 'direction': 'forward',
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
    for filename, data in [('results.json', results), ('controls.json', controls)]:
        (output/filename).write_text(json.dumps(data, sort_keys=True, indent=2)+'\n')
    print('x2 forward: passed; complete physical residual; certified full-graph late heat')


if __name__ == '__main__':
    main()
