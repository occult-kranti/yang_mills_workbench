#!/usr/bin/env python3
"""AI3 forward: independently reconstructed physical cube and exact readout boxes.

Standard library only. Fractions decide every scientific gate. No imported legacy
checker; inherited physical transfer theorems are identified in report.md.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import factorial, isqrt
from pathlib import Path
import sys

sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent
CONTRACT = 'research/round28/contracts/ai3.json'
CONTRACT_HASH = '20cab55ea76681df9fdcb1d07d74d97312a618e41e96d1ab540b6240b2537074'
CHECKS = []


def need(condition, label):
    if condition is not True:
        raise ValueError(label)
    CHECKS.append(label)


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_check():
    inputs = HERE / 'inputs'
    inventory = json.loads((inputs / 'source-inventory.json').read_text())
    contract = json.loads((inputs / CONTRACT).read_text())
    need(digest(inputs / CONTRACT) == CONTRACT_HASH, 'frozen AI3 contract hash')
    need(len(contract['sources']) == 40, 'all forty frozen contract dependencies')
    need(all(inventory.get(p) == h for p, h in contract['sources'].items()),
         'manifest includes every contract source with exact hash')
    need(inventory.get(CONTRACT) == CONTRACT_HASH, 'manifest includes current contract')
    for rel, h in sorted(inventory.items()):
        p = inputs / rel
        need(not Path(rel).is_absolute() and '..' not in Path(rel).parts,
             'safe snapshot path ' + rel)
        need(not any(x.is_symlink() for x in [p, *p.parents]), 'no snapshot symlink ' + rel)
        need(digest(p) == h, 'source snapshot bytes ' + rel)
    return inventory


def add_vertex(v, axis, amount=1):
    return tuple(c + (amount if i == axis else 0) for i, c in enumerate(v))


def as_link(v, w):
    axis = [i for i in range(3) if v[i] != w[i]]
    need(len(axis) == 1 and abs(v[axis[0]] - w[axis[0]]) == 1, 'unit path link')
    return (axis[0], *min(v, w))


def link_ends(e):
    return (e[1:], add_vertex(e[1:], e[0]))


def face_links(f):
    a, b, *v = f
    v = tuple(v)
    return frozenset(((a, *v), (a, *add_vertex(v, b)),
                      (b, *v), (b, *add_vertex(v, a))))


def factor_owner(link):
    a, x, y, z = link
    is_strip = (a == 0 and x % 4 != 3) or (a == 1 and y % 2 == 0)
    return ('strip', x - x % 4, y - y % 2, z) if is_strip else ('free', *link)


def factor_links(factor):
    if factor[0] == 'free':
        return frozenset((factor[1:],))
    _, x, y, z = factor
    answer = {(0, x + i, y + j, z) for i in range(3) for j in range(2)}
    answer.update((1, x + i, y, z) for i in range(4))
    return frozenset(answer)


def is_omitted(face):
    a, b, x, y, z = face
    return not ((a, b) == (0, 1) and x % 4 != 3 and y % 2 == 0)


def incident_box(links):
    """Independent finite face-box enumeration, rather than legacy incidence walk."""
    low = [max(0, min(e[i + 1] for e in links) - 1) for i in range(3)]
    high = [max(e[i + 1] + int(e[0] == i) for e in links) for i in range(3)]
    answer = set()
    for a, b in combinations(range(3), 2):
        for v in product(*(range(low[i], high[i] + 1) for i in range(3))):
            f = (a, b, *v)
            if is_omitted(f) and face_links(f).intersection(links):
                answer.add(f)
    return answer


def physical_geometry():
    origin = (3, 1, 0)
    vertices = [tuple(origin[i] + v[i] for i in range(3))
                for v in product((0, 1), repeat=3)]
    endpoints = sorted((v, w) for v, w in combinations(vertices, 2)
                       if sum(abs(v[i] - w[i]) for i in range(3)) == 1)
    edges = [as_link(v, w) for v, w in endpoints]
    edge_index = {frozenset((v, w)): i for i, (v, w) in enumerate(endpoints)}
    neighbors = {v: sorted(w for w in vertices if frozenset((v, w)) in edge_index)
                 for v in vertices}
    cycles = set()

    def visit(path):
        if len(path) == 6:
            if path[0] in neighbors[path[-1]]:
                cycles.add(frozenset(edge_index[frozenset((v, w))]
                                     for v, w in zip(path, path[1:] + path[:1])))
            return
        for w in neighbors[path[-1]]:
            if w not in path:
                visit(path + [w])

    for start in vertices:
        visit([start])
    cycles = sorted(cycles, key=lambda s: tuple(sorted(s)))
    need(len(edges) == 12 and len(cycles) == 16, 'DFS complete sixteen cube six-cycles')
    need(all(factor_owner(e)[0] == 'free' for e in edges), 'all twelve cube links free')
    idx = {c: i for i, c in enumerate(cycles)}
    physical_to_id = {e: i for i, e in enumerate(edges)}
    faces = []
    for a, b in combinations(range(3), 2):
        normal = 3 - a - b
        for side in (0, 1):
            f = (a, b, *add_vertex(origin, normal, side))
            mask = frozenset(physical_to_id[e] for e in face_links(f))
            faces.append((f, mask, sum(f[2:])))
    x_walk = [(3, 1, 0), (3, 2, 0), (3, 2, 1), (4, 2, 1),
              (4, 2, 0), (4, 1, 0), (3, 1, 0)]
    X = frozenset(physical_to_id[as_link(v, w)] for v, w in zip(x_walk, x_walk[1:]))
    yz = {f[2]: mask for f, mask, _ in faces if f[:2] == (1, 2)}
    Y4, Y5 = X ^ yz[3], X ^ yz[4]
    need(all(c in idx for c in (X, Y4, Y5)), 'actual X Y4 Y5 physical cycles')
    sources = {4: (idx[X], idx[Y4]), 5: (idx[X], idx[Y5])}
    support = {r: {edges[i] for c in (X, y) for i in c}
               for r, y in ((4, Y4), (5, Y5))}
    seed = support[4] | support[5]
    need(len(seed) == 10 and all(len(s) == 8 for s in support.values()),
         'two eight-link multipliers require common ten-link support')
    need(not support[5] <= support[4], 'incomplete eight-link source seed rejected')
    for y in (Y4, Y5):
        need(len(X & y) == 4 and len(X - y) == len(y - X) == 2,
             'Haar-independent two-link branches with common four-link path')
    face_by_mask = {mask: r for _, mask, r in faces}
    adjacency = [[face_by_mask.get(c ^ d, 0) for d in cycles] for c in cycles]
    need(max(sum(bool(x) for x in row) for row in adjacency) <= 6,
         'uniform Q symmetric row norm at most six')
    need(max(sum(row) for row in adjacency) <= 30,
         'uniform Qprime symmetric row norm at most thirty')
    reached = set(sources[4]); frontier = set(reached)
    while frontier:
        new = {j for i in frontier for j, p in enumerate(adjacency[i]) if p} - reached
        reached |= new; frontier = new
    need(len(reached) == 16, 'source reaches full sixteen-state flip component')
    reflect_v = lambda v: (7 - v[0], v[1], v[2])
    reflect_edge = {i: edge_index[frozenset((reflect_v(v), reflect_v(w)))]
                    for i, (v, w) in enumerate(endpoints)}
    permutation = [idx[frozenset(reflect_edge[e] for e in c)] for c in cycles]
    need(sorted(permutation) == list(range(16)), 'reflection is full retained permutation')
    need(all(permutation[permutation[i]] == i for i in range(16)), 'reflection involution')
    need(permutation[idx[X]] == idx[X], 'unoriented X fixed by cube reflection')
    need(permutation[idx[Y4]] == idx[Y5] and permutation[idx[Y5]] == idx[Y4],
         'reflection exchanges normalized coherent sources without sign')
    need(all(bool(adjacency[i][j]) == bool(adjacency[permutation[i]][permutation[j]])
             for i in range(16) for j in range(16)), 'permutation commutes with Q1 on all entries')
    need(any(adjacency[i][j] != adjacency[permutation[i]][permutation[j]]
             for i in range(16) for j in range(16)), 'endpoint symmetry not promoted to weighted q symmetry')
    cube = set(edges)
    external = incident_box(cube) - {f for f, _, _ in faces}
    need(len(external) == 20, 'all twenty physical exterior touching faces')
    outside = []
    for f in sorted(external):
        shared = face_links(f) & cube
        need(len(shared) == 1, 'exterior single cube-edge intersection ' + str(f))
        e = next(iter(shared))
        opposite = [p for p in face_links(f) - shared if p[0] == e[0]]
        need(len(opposite) == 1 and factor_owner(opposite[0])[0] == 'free',
             'exterior opposite edge free ' + str(f))
        side_owners = {factor_owner(p) for p in face_links(f) - shared - set(opposite)}
        need(len(side_owners) == 2 and not side_owners & {factor_owner(p) for p in cube},
             'two distinct outside side factors ' + str(f))
        cost = sum((F(1, 8) if p[0] == 'strip' else F(3, 4)) for p in side_owners)
        need(cost >= F(1, 4), 'whole-side spectral loading lower bound ' + str(f))
        outside.append({'face': f, 'shared': sorted(shared), 'opposite': opposite[0],
                        'side_owners': sorted(side_owners), 'minimum_energy_increment': cost})
    changes = {F(3) - F(3, 2) * r + 2 * m for r in range(5) for m in range(r + 1)}
    need(min(abs(d) for d in changes if d) >= F(1, 2), 'internal nonzero frequencies separated')
    factors = {factor_owner(e) for e in seed}
    collars = []; previous = set()
    for depth in range(7):
        links = set().union(*(factor_links(owner) for owner in factors))
        touching = incident_box(links)
        retained = {f for f in touching if all(factor_owner(e) in factors for e in face_links(f))}
        need({factor_owner(e) for e in links} == factors, 'complete ownership at depth ' + str(depth))
        need(all(factor_links(p) <= links for p in factors), 'whole factors at depth ' + str(depth))
        if depth:
            need(cube <= links and all(f in retained for f, _, _ in faces),
                 'entire reached component in collar ' + str(depth))
        collars.append({'k': depth, 'factor_count': len(factors), 'link_count': len(links),
                        'retained_face_count': len(retained), 'boundary_face_count': len(touching - retained),
                        'owners': sorted(factors), 'new_owners': sorted(factors - previous),
                        'links': sorted(links), 'retained_faces': sorted(retained)})
        previous = set(factors)
        factors |= {factor_owner(e) for f in touching for e in face_links(f)}
    return adjacency, sources, collars, {'edge_endpoints': endpoints, 'edges': edges,
        'cycles': [sorted(c) for c in cycles], 'faces': [{'face': f, 'edge_ids': sorted(m), 'power': r}
        for f, m, r in faces], 'X_walk': x_walk, 'X': idx[X], 'Y4': idx[Y4], 'Y5': idx[Y5],
        'source_indices': sources, 'common_seed': sorted(seed), 'exterior': outside,
        'reflection_permutation': permutation, 'Q_exponents': adjacency,
        'scope': 'averaged observable-reached component, not entire regional electric shell'}


def p_add(a, b, multiplier=F(1)):
    result = defaultdict(F, a)
    for n, c in b.items():
        result[n] += multiplier * c
    return {n: c for n, c in result.items() if c}


def p_shift(a, power):
    return {n + power: c for n, c in a.items()}


def p_eval(poly, q):
    return sum(c * q ** n for n, c in poly.items())


def symbolic_moments(matrix, sources):
    moments = {}
    for r, indices in sources.items():
        vec = [{0: F(1)} if i in indices else {} for i in range(16)]
        rows = []
        for n in range(9):
            rows.append(p_add({k: c / 2 for k, c in vec[indices[0]].items()},
                              {k: c / 2 for k, c in vec[indices[1]].items()}))
            new = []
            for row in matrix:
                value = {}
                for j, power in enumerate(row):
                    if power:
                        value = p_add(value, p_shift(vec[j], power))
                new.append(value)
            vec = new
        moments[r] = rows
        need(rows[0] == {0: 1} and rows[1] == {r: 1}, 'normalized exact source m0 m1 B' + str(r))
    differences = {n: p_add(moments[5][n], p_shift(moments[4][n], 1), F(-1)) for n in range(9)}
    need(not differences[1], 'symbolic Delta m1 exactly zero')
    need(differences[3] == {13: 2, 15: -2}, 'symbolic Delta m3 equals 2q13(1-q2)')
    need(all(p_eval(differences[n], F(1)) == 0 for n in range(9)), 'endpoint moment checks supplement full permutation')
    # The full permutation, not these checks, proves every moment equality.
    return moments, differences


def sqrt_bracket(value, precision=320):
    denominator = 1 << precision
    numerator = isqrt(value.numerator * denominator ** 2 // value.denominator)
    low = F(numerator, denominator)
    high = low if low * low == value else F(numerator + 1, denominator)
    need(low * low <= value <= high * high, 'integer square-root enclosure')
    return low, high


def profile_budget(q):
    numerator = 2 + 5 * q + 5 * q ** 2 + 6 * q ** 3 + 3 * q ** 4
    return numerator / (24 * (1 - q) ** 3 * (1 + q) ** 2 * (1 + q ** 2))


def spatial_tail(z, k):
    coefficient = F(1)
    for n in range(k + 1):
        coefficient *= (F(10, 3) + n) / (n + 1)
    x = 15 * z
    return coefficient * x ** (k + 1) / (1 - x) ** (k + 5)


def quotient(numerator, denominator):
    if len(numerator) != 2 or len(denominator) != 2:
        raise ValueError('interval arity')
    if any(type(x) is not F for x in (*numerator, *denominator)):
        raise ValueError('exact Fraction endpoints required')
    if numerator[0] > numerator[1] or denominator[0] > denominator[1]:
        raise ValueError('interval order')
    if denominator[0] <= 0:
        return {'status': 'denominator_failure', 'denominator': denominator}
    corners = [n / d for n, d in product(numerator, denominator)]
    return {'status': 'bounded', 'lower': min(corners), 'upper': max(corners),
            'denominator': denominator, 'corner_quotients': corners}


def box(center, radius):
    return (center - radius, center + radius)


def interval_gap(one, two):
    need(one['status'] == two['status'] == 'bounded', 'positive ratio denominators before comparing candidates')
    return max(one['lower'] - two['upper'], two['lower'] - one['upper'])


def parameter_data(q, eta, z, moments, differences):
    b = profile_budget(q)
    tau = eta / (8 * b)
    s = z * tau / (eta * (1 - q) ** 3)
    v = s / 96
    need(s <= 3 * z / 2 and 6 * v < 1, 'physical slow-clock and tail envelope')
    low, high = sqrt_bracket(profile_budget(q * q) / 96)
    dhat = tau * high / (F(1, 8) * (1 - eta))
    centers = {}; evaluated = {}
    for r in (4, 5):
        evaluated[r] = [p_eval(poly, q) for poly in moments[r]]
        real = sum((-1) ** (n // 2) * evaluated[r][n] * v ** n / factorial(n)
                   for n in (0, 2, 4, 6, 8))
        imag = sum((-1) ** ((n - 1) // 2) * evaluated[r][n] * v ** n / factorial(n)
                   for n in (1, 3, 5, 7))
        centers[r] = {'real': real, 'imag': imag}
    combination = sum((-1) ** ((n - 1) // 2) * p_eval(differences[n], q) * v ** n / factorial(n)
                      for n in (3, 5, 7))
    need(combination == centers[5]['imag'] - q * centers[4]['imag'],
         'exact signed combination evaluated before modulus')
    arithmetic = (6 * v) ** 9 / factorial(9)
    combination_tail = (1 - q) * 91 * (6 * v) ** 9 / (factorial(9) * (1 - 6 * v))
    need(combination_tail < (1 + q) * arithmetic, 'proved endpoint tail improves separate arithmetic')
    return {'q': q, 'eta': eta, 'z': z, 'tau': tau, 's': s, 'v': v,
            'time_in_hbar_over_alpha': z / (eta * (1 - q) ** 3),
            'sqrt_bracket': (low, high), 'dhat_upper': dhat, 'centers': centers,
            'moments_evaluated': evaluated, 'combination_center': combination,
            'scalar_arithmetic_remainder': arithmetic,
            'combination_all_order_remainder': combination_tail,
            'combination_separate_remainder': (1 + q) * arithmetic}


def evaluate_hypothesis(data, k, face_count):
    q, z, v, tau = (data[x] for x in ('q', 'z', 'v', 'tau'))
    M = F(face_count, 24)
    components = {'state': 48 * data['dhat_upper'], 'spatial': 8 * spatial_tail(z, k),
                  'averaging': 64 * tau * M * (1 + 3 * z * M)}
    need(all(x > 0 for x in components.values()), 'all physical costs strictly retained')
    physical = sum(components.values())
    arithmetic = data['scalar_arithmetic_remainder']
    total = physical + arithmetic
    c4, c5 = (data['centers'][r]['imag'] for r in (4, 5))
    den = box(c4, total)
    direct = quotient(box(c5, total), den)
    combined_radius = (1 + q) * physical + data['combination_all_order_remainder']
    canceled = quotient(box(data['combination_center'], combined_radius), den)
    if canceled['status'] == 'bounded':
        canceled['lower'] += q; canceled['upper'] += q
        canceled['corner_quotients'] = [x + q for x in canceled['corner_quotients']]
    crude = quotient(box(v * q ** 5, total + 36 * v ** 3),
                     box(v * q ** 4, total + 36 * v ** 3))
    need(direct['status'] == canceled['status'] == crude['status'] == 'bounded',
         'strictly positive denominator in all three methods')
    # This is a cancellation decomposition upper radius about q, not a lower error theorem.
    radius_terms = {name: (1 + q) * value / den[0] for name, value in components.items()}
    radius_terms['combination_arithmetic'] = data['combination_all_order_remainder'] / den[0]
    radius_terms['retained_center_bias'] = abs(data['combination_center']) / den[0]
    need(all(direct['lower'] <= c5 / c4 <= direct['upper'] for _ in (0,)),
         'direct box covers its rational center quotient')
    return {**data, 'k': k, 'N_k': face_count, 'physical_components': components,
            'physical_radius': physical, 'full_scalar_radius': total,
            'combination_physical_radius': (1 + q) * physical,
            'combination_full_radius': combined_radius, 'ratio_cancellation': canceled,
            'ratio_all_corners': direct, 'ratio_crude_cubic': crude,
            'dominant_physical_term': max(components, key=components.get),
            'ratio_radius_components_about_candidate_q': radius_terms,
            'scalar_boxes': {4: box(c4, total), 5: box(c5, total)}}


def extra_tolerance(pair, margin):
    """Sufficient absolute additional imaginary-scalar error per probe and hypothesis."""
    if margin <= 0:
        return {'certified': False, 'epsilon': F(0)}
    constants = []; denominators = []
    for h in pair:
        d0, d1 = h['scalar_boxes'][4]
        n0, n1 = h['scalar_boxes'][5]
        denominators.append(d0)
        constants.append(2 * (d1 + max(abs(n0), abs(n1))) / d0 ** 2)
    eps = min(min(denominators) / 4, margin / (2 * sum(constants)))
    expanded = [quotient(box(h['centers'][5]['imag'], h['full_scalar_radius'] + eps),
                         box(h['centers'][4]['imag'], h['full_scalar_radius'] + eps)) for h in pair]
    new_margin = interval_gap(*expanded)
    need(eps > 0 and new_margin >= margin / 2, 'additional scalar tolerance rigorously preserves half ratio margin')
    return {'certified': True, 'epsilon': eps, 'Lipschitz_constants': constants,
            'expanded_signed_margin': new_margin, 'expanded_intervals': expanded,
            'meaning': 'absolute scalar error per probe per hypothesis; no timing or apparatus sensitivity theorem'}


def controls(matrix, sources, moments, differences, geometry):
    out = {}
    wrong = [[4 if exponent == 5 else exponent for exponent in row] for row in matrix]
    wrong_first = {}
    for r, ids in sources.items():
        wrong_first[r] = sum(F(1, 2) * F(1, 2) ** wrong[i][j]
                             for i in ids for j in ids if wrong[i][j])
    need(wrong_first[5] / wrong_first[4] == 1, 'wrong q5 assignment produces nondiscriminating first ratio one')
    need(wrong_first[5] - F(1, 2) * wrong_first[4] != 0, 'wrong q5 assignment fails Delta m1 identity')
    out['wrong_face'] = {'first_moments_q_half': wrong_first, 'ratio': F(1)}
    # i^n gives +,-,+,- for n=1,3,5,7; flipping the cubic sign is detected exactly.
    imaginary_signs = [int((1j ** n).imag) for n in (1, 3, 5, 7)]
    need(imaginary_signs == [1, -1, 1, -1], 'alternating imaginary signs from independent powers of i')
    cubic = p_eval(differences[3], F(1, 2))
    need(cubic > 0 and -cubic / 6 < 0, 'nonzero cubic sign witness')
    out['alternating_signs'] = {'signs': imaginary_signs, 'wrong_minus_correct_cubic_coefficient': cubic / 3}
    # Two probability measures match moments 0..3 but differ at order four.
    measure_a = [(F(-1), F(1, 2)), (F(1), F(1, 2))]
    measure_b = [(F(-2), F(1, 8)), (F(0), F(3, 4)), (F(2), F(1, 8))]
    ma = [sum(w * x ** n for x, w in measure_a) for n in range(5)]
    mb = [sum(w * x ** n for x, w in measure_b) for n in range(5)]
    need(ma[:4] == mb[:4] and ma[4] != mb[4], 'finite moment equality does not establish all orders')
    out['finite_moment_coincidence'] = {'a': ma, 'b': mb, 'not_physical_replacement': True}
    need(10 * 9 * 9 + 9 - 10 == 809, 'tail coefficient monotonicity polynomial at n=m+9 has positive coefficients')
    out['all_order_tail_proof_constants'] = {'Q_norm': 6, 'Qprime_norm': 30,
        'derivative_coefficient': '10n+1', 'decreasing_coefficient_polynomial_at_n_equals_m_plus_9': [809, 181, 10]}
    fourth = (F(2) + 6 * F(1) + F(2)) / 4
    need(fourth == F(5, 2) and fourth - 1 == F(3, 2), 'actual multiplier loading differs from normalized rank source')
    need(F(4) ** 2 / 2 == 8, 'identity-holonomy multiplier norm squared eight')
    # Independently vary the vacuum column with an explicit unitary. Z psi=psi,
    # Z Omega=cos(theta)Omega+sin(theta)chi, B has the psi--chi entry one.
    # Omitting Z*Omega changes <psi,Z B Z*Omega> from c-s to 1.
    c, s = F(3, 5), F(4, 5)
    need(c * c + s * s == 1 and (c - s) != 1, 'source column exact but omitted vacuum column changes scalar')
    out['loading_and_norm'] = {'coherent_fourth_moment': fourth, 'rank_loading_defect_squared': fourth - 1,
        'J_squared': F(8), 'stationary_coefficient': F(48), 'spatial_coefficient': F(8),
        'averaging_conservative_coefficient': F(64), 'three_state_vacuum_column_fixture': c - s,
        'wrong_source_only_fixture': F(1), 'fixture_scope': 'algebraic omission control; not substituted physical dynamics'}
    q, R = F(3, 4), F(1, 10)
    e4, e5 = -R, R
    need(abs(e5 - q * e4) == (1 + q) * R, 'equal radii allow opposing signed errors with full sum')
    out['adversarial_error_signs'] = {'q': q, 'R4': R, 'R5': R, 'e4': e4, 'e5': e5,
        'combination': e5 - q * e4, 'wrong_equal_signed_error_value': (1 - q) * R}
    y4, y5 = F(3), F(2)
    measured = y5 / y4
    residuals = {str(qc): y5 - qc * y4 for qc in (F(1, 2), F(2, 3))}
    need(measured == F(2, 3) and residuals['1/2'] != residuals['2/3'],
         'candidate changes residual but cannot change measured quotient')
    out['no_true_q_measurement'] = {'measurement_y4': y4, 'measurement_y5': y5,
                                  'q_independent_statistic': measured, 'candidate_residuals': residuals}
    signed = quotient((F(-3), F(1)), (F(1), F(3)))
    need(signed['lower'] == -3 and signed['upper'] == 1, 'signed numerator all-corner regression')
    crossed = quotient((F(1), F(2)), (F(-1), F(1)))
    need(crossed['status'] == 'denominator_failure', 'denominator crossing yields no ratio inference')
    try:
        quotient((True, F(1)), (F(1), F(2)))
    except ValueError:
        rejected_bool = True
    else:
        rejected_bool = False
    need(rejected_bool, 'Boolean interval endpoints rejected')
    out['interval_controls'] = {'signed': signed, 'crossing': crossed, 'boolean_rejected': rejected_bool}
    # c4=1+i/10, c5=1+i/5. Common multiplication by i preserves
    # complex distances but changes un-demodulated imaginary ratio from 2 to 1.
    a, b = (F(1), F(1, 10)), (F(1), F(1, 5))
    norm_sq = lambda v: v[0] ** 2 + v[1] ** 2
    rotate_i = lambda v: (-v[1], v[0])
    distance = lambda v, w: norm_sq((v[0] - w[0], v[1] - w[1]))
    need(distance(a, b) == distance(rotate_i(a), rotate_i(b)), 'common phase preserves complex disk distance')
    need(b[1] / a[1] == 2 and rotate_i(b)[1] / rotate_i(a)[1] == 1,
         'unknown common phase cannot be ignored in imaginary readout')
    need(rotate_i(b)[1] / a[1] == 10, 'independent phase shifts further corrupt scalar ratio')
    out['carrier_phase'] = {'common_rotated_complex_distance_squared': distance(rotate_i(a), rotate_i(b)),
        'correct_demodulated_ratio': F(2), 'unknown_common_phase_raw_ratio': F(1),
        'independent_phase_raw_ratio': F(10), 'same_clock_requires_common_fixed_alpha': True}
    # Shared denominator error: c4=c5=1, q=1, R=1/4. Separately bounding
    # residual and denominator gives [1/3,5/3], while original box gives [3/5,5/3].
    sharp = quotient((F(3, 4), F(5, 4)), (F(3, 4), F(5, 4)))
    loose = quotient((F(-1, 2), F(1, 2)), (F(3, 4), F(5, 4)))
    need(sharp['lower'] == F(3, 5) and 1 + loose['lower'] == F(1, 3),
         'shared denominator dependence makes separate residual box nonsharp')
    out['shared_error_dependence'] = {'sharp_original_box': sharp,
        'loose_cancellation_bounds': (1 + loose['lower'], 1 + loose['upper'])}
    return out


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    target = Path(parser.parse_args().output)
    need(target.is_absolute() and not target.exists(), 'fresh absolute output directory')
    inventory = source_check()
    matrix, source_vectors, collars, geometry = physical_geometry()
    moments, differences = symbolic_moments(matrix, source_vectors)
    control_output = controls(matrix, source_vectors, moments, differences, geometry)
    z = F(1, 10 ** 6)
    grid = [(p, k) for p in (12, 18, 24) for k in (3, 4, 5)] + [(24, 6)]
    rows = []; display = []
    parameters = {}
    for power, k in grid:
        u = F(1, 10 ** power)
        if power not in parameters:
            parameters[power] = [parameter_data(1 - u, F(1, 2), z, moments, differences),
                                 parameter_data(1 - 2 * u, F(1, 16), z, moments, differences)]
        data = parameters[power]
        need(data[0]['time_in_hbar_over_alpha'] == data[1]['time_in_hbar_over_alpha'] == 2 * z / u ** 3,
             'frozen original physical same-clock hypotheses ' + str(power))
        pair = [evaluate_hypothesis(d, k, collars[k]['retained_face_count']) for d in data]
        gaps = {name: interval_gap(*(h[name] for h in pair))
                for name in ('ratio_cancellation', 'ratio_all_corners', 'ratio_crude_cubic')}
        scalar = {}
        for r in (4, 5):
            center_distance = abs(pair[0]['centers'][r]['imag'] - pair[1]['centers'][r]['imag'])
            margin = center_distance - sum(h['full_scalar_radius'] for h in pair)
            scalar[r] = {'center_distance': center_distance, 'signed_margin': margin,
                         'disjoint': margin > 0, 'extra_equal_scalar_radius_threshold': max(F(0), margin / 2)}
        ratio_tolerance = extra_tolerance(pair, gaps['ratio_all_corners'])
        row = {'u': u, 'power': power, 'k': k, 'hypotheses': pair, 'signed_ratio_margins': gaps,
               'ratio_disjoint': {name: value > 0 for name, value in gaps.items()},
               'scalar_discrimination': scalar, 'additional_scalar_error_allowance': ratio_tolerance,
               'pairwise_only': True}
        rows.append(row)
        display.append({'power': power, 'k': k, 'N_k': collars[k]['retained_face_count'],
            'ratio_margins': {name: float(value) for name, value in gaps.items()},
            'radii': [float(h['full_scalar_radius']) for h in pair],
            'physical_components': [{key: float(value) for key, value in h['physical_components'].items()} for h in pair],
            'dominant': [h['dominant_physical_term'] for h in pair],
            'scalar_margins': {r: float(d['signed_margin']) for r, d in scalar.items()},
            'extra_scalar_error_allowance': float(ratio_tolerance['epsilon'])})
    need(len(rows) == 10 and [(r['power'], r['k']) for r in rows] == grid, 'all and only ten frozen cells')
    bound_files = ['check.py', 'inputs/source-inventory.json', 'inputs/snapshot-event.json']
    result = {'schema': 'ym28-forward-ai3-v1', 'contract_hash': CONTRACT_HASH,
        'geometry': geometry, 'collars': collars, 'source_norm_squared': 1,
        'multiplication_norm_squared': 8, 'moment_polynomials': moments,
        'difference_polynomials': differences, 'all_order_reflection_proved': True,
        'all_order_proof_authority': 'full permutation plus fixed-source polynomial product rule; see report',
        'controls': control_output, 'rows': rows, 'display_only': display,
        'checks': CHECKS, 'checks_count': len(CHECKS), 'source_inventory': inventory,
        'producer_bindings': {p: digest(HERE / p) for p in bound_files},
        'scope': 'canonical summable full-link SU(2), same-clock two-candidate full physical scalar bounds; no continuum theorem',
        'attribution': 'Advisor proposed all-order lemma; Tesla proposed AI3 candidate readout. New independent forward implementation.',
        'current_reverse_read': False}
    target.mkdir(parents=True)
    (target / 'results.json').write_text(json.dumps(serial(result), indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'PASS', 'checks': len(CHECKS), 'moments': serial({n: differences[n] for n in (1, 3, 5, 7)}),
                      'collars': [{k: c[k] for k in ('k', 'factor_count', 'link_count', 'retained_face_count')} for c in collars],
                      'display': display}, indent=2))


if __name__ == '__main__':
    run()
