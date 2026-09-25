#!/usr/bin/env python3
"""Round33 BB1 skeptic pre-comparison checker (zero-selected patterned family).

Written after the BB1 contract froze (sha256 30400d2e...8018, frozen
2026-09-24T23:36:46Z), from the frozen contract, advisor/selection-bb1.md,
advisor/plan.json, advisor/deliberation-2.md, experts/modern/bb-targets-proposal.md
(the recorded previews), the skeptic's own Round33 record (triage.md,
prospective-controls.json, loop2-review.md, bb-contract-review.md/.json, the BA1
package) and the declared premises (BA1 gate, forward and reverse reports and
the BA1 review; AV1 reports and gate; AM2 reports and review; AQ1; I1; AW1;
AY1; AY2), before reading research/round33/forward/bb1/ or
research/round33/reverse/bb1/ (only the file names of their inputs/ were listed
and hashed). Nothing is imported from any producer, assistant or tool. Standard
library only. Every admission Boolean is decided with fractions.Fraction and
directed enclosures (exp from above by a Taylor polynomial plus a geometric
tail and from below by its partial sum, log from below by 2(x-1)/(x+1), square
roots by integer brackets); floats appear only in the labelled 'previews'
blocks. Every check and control raises an explicit exception, so python -O
cannot disable it. Model-agent skeptic with correlated ancestry; not human
peer review. Human project author: Hruday N M (BUNZEEY).

What is derived here:
  * the frozen contract read back: pairs, brackets, control mirror (37), the
    semantics coverage (21 BB1 + 16 inherited from BA1), gate fields, template
    scan, placeholder scan, the 35-file reverse inventory, and the skeptic's 17
    pre-freeze replacement texts found verbatim in the frozen bytes;
  * the every-site coefficient input (form b): every source site of every
    comparison has |p|_inf >= N, so d_inf(u, sources) >= N-|u|_inf for every u
    in Lambda_N (enumerated on Lambda_2..Lambda_4, all centered pairs, general
    volumes), giving sum_{I ni u} ||delta_I|| <= K q^(N-|u|_inf) with
    K = 2T(64|tau|) = 49/111790368; form (a) with the labelled K_own;
  * |I| <= (1+diam I)^3 <= 8*2^(diam I), the cardinality excess of AM2 words
    (loss e^{4b} attained by the generic k=0 count, e^{3b} for k>=1), the face
    order count (|M| <= 2n+1);
  * the density-level constants C and c_site at q=1/64 and the secondary pair,
    both signs, every comparison: near term 2 sum_{y in Y} D(y) (derivative
    identity and variance bound), far term by the truncated-correlation split
    recursion with cardinality control (mixed weight theta=64, e^b=9/8), the
    split (sine-bound) variant, the recorded-preview structure, union and
    crude tiers, tau/100 ratios, KP feasibility, the mixed-weight loss;
  * exact finite fixtures for the traps, and a packet validator executing all
    37 contract controls as damaging mutations.

Usage: python3 -B research/round33/skeptic/bb1_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = 'research/round33/contracts/bb1.json'
CONTRACT = ROOT / CONTRACT_REL
CONTRACT_SHA256 = '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018'
REVIEW_REL = 'research/round33/skeptic/bb-contract-review.json'
PINNED = {
    'research/round21/forward/i1/report.md': '836a4c7d421f0ddf3589c159d2f057839421532c88157a054a61b51c25c781a9',
    'research/round29/forward/am2/report.md': '1b58fb9c1a199f06b156d04c2a9e89f34ba63cf675a5f7c8bfc25bb568e4e019',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round32/forward/av1/report.md': '7f86e941933913584de2b9e542359e4a3b3c275c1bc8623dca3c367d88437353',
    'research/round33/advisor/ba1-gate.json': '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    'research/round33/reverse/ba1/report.md': 'a986c205542376c2ad5058cdf88e082abe9c12eeba87b052abf3ad9cefebbb86',
    'research/round33/forward/ba1/report.md': 'd8ed5bfa780b95a57e5ba822b81f0fea5f71aaa7ea1a01bb4dbecb0d417aa769',
    'research/round33/contracts/ba1.json': '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9',
    REVIEW_REL: 'c43549ef9deffd9e84c10e4266ff322c897b3d8e5f175ab52d68bdbdcd5f4ea2',
}

DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN, E_Z = (0, 0, 0), (0, 0, 1)
R_COVER = (ORIGIN, E_Z)
MODEL_ID = 'AQ_patterned_zero_selected'
CLOCK = 's=alpha*t_E/hbar, theta=alpha*t/hbar'
WINDOW = 'not applicable (static densities)'
TOPOLOGY = 'trace norm on B(H_Y)'
UNIFORM_IN = 'N at fixed spacing'
RATE_UNITS = 'per coarse l_inf step at fixed spacing'
R = F(1, 64)
G_R, GP_R = F(148, 7), F(352)
TIERS = ('crude_majorant', 'exact_first_order')
ROUTES = ('polymer_kp', 'iterated_split')
INPUTS = ('gate_bound_K', 'labelled_weighted_norm', 'labelled_reinstantiated_disc', 'crude_analytic_disc')
EXACT_INPUTS = ('gate_bound_K', 'labelled_weighted_norm', 'labelled_reinstantiated_disc')
# Mirror of research/round33/tools/phrase_scan.py ROUND_FORBIDDEN and NEGATION (not imported).
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
# Mirror of the freezer's rule R1 detector (research/round33/tools/freeze_contract.py), not imported.
PLACEHOLDER = re.compile(r'<(?![=<>])([^<>=]*)(?<![-=|])>(?!=)')
REQUIRED_FIXTURES = ('coefficient_decay_not_marginal_decay', 'second_order_propagation', 'normalization_spectators',
                     'global_fidelity', 'straddling_supports', 'split_trace_and_lipschitz', 'split_per_site_charging',
                     'polymer_identity', 'polymer_cardinality_factor', 'cutoff_eckart', 'cutoff_limit_order',
                     'fixed_versus_moving_vector', 'zero_free_region', 'outside_vector_not_ground_state')


class Rejected(Exception):
    """Raised by the validator when it refuses a packet; controls require it."""


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


def q(x):
    return str(x)


def preview(x):
    return format(float(x), '.12e')


def fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def exp_up(x, n=12):
    """Directed upper bound of e^x for 0<=x<n+2: Taylor polynomial plus geometric tail."""
    x = F(x)
    if x < 0 or x >= n + 2:
        raise CheckFailure('exp_up domain')
    s = sum((x ** k / fact(k) for k in range(n + 1)), F(0))
    return s + x ** (n + 1) / fact(n + 1) / (1 - x / (n + 2))


def exp_lo(x, n=12):
    x = F(x)
    if x < 0:
        raise CheckFailure('exp_lo domain')
    return sum((x ** k / fact(k) for k in range(n + 1)), F(0))


def ln_lo(x):
    """Directed lower bound of log x for x>=1: 2(x-1)/(x+1)."""
    x = F(x)
    if x < 1:
        raise CheckFailure('ln_lo domain')
    return 2 * (x - 1) / (x + 1)


def small_exp_up(x):
    return exp_up(x, 3 if x < F(1, 100) else 12)


def _order(x):
    return 12 if x >= F(1, 100) else 4


def g_up(t):
    return 16 * exp_up(8 * t, _order(8 * t)) * (1 + 10 * t)


def gp_up(t):
    return 16 * exp_up(8 * t, _order(8 * t)) * (18 + 80 * t)


def sqrt_lo_hi(x, scale=10 ** 15):
    """Rational bracket [lo, hi] of sqrt(x) for a nonnegative Fraction x."""
    x = F(x)
    if x < 0:
        raise CheckFailure('sqrt domain')
    num, den = x.numerator, x.denominator
    r = isqrt(num * den * scale * scale)
    lo = F(r, den * scale)
    hi = F(r + 1, den * scale)
    if not (lo * lo <= x <= hi * hi):
        raise CheckFailure('sqrt bracket')
    return lo, hi


def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def sub(a, b):
    return tuple(i - j for i, j in zip(a, b))


def dinf(p, r):
    return max(abs(x - y) for x, y in zip(p, r))


def d1(p, r):
    return sum(abs(x - y) for x, y in zip(p, r))


def norm_inf(p):
    return max(abs(x) for x in p)


def diam(pts, metric):
    pts = list(pts)
    return max((metric(a, b) for a in pts for b in pts), default=0)


def set_dist(u, pts, metric):
    return min(metric(u, p) for p in pts)


# ---------------------------------------------------------------- geometry (I1)
def pi_map(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    ea, ec = DIRS[a], DIRS[c]
    return ((p, a), (p, c), (add(p, ea), c), (add(p, ec), a))


def owner_set(p, a, c):
    return frozenset(pi_map(tail) for tail, _ in face_links(p, a, c))


def is_selected(p, a, c):
    return (a, c) == ('x', 'y') and p[0] % 4 in (0, 1, 2) and p[1] % 2 == 0


def anchor_classes():
    out = []
    for r, s in product(range(4), range(2)):
        p = (r, s, 0)
        for a, c in ORIENT:
            out.append({'orient': a + c, 'r': r, 's': s, 'rel': owner_set(p, a, c), 'selected': is_selected(p, a, c)})
    return out


CLASSES = anchor_classes()
OMITTED = [k for k in CLASSES if not k['selected']]


def parse_i1_table(text):
    rows = re.findall(r'^\| (xy|xz|yz): [^|]*\| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|$', text, re.M)
    names = {'0': ORIGIN, 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': E_Z}
    out = {}
    for orient, cnt, supp, role in rows:
        key = (orient, tuple(sorted(names[t.strip()] for t in supp.split(','))), role == 'selected')
        out[key] = out.get(key, 0) + int(cnt)
    return out


def class_table():
    out = {}
    for k in CLASSES:
        key = (k['orient'], tuple(sorted(k['rel'])), k['selected'])
        out[key] = out.get(key, 0) + 1
    return out


def cube(n):
    return set(product(range(-n, n + 1), repeat=3))


def cuboid(lo, hi):
    return set(product(*[range(a, b + 1) for a, b in zip(lo, hi)]))


def star_anchors(sites):
    return sorted(b for b in sites if all(add(b, s) in sites for s in S_STAR))


def f1_faces(sites):
    out = {}
    for b in star_anchors(sites):
        for idx, k in enumerate(OMITTED):
            out[(b, idx)] = frozenset(add(b, d) for d in k['rel'])
    return out


def f2_faces(sites):
    out = {}
    for b in sites:
        for idx, k in enumerate(OMITTED):
            own = frozenset(add(b, d) for d in k['rel'])
            if own <= sites:
                out[(b, idx)] = own
    return out


# ---------------------------------------------------------------- admitted constants (BA1, AV1, AM2)
def j_of(abs_tau):
    return 28 * abs_tau


def t1_of(abs_tau):
    return F(49, 144) * abs_tau


def tbar_of(abs_tau):
    """AV1 exact-first-order anchored norm t <= t_1/(1-352J) (real coupling)."""
    return t1_of(abs_tau) / (1 - 352 * j_of(abs_tau))


def w_max_of(abs_tau):
    return R / (j_of(abs_tau) * G_R)


def T_disc(rho):
    """BA1 reverse Lemma 1.2: T(rho) = (49 rho/144)/(1 - 28 rho G'(R)); the circle bound of the anchored norm."""
    lip = 28 * rho * GP_R
    if lip >= 1 or 28 * rho * G_R > R:
        raise CheckFailure('disc radius outside the contraction')
    return F(49, 144) * rho / (1 - lip)


def K_form_b(abs_tau, q_rate):
    """Every-site form (b): BA1 reverse Theorem 4.1 at rho=|tau|/q with R replaced by {u}: 2T(rho)."""
    return 2 * T_disc(abs_tau / q_rate)


def K_own_of(abs_tau, w):
    """Form (a): BA1 forward boundary-weighted norm constant T_w/(1-Gamma) at e^beta=w (labelled values)."""
    j = j_of(abs_tau)
    gam = j * w * GP_R
    t_w = w * t1_of(abs_tau) / (1 - gam)
    return t_w / (1 - gam)


def K_gen_of(abs_tau, w):
    """BA1 forward telescoped general-comparison value K_12 + K_nest/(1-q) (labelled; the BA1 gate's forward value)."""
    k12 = K_own_of(abs_tau, w)
    qq = F(1) / w
    return k12 + qq * k12 / (1 - qq)


def K_crude_b(abs_tau, q_rate):
    rho = abs_tau / q_rate
    return 2 * 28 * rho * G_R


def T_mix(abs_tau, w, e_b, tier='exact_first_order'):
    """Mixed-weight fixed-point bound sup_x sum_{J ni x} w^{diam J} e^{b|J|} ||c_J||.
    Loss w e^{4b} per interaction (|M| <= |X| + sum|I_j|, |X|<=4); first-order owner sets have diameter 1 and at
    most 3 sites; self-map J w e^{4b} G(R) <= R required."""
    j = j_of(abs_tau)
    loss = w * e_b ** 4
    if j * loss * G_R > R:
        raise CheckFailure('mixed weight: self-map fails')
    if tier == 'exact_first_order':
        return w * e_b ** 3 * t1_of(abs_tau) / (1 - j * loss * GP_R)
    return j * loss * G_R


def far_constants(abs_tau, theta, e_b, tier='exact_first_order'):
    """Truncated-correlation split recursion: Psi(Z) <= A |Z| e^{beta|Z|} Delta_Z with
    beta = 2 t', t' = sup_x sum_{J ni x} e^{b|J|}||c_J||, M = sup_x sum_{J ni x} theta^{diam J} e^{b|J|}||c_J||,
    eps = b - beta (b = log e_b bounded from below), A = 4M/(eps e - 4M)."""
    t_p = T_mix(abs_tau, F(1), e_b, tier)
    m_w = T_mix(abs_tau, theta, e_b, tier)
    beta = 2 * t_p
    eps = ln_lo(e_b) - beta
    e_lo = exp_lo(F(1))
    if eps <= 0 or eps * e_lo <= 4 * m_w:
        raise CheckFailure('far recursion does not close')
    a_far = 4 * m_w / (eps * e_lo - 4 * m_w)
    return {'t_prime': t_p, 'M': m_w, 'beta': beta, 'eps': eps, 'A': a_far, 'e2beta_up': small_exp_up(2 * beta)}


def assemble(k_in, q_rate, far, site0='N', form='R'):
    """Derivative near term (constant 2, exact) plus far recursion.
    R form: 2K(q_0 + 1 + 2A e^{2beta}) with q_0 = q (every-site input at u=0) or 1 (R-only input at both sites).
    region form (per site): 2K(1+A), valid with e^{beta|Y|} <= e^{|Y|/10^8} when beta <= 10^-8."""
    if form == 'R':
        q0 = q_rate if site0 == 'N' else F(1)
        return 2 * k_in * (q0 + 1 + 2 * far['A'] * far['e2beta_up'])
    return 2 * k_in * (1 + far['A'])


def assemble_split(k_in, q_rate, far, abs_tau, site0='N'):
    """Split (sine-bound) variant for R: 2||X^1-X^2|| <= 2(D_0+D_ez)(1+tbar+K) plus the far recursion with the
    omega-Lipschitz factor 2 (A' = 2M/(eps e - 2M))."""
    tb = tbar_of(abs_tau)
    q0 = q_rate if site0 == 'N' else F(1)
    a_split = 2 * far['M'] / (far['eps'] * exp_lo(F(1)) - 2 * far['M'])
    return 2 * k_in * ((q0 + 1) * (1 + tb + k_in) + 2 * a_split * far['e2beta_up'])


def shell_sum(x):
    """S(x) = sum_{d>=1} (24d^2+8d+2) x^{-d} (l_inf shells around R={0,e_z})."""
    r = F(1) / x
    if r >= 1:
        raise CheckFailure('shell sum diverges')
    return 24 * r * (1 + r) / (1 - r) ** 3 + 8 * r / (1 - r) ** 2 + 2 * r / (1 - r)


# ---------------------------------------------------------------- qubit algebra (finite fixtures)
def mask_of(*sites):
    s = 0
    for i in sites:
        s |= 1 << i
    return s


def vac(n, zero=F(0), one=F(1)):
    v = [zero] * (2 ** n)
    v[0] = one
    return v


def cre(vec, mask, amp, zero=F(0)):
    out = [zero] * len(vec)
    for s, x in enumerate(vec):
        if not (s & mask) and x != zero:
            out[s | mask] = out[s | mask] + amp * x
    return out


def state(n, creations, zero=F(0), one=F(1)):
    v = vac(n, zero, one)
    for mask, amp in creations:
        c = cre(v, mask, amp, zero)
        v = [x - y for x, y in zip(v, c)]
    return v


def ip(u, v):
    tot = u[0] * v[0]
    for a, b in zip(u[1:], v[1:]):
        tot = tot + a * b
    return tot


def rdm_raw(vec, sites, n):
    """Unnormalized reduced density (real vectors) on the listed sites."""
    k = len(sites)
    rest = [i for i in range(n) if i not in sites]

    def idx(a, r_):
        s = 0
        for j, i in enumerate(sites):
            if a >> j & 1:
                s |= 1 << i
        for j, i in enumerate(rest):
            if r_ >> j & 1:
                s |= 1 << i
        return s

    rho = [[None] * (2 ** k) for _ in range(2 ** k)]
    for a in range(2 ** k):
        for b in range(2 ** k):
            tot = None
            for r_ in range(2 ** len(rest)):
                term = vec[idx(a, r_)] * vec[idx(b, r_)]
                tot = term if tot is None else tot + term
            rho[a][b] = tot
    return rho


def rdm(vec, sites, n):
    raw = rdm_raw(vec, sites, n)
    z = sum(raw[a][a] for a in range(len(raw)))
    return [[x / z for x in row] for row in raw], z


def apply_op(vec, mat, sites):
    k = len(sites)
    msk = mask_of(*sites)
    out = [F(0)] * len(vec)
    for s, x in enumerate(vec):
        if not x:
            continue
        b = 0
        for j, i in enumerate(sites):
            if s >> i & 1:
                b |= 1 << j
        rest = s & ~msk
        for a in range(2 ** k):
            e = mat[a][b]
            if e:
                t = rest
                for j, i in enumerate(sites):
                    if a >> j & 1:
                        t |= 1 << i
                out[t] += e * x
    return out


def omega(psi, op):
    return ip(psi, op(psi)) / ip(psi, psi)


def trunc(psi, op_a, op_b):
    return ip(psi, op_a(op_b(psi))) / ip(psi, psi) - omega(psi, op_a) * omega(psi, op_b)


def matvec(mat, v):
    return [sum((mat[i][j] * v[j] for j in range(len(v))), F(0)) for i in range(len(mat))]


def psd(mat):
    """Exact positive-semidefiniteness of a symmetric rational matrix (LDL^T with zero-pivot handling)."""
    a = [list(row) for row in mat]
    n = len(a)
    for i in range(n):
        piv = a[i][i]
        if piv < 0:
            return False
        if piv == 0:
            if any(a[i][j] != 0 for j in range(i + 1, n)):
                return False
            continue
        for r_ in range(i + 1, n):
            f = a[r_][i] / piv
            for c_ in range(i, n):
                a[r_][c_] -= f * a[i][c_]
    return True


def trace_norm_2x2(mat):
    """Directed bracket of the trace norm of a real symmetric 2x2 matrix."""
    p, r_, s = mat[0][0], mat[0][1], mat[1][1]
    det = p * s - r_ * r_
    if det >= 0:
        v = abs(p + s)
        return v, v
    return sqrt_lo_hi((p - s) ** 2 + 4 * r_ * r_)


class P:
    """Minimal exact multivariate polynomial (dict exponent tuple -> Fraction)."""
    NV = 3

    def __init__(self, terms=None):
        self.t = {k: F(v) for k, v in (terms or {}).items() if v != 0}

    @classmethod
    def const(cls, c):
        return cls({(0,) * cls.NV: F(c)})

    @classmethod
    def var(cls, i):
        e = [0] * cls.NV
        e[i] = 1
        return cls({tuple(e): F(1)})

    def __add__(self, o):
        o = o if isinstance(o, P) else P.const(o)
        out = dict(self.t)
        for k, v in o.t.items():
            out[k] = out.get(k, F(0)) + v
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.t.items()})

    def __sub__(self, o):
        return self + (-(o if isinstance(o, P) else P.const(o)))

    def __mul__(self, o):
        o = o if isinstance(o, P) else P.const(o)
        out = {}
        for k1, v1 in self.t.items():
            for k2, v2 in o.t.items():
                k = tuple(a + b for a, b in zip(k1, k2))
                out[k] = out.get(k, F(0)) + v1 * v2
        return P(out)

    __rmul__ = __mul__

    def __eq__(self, o):
        o = o if isinstance(o, P) else P.const(o)
        return self.t == o.t

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        return hash(tuple(sorted(self.t.items())))

    def at(self, vals):
        tot = F(0)
        for k, v in self.t.items():
            term = v
            for x, e in zip(vals, k):
                term *= F(x) ** e
            tot += term
        return tot

    def coeff(self, i, power):
        """Coefficient polynomial of variable i at the given power."""
        out = {}
        for k, v in self.t.items():
            if k[i] == power:
                kk = list(k)
                kk[i] = 0
                out[tuple(kk)] = v
        return P(out)


PZ, P1 = P.const(0), P.const(1)


def phrase_hits(text, forbidden, template=None):
    body = re.sub(r'\s+', ' ', str(text)).strip()
    if template:
        body = body.replace(re.sub(r'\s+', ' ', template).strip(), ' ')
    hits = []
    for clause in [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', body) if c.strip()]:
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                hits.append({'phrase': phrase, 'negated': bool(NEGATION.search(clause))})
    return [h for h in hits if not h['negated']]


def placeholder_spans(text):
    out = []
    for m_ in PLACEHOLDER.finditer(text):
        inner = m_.group(1)
        if re.search(r'\s', inner) or '|' in inner or 'e.g.' in inner:
            out.append(m_.group(0))
    return out


def strings_of(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings_of(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings_of(v)


def json_path_get(doc, path):
    cur = doc
    for part in path[2:].replace('[', '.[').split('.'):
        if part.startswith('['):
            cur = cur[int(part[1:-1])]
        else:
            cur = cur[part]
    return cur


def has_float(value):
    if isinstance(value, float):
        return True
    if isinstance(value, dict):
        return any(has_float(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(has_float(v) for v in value)
    return False


def enumerate_polymers(sup):
    """Overlap-connected pairs (F,F') of families of pairwise disjoint supports with equal excitation sets.
    sup: list of (sites tuple, amplitude). Returns the sorted polymer list [((L idx),(R idx)), X, w] and the number
    of family pairs with different excitation sets (their inner product is zero)."""
    fams = []
    for k in range(len(sup) + 1):
        for cmb in combinations(range(len(sup)), k):
            sets = [set(sup[i][0]) for i in cmb]
            if any(sets[i] & sets[j] for i in range(len(sets)) for j in range(i + 1, len(sets))):
                continue
            fams.append(cmb)

    def union_of(cmb):
        return frozenset().union(*[frozenset(sup[i][0]) for i in cmb]) if cmb else frozenset()

    def weight(cmb):
        w = F((-1) ** len(cmb))
        for i in cmb:
            w *= sup[i][1]
        return w

    polymers = {}
    zero_pairs = 0
    for fa in fams:
        for fb in fams:
            if union_of(fa) != union_of(fb):
                zero_pairs += 1
                continue
            if not fa:
                continue
            verts = [('L', i) for i in fa] + [('R', i) for i in fb]
            seen = set()
            for v0 in verts:
                if v0 in seen:
                    continue
                stack, cur = [v0], []
                seen.add(v0)
                while stack:
                    v = stack.pop()
                    cur.append(v)
                    for u2 in verts:
                        if u2 not in seen and u2[0] != v[0] and set(sup[u2[1]][0]) & set(sup[v[1]][0]):
                            seen.add(u2)
                            stack.append(u2)
                key = (tuple(sorted(i for s_, i in cur if s_ == 'L')), tuple(sorted(i for s_, i in cur if s_ == 'R')))
                xl, xr = union_of(key[0]), union_of(key[1])
                if xl != xr:
                    raise CheckFailure('polymer component with unequal excitation sets')
                polymers[key] = (xl, weight(key[0]) * weight(key[1]))
    plist = [(k, v[0], v[1]) for k, v in sorted(polymers.items())]
    return plist, zero_pairs


def polymer_partition(plist, avail, start=0):
    """Hard-core polymer sum over compatible (pairwise disjoint) families of the listed polymers."""
    tot = F(1)
    for idx in range(start, len(plist)):
        _, xs_, w = plist[idx]
        if xs_ <= avail:
            tot += w * polymer_partition(plist, avail - xs_, idx + 1)
    return tot


# ---------------------------------------------------------------- validator
def recompute_constant(rec, abs_tau):
    inp = rec['inputs']
    if inp['K_source'] == 'gate_bound_K' or inp['K_source'] == 'labelled_reinstantiated_disc':
        k_in = K_form_b(abs_tau, rec['q'])
    elif inp['K_source'] == 'labelled_weighted_norm':
        k_in = K_own_of(abs_tau, F(1) / rec['q'])
    elif inp['K_source'] == 'crude_analytic_disc':
        k_in = K_crude_b(abs_tau, rec['q'])
    else:
        raise Rejected('tier mixing: input vocabulary')
    far = far_constants(abs_tau, inp['theta'], inp['e_b'], rec['tier'])
    return assemble(k_in, rec['q'], far, site0=inp['site0'], form=rec['form'])


def validate(pk, c):
    if pk['contract_sha256'] != CONTRACT_SHA256:
        raise Rejected('contract hash')
    if sorted(pk['controls_executed']) != sorted(c['controls']) or not all(
            v is True for v in pk['controls_executed'].values()):
        raise Rejected('control boolean')
    if sorted(pk['snapshots']) != sorted(c['inventory']):
        raise Rejected('snapshot missing')
    if has_float([pk['tau_abs'], pk['constants'], pk['scaling'], pk['lemma'], pk['proof_weights']]):
        raise Rejected('exact arithmetic')
    for key in ('continuum_claim', 'scientific_priority_verified', 'weak_coupling_claim'):
        if pk['claims'].get(key) is not False:
            raise Rejected('forbidden claim ' + key)
    if pk['model_id'] != MODEL_ID or pk['triple'] != ['0', '0', '0'] or pk['tau_abs'] != c['tau_abs'] \
            or pk['signs'] != ['+', '-'] or pk['N_min'] != 2 or pk['metric'] != 'coarse_linf' or pk['d_X'] != 1:
        raise Rejected('changed model relabelled')
    if pk['families'] != ['F1', 'F2'] or pk['family_defs'] != c['family_defs']:
        raise Rejected('two families not named')
    missing = [k for k in c['parameter_keys_required'] if k not in pk['parameters_declared']]
    if missing:
        raise Rejected('parameters field missing: ' + ','.join(missing))
    if pk['clock'] != CLOCK or pk['window'] != WINDOW:
        raise Rejected('clock')
    if any(v != {'clock': CLOCK, 'tau_abs': c['tau_abs']} for v in pk['clock_by_comparison'].values()) \
            or sorted(pk['clock_by_comparison']) != sorted(c['comparisons']):
        raise Rejected('common clock')
    if pk['topology'] != TOPOLOGY or pk['fixtures'].get('fixed_versus_moving_vector', {}).get('exhibited') is not True:
        raise Rejected('topology')
    fx = pk['fixtures']
    for name in REQUIRED_FIXTURES:
        row = fx.get(name)
        if row is None or row.get('exhibited') is not True:
            raise Rejected('fixture missing: ' + name)
        if row.get('model_is_finite_graph') is not True or row.get('transfers_to_aq') is not False:
            raise Rejected('fixture label: ' + name)
    dec = pk['decomposition']
    if dec != c['decomposition']:
        raise Rejected('decomposition')
    lem = pk['lemma']
    for key in ('eta', 'kappa_0', 'w_prime', 'p'):
        if key not in lem or not isinstance(lem[key], F):
            raise Rejected('marginal-locality lemma: constant %s not an exact rational' % key)
    if lem['kp_asserted_without_counts'] is not False or lem['form'] != c['lemma_form']:
        raise Rejected('marginal-locality lemma: form')
    if lem['w_prime'] <= 1:
        raise Rejected('marginal-locality lemma: form')
    ci = pk['coefficient_input']
    if ci['every_site'] is not True or ci['far_site_input'] != 'every_site_form':
        raise Rejected('every-site coefficient input: R-only input at far sites')
    if ci['form'] == 'b' and (ci['proved_in_full'] is not True or ci['cited_as_admitted'] is not False):
        raise Rejected('every-site coefficient input: restated form cited as admitted')
    if ci['exponent'] != 'N-|u|_inf':
        raise Rejected('every-site coefficient input: exponent')
    if ci['form'] == 'a' and ci['K_label'] != 'labelled_weighted_norm':
        raise Rejected('every-site coefficient input: form (a) constants are labelled values')
    if ci['outside_smaller_box'] != 'anchored norm 2 tbar':
        raise Rejected('every-site coefficient input: outside the smaller box')
    mw = pk['mixed_weight']
    if mw['used'] is True and (mw['proved_in_full'] is not True or mw['cited_from'] is not None):
        raise Rejected('mixed-weight lemma not proved')
    if mw['loss_per'] != 'interaction':
        raise Rejected('mixed-weight lemma: loss per creation')
    pw = pk['proof_weights']
    if pw['declared_before_constants'] is not True:
        raise Rejected('rate constant pair: proof weights declared after constants')
    if pw['theta'] * pw['e_b'] ** 4 > c['w_max'] or pw['theta'] < 1 or pw['e_b'] < 1:
        raise Rejected('rate constant pair: proof weight outside the admissible range')
    if mw['loss'] != pw['theta'] * pw['e_b'] ** 4:
        raise Rejected('mixed-weight lemma: loss per creation')
    st = pk['straddling']
    if st['included'] is not True:
        raise Rejected('normalization couples supports: straddling supports dropped')
    if st['charged_beyond_first_order'] is not True:
        raise Rejected('normalization couples supports: straddling charged only at first order')
    if st['normalization'] != 'exact ratio (Tr N_c >= 1)':
        raise Rejected('normalization couples supports: normalization')
    if pk['outside_state']['gap_argument'] is not False:
        raise Rejected('outside vector is not a ground state')
    if pk['locality_mechanism'] != 'coefficient input and straddle recursion':
        if pk['locality_mechanism'] == 'global overlap':
            raise Rejected('global fidelity route')
        raise Rejected('global Lipschitz as decay')
    if pk['lipschitz_decay_factor'] is not None:
        raise Rejected('global Lipschitz as decay')
    an = pk['analyticity']
    if an['density_analytic_claimed'] is not False and an['zero_free_region'] is None:
        raise Rejected('zero-free region required')
    po = pk['polymer']
    if po['identity_checked'] is not True:
        raise Rejected('polymer identity')
    if po['kp_function'] != 'a|X_gamma|':
        if po['kp_function'] == 'a' and c['kp_nocard_exact_lower'] > c['kp_nocard_bound']:
            raise Rejected('polymer cardinality factor dropped')
        raise Rejected('polymer identity')
    sop = pk['second_order']
    if sop['claimed_derivative'] != c['second_order_derivative']:
        raise Rejected('second-order propagation')
    if 2 * sop['per_link_factor_sq'] * c['second_order_delta_e'] < c['second_order_offdiag_change_twice']:
        raise Rejected('second-order propagation: per-link factor below the exact one')
    sp = pk['split']
    if sp['charging'] != 'per_site':
        if sp['charging'] == 'product_of_region_sizes' and c['product_charging_increases']:
            raise Rejected('split charging: product of growing region sizes')
        raise Rejected('split charging')
    if sp['trace_N_ge_1_checked'] is not True or sp['lipschitz_checked'] is not True:
        raise Rejected('split charging: trace or Lipschitz unchecked')
    if pk['marginal'] != {'state_decay_inferred_from_coefficients': False, 'fixture_exhibited': True}:
        raise Rejected('marginal: coefficient decay is not marginal decay')
    cut = pk['cutoff']
    if cut['uniform_in_L'] is not True or cut['removal'] != 'AV1 F20-F23 at fixed N (F2 via AY1)':
        raise Rejected('cutoff uniform then removed')
    if cut['vector_convergence'] is not True or cut['eigenvalue_only'] is not False:
        raise Rejected('cutoff vector removal')
    if cut['order'] != 'L to infinity at fixed N; N never inside a fixed Q_L' or cut['limits_swapped'] is not False:
        raise Rejected('cutoff limit order')
    comps = pk['comparisons']
    if sorted(comps) != sorted(c['comparisons']):
        raise Rejected('comparison set')
    for name, row in comps.items():
        if row['covered'] is not True or row['constant'] != 'C':
            raise Rejected('comparison not covered: ' + name)
        if row['route'] not in ('direct', 'nested'):
            if row['route'] == 'union' and row.get('labelled') is not True:
                raise Rejected('comparison: union factor 2 not labelled')
            raise Rejected('comparison route')
    reg = pk['region']
    if reg['Y_dependence'] != '|Y| e^{|Y|/10^8}' or reg['exponent'] != 'd_Y = N - max_y |y|_inf':
        raise Rejected('region constant scales with Y')
    if reg['R_constant_reused'] is not False:
        raise Rejected('region constant scales with Y: R constant reused on Y')
    if pk['rate_units'] != RATE_UNITS or pk['rate_in_a'] is not False or pk['physical_length'] is not None:
        raise Rejected('rate in a')
    if pk['uniform_in'] != UNIFORM_IN:
        raise Rejected('uniform in a')
    if pk['combine'] != 'linear':
        raise Rejected('root-N or non-linear combination')
    # constants
    ids = set()
    for rec in pk['constants']:
        if rec['tier'] not in TIERS or rec['route'] not in ROUTES or rec['inputs']['K_source'] not in INPUTS:
            raise Rejected('tier mixing: vocabulary')
        if rec['tier'] == 'exact_first_order' and rec['inputs']['K_source'] not in EXACT_INPUTS:
            raise Rejected('tier mixing: crude input under an exact label')
        if rec['tier'] == 'crude_majorant' and rec['inputs']['K_source'] in EXACT_INPUTS:
            raise Rejected('tier mixing: exact input under a crude label')
        pair = c['pairs'].get(rec['pair'])
        if pair is None or rec['q'] != pair['q'] or rec['target'] != pair['target'] or rec['form'] != pair['form']:
            raise Rejected('rate constant pair not the frozen pair')
        if rec['inputs']['theta'] != pw['theta'] and rec['pair'] in ('headline', 'region'):
            raise Rejected('rate constant pair: proof weight not the declared one')
        if rec['value'] < recompute_constant(rec, pk['tau_abs']):
            raise Rejected('constant not reproduced from its declared inputs')
        if rec['meets_target'] != (rec['value'] <= rec['target']):
            raise Rejected('insufficient verdict: target flag')
        if rec['signs'] != ['+', '-']:
            raise Rejected('changed model relabelled: one sign')
        if rec['form'] == 'region' and rec['tier'] == 'exact_first_order' and rec['beta'] > F(1, 10 ** 8):
            raise Rejected('region constant scales with Y: exponent above 1/10^8')
        ids.add(rec['id'])
    if not {'C_headline', 'c_site_region', 'C_secondary', 'c_site_secondary'} <= ids:
        raise Rejected('rate constant pair: headline, region or secondary constant missing')
    if pk['q_optimized_per_N'] is not False:
        raise Rejected('rate constant pair: q optimized after the constants were seen')
    missed = [r_['id'] for r_ in pk['constants'] if not r_['meets_target']]
    if sorted(m_['id'] for m_ in pk['missed']) != sorted(missed) or any(
            m_['retuned'] is not False or not m_['dominating_term'] for m_ in pk['missed']):
        raise Rejected('insufficient verdict retained')
    for rec in pk['constants']:
        if rec['pair'] in ('headline', 'region') and rec['tier'] == 'exact_first_order' and not rec['meets_target'] \
                and pk['verdict'] == 'accepted_within_scope':
            raise Rejected('insufficient verdict retained')
    for cid, ratio in pk['scaling'].items():
        br = pk['scaling_bracket_of'].get(cid)
        if br not in c['brackets']:
            raise Rejected('tau scaling exponent: bracket missing for ' + cid)
        lo, hi = c['brackets'][br]
        if not (lo <= ratio <= hi):
            raise Rejected('tau scaling exponent: ' + cid)
    if pk['brackets_declared'] != c['brackets_text']:
        raise Rejected('tau scaling exponent: bracket chosen after evaluation')
    if pk['sub_labels'] != c['sub_labels']:
        raise Rejected('gate field: sub-label')
    for text in pk['limit_statements']:
        low = text.lower()
        if 'whole sequence' not in low and 'subsequence' not in low and 'per comparison' not in low:
            raise Rejected('subsequence versus whole sequence')
    if pk['gate_fields'].get('whole_sequence_claimed') is not False:
        raise Rejected('subsequence versus whole sequence: whole_sequence_claimed')
    if pk['gate_fields'].get('uniqueness_of_ground_state_claimed') is not False:
        raise Rejected('named construction is not uniqueness')
    if pk['gate_fields'] != c['gate_fields']:
        raise Rejected('gate field')
    if pk['sentence'] != c['sentence']:
        raise Rejected('mandatory sentence')
    for text in pk['statements']:
        if re.search(r'\buniform in a\b', text, re.I) and not NEGATION.search(text):
            raise Rejected('uniform in a')
        hits = phrase_hits(text, c['forbidden'], c['sentence'])
        if hits:
            if any('unique' in h['phrase'] or 'thermodynamic' in h['phrase'] or 'infinite-volume' in h['phrase']
                   for h in hits):
                raise Rejected('named construction is not uniqueness: forbidden phrasing')
            raise Rejected('forbidden phrasing')
    for text in pk['contract_strings']:
        if placeholder_spans(text):
            raise Rejected('placeholder span')
    inv = pk['reverse_inputs']
    if sorted(inv) != sorted(c['inventory']):
        extra = sorted(set(inv) - set(c['inventory']))
        if any(('round33/skeptic/' in p_ and not p_.endswith(('/ba1.md', '/ba2.md'))) or 'deliberation' in p_
               or 'round33/experts/' in p_ or '/forward/bb1/' in p_ or '/bb2/' in p_ or 'plan.json' in p_
               for p_ in extra):
            raise Rejected('reverse premise isolation')
        raise Rejected('reverse premise inventory')
    return True


# ---------------------------------------------------------------- execute
def execute():
    contract_bytes = CONTRACT.read_bytes()
    c_sha = hashlib.sha256(contract_bytes).hexdigest()
    need(c_sha == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=c_sha)
    con = json.loads(contract_bytes)
    par, pre = con['parameters'], con['preregistration']
    for rel, sha in sorted(PINNED.items()):
        got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if got != sha:
            raise CheckFailure('pinned premise changed: ' + rel)
    need(True, 'premise_sha256_pinned', files=sorted(PINNED))
    tau = F(pre['tau']['value'])
    need(con['status'] == 'frozen_before_production' and con['id'] == 'BB1' and tau == F(1, 10 ** 8)
         and pre['tau']['signs_evaluated'] == ['+', '-'] and pre['model_id'] == MODEL_ID
         and pre['selected_triple_alpha_units'] == ['0', '0', '0'] and con['direction'] == 'paired'
         and con['producers'] == ['forward', 'reverse'] and con['reverse_premise_isolation'] is True
         and par['N_min'] == '2', 'contract_model_tau_signs_read', tau=q(tau))
    rcp = par['rate_constant_pair']
    q_head, c_head = F(rcp['headline']['q']), F(rcp['headline']['C_target'])
    q_reg, c_reg = F(rcp['region_form']['q']), F(rcp['region_form']['c_site_target'])
    c2_t, cs2_t = F(rcp['secondary']['C_target']), F(rcp['secondary']['c_site_target'])
    q2 = 151552 * tau
    need(q_head == F(1, 64) == q_reg and c_head == F(1, 250000) and c_reg == F(1, 500000)
         and c2_t == F(1, 20000) and cs2_t == F(1, 40000) and rcp['secondary']['q'].startswith('151552|tau|')
         and rcp['headline']['tier'] == 'exact_first_order' and pre['target']['value'] == '1/250000 and 1/500000'
         and pre['target']['comparator'] == '<=' and 'e^{|Y|/10^8}' in rcp['region_form']['form']
         and 'd_Y = N - max_{y in Y} |y|_inf' in rcp['region_form']['form'],
         'contract_frozen_pairs_read', headline=[q(q_head), q(c_head)], region=[q(q_reg), q(c_reg)],
         secondary=[q(q2), q(c2_t), q(cs2_t)])
    controls = list(con['controls'])
    need(controls == pre['controls_required']['ids'] and len(controls) == 37 and len(set(controls)) == 37,
         'contract_control_mirror', controls=37, mirror=37)
    ncs = con['new_control_semantics']
    ba1c = json.loads((ROOT / 'research/round33/contracts/ba1.json').read_text())
    inherited = sorted(set(controls) - set(ncs))
    need(len(ncs) == 21 and not (set(ncs) - set(controls)) and len(inherited) == 16
         and all(k in ba1c['new_control_semantics'] for k in inherited), 'contract_control_semantics_coverage',
         with_bb1_semantics=len(ncs), inherited_from_ba1=inherited,
         note='every control without BB1 semantics is defined in the frozen BA1 contract (plan rule met)')
    gate_fields = dict(pre['gate_fields_required'])
    need(len(gate_fields) == 11 and gate_fields['state_decay_claimed'] is True
         and gate_fields['rate_in_N_claimed'] is True and gate_fields['whole_sequence_claimed'] is False
         and gate_fields['uniqueness_of_ground_state_claimed'] is False
         and gate_fields['common_limit_claimed'] is False, 'contract_gate_fields_read', fields=sorted(gate_fields))
    sentence = pre['mandatory_sentence_template']
    need('C q^(N-1)' in sentence and 'in each on-site cutoff space' in sentence and 'untruncated' in sentence
         and 'not uniqueness of any ground state' in sentence, 'contract_sentence_template_read')
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])
    need(phrase_hits(sentence, forbidden) == [], 'template_phrase_scan_clean_without_removal',
         scanned_phrases=len(forbidden))
    other = [s for k, v in con.items() if k not in ('preregistration',) for s in strings_of(v)]
    other += [s for k, v in pre.items() if k not in ('mandatory_sentence_template', 'forbidden_phrasings')
              for s in strings_of(v)]
    aff = [h for s in other for h in phrase_hits(s, forbidden, sentence)]
    need(aff == [], 'contract_fields_phrase_scan_clean', strings=len(other))
    spans = [s for text in strings_of(con) for s in placeholder_spans(text)]
    need(spans == [] and placeholder_spans('N at least 2 and J<=28|tau|') == []
         and placeholder_spans('<to be filled>') == ['<to be filled>'], 'contract_R1_placeholder_mirror_clean')
    inventory = sorted(['AGENTS.md', CONTRACT_REL] + list(con['shared_premises']))
    need(len(inventory) == 35 and len(set(inventory)) == 35 and all((ROOT / p_).is_file() for p_ in inventory)
         and not any(('round33/skeptic/' in p_ and not p_.endswith(('/ba1.md', '/ba2.md'))) or 'deliberation' in p_
                     or 'round33/experts/' in p_ or 'plan.json' in p_ or '/bb2/' in p_ for p_ in inventory),
         'contract_reverse_inventory_derivable', files=len(inventory),
         note='the two producer inputs/ folders were listed and hashed outside this program: 35 files each, '
              'byte-identical to the repository, equal to this list')
    brackets_text = dict(pre['scaling_brackets_per_constant'])
    need(brackets_text['C_headline'].startswith('[95,105]') and brackets_text['c_site'] == '[95,105]'
         and brackets_text['secondary_constants'].startswith('[99/100,101/100]')
         and brackets_text['q_secondary'] == 'exactly 100', 'contract_scaling_brackets_read')
    brackets = {'C_headline': (F(95), F(105)), 'c_site': (F(95), F(105)),
                'secondary_constants': (F(99, 100), F(101, 100)), 'q_secondary': (F(100), F(100))}
    need(par['window'].startswith('not applicable') and 'l-infinity' in par['metric'] and 'star diameter 1'
         in par['metric'] and '1/(37888|tau|)' in par['weights'] and 'w e^{4b}' in par['weights']
         and '8*2^{diam I}' in par['weights'] and 'F20-F23' in par['cutoff'] and 'AY1' in par['cutoff']
         and len(par['comparisons']) == 5 and 'compared directly' in par['comparisons'][4]
         and 'K=49/111790368' in par['coefficient_input'], 'contract_parameters_read', keys=sorted(par))
    # the skeptic's 17 pre-freeze replacement texts, found verbatim
    review = json.loads((ROOT / REVIEW_REL).read_text())
    edits = review['bb1']['blocking'] + review['bb1']['non_blocking']
    verbatim = [e['path'] for e in edits if json_path_get(con, e['path']) == e['replacement']]
    need(len(edits) == 17 and len(verbatim) == 17 and len(review['bb1']['blocking']) == 7,
         'prefreeze_edits_verbatim_in_frozen_bytes', blocking=7, non_blocking=10, paths=verbatim)
    ba1g = json.loads((ROOT / 'research/round33/advisor/ba1-gate.json').read_text())
    av1g = json.loads((ROOT / 'research/round32/advisor/av1-gate.json').read_text())
    ay1g = json.loads((ROOT / 'research/round32/advisor/ay1-gate.json').read_text())
    ay2g = json.loads((ROOT / 'research/round32/advisor/ay2-gate.json').read_text())
    rev_ba1 = (ROOT / 'research/round33/reverse/ba1/report.md').read_text()
    fwd_ba1 = (ROOT / 'research/round33/forward/ba1/report.md').read_text()
    av1f = (ROOT / 'research/round32/forward/av1/report.md').read_text()
    need('K=49/111790368' in ba1g['accepted'] and 'for u in R' in ba1g['decision']
         and 'K=2734375/12204185915601' in ba1g['accepted'] and 'Theorem 4.1' in rev_ba1
         and 'for `u` in `R`' in rev_ba1 and 'Lemma 3.1 (common core)' in rev_ba1
         and 'K_{\\rm own}=\\frac{T_w}{1-\\Gamma}' in fwd_ba1 and '19140625/86785322066496' in fwd_ba1
         and 't<=t_1/(1-352J)' in av1g['accepted'] and 'HNM-AV1-F22' in av1f and 'HNM-AV1-F09' in av1f
         and 'cutoff-vector removal' in ay1g['accepted']
         and '10 faces with owner set exactly R' in ay2g['accepted'], 'admitted_inputs_bound_to_premises',
         note='the BA1 gate admits the bound for u in R only; form (b) at every u is a BB1 lemma re-proved here')

    # 1. geometry: classes and the every-site source distances
    i1 = parse_i1_table((ROOT / 'research/round21/forward/i1/report.md').read_text())
    need(class_table() == i1 and len(CLASSES) == 24 and len(OMITTED) == 21, 'face_classes_match_I1_table')
    fams = {}
    for mm in (2, 3, 4, 5):
        fams[('F1', mm)] = f1_faces(cube(mm))
        fams[('F2', mm)] = f2_faces(cube(mm))
    order = [('F1', 2), ('F2', 2), ('F1', 3), ('F2', 3), ('F1', 4), ('F2', 4), ('F1', 5), ('F2', 5)]
    every_site_rows = []
    for i_, a_key in enumerate(order):
        for b_key in order[i_ + 1:]:
            small, big = fams[a_key], fams[b_key]
            nn = a_key[1]
            if nn == 5:
                continue
            if not set(small) <= set(big):
                raise CheckFailure('face sets not nested')
            src_sites = set().union(*[big[k] for k in big if k not in small])
            min_norm = min(norm_inf(p_) for p_ in src_sites)
            row = {'smaller': '%s_%d' % a_key, 'larger': '%s_%d' % b_key, 'min_source_norm_inf': min_norm,
                   'source_faces': sum(1 for k in big if k not in small)}
            if nn <= 3 and b_key[1] <= nn + 1:
                lam = cube(nn)
                att = 0
                for u in sorted(lam):
                    dd = set_dist(u, src_sites, dinf)
                    if dd < nn - norm_inf(u):
                        raise CheckFailure('every-site distance violated')
                    att += dd == nn - norm_inf(u)
                row['sites_checked'] = len(lam)
                row['sites_attaining_N_minus_norm'] = att
            if min_norm != nn:
                raise CheckFailure('source sites not at |p|_inf >= N with equality')
            every_site_rows.append(row)
    need(len(every_site_rows) == 27, 'every_site_sources_all_centered_pairs',
         pairs=every_site_rows, note='F1_N in F2_N in F1_(N+1) in F2_(N+1); every source site has |p|_inf >= N '
                                     '(attained), so d_inf(u, sources) >= N-|u|_inf for every u in Lambda_N; '
                                     'checked site by site on Lambda_2 and Lambda_3')
    gv_rows = {}
    for nn in (2, 3):
        v1 = cuboid((-nn, -nn, -nn), (nn + 1, nn, nn + 2))
        v2 = cuboid((-nn - 1, -nn, -nn), (nn, nn + 1, nn))
        for pres, fn in (('F1', f1_faces), ('F2', f2_faces)):
            a_, b_ = fn(v1), fn(v2)
            sym = [a_[k] for k in a_ if k not in b_] + [b_[k] for k in b_ if k not in a_]
            pts = set().union(*sym)
            mn = min(norm_inf(p_) for p_ in pts)
            if mn < nn:
                raise CheckFailure('general-volume source inside Lambda_(N-1)')
            gv_rows['N=%d_%s' % (nn, pres)] = {'symmetric_difference_faces': len(sym), 'min_source_norm_inf': mn}
    need(True, 'every_site_sources_general_volumes', cases=gv_rows,
         note='direct comparison of two volumes of one prescription containing Lambda_N: every term present in one '
              'and not the other contains a site outside Lambda_N and has diameter 1, so all its sites have '
              '|p|_inf >= N (all sizes)')
    size_rows = [(dd, (1 + dd) ** 3, 8 * 2 ** dd) for dd in range(0, 65)]
    need(all(a <= b for _, a, b in size_rows) and [dd for dd, a, b in size_rows if a == b] == [3],
         'support_size_diameter_bound', statement='|I| <= (1+diam I)^3 <= 8*2^(diam I), equality only at diam 3')
    # cardinality excess of AM2 words (generic 16 output sets) and the face order count
    x_star = frozenset(S_STAR)
    cands = sorted({frozenset(add(b, d) for d in k['rel']) for k in OMITTED
                    for b in {sub(p_, d) for p_ in S_STAR for d in k['rel']}
                    if frozenset(add(b, d) for d in k['rel']) & x_star}, key=lambda s: sorted(s))
    exc = {0: set(), 1: set(), 2: set()}
    words = 0
    for k in (0, 1, 2):
        for combo in combinations(cands, k):
            if any(a & b for a, b in combinations(combo, 2)):
                continue
            nset = frozenset().union(*combo) if combo else frozenset()
            base = nset - x_star
            for msk in range(16):
                ys = frozenset(S_STAR[i] for i in range(4) if msk >> i & 1)
                m_ = base | ys
                if not m_ or not (m_ <= nset | x_star):
                    continue
                words += 1
                exc[k].add(len(m_) - sum(len(i_) for i_ in combo))
    osets = sorted({own for fam in (fams[('F1', 2)],) for own in fam.values()}, key=lambda s: sorted(s))
    near0 = [s for s in osets if dinf(ORIGIN, sorted(s)[0]) <= 2]
    pair_union = max(len(a | b) for a, b in combinations(near0, 2) if a & b)
    need(max(exc[0]) == 4 and max(exc[1]) <= 3 and max(exc[2]) <= 3 and max(len(s) for s in osets) == 3
         and pair_union == 5, 'cardinality_loss_and_face_order_count', words=words,
         max_excess_k0=4, max_excess_k1=max(exc[1]), max_excess_k2=max(exc[2]),
         note='|M| <= |X| + sum|I_j| (loss e^{4b}, attained by the generic k=0 count; e^{3b} suffices for k>=1); '
              'owner sets have at most 3 sites, so a connected family of n faces covers at most 2n+1 sites and a '
              'support M arises only at order >= ceil((|M|-1)/2)')

    # 2. constants: coefficient inputs
    signs = (tau, -tau)
    at = abs(tau)
    j0 = j_of(at)
    w_max = w_max_of(at)
    tb = tbar_of(at)
    k_b = K_form_b(at, q_head)
    k_own = K_own_of(at, F(64))
    k_gen = K_gen_of(at, F(64))
    k_crude = K_crude_b(at, q_head)
    rho2 = at / q2
    k_2 = K_form_b(at, q2)
    need(k_b == F(49, 111790368) and k_own == F(19140625, 86785322066496) and k_gen == F(2734375, 12204185915601)
         and k_crude == F(296, 390625) and k_2 == F(49, 10202112) and rho2 == F(1, 151552)
         and w_max == F(390625, 148) and tb == F(49, 14398580736), 'coefficient_inputs_exact',
         K_form_b=q(k_b), K_own_form_a=q(k_own), K_gen_forward_telescoped=q(k_gen), K_crude=q(k_crude),
         K_secondary_reinstantiated=q(k_2), tbar=q(tb),
         note='form (b) constant 2T(rho) is uniform in u; the secondary radius |tau|/q_2=1/151552 is not a gate radius '
              '(labelled re-instantiation)')
    # 3. proof weights and the far recursion
    theta = F(1) / q_head
    e_b = F(9, 8)
    loss = theta * e_b ** 4
    far = far_constants(at, theta, e_b)
    need(loss == F(6561, 64) and loss <= w_max and far['beta'] <= F(1, 10 ** 8) and far['A'] < F(1, 100000)
         and j0 * loss * G_R <= R, 'proof_weights_admissible', theta=q(theta), e_b=q(e_b), loss=q(loss),
         w_max=q(w_max), beta=q(far['beta']), eps_lower=q(far['eps']), M=q(far['M']), t_prime=q(far['t_prime']),
         A=q(far['A']), A_preview=preview(far['A']),
         note='declared before any constant: creation weight theta=1/q=64, cardinality factor e^b=9/8 (b>=2/17 by '
              'the log bound), loss theta e^{4b}=6561/64 per interaction, far factor A=4M/(eps e-4M)')
    theta2 = F(1) / q2
    far2 = far_constants(at, theta2, e_b)
    need(theta2 * e_b ** 4 <= w_max and far2['beta'] <= F(1, 10 ** 8), 'proof_weights_admissible_secondary',
         theta=q(theta2), loss=q(theta2 * e_b ** 4), A=q(far2['A']), A_preview=preview(far2['A']))
    # 4. assembled constants, both signs, every comparison
    const = {}
    for sgn in signs:
        a_t = abs(sgn)
        fr = far_constants(a_t, theta, e_b)
        fr2 = far_constants(a_t, F(1) / (151552 * a_t), e_b)
        kb = K_form_b(a_t, q_head)
        ko = K_own_of(a_t, F(64))
        kg = K_gen_of(a_t, F(64))
        k2 = K_form_b(a_t, 151552 * a_t)
        kc = K_crude_b(a_t, q_head)
        frc = far_constants(a_t, theta, e_b, 'crude_majorant')
        row = {
            'C_b_every_site': assemble(kb, q_head, fr, 'N', 'R'),
            'C_b_R_only': assemble(kb, q_head, fr, 'N-1', 'R'),
            'c_site_b': assemble(kb, q_head, fr, form='region'),
            'C_a_own': assemble(ko, q_head, fr, 'N', 'R'),
            'c_site_a_own': assemble(ko, q_head, fr, form='region'),
            'C_a_gen': assemble(kg, q_head, fr, 'N', 'R'),
            'C_split_b_every_site': assemble_split(kb, q_head, fr, a_t, 'N'),
            'C_split_b_R_only': assemble_split(kb, q_head, fr, a_t, 'N-1'),
            'C_union_b_every_site': 2 * assemble(kb, q_head, fr, 'N', 'R'),
            'C_union_b_R_only': 2 * assemble(kb, q_head, fr, 'N-1', 'R'),
            'c_site_union_b': 2 * assemble(kb, q_head, fr, form='region'),
            'C_secondary_every_site': assemble(k2, 151552 * a_t, fr2, 'N', 'R'),
            'C_secondary_R_only': assemble(k2, 151552 * a_t, fr2, 'N-1', 'R'),
            'c_site_secondary': assemble(k2, 151552 * a_t, fr2, form='region'),
            'C_crude_every_site': assemble(kc, q_head, frc, 'N', 'R'),
            'C_crude_R_only': assemble(kc, q_head, frc, 'N-1', 'R'),
            'c_site_crude_own_exponent': assemble(kc, q_head, frc, form='region'),
        }
        const['+' if sgn > 0 else '-'] = row
    need(const['+'] == const['-'], 'both_signs_identical', note='every bound depends on |tau| only')
    cst = const['+']
    far_c = far_constants(at, theta, e_b, 'crude_majorant')
    need(cst['C_b_every_site'] <= c_head and cst['C_b_R_only'] <= c_head and cst['c_site_b'] <= c_reg
         and cst['C_a_own'] <= c_head and cst['c_site_a_own'] <= c_reg and cst['C_split_b_R_only'] <= c_head
         and cst['C_secondary_every_site'] <= c2_t and cst['C_secondary_R_only'] <= c2_t
         and cst['c_site_secondary'] <= cs2_t and cst['C_crude_every_site'] > c_head
         and cst['C_union_b_every_site'] <= c_head and cst['C_union_b_R_only'] <= c_head
         and cst['c_site_union_b'] <= c_reg and far_c['beta'] > F(1, 10 ** 8),
         'frozen_targets_met_crude_fails', margins={k: preview((c_head if k.startswith('C_') and 'secondary' not in k
                                                                  else c_reg if k.startswith('c_site') and
                                                                  'secondary' not in k else c2_t if
                                                                  k.startswith('C_') else cs2_t) / v)
                                                     for k, v in sorted(cst.items())},
         note='union comparisons (factor 2) pass here but are labelled only; the crude region constant needs its own '
              'exponent beta=%s > 1/10^8 and is never written in the frozen form' % preview(far_c['beta']))
    # recorded-preview structure (advisor previews), recomputed exactly for the post-comparison
    t_star = T_disc(F(1, 37888))
    eta_str = 32 * t_star / (1 - 32 * t_star)
    t_128 = T_disc(128 * at)
    eta_128 = 32 * t_128 / (1 - 32 * t_128)
    prev_split_R_only = 2 * (2 * k_b) * (1 + 2 * tb) * (1 + eta_str)
    prev_split_every = 2 * (k_b * q_head + k_b) * (1 + 2 * tb) * (1 + eta_str)
    prev_split_fwd = 2 * (k_gen * q_head + k_gen) * (1 + 2 * tb) * (1 + eta_str)
    w_c = F(390625, 296)
    s_prev = shell_sum(q_head * w_c)
    t_kp = 2 * t_star
    eta_far_prev = exp_up(F(2, 1000)) * 4 * t_kp * s_prev / (1 - 4 * t_kp)
    prev_poly_R_only = 2 * (2 * k_b) * (1 + tb) * (1 + eta_far_prev)
    need(eta_str == F(49, 126095) and prev_split_R_only == F(352765230433, 201124673670833280)
         and s_prev == F(99977074261152768, 51346528044814241) and prev_split_R_only <= c_head
         and prev_poly_R_only <= c_head and eta_128 < eta_str, 'recorded_preview_structure_recomputed',
         eta_str=q(eta_str), eta_str_T128=preview(eta_128), C_split_R_only=q(prev_split_R_only),
         C_split_R_only_preview=preview(prev_split_R_only), C_split_every_site=preview(prev_split_every),
         C_split_forward_Kgen=preview(prev_split_fwd), shell_sum=q(s_prev), eta_far_preview=preview(eta_far_prev),
         C_poly_R_only=preview(prev_poly_R_only),
         note='the recorded split structure 2(d_0+d_ez)(1+2tbar)(1+32T_*/(1-32T_*)) charges |I|<=8*2^diam at creation '
              'weight 2/q bounded by T_*; it does not charge the normalization of intermediate regions (reading R6)')
    # 5. scaling
    small = tau / 100
    fr_s = far_constants(small, theta, e_b)
    fr2_s = far_constants(small, F(1) / (151552 * small), e_b)
    ratios = {
        'C_headline_every_site': cst['C_b_every_site'] / assemble(K_form_b(small, q_head), q_head, fr_s, 'N', 'R'),
        'C_headline_R_only': cst['C_b_R_only'] / assemble(K_form_b(small, q_head), q_head, fr_s, 'N-1', 'R'),
        'c_site': cst['c_site_b'] / assemble(K_form_b(small, q_head), q_head, fr_s, form='region'),
        'C_headline_form_a': cst['C_a_own'] / assemble(K_own_of(small, F(64)), q_head, fr_s, 'N', 'R'),
        'C_secondary': cst['C_secondary_every_site'] / assemble(K_form_b(small, 151552 * small), 151552 * small,
                                                                  fr2_s, 'N', 'R'),
        'c_site_secondary': cst['c_site_secondary'] / assemble(K_form_b(small, 151552 * small), 151552 * small,
                                                                 fr2_s, form='region'),
        'q_secondary': q2 / (151552 * small),
        'C_recorded_split_R_only': prev_split_R_only / (2 * (2 * K_form_b(small, q_head)) * (1 + 2 * tbar_of(small))
                                                        * (1 + eta_str)),
    }
    hb, sb = brackets['C_headline'], brackets['secondary_constants']
    need(all(hb[0] <= ratios[k] <= hb[1] for k in ('C_headline_every_site', 'C_headline_R_only', 'c_site',
                                                   'C_headline_form_a', 'C_recorded_split_R_only'))
         and sb[0] <= ratios['C_secondary'] <= sb[1] and sb[0] <= ratios['c_site_secondary'] <= sb[1]
         and ratios['q_secondary'] == 100, 'tau_scaling_in_brackets',
         ratios={k: preview(v) for k, v in ratios.items()})
    kb_ratio = k_b / K_form_b(small, q_head)
    need(kb_ratio == F(4340004, 43129) and k_2 == K_form_b(small, 151552 * small), 'input_scaling_exact',
         K_ratio=q(kb_ratio), note='the form (b) input is linear with ratio 4340004/43129; the secondary input is '
                                   'exactly tau-invariant (rho_2=1/151552 at every tau)')
    # 6. KP feasibility and the mixed-weight loss (polymer route)
    a_kp = F(1, 1000)
    w_kp = F(1024)
    t_kp_mix = T_mix(at, w_kp, e_b)
    zeta = ln_lo(e_b) - a_kp / 2 - 2 * t_kp_mix
    kp_sum = 4 * t_kp_mix ** 2 / (exp_lo(F(1)) * zeta)
    need(w_kp * e_b ** 4 <= w_max and zeta > 0 and kp_sum <= a_kp and shell_sum(q_head * w_kp) < 3,
         'kp_condition_feasible', a=q(a_kp), cluster_weight=q(w_kp), e_b=q(e_b), loss=q(w_kp * e_b ** 4),
         T_mixed=preview(t_kp_mix), zeta=preview(zeta), kp_sum_bound=preview(kp_sum),
         shell_sum_qW=preview(shell_sum(q_head * w_kp)),
         note='sup_x sum_{gamma ni x}|w(gamma)| e^{a|X|} W^{diam X} <= 2Z sum nu(J)|J|e^{|J|Z} <= 4T^2/(e zeta) with '
              'Z=2T, b >= a/2+Z+zeta; the mixed weight carries the cardinality factor; KP holds by about six '
              'orders of magnitude')
    lip_omega = 2 * (2 * (1 + tb) ** 2 * (2 * tb + tb ** 2) + (2 * tb + tb ** 2) ** 2)
    need(lip_omega < F(148, 390625) and F(37, 6249384) == j0 * G_R / (1 - j0 * GP_R), 'density_lipschitz_not_decay',
         L_omega_R=q(lip_omega), L_omega_preview=preview(lip_omega), q_min='148/390625',
         note='the outside-state Lipschitz constant of rho_R (straddle-only refinement) is about 2.7e-8; used as a '
              'per-shell factor it would cross the BA1 floor q_min, so it is a Lipschitz constant, not a rate')

    # 7. fixtures
    fixtures = {}
    # (a) coefficient decay is not marginal decay (AV1 F13 type)
    f13 = {}
    for bb in (F(1, 2), F(0)):
        psi = state(3, [(mask_of(0, 1), F(1, 3)), (mask_of(1), bb), (mask_of(2), F(2, 5))])
        f13[str(bb)] = rdm(psi, [0], 3)[0]
    need(f13['1/2'] == [[F(45, 49), F(6, 49)], [F(6, 49), F(4, 49)]] and f13['0'] == [[F(9, 10), F(0)],
                                                                                     [F(0), F(1, 10)]],
         'fixture_coefficient_decay_not_marginal_decay', rho_b_half=[[q(x) for x in r_] for r_ in f13['1/2']],
         rho_b_zero=[[q(x) for x in r_] for r_ in f13['0']], model_is_finite_graph=True, transfers_to_aq=False)
    fixtures['coefficient_decay_not_marginal_decay'] = True
    # (b) second-order propagation: chain r - o - o'' with straddling a={r,o}, b={o,o''}, change only e={o''}
    va, vb, ve = P.var(0), P.var(1), P.var(2)
    psi_p = state(3, [(mask_of(0, 1), va), (mask_of(1, 2), vb), (mask_of(2), ve)], zero=PZ, one=P1)
    raw = rdm_raw(psi_p, [0], 3)
    zpoly = raw[0][0] + raw[1][1]
    need(raw[0][1] == -(va * vb * ve) and zpoly == (1 + va * va) * (1 + ve * ve) + vb * vb,
         'fixture_second_order_propagation_polynomial', offdiag_numerator='-a b e',
         normalization='(1+a^2)(1+e^2)+b^2', model_is_finite_graph=True, transfers_to_aq=False)
    a0, b0, de = F(1, 3), F(1, 4), F(1, 5)
    z0 = (1 + a0 * a0) + b0 * b0
    deriv = -a0 * b0 / z0
    rho_e = raw[0][1].at((a0, b0, de)) / zpoly.at((a0, b0, de))
    off_change_twice = 2 * abs(rho_e)
    need(deriv != 0 and 2 * (a0 * b0) ** 2 * de < off_change_twice <= 2 * a0 * b0 * de,
         'fixture_second_order_per_link_factor', derivative_at_0=q(deriv), offdiag_change=q(rho_e),
         note='the R-marginal moves at order a*b*e: a zero first-order propagation claim and a per-link factor '
              'a^2 (fourth order) both fail; the exact per-link factors are the straddling amplitudes')
    fixtures['second_order_propagation'] = True
    # (c) normalization: spectator independence (AV1 values) and global fidelity
    base = [(mask_of(0), F(1, 60)), (mask_of(1), F(1, 70)), (mask_of(0, 1), F(1, 50)), (mask_of(0, 2), F(1, 9)),
            (mask_of(1, 2), F(1, 10)), (mask_of(0, 1, 2), F(1, 11)), (mask_of(2), F(-1, 12))]
    base2 = [(m_, (F(1, 61) if m_ == mask_of(0) else a_)) for m_, a_ in base]
    weights, rhos, diffs, infid = [], [], [], []
    for k in range(4):
        n_ = 3 + k
        psi_a = state(n_, base + [(mask_of(3 + j), F(1, 6)) for j in range(k)])
        psi_b = state(n_, base2 + [(mask_of(3 + j), F(-1, 6)) for j in range(k)])
        weights.append(sum(psi_a[s] ** 2 for s in range(2 ** n_) if not (s & 3)))
        ra, rb = rdm(psi_a, [0, 1], n_)[0], rdm(psi_b, [0, 1], n_)[0]
        rhos.append(ra)
        diffs.append([[x - y for x, y in zip(r1, r2)] for r1, r2 in zip(ra, rb)])
        infid.append(1 - ip(psi_a, psi_b) ** 2 / (ip(psi_a, psi_a) * ip(psi_b, psi_b)))
    need(weights == [F(145, 144), F(5365, 5184), F(198505, 186624), F(7344685, 6718464)]
         and all(r_ == rhos[0] for r_ in rhos), 'fixture_normalization_spectators', weights=[q(w) for w in weights],
         model_is_finite_graph=True, transfers_to_aq=False,
         note='rho_R is identical for 0..3 decoupled spectators while <psi,P_R psi> runs through the AV1 values')
    fixtures['normalization_spectators'] = True
    ov0 = 1 - infid[0]
    need(all(d_ == diffs[0] for d_ in diffs) and any(x != 0 for r_ in diffs[0] for x in r_)
         and all(1 - infid[k] == ov0 * F(35, 37) ** (2 * k) for k in range(4))
         and all(infid[k + 1] > infid[k] for k in range(3)), 'fixture_global_fidelity',
         infidelities=[preview(x) for x in infid], per_spectator_overlap_squared='(35/37)^2',
         model_is_finite_graph=True, transfers_to_aq=False,
         note='the global overlap decays geometrically in the number of changed spectators while the R-marginal '
              'difference is fixed; any locality bound through the global overlap grows toward 2')
    fixtures['global_fidelity'] = True
    # (d) straddling supports: e first order, off-diagonal second order; first-order R-marginal
    aa, bb2 = F(1, 3), F(1, 2)
    psi = state(3, [(mask_of(0, 1), aa), (mask_of(1), bb2)])
    n_out = (1 + bb2 ** 2)
    d_sq = ip(psi, psi) - n_out
    first_order = {}
    labels = {'{r0}': mask_of(0), '{r1}': mask_of(1), '{r0,r1}': mask_of(0, 1), '{r0,o}': mask_of(0, 2),
              '{r1,o}': mask_of(1, 2), '{r0,r1,o} (strictly contains R)': mask_of(0, 1, 2), '{o}': mask_of(2)}
    for lab, msk in labels.items():
        amp = dict(base)[msk]
        eps_v = P.var(0)
        psi_e = state(3, [(msk, eps_v * amp)], zero=PZ, one=P1)
        raw_e = rdm_raw(psi_e, [0, 1], 3)
        ztot = raw_e[0][0] + raw_e[1][1] + raw_e[2][2] + raw_e[3][3]
        lin = [[raw_e[i][j].coeff(0, 1) - (raw_e[i][j].coeff(0, 0) * ztot.coeff(0, 1)) for j in range(4)]
               for i in range(4)]
        quad = [[raw_e[i][j].coeff(0, 2) for j in range(4)] for i in range(4)]
        first_order[lab] = {'first_order_zero': all(x == 0 for r_ in lin for x in r_),
                            'second_order_block_zero': all(x == 0 for r_ in quad for x in r_)}
    inside = [k for k in labels if k in ('{r0}', '{r1}', '{r0,r1}')]
    straddle = [k for k in labels if 'o' in k and k != '{o}']
    need(d_sq / n_out == aa ** 2 / (1 + bb2 ** 2) and f13['1/2'][0][1] == F(6, 49)
         and all(not first_order[k]['first_order_zero'] for k in inside)
         and all(first_order[k]['first_order_zero'] and not first_order[k]['second_order_block_zero']
                 for k in straddle) and first_order['{o}']['first_order_zero'],
         'fixture_straddling_supports', e_squared=q(d_sq / n_out), per_support=first_order,
         model_is_finite_graph=True, transfers_to_aq=False,
         note='a straddling creation enters e at first order but the off-diagonal marginal only at order a*b; every '
              'support meeting the complement of R, including {r0,r1,o} which strictly contains R, has zero '
              'first-order R-marginal and a nonzero second-order block; only supports contained in R move rho_R at '
              'first order (contract wording defect D1: "strictly containing R" should read "contained in R")')
    fixtures['straddling_supports'] = True
    # (e) the truncated-correlation reduction, the derivative identity and the near bound
    col = [(mask_of(0), F(1, 5)), (mask_of(0, 1), F(1, 3)), (mask_of(1), F(1, 4)), (mask_of(1, 2), F(1, 6)),
           (mask_of(2), F(1, 7))]
    psi = state(3, col)
    e_mat = [[F(1, 2), F(1, 3)], [F(1, 3), F(-1, 4)]]
    d_amp = F(1, 9)

    def op_e(v):
        return apply_op(v, e_mat, [0])

    def op_b(v):
        return cre(v, mask_of(2), d_amp)

    lhs = trunc(psi, op_e, op_b)
    phi = state(2, [(mask_of(0), F(1, 4)), (mask_of(0, 1), F(1, 6)), (mask_of(1), F(1, 7))])
    om_e = omega(psi, op_e)
    e_p = [[e_mat[a][b] - (om_e if a == b else 0) for b in range(2)] for a in range(2)]

    def embed(v2):
        out = [F(0)] * 8
        for s, x in enumerate(v2):
            out[s << 1] = x
        return out

    def x_apply(vec, crs):
        for mm, amp in crs:
            cc = cre(vec, mm, amp)
            vec = [x - y for x, y in zip(vec, cc)]
        return vec

    def g_op(mat, crs):
        gm = [[F(0)] * 4 for _ in range(4)]
        for v in range(4):
            for w in range(4):
                e1 = [F(0)] * 4
                e1[v] = F(1)
                e2 = [F(0)] * 4
                e2[w] = F(1)
                gm[v][w] = ip(x_apply(embed(e1), crs), apply_op(x_apply(embed(e2), crs), mat, [0]))
        return gm

    x_all = [(mask_of(0), F(1, 5)), (mask_of(0, 1), F(1, 3))]
    x_in = [(mask_of(0), F(1, 5))]
    g_ep = g_op(e_p, x_all)
    xin0 = x_apply(vac(3), x_in)
    g_scal = ip(xin0, apply_op(xin0, e_p, [0]))
    h_op = [[g_ep[v][w] - (g_scal if v == w else 0) for w in range(4)] for v in range(4)]
    g_one = g_op([[F(1), F(0)], [F(0), F(1)]], x_all)
    om_g1 = omega(phi, lambda v: matvec(g_one, v))
    rhs = trunc(phi, lambda v: matvec(h_op, v), lambda v: cre(v, mask_of(1), d_amp)) / om_g1
    g_minus = [[g_one[i][j] - (1 if i == j else 0) for j in range(4)] for i in range(4)]
    need(lhs == rhs and lhs != 0 and om_g1 >= 1 and psd(g_minus), 'fixture_truncated_correlation_reduction',
         omega_E_B=q(lhs), omega_phi_G1=q(om_g1),
         identity='omega(E;B) = omega_phi(H_{E-omega(E)};B)/omega_phi(G_1), G_1 >= 1 as an operator',
         model_is_finite_graph=True, transfers_to_aq=False)
    lam = P.var(0)
    dcol = [(mask_of(0), F(1, 11)), (mask_of(0, 1), F(-1, 13)), (mask_of(1, 2), F(1, 17))]
    dmap = dict(dcol)
    psi_l = state(3, [(mm, amp + lam * dmap.get(mm, F(0))) for mm, amp in col] +
                  [(mm, lam * amp) for mm, amp in dcol if mm not in dict(col)], zero=PZ, one=P1)
    deriv_vec = [x.coeff(0, 1).at((0, 0, 0)) for x in psi_l]
    psi0 = [x.coeff(0, 0).at((0, 0, 0)) for x in psi_l]
    dhat = [F(0)] * 8
    for mm, amp in dcol:
        cc = cre(psi0, mm, amp)
        dhat = [x + y for x, y in zip(dhat, cc)]
    need(deriv_vec == [-x for x in dhat] and psi0 == psi, 'fixture_derivative_identity',
         identity='d/dlambda psi(c+lambda delta) = -delta_hat psi (delta_I c_I = 0)', model_is_finite_graph=True,
         transfers_to_aq=False)
    a_obs = [[F(1, 2), F(1, 5)], [F(1, 5), F(-1, 3)]]
    var_a = omega(psi, lambda v: apply_op(apply_op(v, a_obs, [0]), a_obs, [0])) - omega(
        psi, lambda v: apply_op(v, a_obs, [0])) ** 2
    near_rows = []
    for mm, amp in dcol:
        if not (mm & 1):
            continue
        tv = trunc(psi, lambda v: apply_op(v, a_obs, [0]), lambda v, mm=mm, amp=amp: cre(v, mm, amp))
        pvac = sum(psi[s] ** 2 for s in range(8) if not (s & mm)) / ip(psi, psi)
        near_rows.append({'support_mask': mm, 'lhs_sq': q(tv * tv), 'rhs_sq': q(amp * amp * pvac * var_a)})
        if not tv * tv <= amp * amp * pvac * var_a:
            raise CheckFailure('near bound')
    need(len(near_rows) == 2 and var_a <= 1, 'fixture_near_support_variance_bound', rows=near_rows,
         bound='|omega(A;delta_hat_I)| <= ||delta_I|| ||<Omega_I|psi>||/||psi|| sqrt(Var A) <= ||delta_I||',
         model_is_finite_graph=True, transfers_to_aq=False)
    # (f) split: Tr N >= 1 and the outside-state Lipschitz bound on a mixed outside state
    xs = [(mask_of(0), F(1, 5)), (mask_of(0, 1), F(1, 4))]

    def n_map(om):
        out = [[F(0)] * 2 for _ in range(2)]
        for i in range(2):
            for j in range(2):
                if om[i][j] == 0:
                    continue
                ket = x_apply([F(1) if s == (i << 1) else F(0) for s in range(4)], xs)
                bra = x_apply([F(1) if s == (j << 1) else F(0) for s in range(4)], xs)
                for r_ in range(2):
                    for c_ in range(2):
                        out[r_][c_] += om[i][j] * sum(ket[r_ | (o << 1)] * bra[c_ | (o << 1)] for o in range(2))
        return out

    om1 = [[F(2, 3), F(1, 6)], [F(1, 6), F(1, 3)]]
    om2 = [[F(1, 2), F(-1, 5)], [F(-1, 5), F(1, 2)]]
    n1, n2 = n_map(om1), n_map(om2)
    tr1, tr2 = n1[0][0] + n1[1][1], n2[0][0] + n2[1][1]
    rho1 = [[x / tr1 for x in r_] for r_ in n1]
    rho2m = [[x / tr2 for x in r_] for r_ in n2]
    dl = [[a - b for a, b in zip(r1, r2)] for r1, r2 in zip(rho1, rho2m)]
    nd = n_map([[a - b for a, b in zip(r1, r2)] for r1, r2 in zip(om1, om2)])
    lhs_hi = trace_norm_2x2(dl)[1]
    rhs_lo = 2 * trace_norm_2x2(nd)[0]
    need(tr1 >= 1 and tr2 >= 1 and lhs_hi <= rhs_lo and psd(om1) and psd(om2), 'fixture_split_trace_and_lipschitz',
         trace_N=[q(tr1), q(tr2)], lhs_upper=preview(lhs_hi), rhs_lower=preview(rhs_lo),
         model_is_finite_graph=True, transfers_to_aq=False)
    fixtures['split_trace_and_lipschitz'] = True
    prod_b = [F(fact(k + 1), 10 ** k) for k in range(1, 16)]
    site_b = [F(1, 2 ** k) for k in range(1, 16)]
    increases = any(prod_b[k + 1] > prod_b[k] for k in range(len(prod_b) - 1))
    need(increases and prod_b[9] > prod_b[8] and all(site_b[k + 1] < site_b[k] for k in range(14)),
         'fixture_split_per_site_charging', product_charged=[q(x) for x in prod_b[7:11]],
         per_site=[q(x) for x in site_b[:4]], model_is_finite_graph=True, transfers_to_aq=False,
         note='charging the product of region sizes s_k=k+1 at amplitude 1/10 gives (k+1)!/10^k, increasing from k=9; '
              'per-site charging gives a geometric series')
    fixtures['split_per_site_charging'] = True
    # (g) polymer identity (four sites) and the cardinality factor
    sup = [((0,), F(1, 2)), ((1,), F(1, 3)), ((0, 1), F(1, 5)), ((1, 2), F(1, 7)), ((2, 3), F(1, 11)),
           ((0, 1, 2), F(1, 13)), ((3,), F(1, 17)), ((1, 2, 3), F(-1, 19))]
    psi4 = state(4, [(mask_of(*s_), a_) for s_, a_ in sup])
    plist, zero_pairs = enumerate_polymers(sup)

    brute = ip(psi4, psi4)
    zp = polymer_partition(plist, frozenset(range(4)))
    need(brute == zp and zero_pairs > 0 and len(plist) > 8, 'fixture_polymer_identity_brute_force', norm_squared=q(brute),
         polymers=len(plist), different_excitation_pairs_zero=zero_pairs, model_is_finite_graph=True,
         transfers_to_aq=False, note='(psi,psi) equals the hard-core polymer sum over compatible families of '
                                     'overlap-connected pairs (F,F\') with equal excitation sets')
    fixtures['polymer_identity'] = True
    a_c, u_c, v_c = F(1, 100), F(1, 20), F(1, 20)
    card_sup = [((0, 1, 2, 3), u_c)] + [((k, k + 4), v_c) for k in range(4)]
    card_poly, _ = enumerate_polymers(card_sup)
    kp_rows = []
    for key, xg, wg in card_poly:
        lhs_kp = sum((abs(w2) * exp_up(a_c * len(x2)) for _, x2, w2 in card_poly if x2 & xg), F(0))
        kp_rows.append((key, len(xg), lhs_kp))
        if lhs_kp > a_c * len(xg):
            raise CheckFailure('KP with cardinality fails on the fixture')
    g1 = [row for row in card_poly if row[0] == ((0,), (0,))][0]
    exact_single = sum((abs(w2) for _, x2, w2 in card_poly if x2 & g1[1]), F(0))
    need(len(card_poly) == 5 and all(k_[0] == k_[1] for k_, _, _ in card_poly) and exact_single == u_c ** 2 + 4 * v_c ** 2
         and exact_single > a_c and exact_single <= 4 * a_c,
         'fixture_polymer_cardinality_factor', exact_single_polymer_part=q(exact_single), bound_without_card=q(a_c),
         bound_with_card=q(4 * a_c), model_is_finite_graph=True, transfers_to_aq=False,
         note='J_0={0,1,2,3} (u=1/20) overlapped by four P_k={k,k+4} (v=1/20); KP with a(gamma)=a|X| holds, while the '
              'cluster sum incompatible with ({J_0},{J_0}) already exceeds the no-cardinality bound a=1/100')
    fixtures['polymer_cardinality_factor'] = True
    # (h) cutoff: Eckart with gap 1/2, degenerate counterexample, limit order, fixed versus moving vector
    ham = (F(0), F(1, 2), F(2))
    ek = []
    for sq in ((F(1, 9), F(4, 9), F(4, 9)), (F(5, 9), F(16, 45), F(4, 45)), (F(1), F(0), F(0))):
        e_l = sum(h * s_ for h, s_ in zip(ham, sq))
        ek.append((1 - sq[0], 2 * e_l))
    degenerate = (F(0), F(0), F(1))
    need(ek == [(F(8, 9), F(20, 9)), (F(4, 9), F(32, 45)), (F(0), F(0))] and all(a_ <= b_ for a_, b_ in ek)
         and degenerate[1] == degenerate[0] and 1 > 2 * degenerate[1], 'fixture_cutoff_eckart',
         pairs=[[q(a_), q(b_)] for a_, b_ in ek], model_is_finite_graph=True, transfers_to_aq=False,
         note='1-|<psi,psi_L>|^2 <= 2(E_L-E_0) with gap 1/2 (AV1 F22); without a gap (diag(0,0,1)) a vector with the '
              'ground energy is orthogonal to the ground vector')
    fixtures['cutoff_eckart'] = True

    def xnl(nn, ll):
        return min(F(1), F(ll, nn))

    need(all(xnl(nn, ll) == 1 for nn in range(1, 20) for ll in range(nn, 40))
         and all(xnl(nn, ll) <= F(ll, nn) for ll in range(1, 10) for nn in range(ll, 60)) and xnl(1000, 3) < F(1, 100),
         'fixture_cutoff_limit_order', model_is_finite_graph=True, transfers_to_aq=False,
         note='x(N,L)=min(1,L/N): lim_N lim_L = 1 but lim_L lim_N = 0; the N and L limits are never exchanged')
    fixtures['cutoff_limit_order'] = True
    mv_rows = []
    for nn in range(2, 6):
        diff2 = [[F(-1), F(0)], [F(0), F(1)]]
        lo_, hi_ = trace_norm_2x2(diff2)
        mv_rows.append({'n': nn, 'trace_distance_lower': q(lo_), 'overlap_with_e1': '0'})
        if lo_ != 2 or hi_ - 2 > F(1, 10 ** 12):
            raise CheckFailure('moving vector fixture')
    need(len(mv_rows) == 4, 'fixture_fixed_versus_moving_vector', rows=mv_rows, model_is_finite_graph=True,
         transfers_to_aq=False,
         note='rho_n=|e_n><e_n|: ||rho_n-rho_1||_1=2 for n>1 while <e_1,rho_n e_1>=0; weak vanishing is not trace-norm '
              'convergence, so the topology is the trace norm on B(H_Y)')
    fixtures['fixed_versus_moving_vector'] = True
    zval = (1 + 4 * (F(0) ** 2 - F(1, 2) ** 2), 4 * 2 * F(0) * F(1, 2))
    need(zval == (F(0), F(0)), 'fixture_zero_free_region', normalization='1+4z^2 vanishes at z=i/2',
         model_is_finite_graph=True, transfers_to_aq=False)
    fixtures['zero_free_region'] = True
    phi_out = state(2, [(mask_of(0), F(1, 2))])
    e_out = sum(phi_out[s] ** 2 * bin(s).count('1') for s in range(4)) / ip(phi_out, phi_out)
    need(e_out == F(1, 5) and e_out > 0, 'fixture_outside_vector_not_ground_state', outside_energy=q(e_out),
         model_is_finite_graph=True, transfers_to_aq=False,
         note='phi_out=(1-b c_o)Omega with b=1/2 has number energy 1/5 above the outside ground value 0: it is the '
              'restriction of the box coefficient family, not an outside ground state, so no gap argument applies')
    fixtures['outside_vector_not_ground_state'] = True
    fixtures['coefficient_decay_not_marginal_decay'] = True

    # 8. packet validator and the 37 controls
    comparisons = {'F1_nested': 'F1 on Lambda_N versus F1 on Lambda_{N+1}',
                   'F2_nested': 'F2 on Lambda_N versus F2 on Lambda_{N+1}',
                   'F1_vs_F2_fixed_N': 'F1 versus F2 on the same Lambda_N',
                   'centered_pairs_direct': 'any two centered boxes of F1 or F2, compared directly',
                   'one_prescription_volumes_direct': 'two volumes of one prescription containing Lambda_N, direct'}
    family_defs = {'F1': 'AQ1 centered whole-star boxes Lambda_N', 'F2': 'I1 section 6 all-contained-face boxes with '
                                                                         'padding on Lambda_N'}
    decomposition = {'identity': 'rho_Y = N_c(omega_O)/Tr N_c(omega_O)', 'trace_N_ge_1': 'AV1 orthogonality (F09)',
                     'lipschitz_omega': '||rho(omega)-rho(omega\')||_1 <= 2||N_c(omega-omega\')||_1',
                     'lipschitz_c': '||rho_c-rho_c\'||_1 <= 2||X_c-X_c\'|| (sine bound)', 'tier_route_named': True}
    lemma_form = 'near 2(1+eta) sum_{I meets Y} + far sum kappa(I), kappa <= kappa_0 w\'^(-d) p(|I|)'
    pairs = {'headline': {'q': q_head, 'target': c_head, 'form': 'R'},
             'region': {'q': q_reg, 'target': c_reg, 'form': 'region'},
             'secondary_C': {'q': q2, 'target': c2_t, 'form': 'R'},
             'secondary_c_site': {'q': q2, 'target': cs2_t, 'form': 'region'},
             'crude_R': {'q': q_head, 'target': c_head, 'form': 'R'}}
    ctx = {'controls': controls, 'inventory': inventory, 'tau_abs': tau, 'family_defs': family_defs,
           'parameter_keys_required': ['metric', 'weights', 'window', 'clock', 'N_min', 'rate_constant_pair',
                                       'comparisons', 'cutoff', 'coefficient_input'],
           'comparisons': sorted(comparisons), 'decomposition': decomposition, 'lemma_form': lemma_form,
           'w_max': w_max, 'pairs': pairs, 'brackets': brackets, 'brackets_text': brackets_text,
           'sub_labels': ['boundary_decay_rate_only', 'static_not_dynamic'], 'gate_fields': gate_fields,
           'sentence': sentence, 'forbidden': forbidden, 'kp_nocard_exact_lower': exact_single,
           'kp_nocard_bound': a_c, 'second_order_derivative': deriv, 'second_order_delta_e': de,
           'second_order_offdiag_change_twice': off_change_twice, 'product_charging_increases': increases}

    def rec(cid, pair, tier, k_source, value, site0='N', theta_=theta, beta=far['beta']):
        pr = pairs[pair]
        return {'id': cid, 'pair': pair, 'q': pr['q'], 'form': pr['form'], 'tier': tier, 'route': 'iterated_split',
                'value': value, 'target': pr['target'], 'meets_target': value <= pr['target'],
                'inputs': {'K_source': k_source, 'theta': theta_, 'e_b': e_b, 'site0': site0}, 'signs': ['+', '-'],
                'beta': beta}

    constants_ref = [
        rec('C_headline', 'headline', 'exact_first_order', 'gate_bound_K', cst['C_b_every_site']),
        rec('C_headline_R_only_input', 'headline', 'exact_first_order', 'gate_bound_K', cst['C_b_R_only'], 'N-1'),
        rec('c_site_region', 'region', 'exact_first_order', 'gate_bound_K', cst['c_site_b']),
        rec('C_headline_form_a', 'headline', 'exact_first_order', 'labelled_weighted_norm', cst['C_a_own']),
        rec('C_secondary', 'secondary_C', 'exact_first_order', 'labelled_reinstantiated_disc',
            cst['C_secondary_every_site'], theta_=theta2, beta=far2['beta']),
        rec('c_site_secondary', 'secondary_c_site', 'exact_first_order', 'labelled_reinstantiated_disc',
            cst['c_site_secondary'], theta_=theta2, beta=far2['beta']),
        rec('C_crude', 'crude_R', 'crude_majorant', 'crude_analytic_disc', cst['C_crude_every_site'],
            beta=far_c['beta']),
    ]
    fixture_rows = {name: {'exhibited': fixtures.get(name) is True, 'model_is_finite_graph': True,
                           'transfers_to_aq': False} for name in REQUIRED_FIXTURES}
    base_pk = {
        'contract_sha256': CONTRACT_SHA256, 'controls_executed': {cid: True for cid in controls},
        'snapshots': list(inventory), 'reverse_inputs': list(inventory),
        'claims': {'continuum_claim': False, 'scientific_priority_verified': False, 'weak_coupling_claim': False},
        'model_id': MODEL_ID, 'triple': ['0', '0', '0'], 'tau_abs': tau, 'signs': ['+', '-'], 'N_min': 2,
        'metric': 'coarse_linf', 'd_X': 1, 'families': ['F1', 'F2'], 'family_defs': dict(family_defs),
        'parameters_declared': sorted(par), 'clock': CLOCK, 'window': WINDOW,
        'clock_by_comparison': {k: {'clock': CLOCK, 'tau_abs': tau} for k in comparisons}, 'topology': TOPOLOGY,
        'fixtures': fixture_rows, 'decomposition': dict(decomposition),
        'lemma': {'form': lemma_form, 'eta': F(0), 'kappa_0': 4 * far['A'] * far['e2beta_up'], 'w_prime': theta,
                  'p': F(1), 'kp_asserted_without_counts': False},
        'coefficient_input': {'form': 'b', 'every_site': True, 'proved_in_full': True, 'cited_as_admitted': False,
                              'exponent': 'N-|u|_inf', 'K': k_b, 'K_label': 'gate_bound_K',
                              'far_site_input': 'every_site_form', 'outside_smaller_box': 'anchored norm 2 tbar'},
        'mixed_weight': {'used': True, 'proved_in_full': True, 'cited_from': None, 'loss_per': 'interaction',
                         'loss': loss},
        'proof_weights': {'declared_before_constants': True, 'theta': theta, 'e_b': e_b},
        'straddling': {'included': True, 'charged_beyond_first_order': True,
                       'normalization': 'exact ratio (Tr N_c >= 1)'},
        'outside_state': {'gap_argument': False}, 'locality_mechanism': 'coefficient input and straddle recursion',
        'lipschitz_decay_factor': None,
        'analyticity': {'density_analytic_claimed': False, 'zero_free_region': None},
        'polymer': {'identity_checked': True, 'kp_function': 'a|X_gamma|'},
        'second_order': {'claimed_derivative': deriv, 'per_link_factor_sq': a0 * b0},
        'split': {'charging': 'per_site', 'trace_N_ge_1_checked': True, 'lipschitz_checked': True},
        'marginal': {'state_decay_inferred_from_coefficients': False, 'fixture_exhibited': True},
        'cutoff': {'uniform_in_L': True, 'removal': 'AV1 F20-F23 at fixed N (F2 via AY1)', 'vector_convergence': True,
                   'eigenvalue_only': False, 'order': 'L to infinity at fixed N; N never inside a fixed Q_L',
                   'limits_swapped': False},
        'comparisons': {k: {'covered': True, 'constant': 'C', 'route': 'direct'} for k in comparisons},
        'region': {'Y_dependence': '|Y| e^{|Y|/10^8}', 'exponent': 'd_Y = N - max_y |y|_inf',
                   'R_constant_reused': False},
        'rate_units': RATE_UNITS, 'rate_in_a': False, 'physical_length': None, 'uniform_in': UNIFORM_IN,
        'combine': 'linear', 'constants': constants_ref, 'q_optimized_per_N': False,
        'missed': [{'id': 'C_crude', 'dominating_term': 'crude BA1 input 296/390625 (2x28 rho G(R))',
                    'retuned': False}],
        'verdict': 'accepted_within_scope',
        'scaling': {'C_headline': ratios['C_headline_every_site'], 'c_site': ratios['c_site'],
                    'C_secondary': ratios['C_secondary'], 'c_site_secondary': ratios['c_site_secondary'],
                    'q_secondary': ratios['q_secondary']},
        'scaling_bracket_of': {'C_headline': 'C_headline', 'c_site': 'c_site', 'C_secondary': 'secondary_constants',
                               'c_site_secondary': 'secondary_constants', 'q_secondary': 'q_secondary'},
        'brackets_declared': dict(brackets_text),
        'sub_labels': ['boundary_decay_rate_only', 'static_not_dynamic'],
        'limit_statements': ['The density bound holds per comparison of two finite boxes; no limit, whole sequence or '
                             'subsequence statement about states is made here (BB2).'],
        'gate_fields': dict(gate_fields), 'sentence': sentence,
        'statements': [sentence + ' The rate is q per coarse step at fixed spacing.',
                       'This is not the thermodynamic limit and not uniqueness of any ground state.'],
        'contract_strings': list(strings_of(con)),
    }
    need(validate(base_pk, ctx), 'reference_packet_accepted')
    nested = ('controls_executed', 'claims', 'family_defs', 'clock_by_comparison', 'fixtures', 'decomposition',
              'lemma', 'coefficient_input', 'mixed_weight', 'proof_weights', 'straddling', 'outside_state',
              'analyticity', 'polymer', 'second_order', 'split', 'marginal', 'cutoff', 'comparisons', 'region',
              'gate_fields', 'scaling', 'scaling_bracket_of', 'brackets_declared')

    def mut(**kw):
        pk = dict(base_pk)
        for key in nested:
            pk[key] = dict(base_pk[key])
        pk['fixtures'] = {k: dict(v) for k, v in base_pk['fixtures'].items()}
        pk['comparisons'] = {k: dict(v) for k, v in base_pk['comparisons'].items()}
        pk['constants'] = [dict(r_, inputs=dict(r_['inputs'])) for r_ in base_pk['constants']]
        pk['missed'] = [dict(m_) for m_ in base_pk['missed']]
        for k, val in kw.items():
            if k.startswith('const:'):
                _, cid, field = k.split(':')
                for r_ in pk['constants']:
                    if r_['id'] == cid:
                        if field.startswith('inputs.'):
                            r_['inputs'][field[7:]] = val
                        else:
                            r_[field] = val
            elif k.startswith('comp:'):
                _, cname, field = k.split(':')
                pk['comparisons'][cname][field] = val
            elif k.startswith('fix:'):
                _, fname, field = k.split(':')
                pk['fixtures'][fname][field] = val
            elif k.startswith('clk:'):
                pk['clock_by_comparison'][k[4:]] = val
            elif '.' in k:
                head_, tail = k.split('.', 1)
                pk[head_][tail] = val
            else:
                pk[k] = val
        return lambda: validate(pk, ctx)

    ok = [('reference packet', lambda: validate(base_pk, ctx))]
    control('coherent_evidence_tampering',
            [('contract hash rebound', mut(contract_sha256='0' * 64), 'contract hash'),
             ('control Boolean flipped', mut(**{'controls_executed.cutoff_limit_order': False}), 'control boolean'),
             ('snapshot removed', mut(snapshots=inventory[:-1]), 'snapshot missing'),
             ('headline halved with hashes rebound', mut(**{'const:C_headline:value': cst['C_b_every_site'] / 2}),
              'constant not reproduced')], ok)
    control('exact_arithmetic_admission',
            [('float headline', mut(**{'const:C_headline:value': float(cst['C_b_every_site'])}), 'exact arithmetic'),
             ('float ratio', mut(**{'scaling.q_secondary': 100.0}), 'exact arithmetic'),
             ('float lemma constant', mut(**{'lemma.kappa_0': 1e-5}), 'exact arithmetic')], ok)
    control('no_priority_or_continuum_claim',
            [('continuum', mut(**{'claims.continuum_claim': True}), 'forbidden claim continuum_claim'),
             ('priority', mut(**{'claims.scientific_priority_verified': True}), 'forbidden claim scientific_priority'),
             ('weak coupling', mut(**{'claims.weak_coupling_claim': True}), 'forbidden claim weak_coupling')], ok)
    control('changed_model_relabelled',
            [('tau 1e-14', mut(tau_abs=F(1, 10 ** 14)), 'changed model'),
             ('uniform triple', mut(triple=['tau/24', 'tau/24', 'tau/24']), 'changed model'),
             ('finite-graph model id', mut(model_id='FG(qubit_chain)'), 'changed model'),
             ('one sign', mut(signs=['+']), 'changed model'),
             ('l1 metric', mut(metric='coarse_l1', d_X=2), 'changed model')], ok)
    control('insufficient_verdict_retained',
            [('crude reported as meeting', mut(**{'const:C_crude:meets_target': True}), 'insufficient verdict'),
             ('missed list emptied', mut(missed=[]), 'insufficient verdict'),
             ('crude retuned', mut(missed=[dict(base_pk['missed'][0], retuned=True)]), 'insufficient verdict')], ok)
    control('tau_scaling_exponent',
            [('square-root headline ratio 10', mut(**{'scaling.C_headline': F(10)}), 'tau scaling'),
             ('secondary with a linear ratio', mut(**{'scaling.C_secondary': F(100)}), 'tau scaling'),
             ('q_2 ratio 99', mut(**{'scaling.q_secondary': F(99)}), 'tau scaling'),
             ('bracket chosen after evaluation', mut(brackets_declared=dict(brackets_text, c_site='[90,110]')),
              'tau scaling')], ok, ratios={k: q(v) for k, v in ratios.items()})
    control('wrong_delta_alpha_hbar_clock',
            [('u labelled theta', mut(clock='theta=delta*t/hbar'), 'clock'),
             ('window in u', mut(window='|u| at most 1'), 'clock')], ok)
    control('root_n_misuse',
            [('rss of near and far terms', mut(combine='rss'), 'root-N'),
             ('far sum divided by sqrt(N)', mut(combine='far/sqrt(N)'), 'root-N'),
             ('one-prescription volumes through an unlabelled union',
              mut(**{'comp:one_prescription_volumes_direct:route': 'union'}), 'comparison')], ok)
    control('tier_mixing_rejected',
            [('exact label on crude input', mut(**{'const:C_headline:inputs.K_source': 'crude_analytic_disc'}),
              'tier mixing'),
             ('BA1 route as the BB1 route', mut(**{'const:C_headline:route': 'analytic_disc'}), 'tier mixing'),
             ('Lieb-Robinson tier', mut(**{'const:c_site_region:tier': 'polynomial_lieb_robinson'}), 'tier mixing'),
             ('crude label on the gate input', mut(**{'const:C_crude:inputs.K_source': 'gate_bound_K'}),
              'tier mixing')], ok)
    control('reverse_premise_isolation',
            [('BB contract review added', mut(reverse_inputs=inventory + ['research/round33/skeptic/'
                                                                          'bb-contract-review.md']),
              'reverse premise isolation'),
             ('BB targets proposal added', mut(reverse_inputs=inventory + ['research/round33/experts/modern/'
                                                                           'bb-targets-proposal.md']),
              'reverse premise isolation'),
             ('triage added', mut(reverse_inputs=inventory + ['research/round33/skeptic/triage.md']),
              'reverse premise isolation'),
             ('forward BB1 file added', mut(reverse_inputs=inventory + ['research/round33/forward/bb1/report.md']),
              'reverse premise isolation'),
             ('BB2 producer file added', mut(reverse_inputs=inventory + ['research/round33/reverse/bb2/report.md']),
              'reverse premise isolation'),
             ('plan added', mut(reverse_inputs=inventory + ['research/round33/advisor/plan.json']),
              'reverse premise isolation'),
             ('premise dropped', mut(reverse_inputs=inventory[1:]), 'reverse premise inventory')], ok,
            reading='executed on a synthetic inventory derived from the contract; the actual inputs/ were hashed')
    control('uniform_in_N_not_in_a',
            [('uniform in a', mut(uniform_in='a'), 'uniform in a'),
             ('affirmative sentence', mut(statements=['The constant C is uniform in a.']), 'uniform in a')], ok)
    control('placeholder_span_rejected',
            [('placeholder in a contract string', mut(contract_strings=['C at most <to be filled>']),
              'placeholder span'),
             ('bar placeholder', mut(contract_strings=['q=<1/64|q_2>']), 'placeholder span')],
            ok + [('inequality digraphs', mut(contract_strings=['J<=28|tau| and N>=2']))])
    control('negation_aware_phrase_scan',
            [('affirmative thermodynamic limit', mut(statements=['The densities define the thermodynamic limit.']),
              'forbidden phrasing'),
             ('boundary independent', mut(statements=['The density on R is boundary independent.']),
              'forbidden phrasing'),
             ('confirms', mut(statements=['The bound confirms the locality.']), 'forbidden phrasing')],
            ok + [('negated mention', mut(statements=['This is not the thermodynamic limit.']))])
    control('parameters_declare_metric_weights_window',
            [('metric missing', mut(parameters_declared=[k for k in sorted(par) if k != 'metric']),
              'parameters field missing'),
             ('weights missing', mut(parameters_declared=[k for k in sorted(par) if k != 'weights']),
              'parameters field missing'),
             ('window missing', mut(parameters_declared=[k for k in sorted(par) if k != 'window']),
              'parameters field missing'),
             ('coefficient input missing', mut(parameters_declared=[k for k in sorted(par)
                                                                    if k != 'coefficient_input']),
              'parameters field missing')], ok)
    control('rate_constant_pair_prefrozen',
            [('target loosened', mut(**{'const:C_headline:target': F(1, 100000)}), 'rate constant pair'),
             ('q moved to 1/32', mut(**{'const:C_headline:q': F(1, 32)}), 'rate constant pair'),
             ('q optimized per N', mut(q_optimized_per_N=True), 'rate constant pair'),
             ('proof weight above w_max after the loss', mut(**{'proof_weights.theta': F(2048)}),
              'rate constant pair: proof weight'),
             ('weights declared after the constants', mut(**{'proof_weights.declared_before_constants': False}),
              'rate constant pair: proof weights declared after')], ok)
    control('decay_rate_in_N_not_a',
            [('rate in a', mut(rate_in_a=True), 'rate in a'),
             ('length in fm', mut(physical_length='0.1 fm per step'), 'rate in a')], ok)
    control('topology_named',
            [('weak topology', mut(topology='weak-* on B(H_Y)'), 'topology'),
             ('moving-vector fixture missing', mut(**{'fix:fixed_versus_moving_vector:exhibited': False}),
              'topology')], ok)
    control('two_families_named',
            [('F1 only', mut(families=['F1']), 'two families'),
             ('F2 definition altered', mut(family_defs=dict(family_defs, F2='F2 without padding')), 'two families')],
            ok)
    control('subsequence_versus_whole_sequence',
            [('unqualified limit', mut(limit_statements=['The densities converge.']), 'subsequence'),
             ('whole sequence claimed', mut(**{'gate_fields.whole_sequence_claimed': True}), 'subsequence')], ok)
    control('common_clock',
            [('one comparison at another coupling', mut(**{'clk:F1_vs_F2_fixed_N': {'clock': CLOCK,
                                                                                    'tau_abs': F(1, 10 ** 9)}}),
              'common clock'),
             ('one comparison with the u clock', mut(**{'clk:F2_nested': {'clock': 'u=theta/8', 'tau_abs': tau}}),
              'common clock')], ok)
    control('coefficient_decay_not_marginal_decay',
            [('state decay inferred', mut(marginal={'state_decay_inferred_from_coefficients': True,
                                                    'fixture_exhibited': True}), 'marginal'),
             ('fixture missing', mut(marginal={'state_decay_inferred_from_coefficients': False,
                                               'fixture_exhibited': False}), 'marginal')], ok,
            fixture='fixture_coefficient_decay_not_marginal_decay')
    control('normalization_couples_supports',
            [('straddling dropped', mut(**{'straddling.included': False}), 'normalization couples supports'),
             ('straddling at first order only', mut(**{'straddling.charged_beyond_first_order': False}),
              'normalization couples supports'),
             ('normalized by 1+O(t^2)', mut(**{'straddling.normalization': '1+O(t^2)'}),
              'normalization couples supports')], ok,
            fixtures=['fixture_normalization_spectators', 'fixture_straddling_supports'])
    control('outside_vector_not_ground_state',
            [('gap argument on phi_out', mut(**{'outside_state.gap_argument': True}), 'outside vector')], ok,
            fixture='fixture_outside_vector_not_ground_state')
    control('global_fidelity_orthogonality_catastrophe',
            [('global overlap route', mut(locality_mechanism='global overlap'), 'global fidelity'),
             ('fidelity fixture missing', mut(**{'fix:global_fidelity:exhibited': False}), 'fixture missing')], ok,
            fixture='fixture_global_fidelity')
    control('marginal_locality_constants_explicit',
            [('eta missing', mut(lemma={k: v for k, v in base_pk['lemma'].items() if k != 'eta'}),
              'marginal-locality lemma'),
             ('kappa_0 not exact', mut(**{'lemma.kappa_0': 'small'}), 'marginal-locality lemma'),
             ('KP asserted without counts', mut(**{'lemma.kp_asserted_without_counts': True}),
              'marginal-locality lemma'),
             ('no decay in kappa', mut(**{'lemma.w_prime': F(1)}), 'marginal-locality lemma')], ok)
    control('cutoff_uniform_then_removed',
            [('bound not uniform in L', mut(**{'cutoff.uniform_in_L': False}), 'cutoff uniform then removed'),
             ('removal by AM2 eigenvalues', mut(**{'cutoff.removal': 'AM2 section 6 eigenvalues'}),
              'cutoff uniform then removed')], ok)
    control('cutoff_vector_removal',
            [('eigenvalue convergence only', mut(**{'cutoff.eigenvalue_only': True}), 'cutoff vector removal'),
             ('no vector convergence', mut(**{'cutoff.vector_convergence': False}), 'cutoff vector removal')], ok,
            fixture='fixture_cutoff_eckart')
    control('region_constant_scales_with_Y',
            [('R constant reused on Y', mut(**{'region.R_constant_reused': True}), 'region constant'),
             ('exponent N-1 for every Y', mut(**{'region.exponent': 'N-1'}), 'region constant'),
             ('|Y| dependence dropped', mut(**{'region.Y_dependence': 'none'}), 'region constant'),
             ('crude exponent in the frozen form', mut(**{'const:c_site_region:beta': far_c['beta']}),
              'region constant')], ok)
    control('named_construction_not_uniqueness',
            [('uniqueness claimed', mut(**{'gate_fields.uniqueness_of_ground_state_claimed': True}),
              'named construction'),
             ('the infinite-volume ground state', mut(statements=['The bound identifies the infinite-volume ground '
                                                                  'state.']), 'named construction')], ok)
    control('global_lipschitz_not_decay',
            [('density Lipschitz as the rate', mut(lipschitz_decay_factor=lip_omega), 'global Lipschitz'),
             ('AM2 exclusion constant as the rate', mut(lipschitz_decay_factor=F(77, 390625)), 'global Lipschitz'),
             ('Lipschitz mechanism', mut(locality_mechanism='Lipschitz per shell'), 'global Lipschitz')], ok,
            L_omega=q(lip_omega))
    control('fixture_second_order_propagation',
            [('first-order propagation (zero derivative)', mut(**{'second_order.claimed_derivative': F(0)}),
              'second-order propagation'),
             ('per-link factor a^2', mut(**{'second_order.per_link_factor_sq': (a0 * b0) ** 2}),
              'per-link factor below the exact one')], ok)
    control('fixture_split_lipschitz_and_trace',
            [('product of growing region sizes', mut(**{'split.charging': 'product_of_region_sizes'}),
              'product of growing region sizes'),
             ('trace not checked', mut(**{'split.trace_N_ge_1_checked': False}), 'split charging: trace')], ok)
    control('fixture_polymer_identity',
            [('identity not checked', mut(**{'polymer.identity_checked': False}), 'polymer identity'),
             ('cardinality factor dropped', mut(**{'polymer.kp_function': 'a'}), 'polymer cardinality factor')], ok)
    control('zero_free_region_required',
            [('analytic density claimed', mut(analyticity={'density_analytic_claimed': True,
                                                           'zero_free_region': None}), 'zero-free region')], ok,
            fixture='fixture_zero_free_region')
    control('every_site_coefficient_input',
            [('R-only input at far sites', mut(**{'coefficient_input.far_site_input': 'R_only_gate_statement'}),
              'every-site coefficient input'),
             ('form (b) cited as admitted', mut(**{'coefficient_input.cited_as_admitted': True}),
              'every-site coefficient input'),
             ('exponent N at every site', mut(**{'coefficient_input.exponent': 'N'}), 'every-site coefficient input'),
             ('form (a) relabelled as the gate bound', mut(**{'coefficient_input.form': 'a'}),
              'every-site coefficient input'),
             ('no input outside the smaller box', mut(**{'coefficient_input.outside_smaller_box': 'zero'}),
              'every-site coefficient input')], ok)
    control('mixed_weight_lemma_proved',
            [('cited from BA1', mut(**{'mixed_weight.cited_from': 'BA1'}), 'mixed-weight lemma'),
             ('loss per creation', mut(**{'mixed_weight.loss_per': 'creation'}), 'mixed-weight lemma'),
             ('loss misstated', mut(**{'mixed_weight.loss': theta}), 'mixed-weight lemma')], ok)
    control('cutoff_limit_order',
            [('limits swapped', mut(**{'cutoff.limits_swapped': True}), 'cutoff limit order'),
             ('N inside a fixed Q_L', mut(**{'cutoff.order': 'N to infinity in each Q_L, then L'}),
              'cutoff limit order')], ok, fixture='fixture_cutoff_limit_order')
    ids = set(controls)
    done = {row['id'] for row in CHECKS if row.get('kind') == 'control'}
    missing = sorted(ids - done)
    n_mut = sum(len(row['mutations']) for row in CHECKS if row.get('kind') == 'control')
    n_pos = sum(len(row['positives']) for row in CHECKS if row.get('kind') == 'control')
    need(not missing, 'contract_controls_covered', implemented=len(ids & done), of=len(ids), mutations=n_mut,
         positives=n_pos, deferred=missing)

    constants_out = {k: {'value': q(v), 'preview': preview(v)} for k, v in sorted(cst.items())}
    return {
        'loop': 'BB1', 'stage': 'pre_comparison', 'reviewer': 'skeptic (model agent, correlated ancestry)',
        'human_author': 'Hruday N M (BUNZEEY)', 'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'model': MODEL_ID + ': SU(2) Kogut-Susskind form on Z^3 at fixed spacing, coarse 24-link factors, selected '
                            'triple (0,0,0), Haar product reference, 21 omitted faces per anchor with -(tau/3)W_f; '
                            'both signs |tau|<=10^-8; AM2 creation expansion (J<=28|tau|, R=1/64) in each on-site '
                            'cutoff space; F1 (AQ1 whole-star) and F2 (I1 section 6 with padding) on centered '
                            'Lambda_N, N at least 2; reduced densities of the finite-box ground vectors on R={0,e_z} '
                            'and on finite complete-factor regions Y inside Lambda_N; trace norm on B(H_Y)',
        'scratch': '/tmp/claude-0/skeptic-bb1-private/ (private, disclosed; not evidence)',
        'coefficient_input': {'form_b_K': q(k_b), 'form_b_statement': 'sum_{I ni u}||delta_I|| <= K q^(N-|u|_inf), '
                                                                      'every u in Lambda_N, every comparison',
                              'form_a_K_own': q(k_own), 'forward_K_gen_telescoped': q(k_gen),
                              'secondary_K_2': q(k_2), 'crude_K': q(k_crude), 'outside_smaller_box': '2 tbar',
                              'tbar': q(tb), 'every_site_rows': every_site_rows, 'general_volumes': gv_rows},
        'proof_weights': {'theta': q(theta), 'e_b': q(e_b), 'loss': q(loss), 'w_max': q(w_max),
                          'theta_secondary': q(theta2), 'loss_secondary': q(theta2 * e_b ** 4)},
        'far_recursion': {k: q(v) for k, v in far.items()},
        'far_recursion_secondary': {k: q(v) for k, v in far2.items()},
        'far_recursion_crude': {k: q(v) for k, v in far_c.items()},
        'constants': constants_out,
        'constant_labels': {
            'C_b_every_site': 'headline R form, exact_first_order, input form (b) K=49/111790368 (gate bound value, '
                              're-proved at every u), q^N at 0 and q^(N-1) at e_z; near 2, far 4A e^{2beta}',
            'C_b_R_only': 'same with the BA1 gate statement at both sites of R (q^(N-1) at 0 and e_z)',
            'c_site_b': 'region form per site, 2K(1+A), with e^{beta|Y|}, beta<=10^-8',
            'C_a_own': 'headline with form (a) K_own=19140625/86785322066496 (labelled weighted_norm)',
            'c_site_a_own': 'region form with form (a)',
            'C_a_gen': 'headline with the forward telescoped K_gen (labelled)',
            'C_split_b_every_site': 'split (sine-bound) near term 2(1+tbar+K)(D_0+D_ez), far A\'=2M/(eps e-2M)',
            'C_split_b_R_only': 'split variant with the R-only input',
            'C_union_b_every_site': 'density comparison through the union (factor 2), labelled only',
            'C_union_b_R_only': 'union with the R-only input, labelled only',
            'c_site_union_b': 'region union, labelled only',
            'C_secondary_every_site': 'secondary q_2=151552|tau|, input 2T(1/151552)=49/10202112 (labelled '
                                      're-instantiation), theta=1/q_2',
            'C_secondary_R_only': 'secondary with both sites at q_2^(N-1)',
            'c_site_secondary': 'secondary region form',
            'C_crude_every_site': 'crude_majorant: input 296/390625, crude mixed norms; misses 1/250000, retained',
            'C_crude_R_only': 'crude with both sites at q^(N-1)',
            'c_site_crude_own_exponent': 'crude region constant; its exponent beta_crude > 10^-8 cannot be written '
                                         'in the frozen form (labelled, never a target)'},
        'recorded_preview_structure': {'eta_str': q(eta_str), 'C_split_R_only': q(prev_split_R_only),
                                       'C_split_every_site_preview': preview(prev_split_every),
                                       'C_split_forward_Kgen_preview': preview(prev_split_fwd),
                                       'shell_sum_at_qWc': q(s_prev), 'eta_far_preview': preview(eta_far_prev),
                                       'C_poly_R_only_preview': preview(prev_poly_R_only)},
        'targets': {'headline': [q(q_head), q(c_head)], 'region': [q(q_reg), q(c_reg)],
                    'secondary': [q(q2), q(c2_t), q(cs2_t)]},
        'kp_feasibility': {'a': q(a_kp), 'W_c': q(w_kp), 'e_b': q(e_b), 'loss': q(w_kp * e_b ** 4),
                           'T_mixed': q(t_kp_mix), 'kp_sum_bound_preview': preview(kp_sum)},
        'density_lipschitz_R': q(lip_omega),
        'scaling': {k: q(v) for k, v in ratios.items()},
        'scaling_previews': {k: preview(v) for k, v in ratios.items()},
        'gate_fields': dict(gate_fields), 'sentence': sentence,
        'continuum_claim': False, 'scientific_priority_verified': False, 'weak_coupling_claim': False,
        'controls': {'implemented': len(ids & done), 'of': len(ids), 'mutations': n_mut, 'positives': n_pos},
        'deferred_controls': {},
        'deferred_parts': {
            'reverse_premise_isolation': 'executed on a synthetic inventory derived from the contract; the actual '
                                         'producer inputs/ were listed and hashed outside this program (35 files '
                                         'each, byte-identical)',
            'negation_aware_phrase_scan': 'a mirror of tools/phrase_scan.py (lists and negation frame copied, not '
                                          'imported); the tool itself runs at gate recording',
            'placeholder_span_rejected': 'a mirror of the freezer rule R1 detector, not imported',
            'coherent_evidence_tampering': 'packet-level mutations; producer freeze inventories are checked at '
                                           'post-comparison',
            'polymer_route_constants': 'KP feasibility and the mixed-weight loss are checked; the forward far '
                                       'constant is not re-derived here (its KP parameters are the producer\'s '
                                       'choice); the recorded preview structure is recomputed for comparison',
            'untruncated_passage': 'argued (AV1 F20-F23, AY1 for F2), with the Eckart fixture; no infinite-'
                                   'dimensional computation'},
        'checks': CHECKS,
        'previews': {k: v['preview'] for k, v in constants_out.items()},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if out.resolve() == ROOT or ROOT in out.resolve().parents:
        raise SystemExit('--output must lie outside the checkout')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    result = execute()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'controls': result['controls'],
                      'C_headline': result['previews']['C_b_every_site'],
                      'c_site': result['previews']['c_site_b']}))


if __name__ == '__main__':
    main()
