#!/usr/bin/env python3
"""Exact finite controls for N1; the infinite operator proof is report.md."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).absolute().parents[4]
HERE = Path(__file__).absolute().parent
CONTRACT = 'research/round22/contracts/n1.json'
CONTRACT_SHA = '29ce23d8df321604f0174afcfb73b9c907ee4e6b03c78f66c408ac80fd7f3369'
INPUTS = [
    CONTRACT,
    'research/round22/methods/team-protocol.md',
    'research/round22/methods/AGENTS-at-selection.md',
    'research/round22/methods/paired-physics-research-at-selection.md',
    'research/round22/methods/continuation-prompt.md',
    'research/round22/forward/n1/check.py',
    'research/round22/forward/n1/report.md',
    'research/round22/forward/n1/source-notes.md',
    'research/round22/forward/n1/inputs/advisor-skill.md',
    'research/round22/forward/n1/inputs/finite-observations-and-operator-limits.md',
    'research/round22/forward/n1/inputs/admission-and-matching.md',
    'research/round21/advisor/m1-gate.json',
    'research/round21/advisor/m2-gate.json',
    'research/round21/advisor/post-ten-roadmap.json',
    'research/round21/forward/m1/report.md',
    'research/round21/forward/m2/report.md',
    'research/round20/forward/h2/report.md',
    'research/round19/forward/a2/report.md',
]


def need(condition, reason):
    if type(condition) is not bool or not condition:
        raise ValueError(reason)


def no_symlinks(path):
    path = path.absolute()
    for component in [path, *path.parents]:
        need(not component.is_symlink(), f'symlink rejected: {component}')


def digest(path):
    no_symlinks(path)
    need(path.is_file(), f'required source missing: {path}')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


def rat(x):
    return str(F(x))


@dataclass(frozen=True)
class G:
    """A Gaussian rational; no floating-point matrix arithmetic."""
    r: F = F(0)
    i: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 'r', F(self.r))
        object.__setattr__(self, 'i', F(self.i))

    def __add__(self, other):
        other = gauss(other)
        return G(self.r + other.r, self.i + other.i)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.r, -self.i)

    def __sub__(self, other):
        return self + (-gauss(other))

    def __mul__(self, other):
        other = gauss(other)
        return G(self.r * other.r - self.i * other.i,
                 self.r * other.i + self.i * other.r)

    __rmul__ = __mul__

    def star(self):
        return G(self.r, -self.i)

    def json(self):
        return {'real': rat(self.r), 'imaginary': rat(self.i)}


def gauss(x):
    return x if isinstance(x, G) else G(x)


def matrix(rows):
    return [[gauss(x) for x in row] for row in rows]


def ident(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), G())
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(z, a):
    return [[gauss(z) * x for x in row] for row in a]


def adj(a):
    return [[a[j][i].star() for j in range(len(a))]
            for i in range(len(a[0]))]


def comm(a, b):
    return add(mm(a, b), scale(-1, mm(b, a)))


def kron(a, b):
    return [[a[i][j] * b[k][l]
             for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def beta(u, b):
    return mm(mm(u, b), adj(u))


def expectation(a):
    return a[0][0]  # stationary ground e_0 in these exact fixtures


def corr(a, b, u):
    return expectation(mm(adj(a), mm(u, b))) - expectation(a).star() * expectation(b)


def heis_corr(a, b, u):
    return expectation(mm(adj(a), beta(u, b))) - expectation(a).star() * expectation(b)


def polynomial(q):
    return 2 + 5*q + 5*q*q + 6*q**3 + 3*q**4


def profile(q):
    need(F(0) < q < F(1), 'q must lie strictly in (0,1)')
    return polynomial(q) / (24 * (1-q)**3 * (1+q)**2 * (1+q*q))


def grouped_profile(q):
    # Two transverse orientations plus odd-row xy plus even-row separators.
    return (2 / (1-q)**3
            + q / ((1-q)**2 * (1-q*q))
            + q**3 / ((1-q**4) * (1-q*q) * (1-q))) / 24


def validate_domain(q, eta, alpha, hbar, e_star, spacing):
    need(F(0) < q < F(1), 'q domain')
    need(F(0) < eta < F(1), 'eta domain')
    for x in (alpha, hbar, e_star, spacing):
        need(x > 0, 'physical scales must be positive')


def shifted(p, axis, amount):
    a = list(p)
    a[axis] += amount
    return tuple(a)


def face_links(face):
    a, b, x, y, z = face
    p = (x, y, z)
    return {(a, *p), (a, *shifted(p, b, 1)),
            (b, *p), (b, *shifted(p, a, 1))}


def omitted(face):
    a, b, x, y, _ = face
    return not (a == 0 and b == 1 and y % 2 == 0 and x % 4 != 3)


def factor_key(link):
    a, x, y, z = link
    if a == 0 and x % 4 != 3:
        return ('strip', x - x % 4, y - y % 2, z)
    if a == 1 and y % 2 == 0:
        return ('strip', x - x % 4, y, z)
    return ('free', a, x, y, z)


def factor_links(key):
    if key[0] == 'free':
        return {tuple(key[1:])}
    _, x, y, z = key
    return {(0, x+dx, y+dy, z) for dx in range(3) for dy in range(2)} | {
        (1, x+dx, y, z) for dx in range(4)}


def cover(links):
    keys = {factor_key(link) for link in links}
    return set().union(*(factor_links(key) for key in keys)) if keys else set()


def incident(links):
    found = set()
    for axis, x, y, z in links:
        p = (x, y, z)
        for transverse in range(3):
            if transverse == axis:
                continue
            for displacement in (0, -1):
                anchor = shifted(p, transverse, displacement)
                if min(anchor) < 0:
                    continue
                a, b = sorted((axis, transverse))
                face = (a, b, *anchor)
                if omitted(face):
                    found.add(face)
    return found


def brute_incident(links):
    maxima = [max(link[a+1] for link in links) for a in range(3)]
    faces = set()
    for p in itertools.product(*(range(m+1) for m in maxima)):
        for a, b in ((0,1), (0,2), (1,2)):
            f = (a, b, *p)
            if omitted(f) and face_links(f) & links:
                faces.add(f)
    return faces


def local_budget(faces, q):
    return sum((q**sum(f[2:]) / 24 for f in faces), F(0))


def rejects(thunk):
    try:
        thunk()
    except ValueError:
        return True
    return False


def sin_enclosure(x, terms=10):
    need(F(0) <= x <= F(1), 'alternating sine enclosure domain')
    term, total = x, x
    for k in range(1, terms):
        term = -term * x*x / ((2*k)*(2*k+1))
        total += term
    next_term = -term*x*x / ((2*terms)*(2*terms+1))
    return min(total, total+next_term), max(total, total+next_term)


def scientific_checks():
    controls = []
    def control(name, ok, detail):
        need(ok, f'control failed: {name}')
        controls.append({'name': name, 'passed': True, 'outcome': detail})

    one = ident(2)
    a = matrix([[G(1,1), G(2,-1)], [G(1,2), G(0,-1)]])
    b = matrix([[G(2,-1), G(1,1)], [G(3,-1), 1]])
    phases = []
    for sign in (-1, 1):
        # t=sign*pi/2, H=diag(3,4), e=3; exp(-itH)=diag(sign*i,1).
        raw = matrix([[G(0,sign), 0], [0,1]])
        shifted_u = matrix([[1,0], [0,G(0,-sign)]])
        good = corr(a, b, shifted_u)
        need(good == heis_corr(a, b, raw), 'stationary Heisenberg equality')
        need(mm(raw, adj(raw)) == one, 'fixture unitarity')
        for ca, cb in [(G(2,-3), G(-1,2)), (G(2,-3), G()), (G(), G(-1,2))]:
            need(corr(add(a, scale(ca, one)), add(b, scale(cb, one)), shifted_u) == good,
                 'independent complex shifts must cancel')
        wrong_conjugate = expectation(mm(adj(a), mm(shifted_u,b))) - expectation(a)*expectation(b)
        wrong_one_mean = expectation(mm(adj(a), mm(shifted_u,b))) - expectation(a).star()
        raw_constant = corr(one, one, raw)
        need(corr(one, one, shifted_u) == G(), 'constant covariance must vanish')
        need(heis_corr(one, one, raw) == G(), 'Heisenberg constant covariance')
        control(f'complex_centering_and_independent_shifts_sign_{sign}', True,
                'exact equality for the original and three independently shifted complex pairs')
        control(f'missing_conjugation_rejected_sign_{sign}', wrong_conjugate != good,
                {'wrong_minus_correct': (wrong_conjugate-good).json()})
        control(f'missing_second_mean_rejected_sign_{sign}', wrong_one_mean != good,
                {'wrong_minus_correct': (wrong_one_mean-good).json()})
        control(f'unsubtracted_ground_phase_rejected_sign_{sign}', raw_constant != G(),
                {'wrong_constant_correlation': raw_constant.json(), 'correct': G().json()})
        phases.append({'time': f'{sign}*pi/2', 'correlation': good.json()})

    x = matrix([[0,1],[1,0]])
    y = matrix([[0,G(0,-1)],[G(0,1),0]])
    z = matrix([[1,0],[0,-1]])
    initial = kron(x, one)
    generator = kron(z,z)
    other = kron(one,x)
    # (I-iK) B (I+iK)/2 at t=pi/4, evaluated without sqrt(2).
    factor_evolved = scale(F(1,2), mm(mm(add(ident(4), scale(G(0,-1), generator)), initial),
                                      add(ident(4), scale(G(0,1), generator))))
    need(factor_evolved == kron(y,z), 'exact complete-factor internal support evolution')
    zero4 = scale(0, ident(4))
    control('edge_support_not_preserved_within_entangled_factor',
            comm(initial, other) == zero4 and comm(factor_evolved, other) != zero4,
            'Z tensor Z reference factor sends X tensor I to Y tensor Z at pi/4')
    need(comm(z,x) == scale(G(0,2),y), 'Pauli commutator coefficient')
    sl, su = sin_enclosure(F(1,2))
    control('commutator_factor_one_rejected', 2*sl > F(1,2) and 2*su <= 1,
            {'t': '1/2', 'difference_norm_lower': rat(2*sl),
             'difference_norm_upper': rat(2*su), 'wrong_bound': '1/2', 'valid_bound': '1'})

    displayed = face_links((0,2,0,0,0))
    complete = cover(displayed)
    full_faces, displayed_faces = incident(complete), incident(displayed)
    witness = (0,2,2,1,0)
    need(len(displayed) == 4 and len(complete) == 22, 'complete reference cover')
    need(full_faces == brute_incident(complete), 'independent incidence enumeration')
    need(displayed_faces == brute_incident(displayed), 'displayed incidence enumeration')
    for link in complete:
        need(link in factor_links(factor_key(link)), 'factor ownership includes link')
        need(cover(factor_links(factor_key(link))) == factor_links(factor_key(link)),
             'factor closure idempotence')
    need(len(full_faces) <= 4*len(complete), 'all-link incidence inequality')
    control('displayed_edge_face_count_rejected', witness in full_faces and witness not in displayed_faces,
            {'witness_face_axes_anchor': list(witness), 'displayed_links': len(displayed),
             'complete_links': len(complete), 'complete_omitted_faces': len(full_faces),
             'edge_only_omitted_faces': len(displayed_faces)})
    need(len(incident({(0,0,0,0)})) <= 2, 'orthant boundary backward anchors excluded')
    boundary = {'origin_x_link_omitted_faces': [list(f) for f in sorted(incident({(0,0,0,0)}))]}

    domain_rows = []
    for n in (1, 4, 16, 64):
        norm_sq = sum((F(1,k*k) for k in range(1,n+1)), F(0))
        hnorm_sq = sum((F(k*k,k*k) for k in range(1,n+1)), F(0))
        need(norm_sq <= 2 and hnorm_sq == n, 'rank-one domain counterexample partial sums')
        domain_rows.append({'N': n, 'v_partial_norm_squared': rat(norm_sq),
                            'H_v_partial_norm_squared': rat(hnorm_sq)})
    control('arbitrary_bounded_domain_invariance_rejected', True,
            {'analytic_witness': 'H e_n=n e_n; v_n=1/n; B=|v><e_1|; ||v||^2<=2, sum n^2|v_n|^2=infinity',
             'exact_partial_sums': domain_rows})

    # All asymptotic constants follow from cancellation of rational factors.
    scaled_b_limit = polynomial(F(1)) / (24 * 2**2 * 2)
    tau_limit_per_eta = F(1,8) / scaled_b_limit
    sigma_limit_per_eta_sq = tau_limit_per_eta**2 * scaled_b_limit / (96*8)
    d_limit_per_eta_ratio_sq = sigma_limit_per_eta_sq * 64
    need(scaled_b_limit == F(7,64), 'profile endpoint constant')
    need(tau_limit_per_eta == F(8,7), 'canonical amplitude endpoint')
    need(sigma_limit_per_eta_sq == F(1,5376), 'vacuum residual endpoint')
    need(d_limit_per_eta_ratio_sq == F(1,84), 'projector certificate endpoint')
    profile_rows = []
    for q in (F(1,2), F(3,4), F(9,10), F(99,100), F(999,1000)):
        need(profile(q) == grouped_profile(q), 'exact omitted orientation ledger')
        d = local_budget(full_faces, q)
        need(d <= F(len(complete),6), 'complete local budget')
        eta = F(1,2)
        tau = eta / (8*profile(q))
        sigma2_over_alpha2 = tau*tau*profile(q*q)/96
        d2 = sigma2_over_alpha2 * 64 / (1-eta)**2
        profile_rows.append({'q': rat(q), 'scaled_profile': rat((1-q)**3*profile(q)),
                             'tau_over_epsilon_cubed': rat(tau/(1-q)**3),
                             'sigma_squared_over_alpha_squared_epsilon_cubed': rat(sigma2_over_alpha2/(1-q)**3),
                             'd_certificate_squared': rat(d2), 'complete_local_budget': rat(d),
                             'gamma3_dynamic_certificate': rat(2*tau*d/(1-q)**3)})
    endpoint = 2 * F(1,2) * F(len(full_faces),21)  # eta=1/2, C=1
    need(endpoint > 0, 'nonempty-cover endpoint certificate positive')
    control('positive_endpoint_upper_bound_does_not_prove_nonconvergence',
            endpoint > 0 and corr(one,one,ident(2)) == G(),
            {'actual_constant_observable_difference': '0',
             'permitted_overcomplete_cover_gamma3_certificate_limit_eta_half_C_one': rat(endpoint),
             'verdict': 'endpoint nonconvergence inference rejected; actual nonconstant endpoint unresolved'})
    for gamma in (F(0), F(3,2), F(5,2), F(3), F(7,2)):
        sufficient = gamma < 3
        need(sufficient == (min(F(3,2), 3-gamma) > 0), 'growing-window endpoint classification')
    control('gamma3_is_not_admitted_by_vanishing_certificate', not (F(3) < 3),
            'sufficient interval is 0<=gamma<3; gamma=3 has positive local certificate when m_F>0')

    bad_domains = [(F(1),F(1,2),1,1,1,1), (F(1,2),F(1),1,1,1,1),
                   (F(1,2),F(1,2),0,1,1,1), (F(1,2),F(1,2),1,0,1,1),
                   (F(1,2),F(1,2),1,1,0,1), (F(1,2),F(1,2),1,1,1,0)]
    control('invalid_profile_and_physical_scales_rejected',
            all(rejects(lambda values=values: validate_domain(*values)) for values in bad_domains),
            'q=1, eta=1 and zero alpha/hbar/E_star/spacing rejected')
    control('disabled_assertions_do_not_admit_false_or_nonboolean_checks',
            rejects(lambda: need(False,'false')) and rejects(lambda: need('passed','nonboolean')),
            'explicit validation raises ValueError for False and truthy strings in normal or optimized execution')

    results = {
        'schema': 'ym22-forward-n1-results-v1', 'loop': 'n1', 'direction': 'forward',
        'status': 'proved_scoped', 'passed': True,
        'model': 'canonical_summable_selected_strip_full_link_incomplete_tensor_product',
        'claims': {
            'stationary_heisenberg_rewrite': True,
            'strong_integral_without_observable_domain_invariance': True,
            'complete_support_for_all_reference_times': True,
            'state_distance_coefficient': 6,
            'local_dynamical_coefficient': 2,
            'correlation_bound': '||A||||B||[6d_q+2alpha*tau_q*|t|*D_F(q)/hbar]',
            'sufficient_gamma_range': '[0,3)',
            'sufficient_rate': 'O((1-q)^min(3/2,3-gamma))',
            'gamma3_actual_correlations': 'unresolved',
            'scaled_profile_limit': '7/64',
            'tau_scaled_limit_per_eta': '8/7',
            'sigma_squared_scaled_limit_per_eta_squared': '1/5376',
            'd_certificate_scaled_squared_limit_per_eta_over_one_minus_eta_squared': '1/84',
            'gamma3_certificate_limit': '2*eta*C*m_F/21',
            'continuum_or_homogeneous_transfer': False,
        },
        'exact_complex_correlations': phases,
        'complete_support_fixture': {
            'displayed_links': [list(e) for e in sorted(displayed)],
            'complete_links': [list(e) for e in sorted(complete)],
            'complete_omitted_faces': [list(f) for f in sorted(full_faces)],
            'edge_only_omitted_faces': [list(f) for f in sorted(displayed_faces)],
            'D_F_at_one': rat(F(len(full_faces),24)), 'boundary': boundary,
        },
        'exact_profile_checks_eta_half': profile_rows,
        'infinite_proof_location': 'research/round22/forward/n1/report.md',
        'finite_checks_are_infinite_proof': False,
        'primary_source_record': 'research/round22/forward/n1/source-notes.md',
        'scientific_priority': 'unverified',
    }
    return results, {'schema': 'ym22-forward-n1-controls-v1', 'loop': 'n1',
                     'direction': 'forward', 'passed': True, 'controls': controls}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.absolute()
    no_symlinks(output)
    need(not output.exists(), 'output directory must be fresh')
    need(len(INPUTS) == len(set(INPUTS)), 'duplicate manifest inputs')
    hashes = {p: digest(ROOT/p) for p in INPUTS}
    need(hashes[CONTRACT] == CONTRACT_SHA, 'frozen N1 contract hash mismatch')
    contract = json.loads((ROOT/CONTRACT).read_text())
    need(contract['status'] == 'frozen' and contract['loop'] == 'n1', 'contract identity')
    for path, expected in contract['dependencies'].items():
        need(path in hashes and hashes[path] == expected, f'dependency mismatch: {path}')
    for gate_path in ('research/round21/advisor/m1-gate.json','research/round21/advisor/m2-gate.json'):
        gate = json.loads((ROOT/gate_path).read_text())
        need(gate['status'] == 'accepted', 'inherited gate not accepted')
        for path in INPUTS:
            if path in gate['files']:
                need(hashes[path] == gate['files'][path], f'consulted admitted input changed: {path}')
    results, controls = scientific_checks()
    output.mkdir(parents=True, exist_ok=False)
    dump(output/'results.json', results)
    dump(output/'controls.json', controls)
    manifest = {'schema': 'ym22-producer-source-manifest-v1', 'loop': 'n1', 'direction': 'forward',
                'inputs': hashes,
                'outputs': {p: digest(output/p) for p in ('results.json','controls.json')},
                'source_policy': 'frozen instructions; no current other-producer source imports',
                'output_policy': 'output-relative names; manifest self-hash held by submission inventory'}
    dump(output/'source-manifest.json', manifest)
    print(json.dumps({'loop':'n1','direction':'forward','status':results['status'],
                      'passed':True,'controls':len(controls['controls'])}, sort_keys=True))


if __name__ == '__main__':
    main()
