#!/usr/bin/env python3
"""HNM-BA2 reverse producer: boundary comparison of the Heisenberg dynamics of the two
named construction families F1 (AQ1 centered whole-star boxes) and F2 (I1 section 6
all-contained-face boxes with padding) on compact windows, by the reverse route:
Duhamel with the inner F2 evolution bounded by the owner-set Nachtergaele-Sims
constants (||Phi'||_F<=1323|tau|), each family's within-family Cauchy estimate against
its own Nachtergaele-Sims limit, identification of the F2 limit dynamics with the AQ1
limit T_theta, and the AQ1 sections 4-5 rerun for F2 limit states.

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production (Claude,
an AI model) under reverse premise isolation; HNM labels are project aliases. The
Lieb-Robinson bound and the dynamics theorem are Nachtergaele-Sims arXiv:1410.8174v1
(Theorem 3.1, Theorem 4.1); Duhamel formulas are standard; the compactness/GNS/Fourier
strategy is credited to Gauvin arXiv:2503.15539v3 A.10 as in AQ1. Scientific priority
is unverified.

Standard library only. Exact Fraction arithmetic decides every Boolean; decimal
strings are truncated previews computed with integers. Every contract control is a
damaging-mutation control whose rejection is required. Failures raise explicit
exceptions (never assert), so the output bytes are identical under python -O.

Usage: python3 -B research/round33/reverse/ba2/check.py --output /absolute/fresh/dir
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
REPORT = HERE / 'report.md'
CONTRACT_REL = 'research/round33/contracts/ba2.json'
CONTRACT_SHA256 = '275ba3b002529b7295d0f8b91dc1cc7a96451e3c7f936ee698a932fdca54fcff'
NS_REL = 'research/round33/sources/nachtergaele-sims-1410.8174v1.md'
NS_PDF_SHA256 = '501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba'
I1_REL = 'research/round21/forward/i1/report.md'
AQ1_REL = 'research/round29/forward/aq1/report.md'
AY1R_REL = 'research/round32/reverse/ay1/report.md'
AQ1_GATE_REL = 'research/round29/advisor/aq1-gate.json'
AY1_GATE_REL = 'research/round32/advisor/ay1-gate.json'
AY2_GATE_REL = 'research/round32/advisor/ay2-gate.json'
PINNED_SHA256 = {
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    NS_REL: '6a28f4cd6aa2c55286fa839d83c00356ff0709f8b02027ee5b39050df1d6c921',
}
# The shared premises the frozen contract declares (pinned so that a coherent removal
# of a snapshot together with its contract line is still rejected).
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
    'research/round33/advisor/selection-ba2.md', NS_REL,
    'research/round29/experts/aq-source-dictionary.md', 'research/round29/experts/aq-primary-bindings.json',
    'research/round29/skeptic/aq1.md',
)
FORBIDDEN_PREFIXES = (
    'research/round33/forward/', 'research/round33/skeptic/', 'research/round33/experts/',
    'research/round33/advisor/deliberation', 'research/round33/advisor/panel', 'research/round33/reverse/',
)
FORBIDDEN_WORDS = ('triage', 'recommendation', 'prospective', 'loop2', 'loop-2', 'deliberation', 'memo')
# Frozen targets (the contract sha256 is pinned, so these equal the frozen text).
TARGET_COMPARISON = Q(6, 10 ** 11)
TARGET_CAUCHY = Q(25, 10 ** 11)
F1_NAME = 'F1 (AQ1 centered whole-star boxes)'
F2_NAME = 'F2 (I1 section 6 all-contained-face boxes with padding)'
PHI = 'whole-star Phi'
PHI_PRIME = "owner-set Phi'"
ONSITE_SLOT = 'H_x slot of (44); handled by the interaction picture (54),(57) inside Theorem 3.1'
TIER = 'polynomial_lieb_robinson'
DYNAMICS_TOPOLOGY = 'operator norm on B(H_R), uniformly for |theta|<=8 (compact window)'
STATES_TOPOLOGY = 'local trace norm on finite regions (subsequential F2 limit states, O6 only)'
GNS_TOPOLOGY = 'strong continuity of the GNS unitary group (not norm continuity in theta)'


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


def parse_sci(text):
    """'6x10^-11' or '2.5x10^-10' -> exact Fraction."""
    m = re.fullmatch(r'([0-9]+(?:\.[0-9]+)?)x10\^-([0-9]+)', text)
    require(m is not None, 'malformed scientific literal: ' + text)
    return Q(m.group(1)) / 10 ** int(m.group(2))


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


DEN = 10 ** 40


def floor_to(x, den=DEN):
    x = Q(x)
    return Q((x.numerator * den) // x.denominator, den)


def ceil_to(x, den=DEN):
    x = Q(x)
    return Q(-((-x.numerator * den) // x.denominator), den)


def exp_bounds(x, terms=30):
    """Directed enclosure of exp(x) for 0<=x<=1/2: partial sum plus geometric tail."""
    x = Q(x)
    must(Q(0) <= x and x <= Q(1, 2), 'exponential argument outside [0,1/2]')
    partial, power = Q(0), Q(1)
    for k in range(terms + 1):
        partial += power / factorial(k)
        power *= x
    tail = power / factorial(terms + 1) / (1 - x / (terms + 2))
    return floor_to(partial), ceil_to(partial + tail)


def E_up(x):
    """Rational upper bound of E(x)=2(e^x-1-x)/x^2=2 sum_j x^j/(j+2)!, 0<=x<5:
    (j+2)!>=24*5^(j-2) for j>=2 gives E(x)<=1+x/3+x^2/(12(1-x/5))."""
    x = Q(x)
    must(Q(0) <= x and x < 5, 'E_up argument outside [0,5)')
    return 1 + x / 3 + x * x / (12 * (1 - x / 5))


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


def l1(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


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


def class_face_links(anchor, cls):
    name, r, s, support, _ = cls
    a, c = {n: (x, y) for n, x, y in ORIENTATIONS}[name]
    p = (4 * anchor[0] + r, 2 * anchor[1] + s, anchor[2])
    links = face_links(p, a, c)
    must(tuple(sorted({coarse(t) for t, _ in links})) == owners_of(anchor, cls), 'owner set differs from the link tails')
    return links


def box_sites(N):
    rng = range(-N, N + 1)
    return [(x, y, z) for x in rng for y in rng for z in rng]


def f1_faces(N, classes):
    """AQ1 family: omitted faces of whole stars b+S contained in Lambda_N (I1.6)."""
    sites = set(box_sites(N))
    out = {}
    for b in box_sites(N):
        if all(vadd(b, v) in sites for v in STAR):
            for k, cls in enumerate(classes):
                out[(b, k)] = owners_of(b, cls)
    return out


def f2_faces(N, classes):
    """I1 section-6 family: every omitted face whose actual owner set lies in Lambda_N
    (the native restriction of the owner-set interaction Phi' to Lambda_N)."""
    sites = set(box_sites(N))
    out = {}
    for b in box_sites(N):
        for k, cls in enumerate(classes):
            ow = owners_of(b, cls)
            if all(o in sites for o in ow):
                out[(b, k)] = ow
    return out


def whole_stars(N):
    sites = set(box_sites(N))
    return {b: tuple(vadd(b, v) for v in STAR) for b in box_sites(N) if all(vadd(b, v) in sites for v in STAR)}


def padding_sites(N):
    sites = set(box_sites(N))
    plus = {vadd(b, v) for b in sites for v in STAR}
    return plus - sites


def factor_links(b):
    return [((4 * b[0] + r, 2 * b[1] + s, b[2]), d) for r in range(4) for s in range(2) for d in range(3)]


def cover_counts(cover):
    links = [l for b in cover for l in factor_links(b)]
    ends = {t for t, _ in links} | {vadd(t, DIRS[d]) for t, d in links}
    return len(links), len(ends)


# ---------------------------------------------------- decay function F(r)
def F(r):
    return Q(1, (1 + r) ** 4)


def shell_count(r):
    """Number of Z^3 points at l1 distance exactly r from the origin (enumerated)."""
    n = 0
    for x in range(-r, r + 1):
        for y in range(-(r - abs(x)), r - abs(x) + 1):
            rest = r - abs(x) - abs(y)
            n += 1 if rest == 0 else 2
    return n


def shell_formula(r):
    return 1 if r == 0 else 4 * r * r + 2


def tail_upper(m):
    """T(m)=sum_{r>=m}(4r^2+2)(1+r)^-4 <= 4 sum_{k>=m+1} k^-2 <= 4/m (m>=1)."""
    must(m >= 1, 'tail index must be at least 1')
    return Q(4, m)


def tail_partial(m, count):
    return sum((Q(shell_formula(r)) * F(r) for r in range(m, m + count)), Q(0))


# ------------------------------------------ exact Gaussian-rational matrices
# A complex number is a pair (re, im) of Fractions; a matrix is a tuple of row tuples.
C0 = (Q(0), Q(0))
C1 = (Q(1), Q(0))
CI = (Q(0), Q(1))


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cconj(a):
    return (a[0], -a[1])


def ipow(n):
    """i^n for integer n, exactly."""
    return ((C1, CI, (Q(-1), Q(0)), (Q(0), Q(-1)))[n % 4])


def mat(rows):
    return tuple(tuple((Q(v), Q(0)) if not isinstance(v, tuple) else (Q(v[0]), Q(v[1])) for v in row) for row in rows)


def mdim(A):
    return len(A)


def meye(n):
    return tuple(tuple(C1 if i == j else C0 for j in range(n)) for i in range(n))


def mmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return tuple(tuple(_dot(A[i], B, j, k) for j in range(m)) for i in range(n))


def _dot(row, B, j, k):
    acc = C0
    for t in range(k):
        if row[t] != C0 and B[t][j] != C0:
            acc = cadd(acc, cmul(row[t], B[t][j]))
    return acc


def madd(A, B):
    return tuple(tuple(cadd(a, b) for a, b in zip(ra, rb)) for ra, rb in zip(A, B))


def mscale(c, A):
    return tuple(tuple(cmul(c, a) for a in row) for row in A)


def mdag(A):
    return tuple(tuple(cconj(A[j][i]) for j in range(len(A))) for i in range(len(A[0])))


def kron(A, B):
    return tuple(tuple(cmul(A[i // len(B)][j // len(B[0])], B[i % len(B)][j % len(B[0])])
                       for j in range(len(A[0]) * len(B[0]))) for i in range(len(A) * len(B)))


def mzero(A):
    return all(v == C0 for row in A for v in row)


def spectral_unitary(H, eigenvalues, n_quarter):
    """exp(i*(n_quarter*pi/2)*H) for Hermitian H with the given integer spectrum, from the
    Lagrange spectral projectors of H itself (exact). Verifies the minimal polynomial."""
    n = mdim(H)
    I = meye(n)
    prod = I
    for lam in eigenvalues:
        prod = mmul(prod, madd(H, mscale((Q(-lam), Q(0)), I)))
    must(mzero(prod), 'claimed spectrum does not annihilate H')
    U = tuple(tuple(C0 for _ in range(n)) for _ in range(n))
    total = tuple(tuple(C0 for _ in range(n)) for _ in range(n))
    for lam in eigenvalues:
        P = I
        for mu in eigenvalues:
            if mu != lam:
                P = mscale((Q(1, lam - mu), Q(0)), mmul(P, madd(H, mscale((Q(-mu), Q(0)), I))))
        total = madd(total, P)
        U = madd(U, mscale(ipow(n_quarter * lam), P))
    must(total == I, 'spectral projectors do not resolve the identity')
    return U


PAULI_X = mat([[0, 1], [1, 0]])
PAULI_Z = mat([[1, 0], [0, -1]])
I2 = meye(2)


def padding_factorization_fixture():
    """Sites a (in R), b (bulk of Lambda_N), p (padding qutrit with on-site h_p=diag(0,1,2)).
    H2 = X_a X_b (a stand-in bounded box Hamiltonian); Hpad = H2 (x) 1 + 1 (x) h_p.
    At u=pi/2 both exponentials are exact Gaussian-rational matrices."""
    H2 = kron(PAULI_X, PAULI_X)
    hp = mat([[0, 0, 0], [0, 1, 0], [0, 0, 2]])
    Hpad = madd(kron(H2, meye(3)), kron(meye(4), hp))
    U2 = spectral_unitary(H2, (-1, 1), 1)
    Upad = spectral_unitary(Hpad, (-1, 0, 1, 2, 3), 1)
    Up = spectral_unitary(hp, (0, 1, 2), 1)
    A = kron(PAULI_Z, I2)                                   # A in B(H_R), R={a}
    lhs = mmul(mmul(Upad, kron(A, meye(3))), mdag(Upad))
    rhs = kron(mmul(mmul(U2, A), mdag(U2)), meye(3))
    commutes = mzero(madd(mmul(kron(H2, meye(3)), kron(meye(4), hp)),
                          mscale((Q(-1), Q(0)), mmul(kron(meye(4), hp), kron(H2, meye(3))))))
    return {'factorizes': lhs == rhs, 'tensor_product_unitary': Upad == kron(U2, Up), 'padding_commutes': commutes,
            'evolved_A_is_minus_A': mmul(mmul(U2, A), mdag(U2)) == mscale((Q(-1), Q(0)), A),
            'U2_is_iXX': U2 == mscale(CI, H2)}


def algebraic_not_gns_fixture():
    """Same algebraic dynamics, different states: H=diag(0,1), A=sigma_x, u=pi/2."""
    H = mat([[0, 0], [0, 1]])
    U = spectral_unitary(H, (0, 1), 1)
    tauA = mmul(mmul(U, PAULI_X), mdag(U))
    prod = mmul(PAULI_X, tauA)
    return prod[0][0], prod[1][1]


# ------------------------------------------------------------ claim validators
GATE_FIELD_NAMES = ('uniqueness_of_ground_state_claimed', 'gns_dynamics_equality_claimed', 'uniform_in_time_claimed',
                    'rate_in_N_claimed', 'rate_in_a_claimed', 'continuum_claim', 'scientific_priority_verified',
                    'whole_sequence_claimed', 'whole_sequence_scope', 'dynamics_level',
                    'dynamics_limit_identified_claimed', 'common_limit_claimed', 'state_convergence_claimed',
                    'translation_invariance_claimed', 'weak_coupling_claim', 'true_values_rule')
ALWAYS_FALSE = ('uniqueness_of_ground_state_claimed', 'gns_dynamics_equality_claimed', 'uniform_in_time_claimed',
                'rate_in_a_claimed', 'continuum_claim', 'scientific_priority_verified', 'common_limit_claimed',
                'state_convergence_claimed', 'translation_invariance_claimed', 'weak_coupling_claim')
TRUE_IF_ADMITTED = {'rate_in_N_claimed': ('comparison', 'cauchy_F1', 'cauchy_F2'),
                    'whole_sequence_claimed': ('cauchy_F1', 'cauchy_F2'),
                    'dynamics_limit_identified_claimed': ('comparison', 'cauchy_F2')}


def validate_claim_flags(flags):
    for key in ('continuum_claim', 'uniqueness_of_ground_state_claimed', 'gns_dynamics_equality_claimed',
                'uniform_in_time_claimed', 'rate_in_a_claimed', 'scientific_priority_verified', 'weak_coupling_claim',
                'uniform_wilson_claim', 'resolved_interaction_shift'):
        require(flags.get(key) is False, 'claim flag must be exactly false: ' + key)
    return True


def validate_gate_fields(exported, required, admitted):
    require(sorted(exported) == sorted(required), 'gate fields must be exactly the contract gate_fields_required')
    for key in ALWAYS_FALSE:
        require(exported[key] is False, 'gate field must be false: ' + key)
    for key, needs in TRUE_IF_ADMITTED.items():
        want = all(admitted.get(n) is True for n in needs)
        require(exported[key] is want, 'gate field ' + key + ' must be true only if its targets are admitted')
    for key in ('whole_sequence_scope', 'dynamics_level', 'true_values_rule'):
        require(exported[key] == required[key], 'gate field text differs from the contract: ' + key)
    require(exported['dynamics_level'] == 'algebraic_heisenberg_compact_window', 'dynamics level must be algebraic')
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
    require(rec.get('metric') == 'l1 on the coarse Z^3 factor lattice', 'metric must be the coarse l1 metric')
    require(rec.get('weights') == 'F(r)=(1+r)^-4', 'weights must be the AQ1 polynomial F')
    require(parse_q(rec.get('window_theta')) == 8, 'window must be |theta|<=8')
    require(rec.get('finite_graph') is False and rec.get('uniform_model') is False, 'finite-graph or uniform model relabelled')
    return True


def certify_lr_record(rec):
    """One tier and one interaction per constant; the inner family's own constants only."""
    require(rec.get('tier') == TIER, 'tier must be named polynomial_lieb_robinson (AQ1 F)')
    require(rec.get('F') == '(1+r)^-4', 'decay function must be the AQ1 F(r)=(1+r)^-4')
    fam = rec.get('inner_family')
    require(fam in ('F1', 'F2'), 'inner family must be named (F1 or F2)')
    want_inter, want_norm = {'F1': (PHI, Q(2268)), 'F2': (PHI_PRIME, Q(1323))}[fam]
    require(rec.get('interaction') == want_inter, 'inner-family constants swapped: ' + fam + ' inner needs ' + want_inter)
    require(parse_q(rec.get('norm_F_per_tau')) == want_norm, 'interaction norm must be the inner family own constant')
    require(parse_q(rec.get('C')) == 224, 'convolution constant must be the AQ1 C<=224 of F(r)=(1+r)^-4')
    require(rec.get('onsite_placement') == ONSITE_SLOT, 'unbounded on-site terms must sit in the H_x slot (interaction picture)')
    require(rec.get('native_restriction') is True, 'inner evolution must be the native restriction (44) of its interaction')
    return True


def certify_onsite_placement(rec):
    require(rec.get('onsite_in_interaction') is False, 'unbounded on-site term placed inside the bounded interaction')
    require(rec.get('lr_applied_to') == 'native restriction with H_x unbounded on-site', 'bounded-interaction LR bound applied to the full Hamiltonian')
    require(rec.get('interaction_norm_cutoff_independent') is True, 'interaction norm depends on an on-site cutoff')
    return True


def certify_comparison_source(rec, enum):
    require(rec.get('terms') == 'extra F2 faces: owner set inside Lambda_N, anchor star not inside Lambda_N',
            'comparison source must be exactly the extra F2 faces (new terms only)')
    require(rec.get('padding_charged') is False, 'padding on-site terms left in the Duhamel difference')
    require(rec.get('old_terms_charged') is False, 'comparison source charged with F1 (old) terms')
    require(rec.get('combine') == 'linear', 'deterministic face bounds add linearly (no root-N)')
    require(parse_q(rec.get('per_face_norm_per_tau')) == Q(1, 3), 'each face -(tau/3)W_f has norm |tau|/3')
    require(parse_q(rec.get('owners_max')) == 3, 'every omitted face has at most three owners')
    for N, data in enum.items():
        require(data['count'] == 28 * N * (5 * N + 1) and rec.get('count_formula') == '28N(5N+1)',
                'extra-face count differs from the enumeration')
        require(data['min_dist_e_z'] == N - 1 and rec.get('dist_e_z') == 'N-1', 'distance from e_z must be N-1 (enumerated)')
        require(data['min_dist_0'] == N and rec.get('dist_0') == 'N', 'distance from 0 must be N (enumerated)')
        require(data['max_owners'] <= parse_q(rec['owners_max']), 'a face has more owners than charged')
    require(parse_q(rec.get('geometry_coefficient')) == 168, 'geometry coefficient 3*28*2=168 per (5N+1)N^-3')
    return True


def certify_cauchy_source(rec):
    fam = rec.get('family')
    require(fam in ('F1', 'F2'), 'Cauchy family must be named')
    require(rec.get('terms') == 'new terms X inside Lambda_M, not inside Lambda_N', 'Cauchy source must be the new terms only')
    require(rec.get('route') == 'sup over M greater than N, one Duhamel between Lambda_N and Lambda_M',
            'an N to N+1 bound alone is not a Cauchy estimate')
    require(rec.get('combine') == 'linear', 'deterministic bounds add linearly (no root-N)')
    require(rec.get('incoming_included') is True, 'per-site sums must include incoming anchors')
    want = {'F1': Q(28), 'F2': Q(49, 3)}[fam]
    require(parse_q(rec.get('per_site_per_tau')) == want, 'per-site source sum must be J=28|tau| (F1) or 49|tau|/3 (F2)')
    if fam == 'F2':
        require(rec.get('charge') == 'face by face through owner sets', 'F2 regrouped clipped groups must be charged face by face')
    require(parse_q(rec.get('tail_coefficient')) == 8 and rec.get('rate') == '1/(N-1)',
            'polynomial tail: 4/N+4/(N-1)<=8/(N-1), the honest O(1/N) rate')
    return True


def certify_rate_claim(rec):
    require(rec.get('decay') == 'polynomial', 'exponential decay in N claimed with the polynomial F')
    require(rec.get('comparison_exponent') == 2 and rec.get('cauchy_exponent') == 1,
            'rates: comparison N^-2 ((5N+1)N^-3), Cauchy 1/N')
    require(rec.get('in') == 'N at fixed spacing', 'rate must be in N at fixed spacing, never in a')
    return True


def certify_decay_claim(claim, witnesses):
    """With the polynomial F only a polynomial rate in N is available. An exponential claim
    C0*q^m is rejected; the exact lower witnesses m*S(m)>=1/2 of the tail name where it fails."""
    if claim.get('decay') == 'polynomial':
        return True
    c0, q = parse_q(claim['C0']), parse_q(claim['q'])
    bad = [m for m, s in witnesses if s > c0 * q ** m]
    require(False, 'exponential decay in N claimed with the polynomial Lieb-Robinson function'
            + (' (exact tail witness exceeds C0*q^m at m=' + str(bad[0]) + ')' if bad else ''))


def certify_exponential_instance(inst):
    require(inst.get('label') == 'exponential_lieb_robinson', 'an exponential F_mu must be a separately labelled instance')
    require(inst.get('admission_weight') is False, 'no target is frozen for the exponential instance')
    mu = parse_q(inst.get('mu'))
    require(mu > 0, 'F_mu needs mu>0')
    require(inst.get('norm_factor') == 'e^{2 mu} 81 J' and inst.get('C_source') == 'own C_{F_mu}<=224',
            'F_mu constants mixed with the AQ1 polynomial constants')
    return True


def certify_cauchy_claim(kind, per_step_exponent=None):
    require(kind == 'sup_M', 'an N to N+1 bound summed as a Cauchy estimate is rejected (harmonic sum diverges)')
    return True


def certify_scaling(ratio, bracket):
    lo, hi = bracket
    require(lo <= ratio <= hi, 'tau -> tau/100 ratio outside its preregistered bracket')
    return True


def certify_order_label(label, ratio, quad_bracket):
    require(label == 'quadratic', 'the dynamics difference is O(tau^2 U^2); a linear label is rejected')
    certify_scaling(ratio, quad_bracket)
    return True


def certify_window_claim(rec):
    require(rec.get('uniform_in_time') is False, 'uniform-in-time claim rejected (bound grows like U^2 e^{vU})')
    require(rec.get('window') == '|theta|<=8' and rec.get('U') == '1', 'window must be named with U=Theta/8')
    return True


def certify_dynamics_level(rec):
    require(rec.get('level') == 'algebraic_heisenberg_compact_window', 'comparison is of algebraic dynamics only')
    require(rec.get('gns_equality') is False and rec.get('correlation_equality') is False,
            'GNS dynamics or correlation-function equality of different states needs a proved common state')
    return True


def certify_identification(rec):
    require(rec.get('source') == 'comparison bound b(N) -> 0 along the whole sequence',
            'the F2 limit dynamics is identified only through the comparison bound')
    require(rec.get('sequence') == 'whole sequence', 'identification needs whole-sequence dynamics convergence')
    require(rec.get('general_local_X') is True, 'identification on all local observables needed for the automorphism group')
    return True


def certify_o6(rec):
    for step in ('stationarity', 'gns_strong_continuity', 'nonnegative_generator', 'gauge_physical_restriction'):
        s = rec.get(step)
        require(isinstance(s, dict) and s.get('status') == 'rerun', 'O6 step not rerun: ' + step)
        require(s.get('subsequence') == 'F2 own subsequence', 'O6 step must use F2 own subsequences: ' + step)
        require(s.get('dynamics') == 'AQ1 T_theta, identified with the F2 limit', 'O6 step uses unidentified dynamics: ' + step)
    return True


def certify_limit_statement(rec):
    require(rec.get('quantifier') in ('whole sequence', 'subsequence'), 'limit statement must say whole sequence or subsequence')
    if rec['quantifier'] == 'whole sequence':
        require(rec.get('from') == 'Cauchy bound', 'whole-sequence claims come only from a Cauchy bound')
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


def certify_families(rec):
    require(rec == [F1_NAME, F2_NAME], 'exactly the two named families F1 and F2 are compared')
    return True


def certify_family_faces(name, face_set, f1_set, f2_set):
    require({'F1': f1_set, 'F2': f2_set}[name] == face_set, 'family ' + name + ' face set differs from its definition')
    return True


def certify_topology(rec):
    require(rec.get('dynamics') == DYNAMICS_TOPOLOGY, 'dynamics topology must be operator norm uniformly on the window')
    require(rec.get('states') == STATES_TOPOLOGY, 'state topology must be local trace norm')
    require(rec.get('time_continuity') == GNS_TOPOLOGY, 'norm continuity in theta on all of B(H_R) is not claimed')
    require(rec['dynamics'] != rec['states'], 'one topology for both rejected')
    return True


def certify_same_coupling(tau1, tau2):
    require(parse_q(tau1) == parse_q(tau2), 'cross-coupling comparison rejected: both families at the same tau')
    return True


def certify_cover(cover, n_links, n_endpoints):
    require(tuple(sorted(cover)) == COVER, 'cover must be the complete factor cover R={0,e_z} of W')
    require(n_links == 48 and n_endpoints == 36, 'complete cover has 48 links and 36 endpoints')
    return True


def certify_incoming(j_per_tau, stars_per_site, star_norm_per_tau):
    require(stars_per_site == 4, 'per-site sums must count all four incident stars (incoming anchors)')
    require(parse_q(j_per_tau) == stars_per_site * parse_q(star_norm_per_tau) == 28, 'J=28|tau|')
    return True


def certify_face_pins(pins, derived):
    require(pins.get('provenance') == 'derived from the I1 table by translation covariance', 'face counts must be derived')
    for key in ('faces_per_factor', 'owner_sets_per_factor', 'faces_meeting_R', 'faces_inside_R'):
        require(pins.get(key) == derived[key], 'face pin differs from the all-site derivation: ' + key)
    return True


def certify_f2_charge(charged, new_faces):
    require(charged == new_faces, 'F2 regrouped clipped groups charged more than once (old faces recharged)')
    return True


def certify_boundary_source(source_terms, new_terms, meets):
    """The source is exactly the set of added terms (none old, none missing), each meeting the added region."""
    require(set(source_terms) == set(new_terms), 'boundary source must contain exactly the new terms (no old terms, none missing)')
    require(all(meets(t) for t in source_terms), 'a source term does not meet the added region')
    return True


def certify_outcome(recorded, facts):
    if not (facts['lr_applies'] and facts['source_counted']):
        want = 'insufficient'
    elif all(facts[k] for k in ('comparison', 'cauchy_F1', 'cauchy_F2', 'identified', 'o6')):
        want = 'accepted_within_scope'
    else:
        want = 'limited'
    require(recorded == want, 'recorded verdict ' + str(recorded) + ' differs from the rule (' + want + ')')
    return True


def admit_bound(value, target):
    v, t = parse_q(value), parse_q(target)
    require(v <= t, 'bound exceeds the frozen target')
    return True


def assemble_linear(terms, combine='linear'):
    require(combine == 'linear', 'root-sum-square or root-N assembly rejected')
    return sum((parse_q(t) for t in terms), Q(0))


def divide_by_root(value, count):
    require(False, 'division by sqrt(N) or sqrt(#faces) rejected for deterministic bounds')


def certify_error_ledger(ledger, names):
    require(sorted(ledger) == sorted(names), 'error ledger must itemize exactly the preregistered terms')
    for k, v in ledger.items():
        require(isinstance(v, dict) and ('value' in v or 'not_applicable' in v), 'ledger entry malformed: ' + k)
        if 'not_applicable' in v:
            require(bool(v.get('reason')), 'not_applicable ledger entry needs a stated reason: ' + k)
    return True


# --------------------------------------------------------- text scanners
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state',
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
    require(any(line.strip().endswith(template) or template in line for line in report_text.splitlines()),
            'mandatory sentence template must be one unbroken span on one line')
    return True


def ns_quote_lines(ns_text):
    """Verbatim Part A statements that the report must quote (never paraphrased)."""
    part_a = ns_text.split('## Part A.')[1].split('## Part B.')[0]
    lines = [ln for ln in part_a.splitlines() if ln.strip()]
    wanted = []
    for tag in ('(40)', '(41)', '(44)', '(48)', '(49)', '(50)', '(51)', '(52)', '(77)'):
        hit = [ln[2:] for ln in lines if ln.startswith('- ' + tag)]
        must(len(hit) == 1, 'excerpt line missing: ' + tag)
        wanted.append(hit[0])
    for start in ('To each x ∈ Γ a separable complex Hilbert space', 'essentially self-adjoint on the dense domain (45)',
                  '**Theorem 3.1.** Let Γ and F be as indicated above.', 'holds for all t ∈ ℝ, where the quantity D(X, Y)',
                  'The proof (steps 1–4) uses an interaction-picture dynamics (57)', 'exists and the convergence is uniform for t in compact sets.',
                  'In its proof: (78)'):
        hit = [ln for ln in lines if ln.startswith(start)]
        must(len(hit) == 1, 'excerpt passage missing: ' + start)
        wanted.append(hit[0])
    t41 = [ln for ln in lines if ln.startswith('**Theorem 4.1**')]
    must(len(t41) == 1, 'Theorem 4.1 line missing')
    body = t41[0].split('). ', 1)[1]           # the statement, after the section-title parenthesis
    must(body.startswith('Let Γ and F be as described in Section 3.'), 'Theorem 4.1 statement start')
    wanted.append(body)
    part_b = ns_text.split('## Part B.')[1]
    b47 = [ln for ln in part_b.splitlines() if ln.startswith('(47)')]
    must(len(b47) == 1, 'excerpt (47) line missing')
    wanted.append(b47[0])
    setting = [ln for ln in lines if ln.startswith('Setting (Section 3).')]
    must(len(setting) == 1, 'excerpt setting line missing')
    wanted.append(setting[0])
    return wanted


def certify_quotes(report_text, quotes, source_label):
    require(source_label == NS_REL, 'the Lieb-Robinson form must be quoted from the committed excerpt, not second-hand')
    for q in quotes:
        require(q in report_text, 'Nachtergaele-Sims passage not quoted verbatim: ' + q[:70])
    return True


# ------------------------------------------------------ contract and premises
CONTROL_IDS = (
    'coherent_evidence_tampering', 'exact_arithmetic_admission', 'no_priority_or_continuum_claim',
    'changed_model_relabelled', 'insufficient_verdict_retained', 'tau_scaling_exponent', 'wrong_delta_alpha_hbar_clock',
    'missing_incoming_stars', 'root_n_misuse', 'tier_mixing_rejected', 'reverse_premise_isolation', 'face_count_all_sites',
    'uniform_in_N_not_in_a', 'placeholder_span_rejected', 'negation_aware_phrase_scan',
    'parameters_declare_metric_weights_window', 'lieb_robinson_polynomial_tail', 'lieb_robinson_F_declared',
    'lieb_robinson_form_quoted', 'unbounded_onsite_interaction_picture', 'duhamel_inner_family_constants',
    'extra_face_count_and_distance', 'duhamel_tau_order_quadratic', 'time_window_named_common_clock',
    'algebraic_not_gns_dynamics', 'f2_limit_dynamics_equals_f1', 'two_families_named', 'subsequence_versus_whole_sequence',
    'decay_rate_in_N_not_a', 'boundary_source_new_terms_only', 'f2_regrouping_charged_once', 'full_original_wilson_cover',
    'topology_named', 'cross_coupling_comparison_rejected', 'gate_fields_topic_specific')
INHERITED_SEMANTICS = ('full_original_wilson_cover', 'topology_named', 'cross_coupling_comparison_rejected',
                       'gate_fields_topic_specific')
EXPECTED_EXCLUSIONS = [
    'equality of GNS dynamics or of correlation functions of different states', 'uniform-in-time statements',
    'exponential decay in N with the polynomial Lieb-Robinson function', 'uniqueness of every infinite-volume ground state',
    'any estimate uniform in the lattice spacing a', 'continuum or weak coupling', 'scientific priority']
ERROR_TERMS = ['lieb_robinson_tail', 'duhamel_boundary_sum', 'interaction_picture_onsite', 'inner_family_constants', 'arithmetic']
TEMPLATE_NEGATIONS = ('not equality of GNS dynamics or of correlation functions of different states',
                      'not a uniform-in-time statement', 'not a statement uniform in the lattice spacing a')


def parse_contract_numbers(data):
    p, pre, ncs = data['parameters'], data['preregistration'], data['new_control_semantics']
    for key in ('metric', 'weights', 'window', 'boundary_source', 'targets'):
        require(isinstance(p.get(key), str if key != 'targets' else dict) and bool(p.get(key)),
                'parameters must declare ' + key + ' as a field (not prose)')
    require('clock' in pre and 'theta=alpha*t/hbar' in pre['clock'] and 'u=theta/8' in pre['clock'], 'clock field')
    t = p['targets']
    m = re.search(r'<= ([0-9.]+x10\^-[0-9]+) \(5N\+1\) N\^-3 \|\|A\|\| for \|theta\| at most (\d+) and N at least (\d+) '
                  r'\(polynomial_lieb_robinson tier\)', t.get('comparison', ''))
    require(m is not None, 'comparison target text malformed')
    cmp_t, theta_c, n0_c = parse_sci(m.group(1)), int(m.group(2)), int(m.group(3))
    m = re.search(r'sup over M greater than N of \|\|T\^\{F1,M\}_theta\(A\)-T\^\{F1,N\}_theta\(A\)\|\| at most '
                  r'([0-9.]+x10\^-[0-9]+)/\(N-1\) \|\|A\|\| for \|theta\| at most (\d+) and N at least (\d+), and the same for F2',
                  t.get('within_family_cauchy', ''))
    require(m is not None, 'Cauchy target text malformed')
    cau_t, theta_k, n0_k = parse_sci(m.group(1)), int(m.group(2)), int(m.group(3))
    vals = pre['target']['value'].split(' and ')
    require(len(vals) == 2 and parse_sci(vals[0]) == cmp_t and parse_sci(vals[1]) == cau_t, 'preregistered target values')
    require(pre['target']['comparator'] == '<=', 'target comparator')
    require(cmp_t == TARGET_COMPARISON and cau_t == TARGET_CAUCHY, 'targets differ from the frozen values')
    m = re.search(r'\|theta\|<=(\d+) in theta=alpha t/hbar \(normalized u=theta/(\d+)<=1 internally\)', p['window'])
    require(m is not None, 'window field malformed')
    theta, eight = int(m.group(1)), int(m.group(2))
    require(theta == theta_c == theta_k == 8 and eight == 8 and n0_c == n0_k == 2, 'window/N_0 inconsistent')
    mm = p['metric']
    c_conv = re.search(r'convolution constant C at most (\d+)', mm)
    phi = re.search(r'\|\|Phi\|\|_F at most (\d+)J = (\d+)\|tau\|', mm)
    phip = re.search(r"\|\|Phi'\|\|_F at most (\d+)\|tau\|", mm)
    require(bool(c_conv and phi and phip) and 'F(r)=(1+r)^-4' in mm and '4r^2+2 sites' in mm, 'metric constants malformed')
    require('(1+r)^-4' in p['weights'] and 'labelled extra' in p['weights'], 'weights field malformed')
    require('28N(5N+1)' in p['boundary_source'] and 'at least N-1 from e_z and at least N from 0' in p['boundary_source'],
            'boundary source field malformed')
    pins = re.search(r'(\d+) faces per factor, (\d+) owner sets, (\d+) meeting R, (\d+) inside R', ncs['face_count_all_sites'])
    require(pins is not None, 'face pins malformed')
    br_c = re.match(r'\[(\d+),(\d+)\]', pre['scaling_brackets_per_constant']['comparison_coefficient'])
    br_k = re.match(r'\[(\d+),(\d+)\]', pre['scaling_brackets_per_constant']['cauchy_coefficient'])
    br_q = re.search(r'lies in \[(\d+),(\d+)\]', ncs['duhamel_tau_order_quadratic'])
    require(bool(br_c and br_k and br_q), 'scaling brackets malformed')
    require('J=28|tau|, four stars' in ncs['missing_incoming_stars'] and '49|tau|/3' in ncs['f2_regrouping_charged_once'],
            'incidence semantics malformed')
    return {
        'target_comparison': cmp_t, 'target_cauchy': cau_t, 'theta_window': Q(theta), 'N0': n0_c,
        'C': Q(int(c_conv.group(1))), 'phi_factor': Q(int(phi.group(1))), 'phi_norm': Q(int(phi.group(2))),
        'phi_prime_norm': Q(int(phip.group(1))),
        'pins': {'faces_per_factor': int(pins.group(1)), 'owner_sets_per_factor': int(pins.group(2)),
                 'faces_meeting_R': int(pins.group(3)), 'faces_inside_R': int(pins.group(4))},
        'bracket_comparison': (Q(int(br_c.group(1))), Q(int(br_c.group(2)))),
        'bracket_cauchy': (Q(int(br_k.group(1))), Q(int(br_k.group(2)))),
        'bracket_quadratic': (Q(int(br_q.group(1))), Q(int(br_q.group(2)))),
        'tau': parse_q(pre['tau']['value']),
    }


def validate_contract(data):
    require(data.get('id') == 'BA2' and data.get('round') == 33 and data.get('status') == 'frozen_before_production',
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
    require('F1 (AQ1 centered whole-star boxes)' in data['model'] and 'F2 (I1 section 6 all-contained-face boxes with padding)'
            in data['model'] and '|tau|<=10^-8' in data['model'], 'families or cap missing from the model')
    ids = data['controls']
    require(tuple(ids) == CONTROL_IDS and ids == pre['controls_required']['ids'], 'controls differ from the preregistered ids')
    require(set(data['new_control_semantics']) <= set(ids) and sorted(set(ids) - set(data['new_control_semantics']))
            == sorted(INHERITED_SEMANTICS), 'control semantics changed (31 new, 4 inherited)')
    require(sorted(data['shared_premises']) == sorted(REQUIRED_PREMISES), 'shared premises differ from the frozen list')
    require(data['claim_exclusions'] == EXPECTED_EXCLUSIONS, 'claim exclusions changed')
    for phrase in ('the infinite-volume ground state', 'the thermodynamic limit', 'the AQ state'):
        require(phrase in pre['forbidden_phrasings'], 'forbidden phrasing list changed')
    tpl = pre['mandatory_sentence_template']
    require(all(n in tpl for n in TEMPLATE_NEGATIONS) and 'b(N)' in tpl, 'mandatory template lost a negation')
    gf = pre['gate_fields_required']
    require(tuple(sorted(gf)) == tuple(sorted(GATE_FIELD_NAMES)), 'gate field names')
    require(all(gf[k] is False for k in ALWAYS_FALSE), 'a required-false gate field was flipped')
    require(all(gf[k] is True for k in TRUE_IF_ADMITTED), 'a claimed gate field was flipped')
    require(pre['tier_names_allowed'] == ['polynomial_lieb_robinson', 'exponential_lieb_robinson'], 'tier names')
    require(pre['sub_labels_allowed'] == ['dynamics_on_compact_windows'], 'sub label')
    require(pre['error_terms_itemized'] == ERROR_TERMS, 'error terms')
    certify_no_placeholder(list(all_strings(data)))
    return parse_contract_numbers(data)


def validate_contract_bytes(raw, expected_sha):
    require(sha256_bytes(raw) == expected_sha, 'contract bytes do not match the bound hash')
    data = json.loads(raw)
    return data, validate_contract(data)


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    for f in files:
        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)
        require(not any(w in f.lower() for w in FORBIDDEN_WORDS), 'forbidden triage/deliberation/memo file in reverse inputs: ' + f)
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
    return json.dumps(data, indent=2).encode()


# --------------------------------------------------------- constant formulas
def lr_prefactor(norm, C, U):
    """(2/C) int_0^U (e^{2 norm C s}-1) ds = 2 norm U^2 E(2 norm C U) <= 2 norm U^2 E_up(.)"""
    return 2 * norm * U * U * E_up(2 * norm * C * U)


def comparison_value(lr, src, tau, U, enum):
    certify_lr_record(lr)
    certify_comparison_source(src, enum)
    a = abs(parse_q(tau))
    return (lr_prefactor(parse_q(lr['norm_F_per_tau']) * a, parse_q(lr['C']), parse_q(U))
            * parse_q(src['per_face_norm_per_tau']) * a * parse_q(src['geometry_coefficient']))


def cauchy_value(lr, src, tau, U):
    certify_lr_record(lr)
    certify_cauchy_source(src)
    require(lr['inner_family'] == src['family'], 'a within-family Cauchy estimate uses its own family inside the integral')
    a = abs(parse_q(tau))
    return (lr_prefactor(parse_q(lr['norm_F_per_tau']) * a, parse_q(lr['C']), parse_q(U))
            * parse_q(src['per_site_per_tau']) * a * parse_q(src['tail_coefficient']))


def naive_linear_bound(tau, U, faces_per_tau):
    """The first-order Duhamel bound 2U sum||v_f|| without the commutator structure (linear in tau)."""
    return 2 * parse_q(U) * abs(parse_q(tau)) * faces_per_tau


# ==================================================================== compute
def enumerate_box(N, classes):
    f1 = f1_faces(N, classes)
    f2 = f2_faces(N, classes)
    extra = {k: v for k, v in f2.items() if k not in f1}
    sites = set(box_sites(N))
    anchors_on_layer = all(max(b) == N for (b, _k) in extra)            # some b_i = N (b+e_i leaves the box)
    plane_ok = True
    for (b, k), ow in extra.items():
        planes = [i for i in range(3) if b[i] == N]
        plane_ok = plane_ok and len(planes) >= 1 and all(o[i] == N for i in planes for o in ow)
    owners_on_layer = all(linf(o) == N for ow in extra.values() for o in ow)
    d0 = min(l1(o, ORIGIN) for ow in extra.values() for o in ow)
    dz = min(l1(o, EZ) for ow in extra.values() for o in ow)
    exact_sum = sum((F(l1(o, x)) for ow in extra.values() for o in ow for x in COVER), Q(0))
    one_plane = sum(1 for (b, k) in extra if sum(1 for i in range(3) if b[i] == N) == 1)
    two_plane = sum(1 for (b, k) in extra if sum(1 for i in range(3) if b[i] == N) == 2)
    three_plane = sum(1 for (b, k) in extra if sum(1 for i in range(3) if b[i] == N) == 3)
    per_site_faces = {}
    for ow in f2.values():
        for o in ow:
            per_site_faces[o] = per_site_faces.get(o, 0) + 1
    stars = whole_stars(N)
    per_site_stars = {}
    for pts in stars.values():
        for p in pts:
            per_site_stars[p] = per_site_stars.get(p, 0) + 1
    f1_from_stars = {(b, k) for b in stars for k in range(len(classes))}
    meeting_R = {k for k, ow in f2.items() if any(o in COVER for o in ow)}
    pad = padding_sites(N)
    return {
        'f1': f1, 'f2': f2, 'extra': extra, 'count': len(extra), 'f1_count': len(f1), 'f2_count': len(f2),
        'f1_subset_f2': set(f1) <= set(f2), 'anchors_on_layer': anchors_on_layer, 'owners_on_plane': plane_ok,
        'owners_on_layer': owners_on_layer, 'min_dist_0': d0, 'min_dist_e_z': dz,
        'max_owners': max(len(ow) for ow in extra.values()), 'disjoint_from_R': all(o not in COVER for ow in extra.values() for o in ow),
        'charged_once': len(extra) == len(set(extra)), 'exact_sum': exact_sum,
        'anchor_faces': {'one_plane': one_plane, 'two_plane': two_plane, 'three_plane': three_plane},
        'partial_groups': len({b for (b, _k) in extra}),
        'max_faces_per_site': max(per_site_faces.values()), 'max_stars_per_site': max(per_site_stars.values()),
        'f1_is_whole_star_native': set(f1) == f1_from_stars,
        'f2_is_owner_set_native': set(f2) == {(b, k) for b in sites for k in range(len(classes))
                                            if all(o in sites for o in owners_of(b, classes[k]))},
        'meeting_R_f1': len({k for k in f1 if k in meeting_R}), 'meeting_R_f2': len(meeting_R),
        'padding_sites': len(pad), 'B_plus_sites': len(pad) + len(sites),
        'padding_touched': any(o in pad for ow in f2.values() for o in ow),
    }


def positive_checks():
    check_py_sha = sha256_file(HERE / 'check.py')                  # recorded before any evaluation
    raw = (INPUTS / CONTRACT_REL).read_bytes()
    contract_sha = sha256_bytes(raw)
    must(contract_sha == CONTRACT_SHA256, 'contract snapshot hash differs from the bound constant')
    pinned = {}
    for rel in sorted(PINNED_SHA256):
        rb = (INPUTS / rel).read_bytes()
        must(sha256_bytes(rb) == PINNED_SHA256[rel], 'pinned premise hash changed: ' + rel)
        pinned[rel] = sha256_bytes(rb)
    contract, P = validate_contract_bytes(raw, CONTRACT_SHA256)
    check('contract_snapshot_bound', contract_sha == CONTRACT_SHA256, contract_sha256=contract_sha,
          source='inputs/' + CONTRACT_REL, verified='before any evaluation')
    check('check_py_sha256_recorded_before_evaluation', len(check_py_sha) == 64, check_py_sha256=check_py_sha)
    ns_text = (INPUTS / NS_REL).read_text()
    check('pinned_gate_and_excerpt_hashes', NS_PDF_SHA256 in ns_text and len(pinned) == 6, pinned_sha256=pinned,
          ns_pdf_sha256_named_in_excerpt=NS_PDF_SHA256)
    cache = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if '__pycache__' in p.parts or p.suffix == '.pyc')
    check('no_interpreter_cache_in_closure', cache == [])
    files = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    must(validate_inventory(files, contract), 'inventory')
    pre, ncs = contract['preregistration'], contract['new_control_semantics']
    TAU = P['tau']
    THETA = P['theta_window']
    U = THETA / 8
    must(certify_clock(THETA, U, 'theta=alpha t/hbar') and U == 1, 'clock conversion')
    template = pre['mandatory_sentence_template']
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])

    # -------------------------------------------------- item 1: F, C, norms
    shells_ok = all(shell_count(r) == shell_formula(r) for r in range(0, 31))
    normF_partial = 1 + sum((Q(shell_formula(r)) * F(r) for r in range(1, 41)), Q(0))
    normF_up = normF_partial + Q(6, 41)           # sum_{r>40} 6(1+r)^-2 <= 6/41
    shell_bound = all(4 * r * r + 2 <= 6 * (r + 1) ** 2 and 4 * r * r + 2 <= 4 * (r + 1) ** 2 for r in range(0, 400))
    half_ok = all((1 + Q(d)) ** 4 <= 16 * (1 + Q(d, 2)) ** 4 for d in range(0, 200))
    conv_samples = {}
    box = [(x, y, z) for x in range(-6, 7) for y in range(-6, 7) for z in range(-6, 7)]
    for y in ((0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0), (2, 2, 1)):
        d = l1(ORIGIN, y)
        conv_samples[str(y)] = sum((F(l1(ORIGIN, z)) * F(l1(z, y)) for z in box), Q(0)) / F(d)
    C_up = 32 * 7
    check('item1_F_convolution_constants', shells_ok and normF_up <= 7 and shell_bound and half_ok and C_up == P['C'] == 224
          and all(v <= C_up for v in conv_samples.values()),
          F='F(r)=(1+r)^-4 on the coarse l1 metric (non-increasing, positive)',
          shell_counts='#{y: |y|_1=r} = 4r^2+2 (r>=1), enumerated for r<=30',
          norm_F_upper=exact(normF_up), norm_F_bound='||F||<=1+6 sum_{k>=2}k^-2<=7',
          convolution='either d(x,z)>=d/2 or d(z,y)>=d/2; F(d/2)<=16F(d); C<=32||F||<=224',
          finite_window_convolution_samples={k: sci(v, 8) for k, v in conv_samples.items()},
          note='samples are finite-window partial sums (previews of the supremum, not used to decide C)')

    i1_text = (INPUTS / I1_REL).read_text()
    parsed_rows, derived_rows = parse_i1_table(i1_text), derive_i1_table()
    must(parsed_rows == derived_rows and len(derived_rows) == 24, 'I1 table differs from its derivation')
    classes = [r for r in derived_rows if r[4] == 'omitted']
    must(len(classes) == 21, 'omitted classes')

    def faces_through(u):
        out = {}
        for k, cls in enumerate(classes):
            for dv in cls[3]:
                b = vsub(u, dv)
                out[(b, k)] = owners_of(b, cls)
        return out

    at0, atz = faces_through(ORIGIN), faces_through(EZ)
    derived_pins = {'faces_per_factor': len(at0), 'owner_sets_per_factor': len(set(at0.values())),
                    'faces_meeting_R': len(set(at0) | set(atz)),
                    'faces_inside_R': sum(1 for ow in at0.values() if ow == COVER)}
    far = (3, -2, 5)
    covariant = len(faces_through(far)) == 49 and len(set(faces_through(far).values())) == 15
    for (b, k) in list(at0)[:5]:
        class_face_links(b, classes[k])
    both = sum(1 for key in at0 if key in atz)
    check('i1_table_parsed_and_rederived', derived_pins == P['pins'] and covariant and both == 16
          and certify_face_pins(dict(derived_pins, provenance='derived from the I1 table by translation covariance'), derived_pins),
          pins=derived_pins, faces_containing_both_sites_of_R=both, translation_covariance_checked_at=str(far),
          support_sizes={'two_site': sum(1 for c in classes if len(c[3]) == 2), 'three_site': sum(1 for c in classes if len(c[3]) == 3)})

    # interaction norms (48): per-site sums and the l1 diameter-2 placement
    J_star = Q(4 * 7)
    J_face = Q(derived_pins['faces_per_factor'], 3)
    diam_ok = all(max(l1(a, b) for a in cls[3] for b in cls[3]) <= 2 for cls in classes) and \
        max(l1(a, b) for a in STAR for b in STAR) == 2
    norm_phi = (1 / F(2)) * J_star
    norm_phi_prime = (1 / F(2)) * J_face
    # labelled exact (48)-norms by pair enumeration (not used in any constant)
    pair_face, pair_star = {}, {}
    for ow in at0.values():
        for y in ow:
            pair_face[y] = pair_face.get(y, 0) + 1
    for b in [vsub(ORIGIN, s) for s in STAR]:
        for y in (vadd(b, s) for s in STAR):
            pair_star[y] = pair_star.get(y, 0) + 1
    sharp_face = max(Q(n, 3) / F(l1(ORIGIN, y)) for y, n in pair_face.items())
    sharp_star = max(Q(7 * n) / F(l1(ORIGIN, y)) for y, n in pair_star.items())
    check('item1_interaction_norms_Phi_and_Phi_prime',
          diam_ok and norm_phi == P['phi_norm'] == 2268 and P['phi_factor'] == 81 and norm_phi_prime == P['phi_prime_norm'] == 1323
          and certify_incoming(J_star, 4, 7),
          whole_star={'J_per_tau': qs(J_star), 'norm_F_per_tau': qs(norm_phi), 'derivation': '4 incident stars x 7|tau|; F(2)^-1=81'},
          owner_set={'per_site_per_tau': qs(J_face), 'norm_F_per_tau': qs(norm_phi_prime),
                     'derivation': "Phi'(M)=-(tau/3) sum_{M_f=M} W_f; 49 faces through a site (15 owner sets); 81*49/3=1323"},
          labelled_exact_48_norms_not_used={'owner_set_per_tau': qs(sharp_face), 'whole_star_per_tau': qs(sharp_star),
                                            'note': 'pair enumeration; upper bounds 1323 and 2268 are the contract constants used everywhere'})

    quotes = ns_quote_lines(ns_text)
    report_text = REPORT.read_text()
    check('item1_ns_quotation_verbatim', certify_quotes(report_text, quotes, NS_REL), quoted_passages=len(quotes),
          source=NS_REL, pdf_sha256=NS_PDF_SHA256,
          placement={'H_x': 'h_b (normalized, unbounded, self-adjoint, compact resolvent) in the on-site slot of (44)',
                     'Phi(X)': 'whole stars b+S (F1) or owner sets M (F2), bounded self-adjoint Wilson sums',
                     'native_restriction': 'H^{F1}_N = sum h_b + sum_{X in Lambda_N} Phi(X); H^{(2)}_N = sum h_b + sum_{M in Lambda_N} Phi\'(M)',
                     'time': 'NS t is the normalized time u=theta/8'})
    ladder = {str(L): {'norm_h_L': L, 'wrong_norm_F_lower': L, 'wrong_velocity_lower': 2 * L * 224} for L in (1, 10, 100, 1000)}
    placement = {'onsite_in_interaction': False, 'lr_applied_to': 'native restriction with H_x unbounded on-site',
                 'interaction_norm_cutoff_independent': True}
    check('item1_onsite_placement_interaction_picture', certify_onsite_placement(placement), placement=placement,
          wrong_placement_ladder_fixture=ladder,
          note='h_b enters no constant: Theorem 3.1 handles it by the interaction picture; placing a cutoff h_L=diag(0..L) '
               'inside Phi gives ||Phi||_F>=L, unbounded in the cutoff')

    # -------------------------------------------------- item 2: extra faces
    enum = {}
    for N in (2, 3):
        e = enumerate_box(N, classes)
        must(e['count'] == 28 * N * (5 * N + 1) and e['f1_subset_f2'] and e['anchors_on_layer'] and e['owners_on_plane']
             and e['owners_on_layer'] and e['min_dist_0'] == N and e['min_dist_e_z'] == N - 1 and e['max_owners'] == 3
             and e['disjoint_from_R'] and e['charged_once'] and e['f1_is_whole_star_native'] and e['f2_is_owner_set_native']
             and e['anchor_faces'] == {'one_plane': 140 * N * N, 'two_plane': 28 * N, 'three_plane': 0}
             and e['meeting_R_f1'] == e['meeting_R_f2'] == 82 and e['padding_sites'] == 3 * (2 * N + 1) ** 2
             and not e['padding_touched'] and e['max_faces_per_site'] == 49 and e['max_stars_per_site'] == 4,
             'enumeration identity failed at N=' + str(N))
        enum[N] = e
    counts = {}
    for N in range(2, 7):
        f1n, f2n = len(f1_faces(N, classes)), len(f2_faces(N, classes))
        counts[str(N)] = {'F1': f1n, 'F2': f2n, 'extra': f2n - f1n}
        must(f1n == 168 * N ** 3 and f2n == 28 * N * (2 * N + 1) * (3 * N + 1) and f2n - f1n == 28 * N * (5 * N + 1), 'count formula')
    per_plane = {}
    for i, name in ((0, 'x'), (1, 'y'), (2, 'z')):
        per_plane[name] = sum(1 for c in classes if all(v[i] == 0 for v in c[3]))
    per_edge = {}
    for k, name in ((2, 'xy planes: support in {0,e_z}'), (1, 'xz planes: support in {0,e_y}'), (0, 'yz planes: support in {0,e_x}')):
        per_edge[name] = sum(1 for c in classes if all(v[j] == 0 for v in c[3] for j in range(3) if j != k))
    all_size = (per_plane == {'x': 17, 'y': 13, 'z': 5} and sum(per_edge.values()) == 14
                and all(4 * N * N * 35 + 2 * N * 14 == 28 * N * (5 * N + 1) for N in range(2, 50)))
    check('item2_extra_faces_enumerated_and_all_size',
          all_size and all(enum[N]['count'] == 28 * N * (5 * N + 1) for N in (2, 3)),
          enumerated={str(N): {k: enum[N][k] for k in ('count', 'f1_count', 'f2_count', 'min_dist_0', 'min_dist_e_z',
                                                         'max_owners', 'partial_groups', 'anchor_faces', 'padding_sites',
                                                         'B_plus_sites', 'meeting_R_f1', 'meeting_R_f2')} for N in (2, 3)},
          counts_N2_to_6=counts,
          all_size_argument='an extra face has anchor b in Lambda_N with b+S not inside Lambda_N, so b_i=N for some i, and its '
                            'support avoids e_i; anchors with exactly one b_i=N: 3 planes x (2N)^2 anchors x (17+13+5)/3 classes '
                            '-> 4N^2*35; exactly two: 3 edges x 2N anchors -> 2N*(10+3+1); three: none -> 140N^2+28N=28N(5N+1)',
          classes_avoiding_e_i=per_plane, classes_on_edges=per_edge,
          distance='every owner o has o_i=N on the plane of its anchor, so |o|_1>=N and |o-e_z|_1>=N-1 (attained at (0,0,N))',
          fine_units_reading='tail blocks of an owner on the z-plane are N-1 fine steps from T_{e_z} (4N-3 on the x-plane, '
                             '2N-1 on the y-plane); informational only, no constant uses a fine distance',
          charged_once='each extra face is one (anchor, class) pair, charged once as -(tau/3)W_f')

    fx = padding_factorization_fixture()
    check('item2_padding_factorization',
          fx['factorizes'] and fx['tensor_product_unitary'] and fx['padding_commutes'] and fx['evolved_A_is_minus_A'] and fx['U2_is_iXX']
          and all(not enum[N]['padding_touched'] for N in (2, 3)),
          statement='H^{F2,pad}_N = H^(2)_N (x) 1 + 1 (x) sum_{x in B_+ minus Lambda_N} h_x; e^{iuH^pad} = e^{iuH^(2)} (x) e^{iuP}; '
                    'so T^{F2,pad}(A (x) 1) = T^(2)(A) (x) 1 exactly and the padding never enters the Duhamel source',
          padding_sites={str(N): enum[N]['padding_sites'] for N in (2, 3)},
          exact_fixture={k: v for k, v in fx.items()})

    # -------------------------------------------------- item 3: comparison
    LR_F2 = {'tier': TIER, 'F': '(1+r)^-4', 'inner_family': 'F2', 'interaction': PHI_PRIME, 'norm_F_per_tau': '1323',
             'C': '224', 'onsite_placement': ONSITE_SLOT, 'native_restriction': True}
    LR_F1 = {'tier': TIER, 'F': '(1+r)^-4', 'inner_family': 'F1', 'interaction': PHI, 'norm_F_per_tau': '2268',
             'C': '224', 'onsite_placement': ONSITE_SLOT, 'native_restriction': True}
    SRC_CMP = {'terms': 'extra F2 faces: owner set inside Lambda_N, anchor star not inside Lambda_N', 'padding_charged': False,
               'old_terms_charged': False, 'combine': 'linear', 'per_face_norm_per_tau': '1/3', 'owners_max': '3',
               'count_formula': '28N(5N+1)', 'dist_e_z': 'N-1', 'dist_0': 'N', 'geometry_coefficient': '168'}
    SRC_F1 = {'family': 'F1', 'terms': 'new terms X inside Lambda_M, not inside Lambda_N',
              'route': 'sup over M greater than N, one Duhamel between Lambda_N and Lambda_M', 'combine': 'linear',
              'incoming_included': True, 'per_site_per_tau': '28', 'tail_coefficient': '8', 'rate': '1/(N-1)'}
    SRC_F2 = dict(SRC_F1, family='F2', per_site_per_tau='49/3', charge='face by face through owner sets')
    K_cmp = comparison_value(LR_F2, SRC_CMP, TAU, U, enum)
    K_cmp_neg = comparison_value(LR_F2, SRC_CMP, -TAU, U, enum)
    x_f2 = 2 * 1323 * 224 * TAU * U
    x_f1 = 2 * 2268 * 224 * TAU * U
    e_lo, e_hi = exp_bounds(x_f2)
    E_true_lo = 2 * (e_lo - 1 - x_f2) / (x_f2 * x_f2)
    E_true_hi = 2 * (e_hi - 1 - x_f2) / (x_f2 * x_f2)
    geom_ok = all(84 * N * (5 * N + 1) * (Q(1, N ** 4) + Q(1, (N + 1) ** 4)) <= 168 * Q(5 * N + 1, N ** 3) for N in range(2, 200))
    b = {str(N): exact(K_cmp * Q(5 * N + 1, N ** 3)) for N in (2, 3, 10, 100)}
    sharper = {}
    for N in (2, 3):
        s = lr_prefactor(1323 * TAU, 224, U) * (TAU / 3) * enum[N]['exact_sum']
        bound = K_cmp * Q(5 * N + 1, N ** 3)
        must(s <= bound and enum[N]['exact_sum'] <= 84 * N * (5 * N + 1) * (Q(1, N ** 4) + Q(1, (N + 1) ** 4)), 'sharper sum')
        sharper[str(N)] = {'exact_boundary_sum': exact(enum[N]['exact_sum']), 'labelled_comparison_value': exact(s),
                           'all_size_bound_value': exact(bound)}
    cmp_admitted = K_cmp <= P['target_comparison'] and K_cmp_neg == K_cmp
    check('item3_duhamel_comparison_inner_F2', cmp_admitted and geom_ok and E_true_lo <= E_up(x_f2) and E_true_hi <= E_up(x_f2) + Q(1, 10 ** 20)
          and K_cmp == 148176 * TAU * TAU * U * U * E_up(x_f2),
          formula='||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| <= sum_{f in E_N} int_0^U ||[v_f, tau^{(2),N}_s(A)]|| ds '
                  '<= 2||Phi\'||_F U^2 E(x) (|tau|/3) sum_f D(R,M_f) <= 148176 tau^2 U^2 E_up(x) (5N+1) N^-3 ||A||',
          x='2*1323*224*|tau|*U', E_up='1+x/3+x^2/(12(1-x/5))', E_enclosure_from_exp=[sci(E_true_lo, 15), sci(E_true_hi, 15)],
          K_cmp=exact(K_cmp), K_cmp_minus_tau=exact(K_cmp_neg), target=qs(P['target_comparison']),
          margin=sci(P['target_comparison'] / K_cmp, 8), b_N=b, labelled_sharper_enumerated=sharper,
          lr_record=LR_F2, source_record=SRC_CMP)
    # first order: at tau=0 the on-site evolution keeps A in B(H_R); extra faces never meet R
    coeffs = [K_cmp / (TAU * TAU)] + [comparison_value(LR_F2, SRC_CMP, TAU / 10 ** j, U, enum) / (TAU / 10 ** j) ** 2 for j in (2, 4)]
    linear_coeff = [comparison_value(LR_F2, SRC_CMP, TAU / 10 ** j, U, enum) / (TAU / 10 ** j) for j in (0, 2, 4)]
    check('item3_first_order_vanishes_quadratic_in_tau',
          all(enum[N]['disjoint_from_R'] for N in (2, 3)) and coeffs[0] > coeffs[1] > coeffs[2] > 148176
          and linear_coeff[0] > linear_coeff[1] > linear_coeff[2],
          reason='first-order term i int tau^0_s([V, tau^0_{u-s}(A)]) ds with the on-site (tau=0) dynamics: tau^0 maps B(H_R) '
                 'to itself and every extra face has owners at l1 distance >=N-1>=1 from R, so the commutator vanishes; '
                 'in the bound, e^{vs}-1=O(|tau|s) times ||v_f||=|tau|/3 gives tau^2 U^2',
          tau_squared_coefficients=[sci(c, 10) for c in coeffs], limit_coefficient='148176',
          linear_coefficients_to_zero=[sci(c, 6) for c in linear_coeff])

    # -------------------------------------------------- item 4: Cauchy, limits, identification, O6
    c1 = cauchy_value(LR_F1, SRC_F1, TAU, U)
    c2 = cauchy_value(LR_F2, SRC_F2, TAU, U)
    tails_ok = all(tail_partial(m, 400) <= tail_upper(m) for m in range(1, 21))
    witnesses = []
    for j in range(1, 9):
        m = 2 ** j
        s = tail_partial(m, m)
        witnesses.append((m, s))
    wit_ok = all(m * s >= Q(1, 2) for m, s in witnesses)
    # enumerated sources Lambda_2 -> Lambda_3
    st2, st3 = whole_stars(2), whole_stars(3)
    new_stars = {bb: pts for bb, pts in st3.items() if bb not in st2}
    f2_2, f2_3 = enum[2]['f2'], enum[3]['f2']
    new_faces = {k: v for k, v in f2_3.items() if k not in f2_2}
    stars_far = all(linf(p) >= 2 for pts in new_stars.values() for p in pts) and all(p not in COVER for pts in new_stars.values() for p in pts)
    faces_far = all(linf(o) >= 2 for ow in new_faces.values() for o in ow) and all(o not in COVER for ow in new_faces.values() for o in ow)
    sum_f1 = sum((7 * F(l1(p, x)) for pts in new_stars.values() for p in pts for x in COVER), Q(0))
    sum_f2 = sum((Q(1, 3) * F(l1(o, x)) for ow in new_faces.values() for o in ow for x in COVER), Q(0))
    new_terms_ok = all(any(linf(p) > 2 for p in pts) for pts in new_stars.values()) and \
        all(any(linf(o) > 2 for o in ow) for ow in new_faces.values())
    grown = {bb for (bb, _k) in new_faces if bb in set(box_sites(2))}
    old_in_grown = sum(1 for (bb, _k) in f2_2 if bb in grown)
    check('item4_cauchy_sources_and_tails',
          tails_ok and wit_ok and stars_far and faces_far and new_terms_ok and len(new_stars) == 6 ** 3 - 4 ** 3
          and len(new_faces) == 5880 - 1960 and sum_f1 <= 28 * (tail_upper(2) + tail_upper(1)) and sum_f2 <= Q(49, 3) * (tail_upper(2) + tail_upper(1))
          and 28 * (tail_upper(2) + tail_upper(1)) <= 28 * 8,
          tail='T(m)=sum_{r>=m}(4r^2+2)(1+r)^-4 <= 4 sum_{k>=m+1}k^-2 <= 4/m; new terms have every point at sup-norm >=N, '
               'so |y|_1>=N from 0 and |y-e_z|_1>=N-1: source sum <= J(4/N+4/(N-1)) <= 8J/(N-1)',
          polynomial_lower_witnesses={str(m): sci(m * s, 8) for m, s in witnesses},
          enumerated_N2_to_N3={'F1_new_stars': len(new_stars), 'F2_new_faces': len(new_faces),
                               'F1_source_sum_per_tau': exact(sum_f1), 'F2_source_sum_per_tau': exact(sum_f2),
                               'F2_grown_old_anchors': len(grown), 'F2_old_faces_in_grown_groups': old_in_grown})
    check('item4_cauchy_F1_own_limit', c1 <= P['target_cauchy'] and c1 == 1016064 * TAU * TAU * U * U * E_up(x_f1)
          and cauchy_value(LR_F1, SRC_F1, -TAU, U) == c1,
          formula='sup_{M>N} ||T^{F1,M}_theta(A)-T^{F1,N}_theta(A)|| <= 2||Phi||_F U^2 E(x) J 8/(N-1) = 1016064 tau^2 U^2 E_up(x)/(N-1)',
          x='2*2268*224*|tau|*U', c1=exact(c1), target=qs(P['target_cauchy']), margin=sci(P['target_cauchy'] / c1, 8),
          lr_record=LR_F1, source_record=SRC_F1)
    check('item4_cauchy_F2_own_limit', c2 <= P['target_cauchy'] and c2 == 345744 * TAU * TAU * U * U * E_up(x_f2)
          and cauchy_value(LR_F2, SRC_F2, -TAU, U) == c2,
          formula="sup_{M>N} ||T^{F2,M}_theta(A)-T^{F2,N}_theta(A)|| <= 2||Phi'||_F U^2 E(x) (49|tau|/3) 8/(N-1) = 345744 tau^2 U^2 E_up(x)/(N-1)",
          x='2*1323*224*|tau|*U', c2=exact(c2), target=qs(P['target_cauchy']), margin=sci(P['target_cauchy'] / c2, 8),
          lr_record=LR_F2, source_record=SRC_F2)
    tri = {str(N): {'triangle_through_limits': exact((c1 + c2) / (N - 1)),
                    'comparison_target': exact(P['target_comparison'] * Q(5 * N + 1, N ** 3))} for N in (2, 1000)}
    tri_fails = all((c1 + c2) / (N - 1) > P['target_comparison'] * Q(5 * N + 1, N ** 3) for N in (2, 1000))
    genX = {}
    base = lr_prefactor(1323 * TAU, 224, U) * (TAU / 3)
    for N in (10, 100, 1000):
        genX[str(N)] = exact(base * 28 * N * (5 * N + 1) * 3 * 27 * F(N - 1))
    genX_decreasing = Q(genX['10']['exact']) > Q(genX['100']['exact']) > Q(genX['1000']['exact'])
    ident = {'source': 'comparison bound b(N) -> 0 along the whole sequence', 'sequence': 'whole sequence', 'general_local_X': True}
    check('item4_limit_identification', certify_identification(ident) and tri_fails and genX_decreasing,
          statement='T^{F2}_theta(A) := lim_N T^{F2,N}_theta(A) exists (Theorem 4.1 for Phi\'; quantitatively c2/(N-1) on B(H_R)) '
                    'and equals the AQ1 limit T_theta(A) = lim_N T^{F1,N}_theta(A) because ||T^{F2,N}-T^{F1,N}||<=b(N)->0; '
                    'for A in A_X, X inside Lambda_{N0}, the same Duhamel bound with d>=N-N0 gives '
                    'b_X(N) <= 882 tau^2 U^2 E |X| 84 N(5N+1) (1+N-N0)^-4 -> 0, so the two automorphism groups agree on the '
                    'local algebra and hence on its norm closure',
          general_X_example_Lambda_1={'X_sites': 27, 'N0': 1, 'b_X': genX},
          limit_bounds={'F1': '||T_theta(A)-T^{F1,N}_theta(A)|| <= c1/(N-1)', 'F2': '||T_theta(A)-T^{F2,N}_theta(A)|| <= c2/(N-1)'},
          labelled_weaker_triangle_bound=tri, triangle_meets_comparison_target=False)
    L_vals = {str(L): exact(2 * c2 / (L - 1)) for L in (10, 100, 1000)}
    O6 = {step: {'status': 'rerun', 'subsequence': 'F2 own subsequence', 'dynamics': 'AQ1 T_theta, identified with the F2 limit'}
          for step in ('stationarity', 'gns_strong_continuity', 'nonnegative_generator', 'gauge_physical_restriction')}
    w0, w1 = algebraic_not_gns_fixture()
    check('item4_O6_rerun_for_F2_limit_states', certify_o6(O6) and w0 == CI and w1 == (Q(0), Q(-1)),
          o6=O6, stationarity_error_bound_2c2_over_L_minus_1=L_vals,
          stationarity='omega_N(T^{F2,N}(A))=omega_N(A) (simple F2 ground, AY1); replace T^{F2,N} by T^{F2,L} (fixed region '
                       'Lambda_L, error c2/(L-1) for every N>L), pass the F2 subsequence N_k in local trace norm, then '
                       '|omega(T_theta(A))-omega(A)| <= 2c2/(L-1) -> 0; general local A by Theorem 4.1 for Phi\'',
          gns='U_theta pi(A)Omega = pi(T_theta(A))Omega; theta -> omega(A* T^{F2,L}_theta(A)) is continuous (normal rho_L, '
              'strongly continuous finite unitary group); uniform approximation on the window passes continuity to omega(A*T_theta(A)); '
              '||(U_theta-1)pi(A)Omega||^2 = 2omega(A*A)-2Re omega(A*T_theta(A)) -> 0; Stone: U_theta = exp(i theta G), G=H/alpha',
          generator='c_N(theta)=<A Omega_N, e^{i theta (G_N-E_N)} A Omega_N> has spectral support in [0,inf); c_{N_k}(theta)->c(theta) '
                    'pointwise (the Duhamel bounds hold on every compact window with U=Theta/8); f in C_c^inf((-inf,0)), f>=0: '
                    'int f dnu_N=0 passes by dominated convergence; the negative spectral projection of G vanishes on the dense '
                    'local cyclic vectors, so G>=0',
          gauge='every retained F2 term is a Wilson loop or an on-site Casimir, the F2 ground is simple hence gauge invariant; '
                'T_theta preserves the gauge-invariant algebra; the physical cyclic space reduces U_theta',
          different_states_same_dynamics_fixture={'omega_0(A tau(A))': 'i', 'omega_1(A tau(A))': '-i',
                                                  'model': 'H=diag(0,1), A=sigma_x, u=pi/2 (exact Gaussian rationals)'})

    # -------------------------------------------------- item 6: scaling
    def ratio(fn):
        return fn(TAU) / fn(TAU / 100)
    r_cmp = ratio(lambda t: comparison_value(LR_F2, SRC_CMP, t, U, enum))
    r_c1 = ratio(lambda t: cauchy_value(LR_F1, SRC_F1, t, U))
    r_c2 = ratio(lambda t: cauchy_value(LR_F2, SRC_F2, t, U))
    check('item6_tau_scaling_per_constant',
          certify_scaling(r_cmp, P['bracket_comparison']) and certify_scaling(r_c1, P['bracket_cauchy'])
          and certify_scaling(r_c2, P['bracket_cauchy']) and certify_order_label('quadratic', r_cmp, P['bracket_quadratic']),
          ratios={'comparison_coefficient': exact(r_cmp), 'cauchy_coefficient_F1': exact(r_c1), 'cauchy_coefficient_F2': exact(r_c2)},
          brackets={'comparison_coefficient': [qs(v) for v in P['bracket_comparison']], 'cauchy_coefficient': [qs(v) for v in P['bracket_cauchy']],
                    'duhamel_tau_order_quadratic': [qs(v) for v in P['bracket_quadratic']]},
          rule='same exact rational formula at tau and tau/100, no intermediate rounding')
    U_growth = {str(u): exact(comparison_value(LR_F2, SRC_CMP, TAU, Q(u), enum) / K_cmp) for u in (2, 10)}
    return locals()


def run_controls(c):
    raw, contract, P, enum, TAU, U, THETA = c['raw'], c['contract'], c['P'], c['enum'], c['TAU'], c['U'], c['THETA']
    LR_F1, LR_F2, SRC_CMP, SRC_F1, SRC_F2 = c['LR_F1'], c['LR_F2'], c['SRC_CMP'], c['SRC_F1'], c['SRC_F2']
    report_text, template, forbidden, quotes = c['report_text'], c['template'], c['forbidden'], c['quotes']
    files, classes = c['files'], c['classes']
    pre = contract['preregistration']

    def rebound(edit):
        t = tamper(raw, edit)
        return lambda: validate_contract_bytes(t, sha256_bytes(t))

    def drop_control(d):
        d['controls'].remove('root_n_misuse')
        d['preregistration']['controls_required']['ids'].remove('root_n_misuse')
        del d['new_control_semantics']['root_n_misuse']

    def loosen_target(d):
        t = d['parameters']['targets']
        t['comparison'] = t['comparison'].replace('6x10^-11', '6x10^-9')
        d['preregistration']['target']['value'] = d['preregistration']['target']['value'].replace('6x10^-11', '6x10^-9')

    def drop_premise(d):
        d['shared_premises'].remove('research/round29/skeptic/aq1.md')
    dropped = tamper(raw, drop_premise)
    files_dropped = [f for f in files if f != 'research/round29/skeptic/aq1.md']
    gate_rel = 'research/round32/advisor/ay2-gate.json'
    gate_bytes = (INPUTS / gate_rel).read_bytes()
    ns_bytes = (INPUTS / NS_REL).read_bytes()
    control('coherent_evidence_tampering', [
        ('isolation_flag_flipped_rehashed', rebound(lambda d: d.__setitem__('reverse_premise_isolation', False))),
        ('control_removed_rehashed', rebound(drop_control)),
        ('gate_field_flipped_rehashed', rebound(lambda d: d['preregistration']['gate_fields_required'].__setitem__('gns_dynamics_equality_claimed', True))),
        ('hash_binding_flag_flipped_rehashed', rebound(lambda d: d['preregistration']['hash_binding'].__setitem__('admitted_gate_sha256_pinned_in_check_py', False))),
        ('comparison_target_loosened_rehashed', rebound(loosen_target)),
        ('snapshot_removed_with_contract_line', lambda: validate_inventory(files_dropped, json.loads(dropped))),
        ('byte_change_without_rehash', lambda: validate_contract_bytes(raw + b' ', CONTRACT_SHA256)),
        ('pinned_gate_edited', lambda: certify_pinned(gate_rel, gate_bytes.replace(b'accepted_within_scope', b'limited', 1))),
        ('ns_excerpt_edited', lambda: certify_pinned(NS_REL, ns_bytes.replace('− 1) D(X, Y)'.encode(), ') D(X, Y)'.encode(), 1))),
    ])
    control('exact_arithmetic_admission', [
        ('float_tau', lambda: admit_bound(1.48e-11, P['target_comparison'])),
        ('bool_value', lambda: parse_q(True)),
        ('nan_string', lambda: parse_q('nan')),
        ('zero_denominator', lambda: parse_q('1/0')),
        ('float_target', lambda: admit_bound(c['K_cmp'], 6e-11)),
        ('decimal_preview_as_admission', lambda: admit_bound(sci(c['K_cmp']), P['target_comparison'])),
    ], admission='Fraction only; E(x) replaced by the rational upper bound E_up; previews are truncated strings never read')
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
        ('linf_metric', lambda: certify_model(dict(model, metric='l-infinity on the fine lattice'), TAU)),
        ('exponential_weights', lambda: certify_model(dict(model, weights='F(r)=e^{-mu r}(1+r)^-4'), TAU)),
        ('window_64', lambda: certify_model(dict(model, window_theta='64'), TAU)),
    ])
    facts = c['facts']
    missed = dict(facts, comparison=False)
    K_big = comparison_value(LR_F2, SRC_CMP, Q(1, 10 ** 7), U, enum)
    control('insufficient_verdict_retained', [
        ('missed_comparison_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', missed)),
        ('lr_not_applicable_relabelled_limited', lambda: certify_outcome('limited', dict(facts, lr_applies=False))),
        ('miscounted_source_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', dict(facts, source_counted=False))),
        ('o6_open_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', dict(facts, o6=False))),
        ('retuned_tau_to_pass', lambda: certify_model(dict(model, tau='1/1000000000'), TAU)),
    ], hypothetical_missed_example={'tau': '1/10000000', 'K_cmp': exact(K_big), 'meets_target': K_big <= P['target_comparison'],
                                    'rule_outcome': 'limited', 'dominating_term': 'duhamel_boundary_sum times the quadratic LR prefactor'})
    lin = naive_linear_bound(TAU, U, Q(1, 3)) / naive_linear_bound(TAU / 100, U, Q(1, 3))
    control('tau_scaling_exponent', [
        ('linear_order_bound', lambda: certify_scaling(lin, P['bracket_comparison'])),
        ('cubic_label', lambda: certify_scaling(c['r_cmp'] * 100, P['bracket_comparison'])),
        ('post_hoc_bracket', lambda: require((Q(10015), Q(10025)) == P['bracket_comparison'], 'bracket chosen after evaluation rejected')),
        ('cauchy_linear', lambda: certify_scaling(lin, P['bracket_cauchy'])),
    ], linear_ratio=qs(lin))
    control('wrong_delta_alpha_hbar_clock', [
        ('u_window_labelled_theta', lambda: certify_clock(THETA, THETA, 'theta=alpha t/hbar')),
        ('delta_clock_label', lambda: certify_clock(THETA, U, 'u=delta t/hbar')),
        ('one_eighth_window', lambda: certify_clock(THETA, Q(1, 8), 'theta=alpha t/hbar')),
        ('euclidean_clock', lambda: certify_clock(THETA, U, 's=alpha t_E/hbar')),
    ], conversion='u=delta t/hbar=theta/8 with delta=alpha/8; |theta|<=8 is |u|<=1')
    control('missing_incoming_stars', [
        ('outgoing_star_J', lambda: certify_incoming(7, 1, 7)),
        ('outgoing_star_norm_567', lambda: certify_lr_record(dict(LR_F1, norm_F_per_tau='567'))),
        ('f1_cauchy_outgoing_only', lambda: certify_cauchy_source(dict(SRC_F1, per_site_per_tau='7'))),
        ('f2_cauchy_anchored_faces_only', lambda: certify_cauchy_source(dict(SRC_F2, per_site_per_tau='7'))),
        ('incoming_flag_false', lambda: certify_cauchy_source(dict(SRC_F1, incoming_included=False))),
    ])
    control('root_n_misuse', [
        ('divide_by_sqrt_faces', lambda: divide_by_root(c['K_cmp'], 616)),
        ('rss_assembly', lambda: assemble_linear(['1', '1'], combine='rss')),
        ('comparison_root_N', lambda: certify_comparison_source(dict(SRC_CMP, combine='root_N'), enum)),
        ('cauchy_rss', lambda: certify_cauchy_source(dict(SRC_F2, combine='rss'))),
    ])
    control('tier_mixing_rejected', [
        ('exponential_tier_with_polynomial_F', lambda: certify_lr_record(dict(LR_F2, tier='exponential_lieb_robinson'))),
        ('tier_missing', lambda: certify_lr_record({k: v for k, v in LR_F2.items() if k != 'tier'})),
        ('F_mu_with_AQ1_constants', lambda: certify_lr_record(dict(LR_F2, F='e^{-mu r}(1+r)^-4'))),
        ('phi_constants_on_F2_inner', lambda: certify_lr_record(dict(LR_F2, interaction=PHI, norm_F_per_tau='2268'))),
    ])
    control('reverse_premise_isolation', [
        ('forward_ba2_report_added', lambda: validate_inventory(files + ['research/round33/forward/ba2/report.md'], contract)),
        ('skeptic_triage_added', lambda: validate_inventory(files + ['research/round33/skeptic/triage.md'], contract)),
        ('deliberation_added', lambda: validate_inventory(files + ['research/round33/advisor/deliberation-2.md'], contract)),
        ('lens_memo_added', lambda: validate_inventory(files + ['research/round33/experts/jung/memo.md'], contract)),
        ('ba1_reverse_added', lambda: validate_inventory(files + ['research/round33/reverse/ba1/report.md'], contract)),
        ('premise_removed', lambda: validate_inventory(files[1:], contract)),
    ])
    dp = c['derived_pins']
    control('face_count_all_sites', [
        ('literal_counts', lambda: certify_face_pins(dict(dp, provenance='literal'), dp)),
        ('site_0_anchored_only', lambda: certify_face_pins(dict(dp, provenance='derived from the I1 table by translation covariance', faces_per_factor=21), dp)),
        ('bound_84_as_count', lambda: certify_face_pins(dict(dp, provenance='derived from the I1 table by translation covariance', faces_meeting_R=84), dp)),
        ('inside_R_16', lambda: certify_face_pins(dict(dp, provenance='derived from the I1 table by translation covariance', faces_inside_R=16), dp)),
    ], derived=dp)
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
        ('contract_placeholder_rehashed', rebound(lambda d: d.__setitem__('selected_after', '<preceding gate>'))),
    ])
    control('negation_aware_phrase_scan', [
        ('affirmative_thermodynamic_limit', lambda: certify_phrasing(report_text + '\nThe thermodynamic limit exists.', forbidden, template)),
        ('affirmative_predicts', lambda: certify_phrasing(report_text + '\nThis predicts the gap.', forbidden, template)),
        ('affirmative_unique_limit', lambda: certify_phrasing(report_text + '\nWe obtain the unique limit.', forbidden, template)),
        ('affirmative_aq_state', lambda: certify_phrasing(report_text + '\nThe AQ state is reached.', forbidden, template)),
    ], negated_positive_control=certify_phrasing('This is not the thermodynamic limit.', forbidden, template))
    control('parameters_declare_metric_weights_window', [
        ('metric_removed', rebound(lambda d: d['parameters'].pop('metric'))),
        ('weights_removed', rebound(lambda d: d['parameters'].pop('weights'))),
        ('window_removed', rebound(lambda d: d['parameters'].pop('window'))),
        ('clock_removed', rebound(lambda d: d['preregistration'].pop('clock'))),
    ], declared={'metric': 'parameters.metric', 'weights': 'parameters.weights', 'window': 'parameters.window',
                 'clock': 'preregistration.clock', 'N_0': 'targets text (N at least 2)', 'd_X': 'not declared (no exponential target)'})
    rate = c['rate_rec']
    control('lieb_robinson_polynomial_tail', [
        ('comparison_N_minus_4', lambda: certify_rate_claim(dict(rate, comparison_exponent=4))),
        ('cauchy_N_minus_2_from_steps', lambda: certify_rate_claim(dict(rate, cauchy_exponent=2))),
        ('exponential_rate', lambda: certify_rate_claim(dict(rate, decay='exponential'))),
        ('n_to_n_plus_1_as_cauchy', lambda: certify_cauchy_claim('N_to_N_plus_1')),
        ('exponential_q_half', lambda: certify_decay_claim({'decay': 'exponential', 'C0': '1', 'q': '1/2'}, c['witnesses'])),
    ])
    inst = {'label': 'exponential_lieb_robinson', 'admission_weight': False, 'mu': '1/10',
            'norm_factor': 'e^{2 mu} 81 J', 'C_source': 'own C_{F_mu}<=224'}
    must(certify_exponential_instance(inst), 'instance rule')
    control('lieb_robinson_F_declared', [
        ('F_mu_with_AQ1_norm', lambda: certify_exponential_instance(dict(inst, norm_factor='81 J'))),
        ('F_mu_with_AQ1_C_unstated', lambda: certify_exponential_instance(dict(inst, C_source='AQ1 C=224'))),
        ('unlabelled_instance', lambda: certify_exponential_instance(dict(inst, label='polynomial_lieb_robinson'))),
        ('instance_with_admission_weight', lambda: certify_exponential_instance(dict(inst, admission_weight=True))),
    ], note='no exponential instance is produced in this loop; the rule is enforced for any such instance')
    para = report_text.replace(quotes[6], '‖[τ_t(A), B]‖ ≤ 2‖A‖‖B‖ e^{v|t|} D(X, Y)')
    control('lieb_robinson_form_quoted', [
        ('second_hand_source_aq1', lambda: certify_quotes(report_text, quotes, AQ1_REL)),
        ('paraphrased_51', lambda: certify_quotes(para, quotes, NS_REL)),
        ('rederived_constant_form', lambda: certify_quotes(report_text, quotes[:6] + ['‖[τ_t^Λ(A), B]‖ ≤ (2‖A‖‖B‖/C) e^{2‖Φ‖C|t|} D(X, Y)'], NS_REL)),
    ])
    pl = c['placement']
    control('unbounded_onsite_interaction_picture', [
        ('onsite_inside_Phi', lambda: certify_onsite_placement(dict(pl, onsite_in_interaction=True))),
        ('bounded_LR_on_full_hamiltonian', lambda: certify_onsite_placement(dict(pl, lr_applied_to='full Hamiltonian as a bounded interaction'))),
        ('cutoff_dependent_norm', lambda: certify_onsite_placement(dict(pl, interaction_norm_cutoff_independent=False))),
        ('lr_record_onsite_in_phi', lambda: certify_lr_record(dict(LR_F2, onsite_placement='h_b inside Phi as one-site terms'))),
    ], ladder=c['ladder'])
    control('duhamel_inner_family_constants', [
        ('f2_inner_with_phi_2268', lambda: certify_lr_record(dict(LR_F2, interaction=PHI, norm_F_per_tau='2268'))),
        ('f1_inner_with_phi_prime_1323', lambda: certify_lr_record(dict(LR_F1, interaction=PHI_PRIME, norm_F_per_tau='1323'))),
        ('inner_family_unnamed', lambda: certify_lr_record(dict(LR_F2, inner_family=None))),
        ('f2_cauchy_with_f1_inner', lambda: cauchy_value(LR_F1, SRC_F2, TAU, U)),
        ('not_native_restriction', lambda: certify_lr_record(dict(LR_F1, native_restriction=False))),
    ], witness=c['swap_witness'])
    bad_enum = {N: dict(enum[N], count=enum[N]['count'] - 28 * N) for N in (2, 3)}
    control('extra_face_count_and_distance', [
        ('count_140N2_formula', lambda: certify_comparison_source(dict(SRC_CMP, count_formula='140N^2'), enum)),
        ('edge_anchors_dropped', lambda: certify_comparison_source(SRC_CMP, bad_enum)),
        ('distance_N_from_e_z', lambda: certify_comparison_source(dict(SRC_CMP, dist_e_z='N'), enum)),
        ('two_owners_charged', lambda: certify_comparison_source(dict(SRC_CMP, owners_max='2'), enum)),
        ('padding_charged', lambda: certify_comparison_source(dict(SRC_CMP, padding_charged=True), enum)),
    ])
    control('duhamel_tau_order_quadratic', [
        ('linear_label', lambda: certify_order_label('linear', c['r_cmp'], P['bracket_quadratic'])),
        ('linear_formula_ratio', lambda: certify_order_label('quadratic', lin, P['bracket_quadratic'])),
    ], ratio=exact(c['r_cmp']))
    win = {'uniform_in_time': False, 'window': '|theta|<=8', 'U': '1'}
    must(certify_window_claim(win), 'window record')
    must(Q(c['U_growth']['2']['exact']) > 4 and Q(c['U_growth']['10']['exact']) > 100, 'bound grows faster than U^2')
    control('time_window_named_common_clock', [
        ('uniform_in_time', lambda: certify_window_claim(dict(win, uniform_in_time=True))),
        ('window_unnamed', lambda: certify_window_claim(dict(win, window=None))),
        ('U_equals_Theta', lambda: certify_window_claim(dict(win, U='8'))),
    ], growth_with_U=c['U_growth'])
    dl = {'level': 'algebraic_heisenberg_compact_window', 'gns_equality': False, 'correlation_equality': False}
    must(certify_dynamics_level(dl), 'dynamics level')
    control('algebraic_not_gns_dynamics', [
        ('gns_equality', lambda: certify_dynamics_level(dict(dl, gns_equality=True))),
        ('correlation_equality', lambda: certify_dynamics_level(dict(dl, correlation_equality=True))),
        ('gns_level', lambda: certify_dynamics_level(dict(dl, level='gns_dynamics'))),
    ], fixture='H=diag(0,1), A=sigma_x, u=pi/2: omega_0(A tau(A))=i, omega_1(A tau(A))=-i under one algebraic dynamics')
    ident, O6 = c['ident'], c['O6']
    control('f2_limit_dynamics_equals_f1', [
        ('identified_from_static_closeness', lambda: certify_identification(dict(ident, source='AY1 static closeness 2D'))),
        ('identified_along_subsequence', lambda: certify_identification(dict(ident, sequence='subsequence'))),
        ('R_only_identification', lambda: certify_identification(dict(ident, general_local_X=False))),
        ('stationarity_assumed', lambda: certify_o6(dict(O6, stationarity=dict(O6['stationarity'], status='assumed')))),
        ('f1_subsequence_used', lambda: certify_o6(dict(O6, nonnegative_generator=dict(O6['nonnegative_generator'], subsequence='F1 subsequence')))),
    ])
    f1set, f2set = set(enum[2]['f1']), set(enum[2]['f2'])
    control('two_families_named', [
        ('single_family', lambda: certify_families([F1_NAME])),
        ('all_boundary_conditions', lambda: certify_families(['all boundary conditions'])),
        ('f2_collapsed_onto_f1', lambda: certify_family_faces('F2', f1set, f1set, f2set)),
    ])
    control('subsequence_versus_whole_sequence', [
        ('states_whole_sequence_from_compactness', lambda: certify_limit_statement({'quantifier': 'whole sequence', 'from': 'compactness'})),
        ('unquantified_limit', lambda: certify_limit_statement({'quantifier': None})),
        ('dynamics_whole_sequence_from_subsequence', lambda: certify_limit_statement({'quantifier': 'whole sequence', 'from': 'diagonal extraction'})),
    ], statements={'dynamics': 'whole sequence (Cauchy bound)', 'states': 'subsequence (F2 own diagonal extraction)'})
    control('decay_rate_in_N_not_a', [
        ('converted_to_fm', lambda: certify_rate_units('decays like N^-2 per coarse step, i.e. like (Na)^-2 in fm')),
        ('correlation_length', lambda: certify_rate_units('a correlation length per coarse step')),
        ('rate_in_lattice_spacing', lambda: certify_rate_units('a rate in the lattice spacing per coarse step')),
        ('no_coarse_step', lambda: certify_rate_units('decays like N^-2')),
    ], accepted=c['rate_units_text'])
    sites2 = set(box_sites(2))
    ex2 = sorted(enum[2]['extra'].items())
    f1_face = sorted(enum[2]['f1'].items())[0]
    star_leaves = lambda t: not all(vadd(t[0][0], v) in sites2 for v in STAR)
    point_outside = lambda t: any(p not in sites2 for p in t[1])
    ns2 = sorted(c['new_stars'].items())
    inside_star = sorted(c['st2'].items())[0]
    must(certify_boundary_source(ex2, ex2, star_leaves) and certify_boundary_source(ns2, ns2, point_outside), 'source sets')
    control('boundary_source_new_terms_only', [
        ('old_f1_face_in_comparison_source', lambda: certify_boundary_source(ex2 + [f1_face], ex2, star_leaves)),
        ('comparison_source_short_one', lambda: certify_boundary_source(ex2[1:], ex2, star_leaves)),
        ('cauchy_old_star_in_source', lambda: certify_boundary_source(ns2 + [inside_star], ns2, point_outside)),
        ('cauchy_term_not_meeting_added_region', lambda: certify_boundary_source([inside_star], [inside_star], point_outside)),
    ], comparison_terms=len(ex2), cauchy_F1_new_stars_N2_to_N3=len(ns2))
    control('f2_regrouping_charged_once', [
        ('whole_group_recharge', lambda: certify_f2_charge(len(c['new_faces']) + c['old_in_grown'], len(c['new_faces']))),
        ('double_charge', lambda: certify_f2_charge(2 * len(c['new_faces']), len(c['new_faces']))),
        ('anchor_groups_as_source', lambda: certify_cauchy_source(dict(SRC_F2, charge='whole anchor groups'))),
    ], new_faces_N2_to_N3=len(c['new_faces']), old_faces_in_grown_groups=c['old_in_grown'])
    control('full_original_wilson_cover', [
        ('cover_zero_only', lambda: certify_cover((ORIGIN,), *cover_counts((ORIGIN,)))),
        ('four_drawn_links', lambda: certify_cover(COVER, 4, 4)),
        ('extra_factor', lambda: certify_cover((ORIGIN, EZ, (1, 0, 0)), *cover_counts((ORIGIN, EZ, (1, 0, 0))))),
    ], cover=str(COVER), links_endpoints=list(cover_counts(COVER)))
    topo = {'dynamics': DYNAMICS_TOPOLOGY, 'states': STATES_TOPOLOGY, 'time_continuity': GNS_TOPOLOGY}
    must(certify_topology(topo), 'topology record')
    shift = []
    for n in range(1, 41):
        # U(t)e_j=e^{ijt}e_j, A e_j=e_{2j}; at t=pi/n: (U A U* - A)e_n = (e^{i2nt}e^{-int}-1)e_{2n} = (i^4 conj(i^2)-1)e_{2n}
        coeff = cadd(cmul(ipow(4), cconj(ipow(2))), (Q(-1), Q(0)))
        shift.append(coeff == (Q(-2), Q(0)))
    control('topology_named', [
        ('norm_continuity_in_theta', lambda: certify_topology(dict(topo, time_continuity='norm continuity in theta on B(H_R)'))),
        ('weak_star_states', lambda: certify_topology(dict(topo, states='weak-* on finite-rank observables'))),
        ('one_topology', lambda: certify_topology(dict(topo, states=DYNAMICS_TOPOLOGY))),
    ], shift_witness_norm_2_for_n_up_to_40=all(shift), topologies=topo)
    control('cross_coupling_comparison_rejected', [
        ('plus_versus_minus_tau', lambda: certify_same_coupling(TAU, -TAU)),
        ('tau_versus_half_tau', lambda: certify_same_coupling(TAU, TAU / 2)),
    ], reason='at different couplings the Duhamel source contains all faces, including the 82 meeting R, and the difference is first order')
    gf, req, adm = c['gate_fields'], pre['gate_fields_required'], c['admitted']
    control('gate_fields_topic_specific', [
        ('field_missing', lambda: validate_gate_fields({k: v for k, v in gf.items() if k != 'common_limit_claimed'}, req, adm)),
        ('gns_equality_true', lambda: validate_gate_fields(dict(gf, gns_dynamics_equality_claimed=True), req, adm)),
        ('rate_true_with_missed_target', lambda: validate_gate_fields(gf, req, dict(adm, cauchy_F1=False))),
        ('generic_ay_fields', lambda: validate_gate_fields(dict({k: v for k, v in gf.items() if k != 'uniqueness_of_ground_state_claimed'}, uniqueness_claimed=False), req, adm)),
        ('scope_text_changed', lambda: validate_gate_fields(dict(gf, whole_sequence_scope='all states'), req, adm)),
    ])


def compute():
    c = positive_checks()
    contract, P, TAU = c['contract'], c['P'], c['TAU']
    pre = contract['preregistration']
    K_cmp, c1, c2 = c['K_cmp'], c['c1'], c['c2']
    admitted = {'comparison': K_cmp <= P['target_comparison'], 'cauchy_F1': c1 <= P['target_cauchy'],
                'cauchy_F2': c2 <= P['target_cauchy']}
    lr_applies = certify_lr_record(c['LR_F2']) and certify_lr_record(c['LR_F1']) and certify_onsite_placement(c['placement'])
    source_counted = all(c['enum'][N]['count'] == 28 * N * (5 * N + 1) for N in (2, 3))
    facts = {'lr_applies': lr_applies, 'source_counted': source_counted, 'comparison': admitted['comparison'],
             'cauchy_F1': admitted['cauchy_F1'], 'cauchy_F2': admitted['cauchy_F2'],
             'identified': certify_identification(c['ident']) and admitted['comparison'], 'o6': certify_o6(c['O6'])}
    if not (facts['lr_applies'] and facts['source_counted']):
        outcome = 'insufficient'
    elif all(facts[k] for k in ('comparison', 'cauchy_F1', 'cauchy_F2', 'identified', 'o6')):
        outcome = 'accepted_within_scope'
    else:
        outcome = 'limited'
    must(certify_outcome(outcome, facts), 'outcome rule')
    req = pre['gate_fields_required']
    gate_fields = {}
    for k in GATE_FIELD_NAMES:
        v = req[k]
        if k in TRUE_IF_ADMITTED:
            v = all(admitted.get(n) is True for n in TRUE_IF_ADMITTED[k])
        gate_fields[k] = v
    must(validate_gate_fields(gate_fields, req, admitted), 'gate fields')
    flags = {'continuum_claim': False, 'uniqueness_of_ground_state_claimed': False, 'gns_dynamics_equality_claimed': False,
             'uniform_in_time_claimed': False, 'rate_in_a_claimed': False, 'scientific_priority_verified': False,
             'weak_coupling_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False}
    must(validate_claim_flags(flags), 'claim flags')
    model_rec = {'model_id': 'AQ_patterned_zero_selected', 'tau': qs(TAU), 'triple': ['0', '0', '0'], 'group': 'SU(2)',
                 'dimension': 3, 'families': [F1_NAME, F2_NAME], 'metric': 'l1 on the coarse Z^3 factor lattice',
                 'weights': 'F(r)=(1+r)^-4', 'window_theta': '8', 'finite_graph': False, 'uniform_model': False}
    rate_rec = {'decay': 'polynomial', 'comparison_exponent': 2, 'cauchy_exponent': 1, 'in': 'N at fixed spacing'}
    uniformity_text = 'every constant is uniform in N at fixed spacing and fixed tau; nothing is uniform in the spacing'
    rate_units_text = 'N^-2 and 1/N per coarse step at fixed spacing and strong bare coupling; a coarse step is (4a,2a,a)'
    must(certify_model(model_rec, TAU) and certify_rate_claim(rate_rec) and certify_rate_units(rate_units_text)
         and certify_families(model_rec['families']) and certify_limit_statement({'quantifier': 'whole sequence', 'from': 'Cauchy bound'})
         and certify_limit_statement({'quantifier': 'subsequence'}) and certify_same_coupling(TAU, TAU)
         and certify_cover(COVER, *cover_counts(COVER)), 'claim records')
    uni_ok = True
    try:
        certify_uniformity(uniformity_text)
    except AdmissionError:
        uni_ok = False
    must(uni_ok, 'uniformity wording')
    e2 = c['enum'][2]
    swap_witness = {'F1_box_is_native_restriction_of_Phi_prime': False, 'faces_missing_from_F1_vs_Phi_prime_native_N2': e2['count'],
                    'F2_box_is_native_restriction_of_Phi': False, 'partial_star_groups_in_F2_N2': e2['partial_groups'],
                    'swapped_value_F2_inner_with_2268': exact(2 * 2268 * TAU * TAU / 3 * 168 * E_up(2 * 2268 * 224 * TAU))}
    c.update(admitted=admitted, facts=facts, outcome=outcome, gate_fields=gate_fields, flags=flags, model_rec=model_rec,
             rate_rec=rate_rec, uniformity_text=uniformity_text, rate_units_text=rate_units_text, swap_witness=swap_witness)
    check('item5_honest_meaning_and_claims', True, gate_fields=gate_fields, admitted=admitted,
          meaning='algebraic Heisenberg dynamics of the named constructions F1, F2 on the compact window |theta|<=8; '
                  'not equality of GNS dynamics or of correlation functions of different states (those need a common state, BB2); '
                  'not uniform in time; not uniform in the lattice spacing a')
    run_controls(c)

    # ------------------------------------------------ report-level checks
    report_text, template, forbidden = c['report_text'], c['template'], c['forbidden']
    exported_texts = [template, c['uniformity_text'], c['rate_units_text']]
    check('item5_mandatory_template_once', certify_template_span(report_text, template), template_sha256=sha256_bytes(template.encode()))
    check('report_phrase_scan_negation_aware', certify_phrasing(report_text, forbidden, template)
          and all(certify_phrasing(t, forbidden, template) for t in exported_texts), scanned=['report.md', 'exported sentences'],
          forbidden_count=len(forbidden))
    ex_ok = all(e in report_text for e in contract['claim_exclusions'])
    const_ok = all(qs(v) in report_text for v in (K_cmp, c1, c2))
    disclosure = ('Claude' in report_text and 'AI' in report_text and '/tmp/claude-0/ba2-reverse-private/' in report_text
                  and 'a chosen subsequential' in report_text and 'HNM-BA2-R' in report_text)
    check('report_binds_constants_exclusions_disclosure', ex_ok and const_ok and disclosure,
          exclusions_verbatim=ex_ok, headline_rationals_in_report=const_ok)
    ledger = {
        'lieb_robinson_tail': {'value': 'comparison: F(N)+F(N-1)<=2N^-4 per owner; Cauchy: T(N)+T(N-1)<=8/(N-1)',
                               'tier': TIER},
        'duhamel_boundary_sum': {'value': 'comparison: (|tau|/3) 28N(5N+1) 3 (N^-4+(N+1)^-4) <= (|tau|/3) 168 (5N+1) N^-3; '
                                          'Cauchy: J 8/(N-1) with J=28|tau| (F1) or 49|tau|/3 (F2)'},
        'interaction_picture_onsite': {'value': '0', 'reason': 'h_b enters no constant (H_x slot of (44), interaction picture in '
                                                              'the proof of Theorem 3.1); padding on-site terms factor out exactly'},
        'inner_family_constants': {'value': "comparison and F2 Cauchy: Phi', 1323|tau|, C<=224; F1 Cauchy: Phi, 2268|tau|, C<=224; "
                                            'time integral 2||Phi||_F U^2 E(x), E<=E_up rational'},
        'arithmetic': {'value': '0', 'reason': 'exact Fractions; E(x) replaced by the directed rational upper bound '
                                               '1+x/3+x^2/(12(1-x/5)); decimals are truncated previews'},
    }
    check('error_ledger_itemized', certify_error_ledger(ledger, pre['error_terms_itemized']), ledger=ledger)

    ids = [x['id'] for x in CHECKS]
    missing = [x for x in contract['controls'] if x not in ids]
    must(missing == [], 'contract controls without a check: ' + ','.join(missing))
    must(sorted(MUTATION_CONTROLS) == sorted(contract['controls']), 'every contract control carries damaging mutations')
    n_mut = sum(len(x.get('rejected_mutations', {})) for x in CHECKS)

    P_ = P
    headline = {
        'comparison_coefficient': dict(exact(K_cmp), bound='b(N) = K_cmp (5N+1) N^-3 ||A||, |theta|<=8, N>=2, both signs',
                                       formula='148176 tau^2 U^2 E_up(592704 |tau| U), U=1', target=qs(P_['target_comparison']),
                                       target_met=admitted['comparison'], margin=sci(P_['target_comparison'] / K_cmp, 8),
                                       tier=TIER, inner_family='F2', interaction=PHI_PRIME + ' 1323|tau|, C<=224',
                                       route='Duhamel with the inner F2 evolution; source = extra faces',
                                       tau_over_100_ratio=exact(c['r_cmp'])),
        'cauchy_coefficient_F1': dict(exact(c1), bound='sup_{M>N} ||T^{F1,M}_theta(A)-T^{F1,N}_theta(A)|| <= c1/(N-1) ||A||',
                                      formula='1016064 tau^2 U^2 E_up(1016064 |tau| U)', target=qs(P_['target_cauchy']),
                                      target_met=admitted['cauchy_F1'], margin=sci(P_['target_cauchy'] / c1, 8), tier=TIER,
                                      inner_family='F1 (box Lambda_M)', interaction=PHI + ' 2268|tau|, C<=224',
                                      route='own-family Duhamel between Lambda_N and Lambda_M; own Nachtergaele-Sims limit',
                                      tau_over_100_ratio=exact(c['r_c1'])),
        'cauchy_coefficient_F2': dict(exact(c2), bound='sup_{M>N} ||T^{F2,M}_theta(A)-T^{F2,N}_theta(A)|| <= c2/(N-1) ||A||',
                                      formula='345744 tau^2 U^2 E_up(592704 |tau| U)', target=qs(P_['target_cauchy']),
                                      target_met=admitted['cauchy_F2'], margin=sci(P_['target_cauchy'] / c2, 8), tier=TIER,
                                      inner_family='F2 (box Lambda_M)', interaction=PHI_PRIME + ' 1323|tau|, C<=224',
                                      route='own-family Duhamel between Lambda_N and Lambda_M, face by face; own Nachtergaele-Sims limit',
                                      tau_over_100_ratio=exact(c['r_c2'])),
        'b_N_values': c['b'],
        'limit_bounds': {'F1': '||T_theta(A)-T^{F1,N}_theta(A)|| <= c1/(N-1) ||A||',
                         'F2': '||T_theta(A)-T^{F2,N}_theta(A)|| <= c2/(N-1) ||A||, T_theta the AQ1 limit (identified)'},
        'labelled_weaker_triangle_bound': c['tri'],
        'labelled_sharper_enumerated_comparison': c['sharper'],
    }
    result = {
        'loop': 'BA2', 'direction': 'reverse',
        'route': 'Duhamel with the inner F2 evolution and the owner-set Nachtergaele-Sims constants; own-family Cauchy '
                 'estimates against each family own Nachtergaele-Sims limit; identification of the F2 limit with the AQ1 limit',
        'human_author': contract['human_author'],
        'ai_assistance': 'AI-assisted reverse production (Claude, an AI model); correlated model-agent work, not human review',
        'contribution_alias': 'HNM-BA2-R reverse inner-F2 Duhamel comparison, own-family Cauchy limits and F2 limit dynamics',
        'attribution': {'lieb_robinson': 'Nachtergaele-Sims arXiv:1410.8174v1 Theorem 3.1 (51)-(52), quoted verbatim from the committed excerpt',
                        'limit_dynamics': 'Nachtergaele-Sims arXiv:1410.8174v1 Theorem 4.1 (77)',
                        'duhamel': 'standard interaction-picture identity for a bounded perturbation',
                        'o6_strategy': 'AQ1 sections 4-5 (Gauvin arXiv:2503.15539v3 A.10 as the prior strategy)',
                        'scientific_priority': 'unverified'},
        'contract_sha256': c['contract_sha'], 'check_py_sha256_recorded_before_evaluation': c['check_py_sha'],
        'pinned_premise_sha256': c['pinned'],
        'model': contract['model'],
        'model_label': 'AQ_patterned_zero_selected; zero triple (Haar reference); 21 omitted faces per anchor as -(tau/3)W_f in '
                       'normalized units delta=alpha/8; |tau|<=10^-8 both signs; F1 and F2 on Lambda_N=[-N,N]^3, N>=2; '
                       'cover R={0,e_z} (48 links, 36 endpoints); fixed spacing; common clock theta=alpha t/hbar, u=theta/8',
        'families': {'F1': F1_NAME, 'F2': F2_NAME},
        'parameters_used': {'metric': 'coarse l1; F(r)=(1+r)^-4; ||F||<=7; C<=224', 'window': '|theta|<=8, U=Theta/8=1',
                            'clock': 'theta=alpha t/hbar; normalized u=theta/8 internally', 'N_0': 2, 'tau': qs(TAU)},
        'label': 'dynamics_on_compact_windows', 'sub_label': 'dynamics_on_compact_windows',
        'headline': headline,
        'boundary_source': {'extra_faces': '28N(5N+1)', 'anchors': '140N^2 faces at anchors with one b_i=N, 28N at two, none at three',
                            'distance': 'owners on the outer layer: coarse l1 >=N from 0 and >=N-1 from e_z (attained)',
                            'fine_units_reading': 'N-1 fine steps along z between tail blocks (4N-3 along x, 2N-1 along y); informational',
                            'padding': 'H^{F2,pad} = H^(2) (x) 1 + 1 (x) sum_pad h_x factors out exactly; never charged',
                            'enumerated': {str(N): {k: c['enum'][N][k] for k in ('count', 'min_dist_0', 'min_dist_e_z', 'max_owners',
                                                                                   'partial_groups', 'padding_sites')} for N in (2, 3)}},
        'o6': c['O6'],
        'identification': c['ident'],
        'topologies': {'dynamics': DYNAMICS_TOPOLOGY, 'states': STATES_TOPOLOGY, 'time_continuity': GNS_TOPOLOGY},
        'honest_meaning': 'algebraic Heisenberg dynamics of the named constructions on the compact window |theta|<=8 at a rate in N '
                          '(at fixed spacing); not equality of GNS dynamics or of correlation functions of different states (BB2); '
                          'not uniform in time; not uniform in the lattice spacing a',
        'mandatory_sentence_template': c['template'],
        'b_N_filled': 'b(N) = ' + qs(K_cmp) + ' (5N+1) N^-3 (about ' + sci(K_cmp, 6) + ' (5N+1) N^-3)',
        'gate_fields': gate_fields,
        'error_ledger': ledger,
        'scaling': {'comparison_coefficient': exact(c['r_cmp']), 'cauchy_coefficient_F1': exact(c['r_c1']),
                    'cauchy_coefficient_F2': exact(c['r_c2']), 'brackets_read_from': 'preregistration.scaling_brackets_per_constant'},
        'trap_fixtures': {
            'polynomial_versus_exponential_tail': 'exact m*S(m)>=1/2 for m=2..256 (S(m)=sum_{r=m}^{2m-1}(4r^2+2)(1+r)^-4)',
            'onsite_term_placed_wrongly': 'cutoff ladder h_L=diag(0..L) inside Phi gives ||Phi||_F>=L for L=1..1000',
            'padding_terms_in_duhamel': 'exact Gaussian-rational factorization e^{iuHpad}(A(x)1)e^{-iuHpad}=(e^{iuH}Ae^{-iuH})(x)1 at u=pi/2',
            'inner_family_constant_swapped': 'F1 box is not the native restriction of Phi\' (616 faces missing at N=2); F2 box is not '
                                             'the native restriction of Phi (60 partial groups at N=2)',
            'n_to_n_plus_1_summed': 'harmonic increments 1/(n+1) do not sum; a Cauchy estimate needs sup over M'},
        'exclusions': {'contract': contract['claim_exclusions'], 'preregistration': pre['claim_exclusions']},
        'routes_executed': [
            'item 1: Theorem 3.1/4.1 quoted verbatim; F, ||F||<=7, C<=224; h_b in the H_x slot; Phi 2268|tau| and Phi\' 1323|tau| re-derived',
            'item 2: extra faces enumerated on Lambda_2, Lambda_3 (and counts to N=6) with the all-size anchor decomposition; padding factorization',
            'item 3: Duhamel with the inner F2 evolution; LR bound per extra face; exact K_cmp at the cap, both signs; first order vanishes',
            'item 4: own-family Cauchy for F1 (Phi) and F2 (Phi\', face by face); limits; identification; AQ1 sections 4-5 rerun for F2',
            'item 5: honest meaning; gate fields; mandatory template quoted once',
            'item 6: tau/100 scaling per constant; five trap fixtures; 35 controls as damaging mutations'],
        'contract_controls_covered': list(contract['controls']),
        'controls_with_damaging_mutations': sorted(MUTATION_CONTROLS),
        'controls_not_implementable_as_mutations': [],
        'damaging_mutations_rejected': n_mut,
        'proposed_reverse_verdict': outcome,
        'outcome_note': 'proposed for the reverse half only; acceptance needs both routes and the skeptical review',
        'contract_wording_notes': [
            'parameters declares metric, weights and window; N_0 appears only in the target text and d_X is absent (no exponential target)',
            'preregistration.observable names an N to N+1 quantity while the Cauchy target is the sup over M greater than N; the sup is proved',
            'item 3 writes B(N) and b(N) for the same bound; item 4 writes tau^{F,M}_theta for T^{F,M}_theta (tau is also the coupling)',
            'two brackets for the comparison ratio ([9500,10500] and [9900,10100]); both are met',
            'state_provenance says no state enters, yet O6 needs the F2 subsequential limit states of AY1',
            'new_control_semantics covers 31 of the 35 controls; full_original_wilson_cover, topology_named, '
            'cross_coupling_comparison_rejected and gate_fields_topic_specific carry inherited semantics (implemented here)'],
        'checks': CHECKS,
    }
    result.update(flags)
    result.update({k: v for k, v in gate_fields.items()})
    return result


def main():
    ap = argparse.ArgumentParser(description='HNM-BA2 reverse producer checker (exact arithmetic)')
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
    manifest = {'loop': 'BA2', 'direction': 'reverse', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    h = result['headline']
    print(json.dumps({'loop': 'BA2', 'direction': 'reverse', 'checks': len(result['checks']),
                      'damaging_mutations': result['damaging_mutations_rejected'],
                      'K_cmp': h['comparison_coefficient']['preview'], 'c1': h['cauchy_coefficient_F1']['preview'],
                      'c2': h['cauchy_coefficient_F2']['preview'], 'outcome': result['proposed_reverse_verdict']}, sort_keys=True))


if __name__ == '__main__':
    main()
