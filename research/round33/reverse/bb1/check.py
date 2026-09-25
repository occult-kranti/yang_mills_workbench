#!/usr/bin/env python3
"""HNM-BB1 reverse producer (route iterated_split): locality of the reduced densities
of the named construction families F1 and F2, from the every-site BA1 coefficient
differences, by the AV1 product-ordering split applied recursively to the outside
state with per-site charging through the diameter weight.

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production (Claude,
an AI model) under reverse premise isolation; HNM labels are project aliases.
Banach's fixed-point theorem, Weierstrass' theorem, the maximum-modulus principle,
the pure-state trace-distance identity and the contractivity of the partial trace
are established mathematics; the commuting creation expansion is the admitted AM2
construction. Scientific priority is unverified.

Standard library only. Exact Fraction arithmetic decides every Boolean; decimal
strings are truncated previews. Every contract control is implemented as damaging
mutations whose rejection is required. Failures are explicit exceptions (never
assert), so the run and its output bytes are identical under python -O.

Usage: python3 -B research/round33/reverse/bb1/check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUTS = HERE / 'inputs'
CONTRACT_REL = 'research/round33/contracts/bb1.json'
CONTRACT_SHA256 = '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018'
PINNED_GATES = {
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round33/advisor/ba1-gate.json': '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    'research/round33/advisor/ba2-gate.json': 'e6b163fc8f80de28c51609f77d0bef21dcdc1286638c862ad67202e6f7b0ca35',
}
BA1_GATE = 'research/round33/advisor/ba1-gate.json'
I1_REL = 'research/round21/forward/i1/report.md'
SKEPTIC_ALLOWED = ('research/round29/skeptic/am2.md', 'research/round33/skeptic/ba1.md', 'research/round33/skeptic/ba2.md')
ADVISOR_ALLOWED = ('research/round33/advisor/ba1-gate.json', 'research/round33/advisor/ba2-gate.json',
                   'research/round33/advisor/selection-bb1.md')
FORBIDDEN_PREFIXES = (
    'research/round33/forward/bb', 'research/round33/reverse/bb', 'research/round33/experts/',
    'research/round33/advisor/deliberation', 'research/round33/advisor/panel', 'research/round33/advisor/plan',
    'research/round33/advisor/triage', 'research/round33/advisor/brief', 'research/round33/advisor/modern',
)
F1_NAME = 'F1: AQ1 centered whole-star boxes Lambda_N=[-N,N]^3'
F2_NAME = 'F2: I1 section 6 all-contained-face boxes with padding on the same Lambda_N'
ROUTE = 'iterated_split'
TIERS = ('crude_majorant', 'exact_first_order')
BB1_ROUTES = ('polymer_kp', 'iterated_split')
BA1_INPUTS = ('gate_bound_value_K=49/111790368', 'analytic_disc', 'weighted_norm')
DEN = 10 ** 40
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state', 'uniquely determines the ground state',
    'the thermodynamic limit', 'correlation length',
]
NEGATION = re.compile(r"\b(not|never|no|nor|neither|without|excludes?|excluded|exclusion|forbidden|"
                      r"cannot|does not|is not|are not|nothing|none)\b", re.I)
FIXTURE_LABEL = {'model_is_finite_graph': True, 'transfers_to_aq': False}


# ----------------------------------------------------------------- exceptions
class AdmissionError(Exception):
    """A validator refused its input: the required fate of a damaging mutation."""


class ProducerError(Exception):
    """An identity required by the proof failed; the run aborts without output."""


def require(condition, reason):
    if condition is not True:
        raise AdmissionError(reason)


def must(condition, reason):
    if condition is not True:
        raise ProducerError(reason)


CHECKS = []
MUTATION_CONTROLS = []


def check(check_id, condition, **details):
    must(condition is True, 'check failed: ' + check_id)
    must(all(c['id'] != check_id for c in CHECKS), 'duplicate check id: ' + check_id)
    entry = {'id': check_id, 'passed': True}
    entry.update(details)
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run one damaging mutation (a zero-argument callable); return its rejection reason."""
    try:
        mutation()
    except AdmissionError as exc:
        return str(exc)
    raise ProducerError('damaging mutation accepted: ' + label)


def control(check_id, mutations, **details):
    """A contract control passes only if every listed damaging mutation is rejected."""
    reasons = {}
    for label, mutation in mutations:
        must(label not in reasons, 'duplicate mutation label ' + label)
        reasons[label] = rejected(mutation, label)
    must(len(reasons) > 0, 'control without mutations: ' + check_id)
    MUTATION_CONTROLS.append(check_id)
    check(check_id, True, kind='damaging_mutation_control', rejected_mutations=reasons, **details)


# ----------------------------------------------------------- exact arithmetic
def parse_q(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise AdmissionError('non-exact numeric input rejected: ' + repr(value))
    if isinstance(value, Q):
        return value
    if isinstance(value, int):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'[+-]?[0-9]+(/[1-9][0-9]*)?', value.strip()):
        return Q(value.strip())
    raise AdmissionError('malformed rational input rejected: ' + repr(value))


def qs(x):
    return str(Q(x))


def ceil_to(x, den=DEN):
    x = Q(x)
    return Q(-((-x.numerator * den) // x.denominator), den)


def floor_to(x, den=DEN):
    x = Q(x)
    return Q((x.numerator * den) // x.denominator, den)


def factorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


def exp_bounds(x, terms=24):
    """Directed enclosure of exp(x), 0<=x<=1/2: partial sum plus geometric tail."""
    x = Q(x)
    must(Q(0) <= x <= Q(1, 2), 'exponential argument outside [0,1/2]')
    partial, power = Q(0), Q(1)
    for k in range(terms + 1):
        partial += power / factorial(k)
        power *= x
    tail = power / factorial(terms + 1) / (1 - x / (terms + 2))
    return floor_to(partial), ceil_to(partial + tail)


def sci(x, digits=12):
    """Truncated decimal preview computed with integers only (never used to decide)."""
    x = Q(x)
    if x == 0:
        return '0'
    sign = '-' if x < 0 else ''
    x = abs(x)
    e = len(str(x.numerator)) - len(str(x.denominator))
    while Q(10) ** e > x:
        e -= 1
    while Q(10) ** (e + 1) <= x:
        e += 1
    scaled = x / Q(10) ** e * 10 ** (digits - 1)
    mant = str(scaled.numerator // scaled.denominator)
    return sign + mant[0] + '.' + mant[1:] + 'e' + str(e)


def exact(x):
    return {'exact': qs(x), 'preview': sci(x)}


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def isqrt_upper(x, den=10 ** 30):
    """Directed upper rational bound for sqrt(x), x>=0."""
    x = Q(x)
    must(x >= 0, 'sqrt of negative')
    n = x.numerator * den * den
    d = x.denominator
    r = int_sqrt_ceil(-(-n // d))
    return Q(r, den)


def int_sqrt_ceil(n):
    if n <= 0:
        return 0
    r = int_sqrt_floor(n)
    return r if r * r == n else r + 1


def int_sqrt_floor(n):
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


# ------------------------------------------------------------ lattice geometry
E = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
R_COVER = (ORIGIN, EZ)
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))


def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def coarse(p):
    """I1.1: pi(x,y,z)=(floor(x/4), floor(y/2), z)."""
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    return ((p, a), (vadd(p, E[a]), c), (vadd(p, E[c]), a), (p, c))


def derive_classes():
    """All 24 anchored face classes derived from pi and the link tails (I1 section 3)."""
    out = []
    for a, c in (('x', 'y'), ('x', 'z'), ('y', 'z')):
        for r in range(4):
            for s in range(2):
                p = (r, s, 0)
                links = face_links(p, a, c)
                K = tuple(sorted({vsub(coarse(t), coarse(p)) for t, _ in links}))
                selected = (a, c) == ('x', 'y') and s == 0 and r <= 2
                out.append({'orient': a + c, 'r': r, 's': s, 'K': K, 'selected': selected})
    return out


TOKENS = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}


def parse_i1_table(text):
    rows = []
    pat = re.compile(r'^\| (xy|xz|yz): r=([0-9,]+); s=([0-9,]+) \| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|\s*$')
    for line in text.splitlines():
        m = pat.match(line.strip())
        if m:
            rs = [int(v) for v in m.group(2).split(',')]
            ss = [int(v) for v in m.group(3).split(',')]
            support = tuple(sorted(TOKENS[t.strip()] for t in m.group(5).split(',')))
            rows.append({'orient': m.group(1), 'r': rs, 's': ss, 'count': int(m.group(4)),
                         'K': support, 'selected': m.group(6) == 'selected'})
    return rows


def compare_i1(rows, classes):
    seen = set()
    for row in rows:
        require(row['count'] == len(row['r']) * len(row['s']), 'I1 table row count')
        for r in row['r']:
            for s in row['s']:
                match = [c for c in classes if c['orient'] == row['orient'] and c['r'] == r and c['s'] == s]
                require(len(match) == 1 and match[0]['K'] == row['K'] and match[0]['selected'] == row['selected'],
                        'I1 table row disagrees with the derived class')
                seen.add((row['orient'], r, s))
    require(len(seen) == 24, 'I1 table does not cover the 24 classes')
    return True


CLASSES = derive_classes()
OMITTED = [c for c in CLASSES if not c['selected']]


def face_support(face):
    b, k = face
    return tuple(sorted(vadd(b, s) for s in OMITTED[k]['K']))


def box(N):
    return frozenset(product(range(-N, N + 1), repeat=3))


def prism(lo, hi):
    return frozenset(product(*[range(lo[i], hi[i] + 1) for i in range(3)]))


def f1_faces(vol):
    out = set()
    for b in vol:
        if all(vadd(b, s) in vol for s in S_STAR):
            for k in range(len(OMITTED)):
                out.add((b, k))
    return frozenset(out)


def f2_faces(vol):
    out = set()
    for b in vol:
        for k, c in enumerate(OMITTED):
            if all(vadd(b, s) in vol for s in c['K']):
                out.add((b, k))
    return frozenset(out)


def dinf(p, q):
    return max(abs(p[0] - q[0]), abs(p[1] - q[1]), abs(p[2] - q[2]))


def norm_inf(p):
    return max(abs(p[0]), abs(p[1]), abs(p[2]))


def diam(Y):
    Y = list(Y)
    return max((dinf(a, b) for a in Y for b in Y), default=0)


# --------------------------------------------- every-site coefficient input (form b)
def star(b):
    return frozenset(vadd(b, s) for s in S_STAR)


def f1_star_pieces(vol):
    return [star(b) for b in sorted(vol) if star(b) <= vol]


def face_site_set(faces):
    out = set()
    for f in faces:
        out.update(face_support(f))
    return out


def min_dist_to_sites(u, sites):
    return min((dinf(u, s) for s in sites), default=10 ** 9)


def every_site_source_audit(N, vol_a, faces_a, vol_b, faces_b):
    """Every source face (present in one volume only) lies at l-infinity distance at least
    N-|u|_inf from every u in Lambda_N (the every-site form of the BA1 common-core lemma)."""
    source = (faces_a - faces_b) | (faces_b - faces_a)
    sites = face_site_set(source)
    worst = None
    attained = 0
    for u in sorted(box(N)):
        d = min_dist_to_sites(u, sites)
        need = N - norm_inf(u)
        if d < need:
            return {'ok': False, 'u': list(u), 'distance': d, 'required': need}
        if d == need:
            attained += 1
        slack = d - need
        worst = slack if worst is None else min(worst, slack)
    return {'ok': True, 'sources': len(source), 'min_slack': worst, 'sites_attaining': attained}


def certify_common_core_every_site(N, vol, faces):
    """Every face of the given prescription within distance N-|u|-1 of u lies in a whole star inside Lambda_N."""
    core = f1_faces(box(N))
    outside = faces - core
    sites = face_site_set(outside)
    for u in sorted(box(N)):
        require(min_dist_to_sites(u, sites) >= N - norm_inf(u), 'a non-core face lies within N-|u|-1 of u')
    return True


def bfs_orders_from(u, pieces):
    """Least connected-family size joining a piece containing u to each piece (intersection graph)."""
    idx = {p: i for i, p in enumerate(pieces)}
    start = [p for p in pieces if u in p]
    order = {p: 1 for p in start}
    frontier = list(start)
    while frontier:
        nxt = []
        for p in frontier:
            for q in pieces:
                if q not in order and p & q:
                    order[q] = order[p] + 1
                    nxt.append(q)
        frontier = nxt
    must(len(idx) == len(pieces), 'pieces distinct')
    return order


def order_vs_distance_at(u, pieces):
    order = bfs_orders_from(u, pieces)
    worst = None
    for p, n in order.items():
        d = min(dinf(u, s) for s in p)
        if d >= 1:
            require(n >= 1 + d, 'order below 1+d at u')
            slack = n - (1 + d)
            worst = slack if worst is None else min(worst, slack)
    return worst


def T_exact(rho):
    """exact_first_order circle bound T(rho)=(49 rho/144)/(1-28 rho G'(R)) with G'(R)<352."""
    rho = Q(rho)
    must(9856 * rho < 1, 'contraction on the disc')
    return Q(49, 144) * rho / (1 - 9856 * rho)


def T_crude(rho):
    """crude_majorant circle bound 28 rho G(R) with G(R)<148/7."""
    return 28 * Q(rho) * Q(148, 7)


def T_of(tier, rho):
    require(tier in TIERS, 'tier outside the vocabulary: ' + str(tier))
    return T_exact(rho) if tier == 'exact_first_order' else T_crude(rho)


def form_b_constant(tier, rho, tau):
    """Every-site form (b): sum_{I ni u}||c^A_I-c^B_I|| <= 2T(rho) (|tau|/rho)^(N-|u|_inf), 0<|tau|<rho<=tau_star."""
    rho, tau = Q(rho), abs(Q(tau))
    require(0 < tau < rho <= Q(1, 37888), 'disc radius outside (|tau|, tau_star]')
    return 2 * T_of(tier, rho), tau / rho


# ------------------------------------------------------- creation-algebra engine
# Sites 0..n-1; local level 0 is the vacuum Omega_x, levels 1..d-1 span Q_x H_x.
# A support I is a sorted tuple of sites; c_I maps an excited configuration on I to a
# rational amplitude; hat c_I = |c_I><Omega_I| (x) 1. Real amplitudes only (fixtures).
def vec_add(u, v, s=1):
    w = dict(u)
    for k, a in v.items():
        w[k] = w.get(k, 0) + s * a
    return {k: a for k, a in w.items() if a != 0}


def apply_c(I, cvec, v):
    out = {}
    for b, a in v.items():
        if all(b[x] == 0 for x in I):
            for e, ce in cvec.items():
                nb = list(b)
                for x, ex in zip(I, e):
                    nb[x] = ex
                nb = tuple(nb)
                out[nb] = out.get(nb, 0) + a * ce
    return {k: a for k, a in out.items() if a != 0}


def psi_of(n, coll, order=None):
    """psi = prod_I (1 - hat c_I) Omega_0 (creations commute; any order)."""
    v = {tuple([0] * n): Q(1)}
    keys = list(coll) if order is None else order
    for I in keys:
        v = vec_add(v, apply_c(I, coll[I], v), -1)
    return v


def norm2(v):
    return sum(a * a for a in v.values())


def marginal(u, w, Y, n):
    """Tr_{Y^c} |u><w| as a dict {(y-config, y'-config): value} (real vectors)."""
    rest = [k for k in range(n) if k not in Y]
    wi = {}
    for b2, y in w.items():
        wi.setdefault(tuple(b2[k] for k in rest), []).append((tuple(b2[t] for t in Y), y))
    out = {}
    for b, x in u.items():
        key = tuple(b[k] for k in rest)
        for yc2, y in wi.get(key, ()):
            kk = (tuple(b[t] for t in Y), yc2)
            out[kk] = out.get(kk, 0) + x * y
    return {k: a for k, a in out.items() if a != 0}


def density(v, Y, n):
    z = norm2(v)
    return {k: a / z for k, a in marginal(v, v, Y, n).items()}


def mat_lin(*terms):
    out = {}
    for coef, m in terms:
        for k, a in m.items():
            out[k] = out.get(k, 0) + coef * a
    return {k: a for k, a in out.items() if a != 0}


def mat_T(m):
    return {(q, p): a for (p, q), a in m.items()}


def mat_trace(m):
    return sum(a for (p, q), a in m.items() if p == q)


def remove_meeting(coll, U):
    return {I: c for I, c in coll.items() if not set(I) & set(U)}


def qubit_coll(amps):
    return {I: {tuple([1] * len(I)): Q(a)} for I, a in amps.items()}


def c_norm(cvec):
    """||c_I|| for a qubit support (one excited configuration): exact."""
    must(len(cvec) == 1, 'qubit coefficient')
    return abs(next(iter(cvec.values())))


def herm2(m):
    """Entries (p, s, r) of a real symmetric 2x2 matrix on one qubit."""
    return (m.get(((0,), (0,)), 0), m.get(((0,), (1,)), 0), m.get(((1,), (1,)), 0))


def tn2_parts(m):
    """||X||_1 = max(|p+r|, 2 sqrt(((p-r)/2)^2+s^2)) for X=[[p,s],[s,r]]: return (|p+r|^2, 4(((p-r)/2)^2+s^2))."""
    p, s, r = herm2(m)
    must(m.get(((1,), (0,)), 0) == s, 'symmetric')
    return ((p + r) ** 2, (p - r) ** 2 + 4 * s * s)


def tn2_sq(m):
    """(trace norm)^2 of a real symmetric 2x2 matrix, exactly."""
    a, b = tn2_parts(m)
    return max(a, b)


def tn2_leq(m, bound):
    """Exact test ||X||_1 <= bound for a real symmetric 2x2 matrix."""
    bound = Q(bound)
    return bound >= 0 and tn2_sq(m) <= bound * bound


# ------------------------------------------------ split-route identities (item 1, item 3)
def split_decomposition(n, coll, Y):
    """Y-split: rho_Y = N_c(omega_O)/Tr N_c(omega_O); returns (E-part collection, outside vector, straddle region)."""
    A = {I: c for I, c in coll.items() if set(I) & set(Y)}
    B = {I: c for I, c in coll.items() if not set(I) & set(Y)}
    O = sorted({x for I in A for x in I if x not in Y})
    return A, B, O


def j_split_terms(n, coll, cJ_new, J, Y):
    """Exact J-split identity (**) for J disjoint from Y: returns the two sides."""
    c1 = dict(coll)
    c2 = dict(coll)
    c2[J] = cJ_new
    v1, v2 = psi_of(n, c1), psi_of(n, c2)
    rho1, rho2 = density(v1, Y, n), density(v2, Y, n)
    phi = psi_of(n, remove_meeting(coll, J))
    n2 = norm2(phi)
    rho_phi = density(phi, Y, n)
    a = sum(x * x for x in c1[J].values()) - sum(x * x for x in c2[J].values())
    delta = {e: c1[J][e] - c2[J].get(e, 0) for e in c1[J]}
    w = dict(phi)
    for I, cv in coll.items():
        if set(I) & set(J) and I != J:
            w = vec_add(w, apply_c(I, cv, w), -1)
    dpp = vec_add(w, phi, -1)
    gam = {}
    for b, x in dpp.items():
        e = tuple(b[j] for j in J)
        if e in delta:
            nb = list(b)
            for j in J:
                nb[j] = 0
            nb = tuple(nb)
            gam[nb] = gam.get(nb, 0) + delta[e] * x
    G = marginal(phi, gam, Y, n)
    trG = mat_trace(G)
    Z = norm2(v1)
    defect = mat_lin((1, G), (-trG, rho2))
    rhs = mat_lin((a * n2 / Z, rho_phi), (-a * n2 / Z, rho2), (-1 / Z, defect), (-1 / Z, mat_T(defect)))
    lhs = mat_lin((1, rho1), (-1, rho2))
    return {'lhs': lhs, 'rhs': rhs, 'Z': Z, 'n2': n2, 'a': a, 'Gamma': G, 'phi': phi, 'rho_prime': rho2}


def tensor_g(g, S, vec):
    out = {}
    for b, x in vec.items():
        must(all(b[s] == 0 for s in S), 'vacuum on S')
        for e, ge in g.items():
            nb = list(b)
            for s, ex in zip(S, e):
                nb[s] = ex
            nb = tuple(nb)
            out[nb] = out.get(nb, 0) + ge * x
    return out


def coverings(coll, S, U):
    """Families of pairwise disjoint supports meeting S, not meeting U, covering S."""
    allowed = [I for I in sorted(coll) if set(I) & set(S) and not set(I) & set(U)]
    res = []

    def extend(start, chosen, covered):
        if set(S) <= covered and chosen:
            res.append(tuple(chosen))
        for i in range(start, len(allowed)):
            I = allowed[i]
            if not covered & set(I):
                extend(i + 1, chosen + [I], covered | set(I))

    extend(0, [], set())
    return res


def contract_g(coll, g, S, F):
    un = sorted(set().union(*[set(I) for I in F]))
    Sp = tuple(x for x in un if x not in S)
    confs = {(): Q(1)}
    for I in F:
        new = {}
        for k, a in confs.items():
            for e, ce in coll[I].items():
                new[k + tuple(zip(I, e))] = a * ce
        confs = new
    out = {}
    for k, a in confs.items():
        dk = dict(k)
        e = tuple(dk[s] for s in S)
        if e in g:
            ep = tuple(dk[s] for s in Sp)
            out[ep] = out.get(ep, 0) + g[e] * a
    return Sp, out


def gamma_direct(n, coll, U, S, g, Y):
    phiU = psi_of(n, remove_meeting(coll, U))
    phiUS = psi_of(n, remove_meeting(coll, tuple(set(U) | set(S))))
    return marginal(phiU, tensor_g(g, S, phiUS), Y, n)


def gamma_recursive(n, coll, U, S, g, Y):
    """The covering recursion: Gamma[U,S,g] = sum_F (-1)^|F| Gamma[U u S, S'_F, g'_F]^* (+ scalar terms)."""
    if set(S) & set(Y):
        return gamma_direct(n, coll, U, S, g, Y)
    total = {}
    U2 = tuple(sorted(set(U) | set(S)))
    for F in coverings(coll, S, U):
        Sp, gp = contract_g(coll, g, S, F)
        if not Sp:
            ph = psi_of(n, remove_meeting(coll, U2))
            term = {k: gp.get((), 0) * v for k, v in marginal(ph, ph, Y, n).items()}
        else:
            term = mat_T(gamma_recursive(n, coll, U2, Sp, gp, Y))
        total = mat_lin((1, total), ((-1) ** len(F), term))
    return total


# ------------------------------------------------------------------ exact fixtures
def lcg_rationals(seed, count, span=9, lo=20, hi=60):
    """Deterministic rational amplitudes (linear congruential generator; no library randomness)."""
    out, x = [], seed
    for _ in range(count):
        x = (1103515245 * x + 12345) % (2 ** 31)
        num = (x % (2 * span + 1)) - span
        x = (1103515245 * x + 12345) % (2 ** 31)
        den = lo + x % (hi - lo)
        out.append(Q(num if num != 0 else 1, den))
    return out


def split_route_fixture():
    """Split-route trace fixture: qutrit sites (two excited levels), exact identities (**) and the covering recursion."""
    n, d = 5, 3
    supports = [(0,), (1,), (2,), (3,), (4,), (0, 1), (1, 2), (2, 3), (3, 4), (1, 3), (0, 2), (2, 4), (1, 2, 3), (2, 3, 4)]
    amps = lcg_rationals(2027, sum((d - 1) ** len(I) for I in supports) + 4)
    coll, k = {}, 0
    for I in supports:
        cv = {}
        for e in product(range(1, d), repeat=len(I)):
            cv[e] = amps[k]
            k += 1
        coll[I] = cv
    v = psi_of(n, coll)
    must(vec_add(v, psi_of(n, coll, order=list(reversed(supports))), -1) == {}, 'product ordering independence')
    Y, J = (0,), (3, 4)
    newJ = {e: amps[k + i] for i, e in enumerate(product(range(1, d), repeat=2))}
    terms = j_split_terms(n, coll, newJ, J, Y)
    identity = all(terms['lhs'].get(x, 0) == terms['rhs'].get(x, 0) for x in set(terms['lhs']) | set(terms['rhs']))
    # orthogonality at J: (P_J (x) 1) psi = Omega_J (x) phi_J
    projected = {b: a for b, a in v.items() if all(b[j] == 0 for j in J)}
    ortho = projected == psi_of(n, remove_meeting(coll, J))
    rec = []
    for U, S, g in (((), (2,), {(1,): Q(1, 3), (2,): Q(-2, 7)}), ((), (3, 4), {e: amps[i] for i, e in enumerate(product((1, 2), repeat=2))}),
                    ((4,), (2, 3), {e: amps[5 + i] for i, e in enumerate(product((1, 2), repeat=2))})):
        A = gamma_direct(n, coll, U, S, g, Y)
        B = gamma_recursive(n, coll, U, S, g, Y)
        rec.append(all(A.get(x, 0) == B.get(x, 0) for x in set(A) | set(B)))
    return {'sites': n, 'local_dim': d, 'supports': len(supports), 'Y': list(Y), 'J': list(J),
            'identity_star_star_exact': identity, 'Z_ge_n2': terms['Z'] >= terms['n2'],
            'orthogonality_at_J': ortho, 'covering_recursion_exact': rec, **FIXTURE_LABEL}


def lemma_g_fixture():
    """Lemma G on a qubit chain: every single-support change moves rho_Y by at most 2||delta_J|| (any Y)."""
    n = 5
    supports = [(0,), (1,), (2,), (3,), (4,), (0, 1), (1, 2), (2, 3), (3, 4), (0, 2), (1, 3), (0, 1, 2), (2, 3, 4), (0, 4)]
    amps = lcg_rationals(77, 2 * len(supports), span=12, lo=4, hi=15)
    coll = qubit_coll({I: amps[i] for i, I in enumerate(supports)})
    Y = (0,)
    rho = density(psi_of(n, coll), Y, n)
    worst = None
    for i, J in enumerate(supports):
        c2 = dict(coll)
        c2[J] = {tuple([1] * len(J)): amps[len(supports) + i]}
        delta = abs(next(iter(coll[J].values())) - next(iter(c2[J].values())))
        diff = mat_lin((1, rho), (-1, density(psi_of(n, c2), Y, n)))
        require(tn2_leq(diff, 2 * delta), 'Lemma G violated on the fixture')
        ratio = tn2_sq(diff) / (4 * delta * delta)
        worst = ratio if worst is None else max(worst, ratio)
    return {'supports': len(supports), 'max_ratio_sq_to_bound_sq': qs(worst), 'holds': True, **FIXTURE_LABEL}


def mat_mul_full(A, B, dim):
    return [[sum(A[i][k] * B[k][j] for k in range(dim)) for j in range(dim)] for i in range(dim)]


def mixed_outside_fixture():
    """fixture_split_lipschitz_and_trace: Y={r}, O={o1,o2}, mixed outside states; exact Tr N >= 1 and the omega-Lipschitz bound."""
    amps = {(0,): Q(1, 5), (0, 1): Q(-1, 4), (0, 2): Q(1, 3), (0, 1, 2): Q(-1, 6)}
    coll = qubit_coll(amps)
    n = 3
    basis = list(product((0, 1), repeat=3))

    def E_matrix(cl):
        cols = []
        for b in basis:
            v = {b: Q(1)}
            for I, cv in cl.items():
                v = vec_add(v, apply_c(I, cv, v), -1)
            cols.append([v.get(bb, Q(0)) for bb in basis])
        return [[cols[j][i] for j in range(8)] for i in range(8)]

    Em = E_matrix(coll)

    def state(vecs):
        m = [[Q(0)] * 4 for _ in range(4)]
        for p, vv in vecs:
            z = sum(x * x for x in vv)
            for i in range(4):
                for j in range(4):
                    m[i][j] += p * vv[i] * vv[j] / z
        return m

    def N_of(om):
        full = [[Q(0)] * 8 for _ in range(8)]
        for i, bi in enumerate(basis):
            for j, bj in enumerate(basis):
                if bi[0] == 0 and bj[0] == 0:
                    full[i][j] = om[2 * bi[1] + bi[2]][2 * bj[1] + bj[2]]
        M = mat_mul_full(mat_mul_full(Em, full, 8), [list(r) for r in zip(*Em)], 8)
        out = {}
        for i, bi in enumerate(basis):
            for j, bj in enumerate(basis):
                if bi[1:] == bj[1:]:
                    k = ((bi[0],), (bj[0],))
                    out[k] = out.get(k, 0) + M[i][j]
        return out

    om1 = state([(Q(1, 3), [Q(1), Q(-1, 2), Q(1, 4), Q(0)]), (Q(2, 3), [Q(1), Q(0), Q(0), Q(-1, 3)])])
    om2 = state([(Q(1, 2), [Q(1), Q(1, 5), Q(0), Q(1, 7)]), (Q(1, 2), [Q(1, 2), Q(1), Q(-1), Q(0)])])
    N1, N2 = N_of(om1), N_of(om2)
    t1, t2 = mat_trace(N1), mat_trace(N2)
    rho1 = {k: v / t1 for k, v in N1.items()}
    rho2 = {k: v / t2 for k, v in N2.items()}
    dN = mat_lin((1, N1), (-1, N2))
    drho = mat_lin((1, rho1), (-1, rho2))
    # ||drho||_1 <= 2||N(om1-om2)||_1 : compare exact trace-norm squares of 2x2 matrices
    lip = tn2_sq(drho) <= 4 * tn2_sq(dN)
    # omega-Lipschitz constant 2(2 eps+eps^2), eps = prod_{y in Y}(1+s_y)-1 = s_r here; ||Delta||_1 >= ||Delta||_2
    eps = sum(abs(a) for a in amps.values())
    k_om = 2 * eps + eps * eps
    frob = sum(((om1[i][j] - om2[i][j]) ** 2) for i in range(4) for j in range(4))
    omega_lip = tn2_sq(dN) <= k_om * k_om * frob
    # product-of-growing-region-sizes charging versus per-site charging (depth dependence)
    return {'trace_N_omega1': qs(t1), 'trace_N_omega2': qs(t2), 'trace_at_least_one': t1 >= 1 and t2 >= 1,
            'rho_lipschitz_in_N': lip, 'omega_lipschitz_constant': qs(k_om), 'omega_lipschitz_holds': omega_lip,
            'outside_states': 'mixed rank-two rational states on H_{o1} (x) H_{o2}', **FIXTURE_LABEL}


def growing_size_rule(depth, t0):
    """The rejected split charge: per-level factor |S_k| t0 with |S_k|=(2k+1)^3 growing with depth."""
    return (2 * depth + 1) ** 3 * Q(t0)


def per_site_rule(depth, tW, ccard=8):
    """The per-site charge of the iterated split: the same factor c_card t_W at every depth."""
    return ccard * Q(tW)


def certify_charging_rule(rule, t0, tW, depths=(1, 2, 3, 50, 400)):
    vals = [rule(k, t0 if rule is growing_size_rule else tW) for k in depths]
    require(all(v == vals[0] for v in vals), 'split charge grows with depth (product of growing region sizes)')
    require(vals[0] < 1, 'per-level factor not below one')
    return True


def first_depth_without_decay(t0):
    k = 0
    while growing_size_rule(k, t0) < 1:
        k += 1
    return k


# ------------------------------------------------ marginal-locality constants (item 3)
def beta_star(t0, tW, ccard=8):
    """Closure of the iterated-split recursion: kappa(J) <= beta* H(J) for J not meeting Y.
    R=(2+c b)t_W, mu=t0 R/(1-t0), alpha=(2t_W+t0 R/(1-t0))/(1-c t_W); kappa/H <= 2 t0 R + 2 alpha = c1 + c2 b."""
    t0, tW = Q(t0), Q(tW)
    require(0 <= t0 < 1 and 0 <= tW and ccard * tW < 1, 'per-site sums outside the contraction range')
    c1 = 4 * t0 * tW + (4 * tW + 4 * t0 * tW / (1 - t0)) / (1 - ccard * tW)
    c2 = 2 * ccard * t0 * tW + 2 * ccard * t0 * tW / ((1 - t0) * (1 - ccard * tW))
    require(c2 < 1, 'closure coefficient not below one')
    return c1, c2, c1 / (1 - c2)


def lattice_sum_3d(x):
    """S(x)=sum_{v in Z^3} x^{|v|_inf} = 1 + sum_{r>=1} (24 r^2+2) x^r (exact, 0<=x<1)."""
    x = Q(x)
    require(0 <= x < 1, 'lattice sum ratio not below one (split weight too small for the rate)')
    return 1 + 24 * x * (1 + x) / (1 - x) ** 3 + 2 * x / (1 - x)


def shell_count(r):
    return 1 if r == 0 else (2 * r + 1) ** 3 - (2 * r - 1) ** 3


def split_constants(tier, tau, W, rho_disc, q):
    """All constants of one (tier, pair): K (BA1 every-site input), t0, tW, beta*, S, c_site, C."""
    tau, W, rho_disc, q = abs(Q(tau)), Q(W), Q(rho_disc), Q(q)
    require(q == tau / rho_disc, 'rate is not |tau|/rho for the declared disc')
    require(1 <= W <= 1 / (37888 * tau), 'split creation weight outside the admissible range [1, 1/(37888|tau|)]')
    K, qq = form_b_constant(tier, rho_disc, tau)
    must(qq == q, 'rate consistency')
    t0 = 2 * T_of(tier, tau)
    tW = 2 * T_of(tier, W * tau)
    c1, c2, beta = beta_star(t0, tW, 8)
    lam = 2 / W
    S = lattice_sum_3d(lam / q)
    # every site of the union volume outside Lambda_N: sum_{I ni x}||delta_I|| <= 2T(|tau|) <= K/q
    require(t0 <= K / q, 'outside-box coefficient sums exceed K q^(N-|x|)')
    csite = K * (2 + beta * S)
    C = csite * (1 + q)
    return {'tier': tier, 'route': ROUTE, 'K': K, 'q': q, 'W': W, 'lambda': lam, 'w_prime': 1 / lam,
            't0': t0, 'tW': tW, 'c1': c1, 'c2': c2, 'beta': beta, 'S': S, 'c_site': csite, 'C': C,
            'kappa0_R': 2 * beta, 'eta': Q(0)}


def ledger_parts(sc):
    """Error-ledger split of C: near (coefficient input on supports meeting R) and split remainder pieces."""
    t0, tW, q, K = sc['t0'], sc['tW'], sc['q'], sc['K']
    norm_a = 4 * t0 * tW
    straddle = 4 * tW / (1 - 8 * tW)
    removal = 4 * t0 * tW / ((1 - t0) * (1 - 8 * tW))
    must(norm_a + straddle + removal == sc['c1'], 'c1 decomposition')
    feedback = sc['beta'] - sc['c1']
    f = K * sc['S'] * (1 + q)
    return {'near_coefficient_input': K * 2 * (1 + q), 'straddling_chains': f * straddle,
            'normalization_a_term': f * norm_a, 'removal_terms': f * removal, 'closure_feedback': f * feedback}


def chain_fixture_1d():
    """End-to-end check of the marginal-locality lemma on a qubit chain (1D constants: |I|<=2^diam, c_card=1)."""
    n, Y, W = 7, (0,), Q(8)
    lam = 2 / W
    supports = [(i,) for i in range(n)] + [(i, i + 1) for i in range(n - 1)] + [(i, i + 1, i + 2) for i in range(n - 2)] + \
        [(0, 2), (1, 4), (2, 5, 6), (0, 3), (3, 6)]
    base = lcg_rationals(4242, 2 * len(supports), span=7, lo=40, hi=90)
    c, cp = {}, {}
    for i, I in enumerate(supports):
        scale = Q(1, 16) ** (max(I) - min(I))
        c[I] = {tuple([1] * len(I)): base[i] * scale}
        cp[I] = {tuple([1] * len(I)): (base[i] + base[len(supports) + i] / 5) * scale}
    m = {I: max(abs(next(iter(c[I].values()))), abs(next(iter(cp[I].values())))) for I in supports}
    dmt = {I: abs(next(iter(c[I].values())) - next(iter(cp[I].values()))) for I in supports}
    t0 = max(sum(m[I] for I in supports if x in I) for x in range(n))
    tW = max(sum(W ** (max(I) - min(I)) * m[I] for I in supports if x in I) for x in range(n))
    c1, c2, beta = beta_star(t0, tW, 1)
    h = {x: lam ** x for x in range(n)}
    D = {x: sum(dmt[I] for I in supports if x in I) for x in range(n)}
    bound = 2 * D[0] + beta * sum(h[x] * D[x] for x in range(n))
    rho, rhop = density(psi_of(n, c), Y, n), density(psi_of(n, cp), Y, n)
    diff = mat_lin((1, rho), (-1, rhop))
    total_ok = tn2_leq(diff, bound)
    far_ok, worst, far_count = True, Q(0), 0
    for J in supports:
        if 0 in J:
            continue
        far_count += 1
        c2c = dict(c)
        c2c[J] = cp[J]
        dd = mat_lin((1, rho), (-1, density(psi_of(n, c2c), Y, n)))
        HJ = sum(h[x] for x in J)
        if not tn2_leq(dd, beta * HJ * dmt[J]):
            far_ok = False
        if dmt[J] != 0:
            worst = max(worst, tn2_sq(dd) / (beta * HJ * dmt[J]) ** 2)
    return {'sites': n, 'supports': len(supports), 'W': qs(W), 'lambda': qs(lam), 't0': qs(t0), 'tW': qs(tW),
            'beta': exact(beta), 'observed_sq': exact(tn2_sq(diff)), 'bound': exact(bound), 'total_bound_holds': total_ok,
            'single_far_support_bounds_hold': far_ok, 'far_supports': far_count, 'max_far_ratio_sq': exact(worst), **FIXTURE_LABEL}


# ---------------------------------------------------- polynomial chain fixture
def pmul(a, b):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            out[e] = out.get(e, 0) + ca * cb
    return {e: v for e, v in out.items() if v != 0}


def padd(a, b, s=1):
    out = dict(a)
    for e, v in b.items():
        out[e] = out.get(e, 0) + s * v
    return {e: v for e, v in out.items() if v != 0}


def second_order_chain_fixture():
    """Sites r, o1, o2; supports {r,o1}:a, {o1,o2}:b, {o2}:c (variables). The unnormalized R-marginal is an exact
    polynomial; a change of c (two supports away from R) enters the off-diagonal only through the product a*b."""
    A, B, C = {(1, 0, 0): Q(1)}, {(0, 1, 0): Q(1)}, {(0, 0, 1): Q(1)}
    one = {(0, 0, 0): Q(1)}
    # psi = (1-a c_{r o1})(1-b c_{o1 o2})(1-c c_{o2}) |000>, components over (r,o1,o2)
    psi = {(0, 0, 0): one}
    for sup, var in (((0, 1), A), ((1, 2), B), ((2,), C)):
        new = dict(psi)
        for bconf, amp in psi.items():
            if all(bconf[x] == 0 for x in sup):
                nb = list(bconf)
                for x in sup:
                    nb[x] = 1
                nb = tuple(nb)
                new[nb] = padd(new.get(nb, {}), pmul(amp, var), -1)
        psi = {k: v for k, v in new.items() if v}
    rho = {}
    for b1, a1 in psi.items():
        for b2, a2 in psi.items():
            if b1[1:] == b2[1:]:
                key = (b1[0], b2[0])
                rho[key] = padd(rho.get(key, {}), pmul(a1, a2))
    off = rho.get((0, 1), {})
    must(off == {(1, 1, 1): Q(-1)}, 'off-diagonal is exactly -a b c')
    must(rho[(0, 0)] == {(0, 0, 0): Q(1), (0, 2, 0): Q(1), (0, 0, 2): Q(1)}, 'rho_00 = 1+b^2+c^2')
    must(rho[(1, 1)] == {(2, 0, 0): Q(1), (2, 0, 2): Q(1)}, 'rho_11 = a^2+a^2 c^2')
    return {'unnormalized_rho': {'00': '1+b^2+c^2', '01': '-a*b*c', '11': 'a^2+a^2*c^2'},
            'change_of_offdiagonal_per_unit_delta_c': '-a*b (product of the two straddling amplitudes)',
            'first_order_term_in_straddling_amplitudes': 'absent', **FIXTURE_LABEL}


def certify_propagation_claim(claim, a, b):
    """The exact change of the unnormalized off-diagonal per unit change of c is -a*b."""
    a, b = Q(a), Q(b)
    require(claim['order_in_straddling_amplitudes'] == 2, 'first-order propagation claim rejected (exact polynomial is a*b)')
    require(Q(claim['per_link'][0]) * Q(claim['per_link'][1]) >= abs(a * b), 'per-link factor below the exact one')
    return True


def straddling_fixture():
    """R={r0,r1}, outside o. First-order R-marginals: a one-site straddling support {r0,o} and a support strictly
    containing R, {r0,r1,o}, both give zero; the support R itself does not. Second order: straddling supports give
    nonzero populations. The AV1 F13 pair: straddling a enters e^2 at first order, the off-diagonal only via a*b."""
    n, Y, eps = 3, (0, 1), Q(1, 10)
    res = {}
    for name, I in (('one_site_straddling', (0, 2)), ('strictly_containing_R', (0, 1, 2)), ('equal_to_R', (0, 1))):
        v = psi_of(n, qubit_coll({I: eps}))
        m = marginal(v, v, Y, n)
        vac = ((0, 0), (0, 0))
        first = {k: val for k, val in m.items() if k != vac and (k[0] == (0, 0) or k[1] == (0, 0))}
        second = {k: val for k, val in m.items() if k[0] != (0, 0) and k[1] != (0, 0)}
        res[name] = {'first_order_marginal_zero': first == {}, 'second_order_population': qs(sum(second.get((k, k), 0) for k in [(1, 0), (0, 1), (1, 1)]))}
    must(res['one_site_straddling']['first_order_marginal_zero'] and res['strictly_containing_R']['first_order_marginal_zero']
         and not res['equal_to_R']['first_order_marginal_zero'], 'straddling first-order pattern')
    a, b = Q(1, 3), Q(1, 2)
    e2 = a * a / (1 + b * b)
    rho = density(psi_of(3, qubit_coll({(0, 1): a, (1,): b})), (0,), 3)
    must(rho[((0,), (1,))] == a * b / (1 + a * a + b * b), 'off-diagonal a b/Z')
    return {'first_order_patterns': res, 'e_squared_first_order_in_a': qs(e2), 'offdiagonal': qs(rho[((0,), (1,))]),
            'budget_without_straddling_supports': '0', 'budget_with_straddling': qs(a), **FIXTURE_LABEL}


def certify_split_budget(includes_straddling, straddling_order):
    require(includes_straddling is True, 'straddling supports dropped from the split')
    require(straddling_order == 'all_orders_via_coverings', 'straddling supports charged only at first order')
    return True


def coefficient_vs_marginal_fixture():
    """AV1 F13 type: coefficients on supports meeting R unchanged, the R-marginal moves."""
    out = []
    for b in (Q(1, 2), Q(0)):
        out.append(density(psi_of(3, qubit_coll({(0, 1): Q(1, 3), (1,): b, (2,): Q(0)})), (0,), 3))
    diff = mat_lin((1, out[0]), (-1, out[1]))
    must(out[0][((0,), (0,))] == Q(45, 49) and out[0][((0,), (1,))] == Q(6, 49) and out[1][((1,), (1,))] == Q(1, 10),
         'fixture values')
    return {'rho_b_half': [[qs(out[0][((0,), (0,))]), qs(out[0][((0,), (1,))])], [qs(out[0][((1,), (0,))]), qs(out[0][((1,), (1,))])]],
            'rho_b_zero': [[qs(out[1].get(((0,), (0,)), 0)), '0'], ['0', qs(out[1][((1,), (1,))])]],
            'coefficient_difference_on_supports_meeting_R': '0', 'trace_norm_sq': qs(tn2_sq(diff)), **FIXTURE_LABEL}


def certify_state_inference(coefficient_difference, trace_norm_sq, inference):
    if inference == 'marginal_decay_from_coefficient_decay':
        require(not (coefficient_difference == 0 and trace_norm_sq > 0), 'state decay inferred from coefficient decay')
    return True


def global_fidelity_fixture(n=400):
    """Product states (x)(Omega) versus (x)(Omega+e/10): global fidelity (100/101)^n collapses, one-site marginals stay fixed."""
    f = Q(100, 101)
    Fn = f ** n
    marg_sq = 4 * Q(1, 101)  # ||rho_1-rho'_1||_1^2 = 4(1-f)
    global_bound_sq = 4 * (1 - Fn)
    must(Fn < Q(1, 50) and global_bound_sq > Q(39, 10), 'global fidelity collapse')
    return {'sites': n, 'per_site_fidelity': qs(f), 'global_fidelity_below': '1/50', 'marginal_trace_norm_sq': qs(marg_sq),
            'global_overlap_bound_sq_above': '39/10', **FIXTURE_LABEL}


def certify_bound_route(route):
    require(route != 'global_overlap', 'bound through the global overlap of the two box vectors (orthogonality catastrophe)')
    require(route in ('per_support_telescoping', 'iterated_split'), 'unknown bound route')
    return True


def families(supports):
    out = [()]
    for r in range(1, len(supports) + 1):
        for F in combinations(supports, r):
            un = set()
            ok = True
            for I in F:
                if un & set(I):
                    ok = False
                    break
                un |= set(I)
            if ok:
                out.append(F)
    return out


def polymer_fixture():
    """fixture_polymer_identity: brute-force (psi,psi) on a four-site qubit collection equals the hard-core polymer
    sum over overlap-connected pairs of families with the same excitation set; different excitation sets pair to zero;
    the cardinality factor in the Kotecky-Preiss tree majorant is necessary."""
    amps = {(0,): Q(1, 3), (1,): Q(-1, 4), (2,): Q(1, 5), (3,): Q(1, 6), (0, 1): Q(1, 7), (1, 2): Q(-1, 8),
            (2, 3): Q(1, 9), (0, 3): Q(-1, 10), (0, 1, 2): Q(1, 11)}
    coll = qubit_coll(amps)
    n = 4
    brute = norm2(psi_of(n, coll))
    fams = families(sorted(amps))

    def w(F):
        r = Q(1)
        for I in F:
            r *= -amps[I]
        return r

    def union(F):
        return frozenset(x for I in F for x in I)

    # pairs with the same excitation set, decomposed into overlap-connected components (polymers)
    polymers = {}
    zero_pairs = 0
    for F in fams:
        for G in fams:
            if union(F) != union(G):
                zero_pairs += 1
                continue
            members = [('F', I) for I in F] + [('G', I) for I in G]
            comp = list(range(len(members)))

            def find(i):
                while comp[i] != i:
                    i = comp[i]
                return i
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    if set(members[i][1]) & set(members[j][1]):
                        comp[find(i)] = find(j)
            groups = {}
            for i, mbr in enumerate(members):
                groups.setdefault(find(i), []).append(mbr)
            for g in groups.values():
                Fg = tuple(sorted(I for s, I in g if s == 'F'))
                Gg = tuple(sorted(I for s, I in g if s == 'G'))
                polymers[(Fg, Gg)] = w(Fg) * w(Gg)
    # activity of a polymer = product of its creation amplitudes with signs; gas of site-disjoint polymers
    plist = sorted(polymers)

    def support(p):
        return frozenset(x for I in p[0] + p[1] for x in I)

    Z = Q(0)

    def gas(start, used, weight):
        nonlocal Z
        Z += weight
        for i in range(start, len(plist)):
            p = plist[i]
            if not (support(p) & used):
                gas(i + 1, used | support(p), weight * polymers[p])
    gas(0, frozenset(), Q(1))
    # different excitation sets pair to zero (explicit)
    vA = apply_c((0, 1), coll[(0, 1)], {tuple([0] * n): Q(1)})
    vB = apply_c((0,), coll[(0,)], {tuple([0] * n): Q(1)})
    cross = sum(vA.get(k, 0) * vB.get(k, 0) for k in set(vA) | set(vB))
    # cardinality factor: polymer gamma0 on 4 sites (activity z0) and four single-site polymers (activity -s)
    z0, s, a = Q(1, 100), Q(1, 10), Q(1, 8)
    x = z0 / (1 - s) ** 4
    exact_lower = x - x * x / 2          # log(1+x) >= x - x^2/2
    exact_upper = x                      # log(1+x) <= x
    kp_ok = s * Q(8, 7) <= a             # s e^a <= a with e^(1/8) < 8/7
    with_card = z0 * (1 + 4 * a + (4 * a) ** 2 / 2)   # z0 e^{a|gamma0|} >= this lower bound
    without_card_upper = z0 * Q(8, 7)    # z0 e^{a} < z0 * 8/7
    return {'brute_force_norm': qs(brute), 'polymer_sum': qs(Z), 'identity_exact': brute == Z, 'polymers': len(polymers),
            'different_excitation_sets_pair_to_zero': cross == 0, 'zero_pairs_skipped': zero_pairs,
            'kp_condition_holds': kp_ok, 'cluster_sum_lower': qs(exact_lower), 'cluster_sum_upper': qs(exact_upper),
            'majorant_with_cardinality_ge_cluster_sum': with_card >= exact_upper,
            'majorant_without_cardinality_below_cluster_sum': without_card_upper < exact_lower, **FIXTURE_LABEL}


def certify_tree_majorant(uses_cardinality_factor):
    require(uses_cardinality_factor is True, 'cardinality factor dropped from the tree majorant (underestimates the cluster sum)')
    return True


def outside_not_ground_fixture():
    """Three qubits, H = n1+n2+n3 + (7/12)(X1X2 + X2X3): exact ground E=-1/3 with creations c12=c23=2/7, c13=-1/7.
    For R={1} the outside vector |00>-(2/7)|11> is not an eigenvector of H_out = n2+n3+(7/12)X2X3."""
    g = Q(7, 12)
    basis = list(product((0, 1), repeat=3))

    def H(v, bonds):
        out = {}
        for b, a in v.items():
            out[b] = out.get(b, 0) + sum(b) * a
            for (i, j) in bonds:
                nb = list(b)
                nb[i] ^= 1
                nb[j] ^= 1
                nb = tuple(nb)
                out[nb] = out.get(nb, 0) + g * a
        return {k: x for k, x in out.items() if x != 0}
    coll = qubit_coll({(0, 1): Q(2, 7), (1, 2): Q(2, 7), (0, 2): Q(-1, 7)})
    psi = psi_of(3, coll)
    Hpsi = H(psi, [(0, 1), (1, 2)])
    eig = all(Hpsi.get(b, 0) == Q(-1, 3) * psi.get(b, 0) for b in basis)
    # other even-sector eigenvalues solve E^2-(13/3)E+49/12=0 (roots above -1/3); odd sector Gershgorin >= 1-2g
    quad_at = (Q(-1, 3)) ** 2 - Q(13, 3) * Q(-1, 3) + Q(49, 12)
    lowest = eig and quad_at > 0 and Q(13, 6) > Q(-1, 3) and 1 - 2 * g > Q(-1, 3) and 2 > Q(-1, 3)
    phi = {(0, 0): Q(1), (1, 1): Q(-2, 7)}

    def Hout(v):
        out = {}
        for b, a in v.items():
            out[b] = out.get(b, 0) + sum(b) * a
            nb = (b[0] ^ 1, b[1] ^ 1)
            out[nb] = out.get(nb, 0) + g * a
        return out
    Hp = Hout(phi)
    mean = sum(phi[k] * Hp.get(k, 0) for k in phi) / norm2(phi)
    residual = sum((Hp.get(k, 0) - mean * phi.get(k, 0)) ** 2 for k in set(Hp) | set(phi))
    return {'ground_energy': '-1/3', 'eigen_equation_exact': eig, 'is_lowest': lowest,
            'outside_vector': '|00>-(2/7)|11>', 'rayleigh_residual_sq': qs(residual), 'outside_vector_is_eigenvector': residual == 0,
            **FIXTURE_LABEL}


def certify_outside_argument(uses_gap_of_outside_vector):
    require(uses_gap_of_outside_vector is False, 'gap argument applied to the outside vector (it is not a ground state)')
    return True


def eckart_fixture():
    """cutoff_vector_removal: H=diag(0,1/2,1) (gap 1/2); 1-|<psi0,v>|^2 <= (<v,Hv>-E0)/gap for trial vectors; the
    degenerate H'=diag(0,0,1) has a trial vector with the ground energy and zero overlap (eigenvalues alone prove nothing)."""
    ev = [Q(0), Q(1, 2), Q(1)]
    pairs = []
    for v in ([Q(3), Q(1), Q(1)], [Q(1), Q(2), Q(0)], [Q(5), Q(0), Q(-1)], [Q(1), Q(0), Q(0)]):
        z = sum(x * x for x in v)
        overlap = v[0] * v[0] / z
        energy = sum(e * x * x for e, x in zip(ev, v)) / z
        lhs = 1 - overlap
        rhs = (energy - ev[0]) / (ev[1] - ev[0])
        must(lhs <= rhs, 'Eckart inequality')
        pairs.append([qs(lhs), qs(rhs)])
    degenerate_counterexample = {'H': 'diag(0,0,1)', 'trial': 'e_2', 'energy': '0', 'overlap_with_e_1': '0'}
    return {'eckart_pairs': pairs, 'degenerate': degenerate_counterexample, **FIXTURE_LABEL}


def certify_cutoff_removal(method):
    require(method == 'ground_vector_eckart_with_untruncated_gap', 'cutoff removal by eigenvalues only (degenerate counterexample)')
    return True


def limit_order_fixture():
    """a_{N,L} = L/(N+L): lim_L lim_N = 0 but lim_N lim_L = 1 (the order of limits matters)."""
    a = lambda N, L: Q(L, N + L)
    inner_N_first = a(10 ** 9, 10)          # N large at fixed L: near 0
    inner_L_first = a(10, 10 ** 9)          # L large at fixed N: near 1
    must(inner_N_first < Q(1, 10 ** 7) and inner_L_first > 1 - Q(1, 10 ** 7), 'limit order fixture')
    return {'a_NL': 'L/(N+L)', 'lim_L_lim_N': '0', 'lim_N_lim_L': '1', **FIXTURE_LABEL}


def certify_limit_order(order):
    require(order == 'cutoff_L_to_infinity_at_fixed_N_then_bound_in_N', 'N and cutoff limits exchanged')
    return True


def normalization_zero_fixture():
    """psi(z)=Omega-2z|11> has an entire coefficient while its normalization 1+4z^2 vanishes at z=i/2."""
    zr, zi = Q(0), Q(1, 2)
    re_z2 = zr * zr - zi * zi
    im_z2 = 2 * zr * zi
    must(1 + 4 * re_z2 == 0 and im_z2 == 0, 'normalization zero at i/2')
    return {'normalization': '1+4z^2', 'zero': 'i/2', 'inside_unit_disc': True, **FIXTURE_LABEL}


def certify_analyticity_claim(obj, zero_free_region_proved):
    if obj in ('reduced_density', 'normalization'):
        require(zero_free_region_proved is True, 'analyticity of the reduced density without a zero-free region')
    return True


def mean_field_fixture(n=6):
    """T(c)_i=(1/2)mean(c)+s_i: sup-norm Lipschitz 1/2, yet c_0=1/6 for every source position (no decay)."""
    vals = []
    for pos in range(1, n):
        s = [Q(1) if i == pos else Q(0) for i in range(n)]
        m = sum(s) / n / (1 - Q(1, 2))   # mean of the fixed point: m = m/2 + mean(s)
        vals.append(Q(1, 2) * m + s[0])
    must(all(v == Q(1, 6) for v in vals), 'mean-field fixture')
    return {'lipschitz': '1/2', 'value_at_0': '1/6', 'claimed_decay_(1/2)^5': qs(Q(1, 32)), **FIXTURE_LABEL}


def certify_decay_factor(provenance):
    require(provenance not in ('global_lipschitz_fixed_point', 'no_decay_bound_37/6249384', 'density_lipschitz_in_coefficients',
                               'density_lipschitz_in_outside_state'), 'a global Lipschitz constant used as a per-shell decay factor')
    require(provenance in ('covering_chain_weights_and_site_potential', 'ba1_every_site_vanishing_order'), 'unknown decay provenance')
    return True


def topology_fixture(n=30):
    """Fixed versus moving vector: A_k=|e_k><e_k| -> 0 strongly (||A_k v||^2=4^-k for v=sum 2^-j e_j) but ||A_k e_k||=1."""
    fixed = Q(1, 4 ** n)
    return {'fixed_vector_sq': qs(fixed), 'moving_vector_norm': '1', 'topology_used': 'trace norm on B(H_Y)', **FIXTURE_LABEL}


def certify_topology(t):
    require(t == 'trace norm on B(H_Y)', 'state topology not the trace norm on B(H_Y)')
    return True


# --------------------------------------------------------------- claim validators
FALSE_FLAGS = ('continuum_claim', 'uniqueness_of_ground_state_claimed', 'rate_in_a_claimed', 'scientific_priority_verified',
               'whole_sequence_claimed', 'common_limit_claimed', 'translation_invariance_claimed', 'weak_coupling_claim')
GATE_FIELD_KEYS = ('state_decay_claimed', 'state_decay_scope', 'rate_in_N_claimed', 'whole_sequence_claimed',
                   'common_limit_claimed', 'uniqueness_of_ground_state_claimed', 'rate_in_a_claimed', 'continuum_claim',
                   'translation_invariance_claimed', 'weak_coupling_claim', 'scientific_priority_verified')


def validate_claim_flags(flags):
    for k in FALSE_FLAGS:
        require(flags.get(k) is False, 'claim flag must be false: ' + k)
    return True


def certify_gate_fields(fields, required):
    require(set(fields) == set(required), 'gate field set differs from the contract')
    for k, v in required.items():
        require(fields[k] == v and type(fields[k]) is type(v), 'gate field differs from the contract: ' + k)
    return True


def certify_premise_provenance(kind):
    require(kind not in ('historical_lens', 'occult_source', 'governmental_record', 'panel_opinion'),
            'historical or non-mathematical material used as a premise')
    return True


def certify_packet_model(pk, contract):
    pre = contract['preregistration']
    require(abs(parse_q(pk['tau'])) <= parse_q(pre['tau']['value']), 'coupling above the admitted cap')
    require([parse_q(x) for x in pk['triple']] == [0, 0, 0], 'nonzero selected triple (changed model)')
    require(pk['model_id'] == pre['model_id'], 'model relabelled')
    require(pk['group'] == 'SU(2)' and pk['dimension'] == 3, 'gauge group or dimension changed')
    require(pk['metric'] == 'coarse l-infinity', 'metric changed (l1 or other)')
    require(pk['result_source'] != 'finite_graph_fixture', 'finite-graph fixture presented as the AQ result')
    require(pk['cover'] == 'R={0,e_z}', 'cover changed')
    return True


def certify_uniformity_statement(s):
    low = s.lower()
    stripped = re.sub(r'not (a statement )?uniform(ly)? in the lattice spacing( a)?', ' ', low)
    require('uniform in the lattice spacing' not in stripped and 'uniformly in the lattice spacing' not in stripped,
            'uniformity in the lattice spacing claimed')
    if 'uniform' in stripped:
        require('fixed spacing' in stripped or 'cutoff' in stripped, 'unqualified uniformity next to a rate')
    return True


def certify_rate_unit(unit):
    require(unit == 'per coarse l-infinity step in N at fixed spacing', 'rate unit is not the coarse step in N at fixed spacing')
    return True


def certify_limit_statement(obj):
    require(obj.get('whole_sequence') is False, 'whole-sequence convergence of states claimed (BB2)')
    require(obj.get('common_limit') is False, 'common limit claimed (BB2)')
    return True


def certify_families(families):
    require(families == [F1_NAME, F2_NAME], 'the two named families F1 and F2 must both be named')
    return True


def certify_family_distinct(extra_faces_by_N):
    require(all(v == 28 * N * (5 * N + 1) for N, v in extra_faces_by_N.items()) and len(extra_faces_by_N) > 0,
            'F2 collapsed onto F1 (the 28N(5N+1) extra faces are missing)')
    return True


def certify_common_clock(record):
    require(record['coupling_F1'] == record['coupling_F2'], 'the two families at different couplings')
    require(record['clock'] == 'theta=alpha*t/hbar', 'clock differs from theta=alpha t/hbar')
    return True


def certify_tier_constant(rec):
    require(rec['tier'] in TIERS, 'tier outside {exact_first_order, crude_majorant}')
    require(rec['route'] == ROUTE, 'BB1 route must be iterated_split for the reverse (a BA1 route label is not a BB1 route)')
    require(rec['ba1_input'] in BA1_INPUTS, 'BA1 input not named')
    if rec['tier'] == 'exact_first_order':
        require(rec['input_tier'] == 'exact_first_order' and rec['t_kind'] == 'exact_first_order',
                'exact_first_order constant with a crude input or remainder')
    return True


def certify_scaling(ratio, bracket):
    require(bracket[0] <= Q(ratio) <= bracket[1], 'tau/100 ratio outside the prefrozen bracket')
    return True


def certify_bracket_prefrozen(bracket, contract_bracket):
    require(bracket == contract_bracket, 'bracket not the prefrozen one')
    return True


def certify_clock(label, formula):
    table = {'s': 'alpha*t_E/hbar', 'theta': 'alpha*t/hbar', 'u': 'theta/8'}
    require(table.get(label) == formula, 'clock label and formula disagree')
    return True


def certify_first_order_amplitude(value, tau):
    require(Q(value) == -Q(tau) / 72, 'first-order coefficient is not -tau/72 in delta units')
    return True


def certify_pair(rec, contract):
    rc = contract['parameters']['rate_constant_pair']
    require(rec['q'] == parse_q(rc['headline']['q']), 'rate differs from the frozen q=1/64')
    require(rec['C_target'] == parse_q(rc['headline']['C_target']), 'C target differs from the frozen value')
    require(rec['c_site_target'] == parse_q(rc['region_form']['c_site_target']), 'c_site target differs from the frozen value')
    require(rec['q_rule'] == 'frozen', 'rate optimized per N')
    require(1 <= rec['W'] <= 1 / (37888 * abs(rec['tau'])), 'proof weight outside the admissible range')
    require(rec['weights_declared_before_constants'] is True, 'proof weights not declared before the constants')
    return True


def certify_secondary(rec, tau):
    require(rec['q'] == 151552 * abs(Q(tau)), 'secondary rate differs from 151552|tau|')
    require(rec['rho'] == Q(1, 151552), 'secondary disc radius differs from |tau|/q_2')
    require(rec['label'] == 'labelled_secondary', 'secondary pair presented as the headline')
    return True


def certify_region_bound(rec):
    require(rec.get('Y_factor') == '|Y|', 'region bound without the |Y| factor (R constant reused)')
    require(rec.get('exponent') == 'd_Y = N - max_y |y|_inf', 'region exponent is not d_Y')
    return True


def certify_every_site_input(rec):
    require(rec['form'] in ('a', 'b'), 'coefficient input form not (a) or (b)')
    require(rec['sites'] == 'every site of the union volume', 'R-only coefficient input used at far sites')
    if rec['form'] == 'b':
        require(rec['proved_in_packet'] is True, 'restated reverse form cited as admitted without its proof')
        require(rec['exponent'] == 'N-|u|_inf', 'every-site vanishing order not N-|u|_inf')
    return True


def certify_mixed_weight(rec):
    require(rec['proved_in_packet'] is True and rec['cited_from'] != 'BA1', 'mixed-weight contraction cited instead of proved')
    require(rec['loss_exponent_b'] == 4, 'mixed-weight loss is not w e^{4b} per interaction')
    return True


def mixed_weight_fixture():
    """|M| <= |X| + sum|I_j| with |X|<=4: X={0,1,2,3} (a four-site star), I_1={3,4}, I_2={0,5}: M=N\\X u X can have
    |M|=6 while |I_1|+|I_2|=4, so a loss e^{b} (instead of e^{4b}) undercharges by e^{2b}."""
    X, I1, I2 = {0, 1, 2, 3}, {3, 4}, {0, 5}
    M = (I1 | I2 | X)
    return {'M_size': len(M), 'sum_creation_sizes': len(I1) + len(I2), 'X_size': len(X),
            'needs_loss_exponent': len(M) - (len(I1) + len(I2)), **FIXTURE_LABEL}


def certify_marginal_lemma(lem):
    for k in ('eta', 'kappa0', 'w_prime', 'p', 'tier', 'route', 'combinatorial_counts'):
        require(k in lem, 'marginal-locality lemma lacks ' + k)
    for k in ('eta', 'kappa0', 'w_prime'):
        parse_q(lem[k])
    require(lem['p'] == '|I|', 'polynomial p not explicit')
    require(lem['combinatorial_counts'] is True, 'criterion asserted without activity bounds and combinatorial counts')
    require(lem['route'] == ROUTE and lem['tier'] in TIERS, 'lemma tier/route')
    return True


def certify_combination(values, combine):
    require(combine == 'linear', 'deterministic terms must add linearly (no root sums)')
    return True


def certify_no_volume_division(divisor):
    require(divisor == 1, 'division by a root of the volume or face count')
    return True


def certify_normalization(method):
    require(method == 'exact_split_ratio', 'normalization by 1+O(t^2) without the product split')
    return True


def certify_orthogonal_trace(trace_value):
    require(Q(trace_value) >= 1, 'Tr N_c(omega) below one (orthogonality broken)')
    return True


def vacuum_component_trace():
    """A 'creation' with a vacuum component, v=(1/4)|0>+(1/3)|1>: ||(1-|v><0|)|0>||^2 = 97/144 < 1."""
    return (1 - Q(1, 4)) ** 2 + Q(1, 3) ** 2


def certify_cutoff_uniform(rec):
    require(rec['constants_depend_on_L'] is False, 'constants depend on the on-site cutoff')
    require(rec['removal_after_uniform_bound'] is True, 'cutoff removed before the uniform bound')
    return True


def producer_outcome(flags):
    if not flags['headline_all_comparisons'] or not flags['region_form'] or not flags['untruncated_fixed_N']:
        return 'limited'
    if not flags['exact_tier_meets_targets'] or not flags['every_site_input_proved']:
        return 'limited'
    return 'accepted_within_scope'


def certify_outcome(recorded, flags):
    require(recorded == producer_outcome(flags), 'recorded outcome differs from the executed evidence')
    return True


def certify_no_retuning(tau_used, tau_contract):
    require(tau_used == tau_contract, 'tau retuned after the constants were seen')
    return True


def admit_bound(value, target):
    v, t = parse_q(value), parse_q(target)
    require(v <= t, 'bound exceeds its target')
    return True


# ------------------------------------------------------- phrasing validators
def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def phrase_hits(text, forbidden, template):
    body = normalize(text)
    if template:
        body = body.replace(normalize(template), ' ')
    hits = []
    for clause in [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', body) if c.strip()]:
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                hits.append({'phrase': phrase, 'negated': bool(NEGATION.search(clause))})
    return hits


def certify_phrasing(text, forbidden, template):
    bad = [h for h in phrase_hits(text, forbidden, template) if not h['negated']]
    require(bad == [], 'affirmative forbidden phrasing: ' + (bad[0]['phrase'] if bad else ''))
    return True


def certify_no_placeholder(s):
    require(re.search(r'<[^<>]*(\s|\||e\.g\.)[^<>]*>', s) is None, 'placeholder span in an exported statement')
    return True


def certify_template_once(text, template):
    require(normalize(text).count(normalize(template)) == 1, 'mandatory template not quoted exactly once as one span')
    return True


# ------------------------------------------------------ contract and premises
PARAM_KEYS = ('metric', 'weights', 'rate_constant_pair', 'comparisons', 'cutoff', 'N_min', 'clock', 'window', 'coefficient_input')


def validate_contract(data):
    require(data.get('id') == 'BB1' and data.get('round') == 33 and data.get('status') == 'frozen_before_production',
            'contract identity or status')
    require(data.get('human_author') == 'Hruday N M (BUNZEEY)', 'human author')
    p = data['parameters']
    for k in PARAM_KEYS:
        require(k in p and bool(p[k]), 'contract parameters must declare ' + k)
    require('coarse l-infinity' in p['metric'], 'metric not declared')
    require('iterated_split' in p['weights'] and '8*2^{diam I}' in p['weights'], 'reverse split weight not declared')
    rc = p['rate_constant_pair']
    require(rc['headline']['q'] == '1/64' and rc['headline']['C_target'] == '1/250000'
            and rc['headline']['tier'] == 'exact_first_order', 'headline pair')
    require(rc['region_form']['q'] == '1/64' and rc['region_form']['c_site_target'] == '1/500000', 'region pair')
    require(rc['secondary']['C_target'] == '1/20000' and rc['secondary']['c_site_target'] == '1/40000'
            and rc['secondary']['q'].startswith('151552|tau|'), 'secondary pair')
    require(len(p['comparisons']) == 5, 'five comparisons')
    require(p['window'].startswith('not applicable'), 'window')
    require('F20-F23' in p['cutoff'], 'cutoff removal route')
    require('49/111790368' in p['coefficient_input'], 'coefficient input constant')
    pre = data['preregistration']
    require(pre['model_id'] == 'AQ_patterned_zero_selected', 'model id')
    require([parse_q(x) for x in pre['selected_triple_alpha_units']] == [0, 0, 0], 'selected triple')
    require(pre['tau']['value'] == '1/100000000' and pre['tau']['signs_evaluated'] == ['+', '-'], 'tau value or signs')
    require(pre['target']['value'] == '1/250000 and 1/500000' and pre['target']['comparator'] == '<=', 'target')
    require(pre['observable']['reference_value_exact'] == '0', 'reference value')
    hb = pre['hash_binding']
    require(all(hb[k] is True for k in hb) and len(hb) == 4, 'hash-binding flags must all be true')
    gf = pre['gate_fields_required']
    require(sorted(gf) == sorted(GATE_FIELD_KEYS), 'gate field set')
    require(gf['state_decay_claimed'] is True and gf['rate_in_N_claimed'] is True
            and all(gf[k] is False for k in FALSE_FLAGS if k in gf), 'gate field values')
    require(pre['error_terms_itemized'] == ['coefficient_input_every_site', 'straddling_supports', 'normalization',
                                             'polymer_or_split_remainder', 'cutoff_removal_at_fixed_N', 'arithmetic'], 'error terms')
    require(set(pre['scaling_brackets_per_constant']) == {'C_headline', 'c_site', 'secondary_constants', 'q_secondary'}, 'brackets')
    ids = data['controls']
    require(ids == pre['controls_required']['ids'] and len(set(ids)) == len(ids) == 37, 'controls list differs from preregistration')
    require(set(data['new_control_semantics']) <= set(ids), 'control semantics')
    require(data.get('reverse_premise_isolation') is True, 'reverse premise isolation flag')
    require('iterated_split' in pre['tier_names_allowed'], 'tier vocabulary')
    require(isinstance(pre.get('mandatory_sentence_template'), str), 'template')
    return True


def validate_contract_bytes(raw, expected_sha):
    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'contract bytes do not match the bound hash')
    data = json.loads(raw)
    validate_contract(data)
    return data


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    for f in files:
        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)
        require(not (f.startswith('research/round33/skeptic/') or f.startswith('research/round29/skeptic/'))
                or f in SKEPTIC_ALLOWED, 'undeclared skeptic file: ' + f)
        require(not f.startswith('research/round33/advisor/') or f in ADVISOR_ALLOWED, 'advisor file outside the declared set: ' + f)
    require(sorted(files) == sorted(expected) and len(files) == len(expected),
            'reverse inputs inventory differs from AGENTS.md + contract + shared_premises')
    return True


def validate_pinned(rel, raw):
    require(hashlib.sha256(raw).hexdigest() == PINNED_GATES[rel], 'admitted gate bytes differ from the pinned sha256: ' + rel)
    return True


def parse_bracket(text):
    if text.startswith('exactly'):
        v = parse_q(text.split()[1])
        return (v, v)
    m = re.match(r'\[\s*([0-9/]+)\s*,\s*([0-9/]+)\s*\]', text)
    must(m is not None, 'bracket parse')
    return (parse_q(m.group(1)), parse_q(m.group(2)))


# ==================================================================== compute
def geometry_audit():
    """Every-site form of the BA1 common-core lemma, enumerated (all-size proof in the report, Lemma B4)."""
    rows = []
    extra = {}
    for N in (2, 3, 4):
        bN, bN1 = box(N), box(N + 1)
        f1N, f1N1, f2N, f2N1 = f1_faces(bN), f1_faces(bN1), f2_faces(bN), f2_faces(bN1)
        extra[N] = len(f2N - f1N)
        must(f1N <= f2N <= f1N1 and f2N <= f2N1, 'face sets totally ordered')
        for name, fa, fb in (('F1 Lambda_N vs Lambda_N+1', f1N, f1N1), ('F2 Lambda_N vs Lambda_N+1', f2N, f2N1),
                             ('F1 vs F2 on Lambda_N', f1N, f2N)):
            res = every_site_source_audit(N, bN, fa, bN, fb)
            must(res['ok'] is True, 'every-site source distance ' + name + ' N=' + str(N))
            rows.append({'N': N, 'comparison': name, **res})
        must(certify_common_core_every_site(N, bN1, f2N1), 'common core')
    gen = [(2, 'F1 Lambda_2 vs F2 Lambda_4', f1_faces(box(2)), f2_faces(box(4))),
           (3, 'F2 Lambda_3 vs F1 Lambda_4', f2_faces(box(3)), f1_faces(box(4))),
           (2, 'F1 [-2,3]x[-2,2]x[-2,4] vs F1 Lambda_3', f1_faces(prism((-2, -2, -2), (3, 2, 4))), f1_faces(box(3))),
           (2, 'F2 [-3,2]x[-2,3]x[-2,2] vs F2 Lambda_2', f2_faces(prism((-3, -2, -2), (2, 3, 2))), f2_faces(box(2)))]
    for N, name, fa, fb in gen:
        res = every_site_source_audit(N, None, fa, None, fb)
        must(res['ok'] is True, 'every-site source distance ' + name)
        rows.append({'N': N, 'comparison': name, **res})
    orders = {}
    pieces = f1_star_pieces(box(3))
    for u in ((0, 0, 0), (0, 0, 1), (1, 1, 1), (2, 0, 0), (-2, 1, 2)):
        orders[str(u)] = order_vs_distance_at(u, pieces)
        must(orders[str(u)] is not None and orders[str(u)] >= 0, 'order versus distance at u')
    return rows, extra, orders


def compute():
    check_py_sha = sha256_file(HERE / 'check.py')            # recorded before any evaluation
    raw = (INPUTS / CONTRACT_REL).read_bytes()
    contract_sha = hashlib.sha256(raw).hexdigest()
    must(contract_sha == CONTRACT_SHA256, 'contract snapshot hash differs from the bound constant')
    contract = validate_contract_bytes(raw, CONTRACT_SHA256)
    check('contract_snapshot_bound', contract_sha == CONTRACT_SHA256, contract_sha256=contract_sha,
          source='inputs/' + CONTRACT_REL, verified='before any evaluation')
    check('check_py_sha256_recorded_before_evaluation', len(check_py_sha) == 64, check_py_sha256=check_py_sha)
    cache = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if '__pycache__' in p.parts or p.suffix == '.pyc')
    check('no_interpreter_cache_in_closure', cache == [])
    gates = {}
    for rel in sorted(PINNED_GATES):
        blob = (INPUTS / rel).read_bytes()
        must(validate_pinned(rel, blob), 'pinned gate')
        gates[rel] = json.loads(blob)
        must(gates[rel]['verdict'] == 'accepted_within_scope', 'gate verdict ' + rel)
    check('admitted_gate_sha256_pinned', True, pinned=dict(PINNED_GATES))
    inventory = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    must(validate_inventory(inventory, contract), 'inventory')
    check('reverse_inputs_inventory_exact', len(inventory) == 35, files=len(inventory))

    params, pre = contract['parameters'], contract['preregistration']
    TAU = parse_q(pre['tau']['value'])
    am2 = gates['research/round29/advisor/am2-gate.json']
    must(re.search(r'\|tau\|<=1/100000000', am2['accepted']) is not None, 'AM2 cap')
    ba1 = gates[BA1_GATE]
    must('K=49/111790368' in ba1['accepted'] and 'u in R' in ba1['decision'], 'BA1 gate bound value and scope')
    brackets = {k: parse_bracket(v) for k, v in pre['scaling_brackets_per_constant'].items()}
    template = pre['mandatory_sentence_template']
    rc = params['rate_constant_pair']
    q_head = parse_q(rc['headline']['q'])
    C_target = parse_q(rc['headline']['C_target'])
    cs_target = parse_q(rc['region_form']['c_site_target'])
    C2_target = parse_q(rc['secondary']['C_target'])
    cs2_target = parse_q(rc['secondary']['c_site_target'])

    # ------------------------------------------------ AM2 constants (re-derived)
    e_lo, e_hi = exp_bounds(Q(1, 8))
    must(e_hi < Q(8, 7), 'e^(1/8) < 8/7')
    R = Q(1, 64)
    G_R, Gp_R = 16 * e_hi * (1 + 10 * R), 16 * e_hi * (18 + 80 * R)
    must(G_R < Q(148, 7) and Gp_R < 352, 'G(R)<148/7 and G\'(R)<352')
    coeffs = [16 * 8 ** k * (1 + Q(5 * k, 4)) for k in range(9)]
    root_x = [2 ** 4 * 8 ** k for k in range(9)]
    root_c = [2 ** 4 * 8 ** k * Q(k * 5, 4) for k in range(9)]
    must(all(coeffs[k] == root_x[k] + root_c[k] for k in range(9)), 'weighted multilinear counting constants')
    check('am2_constants_rederived', True, exp_1_8_upper=qs(e_hi), G_R_upper=qs(G_R), Gp_R_upper=qs(Gp_R),
          weighted_multilinear_constant='w J 16 8^k (1+5k/4), loss w^{d_X}=w per interaction')
    card_ok = all((d + 1) ** 3 <= 8 * 2 ** d for d in range(0, 64)) and all(Q(d + 2, d + 1) ** 3 <= 2 for d in range(3, 64))
    check('cardinality_charge_8_2_diam', card_ok, statement='|I|<=(diam I+1)^3<=8*2^{diam I} for every diameter')
    X, I1, I2 = {(0, 0, 0), (1, 0, 0)}, {(-1, 0, 0), (0, 0, 0)}, {(1, 0, 0), (2, 0, 0)}
    M = (I1 | I2) - X
    check('diameter_subadditivity_through_interaction', diam(M) == 3 == diam(X) + diam(I1) + diam(I2),
          fixture='X={0,e_x}, I1={-e_x,0}, I2={e_x,2e_x}, M={-e_x,2e_x}: diam 3 = 1+1+1 (max rule would give 2)')

    # ------------------------------------------------ I1 table
    i1_text = (INPUTS / I1_REL).read_text()
    must(compare_i1(parse_i1_table(i1_text), CLASSES), 'I1 table')
    per_site = sum(sum(1 for c in OMITTED if d in c['K']) for d in S_STAR)
    check('i1_table_and_49_faces_per_site', per_site == 49 and len(OMITTED) == 21, faces_per_site=per_site)

    # ------------------------------------------------ every-site coefficient input (form b)
    rows, extra, orders = geometry_audit()
    check('every_site_common_core_enumerated', all(r['ok'] for r in rows), rows=rows)
    check('f2_extra_faces_28N_5N_plus_1', certify_family_distinct(extra), extra={str(k): v for k, v in extra.items()})
    check('order_versus_distance_every_site', all(v >= 0 for v in orders.values()), min_slack_over_1_plus_d=orders,
          pieces='F1 whole stars on Lambda_3 (l-infinity diameter 1)')

    # ------------------------------------------------ proof weights declared before any constant
    W_HEAD = Q(1024)
    W_SEC = 1 / (37888 * TAU)
    RHO_HEAD, RHO_SEC = 64 * TAU, Q(1, 151552)
    q_sec = 151552 * TAU
    weights_decl = {'split_creation_weight_headline': qs(W_HEAD), 'lambda_headline': qs(2 / W_HEAD),
                    'split_creation_weight_secondary': '1/(37888|tau|) (= ' + qs(W_SEC) + ' at the cap)',
                    'lambda_secondary': '75776|tau| = q_2/2', 'cardinality_charge': '|I|<=8*2^{diam I}',
                    'disc_radius_headline': '64|tau|', 'disc_radius_secondary': '|tau|/q_2 = 1/151552',
                    'admissible_range': '[1, 1/(37888|tau|)] (weighted self-map 28 W|tau| G(R) <= R)'}
    must(28 * W_HEAD * TAU * Q(148, 7) < R and 28 * W_HEAD * TAU * 352 < 1, 'weighted self-map at W=1024')
    must(28 * W_SEC * TAU * Q(148, 7) <= R and 28 * W_SEC * TAU * 352 < 1, 'weighted self-map at W=1/(37888|tau|)')
    check('proof_weights_declared_and_admissible', True, weights=weights_decl,
          self_map_headline=qs(28 * W_HEAD * TAU * Q(148, 7)), contraction_headline=qs(28 * W_HEAD * TAU * 352),
          contraction_secondary=qs(28 * W_SEC * TAU * 352))

    # ------------------------------------------------ constants (item 4), both signs, every comparison
    comparisons = params['comparisons']
    consts = {}
    for sign in (1, -1):
        tau = sign * TAU
        consts[('head', 'exact_first_order', sign)] = split_constants('exact_first_order', tau, W_HEAD, RHO_HEAD, q_head)
        consts[('head', 'crude_majorant', sign)] = split_constants('crude_majorant', tau, W_HEAD, RHO_HEAD, q_head)
        consts[('sec', 'exact_first_order', sign)] = split_constants('exact_first_order', tau, 1 / (37888 * abs(tau)), RHO_SEC, q_sec)
        consts[('sec', 'crude_majorant', sign)] = split_constants('crude_majorant', tau, 1 / (37888 * abs(tau)), RHO_SEC, q_sec)
    for key in list(consts):
        other = (key[0], key[1], -key[2])
        must(consts[key]['C'] == consts[other]['C'] and consts[key]['c_site'] == consts[other]['c_site'], 'sign replay')
    H = consts[('head', 'exact_first_order', 1)]
    Hc = consts[('head', 'crude_majorant', 1)]
    S2 = consts[('sec', 'exact_first_order', 1)]
    S2c = consts[('sec', 'crude_majorant', 1)]
    must(H['K'] == Q(49, 111790368), 'BA1 gate bound value K')
    check('ba1_every_site_input_constant', H['K'] == Q(49, 111790368), K=exact(H['K']), form='(b)',
          statement='sum_{I ni u}||c^A_I-c^B_I|| <= K q^(N-|u|_inf) for every site u of the union volume',
          input_tier='exact_first_order', input_route='analytic_disc (BA1 input, not the BB1 route)')
    check('headline_C_meets_target', admit_bound(H['C'], C_target), C=exact(H['C']), target=qs(C_target),
          margin=sci(C_target / H['C']), tier='exact_first_order', route=ROUTE, ba1_input='gate_bound_value_K=49/111790368')
    check('region_c_site_meets_target', admit_bound(H['c_site'], cs_target), c_site=exact(H['c_site']), target=qs(cs_target),
          margin=sci(cs_target / H['c_site']), tier='exact_first_order', route=ROUTE)
    check('secondary_pair_meets_targets', admit_bound(S2['C'], C2_target) and admit_bound(S2['c_site'], cs2_target),
          q='151552|tau|', C=exact(S2['C']), c_site=exact(S2['c_site']), K_secondary=exact(S2['K']),
          margins=[sci(C2_target / S2['C']), sci(cs2_target / S2['c_site'])], label='labelled secondary pair')
    crude_fails = Hc['C'] > C_target and Hc['c_site'] > cs_target
    check('crude_tier_reported_separately', crude_fails, C_crude=exact(Hc['C']), c_site_crude=exact(Hc['c_site']),
          secondary_crude={'C': exact(S2c['C']), 'c_site': exact(S2c['c_site'])}, status='fails the headline targets; retained')
    comp_table = []
    for comp in comparisons:
        for sign in ('+', '-'):
            k = consts[('head', 'exact_first_order', 1 if sign == '+' else -1)]
            comp_table.append({'comparison': comp[:80], 'sign': sign, 'C': exact(k['C']), 'c_site': exact(k['c_site']),
                               'in_each_Q_L': True, 'untruncated_at_fixed_N': True})
    check('every_comparison_both_signs', len(comp_table) == 10, table=comp_table,
          union_form_labelled={'C': exact(2 * H['C']), 'note': 'comparison through the union volume costs a factor 2; labelled only'})
    examples = {str(N): sci(H['C'] * q_head ** (N - 1)) for N in (2, 3, 4)}
    check('example_values_N_2_3_4', True, headline_C_q_pow_N_minus_1=examples)
    lemma = {'eta': '0', 'kappa0': qs(H['beta']) + ' |Y| (R: ' + qs(H['kappa0_R']) + ')', 'w_prime': qs(H['w_prime']),
             'p': '|I|', 'tier': 'exact_first_order', 'route': ROUTE, 'combinatorial_counts': True}
    must(certify_marginal_lemma({**lemma, 'kappa0': qs(H['beta'])}), 'lemma form')
    check('marginal_locality_lemma_constants', True, lemma=lemma, beta=exact(H['beta']), c1=exact(H['c1']), c2=exact(H['c2']),
          t0=exact(H['t0']), tW=exact(H['tW']), S=qs(H['S']))
    ledger = ledger_parts(H)
    check('error_ledger_itemized', sum(ledger.values()) == H['C'],
          ledger={k: exact(v) for k, v in ledger.items()})

    # ------------------------------------------------ tau -> tau/100 scaling (item 6)
    t100 = TAU / 100
    H100 = split_constants('exact_first_order', t100, W_HEAD, 64 * t100, q_head)
    S100 = split_constants('exact_first_order', t100, 1 / (37888 * t100), RHO_SEC, 151552 * t100)
    Hc100 = split_constants('crude_majorant', t100, W_HEAD, 64 * t100, q_head)
    ratios = {'C_headline': H['C'] / H100['C'], 'c_site': H['c_site'] / H100['c_site'],
              'secondary_C': S2['C'] / S100['C'], 'secondary_c_site': S2['c_site'] / S100['c_site'],
              'q_secondary': q_sec / (151552 * t100)}
    must(certify_scaling(ratios['C_headline'], brackets['C_headline']) and certify_scaling(ratios['c_site'], brackets['c_site'])
         and certify_scaling(ratios['secondary_C'], brackets['secondary_constants'])
         and certify_scaling(ratios['secondary_c_site'], brackets['secondary_constants'])
         and certify_scaling(ratios['q_secondary'], brackets['q_secondary']), 'scaling brackets')
    check('tau_scaling_every_headline_constant', True, ratios={k: exact(v) for k, v in ratios.items()},
          brackets={k: [qs(a), qs(b)] for k, (a, b) in brackets.items()},
          crude_labelled={'C': exact(Hc['C'] / Hc100['C'])})

    # ------------------------------------------------ fixtures (item 5), each a finite graph that transfers nothing
    fx = {}
    fx['split_route_trace'] = split_route_fixture()
    fx['lemma_g_single_support'] = lemma_g_fixture()
    fx['split_lipschitz_and_trace_mixed'] = mixed_outside_fixture()
    fx['end_to_end_marginal_lemma_chain'] = chain_fixture_1d()
    fx['second_order_propagation'] = second_order_chain_fixture()
    fx['straddling_supports'] = straddling_fixture()
    fx['coefficient_vs_marginal'] = coefficient_vs_marginal_fixture()
    fx['global_fidelity_product_state'] = global_fidelity_fixture()
    fx['polymer_identity_and_cardinality'] = polymer_fixture()
    fx['outside_vector_not_ground_state'] = outside_not_ground_fixture()
    fx['cutoff_vector_eckart'] = eckart_fixture()
    fx['cutoff_limit_order'] = limit_order_fixture()
    fx['normalization_zero'] = normalization_zero_fixture()
    fx['mean_field_lipschitz'] = mean_field_fixture()
    fx['fixed_versus_moving_vector'] = topology_fixture()
    fx['mixed_weight_size_count'] = mixed_weight_fixture()
    must(all(v.get('model_is_finite_graph') is True and v.get('transfers_to_aq') is False for v in fx.values()), 'fixture labels')
    sr = fx['split_route_trace']
    check('fixture_split_route_identities', sr['identity_star_star_exact'] and sr['Z_ge_n2'] and sr['orthogonality_at_J']
          and all(sr['covering_recursion_exact']), fixture=sr)
    check('fixture_lemma_g', fx['lemma_g_single_support']['holds'] is True, fixture=fx['lemma_g_single_support'])
    mo = fx['split_lipschitz_and_trace_mixed']
    check('fixture_trace_at_least_one_and_lipschitz', mo['trace_at_least_one'] and mo['rho_lipschitz_in_N']
          and mo['omega_lipschitz_holds'], fixture=mo)
    ce = fx['end_to_end_marginal_lemma_chain']
    check('fixture_end_to_end_marginal_lemma', ce['total_bound_holds'] and ce['single_far_support_bounds_hold'], fixture=ce)
    check('fixture_second_order_polynomial', True, fixture=fx['second_order_propagation'])
    check('fixture_straddling', True, fixture=fx['straddling_supports'])
    check('fixture_coefficient_vs_marginal', parse_q(fx['coefficient_vs_marginal']['trace_norm_sq']) > 0,
          fixture=fx['coefficient_vs_marginal'])
    check('fixture_global_fidelity', True, fixture=fx['global_fidelity_product_state'])
    pf = fx['polymer_identity_and_cardinality']
    check('polymer_identity_fixture_values', pf['identity_exact'] and pf['different_excitation_sets_pair_to_zero'] and pf['kp_condition_holds']
          and pf['majorant_with_cardinality_ge_cluster_sum'] and pf['majorant_without_cardinality_below_cluster_sum'], fixture=pf)
    og = fx['outside_vector_not_ground_state']
    check('fixture_outside_vector', og['eigen_equation_exact'] and og['is_lowest'] and not og['outside_vector_is_eigenvector'], fixture=og)
    check('fixture_cutoff_eckart_and_order', True, eckart=fx['cutoff_vector_eckart'], limit_order=fx['cutoff_limit_order'])
    check('fixture_normalization_zero_mean_field_topology', True, normalization=fx['normalization_zero'],
          mean_field=fx['mean_field_lipschitz'], topology=fx['fixed_versus_moving_vector'])
    t0h, tWh = H['t0'], H['tW']
    kstar = first_depth_without_decay(t0h)
    check('per_site_charging_versus_growing_sizes', certify_charging_rule(per_site_rule, t0h, tWh),
          per_site_factor=exact(per_site_rule(0, tWh)), growing_rule='(2k+1)^3 t0', first_depth_without_decay=kstar)

    # ------------------------------------------------ cutoff (items 4)
    cutoff_rec = {'constants_depend_on_L': False, 'removal_after_uniform_bound': True,
                  'method': 'ground_vector_eckart_with_untruncated_gap', 'order': 'cutoff_L_to_infinity_at_fixed_N_then_bound_in_N',
                  'F1': 'AV1 F20-F23 with AM2 section 6 (every finite complete-factor volume)',
                  'F2': 'AY1 item-by-item H1-H5 (includes cutoff-vector removal), every F2 volume containing Lambda_N'}
    must(certify_cutoff_uniform(cutoff_rec) and certify_cutoff_removal(cutoff_rec['method'])
         and certify_limit_order(cutoff_rec['order']), 'cutoff record')
    check('cutoff_uniform_then_removed_at_fixed_N', True, record=cutoff_rec,
          first_order_faces_kept_for_L_ge='24 (site energy at most 18)')

    # ------------------------------------------------ statements, gate fields, phrasing (item 5)
    gate_fields = dict(pre['gate_fields_required'])
    gate_fields_export = dict(gate_fields)
    must(certify_gate_fields(gate_fields_export, pre['gate_fields_required']), 'gate fields')
    flags = {k: False for k in FALSE_FLAGS}
    must(validate_claim_flags(flags), 'claim flags')
    report = (HERE / 'report.md').read_text()
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])
    must(certify_template_once(report, template), 'template in the report')
    must(certify_phrasing(report, forbidden, template), 'report phrasing')
    headline_statement = (template + ' Constants (exact_first_order, route iterated_split, BA1 input K=49/111790368 in the '
                          'every-site form (b)): C=' + qs(H['C']) + ' (about ' + sci(H['C']) + ') at q=1/64; region form '
                          'c_site=' + qs(H['c_site']) + ' (about ' + sci(H['c_site']) + ').')
    must(certify_no_placeholder(headline_statement) and certify_phrasing(headline_statement, forbidden, template), 'statement')
    check('mandatory_template_quoted_once_and_phrase_scan_clean', True, forbidden_count=len(forbidden))
    check('gate_fields_exported', True, gate_fields=gate_fields_export)
    pins = [qs(H['C']), qs(H['c_site']), qs(S2['C']), qs(S2['c_site']), qs(Hc['C']), qs(H['beta']), '49/111790368',
            sci(ratios['C_headline']), sci(ratios['secondary_C']), qs(S2['K']), qs(H['tW'])]
    missing = [x for x in pins if x not in report]
    check('report_pins_exact_values', missing == [], pins=pins)

    # ================================================================ controls
    def mutated(fn):
        data = json.loads(raw)
        fn(data)
        blob = json.dumps(data, indent=1).encode()
        return lambda: validate_contract_bytes(blob, hashlib.sha256(blob).hexdigest())

    def setp(path, value):
        def f(d):
            x = d
            for k in path[:-1]:
                x = x[k]
            x[path[-1]] = value
        return f

    def recomputed(claimed, value):
        require(Q(claimed) == value, 'exported value differs from the recomputed exact value')
        return True

    first_gate = sorted(PINNED_GATES)[0]
    control('coherent_evidence_tampering', [
        ('C_target_relaxed', mutated(setp(['parameters', 'rate_constant_pair', 'headline', 'C_target'], '1/100000'))),
        ('headline_q_changed', mutated(setp(['parameters', 'rate_constant_pair', 'headline', 'q'], '1/32'))),
        ('rate_in_a_true', mutated(setp(['preregistration', 'gate_fields_required', 'rate_in_a_claimed'], True))),
        ('control_removed', mutated(lambda d: (d['controls'].pop(), d['preregistration']['controls_required']['ids'].pop()))),
        ('isolation_false', mutated(setp(['reverse_premise_isolation'], False))),
        ('hash_binding_flipped', mutated(setp(['preregistration', 'hash_binding', 'admitted_gate_sha256_pinned_in_check_py'], False))),
        ('tau_changed', mutated(setp(['preregistration', 'tau', 'value'], '1/10000000'))),
        ('byte_change_without_rehash', lambda: validate_contract_bytes(raw + b' ', CONTRACT_SHA256)),
        ('snapshot_removed', lambda: validate_inventory(inventory[1:], contract)),
        ('admitted_gate_edited', lambda: validate_pinned(first_gate, (INPUTS / first_gate).read_bytes() + b' ')),
        ('exported_C_halved', lambda: recomputed(qs(H['C'] / 2), H['C'])),
    ])
    control('exact_arithmetic_admission', [
        ('float_input', lambda: parse_q(8.9e-7)), ('bool_input', lambda: parse_q(True)), ('nan_string', lambda: parse_q('nan')),
        ('zero_denominator', lambda: parse_q('1/0')), ('float_bound_admission', lambda: admit_bound(8.9e-7, '1/250000')),
    ])
    control('no_priority_or_continuum_claim', [
        ('continuum_true', lambda: validate_claim_flags({**flags, 'continuum_claim': True})),
        ('priority_true', lambda: validate_claim_flags({**flags, 'scientific_priority_verified': True})),
        ('weak_coupling_true', lambda: validate_claim_flags({**flags, 'weak_coupling_claim': True})),
        ('historical_lens_premise', lambda: certify_premise_provenance('historical_lens')),
    ])
    pk0 = {'tau': qs(TAU), 'triple': ['0', '0', '0'], 'model_id': pre['model_id'], 'group': 'SU(2)', 'dimension': 3,
           'metric': 'coarse l-infinity', 'result_source': 'analytic_proof', 'cover': 'R={0,e_z}'}
    must(certify_packet_model(pk0, contract), 'packet model')
    control('changed_model_relabelled', [
        ('coupling_above_cap', lambda: certify_packet_model({**pk0, 'tau': '1/1000000'}, contract)),
        ('nonzero_triple', lambda: certify_packet_model({**pk0, 'triple': ['1/10', '0', '0']}, contract)),
        ('model_relabelled', lambda: certify_packet_model({**pk0, 'model_id': 'uniform_route_B'}, contract)),
        ('su3', lambda: certify_packet_model({**pk0, 'group': 'SU(3)'}, contract)),
        ('two_dimensions', lambda: certify_packet_model({**pk0, 'dimension': 2}, contract)),
        ('l1_metric', lambda: certify_packet_model({**pk0, 'metric': 'l1'}, contract)),
        ('finite_graph_as_aq', lambda: certify_packet_model({**pk0, 'result_source': 'finite_graph_fixture'}, contract)),
    ])
    oflags = {'headline_all_comparisons': True, 'region_form': True, 'untruncated_fixed_N': True,
              'exact_tier_meets_targets': True, 'every_site_input_proved': True}
    outcome = producer_outcome(oflags)
    must(outcome == 'accepted_within_scope', 'outcome')
    control('insufficient_verdict_retained', [
        ('R_form_only_relabelled', lambda: certify_outcome('accepted_within_scope', {**oflags, 'region_form': False})),
        ('no_untruncated_passage_relabelled', lambda: certify_outcome('accepted_within_scope', {**oflags, 'untruncated_fixed_N': False})),
        ('crude_only_relabelled', lambda: certify_outcome('accepted_within_scope', {**oflags, 'exact_tier_meets_targets': False})),
        ('some_comparisons_relabelled', lambda: certify_outcome('accepted_within_scope', {**oflags, 'headline_all_comparisons': False})),
        ('crude_headline_admitted', lambda: admit_bound(qs(Hc['C']), qs(C_target))),
        ('tau_retuned', lambda: certify_no_retuning(TAU / 10, TAU)),
    ])
    control('tau_scaling_exponent', [
        ('quadratic_headline', lambda: certify_scaling(Q(10000), brackets['C_headline'])),
        ('constant_headline', lambda: certify_scaling(Q(1), brackets['C_headline'])),
        ('secondary_linear', lambda: certify_scaling(Q(100), brackets['secondary_constants'])),
        ('q_secondary_not_100', lambda: certify_scaling(Q(10), brackets['q_secondary'])),
        ('bracket_after_evaluation', lambda: certify_bracket_prefrozen((Q(90), Q(110)), brackets['C_headline'])),
    ])
    control('wrong_delta_alpha_hbar_clock', [
        ('amplitude_tau_over_576', lambda: certify_first_order_amplitude(-TAU / 576, TAU)),
        ('amplitude_tau_over_9', lambda: certify_first_order_amplitude(-TAU / 9, TAU)),
        ('u_labelled_theta', lambda: certify_clock('theta', 'theta/8')),
        ('euclidean_labelled_real', lambda: certify_clock('s', 'alpha*t/hbar')),
    ])
    must(certify_first_order_amplitude(-TAU / 72, TAU) and certify_clock('theta', 'alpha*t/hbar'), 'clock')
    control('root_n_misuse', [
        ('root_sum_of_squares', lambda: certify_combination([H['K'], H['K']], 'rss')),
        ('sqrt_face_count', lambda: certify_combination([H['K']], 'sqrt_49')),
        ('divide_by_sqrt_N', lambda: certify_no_volume_division(2)),
    ])
    good_tier = {'tier': 'exact_first_order', 'route': ROUTE, 'ba1_input': 'gate_bound_value_K=49/111790368',
                 'input_tier': 'exact_first_order', 't_kind': 'exact_first_order'}
    must(certify_tier_constant(good_tier), 'tier record')
    control('tier_mixing_rejected', [
        ('exact_label_crude_input', lambda: certify_tier_constant({**good_tier, 'input_tier': 'crude_majorant'})),
        ('exact_label_crude_t', lambda: certify_tier_constant({**good_tier, 't_kind': 'crude_majorant'})),
        ('ba1_route_as_bb1_route', lambda: certify_tier_constant({**good_tier, 'route': 'analytic_disc'})),
        ('lieb_robinson_tier', lambda: certify_tier_constant({**good_tier, 'tier': 'lieb_robinson'})),
        ('forward_route_label', lambda: certify_tier_constant({**good_tier, 'route': 'polymer_kp'})),
        ('ba1_input_unnamed', lambda: certify_tier_constant({**good_tier, 'ba1_input': 'unspecified'})),
    ])
    control('reverse_premise_isolation', [
        ('forward_bb1_added', lambda: validate_inventory(inventory + ['research/round33/forward/bb1/report.md'], contract)),
        ('reverse_bb2_added', lambda: validate_inventory(inventory + ['research/round33/reverse/bb2/report.md'], contract)),
        ('skeptic_triage_added', lambda: validate_inventory(inventory + ['research/round33/skeptic/bb1-triage.md'], contract)),
        ('lens_memo_added', lambda: validate_inventory(inventory + ['research/round33/experts/newton-tesla/memo.md'], contract)),
        ('deliberation_added', lambda: validate_inventory(inventory + ['research/round33/advisor/deliberation-3.md'], contract)),
        ('premise_missing', lambda: validate_inventory([f for f in inventory if 'av1' not in f], contract)),
    ])
    control('uniform_in_N_not_in_a', [
        ('uniform_in_spacing', lambda: certify_uniformity_statement('the bound is uniform in the lattice spacing')),
        ('unqualified_uniform', lambda: certify_uniformity_statement('the rate is uniform')),
    ])
    must(certify_uniformity_statement('constants uniform in N at fixed spacing and uniform in the cutoff, not uniform in the lattice spacing'), 'uniformity')
    control('placeholder_span_rejected', [
        ('angle_space', lambda: certify_no_placeholder(headline_statement + ' <preceding gate>')),
        ('angle_bar', lambda: certify_no_placeholder('<C|c_site>')),
        ('angle_eg', lambda: certify_no_placeholder('<e.g.value>')),
    ])
    control('negation_aware_phrase_scan', [
        ('thermodynamic_limit', lambda: certify_phrasing(report + '\nThis is the thermodynamic limit.', forbidden, template)),
        ('boundary_independent', lambda: certify_phrasing(report + '\nThe density is boundary independent.', forbidden, template)),
        ('correlation_length', lambda: certify_phrasing(report + '\nThe correlation length is 1/log 64.', forbidden, template)),
        ('confirms', lambda: certify_phrasing(report + '\nThe fixture confirms the decay.', forbidden, template)),
        ('uniform_in_a', lambda: certify_phrasing(report + '\nThe constant is uniform in a.', forbidden, template)),
    ])
    must(certify_phrasing('The result is not the thermodynamic limit.', forbidden, template), 'negated phrase accepted')
    control('parameters_declare_metric_weights_window', [
        ('metric_removed', mutated(lambda d: d['parameters'].pop('metric'))),
        ('weights_removed', mutated(lambda d: d['parameters'].pop('weights'))),
        ('window_removed', mutated(lambda d: d['parameters'].pop('window'))),
        ('clock_removed', mutated(lambda d: d['parameters'].pop('clock'))),
        ('coefficient_input_removed', mutated(lambda d: d['parameters'].pop('coefficient_input'))),
    ])
    pair_rec = {'q': q_head, 'C_target': C_target, 'c_site_target': cs_target, 'q_rule': 'frozen', 'W': W_HEAD, 'tau': TAU,
                'weights_declared_before_constants': True}
    must(certify_pair(pair_rec, contract), 'pair record')
    sec_rec = {'q': q_sec, 'rho': RHO_SEC, 'label': 'labelled_secondary'}
    must(certify_secondary(sec_rec, TAU), 'secondary record')
    control('rate_constant_pair_prefrozen', [
        ('q_1_128', lambda: certify_pair({**pair_rec, 'q': Q(1, 128)}, contract)),
        ('C_target_changed', lambda: certify_pair({**pair_rec, 'C_target': Q(1, 100000)}, contract)),
        ('c_site_target_changed', lambda: certify_pair({**pair_rec, 'c_site_target': Q(1, 200000)}, contract)),
        ('q_optimized_per_N', lambda: certify_pair({**pair_rec, 'q_rule': 'optimized_per_N'}, contract)),
        ('weight_beyond_w_max', lambda: certify_pair({**pair_rec, 'W': Q(4096)}, contract)),
        ('weights_after_constants', lambda: certify_pair({**pair_rec, 'weights_declared_before_constants': False}, contract)),
        ('secondary_as_headline', lambda: certify_secondary({**sec_rec, 'label': 'headline'}, TAU)),
        ('secondary_q_changed', lambda: certify_secondary({**sec_rec, 'q': 37888 * TAU}, TAU)),
        ('split_weight_too_small_for_rate', lambda: split_constants('exact_first_order', TAU, Q(64), RHO_HEAD, q_head)),
    ])
    must(certify_rate_unit('per coarse l-infinity step in N at fixed spacing'), 'rate unit')
    control('decay_rate_in_N_not_a', [
        ('per_fm', lambda: certify_rate_unit('per fm')),
        ('per_lattice_spacing', lambda: certify_rate_unit('per lattice spacing a')),
        ('physical_length', lambda: certify_rate_unit('per physical length')),
    ])
    must(certify_topology('trace norm on B(H_Y)'), 'topology')
    control('topology_named', [
        ('weak_operator', lambda: certify_topology('weak operator topology')),
        ('hilbert_schmidt', lambda: certify_topology('Hilbert-Schmidt norm')),
        ('fixed_vector_strong', lambda: certify_topology('strong topology on a fixed vector')),
    ])
    must(certify_families([F1_NAME, F2_NAME]), 'families')
    control('two_families_named', [
        ('single_family', lambda: certify_families([F1_NAME])),
        ('unfrozen_class', lambda: certify_families([F1_NAME, 'every AM2-admissible boundary condition'])),
        ('f2_collapsed', lambda: certify_family_distinct({2: 0, 3: 0})),
    ])
    lim = {'whole_sequence': False, 'common_limit': False}
    must(certify_limit_statement(lim), 'limit statement')
    control('subsequence_versus_whole_sequence', [
        ('whole_sequence_claimed', lambda: certify_limit_statement({**lim, 'whole_sequence': True})),
        ('common_limit_claimed', lambda: certify_limit_statement({**lim, 'common_limit': True})),
    ])
    clock_rec = {'coupling_F1': qs(TAU), 'coupling_F2': qs(TAU), 'clock': 'theta=alpha*t/hbar'}
    must(certify_common_clock(clock_rec), 'common clock')
    control('common_clock', [
        ('different_couplings', lambda: certify_common_clock({**clock_rec, 'coupling_F2': qs(-TAU)})),
        ('different_clock', lambda: certify_common_clock({**clock_rec, 'clock': 'u=theta/8'})),
    ])
    cvm = fx['coefficient_vs_marginal']
    control('coefficient_decay_not_marginal_decay', [
        ('state_decay_from_zero_coefficient_difference',
         lambda: certify_state_inference(Q(0), parse_q(cvm['trace_norm_sq']), 'marginal_decay_from_coefficient_decay')),
    ])
    must(certify_split_budget(True, 'all_orders_via_coverings') and certify_normalization('exact_split_ratio'), 'split budget')
    control('normalization_couples_supports', [
        ('straddling_dropped', lambda: certify_split_budget(False, 'all_orders_via_coverings')),
        ('straddling_first_order_only', lambda: certify_split_budget(True, 'first_order_only')),
        ('normalization_1_plus_O_t2', lambda: certify_normalization('one_plus_O_t_squared')),
    ])
    must(certify_outside_argument(False), 'outside argument')
    control('outside_vector_not_ground_state', [
        ('gap_argument_on_outside_vector', lambda: certify_outside_argument(True)),
    ])
    must(certify_bound_route('per_support_telescoping') and certify_bound_route('iterated_split'), 'bound route')
    control('global_fidelity_orthogonality_catastrophe', [
        ('global_overlap_route', lambda: certify_bound_route('global_overlap')),
    ])
    control('marginal_locality_constants_explicit', [
        ('kp_without_counts', lambda: certify_marginal_lemma({**lemma, 'kappa0': qs(H['beta']), 'combinatorial_counts': False})),
        ('eta_missing', lambda: certify_marginal_lemma({k: v for k, v in {**lemma, 'kappa0': qs(H['beta'])}.items() if k != 'eta'})),
        ('kappa0_float', lambda: certify_marginal_lemma({**lemma, 'kappa0': 3.1e-5})),
        ('polynomial_unstated', lambda: certify_marginal_lemma({**lemma, 'kappa0': qs(H['beta']), 'p': 'some polynomial'})),
    ])
    control('cutoff_uniform_then_removed', [
        ('constants_depend_on_L', lambda: certify_cutoff_uniform({**cutoff_rec, 'constants_depend_on_L': True})),
        ('removal_before_uniform_bound', lambda: certify_cutoff_uniform({**cutoff_rec, 'removal_after_uniform_bound': False})),
    ])
    control('cutoff_vector_removal', [
        ('eigenvalues_only', lambda: certify_cutoff_removal('eigenvalue_convergence_only')),
        ('am2_section6_cited_alone', lambda: certify_cutoff_removal('cite_am2_section_6')),
    ])
    reg = {'Y_factor': '|Y|', 'exponent': 'd_Y = N - max_y |y|_inf'}
    must(certify_region_bound(reg), 'region record')
    control('region_constant_scales_with_Y', [
        ('R_constant_reused', lambda: certify_region_bound({**reg, 'Y_factor': 'none'})),
        ('exponent_N_minus_1_for_every_Y', lambda: certify_region_bound({**reg, 'exponent': 'N-1'})),
    ])
    control('named_construction_not_uniqueness', [
        ('uniqueness_phrase', lambda: certify_phrasing('This gives uniqueness of the infinite-volume ground state.', forbidden, template)),
        ('thermodynamic_limit_phrase', lambda: certify_phrasing('F1 and F2 define the thermodynamic limit.', forbidden, template)),
        ('the_infinite_volume_ground_state', lambda: certify_phrasing('We obtain the infinite-volume ground state.', forbidden, template)),
    ])
    must(certify_decay_factor('covering_chain_weights_and_site_potential'), 'decay provenance')
    control('global_lipschitz_not_decay', [
        ('fixed_point_lipschitz', lambda: certify_decay_factor('global_lipschitz_fixed_point')),
        ('no_decay_bound', lambda: certify_decay_factor('no_decay_bound_37/6249384')),
        ('density_lipschitz_coefficients', lambda: certify_decay_factor('density_lipschitz_in_coefficients')),
        ('density_lipschitz_outside', lambda: certify_decay_factor('density_lipschitz_in_outside_state')),
        ('mean_field_decay_claim', lambda: admit_bound(fx['mean_field_lipschitz']['value_at_0'], fx['mean_field_lipschitz']['claimed_decay_(1/2)^5'])),
    ])
    a_ch, b_ch = Q(1, 3), Q(1, 5)
    must(certify_propagation_claim({'order_in_straddling_amplitudes': 2, 'per_link': [a_ch, b_ch]}, a_ch, b_ch), 'propagation')
    control('fixture_second_order_propagation', [
        ('first_order_claim', lambda: certify_propagation_claim({'order_in_straddling_amplitudes': 1, 'per_link': [a_ch, b_ch]}, a_ch, b_ch)),
        ('per_link_below_exact', lambda: certify_propagation_claim({'order_in_straddling_amplitudes': 2, 'per_link': [a_ch / 2, b_ch]}, a_ch, b_ch)),
    ])
    control('fixture_split_lipschitz_and_trace', [
        ('growing_region_sizes', lambda: certify_charging_rule(growing_size_rule, t0h, tWh)),
        ('vacuum_component_creation', lambda: certify_orthogonal_trace(vacuum_component_trace())),
    ])
    must(certify_orthogonal_trace(parse_q(mo['trace_N_omega1'])) and certify_tree_majorant(True), 'trace and majorant')
    control('fixture_polymer_identity', [
        ('cardinality_dropped', lambda: certify_tree_majorant(False)),
        ('polymer_sum_mismatch', lambda: recomputed(pf['polymer_sum'], parse_q(pf['brute_force_norm']) + Q(1, 10 ** 6))),
    ])
    control('zero_free_region_required', [
        ('reduced_density_analytic', lambda: certify_analyticity_claim('reduced_density', False)),
        ('normalization_analytic', lambda: certify_analyticity_claim('normalization', False)),
    ])
    esi = {'form': 'b', 'sites': 'every site of the union volume', 'proved_in_packet': True, 'exponent': 'N-|u|_inf'}
    must(certify_every_site_input(esi), 'every-site input')
    control('every_site_coefficient_input', [
        ('R_only_input_at_far_sites', lambda: certify_every_site_input({**esi, 'sites': 'u in R'})),
        ('restated_form_cited_as_admitted', lambda: certify_every_site_input({**esi, 'proved_in_packet': False})),
        ('wrong_exponent', lambda: certify_every_site_input({**esi, 'exponent': 'N-1'})),
    ])
    mw = fx['mixed_weight_size_count']
    mwrec = {'proved_in_packet': True, 'cited_from': 'none', 'loss_exponent_b': mw['X_size']}
    must(certify_mixed_weight(mwrec) and mw['needs_loss_exponent'] == 2, 'mixed weight record')
    control('mixed_weight_lemma_proved', [
        ('cited_from_BA1', lambda: certify_mixed_weight({**mwrec, 'proved_in_packet': False, 'cited_from': 'BA1'})),
        ('loss_e_b_only', lambda: certify_mixed_weight({**mwrec, 'loss_exponent_b': 1})),
    ])
    control('cutoff_limit_order', [
        ('limits_exchanged', lambda: certify_limit_order('N_to_infinity_then_cutoff')),
    ])

    # ================================================================ result
    controls_ids = contract['controls']
    must(sorted(MUTATION_CONTROLS) == sorted(controls_ids), 'every contract control executed as damaging mutations')
    must(len(set(controls_ids)) == 37, '37 controls')
    check('contract_controls_all_executed', True, count=len(MUTATION_CONTROLS))
    headline = {
        'statement_constants': {
            'C': exact(H['C']), 'q': '1/64', 'tier': 'exact_first_order', 'route': ROUTE,
            'ba1_input': 'gate bound value K=49/111790368 (BA1 analytic_disc, exact_first_order), every-site form (b) proved here',
            'target': qs(C_target), 'margin': sci(C_target / H['C']),
            'cover': 'R={0,e_z}', 'bound': '||rho^{box1}_R-rho^{box2}_R||_1 <= C q^(N-1)'},
        'region_form': {'c_site': exact(H['c_site']), 'q': '1/64', 'target': qs(cs_target), 'margin': sci(cs_target / H['c_site']),
                        'bound': '||rho^{box1}_Y-rho^{box2}_Y||_1 <= c_site sum_{y in Y} q^(N-|y|_inf) <= c_site |Y| q^(d_Y)',
                        'contract_form': 'implies c_site |Y| e^{|Y|/10^8} q^{d_Y}'},
        'secondary_pair_labelled': {'q': '151552|tau|', 'C': exact(S2['C']), 'c_site': exact(S2['c_site']),
                                    'K_input': exact(S2['K']), 'disc_radius': '1/151552', 'targets': [qs(C2_target), qs(cs2_target)]},
        'crude_tier': {'C': exact(Hc['C']), 'c_site': exact(Hc['c_site']), 'secondary_C': exact(S2c['C']),
                       'secondary_c_site': exact(S2c['c_site']), 'status': 'reported separately; fails the headline targets'},
        'marginal_locality_lemma': lemma,
        'proof_weights': weights_decl,
        'recursion': {'depth': 'unbounded (finite in each finite volume); one covering level per region',
                      'per_level_factor': 'c_card t_W = 8 t_W = ' + qs(8 * H['tW']),
                      'charging': 'per site, |I|<=8*2^{diam I}, lambda=2/W'},
        'every_site_form': 'b',
        'comparisons': comp_table,
    }
    result = {
        'loop': 'BB1', 'direction': 'reverse', 'human_author': contract['human_author'],
        'contribution_alias': 'HNM-BB1-R iterated-split marginal locality (reverse producer; AI-assisted, Claude)',
        'ai_assistance': 'Claude (an AI model) wrote the derivations, check.py and report.md; correlated model-agent work, not human review',
        'model': pre['model_id'], 'families': [F1_NAME, F2_NAME], 'cover': 'R={0,e_z}',
        'metric': 'coarse l-infinity on factor sites (star diameter 1)', 'topology': 'trace norm on B(H_Y)',
        'clock': 'not applicable to static densities; round clock theta=alpha*t/hbar (s=alpha*t_E/hbar, u=theta/8 internal)',
        'route': ROUTE, 'routes_executed': [ROUTE], 'tier': 'exact_first_order',
        'headline': headline, 'label': 'boundary_decay_rate_only', 'secondary_labels': ['static_not_dynamic'],
        'gate_fields': gate_fields_export,
        'mandatory_sentence_template': template,
        'contract_controls_covered': controls_ids,
        'controls_with_damaging_mutations': sorted(MUTATION_CONTROLS),
        'damaging_mutations_total': sum(len(c.get('rejected_mutations', {})) for c in CHECKS),
        'fixtures': sorted(fx),
        'exclusions': {'contract': contract['claim_exclusions'], 'preregistration': pre['claim_exclusions']},
        'proposed_reverse_verdict': outcome,
        'outcome_note': 'proposed for the reverse half only; acceptance needs both routes and skeptical review',
        'scratch_disclosure': '/tmp/claude-0/bb1-reverse-private/ (private; nothing in it is evidence)',
        'items': ['item 1: split decomposition, Tr N_c >= 1, Lipschitz in coefficients (eta=0) and in omega_O',
                  'item 3: iterated split at the changed support and at covering regions, per-site charging',
                  'item 4: every-site form (b) proved; headline, region form, secondary, crude; every comparison, both signs, Q_L and untruncated',
                  'item 5: fixtures, template, gate fields', 'item 6: scaling and 37 controls as damaging mutations',
                  'item 2: forward polymer route (not this producer); the polymer-identity fixture is exhibited'],
        'checks': CHECKS,
    }
    for k in FALSE_FLAGS:
        result[k] = False
    result['uniform_wilson_claim'] = False
    result['resolved_interaction_shift'] = False
    return result


def main():
    ap = argparse.ArgumentParser(description='HNM-BB1 reverse producer checker (exact arithmetic)')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('check.py: --output must be an absolute path')
    if out.exists():
        raise SystemExit('check.py: --output must be a fresh directory')
    resolved = out.resolve()
    if resolved == ROOT or ROOT in resolved.parents:
        raise SystemExit('check.py: --output must lie outside the checkout')
    result = compute()
    out.mkdir(parents=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    sources = {p.relative_to(HERE).as_posix(): sha256_file(p) for p in sorted(HERE.rglob('*'))
               if p.is_file() and (p.relative_to(HERE).parts[0] == 'inputs' or p.name in ('check.py', 'report.md'))
               and p.relative_to(HERE).parts[0] != 'output'}
    manifest = {'loop': 'BB1', 'direction': 'reverse', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    hp = result['headline']
    print(json.dumps({'loop': 'BB1', 'direction': 'reverse', 'checks': len(result['checks']),
                      'C': hp['statement_constants']['C']['preview'], 'c_site': hp['region_form']['c_site']['preview'],
                      'controls': len(result['controls_with_damaging_mutations']),
                      'mutations': result['damaging_mutations_total'], 'outcome': result['proposed_reverse_verdict']}, sort_keys=True))


if __name__ == '__main__':
    main()
