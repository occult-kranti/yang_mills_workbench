#!/usr/bin/env python3
"""HNM-AY1 reverse producer: uniform local closeness of all subsequential limits of
two named construction families and their common first-order reduced density on the
cover R={0,e_z}, by the vacuum-overlap / fidelity route (reverse reconstruction).

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production (Claude,
an AI model) under premise isolation; HNM labels are project aliases. Fidelity,
Bures-angle and Fuchs-van de Graaf inequalities, commuting-creation expansions and
Peter-Weyl selection rules are established mathematics; scientific priority is
unverified.

Standard library only (argparse, fractions, hashlib, json, math, pathlib, re). Exact
Fraction arithmetic decides every Boolean; decimal strings are truncated previews.
Every contract control is implemented as damaging mutations whose rejection is
required. Failures are explicit exceptions (never assert), so the run and its output
bytes are identical under python -O.

Usage: python3 -B research/round32/reverse/ay1/check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import math
import re
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUTS = HERE / 'inputs'
CONTRACT_REL = 'research/round32/contracts/ay1.json'
CONTRACT_SHA256 = 'be9b354420e66e7edba03d59b3d194b69f26782b44cfb63cb10e176bf4879ae0'
AM2_GATE_REL = 'research/round29/advisor/am2-gate.json'
AV1_GATE_REL = 'research/round32/advisor/av1-gate.json'
AW1_GATE_REL = 'research/round32/advisor/aw1-gate.json'
AW2_GATE_REL = 'research/round32/advisor/aw2-gate.json'
AX1_GATE_REL = 'research/round32/advisor/ax1-gate.json'
AQ1_REL = 'research/round29/forward/aq1/report.md'
AM2_FWD_REL = 'research/round29/forward/am2/report.md'
I1_REL = 'research/round21/forward/i1/report.md'
DEN = 10 ** 40
FORBIDDEN_PREFIXES = (
    'research/round32/forward/ay1/',
    'research/round32/reverse/ay1/',
    'research/round32/skeptic/ay1',
    'research/round32/skeptic/triage',
    'research/round32/experts/',
    'research/round32/advisor/deliberation-',
    'research/round32/advisor/panel',
)
F1_NAME = 'centered whole-star boxes Lambda_N (AQ1)'
F2_NAME = 'all-contained-face boxes with padding (I1 section 6)'
STATES_TOPOLOGY = 'trace norm on B(H_R)'
DYNAMICS_TOPOLOGY = 'operator norm on bounded local observables, uniformly on compact time windows'


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
    if isinstance(value, str) and re.fullmatch(r'[+-]?[0-9]+(/[1-9][0-9]*)?', value):
        return Q(value)
    raise AdmissionError('malformed rational input rejected: ' + repr(value))


def qs(x):
    return str(Q(x))


def ceil_to(x, den=DEN):
    x = Q(x)
    return Q(-((-x.numerator * den) // x.denominator), den)


def floor_to(x, den=DEN):
    x = Q(x)
    return Q((x.numerator * den) // x.denominator, den)


def sqrt_bounds(y):
    """Directed rational enclosure lo<=sqrt(y)<=hi at resolution 10^-40."""
    y = Q(y)
    must(y >= 0, 'negative square-root argument')
    scaled = y.numerator * DEN * DEN
    s = math.isqrt(scaled // y.denominator)
    lo = Q(s, DEN)
    hi = lo if s * s * y.denominator == scaled else Q(s + 1, DEN)
    must(lo * lo <= y and y <= hi * hi, 'square-root enclosure failed')
    return lo, hi


def factorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


def exp_bounds(x, terms=24):
    """Directed enclosure of exp(x), 0<=x<=1/2: partial sum plus geometric tail."""
    x = Q(x)
    must(Q(0) <= x and x <= Q(1, 2), 'exponential argument outside [0,1/2]')
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


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact(x):
    return {'exact': qs(x), 'preview': sci(x)}


# ------------------------------------------------------- SU(2) Haar and units
HALF = Q(1, 2)


def spin0_multiplicity(n):
    """Multiplicity of spin 0 in (1/2)^{tensor n}, by the Clebsch-Gordan recursion on 2j."""
    dist = {0: 1}
    for _ in range(n):
        new = {}
        for tj, m in dist.items():
            for nt in (tj - 1, tj + 1):
                if nt >= 0:
                    new[nt] = new.get(nt, 0) + m
        dist = new
    return dist.get(0, 0)


def haar_W_moment(n):
    return Q(spin0_multiplicity(n), 2 ** n)


CASIMIR_HALF = HALF * (HALF + 1)                           # 3/4
FACE_ENERGY = {'delta': 8 * 4 * CASIMIR_HALF, 'alpha': 4 * CASIMIR_HALF}   # 24 and 3
FACE_COUPLING_PER_TAU = {'delta': -Q(1, 3), 'alpha': -Q(1, 24)}             # I1.5 per face
CLOCK_EXPONENT = {'alpha': FACE_ENERGY['alpha'], 'delta': FACE_ENERGY['delta']}


def raw_first_order_amplitude(coupling_units, energy_units):
    return FACE_COUPLING_PER_TAU[coupling_units] / FACE_ENERGY[energy_units]


def certify_first_order_amplitude(value):
    require(value == -Q(1, 72), 'first-order creation amplitude per face must be -tau/72 in one consistent unit system; got ' + qs(value))
    return value


def certify_clock(clock, exponent):
    require(clock in ('s=alpha*t_E/hbar', 'theta=alpha*t/hbar'), 'clock is not the common preregistered clock: ' + clock)
    require(exponent == CLOCK_EXPONENT['alpha'], 'W Omega_0 energy on the alpha clock is 3, not ' + qs(exponent))
    return True


# ------------------------------------------------------------ lattice geometry
DIRS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
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
    """Re-derive the 24 anchored classes from pi and the link tails (I1.1, I1.4)."""
    rows = []
    for r in range(4):
        for s in range(2):
            p = (r, s, 0)
            for name, a, c in ORIENTATIONS:
                owners = tuple(sorted({coarse(t) for t, _ in face_links(p, a, c)}))
                selected = name == 'xy' and s == 0 and r in (0, 1, 2)
                rows.append((name, r, s, owners, 'selected' if selected else 'omitted'))
    return sorted(rows)


def class_face(anchor, cls):
    name, r, s, support, _ = cls
    a, c = {n: (x, y) for n, x, y in ORIENTATIONS}[name]
    p = (4 * anchor[0] + r, 2 * anchor[1] + s, anchor[2])
    links = face_links(p, a, c)
    owners = tuple(sorted(vadd(anchor, v) for v in support))
    must(tuple(sorted({coarse(t) for t, _ in links})) == owners, 'owner set differs from the link tails')
    return links, owners


def faces_touching(u, classes):
    """Every omitted face (anchor, class index) whose owner set contains factor u."""
    out = {}
    for k, cls in enumerate(classes):
        for d in cls[3]:
            b = vsub(u, d)
            out[(b, k)] = class_face(b, cls)
    return out


def box_sites(N):
    rng = range(-N, N + 1)
    return [(x, y, z) for x in rng for y in rng for z in rng]


def f1_faces(N, classes):
    """AQ1 family: omitted faces of whole stars b+S contained in Lambda_N (I1.6)."""
    sites = set(box_sites(N))
    out = {}
    for b in sorted(sites):
        if all(vadd(b, v) in sites for v in STAR):
            for k, cls in enumerate(classes):
                out[(b, k)] = class_face(b, cls)
    return out


def f2_faces(N, classes):
    """I1 section-6 family: every omitted face whose actual owner set lies in Lambda_N."""
    sites = set(box_sites(N))
    out = {}
    for b in sorted(sites):
        for k, cls in enumerate(classes):
            links, owners = class_face(b, cls)
            if all(o in sites for o in owners):
                out[(b, k)] = (links, owners)
    return out


def certify_cover(cover, n_links, n_endpoints):
    require(tuple(sorted(cover)) == COVER, 'cover must be the complete factor cover R={0,e_z} of W')
    require(n_links == 48 and n_endpoints == 36, 'complete cover has 48 links and 36 endpoints')
    return True


def factor_links(b):
    out = set()
    for r in range(4):
        for s in range(2):
            t = (4 * b[0] + r, 2 * b[1] + s, b[2])
            for d in range(3):
                out.add((t, d))
    return out


def certify_incident_anchors(anchors):
    expected = {vsub(u, s) for u in COVER for s in STAR}
    require(set(anchors) == expected and len(expected) == 7,
            'incident anchors must be the seven sites R-S (incoming stars included)')
    return True


def certify_J_per_tau(j_per_tau, stars_per_site, star_norm_per_tau):
    require(stars_per_site == len(STAR), 'every site lies in |S|=4 stars (incoming stars included)')
    require(j_per_tau == stars_per_site * star_norm_per_tau and j_per_tau == 28, 'J=28|tau| from four stars of norm 7|tau|')
    return True


def certify_reset_R(reset_per_tau, incident, group_norm_per_tau):
    require(incident == 7, 'reset must charge all seven incident groups')
    require(reset_per_tau == 2 * incident * group_norm_per_tau, 'reset changes each incident group by at most twice its norm')
    return True


# ---------------------------------------------------- padded-family validator
def validate_padded_family(rec):
    """I1 section 6: every hypothesis the AM2 contraction uses, for one padded box."""
    B = rec['volume_B']
    V = rec['am2_volume']
    groups = rec['groups']
    seen = {}
    for b, faces in groups.items():
        for f, owners in faces.items():
            require(all(o in B for o in owners), 'face with actual support outside B retained: not the all-contained-face family')
            require(f not in seen, 'face counted in two groups: per-site sum and norms invalid')
            seen[f] = b
            require(f[0] == b, 'face grouped away from its anchor')
    for b, X in rec['indexed_supports'].items():
        require(len(X) <= 4, 'indexed support larger than four sites: AM2 constants do not apply')
        require(all(x in V for x in X), 'indexed support leaves the AM2 volume: padding missing')
    for x in rec['interacting_padded_sites']:
        require(x not in B, 'site list malformed')
    require(len(rec['interacting_padded_sites']) == 0, 'padded sites interact: the padding does not decouple')
    norms = {b: Q(len(faces), 3) for b, faces in groups.items()}
    require(all(n <= 7 for n in norms.values()), 'group norm exceeds 7|tau|')
    per_site = {}
    for b, X in rec['indexed_supports'].items():
        for x in X:
            per_site[x] = per_site.get(x, Q(0)) + norms.get(b, Q(0))
    j_per_tau = max(per_site.values())
    require(j_per_tau <= 28, 'per-site indexed sum exceeds 28|tau|: J_0 not met')
    max_support = max(len(X) for X in rec['indexed_supports'].values())
    require(rec['termination_order_claim'] == 2 * max_support, 'termination order must be 2*max|X|=8')
    incident = [b for b, X in rec['indexed_supports'].items() if any(u in X for u in COVER)]
    reset_needed = 2 * sum(norms[b] for b in incident)
    require(rec['reset_R_claim'] >= reset_needed, 'reset budget below the incident groups actually meeting R')
    require(rec['reset_R_claim'] <= 98, 'reset budget above the seven-group value')
    return {'J_per_tau': j_per_tau, 'max_support': max_support, 'termination': 2 * max_support,
            'incident_groups': len(incident), 'reset_R_needed_per_tau': reset_needed}


def padded_record(N, classes):
    B = set(box_sites(N))
    faces = f2_faces(N, classes)
    groups = {}
    for (b, k), (links, owners) in faces.items():
        groups.setdefault(b, {})[(b, k)] = owners
    indexed = {b: tuple(vadd(b, v) for v in STAR) for b in groups}
    Bplus = set(B)
    for b in B:
        for v in STAR:
            Bplus.add(vadd(b, v))
    return {'volume_B': B, 'am2_volume': Bplus, 'groups': groups, 'indexed_supports': indexed,
            'interacting_padded_sites': [], 'termination_order_claim': 8, 'reset_R_claim': Q(98)}


# ------------------------------------------------ creation-algebra termination
def four_qubit_termination():
    """ad_C^k(V) Omega for C=sum sigma^+_i on four qubits and V=|0000><1111|+h.c.: order 8 is the last."""
    n = 4
    dim = 2 ** n

    def create(state):
        out = {}
        for i in range(n):
            if not (state >> i) & 1:
                out[state | (1 << i)] = out.get(state | (1 << i), 0) + 1
        return out

    def mat_C():
        return {(t, s): v for s in range(dim) for t, v in create(s).items()}

    def mul(A, B):
        out = {}
        for (i, k), a in A.items():
            for (k2, j), b in B.items():
                if k == k2:
                    out[(i, j)] = out.get((i, j), 0) + a * b
        return {k: v for k, v in out.items() if v != 0}

    def sub(A, B):
        out = dict(A)
        for k, v in B.items():
            out[k] = out.get(k, 0) - v
        return {k: v for k, v in out.items() if v != 0}

    C = mat_C()
    V = {(0, dim - 1): 1, (dim - 1, 0): 1}
    ad = V
    coeffs = {}
    for k in range(1, 10):
        ad = sub(mul(C, ad), mul(ad, C))
        coeffs[k] = sum(v for (i, j), v in ad.items() if j == 0 and i == dim - 1)
        if k == 9:
            coeffs['ad9_zero'] = len(ad) == 0
    return coeffs


def certify_termination(order, max_support):
    require(order == 2 * max_support, 'nested commutators vanish only beyond 2*max|X|; order ' + str(order) + ' claimed')
    return True


# --------------------------------------------------------- tier (ii) constants
def tier_ii(tau, remainder='contract_352', G_prime_up=Q(352)):
    at = abs(parse_q(tau))
    a = at / 144
    J = 28 * at
    t1 = 49 * a
    must(G_prime_up * J < 1, 'self-consistency needs 352J<1')
    T = t1 / (1 - G_prime_up * J)
    if remainder == 'contract_352':
        rho = G_prime_up * J * T
    elif remainder == 'directed_288':
        must(8 * T < 1, 'directed exponential needs 8T<1')
        rho = 288 * J * T / (1 - 8 * T)
    else:
        raise ProducerError('unknown remainder form')
    return {'tau_abs': at, 'a': a, 'J': J, 't1': t1, 'T': T, 'rho': rho}


def eps_admitted(c):
    return 2 * c['T'] + c['T'] ** 2


def eps_R_local(c):
    a, rho = c['a'], c['rho']
    return 82 * a + 2 * rho + (33 * a + rho) ** 2


def density_bound(eps):
    return 2 * eps * (1 + eps) / (1 + eps ** 2)


def bures_pair_bound(eps):
    return 4 * eps / (1 + eps ** 2)


def fidelity_bound_up(eps):
    lo, _ = sqrt_bounds(1 + eps ** 2)
    return ceil_to(2 * eps / lo)


def fidelity_bound_lo(eps):
    _, hi = sqrt_bounds(1 + eps ** 2)
    return floor_to(2 * eps / hi)


class Term:
    __slots__ = ('name', 'value', 'tier', 'provenance')

    def __init__(self, name, value, tier, provenance):
        self.name, self.value, self.tier, self.provenance = name, Q(value), tier, provenance


LEDGER_ITEMS = ('am2_remainder', 'straddling', 'two_creation', 'density', 'normalization')


def assemble_ledger(terms, combine='linear'):
    require(sorted(t.name for t in terms) == sorted(LEDGER_ITEMS), 'ledger must itemize every AW1 remainder item exactly once')
    tiers = {t.tier for t in terms}
    require(tiers == {'ii'}, 'tier mixing: every ledger item must carry tier (ii)')
    require(all(t.value > 0 for t in terms if t.name != 'normalization') and all(t.value >= 0 for t in terms),
            'a ledger item is zero or negative (charged at its positive majorant)')
    require(combine == 'linear', 'ledger items add linearly (triangle inequality); root-sum-square is a root-n misuse')
    return sum(t.value for t in terms)


def trace_norm_ledger(tau, inR='triangle', remainder='contract_352', eps_mode='R_local', straddle_faces=72,
                      pair_faces=33, tier_override=None, crude_t=None):
    c = tier_ii(tau, remainder)
    a, T, rho = c['a'], c['T'], c['rho']
    if crude_t is not None:
        T_str = crude_t
    else:
        T_str = T
    eps = eps_R_local(c) if eps_mode == 'R_local' else eps_admitted(c)
    if inR == 'triangle':
        in_R = 2 * rho
    elif inR == 'orthogonal_sectors':
        in_R = sqrt_bounds(2)[1] * rho
    else:
        raise ProducerError('unknown in-R mode')
    tier = tier_override or 'ii'
    terms = [
        Term('am2_remainder', 2 * in_R, 'ii', 'AM2 remainder of c_R, c_{0}, c_{e_z} at both sites of R (anchored rho=352JT)'),
        Term('straddling', 2 * T_str * (straddle_faces * a + 2 * rho), tier if crude_t is not None else 'ii',
             'straddling supports: outside excitation <= T (AW1 R15) times the 72 first-order faces meeting R outside R plus 2rho'),
        Term('two_creation', 2 * (pair_faces * a + rho) ** 2, 'ii', 'disjoint pairs I>0, J>e_z: (33a+rho)^2'),
        Term('density', 2 * eps ** 2, 'ii', 'diagonal defect plus excited block: 2(1-F)<=2eps^2, eps R-local (82 faces)'),
        Term('normalization', 2 * eps ** 2 * 10 * a, 'ii', 'first-order vector times e^2/(1+e^2); ||c^(1)_R||<=10a (third order)'),
    ]
    total = assemble_ledger(terms)
    return {'constants': c, 'eps': eps, 'terms': terms, 'total': total, 'K2_prime': total / c['tau_abs'] ** 2}


def ledger_json(led):
    at2 = led['constants']['tau_abs'] ** 2
    return {'items': {t.name: {'exact': qs(t.value), 'over_tau_squared_preview': sci(t.value / at2), 'tier': t.tier,
                               'provenance': t.provenance} for t in led['terms']},
            'eps': exact(led['eps']), 'total': exact(led['total']), 'K2_prime': exact(led['K2_prime'])}


# --------------------------------------------------- first-order density on R
def certify_first_order_density(rho1, F_R, pairing):
    """rho1: {(i,j): coefficient} in the orthonormal basis e_O=Omega_R, e_f=2 W_f Omega_R."""
    for (i, j), v in rho1.items():
        require(i == 'O' or i in F_R, 'first-order density has a leg outside H_R (non-R face)')
        require(j == 'O' or j in F_R, 'first-order density has a leg outside H_R (non-R face)')
    for (i, j), v in rho1.items():
        require(rho1.get((j, i), Q(0)) == v, 'first-order density is not Hermitian (adjoint term dropped)')
    require(rho1.get(('O', 'O'), Q(0)) == 0, 'first-order diagonal is nonzero: contradicts the derivative of the fidelity identity')
    require(all(v == 0 for (i, j), v in rho1.items() if i != 'O' and j != 'O'),
            'first-order excited block is nonzero: contradicts positivity with Tr(1-P)rho(1-P)<=eps^2')
    for f in F_R:
        require(rho1.get((f, 'O'), Q(0)) == Q(1, 144), 'coefficient of |e_f><Omega_R| must be 1/144 (amplitude 1/72 times ||W_f Omega_R||=1/2)')
    trW = pairing(rho1, 'W')
    require(trW == Q(1, 144), 'Tr(rho^(1) W) must equal the AW1-admitted +1/144; got ' + qs(trW))
    return trW


# --------------------------------------------------------- finite fixtures
def fx_ground(c):
    """Exact ground vector prod_I (1 - c_I-hat) Omega on four qubit sites (0, e_z, o1, o2)."""
    vec = {(0, 0, 0, 0): Q(1)}
    for I in sorted(c):
        out = dict(vec)
        for st, cf in vec.items():
            if all(st[s] == 0 for s in I):
                n = list(st)
                for s in I:
                    n[s] = 1
                n = tuple(n)
                out[n] = out.get(n, Q(0)) - c[I] * cf
        vec = {k: v for k, v in out.items() if v != 0}
    return vec


def fx_apply(I, amp, vec):
    out = {}
    for st, cf in vec.items():
        if all(st[s] == 0 for s in I):
            n = list(st)
            for s in I:
                n[s] = 1
            n = tuple(n)
            out[n] = out.get(n, Q(0)) + amp * cf
    return {k: v for k, v in out.items() if v != 0}


RBASIS = ((0, 0), (0, 1), (1, 0), (1, 1))


def fx_rho_R(psi):
    nn = sum(v * v for v in psi.values())
    M = {(i, j): Q(0) for i in RBASIS for j in RBASIS}
    for s1, v1 in psi.items():
        for s2, v2 in psi.items():
            if s1[2:] == s2[2:]:
                M[(s1[:2], s2[:2])] += v1 * v2
    return {k: v / nn for k, v in M.items()}, nn


def fx_partial_overlap(psi, phi_out):
    """(1_R (x) <phi_out|) psi as a vector on H_R."""
    out = {i: Q(0) for i in RBASIS}
    for st, v in psi.items():
        out[st[:2]] += v * phi_out.get(st[2:], Q(0))
    return out


def fx_env(lam, u, u2, v0, vz, s1, s2, s3, w, v1):
    return {(0, 1): lam * u + lam * lam * u2, (0,): lam * lam * v0, (1,): lam * lam * vz,
            (0, 2): lam * s1, (1, 3): lam * s2, (0, 1, 2): lam * s3, (2, 3): lam * w, (2,): lam * lam * v1}


def fx_analyse(c, lam, u):
    psi = fx_ground(c)
    rho, nn = fx_rho_R(psi)
    out_c = {I: v for I, v in c.items() if not (set(I) & {0, 1})}
    phi_full = fx_ground(out_c)
    phi_out = {st[2:]: v for st, v in phi_full.items()}
    vac_proj = {st[2:]: v for st, v in psi.items() if st[:2] == (0, 0)}
    split_ok = vac_proj == phi_out
    n2 = sum(v * v for v in phi_out.values())
    overlap = fx_partial_overlap(psi, phi_out)
    identity_ok = all(rho[(i, (0, 0))] == overlap[i] / nn for i in RBASIS)
    psi_out = {(0, 0) + k: v for k, v in phi_out.items()}
    delta = dict(psi)
    for k, v in psi_out.items():
        delta[k] = delta.get(k, Q(0)) - v
    delta = {k: v for k, v in delta.items() if v != 0}
    e2 = sum(v * v for v in delta.values()) / n2
    fidelity_ok = rho[((0, 0), (0, 0))] == 1 / (1 + e2)
    parts = {'in_R': {}, 'straddling': {}, 'pairs': {}}
    meet = [I for I in c if set(I) & {0, 1}]
    for I in meet:
        key = 'in_R' if set(I) <= {0, 1} else 'straddling'
        for k, v in fx_apply(I, -c[I], psi_out).items():
            parts[key][k] = parts[key].get(k, Q(0)) + v
    for I in meet:
        for J in meet:
            if 0 in I and 1 not in I and 1 in J and 0 not in J and not (set(I) & set(J)):
                for k, v in fx_apply(I, c[I], fx_apply(J, c[J], psi_out)).items():
                    parts['pairs'][k] = parts['pairs'].get(k, Q(0)) + v
    recomposed = {}
    for p in parts.values():
        for k, v in p.items():
            recomposed[k] = recomposed.get(k, Q(0)) + v
    recomposed = {k: v for k, v in recomposed.items() if v != 0}
    delta_ok = recomposed == delta
    xi = {key: {i: w / n2 for i, w in fx_partial_overlap(p, phi_out).items()} for key, p in parts.items()}
    xi_total = {i: sum(xi[key][i] for key in xi) for i in RBASIS}
    offdiag_ok = xi_total[(0, 0)] == 0 and all(rho[(i, (0, 0))] == xi_total[i] / (1 + e2) for i in RBASIS if i != (0, 0))
    first = lam * u
    xi['in_R'][(1, 1)] += first                     # subtract the first-order part -c^(1)_R
    norms2 = {key: sum(w * w for w in v.values()) for key, v in xi.items()}
    anch = max(sum(abs(v) for I, v in c.items() if x in I) for x in range(4))
    in_R = abs(c[(0, 1)] - first) + abs(c[(0,)]) + abs(c[(1,)])
    strad = sum(abs(v) for I, v in c.items() if (set(I) & {0, 1}) and (set(I) - {0, 1}))
    s0 = sum(abs(v) for I, v in c.items() if 0 in I and 1 not in I)
    sz = sum(abs(v) for I, v in c.items() if 1 in I and 0 not in I)
    eps = sum(abs(v) for I, v in c.items() if set(I) & {0, 1}) + s0 * sz
    items = {'in_R': in_R, 'straddling': anch * strad, 'pairs': s0 * sz}
    X = dict(rho)
    X[((0, 0), (0, 0))] -= 1
    X[((1, 1), (0, 0))] += first
    X[((0, 0), (1, 1))] += first
    tr_X2 = sum(v * v for v in X.values())
    bound = 2 * (in_R + anch * strad + s0 * sz) + 2 * eps * eps * (1 + abs(first))
    return {'rho': rho, 'split_ok': split_ok, 'identity_ok': identity_ok, 'fidelity_ok': fidelity_ok, 'offdiag_ok': offdiag_ok,
            'delta_expansion_ok': delta_ok, 'e2': e2, 'eps': eps, 'xi_part_norm_sq': norms2, 'items': items,
            'tr_X2': tr_X2, 'bound': bound, 'first_order_trace_norm': 2 * abs(first)}


def certify_item(component_norm_sq, item):
    require(item >= 0 and component_norm_sq <= item * item, 'ledger item below its component (item undercounts)')
    return True


# ------------------------------------------------------------ claim validators
GATE_FIELDS = ('uniqueness_claimed', 'whole_sequence_claimed', 'rate_claimed', 'translation_invariance_claimed',
               'boundary_independence_of_dynamics_claimed')
FIXED_FALSE_FLAGS = ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified') + GATE_FIELDS


def validate_claim_flags(flags):
    for k in FIXED_FALSE_FLAGS:
        require(flags.get(k) is False, 'claim flag must be false: ' + k)
    return True


def certify_topologies(states, dynamics):
    require(states == STATES_TOPOLOGY, 'states must be compared in trace norm on B(H_R), not ' + states)
    require(dynamics == DYNAMICS_TOPOLOGY, 'dynamics topology must be the norm on compact time windows, not ' + dynamics)
    require(states != dynamics, 'the two topologies must be named separately')
    return True


def certify_limit_is_state(mass):
    require(mass == 1, 'weak-* limit on finite-rank observables lost mass ' + qs(1 - mass) + ': not a state; trace norm with tightness is required')
    return True


def certify_families(families):
    require(list(families) == [F1_NAME, F2_NAME], 'exactly the two named construction families are compared: ' + json.dumps(list(families)))
    return True


def certify_family_is_F2(face_set, f2_set, f1_set):
    require(face_set == f2_set, 'face set is not the all-contained-face family (I1 section 6)')
    require(face_set != f1_set, 'family collapsed onto F1 (whole-star rule applied): not the named F2')
    return True


def certify_sequence_claim(claim, limits):
    if claim == 'whole_sequence_converges':
        require(len(set(limits)) == 1, 'whole-sequence convergence claimed while two subsequential limits differ')
    require(claim in ('whole_sequence_converges', 'every subsequential limit', 'a chosen subsequential limit'), 'unknown quantifier')
    return True


def certify_equality_claim(x, y, basis):
    require(basis == 'exact identity', 'closeness or a common enclosing interval is not equality (basis: ' + basis + ')')
    require(x == y, 'claimed equality is false')
    return True


def certify_comparison(tau1, tau2, clock1, clock2, order):
    require(tau1 == tau2, 'limits compared at different couplings: the common first-order density needs the same tau')
    require(clock1 == clock2 == 's=alpha*t_E/hbar', 'limits compared on different clocks (common clock required)')
    require(order in (1, 2), 'closeness order must be 1 or 2')
    return True


def certify_closeness_constant(value, provenance, D_ii):
    require(provenance == 'AV1 admitted tier (ii) D_ii (forward exact, certified by both inequalities)',
            'closeness constant must use the single AV1 admitted tier, not ' + provenance)
    require(value == 2 * D_ii, 'closeness constant must be exactly 2*D_ii')
    return True


def certify_uniformity(parameter):
    require(parameter in ('box size N', 'on-site cutoff L', 'construction family', 'subsequence'),
            'bounds are uniform in N (and cutoff, family, subsequence) at fixed spacing a; not uniform in ' + parameter)
    return True


def certify_state_budget(budget, lower):
    require(budget >= lower, 'claimed ||rho_R-P_R||_1 budget is below the proved first-order size: first-order mean not charged')
    return True


def certify_trace_norm_constant(value, provenance):
    require(provenance == 'trace-norm ledger over B(H_R)', 'a single-observable (scalar) constant is not a trace-norm constant: ' + provenance)
    return True


def certify_scaling(ratio, order):
    bands = {1: (Q(99), Q(101)), 2: (Q(9900), Q(10100))}
    require(order in bands, 'unknown order')
    lo, hi = bands[order]
    require(lo <= ratio <= hi, 'tau -> tau/100 ratio ' + sci(ratio, 8) + ' is not order ' + str(order))
    return True


def certify_centering(label, residue, m, d):
    expected = {'vector': d * d, 'scalar': -2 * m * d - d * d, 'uncentered': m * m}
    require(label in expected and residue == expected[label], 'centering residue mislabelled')
    require(label == 'vector', 'only vector centering removes the mean from the correlation vector')
    return True


def certify_model(tau, triple, model_id, j_per_tau, family):
    t = parse_q(tau)
    require(abs(t) <= TAU_CAP, 'coupling above the preregistered cap: changed model')
    require(tuple(parse_q(x) for x in triple) == (0, 0, 0), 'nonzero selected triple: P_R is not Haar (changed model)')
    require(model_id == 'AQ_patterned_zero_selected', 'model id relabelled: ' + model_id)
    require(j_per_tau == 28, 'interaction family changed (per-site sum ' + qs(j_per_tau) + '|tau|)')
    require(family in (F1_NAME, F2_NAME), 'unnamed construction family')
    return True


def producer_outcome(f1, f2, closeness, first_order, exact_constants, tier):
    if f1 == 'fails' or f2 == 'fails':
        return 'insufficient'
    if tier != 'ii' or not exact_constants:
        return 'limited'
    if f1 != 'verified' or f2 != 'verified' or not closeness or not first_order:
        return 'limited'
    return 'accepted_within_scope'


def certify_outcome(recorded, inputs):
    require(recorded == producer_outcome(**inputs), 'recorded outcome differs from the rule-derived outcome')
    return recorded


def admit_bound(value, target):
    require(isinstance(value, Q) and not isinstance(value, bool), 'admission requires an exact Fraction')
    require(value <= target, 'bound exceeds target')
    return True


def certify_l1_budget(value, faces, per_face):
    require(value >= faces * per_face, 'anchored/R budget is an l1 sum over faces; ' + sci(value, 6) + ' < ' + sci(faces * per_face, 6))
    return True


def certify_volume_independence(value, N):
    require(N is None, 'no division by a volume factor: the bound is uniform in N, not averaged over N')
    return True


# --------------------------------------------------------- phrasing validator
SENTENCE_NEGATIONS = ('does not assert', 'equality of the states', 'whole-sequence convergence', 'translation invariance',
                      'boundary independence of the dynamics', 'rate in N')


def certify_sentence(s):
    require(all(t in s for t in SENTENCE_NEGATIONS), 'mandatory sentence lost one of its negations')
    require('subsequential limits' in s, 'mandatory sentence must quantify over subsequential limits')
    certify_phrasing_line(s)
    return True


def certify_phrasing_line(line):
    low = line.lower()
    require('the thermodynamic limit' not in low, 'forbidden phrasing: "the thermodynamic limit"')
    if 'the aq state' in low:
        require('uniqueness of the aq state' in low and 'not' in low, 'forbidden phrasing: "the AQ state"')
    if 'uniq' in low:
        require(re.search(r'(?<![a-z])not(?![a-z])', low) is not None, 'forbidden phrasing: "unique" without "not"')
    return True


def certify_report_phrasing(text):
    for line in text.splitlines():
        certify_phrasing_line(line)
    require('a chosen subsequential' in text, 'required phrasing "a chosen subsequential" missing')
    return True


# ------------------------------------------------------ contract and premises
def am2_cap_from_gate():
    gate = json.loads((INPUTS / AM2_GATE_REL).read_text())
    m = re.search(r'\|tau\|<=1/(\d+)', gate['accepted'])
    must(m is not None and gate['verdict'] == 'accepted_within_scope', 'AM2 gate cap not found')
    return Q(1, int(m.group(1)))


def av1_target_from_gate(gate):
    m = re.search(r'meet 4/10\^7', gate['accepted'])
    must(m is not None, 'AV1 admitted target not found')
    return Q(4, 10 ** 7)


def validate_contract(data, am2_cap, av1_target):
    require(data.get('id') == 'AY1' and data.get('status') == 'frozen_before_production' and data.get('round') == 32,
            'contract identity or status')
    p = data['parameters']
    require(parse_q(p['tau_cap']) == am2_cap, 'contract tau cap differs from the admitted AM2 cap')
    certify_families(p['families'])
    require('trace norm' in p['topology'] and 'compact time windows' in p['topology'], 'contract topology text')
    pre = data['preregistration']
    require(pre['model_id'] == 'AQ_patterned_zero_selected', 'model id')
    require(all(parse_q(x) == 0 for x in pre['selected_triple_alpha_units']) and len(pre['selected_triple_alpha_units']) == 3,
            'selected triple is not zero')
    require(parse_q(pre['tau']['value']) == am2_cap and pre['tau']['signs_evaluated'] == ['+', '-'], 'tau value or signs')
    target = pre['target']
    require(target['quantity'] == 'closeness constant 2D at the cap' and target['comparator'] == '<=', 'target quantity/comparator')
    require(parse_q(target['value']) == 2 * av1_target, 'target is not twice the AV1 admitted target 4/10^7')
    gf = pre['gate_fields_required']
    require(sorted(gf) == sorted(GATE_FIELDS) and all(v is False for v in gf.values()), 'gate fields must all be false')
    certify_sentence(pre['mandatory_sentence_template'])
    require(pre['error_terms_itemized'] == ['state_boundary', 'second_order_difference', 'arithmetic'], 'error terms')
    require('uniform_local_closeness_not_uniqueness' in pre['sub_labels_allowed'], 'sub-label vocabulary')
    require(pre['observable']['reference_value_exact'] == 'P_R' and pre['observable']['reference_route'] == 'haar', 'reference')
    require('u=s/8' in pre['clock'] and 'exponent 24 forbidden' in pre['clock'], 'clock rule')
    ids = data['controls']
    require(ids == pre['controls_required']['ids'] and len(set(ids)) == len(ids) == 21, 'controls list differs from the preregistered ids')
    require(data.get('reverse_premise_isolation') is True, 'reverse premise isolation flag')
    return True


def validate_contract_bytes(raw, expected_sha, am2_cap, av1_target):
    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'contract bytes do not match the bound hash')
    data = json.loads(raw)
    validate_contract(data, am2_cap, av1_target)
    return data


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    for f in files:
        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)
        require(f not in contract.get('forward_additional_premises', []), 'forward-only premise in reverse inputs: ' + f)
    require(sorted(files) == sorted(expected) and len(files) == len(expected),
            'reverse inputs inventory differs from AGENTS.md + contract + shared_premises')
    return True


def gate_rational(text, key):
    m = re.search(re.escape(key) + r'=(\d+)/(\d+)', text)
    must(m is not None, 'gate value not found: ' + key)
    return Q(int(m.group(1)), int(m.group(2)))


def validate_gate_value(text, key, recomputed):
    m = re.search(re.escape(key) + r'=(\d+)/(\d+)', text)
    require(m is not None, 'gate value missing: ' + key)
    require(Q(int(m.group(1)), int(m.group(2))) == recomputed, 'gate value ' + key + ' differs from its exact recomputation')
    return True


TAU_CAP = None


# ==================================================================== compute
def compute():
    global TAU_CAP
    check_py_sha = sha256_file(HERE / 'check.py')            # recorded before any evaluation
    raw = (INPUTS / CONTRACT_REL).read_bytes()
    contract_sha = hashlib.sha256(raw).hexdigest()
    must(contract_sha == CONTRACT_SHA256, 'contract snapshot hash differs from the bound constant')
    am2_cap = am2_cap_from_gate()
    av1_gate = json.loads((INPUTS / AV1_GATE_REL).read_text())
    aw1_gate = json.loads((INPUTS / AW1_GATE_REL).read_text())
    ax1_gate = json.loads((INPUTS / AX1_GATE_REL).read_text())
    am2_gate = json.loads((INPUTS / AM2_GATE_REL).read_text())
    av1_target = av1_target_from_gate(av1_gate)
    contract = validate_contract_bytes(raw, CONTRACT_SHA256, am2_cap, av1_target)
    check('contract_snapshot_bound', contract_sha == CONTRACT_SHA256, contract_sha256=contract_sha,
          source='inputs/' + CONTRACT_REL, verified='before any evaluation')
    check('check_py_sha256_recorded_before_evaluation', len(check_py_sha) == 64, check_py_sha256=check_py_sha)
    cache = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if '__pycache__' in p.parts or p.suffix == '.pyc')
    check('no_interpreter_cache_in_closure', cache == [])

    params, pre = contract['parameters'], contract['preregistration']
    TAU_CAP = parse_q(params['tau_cap'])
    target = parse_q(pre['target']['value'])
    signs = pre['tau']['signs_evaluated']

    # ------------------------------------------------ AM2 constants (re-derived)
    e_lo, e_hi = exp_bounds(Q(1, 8))
    must(e_hi < Q(8, 7), 'exp(1/8)<8/7')
    R_RADIUS = Q(1, 64)
    G_R_up = 16 * Q(8, 7) * (1 + 10 * R_RADIUS)
    Gp_R_up = 16 * Q(8, 7) * (18 + 80 * R_RADIUS)
    J0 = 28 * TAU_CAP
    taylor_ok = all(16 * 8 ** k * (1 + Q(5 * k, 4)) == factorial(k) * (16 * (Q(8 ** k, factorial(k)) + (10 * Q(8 ** (k - 1), factorial(k - 1)) if k > 0 else 0)))
                    for k in range(9))
    term = four_qubit_termination()
    check('am2_constants_rederived',
          G_R_up == Q(148, 7) and Gp_R_up == 352 and J0 == Q(7, 25000000) and J0 * G_R_up < R_RADIUS
          and 2 * J0 * Gp_R_up < 1 and 2 * J0 * Gp_R_up == Q(77, 390625) and taylor_ok
          and term[8] == factorial(8) and term['ad9_zero'] is True and term[7] == 0,
          exp_one_eighth_enclosure=[qs(e_lo), qs(e_hi)], G_R_upper=qs(G_R_up), G_prime_R_upper=qs(Gp_R_up), J0=qs(J0),
          J0_G_R=qs(J0 * G_R_up), two_J0_Gp_R=qs(2 * J0 * Gp_R_up), four_qubit_termination={'ad8_coefficient': term[8], 'ad9_zero': True},
          note='G(t)=16e^{8t}(1+10t); coefficients k!*[t^k]G = 16*8^k(1+5k/4) for k<=8; termination 2|X|=8 for |X|=4')

    # ------------------------------------------------ gate bindings (AV1, AW1)
    c_cap = tier_ii(TAU_CAP)
    eps_adm = eps_admitted(c_cap)
    D_ii = density_bound(eps_adm)
    D_gate = gate_rational(av1_gate['accepted'], 'D_ii')
    t_i = J0 * G_R_up
    eps_i = 2 * t_i + t_i ** 2
    D_i = density_bound(eps_i)
    D_i_gate = gate_rational(av1_gate['accepted'], 'D_i')
    a_cap = c_cap['a']
    K2_plus = (c_cap['rho'] + 2 * c_cap['T'] ** 2 + eps_adm ** 2 + a_cap * eps_adm ** 2) / TAU_CAP ** 2
    K2_gate = gate_rational(aw1_gate['accepted'], 'K_2^+')
    check('av1_gate_D_ii_recomputed', D_ii == D_gate and av1_gate['verdict'] == 'accepted_within_scope' and D_i == D_i_gate,
          D_ii=exact(D_ii), D_i=exact(D_i), eps_admitted=exact(eps_adm), T=qs(c_cap['T']), rho=qs(c_cap['rho']),
          note='D_ii=2eps(1+eps)/(1+eps^2), eps=2T+T^2, T=(49|tau|/144)/(1-352J), read from the AV1 gate and recomputed exactly')
    check('aw1_gate_K2_plus_recomputed', K2_plus == K2_gate and aw1_gate['verdict'] == 'accepted_within_scope',
          K2_plus=exact(K2_plus), itemization='rho + T*T (straddling) + T^2 (two-creation) + (2T+T^2)^2 (density) + (|tau|/144)(2T+T^2)^2',
          note='the AW1 admitted (skeptic) itemization, recomputed exactly and equal to the gate value')

    # ------------------------------------------------ Haar and units
    moments = [haar_W_moment(n) for n in range(5)]
    amp = certify_first_order_amplitude(raw_first_order_amplitude('delta', 'delta'))
    check('haar_moments_and_units', moments == [1, 0, Q(1, 4), 0, Q(1, 8)] and amp == -Q(1, 72)
          and raw_first_order_amplitude('alpha', 'alpha') == amp and FACE_ENERGY['delta'] == 24 and FACE_ENERGY['alpha'] == 3,
          E_W_n=[qs(m) for m in moments], amplitude_per_tau=qs(amp), face_norm=qs(HALF), per_face_creation_norm='|tau|/144')

    # ------------------------------------------------ geometry and counts
    parsed = parse_i1_table((INPUTS / I1_REL).read_text())
    derived_table = derive_i1_table()
    classes = [row for row in derived_table if row[4] == 'omitted']
    must(len(classes) == 21, 'I1 omitted classes')
    t0 = faces_touching(ORIGIN, classes)
    tz = faces_touching(EZ, classes)
    meet_R = dict(t0)
    meet_R.update(tz)
    inside_R = {f: v for f, v in meet_R.items() if v[1] == COVER}
    both = {f: v for f, v in meet_R.items() if ORIGIN in v[1] and EZ in v[1]}
    straddle = {f: v for f, v in meet_R.items() if v[1] != COVER}
    only0 = {f: v for f, v in t0.items() if EZ not in v[1]}
    onlyz = {f: v for f, v in tz.items() if ORIGIN not in v[1]}
    owner_sets_0 = {v[1] for v in t0.values()}
    owner_sets_R = {v[1] for v in meet_R.values()}
    W_face = face_links(ORIGIN, 0, 2)
    W_ids = [f for f, v in inside_R.items() if v[0] == W_face]
    share_ok = True
    fl = list(meet_R.values())
    for i in range(len(fl)):
        for j in range(i + 1, len(fl)):
            if len(fl[i][0] & fl[j][0]) > 1:
                share_ok = False
    check('face_counts_R_local', parsed == derived_table and len(t0) == 49 and len(tz) == 49 and len(meet_R) == 82
          and len(inside_R) == 10 and len(both) == 16 and len(straddle) == 72 and len(only0) == 33 and len(onlyz) == 33
          and len(owner_sets_0) == 15 and len(owner_sets_R) == 27 and len(W_ids) == 1 and share_ok,
          counts={'faces_per_factor': len(t0), 'faces_meeting_R': len(meet_R), 'owner_set_exactly_R': len(inside_R),
                  'containing_both_sites': len(both), 'straddling': len(straddle), 'containing_0_not_e_z': len(only0),
                  'containing_e_z_not_0': len(onlyz), 'owner_sets_per_factor': len(owner_sets_0), 'owner_sets_meeting_R': len(owner_sets_R)},
          F_R=sorted('%s r=%d s=%d anchor=%s' % (classes[k][0], classes[k][1], classes[k][2], b) for (b, k) in inside_R),
          wilson_face='xz r=0 s=0 anchor (0,0,0)', distinct_faces_share_at_most_one_link=share_ok,
          provenance='I1 snapshot table parsed and re-derived from pi and link tails; translation covariance at every site')
    F_R = sorted(inside_R)
    W_id = W_ids[0]
    links_W = set(factor_links(ORIGIN)) | set(factor_links(EZ))
    endpoints = set()
    for (t, d) in links_W:
        endpoints.add(t)
        endpoints.add(vadd(t, DIRS[d]))
    incident = sorted({vsub(u, s) for u in COVER for s in STAR})
    certify_cover(COVER, len(links_W), len(endpoints))
    certify_incident_anchors(incident)

    # ------------------------------------------------ item 1: the two families
    boxes = {}
    for N in (2, 3):
        F1 = f1_faces(N, classes)
        F2 = f2_faces(N, classes)
        per_site_1 = {}
        per_site_2 = {}
        for fam, store in ((F1, per_site_1), (F2, per_site_2)):
            for f, (links, owners) in fam.items():
                for o in owners:
                    store[o] = store.get(o, 0) + 1
        rec = padded_record(N, classes)
        info = validate_padded_family(rec)
        partial = sum(1 for b, g in rec['groups'].items() if len(g) < 21)
        boxes[N] = {'F1_faces': len(F1), 'F2_faces': len(F2), 'F2_minus_F1': len(set(F2) - set(F1)),
                    'F1_subset_F2': set(F1) <= set(F2), 'meeting_R_in_F1': set(meet_R) <= set(F1),
                    'meeting_R_in_F2': set(meet_R) <= set(F2), 'max_faces_per_site_F1': max(per_site_1.values()),
                    'max_faces_per_site_F2': max(per_site_2.values()), 'padded_J_per_tau': qs(info['J_per_tau']),
                    'padded_termination': info['termination'], 'padded_incident_groups_R': info['incident_groups'],
                    'padded_reset_R_per_tau': qs(info['reset_R_needed_per_tau']), 'F2_partial_groups': partial,
                    'am2_volume_sites': len(rec['am2_volume']), 'B_sites': len(rec['volume_B'])}
        boxes[N]['_F1'], boxes[N]['_F2'], boxes[N]['_rec'] = F1, F2, rec
    sandwich = set(boxes[2]['_F1']) <= set(boxes[2]['_F2']) <= set(boxes[3]['_F1'])
    f1_ok = all(boxes[N]['meeting_R_in_F1'] and boxes[N]['max_faces_per_site_F1'] <= 49 for N in (2, 3))
    f2_ok = all(boxes[N]['meeting_R_in_F2'] and boxes[N]['max_faces_per_site_F2'] <= 49 and boxes[N]['F2_minus_F1'] > 0
                and Q(boxes[N]['padded_J_per_tau']) == 28 and boxes[N]['padded_termination'] == 8
                and boxes[N]['padded_incident_groups_R'] == 7 and Q(boxes[N]['padded_reset_R_per_tau']) == 98 for N in (2, 3))
    chain = {
        'I1': ('research/round21/forward/i1/report.md', 'An all-actual-support-contained block prescription' in (INPUTS / I1_REL).read_text()),
        'AM2': (AM2_GATE_REL, am2_gate['verdict'] == 'accepted_within_scope' and 'alpha/16' in am2_gate['accepted']),
        'AQ1': (AQ1_REL, '56|\\tau||F|' in (INPUTS / AQ1_REL).read_text() and 'Diagonal extraction' in (INPUTS / AQ1_REL).read_text()),
        'AV1': (AV1_GATE_REL, av1_gate['verdict'] == 'accepted_within_scope' and 'every subsequential limit of AQ1' in av1_gate['accepted']),
        'AW1': (AW1_GATE_REL, aw1_gate['verdict'] == 'accepted_within_scope' and 'every AQ1 subsequential limit' in aw1_gate['accepted']),
    }
    check('item1_F1_admitted_chain', all(v[1] for v in chain.values()) and f1_ok,
          chain=[{'step': k, 'source': v[0], 'bound': v[1]} for k, v in chain.items()],
          statement='I1 dictionary -> AM2 finite-volume ground and gap (J<=28|tau|<=J_0) -> AQ1 reset 56|tau||F|, trace-norm '
                    'compactness, diagonal extraction, Nachtergaele-Sims dynamics -> AV1 split, D_ii, cutoff-vector removal, passage '
                    'to every subsequential limit -> AW1 first-order +tau/144 and K_2^+ uniform in N and every limit')
    check('item1_F2_padded_am2_contraction', f2_ok and sandwich,
          boxes={str(N): {k: v for k, v in boxes[N].items() if not k.startswith('_')} for N in (2, 3)},
          family_sandwich_N2='faces(F1,Lambda_2) <= faces(F2,Lambda_2) <= faces(F1,Lambda_3)',
          itemized=['supports: every retained group is supported in (b+S) cap B, indexed by X_b=b+S inside B_+=B+S (|X_b|=4)',
                    'norms: ||phi_b^(B)||<=(|tau|/3)*#retained<=7|tau|',
                    'per-site sum: u in X_b iff b in u-S, so J<=4*7|tau|=28|tau|<=J_0=7/25000000 (computed max 28 on both boxes)',
                    'termination: ad^k(V_X)Omega=0 for k>2|X|=8 (four-qubit fixture: ad^8 coefficient 8!, ad^9=0)',
                    'constants: G(R)<148/7, G_prime(R)<352, J_0G(R)<R, 2J_0G_prime(R)=77/390625<1 unchanged',
                    'decoupling: no retained face touches B_+ minus B, so the padded ground is psi_B (x) Omega_pad'],
          J_per_tau_max=28, J0=qs(J0))
    check('item1_F2_reset_and_compactness', all(Q(boxes[N]['padded_reset_R_per_tau']) == 98 for N in (2, 3)),
          reset_general='Tr(rho_F h_F)<=2*7|tau|*|F-S|<=56|tau||F| for every finite F inside B',
          reset_R='<=98|tau| (seven incident groups, each changed by at most 14|tau|)',
          compactness='Tr rho_F(1-Q_{F,L})<=C_F/L and ||rho_F-Q rho_F Q||_1<=2sqrt(C_F/L) with Q_{F,L}=1_[0,L](h_F) finite rank '
                      '(compact resolvent); precompact in trace norm on every finite F; diagonal extraction over nested cubes')
    certify_topologies(STATES_TOPOLOGY, DYNAMICS_TOPOLOGY)

    # ------------------------------------------------ item 2: closeness 2D
    bures = bures_pair_bound(eps_adm)
    D_fid_up = fidelity_bound_up(eps_adm)
    D_fid_lo = fidelity_bound_lo(eps_adm)
    two_D = 2 * D_ii
    closeness_ok = (bures <= 2 * D_fid_lo and 2 * D_fid_up <= two_D and eps_adm <= 1 and admit_bound(two_D, target)
                    and certify_closeness_constant(two_D, 'AV1 admitted tier (ii) D_ii (forward exact, certified by both inequalities)', D_ii))
    fid_floor = 1 / (1 + eps_adm ** 2)
    check('item2_pairwise_closeness_2D', closeness_ok, two_D=exact(two_D), D=exact(D_ii),
          fidelity_floor=exact(fid_floor), D_fidelity_upper=exact(D_fid_up), bures_pairwise=exact(bures),
          target=qs(target), target_met=True, margin=sci(target / two_D, 8),
          F2_same_constants='F2 boxes: J<=28|tau| and at most 49 retained faces per site (enumerated), so T, rho, eps and D_ii are unchanged',
          finite_volume='||rho_{N,R}-rho_prime_{M,R}||_1<=2D for all N,M>=2 in either family, every cutoff L and the untruncated grounds',
          chain='F=<Omega_R,rho_R Omega_R>=1/(1+e^2)>=1/(1+eps^2) in every box of both families; passes to every limit '
                '(|Tr((rho-sigma)P)|<=||rho-sigma||_1); ||rho-P||_1<=2sqrt(1-F)<=2eps/sqrt(1+eps^2)<=D_ii; pairwise: '
                'Bures angle A<=arctan(eps) each, A(rho,rho_prime)<=2arctan(eps)<=pi/2, Fuchs-van de Graaf gives '
                '||rho-rho_prime||_1<=2sin(2arctan eps)=4eps/(1+eps^2)<=2D_ii')

    # ------------------------------------------------ item 3: first-order density
    pair_haar = {}
    for f in F_R:
        for g in F_R:
            pair_haar[(f, g)] = moments[2] if f == g else Q(0)      # E[W_f W_g]: share <=1 link -> 0

    def pairing(rho1, obs):
        g_id = W_id if obs == 'W' else obs
        total = Q(0)
        for (i, j), v in rho1.items():
            if i != 'O' and j == 'O':
                total += v * 2 * pair_haar[(g_id, i)]          # <e_O, W_g e_f> = 2 E[W_g W_f]
            elif i == 'O' and j != 'O':
                total += v * 2 * pair_haar[(j, g_id)]          # <e_f, W_g e_O> = 2 E[W_f W_g]
        return total

    rho1 = {}
    for f in F_R:
        rho1[(f, 'O')] = -amp * HALF      # -c^(1)_R/tau = (1/72) sum W_f Omega_R = (1/144) sum e_f, e_f = 2 W_f Omega_R
        rho1[('O', f)] = rho1[(f, 'O')]
    must(all(v == Q(1, 144) for v in rho1.values()), 'rho^(1) coefficients')
    trW = certify_first_order_density(rho1, F_R, pairing)
    all_g = all(pairing(rho1, g) == Q(1, 144) for g in F_R)
    eta_norm_sq = sum(rho1[(f, 'O')] ** 2 for f in F_R)
    tn_sq = 4 * eta_norm_sq
    s10_lo, s10_hi = sqrt_bounds(10)
    first_order_by_sign = {s: qs((1 if s == '+' else -1) * TAU_CAP * trW) for s in signs}
    check('item3_first_order_density_explicit', trW == Q(1, 144) and all_g and tn_sq == Q(10, 5184),
          rho1='rho^(1)_R = (1/72) sum_{f in F_R} (|W_f Omega_R><Omega_R| + |Omega_R><W_f Omega_R|), F_R = the 10 faces with owner set exactly R',
          basis_form='(1/144) sum_f (|e_f><e_0| + |e_0><e_f|), e_0=Omega_R, e_f=2W_f Omega_R orthonormal',
          trace_norm='sqrt(10)/72', trace_norm_squared=qs(tn_sq), trace_norm_bracket=[qs(floor_to(s10_lo / 72)), qs(ceil_to(s10_hi / 72))],
          Tr_rho1_W=qs(trW), Tr_rho1_Wg_all_F_R=all_g, first_order_W_mean_at_cap=first_order_by_sign,
          aw1_consistency='tau Tr(rho^(1) W)=+tau/144 as admitted in AW1 (both signs)')
    diag_mut = dict(rho1)
    diag_mut[('O', 'O')] = Q(1, 144)
    exc_mut = dict(rho1)
    exc_mut[(F_R[0], F_R[1])] = Q(1, 144)
    exc_mut[(F_R[1], F_R[0])] = Q(1, 144)
    check('item3_fidelity_derivative_block_structure', True,
          statement='F(tau)=1/(1+e^2) with e<=eps(tau)=O(tau) gives a zero first-order diagonal; Tr(1-P)rho(1-P)=1-F<=eps^2 with '
                    'positivity gives a zero first-order excited block; so rho^(1) is off-diagonal and equals the derivative of '
                    '(1-P_R)rho_R Omega_R = xi_hat/(1+e^2) from the vacuum-overlap vector identity rho_R Omega_R=(1_R(x)<phi_out|)psi/||psi||^2',
          rejected_mutations={'first_order_diagonal': rejected(lambda: certify_first_order_density(diag_mut, F_R, pairing), 'diag'),
                              'first_order_excited_block': rejected(lambda: certify_first_order_density(exc_mut, F_R, pairing), 'exc')},
          remainder_identity='rho-P-tau rho1 = [(F-1)P + rho_perp_perp] + [|rho_perp_0 - tau eta><Omega| + h.c.], '
                             '||first||_1=2(1-F)<=2eps^2, rho_perp_0 - tau eta = r_xi/(1+e^2) - tau eta e^2/(1+e^2)')

    led = trace_norm_ledger(TAU_CAP)
    K2p = led['K2_prime']
    led_minus = trace_norm_ledger(-TAU_CAP)
    must(led_minus['K2_prime'] == K2p, '-tau replay')
    two_K2_tau2 = 2 * K2p * TAU_CAP ** 2
    lower_first = floor_to(s10_lo / 72) * TAU_CAP - K2p * TAU_CAP ** 2
    check('item3_second_order_ledger_K2_prime', two_K2_tau2 < two_D and lower_first > two_K2_tau2,
          ledger=ledger_json(led), K2_prime=exact(K2p), two_K2_prime_tau_squared=exact(two_K2_tau2),
          ratio_2D_over_2K2tau2=sci(two_D / two_K2_tau2, 8), minus_tau='replay of the same |tau| formula',
          statement='for every box of either family at every cutoff L>=24, the untruncated ground and every subsequential limit: '
                    '||rho_R - P_R - tau rho^(1)_R||_1 <= K2_prime tau^2; hence two limits differ by at most 2 K2_prime tau^2')
    variants = {
        'orthogonal_in_R_sectors_sqrt2': trace_norm_ledger(TAU_CAP, inR='orthogonal_sectors'),
        'directed_am2_remainder_288': trace_norm_ledger(TAU_CAP, remainder='directed_288'),
        'both_refinements': trace_norm_ledger(TAU_CAP, inR='orthogonal_sectors', remainder='directed_288'),
        'admitted_eps_in_density': trace_norm_ledger(TAU_CAP, eps_mode='admitted'),
    }
    must(all(v['K2_prime'] <= K2p for k, v in variants.items() if k != 'admitted_eps_in_density'), 'refinements are smaller')
    ratio = K2p / K2_plus
    k2p_items = {t.name: t.value / TAU_CAP ** 2 for t in led['terms']}
    k2plus_items = {'am2_remainder': c_cap['rho'] / TAU_CAP ** 2, 'straddling': c_cap['T'] ** 2 / TAU_CAP ** 2,
                    'two_creation': c_cap['T'] ** 2 / TAU_CAP ** 2, 'density': eps_adm ** 2 / TAU_CAP ** 2,
                    'normalization': a_cap * eps_adm ** 2 / TAU_CAP ** 2}
    must(sum(k2plus_items.values()) == K2_plus, 'K_2^+ itemization')
    per_unit = {k: sci(k2p_items[k] / 2, 8) for k in LEDGER_ITEMS}
    check('item3_K2_prime_versus_K2_plus', ratio > 3 and ratio < 4 and K2p > K2_plus
          and k2p_items['straddling'] / 2 < k2plus_items['straddling'] + k2plus_items['two_creation']
          and (k2p_items['density'] + k2p_items['straddling'] + k2p_items['two_creation']) / 2
          < k2plus_items['density'] + k2plus_items['straddling'] + k2plus_items['two_creation'],
          K2_prime=exact(K2p), K2_plus=exact(K2_plus), ratio=exact(ratio),
          items_over_tau2={'K2_prime': {k: sci(v, 10) for k, v in k2p_items.items()},
                           'K2_plus': {k: sci(v, 10) for k, v in k2plus_items.items()},
                           'K2_prime_per_unit_trace_multiplier': per_unit},
          variants={k: {'K2_prime': exact(v['K2_prime']), 'ratio_to_K2_plus': sci(v['K2_prime'] / K2_plus, 8)} for k, v in variants.items()},
          reading='K2_prime bounds the full trace norm over B(H_R) (multiplier 2, all in-R remainder supports at both sites); '
                  'K2_plus bounds the single observable W (multiplier 2||W Omega_R||=1, only c_R). The R-local face restriction '
                  'lowers every count-dependent item per unit multiplier, but the AM2 remainder dominates both constants.')
    scal = {}
    for lab, val in (('two_D', lambda t: 2 * density_bound(eps_admitted(tier_ii(t)))),
                     ('two_K2_prime_tau2', lambda t: 2 * trace_norm_ledger(t)['total'])):
        scal[lab] = val(TAU_CAP) / val(TAU_CAP / 100)
    mono = [trace_norm_ledger(TAU_CAP / 10 ** k)['K2_prime'] for k in range(4)]
    check('item3_scaling_and_monotonicity', certify_scaling(scal['two_D'], 1) and certify_scaling(scal['two_K2_prime_tau2'], 2)
          and all(mono[i] >= mono[i + 1] for i in range(3)),
          ratio_tau_over_tau_100={k: sci(v, 10) for k, v in scal.items()},
          K2_prime_at_tau_over_10k=[sci(v, 10) for v in mono],
          note='every item is tau^2 times a nondecreasing function of |tau|, so the cap value bounds every smaller |tau|')

    # ------------------------------------------------ item 4: sentences and gate fields
    tmpl = pre['mandatory_sentence_template']
    filled = (tmpl.replace('the named construction families F1 and F2',
                           'the named construction families F1 (' + F1_NAME + ', N>=2) and F2 (' + F2_NAME + ', Lambda_N, N>=2)')
              .replace('at the same coupling', 'at the same coupling tau with |tau|<=10^-8 (either sign)')
              .replace('<= 2D', '<= 2D = ' + qs(two_D) + ' (~' + sci(two_D, 6) + ' at the cap)')
              .replace('agree to first order in tau',
                       'agree to first order in tau (common rho^(1)_R; ||rho_R - rho\'_R||_1 <= 2 K2_prime tau^2 = ' + sci(two_K2_tau2, 6) + ' at the cap)'))
    certify_sentence(filled)
    jung = ('For every pair of subsequential limits omega\', omega\'\' of the named families F1, F2 at the same coupling tau, '
            'and for every A in B(H_R) with ||A|| <= 1 on the fixed cover R: |omega\'(A) - omega\'\'(A)| <= 2D(tau) = '
            + sci(two_D, 6) + ' at |tau|=10^-8 [order tau^1], and <= 2 K2_prime tau^2 = ' + sci(two_K2_tau2, 6)
            + ' [order tau^2, after subtracting the common first-order density rho^(1)_R]. This is uniform local closeness on a fixed '
            'region at fixed coupling, inherited from a finite-volume bound that holds for every volume. It does not assert '
            'omega\' = omega\'\', convergence of any whole sequence, translation invariance, boundary independence beyond R, or '
            'any rate in N; two states satisfying it may differ by the stated order on R and without bound elsewhere.')
    certify_phrasing_line(jung)
    gate_fields = dict(pre['gate_fields_required'])
    validate_claim_flags(dict(gate_fields, continuum_claim=False, uniform_wilson_claim=False, resolved_interaction_shift=False,
                              scientific_priority_verified=False))
    check('item4_mandatory_sentences_and_gate_fields', all(v is False for v in gate_fields.values()),
          contract_template_filled=filled, jung_form_filled=jung, gate_fields=gate_fields)
    report_text = (HERE / 'report.md').read_text()
    certify_report_phrasing(report_text)
    check('report_phrasing', True, rules=['no "the thermodynamic limit"', '"the AQ state" only inside the verbatim negated exclusion',
                                          'every line containing "uniq" contains "not"', 'contains "a chosen subsequential"'],
          rejected_mutations={
              'the_AQ_state_is_unique': rejected(lambda: certify_report_phrasing(report_text + '\nThe AQ state is unique.\n'), 'aq'),
              'thermodynamic_limit': rejected(lambda: certify_report_phrasing(report_text + '\nThe states converge to the thermodynamic limit, as not shown.\n'), 'tl'),
              'unique_without_not': rejected(lambda: certify_report_phrasing(report_text + '\nThe limit is unique.\n'), 'uq'),
              'missing_chosen_subsequential': rejected(lambda: certify_report_phrasing(report_text.replace('a chosen subsequential', 'some limit')), 'cs')})

    # ------------------------------------------------ fixtures (finite audits)
    lam = Q(1, 50)
    u = -HALF
    envA = fx_env(lam, u, Q(1, 3), Q(1, 5), -Q(1, 7), HALF, -Q(2, 3), Q(1, 4), Q(3, 5), Q(1, 6))
    envB = fx_env(lam, u, -Q(1, 4), Q(2, 9), Q(1, 3), -Q(1, 3), Q(1, 5), -Q(3, 7), -HALF, Q(2, 5))
    fA, fB = fx_analyse(envA, lam, u), fx_analyse(envB, lam, u)
    items_ok = all(certify_item(fx[ 'xi_part_norm_sq'][k], fx['items'][k]) for fx in (fA, fB) for k in ('in_R', 'straddling', 'pairs'))
    diff2 = sum((fA['rho'][k] - fB['rho'][k]) ** 2 for k in fA['rho'])
    envA10 = fx_env(lam / 10, u, Q(1, 3), Q(1, 5), -Q(1, 7), HALF, -Q(2, 3), Q(1, 4), Q(3, 5), Q(1, 6))
    envB10 = fx_env(lam / 10, u, -Q(1, 4), Q(2, 9), Q(1, 3), -Q(1, 3), Q(1, 5), -Q(3, 7), -HALF, Q(2, 5))
    fA10, fB10 = fx_analyse(envA10, lam / 10, u), fx_analyse(envB10, lam / 10, u)
    diff2_10 = sum((fA10['rho'][k] - fB10['rho'][k]) ** 2 for k in fA10['rho'])
    fx_scal = diff2 / diff2_10
    check('fixture_overlap_identity_and_two_environments',
          all(fx[k] is True for fx in (fA, fB) for k in ('split_ok', 'identity_ok', 'fidelity_ok', 'offdiag_ok', 'delta_expansion_ok'))
          and items_ok and all(fx['xi_part_norm_sq']['straddling'] > 0 for fx in (fA, fB))
          and all(4 * fx['tr_X2'] <= fx['bound'] ** 2 for fx in (fA, fB)) and diff2 > 0
          and 4 * diff2 <= (fA['bound'] + fB['bound']) ** 2 and (fA['first_order_trace_norm']) ** 2 > (fA['bound'] + fB['bound']) ** 2
          and Q(5000) <= fx_scal <= Q(20000),
          model_is_finite_graph=True, transfers_to_aq=False,
          fixture='four qubit sites (0, e_z | o1, o2); first-order creations on two or three sites, second-order single-site; '
                  'two environments A and B share only the first-order in-R creation lam*u (u=-1/2, lam=1/50)',
          verified=['(<Omega_R|(x)1)psi = prod_{I cap R empty}(1-c_I)Omega_out', 'rho_R Omega_R = (1_R(x)<phi_out|)psi/||psi||^2',
                    'F=1/(1+e^2)', '(1-P_R)rho_R Omega_R = xi_hat/(1+e^2) exactly', 'delta = in-R + straddling + pair terms exactly', 'each xi component within its ledger item',
                    'straddling component nonzero (item required)', '||rho-P-lam rho1||_1 <= 2||.||_2 <= ledger bound (both envs)',
                    'rho_A != rho_B but 2||rho_A-rho_B||_2 <= bound_A+bound_B < ||lam rho1||_1', 'difference scales as lam^2 (Tr diff^2 ratio ~10^4)'],
          straddling_component_norm_sq={'A': qs(fA['xi_part_norm_sq']['straddling']), 'B': qs(fB['xi_part_norm_sq']['straddling'])},
          diff_squared_ratio_lam_over_lam10=sci(fx_scal, 8),
          rejected_mutations={'straddling_item_dropped': rejected(lambda: certify_item(fA['xi_part_norm_sq']['straddling'], Q(0)), 'strad')})

    # ------------------------------------------------ controls
    control('missing_incoming_stars', [
        ('orthant_anchors_0_e_z_only', lambda: certify_incident_anchors([ORIGIN, EZ])),
        ('one_star_J_7', lambda: certify_J_per_tau(7, 1, 7)),
        ('reset_two_anchors_28', lambda: certify_reset_R(28, 2, 7)),
        ('F2_reset_outgoing_groups_only', lambda: validate_padded_family(dict(boxes[2]['_rec'], reset_R_claim=Q(28)))),
    ], incident_anchors=[list(a) for a in incident], J_per_tau=28, reset_R_per_tau=98)
    control('full_original_wilson_cover', [
        ('four_drawn_links', lambda: certify_cover(COVER, 4, 6)),
        ('cover_origin_only', lambda: certify_cover((ORIGIN,), 24, 22)),
        ('cover_with_extra_factor', lambda: certify_cover((ORIGIN, EZ, (1, 0, 0)), 72, 50)),
    ], cover=[list(x) for x in COVER], links=len(links_W), endpoints=len(endpoints))
    clock_text = pre['clock']
    control('wrong_delta_alpha_hbar_clock', [
        ('mixed_units_delta_coupling_alpha_energy', lambda: certify_first_order_amplitude(raw_first_order_amplitude('delta', 'alpha'))),
        ('mixed_units_alpha_coupling_delta_energy', lambda: certify_first_order_amplitude(raw_first_order_amplitude('alpha', 'delta'))),
        ('exponent_24_on_alpha_clock', lambda: certify_clock('s=alpha*t_E/hbar', Q(24))),
        ('u_equals_s_over_8_clock', lambda: certify_clock('u=s/8', Q(3))),
    ], clock_read_from_contract=clock_text, amplitude=qs(amp), W_Omega_energy={'alpha': 3, 'delta': 24})
    m_c, d_c = Q(1, 4), Q(1, 100)
    must(certify_centering('vector', d_c * d_c, m_c, d_c), 'vector centering')
    scalar_as_density = {(f, 'O'): Q(0) for f in F_R}
    scalar_as_density.update({('O', 'O'): Q(1, 144)})
    control('vector_versus_scalar_centering', [
        ('scalar_subtraction_as_vector_centering', lambda: certify_centering('scalar', -2 * m_c * d_c - d_c * d_c, m_c, d_c)),
        ('uncentered_residue_as_centered', lambda: certify_centering('uncentered', m_c * m_c, m_c, d_c)),
        ('scalar_first_order_shift_as_density', lambda: certify_first_order_density(scalar_as_density, F_R, pairing)),
        ('scalar_W_constant_as_trace_norm_constant', lambda: certify_trace_norm_constant(K2_plus, 'AW1 Wilson-mean K_2^+')),
    ], residues={'vector': qs(d_c * d_c), 'scalar': qs(-2 * m_c * d_c - d_c * d_c), 'uncentered': qs(m_c * m_c)},
        note='rho^(1)_R is a vector-level (off-diagonal) object; a scalar mean shift or a single-observable constant is not it')
    zero_density = {(f, 'O'): Q(0) for f in F_R}
    zero_density.update({('O', f): Q(0) for f in F_R})
    must(certify_state_budget(D_ii, lower_first), 'D_ii charges the first-order density')
    control('first_order_mean_charged', [
        ('zero_first_order_density', lambda: certify_first_order_density(zero_density, F_R, pairing)),
        ('state_budget_second_order_only', lambda: certify_state_budget(K2p * TAU_CAP ** 2, lower_first)),
        ('state_budget_two_K2_prime', lambda: certify_state_budget(two_K2_tau2, lower_first)),
    ], first_order_trace_norm='sqrt(10)|tau|/72', proved_first_order_lower=exact(lower_first),
        note='||tau rho^(1)||_1=sqrt(10)|tau|/72 exceeds the second-order budget; D_ii (linear) charges it')
    at4 = lambda t: 2 * sqrt_bounds(49 * abs(t) / 3)[1]
    at4_ratio = at4(TAU_CAP) / at4(TAU_CAP / 100)
    control('tau_scaling_exponent', [
        ('second_order_difference_labelled_first_order', lambda: certify_scaling(scal['two_K2_prime_tau2'], 1)),
        ('two_D_labelled_second_order', lambda: certify_scaling(scal['two_D'], 2)),
        ('at4_square_root_labelled_linear', lambda: certify_scaling(at4_ratio, 1)),
    ], ratios={k: sci(v, 10) for k, v in scal.items()}, at4_ratio=sci(at4_ratio, 8))
    control('changed_model_relabelled', [
        ('nonzero_selected_triple', lambda: certify_model(TAU_CAP, ('0', '1/100', '0'), 'AQ_patterned_zero_selected', 28, F1_NAME)),
        ('coupling_above_cap', lambda: certify_model(TAU_CAP * 10, ('0', '0', '0'), 'AQ_patterned_zero_selected', 28, F1_NAME)),
        ('uniform_route_B_J_29', lambda: certify_model(TAU_CAP, ('0', '0', '0'), 'AQ_patterned_zero_selected', 29, F1_NAME)),
        ('finite_graph_model_id', lambda: certify_model(TAU_CAP, ('0', '0', '0'), 'FG(four_qubit_fixture)', 28, F1_NAME)),
        ('unnamed_boundary_family', lambda: certify_model(TAU_CAP, ('0', '0', '0'), 'AQ_patterned_zero_selected', 28, 'periodic boxes')),
    ], note='beyond the cap or at a nonzero triple the certificate is silent; that is not a failure of the model')
    base = json.loads(raw)

    def coherent(mut):
        doc = json.loads(json.dumps(base))
        mut(doc)
        blob = json.dumps(doc, indent=2).encode()
        return blob, hashlib.sha256(blob).hexdigest()

    tampers = {
        'target_relaxed_1e-3': coherent(lambda d: d['preregistration']['target'].__setitem__('value', '1/1000')),
        'tau_cap_1e-7': coherent(lambda d: d['parameters'].__setitem__('tau_cap', '1/10000000')),
        'gate_field_uniqueness_true': coherent(lambda d: d['preregistration']['gate_fields_required'].__setitem__('uniqueness_claimed', True)),
        'family_removed': coherent(lambda d: d['parameters']['families'].pop()),
        'template_negation_removed': coherent(lambda d: d['preregistration'].__setitem__(
            'mandatory_sentence_template', d['preregistration']['mandatory_sentence_template'].replace('does not assert', 'asserts'))),
        'control_removed': coherent(lambda d: d['controls'].pop()),
        'isolation_flag_false': coherent(lambda d: d.__setitem__('reverse_premise_isolation', False)),
    }
    D_tamper = av1_gate['accepted'].replace('D_ii=585079838465912592144137406066050', 'D_ii=585079838465912592144137406066049')
    K_tamper = aw1_gate['accepted'].replace('K_2^+=81108864767825329926713064490531229475390625', 'K_2^+=40554432383912664963356532245265614737695312')
    must(validate_gate_value(av1_gate['accepted'], 'D_ii', D_ii) and validate_gate_value(aw1_gate['accepted'], 'K_2^+', K2_plus), 'gate values')
    control('coherent_evidence_tampering',
            [(label, (lambda b=blob, h=digest: validate_contract_bytes(b, h, am2_cap, av1_target))) for label, (blob, digest) in sorted(tampers.items())]
            + [('byte_change_without_rehash', lambda: validate_contract_bytes(raw + b' ', CONTRACT_SHA256, am2_cap, av1_target)),
               ('av1_gate_D_ii_edited', lambda: validate_gate_value(D_tamper, 'D_ii', D_ii)),
               ('aw1_gate_K2_plus_halved', lambda: validate_gate_value(K_tamper, 'K_2^+', K2_plus))],
            note='each tampered contract copy is rehashed coherently; semantic validation still rejects it')
    good = dict(f1='verified', f2='verified', closeness=True, first_order=True, exact_constants=True, tier='ii')
    outcome = certify_outcome(producer_outcome(**good), good)
    only_f1 = dict(good, f2='unverified')
    no_density = dict(good, first_order=False)
    f2_fails = dict(good, f2='fails')
    tier_i = dict(good, tier='i')
    must(producer_outcome(**only_f1) == 'limited' and producer_outcome(**no_density) == 'limited'
         and producer_outcome(**f2_fails) == 'insufficient' and producer_outcome(**tier_i) == 'limited', 'outcome rule')
    two_D_i = 2 * D_i
    must(two_D_i > target, 'tier (i) closeness fails the target and is retained')
    control('insufficient_verdict_retained', [
        ('one_family_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', only_f1)),
        ('no_first_order_density_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', no_density)),
        ('failing_family_relabelled_limited', lambda: certify_outcome('limited', f2_fails)),
        ('tier_i_only_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', tier_i)),
        ('tier_i_closeness_admitted', lambda: admit_bound(two_D_i, target)),
    ], retained={'tier_i_two_D_i': exact(two_D_i), 'tier_i_meets_target': False, 'one_family': 'limited',
                 'no_first_order_density': 'limited', 'family_fails_premises': 'insufficient'})
    control('exact_arithmetic_admission', [
        ('float_tau', lambda: tier_ii(1e-08)),
        ('bool_tau', lambda: tier_ii(True)),
        ('nan_string', lambda: parse_q('NaN')),
        ('zero_denominator', lambda: parse_q('1/0')),
        ('float_bound_admission', lambda: admit_bound(float(two_D), target)),
    ], note='every Boolean is decided on Fraction values; decimal strings are truncated previews')
    items_list = [t.value for t in led['terms']]
    rss = sqrt_bounds(sum(v * v for v in items_list))[1]
    control('root_n_misuse', [
        ('sqrt72_for_straddling_budget', lambda: certify_l1_budget(sqrt_bounds(72)[1] * a_cap, 72, a_cap)),
        ('sqrt82_for_R_first_order_sum', lambda: certify_l1_budget(sqrt_bounds(82)[1] * a_cap, 82, a_cap)),
        ('root_sum_square_ledger', lambda: assemble_ledger(led['terms'], combine='rss')),
        ('division_by_sqrt_volume', lambda: certify_volume_independence(two_D, 125)),
    ], rss_would_give=sci(rss, 8), linear_sum=sci(led['total'], 8),
        legitimate_root='sqrt(10)/72 is the exact Hilbert norm of ten orthogonal face vectors inside one owner set, not a budget')
    flags = dict(gate_fields, continuum_claim=False, uniform_wilson_claim=False, resolved_interaction_shift=False,
                 scientific_priority_verified=False)
    must(validate_claim_flags(flags), 'claim flags')
    control('no_priority_or_continuum_claim', [
        ('continuum_true', lambda: validate_claim_flags(dict(flags, continuum_claim=True))),
        ('priority_true', lambda: validate_claim_flags(dict(flags, scientific_priority_verified=True))),
        ('uniform_wilson_true', lambda: validate_claim_flags(dict(flags, uniform_wilson_claim=True))),
        ('uniqueness_true', lambda: validate_claim_flags(dict(flags, uniqueness_claimed=True))),
    ], flags=flags)
    Dm = D_ii
    mass = 1 - Dm / 2
    control('topology_named', [
        ('weak_star_for_states', lambda: certify_topologies('weak-* on finite-rank observables', DYNAMICS_TOPOLOGY)),
        ('one_topology_for_both', lambda: certify_topologies(STATES_TOPOLOGY, STATES_TOPOLOGY)),
        ('norm_continuity_on_all_of_B', lambda: certify_topologies(STATES_TOPOLOGY, 'norm continuity in time on all of B(H_F)')),
        ('weak_star_mass_escape_limit_as_state', lambda: certify_limit_is_state(mass)),
    ], states=STATES_TOPOLOGY, dynamics=DYNAMICS_TOPOLOGY,
        mass_escape_example='rho_n=(1-D/2)|e_0><e_0|+(D/2)|e_n><e_n|: weak-* limit mass 1-D/2, pairwise trace distance D; the reset energy supplies tightness')
    F2N2, F1N2 = set(boxes[2]['_F2']), set(boxes[2]['_F1'])
    must(certify_family_is_F2(F2N2, F2N2, F1N2), 'F2 identity')
    control('two_families_named', [
        ('single_family', lambda: certify_families([F1_NAME])),
        ('all_boundary_conditions', lambda: certify_families([F1_NAME, 'all boundary conditions'])),
        ('F2_without_padding_whole_star_rule', lambda: certify_family_is_F2(F1N2, F2N2, F1N2)),
    ], families=[F1_NAME, F2_NAME], F2_minus_F1_faces_N2=boxes[2]['F2_minus_F1'])
    lam_m = Q(1, 10 ** 4)
    fidelity_m = 1 / (1 + lam_m ** 2)
    dist_sq_P = 4 * (1 - fidelity_m)
    pair_sq = 4 * (1 - fidelity_m ** 2)
    D_m_sq = 4 * lam_m ** 2 / (1 + lam_m ** 2)
    bures_m = bures_pair_bound(lam_m)
    moving_ok = dist_sq_P == D_m_sq and 0 < pair_sq <= 4 * D_m_sq and pair_sq <= bures_m ** 2
    must(moving_ok, 'moving-vector example')
    limits_seq = ('rho_0', 'rho_1')
    control('subsequence_versus_whole_sequence', [
        ('whole_sequence_claimed_from_uniform_closeness', lambda: certify_sequence_claim('whole_sequence_converges', limits_seq)),
        ('unquantified_limit', lambda: certify_sequence_claim('the limit', limits_seq)),
    ], fixed_vector_versus_moving_vector={
        'fixed_vector': 'P=|Omega><Omega|', 'moving_vectors': 'w_N=Omega+lam e_{1+(N mod 2)}, lam=1/10000',
        'distance_to_fixed_squared': qs(dist_sq_P), 'D_squared': qs(D_m_sq), 'pair_distance_squared': qs(pair_sq),
        'bures_pair_bound': qs(bures_m), 'reading': 'every element is within D of the fixed vector and pairwise within 2D, yet the '
                                                     'moving sequence has two distinct subsequential limits'},
        quantifier='every subsequential limit; a chosen subsequential limit is one member of that set')
    mid = TAU_CAP / 144
    xp, xm = mid + K2_plus * TAU_CAP ** 2 / 2, mid - K2_plus * TAU_CAP ** 2 / 2
    lo_i, hi_i = mid - K2_plus * TAU_CAP ** 2, mid + K2_plus * TAU_CAP ** 2
    must(lo_i <= xm < xp <= hi_i, 'common interval example')
    bad_sentence = filled.replace('this does not assert', 'this asserts')
    control('local_closeness_not_uniqueness', [
        ('equality_from_closeness', lambda: certify_equality_claim('rho_0', 'rho_1', 'trace distance <= 2D')),
        ('equality_from_common_enclosing_interval', lambda: certify_equality_claim(xp, xm, 'common enclosing interval')),
        ('sentence_without_negation', lambda: certify_sentence(bad_sentence)),
    ], common_interval={'interval': [qs(lo_i), qs(hi_i)], 'two_members': [qs(xp), qs(xm)], 'equal': False},
        note='two states within 2D (or two numbers in one enclosure) need not coincide')
    sep_lower = 2 * floor_to(s10_lo / 72) * TAU_CAP - two_K2_tau2
    must(sep_lower > two_K2_tau2, 'the +tau/-tau first-order separation exceeds the second-order budget')
    control('common_clock', [
        ('second_order_closeness_across_plus_minus_tau', lambda: certify_comparison(TAU_CAP, -TAU_CAP, 's=alpha*t_E/hbar', 's=alpha*t_E/hbar', 2)),
        ('alpha_clock_versus_delta_clock', lambda: certify_comparison(TAU_CAP, TAU_CAP, 's=alpha*t_E/hbar', 'u=delta*t_E/hbar', 1)),
        ('u_equals_s_over_8_packet', lambda: certify_comparison(TAU_CAP, TAU_CAP, 'u=s/8', 'u=s/8', 1)),
    ], clock='s=alpha*t_E/hbar (theta=alpha*t/hbar); the closeness statement is static, the clock is common by construction',
        plus_minus_tau_first_order_separation_lower=exact(sep_lower),
        remark='at opposite couplings the first-order densities are opposite, so a second-order closeness claim across +-tau is false')
    m_rev = re.search(r'D_ii<=(\d+)/10\^40', av1_gate['accepted'])
    must(m_rev is not None, 'AV1 reverse labelled refinement not found in the gate')
    D_rev_refine = Q(int(m_rev.group(1)), 10 ** 40)
    must(D_rev_refine < D_ii, 'the labelled refinement is smaller than the admitted D_ii')
    control('tier_mixing_rejected', [
        ('D_ii_plus_D_i', lambda: certify_closeness_constant(D_ii + D_i, 'AV1 admitted tier (ii) D_ii (forward exact, certified by both inequalities)', D_ii)),
        ('reverse_82_face_refinement_as_admitted', lambda: certify_closeness_constant(D_ii + D_rev_refine, 'AV1 reverse labelled refinement', D_ii)),
        ('crude_t_in_straddling_item', lambda: trace_norm_ledger(TAU_CAP, tier_override='i', crude_t=t_i)),
        ('t1_without_self_consistency', lambda: certify_closeness_constant(4 * c_cap['t1'], 'AV1 admitted tier (ii) D_ii (forward exact, certified by both inequalities)', D_ii)),
    ], admitted=exact(two_D), note='one tier throughout: 2D=2D_ii; K2_prime items all tier (ii)')
    inventory = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    must(validate_inventory(inventory, contract), 'reverse inputs inventory')
    control('reverse_premise_isolation', [
        ('skeptic_triage_added', lambda: validate_inventory(inventory + ['research/round32/skeptic/triage.md'], contract)),
        ('jung_loop2_added', lambda: validate_inventory(inventory + ['research/round32/experts/jung/loop2-response.md'], contract)),
        ('forward_ay1_added', lambda: validate_inventory(inventory + ['research/round32/forward/ay1/report.md'], contract)),
        ('deliberation_added', lambda: validate_inventory(inventory + ['research/round32/advisor/deliberation-7.md'], contract)),
        ('premise_missing', lambda: validate_inventory(inventory[1:], contract)),
    ], inventory_size=len(inventory))
    rec2 = boxes[2]['_rec']
    straddling_face = None
    for b in sorted(rec2['volume_B']):
        for k, cls in enumerate(classes):
            links, owners = class_face(b, cls)
            if any(o not in rec2['volume_B'] for o in owners):
                straddling_face = ((b, k), owners, b)
                break
        if straddling_face is not None:
            break
    must(straddling_face is not None, 'a boundary face with support outside B exists')
    g_straddle = {b: dict(v) for b, v in rec2['groups'].items()}
    g_straddle.setdefault(straddling_face[2], {})[straddling_face[0]] = straddling_face[1]
    g_double = {b: dict(v) for b, v in rec2['groups'].items()}
    some_b = sorted(g_double)[0]
    some_f = sorted(g_double[some_b])[0]
    other_b = sorted(g_double)[1]
    g_double[other_b][some_f] = g_double[some_b][some_f]
    pad_site = sorted(rec2['am2_volume'] - rec2['volume_B'])[0]
    control('padding_family_contraction_proved', [
        ('no_padding_am2_volume_equals_B', lambda: validate_padded_family(dict(rec2, am2_volume=set(rec2['volume_B'])))),
        ('straddling_face_retained', lambda: validate_padded_family(dict(rec2, groups=g_straddle))),
        ('face_double_counted', lambda: validate_padded_family(dict(rec2, groups=g_double))),
        ('padded_site_interacting', lambda: validate_padded_family(dict(rec2, interacting_padded_sites=[pad_site]))),
        ('termination_order_six_imported', lambda: validate_padded_family(dict(rec2, termination_order_claim=6))),
    ], positive={str(N): {'J_per_tau': boxes[N]['padded_J_per_tau'], 'termination': boxes[N]['padded_termination'],
                          'reset_R_per_tau': boxes[N]['padded_reset_R_per_tau'], 'partial_groups': boxes[N]['F2_partial_groups']}
                 for N in (2, 3)}, J0=qs(J0), J0_G_R=qs(J0 * G_R_up), two_J0_Gp_R=qs(2 * J0 * Gp_R_up))
    ax1_dict = re.search(r'tau=96/g\^4, so g\^4=9\.6x10\^9 at the cap', ax1_gate['accepted']) is not None
    must(ax1_dict and certify_uniformity('box size N'), 'uniformity parameter')
    control('not_uniform_in_a', [
        ('uniform_in_lattice_spacing', lambda: certify_uniformity('lattice spacing a')),
        ('uniform_in_a', lambda: certify_uniformity('a')),
        ('weak_coupling_g_to_0', lambda: certify_uniformity('bare coupling g -> 0')),
        ('N_to_infinity_called_continuum', lambda: certify_uniformity('continuum limit N -> infinity')),
    ], uniform_over=['box size N', 'on-site cutoff L', 'construction family', 'subsequence'],
        fixed=['lattice spacing a', 'alpha', 'hbar', 'E_star', 'tau'],
        illustration='AX1 gate (uniform model, different family): the cap corresponds to g^4=9.6x10^9, strong bare coupling; '
                     'nothing is uniform in a or valid at weak coupling')

    ids = [c['id'] for c in CHECKS]
    missing = [c for c in contract['controls'] if c not in ids]
    must(missing == [], 'contract controls without a check: ' + ','.join(missing))
    must(sorted(MUTATION_CONTROLS) == sorted(contract['controls']), 'every contract control carries damaging mutations')

    headline = {
        'D': dict(exact(D_ii), source='AV1 gate tier (ii), recomputed exactly (eps=2T+T^2)'),
        'two_D': dict(exact(two_D), target=qs(target), target_comparator='<=', target_met=True, margin=sci(target / two_D, 8)),
        'bures_pairwise_bound': exact(bures),
        'K2_prime': dict(exact(K2p), meaning='trace-norm second-order remainder on B(H_R), R-local counts 82/72/33/10'),
        'K2_plus': dict(exact(K2_plus), meaning='AW1 admitted Wilson-mean second-order constant (single observable W)'),
        'K2_prime_over_K2_plus': exact(ratio),
        'two_K2_prime_tau_squared_at_cap': exact(two_K2_tau2),
        'first_order_density': 'rho^(1)_R=(1/72) sum_{f in F_R}(|W_f Omega_R><Omega_R|+|Omega_R><W_f Omega_R|), ||rho^(1)_R||_1=sqrt(10)/72',
    }
    result = {
        'loop': 'AY1', 'direction': 'reverse', 'route': 'vacuum overlap / fidelity (Bures angle) and derivative of the vacuum-overlap vector identity',
        'human_author': contract['human_author'],
        'ai_assistance': 'AI-assisted reverse production (Claude, an AI model); correlated model-agent work, not human review',
        'contribution_alias': 'HNM-AY1-R reverse fidelity closeness and overlap-derivative first-order density',
        'attribution': {
            'fidelity_inequalities': 'standard: pure-state trace distance, Uhlmann fidelity, Bures angle metric, Fuchs-van de Graaf',
            'creation_expansion': 'admitted AM2 construction (Bravyi-DiVincenzo-Loss lineage; Gauvin arXiv:2503.15539v3 A.6-A.8 as template)',
            'padding': 'I1 section 6 prescription; the itemized AM2 re-application is this producer\'s',
            'scientific_priority': 'unverified'},
        'contract_sha256': contract_sha,
        'check_py_sha256_recorded_before_evaluation': check_py_sha,
        'model': contract['model'],
        'model_label': 'AQ_patterned_zero_selected; zero selected triple, Haar reference; whole stars phi_b=-(tau/3) sum W_f; '
                       '|tau|<=10^-8 both signs; families F1 and F2 (N>=2); cover R={0,e_z} (48 links, 36 endpoints, 7 incident anchors); '
                       'fixed spacing and fixed positive alpha, hbar, E_star; common clock s=alpha*t_E/hbar',
        'families': {'F1': F1_NAME, 'F2': F2_NAME},
        'states_compared': 'all subsequential limits of F1 and F2',
        'region': 'R fixed before production',
        'topology': STATES_TOPOLOGY,
        'topologies': {'states': STATES_TOPOLOGY, 'dynamics': DYNAMICS_TOPOLOGY},
        'closeness_order': [1, 2],
        'label': 'uniform_local_closeness_not_uniqueness',
        'headline': headline,
        'target': {'quantity': pre['target']['quantity'], 'value': qs(target), 'comparator': '<=', 'read_from': 'contract preregistration.target'},
        'error_ledger': {
            'state_boundary': {'value': qs(two_D), 'preview': sci(two_D), 'meaning': 'pairwise closeness of any two subsequential limits of F1/F2 '
                               'at the same tau from the finite-volume AV1 bound (order tau)'},
            'second_order_difference': {'value': qs(two_K2_tau2), 'preview': sci(two_K2_tau2),
                                        'meaning': 'after the common first-order density, 2 K2_prime tau^2 (order tau^2)'},
            'arithmetic': {'value': '0', 'reason': 'headline constants are exact rationals; directed 10^-40 roundings enter only the '
                                                  'fidelity cross-check, the sqrt(2) variant and brackets; decimals are truncated previews'}},
        'mandatory_sentence_contract_template': filled,
        'mandatory_sentence_jung_form': jung,
        'quantitative_boundary_comparison_definition': 'a closeness bound (2D, and 2K2_prime tau^2) plus a matching first-order term '
                                                       '(the common rho^(1)_R); explicitly not a variational statement about which boundary '
                                                       'condition the infinite-volume theory selects',
        'contract_controls_covered': list(contract['controls']),
        'controls_with_damaging_mutations': sorted(MUTATION_CONTROLS),
        'controls_not_implementable_as_mutations': [],
        'item5_freeze_and_replays': 'executed by research/round32/tools/freeze.py (normal and -O replays into fresh external '
                                    'directories, byte-identical to output/), recorded in freeze.json',
        'routes_executed': [
            'item 1: F1 admitted chain cited step by step; F2 AM2 contraction, reset and compactness itemized and enumerated (N=2,3)',
            'item 2: fidelity identity passed to limits; trace-norm triangle via P_R (2D) and Bures-angle route 4eps/(1+eps^2)',
            'item 3: derivative of the fidelity identity (diagonal, excited block) and of the vacuum-overlap vector identity '
            '(off-diagonal) giving rho^(1)_R; R-local trace-norm ledger K2_prime; comparison with K_2^+',
            'item 4: contract template and Jung-form sentence filled; gate fields exported',
            'items 5-6: 21 contract controls as damaging mutations; fixtures (finite audits)'],
        'exclusions': {'contract': contract['claim_exclusions'], 'preregistration': pre['claim_exclusions']},
        'sub_label': 'uniform_local_closeness_not_uniqueness',
        'proposed_reverse_verdict': outcome,
        'outcome_note': 'proposed for the reverse half only; the acceptance rule needs both routes and skeptical review',
        'tier_i_retained': {'two_D_i': exact(two_D_i), 'meets_target': False},
        'checks': CHECKS,
    }
    result.update(flags)
    return result


def main():
    ap = argparse.ArgumentParser(description='HNM-AY1 reverse producer checker (exact arithmetic)')
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
    manifest = {'loop': 'AY1', 'direction': 'reverse', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AY1', 'direction': 'reverse', 'checks': len(result['checks']),
                      'two_D': result['headline']['two_D']['preview'], 'K2_prime': result['headline']['K2_prime']['preview'],
                      'K2_plus': result['headline']['K2_plus']['preview'], 'outcome': result['proposed_reverse_verdict']},
                     sort_keys=True))


if __name__ == '__main__':
    main()
