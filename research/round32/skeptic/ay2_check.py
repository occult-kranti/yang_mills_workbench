#!/usr/bin/env python3
"""Round32 AY2 skeptic pre-comparison checker (statement loop, zero-selected patterned family).

Written after the AY2 contract froze, from the frozen contract, the AY1 gate (both
hash-pinned), the AY1 contract (hash-pinned, only to compare the sentence
template), the I1 face table (hash-pinned) and the skeptic's own notes, without
opening or listing anything under research/round32/forward/ay2/ except the names
of its inputs/ snapshot. Nothing is imported from any producer or assistant. Standard library
only. Every admission Boolean is decided with fractions.Fraction; floats appear
only in the labelled 'previews' block. Every check and control raises an
explicit exception, so python -O cannot disable it. Model-agent skeptic with
correlated ancestry; not human peer review, not formal verification.

What is derived here:
  * the AY1 gate constants (D, 2D, K_2', 2K_2' tau^2, K_2^+) read as exact
    rationals and recomputed from the gate's own item formula;
  * the first-order density rho^(1)_R: the Gram matrix of {Omega_R, W_f Omega_R}
    over the 10 faces with owner set R by explicit SU(2) Haar integration
    (U=[[a,-b*],[b,a*]], uniform measure on S^3), the rank-two spectrum and
    the trace norm sqrt(10)|tau|/72; the 72 straddling faces vanish under the
    R-marginal by partial Haar integration;
  * the two-sided tier first_order_distance_from_product with sqrt(10) enclosed
    by directed rationals, its relative width against the preregistered 1/100
    (decided exactly by squaring), the +-tau separation;
  * an exact falsifying-scenario fixture: two gauge-invariant pure densities on
    H_R that satisfy every admitted R-local bound (D, K_2' remainder, AW1 Wilson
    enclosure) and differ by almost 2K_2' tau^2 (not asserted to be realized
    by the AQ Hamiltonian);
  * the constants available to the candidate routes (AM2, AQ1, AY1 reverse);
  * a statement-packet validator, the six-row obligations table and the 21
    contract controls as damaging mutations.

Usage: python3 -B research/round32/skeptic/ay2_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import product
from math import factorial, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / 'research/round32/contracts/ay2.json'
CONTRACT_SHA256 = '8e55e8e9d54b26520ab0fa10c1c6a967a616aabb4dc8c47988ff687d14d96b38'
AY1_GATE = ROOT / 'research/round32/advisor/ay1-gate.json'
AY1_GATE_SHA256 = 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5'
AY1_CONTRACT = ROOT / 'research/round32/contracts/ay1.json'
AY1_CONTRACT_SHA256 = 'be9b354420e66e7edba03d59b3d194b69f26782b44cfb63cb10e176bf4879ae0'
I1_REPORT = ROOT / 'research/round21/forward/i1/report.md'
I1_REPORT_SHA256 = '836a4c7d421f0ddf3589c159d2f057839421532c88157a054a61b51c25c781a9'

DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
R_COVER = ((0, 0, 0), (0, 0, 1))
MODEL_ID = 'AQ_patterned_zero_selected'
TOPOLOGY_STATES = 'trace norm on B(H_R)'
TOPOLOGY_DYNAMICS = 'norm on compact time windows'
CLOCK = 's=alpha*t_E/hbar, theta=alpha*t/hbar'
UNIFORM_IN = 'N (volume) at fixed spacing'
SUB_LABEL = 'uniform_local_closeness_not_uniqueness'
TIER_LABEL = 'first_order_distance_from_product'
FIVE = ('uniqueness_claimed', 'whole_sequence_claimed', 'rate_claimed', 'translation_invariance_claimed',
        'boundary_independence_of_dynamics_claimed')
OBLIGATION_IDS = ('uniqueness', 'whole_sequence_convergence', 'translation_invariance', 'rate_in_N',
                  'boundary_independence_of_dynamics', 'padded_family_dynamics')
FORBIDDEN_PHRASES = ('the aq state', 'the thermodynamic limit', 'the limit state', 'converges as n',
                     'uniform in a', 'boundary independent state', 'resolved interaction shift')
TIER_SENTENCE = ('For every chosen subsequential limit of either named family F1, F2 at |tau|<=10^-8 (either sign), '
                 'the reduced density on the fixed cover R satisfies sqrt(10)|tau|/72 - K_2\' tau^2 <= '
                 '||rho_R - P_R||_1 <= sqrt(10)|tau|/72 + K_2\' tau^2 (label first_order_distance_from_product); '
                 'this is a static property of the state on R, not an interaction-shift, Euclidean-node or '
                 'dynamical claim, and it does not identify the limit.')


class Rejected(Exception):
    """Raised by a validator that refuses a packet; controls require it."""


class CheckFailure(RuntimeError):
    """Raised when a required check or control fails."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise CheckFailure(cid)
    if any(row['id'] == cid for row in CHECKS):
        raise CheckFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def rejects(fn, reason):
    try:
        fn()
    except Rejected as exc:
        if reason not in str(exc):
            raise CheckFailure('rejected for the wrong reason: %s (expected %s)' % (exc, reason))
        return True
    return False


def accepts(fn):
    try:
        fn()
    except Rejected:
        return False
    return True


def control(cid, mutations, positives=(), **detail):
    rows = []
    for label, fn, reason in mutations:
        if not rejects(fn, reason):
            raise CheckFailure('control %s: mutation %s accepted' % (cid, label))
        rows.append({'mutation': label, 'rejected_for': reason})
    pos = []
    for label, fn in positives:
        if not accepts(fn):
            raise CheckFailure('control %s: positive %s rejected' % (cid, label))
        pos.append(label)
    need(True, cid, kind='control', mutations=rows, positives=pos, **detail)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def q(x):
    return str(x)


def preview(x):
    return format(float(x), '.12e')


def sqrt_bracket(n, scale):
    """Directed rational bracket lo <= sqrt(n) <= hi with hi-lo <= 1/scale."""
    r = isqrt(n * scale * scale)
    lo = F(r, scale)
    hi = lo if r * r == n * scale * scale else F(r + 1, scale)
    if not (lo * lo <= n <= hi * hi and hi - lo <= F(1, scale) and lo >= 0):
        raise CheckFailure('sqrt bracket')
    return lo, hi


def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def sub(a, b):
    return tuple(i - j for i, j in zip(a, b))


# ---------------------------------------------------------------- geometry (I1 dictionary)
def pi_map(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face(p, a, c):
    ea, ec = DIRS[a], DIRS[c]
    oriented = (((p, a), False), ((add(p, ea), c), False), ((add(p, ec), a), True), ((p, c), True))
    links = tuple(ln for ln, _ in oriented)
    return {'base': p, 'orient': a + c, 'oriented': oriented, 'links': links,
            'owners': frozenset(pi_map(ln[0]) for ln in links)}


def is_selected(p, a, c):
    return (a, c) == ('x', 'y') and p[0] % 4 in (0, 1, 2) and p[1] % 2 == 0


def anchored_faces(b):
    out = []
    for r, s in product(range(4), range(2)):
        p = (4 * b[0] + r, 2 * b[1] + s, b[2])
        for a, c in ORIENT:
            f = face(p, a, c)
            f.update({'anchor': b, 'r': r, 's': s, 'selected': is_selected(p, a, c)})
            out.append(f)
    return out


def omitted_faces(b):
    return [f for f in anchored_faces(b) if not f['selected']]


def parse_i1_table(text):
    rows = re.findall(r'^\| (xy|xz|yz): [^|]*\| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|$', text, re.M)
    out = {}
    names = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}
    for orient, cnt, supp, role in rows:
        sites = tuple(sorted(names[t.strip()] for t in supp.split(',')))
        key = (orient, sites, role == 'selected')
        out[key] = out.get(key, 0) + int(cnt)
    return out


def box(n):
    return list(product(range(-n, n + 1), repeat=3))


def l1(a, b):
    return sum(abs(i - j) for i, j in zip(a, b))


def linf(a, b):
    return max(abs(i - j) for i, j in zip(a, b))


# ---------------------------------------------------------------- exact SU(2) Haar integration
# U=[[a,-conj(b)],[b,conj(a)]], |a|^2+|b|^2=1; variables 0=a, 1=conj(a), 2=b, 3=conj(b).
ENTRY = {False: {(0, 0): (1, 0), (0, 1): (-1, 3), (1, 0): (1, 2), (1, 1): (1, 1)},
         True: {(0, 0): (1, 1), (0, 1): (1, 3), (1, 0): (-1, 2), (1, 1): (1, 0)}}


def trace_poly(oriented):
    """Tr of the ordered product of link matrices (dagger flag per link) as a polynomial."""
    n = len(oriented)
    poly = {}
    for idx in product((0, 1), repeat=n):
        sign = 1
        mono = {}
        for k, (ln, dag) in enumerate(oriented):
            s, var = ENTRY[dag][(idx[k], idx[(k + 1) % n])]
            sign *= s
            e = list(mono.get(ln, (0, 0, 0, 0)))
            e[var] += 1
            mono[ln] = tuple(e)
        key = tuple(sorted(mono.items()))
        poly[key] = poly.get(key, 0) + sign
    return {k: F(v) for k, v in poly.items() if v}


def poly_mul(p, qq):
    out = {}
    for k1, c1 in p.items():
        d1 = dict(k1)
        for k2, c2 in qq.items():
            d = dict(d1)
            for ln, e in k2:
                if ln in d:
                    o = d[ln]
                    d[ln] = (o[0] + e[0], o[1] + e[1], o[2] + e[2], o[3] + e[3])
                else:
                    d[ln] = e
            key = tuple(sorted(d.items()))
            out[key] = out.get(key, 0) + c1 * c2
    return {k: v for k, v in out.items() if v != 0}


def poly_add(p, qq, cq=1):
    out = dict(p)
    for k, v in qq.items():
        out[k] = out.get(k, 0) + cq * v
    return {k: v for k, v in out.items() if v != 0}


def link_moment(e):
    """E[a^e0 conj(a)^e1 b^e2 conj(b)^e3] for the uniform measure on S^3."""
    if e[0] != e[1] or e[2] != e[3]:
        return F(0)
    return F(factorial(e[0]) * factorial(e[2]), factorial(e[0] + e[2] + 1))


def integrate(p, links=None):
    out = {}
    for key, c in p.items():
        coef = F(c)
        rest = []
        for ln, e in key:
            if links is None or ln in links:
                m = link_moment(e)
                if m == 0:
                    coef = F(0)
                    break
                coef *= m
            else:
                rest.append((ln, e))
        if coef != 0:
            k = tuple(rest)
            out[k] = out.get(k, 0) + coef
    return {k: v for k, v in out.items() if v != 0}


def expect(factors):
    """Haar expectation of a product of polynomials, integrating out links progressively."""
    acc = {(): F(1)}
    for i, f in enumerate(factors):
        acc = poly_mul(acc, f)
        later = set()
        for g in factors[i + 1:]:
            for key in g:
                later.update(ln for ln, _ in key)
        present = {ln for key in acc for ln, _ in key}
        acc = integrate(acc, present - later)
    if any(k != () for k in acc):
        raise CheckFailure('expectation left free links')
    return acc.get((), F(0))


ONE = {(): F(1)}


# ---------------------------------------------------------------- small exact linear algebra
def mat_mul(a, b):
    n, m, p = len(a), len(b), len(b[0])
    return [[sum((a[i][k] * b[k][j] for k in range(m)), F(0)) for j in range(p)] for i in range(n)]


def mat_trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def mat_rank(a):
    m = [row[:] for row in a]
    rank = 0
    rows, cols = len(m), len(m[0])
    for c in range(cols):
        piv = next((r for r in range(rank, rows) if m[r][c] != 0), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        for r in range(rows):
            if r != rank and m[r][c] != 0:
                fac = m[r][c] / m[rank][c]
                m[r] = [x - fac * y for x, y in zip(m[r], m[rank])]
        rank += 1
    return rank


def charpoly(a):
    """Faddeev-LeVerrier: coefficients c_0..c_n of det(lambda I - A) = sum c_k lambda^(n-k)."""
    n = len(a)
    ident = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    coeffs = [F(1)]
    mk = [[F(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        am = mat_mul(a, mk) if k > 1 else [[F(0)] * n for _ in range(n)]
        mk = [[am[i][j] + coeffs[-1] * ident[i][j] for j in range(n)] for i in range(n)]
        ck = -mat_trace(mat_mul(a, mk)) / k
        coeffs.append(ck)
    return coeffs


def outer(u, v):
    return [[x * y for y in v] for x in u]


def mat_lin(*terms):
    n = len(terms[0][1])
    out = [[F(0)] * n for _ in range(n)]
    for c, m in terms:
        for i in range(n):
            for j in range(n):
                out[i][j] += c * m[i][j]
    return out


# ---------------------------------------------------------------- AY1 constants
def tier_ii(abs_tau):
    """The AY1 gate item formula: a=|tau|/144, J=28|tau|, T=49a/(1-352J), rho=352JT."""
    a = abs_tau / 144
    j = 28 * abs_tau
    t = 49 * a / (1 - 352 * j)
    rho = 352 * j * t
    eps_r = 82 * a + 2 * rho + (33 * a + rho) ** 2
    return {'a': a, 'J': j, 'T': t, 'rho': rho, 'eps_R': eps_r, 'eps_F': 2 * t + t * t}


def k2_prime_items(abs_tau, faces_meeting=82, straddling=72, single_contact=33, rho_factor=4):
    v = tier_ii(abs_tau)
    a, t, rho = v['a'], v['T'], v['rho']
    eps_r = faces_meeting * a + 2 * rho + (single_contact * a + rho) ** 2
    return {'am2_remainder': rho_factor * rho, 'straddling': 2 * t * (straddling * a + 2 * rho),
            'two_creation': 2 * (single_contact * a + rho) ** 2, 'density': 2 * eps_r ** 2,
            'normalization': 20 * a * eps_r ** 2}


def k2_prime(abs_tau, **kw):
    return sum(k2_prime_items(abs_tau, **kw).values(), F(0)) / abs_tau ** 2


def d_forward(eps):
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def k2_plus_formula(abs_tau):
    v = tier_ii(abs_tau)
    e = v['eps_F']
    return (v['rho'] + v['T'] * v['T'] + v['T'] ** 2 + e ** 2 + v['a'] * e ** 2) / abs_tau ** 2


def k2_w_rlocal(abs_tau):
    v = tier_ii(abs_tau)
    a, t, rho, e = v['a'], v['T'], v['rho'], v['eps_R']
    return (rho + t * (6 * a + rho) + (33 * a + rho) ** 2 + e ** 2 + a * e ** 2) / abs_tau ** 2


# ---------------------------------------------------------------- obligations (the skeptic's own table)
def reference_obligations():
    return [
        {'id': 'uniqueness',
         'statement_missing': 'all subsequential limits of F1 and F2 at the same tau coincide as states on the '
                              'quasi-local algebra (only closeness on R to 2D, and to 2K_2\' tau^2 after the common '
                              'first-order term, is proved)',
         'missing_premise': 'a non-perturbative bound on the influence of the box boundary on local marginals that '
                            'decays with the distance; every AY1 constant is uniform in N but does not decay',
         'candidate_route': 'HTW (Henheik-Teufel-Wessel LMP 112 (2022) Thm 7 = Yarotsky 2005 Thm 2) with evaluated '
                            'c_1, c_2, c_HTW(1,1) and 7|tau|<=c_HTW(1,1) at the cap; or complex-tau analyticity of '
                            'the AM2 fixed point uniformly in N plus order-by-order box locality (Vitali); or a '
                            'quasi-adiabatic local-perturbation bound with the AM2 gap; a Dobrushin-type condition '
                            'needs a Euclidean Gibbs representation that no premise supplies',
         'constants_needed': ['c_1', 'c_2', 'c_HTW(1,1)', 'complex-tau radius and uniform normalization bound',
                              'quasi-adiabatic filter constants', 'Dobrushin influence coefficients'],
         'constants_available': 'AM2: J_0=7/25000000, G(R)<148/7, G\'(R)<352, R=1/64, gap 1/2 (every volume, '
                                'every interaction family meeting the AM2 hypotheses); HTW/Yarotsky constants '
                                'unevaluated (AM2 gate); AQ1 Nachtergaele-Sims constants (polynomial F)',
         'status': 'unproved'},
        {'id': 'whole_sequence_convergence',
         'statement_missing': 'for each family the local densities converge along the whole sequence N -> infinity',
         'missing_premise': 'uniqueness of subsequential limits within the family (then trace-norm compactness gives '
                            'whole-sequence convergence) or a Cauchy estimate in N',
         'candidate_route': 'row uniqueness plus AQ1 local trace-norm compactness (sub-subsequence argument); or a '
                            'direct Cauchy estimate from any route of row uniqueness',
         'constants_needed': ['those of row uniqueness'],
         'constants_available': 'AQ1 reset budget and compactness (F1), AY1 F2 extraction; no N-dependent estimate',
         'status': 'unproved'},
        {'id': 'translation_invariance',
         'statement_missing': 'invariance under coarse translations b in Z^3 (fine translations are not symmetries of '
                              'the patterned model)',
         'missing_premise': 'uniqueness across box sequences (centered cubes and their coarse translates)',
         'candidate_route': 'coarse-translation covariance of the construction plus uniqueness for every exhausting '
                            'sequence; partial step: the AY1 argument on every translated cover R+b would give '
                            'closeness to 2K_2\' tau^2 of the translated marginals (not proved in any packet)',
         'constants_needed': ['those of row uniqueness, for arbitrary exhausting sequences'],
         'constants_available': 'coarse covariance by construction; AY1 constants for the fixed cover R only',
         'status': 'unproved'},
        {'id': 'rate_in_N',
         'statement_missing': 'an explicit bound on ||rho_{N,R}-rho_{M,R}||_1 decaying in N',
         'missing_premise': 'any N-dependent estimate',
         'candidate_route': 'HTW exp(c_1|Y|-c_2(N-O(1))); or the analyticity route (|tau|/r_0)^{c(N-1)}, with r_0 '
                            'at most the AM2 real-tau self-map radius 1/37888 if the AM2 estimates extend to complex '
                            'tau; or a quasi-adiabatic local-perturbation bound',
         'constants_needed': ['c_1', 'c_2', 'r_0', 'c'],
         'constants_available': 'none evaluated',
         'status': 'unproved'},
        {'id': 'boundary_independence_of_dynamics',
         'statement_missing': 'the limiting automorphism groups of F1 and F2 coincide on compact time windows '
                              '(algebraic dynamics); GNS-level generators additionally need state uniqueness',
         'missing_premise': 'a Duhamel comparison of the F1 and F2 finite-volume dynamics (they differ by 28N(5N+1) '
                            'faces at l_inf distance >= N-1 from R) with a Lieb-Robinson bound, and the F2 '
                            'Nachtergaele-Sims placement of row padded_family_dynamics',
         'candidate_route': 'Lieb-Robinson (Nachtergaele-Sims) with the AQ1 constants F(r)=(1+r)^-4, ||F||<=7, '
                            'C_F<=224, ||Phi||_F<=2268|tau| and the F2 constant ||Phi\'||_F<=1323|tau|; the '
                            'Duhamel difference is expected to be O(N^-2) on compact windows with the polynomial F '
                            '(not proved)',
         'constants_needed': ['||F||', 'C_F', '||Phi||_F', '||Phi\'||_F'],
         'constants_available': 'AQ1 Nachtergaele-Sims constants (HNM-AQ1.3); AY1 reverse ||Phi\'||_F<=1323|tau| '
                                '(named); the AM2 constants are not Lieb-Robinson constants',
         'status': 'unproved'},
        {'id': 'padded_family_dynamics',
         'statement_missing': 'F2 dynamics, stationarity of F2 limits, GNS continuity, nonnegative generator and the '
                              'AQ2 physical gap for F2 limits',
         'missing_premise': 'AQ1 sections 3-5 and AQ2 re-executed for F2 (owner-set interaction Phi\', padded sites '
                            'decoupled)',
         'candidate_route': 'repeat AQ1 sections 3-5 with Phi\' (support <=3, l1 diameter <=2, J\'=49|tau|/3, '
                            '||Phi\'||_F<=1323|tau|) and the AM2 gap for F2 boxes admitted in AY1',
         'constants_needed': ['||Phi\'||_F', 'C_F', 'AM2 gap for F2'],
         'constants_available': 'all available (AQ1 F, AY1 F2 premises); the proof is not written',
         'status': 'unproved'},
    ]


# ---------------------------------------------------------------- validators
def validate_obligations(rows):
    ids = [r.get('id') for r in rows]
    if len(ids) != len(set(ids)):
        raise Rejected('obligations table incomplete: duplicate row')
    if sorted(ids) != sorted(OBLIGATION_IDS) or len(rows) != 6:
        raise Rejected('obligations table incomplete: rows %s' % sorted(set(OBLIGATION_IDS) - set(ids)))
    for r in rows:
        for key in ('statement_missing', 'missing_premise', 'candidate_route'):
            if not isinstance(r.get(key), str) or len(r[key].strip()) < 20:
                raise Rejected('obligations table incomplete: %s of %s' % (key, r['id']))
        if not r.get('constants_needed'):
            raise Rejected('obligations table incomplete: constants_needed of %s' % r['id'])
        if r.get('status') != 'unproved':
            raise Rejected('obligations table incomplete: %s marked %s' % (r['id'], r.get('status')))
    dyn = [r for r in rows if r['id'] == 'boundary_independence_of_dynamics'][0]
    if 'AQ1' not in dyn['constants_available'] and 'AQ1' not in dyn['candidate_route']:
        raise Rejected('dynamics route: Lieb-Robinson constants are the AQ1 Nachtergaele-Sims constants')
    return True


def validate_evidence(ev, required):
    digest = sha_bytes(json.dumps(ev['rows'], sort_keys=True).encode())
    if digest != ev['digest']:
        raise Rejected('evidence digest mismatch')
    ids = {r['id']: r for r in ev['rows']}
    for cid in required:
        if cid not in ids:
            raise Rejected('missing required control ' + cid)
        if ids[cid].get('passed') is not True:
            raise Rejected('required control not passed ' + cid)
    return True


def sentences(text):
    return [s for s in re.split(r'(?<=[.;])\s+', text) if s.strip()]


def validate(pk, c):
    if pk['contract_sha256'] != CONTRACT_SHA256:
        raise Rejected('contract hash')
    if pk['ay1_gate_sha256'] != AY1_GATE_SHA256:
        raise Rejected('AY1 gate hash')
    if pk['model_id'] != MODEL_ID or pk['triple'] != ['0', '0', '0']:
        raise Rejected('changed model relabelled')
    if pk['tau'] != c['tau'] or pk['signs'] != ['+', '-']:
        raise Rejected('changed model relabelled')
    exact_fields = (pk['D'], pk['two_D'], pk['K2_prime'], pk['two_K2_prime_tau2'], pk['tau'], pk['tier']['lower'],
                    pk['tier']['upper'], pk['sqrt10_bracket'][0], pk['sqrt10_bracket'][1], pk['relative_width_upper'])
    if any(not isinstance(v, F) for v in exact_fields):
        raise Rejected('exact arithmetic')
    if pk['families'] != c['families']:
        raise Rejected('two families not named')
    if pk['cover'] != list(R_COVER) or pk['cover_links'] != 48 or pk['cover_endpoints'] != 36:
        raise Rejected('cover')
    if pk['stars_R'] != 7 or pk['faces_meeting_R'] != 82 or pk['straddling'] != 72:
        raise Rejected('incident stars')
    if pk['clock'] != CLOCK:
        raise Rejected('common clock')
    if not pk['same_coupling'] or pk['pm_tau']['compared_as_same_coupling']:
        raise Rejected('common clock: different couplings')
    if pk['topology_states'] != TOPOLOGY_STATES or pk['topology_dynamics'] != TOPOLOGY_DYNAMICS:
        raise Rejected('topology not named')
    amp = pk['rho1_amplitude_units']
    if amp['normalized'] != F(1, 72) or amp['alpha'] != F(1, 72) or pk['rho1_amplitude'] != F(1, 72):
        raise Rejected('clock or unit mixing')
    if pk['rho1_faces'] != 10:
        raise Rejected('first-order density: 10 faces with owner set R')
    if pk['rho1_trace_norm_sq_over_tau2'] != F(10, 5184):
        raise Rejected('first-order trace norm is sqrt(10)|tau|/72')
    if not pk['first_order_charged'] or pk['trace_W_over_tau'] != F(1, 144):
        raise Rejected('first-order term not charged')
    if pk['centering'] != 'none' or pk['tier']['reference'] != 'P_R':
        raise Rejected('centering: the tier is uncentered, reference P_R')
    if not pk['rho1_includes_tau']:
        raise Rejected('tau counted twice in the first-order term')
    sc = pk['scaling']
    if sc != {'first_order': 1, 'remainder': 2, 'pair_constant_2D': 1}:
        raise Rejected('tau scaling exponent')
    if pk['D'] != c['D'] or pk['two_D'] != 2 * c['D']:
        raise Rejected('D not the AY1 gate value')
    if pk['K2_prime_source'] != 'AY1 gate accepted: single-state remainder':
        raise Rejected('tier mixing: remainder constant not the AY1 single-state K_2\'')
    if pk['K2_prime'] == c['K2_plus']:
        raise Rejected('tier mixing: K_2^+ used as the trace-norm remainder')
    if pk['K2_prime'] != c['K2_prime']:
        if pk['K2_prime'] < c['K2_prime']:
            raise Rejected('K2 prime below the AY1 gate value')
        raise Rejected('tier mixing: K_2\' not the AY1 gate value')
    if pk['two_K2_prime_tau2'] != 2 * pk['K2_prime'] * pk['tau'] ** 2:
        raise Rejected('root-N or non-linear combination')
    if pk['tier']['combine'] != 'triangle':
        raise Rejected('root-N or non-linear combination')
    if pk['tier']['remainder'] != pk['K2_prime'] * pk['tau'] ** 2:
        if pk['tier']['remainder'] == pk['two_K2_prime_tau2']:
            raise Rejected('pair constant used as single-state remainder')
        raise Rejected('tier remainder not K_2\' tau^2')
    if pk['K2_prime_topology'] != 'trace_norm' or pk['K2_prime_vs_K2_plus'] != 'larger':
        raise Rejected('K2 prime versus K2 plus misstated')
    if pk['K2_plus_scope'] != 'single observable W, uniform in N':
        raise Rejected('K2 prime versus K2 plus misstated: K_2^+ is volume-uniform and W-specific')
    if pk['variants_in_tier']:
        raise Rejected('tier mixing: labelled variant in the tier')
    lo, hi = pk['sqrt10_bracket']
    if not (lo * lo <= 10 <= hi * hi):
        raise Rejected('sqrt(10) enclosure not directed')
    at = abs(pk['tau'])
    t_lo, t_hi = pk['tier']['lower'], pk['tier']['upper']
    first_sq = 10 * at * at / 5184
    if not (t_lo + pk['tier']['remainder'] >= 0 and (t_lo + pk['tier']['remainder']) ** 2 <= first_sq):
        raise Rejected('sqrt(10) enclosure not directed: lower end is not a lower bound')
    if not (t_hi - pk['tier']['remainder'] >= 0 and (t_hi - pk['tier']['remainder']) ** 2 >= first_sq):
        raise Rejected('sqrt(10) enclosure not directed: upper end is not an upper bound')
    if t_hi - t_lo - 2 * pk['tier']['remainder'] > F(1, 10 ** 30):
        raise Rejected('tier not tight to its formula')
    if pk['tier']['label'] != TIER_LABEL:
        raise Rejected('tier label: static, not dynamic')
    if pk['tier']['static'] is not True or pk['tier']['kind'] != 'static property of the state on R':
        raise Rejected('tier label: static, not dynamic')
    for key in ('resolved_interaction_shift', 'euclidean_node_certified', 'dynamical_claim'):
        if pk['claims'].get(key) is not False:
            raise Rejected('tier label: static, not dynamic (%s)' % key)
    if pk['relative_width_upper'] != 144 * pk['K2_prime'] * at / lo:
        raise Rejected('relative width not directed')
    if pk['boundary_comparison_content'] != 'matching first-order term':
        raise Rejected('2D alone is not a boundary comparison')
    if pk['falsifying_scenario']['excludable_by_present_bounds'] is not False or \
            pk['falsifying_scenario']['second_order_difference'] != pk['two_K2_prime_tau2']:
        raise Rejected('falsifying scenario')
    if pk['uniform_in'] != UNIFORM_IN or pk['claims'].get('uniform_in_a_claim') is not False:
        raise Rejected('not uniform in a')
    if pk['sub_label'] != SUB_LABEL:
        raise Rejected('local closeness is not uniqueness')
    gf = pk['gate_fields']
    for key in FIVE + ('rate_in_N_claimed',):
        if key not in gf:
            raise Rejected('gate field missing: ' + key)
        if gf[key] is not False:
            if key == 'uniqueness_claimed':
                raise Rejected('local closeness is not uniqueness')
            if key == 'whole_sequence_claimed':
                raise Rejected('subsequence versus whole sequence')
            raise Rejected('gate field claimed: ' + key)
    for key in ('states_compared', 'region', 'topology', 'closeness_order'):
        if key not in gf:
            raise Rejected('gate field missing: ' + key)
    if pk['sentence'] != c['sentence']:
        raise Rejected('mandatory sentence template')
    for text in pk['statements']:
        for sent in sentences(text):
            low = sent.lower()
            for bad in FORBIDDEN_PHRASES:
                if bad in low:
                    raise Rejected('forbidden phrasing: ' + bad)
            if re.search(r'\bunique', low) and not re.search(r'\bnot\b|\bno\b|\bnever\b', low):
                raise Rejected('forbidden phrasing: unique without not')
            if 'a chosen subsequential' not in low and 'subsequential limit' in low and 'every' not in low:
                raise Rejected('forbidden phrasing: a chosen subsequential')
    for key in ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified'):
        if pk['claims'].get(key) is not False:
            raise Rejected('forbidden claim ' + key)
    validate_obligations(pk['obligations'])
    need_verdict = 'accepted_within_scope' if (pk['tier_certified'] and pk['constants_exact']) else 'limited'
    if pk['verdict'] != need_verdict:
        raise Rejected('insufficient verdict retained: verdict must be ' + need_verdict)
    if pk['retained'] != c['retained']:
        raise Rejected('insufficient verdict retained: AY1 retained tier relabelled')
    return True


# ---------------------------------------------------------------- execute
def execute():
    contract_bytes = CONTRACT.read_bytes()
    c_sha = sha_bytes(contract_bytes)
    need(c_sha == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=c_sha)
    gate_bytes = AY1_GATE.read_bytes()
    g_sha = sha_bytes(gate_bytes)
    need(g_sha == AY1_GATE_SHA256, 'ay1_gate_sha256_pinned', sha256=g_sha)
    ay1c_bytes = AY1_CONTRACT.read_bytes()
    need(sha_bytes(ay1c_bytes) == AY1_CONTRACT_SHA256, 'ay1_contract_sha256_pinned')
    i1_bytes = I1_REPORT.read_bytes()
    need(sha_bytes(i1_bytes) == I1_REPORT_SHA256, 'i1_report_sha256_pinned')
    con = json.loads(contract_bytes)
    gate = json.loads(gate_bytes)
    ay1c = json.loads(ay1c_bytes)
    pre = con['preregistration']

    # 0. the frozen contract, read
    tau = F(pre['tau']['value'])
    target = F(pre['target']['value'])
    need(con['id'] == 'AY2' and con['status'] == 'frozen_before_production' and tau == F(1, 10 ** 8)
         and target == F(1, 100) and pre['target']['comparator'] == '<=' and pre['model_id'] == MODEL_ID
         and pre['selected_triple_alpha_units'] == ['0', '0', '0'] and pre['tau']['signs_evaluated'] == ['+', '-']
         and pre['tau']['is_model_change_vs_previous_loop'] is False, 'contract_target_cap_model_read',
         tau=q(tau), target=q(target))
    need(con['producers'] == ['forward'] and con['direction'] == 'statement+skeptic'
         and con['single_direction_independent_replay'] is True and con['reverse_premise_isolation'] is False,
         'contract_single_direction_statement_loop')
    need(con['controls'] == pre['controls_required']['ids'] and len(con['controls']) == 21
         and len(set(con['controls'])) == 21 and 'lower_bound_is_static_not_dynamic' in con['controls']
         and 'obligations_table_complete' in con['controls'], 'contract_control_mirror', controls=21, mirror=21)
    gate_fields_req = dict(pre['gate_fields_required'])
    need(sorted(gate_fields_req) == sorted(FIVE) and all(v is False for v in gate_fields_req.values())
         and all(k in con['required'][5] for k in FIVE + ('rate_in_N_claimed', 'states_compared', 'region',
                                                          'topology', 'closeness_order')),
         'contract_gate_fields', required_false=sorted(FIVE),
         item6_extra=['rate_in_N_claimed', 'states_compared', 'region', 'topology', 'closeness_order'])
    inventory = sorted(['AGENTS.md', 'research/round32/contracts/ay2.json'] + list(con['shared_premises']))
    need(len(con['shared_premises']) == 21 and len(set(inventory)) == 23
         and 'research/round32/advisor/ay1-gate.json' in inventory
         and 'research/round32/contracts/ay1.json' not in inventory
         and 'research/round32/advisor/aw1-gate.json' not in inventory
         and 'research/round32/advisor/av1-gate.json' not in inventory, 'contract_inventory_23_derivable',
         inventory=len(inventory), not_snapshotted=['contracts/ay1.json', 'advisor/av1-gate.json',
                                                    'advisor/aw1-gate.json'])
    need(con['selected_after'] == '<preceding gate>', 'contract_selected_after_placeholder_unfilled',
         finding='non-blocking: every earlier frozen Round32 contract names its preceding gate')
    need('mandatory_sentence_template' not in pre, 'contract_template_not_in_preregistration',
         finding='item 1 template recovered verbatim from the AY1 gate accepted text')
    obl_text = con['required'][1]
    need(all(s in obl_text for s in ('uniqueness', 'whole-sequence', 'translation invariance', 'rate in N',
                                     'boundary independence of dynamics', 'dynamics of the padded family'))
         and 'AM2 constants' in obl_text, 'contract_obligations_six_rows_named',
         reading='the Lieb-Robinson constants are the AQ1 Nachtergaele-Sims constants, not AM2')
    need('within 2D of the product' in con['required'][2] and '8.7e-10' in con['required'][2],
         'contract_item3_wording_read', reading='each limit lies within D of P_R (hence within 2D of each other)')
    need("single state versus product" in pre['error_terms_itemized'][1], 'contract_error_term_wording_read',
         reading='K_2\' tau^2 bounds the single state versus P_R + rho^(1)_R, not versus the product')

    # 1. the AY1 gate, read as exact rationals
    acc, dec = gate['accepted'], gate['decision']

    def grab(pat, s):
        m = re.search(pat, s)
        if m is None:
            raise CheckFailure('gate pattern ' + pat)
        return F(m.group(1))

    d_g = grab(r'; D=(\d+/\d+)', acc)
    two_d_g = grab(r'2D=(\d+/\d+)', acc)
    k2_g = grab(r"K_2'=(\d+/\d+)", acc)
    two_k2_g = grab(r"2K_2' tau\^2=(\d+/\d+)", acc)
    k2p_g = grab(r'K_2\^\+=(\d+/\d+)', acc)
    need(gate['verdict'] == 'accepted_within_scope' and gate['sub_label'] == SUB_LABEL
         and all(gate['gate_fields'][k] is False for k in FIVE + ('rate_in_N_claimed',))
         and gate['gate_fields']['closeness_order'] == [1, 2], 'ay1_gate_verdict_and_fields')
    need(two_d_g == 2 * d_g and two_d_g == grab(r'2D = (\d+/\d+)', dec) and k2_g == grab(r"K_2' = (\d+/\d+)", dec)
         and two_k2_g == 2 * k2_g * tau ** 2, 'ay1_gate_constants_consistent', D=q(d_g), two_D=q(two_d_g),
         K2_prime=q(k2_g), two_K2_prime_tau2=q(two_k2_g), K2_plus=q(k2p_g))
    single = "for every subsequential limit of either family ||rho_R-P_R-rho^(1)_R||_1<=K_2' tau^2"
    need(single in acc and single not in dec and "||rho_R-rho'_R-0||_1 <= 2K_2' tau^2" in dec,
         'ay1_single_state_remainder_is_in_accepted',
         item='AY1 gate accepted, items (2)-(3): for every subsequential limit of either family '
              '||rho_R-P_R-rho^(1)_R||_1<=K_2\' tau^2; the decision item (4) binds only the pair form '
              '(printed with a typographical -0)')
    for s in ("items 4rho+2T(72a+2rho)+2(33a+rho)^2+2eps_R^2+20a eps_R^2", 'a=|tau|/144', 'T=(49a)/(1-352J)',
              'rho=352JT', 'eps_R=82a+2rho+(33a+rho)^2', 'J<=28|tau|=J_0=7/25000000',
              '||rho^(1)_R||_1=sqrt(10)|tau|/72', 'Tr(rho^(1)_R W)=+tau/144'):
        if s not in acc:
            raise CheckFailure('gate string ' + s)
    need(True, 'ay1_gate_item_formula_present')
    template = ay1c['preregistration']['mandatory_sentence_template']
    need(template in acc, 'mandatory_template_recovered_from_ay1_gate', sentence=template)
    need(any('labelled observation only' in lim and '[4.3786e-10, 4.4055e-10]' in lim for lim in gate['limitations']),
         'ay1_tier_recorded_as_observation_only')

    # 2. recompute the gate constants from the gate's own formula
    v = tier_ii(tau)
    items = k2_prime_items(tau)
    k2 = sum(items.values(), F(0)) / tau ** 2
    need(k2 == k2_g, 'K2_prime_recomputed_from_gate_items', items_over_tau2={k: q(x / tau ** 2) for k, x in items.items()})
    need(d_forward(v['eps_F']) == d_g, 'D_recomputed_tier_ii', T=q(v['T']), rho=q(v['rho']))
    need(k2_plus_formula(tau) == k2p_g, 'K2_plus_recomputed')
    ratio_k = k2_g / k2p_g
    need(F(39994, 10000) < ratio_k < F(39996, 10000) and 2 * v['rho'] / tau ** 2 > k2p_g
         and 4 * v['rho'] / tau ** 2 > k2p_g, 'K2_prime_exceeds_K2_plus_with_floor',
         ratio=q(ratio_k), floor_2rho=q(2 * v['rho'] / tau ** 2))
    kw = k2_w_rlocal(tau)
    s2_lo, s2_hi = sqrt_bracket(2, 10 ** 40)
    k2_s2 = (2 * s2_hi * v['rho'] + items['straddling'] + items['two_creation'] + items['density']
             + items['normalization']) / tau ** 2
    need(kw < k2p_g < k2_s2 < k2_g and F(3, 10) < k2p_g - kw < F(1, 3), 'K2_variants_ordered',
         W_projected=q(kw), sqrt2_variant_upper=q(k2_s2))
    mono = [k2_prime(tau / m) for m in (1, 10, 100, 1000)]
    need(all(mono[i + 1] <= mono[i] for i in range(3)), 'K2_prime_monotone_cap_bounds_smaller_tau')
    t_i = 28 * tau * F(148, 7)
    d_i = d_forward(2 * t_i + t_i * t_i)
    need(2 * d_i > F(1, 1250000) and 2 * d_g <= F(1, 1250000), 'ay1_retained_tier_i_still_fails',
         two_D_i=q(2 * d_i))

    # 3. geometry: cover, 7 anchors, 82 faces meeting R, 10 inside, 72 straddling
    classes = {}
    for f in anchored_faces((0, 0, 0)):
        key = (f['orient'], tuple(sorted(f['owners'])), f['selected'])
        classes[key] = classes.get(key, 0) + 1
    need(classes == parse_i1_table(i1_bytes.decode()) and sum(classes.values()) == 24, 'face_classes_match_I1')
    rset = set(R_COVER)
    anchors = sorted({sub(r, s) for r in R_COVER for s in S_STAR})
    meet = [f for b in anchors for f in omitted_faces(b) if f['owners'] & rset]
    inside = [f for f in meet if f['owners'] <= rset]
    stradd = [f for f in meet if not f['owners'] <= rset]
    r_links = set()
    endpoints = set()
    for b in R_COVER:
        for rr, ss in product(range(4), range(2)):
            p = (4 * b[0] + rr, 2 * b[1] + ss, b[2])
            for d in 'xyz':
                r_links.add((p, d))
                endpoints.update({p, add(p, DIRS[d])})
    need(len(anchors) == 7 and len(meet) == 82 and len(inside) == 10 and len(stradd) == 72
         and len(r_links) == 48 and len(endpoints) == 36
         and all(f['anchor'] == (0, 0, 0) and all(ln in r_links for ln in f['links']) for f in inside),
         'cover_and_face_counts', anchors=7, meeting=82, inside=10, straddling=72, links=48, endpoints=36)
    xz = sorted((f['r'], f['s']) for f in inside if f['orient'] == 'xz')
    yz = sorted((f['r'], f['s']) for f in inside if f['orient'] == 'yz')
    need(xz == [(r, s) for r in range(3) for s in range(2)] and yz == [(r, 0) for r in range(4)],
         'rho1_faces_are_xz_r_le_2_and_yz_s_0')
    inside = sorted(inside, key=lambda f: (f['orient'], f['base']))
    w_face = [f for f in inside if f['orient'] == 'xz' and f['base'] == (0, 0, 0)][0]

    # 4. exact Haar integration: moment formula, Gram matrix, R-marginal of straddling faces
    sums = []
    for k in range(1, 5):
        # (|a|^2+|b|^2)^k integrates to 1
        tot = F(0)
        for i in range(k + 1):
            tot += F(factorial(k), factorial(i) * factorial(k - i)) * link_moment((i, i, k - i, k - i))
        sums.append(tot)
    need(sums == [1, 1, 1, 1], 'haar_moment_formula_normalized', k=[1, 2, 3, 4])
    tr = {id(f): trace_poly(f['oriented']) for f in meet}
    single_link = trace_poly((((('L',), 'x'), False),))
    wmom = [expect([single_link] * n) / 2 ** n for n in range(9)]
    need(wmom == [1, 0, F(1, 4), 0, F(1, 8), 0, F(5, 64), 0, F(7, 128)], 'haar_moments_of_W',
         moments=[q(x) for x in wmom])
    gram = [[F(0)] * 11 for _ in range(11)]
    basis = [ONE] + [tr[id(f)] for f in inside]  # Omega_R and e_f = 2 W_f Omega_R = Tr(U_f)
    for i in range(11):
        for j in range(i, 11):
            val = expect([basis[i], basis[j]])
            gram[i][j] = gram[j][i] = val
    ident = [[F(int(i == j)) for j in range(11)] for i in range(11)]
    need(gram == ident, 'gram_Omega_and_2WfOmega_orthonormal', pairs=66,
         method='explicit polynomial Haar integration over every link of the 10 faces')
    vanished = 0
    for f in stradd:
        outside = {ln for ln in f['links'] if pi_map(ln[0]) not in rset}
        if not outside:
            raise CheckFailure('straddling face without an outside-owned link')
        if integrate(tr[id(f)], outside) != {}:
            raise CheckFailure('straddling face survives the R-marginal')
        vanished += 1
    need(vanished == 72 and all(integrate(tr[id(f)], set()) != {} for f in inside),
         'straddling_faces_vanish_under_R_marginal', vanished=72, method='partial Haar integration of the '
                                                                      'outside-owned links')

    # 5. rho^(1)_R: rank-two spectrum and trace norm
    m1 = [[F(0)] * 11 for _ in range(11)]
    for k in range(1, 11):
        m1[0][k] = m1[k][0] = F(1, 144)   # (tau/72) W_f Omega = (tau/144) e_f, per unit tau
    m2 = mat_mul(m1, m1)
    m3 = mat_mul(m2, m1)
    cst = F(10, 20736)
    cp = charpoly(m1)
    need(all(m1[i][j] == m1[j][i] for i in range(11) for j in range(11)) and mat_trace(m1) == 0
         and mat_trace(m2) == 2 * cst and m3 == [[cst * x for x in row] for row in m1] and mat_rank(m1) == 2
         and cp == [F(1), F(0), -cst] + [F(0)] * 9, 'rho1_rank_two_spectrum',
         charpoly='lambda^9 (lambda^2 - 10/20736)', eigenvalues='+-sqrt(10)/144 per unit |tau|, 0 nine-fold',
         trace_norm='2 sqrt(10)/144 = sqrt(10)/72 per unit |tau|')
    x_norm_sq = sum((m1[0][k] ** 2 for k in range(1, 11)), F(0))
    need(x_norm_sq == cst and (2 * 1) ** 2 * x_norm_sq == F(10, 5184) and 10 * 2 * F(1, 72) * F(1, 2) == F(5, 36),
         'rho1_trace_norm_sqrt10_over_72', trace_norm_sq_over_tau2='10/5184', triangle_bound='5|tau|/36',
         note='the ten rank-one pieces have trace norm |tau|/72 each (||W_f Omega||=1/2); orthogonality turns '
              'their sum 10|tau|/72 into sqrt(10)|tau|/72')
    wpoly = {k: val / 2 for k, val in tr[id(w_face)].items()}
    tr_w = sum((2 * m1[0][k] * expect([basis[k], wpoly]) for k in range(1, 11)), F(0))
    tr_w2 = sum((2 * m1[0][k] * expect([basis[k], wpoly, wpoly]) for k in range(1, 11)), F(0))
    need(tr_w == F(1, 144) and tr_w2 == 0, 'rho1_wilson_readouts', trace_rho1_W_over_tau='+1/144',
         trace_rho1_W2=0)

    # 6. the two-sided tier with sqrt(10) enclosed by directed rationals
    at = abs(tau)
    s10_lo, s10_hi = sqrt_bracket(10, 10 ** 40)
    rem = k2_g * tau ** 2
    first_lo, first_hi = s10_lo * at / 72, s10_hi * at / 72
    lower, upper = first_lo - rem, first_hi + rem
    first_sq = 10 * at * at / 5184
    need(lower > 0 and (lower + rem) ** 2 <= first_sq <= (upper - rem) ** 2 and upper < d_g
         and upper - lower - 2 * rem <= F(1, 10 ** 47), 'tier_first_order_distance_from_product',
         lower=q(lower), upper=q(upper), sqrt10_bracket=[q(s10_lo), q(s10_hi)], remainder=q(rem),
         label=TIER_LABEL)
    need(F(43786, 10 ** 14) <= lower and upper <= F(44055, 10 ** 14), 'tier_inside_ay1_recorded_observation',
         ay1_observation='[4.3786e-10, 4.4055e-10]')
    need(lower > 0 and (72 * k2_g * at) ** 2 < 10, 'lower_bound_positive_not_haar_product',
         first_over_remainder_squared=q(10 / (72 * k2_g * at) ** 2),
         note='sqrt(10)|tau|/72 > K_2\' tau^2 iff (72 K_2\' |tau|)^2 < 10: no subsequential limit of either family '
              'has the Haar product as its R-marginal')
    # relative width 2K_2' tau^2 / (sqrt(10)|tau|/72) = 144 K_2' |tau| / sqrt(10), decided by squaring
    rw_lo, rw_hi = 144 * k2_g * at / s10_hi, 144 * k2_g * at / s10_lo
    exact_boolean = (14400 * k2_g * at) ** 2 <= 10
    need(exact_boolean and rw_hi <= target and (upper - lower) * 2 / (upper + lower) <= target,
         'relative_width_meets_target', relative_width_bracket=[q(rw_lo), q(rw_hi)],
         bracket_free_boolean='(14400 K_2\' |tau|)^2 <= 10', squared_lhs=q((14400 * k2_g * at) ** 2),
         margin_lower=q(target / rw_hi))
    k_thr_lo, k_thr_hi = s10_lo / (14400 * at), s10_hi / (14400 * at)
    two_sided_misread = 2 * 144 * k2_g * at / s10_lo
    need(k_thr_lo > k2_s2 and k_thr_lo > k2_g and 144 * k2p_g * at / s10_lo <= target and two_sided_misread > target,
         'target_discrimination', failing_K2_threshold=[q(k_thr_lo), q(k_thr_hi)],
         passes_with=['K_2\'', 'K_2^+', 'sqrt-2 variant'], fails_with=['pair constant as half-width'],
         note='the target is met by construction and cannot separate K_2\' from K_2^+ or the labelled variants')
    lo100 = s10_lo * (at / 100) / 72 - k2_prime(at / 100) * (at / 100) ** 2
    need(F(99) <= lower / lo100 * 1 <= F(101) and F(9900) <= rem / (k2_prime(at / 100) * (at / 100) ** 2) <= F(10100),
         'tier_scaling_exponents', first_order_exponent=1, remainder_exponent=2)
    sep_lo = 2 * first_lo - 2 * rem
    need(sep_lo > F(87, 10 ** 11) and upper <= d_g and sep_lo < 2 * d_g, 'plus_minus_tau_separation',
         separation_lower=q(sep_lo), each_within='D of P_R (upper tier end below D)',
         note='the +-tau limits are at different couplings: a common-clock control, not a boundary comparison')

    # 7. falsifying scenario: an exact 12-dimensional fixture on H_R
    f1 = [f for f in inside if f['orient'] == 'yz' and f['base'] == (1, 0, 0)][0]
    tr1 = tr[id(f1)]
    vpoly = poly_add(poly_mul(tr1, tr1), ONE, -1)            # chi_1(U_f1) = Tr(U_f1)^2 - 1
    full = basis + [vpoly]
    g12 = [[F(0)] * 12 for _ in range(12)]
    wm = [[F(0)] * 12 for _ in range(12)]
    for i in range(12):
        for j in range(i, 12):
            g12[i][j] = g12[j][i] = expect([full[i], full[j]])
            wm[i][j] = wm[j][i] = expect([full[i], full[j], wpoly])
    id12 = [[F(int(i == j)) for j in range(12)] for i in range(12)]
    need(g12 == id12, 'scenario_basis_orthonormal', basis='Omega_R, 2W_f Omega_R (10), chi_1(U_f1) Omega_R',
         f1='yz face (1,0,0)')
    t = tau / 144
    kappa = (k2_g * tau ** 2 - 21 * t * t) / 2
    rows = {}
    for sgn in (1, -1):
        psi = [F(1)] + [t] * 10 + [sgn * kappa]
        n2 = sum((x * x for x in psi), F(0))
        rho = [[x * y / n2 for y in psi] for x in psi]
        omega_w = sum((psi[i] * wm[i][j] * psi[j] for i in range(12) for j in range(12)), F(0)) / n2
        rows[sgn] = (psi, n2, rho, omega_w)
    n2 = rows[1][1]
    rem_bound = ((10 * t * t + kappa ** 2) / n2) * (1 + 2 * s10_hi * t) + \
                (10 * t * t + 2 * kappa * (1 + 5 * t * t) + kappa ** 2) / n2
    dmat = [[rows[1][2][i][j] - rows[-1][2][i][j] for j in range(12)] for i in range(12)]
    test = [[F(0)] * 12 for _ in range(12)]
    test[0][11] = test[11][0] = F(1)
    t2 = mat_mul(test, test)
    diff_lo = sum((dmat[i][j] * test[j][i] for i in range(12) for j in range(12)), F(0))
    need(kappa > 0 and rows[1][1] == rows[-1][1] and rem_bound <= rem and first_hi + rem_bound <= d_g
         and all(abs(rows[s][3] - tau / 144) <= k2p_g * tau ** 2 for s in (1, -1))
         and mat_mul(t2, test) == test and diff_lo == 4 * kappa / n2 and diff_lo >= 2 * rem * (1 - F(1, 10 ** 6)),
         'falsifying_scenario_fixture', kappa=q(kappa), second_order_difference_lower=q(diff_lo),
         ratio_to_2K2tau2=q(diff_lo / (2 * rem)), omega_W_deviation=q(rows[1][3] - tau / 144),
         note='two gauge-invariant pure densities on H_R satisfy ||rho-P_R||_1<=D, ||rho-P_R-rho1||_1<=K_2\' tau^2 '
              'and |omega(W)-tau/144|<=K_2^+ tau^2, yet differ by more than (1-10^-6) 2K_2\' tau^2; not asserted '
              'to be realized by the AQ Hamiltonian')

    # 8. constants available to the candidate routes
    j0 = F(7, 25000000)
    need(j0 * F(148, 7) == F(37, 6250000) and 2 * j0 * 352 == F(77, 390625)
         and F(1, 64) / (28 * F(148, 7)) == F(1, 37888) and F(1, 2 * 28 * 352) == F(1, 19712)
         and tau * 37888 < F(1, 2500), 'route_constants_am2', J0=q(j0), self_map_radius_real_tau='1/37888',
         exclusion_radius_real_tau='1/19712', cap_over_radius=q(tau * 37888), gap='1/2 normalized')
    shells = {}
    for pt in product(range(-9, 10), repeat=3):
        d = sum(abs(x) for x in pt)
        if d <= 9:
            shells[d] = shells.get(d, 0) + 1
    need(all(shells[r] == 4 * r * r + 2 for r in range(1, 10)) and all(4 * r * r + 2 <= 6 * (r + 1) ** 2
                                                                        for r in range(1, 10)),
         'route_constants_aq1_F_norm', F='(1+r)^-4 on l1', F_norm='<= 1 + 6 sum_{m>=2} m^-2 <= 7', C_F='<= 224')
    diam_star = max(l1(x, y) for x in S_STAR for y in S_STAR)
    osets = {frozenset(f['owners']) for f in omitted_faces((0, 0, 0))}
    diam_owner = max(l1(x, y) for o in osets for x in o for y in o)
    per_site_owner = sum(1 for b in [sub((0, 0, 0), s) for s in S_STAR] for f in omitted_faces(b)
                         if (0, 0, 0) in f['owners'])
    phi_f = 81 * 28
    phi_p = 81 * F(per_site_owner, 3)
    need(diam_star == 2 and diam_owner <= 2 and per_site_owner == 49 and phi_f == 2268 and phi_p == 1323,
         'route_constants_lieb_robinson', Phi_F_over_tau=2268, Phi_prime_F_over_tau=q(phi_p),
         lr_exponent_F1=q(2 * phi_f * 224 * tau), lr_exponent_F2=q(2 * phi_p * 224 * tau),
         clock='per normalized u; theta=8u')
    extra = {}
    for n in (2, 3):
        sites = set(box(n))
        f1keys, f2 = set(), {}
        for b in sorted(sites):
            fs = omitted_faces(b)
            if all(add(b, s) in sites for s in S_STAR):
                f1keys.update((f['base'], f['orient']) for f in fs)
            for f in fs:
                if f['owners'] <= sites:
                    f2[(f['base'], f['orient'])] = f['owners']
        diff = set(f2) - f1keys
        dmin = min(min(linf(o, r) for o in f2[k] for r in R_COVER) for k in diff)
        if not (f1keys <= set(f2) and len(diff) == 28 * n * (5 * n + 1) and dmin == n - 1):
            raise CheckFailure('F2-F1 boundary shell')
        extra[n] = (len(diff), dmin)
    need(True, 'route_constants_boundary_shell', extra_faces={str(k): v[0] for k, v in extra.items()},
         formula='28N(5N+1) at l_inf distance N-1 from R')

    # 9. validator, obligations and the 21 contract controls
    families = ['F1: centered whole-star boxes Lambda_N (AQ1)',
                'F2: all-contained-face boxes with padding (I1 section 6), same Lambda_N']
    retained = {'two_D_i': q(2 * d_i), 'status': 'fails 1/1250000; retained (AY1)'}
    ctx = {'tau': tau, 'families': families, 'D': d_g, 'K2_prime': k2_g, 'K2_plus': k2p_g, 'sentence': template,
           'retained': retained}
    base = {
        'contract_sha256': CONTRACT_SHA256, 'ay1_gate_sha256': AY1_GATE_SHA256, 'model_id': MODEL_ID,
        'triple': ['0', '0', '0'], 'tau': tau, 'signs': ['+', '-'], 'families': list(families),
        'cover': list(R_COVER), 'cover_links': 48, 'cover_endpoints': 36, 'stars_R': 7, 'faces_meeting_R': 82,
        'straddling': 72, 'clock': CLOCK, 'same_coupling': True, 'topology_states': TOPOLOGY_STATES,
        'topology_dynamics': TOPOLOGY_DYNAMICS, 'rho1_faces': 10, 'rho1_amplitude': F(1, 72),
        'rho1_amplitude_units': {'normalized': F(1, 3) / 24, 'alpha': F(1, 24) / 3}, 'rho1_includes_tau': True,
        'rho1_trace_norm_sq_over_tau2': F(10, 5184), 'first_order_charged': True, 'trace_W_over_tau': F(1, 144),
        'centering': 'none', 'scaling': {'first_order': 1, 'remainder': 2, 'pair_constant_2D': 1},
        'D': d_g, 'two_D': 2 * d_g, 'K2_prime': k2_g, 'K2_prime_source': 'AY1 gate accepted: single-state remainder',
        'two_K2_prime_tau2': 2 * k2_g * tau ** 2, 'K2_prime_topology': 'trace_norm', 'K2_prime_vs_K2_plus': 'larger',
        'K2_plus_scope': 'single observable W, uniform in N', 'variants_in_tier': [],
        'sqrt10_bracket': [s10_lo, s10_hi],
        'tier': {'lower': lower, 'upper': upper, 'remainder': rem, 'combine': 'triangle', 'reference': 'P_R',
                 'label': TIER_LABEL, 'static': True, 'kind': 'static property of the state on R'},
        'relative_width_upper': rw_hi, 'boundary_comparison_content': 'matching first-order term',
        'falsifying_scenario': {'second_order_difference': 2 * k2_g * tau ** 2, 'excludable_by_present_bounds': False},
        'pm_tau': {'separation_lower': sep_lo, 'compared_as_same_coupling': False},
        'uniform_in': UNIFORM_IN, 'sub_label': SUB_LABEL, 'sentence': template,
        'gate_fields': {'uniqueness_claimed': False, 'whole_sequence_claimed': False, 'rate_claimed': False,
                        'rate_in_N_claimed': False, 'translation_invariance_claimed': False,
                        'boundary_independence_of_dynamics_claimed': False,
                        'states_compared': 'all subsequential limits of F1 and F2 (every pair, same tau)',
                        'region': 'R={0,e_z} fixed before production', 'topology': TOPOLOGY_STATES,
                        'closeness_order': [1, 2]},
        'statements': [template, TIER_SENTENCE,
                       'Each statement holds for a chosen subsequential limit of either family; uniqueness is not '
                       'claimed.'],
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                   'uniform_in_a_claim': False, 'resolved_interaction_shift': False, 'euclidean_node_certified': False,
                   'dynamical_claim': False},
        'obligations': reference_obligations(), 'tier_certified': True, 'constants_exact': True,
        'verdict': 'accepted_within_scope', 'retained': dict(retained),
    }
    need(validate(base, ctx), 'reference_packet_accepted')

    nested = ('claims', 'gate_fields', 'rho1_amplitude_units', 'scaling', 'tier', 'falsifying_scenario', 'pm_tau',
              'retained')

    def mut(**kw):
        pk = dict(base)
        for key in nested:
            pk[key] = dict(base[key])
        pk['obligations'] = [dict(r) for r in base['obligations']]
        for k, val in kw.items():
            if '.' in k:
                head, tail = k.split('.', 1)
                pk[head][tail] = val
            else:
                pk[k] = val
        return lambda: validate(pk, ctx)

    def drop_row(rid):
        return mut(obligations=[dict(r) for r in base['obligations'] if r['id'] != rid])

    def edit_row(rid, **kw):
        rows_ = [dict(r) for r in base['obligations']]
        for r in rows_:
            if r['id'] == rid:
                r.update(kw)
        return mut(obligations=rows_)

    ok = [('reference packet', lambda: validate(base, ctx))]
    k2_orthant = k2_prime(tau, faces_meeting=42, straddling=32)
    control('missing_incoming_stars',
            [('orthant two anchors', mut(stars_R=2, faces_meeting_R=42, straddling=32), 'incident stars'),
             ('K2 recomputed with orthant pins', mut(K2_prime=k2_orthant, two_K2_prime_tau2=2 * k2_orthant * tau ** 2,
                                                     **{'tier.remainder': k2_orthant * tau ** 2}), 'K2 prime below')],
            ok, K2_orthant_pins=q(k2_orthant))
    control('full_original_wilson_cover',
            [('R={0}', mut(cover=[(0, 0, 0)]), 'cover'), ('four drawn links', mut(cover_links=4), 'cover'),
             ('W alone as rho1', mut(rho1_faces=1, rho1_trace_norm_sq_over_tau2=F(1, 5184)), 'first-order density')],
            ok)
    control('wrong_delta_alpha_hbar_clock',
            [('u=s/8', mut(clock='u=s/8'), 'common clock'),
             ('amplitude tau/9', mut(**{'rho1_amplitude_units.normalized': F(1, 9)}), 'clock or unit mixing'),
             ('amplitude tau/576', mut(**{'rho1_amplitude_units.alpha': F(1, 576)}), 'clock or unit mixing')], ok)
    control('vector_versus_scalar_centering',
            [('vector centering', mut(centering='vector'), 'centering'),
             ('tier centred on P_R+rho1', mut(**{'tier.reference': 'P_R+rho1_R'}), 'centering')], ok)
    control('first_order_mean_charged',
            [('rho1 dropped', mut(first_order_charged=False), 'first-order term not charged'),
             ('Wilson readout zero', mut(trace_W_over_tau=F(0)), 'first-order term not charged'),
             ('triangle 5|tau|/36 as the first-order norm', mut(rho1_trace_norm_sq_over_tau2=F(25, 1296)),
              'first-order trace norm')], ok)
    control('tau_scaling_exponent',
            [('first order quadratic', mut(scaling={'first_order': 2, 'remainder': 2, 'pair_constant_2D': 1}),
              'tau scaling'),
             ('remainder linear', mut(scaling={'first_order': 1, 'remainder': 1, 'pair_constant_2D': 1}),
              'tau scaling')], ok)
    control('changed_model_relabelled',
            [('tau 1e-14', mut(tau=F(1, 10 ** 14)), 'changed model'),
             ('uniform triple', mut(triple=['tau/24', 'tau/24', 'tau/24']), 'changed model'),
             ('uniform model id', mut(model_id='AQ_uniform_routeB'), 'changed model'),
             ('one sign', mut(signs=['+']), 'changed model')], ok)
    control('insufficient_verdict_retained',
            [('tier uncertified but accepted', mut(tier_certified=False), 'insufficient verdict'),
             ('inexact constant but accepted', mut(constants_exact=False), 'insufficient verdict'),
             ('AY1 tier i relabelled as passing', mut(retained={'two_D_i': q(2 * d_i), 'status': 'passes'}),
              'insufficient verdict')], ok)
    control('exact_arithmetic_admission',
            [('float K2', mut(K2_prime=float(k2_g)), 'exact arithmetic'),
             ('float tier', mut(**{'tier.lower': float(lower)}), 'exact arithmetic'),
             ('float sqrt10', mut(sqrt10_bracket=[3.1622776601683795, s10_hi]), 'exact arithmetic')], ok)
    control('root_n_misuse',
            [('rss tier', mut(**{'tier.combine': 'root_sum_square'}), 'root-N'),
             ('sqrt2 pair constant', mut(two_K2_prime_tau2=k2_g * tau ** 2 * F(1414, 1000)), 'root-N')], ok)
    control('no_priority_or_continuum_claim',
            [('continuum', mut(**{'claims.continuum_claim': True}), 'forbidden claim continuum_claim'),
             ('weak coupling', mut(**{'claims.weak_coupling_claim': True}), 'forbidden claim weak_coupling_claim'),
             ('priority', mut(**{'claims.scientific_priority_verified': True}), 'forbidden claim scientific_priority')],
            ok)
    control('topology_named',
            [('weak-* states', mut(topology_states='weak-* on fixed observables'), 'topology'),
             ('one topology', mut(topology_dynamics=TOPOLOGY_STATES), 'topology')], ok)
    control('two_families_named',
            [('one family', mut(families=families[:1]), 'two families'),
             ('orthant substituted', mut(families=[families[0], 'orthant boxes']), 'two families')], ok)
    control('subsequence_versus_whole_sequence',
            [('whole sequence', mut(**{'gate_fields.whole_sequence_claimed': True}), 'subsequence'),
             ('the limit state', mut(statements=['The limit state lies in the tier.']), 'forbidden phrasing'),
             ('converges as N', mut(statements=['rho_R converges as N grows.']), 'forbidden phrasing')], ok)
    control('local_closeness_not_uniqueness',
            [('uniqueness', mut(**{'gate_fields.uniqueness_claimed': True}), 'not uniqueness'),
             ('sub-label', mut(sub_label='uniqueness'), 'not uniqueness'),
             ('the AQ state', mut(statements=['The AQ state is within the tier.']), 'forbidden phrasing'),
             ('unique without not', mut(statements=['The limit is unique on R.']), 'unique without not')], ok)
    control('common_clock',
            [('u clock', mut(clock='u=delta*t/hbar'), 'common clock'),
             ('+-tau as same coupling', mut(**{'pm_tau.compared_as_same_coupling': True}), 'different couplings'),
             ('different couplings', mut(same_coupling=False), 'different couplings')], ok)
    control('tier_mixing_rejected',
            [('K2+ in the tier', mut(K2_prime=k2p_g, two_K2_prime_tau2=2 * k2p_g * tau ** 2,
                                     **{'tier.remainder': k2p_g * tau ** 2}), 'K_2^+ used'),
             ('sqrt-2 variant in the tier', mut(variants_in_tier=['sqrt2_sectors']), 'labelled variant'),
             ('remainder from AW1', mut(K2_prime_source='AW1 gate K_2^+'), 'tier mixing'),
             ('larger K2 from a crude tier', mut(K2_prime=k2_g * 2, two_K2_prime_tau2=4 * k2_g * tau ** 2,
                                                  **{'tier.remainder': 2 * k2_g * tau ** 2}), 'tier mixing')], ok)
    control('not_uniform_in_a',
            [('uniform in a', mut(uniform_in='N and a'), 'not uniform in a'),
             ('flag', mut(**{'claims.uniform_in_a_claim': True}), 'not uniform in a'),
             ('phrase', mut(statements=['The tier is uniform in a.']), 'forbidden phrasing')], ok)
    control('lower_bound_is_static_not_dynamic',
            [('label interaction shift', mut(**{'tier.label': 'interaction_shift'}), 'static, not dynamic'),
             ('not static', mut(**{'tier.static': False}), 'static, not dynamic'),
             ('resolved shift', mut(**{'claims.resolved_interaction_shift': True}), 'static, not dynamic'),
             ('Euclidean node', mut(**{'claims.euclidean_node_certified': True}), 'static, not dynamic'),
             ('dynamical claim', mut(**{'claims.dynamical_claim': True}), 'static, not dynamic'),
             ('shift phrase', mut(statements=['The lower bound is a resolved interaction shift.']),
              'forbidden phrasing')], ok)
    control('obligations_table_complete',
            [('drop ' + rid, drop_row(rid), 'obligations table incomplete') for rid in OBLIGATION_IDS]
            + [('empty missing premise', edit_row('uniqueness', missing_premise=''), 'obligations table incomplete'),
               ('empty route', edit_row('rate_in_N', candidate_route=' '), 'obligations table incomplete'),
               ('row marked proved', edit_row('boundary_independence_of_dynamics', status='proved'),
                'obligations table incomplete'),
               ('duplicate row', mut(obligations=base['obligations'] + [dict(base['obligations'][0])]),
                'obligations table incomplete')], ok)
    # extra controls (not contract ids)
    control('pair_constant_not_single_state_remainder',
            [('2K2 tau^2 as half-width', mut(**{'tier.remainder': 2 * k2_g * tau ** 2}), 'pair constant used'),
             ('K2 tau^2/2 as half-width', mut(**{'tier.remainder': k2_g * tau ** 2 / 2}), 'not K_2\' tau^2')], ok)
    control('tau_not_counted_twice',
            [('tau-free rho1 times tau again', mut(rho1_includes_tau=False), 'tau counted twice')], ok)
    control('sqrt10_directed',
            [('lower end with sqrt10 upper', mut(**{'tier.lower': first_hi - rem}), 'not a lower bound'),
             ('upper end with sqrt10 lower', mut(**{'tier.upper': first_lo + rem}), 'not an upper bound'),
             ('swapped bracket', mut(sqrt10_bracket=[s10_hi + F(1, 10 ** 40), s10_hi]), 'not directed')], ok)
    control('two_D_not_a_boundary_comparison',
            [('2D as the comparison', mut(boundary_comparison_content='2D'), '2D alone')], ok)
    control('K2_prime_versus_K2_plus_statement',
            [('smaller', mut(K2_prime_vs_K2_plus='smaller'), 'misstated'),
             ('whole-box K2+', mut(K2_plus_scope='whole-box'), 'volume-uniform')], ok)
    control('falsifying_scenario_recorded',
            [('excludable', mut(**{'falsifying_scenario.excludable_by_present_bounds': True}), 'falsifying scenario'),
             ('2D as the scenario', mut(**{'falsifying_scenario.second_order_difference': 2 * d_g}),
              'falsifying scenario')], ok)
    control('mandatory_sentence_template',
            [('edited', mut(sentence=template.replace('does not assert', 'asserts')), 'mandatory sentence'),
             ('rate field missing', mut(gate_fields={k: val for k, val in base['gate_fields'].items()
                                                      if k != 'rate_in_N_claimed'}), 'gate field missing'),
             ('closeness_order missing', mut(gate_fields={k: val for k, val in base['gate_fields'].items()
                                                          if k != 'closeness_order'}), 'gate field missing')], ok)
    control('dynamics_route_constants_named',
            [('AM2 constants for Lieb-Robinson',
              edit_row('boundary_independence_of_dynamics', candidate_route='a Lieb-Robinson locality argument with '
                                                                              'the AM2 constants',
                       constants_available='AM2 J_0 and G'), 'AQ1 Nachtergaele-Sims')], ok)

    # coherent evidence tampering: executed last, on the evidence of every control above
    rows_ev = [dict(r) for r in CHECKS if r.get('kind') == 'control']
    required_now = [cid for cid in con['controls'] if cid != 'coherent_evidence_tampering']
    ev = {'rows': rows_ev, 'digest': sha_bytes(json.dumps(rows_ev, sort_keys=True).encode())}
    bad = [dict(r) for r in rows_ev]
    bad[[r['id'] for r in bad].index('obligations_table_complete')]['passed'] = False
    ev_bad = {'rows': bad, 'digest': sha_bytes(json.dumps(bad, sort_keys=True).encode())}
    few = [r for r in rows_ev if r['id'] != 'lower_bound_is_static_not_dynamic']
    ev_few = {'rows': few, 'digest': sha_bytes(json.dumps(few, sort_keys=True).encode())}
    ev_stale = {'rows': bad, 'digest': ev['digest']}
    need(validate_evidence(ev, required_now), 'synthetic_evidence_validates', rows=len(rows_ev),
         required=len(required_now))
    control('coherent_evidence_tampering',
            [('rehashed contract', mut(contract_sha256='0' * 64), 'contract hash'),
             ('rehashed AY1 gate', mut(ay1_gate_sha256='0' * 64), 'AY1 gate hash'),
             ('smaller K2 rebound', mut(K2_prime=k2_g - F(1, 10 ** 6), two_K2_prime_tau2=2 * (k2_g - F(1, 10 ** 6)) * tau ** 2,
                                        **{'tier.remainder': (k2_g - F(1, 10 ** 6)) * tau ** 2}), 'K2 prime below'),
             ('flipped obligations control, digest rebound', lambda: validate_evidence(ev_bad, required_now),
              'required control not passed'),
             ('dropped static-label control, digest rebound', lambda: validate_evidence(ev_few, required_now),
              'missing required control'),
             ('flipped control, stale digest', lambda: validate_evidence(ev_stale, required_now), 'digest mismatch')],
            ok, scope='synthetic evidence bundle of this checker; producer freeze and inventory checked at '
                      'post-comparison')

    ids = set(con['controls'])
    done = {row['id'] for row in CHECKS if row.get('kind') == 'control'}
    missing = sorted(ids - done)
    n_mut = sum(len(row['mutations']) for row in CHECKS if row.get('kind') == 'control')
    n_mut_contract = sum(len(row['mutations']) for row in CHECKS if row.get('kind') == 'control' and row['id'] in ids)
    need(not missing, 'contract_controls_covered', implemented=len(ids & done), of=len(ids), deferred=missing,
         rejected_mutations_total=n_mut, rejected_mutations_in_contract_controls=n_mut_contract)

    return {
        'loop': 'AY2', 'stage': 'pre_comparison', 'role': 'skeptic independent derivation (single-direction admission input)',
        'reviewer': 'skeptic (model agent, correlated ancestry); not human peer review, not formal verification',
        'human_author': 'Hruday N M (BUNZEEY)', 'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'ay1_gate_sha256': g_sha, 'checker_sha256': sha_bytes(Path(__file__).read_bytes()),
        'producer_files_read': [],
        'incidental_exposure': 'names of the 23 files under research/round32/forward/ay2/inputs/ listed with find and '
                               'hashed against their repository sources (all identical); git status runs after this '
                               'package was written showed the names (only) of untracked producer paths '
                               'research/round32/forward/ay2/check.py, report.md, freeze.json and output/; none was '
                               'opened, and nothing else under research/round32/forward/ay2/ was listed or opened',
        'model': MODEL_ID + ': SU(2) Kogut-Susskind form on Z^3 at fixed spacing, 24-link factors, selected triple '
                            '(0,0,0), Haar reference P_R, 21 omitted faces per anchor with -(tau/3)W_f; both signs '
                            '|tau|<=10^-8; cover R={0,e_z}; families F1 (AQ1 whole-star) and F2 (I1 section 6 '
                            'all-contained-face with padding) on centered cubes [-N,N]^3',
        'ay1_constants': {'D': q(d_g), 'two_D': q(two_d_g), 'K2_prime': q(k2_g), 'two_K2_prime_tau2': q(two_k2_g),
                          'K2_plus': q(k2p_g), 'K2_prime_over_K2_plus': q(ratio_k),
                          'single_state_remainder_source': 'AY1 gate accepted, items (2)-(3); proved in AY1 forward '
                                                           'HNM-AY1-F11/F14 and reverse sections 3.5-3.7',
                          'K2_W_projected_R_local_labelled': q(kw), 'K2_sqrt2_variant_upper_labelled': q(k2_s2),
                          'two_D_i_retained': q(2 * d_i)},
        'first_order_density': {
            'formula': 'rho1_R = (tau/72) sum_{f in F_R} (|W_f Omega_R><Omega_R| + h.c.) = |x><Omega_R| + h.c., '
                       'x = (tau/144) sum e_f, e_f = 2 W_f Omega_R orthonormal',
            'gram': 'identity on {Omega_R, e_f} (explicit Haar integration)', 'norm_x_sq_over_tau2': '10/20736',
            'charpoly_per_unit_tau': 'lambda^9 (lambda^2 - 10/20736)', 'trace_norm': 'sqrt(10)|tau|/72',
            'trace_norm_sq_at_cap': q(first_sq), 'triangle_bound_not_used': '5|tau|/36',
            'trace_W': '+tau/144', 'trace_W2': '0', 'straddling_faces_vanishing': 72},
        'tier': {'label': TIER_LABEL, 'lower': q(lower), 'upper': q(upper), 'centre': 'sqrt(10)|tau|/72',
                 'half_width': q(rem), 'sqrt10_bracket': [q(s10_lo), q(s10_hi)],
                 'relative_width_bracket': [q(rw_lo), q(rw_hi)], 'target': q(target), 'target_met': exact_boolean,
                 'failing_K2_threshold': [q(k_thr_lo), q(k_thr_hi)],
                 'scope': 'every subsequential limit of either family, both signs, every |tau|<=10^-8 with the cap K_2\'; '
                          'static property of the state on R'},
        'plus_minus_tau': {'separation_lower': q(sep_lo), 'formula': 'sqrt(10)|tau|/36 - 2K_2\' tau^2'},
        'falsifying_scenario': {'second_order_difference_bound': q(two_k2_g), 'fixture_difference_lower': q(diff_lo),
                                'kappa': q(kappa), 'fixture': 'psi_pm = Omega_R + x +- kappa chi_1(U_f1) Omega_R, '
                                                              'f1 = yz face (1,0,0)'},
        'route_constants': {'am2_self_map_radius_real_tau': '1/37888', 'am2_exclusion_radius_real_tau': '1/19712',
                            'aq1_F': '(1+r)^-4, ||F||<=7, C_F<=224', 'Phi_F_over_tau': '2268',
                            'Phi_prime_F_over_tau': q(phi_p), 'F2_minus_F1_faces': '28N(5N+1)',
                            'distance_from_R': 'N-1', 'htw_constants': 'unevaluated (AM2 gate limitation)'},
        'predictions': {
            'tier_lower_with_this_bracket': q(lower), 'tier_upper_with_this_bracket': q(upper),
            'tier_exact_form': 'sqrt(10)|tau|/72 -/+ K_2\' tau^2 with K_2\' the AY1 gate rational',
            'first_order_term_bracket': [q(first_lo), q(first_hi)], 'half_width': q(rem), 'width': q(2 * rem),
            'relative_width_bracket': [q(rw_lo), q(rw_hi)], 'relative_half_width_upper': q(rw_hi / 2),
            'plus_minus_separation_lower': q(sep_lo), 'second_order_difference': q(two_k2_g),
            'counts': {'anchors': 7, 'faces_meeting_R': 82, 'faces_owner_set_R': 10, 'straddling': 72},
            'K2_prime_over_K2_plus': q(ratio_k), 'failing_K2_threshold_lower': q(k_thr_lo)},
        'obligations': reference_obligations(),
        'gate_fields': dict(base['gate_fields']), 'sentence': template, 'tier_sentence': TIER_SENTENCE,
        'claims': dict(base['claims']),
        'deferred_controls': {},
        'deferred_parts': {
            'coherent_evidence_tampering': 'executed on a synthetic evidence bundle; the producer freeze and '
                                           'inventory are checked at post-comparison',
            'obligations_table_complete': 'executed on the skeptic reference table; the producer table is checked '
                                          'at post-comparison',
            'mandatory_sentence_template': 'phrase scan of the producer report at post-comparison'},
        'checks': CHECKS,
        'previews': {'D': preview(d_g), 'two_D': preview(two_d_g), 'K2_prime': preview(k2_g), 'K2_plus': preview(k2p_g),
                     'K2_prime_over_K2_plus': preview(ratio_k), 'first_order_term': preview(first_hi),
                     'tier_lower': preview(lower), 'tier_upper': preview(upper), 'half_width': preview(rem),
                     'width': preview(2 * rem), 'relative_width': preview(rw_hi), 'target_margin': preview(target / rw_hi),
                     'failing_K2_threshold': preview(k_thr_lo), 'first_over_remainder': preview(first_lo / rem),
                     'plus_minus_separation_lower': preview(sep_lo), 'fixture_difference': preview(diff_lo),
                     'fixture_ratio': preview(diff_lo / (2 * rem)), 'upper_over_D': preview(upper / d_g),
                     'lr_exponent_F1_per_u': preview(2 * phi_f * 224 * tau),
                     'lr_exponent_F2_per_u': preview(2 * phi_p * 224 * tau),
                     'cap_over_am2_radius': preview(tau * 37888),
                     'label': 'floating previews only; no admission Boolean reads them'},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    result = execute()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'tier': [result['previews']['tier_lower'],
                                                                result['previews']['tier_upper']],
                      'relative_width': result['previews']['relative_width']}))


if __name__ == '__main__':
    main()
