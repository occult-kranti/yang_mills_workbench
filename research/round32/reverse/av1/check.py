#!/usr/bin/env python3
"""HNM-AV1 reverse producer: vacuum-overlap (fidelity) route to a volume-uniform
local state bound for the zero-selected AQ subfamily.

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production under
premise isolation; HNM labels are project aliases. Creation-operator expansions and
fidelity/trace-distance inequalities are established mathematics; scientific
priority is unverified.

Standard library only. Exact Fraction arithmetic decides every Boolean; decimal
strings are truncated previews. Every control is a damaging mutation whose
rejection is required; rejections and failures are explicit exceptions (never
assert), so the run and its output bytes are identical under python -O.

Usage: python3 -B research/round32/reverse/av1/check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUTS = HERE / 'inputs'
CONTRACT_REL = 'research/round32/contracts/av1.json'
AM2_GATE_REL = 'research/round29/advisor/am2-gate.json'
CONTRACT_SHA256 = 'c7018519188b953e48e56715a72c90491389e42243ef691cb59dc5b038e91e40'
DEN = 10 ** 40
FORBIDDEN_PREFIXES = (
    'research/round32/skeptic/',
    'research/round32/experts/',
    'research/round32/forward/',
    'research/round32/advisor/deliberation-',
)
CLAIM_FLAGS = {
    'continuum_claim': False,
    'uniform_wilson_claim': False,
    'resolved_interaction_shift': False,
    'scientific_priority_verified': False,
    'euclidean_node_certified': False,
    'first_order_parity_claim': False,
}


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


def rejection(function, *args, **kwargs):
    """Run one damaging mutation; return its rejection reason, abort if accepted."""
    try:
        function(*args, **kwargs)
    except Rejected as exc:
        return str(exc)
    raise ProducerError('damaging mutation accepted by ' + function.__name__)


def control(check_id, mutations, **details):
    """A control passes only if every listed mutation is rejected."""
    rejected = {}
    for label, function, args in mutations:
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
    exact = s * s * y.denominator == scaled
    hi = lo if exact else Q(s + 1, DEN)
    must(lo * lo <= y and y <= hi * hi, 'square-root enclosure failed')
    return lo, hi


def factorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


def binom(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))


def exp_bounds(x, terms=16):
    """Directed enclosure of exp(x) for 0<=x<=1/2: partial sum and geometric tail."""
    x = Q(x)
    must(Q(0) <= x and x <= Q(1, 2), 'exponential argument outside [0,1/2]')
    partial, power = Q(0), Q(1)
    for k in range(terms + 1):
        partial += power / factorial(k)
        power *= x
    tail = power / factorial(terms + 1) / (1 - x / (terms + 2))
    return floor_to(partial), ceil_to(partial + tail)


def atan_inverse_bounds(n, terms=40):
    s, prev = Q(0), Q(0)
    for k in range(terms + 1):
        prev = s
        s += Q((-1) ** k, (2 * k + 1) * n ** (2 * k + 1))
    return min(prev, s), max(prev, s)


def pi_bounds():
    a5 = atan_inverse_bounds(5)
    a239 = atan_inverse_bounds(239)
    return floor_to(16 * a5[0] - 4 * a239[1]), ceil_to(16 * a5[1] - 4 * a239[0])


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


# ------------------------------------------------ SU(2), units, face vectors
HALF = Q(1, 2)


def clebsch_gordan(j1, j2):
    spins, j = [], abs(j1 - j2)
    while j <= j1 + j2:
        spins.append(j)
        j += 1
    return spins


CASIMIR_HALF = HALF * (HALF + 1)                               # j(j+1)=3/4
HAAR_W = Q(clebsch_gordan(HALF, Q(0)).count(Q(0)), 2)          # E[chi_1/2]/2
HAAR_W2 = Q(clebsch_gordan(HALF, HALF).count(Q(0)), 4)         # E[chi_1/2^2]/4
ALPHA_OVER_DELTA = Q(8)                                        # delta=alpha/8
FACE_LINKS = 4
FACE_ENERGY = ALPHA_OVER_DELTA * FACE_LINKS * CASIMIR_HALF     # normalized (delta)
FACE_ENERGY_ALPHA = FACE_ENERGY / ALPHA_OVER_DELTA             # alpha units
FACE_NORM = HALF
OMITTED_PER_ANCHOR_NORM_UNIT = Q(1, 3)                         # |tau|/3 per face, I1.5
COUPLING_PER_TAU = {'delta': Q(1, 24) * ALPHA_OVER_DELTA, 'alpha': Q(1, 24)}
ENERGY_BY_UNITS = {'delta': FACE_ENERGY, 'alpha': FACE_ENERGY_ALPHA}


def per_face_coefficient(abs_tau, coupling_units, energy_units):
    """Norm of H_M^{-1} P_M phi_f Omega_0 for one omitted face (I1.5 convention)."""
    require(coupling_units in COUPLING_PER_TAU and energy_units in ENERGY_BY_UNITS, 'unknown units')
    require(coupling_units == energy_units,
            'mixed normalization: coupling in %s units divided by an energy in %s units' % (coupling_units, energy_units))
    return abs_tau * COUPLING_PER_TAU[coupling_units] * FACE_NORM / ENERGY_BY_UNITS[energy_units]


def certify_face_energy(value, units):
    require(units in ENERGY_BY_UNITS, 'unknown energy units')
    require(Q(value) == ENERGY_BY_UNITS[units],
            'face energy %s labelled %s units is the wrong clock/normalization (24 delta = 3 alpha)' % (qs(value), units))
    return Q(value)


# --------------------------------------------------------------- geometry
DIRS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIENTATIONS = (('xy', 0, 1), ('xz', 0, 2), ('yz', 1, 2))
STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
COVER = (ORIGIN, EZ)


def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def coarse(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    return ((p, a), (vadd(p, DIRS[a]), c), (vadd(p, DIRS[c]), a), (p, c))


def fine_face_classes():
    """Re-derive the 24 anchored face classes from pi and the link tails (I1.4)."""
    rows = []
    for r in range(4):
        for s in range(2):
            p = (r, s, 0)
            for name, a, c in ORIENTATIONS:
                owners = tuple(sorted({coarse(t) for t, _ in face_links(p, a, c)}))
                selected = name == 'xy' and s == 0 and r in (0, 1, 2)
                rows.append((name, r, s, owners, 'selected' if selected else 'omitted'))
    return sorted(rows)


# Explicit encoding of the I1 table (research/round21/forward/i1/report.md, section 3).
I1_TABLE = (
    ('xy', (0, 1, 2), (0,), 3, ((0, 0, 0),), 'selected'),
    ('xy', (0, 1, 2), (1,), 3, ((0, 0, 0), (0, 1, 0)), 'omitted'),
    ('xy', (3,), (0,), 1, ((0, 0, 0), (1, 0, 0)), 'omitted'),
    ('xy', (3,), (1,), 1, ((0, 0, 0), (1, 0, 0), (0, 1, 0)), 'omitted'),
    ('xz', (0, 1, 2), (0, 1), 6, ((0, 0, 0), (0, 0, 1)), 'omitted'),
    ('xz', (3,), (0, 1), 2, ((0, 0, 0), (1, 0, 0), (0, 0, 1)), 'omitted'),
    ('yz', (0, 1, 2, 3), (0,), 4, ((0, 0, 0), (0, 0, 1)), 'omitted'),
    ('yz', (0, 1, 2, 3), (1,), 4, ((0, 0, 0), (0, 1, 0), (0, 0, 1)), 'omitted'),
)


def expand_table(table):
    rows = []
    for name, rs, ss, count, support, role in table:
        require(count == len(rs) * len(ss), 'I1 table row count mismatch')
        for r in rs:
            for s in ss:
                rows.append((name, r, s, tuple(sorted(support)), role))
    return sorted(rows)


class DerivedCount:
    __slots__ = ('value', 'provenance')

    def __init__(self, value, provenance):
        self.value = value
        self.provenance = provenance


PROVENANCE = 'I1_table_translation_covariance_all_sites'


def certified_count(obj, what):
    require(isinstance(obj, DerivedCount) and obj.provenance == PROVENANCE,
            what + ': count is hard-coded, copied or not derived from the I1 table at every site')
    return obj.value


def owner_set(anchor, support):
    return tuple(sorted(vadd(anchor, w) for w in support))


def faces_touching(site, supports):
    """All omitted faces (anchor, class) owning a link of `site`: anchors site - v."""
    return sorted({(vsub(site, v), k) for k, sup in enumerate(supports) for v in sup})


def box_enumeration(lo, hi, supports):
    rng = range(lo, hi + 1)
    sites = [(x, y, z) for x in rng for y in rng for z in rng]
    siteset = set(sites)
    per_site = dict.fromkeys(sites, 0)
    stars_per_site = dict.fromkeys(sites, 0)
    owners = {}
    stars = []
    for b in sites:
        if all(vadd(b, v) in siteset for v in STAR):
            stars.append(b)
            for v in STAR:
                stars_per_site[vadd(b, v)] += 1
            for sup in supports:
                m = owner_set(b, sup)
                owners[m] = owners.get(m, 0) + 1
                for u in m:
                    per_site[u] += 1
    return sites, per_site, owners, stars, stars_per_site


def certify_site_scope(scope):
    require(scope == 'all_sites', 'anchored norm maximum restricted to %s; the fixed point needs every site' % scope)
    return scope


def certify_anchor_set(anchors, supports):
    expected = sorted({vsub(u, v) for u in COVER for v in STAR})
    require(sorted(anchors) == expected,
            'incident anchors %d differ from the complete R-S (%d); incoming stars missing' % (len(anchors), len(expected)))
    return anchors


def certify_t1_over_coefficient(value, exact_lower):
    require(Q(value) >= exact_lower,
            'claimed first-order anchored norm %s|tau|/144 is below the exact global value (>= %s|tau|/144)' % (sci(value, 8), sci(exact_lower, 8)))
    return Q(value)


def factor_links(b):
    links = []
    for r in range(4):
        for s in range(2):
            t = (4 * b[0] + r, 2 * b[1] + s, b[2])
            for d in range(3):
                links.append((t, d))
    return links


W_LINKS = (((0, 0, 0), 0), ((1, 0, 0), 2), ((0, 0, 1), 0), ((0, 0, 0), 2))


def certify_cover(cover):
    owners = {coarse(t) for t, _ in W_LINKS}
    require(owners <= set(cover), 'cover misses an owner of a link of the original xz Wilson loop')
    require(set(cover) == owners, 'cover is not the complete factor cover R={0,e_z} of W')
    return tuple(sorted(cover))


# ------------------------------------------------------------ AM2 constants
R_RADIUS = Q(1, 64)


def am2_enclosures():
    e_lo, e_hi = exp_bounds(8 * R_RADIUS)
    return {
        'exp_one_eighth': (e_lo, e_hi),
        'G': (16 * e_lo * (1 + 10 * R_RADIUS), 16 * e_hi * (1 + 10 * R_RADIUS)),
        'G_prime': (16 * e_lo * (18 + 80 * R_RADIUS), 16 * e_hi * (18 + 80 * R_RADIUS)),
    }


def validate_am2_constants(radius, j0, g_up, gp_up, cap, j_per_tau):
    enc = am2_enclosures()
    require(Q(radius) == R_RADIUS, 'anchored radius differs from the admitted AM2 radius 1/64')
    require(Q(j0) == j_per_tau * cap, 'J0 is not 28 times the admitted tau cap')
    require(Q(g_up) >= enc['G'][1], 'G(R) upper constant is not a certified upper bound')
    require(Q(gp_up) >= enc['G_prime'][1], "G'(R) upper constant is not a certified upper bound")
    require(Q(j0) * Q(g_up) < R_RADIUS, 'self-map J0 G(R) < R fails')
    require(2 * Q(j0) * Q(gp_up) < 1, 'excited-sector contraction 2 J0 G\'(R) < 1 fails')
    return True


def G_upper(t):
    _, e_hi = exp_bounds(ceil_to(8 * t))
    return 16 * e_hi * (1 + 10 * t)


# ------------------------------------------------------------ model / tiers
TAU_CAP = None
J_PER_TAU = None
G_R_UP = Q(148, 7)
GP_R_UP = Q(352)
COUNTS = {}


def certify_model(tau, selected=('0', '0', '0')):
    t = parse_q(tau)
    sel = tuple(parse_q(x) for x in selected)
    require(len(sel) == 3, 'selected triple must have three entries')
    require(all(x == 0 for x in sel),
            'nonzero selected triple: the Haar product is not the onsite ground (a changed model, not a relabelling)')
    require(abs(t) <= TAU_CAP, 'coupling outside the AM2/AQ cap: not certified here (not a gap failure)')
    return t


class Term:
    __slots__ = ('name', 'value', 'tier', 'provenance')

    def __init__(self, name, value, tier, provenance):
        self.name = name
        self.value = Q(value)
        self.tier = tier
        self.provenance = provenance


def assemble_epsilon(tier, terms):
    require(tier in ('i', 'ii'), 'unknown tier')
    for name, term in sorted(terms.items()):
        require(term.tier == tier, 'tier mixing: term %s is tier (%s) inside tier (%s)' % (name, term.tier, tier))
    if tier == 'i':
        require(sorted(terms) == ['t'], 'tier (i) uses only the crude anchored norm t')
        require(terms['t'].provenance in ('am2_majorant', 'am2_majorant_iterated'),
                'tier (i) t must come from the AM2 majorant')
        t = terms['t'].value
        return 2 * t + t * t
    require(sorted(terms) == ['T', 'a1', 'rho'], 'tier (ii) needs a1, rho and T')
    require(terms['a1'].provenance == 'exact_first_order', 'tier (ii) a1 must be the exact first-order collection')
    require(terms['T'].provenance == 'self_consistent',
            'tier (ii) t must come from the self-consistent inequality t<=t1/(1-352J)')
    require(terms['rho'].provenance == 'self_consistent_remainder',
            'tier (ii) remainder must be bounded with the self-consistent t')
    return terms['a1'].value + 2 * terms['rho'].value + terms['T'].value ** 2


def fidelity_bound(eps):
    """D(eps)=2 eps/sqrt(1+eps^2): (rational upper bound, rational lower bound)."""
    eps = Q(eps)
    if eps == 0:
        return Q(0), Q(0)
    lo, hi = sqrt_bounds(1 + eps * eps)
    return ceil_to(2 * eps / lo), floor_to(2 * eps / hi)


def tier_i(tau, iterate=0):
    t_signed = certify_model(tau)
    a = abs(t_signed)
    J = J_PER_TAU * a
    t = J * G_R_UP
    provenance = 'am2_majorant'
    steps = [qs(t)]
    for _ in range(iterate):
        new = ceil_to(J * G_upper(t))
        must(new <= t and t <= R_RADIUS, 'majorant iteration must decrease inside the radius')
        t = new
        provenance = 'am2_majorant_iterated'
        steps.append(qs(t))
    eps = assemble_epsilon('i', {'t': Term('t', t, 'i', provenance)})
    d_up, d_lo = fidelity_bound(eps)
    return {'tier': 'i', 'variant': 'iterated_%d' % iterate if iterate else 'crude_J0_G(R)',
            'tau': qs(t_signed), 'J_upper': qs(J), 't_upper': qs(t), 't_iterates': steps,
            'epsilon': qs(eps), 'D_upper': qs(d_up), 'D_formula_lower': qs(d_lo),
            'D_upper_preview': sci(d_up), 'epsilon_preview': sci(eps),
            '_D_up': d_up, '_D_lo': d_lo}


def tier_ii(tau, norm='per_face', remainder='contract_352'):
    t_signed = certify_model(tau)
    a = abs(t_signed)
    J = J_PER_TAU * a
    K = GP_R_UP * J
    require(K < 1, 'self-consistent factor 352J must be below one')
    coeff = per_face_coefficient(a, 'delta', 'delta')
    if norm == 'per_face':
        t1 = coeff * certified_count(COUNTS['faces_per_factor'], 'faces per factor')
        a1 = coeff * certified_count(COUNTS['faces_meeting_R'], 'faces meeting R')
    elif norm == 'owner_set_orthogonal':
        t1 = coeff * COUNTS['orth_site_sum_hi']
        a1 = coeff * COUNTS['orth_meeting_R_hi']
    else:
        raise Rejected('unknown tier (ii) norm evaluation')
    T = t1 / (1 - K)
    must(T <= R_RADIUS, 'self-consistent t must stay inside the AM2 ball')
    if remainder == 'contract_352':
        rho = K * T
    elif remainder == 'directed_G':
        rho = ceil_to(J * (G_upper(T) - 16))
    else:
        raise Rejected('unknown remainder form')
    must(a == 0 or rho > 0, 'the remainder bound is never zero at nonzero coupling')
    eps = assemble_epsilon('ii', {
        'a1': Term('a1', a1, 'ii', 'exact_first_order'),
        'rho': Term('rho', rho, 'ii', 'self_consistent_remainder'),
        'T': Term('T', T, 'ii', 'self_consistent'),
    })
    d_up, d_lo = fidelity_bound(eps)
    return {'tier': 'ii', 'variant': norm + '+' + remainder, 'tau': qs(t_signed),
            'J_upper': qs(J), 'factor_352J': qs(K), 'per_face_coefficient': qs(coeff),
            't1_first_order_anchored': qs(t1), 'T_self_consistent': qs(T),
            'remainder_anchored_upper': qs(rho), 'a1_first_order_meeting_R': qs(a1),
            'two_creation_term': qs(T * T), 'epsilon': qs(eps),
            'D_upper': qs(d_up), 'D_formula_lower': qs(d_lo),
            'D_upper_preview': sci(d_up), 'epsilon_preview': sci(eps),
            '_D_up': d_up, '_D_lo': d_lo}


def strip(d):
    return {k: v for k, v in d.items() if not k.startswith('_')}


def at4_bound(tau):
    a = abs(parse_q(tau))
    lo, hi = sqrt_bounds(49 * a / 3)
    return 2 * hi, 2 * lo


# ---------------------------------------------------------- qubit fixtures
def apply_creation(support, amp, vec):
    m = 0
    for i in support:
        m |= 1 << i
    out = [Q(0)] * len(vec)
    for s, v in enumerate(vec):
        if v != 0 and (s & m) == 0:
            out[s | m] += amp * v
    return out


def apply_sum(ops, vec):
    out = [Q(0)] * len(vec)
    for support, amp in ops:
        for s, w in enumerate(apply_creation(support, amp, vec)):
            if w != 0:
                out[s] += w
    return out


def fixture_ground(amps, n, order=None):
    vec = [Q(0)] * (1 << n)
    vec[0] = Q(1)
    for support in (order if order is not None else sorted(amps)):
        w = apply_creation(support, amps[support], vec)
        vec = [x - y for x, y in zip(vec, w)]
    return vec


def dot(u, v):
    return sum((x * y for x, y in zip(u, v)), Q(0))


def reduced_R(vec, n):
    rho = [[Q(0)] * 4 for _ in range(4)]
    for o in range(1 << (n - 2)):
        base = o << 2
        for r in range(4):
            vr = vec[base + r]
            if vr != 0:
                for rp in range(4):
                    rho[r][rp] += vr * vec[base + rp]
    return rho


def matmul(a, b):
    n = len(a)
    return [[sum((a[i][k] * b[k][j] for k in range(n)), Q(0)) for j in range(n)] for i in range(n)]


def charpoly(a):
    """Faddeev-LeVerrier: coefficients c[0..n] of det(x I - A)."""
    n = len(a)
    c = [Q(0)] * (n + 1)
    c[n] = Q(1)
    m = [[Q(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        am = matmul(a, m)
        m = [[am[i][j] + (c[n - k + 1] if i == j else 0) for j in range(n)] for i in range(n)]
        am = matmul(a, m)
        c[n - k] = -sum((am[i][i] for i in range(n)), Q(0)) / k
    return c


def roots_above(coeffs, mu):
    """(number of roots > mu, multiplicity at mu) for a real-rooted polynomial (Descartes exact)."""
    n = len(coeffs) - 1
    shifted = [Q(0)] * (n + 1)
    for i, c in enumerate(coeffs):
        if c != 0:
            for j in range(i + 1):
                shifted[j] += c * binom(i, j) * mu ** (i - j)
    m = 0
    while m <= n and shifted[m] == 0:
        m += 1
    signs = [1 if c > 0 else -1 for c in shifted[m:] if c != 0]
    return sum(1 for x, y in zip(signs, signs[1:]) if x != y), m


def count_below(coeffs, mu):
    above, mult = roots_above(coeffs, mu)
    return len(coeffs) - 1 - above - mult


def eigmin_bracket(coeffs, lo=Q(-2), hi=Q(0), steps=64):
    must(count_below(coeffs, lo) == 0 and count_below(coeffs, hi) >= 1, 'eigenvalue bracket precondition')
    for _ in range(steps):
        mid = (lo + hi) / 2
        if count_below(coeffs, mid) >= 1:
            hi = mid
        else:
            lo = mid
    return lo, hi


R_BITS = (0, 1)


def meets_R(support):
    return any(i in R_BITS for i in support)


def fixture_epsilon(amps, supports_filter=meets_R):
    first = sum((abs(a) for s, a in amps.items() if supports_filter(s)), Q(0))
    left = sum((abs(a) for s, a in amps.items() if supports_filter(s) and 0 in s and 1 not in s), Q(0))
    right = sum((abs(a) for s, a in amps.items() if supports_filter(s) and 1 in s and 0 not in s), Q(0))
    return first + left * right


def certify_budget(e2, eps):
    require(Q(e2) <= Q(eps) ** 2, 'budget %s does not bound the actual R-excitation ratio e=%s' % (sci(eps, 6), sci(e2, 6) + '^(1/2)'))
    return True


def certify_local_overlap(claimed, e2):
    claimed = Q(claimed)
    require(Q(0) <= claimed and claimed <= 1, 'claimed local vacuum overlap %s lies outside [0,1]: normalization deleted' % qs(claimed))
    require(claimed == 1 / (1 + Q(e2)), 'claimed local vacuum overlap %s violates Tr(rho_R P_R)=1/(1+e^2)=%s' % (qs(claimed), qs(1 / (1 + Q(e2)))))
    return claimed


def certify_unnormalized_density(candidate, truth):
    n = len(candidate)
    require(all(candidate[i][j] == candidate[j][i] for i in range(n) for j in range(n)),
            'reduced density is not Hermitian: an adjoint cross term was omitted')
    require(candidate == truth, 'reduced density differs from Tr_out|psi><psi|: cross terms or excited block omitted')
    return True


def fixture_analysis(amps, n, name):
    dim = 1 << n
    psi = fixture_ground(amps, n)
    must(psi == fixture_ground(amps, n, order=list(reversed(sorted(amps)))), 'creations must commute')
    # nilpotent exponential series equals the ordered product
    ops = sorted(amps.items())
    term, total = [Q(0)] * dim, [Q(0)] * dim
    term[0] = Q(1)
    total[0] = Q(1)
    for k in range(1, n + 2):
        term = [-x / k for x in apply_sum(ops, term)]
        total = [x + y for x, y in zip(total, term)]
    must(all(x == 0 for x in term) and total == psi, 'e^{-C} series must terminate and equal the product')
    for s1, a1 in ops:
        for s2, a2 in ops:
            if set(s1) & set(s2):
                for b in range(dim):
                    e = [Q(0)] * dim
                    e[b] = Q(1)
                    must(all(x == 0 for x in apply_creation(s1, a1, apply_creation(s2, a2, e))), 'overlapping creations must multiply to zero')
    cr = [(s, a) for s, a in ops if meets_R(s)]
    out_amps = {s: a for s, a in ops if not meets_R(s)}
    psi_out = fixture_ground(out_amps, n)
    projected = [v if (s & 3) == 0 else Q(0) for s, v in enumerate(psi)]
    must(projected == psi_out, '(P_R x 1) psi must equal psi_out')
    delta = [x - y for x, y in zip(psi, psi_out)]
    must(dot(psi_out, delta) == 0, 'psi_out and delta must be orthogonal')
    for b in range(dim):
        e = [Q(0)] * dim
        e[b] = Q(1)
        must(all(x == 0 for x in apply_sum(cr, apply_sum(cr, apply_sum(cr, e)))), 'C_R^3 must vanish')
    first = apply_sum(cr, psi_out)
    second = apply_sum(cr, first)
    must(delta == [-x + y / 2 for x, y in zip(first, second)], 'delta = -C_R psi_out + C_R^2 psi_out/2')
    z_out, z_delta, z = dot(psi_out, psi_out), dot(delta, delta), dot(psi, psi)
    must(z == z_out + z_delta, 'Pythagoras for the split')
    e2 = z_delta / z_out
    rho_un = reduced_R(psi, n)
    rho = [[x / z for x in row] for row in rho_un]
    fidelity = rho[0][0]
    must(fidelity == 1 / (1 + e2), 'Tr(rho_R P_R)=1/(1+e^2)')
    eps = fixture_epsilon(amps)
    must(e2 <= eps * eps, 'e <= eps with straddling and two-creation terms')
    # explicit reduced density with both cross terms (adjoint included)
    phi = [psi_out[o << 2] for o in range(1 << (n - 2))]
    xi = [sum((delta[(o << 2) + r] * phi[o] for o in range(len(phi))), Q(0)) for r in range(4)]
    dd = reduced_R(delta, n)
    phi2 = dot(phi, phi)
    must(phi2 == z_out and xi[0] == 0, 'phi_out norm and <Omega_R,xi>=0')
    decomposition = [[(phi2 if (i == 0 and j == 0) else Q(0)) + (xi[i] if j == 0 else Q(0)) +
                      (xi[j] if i == 0 else Q(0)) + dd[i][j] for j in range(4)] for i in range(4)]
    certify_unnormalized_density(decomposition, rho_un)
    # trace-norm certificate for ||rho_R - P_R||_1 <= 2 sqrt(1-F) <= 2 eps/sqrt(1+eps^2)
    x = [[rho[i][j] - (1 if i == j == 0 else 0) for j in range(4)] for i in range(4)]
    cp = charpoly(x)
    negatives = count_below(cp, Q(0))
    must(negatives == 1, 'rho_R - P_R has exactly one negative eigenvalue')
    lam_lo, lam_hi = eigmin_bracket(cp)
    must(lam_lo * lam_lo <= 1 - fidelity, 'trace norm -2 lambda_min <= 2 sqrt(1-F)')
    must((1 - fidelity) * (1 + eps * eps) <= eps * eps, '1-F <= eps^2/(1+eps^2)')
    # trace-zero effect refinement on two effects 0<=A<=I
    effects = {'P_R': [[Q(1) if i == j == 0 else Q(0) for j in range(4)] for i in range(4)],
               'site0_plus_x': [[(Q(1, 2) if i == j else (Q(1, 2) if (i ^ j) == 1 else Q(0))) for j in range(4)] for i in range(4)]}
    effect_values = {}
    for label, eff in effects.items():
        val = sum((x[i][j] * eff[j][i] for i in range(4) for j in range(4)), Q(0))
        must(abs(val) <= -lam_hi, 'effect refinement |Tr(X A)| <= ||X||_1/2')
        effect_values[label] = qs(val)
    return {
        'name': name, 'sites': n, 'cover_bits': [0, 1],
        'amplitudes': {'{' + ','.join(str(i) for i in s) + '}': qs(a) for s, a in sorted(amps.items())},
        'norm_sq_psi': qs(z), 'norm_sq_psi_out': qs(z_out), 'norm_sq_delta': qs(z_delta),
        'e_squared': qs(e2), 'local_vacuum_overlap': qs(fidelity), 'epsilon': qs(eps),
        'lambda_min_bracket': [qs(lam_lo), qs(lam_hi)],
        'trace_norm_bracket': [qs(-2 * lam_hi), qs(-2 * lam_lo)],
        'trace_norm_preview': sci(-2 * lam_lo, 8), 'effect_values': effect_values,
        'reduced_density': [[qs(v) for v in row] for row in rho],
        '_psi': psi, '_psi_out': psi_out, '_z': z, '_z_out': z_out, '_e2': e2, '_F': fidelity,
        '_lam': (lam_lo, lam_hi), '_rho_un': rho_un, '_xi': xi, '_dd': dd, '_eps': eps,
    }


# ------------------------------------------------------------- cutoff fixture
def mat_inverse(a):
    n = len(a)
    m = [list(row) + [Q(1) if i == j else Q(0) for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        pv = m[col][col]
        m[col] = [v / pv for v in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [row[n:] for row in m]


def transpose(a):
    return [list(r) for r in zip(*a)]


def certify_cutoff_removal(uniform_gap, method):
    require(method == 'rayleigh_quotient_with_uniform_gap',
            'cutoff removal by %s: eigenvalue convergence does not move the ground vector' % method)
    require(Q(uniform_gap) > 0, 'no uniform cutoff gap: vector convergence is not implied')
    return True


def certify_passage(topology, quantifier, claims):
    require(topology == 'local_trace_norm', 'passage by %s is not the admitted local trace-norm convergence' % topology)
    require(quantifier == 'every_subsequential_limit', 'passage quantifier must be every subsequential limit')
    forbidden = sorted(set(claims) - {'bound_on_R'})
    require(not forbidden, 'passage claims beyond the bound: ' + ','.join(forbidden))
    return True


# --------------------------------------------------------------- verdicts
def producer_outcome(split_exact, orthogonal, uniform_in_N, tier_ii_available, D_ii_upper, target,
                     cutoff_complete, passage_complete):
    if not (split_exact and orthogonal and uniform_in_N):
        return 'insufficient'
    if not tier_ii_available or Q(D_ii_upper) > Q(target) or not (cutoff_complete and passage_complete):
        return 'limited'
    return 'accepted_within_scope'


def certify_outcome(recorded, inputs):
    computed = producer_outcome(**inputs)
    require(recorded == computed, 'recorded outcome %s differs from the evidence-derived outcome %s' % (recorded, computed))
    return computed


def validate_claim_flags(flags):
    require(sorted(flags) == sorted(CLAIM_FLAGS), 'claim flag set changed')
    for key in sorted(flags):
        require(flags[key] is False, 'claim flag %s must be false in AV1' % key)
    return True


def admit_bound(value, target):
    require(isinstance(value, Q) and isinstance(target, Q), 'admission requires exact rationals, not floating values')
    return value <= target


def centered_variance_lower(D, charge_mean_square):
    return floor_to(Q(1, 4) - D / 2 - (D * D if charge_mean_square else 0))


def certify_variance_lower(claimed, D):
    worst = Q(1, 4) - D / 2 - D * D     # min over |m|<=D, q>=1/4-D/2 of q-m^2
    require(Q(claimed) <= worst, 'variance lower bound %s omits the mean-square charge m^2<=D^2' % sci(claimed, 12))
    return True


def certify_mean_budget(mean_abs, budget):
    require(Q(mean_abs) <= Q(budget), 'mean budget %s is below the actual first-order mean %s' % (qs(budget), qs(mean_abs)))
    return True


def certify_linear_scaling(bracket):
    require(Q(99) <= bracket[0] and bracket[1] <= Q(101),
            'D(tau)/D(tau/100) in [%s,%s] is not linear scaling [99,101]' % (sci(bracket[0], 6), sci(bracket[1], 6)))
    return True


# --------------------------------------------------------------- contract
def parse_av2_relation(text):
    m = re.search(r'2\(D\+D\^2\)\+(\d+)\*10\^-(\d+)/pi<=10\^-(\d+) requires D<=(\d+)\.(\d+)\*10\^-(\d+)', text)
    require(m is not None, 'AV2 feasibility relation not found in the contract')
    coeff, e1, e2 = int(m.group(1)), int(m.group(2)), int(m.group(3))
    stated = Q(int(m.group(4) + m.group(5)), 10 ** len(m.group(5))) / 10 ** int(m.group(6))
    return coeff, e1, e2, stated


PI_LO, PI_HI = None, None


def av2_feasible(D, relation):
    coeff, e1, e2, _ = relation
    D = Q(D)
    return 2 * (D + D * D) + Q(coeff, 10 ** e1) / PI_LO <= Q(1, 10 ** e2)


def certify_av2_threshold(D, relation):
    require(av2_feasible(D, relation), 'D=%s violates the AV2 window relation 2(D+D^2)+49e-8/pi<=1e-6' % sci(D, 6))
    return True


def am2_cap_from_gate():
    gate = json.loads((INPUTS / AM2_GATE_REL).read_text())
    m = re.search(r'\|tau\|<=1/(\d+)', gate['accepted'])
    must(m is not None and gate['verdict'] == 'accepted_within_scope', 'AM2 gate cap not found')
    return Q(1, int(m.group(1)))


def validate_contract(data, am2_cap):
    require(data.get('id') == 'AV1' and data.get('status') == 'frozen_before_production', 'contract identity or status')
    p = data['parameters']
    require(parse_q(p['tau_cap']) == am2_cap, 'contract tau cap differs from the admitted AM2 cap')
    require(len(p['selected_coefficients_over_alpha']) == 3 and all(parse_q(x) == 0 for x in p['selected_coefficients_over_alpha']),
            'contract selected triple is not zero')
    ref = p['reference_moments']
    require(parse_q(ref['omega_0(W)']) == HAAR_W and parse_q(ref['omega_0(W^2)']) == HAAR_W2,
            'contract reference moments differ from the Haar moments')
    am2 = p['am2_constants']
    jm = re.fullmatch(r'<=(\d+)\|tau\|', am2['per_site_sum_J'])
    require(jm is not None, 'per-site sum format')
    validate_am2_constants(parse_q(am2['anchored_radius_R']), parse_q(am2['J0']), parse_q(am2['G_at_R_upper']),
                           parse_q(am2['G_prime_at_R_upper']), am2_cap, Q(int(jm.group(1))))
    target = data['preregistration']['target']
    require(target['quantity'] == 'D_ii' and target['comparator'] == '<=', 'target quantity/comparator')
    relation = parse_av2_relation(data['new_control_semantics']['av2_feasibility_threshold'])
    tv = parse_q(target['value'])
    require(tv > 0 and av2_feasible(tv, relation), 'contract target violates the AV2 feasibility relation')
    ids = data['controls']
    require(ids == data['preregistration']['controls_required']['ids'] and len(set(ids)) == len(ids),
            'controls list differs from the preregistered control ids')
    require(data.get('reverse_premise_isolation') is True, 'reverse premise isolation flag')
    return True


def validate_contract_bytes(raw, expected_sha, am2_cap):
    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'contract bytes do not match the bound hash')
    data = json.loads(raw)
    validate_contract(data, am2_cap)
    return data


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    for f in files:
        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)
        require(f not in contract.get('forward_additional_premises', []), 'forward-only premise in reverse inputs: ' + f)
    require(set(files) == expected and len(files) == len(expected),
            'reverse inputs inventory differs from AGENTS.md + contract + shared_premises')
    return True


# ==================================================================== compute
def compute():
    global TAU_CAP, J_PER_TAU, PI_LO, PI_HI
    check_py_sha = sha256_file(HERE / 'check.py')          # recorded before any evaluation
    raw = (INPUTS / CONTRACT_REL).read_bytes()
    contract_sha = hashlib.sha256(raw).hexdigest()
    am2_cap = am2_cap_from_gate()
    PI_LO, PI_HI = pi_bounds()
    must(Q(314159, 100000) < PI_LO and PI_HI < Q(314160, 100000), 'pi enclosure')
    contract = validate_contract_bytes(raw, CONTRACT_SHA256, am2_cap)
    record('contract_snapshot_bound', contract_sha == CONTRACT_SHA256, contract_sha256=contract_sha,
           source='inputs/' + CONTRACT_REL)
    record('check_py_hash_recorded_before_evaluation', len(check_py_sha) == 64, check_py_sha256=check_py_sha)
    cache = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if '__pycache__' in p.parts or p.suffix == '.pyc')
    record('no_interpreter_cache_in_closure', cache == [])

    params = contract['parameters']
    TAU_CAP = parse_q(params['tau_cap'])
    target = parse_q(contract['preregistration']['target']['value'])
    secondary_match = re.search(r'report against 10\^-(\d+)', contract['required'][8])
    must(secondary_match is not None, 'secondary comparison not found in contract item 9')
    secondary = Q(1, 10 ** int(secondary_match.group(1)))
    reference = {k: parse_q(v) for k, v in params['reference_moments'].items()}
    relation = parse_av2_relation(contract['new_control_semantics']['av2_feasibility_threshold'])
    points = []
    for text in params['evaluation_points']:
        m = re.match(r'tau=([+-])1/10\^(\d+)', text)
        must(m is not None, 'evaluation point format')
        points.append(Q(1 if m.group(1) == '+' else -1, 10 ** int(m.group(2))))
    must(points[0] == TAU_CAP and points[1] == -TAU_CAP and points[2] == TAU_CAP / 100, 'evaluation points')

    # ---- SU(2), face vectors, units
    record('su2_casimir_and_haar_moments', CASIMIR_HALF == Q(3, 4) and HAAR_W == 0 and HAAR_W2 == Q(1, 4)
           and reference['omega_0(W)'] == HAAR_W and reference['omega_0(W^2)'] == HAAR_W2,
           casimir_half=qs(CASIMIR_HALF), haar_W=qs(HAAR_W), haar_W2=qs(HAAR_W2),
           clebsch_gordan_half_half=[qs(j) for j in clebsch_gordan(HALF, HALF)])
    record('face_vector_energy_24_norm_half', FACE_ENERGY == 24 and FACE_ENERGY_ALPHA == 3 and FACE_NORM ** 2 == HAAR_W2
           and certify_face_energy(24, 'delta') == 24 and certify_face_energy(3, 'alpha') == 3,
           normalized_energy=qs(FACE_ENERGY), alpha_units_energy=qs(FACE_ENERGY_ALPHA), norm=qs(FACE_NORM),
           statement='W_f Omega_0 is j=1/2 on each of its four links: H_0 eigenvalue 8*4*3/4=24, norm^2=E_Haar[W^2]=1/4')
    region = [(x, y, z) for x in range(4) for y in range(4) for z in range(3)]
    all_faces = [frozenset(face_links(p, a, c)) for p in region for _, a, c in ORIENTATIONS]
    max_shared = max(len(f & g) for i, f in enumerate(all_faces) for g in all_faces[i + 1:])
    record('distinct_faces_share_at_most_one_link', max_shared == 1 and len(set(all_faces)) == len(all_faces),
           faces_examined=len(all_faces), max_shared_links=max_shared,
           consequence='a link of f outside g appears once in W_f W_g; its Haar integral vanishes, so W_f Omega_0 are orthogonal')

    # ---- I1 table, translation covariance, counts
    table_rows = expand_table(I1_TABLE)
    fine_rows = fine_face_classes()
    record('i1_table_reproduced_from_fine_lattice', table_rows == fine_rows and len(table_rows) == 24
           and sum(1 for r in table_rows if r[4] == 'omitted') == 21,
           classes=len(table_rows), omitted=sum(1 for r in table_rows if r[4] == 'omitted'))
    supports = [r[3] for r in table_rows if r[4] == 'omitted']
    at0 = faces_touching(ORIGIN, supports)
    atz = faces_touching(EZ, supports)
    n_by_owner = {}
    for b, k in at0:
        m = owner_set(b, supports[k])
        n_by_owner[m] = n_by_owner.get(m, 0) + 1
    meeting = sorted(set(at0) | set(atz))
    inside = [f for f in meeting if set(owner_set(f[0], supports[f[1]])) <= set(COVER)]
    anchors_R = sorted({f[0] for f in meeting})
    incident = sorted({vsub(u, v) for u in COVER for v in STAR})
    owners_meeting = {}
    for b, k in meeting:
        m = owner_set(b, supports[k])
        owners_meeting[m] = owners_meeting.get(m, 0) + 1
    labelled_bound_84 = len(STAR) * len(supports)
    derived = {'faces_per_factor': len(at0), 'owner_sets_per_factor': len(n_by_owner),
               'faces_meeting_R': len(meeting), 'faces_inside_R': len(inside)}
    unique_anchor = all(b == tuple(min(c[i] for c in owner_set(b, supports[k])) for i in range(3)) for b, k in at0)
    record('translation_covariant_face_counts', len(at0) == len(atz) and anchors_R == incident and len(incident) == 7
           and derived['faces_per_factor'] <= labelled_bound_84 and unique_anchor,
           owner_set_anchor='componentwise minimum (unique star per owner set)',
           derived=derived, incident_anchors=len(incident), owner_set_face_counts=sorted(n_by_owner.values()),
           labelled_bound_84=labelled_bound_84, rule='faces owning a link of u are anchored at u-v, v in the class support')
    cm = re.search(r'counts (\d+) \(omitted faces per factor\), (\d+) \(owner sets per factor\), (\d+) \(faces meeting R\) and (\d+) \(faces inside R\)',
                   contract['required'][10])
    must(cm is not None, 'candidate counts not found in contract item 11')
    candidates = {'faces_per_factor': int(cm.group(1)), 'owner_sets_per_factor': int(cm.group(2)),
                  'faces_meeting_R': int(cm.group(3)), 'faces_inside_R': int(cm.group(4))}
    record('derived_counts_reproduce_contract_candidates', derived == candidates, candidates_from_contract=candidates,
           note='candidates are compared, never used; every value used below is the derived one')
    # boxes: all sites, boundary <= bulk
    box_info = {}
    orth_cache = {}
    for n in sorted(set(n_by_owner.values()) | set(owners_meeting.values())):
        orth_cache[n] = sqrt_bounds(n)
    orth_site_hi, orth_site_lo = Q(0), None
    for N in (2, 3):
        sites, per_site, owners, stars, stars_per_site = box_enumeration(-N, N, supports)
        starset = set(stars)
        bulk = [u for u in sites if all(vsub(u, v) in starset for v in STAR)]
        maxc = max(per_site.values())
        site_orth_hi = {}
        for m, cnt in owners.items():
            hi = sqrt_bounds(cnt)[1]
            for u in m:
                site_orth_hi[u] = site_orth_hi.get(u, Q(0)) + hi
        meet_box = sum(c for m, c in owners.items() if set(m) & set(COVER))
        inside_box = sum(c for m, c in owners.items() if set(m) <= set(COVER))
        must(all(per_site[u] <= derived['faces_per_factor'] for u in sites), 'boundary counts at most bulk')
        must(all(per_site[u] == derived['faces_per_factor'] for u in bulk), 'bulk equals the translation count')
        must(all(stars_per_site[u] <= len(STAR) for u in sites), 'at most four stars per site')
        must(all(r in stars for r in incident), 'seven incident stars retained for N>=2')
        orth_site_hi = max(orth_site_hi, max(site_orth_hi.values()))
        box_info['N=%d' % N] = {'sites': len(sites), 'stars': len(stars), 'faces': len(stars) * len(supports),
                                'max_faces_per_site': maxc, 'bulk_sites': len(bulk),
                                'boundary_sites_below_bulk': sum(1 for u in sites if per_site[u] < maxc),
                                'faces_meeting_R': meet_box, 'faces_inside_R': inside_box,
                                'owner_sets_at_origin': sum(1 for m in owners if ORIGIN in m)}
        must(maxc == derived['faces_per_factor'] and meet_box == derived['faces_meeting_R']
             and inside_box == derived['faces_inside_R'], 'box enumeration reproduces the counts')
    _, per_site_n1, _, stars_n1, _ = box_enumeration(-1, 1, supports)
    record('box_enumeration_every_site', True, boxes=box_info,
           N1_incident_stars_retained=sum(1 for r in incident if r in stars_n1),
           note='max over every site equals the bulk count; boundary counts are smaller; N=1 loses incident stars')
    COUNTS['faces_per_factor'] = DerivedCount(derived['faces_per_factor'], PROVENANCE)
    COUNTS['faces_meeting_R'] = DerivedCount(derived['faces_meeting_R'], PROVENANCE)
    orth_origin_hi = sum((orth_cache[c][1] for c in n_by_owner.values()), Q(0))
    orth_origin_lo = sum((orth_cache[c][0] for c in n_by_owner.values()), Q(0))
    orth_meet_hi = sum((sqrt_bounds(c)[1] for c in owners_meeting.values()), Q(0))
    must(orth_site_hi == orth_origin_hi, 'orthogonal anchored sum is maximal in the bulk')
    COUNTS['orth_site_sum_hi'] = orth_site_hi
    COUNTS['orth_meeting_R_hi'] = orth_meet_hi
    record('owner_set_orthogonal_norms', orth_origin_lo <= orth_origin_hi and orth_origin_hi < derived['faces_per_factor']
           and orth_meet_hi < derived['faces_meeting_R'],
           site_sum_sqrt_n_bounds=[qs(orth_origin_lo), qs(orth_origin_hi)], site_sum_preview=sci(orth_origin_hi, 8),
           meeting_R_sum_sqrt_n_upper=qs(orth_meet_hi), meeting_R_preview=sci(orth_meet_hi, 8),
           note='faces with one owner set are orthogonal with norm 1/2: ||c1_M||=(|tau|/144)sqrt(n_M); anchored norm stays l1 over owner sets')

    # ---- Wilson cover
    owners_W = tuple(sorted({coarse(t) for t, _ in W_LINKS}))
    cover_links = set(factor_links(ORIGIN)) | set(factor_links(EZ))
    ends0 = {t for t, _ in factor_links(ORIGIN)} | {vadd(t, DIRS[d]) for t, d in factor_links(ORIGIN)}
    endsz = {t for t, _ in factor_links(EZ)} | {vadd(t, DIRS[d]) for t, d in factor_links(EZ)}
    cover_text = params['cover']
    cmatch = re.search(r'(\d+) links, (\d+) original endpoints, (\w+) incident anchors', cover_text)
    must(cmatch is not None, 'cover text')
    words = {'seven': 7}
    w_face = next(r for r in table_rows if r[0] == 'xz' and r[1] == 0 and r[2] == 0)
    record('wilson_cover_48_links_36_endpoints_7_anchors', owners_W == COVER and certify_cover(COVER) == COVER
           and len(cover_links) == 48 and len(ends0) == 22 and len(endsz) == 22 and len(ends0 & endsz) == 8
           and len(ends0 | endsz) == 36 and int(cmatch.group(1)) == 48 and int(cmatch.group(2)) == 36
           and words.get(cmatch.group(3)) == len(incident),
           links=len(cover_links), endpoints=len(ends0 | endsz), shared_endpoints=len(ends0 & endsz),
           incident_anchors=[list(a) for a in incident])
    record('original_wilson_face_is_an_omitted_first_order_face', w_face[3] == COVER and w_face[4] == 'omitted',
           statement='W itself is one of the ten omitted faces with owner set R, so the first-order vector has a component along W Omega_0; no parity argument removes a first-order mean (its value is not claimed)')

    # ---- AM2 constants and family identification
    enc = am2_enclosures()
    star_norm = len(supports) * OMITTED_PER_ANCHOR_NORM_UNIT
    J_PER_TAU = len(STAR) * star_norm
    lk = [16 * 8 ** k * (1 + Q(5 * k, 4)) for k in range(9)]
    taylor_ok = all(Q(16 * 8 ** k, factorial(k)) + (Q(160 * 8 ** (k - 1), factorial(k - 1)) if k else 0) == lk[k] / factorial(k)
                    for k in range(9))
    am2 = params['am2_constants']
    jm_contract = re.fullmatch(r'<=(\d+)\|tau\|', am2['per_site_sum_J'])
    must(jm_contract is not None, 'per-site sum text')
    record('am2_fixed_point_constants_certified', enc['exp_one_eighth'][1] < Q(8, 7) and enc['G'][1] < G_R_UP
           and enc['G_prime'][1] < GP_R_UP and 16 * Q(8, 7) * (1 + 10 * R_RADIUS) == G_R_UP
           and 16 * Q(8, 7) * (18 + 80 * R_RADIUS) == GP_R_UP and J_PER_TAU == Q(int(jm_contract.group(1))) and taylor_ok
           and J_PER_TAU * TAU_CAP == parse_q(am2['J0']) and parse_q(am2['G_at_R_upper']) == G_R_UP
           and parse_q(am2['G_prime_at_R_upper']) == GP_R_UP and parse_q(am2['anchored_radius_R']) == R_RADIUS
           and am2['majorant_G'] == '16*exp(8t)*(1+10t)' and am2['nested_order_termination'] == 8
           and validate_am2_constants(R_RADIUS, J_PER_TAU * TAU_CAP, G_R_UP, GP_R_UP, TAU_CAP, J_PER_TAU),
           R=qs(R_RADIUS), J_per_tau=qs(J_PER_TAU), star_norm_per_tau=qs(star_norm), J0=qs(J_PER_TAU * TAU_CAP),
           exp_one_eighth=[qs(v) for v in enc['exp_one_eighth']], G_R_enclosure=[qs(v) for v in enc['G']],
           G_prime_R_enclosure=[qs(v) for v in enc['G_prime']], G_R_upper=qs(G_R_UP), G_prime_R_upper=qs(GP_R_UP),
           self_map=qs(J_PER_TAU * TAU_CAP * G_R_UP), contraction=qs(2 * J_PER_TAU * TAU_CAP * GP_R_UP),
           L_k_num=[qs(v) for v in lk])
    nonzero_lambda = Q(1, 100)
    trial = Q(3, 4) * (nonzero_lambda / 3) ** 2 - nonzero_lambda * (nonzero_lambda / 3) / 2
    record('aq1_boxes_are_am2_family', J_PER_TAU == Q(int(jm_contract.group(1))) and trial == -nonzero_lambda ** 2 / 12 and trial < 0,
           statement='Lambda_N=[-N,N]^3 retains exactly the stars b+S inside Lambda_N, the AM2 V for that finite complete-factor set; at the zero triple h_b=8 sum C_e has the constant Haar vacuum (gap 6>=1)',
           nonzero_triple_trial_energy_alpha_one=qs(trial))

    # ---- fixtures: product ordering, trap, counterexample
    fx_b = fixture_analysis({(0,): Q(1, 2), (1,): Q(1, 3), (2,): Q(-1), (0, 1): Q(1, 5), (0, 2): Q(1, 2),
                             (1, 2): Q(-1, 4), (0, 1, 2): Q(1, 7)}, 3, 'B_all_seven_supports')
    record('product_ordering_split_and_vacuum_overlap_identity', True, fixture='fixtures.B_all_supports',
           e_squared=fx_b['e_squared'], epsilon=fx_b['epsilon'], local_vacuum_overlap=fx_b['local_vacuum_overlap'],
           identities=['(P_R x 1)psi=psi_out', '<psi_out,delta>=0', 'C_R^3=0', 'delta=-C_R psi_out+C_R^2 psi_out/2',
                       'Tr(rho_R P_R)=1/(1+e^2)', 'e<=eps', 'rho_R has both cross terms',
                       '||rho_R-P_R||_1<=2sqrt(1-F)<=2eps/sqrt(1+eps^2)'])
    fx_a = fixture_analysis({(0,): Q(1, 2), (0, 2): Q(1, 2), (2,): Q(-1)}, 3, 'A_counterexample')
    naive_amps = {(0,): Q(1, 2), (0, 2): Q(1, 2)}
    fx_naive = fixture_analysis(naive_amps, 3, 'A_naive_restriction')
    record('three_site_counterexample_naive_restriction', fx_a['_e2'] > fx_naive['_e2'] and fx_a['_F'] != fx_naive['_F']
           and fx_a['_lam'][1] < fx_naive['_lam'][0] and fx_a['_rho_un'][0][1] != 0,
           actual={'e2': fx_a['e_squared'], 'F': fx_a['local_vacuum_overlap'], 'trace_norm': fx_a['trace_norm_bracket']},
           naive={'e2': fx_naive['e_squared'], 'F': fx_naive['local_vacuum_overlap'], 'trace_norm': fx_naive['trace_norm_bracket']},
           conclusion='dropping the outside creation (support {2}) changes the R-marginal; the naive e^2 and trace distance are smaller than the actual ones, so naive restriction is neither exact nor a bound')
    scaled = []
    for k in range(1, 5):
        n = 2 + k
        amps = {(0,): Q(1, 2), (0, 2): Q(1, 2)}
        for j in range(2, n):
            amps[(j,)] = Q(-1)
        fx = fixture_analysis(amps, n, 'scaled_k%d' % k)
        scaled.append({'outside_sites': k, 'unnormalized_overlap_norm_sq_psi_out': qs(fx['_z_out']),
                       'global_vacuum_overlap': qs(1 / fx['_z']), 'local_vacuum_overlap': qs(fx['_F'])})
    record('normalization_trap_volume_dependence', all(s['local_vacuum_overlap'] == '8/13' for s in scaled)
           and [s['unnormalized_overlap_norm_sq_psi_out'] for s in scaled] == ['2', '4', '8', '16'],
           scaled=scaled, conclusion='outside creations multiply numerator and denominator by (1+a^2)^k; only the normalized ratio is volume independent, while the global vacuum overlap decays')
    fx_c = fixture_analysis({(0, 2): Q(1, 2), (1, 2): Q(1, 3), (2,): Q(1), (0, 1, 2): Q(1, 5)}, 3, 'C_straddling_only')

    # ---- tiers at both signs, variants, scaling
    tiers = {}
    for key, fn in (('tier_i', lambda t: tier_i(t)), ('tier_i_iterated', lambda t: tier_i(t, iterate=4)),
                    ('tier_ii', lambda t: tier_ii(t)),
                    ('tier_ii_directed_remainder', lambda t: tier_ii(t, remainder='directed_G')),
                    ('tier_ii_owner_set_orthogonal', lambda t: tier_ii(t, norm='owner_set_orthogonal'))):
        tiers[key] = {'+': fn(points[0]), '-': fn(points[1]), 'scaling_point': fn(points[2])}
    for key in tiers:
        must(tiers[key]['+']['_D_up'] == tiers[key]['-']['_D_up'], 'both signs give the same bound')
    D_i = tiers['tier_i']['+']['_D_up']
    D_ii = tiers['tier_ii']['+']['_D_up']
    record('tier_i_values_both_signs', tiers['tier_i']['+']['t_upper'] == qs(J_PER_TAU * TAU_CAP * G_R_UP)
           and D_i == tiers['tier_i']['-']['_D_up'],
           D_i_plus=qs(D_i), D_i_minus=tiers['tier_i']['-']['D_upper'], preview=sci(D_i),
           iterated_D=tiers['tier_i_iterated']['+']['D_upper_preview'])
    record('tier_ii_values_both_signs', D_ii == tiers['tier_ii']['-']['_D_up']
           and tiers['tier_ii']['+']['t1_first_order_anchored'] == qs(per_face_coefficient(TAU_CAP, 'delta', 'delta') * derived['faces_per_factor'])
           and tiers['tier_ii']['+']['a1_first_order_meeting_R'] == qs(per_face_coefficient(TAU_CAP, 'delta', 'delta') * derived['faces_meeting_R'])
           and Q(tiers['tier_ii']['+']['remainder_anchored_upper']) > 0,
           D_ii_plus=qs(D_ii), D_ii_minus=tiers['tier_ii']['-']['D_upper'], preview=sci(D_ii))
    record('tier_ii_sharper_variants_consistent', tiers['tier_ii_directed_remainder']['+']['_D_up'] <= D_ii
           and tiers['tier_ii_owner_set_orthogonal']['+']['_D_up'] < D_ii,
           directed_remainder=tiers['tier_ii_directed_remainder']['+']['D_upper_preview'],
           owner_set_orthogonal=tiers['tier_ii_owner_set_orthogonal']['+']['D_upper_preview'])
    fwd_form_ok = True
    for key in ('tier_i', 'tier_ii'):
        eps = Q(tiers[key]['+']['epsilon'])
        fwd_form_ok = fwd_form_ok and (2 * eps) ** 2 / (1 + eps * eps) <= (2 * eps * (1 + eps) / (1 + eps * eps)) ** 2
    record('fidelity_form_not_weaker_than_direct_form', fwd_form_ok,
           statement='2eps/sqrt(1+eps^2) <= 2eps(1+eps)/(1+eps^2) since (1+eps)^2>=1+eps^2 (contract item 2 form; no forward work read)')
    tier_ii_target_met = admit_bound(D_ii, target) and admit_bound(tiers['tier_ii']['-']['_D_up'], target)
    record('tier_ii_target_met_both_signs', tier_ii_target_met is True, target=qs(target), D_ii=qs(D_ii),
           margin_factor_preview=sci(target / D_ii, 6), source='contract preregistration.target')
    record('secondary_comparison_1e-6', D_ii <= secondary and not (D_i <= secondary), secondary=qs(secondary),
           tier_i_meets_secondary=False)
    record('tier_i_target_not_met_retained', not (D_i <= target), note='tier (i) alone would be limited')
    zero = tier_ii('0')
    record('zero_coupling_free_limit', zero['_D_up'] == 0 and tier_i('0')['_D_up'] == 0)
    scaling = {}
    for key in ('tier_i', 'tier_ii', 'tier_ii_owner_set_orthogonal'):
        big, small = tiers[key]['+'], tiers[key]['scaling_point']
        bracket = (big['_D_lo'] / small['_D_up'], big['_D_up'] / small['_D_lo'])
        certify_linear_scaling(bracket)
        scaling[key] = {'ratio_of_rational_upper_bounds': qs(big['_D_up'] / small['_D_up']),
                        'formula_ratio_bracket': [qs(bracket[0]), qs(bracket[1])],
                        'preview': sci(big['_D_up'] / small['_D_up'], 12)}
    at4_big, at4_small = at4_bound(points[0]), at4_bound(points[2])
    at4_ratio_sq = (Q(49, 3) * abs(points[0])) / (Q(49, 3) * abs(points[2]))
    at4_bracket = (at4_big[1] / at4_small[0], at4_big[0] / at4_small[1])
    record('tau_scaling_ratio_linear_vs_square_root', at4_ratio_sq == 100
           and Q(99, 10) <= at4_bracket[0] and at4_bracket[1] <= Q(101, 10),
           scaling=scaling, at4_square_root_ratio_squared=qs(at4_ratio_sq),
           at4_bracket=[qs(at4_bracket[0]), qs(at4_bracket[1])], at4_D_upper_preview=sci(at4_big[0]))

    # ---- consequences
    consequences = {}
    for key in ('tier_i', 'tier_ii'):
        for sign in ('+', '-'):
            D = tiers[key][sign]['_D_up']
            consequences[key + sign] = {
                'abs_omega_W_upper': qs(D + reference['omega_0(W)']),
                'omega_W2_interval': [qs(reference['omega_0(W^2)'] - D / 2), qs(reference['omega_0(W^2)'] + D / 2)],
                'variance_interval': [qs(centered_variance_lower(D, True)), qs(reference['omega_0(W^2)'] + D / 2)],
            }
            must(certify_variance_lower(centered_variance_lower(D, True), D), 'variance bound charges m^2')
    record('consequences_mean_and_second_moment', True, consequences=consequences,
           statement='|omega(W)|<=D by trace duality; |omega(W^2)-1/4|<=D/2 by the trace-zero effect bound; value/sign of omega(W) not claimed')

    # ---- cutoff fixture (Cayley-rational orthogonal matrix)
    skew = [[Q(0), Q(1), Q(2)], [Q(-1), Q(0), Q(1)], [Q(-2), Q(-1), Q(0)]]
    eye = [[Q(1) if i == j else Q(0) for j in range(3)] for i in range(3)]
    orth = matmul([[eye[i][j] - skew[i][j] for j in range(3)] for i in range(3)],
                  mat_inverse([[eye[i][j] + skew[i][j] for j in range(3)] for i in range(3)]))
    must(matmul(transpose(orth), orth) == eye, 'rational orthogonal matrix')
    spec = [Q(0), Q(1, 2), Q(3)]
    ham = matmul(matmul(orth, [[spec[i] if i == j else Q(0) for j in range(3)] for i in range(3)]), transpose(orth))
    ground = [orth[i][0] for i in range(3)]
    gap_rows = []
    for w in ([Q(1), Q(0), Q(0)], [Q(0), Q(1), Q(0)], [Q(1), Q(1), Q(1)], [Q(1), Q(-2), Q(3)]):
        nw = dot(w, w)
        rq = dot(w, [dot(row, w) for row in ham]) / nw
        infidelity = 1 - dot(ground, w) ** 2 / nw
        must(infidelity <= (rq - spec[0]) / spec[1], 'gap inequality 1-|<psi,w>|^2 <= (<w,Hw>-E)/gap')
        gap_rows.append({'w': [qs(v) for v in w], 'infidelity': qs(infidelity), 'rayleigh_minus_E_over_gap': qs((rq - spec[0]) / spec[1])})
    for k in (1, 2):
        block = [row[:k] for row in ham[:k]]
        must(count_below(charpoly(block), spec[0]) == 0, 'compression raises the ground energy')
    record('cutoff_vector_gap_inequality_fixture', True, rows=gap_rows,
           statement='on each cutoff, 1-|<psi_n,w_n>|^2 <= 2(<w_n,H w_n>-E) with w_n=Q_n psi/||Q_n psi||; the right side tends to 0')

    # =================================================== the 25 contract controls
    control('missing_incoming_stars', [
        ('outgoing_star_anchors_only', certify_anchor_set, ([ORIGIN, EZ], supports)),
        ('outgoing_face_count_21_as_derived', certified_count, (DerivedCount(len(supports), 'outgoing_star_only'), 'faces per factor')),
    ], complete_anchor_count=len(incident), outgoing_only_faces_per_factor=len(supports),
        outgoing_only_faces_meeting_R=2 * len(supports), complete_faces_meeting_R=derived['faces_meeting_R'])
    control('full_original_wilson_cover', [
        ('cover_origin_factor_only', certify_cover, ((ORIGIN,),)),
        ('cover_with_extra_factor', certify_cover, ((ORIGIN, EZ, (0, 0, -1)),)),
    ], cover=[list(c) for c in COVER], links=len(cover_links), endpoints=len(ends0 | endsz))
    wrong_small = abs(points[0]) * COUPLING_PER_TAU['alpha'] * FACE_NORM / ENERGY_BY_UNITS['delta']
    wrong_large = abs(points[0]) * COUPLING_PER_TAU['delta'] * FACE_NORM / ENERGY_BY_UNITS['alpha']
    physical = []
    for alpha, hbar, estar in ((Q(1), Q(1), Q(1)), (Q(5, 3), Q(7), Q(2)), (Q(7), Q(1, 3), Q(11))):
        coupling_phys = alpha * abs(points[0]) / 24
        energy_phys = FACE_ENERGY_ALPHA * alpha
        physical.append(qs(coupling_phys * FACE_NORM / energy_phys))
    must(len(set(physical)) == 1 and physical[0] == qs(per_face_coefficient(abs(points[0]), 'delta', 'delta')), 'unit invariance')
    control('wrong_delta_alpha_hbar_clock', [
        ('alpha_coupling_over_delta_energy', per_face_coefficient, (abs(points[0]), 'alpha', 'delta')),
        ('delta_coupling_over_alpha_energy', per_face_coefficient, (abs(points[0]), 'delta', 'alpha')),
        ('exponent_24_labelled_alpha_units', certify_face_energy, (24, 'alpha')),
        ('energy_3_labelled_normalized', certify_face_energy, (3, 'delta')),
    ], correct_per_face=qs(per_face_coefficient(abs(points[0]), 'delta', 'delta')),
        wrong_factors=[qs(wrong_small / per_face_coefficient(abs(points[0]), 'delta', 'delta')),
                       qs(wrong_large / per_face_coefficient(abs(points[0]), 'delta', 'delta'))],
        physical_scale_invariance=physical, note='static ground-state bound: hbar and E_star do not enter; 24 delta = 3 alpha')
    m_c, d_c = Q(1, 4), Q(1, 100)
    record_vs = {'vector_centering_shift': qs(d_c ** 2), 'scalar_subtraction_shift': qs(-2 * m_c * d_c - d_c ** 2),
                 'uncentered_residue': qs(m_c ** 2)}
    control('vector_versus_scalar_centering', [
        ('variance_lower_without_mean_square', certify_variance_lower, (centered_variance_lower(D_ii, False), D_ii)),
        ('variance_lower_without_mean_square_tier_i', certify_variance_lower, (centered_variance_lower(D_i, False), D_i)),
    ], at4_style_exact_control=record_vs,
        statement='vector centering adds d^2, scalar subtraction gives -2md-d^2; the AV1 variance bound charges m^2<=D^2')
    mean_a = Q(1, 10)
    mean_value = abs(2 * mean_a / (1 + mean_a ** 2))
    D_fixture = fidelity_bound(mean_a)[0]
    must(mean_value <= D_fixture, 'fidelity bound dominates the first-order mean in the fixture')
    control('first_order_mean_charged', [
        ('second_order_only_budget', certify_mean_budget, (mean_value, mean_a ** 2)),
        ('zero_first_order_mean_budget', certify_mean_budget, (mean_value, Q(0))),
    ], fixture_mean_abs=qs(mean_value), fixture_D=qs(D_fixture),
        model_statement='the original W face is inside the first-order vector (owner set R); D_ii is linear in tau and charges it; its coefficient is excluded from claims')
    control('tau_scaling_exponent', [
        ('square_root_bound_labelled_linear', certify_linear_scaling, (at4_bracket,)),
    ], tier_ratios={k: v['preview'] for k, v in scaling.items()}, at4_ratio='10 (exact square root)')
    control('changed_model_relabelled', [
        ('nonzero_selected_triple', certify_model, (points[0], ('0', '1/100', '0'))),
        ('coupling_above_cap', certify_model, (TAU_CAP * 10, ('0', '0', '0'))),
        ('negative_coupling_above_cap', certify_model, (-TAU_CAP * 10, ('0', '0', '0'))),
    ], note='beyond the cap the certificate is silent; that is not a gap failure')
    tampers = {}
    base = json.loads(raw)

    def coherent(mut):
        doc = json.loads(json.dumps(base))
        mut(doc)
        blob = json.dumps(doc, indent=2).encode()
        return blob, hashlib.sha256(blob).hexdigest()

    for label, mut in (
            ('target_relaxed_to_1e-3', lambda d: d['preregistration']['target'].__setitem__('value', '1/1000')),
            ('reference_second_moment_1_3', lambda d: d['parameters']['reference_moments'].__setitem__('omega_0(W^2)', '1/3')),
            ('tau_cap_1e-7', lambda d: d['parameters'].__setitem__('tau_cap', '1/10000000')),
            ('G_prime_288', lambda d: d['parameters']['am2_constants'].__setitem__('G_prime_at_R_upper', '288')),
            ('control_removed', lambda d: d['controls'].pop())):
        blob, digest = coherent(mut)
        tampers[label] = (blob, digest)
    control('coherent_evidence_tampering', [
        (label, validate_contract_bytes, (blob, digest, am2_cap)) for label, (blob, digest) in sorted(tampers.items())
    ] + [('byte_change_without_rehash', validate_contract_bytes, (raw + b' ', CONTRACT_SHA256, am2_cap))],
        note='each tampered copy is rehashed coherently; semantic recomputation still rejects it')
    good_inputs = dict(split_exact=True, orthogonal=True, uniform_in_N=True, tier_ii_available=True,
                       D_ii_upper=D_ii, target=target, cutoff_complete=True, passage_complete=True)
    tier_i_only = dict(good_inputs, tier_ii_available=False, D_ii_upper=D_i)
    over_target = dict(good_inputs, D_ii_upper=target * 2)
    split_failed = dict(good_inputs, orthogonal=False)
    conditional_cutoff = dict(good_inputs, cutoff_complete=False)
    must(producer_outcome(**tier_i_only) == 'limited' and producer_outcome(**over_target) == 'limited'
         and producer_outcome(**split_failed) == 'insufficient' and producer_outcome(**conditional_cutoff) == 'limited',
         'limited and insufficient outcomes are produced')
    outcome = certify_outcome(producer_outcome(**good_inputs), good_inputs)
    control('insufficient_verdict_retained', [
        ('tier_i_only_relabelled_accepted', certify_outcome, ('accepted_within_scope', tier_i_only)),
        ('over_target_relabelled_accepted', certify_outcome, ('accepted_within_scope', over_target)),
        ('split_failure_relabelled_limited', certify_outcome, ('limited', split_failed)),
        ('conditional_cutoff_relabelled_accepted', certify_outcome, ('accepted_within_scope', conditional_cutoff)),
    ], retained_outcomes={'tier_i_only': 'limited', 'over_target': 'limited', 'split_failure': 'insufficient',
                          'conditional_cutoff': 'limited'})
    control('exact_arithmetic_admission', [
        ('float_tau', tier_ii, (1e-08,)),
        ('bool_tau', tier_i, (True,)),
        ('nan_string', parse_q, ('NaN',)),
        ('float_bound_admission', admit_bound, (float(1), target)),
        ('zero_denominator', parse_q, ('1/0',)),
    ], note='every Boolean is decided on Fraction values; decimal strings are previews')
    exact_orth_lo = orth_origin_lo
    control('root_n_misuse', [
        ('sqrt_of_total_49_across_owner_sets', certify_t1_over_coefficient, (sqrt_bounds(derived['faces_per_factor'])[1], exact_orth_lo)),
        ('sqrt_of_faces_meeting_R_per_site', certify_t1_over_coefficient, (sqrt_bounds(derived['faces_meeting_R'])[1], exact_orth_lo)),
    ], exact_anchored_first_order_over_coefficient=[qs(orth_origin_lo), qs(orth_origin_hi)],
        rule='sqrt(n) only within one owner set (orthogonal equal-norm faces); the anchored norm is l1 over owner sets')
    flags_bad = dict(CLAIM_FLAGS, continuum_claim=True)
    flags_prio = dict(CLAIM_FLAGS, scientific_priority_verified=True)
    must(validate_claim_flags(CLAIM_FLAGS), 'claim flags')
    control('no_priority_or_continuum_claim', [
        ('continuum_claim_true', validate_claim_flags, (flags_bad,)),
        ('priority_claim_true', validate_claim_flags, (flags_prio,)),
        ('uniform_wilson_claim_true', validate_claim_flags, (dict(CLAIM_FLAGS, uniform_wilson_claim=True),)),
    ])
    fz = fx_a['_z']
    control('deleted_normalization', [
        ('unnormalized_projection_overlap', certify_local_overlap, (fx_a['_z_out'], fx_a['_e2'])),
        ('vacuum_coefficient_normalization', certify_local_overlap, (fx_a['_psi'][0] ** 2 / fz, fx_a['_e2'])),
    ], actual_overlap=qs(fx_a['_F']), unnormalized=qs(fx_a['_z_out']), global_vacuum=qs(1 / fz), scaled=scaled)
    control('outside_creations_do_not_cancel_naively', [
        ('marginal_of_restricted_vector', certify_local_overlap, (fx_naive['_F'], fx_a['_e2'])),
        ('restricted_e_as_exact_budget', certify_budget, (fx_a['_e2'], sqrt_bounds(fx_naive['_e2'])[1])),
    ], actual={'e2': qs(fx_a['_e2']), 'F': qs(fx_a['_F'])}, naive={'e2': qs(fx_naive['_e2']), 'F': qs(fx_naive['_F'])})
    xi, dd, rho_un = fx_b['_xi'], fx_b['_dd'], fx_b['_rho_un']
    phi2 = fx_b['_z_out']
    no_adjoint = [[(phi2 if (i == 0 and j == 0) else Q(0)) + (xi[i] if j == 0 else Q(0)) + dd[i][j] for j in range(4)] for i in range(4)]
    no_cross = [[(phi2 if (i == 0 and j == 0) else Q(0)) + dd[i][j] for j in range(4)] for i in range(4)]
    no_excited = [[(phi2 if (i == 0 and j == 0) else Q(0)) + (xi[i] if j == 0 else Q(0)) + (xi[j] if i == 0 else Q(0)) for j in range(4)] for i in range(4)]
    control('omitted_adjoint_terms', [
        ('adjoint_cross_term_dropped', certify_unnormalized_density, (no_adjoint, rho_un)),
        ('both_cross_terms_dropped', certify_unnormalized_density, (no_cross, rho_un)),
        ('excited_block_dropped', certify_unnormalized_density, (no_excited, rho_un)),
    ], xi=[qs(v) for v in xi])
    fx_c_inside_eps = fixture_epsilon({s: a for s, a in [((0, 2), Q(1, 2)), ((1, 2), Q(1, 3)), ((2,), Q(1)), ((0, 1, 2), Q(1, 5))]},
                                      supports_filter=lambda s: set(s) <= set(R_BITS))
    must(certify_budget(fx_c['_e2'], fx_c['_eps']), 'full budget bounds the straddling fixture')
    control('straddling_supports_counted', [
        ('fixture_budget_inside_cover_only', certify_budget, (fx_c['_e2'], fx_c_inside_eps)),
        ('model_faces_inside_R_as_meeting_count', certified_count, (DerivedCount(derived['faces_inside_R'], 'inside_cover_only'), 'faces meeting R')),
    ], fixture='fixtures.C_straddling_only', fixture_e2=fx_c['e_squared'], fixture_inside_only_budget=qs(fx_c_inside_eps),
        straddling_faces_meeting_R=derived['faces_meeting_R'] - derived['faces_inside_R'])
    control('anchored_norm_restricted_to_cover', [
        ('model_first_order_norm_from_faces_inside_R', certify_t1_over_coefficient, (Q(derived['faces_inside_R']), exact_orth_lo)),
        ('fixture_anchored_norm_restricted_to_cover', certify_budget, (fx_c['_e2'], fx_c_inside_eps)),
    ], note='the remainder bound needs the global anchored norm of every support, not only supports inside R')
    control('am2_fixed_point_constants', [
        ('G_prime_at_zero_288', validate_am2_constants, (R_RADIUS, J_PER_TAU * TAU_CAP, G_R_UP, Q(288), TAU_CAP, J_PER_TAU)),
        ('radius_1_32', validate_am2_constants, (Q(1, 32), J_PER_TAU * TAU_CAP, G_R_UP, GP_R_UP, TAU_CAP, J_PER_TAU)),
        ('G_at_zero_16', validate_am2_constants, (R_RADIUS, J_PER_TAU * TAU_CAP, Q(16), GP_R_UP, TAU_CAP, J_PER_TAU)),
        ('J0_one_star_7', validate_am2_constants, (R_RADIUS, 7 * TAU_CAP, G_R_UP, GP_R_UP, TAU_CAP, J_PER_TAU)),
    ])

    def first_order_data(energy, norm_sq, faces, owner_sets):
        require(Q(energy) == FACE_ENERGY, 'face energy %s is not the H_0 eigenvalue 24' % qs(energy))
        require(Q(norm_sq) == HAAR_W2, 'face vector norm^2 %s is not E_Haar[W^2]=1/4' % qs(norm_sq))
        certified_count(faces, 'faces per factor')
        require(owner_sets == derived['owner_sets_per_factor'], 'owner-set count differs from the derived 15')
        return True

    must(first_order_data(FACE_ENERGY, HAAR_W2, COUNTS['faces_per_factor'], derived['owner_sets_per_factor']), 'first-order data')
    control('first_order_face_enumeration', [
        ('one_link_energy_6', first_order_data, (FACE_ENERGY / FACE_LINKS, HAAR_W2, COUNTS['faces_per_factor'], derived['owner_sets_per_factor'])),
        ('unit_norm_face', first_order_data, (FACE_ENERGY, Q(1), COUNTS['faces_per_factor'], derived['owner_sets_per_factor'])),
        ('labelled_bound_84_as_count', first_order_data, (FACE_ENERGY, HAAR_W2, DerivedCount(labelled_bound_84, 'labelled_bound'), derived['owner_sets_per_factor'])),
        ('six_owner_classes_as_sets', first_order_data, (FACE_ENERGY, HAAR_W2, COUNTS['faces_per_factor'], len(set(supports)))),
    ], faces_per_factor=derived['faces_per_factor'], owner_sets=derived['owner_sets_per_factor'],
        per_face_coefficient='|tau|/144')
    gapless = []
    for n in range(1, 5):
        even = n % 2 == 0
        ground_n = [Q(1), Q(0)] if even else [Q(0), Q(1)]
        gapless.append({'n': n, 'eigenvalues': ['0', qs(Q(1, n))], 'ground': [qs(v) for v in ground_n]})
    must(all(dot([Q(g) for g in gapless[i]['ground']], [Q(g) for g in gapless[i + 1]['ground']]) == 0 for i in range(3)),
         'gapless family: ground vectors alternate')
    must(certify_cutoff_removal(Q(1, 2), 'rayleigh_quotient_with_uniform_gap'), 'cutoff removal method')
    control('cutoff_vector_removal', [
        ('eigenvalue_convergence_only', certify_cutoff_removal, (Q(1, 2), 'eigenvalues_only')),
        ('no_uniform_gap', certify_cutoff_removal, (Q(0), 'rayleigh_quotient_with_uniform_gap')),
    ], gapless_counterexample=gapless,
        note='eigenvalues {0,1/n} converge while the ground vectors alternate; the AM2 uniform cutoff gap 1/2 is what moves the vector')
    esc = Q(1, 10)
    weak_limit_trace = 1 - esc / 2
    must(weak_limit_trace < 1 and certify_passage('local_trace_norm', 'every_subsequential_limit', ['bound_on_R']), 'passage')
    control('aq_passage_trace_norm_only', [
        ('weak_star_on_finite_rank', certify_passage, ('weak_star_on_finite_rank', 'every_subsequential_limit', ['bound_on_R'])),
        ('uniqueness_claimed', certify_passage, ('local_trace_norm', 'every_subsequential_limit', ['bound_on_R', 'uniqueness'])),
        ('whole_sequence_claimed', certify_passage, ('local_trace_norm', 'whole_sequence', ['bound_on_R'])),
        ('rate_in_N_claimed', certify_passage, ('local_trace_norm', 'every_subsequential_limit', ['bound_on_R', 'rate_in_N'])),
    ], mass_escape_weak_limit_trace=qs(weak_limit_trace))
    control('tier_mixing_rejected', [
        ('exact_a1_with_crude_remainder', assemble_epsilon, ('ii', {
            'a1': Term('a1', 1, 'ii', 'exact_first_order'),
            'rho': Term('rho', 1, 'i', 'am2_majorant'),
            'T': Term('T', 1, 'ii', 'self_consistent')})),
        ('refined_t_without_self_consistency', assemble_epsilon, ('ii', {
            'a1': Term('a1', 1, 'ii', 'exact_first_order'),
            'rho': Term('rho', 1, 'ii', 'self_consistent_remainder'),
            'T': Term('T', 1, 'ii', 'first_order_only')})),
        ('exact_first_order_inside_tier_i', assemble_epsilon, ('i', {'t': Term('t', 1, 'i', 'exact_first_order')})),
    ])
    control('face_count_all_sites', [
        ('scope_sites_0_and_e_z', certify_site_scope, ('sites_0_and_e_z',)),
        ('orthant_corner_count_as_derived', certified_count,
         (DerivedCount(max(box_enumeration(0, 2, supports)[1][u] for u in COVER), 'orthant_sites_0_and_e_z'), 'faces per factor')),
        ('contract_copied_count', certified_count, (DerivedCount(candidates['faces_per_factor'], 'contract_text'), 'faces per factor')),
        ('hard_coded_integer', certified_count, (49, 'faces per factor')),
    ], orthant_restricted_count=max(box_enumeration(0, 2, supports)[1][u] for u in COVER),
        all_site_count=derived['faces_per_factor'])
    inventory = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    must(validate_inventory(inventory, contract), 'reverse inputs inventory')
    control('reverse_premise_isolation', [
        ('skeptic_triage_added', validate_inventory, (inventory + ['research/round32/skeptic/triage.md'], contract)),
        ('deliberation_added', validate_inventory, (inventory + ['research/round32/advisor/deliberation-1.md'], contract)),
        ('forward_at4_reverse_added', validate_inventory, (inventory + ['research/round31/reverse/at4/report.md'], contract)),
        ('premise_missing', validate_inventory, (inventory[1:], contract)),
    ], inventory_size=len(inventory))
    for D in (target, D_ii):
        must(certify_av2_threshold(D, relation), 'AV2 feasibility')
    stated = relation[3]
    control('av2_feasibility_threshold', [
        ('tier_i_value', certify_av2_threshold, (D_i, relation)),
        ('secondary_1e-6_as_threshold', certify_av2_threshold, (secondary, relation)),
        ('just_above_stated_4.22e-7', certify_av2_threshold, (stated + Q(1, 10 ** 9), relation)),
    ], stated_threshold=qs(stated), stated_threshold_feasible=av2_feasible(stated, relation),
        pi_lower=qs(PI_LO), target=qs(target), D_ii=qs(D_ii))

    ids = [c['id'] for c in CHECKS]
    missing = [c for c in contract['controls'] if c not in ids]
    must(missing == [], 'contract controls without a check: ' + ','.join(missing))

    result = {
        'loop': 'AV1', 'direction': 'reverse', 'route': 'vacuum overlap / fidelity',
        'human_author': 'Hruday N M (BUNZEEY)',
        'contribution_alias': 'HNM-AV1-R reverse fidelity local state lemma',
        'attribution': {
            'creation_expansion': 'established commuting-creation (Schrieffer-Wolff type) expansions; Bravyi-DiVincenzo-Loss 2008 as credited in the AM2 lineage; the AM2 snapshots read here cite Gauvin arXiv:2503.15539v3 Supplement A.6-A.8 and Yarotsky',
            'fidelity_inequalities': 'standard: pure-state trace distance 2sqrt(1-|<u,v>|^2), convexity and concavity (HNM-AT4-F08 is its project alias)',
            'scientific_priority': 'unverified'},
        'contract_snapshot_sha256': contract_sha, 'check_py_sha256': check_py_sha,
        'model': contract['model'],
        'target': {'quantity': 'D_ii', 'value': qs(target), 'comparator': '<=', 'read_from': 'contract preregistration.target'},
        'secondary_comparison': {'value': qs(secondary), 'read_from': 'contract required item 9'},
        'reference_values': {k: qs(v) for k, v in reference.items()},
        'constants': {
            'tau_cap': qs(TAU_CAP), 'anchored_radius_R': qs(R_RADIUS), 'J_per_tau': qs(J_PER_TAU),
            'J0': qs(J_PER_TAU * TAU_CAP), 'G_R_upper': qs(G_R_UP), 'G_prime_R_upper': qs(GP_R_UP),
            'exp_one_eighth_enclosure': [qs(v) for v in enc['exp_one_eighth']],
            'casimir_half': qs(CASIMIR_HALF), 'face_energy_normalized': qs(FACE_ENERGY),
            'face_energy_alpha_units': qs(FACE_ENERGY_ALPHA), 'face_vector_norm': qs(FACE_NORM),
            'coupling_per_face_normalized_per_tau': qs(COUPLING_PER_TAU['delta']),
            'per_face_first_order_coefficient_per_tau': qs(per_face_coefficient(Q(1), 'delta', 'delta')),
            'factor_352J_at_cap': qs(GP_R_UP * J_PER_TAU * TAU_CAP),
            'pi_enclosure': [qs(PI_LO), qs(PI_HI)], 'reference_gap_normalized': qs(8 * CASIMIR_HALF)},
        'face_enumeration': {'derived': derived, 'candidates_from_contract': candidates,
                             'owner_set_face_counts_at_origin': {';'.join(','.join(str(c) for c in p) for p in m): n for m, n in sorted(n_by_owner.items())},
                             'incident_anchors': [list(a) for a in incident], 'labelled_bound_84': labelled_bound_84,
                             'boxes': box_info},
        'tiers': {k: {s: strip(v) for s, v in d.items()} for k, d in tiers.items()},
        'D_i': {'+': qs(tiers['tier_i']['+']['_D_up']), '-': qs(tiers['tier_i']['-']['_D_up']),
                'preview': sci(tiers['tier_i']['+']['_D_up'])},
        'D_ii': {'+': qs(D_ii), '-': qs(tiers['tier_ii']['-']['_D_up']), 'preview': sci(D_ii)},
        'at4_square_root_bound_upper': {'value': qs(at4_big[0]), 'preview': sci(at4_big[0])},
        'scaling': scaling, 'consequences': consequences,
        'fixtures': {'A_counterexample': strip(fx_a), 'A_naive': strip(fx_naive), 'B_all_supports': strip(fx_b),
                     'C_straddling_only': strip(fx_c), 'normalization_scaling': scaled},
        'tier_ii_target_met': tier_ii_target_met,
        'secondary_target_met_tier_ii': D_ii <= secondary,
        'tier_i_target_met': D_i <= target,
        'producer_outcome': outcome,
        'sub_label': 'uniform_local_closeness_not_uniqueness',
        'outcome_note': 'proposed for review; admission requires the forward route, exchange and the skeptical review',
        'claim_exclusions': contract['claim_exclusions'],
        'checks': CHECKS,
    }
    result.update(CLAIM_FLAGS)
    return result


def main():
    ap = argparse.ArgumentParser(description='HNM-AV1 reverse producer checker (exact arithmetic)')
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
    manifest = {'loop': 'AV1', 'direction': 'reverse', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AV1', 'direction': 'reverse', 'checks': len(result['checks']),
                      'D_i_plus': result['D_i']['preview'], 'D_ii_plus': result['D_ii']['preview'],
                      'tier_ii_target_met': result['tier_ii_target_met'], 'outcome': result['producer_outcome']},
                     sort_keys=True))


if __name__ == '__main__':
    main()
