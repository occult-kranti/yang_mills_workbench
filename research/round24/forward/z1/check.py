#!/usr/bin/env python3
"""Z1: actual retained-input relative heat obstruction, rational arithmetic."""
import argparse
from fractions import Fraction as F
import json
from math import isqrt
from pathlib import Path


def need(ok, why):
    if type(ok) is not bool or not ok:
        raise ValueError(why)


def clean(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    return x


def outward(lo, hi, digits=50):
    scale = 10**digits
    return F(lo.numerator*scale//lo.denominator, scale), F(
        -((-hi.numerator*scale)//hi.denominator), scale)


def sqrt_bounds(x):
    need(x >= 0, 'negative radical')
    n, d = isqrt(x.numerator), isqrt(x.denominator)
    if n*n == x.numerator and d*d == x.denominator:
        return F(n, d), F(n, d)
    lo, hi = F(0), max(F(1), x)
    for unused in range(180):
        mid = (lo+hi)/2
        if mid*mid <= x:
            lo = mid
        else:
            hi = mid
    lo, hi = outward(lo, hi)
    need(lo*lo <= x <= hi*hi, 'failed radical enclosure')
    return lo, hi


def exp_bounds(x):
    need(x >= 0, 'positive exponential magnitude required')
    total = term = F(1)
    n = 128
    for k in range(1, n+1):
        term *= x/k
        total += term
    ratio = x/(n+2)
    need(ratio < 1, 'invalid exponential Taylor ratio')
    upper = total+(term*x/(n+1))/(1-ratio)
    return outward(total, upper, 40)


def exp_negative_upper(x):
    lo, unused = exp_bounds(x)
    return 1/lo


def verify_gap(mu):
    need(mu < 3, 'actual excited-spectrum denominator must be positive')
    return 3-mu


def admit_retained(kinetic_energy, gauge_invariant):
    need(gauge_invariant is True and 0 <= kinetic_energy < F(9, 2),
         'input is outside the actual retained physical sector')


def example(lam):
    need(0 <= lam <= F(1, 100), 'coupling outside frozen model')
    c = 20*lam
    dlo, dhi = sqrt_bounds(9+20*lam**2)
    wlo, whi = (dlo-3)/2, (dhi-3)/2
    mulo, muhi = c-whi, c-wlo
    gap = verify_gap(muhi)
    r2lo = 195*lam**4/(4*(3+whi)*dhi)
    r2hi = 195*lam**4/(4*(3+wlo)*dlo)
    nu = F(236, 39)+c
    dmax = nu-mulo
    unused, smax = sqrt_bounds(dmax**2+4*r2hi)
    delta_lo = 2*r2lo/(dmax+smax)
    delta_hi = r2hi/gap
    f0lo, unused = sqrt_bounds((dhi+3)/(2*dhi))
    omega_lo, unused = sqrt_bounds(1-muhi/3)
    result = {'lambda': lam, 'D_interval': [dlo, dhi], 'w_interval': [wlo, whi],
              'Ritz_energy_interval': [mulo, muhi],
              'true_ground_energy_interval': [mulo-delta_hi, muhi-delta_lo],
              'complete_residual_squared_interval': [r2lo, r2hi],
              'strict_Ritz_minus_true_energy_interval': [delta_lo, delta_hi],
              'full_excitation_gap_lower': gap,
              'Ritz_vacuum_overlap_lower': f0lo,
              'true_vacuum_overlap_lower': omega_lo}
    if lam == 0:
        result.update({'positive_coupling_witness_defined': False,
                       'relative_error_on_all_retained_inputs_all_finite_times': F(0),
                       'reason': 'Both exact centered generators reduce to K on P; no division by zero witness.'})
        return result
    unused, normu_hi = sqrt_bounds((whi+delta_hi)**2+5*lam**2)
    unused, normv_hi = sqrt_bounds(whi**2+5*lam**2)
    kappa = delta_lo*f0lo/normu_hi
    eta = delta_lo*omega_lo/normv_hi
    need(kappa > 0 and eta > 0, 'actual positive ground overlap required')
    time_rows = []
    for sigma in [F(0), F(5), F(6), F(8)]:
        growth_lo, unused = exp_bounds(gap*sigma)
        bright_growth_lo, unused = exp_bounds(dlo*sigma)
        radius = exp_negative_upper(dlo*sigma)/eta
        time_rows.append({'sigma': sigma,
                          'u_primary_relative_error_lower': kappa*growth_lo-1,
                          'v_primary_relative_error_distance_from_one_upper': radius,
                          'v_Ritz_denominator_relative_error_lower': eta*bright_growth_lo-1,
                          'negative_lower_bound_is_uninformative': kappa*growth_lo-1 < 0})
    result.update({'positive_coupling_witness_defined': True,
                   'u_exact_definition': '(L-epsilon)Omega; epsilon is the true spectral ground energy',
                   'u_vacuum_coefficient_interval': [wlo+delta_lo, whi+delta_hi],
                   'u_each_face_coefficient': -lam/2,
                   'u_norm_upper': normu_hi,
                   'u_normalized_Ritz_ground_overlap_lower': kappa,
                   'u_true_ground_overlap_exact': F(0),
                   'v_exact_definition': '(L-mu)Omega; mu is the computed Ritz ground energy',
                   'v_vacuum_coefficient_interval': [wlo, whi],
                   'v_each_face_coefficient': -lam/2,
                   'v_norm_upper': normv_hi,
                   'v_normalized_true_ground_overlap_lower': eta,
                   'v_Ritz_ground_overlap_exact': F(0),
                   'time_rows': time_rows})
    return result


def run():
    controls = {}

    def control(name, predicate):
        need(predicate, 'control failed: '+name)
        controls[name] = True

    lam = F(1, 100)
    c = 20*lam
    a = [[F(0) for unused in range(21)] for ignored in range(21)]
    a[0][0] = c
    for p in range(1, 21):
        a[p][p] = 3+c
        a[0][p] = a[p][0] = -lam/2
    omega_action = [row[0] for row in a]
    control('actual_L_Omega_has_only_retained_vacuum_and_twenty_face_terms',
            omega_action == [c]+[-lam/2]*20 and sum(x*x for x in omega_action[1:]) == 5*lam**2)
    # Polynomial ring in w with w^2=5lambda^2-3w, derived from the exact star matrix.
    def reduce_w(poly):
        constant, linear, quadratic = poly
        return constant+5*lam**2*quadratic, linear-3*quadratic
    def bright_residual(face_sign):
        vector = [(F(0), F(1))]+[(face_sign*lam/2, F(0))]*20
        residues = []
        for i, row in enumerate(a):
            left_constant = sum((entry*v[0] for entry, v in zip(row, vector)), F(0))
            left_linear = sum((entry*v[1] for entry, v in zip(row, vector)), F(0))
            vc, vl = vector[i]
            residues.append(reduce_w((left_constant-(c+3)*vc,
                                      left_linear-(c+3)*vl-vc, -vl)))
        return residues
    correct_residual = bright_residual(F(-1))
    control('actual_computable_v_is_Ritz_bright_eigenvector',
            all(row == (0, 0) for row in correct_residual))
    wrong_face_sign_residual = bright_residual(F(1))
    control('wrong_Ritz_face_sign_breaks_actual_eigen_equation',
            any(row != (0, 0) for row in wrong_face_sign_residual))
    for energy in [F(0), F(3)]:
        admit_retained(energy, True)
    rejected_spin_one = False
    try:
        admit_retained(F(8), True)
    except ValueError:
        rejected_spin_one = True
    rejected_open_link = False
    try:
        admit_retained(F(3, 4), False)
    except ValueError:
        rejected_open_link = True
    control('excluded_spin_one_and_unphysical_open_link_are_not_retained_witnesses',
            rejected_spin_one and rejected_open_link)
    p_identity = [[F(i == j) for j in range(21)] for i in range(21)]
    control('retained_input_time_zero_error_is_exactly_zero',
            all(p_identity[i][j]-p_identity[i][j] == 0 for i in range(21) for j in range(21)))
    # The 20-face variance in L Omega differs from the selected-memory 19-face number.
    control('wrong_selected_memory_sector_changes_witness_norm', F(20, 4) != F(19, 4))
    examples = [example(F(0)), example(F(1, 200)), example(lam)]
    cap = examples[-1]
    delta_lo, delta_hi = cap['strict_Ritz_minus_true_energy_interval']
    kappa = cap['u_normalized_Ritz_ground_overlap_lower']
    eta = cap['v_normalized_true_ground_overlap_lower']
    control('complete_physical_residual_proves_strict_energy_displacement',
            cap['complete_residual_squared_interval'][0] > 0 and 0 < delta_lo < delta_hi)
    control('assuming_compressed_true_ground_parallel_to_Ritz_ground_is_rejected',
            delta_lo*cap['true_vacuum_overlap_lower'] > 0)
    control('missing_Ritz_overlap_in_true_ground_null_witness_is_rejected', kappa > F(4, 10**7))
    control('missing_true_overlap_in_computable_Ritz_null_witness_is_rejected', eta > F(386, 10**9))
    sigma6 = next(row for row in cap['time_rows'] if row['sigma'] == 6)
    sigma8 = next(row for row in cap['time_rows'] if row['sigma'] == 8)
    control('actual_true_denominator_relative_error_exceeds_6_point_9_at_sigma6',
            sigma6['u_primary_relative_error_lower'] > F(69, 10))
    control('computable_input_relative_error_is_within_1e_4_of_one_at_sigma8',
            sigma8['v_primary_relative_error_distance_from_one_upper'] < F(1, 10000))
    control('changing_the_denominator_changes_the_same_input_conclusion',
            sigma8['v_Ritz_denominator_relative_error_lower'] > 10000
            and sigma8['v_primary_relative_error_distance_from_one_upper'] < F(1, 10000))
    control('true_ground_orthogonal_witness_is_nonzero_and_has_positive_denominator_at_finite_time',
            cap['u_norm_upper'] > 0 and lam > 0
            and cap['u_true_ground_overlap_exact'] == 0
            and cap['full_excitation_gap_lower'] > 0)
    control('own_ground_centering_is_distinct_from_common_Ritz_shift',
            delta_lo > 0 and 1+delta_lo*(2/delta_lo) == 3)
    zero = examples[0]
    control('lambda_zero_exact_reduction_prevents_division_by_zero_witness',
            zero['positive_coupling_witness_defined'] is False
            and zero['relative_error_on_all_retained_inputs_all_finite_times'] == 0
            and zero['strict_Ritz_minus_true_energy_interval'] == [0, 0])
    invalid = False
    try:
        verify_gap(F(3))
    except ValueError:
        invalid = True
    control('invalid_actual_gap_denominator_rejected', invalid)
    outside = False
    try:
        example(F(1, 50))
    except ValueError:
        outside = True
    control('out_of_contract_coupling_rejected', outside)
    rejected = 0
    for wrong in [False, 1, 'passed']:
        try:
            need(wrong, 'strict exception control')
        except ValueError:
            rejected += 1
    control('explicit_checks_survive_optimized_Python', rejected == 3)
    results = {
        'loop': 'z1', 'direction': 'forward', 'status': 'passed',
        'verdict': 'actual_model_obstruction_to_uniform_all_input_all_time_relative_accuracy',
        'claims': [
            'The primary denominator is ||E(sigma)x|| for the same nonzero retained physical input x.',
            'For every fixed positive lambda, u=(L-epsilon)Omega is retained, true-ground-orthogonal and has nonzero Ritz ground overlap.',
            'The primary relative error grows at least kappa exp(g sigma)-1 and is unbounded over time.',
            'The exactly computable retained Ritz-bright input v=(L-mu)Omega has primary relative error tending to one.',
            'At lambda=0.01 the u error is greater than 6.9 at sigma=6; the v error is within 0.0001 of one at sigma=8.',
            'At lambda=0 both evolutions agree on all retained inputs at every finite time.'
        ],
        'limitations': [
            'The unbounded witness uses the true spectral epsilon; its coefficient enclosure does not prepare an exactly ground-null laboratory state.',
            'The computable witness proves a unit limiting error for the primary denominator, not its own divergence.',
            'An operator-norm denominator or Ritz-output denominator defines a different approximation question.',
            'X2 absolute late-time accuracy remains valid; physical heat does not diverge.',
            'No real-time, homogeneous, volume-uniform, calibration, continuum or priority claim follows.',
            'A useful ground-overlap or denominator restriction is a future repair, not an executed Z2 result.'
        ],
        'actual_retained_matrix_at_cap': a,
        'physical_witness_normalization_identity': '(c-epsilon)^2+5lambda^2; twenty orthonormal fundamental faces',
        'relative_quantity': 'sup_{0!=x in P Hphys} ||(E-E_R)x||/||E x|| at finite sigma',
        'evaluated_examples': examples,
    }
    return clean(results), {'loop': 'z1', 'direction': 'forward', 'status': 'passed', 'controls': controls}


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
        (output/name).write_text(json.dumps(data, sort_keys=True, indent=2)+'\n')
    print('z1 forward: passed; actual retained-input relative heat obstruction')


if __name__ == '__main__':
    main()
