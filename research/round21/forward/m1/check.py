#!/usr/bin/env python3
"""Exact fixtures for the M1 complete-factor strong-topology argument."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations, product
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = 'research/round21/contracts/m1.json'
INPUTS = [
    'research/round21/methods/agent-instructions-at-selection.md', CONTRACT,
    'research/round21/methods/paired-physics-research.md',
    'research/round21/advisor/post-six-selection.json',
    'research/round21/advisor/k2-gate.json',
    'research/round20/forward/h1/report.md',
    'research/round20/advisor/h1-gate.json',
    'research/round20/forward/h2/report.md',
    'research/round20/advisor/h2-gate.json',
    'research/round20/forward/g2/report.md',
    'research/round20/advisor/g2-gate.json',
    'research/round19/forward/a2/report.md',
    'research/round19/advisor/a2-gate.json',
    'research/round21/forward/j2/report.md',
    'research/round21/advisor/j2-gate.json',
    str((HERE / 'check.py').relative_to(ROOT)),
    str((HERE / 'report.md').relative_to(ROOT)),
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rejection(call):
    try:
        call()
    except ValueError:
        return True
    return False


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(obj):
    if isinstance(obj, Q):
        return str(obj)
    if isinstance(obj, dict):
        return {k: encode(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [encode(v) for v in obj]
    return obj


def write_json(path, obj):
    path.write_text(json.dumps(encode(obj), indent=2, sort_keys=True) + '\n')


def check_inputs():
    contract = json.loads((ROOT / CONTRACT).read_text())
    require(contract['loop'] == 'm1' and contract['status'] == 'frozen', 'M1 is not frozen')
    dependency = contract['depends_on']
    require(sha(ROOT / dependency['gate']) == dependency['sha256'], 'selection gate changed')
    selection = json.loads((ROOT / contract['selection_record']).read_text())
    require(selection['completed_loops_at_selection'] == ['i1', 'i2', 'j1', 'j2', 'k1', 'k2'],
            'M was not selected after the first six loops')
    require('m' in selection['goals'], 'M is absent from selection')
    pairs = [
        ('research/round20/advisor/h1-gate.json', 'research/round20/forward/h1/report.md', None),
        ('research/round20/advisor/h2-gate.json', 'research/round20/forward/h2/report.md', None),
        ('research/round20/advisor/g2-gate.json', 'research/round20/forward/g2/report.md', None),
        ('research/round19/advisor/a2-gate.json', 'research/round19/forward/a2/report.md', 'forward/a2/report.md'),
        ('research/round21/advisor/j2-gate.json', 'research/round21/forward/j2/report.md', None),
    ]
    for gate_path, report_path, historical_key in pairs:
        gate = json.loads((ROOT / gate_path).read_text())
        require(gate['status'] == 'accepted', 'inherited premise is not accepted')
        require(gate['files'][historical_key or report_path] == sha(ROOT / report_path),
                'admitted report changed: ' + report_path)
    for relative in INPUTS:
        require((ROOT / relative).is_file(), 'missing scientific input: ' + relative)
    return {relative: sha(ROOT / relative) for relative in INPUTS}


# Link = (axis, x, y, z); face = (first_axis, second_axis, x, y, z).
def link(axis, tail):
    require(axis in (0, 1, 2) and len(tail) == 3 and all(v >= 0 for v in tail),
            'link outside positive orthant')
    return (axis, *tail)


def face_links(face):
    a, b, *p = face
    require(0 <= a < b < 3 and all(v >= 0 for v in p), 'invalid face')
    pa, pb = p.copy(), p.copy()
    pa[a] += 1
    pb[b] += 1
    return {link(a, p), link(b, pa), link(a, pb), link(b, p)}


def selected(face):
    a, b, x, y, z = face
    return (a, b) == (0, 1) and y % 2 == 0 and x % 4 != 3


def owner(edge):
    axis, x, y, z = edge
    if axis == 0 and x % 4 != 3:
        return ('strip', x - x % 4, y - y % 2, z)
    if axis == 1 and y % 2 == 0:
        return ('strip', x - x % 4, y, z)
    return ('free', *edge)


def factor_links(factor):
    if factor[0] == 'free':
        return {tuple(factor[1:])}
    _, x, y, z = factor
    require(x % 4 == 0 and y % 2 == 0 and min(x, y, z) >= 0, 'invalid strip anchor')
    return ({(0, x + r, y + s, z) for r in range(3) for s in range(2)} |
            {(1, x + r, y, z) for r in range(4)})


def complete_cover(edges):
    return set().union(*(factor_links(owner(e)) for e in edges)) if edges else set()


def require_complete(edges):
    require(complete_cover(edges) == edges, 'support omits links in a complete factor')


def incident(edge):
    axis, *p = edge
    faces = set()
    for transverse in range(3):
        if transverse == axis:
            continue
        for offset in (0, -1):
            anchor = p.copy()
            anchor[transverse] += offset
            if min(anchor) >= 0:
                a, b = sorted((axis, transverse))
                faces.add((a, b, *anchor))
    return faces


def meeting(edges, omitted_only=True):
    faces = set().union(*(incident(e) for e in edges)) if edges else set()
    return {f for f in faces if not selected(f)} if omitted_only else faces


def brute_meeting(edges):
    maximum = [max(e[i + 1] for e in edges) for i in range(3)]
    found = set()
    for a, b in combinations(range(3), 2):
        for p in product(*(range(n + 1) for n in maximum)):
            face = (a, b, *p)
            if not selected(face) and face_links(face) & edges:
                found.add(face)
    return found


def profile(q, eta=Q(1, 2), alpha=Q(1), E_star=Q(1), hbar=Q(1)):
    require(0 < q < 1, 'q must lie strictly between zero and one')
    require(0 < eta < 1, 'eta requires a strict positive budget')
    require(alpha > 0 and E_star > 0 and hbar > 0, 'positive fixed physical scales required')
    budget = B(q)
    tau = eta / (8 * budget)
    variance = alpha * alpha * tau * tau * B(q * q) / 96
    return {'q': q, 'eta': eta, 'alpha_over_E_star': alpha / E_star,
            'B': budget, 'tau': tau, 'sigma_squared': variance,
            'g_bar': alpha * (1 - eta) / 8,
            'perturbation_norm': alpha * tau * budget,
            'variance_scaled': variance / (alpha * alpha * (1 - q) ** 3)}


def B(q):
    return (2 + 5*q + 5*q*q + 6*q**3 + 3*q**4) / (
        24 * (1 - q)**3 * (1 + q)**2 * (1 + q*q))


def B_by_classes(q):
    return (Q(2, 24) / (1-q)**3 + q / (24*(1-q)**2*(1-q*q)) +
            q**3 / (24*(1-q**4)*(1-q*q)*(1-q)))


def B_by_subtraction(q):
    return Q(1, 8)/(1-q)**3 - (1+q+q*q)/(24*(1-q**4)*(1-q*q)*(1-q))


def poly_add(*polys):
    result = [0] * max(map(len, polys))
    for p in polys:
        for i, value in enumerate(p):
            result[i] += value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_mul(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            result[i+j] += av*bv
    return result


def scale(a, n):
    return [n*v for v in a]


def symbolic_profile_identity():
    # Common denominator: 24(1-q)^3(1+q)^2(1+q^2).
    plus = [1, 1]
    square = poly_mul(plus, plus)
    fourth = poly_mul(square, [1, 0, 1])
    numerator_from_classes = poly_add(
        scale(fourth, 2), poly_mul([0, 1], poly_mul(plus, [1, 0, 1])), [0, 0, 0, 1])
    numerator_from_subtraction = poly_add(
        scale(fourth, 3), [-1, -1, -1])
    expected = [2, 5, 5, 6, 3]
    require(numerator_from_classes == numerator_from_subtraction == expected,
            'exact profile polynomial identity failed')
    residue = Q(sum(expected), 24 * 4 * 2)
    require(residue == Q(7, 64), 'profile cubic residue differs')
    eta = Q(1, 2)
    variance_limit = eta**2 / (64 * 96 * 8 * residue)
    require(variance_limit == eta**2 / 5376, 'exact residual asymptotic differs')
    return {'numerator': expected, 'B_cubic_residue': residue,
            'tau_cubic_coefficient_for_eta_half': eta/(8*residue),
            'variance_cubic_coefficient_for_eta_half': variance_limit}


def sqrt_upper(value, bits=80):
    require(value >= 0, 'square-root argument negative')
    denominator = 1 << bits
    floor = isqrt(value.numerator * denominator**2 // value.denominator)
    lower = Q(floor, denominator)
    upper = lower if lower*lower == value else Q(floor+1, denominator)
    require(lower*lower <= value <= upper*upper and upper-lower <= Q(1, denominator),
            'controlled rational square root enclosure failed')
    return upper


def matmul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), Q())
             for j in range(len(b[0]))] for i in range(len(a))]


def matrix_difference(a, b):
    return [[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def geometry_fixtures():
    original = face_links((0, 2, 0, 0, 0))
    covered = complete_cover(original)
    remote = (0, 2, 2, 1, 0)
    require(len(original) == 4 and len(covered) == 22, 'complete cover fixture changed')
    require(remote in meeting(covered) and remote not in meeting(original),
            'remote omitted face does not discriminate edge-only support')
    fixtures = {
        'boundary_strip': factor_links(('strip', 0, 0, 0)),
        'interior_strip': factor_links(('strip', 4, 2, 1)),
        'origin_z_free_link': {(2, 0, 0, 0)},
        'separator_x_free_link': {(0, 3, 0, 0)},
        'boundary_wilson_complete_cover': covered,
        'interior_wilson_complete_cover': complete_cover(face_links((0, 2, 5, 3, 2))),
    }
    rows = []
    for name, edges in sorted(fixtures.items()):
        require_complete(edges)
        for e in edges:
            require(len(incident(e)) <= 4 and all(e in face_links(f) for f in incident(e)),
                    'link-face incidence failed')
            require(e in factor_links(owner(e)), 'factor owner loses its link')
        factors = {owner(e) for e in edges}
        for fac in factors:
            require(all(owner(e) == fac for e in factor_links(fac)), 'factor supports overlap')
        omitted = meeting(edges)
        require(omitted == brute_meeting(edges), 'incidence misses an omitted face')
        require(len(meeting(edges, False)) <= 4*len(edges), 'complete incidence degree bound failed')
        require(len(omitted) <= 4*len(edges), 'omitted incidence degree bound failed')
        budgets = []
        for q in (Q(1, 2), Q(3, 4), Q(7, 8)):
            D = sum((q**sum(f[2:])/24 for f in omitted), Q())
            require(D <= Q(len(edges), 6), 'complete local budget exceeds universal bound')
            budgets.append({'q': q, 'D_F': D, 'universal_upper': Q(len(edges), 6)})
        rows.append({'name': name, 'factor_count': len(factors), 'link_count': len(edges),
                     'omitted_face_count': len(omitted), 'all_face_count': len(meeting(edges, False)),
                     'links': sorted(edges), 'omitted_faces': sorted(omitted), 'budgets': budgets})
    require(len(incident((2, 0, 0, 0))) == 2 and len(incident((2, 1, 1, 1))) == 4,
            'orthant boundary incidence convention failed')
    return rows, covered, {'displayed_links': sorted(original), 'full_link_count': len(covered),
                           'missed_omitted_face': remote,
                           'edge_only_support_rejected': rejection(lambda: require_complete(original))}


def main(output):
    require(output.is_absolute(), 'fresh output path must be absolute')
    require(not output.exists(), 'output must be fresh; historical evidence is immutable')
    inputs = check_inputs()
    identity = symbolic_profile_identity()
    geometry, support, support_control = geometry_fixtures()
    local_faces = meeting(support)
    alpha, eta, A_norm = Q(1), Q(1, 2), Q(3, 2)
    rows = []
    for q in (Q(1, 2), Q(3, 4), Q(7, 8), Q(15, 16), Q(31, 32), Q(63, 64)):
        row = profile(q, eta, alpha)
        require(row['B'] == B_by_classes(q) == B_by_subtraction(q), 'profile fixture differs')
        D = sum((q**sum(f[2:])/24 for f in local_faces), Q())
        commutator = 2*alpha*row['tau']*D
        coarse = alpha*row['tau']*len(support)/3
        sigma_upper = sqrt_upper(row['sigma_squared'])
        require(commutator <= coarse, 'complete commutator coefficient is incorrect')
        require(row['perturbation_norm'] == alpha*eta/8 > 0, 'constant norm budget failed')
        row.update({'support_links': len(support), 'D_F': D, 'A_norm': A_norm,
                    'commutator_over_A_norm_upper': commutator,
                    'coarse_commutator_over_A_norm_upper': coarse,
                    'sigma_upper': sigma_upper,
                    'local_vector_norm_upper': A_norm*(sigma_upper+commutator),
                    'energy_shift_absolute_upper': row['sigma_squared']/row['g_bar']})
        rows.append(row)
    require(B(Q(1, 2)) == Q(107, 135), 'dyadic profile regression failed')
    # Moving-vector and fixed-vector quantifiers for P_n on ell2.
    coefficients = {0: Q(3, 5), 2: Q(4, 5)}
    require(sum(v*v for v in coefficients.values()) == 1, 'fixed vector not normalized')
    moving = [{'n': n, 'fixed_vector_image_squared': coefficients.get(n, Q())**2,
               'moving_vector_image_squared': Q(1), 'operator_norm': Q(1)}
              for n in (1, 2, 3, 5, 8)]
    require(all(r['fixed_vector_image_squared'] == 0 for r in moving if r['n'] > 2),
            'fixed finite-support tail failed')
    diagonal = [{'n': n, 'bounded_reference_resolvent_norm_squared': Q(1, 2),
                 'unbounded_reference_resolvent_norm_squared': Q(1, (n*n+1)*((n+1)**2+1))}
                for n in (1, 2, 4, 8, 16)]
    require(all(diagonal[i+1]['unbounded_reference_resolvent_norm_squared'] <
                diagonal[i]['unbounded_reference_resolvent_norm_squared']
                for i in range(len(diagonal)-1)), 'resolvent control did not discriminate')
    # The universal commutator coefficient 2 is attained by Pauli Z and X.
    Z, X = [[Q(1), Q(0)], [Q(0), Q(-1)]], [[Q(0), Q(1)], [Q(1), Q(0)]]
    commutator_matrix = matrix_difference(matmul(Z, X), matmul(X, Z))
    gram = matmul(transpose(commutator_matrix), commutator_matrix)
    require(gram[0][1] == gram[1][0] == 0 and gram[0][0] == gram[1][1],
            'commutator Gram is not scalar')
    commutator_square_norm = gram[0][0]
    require(commutator_square_norm > 1, 'factor-two commutator control missing')
    # exp(-i*pi*P_n) is +1 off e_n and -1 on e_n.
    identity2 = [[Q(1), Q(0)], [Q(0), Q(1)]]
    unitary_difference = matrix_difference(Z, identity2)
    unitary_gram = matmul(transpose(unitary_difference), unitary_difference)
    unitary_norm_squared = max(unitary_gram[0][0], unitary_gram[1][1])
    controls = {
        'complete_factor_cover_required': support_control['edge_only_support_rejected'],
        'remote_face_missing_from_displayed_edges_detected':
            tuple(support_control['missed_omitted_face']) not in meeting(set(support_control['displayed_links'])),
        'orthant_negative_anchor_rejected': rejection(lambda: face_links((0, 1, -1, 0, 0))),
        'q_one_rejected': rejection(lambda: profile(Q(1))),
        'q_zero_rejected': rejection(lambda: profile(Q(0))),
        'eta_one_rejected': rejection(lambda: profile(Q(1, 2), eta=Q(1))),
        'eta_zero_rejected': rejection(lambda: profile(Q(1, 2), eta=Q(0))),
        'zero_E_star_rejected': rejection(lambda: profile(Q(1, 2), E_star=Q(0))),
        'zero_hbar_rejected': rejection(lambda: profile(Q(1, 2), hbar=Q(0))),
        'zero_alpha_rejected': rejection(lambda: profile(Q(1, 2), alpha=Q(0))),
        'factor_two_commutator_loss_detected': commutator_square_norm == 4,
        'moving_vector_invalidates_uniform_unit_sphere_claim': all(r['moving_vector_image_squared'] == 1 for r in moving),
        'strong_does_not_imply_norm_resolvent': all(r['bounded_reference_resolvent_norm_squared'] == Q(1, 2) for r in diagonal),
        'nonzero_perturbation_norm_does_not_imply_norm_resolvent_failure': diagonal[-1]['unbounded_reference_resolvent_norm_squared'] < Q(1, 1000),
        'strong_does_not_imply_propagator_norm': rejection(lambda: require(unitary_norm_squared == 0,
            'moving rank-one perturbation has nonzero unitary norm difference')),
        'dyadic_ledger_cannot_be_reused_after_q_changes': B(Q(3, 4)) != Q(107, 135),
    }
    require(all(controls.values()), 'M1 control failed')
    comparison = {
        'strong_perturbation_limit_zero': True,
        'operator_norm_limit_zero': False,
        'strong_resolvent_limit': True,
        'compact_time_strong_unitary_limit': True,
        'norm_resolvent_conclusion': False,
        'homogeneous_limit_obtained': False,
    }
    result = {
        'schema': 'ym21-forward-m1-v1', 'loop': 'm1', 'direction': 'forward',
        'passed': True, 'comparison': comparison,
        'source_hashes': inputs,
        'profile_identity': identity, 'profile_fixtures': rows,
        'support_fixtures': geometry, 'complete_support_control': support_control,
        'moving_projection_fixtures': moving, 'resolvent_topology_fixtures': diagonal,
        'unitary_counterexample_at_time_pi': {'hbar': 1, 'difference_norm_squared': unitary_norm_squared,
                                              'model': 'H_ref=0,V_n=P_n on ell2'},
        'commutator_counterexample': {'operators': 'Pauli Z and X',
                                    'matrix': commutator_matrix, 'commutator_norm_squared': commutator_square_norm},
        'controls': controls,
        'theorem': {
            'local_vector_bound': '||V_q A Omega|| <= ||A||[sigma_q+2 alpha tau_q D_F(q)] <= ||A||[sigma_q+alpha tau_q |E(F)|/3]',
            'domain': 'D(H_q)=D(H_ref), with unchanged closed form domain',
            'resolvent': 'strong at every fixed nonreal z',
            'unitary': 'for every fixed psi and fixed finite T, uniformly on |t|<=T, also after subtracting e_q',
            'norm_resolvent_status': 'unresolved; false comparison flag means no norm conclusion, not a failure theorem',
            'propagator_norm_status': 'unresolved',
            'growing_time_windows': 'not examined in M1',
            'physical_correlator_transfer': 'reserved for evidence-selected M2',
        },
        'limits': ['fixed A2 full-link incomplete tensor product', 'fixed positive alpha/E_star and hbar, fixed spacing',
                   'no nonzero homogeneous omitted coupling', 'q=1 is not a member of the summable profile family',
                   'no K/L diffusion identification', 'no continuum or physical mass claim', 'scientific priority unverified'],
    }
    output.mkdir(parents=True)
    write_json(output/'results.json', result)
    write_json(output/'controls.json', controls)
    manifest = {'schema': 'ym21-source-manifest-v1', 'loop': 'm1', 'direction': 'forward',
                'inputs': inputs,
                'outputs': {name: sha(output/name) for name in ['results.json', 'controls.json']}}
    write_json(output/'source-manifest.json', manifest)
    print(json.dumps({'loop': 'm1', 'direction': 'forward', 'passed': True,
                      'support_fixtures': len(geometry), 'controls': len(controls),
                      'results_sha256': sha(output/'results.json')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    main(args.output)
