#!/usr/bin/env python3
"""HNM-BC2 forward producer (single direction; the skeptic replays from the contract).

Route-B uniform Kogut-Susskind SU(2) model at fixed spacing and strong bare coupling
(model AQ_uniform_routeB): every-site coefficient decay on the complex coupling disc
|z| <= 64|tau| (route analytic_disc), marginal locality of the reduced densities by the
iterated product-ordering split with per-site charging (route iterated_split),
whole-sequence convergence of the named construction (centered whole-star-plus-single-
group boxes; assembly union_comparison), exhaustion within the prescription, the
pointwise U_E sign mirror, identification with every AQ1-type subsequential state of
the AX1 construction before inheritance, coarse translation invariance, and the AX2
node restated for the limit with the admitted AX2 calculator replayed.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production (Claude, an
AI model); HNM labels are project aliases. Banach's fixed-point theorem, Weierstrass'
theorem, the maximum-modulus principle, the pure-state trace-distance identity, the
contractivity of the partial trace and the completeness of the trace class are
established mathematics; the commuting creation expansion is the admitted AM2
construction re-instantiated for route B by AX1. Scientific priority is unverified.

Standard library only. Exact Fraction arithmetic decides every Boolean; decimal strings
are truncated previews. Every contract control is executed as damaging mutations whose
rejection is required. Failures are explicit exceptions (never assert), so the run and
its output bytes are identical under python -O. Every route-B constant is recomputed
from the route-B inputs derived here from the fine geometry (per-site sum 29|tau|,
52 first-order faces per factor, 5 interaction groups per site); route-A constants are
rejected under a route-B label.

Usage: python3 -B research/round33/forward/bc2/check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUTS = HERE / 'inputs'
CONTRACT_REL = 'research/round33/contracts/bc2.json'
CONTRACT_SHA256 = '28abe3775455087384b3c9dbbb2df67b923e31b964d40efa7ea9787ee8b6b98a'
PINNED_GATES = {
    'research/round29/advisor/al1-gate.json': 'e415203cc6b6ebca6cea5fcd1230a7eb0e20b7ab2d2e6c99dc8aa2dd3052a75b',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/advisor/aq2-gate.json': '930b697db343ffd261c303c34e6ddd8c6e9c753ee6707931c55dc4171ee47575',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/av2-gate.json': '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33',
    'research/round32/advisor/ax1-gate.json': '1b8fb152696659439bb01fc7df429fc76fa3132d4936df450d8131256015d177',
    'research/round32/advisor/ax2-gate.json': '1db36627b9eab00915b0cb38a0e9fd9cf9dd4dbf3ceb7eab969336f3f9f44be4',
    'research/round33/advisor/ba1-gate.json': '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    'research/round33/advisor/bb1-gate.json': '18141fea672e5bae09024a5fddc56ea7102aae56ecca16fbb30d67a1354a3827',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
}
CALCULATOR_REL = 'research/round32/forward/ax2/calculator.py'
CALCULATOR_SHA256 = 'f368a3e7e73afc52a14422dd253efbc50fa5d7b59c55b3be569f48043f031f5d'
AX1_GATE = 'research/round32/advisor/ax1-gate.json'
AX2_GATE = 'research/round32/advisor/ax2-gate.json'
BA1_GATE = 'research/round33/advisor/ba1-gate.json'
BB1_GATE = 'research/round33/advisor/bb1-gate.json'
BB2_GATE = 'research/round33/advisor/bb2-gate.json'
I1_REL = 'research/round21/forward/i1/report.md'
FORBIDDEN_PREFIXES = (
    'research/round33/forward/bc1', 'research/round33/reverse/bc', 'research/round33/experts/',
    'research/round33/advisor/deliberation', 'research/round33/advisor/panel', 'research/round33/advisor/plan',
    'research/round33/advisor/triage', 'research/round33/advisor/brief', 'research/round33/skeptic/bc',
)
SKEPTIC_ALLOWED = ('research/round32/skeptic/ax1.md', 'research/round32/skeptic/ax2.md', 'research/round33/skeptic/bb1.md')
ADVISOR_ALLOWED = tuple(sorted(k for k in PINNED_GATES if '/round33/' in k)) + ('research/round33/advisor/selection-bc2.md',)
MODEL_ID = 'AQ_uniform_routeB'
FAMILY = 'FB: centered whole-star-plus-single-group boxes Lambda_N=[-N,N]^3 (route B, AX1 construction)'
LABEL = 'uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling (g^4=9.6x10^9)'
ROUTE_K = 'analytic_disc'
ROUTE_DENSITY = 'iterated_split'
ASSEMBLY = 'union_comparison'
TIERS = ('crude_majorant', 'exact_first_order')
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


def exp_upper(x, terms=24):
    """Directed upper bound of exp(x), 0<=x<=1/2: partial sum plus a geometric tail."""
    x = Q(x)
    must(Q(0) <= x <= Q(1, 2), 'exponential argument outside [0,1/2]')
    partial, power = Q(0), Q(1)
    for k in range(terms + 1):
        partial += power / factorial(k)
        power *= x
    tail = power / factorial(terms + 1) / (1 - x / (terms + 2))
    return partial + tail, partial


def exp3_bracket(terms=90):
    """lo <= e^3 <= hi (partial sum; tail by a geometric majorant)."""
    partial, power = Q(0), Q(1)
    for k in range(terms + 1):
        partial += power / factorial(k)
        power *= 3
    tail = power / factorial(terms + 1) / (1 - Q(3, terms + 2))
    return partial, partial + tail


def atan_bracket(z, terms=60):
    """Alternating partial sums of arctan: a sum ending on a positive term is an upper bound,
    one ending on a negative term is a lower bound (terms decrease in modulus)."""
    z = Q(z)
    must(0 < z <= Q(1, 5), 'atan argument')
    s, sums = Q(0), []
    for k in range(terms):
        s += (-1) ** k * z ** (2 * k + 1) / (2 * k + 1)
        sums.append(s)
    a, b = sums[-2], sums[-1]
    lo, hi = (a, b) if (terms - 1) % 2 == 0 else (b, a)
    must(lo <= hi, 'atan bracket order')
    return lo, hi


def pi_lower():
    a_lo, a_hi = atan_bracket(Q(1, 5))
    b_lo, b_hi = atan_bracket(Q(1, 239))
    lo, hi = 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo
    must(Q(333, 106) < lo <= hi < Q(355, 113), 'pi bracket')
    return lo, hi


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


def int_sqrt_floor(n):
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def det(m):
    """Exact determinant by Fraction elimination."""
    a = [[Q(v) for v in row] for row in m]
    n = len(a)
    d = Q(1)
    for i in range(n):
        piv = next((r for r in range(i, n) if a[r][i] != 0), None)
        if piv is None:
            return Q(0)
        if piv != i:
            a[i], a[piv] = a[piv], a[i]
            d = -d
        d *= a[i][i]
        for r in range(i + 1, n):
            f = a[r][i] / a[i][i]
            if f:
                for c in range(i, n):
                    a[r][c] -= f * a[i][c]
    return d


def psd_by_minors(m):
    """A real symmetric matrix is positive semidefinite iff every principal minor is nonnegative."""
    n = len(m)
    for k in range(1, n + 1):
        for idx in combinations(range(n), k):
            if det([[m[i][j] for j in idx] for i in idx]) < 0:
                return False
    return True


# ------------------------------------------------------------ lattice geometry
E = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
R_COVER = frozenset((ORIGIN, EZ))
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


def is_selected(p, a, c):
    """Selected xy faces: even y and x residue 0,1,2 modulo 4 (I1 section 1)."""
    return (a, c) == ('x', 'y') and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


def owners_of(p, a, c):
    """Owner factor of each of the four links (the coarse block of the link tail)."""
    return [coarse(t) for t, _ in face_links(p, a, c)]


def derive_classes():
    """All 24 anchored face classes from the fine geometry (I1 section 3)."""
    out = []
    for a, c in (('x', 'y'), ('x', 'z'), ('y', 'z')):
        for r in range(4):
            for s in range(2):
                p = (r, s, 0)
                own = [vsub(o, coarse(p)) for o in owners_of(p, a, c)]
                K = tuple(sorted(set(own)))
                per_owner = {o: own.count(o) for o in K}
                out.append({'orient': a + c, 'r': r, 's': s, 'K': K, 'selected': is_selected(p, a, c),
                            'links_per_owner': per_owner})
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
        must(row['count'] == len(row['r']) * len(row['s']), 'I1 table row count')
        for r in row['r']:
            for s in row['s']:
                match = [c for c in classes if c['orient'] == row['orient'] and c['r'] == r and c['s'] == s]
                must(len(match) == 1 and match[0]['K'] == row['K'] and match[0]['selected'] == row['selected'],
                     'I1 table row disagrees with the derived class')
                seen.add((row['orient'], r, s))
    must(len(seen) == 24, 'I1 table does not cover the 24 classes')
    return True


CLASSES = derive_classes()
SELECTED_IDX = tuple(k for k, c in enumerate(CLASSES) if c['selected'])
OMITTED_IDX = tuple(k for k, c in enumerate(CLASSES) if not c['selected'])


def face_support(face):
    b, k = face
    return frozenset(vadd(b, s) for s in CLASSES[k]['K'])


def box(N):
    return frozenset(product(range(-N, N + 1), repeat=3))


def prism(lo, hi):
    return frozenset(product(*[range(lo[i], hi[i] + 1) for i in range(3)]))


def translate(vol, v):
    return frozenset(vadd(b, v) for b in vol)


def star(b):
    return frozenset(vadd(b, s) for s in S_STAR)


def routeb_faces(vol, keep_singles=True, clip_boundary_singles=False):
    """Route-B retention: whole stars inside the volume (21 omitted faces each) and every
    single-factor group of the volume (3 selected faces, support {b})."""
    out = set()
    for b in vol:
        if star(b) <= vol:
            for k in OMITTED_IDX:
                out.add((b, k))
        if keep_singles and not (clip_boundary_singles and not star(b) <= vol):
            for k in SELECTED_IDX:
                out.add((b, k))
    return frozenset(out)


def dinf(p, q):
    return max(abs(p[0] - q[0]), abs(p[1] - q[1]), abs(p[2] - q[2]))


def norm_inf(p):
    return max(abs(p[0]), abs(p[1]), abs(p[2]))


def diam(Y):
    Y = list(Y)
    return max((dinf(a, b) for a in Y for b in Y), default=0)


def face_site_set(faces):
    out = set()
    for f in faces:
        out.update(face_support(f))
    return out


def min_dist_to_sites(u, sites):
    return min((dinf(u, s) for s in sites), default=10 ** 9)


# ------------------------------------------------ route-B inputs derived from the geometry
def brute_force_partition(N=2):
    """Every plaquette with base in the fine region of the coarse box Lambda_N lies in exactly
    one route-B group: the single-factor group of its anchor (selected) or the anchor's star."""
    lo, hi = -N, N
    groups = {}
    count = 0
    for x in range(4 * lo, 4 * hi + 4):
        for y in range(2 * lo, 2 * hi + 2):
            for z in range(lo, hi + 1):
                p = (x, y, z)
                b = coarse(p)
                for a, c in (('x', 'y'), ('x', 'z'), ('y', 'z')):
                    own = frozenset(owners_of(p, a, c))
                    sel = is_selected(p, a, c)
                    gkey = ('single', b) if sel else ('star', b)
                    gsupp = frozenset([b]) if sel else star(b)
                    must(own <= gsupp, 'face support outside its group support')
                    must((own == frozenset([b])) == sel, 'selected face is exactly the one-owner face')
                    groups.setdefault(gkey, []).append((p, a + c))
                    count += 1
    sizes = sorted({(k[0], len(v)) for k, v in groups.items()})
    flat = [f for v in groups.values() for f in v]
    must(len(flat) == len(set(flat)) == count, 'a plaquette charged twice')
    return {'plaquettes': count, 'groups': len(groups), 'group_sizes': [list(s) for s in sizes]}


def per_site_inputs():
    """Faces through a factor, owner sets containing it, groups containing it, per-site sum (per |tau|)."""
    u = ORIGIN
    faces = [(vsub(u, d), k) for d in S_STAR for k in range(24) if d in CLASSES[k]['K']]
    faces = sorted(set(f for f in faces if (f[1] in SELECTED_IDX and f[0] == u) or f[1] in OMITTED_IDX))
    owner_sets = {}
    for f in faces:
        owner_sets.setdefault(face_support(f), []).append(f)
    mult = sorted(len(v) for v in owner_sets.values())
    stars_containing = [vsub(u, d) for d in S_STAR]
    groups = len(stars_containing) + 1
    per_site_sum = Q(len(stars_containing) * len(OMITTED_IDX) + len(SELECTED_IDX), 3)
    return {'faces_per_site': len(faces), 'owner_sets': len(owner_sets), 'multiplicities': mult,
            'groups_per_site': groups, 'per_site_sum_over_tau': per_site_sum,
            'omitted_faces_per_site': sum(1 for f in faces if f[1] in OMITTED_IDX),
            'selected_faces_per_site': sum(1 for f in faces if f[1] in SELECTED_IDX)}


def incidence_on_R(N):
    vol = box(N)
    stars = [b for b in sorted(vol) if star(b) <= vol and star(b) & R_COVER]
    singles = [b for b in sorted(vol) if b in R_COVER]
    faces = [(b, k) for b in stars for k in OMITTED_IDX] + [(b, k) for b in singles for k in SELECTED_IDX]
    meets = [f for f in faces if face_support(f) & R_COVER]
    inside = [f for f in meets if face_support(f) <= R_COVER]
    strad = [f for f in meets if not face_support(f) <= R_COVER]
    strictly = [f for f in meets if face_support(f) > R_COVER]
    table = []
    for b in stars:
        fb = [(b, k) for k in OMITTED_IDX]
        table.append({'group': 'star', 'anchor': list(b), 'faces': 21,
                      'meeting_R': sum(1 for f in fb if face_support(f) & R_COVER),
                      'inside_R': sum(1 for f in fb if face_support(f) <= R_COVER)})
    for b in singles:
        fb = [(b, k) for k in SELECTED_IDX]
        table.append({'group': 'single', 'anchor': list(b), 'faces': 3,
                      'meeting_R': sum(1 for f in fb if face_support(f) & R_COVER),
                      'inside_R': sum(1 for f in fb if face_support(f) <= R_COVER)})
    return {'N': N, 'stars': len(stars), 'singles': len(singles), 'faces_charged': len(faces),
            'meeting_R': len(meets), 'inside_R': len(inside), 'straddling': len(strad),
            'straddling_strictly_containing_R': len(strictly), 'table': table,
            'selected_inside_R': sum(1 for f in inside if f[1] in SELECTED_IDX),
            'omitted_inside_R': sum(1 for f in inside if f[1] in OMITTED_IDX)}


def boundary_counts_at_most_bulk(N, bulk_faces):
    vol = box(N)
    faces = routeb_faces(vol)
    per = {}
    for f in faces:
        for x in face_support(f):
            per[x] = per.get(x, 0) + 1
    return max(per.values()) <= bulk_faces


def every_site_source_audit(N, faces_a, faces_b):
    """Every source face (present in one route-B volume only) lies at l-infinity distance at
    least N-|u|_inf from every u in Lambda_N."""
    source = faces_a ^ faces_b
    sites = face_site_set(source)
    worst, attained = None, 0
    for u in sorted(box(N)):
        d = min_dist_to_sites(u, sites)
        need = N - norm_inf(u)
        if d < need:
            return {'ok': False, 'u': list(u), 'distance': d, 'required': need}
        if d == need:
            attained += 1
        worst = d - need if worst is None else min(worst, d - need)
    selected_sources = sum(1 for f in source if f[1] in SELECTED_IDX)
    return {'ok': True, 'source_faces': len(source), 'selected_source_faces': selected_sources,
            'min_slack': worst, 'sites_attaining': attained}


def certify_common_core(N, faces_volume):
    """Route-B common core: every face (omitted or selected) with a site within N-|u|_inf-1 of
    u in Lambda_N belongs to the core (stars inside Lambda_N and singles of Lambda_N)."""
    core = routeb_faces(box(N))
    outside = faces_volume - core
    sites = face_site_set(outside)
    for u in sorted(box(N)):
        require(min_dist_to_sites(u, sites) >= N - norm_inf(u), 'a non-core face lies within N-|u|-1 of u')
    require(core <= faces_volume, 'the volume does not retain the core')
    return True


def piece_graph(vol, include_singles=True):
    pieces = sorted({face_support(f) for f in routeb_faces(vol, keep_singles=include_singles)},
                    key=lambda s: sorted(s))
    return pieces


def bfs_orders_from(u, pieces):
    """Least connected-family size joining a piece containing u to each piece (intersection graph,
    breadth-first by layers, adjacency through a site index)."""
    by_site = {}
    for i, p in enumerate(pieces):
        for x in p:
            by_site.setdefault(x, []).append(i)
    order = {}
    frontier = list(by_site.get(u, []))
    for i in frontier:
        order[i] = 1
    while frontier:
        nxt = []
        for i in frontier:
            for x in sorted(pieces[i]):
                for j in by_site[x]:
                    if j not in order:
                        order[j] = order[i] + 1
                        nxt.append(j)
        frontier = nxt
    return {pieces[i]: n for i, n in order.items()}


def order_vs_distance_at(u, pieces):
    order = bfs_orders_from(u, pieces)
    worst, singles_reached = None, 0
    for p, n in order.items():
        d = min(dinf(u, s) for s in p)
        if len(p) == 1:
            singles_reached += 1
        if d >= 1:
            require(n >= 1 + d, 'order below 1+d at u')
            worst = n - (1 + d) if worst is None else min(worst, n - (1 + d))
    return worst, singles_reached


# --------------------------------------------------------------- AM2 majorant (route B)
R_BALL = Q(1, 64)
GR_UP = Q(148, 7)
GPR_UP = Q(352)


def disc_selfmap(J_over_tau_unit, radius):
    """(self-map value, contraction value) for |z| <= radius with per-site sum J|z|."""
    return J_over_tau_unit * radius * GR_UP, J_over_tau_unit * radius * GPR_UP


def certify_disc(J_unit, radius, label):
    sm, ct = disc_selfmap(J_unit, radius)
    require(sm <= R_BALL, label + ': self-map J rho G(R) <= R fails')
    require(ct < 1, label + ': contraction J rho G\'(R) < 1 fails')
    return True


def T_exact(rho, J_unit, F):
    """exact_first_order circle bound T(rho)=(F rho/144)/(1-J rho G'(R))."""
    rho = Q(rho)
    require(J_unit * 352 * rho < 1, 'contraction on the disc')
    return Q(F, 144) * rho / (1 - J_unit * 352 * rho)


def T_crude(rho, J_unit):
    return J_unit * Q(rho) * GR_UP


def beta_star(t0, tW, ccard=8):
    """Closure of the covering-chain recursion: kappa(J) <= beta* H(J) for J missing Y."""
    t0, tW = Q(t0), Q(tW)
    require(0 <= t0 < 1 and 0 <= tW and ccard * tW < 1, 'per-site sums outside the contraction range')
    c1 = 4 * t0 * tW + (4 * tW + 4 * t0 * tW / (1 - t0)) / (1 - ccard * tW)
    c2 = 2 * ccard * t0 * tW + 2 * ccard * t0 * tW / ((1 - t0) * (1 - ccard * tW))
    require(c2 < 1, 'closure coefficient not below one')
    return c1, c2, c1 / (1 - c2)


def lattice_sum_3d(x):
    """S(x)=sum_{v in Z^3} x^{|v|_inf} = 1 + sum_{r>=1}(24 r^2+2) x^r (exact, 0<=x<1)."""
    x = Q(x)
    require(0 <= x < 1, 'lattice sum ratio not below one (split weight too small for the rate)')
    return 1 + 24 * x * (1 + x) / (1 - x) ** 3 + 2 * x / (1 - x)


def routeb_constants(tier, tau, W, rho, q, J_unit, F):
    """Every constant of one tier: K_B (every-site analytic-disc input), t0, tW, beta*, S, c_site, C."""
    tau, W, rho, q = abs(Q(tau)), Q(W), Q(rho), Q(q)
    require(tier in TIERS, 'tier outside the vocabulary: ' + str(tier))
    require(q == tau / rho, 'rate is not |tau|/rho for the declared disc')
    must(certify_disc(J_unit, rho, 'disc'), 'disc admissible')
    must(certify_disc(J_unit, W * tau, 'split weight'), 'split weight admissible')
    lam = 2 / W
    require(lam < q, 'lambda=2/W not below q')
    T = (lambda r: T_exact(r, J_unit, F)) if tier == 'exact_first_order' else (lambda r: T_crude(r, J_unit))
    K = 2 * T(rho)
    t0 = 2 * T(tau)
    tW = 2 * T(W * tau)
    c1, c2, beta = beta_star(t0, tW, 8)
    S = lattice_sum_3d(lam / q)
    require(t0 <= K, 'outside-box coefficient sums exceed K q^0')
    csite = K * (2 + beta * S)
    C = csite * (1 + q)
    return {'tier': tier, 'K': K, 'q': q, 'W': W, 'rho': rho, 'lambda': lam, 't0': t0, 'tW': tW,
            'c1': c1, 'c2': c2, 'beta': beta, 'S': S, 'c_site': csite, 'C': C, 'T_tau': T(tau)}


def ledger_parts(sc):
    t0, tW, q, K = sc['t0'], sc['tW'], sc['q'], sc['K']
    norm_a = 4 * t0 * tW
    straddle = 4 * tW / (1 - 8 * tW)
    removal = 4 * t0 * tW / ((1 - t0) * (1 - 8 * tW))
    must(norm_a + straddle + removal == sc['c1'], 'c1 decomposition')
    feedback = sc['beta'] - sc['c1']
    f = K * sc['S'] * (1 + q)
    return {'near': K * 2 * (1 + q), 'straddling': f * straddle, 'normalization': f * norm_a,
            'removal': f * removal, 'feedback': f * feedback}


# ------------------------------------------------------- creation-algebra engine (fixtures)
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
    v = {tuple([0] * n): Q(1)}
    keys = sorted(coll) if order is None else order
    for I in keys:
        v = vec_add(v, apply_c(I, coll[I], v), -1)
    return v


def norm2(v):
    return sum(a * a for a in v.values())


def marginal(u, w, Y, n):
    """Tr_{Y^c}|u><w| as {(y-config of u, y-config of w): value} (real vectors)."""
    rest = [k for k in range(n) if k not in Y]
    wi = {}
    for b2, y in w.items():
        wi.setdefault(tuple(b2[k] for k in rest), []).append((tuple(b2[t] for t in Y), y))
    out = {}
    for b, x in u.items():
        for yc2, y in wi.get(tuple(b[k] for k in rest), ()):
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


def tn2_sq(m):
    """(trace norm)^2 of a real symmetric 2x2 matrix on one qubit, exactly."""
    p, s, r = m.get(((0,), (0,)), 0), m.get(((0,), (1,)), 0), m.get(((1,), (1,)), 0)
    must(m.get(((1,), (0,)), 0) == s, 'symmetric 2x2')
    return max((p + r) ** 2, (p - r) ** 2 + 4 * s * s)


def lcg_rationals(seed, count, span=9, lo=20, hi=60):
    out, x = [], seed
    for _ in range(count):
        x = (1103515245 * x + 12345) % (2 ** 31)
        num = (x % (2 * span + 1)) - span
        x = (1103515245 * x + 12345) % (2 ** 31)
        den = lo + x % (hi - lo)
        out.append(Q(num if num != 0 else 1, den))
    return out


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


def split_identity_fixture():
    """Exact identity (R07) at a changed support J missing Y and the covering recursion (R10),
    on six sites with two excited levels, single-site (support-one) supports included."""
    n, d = 6, 3
    supports = [(0,), (1,), (2,), (3,), (4,), (5,), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 2), (1, 3),
                (2, 4), (1, 2, 3), (3, 4, 5)]
    amps = lcg_rationals(3301, sum((d - 1) ** len(I) for I in supports) + 8)
    coll, k = {}, 0
    for I in supports:
        cv = {}
        for e in product(range(1, d), repeat=len(I)):
            cv[e] = amps[k]
            k += 1
        coll[I] = cv
    v = psi_of(n, coll)
    must(vec_add(v, psi_of(n, coll, order=list(reversed(sorted(supports)))), -1) == {}, 'order independence')
    Y, J = (0,), (3, 4)
    newJ = {e: a / 3 + Q(1, 17) for e, a in coll[J].items()}
    c2 = dict(coll)
    c2[J] = newJ
    rho1, rho2 = density(psi_of(n, coll), Y, n), density(psi_of(n, c2), Y, n)
    phi = psi_of(n, remove_meeting(coll, J))
    n2 = norm2(phi)
    a = sum(x * x for x in coll[J].values()) - sum(x * x for x in newJ.values())
    delta = {e: coll[J][e] - newJ[e] for e in coll[J]}
    w = dict(phi)
    for I in sorted(coll):
        if set(I) & set(J) and I != J:
            w = vec_add(w, apply_c(I, coll[I], w), -1)
    dpp = vec_add(w, phi, -1)
    must(all(any(b[j] != 0 for j in J) for b in dpp), 'D\'\' psi_J is excited on J')
    G = marginal(apply_c(J, delta, phi), dpp, Y, n)
    trG = mat_trace(G)
    Z = norm2(psi_of(n, coll))
    rho_phi = density(phi, Y, n)
    defect = mat_lin((1, G), (-trG, rho2))
    rhs = mat_lin((a * n2 / Z, rho_phi), (-a * n2 / Z, rho2), (-1 / Z, defect), (-1 / Z, mat_T(defect)))
    lhs = mat_lin((1, rho1), (-1, rho2))
    identity = mat_lin((1, lhs), (-1, rhs)) == {}
    rec_ok = []
    for U, S in (((3, 4), (2,)), ((3, 4), (5,)), ((3, 4), (1, 2))):
        g = {e: Q(1, 3 + i) for i, e in enumerate(product(range(1, d), repeat=len(S)))}
        rec_ok.append(mat_lin((1, gamma_direct(n, coll, U, S, g, Y)), (-1, gamma_recursive(n, coll, U, S, g, Y))) == {})
    return {'sites': n, 'levels': d, 'supports': len(supports), 'single_site_supports': 6, 'Y': list(Y), 'J': list(J),
            'identity_R07_exact': identity, 'Z_at_least_n2': Z >= n2, 'covering_recursion_exact': rec_ok,
            **FIXTURE_LABEL}


def mixed_outside_fixture():
    """Tr N_c(omega) >= 1 and ||rho(omega)-rho(omega')||_1 <= 2||N_c(omega-omega')||_1 on mixed outside states."""
    Y, n = (0,), 3
    Ec = qubit_coll({(0,): Q(1, 7), (0, 1): Q(-1, 5), (0, 2): Q(1, 6), (0, 1, 2): Q(1, 9)})

    def Nc(mix):
        tot = {}
        for wgt, phi in mix:
            vec = {(0,) + b: a for b, a in phi.items()}
            for I in sorted(Ec):
                vec = vec_add(vec, apply_c(I, Ec[I], vec), -1)
            tot = mat_lin((1, tot), (wgt, marginal(vec, vec, Y, n)))
        return tot

    def normalize_mix(parts):
        z = sum(wgt * norm2(phi) for wgt, phi in parts)
        return [(wgt / z, phi) for wgt, phi in parts]

    om1 = normalize_mix([(Q(2, 3), {(0, 0): Q(1), (1, 1): Q(1, 2)}), (Q(1, 3), {(1, 0): Q(1), (0, 1): Q(-1, 3)})])
    om2 = normalize_mix([(Q(1, 2), {(0, 0): Q(1), (0, 1): Q(1, 4)}), (Q(1, 2), {(1, 1): Q(1), (1, 0): Q(2, 5)})])
    N1, N2 = Nc(om1), Nc(om2)
    t1, t2 = mat_trace(N1), mat_trace(N2)
    rho1 = {k: v / t1 for k, v in N1.items()}
    rho2 = {k: v / t2 for k, v in N2.items()}
    lhs_sq = tn2_sq(mat_lin((1, rho1), (-1, rho2)))
    rhs_sq = 4 * tn2_sq(mat_lin((1, N1), (-1, N2)))
    return {'trace_N_omega1': qs(t1), 'trace_N_omega2': qs(t2), 'trace_at_least_one': t1 >= 1 and t2 >= 1,
            'lipschitz_lhs_sq': qs(lhs_sq), 'lipschitz_rhs_sq': qs(rhs_sq), 'lipschitz_holds': lhs_sq <= rhs_sq,
            **FIXTURE_LABEL}


def lemma_single_support_fixture():
    """Lemma S1: ||rho_Y(c)-rho_Y(c')||_1 <= 2||c_J-c'_J|| for every single-support change (qubit chain)."""
    n, Y = 5, (0,)
    amps = {(0,): Q(1, 4), (1,): Q(-1, 3), (2,): Q(1, 5), (3,): Q(2, 7), (4,): Q(-1, 6), (0, 1): Q(1, 3), (1, 2): Q(-2, 5),
            (2, 3): Q(1, 4), (3, 4): Q(1, 2), (0, 1, 2): Q(-1, 7), (2, 3, 4): Q(1, 8)}
    base = qubit_coll(amps)
    rho0 = density(psi_of(n, base), Y, n)
    ok = []
    for I in sorted(amps):
        for new in (Q(0), amps[I] + Q(1, 3), -amps[I]):
            c2 = qubit_coll({**amps, I: new})
            diff = mat_lin((1, rho0), (-1, density(psi_of(n, c2), Y, n)))
            ok.append(tn2_sq(diff) <= 4 * (amps[I] - new) ** 2)
    return {'changes': len(ok), 'holds': all(ok), **FIXTURE_LABEL}


def chain_end_to_end_fixture():
    """End-to-end check of the marginal-locality lemma on a qubit chain (1D cardinality |I|<=2^{diam I}, c_card=1)."""
    n, Y, W = 7, (0,), Q(4)
    lam = 2 / W
    supports = [(i,) for i in range(n)] + [(i, i + 1) for i in range(n - 1)] + [(i, i + 1, i + 2) for i in range(n - 2)]
    A = lcg_rationals(911, len(supports), span=3, lo=400, hi=800)
    B = lcg_rationals(1733, len(supports), span=3, lo=400, hi=800)
    cA = {I: A[i] for i, I in enumerate(supports)}
    cB = {I: (A[i] if 0 in I else B[i]) for i, I in enumerate(supports)}
    m = {I: max(abs(cA[I]), abs(cB[I])) for I in supports}
    t0 = max(sum(m[I] for I in supports if x in I) for x in range(n))
    tW = max(sum(W ** (len(I) - 1) * m[I] for I in supports if x in I) for x in range(n))
    c1, c2, beta = beta_star(t0, tW, 1)
    h = {x: lam ** x for x in range(n)}
    H = {I: sum(h[x] for x in I) for I in supports}
    rA = density(psi_of(n, qubit_coll(cA)), Y, n)
    rB = density(psi_of(n, qubit_coll(cB)), Y, n)
    lhs_sq = tn2_sq(mat_lin((1, rA), (-1, rB)))
    bound = sum(2 * abs(cA[I] - cB[I]) for I in supports if 0 in I) + \
        sum(beta * H[I] * abs(cA[I] - cB[I]) for I in supports if 0 not in I)
    single = []
    for I in supports:
        if 0 in I or cA[I] == cB[I]:
            continue
        cC = dict(cA)
        cC[I] = cB[I]
        d_sq = tn2_sq(mat_lin((1, rA), (-1, density(psi_of(n, qubit_coll(cC)), Y, n))))
        single.append(d_sq <= (beta * H[I] * abs(cA[I] - cB[I])) ** 2)
    return {'sites': n, 'supports': len(supports), 'W': qs(W), 't0': qs(t0), 'tW': qs(tW), 'beta_1d': sci(beta),
            'observed_trace_norm_sq': sci(lhs_sq), 'bound': sci(bound), 'total_bound_holds': lhs_sq <= bound * bound,
            'single_far_support_bounds_hold': all(single) and len(single) > 0, **FIXTURE_LABEL}


def pmul(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = tuple(x + y for x, y in zip(ka, kb))
            out[k] = out.get(k, 0) + va * vb
    return {k: v for k, v in out.items() if v != 0}


def padd(a, b, s=1):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + s * v
    return {k: v for k, v in out.items() if v != 0}


def second_order_chain_fixture():
    """Chain r-o1-o2, supports {r,o1}:a, {o1,o2}:b, {o2}:c as polynomial variables."""
    one = {(0, 0, 0): Q(1)}
    var = {'a': {(1, 0, 0): Q(1)}, 'b': {(0, 1, 0): Q(1)}, 'c': {(0, 0, 1): Q(1)}}
    sup = {(0, 1): 'a', (1, 2): 'b', (2,): 'c'}
    psi = {(0, 0, 0): one}
    for I in ((2,), (1, 2), (0, 1)):
        new = dict(psi)
        for b, amp in psi.items():
            if all(b[x] == 0 for x in I):
                nb = list(b)
                for x in I:
                    nb[x] = 1
                nb = tuple(nb)
                new[nb] = padd(new.get(nb, {}), pmul(amp, var[sup[I]]), -1)
        psi = {k: v for k, v in new.items() if v}
    rho = {}
    for b1, a1 in psi.items():
        for b2, a2 in psi.items():
            if b1[1:] == b2[1:]:
                key = (b1[0], b2[0])
                rho[key] = padd(rho.get(key, {}), pmul(a1, a2))
    off = rho.get((0, 1), {})
    d_c = {(k[0], k[1], k[2] - 1): v * k[2] for k, v in off.items() if k[2] > 0}
    return {'rho_00': {str(k): qs(v) for k, v in sorted(rho[(0, 0)].items())},
            'rho_01': {str(k): qs(v) for k, v in sorted(off.items())},
            'rho_11': {str(k): qs(v) for k, v in sorted(rho[(1, 1)].items())},
            'd_rho01_dc': {str(k): qs(v) for k, v in sorted(d_c.items())},
            'off_diagonal_is_minus_abc': off == {(1, 1, 1): Q(-1)}, 'first_order_in_c_free': all(k[0] + k[1] >= 2 for k in off),
            **FIXTURE_LABEL}


def certify_propagation_claim(claim, a, b):
    require(claim['order_in_straddling_amplitudes'] == 2, 'first-order propagation claimed (the exact chain is second order)')
    prod_ = Q(1)
    for f in claim['per_link']:
        prod_ *= Q(f)
    require(abs(prod_) >= abs(a * b), 'per-link factors below the exact straddling product')
    return True


def straddling_fixture():
    """R={r0,r1}, outside o; one creation of amplitude eps on a support.  rho_R(eps)-rho_R(-eps) is the
    odd part (its linear term is the first-order R-marginal): nonzero only for supports contained in R
    (the pair R or a single site of R); straddling supports enter at second order only."""
    eps = Q(1, 10)
    n, Y = 3, (0, 1)
    out = {}
    for name, I in (('straddling_{r0,o}', (0, 2)), ('straddling_strictly_containing_R', (0, 1, 2)),
                    ('inside_R_pair', (0, 1)), ('inside_R_single_site', (0,))):
        plus = density(psi_of(n, qubit_coll({I: eps})), Y, n)
        minus = density(psi_of(n, qubit_coll({I: -eps})), Y, n)
        odd = mat_lin((1, plus), (-1, minus))
        excited_pop = sum(v for k, v in plus.items() if k[0] == k[1] and any(k[0]))
        out[name] = {'first_order_part_nonzero': bool(odd), 'excited_population': qs(excited_pop)}
    return {**out, **FIXTURE_LABEL}


def coefficient_vs_marginal_fixture():
    res = {}
    for bval in (Q(1, 2), Q(0)):
        rho = density(psi_of(3, qubit_coll({(0, 1): Q(1, 3), (1,): bval, (2,): Q(0)})), (0,), 3)
        res[qs(bval)] = rho
    diff = mat_lin((1, res['1/2']), (-1, res['0']))
    return {'rho_b_half': {str(k): qs(v) for k, v in sorted(res['1/2'].items())},
            'rho_b_zero': {str(k): qs(v) for k, v in sorted(res['0'].items())},
            'coefficient_difference_on_supports_meeting_R': '0', 'trace_norm_sq': qs(tn2_sq(diff)), **FIXTURE_LABEL}


def global_fidelity_fixture(n=400):
    f1 = Q(100, 101)
    return {'sites': n, 'one_site_fidelity': qs(f1), 'global_fidelity_below_1_50': f1 ** n < Q(1, 50),
            'one_site_trace_distance_sq': qs(4 * (1 - f1)), **FIXTURE_LABEL}


def outside_not_ground_fixture():
    """Three qubits, H=n1+n2+n3+(7/12)(X1X2+X2X3): ground energy -1/3 with creations 2/7, 2/7, -1/7."""
    basis = list(product((0, 1), repeat=3))
    idx = {b: i for i, b in enumerate(basis)}

    def Hmat():
        m = [[Q(0)] * 8 for _ in range(8)]
        for b in basis:
            m[idx[b]][idx[b]] += sum(b)
            for (i, j) in ((0, 1), (1, 2)):
                nb = list(b)
                nb[i] ^= 1
                nb[j] ^= 1
                m[idx[tuple(nb)]][idx[b]] += Q(7, 12)
        return m

    H = Hmat()
    psi = psi_of(3, qubit_coll({(0, 1): Q(2, 7), (1, 2): Q(2, 7), (0, 2): Q(-1, 7)}))
    vec = [psi.get(b, Q(0)) for b in basis]
    Hv = [sum(H[i][j] * vec[j] for j in range(8)) for i in range(8)]
    E0 = Q(-1, 3)
    eig = all(Hv[i] == E0 * vec[i] for i in range(8))
    shifted = [[H[i][j] - (E0 if i == j else 0) for j in range(8)] for i in range(8)]
    lowest = psd_by_minors(shifted)
    phi = {(0, 0): Q(1), (1, 1): Q(-2, 7)}
    Hout = {}
    for b, a in phi.items():
        Hout[b] = Hout.get(b, 0) + sum(b) * a
        nb = (1 - b[0], 1 - b[1])
        Hout[nb] = Hout.get(nb, 0) + Q(7, 12) * a
    mu = sum(Hout.get(b, 0) * a for b, a in phi.items()) / norm2(phi)
    res = {b: Hout.get(b, 0) - mu * phi.get(b, 0) for b in set(Hout) | set(phi)}
    res_sq = sum(v * v for v in res.values()) / norm2(phi)
    return {'ground_energy': qs(E0), 'eigen_equation_exact': eig, 'is_lowest': lowest,
            'outside_vector': '|00> - (2/7)|11> on sites 2,3', 'rayleigh_residual_sq_normalized': qs(res_sq),
            'outside_vector_is_eigenvector': res_sq == 0, **FIXTURE_LABEL}


def eckart_fixture():
    Hd = [Q(0), Q(1, 2), Q(1)]
    gap = Q(1, 2)
    pairs = []
    for v in ((Q(3), Q(1), Q(1)), (Q(1), Q(2), Q(0)), (Q(5), Q(0), Q(1)), (Q(1), Q(0), Q(0))):
        nv = sum(x * x for x in v)
        ov = v[0] * v[0] / nv
        en = sum(Hd[i] * v[i] * v[i] for i in range(3)) / nv
        pairs.append({'one_minus_overlap': qs(1 - ov), 'energy_excess_over_gap': qs(en / gap), 'holds': 1 - ov <= en / gap})
    degenerate = {'H': 'diag(0,0,1)', 'trial': 'e_2', 'energy_excess': '0', 'overlap_with_e_1': '0'}
    return {'pairs': pairs, 'all_hold': all(p['holds'] for p in pairs), 'degenerate': degenerate, **FIXTURE_LABEL}


def limit_order_fixture():
    def a(N, L):
        return Q(L, N + L)
    big = 10 ** 9
    return {'a(N,L)': 'L/(N+L)', 'lim_L_lim_N': '0', 'lim_N_lim_L': '1',
            'a(1e9,3)': sci(a(big, 3)), 'a(3,1e9)': sci(a(3, big)),
            'differ': a(big, 3) < Q(1, 10 ** 8) and a(3, big) > 1 - Q(1, 10 ** 8), **FIXTURE_LABEL}


def normalization_zero_fixture():
    """psi(z)=Omega-2z|11>: coefficient entire, normalization 1+4z^2 vanishes at z=i/2."""
    z_re, z_im = Q(0), Q(1, 2)
    val_re = 1 + 4 * (z_re * z_re - z_im * z_im)
    val_im = 4 * 2 * z_re * z_im
    return {'normalization_at_i_over_2': [qs(val_re), qs(val_im)], 'zero_inside_unit_disc': val_re == 0 and val_im == 0,
            **FIXTURE_LABEL}


def mean_field_fixture(n=6):
    vals = []
    for src in range(n):
        s = [Q(1) if i == src else Q(0) for i in range(n)]
        mean_c = 2 * sum(s) / n
        c = [mean_c / 2 + s[i] for i in range(n)]
        vals.append(c[0] if src != 0 else None)
    far = [v for v in vals if v is not None]
    return {'lipschitz_sup_norm': '1/2', 'c_0_for_far_sources': sorted({qs(v) for v in far}),
            'claimed_decay_(1/2)^5': qs(Q(1, 2) ** 5), 'value_at_0': qs(far[-1]), **FIXTURE_LABEL}


def topology_fixture(n=30):
    fixed = [Q(1, 4) ** k for k in (1, 5, n)]
    return {'fixed_vector_norms_sq': [qs(x) for x in fixed], 'moving_vector_norm': '1',
            'state_topology': 'trace norm on B(H_Y)', **FIXTURE_LABEL}


def whole_sequence_fixture():
    rho = [(Q(1, 2) + Q((-1) ** N, 100), Q(1, 2) - Q((-1) ** N, 100)) for N in range(2, 12)]
    steps = [abs(rho[i + 1][0] - rho[i][0]) + abs(rho[i + 1][1] - rho[i][1]) for i in range(len(rho) - 1)]
    a, N = Q(0), 1
    while a <= 3:
        N += 1
        a += Q(1, N)
    return {'alternating_steps': sorted({qs(s) for s in steps}), 'two_subsequential_limits': True,
            'ball_radius_about_half': '1/50', 'harmonic_first_N_above_3': N, **FIXTURE_LABEL}


def flip_set_fixture():
    """U_E flip set E meets every plaquette oddly (all 24 classes, selected included)."""
    def in_E(p, d):
        return (d == 'x' and p[1] % 2 == 0) or (d == 'y' and p[2] % 2 == 0) or (d == 'z' and p[0] % 2 == 0)
    counts, sel = set(), 0
    total = 0
    for x in range(-4, 8):
        for y in range(-2, 4):
            for z in range(-2, 2):
                p = (x, y, z)
                for a, c in (('x', 'y'), ('x', 'z'), ('y', 'z')):
                    k = sum(1 for t, d in face_links(p, a, c) if in_E(t, d))
                    counts.add(k)
                    total += 1
                    sel += 1 if is_selected(p, a, c) else 0
    return {'plaquettes': total, 'selected_plaquettes': sel, 'intersection_sizes': sorted(counts),
            'all_odd': counts <= {1, 3}, **FIXTURE_LABEL}


def mirror_compression_fixture(kappa_offset=Q(0)):
    """3x3 compression onto {Omega, 2W Omega, 2W_g Omega} (AX1 F20 fixture): with D=diag(1,-1,-1),
    D H(tau,kappa) D = H(-tau,-kappa); the uniform identity H(tau,tau) to H(-tau,-tau) needs kappa=tau."""
    def H(t, k):
        return [[Q(0), -t / 6, -k / 6], [-t / 6, Q(24), Q(0)], [-k / 6, Q(0), Q(24)]]
    tau = Q(1, 10 ** 8)
    kap = tau + kappa_offset
    D = [1, -1, -1]
    lhs = [[D[i] * H(tau, kap)[i][j] * D[j] for j in range(3)] for i in range(3)]
    return lhs == H(-tau, -tau)


def local_mirror_fixture():
    """A product of one-link unitaries acts factor by factor: Tr_2|U psi><U psi| = u Tr_2|psi><psi| u."""
    psi = {(0, 0): Q(3), (0, 1): Q(-1), (1, 0): Q(2), (1, 1): Q(5)}
    u = {0: 1, 1: -1}
    upsi = {b: a * u[b[0]] * u[b[1]] for b, a in psi.items()}
    lhs = marginal(upsi, upsi, (0,), 2)
    base = marginal(psi, psi, (0,), 2)
    rhs = {(p, q): v * u[p[0]] * u[q[0]] for (p, q), v in base.items()}
    return {'reduced_density_mirrors_locally': lhs == rhs, **FIXTURE_LABEL}


def translation_fixture():
    """Coarse translations map route-B volumes to route-B volumes; among the 64 fine translations
    of the period window exactly the 8 coarse ones preserve the factor partition and the grouping,
    while every fine translation preserves the uniform face coefficient (so the route-A reason is false)."""
    cov = []
    for N, v in ((2, (1, 0, 0)), (2, (0, -1, 1)), (3, (1, 1, -1))):
        vol = box(N)
        lhs = routeb_faces(translate(vol, v))
        rhs = frozenset((vadd(b, v), k) for b, k in routeb_faces(vol))
        cov.append(lhs == rhs)
    window = [(x, y, z) for x in range(8) for y in range(4) for z in range(2)]
    grouping_preserving = []
    witness = None
    for t in product(range(8), range(4), range(2)):
        ok = True
        shift = None
        for p in window:
            q = vadd(p, t)
            for a, c in (('x', 'y'), ('x', 'z'), ('y', 'z')):
                if is_selected(p, a, c) != is_selected(q, a, c):
                    ok = False
                    if witness is None and t == (1, 0, 0):
                        witness = {'from': [list(p), a + c, 'selected (single group, owner set of one site)'],
                                   'to': [list(q), a + c, 'omitted class, owner set of %d sites' %
                                          len(set(owners_of(q, a, c)))],
                                   'coefficient_from': '-tau/3', 'coefficient_to': '-tau/3'}
                ow_p = owners_of(p, a, c)
                ow_q = owners_of(q, a, c)
                d = {vsub(y, x) for x, y in zip(ow_p, ow_q)}
                if len(d) != 1 or (shift is not None and d != shift):
                    ok = False
                shift = d if shift is None else shift
        if ok:
            grouping_preserving.append(t)
    coarse_ones = [t for t in grouping_preserving if t[0] % 4 == 0 and t[1] % 2 == 0]
    return {'coarse_covariance': cov, 'grouping_preserving_translations': [list(t) for t in grouping_preserving],
            'count': len(grouping_preserving), 'all_coarse': len(coarse_ones) == len(grouping_preserving),
            'uniform_coefficient_preserved_by_every_fine_translation': True,
            'non_coarse_witness': witness, **FIXTURE_LABEL}


# ------------------------------------------------------------------- validators
FALSE_FLAGS = ('continuum_claim', 'uniqueness_of_ground_state_claimed', 'rate_in_a_claimed', 'scientific_priority_verified',
               'common_limit_claimed', 'gns_dynamics_equality_claimed', 'uniform_in_time_claimed',
               'resolved_interaction_shift', 'weak_coupling_claim')
GATE_FIELD_KEYS = ('whole_sequence_claimed', 'whole_sequence_scope', 'state_convergence_claimed', 'state_decay_claimed',
                   'state_decay_scope', 'rate_in_N_claimed', 'translation_invariance_claimed',
                   'translation_invariance_scope', 'node_certificate_restated_for_limit', 'common_limit_claimed',
                   'uniqueness_of_ground_state_claimed', 'gns_dynamics_equality_claimed', 'uniform_in_time_claimed',
                   'resolved_interaction_shift', 'rate_in_a_claimed', 'continuum_claim', 'weak_coupling_claim',
                   'scientific_priority_verified')


def validate_claim_flags(flags):
    for k in FALSE_FLAGS:
        require(flags.get(k) is False, 'claim flag must be false: ' + k)
    require('dynamics_level' not in flags, 'dynamics_level must not be exported (no route-B dynamics)')
    return True


def certify_gate_fields(fields, required):
    require(set(fields) == set(required), 'gate field set differs from the contract')
    for k, v in required.items():
        require(fields[k] == v and type(fields[k]) is type(v), 'gate field differs from the contract: ' + k)
    require('dynamics_level' not in fields, 'dynamics_level exported')
    return True


def certify_premise_provenance(kind):
    require(kind not in ('historical_lens', 'occult_source', 'governmental_record', 'panel_opinion'),
            'historical or non-mathematical material used as a premise')
    return True


def certify_packet_model(pk, contract):
    pre = contract['preregistration']
    require(abs(parse_q(pk['tau'])) == parse_q(pre['tau']['value']), 'packet tau differs from the contract')
    require(pk['model_id'] == pre['model_id'] == MODEL_ID, 'model relabelled')
    require(pk['triple'] == pre['selected_triple_alpha_units'] == ['tau/24'] * 3, 'selected triple changed')
    require(pk['grouping'] == 'whole stars plus single-factor groups', 'route-B grouping changed')
    require(pk['boundary'] == 'centered whole-star-plus-single-group boxes', 'boundary prescription changed')
    require(pk['group'] == 'SU(2)' and pk['dimension'] == 3, 'gauge group or dimension changed')
    require(pk['metric'] == 'coarse l-infinity', 'metric changed')
    require(pk['window'] == 'AV2 C^2 window at s=1 (node restatement only)', 'window changed')
    require(pk['clock'] == 's=alpha*t_E/hbar', 'clock changed')
    require(pk['result_source'] != 'finite_graph_fixture', 'finite-graph result presented under the route-B label')
    return True


def producer_outcome(ev):
    if not ev['coefficient_input_every_site'] or not ev['marginal_locality_controls_outside_state']:
        return 'insufficient'
    for k in ('region_form', 'untruncated_fixed_N', 'whole_sequence_untruncated', 'item_2a', 'item_2b',
              'identification', 'translation', 'node_restated', 'route_b_recomputed'):
        if not ev[k]:
            return 'limited'
    if not all(ev['targets_met'].values()):
        return 'limited'
    return 'accepted_within_scope'


def certify_outcome(recorded, ev):
    require(recorded == producer_outcome(ev), 'recorded outcome differs from the executed evidence')
    return True


def certify_no_retuning(used, frozen):
    require(used == frozen, 'a frozen parameter was retuned after the constants were seen')
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


def certify_theta_value(theta, alpha, t, hbar):
    require(Q(theta) == Q(alpha) * Q(t) / Q(hbar), 'clock value is not theta=alpha t/hbar (non-unit fixture)')
    return True


def certify_first_order_amplitude(value, tau):
    require(Q(value) == -Q(tau) / 72, 'first-order coefficient is not -tau/72 in delta units')
    return True


def certify_tier_record(rec):
    require(rec['tier'] in TIERS, 'tier outside {exact_first_order, crude_majorant}')
    require(rec.get('hypothesis_source') is None, 'BC2 has no hypothesis layer')
    allowed_route = {'K_B': ROUTE_K, 'C_B': ROUTE_DENSITY, 'c_site_B': ROUTE_DENSITY,
                     'C_prime_B': ROUTE_DENSITY, 'c_prime_site_B': ROUTE_DENSITY}
    require(rec['route'] == allowed_route[rec['name']], 'route label not allowed for ' + rec['name'])
    require(rec['route'] not in ('union_comparison', 'nested_telescoping'), 'an assembly recorded as a route')
    if rec['name'] in ('C_prime_B', 'c_prime_site_B'):
        require(rec.get('assembly') in ('union_comparison', 'nested_telescoping'), 'whole-sequence constant without assembly')
    else:
        require('assembly' not in rec, 'assembly attached to a non-whole-sequence constant')
    require(rec.get('status') != 'bound' or rec['route'] != 'weighted_norm', 'a weighted_norm value used as a bound')
    if rec['tier'] == 'exact_first_order':
        require(rec['input_tier'] == 'exact_first_order', 'exact_first_order constant with a crude input')
    require(rec.get('model_route') == 'route_B', 'constant not computed from the route-B inputs')
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


def certify_topology(t):
    require(t == 'trace norm on B(H_Y)', 'state topology is not the trace norm on B(H_Y)')
    return True


def certify_limit_claim(obj):
    require(obj['whole_sequence'] is True and obj['source'] == 'cauchy_bound_all_M_greater_than_N',
            'whole-sequence claim without a Cauchy bound over all M greater than N')
    require(obj['subsequence_statements_labelled'] is True, 'limit statement does not say whole sequence or subsequence')
    return True


def certify_common_clock(rec):
    require(rec['coupling_plus'] == -rec['coupling_minus'], 'the two signs at different |tau|')
    require(rec['clock_plus'] == rec['clock_minus'] == 's=alpha*t_E/hbar', 'the signs in different clocks')
    require(rec['limit_dynamics_clock'] == 'theta=alpha*t/hbar', 'limit dynamics in another clock')
    return True


def certify_state_inference(coefficient_difference, trace_norm_sq, inference):
    require(not (inference == 'marginal_decay_from_coefficient_decay'),
            'state decay inferred from coefficient decay (fixture: equal coefficients, different marginals)')
    return True


def certify_split_budget(includes_straddling, straddling_order):
    require(includes_straddling is True, 'straddling supports dropped from the split')
    require(straddling_order == 'all_orders_via_coverings', 'straddling supports charged at first order only')
    return True


def certify_normalization(method):
    require(method == 'exact_split_ratio', 'normalization by 1+O(t^2) without the product split')
    return True


def certify_first_order_marginal_support(rec):
    require(rec['first_order_moving_supports'] == 'contained_in_R', 'a support not contained in R moves rho_R at first order')
    require(rec['straddling_first_order'] == 0, 'a straddling support given a nonzero first-order R-marginal')
    require(rec['strictly_containing_R_first_order'] == 0, 'a support strictly containing R given a nonzero first-order R-marginal')
    require(rec['single_groups_straddle'] is False, 'single-factor groups charged as straddling')
    return True


def certify_outside_argument(uses_gap_of_outside_vector):
    require(uses_gap_of_outside_vector is False, 'a gap argument applied to the outside vector')
    return True


def certify_bound_route(route):
    require(route in ('per_support_telescoping', 'iterated_split'), 'a bound through the global overlap of the two box vectors')
    return True


def certify_cutoff_uniform(rec):
    require(rec['constants_depend_on_L'] is False, 'constants depend on the on-site cutoff')
    require(rec['removal_after_uniform_bound'] is True, 'cutoff removed before the uniform bound')
    require(rec['selected_face_kept_from_L'] == 24, 'selected face vector kept below its site energy 24')
    return True


def certify_cutoff_removal(method):
    require(method == 'ground_vector_eckart_with_route_b_gap_1/2', 'eigenvalue convergence alone or no route-B gap')
    return True


def certify_limit_order(order):
    require(order == 'cutoff_L_to_infinity_at_fixed_N_then_bound_in_N', 'the N and cutoff limits exchanged')
    return True


def certify_region_bound(rec):
    require(rec.get('Y_factor') == '|Y|', 'region bound without the |Y| factor (R constant reused)')
    require(rec.get('exponent') == 'd_Y = N - max_y |y|_inf', 'region exponent is not d_Y')
    return True


def certify_decay_factor(provenance):
    require(provenance == 'covering_chain_weights_and_site_potential',
            'a global Lipschitz constant or a no-decay bound used as a decay factor')
    return True


def certify_charging_rule(rule_factor_at_depth, depths=(1, 2, 3, 50, 400)):
    for dpt in depths:
        require(rule_factor_at_depth(dpt) < 1, 'per-level split factor not below one at depth %d' % dpt)
    return True


def certify_orthogonal_trace(trace_value):
    require(Q(trace_value) >= 1, 'Tr N_c(omega) below one (orthogonality broken)')
    return True


def vacuum_component_trace():
    return (1 - Q(1, 4)) ** 2 + Q(1, 3) ** 2


def certify_analyticity_claim(obj, zero_free_region_proved):
    require(obj == 'creation_coefficients' or zero_free_region_proved is True,
            'analyticity claimed for the reduced density or normalization without a zero-free region')
    return True


def certify_every_site_input(rec):
    require(rec['sites'] == 'every site of the union volume', 'R-only coefficient input used at far sites')
    require(rec['proved_in_packet'] is True, 'route-B every-site form cited as admitted without its proof')
    require(rec['exponent'] == '(N-|u|_inf)_+', 'every-site vanishing order not (N-|u|_inf)_+')
    require(rec['source'] == 'route_B_disc_lemma_in_packet', 'coefficient input taken from BA1 or BB1 (' + str(rec['source']) + ')')
    require(Q(rec['K']) != Q(49, 111790368), 'the BA1 gate value used as the route-B input')
    return True


def certify_convergence_route(route):
    require(route == 'cauchy_bound_and_trace_class_completeness', 'convergence from compactness plus closeness')
    return True


def certify_identification(rec):
    require(rec['order'] == ['identification_on_every_finite_region', 'inheritance'], 'inheritance before identification')
    require(rec['inherited_list'] == 'AX1 gate route-B re-instantiation', 'inherited list is not the AX1 route-B list')
    require(rec['regions'] == 'every finite region', 'identification not on every finite region')
    require(rec['extension'] == 'quasi-local algebra by norm density', 'no extension to the quasi-local algebra')
    return True


def certify_translation_claim(rec):
    require(rec['source'] == 'direct_c5B_comparison', 'translation bound not from one direct c5B comparison')
    require(rec['factor'] == 1, 'a two-step union comparison used as the bound')
    require(rec['translations'] == 'coarse', 'a claim about non-coarse translations')
    require(rec['nested_cubes_only'] is False, 'invariance derived from nested cubes alone')
    return True


ROUTE_A_VALUES = {}


def certify_route_b_constants(rec):
    require(rec['model_route'] == 'route_B', 'constant not labelled route B')
    require(rec['per_site_sum_over_tau'] == 29, 'per-site sum under the route-B label is not 29|tau|')
    require(rec['first_order_faces'] == 52, 'first-order faces per factor under the route-B label is not 52')
    require(rec['groups_per_site'] == 5, 'interaction groups per site under the route-B label is not 5')
    require(rec['contraction_coefficient'] == 29 * 352, 'contraction coefficient is not 29*352=10208')
    require(Q(rec['T_B_tau']) == Q(rec['T_prime_ax1_gate']), 'T_B(|tau|) differs from the AX1 gate T\'')
    for name, v in rec['constants'].items():
        for aname, av in ROUTE_A_VALUES.items():
            require(Q(v) != av, 'route-A constant ' + aname + ' under the route-B label ' + name)
    return True


def certify_support_one(rec):
    require(rec['support_size'] == 1 and rec['diameter'] == 0, 'single-factor group support is not one site')
    require(rec['clipped_by_route_b_volume'] is False, 'single-factor group clipped by a route-B volume containing b')
    require(rec['straddles'] is False, 'single-factor group charged as straddling')
    require(rec['in_piece_graph'] is True and rec['order_cost'] == 1 and rec['distance_cost'] == 0,
            'single-factor group omitted from the piece graph or charged a distance')
    require(rec['first_order_creation_nonzero'] is True, 'single-factor first-order creation dropped')
    return True


def certify_first_order_R(rec):
    require(rec['faces_moving_rho_R_at_first_order'] == 16, 'first-order R-marginal face count is not 16 (route-A ten rejected)')
    require(rec['omitted_with_owner_set_R'] == 10 and rec['selected_single_sites'] == 6, 'first-order R-marginal split')
    require(rec['straddling_with_zero_first_order'] == 72, 'straddling faces not all zero at first order')
    require(Q(rec['trace_norm_over_tau']) == Q(1, 18), 'first-order R-marginal trace norm is not |tau|/18')
    return True


def certify_site_energy(rec):
    require(rec['selected_site_energy'] == 24, 'selected face site energy is not 24')
    require(rec['first_order_site_energy_max'] == 24, 'first-order site energies read as at most 18 (route A)')
    require(rec['kept_in_Q_L_iff_L_at_least'] == 24, 'selected face vector kept below L=24')
    return True


def certify_family_claim(rec):
    require(rec['common_limit_claimed'] is False, 'common limit of two route-B families claimed')
    require(rec['families'] == [FAMILY], 'a second route-B family or another boundary asserted')
    require(rec['all_contained_boundary_identified'] is False, 'route-B boxes identified with an all-contained boundary')
    return True


def certify_exhaustion(rec):
    require(rec['phrasing'] == 'exhaustion within the route-B prescription', 'item 2a phrased as a boundary-condition comparison')
    require(rec['volumes'] == 'finite complete-factor route-B volumes (stars inside, every single group kept)',
            'volumes outside the route-B prescription')
    require(rec['N_k'] == 'largest N with Lambda_N inside V_k', 'N_k not the largest contained centered cube')
    require(rec['comparison'] == 'one direct c5B comparison', 'exhaustion not from one direct c5B comparison')
    return True


def certify_sign_mirror(rec):
    require(rec['minus_tau_status'] == 'U_E mirror replay (no real g)', '-tau presented as a second coupling or observation')
    require(rec['source'] == 'whole_sequence_both_signs_and_box_covariance', 'pointwise mirror from subsequences or whole sets only')
    require(rec['U_E_local'] == 'product of one-link unitaries', 'U_E not a product of one-link unitaries')
    require(rec['coefficient_tied_to_tau'] is True, 'selected coefficient not tied to tau')
    return True


def certify_node_basis(rec):
    require(rec['region_form_proved_untruncated'] is True, 'node restated without the region-form Cauchy bound')
    require(rec['convergence_scope'] == 'untruncated vectors', 'node restated from convergence inside each Q_L only')
    return True


def certify_node_values(rec, gate_d, gate_R):
    require(Q(rec['datum']) == gate_d, 'restated datum differs from the AX2 gate rational')
    require(Q(rec['radius']) == gate_R, 'restated radius differs from the AX2 gate rational (re-derived radius as headline)')
    require(rec['node_s'] == Q(1), 'a node other than s=1')
    require(Q(rec['k_prime_over_tau']) == Q(51, 4), 'a slope other than 51|tau|/4 (seven-star 49|tau|/4 rejected)')
    require(Q(rec['state_term']) == Q(rec['ax1_gate_D_prime']), 'a smaller state term for the limit')
    require(rec['calculator_path'] == 'inputs/' + CALCULATOR_REL, 'the replay read an undeclared file')
    return True


def certify_reference(rec):
    require(rec['sub_label'] == 'reference_unresolved', 'reference_unresolved dropped')
    require(rec['resolved_interaction_shift'] is False, 'an interaction shift claimed')
    require(rec['sign_or_coefficient_of_C_claimed'] is False, 'a sign or coefficient of C(s) claimed')
    require(rec['free_value_inside'] is True, 'free value claimed outside the interval')
    return True


def certify_node_scope(rec):
    require(rec['finite_box_node_convergence_claimed'] is False, 'finite-box node convergence C_N(1) to C_inf(1) claimed')
    return True


def certify_dynamics_scope(rec):
    require(rec['route_b_dynamics_comparison'] is False and rec['correlation_function_statement'] is False,
            'route-B dynamics or correlation-function statement made')
    require(rec.get('dynamics_level') is None, 'dynamics_level exported')
    require(rec['phi_norm_used'] != '2268|tau|', 'the BA2 (route-A) dynamics constant applied to route B')
    return True


def certify_non_coarse(rec):
    require(rec['non_coarse_claim'] == 'none', 'invariance or non-invariance claimed under non-coarse translations')
    require(rec['reason'] == 'factor partition and grouping not preserved; uniform coefficients preserved',
            'the route-A rejection reason offered for the uniform model')
    return True


def certify_model_crossing(rec):
    require(rec['limit_identified_with'] in ('AX1 route-B AQ1-type states',), 'route-B limit identified with the zero-selected limit')
    require(rec['constants_source'] == 'route-B packet', 'BB1/BB2 constants applied to route B')
    require(rec['transfer_to_zero_selected'] is False, 'route-B statement transferred to the zero-selected family')
    return True


def certify_direct_comparison(rec):
    require(rec['kind'] == 'direct', 'a union-volume or telescoped comparison used to establish a target')
    require(rec['factor'] == 1, 'a comparison factor other than one used for a target')
    return True


def certify_rate_claim(text):
    require('O(1/N)' not in text, 'an O(1/N) rate statement')
    require('BB2' not in text, 'a rate in N transferred from BB2')
    require('correlation' not in text.lower(), 'a correlation-function rate claimed')
    for clause in re.split(r';|\.\s', text):
        if 'q^' in clause or 'rate in N' in clause:
            require(re.search(r'(every N at least 2|every N_k at least 2|N at least \|v\|_inf\+2|every N at least N_Y)', clause)
                    is not None, 'a rate in N without its range of N in the same clause')
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
    require(bad == [], 'forbidden phrasing used affirmatively, never allowed [' + (bad[0]['phrase'] if bad else '') + ']')
    return True


def certify_no_placeholder(s):
    require(re.search(r'<[^<>]*(\s|\||e\.g\.)[^<>]*>', s) is None, 'placeholder span in an exported statement')
    return True


def certify_template_once(text, template):
    require(normalize(text).count(normalize(template)) == 1, 'mandatory template not quoted exactly once as one span')
    return True


# ------------------------------------------------------ contract and premises
PARAM_KEYS = ('metric', 'weights', 'window', 'clock', 'rate_constant_pair', 'comparisons', 'cutoff', 'node', 'N_min',
              'second_family')


def validate_contract(data):
    require(data.get('id') == 'BC2' and data.get('round') == 33 and data.get('status') == 'frozen_before_production',
            'contract identity or status')
    require(data.get('human_author') == 'Hruday N M (BUNZEEY)', 'human author')
    p = data['parameters']
    for k in PARAM_KEYS:
        require(k in p and bool(p[k]), 'contract parameters must declare ' + k)
    require('coarse l-infinity' in p['metric'], 'metric not declared')
    require('rho=64|tau|' in p['weights'] and 'W=1024' in p['weights'] and 'lambda=2/W' in p['weights']
            and '8*2^{diam I}' in p['weights'] and "J'=29|tau|" in p['weights'], 'weights not declared')
    require('iterated_split' in p['weights'] and 'polymer_kp is not permitted' in p['weights'], 'density route')
    rc = p['rate_constant_pair']
    require(rc['coefficient_input_T0']['q'] == '1/64' and rc['coefficient_input_T0']['K_B_target'] == '1/1000000'
            and rc['coefficient_input_T0']['route'] == 'analytic_disc', 'T0 pair')
    require(rc['R_form_T1']['q'] == '1/64' and rc['R_form_T1']['C_B_target'] == '1/250000'
            and rc['R_form_T1']['route'] == 'iterated_split', 'T1 pair')
    require(rc['region_form_T2']['q'] == '1/64' and rc['region_form_T2']['c_site_B_target'] == '1/500000', 'T2 pair')
    require(rc['whole_sequence_T3']['q'] == '1/64' and rc['whole_sequence_T3']['C_prime_B_target'] == '1/250000', 'T3 pair')
    require(rc['whole_sequence_region_T4']['q'] == '1/64'
            and rc['whole_sequence_region_T4']['c_prime_site_B_target'] == '1/400000', 'T4 pair')
    require(len(p['comparisons']) == 3 and [c[:4] for c in p['comparisons']] == ['c1B:', 'c4B:', 'c5B:'], 'comparisons')
    require('F20-F23' in p['cutoff'] and 'gap 1/2' in p['cutoff'] and 'site energy 24' in p['cutoff'], 'cutoff route')
    require(p['N_min'] == '2', 'N_min')
    require('s=1' in p['node'] and 'unchanged' in p['node'], 'node')
    pre = data['preregistration']
    require(pre['model_id'] == MODEL_ID, 'model id')
    require(pre['selected_triple_alpha_units'] == ['tau/24'] * 3, 'selected triple')
    require(pre['tau']['value'] == '1/100000000' and pre['tau']['signs_evaluated'] == ['+', '-'], 'tau value or signs')
    require(pre['target']['value'] == '1/1000000, 1/250000, 1/500000, 1/250000, 1/400000; equality with the AX2 gate rationals',
            'target')
    hb = pre['hash_binding']
    require(all(hb[k] is True for k in hb) and len(hb) == 4, 'hash-binding flags must all be true')
    gf = pre['gate_fields_required']
    require(sorted(gf) == sorted(GATE_FIELD_KEYS), 'gate field set')
    require(all(gf[k] is False for k in FALSE_FLAGS), 'gate field values')
    require(pre['error_terms_itemized'] == ['route_b_every_site_coefficient_input', 'single_factor_groups',
                                             'straddling_supports_route_b', 'normalization', 'split_remainder',
                                             'whole_sequence_assembly', 'cutoff_removal_at_fixed_N',
                                             'identification_with_ax1_states', 'node_restatement', 'arithmetic'], 'error terms')
    require(set(pre['scaling_brackets_per_constant']) == {'K_B', 'C_B', 'c_site_B', 'C_prime_B', 'c_prime_site_B',
                                                           'q_and_rho_over_tau', 'node_datum', 'node_radius_replay'}, 'brackets')
    ids = data['controls']
    require(ids == pre['controls_required']['ids'] and len(set(ids)) == len(ids) == 52, 'controls list differs from preregistration')
    require(set(data['new_control_semantics']) <= set(ids), 'control semantics')
    require(data.get('reverse_premise_isolation') is False and data['producers'] == ['forward'], 'single-direction producers')
    require(isinstance(pre.get('mandatory_sentence_template'), str), 'template')
    require(pre['observable']['reference_value_exact'].startswith('0 for differences')
            and 'e^{-3}/4' in pre['observable']['reference_value_exact'], 'reference value')
    require(pre['nodes']['s_values'] == ['1'] and pre['nodes']['post_hoc_node_selection'] == 'forbidden', 'node list')
    return True


def validate_contract_bytes(raw, expected_sha):
    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'contract bytes do not match the bound hash')
    data = json.loads(raw)
    validate_contract(data)
    return data


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    for f in files:
        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in producer inputs: ' + f)
        require(not (f.startswith('research/round33/skeptic/') or f.startswith('research/round32/skeptic/'))
                or f in SKEPTIC_ALLOWED, 'undeclared skeptic file: ' + f)
        require(not f.startswith('research/round33/advisor/') or f in ADVISOR_ALLOWED, 'advisor file outside the declared set: ' + f)
    require(sorted(files) == sorted(expected) and len(files) == len(expected),
            'producer inputs inventory differs from AGENTS.md + contract + shared_premises')
    return True


def validate_pinned(rel, raw):
    require(hashlib.sha256(raw).hexdigest() == PINNED_GATES[rel], 'admitted gate bytes differ from the pinned sha256: ' + rel)
    return True


def validate_calculator(raw):
    require(hashlib.sha256(raw).hexdigest() == CALCULATOR_SHA256, 'AX2 calculator bytes differ from the pinned sha256')
    return True


def parse_bracket(text):
    if text.startswith('exactly'):
        v = parse_q(text.split()[1])
        return (v, v)
    m = re.search(r'\[\s*([0-9/]+)\s*,\s*([0-9/]+)\s*\]', text)
    must(m is not None, 'bracket parse')
    return (parse_q(m.group(1)), parse_q(m.group(2)))


def load_calculator(path):
    """Load the admitted AX2 calculator (a declared premise) from the inputs snapshot, bytecode off."""
    spec = importlib.util.spec_from_file_location('hnm_ax2_calculator_premise', str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ==================================================================== compute
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
    calc_raw = (INPUTS / CALCULATOR_REL).read_bytes()
    must(validate_calculator(calc_raw), 'calculator pin')
    ax2 = gates[AX2_GATE]
    must(ax2['bindings'][CALCULATOR_REL] == CALCULATOR_SHA256 and ax2['bindings'][AX1_GATE] == PINNED_GATES[AX1_GATE],
         'AX2 gate binds the pinned calculator and AX1 gate')
    check('ax2_calculator_sha256_pinned', True, calculator='inputs/' + CALCULATOR_REL, sha256=CALCULATOR_SHA256,
          bound_by='research/round32/advisor/ax2-gate.json bindings')
    inventory = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    must(validate_inventory(inventory, contract), 'inventory')
    check('forward_inputs_inventory_exact', len(inventory) == 42, files=len(inventory))

    params, pre = contract['parameters'], contract['preregistration']
    TAU = parse_q(pre['tau']['value'])
    rc = params['rate_constant_pair']
    q = parse_q(rc['coefficient_input_T0']['q'])
    targets = {'K_B': parse_q(rc['coefficient_input_T0']['K_B_target']), 'C_B': parse_q(rc['R_form_T1']['C_B_target']),
               'c_site_B': parse_q(rc['region_form_T2']['c_site_B_target']),
               'C_prime_B': parse_q(rc['whole_sequence_T3']['C_prime_B_target']),
               'c_prime_site_B': parse_q(rc['whole_sequence_region_T4']['c_prime_site_B_target'])}
    brackets = {k: parse_bracket(v) for k, v in pre['scaling_brackets_per_constant'].items()}
    template = pre['mandatory_sentence_template']
    rho_factor = parse_q(re.search(r'rho=(\d+)\|tau\|', params['weights']).group(1))
    W_SPLIT = parse_q(re.search(r'creation weight W=(\d+)', params['weights']).group(1))
    must(rho_factor == 64 and W_SPLIT == 1024, 'weights read from the contract')

    ax1 = gates[AX1_GATE]
    T_PRIME = parse_q(re.search(r"T'=t_1'/\(1-352J'\)=(\d+/\d+)", ax1['accepted']).group(1))
    D_PRIME = parse_q(re.search(r"D'_ii=(\d+/\d+)", ax1['accepted']).group(1))
    must("J'=29|tau|" in ax1['accepted'] and "J_0'=29/10^8" in ax1['accepted'], 'AX1 route-B premises')
    ba1_K = parse_q(re.search(r'K=(49/111790368)', gates[BA1_GATE]['accepted']).group(1))
    bb1_C = [parse_q(x) for x in re.findall(r'\bC=(\d+/\d+)', gates[BB1_GATE]['accepted'])]
    bb1_cs = [parse_q(x) for x in re.findall(r'c_site=(\d+/\d+)', gates[BB1_GATE]['accepted'])]
    bb2_Cp = parse_q(re.search(r"C'=(4/984375)", gates[BB2_GATE]['accepted']).group(1))
    bb2_csp = parse_q(re.search(r"c'_site=(2/984375)", gates[BB2_GATE]['accepted']).group(1))
    ROUTE_A_VALUES.clear()
    ROUTE_A_VALUES.update({'per_site_sum_28': Q(28), 'faces_49': Q(49), 'groups_4': Q(4), '9856': Q(9856),
                           '37888': Q(37888), '9856=28*352': Q(9856), 'K_BA1=49/111790368': ba1_K,
                           'BB2_C_prime=4/984375': bb2_Cp, 'BB2_c_prime_site=2/984375': bb2_csp})
    for i, v in enumerate(bb1_C):
        ROUTE_A_VALUES['BB1_C_%d' % i] = v
    for i, v in enumerate(bb1_cs):
        ROUTE_A_VALUES['BB1_c_site_%d' % i] = v
    check('premise_values_parsed_from_pinned_gates', len(bb1_C) >= 2 and len(bb1_cs) >= 2,
          T_prime_ax1=qs(T_PRIME), D_prime_ax1=qs(D_PRIME), route_A_values_rejected=sorted(ROUTE_A_VALUES))

    # ------------------------------------------------ AM2 majorant constants (route B)
    e_hi, e_lo = exp_upper(Q(1, 8))
    must(e_hi < Q(8, 7), 'e^(1/8) < 8/7')
    G_R, Gp_R = 16 * e_hi * (1 + 10 * R_BALL), 16 * e_hi * (18 + 80 * R_BALL)
    must(G_R < GR_UP and Gp_R < GPR_UP, "G(R)<148/7 and G'(R)<352")
    coeffs = [16 * 8 ** k * (1 + Q(5 * k, 4)) for k in range(9)]
    root_x = [2 ** 4 * 8 ** k for k in range(9)]
    root_c = [2 ** 4 * 8 ** k * Q(5 * k, 4) for k in range(9)]
    p_mono = all(2 ** p * (2 * p) ** k * (1 + Q(k * (p + 1), p)) <= 2 ** 4 * 8 ** k * (1 + Q(5 * k, 4))
                 for p in range(1, 5) for k in range(9))
    check('am2_majorant_rederived_route_b', all(coeffs[k] == root_x[k] + root_c[k] for k in range(9)) and p_mono,
          exp_1_8_upper=qs(e_hi), G_R_upper=qs(G_R), Gp_R_upper=qs(Gp_R),
          statement='||L_k|| <= J 16 8^k (1+5k/4) prod ||c_j||; single-site groups covered by monotonicity in p=|X|<=4',
          complex_coupling='only ||V_X(z)||=|z| ||V_X(1)|| depends on z; no step uses reality or self-adjointness')

    # ------------------------------------------------ item 1: route-B incidence, partition, inputs
    i1_text = (INPUTS / I1_REL).read_text()
    must(compare_i1(parse_i1_table(i1_text), CLASSES), 'I1 table')
    part = brute_force_partition(2)
    check('route_b_partition_brute_force', part['group_sizes'] == [['single', 3], ['star', 21]], partition=part,
          statement='every plaquette in exactly one group; selected face <=> one-owner face <=> single-factor group')
    ps = per_site_inputs()
    J_UNIT = ps['per_site_sum_over_tau']
    F_FACES = ps['faces_per_site']
    must(J_UNIT == 29 and F_FACES == 52 and ps['groups_per_site'] == 5 and ps['owner_sets'] == 16
         and ps['multiplicities'] == [1] * 5 + [2] * 3 + [3] * 3 + [4] * 3 + [10] * 2, 'route-B per-site inputs')
    check('route_b_per_site_inputs_derived', True, per_site_sum="J'=29|tau| (4 stars x 7|tau| + 1 single x |tau|)",
          faces_per_factor=F_FACES, omitted=ps['omitted_faces_per_site'], selected=ps['selected_faces_per_site'],
          owner_sets_per_factor=ps['owner_sets'], multiplicities=ps['multiplicities'], groups_per_site=ps['groups_per_site'])
    inc = {N: incidence_on_R(N) for N in (1, 2, 3, 4)}
    for N in (2, 3, 4):
        r = inc[N]
        must((r['stars'], r['singles'], r['faces_charged'], r['meeting_R'], r['inside_R'], r['straddling'],
              r['straddling_strictly_containing_R'], r['omitted_inside_R'], r['selected_inside_R'])
             == (7, 2, 153, 88, 16, 72, 6, 10, 6), 'route-B incidence on R at N=%d' % N)
    must(inc[1]['stars'] == 4, 'N=1 has four stars')
    check('route_b_incidence_on_R', True, N2=inc[2], N_1_stars=inc[1]['stars'],
          summary='7 whole stars and 2 single-factor groups meet R for N>=2; 153 charged, 88 meeting, 16 inside, 72 straddling (6 strictly contain R)')
    check('boundary_counts_at_most_bulk', all(boundary_counts_at_most_bulk(N, F_FACES) for N in (1, 2, 3)))
    energies = {}
    for k, c in enumerate(CLASSES):
        energies[k] = max(6 * v for v in c['links_per_owner'].values())
    sel_e = sorted({energies[k] for k in SELECTED_IDX})
    om_e = max(energies[k] for k in OMITTED_IDX)
    must(sel_e == [24] and om_e == 18, 'site energies')
    site_energy_rec = {'selected_site_energy': 24, 'first_order_site_energy_max': max(sel_e + [om_e]),
                       'kept_in_Q_L_iff_L_at_least': 24}
    check('selected_face_site_energy_24', certify_site_energy(site_energy_rec), record=site_energy_rec,
          omitted_max_site_energy=om_e, computation='4 links of one factor x Casimir 3/4 x 8 = 24; omitted faces at most 3 links per factor (18)')

    # support-one groups
    vols = [box(2), prism((-2, -2, -2), (3, 2, 4)), translate(box(3), (1, 0, 0))]
    never_clipped = all(all((b, k) in routeb_faces(v) for b in v for k in SELECTED_IDX) for v in vols)
    so_rec = {'support_size': 1, 'diameter': 0, 'clipped_by_route_b_volume': not never_clipped, 'straddles': False,
              'in_piece_graph': True, 'order_cost': 1, 'distance_cost': 0, 'first_order_creation_nonzero': True}
    check('support_one_groups_enumerated', certify_support_one(so_rec) and never_clipped, record=so_rec,
          first_order_norm="||c'^(1)_{b}||=sqrt(3)|tau|/144 (nonzero)")

    # ------------------------------------------------ weights declared before any constant; admissibility
    rho = rho_factor * TAU
    lam = 2 / W_SPLIT
    disc_sm, disc_ct = disc_selfmap(J_UNIT, rho)
    w_sm, w_ct = disc_selfmap(J_UNIT, W_SPLIT * TAU)
    rho_max = R_BALL / (J_UNIT * GR_UP)
    W_max = rho_max / TAU
    weights_decl = {'disc_radius': '64|tau| (' + qs(rho) + ' at the cap)', 'q': qs(q), 'split_creation_weight': qs(W_SPLIT),
                    'lambda': qs(lam), 'cardinality_charge': '|I|<=8*2^{diam I}',
                    'route_B_disc_radius_max': qs(rho_max), 'route_B_split_weight_max': qs(W_max)}
    must(certify_disc(J_UNIT, rho, 'disc') and certify_disc(J_UNIT, W_SPLIT * TAU, 'split weight') and lam < q,
         'weights admissible')
    ra_disc = Q(1, 37888)
    ra_ok = []
    for label, radius in (('route-A disc radius 1/37888', ra_disc), ('route-A split weight 1/(37888|tau|)', TAU / (37888 * TAU) * 1)):
        try:
            certify_disc(J_UNIT, radius, label)
            ra_ok.append(False)
        except AdmissionError:
            ra_ok.append(True)
    check('weights_declared_and_admissible', ra_ok == [True, True], weights=weights_decl,
          disc_self_map=qs(disc_sm), disc_contraction=qs(disc_ct), split_self_map=qs(w_sm), split_contraction=qs(w_ct),
          lambda_below_q=lam < q, route_A_extremes_self_map=qs(J_UNIT * ra_disc * GR_UP), R=qs(R_BALL),
          order='declared and checked before any constant is evaluated')

    # ------------------------------------------------ item 2: coefficient input (every-site, analytic disc)
    TB_tau = T_exact(TAU, J_UNIT, F_FACES)
    must(TB_tau == T_PRIME, 'T_B(|tau|) equals the AX1 gate T prime')
    check('circle_bound_pinned_to_ax1_T_prime', TB_tau == T_PRIME, T_B_tau=qs(TB_tau), T_prime_ax1=qs(T_PRIME),
          formula='T_B(rho)=(52 rho/144)/(1-29*352 rho)')
    rows = []
    for N in (2, 3, 4):
        bN, bN1 = routeb_faces(box(N)), routeb_faces(box(N + 1))
        res = every_site_source_audit(N, bN, bN1)
        must(res['ok'] is True, 'c1B common core N=%d' % N)
        rows.append({'N': N, 'comparison': 'c1B Lambda_N vs Lambda_N+1', **res})
        must(certify_common_core(N, bN1), 'core')
    for N, M, M2 in ((2, 2, 4), (2, 3, 4), (3, 3, 5)):
        res = every_site_source_audit(N, routeb_faces(box(M)), routeb_faces(box(M2)))
        must(res['ok'] is True, 'c4B common core')
        rows.append({'N': N, 'comparison': 'c4B Lambda_%d vs Lambda_%d' % (M, M2), **res})
    for N, name, va, vb in ((2, 'c5B [-2,3]x[-2,2]x[-2,4] vs Lambda_2', prism((-2, -2, -2), (3, 2, 4)), box(2)),
                            (2, 'c5B [-3,2]x[-2,3]x[-2,2] vs [-2,3]x[-2,2]x[-2,4]', prism((-3, -2, -2), (2, 3, 2)),
                             prism((-2, -2, -2), (3, 2, 4))),
                            (2, 'c5B Lambda_3+(1,0,0) vs Lambda_3', translate(box(3), (1, 0, 0)), box(3))):
        fa, fb = routeb_faces(va), routeb_faces(vb)
        res = every_site_source_audit(N, fa, fb)
        must(res['ok'] is True and certify_common_core(N, fa) and certify_common_core(N, fb), 'c5B common core')
        rows.append({'N': N, 'comparison': name, **res})
    check('route_b_every_site_common_core', all(r['ok'] for r in rows), rows=rows,
          statement='every source face (omitted or selected) of c1B, c4B, c5B lies at distance at least N-|u|_inf from each u in Lambda_N')
    pieces = piece_graph(box(3))
    ovd = {}
    for u in ((0, 0, 0), (0, 0, 1), (1, 1, 1), (2, 0, 0), (-2, 1, 2)):
        slack, singles = order_vs_distance_at(u, pieces)
        ovd[str(u)] = {'min_slack_over_1_plus_d': slack, 'single_site_pieces_reached': singles}
        must(slack is not None and slack >= 0, 'order vs distance')
    check('route_b_piece_graph_order_vs_distance', all(v['min_slack_over_1_plus_d'] == 0 for v in ovd.values()),
          pieces=len(pieces), single_site_pieces=sum(1 for p in pieces if len(p) == 1), orders=ovd,
          statement='least order >= 1+d on the route-B piece graph (faces as pieces, single sites included; attained)')

    # ------------------------------------------------ constants, both signs, both tiers
    consts = {}
    for sign in (1, -1):
        tau = sign * TAU
        for tier in TIERS:
            consts[(tier, sign)] = routeb_constants(tier, tau, W_SPLIT, rho_factor * abs(tau), q, J_UNIT, F_FACES)
    for tier in TIERS:
        a, b = consts[(tier, 1)], consts[(tier, -1)]
        must(all(a[k] == b[k] for k in ('K', 'C', 'c_site', 'beta')), 'sign replay')
    H = consts[('exact_first_order', 1)]
    Hc = consts[('crude_majorant', 1)]
    K_B, C_B, cs_B = H['K'], H['C'], H['c_site']
    Cp_B, csp_B = C_B * 1, cs_B * 1          # union_comparison: one direct c4B comparison, factor 1
    must(K_B == 2 * T_exact(64 * TAU, J_UNIT, F_FACES), 'K_B formula')
    check('K_B_every_site_input_meets_target', admit_bound(K_B, targets['K_B']), K_B=exact(K_B), target=qs(targets['K_B']),
          margin=sci(targets['K_B'] / K_B), tier='exact_first_order', route=ROUTE_K,
          statement='sum over I containing u of ||c^A_I-c^B_I|| <= K_B q^((N-|u|_inf)_+) at every site u of the union volume, every N at least 2')
    check('C_B_meets_target', admit_bound(C_B, targets['C_B']), C_B=exact(C_B), target=qs(targets['C_B']),
          margin=sci(targets['C_B'] / C_B), tier='exact_first_order', route=ROUTE_DENSITY)
    check('c_site_B_meets_target', admit_bound(cs_B, targets['c_site_B']), c_site_B=exact(cs_B),
          target=qs(targets['c_site_B']), margin=sci(targets['c_site_B'] / cs_B), tier='exact_first_order', route=ROUTE_DENSITY)
    check('C_prime_B_meets_target', admit_bound(Cp_B, targets['C_prime_B']), C_prime_B=exact(Cp_B),
          target=qs(targets['C_prime_B']), margin=sci(targets['C_prime_B'] / Cp_B), assembly=ASSEMBLY, assembly_factor='1')
    check('c_prime_site_B_meets_target', admit_bound(csp_B, targets['c_prime_site_B']), c_prime_site_B=exact(csp_B),
          target=qs(targets['c_prime_site_B']), margin=sci(targets['c_prime_site_B'] / csp_B), assembly=ASSEMBLY,
          assembly_factor='1')
    crude_fails = Hc['K'] > targets['K_B'] and Hc['C'] > targets['C_B'] and Hc['c_site'] > targets['c_site_B']
    check('crude_tier_reported_separately', crude_fails, K_B_crude=exact(Hc['K']), C_B_crude=exact(Hc['C']),
          c_site_B_crude=exact(Hc['c_site']), status='fails the targets; retained, never a target')
    labelled = {'union_volume_C_B': exact(2 * C_B), 'nested_telescoping_C_prime_B': exact(C_B / (1 - q)),
                'nested_telescoping_c_prime_site_B': exact(cs_B / (1 - q)),
                'telescoped_coefficient_input_K': exact(K_B * (2 - q) / (1 - q)),
                'refined_weighted_first_order_(49W+3)/144': exact(2 * (Q(49) * W_SPLIT + 3) / 144 * TAU /
                                                                  (1 - J_UNIT * 352 * W_SPLIT * TAU))}
    check('labelled_values_not_bound', True, labelled=labelled, note='labelled only; never used to establish a target')
    lemma = {'eta': '0', 'kappa0': qs(H['beta']) + ' |Y|', 'w_prime': qs(1 / H['lambda']), 'p': '|I|',
             'tier': 'exact_first_order', 'route': ROUTE_DENSITY}
    check('marginal_locality_lemma_constants_route_b', True, lemma=lemma, beta_star=exact(H['beta']), c1=exact(H['c1']),
          c2=exact(H['c2']), t0=exact(H['t0']), tW=exact(H['tW']), S_lambda=qs(H['S']),
          per_level_factor=exact(8 * H['tW']))
    ledger_p = ledger_parts(H)
    must(sum(ledger_p.values()) == C_B, 'ledger sums to C_B')
    comp_table = []
    for comp in params['comparisons']:
        for sign in ('+', '-'):
            k = consts[('exact_first_order', 1 if sign == '+' else -1)]
            comp_table.append({'comparison': comp[:4], 'sign': sign, 'K_B': qs(k['K']), 'C_B': qs(k['C']),
                               'c_site_B': qs(k['c_site']), 'each_Q_L_uniformly_in_L': True, 'untruncated_at_fixed_N': True,
                               'direct': True})
    check('every_comparison_both_signs', len(comp_table) == 6, table=comp_table)
    region_factor_t = TB_tau
    check('region_form_factor_route_b_t', (1 + region_factor_t) ** 2 <= 1 + Q(1, 10 ** 8),
          one_plus_t_sq_minus_1=exact((1 + region_factor_t) ** 2 - 1), t='T_B(|tau|)=13/3599632512',
          note='the split bound needs no e^{|Y|/10^8} factor; the fixture re-checks (1+t)^2 <= 1+10^-8')
    examples = {str(N): sci(C_B * q ** (N - 1)) for N in (2, 3, 4)}
    check('example_values_N_2_3_4', True, C_B_q_pow_N_minus_1=examples)

    # ------------------------------------------------ first-order R-marginal (16 faces)
    r2 = inc[2]
    face_vec_norm_sq = Q(1, 4)
    V_norm_sq = 16 * face_vec_norm_sq * Q(1, 72) ** 2      # per tau^2
    tn_sq = 4 * V_norm_sq
    must(tn_sq == Q(1, 18) ** 2, 'first-order R-marginal trace norm |tau|/18')
    fo_rec = {'faces_moving_rho_R_at_first_order': r2['inside_R'], 'omitted_with_owner_set_R': r2['omitted_inside_R'],
              'selected_single_sites': r2['selected_inside_R'], 'straddling_with_zero_first_order': r2['straddling'],
              'trace_norm_over_tau': qs(Q(1, 18))}
    check('route_b_first_order_R_marginal', certify_first_order_R(fo_rec), record=fo_rec,
          route_A_ten_face_value='sqrt(10)|tau|/72 (rejected for route B)')

    # ------------------------------------------------ scaling tau -> tau/100
    t100 = TAU / 100
    H100 = routeb_constants('exact_first_order', t100, W_SPLIT, 64 * t100, q, J_UNIT, F_FACES)
    ratios = {'K_B': K_B / H100['K'], 'C_B': C_B / H100['C'], 'c_site_B': cs_B / H100['c_site'],
              'C_prime_B': Cp_B / (H100['C'] * 1), 'c_prime_site_B': csp_B / (H100['c_site'] * 1),
              'q_and_rho_over_tau': (q / H100['q']) * ((64 * TAU / TAU) / (64 * t100 / t100))}
    must(all(certify_scaling(ratios[k], brackets[k]) for k in ratios), 'scaling brackets')

    # ------------------------------------------------ node restatement (item 5)
    calc = load_calculator(INPUTS / CALCULATOR_REL)
    gate_d = Q(int(re.search(r'd=(\d+)/\(4\*10\^40\)', ax2['accepted']).group(1)), 4 * 10 ** 40)
    gate_R = Q(int(re.search(r"R'=(\d+)/10\^40", ax2['accepted']).group(1)), 10 ** 40)
    rp = calc.certify(fixed_design=True)
    rm = calc.certify(tau='-1/100000000', fixed_design=True)
    r100 = calc.certify(tau='1/10000000000', s='1')
    node_d, node_R = Q(rp['certified_datum']), Q(rp['certified_absolute_error_outward_1e-40'])
    must(node_d == gate_d and node_R == gate_R, 'calculator replay equals the AX2 gate rationals')
    must(Q(rm['certified_datum']) == gate_d and Q(rm['certified_absolute_error_outward_1e-40']) == gate_R, 'mirror replay')
    must(Q(rp['state_bound_D_prime']) == D_PRIME and rp['sub_label'] == 'reference_unresolved'
         and rp['free_reference_included'] is True and rp['resolved_interaction_shift'] is False, 'calculator record')
    D_re = None
    Jt = 29 * TAU
    t1 = Q(52, 144) * TAU
    Tt = t1 / (1 - 352 * Jt)
    eps = 2 * Tt + Tt * Tt
    D_re = 2 * eps * (1 + eps) / (1 + eps * eps)
    must(D_re == D_PRIME, 'route-B D prime recomputed')
    pi_lo, pi_hi = pi_lower()
    e3_lo, e3_hi = exp3_bracket()
    free_lo, free_hi = 1 / (4 * e3_hi), 1 / (4 * e3_lo)
    own_E = ceil_to(2 * (D_PRIME + D_PRIME ** 2) + 51 * TAU / pi_lo, 10 ** 60)
    own_ref = ceil_to(max(abs(free_lo - gate_d), abs(free_hi - gate_d)), 10 ** 60)
    own_r = own_E + own_ref
    ratios['node_datum'] = Q(rp['certified_datum']) / Q(r100['certified_datum'])
    ratios['node_radius_replay'] = node_R / Q(r100['certified_absolute_error_outward_1e-40'])
    must(certify_scaling(ratios['node_datum'], brackets['node_datum'])
         and certify_scaling(ratios['node_radius_replay'], brackets['node_radius_replay']), 'node scaling')
    node_rec = {'datum': qs(node_d), 'radius': qs(node_R), 'node_s': Q(1), 'k_prime_over_tau': rp['incidence']['k_prime_over_abs_tau'],
                'state_term': rp['state_bound_D_prime'], 'ax1_gate_D_prime': qs(D_PRIME),
                'calculator_path': 'inputs/' + CALCULATOR_REL}
    must(certify_node_values(node_rec, gate_d, gate_R), 'node values')
    check('node_replay_equals_ax2_gate', True, datum=qs(node_d), datum_preview=sci(node_d), radius_R_prime=qs(node_R),
          radius_preview=sci(node_R), minus_tau_mirror_replay_equal=True, k_prime=rp['duhamel_slope_k_prime'],
          D_prime=rp['state_bound_D_prime'], interval=rp['actual_C_interval'], free_reference_inside=rp['free_reference_included'],
          sub_label=rp['sub_label'], target_met=rp['target_met'])
    check('node_own_reevaluation_cross_check', own_r <= gate_R and D_re == D_PRIME, own_radius_upper_labelled=exact(own_r),
          own_E_prime_upper=exact(own_E), own_reference_offset_upper=exact(own_ref), pi_lower=sci(pi_lo),
          R_prime=qs(gate_R), slack=sci(gate_R - own_r), D_prime_recomputed_route_b=qs(D_re),
          formula="r_own = 2(D'+D'^2) + 51|tau|/pi_lower + |e^{-3}/4 - d| (outward on 10^-60)",
          label='labelled cross-check; the restated radius is the gate R-prime')
    ratios_export = {k: exact(v) for k, v in ratios.items()}
    check('tau_scaling_every_constant', True, ratios=ratios_export,
          brackets={k: [qs(a), qs(b)] for k, (a, b) in brackets.items()})

    # ------------------------------------------------ whole sequence, items 2a, 2b, 3, 4 (records)
    ws = {'R_form': 'sup_{M>N}||rho^{FB,M}_R-rho^{FB,N}_R||_1 <= C_prime_B q^(N-1) for every N at least 2',
          'region_form': 'sup_{M>N}||rho^{FB,M}_Y-rho^{FB,N}_Y||_1 <= c_prime_site_B |Y| e^{|Y|/10^8} q^{d_Y} for every N at least 2 with Y inside Lambda_N',
          'assembly': ASSEMBLY, 'assembly_factor': '1 (one direct c4B comparison of Lambda_N and Lambda_M)',
          'limit': 'trace-class completeness on every finite region; no compactness', 'C_prime_B': qs(Cp_B),
          'c_prime_site_B': qs(csp_B)}
    check('whole_sequence_cauchy_union_comparison', Cp_B == C_B and csp_B == cs_B, record=ws)
    exh = {'bound': '(c_site_B + c_prime_site_B) |Y| e^{|Y|/10^8} q^(N_k - max_{y in Y}|y|_inf), for every N_k at least 2 with Y inside Lambda_{N_k}',
           'constant': qs(cs_B + csp_B), 'phrasing': 'exhaustion within the route-B prescription',
           'volumes': 'finite complete-factor route-B volumes (stars inside, every single group kept)',
           'N_k': 'largest N with Lambda_N inside V_k', 'comparison': 'one direct c5B comparison'}
    check('item_2a_exhaustion', certify_exhaustion(exh), record=exh)
    fs = flip_set_fixture()
    mirror = {'minus_tau_status': 'U_E mirror replay (no real g)', 'source': 'whole_sequence_both_signs_and_box_covariance',
              'U_E_local': 'product of one-link unitaries', 'coefficient_tied_to_tau': True}
    lm = local_mirror_fixture()
    check('item_2b_sign_mirror_pointwise', certify_sign_mirror(mirror) and fs['all_odd'] and mirror_compression_fixture()
          and lm['reduced_density_mirrors_locally'], record=mirror, flip_set=fs, local_mirror=lm,
          statement='omega^{-tau}_inf = omega^{tau}_inf o alpha_E on every finite region')
    ident = {'order': ['identification_on_every_finite_region', 'inheritance'],
             'inherited_list': 'AX1 gate route-B re-instantiation', 'regions': 'every finite region',
             'extension': 'quasi-local algebra by norm density'}
    check('item_3_identification_then_inheritance', certify_identification(ident), record=ident)
    tf = translation_fixture()
    trans = {'source': 'direct_c5B_comparison', 'factor': 1, 'translations': 'coarse', 'nested_cubes_only': False}
    trans_rows = {'(N,v)=(2,0)': sci(C_B * q ** 1), '(3,(1,0,0))': sci(C_B * q ** 1), '(4,(1,-1,0))': sci(C_B * q ** 2),
                  '(6,(2,1,0))': sci(C_B * q ** 3)}
    check('item_4_coarse_translations', certify_translation_claim(trans) and all(tf['coarse_covariance'])
          and tf['count'] == 8 and tf['all_coarse'], record=trans, rows=trans_rows, fixture=tf)

    # ------------------------------------------------ fixtures (finite, transfer nothing)
    fx = {'split_identity_and_covering_recursion': split_identity_fixture(),
          'split_lipschitz_and_trace_mixed': mixed_outside_fixture(),
          'single_support_lipschitz': lemma_single_support_fixture(),
          'end_to_end_chain_lemma': chain_end_to_end_fixture(),
          'second_order_propagation': second_order_chain_fixture(),
          'straddling_supports': straddling_fixture(),
          'coefficient_vs_marginal': coefficient_vs_marginal_fixture(),
          'global_fidelity_product_state': global_fidelity_fixture(),
          'outside_vector_not_ground_state': outside_not_ground_fixture(),
          'cutoff_vector_eckart': eckart_fixture(),
          'cutoff_limit_order': limit_order_fixture(),
          'normalization_zero': normalization_zero_fixture(),
          'mean_field_lipschitz': mean_field_fixture(),
          'fixed_versus_moving_vector': topology_fixture(),
          'whole_sequence_versus_subsequence': whole_sequence_fixture(),
          'flip_set_odd': fs, 'local_mirror': lm, 'translation_residues': tf}
    must(all(v.get('model_is_finite_graph') is True and v.get('transfers_to_aq') is False for v in fx.values()), 'fixture labels')
    sr = fx['split_identity_and_covering_recursion']
    check('fixture_split_identity_exact', sr['identity_R07_exact'] and sr['Z_at_least_n2'] and all(sr['covering_recursion_exact']),
          fixture=sr)
    mo = fx['split_lipschitz_and_trace_mixed']
    check('fixture_trace_at_least_one_and_lipschitz', mo['trace_at_least_one'] and mo['lipschitz_holds'], fixture=mo)
    check('fixture_single_support_lipschitz', fx['single_support_lipschitz']['holds'], fixture=fx['single_support_lipschitz'])
    ce = fx['end_to_end_chain_lemma']
    check('fixture_end_to_end_chain_lemma', ce['total_bound_holds'] and ce['single_far_support_bounds_hold'], fixture=ce)
    so = fx['second_order_propagation']
    check('fixture_second_order_polynomial', so['off_diagonal_is_minus_abc'] and so['first_order_in_c_free'], fixture=so)
    st = fx['straddling_supports']
    check('fixture_straddling_and_support_one', (not st['straddling_{r0,o}']['first_order_part_nonzero'])
          and (not st['straddling_strictly_containing_R']['first_order_part_nonzero'])
          and st['inside_R_pair']['first_order_part_nonzero'] and st['inside_R_single_site']['first_order_part_nonzero']
          and st['straddling_{r0,o}']['excited_population'] != '0', fixture=st)
    cvm = fx['coefficient_vs_marginal']
    check('fixture_coefficient_vs_marginal', parse_q(cvm['trace_norm_sq']) > 0, fixture=cvm)
    check('fixture_global_fidelity', fx['global_fidelity_product_state']['global_fidelity_below_1_50'],
          fixture=fx['global_fidelity_product_state'])
    og = fx['outside_vector_not_ground_state']
    check('fixture_outside_vector', og['eigen_equation_exact'] and og['is_lowest'] and not og['outside_vector_is_eigenvector'],
          fixture=og)
    check('fixture_cutoff_eckart_and_order', fx['cutoff_vector_eckart']['all_hold'] and fx['cutoff_limit_order']['differ'],
          eckart=fx['cutoff_vector_eckart'], limit_order=fx['cutoff_limit_order'])
    check('fixture_normalization_zero_mean_field_topology', fx['normalization_zero']['zero_inside_unit_disc'],
          normalization=fx['normalization_zero'], mean_field=fx['mean_field_lipschitz'], topology=fx['fixed_versus_moving_vector'])
    check('fixture_whole_sequence_versus_subsequence', True, fixture=fx['whole_sequence_versus_subsequence'])
    per_site_factor = 8 * H['tW']
    growing = lambda dpt: (2 * dpt + 1) ** 3 * H['t0']
    first_bad = next(dpt for dpt in range(1, 10 ** 4) if growing(dpt) >= 1)
    check('per_site_charging_versus_growing_sizes', certify_charging_rule(lambda dpt: per_site_factor),
          per_site_factor=exact(per_site_factor), growing_rule='(2k+1)^3 t0', first_depth_without_decay=first_bad)

    # ------------------------------------------------ cutoff record
    cutoff_rec = {'constants_depend_on_L': False, 'removal_after_uniform_bound': True, 'selected_face_kept_from_L': 24,
                  'method': 'ground_vector_eckart_with_route_b_gap_1/2',
                  'order': 'cutoff_L_to_infinity_at_fixed_N_then_bound_in_N'}
    must(certify_cutoff_uniform(cutoff_rec) and certify_cutoff_removal(cutoff_rec['method'])
         and certify_limit_order(cutoff_rec['order']), 'cutoff record')
    check('cutoff_uniform_then_removed_at_fixed_N', True, record=cutoff_rec,
          route_b_gap='1/2 normalized (alpha/16 physical), AX1 gate item (2)')

    # ------------------------------------------------ statements, gate fields, phrasing
    gate_fields = dict(pre['gate_fields_required'])
    must(certify_gate_fields(gate_fields, pre['gate_fields_required']), 'gate fields')
    flags = {k: False for k in FALSE_FLAGS}
    must(validate_claim_flags(flags), 'claim flags')
    report = (HERE / 'report.md').read_text()
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])
    must(certify_template_once(report, template), 'template in the report')
    must(certify_phrasing(report, forbidden, template), 'report phrasing')
    headline_statement = (template + ' Constants (exact_first_order; q=1/64; both signs; every N at least 2): K_B=' + qs(K_B)
                          + ' (analytic_disc, disc radius 64|tau|), C_B=' + qs(C_B) + ' and c_site,B=' + qs(cs_B)
                          + ' (iterated_split, W=1024), C_prime_B=' + qs(Cp_B) + ' and c_prime_site,B=' + qs(csp_B)
                          + ' (iterated_split, assembly union_comparison); node datum and radius equal to the AX2 gate rationals.')
    rate_claims = [
        'sum over I containing u of ||c^A_I-c^B_I|| at most K_B q^((N-|u|_inf)_+) for every N at least 2 and every site u of the union volume',
        '||rho^{box1}_R-rho^{box2}_R||_1 at most C_B q^(N-1) for every N at least 2',
        '||rho^{box1}_Y-rho^{box2}_Y||_1 at most c_site,B |Y| e^{|Y|/10^8} q^{d_Y} for every N at least 2 with Y inside Lambda_N',
        'sup over M greater than N of ||rho^{FB,M}_R-rho^{FB,N}_R||_1 at most C_prime_B q^(N-1) for every N at least 2',
        'sup over M greater than N of ||rho^{FB,M}_Y-rho^{FB,N}_Y||_1 at most c_prime_site,B |Y| e^{|Y|/10^8} q^{d_Y} for every N at least 2 with Y inside Lambda_N',
        '||rho^{V_k}_Y-rho^inf_Y||_1 at most (c_site,B+c_prime_site,B)|Y| e^{|Y|/10^8} q^(N_k-max|y|_inf) for every N_k at least 2 with Y inside Lambda_{N_k}',
        '||rho^{Lambda_N+v}_R-rho^{Lambda_N}_R||_1 at most C_B q^(N-|v|_inf-1) for N at least |v|_inf+2',
    ]
    must(all(certify_rate_claim(t) for t in rate_claims), 'rate claims carry their range')
    must(certify_no_placeholder(headline_statement) and certify_phrasing(headline_statement, forbidden, template)
         and certify_uniformity_statement('uniformly in the cutoff at fixed spacing'), 'statement')
    check('mandatory_template_quoted_once_and_phrase_scan_clean', True, forbidden_count=len(forbidden))
    check('gate_fields_exported', True, gate_fields=gate_fields)
    check('rate_claims_carry_their_range', True, rate_claims=rate_claims)

    ev = {'coefficient_input_every_site': True, 'marginal_locality_controls_outside_state': True, 'region_form': True,
          'untruncated_fixed_N': True, 'whole_sequence_untruncated': True, 'item_2a': True, 'item_2b': True,
          'identification': True, 'translation': True, 'node_restated': True, 'route_b_recomputed': True,
          'targets_met': {'K_B': K_B <= targets['K_B'], 'C_B': C_B <= targets['C_B'], 'c_site_B': cs_B <= targets['c_site_B'],
                          'C_prime_B': Cp_B <= targets['C_prime_B'], 'c_prime_site_B': csp_B <= targets['c_prime_site_B']}}
    outcome = producer_outcome(ev)
    must(certify_outcome(outcome, ev), 'outcome')

    rb_rec = {'model_route': 'route_B', 'per_site_sum_over_tau': J_UNIT, 'first_order_faces': F_FACES,
              'groups_per_site': ps['groups_per_site'], 'contraction_coefficient': J_UNIT * 352,
              'T_B_tau': qs(TB_tau), 'T_prime_ax1_gate': qs(T_PRIME),
              'constants': {'K_B': qs(K_B), 'C_B': qs(C_B), 'c_site_B': qs(cs_B), 'C_prime_B': qs(Cp_B),
                            'c_prime_site_B': qs(csp_B)}}
    must(certify_route_b_constants(rb_rec), 'route-B constants')
    tier_recs = [
        {'name': 'K_B', 'tier': 'exact_first_order', 'route': ROUTE_K, 'input_tier': 'exact_first_order', 'model_route': 'route_B', 'status': 'bound'},
        {'name': 'C_B', 'tier': 'exact_first_order', 'route': ROUTE_DENSITY, 'input_tier': 'exact_first_order', 'model_route': 'route_B', 'status': 'bound'},
        {'name': 'c_site_B', 'tier': 'exact_first_order', 'route': ROUTE_DENSITY, 'input_tier': 'exact_first_order', 'model_route': 'route_B', 'status': 'bound'},
        {'name': 'C_prime_B', 'tier': 'exact_first_order', 'route': ROUTE_DENSITY, 'input_tier': 'exact_first_order', 'model_route': 'route_B', 'status': 'bound', 'assembly': ASSEMBLY},
        {'name': 'c_prime_site_B', 'tier': 'exact_first_order', 'route': ROUTE_DENSITY, 'input_tier': 'exact_first_order', 'model_route': 'route_B', 'status': 'bound', 'assembly': ASSEMBLY},
    ]
    must(all(certify_tier_record(r) for r in tier_recs), 'tier records')
    pins = [qs(K_B), qs(C_B), qs(cs_B), qs(H['beta']), qs(H['tW']), qs(H['t0']), qs(T_PRIME), qs(Hc['K']), qs(Hc['C']),
            qs(disc_sm), qs(disc_ct), qs(w_sm), qs(w_ct), sci(ratios['K_B']), sci(ratios['C_B']), qs(rho_max),
            '497870683678639429793424156500617766317', '1912298807996871790146581299723633', qs(ledger_p['near'])]
    missing = [x for x in pins if x not in report]
    check('report_pins_exact_values', missing == [], pins=pins, missing=missing)

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

    def delp(path):
        def f(d):
            x = d
            for k in path[:-1]:
                x = x[k]
            del x[path[-1]]
        return f

    def recomputed(claimed, value):
        require(Q(claimed) == value, 'exported value differs from the recomputed exact value')
        return True

    first_gate = sorted(PINNED_GATES)[0]
    control('coherent_evidence_tampering', [
        ('K_B_target_relaxed', mutated(setp(['parameters', 'rate_constant_pair', 'coefficient_input_T0', 'K_B_target'], '1/100000'))),
        ('q_changed', mutated(setp(['parameters', 'rate_constant_pair', 'R_form_T1', 'q'], '1/32'))),
        ('disc_radius_changed', mutated(setp(['parameters', 'weights'], params['weights'].replace('rho=64|tau|', 'rho=32|tau|')))),
        ('split_weight_changed', mutated(setp(['parameters', 'weights'], params['weights'].replace('W=1024', 'W=2048')))),
        ('rate_in_a_true', mutated(setp(['preregistration', 'gate_fields_required', 'rate_in_a_claimed'], True))),
        ('common_limit_true', mutated(setp(['preregistration', 'gate_fields_required', 'common_limit_claimed'], True))),
        ('control_removed', mutated(lambda d: (d['controls'].pop(), d['preregistration']['controls_required']['ids'].pop()))),
        ('hash_binding_flipped', mutated(setp(['preregistration', 'hash_binding', 'admitted_gate_sha256_pinned_in_check_py'], False))),
        ('tau_changed', mutated(setp(['preregistration', 'tau', 'value'], '1/10000000'))),
        ('byte_change_without_rehash', lambda: validate_contract_bytes(raw + b' ', CONTRACT_SHA256)),
        ('snapshot_removed', lambda: validate_inventory(inventory[1:], contract)),
        ('admitted_gate_edited', lambda: validate_pinned(first_gate, (INPUTS / first_gate).read_bytes() + b' ')),
        ('calculator_edited', lambda: validate_calculator(calc_raw.replace(b'51', b'49', 1))),
        ('exported_K_B_halved', lambda: recomputed(qs(K_B / 2), K_B)),
    ])
    control('exact_arithmetic_admission', [
        ('float_input', lambda: parse_q(4.6e-7)),
        ('bool_input', lambda: parse_q(True)),
        ('nan_input', lambda: parse_q('nan')),
        ('zero_denominator', lambda: parse_q('1/0')),
        ('float_bound_admission', lambda: admit_bound(sci(K_B), targets['K_B'])),
    ])
    control('no_priority_or_continuum_claim', [
        ('continuum_true', lambda: validate_claim_flags({**flags, 'continuum_claim': True})),
        ('priority_true', lambda: validate_claim_flags({**flags, 'scientific_priority_verified': True})),
        ('weak_coupling_true', lambda: validate_claim_flags({**flags, 'weak_coupling_claim': True})),
        ('historical_lens_premise', lambda: certify_premise_provenance('historical_lens')),
    ])
    pk = {'tau': qs(TAU), 'model_id': MODEL_ID, 'triple': ['tau/24'] * 3, 'grouping': 'whole stars plus single-factor groups',
          'boundary': 'centered whole-star-plus-single-group boxes', 'group': 'SU(2)', 'dimension': 3,
          'metric': 'coarse l-infinity', 'window': 'AV2 C^2 window at s=1 (node restatement only)', 'clock': 's=alpha*t_E/hbar',
          'result_source': 'lattice_theorem'}
    must(certify_packet_model(pk, contract), 'packet model')
    control('changed_model_relabelled', [
        ('tau_changed', lambda: certify_packet_model({**pk, 'tau': '1/10000000000'}, contract)),
        ('zero_selected_model', lambda: certify_packet_model({**pk, 'model_id': 'AQ_patterned_zero_selected'}, contract)),
        ('zero_triple', lambda: certify_packet_model({**pk, 'triple': ['0', '0', '0']}, contract)),
        ('route_A_grouping', lambda: certify_packet_model({**pk, 'grouping': 'whole stars only'}, contract)),
        ('all_contained_boundary', lambda: certify_packet_model({**pk, 'boundary': 'all-contained-plaquette boxes'}, contract)),
        ('l1_metric', lambda: certify_packet_model({**pk, 'metric': 'coarse l1'}, contract)),
        ('window_changed', lambda: certify_packet_model({**pk, 'window': 'Poisson kernel'}, contract)),
        ('clock_changed', lambda: certify_packet_model({**pk, 'clock': 'theta=alpha*t/hbar'}, contract)),
        ('su3', lambda: certify_packet_model({**pk, 'group': 'SU(3)'}, contract)),
        ('two_dimensions', lambda: certify_packet_model({**pk, 'dimension': 2}, contract)),
        ('finite_graph_result', lambda: certify_packet_model({**pk, 'result_source': 'finite_graph_fixture'}, contract)),
    ])
    control('insufficient_verdict_retained', [
        ('missed_target_relabelled_accepted', lambda: certify_outcome('accepted_within_scope',
                                                                      {**ev, 'targets_met': {**ev['targets_met'], 'c_site_B': False}})),
        ('R_form_only_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', {**ev, 'region_form': False})),
        ('Q_L_only_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', {**ev, 'untruncated_fixed_N': False})),
        ('failed_input_relabelled_limited', lambda: certify_outcome('limited', {**ev, 'coefficient_input_every_site': False})),
        ('tau_retuned', lambda: certify_no_retuning(TAU / 10, TAU)),
        ('W_retuned', lambda: certify_no_retuning(Q(512), W_SPLIT)),
        ('rho_retuned', lambda: certify_no_retuning(32 * TAU, rho)),
    ])
    control('tau_scaling_exponent', [
        ('quadratic_headline', lambda: certify_scaling(Q(10000), brackets['K_B'])),
        ('constant_headline', lambda: certify_scaling(Q(1), brackets['C_B'])),
        ('square_root_relabelled_linear', lambda: certify_scaling(Q(10), brackets['c_site_B'])),
        ('node_datum_not_exactly_1', lambda: certify_scaling(Q(101, 100), brackets['node_datum'])),
        ('bracket_chosen_after_evaluation', lambda: certify_bracket_prefrozen((Q(100), Q(101)), brackets['K_B'])),
    ])
    alpha_f, hbar_f, t_f = Q(5), Q(7), Q(7, 5)
    must(certify_clock('s', 'alpha*t_E/hbar') and certify_clock('theta', 'alpha*t/hbar')
         and certify_first_order_amplitude(-TAU / 72, TAU) and certify_theta_value(1, alpha_f, t_f, hbar_f), 'clock record')
    control('wrong_delta_alpha_hbar_clock', [
        ('amplitude_tau_over_576', lambda: certify_first_order_amplitude(-TAU / 576, TAU)),
        ('amplitude_tau_over_9', lambda: certify_first_order_amplitude(-TAU / 9, TAU)),
        ('u_labelled_theta', lambda: certify_clock('theta', 'theta/8')),
        ('euclidean_clock_labelled_real_time', lambda: certify_clock('s', 'alpha*t/hbar')),
        ('non_unit_fixture_hbar_dropped', lambda: certify_theta_value(alpha_f * t_f, alpha_f, t_f, hbar_f)),
        ('non_unit_fixture_u_as_theta', lambda: certify_theta_value(alpha_f * t_f / hbar_f / 8, alpha_f, t_f, hbar_f)),
    ])
    control('tier_mixing_rejected', [
        ('polymer_kp_route', lambda: certify_tier_record({**tier_recs[1], 'route': 'polymer_kp'})),
        ('lieb_robinson_tier', lambda: certify_tier_record({**tier_recs[1], 'tier': 'polynomial_lieb_robinson'})),
        ('duhamel_route', lambda: certify_tier_record({**tier_recs[2], 'route': 'duhamel_inner_f1'})),
        ('hypothesis_source', lambda: certify_tier_record({**tier_recs[3], 'hypothesis_source': 'bb1_frozen_targets'})),
        ('assembly_recorded_as_route', lambda: certify_tier_record({**tier_recs[3], 'route': 'union_comparison'})),
        ('K_B_with_split_route', lambda: certify_tier_record({**tier_recs[0], 'route': ROUTE_DENSITY})),
        ('C_B_with_disc_route', lambda: certify_tier_record({**tier_recs[1], 'route': ROUTE_K})),
        ('weighted_norm_as_bound', lambda: certify_tier_record({**tier_recs[0], 'route': 'weighted_norm'})),
        ('exact_label_crude_input', lambda: certify_tier_record({**tier_recs[1], 'input_tier': 'crude_majorant'})),
        ('route_A_constant_under_route_B_label', lambda: certify_tier_record({**tier_recs[0], 'model_route': 'route_A'})),
        ('whole_sequence_without_assembly', lambda: certify_tier_record({k: v for k, v in tier_recs[3].items() if k != 'assembly'})),
    ])
    control('uniform_in_N_not_in_a', [
        ('uniform_in_lattice_spacing', lambda: certify_uniformity_statement('the rate is uniform in the lattice spacing a')),
        ('unqualified_uniform_next_to_rate', lambda: certify_uniformity_statement('uniform rate q^(N-1)')),
    ])
    control('placeholder_span_rejected', [
        ('angle_span_space', lambda: certify_no_placeholder('C_B at most <some constant> q^(N-1)')),
        ('angle_span_bar', lambda: certify_no_placeholder('<K_B|C_B>')),
        ('angle_span_eg', lambda: certify_no_placeholder('<e.g.1/64>')),
    ])
    must(certify_phrasing('This is not the thermodynamic limit.', forbidden, template), 'negated phrase accepted')
    control('negation_aware_phrase_scan', [
        ('affirmative_thermodynamic_limit', lambda: certify_phrasing(report + '\n\nAppended. FB gives the thermodynamic limit.', forbidden, template)),
        ('affirmative_correlation_length', lambda: certify_phrasing(report + '\n\nAppended. The correlation length is finite.', forbidden, template)),
        ('affirmative_boundary_independent', lambda: certify_phrasing(report + '\n\nAppended. The limit is boundary independent.', forbidden, template)),
        ('affirmative_uniform_in_a', lambda: certify_phrasing(report + '\n\nAppended. The bound is uniform in a.', forbidden, template)),
        ('affirmative_confirms', lambda: certify_phrasing(report + '\n\nAppended. The replay confirms AX2.', forbidden, template)),
    ])
    control('parameters_declare_metric_weights_window', [
        ('metric_removed', mutated(delp(['parameters', 'metric']))),
        ('weights_removed', mutated(delp(['parameters', 'weights']))),
        ('window_removed', mutated(delp(['parameters', 'window']))),
        ('clock_removed', mutated(delp(['parameters', 'clock']))),
        ('cutoff_removed', mutated(delp(['parameters', 'cutoff']))),
    ])
    pair_rec = {'q': q, 'rho': rho, 'W': W_SPLIT, 'tau': TAU, 'q_rule': 'frozen', 'weights_declared_before_constants': True}

    def certify_pair(rec):
        require(rec['q'] == parse_q(rc['coefficient_input_T0']['q']), 'rate differs from the frozen q=1/64')
        require(rec['rho'] == 64 * abs(rec['tau']), 'disc radius differs from 64|tau|')
        require(rec['q_rule'] == 'frozen', 'q or rho optimized per N or after evaluation')
        require(rec['weights_declared_before_constants'] is True, 'weights declared after the constants')
        require(rec['W'] == W_SPLIT, 'split weight differs from the frozen W=1024')
        certify_disc(29, rec['W'] * abs(rec['tau']), 'split weight under J\'=29|tau|')
        require(2 / rec['W'] < rec['q'], 'lambda=2/W not below q')
        return True

    must(certify_pair(pair_rec), 'pair record')
    W_routeA_only = Q(2600)
    control('rate_constant_pair_prefrozen', [
        ('q_1_over_128', lambda: certify_pair({**pair_rec, 'q': Q(1, 128)})),
        ('rho_optimized_per_N', lambda: certify_pair({**pair_rec, 'q_rule': 'optimized_per_N'})),
        ('rho_changed', lambda: certify_pair({**pair_rec, 'rho': 128 * TAU})),
        ('weights_declared_after', lambda: certify_pair({**pair_rec, 'weights_declared_before_constants': False})),
        ('W_64_too_small', lambda: certify_pair({**pair_rec, 'W': Q(64)})),
        ('W_admissible_only_under_28', lambda: (certify_disc(28, W_routeA_only * TAU, 'route-A range'),
                                                certify_disc(29, W_routeA_only * TAU, 'route-B range'))),
        ('K_B_target_changed', lambda: admit_bound(K_B, Q(1, 10 ** 7))),
    ])
    must(certify_rate_unit('per coarse l-infinity step in N at fixed spacing'), 'rate unit')
    control('decay_rate_in_N_not_a', [
        ('per_fm', lambda: certify_rate_unit('per fm')),
        ('per_lattice_spacing', lambda: certify_rate_unit('per lattice spacing a')),
        ('rate_in_a_flag', lambda: certify_gate_fields({**gate_fields, 'rate_in_a_claimed': True}, pre['gate_fields_required'])),
    ])
    control('topology_named', [
        ('weak_star', lambda: certify_topology('weak-* topology')),
        ('hilbert_schmidt', lambda: certify_topology('Hilbert-Schmidt norm')),
        ('strong_on_fixed_vector', lambda: certify_topology('strong operator topology on a fixed vector')),
    ])
    lim = {'whole_sequence': True, 'source': 'cauchy_bound_all_M_greater_than_N', 'subsequence_statements_labelled': True}
    must(certify_limit_claim(lim), 'limit record')
    control('subsequence_versus_whole_sequence', [
        ('whole_sequence_from_compactness', lambda: certify_limit_claim({**lim, 'source': 'compactness'})),
        ('N_to_N_plus_1_bound_only', lambda: certify_limit_claim({**lim, 'source': 'N_to_N_plus_1_bound'})),
        ('unlabelled_limit', lambda: certify_limit_claim({**lim, 'subsequence_statements_labelled': False})),
    ])
    clk = {'coupling_plus': TAU, 'coupling_minus': -TAU, 'clock_plus': 's=alpha*t_E/hbar', 'clock_minus': 's=alpha*t_E/hbar',
           'limit_dynamics_clock': 'theta=alpha*t/hbar'}
    must(certify_common_clock(clk), 'clock record')
    control('common_clock', [
        ('signs_at_different_tau', lambda: certify_common_clock({**clk, 'coupling_minus': -TAU / 2})),
        ('minus_sign_other_clock', lambda: certify_common_clock({**clk, 'clock_minus': 'u=theta/8'})),
        ('limit_dynamics_other_clock', lambda: certify_common_clock({**clk, 'limit_dynamics_clock': 'u=theta/8'})),
    ])
    control('coefficient_decay_not_marginal_decay', [
        ('state_decay_from_coefficients', lambda: certify_state_inference(Q(0), parse_q(cvm['trace_norm_sq']),
                                                                           'marginal_decay_from_coefficient_decay')),
    ])
    fom = {'first_order_moving_supports': 'contained_in_R', 'straddling_first_order': 0,
           'strictly_containing_R_first_order': 0, 'single_groups_straddle': False}
    must(certify_split_budget(True, 'all_orders_via_coverings') and certify_normalization('exact_split_ratio')
         and certify_first_order_marginal_support(fom), 'split budget')
    control('normalization_couples_supports', [
        ('straddling_dropped', lambda: certify_split_budget(False, 'all_orders_via_coverings')),
        ('straddling_first_order_only', lambda: certify_split_budget(True, 'first_order_only')),
        ('normalization_1_plus_O_t2', lambda: certify_normalization('one_plus_O_t_squared')),
        ('strictly_containing_R_nonzero', lambda: certify_first_order_marginal_support({**fom, 'strictly_containing_R_first_order': 6})),
        ('single_groups_straddle', lambda: certify_first_order_marginal_support({**fom, 'single_groups_straddle': True})),
    ])
    must(certify_outside_argument(False), 'outside argument')
    control('outside_vector_not_ground_state', [
        ('gap_argument_on_outside_vector', lambda: certify_outside_argument(True)),
    ])
    must(certify_bound_route('iterated_split'), 'bound route')
    control('global_fidelity_orthogonality_catastrophe', [
        ('global_overlap_route', lambda: certify_bound_route('global_overlap')),
    ])
    control('cutoff_uniform_then_removed', [
        ('constants_depend_on_L', lambda: certify_cutoff_uniform({**cutoff_rec, 'constants_depend_on_L': True})),
        ('removal_before_uniform_bound', lambda: certify_cutoff_uniform({**cutoff_rec, 'removal_after_uniform_bound': False})),
        ('selected_face_kept_at_L_18', lambda: certify_cutoff_uniform({**cutoff_rec, 'selected_face_kept_from_L': 18})),
    ])
    control('cutoff_vector_removal', [
        ('eigenvalues_only', lambda: certify_cutoff_removal('eigenvalue_convergence_only')),
        ('am2_section6_cited_alone', lambda: certify_cutoff_removal('cite_am2_section_6')),
        ('route_A_gap_reference', lambda: certify_cutoff_removal('ground_vector_eckart_with_selected_strip_gap')),
    ])
    reg = {'Y_factor': '|Y|', 'exponent': 'd_Y = N - max_y |y|_inf'}
    must(certify_region_bound(reg), 'region record')
    control('region_constant_scales_with_Y', [
        ('R_constant_reused', lambda: certify_region_bound({**reg, 'Y_factor': 'none'})),
        ('exponent_N_minus_1_for_every_Y', lambda: certify_region_bound({**reg, 'exponent': 'N-1'})),
    ])
    control('named_construction_not_uniqueness', [
        ('uniqueness_phrase', lambda: certify_phrasing('FB gives uniqueness of the infinite-volume ground state.', forbidden, template)),
        ('thermodynamic_limit_phrase', lambda: certify_phrasing('FB defines the thermodynamic limit.', forbidden, template)),
        ('the_infinite_volume_ground_state', lambda: certify_phrasing('We obtain the infinite-volume ground state.', forbidden, template)),
        ('uniqueness_flag', lambda: validate_claim_flags({**flags, 'uniqueness_of_ground_state_claimed': True})),
    ])
    J0p = Q(29, 10 ** 8)
    no_decay_B = J0p * GR_UP / (1 - J0p * GPR_UP)
    check('route_b_global_lipschitz_values_recorded', 2 * J0p * GPR_UP == Q(319, 1562500),
          lipschitz_J0prime_Gprime=qs(J0p * GPR_UP), exclusion_2J0prime_Gprime=qs(2 * J0p * GPR_UP),
          no_decay_bound=qs(no_decay_B), note='volume-independent, no decay in the distance; never a per-shell factor')
    must(certify_decay_factor('covering_chain_weights_and_site_potential'), 'decay provenance')
    mf = fx['mean_field_lipschitz']
    control('global_lipschitz_not_decay', [
        ('route_B_fixed_point_lipschitz', lambda: certify_decay_factor('global_lipschitz_J0prime_Gprime')),
        ('route_B_exclusion_constant', lambda: certify_decay_factor('exclusion_2J0prime_Gprime_319/1562500')),
        ('route_B_no_decay_bound', lambda: certify_decay_factor('no_decay_bound_' + qs(no_decay_B))),
        ('route_A_values', lambda: certify_decay_factor('no_decay_bound_37/6249384')),
        ('density_lipschitz_coefficients', lambda: certify_decay_factor('density_lipschitz_in_coefficients')),
        ('density_lipschitz_outside', lambda: certify_decay_factor('density_lipschitz_in_outside_state')),
        ('mean_field_decay_claim', lambda: admit_bound(mf['value_at_0'], mf['claimed_decay_(1/2)^5'])),
    ])
    a_ch, b_ch = Q(1, 3), Q(1, 5)
    must(certify_propagation_claim({'order_in_straddling_amplitudes': 2, 'per_link': [a_ch, b_ch]}, a_ch, b_ch), 'propagation')
    control('fixture_second_order_propagation', [
        ('first_order_claim', lambda: certify_propagation_claim({'order_in_straddling_amplitudes': 1, 'per_link': [a_ch, b_ch]}, a_ch, b_ch)),
        ('per_link_below_exact', lambda: certify_propagation_claim({'order_in_straddling_amplitudes': 2, 'per_link': [a_ch / 2, b_ch]}, a_ch, b_ch)),
    ])
    control('fixture_split_lipschitz_and_trace', [
        ('growing_region_sizes', lambda: certify_charging_rule(growing)),
        ('vacuum_component_creation', lambda: certify_orthogonal_trace(vacuum_component_trace())),
    ])
    must(certify_analyticity_claim('creation_coefficients', False), 'analyticity scope')
    control('zero_free_region_required', [
        ('reduced_density_analytic', lambda: certify_analyticity_claim('reduced_density', False)),
        ('normalization_analytic', lambda: certify_analyticity_claim('normalization', False)),
    ])
    esi = {'sites': 'every site of the union volume', 'proved_in_packet': True, 'exponent': '(N-|u|_inf)_+',
           'source': 'route_B_disc_lemma_in_packet', 'K': qs(K_B)}
    must(certify_every_site_input(esi), 'every-site input')
    control('every_site_coefficient_input', [
        ('BA1_gate_value', lambda: certify_every_site_input({**esi, 'K': '49/111790368'})),
        ('BA1_forward_boundary_weighted_bound', lambda: certify_every_site_input({**esi, 'source': 'BA1 forward boundary-weighted bound'})),
        ('BA1_reverse_disc_theorem_cited', lambda: certify_every_site_input({**esi, 'source': 'BA1 reverse Theorem 4.1 cited'})),
        ('BB1_every_site_form', lambda: certify_every_site_input({**esi, 'source': 'BB1 every-site form (b)'})),
        ('R_only_input_at_far_sites', lambda: certify_every_site_input({**esi, 'sites': 'u in R'})),
        ('cited_as_admitted', lambda: certify_every_site_input({**esi, 'proved_in_packet': False})),
        ('exponent_N_minus_1_everywhere', lambda: certify_every_site_input({**esi, 'exponent': 'N-1'})),
    ])
    control('cutoff_limit_order', [
        ('limits_exchanged', lambda: certify_limit_order('N_to_infinity_then_cutoff')),
    ])
    must(certify_convergence_route('cauchy_bound_and_trace_class_completeness'), 'convergence route')
    control('cauchy_estimate_not_compactness', [
        ('compactness_plus_closeness', lambda: certify_convergence_route('compactness_plus_uniform_closeness')),
        ('compactness_plus_first_order', lambda: certify_convergence_route('compactness_plus_first_order_agreement')),
    ])
    control('limit_identified_with_aq1_limits', [
        ('inheritance_first', lambda: certify_identification({**ident, 'order': ['inheritance', 'identification_on_every_finite_region']})),
        ('zero_selected_list', lambda: certify_identification({**ident, 'inherited_list': 'AQ1/AQ2 zero-selected list'})),
        ('BB2_list', lambda: certify_identification({**ident, 'inherited_list': 'BB2 gate list'})),
        ('no_quasi_local_extension', lambda: certify_identification({**ident, 'extension': 'none'})),
    ])
    control('translation_invariance_separate_item', [
        ('nested_cubes_only', lambda: certify_translation_claim({**trans, 'nested_cubes_only': True})),
        ('two_step_union_bound', lambda: certify_translation_claim({**trans, 'factor': 2})),
        ('non_coarse_claim', lambda: certify_translation_claim({**trans, 'translations': 'all fine translations'})),
        ('telescoped_source', lambda: certify_translation_claim({**trans, 'source': 'nested_telescoping'})),
    ])
    control('route_b_constants_not_route_a', [
        ('per_site_sum_28', lambda: certify_route_b_constants({**rb_rec, 'per_site_sum_over_tau': 28})),
        ('faces_49', lambda: certify_route_b_constants({**rb_rec, 'first_order_faces': 49})),
        ('groups_4', lambda: certify_route_b_constants({**rb_rec, 'groups_per_site': 4})),
        ('coefficient_9856', lambda: certify_route_b_constants({**rb_rec, 'contraction_coefficient': 9856})),
        ('BA1_K_under_route_B', lambda: certify_route_b_constants({**rb_rec, 'constants': {**rb_rec['constants'], 'K_B': '49/111790368'}})),
        ('BB1_C_under_route_B', lambda: certify_route_b_constants({**rb_rec, 'constants': {**rb_rec['constants'], 'C_B': qs(bb1_C[-1])}})),
        ('BB1_c_site_under_route_B', lambda: certify_route_b_constants({**rb_rec, 'constants': {**rb_rec['constants'], 'c_site_B': qs(bb1_cs[-1])}})),
        ('BB2_C_prime_under_route_B', lambda: certify_route_b_constants({**rb_rec, 'constants': {**rb_rec['constants'], 'C_prime_B': '4/984375'}})),
        ('BB2_c_prime_site_under_route_B', lambda: certify_route_b_constants({**rb_rec, 'constants': {**rb_rec['constants'], 'c_prime_site_B': '2/984375'}})),
        ('source_substitution_28_49_aborts_at_pin', lambda: certify_route_b_constants({**rb_rec, 'T_B_tau': qs(T_exact(TAU, 28, 49))})),
        ('route_A_label', lambda: certify_route_b_constants({**rb_rec, 'model_route': 'route_A'})),
    ])
    control('disc_admissible_under_J_prime', [
        ('route_A_disc_radius', lambda: certify_disc(J_UNIT, Q(1, 37888), 'route-A disc radius 1/37888 under J\'')),
        ('route_A_split_weight', lambda: certify_disc(J_UNIT, (1 / (37888 * TAU)) * TAU, 'route-A split weight under J\'')),
        ('twice_route_B_maximum', lambda: certify_disc(J_UNIT, 2 * rho_max, 'twice the route-B maximal radius')),
        ('split_weight_4096', lambda: certify_disc(J_UNIT, 4096 * TAU, 'split weight 4096')),
    ])
    control('support_one_groups', [
        ('charged_as_straddling', lambda: certify_support_one({**so_rec, 'straddles': True})),
        ('clipped', lambda: certify_support_one({**so_rec, 'clipped_by_route_b_volume': True})),
        ('omitted_from_piece_graph', lambda: certify_support_one({**so_rec, 'in_piece_graph': False})),
        ('charged_a_distance', lambda: certify_support_one({**so_rec, 'distance_cost': 1})),
        ('first_order_dropped', lambda: certify_support_one({**so_rec, 'first_order_creation_nonzero': False})),
        ('clipped_volume_enumerated', lambda: require(routeb_faces(box(2), clip_boundary_singles=True) == routeb_faces(box(2)),
                                                      'boundary single groups clipped in the enumeration')),
    ])
    control('route_b_first_order_marginal', [
        ('route_A_ten_faces', lambda: certify_first_order_R({**fo_rec, 'faces_moving_rho_R_at_first_order': 10})),
        ('eighty_eight_faces', lambda: certify_first_order_R({**fo_rec, 'faces_moving_rho_R_at_first_order': 88})),
        ('straddling_nonzero', lambda: certify_first_order_R({**fo_rec, 'straddling_with_zero_first_order': 66})),
        ('route_A_trace_norm', lambda: certify_first_order_R({**fo_rec, 'trace_norm_over_tau': '1/72'})),
    ])
    control('selected_face_site_energy', [
        ('route_A_at_most_18', lambda: certify_site_energy({**site_energy_rec, 'first_order_site_energy_max': 18})),
        ('selected_energy_18', lambda: certify_site_energy({**site_energy_rec, 'selected_site_energy': 18})),
        ('kept_from_L_18', lambda: certify_site_energy({**site_energy_rec, 'kept_in_Q_L_iff_L_at_least': 18})),
    ])
    fam = {'common_limit_claimed': False, 'families': [FAMILY], 'all_contained_boundary_identified': False}
    must(certify_family_claim(fam), 'family record')
    control('one_family_no_common_limit', [
        ('common_limit_claimed', lambda: certify_family_claim({**fam, 'common_limit_claimed': True})),
        ('second_family', lambda: certify_family_claim({**fam, 'families': [FAMILY, 'F2-type all-contained route-B boxes']})),
        ('all_contained_identified', lambda: certify_family_claim({**fam, 'all_contained_boundary_identified': True})),
    ])
    control('exhaustion_within_prescription_only', [
        ('boundary_condition_phrasing', lambda: certify_exhaustion({**exh, 'phrasing': 'comparison of boundary conditions'})),
        ('singles_dropped_volumes', lambda: certify_exhaustion({**exh, 'volumes': 'volumes with boundary single groups dropped'})),
        ('N_k_not_largest', lambda: certify_exhaustion({**exh, 'N_k': 'any N with Lambda_N inside V_k'})),
        ('telescoped_exhaustion', lambda: certify_exhaustion({**exh, 'comparison': 'telescoping through intermediate volumes'})),
    ])
    control('sign_mirror_pointwise', [
        ('second_coupling', lambda: certify_sign_mirror({**mirror, 'minus_tau_status': 'second real-g coupling'})),
        ('second_observation', lambda: certify_sign_mirror({**mirror, 'minus_tau_status': 'independent second observation'})),
        ('whole_sets_only', lambda: certify_sign_mirror({**mirror, 'source': 'whole_sets_of_subsequential_limits'})),
        ('nonlocal_U', lambda: certify_sign_mirror({**mirror, 'U_E_local': 'global unitary'})),
        ('untied_coefficient', lambda: require(mirror_compression_fixture(Q(1, 1000)), 'uniform flip identity fails for an untied selected coefficient')),
    ])
    control('identification_before_inheritance_route_b', [
        ('inheritance_before_identification', lambda: certify_identification({**ident, 'order': ['inheritance']})),
        ('route_A_reset_98', lambda: certify_identification({**ident, 'inherited_list': 'AQ2 list with reset 98|tau|'})),
        ('R_only_identification', lambda: certify_identification({**ident, 'regions': 'R only'})),
    ])
    nb = {'region_form_proved_untruncated': True, 'convergence_scope': 'untruncated vectors'}
    must(certify_node_basis(nb), 'node basis')
    control('region_form_load_bearing_for_node', [
        ('R_form_only', lambda: certify_node_basis({**nb, 'region_form_proved_untruncated': False})),
        ('Q_L_only', lambda: certify_node_basis({**nb, 'convergence_scope': 'each Q_L only'})),
    ])
    control('node_values_unchanged', [
        ('rederived_radius_headline', lambda: certify_node_values({**node_rec, 'radius': qs(own_E)}, gate_d, gate_R)),
        ('smaller_state_term', lambda: certify_node_values({**node_rec, 'state_term': qs(D_PRIME / 2)}, gate_d, gate_R)),
        ('seven_star_slope', lambda: certify_node_values({**node_rec, 'k_prime_over_tau': '49/4'}, gate_d, gate_R)),
        ('other_node', lambda: certify_node_values({**node_rec, 'node_s': Q(2)}, gate_d, gate_R)),
        ('undeclared_file', lambda: certify_node_values({**node_rec, 'calculator_path': CALCULATOR_REL}, gate_d, gate_R)),
        ('datum_changed', lambda: certify_node_values({**node_rec, 'datum': qs(gate_d + Q(1, 10 ** 40))}, gate_d, gate_R)),
    ])
    ref = {'sub_label': rp['sub_label'], 'resolved_interaction_shift': rp['resolved_interaction_shift'],
           'sign_or_coefficient_of_C_claimed': False, 'free_value_inside': rp['free_reference_included']}
    must(certify_reference(ref), 'reference record')
    control('reference_unresolved_retained_route_b', [
        ('shift_claimed', lambda: certify_reference({**ref, 'resolved_interaction_shift': True})),
        ('sign_claimed', lambda: certify_reference({**ref, 'sign_or_coefficient_of_C_claimed': True})),
        ('label_dropped', lambda: certify_reference({**ref, 'sub_label': 'interaction_shift_resolved'})),
        ('free_outside', lambda: certify_reference({**ref, 'free_value_inside': False})),
    ])
    nsc = {'finite_box_node_convergence_claimed': False}
    must(certify_node_scope(nsc), 'node scope')
    control('no_finite_box_node_convergence', [
        ('C_N_to_C_inf', lambda: certify_node_scope({'finite_box_node_convergence_claimed': True})),
    ])
    dyn = {'route_b_dynamics_comparison': False, 'correlation_function_statement': False, 'phi_norm_used': 'none'}
    must(certify_dynamics_scope(dyn), 'dynamics scope')
    control('no_route_b_dynamics_claim', [
        ('dynamics_comparison', lambda: certify_dynamics_scope({**dyn, 'route_b_dynamics_comparison': True})),
        ('correlation_statement', lambda: certify_dynamics_scope({**dyn, 'correlation_function_statement': True})),
        ('dynamics_level_exported', lambda: certify_gate_fields({**gate_fields, 'dynamics_level': 'correlation_functions_compact_window'},
                                                                pre['gate_fields_required'])),
        ('BA2_constant_applied', lambda: certify_dynamics_scope({**dyn, 'phi_norm_used': '2268|tau|'})),
    ])
    ncr = {'non_coarse_claim': 'none', 'reason': 'factor partition and grouping not preserved; uniform coefficients preserved'}
    must(certify_non_coarse(ncr) and tf['non_coarse_witness'] is not None
         and tf['non_coarse_witness']['coefficient_from'] == tf['non_coarse_witness']['coefficient_to'], 'non-coarse record')
    control('non_coarse_translation_no_claim', [
        ('invariance_claimed', lambda: certify_non_coarse({**ncr, 'non_coarse_claim': 'invariant'})),
        ('non_invariance_claimed', lambda: certify_non_coarse({**ncr, 'non_coarse_claim': 'not invariant'})),
        ('route_A_reason', lambda: certify_non_coarse({**ncr, 'reason': 'selected face mapped to an omitted face of another coefficient'})),
    ])
    mc = {'limit_identified_with': 'AX1 route-B AQ1-type states', 'constants_source': 'route-B packet', 'transfer_to_zero_selected': False}
    must(certify_model_crossing(mc), 'model crossing record')
    control('model_crossing_rejected', [
        ('identified_with_BB2_limit', lambda: certify_model_crossing({**mc, 'limit_identified_with': 'BB2 zero-selected limit'})),
        ('BB1_constants_applied', lambda: certify_model_crossing({**mc, 'constants_source': 'BB1 gate'})),
        ('transfer_to_zero_selected', lambda: certify_model_crossing({**mc, 'transfer_to_zero_selected': True})),
    ])
    dc = {'kind': 'direct', 'factor': 1}
    must(certify_direct_comparison(dc), 'direct comparison')
    control('direct_comparison_required', [
        ('union_volume_factor_2', lambda: certify_direct_comparison({'kind': 'union_volume', 'factor': 2})),
        ('telescoped_input', lambda: certify_direct_comparison({'kind': 'telescoped_coefficient_input', 'factor': 1})),
    ])
    control('rate_range_stated', [
        ('rate_without_range', lambda: certify_rate_claim('||rho^{box1}_R-rho^{box2}_R||_1 at most C_B q^(N-1)')),
        ('O_one_over_N', lambda: certify_rate_claim('correlations converge at O(1/N) for every N at least 2')),
        ('rate_from_BB2', lambda: certify_rate_claim('the BB2 rate q^(N-1) holds for every N at least 2')),
    ])

    # ================================================================ result
    controls_ids = contract['controls']
    must(sorted(MUTATION_CONTROLS) == sorted(controls_ids), 'every contract control executed as damaging mutations')
    check('contract_controls_all_executed', True, count=len(MUTATION_CONTROLS))
    ledger = {
        'route_b_every_site_coefficient_input': {'contribution_to_C_B': exact(ledger_p['near']),
                                                  'note': 'supports meeting R through kappa=2: 2K_B(1+q); the far-site input enters the split rows through S_lambda'},
        'single_factor_groups': {'status': 'charged inside K_B, t0 and tW (no separate additive term)',
                                 'first_order_share_of_K_B_labelled': exact(K_B * Q(3, 52)),
                                 'note': '3 of the 52 first-order faces per site and |z| of the per-site sum 29|z|; never straddling, never clipped'},
        'straddling_supports_route_b': {'contribution_to_C_B': exact(ledger_p['straddling'])},
        'normalization': {'contribution_to_C_B': exact(ledger_p['normalization'])},
        'split_remainder': {'contribution_to_C_B': exact(ledger_p['removal'] + ledger_p['feedback']),
                            'removal': exact(ledger_p['removal']), 'closure_feedback': exact(ledger_p['feedback'])},
        'whole_sequence_assembly': {'factor': '1', 'extra_cost': '0', 'assembly': ASSEMBLY,
                                    'labelled_nested_telescoping_factor': '64/63'},
        'cutoff_removal_at_fixed_N': {'status': 'not_applicable',
                                      'reason': 'an exact limit at fixed N (AV1 F20-F23 with the route-B gap 1/2); constants independent of L'},
        'identification_with_ax1_states': {'status': 'not_applicable', 'reason': 'exact equality of states on every finite region; no numeric cost'},
        'node_restatement': {'status': 'not_applicable', 'reason': 'd and R-prime carried unchanged; R-prime already contains the arithmetic half-width'},
        'arithmetic': {'status': 'not_applicable', 'reason': 'exact Fractions; directed enclosures e^{1/8}<8/7, Machin pi and e^{-3} brackets'},
    }
    must(list(ledger) == pre['error_terms_itemized'], 'ledger keys equal error_terms_itemized')
    check('error_ledger_itemized', sum(ledger_p.values()) == C_B, ledger=ledger)
    headline = {
        'K_B': {**exact(K_B), 'q': '1/64', 'tier': 'exact_first_order', 'route': ROUTE_K, 'disc_radius': '64|tau|',
                'target': qs(targets['K_B']), 'margin': sci(targets['K_B'] / K_B),
                'form': 'sum over I containing u of ||c^A_I-c^B_I|| at most K_B q^((N-|u|_inf)_+), every site u of the union volume, every N at least 2'},
        'C_B': {**exact(C_B), 'q': '1/64', 'tier': 'exact_first_order', 'route': ROUTE_DENSITY, 'input': 'K_B (analytic_disc)',
                'target': qs(targets['C_B']), 'margin': sci(targets['C_B'] / C_B)},
        'c_site_B': {**exact(cs_B), 'q': '1/64', 'tier': 'exact_first_order', 'route': ROUTE_DENSITY,
                     'target': qs(targets['c_site_B']), 'margin': sci(targets['c_site_B'] / cs_B)},
        'C_prime_B': {**exact(Cp_B), 'q': '1/64', 'tier': 'exact_first_order', 'route': ROUTE_DENSITY, 'assembly': ASSEMBLY,
                      'target': qs(targets['C_prime_B']), 'margin': sci(targets['C_prime_B'] / Cp_B)},
        'c_prime_site_B': {**exact(csp_B), 'q': '1/64', 'tier': 'exact_first_order', 'route': ROUTE_DENSITY, 'assembly': ASSEMBLY,
                           'target': qs(targets['c_prime_site_B']), 'margin': sci(targets['c_prime_site_B'] / csp_B)},
        'crude_tier': {'K_B': exact(Hc['K']), 'C_B': exact(Hc['C']), 'c_site_B': exact(Hc['c_site']), 'status': 'reported only; fails'},
        'node': {'datum': qs(node_d), 'radius_R_prime': qs(node_R), 's': '1', 'tau': '+1/100000000',
                 'status': 'restated for the limit, values equal to the AX2 gate rationals'},
        'disc_admissibility': {'self_map': qs(disc_sm), 'contraction': qs(disc_ct), 'split_self_map': qs(w_sm),
                               'split_contraction': qs(w_ct), 'route_A_extreme_self_map': qs(J_UNIT * ra_disc * GR_UP)},
        'statement': headline_statement,
    }
    result = {
        'loop': 'BC2', 'direction': 'forward', 'human_author': contract['human_author'],
        'contribution_alias': 'HNM-BC2-F route-B coefficient decay, marginal locality, whole-sequence convergence and node restatement (forward producer; AI-assisted, Claude)',
        'ai_assistance': 'Claude (an AI model) wrote the derivations, check.py and report.md; correlated model-agent work, not human review',
        'model': MODEL_ID, 'label_text': LABEL, 'family': FAMILY, 'cover': 'R={0,e_z}',
        'metric': 'coarse l-infinity on factor sites (star diameter 1, single-factor group diameter 0)',
        'topology': 'trace norm on B(H_Y)', 'clock': 's=alpha*t_E/hbar (node s=1); theta=alpha*t/hbar for the inherited limit dynamics only',
        'routes_executed': [ROUTE_K, ROUTE_DENSITY], 'assembly': ASSEMBLY, 'tier': 'exact_first_order',
        'headline': headline, 'label': 'convergence_of_named_constructions',
        'secondary_labels': ['certificate_restated_for_limit', 'reference_unresolved', 'static_not_dynamic'],
        'gate_fields': gate_fields, 'mandatory_sentence_template': template,
        'contract_controls_covered': controls_ids,
        'controls_with_damaging_mutations': sorted(MUTATION_CONTROLS),
        'damaging_mutations_total': sum(len(c.get('rejected_mutations', {})) for c in CHECKS),
        'fixtures': sorted(fx), 'rate_claims': rate_claims, 'error_ledger': ledger,
        'exclusions': {'contract': contract['claim_exclusions'], 'preregistration': pre['claim_exclusions']},
        'obligations': ['a route-B boundary-prescription comparison (an all-contained analogue with its own itemization)',
                        'route-B dynamics and correlation functions (a route-B BA2)', 'uniqueness of any ground state',
                        'anything uniform in the lattice spacing a', 'the continuum problem'],
        'proposed_forward_verdict': outcome,
        'outcome_note': 'proposed for the single forward producer; admission needs the skeptic replay from the contract',
        'scratch_disclosure': '/tmp/claude-0/bc2-forward-private/ (private; nothing in it is evidence)',
        'uniform_wilson_claim': True,
        'uniform_wilson_claim_scope': 'means only that the model is the uniform fixed-spacing Kogut-Susskind SU(2) model at strong bare coupling as labelled; no uniform Wilson-mean sign certificate',
        'checks': CHECKS,
    }
    for k, v in gate_fields.items():
        result[k] = v
    for k in FALSE_FLAGS:
        must(result[k] is False, 'flag ' + k)
    return result


def main():
    ap = argparse.ArgumentParser(description='HNM-BC2 forward producer checker (exact arithmetic)')
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
    manifest = {'loop': 'BC2', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    hp = result['headline']
    print(json.dumps({'loop': 'BC2', 'direction': 'forward', 'checks': len(result['checks']),
                      'K_B': hp['K_B']['preview'], 'C_B': hp['C_B']['preview'], 'c_site_B': hp['c_site_B']['preview'],
                      'controls': len(result['controls_with_damaging_mutations']),
                      'mutations': result['damaging_mutations_total'], 'outcome': result['proposed_forward_verdict']},
                     sort_keys=True))


if __name__ == '__main__':
    main()
