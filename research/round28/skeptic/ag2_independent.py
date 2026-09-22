#!/usr/bin/env python3
"""Independent exact AG2 controls. Finite matrices are algebra diagnostics only."""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import argparse
import json

CHECKS = []


def require(name, condition):
    if not condition:
        raise RuntimeError(name)
    CHECKS.append(name)


def zero(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def ident(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def mul(a, b):
    n = len(a)
    return [[sum((a[i][k] * b[k][j] for k in range(n)), Q(0))
             for j in range(n)] for i in range(n)]


def comm(a, b):
    return add(mul(a, b), scale(-1, mul(b, a)))


def power(a, n):
    result = ident(len(a))
    for _ in range(n):
        result = mul(result, a)
    return result


def ad(a, b, n):
    for _ in range(n):
        b = comm(a, b)
    return b


def matrix_sum(terms, n):
    result = zero(n)
    for a in terms:
        result = add(result, a)
    return result


def split(k):
    n = len(k)
    p = zero(n)
    p[0][0] = 1
    q = add(ident(n), scale(-1, p))
    c = k[0][0]
    a = add(mul(mul(p, k), q), mul(mul(q, k), p))
    d = mul(mul(q, add(k, scale(-c, ident(n)))), q)
    return c, a, d, p, q


def local_fixture(sign):
    h = [[Q(0), Q(0), Q(0)], [Q(0), Q(1), Q(0)],
         [Q(0), Q(0), Q(2)]]
    phi = scale(sign, [[Q(0), Q(1, 2), Q(1, 3)],
                       [Q(1, 2), Q(1, 5), Q(1, 7)],
                       [Q(1, 3), Q(1, 7), Q(-1, 4)]])
    a1 = zero(3)
    x = zero(3)
    for i in (1, 2):
        a1[0][i] = a1[i][0] = phi[i][0]
        x[i][0] = phi[i][0] / h[i][i]
        x[0][i] = -x[i][0]
    require(f'commutator_sign_{sign}', comm(x, h) == scale(-1, a1))
    direct = []
    for degree in range(5):
        terms = []
        for k in range(degree + 1):
            l = degree - k
            terms.append(scale(Q((-1) ** l, factorial(k) * factorial(l)),
                               mul(mul(power(x, k), h), power(x, l))))
        if degree:
            for k in range(degree):
                l = degree - 1 - k
                terms.append(scale(Q((-1) ** l, factorial(k) * factorial(l)),
                                   mul(mul(power(x, k), phi), power(x, l))))
        direct.append(matrix_sum(terms, 3))
    require(f'first_order_diagonal_{sign}', direct[1] == add(phi, scale(-1, a1)))
    for n in range(1, 4):
        expected = add(scale(Q(1, factorial(n)), ad(x, phi, n)),
                       scale(Q(-1, factorial(n + 1)), ad(x, a1, n)))
        require(f'O1_full_degree_{n+1}_{sign}', direct[n + 1] == expected)
    r2 = direct[2]
    cubic = direct[3]
    c, a3, d, p, q = split(cubic)
    compressed = add(mul(mul(p, cubic), p), mul(mul(q, cubic), q))
    require(f'same_anchor_compression_{sign}', add(cubic, scale(-1, a3)) == compressed)
    require(f'scalar_source_diagonal_{sign}', cubic == add(scale(c, ident(3)), add(a3, d)))
    require(f'wrong_scalar_double_count_{sign}', cubic != add(scale(c, ident(3)), add(a3, mul(mul(q, cubic), q))))
    require(f'wrong_n1_coefficient_{sign}', r2 != add(comm(x, phi), scale(Q(-1, 3), comm(x, a1))))
    require(f'wrong_n2_coefficient_{sign}', cubic != add(scale(Q(1, 2), ad(x, phi, 2)), scale(Q(-1, 3), ad(x, a1, 2))))
    require(f'nonzero_quadratic_vacuum_{sign}', r2[0][0] < 0)
    require(f'unsupported_quartic_E_{sign}', add(r2, scale(0, a3))[0][0] != 0)
    # Independent rank-two cubic source formula, not just a reconstruction.
    u = [x[i][0] for i in range(3)]
    v = [phi[i][0] for i in range(3)]
    uv = sum((u[i] * v[i] for i in range(3)), Q(0))
    uu = sum((t*t for t in u), Q(0))
    for i in (1, 2):
        require(f'actual_source_formula_{sign}_{i}', a3[i][0] == -uv*u[i]-uu*v[i]/3)
    # Full later transport must retain the nonzero E even at zero generator.
    e0 = add(r2, compressed)
    require(f'zero_generator_retains_E_{sign}', e0 != zero(3))
    # A separate formal transport parameter checks all coefficients through two.
    k = add(a3, e0)
    for n in range(3):
        lhs = matrix_sum([scale(Q((-1)**l, factorial(n-l)*factorial(l)),
                                mul(mul(power(x, n-l), k), power(x, l)))
                          for l in range(n+1)], 3)
        rhs = add(scale(Q(1, factorial(n)), ad(x, a3, n)),
                  scale(Q(1, factorial(n)), ad(x, e0, n)))
        require(f'full_E_transport_degree_{n}_{sign}', lhs == rhs)
    return {'quadratic_vacuum': r2[0][0], 'cubic_scalar': c}


def embed_two(matrix, sites):
    out = zero(8)
    a, b = sites
    external = ({0, 1, 2} - set(sites)).pop()
    for i in range(8):
        for j in range(8):
            if ((i >> external) & 1) == ((j >> external) & 1):
                ii = ((i >> a) & 1) + 2*((i >> b) & 1)
                jj = ((j >> a) & 1) + 2*((j >> b) & 1)
                out[i][j] = matrix[ii][jj]
    return out


def cross_fixture():
    def pair(gap, amplitude):
        ph = zero(4)
        ph[0][3] = ph[3][0] = amplitude
        ph[1][1] = Q(1, 5)
        ph[2][2] = Q(-1, 7)
        xx = zero(4)
        xx[3][0] = amplitude/gap
        xx[0][3] = -amplitude/gap
        aa = zero(4)
        aa[0][3] = aa[3][0] = amplitude
        return ph, xx, aa
    left = tuple(embed_two(a, (0, 1)) for a in pair(Q(3), Q(1, 2)))
    right = tuple(embed_two(a, (1, 2)) for a in pair(Q(5), Q(1, 3)))
    p = add(left[0], right[0]); x = add(left[1], right[1]); a = add(left[2], right[2])
    full = add(comm(x, p), scale(Q(-1, 2), comm(x, a)))
    individual = matrix_sum([add(comm(t[1], t[0]), scale(Q(-1, 2), comm(t[1], t[2])))
                             for t in (left, right)], 8)
    require('cross_words_cannot_be_deleted', full != individual)
    cubic = add(scale(Q(1, 2), ad(x, p, 2)), scale(Q(-1, 6), ad(x, a, 2)))
    same = matrix_sum([add(scale(Q(1, 2), ad(t[1], t[0], 2)), scale(Q(-1, 6), ad(t[1], t[2], 2)))
                       for t in (left, right)], 8)
    require('other_cubic_words_cannot_be_deleted', cubic != same)


STAR = {(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)}


def plus(a, b):
    return tuple(x+y for x, y in zip(a, b))


def star(a):
    return {plus(a, b) for b in STAR}


def touching(support):
    return {tuple(x-y for x, y in zip(p, s)) for p in support for s in STAR}


def geometry():
    root = (0, 0, 0)
    neighbors = touching(STAR)
    require('thirteen_star_intersections', len(neighbors) == 13)
    require('twelve_seven_site_crossings', all(len(STAR | star(a)) == 7 for a in neighbors if a != root))
    words = [((), STAR)]
    counts = []
    for n in range(1, 4):
        words = [(anchors+(b,), support | star(b)) for anchors, support in words for b in touching(support)]
        counts.append(len(words))
        require(f'ordered_word_count_{n}', len(words) <= 13**n*factorial(n))
        require(f'complete_union_bound_{n}', all(len(support) <= 4+3*n for _, support in words))
        require(f'all_repeated_word_retained_{n}', any(anchors == (root,)*n for anchors, _ in words))
        if n == 2:
            other = [a for a, _ in words if a != (root, root)]
            require('n2_non_same_at_most_337', len(other) <= 337)
            require('outer_may_miss_seed', any(not (STAR & star(a[-1])) for a, _ in words))
    boundaries = []
    for sides in [(1,1,1), (2,2,2), (3,3,3), (5,5,5)]:
        sites = {(i,j,k) for i in range(sides[0]) for j in range(sides[1]) for k in range(sides[2])}
        retained = [b for b in sites if star(b) <= sites]
        multiplicity = max([sum(x in star(b) for b in retained) for x in sites], default=0)
        require(f'boundary_multiplicity_{sides}', multiplicity <= 4)
        boundaries.append({'sides':sides, 'retained':len(retained), 'max_multiplicity':multiplicity})
    require('empty_boundary', boundaries[0]['retained'] == 0)
    require('one_retained_star', boundaries[1]['retained'] == 1)
    require('interior_overlap_four', boundaries[-1]['max_multiplicity'] == 4)
    return {'relative_word_counts':counts, 'boundaries':boundaries}


def budget(m):
    rho = Q(9, 4)
    s = Q(4, 35)*m
    z = 26*s*rho**3
    r = m**3/567
    e2 = rho**4 * 7*z*(m+s/2)
    e3_other = 6740*rho**10*s*s*(m+s/3)
    e3_same = 8*rho**4*s*s*(m+s/3)
    e4 = rho**4*(m+s/4)*z**3*(13-10*z)/(1-z)**2
    e = e2+e3_other+e3_same+e4
    loose = rho**4*(m+s/2)*z*(7-4*z)/(1-z)**2 + 4*rho**4*r
    f_rho = (1-72*rho**3*m)**(-3)
    f2 = (1-576*m)**(-3)
    theta = 72*rho**4*r*f_rho
    transported = e/(1-theta)
    residual = 64*r*f2
    nonlinear = theta/(1-theta)*4*rho**4*r*(1+f_rho/2)
    k = residual+nonlinear+transported
    return {'M':m, 's_upper':s, 'z':z, 'r3_upper':r,
            'E2':e2, 'E3_other':e3_other, 'E3_same_compressed':e3_same,
            'E4plus':e4, 'E_rho_direct':e, 'E_rho_loose':loose,
            'theta':theta, 'E_transported':transported,
            'selected_residual':residual, 'selected_nonlinear':nonlinear,
            'full_output_K2':k, 'scalar_root_density':k/16,
            'mixing_norm2':k, 'diagonal_norm2':2*k,
            'reference_relative_extra':k/8,
            'reference_gap_lower':1-4*m-k/8,
            'whole_E_budget_is_actual_norm':False,
            'full_mixing_contraction_certified':False}


def scalar_checks():
    rows = []
    require('rational_sigma_majorant', Q(7,12) < Q(16,25))
    require('r3_majorant_squared', Q(16,9)*Q(1,84)**3 <= Q(1,567)**2)
    for m in [Q(0), Q(1,10000), Q(1,1000)]:
        row = budget(m)
        label = str(m)
        require('original_series_'+label, row['z'] < 1)
        require('AG1_series_'+label, 72*Q(9,4)**3*m < 1)
        require('transport_series_'+label, row['theta'] < 1)
        require('direct_beats_loose_'+label, row['E_rho_direct'] <= row['E_rho_loose'])
        require('positive_reference_gap_'+label, row['reference_gap_lower'] > Q(99,100))
        if m:
            require('quadratic_inventory_dominates_cubic_budget_'+label, row['E2'] > 64*row['r3_upper'])
            # Comparing these two upper budgets intentionally yields no physical contraction verdict.
            require('budget_ratio_not_denominator_'+label, not row['full_mixing_contraction_certified'])
        else:
            require('zero_all_terms', row['full_output_K2'] == 0)
        rows.append(row)
    for z in [Q(0), Q(1,4), Q(1,2), Q(3,4)]:
        partial = sum((Q(4+3*n)*z**n for n in range(3,31)), Q(0))
        total = z**3*(13-10*z)/(1-z)**2
        tail = z**31*(97-94*z)/(1-z)**2
        require('exact_positive_tail_'+str(z), partial+tail == total)
    # Bounded exterior identity cannot regularize an arbitrary domain defect:
    # psi_n=1/n, H_ext psi has n-th entry1 and divergent squared norm.
    for n in (1,4,16,64):
        normsq = sum((Q(1,k*k) for k in range(1,n+1)), Q(0))
        require('exterior_norm_bounded_'+str(n), normsq < 2)
        require('exterior_graph_norm_unbounded_'+str(n), Q(n)/normsq >= Q(n,2))
    # f_epsilon(t)=epsilon*sin(t/epsilon^2) has uniform value bound epsilon,
    # while its exact derivative at zero is 1/epsilon.
    for epsilon in (Q(1,10), Q(1,100), Q(1,1000)):
        require('value_bound_does_not_bound_derivative_'+str(epsilon), 1/epsilon > epsilon)
    return rows


def encoded(x):
    if isinstance(x, Q):
        return {'exact':str(x), 'decimal':format(float(x), '.17g')}
    if isinstance(x, dict):
        return {k:encoded(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)):
        return [encoded(v) for v in x]
    return x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('ag2-independent.json'))
    args = parser.parse_args()
    local = {str(s):local_fixture(s) for s in (1,-1)}
    require('quadratic_even', local['1']['quadratic_vacuum'] == local['-1']['quadratic_vacuum'])
    require('cubic_odd', local['1']['cubic_scalar'] == -local['-1']['cubic_scalar'])
    cross_fixture()
    geo = geometry()
    rows = scalar_checks()
    payload = {'schema':'ym28-ag2-independent-v1', 'checks':len(CHECKS),
               'check_names':CHECKS, 'local_algebra_diagnostics':local,
               'geometry':geo, 'bounds':rows,
               'scope':'Exact rational sufficient budgets and independent algebra/support controls. Finite matrices are not the actual SU(2) model. No full mixing contraction or original physical gap certified.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(encoded(payload),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(CHECKS),'status':'passed'},sort_keys=True))


if __name__ == '__main__':
    main()
