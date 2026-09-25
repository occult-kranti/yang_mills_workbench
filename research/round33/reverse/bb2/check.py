#!/usr/bin/env python3
"""HNM-BB2 reverse producer: whole-sequence convergence of the named constructions F1
(AQ1 centered whole-star boxes) and F2 (I1 section 6 all-contained-face boxes with
padding), their common limit, its identification with every AQ1 and F2 subsequential
limit, coarse translation invariance and the correlation functions on |theta|<=8, by the
reverse assembly union_comparison (any two volumes are compared through their union or
through the BB1 direct general-volume comparison hypothesis).

Every BB2 conclusion that uses BB1 is conditional_on_bb1_targets: the BB1 frozen targets
(C_h=1/250000, c_h=1/500000 at q=1/64; secondary C_2h=1/20000, c_2h=1/40000 at
q_2=151552|tau|) are explicit hypotheses. This producer reads no BB1 producer, skeptic or
gate file; the discharge is recorded at the BB2 gate, not here.

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production (Claude, an AI
model) under reverse premise isolation; HNM labels are project aliases. The limit dynamics
is Nachtergaele-Sims arXiv:1410.8174v1 Theorem 4.1 (through the admitted BA2 gate); the
GNS/stationarity/Fourier strategy of AQ1-AQ2 is credited to Gauvin arXiv:2503.15539v3
Supplement A.10 as in AQ1/AQ2. Scientific priority is unverified.

Standard library only. Exact Fraction arithmetic decides every Boolean; decimal strings
are truncated previews computed with integers. Every contract control is a damaging-
mutation control whose rejection is required. Failures raise explicit exceptions (never
assert), so the output bytes are identical under python -O.

Usage: python3 -B research/round33/reverse/bb2/check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUTS = HERE / 'inputs'
REPORT = HERE / 'report.md'
CONTRACT_REL = 'research/round33/contracts/bb2.json'
CONTRACT_SHA256 = 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35'
BB1_CONTRACT_REL = 'research/round33/contracts/bb1.json'
BB1_CONTRACT_SHA256 = '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018'
NS_REL = 'research/round33/sources/nachtergaele-sims-1410.8174v1.md'
NS_PDF_SHA256 = '501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba'
BA1_GATE_REL = 'research/round33/advisor/ba1-gate.json'
BA2_GATE_REL = 'research/round33/advisor/ba2-gate.json'
AQ1_GATE_REL = 'research/round29/advisor/aq1-gate.json'
AQ2_GATE_REL = 'research/round29/advisor/aq2-gate.json'
AV1_GATE_REL = 'research/round32/advisor/av1-gate.json'
AY1_GATE_REL = 'research/round32/advisor/ay1-gate.json'
AY2_GATE_REL = 'research/round32/advisor/ay2-gate.json'
AM2_GATE_REL = 'research/round29/advisor/am2-gate.json'
AW1_GATE_REL = 'research/round32/advisor/aw1-gate.json'
I1_REL = 'research/round21/forward/i1/report.md'
BA2F_REL = 'research/round33/forward/ba2/report.md'
BA2R_REL = 'research/round33/reverse/ba2/report.md'
AV1F_REL = 'research/round32/forward/av1/report.md'
AQ2F_REL = 'research/round29/forward/aq2/report.md'
PINNED_SHA256 = {
    BA1_GATE_REL: '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    BA2_GATE_REL: 'e6b163fc8f80de28c51609f77d0bef21dcdc1286638c862ad67202e6f7b0ca35',
    AQ1_GATE_REL: 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    AQ2_GATE_REL: '930b697db343ffd261c303c34e6ddd8c6e9c753ee6707931c55dc4171ee47575',
    AV1_GATE_REL: '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    AY1_GATE_REL: 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    AY2_GATE_REL: 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    AM2_GATE_REL: 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    AW1_GATE_REL: '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    NS_REL: '6a28f4cd6aa2c55286fa839d83c00356ff0709f8b02027ee5b39050df1d6c921',
}
# The shared premises the frozen contract declares (pinned so that a coherent removal of a
# snapshot together with its contract line is still rejected).
REQUIRED_PREMISES = (
    'research/round29/forward/am2/report.md', 'research/round29/reverse/am2/report.md',
    'research/round29/skeptic/am2.md', 'research/round29/advisor/am2-gate.json',
    'research/round29/forward/aq1/report.md', 'research/round29/advisor/aq1-gate.json',
    'research/round29/forward/aq2/report.md', 'research/round21/forward/i1/report.md',
    'research/round32/advisor/av1-gate.json', 'research/round32/forward/av1/report.md',
    'research/round32/reverse/av1/report.md', 'research/round32/advisor/ay1-gate.json',
    'research/round32/forward/ay1/report.md', 'research/round32/reverse/ay1/report.md',
    'research/round32/advisor/ay2-gate.json', 'research/round32/forward/ay2/report.md',
    'research/round33/methods/paired-physics-research/SKILL.md',
    'research/round33/methods/paired-physics-research/references/complete-residual-and-error-scope.md',
    'research/round33/methods/newton-analysis-synthesis/SKILL.md',
    'research/round33/methods/tesla-mechanism-resonance/SKILL.md',
    'research/round33/methods/historical-physics-panel/SKILL.md',
    'research/round33/methods/qeg-research-advisor/references/round32-state-lemma-and-window.md',
    'research/round32/advisor/aw1-gate.json', 'research/round32/forward/aw1/report.md',
    'research/round33/advisor/ba1-gate.json', 'research/round33/forward/ba1/report.md',
    'research/round33/reverse/ba1/report.md', 'research/round33/skeptic/ba1.md',
    'research/round33/advisor/ba2-gate.json', 'research/round33/forward/ba2/report.md',
    'research/round33/reverse/ba2/report.md', 'research/round33/skeptic/ba2.md',
    'research/round33/contracts/bb1.json', NS_REL,
    'research/round33/advisor/selection-bb2.md', 'research/round29/advisor/aq2-gate.json',
)
ALLOWED_SKEPTIC = ('research/round33/skeptic/ba1.md', 'research/round33/skeptic/ba2.md')
FORBIDDEN_PREFIXES = (
    'research/round33/forward/bb', 'research/round33/reverse/bb', 'research/round33/skeptic/bb',
    'research/round33/advisor/bb', 'research/round33/experts/', 'research/round33/advisor/deliberation',
    'research/round33/advisor/panel', 'research/round33/advisor/plan',
)
FORBIDDEN_WORDS = ('triage', 'recommendation', 'prospective', 'loop2', 'loop-2', 'deliberation', 'memo',
                   'contract-review', 'targets-proposal', 'bb-targets')
F1_NAME = 'F1 (AQ1 centered whole-star boxes)'
F2_NAME = 'F2 (I1 section 6 all-contained-face boxes with padding)'
STATE_TIERS = ('exact_first_order', 'crude_majorant')
DYN_TIER = 'polynomial_lieb_robinson'
DYN_ROUTES = ('duhamel_inner_f1', 'duhamel_inner_f2')
BB1_ROUTES = ('polymer_kp', 'iterated_split')
ASSEMBLY = 'union_comparison'
HYP_SOURCE = 'bb1_frozen_targets'
CONDITION = 'conditional_on_bb1_targets'
BB1_ROUTE_NOTE = 'attached at the BB2 gate from the BB1 gate bound value'
STATES_TOPOLOGY = 'trace norm on B(H_Y) for every finite complete-factor region Y'
DYNAMICS_TOPOLOGY = 'operator norm, uniformly for |theta|<=8 (compact window)'
GNS_TOPOLOGY = 'strong continuity of the GNS unitary group (not norm continuity in theta)'
CUTOFF_ORDER = ['bounds in each Q_L uniformly in L',
                'L to infinity at fixed N and M (AV1 F20-F23: Eckart vector bound, untruncated gap 1/2)',
                'N to infinity on the untruncated vectors only']
R_N_RULE = 'floor((N-1)/2)'
RATE_CERTIFIED_MAX = 14000
RATE_VACUOUS_AT = 14421


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


def factorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


GRID = 10 ** 40


def ceil_to(x, den=GRID):
    x = Q(x)
    return Q(-((-x.numerator * den) // x.denominator), den)


def floor_to(x, den=GRID):
    x = Q(x)
    return Q((x.numerator * den) // x.denominator, den)


E_UP = Q(27183, 10000)     # e < 27183/10000 (certified below)
E_LO = Q(2718, 1000)       # e > 2718/1000 (certified below)


def exp_series(x, terms=24):
    """Directed enclosure of exp(x) for 0<=x<=1: partial sum (lower) and partial sum plus
    the geometric tail bound x^(n+1)/(n+1)! / (1-x/(n+2)) (upper)."""
    x = Q(x)
    must(Q(0) <= x <= 1, 'exponential series argument outside [0,1]')
    partial, power = Q(0), Q(1)
    for k in range(terms + 1):
        partial += power / factorial(k)
        power *= x
    tail = power / factorial(terms + 1) / (1 - x / (terms + 2))
    return partial, partial + tail


def exp_up(x):
    """Rational upper bound of e^x for x>=0: E_UP^floor(x) times the series bound of e^frac."""
    x = Q(x)
    must(x >= 0, 'exp_up argument must be nonnegative')
    k = x.numerator // x.denominator
    return E_UP ** k * exp_series(x - k)[1]


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


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


def linf(a):
    return max(abs(a[0]), abs(a[1]), abs(a[2]))


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
        must(int(m.group(4)) == len(rs) * len(ss), 'I1 table row count mismatch')
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


def owners_of(anchor, cls):
    return tuple(sorted(vadd(anchor, v) for v in cls[3]))


def box_sites(N, shift=(0, 0, 0)):
    rng = range(-N, N + 1)
    return frozenset(vadd((x, y, z), shift) for x in rng for y in rng for z in rng)


def f1_faces(sites, classes):
    """Whole-star prescription on a general volume: omitted faces of whole stars b+S inside it."""
    out = {}
    for b in sites:
        if all(vadd(b, v) in sites for v in STAR):
            for k, cls in enumerate(classes):
                out[(b, k)] = owners_of(b, cls)
    return out


def f2_faces(sites, classes):
    """All-contained-face prescription on a general volume (owner set inside the volume)."""
    out = {}
    for b in sites:
        for k, cls in enumerate(classes):
            ow = owners_of(b, cls)
            if all(o in sites for o in ow):
                out[(b, k)] = ow
    return out


def padding(sites):
    return frozenset(vadd(b, v) for b in sites for v in STAR) - sites


def translate_faces(faces, v):
    return {(vadd(b, v), k): tuple(sorted(vadd(o, v) for o in ow)) for (b, k), ow in faces.items()}


def union_factor(V1, V2):
    """Legs of the union comparison: V1 against V1 u V2 and V2 against V1 u V2; a leg whose
    volume already equals the union costs nothing."""
    U = V1 | V2
    return (1 if V1 != U else 0) + (1 if V2 != U else 0)


def fine_class(p, o):
    return (o, p[0] % 4, p[1] % 2)


def fine_owners(p, o):
    name, a, c = [t for t in ORIENTATIONS if t[0] == o][0]
    return tuple(sorted({coarse(t) for t, _ in face_links(p, a, c)}))


def is_coarse_fine_translation(t):
    return t[0] % 4 == 0 and t[1] % 2 == 0


# -------------------------------------------- exact Gaussian-rational matrices
C0 = (Q(0), Q(0))
C1 = (Q(1), Q(0))
CI = (Q(0), Q(1))


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cconj(a):
    return (a[0], -a[1])


def cabs2(a):
    return a[0] * a[0] + a[1] * a[1]


def mat(rows):
    return tuple(tuple((Q(v), Q(0)) if not isinstance(v, tuple) else (Q(v[0]), Q(v[1])) for v in row) for row in rows)


def mmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    out = []
    for i in range(n):
        row = []
        for j in range(m):
            acc = C0
            for t in range(k):
                acc = cadd(acc, cmul(A[i][t], B[t][j]))
            row.append(acc)
        out.append(tuple(row))
    return tuple(out)


def mdag(A):
    return tuple(tuple(cconj(A[j][i]) for j in range(len(A))) for i in range(len(A[0])))


def mvec(A, v):
    return tuple(_sum(cmul(A[i][j], v[j]) for j in range(len(v))) for i in range(len(A)))


def _sum(items):
    acc = C0
    for x in items:
        acc = cadd(acc, x)
    return acc


def inner(u, v):
    return _sum(cmul(cconj(a), b) for a, b in zip(u, v))


PAULI_X = mat([[0, 1], [1, 0]])


def ipow(n):
    """i^n for integer n, exactly."""
    return (C1, CI, (Q(-1), Q(0)), (Q(0), Q(-1)))[n % 4]


# ------------------------------------------------------------ claim validators
GATE_FIELD_NAMES = ('whole_sequence_claimed', 'whole_sequence_scope', 'common_limit_claimed',
                    'state_convergence_claimed', 'translation_invariance_claimed', 'translation_invariance_scope',
                    'rate_in_N_claimed', 'dynamics_level', 'uniqueness_of_ground_state_claimed', 'rate_in_a_claimed',
                    'continuum_claim', 'gns_dynamics_equality_claimed', 'uniform_in_time_claimed',
                    'weak_coupling_claim', 'scientific_priority_verified')
ALWAYS_FALSE = ('uniqueness_of_ground_state_claimed', 'rate_in_a_claimed', 'continuum_claim',
                'gns_dynamics_equality_claimed', 'uniform_in_time_claimed', 'weak_coupling_claim',
                'scientific_priority_verified')
BB1_DEPENDENT = ('whole_sequence_claimed', 'common_limit_claimed', 'state_convergence_claimed',
                 'translation_invariance_claimed', 'rate_in_N_claimed')
EXPECTED_GATE_FIELDS = {
    'whole_sequence_claimed': True,
    'whole_sequence_scope': 'reduced densities of the named constructions F1 and F2 on every finite region',
    'common_limit_claimed': True, 'state_convergence_claimed': True, 'translation_invariance_claimed': True,
    'translation_invariance_scope': 'coarse translations; the limit of the named constructions',
    'rate_in_N_claimed': True, 'dynamics_level': 'correlation_functions_compact_window',
    'uniqueness_of_ground_state_claimed': False, 'rate_in_a_claimed': False, 'continuum_claim': False,
    'gns_dynamics_equality_claimed': False, 'uniform_in_time_claimed': False, 'weak_coupling_claim': False,
    'scientific_priority_verified': False}


def validate_claim_flags(flags):
    for key in ('continuum_claim', 'uniqueness_of_ground_state_claimed', 'gns_dynamics_equality_claimed',
                'uniform_in_time_claimed', 'rate_in_a_claimed', 'scientific_priority_verified', 'weak_coupling_claim',
                'uniform_wilson_claim', 'resolved_interaction_shift'):
        require(flags.get(key) is False, 'claim flag must be exactly false: ' + key)
    return True


def validate_gate_fields(exported, required, discharged):
    """gate_fields_rule: the contract values hold for accepted_within_scope after the discharge;
    an undischarged hypothesis keeps every field that depends on it false."""
    require(sorted(exported) == sorted(required) == sorted(GATE_FIELD_NAMES), 'gate fields must be exactly gate_fields_required')
    for key in ALWAYS_FALSE:
        require(exported[key] is False, 'gate field must be false: ' + key)
    for key in ('whole_sequence_scope', 'translation_invariance_scope'):
        require(exported[key] == required[key], 'gate field text differs from the contract: ' + key)
    if discharged:
        require(exported == required, 'after the discharge the gate fields are exactly the contract values')
    else:
        for key in BB1_DEPENDENT:
            require(exported[key] is False, 'undischarged BB1 hypothesis: field must stay false: ' + key)
        require(exported['dynamics_level'] != 'correlation_functions_compact_window',
                'undischarged BB1 hypothesis: dynamics_level must not be correlation_functions_compact_window')
    return True


def certify_clock(theta_window, U, clock_label):
    require(clock_label == 'theta=alpha t/hbar', 'physical clock must be theta=alpha t/hbar (common clock)')
    require(parse_q(U) == Q(parse_q(theta_window), 8), 'normalized window must be U=Theta/8 (u=theta/8, delta=alpha/8)')
    return True


def certify_model(rec, contract_tau):
    require(rec.get('model_id') == 'AQ_patterned_zero_selected', 'model id must be AQ_patterned_zero_selected')
    require(parse_q(rec.get('tau')) == contract_tau, 'packet tau differs from the contract (retuning or changed model)')
    require([parse_q(v) for v in rec.get('triple')] == [0, 0, 0], 'selected triple must be exactly (0,0,0)')
    require(rec.get('group') == 'SU(2)' and rec.get('dimension') == 3, 'group/dimension must be SU(2) on Z^3')
    require(rec.get('families') == [F1_NAME, F2_NAME], 'both named construction families required')
    require(rec.get('state_metric') == 'coarse l-infinity on factor sites (star diameter 1)', 'state metric must be coarse l-infinity')
    require(rec.get('dynamics_metric') == 'l1 on the coarse factor lattice, F(r)=(1+r)^-4', 'dynamics metric must be coarse l1 with the AQ1 F')
    require(parse_q(rec.get('window_theta')) == 8, 'window must be |theta|<=8')
    require(rec.get('finite_graph') is False and rec.get('uniform_model') is False, 'finite-graph or uniform model relabelled')
    return True


def certify_same_coupling(tau1, tau2, clock1='theta=alpha t/hbar', clock2='theta=alpha t/hbar'):
    require(parse_q(tau1) == parse_q(tau2), 'cross-coupling comparison rejected: every comparison at the same tau')
    require(clock1 == clock2 == 'theta=alpha t/hbar', 'both families and all comparisons use the common clock theta=alpha t/hbar')
    return True


def certify_hypothesis_record(rec, frozen):
    require(rec.get('source') == HYP_SOURCE, 'hypotheses must be the BB1 frozen targets')
    require(rec.get('label') == CONDITION, 'the condition conditional_on_bb1_targets was dropped')
    for key in ('q', 'C_h', 'c_h', 'q2_per_tau', 'C_2h', 'c_2h'):
        require(parse_q(rec.get(key)) == frozen[key], 'a BB1 value other than the frozen target: ' + key)
    require(rec.get('discharged') is False and rec.get('bb1_gate_sha256') is None,
            'a BB2 producer reads no BB1 gate and cannot record the discharge')
    require(rec.get('unconditional') is False, 'a conclusion called unconditional before the discharge')
    return True


def certify_monotone(fn, points, deltas):
    """Each state constant must be nondecreasing in each hypothesis constant (checked exactly)."""
    for Ch, ch in points:
        base = fn(Ch, ch)
        for d in deltas:
            require(fn(Ch + d, ch) >= base, 'constant decreases when C_h increases')
            require(fn(Ch, ch + d) >= base, 'constant decreases when c_h increases')
    return True


def certify_state_constant(rec):
    require(rec.get('tier') in STATE_TIERS, 'state constant must carry exactly one state tier (exact_first_order or crude_majorant)')
    require(rec.get('assembly') == ASSEMBLY, 'the reverse assembly is union_comparison, recorded in the assembly field')
    require(rec.get('hypothesis_source') == HYP_SOURCE, 'state constant must name the hypothesis source bb1_frozen_targets')
    require('route' not in rec, 'assembly or a route recorded as a route label on a BB2 state constant')
    require(rec.get('bb1_route') == BB1_ROUTE_NOTE, 'a BB2 producer cannot claim a BB1 route (polymer_kp or iterated_split)')
    require(parse_q(rec.get('assembly_factor')) == 1, 'nested centered cubes: the union is the larger cube, factor 1')
    return True


def certify_dynamics_constant(rec, options):
    require(rec.get('tier') == DYN_TIER, 'dynamics constant must carry the tier polynomial_lieb_robinson')
    require(rec.get('route') in DYN_ROUTES, 'dynamics constant must carry exactly one BA2 route')
    require(rec.get('source') == BA2_GATE_REL, 'dynamics constant must be read from the BA2 gate')
    require('assembly' not in rec and 'hypothesis_source' not in rec, 'state labels on a dynamics constant (tier mixing)')
    key = (rec.get('family'), rec.get('route'))
    require(key in options, 'route not admitted for this family in the BA2 gate')
    require(parse_q(rec.get('value')) in [2 * k for k in options[key]],
            'dynamics constant is not twice an exact BA2 gate value of its route (finite-box and limit replacement)')
    return True


def certify_item5(rec):
    require(rec.get('r_N') == R_N_RULE, 'r_N must be floor((N-1)/2) as frozen')
    require(rec.get('N_min') == 5, 'item 5 needs N at least 5 (r_N at least 2)')
    require(rec.get('centering') == 'complex_mean', 'correlations are centred with |omega(A)|^2 (complex means)')
    require(rec.get('window') == '|theta|<=8', 'window must be |theta|<=8')
    require(rec.get('constants') == ['C_dyn', 'c_site_prime', 'C_prime'] and rec.get('lumped') is False,
            'three separate constants: a single lumped bracket for item 5 is rejected')
    require(rec.get('combine') == 'linear', 'deterministic terms add linearly')
    require(rec.get('decay') == 'polynomial', 'exponential Lieb-Robinson tail claimed with the polynomial F')
    require(rec.get('uniform_in_time') is False, 'uniform-in-time claim rejected')
    require(rec.get('gns_dynamics_equality') is False, 'equality of GNS dynamics of different states rejected')
    return True


def certify_rate_claim(claim, certified_max, vacuous_at):
    """O(1/N) is certified for the frozen bound on 5<=N<=certified_max; at vacuous_at the frozen
    region term alone exceeds the trivial bound 2 (exact witness)."""
    require(claim.get('form') == 'O(1/N)', 'the rate of the frozen bound is O(1/N) (polynomial F), never exponential')
    rng = claim.get('range')
    require(isinstance(rng, list) and len(rng) == 2 and rng[0] == 5 and isinstance(rng[1], int),
            'the O(1/N) range must be stated explicitly')
    require(rng[1] <= certified_max, 'O(1/N) claimed beyond the certified range: the frozen bound is vacuous at N=' + str(vacuous_at))
    return True


def certify_r_N(rule, label='rule'):
    require(label != 'post_hoc', 'post-hoc choice of r_N rejected')
    for N in range(5, 400):
        require(rule(N) == (N - 1) // 2, 'r_N differs from floor((N-1)/2) at N=' + str(N))
    return True


def certify_centering(omega_AA, centering_value, var_vector):
    """The centred correlation at theta=0 is the squared norm of (A-a)phi: omega(A*A)-|a|^2."""
    require(parse_q(omega_AA[0]) - parse_q(centering_value) == var_vector and omega_AA[1] == 0,
            'centering must use |omega(A)|^2 (complex mean), not omega(A)^2')
    return True


def certify_cauchy_claim(rec):
    require(rec.get('kind') == 'sup_over_all_M_greater_than_N', 'an N to N+1 bound alone is not a Cauchy estimate')
    require(rec.get('limit_from') == 'Cauchy bound and completeness of the trace class',
            'whole-sequence convergence from compactness plus closeness is rejected')
    return True


def certify_whole_sequence(tail_sups, bound):
    """tail_sups[N] = sup over M>N (in the window) of the distance; a whole-sequence claim needs
    an explicit bound b(N)>=tail_sups[N] with b(N)->0 (here: b(last)<=1/1000)."""
    for N, s in tail_sups.items():
        require(s <= bound(N), 'tail supremum exceeds the claimed Cauchy bound at N=' + str(N))
    last = max(tail_sups)
    require(bound(last) <= Q(1, 1000), 'the claimed bound does not tend to zero')
    return True


def certify_limit_statement(rec):
    require(rec.get('quantifier') in ('whole sequence', 'subsequence'), 'limit statement must say whole sequence or subsequence')
    if rec['quantifier'] == 'whole sequence':
        require(rec.get('from') == 'Cauchy bound', 'whole-sequence claims come only from a Cauchy bound')
    return True


def certify_topology(rec):
    require(rec.get('states') == STATES_TOPOLOGY, 'state topology must be the trace norm on B(H_Y)')
    require(rec.get('dynamics') == DYNAMICS_TOPOLOGY, 'dynamics topology must be the norm on the compact window')
    require(rec.get('representations') == GNS_TOPOLOGY, 'representations: GNS strong continuity only')
    require(len({rec['states'], rec['dynamics'], rec['representations']}) == 3, 'one topology for everything rejected')
    return True


def certify_families(rec):
    require(rec == [F1_NAME, F2_NAME], 'exactly the two named families F1 and F2')
    return True


def certify_family_faces(f1_set, f2_set):
    require(f1_set != f2_set and set(f1_set) < set(f2_set), 'F2 collapsed onto F1 (the families differ by the extra faces)')
    return True


def certify_identification(rec, admitted):
    require(rec.get('order') == ['whole-sequence limit', 'identified with every AQ1 and every F2 subsequential limit',
                                 'properties inherited'], 'inheriting AQ1/AQ2 properties before the identification is rejected')
    require(rec.get('sequence') == 'whole sequence', 'identification needs the whole-sequence limit')
    require(rec.get('source') == 'every subsequence of a trace-norm convergent sequence has the same limit on each finite region',
            'identification source must be the whole-sequence convergence')
    for prop in rec.get('inherited', []):
        gate = prop.get('gate')
        require(gate in admitted and prop.get('gate_text') in admitted[gate],
                'property not admitted by its gate: ' + str(prop.get('name')))
    return True


def certify_translation(rec, Ch, q):
    v, fine = rec.get('v'), rec.get('fine')
    require(tuple(fine) == (4 * v[0], 2 * v[1], v[2]), 'non-coarse fine translation rejected (breaks residues and face classes)')
    require(rec.get('item') == 'pre-registered item 4', 'translation invariance only as the separate pre-registered item 4')
    require(rec.get('source') == 'bb1 general-volume comparison: Lambda_N+v versus Lambda_N, both containing Lambda_(N-|v|_inf)',
            'translation invariance from nested cubes alone is rejected')
    N = rec.get('N')
    require(N >= linf(v) + 2, 'needs N at least |v|_inf+2')
    require(parse_q(rec.get('bound')) == Ch * q ** (N - linf(v) - 1), 'bound must be C_h q^(N-|v|_inf-1)')
    return True


def certify_fine_symmetry(t, preserved):
    require(preserved is True and is_coarse_fine_translation(t), 'a non-coarse fine translation is not a symmetry of the patterned model')
    return True


def certify_region_bound(rec, N, Y):
    require(rec.get('constant') == 'c_site_prime', 'a constant proved for R reused on a region Y')
    require(rec.get('size_factor') == '|Y| e^{|Y|/10^8}', 'region bound must carry |Y| e^{|Y|/10^8}')
    require(rec.get('exponent') == N - max(linf(y) for y in Y), 'region exponent must be d_Y = N - max_Y |y|_inf')
    return True


def certify_cutoff(rec):
    require(rec.get('order') == CUTOFF_ORDER, 'the N and L limits are never exchanged (uniform in L, then L at fixed N)')
    require(rec.get('constants_depend_on_L') is False, 'Cauchy constants must be uniform in the cutoff L')
    require(rec.get('vector_removal') is True, 'eigenvalue convergence alone does not remove the cutoff for vectors')
    return True


def certify_dynamics_level(rec):
    require(rec.get('level') == 'correlation_functions_compact_window', 'dynamics level is correlation functions on a compact window')
    require(rec.get('gns_equality_of_different_states') is False, 'equality of GNS dynamics of different states rejected')
    require(rec.get('correlations_of_different_states_equal') is False, 'equality of correlation functions of different states rejected')
    return True


def certify_window(rec):
    require(rec.get('uniform_in_time') is False, 'uniform-in-time claim rejected (the BA2 bounds grow like U^2/(1-vU/3))')
    require(rec.get('window') == '|theta|<=8' and rec.get('U') == '1', 'window must be named with U=Theta/8')
    return True


def certify_outcome(recorded, facts):
    if not facts['cauchy_closed'] or facts['discharge'] == 'bb1_insufficient':
        want = 'insufficient'
    elif facts['discharge'] == 'partial' or not all(facts['items'].values()) or not facts['targets_met']:
        want = 'limited'
    else:
        want = 'accepted_within_scope'
    require(recorded == want, 'recorded verdict ' + str(recorded) + ' differs from the rule (' + want + ')')
    if facts['discharge'] == 'pending':
        require(facts.get('condition') == CONDITION, 'a verdict proposed before the discharge must carry the condition')
    return True


def admit_bound(value, target):
    v, t = parse_q(value), parse_q(target)
    require(v <= t, 'bound exceeds the frozen target')
    return True


def assemble_linear(terms, combine='linear'):
    require(combine == 'linear', 'root-sum-square or root-N assembly rejected')
    return sum((parse_q(t) for t in terms), Q(0))


def divide_by_root(value, count):
    require(False, 'division by sqrt(N) rejected for deterministic bounds')


def certify_scaling(ratio, bracket):
    lo, hi = bracket
    require(lo <= ratio <= hi, 'tau -> tau/100 ratio outside its preregistered bracket')
    return True


def certify_rate_pair(rec, frozen_q, Ch, ch):
    require(parse_q(rec.get('q')) == frozen_q, 'the rate pair is frozen at q=1/64 (no q optimized per N)')
    require(rec.get('q_per_N') is False, 'optimizing q per N rejected')
    require(parse_q(rec.get('C_h')) == Ch and parse_q(rec.get('c_h')) == ch, 'hypothesis constants are frozen')
    return True


def certify_uniformity(text):
    low = text.lower()
    require(re.search(r'uniform(ly)? in (the )?(lattice spacing|a)(?![a-z0-9_])', low) is None,
            'uniformity in the lattice spacing rejected')
    require(re.search(r'(g|bare coupling) ?-> ?0', low) is None and 'continuum' not in low, 'weak coupling or continuum reading rejected')
    require('in n at fixed spacing' in low, "uniformity statements must say 'in N at fixed spacing'")
    return True


def certify_rate_units(text):
    low = text.lower()
    for bad in ('fm', 'fermi', 'physical length', 'correlation length', 'in the lattice spacing', 'per a'):
        require(re.search(r'(?<![a-z])' + re.escape(bad) + r'(?![a-z])', low) is None, 'rate converted to a physical length or to a')
    require('per coarse step' in low, 'rate must be per coarse step at fixed spacing')
    return True


def certify_error_ledger(ledger, names):
    require(sorted(ledger) == sorted(names), 'error ledger must itemize exactly the preregistered terms')
    for k, v in ledger.items():
        require(isinstance(v, dict) and ('value' in v or 'not_applicable' in v), 'ledger entry malformed: ' + k)
        if 'not_applicable' in v:
            require(bool(v.get('reason')), 'not_applicable ledger entry needs a stated reason: ' + k)
    return True


def certify_cutoff_exchange(a, Lmax):
    """Fixture a(N,L)=1 if L<=N else 0: the iterated limits differ, so the order is part of the claim."""
    lim_N_then_L = all(a(N, L) == 1 for L in range(1, Lmax) for N in range(L, Lmax))
    lim_L_then_N = all(a(N, L) == 0 for N in range(1, Lmax) for L in range(N + 1, Lmax + N))
    require(lim_N_then_L and lim_L_then_N, 'exchange fixture broken')
    return True


# --------------------------------------------------------- text scanners
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


def _norm_ws(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def phrase_hits(text, forbidden, template):
    body = _norm_ws(text)
    if template:
        body = body.replace(_norm_ws(template), ' ')
    hits = []
    for clause in [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', body) if c.strip()]:
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                if not NEGATION.search(clause):
                    hits.append(phrase + ' :: ' + clause[:160])
    return hits


def certify_phrasing(text, forbidden, template):
    hits = phrase_hits(text, forbidden, template)
    require(hits == [], 'affirmative forbidden phrasing: ' + (hits[0] if hits else ''))
    return True


PLACEHOLDER = re.compile(r'<[^<>]*>')


def certify_no_placeholder(strings):
    for s in strings:
        for m in PLACEHOLDER.finditer(s):
            span = m.group(0)
            require(not (re.search(r'\s', span) or '|' in span or 'e.g.' in span), 'placeholder span blocks the freeze: ' + span[:60])
    return True


def all_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from all_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from all_strings(v)


def certify_template_span(report_text, template):
    require(report_text.count(template) == 1, 'mandatory sentence template must appear exactly once verbatim')
    require(any(template in line for line in report_text.splitlines()), 'mandatory sentence template must be one unbroken span on one line')
    return True


def ns_quote_lines(ns_text):
    """Verbatim Part A statements used here (the finite-box dynamics (44)-(46) and Theorem 4.1)."""
    part_a = ns_text.split('## Part A.')[1].split('## Part B.')[0]
    lines = [ln for ln in part_a.splitlines() if ln.strip()]
    wanted = []
    for tag in ('(44)', '(77)'):
        hit = [ln[2:] for ln in lines if ln.startswith('- ' + tag)]
        must(len(hit) == 1, 'excerpt line missing: ' + tag)
        wanted.append(hit[0])
    for start in ('essentially self-adjoint on the dense domain (45)', 'exists and the convergence is uniform for t in compact sets.'):
        hit = [ln for ln in lines if ln.startswith(start)]
        must(len(hit) == 1, 'excerpt passage missing: ' + start)
        wanted.append(hit[0])
    t41 = [ln for ln in lines if ln.startswith('**Theorem 4.1**')]
    must(len(t41) == 1, 'Theorem 4.1 line missing')
    body = t41[0].split('). ', 1)[1]
    must(body.startswith('Let Γ and F be as described in Section 3.'), 'Theorem 4.1 statement start')
    wanted.append(body)
    return wanted


def certify_quotes(report_text, quotes, source_label):
    require(source_label == NS_REL, 'the limit-dynamics theorem must be quoted from the committed excerpt, not second-hand')
    for q in quotes:
        require(q in report_text, 'Nachtergaele-Sims passage not quoted verbatim: ' + q[:70])
    return True


# ------------------------------------------------------ contract and premises
CONTROL_IDS = (
    'coherent_evidence_tampering', 'exact_arithmetic_admission', 'no_priority_or_continuum_claim',
    'changed_model_relabelled', 'insufficient_verdict_retained', 'tau_scaling_exponent', 'wrong_delta_alpha_hbar_clock',
    'root_n_misuse', 'tier_mixing_rejected', 'reverse_premise_isolation', 'uniform_in_N_not_in_a',
    'placeholder_span_rejected', 'negation_aware_phrase_scan', 'parameters_declare_metric_weights_window',
    'rate_constant_pair_prefrozen', 'decay_rate_in_N_not_a', 'topology_named', 'two_families_named',
    'subsequence_versus_whole_sequence', 'common_clock', 'named_construction_not_uniqueness',
    'cauchy_estimate_not_compactness', 'limit_identified_with_aq1_limits', 'translation_invariance_separate_item',
    'region_constant_scales_with_Y', 'cutoff_uniform_then_removed', 'algebraic_not_gns_dynamics',
    'lieb_robinson_polynomial_tail', 'time_window_named_common_clock', 'fixture_whole_sequence_vs_subsequence',
    'fixture_translation_residues', 'fixture_correlation_centering', 'conditional_on_bb1_targets', 'r_N_prefrozen')
EXPECTED_EXCLUSIONS = [
    'uniqueness of every infinite-volume ground state', 'states outside the named constructions',
    'uniform-in-time statements', 'equality of GNS dynamics of different states',
    'any estimate uniform in the lattice spacing a', 'continuum or weak coupling', 'scientific priority']
EXPECTED_PREREG_EXCLUSIONS = [
    'uniqueness of every infinite-volume ground state',
    'statements about boundary conditions outside the named constructions',
    'any estimate uniform in the lattice spacing a', 'continuum or weak coupling', 'scientific priority']
ERROR_TERMS = ['bb1_hypothesis_constants', 'cauchy_telescoping_or_union', 'identification_with_subsequential_limits',
               'translation_general_volume', 'dynamics_constant_from_ba2', 'region_form_on_Lambda_rN', 'arithmetic']
TARGET_C_PRIME = Q(1, 100000)
TARGET_C_SITE = Q(1, 200000)
TARGET_C_DYN = Q(1, 2000000000)
TARGET_C_PRIME_2 = Q(1, 8000)


def parse_bb1_contract(data):
    require(data.get('id') == 'BB1' and data.get('status') == 'frozen_before_production', 'BB1 contract identity')
    rp = data['parameters']['rate_constant_pair']
    require(rp['headline']['tier'] == 'exact_first_order', 'BB1 headline tier')
    sec = re.match(r'(\d+)\|tau\|', rp['secondary']['q'])
    require(sec is not None, 'BB1 secondary q malformed')
    region = rp['region_form']['form']
    require('c_site |Y| e^{|Y|/10^8} q^{d_Y}, d_Y = N - max_{y in Y} |y|_inf (so d_R = N-1)' in region, 'BB1 region form text')
    comps = data['parameters']['comparisons']
    require(len(comps) == 5 and comps[3].startswith('any two centered boxes') and comps[4].startswith('two finite complete-factor volumes of one prescription'),
            'BB1 comparison list')
    require('a comparison of the reduced densities through the union costs a factor 2 and is labelled only' in comps[4],
            'BB1 union wording')
    return {'q': parse_q(rp['headline']['q']), 'C_h': parse_q(rp['headline']['C_target']),
            'c_h': parse_q(rp['region_form']['c_site_target']), 'q2_per_tau': Q(int(sec.group(1))),
            'C_2h': parse_q(rp['secondary']['C_target']), 'c_2h': parse_q(rp['secondary']['c_site_target']),
            'comparisons': list(comps), 'region_form': region}


def parse_contract_numbers(data, bb1):
    p, pre, ncs = data['parameters'], data['preregistration'], data['new_control_semantics']
    for key in ('metric', 'weights', 'window', 'clock'):
        require(isinstance(p.get(key), str) and bool(p.get(key)), 'parameters must declare ' + key + ' as a field (not prose)')
    require('clock' in pre and 'theta=alpha*t/hbar' in pre['clock'] and 'u=theta/8' in pre['clock'], 'preregistration clock field')
    require(p['clock'] == 'theta=alpha t/hbar for item 5' and p['window'] == '|theta| at most 8 (item 5)', 'clock/window fields')
    require('coarse l-infinity metric on factor sites (star diameter 1) for states' in p['metric']
            and 'l1 on the coarse factor lattice with F(r)=(1+r)^-4 for dynamics' in p['metric'], 'metric field malformed')
    rp = p['rate_constant_pair']
    m = re.search(r'with q=(1/64), C_h=(1/\d+) and c_h=(1/\d+); secondary q_2=(\d+)\|tau\|, C_2h=(1/\d+), c_2h=(1/\d+)', rp['hypotheses'])
    require(m is not None, 'hypothesis text malformed')
    hyp = {'q': Q(m.group(1)), 'C_h': Q(m.group(2)), 'c_h': Q(m.group(3)), 'q2_per_tau': Q(int(m.group(4))),
           'C_2h': Q(m.group(5)), 'c_2h': Q(m.group(6))}
    m2 = re.search(r'the R form with C_h=(1/\d+) and the region form with c_h=(1/\d+) at q=(1/64) \(secondary: C_2h=(1/\d+) '
                   r'and c_2h=(1/\d+) at q_2=(\d+)\|tau\|\)', ncs['conditional_on_bb1_targets'])
    require(m2 is not None, 'conditional_on_bb1_targets semantics malformed')
    hyp2 = {'C_h': Q(m2.group(1)), 'c_h': Q(m2.group(2)), 'q': Q(m2.group(3)), 'C_2h': Q(m2.group(4)),
            'c_2h': Q(m2.group(5)), 'q2_per_tau': Q(int(m2.group(6)))}
    for key in hyp2:
        require(hyp[key] == hyp2[key] == bb1[key], 'hypothesis differs from the BB1 frozen target: ' + key)
    h = rp['headline']
    require(parse_q(h['q']) == hyp['q'] and h['tier'] == 'exact_first_order', 'headline q/tier')
    tC, tc = parse_q(h['C_prime_target']), parse_q(h['c_site_prime_target'])
    d = rp['dynamics']
    tD = parse_q(d['C_dyn_target'])
    require(d['tier'] == DYN_TIER and 'duhamel_inner_f1 or duhamel_inner_f2' in d['routes'], 'dynamics tier/routes')
    tC2 = parse_q(rp['secondary']['C_prime_target'])
    require('151552|tau|' in rp['secondary']['q'], 'secondary q')
    require((tC, tc, tD, tC2) == (TARGET_C_PRIME, TARGET_C_SITE, TARGET_C_DYN, TARGET_C_PRIME_2), 'targets differ from the frozen values')
    vals = pre['target']['value']
    require(vals == '1/100000, 1/200000 and 1/2000000000' and pre['target']['comparator'] == '<=', 'preregistered target values')
    items = p['items']
    require('r_N=floor((N-1)/2)' in items['5_correlations'] and 'N at least 5' in items['5_correlations']
            and '|theta| at most 8' in items['5_correlations'], 'item 5 frozen parameters')
    require("||A||^2 [C_dyn/(r_N-1) + c'_site |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N-r_N) + 2C' q^(N-1)]" in items['5_correlations'],
            'item 5 formula changed')
    require('-|omega^{F,N}(A)|^2' in items['5_correlations'], 'item 5 centering changed')
    require('C_h q^(N-|v|_inf-1) for N at least |v|_inf+2' in items['4_translations']
            and '(fine translation (4v_x,2v_y,v_z), preserving residues and face classes)' in items['4_translations'], 'item 4 text')
    require('sup over M greater than N' in items['1_whole_sequence'] and 'c\'_site |Y| e^{|Y|/10^8} q^{d_Y}' in items['1_whole_sequence'],
            'item 1 text')
    require(ncs['r_N_prefrozen'].startswith('r_N = floor((N-1)/2) is frozen as written'), 'r_N semantics changed')
    br = pre['scaling_brackets_per_constant']
    require(br['C_prime'].startswith('exactly 1') and br['c_site_prime'].startswith('exactly 1'), 'state brackets')
    bd = re.match(r'\[(\d+),(\d+)\]', br['C_dyn'])
    bs = re.match(r'\[(\d+)/(\d+),(\d+)/(\d+)\]', br['secondary_constants'])
    require(bd is not None and bs is not None and br['q_secondary'] == 'exactly 100', 'scaling brackets malformed')
    require(br['item_5_sum'].startswith('no single bracket'), 'item-5 sum bracket rule')
    return {
        'hyp': hyp, 'target_C_prime': tC, 'target_c_site': tc, 'target_C_dyn': tD, 'target_C_prime_2': tC2,
        'bracket_C_dyn': (Q(int(bd.group(1))), Q(int(bd.group(2)))),
        'bracket_secondary': (Q(int(bs.group(1)), int(bs.group(2))), Q(int(bs.group(3)), int(bs.group(4)))),
        'bracket_state': (Q(1), Q(1)), 'bracket_q2': (Q(100), Q(100)),
        'tau': parse_q(pre['tau']['value']), 'N_min_item5': 5,
    }


def validate_contract(data, bb1):
    require(data.get('id') == 'BB2' and data.get('round') == 33 and data.get('status') == 'frozen_before_production',
            'contract identity or status')
    require(data.get('human_author') == 'Hruday N M (BUNZEEY)', 'human author')
    require(data.get('direction') == 'paired' and data.get('producers') == ['forward', 'reverse'], 'paired producers')
    require(data.get('reverse_premise_isolation') is True, 'reverse premise isolation flag')
    pre = data['preregistration']
    require(pre.get('frozen_before_any_outcome') is True, 'preregistration frozen flag')
    require(all(v is True for v in pre['hash_binding'].values()) and len(pre['hash_binding']) == 4, 'hash-binding flags')
    require(pre.get('model_id') == 'AQ_patterned_zero_selected', 'model id')
    require([parse_q(x) for x in pre['selected_triple_alpha_units']] == [0, 0, 0], 'selected triple is not zero')
    require(parse_q(pre['tau']['value']) == Q(1, 10 ** 8) and pre['tau']['signs_evaluated'] == ['+', '-'], 'tau value or signs')
    require(pre['tau']['is_model_change_vs_previous_loop'] is False, 'tau model-change flag')
    require(F1_NAME in data['model'] and F2_NAME in data['model'] and '|tau|<=10^-8' in data['model'], 'families or cap missing')
    ids = data['controls']
    require(tuple(ids) == CONTROL_IDS and ids == pre['controls_required']['ids'], 'controls differ from the preregistered ids')
    require(set(data['new_control_semantics']) <= set(ids), 'control semantics for an unknown control')
    require(sorted(data['shared_premises']) == sorted(REQUIRED_PREMISES), 'shared premises differ from the frozen list')
    require(data['claim_exclusions'] == EXPECTED_EXCLUSIONS, 'claim exclusions changed')
    require(pre['claim_exclusions'] == EXPECTED_PREREG_EXCLUSIONS, 'preregistration claim exclusions changed')
    require(pre['error_terms_itemized'] == ERROR_TERMS, 'error terms')
    require(pre['gate_fields_required'] == EXPECTED_GATE_FIELDS, 'gate_fields_required changed')
    require(pre['sub_labels_allowed'] == ['convergence_of_named_constructions', 'common_limit_of_named_constructions'], 'sub-labels')
    certify_no_placeholder(list(all_strings(data)))
    return parse_contract_numbers(data, bb1)


def validate_contract_bytes(raw, expected_sha, bb1):
    require(sha256_bytes(raw) == expected_sha, 'contract bytes do not match the bound hash')
    data = json.loads(raw)
    return data, validate_contract(data, bb1)


def validate_bb1_bytes(raw, expected_sha):
    require(sha256_bytes(raw) == expected_sha, 'BB1 contract bytes do not match the bound hash')
    return parse_bb1_contract(json.loads(raw))


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    for f in files:
        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)
        require(not any(w in f.lower() for w in FORBIDDEN_WORDS), 'forbidden triage/deliberation/memo file in reverse inputs: ' + f)
        if f.startswith('research/round33/skeptic/'):
            require(f in ALLOWED_SKEPTIC, 'only the declared BA1 and BA2 reviews may be skeptic inputs: ' + f)
    require(set(REQUIRED_PREMISES) <= set(files), 'a declared premise snapshot is missing')
    require(sorted(files) == sorted(expected) and len(files) == len(expected),
            'reverse inputs inventory differs from AGENTS.md + contract + shared_premises')
    return True


def certify_pinned(rel, raw):
    require(sha256_bytes(raw) == PINNED_SHA256[rel], 'pinned premise changed: ' + rel)
    return True


def tamper(raw, edit):
    data = json.loads(raw)
    edit(data)
    return json.dumps(data, indent=1).encode()


# ------------------------------------------------ BA2 gate: dynamics constants
BA2_PATTERNS = {
    'K_F1_fwd': r'F1 with K_F1 = (\d+/\d+) \(about 5\.94718e-11, forward, faces charged once, inner F1\)',
    'K_F1_rev': r'and the second route (\d+/\d+) \(about 1\.01951e-10, reverse, whole stars, inner F1 on Lambda_M\)',
    'K_F2_fwd': r'F2 with K_F2 = (\d+/\d+) \(about 9\.45177e-11, forward, one F1-inner Duhamel plus the comparison\)',
    'K_F2_rev': r"and the second route (\d+/\d+) \(about 3\.46428e-11, reverse, owner-set Phi', faces charged once\)",
}
BA2_REQUIRED_TEXT = (
    '||T^{F2,N}_theta(A)-T_theta(A)|| <= min(K_F1, second-route K_F2)/(N-1) ||A||',
    'every value is at most the frozen 2.5x10^-10',
    'route duhamel_inner_f1', 'route duhamel_inner_f2', 'tier polynomial_lieb_robinson',
    'the F2 limit dynamics equals the AQ1 limit dynamics T_theta',
    'AQ1 sections 4-5 are rerun for every subsequential F2 limit state',
)


def parse_ba2_gate(raw):
    certify_pinned(BA2_GATE_REL, raw)
    g = json.loads(raw)
    require(g.get('verdict') == 'accepted_within_scope' and g.get('loop') == 'BA2', 'BA2 gate verdict')
    acc = g['accepted']
    vals = {}
    for key, pat in BA2_PATTERNS.items():
        m = re.search(pat, acc)
        require(m is not None, 'BA2 gate constant not found: ' + key)
        vals[key] = parse_q(m.group(1))
    for t in BA2_REQUIRED_TEXT:
        require(t in acc, 'BA2 gate statement missing: ' + t[:60])
    gf = g['gate_fields']
    require(gf['whole_sequence_claimed'] is True and gf['dynamics_limit_identified_claimed'] is True
            and gf['dynamics_level'] == 'algebraic_heisenberg_compact_window', 'BA2 gate fields')
    return vals, g


def K_F1_formula(tau):
    """BA2 forward (HNM-BA2-F08): K_c1 = 592704 tau^2/(1-338688|tau|), inner F1, faces charged once."""
    a = abs(Q(tau))
    return 592704 * a * a / (1 - 338688 * a)


def E_up_ba2(y):
    """BA2 reverse rational upper bound of E(y)=2(e^y-1-y)/y^2."""
    return 1 + y / 3 + y * y / (12 * (1 - y / 5))


def K_F2_rev_formula(tau):
    """BA2 reverse: c2 = 345744 tau^2 U^2 E_up(592704|tau|U), U=1, inner F2, owner-set Phi'."""
    a = abs(Q(tau))
    return 345744 * a * a * E_up_ba2(592704 * a)


def K_F1_rev_formula(tau):
    a = abs(Q(tau))
    return 1016064 * a * a * E_up_ba2(1016064 * a)


def K_F2_fwd_formula(tau):
    a = abs(Q(tau))
    return 941976 * a * a / (1 - 338688 * a)


# ==================================================================== compute
def positive_checks():
    check_py_sha = sha256_file(HERE / 'check.py')                  # recorded before any evaluation
    raw = (INPUTS / CONTRACT_REL).read_bytes()
    bb1_raw = (INPUTS / BB1_CONTRACT_REL).read_bytes()
    contract_sha, bb1_sha = sha256_bytes(raw), sha256_bytes(bb1_raw)
    must(contract_sha == CONTRACT_SHA256, 'BB2 contract snapshot hash differs from the bound constant')
    must(bb1_sha == BB1_CONTRACT_SHA256, 'BB1 contract snapshot hash differs from the bound constant')
    pinned = {}
    for rel in sorted(PINNED_SHA256):
        rb = (INPUTS / rel).read_bytes()
        must(sha256_bytes(rb) == PINNED_SHA256[rel], 'pinned premise hash changed: ' + rel)
        pinned[rel] = sha256_bytes(rb)
    bb1 = validate_bb1_bytes(bb1_raw, BB1_CONTRACT_SHA256)
    contract, P = validate_contract_bytes(raw, CONTRACT_SHA256, bb1)
    check('contract_snapshots_bound_before_evaluation', contract_sha == CONTRACT_SHA256 and bb1_sha == BB1_CONTRACT_SHA256,
          bb2_contract_sha256=contract_sha, bb1_contract_sha256=bb1_sha, verified='both before any evaluation',
          sources=['inputs/' + CONTRACT_REL, 'inputs/' + BB1_CONTRACT_REL])
    check('check_py_sha256_recorded_before_evaluation', len(check_py_sha) == 64, check_py_sha256=check_py_sha)
    ns_text = (INPUTS / NS_REL).read_text()
    check('pinned_gate_and_excerpt_hashes', NS_PDF_SHA256 in ns_text and len(pinned) == len(PINNED_SHA256),
          pinned_sha256=pinned, ns_pdf_sha256_named_in_excerpt=NS_PDF_SHA256)
    cache = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if '__pycache__' in p.parts or p.suffix == '.pyc')
    check('no_interpreter_cache_in_closure', cache == [])
    files = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    check('reverse_inputs_inventory_isolated', validate_inventory(files, contract), inputs=len(files),
          declared='AGENTS.md + contract + 36 shared premises', skeptic_inputs=list(ALLOWED_SKEPTIC))
    pre, ncs = contract['preregistration'], contract['new_control_semantics']
    TAU = P['tau']
    THETA = Q(8)
    U = THETA / 8
    must(certify_clock(THETA, U, 'theta=alpha t/hbar') and U == 1, 'clock conversion')
    template = pre['mandatory_sentence_template']
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])
    hyp = P['hyp']
    q, Ch, ch = hyp['q'], hyp['C_h'], hyp['c_h']

    # -------------------------------------------------- hypotheses (BB1 frozen targets)
    hyp_rec = {'source': HYP_SOURCE, 'label': CONDITION, 'q': qs(q), 'C_h': qs(Ch), 'c_h': qs(ch),
               'q2_per_tau': qs(hyp['q2_per_tau']), 'C_2h': qs(hyp['C_2h']), 'c_2h': qs(hyp['c_2h']),
               'discharged': False, 'bb1_gate_sha256': None, 'unconditional': False}
    comps = bb1['comparisons']
    check('hypotheses_equal_bb1_frozen_targets', certify_hypothesis_record(hyp_rec, bb1),
          hypotheses=hyp_rec, read_from=['bb2 parameters.rate_constant_pair.hypotheses',
                                         'bb2 new_control_semantics.conditional_on_bb1_targets',
                                         'bb1 parameters.rate_constant_pair (C_target, c_site_target, secondary)'],
          bb1_comparisons={'B' + str(i + 1): c for i, c in enumerate(comps)}, bb1_region_form=bb1['region_form'],
          discharge='not recorded by this producer (it reads no BB1 gate); recorded at the BB2 gate')

    # -------------------------------------------------- BA2 gate dynamics constants
    ba2_raw = (INPUTS / BA2_GATE_REL).read_bytes()
    ba2, ba2_gate = parse_ba2_gate(ba2_raw)
    ba2f = (INPUTS / BA2F_REL).read_text()
    ba2r = (INPUTS / BA2R_REL).read_text()
    formula_prov = ('K_c1 = 592704 tau^2/(1-338688|tau|) = 9261/155720800000000' in ba2f
                    and 'K_c2=K_c1+(11/8)K_cmp=941976 tau^2/(1-338688|tau|)=117747/1245766400000000' in ba2f
                    and 'c2 = 345744 tau^2U^2E_up(592704|tau|U) = 1055961408185869563/30481402343750000000000000000' in ba2r
                    and 'c1 = 1016064 tau^2U^2E_up(1016064|tau|U) = 12128856933354903/118967041015625000000000000' in ba2r
                    and '`E_up(y)=1+y/3+y^2/(12(1-y/5))`' in ba2r)
    formulas_match = (K_F1_formula(TAU) == ba2['K_F1_fwd'] and K_F2_rev_formula(TAU) == ba2['K_F2_rev']
                      and K_F1_rev_formula(TAU) == ba2['K_F1_rev'] and K_F2_fwd_formula(TAU) == ba2['K_F2_fwd'])
    options = {('F1', 'duhamel_inner_f1'): [ba2['K_F1_fwd'], ba2['K_F1_rev']],
               ('F2', 'duhamel_inner_f1'): [ba2['K_F2_fwd']],
               ('F2', 'duhamel_inner_f2'): [ba2['K_F2_rev']]}
    DYN = {
        'F1': {'family': 'F1', 'tier': DYN_TIER, 'route': 'duhamel_inner_f1', 'source': BA2_GATE_REL,
               'value': qs(2 * ba2['K_F1_fwd']), 'K_gate': qs(ba2['K_F1_fwd']),
               'formula': 'C_dyn = 2 K_F1, K_F1 = 592704 tau^2/(1-338688|tau|) (BA2 forward, faces charged once, inner F1)'},
        'F2': {'family': 'F2', 'tier': DYN_TIER, 'route': 'duhamel_inner_f2', 'source': BA2_GATE_REL,
               'value': qs(2 * ba2['K_F2_rev']), 'K_gate': qs(ba2['K_F2_rev']),
               'formula': "C_dyn = 2 K'_F2, K'_F2 = 345744 tau^2 E_up(592704|tau|) (BA2 reverse, owner-set Phi', inner F2)"},
    }
    Cdyn = {F: parse_q(DYN[F]['value']) for F in ('F1', 'F2')}
    dyn_ok = all(certify_dynamics_constant(DYN[F], options) for F in ('F1', 'F2'))
    check('ba2_gate_dynamics_constants_read_exactly', dyn_ok and formula_prov and formulas_match
          and all(Cdyn[F] <= P['target_C_dyn'] for F in Cdyn),
          ba2_gate_values={k: exact(v) for k, v in sorted(ba2.items())},
          dynamics_constants={F: dict(DYN[F], preview=sci(Cdyn[F]), target=qs(P['target_C_dyn']),
                                      margin=sci(P['target_C_dyn'] / Cdyn[F], 8)) for F in ('F1', 'F2')},
          why_twice='item 5 replaces T^{F,N}_theta(A) by T^{F,r_N}_theta(A) inside omega^{F,N} (BA2 sup over M>r_N, M=N) '
                    'and T_theta(A) by T^{F,r_N}_theta(A) inside omega_inf (BA2 limit bound); each costs K_F/(r_N-1) ||A||^2',
          labelled_alternatives={'F1 via BA2 reverse whole-star (duhamel_inner_f1)': exact(2 * ba2['K_F1_rev']),
                                 'F2 via BA2 forward through F1 (duhamel_inner_f1)': exact(2 * ba2['K_F2_fwd'])},
          formula_provenance='BA2 forward report (K_c1, K_c2) and BA2 reverse report (c1, c2, E_up), re-evaluated exactly at |tau|=10^-8')

    # -------------------------------------------------- premise gates (inheritance, cutoff)
    gates = {}
    for rel in (BA1_GATE_REL, AQ1_GATE_REL, AQ2_GATE_REL, AV1_GATE_REL, AY1_GATE_REL, AM2_GATE_REL):
        gates[rel] = json.loads((INPUTS / rel).read_text())
    admitted_texts = {
        'AQ1': gates[AQ1_GATE_REL]['accepted'], 'AQ2': gates[AQ2_GATE_REL]['accepted'],
        'BA2': ba2_gate['accepted'], 'AY1': gates[AY1_GATE_REL]['accepted'],
    }
    ba1_acc = gates[BA1_GATE_REL]['accepted']
    ba1_ok = (gates[BA1_GATE_REL]['verdict'] == 'accepted_within_scope'
              and 'any two complete-factor volumes of one prescription containing Lambda_N' in ba1_acc
              and 'any two centered boxes of size at least N' in ba1_acc)
    av1_ok = ('The on-site cutoff is removed for the ground vector itself in each fixed box (uniform-gap argument)'
              in gates[AV1_GATE_REL]['accepted'])
    av1f = (INPUTS / AV1F_REL).read_text()
    f20_23 = all('\\tag{HNM-AV1-F' + str(k) + '}' in av1f for k in (20, 21, 22, 23)) and 'Eckart-type vector bound' in av1f
    am2_ok = 'For every nonempty finite I1 complete-factor volume' in gates[AM2_GATE_REL]['accepted'] \
        and 'unique ground and a physical gap at least alpha/16' in gates[AM2_GATE_REL]['accepted']
    check('premise_gates_read', ba1_ok and av1_ok and f20_23 and am2_ok,
          ba1='coefficient input of B5: any two complete-factor volumes of one prescription containing Lambda_N (BA1 gate)',
          av1='cutoff-vector removal F20-F23 (Eckart, untruncated gap 1/2) in each fixed box',
          am2='simple ground and gap alpha/16 for every nonempty finite I1 complete-factor volume (hence translated boxes)')

    # -------------------------------------------------- item 0: union comparison assembly
    def C_prime_fn(C_h, c_h):
        return 1 * C_h

    def c_site_fn(C_h, c_h):
        return 1 * c_h

    union_cases = {}
    for N in (2, 3):
        for M in (N + 1, N + 3):
            union_cases['Lambda_%d,Lambda_%d' % (N, M)] = union_factor(box_sites(N), box_sites(M))
    trans_cases = {}
    for N, v in ((3, (1, 0, 0)), (3, (0, 1, 1)), (4, (2, -1, 0)), (4, (1, 1, 1))):
        V1, V2 = box_sites(N), box_sites(N, v)
        U_ = V1 | V2
        centered = any(U_ == box_sites(m) for m in range(N, N + 4))
        inner_box = box_sites(N - linf(v))
        trans_cases['Lambda_%d vs Lambda_%d+%s' % (N, N, str(v))] = {
            'union_factor': union_factor(V1, V2), 'nested': V1 <= V2 or V2 <= V1, 'union_is_centered_cube': centered,
            'both_contain_Lambda_(N-|v|)': inner_box <= V1 and inner_box <= V2}
    grid = [(Ch, ch), (Ch / 2, ch * 3), (Ch * 7, ch / 5)]
    deltas = [Q(1, 10 ** 9), Q(1, 10 ** 5), Q(3)]
    STATE = {
        'C_prime': {'tier': 'exact_first_order', 'assembly': ASSEMBLY, 'hypothesis_source': HYP_SOURCE,
                    'bb1_route': BB1_ROUTE_NOTE, 'assembly_factor': '1', 'function': "C'(C_h,c_h) = 1*C_h",
                    'value': qs(C_prime_fn(Ch, ch))},
        'c_site_prime': {'tier': 'exact_first_order', 'assembly': ASSEMBLY, 'hypothesis_source': HYP_SOURCE,
                         'bb1_route': BB1_ROUTE_NOTE, 'assembly_factor': '1', 'function': "c'_site(C_h,c_h) = 1*c_h",
                         'value': qs(c_site_fn(Ch, ch))},
    }
    Cp, cs = C_prime_fn(Ch, ch), c_site_fn(Ch, ch)
    assembly_ok = (all(v == 1 for v in union_cases.values())
                   and all(t['union_factor'] == 2 and not t['nested'] and not t['union_is_centered_cube'] and t['both_contain_Lambda_(N-|v|)']
                           for t in trans_cases.values())
                   and certify_monotone(C_prime_fn, grid, deltas) and certify_monotone(c_site_fn, grid, deltas)
                   and all(certify_state_constant(STATE[k]) for k in STATE))
    check('item0_union_comparison_assembly', assembly_ok and Cp <= P['target_C_prime'] and cs <= P['target_c_site'],
          assembly=ASSEMBLY, lemma='for volumes V1,V2 of one prescription containing Lambda_n, U=V1 u V2 contains Lambda_n and '
                                   '||rho^{V1}_Y-rho^{V2}_Y||_1 <= [V1!=U] H(V1,U) + [V2!=U] H(V2,U), H the BB1 hypothesis bound',
          nested_centered_union_factors=union_cases, translated_pairs=trans_cases,
          state_constants={k: dict(STATE[k], preview=sci(parse_q(STATE[k]['value']))) for k in STATE},
          targets={'C_prime': qs(P['target_C_prime']), 'c_site_prime': qs(P['target_c_site'])},
          margins={'C_prime': qs(P['target_C_prime'] / Cp), 'c_site_prime': qs(P['target_c_site'] / cs)},
          monotone='checked exactly at 3 points x 3 increments in each hypothesis constant (linear, coefficients 1 and 0)')

    # -------------------------------------------------- item 1: whole-sequence Cauchy estimates
    regions = {'R': COVER, '{0}': (ORIGIN,), '{e_x,e_y}': ((1, 0, 0), (0, 1, 0)), 'Lambda_1': tuple(sorted(box_sites(1))),
               '{(2,0,0),(2,1,0)}': ((2, 0, 0), (2, 1, 0))}
    region_table = {}
    for name, Y in regions.items():
        mY = max(linf(y) for y in Y)
        row = {}
        for N in (max(2, mY), max(2, mY) + 1, max(2, mY) + 4):
            rec = {'constant': 'c_site_prime', 'size_factor': '|Y| e^{|Y|/10^8}', 'exponent': N - mY}
            must(certify_region_bound(rec, N, Y), 'region record')
            row[str(N)] = {'d_Y': N - mY, 'bound': "c'_site*%d*e^{%d/10^8}*q^%d" % (len(Y), len(Y), N - mY),
                           'upper_value': sci(cs * len(Y) * exp_up(Q(len(Y), 10 ** 8)) * q ** (N - mY), 8)}
        region_table[name] = {'|Y|': len(Y), 'max_|y|_inf': mY, 'rows': row}
    cauchy_rec = {'kind': 'sup_over_all_M_greater_than_N', 'limit_from': 'Cauchy bound and completeness of the trace class'}
    Rrows = {str(N): exact(Cp * q ** (N - 1)) for N in (2, 3, 4, 10)}
    # exact finite audit of the two Banach-space facts used: partial trace is trace-norm contractive and positivity/trace
    # survive trace-norm limits (checked on diagonal two-qubit densities, where the trace norm is the l1 norm)
    joint_pairs = [((Q(1, 2), Q(1, 4), Q(1, 8), Q(1, 8)), (Q(3, 8), Q(3, 8), Q(1, 8), Q(1, 8))),
                   ((Q(9, 10), Q(0), Q(0), Q(1, 10)), (Q(1, 2), Q(1, 2), Q(0), Q(0)))]
    contractive = True
    for a, b in joint_pairs:
        joint = sum(abs(x - y) for x, y in zip(a, b))
        marg = abs((a[0] + a[1]) - (b[0] + b[1])) + abs((a[2] + a[3]) - (b[2] + b[3]))
        contractive = contractive and marg <= joint
    check('item1_whole_sequence_cauchy_R_and_regions',
          certify_cauchy_claim(cauchy_rec) and contractive and all(Q(v['exact']) <= P['target_C_prime'] * q ** (int(N) - 1)
                                                                     for N, v in Rrows.items()),
          statement="for F in {F1,F2}, N>=2: sup_{M>N} ||rho^{F,M}_R-rho^{F,N}_R||_1 <= C' q^(N-1) and, for every finite "
                    "complete-factor Y inside Lambda_N, sup_{M>N} ||rho^{F,M}_Y-rho^{F,N}_Y||_1 <= c'_site |Y| e^{|Y|/10^8} q^{d_Y}, "
                    'd_Y=N-max_Y|y|_inf; each M>N compared directly (B4 same family nested, or B5 nested), never by summing steps',
          C_prime=exact(Cp), c_site_prime=exact(cs), R_rows=Rrows, region_rows=region_table,
          limit='the tail supremum tends to 0, so (rho^{F,N}_Y)_N is Cauchy in the trace class T(H_Y), which is complete; '
                'its limit rho^inf_Y is positive with trace one, partial traces are compatible (||Tr_2 X||_1<=||X||_1), and '
                "||rho^inf_Y-rho^{F,N}_Y||_1 <= c'_site|Y|e^{|Y|/10^8}q^{d_Y} by closedness of the ball; no compactness is used",
          contractivity_audit='diagonal two-qubit pairs: marginal l1 distance <= joint l1 distance (exact)')
    cut = {'order': CUTOFF_ORDER, 'constants_depend_on_L': False, 'vector_removal': True}
    x_psi = (Q(2, 3), Q(2, 3), Q(1, 3))                 # Eckart fixture: H=diag(0,1/2,1), untruncated gap 1/2
    H_diag = (Q(0), Q(1, 2), Q(1))
    E_L = sum(c * c * h for c, h in zip(x_psi, H_diag))
    eckart_ok = 1 - x_psi[0] ** 2 <= (E_L - 0) / Q(1, 2)
    check('item1_cutoff_uniform_then_removed', certify_cutoff(cut) and eckart_ok and av1_ok and f20_23,
          order=CUTOFF_ORDER,
          statement='in each Q_L the hypotheses hold with the same constants, so item 1 holds in each Q_L uniformly in L; at fixed '
                    'N and M, rho^{F,N,L}_Y -> rho^{F,N}_Y in trace norm (AV1 F20-F23; F2 through the AY1 itemization; translated '
                    'boxes through the covariance unitary), so the bound passes to the untruncated vectors; only then N -> infinity',
          eckart_fixture={'H': 'diag(0,1/2,1)', 'psi_L': '(2/3,2/3,1/3)', 'E_L-E_0': qs(E_L), '1-|<psi,psi_L>|^2': qs(1 - x_psi[0] ** 2),
                          'bound_(E_L-E_0)/gap': qs(E_L / Q(1, 2))})

    # -------------------------------------------------- item 2: common limit
    common_const = 2 * cs + ch
    id_rows = {str(N): exact((2 * Cp + Ch) * q ** (N - 1)) for N in (2, 5, 10)}
    check('item2_common_limit_F1_F2', common_const == 2 * cs + ch == Q(3, 500000) and 2 * Cp + Ch == Q(3, 250000)
          and all(q ** (N + 1) < q ** N for N in range(2, 50)),
          identification_bound_on_R_rows=id_rows,
          statement='||rho^{F1,inf}_Y-rho^{F2,inf}_Y||_1 <= ||rho^{F1,inf}_Y-rho^{F1,N}_Y||_1 + ||rho^{F1,N}_Y-rho^{F2,N}_Y||_1 '
                    "+ ||rho^{F2,N}_Y-rho^{F2,inf}_Y||_1 <= (2c'_site + c_h)|Y| e^{|Y|/10^8} q^{d_Y} for every N, hence 0: "
                    'the two whole-sequence limits coincide on every finite region (B3 for the middle term)',
          identification_constant_region=exact(common_const), identification_constant_R=exact(2 * Cp + Ch),
          hypothesis='B3 (F1 versus F2 on the same Lambda_N), R and region forms')

    # -------------------------------------------------- item 3: identification and inheritance
    INHERIT = [
        {'name': 'locally normal gauge-invariant state, stationary under T_theta', 'gate': 'AQ1',
         'gate_text': 'compatible locally normal gauge-invariant stationary state'},
        {'name': 'strongly continuous GNS evolution, nonnegative self-adjoint physical energy generator', 'gate': 'AQ1',
         'gate_text': 'strongly continuous GNS evolution with a nonnegative self-adjoint physical energy generator'},
        {'name': 'physical cyclic restriction reducing', 'gate': 'AQ1', 'gate_text': 'The forward physical cyclic restriction is reducing'},
        {'name': 'gauge-fixed space equals the invariant-local cyclic completion and reduces the generator', 'gate': 'AQ2',
         'gate_text': 'the complete original-endpoint gauge-fixed space equals the invariant-local cyclic completion and reduces the physical energy generator'},
        {'name': 'H_phys >= (alpha/16)(I-P_Omega), simple vacuum on the invariant-local cyclic completion', 'gate': 'AQ2',
         'gate_text': 'Centered Fourier tests including zero give H_phys >= (alpha/16)(I-P_Omega) and a simple vacuum in this representation'},
        {'name': 'full-GNS strengthening only as qualified (uses the AM2 full-Hilbert finite gap)', 'gate': 'AQ2',
         'gate_text': "The full-GNS strengthening explicitly uses AM2's separately reviewed full-Hilbert finite gap"},
        {'name': 'original xz Wilson variance at least 61999/250000 in the same state', 'gate': 'AQ2',
         'gate_text': 'variance >=61999/250000>1/5'},
        {'name': 'F2 limit dynamics equals T_theta; AQ1 sections 4-5 rerun for F2 limit states', 'gate': 'BA2',
         'gate_text': 'AQ1 sections 4-5 are rerun for every subsequential F2 limit state'},
    ]
    ident = {'order': ['whole-sequence limit', 'identified with every AQ1 and every F2 subsequential limit', 'properties inherited'],
             'sequence': 'whole sequence',
             'source': 'every subsequence of a trace-norm convergent sequence has the same limit on each finite region',
             'inherited': INHERIT}
    check('item3_identification_then_inheritance', certify_identification(ident, admitted_texts),
          inherited=[p['name'] + ' [' + p['gate'] + ']' for p in INHERIT],
          representation='the GNS representation (pi_inf, H_inf, Omega_inf) of omega_inf, unitarily equivalent to the AQ1 chosen '
                         'representation because omega_inf equals the AQ1 chosen subsequential state',
          not_inherited=['uniqueness of every infinite-volume ground state', 'states outside the named constructions',
                         'equality of GNS dynamics of different states', 'an unqualified full-GNS gap'])

    # -------------------------------------------------- item 4: coarse translations
    i1_text = (INPUTS / I1_REL).read_text()
    parsed_rows, derived_rows = parse_i1_table(i1_text), derive_i1_table()
    must(parsed_rows == derived_rows and len(derived_rows) == 24, 'I1 table differs from its derivation')
    classes = [r for r in derived_rows if r[4] == 'omitted']
    must(len(classes) == 21, 'omitted classes')
    sel_classes = {(r[0], r[1], r[2]) for r in derived_rows if r[4] == 'selected'}
    window = [(x, y, z) for x in range(8) for y in range(4) for z in range(2)]
    trans_table = {}
    for t in [(tx, ty, tz) for tx in range(8) for ty in range(4) for tz in range(2)]:
        cls_ok = all((fine_class(vadd(p, t), o) in sel_classes) == (fine_class(p, o) in sel_classes)
                     and fine_class(vadd(p, t), o)[1:] == fine_class(p, o)[1:] for p in window for o in ('xy', 'xz', 'yz'))
        shifts = {vsub(tuple(fine_owners(vadd(p, t), o))[0], tuple(fine_owners(p, o))[0]) for p in window for o in ('xy', 'xz', 'yz')}
        pi_ok = len(shifts) == 1
        trans_table[t] = (cls_ok, pi_ok)
    exact_char = all((ok_c and ok_p) == is_coarse_fine_translation(t) for t, (ok_c, ok_p) in trans_table.items())
    witness = {'t': '(1,0,0)', 'face': 'xy at fine (2,0,0), class r=2,s=0 selected',
               'image_class': str(fine_class((3, 0, 0), 'xy')), 'image_selected': fine_class((3, 0, 0), 'xy') in sel_classes}
    cov = {}
    for N, v in ((3, (1, 0, 0)), (3, (0, -1, 1)), (4, (1, 1, 0))):
        base, moved = box_sites(N), box_sites(N, v)
        f1b, f1m = f1_faces(base, classes), f1_faces(moved, classes)
        f2b, f2m = f2_faces(base, classes), f2_faces(moved, classes)
        cov['N=%d,v=%s' % (N, str(v))] = {
            'F1_covariant': translate_faces(f1b, v) == f1m, 'F2_covariant': translate_faces(f2b, v) == f2m,
            'padding_covariant': frozenset(vadd(p, v) for p in padding(base)) == padding(moved),
            'F1_faces': len(f1b), 'F2_faces': len(f2b)}
    cov_ok = all(c['F1_covariant'] and c['F2_covariant'] and c['padding_covariant'] for c in cov.values())
    trows = {}
    for N, v in ((2, (0, 0, 0)), (3, (1, 0, 0)), (4, (1, -1, 0)), (6, (2, 1, 0)), (8, (1, 2, -3)), (10, (3, 0, 0))):
        rec = {'v': v, 'fine': (4 * v[0], 2 * v[1], v[2]), 'N': N, 'item': 'pre-registered item 4',
               'source': 'bb1 general-volume comparison: Lambda_N+v versus Lambda_N, both containing Lambda_(N-|v|_inf)',
               'bound': qs(Ch * q ** (N - linf(v) - 1))}
        must(certify_translation(rec, Ch, q), 'translation record')
        trows['N=%d,v=%s' % (N, str(v))] = dict(exact(Ch * q ** (N - linf(v) - 1)),
                                                union_fallback_labelled=sci(2 * Ch * q ** (N - linf(v) - 1)))
    check('item4_coarse_translation_invariance', exact_char and cov_ok and witness['image_selected'] is False,
          characterization='a fine translation t preserves the selected set, the face classes and the owner map pi (up to a '
                           'constant coarse shift) iff t=(4v_x,2v_y,v_z); checked exhaustively for t in [0,8)x[0,4)x[0,2)',
          coarse_count=sum(1 for t in trans_table if is_coarse_fine_translation(t)), window_translations=len(trans_table),
          non_coarse_witness=witness, face_set_covariance=cov, bound_rows=trows,
          statement='for coarse v and N>=|v|_inf+2: ||rho^{Lambda_N+v}_R-rho^{Lambda_N}_R||_1 <= C_h q^(N-|v|_inf-1) (B5 direct, '
                    'both volumes contain Lambda_(N-|v|_inf)); with the region form, omega_inf(alpha_v(A))=omega_inf(A) for every '
                    'local A; labelled fallback with nested-only B5: 2 C_h q^(N-|v|_inf-1) through the union')

    # -------------------------------------------------- item 5: correlation functions
    def rN(N):
        return (N - 1) // 2
    must(certify_r_N(rN), 'r_N rule')
    geom = all(rN(N) >= 2 and 1 <= rN(N) < N and 2 * (N - rN(N)) >= N + 1 and (2 * rN(N) + 1) ** 3 <= N ** 3
               for N in range(5, 2000))
    e_series_lo, e_series_hi = exp_series(Q(1))
    e_ok = E_LO < e_series_lo and e_series_hi < E_UP

    def region_up(N):
        r = rN(N)
        Y = (2 * r + 1) ** 3
        return cs * Y * exp_up(Q(Y, 10 ** 8)) * q ** (N - r)

    def item5_terms(N, F):
        r = rN(N)
        return {'dynamics': Cdyn[F] / (r - 1), 'region': region_up(N), 'R': 2 * Cp * q ** (N - 1)}

    item5 = {}
    for F in ('F1', 'F2'):
        for N in (5, 6, 10, 20):
            t = item5_terms(N, F)
            total = assemble_linear([t['dynamics'], t['region'], t['R']])
            item5['%s,N=%d' % (F, N)] = {
                'r_N': rN(N), '|Lambda_rN|': (2 * rN(N) + 1) ** 3,
                'C_dyn/(r_N-1)': exact(t['dynamics']),
                "c'_site|Lambda_rN|e^{|Lambda_rN|/10^8}q^(N-r_N) (directed upper)": dict(exact(ceil_to(t['region'])), grid='10^-40'),
                "2C'q^(N-1)": exact(t['R']),
                'sum (directed upper)': dict(exact(ceil_to(total)), grid='10^-40')}
    rec5 = {'r_N': R_N_RULE, 'N_min': 5, 'centering': 'complex_mean', 'window': '|theta|<=8',
            'constants': ['C_dyn', 'c_site_prime', 'C_prime'], 'lumped': False, 'combine': 'linear', 'decay': 'polynomial',
            'uniform_in_time': False, 'gns_dynamics_equality': False}
    check('item5_correlation_bound_three_constants', certify_item5(rec5) and geom and e_ok,
          record=rec5, dynamics_constants={F: exact(Cdyn[F]) for F in Cdyn}, C_prime=exact(Cp), c_site_prime=exact(cs),
          values=item5,
          proof='|c^{F,N}_A-c^inf_A| <= |omega^{F,N}(A*(T^{F,N}-T^{F,r})(A))| + |(omega^{F,N}-omega_inf)(A*T^{F,r}(A))| + '
                '|omega_inf(A*(T^{F,r}-T)(A))| + ||a_N|^2-|a|^2|, r=r_N; the four terms are <= ||A||^2 times K_F/(r-1), '
                "c'_site|Lambda_r|e^{|Lambda_r|/10^8}q^(N-r), K_F/(r-1) and 2C'q^(N-1)",
          e_enclosure={'E_LO': qs(E_LO), 'E_UP': qs(E_UP), 'series_24_terms': [sci(e_series_lo, 15), sci(e_series_hi, 15)]})

    # O(1/N) on the certified range, by blocks, with integer comparisons
    K_reg = cs * 625 * E_UP * Q(1, 8) ** 6            # max over 5<=N<=464 of N*region(N)
    K_R = 10 * Cp * q ** 4                           # max over N>=5 of N*2C'q^(N-1)
    blockA_ok = all((N + 1) ** 4 < 8 * N ** 4 for N in range(5, 465)) and 463 ** 3 < 10 ** 8
    blocks = []
    a = 465
    while a <= RATE_CERTIFIED_MAX:
        b = min(2 * a - 1, RATE_CERTIFIED_MAX)
        while True:
            k = -((-b ** 3) // 10 ** 8)              # ceil(b^3/10^8)
            # c' b^4 E_UP^k 8^-(a+1) <= K_reg  <=>  b^4 27183^k 10000*262144 <= 625*27183*10^(4k) 8^(a+1)
            if b ** 4 * 27183 ** k * 10000 * 262144 <= 625 * 27183 * 10 ** (4 * k) * 8 ** (a + 1):
                break
            b = (a + b) // 2
            must(b >= a, 'block search failed')
        blocks.append((a, b, k))
        a = b + 1
    ratio_dyn_ok = all(N * 1 <= 10 * (rN(N) - 1) for N in range(5, RATE_CERTIFIED_MAX + 1))
    K5 = {F: 10 * Cdyn[F] + K_reg + K_R for F in Cdyn}
    Nv = RATE_VACUOUS_AT
    rv = rN(Nv)
    Yv = (2 * rv + 1) ** 3
    kv = Yv // 10 ** 8
    # c'|Y| E_LO^k q^(N-r) >= 2  <=>  |Y| 2718^k >= 2*500000*1000^k*64^(N-r)
    vacuous = Yv * 2718 ** kv >= 2 * 500000 * 1000 ** kv * 64 ** (Nv - rv)
    rate_claim = {'form': 'O(1/N)', 'range': [5, RATE_CERTIFIED_MAX]}
    check('item5_rate_in_N_certified_range', blockA_ok and ratio_dyn_ok and vacuous
          and certify_rate_claim(rate_claim, RATE_CERTIFIED_MAX, RATE_VACUOUS_AT),
          statement='for 5<=N<=14000 the frozen item-5 bracket is at most K5_F/N with K5_F = 10 C_dyn[F] + K_reg + K_R '
                    '(N/(r_N-1)<=10; N*region(N)<=K_reg by block A (|Lambda_rN|<=10^8, N^4 8^-(N+1) decreasing) and blocks B; '
                    "N*2C'q^(N-1)<=K_R)",
          K5={F: exact(K5[F]) for F in K5}, K_reg=exact(K_reg), K_R=exact(K_R),
          block_A='5<=N<=464', blocks_B=[{'N': [a_, b_], 'ceil_b3_over_1e8': k_} for a_, b_, k_ in blocks],
          vacuous_at={'N': Nv, 'r_N': rv, '|Lambda_rN|': Yv, 'floor(|Y|/10^8)': kv,
                      'statement': "c'_site|Lambda_rN|e^{|Lambda_rN|/10^8}q^(N-r_N) >= 2 exactly (E_LO lower bound), so the "
                                   'frozen bracket exceeds the trivial bound 2 for |c^N-c^inf|/||A||^2'},
          float_previews_labelled={'region term exceeds the dynamics term first at': 14411, 'region term exceeds 1 first at': 14419},
          qualitative='for every fixed r>=2, limsup_N |c^{F,N}_A-c^inf_A| <= ||A||^2 C_dyn/(r-1); r is arbitrary, so the whole '
                      'sequence of correlation functions converges for every theta in the window (no rate; r_N is not re-chosen)')

    # -------------------------------------------------- item 6: tau scaling per constant
    t100 = TAU / 100
    ratios = {
        'C_prime': Q(Ch) / Q(Ch), 'c_site_prime': Q(ch) / Q(ch),
        'C_dyn_F1': (2 * K_F1_formula(TAU)) / (2 * K_F1_formula(t100)),
        'C_dyn_F2': (2 * K_F2_rev_formula(TAU)) / (2 * K_F2_rev_formula(t100)),
        'C_prime_secondary': hyp['C_2h'] / hyp['C_2h'], 'c_site_prime_secondary': hyp['c_2h'] / hyp['c_2h'],
        'q_secondary': (hyp['q2_per_tau'] * TAU) / (hyp['q2_per_tau'] * t100),
    }
    brackets = {'C_prime': P['bracket_state'], 'c_site_prime': P['bracket_state'], 'C_dyn_F1': P['bracket_C_dyn'],
                'C_dyn_F2': P['bracket_C_dyn'], 'C_prime_secondary': P['bracket_secondary'],
                'c_site_prime_secondary': P['bracket_secondary'], 'q_secondary': P['bracket_q2']}
    check('item6_tau_scaling_per_constant', all(certify_scaling(ratios[k], brackets[k]) for k in ratios),
          ratios={k: exact(v) for k, v in ratios.items()}, brackets={k: [qs(x) for x in v] for k, v in brackets.items()},
          item_5_sum='no single bracket; each constant checked separately',
          rule='same exact rational formula at tau and tau/100, no intermediate rounding')

    # -------------------------------------------------- secondary pair (labelled)
    q2 = hyp['q2_per_tau'] * TAU
    Cp2, cs2 = C_prime_fn(hyp['C_2h'], hyp['c_2h']), c_site_fn(hyp['C_2h'], hyp['c_2h'])
    check('secondary_pair_labelled', Cp2 <= P['target_C_prime_2'] and q2 == Q(592, 390625),
          label='secondary (labelled; conditional on the BB1 secondary pair); the headline decides the loop',
          q2=exact(q2), C_prime_2=exact(Cp2), c_site_prime_2=exact(cs2), target_C_prime_2=qs(P['target_C_prime_2']),
          margin=qs(P['target_C_prime_2'] / Cp2))

    # -------------------------------------------------- NS quotation
    quotes = ns_quote_lines(ns_text)
    report_text = REPORT.read_text()
    check('ns_theorem_4_1_quoted_verbatim', certify_quotes(report_text, quotes, NS_REL), quoted_passages=len(quotes),
          source=NS_REL, pdf_sha256=NS_PDF_SHA256,
          use='T^{F,N}_theta is (46) for the native restriction (44); T_theta is the (77) limit, admitted in the BA2 gate for both families')

    return locals()


def fixtures(c):
    """Exact finite fixtures named by the fixture controls (model_is_finite_graph true, transfers_to_aq false)."""
    out = {}
    # (a) one-state ball, two subsequential limits
    P0 = (Q(1, 2), Q(1, 2))
    delta = Q(1, 1000)
    seq = {N: (Q(1, 2) + (-1) ** N * delta, Q(1, 2) - (-1) ** N * delta) for N in range(2, 40)}
    in_ball = all(abs(s[0] - P0[0]) + abs(s[1] - P0[1]) <= 2 * delta for s in seq.values())
    tails = {N: max(abs(seq[M][0] - seq[N][0]) + abs(seq[M][1] - seq[N][1]) for M in range(N + 1, 40)) for N in range(2, 38)}
    out['one_state_ball'] = {'every_term_within_2delta_of_P': in_ball, 'tail_sup': qs(tails[2]), 'limits': ['even', 'odd'],
                             'distance_of_limits': qs(4 * delta)}
    # (b) steps 1/(n+1) -> 0 but no Cauchy property (zigzag harmonic walk on [0,1])
    x, d, xs = Q(0), 1, [Q(0)]
    for n in range(1, 1500):
        x = x + d * Q(1, n + 1)
        if x >= 1:
            d = -1
        elif x <= 0:
            d = 1
        xs.append(x)
    steps_ok = all(abs(xs[n + 1] - xs[n]) <= Q(1, n + 2) for n in range(len(xs) - 1))
    zig_tail = {N: max(xs[N:]) - min(xs[N:]) for N in (10, 100, 400)}
    out['harmonic_zigzag'] = {'step_bound_1/(n+1)': steps_ok, 'tail_oscillation': {str(k): sci(v, 6) for k, v in zig_tail.items()}}
    # (c) correlation centering with a complex mean (exact)
    phi = ((Q(3, 5), Q(0)), (Q(4, 5), Q(0)))
    A = ((C0, CI), (C0, C0))                         # A e_1 = i e_0
    Aphi = mvec(A, phi)
    a = inner(phi, Aphi)                             # 12i/25
    AA = mmul(mdag(A), A)
    omega_AA = inner(phi, mvec(AA, phi))
    shifted = tuple(cadd(Aphi[i], cmul((-a[0], -a[1]), phi[i])) for i in range(2))
    var_vec = sum(cabs2(z) for z in shifted)
    a_sq = cmul(a, a)
    out['centering'] = {'omega(A)': [qs(a[0]), qs(a[1])], '|omega(A)|^2': qs(cabs2(a)), 'omega(A)^2': [qs(a_sq[0]), qs(a_sq[1])],
                        'omega(A*A)': qs(omega_AA[0]), '||(A-a)phi||^2': qs(var_vec)}
    # (d) topology: fixed vector versus moving vector (U(t)e_j=e^{ijt}e_j, A e_j=e_{2j})
    # (U(t)AU(t)*-A)e_j = (e^{ijt}-1)e_{2j}; at t=pi/n on e_n the phase is e^{i pi}=i^2
    moving = all(cadd(ipow(2 * n // n), (Q(-1), Q(0))) == (Q(-2), Q(0)) for n in range(1, 41))
    # on the fixed vector e_1: |e^{i pi/n}-1| <= pi/n < 22/(7n), below 1/10 from n=32 on
    fixed = all((Q(22, 7 * n) < Q(1, 10)) == (n >= 32) for n in range(1, 400))
    out['topology'] = {'moving_vector_norm_2_for_n_le_40': moving, 'fixed_vector_bound': '|e^{i pi/n}-1| <= pi/n < 22/(7n) -> 0',
                       'fixed_ok': fixed}
    # (e) same algebraic dynamics, different states: H=diag(0,1), A=sigma_x, u=pi/2 (e^{iuH}=diag(1,i))
    Uh = ((C1, C0), (C0, CI))
    tauA = mmul(mmul(Uh, PAULI_X), mdag(Uh))
    prod = mmul(PAULI_X, tauA)
    out['algebraic_not_gns'] = {'omega_0(A tau(A))': [qs(prod[0][0][0]), qs(prod[0][0][1])],
                                'omega_1(A tau(A))': [qs(prod[1][1][0]), qs(prod[1][1][1])]}
    # (f) cutoff exchange
    out['cutoff_exchange'] = {'a(N,L)': '1 if L<=N else 0', 'lim_L lim_N': 1, 'lim_N lim_L': 0,
                              'checked': certify_cutoff_exchange(lambda N, L: 1 if L <= N else 0, 30)}
    must(in_ball and tails[2] == 4 * delta and steps_ok and all(v >= Q(1, 2) for v in zig_tail.values())
         and a == (Q(0), Q(12, 25)) and var_vec == Q(256, 625) and omega_AA == (Q(16, 25), Q(0)) and moving and fixed
         and prod[0][0] == CI and prod[1][1] == (Q(0), Q(-1)) and certify_centering(omega_AA, cabs2(a), var_vec),
         'fixture identities')
    return out, {'seq_tails': tails, 'zig_tail': zig_tail, 'var_vec': var_vec, 'omega_AA': omega_AA, 'a': a, 'delta': delta}


def run_controls(c, fx, fxd):
    raw, contract, P, bb1 = c['raw'], c['contract'], c['P'], c['bb1']
    bb1_raw = c['bb1_raw']
    TAU, U, THETA = c['TAU'], c['U'], c['THETA']
    report_text, template, forbidden = c['report_text'], c['template'], c['forbidden']
    files, classes, q, Ch, ch = c['files'], c['classes'], c['q'], c['Ch'], c['ch']
    pre = contract['preregistration']
    DYN, options, STATE = c['DYN'], c['options'], c['STATE']

    def rebound(edit):
        t = tamper(raw, edit)
        return lambda: validate_contract_bytes(t, sha256_bytes(t), bb1)

    def drop_control(d):
        d['controls'].remove('r_N_prefrozen')
        d['preregistration']['controls_required']['ids'].remove('r_N_prefrozen')
        del d['new_control_semantics']['r_N_prefrozen']

    def loosen_target(d):
        h = d['parameters']['rate_constant_pair']['headline']
        h['C_prime_target'] = '1/10000'
        d['preregistration']['target']['value'] = '1/10000, 1/200000 and 1/2000000000'

    def hypothesis_changed(d):
        rp = d['parameters']['rate_constant_pair']
        rp['hypotheses'] = rp['hypotheses'].replace('C_h=1/250000', 'C_h=1/2500000')
        s = d['new_control_semantics']
        s['conditional_on_bb1_targets'] = s['conditional_on_bb1_targets'].replace('C_h=1/250000', 'C_h=1/2500000')

    def drop_premise(d):
        d['shared_premises'].remove('research/round33/skeptic/ba2.md')
    dropped = tamper(raw, drop_premise)
    files_dropped = [f for f in files if f != 'research/round33/skeptic/ba2.md']
    ba2_bytes = (INPUTS / BA2_GATE_REL).read_bytes()
    ns_bytes = (INPUTS / NS_REL).read_bytes()
    bb1_tampered = tamper(bb1_raw, lambda d: d['parameters']['rate_constant_pair']['headline'].__setitem__('C_target', '1/2500000'))
    control('coherent_evidence_tampering', [
        ('isolation_flag_flipped_rehashed', rebound(lambda d: d.__setitem__('reverse_premise_isolation', False))),
        ('control_removed_rehashed', rebound(drop_control)),
        ('gate_field_flipped_rehashed', rebound(lambda d: d['preregistration']['gate_fields_required'].__setitem__('gns_dynamics_equality_claimed', True))),
        ('hash_binding_flag_flipped_rehashed', rebound(lambda d: d['preregistration']['hash_binding'].__setitem__('admitted_gate_sha256_pinned_in_check_py', False))),
        ('C_prime_target_loosened_rehashed', rebound(loosen_target)),
        ('hypothesis_changed_in_both_places_rehashed', rebound(hypothesis_changed)),
        ('r_N_formula_changed_rehashed', rebound(lambda d: d['parameters']['items'].__setitem__('5_correlations', d['parameters']['items']['5_correlations'].replace('r_N=floor((N-1)/2)', 'r_N=N-2')))),
        ('snapshot_removed_with_contract_line', lambda: validate_inventory(files_dropped, json.loads(dropped))),
        ('byte_change_without_rehash', lambda: validate_contract_bytes(raw + b' ', CONTRACT_SHA256, bb1)),
        ('bb1_contract_target_edited', lambda: validate_bb1_bytes(bb1_tampered, BB1_CONTRACT_SHA256)),
        ('ba2_gate_constant_edited', lambda: parse_ba2_gate(ba2_bytes.replace(b'9261/155720800000000', b'9261/1557208000000000', 1))),
        ('ns_excerpt_edited', lambda: certify_pinned(NS_REL, ns_bytes.replace('uniform for t in compact sets'.encode(), 'uniform for all t'.encode(), 1))),
    ])
    control('exact_arithmetic_admission', [
        ('float_constant', lambda: admit_bound(4e-6, P['target_C_prime'])),
        ('bool_value', lambda: parse_q(True)),
        ('nan_string', lambda: parse_q('nan')),
        ('zero_denominator', lambda: parse_q('1/0')),
        ('float_target', lambda: admit_bound(c['Cdyn']['F1'], 5e-10)),
        ('decimal_preview_as_admission', lambda: admit_bound(sci(c['Cdyn']['F1']), P['target_C_dyn'])),
    ], admission='Fraction only; e^x replaced by directed rational enclosures; previews are truncated strings never read')
    flags = c['flags']
    control('no_priority_or_continuum_claim', [
        ('continuum_true', lambda: validate_claim_flags(dict(flags, continuum_claim=True))),
        ('priority_true', lambda: validate_claim_flags(dict(flags, scientific_priority_verified=True))),
        ('weak_coupling_true', lambda: validate_claim_flags(dict(flags, weak_coupling_claim=True))),
        ('ground_state_uniqueness_true', lambda: validate_claim_flags(dict(flags, uniqueness_of_ground_state_claimed=True))),
    ], provenance='historical, occult or governmental material supplies no premise')
    model = c['model_rec']
    control('changed_model_relabelled', [
        ('tau_1e-7', lambda: certify_model(dict(model, tau='1/10000000'), TAU)),
        ('nonzero_triple', lambda: certify_model(dict(model, triple=['1', '0', '0']), TAU)),
        ('su3_group', lambda: certify_model(dict(model, group='SU(3)'), TAU)),
        ('two_dimensional', lambda: certify_model(dict(model, dimension=2), TAU)),
        ('finite_graph', lambda: certify_model(dict(model, finite_graph=True), TAU)),
        ('uniform_model', lambda: certify_model(dict(model, uniform_model=True), TAU)),
        ('l1_state_metric', lambda: certify_model(dict(model, state_metric='l1 on the coarse factor lattice'), TAU)),
        ('exponential_weights', lambda: certify_model(dict(model, dynamics_metric='l1 on the coarse factor lattice, F(r)=e^{-mu r}'), TAU)),
        ('window_64', lambda: certify_model(dict(model, window_theta='64'), TAU)),
        ('literal_vertex_boxes', lambda: certify_model(dict(model, families=[F1_NAME, 'literal vertex boxes']), TAU)),
    ])
    facts = c['facts']
    control('insufficient_verdict_retained', [
        ('missed_C_prime_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', dict(facts, targets_met=False))),
        ('bb1_insufficient_relabelled_limited', lambda: certify_outcome('limited', dict(facts, discharge='bb1_insufficient'))),
        ('partial_discharge_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', dict(facts, discharge='partial'))),
        ('item4_dropped_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', dict(facts, items=dict(facts['items'], item4=False)))),
        ('cauchy_open_relabelled_limited', lambda: certify_outcome('limited', dict(facts, cauchy_closed=False))),
        ('condition_dropped_before_discharge', lambda: certify_outcome('accepted_within_scope', dict(facts, condition=None))),
        ('retuned_tau_to_pass', lambda: certify_model(dict(model, tau='1/1000000000'), TAU)),
    ], hypothetical_missed_example={'C_h': '1/50000', "C'": exact(Q(1, 50000)), 'meets_1/100000': Q(1, 50000) <= P['target_C_prime'],
                                    'rule_outcome': 'limited', 'dominating_term': 'bb1_hypothesis_constants (C_h itself)'})
    lin = (2 * Q(1, 3) * abs(TAU)) / (2 * Q(1, 3) * abs(TAU / 100))
    control('tau_scaling_exponent', [
        ('C_dyn_linear_order', lambda: certify_scaling(lin, P['bracket_C_dyn'])),
        ('C_prime_tau_dependent', lambda: certify_scaling(Q(100), P['bracket_state'])),
        ('C_dyn_cubic_label', lambda: certify_scaling(c['ratios']['C_dyn_F1'] * 100, P['bracket_C_dyn'])),
        ('secondary_with_1_over_1_minus_q2_misread', lambda: certify_scaling(Q(103, 100), P['bracket_secondary'])),
        ('q2_ratio_10', lambda: certify_scaling(Q(10), P['bracket_q2'])),
        ('post_hoc_bracket', lambda: require((Q(10000), Q(10040)) == P['bracket_C_dyn'], 'bracket chosen after evaluation rejected')),
    ], linear_ratio=qs(lin))
    control('wrong_delta_alpha_hbar_clock', [
        ('u_window_labelled_theta', lambda: certify_clock(THETA, THETA, 'theta=alpha t/hbar')),
        ('delta_clock_label', lambda: certify_clock(THETA, U, 'u=delta t/hbar')),
        ('one_eighth_window', lambda: certify_clock(THETA, Q(1, 8), 'theta=alpha t/hbar')),
        ('euclidean_clock', lambda: certify_clock(THETA, U, 's=alpha t_E/hbar')),
    ], conversion='u=delta t/hbar=theta/8 with delta=alpha/8; |theta|<=8 is |u|<=1')
    t5 = c['item5_terms'](5, 'F1')
    control('root_n_misuse', [
        ('item5_terms_in_quadrature', lambda: assemble_linear([t5['dynamics'], t5['region'], t5['R']], combine='rss')),
        ('divide_by_sqrt_N', lambda: divide_by_root(c['Cdyn']['F1'], 5)),
        ('union_legs_rss', lambda: assemble_linear([Ch, Ch], combine='rss')),
    ])
    control('tier_mixing_rejected', [
        ('state_constant_lr_tier', lambda: certify_state_constant(dict(STATE['C_prime'], tier=DYN_TIER))),
        ('dynamics_constant_state_tier', lambda: certify_dynamics_constant(dict(DYN['F1'], tier='exact_first_order'), options)),
        ('bb1_route_claimed', lambda: certify_state_constant(dict(STATE['C_prime'], bb1_route='polymer_kp'))),
        ('assembly_as_route_label', lambda: certify_state_constant(dict(STATE['c_site_prime'], route=ASSEMBLY))),
        ('assembly_missing', lambda: certify_state_constant({k: v for k, v in STATE['C_prime'].items() if k != 'assembly'})),
        ('lumped_item5_bracket', lambda: certify_item5(dict(c['rec5'], constants=['C_total'], lumped=True))),
        ('dynamics_value_not_from_gate', lambda: certify_dynamics_constant(dict(DYN['F2'], value=qs(parse_q(DYN['F2']['value']) * 2)), options)),
        ('f1_constant_with_inner_f2_route', lambda: certify_dynamics_constant(dict(DYN['F1'], route='duhamel_inner_f2'), options)),
        ('dynamics_with_assembly_label', lambda: certify_dynamics_constant(dict(DYN['F1'], assembly=ASSEMBLY), options)),
    ])
    control('reverse_premise_isolation', [
        ('forward_bb2_report_added', lambda: validate_inventory(files + ['research/round33/forward/bb2/report.md'], contract)),
        ('bb1_gate_added', lambda: validate_inventory(files + ['research/round33/advisor/bb1-gate.json'], contract)),
        ('bb1_reverse_producer_added', lambda: validate_inventory(files + ['research/round33/reverse/bb1/report.md'], contract)),
        ('bb1_skeptic_added', lambda: validate_inventory(files + ['research/round33/skeptic/bb1.md'], contract)),
        ('skeptic_triage_added', lambda: validate_inventory(files + ['research/round33/skeptic/triage-bb.md'], contract)),
        ('bb_contract_review_added', lambda: validate_inventory(files + ['research/round33/skeptic/bb-contract-review.md'], contract)),
        ('lens_memo_added', lambda: validate_inventory(files + ['research/round33/experts/jung/memo.md'], contract)),
        ('deliberation_added', lambda: validate_inventory(files + ['research/round33/advisor/deliberation-4.md'], contract)),
        ('premise_removed', lambda: validate_inventory(files[1:], contract)),
    ])
    control('uniform_in_N_not_in_a', [
        ('uniform_in_lattice_spacing', lambda: certify_uniformity('uniform in the lattice spacing a and in N at fixed spacing')),
        ('uniform_in_a', lambda: certify_uniformity('the constant is uniform in a; in N at fixed spacing')),
        ('unqualified_uniformly', lambda: certify_uniformity('the rate holds uniformly in N')),
        ('continuum_reading', lambda: certify_uniformity('in N at fixed spacing, hence a continuum statement')),
    ], accepted_wording=c['uniformity_text'])
    control('placeholder_span_rejected', [
        ('placeholder_gate', lambda: certify_no_placeholder(['selected after <preceding gate>'])),
        ('bar_span', lambda: certify_no_placeholder(['<a|b>'])),
        ('eg_span', lambda: certify_no_placeholder(['<e.g.x>'])),
        ('contract_placeholder_rehashed', rebound(lambda d: d.__setitem__('selected_after', '<BB1 gate>'))),
    ])
    control('negation_aware_phrase_scan', [
        ('affirmative_thermodynamic_limit', lambda: certify_phrasing(report_text + '\nThis is the thermodynamic limit.', forbidden, template)),
        ('affirmative_infinite_volume_ground_state', lambda: certify_phrasing(report_text + '\nWe construct the infinite-volume ground state.', forbidden, template)),
        ('affirmative_unique_limit', lambda: certify_phrasing(report_text + '\nWe obtain the unique limit.', forbidden, template)),
        ('affirmative_boundary_independent', lambda: certify_phrasing(report_text + '\nThe limit is boundary independent.', forbidden, template)),
        ('affirmative_confirms', lambda: certify_phrasing(report_text + '\nThis confirms the gap.', forbidden, template)),
    ], negated_positive_control=certify_phrasing('This is not the thermodynamic limit.', forbidden, template))
    control('parameters_declare_metric_weights_window', [
        ('metric_removed', rebound(lambda d: d['parameters'].pop('metric'))),
        ('weights_removed', rebound(lambda d: d['parameters'].pop('weights'))),
        ('window_removed', rebound(lambda d: d['parameters'].pop('window'))),
        ('clock_removed', rebound(lambda d: d['parameters'].pop('clock'))),
    ], declared={'metric': 'parameters.metric', 'weights': 'parameters.weights', 'window': 'parameters.window',
                 'clock': 'parameters.clock and preregistration.clock', 'N_min': 'parameters.N_min'})
    pair = {'q': qs(q), 'q_per_N': False, 'C_h': qs(Ch), 'c_h': qs(ch)}
    must(certify_rate_pair(pair, P['hyp']['q'], Ch, ch), 'rate pair')
    control('rate_constant_pair_prefrozen', [
        ('q_optimized_per_N', lambda: certify_rate_pair(dict(pair, q_per_N=True), P['hyp']['q'], Ch, ch)),
        ('q_one_over_32', lambda: certify_rate_pair(dict(pair, q='1/32'), P['hyp']['q'], Ch, ch)),
        ('C_h_retuned', lambda: certify_rate_pair(dict(pair, C_h='1/300000'), P['hyp']['q'], Ch, ch)),
        ('c_h_retuned', lambda: certify_rate_pair(dict(pair, c_h='1/400000'), P['hyp']['q'], Ch, ch)),
    ])
    control('decay_rate_in_N_not_a', [
        ('converted_to_fm', lambda: certify_rate_units('decays like 64^-N per coarse step, i.e. per 4a in fm')),
        ('correlation_length', lambda: certify_rate_units('a correlation length of 1/ln 64 per coarse step')),
        ('rate_in_lattice_spacing', lambda: certify_rate_units('a rate in the lattice spacing per coarse step')),
        ('no_coarse_step', lambda: certify_rate_units('decays like 64^-N')),
    ], accepted=c['rate_units_text'])
    topo = c['topo']
    control('topology_named', [
        ('norm_continuity_in_theta', lambda: certify_topology(dict(topo, representations='norm continuity in theta on B(H_R)'))),
        ('weak_star_states', lambda: certify_topology(dict(topo, states='weak-* on finite-rank observables'))),
        ('one_topology', lambda: certify_topology(dict(topo, states=DYNAMICS_TOPOLOGY))),
    ], fixed_versus_moving_vector=fx['topology'], topologies=topo)
    f1set, f2set = set(c['f1_2']), set(c['f2_2'])
    control('two_families_named', [
        ('single_family', lambda: certify_families([F1_NAME])),
        ('all_boundary_conditions', lambda: certify_families(['all boundary conditions'])),
        ('f2_collapsed_onto_f1', lambda: certify_family_faces(f1set, f1set)),
    ], faces_N2={'F1': len(f1set), 'F2': len(f2set)})
    control('subsequence_versus_whole_sequence', [
        ('states_whole_sequence_from_compactness', lambda: certify_limit_statement({'quantifier': 'whole sequence', 'from': 'compactness'})),
        ('unquantified_limit', lambda: certify_limit_statement({'quantifier': None})),
        ('whole_sequence_from_diagonal_extraction', lambda: certify_limit_statement({'quantifier': 'whole sequence', 'from': 'diagonal extraction'})),
    ], statements={'BB2 states': 'whole sequence (Cauchy bound)', 'AQ1/AY1 states': 'subsequence (compactness), identified in item 3'})
    control('common_clock', [
        ('plus_versus_minus_tau', lambda: certify_same_coupling(TAU, -TAU)),
        ('tau_versus_half_tau', lambda: certify_same_coupling(TAU, TAU / 2)),
        ('f2_on_u_clock', lambda: certify_same_coupling(TAU, TAU, 'theta=alpha t/hbar', 'u=delta t/hbar')),
    ], reason='every comparison and both families at the same coupling and the common clock theta=alpha t/hbar')
    control('named_construction_not_uniqueness', [
        ('the_infinite_volume_ground_state', lambda: certify_phrasing('The limit is the infinite-volume ground state.', forbidden, template)),
        ('uniqueness_phrase', lambda: certify_phrasing('This gives uniqueness of the infinite-volume ground state.', forbidden, template)),
        ('thermodynamic_limit_phrase', lambda: certify_phrasing('We call omega_inf the thermodynamic limit.', forbidden, template)),
        ('uniqueness_flag', lambda: validate_claim_flags(dict(flags, uniqueness_of_ground_state_claimed=True))),
    ], wording='the limit of the named constructions (F1 and F2)')
    tails = fxd['seq_tails']
    control('cauchy_estimate_not_compactness', [
        ('compactness_plus_closeness', lambda: certify_cauchy_claim(dict(c['cauchy_rec'], limit_from='compactness plus the one-state ball'))),
        ('n_to_n_plus_1_only', lambda: certify_cauchy_claim(dict(c['cauchy_rec'], kind='N_to_N_plus_1'))),
        ('one_state_ball_sequence_as_cauchy', lambda: certify_whole_sequence(tails, lambda N: 2 * fxd['delta'] * Q(1, N))),
    ])
    ident, admitted = c['ident'], c['admitted_texts']
    control('limit_identified_with_aq1_limits', [
        ('inherit_before_identification', lambda: certify_identification(dict(ident, order=['whole-sequence limit', 'properties inherited', 'identified with every AQ1 and every F2 subsequential limit']), admitted)),
        ('identification_along_subsequence', lambda: certify_identification(dict(ident, sequence='subsequence'), admitted)),
        ('inherit_uniqueness', lambda: certify_identification(dict(ident, inherited=ident['inherited'] + [{'name': 'uniqueness of every infinite-volume ground state', 'gate': 'AQ2', 'gate_text': 'uniqueness of every infinite-volume ground state'}]), admitted)),
        ('inherit_unqualified_full_gns_gap', lambda: certify_identification(dict(ident, inherited=ident['inherited'] + [{'name': 'full-GNS gap', 'gate': 'AQ2', 'gate_text': 'H >= (alpha/16)(I-P_Omega) on the full GNS space without qualification'}]), admitted)),
        ('inherit_translation_invariance_from_aq1', lambda: certify_identification(dict(ident, inherited=ident['inherited'] + [{'name': 'translation invariance', 'gate': 'AQ1', 'gate_text': 'translation invariant state'}]), admitted)),
    ])
    trec = {'v': (1, 0, 0), 'fine': (4, 0, 0), 'N': 3, 'item': 'pre-registered item 4',
            'source': 'bb1 general-volume comparison: Lambda_N+v versus Lambda_N, both containing Lambda_(N-|v|_inf)',
            'bound': qs(Ch * q ** 1)}
    must(certify_translation(trec, Ch, q), 'translation record')
    control('translation_invariance_separate_item', [
        ('from_nested_cubes', lambda: certify_translation(dict(trec, source='nested centered cubes'), Ch, q)),
        ('not_separate_item', lambda: certify_translation(dict(trec, item='corollary of item 1'), Ch, q)),
        ('N_too_small', lambda: certify_translation(dict(trec, N=2, bound=qs(Ch)), Ch, q)),
        ('union_factor_hidden', lambda: certify_translation(dict(trec, bound=qs(Ch * q ** 2)), Ch, q)),
    ])
    Yl1 = tuple(sorted(box_sites(1)))
    rgood = {'constant': 'c_site_prime', 'size_factor': '|Y| e^{|Y|/10^8}', 'exponent': 3 - 1}
    control('region_constant_scales_with_Y', [
        ('R_constant_reused_on_Y', lambda: certify_region_bound(dict(rgood, constant='C_prime'), 3, Yl1)),
        ('size_factor_dropped', lambda: certify_region_bound(dict(rgood, size_factor='1'), 3, Yl1)),
        ('exponent_N_minus_1_for_all_Y', lambda: certify_region_bound(dict(rgood, exponent=3), 4, ((2, 0, 0),))),
        ('e_factor_dropped', lambda: certify_region_bound(dict(rgood, size_factor='|Y|'), 3, Yl1)),
    ])
    control('cutoff_uniform_then_removed', [
        ('limits_exchanged', lambda: certify_cutoff(dict(c['cut'], order=list(reversed(CUTOFF_ORDER))))),
        ('L_dependent_constant', lambda: certify_cutoff(dict(c['cut'], constants_depend_on_L=True))),
        ('eigenvalue_only_removal', lambda: certify_cutoff(dict(c['cut'], vector_removal=False))),
    ], exchange_fixture=fx['cutoff_exchange'])
    dl = c['dl']
    control('algebraic_not_gns_dynamics', [
        ('gns_equality_finite_versus_limit', lambda: certify_dynamics_level(dict(dl, gns_equality_of_different_states=True))),
        ('correlations_equal_F1_F2_boxes', lambda: certify_dynamics_level(dict(dl, correlations_of_different_states_equal=True))),
        ('algebraic_level_relabelled', lambda: certify_dynamics_level(dict(dl, level='gns_dynamics'))),
    ], fixture=fx['algebraic_not_gns'])
    control('lieb_robinson_polynomial_tail', [
        ('exponential_rate_item5', lambda: certify_item5(dict(c['rec5'], decay='exponential'))),
        ('O_one_over_N_for_all_N', lambda: certify_rate_claim({'form': 'O(1/N)', 'range': [5, 10 ** 9]}, RATE_CERTIFIED_MAX, RATE_VACUOUS_AT)),
        ('exponential_form', lambda: certify_rate_claim({'form': 'O(q^N)', 'range': [5, 100]}, RATE_CERTIFIED_MAX, RATE_VACUOUS_AT)),
        ('unstated_range', lambda: certify_rate_claim({'form': 'O(1/N)', 'range': None}, RATE_CERTIFIED_MAX, RATE_VACUOUS_AT)),
    ], vacuous_witness_N=RATE_VACUOUS_AT)
    win = {'uniform_in_time': False, 'window': '|theta|<=8', 'U': '1'}
    must(certify_window(win), 'window record')
    control('time_window_named_common_clock', [
        ('uniform_in_time', lambda: certify_window(dict(win, uniform_in_time=True))),
        ('window_unnamed', lambda: certify_window(dict(win, window=None))),
        ('U_equals_Theta', lambda: certify_window(dict(win, U='8'))),
    ])
    zig = fxd['zig_tail']
    control('fixture_whole_sequence_vs_subsequence', [
        ('alternating_one_state_ball_as_convergent', lambda: certify_whole_sequence(tails, lambda N: 2 * fxd['delta'])),
        ('harmonic_steps_as_cauchy', lambda: certify_cauchy_claim({'kind': 'N_to_N_plus_1', 'limit_from': 'Cauchy bound and completeness of the trace class'})),
        ('harmonic_tail_as_small', lambda: certify_whole_sequence({N: v for N, v in zig.items()}, lambda N: Q(1, N))),
    ], fixture={'one_state_ball': fx['one_state_ball'], 'harmonic_zigzag': fx['harmonic_zigzag']},
        model_is_finite_graph=True, transfers_to_aq=False)
    control('fixture_translation_residues', [
        ('fine_x_by_1', lambda: certify_fine_symmetry((1, 0, 0), c['trans_table'][(1, 0, 0)][0] and c['trans_table'][(1, 0, 0)][1])),
        ('fine_y_by_1', lambda: certify_fine_symmetry((0, 1, 0), c['trans_table'][(0, 1, 0)][0] and c['trans_table'][(0, 1, 0)][1])),
        ('fine_x_by_2', lambda: certify_fine_symmetry((2, 0, 0), c['trans_table'][(2, 0, 0)][0] and c['trans_table'][(2, 0, 0)][1])),
        ('non_coarse_record', lambda: certify_translation(dict(trec, fine=(1, 0, 0)), Ch, q)),
        ('translated_box_through_nested_cubes', lambda: certify_translation(dict(trec, source='nested centered cubes'), Ch, q)),
    ], witness=c['witness'], model_is_finite_graph=True, transfers_to_aq=False)
    va = fxd['var_vec']
    control('fixture_correlation_centering', [
        ('real_square_centering', lambda: certify_centering(fxd['omega_AA'], cmul(fxd['a'], fxd['a'])[0], va)),
        ('uncentred', lambda: certify_centering(fxd['omega_AA'], Q(0), va)),
        ('post_hoc_r_N', lambda: certify_r_N(lambda N: (N - 1) // 2, label='post_hoc')),
        ('exponential_tail_polynomial_F', lambda: certify_item5(dict(c['rec5'], decay='exponential'))),
    ], fixture=fx['centering'], model_is_finite_graph=True, transfers_to_aq=False)
    hrec = c['hyp_rec']
    control('conditional_on_bb1_targets', [
        ('bb1_value_other_than_target', lambda: certify_hypothesis_record(dict(hrec, C_h='1/300000'), bb1)),
        ('condition_dropped', lambda: certify_hypothesis_record(dict(hrec, label=None), bb1)),
        ('unconditional_before_discharge', lambda: certify_hypothesis_record(dict(hrec, unconditional=True), bb1)),
        ('producer_records_discharge', lambda: certify_hypothesis_record(dict(hrec, discharged=True, bb1_gate_sha256='0' * 64), bb1)),
        ('decreasing_constant', lambda: certify_monotone(lambda C_h, c_h: 3 * C_h - c_h, c['grid'], c['deltas'])),
        ('gate_fields_true_before_discharge', lambda: validate_gate_fields(pre['gate_fields_required'], pre['gate_fields_required'], False)),
    ])
    control('r_N_prefrozen', [
        ('r_N_N_minus_2', lambda: certify_r_N(lambda N: N - 2)),
        ('r_N_floor_N_over_2', lambda: certify_r_N(lambda N: N // 2)),
        ('r_N_optimized', lambda: certify_r_N(lambda N: min(N - 2, 231))),
        ('record_with_other_r_N', lambda: certify_item5(dict(c['rec5'], r_N='floor(N/3)'))),
    ])


def compute():
    c = positive_checks()
    contract, P = c['contract'], c['P']
    pre = contract['preregistration']
    TAU = c['TAU']
    flags = {'continuum_claim': False, 'uniqueness_of_ground_state_claimed': False, 'gns_dynamics_equality_claimed': False,
             'uniform_in_time_claimed': False, 'rate_in_a_claimed': False, 'scientific_priority_verified': False,
             'weak_coupling_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False}
    must(validate_claim_flags(flags), 'claim flags')
    model_rec = {'model_id': 'AQ_patterned_zero_selected', 'tau': qs(TAU), 'triple': ['0', '0', '0'], 'group': 'SU(2)',
                 'dimension': 3, 'families': [F1_NAME, F2_NAME],
                 'state_metric': 'coarse l-infinity on factor sites (star diameter 1)',
                 'dynamics_metric': 'l1 on the coarse factor lattice, F(r)=(1+r)^-4', 'window_theta': '8',
                 'finite_graph': False, 'uniform_model': False}
    uniformity_text = 'every constant is uniform in N at fixed spacing and fixed tau and uniform in the on-site cutoff L; nothing is uniform in the spacing'
    rate_units_text = 'q^(N-1) with q=1/64 per coarse step at fixed spacing and strong bare coupling; a coarse step is (4a,2a,a)'
    topo = {'states': STATES_TOPOLOGY, 'dynamics': DYNAMICS_TOPOLOGY, 'representations': GNS_TOPOLOGY}
    dl = {'level': 'correlation_functions_compact_window', 'gns_equality_of_different_states': False,
          'correlations_of_different_states_equal': False}
    must(certify_model(model_rec, TAU) and certify_rate_units(rate_units_text) and certify_uniformity(uniformity_text)
         and certify_topology(topo) and certify_dynamics_level(dl) and certify_families(model_rec['families'])
         and certify_limit_statement({'quantifier': 'whole sequence', 'from': 'Cauchy bound'})
         and certify_limit_statement({'quantifier': 'subsequence'}) and certify_same_coupling(TAU, TAU), 'claim records')
    f1_2, f2_2 = f1_faces(box_sites(2), c['classes']), f2_faces(box_sites(2), c['classes'])
    must(certify_family_faces(set(f1_2), set(f2_2)) and len(f2_2) - len(f1_2) == 28 * 2 * 11, 'families differ by 28N(5N+1)')
    items = {'item1': True, 'item2': True, 'item3': True, 'item4': True, 'item5': True}
    targets_met = (c['Cp'] <= P['target_C_prime'] and c['cs'] <= P['target_c_site']
                   and all(c['Cdyn'][F] <= P['target_C_dyn'] for F in c['Cdyn']))
    facts = {'cauchy_closed': True, 'discharge': 'pending', 'items': items, 'targets_met': targets_met, 'condition': CONDITION}
    outcome = 'accepted_within_scope'
    must(certify_outcome(outcome, facts), 'outcome rule')
    req = pre['gate_fields_required']
    gate_undischarged = dict(req)
    for k in BB1_DEPENDENT:
        gate_undischarged[k] = False
    gate_undischarged['dynamics_level'] = 'algebraic_heisenberg_compact_window'
    gate_after = dict(req)
    must(validate_gate_fields(gate_undischarged, req, False) and validate_gate_fields(gate_after, req, True), 'gate fields')
    c.update(flags=flags, model_rec=model_rec, uniformity_text=uniformity_text, rate_units_text=rate_units_text, topo=topo,
             dl=dl, facts=facts, f1_2=f1_2, f2_2=f2_2)
    fx, fxd = fixtures(c)
    check('fixtures_exact', True, fixtures=fx, model_is_finite_graph=True, transfers_to_aq=False)
    check('gate_fields_undischarged_and_after_discharge', True, gate_fields_undischarged=gate_undischarged,
          gate_fields_after_discharge=gate_after,
          rule='gate_fields_rule: the contract values hold for accepted_within_scope after the discharge; before it every '
               'BB1-dependent field stays false and dynamics_level stays at the BA2 algebraic level')
    run_controls(c, fx, fxd)

    # ------------------------------------------------ report-level checks
    report_text, template, forbidden = c['report_text'], c['template'], c['forbidden']
    exported_texts = [template, uniformity_text, rate_units_text]
    check('mandatory_template_once', certify_template_span(report_text, template), template_sha256=sha256_bytes(template.encode()))
    check('report_phrase_scan_negation_aware', certify_phrasing(report_text, forbidden, template)
          and all(certify_phrasing(t, forbidden, template) for t in exported_texts), scanned=['report.md', 'exported sentences'],
          forbidden_count=len(forbidden))
    ex_ok = all(e in report_text for e in contract['claim_exclusions']) and all(e in report_text for e in pre['claim_exclusions'])
    const_ok = all(qs(v) in report_text for v in (c['Cp'], c['cs'], c['Cdyn']['F1'], c['Cdyn']['F2'], c['K5']['F1'], c['K5']['F2']))
    disclosure = ('Claude' in report_text and 'AI' in report_text and '/tmp/claude-0/bb2-reverse-private/' in report_text
                  and 'HNM-BB2-R' in report_text and CONDITION in report_text and ASSEMBLY in report_text
                  and 'Hruday N M (BUNZEEY)' in report_text)
    check('report_binds_constants_exclusions_disclosure', ex_ok and const_ok and disclosure,
          exclusions_verbatim=ex_ok, headline_rationals_in_report=const_ok)
    ledger = {
        'bb1_hypothesis_constants': {'value': 'C_h=1/250000 (R form), c_h=1/500000 (region form) at q=1/64; secondary C_2h=1/20000, '
                                              'c_2h=1/40000 at q_2=151552|tau| (labelled)', 'label': CONDITION},
        'cauchy_telescoping_or_union': {'value': "union comparison, factor 1 for nested centered cubes (the union is the larger cube): "
                                                 "C'=C_h, c'_site=c_h; no telescoping sum; non-nested pairs cost factor 2 (labelled)"},
        'identification_with_subsequential_limits': {'value': '0', 'reason': 'exact: a trace-norm convergent sequence has every '
                                                                             'subsequence converging to the same limit; no constant enters'},
        'translation_general_volume': {'value': 'C_h q^(N-|v|_inf-1) on R, c_h|Y|e^{|Y|/10^8}q^(N-|v|_inf-max_Y|y|_inf) on Y (B5 direct); '
                                                'labelled union fallback 2C_h q^(N-|v|_inf-1)'},
        'dynamics_constant_from_ba2': {'value': 'C_dyn[F1]=' + qs(c['Cdyn']['F1']) + ' (duhamel_inner_f1), C_dyn[F2]=' + qs(c['Cdyn']['F2'])
                                                + ' (duhamel_inner_f2): twice the exact BA2 gate values', 'tier': DYN_TIER},
        'region_form_on_Lambda_rN': {'value': "c'_site |Lambda_rN| e^{|Lambda_rN|/10^8} q^(N-r_N); O(1/N) of the bracket certified "
                                              'on 5<=N<=14000; vacuous at N=14421'},
        'arithmetic': {'value': '0', 'reason': 'exact Fractions; e^x replaced by directed enclosures (E_UP=27183/10000, E_LO=2718/1000, '
                                               'series with tail bound); decimals are truncated previews; block comparisons in integers'},
    }
    check('error_ledger_itemized', certify_error_ledger(ledger, pre['error_terms_itemized']), ledger=ledger)

    ids = [x['id'] for x in CHECKS]
    missing = [x for x in contract['controls'] if x not in ids]
    must(missing == [], 'contract controls without a check: ' + ','.join(missing))
    must(sorted(MUTATION_CONTROLS) == sorted(contract['controls']), 'every contract control carries damaging mutations')
    n_mut = sum(len(x.get('rejected_mutations', {})) for x in CHECKS)

    Cp, cs, Cdyn, K5 = c['Cp'], c['cs'], c['Cdyn'], c['K5']
    headline = {
        'C_prime': dict(exact(Cp), function="C'(C_h,c_h)=C_h", target=qs(P['target_C_prime']), margin=qs(P['target_C_prime'] / Cp),
                        tier='exact_first_order', assembly=ASSEMBLY, hypothesis_source=HYP_SOURCE, bb1_route=BB1_ROUTE_NOTE,
                        bound="sup_{M>N} ||rho^{F,M}_R-rho^{F,N}_R||_1 <= C' q^(N-1), q=1/64, N>=2, F in {F1,F2}"),
        'c_site_prime': dict(exact(cs), function="c'_site(C_h,c_h)=c_h", target=qs(P['target_c_site']), margin=qs(P['target_c_site'] / cs),
                             tier='exact_first_order', assembly=ASSEMBLY, hypothesis_source=HYP_SOURCE, bb1_route=BB1_ROUTE_NOTE,
                             bound="sup_{M>N} ||rho^{F,M}_Y-rho^{F,N}_Y||_1 <= c'_site |Y| e^{|Y|/10^8} q^{d_Y}"),
        'C_dyn': {F: dict(exact(Cdyn[F]), tier=DYN_TIER, route=c['DYN'][F]['route'], target=qs(P['target_C_dyn']),
                          margin=sci(P['target_C_dyn'] / Cdyn[F], 8), source=BA2_GATE_REL, formula=c['DYN'][F]['formula'],
                          tau_over_100_ratio=exact(c['ratios']['C_dyn_' + F])) for F in ('F1', 'F2')},
        'item4_bound': "||rho^{Lambda_N+v}_R-rho^{Lambda_N}_R||_1 <= C_h q^(N-|v|_inf-1) = (1/250000) 64^-(N-|v|_inf-1), "
                       'N>=|v|_inf+2, v coarse (fine (4v_x,2v_y,v_z))',
        'item4_rows': c['trows'],
        'item5_values': c['item5'],
        'item5_K5_certified_5_to_14000': {F: exact(K5[F]) for F in K5},
        'item5_vacuous_at': RATE_VACUOUS_AT,
        'secondary_labelled': {'q2': exact(c['q2']), 'C_prime_2': exact(c['Cp2']), 'c_site_prime_2': exact(c['cs2']),
                               'target_C_prime_2': qs(P['target_C_prime_2'])},
    }
    hypotheses_used = {
        'item1': {'comparisons': ['B4 restricted to same-family nested pairs (Lambda_N inside Lambda_M, M>N)',
                                  'equivalently B5 for nested one-prescription pairs'],
                  'forms': ['R (C_h)', 'region (c_h)'], 'cutoff_regimes': ['each Q_L uniformly in L', 'untruncated at fixed N'],
                  'signs': ['+tau', '-tau']},
        'item2': {'comparisons': ['B3 (F1 versus F2 on the same Lambda_N)', 'plus item 1'], 'forms': ['R (C_h)', 'region (c_h)'],
                  'cutoff_regimes': ['untruncated at fixed N', 'each Q_L for the cutoff-space version'], 'signs': ['+tau', '-tau']},
        'item3': {'comparisons': ['through items 1-2 (B3, B4/B5 nested)'],
                  'forms': ['R form for R-marginals', 'region form for every finite region'],
                  'cutoff_regimes': ['untruncated at fixed N'], 'signs': ['+tau', '-tau']},
        'item4': {'comparisons': ['B5 for the non-nested pair (Lambda_N+v, Lambda_N), both containing Lambda_(N-|v|_inf)',
                                  'labelled fallback: B5 nested-only through the union (factor 2)'],
                  'forms': ['R (C_h) for the quantitative bound', 'region (c_h) for invariance on every finite region'],
                  'cutoff_regimes': ['untruncated at fixed N', 'each Q_L'], 'signs': ['+tau', '-tau']},
        'item5': {'comparisons': ['through item 1 (B4/B5 nested)'],
                  'forms': ["R form (C')", "region form at Y=Lambda_{r_N} (c'_site)"],
                  'cutoff_regimes': ['untruncated at fixed N'], 'signs': ['+tau', '-tau'],
                  'admitted_not_hypotheses': 'BA2 gate K_F1 (duhamel_inner_f1), K\'_F2 (duhamel_inner_f2) and the identification of the F2 limit dynamics'},
        'secondary': {'comparisons': ['as items 1-2'], 'forms': ['R (C_2h)', 'region (c_2h)'], 'label': 'labelled only'},
    }
    result = {
        'loop': 'BB2', 'direction': 'reverse', 'assembly': ASSEMBLY,
        'human_author': contract['human_author'],
        'ai_assistance': 'AI-assisted reverse production (Claude, an AI model); correlated model-agent work, not human review',
        'contribution_alias': 'HNM-BB2-R reverse union-comparison whole-sequence convergence, common limit, identification, '
                              'coarse translation invariance and correlation functions of the named constructions (conditional on the BB1 frozen targets)',
        'attribution': {'limit_dynamics': 'Nachtergaele-Sims arXiv:1410.8174v1 Theorem 4.1 (77), quoted verbatim; admitted for F1 and F2 in the BA2 gate',
                        'gns_strategy': 'AQ1 sections 4-5 and AQ2 (Gauvin arXiv:2503.15539v3 Supplement A.10 as the prior strategy)',
                        'banach_space_facts': 'completeness of the trace class and trace-norm contractivity of the partial trace (standard)',
                        'scientific_priority': 'unverified'},
        'contract_sha256': c['contract_sha'], 'bb1_contract_sha256': c['bb1_sha'],
        'check_py_sha256_recorded_before_evaluation': c['check_py_sha'],
        'pinned_premise_sha256': c['pinned'],
        'model': contract['model'],
        'families': {'F1': F1_NAME, 'F2': F2_NAME},
        'label': 'convergence_of_named_constructions', 'secondary_sub_labels': ['common_limit_of_named_constructions'],
        'condition': CONDITION,
        'hypotheses': c['hyp_rec'],
        'hypotheses_used': hypotheses_used,
        'bb1_comparisons': {'B' + str(i + 1): s for i, s in enumerate(c['bb1']['comparisons'])},
        'headline': headline,
        'topologies': c['topo'],
        'cutoff_order': CUTOFF_ORDER,
        'mandatory_sentence_template': c['template'],
        'gate_fields': gate_undischarged,
        'gate_fields_after_discharge': gate_after,
        'gate_fields_note': 'top-level gate fields are the values before the BB1 discharge (gate_fields_rule); gate_fields_after_discharge '
                            'are the contract values that hold for accepted_within_scope once the BB1 gate admits every hypothesis used',
        'error_ledger': ledger,
        'scaling': {k: exact(v) for k, v in c['ratios'].items()},
        'exclusions': {'contract': contract['claim_exclusions'], 'preregistration': pre['claim_exclusions']},
        'routes_executed': [
            'hypotheses: BB1 frozen targets read from both contracts and cross-checked; BA2 gate constants read exactly and re-derived from the BA2 formulas',
            'item 0: union comparison lemma; factor 1 for nested centered cubes, 2 for translated pairs (enumerated); monotone constants',
            'item 1: whole-sequence Cauchy estimate over all M>N on R and on regions Y; limit from completeness of the trace class; cutoff order',
            'item 2: common limit through B3',
            'item 3: identification with every AQ1 and F2 subsequential limit, then inheritance of exactly the gate-admitted properties',
            'item 4: coarse translation covariance (I1 table, face sets, padding), B5 direct bound, non-coarse translations rejected',
            'item 5: C_dyn per family from the BA2 gate, three separate constants, r_N frozen, O(1/N) certified on 5<=N<=14000, vacuous at N=14421',
            'item 6: tau/100 scaling per constant; six fixtures; 34 controls as damaging mutations'],
        'contract_controls_covered': list(contract['controls']),
        'controls_with_damaging_mutations': sorted(MUTATION_CONTROLS),
        'controls_not_implementable_as_mutations': [],
        'damaging_mutations_rejected': n_mut,
        'proposed_reverse_verdict': outcome,
        'proposed_reverse_verdict_condition': CONDITION + ': unconditional only after the BB1 gate admits, for every comparison '
                                              '(B3, B4/B5 nested, B5 general), form (R, region), cutoff regime and sign used, constants at '
                                              'most the hypothesis values; partial discharge gives limited, BB1 insufficient gives insufficient',
        'verdict_by_discharge': {'full': 'accepted_within_scope', 'B5_general_not_admitted': 'limited (item 4 quantitative bound dropped; '
                                 'the union fallback 2C_h needs B5 nested)', 'region_form_not_admitted': 'limited (item 5 and the region parts '
                                 'of items 1-3 dropped; items 1-2 on R, item 3 for R-marginals)', 'bb1_insufficient': 'insufficient'},
        'outcome_note': 'proposed for the reverse half only; acceptance needs both routes, the BB1 discharge and the skeptical review',
        'limitations_recorded': [
            'item 5: the frozen bracket is O(1/N) only on 5<=N<=14000 (certified); at N=14421 its region term alone exceeds 2 because '
            '|Lambda_{r_N}| grows like N^3 inside e^{|Lambda_{r_N}|/10^8}; the whole sequence of correlation functions still converges (no rate)',
            'all BB2 conclusions are conditional_on_bb1_targets until the BB1 gate discharges them',
            'item 4 at the contract constant needs the direct non-nested B5 comparison; the union route alone gives 2C_h',
        ],
        'uniformity': uniformity_text, 'rate_units': rate_units_text,
        'checks': CHECKS,
    }
    result.update(flags)
    result.update(gate_undischarged)
    return result


def main():
    ap = argparse.ArgumentParser(description='HNM-BB2 reverse producer checker (exact arithmetic)')
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
    manifest = {'loop': 'BB2', 'direction': 'reverse', 'contract_sha256': CONTRACT_SHA256, 'bb1_contract_sha256': BB1_CONTRACT_SHA256,
                'sources': sources, 'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    h = result['headline']
    print(json.dumps({'loop': 'BB2', 'direction': 'reverse', 'checks': len(result['checks']),
                      'damaging_mutations': result['damaging_mutations_rejected'],
                      'C_prime': h['C_prime']['exact'], 'c_site_prime': h['c_site_prime']['exact'],
                      'C_dyn_F1': h['C_dyn']['F1']['preview'], 'C_dyn_F2': h['C_dyn']['F2']['preview'],
                      'outcome': result['proposed_reverse_verdict']}, sort_keys=True))


if __name__ == '__main__':
    main()
