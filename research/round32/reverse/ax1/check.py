#!/usr/bin/env python3
"""HNM-AX1 reverse producer: route-B (Haar reference) re-derivation for the uniform
Kogut-Susskind SU(2) Hamiltonian at fixed spacing and strong bare coupling.

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production under
premise isolation; HNM labels are project aliases. Creation-operator expansions,
Peter-Weyl/centre gradings, trace-distance inequalities and the Nachtergaele-Sims
dynamics theorem are established mathematics; scientific priority is unverified.

The reverse route starts from the uniform Hamiltonian (every elementary face has
coefficient nu=alpha*tau/24) and reconstructs what a Haar-reference re-instantiation
of the admitted AM2/AQ1/AQ2/AV1 chain needs: the single-factor grouping, the per-site
sum, the J_0 re-freeze, the reset budget, the itemized incidence on the cover R, the
state-lemma tiers and the transfer of the AW1 flip/parity statements.

Standard library only. Exact Fraction arithmetic decides every Boolean; decimal
strings are truncated previews. Every contract control is a damaging mutation whose
rejection is required; rejections and failures are explicit exceptions (never
assert), so the run and its output bytes are identical under python -O.

Usage: python3 -B research/round32/reverse/ax1/check.py --output /absolute/fresh/dir
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
CONTRACT_REL = 'research/round32/contracts/ax1.json'
AM2_GATE_REL = 'research/round29/advisor/am2-gate.json'
AL1_GATE_REL = 'research/round29/advisor/al1-gate.json'
AV1_GATE_REL = 'research/round32/advisor/av1-gate.json'
AW1_GATE_REL = 'research/round32/advisor/aw1-gate.json'
CONTRACT_SHA256 = 'bc834eec4f5377041cea9db42a8674cf1f3de0a43b7fef3696a461a011da7d8d'
DEN = 10 ** 40
LABEL = 'uniform Kogut-Susskind SU(2) at fixed spacing, strong bare coupling'
FORBIDDEN_INPUTS = (
    'research/round32/skeptic/triage.md',
    'research/round32/skeptic/loop2-response.md',
    'research/round32/skeptic/ax1',
    'research/round32/experts/',
    'research/round32/advisor/deliberation-',
    'research/round32/forward/ax1/',
    'research/round32/reverse/ax1/',
)
CLAIM_FLAGS = {
    'continuum_claim': False,
    'uniform_wilson_claim': True,
    'weak_coupling_claim': False,
    'resolved_interaction_shift': False,
    'scientific_priority_verified': False,
    'euclidean_node_certified': False,
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


def rejection(function, *args):
    """Run one damaging mutation; return its rejection reason, abort if accepted."""
    try:
        function(*args)
    except Rejected as exc:
        return str(exc)
    raise ProducerError('damaging mutation accepted by ' + function.__name__)


def control(check_id, mutations, **details):
    """A control passes only if every listed mutation is rejected."""
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
    exact = s * s * y.denominator == scaled
    hi = lo if exact else Q(s + 1, DEN)
    must(lo * lo <= y and y <= hi * hi, 'square-root enclosure failed')
    return lo, hi


def factorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


def exp_bounds(x, terms=16):
    """Directed enclosure of exp(x) for 0<=x<=1/2: partial sum plus geometric tail."""
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
    """Machin: pi=16 atan(1/5)-4 atan(1/239) with alternating-series brackets."""
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


# ------------------------------------------------------- SU(2) and units
HALF = Q(1, 2)


def clebsch_gordan(j1, j2):
    spins, j = [], abs(j1 - j2)
    while j <= j1 + j2:
        spins.append(j)
        j += 1
    return spins


CASIMIR_HALF = HALF * (HALF + 1)                               # j(j+1)=3/4
HAAR_W = Q(clebsch_gordan(HALF, Q(0)).count(Q(0)), 2)          # E[chi_1/2]/2 = 0
HAAR_W2 = Q(clebsch_gordan(HALF, HALF).count(Q(0)), 4)         # E[chi_1/2^2]/4 = 1/4
ALPHA_OVER_DELTA = Q(8)                                        # delta = alpha/8
ONSITE_GAP = ALPHA_OVER_DELTA * CASIMIR_HALF                   # Haar reference gap 6
FACE_LINKS = 4
FACE_ENERGY = ALPHA_OVER_DELTA * FACE_LINKS * CASIMIR_HALF     # 24 normalized
FACE_ENERGY_ALPHA = FACE_ENERGY / ALPHA_OVER_DELTA             # 3 in alpha units
FACE_NORM = HALF                                               # ||W_f Omega_0||
FACE_COEFF_NORMALIZED = Q(-1, 3)   # H/delta contains -(nu/delta) W_f = -(tau/3) W_f per unit tau
FACE_COEFF_ALPHA = Q(-1, 24)       # H/alpha contains -(tau/24) W_f per unit tau
COUPLING_PER_TAU = {'delta': abs(FACE_COEFF_NORMALIZED), 'alpha': abs(FACE_COEFF_ALPHA)}
ENERGY_BY_UNITS = {'delta': FACE_ENERGY, 'alpha': FACE_ENERGY_ALPHA}


def per_face_coefficient(abs_tau, coupling_units, energy_units):
    """Norm of H_M^{-1} P_M (coefficient * W_f) Omega_0 for one face (I1.5 convention)."""
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
ORIENT_AXES = {name: (a, c) for name, a, c in ORIENTATIONS}
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


def fine_is_selected(p, name):
    """I1 definition: selected xy faces have even y and x residues 0,1,2 modulo 4."""
    return name == 'xy' and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


def fine_face_classes():
    """Re-derive the 24 anchored face classes of one factor from pi and the link tails (I1.4)."""
    rows = []
    for r in range(4):
        for s in range(2):
            p = (r, s, 0)
            for name, a, c in ORIENTATIONS:
                owners = tuple(sorted({coarse(t) for t, _ in face_links(p, a, c)}))
                rows.append((name, r, s, owners, 'selected' if fine_is_selected(p, name) else 'omitted'))
    return sorted(rows)


# Explicit encoding of the I1 table (research/round21/forward/i1/report.md, section 3):
# orientation, r values, s values, class count, relative owner support, role.
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


CLASSES = []          # filled from the expanded I1 table: (name, r, s, support, role)


def face_base(anchor, k):
    name, r, s, _, _ = CLASSES[k]
    return (4 * anchor[0] + r, 2 * anchor[1] + s, anchor[2])


def face_label(anchor, k):
    name, r, s, _, role = CLASSES[k]
    p = face_base(anchor, k)
    return '%s[%s] r=%d s=%d anchor=(%d,%d,%d) base=(%d,%d,%d)' % (
        name, role[:3], r, s, anchor[0], anchor[1], anchor[2], p[0], p[1], p[2])


def face_link_set(anchor, k):
    name, _, _, _, _ = CLASSES[k]
    a, c = ORIENT_AXES[name]
    return frozenset(face_links(face_base(anchor, k), a, c))


def owner_set(anchor, k):
    return tuple(sorted(vadd(anchor, w) for w in CLASSES[k][3]))


def class_ids(role):
    return [k for k, row in enumerate(CLASSES) if row[4] == role]


class DerivedCount:
    __slots__ = ('value', 'provenance')

    def __init__(self, value, provenance):
        self.value = value
        self.provenance = provenance


PROVENANCE = 'I1_24_class_table_translation_covariance_all_sites'


def certified_count(obj, what):
    require(isinstance(obj, DerivedCount) and obj.provenance == PROVENANCE,
            what + ': count is hard-coded, copied, omitted-only or not derived from the 24-class I1 table at every site')
    return obj.value


def certify_site_scope(scope):
    require(scope == 'all_sites', 'anchored norm maximum restricted to %s; the fixed point needs every site' % scope)
    return scope


def certify_labelled_bound(value, derived_exact, label):
    require(label == 'labelled_bound', 'a %s count is used as an exact enumeration; it is only an anchor-group bound' % qs(value))
    require(Q(value) >= Q(derived_exact), 'labelled bound %s is below the exact count %s' % (qs(value), qs(derived_exact)))
    return Q(value)


def certify_anchor_set(anchors):
    expected = sorted({vsub(u, v) for u in COVER for v in STAR})
    require(sorted(anchors) == expected,
            'incident anchors %d differ from the complete R-S (%d); incoming stars missing' % (len(anchors), len(expected)))
    return anchors


W_LINKS = (((0, 0, 0), 0), ((1, 0, 0), 2), ((0, 0, 1), 0), ((0, 0, 0), 2))


def certify_cover(cover):
    owners = {coarse(t) for t, _ in W_LINKS}
    require(owners <= set(cover), 'cover misses an owner of a link of the original xz Wilson loop')
    require(set(cover) == owners, 'cover is not the complete factor cover R={0,e_z} of W')
    return tuple(sorted(cover))


def factor_links(b):
    links = []
    for r in range(4):
        for s in range(2):
            t = (4 * b[0] + r, 2 * b[1] + s, b[2])
            for d in range(3):
                links.append((t, d))
    return links


# ------------------------------------------------ route-B grouping and boxes
# A grouping rule maps each anchor b to a list of (kind, support offsets, class ids).
GROUPINGS = ('route_B', 'selected_in_star', 'zero_selected', 'double_count', 'per_face')


def groups_at_anchor(rule):
    omitted, selected = class_ids('omitted'), class_ids('selected')
    if rule == 'route_B':
        return [('whole_star', STAR, omitted), ('single_factor', (ORIGIN,), selected)]
    if rule == 'selected_in_star':
        return [('whole_star', STAR, omitted + selected)]
    if rule == 'zero_selected':
        return [('whole_star', STAR, omitted)]
    if rule == 'double_count':
        return [('whole_star', STAR, omitted + selected), ('single_factor', (ORIGIN,), selected)]
    if rule == 'per_face':
        return [('face', CLASSES[k][3], [k]) for k in omitted + selected]
    raise Rejected('unknown grouping rule ' + repr(rule))


def box_groups(N, rule):
    """Retained groups of a centred box [-N,N]^3: a group is kept iff its support lies in the box."""
    rng = range(-N, N + 1)
    sites = [(x, y, z) for x in rng for y in rng for z in rng]
    siteset = set(sites)
    groups = []
    for b in sites:
        for kind, support, ks in groups_at_anchor(rule):
            sup = tuple(sorted(vadd(b, v) for v in support))
            if all(u in siteset for u in sup):
                groups.append({'kind': kind, 'anchor': b, 'support': sup, 'faces': [(b, k) for k in ks]})
    return sites, groups


def group_norm_per_tau(group):
    """Triangle-inequality norm of -(tau/3) sum_f W_f per unit |tau| (normalized units)."""
    return Q(len(group['faces']), 3)


def per_site_sums(sites, groups):
    sums = dict.fromkeys(sites, Q(0))
    for g in groups:
        for u in g['support']:
            sums[u] += group_norm_per_tau(g)
    return sums


def per_site_face_counts(sites, groups):
    counts = dict.fromkeys(sites, 0)
    for g in groups:
        for b, k in g['faces']:
            for u in owner_set(b, k):
                if u in counts:
                    counts[u] += 1
    return counts


def bulk_per_site_sum(rule):
    sites, groups = box_groups(3, rule)
    sums = per_site_sums(sites, groups)
    return max(sums.values()), sums[ORIGIN]


def certify_no_double_count(groups):
    seen = {}
    for g in groups:
        for f in g['faces']:
            require(f not in seen, 'face %s charged twice (%s and %s)' % (face_label(*f), seen.get(f), g['kind'] + '@' + str(g['anchor'])))
            seen[f] = g['kind'] + '@' + str(g['anchor'])
    return len(seen)


def certify_per_site_sum(claimed_units, rule, derived_route_b):
    require(rule == 'route_B', 'grouping %s is not route B (whole stars of the 21 omitted classes plus one single-factor group of the three selected faces)' % rule)
    require(Q(claimed_units) == Q(derived_route_b),
            "per-site sum %s|tau| differs from the recomputed route-B value %s|tau|" % (qs(claimed_units), qs(derived_route_b)))
    return Q(claimed_units)


# ------------------------------------------------------------ AM2 constants
R_RADIUS = Q(1, 64)
G_R_UP = Q(148, 7)
GP_R_UP = Q(352)
MAX_SUPPORT = 4


def am2_enclosures():
    e_lo, e_hi = exp_bounds(8 * R_RADIUS)
    return {
        'exp_one_eighth': (e_lo, e_hi),
        'G': (16 * e_lo * (1 + 10 * R_RADIUS), 16 * e_hi * (1 + 10 * R_RADIUS)),
        'G_prime': (16 * e_lo * (18 + 80 * R_RADIUS), 16 * e_hi * (18 + 80 * R_RADIUS)),
    }


def G_upper(t):
    _, e_hi = exp_bounds(ceil_to(8 * t))
    return 16 * e_hi * (1 + 10 * t)


def lk_num(k, p=MAX_SUPPORT):
    """AM2 anchored coefficient 2^p (2p)^k (1 + k(p+1)/p); p=4 gives 16*8^k(1+5k/4)."""
    return Q(2 ** p * (2 * p) ** k) * (1 + Q(k * (p + 1), p))


TAU_CAP = None
J_PER_TAU = None      # route-B per-site sum per |tau| (derived, 29)
J0_PRIME = None       # contract R1 re-freeze (read, then validated)


def validate_j0_resolution(res, j_per_tau, cap):
    """R1: J_0' >= J' at the cap with the two exact AM2 contraction inequalities."""
    require(isinstance(res, dict), 'J_0 resolution missing')
    require(res.get('label') == 'R1', 'J_0 resolution %r is not the contract R1 re-freeze' % res.get('label'))
    require(Q(res.get('cap')) == cap, 'resolution changes the coupling cap (%s): a changed coupling, not the contract model' % qs(res.get('cap')))
    j0 = Q(res.get('J0'))
    require(j_per_tau * cap <= j0,
            'J_0=%s is exceeded by the route-B per-site sum %s at the cap' % (qs(j0), qs(j_per_tau * cap)))
    require('self_map' in res and 'contraction' in res, 'the two exact contraction inequalities are not both declared')
    require(Q(res['self_map']) == j0 * G_R_UP and Q(res['self_map']) < R_RADIUS,
            'declared self-map value %s is not J_0*148/7 below 1/64' % qs(res['self_map']))
    require(Q(res['contraction']) == 2 * j0 * GP_R_UP and Q(res['contraction']) < 1,
            'declared contraction value %s is not 2*J_0*352 below 1' % qs(res['contraction']))
    return j0


def certify_am2_reuse(record_):
    """Hypotheses under which the AM2 fixed point, exclusion and cutoff passage re-apply."""
    require(isinstance(record_, dict), 'no AM2 re-use justification')
    route = record_.get('route')
    require(route in ('A', 'B'), 'AM2 re-use without a declared reference route')
    require(Q(record_['onsite_lower_gap']) >= 1, 'on-site operator lacks h_x>=Q_x (gap %s<1)' % qs(record_['onsite_lower_gap']))
    require(record_['max_support'] <= MAX_SUPPORT, 'maximal interaction support %d>4 changes L_k and G' % record_['max_support'])
    require(record_['termination_order'] == 2 * record_['max_support'],
            'nested-commutator termination %d is not 2*(max support)' % record_['termination_order'])
    cap = Q(record_['cap'])
    j = Q(record_['J_per_tau']) * cap
    j0 = Q(record_['J0'])
    require(j <= j0, 'per-site sum %s at the cap exceeds the cited J_0=%s: the AM2 theorem does not apply as cited' % (qs(j), qs(j0)))
    require(j0 * G_R_UP < R_RADIUS and 2 * j0 * GP_R_UP < 1, 'contraction fails at the cited J_0')
    if route == 'B':
        require(record_['reference'] == 'haar' and Q(record_['J_per_tau']) == J_PER_TAU,
                'route B needs the Haar reference and the recomputed per-site sum %s|tau|' % qs(J_PER_TAU))
    else:
        require(record_['reference'] == 'selected_strip' and Q(record_['J_per_tau']) == 28,
                'route A needs the selected-strip reference (inherited A1 strip theorem) and J=28|tau|')
    return True


# ------------------------------------------------ dictionary, box, label, route
def g4_from_tau(tau):
    return Q(96) / abs(Q(tau))


def uniform_triple(tau):
    t = Q(tau)
    return (t / 24, t / 24, t / 24)


def certify_uniform_triple_in_box(triple, tau, end_bound, bridge_bound):
    require(len(triple) == 3, 'selected triple must have three entries')
    t = parse_q(tau)
    tri = tuple(parse_q(x) for x in triple)
    require(tri == uniform_triple(t), 'selected triple %s is not the uniform value tau/24 on every selected face' % str([qs(x) for x in tri]))
    require(abs(tri[0]) <= end_bound and abs(tri[2]) <= end_bound, 'end coefficients leave the admitted box |lambda|<=alpha/2')
    require(abs(tri[1]) <= bridge_bound, 'bridge coefficient %s leaves the admitted box |mu|<=alpha/8' % qs(tri[1]))
    require(abs(t) <= TAU_CAP, 'coupling outside the AM2/AQ cap: not certified here (not a gap failure)')
    return tri


def certify_label(label, g4, tau):
    low = label.lower()
    require('weak coupling' not in low and 'weak-coupling' not in low, 'label claims weak coupling')
    require('continuum' not in low, 'label claims a continuum statement')
    require(label == LABEL, 'label %r is not the contract label %r' % (label, LABEL))
    require(Q(g4) == g4_from_tau(tau), 'g^4=%s does not follow from the AL1 dictionary tau=96/g^4 (%s)' % (qs(g4), qs(g4_from_tau(tau))))
    return label


def certify_route(packet):
    require(isinstance(packet, dict) and packet.get('route') in ('A', 'B'), 'reference route not declared')
    if packet['route'] == 'B':
        require(packet.get('reference') == 'haar', 'route B requires the Haar product reference')
        require(packet.get('onsite') == 'casimir_only', 'route B on-site operator must be 8*sum C_e only')
        require(packet.get('selected_faces_in') == 'interaction', 'route B moves the selected faces into the interaction')
        require(packet.get('groups') == ['single_factor', 'whole_star'], 'route B groups are whole stars plus single-factor groups')
    else:
        require(packet.get('reference') == 'selected_strip', 'route A keeps the selected faces on site: its reference is the selected strip, not Haar')
        require(packet.get('selected_faces_in') == 'onsite', 'route A keeps the selected faces on site')
    return packet['route']


def onsite_trial_energy(k):
    """Normalized trial (Omega + t W Omega), t=k/24, for h = 8 sum C_e - k W on one selected face."""
    t = k / 24
    num = t * t * FACE_ENERGY * HAAR_W2 - 2 * k * t * HAAR_W2
    return num, num / (1 + t * t * HAAR_W2)


def certify_haar_is_onsite_ground(route, tau):
    """Claim: the constant Haar vector is the on-site ground of the declared route."""
    if route == 'B':
        return True        # h_b = 8 sum C_e >= 0 with kernel the constants
    k = abs(FACE_COEFF_NORMALIZED) * Q(tau)
    _, e = onsite_trial_energy(k)
    require(not (e < 0), 'route A on-site operator has a trial of energy %s<0 below the Haar vector: Haar is not its ground' % qs(e))
    return True


def certify_sign_convention(omitted_per_tau, selected_per_tau):
    require(Q(omitted_per_tau) == FACE_COEFF_NORMALIZED, 'omitted faces do not enter as -(tau/3) W_f (I1.5)')
    require(Q(selected_per_tau) == FACE_COEFF_NORMALIZED,
            'selected faces enter as %s*tau*W_f, not with the same sign and magnitude -(tau/3) as the omitted faces (mixed convention)' % qs(selected_per_tau))
    return True


# ------------------------------------------------------ reset and incidence
def certify_reset(claimed_budget, claimed_eps, gap, derived_budget):
    require(Q(claimed_budget) == Q(derived_budget),
            'reset budget %s|tau| differs from 2*(sum of the norms of all groups meeting R)=%s|tau|' % (qs(claimed_budget), qs(derived_budget)))
    require(Q(gap) == ONSITE_GAP, 'reset overlap divides by gap %s, not the Haar reference gap 6 (h_R>=6(I-P_R))' % qs(gap))
    require(Q(claimed_eps) == Q(derived_budget) / ONSITE_GAP, 'epsilon_R %s|tau| is not budget/6' % qs(claimed_eps))
    return Q(claimed_eps)


def incidence_rows(groups_meeting, meeting_faces):
    rows = []
    for g in groups_meeting:
        faces = sorted(g['faces'])
        rows.append({'kind': g['kind'], 'anchor': g['anchor'], 'support': g['support'], 'faces': faces,
                     'faces_owning_link_in_R': sum(1 for f in faces if f in meeting_faces),
                     'faces_inside_R': sum(1 for f in faces if set(owner_set(*f)) <= set(COVER))})
    return rows


def certify_incidence_table(table, meeting_faces):
    require(isinstance(table, list) and len(table) > 0
            and all(isinstance(r, dict) and isinstance(r.get('faces'), list) and len(r['faces']) > 0 for r in table),
            'incidence counts asserted without an itemized face table')
    seen = {}
    for row in table:
        for f in row['faces']:
            require(f not in seen, 'face %s is charged twice in the incidence table' % face_label(*f))
            seen[f] = row['kind']
    missing = sorted(set(meeting_faces) - set(seen))
    require(not missing, '%d faces owning a link in R are not charged to any group meeting R' % len(missing))
    stars = sum(1 for r in table if r['kind'] == 'whole_star')
    singles = sum(1 for r in table if r['kind'] == 'single_factor')
    require(stars + singles == len(table), 'unknown group kind in the incidence table')
    selected_faces = sum(len(r['faces']) for r in table if r['kind'] == 'single_factor')
    norm_alpha = sum((Q(len(r['faces']), 3) / ALPHA_OVER_DELTA for r in table), Q(0))
    return {'stars': stars, 'single_factor_groups': singles, 'selected_faces': selected_faces,
            'faces_charged': len(seen), 'faces_owning_link_in_R': sum(r['faces_owning_link_in_R'] for r in table),
            'B_N_alpha_units_per_tau': norm_alpha, 'k_prime_per_tau': 2 * norm_alpha}


def certify_selected_incidence(groups, faces, derived_groups, derived_faces):
    require(groups == derived_groups, '%d single-factor selected groups claimed to meet R; the itemized table has %d' % (groups, derived_groups))
    require(faces == derived_faces, '%d selected faces claimed inside R; the itemized table has %d' % (faces, derived_faces))
    return True


def certify_duhamel_slope(k_per_tau, units, derived_alpha):
    require(units == 'alpha', 'Duhamel slope stated in %s units; the clock theta=alpha t/hbar needs G=H/alpha units' % units)
    require(Q(k_per_tau) == Q(derived_alpha), "slope %s|tau| differs from k'=2||B_N||=%s|tau| (G=H/alpha)" % (qs(k_per_tau), qs(derived_alpha)))
    return True


# ------------------------------------------------------------- tiers (AV1)
class Term:
    __slots__ = ('name', 'value', 'tier', 'provenance')

    def __init__(self, name, value, tier, provenance):
        self.name = name
        self.value = Q(value)
        self.tier = tier
        self.provenance = provenance


A1_PROVENANCES = ('exact_first_order', 'two_site_anchored', 'labelled_bound', 'owner_set_orthogonal')


def assemble_epsilon(tier, terms):
    require(tier in ('i', 'ii'), 'unknown tier')
    for name, term in sorted(terms.items()):
        require(term.tier == tier, 'tier mixing: term %s is tier (%s) inside tier (%s)' % (name, term.tier, tier))
    if tier == 'i':
        require(sorted(terms) == ['t'], 'tier (i) uses only the crude anchored norm t')
        require(terms['t'].provenance in ('am2_majorant', 'am2_majorant_iterated'), 'tier (i) t must come from the AM2 majorant')
        t = terms['t'].value
        return 2 * t + t * t
    require(sorted(terms) == ['T', 'a1', 'rho'], 'tier (ii) needs a1, rho and T')
    require(terms['a1'].provenance in A1_PROVENANCES, 'tier (ii) a1 must be a first-order collection bound')
    require(terms['T'].provenance == 'self_consistent', "tier (ii) t must come from t<=t1/(1-352J')")
    require(terms['rho'].provenance == 'self_consistent_remainder', 'tier (ii) remainder must use the self-consistent t')
    return terms['a1'].value + 2 * terms['rho'].value + terms['T'].value ** 2


def fidelity_forms(eps):
    """Reverse route D(eps)=2eps/sqrt(1+eps^2): exact rational 2eps, directed 1e-40 value, density form."""
    eps = Q(eps)
    if eps == 0:
        return Q(0), Q(0), Q(0)
    lo, _ = sqrt_bounds(1 + eps * eps)
    return 2 * eps, ceil_to(2 * eps / lo), 2 * eps * (1 + eps) / (1 + eps * eps)


COUNTS = {}


def certify_model(tau, triple=None):
    t = parse_q(tau)
    tri = uniform_triple(t) if triple is None else tuple(parse_q(x) for x in triple)
    require(len(tri) == 3 and tri == uniform_triple(t),
            'selected triple %s is not tied to tau (a changed model, not the uniform model)' % str([qs(x) for x in tri]))
    require(abs(t) <= TAU_CAP, 'coupling outside the AX1 cap: not certified here (not a gap failure)')
    return t


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
    d2, dfid, dden = fidelity_forms(eps)
    return {'tier': 'i', 'variant': 'iterated_%d' % iterate if iterate else "crude_J'G(R)",
            'tau': qs(t_signed), 'J_prime_upper': qs(J), 't_upper': qs(t), 't_iterates': steps,
            'epsilon': qs(eps), 'D_exact_2eps': qs(d2), 'D_fidelity_directed_1e-40': qs(dfid),
            'D_density_form_exact': qs(dden), 'D_preview': sci(d2), 'epsilon_preview': sci(eps),
            '_D': d2, '_eps': eps}


def tier_ii(tau, variant='exact_counts'):
    t_signed = certify_model(tau)
    a = abs(t_signed)
    J = J_PER_TAU * a
    K = GP_R_UP * J
    require(K < 1, "self-consistent factor 352J' must be below one")
    coeff = per_face_coefficient(a, 'delta', 'delta')
    if variant in ('exact_counts', 'global_two_site', 'directed_remainder'):
        t1 = coeff * certified_count(COUNTS['faces_per_factor'], 'faces per factor')
        a1 = coeff * certified_count(COUNTS['faces_meeting_R'], 'faces meeting R')
        a1_prov = 'exact_first_order'
    elif variant == 'labelled_bound_96_168':
        t1 = coeff * certify_labelled_bound(COUNTS['bound_per_factor'], COUNTS['faces_per_factor'].value, 'labelled_bound')
        a1 = coeff * certify_labelled_bound(COUNTS['bound_R'], COUNTS['faces_meeting_R'].value, 'labelled_bound')
        a1_prov = 'labelled_bound'
    elif variant == 'owner_set_orthogonal':
        t1 = coeff * COUNTS['orth_site_sum_hi']
        a1 = coeff * COUNTS['orth_meeting_R_hi']
        a1_prov = 'owner_set_orthogonal'
    else:
        raise Rejected('unknown tier (ii) variant')
    T = t1 / (1 - K)
    must(T <= R_RADIUS, 'self-consistent t must stay inside the AM2 ball')
    rho = ceil_to(J * (G_upper(T) - 16)) if variant == 'directed_remainder' else K * T
    must(a == 0 or rho > 0, 'the remainder bound is never zero at nonzero coupling')
    if variant == 'global_two_site':
        a1, a1_prov = 2 * t1, 'two_site_anchored'
    eps = assemble_epsilon('ii', {'a1': Term('a1', a1, 'ii', a1_prov),
                                  'rho': Term('rho', rho, 'ii', 'self_consistent_remainder'),
                                  'T': Term('T', T, 'ii', 'self_consistent')})
    d2, dfid, dden = fidelity_forms(eps)
    return {'tier': 'ii', 'variant': variant, 'tau': qs(t_signed), 'J_prime_upper': qs(J), 'factor_352J_prime': qs(K),
            'per_face_coefficient': qs(coeff), 't1_first_order_anchored': qs(t1), 'T_self_consistent': qs(T),
            'remainder_anchored_upper_rho': qs(rho), 'a1_first_order_meeting_R': qs(a1), 'a1_provenance': a1_prov,
            'two_creation_term': qs(T * T), 'epsilon': qs(eps), 'D_exact_2eps': qs(d2),
            'D_fidelity_directed_1e-40': qs(dfid), 'D_density_form_exact': qs(dden),
            'D_preview': sci(d2), 'epsilon_preview': sci(eps), '_D': d2, '_eps': eps,
            '_parts': {'a1': a1, 'rho': rho, 'T': T}}


def strip(d):
    return {k: v for k, v in d.items() if not k.startswith('_')}


def certify_t1_over_coefficient(value, exact_lower):
    require(Q(value) >= exact_lower,
            'claimed first-order anchored norm %s|tau|/144 is below the exact global value (>= %s|tau|/144): root-n misuse' % (sci(value, 8), sci(exact_lower, 8)))
    return Q(value)


def admit_bound(value, target):
    require(isinstance(value, Q) and isinstance(target, Q), 'admission requires exact rationals, not floating values')
    return value <= target


def centered_variance_lower(D, charge_mean_square):
    return floor_to(Q(1, 4) - D / 2 - (D * D if charge_mean_square else 0))


def certify_variance_lower(claimed, D):
    worst = Q(1, 4) - D / 2 - D * D
    require(Q(claimed) <= worst, 'variance lower bound %s omits the mean-square charge m^2<=D^2' % sci(claimed, 12))
    return True


def certify_mean_budget(first_order_abs, budget):
    require(Q(first_order_abs) <= Q(budget), 'mean budget %s is below the first-order Wilson mean |tau|/144=%s' % (sci(budget, 6), sci(first_order_abs, 6)))
    return True


def certify_linear_scaling(bracket):
    require(Q(99) <= bracket[0] and bracket[1] <= Q(101),
            'D(tau)/D(tau/100) in [%s,%s] is not linear scaling [99,101]' % (sci(bracket[0], 6), sci(bracket[1], 6)))
    return True


# --------------------------------------------------------- AX2 feasibility
PI_LO, PI_HI = None, None


def ax2_feasible(D, relation, cap):
    coeff, e2 = relation[0], relation[1]
    D = Q(D)
    return 2 * (D + D * D) + coeff * cap / PI_LO <= Q(1, 10 ** e2)


def certify_ax2_threshold(D, relation, cap):
    require(ax2_feasible(D, relation, cap), "D'=%s violates the AX2 window relation 2(D'+D'^2)+51|tau|/pi<=1e-6" % sci(D, 6))
    return True


def ax2_threshold_bracket(relation, cap):
    coeff, e2 = relation[0], relation[1]
    x_lo = Q(1, 10 ** e2) - coeff * cap / PI_LO
    x_hi = Q(1, 10 ** e2) - coeff * cap / PI_HI
    lo = (sqrt_bounds(1 + 2 * x_lo)[0] - 1) / 2
    hi = (sqrt_bounds(1 + 2 * x_hi)[1] - 1) / 2
    return floor_to(lo), ceil_to(hi)


# ------------------------------------------------------------ outcome/flags
def producer_outcome(grouping_ok, contraction_ok, checklist_unproved, incidence_itemized, tier_ii_available,
                     D_plus, D_minus, target):
    if not (grouping_ok and contraction_ok):
        return 'insufficient'
    if checklist_unproved or not incidence_itemized or not tier_ii_available:
        return 'limited'
    if Q(D_plus) > Q(target) or Q(D_minus) > Q(target):
        return 'limited'
    return 'accepted_within_scope'


def certify_outcome(recorded, inputs):
    computed = producer_outcome(**inputs)
    require(recorded == computed, 'recorded outcome %s differs from the evidence-derived outcome %s' % (recorded, computed))
    return computed


def validate_claims(flags, label):
    require(sorted(flags) == sorted(CLAIM_FLAGS), 'claim flag set changed')
    for key in ('continuum_claim', 'weak_coupling_claim', 'resolved_interaction_shift',
                'scientific_priority_verified', 'euclidean_node_certified'):
        require(flags[key] is False, 'claim flag %s must be false in AX1' % key)
    require(flags['uniform_wilson_claim'] is True and label == LABEL,
            'uniform_wilson_claim is admitted only for the fixed-spacing model with the label %r' % LABEL)
    return True


# ------------------------------------------- termination-order qubit fixture
def mat_zero(n):
    return [[Q(0)] * n for _ in range(n)]


def mat_mul(a, b):
    n = len(a)
    out = mat_zero(n)
    for i in range(n):
        ai = a[i]
        for k in range(n):
            if ai[k] != 0:
                bk = b[k]
                for j in range(n):
                    if bk[j] != 0:
                        out[i][j] += ai[k] * bk[j]
    return out


def mat_sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mat_add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def is_zero(a):
    return all(x == 0 for row in a for x in row)


def site_op(nq, i, kind):
    """kind 'plus': |1><0| at qubit i (an AM2 creation); 'x': bit flip at qubit i."""
    dim = 1 << nq
    m = mat_zero(dim)
    for s in range(dim):
        bit = (s >> i) & 1
        if kind == 'plus' and bit == 0:
            m[s | (1 << i)][s] = Q(1)
        elif kind == 'x':
            m[s ^ (1 << i)][s] = Q(1)
    return m


def termination_fixture():
    nq = 4
    C = mat_zero(1 << nq)
    for i in range(nq):
        C = mat_add(C, site_op(nq, i, 'plus'))
    star = site_op(nq, 0, 'x')
    for i in range(1, nq):
        star = mat_mul(star, site_op(nq, i, 'x'))
    single = site_op(nq, 0, 'x')

    def ad_powers(V, kmax):
        out = [V]
        for _ in range(kmax):
            V = mat_sub(mat_mul(C, V), mat_mul(V, C))
            out.append(V)
        return out

    sp = ad_powers(star, 9)
    gp = ad_powers(single, 3)
    both = ad_powers(mat_add(star, single), 9)
    vac = 0
    full = (1 << nq) - 1
    return {'star_ad8_vacuum_to_1111': qs(sp[8][full][vac]), 'star_ad9_zero': is_zero(sp[9]),
            'star_ad8_nonzero': not is_zero(sp[8]), 'single_ad2_nonzero': not is_zero(gp[2]),
            'single_ad3_zero': is_zero(gp[3]), 'sum_ad9_zero': is_zero(both[9]),
            'eight_factorial': factorial(8)}


# ------------------------------------- exact one-plaquette field Q(sqrt(d))
class QS:
    """a + b*sqrt(d) with rational a, b and a fixed positive rational d."""
    __slots__ = ('a', 'b', 'd')

    def __init__(self, a, b, d):
        self.a, self.b, self.d = Q(a), Q(b), Q(d)

    def _c(self, o):
        if isinstance(o, QS):
            must(o.d == self.d, 'mixed quadratic fields')
            return o
        return QS(o, 0, self.d)

    def __add__(self, o):
        o = self._c(o)
        return QS(self.a + o.a, self.b + o.b, self.d)

    def __sub__(self, o):
        o = self._c(o)
        return QS(self.a - o.a, self.b - o.b, self.d)

    def __mul__(self, o):
        o = self._c(o)
        return QS(self.a * o.a + self.b * o.b * self.d, self.a * o.b + self.b * o.a, self.d)

    def __neg__(self):
        return QS(-self.a, -self.b, self.d)

    def inv(self):
        n = self.a * self.a - self.b * self.b * self.d
        must(n != 0, 'division by zero in Q(sqrt d)')
        return QS(self.a / n, -self.b / n, self.d)

    def __truediv__(self, o):
        return self * self._c(o).inv()

    def eq(self, o):
        o = self._c(o)
        return self.a == o.a and self.b == o.b

    def sign(self):
        """Exact sign of a + b sqrt(d)."""
        sa = (self.a > 0) - (self.a < 0)
        sb = (self.b > 0) - (self.b < 0)
        if sb == 0:
            return sa
        if sa == 0:
            return sb
        if sa == sb:
            return sa
        diff = self.a * self.a - self.b * self.b * self.d
        if diff == 0:
            return 0
        return sa if diff > 0 else sb

    def text(self):
        return '%s + %s*sqrt(%s)' % (qs(self.a), qs(self.b), qs(self.d))


def quad_equal(x, y):
    """Exact equality of b*sqrt(d) and b'*sqrt(d') (pure surds) or of two elements of one field."""
    if x.d == y.d:
        return x.eq(y)
    must(x.a == 0 and y.a == 0, 'cross-field comparison only for pure surds')
    return ((x.b > 0) == (y.b > 0)) and ((x.b < 0) == (y.b < 0)) and x.b * x.b * x.d == y.b * y.b * y.d


def plaquette_mean(k):
    """Ground mean of W for h = diag(0,24) - k W on the j<=1/2 gauge-invariant plaquette space.

    W chi_0 = chi_1/2 / 2 and the truncated W is [[0,1/2],[1/2,0]] in (chi_0, chi_1/2).
    A finite graph (transfers_to_aq false); used for the sign and kappa-tying demonstrations.
    """
    k = Q(k)
    if k == 0:
        return QS(0, 0, 1)
    d = 144 + k * k / 4
    s = QS(0, 1, d)
    lam = QS(12, 0, d) - s                    # lower eigenvalue 12 - sqrt(144 + k^2/4)
    v0, v1 = QS(k / 2, 0, d), -lam
    must((v1 * (-k / 2)).eq(lam * v0) and (v0 * (-k / 2) + v1 * 24).eq(lam * v1), 'eigenvector identity')
    must(lam.sign() <= 0, 'ground energy is nonpositive')
    mean = (v0 * v1) / (v0 * v0 + v1 * v1)
    must((mean * mean).b == 0 and (mean * mean).a == k * k / (16 * d), '<W>^2 = k^2/(16 d)')
    return mean


KAPPA_RULES = {
    'tied_tau_over_24': lambda t: t / 24,
    'absolute_value': lambda t: abs(t) / 24,
    'offset': lambda t: t / 24 + Q(1, 7),
    'double': lambda t: t / 12,
    'zero_selected': lambda t: Q(0),
}


def selected_mean(rule, tau):
    return plaquette_mean(ALPHA_OVER_DELTA * KAPPA_RULES[rule](Q(tau)))


# ------------------------------------------------------ link-flip set E
def in_flip_set(link):
    """E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even} (AW1-admitted)."""
    p, d = link
    return p[(d + 1) % 3] % 2 == 0


def flip_count(links):
    return sum(1 for l in links if in_flip_set(l))


def hamiltonian_coefficients(groups, tau, rule):
    """Face -> coefficient of W_f in H/delta; selected faces carry -8*kappa(tau)."""
    coeffs = {}
    for g in groups:
        for b, k in g['faces']:
            if CLASSES[k][4] == 'omitted':
                c = FACE_COEFF_NORMALIZED * Q(tau)
            else:
                c = -ALPHA_OVER_DELTA * KAPPA_RULES[rule](Q(tau))
            must((b, k) not in coeffs, 'face charged twice in the Hamiltonian')
            coeffs[(b, k)] = c
    return coeffs


def flip_image(coeffs):
    return {f: c * (-1) ** flip_count(face_link_set(*f)) for f, c in coeffs.items()}


FLIP_GROUPS = None


def certify_uniform_antisymmetry(rule, tau):
    """Uniform flip identity U_E H(tau) U_E^* = H(-tau) with every face tied to tau."""
    t = Q(tau)
    image = flip_image(hamiltonian_coefficients(FLIP_GROUPS, t, rule))
    target = hamiltonian_coefficients(FLIP_GROUPS, -t, rule)
    require(image == target, 'U_E H(tau) U_E^* differs from H(-tau) under rule %s (kappa(tau)=%s, kappa(-tau)=%s): the uniform flip identity breaks'
            % (rule, qs(KAPPA_RULES[rule](t)), qs(KAPPA_RULES[rule](-t))))
    require(KAPPA_RULES[rule](t) == t / 24 and KAPPA_RULES[rule](-t) == -t / 24,
            'flip identity holds but kappa(tau)=%s, kappa(-tau)=%s under rule %s is not nu=alpha*tau/24: odd but not the uniform model'
            % (qs(KAPPA_RULES[rule](t)), qs(KAPPA_RULES[rule](-t)), rule))
    return True


# ------------------------------------------------------------ contract
def parse_contract(data):
    p = data['parameters']
    out = {}
    out['tau_cap'] = parse_q(p['tau_cap'])
    m = re.fullmatch(r'tau/(\d+) for each selected face \(box check \|tau\|/(\d+)<=1/(\d+) and <=1/(\d+)\)',
                     p['uniform_selected_coefficient_over_alpha'])
    require(m is not None, 'uniform selected coefficient text not parsed')
    out['selected_over'] = int(m.group(1))
    out['box_over'] = int(m.group(2))
    out['bridge_bound'] = Q(1, int(m.group(3)))
    out['end_bound'] = Q(1, int(m.group(4)))
    m = re.fullmatch(r'(\d+)\|tau\| \((\d+) from four anchor stars \+ (\d+) from the single-factor group\)', p['per_site_sum_J_prime'])
    require(m is not None, 'per-site sum text not parsed')
    out['J_prime'] = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"R1: re-freeze J_0'=(\d+)/10\^(\d+) with exact contraction checks J_0'\*(\d+)/(\d+)=(\d+)/(\d+)<1/(\d+) "
                     r"and 2\*J_0'\*(\d+)=(\d+)/(\d+)<(\d+) \(alternative R2: cap \|tau\|<=(\d+)/(\d+) is a changed coupling and is not selected\)",
                     p['J0_resolution'])
    require(m is not None, 'J_0 resolution text not parsed')
    g = [int(x) for x in m.groups()]
    out['J0_prime'] = Q(g[0], 10 ** g[1])
    out['G_R_text'] = Q(g[2], g[3])
    out['self_map_text'] = Q(g[4], g[5])
    out['radius_text'] = Q(1, g[6])
    out['GP_R_text'] = Q(g[7])
    out['contraction_text'] = Q(g[8], g[9])
    out['contraction_bound_text'] = Q(g[10])
    out['R2_cap'] = Q(g[11], g[12])
    m = re.fullmatch(r'omega\(h_R\)<=2\((\d+)\*(\d+)\|tau\|\+(\d+)\|tau\|\)=(\d+)\|tau\|, epsilon_R<=(\d+)\|tau\| \(square-root control only\)',
                     p['reset_budget'])
    require(m is not None, 'reset budget text not parsed')
    out['reset'] = tuple(int(x) for x in m.groups())
    words = {'two': 2, 'six': 6, 'seven': 7, 'three': 3, 'one': 1, 'zero': 0}
    m = re.fullmatch(r"exactly (\w+) single-factor selected groups \((\w+) faces\) meet R; \|\|B_N\|\|<=(\d+)\|tau\|/(\d+)\+(\d+)\|tau\|/(\d+)=(\d+)\|tau\|/(\d+), k'=(\d+)\|tau\|/(\d+)",
                     p['incidence'])
    require(m is not None and m.group(1) in words and m.group(2) in words, 'incidence text not parsed')
    out['incidence'] = (words[m.group(1)], words[m.group(2)], Q(int(m.group(3)), int(m.group(4))),
                        Q(int(m.group(5)), int(m.group(6))), Q(int(m.group(7)), int(m.group(8))), Q(int(m.group(9)), int(m.group(10))))
    m = re.fullmatch(r'faces owning a link of a factor bounded by (\d+) \(four anchors times (\d+)\) and (\d+) for R; '
                     r'omega\(W\)\^\{\(1\)\}=\+-\|tau\|/(\d+) unchanged; parity rule unchanged', p['first_order_faces'])
    require(m is not None, 'first-order faces text not parsed')
    out['first_order'] = tuple(int(x) for x in m.groups())
    m = re.fullmatch(r'tau=(\d+)/g\^4; at the cap g\^4=(\d+)\.(\d+)x10\^(\d+)', p['dictionary'])
    require(m is not None, 'dictionary text not parsed')
    out['dictionary_numerator'] = int(m.group(1))
    out['g4_cap_text'] = Q(int(m.group(2) + m.group(3)), 10 ** len(m.group(3))) * 10 ** int(m.group(4))
    m = re.search(r"2\(D'\+D'\^2\)\+(\d+)\|tau\|/pi<=10\^-(\d+), i\.e\. D'<=(\d+)\.(\d+)x10\^-(\d+)", p['d_prime_note'])
    require(m is not None, 'AX2 relation text not parsed')
    out['ax2_relation'] = (int(m.group(1)), int(m.group(2)))
    out['ax2_stated_threshold'] = Q(int(m.group(3) + m.group(4)), 10 ** len(m.group(4))) / 10 ** int(m.group(5))
    pre = data['preregistration']
    out['target'] = parse_q(pre['target']['value'])
    out['target_quantity'] = pre['target']['quantity']
    out['target_comparator'] = pre['target']['comparator']
    ref = re.fullmatch(r'(\d+) and (\d+/\d+)', pre['observable']['reference_value_exact'])
    require(ref is not None, 'reference values not parsed')
    out['reference'] = (parse_q(ref.group(1)), parse_q(ref.group(2)))
    out['reference_route'] = pre['observable']['reference_route']
    out['selected_triple_text'] = list(pre['selected_triple_alpha_units'])
    out['model_id'] = pre['model_id']
    out['tau_prereg'] = parse_q(pre['tau']['value'])
    out['signs'] = list(p['signs'])
    return out


def validate_contract(data, derived):
    require(data.get('id') == 'AX1' and data.get('status') == 'frozen_before_production', 'contract identity or status')
    require(data.get('reverse_premise_isolation') is True, 'reverse premise isolation flag')
    ids = data['controls']
    require(ids == data['preregistration']['controls_required']['ids'] and len(set(ids)) == len(ids),
            'controls list differs from the preregistered control ids')
    c = parse_contract(data)
    require(c['tau_cap'] == derived['cap'] and c['tau_prereg'] == derived['cap'], 'contract tau cap differs from the admitted AM2 cap')
    require(c['signs'] == ['+', '-'] and data['preregistration']['tau']['signs_evaluated'] == ['+', '-'], 'both signs must be evaluated')
    require(c['model_id'] == 'AQ_uniform_routeB' and c['reference_route'] == 'haar', 'model id or reference route is not the route-B Haar model')
    require(c['selected_triple_text'] == ['tau/%d' % derived['selected_over']] * 3 and c['selected_over'] == derived['selected_over']
            and c['box_over'] == derived['selected_over'], 'selected triple is not the uniform tau/24')
    require(c['bridge_bound'] == derived['bridge_bound'] and c['end_bound'] == derived['end_bound'], 'coefficient box bounds')
    require(c['J_prime'] == derived['J_prime_split'], "per-site sum split %s differs from the recomputed %s" % (c['J_prime'], derived['J_prime_split']))
    require(c['G_R_text'] == G_R_UP and c['GP_R_text'] == GP_R_UP and c['radius_text'] == R_RADIUS and c['contraction_bound_text'] == 1,
            'AM2 constants in the resolution differ from the admitted ones')
    validate_j0_resolution({'label': 'R1', 'cap': derived['cap'], 'J0': c['J0_prime'],
                            'self_map': c['self_map_text'], 'contraction': c['contraction_text']}, derived['J_per_tau'], derived['cap'])
    require(c['R2_cap'] * derived['J_per_tau'] == derived['old_J0'] and c['R2_cap'] < derived['cap'],
            'the R2 alternative is not the changed cap J_0/29')
    require(c['reset'] == derived['reset_split'], 'reset budget split %s differs from the recomputed %s' % (c['reset'], derived['reset_split']))
    require(c['incidence'] == derived['incidence_tuple'], 'incidence text differs from the itemized table')
    require(c['first_order'] == derived['first_order_tuple'], 'first-order face bounds or coefficient differ from the derivation')
    require(c['dictionary_numerator'] == 96 and c['g4_cap_text'] == derived['g4_cap'], 'dictionary or g^4 at the cap differs from tau=96/g^4')
    require(c['ax2_relation'] == derived['ax2_relation'], 'AX2 relation differs from 2*k\'*M_1 with M_1=4/pi')
    require(c['reference'] == (HAAR_W, HAAR_W2), 'reference values differ from the Haar moments 0 and 1/4')
    require('D_ii' in c['target_quantity'] and c['target_comparator'] == '<=' and c['target'] > 0, 'target quantity or comparator')
    require(ax2_feasible(c['target'], c['ax2_relation'], derived['cap']), 'contract target violates the AX2 feasibility relation')
    return c


def validate_contract_bytes(raw, expected_sha, derived):
    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'contract bytes do not match the bound hash')
    data = json.loads(raw)
    return validate_contract(data, derived)


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    for f in files:
        require(not f.startswith(FORBIDDEN_INPUTS), 'forbidden premise in reverse inputs: ' + f)
        require(f not in contract.get('forward_additional_premises', []), 'forward-only premise in reverse inputs: ' + f)
    require(set(files) == expected and len(files) == len(expected),
            'reverse inputs inventory differs from AGENTS.md + contract + shared_premises')
    return True


def gate_text(rel):
    gate = json.loads((INPUTS / rel).read_text())
    must(gate.get('verdict') == 'accepted_within_scope', 'inherited gate not accepted: ' + rel)
    return gate['accepted']


# ==================================================================== compute
def compute():
    global TAU_CAP, J_PER_TAU, J0_PRIME, PI_LO, PI_HI, FLIP_GROUPS
    check_py_sha = sha256_file(HERE / 'check.py')          # recorded before any evaluation
    raw = (INPUTS / CONTRACT_REL).read_bytes()
    contract_sha = hashlib.sha256(raw).hexdigest()
    must(contract_sha == CONTRACT_SHA256, 'contract snapshot hash differs from the bound hash')
    record('contract_snapshot_bound', contract_sha == CONTRACT_SHA256, contract_sha256=contract_sha,
           source='inputs/' + CONTRACT_REL)
    record('check_py_hash_recorded_before_evaluation', len(check_py_sha) == 64, check_py_sha256=check_py_sha)
    cache = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if '__pycache__' in p.parts or p.suffix == '.pyc')
    record('no_interpreter_cache_in_closure', cache == [])
    contract = json.loads(raw)
    PI_LO, PI_HI = pi_bounds()
    must(Q(314159, 100000) < PI_LO and PI_HI < Q(314160, 100000), 'pi enclosure')

    # ---- inherited gates (snapshots): cap, dictionary, flip set, first-order coefficient
    am2_text = gate_text(AM2_GATE_REL)
    m = re.search(r'\|tau\|<=1/(\d+)', am2_text)
    must(m is not None and 'alpha/16' in am2_text, 'AM2 gate cap / gap not found')
    am2_cap = Q(1, int(m.group(1)))
    al1_text = gate_text(AL1_GATE_REL)
    must('tau=96/g^4' in al1_text and 'r=4/g^4' in al1_text, 'AL1 dictionary not found')
    aw1_text = gate_text(AW1_GATE_REL)
    must('E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even}' in aw1_text and '+tau/144' in aw1_text, 'AW1 flip set / coefficient not found')
    av1_text = gate_text(AV1_GATE_REL)
    m = re.search(r'D_ii=(\d+)/(\d+) \(~1\.3612e-8', av1_text)
    must(m is not None, 'AV1 admitted D_ii not found')
    av1_D = Q(int(m.group(1)), int(m.group(2)))
    TAU_CAP = parse_q(contract['parameters']['tau_cap'])
    must(TAU_CAP == am2_cap, 'contract cap differs from the AM2 cap')
    target = parse_q(contract['preregistration']['target']['value'])
    record('inherited_gates_read', True, am2_cap=qs(am2_cap), al1_dictionary='tau=96/g^4, r=4/g^4',
           aw1_flip_set='E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even}', av1_admitted_D_ii_zero_selected=qs(av1_D),
           note='read from hash-bound premise snapshots; the AV1 value belongs to the zero-selected family and is not used as a route-B constant')

    # ---- SU(2) and units
    casimir_spectrum = [j * (j + 1) for j in (Q(0), HALF, Q(1), Q(3, 2))]
    record('su2_casimir_haar_moments_onsite_gap', CASIMIR_HALF == Q(3, 4) and HAAR_W == 0 and HAAR_W2 == Q(1, 4)
           and ONSITE_GAP == 6 and min(x for x in casimir_spectrum if x > 0) == CASIMIR_HALF,
           casimir_spectrum=[qs(x) for x in casimir_spectrum], haar_W=qs(HAAR_W), haar_W2=qs(HAAR_W2),
           onsite_gap_normalized=qs(ONSITE_GAP),
           theorem='h_b=8 sum_{e owned by b} C_e has kernel the constant (Haar) function (spin 0 on all 24 links) and next eigenvalue 8*3/4=6, so h_b>=6Q_b>=Q_b')
    record('face_vector_energy_24_norm_half', FACE_ENERGY == 24 and FACE_ENERGY_ALPHA == 3 and FACE_NORM ** 2 == HAAR_W2
           and certify_face_energy(24, 'delta') == 24 and certify_face_energy(3, 'alpha') == 3
           and per_face_coefficient(Q(1), 'delta', 'delta') == Q(1, 144) and per_face_coefficient(Q(1), 'alpha', 'alpha') == Q(1, 144),
           normalized_energy=qs(FACE_ENERGY), alpha_units_energy=qs(FACE_ENERGY_ALPHA), per_face_coefficient_per_tau='1/144',
           statement='every face (omitted or selected) gives W_f Omega_0 with spin 1/2 on its four links: H_0 eigenvalue 24, norm 1/2')
    region = [(x, y, z) for x in range(4) for y in range(4) for z in range(3)]
    all_faces = [frozenset(face_links(p, a, c)) for p in region for _, a, c in ORIENTATIONS]
    max_shared = max(len(f & g) for i, f in enumerate(all_faces) for g in all_faces[i + 1:])
    record('distinct_faces_share_at_most_one_link', max_shared == 1 and len(set(all_faces)) == len(all_faces),
           faces_examined=len(all_faces), max_shared_links=max_shared)

    # ---- the 24 anchored classes
    table_rows = expand_table(I1_TABLE)
    fine_rows = fine_face_classes()
    CLASSES.extend(table_rows)
    omitted, selected = class_ids('omitted'), class_ids('selected')
    record('i1_24_class_table_reproduced_from_fine_lattice', table_rows == fine_rows and len(table_rows) == 24
           and len(omitted) == 21 and len(selected) == 3 and all(CLASSES[k][3] == (ORIGIN,) for k in selected),
           classes=len(table_rows), omitted=len(omitted), selected=len(selected),
           selected_classes=[CLASSES[k][0] + ' r=%d s=%d' % (CLASSES[k][1], CLASSES[k][2]) for k in selected])

    # ---- item 1: dictionary, box, label
    dict_rows = []
    for g2, a in ((Q(3, 2), Q(5, 7)), (Q(1, 10), Q(2)), (Q(40000), Q(1, 3))):
        alpha, lam = g2 / (2 * a), 2 / (g2 * a)
        tau_d = 24 * lam / alpha
        dict_rows.append({'g2': qs(g2), 'a': qs(a), 'tau': qs(tau_d), 'g4_tau': qs(tau_d * g2 * g2),
                          'nu_equals_lambda': (alpha * tau_d / 24 == lam)})
        must(tau_d * g2 * g2 == 96 and alpha * tau_d / 24 == lam and (alpha / 8) * (tau_d / 3) == lam, 'dictionary identity')
    g4_cap = g4_from_tau(TAU_CAP)
    tri = certify_uniform_triple_in_box(uniform_triple(TAU_CAP), TAU_CAP, HALF, Q(1, 8))
    tri_m = certify_uniform_triple_in_box(uniform_triple(-TAU_CAP), -TAU_CAP, HALF, Q(1, 8))
    record('item1_dictionary_box_label', g4_cap == 9600000000 and certify_label(LABEL, g4_cap, TAU_CAP) == LABEL
           and tri[1] == Q(1, 2400000000) and tri_m[1] == -Q(1, 2400000000),
           dictionary='alpha=g^2/(2a), lambda=2/(g^2 a), nu=lambda=alpha*tau/24, tau=96/g^4; nu/delta=tau/3',
           dictionary_rows=dict_rows, g4_at_cap=qs(g4_cap), selected_triple_alpha_units=[qs(x) for x in tri],
           box='|lambda_L|,|lambda_R|<=1/2, |mu|<=1/8 (alpha units): |tau|/24<=1/2400000000', label=LABEL,
           sign_note='tau=96/g^4>0 for real g; tau<0 is the U_E image of the tau>0 model (item 9), not a real-g KS coupling')

    # ---- item 2: route B, grouping, per-site sum, support, no double count
    k_sel = abs(FACE_COEFF_NORMALIZED) * TAU_CAP
    trial_num, trial = onsite_trial_energy(k_sel)
    must(trial_num == -TAU_CAP ** 2 / 864 and trial < 0, 'route A trial energy')
    route_packet = {'route': 'B', 'reference': 'haar', 'onsite': 'casimir_only', 'selected_faces_in': 'interaction',
                    'groups': ['single_factor', 'whole_star']}
    record('item2_route_b_declared_haar_reference', certify_route(route_packet) == 'B' and certify_haar_is_onsite_ground('B', TAU_CAP),
           route=route_packet, route_A_trial_numerator_at_cap=qs(trial_num), route_A_trial_rayleigh_quotient_at_cap=qs(trial),
           statement='route A (selected faces on site) has a trial Omega+(k/24)W Omega, k=tau/3, with numerator -tau^2/864<0 below Haar, so its reference is the selected strip; route B keeps the Haar product and moves the selected faces into V')
    sites3, groups3 = box_groups(3, 'route_B')
    sums3 = per_site_sums(sites3, groups3)
    j_bulk = max(sums3.values())
    star_units = len(STAR) * Q(len(omitted), 3)
    single_units = Q(len(selected), 3)
    J_PER_TAU = star_units + single_units
    charged = certify_no_double_count(groups3)
    alt = {r: qs(bulk_per_site_sum(r)[0]) for r in ('route_B', 'selected_in_star', 'zero_selected', 'per_face')}
    max_support = max(len(g['support']) for g in groups3)
    record('item2_grouping_per_site_sum_29', j_bulk == J_PER_TAU == 29 and sums3[ORIGIN] == 29 and star_units == 28 and single_units == 1
           and charged == sum(len(g['faces']) for g in groups3) and max_support == MAX_SUPPORT
           and all(v <= 29 for v in sums3.values()),
           psi_b='-(tau/3) sum of the three selected xy faces of factor b; ||psi_b||<=3*(1/3)|tau|=|tau| (equality at the identity configuration)',
           J_prime_per_tau=qs(J_PER_TAU), split={'four_anchor_stars': qs(star_units), 'single_factor_group': qs(single_units)},
           box_N3_bulk_max=qs(j_bulk), faces_charged_once_in_box_N3=charged, max_support=max_support,
           alternative_groupings_per_site_sum=alt,
           alternatives_note='selected_in_star gives 32|tau| and changes the box inventory; per_face gives 52/3|tau| with support three but changes the boundary prescription and the AM2 constants; zero_selected (28) drops the selected faces and is not the uniform model')
    tf = termination_fixture()
    record('item2_termination_order_unchanged', tf['star_ad9_zero'] and tf['star_ad8_nonzero'] and tf['single_ad3_zero']
           and tf['single_ad2_nonzero'] and tf['sum_ad9_zero'] and Q(tf['star_ad8_vacuum_to_1111']) == factorial(8),
           fixture=tf, model_is_finite_graph=True, transfers_to_aq=False,
           statement='a group of support |X| gives nonzero nested creation commutators only up to order 2|X|: whole stars 8, single-factor groups 2; the maximum stays eight')

    # ---- item 3: J_0 re-freeze and the AM2 re-instantiation
    enc = am2_enclosures()
    old_J0 = 28 * TAU_CAP
    must(old_J0 == Q(7, 25000000), 'admitted AM2 J_0')
    cparse = parse_contract(contract)
    J0_PRIME = validate_j0_resolution({'label': 'R1', 'cap': TAU_CAP, 'J0': cparse['J0_prime'],
                                       'self_map': cparse['self_map_text'], 'contraction': cparse['contraction_text']},
                                      J_PER_TAU, TAU_CAP)
    self_map = J0_PRIME * G_R_UP
    contraction = 2 * J0_PRIME * GP_R_UP
    lk_ok = all(lk_num(k) == 16 * 8 ** k * (1 + Q(5 * k, 4)) for k in range(9))
    record('item3_j0_exceeded_and_refrozen', J_PER_TAU * TAU_CAP > old_J0 and J0_PRIME == Q(29, 10 ** 8)
           and self_map == Q(1073, 175000000) and self_map < R_RADIUS and contraction == Q(319, 1562500) and contraction < 1
           and J0_PRIME * enc['G'][1] < self_map and 2 * J0_PRIME * enc['G_prime'][1] < contraction
           and enc['exp_one_eighth'][1] < Q(8, 7) and enc['G'][1] < G_R_UP and enc['G_prime'][1] < GP_R_UP and lk_ok
           and cparse['R2_cap'] == old_J0 / J_PER_TAU,
           J_prime_at_cap=qs(J_PER_TAU * TAU_CAP), frozen_AM2_J0=qs(old_J0), J0_prime=qs(J0_PRIME),
           self_map_J0p_times_148_over_7=qs(self_map), radius=qs(R_RADIUS), contraction_2_J0p_times_352=qs(contraction),
           lipschitz_J0p_times_352=qs(J0_PRIME * GP_R_UP), exp_one_eighth_enclosure=[qs(v) for v in enc['exp_one_eighth']],
           G_R_enclosure=[qs(v) for v in enc['G']], G_prime_R_enclosure=[qs(v) for v in enc['G_prime']],
           R2_alternative_cap=qs(cparse['R2_cap']), R2_status='changed coupling (cap 7/725000000<10^-8); not selected',
           contract_source='inputs/' + CONTRACT_REL, contract_sha256=contract_sha)
    am2_record_b = {'route': 'B', 'reference': 'haar', 'onsite_lower_gap': ONSITE_GAP, 'max_support': MAX_SUPPORT,
                    'termination_order': 8, 'cap': TAU_CAP, 'J_per_tau': J_PER_TAU, 'J0': J0_PRIME}
    am2_record_a = {'route': 'A', 'reference': 'selected_strip', 'onsite_lower_gap': Q(1), 'max_support': MAX_SUPPORT,
                    'termination_order': 8, 'cap': TAU_CAP, 'J_per_tau': Q(28), 'J0': old_J0}
    record('item3_am2_gap_reinstantiated', certify_am2_reuse(am2_record_b) and certify_am2_reuse(am2_record_a),
           hypotheses=['h_b>=Q_b with unique gauge-invariant vacuum (Haar; gap 6>=1)',
                       'max support 4, so L_k=16*8^k(1+5k/4) and G(t)=16e^{8t}(1+10t) are unchanged',
                       "J'<=29|tau|<=J_0' with J_0'G(R)<1/64 and 2J_0'G'(R)<1",
                       'V bounded, self-adjoint and gauge invariant in each finite volume',
                       'h_b has compact resolvent (Casimir sum on SU(2)^24), so AM2 section 6 cutoff removal applies'],
           conclusion="for every nonempty finite complete-factor volume and both signs of |tau|<=10^-8 the route-B Hamiltonian has a unique full-Hilbert ground and gap >=1/2 normalized, i.e. >=alpha/16 physical",
           route_A_cross_check='the same finite operator split with the selected faces on site (J=28|tau|<=J_0, uniform triple in the box) is covered by AM2 as admitted, resting on the inherited A1 strip theorem; route A is not used for the Haar-dependent steps',
           nonzero_excited_sector='every factor contains three selected faces whose links it owns; (W_g-<W_g>)Omega_H is gauge invariant, nonzero (strictly positive ground) and orthogonal to the ground',
           physical_gap='Delta>=delta/2=alpha/16=g^2/(32a)')

    # ---- item 5 and 6 enumeration: faces owning a link of u from the 24 classes
    def touching(site, ks):
        return sorted({(vsub(site, v), k) for k in ks for v in CLASSES[k][3]})
    all_k = list(range(len(CLASSES)))
    at0, atz = touching(ORIGIN, all_k), touching(EZ, all_k)
    at0_omitted = touching(ORIGIN, omitted)
    meeting = sorted(set(at0) | set(atz))
    meeting_set = set(meeting)
    inside = [f for f in meeting if set(owner_set(*f)) <= set(COVER)]
    n_by_owner = {}
    for f in at0:
        mo = owner_set(*f)
        n_by_owner[mo] = n_by_owner.get(mo, 0) + 1
    owners_meeting = {}
    for f in meeting:
        mo = owner_set(*f)
        owners_meeting[mo] = owners_meeting.get(mo, 0) + 1
    incident = sorted({vsub(u, v) for u in COVER for v in STAR})
    bound_per_factor = len(STAR) * len(CLASSES)
    bound_R = len(incident) * len(CLASSES)
    derived_counts = {'faces_per_factor': len(at0), 'owner_sets_per_factor': len(n_by_owner),
                      'faces_meeting_R': len(meeting), 'faces_inside_R': len(inside),
                      'selected_faces_per_factor': len(selected), 'omitted_faces_per_factor': len(at0_omitted),
                      'straddling_faces_meeting_R': len(meeting) - len(inside),
                      'faces_owning_both_sites_of_R': len(set(at0) & set(atz))}
    # independent brute force on the fine lattice (no class table)
    brute = {'own0': 0, 'meet': 0, 'inside': 0, 'selected_own0': 0}
    for x in range(-12, 12):
        for y in range(-6, 6):
            for z in range(-3, 4):
                for name, a, c in ORIENTATIONS:
                    p = (x, y, z)
                    ow = {coarse(t) for t, _ in face_links(p, a, c)}
                    if ORIGIN in ow:
                        brute['own0'] += 1
                        brute['selected_own0'] += 1 if fine_is_selected(p, name) else 0
                    if ow & set(COVER):
                        brute['meet'] += 1
                    if ow <= set(COVER):
                        brute['inside'] += 1
    must(brute['own0'] == len(at0) and brute['meet'] == len(meeting) and brute['inside'] == len(inside)
         and brute['selected_own0'] == len(selected), 'fine-lattice brute force reproduces the class-table counts')
    unique_anchor = all(f[0] == tuple(min(c[i] for c in owner_set(*f)) for i in range(3)) for f in at0)
    record('item6_first_order_faces_uniform_counts', derived_counts['faces_per_factor'] == 52 and len(at0) == len(atz)
           and derived_counts['faces_meeting_R'] == 88 and derived_counts['faces_inside_R'] == 16
           and derived_counts['owner_sets_per_factor'] == 16 and derived_counts['omitted_faces_per_factor'] == 49
           and sorted({f[0] for f in meeting}) == incident and unique_anchor
           and bound_per_factor == 96 and bound_R == 168,
           derived=derived_counts, fine_lattice_brute_force=brute, owner_set_face_counts=sorted(n_by_owner.values()),
           labelled_bounds={'per_factor_4_anchors_times_24': bound_per_factor, 'R_7_anchors_times_24': bound_R},
           rule='faces owning a link of u are the pairs (u-v,k) with v in the class support; sum over the 24 classes of |support|=21+4+8+16+3=52',
           finding='the contract candidates 96 and 168 are reproduced only as anchor-group bounds (4x24, 7x24); the exact counts are 52 per factor and 88 meeting R')
    COUNTS['faces_per_factor'] = DerivedCount(derived_counts['faces_per_factor'], PROVENANCE)
    COUNTS['faces_meeting_R'] = DerivedCount(derived_counts['faces_meeting_R'], PROVENANCE)
    COUNTS['bound_per_factor'] = bound_per_factor
    COUNTS['bound_R'] = bound_R
    COUNTS['orth_site_sum_hi'] = sum((sqrt_bounds(n)[1] for n in n_by_owner.values()), Q(0))
    COUNTS['orth_site_sum_lo'] = sum((sqrt_bounds(n)[0] for n in n_by_owner.values()), Q(0))
    COUNTS['orth_meeting_R_hi'] = sum((sqrt_bounds(n)[1] for n in owners_meeting.values()), Q(0))
    box_info = {}
    for N in (2, 3):
        sites, groups = box_groups(N, 'route_B')
        counts = per_site_face_counts(sites, groups)
        sums = per_site_sums(sites, groups)
        box_faces = {f for g in groups for f in g['faces']}
        meet_box = sum(1 for f in box_faces if set(owner_set(*f)) & set(COVER))
        inside_box = sum(1 for f in box_faces if set(owner_set(*f)) <= set(COVER))
        stars_in = [g['anchor'] for g in groups if g['kind'] == 'whole_star']
        singles_R = [g['anchor'] for g in groups if g['kind'] == 'single_factor' and g['anchor'] in COVER]
        must(max(counts.values()) == 52 and all(counts[u] <= 52 for u in sites) and max(sums.values()) == 29
             and meet_box == 88 and inside_box == 16 and all(a in stars_in for a in incident) and len(singles_R) == 2,
             'box enumeration reproduces the translation-covariant counts')
        box_info['N=%d' % N] = {'sites': len(sites), 'whole_stars': len(stars_in), 'single_factor_groups': len(sites),
                                'faces': len(box_faces), 'max_faces_per_site': max(counts.values()),
                                'boundary_sites_below_bulk': sum(1 for u in sites if counts[u] < 52),
                                'max_per_site_sum_per_tau': qs(max(sums.values())), 'faces_meeting_R': meet_box,
                                'faces_inside_R': inside_box, 'incident_stars_retained': sum(1 for a in incident if a in stars_in),
                                'single_factor_groups_meeting_R': len(singles_R)}
    _, groups1 = box_groups(1, 'route_B')
    n1_stars = sum(1 for g in groups1 if g['kind'] == 'whole_star' and g['anchor'] in incident)
    all_size = all(all(-N <= b[i] and b[i] + 1 <= N for i in range(3)) for N in range(2, 12) for b in incident)
    record('item5_incidence_all_sizes_and_boxes', all_size and n1_stars == 4 and len(incident) == 7,
           boxes=box_info, N1_incident_stars_retained=n1_stars,
           all_size_argument='b+S lies in [-N,N]^3 iff b in [-N,N-1]^3; R-S has coordinates in {-1,0,1}, so all seven stars are retained for every N>=2; the single-factor groups at 0 and e_z are retained for every N>=1')

    # ---- items 5 and 10: itemized incidence table on R
    _, groups2 = box_groups(2, 'route_B')
    FLIP_GROUPS = groups2
    groups_meeting = sorted([g for g in groups2 if set(g['support']) & set(COVER)], key=lambda g: (g['kind'], g['anchor']))
    rows = incidence_rows(groups_meeting, meeting_set)
    totals = certify_incidence_table(rows, meeting_set)
    table_out = []
    for r in rows:
        table_out.append({'kind': r['kind'], 'anchor': list(r['anchor']), 'support': [list(u) for u in r['support']],
                          'n_faces': len(r['faces']), 'faces': [face_label(*f) for f in r['faces']],
                          'faces_owning_link_in_R': r['faces_owning_link_in_R'], 'faces_inside_R': r['faces_inside_R'],
                          'norm_normalized_per_tau': qs(Q(len(r['faces']), 3)),
                          'norm_alpha_units_per_tau': qs(Q(len(r['faces']), 3) / ALPHA_OVER_DELTA)})
    B_N = totals['B_N_alpha_units_per_tau']
    k_prime = totals['k_prime_per_tau']
    record('item10_incidence_table_itemized_no_double_count', totals['stars'] == 7 and totals['single_factor_groups'] == 2
           and totals['selected_faces'] == 6 and totals['faces_charged'] == 7 * 21 + 2 * 3
           and totals['faces_owning_link_in_R'] == 88 and B_N == Q(51, 8) and k_prime == Q(51, 4)
           and sorted(r['anchor'] for r in rows if r['kind'] == 'whole_star') == incident,
           table=table_out, totals={k: (qs(v) if isinstance(v, Q) else v) for k, v in totals.items()},
           partition_proof='each face has a unique anchor pi(base) and a unique class; stars hold only the 21 omitted classes and single-factor groups only the 3 selected classes, so no face is charged twice',
           B_N='||B_N||<=7*(7|tau|/8)+2*(|tau|/8)=51|tau|/8 in G=H/alpha units', k_prime="k'=2||B_N|| ||W||=51|tau|/4")

    # ---- item 4: reset budget and the AQ1/AQ2 checklist
    reset_budget = 2 * sum((Q(len(r['faces']), 3) for r in rows), Q(0))
    eps_R = certify_reset(reset_budget, reset_budget / ONSITE_GAP, ONSITE_GAP, reset_budget)
    td_sq_bound = eps_R * TAU_CAP                    # (2 sqrt eps)^2/4 <= (1/1000)^2 iff eps <= 10^-6
    gap_one_eps = reset_budget * TAU_CAP
    C_F_per_site = 2 * J_PER_TAU
    ns_norm = 81 * J_PER_TAU
    shells_ok = all(4 * r * r + 2 <= 6 * (r + 1) ** 2 for r in range(1, 200))
    variance_floor = Q(1, 4) - Q(1, 500) - Q(1, 250000)
    record('item4_reset_budget_102_epsilon_17', reset_budget == 102 and eps_R == 17 and td_sq_bound <= Q(1, 10 ** 6)
           and gap_one_eps > Q(1, 10 ** 6) and C_F_per_site == 58 and ns_norm == 2349 and shells_ok
           and variance_floor == Q(61999, 250000) and variance_floor > Q(1, 5),
           reset='omega(h_R)<=2(7*7|tau|+2*|tau|)=102|tau|', epsilon_R='<=102|tau|/6=17|tau| (h_R>=6(I-P_R))',
           trace_distance='||rho_R-P_R||_1<=2sqrt(17|tau|)<=1/500 at the cap (square-root control only)',
           gap_one_counterfactual='with the selected-strip gap one, 102|tau|=102/10^8>10^-6 and the verbatim AQ2 1/500 would fail: the Haar gap six is load-bearing',
           aq1_C_F='Tr(rho h_F)<=2(4*7+1)|tau||F|=58|tau||F|', ns_interaction_norm="||Phi||_F<=81J'=2349|tau|",
           variance_floor=qs(variance_floor))
    checklist = [
        {'step': 'AM2 unique ground and centred full-space gap', 'source': 'round29/forward/am2 sections 1-4', 'status': 'new_constant',
         'admitted': 'J<=28|tau|<=J_0=7/25000000', 'route_B': "J'<=29|tau|<=J_0'=29/10^8; J_0'G(R)<1073/175000000<1/64; 2J_0'G'(R)<319/1562500<1; gap 1/2 normalized"},
        {'step': 'AM2 on-site hypothesis h_x>=Q_x', 'source': 'am2 (HNM-AM2.1)', 'status': 'verbatim',
         'admitted': 'selected-strip reference, gap delta (normalized 1)', 'route_B': 'Haar reference, h_b=8 sum C_e>=6Q_b>=Q_b'},
        {'step': 'AM2 anchored majorant, termination order and G', 'source': 'am2 (HNM-AM2.5, AM2.8)', 'status': 'verbatim',
         'admitted': 'max support 4, L_k=16*8^k(1+5k/4), order 8', 'route_B': 'max support 4 (stars) and 1 (single-factor groups): unchanged'},
        {'step': 'AM2 gauge covariance, physical restriction, nonzero excited sector', 'source': 'am2 section 5', 'status': 'verbatim',
         'admitted': 'selected square witness', 'route_B': 'selected face witness in every factor; Haar vacuum gauge invariant'},
        {'step': 'AM2 cutoff removal', 'source': 'am2 section 6', 'status': 'verbatim',
         'admitted': 'compact resolvent, form core, min-max', 'route_B': 'same (pure Casimir sum)'},
        {'step': 'AQ1 reset energy C_F', 'source': 'aq1 (HNM-AQ1.1)', 'status': 'new_constant',
         'admitted': '8M|F|=56|tau||F|', 'route_B': "2J'|F|=58|tau||F|"},
        {'step': 'AQ1 trace-norm compactness and diagonal extraction', 'source': 'aq1 (HNM-AQ1.2)', 'status': 'verbatim',
         'admitted': 'C_F/L tails', 'route_B': 'same with C_F=58|tau||F|'},
        {'step': 'AQ1 Nachtergaele-Sims placement', 'source': 'aq1 (HNM-AQ1.3)', 'status': 'new_constant',
         'admitted': 'J<=28|tau|, ||Phi||_F<=2268|tau|', 'route_B': "J'<=29|tau|, ||Phi||_F<=81J'=2349|tau|; ||F||<=7, C<=224 unchanged"},
        {'step': 'AQ1 stationarity, GNS strong continuity, Stone generator', 'source': 'aq1 section 4', 'status': 'verbatim',
         'admitted': 'norm volume limits on compact times', 'route_B': 'same'},
        {'step': 'AQ1 nonnegativity of the generator', 'source': 'aq1 section 5', 'status': 'verbatim',
         'admitted': 'Fourier tests on (-inf,0)', 'route_B': 'same'},
        {'step': 'AQ1/AQ2 gauge invariance, Haar projection, physical density', 'source': 'aq1 section 5, aq2 sections 1-2', 'status': 'verbatim',
         'admitted': 'endpoint group G', 'route_B': 'same'},
        {'step': 'AQ2 physical gap alpha/16 and simple vacuum', 'source': 'aq2 section 3', 'status': 'new_constant',
         'admitted': 'AM2 full-Hilbert finite gap at J_0', 'route_B': "AX1 re-frozen full-Hilbert finite gap at J_0' (value alpha/16 unchanged)"},
        {'step': 'AQ2 Wilson-cover reset', 'source': 'aq2 (HNM-AQ2.8)', 'status': 'new_constant',
         'admitted': '2*7*7|tau|=98|tau|', 'route_B': '2(7*7+2)|tau|=102|tau|'},
        {'step': 'AQ2 reference overlap and trace distance', 'source': 'aq2 (HNM-AQ2.9)', 'status': 'new_constant',
         'admitted': 'epsilon<=98|tau| (gap one), 2sqrt(eps)<=1/500', 'route_B': 'epsilon<=17|tau| (gap six), 2sqrt(17|tau|)<=1/500'},
        {'step': 'AQ2 reference moments Tr(P_R W)=0, Tr(P_R W^2)=1/4', 'source': 'aq2 section 5', 'status': 'verbatim',
         'admitted': 'one free z link Haar', 'route_B': 'all 48 cover links Haar'},
        {'step': 'AQ2 Wilson variance floor', 'source': 'aq2 (HNM-AQ2.10)', 'status': 'verbatim',
         'admitted': '61999/250000>1/5', 'route_B': '61999/250000>1/5'},
        {'step': 'AT4 local Duhamel slope', 'source': 'at4 (F10-F11)', 'status': 'new_constant',
         'admitted': '||B_N||<=49|tau|/8, k=49|tau|/4', 'route_B': "||B_N||<=51|tau|/8, k'=51|tau|/4"},
        {'step': 'AV1 state lemma tiers', 'source': 'av1 reports and gate', 'status': 'new_constant',
         'admitted': "J=28|tau|, t_1=49|tau|/144, a_1=82|tau|/144", 'route_B': "J'=29|tau|, t_1'=52|tau|/144, a_1'=88|tau|/144"},
    ]
    unproved = [r['step'] for r in checklist if r['status'] not in ('verbatim', 'new_constant')]
    record('item4_reinstantiation_checklist', unproved == [] and len(checklist) == 18
           and sum(1 for r in checklist if r['status'] == 'new_constant') == 8,
           checklist=checklist, named_constants_unproved=unproved,
           new_constants={'C_F_per_site_per_tau': qs(C_F_per_site), 'ns_norm_per_tau': qs(ns_norm),
                          'reset_per_tau': qs(reset_budget), 'epsilon_R_per_tau': qs(eps_R),
                          'B_N_alpha_per_tau': qs(B_N), 'k_prime_per_tau': qs(k_prime), 'J0_prime': qs(J0_PRIME)})

    # ---- item 6: state-lemma tiers at both signs
    points = {'+': TAU_CAP, '-': -TAU_CAP, 'scaling_only_tau_over_100': TAU_CAP / 100}
    tiers = {}
    for key, fn in (('tier_i', lambda t: tier_i(t)), ('tier_i_iterated', lambda t: tier_i(t, iterate=4)),
                    ('tier_ii', lambda t: tier_ii(t, 'exact_counts')),
                    ('tier_ii_global_two_site', lambda t: tier_ii(t, 'global_two_site')),
                    ('tier_ii_labelled_bound_96_168', lambda t: tier_ii(t, 'labelled_bound_96_168')),
                    ('tier_ii_owner_set_orthogonal', lambda t: tier_ii(t, 'owner_set_orthogonal')),
                    ('tier_ii_directed_remainder', lambda t: tier_ii(t, 'directed_remainder'))):
        tiers[key] = {s: fn(v) for s, v in points.items()}
        must(tiers[key]['+']['_D'] == tiers[key]['-']['_D'], 'both signs give the same |tau| bound')
    D_i = tiers['tier_i']['+']['_D']
    D_ii = tiers['tier_ii']['+']['_D']
    ii = tiers['tier_ii']['+']
    record('item6_tier_i_crude_both_signs', Q(tiers['tier_i']['+']['t_upper']) == self_map and D_i == tiers['tier_i']['-']['_D']
           and not (D_i <= target),
           t_upper=tiers['tier_i']['+']['t_upper'], D_prime_i=qs(D_i), preview=sci(D_i),
           iterated_preview=tiers['tier_i_iterated']['+']['D_preview'], target_met=False)
    record('item6_tier_ii_exact_first_order_both_signs', Q(ii['t1_first_order_anchored']) == Q(13, 3600000000)
           and Q(ii['T_self_consistent']) == Q(13, 3599632512) and Q(ii['a1_first_order_meeting_R']) == Q(11, 1800000000)
           and Q(ii['remainder_anchored_upper_rho']) > 0 and D_ii == tiers['tier_ii']['-']['_D']
           and admit_bound(D_ii, target) and admit_bound(tiers['tier_ii']['-']['_D'], target),
           t1_prime=ii['t1_first_order_anchored'], T_prime=ii['T_self_consistent'], rho_prime=ii['remainder_anchored_upper_rho'],
           a1_prime=ii['a1_first_order_meeting_R'], epsilon=ii['epsilon'], D_prime_ii=qs(D_ii), preview=sci(D_ii),
           target=qs(target), margin_preview=sci(target / D_ii, 6), source='contract preregistration.target')
    variants_ok = all(admit_bound(tiers[k][s]['_D'], target) for k in tiers if k.startswith('tier_ii') for s in ('+', '-'))
    record('item6_tier_ii_variants_all_meet_target', variants_ok
           and tiers['tier_ii_owner_set_orthogonal']['+']['_D'] < D_ii
           and tiers['tier_ii_directed_remainder']['+']['_D'] <= D_ii
           and D_ii < tiers['tier_ii_global_two_site']['+']['_D'] < tiers['tier_ii_labelled_bound_96_168']['+']['_D'],
           variants={k: {'D_exact_2eps': tiers[k]['+']['D_exact_2eps'], 'D_density_form_exact': tiers[k]['+']['D_density_form_exact'],
                         'preview': tiers[k]['+']['D_preview']} for k in tiers if k.startswith('tier_ii')})
    record('item6_density_form_certified_by_both_inequalities', all(
        Q(tiers[k]['+']['D_fidelity_directed_1e-40']) <= Q(tiers[k]['+']['D_exact_2eps']) + Q(1, DEN)
        and Q(tiers[k]['+']['D_exact_2eps']) < Q(tiers[k]['+']['D_density_form_exact']) for k in tiers),
        statement='2eps/sqrt(1+eps^2) <= 2eps < 2eps(1+eps)/(1+eps^2): the exact 2eps is a fidelity-route bound; the density form is certified by both admitted inequalities')
    scaling = {}
    for key in ('tier_i', 'tier_ii', 'tier_ii_labelled_bound_96_168'):
        ratio = tiers[key]['+']['_D'] / tiers[key]['scaling_only_tau_over_100']['_D']
        certify_linear_scaling((ratio, ratio))
        scaling[key] = {'ratio_exact': qs(ratio), 'preview': sci(ratio, 12)}
    sq_big, sq_small = sqrt_bounds(eps_R * TAU_CAP), sqrt_bounds(eps_R * TAU_CAP / 100)
    sq_bracket = (sq_big[0] / sq_small[1], sq_big[1] / sq_small[0])
    record('tau_scaling_linear_vs_square_root_reset', Q(99, 10) <= sq_bracket[0] and sq_bracket[1] <= Q(101, 10),
           scaling=scaling, reset_square_root_ratio_bracket=[qs(sq_bracket[0]), qs(sq_bracket[1])])
    first_order_abs = TAU_CAP / 144
    consequences = {}
    for key in ('tier_i', 'tier_ii'):
        for sign in ('+', '-'):
            D = tiers[key][sign]['_D']
            must(certify_variance_lower(centered_variance_lower(D, True), D) and certify_mean_budget(first_order_abs, D), 'consequences')
            consequences[key + sign] = {'abs_omega_W_upper': qs(D), 'omega_W2_interval': [qs(Q(1, 4) - D / 2), qs(Q(1, 4) + D / 2)],
                                        'variance_interval': [qs(centered_variance_lower(D, True)), qs(Q(1, 4) + D / 2)]}
    record('consequences_mean_second_moment_and_first_order_compatibility', D_ii >= first_order_abs, consequences=consequences,
           first_order_mean_abs=qs(first_order_abs),
           statement='|omega(W)|<=D, |omega(W^2)-1/4|<=D/2 (trace-zero effect bound), m^2<=D^2 charged; D_ii>=|tau|/144 so the first-order mean is paid for')
    relation = cparse['ax2_relation']
    thr = ax2_threshold_bracket(relation, TAU_CAP)
    stated = cparse['ax2_stated_threshold']
    record('ax2_feasibility_relation', relation == (51, 6) and ax2_feasible(D_ii, relation, TAU_CAP)
           and ax2_feasible(target, relation, TAU_CAP)
           and ax2_feasible(tiers['tier_ii_labelled_bound_96_168']['+']['_D'], relation, TAU_CAP)
           and not ax2_feasible(D_i, relation, TAU_CAP) and not ax2_feasible(stated, relation, TAU_CAP)
           and thr[1] < stated and target < thr[0],
           relation="2(D'+D'^2)+51|tau|/pi<=10^-6 (k'M_1 with M_1=4s/pi at s=1)", threshold_bracket=[qs(thr[0]), qs(thr[1])],
           threshold_preview=sci(thr[0], 8), contract_stated_threshold=qs(stated),
           finding="the contract's 'D'<=4.19x10^-7' is rounded up: the exact threshold is about 4.18831e-7, so 4.19e-7 itself is infeasible; the tested target 4/10^7 is feasible")

    # ---- item 9: transfer of the flip identity, the parity theorem and +tau/144
    residue_ok = all(flip_count(face_links(p, a, c)) % 2 == 1
                     for p in [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)] for _, a, c in ORIENTATIONS)
    hist = {1: 0, 3: 0}
    for x in range(-6, 7):
        for y in range(-6, 7):
            for z in range(-6, 7):
                for _, a, c in ORIENTATIONS:
                    n = flip_count(face_links((x, y, z), a, c))
                    must(n in hist, 'a plaquette meets E evenly')
                    hist[n] += 1
    box_faces2 = [f for g in groups2 for f in g['faces']]
    box_odd = all(flip_count(face_link_set(*f)) % 2 == 1 for f in box_faces2)
    rule_images = {}
    for rule in sorted(KAPPA_RULES):
        img = flip_image(hamiltonian_coefficients(groups2, TAU_CAP, rule))
        rule_images[rule] = img == hamiltonian_coefficients(groups2, -TAU_CAP, rule)
    record('item9_uniform_flip_identity', residue_ok and box_odd and certify_uniform_antisymmetry('tied_tau_over_24', TAU_CAP)
           and rule_images['tied_tau_over_24'] and not rule_images['absolute_value'] and not rule_images['offset'],
           residue_cases=24, fine_box_histogram={'meets_E_once': hist[1], 'meets_E_three_times': hist[3]},
           route_B_box_N2_faces=len(box_faces2), omitted_faces=sum(1 for f in box_faces2 if CLASSES[f[1]][4] == 'omitted'),
           selected_faces=sum(1 for f in box_faces2 if CLASSES[f[1]][4] == 'selected'),
           image_equals_H_minus_tau_by_rule=rule_images,
           proof='U_E (central -1 on each link of E) commutes with every C_e, hence with h_b, its spectral cutoffs and P_b, and with every endpoint gauge action; each plaquette meets E in 1 or 3 links so U_E W_f U_E^*=-W_f; in the uniform model every face term is -(tau/3)W_f, so U_E H(tau) U_E^*=H(-tau) in every centred box and cutoff compression, with no inherited strip-operator form needed',
           consequences='omega_{N,-tau}(W)=-omega_{N,tau}(W); omega_N(W^2), C_N, c_N even in tau; AQ limits: S(-tau)=S(tau)o alpha_E as whole sets (pointwise only along a common subsequence); no O(tau^3) remainder from oddness')
    Wf = (ORIGIN, next(k for k in omitted if CLASSES[k][0] == 'xz' and CLASSES[k][1] == 0 and CLASSES[k][2] == 0))
    W_set = face_link_set(*Wf)
    must(W_set == frozenset(W_LINKS), 'the original xz Wilson face is the omitted class xz r=0 s=0 at anchor 0')

    def odd_links(faces):
        mult = {}
        for f in faces:
            for l in face_link_set(*f):
                mult[l] = mult.get(l, 0) + 1
        return sum(1 for v in mult.values() if v % 2 == 1)

    pair_nonzero = [f for f in meeting if odd_links([Wf, f]) == 0]
    triple_W2 = all(odd_links([Wf, Wf, f]) > 0 for f in meeting)
    sym_sizes = {}
    for f in box_faces2:
        n = len(W_set ^ face_link_set(*f))
        sym_sizes[n] = sym_sizes.get(n, 0) + 1
    sel_sharing = sorted(face_label(*f) for f in meeting if CLASSES[f[1]][4] == 'selected' and len(W_set & face_link_set(*f)) == 1)
    triples_zero, n_triples = True, 0
    for i, f in enumerate(meeting):
        for j in range(i, len(meeting)):
            for kk in range(j, len(meeting)):
                n_triples += 1
                if odd_links([f, meeting[j], meeting[kk]]) == 0:
                    triples_zero = False
    coef = abs(FACE_COEFF_NORMALIZED) / FACE_ENERGY            # tau/72 per face in psi^(1)
    first_order = 2 * coef * sum((HAAR_W2 if f == Wf else Q(0) for f in pair_nonzero), Q(0))
    record('item9_parity_and_first_order_transfer', pair_nonzero == [Wf] and triple_W2 and triples_zero
           and sorted(sym_sizes) == [0, 6, 8] and sym_sizes[0] == 1 and first_order == Q(1, 144) and len(sel_sharing) == 2,
           faces_meeting_R_checked=len(meeting), selected_faces_meeting_R=sum(1 for f in meeting if CLASSES[f[1]][4] == 'selected'),
           only_W_pairs_with_W=True, E_W2_Wf_zero_for_every_face_including_W_and_selected=triple_W2,
           W_symmetric_difference_sizes_box_N2={str(k): v for k, v in sorted(sym_sizes.items())},
           selected_faces_sharing_a_link_with_W=sel_sharing, triple_products_checked=n_triples,
           first_order_coefficient=qs(first_order),
           statement='the per-link centre grading treats a selected face like any other single-face character: E[W^2 W_f]=0 and E[W W_f]=0 for f!=W, P_24 V W Omega_0=0 (odd-link sets of size 0,6,8), zero splitting of the invariant multiplet; omega(W)=2Re<W Omega_0,psi^(1)>+O(tau^2)=-2Re<W Omega_0,c^(1)>+O(tau^2)=+tau/144 (only f=W)')
    sign_rows = {}
    for rule in ('tied_tau_over_24', 'absolute_value', 'offset', 'double', 'zero_selected'):
        mp, mm = selected_mean(rule, TAU_CAP), selected_mean(rule, -TAU_CAP)
        sign_rows[rule] = {'kappa_plus': qs(KAPPA_RULES[rule](TAU_CAP)), 'kappa_minus': qs(KAPPA_RULES[rule](-TAU_CAP)),
                           'mean_plus': mp.text(), 'antisymmetric': quad_equal(mm, -mp), 'sign_plus': mp.sign()}
    omitted_mean = plaquette_mean(abs(FACE_COEFF_NORMALIZED) * TAU_CAP)
    k1 = abs(FACE_COEFF_NORMALIZED) * TAU_CAP
    fo_ok = (omitted_mean * omitted_mean).a <= (k1 / 48) ** 2 and (omitted_mean * omitted_mean).a >= (k1 / 48) ** 2 * (1 - k1 * k1 / 576)
    record('item9_one_plaquette_sign_and_kappa_tying_fixture', sign_rows['tied_tau_over_24']['antisymmetric']
           and sign_rows['tied_tau_over_24']['sign_plus'] == 1 and not sign_rows['absolute_value']['antisymmetric']
           and not sign_rows['offset']['antisymmetric'] and fo_ok and k1 / 48 == TAU_CAP / 144
           and quad_equal(plaquette_mean(-k1), -omitted_mean),
           rows=sign_rows, omitted_face_mean_plus=omitted_mean.text(), first_order='k/48 with k=tau/3 gives +tau/144',
           model_is_finite_graph=True, transfers_to_aq=False,
           statement='decoupled one-plaquette j<=1/2 fixtures in exact Q(sqrt d): the selected-face mean is odd in tau exactly when kappa is tied to tau')
    transfer = {
        'verbatim': ['finite-box parity theorem (first-order vanishing for omega(W^2), c(theta), C(s); C_N constant unbounded, not uniform in N)',
                     'flip identity, now H(tau)->H(-tau) for the uniform model (kappa tied to tau)',
                     'finite-box antisymmetry of omega_N(W) and evenness of omega_N(W^2), C_N, c_N',
                     'AQ set-level statement S(-tau)=S(tau)o alpha_E; pointwise only along a common subsequence',
                     'no O(tau^3) remainder from oddness',
                     'first-order Wilson mean +tau/144 (only f=W), orientation invariance'],
        'needs_route_B_constants': ['second-order remainder K_2 (J\'=29|tau|, t_1\'=52|tau|/144, single-site first-order creations from selected faces now enter the two-creation and density terms)',
                                    'supplementary omega(W^2) constant', 'AW2 enclosure and the decade-grid coupling rule',
                                    'uniform-in-N tau^2 constants'],
        'no_longer_true_in_route_B': 'AW1 remark that every first-order support has at least two sites: selected faces give single-site first-order creations c^(1)_{b}',
    }

    # ---- error ledger (six prereg names)
    parts = ii['_parts']
    ledger = {
        'am2_remainder': {'tier': 'ii', 'value': qs(2 * parts['rho']), 'formula': "2*352J'T'"},
        'two_creation': {'tier': 'ii', 'value': qs(parts['T'] ** 2), 'formula': "T'^2 (now includes single-site selected creations at 0 and e_z)"},
        'straddling': {'tier': 'ii', 'value': 'inside a_1\' and 2rho\'', 'formula': '%d of the %d faces meeting R have owner sets straddling R' % (derived_counts['straddling_faces_meeting_R'], derived_counts['faces_meeting_R'])},
        'density': {'tier': 'ii', 'value': 'not_applicable', 'reason': 'the fidelity route bounds the whole trace distance through Tr(rho_R P_R)=1/(1+e^2); no separate density term'},
        'onsite_cutoff_vector': {'tier': 'ii', 'value': '0', 'reason': "exact per-box limit: AV1 R20-R21 argument with the re-frozen uniform gap 1/2; Q_L W_f Omega_0=W_f Omega_0 for L>=24"},
        'arithmetic': {'tier': 'ii', 'value': '0', 'reason': 'exact rational 2eps; the directed fidelity value is rounded outward to 10^-40'},
    }
    must(sorted(ledger) == sorted(contract['preregistration']['error_terms_itemized']), 'error ledger names')

    # ---- contract candidates compared after derivation
    derived = {'cap': am2_cap, 'selected_over': 24, 'bridge_bound': Q(1, 8), 'end_bound': HALF,
               'J_per_tau': J_PER_TAU, 'J_prime_split': (int(J_PER_TAU), int(star_units), int(single_units)), 'old_J0': old_J0,
               'reset_split': (7, 7, 2, int(reset_budget), int(eps_R)),
               'incidence_tuple': (totals['single_factor_groups'], totals['selected_faces'], Q(49, 8), Q(2, 8), B_N, k_prime),
               'first_order_tuple': (bound_per_factor, len(CLASSES), bound_R, 144), 'g4_cap': g4_cap,
               'ax2_relation': (int(4 * k_prime), 6)}
    must(Q(7 * 7, 8) + Q(2, 8) == B_N and derived['reset_split'][0] == totals['stars'] and ONSITE_GAP * eps_R == reset_budget, 'derived tuples')
    c_checked = validate_contract_bytes(raw, CONTRACT_SHA256, derived)
    record('contract_candidates_compared_after_derivation', c_checked['J0_prime'] == J0_PRIME,
           read_from_contract={'tau_cap': qs(c_checked['tau_cap']), 'target': qs(c_checked['target']),
                               'J0_prime': qs(c_checked['J0_prime']), 'self_map': qs(c_checked['self_map_text']),
                               'contraction': qs(c_checked['contraction_text']), 'R2_cap': qs(c_checked['R2_cap']),
                               'reference': [qs(x) for x in c_checked['reference']], 'reference_route': c_checked['reference_route']},
           note='every number used above was derived first; the contract texts are parsed and compared, never used as inputs to a count')

    # =================================================== the 28 contract controls
    control('missing_incoming_stars', [
        ('outgoing_star_anchors_only', certify_anchor_set, ([ORIGIN, EZ],)),
        ('outgoing_only_per_site_sum_8', certify_per_site_sum, (8, 'route_B', J_PER_TAU)),
        ('reset_with_outgoing_stars_only', certify_reset, (2 * (2 * 7 + 2), Q(2 * (2 * 7 + 2), 6), ONSITE_GAP, reset_budget)),
    ], complete_anchor_count=len(incident), complete_per_site_sum=qs(J_PER_TAU))
    control('full_original_wilson_cover', [
        ('cover_origin_factor_only', certify_cover, ((ORIGIN,),)),
        ('cover_with_extra_factor', certify_cover, ((ORIGIN, EZ, (0, 0, -1)),)),
    ], cover=[list(c) for c in COVER], links=len(set(factor_links(ORIGIN)) | set(factor_links(EZ))))
    control('wrong_delta_alpha_hbar_clock', [
        ('alpha_coupling_over_delta_energy', per_face_coefficient, (TAU_CAP, 'alpha', 'delta')),
        ('delta_coupling_over_alpha_energy', per_face_coefficient, (TAU_CAP, 'delta', 'alpha')),
        ('energy_24_labelled_alpha_units', certify_face_energy, (24, 'alpha')),
        ('normalized_slope_labelled_alpha', certify_duhamel_slope, (ALPHA_OVER_DELTA * k_prime, 'alpha', k_prime)),
        ('slope_in_delta_units', certify_duhamel_slope, (k_prime, 'delta', k_prime)),
    ], correct_per_face_per_tau='1/144', k_prime_alpha_units=qs(k_prime))
    control('vector_versus_scalar_centering', [
        ('variance_lower_without_mean_square_tier_ii', certify_variance_lower, (centered_variance_lower(D_ii, False), D_ii)),
        ('variance_lower_without_mean_square_tier_i', certify_variance_lower, (centered_variance_lower(D_i, False), D_i)),
    ], statement='vector centring adds d^2, scalar subtraction gives -2md-d^2; the variance bound charges m^2<=D^2')
    control('first_order_mean_charged', [
        ('second_order_only_budget', certify_mean_budget, (first_order_abs, 2 * parts['rho'] + parts['T'] ** 2)),
        ('zero_budget', certify_mean_budget, (first_order_abs, Q(0))),
    ], first_order_mean_abs=qs(first_order_abs), D_prime_ii=qs(D_ii))
    control('tau_scaling_exponent', [
        ('square_root_reset_labelled_linear', certify_linear_scaling, (sq_bracket,)),
    ], linear_ratios={k: v['preview'] for k, v in scaling.items()}, reset_ratio='10 (square root)')
    control('changed_model_relabelled', [
        ('zero_selected_triple_as_uniform', certify_model, (TAU_CAP, ('0', '0', '0'))),
        ('ends_only_triple_as_uniform', certify_model, (TAU_CAP, (qs(TAU_CAP / 24), '0', qs(TAU_CAP / 24)))),
        ('coupling_above_cap', certify_model, (TAU_CAP * 10,)),
        ('route_a_reference_labelled_route_b', certify_route, ({'route': 'B', 'reference': 'selected_strip', 'onsite': 'casimir_only',
                                                                 'selected_faces_in': 'interaction', 'groups': ['single_factor', 'whole_star']},)),
    ], note='beyond the cap the certificate is silent; that is not a gap failure')
    base = json.loads(raw)

    def coherent(mut):
        doc = json.loads(json.dumps(base))
        mut(doc)
        blob = json.dumps(doc, indent=2).encode()
        return blob, hashlib.sha256(blob).hexdigest()

    def text_edit(key, old, new):
        def mut(d):
            must(old in d['parameters'][key], 'tamper anchor missing')
            d['parameters'][key] = d['parameters'][key].replace(old, new)
        return mut

    tampers = [
        ('J0_prime_old_value', text_edit('J0_resolution', "J_0'=29/10^8", "J_0'=28/10^8")),
        ('per_site_sum_28', text_edit('per_site_sum_J_prime', '29|tau| (28 from four anchor stars + 1', '28|tau| (28 from four anchor stars + 0')),
        ('reset_98', text_edit('reset_budget', '=102|tau|', '=98|tau|')),
        ('incidence_seven_groups', text_edit('incidence', 'exactly two single-factor', 'exactly seven single-factor')),
        ('first_order_bound_52_as_candidate', text_edit('first_order_faces', 'bounded by 96', 'bounded by 49')),
        ('g4_wrong_decade', text_edit('dictionary', 'g^4=9.6x10^9', 'g^4=9.6x10^8')),
        ('target_relaxed_1e-3', lambda d: d['preregistration']['target'].__setitem__('value', '1/1000')),
        ('tau_cap_1e-7', lambda d: d['parameters'].__setitem__('tau_cap', '1/10000000')),
        ('selected_triple_tau_over_12', lambda d: d['preregistration'].__setitem__('selected_triple_alpha_units', ['tau/12'] * 3)),
        ('reference_route_selected_strip', lambda d: d['preregistration']['observable'].__setitem__('reference_route', 'selected_strip')),
        ('control_removed', lambda d: d['controls'].pop()),
    ]
    tamper_mutations = []
    for label, mut in tampers:
        blob, digest = coherent(mut)
        tamper_mutations.append((label, validate_contract_bytes, (blob, digest, derived)))
    tamper_mutations.append(('byte_change_without_rehash', validate_contract_bytes, (raw + b' ', CONTRACT_SHA256, derived)))
    control('coherent_evidence_tampering', tamper_mutations,
            note='each tampered copy is rehashed coherently; semantic recomputation from the derived route-B constants still rejects it')
    good = dict(grouping_ok=True, contraction_ok=True, checklist_unproved=unproved, incidence_itemized=True,
                tier_ii_available=True, D_plus=D_ii, D_minus=tiers['tier_ii']['-']['_D'], target=target)
    crude_only = dict(good, tier_ii_available=False, D_plus=D_i, D_minus=D_i)
    contraction_failed = dict(good, contraction_ok=False)
    constant_unproved = dict(good, checklist_unproved=['AQ2 Wilson-cover reset'])
    over_target = dict(good, D_plus=2 * target)
    must(producer_outcome(**crude_only) == 'limited' and producer_outcome(**contraction_failed) == 'insufficient'
         and producer_outcome(**constant_unproved) == 'limited' and producer_outcome(**over_target) == 'limited',
         'limited and insufficient outcomes are produced')
    outcome = certify_outcome(producer_outcome(**good), good)
    control('insufficient_verdict_retained', [
        ('crude_only_relabelled_accepted', certify_outcome, ('accepted_within_scope', crude_only)),
        ('contraction_failure_relabelled_limited', certify_outcome, ('limited', contraction_failed)),
        ('unproved_constant_relabelled_accepted', certify_outcome, ('accepted_within_scope', constant_unproved)),
        ('over_target_relabelled_accepted', certify_outcome, ('accepted_within_scope', over_target)),
    ], retained_outcomes={'crude_only': 'limited', 'contraction_failed': 'insufficient', 'constant_unproved': 'limited', 'over_target': 'limited'})
    control('exact_arithmetic_admission', [
        ('float_tau', tier_ii, (1e-08,)),
        ('bool_tau', tier_i, (True,)),
        ('nan_string', parse_q, ('NaN',)),
        ('float_bound_admission', admit_bound, (float(1), target)),
        ('zero_denominator', parse_q, ('1/0',)),
    ], note='every Boolean is decided on Fraction values; decimal strings are previews')
    orth_R_lo = sum((sqrt_bounds(n)[0] for n in owners_meeting.values()), Q(0))
    control('root_n_misuse', [
        ('sqrt_52_as_anchored_norm', certify_t1_over_coefficient, (sqrt_bounds(52)[1], COUNTS['orth_site_sum_lo'])),
        ('sqrt_88_as_R_sum', certify_t1_over_coefficient, (sqrt_bounds(88)[1], orth_R_lo)),
    ], owner_set_sqrt_sum_per_factor=[qs(COUNTS['orth_site_sum_lo']), qs(COUNTS['orth_site_sum_hi'])],
        note='the anchored norm is an l1 sum over owner sets of sqrt(n_M); a single square root of the face count is not a bound')
    control('no_priority_or_continuum_claim', [
        ('continuum_true', validate_claims, (dict(CLAIM_FLAGS, continuum_claim=True), LABEL)),
        ('weak_coupling_true', validate_claims, (dict(CLAIM_FLAGS, weak_coupling_claim=True), LABEL)),
        ('priority_true', validate_claims, (dict(CLAIM_FLAGS, scientific_priority_verified=True), LABEL)),
        ('interaction_shift_true', validate_claims, (dict(CLAIM_FLAGS, resolved_interaction_shift=True), LABEL)),
        ('euclidean_node_true', validate_claims, (dict(CLAIM_FLAGS, euclidean_node_certified=True), LABEL)),
        ('uniform_wilson_without_fixed_spacing_label', validate_claims, (CLAIM_FLAGS, 'uniform Wilson magnetic theory')),
    ])
    control('uniform_triple_in_box', [
        ('ends_only_triple', certify_uniform_triple_in_box, ((TAU_CAP / 24, Q(0), TAU_CAP / 24), TAU_CAP, HALF, Q(1, 8))),
        ('bridge_outside_box_tau_4', certify_uniform_triple_in_box, (uniform_triple(4), Q(4), HALF, Q(1, 8))),
        ('ends_outside_box_tau_16', certify_uniform_triple_in_box, (uniform_triple(16), Q(16), HALF, Q(1, 8))),
        ('two_entries', certify_uniform_triple_in_box, ((TAU_CAP / 24, TAU_CAP / 24), TAU_CAP, HALF, Q(1, 8))),
    ], uniform_triple_at_cap=[qs(x) for x in tri])
    control('selected_reference_not_haar', [
        ('haar_claimed_ground_route_a_plus', certify_haar_is_onsite_ground, ('A', TAU_CAP)),
        ('haar_claimed_ground_route_a_minus', certify_haar_is_onsite_ground, ('A', -TAU_CAP)),
    ], trial_energy_at_cap=qs(trial))
    control('reference_route_declared', [
        ('route_missing', certify_route, ({},)),
        ('route_a_with_haar', certify_route, ({'route': 'A', 'reference': 'haar', 'selected_faces_in': 'onsite'},)),
        ('route_b_selected_on_site', certify_route, (dict(route_packet, selected_faces_in='onsite'),)),
        ('route_b_without_single_factor_groups', certify_route, (dict(route_packet, groups=['whole_star']),)),
    ], declared=route_packet)
    control('per_site_sum_recomputed', [
        ('single_factor_group_dropped_28', certify_per_site_sum, (28, 'route_B', J_PER_TAU)),
        ('selected_merged_into_stars_32', certify_per_site_sum, (32, 'selected_in_star', J_PER_TAU)),
        ('one_star_7', certify_per_site_sum, (7, 'route_B', J_PER_TAU)),
        ('single_factor_counted_twice_30', certify_per_site_sum, (30, 'route_B', J_PER_TAU)),
    ], recomputed=qs(J_PER_TAU), box_N3_bulk=qs(j_bulk))
    control('reset_budget_recomputed', [
        ('aq2_verbatim_98', certify_reset, (98, Q(98, 6), ONSITE_GAP, reset_budget)),
        ('one_single_factor_group_100', certify_reset, (100, Q(100, 6), ONSITE_GAP, reset_budget)),
        ('single_factor_at_all_seven_anchors_112', certify_reset, (112, Q(112, 6), ONSITE_GAP, reset_budget)),
        ('gap_one_overlap', certify_reset, (102, 102, 1, reset_budget)),
    ], recomputed=qs(reset_budget), epsilon_R=qs(eps_R))
    control('selected_incidence_count', [
        ('seven_groups_from_R_minus_S', certify_selected_incidence, (7, 21, totals['single_factor_groups'], totals['selected_faces'])),
        ('zero_selected_groups', certify_selected_incidence, (0, 0, totals['single_factor_groups'], totals['selected_faces'])),
        ('origin_only', certify_selected_incidence, (1, 3, totals['single_factor_groups'], totals['selected_faces'])),
    ], derived_groups=totals['single_factor_groups'], derived_faces=totals['selected_faces'])
    control('first_order_faces_uniform', [
        ('omitted_only_49', certified_count, (DerivedCount(derived_counts['omitted_faces_per_factor'], 'I1_21_omitted_classes'), 'faces per factor')),
        ('contract_96_as_exact', certified_count, (DerivedCount(bound_per_factor, 'contract_text'), 'faces per factor')),
        ('hard_coded_52', certified_count, (52, 'faces per factor')),
        ('bound_96_used_as_exact', certify_labelled_bound, (bound_per_factor, derived_counts['faces_per_factor'], 'exact_enumeration')),
        ('scope_sites_0_and_e_z', certify_site_scope, ('sites_0_and_e_z',)),
    ], exact=derived_counts['faces_per_factor'], labelled_bound=bound_per_factor)
    control('uniform_label_strong_coupling', [
        ('weak_coupling_label', certify_label, ('uniform Kogut-Susskind SU(2) at fixed spacing, weak coupling', g4_cap, TAU_CAP)),
        ('continuum_label', certify_label, (LABEL + ' (continuum limit)', g4_cap, TAU_CAP)),
        ('g4_as_96_tau', certify_label, (LABEL, 96 * TAU_CAP, TAU_CAP)),
        ('g4_as_24_over_tau', certify_label, (LABEL, 24 / TAU_CAP, TAU_CAP)),
        ('label_without_fixed_spacing', certify_label, ('uniform Kogut-Susskind SU(2), strong bare coupling', g4_cap, TAU_CAP)),
    ], label=LABEL, g4_at_cap=qs(g4_cap))
    control('am2_gap_reuse_justified', [
        ('route_b_citing_frozen_J0', certify_am2_reuse, (dict(am2_record_b, J0=old_J0),)),
        ('gapless_onsite', certify_am2_reuse, (dict(am2_record_b, onsite_lower_gap=Q(0)),)),
        ('support_five', certify_am2_reuse, (dict(am2_record_b, max_support=5, termination_order=10),)),
        ('copied_order_six_termination', certify_am2_reuse, (dict(am2_record_b, termination_order=6),)),
        ('route_a_with_haar_reference', certify_am2_reuse, (dict(am2_record_a, reference='haar'),)),
        ('route_b_undercounted_J_28', certify_am2_reuse, (dict(am2_record_b, J_per_tau=Q(28), J0=old_J0),)),
    ])
    control('j0_resolution_declared', [
        ('old_J0_at_cap', validate_j0_resolution, ({'label': 'R1', 'cap': TAU_CAP, 'J0': old_J0, 'self_map': old_J0 * G_R_UP,
                                                    'contraction': 2 * old_J0 * GP_R_UP}, J_PER_TAU, TAU_CAP)),
        ('R2_changed_cap', validate_j0_resolution, ({'label': 'R2', 'cap': cparse['R2_cap'], 'J0': old_J0, 'self_map': old_J0 * G_R_UP,
                                                     'contraction': 2 * old_J0 * GP_R_UP}, J_PER_TAU, TAU_CAP)),
        ('contraction_not_declared', validate_j0_resolution, ({'label': 'R1', 'cap': TAU_CAP, 'J0': J0_PRIME, 'self_map': self_map}, J_PER_TAU, TAU_CAP)),
        ('stale_self_map_148_over_25000000', validate_j0_resolution, ({'label': 'R1', 'cap': TAU_CAP, 'J0': J0_PRIME, 'self_map': Q(148, 25000000),
                                                                      'contraction': contraction}, J_PER_TAU, TAU_CAP)),
    ], J0_prime=qs(J0_PRIME), self_map=qs(self_map), contraction=qs(contraction))
    control('uniform_sign_convention', [
        ('selected_positive_sign', certify_sign_convention, (FACE_COEFF_NORMALIZED, -FACE_COEFF_NORMALIZED)),
        ('selected_alpha_magnitude_in_normalized_packet', certify_sign_convention, (FACE_COEFF_NORMALIZED, FACE_COEFF_ALPHA)),
        ('omitted_flipped', certify_sign_convention, (-FACE_COEFF_NORMALIZED, FACE_COEFF_NORMALIZED)),
    ], convention='every face term is -(tau/3)W_f in H/delta (-(tau/24)W_f in H/alpha)')
    control('tier_mixing_rejected', [
        ('exact_a1_with_crude_remainder', assemble_epsilon, ('ii', {
            'a1': Term('a1', 1, 'ii', 'exact_first_order'), 'rho': Term('rho', 1, 'i', 'am2_majorant'),
            'T': Term('T', 1, 'ii', 'self_consistent')})),
        ('refined_t_without_self_consistency', assemble_epsilon, ('ii', {
            'a1': Term('a1', 1, 'ii', 'exact_first_order'), 'rho': Term('rho', 1, 'ii', 'self_consistent_remainder'),
            'T': Term('T', 1, 'ii', 'first_order_only')})),
        ('exact_first_order_inside_tier_i', assemble_epsilon, ('i', {'t': Term('t', 1, 'i', 'exact_first_order')})),
    ])
    inventory = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    must(validate_inventory(inventory, contract), 'reverse inputs inventory')
    control('reverse_premise_isolation', [
        ('skeptic_triage_added', validate_inventory, (inventory + ['research/round32/skeptic/triage.md'], contract)),
        ('loop2_response_added', validate_inventory, (inventory + ['research/round32/skeptic/loop2-response.md'], contract)),
        ('expert_file_added', validate_inventory, (inventory + ['research/round32/experts/modern/loop2-response.md'], contract)),
        ('forward_ax1_added', validate_inventory, (inventory + ['research/round32/forward/ax1/report.md'], contract)),
        ('deliberation_added', validate_inventory, (inventory + ['research/round32/advisor/deliberation-1.md'], contract)),
        ('premise_missing', validate_inventory, (inventory[1:], contract)),
    ], positive_inventory_equals_declared=True, inventory_size=len(inventory),
        declared_size=len({'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])))
    control('uniform_kappa_tied_to_tau', [
        ('kappa_absolute_value', certify_uniform_antisymmetry, ('absolute_value', TAU_CAP)),
        ('kappa_offset', certify_uniform_antisymmetry, ('offset', TAU_CAP)),
        ('kappa_double', certify_uniform_antisymmetry, ('double', TAU_CAP)),
        ('kappa_zero_selected', certify_uniform_antisymmetry, ('zero_selected', TAU_CAP)),
    ], accepted_rule='tied_tau_over_24', one_plaquette_rows=sign_rows)
    dup_rows = [dict(r) for r in rows]
    star0 = next(i for i, r in enumerate(dup_rows) if r['kind'] == 'whole_star' and r['anchor'] == ORIGIN)
    single0 = next(r for r in dup_rows if r['kind'] == 'single_factor' and r['anchor'] == ORIGIN)
    dup_rows[star0] = dict(dup_rows[star0], faces=dup_rows[star0]['faces'] + single0['faces'][:1])
    _, groups_dc = box_groups(2, 'double_count')
    control('route_b_no_double_count', [
        ('selected_face_in_star_and_single_factor_group', certify_no_double_count, (groups_dc,)),
        ('double_counted_per_site_sum_33', certify_per_site_sum, (bulk_per_site_sum('double_count')[0], 'double_count', J_PER_TAU)),
        ('incidence_table_with_duplicate', certify_incidence_table, (dup_rows, meeting_set)),
    ], double_count_per_site_sum=qs(bulk_per_site_sum('double_count')[0]))
    missing_rows = [r for r in rows if not (r['kind'] == 'whole_star' and r['anchor'] == (-1, 0, 0))]
    control('incidence_table_itemized', [
        ('asserted_totals_without_table', certify_incidence_table,
         ({'stars': 7, 'single_factor_groups': 2, 'selected_faces': 6, 'B_N': '51/8'}, meeting_set)),
        ('rows_without_faces', certify_incidence_table, ([dict(r, faces=[]) for r in rows], meeting_set)),
        ('incoming_star_minus_e_x_missing', certify_incidence_table, (missing_rows, meeting_set)),
    ], table_rows=len(rows))

    ids = [c['id'] for c in CHECKS]
    missing = [c for c in contract['controls'] if c not in ids]
    must(missing == [], 'contract controls without a check: ' + ','.join(missing))
    must(validate_claims(CLAIM_FLAGS, LABEL), 'claim flags')

    result = {
        'loop': 'AX1', 'direction': 'reverse', 'route': 'B (Haar reference; selected faces as single-factor interaction groups)',
        'human_author': 'Hruday N M (BUNZEEY)',
        'contribution_alias': 'HNM-AX1-R reverse route-B reconstruction for the uniform model',
        'attribution': {
            'creation_expansion': 'admitted AM2 construction (commuting-creation expansions; Bravyi-DiVincenzo-Loss 2008 as credited in the AM2 lineage; Gauvin arXiv:2503.15539v3 Supplement A.6-A.8 template)',
            'dynamics': 'Nachtergaele-Sims arXiv:1410.8174v1 Section 3/Theorem 4.1 as placed in AQ1',
            'centre_grading': 'Peter-Weyl/Z_2 centre flips of lattice gauge theory are established; no priority claimed',
            'scientific_priority': 'unverified'},
        'contract_snapshot_sha256': contract_sha, 'check_py_sha256': check_py_sha,
        'model': contract['model'], 'model_label': LABEL,
        'dictionary': {'alpha': 'g^2/(2a)', 'lambda': '2/(g^2 a)', 'nu': 'lambda = alpha*tau/24', 'tau': '96/g^4',
                       'g4_at_cap': qs(g4_cap), 'normalized_face_coefficient': '-(tau/3) W_f', 'physical_gap': 'alpha/16 = g^2/(32a)'},
        'target': {'quantity': 'D_ii (uniform, route B) at the cap', 'value': qs(target), 'comparator': '<=',
                   'read_from': 'contract preregistration.target'},
        'reference_values': {'omega_0(W)': qs(HAAR_W), 'omega_0(W^2)': qs(HAAR_W2), 'route': 'haar'},
        'j0_resolution': {'resolution': 'R1', 'J0_prime': qs(J0_PRIME), 'J_prime_at_cap': qs(J_PER_TAU * TAU_CAP),
                          'frozen_AM2_J0': qs(old_J0), 'G_R_upper': qs(G_R_UP), 'G_prime_R_upper': qs(GP_R_UP),
                          'self_map_upper': qs(self_map), 'radius': qs(R_RADIUS), 'contraction_upper': qs(contraction),
                          'R2_changed_cap_not_selected': qs(cparse['R2_cap']),
                          'contract_source': 'inputs/' + CONTRACT_REL, 'contract_sha256': contract_sha},
        'grouping': {'per_site_sum_per_tau': qs(J_PER_TAU), 'stars': '4 x 7|tau|', 'single_factor': '1 x |tau|',
                     'max_support': MAX_SUPPORT, 'termination_order': 8, 'alternatives': alt},
        'incidence': {'table': table_out, 'totals': {k: (qs(v) if isinstance(v, Q) else v) for k, v in totals.items()}},
        'face_enumeration': {'derived': derived_counts, 'labelled_bounds': {'per_factor': bound_per_factor, 'R': bound_R},
                             'owner_set_face_counts_per_factor': sorted(n_by_owner.values()), 'boxes': box_info},
        'reset': {'budget_per_tau': qs(reset_budget), 'epsilon_R_per_tau': qs(eps_R), 'reference_gap': qs(ONSITE_GAP)},
        'checklist': checklist,
        'tiers': {k: {s: strip(v) for s, v in d.items()} for k, d in tiers.items()},
        'D_prime_i': {'+': qs(D_i), '-': qs(tiers['tier_i']['-']['_D']), 'preview': sci(D_i), 'form': 'exact rational 2*eps_i (fidelity route)'},
        'D_prime_ii': {'+': qs(D_ii), '-': qs(tiers['tier_ii']['-']['_D']), 'preview': sci(D_ii),
                       'form': 'exact rational 2*eps_ii with the exact counts 52 and 88 (fidelity route)',
                       'density_form_both_inequalities': tiers['tier_ii']['+']['D_density_form_exact'],
                       'labelled_bound_96_168_variant': tiers['tier_ii_labelled_bound_96_168']['+']['D_exact_2eps']},
        'tier_ii_target_met': admit_bound(D_ii, target) and admit_bound(tiers['tier_ii']['-']['_D'], target),
        'tier_i_target_met': D_i <= target,
        'ax2_feasibility': {'threshold_bracket': [qs(thr[0]), qs(thr[1])], 'contract_stated': qs(stated),
                            'D_prime_ii_feasible': ax2_feasible(D_ii, relation, TAU_CAP)},
        'error_terms_itemized': ledger,
        'transfer': transfer,
        'consequences': consequences,
        'producer_outcome': outcome,
        'sub_label': 'uniform_local_closeness_not_uniqueness',
        'outcome_note': 'proposed for review; admission requires the forward route, the exchange and the skeptical review',
        'claim_exclusions': contract['claim_exclusions'],
        'preregistered_claim_exclusions': contract['preregistration']['claim_exclusions'],
        'limitations': [
            'fixed spacing, strong bare coupling |tau|<=10^-8 (g^4>=9.6x10^9); tau<0 is the U_E image of the tau>0 model, not a real-g Kogut-Susskind coupling',
            'finite-volume gap uniform over centred whole-star boxes; AQ statements are about every subsequential limit (no uniqueness, whole-sequence convergence or rate in N)',
            'whole-star box boundary (selected faces of every factor kept); not identified with the all-contained-plaquette boundary (AL1)',
            'inherited without re-proof: AM2 multilinear majorant, fixed point, exclusion and cutoff passage (re-instantiated with J_0 prime), AQ1 compactness and Nachtergaele-Sims dynamics, AQ2 Fourier gap passage, AV1 product split, cutoff-vector removal and AQ passage, I1 dictionary',
            'route-A cross-check of the gap rests on the inherited A1 strip theorem, which this producer did not read',
            'upper certificates only; no value or sign of omega(W) beyond |omega(W)|<=D prime; the first-order coefficient transfers but K_2 is not re-derived',
            "headline D'_ii=2eps rests on the fidelity inequality; the density form is certified by both admitted inequalities",
            'the contract candidates 96 and 168 are anchor-group bounds, not the exact counts 52 and 88',
            "the contract's rounded AX2 threshold 4.19x10^-7 is itself infeasible; the exact threshold is about 4.18831x10^-7",
            'the contract text states the grouping, 29|tau|, J_0 prime and the rationals; they were recomputed, not discovered blind',
            'fixtures are finite graphs or algebras (transfers_to_aq false)',
            'scientific priority unverified'],
        'reads_disclosure': {
            'inputs': 'only the inputs/ snapshots, contract first',
            'extra_inherited': ['research/round32/tools/README.md', 'research/round32/tools/freeze.py',
                                'research/round32/reverse/av1/check.py (code style)', 'research/round32/reverse/aw1/check.py (line count only)'],
            'scratchpad': 'private folder /tmp/claude-0/ax1-reverse-private only; no other scratchpad file read'},
        'checks': CHECKS,
    }
    result.update(CLAIM_FLAGS)
    return result


def main():
    ap = argparse.ArgumentParser(description='HNM-AX1 reverse producer checker (exact arithmetic)')
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
               if p.is_file() and (p.relative_to(HERE).parts[0] == 'inputs' or p.name == 'check.py')}
    manifest = {'loop': 'AX1', 'direction': 'reverse', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AX1', 'direction': 'reverse', 'checks': len(result['checks']),
                      'D_prime_i': result['D_prime_i']['preview'], 'D_prime_ii': result['D_prime_ii']['preview'],
                      'tier_ii_target_met': result['tier_ii_target_met'], 'outcome': result['producer_outcome']},
                     sort_keys=True))


if __name__ == '__main__':
    main()
