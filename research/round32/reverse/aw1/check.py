#!/usr/bin/env python3
"""HNM-AW1 reverse producer: parity theorem, link-flip antisymmetry, the exact
first-order Wilson mean and an itemized second-order remainder K_2 for the
zero-selected AQ subfamily (reverse reconstruction route).

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production under
premise isolation; HNM labels are project aliases. Peter-Weyl/Clebsch-Gordan
selection rules, center-flip (Z_2 grading) arguments, Rayleigh-Schroedinger and
commuting-creation expansions are established mathematics; scientific priority is
unverified.

Standard library only. Exact Fraction arithmetic (and exact quadratic-field
arithmetic for the one-plaquette fixtures) decides every Boolean; decimal strings
are truncated previews. Every control is a damaging mutation whose rejection is
required; rejections and failures are explicit exceptions (never assert), so the
run and its output bytes are identical under python -O.

Usage: python3 -B research/round32/reverse/aw1/check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from itertools import combinations_with_replacement
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUTS = HERE / 'inputs'
CONTRACT_REL = 'research/round32/contracts/aw1.json'
AV1_GATE_REL = 'research/round32/advisor/av1-gate.json'
AM2_GATE_REL = 'research/round29/advisor/am2-gate.json'
I1_REL = 'research/round21/forward/i1/report.md'
CONTRACT_SHA256 = 'c24bf7eb6a1c24034427c810a9c26c4c86d1f9c1d31b0fe36ea4cf2a796814ef'
DEN = 10 ** 40
FORBIDDEN_EXACT = (
    'research/round32/skeptic/triage.md',
    'research/round32/skeptic/loop2-response.md',
)
FORBIDDEN_PREFIXES = (
    'research/round32/advisor/deliberation-',
    'research/round32/forward/aw1/',
    'research/round32/reverse/aw1/',
    'research/round32/skeptic/aw1',
)
FORBIDDEN_PATTERN = re.compile(r'^research/round32/experts/[^/]+/loop2-response\.md$')
FIXED_FALSE_FLAGS = ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift',
                     'scientific_priority_verified', 'third_order_remainder_claim')


# ----------------------------------------------------------------- exceptions
class Rejected(Exception):
    """A validator refused its input: the required fate of a damaging mutation."""


class ProducerError(Exception):
    """An identity required by the proof failed; the run aborts without output."""


def require(condition, reason):
    if condition is not True:
        raise Rejected(reason)


def must(condition, reason):
    if condition is not True:
        raise ProducerError(reason)


CHECKS = []


def record(check_id, condition, **details):
    must(condition, 'check failed: ' + check_id)
    must(all(c['id'] != check_id for c in CHECKS), 'duplicate check id: ' + check_id)
    entry = {'id': check_id, 'passed': True}
    entry.update(details)
    CHECKS.append(entry)


def rejection(function, *args):
    try:
        function(*args)
    except Rejected as exc:
        return str(exc)
    raise ProducerError('damaging mutation accepted by ' + function.__name__)


def control(check_id, mutations, **details):
    """A contract control passes only if every listed damaging mutation is rejected."""
    rejected = {}
    for label, function, args in mutations:
        must(label not in rejected, 'duplicate mutation label ' + label)
        rejected[label] = rejection(function, *args)
    record(check_id, len(rejected) == len(mutations) and len(mutations) > 0,
           kind='damaging_mutation_control', rejected_mutations=rejected, **details)


# ----------------------------------------------------------- exact arithmetic
def parse_q(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise Rejected('non-exact numeric input rejected: ' + repr(value))
    if isinstance(value, Q):
        return value
    if isinstance(value, int):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'[+-]?[0-9]+(/[1-9][0-9]*)?', value):
        return Q(value)
    raise Rejected('malformed rational input rejected: ' + repr(value))


def qs(x):
    return str(Q(x))


def ceil_to(x, den=DEN):
    x = Q(x)
    return Q(-((-x.numerator * den) // x.denominator), den)


def floor_to(x, den=DEN):
    x = Q(x)
    return Q((x.numerator * den) // x.denominator, den)


def sqrt_bounds(y):
    y = Q(y)
    must(y >= 0, 'negative square-root argument')
    scaled = y.numerator * DEN * DEN
    s = isqrt(scaled // y.denominator)
    lo = Q(s, DEN)
    hi = lo if s * s * y.denominator == scaled else Q(s + 1, DEN)
    must(lo * lo <= y and y <= hi * hi, 'square-root enclosure failed')
    return lo, hi


def rational_sqrt(y):
    """Exact square root of a rational square, else None."""
    y = Q(y)
    if y < 0:
        return None
    a, b = isqrt(y.numerator), isqrt(y.denominator)
    return Q(a, b) if a * a == y.numerator and b * b == y.denominator else None


def factorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


def exp_bounds(x, terms=18):
    x = Q(x)
    must(Q(0) <= x and x <= Q(1, 2), 'exponential argument outside [0,1/2]')
    partial, power = Q(0), Q(1)
    for k in range(terms + 1):
        partial += power / factorial(k)
        power *= x
    tail = power / factorial(terms + 1) / (1 - x / (terms + 2))
    return floor_to(partial), ceil_to(partial + tail)


def sci(x, digits=10):
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


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sgn(x):
    return (x > 0) - (x < 0)


class QF:
    """Exact element a + b*sqrt(D) of the real quadratic field Q(sqrt(D))."""
    __slots__ = ('a', 'b', 'D')

    def __init__(self, a, b, D):
        self.a, self.b, self.D = Q(a), Q(b), Q(D)
        must(self.D > 0 and rational_sqrt(self.D) is None, 'quadratic field needs a positive non-square D')

    def _same(self, o):
        if not isinstance(o, QF):
            o = QF(o, 0, self.D)
        must(o.D == self.D, 'quadratic-field elements from different fields')
        return o

    def __add__(self, o):
        o = self._same(o)
        return QF(self.a + o.a, self.b + o.b, self.D)

    __radd__ = __add__

    def __neg__(self):
        return QF(-self.a, -self.b, self.D)

    def __sub__(self, o):
        return self + (-self._same(o))

    def __mul__(self, o):
        o = self._same(o)
        return QF(self.a * o.a + self.b * o.b * self.D, self.a * o.b + self.b * o.a, self.D)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = self._same(o)
        n = o.a * o.a - o.b * o.b * self.D
        must(n != 0, 'division by zero in quadratic field')
        return self * QF(o.a / n, -o.b / n, self.D)

    def key(self):
        return (self.a, self.b, self.D)

    def sign(self):
        a, b = sgn(self.a), sgn(self.b)
        if b == 0 or a == b:
            return a if a != 0 else b
        if a == 0:
            return b
        big = sgn(self.a * self.a - self.b * self.b * self.D)
        return a * big

    def bounds(self):
        lo, hi = sqrt_bounds(self.D)
        v1, v2 = self.a + self.b * lo, self.a + self.b * hi
        return min(v1, v2), max(v1, v2)

    def text(self):
        return '%s + (%s)*sqrt(%s)' % (qs(self.a), qs(self.b), qs(self.D))


# ------------------------------------------------ SU(2) character algebra
HALF = Q(1, 2)


def chi_half_times(cls):
    """Multiply a class function {2j: multiplicity} by chi_{1/2} (Clebsch-Gordan)."""
    out = {}
    for tj, m in cls.items():
        for nt in (tj - 1, tj + 1):
            if nt >= 0:
                out[nt] = out.get(nt, 0) + m
    return out


def trivial_multiplicity_chi_half_power(n):
    cls = {0: 1}
    for _ in range(n):
        cls = chi_half_times(cls)
    return cls.get(0, 0)


def haar_W_moment_cg(n):
    """E_Haar[W^n], W=chi_{1/2}/2: trivial multiplicity in (1/2)^{(x)n} over 2^n."""
    return Q(trivial_multiplicity_chi_half_power(n), 2 ** n)


def haar_W_moment_weyl(n):
    """Weyl integration: E[cos^n] = (2/pi) int_0^pi cos^n sin^2, by Wallis ratios."""
    def wallis_over_pi(m):
        if m % 2:
            return Q(0)
        r = Q(1)
        for k in range(1, m, 2):
            r *= Q(k, k + 1)
        return r
    return 2 * (wallis_over_pi(n) - wallis_over_pi(n + 2))


def haar_W_moment_sphere(n):
    """Free-link route: the plaquette holonomy is Haar = uniform on S^3; W = q_0."""
    if n % 2:
        return Q(0)
    r = Q(1)
    for i in range(n // 2):
        r *= Q(2 * i + 1, 4 + 2 * i)
    return r


def casimir(two_j):
    j = Q(two_j, 2)
    return j * (j + 1)


def center_parity(two_j):
    return 1 if two_j % 2 == 0 else -1


CASIMIR_HALF = casimir(1)
HAAR_W = haar_W_moment_cg(1)
HAAR_W2 = haar_W_moment_cg(2)
HAAR_W4 = haar_W_moment_cg(4)
ALPHA_OVER_DELTA = Q(8)
FACE_ENERGY_ALPHA = 4 * CASIMIR_HALF              # 3 (alpha units)
FACE_ENERGY = ALPHA_OVER_DELTA * FACE_ENERGY_ALPHA  # 24 (normalized, delta=alpha/8)
W_OMEGA_NORM = HALF                               # ||W Omega_R|| = sqrt(E[W^2]) = 1/2
# I1.5: each omitted face enters H with -(alpha tau/24) W_f; normalized phi_b=-(tau/3) sum W_f
FACE_COUPLING_PER_TAU = {'delta': -Q(1, 3), 'alpha': -Q(1, 24)}
FACE_ENERGY_BY_UNITS = {'delta': FACE_ENERGY, 'alpha': FACE_ENERGY_ALPHA}


def first_order_amplitude(coupling_units, energy_units):
    """psi^(1) = -H_0^{-1} V Omega_0 = amp * tau * sum_f W_f Omega_0 (per unit tau)."""
    require(coupling_units in FACE_COUPLING_PER_TAU and energy_units in FACE_ENERGY_BY_UNITS, 'unknown units')
    require(coupling_units == energy_units,
            'mixed normalization: coupling in %s units over an energy in %s units' % (coupling_units, energy_units))
    return -FACE_COUPLING_PER_TAU[coupling_units] / FACE_ENERGY_BY_UNITS[energy_units]


def am2_creation_coefficient(units='delta'):
    """AM2/AV1 c^(1)=L_0=H^{-1}PV Omega_0 per unit tau per face: the negative of psi^(1)."""
    return -first_order_amplitude(units, units)


# --------------------------------------------------------------- geometry
DIRS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
AXIS = {'x': 0, 'y': 1, 'z': 2}
ORIENTATIONS = (('xy', 0, 1), ('xz', 0, 2), ('yz', 1, 2))
STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
COVER = (ORIGIN, EZ)
OFFSET_TOKENS = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}


def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def coarse(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    return frozenset({(p, a), (vadd(p, DIRS[a]), c), (vadd(p, DIRS[c]), a), (p, c)})


def orientation_axes(name):
    return {n: (a, c) for n, a, c in ORIENTATIONS}[name]


# The original xz Wilson loop (AQ2 section 4, AT4 F04): (1/2)Tr U_(0,x)U_(e_x,z)U_(e_z,x)^-1 U_(0,z)^-1
W_DISPLAYED = frozenset({((0, 0, 0), 0), ((1, 0, 0), 2), ((0, 0, 1), 0), ((0, 0, 0), 2)})
W_FACE = face_links(ORIGIN, 0, 2)


def parse_i1_table(text):
    rows = []
    pat = re.compile(r'^\| (xy|xz|yz): r=([0-9,]+); s=([0-9,]+) \| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|\s*$')
    for line in text.splitlines():
        m = pat.match(line)
        if not m:
            continue
        rs = [int(v) for v in m.group(2).split(',')]
        ss = [int(v) for v in m.group(3).split(',')]
        require(int(m.group(4)) == len(rs) * len(ss), 'I1 table row count mismatch')
        support = tuple(sorted(OFFSET_TOKENS[tok.strip()] for tok in m.group(5).split(',')))
        for r in rs:
            for s in ss:
                rows.append((m.group(1), r, s, support, m.group(6)))
    return sorted(rows)


def derive_i1_table():
    """Re-derive the anchored classes from pi and the link tails (I1.4) and the selection rule."""
    rows = []
    for r in range(4):
        for s in range(2):
            p = (r, s, 0)
            for name, a, c in ORIENTATIONS:
                owners = tuple(sorted({coarse(t) for t, _ in face_links(p, a, c)}))
                selected = name == 'xy' and s == 0 and r in (0, 1, 2)
                rows.append((name, r, s, owners, 'selected' if selected else 'omitted'))
    return sorted(rows)


class DerivedCount:
    __slots__ = ('value', 'provenance')

    def __init__(self, value, provenance):
        self.value = value
        self.provenance = provenance


PROVENANCE = 'I1_snapshot_table_translation_covariance_all_sites'


def certified_count(obj, what):
    require(isinstance(obj, DerivedCount) and obj.provenance == PROVENANCE,
            what + ': count is hard-coded, copied, outgoing-only or not derived from the I1 table at every site')
    return obj.value


def class_face(anchor, cls):
    name, r, s, support, _ = cls
    a, c = orientation_axes(name)
    p = (4 * anchor[0] + r, 2 * anchor[1] + s, anchor[2])
    return face_links(p, a, c), tuple(sorted(vadd(anchor, v) for v in support))


def faces_of_factor(u, classes):
    """Every omitted face (anchor, class index) owning a link of factor u, with links and owner set."""
    out = {}
    for k, cls in enumerate(classes):
        for d in cls[3]:
            b = vsub(u, d)
            links, owners = class_face(b, cls)
            must(tuple(sorted({coarse(t) for t, _ in links})) == owners, 'owner set differs from link tails')
            out[(b, k)] = (links, owners)
    return out


def box_sites(N):
    rng = range(-N, N + 1)
    return [(x, y, z) for x in rng for y in rng for z in rng]


def box_faces(N, classes, selected_classes):
    sites = box_sites(N)
    siteset = set(sites)
    stars = [b for b in sites if all(vadd(b, v) in siteset for v in STAR)]
    omitted = []
    for b in stars:
        for k, cls in enumerate(classes):
            omitted.append(((b, k),) + class_face(b, cls))
    selected = []
    for b in sites:
        for cls in selected_classes:
            selected.append(class_face(b, cls)[0])
    return sites, stars, omitted, selected


# --------------------------------------------------------------- flip set
def parse_flip_set(text):
    parts = re.findall(r'\{\(p,([xyz])\): p_([xyz]) even\}', text)
    require(len(parts) == 3 and sorted(d for d, _ in parts) == ['x', 'y', 'z'], 'flip set text malformed')
    return {AXIS[d]: AXIS[c] for d, c in parts}


def in_flip(rule, link):
    p, d = link
    if d not in rule:
        return False
    return p[rule[d]] % 2 == 0


def flip_count(rule, links):
    return sum(1 for l in links if in_flip(rule, l))


def plaquettes_in_box(lo, hi):
    out = []
    for x in range(lo[0], hi[0] + 1):
        for y in range(lo[1], hi[1] + 1):
            for z in range(lo[2], hi[2] + 1):
                for name, a, c in ORIENTATIONS:
                    out.append(face_links((x, y, z), a, c))
    return out


def certify_flip_set(membership, plaquettes, label):
    """A flip set is admissible only if it meets every plaquette in an odd number of links."""
    even = [f for f in plaquettes if sum(1 for l in f if membership(l)) % 2 == 0]
    require(even == [], '%s meets %d plaquettes evenly: U_E would not flip every W_f' % (label, len(even)))
    return True


def certify_flip_sign(link_multiset, rule, claimed_sign):
    """U_E multiplies a product of j=1/2 link factors by (-1)^(number of factors on E-links)."""
    actual = (-1) ** sum(1 for l in link_multiset if in_flip(rule, l))
    require(claimed_sign == actual, 'claimed U_E sign %d but the term carries an even number of E-link factors' % claimed_sign)
    return True


def periodic_plaquettes(sides):
    """Plaquettes of a periodic fine box (coordinates reduced modulo the sides)."""
    out = []
    for x in range(sides[0]):
        for y in range(sides[1]):
            for z in range(sides[2]):
                for _, a, c in ORIENTATIONS:
                    wrapped = frozenset((tuple(q % n for q, n in zip(t, sides)), d) for t, d in face_links((x, y, z), a, c))
                    out.append(wrapped)
    return out


def residue_solutions():
    """Reverse reconstruction: all rules 'link (p,d) in E iff p_sigma(d) even' meeting every plaquette oddly."""
    cube = [(x, y, z) for x in range(2) for y in range(2) for z in range(2)]
    sols = []
    for s0 in range(3):
        for s1 in range(3):
            for s2 in range(3):
                rule = {0: s0, 1: s1, 2: s2}
                if all(flip_count(rule, face_links(p, a, c)) % 2 == 1 for p in cube for _, a, c in ORIENTATIONS):
                    sols.append(rule)
    return sols


# --------------------------------------------------------- finite matrices
def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def diag(vals):
    return [[Q(vals[i]) if i == j else Q(0) for j in range(len(vals))] for i in range(len(vals))]


def kron(a, b):
    return [[a[i // len(b)][j // len(b)] * b[i % len(b)][j % len(b)] for j in range(len(a) * len(b))]
            for i in range(len(a) * len(b))]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a))] for i in range(len(a))]


def mscale(s, a):
    return [[Q(s) * v for v in row] for row in a]


def eye(n):
    return diag([1] * n)


def one_plaquette(jmax2):
    """Gauge-invariant one-plaquette space, characters chi_j(U_f), j<=jmax: G_0 and W (alpha units)."""
    n = jmax2 + 1
    g0 = diag([4 * casimir(t) for t in range(n)])
    w = [[Q(0)] * n for _ in range(n)]
    for i in range(n - 1):
        w[i][i + 1] = w[i + 1][i] = HALF
    flip = diag([center_parity(t) for t in range(n)])
    return g0, w, flip


def rs_series(h0diag, v, observable, order):
    """Exact Rayleigh-Schroedinger expansion of the ground expectation of `observable`."""
    n = len(h0diag)
    must(all(h0diag[i] > h0diag[0] for i in range(1, n)), 'simple unperturbed ground required')
    psis = [[Q(1)] + [Q(0)] * (n - 1)]
    energies = [Q(h0diag[0])]
    for k in range(1, order + 1):
        vp = [sum(v[i][j] * psis[k - 1][j] for j in range(n)) for i in range(n)]
        energies.append(vp[0])
        new = [Q(0)] * n
        for i in range(1, n):
            s = -vp[i] + sum(energies[m] * psis[k - m][i] for m in range(1, k))
            new[i] = s / (h0diag[i] - h0diag[0])
        psis.append(new)

    def ip(u, m, w):
        return sum(u[i] * sum(m[i][j] * w[j] for j in range(n)) for i in range(n))

    ident = eye(n)
    num = [sum(ip(psis[a], observable, psis[k - a]) for a in range(k + 1)) for k in range(order + 1)]
    den = [sum(ip(psis[a], ident, psis[k - a]) for a in range(k + 1)) for k in range(order + 1)]
    out = []
    for k in range(order + 1):
        out.append((num[k] - sum(den[m] * out[k - m] for m in range(1, k + 1))) / den[0])
    return out, energies, psis


def two_level_ground_mean(b, gap=Q(3)):
    """Exact ground of [[0,b],[b,gap]]: v=(gap-sqrt(D))/(2b), <W>=v/(1+v^2) with W=[[0,1/2],[1/2,0]]."""
    b = Q(b)
    must(b != 0, 'two-level fixture needs b != 0')
    D = gap * gap + 4 * b * b
    v = QF(gap / (2 * b), -1 / (2 * b), D)
    mean = v / (QF(1, 0, D) + v * v)
    # verify the eigen-equation b v^2 - gap v - b = 0 exactly
    res = v * v * b - v * gap - QF(b, 0, D)
    must(res.a == 0 and res.b == 0, 'two-level eigen-equation fails')
    return v, mean


# ----------------------------------------------------- creation-algebra fixture
FIX_DIMS = (3, 3, 2, 2)          # sites 0, e_z (the cover R) and two outside sites o1, o2
FIX_R = (0, 1)


def fx_apply(support, amps, vec):
    out = {}
    for st, cf in vec.items():
        if all(st[s] == 0 for s in support):
            for exc, a in amps.items():
                n = list(st)
                for s, e in zip(support, exc):
                    n[s] = e
                n = tuple(n)
                out[n] = out.get(n, 0) + a * cf
    return {k: v for k, v in out.items() if v != 0}


def fx_sub(u, v):
    out = dict(u)
    for k, x in v.items():
        out[k] = out.get(k, 0) - x
    return {k: x for k, x in out.items() if x != 0}


def fx_ip(u, v):
    return sum(x * v.get(k, 0) for k, x in u.items())


def fx_product(creators, keys, vec):
    for key in keys:
        vec = fx_sub(vec, fx_apply(key, creators[key], vec))
    return vec


def fx_act_R(matrix, vec):
    out = {}
    for st, cf in vec.items():
        for (l, m), a in matrix.items():
            if (st[0], st[1]) == m:
                n = (l[0], l[1]) + st[2:]
                out[n] = out.get(n, 0) + a * cf
    return {k: v for k, v in out.items() if v != 0}


def fx_norm_bounds(amps):
    return sqrt_bounds(sum(a * a for a in amps.values()))


# ------------------------------------------------------------- K_2 ledger
LEDGER_TERMS = ('am2_remainder', 'straddling', 'two_creation', 'density', 'normalization')
TAU_CAP = None
G_R_UP = Q(148, 7)
GP_R_UP = Q(352)
R_RADIUS = Q(1, 64)
J_PER_TAU = Q(28)
COUNTS = {}


class Term:
    __slots__ = ('name', 'value', 'tier', 'provenance')

    def __init__(self, name, value, tier, provenance):
        self.name, self.value, self.tier, self.provenance = name, Q(value), tier, provenance


def certify_model(tau, selected=('0', '0', '0')):
    t = parse_q(tau)
    sel = tuple(parse_q(x) for x in selected)
    require(len(sel) == 3, 'selected triple must have three entries')
    require(all(x == 0 for x in sel),
            'nonzero selected triple: Haar is not the onsite ground and U_E maps kappa to -kappa (a changed model)')
    require(abs(t) <= TAU_CAP, 'coupling outside the AM2/AQ cap: not certified here (not a failure)')
    return t


def certify_overlap_multiplier(mult, label):
    mult = Q(mult)
    exact = 2 * W_OMEGA_NORM
    if label == 'exact_single_component':
        require(mult == exact, 'exact overlap multiplier is 2||W Omega_R||=1, got %s' % qs(mult))
    elif label == 'conservative_labelled':
        require(mult >= exact and mult == 4, 'conservative multiplier must be the labelled factor 4')
    else:
        require(False, 'overlap multiplier %s without a tier label (a factor 4 is accepted only if labelled conservative)' % qs(mult))
    return mult


def assemble_remainder(tier, terms):
    require(tier in ('exact', 'crude'), 'unknown tier')
    require(sorted(terms) == sorted(LEDGER_TERMS),
            'itemized ledger incomplete or padded: %s' % ','.join(sorted(terms)))
    for name, term in sorted(terms.items()):
        require(term.tier == tier, 'tier mixing: %s is %s-tier inside the %s tier' % (name, term.tier, tier))
    require(terms['am2_remainder'].value > 0, 'the AM2 remainder is never zero at nonzero coupling')
    for name in ('straddling', 'two_creation', 'density', 'normalization'):
        require(terms[name].value >= 0, 'negative ledger entry ' + name)
    if tier == 'exact':
        require(terms['am2_remainder'].provenance in ('self_consistent_352JT', 'self_consistent_directed_G'),
                'exact-tier remainder must use t<=t1/(1-352J)')
        require(terms['straddling'].provenance == 'enumeration_6_faces_containing_R',
                'exact-tier straddling must be pinned to the 6 faces strictly containing R')
        require(terms['two_creation'].provenance == 'enumeration_33x33_single_site',
                'exact-tier two-creation term must be pinned to 33 single-site faces per site of R')
        require(terms['density'].provenance == 'enumeration_82_faces_meeting_R',
                'exact-tier density must be pinned to the 82 faces meeting R')
    else:
        for name, term in terms.items():
            require(term.provenance.startswith('crude_'), 'crude tier term %s is not crude' % name)
    return sum((terms[n].value for n in LEDGER_TERMS), Q(0))


def remainder_ledger(tau, tier='exact', multiplier=None, remainder_form='contract_352'):
    t_signed = certify_model(tau)
    a = abs(t_signed)
    must(a > 0, 'the ledger is evaluated at nonzero coupling')
    J = J_PER_TAU * a
    face = a * W_OMEGA_NORM * abs(am2_creation_coefficient('delta'))   # |tau|/144 per face vector
    if multiplier is None:
        multiplier = (Q(1), 'exact_single_component')
    mult = certify_overlap_multiplier(*multiplier)
    if tier == 'exact':
        K = GP_R_UP * J
        require(K < 1, 'self-consistent factor 352J must be below one')
        t1 = face * certified_count(COUNTS['faces_per_factor'], 'faces per factor')
        T = t1 / (1 - K)
        must(T <= R_RADIUS, 'self-consistent t inside the AM2 ball')
        if remainder_form == 'contract_352':
            rho, rprov = K * T, 'self_consistent_352JT'
        elif remainder_form == 'directed_G':
            e_lo, e_hi = exp_bounds(ceil_to(8 * T))
            rho, rprov = ceil_to(J * (16 * e_hi * (1 + 10 * T) - 16)), 'self_consistent_directed_G'
        else:
            raise Rejected('unknown remainder form')
        s_strad = face * certified_count(COUNTS['faces_strictly_containing_R'], 'faces strictly containing R') + rho
        s_single = face * certified_count(COUNTS['single_site_faces_at_0'], 'single-site faces') + rho
        eps = face * certified_count(COUNTS['faces_meeting_R'], 'faces meeting R') + 2 * rho + s_single * s_single
        terms = {
            'am2_remainder': Term('am2_remainder', mult * rho, 'exact', rprov),
            'straddling': Term('straddling', 2 * W_OMEGA_NORM * T * s_strad, 'exact', 'enumeration_6_faces_containing_R'),
            'two_creation': Term('two_creation', 2 * W_OMEGA_NORM * s_single * s_single, 'exact', 'enumeration_33x33_single_site'),
            'density': Term('density', eps * eps, 'exact', 'enumeration_82_faces_meeting_R'),
            'normalization': Term('normalization', (2 * W_OMEGA_NORM * eps + eps * eps) * eps * eps, 'exact',
                                  'third_order_ratio'),
        }
        extra = {'t1': t1, 'T': T, 'rho': rho, 's_straddling_containing_R': s_strad,
                 's_single_site': s_single, 'epsilon': eps, 'factor_352J': K}
    elif tier == 'crude':
        T = J * G_R_UP
        rho = GP_R_UP * J * T
        eps = 2 * T + T * T
        terms = {
            'am2_remainder': Term('am2_remainder', mult * rho, 'crude', 'crude_352J_t_majorant'),
            'straddling': Term('straddling', 2 * W_OMEGA_NORM * T * T, 'crude', 'crude_t_times_t'),
            'two_creation': Term('two_creation', 2 * W_OMEGA_NORM * T * T, 'crude', 'crude_t_squared'),
            'density': Term('density', eps * eps, 'crude', 'crude_eps_2t_plus_t2'),
            'normalization': Term('normalization', (2 * W_OMEGA_NORM * eps + eps * eps) * eps * eps, 'crude',
                                  'crude_third_order_ratio'),
        }
        extra = {'t_crude': T, 'rho': rho, 'epsilon': eps}
    else:
        raise Rejected('unknown tier')
    B = assemble_remainder(tier, terms)
    return {'tier': tier, 'tau': t_signed, 'B': B, 'K2': B / (a * a), 'terms': terms, 'extra': extra,
            'multiplier': mult, 'multiplier_label': multiplier[1], 'remainder_form': remainder_form}


def ledger_json(led):
    out = {'tier': led['tier'], 'tau': qs(led['tau']), 'B_upper': qs(led['B']), 'B_preview': sci(led['B']),
           'K2_exact_rational': qs(led['K2']), 'K2_ceiling_1e-40': qs(ceil_to(led['K2'])),
           'K2_preview': sci(led['K2']), 'overlap_multiplier': qs(led['multiplier']),
           'overlap_multiplier_label': led['multiplier_label'], 'remainder_form': led['remainder_form'],
           'terms': {}, 'inputs': {k: qs(v) for k, v in sorted(led['extra'].items())}}
    a2 = led['tau'] * led['tau']
    for name in LEDGER_TERMS:
        t = led['terms'][name]
        out['terms'][name] = {'value': qs(t.value), 'per_tau2_preview': sci(t.value / a2), 'tier': t.tier,
                              'provenance': t.provenance}
    return out


def w2_ledger(tau):
    """Supplementary: |omega(W^2)-1/4| at the exact tier (y=(W^2-1/4)Omega_R, ||y||=1/4, ||W^2-1/4||=3/4)."""
    led = remainder_ledger(tau, 'exact')
    ex = led['extra']
    y_norm = Q(1, 4)
    val = 2 * y_norm * (ex['rho'] + ex['T'] * ex['s_straddling_containing_R'] + ex['s_single_site'] ** 2) \
        + Q(3, 4) * ex['epsilon'] ** 2
    return val


def aw2_rule(K2, grid_start_exp, threshold, max_steps=40):
    k = grid_start_exp
    for _ in range(max_steps):
        tau = Q(1, 10 ** k)
        if K2 * tau <= threshold:
            return tau
        k += 1
    raise Rejected('no decade-grid coupling satisfies the frozen AW2 rule')


def certify_tau_aw2(choice, K2, rule):
    computed = aw2_rule(K2, rule['grid_start_exp'], rule['threshold'])
    require(Q(choice) == computed, 'tau_AW2=%s is not the frozen rule value %s (largest decade coupling with K_2^+ tau<=%s)'
            % (qs(choice), qs(computed), qs(rule['threshold'])))
    return computed


# --------------------------------------------------------------- verdicts
def producer_outcome(parity_complete, coefficient_exact, flip_finite_volume, flip_aq_set_level,
                     k2_exact_tier, k2_uniform_in_N, rule_evaluated, sign_margin):
    if not (parity_complete and coefficient_exact):
        return 'insufficient'
    if not (flip_finite_volume and flip_aq_set_level and k2_exact_tier and k2_uniform_in_N and rule_evaluated):
        return 'limited'
    if Q(sign_margin) < 2:
        return 'limited'
    return 'accepted_within_scope'


def certify_outcome(recorded, inputs):
    computed = producer_outcome(**inputs)
    require(recorded == computed, 'recorded outcome %s differs from the evidence-derived outcome %s' % (recorded, computed))
    return computed


def validate_claim_flags(flags, parity_complete, flip_complete):
    expected = set(FIXED_FALSE_FLAGS) | {'first_order_parity_claim', 'flip_lemma_claim'}
    require(set(flags) == expected, 'claim flag set changed')
    for key in FIXED_FALSE_FLAGS:
        require(flags[key] is False, 'claim flag %s must be false in AW1' % key)
    require(flags['first_order_parity_claim'] is parity_complete, 'first_order_parity_claim must equal item-1 completion')
    require(flags['flip_lemma_claim'] is flip_complete, 'flip_lemma_claim must equal the flip-lemma completion')
    return True


def admit_bound(value, target):
    require(isinstance(value, Q) and isinstance(target, Q), 'admission requires exact rationals, not floating values')
    return value <= target


# --------------------------------------------------------------- validators
def certify_first_order_coefficient(value):
    require(Q(value) == COUNTS['derived_coefficient'],
            'first-order coefficient %s differs from the derived +1/144 (units, norm, 2Re, sign or face count)' % qs(value))
    return Q(value)


def certify_haar_moments(table):
    for n, v in table.items():
        require(parse_q(v) == haar_W_moment_cg(n), 'Haar moment E[W^%d]=%s contradicts the Clebsch-Gordan count' % (n, qs(v)))
    return True


def certify_pairing(face_a, face_b, claimed):
    """E_Haar[W_a W_b]: 1/4 on the diagonal, zero whenever a link carries one j=1/2 factor."""
    odd = face_a ^ face_b
    actual = HAAR_W2 if not odd else Q(0)
    require(Q(claimed) == actual, 'pairing E[W_a W_b]=%s but a link carries an odd number of j=1/2 factors' % qs(claimed)
            if odd else 'diagonal pairing must be E[W^2]=1/4')
    return actual


def haar_plaquette_product(faces):
    """E_Haar of a product of plaquette variables: zero if some link carries an odd number of j=1/2
    factors (Gamma_l is unitary and Haar-invariant); for a power of one plaquette the CG moment."""
    odd = frozenset()
    for f in faces:
        odd = odd ^ f
    if odd:
        return Q(0)
    must(len(set(faces)) == 1, 'only single-plaquette powers are evaluated here')
    return haar_W_moment_cg(len(faces))


def certify_tau_odd(value_plus, value_minus, label):
    require(value_minus.key() == (-value_plus).key(), '%s: the mirrored value is not the negative (not odd under the claimed map)' % label)
    return True


def certify_first_order_terms(claimed):
    """C(s), c(theta), omega(W^2): the state, Duhamel and energy first-order coefficients must vanish."""
    require(sorted(claimed) == ['duhamel', 'energy', 'state'], 'first-order terms must be itemized as state, Duhamel, energy')
    for k in sorted(claimed):
        require(Q(claimed[k]) == 0, 'first-order %s term %s: parity forces zero (E[W^2 W_f]=0, E[W_f]=0)' % (k, qs(claimed[k])))
    return True


def certify_multiplet_component(odd_set_size, energy_normalized):
    """A component returns to the energy-24 multiplet only with exactly four odd (j=1/2) links."""
    require(odd_set_size == 4 and Q(energy_normalized) == FACE_ENERGY,
            'component with %d odd links and energy %s is not in the energy-24 multiplet' % (odd_set_size, qs(energy_normalized)))
    return True


def certify_effect_label(label):
    require(label == 'static_equal_time_mean',
            'the first-order effect is a static equal-time ground mean; label %s (dynamical/mass-gap/C(s) shift) rejected' % label)
    return label


def certify_sign(tau, signed_value):
    require(sgn(Q(signed_value)) == sgn(Q(tau)), 'sign(<W>) must equal sign(tau) at first order (I1.5 convention)')
    return True


def certify_signed_first_order(tau, value):
    require(Q(value) == COUNTS['derived_coefficient'] * Q(tau),
            'first-order term %s is not the signed tau/144 at tau=%s (sign-blind |tau| evaluation?)' % (qs(value), qs(tau)))
    return True


def certify_quadratic_scaling(ratio_lo, ratio_hi, label):
    require(Q(99) <= ratio_lo and ratio_hi <= Q(101),
            '%s: B(tau)/B(tau/10) in [%s,%s] is not quadratic ([99,101])' % (label, sci(ratio_lo, 6), sci(ratio_hi, 6)))
    return True


def certify_remainder_order_claim(order, justification):
    require(order == 2, 'remainder order %d claimed from %s: oddness alone gives no O(tau^3); K tau|tau| is odd' % (order, justification))
    return True


def certify_tau_antisymmetry_claim(kappa, route):
    require(route == 'U_E', 'unknown antisymmetry route')
    require(all(Q(k) == 0 for k in kappa),
            'U_E maps (tau,kappa) to (-tau,-kappa): tau-antisymmetry at a nonzero selected triple is not given by U_E')
    return True


def certify_hamiltonian_image(image, target):
    require(image == target, 'U_E-conjugated Hamiltonian differs from the claimed image')
    return True


def certify_mean_first_order(value):
    require(Q(value) != 0, 'zero first-order mean: parity does not remove W paired with itself (f=W)')
    return certify_first_order_coefficient(value)


def certify_centering_identity(label, residue):
    require(label == 'vector', 'scalar subtraction is not vector centering (AT4 control: +1/10000 vs -51/10000)')
    require(Q(residue) >= 0, 'vector centering adds d^2 >= 0')
    return True


def certify_uncentered_equals_centered_to_second_order(m2_coefficient):
    require(Q(m2_coefficient) == 0, 'uncentered and centered correlations differ by m^2=(tau/144)^2+...: the mean is charged at second order')
    return True


def certify_wilson_split(n_classes_anchor0, w_included, contributing, coefficient):
    require(n_classes_anchor0 == 21 and w_included is True,
            'the Wilson face is one of the 21 omitted classes anchored at 0; excluding it changes the model')
    require(contributing == 1, 'only f=W pairs with W Omega_R; %d contributing faces merges W with the other 20' % contributing)
    return certify_first_order_coefficient(coefficient)


def certify_first_order_R_sum(value, exact_l1_lower):
    require(Q(value) >= exact_l1_lower, 'first-order R-sum %s|tau|/144 below the l1-over-owner-sets value (root-n misuse)' % sci(value, 8))
    return True


def certify_assembly(label):
    require(label == 'linear_sum', 'ledger terms are absolute bounds of different contributions: add them, never root-sum-square')
    return True


def certify_cover(cover):
    owners = {coarse(t) for t, _ in W_FACE}
    require(set(cover) == owners, 'cover is not the complete factor cover R={0,e_z} of the original W')
    return tuple(sorted(cover))


def certify_anchor_set(anchors):
    expected = sorted({vsub(u, v) for u in COVER for v in STAR})
    require(sorted(anchors) == expected, 'incident anchors %d differ from the complete R-S (7): incoming stars missing' % len(anchors))
    return True


def certify_clock_exponent(exponent, clock):
    require(clock in ('alpha', 'delta'), 'unknown clock')
    require(Q(exponent) == (FACE_ENERGY_ALPHA if clock == 'alpha' else FACE_ENERGY),
            'Euclidean exponent %s with the %s clock is the eightfold clock error (24 delta = 3 alpha)' % (qs(exponent), clock))
    return True


def certify_model_id(model_id, provenance):
    require(model_id == 'AQ_patterned_zero_selected', 'model id %s is not the frozen AQ subfamily (finite graph relabelled?)' % model_id)
    require(provenance == 'AQ1_centered_whole_star_subsequence', 'state provenance %s is not the AQ1 construction' % provenance)
    return True


def certify_aq_pointwise_claim(common_subsequence):
    require(common_subsequence is True, 'pointwise omega_{-tau}=-omega_tau needs a common subsequence; AQ statement is set-level')
    return True


def certify_variance_lower(claimed, m_abs, second_moment_lower):
    require(Q(claimed) <= Q(second_moment_lower) - Q(m_abs) ** 2, 'variance bound omits the mean-square charge m^2')
    return True


# --------------------------------------------------------------- contract
def am2_cap_from_gate():
    gate = json.loads((INPUTS / AM2_GATE_REL).read_text())
    m = re.search(r'\|tau\|<=1/(\d+)', gate['accepted'])
    must(m is not None and gate['verdict'] == 'accepted_within_scope', 'AM2 gate cap not found')
    return Q(1, int(m.group(1)))


def parse_aw2_rule(text):
    m = re.search(r'decade grid \{10\^-(\d+), 10\^-(\d+), \.\.\.\} with K_2\^\+ \* tau <= 1/(\d+) \(half the first-order coefficient\)', text)
    require(m is not None, 'AW2 coupling rule text not found')
    require(int(m.group(2)) == int(m.group(1)) + 1, 'AW2 grid is not a decade grid')
    return {'grid_start_exp': int(m.group(1)), 'threshold': Q(1, int(m.group(3)))}


EXPECTED_ERROR_TERMS = ['am2_remainder', 'two_creation', 'straddling', 'density', 'normalization_order',
                        'overlap_multiplier', 'arithmetic']


def validate_contract(data, am2_cap, derived_coefficient):
    require(data.get('id') == 'AW1' and data.get('status') == 'frozen_before_production', 'contract identity or status')
    p = data['parameters']
    require(parse_q(p['tau_cap']) == am2_cap, 'contract tau cap differs from the admitted AM2 cap')
    require(p['signs'] == ['+', '-'], 'both signs must be evaluated')
    require(len(p['selected_coefficients_over_alpha']) == 3 and all(parse_q(x) == 0 for x in p['selected_coefficients_over_alpha']),
            'contract selected triple is not zero')
    rule = parse_flip_set(p['flip_set'])
    cube = [face_links((x, y, z), a, c) for x in range(2) for y in range(2) for z in range(2) for _, a, c in ORIENTATIONS]
    certify_flip_set(lambda l: in_flip(rule, l), cube, 'contract flip set')
    m = re.search(r'omega_tau\(W\)=\+tau/(\d+)\+r\(tau\)', p['first_order_candidate'])
    require(m is not None and Q(1, int(m.group(1))) == derived_coefficient, 'first-order candidate differs from the derived +1/144')
    aw2 = parse_aw2_rule(p['aw2_coupling_rule'])
    require(aw2['threshold'] == derived_coefficient / 2, 'AW2 threshold is not half the derived first-order coefficient')
    pre = data['preregistration']
    tgt = pre['target']
    require(tgt['quantity'] == 'K_2^+ tau at the cap' and tgt['comparator'] == '<=' and parse_q(tgt['value']) == aw2['threshold'],
            'preregistered target differs from the frozen AW2 threshold')
    ref = re.fullmatch(r'(\S+) and (\S+)', pre['observable']['reference_value_exact'])
    require(ref is not None and parse_q(ref.group(1)) == HAAR_W and parse_q(ref.group(2)) == HAAR_W2,
            'reference values differ from the Haar moments 0 and 1/4')
    require(parse_q(pre['tau']['value']) == am2_cap and pre['tau']['signs_evaluated'] == ['+', '-'], 'prereg tau block')
    require(pre['error_terms_itemized'] == EXPECTED_ERROR_TERMS, 'itemized error-term list changed')
    ids = data['controls']
    require(ids == pre['controls_required']['ids'] and len(set(ids)) == len(ids) == 30,
            'controls list differs from the preregistered 30 control ids')
    require(set(data['new_control_semantics']) <= set(ids), 'semantics for an undeclared control')
    require(data.get('reverse_premise_isolation') is True, 'reverse premise isolation flag')
    return True


def validate_contract_bytes(raw, expected_sha, am2_cap, derived_coefficient):
    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'contract bytes do not match the bound hash')
    data = json.loads(raw)
    validate_contract(data, am2_cap, derived_coefficient)
    return data


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    for f in files:
        require(f not in FORBIDDEN_EXACT and not f.startswith(FORBIDDEN_PREFIXES) and not FORBIDDEN_PATTERN.match(f),
                'forbidden premise in reverse inputs: ' + f)
        require(f not in contract.get('forward_additional_premises', []), 'forward-only premise in reverse inputs: ' + f)
    require(sorted(files) == sorted(expected) and len(files) == len(expected),
            'reverse inputs inventory differs from AGENTS.md + contract + shared_premises')
    return True


def quat_mul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def quat_inv(q):
    return (q[0], -q[1], -q[2], -q[3])


def quat_neg(q):
    return tuple(-x for x in q)


def wilson_value(links):
    """links: dict over the four W links; (1/2)Tr U(0,x)U(e_x,z)U(e_z,x)^-1U(0,z)^-1 = real quaternion part."""
    u = quat_mul(quat_mul(links[((0, 0, 0), 0)], links[((1, 0, 0), 2)]),
                 quat_mul(quat_inv(links[((0, 0, 1), 0)]), quat_inv(links[((0, 0, 0), 2)])))
    return u[0]


def symbolic_hamiltonian(N, tau, kappa, classes, selected_classes):
    """Normalized H_N(tau,kappa) as exact coefficients: Casimirs, omitted faces (-tau/3), selected faces (-8 kappa_r)."""
    sites, stars, omitted, _ = box_faces(N, classes, selected_classes)
    h = {}
    for b in sites:
        for r in range(4):
            for s in range(2):
                t = (4 * b[0] + r, 2 * b[1] + s, b[2])
                for d in range(3):
                    h[('C', (t, d))] = Q(8)
        for cls in selected_classes:
            links = class_face(b, cls)[0]
            h[('W', links)] = h.get(('W', links), Q(0)) - 8 * Q(kappa[cls[1]])
    for _, links, _ in omitted:
        h[('W', links)] = h.get(('W', links), Q(0)) - Q(tau) / 3
    return {k: v for k, v in h.items() if v != 0}


def conjugate_by_flip(h, rule):
    out = {}
    for (kind, obj), v in h.items():
        if kind == 'C':
            out[(kind, obj)] = v
        else:
            out[(kind, obj)] = v * (-1) ** flip_count(rule, obj)
    return out


# ==================================================================== compute
def compute():
    global TAU_CAP
    check_py_sha = sha256_file(HERE / 'check.py')          # recorded before any evaluation
    raw = (INPUTS / CONTRACT_REL).read_bytes()
    contract_sha = hashlib.sha256(raw).hexdigest()
    am2_cap = am2_cap_from_gate()
    TAU_CAP = am2_cap

    # ---------------------------------------------- A. first-order coefficient (derived before reading candidates)
    amp = first_order_amplitude('delta', 'delta')
    must(amp == first_order_amplitude('alpha', 'alpha') == Q(1, 72), 'psi^(1) amplitude tau/72 in both unit systems')
    c1 = am2_creation_coefficient('delta')
    must(c1 == -amp, 'AM2 creation convention: c^(1)=L_0=-psi^(1)')
    derived_coefficient = 2 * amp * HAAR_W2          # 2 <W Omega_0, psi^(1)> with only f=W surviving
    COUNTS['derived_coefficient'] = derived_coefficient
    must(derived_coefficient == Q(1, 144), 'derived first-order coefficient')

    contract = validate_contract_bytes(raw, CONTRACT_SHA256, am2_cap, derived_coefficient)
    record('contract_snapshot_bound', contract_sha == CONTRACT_SHA256, contract_sha256=contract_sha,
           source='inputs/' + CONTRACT_REL)
    record('check_py_hash_recorded_before_evaluation', len(check_py_sha) == 64, check_py_sha256=check_py_sha)
    cache = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if '__pycache__' in p.parts or p.suffix == '.pyc')
    record('no_interpreter_cache_in_closure', cache == [])

    params = contract['parameters']
    pre = contract['preregistration']
    target = parse_q(pre['target']['value'])
    aw2 = parse_aw2_rule(params['aw2_coupling_rule'])
    ref_m = re.fullmatch(r'(\S+) and (\S+)', pre['observable']['reference_value_exact'])
    reference = {'omega_0(W)': parse_q(ref_m.group(1)), 'omega_0(W^2)': parse_q(ref_m.group(2))}
    contract_rule = parse_flip_set(params['flip_set'])
    cap = am2_cap
    taus = [cap if s == '+' else -cap for s in params['signs']]

    # ---------------------------------------------- B. SU(2) characters: three exact routes
    moments = {}
    for n in range(9):
        cg, weyl, sph = haar_W_moment_cg(n), haar_W_moment_weyl(n), haar_W_moment_sphere(n)
        must(cg == weyl == sph, 'Haar moment routes disagree at n=%d' % n)
        moments[n] = cg
    record('haar_parity_three_exact_routes', moments[1] == 0 and moments[2] == Q(1, 4) and moments[3] == 0
           and moments[4] == Q(1, 8) and all(moments[n] == 0 for n in (1, 3, 5, 7))
           and reference['omega_0(W)'] == HAAR_W and reference['omega_0(W^2)'] == HAAR_W2,
           moments={str(n): qs(v) for n, v in moments.items()},
           routes=['Clebsch-Gordan trivial multiplicity in (1/2)^{(x)n} / 2^n',
                   'Weyl integration (2/pi) int cos^n sin^2 by Wallis ratios',
                   'free z link: plaquette holonomy Haar = uniform S^3, W=q_0 (AQ2 section 5)'],
           trivial_multiplicities=[trivial_multiplicity_chi_half_power(n) for n in range(9)],
           reference_read_from_contract={k: qs(v) for k, v in reference.items()})
    spec = [{'two_j': t, 'casimir': qs(casimir(t)), 'center_parity': center_parity(t)} for t in range(7)]
    record('center_flip_commutes_with_casimir', CASIMIR_HALF == Q(3, 4) and all(center_parity(t) == (-1) ** t for t in range(7)),
           spectrum=spec, statement='Gamma_l (U_l -> -U_l) acts as (-1)^{2j} and C_l as j(j+1) on the same Peter-Weyl blocks')

    # ---------------------------------------------- C. I1 table, classes, counts
    i1_text = (INPUTS / I1_REL).read_text()
    parsed = parse_i1_table(i1_text)
    derived_table = derive_i1_table()
    must(len(parsed) == 24, 'I1 table parse')
    record('i1_table_parsed_from_snapshot_equals_fine_lattice', parsed == derived_table
           and sum(1 for r in parsed if r[4] == 'omitted') == 21,
           classes=len(parsed), omitted=sum(1 for r in parsed if r[4] == 'omitted'), source='inputs/' + I1_REL)
    classes = [r for r in parsed if r[4] == 'omitted']
    selected_classes = [r for r in parsed if r[4] == 'selected']
    f0 = faces_of_factor(ORIGIN, classes)
    fz = faces_of_factor(EZ, classes)
    meeting = dict(f0)
    meeting.update(fz)
    R = set(COVER)
    by_owner0 = {}
    for key, (links, owners) in f0.items():
        by_owner0[owners] = by_owner0.get(owners, 0) + 1
    mult_hist = {}
    for n in by_owner0.values():
        mult_hist[n] = mult_hist.get(n, 0) + 1
    inside = [k for k, (l, o) in meeting.items() if set(o) <= R]
    both = [k for k, (l, o) in meeting.items() if R <= set(o)]
    strict = [k for k in both if k not in inside]
    single0 = [k for k, (l, o) in meeting.items() if ORIGIN in o and EZ not in o]
    singlez = [k for k, (l, o) in meeting.items() if EZ in o and ORIGIN not in o]
    straddling = [k for k, (l, o) in meeting.items() if not set(o) <= R]
    anchored0 = [k for k in meeting if k[0] == ORIGIN]
    w_key = [k for k, (l, o) in meeting.items() if l == W_FACE]
    must(len(w_key) == 1, 'the Wilson face is one omitted face meeting R')
    w_key = w_key[0]
    must(W_DISPLAYED == W_FACE, 'displayed W links equal the xz face at the fine origin')
    others0 = [k for k in anchored0 if k != w_key]
    split20 = {'inside_R': sum(1 for k in others0 if set(meeting[k][1]) <= R),
               'strictly_containing_R': sum(1 for k in others0 if R < set(meeting[k][1])),
               'single_site_0': sum(1 for k in others0 if EZ not in meeting[k][1])}
    incident = sorted({k[0] for k in meeting})
    derived = {'faces_per_factor': len(f0), 'owner_sets_per_factor': len(by_owner0),
               'faces_meeting_R': len(meeting), 'faces_inside_R': len(inside), 'faces_touching_both': len(both),
               'faces_strictly_containing_R': len(strict), 'straddling_faces': len(straddling),
               'single_site_faces_at_0': len(single0), 'single_site_faces_at_e_z': len(singlez),
               'classes_anchored_at_0': len(anchored0), 'other_classes_anchored_at_0': len(others0)}
    for name, value in derived.items():
        COUNTS[name] = DerivedCount(value, PROVENANCE)
    record('face_enumeration_translation_covariance', len(fz) == len(f0) and incident == sorted({vsub(u, v) for u in COVER for v in STAR})
           and len(incident) == 7 and derived['straddling_faces'] == derived['faces_strictly_containing_R']
           + derived['single_site_faces_at_0'] + derived['single_site_faces_at_e_z']
           and derived['faces_meeting_R'] == 2 * derived['faces_per_factor'] - derived['faces_touching_both']
           and split20['inside_R'] + split20['strictly_containing_R'] + split20['single_site_0'] == derived['other_classes_anchored_at_0'],
           derived=derived, owner_set_multiplicity_histogram={str(k): v for k, v in sorted(mult_hist.items())},
           wilson_face={'fine_base': [0, 0, 0], 'orientation': 'xz', 'class': 'xz r=0 s=0', 'anchor': [0, 0, 0],
                        'owner_set': [list(o) for o in meeting[w_key][1]]},
           other_20_anchored_at_0_split=split20, incident_anchors=[list(a) for a in incident],
           rule='faces owning a link of u are the classes k anchored at u-d, d in the class support (I1.4)')
    cand = re.search(r'(\d+) owner sets with multiplicities \{([0-9x,]+)\}, (\d+) faces meeting R, (\d+) touching both factors of R',
                     contract['required'][3])
    sel_text = (INPUTS / 'research/round32/advisor/selection-aw1.md').read_text()
    sel_m = re.search(r'\((\d+)/(\d+)/(\d+)/(\d+)/(\d+)\)', sel_text)
    must(cand is not None and sel_m is not None, 'contract/selection candidate counts not found')
    cand_counts = {'owner_sets_per_factor': int(cand.group(1)), 'faces_meeting_R': int(cand.group(3)),
                   'faces_touching_both': int(cand.group(4))}
    cand_hist = {int(m): int(c) for m, c in (item.split('x') for item in cand.group(2).split(','))}
    sel_counts = dict(zip(['faces_per_factor', 'owner_sets_per_factor', 'faces_meeting_R', 'faces_inside_R', 'straddling_faces'],
                          [int(sel_m.group(i)) for i in range(1, 6)]))
    record('derived_counts_reproduce_contract_candidates',
           all(derived[k] == v for k, v in cand_counts.items()) and mult_hist == cand_hist
           and all(derived[k] == v for k, v in sel_counts.items()),
           candidates_contract_item_4=cand_counts, candidates_selection_note=sel_counts,
           note='candidates are parsed and compared only after derivation; every value used is the derived one')
    box_info = {}
    for N in (2, 3):
        sites, stars, omitted, selected = box_faces(N, classes, selected_classes)
        per_site = {}
        for _, links, owners in omitted:
            for u in owners:
                per_site[u] = per_site.get(u, 0) + 1
        anchors_R = [a for a in sorted({vsub(u, v) for u in COVER for v in STAR}) if a in set(stars)]
        box_info[str(N)] = {'sites': len(sites), 'stars': len(stars), 'omitted_faces': len(omitted),
                            'selected_faces': len(selected), 'max_faces_per_site': max(per_site.values()),
                            'incident_stars_retained': len(anchors_R)}
        must(max(per_site.values()) == derived['faces_per_factor'] and len(anchors_R) == 7, 'box counts')
    record('whole_star_boxes_bulk_bound_and_incident_stars', True, boxes=box_info,
           statement='every per-site count is at most the bulk 49; all seven incident stars are retained for N>=2')

    # ---------------------------------------------- D. parity theorem (item 1)
    _, _, omitted2, selected2 = box_faces(2, classes, selected_classes)
    all_faces2 = [links for _, links, _ in omitted2]
    w_count = sum(1 for f in all_faces2 if f == W_FACE)
    must(w_count == 1, 'W occurs once among the omitted faces of Lambda_2')

    def odd_links(faces):
        odd = frozenset()
        for f in faces:
            odd = odd ^ f
        return odd

    e_w2wf = [len(odd_links([W_FACE, W_FACE, f])) > 0 for f in all_faces2]
    e_wwf = [f for f in all_faces2 if not odd_links([W_FACE, f])]
    e_wf = [len(odd_links([f])) > 0 for f in all_faces2]
    meeting_faces = sorted((links for links, _ in meeting.values()), key=lambda f: sorted(f))
    e_w2wf_R = [len(odd_links([W_FACE, W_FACE, f])) > 0 for f in meeting_faces]
    record('parity_E_W2_Wf_vanishes_every_omitted_face', all(e_w2wf) and all(e_w2wf_R) and all(e_wf)
           and len(odd_links([W_FACE] * 3)) == 4 and moments[3] == 0,
           faces_in_Lambda_2=len(all_faces2), faces_meeting_R=len(meeting_faces),
           statement='E[W^2 W_f]=0 for every omitted f including f=W (a link carries an odd number of j=1/2 factors; '
                     'for f=W each link carries three); E[W_f]=0; E[W^3]=0')
    first_order_state = 2 * amp * sum(haar_plaquette_product([W_FACE, W_FACE, f]) for f in all_faces2)
    v_per_tau = FACE_COUPLING_PER_TAU['alpha']                    # V' = -(1/24) sum W_f in alpha units
    energy_first = v_per_tau * sum(haar_plaquette_product([f]) for f in all_faces2)
    duhamel_first = -(v_per_tau * sum(haar_plaquette_product([W_FACE, W_FACE, f]) for f in all_faces2)
                      - energy_first * HAAR_W2)
    terms_C = {'state': first_order_state, 'duhamel': duhamel_first, 'energy': energy_first}
    terms_c_theta = dict(terms_C)
    terms_W2 = {'state': first_order_state, 'duhamel': Q(0), 'energy': energy_first}
    must(certify_first_order_terms(terms_C) and certify_first_order_terms(terms_c_theta) and certify_first_order_terms(terms_W2),
         'first-order parity terms')
    omega_W_first = 2 * amp * sum(haar_plaquette_product([W_FACE, f]) for f in all_faces2)
    record('first_order_terms_state_duhamel_energy_vanish', omega_W_first == derived_coefficient and len(e_wwf) == 1,
           C_of_s={'state_coefficient_of_exp(-3s)': qs(terms_C['state']), 'duhamel_coefficient_of_s_exp(-3s)': qs(terms_C['duhamel']),
                   'energy_first_order': qs(terms_C['energy']), 'mean_square': 'm^2=(tau/144)^2+O(tau^3): second order'},
           real_time_c_theta={'state_coefficient_of_exp(3i theta)': qs(terms_c_theta['state']),
                              'duhamel_coefficient_of_i theta exp(3i theta)': qs(terms_c_theta['duhamel'])},
           omega_W2={'state': qs(terms_W2['state'])}, omega_W_first_order_coefficient=qs(omega_W_first),
           vectors='c^(1) is odd under Gamma_l on the four links of each f; W^2 Omega_0 and W alpha^0_theta(W) Omega_0 = e^{3i theta} W^2 Omega_0 '
                   'are even under every Gamma_l; unitary Gamma_l forces the pairings to vanish')
    # multiplet
    sizes = {}
    for f in all_faces2:
        sizes[len(W_FACE ^ f)] = sizes.get(len(W_FACE ^ f), 0) + 1
    ident = W_FACE ^ W_FACE
    comps_f_eq_W = {'vacuum': {'energy_normalized': '0', 'weight': qs(HAAR_W2)},
                    'spin_one_on_W': {'energy_normalized': qs(ALPHA_OVER_DELTA * 4 * casimir(2)), 'weight_norm_sq': qs(Q(1, 16))}}
    must(len(ident) == 0 and 4 not in sizes and sizes.get(0) == 1, 'no omitted face returns W Omega_0 to the multiplet')
    triple_faces = meeting_faces
    n_triples, bad_triples = 0, 0
    for g, f, h in combinations_with_replacement(range(len(triple_faces)), 3):
        n_triples += 1
        chain = triple_faces[g] ^ triple_faces[f] ^ triple_faces[h]
        if not chain or flip_count(contract_rule, chain) % 2 == 0:
            bad_triples += 1
    record('degenerate_multiplet_zero_first_order_splitting', bad_triples == 0,
           odd_set_sizes_of_W_times_Wf=({str(k): v for k, v in sorted(sizes.items())}), f_equal_W_components=comps_f_eq_W,
           physical_multiplet_triples_checked=n_triples,
           statement='V W Omega_0 has odd-link sets W^f of size 0 (f=W: vacuum 1/4 plus spin one at energy 64), 6 or 8, '
                     'never 4: P_24 V W Omega_0=0. On the gauge-invariant energy-24 space span{W_g Omega_0}, '
                     'E[W_g W_f W_h]=0 for all triples because E pairs oddly with g+f+h. The unconstrained (non-invariant) '
                     'energy-24 eigenspace is not claimed to be unsplit.')
    record('parity_conclusion_first_order', True,
           omega_W2='1/4+O(tau^2): first-order coefficient 0 (constant: supplementary exact-tier bound below)',
           C_of_s='exp(-3s)/4+O(tau^2) in every finite box (real-analytic in tau, first derivative 0); the O(tau^2) '
                  'constant of C(s) is explicitly left unbounded here, so no uniform or AQ-limit tau^2 statement for C(s)',
           omega_W='+tau/144 at first order (f=W paired with itself; not removed by parity)')

    # ---------------------------------------------- E. first-order coefficient (item 3)
    signed = {qs(t): qs(derived_coefficient * t) for t in taus}
    must(all(certify_signed_first_order(t, derived_coefficient * t) for t in taus), 'signed first-order values')
    pair_rows = []
    for key in sorted(meeting, key=lambda k: (k[0], k[1])):
        links = meeting[key][0]
        pair_rows.append(certify_pairing(W_FACE, links, HAAR_W2 if links == W_FACE else Q(0)))
    orientation_rows = {}
    for k, cls in enumerate(classes):
        g_links, g_owner = class_face(ORIGIN, cls)
        same_owner = [f for f in all_faces2 if tuple(sorted({coarse(t) for t, _ in f})) == g_owner]
        coeff = 2 * amp * sum(haar_plaquette_product([g_links, f]) for f in same_owner)
        orientation_rows['%s r=%d s=%d' % (cls[0], cls[1], cls[2])] = qs(coeff)
        must(coeff == derived_coefficient, 'orientation invariance of the first-order coefficient')
    record('first_order_coefficient_plus_tau_over_144', derived_coefficient == Q(1, 144) and sum(pair_rows) == HAAR_W2,
           psi1_amplitude_per_tau=qs(amp), am2_c1_coefficient_per_tau=qs(c1),
           formula='omega_tau(W) = 2 Re<W Omega_0, psi^(1)> + O(tau^2) = -2 Re<W Omega_0, c^(1)> + O(tau^2) with c^(1)=L_0 (AM2/AV1 sign)',
           sign_derivation='H contains -(alpha tau/24) W_f (I1.5); psi^(1)=-H_0^{-1}V Omega_0=+(tau/72) sum W_f Omega_0; '
                           'only f=W survives: 2(tau/72)E[W^2]=tau/144>0 for tau>0',
           signed_first_order_terms=signed, candidate_from_contract=params['first_order_candidate'],
           orientation_invariance=orientation_rows, reversed_orientation='chi_1/2(U^-1)=chi_1/2(U): identical W and coefficient')

    # ---------------------------------------------- F. flip lemma (item 2)
    sols = residue_solutions()
    cyclic = {0: 1, 1: 2, 2: 0}
    anti = {0: 2, 1: 0, 2: 1}
    must(sols == [anti, cyclic] or sols == [cyclic, anti], 'reverse reconstruction of one-coordinate flip rules')
    record('flip_set_reverse_derived', contract_rule == cyclic and len(sols) == 2,
           solutions=['{(p,%s): p_%s even}' % ('xyz'[d], 'xyz'[s[d]]) for s in sols for d in range(3)],
           contract_rule_is_cyclic=contract_rule == cyclic,
           derivation='xy is odd iff exactly one of [sigma(x)=y],[sigma(y)=x]; similarly xz, yz: exactly the two derangements')
    residue = {}
    for name, a, c in ORIENTATIONS:
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    residue['%s@%d%d%d' % (name, x, y, z)] = flip_count(contract_rule, face_links((x, y, z), a, c))
    must(all(v in (1, 3) for v in residue.values()) and len(residue) == 24, 'residue enumeration')
    big = plaquettes_in_box((-9, -9, -9), (9, 9, 9))
    hist = {}
    for f in big:
        n = flip_count(contract_rule, f)
        hist[n] = hist.get(n, 0) + 1
    fac_counts = {'factor_0': sorted({flip_count(contract_rule, l) for l, _ in f0.values()}),
                  'factor_e_z': sorted({flip_count(contract_rule, l) for l, _ in fz.values()})}
    sel_counts_E = sorted({flip_count(contract_rule, class_face(u, cls)[0]) for u in COVER for cls in selected_classes})
    lam2_counts = sorted({flip_count(contract_rule, l) for l in all_faces2} | {flip_count(contract_rule, l) for l in selected2})
    must(certify_flip_set(lambda l: in_flip(contract_rule, l), big, 'E'), 'E odd on the box')
    record('flip_set_odd_intersection_full_enumeration', set(hist) <= {1, 3} and all(set(v) <= {1, 3} for v in fac_counts.values())
           and len(f0) == 49 and len(fz) == 49 and set(sel_counts_E) <= {1, 3} and set(lam2_counts) <= {1, 3},
           residue_classes=residue, fine_box='[-9,9]^3', plaquettes=len(big), histogram={str(k): v for k, v in sorted(hist.items())},
           omitted_faces_of_factor=fac_counts, faces_enumerated_per_factor=[len(f0), len(fz)],
           selected_faces_counts=sel_counts_E, lambda2_all_faces_counts=lam2_counts,
           note='factor 0 and factor e_z exhaust the two z-parity classes; coarse x,y translations are even fine shifts')
    g_fun = lambda p: (p[0] * p[1] + p[1] * p[2] + p[2] * p[0]) % 2
    cob_ok = all((in_flip(cyclic, (p, d)) != in_flip(anti, (p, d))) == (g_fun(p) != g_fun(vadd(p, DIRS[d])))
                 for x in range(-4, 5) for y in range(-4, 5) for z in range(-4, 5) for p in [(x, y, z)] for d in range(3))
    record('flip_set_unique_up_to_center_gauge', cob_ok,
           statement='the two solutions differ by the coboundary of g=xy+yz+zx mod 2 (a center gauge transformation); '
                     'E itself is not a cocycle (its coboundary is 1 on every plaquette), so U_E is not a gauge transformation')
    # exact quaternion fixture: flip on W's links, gauge commutation
    links = {((0, 0, 0), 0): (Q(3, 5), Q(4, 5), Q(0), Q(0)), ((1, 0, 0), 2): (Q(1, 3), Q(2, 3), Q(2, 3), Q(0)),
             ((0, 0, 1), 0): (Q(1, 2), Q(1, 2), Q(1, 2), Q(1, 2)), ((0, 0, 0), 2): (Q(2, 7), Q(3, 7), Q(6, 7), Q(0))}
    must(all(sum(x * x for x in q) == 1 for q in links.values()), 'rational unit quaternions')
    w0 = wilson_value(links)
    flipped = {l: (quat_neg(q) if in_flip(contract_rule, l) else q) for l, q in links.items()}
    gauge = {(0, 0, 0): (Q(0), Q(3, 5), Q(0), Q(4, 5)), (1, 0, 0): (Q(1, 3), Q(0), Q(2, 3), Q(2, 3)),
             (1, 0, 1): (Q(2, 3), Q(1, 3), Q(0), Q(2, 3)), (0, 0, 1): (Q(6, 7), Q(0), Q(2, 7), Q(3, 7))}
    must(all(sum(x * x for x in q) == 1 for q in gauge.values()), 'rational unit gauge quaternions')

    def gauge_act(ls):
        return {(t, d): quat_mul(quat_mul(gauge[t], q), quat_inv(gauge[vadd(t, DIRS[d])])) for (t, d), q in ls.items()}

    def flip_act(ls):
        return {l: (quat_neg(q) if in_flip(contract_rule, l) else q) for l, q in ls.items()}

    record('flip_exact_su2_fixture', wilson_value(flipped) == -w0 and wilson_value(gauge_act(links)) == w0
           and flip_act(gauge_act(links)) == gauge_act(flip_act(links)) and flip_count(contract_rule, W_FACE) == 3,
           W_value=qs(w0), W_after_flip=qs(wilson_value(flipped)), links_of_W_in_E=flip_count(contract_rule, W_FACE),
           statement='-1 is central: -(g U h^-1)=g(-U)h^-1, so U_E commutes with every endpoint gauge action and flips W',
           configuration='one exact rational SU(2) configuration of the four W links and their endpoint gauge elements (identity check, not a model)')
    # symbolic Hamiltonian conjugation
    kappa0 = (Q(0), Q(0), Q(0))
    kappa1 = (Q(1, 7), Q(-1, 9), Q(1, 3))
    tau_f = cap
    h_plus = symbolic_hamiltonian(2, tau_f, kappa0, classes, selected_classes)
    h_minus = symbolic_hamiltonian(2, -tau_f, kappa0, classes, selected_classes)
    conj0 = conjugate_by_flip(h_plus, contract_rule)
    hk = symbolic_hamiltonian(2, tau_f, kappa1, classes, selected_classes)
    conjk = conjugate_by_flip(hk, contract_rule)
    h_mm = symbolic_hamiltonian(2, -tau_f, tuple(-k for k in kappa1), classes, selected_classes)
    h_mk = symbolic_hamiltonian(2, -tau_f, kappa1, classes, selected_classes)
    record('flip_hamiltonian_conjugation_every_box_term', conj0 == h_minus and conjk == h_mm and conjk != h_mk,
           box='Lambda_2 (all onsite Casimirs, 1344 omitted and 375 selected face terms)',
           terms=len(h_plus), statement='U_E H_N(tau,kappa) U_E^* = H_N(-tau,-kappa); at kappa=0 this is H_N(-tau); '
                                         'on-site cutoffs are spectral projections of Casimir sums, fixed by U_E')
    # one-plaquette exact fixture (labelled finite graph), both signs separately in Q(sqrt(D))
    g0, wmat, fl = one_plaquette(1)
    plaq_rows = {}
    for t in (cap, Q(1, 100)):
        hp = madd(g0, mscale(FACE_COUPLING_PER_TAU['alpha'] * t, wmat))
        hm = madd(g0, mscale(FACE_COUPLING_PER_TAU['alpha'] * (-t), wmat))
        must(matmul(matmul(fl, hp), fl) == hm, 'U H(tau) U = H(-tau) on the fixture')
        vp, mp = two_level_ground_mean(hp[0][1])
        vm, mm = two_level_ground_mean(hm[0][1])
        must(mp.key() == (-mm).key() and (vp + vm).a == 0 and (vp + vm).b == 0, 'exact antisymmetry of the fixture mean')
        must(mp.sign() == 1 and mm.sign() == -1, 'fixture sign')
        lo, hi = mp.bounds()
        plaq_rows[qs(t)] = {'mean_plus': mp.text(), 'mean_minus': mm.text(), 'mean_plus_bounds': [qs(lo), qs(hi)],
                            'first_order_tau_over_144': qs(t / 144)}
    series_W, energies_W, _ = rs_series([Q(0), Q(3), Q(8), Q(15)], mscale(FACE_COUPLING_PER_TAU['alpha'], one_plaquette(3)[1]),
                                        one_plaquette(3)[1], 5)
    w_sq = matmul(one_plaquette(3)[1], one_plaquette(3)[1])
    series_W2, _, _ = rs_series([Q(0), Q(3), Q(8), Q(15)], mscale(FACE_COUPLING_PER_TAU['alpha'], one_plaquette(3)[1]), w_sq, 5)
    record('one_plaquette_exact_flip_and_sign_fixture', series_W[1] == Q(1, 144) and all(series_W[k] == 0 for k in (0, 2, 4))
           and series_W2[0] == Q(1, 4) and all(series_W2[k] == 0 for k in (1, 3, 5)),
           label='finite graph: one gauge-invariant plaquette, j<=1/2 exact (both signs separately) and j<=3/2 series',
           model_is_finite_graph=True, transfers_to_aq=False, graph_name='one_plaquette_character_truncation',
           exact_two_level=plaq_rows, rs_mean_W=[qs(v) for v in series_W], rs_mean_W2=[qs(v) for v in series_W2],
           rs_energy=[qs(v) for v in energies_W])
    # AQ passage toy: set-level versus pointwise
    a_toy = Q(1, 1000)

    def x_seq(t, N):
        # a finite-volume sequence obeying the flip identity x_N(-t)=-x_N(t) exactly, with two subsequential limits
        return t / 144 + sgn(t) * (a_toy if N % 2 == 0 else -a_toy)

    must(all(x_seq(-cap, N) == -x_seq(cap, N) for N in range(2, 12)), 'toy obeys the finite-volume flip identity')
    set_plus = sorted({x_seq(cap, N) for N in range(2, 12)})
    set_minus = sorted({x_seq(-cap, N) for N in range(2, 12)})
    independent = x_seq(-cap, 3) + x_seq(cap, 2)          # -tau along odd N, +tau along even N
    common = x_seq(-cap, 2) + x_seq(cap, 2)
    pointwise_rejected = rejection(certify_aq_pointwise_claim, False)
    record('flip_aq_passage_whole_set', set_minus == sorted(-v for v in set_plus) and independent != 0 and common == 0,
           statement='omega_{N,-tau}=omega_{N,tau} o alpha_E for every N and cutoff (unique grounds, AM2); along any common '
                     'subsequence the -tau states converge to omega_tau o alpha_E, so S(-tau)=S(tau) o alpha_E as sets; '
                     'alpha_E intertwines the finite and Nachtergaele-Sims dynamics, so paired states have equal C(s), c(theta), omega(W^2)',
           toy_sets={'S_plus': [qs(v) for v in set_plus], 'S_minus': [qs(v) for v in set_minus]},
           toy_label='abstract scalar sequences obeying the finite-volume identity; not AQ data',
           independent_subsequences_sum=qs(independent), common_subsequence_sum=qs(common),
           pointwise_claim_without_common_subsequence_rejected=pointwise_rejected)
    # finding (not claimed): a selected-even flip cochain exists
    b8 = (0, 1, 0, 1, 1, 0, 1, 0)

    def in_epp(link):
        p, d = link
        if d == 0:
            return p[1] % 2 == 1 and p[0] % 4 in (0, 1, 2)
        if d == 1:
            return p[1] % 2 == 1 and b8[p[0] % 8] == 1
        return False

    epp_ok = True
    for x in range(-9, 11):
        for y in range(-5, 7):
            for z in range(-3, 4):
                for name, a, c in ORIENTATIONS:
                    f = face_links((x, y, z), a, c)
                    sel = name == 'xy' and y % 2 == 0 and x % 4 in (0, 1, 2)
                    if (sum(1 for l in f if in_epp(l)) % 2 == 1) != sel:
                        epp_ok = False
                    if (sum(1 for l in f if in_flip(contract_rule, l) != in_epp(l)) % 2) != (0 if sel else 1):
                        epp_ok = False
    record('finding_selected_even_flip_cochain_not_claimed', epp_ok,
           status='finding for review; not claimed, not used by any admission Boolean or claim flag',
           statement="E''={(p,x): p_y odd, p_x mod 4 in {0,1,2}} u {(p,y): p_y odd, b(p_x mod 8)=1}, b=(0,1,0,1,1,0,1,0), "
                     "has coboundary equal to the selected-face indicator (cube condition holds: 0 or 2 selected faces per cube). "
                     "E'=E xor E'' meets omitted faces oddly and selected faces evenly, so U_E' would map H(tau,kappa) to H(-tau,kappa) "
                     "if the selected-strip onsite operator contains only Casimirs and selected W terms (AT4 F01 form; A1 not read). "
                     "The contract control (U_E gives no tau-antisymmetry at kappa!=0) is unaffected.")

    # ---------------------------------------------- G. K_2 ledger (item 4)
    led = {}
    for t in taus:
        led[('exact', qs(t))] = remainder_ledger(t, 'exact')
        led[('crude', qs(t))] = remainder_ledger(t, 'crude')
    must(led[('exact', qs(taus[0]))]['K2'] == led[('exact', qs(taus[1]))]['K2'], 'sign-blind remainder (|tau| replay)')
    ex = led[('exact', qs(cap))]
    cr = led[('crude', qs(cap))]
    cons = remainder_ledger(cap, 'exact', multiplier=(Q(4), 'conservative_labelled'))
    dirg = remainder_ledger(cap, 'exact', remainder_form='directed_G')
    K2 = ex['K2']
    K2_up = ceil_to(K2)
    mono = [remainder_ledger(cap / 10 ** k, 'exact')['K2'] for k in range(1, 4)]
    must(all(m <= K2 for m in mono) and all(mono[i + 1] <= mono[i] for i in range(len(mono) - 1)), 'K_2 increasing in |tau|')
    ratio = ex['B'] / remainder_ledger(cap / 10, 'exact')['B']
    must(certify_quadratic_scaling(ratio, ratio, 'exact ledger'), 'quadratic scaling')
    w2 = w2_ledger(cap)
    record('k2_exact_tier_itemized_uniform', K2 > 0 and K2_up >= K2 and cons['K2'] > K2 and dirg['K2'] < K2,
           exact_tier=ledger_json(ex), conservative_multiplier_4=ledger_json(cons), directed_G_variant=ledger_json(dirg),
           K2_at_smaller_tau_previews=[sci(m) for m in mono], quadratic_ratio_B_tau_over_B_tenth=sci(ratio),
           uniform='every entry is an anchored sum at the two sites of R or the global t<=T, bounded independently of N and of the cutoff (L>=24)')
    record('k2_crude_tier_retained', cr['K2'] > K2, crude_tier=ledger_json(cr),
           note='crude majorant t<=J G(R)=592|tau| everywhere; limited-tier value, retained')
    record('omega_W2_supplementary_second_order_bound', w2 > 0, value_at_cap=qs(w2), K_W2_per_tau2=sci(w2 / (cap * cap)),
           statement='|omega(W^2)-1/4| <= 2||y||(rho+T s_strad+s_0 s_z)+(3/4)eps^2 with y=(W^2-1/4)Omega_R, ||y||=1/4: '
                     'uniform in N, passes to every AQ limit; supplementary to item 1, not a target')

    # ---------------------------------------------- H. creation-algebra audit fixture
    creators = {
        (0, 1): {(1, 1): Q(1, 5), (2, 1): Q(-1, 7), (1, 2): Q(1, 9)},
        (0, 1, 2): {(1, 1, 1): Q(1, 4), (2, 1, 1): Q(1, 6)},
        (0, 2): {(1, 1): Q(1, 3)}, (0, 3): {(2, 1): Q(-1, 8)}, (1, 3): {(1, 1): Q(1, 5)},
        (0,): {(1,): Q(1, 10)}, (1,): {(2,): Q(-1, 9)},
        (2,): {(1,): Q(-2, 3)}, (3,): {(1,): Q(1, 2)}, (2, 3): {(1, 1): Q(1, 4)},
    }
    vac = {(0, 0, 0, 0): Q(1)}
    out_keys = sorted(k for k in creators if 0 not in k and 1 not in k)
    in_keys = sorted(k for k in creators if 0 in k or 1 in k)
    psi_out = fx_product(creators, out_keys, vac)
    psi = fx_product(creators, in_keys, psi_out)
    must(psi == fx_product(creators, list(reversed(in_keys + out_keys)), vac), 'creators commute (product order)')
    w_vec = {(1, 1): Q(3, 10), (2, 1): Q(2, 5)}
    wmatrix = {}
    for k, a in w_vec.items():
        wmatrix[((0, 0), k)] = a
        wmatrix[(k, (0, 0))] = a
    wmatrix[((1, 0), (0, 1))] = wmatrix[((0, 1), (1, 0))] = Q(1, 3)
    wmatrix[((1, 1), (1, 1))] = Q(1, 5)
    wmatrix[((2, 2), (1, 0))] = wmatrix[((1, 0), (2, 2))] = Q(-1, 7)
    rows = {}
    for (l, m), a in wmatrix.items():
        rows[l] = rows.get(l, Q(0)) + abs(a)
    w_opnorm_up = max(rows.values())
    must(sum(a * a for a in w_vec.values()) == Q(1, 4), 'fixture ||W Omega_R||=1/2')
    delta = fx_sub(psi, psi_out)
    must(all(st[0] != 0 or st[1] != 0 for st in delta), '(P_R x 1) delta = 0')
    n2 = fx_ip(psi_out, psi_out)
    e2 = fx_ip(delta, delta) / n2
    omega_direct = fx_ip(psi, fx_act_R(wmatrix, psi)) / fx_ip(psi, psi)
    wpsi_out = fx_act_R(wmatrix, psi_out)
    X = 2 * fx_ip(wpsi_out, delta) / n2
    Y = fx_ip(delta, fx_act_R(wmatrix, delta)) / n2
    parts = {k: -2 * fx_ip(wpsi_out, fx_apply(k, creators[k], psi_out)) / n2 for k in in_keys}
    X_R = -2 * sum(a * creators[(0, 1)].get(k, 0) for k, a in w_vec.items())
    pair_keys = [(i, j) for i in in_keys for j in in_keys if 0 in i and 1 not in i and 1 in j and 0 not in j and not set(i) & set(j)]
    X_pair = sum((2 * fx_ip(wpsi_out, fx_apply(i, creators[i], fx_apply(j, creators[j], psi_out))) / n2 for i, j in pair_keys), Q(0))
    single = [k for k in in_keys if not (0 in k and 1 in k)]
    norms = {k: fx_norm_bounds(v) for k, v in creators.items()}

    def anchored_lo(site, keys):
        return sum((norms[k][0] for k in keys if site in k), Q(0))

    t_o1_lo = anchored_lo(2, out_keys)
    t_o2_lo = anchored_lo(3, out_keys)
    s0_lo = sum((norms[k][0] for k in in_keys if 0 in k and 1 not in k), Q(0))
    sz_lo = sum((norms[k][0] for k in in_keys if 1 in k and 0 not in k), Q(0))
    s0_up = sum((norms[k][1] for k in in_keys if 0 in k and 1 not in k), Q(0))
    sz_up = sum((norms[k][1] for k in in_keys if 1 in k and 0 not in k), Q(0))
    eps_lo = sum((norms[k][0] for k in in_keys), Q(0))
    q_o1 = {st: v for st, v in psi_out.items() if st[2] != 0}
    q_o2 = {st: v for st, v in psi_out.items() if st[3] != 0}
    strad_bound_lo = 2 * HALF * t_o1_lo * norms[(0, 1, 2)][0]
    fixture_ok = (omega_direct == (X + Y) / (1 + e2) and X == sum(parts.values()) + X_pair and parts[(0, 1)] == X_R
                  and all(parts[k] == 0 for k in single) and parts[(0, 1, 2)] != 0 and X != X_R
                  and parts[(0, 1, 2)] ** 2 <= strad_bound_lo ** 2
                  and X_pair ** 2 <= (2 * HALF * s0_lo * sz_lo) ** 2
                  and abs(Y) <= w_opnorm_up * e2
                  and e2 <= eps_lo ** 2
                  and fx_ip(q_o1, q_o1) <= t_o1_lo ** 2 * n2 and fx_ip(q_o2, q_o2) <= t_o2_lo ** 2 * n2)
    record('creation_fixture_decomposition_identity_and_bounds', fixture_ok,
           label='finite creation-algebra fixture (sites 0,e_z,o1,o2; dims 3,3,2,2); audits the K_2 algebra, not a rotor truncation',
           model_is_finite_graph=True, transfers_to_aq=False, graph_name='four_site_creation_algebra',
           omega=qs(omega_direct), X=qs(X), Y=qs(Y), e2=qs(e2), X_R_leading=qs(X_R), X_straddling=qs(parts[(0, 1, 2)]),
           X_pair=qs(X_pair), single_site_linear_parts=[qs(parts[k]) for k in single],
           identity='omega=(X+Y)/(1+e^2), X=-2<w,c_R>+straddling+pairs, single-R-site creators contribute exactly 0',
           outside_excitation_lemma='||(Q_x x 1) phi_out|| <= t_x ||phi_out|| checked at o1 and o2')

    # ---------------------------------------------- I. feasibility, AW2 rule, AV1 compatibility (item 5, 6)
    feasible = admit_bound(K2 * cap, target)
    margin = derived_coefficient / (K2 * cap)          # (tau/144)/(K_2^+ tau^2) = 1/(144 K_2^+ tau)
    tau_aw2 = aw2_rule(K2, aw2['grid_start_exp'], aw2['threshold'])
    crude_feasible = cr['K2'] * cap <= target
    crude_rule_info = aw2_rule(cr['K2'], aw2['grid_start_exp'], aw2['threshold'])
    av1_gate = json.loads((INPUTS / AV1_GATE_REL).read_text())
    dm = re.search(r'D_ii=(\d+)/(\d+) \(certified by both inequalities\) as the admitted state bound', av1_gate['decision'])
    must(dm is not None, 'AV1 admitted D not found')
    D_av1 = Q(int(dm.group(1)), int(dm.group(2)))
    av1_compatible = D_av1 >= cap * derived_coefficient + K2 * cap * cap
    record('feasibility_and_frozen_aw2_rule', feasible and margin >= 2 and tau_aw2 == cap and not crude_feasible and av1_compatible,
           target_read_from_contract=qs(target), K2_times_tau_at_cap=qs(K2 * cap), K2_times_tau_preview=sci(K2 * cap),
           margin_against_1_288=sci(target / (K2 * cap)), sign_margin_1_over_144K2tau=sci(margin),
           tau_AW2=qs(tau_aw2), rule=params['aw2_coupling_rule'],
           crude_tier={'K2_times_tau': sci(cr['K2'] * cap), 'feasible_at_cap': crude_feasible,
                       'rule_value_informational_only': qs(crude_rule_info)},
           conservative_multiplier_4={'K2_times_tau': sci(cons['K2'] * cap), 'feasible_at_cap': cons['K2'] * cap <= target},
           av1_D_ii=qs(D_av1), av1_compatibility='D_ii >= |tau|/144 + K_2^+ tau^2 at the cap',
           no_enclosure='no enclosure or sign of omega(W) is admitted here; AW2 instantiates it')

    # =================================================== the 30 contract controls
    control('missing_incoming_stars', [
        ('outgoing_star_face_count', certified_count, (DerivedCount(len(classes), 'outgoing_star_only'), 'faces per factor')),
        ('two_anchor_cover_sum', certified_count, (DerivedCount(2 * len(classes), 'outgoing_star_only'), 'faces meeting R')),
        ('anchors_0_and_e_z_only', certify_anchor_set, ([ORIGIN, EZ],)),
    ], complete_faces_per_factor=derived['faces_per_factor'], outgoing_only=len(classes))
    control('full_original_wilson_cover', [
        ('cover_origin_only', certify_cover, ((ORIGIN,),)),
        ('cover_with_extra_factor', certify_cover, ((ORIGIN, EZ, (0, 0, -1)),)),
    ], cover=[list(c) for c in COVER], W_link_owners=sorted({str(coarse(t)) for t, _ in W_FACE}))
    control('wrong_delta_alpha_hbar_clock', [
        ('alpha_coupling_over_delta_energy', first_order_amplitude, ('alpha', 'delta')),
        ('delta_coupling_over_alpha_energy', first_order_amplitude, ('delta', 'alpha')),
        ('exponent_24_with_alpha_clock', certify_clock_exponent, (24, 'alpha')),
        ('exponent_3_with_delta_clock', certify_clock_exponent, (3, 'delta')),
    ], amplitude_both_units=qs(amp), mixed_coefficients=[qs(2 * HAAR_W2 * Q(1, 24) / FACE_ENERGY), qs(2 * HAAR_W2 * Q(1, 3) / FACE_ENERGY_ALPHA)],
        note='static coefficient tau/144 is independent of alpha, hbar, E_star; C(s) uses exp(-3s), s=alpha t_E/hbar')
    control('vector_versus_scalar_centering', [
        ('scalar_subtraction_as_vector', certify_centering_identity, ('scalar', -2 * Q(1, 4) * Q(1, 100) - Q(1, 100) ** 2)),
        ('negative_vector_residue', certify_centering_identity, ('vector', -Q(1, 10000))),
    ], exact_control={'vector': qs(Q(1, 100) ** 2), 'scalar': qs(-2 * Q(1, 4) * Q(1, 100) - Q(1, 100) ** 2), 'uncentered_residue': qs(Q(1, 16))})
    control('first_order_mean_charged', [
        ('zero_first_order_mean', certify_mean_first_order, (Q(0),)),
        ('uncentered_equals_centered_at_tau2', certify_uncentered_equals_centered_to_second_order, (derived_coefficient ** 2,)),
        ('variance_without_mean_square', certify_variance_lower, (Q(1, 4) - K2 * cap * cap, cap / 144, Q(1, 4) - K2 * cap * cap)),
    ], mean_square_second_order_coefficient=qs(derived_coefficient ** 2))
    B_lin_hi = led[('exact', qs(cap))]['B']
    lin_ratio = (cap * derived_coefficient) / ((cap / 10) * derived_coefficient)
    d_av1 = lambda t: (lambda T: (lambda e: 2 * e * (1 + e) / (1 + e * e))(2 * T + T * T))(Q(49, 144) * abs(t) / (1 - 352 * 28 * abs(t)))
    av1_ratio = d_av1(cap) / d_av1(cap / 10)
    control('tau_scaling_exponent', [
        ('linear_av1_bound_as_tau2_remainder', certify_quadratic_scaling, (av1_ratio, av1_ratio, 'AV1 D relabelled')),
        ('first_order_term_as_remainder', certify_quadratic_scaling, (lin_ratio, lin_ratio, 'first-order term')),
        ('cubic_claim', certify_remainder_order_claim, (3, 'scaling fit')),
    ], exact_ratio=sci(ratio), linear_ratio=qs(lin_ratio), av1_ratio=sci(av1_ratio))
    control('changed_model_relabelled', [
        ('nonzero_selected_triple', certify_model, (cap, ('0', '1/100', '0'))),
        ('coupling_above_cap', certify_model, (cap * 10,)),
        ('finite_graph_fixture_as_model', certify_model_id, ('finite_graph_one_plaquette', 'AQ1_centered_whole_star_subsequence')),
        ('finite_volume_provenance', certify_model_id, ('AQ_patterned_zero_selected', 'finite_box_Lambda_2')),
    ])
    base = json.loads(raw)

    def coherent(mut):
        doc = json.loads(json.dumps(base))
        mut(doc)
        blob = json.dumps(doc, indent=2).encode()
        return blob, hashlib.sha256(blob).hexdigest()

    tampers = []
    for label, mut in (
            ('target_relaxed_to_1_144', lambda d: d['preregistration']['target'].__setitem__('value', '1/144')),
            ('flip_set_z_part_changed', lambda d: d['parameters'].__setitem__('flip_set', 'E={(p,x): p_y even} u {(p,y): p_z even} u {(p,z): p_z even}')),
            ('candidate_tau_over_72', lambda d: d['parameters'].__setitem__('first_order_candidate', 'omega_tau(W)=+tau/72+r(tau) in alpha units under I1.5 (to be derived, not assumed)')),
            ('aw2_threshold_1_144', lambda d: d['parameters'].__setitem__('aw2_coupling_rule', d['parameters']['aw2_coupling_rule'].replace('<= 1/288', '<= 1/144'))),
            ('tau_cap_1e-7', lambda d: d['parameters'].__setitem__('tau_cap', '1/10000000')),
            ('reference_second_moment_1_3', lambda d: d['preregistration']['observable'].__setitem__('reference_value_exact', '0 and 1/3')),
            ('error_term_removed', lambda d: d['preregistration']['error_terms_itemized'].pop()),
            ('control_removed', lambda d: d['controls'].pop())):
        blob, digest = coherent(mut)
        tampers.append((label, validate_contract_bytes, (blob, digest, am2_cap, derived_coefficient)))
    tampers.append(('byte_change_without_rehash', validate_contract_bytes, (raw + b' ', CONTRACT_SHA256, am2_cap, derived_coefficient)))
    control('coherent_evidence_tampering', tampers, note='each tampered copy is rehashed coherently; semantic re-derivation still rejects it')
    good = dict(parity_complete=True, coefficient_exact=True, flip_finite_volume=True, flip_aq_set_level=True,
                k2_exact_tier=True, k2_uniform_in_N=True, rule_evaluated=True, sign_margin=margin)
    crude_only = dict(good, k2_exact_tier=False)
    parity_fail = dict(good, parity_complete=False)
    coeff_fail = dict(good, coefficient_exact=False)
    fv_only = dict(good, flip_aq_set_level=False)
    must(producer_outcome(**crude_only) == 'limited' and producer_outcome(**parity_fail) == 'insufficient'
         and producer_outcome(**coeff_fail) == 'insufficient' and producer_outcome(**fv_only) == 'limited', 'retained outcomes')
    outcome = certify_outcome(producer_outcome(**good), good)
    control('insufficient_verdict_retained', [
        ('crude_only_relabelled_accepted', certify_outcome, ('accepted_within_scope', crude_only)),
        ('parity_failure_relabelled_limited', certify_outcome, ('limited', parity_fail)),
        ('coefficient_failure_relabelled_limited', certify_outcome, ('limited', coeff_fail)),
        ('finite_volume_flip_relabelled_accepted', certify_outcome, ('accepted_within_scope', fv_only)),
    ], crude_tier_feasible=crude_feasible, crude_tier_retained='limited-tier value, fails 1/288 at the cap')
    control('exact_arithmetic_admission', [
        ('float_tau', remainder_ledger, (1e-08,)),
        ('bool_tau', certify_model, (True,)),
        ('nan_string', parse_q, ('NaN',)),
        ('float_bound_admission', admit_bound, (float(K2 * cap), target)),
        ('zero_denominator', parse_q, ('1/0',)),
    ], note='every Boolean is decided on Fraction (or exact Q(sqrt D)) values; no numerical-library import')
    l1_lower = Q(0)
    by_owner_R = {}
    for key, (lk, owners) in meeting.items():
        by_owner_R[owners] = by_owner_R.get(owners, 0) + 1
    for n in by_owner_R.values():
        l1_lower += sqrt_bounds(n)[0]
    control('root_n_misuse', [
        ('sqrt_82_for_R_sum', certify_first_order_R_sum, (sqrt_bounds(derived['faces_meeting_R'])[1], l1_lower)),
        ('rss_ledger_assembly', certify_assembly, ('root_sum_square',)),
    ], exact_l1_over_owner_sets_lower=sci(l1_lower), owner_sets_meeting_R=len(by_owner_R))
    flags_ok = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
                'scientific_priority_verified': False, 'third_order_remainder_claim': False,
                'first_order_parity_claim': True, 'flip_lemma_claim': True}
    must(validate_claim_flags(flags_ok, True, True), 'claim flags')
    control('no_priority_or_continuum_claim', [
        ('continuum_true', validate_claim_flags, (dict(flags_ok, continuum_claim=True), True, True)),
        ('priority_true', validate_claim_flags, (dict(flags_ok, scientific_priority_verified=True), True, True)),
        ('uniform_wilson_true', validate_claim_flags, (dict(flags_ok, uniform_wilson_claim=True), True, True)),
        ('resolved_shift_true', validate_claim_flags, (dict(flags_ok, resolved_interaction_shift=True), True, True)),
    ])
    control('haar_parity_exact', [
        ('E_W3_one_eighth', certify_haar_moments, ({3: Q(1, 8)},)),
        ('E_W4_as_E_W2_squared', certify_haar_moments, ({4: HAAR_W2 ** 2},)),
        ('E_W2_one_half', certify_haar_moments, ({2: HALF},)),
        ('float_moment', certify_haar_moments, ({2: 0.25},)),
    ], moments={str(n): qs(v) for n, v in moments.items() if n <= 4})
    control('first_order_shift_of_C_vanishes', [
        ('state_term_with_W_instead_of_W2', certify_first_order_terms, (dict(terms_C, state=2 * amp * HAAR_W2),)),
        ('duhamel_f_equals_W_counted', certify_first_order_terms, (dict(terms_C, duhamel=-v_per_tau * HAAR_W4),)),
        ('static_mean_as_C_shift', certify_first_order_terms, (dict(terms_C, energy=derived_coefficient),)),
        ('missing_itemization', certify_first_order_terms, ({'state': Q(0), 'duhamel': Q(0)},)),
    ], computed={k: qs(v) for k, v in terms_C.items()})
    control('degenerate_multiplet_first_order', [
        ('identity_component_as_multiplet', certify_multiplet_component, (0, 0)),
        ('one_shared_link_component', certify_multiplet_component, (6, 36)),
        ('spin_one_component', certify_multiplet_component, (0, 64)),
    ], odd_set_sizes={str(k): v for k, v in sorted(sizes.items())})
    control('wilson_mean_first_order_coefficient', [
        ('norm_one_instead_of_half', certify_first_order_coefficient, (2 * amp,)),
        ('missing_two_re', certify_first_order_coefficient, (amp * HAAR_W2,)),
        ('am2_sign_literal', certify_first_order_coefficient, (2 * c1 * HAAR_W2,)),
        ('mixed_units_1152', certify_first_order_coefficient, (Q(1, 1152),)),
        ('mixed_units_18', certify_first_order_coefficient, (Q(1, 18),)),
        ('all_ten_R_faces', certify_first_order_coefficient, (10 * derived_coefficient,)),
    ], derived=qs(derived_coefficient))
    other_R = [meeting[k][0] for k in inside if meeting[k][0] != W_FACE]
    control('wrong_face_control', [
        ('yz_face_in_R_contributes', certify_pairing, (W_FACE, other_R[0], HAAR_W2)),
        ('straddling_face_contributes', certify_pairing, (W_FACE, meeting[strict[0]][0], HAAR_W2)),
        ('W_self_pairing_dropped', certify_pairing, (W_FACE, W_FACE, Q(0))),
    ], faces_checked=len(pair_rows), nonzero_pairings=sum(1 for v in pair_rows if v != 0))
    fx_plus = two_level_ground_mean(FACE_COUPLING_PER_TAU['alpha'] * cap * HALF)[1]
    fx_minus = two_level_ground_mean(FACE_COUPLING_PER_TAU['alpha'] * (-cap) * HALF)[1]
    must(fx_plus.sign() == 1 and fx_minus.sign() == -1 and certify_tau_odd(fx_plus, fx_minus, 'one-plaquette fixture'),
         'signed fixture values flip under tau -> -tau')
    control('sign_flip_tau', [
        ('sign_blind_minus_tau', certify_signed_first_order, (-cap, derived_coefficient * cap)),
        ('sign_blind_fixture', certify_sign, (-cap, fx_plus.bounds()[0])),
        ('fixture_minus_tau_as_plus_value', certify_tau_odd, (fx_plus, fx_plus, 'one-plaquette fixture read sign-blind')),
    ], signed_values=signed, fixture_signs={'plus_tau': fx_plus.sign(), 'minus_tau': fx_minus.sign()},
        fixture_values={'plus_tau': fx_plus.text(), 'minus_tau': fx_minus.text()})
    control('second_order_remainder_itemized', [
        ('straddling_dropped', assemble_remainder, ('exact', {k: v for k, v in ex['terms'].items() if k != 'straddling'})),
        ('zero_am2_remainder', assemble_remainder, ('exact', dict(ex['terms'], am2_remainder=Term('am2_remainder', 0, 'exact', 'self_consistent_352JT')))),
        ('density_unpinned', assemble_remainder, ('exact', dict(ex['terms'], density=Term('density', ex['terms']['density'].value, 'exact', 'guess')))),
        ('normalization_dropped', assemble_remainder, ('exact', {k: v for k, v in ex['terms'].items() if k != 'normalization'})),
    ], ledger_names=list(EXPECTED_ERROR_TERMS), normalization_order=3, arithmetic='exact rationals; K_2^+ also given as a 10^-40 ceiling')
    control('static_not_dynamic_effect', [
        ('dynamical_shift_label', certify_effect_label, ('dynamical_shift',)),
        ('mass_gap_correction_label', certify_effect_label, ('mass_gap_correction',)),
        ('C_first_order_shift_label', certify_effect_label, ('C(s)_first_order_shift',)),
    ], evidence='first-order C(s) coefficient 0 while omega(W) coefficient 1/144: a static equal-time ground mean')
    control('wilson_overlap_single_component', [
        ('factor_4_unlabelled', certify_overlap_multiplier, (4, 'unlabelled')),
        ('multiplier_half', certify_overlap_multiplier, (HALF, 'exact_single_component')),
        ('factor_2_as_conservative', certify_overlap_multiplier, (2, 'conservative_labelled')),
    ], W_Omega_R_norm=qs(W_OMEGA_NORM), exact_multiplier=qs(2 * W_OMEGA_NORM),
        fixture_single_site_parts=[qs(parts[k]) for k in single])
    vpm, mean_fix = two_level_ground_mean(FACE_COUPLING_PER_TAU['alpha'] * cap * HALF)
    must(certify_sign(cap, (mean_fix.bounds()[0] + mean_fix.bounds()[1]) / 2) and mean_fix.sign() == 1, 'fixture sign')
    control('sign_convention_fixture', [
        ('contract_formula_with_am2_c1', certify_sign, (cap, 2 * c1 * HAAR_W2 * cap)),
        ('plus_sign_coupling', certify_sign, (cap, two_level_ground_mean(-FACE_COUPLING_PER_TAU['alpha'] * cap * HALF)[1].bounds()[1])),
    ], fixture='one plaquette (finite graph), I1.5 coupling -(tau/24)W, j<=1/2 exact: <W>(tau) has the sign of tau',
        model_is_finite_graph=True, transfers_to_aq=False, graph_name='one_plaquette_character_truncation',
        fixture_mean_bounds=[qs(v) for v in mean_fix.bounds()])
    rule_d = {'grid_start_exp': aw2['grid_start_exp'], 'threshold': aw2['threshold']}
    must(certify_tau_aw2(tau_aw2, K2, rule_d) == cap, 'frozen AW2 rule')
    control('aw2_coupling_rule_prefrozen', [
        ('not_largest_1e-9', certify_tau_aw2, (cap / 10, K2, rule_d)),
        ('crude_constant_choice', certify_tau_aw2, (crude_rule_info, K2, rule_d)),
        ('off_grid_2e-8', certify_tau_aw2, (2 * cap, K2, rule_d)),
        ('threshold_1_144', certify_tau_aw2, (cap / 10, K2 * 25, {'grid_start_exp': 8, 'threshold': Q(1, 144)})),
    ], tau_AW2=qs(tau_aw2))
    minus_one = lambda l: in_flip(contract_rule, l) and l != ((0, 0, 0), 0)
    star_v = lambda l: l[0] == (0, 0, 0) or vadd(l[0], DIRS[l[1]]) == (0, 0, 0)
    local = plaquettes_in_box((-2, -2, -2), (2, 2, 2))
    even_after = sum(1 for f in local if sum(1 for l in f if minus_one(l)) % 2 == 0)
    control('flip_set_odd_intersection', [
        ('E_minus_one_link', certify_flip_set, (minus_one, local, 'E minus ((0,0,0),x)')),
        ('vertex_star_coboundary', certify_flip_set, (star_v, local, 'vertex-star coboundary')),
        ('x_part_only', certify_flip_set, (lambda l: l[1] == 0 and l[0][1] % 2 == 0, local, 'x part of E')),
        ('odd_periodic_side', certify_flip_set, (lambda l: in_flip(contract_rule, l), periodic_plaquettes((4, 3, 4)), 'E on a periodic box with odd y side')),
        ('spin_one_term_W_squared_flips', certify_flip_sign, (list(W_FACE) * 2, contract_rule, -1)),
    ], plaquettes_even_after_removing_one_link=even_after,
        boundary_convention='open centered whole-star boxes (no periodic identification, no frozen or gauge-fixed links)')
    control('flip_breaks_at_nonzero_kappa', [
        ('antisymmetry_claim_kappa_L', certify_tau_antisymmetry_claim, ((Q(1, 7), 0, 0), 'U_E')),
        ('antisymmetry_claim_kappa_M', certify_tau_antisymmetry_claim, ((0, Q(-1, 9), 0), 'U_E')),
        ('image_kappa_preserved', certify_hamiltonian_image, (conjk, h_mk)),
    ], statement='U_E H(tau,kappa) U_E^*=H(-tau,-kappa) != H(-tau,kappa) for kappa!=0')
    control('flip_no_third_order_claim', [
        ('cubic_from_oddness', certify_remainder_order_claim, (3, 'oddness')),
        ('cubic_from_flip_lemma', certify_remainder_order_claim, (3, 'flip lemma')),
    ], counterexample={'r(tau)': 'K tau|tau| is odd and |r(+-cap)|=K cap^2 exactly',
                       'values': [qs(K2 * t * abs(t)) for t in taus]})
    t1_face = derived_coefficient * cap
    mixed = dict(ex['terms'], am2_remainder=cr['terms']['am2_remainder'])
    control('tier_mixing_rejected', [
        ('exact_counts_crude_remainder', assemble_remainder, ('exact', mixed)),
        ('crude_ledger_with_exact_density', assemble_remainder, ('crude', dict(cr['terms'], density=ex['terms']['density']))),
        ('t1_without_self_consistency', assemble_remainder, ('exact', dict(ex['terms'], am2_remainder=Term('am2_remainder', GP_R_UP * J_PER_TAU * cap * 49 * t1_face, 'exact', 't1_direct')))),
    ])
    inventory = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    must(validate_inventory(inventory, contract), 'reverse inputs inventory')
    control('reverse_premise_isolation', [
        ('skeptic_triage_added', validate_inventory, (inventory + ['research/round32/skeptic/triage.md'], contract)),
        ('loop2_response_added', validate_inventory, (inventory + ['research/round32/experts/modern/loop2-response.md'], contract)),
        ('deliberation_added', validate_inventory, (inventory + ['research/round32/advisor/deliberation-3.md'], contract)),
        ('forward_aw1_added', validate_inventory, (inventory + ['research/round32/forward/aw1/report.md'], contract)),
        ('premise_missing', validate_inventory, (inventory[1:], contract)),
    ], inventory_size=len(inventory))
    control('wilson_face_separated', [
        ('W_excluded_from_omitted_set', certify_wilson_split, (20, False, 0, Q(0))),
        ('W_merged_with_R_faces', certify_wilson_split, (21, True, 10, 10 * derived_coefficient)),
        ('W_counted_twice', certify_wilson_split, (21, True, 2, 2 * derived_coefficient)),
    ], split={'W': 1, 'others_anchored_at_0': derived['other_classes_anchored_at_0'], 'others_split': split20})
    # positive nonzero-kappa demonstration: two one-plaquette systems (omitted f with tau, selected g with kappa)
    kap = Q(1, 7)
    hf = lambda t: madd([row[:2] for row in g0[:2]], mscale(FACE_COUPLING_PER_TAU['alpha'] * t, [row[:2] for row in wmat[:2]]))
    hg = lambda k: madd([row[:2] for row in g0[:2]], mscale(-k, [row[:2] for row in wmat[:2]]))
    I2 = eye(2)
    H2 = lambda t, k: madd(kron(hf(t), I2), kron(I2, hg(k)))
    F2 = kron(diag([1, -1]), diag([1, -1]))
    img = matmul(matmul(F2, H2(cap, kap)), F2)
    # H2[0][1] is the off-diagonal entry of the g-block (index order f (x) g); the ground is the product of block grounds
    _, mg_pp = two_level_ground_mean(H2(cap, kap)[0][1])
    _, mg_mm = two_level_ground_mean(H2(-cap, -kap)[0][1])
    _, mg_mk = two_level_ground_mean(H2(-cap, kap)[0][1])
    must(matmul(matmul(F2, H2(-cap, kap)), F2) == H2(cap, -kap), 'fixture block structure')
    must(certify_tau_odd(mg_pp, mg_mm, 'U_E image (tau,kappa)->(-tau,-kappa)'), 'selected mean flips under U_E')
    rs_g, _, _ = rs_series([Q(0), Q(3)], mscale(-1, [row[:2] for row in wmat[:2]]), [row[:2] for row in wmat[:2]], 2)
    demo_ok = img == H2(-cap, -kap) and img != H2(-cap, kap) and mg_pp.key() == (-mg_mm).key() and mg_pp.sign() == 1 \
        and rs_g[1] == Q(1, 6) and conjk == h_mm
    must(demo_ok, 'nonzero-kappa positive demonstration')
    control('flip_nonzero_kappa_positive_demonstration', [
        ('claim_image_is_H_minus_tau_kappa', certify_hamiltonian_image, (img, H2(-cap, kap))),
        ('claim_selected_mean_tau_odd_at_fixed_kappa', certify_tau_odd, (mg_pp, mg_mk, '<W_g>(tau,kappa) vs <W_g>(-tau,kappa)')),
    ], model_is_finite_graph=True, transfers_to_aq=False, graph_name='two_plaquette_omitted_plus_selected',
        demonstration={'fixture': 'finite graph: omitted plaquette f (tau) and selected plaquette g (kappa=1/7), j<=1/2 each',
                      'U_E_image': 'H(-tau,-kappa) exactly (4x4 exact matrices)',
                      '<W_g>(tau,kappa)': mg_pp.text(), '<W_g>(-tau,-kappa)': mg_mm.text(),
                      '<W_g>(-tau,kappa)': mg_mk.text() + ' (unchanged: not tau-odd)',
                      'first_order_coefficient_of_<W_g>_in_kappa': qs(rs_g[1]),
                      'lattice': 'Lambda_2 symbolic conjugation: selected coefficients -8 kappa_r map to +8 kappa_r'})

    ids = [c['id'] for c in CHECKS]
    missing = [c for c in contract['controls'] if c not in ids]
    must(missing == [], 'contract controls without a check: ' + ','.join(missing))

    flags = dict(flags_ok)
    result = {
        'loop': 'AW1', 'direction': 'reverse', 'route': 'reverse reconstruction from the desired first-order and parity conclusions',
        'human_author': 'Hruday N M (BUNZEEY)',
        'contribution_alias': 'HNM-AW1-R reverse parity/flip/first-order/K_2 package',
        'attribution': {
            'peter_weyl_clebsch_gordan': 'standard SU(2) representation theory (trivial multiplicity in (1/2)^{(x)n}, Weyl integration)',
            'center_flip': 'Z_2 center grading and center-flip symmetries are a known kind of argument; no priority claimed',
            'creation_expansion': 'AM2 commuting-creation expansion (Bravyi-DiVincenzo-Loss 2008 lineage as credited in AM2; Gauvin arXiv:2503.15539v3 A.6-A.8 template)',
            'scientific_priority': 'unverified'},
        'contract_snapshot_sha256': contract_sha, 'check_py_sha256': check_py_sha,
        'model': contract['model'],
        'target': {'quantity': 'K_2^+ tau at the cap', 'value': qs(target), 'comparator': '<=', 'read_from': 'contract preregistration.target'},
        'reference_values': {k: qs(v) for k, v in reference.items()},
        'first_order_coefficient': {'value': qs(derived_coefficient), 'sign': 'sign(tau)',
                                    'signed_terms_at_cap': signed},
        'K2_plus_exact_tier': {'exact_rational': qs(K2), 'ceiling_1e-40': qs(K2_up), 'preview': sci(K2)},
        'K2_plus_crude_tier': {'exact_rational': qs(cr['K2']), 'ceiling_1e-40': qs(ceil_to(cr['K2'])), 'preview': sci(cr['K2'])},
        'K2_plus_conservative_multiplier_4': {'exact_rational': qs(cons['K2']), 'preview': sci(cons['K2'])},
        'K2_directed_G_variant': {'exact_rational': qs(dirg['K2']), 'preview': sci(dirg['K2'])},
        'K_omega_W2_supplementary': {'exact_rational': qs(w2 / (cap * cap)), 'preview': sci(w2 / (cap * cap))},
        'ledgers': {'exact_plus': ledger_json(ex), 'exact_minus': ledger_json(led[('exact', qs(-cap))]),
                    'crude_plus': ledger_json(cr), 'crude_minus': ledger_json(led[('crude', qs(-cap))])},
        'error_terms_itemized': {
            'am2_remainder': 'rho=352 J T, T=t_1/(1-352J), t_1=49|tau|/144 (exact tier); 352 J t_crude (crude tier)',
            'two_creation': '2||W Omega_R|| s_0 s_z, s_0=s_z=33|tau|/144+rho (exact); t_crude^2 (crude)',
            'straddling': '2||W Omega_R|| T (6|tau|/144+rho): the 6 of the 72 straddling faces that strictly contain R pair with outside excitations of phi_out (||(Q_x x 1)phi_out||<=t||phi_out||); the other 66 enter only the two-creation and density terms',
            'density': '||W|| e^2 <= eps^2, eps=82|tau|/144+2 rho+s_0 s_z (exact); (2t+t^2)^2 (crude)',
            'normalization_order': 'third order: (e+e^2)e^2',
            'overlap_multiplier': '2||W Omega_R||=1 (only c_R overlaps W Omega_R); factor 4 only as the labelled conservative variant',
            'arithmetic': 'all exact rationals; ceiling to 10^-40 recorded'},
        'feasibility': {'K2_times_tau_at_cap': qs(K2 * cap), 'target': qs(target), 'feasible': feasible,
                        'sign_margin': sci(margin), 'tau_AW2': qs(tau_aw2)},
        'face_enumeration': {'derived': derived, 'owner_set_multiplicity_histogram': {str(k): v for k, v in sorted(mult_hist.items())},
                             'other_20_split': split20, 'boxes': box_info},
        'flip_set': {'contract_text': params['flip_set'], 'rule': {'xyz'[d]: 'xyz'[c] for d, c in sorted(contract_rule.items())},
                     'histogram_fine_box': {str(k): v for k, v in sorted(hist.items())}},
        'producer_outcome': outcome,
        'sub_label': 'static_not_dynamic',
        'outcome_note': 'proposed for review; admission requires the forward route, exchange and the skeptical review; '
                        'no enclosure or sign of omega(W) is admitted in AW1 (AW2)',
        'claim_exclusions': contract['claim_exclusions'],
        'checks': CHECKS,
    }
    result.update(flags)
    return result


def main():
    ap = argparse.ArgumentParser(description='HNM-AW1 reverse producer checker (exact arithmetic)')
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
    manifest = {'loop': 'AW1', 'direction': 'reverse', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AW1', 'direction': 'reverse', 'checks': len(result['checks']),
                      'K2_exact': result['K2_plus_exact_tier']['preview'], 'K2_crude': result['K2_plus_crude_tier']['preview'],
                      'tau_AW2': result['feasibility']['tau_AW2'], 'outcome': result['producer_outcome']}, sort_keys=True))


if __name__ == '__main__':
    main()
