#!/usr/bin/env python3
"""BD2 forward producer (single producer of a single+skeptic loop), Round33 investigation 8 of 8.

Applications II in SU(2): (a) the Round11 two-plaquette graph with INDEPENDENT couplings,
H_FG(l1,l2) = K - l1 W_1 - l2 W_2 (alpha units, K the seven link Casimirs, rho=1): exact bivariate
Rayleigh-Schroedinger coefficients of <W_1>, <z>, <C_shared> through total order 4 at D=6 and D=8, the
one-link centre flips, and certified enclosures of <z> at l1=l2 on the AZ2 grid; (b) the zero-selected
Z^3 family: the 1x2 Wilson loop (first order 0, evenness, the admitted bound K_2' tau^2, a labelled formal
second-order coefficient) and a two-sided band for the electric energy on the cover R; (c) the 2+1-dimensional
recount of the AM2 constants for a declared factorization.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production (a Claude model agent).

Standard library only.  The admitted AZ2 checker (research/round32/forward/az2/check.py) and the Round11
solver are declared premises: the AZ2 exact graph algebra is COPIED verbatim below (with attribution) and each
copied block is compared textually with the snapshot; nothing is imported from the repository.  A
decimal.Decimal inverse iteration only PROPOSES Ritz vectors; every admission Boolean is decided in exact
Fraction arithmetic.  Conditions raise AdmissionError explicitly (never `assert`), so every check stays active
under `python -O`.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import decimal
import hashlib
import json
import re
from fractions import Fraction as Q
from functools import lru_cache
from math import comb, factorial, isqrt
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round33/contracts/bd2.json'
CONTRACT_SHA256 = '783cad8054a9b7ed3f741e0c06fffd94cfa0d6fda0dcbb7aa0b464058e46f41e'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'
SCRATCH = '/tmp/claude-0/bd2-forward-private/'

P_AZ2_GATE = 'research/round32/advisor/az2-gate.json'
P_AZ2_REPORT = 'research/round32/forward/az2/report.md'
P_AZ2_CHECK = 'research/round32/forward/az2/check.py'
P_AZ2_SKEPTIC = 'research/round32/skeptic/az2.md'
P_AW1_GATE = 'research/round32/advisor/aw1-gate.json'
P_AW1F = 'research/round32/forward/aw1/report.md'
P_AV1_GATE = 'research/round32/advisor/av1-gate.json'
P_AV1F = 'research/round32/forward/av1/report.md'
P_AV2_GATE = 'research/round32/advisor/av2-gate.json'
P_AY1_GATE = 'research/round32/advisor/ay1-gate.json'
P_AY1F = 'research/round32/forward/ay1/report.md'
P_AY2_GATE = 'research/round32/advisor/ay2-gate.json'
P_AY2F = 'research/round32/forward/ay2/report.md'
P_AM2_GATE = 'research/round29/advisor/am2-gate.json'
P_AM2F = 'research/round29/forward/am2/report.md'
P_AQ1_GATE = 'research/round29/advisor/aq1-gate.json'
P_AQ1F = 'research/round29/forward/aq1/report.md'
P_I1 = 'research/round21/forward/i1/report.md'
P_BB2_GATE = 'research/round33/advisor/bb2-gate.json'
P_BB2F = 'research/round33/forward/bb2/report.md'
P_R11_README = 'research/round11/README.md'
P_R11_ADV = 'research/round11/advisor/advisor.md'
P_R11_SOLVER = 'research/round11/solver/two_plaquette.py'
P_R11_SOLVER_README = 'research/round11/solver/README.md'
P_BA1 = 'research/round33/contracts/ba1.json'
P_BB2C = 'research/round33/contracts/bb2.json'

# Admitted gates and premise code, pinned by sha256 (recorded before any evaluation; a changed byte aborts).
PINNED = {
    P_AZ2_GATE: 'd36d53dcad8b1d3e4789d3be76b9e491e73cc5cf2ca88f281f66fd255f98b394',
    P_AW1_GATE: '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    P_AV1_GATE: '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    P_AV2_GATE: '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33',
    P_AY1_GATE: 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    P_AY2_GATE: 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    P_AM2_GATE: 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    P_AQ1_GATE: 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    P_BB2_GATE: 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
    P_AZ2_CHECK: '4ad3a9f8127ed983a3af9343a4697b77a35bec26f4cd75f1683e32307cab1c7d',
    P_R11_SOLVER: 'ae9084850538ebf523f8c34564352b48ce0b30d07955991d4b4d1980ab36ce43',
}

LINKS = ('h1', 'h2', 'h3', 'h4', 'vL', 'vM', 'vR')
ORIENT = {'h1': ('TL', 'TM'), 'h2': ('TM', 'TR'), 'h3': ('BL', 'BM'), 'h4': ('BM', 'BR'),
          'vL': ('TL', 'BL'), 'vM': ('TM', 'BM'), 'vR': ('TR', 'BR')}
VERTICES = ('TL', 'TM', 'TR', 'BL', 'BM', 'BR')
LINK_CLASS = {'h1': 'j', 'vL': 'j', 'h3': 'j', 'h2': 'k', 'vR': 'k', 'h4': 'k', 'vM': 'ell'}
FACE1_NONSHARED = ('h1', 'vL', 'h3')      # square 1 = U = vM h3^-1 vL^-1 h1
FACE2_NONSHARED = ('h2', 'vR', 'h4')      # square 2 = V = h2 vR h4^-1 vM^-1
SHARED = 'vM'


class AdmissionError(Exception):
    """An admission condition failed or a damaging mutation was accepted."""


def require(condition, message):
    if not condition:
        raise AdmissionError(message)


CHECKS = []
PENDING = []   # labels of damaging mutations rejected since the previous recorded check


def check(identity, condition, **details):
    require(condition, 'failed check ' + identity)
    require(all(c['id'] != identity for c in CHECKS), 'duplicate check id ' + identity)
    entry = {'id': identity, 'passed': True}
    entry.update(details)
    if PENDING:
        entry['rejected_mutations'] = list(PENDING)
        del PENDING[:]
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run a damaging mutation; it must raise AdmissionError."""
    try:
        mutation()
    except AdmissionError:
        PENDING.append(label)
        return label
    raise AdmissionError('damaging mutation accepted: ' + label)


# ---------------------------------------------------------------------------
# Exact-arithmetic helpers: copied verbatim from the admitted AZ2 checker (bound textually below).
# ---------------------------------------------------------------------------
def rat(value):
    """Exact rational input only: int, Fraction or an integer/ratio string."""
    if isinstance(value, bool) or isinstance(value, float) or isinstance(value, decimal.Decimal):
        raise AdmissionError('non-exact input rejected: ' + repr(value))
    if isinstance(value, (int, Q)):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value):
        num, _, den = value.partition('/')
        if den and int(den) == 0:
            raise AdmissionError('zero denominator rejected')
        return Q(int(num), int(den) if den else 1)
    raise AdmissionError('malformed rational rejected: ' + repr(value))


def s(q):
    return str(Q(q))


def dec(q, digits=12):
    """Truncated scientific decimal preview of an exact rational (never an admission value)."""
    q = Q(q)
    if q == 0:
        return '0'
    sign = '-' if q < 0 else ''
    q = abs(q)
    e = len(str(q.numerator)) - len(str(q.denominator))
    while q >= Q(10) ** (e + 1):
        e += 1
    while q < Q(10) ** e:
        e -= 1
    scaled = q / Q(10) ** (e - digits + 1)
    m = str(scaled.numerator // scaled.denominator)
    return sign + m[0] + '.' + m[1:] + 'e' + str(e)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def magnitude(q):
    """Integer e with 10^e <= |q| < 10^(e+1) (q != 0), exact."""
    q = abs(Q(q))
    e = len(str(q.numerator)) - len(str(q.denominator))
    while q >= Q(10) ** (e + 1):
        e += 1
    while q < Q(10) ** e:
        e -= 1
    return e


def sqrt_bracket(x, sig=40):
    """Directed rational bracket lo <= sqrt(x) <= hi with about `sig` significant digits (integer isqrt)."""
    x = rat(x)
    require(x >= 0, 'square root of a negative number')
    if x == 0:
        return Q(0), Q(0)
    k = sig - magnitude(x) // 2
    scale = Q(10) ** (2 * k)
    n = (x * scale).numerator // (x * scale).denominator
    r = isqrt(n)
    lo = Q(r) / Q(10) ** k
    hi = Q(r + 1) / Q(10) ** k
    require(lo * lo <= x <= hi * hi and lo >= 0, 'directed square-root bracket')
    return lo, hi


def sqrt_up(x, sig=40):
    return sqrt_bracket(x, sig)[1]


def out_dn(q, k):
    """Outward (downward) rounding to denominator 10^k."""
    q = Q(q) * Q(10) ** k
    return Q(q.numerator // q.denominator) / Q(10) ** k


def out_up(q, k):
    q = Q(q) * Q(10) ** k
    return Q(-((-q.numerator) // q.denominator)) / Q(10) ** k


def up_sig(q, sig=30):
    """Upward rounding of a nonnegative rational to about `sig` significant digits (ledger export)."""
    q = Q(q)
    require(q >= 0, 'up_sig expects a nonnegative value')
    if q == 0:
        return Q(0)
    return out_up(q, sig - 1 - magnitude(q))


def read_input(rel):
    return (BASE / 'inputs' / rel).read_text(encoding='utf-8')


def load_json_input(rel):
    return json.loads(read_input(rel))


def match(pattern, text, label, flags=0):
    m = re.search(pattern, text, flags)
    require(m is not None, 'premise text not parsed: ' + label)
    return m


def strip_code(text):
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    return re.sub(r'`[^`\n]*`', ' ', text)


# ---------------------------------------------------------------------------
# Exact invariant algebra of two adjacent SU(2) plaquettes and the AZ2 certificate: copied verbatim from the admitted
# AZ2 forward checker (Round32; Round11 conventions re-implemented in Fractions there).  Coordinates x=Tr(U)/2, y=Tr(V)/2,
# z=Tr(UV)/2 with U=vM h3^-1 vL^-1 h1, V=h2 vR h4^-1 vM^-1 (Round11 G2).
# ---------------------------------------------------------------------------
ZERO3 = (0, 0, 0)
EX, EY, EZ = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def basis(d):
    """Round11 `basis(d)`: monomials x^a y^b z^c of total degree <= d, ordered by degree, then a, then b."""
    return [(a, b, n - a - b) for n in range(d + 1) for a in range(n + 1) for b in range(n - a + 1)]


def parity_class(m):
    a, b, c = m
    return ((a + c) % 2, (b + c) % 2)


@lru_cache(None)
def haar_x_power(n):
    """E[x^n] for a scalar coordinate of normalized Haar S^3 (Catalan(n/2)/4^(n/2))."""
    if n % 2:
        return Q(0)
    m = n // 2
    return Q(comb(2 * m, m), 4 ** m * (m + 1))


@lru_cache(None)
def radial_moment(n, k):
    return sum(((-1) ** j * comb(k, j) * haar_x_power(n + 2 * j) for j in range(k + 1)), Q(0))


@lru_cache(None)
def moment(a, b, c):
    """Haar E[x^a y^b z^c] (Round11 advisor Q4)."""
    require(min(a, b, c) >= 0, 'negative exponent')
    return sum((Q(comb(c, 2 * k), 2 * k + 1) * radial_moment(a + c - 2 * k, k) * radial_moment(b + c - 2 * k, k)
                for k in range(c // 2 + 1)), Q(0))


def padd(p, q, scale=1):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0) + scale * v
    return {k: Q(v) for k, v in out.items() if v}


def pscale(p, c):
    return {k: c * v for k, v in p.items() if c * v}


def pmul(p, q):
    out = {}
    for (a, b, c), u in p.items():
        for (d, e, f), w in q.items():
            k = (a + d, b + e, c + f)
            out[k] = out.get(k, 0) + u * w
    return {k: v for k, v in out.items() if v}


def pshift(p, e):
    return {(k[0] + e[0], k[1] + e[1], k[2] + e[2]): v for k, v in p.items()}


def pdeg(p):
    return max((sum(k) for k in p), default=0)


def inner(p, q):
    """Physical L^2 inner product <p,q> (real polynomials, normalized Haar measure on the quotient)."""
    tot = Q(0)
    for (a, b, c), u in p.items():
        for (d, e, f), w in q.items():
            mm = moment(a + d, b + e, c + f)
            if mm:
                tot += u * w * mm
    return tot


def proj_coeffs(bs, p):
    """c_i = <m_i, p> for the monomials of a basis."""
    out = []
    for (a, b, c) in bs:
        tot = Q(0)
        for (d, e, f), w in p.items():
            mm = moment(a + d, b + e, c + f)
            if mm:
                tot += w * mm
        out.append(tot)
    return out


def dot(u, w):
    return sum((a * b for a, b in zip(u, w) if a and b), Q(0))


def casimir_terms(m, which):
    """One-group Casimirs in quotient coordinates (Round11 K3/K4 decomposition K = 3 C_U + 3 C_V + S).
    C_U acts on (x,z), C_V on (y,z), S (shared link vM, derivative L_U - R_V) on (x,y)."""
    a, b, c = m
    out = {}

    def add(k, val):
        out[k] = out.get(k, 0) + val
    if which == 'U':
        p1, p2, coef_mixed, target = a, c, 2 * a * c, (a - 1, b + 1, c - 1)
        add(m, Q(3, 4) * (a + c))
        if a >= 2:
            add((a - 2, b, c), -Q(a * (a - 1), 4)); add(m, Q(a * (a - 1), 4))
        if c >= 2:
            add((a, b, c - 2), -Q(c * (c - 1), 4)); add(m, Q(c * (c - 1), 4))
    elif which == 'V':
        p1, p2, coef_mixed, target = b, c, 2 * b * c, (a + 1, b - 1, c - 1)
        add(m, Q(3, 4) * (b + c))
        if b >= 2:
            add((a, b - 2, c), -Q(b * (b - 1), 4)); add(m, Q(b * (b - 1), 4))
        if c >= 2:
            add((a, b, c - 2), -Q(c * (c - 1), 4)); add(m, Q(c * (c - 1), 4))
    elif which == 'S':
        p1, p2, coef_mixed, target = a, b, 2 * a * b, (a - 1, b - 1, c + 1)
        add(m, Q(3, 4) * (a + b))
        if a >= 2:
            add((a - 2, b, c), -Q(a * (a - 1), 4)); add(m, Q(a * (a - 1), 4))
        if b >= 2:
            add((a, b - 2, c), -Q(b * (b - 1), 4)); add(m, Q(b * (b - 1), 4))
    else:
        raise AdmissionError('unknown Casimir ' + which)
    if p1 >= 1 and p2 >= 1:
        add(target, -Q(coef_mixed, 4)); add(m, Q(coef_mixed, 4))
    return {k: v for k, v in out.items() if v}


KINETIC_MODELS = {
    'R11_rho1': (3, 3, 1),            # the seven-link sum: 3 C_U + 3 C_V + C_shared (Round11 K1, rho=1)
    'shared_casimir_dropped': (3, 3, 0),
    'anisotropic_rho2': (3, 3, 2),
    'independent_rotor': (4, 4, 0),   # 4(C_U + C_V): the shared-link cross term 2 L_U.R_V dropped
}


def kinetic(p, model='R11_rho1'):
    cU, cV, cS = KINETIC_MODELS[model]
    out = {}
    for m, v in p.items():
        for coef, which in ((cU, 'U'), (cV, 'V'), (cS, 'S')):
            if coef:
                for k, w in casimir_terms(m, which).items():
                    out[k] = out.get(k, 0) + coef * v * w
    return {k: v for k, v in out.items() if v}


def eps_free(a, b, c):
    """Round11 E2: 3j(j+1)+3k(k+1)+ell(ell+1), j=(a+c)/2, k=(b+c)/2, ell=(a+b)/2."""
    j, k, l = Q(a + c, 2), Q(b + c, 2), Q(a + b, 2)
    return 3 * j * (j + 1) + 3 * k * (k + 1) + l * (l + 1)


def shell_min(d):
    """Round11 E3: exact minimum free energy in the orthogonal shell of degree d."""
    return Q(5, 8) * d * d + 2 * d + Q(3, 8) * (d % 2)


# ---------------------------------------------------------------------------
# Exact Gram projections: the monomial Gram matrix is block diagonal in the four link-flip parity classes.
# ---------------------------------------------------------------------------
def ldl_exact(M):
    """Exact LDL^T of a symmetric positive definite Fraction matrix (every pivot must be positive)."""
    n = len(M)
    A = [list(r) for r in M]
    L = [[Q(0)] * n for _ in range(n)]
    d = [Q(0)] * n
    for k in range(n):
        d[k] = A[k][k]
        require(d[k] > 0, 'Gram pivot not positive')
        L[k][k] = Q(1)
        for i in range(k + 1, n):
            L[i][k] = A[i][k] / d[k]
        for i in range(k + 1, n):
            lik = L[i][k]
            if lik:
                f = lik * d[k]
                for j in range(k + 1, i + 1):
                    if L[j][k]:
                        A[i][j] -= f * L[j][k]
    return L, d


class GramSolver:
    """Exact solver for G z = c on span(basis), G_ij = <m_i, m_j>; verifies the parity-block structure."""

    def __init__(self, bs):
        self.bs = bs
        classes = {}
        for i, m in enumerate(bs):
            classes.setdefault(parity_class(m), []).append(i)
        self.blocks = [classes[k] for k in sorted(classes)]
        # the Gram matrix couples only equal parity classes (link-flip Haar symmetry); verified entrywise
        off = 0
        for i, p in enumerate(bs):
            for j, q in enumerate(bs):
                if parity_class(p) != parity_class(q) and moment(p[0] + q[0], p[1] + q[1], p[2] + q[2]):
                    off += 1
        require(off == 0, 'Gram matrix is not block diagonal in the parity classes')
        self.fac = []
        for idx in self.blocks:
            M = [[moment(bs[i][0] + bs[j][0], bs[i][1] + bs[j][1], bs[i][2] + bs[j][2]) for j in idx] for i in idx]
            self.fac.append(ldl_exact(M))

    def solve(self, c):
        x = [Q(0)] * len(c)
        for idx, (L, d) in zip(self.blocks, self.fac):
            y = [c[i] for i in idx]
            n = len(y)
            for i in range(n):
                acc = y[i]
                for j in range(i):
                    if L[i][j] and y[j]:
                        acc -= L[i][j] * y[j]
                y[i] = acc
            y = [y[i] / d[i] for i in range(n)]
            for i in range(n - 1, -1, -1):
                acc = y[i]
                for j in range(i + 1, n):
                    if L[j][i] and y[j]:
                        acc -= L[j][i] * y[j]
                y[i] = acc
            for k, i in enumerate(idx):
                x[i] = y[k]
        return x

    def poly(self, z):
        return {m: v for m, v in zip(self.bs, z) if v}


class Shell:
    """The orthogonal shell of degree d relative to P_{d-1}: the vectors Q_{d-1} m_s (a+b+c=d) must be exactly
    mutually orthogonal (one spin-network sector per monomial); verified by an exactly diagonal Schur complement."""

    def __init__(self, d, gs_below):
        self.d = d
        self.gs = gs_below
        self.sectors = [m for m in basis(d) if sum(m) == d]
        bsb = gs_below.bs
        self.B = [[moment(p[0] + t[0], p[1] + t[1], p[2] + t[2]) for p in bsb] for t in self.sectors]
        self.Y = [gs_below.solve(col) for col in self.B]
        self.sigma = []
        for i, t in enumerate(self.sectors):
            self.sigma.append(moment(2 * t[0], 2 * t[1], 2 * t[2]) - dot(self.B[i], self.Y[i]))
        require(all(x > 0 for x in self.sigma), 'shell sector norm not positive')
        self.offdiag_nonzero = 0
        self.pairs_checked = 0
        for i in range(len(self.sectors)):
            for j in range(i + 1, len(self.sectors)):
                ti, tj = self.sectors[i], self.sectors[j]
                val = moment(ti[0] + tj[0], ti[1] + tj[1], ti[2] + tj[2]) - dot(self.B[i], self.Y[j])
                self.pairs_checked += 1
                if val:
                    self.offdiag_nonzero += 1
        require(self.offdiag_nonzero == 0, 'shell sectors are not mutually orthogonal')

    def components(self, p, c_below):
        """<Q_{d-1} m_s, p> for every sector, given c_below = <m_i, p> on P_{d-1}."""
        out = []
        for i, t in enumerate(self.sectors):
            tot = Q(0)
            for (a, b, c), w in p.items():
                mm = moment(a + t[0], b + t[1], c + t[2])
                if mm:
                    tot += w * mm
            out.append(tot - dot(self.Y[i], c_below))
        return out

    def weights(self, p, c_below):
        return [g * g / sg for g, sg in zip(self.components(p, c_below), self.sigma)]


def sector_class(t, D):
    """Spin labels of a shell sector (a,b,c): j=(a+c)/2 on h1,vL,h3; k=(b+c)/2 on h2,vR,h4; ell=(a+b)/2 on vM.
    Returns the set of link classes whose spin exceeds the per-link retained maximum D/2."""
    a, b, c = t
    out = set()
    if a + c > D:
        out.add('j')
    if b + c > D:
        out.add('k')
    if a + b > D:
        out.add('ell')
    return out


def boundary_class(t, D):
    """Shell-D sectors whose link spin equals the retained maximum D/2 (the per-link boundary layer)."""
    a, b, c = t
    out = set()
    if a + c == D:
        out.add('j')
    if b + c == D:
        out.add('k')
    if a + b == D:
        out.add('ell')
    return out


# ---------------------------------------------------------------------------
# Energy thresholds of the omitted space (Round11 E2/E3), per link class and for the joint product channel.
# ---------------------------------------------------------------------------
def thresholds(D):
    """Exact minima of the free electric energy over omitted sectors (total degree >= D+1), by class.
    Enumeration stops once the shell minimum m_d (E3, increasing in d) exceeds every current class minimum."""
    preds = {
        'all': lambda a, b, c: True,
        'j': lambda a, b, c: a + c > D,
        'k': lambda a, b, c: b + c > D,
        'ell': lambda a, b, c: a + b > D,
        'product': lambda a, b, c: a + c <= D and b + c <= D and a + b <= D,
    }
    best = {k: None for k in preds}
    d = D + 1
    shells_checked = []
    while True:
        shell = [(a, b, d - a - b) for a in range(d + 1) for b in range(d - a + 1)]
        smin = min(eps_free(*t) for t in shell)
        require(smin == shell_min(d), 'E3 shell minimum formula fails at degree %d' % d)
        shells_checked.append(d)
        for key, pred in preds.items():
            for t in shell:
                if pred(*t):
                    e = eps_free(*t)
                    if best[key] is None or e < best[key][0]:
                        best[key] = (e, t)
        if all(best[k] is not None for k in best) and shell_min(d + 1) > max(best[k][0] for k in best):
            break
        d += 1
        require(d <= 6 * (D + 1), 'threshold enumeration did not terminate')
    return best, shells_checked


# ---------------------------------------------------------------------------
# Decimal Ritz proposal (a proposal only: its output is rounded to an exact integer vector and certified exactly).
# ---------------------------------------------------------------------------
DCTX = decimal.Context(prec=110, rounding=decimal.ROUND_HALF_EVEN)
RITZ_ITERATIONS = 40
RITZ_SCALE = 10 ** 100


def to_dec(x):
    x = Q(x)
    return DCTX.divide(decimal.Decimal(x.numerator), decimal.Decimal(x.denominator))


class RitzProposal:
    """Inverse iteration (A - sigma G) w = G v in 110-digit decimal arithmetic on P_D; sigma = -tau^2/6 - 1/1000."""

    def __init__(self, D):
        bs = basis(D)
        self.bs = bs
        n = len(bs)
        kp = [kinetic({q: Q(1)}) for q in bs]
        self.G = [[to_dec(moment(p[0] + q[0], p[1] + q[1], p[2] + q[2])) for q in bs] for p in bs]
        self.AK = [[to_dec(sum((v * moment(p[0] + k[0], p[1] + k[1], p[2] + k[2]) for k, v in kp[j].items()), Q(0)))
                    for j in range(n)] for p in bs]
        self.MV = [[to_dec(moment(p[0] + q[0] + 1, p[1] + q[1], p[2] + q[2]) + moment(p[0] + q[0], p[1] + q[1] + 1, p[2] + q[2]))
                    for q in bs] for p in bs]

    def vector(self, tau):
        n = len(self.bs)
        taud = to_dec(tau)
        sigma = to_dec(-tau * tau / 6 - Q(1, 1000))
        M = [[DCTX.subtract(DCTX.subtract(self.AK[i][j], DCTX.multiply(taud, self.MV[i][j])), DCTX.multiply(sigma, self.G[i][j]))
              for j in range(n)] for i in range(n)]
        L = [[decimal.Decimal(0)] * n for _ in range(n)]
        dg = [decimal.Decimal(0)] * n
        for k in range(n):
            acc = M[k][k]
            for j in range(k):
                acc = DCTX.subtract(acc, DCTX.multiply(DCTX.multiply(L[k][j], L[k][j]), dg[j]))
            dg[k] = acc
            require(acc > 0, 'decimal proposal: shifted matrix not positive definite')
            for i in range(k + 1, n):
                t = M[i][k]
                for j in range(k):
                    t = DCTX.subtract(t, DCTX.multiply(DCTX.multiply(L[i][j], L[k][j]), dg[j]))
                L[i][k] = DCTX.divide(t, acc)
        v = [decimal.Decimal(0)] * n
        v[0] = decimal.Decimal(1)
        for _ in range(RITZ_ITERATIONS):
            y = []
            for row in self.G:
                acc = decimal.Decimal(0)
                for a, b in zip(row, v):
                    if b:
                        acc = DCTX.add(acc, DCTX.multiply(a, b))
                y.append(acc)
            for i in range(n):
                acc = y[i]
                for j in range(i):
                    acc = DCTX.subtract(acc, DCTX.multiply(L[i][j], y[j]))
                y[i] = acc
            y = [DCTX.divide(y[i], dg[i]) for i in range(n)]
            for i in range(n - 1, -1, -1):
                acc = y[i]
                for j in range(i + 1, n):
                    acc = DCTX.subtract(acc, DCTX.multiply(L[j][i], y[j]))
                y[i] = acc
            v = [DCTX.divide(x, y[0]) for x in y]
        return [round(Q(x) * RITZ_SCALE) for x in v]


# ---------------------------------------------------------------------------
# Exact certificate at one (D, tau):  complete residual, itemized ledger, energy and Wilson enclosures, tails.
# ---------------------------------------------------------------------------
WEYL_FREE_GAP = Q(3)      # E_1(K) = m_1 = 3 (Round11 E3; span{x,y})
V_NORM_PER_TAU = Q(2)     # ||W_1 + W_2|| <= 2
EXPORT_DIGITS = 45        # outward rounding of exported enclosure ends to denominator 10^45


class PerCutoff:
    def __init__(self, D, tail_lower_contract):
        self.D = D
        self.bs = basis(D)
        self.gs = GramSolver(self.bs)
        self.gs_below = GramSolver(basis(D - 1))
        self.shell_next = Shell(D + 1, self.gs)          # first omitted shell (the complete leakage lives here)
        self.shell_top = Shell(D, self.gs_below)         # top retained shell (per-link boundary layers)
        self.proposal = RitzProposal(D)
        self.thr, self.thr_shells = thresholds(D)
        self.tail_lower = self.thr['all'][0]
        require(self.tail_lower == shell_min(D + 1) == tail_lower_contract, 'tail_lower differs from E3 or the contract')


def certify(pc, tau, vector=None):
    """Exact certificate for H_FG = K - tau (W_1 + W_2) on the physical space at cutoff pc.D."""
    D, bs, gs = pc.D, pc.bs, pc.gs
    tau = rat(tau)
    w = pc.proposal.vector(tau) if vector is None else vector
    vp = {m: Q(c) for m, c in zip(bs, w) if c}
    require(vp and pdeg(vp) <= D, 'Ritz vector outside P_D')
    N = inner(vp, vp)
    Kv = kinetic(vp)
    xv, yv = pshift(vp, EX), pshift(vp, EY)
    t = padd(xv, yv)
    Hv = padd(Kv, t, -tau)
    mu = inner(vp, Hv) / N
    rho2 = inner(Hv, Hv) / N - mu * mu
    wR = inner(vp, xv) / N
    wR_y = inner(vp, yv) / N
    w2R = inner(xv, xv) / N
    # retained (P_D) and omitted (Q_D) parts of the complete residual (H - mu) v
    r = padd(Hv, vp, -mu)
    cr = proj_coeffs(bs, r)
    rP2 = dot(cr, gs.solve(cr)) / N
    cx, cy = proj_coeffs(bs, xv), proj_coeffs(bs, yv)
    zx, zy = gs.solve(cx), gs.solve(cy)
    QX = (inner(xv, xv) - dot(cx, zx)) / N
    QY = (inner(yv, yv) - dot(cy, zy)) / N
    QXY = (inner(xv, yv) - dot(cx, zy)) / N
    ct = [a + b for a, b in zip(cx, cy)]
    zt = [a + b for a, b in zip(zx, zy)]
    PQ = inner(t, t) / N - dot(ct, zt) / N
    rhoQ2 = tau * tau * PQ
    sec_w = [x / N for x in pc.shell_next.weights(t, ct)]
    sec_x = [x / N for x in pc.shell_next.weights(xv, cx)]
    sec_y = [x / N for x in pc.shell_next.weights(yv, cy)]
    # per-link boundary layer of the Ritz vector (top retained shell, link spin exactly D/2)
    cvb = proj_coeffs(pc.gs_below.bs, vp)
    top_w = [x / N for x in pc.shell_top.weights(vp, cvb)]
    # certified gap (Weyl: E_1(H) >= E_1(K) - ||V||) and Temple / Davis-Kahan (complete residual)
    b = WEYL_FREE_GAP - V_NORM_PER_TAU * abs(tau)
    rho_lo, rho_up = sqrt_bracket(rho2)
    ok = mu < b
    E0_temple = mu - rho2 / (b - mu) if ok else None
    s_A = rho_up / (b - mu) if ok else None
    # Round11 tail comparison (T1-T5) with the solver's tail bound: H >= B (+) R Q_D, B = A - C C*/(tau_t - R)
    tail_t = pc.tail_lower - V_NORM_PER_TAU * abs(tau)
    R = b
    require(R < tail_t, 'comparison threshold must lie below the tail threshold')
    beta0 = mu - rhoQ2 / (tail_t - R)
    Pt = gs.poly(zt)
    Qt = padd(t, Pt, -1)
    VQt = pmul({EX: Q(1), EY: Q(1)}, Qt)
    cc = proj_coeffs(bs, VQt)
    CCv = pscale(gs.poly(gs.solve(cc)), tau * tau)             # C C* v = P_D V Q_D V v  (unnormalized)
    rPpoly = padd(padd(Kv, vp, -mu), Pt, -tau)                 # P_D (H - mu) v
    resid = padd(rPpoly, padd(CCv, vp, -rhoQ2), -1 / (tail_t - R))
    eta2 = inner(resid, resid) / N
    bB = b - V_NORM_PER_TAU ** 2 * tau * tau / (tail_t - R)    # lambda_1(B) >= lambda_1(A) - ||CC*||/(tau_t - R)
    ok = ok and beta0 < bB
    E0_r11 = beta0 - eta2 / (bB - beta0) if ok else None
    res = {'D': D, 'tau': tau, 'w': w, 'N': N, 'mu': mu, 'rho2': rho2, 'rhoP2': rP2, 'rhoQ2': rhoQ2, 'PQ': PQ,
           'QX': QX, 'QY': QY, 'QXY': QXY, 'wR': wR, 'wR_y': wR_y, 'w2R': w2R, 'sec_w': sec_w, 'sec_x': sec_x, 'sec_y': sec_y,
           'top_w': top_w, 'gap_lower_b': b, 'residual_argument_ok': ok, 'tail_t': tail_t, 'R': R, 'beta0': beta0, 'eta2': eta2,
           'bB': bB, 'rho_bracket': (rho_lo, rho_up)}
    if not ok:
        return res
    E0_low = max(E0_temple, E0_r11)
    sB2 = (mu - E0_low) / (b - mu)
    s_B = sqrt_up(sB2)
    s_used = min(s_A, s_B)
    require(s_used < 1, 'angle bound must be below one')
    delta = 2 * s_used + 2 * s_used * s_used          # |<v,Wv> - <psi0,W psi0>| <= 2 s sigma_W + 2 s^2, sigma_W <= ||W|| <= 1
    lo, hi = wR - delta, wR + delta
    # certified tails of the TRUE ground state (Lemma C and its per-link form), using the tail threshold
    rhoQ_up = sqrt_up(rhoQ2)
    T_joint = (rhoQ_up + V_NORM_PER_TAU * abs(tau) * s_used) / (tail_t - mu)
    T_link = {}
    for cls, cfac in (('j', 1), ('k', 1), ('ell', 2)):
        lam2 = sum((wt for tt, wt in zip(pc.shell_top.sectors, top_w) if cls in boundary_class(tt, D)), Q(0))
        lam_up = sqrt_up(lam2)
        t_e = pc.thr[cls][0]
        T_link[cls] = {'boundary_layer_weight': lam2, 'threshold': t_e,
                       'bound': cfac * abs(tau) * (lam_up + s_used) / (t_e - V_NORM_PER_TAU * abs(tau) - mu), 'faces_touching': cfac}
    # arithmetic: directed square-root widths and the outward export rounding
    lo_out, hi_out = out_dn(lo, EXPORT_DIGITS), out_up(hi, EXPORT_DIGITS)
    E0_lo_out, E0_hi_out = out_dn(E0_low, EXPORT_DIGITS), out_up(mu, EXPORT_DIGITS)
    res.update({'E0_temple': E0_temple, 'E0_r11': E0_r11, 'E0_low': E0_low, 's_A': s_A, 's_B': s_B, 's_used': s_used,
                'delta': delta, 'lo': lo, 'hi': hi, 'lo_out': lo_out, 'hi_out': hi_out, 'E0_lo_out': E0_lo_out, 'E0_hi_out': E0_hi_out,
                'T_joint': T_joint, 'T_link': T_link, 'rhoQ_up': rhoQ_up,
                'arith_sqrt_width': rho_up - rho_lo, 'arith_export_width': (lo - lo_out) + (hi_out - hi)})
    return res


def classify_leakage(cert, pc):
    """Per-link, product-channel and corner weights of the complete omitted residual (exact, normalized)."""
    tau2 = cert['tau'] ** 2
    per = {'j': Q(0), 'k': Q(0), 'ell': Q(0)}
    prod = Q(0)
    corners = {}
    for t, wt in zip(pc.shell_next.sectors, cert['sec_w']):
        cls = sector_class(t, pc.D)
        for c in cls:
            per[c] += tau2 * wt
        if not cls:
            prod += tau2 * wt
        if len(cls) == 2:
            corners['+'.join(sorted(cls))] = tau2 * wt
        require(len(cls) <= 2, 'a shell sector cannot exceed the per-link maximum on all three link classes')
    return per, prod, corners


# ---------------------------------------------------------------------------
# Exact Rayleigh-Schroedinger series about the free ground state (full space: every psi_n lies in P_n).
# ---------------------------------------------------------------------------
def haar_mean(p):
    return sum((v * moment(*k) for k, v in p.items()), Q(0))


def solve_kinetic(f, D, model='R11_rho1'):
    """Solve K p = f with E[p] = 0 inside P_D by degree back-substitution (K is triangular in degree with diagonal
    eps_free on the monomial quotient).  Requires E[f] = 0.  The returned p satisfies K p = f EXACTLY as
    polynomials, i.e. the full-space resolvent equation, with zero omitted-space residual."""
    require(pdeg(f) <= D, 'right-hand side leaves P_D')
    rem = dict(f)
    p = {}
    for d in range(pdeg(f), 0, -1):
        top = {k: v for k, v in rem.items() if sum(k) == d}
        step = {k: v / eps_free(*k) for k, v in top.items()}
        p = padd(p, step)
        rem = padd(rem, kinetic(step, model), -1)
        require(all(sum(k) < d for k in rem), 'kinetic operator not triangular in degree')
    require(set(rem) <= {ZERO3} and rem.get(ZERO3, 0) == 0, 'solvability: E[f] must vanish')
    p = padd(p, {ZERO3: haar_mean(p)}, -1)
    require(padd(kinetic(p, model), f, -1) == {}, 'full-space resolvent equation K p = f not exact')
    require(haar_mean(p) == 0, 'intermediate normalization')
    return p


def rs_series(order, D, faces=((1, 0, 0), (0, 1, 0)), sign=-1, model='R11_rho1'):
    """H(tau) = K + tau V, V = sign * sum of the face traces; returns psi_n (intermediate normalization) and E^(n)."""
    V = {f: Q(sign) for f in faces}
    psi = [{ZERO3: Q(1)}]
    En = [Q(0)]
    for n in range(1, order + 1):
        Vpsi = pmul(V, psi[n - 1])
        En.append(haar_mean(Vpsi))
        rhs = pscale(Vpsi, Q(-1))
        for k in range(1, n + 1):
            rhs = padd(rhs, psi[n - k], En[k])
        psi.append(solve_kinetic(rhs, D, model))
        require(pdeg(psi[n]) <= n <= D, 'psi_n must lie in P_n inside P_D')
    return psi, En


def observable_series(psi, O, order):
    A = [sum((inner(psi[i], pmul(O, psi[n - i])) for i in range(n + 1)), Q(0)) for n in range(order + 1)]
    Nn = [sum((inner(psi[i], psi[n - i]) for i in range(n + 1)), Q(0)) for n in range(order + 1)]
    out = []
    for n in range(order + 1):
        out.append((A[n] - sum((out[k] * Nn[n - k] for k in range(n)), Q(0))) / Nn[0])
    return out


# ---------------------------------------------------------------------------
# Exact SU(2) fixtures: rational unit quaternions for the seven links and the six vertex gauge transformations.
# ---------------------------------------------------------------------------
def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def qinv(p):
    return (p[0], -p[1], -p[2], -p[3])


def rational_unit_quaternions(count):
    out = []
    for n in range(2, 40):
        for a in range(-n, n + 1):
            for b in range(0, n + 1):
                for c in range(0, n + 1):
                    r = n * n - a * a - b * b - c * c
                    if r < 0:
                        continue
                    d = isqrt(r)
                    if d * d == r and (b, c, d) != (0, 0, 0) and a != 0:
                        out.append((Q(a, n), Q(b, n), Q(c, n), Q(d, n)))
                        if len(out) >= count:
                            return out
    raise AdmissionError('not enough rational unit quaternions')


def holonomies(links):
    U = qmul(qmul(qmul(links['vM'], qinv(links['h3'])), qinv(links['vL'])), links['h1'])
    V = qmul(qmul(qmul(links['h2'], links['vR']), qinv(links['h4'])), qinv(links['vM']))
    return U, V


def invariants(links):
    U, V = holonomies(links)
    return (U[0], V[0], qmul(U, V)[0])     # x = Tr(U)/2, y = Tr(V)/2, z = Tr(UV)/2 (real parts of unit quaternions)


def gauge(links, g):
    return {e: qmul(qmul(g[ORIENT[e][0]], links[e]), qinv(g[ORIENT[e][1]])) for e in LINKS}


def sig_pair(q, sig=30):
    """Outward bracket of a signed rational with about `sig` significant digits (export only)."""
    q = Q(q)
    if q == 0:
        return Q(0), Q(0)
    k = sig - 1 - magnitude(q)
    return out_dn(q, k), out_up(q, k)


# ---------------------------------------------------------------------------
# BD2 contract: every grid value, cutoff, order, target, template and control id is read from the sha256-bound snapshot.
# ---------------------------------------------------------------------------
def load_contract():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen BD2 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'BD2' and c.get('round') == 33 and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


BD2_NEW_CONTROLS = ('graph_couplings_named', 'exact_rs_zero_truncation', 'independent_coupling_flip', 'enclosure_itemized_residual',
                    'formal_coefficient_labelled', 'evenness_from_flip', 'unbounded_observable_handled', 'band_both_signs',
                    'dimension_recount', 'no_area_law_claim', 'no_transfer_to_eqed', 'rate_range_stated', 'tier_mixing_rejected',
                    'changed_model_relabelled', 'parameters_declare_metric_weights_window')
BA1_INHERITED_CONTROLS = ('coherent_evidence_tampering', 'exact_arithmetic_admission', 'no_priority_or_continuum_claim',
                          'insufficient_verdict_retained', 'placeholder_span_rejected', 'negation_aware_phrase_scan')


def contract_values(c):
    pre = c['preregistration']
    par = c['parameters']
    v = {'contract': c, 'par': par, 'pre': pre}
    v['model'] = c['model']
    require('H_FG(l1,l2) = K - l1 W_1 - l2 W_2 on the Round11 two-plaquette graph (open two-square patch, 6 vertices, 7 links' in v['model']
            and 'zero-selected patterned family' in v['model'] and 're-instantiated in 2+1 dimensions' in v['model'], 'model string')
    # --- Hamiltonian terms (rule R3: every term named with its coefficient) ---
    terms = par['hamiltonian_terms']
    require(len(terms) == 6, 'six Hamiltonian term rows')
    require(terms[0]['term'] == 'K: sum of the seven link Casimirs of the Round11 two-square patch (rho=1)' and terms[0]['coefficient'] == '1 (alpha units)', 'K term')
    require(terms[1] == {'term': 'W_1 = (1/2) Tr U_1 of square 1', 'coefficient': '-l1'}, 'W_1 term')
    require(terms[2] == {'term': 'W_2 = (1/2) Tr U_2 of square 2', 'coefficient': '-l2'}, 'W_2 term')
    require(terms[3]['term'] == '2+1D model (item 5, constants only): electric 8 C_e on every link of Z^2' and terms[3]['coefficient'] == '8 (delta units), per link', '2+1D electric term')
    require(terms[4]['term'] == '2+1D model (item 5, constants only): W_f = (1/2) Tr U_f on every elementary face of Z^2' and terms[4]['coefficient'] == '-tau/3', '2+1D face term')
    require('selected faces 0 (AW1/AY1 model)' in terms[5]['term'] and '21 omitted faces per anchor' in terms[5]['term']
            and terms[5]['coefficient'] == '8 and -tau/3 (delta units)', 'Z^3 family term')
    v['terms'] = terms
    require(par['model_is_finite_graph'] is True, 'parameters.model_is_finite_graph')
    # --- graph grid and orders ---
    m = match(r'at l1=l2 in \{\+-1/(\d+), \+-1/(\d+), \+-1/(\d+)\} \(the AZ2 grid\) at D=(\d+) and D=(\d+)', par['graph_grid'], 'graph grid')
    v['grid'] = [Q(1, int(m.group(i))) for i in (1, 2, 3)]
    v['cutoffs'] = [int(m.group(4)), int(m.group(5))]
    require(v['grid'] == [Q(1, 1000), Q(1, 100), Q(1, 10)] and v['cutoffs'] == [6, 8], 'grid and cutoffs')
    m = match(r'of <W_1>, <z> and <C_shared> in \(l1,l2\) through total order (\d+) at D=(\d+) and D=(\d+)$', par['graph_orders'], 'graph orders')
    v['order'] = int(m.group(1))
    require(v['order'] == 4 and [int(m.group(2)), int(m.group(3))] == v['cutoffs'], 'order and cutoffs of the coefficient table')
    # --- Z^3 1x2 loop ---
    zz = par['z3_1x2']
    for frag in ('the 1x2 rectangle in the xz plane formed by the original xz face W (fine origin, r=0, s=0) and the xz face at the fine point e_x (r=1, s=0)',
                 'whose six links are all owned by R={0,e_z}, so W_{1x2} lies in B(H_R) with norm at most 1',
                 'first-order coefficient exactly 0 in every box (centre grading, Kato per box)',
                 "the certified bound |omega(W_{1x2})| <= K_2' tau^2 at both signs from the AY1 per-box ball (forward F11-F14)",
                 'Tr(P_R W_{1x2}) = Tr(rho^(1)_R W_{1x2}) = 0 by single-occurrence orthogonality',
                 'evenness in tau (AW1 flip lemma, area 2) in every open centered whole-star box at kappa=0 and every on-site cutoff',
                 'labelled formal_second_order_coefficient: no certified third-order remainder and no sign'):
        require(frag in zz, 'z3_1x2 parameter fragment: ' + frag[:40])
    v['z3_1x2'] = zz
    # --- electric band ---
    eb = par['electric_band']
    m = match(r'h_R the sum of (\d+) C_e over the (\d+) links of R in delta units', eb, 'band observable')
    v['band_casimir_factor'], v['band_links'] = int(m.group(1)), int(m.group(2))
    m = match(r'operator inequality h_R >= (\d+) Q_R \(I1: free Casimir gap (\d+) delta', eb, 'band operator inequality')
    v['band_gap'] = int(m.group(1))
    require(int(m.group(2)) == v['band_gap'], 'free Casimir gap')
    m = match(r'upper endpoint omega\(h_R\) <= (\d+)\|tau\| from the AQ1 reset \(HNM-AQ1\.1 with the (\d+) incident anchors of R', eb, 'band upper endpoint')
    v['band_upper_coeff'], v['band_anchors'] = int(m.group(1)), int(m.group(2))
    m = match(r"the AQ1 gate's generic (\d+)\|tau\|\|F\| at F=R is valid but is not the frozen endpoint", eb, 'generic reset budget')
    v['band_generic_coeff'] = int(m.group(1))
    m = match(r'exact rational endpoints at tau=10\^-(\d+)$', eb, 'band evaluation point')
    v['band_tau'] = Q(1, 10 ** int(m.group(1)))
    for frag in ('the Fuchs-van de Graaf inequality for the pure reference proved inline ((1/2)||rho_R - P_R||_1 <= sqrt(Tr(Q_R rho_R)), by convexity from the pure-state case)',
                 'for the limit, the AY2 gate item (2)', 'HNM-AY1-F11 to F14', 'the AY2 directed bracket of sqrt(10)',
                 'labelled as a reviewed step of the admitted AY1 proof and not as an AY1 or AY2 gate sentence',
                 'passed to the limit by lower semicontinuity of the monotone limit under trace-norm convergence on R',
                 'omega(h_R) is the monotone limit over the spectral projections Q_L of h_R of Tr(rho_R h_R Q_L)'):
        require(frag in eb, 'electric_band fragment: ' + frag[:40])
    v['electric_band'] = eb
    # --- 2+1 dimensions ---
    dm = par['dimension_2p1']
    for frag in ('per-link electric term 8 C_e, every elementary face with -(tau/3) W_f, no selected faces, Haar product reference',
                 'single-site factors owning the links (p,x) and (p,y), owner sets {p, p+e_x, p+e_y}, each face its own interaction term V_X on its owner set, three faces per site',
                 'the AM2 inverse uses the AM2 normalization h_x >= Q_x (unit on-site gap; the free Casimir gap 6 is not used)',
                 'the self-map condition J G_3(R) <= R and the exclusion condition 2 J G_3\'(R) < 1',
                 'the window kernel constants of AV2 (a one-dimensional spectral identity) are recorded as dimension-independent'):
        require(frag in dm, 'dimension_2p1 fragment: ' + frag[:40])
    m = match(r'maximal support p=(\d+)', dm, 'maximal support')
    v['p2'] = int(m.group(1))
    m = match(r'the radius is the AM2 radius R=1/(\d+)', dm, 'AM2 radius')
    v['R_am2'] = Q(1, int(m.group(1)))
    require(v['p2'] == 3 and v['R_am2'] == Q(1, 64), '2+1D declared p and radius')
    v['dimension_2p1'] = dm
    v['N_min'] = int(par['N_min'])
    require(v['N_min'] == 2, 'N_min')
    for key in ('metric', 'weights', 'window', 'clock'):
        require(isinstance(par.get(key), str) and par[key], 'parameters.' + key + ' missing')
    # --- preregistration ---
    require(pre['schema'] == 'hnm-r33-prereg-v1' and pre['frozen_before_any_outcome'] is True, 'prereg schema')
    tg = pre['target']
    v['target'] = rat(tg['value'])
    v['target_comparator'] = tg['comparator']
    v['target_quantity'] = tg['quantity']
    require(v['target'] == Q(1, 10 ** 16) and v['target_comparator'] == '<=' and 'with l1=l2 nonzero, at D=8' in v['target_quantity'], 'target')
    require('(upper - lower)/min(|lower|, |upper|) of the exported exact enclosure' in tg['note'], 'relative width definition')
    v['target_note'] = tg['note']
    m = match(r'^graph grid as in parameters\.graph_grid; (\d+)/(\d+) for the Z\^3 items$', pre['tau']['value'], 'tau value')
    v['tau_z3'] = Q(int(m.group(1)), int(m.group(2)))
    require(v['tau_z3'] == v['band_tau'] == Q(1, 10 ** 8), 'Z^3 evaluation point')
    v['signs'] = list(pre['tau']['signs_evaluated'])
    require(v['signs'] == ['+', '-'] and pre['tau']['rule_if_chosen_later'] is None, 'both signs')
    v['model_id'] = pre['model_id']
    require(v['model_id'] == 'FG(round11_two_plaquette_independent_couplings)' and pre['model_is_finite_graph'] is True, 'model id')
    v['selected_triple'] = list(pre['selected_triple_alpha_units'])
    require(v['selected_triple'] == ['0', '0', '0'], 'selected triple')
    v['tier_names'] = list(pre['tier_names_allowed'])
    require(v['tier_names'] == ['exact_first_order', 'first_order_distance_from_product', 'crude_majorant'], 'tier names')
    v['tier_rule'] = pre['tier_label_rule']
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['outcomes'] = list(pre['expected_outcome_types'])
    require(v['outcomes'] == ['accepted_within_scope', 'limited', 'insufficient'], 'outcome types')
    v['error_terms'] = list(pre['error_terms_itemized'])
    require(v['error_terms'] == ['graph_truncation_zero', 'graph_residual_itemized', 'flip_parity_graph', 'z3_formal_coefficient',
                                 'band_lower_trace_duality', 'band_upper_energy_budget', 'cutoff_monotone_passage', 'dimension_recount', 'arithmetic'],
            'preregistered error terms')
    v['error_terms_rule'] = pre['error_terms_rule']
    sb = pre['scaling_brackets_per_constant']
    m = match(r'\[(\d+),(\d+)\]$', sb['band_lower'], 'band_lower bracket')
    v['bracket_band_lower'] = (Q(int(m.group(1))), Q(int(m.group(2))))
    m = match(r'exactly (\d+)$', sb['band_upper'], 'band_upper bracket')
    v['bracket_band_upper'] = Q(int(m.group(1)))
    m = match(r'ratio exactly (\d+)\)$', sb['z3_formal'], 'z3_formal bracket')
    v['bracket_z3_formal'] = Q(int(m.group(1)))
    require(sb['dimension_constants'] == 'tau-independent' and sb['graph_coefficients'].endswith('(not applicable)'), 'other brackets')
    v['scaling_brackets'] = dict(sb)
    v['gate_fields'] = dict(pre['gate_fields_required'])
    require(v['gate_fields'] == {'model_is_finite_graph': True, 'transfers_to_aq': False, 'graph_sign_certified': True, 'z3_1x2_formal_only': True,
                                 'electric_band_claimed': True,
                                 'electric_band_scope': 'omega(h_R) for every finite box of F1 and F2 (untruncated at fixed N) and the limit of the named constructions, both signs',
                                 'area_law_claimed': False, 'uniqueness_of_ground_state_claimed': False, 'rate_in_a_claimed': False,
                                 'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False}, 'gate fields')
    v['gate_fields_rule'] = pre['gate_fields_rule']
    v['sentence'] = pre['mandatory_sentence_template']
    require(v['sentence'].startswith('On the Round11 two-plaquette graph with independent couplings,') and v['sentence'].endswith('not a statement uniform in the lattice spacing a.'),
            'mandatory template')
    v['forbidden'] = list(pre['forbidden_phrasings'])
    require(v['forbidden'] == ['the infinite-volume ground state', 'the thermodynamic limit', 'the AQ state', 'correlation length', 'uniform in a',
                               'confirms', 'predicts', 'string tension', 'confinement'], 'forbidden phrasings')
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']) and len(v['controls']) == 21, 'controls list equals the preregistered ids')
    require(set(BD2_NEW_CONTROLS) <= set(c['new_control_semantics']) and set(BD2_NEW_CONTROLS) | set(BA1_INHERITED_CONTROLS) == set(v['controls']),
            'control semantics: BD2 overrides plus BA1-inherited definitions')
    v['control_semantics'] = dict(c['new_control_semantics'])
    v['control_semantics_note'] = c['control_semantics_note']
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['acceptance'] = dict(c['acceptance'])
    v['shared'] = list(c['shared_premises'])
    v['required'] = list(c['required'])
    require(len(v['required']) == 7 and all(v['required'][k].startswith('%d. ' % (k + 1)) for k in range(7)), 'seven required items')
    v['hash_binding'] = dict(pre['hash_binding'])
    require(all(v['hash_binding'].get(k) is True for k in ('contract_sha256_in_producer_inputs', 'check_py_reads_target_and_reference_from_contract',
                                                          'check_py_sha256_recorded_before_full_size_evaluation', 'admitted_gate_sha256_pinned_in_check_py')),
            'hash binding')
    require(c['direction'] == 'single+skeptic' and pre['direction'] == 'single+skeptic' and c['producers'] == ['forward']
            and c.get('reverse_premise_isolation') is False, 'direction')
    require(pre['nodes']['s_values'] == [] and pre['nodes']['post_hoc_node_selection'] == 'forbidden', 'no Euclidean nodes')
    v['state_provenance'] = pre['state_provenance']
    v['observable_block'] = dict(pre['observable'])
    require(pre['observable']['centering'] == 'none' and pre['observable']['reference_route'] == 'Haar', 'observable block')
    v['clock_pre'] = pre['clock']
    v['selected_after'] = c.get('selected_after')
    v['stop'] = c.get('stop', '')
    return v


# ---------------------------------------------------------------------------
# Round33 phrase scan (infrastructure copied from research/round33/tools/phrase_scan.py; computes no scientific result).
# ---------------------------------------------------------------------------
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


def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def clauses(text):
    return [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', text) if c.strip()]


def phrase_hits(text, forbidden, template=None):
    body = normalize(text)
    if template:
        body = body.replace(normalize(template), ' ')
    hits = []
    for clause in clauses(body):
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                hits.append({'phrase': phrase, 'clause': clause[:240], 'negated': bool(NEGATION.search(clause))})
    return hits


def affirmative(hits):
    return [h for h in hits if not h['negated']]


PLACEHOLDER = re.compile(r'<(?!=)([^<>\n]*)>')


def placeholder_spans(text):
    """(freezer R1 reading) angle-bracket spans containing whitespace, a vertical bar or 'e.g.'."""
    return [m.group(0) for m in PLACEHOLDER.finditer(text) if re.search(r'\s|\||e\.g\.', m.group(1))]


def all_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, val in obj.items():
            yield str(k)
            yield from all_strings(val)
    elif isinstance(obj, (list, tuple)):
        for val in obj:
            yield from all_strings(val)


def top_level_block(text, header):
    """The top-level block of a source file that starts with `header` (a def/class/assignment line)."""
    lines = text.split('\n')
    starts = [i for i, ln in enumerate(lines) if ln.startswith(header)]
    require(len(starts) == 1, 'source block not found exactly once: ' + header)
    i = starts[0]
    j = i + 1
    while j < len(lines) and (lines[j] == '' or lines[j][0] in ' \t'):
        j += 1
    return '\n'.join(lines[i:j]).rstrip()


# ---------------------------------------------------------------------------
# Item 1: bivariate Rayleigh-Schroedinger series for H_FG(l1,l2) = K - l1 x - l2 y (full graph space, exact).
# ---------------------------------------------------------------------------
def apply_casimir(p, which):
    out = {}
    for m, val in p.items():
        for k, w in casimir_terms(m, which).items():
            out[k] = out.get(k, 0) + val * w
    return {k: Q(val) for k, val in out.items() if val}


OBSERVABLES = {'W_1': lambda p: pshift(p, EX), 'W_2': lambda p: pshift(p, EY), 'z': lambda p: pshift(p, EZ),
               'C_shared': lambda p: apply_casimir(p, 'S')}


def rs2_series(order, D, model='R11_rho1', couple=(True, True)):
    """H(l1,l2) = K + l1 V1 + l2 V2 with V1 = -x (= -W_1) and V2 = -y (= -W_2); intermediate normalization
    E[psi_mn] = 0 for (m,n) != (0,0).  K psi_mn = -V1 psi_(m-1,n) - V2 psi_(m,n-1) + sum E_ij psi_(m-i,n-j), solved
    by degree back-substitution with the full-space polynomial identity checked (zero omitted residual)."""
    psi = {(0, 0): {ZERO3: Q(1)}}
    En = {(0, 0): Q(0)}
    for n in range(1, order + 1):
        for m in range(n + 1):
            k = n - m
            src = {}
            if m >= 1 and couple[0]:
                src = padd(src, pmul({EX: Q(-1)}, psi[(m - 1, k)]))
            if k >= 1 and couple[1]:
                src = padd(src, pmul({EY: Q(-1)}, psi[(m, k - 1)]))
            En[(m, k)] = haar_mean(src)
            rhs = pscale(src, Q(-1))
            for (i, j), e in list(En.items()):
                if (i, j) != (0, 0) and i <= m and j <= k and e:
                    rhs = padd(rhs, psi[(m - i, k - j)], e)
            psi[(m, k)] = solve_kinetic(rhs, D, model)
            require(pdeg(psi[(m, k)]) <= n <= D, 'psi_mn must lie in P_(m+n) inside P_D')
    return psi, En


def table_keys(order):
    return [(m, n - m) for n in range(order + 1) for m in range(n, -1, -1)]


def obs2(psi, O, order):
    keys = table_keys(order)
    A, Nn = {}, {}
    for (m, n) in keys:
        a_ = Q(0)
        nn = Q(0)
        for i in range(m + 1):
            for j in range(n + 1):
                a_ += inner(psi[(i, j)], O(psi[(m - i, n - j)]))
                nn += inner(psi[(i, j)], psi[(m - i, n - j)])
        A[(m, n)], Nn[(m, n)] = a_, nn
    out = {}
    for (m, n) in keys:
        acc = A[(m, n)]
        for (k, l) in keys:
            if k <= m and l <= n and (k, l) != (m, n):
                acc -= out[(k, l)] * Nn[(m - k, n - l)]
        out[(m, n)] = acc / Nn[(0, 0)]
    return out


def diagonal(tab, order):
    return [sum((val for (m, n), val in tab.items() if m + n == o), Q(0)) for o in range(order + 1)]


def flip_poly(p, signs):
    sx, sy, sz = signs
    return {m: val * (sx ** m[0]) * (sy ** m[1]) * (sz ** m[2]) for m, val in p.items()}


def tab_str(tab):
    return {'%d,%d' % k: s(val) for k, val in tab.items()}


# ---------------------------------------------------------------------------
# Item 2: the certified <z> enclosure re-uses the AZ2 certificate of the ground state (same Hamiltonian at l1=l2).
# ---------------------------------------------------------------------------
Z_NORM = Q(1)   # ||z|| = sup |Tr(UV)|/2 = 1 (attained at the identity configuration)


def certify_z(pc, tau):
    ct = certify(pc, tau)
    require(ct['residual_argument_ok'] and 'delta' in ct, 'residual argument failed')
    vp = {m: Q(c_) for m, c_ in zip(pc.bs, ct['w']) if c_}
    zR = inner(vp, pshift(vp, EZ)) / ct['N']
    delta_z = 2 * ct['s_used'] * Z_NORM + 2 * ct['s_used'] ** 2 * Z_NORM
    lo, hi = zR - delta_z, zR + delta_z
    ct.update({'zR': zR, 'delta_z': delta_z, 'z_lo': lo, 'z_hi': hi, 'z_lo_out': out_dn(lo, EXPORT_DIGITS), 'z_hi_out': out_up(hi, EXPORT_DIGITS)})
    return ct


def rel_width(lo, hi):
    return (hi - lo) / min(abs(lo), abs(hi))


# ---------------------------------------------------------------------------
# Items 3-4: fine Z^3 geometry of the I1 blocking (read, not typed: the I1.1 map and the selected-strip rule).
# ---------------------------------------------------------------------------
FDIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}


def vadd(p, d, k=1):
    return (p[0] + k * d[0], p[1] + k * d[1], p[2] + k * d[2])


def coarse(p):
    """I1.1: pi(x,y,z) = (floor(x/4), floor(y/2), z) (Euclidean division, negative coordinates included)."""
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(f):
    p, a, c = f
    return ((p, a), (vadd(p, FDIRS[a]), c), (vadd(p, FDIRS[c]), a), (p, c))


def face_owners(f):
    """I1.4: owner set {pi(p), pi(p+e_a), pi(p+e_c)} (tails of the four links)."""
    return frozenset(coarse(l[0]) for l in face_links(f))


def is_selected(f):
    """Selected strip: xy faces at (4i+r, 2j, k), r=0,1,2 (coefficient 0 at the zero triple)."""
    p, a, c = f
    return (a, c) == ('x', 'y') and p[0] % 4 in (0, 1, 2) and p[1] % 2 == 0


def in_flip_set(link):
    """AW1 flip set E: x-links with p_y even, y-links with p_z even, z-links with p_x even."""
    p, d = link
    return {'x': p[1], 'y': p[2], 'z': p[0]}[d] % 2 == 0


def link_counter(loops):
    cnt = {}
    for loop in loops:
        for l in loop:
            cnt[l] = cnt.get(l, 0) + 1
    return cnt


def grading_zero(loops):
    """AW1 F04 (centre grading): the Haar mean of a product of loop traces vanishes unless every link is covered evenly."""
    return any(val % 2 for val in link_counter(loops).values())


def window_faces():
    out = []
    for px in range(-8, 12):
        for py in range(-4, 6):
            for pz in range(-3, 5):
                for (a, c) in (('x', 'y'), ('x', 'z'), ('y', 'z')):
                    out.append(((px, py, pz), a, c))
    return out


# ---------------------------------------------------------------------------
# Item 5: 2+1-dimensional recount (declared factorization) and the AM2 counting for general p.
# ---------------------------------------------------------------------------
def am2_numerator(p, k):
    """AM2 (HNM-AM2.5) counting for support |X|<=p: 2^p (2p)^k [1 + k(p+1)/p] (two root placements)."""
    return 2 ** p * (2 * p) ** k * (1 + Q(k * (p + 1), p))


def g_closed_form_coeffs(p, kmax):
    """k! [t^k] of 2^p e^{2pt} (1 + 2(p+1) t)."""
    out = []
    for k in range(kmax + 1):
        c_ = Q(2 ** p * (2 * p) ** k)
        if k >= 1:
            c_ += Q(2 ** p * 2 * (p + 1) * k * (2 * p) ** (k - 1))
        out.append(c_)
    return out


def exp_bracket(x, n):
    """Directed rational bracket of e^x (0 < x < 1): partial sum and partial sum plus the geometric tail bound."""
    x = rat(x)
    require(0 < x < 1, 'exp bracket range')
    S = sum((x ** k / factorial(k) for k in range(n + 1)), Q(0))
    tail = x ** (n + 1) / factorial(n + 1) * Q(n + 2) / (n + 2 - x)
    return S, S + tail


def mat_zero(n):
    return [[Q(0)] * n for _ in range(n)]


def mat_mul(A, B):
    n = len(A)
    out = mat_zero(n)
    for i in range(n):
        for k in range(n):
            if A[i][k]:
                aik = A[i][k]
                row = B[k]
                for j in range(n):
                    if row[j]:
                        out[i][j] += aik * row[j]
    return out


def mat_sub(A, B):
    return [[a - b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def kron(A, B):
    n, m = len(A), len(B)
    out = mat_zero(n * m)
    for i in range(n):
        for j in range(n):
            if A[i][j]:
                for k in range(m):
                    for l in range(m):
                        if B[k][l]:
                            out[i * m + k][j * m + l] = A[i][j] * B[k][l]
    return out


def creation_fixture(p, kmax):
    """AM2-type exact fixture on p qubits: C = sum_x sigma^+_x, V = tensor of sigma^-; returns ad_C^k(V) Omega for k<=kmax
    and whether ad_C^kmax(V) vanishes as an operator."""
    I2 = [[Q(1), Q(0)], [Q(0), Q(1)]]
    sp = [[Q(0), Q(0)], [Q(1), Q(0)]]      # |1><0|
    sm = [[Q(0), Q(1)], [Q(0), Q(0)]]      # |0><1|
    n = 2 ** p
    C = mat_zero(n)
    for x in range(p):
        op = [[Q(1)]]
        for y in range(p):
            op = kron(op, sp if y == x else I2)
        C = [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(C, op)]
    Vop = [[Q(1)]]
    for y in range(p):
        Vop = kron(Vop, sm)
    ad = Vop
    vecs = []
    for k in range(kmax + 1):
        if k:
            ad = mat_sub(mat_mul(C, ad), mat_mul(ad, C))
        vecs.append([row[0] for row in ad])     # ad^k(V) applied to Omega = |0...0> (first basis vector)
    vanishes = all(val == 0 for row in ad for val in row)
    return vecs, vanishes


def forward_verdict(graph_ok, band_ok, orders_complete, width_met, band_limit, dim_complete, w12_all, obligations_listed, overclaim):
    """Contract acceptance: insufficient if the graph algebra or the band cannot be established (or an excluded claim is
    made); limited if a graph order or cutoff is missing, an enclosure misses the width target, the band holds only for
    finite boxes, the 2+1D constants are incomplete, the W_{1x2} bound misses a box or the limit, or an obligation row is
    missing; otherwise accepted_within_scope."""
    if overclaim or not graph_ok or not band_ok:
        return 'insufficient'
    if not (orders_complete and width_met and band_limit and dim_complete and w12_all and obligations_listed):
        return 'limited'
    return 'accepted_within_scope'


def point_key(D, tau):
    sign = '+' if tau > 0 else ('-' if tau < 0 else '')
    return 'D%d_l%s%s' % (D, sign, s(abs(tau)))


# ---------------------------------------------------------------------------
def compute(check_sha):
    c, contract_digest = load_contract()          # sha256 verified before any evaluation
    V = contract_values(c)
    check('contract_snapshot_sha256',
          contract_digest == CONTRACT_SHA256 and len(V['controls']) == 21 and V['target'] == Q(1, 10 ** 16),
          contract_sha256=contract_digest, contract_path=CONTRACT_REL, check_py_sha256_recorded_before_evaluation=check_sha,
          grid_read_from_contract=[s(x) for x in V['grid']], cutoffs_read_from_contract=V['cutoffs'], order_read_from_contract=V['order'],
          target_read_from_contract=s(V['target']), target_comparator=V['target_comparator'], target_quantity=V['target_quantity'],
          z3_tau_read_from_contract=s(V['tau_z3']), band_upper_read_from_contract='%d|tau| (%d incident anchors)' % (V['band_upper_coeff'], V['band_anchors']),
          dimension_2p1_read_from_contract={'p': V['p2'], 'R': s(V['R_am2'])}, hash_binding=V['hash_binding'])

    # ======================= premise inventory, isolation and pinned hashes =======================
    expected_inputs = ['AGENTS.md', CONTRACT_REL] + V['shared']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    forbidden_prefixes = ('research/round33/forward/bd1', 'research/round33/reverse/', 'research/round33/forward/bc1', 'research/round33/forward/bc2',
                          'research/round33/experts/')
    allowed_skeptic = {'research/round33/skeptic/bb2.md', P_AZ2_SKEPTIC}

    def validate_inventory(inv):
        require(sorted(inv) == sorted(set(expected_inputs)) and len(inv) == 35, 'inputs differ from AGENTS.md + contract + shared premises')
        require(not any('__pycache__' in k or k.endswith('.pyc') for k in inv), 'interpreter cache in inputs')
        require(not any(k.startswith(forbidden_prefixes) for k in inv), 'isolation: a current-round producer or expert file in inputs')
        require({k for k in inv if '/skeptic/' in k} <= allowed_skeptic, 'isolation: an undeclared skeptic file in inputs')
        for k, h in PINNED.items():
            require(inv.get(k) == h, 'pinned premise hash differs: ' + k)
        require(inv.get(CONTRACT_REL) == contract_digest, 'contract snapshot hash')
        return True
    bad_inv = dict(inventory)
    bad_inv[P_AY1_GATE] = '0' * 64
    check('premise_inventory_and_pins',
          validate_inventory(inventory)
          and rejected(lambda: validate_inventory(bad_inv), 'pinned_gate_hash_changed')
          and rejected(lambda: validate_inventory(dict(inventory, **{'research/round33/forward/bd1/report.md': '0' * 64})), 'bd1_producer_file_in_inputs'),
          inventory_files=len(inventory), inputs_sha256=inventory, pinned=PINNED,
          isolation='inputs equal AGENTS.md + the BD2 contract + its 33 shared premises; no BD1/BC producer, current skeptic or expert file')

    # ======================= admitted gates: verdicts and the exact texts used =======================
    G = {k: load_json_input(k) for k in (P_AZ2_GATE, P_AW1_GATE, P_AV1_GATE, P_AV2_GATE, P_AY1_GATE, P_AY2_GATE, P_AM2_GATE, P_AQ1_GATE, P_BB2_GATE)}
    require(all(g['verdict'] == 'accepted_within_scope' for g in G.values()), 'every premise gate is accepted_within_scope')
    az2, aw1, av1, av2, ay1, ay2, am2g, aq1g, bb2 = (G[k] for k in (P_AZ2_GATE, P_AW1_GATE, P_AV1_GATE, P_AV2_GATE, P_AY1_GATE, P_AY2_GATE,
                                                                   P_AM2_GATE, P_AQ1_GATE, P_BB2_GATE))
    require('H_FG = K - tau_FG (W_1 + W_2)' in az2['accepted'] and 'second-order <W_1^2>, <W_1 W_2>, <z> equal 7/576, 79/2808, 7/216' in az2['accepted']
            and '(187/33696) tau_FG^3' in az2['accepted'] and 'E_0 = -tau_FG^2/6 + (187/67392) tau_FG^4' in az2['accepted'], 'AZ2 gate values')
    m = match(r'D=8, tau_FG=\+1/10: \[(\d+)/(\d+), (\d+)/(\d+)\]', az2['accepted'], 'AZ2 D=8 enclosure')
    az2_d8_w = [s(Q(int(m.group(1)), int(m.group(2)))), s(Q(int(m.group(3)), int(m.group(4))))]
    require('a_3 = -5/864, E_2 = -1/12' in az2['decision'] and 'tau^3/4212' in az2['decision'], 'AZ2 one-face values and second-square shift')
    require(az2['gate_fields'] == {'fg_coefficients_fitted': False, 'model_is_finite_graph': True, 'transfers_to_aq': False}, 'AZ2 gate fields')
    FLIP_E_TEXT = 'E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even}'
    for frag in (FLIP_E_TEXT, '(3) omega_tau(W)=+tau/144+r(tau) under I1.5',
                 'at kappa=0 omega_{N,-tau}(W)=-omega_{N,tau}(W) and omega_N(W^2), C_N, c_N are even in tau',
                 'for AQ limits S(-tau)=S(tau)o alpha_E as whole sets of subsequential limits', 'oddness gives no O(tau^3) remainder'):
        require(frag in aw1['accepted'], 'AW1 gate fragment ' + frag[:30])
    require('The on-site cutoff is removed for the ground vector itself in each fixed box' in av1['accepted'], 'AV1 gate cutoff-vector removal')
    require('M_0=||ghat||_1=2, M_1=4s/pi, M_2=2s^2' in av2['accepted'], 'AV2 window constants')
    for frag in ('reset omega(h_R)<=98|tau| and C_F=56|tau||F|', 'with ||rho^(1)_R||_1=sqrt(10)|tau|/72',
                 "for every subsequential limit of either family ||rho_R-P_R-rho^(1)_R||_1<=K_2' tau^2",
                 'the common first-order density is rho^(1)_R=(tau/72) sum_{f in F_R}(|W_f Omega_R><Omega_R|+|Omega_R><W_f Omega_R|) over the 10 faces F_R with owner set exactly R'):
        require(frag in ay1['accepted'], 'AY1 gate fragment ' + frag[:30])
    m = match(r"R-local trace-norm constant K_2'=(\d+)/(\d+) ", ay1['accepted'], "AY1 K_2'")
    K2p = Q(int(m.group(1)), int(m.group(2)))
    m = match(r'certified at \|tau\|=10\^-8 with the directed bracket sqrt\(10\) in \[(\d+)/(\d+), (\d+)/(\d+)\] as (\d+)/(\d+) \(~4\.37863477824e-10\) '
              r'<= \|\|rho_R-P_R\|\|_1 <= (\d+)/(\d+) ', ay2['accepted'], 'AY2 tier')
    sqrt10_lo, sqrt10_hi = Q(int(m.group(1)), int(m.group(2))), Q(int(m.group(3)), int(m.group(4)))
    L_ay2, U_ay2 = Q(int(m.group(5)), int(m.group(6))), Q(int(m.group(7)), int(m.group(8)))
    require(ay2['gate_fields']['tier_label'] == 'first_order_distance_from_product' and '(2) Two-sided tier first_order_distance_from_product' in ay2['accepted'],
            'AY2 tier label')
    m = match(r"K_2'=(\d+)/(\d+) \(~13417\.5275440\)", ay2['accepted'], "AY2 restated K_2'")
    require(Q(int(m.group(1)), int(m.group(2))) == K2p, "K_2' identical in the AY1 and AY2 gates")
    require('G(t)=16 exp(8t)(1+10t)' in am2g['accepted'], 'AM2 gate majorant')
    require('The actual reference reset bound is 56|tau||R|' in aq1g['accepted'], 'AQ1 gate reset bound')
    for frag in ('Item 2: the F1 and F2 limits coincide on every finite region',
                 'Item 3: the limit equals every AQ1 subsequential limit (F1) and every F2 subsequential limit on every finite region'):
        require(frag in bb2['accepted'], 'BB2 gate fragment ' + frag[:30])
    require(bb2['gate_fields']['whole_sequence_claimed'] is True and bb2['gate_fields']['uniqueness_of_ground_state_claimed'] is False
            and bb2['gate_fields']['common_limit_claimed'] is True, 'BB2 gate fields')
    # the premise reports whose labelled steps are used
    ay1r, av1r, aq1r, aw1r, am2r, i1r = (read_input(k) for k in (P_AY1F, P_AV1F, P_AQ1F, P_AW1F, P_AM2F, P_I1))
    require(all(('\\tag{HNM-AY1-F1%d}' % k) in ay1r for k in (1, 2, 3, 4)) and 'The bound holds uniformly in `N`, in the cutoff (`L>=24`) and in both families. It passes to the untruncated ground (AV1 F22)' in ay1r,
            'AY1 forward F11-F14 and the per-box passage')
    require('\\omega^{(2)}_N(h_R)\\le 2\\cdot7\\cdot7|\\tau|=98|\\tau|' in ay1r and 'h_b=8\\sum_{e\\in b}C_e\\ \\ge 6Q_b\\ \\ge Q_b' in ay1r, 'AY1 reset and on-site inequality')
    require('\\tag{HNM-AV1-F22}' in av1r and '\\tag{HNM-AV1-F23}' in av1r, 'AV1 cutoff-vector removal')
    require('\\operatorname{Tr}(\\rho_{N,F}h_F)\\le2M N_{F,N}\\le8M|F|=56|\\tau||F|=:C_F,' in aq1r and '\\tag{HNM-AQ1.1}' in aq1r, 'AQ1.1')
    require(all(('\\tag{HNM-AW1-F%02d}' % k) in aw1r for k in (4, 9, 10)), 'AW1 F04, F09, F10')
    require("Each free Casimir has unique Haar vacuum and gap `3alpha/4=6delta`." in i1r
            and 'T_b=\\{(4i+r,2j+s,k):0\\le r<4,\\ 0\\le s<2\\},' in i1r and '\\quad \\pi(x,y,z)=(\\lfloor x/4\\rfloor,\\lfloor y/2\\rfloor,z).' in i1r,
            'I1 blocking and free Casimir gap')
    am2_strings = ['\\qquad L_k^{\\rm num}=16\\,8^k(1+5k/4).', 'This contributes `2^p(2p)^k J product||c_j||_a`.',
                   'This contributes `2^p(2p)^k k(p+1)/p` times the same J product.', 'G(t)=\\sum_{k\\ge0}{L_k^{\\rm num}t^k\\over k!}',
                   '=16e^{8t}(1+10t),\\quad', "G'(t)=16e^{8t}(18+80t).", 'The nested commutator is zero for k>2p=8.',
                   "For R=1/64, `exp(1/8)<8/7`", 'J:=\\max_u\\sum_{X\\ni u}\\|V_X\\|\\le28|\\tau|\\le J_0={7\\over25000000}.',
                   'h_x\\Omega_x=0,\\quad h_x\\ge Q_x=I-|\\Omega_x\\rangle\\langle\\Omega_x|,']
    require(all(x in am2r for x in am2_strings), 'AM2 report counting strings')
    check('admitted_gates_and_reports_bound',
          True,
          gates={k: {'verdict': g['verdict'], 'sha256': inventory[k]} for k, g in G.items()},
          K2prime_from_AY1_gate=s(K2p), sqrt10_bracket_from_AY2_gate=[s(sqrt10_lo), s(sqrt10_hi)], AY2_tier_lower=s(L_ay2), AY2_tier_upper=s(U_ay2),
          AZ2_D8_plus_one_tenth_W1_enclosure=az2_d8_w, AW1_flip_set=FLIP_E_TEXT, AM2_strings_bound=len(am2_strings),
          premise_steps_used=['AY1 forward HNM-AY1-F11..F14 (per-box ball, reviewed step)', 'AV1 F22-F23 (untruncated ground vector)',
                              'AQ1.1 (reset)', 'AW1 F04, F09, F10 (grading, flip lemma)', 'I1.1, I1.3, I1.4 (blocking, gap 6 delta)',
                              'AM2.1-AM2.9 (counting for general p)', 'BB2 gate items 2-3 (limit of the named constructions)'])

    # ======================= verbatim copies of the admitted AZ2 algebra (textual binding) =======================
    az2_src = read_input(P_AZ2_CHECK)
    own_src = (BASE / 'check.py').read_text(encoding='utf-8')
    copied = ['def rat(', 'def s(', 'def dec(', 'def sha_bytes(', 'def sha(', 'def magnitude(', 'def sqrt_bracket(', 'def sqrt_up(', 'def out_dn(',
              'def out_up(', 'def up_sig(', 'def read_input(', 'def load_json_input(', 'def match(', 'def strip_code(', 'ZERO3 = ', 'EX, EY, EZ = ',
              'def basis(', 'def parity_class(', 'def haar_x_power(', 'def radial_moment(', 'def moment(', 'def padd(', 'def pscale(', 'def pmul(',
              'def pshift(', 'def pdeg(', 'def inner(', 'def proj_coeffs(', 'def dot(', 'def casimir_terms(', 'KINETIC_MODELS = {', 'def kinetic(',
              'def eps_free(', 'def shell_min(', 'def ldl_exact(', 'class GramSolver:', 'class Shell:', 'def sector_class(', 'def boundary_class(',
              'def thresholds(', 'DCTX = ', 'RITZ_ITERATIONS = ', 'RITZ_SCALE = ', 'def to_dec(', 'class RitzProposal:', 'WEYL_FREE_GAP = ',
              'V_NORM_PER_TAU = ', 'EXPORT_DIGITS = ', 'class PerCutoff:', 'def certify(', 'def classify_leakage(', 'def haar_mean(',
              'def solve_kinetic(', 'def rs_series(', 'def observable_series(', 'def qmul(', 'def qinv(', 'def rational_unit_quaternions(',
              'def holonomies(', 'def invariants(', 'def gauge(', 'def sig_pair(']
    differ = [h for h in copied if top_level_block(own_src, h) != top_level_block(az2_src, h)]
    check('az2_algebra_copied_verbatim',
          not differ,
          blocks_compared=len(copied), differing=differ, source=P_AZ2_CHECK, source_sha256=inventory[P_AZ2_CHECK],
          attribution='exact graph algebra of the admitted AZ2 forward checker (Round32), copied verbatim and compared block by block with the snapshot; not imported')

    # ======================= Round11 conventions, bound to the snapshot text (as in AZ2) =======================
    solver = read_input(P_R11_SOLVER)
    sreadme = read_input(P_R11_SOLVER_README)
    adv = read_input(P_R11_ADV)
    r11 = read_input(P_R11_README)
    solver_strings = [
        'return [(a,b,n-a-b) for n in range(d+1) for a in range(n+1) for b in range(n-a+1)]',
        'return sum((F(comb(c,2*k),2*k+1)*radial_moment(a+c-2*k,k)*radial_moment(b+c-2*k,k) for k in range(c//2+1)),F(0))',
        'return F(comb(2*m,m),4**m*(m+1))',
        "(3*(3+r)/4 if i<2 else F(9,2))", "(-(3+r)/4 if i<2 else F(-3,2))",
        'out=add(out,mul(add(Z,mul(X,Y),-1),deriv(deriv(p,0),1)),-r/2)',
        'out=add(out,mul(add(Y,mul(X,Z),-1),deriv(deriv(p,0),2)),F(-3,2))',
        'out=add(out,mul(add(X,mul(Y,Z),-1),deriv(deriv(p,1),2)),F(-3,2))',
        'return 3*j*(j+1)+3*s*(s+1)+r*ell*(ell+1)',
        'if r==1: return a*(F(5,8)*d*d+2*d+F(3,8)*(d%2))',
        '# W=-lambda1*x-lambda2*y. Constants have no P-Q coupling.',
        'import numpy as np', 'from scipy.linalg import eigh',
    ]
    missing = [x for x in solver_strings if x not in solver]
    require(not missing, 'Round11 solver snapshot lacks: ' + repr(missing[:2]))
    require('E[x²]=E[y²]=E[z²]=1/4 and E[xyz]=1/16' in sreadme and 'For ρ=1 this gives Kx=3x, Ky=3y, Kz=9z/2 and K(xy)=13xy/2−z/2' in sreadme
            and '`H = α Kρ + λ1(1−x) + λ2(1−y)`' in sreadme and "`τ/α = 5d²/8 + 2d + 3(d mod 2)/8`" in sreadme, 'Round11 solver README fixtures')
    require('K1=0,\\quad Kx=3x,\\quad Ky=3y,\\quad Kz=\\tfrac92z,' in adv and 'K(xy)=\\tfrac{13}2xy-\\tfrac12z.' in adv
            and 'm_d=\\tfrac58d^2+2d+\\tfrac38(d\\bmod2),\\qquad d\\ge0.' in adv and 'Q_D K Q_D\\ge m_{D+1}Q_D,' in adv
            and 'B=A-\\frac{CC^*}{\\tau-R}.' in adv and '\\epsilon_{abc}=3j(j+1)+3k(k+1)+\\ell(\\ell+1),' in adv
            and 'D_s^a=L_U^a-R_V^a.' in adv, 'Round11 advisor equations K1, K5, E2, E3, E4, T5')
    require('U=v_Mh_3^{-1}v_L^{-1}h_1,' in adv and 'V=h_2v_Rh_4^{-1}v_M^{-1}.' in adv, 'Round11 loop paths G2')
    require('The physical Hilbert space is L² of' in sreadme and 'For rho=1, alpha>0 and finite lambda1,lambda2>=0' in r11, 'Round11 scope')
    X1, Y1, Z1 = {EX: Q(1)}, {EY: Q(1)}, {EZ: Q(1)}

    def validate_k5(model):
        require(kinetic({ZERO3: Q(1)}, model) == {}, 'K1=0')
        require(kinetic(X1, model) == {EX: Q(3)} and kinetic(Y1, model) == {EY: Q(3)}, 'Kx=3x, Ky=3y (seven links, shared Casimir included)')
        require(kinetic(Z1, model) == {EZ: Q(9, 2)}, 'Kz=9z/2')
        require(kinetic({(1, 1, 0): Q(1)}, model) == {(1, 1, 0): Q(13, 2), EZ: Q(-1, 2)}, 'K(xy)=13xy/2-z/2 (shared-link cross term)')
        return True
    diag_ok = all(kinetic({m_: Q(1)}).get(m_, Q(0)) == eps_free(*m_) and all(sum(k) < sum(m_) for k in kinetic({m_: Q(1)}) if k != m_) for m_ in basis(9))
    b4 = basis(4)
    sym_ok = all(inner({p: Q(1)}, kinetic({q: Q(1)})) == inner(kinetic({p: Q(1)}), {q: Q(1)}) for p in b4 for q in b4)
    parity_ok = all(moment(a_, b_, cc) == 0 for (a_, b_, cc) in basis(12) if (a_ + cc) % 2 or (b_ + cc) % 2)
    # the shared-link Casimir S: leading eigenvalue ell(ell+1), ell=(a+b)/2; S z = 0 (z does not depend on vM); symmetric
    s_diag_ok = all(apply_casimir({m_: Q(1)}, 'S').get(m_, Q(0)) == Q(m_[0] + m_[1], 2) * (Q(m_[0] + m_[1], 2) + 1) for m_ in basis(9))
    s_sym_ok = all(inner({p: Q(1)}, apply_casimir({q: Q(1)}, 'S')) == inner(apply_casimir({p: Q(1)}, 'S'), {q: Q(1)}) for p in b4 for q in b4)
    s_fix = {'S1': apply_casimir({ZERO3: Q(1)}, 'S'), 'Sx': apply_casimir(X1, 'S'), 'Sy': apply_casimir(Y1, 'S'), 'Sz': apply_casimir(Z1, 'S'),
             'Sxy': apply_casimir({(1, 1, 0): Q(1)}, 'S')}
    s_ok = (s_diag_ok and s_sym_ok and s_fix['S1'] == {} and s_fix['Sx'] == {EX: Q(3, 4)} and s_fix['Sy'] == {EY: Q(3, 4)} and s_fix['Sz'] == {}
            and s_fix['Sxy'] == {(1, 1, 0): Q(2), EZ: Q(-1, 2)})
    decomposition_ok = all(padd(kinetic({m_: Q(1)}), padd(padd(pscale(apply_casimir({m_: Q(1)}, 'U'), Q(3)), pscale(apply_casimir({m_: Q(1)}, 'V'), Q(3))),
                                                            apply_casimir({m_: Q(1)}, 'S')), -1) == {} for m_ in basis(6))
    check('round11_conventions_bound',
          validate_k5('R11_rho1') and diag_ok and sym_ok and parity_ok and s_ok and decomposition_ok
          and moment(2, 0, 0) == moment(0, 2, 0) == moment(0, 0, 2) == Q(1, 4) and moment(1, 1, 1) == Q(1, 16) and moment(1, 0, 0) == 0
          and all(comb(D + 3, 3) == len(basis(D)) for D in V['cutoffs'])
          and WEYL_FREE_GAP == shell_min(1) == min(eps_free(*m_) for m_ in basis(1) if sum(m_) == 1)
          and V_NORM_PER_TAU == invariants({e_: (Q(1), Q(0), Q(0), Q(0)) for e_ in LINKS})[0] + invariants({e_: (Q(1), Q(0), Q(0), Q(0)) for e_ in LINKS})[1]
          and Z_NORM == invariants({e_: (Q(1), Q(0), Q(0), Q(0)) for e_ in LINKS})[2],
          free_gap_E1_of_K=s(WEYL_FREE_GAP), solver_snapshot_sha256=inventory[P_R11_SOLVER], solver_strings_bound=len(solver_strings),
          shared_link_casimir={'operator': "C_shared = S (the vM Casimir, derivative L_U - R_V; Round11 K1)", 'leading_eigenvalue': 'ell(ell+1), ell=(a+b)/2',
                               'fixtures': {k: {str(list(m_)): s(x) for m_, x in p.items()} for k, p in s_fix.items()}},
          decomposition='K = 3 C_U + 3 C_V + C_shared checked on every monomial of degree <= 6',
          dimensions={str(D): len(basis(D)) for D in V['cutoffs']},
          not_imported='the Round11 solver (numpy/scipy) is never imported; its conventions are bound by the strings above')

    # ======================= gauge invariance and the three one-link centre flips (exact quaternion fixture) =======================
    qs = rational_unit_quaternions(60)
    links = {e: qs[i] for i, e in enumerate(LINKS)}
    inv_ok = True
    for trial in range(4):
        g = {vx: qs[7 + 6 * trial + i] for i, vx in enumerate(VERTICES)}
        inv_ok = inv_ok and invariants(gauge(links, g)) == invariants(links)
    x0, y0, z0 = invariants(links)
    FLIP_SIGNS = {}
    for e in LINKS:
        fl = dict(links)
        fl[e] = tuple(-t for t in links[e])
        xf, yf, zf = invariants(fl)
        FLIP_SIGNS[e] = tuple(Q(1) if new == old else Q(-1) for new, old in ((xf, x0), (yf, y0), (zf, z0)))
        require(all(new == sg * old for new, old, sg in zip((xf, yf, zf), (x0, y0, z0), FLIP_SIGNS[e])), 'flip acts by signs')
    require(x0 != 0 and y0 != 0 and z0 != 0, 'fixture must separate the signs')
    flips_ok = (all(FLIP_SIGNS[e] == (-1, 1, -1) for e in FACE1_NONSHARED) and all(FLIP_SIGNS[e] == (1, -1, -1) for e in FACE2_NONSHARED)
                and FLIP_SIGNS[SHARED] == (-1, -1, 1))
    F1S, F2S, FMS = FLIP_SIGNS['h1'], FLIP_SIGNS['h2'], FLIP_SIGNS[SHARED]
    # each flip commutes with K and with C_shared (centre elements commute with all translations), and preserves the Haar measure
    commute_ok = all(flip_poly(kinetic({m_: Q(1)}), sg) == kinetic(flip_poly({m_: Q(1)}, sg)) and
                     flip_poly(apply_casimir({m_: Q(1)}, 'S'), sg) == apply_casimir(flip_poly({m_: Q(1)}, sg), 'S')
                     for m_ in basis(8) for sg in (F1S, F2S, FMS))
    haar_ok = all(moment(*m_) == moment(*m_) * sg[0] ** m_[0] * sg[1] ** m_[1] * sg[2] ** m_[2] for m_ in basis(12) for sg in (F1S, F2S, FMS))
    gauge_reason = ('every basis element is a polynomial in the traces x,y,z of closed holonomies, invariant under all six vertex SU(2) '
                    'actions (all six Gauss constraints solved by the Round11 tree reduction Q1-Q3); H commutes with the gauge action, '
                    'so v, Hv and the complete residual lie in the gauge-invariant subspace and (I-P_phys) v = 0 exactly')
    check('gauge_invariance_and_one_link_flips',
          inv_ok and flips_ok and commute_ok and haar_ok,
          link_quaternions={e: [s(x) for x in links[e]] for e in LINKS}, invariants=[s(x0), s(y0), s(z0)],
          flip_signs_on_xyz={e: [s(x) for x in FLIP_SIGNS[e]] for e in LINKS},
          reading={'face-1 non-shared link (h1, vL or h3)': '(x,y,z) -> (-x, y, -z): H(l1,l2) -> H(-l1,l2)',
                   'face-2 non-shared link (h2, vR or h4)': '(x,y,z) -> (x, -y, -z): H(l1,l2) -> H(l1,-l2)',
                   'shared link vM': '(x,y,z) -> (-x, -y, z): H(l1,l2) -> H(-l1,-l2) (proves only the joint statement)'},
          commutation='each flip commutes with K and C_shared on every monomial of degree <= 8 and preserves every Haar moment through degree 12',
          ledger_item_c={'value': '0', 'reason': gauge_reason})

    # ======================= item 1: bivariate Rayleigh-Schroedinger tables at D=6 and D=8 =======================
    order = V['order']
    tables = {}
    for D in V['cutoffs']:
        psi, En = rs2_series(order + 1, D)
        tables[D] = {'psi': psi, 'E': En}
        for name in ('W_1', 'W_2', 'z', 'C_shared'):
            tables[D][name] = obs2(psi, OBSERVABLES[name], order)
    T6, T8 = tables[6], tables[8]
    same = all(T6[k] == T8[k] for k in ('W_1', 'W_2', 'z', 'C_shared', 'E')) and T6['psi'] == T8['psi']
    w1t, zt, cst, Et = T8['W_1'], T8['z'], T8['C_shared'], T8['E']
    keys = table_keys(order)
    # Hellmann-Feynman: <W_1> = -dE/dl1, <W_2> = -dE/dl2; exchange symmetry <W_2>_(m,n) = <W_1>_(n,m)
    hf_ok = all(w1t[(m_, n_)] == -(m_ + 1) * Et[(m_ + 1, n_)] and T8['W_2'][(m_, n_)] == -(n_ + 1) * Et[(m_, n_ + 1)] for (m_, n_) in keys)
    exch_ok = all(T8['W_2'][(m_, n_)] == w1t[(n_, m_)] and zt[(m_, n_)] == zt[(n_, m_)] and cst[(m_, n_)] == cst[(n_, m_)] for (m_, n_) in keys)
    # second route for the second-order C_shared coefficients: E_20(rho) = -1/(3(3+rho)) from the rho-weighted kinetic operators
    # (x is an exact eigenvector of the rho-weighted K with eigenvalue 3(3+rho)/4, so E_20(rho) = -E[x^2]/(3(3+rho)/4) exactly)
    lam1, lam2 = kinetic(X1, 'R11_rho1'), kinetic(X1, 'anisotropic_rho2')
    e20_rho1, e20_rho2 = -moment(2, 0, 0) / lam1[EX], -moment(2, 0, 0) / lam2[EX]
    rho_route = (lam1 == {EX: Q(3)} and lam2 == {EX: Q(15, 4)} and e20_rho1 == Q(-1, 12) == Et[(2, 0)] and e20_rho2 == Q(-1, 15)
                 and cst[(2, 0)] == Q(1, 3 * (3 + 1) ** 2))    # d/drho [-1/(3(3+rho))] at rho=1 = 1/48
    # diagonal l1=l2 sums reproduce the admitted AZ2 series (equal-coupling model), a consistency check only
    diag_w1, diag_z, diag_cs, diag_E = diagonal(w1t, order), diagonal(zt, order), diagonal(cst, order), diagonal(Et, order + 1)
    az2_consistent = (diag_w1 == [Q(0), Q(1, 6), Q(0), Q(-187, 33696), Q(0)] and diag_z == [Q(0), Q(0), Q(7, 216), Q(0), Q(-349, 151632)]
                      and diag_E[:5] == [Q(0), Q(0), Q(-1, 6), Q(0), Q(187, 67392)])
    one_face = obs2(rs2_series(order, 6, couple=(True, False))[0], OBSERVABLES['W_1'], order)
    one_face_ok = one_face[(3, 0)] == Q(-5, 864) == w1t[(3, 0)] and w1t[(1, 2)] == Q(1, 4212)
    zero_trunc = all(pdeg(T8['psi'][k]) <= sum(k) for k in T8['psi'])
    check('rs2_tables_exact',
          same and hf_ok and exch_ok and rho_route and az2_consistent and one_face_ok and zero_trunc,
          W_1=tab_str(w1t), z=tab_str(zt), C_shared=tab_str(cst), E_0=tab_str(Et), W_2=tab_str(T8['W_2']),
          nonzero={'W_1': {k: v for k, v in tab_str(w1t).items() if v != '0'}, 'z': {k: v for k, v in tab_str(zt).items() if v != '0'},
                   'C_shared': {k: v for k, v in tab_str(cst).items() if v != '0'}},
          psi={'1,0': {str(list(m_)): s(x) for m_, x in T8['psi'][(1, 0)].items()}, '0,1': {str(list(m_)): s(x) for m_, x in T8['psi'][(0, 1)].items()},
               '1,1': {str(list(m_)): s(x) for m_, x in T8['psi'][(1, 1)].items()}},
          identical_at_cutoffs=V['cutoffs'], total_order=order,
          diagonal_l1_eq_l2={'W_1': [s(x) for x in diag_w1], 'z': [s(x) for x in diag_z], 'C_shared': [s(x) for x in diag_cs], 'E_0': [s(x) for x in diag_E]},
          second_order_at_l1_eq_l2={'z': s(diag_z[2]), 'C_shared': s(diag_cs[2])},
          hellmann_feynman='<W_1>_(m,n) = -(m+1) E_(m+1,n) and <W_2>_(m,n) = -(n+1) E_(m,n+1) for every m+n <= 4',
          c_shared_second_route='E_20(rho) = -1/(3(3+rho)) at rho=1,2 (rho-weighted K); d/drho at rho=1 gives 1/48 = <C_shared>_(2,0)',
          consistency_with_admitted_AZ2='the l1=l2 diagonal sums equal the AZ2-admitted equal-coupling series (1/6, -187/33696; 7/216, -349/151632; -1/6, 187/67392): a consistency check, not a transfer',
          one_face_and_second_square='c_(3,0) of <W_1> = -5/864 is the one-face coefficient (the l2=0 section) and c_(1,2) = 1/4212 is the second-square term, matching the AZ2 skeptic record')

    # ---- control exact_rs_zero_truncation ----
    RS_PROVENANCE = 'exact Rayleigh-Schroedinger (polynomial resolvent, zero omitted residual)'

    def validate_rs(tab6, tab8, provenance, psi8):
        require(provenance == RS_PROVENANCE, 'graph coefficients come from exact perturbation theory, never a fit')
        require(tab6 == tab8, 'a coefficient differs between the cutoffs D=6 and D=8')
        require(all(pdeg(p) <= sum(k) <= max(V['cutoffs']) for k, p in psi8.items()), 'psi_mn must lie in P_(m+n): zero truncation')
        return True
    grid_pts_plus = [g_ for g_ in V['grid']]
    bad8 = dict(zt)
    bad8[(1, 1)] = zt[(1, 1)] + Q(1, 10 ** 12)
    check('exact_rs_zero_truncation',
          validate_rs(T6['z'], T8['z'], RS_PROVENANCE, T8['psi']) and validate_rs(T6['W_1'], T8['W_1'], RS_PROVENANCE, T8['psi'])
          and validate_rs(T6['C_shared'], T8['C_shared'], RS_PROVENANCE, T8['psi'])
          and rejected(lambda: validate_rs(T6['z'], bad8, RS_PROVENANCE, T8['psi']), 'coefficient_differs_between_cutoffs')
          and rejected(lambda: validate_rs(T6['z'], T8['z'], 'least-squares fit to the grid Ritz values', T8['psi']), 'fitted_coefficient_provenance')
          and rejected(lambda: validate_rs(T6['z'], T8['z'], RS_PROVENANCE, {**T8['psi'], (1, 0): {(3, 0, 0): Q(1)}}), 'psi_outside_P_(m+n)'),
          truncation_error='0: every psi_mn (m+n <= 5) lies in P_(m+n) inside P_6, and K psi_mn = rhs_mn holds as a polynomial identity (full-space resolvent)',
          provenance=RS_PROVENANCE, cutoffs=V['cutoffs'])

    # ---- control independent_coupling_flip (parities checked on the full two-variable table) ----
    PARITY_RULES = {'W_1': (1, 0), 'z': (1, 1), 'C_shared': (0, 0)}      # (parity in l1, parity in l2): 1 = odd, 0 = even

    def parity_table_ok(tab, rule):
        return all(val == 0 for (m_, n_), val in tab.items() if (m_ % 2, n_ % 2) != rule)
    vec_parity_ok = all(flip_poly(T8['psi'][(m_, n_)], F1S) == pscale(T8['psi'][(m_, n_)], Q((-1) ** m_)) and
                        flip_poly(T8['psi'][(m_, n_)], F2S) == pscale(T8['psi'][(m_, n_)], Q((-1) ** n_)) for (m_, n_) in T8['psi'])
    CLAIM = {'l1': {'flip_link': 'h1', 'face': 1}, 'l2': {'flip_link': 'h2', 'face': 2}, 'checked_on': 'full (m,n) table'}

    def validate_parity_claim(cl):
        require(cl['checked_on'] == 'full (m,n) table', 'parities must be checked on the full two-variable table, not only at l1=l2')
        require(cl['l1']['flip_link'] in FACE1_NONSHARED and FLIP_SIGNS[cl['l1']['flip_link']][:2] == (-1, 1),
                'the l1 parity needs the flip of a non-shared link of face 1 (reverses W_1 and z, fixes W_2)')
        require(cl['l2']['flip_link'] in FACE2_NONSHARED and FLIP_SIGNS[cl['l2']['flip_link']][:2] == (1, -1),
                'the l2 parity needs the flip of a non-shared link of face 2 (reverses W_2 and z, fixes W_1)')
        for name, rule in PARITY_RULES.items():
            require(parity_table_ok(T8[name], rule), 'parity of ' + name + ' fails on the table')
        return True
    diag_only = all(diagonal(w1t, order)[o] == 0 for o in (0, 2, 4))
    check('independent_coupling_flip',
          validate_parity_claim(CLAIM) and vec_parity_ok and diag_only and all(parity_table_ok(T8[n_], r_) for n_, r_ in PARITY_RULES.items())
          and rejected(lambda: validate_parity_claim({'l1': {'flip_link': 'vM', 'face': 1}, 'l2': {'flip_link': 'vM', 'face': 2}, 'checked_on': 'full (m,n) table'}),
                       'two_variable_parity_from_the_single_shared_link_flip')
          and rejected(lambda: validate_parity_claim(dict(CLAIM, checked_on='diagonal l1=l2 only')), 'parity_checked_at_l1_eq_l2_only')
          and rejected(lambda: validate_parity_claim(dict(CLAIM, l1={'flip_link': 'h2', 'face': 2})), 'l1_parity_from_a_face_2_link')
          and rejected(lambda: validate_parity_claim(dict(CLAIM, l2={'flip_link': 'vL', 'face': 1})), 'l2_parity_from_a_face_1_link'),
          proof={'<W_1>': 'odd in l1 (F_h1: psi(-l1,l2) = F_h1 psi(l1,l2), F_h1 x F_h1 = -x), even in l2 (F_h2 fixes x)',
                 '<z>': 'odd in l1 and odd in l2 (both flips reverse z)', '<C_shared>': 'even in each (C_shared commutes with every centre flip)'},
          vector_level='F_h1 psi_mn = (-1)^m psi_mn and F_h2 psi_mn = (-1)^n psi_mn for every m+n <= 5 (exact)',
          parity_rules={k: ['odd' if r_[0] else 'even', 'odd' if r_[1] else 'even'] for k, r_ in PARITY_RULES.items()},
          consequence='every even-order coefficient of <W_1> at l1=l2 vanishes (orders 0, 2, 4 checked)')

    # ======================= item 2: certificates of <z> on the AZ2 grid at l1=l2, both cutoffs =======================
    pcs = {D: PerCutoff(D, shell_min(D + 1)) for D in V['cutoffs']}
    check('shell_sectors_orthogonal',
          all(pc.shell_next.offdiag_nonzero == 0 and pc.shell_top.offdiag_nonzero == 0 for pc in pcs.values())
          and all(len(pc.shell_next.sectors) == (D + 2) * (D + 3) // 2 and pc.tail_lower == shell_min(D + 1) for D, pc in pcs.items())
          and [pcs[D].tail_lower for D in V['cutoffs']] == [Q(45), Q(69)],
          shells={str(D): {'first_omitted_shell_degree': D + 1, 'sectors': len(pc.shell_next.sectors), 'pairs_checked': pc.shell_next.pairs_checked,
                           'top_sectors': len(pc.shell_top.sectors), 'gram_parity_blocks': [len(b) for b in pc.gs.blocks]} for D, pc in pcs.items()},
          tail_lower={str(D): s(pcs[D].tail_lower) for D in V['cutoffs']})
    taus = [Q(0)] + [sg * g_ for g_ in V['grid'] for sg in (1, -1)]
    certs = {}
    for D in V['cutoffs']:
        for tau in taus:
            certs[(D, tau)] = certify_z(pcs[D], tau)
    grid_pts = [(D, tau) for D in V['cutoffs'] for tau in taus if tau != 0]
    ident_ok = True
    for k, ct in certs.items():
        ident_ok = ident_ok and ct['rho2'] == ct['rhoP2'] + ct['rhoQ2'] and ct['PQ'] == ct['QX'] + ct['QY'] + 2 * ct['QXY']
        ident_ok = ident_ok and sum(ct['sec_w'], Q(0)) == ct['PQ'] and ct['wR_y'] == ct['wR']
    z_sign_ok = all(certs[k]['z_lo_out'] > 0 for k in grid_pts)
    flipsign = lambda m_: -1 if (m_[0] + m_[1]) % 2 else 1     # noqa: E731  shared-link flip (x,y,z)->(-x,-y,z)
    mirror_ok = True
    for D in V['cutoffs']:
        for g_ in V['grid']:
            cp, cm = certs[(D, g_)], certs[(D, -g_)]
            mirror_ok = mirror_ok and cm['w'] == [flipsign(m_) * x for m_, x in zip(pcs[D].bs, cp['w'])]
            mirror_ok = mirror_ok and cm['zR'] == cp['zR'] and cm['z_lo_out'] == cp['z_lo_out'] and cm['z_hi_out'] == cp['z_hi_out']
    nest_ok = all(certs[(6, t)]['z_lo_out'] <= certs[(8, t)]['z_lo_out'] and certs[(8, t)]['z_hi_out'] <= certs[(6, t)]['z_hi_out'] for t in taus)
    free_ok = all(certs[(D, Q(0))]['z_lo_out'] == 0 == certs[(D, Q(0))]['z_hi_out'] and certs[(D, Q(0))]['zR'] == 0 for D in V['cutoffs'])
    rels = {k: rel_width(certs[k]['z_lo_out'], certs[k]['z_hi_out']) for k in grid_pts}
    rel8 = {k: r_ for k, r_ in rels.items() if k[0] == 8}
    worst8 = max(rel8.values())
    width_met = all(r_ <= V['target'] for r_ in rel8.values())
    az2_reproduced = [s(certs[(8, Q(1, 10))]['lo_out']), s(certs[(8, Q(1, 10))]['hi_out'])] == az2_d8_w
    check('z_certificates_complete',
          ident_ok and z_sign_ok and mirror_ok and nest_ok and free_ok and az2_reproduced,
          points=len(certs), grid_points=len(grid_pts), observable='<z> = <psi_0,(1/2)Tr(UV)psi_0>, the 1x2 loop (outer boundary of both squares)',
          observable_norm='||z|| = 1 (Tr(UV)/2 at the identity configuration); sigma_z = ||(z-<z>)psi_0|| <= 1',
          lemma='|<v,zv>/<v,v> - <psi_0,zpsi_0>| <= 2 s sigma_z + 2 s^2 ||z|| with s = min(Davis-Kahan, Eckart) (AZ2 Lemmas 3-6)',
          sign='every enclosure lies in (0, infinity): <z> > 0 at every grid point, both signs of l1=l2 (z is even under the shared-link flip)',
          cutoff_nesting='the D=8 enclosure lies inside the D=6 enclosure at every point (observed consistency check)',
          mirror='the -l certificate is computed separately and equals the shared-link flip image of the +l certificate exactly',
          free_reference={str(D): [s(certs[(D, Q(0))]['z_lo_out']), s(certs[(D, Q(0))]['z_hi_out'])] for D in V['cutoffs']},
          az2_W1_enclosure_reproduced_D8_plus_one_tenth=az2_reproduced,
          relative_width_preview={point_key(*k): dec(r_, 6) for k, r_ in rels.items()},
          enclosures={point_key(*k): [s(certs[k]['z_lo_out']), s(certs[k]['z_hi_out'])] for k in grid_pts},
          enclosures_preview={point_key(*k): [dec(certs[k]['z_lo_out'], 25), dec(certs[k]['z_hi_out'], 25)] for k in grid_pts},
          half_width_preview={point_key(*k): dec(certs[k]['delta_z'], 4) for k in grid_pts},
          sin_theta_used_preview={point_key(*k): dec(certs[k]['s_used'], 4) for k in grid_pts})

    # ---- the five-part ledger at every point (AZ2 type) ----
    for k, ct in certs.items():
        if 'T_link' in ct:
            for cls, rec in ct['T_link'].items():
                rec['used'] = min(rec['bound'], ct['T_joint'])
    records = {}
    for (D, tau), ct in sorted(certs.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        pc = pcs[D]
        per, prod, cor = classify_leakage(ct, pc)
        tau2 = tau * tau
        per_link = {}
        for link in LINKS:
            cls = LINK_CLASS[link]
            per_link[link] = {
                'class': {'j': 'left three-link path h1-vL-h3 (spin j=(a+c)/2)', 'k': 'right three-link path h2-vR-h4 (spin k=(b+c)/2)',
                          'ell': 'shared link vM (spin ell=(a+b)/2)'}[cls],
                'retained_max_spin': s(Q(D, 2)), 'threshold_free_energy': s(pc.thr[cls][0]), 'threshold_sector_abc': list(pc.thr[cls][1]),
                'ritz_leakage_weight_upper': s(up_sig(per[cls])), 'boundary_layer_weight_upper': s(up_sig(ct['T_link'][cls]['boundary_layer_weight'])),
                'faces_touching_link': ct['T_link'][cls]['faces_touching'],
                'certified_tail_upper': s(up_sig(ct['T_link'][cls]['used'])), 'certified_tail_preview': dec(ct['T_link'][cls]['used'], 4)}
        joint = {
            'complete_omitted_residual_squared_upper': s(up_sig(ct['rhoQ2'])), 'complete_omitted_residual_preview': dec(ct['rhoQ2'], 6),
            'x_channel_squared_upper': s(up_sig(tau2 * ct['QX'])), 'y_channel_squared_upper': s(up_sig(tau2 * ct['QY'])),
            'interference_2XY_bracket': [s(val) for val in sig_pair(2 * tau2 * ct['QXY'])],
            'product_channel_weight_upper': s(up_sig(prod)), 'product_channel_preview': dec(prod, 6),
            'product_channel_threshold': s(pc.thr['product'][0]),
            'per_link_class_weights_upper': {k2: s(up_sig(val)) for k2, val in per.items()},
            'corner_overlaps_upper': {k2: s(up_sig(val)) for k2, val in sorted(cor.items())},
            'sectors': len(ct['sec_w']), 'joint_threshold_tail_lower': s(pc.tail_lower), 'interacting_tail_threshold': s(ct['tail_t']),
            'certified_joint_tail_upper': s(up_sig(ct['T_joint'])),
            'identity': 'rho_Q^2 = sum of all shell-(D+1) sector weights = (j + k + ell per-link classes) + product channel - corner overlaps (exact)'}
        rec = {
            'D': D, 'l1_eq_l2': s(tau), 'dimension': len(pc.bs), 'model': 'FG(round11_two_plaquette_independent_couplings) at l1=l2',
            'z_ritz_preview': dec(ct['zR'], 25), 'z_enclosure': [s(ct['z_lo_out']), s(ct['z_hi_out'])],
            'z_enclosure_preview': [dec(ct['z_lo_out'], 25), dec(ct['z_hi_out'], 25)],
            'z_half_width_upper': s(up_sig(ct['delta_z'])), 'z_half_width_preview': dec(ct['delta_z'], 4),
            'z_sign_certified': (ct['z_lo_out'] > 0) if tau != 0 else None,
            'free_reference_inside_enclosure': ct['z_lo_out'] <= 0 <= ct['z_hi_out'],
            'relative_width_upper': s(up_sig(rels[(D, tau)])) if tau != 0 else None,
            'relative_width_preview': dec(rels[(D, tau)], 6) if tau != 0 else None,
            'W1_enclosure_same_certificate': [s(ct['lo_out']), s(ct['hi_out'])],
            'energy_enclosure': [s(ct['E0_lo_out']), s(ct['E0_hi_out'])],
            'gap_lower_E1_minus_E0': s(out_dn(ct['gap_lower_b'] - ct['mu'], EXPORT_DIGITS)),
            'ledger': {
                'a_per_link_representation_tail': per_link,
                'b_joint_product_channel': joint,
                'c_gauge_invariant_projection': {'value': '0', 'status': 'exactly_zero', 'reason': gauge_reason},
                'd_ritz_eigenvector_residual': {
                    'retained_ritz_residual_squared_upper': s(up_sig(ct['rhoP2'])), 'complete_residual_squared_upper': s(up_sig(ct['rho2'])),
                    'certified_gap_E1_lower': s(ct['gap_lower_b']),
                    'sin_theta_davis_kahan_complete_residual_upper': s(up_sig(ct['s_A'])),
                    'sin_theta_eckart_tail_comparison_upper': s(up_sig(ct['s_B'])),
                    'sin_theta_used_upper': s(up_sig(ct['s_used'])), 'sin_theta_used_preview': dec(ct['s_used'], 4),
                    'observable_step': '2 s sigma_z + 2 s^2 ||z||, sigma_z <= ||z|| = 1'},
                'e_arithmetic': {'directed_sqrt_width_upper': s(up_sig(ct['arith_sqrt_width'])),
                                 'export_rounding_width_upper': s(up_sig((ct['z_lo'] - ct['z_lo_out']) + (ct['z_hi_out'] - ct['z_hi']))),
                                 'status': 'charged: square roots rounded upward with integer isqrt; exported ends rounded outward to 10^-%d' % EXPORT_DIGITS,
                                 'decimal_proposal': 'the 110-digit Ritz proposal is not an admission value; its rounding is measured exactly in item d'}},
        }
        records[point_key(D, tau)] = rec
    LEDGER_KEYS = ('a_per_link_representation_tail', 'b_joint_product_channel', 'c_gauge_invariant_projection',
                   'd_ritz_eigenvector_residual', 'e_arithmetic')

    def validate_ledger(ld):
        for key in LEDGER_KEYS:
            require(key in ld, 'ledger item missing: ' + key)
        require(set(ld['a_per_link_representation_tail']) == set(LINKS), 'seven per-link rows required')
        require('product_channel_weight_upper' in ld['b_joint_product_channel'] and 'interference_2XY_bracket' in ld['b_joint_product_channel'],
                'joint product channel must be itemized')
        require(ld['c_gauge_invariant_projection'].get('reason'), 'a zero entry needs a stated reason')
        require('observable_step' in ld['d_ritz_eigenvector_residual'], 'the observable step of the enclosure is part of item d')
        return True

    def validate_enclosure_record(rec):
        require('ledger' in rec, 'an enclosure without the itemized residual is rejected')
        return validate_ledger(rec['ledger'])
    L0 = records['D8_l+1/10']

    def lmut(drop=None, **kw):
        r2 = json.loads(json.dumps(L0))
        if drop:
            r2['ledger'].pop(drop)
        for k1, v1 in kw.items():
            r2['ledger'][k1] = v1
        return lambda: validate_enclosure_record(r2)
    check('enclosure_itemized_residual',
          all(validate_enclosure_record(r_) for r_ in records.values())
          and rejected(lambda: validate_enclosure_record({k1: v1 for k1, v1 in L0.items() if k1 != 'ledger'}), 'enclosure_without_ledger')
          and rejected(lmut(drop='b_joint_product_channel'), 'joint_channel_not_itemized')
          and rejected(lmut(a_per_link_representation_tail={k1: v1 for k1, v1 in L0['ledger']['a_per_link_representation_tail'].items() if k1 != 'vM'}),
                       'shared_link_row_removed')
          and rejected(lmut(c_gauge_invariant_projection={'value': '0', 'status': 'not_applicable'}), 'gauge_entry_without_reason')
          and rejected(lmut(drop='e_arithmetic'), 'arithmetic_item_missing'),
          ledger_items=list(LEDGER_KEYS), points=len(records),
          reading='per-link rows (seven links), joint product channel with corner overlaps and the 2XY interference, gauge projection 0 with its reason, '
                  'Ritz residual with Davis-Kahan and Eckart angles and the Weyl gap 3-2|l|, directed arithmetic')

    target_rows = {point_key(*k): {'relative_width_upper': s(up_sig(r_)), 'preview': dec(r_, 6), 'meets_target': r_ <= V['target']} for k, r_ in rel8.items()}
    check('target_relative_width_D8',
          width_met,
          target=s(V['target']), comparator=V['target_comparator'], rows=target_rows, worst=dec(worst8, 8), margin=dec(V['target'] / worst8, 6),
          dominating_point='D8_l+1/10 (and its mirror): the Eckart angle s is largest where |l| is largest while <z> ~ (7/216) l^2',
          d6_widths_reported_not_targeted={point_key(*k): dec(r_, 6) for k, r_ in rels.items() if k[0] == 6})


    # ======================= item 3: the Z^3 1x2 Wilson loop (fine lattice geometry from I1.1-I1.4) =======================
    R_SET = frozenset({(0, 0, 0), (0, 0, 1)})
    faces = window_faces()
    omitted = [f for f in faces if not is_selected(f)]
    meet = [f for f in omitted if face_owners(f) & R_SET]
    inside = [f for f in omitted if face_owners(f) == R_SET]
    containing = [f for f in omitted if R_SET <= face_owners(f)]
    per_anchor = [f for f in omitted if coarse(f[0]) == (0, 0, 0)]
    per_factor = [f for f in omitted if (0, 0, 0) in face_owners(f)]
    R_LINKS = [((x, y, z), d) for x in range(4) for y in range(2) for z in range(2) for d in 'xyz']
    F1 = ((0, 0, 0), 'x', 'z')     # the original xz face W: fine origin, r=0, s=0
    F2 = ((1, 0, 0), 'x', 'z')     # the xz face at the fine point e_x: r=1, s=0
    RECT = [((0, 0, 0), 'x'), ((1, 0, 0), 'x'), ((2, 0, 0), 'z'), ((1, 0, 1), 'x'), ((0, 0, 1), 'x'), ((0, 0, 0), 'z')]
    cov = link_counter([face_links(F1), face_links(F2)])
    rect_from_faces = sorted(l for l, n_ in cov.items() if n_ % 2)
    shared_link = [l for l, n_ in cov.items() if n_ == 2]
    geom = {'faces_meeting_R': len(meet), 'faces_inside_R': len(inside), 'faces_containing_R': len(containing),
            'straddling_meeting_R': len(meet) - len(inside), 'omitted_per_anchor': len(per_anchor), 'faces_per_factor': len(per_factor),
            'faces_per_site_of_R_without_the_other_site': len(per_factor) - len(containing), 'R_links': len(R_LINKS)}
    geom_ok = (geom == {'faces_meeting_R': 82, 'faces_inside_R': 10, 'faces_containing_R': 16, 'straddling_meeting_R': 72, 'omitted_per_anchor': 21,
                        'faces_per_factor': 49, 'faces_per_site_of_R_without_the_other_site': 33, 'R_links': V['band_links']}
               and all(coarse(l[0]) in R_SET for l in R_LINKS) and len(R_LINKS) == 48)
    rect_ok = (rect_from_faces == sorted(RECT) and len(RECT) == 6 and shared_link == [((1, 0, 0), 'z')]
               and all(coarse(l[0]) in R_SET for l in RECT) and F1 in inside and F2 in inside
               and (F1[0][0] % 4, F1[0][1] % 2) == (0, 0) and (F2[0][0] % 4, F2[0][1] % 2) == (1, 0))

    # exact quaternion fixture: the fine traces equal the Round11 invariants x, y, z of the same seven links
    def fine_hol(qmap, path):
        h = (Q(1), Q(0), Q(0), Q(0))
        for l, sgn in path:
            h = qmul(h, qmap[l] if sgn > 0 else qinv(qmap[l]))
        return h

    def face_path(f):
        l0, l1, l2, l3 = face_links(f)
        return [(l0, 1), (l1, 1), (l2, -1), (l3, -1)]
    RECT_PATH = [(((0, 0, 0), 'x'), 1), (((1, 0, 0), 'x'), 1), (((2, 0, 0), 'z'), 1), (((1, 0, 1), 'x'), -1), (((0, 0, 1), 'x'), -1), (((0, 0, 0), 'z'), -1)]
    seven = sorted(set(face_links(F1)) | set(face_links(F2)))
    qfix = {l: qs[20 + i] for i, l in enumerate(seven)}
    r11_links = {'h1': qfix[((0, 0, 1), 'x')], 'h2': qfix[((1, 0, 1), 'x')], 'h3': qfix[((0, 0, 0), 'x')], 'h4': qfix[((1, 0, 0), 'x')],
                 'vL': qinv(qfix[((0, 0, 0), 'z')]), 'vM': qinv(qfix[((1, 0, 0), 'z')]), 'vR': qinv(qfix[((2, 0, 0), 'z')])}
    w_f1, w_f2, w_12 = fine_hol(qfix, face_path(F1))[0], fine_hol(qfix, face_path(F2))[0], fine_hol(qfix, RECT_PATH)[0]
    ident_fix = (w_f1, w_f2, w_12) == invariants(r11_links)
    qflip = {l: (tuple(-t for t in q_) if in_flip_set(l) else q_) for l, q_ in qfix.items()}
    flip_fix = (fine_hol(qflip, face_path(F1))[0] == -w_f1 and fine_hol(qflip, face_path(F2))[0] == -w_f2 and fine_hol(qflip, RECT_PATH)[0] == w_12)
    check('z3_rectangle_geometry',
          geom_ok and rect_ok and ident_fix and flip_fix,
          counts=geom, rectangle_links=[[list(l[0]), l[1]] for l in RECT], rectangle_owners=[list(coarse(l[0])) for l in RECT],
          faces={'W (F1)': [list(F1[0]), F1[1] + F1[2], 'r=0, s=0', sorted(map(list, face_owners(F1)))],
                 'second face (F2)': [list(F2[0]), F2[1] + F2[2], 'r=1, s=0', sorted(map(list, face_owners(F2)))]},
          shared_middle_link=[list(shared_link[0][0]), shared_link[0][1]],
          identification='on the seven fine links of F1 and F2 (product Haar), (W_F1, W_F2, W_{1x2}) = (x, y, z) of the Round11 graph: checked on exact rational quaternions',
          fixture_traces=[s(w_f1), s(w_f2), s(w_12)], norm='||W_{1x2}|| <= 1; W_{1x2} is in B(H_R) because all six links are owned by R')

    # ---- first order: centre grading (AW1 F04), Kato per box, Tr(P_R W12) = Tr(rho^(1)_R W12) = 0 ----
    single_nonzero = [f for f in omitted if not grading_zero([RECT, face_links(f)])]
    e_w12 = grading_zero([RECT])
    tr_rho1_w12 = sum((Q(1, 36) * (0 if grading_zero([RECT, face_links(f)]) else 1) for f in inside), Q(0))     # (tau/36) sum E[W12 W_f] / tau
    tr_rho1_w = sum((Q(1, 36) * (moment(2, 0, 0) if f == F1 else (0 if grading_zero([face_links(F1), face_links(f)]) else None)) for f in inside), Q(0))
    moments_two_routes = moment(0, 0, 1) == 0 and moment(1, 0, 1) == 0 and moment(0, 1, 1) == 0
    first_order_ok = (not single_nonzero and e_w12 and tr_rho1_w12 == 0 and tr_rho1_w == Q(1, 144) and moments_two_routes)
    check('z3_first_order_zero',
          first_order_ok,
          grading='every link of W_{1x2} occurs once; a single face covers at most three of its six links, so E[W_{1x2} W_f] = 0 for every face f '
                  '(single-occurrence orthogonality, AW1 F04), and E[W_{1x2}] = 0',
          kato_per_box='in every box of F1 and F2 (simple isolated ground, gap >= 1/2, bounded V; AM2, AY1 item 1) omega_N(W_{1x2}) is real-analytic in tau and '
                       'd omega_N(W_{1x2})/dtau at 0 = 2 Re<W_{1x2}Omega_0,psi_1> = (1/36) sum_f E[W_{1x2} W_f] = 0',
          trace_P_R_W12='0', trace_rho1_R_W12='0', positive_control_trace_rho1_R_W=s(tr_rho1_w) + ' tau (AW1: +tau/144)',
          second_route='Round11 moments on the seven links: E[z] = E[xz] = E[yz] = 0', faces_scanned=len(omitted))

    # ---- the admitted bound |omega(W12)| <= K_2' tau^2 (AY1 per-box ball; AY1/AY2 gate ball; BB2 identification) ----
    t8 = V['tau_z3']
    a_ = t8 / 144
    J8 = 28 * t8
    T_ = 49 * a_ / (1 - 352 * J8)
    rho_ = 352 * J8 * T_
    epsR = geom['faces_meeting_R'] * a_ + 2 * rho_ + (geom['faces_per_site_of_R_without_the_other_site'] * a_ + rho_) ** 2
    K2_items = {'am2_remainder_4rho': 4 * rho_, 'straddling_2T(72a+2rho)': 2 * T_ * (geom['straddling_meeting_R'] * a_ + 2 * rho_),
                'two_creation_2(33a+rho)^2': 2 * (geom['faces_per_site_of_R_without_the_other_site'] * a_ + rho_) ** 2,
                'density_2epsR^2': 2 * epsR ** 2, 'normalization_20a_epsR^2': 20 * a_ * epsR ** 2}
    K2p_re = sum(K2_items.values(), Q(0)) / t8 ** 2
    bound_w12 = K2p * t8 ** 2
    k2_ok = K2p_re == K2p and T_ == Q(49, 14398580736) and rho_ == Q(3773, 11248891200000000)
    W12_BOUND_ROWS = []
    for fam in ('F1 boxes', 'F2 boxes', 'limit of the named constructions'):
        for sg in ('+', '-'):
            W12_BOUND_ROWS.append({'family': fam, 'sign': sg, 'bound': s(bound_w12), 'tier': 'exact_first_order',
                                   'source': ("AY1 forward HNM-AY1-F11..F14 per-box ball (a reviewed step of the admitted AY1 proof; uniform in N, cutoff and both families; "
                                              "untruncated ground vector by AV1 F22) with the AY1 gate K_2'") if fam != 'limit of the named constructions' else
                                             ("AY1 gate items (3)-(4) and AY2 gate item (1): the ball for every subsequential limit of F1 and F2, identified with the "
                                              "limit of the named constructions by BB2 gate items 2-3"),
                                   'model': 'AQ_patterned_zero_selected', 'mirror_replay': sg == '-'})
    check('z3_bound_K2prime',
          k2_ok and bound_w12 > 0 and len(W12_BOUND_ROWS) == 6,
          K2prime=s(K2p), K2prime_preview=dec(K2p, 12), K2prime_items_over_tau2={k: dec(v / t8 ** 2, 10) for k, v in K2_items.items()},
          second_code_path='K_2\' recomputed from the AY1 F14 items with T=49a/(1-352J), rho=352JT, J=28|tau| and the enumerated pins 82, 72, 33 equals the AY1 gate value',
          bound_at_cap=s(bound_w12), bound_preview=dec(bound_w12, 12), rows=W12_BOUND_ROWS,
          derivation='omega(W_{1x2}) = Tr(rho_R W_{1x2}) = Tr(P_R W_{1x2}) + Tr(rho^(1)_R W_{1x2}) + Tr((rho_R - P_R - rho^(1)_R) W_{1x2}); the first two are 0 and '
                     '|Tr(X W_{1x2})| <= ||W_{1x2}|| ||X||_1 <= K_2\' tau^2 (trace duality, ||W_{1x2}|| <= 1)',
          note='no sign: the bound is symmetric about 0; K_2^+ (AW1) is W-specific and is not used for W_{1x2}')

    # ---- control evenness_from_flip ----
    flip_counts = {'rectangle': sum(in_flip_set(l) for l in RECT), 'F1': sum(in_flip_set(l) for l in face_links(F1)),
                   'F2': sum(in_flip_set(l) for l in face_links(F2))}
    every_plaquette_odd = all(sum(in_flip_set(l) for l in face_links(f)) % 2 == 1 for f in faces)
    EVEN = {'boxes': 'F1: every open centered whole-star box, every on-site cutoff, kappa=0', 'limit': 'through BB2 at each sign (whole-sequence limit of F1 boxes)',
            'F2_boxes_claimed': False, 'remainder_from_evenness': None, 'kappa': 0, 'loop': 'W_{1x2}'}

    def validate_even(e, loop_links):
        require(sum(in_flip_set(l) for l in loop_links) % 2 == 0, 'U_E fixes the loop only if it meets E evenly (area 2); an area-1 loop is odd')
        require(e['F2_boxes_claimed'] is False, 'the AW1 flip lemma is admitted for F1 boxes only; F2 boxes are not claimed')
        require(e['remainder_from_evenness'] is None, 'evenness gives no remainder bound')
        require(e['kappa'] == 0, 'antisymmetry of the face terms under U_E is used at the zero triple only')
        return True
    check('evenness_from_flip',
          every_plaquette_odd and flip_counts == {'rectangle': 6, 'F1': 3, 'F2': 3} and flip_fix and validate_even(EVEN, RECT)
          and rejected(lambda: validate_even(dict(EVEN, F2_boxes_claimed=True), RECT), 'evenness_claimed_for_F2_boxes')
          and rejected(lambda: validate_even(dict(EVEN, remainder_from_evenness='O(tau^4)'), RECT), 'remainder_bound_from_evenness')
          and rejected(lambda: validate_even(EVEN, face_links(F1)), 'area_one_loop_W_claimed_even')
          and rejected(lambda: validate_even(dict(EVEN, kappa=1), RECT), 'nonzero_selected_triple'),
          flip_set=FLIP_E_TEXT, E_intersections=flip_counts, every_plaquette_of_the_window_odd=every_plaquette_odd, plaquettes_checked=len(faces),
          statement='U_E W_f U_E^* = -W_f for every plaquette and U_E W_{1x2} U_E^* = W_{1x2}; with U_E H_N(tau,0) U_E^* = H_N(-tau,0) (AW1 F09) the ground vector '
                    'maps to itself up to U_E, so omega_{N,-tau}(W_{1x2}) = omega_{N,tau}(W_{1x2}) in every F1 box and on-site cutoff (AW1 F10); both signs converge '
                    'as whole sequences (BB2 item 1), so the limit of the named constructions is even in tau as well',
          not_claimed='F2 boxes; any remainder bound; kappa != 0')

    # ---- control formal_coefficient_labelled: the formal second-order coefficient ----
    near = [f for f in omitted if set(face_links(f)) & set(RECT)]
    pairs = [(g, f) for g in near for f in near if not grading_zero([face_links(g), face_links(f), RECT])]
    E_rect = 8 * Q(3, 4) * len(RECT)
    E_face = 8 * Q(3, 4) * 4
    c1 = Q(1, 3) / E_face
    haar_pair = moment(1, 1, 1)
    termA = 2 * Q(1, 3) * c1 / E_rect * len(pairs) * haar_pair
    termB = c1 ** 2 * len(pairs) * haar_pair
    formal = termA + termB
    formal_ok = (sorted(pairs) == sorted([(F1, F2), (F2, F1)]) and E_rect == 36 and E_face == 24 and c1 == Q(1, 72) and haar_pair == Q(1, 16)
                 and termA == Q(1, 31104) and termB == Q(1, 41472) and formal == Q(7, 124416))
    graph_consistency = zt[(1, 1)] / 24 ** 2 == formal
    FORMAL = {'label': 'formal_second_order_coefficient', 'value': s(formal), 'certified_third_order_remainder': None, 'sign_of_omega_claimed': False,
              'certified_value_of_omega': None, 'bound': "K_2' tau^2 (no sign)", 'bound_encloses_formal_coefficient': False,
              'rectangle': [[list(l[0]), l[1]] for l in RECT], 'model': 'AQ_patterned_zero_selected (formal, every box N>=2 and the limit alike)'}

    def validate_formal(fm):
        require(fm['label'] == 'formal_second_order_coefficient', 'the Z^3 second-order coefficient must carry the formal label')
        require(fm['certified_third_order_remainder'] is None and fm['certified_value_of_omega'] is None, 'no certified remainder or value is claimed')
        require(fm['sign_of_omega_claimed'] is False, 'no sign of omega(W_{1x2}) is claimed')
        require(fm['bound_encloses_formal_coefficient'] is False, "the bound K_2' tau^2 is not an enclosure of the formal coefficient")
        require(all(coarse(tuple(l[0])) in R_SET for l in fm['rectangle']), 'the bound applies only to a rectangle contained in R')
        return True
    shifted = [[[l[0][0] + 2, l[0][1], l[0][2]], l[1]] for l in RECT]
    check('formal_coefficient_labelled',
          formal_ok and validate_formal(FORMAL)
          and rejected(lambda: validate_formal(dict(FORMAL, label='certified_second_order_value')), 'formal_coefficient_presented_as_certified_value')
          and rejected(lambda: validate_formal(dict(FORMAL, sign_of_omega_claimed=True)), 'sign_of_omega_from_the_formal_coefficient')
          and rejected(lambda: validate_formal(dict(FORMAL, bound_encloses_formal_coefficient=True)), 'bound_read_as_enclosure_of_the_formal_coefficient')
          and rejected(lambda: validate_formal(dict(FORMAL, certified_third_order_remainder='K_3 |tau|^3')), 'third_order_remainder_claimed')
          and rejected(lambda: validate_formal(dict(FORMAL, rectangle=shifted)), 'rectangle_not_contained_in_R'),
          formal_second_order_coefficient=s(formal), preview=dec(formal, 10),
          derivation={'psi_1': '(1/72) sum_f W_f Omega_0 (face energy 24, coefficient -tau/3)', 'E_1': '0',
                      'term_2Re<W12Omega_0,psi_2>': s(termA), 'term_<psi_1,W12psi_1>': s(termB),
                      'surviving_pairs': 'only (F1,F2) and (F2,F1): E[W_F1 W_F2 W_{1x2}] = E[xyz] = 1/16; W_{1x2} Omega_0 has energy 36',
                      'normalization': 'no second-order normalization term because E[W_{1x2}] = 0'},
          consistency_labelled='equals the graph coefficient 7/216 of <z> at l1=l2 under tau_FG = tau/24 (same two-face algebra and energies); a consistency identity, not a transfer',
          obstruction="the admitted certified bound K_2' tau^2 exceeds the formal term (7/124416) tau^2 by the factor %s; no remainder beyond second order is admitted" % dec(K2p / formal, 6),
          label=FORMAL['label'])

    # ======================= item 4: the electric energy band on R =======================
    tb = V['band_tau']
    stars_meeting_R = sorted({(r_[0] - s_[0], r_[1] - s_[1], r_[2] - s_[2]) for r_ in R_SET for s_ in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))})
    star_norm = len(per_anchor) * Q(1, 3)                         # ||phi_b|| = 21 |tau|/3 = 7|tau| (I1.5)
    upper_coeff = 2 * len(stars_meeting_R) * star_norm            # AQ1.1 with the 7 incident anchors of R
    generic_coeff = 2 * 4 * 2 * star_norm                         # 56|tau||F| at |F|=2 (valid, not frozen)
    gap_min = 8 * Q(3, 4)                                         # smallest nonzero value of 8 sum_e j_e(j_e+1): one link at j=1/2
    L_box = sqrt10_lo * tb / 72 - K2p * tb ** 2
    lower_box = V['band_gap'] * (L_box / 2) ** 2
    lower_lim = V['band_gap'] * (L_ay2 / 2) ** 2
    upper = upper_coeff * tb
    band_ok = (len(stars_meeting_R) == V['band_anchors'] == 7 and upper_coeff == V['band_upper_coeff'] and generic_coeff == 2 * V['band_generic_coeff']
               and gap_min == V['band_gap'] and L_box == L_ay2 and lower_box == lower_lim and 0 < lower_lim < upper and sqrt10_lo ** 2 < 10 < sqrt10_hi ** 2)
    # per-link formal second-order values from the I1 face classes (selected faces carry coefficient 0)
    incidence = {l: sum(1 for f in omitted if l in face_links(f)) for l in R_LINKS}
    per_link_formal = {l: n_ * 8 * Q(3, 4) * Q(1, 4) * c1 ** 2 for l, n_ in incidence.items()}
    formal_h = sum(per_link_formal.values(), Q(0))
    hist = {}
    for n_ in incidence.values():
        hist[n_] = hist.get(n_, 0) + 1
    per_link_rows = {'%d,%d,%d,%s' % (l[0][0], l[0][1], l[0][2], l[1]): {'omitted_faces': n_, 'formal_coefficient': s(per_link_formal[l])}
                     for l, n_ in sorted(incidence.items())}
    formal_h_ok = (sum(incidence.values()) == 4 * 2 * len(per_anchor) and formal_h == Q(7, 144) and hist == {4: 28, 3: 16, 2: 4}
                   and all(per_link_formal[l] == Q(incidence[l], 3456) for l in R_LINKS))
    # Fuchs-van de Graaf for a pure reference, exact fixtures (2x2: the difference of two trace-one matrices is traceless)
    def tn2(rho):
        """((1/2)||rho - P||_1)^2 for a real symmetric 2x2 density rho and P = e1 e1^T (eigenvalues +-sqrt(-det))."""
        d11, d12, d22 = rho[0][0] - 1, rho[0][1], rho[1][1]
        return -(d11 * d22 - d12 * d12)
    psi_a, psi_b = (Q(3, 5), Q(4, 5)), (Q(5, 13), Q(12, 13))
    pure = [[psi_a[i] * psi_a[j] for j in range(2)] for i in range(2)]
    mixed = [[(psi_a[i] * psi_a[j] + psi_b[i] * psi_b[j]) / 2 for j in range(2)] for i in range(2)]
    fvdg_ok = (tn2(pure) == 1 - pure[0][0] and tn2(mixed) <= 1 - mixed[0][0] and tn2(mixed) < 1 - mixed[0][0])

    def validate_fvdg_constant(const):
        # claimed inequality: const * ||rho - P||_1 <= sqrt(Tr(Q rho)), tested exactly on the pure fixture (squared form)
        require((2 * const) ** 2 * tn2(pure) <= 1 - pure[0][0], 'the Fuchs-van de Graaf constant must be 1/2 (equality for pure states)')
        return True
    # lower semicontinuity versus continuity: rho_k = (1-1/k)|0><0| + (1/k)|k><k|, h = diag(n): energy 1 for every k, limit energy 0
    lsc_rows = [(k, Q(1, k) * k, 2 * Q(1, k)) for k in (2, 10, 1000)]   # (k, Tr(rho_k h), ||rho_k - |0><0| ||_1)
    lsc_ok = all(e_ == 1 for _, e_, _ in lsc_rows) and lsc_rows[-1][2] == Q(1, 500)
    BAND_ROUTE = {'value': 'monotone limit over the spectral projections Q_L of h_R of Tr(rho_R h_R Q_L)',
                  'upper': 'AQ1 reset HNM-AQ1.1 with the 7 incident anchors (F2: AY1 gate item (1))', 'upper_coefficient': upper_coeff,
                  'upper_passage': 'lower semicontinuity', 'lower_inequality': 'h_R >= 6 Q_R', 'lower_gap': gap_min,
                  'lower_distance_source_boxes': 'AY1 forward HNM-AY1-F11..F14 per-box ball', 'lower_distance_source_limit': 'AY2 gate item (2)',
                  'bounded_constant_applied_to_h_R': False, 'fvdg_constant': Q(1, 2)}

    def validate_band_route(b):
        require(b['value'].startswith('monotone limit over the spectral projections'), 'omega(h_R) must be defined as the monotone cutoff limit')
        require(b['bounded_constant_applied_to_h_R'] is False, 'a bounded-observable trace-norm constant cannot be applied to the unbounded h_R')
        require(b['upper_coefficient'] == V['band_upper_coeff'], 'the upper budget is the frozen 98|tau| (not 56|tau||F|, not 28|tau|)')
        require(b['upper_passage'] == 'lower semicontinuity', 'the upper endpoint passes to the limit by lower semicontinuity only')
        require(b['lower_gap'] == V['band_gap'] and b['lower_inequality'] == 'h_R >= 6 Q_R', 'operator inequality h_R >= 6 Q_R')
        require(b['lower_distance_source_boxes'] == 'AY1 forward HNM-AY1-F11..F14 per-box ball', 'finite boxes use the AY1 per-box ball, not the limit-level AY2 distance')
        require(b['lower_distance_source_limit'] == 'AY2 gate item (2)', 'the limit uses the AY2 gate item (2)')
        validate_fvdg_constant(b['fvdg_constant'])
        return True
    check('unbounded_observable_handled',
          band_ok and fvdg_ok and lsc_ok and validate_band_route(BAND_ROUTE)
          and rejected(lambda: validate_band_route(dict(BAND_ROUTE, bounded_constant_applied_to_h_R=True)), 'bounded_trace_norm_constant_applied_to_h_R')
          and rejected(lambda: validate_band_route(dict(BAND_ROUTE, lower_distance_source_boxes='AY2 gate item (2)')), 'limit_level_AY2_distance_used_for_a_finite_box')
          and rejected(lambda: validate_band_route(dict(BAND_ROUTE, upper_coefficient=generic_coeff)), 'upper_budget_56_tau_F_not_frozen')
          and rejected(lambda: validate_band_route(dict(BAND_ROUTE, upper_coefficient=Q(28))), 'upper_budget_two_anchor_28_tau')
          and rejected(lambda: validate_band_route(dict(BAND_ROUTE, upper_passage='trace-norm continuity')), 'energy_passed_to_the_limit_by_continuity')
          and rejected(lambda: validate_band_route(dict(BAND_ROUTE, fvdg_constant=Q(1))), 'fuchs_van_de_graaf_without_the_one_half'),
          monotone_passage='for L >= 6: h_R Q_L >= 6 (Q_L - P_R) since the spectrum of h_R is {0} u [6, infinity) with kernel P_R; Tr(rho h_R Q_L) is nondecreasing in L '
                           'and tends to omega(h_R) in [0, infinity]; Tr(rho (Q_L - P_R)) -> Tr(rho Q_R), so omega(h_R) >= 6 Tr(Q_R rho_R)',
          fuchs_van_de_graaf='pure pair: (1/2)||P_phi - P_Omega||_1 = sqrt(1 - |<Omega,phi>|^2) for unit vectors; mixed rho = sum p_i P_(phi_i): convexity of the trace norm and '
                             'concavity of sqrt give (1/2)||rho - P_R||_1 <= sum p_i sqrt(1 - |<Omega,phi_i>|^2) <= sqrt(Tr(Q_R rho))',
          fvdg_fixture={'pure_squared_half_norm': s(tn2(pure)), 'pure_Tr_Q_rho': s(1 - pure[0][0]), 'mixed_squared_half_norm': s(tn2(mixed)), 'mixed_Tr_Q_rho': s(1 - mixed[0][0])},
          lower_semicontinuity='for each L, Tr(rho_R h_R Q_L) = lim_k Tr(rho_{N_k,R} h_R Q_L) <= liminf_k omega_{N_k}(h_R) <= 98|tau| (h_R Q_L bounded); sup over L gives omega(h_R) <= 98|tau|',
          lsc_fixture={'rows_k_energy_distance': [[k, s(e_), s(d_)] for k, e_, d_ in lsc_rows], 'limit_energy': '0',
                       'reading': 'energy 1 in every term, trace-norm limit with energy 0: only the upper endpoint passes by semicontinuity; the lower endpoint is proved at the limit directly'},
          anchors_meeting_R=[list(x) for x in stars_meeting_R], star_norm_per_tau=s(star_norm), upper_coefficient=s(upper_coeff), generic_valid_not_frozen=s(generic_coeff))

    BAND_ROWS = []
    for fam in ('F1 boxes', 'F2 boxes', 'limit of the named constructions'):
        for sg in ('+', '-'):
            is_lim = fam == 'limit of the named constructions'
            BAND_ROWS.append({'family': fam, 'sign': sg, 'tau': ('' if sg == '+' else '-') + s(tb),
                              'lower': s(lower_lim if is_lim else lower_box), 'upper': s(upper),
                              'lower_tier': 'first_order_distance_from_product', 'upper_tier': 'crude_majorant',
                              'lower_source': ('AY2 gate item (2) lower end L, identified with the limit by BB2 gate items 2-3' if is_lim else
                                               "AY1 forward HNM-AY1-F11..F14 per-box ball with the AY1 gate K_2' and the AY2 directed sqrt(10) bracket "
                                               "(a reviewed step of the admitted AY1 proof, not an AY1 or AY2 gate sentence)"),
                              'upper_source': ('AQ1 reset HNM-AQ1.1 (7 incident anchors) in every box, passed to the limit by lower semicontinuity' if is_lim else
                                               ('AQ1 reset HNM-AQ1.1 (7 incident anchors)' if fam == 'F1 boxes' else 'AY1 gate item (1): reset omega(h_R)<=98|tau| for F2')),
                              'state': 'untruncated finite-box ground vector at fixed N (every N>=2)' if not is_lim else 'limit of the named constructions (BB2)',
                              'model': 'AQ_patterned_zero_selected', 'mirror_replay': sg == '-'})

    def validate_band_rows(rows):
        need = {(f_, sg) for f_ in ('F1 boxes', 'F2 boxes', 'limit of the named constructions') for sg in ('+', '-')}
        require({(r_['family'], r_['sign']) for r_ in rows} == need, 'the band is stated at both signs for F1 boxes, F2 boxes and the limit')
        for r_ in rows:
            lo_, hi_ = rat(r_['lower']), rat(r_['upper'])
            require(0 < lo_ <= hi_, 'exact rational endpoints with 0 < lower <= upper')
            twin = [q_ for q_ in rows if q_['family'] == r_['family'] and q_['sign'] != r_['sign']][0]
            require(twin['lower'] == r_['lower'] and twin['upper'] == r_['upper'], 'the -tau row is the mirror replay of the +tau row')
        return True
    check('band_both_signs',
          validate_band_rows(BAND_ROWS)
          and rejected(lambda: validate_band_rows([r_ for r_ in BAND_ROWS if not (r_['family'] == 'F2 boxes' and r_['sign'] == '-')]), 'minus_tau_F2_row_missing')
          and rejected(lambda: validate_band_rows([r_ for r_ in BAND_ROWS if r_['family'] != 'limit of the named constructions']), 'band_for_finite_boxes_only')
          and rejected(lambda: validate_band_rows([dict(r_, lower=0.1) if r_['family'] == 'F1 boxes' else r_ for r_ in BAND_ROWS]), 'floating_point_endpoint')
          and rejected(lambda: validate_band_rows([dict(r_, upper=s(2 * upper)) if (r_['family'], r_['sign']) == ('limit of the named constructions', '-') else r_
                                                   for r_ in BAND_ROWS]), 'minus_tau_row_not_a_mirror'),
          rows=BAND_ROWS, lower_exact=s(lower_lim), upper_exact=s(upper), lower_preview=dec(lower_lim, 12), upper_preview=dec(upper, 12),
          L_distance_lower=s(L_ay2), formula='lower = 6 (L/2)^2 = (3/2) L^2 with L = sqrt(10)_lo |tau|/72 - K_2\' tau^2; upper = 98|tau|',
          formal_second_order_value_per_link=per_link_rows, formal_second_order_total=s(formal_h) + ' tau^2 (formal_second_order_coefficient; no certified remainder)',
          incidence_histogram={str(k): v for k, v in sorted(hist.items())},
          formal_total_preview_at_cap=dec(formal_h * tb ** 2, 8),
          obstruction='a tight enclosure needs a second-order upper bound on an unbounded observable (an energy-weighted state estimate); the admitted upper budget is first order '
                      'and exceeds the formal value by the factor %s, the lower end is below it by the factor %s' % (dec(upper / (formal_h * tb ** 2), 6), dec(formal_h * tb ** 2 / lower_lim, 6)))

    # ======================= item 5: 2+1-dimensional recount (declared factorization) =======================
    ex2, ey2 = (1, 0), (0, 1)

    def z2_face(p):
        return (((p[0], p[1]), 'x'), ((p[0] + 1, p[1]), 'y'), ((p[0], p[1] + 1), 'x'), ((p[0], p[1]), 'y'))
    sites2 = [(i, j) for i in range(-4, 5) for j in range(-4, 5)]
    owner_sets2 = {p: frozenset(l[0] for l in z2_face(p)) for p in sites2}      # single-site factors own (p,x) and (p,y)
    bulk2 = [(i, j) for i in range(-2, 3) for j in range(-2, 3)]
    faces_per_site = {u: sum(1 for X in owner_sets2.values() if u in X) for u in bulk2}
    stars2 = sorted({(q[0] - p[0], q[1] - p[1]) for p, X in owner_sets2.items() for q in X})
    p2 = max(len(X) for X in owner_sets2.values())
    J2_per_tau = max(faces_per_site.values()) * Q(1, 3)                        # each face its own term, ||V_X|| = |tau|/3
    incoming2 = {u: sorted((u[0] - d[0], u[1] - d[1]) for d in stars2) for u in bulk2[:1]}
    counts_ok = (p2 == V['p2'] and set(faces_per_site.values()) == {3} and stars2 == [(0, 0), (0, 1), (1, 0)] and J2_per_tau == 1
                 and all(owner_sets2[p] == frozenset({p, (p[0] + 1, p[1]), (p[0], p[1] + 1)}) for p in sites2))
    nums3 = [am2_numerator(p2, k) for k in range(2 * p2 + 1)]
    nums4 = [am2_numerator(4, k) for k in range(9)]
    formula_ok = (all(nums4[k] == 16 * 8 ** k * (1 + Q(5 * k, 4)) for k in range(9))
                  and all(g_closed_form_coeffs(p_, 12) == [am2_numerator(p_, k) for k in range(13)] for p_ in (3, 4))
                  and nums3 == [Q(8), Q(112), Q(1056), Q(8640), Q(65664), Q(476928), Q(3359232)])
    # G_3(t) = 8 e^{6t}(1+8t), G_3'(t) = 8 e^{6t}(14+48t): k! [t^k] G_3' = L_{k+1}
    gp_ok = all(Q(8 * 14 * 6 ** k) + (Q(8 * 48 * k * 6 ** (k - 1)) if k else 0) == am2_numerator(3, k + 1) for k in range(12))
    vecs3, vanish3 = creation_fixture(p2, 2 * p2 + 1)
    vecs4, vanish4_at7 = creation_fixture(4, 7)
    term_ok = (vecs3[2 * p2][-1] == (-1) ** p2 * factorial(2 * p2) and all(x == 0 for x in vecs3[2 * p2][:-1]) and vanish3 and not vanish4_at7)
    x_exp = 2 * p2 * V['R_am2']
    e_lo_ex, e_hi_ex = exp_bracket(x_exp, 24)
    e_lo, e_hi = out_dn(e_lo_ex, 40), out_up(e_hi_ex, 40)
    G3_coef = 2 ** p2 * (1 + 2 * (p2 + 1) * V['R_am2'])                          # G_3(R) = 9 e^{3/32}
    G3p_coef = 2 ** p2 * (2 * p2 + 2 * (p2 + 1) + 4 * p2 * (p2 + 1) * V['R_am2'])  # G_3'(R) = 118 e^{3/32}
    G3 = (G3_coef * e_lo, G3_coef * e_hi)
    G3p = (G3p_coef * e_lo, G3p_coef * e_hi)
    tau_star_lo = V['R_am2'] / (J2_per_tau * G3[1])
    tau_star_hi = V['R_am2'] / (J2_per_tau * G3[0])
    cap = out_dn(tau_star_lo, 15)
    excl_lo = 1 / (2 * J2_per_tau * G3p[1])
    selfmap_ok = cap * J2_per_tau * G3[1] <= V['R_am2']
    excl_ok = 2 * cap * J2_per_tau * G3p[1] < 1
    trunc = sum((am2_numerator(p2, k) * V['R_am2'] ** k / factorial(k) for k in range(2 * p2 + 1)), Q(0))
    cap_trunc = out_dn(V['R_am2'] / trunc, 15)
    dim_ok = (counts_ok and formula_ok and gp_ok and term_ok and x_exp == Q(3, 32) and G3_coef == 9 and G3p_coef == 118
              and e_lo < e_hi and selfmap_ok and excl_ok and cap < tau_star_hi and tau_star_lo < excl_lo)
    DIM = {'model': 'declared 2+1D model: Z^2, 8 C_e per link, -(tau/3) W_f on every face, no selected faces, Haar product reference (delta units)',
           'factorization': 'single-site factors owning (p,x) and (p,y)', 'owner_set': '{p, p+e_x, p+e_y}', 'star': [list(d) for d in stars2],
           'p': p2, 'faces_per_site': 3, 'incoming_stars_per_site': 3, 'faces_anchored_per_site': 1,
           'J_over_tau': s(J2_per_tau), 'termination_order': 2 * p2, 'numerators': [s(x) for x in nums3],
           'G_p': '2^p e^{2pt}(1+2(p+1)t) = 8 e^{6t}(1+8t)', 'G_p_prime': '8 e^{6t}(14+48t)',
           'exp_argument': s(x_exp), 'exp_bracket': [s(e_lo), s(e_hi)], 'G3_R': [s(G3[0]), s(G3[1])], 'G3prime_R': [s(G3p[0]), s(G3p[1])],
           'cap_directed_lower': s(cap), 'tau_star_bracket': [s(out_dn(tau_star_lo, 15)), s(out_up(tau_star_hi, 15))],
           'binding_condition': 'self-map J G_3(R) <= R', 'dictionary': 'own contract (g^2 has mass dimension in 2+1D)', 'tier': None}
    DIM3 = {'p': 4, 'J_over_tau': '28', 'termination_order': 8, 'G_R_upper': '148/7', 'Gprime_R_upper': '352', 'dictionary': 'tau=96/g^4 (3+1D, AL1 via AX1)'}

    def validate_dim(d):
        require(d['p'] == p2 == 3, 'maximal support recounted for the 2D factorization is 3 (a 3+1D p=4 is rejected)')
        require(rat(d['J_over_tau']) == J2_per_tau == 1, 'the 2+1D per-site sum is |tau| (three faces of norm |tau|/3; 28|tau| is 3+1D)')
        require(d['termination_order'] == 2 * d['p'] == 6 and vanish3, 'termination order 2p = 6 (the 3+1D order 8 is rejected)')
        require(d['numerators'] == [s(am2_numerator(d['p'], k)) for k in range(2 * d['p'] + 1)], 'AM2 numerators at p=3')
        require(d['G3_R'] == [s(G3[0]), s(G3[1])] and d['exp_argument'] == '3/32', 'G_3(R) from the own directed enclosure of e^{3/32}')
        require(d['dictionary'].startswith('own contract'), 'the 3+1D dictionary is not the 2+1D one')
        require(d['tier'] is None, 'the 2+1D constants carry no tier')
        return True
    check('dimension_recount',
          dim_ok and validate_dim(DIM)
          and rejected(lambda: validate_dim(dict(DIM, p=DIM3['p'], numerators=[s(x) for x in nums4])), 'three_plus_one_support_p4_reused')
          and rejected(lambda: validate_dim(dict(DIM, J_over_tau=DIM3['J_over_tau'])), 'three_plus_one_per_site_sum_28_tau_reused')
          and rejected(lambda: validate_dim(dict(DIM, termination_order=DIM3['termination_order'])), 'three_plus_one_termination_order_8_reused')
          and rejected(lambda: validate_dim(dict(DIM, G3_R=['0', DIM3['G_R_upper']])), 'three_plus_one_G_R_148_over_7_reused')
          and rejected(lambda: validate_dim(dict(DIM, dictionary=DIM3['dictionary'])), 'three_plus_one_dictionary_reused')
          and rejected(lambda: validate_dim(dict(DIM, tier='crude_majorant')), 'tier_attached_to_a_2p1_constant'),
          recount=DIM, faces_per_site_bulk=sorted(set(faces_per_site.values())), sites_checked=len(bulk2),
          incoming_stars_example={str(k): [list(x) for x in v] for k, v in incoming2.items()},
          termination_fixture={'p': p2, 'ad_C^6(V)Omega': '%d |111>' % ((-1) ** p2 * factorial(2 * p2)), 'ad_C^7(V)': '0',
                               'p=4 control': 'ad_C^7(V) != 0 (so order 6 is not a p=4 termination)'},
          exp_enclosure={'series_terms': 25, 'lower': s(e_lo), 'upper': s(e_hi), 'preview': dec(e_lo, 20)},
          G3_R_preview=[dec(G3[0], 12), dec(G3[1], 12)], G3prime_R_preview=[dec(G3p[0], 12), dec(G3p[1], 12)],
          cap={'directed_lower': s(cap), 'preview': dec(cap, 12), 'self_map_at_cap': s(cap * J2_per_tau * G3[1]), 'exclusion_at_cap': s(2 * cap * J2_per_tau * G3p[1]),
               'exclusion_alone_lower': dec(excl_lo, 12), 'tau_star_bracket_preview': [dec(tau_star_lo, 12), dec(tau_star_hi, 12)]},
          labelled_variant={'truncated_majorant_sum_k_le_6_at_R': s(trunc), 'cap_from_truncated_majorant': s(cap_trunc), 'status': 'labelled variant, not the headline'},
          three_plus_one_reference_not_reused=DIM3)


    # ======================= item 5 (continued): what transfers verbatim and what needs its own contract =======================
    TRANSFERS = {
        'verbatim_algebraic': [
            'the SU(2) centre grading and Haar parity rule (AW1 F04) and the Haar moments E[W^n]: per-link algebra, dimension-independent',
            'the AM2 creation algebra (commuting nilpotent creations, the fixed-point form, the Banach self-map and Lipschitz structure) and its counting '
            'L_k^num(p) = 2^p (2p)^k (1 + k(p+1)/p) for general p, here instantiated at p=3',
            'the AV2 window-kernel constants M_0 = 2, M_1 = 4s/pi, M_2 = 2s^2 (a one-dimensional spectral identity, dimension-independent)',
            'trace duality, the Fuchs-van de Graaf inequality and the monotone spectral-cutoff passage (operator facts)',
            'the Round11 two-plaquette graph algebra (a finite graph; no spatial dimension enters)'],
        'own_contract_needed': [
            'the finite-volume ground-state and gap theorem in 2+1 dimensions (missing: a 2D finite-volume prescription, the on-site domains of 8(C_(p,x)+C_(p,y)), '
            'and AM2 sections 4-6 re-verified for the 2D factorization)',
            'the AQ chain in 2+1 dimensions (AQ1 construction and compactness, AQ2 gap transfer, AV1 state lemma, AW1 and AY1/AY2 constants, BB1/BB2 limit)',
            'the Euclidean node certificate (AV2 radius uses the 3+1D state bound D and the seven-star Duhamel slope)',
            'the dictionary (in 2+1 dimensions g^2 has mass dimension; the 3+1D coupling dictionary does not apply)']}
    check('dimension_transfer_rows',
          len(TRANSFERS['verbatim_algebraic']) == 5 and len(TRANSFERS['own_contract_needed']) == 4 and dim_ok,
          transfers=TRANSFERS, window_constants_from_AV2_gate='M_0=||ghat||_1=2, M_1=4s/pi, M_2=2s^2',
          obligation='no finite-volume ground-state or gap statement in 2+1 dimensions is claimed; the recounted constants are not a theorem')

    # ======================= item 6: obligations and no-transfer rows =======================
    OBLIGATIONS = [
        {'id': 'area_law', 'status': 'not proved', 'claimed': False,
         'missing_premise': 'analyticity of the reduced density in a complex tau-disc uniformly in N (a zero-free region for the complexified normalization) and a family of '
                            'growing loops; no zero-free region is admitted',
         'candidate_route': 'a polymer expansion with a proved zero-free region (its own contract)'},
        {'id': 'certified_sign_of_the_Z3_1x2_loop', 'status': 'not proved', 'claimed': False,
         'missing_premise': 'a uniform remainder |omega(W_{1x2}) - (7/124416) tau^2| <= K_4 tau^4 with K_4 tau^2 below 7/124416 (by evenness the third order vanishes for F1 boxes '
                            'and the limit; F2 boxes would need a third-order remainder), i.e. a uniform second-order expansion of the state with certified remainder',
         'candidate_route': "a second-order creation expansion with an R-local fourth-order majorant; the admitted K_2' tau^2 is %s times the formal term" % dec(K2p / formal, 6)},
        {'id': 'tight_electric_energy_enclosure', 'status': 'not proved', 'claimed': False,
         'missing_premise': 'a second-order upper bound on the unbounded omega(h_R) (an energy-weighted or relative-form state estimate); the reset budget is first order',
         'candidate_route': 'relative-form bounds of h_R against the AM2 creation expansion (its own contract)'},
        {'id': 'site_blocked_uniform_3p1_regime', 'status': 'not in this packet', 'claimed': False,
         'missing_premise': 'its own contract (uniform site-blocked model in 3+1 dimensions)', 'candidate_route': 'separate contract'},
        {'id': 'finite_volume_theorem_2p1', 'status': 'not proved', 'claimed': False,
         'missing_premise': 'a 2D finite-volume prescription, the on-site domains, AM2 sections 4-6 re-verified; then the AQ chain, node and dictionary in 2+1 dimensions',
         'candidate_route': 'its own contract using the recounted constants of item 5'},
        {'id': 'einstein_qed_rounds', 'status': 'no-transfer row', 'claimed': False,
         'missing_premise': 'none: the Einstein-QED evidence rounds share no equation with this SU(2) chain', 'candidate_route': 'not applicable (no comparison)'}]

    def validate_obligations(rows):
        ids = [r_['id'] for r_ in rows]
        require(ids == ['area_law', 'certified_sign_of_the_Z3_1x2_loop', 'tight_electric_energy_enclosure', 'site_blocked_uniform_3p1_regime',
                        'finite_volume_theorem_2p1', 'einstein_qed_rounds'], 'every obligation and no-transfer row of item 6')
        require(all(r_['claimed'] is False and r_['missing_premise'] for r_ in rows), 'each row is unclaimed and names its missing premise')
        return True
    check('obligations_and_no_transfer_rows',
          validate_obligations(OBLIGATIONS)
          and rejected(lambda: validate_obligations(OBLIGATIONS[:1] + OBLIGATIONS[2:]), 'sign_obligation_dropped')
          and rejected(lambda: validate_obligations([dict(r_, claimed=True) if r_['id'] == 'area_law' else r_ for r_ in OBLIGATIONS]), 'area_law_row_claimed'),
          rows=OBLIGATIONS, not_claimed=['uniqueness of any ground state', 'any estimate uniform in the lattice spacing', 'continuum or weak coupling', 'scientific priority'])

    # ---- control no_area_law_claim ----
    AREA = {'area_law_claimed': False, 'string_tension_statement': None, 'reason': 'no zero-free region is admitted (obligation row area_law)'}

    def validate_area(a):
        require(a['area_law_claimed'] is False and a['string_tension_statement'] is None, 'no area-law or string-tension statement')
        require('zero-free region' in a['reason'], 'the obstruction is recorded')
        return True
    check('no_area_law_claim',
          validate_area(AREA)
          and rejected(lambda: validate_area(dict(AREA, area_law_claimed=True)), 'area_law_claimed_true')
          and rejected(lambda: validate_area(dict(AREA, string_tension_statement='sigma a^2 bounded below by the 1x2 ratio')), 'string_tension_statement_from_1x2'),
          record=AREA)

    # ---- control no_transfer_to_eqed ----
    EQED = {'rounds': 'the Einstein-QED evidence rounds of the repository', 'relation': 'no_shared_equation', 'comparison': None}

    def validate_eqed(r_):
        require(r_['relation'] == 'no_shared_equation' and r_['comparison'] is None, 'recorded as a no-transfer row, not as a comparison')
        return True
    check('no_transfer_to_eqed',
          validate_eqed(EQED)
          and rejected(lambda: validate_eqed(dict(EQED, relation='comparison', comparison='field-strength analogy')), 'eqed_comparison_drawn')
          and rejected(lambda: validate_eqed(dict(EQED, relation='shared_equation')), 'eqed_shared_equation_claimed'),
          row=EQED)

    # ---- control rate_range_stated ----
    RATES = []    # BD2 makes no new claim of a rate in N

    def validate_rates(rows, flag):
        require(flag is False, 'BD2 makes no new claim of a rate in N')
        for r_ in rows:
            require(r_.get('range_of_N'), 'every rate in N carries its range of N in the same clause')
        return True
    check('rate_range_stated',
          validate_rates(RATES, False)
          and rejected(lambda: validate_rates([{'rate': 'K5/N', 'source': 'BB2'}], False), 'rate_without_range')
          and rejected(lambda: validate_rates(RATES, True), 'rate_in_N_claimed_true'),
          rates=RATES, rate_in_N_claimed=False,
          note='the BB2 limit is used only for its identification (items 2-3); its rate (certified range 5<=N<=14000) is not used or restated as a BD2 claim')

    # ---- control tier_mixing_rejected (BD2 definition) ----
    TIERS = {
        'band_lower': {'tier': 'first_order_distance_from_product', 'source': 'AY2 gate item (2) (limit); AY1 forward per-box ball (F1, F2 boxes)'},
        'band_upper': {'tier': 'crude_majorant', 'source': 'AQ1 reset HNM-AQ1.1 (F2: AY1 gate item (1))'},
        'w12_bound': {'tier': 'exact_first_order', 'source': "AY1 gate K_2' (inherited)"},
        'graph_coefficients': {'tier': None, 'source': 'exact Rayleigh-Schroedinger algebra (AZ2-type certificate code)'},
        'graph_enclosures': {'tier': None, 'source': 'AZ2-type certificate'},
        'z3_formal_coefficient': {'tier': None, 'source': 'formal second-order perturbation theory (labelled formal_second_order_coefficient)'},
        'dimension_2p1_constants': {'tier': None, 'source': 'AM2 counting recounted at p=3'}}
    FORBIDDEN_LABELS = ('weighted_norm', 'analytic_disc', 'nested_telescoping', 'union_comparison', 'bb1_frozen_targets', 'polynomial_lieb_robinson')

    def validate_tiers(t):
        require(t['band_lower']['tier'] == 'first_order_distance_from_product', 'band lower endpoint tier')
        require(t['band_upper']['tier'] == 'crude_majorant', 'band upper endpoint tier')
        require(t['w12_bound']['tier'] == 'exact_first_order', 'W_{1x2} bound tier')
        for key in ('graph_coefficients', 'graph_enclosures', 'z3_formal_coefficient', 'dimension_2p1_constants'):
            require(t[key]['tier'] is None, 'no tier on ' + key)
        for key, row in t.items():
            require(row['source'], 'every value names its source')
            require(row['tier'] is None or row['tier'] in V['tier_names'], 'tier outside the allowed names')
            require(not any(lb in json.dumps(row) for lb in FORBIDDEN_LABELS), 'plan route label, hypothesis source or Lieb-Robinson tier')
        return True

    def tmut(key, **kw):
        t2 = json.loads(json.dumps(TIERS))
        t2[key].update(kw)
        return lambda: validate_tiers(t2)
    check('tier_mixing_rejected',
          validate_tiers(TIERS)
          and rejected(tmut('band_lower', tier='crude_majorant'), 'band_lower_under_the_upper_tier')
          and rejected(tmut('band_upper', tier='first_order_distance_from_product'), 'band_upper_under_the_lower_tier')
          and rejected(tmut('graph_coefficients', tier='exact_first_order'), 'tier_attached_to_a_graph_coefficient')
          and rejected(tmut('dimension_2p1_constants', tier='crude_majorant'), 'tier_attached_to_a_2p1_constant')
          and rejected(tmut('w12_bound', tier='polynomial_lieb_robinson'), 'lieb_robinson_tier')
          and rejected(tmut('band_lower', source='bb1_frozen_targets'), 'hypothesis_source')
          and rejected(tmut('band_upper', source='nested_telescoping'), 'plan_route_label'),
          tiers=TIERS, rule=V['tier_rule'])

    # ---- control changed_model_relabelled (BD2 definition) ----
    MODELS = {'graph_table': 'FG(round11_two_plaquette_independent_couplings)', 'graph_enclosures': 'FG(round11_two_plaquette_independent_couplings) at l1=l2',
              'w12_bound': 'AQ_patterned_zero_selected', 'w12_evenness': 'AQ_patterned_zero_selected: F1 boxes and the limit',
              'band': 'AQ_patterned_zero_selected: F1 boxes, F2 boxes and the limit', 'formal': 'AQ_patterned_zero_selected (formal)',
              'dimension_2p1': 'declared 2+1D model'}
    ALLOWED_MODEL = {'graph_table': ('FG(round11_two_plaquette_independent_couplings)',),
                     'graph_enclosures': ('FG(round11_two_plaquette_independent_couplings) at l1=l2',),
                     'w12_bound': ('AQ_patterned_zero_selected',), 'w12_evenness': ('AQ_patterned_zero_selected: F1 boxes and the limit',),
                     'band': ('AQ_patterned_zero_selected: F1 boxes, F2 boxes and the limit',), 'formal': ('AQ_patterned_zero_selected (formal)',),
                     'dimension_2p1': ('declared 2+1D model',)}

    def validate_models(mdl, table_value=None):
        for key, allowed in ALLOWED_MODEL.items():
            require(mdl.get(key) in allowed, 'value relabelled to another model: ' + key)
        if table_value is not None:
            require(table_value == (w1t[(3, 0)], w1t[(1, 2)]), 'independent-coupling coefficients must come from the (l1,l2) table')
        return True
    check('changed_model_relabelled',
          validate_models(MODELS, (w1t[(3, 0)], w1t[(1, 2)]))
          and rejected(lambda: validate_models(dict(MODELS, graph_enclosures='AQ_patterned_zero_selected')), 'graph_value_presented_as_Z3_value')
          and rejected(lambda: validate_models(dict(MODELS, dimension_2p1='AQ_patterned_zero_selected')), 'three_plus_one_constant_under_the_2p1_label')
          and rejected(lambda: validate_models(dict(MODELS, w12_evenness='AQ_patterned_zero_selected: F2 boxes')), 'F1_value_under_F2')
          and rejected(lambda: validate_models(dict(MODELS, band='AQ_patterned_zero_selected: limit (finite-box source)')), 'finite_box_value_under_the_limit')
          and rejected(lambda: validate_models(MODELS, (Q(-187, 33696), Q(0))), 'equal_coupling_value_under_the_independent_label')
          and rejected(lambda: validate_models(MODELS, (Q(-5, 864), Q(0))), 'one_face_value_under_the_independent_label'),
          models=MODELS)

    # ---- control graph_couplings_named ----
    GRAPH_MODEL = {'model_id': V['model_id'], 'graph': 'Round11 two-plaquette (open two-square patch; 6 vertices, 7 links, 6 Gauss constraints)',
                   'terms': [['K', 'sum of the seven link Casimirs (rho=1)', '1'], ['W_1', '(1/2) Tr U_1 of square 1', '-l1'], ['W_2', '(1/2) Tr U_2 of square 2', '-l2']],
                   'kinetic': 'R11_rho1', 'couplings': 'independent (l1,l2)', 'units': 'alpha', 'sector': 'gauge-invariant',
                   'free_reference': 'rs2_series order 0 and certify(pc, 0): the same code path', 'model_is_finite_graph': True, 'transfers_to_aq': False}

    def validate_graph_model(gm):
        require(gm['model_id'] == V['model_id'] and gm['graph'].startswith('Round11 two-plaquette') and '7 links' in gm['graph'], 'graph and model id')
        require([t_[0] for t_ in gm['terms']] == ['K', 'W_1', 'W_2'] and [t_[2] for t_ in gm['terms']] == ['1', '-l1', '-l2'], 'every term named with its coefficient')
        require(gm['couplings'] == 'independent (l1,l2)', 'independent couplings')
        validate_k5(gm['kinetic'])
        require(gm['model_is_finite_graph'] is True and gm['transfers_to_aq'] is False, 'finite-graph flags')
        require(gm['free_reference'].endswith('the same code path'), 'the free reference is computed in the same code path')
        return True
    free_ref_ok = all(tables[D][nm][(0, 0)] == 0 for D in V['cutoffs'] for nm in ('W_1', 'z', 'C_shared')) and free_ok

    def gmut(**kw):
        g2 = json.loads(json.dumps(GRAPH_MODEL))
        g2.update(kw)
        return lambda: validate_graph_model(g2)
    check('graph_couplings_named',
          validate_graph_model(GRAPH_MODEL) and free_ref_ok
          and rejected(gmut(terms=GRAPH_MODEL['terms'][:2]), 'one_face_model_second_face_uncoupled')
          and rejected(gmut(couplings='equal tau_FG'), 'equal_coupling_model_under_independent_label')
          and rejected(gmut(kinetic='anisotropic_rho2'), 'shared_link_rho2')
          and rejected(gmut(kinetic='independent_rotor'), 'independent_rotor_kinetic')
          and rejected(gmut(model_id='AQ_patterned_zero_selected'), 'aq_model_id')
          and rejected(gmut(transfers_to_aq=True), 'transfers_to_aq_true')
          and rejected(gmut(free_reference='imported from the AZ2 gate'), 'free_reference_from_another_path'),
          model=GRAPH_MODEL, free_reference={'W_1': '0', 'z': '0', 'C_shared': '0'})

    # ---- control parameters_declare_metric_weights_window (BD2 definition) ----
    def validate_params(par):
        for key in ('metric', 'weights', 'window', 'clock'):
            require(isinstance(par.get(key), str) and par[key].strip(), 'parameters.' + key + ' must be declared')
        for key in ('weights', 'window', 'clock'):
            m_na = re.match(r'^not applicable \(([^()]{3,})\)', par[key])
            require(m_na is not None, 'parameters.' + key + ": 'not applicable' needs its reason")
        require('d_X' not in par and 'N_0' not in par, 'd_X and N_0 do not apply')
        return True
    par0 = V['par']
    check('parameters_declare_metric_weights_window',
          validate_params(par0)
          and rejected(lambda: validate_params({k: v for k, v in par0.items() if k != 'window'}), 'window_field_absent')
          and rejected(lambda: validate_params(dict(par0, weights='not applicable')), 'not_applicable_without_reason')
          and rejected(lambda: validate_params(dict(par0, N_0='2')), 'N_0_declared'),
          metric=par0['metric'], weights=par0['weights'], window=par0['window'], clock=par0['clock'])

    # ---- control exact_arithmetic_admission ----
    check('exact_arithmetic_admission',
          rat('7/124416') == formal and isinstance(certs[(8, Q(1, 10))]['z_lo'], Q) and isinstance(cap, Q)
          and rejected(lambda: rat(7 / 124416), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('nan'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator')
          and rejected(lambda: rat(to_dec(certs[(8, Q(1, 10))]['zR'])), 'decimal_proposal_value_as_admission'),
          arithmetic='fractions.Fraction throughout; decimal only proposes the Ritz vector; square roots by integer isqrt with upward rounding; exp(3/32) by a '
                     'directed series bracket; exports rounded outward')

    # ---- claim flags ----
    FLAGS = {'model_is_finite_graph': True, 'transfers_to_aq': False, 'graph_sign_certified': True, 'z3_1x2_formal_only': True, 'electric_band_claimed': True,
             'area_law_claimed': False, 'uniqueness_of_ground_state_claimed': False, 'rate_in_a_claimed': False, 'rate_in_N_claimed': False,
             'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False, 'uniform_wilson_claim': False,
             'resolved_interaction_shift': False, 'z3_1x2_sign_claimed': False, 'tight_electric_enclosure_claimed': False,
             'finite_volume_theorem_2p1_claimed': False, 'aq_statement_2p1_claimed': False, 'fg_coefficients_fitted': False}

    def validate_flags(fl):
        for k1, v1 in FLAGS.items():
            require(fl.get(k1) is v1, 'claim flag ' + k1 + ' changed')
        return True

    def fmut(**kw):
        f2 = dict(FLAGS)
        f2.update(kw)
        return lambda: validate_flags(f2)
    require(all(FLAGS[k1] is v1 for k1, v1 in V['gate_fields'].items() if isinstance(v1, bool)), 'preregistered gate fields exported unchanged')
    check('no_priority_or_continuum_claim',
          validate_flags(FLAGS)
          and rejected(fmut(continuum_claim=True), 'continuum_true') and rejected(fmut(scientific_priority_verified=True), 'priority_true')
          and rejected(fmut(weak_coupling_claim=True), 'weak_coupling_true') and rejected(fmut(rate_in_a_claimed=True), 'rate_in_a_true')
          and rejected(fmut(uniqueness_of_ground_state_claimed=True), 'uniqueness_true'),
          flags=FLAGS, historical_or_occult_numeric_premise=False)

    # ======================= scaling brackets per constant (preregistered) =======================
    def lower_at(t_):
        return V['band_gap'] * ((sqrt10_lo * t_ / 72 - K2p * t_ ** 2) / 2) ** 2
    ratio_lower = lower_at(tb) / lower_at(tb / 100)
    ratio_upper = (upper_coeff * tb) / (upper_coeff * tb / 100)
    ratio_formal = (formal * tb ** 2) / (formal * (tb / 100) ** 2)
    blo, bhi = V['bracket_band_lower']

    def validate_scaling(rl, ru, rf):
        require(blo <= rl <= bhi, 'band_lower scaling outside its bracket')
        require(ru == V['bracket_band_upper'], 'band_upper scaling must be exactly 100')
        require(rf == V['bracket_z3_formal'], 'z3_formal scaling must be exactly 10000')
        return True
    check('scaling_brackets_per_constant',
          validate_scaling(ratio_lower, ratio_upper, ratio_formal),
          ratios={'band_lower': dec(ratio_lower, 10), 'band_upper': s(ratio_upper), 'z3_formal': s(ratio_formal),
                  'graph_coefficients': 'not applicable (coupling-independent exact rationals)',
                  'dimension_constants': 'tau-independent (G_3(R), G_3\'(R), counts and the cap involve no tau; J/|tau| = 1)'},
          brackets=V['scaling_brackets'],
          note="K_2' is the cap value, which bounds every smaller |tau| (AY2 gate), so the tau/100 lower end uses the same constant")

    # ======================= error ledger (preregistered terms) =======================
    ERROR_LEDGER = {
        'graph_truncation_zero': {'value': '0', 'reason': 'psi_mn lies in P_(m+n) inside P_6; K psi_mn = rhs_mn is a polynomial identity (full-space resolvent); tables identical at D=6 and D=8'},
        'graph_residual_itemized': {'value': 'per point (records)', 'reason': 'five-part AZ2-type ledger at all 14 points; worst D=8 half-width %s' % records['D8_l+1/10']['z_half_width_preview']},
        'flip_parity_graph': {'value': '0', 'reason': 'exact identities: the one-link flips act by signs, commute with K and C_shared and preserve the Haar measure; parities hold coefficient by coefficient'},
        'z3_formal_coefficient': {'value': s(formal), 'reason': "formal_second_order_coefficient: no certified third-order remainder; the only certified size statement is |omega(W_{1x2})| <= K_2' tau^2 = " + s(bound_w12)},
        'band_lower_trace_duality': {'value': s(lower_lim), 'reason': 'h_R >= 6 Q_R, Fuchs-van de Graaf (pure reference), L from AY2 (limit) or the AY1 per-box ball (boxes); sqrt(10) bracket width charged in L'},
        'band_upper_energy_budget': {'value': s(upper), 'reason': 'AQ1 reset 2*7*7|tau| = 98|tau| (F2: AY1 gate item (1)); passed to the limit by lower semicontinuity'},
        'cutoff_monotone_passage': {'value': 'not_applicable', 'reason': 'no numeric cost: omega(h_R) is the monotone limit of Tr(rho h_R Q_L); the passage is exact (monotone convergence and lower semicontinuity)'},
        'dimension_recount': {'value': 'exp(3/32) bracket width ' + dec(e_hi - e_lo, 3), 'reason': 'directed rational enclosure of e^{3/32} (25-term series with geometric tail, outward to 10^-40); counts exact'},
        'arithmetic': {'value': 'charged', 'reason': 'exact Fractions; directed square roots (isqrt, upward); exported ends rounded outward to 10^-45; sqrt(10) from the AY2 gate bracket'}}
    check('error_ledger_itemized',
          list(ERROR_LEDGER) == V['error_terms'] and all(r_['reason'] for r_ in ERROR_LEDGER.values()),
          ledger=ERROR_LEDGER, rule=V['error_terms_rule'])

    # ======================= verdict and the acceptance rule =======================
    graph_ok = same and hf_ok and all(parity_table_ok(T8[n_], r_) for n_, r_ in PARITY_RULES.items()) and zero_trunc
    orders_complete = all(len(T8[nm]) == len(table_keys(order)) for nm in ('W_1', 'z', 'C_shared')) and V['cutoffs'] == [6, 8]
    certified_all = all(records[point_key(*k)]['z_sign_certified'] is True for k in grid_pts) and nest_ok
    verdict = forward_verdict(graph_ok and certified_all, band_ok and validate_band_rows(BAND_ROWS), orders_complete, width_met,
                              any(r_['family'] == 'limit of the named constructions' for r_ in BAND_ROWS), dim_ok, len(W12_BOUND_ROWS) == 6,
                              validate_obligations(OBLIGATIONS), False)

    def validate_verdict(reported, *args):
        require(reported == forward_verdict(*args), 'reported verdict differs from the contract acceptance rule')
        return True
    check('insufficient_verdict_retained',
          verdict == 'accepted_within_scope'
          and forward_verdict(True, True, True, False, True, True, True, True, False) == 'limited'
          and forward_verdict(True, True, True, True, False, True, True, True, False) == 'limited'
          and forward_verdict(False, True, True, True, True, True, True, True, False) == 'insufficient'
          and rejected(lambda: validate_verdict('accepted_within_scope', True, True, True, False, True, True, True, True, False), 'missed_width_target_relabelled_accepted')
          and rejected(lambda: validate_verdict('accepted_within_scope', True, True, True, True, False, True, True, True, False), 'band_for_finite_boxes_only_relabelled_accepted')
          and rejected(lambda: validate_verdict('limited', False, True, True, True, True, True, True, True, False), 'failed_graph_algebra_relabelled_limited')
          and rejected(lambda: validate_verdict('accepted_within_scope', True, True, True, True, True, False, True, True, False), 'incomplete_2p1_constants_relabelled_accepted'),
          rule='insufficient if the graph algebra or the band cannot be established; limited if a graph order or cutoff is missing, an enclosure misses the width target, '
               'the band holds only for finite boxes or the 2+1D constants are incomplete; otherwise accepted_within_scope',
          acceptance_clauses=V['acceptance'], retuning='the grid, cutoffs, target and tau are read from the contract and never changed')


    # ======================= contract wording defects (non-blocking), each a verified fact about the frozen text =======================
    defects = []
    if V['model_id'].startswith('FG(') and 'zero-selected patterned family' in V['model'] and 're-instantiated in 2+1 dimensions' in V['model']:
        defects.append({'id': 'W1', 'field': 'preregistration.model_id, model_is_finite_graph', 'defect': 'the single model id and the finite-graph flag name only the graph model of items 1-2, '
                        'while items 3-5 concern the zero-selected Z^3 family and the declared 2+1D model; every value here carries its own model label'})
    if V['selected_triple'] == ['0', '0', '0']:
        defects.append({'id': 'W2', 'field': 'preregistration.selected_triple_alpha_units', 'defect': 'the zero triple belongs to the Z^3 family; the graph has no selected faces'})
    if 'a certified sign of the Z^3 1x2 loop (a uniform fourth-order remainder)' in V['required'][5] and 'F2 boxes are not claimed' in V['control_semantics']['evenness_from_flip']:
        defects.append({'id': 'W3', 'field': 'required[5]', 'defect': "'a uniform fourth-order remainder' presupposes evenness, which is admitted for F1 boxes and the limit only; "
                        'for F2 boxes a third-order remainder would be needed; recorded so in the obligation row'})
    if 'three faces per site' in V['dimension_2p1']:
        defects.append({'id': 'W4', 'field': 'parameters.dimension_2p1', 'defect': "'three faces per site': each site anchors one face and lies in three owner sets; read as the number of "
                        'faces (interaction terms) whose owner set contains the site, which is what the per-site sum uses'})
    if V['scaling_brackets']['dimension_constants'] == 'tau-independent':
        defects.append({'id': 'W5', 'field': 'preregistration.scaling_brackets_per_constant.dimension_constants', 'defect': "'tau-independent' holds for G_3(R), G_3'(R), the counts and the cap; "
                        'the per-site sum itself is J = |tau| (linear); its ratio J/|tau| = 1 is what is tau-independent'})
    if 'exact_first_order (the inherited AY1 constant)' in V['control_semantics']['tier_mixing_rejected']:
        defects.append({'id': 'W6', 'field': 'new_control_semantics.tier_mixing_rejected', 'defect': "the AY1 gate and report call K_2' a tier-(ii) constant; the BD2 tier name "
                        'exact_first_order is used for the same constant (AV1 tier (ii) = exact first-order coefficient with the self-consistent AM2 remainder)'})
    terms_neg = V['terms'][1]['coefficient'] == '-l1' and V['terms'][2]['coefficient'] == '-l2'
    if terms_neg:
        defects.append({'id': 'W7', 'field': 'parameters.hamiltonian_terms', 'defect': 'the Round11 solver API restricts lambda >= 0; the negative grid points and negative couplings lie outside it; '
                        'the certificates and the perturbation theory need no sign (||x||, ||y|| <= 1)'})
    check('contract_wording_defects_recorded', len(defects) == 7 and terms_neg, defects=defects, blocking=False)

    # ======================= report: template once, phrase scan, placeholder spans, exact values, map =======================
    report_text = (BASE / 'report.md').read_text(encoding='utf-8')
    sentence = V['sentence']
    forbidden_all = ROUND_FORBIDDEN + V['forbidden']
    z_d8 = records['D8_l+1/10']['z_enclosure']
    z_d6 = records['D6_l+1/10']['z_enclosure']
    required_values = ['7/216', '-349/303264', '1/48', '-5/4608', '-49/438048', '1/6', '1/4212', '-5/864', '1/24', '-7997/3504384', '7/124416',
                       '1/31104', '1/41472', '7/144', '1/3456', s(K2p), s(bound_w12), s(L_ay2), s(lower_lim), s(upper), s(cap), s(e_lo), s(e_hi),
                       '1/10000000000000000', z_d8[0], z_d8[1], z_d6[0], z_d6[1]]
    headline_texts = [
        'On the Round11 two-plaquette graph H_FG(l1,l2) = K - l1 W_1 - l2 W_2 (alpha units, independent couplings) the exact coefficients of <W_1>, <z> and <C_shared> through total order 4 are identical at D=6 and D=8 with zero truncation error.',
        '<W_1> is odd in l1 and even in l2, <z> is odd in each coupling and <C_shared> is even in each, by the one-link centre flips of a non-shared link of face 1 and of face 2.',
        'At l1=l2 on the AZ2 grid <z> is enclosed with a positive certified sign at D=6 and D=8, the D=8 enclosure inside the D=6 one, and the D=8 relative width is below 1/10^16.',
        'In the zero-selected SU(2) family the 1x2 Wilson mean has first-order coefficient 0 in every box, obeys |omega(W_{1x2})| <= K_2\' tau^2 at both signs for every box of F1 and F2 and for the limit of the named constructions, and is even in tau in every F1 box and for the limit.',
        'Its second-order coefficient 7/124416 is a formal_second_order_coefficient only: no sign and no certified remainder.',
        'The electric energy on R lies in [(3/2) L^2, 98|tau|] at both signs for every F1 and F2 box and for the limit, with L the AY2/AY1 lower distance.',
        'The 2+1D recount gives p=3, J=|tau|, termination order 6, G_3(R)=9 e^{3/32}, G_3\'(R)=118 e^{3/32} and a directed cap; no 2+1D finite-volume theorem is claimed.']
    verdict_line = (verdict + " (forward half of a single+skeptic loop; admission requires the skeptic's replay from the contract alone and its review); "
                    'sub-labels sign_certified_finite_graph, transfer_to_named_model, obstruction_recorded, static_not_dynamic')
    exported_texts = headline_texts + [verdict_line] + [r_['missing_premise'] for r_ in OBLIGATIONS] + V['claim_exclusions'] + V['prereg_exclusions'] + [d_['defect'] for d_ in defects]

    def scan_report(text, texts):
        require(text.count(sentence) == 1, 'the mandatory template must appear exactly once as one unbroken span')
        hits = affirmative(phrase_hits(text, forbidden_all, sentence)) + affirmative(phrase_hits('. '.join(texts), forbidden_all, sentence))
        require(not hits, 'affirmative forbidden phrasing: ' + (hits[0]['phrase'] if hits else ''))
        for val in required_values:
            require(val in text, 'report does not carry the exact value ' + val[:40])
        for fld in V['gate_fields']:
            require(fld in text, 'gate field not named in the report: ' + fld)
        require(SCRATCH in text and HUMAN_AUTHOR in text and 'AI-assisted' in text, 'author, AI assistance and scratch disclosure')
        return True

    def scan_placeholders(text, texts):
        require(not placeholder_spans(text), 'placeholder span in the report: ' + (placeholder_spans(text) or [''])[0])
        require(not any(placeholder_spans(t_) for t_ in texts), 'placeholder span in an exported text')
        require(not any(placeholder_spans(t_) for t_ in all_strings(c)), 'placeholder span in the contract')
        return True
    check('negation_aware_phrase_scan',
          scan_report(report_text, exported_texts)
          and not affirmative(phrase_hits('This packet is not the thermodynamic limit and makes no string tension statement.', forbidden_all))
          and rejected(lambda: scan_report(report_text + '\nThe limit of the named constructions is the thermodynamic limit.\n', exported_texts), 'affirmative_thermodynamic_limit')
          and rejected(lambda: scan_report(report_text + '\nThe positive <z> confirms an area law.\n', exported_texts), 'affirmative_confirms')
          and rejected(lambda: scan_report(report_text, exported_texts + ['The 1x2 ratio gives the string tension.']), 'affirmative_string_tension_in_results')
          and rejected(lambda: scan_report(report_text.replace(sentence, sentence.replace('not an area law, ', '')), exported_texts), 'mandatory_template_altered')
          and rejected(lambda: scan_report(report_text + '\n' + sentence + '\n', exported_texts), 'mandatory_template_quoted_twice'),
          forbidden=len(forbidden_all), template_removed_as_one_literal=True, negation_frame=NEGATION.pattern,
          scanned=['report.md', 'exported headline, verdict, obligation, exclusion and defect texts'])
    check('placeholder_span_rejected',
          scan_placeholders(report_text, exported_texts)
          and rejected(lambda: scan_placeholders(report_text + '\nvalue <insert the constant here>\n', exported_texts), 'placeholder_with_whitespace')
          and rejected(lambda: scan_placeholders(report_text, exported_texts + ['the tier is <exact|crude>']), 'placeholder_with_vertical_bar')
          and rejected(lambda: scan_placeholders(report_text + '\n<e.g.K_2>\n', exported_texts), 'placeholder_with_e_g'),
          rule="an angle-bracket span (not an inequality '<=') containing whitespace, a vertical bar or 'e.g.' is rejected; spans like <z> are expectation brackets",
          scanned=['report.md', 'exported texts', 'every contract string'])

    def map_rows(text):
        sec = text.split('## 13. Item and control map', 1)
        require(len(sec) == 2, 'map section 13 missing')
        return [ln for ln in sec[1].split('\n## ', 1)[0].splitlines() if ln.startswith('| ')]

    def validate_map(rows):
        miss_c = [cid for cid in V['controls'] if not any(r1.startswith('| `' + cid + '` |') for r1 in rows)]
        miss_i = [k for k in range(1, 8) if not any(r1.startswith('| item %d ' % k) for r1 in rows)]
        require(not miss_c and not miss_i, 'map lacks rows for ' + ','.join(miss_c + ['item %d' % k for k in miss_i]))
        return True
    mrows = map_rows(report_text)
    check('report_item_and_control_map',
          validate_map(mrows)
          and rejected(lambda: validate_map([r1 for r1 in mrows if not r1.startswith('| `dimension_recount` |')]), 'control_row_removed_from_map')
          and rejected(lambda: validate_map([r1 for r1 in mrows if not r1.startswith('| item 4 ')]), 'item_4_row_removed_from_map'),
          controls_in_map=len(V['controls']), items_in_map=7, map_section='report.md section 13')

    # ======================= no solver / numerical library import =======================
    src_lines = [ln.strip() for ln in own_src.splitlines()]
    banned = ['import ' + 'numpy', 'from ' + 'numpy', 'import ' + 'scipy', 'from ' + 'scipy', 'import ' + 'flint', 'from ' + 'flint',
              'import ' + 'two_plaquette', 'from ' + 'two_plaquette', 'import ' + 'mpmath', 'from ' + 'research', 'import ' + 'check', 'import ' + 'runpy']
    check('no_repository_or_numerical_import',
          not any(ln.startswith(b) for ln in src_lines for b in banned),
          banned_imports_absent=True, note='the AZ2 checker and the Round11 solver are premises read as text; nothing is imported from the repository')

    # ======================= packet, headline and coherent tampering =======================
    grid_keys = [point_key(*k) for k in grid_pts]
    headline = {
        'graph_model': 'H_FG(l1,l2) = K - l1 W_1 - l2 W_2 in alpha units on the Round11 two-plaquette graph (K the seven link Casimirs, rho=1; gauge-invariant sector)',
        'coefficient_tables_nonzero': {'W_1': {k: v for k, v in tab_str(w1t).items() if v != '0'}, 'z': {k: v for k, v in tab_str(zt).items() if v != '0'},
                                       'C_shared': {k: v for k, v in tab_str(cst).items() if v != '0'}},
        'coefficient_index': '(m,n) = power of l1, power of l2; total order m+n <= 4; identical at D=6 and D=8; truncation error 0',
        'second_order_at_l1_eq_l2': {'z': s(diag_z[2]), 'C_shared': s(diag_cs[2])},
        'parities': {'W_1': 'odd in l1, even in l2', 'z': 'odd in l1, odd in l2', 'C_shared': 'even in l1, even in l2'},
        'z_enclosures': {k: records[k]['z_enclosure'] for k in grid_keys},
        'z_enclosures_preview': {k: records[k]['z_enclosure_preview'] for k in grid_keys},
        'z_relative_width_preview': {k: records[k]['relative_width_preview'] for k in grid_keys},
        'z_sign_certified_all_grid_points': all(records[k]['z_sign_certified'] for k in grid_keys),
        'target': s(V['target']), 'target_comparator': V['target_comparator'], 'target_met': width_met, 'worst_D8_relative_width_preview': dec(worst8, 8),
        'z3_1x2': {'first_order_coefficient': '0', 'bound': s(bound_w12), 'K2prime': s(K2p), 'tier': 'exact_first_order', 'evenness': 'F1 boxes and the limit',
                   'formal_second_order_coefficient': s(formal), 'label': 'formal_second_order_coefficient'},
        'electric_band': {'tau': s(tb), 'lower': s(lower_lim), 'upper': s(upper), 'lower_tier': 'first_order_distance_from_product', 'upper_tier': 'crude_majorant',
                          'formal_second_order_total_per_tau2': s(formal_h), 'scope': V['gate_fields']['electric_band_scope']},
        'dimension_2p1': {'p': p2, 'J': '|tau|', 'faces_per_site': 3, 'termination_order': 2 * p2, 'numerators': [s(x) for x in nums3],
                          'exp_3_over_32': [s(e_lo), s(e_hi)], 'G3_R': [s(G3[0]), s(G3[1])], 'G3prime_R': [s(G3p[0]), s(G3p[1])], 'cap_directed_lower': s(cap)},
        'statements': headline_texts}
    LABEL = {'model_id': V['model_id'], 'graph': GRAPH_MODEL['graph'], 'model_is_finite_graph': True, 'transfers_to_aq': False,
             'other_models': {'items_3_4': 'AQ_patterned_zero_selected (F1, F2 boxes and the limit of the named constructions)', 'item_5': DIM['model']},
             'sub_labels': ['sign_certified_finite_graph', 'transfer_to_named_model', 'obstruction_recorded', 'static_not_dynamic'], 'tiers': TIERS}
    require(all(x in V['sub_labels'] for x in LABEL['sub_labels']), 'sub-labels from the allowed list')
    gate_fields = dict(V['gate_fields'])
    packet = {
        'loop': 'BD2', 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'contribution_alias': 'HNM-BD2-F forward applications II: independent-coupling two-plaquette coefficients and certified 1x2 signs, the Z^3 1x2 loop and '
                              'electric-energy band on R, and the 2+1D AM2 recount',
        'ai_assistance': 'AI-assisted forward production (a Claude model agent); correlated model-agent work, not independent human review',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha, 'scratch_folder': SCRATCH,
        'model': {'statement': V['model'], 'graph': GRAPH_MODEL, 'z3': 'AQ_patterned_zero_selected, tau=+-' + s(V['tau_z3']) + ', F1 and F2 boxes N>=2 and the limit of the named constructions',
                  'dimension_2p1': DIM['model'], 'clock': V['par']['clock']},
        'headline': headline, 'label': LABEL, 'points': records, 'coefficient_tables': {'W_1': tab_str(w1t), 'z': tab_str(zt), 'C_shared': tab_str(cst), 'E_0': tab_str(Et)},
        'z3_1x2': {'formal': FORMAL, 'bound_rows': W12_BOUND_ROWS, 'evenness': EVEN, 'K2prime_items_over_tau2': {k: s(v / t8 ** 2) for k, v in K2_items.items()}},
        'electric_band': {'rows': BAND_ROWS, 'route': {k: (s(v) if isinstance(v, Q) else v) for k, v in BAND_ROUTE.items()}, 'per_link_formal': per_link_rows},
        'dimension_2p1': DIM, 'transfers': TRANSFERS, 'obligations': OBLIGATIONS, 'error_terms_itemized': ERROR_LEDGER,
        'mandatory_sentence': sentence, 'gate_fields': gate_fields,
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions'],
                       'additional': ['no statement about the AQ construction from the graph (transfers_to_aq false)', 'no dynamical or mass-gap reading of a static mean',
                                      'no cutoff beyond D=8', 'no F2 evenness', 'no 2+1D finite-volume, AQ, node or dictionary statement']},
        'contract_wording_defects': defects,
        'routes_executed': ['forward: bivariate Rayleigh-Schroedinger series in the full graph space (polynomial resolvent, zero omitted residual) at D=6 and D=8',
                            'forward: exact AZ2-type Ritz certificates of the l1=l2 ground state at 14 points with the complete shell-(D+1) residual and the z observable step',
                            'forward: fine-lattice enumeration of the I1 blocking, the rectangle, the flip set and the face incidences',
                            "forward: K_2' re-derived from the AY1 F14 items; band endpoints from the AY2/AY1 distance and the AQ1 reset",
                            'forward: 2+1D recount of the AM2 counting at p=3 with a directed exp(3/32) bracket'],
        'routes_not_executed': ["skeptic replay from the contract alone and review (single+skeptic; outside this producer)"],
        'protocol_steps_outside_check_py': {'freeze_and_byte_identical_replays': 'research/round33/tools/freeze.py', 'phrase_scan_cli': 'research/round33/tools/phrase_scan.py'},
        'proposed_forward_verdict': verdict_line,
    }
    packet.update(FLAGS)

    def packet_hash(pk):
        body = {k1: v1 for k1, v1 in pk.items() if k1 != 'packet_sha256'}
        return sha_bytes(json.dumps(body, sort_keys=True).encode('utf-8'))

    def validate_packet(pk, inv):
        require(pk.get('packet_sha256') == packet_hash(pk), 'packet hash mismatch')
        ids = {ch['id']: ch for ch in pk['checks']}
        for cid in V['controls']:
            if cid == 'coherent_evidence_tampering':
                continue
            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)
        validate_flags({k1: pk[k1] for k1 in FLAGS})
        validate_inventory(inv)
        require(pk['contract_sha256'] == contract_digest, 'contract hash changed')
        hd = pk['headline']
        for key in grid_keys:
            D_, t_ = [(k[0], k[1]) for k in grid_pts if point_key(*k) == key][0]
            exact = [s(certs[(D_, t_)]['z_lo_out']), s(certs[(D_, t_)]['z_hi_out'])]
            require(hd['z_enclosures'][key] == exact == pk['points'][key]['z_enclosure'], 'z enclosure differs from recomputation: ' + key)
            require(set(pk['points'][key]['ledger']['a_per_link_representation_tail']) == set(LINKS), 'per-link ledger rows changed')
        require(pk['coefficient_tables'] == {'W_1': tab_str(w1t), 'z': tab_str(zt), 'C_shared': tab_str(cst), 'E_0': tab_str(Et)}, 'coefficient table changed')
        require(hd['z3_1x2']['bound'] == s(bound_w12) and hd['z3_1x2']['K2prime'] == s(K2p), "W_{1x2} bound or K_2' changed")
        validate_formal(pk['z3_1x2']['formal'])
        require(pk['z3_1x2']['formal']['value'] == s(formal), 'formal coefficient changed')
        require(hd['electric_band']['lower'] == s(lower_lim) and hd['electric_band']['upper'] == s(upper), 'band endpoints changed')
        validate_band_rows(pk['electric_band']['rows'])
        require([r_['lower'] for r_ in pk['electric_band']['rows']] == [s(lower_lim)] * 6, 'band lower endpoints changed')
        validate_dim(pk['dimension_2p1'])
        require(hd['dimension_2p1']['cap_directed_lower'] == s(cap) == pk['dimension_2p1']['cap_directed_lower'], '2+1D cap changed')
        require(pk['gate_fields'] == V['gate_fields'], 'gate fields changed')
        validate_obligations(pk['obligations'])
        require(pk['proposed_forward_verdict'] == verdict_line, 'verdict changed')
        require(pk['mandatory_sentence'] == sentence, 'mandatory sentence changed')
        return True

    base_packet = dict(packet)
    base_packet['checks'] = [dict(ch) for ch in CHECKS]
    base_packet['packet_sha256'] = packet_hash(base_packet)

    def tamper(fn):
        def run():
            pk = json.loads(json.dumps(base_packet))
            inv = dict(inventory)
            fn(pk, inv)
            pk['packet_sha256'] = packet_hash(pk)
            return validate_packet(pk, inv)
        return run

    def t_control(pk, inv):
        for ch in pk['checks']:
            if ch['id'] == 'unbounded_observable_handled':
                ch['passed'] = False

    def t_zlower(pk, inv):
        pk['points']['D8_l+1/10']['z_enclosure'][0] = s(Q(pk['points']['D8_l+1/10']['z_enclosure'][0]) + Q(1, 10 ** 30))
        pk['headline']['z_enclosures']['D8_l+1/10'] = pk['points']['D8_l+1/10']['z_enclosure']

    def t_coef(pk, inv):
        pk['coefficient_tables']['z']['1,1'] = '7/215'

    def t_bound(pk, inv):
        pk['headline']['z3_1x2']['bound'] = s(bound_w12 / 4)

    def t_formal(pk, inv):
        pk['z3_1x2']['formal']['label'] = 'certified_second_order_value'

    def t_band(pk, inv):
        for r_ in pk['electric_band']['rows']:
            r_['lower'] = s(Q(7, 144) * tb ** 2)
        pk['headline']['electric_band']['lower'] = s(Q(7, 144) * tb ** 2)

    def t_cap(pk, inv):
        pk['dimension_2p1']['p'] = 4

    def t_snapshot(pk, inv):
        inv.pop(P_AZ2_CHECK)

    def t_contract(pk, inv):
        inv[CONTRACT_REL] = '0' * 64
        pk['contract_sha256'] = '0' * 64

    def t_gate(pk, inv):
        pk['gate_fields']['area_law_claimed'] = True
        pk['area_law_claimed'] = True

    def t_verdict(pk, inv):
        pk['proposed_forward_verdict'] = 'limited ' + pk['proposed_forward_verdict']

    def t_sentence(pk, inv):
        pk['mandatory_sentence'] = pk['mandatory_sentence'].replace('not an area law, ', '')

    def t_obligation(pk, inv):
        pk['obligations'] = pk['obligations'][1:]
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_zlower), 'z_enclosure_lower_end_raised_hash_rebound')
          and rejected(tamper(t_coef), 'z_coefficient_changed_hash_rebound')
          and rejected(tamper(t_bound), 'W12_bound_quartered_hash_rebound')
          and rejected(tamper(t_formal), 'formal_coefficient_relabelled_hash_rebound')
          and rejected(tamper(t_band), 'band_lower_replaced_by_the_formal_value_hash_rebound')
          and rejected(tamper(t_cap), 'three_plus_one_support_in_2p1_hash_rebound')
          and rejected(tamper(t_snapshot), 'az2_checker_snapshot_removed_hash_rebound')
          and rejected(tamper(t_contract), 'contract_hash_replaced_hash_rebound')
          and rejected(tamper(t_gate), 'area_law_gate_field_true_hash_rebound')
          and rejected(tamper(t_verdict), 'verdict_changed_hash_rebound')
          and rejected(tamper(t_sentence), 'mandatory_sentence_changed_hash_rebound')
          and rejected(tamper(t_obligation), 'obligation_row_removed_hash_rebound'))

    spans_in_results = [t_ for t_ in all_strings(dict(packet, checks=CHECKS)) if placeholder_spans(t_)]
    require(not spans_in_results, 'placeholder span in results: ' + (spans_in_results or [''])[0][:80])
    ids = [ch['id'] for ch in CHECKS]
    missing_c = [cid for cid in V['controls'] if cid not in ids]
    require(not missing_c, 'contract controls without a check: ' + ','.join(missing_c))
    positive_only = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch.get('rejected_mutations')]
    require(not positive_only, 'contract controls without a damaging mutation: ' + ','.join(positive_only))
    require(not PENDING, 'rejected mutations not attached to a check')
    packet['checks'] = CHECKS
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['controls_with_damaging_mutations'] = sum(1 for ch in CHECKS if ch['id'] in V['controls'] and ch.get('rejected_mutations'))
    packet['rejected_mutations_in_control_checks'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS if ch['id'] in V['controls'])
    packet['rejected_mutation_total'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS)
    packet['check_count'] = len(CHECKS)
    return packet


def float_free(obj):
    if isinstance(obj, float):
        return False
    if isinstance(obj, dict):
        return all(float_free(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(float_free(v) for v in obj)
    return True


def main():
    ap = argparse.ArgumentParser(description='BD2 forward exact checker')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    require(out.is_absolute(), 'absolute output directory required')
    out = out.resolve()
    require(not out.exists(), 'fresh (non-existent) output directory required')
    require(ROOT not in out.parents and out != ROOT, 'output directory must be outside the checkout')
    check_sha = sha(BASE / 'check.py')   # recorded before any evaluation
    result = compute(check_sha)
    require(float_free(result), 'floating-point value in results')
    out.mkdir(parents=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    sources = {}
    for p in sorted(BASE.rglob('*')):
        rel = p.relative_to(BASE)
        if p.is_file() and rel.parts[0] != 'output' and (rel.parts[0] == 'inputs' or p.name in ('check.py', 'report.md')):
            sources[rel.as_posix()] = sha(p)
    manifest = {'loop': 'BD2', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    hd = result['headline']
    print(json.dumps({'loop': 'BD2', 'direction': 'forward', 'checks': len(result['checks']),
                      'z_D8_l+1/10': hd['z_enclosures_preview']['D8_l+1/10'], 'band': [hd['electric_band']['lower'], hd['electric_band']['upper']],
                      'verdict': result['proposed_forward_verdict'].split(' ')[0]}, sort_keys=True))


if __name__ == '__main__':
    main()
