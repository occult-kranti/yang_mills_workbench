#!/usr/bin/env python3
"""Exact AG3 forward controls. No local or third-party imports."""
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from math import factorial
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
NAMES = []
CBAR = Q(288, 31)
BWEIGHT = Q(3, 2)


def check(label, truth):
    if not truth:
        raise RuntimeError('FAILED: ' + label)
    NAMES.append(label)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rationalize(x):
    if isinstance(x, Q):
        return {'numerator': x.numerator, 'denominator': x.denominator}
    if isinstance(x, dict):
        return {str(k): rationalize(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [rationalize(v) for v in x]
    return x


def matrix(rows):
    return [[Q(x) for x in row] for row in rows]


def zeros(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def diag(values):
    return [[Q(values[i]) if i == j else Q(0) for j in range(len(values))]
            for i in range(len(values))]


def lin(*pairs):
    out = zeros(len(pairs[0][1]))
    for coefficient, mat in pairs:
        for i, row in enumerate(mat):
            for j, entry in enumerate(row):
                out[i][j] += coefficient * entry
    return out


def product(left, right):
    n = len(left)
    return [[sum(left[i][k] * right[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]


def bracket(left, right):
    return lin((1, product(left, right)), (-1, product(right, left)))


def adjoint(mat):
    return [list(row) for row in zip(*mat)]


def ad(X, V, n):
    for _ in range(n):
        V = bracket(X, V)
    return V


def powers(X, degree):
    seq = [diag([1]*len(X))]
    for n in range(1, degree+1):
        seq.append(product(seq[-1], X))
    return seq


def exponential_product_coefficients(X, H, B, degree):
    # Direct left/right multiplication, separate from nested-commutator RHS.
    xp = powers(X, degree)
    output = []
    for n in range(degree+1):
        coefficient = zeros(len(X))
        for input_degree, term in ((0, H), (1, B)):
            if n < input_degree:
                continue
            for left_order in range(n-input_degree+1):
                right_order = n-input_degree-left_order
                weight = Q((-1)**right_order,
                           factorial(left_order)*factorial(right_order))
                contribution = product(product(xp[left_order], term), xp[right_order])
                coefficient = lin((1, coefficient), (weight, contribution))
        output.append(coefficient)
    return output


def local_split(K):
    n = len(K)
    scalar = K[0][0]
    mixing = [[K[i][j] if (i == 0) != (j == 0) else Q(0)
               for j in range(n)] for i in range(n)]
    complement = [[K[i][j] - (scalar if i == j else 0)
                   if i and j else Q(0) for j in range(n)] for i in range(n)]
    return scalar, mixing, complement


def inverse_generator(B, energies):
    u = [Q(0)] + [B[i][0]/energies[i] for i in range(1, len(B))]
    X = [[u[i] if j == 0 else (-u[j] if i == 0 else Q(0))
          for j in range(len(B))] for i in range(len(B))]
    return X, u


def tensor_pair(mat, pair):
    out = zeros(8)
    exterior = next(k for k in range(3) if k not in pair)
    bits = [[(i >> (2-j)) & 1 for j in range(3)] for i in range(8)]
    for i in range(8):
        for j in range(8):
            if bits[i][exterior] == bits[j][exterior]:
                u = 2*bits[i][pair[0]]+bits[i][pair[1]]
                v = 2*bits[j][pair[0]]+bits[j][pair[1]]
                out[i][j] = mat[u][v]
    return out


def finite_algebra():
    H0 = diag([0, 2, 5, 9])
    K = matrix([[3, 1, 2, -1], [1, 4, 1, 2], [2, 1, -2, 3], [-1, 2, 3, 1]])
    scalar, B, Z = local_split(K)
    scalar_matrix = diag([scalar]*4)
    Dbase = diag([0, 2, 2, 2])
    D = lin((1, Dbase), (1, Z))
    X, u = inverse_generator(B, [0, 2, 5, 9])
    check('full_K_split', K == lin((1, scalar_matrix), (1, B), (1, Z)))
    check('centered_complement_annihilates_vacuum', all(Z[i][0] == 0 for i in range(4)))
    check('source_is_full_local_mixing', local_split(B)[1] == B)
    check('bare_inverse_commutator', bracket(X, H0) == lin((-1, B)))
    check('bare_generator_skew', adjoint(X) == lin((-1, X)))
    check('reduced_inverse_norm_control', sum(x*x for x in u) <= sum(B[i][0]**2 for i in range(4)))
    check('retained_D_commutator_nonzero', bracket(X, D) != zeros(4))
    check('old_scalar_commutes', bracket(X, scalar_matrix) == zeros(4))
    H = lin((1, H0), (1, D), (1, scalar_matrix))
    for sign in (-1, 0, 1):
        XS, BS = lin((sign, X)), lin((sign, B))
        direct = exponential_product_coefficients(XS, H, BS, 6)
        for n in range(7):
            if n == 0:
                target = H
            else:
                target = lin((Q(1, factorial(n)), ad(XS, D, n)))
                if n >= 2:
                    target = lin((1, target),
                                 (Q(n-1, factorial(n)), ad(XS, BS, n-1)))
            check(f'full_exponential_sign{sign}_degree{n}', direct[n] == target)
        if sign == 0:
            check('zero_source_update_exact', all(term == zeros(4) for term in direct[1:]))
    Rsecond = lin((Q(1, 2), ad(X, D, 2)), (Q(1, 2), bracket(X, B)))
    gamma, newB, newZ = local_split(Rsecond)
    check('new_scalar_nonzero_fixture', gamma != 0)
    check('complete_new_scalar_split', Rsecond == lin((1, diag([gamma]*4)), (1, newB), (1, newZ)))
    check('dropped_new_scalar_rejected', Rsecond != lin((1, newB), (1, newZ)))
    rawQ = [[Rsecond[i][j] if i and j else Q(0) for j in range(4)] for i in range(4)]
    check('uncentered_complement_double_count_rejected', Rsecond != lin((1, diag([gamma]*4)), (1, newB), (1, rawQ)))
    check('wrong_BCH_B_half_coefficient_rejected', Rsecond != lin((Q(1, 2), ad(X, D, 2)), (1, bracket(X, B))))
    check('omitted_retained_D_rejected', ad(X, D, 1) != zeros(4))
    check('old_scalar_drop_rejected', H != lin((1, H0), (1, D)))

    Blocal = matrix([[0, 1, 2, 1], [1, 0, 0, 0], [2, 0, 0, 0], [1, 0, 0, 0]])
    Dlocal = matrix([[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, -1, 1], [0, 0, 1, 2]])
    Xlocal, _ = inverse_generator(Blocal, [0, 1, 1, 2])
    pairs = ((0, 1), (1, 2))
    xs = [tensor_pair(Xlocal, p) for p in pairs]
    bs = [tensor_pair(Blocal, p) for p in pairs]
    ds = [tensor_pair(Dlocal, p) for p in pairs]
    totalX, totalB, totalD = (lin((1, v[0]), (1, v[1])) for v in (xs, bs, ds))
    totalH0 = diag([bin(i).count('1') for i in range(8)])
    check('overlap_full_exterior_identity_commutator', bracket(totalX, totalH0) == lin((-1, totalB)))
    crossD = lin((1, bracket(xs[0], ds[1])), (1, bracket(xs[1], ds[0])))
    check('overlap_cross_retained_D_nonzero', crossD != zeros(8))
    direct = exponential_product_coefficients(totalX, lin((1, totalH0), (1, totalD)), totalB, 4)
    for n in range(1, 5):
        expected = lin((Q(1, factorial(n)), ad(totalX, totalD, n)))
        if n >= 2:
            expected = lin((1, expected), (Q(n-1, factorial(n)), ad(totalX, totalB, n-1)))
        check(f'overlap_full_BCH_degree{n}', direct[n] == expected)
    check('excited_exterior_actual_source_nonzero', any(bs[0][i][1] != 0 for i in range(8)))
    projected = [[bs[0][i][j] if i % 2 == 0 and j % 2 == 0 else Q(0)
                  for j in range(8)] for i in range(8)]
    check('global_vacuum_exterior_substitution_rejected',
          all(projected[i][1] == 0 for i in range(8)) and projected != bs[0])
    return {'local_inverse_u': u, 'new_scalar_second_coefficient': gamma,
            'status': 'Exact finite algebra controls only; no physical SU(2) cutoff or observable.'}


def support_controls():
    U, V, W = set(range(4)), set(range(3, 7)), set(range(6, 10))
    b = BWEIGHT
    union = U | V
    for root in sorted(union):
        left = 2*b**len(union)
        old = (2/b)*b**len(U)*b**len(V) if root in U else Q(0)
        incoming = (2/b)*b**len(U)*b**len(V) if root in V else Q(0)
        check(f'two_root_complete_union_{root}', left <= old+incoming)
        if root == 6:
            check('missing_incoming_root_rejected', left > old)
        if root == 0:
            check('missing_old_root_rejected', left > incoming)
    check('nonempty_overlap_factor_exact_fixture', b**len(union) == b**len(U)*b**len(V)/b)
    check('outer_support_can_miss_seed', not U.intersection(W) and bool(union.intersection(W)))
    check('generated_union_not_reset_to_four', len(union | W) == 10)
    check('repeated_support_retained', len(U | U) == 4 and bool(U.intersection(U)))
    # An operator of norm b^-m on m sites has b-norm1 and weight2 norm(4/3)^m.
    examples = []
    for m in (4, 8, 16):
        amplitude = b**(-m)
        output_two = 2**m * amplitude
        check(f'weight_reset_discriminant_{m}', b**m*amplitude == 1 and output_two > 1)
        examples.append({'support_size': m, 'norm_b': Q(1), 'norm_2': output_two})
    check('no_fixed_weight_contraction_inferred', Q(4, 5)*(Q(4, 3)**16) > 1)
    check('remaining_positive_weight_is_not_new_input_two', BWEIGHT < 2)
    base_star = ((0,0,0),(1,0,0),(0,1,0),(0,0,1))
    for side, expected_anchors in ((1,0),(2,1)):
        sites = set(itertools.product(range(side), repeat=3))
        anchors = [a for a in sites if all(tuple(a[i]+z[i] for i in range(3)) in sites
                                           for z in base_star)]
        check(f'complete_star_boundary_side{side}', len(anchors) == expected_anchors)
        if not anchors:
            family_X = [diag([0,0]) for _ in anchors]
            Xempty = zeros(2)
            for term in family_X:
                Xempty = lin((1,Xempty),(1,term))
            expansion = exponential_product_coefficients(Xempty, diag([0,1]), zeros(2), 3)
            check('no_star_full_zero_update', expansion[0] == diag([0,1])
                  and all(v == zeros(2) for v in expansion[1:]))
    return {'unions': [sorted(U), sorted(union), sorted(union | W)],
            'growing_support_counterexamples': examples}


def endpoint(name, M, kcap):
    dcap = 64*M+2*kcap
    theta = CBAR*kcap
    qcap = CBAR*(dcap+kcap)/(1-theta)
    L = qcap*kcap
    old_scalar = kcap/64
    new_scalar = 4*L/81
    kappa = 4*M+kcap/8+32*L/81
    check(name+'_complete_radius_positive', 0 <= theta < 1)
    check(name+'_complete_new_reference_positive', 1-kappa > 0)
    for numerator in (0, 1, 5, 10):
        actual_r = kcap*Q(numerator, 10)
        actual_q = CBAR*(dcap+actual_r)/(1-CBAR*actual_r)
        rhs = actual_r*actual_q
        check(name+f'_actual_r_factor_{numerator}', rhs <= qcap*actual_r)
        if not actual_r:
            check(name+'_zero_r_no_division', rhs == 0)
    tail_order = 6
    partial = sum(theta**n for n in range(1, tail_order+1))
    tail = theta**(tail_order+1)/(1-theta)
    check(name+'_complete_geometric_tail_exact', partial+tail == theta/(1-theta))
    check(name+'_norm_cost_scalar_support4', Q(1, 4)*BWEIGHT**-4 == Q(4, 81))
    check(name+'_norm_cost_diagonal_support4', 2*BWEIGHT**-4 == Q(32, 81))
    return {'M': M, 'K2_cap': kcap, 'D2_cap': dcap, 'theta_cap': theta,
            'r_ceiling': kcap, 'd_ceiling': dcap, 'theta': theta, 'ratio': qcap,
            'remainder': L, 'scalar_density': old_scalar+new_scalar, 'reference_gap': 1-kappa,
            'actual_r_multiplicative_coefficient': qcap, 'R_b_cap': L,
            'old_scalar_density_cap': old_scalar, 'new_scalar_density_cap': new_scalar,
            'total_scalar_density_cap': old_scalar+new_scalar,
            'new_mixing_b_cap': L, 'new_centered_diagonal_b_cap': 2*L,
            'complete_diagonal_b_cap': dcap+2*L,
            'reference_relative_kappa_cap': kappa, 'reference_gap_lower': 1-kappa,
            'passive_embedding_ratio': Q(81,256),
            'beats_passive_upper_budget': qcap < Q(81,256),
            'actual_lower_weight_input_contraction': False,
            'tail_after_order6_cap': (dcap+kcap)*tail,
            'interpretation': 'All coefficients multiply actual indexed input r; displayed absolute budgets use its upper cap.'}


def source_bindings():
    source = json.loads((BASE/'inputs/source-inventory.json').read_text())
    contract_path = 'research/round28/contracts/ag3.json'
    contract = json.loads((ROOT/contract_path).read_text())
    check('contract_source_coverage', all(source.get(p) == h for p,h in contract['sources'].items()))
    check('current_contract_bound', source.get(contract_path) == digest(ROOT/contract_path))
    for path, expected in source.items():
        check('live:'+path, digest(ROOT/path) == expected)
        check('snapshot:'+path, digest(BASE/'inputs'/path) == expected)
    instructions = json.loads((BASE/'inputs/instruction-inventory.json').read_text())
    for path, record in instructions.items():
        check('instruction:'+path, digest(BASE/'inputs/instructions'/path) == record['sha256'])
    own = {p:digest(BASE/p) for p in ('check.py', 'report.md', 'inputs/source-inventory.json',
                                     'inputs/instruction-inventory.json', 'inputs/preproduction.json')}
    return {'sources':source, 'instructions':instructions, 'producer':own}


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    dest = parser.parse_args().output
    if not dest.is_absolute() or dest.exists():
        raise SystemExit('--output must be a fresh absolute directory')
    sources = source_bindings()
    log_lower = sum(Q((-1)**(j+1), j*3**j) for j in range(1, 5))
    check('alternating_log_lower_exact', log_lower == Q(31, 108))
    check('overlap_constant_exact', Q(8, 3)/log_lower == CBAR)
    # Polynomial identity: (1+t)(1-t+t^2-t^3)=1-t^4.
    poly = [Q(1), Q(-1), Q(1), Q(-1)]
    result = [Q(0)]*5
    for j, coefficient in enumerate(poly):
        result[j] += coefficient
        result[j+1] += coefficient
    check('positive_log_remainder_identity', result == [1,0,0,0,-1])
    main = endpoint('main', Q(1,1000), Q(7,1000))
    narrow = endpoint('narrow', Q(1,10000), Q(7,100000))
    check('main_target_exact_fraction', main['actual_r_multiplicative_coefficient'] == Q(3060,3623))
    check('main_factor_below_17_over_20', main['actual_r_multiplicative_coefficient'] < Q(17,20))
    check('narrow_target_exact_fraction', narrow['actual_r_multiplicative_coefficient'] == Q(5949,96812))
    check('narrow_factor_below_1_over_16', narrow['actual_r_multiplicative_coefficient'] < Q(1,16))
    check('passive_support4_embedding_exact', (BWEIGHT/2)**4 == Q(81,256))
    check('main_weaker_than_passive_budget', main['ratio'] > Q(81,256))
    check('narrow_stronger_than_passive_budget', narrow['ratio'] < Q(81,256))
    check('main_reference_gap_display', main['reference_gap_lower'] > Q(124,125))
    check('narrow_reference_gap_display', narrow['reference_gap_lower'] > Q(1999,2000))
    rtrue, outtrue, rbound, outbound = Q(1,100), Q(1,10), Q(1), Q(1,5)
    check('two_upper_budgets_do_not_prove_contraction', rtrue <= rbound and outtrue <= outbound
          and outbound/rbound < Q(17,20) and outtrue/rtrue > 1)
    algebra = finite_algebra()
    supports = support_controls()
    output = {'schema':'ag3-forward-exact-v1', 'status':'passed', 'checks':NAMES,
              'check_count':len(NAMES), 'coefficient_c_upper':CBAR,
              'input_weight':Q(2), 'output_weight':BWEIGHT,
              'endpoints':{'main':main,'narrow':narrow}, 'algebra':algebra,
              'support_controls':supports, 'bindings':sources,
              'scope':{'full_source_correction':True, 'weight_changing_bound':True,
                       'all_stage_iteration':False, 'full_hamiltonian_gap':False,
                       'full_indexed_mixing_correction':True, 'cross_weight_reduction':True,
                       'same_weight_contraction':False, 'all_stage_convergence':False,
                       'reference_only_gap':True, 'full_homogeneous_gap':False,
                       'continuum_Yang_Mills':False}}
    dest.mkdir(parents=True)
    (dest/'results.json').write_text(json.dumps(rationalize(output),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','checks':len(NAMES),'results_sha256':digest(dest/'results.json')}))


if __name__ == '__main__':
    run()
