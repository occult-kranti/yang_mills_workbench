#!/usr/bin/env python3
"""HNM-BD1 reverse producer: centre-symmetry transfer of the AW1 parity theorem, the
link-flip lemma and the first-order Wilson mean across the frozen gauge-group list,
with the SU(3), SO(3) and SU(5) obstruction cells and the SU(2) area-parity corollary.

Route of computation: weyl_integration. Every Haar moment is a constant term of a
Laurent polynomial on the maximal torus (Weyl integration formula with the
Vandermonde density for SU(N), the SO(3) torus density, the binomial constant term
for U(1), direct summation for Z2). One-plaquette class functions are symmetric
Laurent polynomials; the electric operator acts on their Weyl numerators
f*a_rho (Weyl character formula, determinant ratio) as the flat torus Laplacian
shifted by |rho|^2; Rayleigh-Schroedinger inner products are constant terms.
No character table, tensor-product multiplicity or Clebsch-Gordan series is used.

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production (a
Claude model agent) under reverse premise isolation; HNM labels are project aliases.
The Weyl integration and character formulas, the Casimir eigenvalue formula, Schur's
lemma, Peter-Weyl orthogonality, Rayleigh-Schroedinger and Hellmann-Feynman
identities, Kato analytic perturbation theory and centre-flip arguments are
established mathematics; scientific priority is unverified.

Standard library only. Exact Fraction arithmetic decides every Boolean; decimal
strings are truncated previews. Every contract control is a damaging mutation whose
rejection is required; rejections and failures are explicit exceptions (never
assert), so the run and its output bytes are identical under python -O.

Usage: python3 -B research/round33/reverse/bd1/check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUTS = HERE / 'inputs'
CONTRACT_REL = 'research/round33/contracts/bd1.json'
CONTRACT_SHA256 = 'a5c8416600c49b0728fdca05cd67c3ff2e53d9fd9e146d4305abcd2da775c1fc'
AGENTS_SHA256 = '870e1a6b1ff81d6e09888d7084dada2dfdb8128048d97857d9c6b1ffce1b9285'
GATE_SHA256 = {
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/aw2-gate.json': '640a3b0a74c7fcd66318ba7ce2a60942f837ad154f157bc1d69323589b24be62',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round32/advisor/az1-gate.json': '255ce6702628b26b082ceb0e03732c87be84c9ce6315b65c9792087d0cdc03ad',
    'research/round32/advisor/az2-gate.json': 'd36d53dcad8b1d3e4789d3be76b9e491e73cc5cf2ca88f281f66fd255f98b394',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
}
AW1_GATE = 'research/round32/advisor/aw1-gate.json'
BB2_GATE = 'research/round33/advisor/bb2-gate.json'
AZ1_GATE = 'research/round32/advisor/az1-gate.json'
AW1_REVERSE_REPORT = 'research/round32/reverse/aw1/report.md'
AW1_SKEPTIC = 'research/round32/skeptic/aw1.md'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'
ROUTE = 'weyl_integration'
ROUTES_ALLOWED = ('characters', 'weyl_integration')
TIER = 'exact_first_order'
PLAN_ROUTE_LABELS = ('weighted_norm', 'analytic_disc', 'polymer_kp', 'iterated_split', 'duhamel_inner_f1', 'duhamel_inner_f2')
GROUP_ORDER = ('SU(2)', 'SU(3)', 'SU(4)', 'SU(5)', 'U(1)', 'Z2', 'SO(3)')
REQUIRED_CONTROLS = (
    'coherent_evidence_tampering', 'exact_arithmetic_admission', 'no_priority_or_continuum_claim',
    'changed_model_relabelled', 'insufficient_verdict_retained', 'placeholder_span_rejected',
    'negation_aware_phrase_scan', 'parameters_declare_metric_weights_window', 'tier_mixing_rejected',
    'frozen_convention_used', 'su2_constants_not_transferred', 'flip_criterion_central_minus_one',
    'parity_criterion_third_moment', 'moment_tables_two_routes', 'su3_obstruction_mandatory',
    'so3_obstruction_mandatory', 'flip_sets_verified', 'area_parity_scope', 'one_plaquette_model_terms',
    'no_transfer_called_prediction', 'am2_not_reinstantiated', 'su5_flip_obstruction_fourth_order')
EXPECTED_GATE_FIELDS = {
    'model_is_finite_graph': True, 'transfers_to_aq': False, 'flip_transfer_claimed': True,
    'parity_transfer_claimed': True, 'obstructions_recorded': True, 'area_parity_limit_claimed': True,
    'uniqueness_of_ground_state_claimed': False, 'rate_in_a_claimed': False, 'continuum_claim': False,
    'weak_coupling_claim': False, 'scientific_priority_verified': False}
FORBIDDEN_INPUT_PREFIXES = (
    'research/round33/forward/bd1/', 'research/round33/forward/bd2/', 'research/round33/forward/bc1/',
    'research/round33/forward/bc2/', 'research/round33/reverse/', 'research/round33/experts/',
    'research/round33/skeptic/bd', 'research/round33/skeptic/bc')
# Round33 phrase list copied from research/round33/tools/phrase_scan.py (infrastructure, not premise)
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
PLACEHOLDER = re.compile(r'<(?![=<>])([^<>=]*)(?<![-=|])>(?!=)')
PREVIEW_DIGITS = 12


# ----------------------------------------------------------------- exceptions
class Rejected(Exception):
    """A validator refused its input: the required fate of a damaging mutation."""


class ProducerError(Exception):
    """An identity required by the derivation failed; the run aborts without output."""


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
        raise Rejected('non-exact numeric input rejected')
    if isinstance(value, Q):
        return value
    if isinstance(value, int):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'[+-]?[0-9]+(/[1-9][0-9]*)?', value):
        return Q(value)
    raise Rejected('malformed rational input rejected')


def qs(x):
    return str(Q(x))


def sci(x, digits=PREVIEW_DIGITS):
    """Truncated decimal preview of an exact rational (never read by an admission)."""
    x = Q(x)
    if x == 0:
        return '0'
    sign = '-' if x < 0 else ''
    x = abs(x)
    e = len(str(x.numerator)) - len(str(x.denominator))
    if x < Q(10) ** e:
        e -= 1
    if x >= Q(10) ** (e + 1):
        e += 1
    m = x / Q(10) ** e
    digs = str((m.numerator * 10 ** (digits - 1)) // m.denominator)
    return '%s%s.%se%d' % (sign, digs[0], digs[1:], e)


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_q(rows, ncols):
    """Rank over Q by exact Gaussian elimination."""
    rows = [list(r) for r in rows if any(v != 0 for v in r)]
    rank = 0
    col = 0
    while rank < len(rows) and col < ncols:
        piv = None
        for i in range(rank, len(rows)):
            if rows[i][col] != 0:
                piv = i
                break
        if piv is None:
            col += 1
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        pv = rows[rank][col]
        rows[rank] = [v / pv for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
        col += 1
    return rank


def gf2_solve(rows, rhs, nvars):
    """Solve A x = rhs over GF(2); rows are int bitmasks. Returns (solvable, rank)."""
    piv_rows = {}
    for r, b in zip(rows, rhs):
        r_, b_ = r, b
        while r_:
            top = r_.bit_length() - 1
            if top in piv_rows:
                pr, pb = piv_rows[top]
                r_ ^= pr
                b_ ^= pb
            else:
                piv_rows[top] = (r_, b_)
                break
        if r_ == 0 and b_ == 1:
            return False, len(piv_rows)
    return True, len(piv_rows)


def gf2_rank(rows):
    return gf2_solve(rows, [0] * len(rows), 0)[1]


# ------------------------------------------------ Laurent polynomials on the torus
def padd(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + v
        if out[k] == 0:
            del out[k]
    return out


def pscale(a, s):
    s = Q(s)
    return {k: v * s for k, v in a.items() if v * s != 0}


def pmul(G, a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = G.add(ka, kb)
            out[k] = out.get(k, 0) + va * vb
    return {k: v for k, v in out.items() if v != 0}


def ppow(G, f, k):
    out = {G.zero: Q(1)}
    for _ in range(k):
        out = pmul(G, out, f)
    return out


def perm_sign(p):
    s = 1
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s = -s
    return s


class TorusSU:
    """SU(N) maximal torus: x_1..x_N with x_1...x_N=1; exponents taken modulo the diagonal."""
    kind = 'SU'

    def __init__(self, n):
        self.n = n
        self.name = 'SU(%d)' % n
        self.wilson_representation = 'fundamental'
        self.dim_fund = n
        self.weyl_order = factorial(n)
        self.zero = tuple([0] * n)
        self.rho = tuple(range(n - 1, -1, -1))
        chi, chib = {}, {}
        for i in range(n):
            chi = padd(chi, {self.norm(tuple(1 if j == i else 0 for j in range(n))): Q(1)})
            chib = padd(chib, {self.norm(tuple(-1 if j == i else 0 for j in range(n))): Q(1)})
        self.chi, self.chib = chi, chib
        self.W = pscale(padd(chi, chib), Q(1, 2 * n))
        a = {}
        for p in permutations(range(n)):
            a = padd(a, {self.norm(tuple(self.rho[p[i]] for i in range(n))): Q(perm_sign(p))})
        self.arho = a
        self.rho_sq = self.sq0(self.rho)
        self._density = None

    def norm(self, e):
        m = min(e)
        return tuple(v - m for v in e)

    def add(self, a, b):
        return self.norm(tuple(x + y for x, y in zip(a, b)))

    def neg(self, a):
        return self.norm(tuple(-x for x in a))

    def sq0(self, e):
        s = sum(e)
        return Q(sum(v * v for v in e)) - Q(s * s, self.n)

    def energy(self, mu):
        """32 C_2 with C_2 = (|lambda+rho|^2 - |rho|^2)/2 in the trace-form metric (torus Laplacian)."""
        return 16 * (self.sq0(mu) - self.rho_sq)

    def dominant(self, mu):
        return all(mu[i] > mu[i + 1] for i in range(self.n - 1))

    def label(self, mu):
        return tuple(mu[i] - self.rho[i] for i in range(self.n))

    def weyl_images(self, mu):
        out = []
        for i in range(self.n - 1):
            m = list(mu)
            m[i], m[i + 1] = m[i + 1], m[i]
            out.append((self.norm(tuple(m)), -1))
        return out

    def density(self):
        """Weyl density prod_{i!=j}(1-x_i/x_j) = |a_rho|^2 on the torus, fully expanded."""
        if self._density is None:
            d = {self.zero: Q(1)}
            for i in range(self.n):
                for j in range(self.n):
                    if i != j:
                        e = tuple(1 if k == i else (-1 if k == j else 0) for k in range(self.n))
                        d = pmul(self, d, {self.zero: Q(1), self.norm(e): Q(-1)})
            self._density = d
        return self._density

    def haar_m1(self, f):
        d = self.density()
        return sum((v * d.get(self.neg(k), 0) for k, v in f.items()), Q(0)) / self.weyl_order

    def central_minus_one_is_torus_function(self):
        # x -> -x is a function on the SU(N) torus iff (-1)^N = 1 (x_1...x_N=1 must be preserved)
        return (-1) ** self.n == 1

    def flip_sign(self, mu):
        must(self.central_minus_one_is_torus_function(), 'central -1 used on ' + self.name)
        return (-1) ** sum(mu)

    def grade(self, mu):
        return (sum(mu) - sum(self.rho)) % self.n


class TorusU1:
    kind = 'U1'
    name = 'U(1)'
    wilson_representation = 'charge 1'
    dim_fund = 1
    weyl_order = 1
    zero = (0,)
    rho = (0,)

    def __init__(self):
        self.chi = {(1,): Q(1)}
        self.chib = {(-1,): Q(1)}
        self.W = {(1,): Q(1, 2), (-1,): Q(1, 2)}
        self.arho = {(0,): Q(1)}

    def norm(self, e):
        return e

    def add(self, a, b):
        return (a[0] + b[0],)

    def neg(self, a):
        return (-a[0],)

    def energy(self, mu):
        return Q(32 * mu[0] * mu[0])

    def dominant(self, mu):
        return True

    def label(self, mu):
        return mu

    def weyl_images(self, mu):
        return []

    def haar_m1(self, f):
        return f.get((0,), Q(0))

    def central_minus_one_is_torus_function(self):
        return True

    def flip_sign(self, mu):
        return (-1) ** (mu[0] % 2)

    def grade(self, mu):
        return mu[0]


class TorusZ2:
    kind = 'Z2'
    name = 'Z2'
    wilson_representation = 'sign'
    dim_fund = 1
    weyl_order = 1
    zero = (0,)
    rho = (0,)

    def __init__(self):
        self.chi = {(1,): Q(1)}
        self.chib = {(1,): Q(1)}
        self.W = {(1,): Q(1)}
        self.arho = {(0,): Q(1)}

    def norm(self, e):
        return (e[0] % 2,)

    def add(self, a, b):
        return ((a[0] + b[0]) % 2,)

    def neg(self, a):
        return ((-a[0]) % 2,)

    def energy(self, mu):
        return Q(32 * (mu[0] % 2))

    def dominant(self, mu):
        return True

    def label(self, mu):
        return mu

    def weyl_images(self, mu):
        return []

    def haar_m1(self, f):
        # direct summation over the two group elements g=+1,-1: f(g)=sum_n c_n g^n
        vals = [sum((v * (g ** k[0]) for k, v in f.items()), Q(0)) for g in (1, -1)]
        return (vals[0] + vals[1]) / 2

    def central_minus_one_is_torus_function(self):
        return True

    def flip_sign(self, mu):
        return (-1) ** (mu[0] % 2)

    def grade(self, mu):
        return mu[0] % 2


class TorusSO3:
    """SO(3) maximal torus z=e^{i theta}; rho-shifted Weyl numerator a_rho=1-z^{-1}."""
    kind = 'SO3'
    name = 'SO(3)'
    wilson_representation = 'vector'
    dim_fund = 3
    weyl_order = 2
    zero = (0,)
    rho = (0,)

    def __init__(self):
        self.chi = {(1,): Q(1), (0,): Q(1), (-1,): Q(1)}
        self.chib = dict(self.chi)
        self.W = pscale(self.chi, Q(1, 3))
        self.arho = {(0,): Q(1), (-1,): Q(-1)}

    def norm(self, e):
        return e

    def add(self, a, b):
        return (a[0] + b[0],)

    def neg(self, a):
        return (-a[0],)

    def energy(self, mu):
        k = mu[0]
        return Q(32 * k * (k + 1))

    def dominant(self, mu):
        return mu[0] >= 0

    def label(self, mu):
        return mu

    def weyl_images(self, mu):
        return [((-1 - mu[0],), -1)]

    def haar_m1(self, f):
        # SO(3) torus formula: (1/2) CT[f(z)(2-z-z^{-1})]
        dens = {(0,): Q(2), (1,): Q(-1), (-1,): Q(-1)}
        return sum((v * dens.get((-k[0],), 0) for k, v in f.items()), Q(0)) / 2

    def central_minus_one_is_torus_function(self):
        return False

    def flip_sign(self, mu):
        raise ProducerError('SO(3) has no central element acting as -1')

    def grade(self, mu):
        return 0


def make_groups():
    return {'SU(2)': TorusSU(2), 'SU(3)': TorusSU(3), 'SU(4)': TorusSU(4), 'SU(5)': TorusSU(5),
            'U(1)': TorusU1(), 'Z2': TorusZ2(), 'SO(3)': TorusSO3()}


# ------------------------------------------------ Weyl numerators, inner products, Haar
def numer(G, f):
    return pmul(G, f, G.arho)


def ip(G, A, B):
    """(f,g) = (1/|W|) CT[conj(f a_rho) (g a_rho)] = (1/|W|) sum_mu A_mu B_mu (real coefficients)."""
    if len(A) > len(B):
        A, B = B, A
    return sum((v * B.get(k, 0) for k, v in A.items()), Q(0)) / G.weyl_order


def haar_m2(G, f):
    return ip(G, G.arho, numer(G, f))


def haar_moment_m1(G, k):
    if G.kind == 'U1':
        # direct integration of cos^k: binomial constant term 2^-k sum_j C(k,j) [2j=k]
        return Q(sum(comb(k, j) for j in range(k + 1) if 2 * j == k), 2 ** k)
    return G.haar_m1(ppow(G, G.W, k))


def antisymmetric(G, A):
    for mu, v in A.items():
        for img, s in G.weyl_images(mu):
            if A.get(img, 0) != s * v:
                return False
        if G.kind == 'SU' and len(set(mu)) != len(mu):
            return False
    return True


def decompose(G, f):
    """Weyl character formula (determinant ratio): coefficients of f on the Weyl characters."""
    A = numer(G, f)
    must(antisymmetric(G, A), 'numerator not antisymmetric for ' + G.name)
    return {G.label(mu): v for mu, v in sorted(A.items()) if G.dominant(mu)}


def resolvent(G, A):
    """R = Q H_0^{-1} Q on numerators: remove the vacuum component, divide by torus energies."""
    c = ip(G, G.arho, A)
    A = padd(A, pscale(G.arho, -c))
    out = {}
    for mu, v in A.items():
        e = G.energy(mu)
        must(e != 0, 'vacuum-energy monomial survived the projection in ' + G.name)
        out[mu] = v / e
    return out


def apply_h0(G, A):
    return {mu: v * G.energy(mu) for mu, v in A.items() if v * G.energy(mu) != 0}


def rayleigh_schroedinger(G, order):
    """H(tau)=H_0+tau V, V=-(1/3)W, intermediate normalization; psi_n numerators and E_n."""
    vac = dict(G.arho)
    psi = [vac]
    E = [Q(0)]
    V = pscale(G.W, Q(-1, 3))
    for n in range(1, order + 1):
        E.append(ip(G, vac, pmul(G, V, psi[n - 1])))
        src = pscale(pmul(G, V, psi[n - 1]), Q(-1))
        for k in range(1, n):
            src = padd(src, pscale(psi[n - k], E[k]))
        psi.append(resolvent(G, src))
        must(antisymmetric(G, psi[n]), 'RS vector not antisymmetric')
    E.append(ip(G, vac, pmul(G, V, psi[order])))
    return psi, E


def expectation_series(G, psi, obs_numer_fn, order):
    """Coefficients of (psi, O psi)/(psi, psi) for O given by its action on numerators."""
    Opsi = [obs_numer_fn(p) for p in psi[:order + 1]]
    Npol = [sum((ip(G, psi[i], Opsi[n - i]) for i in range(n + 1)), Q(0)) for n in range(order + 1)]
    Dpol = [sum((ip(G, psi[i], psi[n - i]) for i in range(n + 1)), Q(0)) for n in range(order + 1)]
    out = []
    for n in range(order + 1):
        out.append((Npol[n] - sum((out[k] * Dpol[n - k] for k in range(n)), Q(0))) / Dpol[0])
    return out


# ------------------------------------------------ Casimir normalization and centre
def casimir_of(G, f):
    """Casimir values of the Weyl characters in f (energy/32 of the dominant numerator monomials)."""
    A = numer(G, f)
    return sorted({G.energy(mu) / 32 for mu in A if G.dominant(mu)})


def elementary_symmetric(G, k):
    out = {}
    for idx in combinations(range(G.n), k):
        out = padd(out, {G.norm(tuple(1 if j in idx else 0 for j in range(G.n))): Q(1)})
    return out


def su_dominant_labels(n, top):
    """Dominant SU(n) labels lambda_1>=...>=lambda_{n-1}>=lambda_n=0 with lambda_1<=top."""
    out = []
    for lam in product(range(top + 1), repeat=n - 1):
        if all(lam[i] >= lam[i + 1] for i in range(n - 2)):
            out.append(tuple(lam) + (0,))
    return out


def su_casimir_label(G, lam):
    return G.energy(tuple(lam[i] + G.rho[i] for i in range(G.n))) / 32


def commutant_real_dimension(mats, n):
    """Real dimension of {X in M_n(C): XM=MX for all M}, matrices given as (real, imag) Fraction pairs."""
    nv = 2 * n * n
    rows = []

    def idx(part, i, j):
        return part * n * n + i * n + j
    for P, R in mats:
        for i in range(n):
            for j in range(n):
                re_row = [Q(0)] * nv
                im_row = [Q(0)] * nv
                for k in range(n):
                    # (XM)_ij = sum_k X_ik M_kj ; (MX)_ij = sum_k M_ik X_kj ; X = A + iB, M = P + iR
                    re_row[idx(0, i, k)] += P[k][j]
                    re_row[idx(1, i, k)] -= R[k][j]
                    re_row[idx(0, k, j)] -= P[i][k]
                    re_row[idx(1, k, j)] += R[i][k]
                    im_row[idx(0, i, k)] += R[k][j]
                    im_row[idx(1, i, k)] += P[k][j]
                    im_row[idx(0, k, j)] -= R[i][k]
                    im_row[idx(1, k, j)] -= P[i][k]
                rows.append(re_row)
                rows.append(im_row)
    return nv - rank_q(rows, nv)


def givens(n, k, c, s):
    P = [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]
    P[k][k], P[k][k + 1], P[k + 1][k], P[k + 1][k + 1] = c, -s, s, c
    return P


def zero_mat(n):
    return [[Q(0)] * n for _ in range(n)]


def centre_analysis(name):
    """Exhibit a central z with rho_fund(z)=-I or prove none exists (exact)."""
    if name.startswith('SU('):
        n = int(name[3:-1])
        gens = [(givens(n, k, Q(3, 5), Q(4, 5)), zero_mat(n)) for k in range(n - 1)]
        D_im = zero_mat(n)
        D_re = [[Q(1) if (i == j and i >= 2) else Q(0) for j in range(n)] for i in range(n)]
        D_im[0][0], D_im[1][1] = Q(1), Q(-1)
        gens.append((D_re, D_im))          # diag(i,-i,1,...,1) in SU(n)
        dim = commutant_real_dimension(gens, n)
        must(dim == 2, 'commutant of SU(%d) generators is the complex scalars' % n)
        has = (-1) ** n == 1
        return {'group': name, 'centre': 'scalars zeta I with zeta^%d=1 (commutant of %d exact SU(%d) elements has complex dimension 1; det(zeta I)=zeta^%d)' % (n, n, n, n),
                'wilson_action_of_centre': 'rho_fund(zeta I)=zeta I', 'central_minus_one': has,
                'element': '-I (det(-I)=(-1)^%d=1)' % n if has else None,
                'reason': ('-I lies in SU(%d) because (-1)^%d=1 and acts as -I on the fundamental' % (n, n)) if has else
                          ('det(-I)=(-1)^%d=-1, so -I is not in SU(%d); the centre acts on the fundamental by the %d-th roots of unity, none equal to -1' % (n, n, n)),
                'commutant_complex_dimension': 1}
    if name == 'U(1)':
        return {'group': name, 'centre': 'U(1) (abelian)', 'wilson_action_of_centre': 'rho_1(e^{i phi})=e^{i phi}',
                'central_minus_one': True, 'element': 'e^{i pi}=-1',
                'reason': 'every element is central and the charge-1 representation sends e^{i pi} to -1', 'commutant_complex_dimension': None}
    if name == 'Z2':
        return {'group': name, 'centre': 'Z2 (abelian)', 'wilson_action_of_centre': 'sign(g)',
                'central_minus_one': True, 'element': 'the nontrivial element -1',
                'reason': 'the sign character sends the nontrivial element to -1', 'commutant_complex_dimension': None}
    if name == 'SO(3)':
        g1 = (givens(3, 0, Q(3, 5), Q(4, 5)), zero_mat(3))
        g2 = (givens(3, 1, Q(5, 13), Q(12, 13)), zero_mat(3))
        dim = commutant_real_dimension([g1, g2], 3)
        must(dim == 2, 'commutant of two rational rotations is the complex scalars')
        return {'group': name, 'centre': 'trivial: a central element is a real scalar c I (commutant of two exact rotations about different axes) with c^3=det=1, so c=1',
                'wilson_action_of_centre': 'rho_vector(I)=I', 'central_minus_one': False, 'element': None,
                'reason': 'the centre of SO(3) is trivial and the vector representation of the identity is I, not -I',
                'commutant_complex_dimension': 1}
    raise ProducerError('unknown group ' + name)


# ------------------------------------------------------------------ geometry (I1)
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
AXES = 'xyz'


def vadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def coarse(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(face):
    p, a, c = face
    return [(p, a), (vadd(p, UNIT[a]), c), (vadd(p, UNIT[c]), a), (p, c)]


def is_selected(face):
    p, a, c = face
    return a == 0 and c == 1 and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


def tail_range(N):
    return ((-4 * N, 4 * N + 3), (-2 * N, 2 * N + 1), (-N, N))


def owned_by_box(link, N):
    b = coarse(link[0])
    return all(-N <= v <= N for v in b)


def box_plaquettes(N):
    rng = tail_range(N)
    out = []
    for a, c in ((0, 1), (0, 2), (1, 2)):
        for x in range(rng[0][0], rng[0][1] + 1):
            for y in range(rng[1][0], rng[1][1] + 1):
                for z in range(rng[2][0], rng[2][1] + 1):
                    f = ((x, y, z), a, c)
                    if all(owned_by_box(l, N) for l in face_links(f)):
                        out.append(f)
    return out


def factor_tails(b):
    return [(4 * b[0] + r, 2 * b[1] + s, b[2]) for r in range(4) for s in range(2)]


def anchored_faces(b):
    return [(p, a, c) for p in factor_tails(b) for a, c in ((0, 1), (0, 2), (1, 2))]


def retained_faces(N):
    out = []
    for b in product(range(-N, N), repeat=3):
        for f in anchored_faces(b):
            if not is_selected(f):
                out.append(f)
    return out


def faces_meeting_factor(b):
    tails = set(factor_tails(b))
    out = []
    for x in range(4 * b[0] - 1, 4 * b[0] + 5):
        for y in range(2 * b[1] - 1, 2 * b[1] + 3):
            for z in range(b[2] - 1, b[2] + 2):
                for a, c in ((0, 1), (0, 2), (1, 2)):
                    f = ((x, y, z), a, c)
                    if any(l[0] in tails for l in face_links(f)):
                        out.append(f)
    return out


def parse_rule(text):
    """'{(p,x): p_y even} u ...' -> {direction: keyed coordinate}"""
    rule = {}
    for d, k in re.findall(r'\(p,([xyz])\): p_([xyz]) even', text):
        must(AXES.index(d) not in rule, 'repeated direction in flip-set text')
        rule[AXES.index(d)] = AXES.index(k)
    return rule


def in_rule(rule, link):
    d = link[1]
    return d in rule and link[0][rule[d]] % 2 == 0


def count_in(rule, face):
    return sum(1 for l in face_links(face) if in_rule(rule, l))


def reverse_derive_e3():
    """All one-coordinate rules sigma:{x,y,z}->{x,y,z} odd on every plaquette class (24 residue classes)."""
    sols = []
    for sigma in product(range(3), repeat=3):
        rule = {d: sigma[d] for d in range(3)}
        ok = all(count_in(rule, (p, a, c)) % 2 == 1 for p in product((0, 1), repeat=3)
                 for a, c in ((0, 1), (0, 2), (1, 2)))
        if ok:
            sols.append(rule)
    return sols


# 2D geometry for E_2
def face_links_2d(p):
    return [(p, 0), ((p[0] + 1, p[1]), 1), ((p[0], p[1] + 1), 0), (p, 1)]


def rule2d_member(rule, link):
    kind = rule.get(link[1], 'none')
    if kind == 'none':
        return False
    if kind == 'all':
        return True
    coord, par = kind
    return link[0][coord] % 2 == par


def reverse_derive_e2():
    options = ['none', 'all', (0, 0), (0, 1), (1, 0), (1, 1)]
    sols = []
    for kx, ky in product(options, repeat=2):
        rule = {0: kx, 1: ky}
        if all(sum(1 for l in face_links_2d(p) if rule2d_member(rule, l)) == 1 for p in product((0, 1), repeat=2)):
            sols.append(rule)
    return sols


def torus_faces(sides):
    dim = len(sides)
    out = []
    for p in product(*[range(L) for L in sides]):
        for a, c in combinations(range(dim), 2):
            ea = tuple(1 if i == a else 0 for i in range(dim))
            ec = tuple(1 if i == c else 0 for i in range(dim))
            pa = tuple((p[i] + ea[i]) % sides[i] for i in range(dim))
            pc = tuple((p[i] + ec[i]) % sides[i] for i in range(dim))
            out.append([(p, a), (pa, c), (pc, a), (p, c)])
    return out


def torus_rule_even_count(sides, member):
    return sum(1 for f in torus_faces(sides) if sum(1 for l in f if member(l)) % 2 == 0)


def torus_flip_set_exists(sides):
    """GF(2): is there any link set meeting every plaquette of the torus an odd number of times?"""
    dim = len(sides)
    links = {}
    for p in product(*[range(L) for L in sides]):
        for d in range(dim):
            links[(p, d)] = len(links)
    rows = []
    for f in torus_faces(sides):
        r = 0
        for l in f:
            r ^= 1 << links[l]
        rows.append(r)
    ok, _ = gf2_solve(rows, [1] * len(rows), len(links))
    return ok


# ------------------------------------------------ SU(2) loops, surfaces, quaternions
def loop_links(vertices):
    out = []
    for i in range(len(vertices)):
        v, w = vertices[i], vertices[(i + 1) % len(vertices)]
        d = vsub(w, v)
        must(sum(abs(x) for x in d) == 1, 'loop step is not a lattice link')
        axis = [abs(x) for x in d].index(1)
        tail = v if d[axis] == 1 else w
        out.append((tail, axis))
    return out


def boundary(faces):
    acc = {}
    for f in faces:
        for l in face_links(f):
            acc[l] = acc.get(l, 0) ^ 1
    return {l for l, v in acc.items() if v}


def rectangle(p, a, c, m, n):
    ea, ec = UNIT[a], UNIT[c]
    verts = []
    for i in range(m):
        verts.append(tuple(p[k] + i * ea[k] for k in range(3)))
    for j in range(n):
        verts.append(tuple(p[k] + m * ea[k] + j * ec[k] for k in range(3)))
    for i in range(m, 0, -1):
        verts.append(tuple(p[k] + i * ea[k] + n * ec[k] for k in range(3)))
    for j in range(n, 0, -1):
        verts.append(tuple(p[k] + j * ec[k] for k in range(3)))
    faces = [(tuple(p[k] + i * ea[k] + j * ec[k] for k in range(3)), a, c) for i in range(m) for j in range(n)]
    return verts, faces


def cube_faces(p):
    out = []
    for a, c in ((0, 1), (0, 2), (1, 2)):
        o = 3 - a - c
        out.append((p, a, c))
        out.append((vadd(p, UNIT[o]), a, c))
    return out


def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def qinv(q):
    return (q[0], -q[1], -q[2], -q[3])


RATIONAL_UNIT_QUATERNIONS = [
    tuple(Q(v, 5) for v in (1, 2, 2, 4)), tuple(Q(v, 7) for v in (2, 3, 6, 0)),
    tuple(Q(v, 9) for v in (1, 4, 8, 0)), tuple(Q(v, 5) for v in (3, 4, 0, 0)),
    tuple(Q(v, 5) for v in (2, 2, 1, 4)), tuple(Q(v, 3) for v in (1, 2, 2, 0)),
    tuple(Q(v, 13) for v in (5, 12, 0, 0)), tuple(Q(v, 7) for v in (6, 2, 3, 0)),
]


def holonomy_W(vertices, config):
    q = (Q(1), Q(0), Q(0), Q(0))
    for i in range(len(vertices)):
        v, w = vertices[i], vertices[(i + 1) % len(vertices)]
        d = vsub(w, v)
        axis = [abs(x) for x in d].index(1)
        if d[axis] == 1:
            q = qmul(q, config[(v, axis)])
        else:
            q = qmul(q, qinv(config[(w, axis)]))
    return q[0]


# ------------------------------------------------------------ text scanners
def normalize_ws(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def clauses(text):
    return [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', text) if c.strip()]


def phrase_hits(text, forbidden, template):
    body = normalize_ws(text)
    if template:
        body = body.replace(normalize_ws(template), ' ')
    hits = []
    for clause in clauses(body):
        for i, phrase in enumerate(forbidden):
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                hits.append((i, bool(NEGATION.search(clause))))
    return hits


def certify_phrase_scan(text, forbidden, template):
    aff = [i for i, neg in phrase_hits(text, forbidden, template) if not neg]
    require(aff == [], 'affirmative forbidden phrase rejected (list indices %s)' % sorted(set(aff)))
    return True


def certify_no_placeholder(text):
    bad = [m.group(0) for m in PLACEHOLDER.finditer(text)
           if re.search(r'\s', m.group(1)) or '|' in m.group(1) or 'e.g.' in m.group(1)]
    require(bad == [], 'angle-bracket placeholder span rejected (%d spans)' % len(bad))
    return True


def certify_template_once(text, template):
    require(text.count(template) == 1, 'mandatory template must appear exactly once as one unbroken span')
    return True


def certify_no_forbidden_verbs(text):
    verbs = ('pre' + 'dicts', 'con' + 'firms')
    for v in verbs:
        require(re.search(r'(?<![\w])' + v + r'(?![\w])', text, re.I) is None,
                'a transfer or non-transfer described with a verb the contract forbids is rejected')
    return True


# ------------------------------------------------------------ validators
def validate_parameters(params):
    for key in ('metric', 'weights', 'window', 'clock'):
        require(key in params and isinstance(params[key], str) and params[key].strip() != '',
                'parameters field missing: ' + key)
        txt = params[key].strip()
        if txt.startswith('not applicable'):
            require(len(txt[len('not applicable'):].strip(' ;,')) >= 8,
                    'parameters field not applicable without a stated reason: ' + key)
    for key in ('d_X', 'N_0'):
        require(key not in params, 'parameters field declared although it does not apply to BD1: ' + key)
    return True


CONVENTION_SNIPPETS = (
    'per-link electric term 8 C_2(r) in delta units', 'C_F = (N^2-1)/(2N)', 'C_2(n) = n^2',
    'C_2(l) = l(l+1)', 'C_2 = 1 on the odd (sign) link state', 'face energy 32 C_F',
    'magnetic term -(tau/3) sum_f W_f with W_f = Re chi_fund(U_f)/dim fund',
    'c^(1) = -(tau/3)/(32 C_F) sum_f W_f Omega_0', 'omega(W) = -2 Re (W Omega_0, c^(1))',
    'Wilson representation: fundamental for SU(N), charge 1 for U(1), sign for Z2, vector for SO(3)')
CLAIM_EXCLUSION_KEYS = ('any AM2, AV1 or AQ statement for a group other than SU(2)', 'a dictionary to a bare coupling',
                        'weak coupling or continuum', 'uniqueness of any ground state',
                        'any estimate uniform in the lattice spacing a', 'scientific priority',
                        'periodic boxes with an odd side')


def contract_casimir_rule(name):
    """C_F as the frozen convention text states it (parsed rule, evaluated per group)."""
    if name.startswith('SU('):
        n = int(name[3:-1])
        return Q(n * n - 1, 2 * n)
    return {'U(1)': Q(1), 'Z2': Q(1), 'SO(3)': Q(2)}[name]


def validate_contract(data, derived):
    require(data.get('id') == 'BD1' and data.get('round') == 33, 'contract identity')
    require(data.get('status') == 'frozen_before_production', 'contract not frozen')
    params = data.get('parameters', {})
    require(tuple(params.get('groups', [])) == GROUP_ORDER, 'frozen group list changed')
    conv = params.get('convention', '')
    for snip in CONVENTION_SNIPPETS:
        require(snip in conv, 'frozen convention text changed')
    per_link = int(re.search(r'per-link electric term (\d+) C_2', conv).group(1))
    face = int(re.search(r'face energy (\d+) C_F', conv).group(1))
    require(face == 4 * per_link == 32, 'face energy is not four links of the per-link electric term')
    for name in GROUP_ORDER:
        require(derived['casimir_F'][name] == contract_casimir_rule(name), 'Casimir normalization differs from the torus derivation')
    terms = [t.get('coefficient') for t in params.get('hamiltonian_terms', [])]
    require(terms == ['32 (delta units)', '-tau/3', '8 (delta units), per link', '-tau/3'], 'hamiltonian terms changed')
    require(params.get('model_is_finite_graph') is True, 'finite-graph flag')
    fs = params.get('flip_sets', '')
    e3 = parse_rule(fs.split('E_2 =')[0])
    require(e3 == derived['e3_cyclic'], 'E_3 text differs from the reverse-derived cyclic rule')
    e2 = parse_rule(fs.split('E_2 =')[1].split(' on [')[0])
    require(e2 == {0: 1} and derived['e2_x_rule_is_solution'] is True, 'E_2 text differs from a reverse-derived solution')
    require(fs.count('N=2,3,4') == 2 and 'periodic tori with an odd side' in fs, 'flip-set boxes changed')
    ap = params.get('area_parity', '')
    require('kappa=0' in ap and '(-1)^{A(C)}' in ap and 'for the limit of the named constructions' in ap, 'area-parity scope changed')
    validate_parameters(params)
    require(params.get('N_min') == '2', 'N_min')
    ctrl = data.get('controls', [])
    require(len(ctrl) == len(REQUIRED_CONTROLS) and set(ctrl) == set(REQUIRED_CONTROLS), 'control list changed')
    pre = data.get('preregistration', {})
    require(pre.get('controls_required', {}).get('ids') == ctrl, 'control mirror differs')
    ex = data.get('claim_exclusions', [])
    require(len(ex) == 7 and all(any(k in e for e in ex) for k in CLAIM_EXCLUSION_KEYS), 'claim exclusions changed')
    require(pre.get('schema') == 'hnm-r33-prereg-v1', 'prereg schema')
    require(pre.get('tier_names_allowed') == [TIER], 'tier vocabulary changed')
    require(pre.get('sub_labels_allowed') == ['transfer_to_named_model', 'obstruction_recorded'], 'sub-label vocabulary changed')
    gf = pre.get('gate_fields_required', {})
    for k, v in EXPECTED_GATE_FIELDS.items():
        require(gf.get(k) is v, 'gate field changed: ' + k)
    require(isinstance(gf.get('flip_transfer_scope'), str) and 'central element acting as -1' in gf['flip_transfer_scope'], 'flip scope text')
    tgt = pre.get('target', {})
    require(tgt.get('comparator') == '== and !=0', 'target comparator changed')
    tau = pre.get('tau', {})
    require(tau.get('signs_evaluated') == ['+', '-'] and '1/100000000' in tau.get('value', ''), 'tau prereg changed')
    obs = pre.get('observable', {})
    require(obs.get('reference_route') == 'Haar' and 'free (tau=0) values' in obs.get('reference_value_exact', ''), 'reference changed')
    fp = pre.get('forbidden_phrasings', [])
    require(('pre' + 'dicts') in fp and ('con' + 'firms') in fp, 'forbidden phrasings changed')
    tpl = pre.get('mandatory_sentence_template', '')
    for key in ('SU(3) and SO(3) are recorded obstructions with exact nonzero coefficients',
                'SU(5) is a recorded flip obstruction with an exact nonzero fourth-order coefficient',
                'for the limit of the named constructions', 'not a statement uniform in the lattice spacing a'):
        require(key in tpl, 'mandatory template changed')
    require(pre.get('error_terms_itemized') == ['moment_arithmetic', 'character_multiplicities', 'weyl_constant_terms',
                                                'one_plaquette_truncation', 'flip_set_enumeration', 'bb2_limit_passage',
                                                'arithmetic'], 'error-term list changed')
    sb = pre.get('scaling_brackets_per_constant', {})
    require(set(sb) == {'first_order_terms', 'obstruction_second_order_terms', 'su5_fourth_order_term', 'moments'}
            and 'ratio exactly 100 ' in sb['first_order_terms'] and 'ratio exactly 10000)' in sb['obstruction_second_order_terms']
            and 'ratio exactly 100000000)' in sb['su5_fourth_order_term'] and 'ratio exactly 1)' in sb['moments'], 'scaling brackets changed')
    return data


def validate_contract_bytes(raw, expected_sha, derived):
    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'contract bytes do not match the bound hash')
    return validate_contract(json.loads(raw.decode('utf-8')), derived)


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    require(set(files) == expected and len(files) == len(expected), 'inputs inventory differs from AGENTS.md, the contract and shared_premises')
    require(not any(f.startswith(p) for f in files for p in FORBIDDEN_INPUT_PREFIXES), 'forbidden current-loop or expert file in inputs')
    return True


def validate_gate(rel, raw, expected_sha, e3_rule):
    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'gate bytes do not match the pinned hash')
    g = json.loads(raw.decode('utf-8'))
    require(g.get('verdict') == 'accepted_within_scope', 'gate verdict is not accepted_within_scope')
    acc = g.get('accepted', '')
    if rel == BB2_GATE:
        gf = g.get('gate_fields', {})
        require(gf.get('whole_sequence_claimed') is True and gf.get('state_convergence_claimed') is True
                and gf.get('common_limit_claimed') is True and gf.get('uniqueness_of_ground_state_claimed') is False,
                'BB2 whole-sequence convergence fields')
        require('both signs' in acc and 'every finite region' in acc and 'F1 = AQ1 centered whole-star boxes' in acc,
                'BB2 accepted scope')
    if rel == AW1_GATE:
        m = re.search(r'E=\{\(p,x\):p_y even\} u \{\(p,y\):p_z even\} u \{\(p,z\):p_x even\}', acc)
        require(m is not None and e3_rule == {0: 1, 1: 2, 2: 0}, 'AW1 flip set')
        require('U_E H_N(tau,kappa) U_E^*=H_N(-tau,-kappa)' in acc and 'omega_tau(W)=+tau/144' in acc, 'AW1 flip lemma and coefficient')
        require('at kappa=0 omega_{N,-tau}(W)=-omega_{N,tau}(W)' in acc, 'AW1 finite-box oddness')
    if rel == AZ1_GATE:
        require('tau=24 lambda/alpha=96/g^4' in acc, 'AZ1 records the SU(2) dictionary')
    return g


def validate_results_controls(checks, controls):
    by = {c['id']: c for c in checks}
    for cid in controls:
        c = by.get(cid)
        require(c is not None and c.get('passed') is True and c.get('kind') == 'damaging_mutation_control'
                and isinstance(c.get('rejected_mutations'), dict) and len(c['rejected_mutations']) > 0,
                'required control missing, flipped or without a rejected mutation')
    return True


def validate_claim_flags(flags):
    for k in ('continuum_claim', 'scientific_priority_verified', 'weak_coupling_claim', 'rate_in_a_claimed',
              'uniqueness_of_ground_state_claimed', 'transfers_to_aq', 'uniform_wilson_claim',
              'resolved_interaction_shift', 'historical_or_occult_provenance_premise'):
        require(flags.get(k) is False, 'claim flag must be false: ' + k)
    require(flags.get('model_is_finite_graph') is True, 'finite-graph flag must be true')
    return True


REP = {'SU(2)': 'fundamental', 'SU(3)': 'fundamental', 'SU(4)': 'fundamental', 'SU(5)': 'fundamental',
       'U(1)': 'charge 1', 'Z2': 'sign', 'SO(3)': 'vector'}
PATTERNED = 'SU(2) zero-selected patterned family'


def validate_cell(cell, table):
    g = cell.get('group')
    require(g in GROUP_ORDER, 'unknown group label')
    require(cell.get('wilson_representation') == REP[g], 'Wilson representation does not belong to the group label')
    allowed = {'H_FG(%s)' % g, 'H^{%s}_N' % g} | ({PATTERNED} if g == 'SU(2)' else set())
    require(cell.get('model') in allowed, 'model label does not belong to the group label')
    ref = table.get((g, cell.get('quantity')))
    require(ref is not None, 'no computed cell for this group and quantity')
    require(parse_q(cell.get('value')) == ref['value'], 'value under this group label is not the value computed for it')
    require(cell['model'] in ref['models'], 'value presented on a model where it is not derived')
    require(cell.get('tau') == 'symbolic', 'group cells carry symbolic tau')
    require(cell.get('normalization') == 'frozen', 'cell under another normalization')
    return True


def producer_outcome(inp):
    if not (inp['criterion_A_proved'] and inp['criterion_B_proved'] and inp['su3_cell'] and inp['so3_cell'] and inp['su5_cell']):
        return 'insufficient'
    if not (inp['all_groups_classified'] and inp['internal_routes_agree'] and inp['area_parity_limit']
            and inp['flip_sets_verified'] and inp['ledger_complete']):
        return 'limited'
    return 'accepted_within_scope'


def certify_outcome(recorded, inp):
    require(recorded == producer_outcome(inp), 'recorded outcome differs from the frozen outcome rule')
    return True


def certify_group_list(groups):
    require(tuple(groups) == GROUP_ORDER, 'group list changed after the freeze (retuning rejected)')
    return True


def validate_value_entry(kind, entry):
    require(isinstance(entry, dict), 'value entry')
    require('hypothesis_source' not in entry, 'hypothesis source attached to a BD1 value')
    route = entry.get('route_of_computation')
    require(route in ROUTES_ALLOWED, 'route_of_computation must be characters or weyl_integration')
    require(route not in PLAN_ROUTE_LABELS, 'plan route label on a BD1 value')
    require(isinstance(entry.get('value'), str), 'value must be an exact rational string')
    parse_q(entry['value'])
    if kind in ('first_order_coefficient', 'first_order_derivative'):
        require(entry.get('tier') == TIER, 'first-order value without the exact_first_order tier')
    elif kind in ('moment', 'second_order_coefficient', 'fourth_order_coefficient', 'third_order_coefficient'):
        require('tier' not in entry, 'a tier on a moment or a higher-order coefficient is rejected')
    else:
        require(False, 'unknown value kind')
    return True


def first_order_from_convention(E_W2, C_F, per_link=8, links=4, magnetic=Q(1, 3)):
    return 2 * magnetic * E_W2 / (per_link * links * C_F)


def certify_first_order_cell(group, value, derived):
    E_W2, C_F = derived[group]
    require(parse_q(value) == first_order_from_convention(E_W2, C_F), 'first-order cell not computed under the frozen convention')
    return True


def certify_no_su2_constant(entry, computed):
    g = entry['group']
    if g != 'SU(2)':
        require(entry.get('source_group', g) == g, 'value copied from another group')
        require(parse_q(entry['first_order_coefficient']) == computed[g], 'first-order coefficient not derived in its own cell')
        require(entry.get('dictionary') is None, 'dictionary to a bare coupling asserted for a group other than SU(2)')
    return True


def certify_flip_entry(entry, centre, obstruction, flip_sets_ok):
    g = entry['group']
    st = entry.get('status')
    require(entry.get('column') == 'flip', 'flip and parity columns conflated')
    if st == 'transfer':
        require(centre[g]['central_minus_one'] is True, 'flip entry for a group without a central element acting as -1')
        require(entry.get('element') is not None and entry.get('element') == centre[g]['element'], 'central element not exhibited')
        require(flip_sets_ok is True, 'flip claimed without verified flip sets')
        allowed = {'H_FG(%s)' % g, 'H^{%s}_N' % g} | ({PATTERNED} if g == 'SU(2)' else set())
        require(set(entry.get('models', [])) <= allowed and len(entry.get('models', [])) > 0, 'flip claimed outside the named models')
    elif st == 'obstruction':
        require(centre[g]['central_minus_one'] is False, 'obstruction recorded for a group with a central -1')
        ce = entry.get('counterexample')
        require(isinstance(ce, dict), 'flip obstruction asserted from the missing central element alone')
        require(ce.get('order') in (2, 4) and parse_q(ce.get('value')) != 0 and parse_q(ce.get('value')) == obstruction[g],
                'flip obstruction must rest on the exact nonzero even-order coefficient of its cell')
    else:
        require(False, 'flip status must be transfer or obstruction')
    return True


def certify_parity_entry(entry, e_w3, single_occurrence_ok, first_derivs):
    g = entry['group']
    st = entry.get('status')
    require(entry.get('column') == 'parity', 'flip and parity columns conflated')
    if st == 'transfer':
        require(e_w3[g] == 0, 'parity claimed with a nonzero third moment')
        require(entry.get('single_occurrence_orthogonality') is True and single_occurrence_ok is True,
                'parity claimed without single-occurrence orthogonality')
    elif st == 'obstruction':
        require(e_w3[g] != 0, 'parity obstruction recorded for a group with vanishing third moment')
        require(parse_q(entry.get('derivative')) == first_derivs[g] and first_derivs[g] != 0,
                'parity obstruction without its nonzero first-order derivative')
    else:
        require(False, 'parity status must be transfer or obstruction')
    return True


def certify_moment_cell(cell):
    vals = cell.get('values')
    require(isinstance(vals, dict) and len(vals) >= 2, 'single-route moment cell rejected')
    qv = [parse_q(v) for v in vals.values()]
    require(all(v == qv[0] for v in qv), 'route evaluations disagree on a moment')
    require(cell.get('route_of_computation') in ROUTES_ALLOWED, 'moment route')
    return True


def compare_route_tables(t1, t2):
    require(set(t1) == set(t2), 'route tables cover different cells')
    for k in sorted(t1):
        require(parse_q(t1[k]) == parse_q(t2[k]), 'routes disagree on a cell')
    return True


def certify_obstruction_cell(name, cell, computed):
    require(cell is not None, 'mandatory obstruction cell omitted')
    require(cell.get('group') == name and cell.get('status') == 'obstruction', 'obstruction cell called a transfer')
    require(cell.get('central_minus_one') is False, 'obstruction cell with a central -1')
    vals = (parse_q(cell.get('E_W3')), parse_q(cell.get('d_omega_W2_dtau')), parse_q(cell.get('omega_2')))
    require(all(v != 0 for v in vals), 'an obstruction coefficient is zero')
    require(vals == computed[name], 'obstruction cell values differ from the computed ones')
    require(cell.get('omega_W_odd_in_tau') is False and cell.get('first_order_parity_holds') is False, 'obstruction record')
    return True


def certify_flip_set(member, faces_links, mode):
    counts = [sum(1 for l in fl if member(l)) for fl in faces_links]
    if mode == 'odd':
        require(all(c % 2 == 1 for c in counts), 'flip set meets %d plaquettes evenly' % sum(1 for c in counts if c % 2 == 0))
    elif mode == 'exactly_one':
        require(all(c == 1 for c in counts), 'E_2 meets %d plaquettes other than exactly once' % sum(1 for c in counts if c != 1))
    else:
        require(False, 'mode')
    return True


def certify_periodic_record(status):
    require(status == 'obstruction_recorded', 'periodic torus with an odd side presented as verified')
    return True


def rule_sign(rule, loop):
    if rule == 'spanning_surface_plaquette_count':
        return (-1) ** loop['area']
    if rule == 'perimeter':
        return (-1) ** loop['perimeter']
    raise Rejected('unknown sign rule')


AREA_BOXES = ('open centered whole-star boxes Lambda_N, N at least 2', 'every on-site cutoff', 'limit of the named constructions')


def certify_area_parity_claim(claim, loops):
    require(claim.get('group') == 'SU(2)', 'area parity claimed for a group other than SU(2)')
    require(claim.get('kappa') == '0', 'area parity claimed at a nonzero selected triple')
    require(claim.get('family') == 'zero-selected patterned family', 'area parity outside the zero-selected family')
    require(all(b in AREA_BOXES for b in claim.get('boxes', [])) and len(claim.get('boxes', [])) > 0, 'area parity claimed for another boundary condition or box family')
    for lp in loops:
        require(rule_sign(claim.get('sign_rule'), lp) == lp['flip_sign'], 'sign rule disagrees with the exact flip sign')
    return True


def certify_fg_model(model):
    require(model.get('electric') == '32 C_2(r) on chi_r', 'one-plaquette electric term changed')
    require(model.get('magnetic') == '-(tau/3) W', 'one-plaquette magnetic term changed')
    require(model.get('model_is_finite_graph') is True and model.get('transfers_to_aq') is False, 'finite-graph labels')
    require(model.get('free_reference_same_code_path') is True, 'free reference not computed in the same code path')
    require(model.get('value_kind') == 'finite_model_value', 'one-plaquette coefficient presented as a lattice-limit value')
    return True


def certify_non_transfer(entry):
    if entry.get('status') == 'obstruction':
        require(isinstance(entry.get('counterexample'), dict), 'non-transfer recorded without its exact counterexample')
    return True


def certify_chain_claims(g, claims):
    if g != 'SU(2)':
        for k in ('AM2', 'AV1', 'AQ', 'dictionary'):
            require(claims.get(k) is False, 'AM2/AV1/AQ chain or dictionary statement for a group other than SU(2) rejected')
    require(set(claims.get('transferred', [])) <= {'flip_lemma', 'parity_theorem', 'first_order_coefficient'},
            'transfer beyond the flip lemma, the parity theorem and the first-order coefficient')
    return True


def certify_su5_cell(cell, computed_w4):
    require(cell is not None, 'SU(5) cell omitted')
    require(cell.get('central_minus_one') is False, 'SU(5) central -1')
    require(parse_q(cell.get('E_W3')) == 0 and cell.get('parity_status') == 'transfer', 'SU(5) parity column must be a transfer')
    require(parse_q(cell.get('d_omega_W2_dtau')) == 0 and parse_q(cell.get('omega_2')) == 0, 'SU(5) vanishing coefficients')
    require(cell.get('flip_status') == 'obstruction', 'SU(5) called a flip transfer')
    require(cell.get('flip_counterexample') == 'omega_4', 'SU(5) flip obstruction resting on the missing central element alone')
    w4 = parse_q(cell.get('omega_4'))
    require(w4 != 0 and w4 == computed_w4, 'SU(5) fourth-order coefficient zero or not the computed value')
    require(cell.get('route_of_computation') in ROUTES_ALLOWED, 'SU(5) route not recorded')
    return True


# ------------------------------------------------------------------- main evaluation
def compute():
    check_py_sha = sha256_file(HERE / 'check.py')          # recorded before any evaluation
    raw = (INPUTS / CONTRACT_REL).read_bytes()
    contract_sha = hashlib.sha256(raw).hexdigest()
    must(contract_sha == CONTRACT_SHA256, 'contract snapshot hash differs from the pinned value')

    # ---------------- A. reverse derivations fixed before any contract field is read
    G = make_groups()
    casimir_F = {}
    for name in GROUP_ORDER:
        vals = casimir_of(G[name], G[name].chi)
        must(len(vals) == 1 and casimir_of(G[name], G[name].chib) == vals, 'fundamental is one Weyl character')
        casimir_F[name] = vals[0]
    e3_solutions = reverse_derive_e3()
    cyclic = {0: 1, 1: 2, 2: 0}
    anticyclic = {0: 2, 1: 0, 2: 1}
    must(len(e3_solutions) == 2 and cyclic in e3_solutions and anticyclic in e3_solutions, 'E_3 reverse derivation')
    e2_solutions = reverse_derive_e2()
    derived = {'casimir_F': casimir_F, 'e3_cyclic': cyclic,
               'e2_x_rule_is_solution': {0: (1, 0), 1: 'none'} in e2_solutions}

    contract = validate_contract_bytes(raw, CONTRACT_SHA256, derived)
    params = contract['parameters']
    pre = contract['preregistration']
    record('contract_snapshot_bound', contract_sha == CONTRACT_SHA256, contract_sha256=contract_sha,
           source='inputs/' + CONTRACT_REL, verified='before any contract field was parsed')
    record('check_py_sha256_recorded_before_evaluation', len(check_py_sha) == 64, check_py_sha256=check_py_sha)
    cache = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if '__pycache__' in p.parts or p.suffix == '.pyc')
    record('no_interpreter_cache_in_closure', cache == [])
    inventory = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    must(validate_inventory(inventory, contract), 'reverse inputs inventory')
    record('reverse_premise_inventory_exact', len(inventory) == 23, inventory_size=len(inventory),
           rule='inputs equals AGENTS.md, the contract and the 21 shared_premises; no current forward, expert or BD skeptic file')

    gates = {}
    for rel, sha in sorted(GATE_SHA256.items()):
        gates[rel] = validate_gate(rel, (INPUTS / rel).read_bytes(), sha, parse_rule(params['flip_sets'].split('E_2 =')[0]))
    agents_sha = sha256_file(INPUTS / 'AGENTS.md')
    aw1_binding = gates[AW1_GATE]['bindings']['AGENTS.md']
    record('admitted_gate_sha256_pinned', agents_sha == AGENTS_SHA256 == aw1_binding,
           pinned=dict(sorted(GATE_SHA256.items())), agents_md_sha256=agents_sha,
           semantic=['AW1 flip set, identity and +tau/144', 'BB2 whole-sequence, both signs, every finite region', 'AZ1 SU(2) dictionary text'])

    target = pre['target']
    comparators = target['comparator'].split(' and ')
    must(comparators == ['==', '!=0'], 'comparator parse')
    tau_cor = parse_q(re.search(r'(\d+/\d+) for the SU\(2\) corollary', pre['tau']['value']).group(1))
    must(tau_cor == Q(1, 10 ** 8), 'SU(2) corollary coupling read from the contract')
    record('contract_fields_read_and_validated', True, target_quantity=target['quantity'], target_value=target['value'],
           comparators=comparators, reference=pre['observable']['reference_value_exact'],
           reference_route=pre['observable']['reference_route'], su2_corollary_tau=qs(tau_cor),
           signs=pre['tau']['signs_evaluated'], groups=list(params['groups']),
           note='read after the reverse derivation of the Casimir normalization and of the flip sets')

    # ---------------- B. Casimir normalization from the torus Laplacian
    lie = {}
    for n in (2, 3, 4, 5):
        diag = [Q(n - 1, 2)] * n          # off-diagonal generators: (E_ii+E_jj)/2 from each of the n-1 pairs containing i
        for k in range(1, n):
            for i in range(k):
                diag[i] += Q(1, 2 * k * (k + 1))
            diag[k] += Q(k * k, 2 * k * (k + 1))
        lie['SU(%d)' % n] = diag
    cas_rows = {}
    for name in GROUP_ORDER:
        g = G[name]
        row = {'C_F_torus': qs(casimir_F[name]), 'C_F_frozen_rule': qs(contract_casimir_rule(name)),
               'face_energy_32C_F': qs(32 * casimir_F[name]), 'per_link_8C_F': qs(8 * casimir_F[name])}
        if g.kind == 'SU':
            n = g.n
            adj = casimir_of(g, padd(pmul(g, g.chi, g.chib), {g.zero: Q(-1)}))
            row['adjoint'] = [qs(v) for v in adj]
            must(adj == [Q(n)], 'adjoint Casimir N')
            for k in range(1, n):
                ck = casimir_of(g, elementary_symmetric(g, k))
                must(ck == [Q(k * (n - k) * (n + 1), 2 * n)], 'Lambda^k Casimir')
            row['Lambda_k'] = [qs(casimir_of(g, elementary_symmetric(g, k))[0]) for k in range(1, n)]
            must(all(v == casimir_F[name] for v in lie[name]), 'Lie-algebra sum T_a T_a equals C_F I (tr T_aT_b=delta/2)')
            row['lie_algebra_sum_TaTa'] = qs(lie[name][0])
        cas_rows[name] = row
    must(casimir_F['SU(2)'] == Q(3, 4), 'SU(2) C_F=j(j+1) at j=1/2 (I1.5 normalization: 6 per link, 24 per face)')
    record('casimir_normalization_torus_laplacian', all(casimir_F[n] == contract_casimir_rule(n) for n in GROUP_ORDER),
           rule='C_2(lambda)=(|lambda+rho|^2-|rho|^2)/2 (flat torus Laplacian on the Weyl numerator); electric energy 32 C_2 per plaquette character',
           table=cas_rows)

    # minimal nonzero Casimir and the Casimir-C_F irreps
    cmin = {}
    at_cf = {}
    for name in GROUP_ORDER:
        g = G[name]
        if g.kind == 'SU':
            n = g.n
            labs = [l for l in su_dominant_labels(n, 3) if any(l)]
            vals = {l: su_casimir_label(g, l) for l in labs}
            cmin[name] = min(vals.values())
            at_cf[name] = sorted(l for l, v in vals.items() if v == casimir_F[name])
            must(at_cf[name] == sorted({tuple([1] + [0] * (n - 1)), tuple([1] * (n - 1) + [0])}), 'only F and its conjugate at C_F')
            cart = [[Q(2) if i == j else (Q(-1) if abs(i - j) == 1 else Q(0)) for j in range(n - 1)] for i in range(n - 1)]
            inv = invert(cart)
            must(all(v > 0 for r in inv for v in r), 'inverse Cartan matrix positive')
            # superadditivity: C(lambda+omega_j) - C(lambda) - C(omega_j) = (lambda, omega_j) > 0 for lambda != 0
            for l in labs:
                for j in range(1, n):
                    om = tuple([1] * j + [0] * (n - j))
                    s = tuple(a + b for a, b in zip(l, om))
                    if s[0] <= 3:
                        must(su_casimir_label(g, s) - vals[l] - su_casimir_label(g, om) > 0, 'Casimir superadditivity')
        elif name == 'U(1)':
            cmin[name] = min(Q(k * k) for k in range(-3, 4) if k)
            at_cf[name] = [(-1,), (1,)]
        elif name == 'Z2':
            cmin[name] = Q(1)
            at_cf[name] = [(1,)]
        else:
            cmin[name] = min(Q(k * (k + 1)) for k in range(1, 5))
            at_cf[name] = [(1,)]
        must(cmin[name] == casimir_F[name], 'minimal nonzero Casimir equals C_F')
    record('minimal_casimir_and_fundamental_level', True, C_min={k: qs(v) for k, v in cmin.items()},
           irreps_at_C_F={k: [list(x) for x in v] for k, v in at_cf.items()},
           proof='SU(N): C(lambda+omega_j)=C(lambda)+C(omega_j)+(lambda,omega_j) with (omega_i,omega_j) positive, and C(omega_k)=k(N-k)(N+1)/(2N) is minimal exactly at k=1,N-1; U(1) n^2; Z2 1; SO(3) l(l+1)')

    # ---------------- C. Haar moments by Weyl integration (two constant-term evaluations)
    moments = {}
    moment_cells = {}
    for name in GROUP_ORDER:
        g = G[name]
        ks = range(1, 7) if name == 'SU(5)' else range(1, 5)
        moments[name] = {}
        for k in ks:
            m1 = haar_moment_m1(g, k)
            m2 = haar_m2(g, ppow(g, g.W, k))
            must(m1 == m2, 'Weyl constant-term evaluations disagree: %s k=%d' % (name, k))
            moments[name][k] = m1
            moment_cells['%s E[W^%d]' % (name, k)] = {
                'values': {'density_constant_term' if g.kind not in ('U1', 'Z2') else
                           ('binomial_constant_term' if g.kind == 'U1' else 'direct_summation'): qs(m1),
                           'weyl_numerator_constant_term': qs(m2)},
                'route_of_computation': ROUTE}
        must(moments[name][1] == 0, 'E[W]=0')
    for c in moment_cells.values():
        must(certify_moment_cell(c), 'moment cell')
    moment_table = {name: {'E[W^%d]' % k: {'value': qs(v), 'route_of_computation': ROUTE}
                           for k, v in sorted(moments[name].items())} for name in GROUP_ORDER}
    expected_closed = {'SU(2)': [0, Q(1, 4), 0, Q(1, 8)], 'SU(3)': [0, Q(1, 18), Q(1, 108), Q(1, 108)],
                       'SU(4)': [0, Q(1, 32), 0, Q(7, 2048)], 'SU(5)': [0, Q(1, 50), 0, Q(3, 2500)],
                       'U(1)': [0, Q(1, 2), 0, Q(3, 8)], 'Z2': [0, Q(1), 0, Q(1)], 'SO(3)': [0, Q(1, 9), Q(1, 27), Q(1, 27)]}
    record('haar_moments_weyl_integration', all([moments[n][k] for k in range(1, 5)] == expected_closed[n] for n in GROUP_ORDER),
           route_of_computation=ROUTE, table=moment_table,
           evaluations='(i) density constant term (1/|W|)CT[W^k prod_{i!=j}(1-x_i/x_j)] (SU(N)), (1/2)CT[W^k(2-z-z^-1)] (SO(3)), binomial constant term of cos^k (U(1)), summation over the two elements (Z2); (ii) factorized numerator constant term (1/|W|)CT[conj(a_rho) W^k a_rho]',
           su5_supplementary={'E[W^5]': qs(moments['SU(5)'][5]), 'E[W^6]': qs(moments['SU(5)'][6])})

    cubic = {}
    e_w3 = {}
    for name in GROUP_ORDER:
        g = G[name]
        d = g.dim_fund
        row = {}
        for a in range(4):
            f = pmul(g, ppow(g, g.chi, a), ppow(g, g.chib, 3 - a))
            v1 = g.haar_m1(f) if g.kind != 'U1' else f.get((0,), Q(0))
            v2 = haar_m2(g, f)
            must(v1 == v2 and v1.denominator == 1 and v1 >= 0, 'cubic moment is a nonnegative integer constant term')
            row[(a, 3 - a)] = v1
        e3 = sum((comb(3, a) * row[(a, 3 - a)] for a in range(4)), Q(0)) / Q(2 * d) ** 3
        must(e3 == moments[name][3], 'E[W^3] from the cubic moments')
        must((e3 == 0) == all(v == 0 for v in row.values()), 'E[W^3]=0 iff every cubic moment vanishes')
        cubic[name] = {'E[chi^%d conj(chi)^%d]' % k: int(v) for k, v in sorted(row.items())}
        e_w3[name] = e3
    record('cubic_moments_constant_terms', True, route_of_computation=ROUTE, table=cubic,
           rule='E[W^3]=(2d)^-3 sum_a C(3,a) E[chi^a conj(chi)^(3-a)] with every cubic moment a nonnegative integer, so E[W^3]=0 iff all vanish')

    # ---------------- D. one-plaquette Rayleigh-Schroedinger on the torus
    rs = {}
    for name in GROUP_ORDER:
        g = G[name]
        psi, E = rayleigh_schroedinger(g, 5)
        wser = expectation_series(g, psi, lambda A, g=g: pmul(g, g.W, A), 5)
        w2ser = expectation_series(g, psi, lambda A, g=g: pmul(g, pmul(g, g.W, g.W), A), 3)
        cser = expectation_series(g, psi, lambda A, g=g: pscale(apply_h0(g, A), Q(1, 32)), 4)
        hf = [-3 * (n + 1) * E[n + 1] for n in range(5)]
        must(wser[:5] == hf, 'Hellmann-Feynman series equals the expectation series (%s)' % name)
        must(wser[0] == moments[name][1] and w2ser[0] == moments[name][2], 'free reference in the same code path')
        rs[name] = {'psi': psi, 'E': E, 'W': wser, 'W2': w2ser, 'C': cser}

    # SU(2) convention check against admitted SU(2) values (not transferred to any other group)
    aw1r = (INPUTS / AW1_REVERSE_REPORT).read_text()
    sk = (INPUTS / AW1_SKEPTIC).read_text()
    m3 = re.search(r'<W> = tau/144 \+ 0 tau\^2 - \((\d+)/(\d+)\)tau\^3', aw1r)
    mw2 = re.search(r'<W\^2> = 1/4 \+ 0 tau \+ \((\d+)/(\d+)\)tau\^2', aw1r)
    m5 = re.search(r'\+(\d+)tau\^5/(\d+)', sk)
    me2 = re.search(r'E_2=-tau\^2/(\d+)', sk)
    adm = {'omega_1': Q(1, 144) if 'omega_tau(W)=+tau/144' in gates[AW1_GATE]['accepted'] else None,
           'omega_3': -Q(int(m3.group(1)), int(m3.group(2))), 'omega_5': Q(int(m5.group(1)), int(m5.group(2))),
           'omega_W2_2': Q(int(mw2.group(1)), int(mw2.group(2))), 'E_2_normalized': -8 * Q(1, int(me2.group(1)))}
    su2 = rs['SU(2)']
    got = {'omega_1': su2['W'][1], 'omega_3': su2['W'][3], 'omega_5': su2['W'][5], 'omega_W2_2': su2['W2'][2], 'E_2_normalized': su2['E'][2]}
    record('su2_convention_check_admitted_series', got == adm, admitted_read_from=['AW1 gate (+tau/144)', AW1_REVERSE_REPORT, AW1_SKEPTIC],
           values={k: qs(v) for k, v in sorted(got.items())},
           note='a check of the frozen convention on SU(2) only (alpha-unit E_2 times 8); no SU(2) value is used for another group')

    # first-order coefficients
    first = {}
    conv_derived = {}
    for name in GROUP_ORDER:
        closed = first_order_from_convention(moments[name][2], casimir_F[name])
        must(closed == rs[name]['W'][1] == -6 * rs[name]['E'][2], 'first-order coefficient: closed form, torus RS and Hellmann-Feynman')
        conv_derived[name] = (moments[name][2], casimir_F[name])
        first[name] = {'value': qs(closed), 'tier': TIER, 'route_of_computation': ROUTE,
                       'formula': '2 (1/3) E[W^2]/(32 C_F) = 2 (1/3) (%s)/(%s)' % (qs(moments[name][2]), qs(32 * casimir_F[name])),
                       'models': ['H_FG(%s)' % name, 'H^{%s}_N' % name] + ([PATTERNED] if name == 'SU(2)' else [])}
    record('first_order_coefficients_all_groups', True, coefficients=first,
           c1_convention='c^(1)=-(tau/3)/(32 C_F) sum_f W_f Omega_0 and omega(W)=-2 Re(W Omega_0,c^(1))+O(tau^2)',
           literal_display_sign='2(W Omega_0,c^(1)) gives the negative of each value (the AW1 wording defect; rejected)',
           box_models='in H^G_N only f=W pairs with W (single-occurrence orthogonality), so the box first-order coefficient equals the one-plaquette value, in each box inside its Kato radius')

    # ---------------- E. criterion A
    centre = {name: centre_analysis(name) for name in GROUP_ORDER}
    flip_groups = [n for n in GROUP_ORDER if centre[n]['central_minus_one']]
    must(flip_groups == ['SU(2)', 'SU(4)', 'U(1)', 'Z2'], 'criterion A classification')
    record('criterion_A_centre_analysis', True, centre=centre, groups_with_central_minus_one=flip_groups)

    flip_demo = {}
    for name in GROUP_ORDER:
        g = G[name]
        if not g.central_minus_one_is_torus_function():
            flip_demo[name] = 'the map x to zx for z=-1 is not a map of the torus of %s: it would send x_1...x_N=1 to (-1)^N' % name \
                if g.kind == 'SU' else 'no central element acts as -1 (trivial centre)'
            continue
        s_vac = {g.flip_sign(mu) for mu in g.arho}
        must(len(s_vac) == 1, 'vacuum numerator has one central sign')
        s0 = s_vac.pop()

        def U(A, g=g, s0=s0):
            return {mu: v * g.flip_sign(mu) * s0 for mu, v in A.items()}
        psi = rs[name]['psi']
        ok = U(g.arho) == g.arho
        ok = ok and all(g.flip_sign(mu) == -1 for mu in g.W)
        ok = ok and all(U(p) == pscale(p, (-1) ** n) for n, p in enumerate(psi))
        ok = ok and all(apply_h0(g, U(p)) == U(apply_h0(g, p)) for p in psi)
        ok = ok and all(U(pmul(g, g.W, p)) == pscale(pmul(g, g.W, U(p)), -1) for p in psi[:3])
        ok = ok and all(rs[name]['W'][k] == 0 for k in (0, 2, 4)) and all(rs[name]['W2'][k] == 0 for k in (1, 3))
        must(ok, 'one-plaquette flip identities for ' + name)
        flip_demo[name] = 'U f(x)=f(zx), z=%s: fixes the vacuum, commutes with H_0, maps W to -W, U psi_n=(-1)^n psi_n for n=0..5; even coefficients of omega(W) and odd coefficients of omega(W^2) vanish through order 4 and 3' % centre[name]['element']
    record('criterion_A_one_plaquette_flip_operator', True, demonstrations=flip_demo,
           kato_radius_one_plaquette='ground simple for |tau| below 48 C_min (Weyl: 2|tau|/3 below the gap 32 C_min)')

    # box operator identity: every retained face and every owned plaquette meets E_3 oddly
    e3 = cyclic
    box_stats = {}
    for N in (2, 3, 4):
        plaqs = box_plaquettes(N)
        ret = retained_faces(N)
        must(all(all(owned_by_box(l, N) for l in face_links(f)) for f in ret), 'retained faces owned by the box')
        hist = {}
        for f in plaqs:
            c = count_in(e3, f)
            hist[c] = hist.get(c, 0) + 1
        must(set(hist) <= {1, 3}, 'E_3 odd on every owned plaquette')
        must(all(count_in(e3, f) % 2 == 1 for f in ret), 'E_3 odd on every retained face')
        box_stats['N=%d' % N] = {'owned_plaquettes': len(plaqs), 'meet_once': hist.get(1, 0), 'meet_three_times': hist.get(3, 0),
                                 'retained_faces': len(ret), 'anchors': (2 * N) ** 3}
    must(box_stats['N=2']['owned_plaquettes'] == 2335 and box_stats['N=2']['retained_faces'] == 1344, 'N=2 counts')
    # exact holonomy fixtures for the flip on a face (U(1), SU(2), SU(4) via SO(4), Z2)
    face0 = ((0, 0, 0), 0, 2)
    fl = face_links(face0)
    u1 = [(Q(3, 5), Q(4, 5)), (Q(5, 13), Q(12, 13)), (Q(8, 17), Q(15, 17)), (Q(7, 25), Q(24, 25))]

    def cmul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    def u1_W(vals):
        h = cmul(cmul(vals[0], vals[1]), cmul((vals[2][0], -vals[2][1]), (vals[3][0], -vals[3][1])))
        return h[0]
    w_u1 = u1_W(u1)
    u1_flipped = [((-v[0], -v[1]) if in_rule(e3, l) else v) for v, l in zip(u1, fl)]
    qs4 = RATIONAL_UNIT_QUATERNIONS[:4]
    su2_links = {l: q for l, q in zip(fl, qs4)}
    verts0 = [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)]
    w_su2 = holonomy_W(verts0, su2_links)
    su2_flipped = {l: (tuple(-x for x in q) if in_rule(e3, l) else q) for l, q in su2_links.items()}
    n_in = count_in(e3, face0)
    fixtures_ok = (u1_W(u1_flipped) == (-1) ** n_in * w_u1 and holonomy_W(verts0, su2_flipped) == (-1) ** n_in * w_su2
                   and w_u1 != 0 and w_su2 != 0 and n_in % 2 == 1)
    # SU(4): z=-I is scalar; tr(zU)=-tr U for an exact SO(4) element U
    U4 = matmul(matmul(givens(4, 0, Q(3, 5), Q(4, 5)), givens(4, 1, Q(5, 13), Q(12, 13))), givens(4, 2, Q(8, 17), Q(15, 17)))
    tr4 = sum(U4[i][i] for i in range(4))
    fixtures_ok = fixtures_ok and sum(-U4[i][i] for i in range(4)) == -tr4 and tr4 != 0
    record('criterion_A_box_operator_identity', fixtures_ok, flip_set='E_3 (reverse-derived cyclic rule)', boxes=box_stats,
           identity='U_E H^G_N(tau) U_E^* = H^G_N(-tau) in every open centered whole-star box and every on-site cutoff, for G in ' + ', '.join(flip_groups),
           fixtures={'face': 'xz face at 0, |f cap E_3|=%d' % n_in, 'U(1)_W': qs(w_u1), 'SU(2)_W': qs(w_su2), 'SU(4)_trace_SO4_element': qs(tr4)},
           proof='z central with rho_fund(z)=-I and z^2=1: U_E is the scalar rho_r(z)=+-1 on each Peter-Weyl block (commutes with every Casimir and every on-site spectral cutoff), commutes with left and right translations (every endpoint gauge action), fixes the Haar vacuum, and multiplies each face holonomy by z^{|f cap E_3|}=z')

    # ---------------- F. criterion B
    critB = {}
    first_derivs = {}
    for name in GROUP_ORDER:
        g = G[name]
        EF = 32 * casimir_F[name]
        nW = numer(g, g.W)
        must(all(g.energy(mu) == EF for mu in nW), 'W Omega_0 is an H_0 eigenvector at 32 C_F')
        psi1 = rs[name]['psi'][1]
        nW2 = numer(g, pmul(g, g.W, g.W))
        alpha = 2 * ip(g, psi1, nW2)
        beta = ip(g, nW, pmul(g, g.W, nW)) / 3
        E1 = rs[name]['E'][1]
        centring = rs[name]['W'][1] * ip(g, nW, g.arho)
        must(alpha == rs[name]['W2'][1] == Q(2, 3) * e_w3[name] / EF and beta == e_w3[name] / 3 and E1 == 0 and centring == 0,
             'first-order terms of omega(W^2), C(s), c(theta)')
        must((alpha == 0 and beta == 0) == (e_w3[name] == 0), 'first-order terms vanish iff E[W^3]=0')
        first_derivs[name] = alpha
        critB[name] = {'d_omega_W2_dtau': {'value': qs(alpha), 'tier': TIER, 'route_of_computation': ROUTE},
                       'state_term_coefficient': {'value': qs(alpha), 'tier': TIER, 'route_of_computation': ROUTE},
                       'duhamel_coefficient': {'value': qs(beta), 'tier': TIER, 'route_of_computation': ROUTE},
                       'energy_term_E1': qs(E1), 'vector_centring_term': qs(centring),
                       'dC_ds_form': 'd/dtau C(s) at 0 = e^{-%s s}(%s + %s s)' % (qs(EF), qs(alpha), qs(beta)),
                       'dc_dtheta_form': 'd/dtau c(theta) at 0 = e^{i %s theta}(%s - i %s theta)' % (qs(EF), qs(alpha), qs(beta)),
                       'parity_holds': e_w3[name] == 0}
    record('criterion_B_one_plaquette_first_order_terms', True, terms=critB,
           closed_forms='state = d omega(W^2)/dtau = (2/3)E[W^3]/(32 C_F); Duhamel = (1/3)E[W^3]; energy E_1=-(1/3)E[W]=0; centring omega_1 E[W]=0')

    level = {}
    for name in GROUP_ORDER:
        g = G[name]
        nc, ncb = numer(g, g.chi), numer(g, g.chib)
        if g.chi == g.chib:
            val = ip(g, nc, pmul(g, g.W, nc)) / ip(g, nc, nc)
            must((val == 0) == (e_w3[name] == 0), 'real level shift vanishes iff E[W^3]=0')
            level[name] = {'dimension_per_plaquette': 1, 'W_on_level': [qs(val)],
                           'first_order_shift': '-(tau/3)(%s)' % qs(val)}
        else:
            M = [[ip(g, x, pmul(g, g.W, y)) for y in (nc, ncb)] for x in (nc, ncb)]
            re_ = padd(nc, ncb)
            im_ = padd(nc, pscale(ncb, -1))      # 2i Im(chi) numerator
            n_re, n_im = ip(g, re_, re_), ip(g, im_, im_)
            w_re = ip(g, re_, pmul(g, g.W, re_)) / n_re
            w_im = ip(g, im_, pmul(g, g.W, im_)) / n_im
            cross = ip(g, re_, pmul(g, g.W, im_))
            must(cross == 0, 'Re/Im cross element')
            zero = all(v == 0 for r in M for v in r)
            must(zero == (e_w3[name] == 0), 'complex level splits iff E[W^3] nonzero')
            level[name] = {'dimension_per_plaquette': 2, 'W_matrix_on_chi_conjchi': [[qs(v) for v in r] for r in M],
                           'W_on_Re_chi': qs(w_re), 'W_on_Im_chi': qs(w_im),
                           'first_order_shifts': ['-(tau/3)(%s)' % qs(w_re), '-(tau/3)(%s)' % qs(w_im)]}
        level[name]['zero_first_order_splitting'] = e_w3[name] == 0
    record('criterion_B_complex_level_zero_splitting', True, level=level,
           statement='on the gauge-invariant level at 32 C_F (W_g Omega_0 and Im chi_fund(U_g) Omega_0 for complex representations) the first-order compression of V is -(tau/3) times cubic moments; it vanishes on the whole level iff E[W^3]=0')

    # single-occurrence orthogonality
    so_ok = True
    for name in GROUP_ORDER:
        g = G[name]
        so_ok = so_ok and g.haar_m1(g.chi) == 0 and haar_m2(g, g.chi) == 0
    Wface = ((0, 0, 0), 0, 2)
    ret2 = retained_faces(2)
    must(Wface in ret2, 'the Wilson face is retained in Lambda_2')
    wl = set(face_links(Wface))
    min_outside = min(len(set(face_links(f)) - wl) for f in ret2 if f != Wface)
    plaqs2 = box_plaquettes(2)
    by_link = {}
    for f in plaqs2:
        for l in face_links(f):
            by_link.setdefault(l, []).append(f)
    share_ok = True
    for f in plaqs2:
        ls = face_links(f)
        for i in range(4):
            for j in range(i + 1, 4):
                if set(by_link[ls[i]]) & set(by_link[ls[j]]) != {f}:
                    share_ok = False
    near = sorted(set(faces_meeting_factor((0, 0, 0))) | set(faces_meeting_factor((0, 0, 1))))
    triple_bad = 0
    ntrip = 0
    for tri in combinations_with_replacement(near, 3):
        ntrip += 1
        if tri[0] == tri[1] == tri[2]:
            continue
        cnt = {}
        for f in tri:
            for l in face_links(f):
                cnt[l] = cnt.get(l, 0) + 1
        if 1 not in cnt.values():
            triple_bad += 1
    so_ok = so_ok and min_outside >= 3 and share_ok and triple_bad == 0
    record('criterion_B_single_occurrence_orthogonality', so_ok,
           rule='a link occurring in exactly one factor carries a single fundamental (or conjugate) matrix element; its Haar integral is the projector onto invariants, of trace E[chi_fund]=0 (constant term), hence 0',
           enumeration={'retained_faces_N2': len(ret2), 'min_links_of_f_outside_W': min_outside,
                        'distinct_plaquettes_share_at_most_one_link_N2': share_ok, 'faces_meeting_R': len(near),
                        'multisets_of_three_faces_meeting_R': ntrip, 'not_all_equal_without_single_link': triple_bad})

    # gauge-invariant level = plaquette characters: 4-cycles of Z^3 are plaquettes
    def nbrs(v):
        for d in range(3):
            for s in (1, -1):
                w = list(v)
                w[d] += s
                yield tuple(w)
    o = (0, 0, 0)
    cycles = set()
    short = 0
    for v1 in nbrs(o):
        for v2 in nbrs(v1):
            if v2 == o:
                continue
            if o in set(nbrs(v2)):
                short += 1
            for v3 in nbrs(v2):
                if v3 in (o, v1):
                    continue
                if o in set(nbrs(v3)) and len({o, v1, v2, v3}) == 4:
                    cycles.add(frozenset(loop_links([o, v1, v2, v3])))
    plaq_sets = set()
    for a, c in ((0, 1), (0, 2), (1, 2)):
        for dx in product((0, -1), repeat=2):
            p = [0, 0, 0]
            p[a], p[c] = dx
            plaq_sets.add(frozenset(face_links((tuple(p), a, c))))
    record('criterion_B_gauge_invariant_level_is_plaquette_characters', cycles == plaq_sets and len(cycles) == 12 and short == 0,
           four_cycles_through_origin=len(cycles), triangles=short,
           level_vectors_per_plaquette={n: level[n]['dimension_per_plaquette'] for n in GROUP_ORDER},
           argument='sum_e 8 C(r_e)=32 C_F with C(r) at least C_F on nontrivial links forces four links with C=C_F; gauge invariance forces degree at least 2 at every vertex, so the links form a 4-cycle, i.e. a plaquette, carrying chi_fund or its conjugate')

    kato = {}
    for name in GROUP_ORDER:
        kato[name] = {'one_plaquette_radius': qs(48 * cmin[name]),
                      'box_radius_formula': '12 C_min/F_N, F_N=21(2N)^3 retained faces',
                      'box_radius_N2': qs(12 * cmin[name] / box_stats['N=2']['retained_faces']),
                      'box_radius_N3': qs(12 * cmin[name] / box_stats['N=3']['retained_faces']),
                      'box_radius_N4': qs(12 * cmin[name] / box_stats['N=4']['retained_faces'])}
    record('kato_radii_explicit', all(box_stats['N=%d' % N]['retained_faces'] == 21 * (2 * N) ** 3 for N in (2, 3, 4)), radii=kato,
           rule='ground of H_0 simple with gap 8 C_min (full box space); ||V|| at most |tau| F_N/3; simple isolated ground and Kato analyticity for 2||V|| below the gap; box-dependent, not uniform in N')

    # Z_N grading and the first possible nonzero even order
    grading = {}
    for name in ('SU(3)', 'SU(4)', 'SU(5)'):
        g = G[name]
        n = g.n
        ok = True
        for k, p in enumerate(rs[name]['psi']):
            allowed = {(k - 2 * j) % n for j in range(k + 1)}
            ok = ok and {g.grade(mu) for mu in p} <= allowed
        evens = [m for m in (2, 4) if rs[name]['W'][m] != 0]
        first_even = (n - 1) if n % 2 == 1 else None
        ok = ok and (evens == ([first_even] if first_even is not None and first_even <= 4 else []) or (name == 'SU(3)' and evens == [2, 4]))
        grading[name] = {'grades_of_psi_n_within_paths': ok, 'first_possible_nonzero_even_order': first_even,
                         'nonzero_even_orders_through_4': evens}
        must(ok, 'Z_N grading of the RS vectors (%s)' % name)
    record('zn_grading_even_orders', True, grading=grading,
           rule='omega(W) at order 2m pairs 2m+1 steps of N-ality +-1 returning to 0 mod N; for odd N this needs 2m+1 at least N, so the first possible even order is N-1; for even N every even order vanishes')

    # ---------------- G. obstruction cells
    obst = {}
    for name in ('SU(3)', 'SO(3)'):
        EF = 32 * casimir_F[name]
        w2 = rs[name]['W'][2]
        must(w2 == e_w3[name] / (3 * EF * EF) and first_derivs[name] == 2 * e_w3[name] / (3 * EF), 'closed forms')
        obst[name] = {'group': name, 'status': 'obstruction', 'central_minus_one': False, 'reason': centre[name]['reason'],
                      'E_W3': qs(e_w3[name]), 'd_omega_W2_dtau': qs(first_derivs[name]), 'omega_2': qs(w2),
                      'omega_3': qs(rs[name]['W'][3]), 'omega_4': qs(rs[name]['W'][4]),
                      'omega_W_odd_in_tau': False, 'first_order_parity_holds': False,
                      'model': 'H_FG(%s)' % name, 'model_is_finite_graph': True, 'transfers_to_aq': False,
                      'route_of_computation': ROUTE,
                      'closed_forms': 'd omega(W^2)/dtau=(2/3)E[W^3]/(32C_F); omega_2=E[W^3]/(3(32C_F)^2)',
                      'd_omega_W2_dtau_entry': {'value': qs(first_derivs[name]), 'tier': TIER, 'route_of_computation': ROUTE},
                      'omega_2_entry': {'value': qs(w2), 'route_of_computation': ROUTE},
                      'previews': {'d_omega_W2_dtau': sci(first_derivs[name]), 'omega_2': sci(w2)}}
    record('obstruction_cell_su3', obst['SU(3)']['omega_2'] == '1/589824' and obst['SU(3)']['d_omega_W2_dtau'] == '1/6912'
           and obst['SU(3)']['E_W3'] == '1/108', cell=obst['SU(3)'])
    record('obstruction_cell_so3', obst['SO(3)']['omega_2'] == '1/331776' and obst['SO(3)']['d_omega_W2_dtau'] == '1/2592'
           and obst['SO(3)']['E_W3'] == '1/27', cell=obst['SO(3)'])
    g5 = G['SU(5)']
    lam_E = []
    for k in range(1, 5):
        ek = elementary_symmetric(g5, k)
        dec = decompose(g5, pmul(g5, g5.chi, ek))
        must(dec.get(tuple([1] * (k + 1) + [0] * (4 - k)) if k < 4 else (0,) * 5, 0) == 1, 'chi times Lambda^k contains Lambda^(k+1) once')
        lam_E.append(32 * casimir_of(g5, ek)[0])
    must(ip(g5, g5.arho, numer(g5, pmul(g5, g5.chi, elementary_symmetric(g5, 4)))) == 1, '(Omega, chi Lambda^4)=1')
    prodE = lam_E[0] * lam_E[1] * lam_E[2] * lam_E[3]
    w4_closed = Q(10, 81) * Q(1, 10 ** 5) / prodE
    w4 = rs['SU(5)']['W'][4]
    must(w4 == w4_closed == -15 * rs['SU(5)']['E'][5] and w4 == Q(1, 2 ** 30 * 3 ** 10), 'SU(5) fourth-order coefficient')
    su5 = {'group': 'SU(5)', 'central_minus_one': False, 'reason': centre['SU(5)']['reason'],
           'E_W3': qs(e_w3['SU(5)']), 'parity_status': 'transfer', 'flip_status': 'obstruction',
           'd_omega_W2_dtau': qs(first_derivs['SU(5)']), 'omega_2': qs(rs['SU(5)']['W'][2]),
           'omega_3': qs(rs['SU(5)']['W'][3]), 'omega_4': qs(w4), 'omega_4_factored': '1/(2^30 3^10)',
           'omega_4_preview': sci(w4), 'flip_counterexample': 'omega_4', 'route_of_computation': ROUTE,
           'omega_4_entry': {'value': qs(w4), 'route_of_computation': ROUTE},
           'closed_form': 'omega_4=-15 E_5, E_5=(-1/3)^5 2 (1/10)^5 prod_k 1/E(Lambda^k): only the column chains Lambda^1..Lambda^4 (and conjugates) return to the trivial class in five steps; E(Lambda^k)=' + ', '.join(qs(v) for v in lam_E),
           'model': 'H_FG(SU(5))', 'model_is_finite_graph': True, 'transfers_to_aq': False,
           'consequence': 'omega(W) is not odd in tau on H_FG(SU(5)); no unitary commuting with the electric term and reversing W exists on that model (it would fix the simple vacuum and make omega(W) odd)'}
    record('obstruction_cell_su5_fourth_order', rs['SU(5)']['W'][2] == 0 and first_derivs['SU(5)'] == 0 and w4 != 0, cell=su5)

    # ---------------- H. flip sets
    record('flip_set_e3_reverse_derived', len(e3_solutions) == 2 and parse_rule(params['flip_sets'].split('E_2 =')[0]) == cyclic,
           solutions=['cyclic: x keyed to p_y, y to p_z, z to p_x', 'anticyclic: x keyed to p_z, y to p_x, z to p_y'],
           residue_classes=24, note='derived by search over the 27 one-coordinate rules before the contract text was parsed')
    record('flip_set_e3_boxes_and_retained_faces', True, boxes=box_stats)
    fac = {}
    patterns = {}
    for b in ((0, 0, 0), (0, 0, 1), (1, 0, 0), (0, 1, 0), (-1, -1, -1), (2, -3, 1), (-2, 1, -2)):
        faces = faces_meeting_factor(b)
        om = [f for f in faces if not is_selected(f)]
        se = [f for f in faces if is_selected(f)]
        must(len(om) == 49 and len(se) == 3 and all(count_in(e3, f) in (1, 3) for f in faces), 'factor faces meet E_3 oddly')
        links_b = [(p, d) for p in factor_tails(b) for d in range(3)]
        rel = tuple(sorted((vsub(p, (4 * b[0], 2 * b[1], b[2])), d) for p, d in links_b if in_rule(e3, (p, d))))
        patterns[b] = rel
        fac[str(b)] = {'omitted_faces_meeting': len(om), 'selected_faces': len(se), 'E3_links_in_factor': len(rel), 'z_parity': b[2] % 2}
    z_inv = patterns[(0, 0, 0)] == patterns[(1, 0, 0)] == patterns[(0, 1, 0)] and patterns[(0, 0, 0)] != patterns[(0, 0, 1)]
    diff = sorted(set(patterns[(0, 0, 0)]) ^ set(patterns[(0, 0, 1)]))
    record('flip_set_e3_coarse_factors', z_inv and {d for _, d in diff} == {1} and len(diff) == 8,
           factors=fac, even_z_links=len(patterns[(0, 0, 0)]), odd_z_links=len(patterns[(0, 0, 1)]),
           note='E_3 cap factor depends only on the parity of the coarse z coordinate; the 8 y-links switch, so E_3 is not invariant under odd coarse translations in z, which the flip lemma does not need')
    e2 = {}
    for N in (2, 3, 4):
        faces2 = [face_links_2d((x, y)) for x in range(-N, N) for y in range(-N, N)]
        certify_flip_set(lambda l: rule2d_member({0: (1, 0), 1: 'none'}, l), faces2, 'exactly_one')
        e2['N=%d' % N] = len(faces2)
    record('flip_set_e2_boxes', {0: (1, 0), 1: 'none'} in e2_solutions and len(e2_solutions) == 4, plaquettes=e2,
           reverse_solutions=4, note='exactly one link of E_2={(p,x): p_y even} per plaquette of [-N,N]^2; four one-direction solutions exist, E_2 is one of them')
    tor = {}
    for sides in ((4, 3), (3, 4), (3, 3), (5, 5)):
        tor['E_2 on %dx%d' % sides] = {'even_plaquettes': torus_rule_even_count(sides, lambda l: l[1] == 0 and l[0][1] % 2 == 0),
                                       'any_flip_set_exists_gf2': torus_flip_set_exists(sides)}
    for sides in ((4, 3, 4), (3, 4, 4), (3, 3, 4), (3, 3, 3), (4, 4, 4)):
        tor['E_3 on %dx%dx%d' % sides] = {'even_plaquettes': torus_rule_even_count(sides, lambda l: l[0][cyclic[l[1]]] % 2 == 0),
                                          'any_flip_set_exists_gf2': torus_flip_set_exists(sides)}
    must(tor['E_3 on 4x3x4']['even_plaquettes'] == 16 and tor['E_3 on 4x4x4']['even_plaquettes'] == 0
         and tor['E_2 on 4x3']['even_plaquettes'] == 4 and tor['E_2 on 3x4']['even_plaquettes'] == 0, 'seam counts')
    record('periodic_tori_odd_side_recorded', certify_periodic_record('obstruction_recorded'), tori=tor, status='obstruction_recorded',
           note='the rules E_3 and E_2 fail at the seam of a torus whose side along the keyed coordinate is odd; no flip or parity statement is made on any periodic box with an odd side')
    exist = {k: v['any_flip_set_exists_gf2'] for k, v in tor.items()}
    must(exist == {'E_2 on 4x3': True, 'E_2 on 3x4': True, 'E_2 on 3x3': False, 'E_2 on 5x5': False, 'E_3 on 4x3x4': True,
                   'E_3 on 3x4x4': True, 'E_3 on 3x3x4': False, 'E_3 on 3x3x3': False, 'E_3 on 4x4x4': True}, 'GF(2) pattern')
    record('finding_torus_flip_set_existence_gf2', True, existence=exist, claimed=False,
           finding='over GF(2) a link set odd on every plaquette of a torus exists iff every coordinate 2-plane has an even number of plaquettes (2D: L_x L_y even; 3D: at most one odd side); the contract obstruction is exact for E_3 and E_2 on the seam, not for every flip set; recorded, not claimed, and no periodic statement is made')

    # ---------------- I. SU(2) area parity
    loops = []
    rng_x, rng_y, rng_z = range(-5, 5), range(-3, 3), range(-2, 2)
    tested = 0
    parity_ok = True
    for a, c in ((0, 1), (0, 2), (1, 2)):
        for m in (1, 2, 3):
            for n in (1, 2, 3):
                for p in product(rng_x, rng_y, rng_z):
                    verts, faces = rectangle(p, a, c, m, n)
                    cl = set(loop_links(verts))
                    if boundary(faces) != cl:
                        parity_ok = False
                    if sum(1 for l in cl if in_rule(e3, l)) % 2 != len(faces) % 2:
                        parity_ok = False
                    tested += 1
    state = 12345
    rand_ok = True
    for trial in range(400):
        faces = []
        for _ in range(1 + trial % 9):
            state = (1103515245 * state + 12345) % (2 ** 31)
            x = state % 9 - 4
            state = (1103515245 * state + 12345) % (2 ** 31)
            y = state % 7 - 3
            state = (1103515245 * state + 12345) % (2 ** 31)
            z = state % 5 - 2
            state = (1103515245 * state + 12345) % (2 ** 31)
            a, c = ((0, 1), (0, 2), (1, 2))[state % 3]
            faces.append(((x, y, z), a, c))
        chain = {}
        for f in faces:
            chain[f] = chain.get(f, 0) ^ 1
        surf = [f for f, v in chain.items() if v]
        cb = boundary(surf)
        if sum(1 for l in cb if in_rule(e3, l)) % 2 != len(surf) % 2:
            rand_ok = False
    # same loop, two spanning surfaces
    v1, f1 = rectangle((0, 0, 0), 0, 1, 1, 1)
    open_box = [f for f in cube_faces((0, 0, 0)) if f != ((0, 0, 0), 0, 1)]
    v2, f2 = rectangle((0, 0, 0), 0, 2, 2, 2)
    tent = [f for f in f2 if f != ((0, 0, 0), 0, 2)] + [f for f in cube_faces((0, -1, 0)) if f != ((0, 0, 0), 0, 2)]
    bent = [((0, 0, 0), 0, 2), ((0, 0, 0), 0, 1)]
    surf_ok = (boundary(open_box) == set(loop_links(v1)) and len(open_box) == 5 and boundary(tent) == set(loop_links(v2))
               and len(tent) == 8 and len(boundary(bent)) == 6)
    record('area_parity_surface_parity', parity_ok and rand_ok and surf_ok, rectangles_tested=tested, random_surfaces=400,
           two_surfaces={'unit loop': [1, 5], '2x2 loop': [4, 8]}, bent_loop_area=2,
           rule='|C cap E_3| = sum over a spanning surface of |f cap E_3| mod 2 = A(C) mod 2, because boundary is linear over GF(2) and every |f cap E_3| is odd')

    # closed surfaces are even: cycle space of a fine box and the E_3 argument
    verts_b = list(product(range(3), repeat=3))
    links_b = [(v, d) for v in verts_b for d in range(3) if v[d] + 1 <= 2]
    lidx = {l: i for i, l in enumerate(links_b)}
    faces_b = [(p, a, c) for p in verts_b for a, c in ((0, 1), (0, 2), (1, 2)) if p[a] + 1 <= 2 and p[c] + 1 <= 2]
    rows2 = []
    for f in faces_b:
        r = 0
        for l in face_links(f):
            r ^= 1 << lidx[l]
        rows2.append(r)
    fidx = {f: i for i, f in enumerate(faces_b)}
    cubes = [p for p in verts_b if all(v + 1 <= 2 for v in p)]
    rows3 = []
    for p in cubes:
        r = 0
        for f in cube_faces(p):
            r ^= 1 << fidx[f]
        rows3.append(r)
    rank2 = gf2_rank(rows2)
    rank3 = gf2_rank(rows3)
    record('closed_surfaces_even', len(faces_b) - rank2 == rank3 == len(cubes) == 8,
           fine_box='[0,2]^3', plaquettes=len(faces_b), cycle_space_dimension=len(faces_b) - rank2, cube_boundaries_rank=rank3,
           argument='every 2-cycle is a sum of cube boundaries (6 plaquettes each), so it has an even number of plaquettes; equivalently |z| = |boundary(z) cap E_3| = 0 mod 2 for any 2-cycle z')

    # exact SU(2) holonomy fixture for the area sign
    fixture_loops = [('plaquette', rectangle((0, 0, 0), 0, 1, 1, 1)), ('2x1', rectangle((-1, 0, 0), 0, 2, 2, 1)),
                     ('3x1', rectangle((0, -1, 0), 1, 2, 3, 1)), ('2x2', rectangle((1, 1, -1), 0, 1, 2, 2)),
                     ('3x2', rectangle((-2, 0, 0), 0, 2, 3, 2))]
    fixture_rows = {}
    loop_records = []
    hol_ok = True
    for idx, (label, (verts, faces)) in enumerate(fixture_loops):
        cl = loop_links(verts)
        cfg = {l: RATIONAL_UNIT_QUATERNIONS[(i + idx) % len(RATIONAL_UNIT_QUATERNIONS)] for i, l in enumerate(cl)}
        w0 = holonomy_W(verts, cfg)
        flipped = {l: (tuple(-x for x in q) if in_rule(e3, l) else q) for l, q in cfg.items()}
        w1 = holonomy_W(verts, flipped)
        sign = (-1) ** len(faces)
        hol_ok = hol_ok and w0 != 0 and w1 == sign * w0
        fixture_rows[label] = {'area': len(faces), 'perimeter': len(cl), 'W': qs(w0), 'W_flipped': qs(w1)}
        loop_records.append({'area': len(faces), 'perimeter': len(cl), 'flip_sign': 1 if w1 == w0 else -1})
    bent_links = boundary(bent)
    loop_records.append({'area': len(bent), 'perimeter': len(bent_links),
                         'flip_sign': (-1) ** sum(1 for l in bent_links if in_rule(e3, l))})
    record('area_parity_exact_su2_holonomy_fixture', hol_ok, loops=fixture_rows, model_is_finite_graph=True, transfers_to_aq=False,
           note='exact rational unit quaternions; flipping the links of E_3 multiplies W_C by (-1)^{A(C)}')

    bb2 = gates[BB2_GATE]
    Y_example = sorted({coarse(l[0]) for l in loop_links(fixture_loops[4][1][0])})
    record('area_parity_box_and_limit', True,
           box_statement='SU(2), kappa=0, every open centered whole-star box Lambda_N (N at least 2) and every on-site cutoff, |tau| at most 10^-8: U_E commutes with the cutoff projections and fixes Omega_0; the finite-box ground eigenvalue is simple (AM2, inherited through AW1), so U_E psi_N(tau) is a multiple of psi_N(-tau) and omega_{N,-tau}(W_C)=(-1)^{A(C)} omega_{N,tau}(W_C), for the untruncated ground vectors as well',
           limit_statement='for a loop C with links in a finite complete-factor region Y, rho^{N,-tau}_Y=U_{E cap Y} rho^{N,tau}_Y U_{E cap Y}^* in every box; BB2 gives trace-norm convergence of rho^{N,+tau}_Y and rho^{N,-tau}_Y along the whole sequence at each sign, and conjugation is trace-norm continuous, so omega^{-tau}_inf(W_C)=(-1)^{A(C)} omega^{tau}_inf(W_C) pointwise for the limit of the named constructions',
           bb2_gate_fields={k: bb2['gate_fields'][k] for k in ('whole_sequence_claimed', 'state_convergence_claimed', 'common_limit_claimed', 'uniqueness_of_ground_state_claimed')},
           bb2_sub_label=bb2.get('sub_label'), aw1_gate_title=gates[AW1_GATE]['title'],
           example_region_for_3x2_loop=[list(y) for y in Y_example], tau=qs(tau_cor), signs=['+', '-'])

    # centre-even observables (one-plaquette demonstration and the cutoff argument)
    ce_ok = all(rs[n]['C'][k] == 0 for n in flip_groups for k in (1, 3)) and all(rs[n]['W2'][k] == 0 for n in flip_groups for k in (1, 3))
    record('centre_even_observables_even', ce_ok, demonstration='omega(C_2) and omega(W^2) on H_FG(G) have vanishing odd coefficients through order 3 for ' + ', '.join(flip_groups),
           argument='a bounded observable with alpha_E(A)=A has omega_{-tau}(A)=omega_tau(A); a Casimir enters through 1_[0,L](C_e) C_e, a function of C_e commuting with U_E, and the monotone limit in L')

    # ---------------- J. scaling brackets, tiers, ledger, gate fields
    t0 = tau_cor
    rat1 = (Q(1, 1152) * t0) / (Q(1, 1152) * t0 / 100)
    rat2 = (rs['SU(3)']['W'][2] * t0 ** 2) / (rs['SU(3)']['W'][2] * (t0 / 100) ** 2)
    rat2b = (rs['SO(3)']['W'][2] * t0 ** 2) / (rs['SO(3)']['W'][2] * (t0 / 100) ** 2)
    rat4 = (w4 * t0 ** 4) / (w4 * (t0 / 100) ** 4)
    record('scaling_brackets', rat1 == 100 and rat2 == rat2b == 10000 and rat4 == 10 ** 8,
           ratios={'first_order_terms': qs(rat1), 'obstruction_second_order_terms': qs(rat2),
                   'su5_fourth_order_term': qs(rat4), 'moments': '1'}, evaluated_at=qs(t0))

    entries = []
    for name in GROUP_ORDER:
        entries.append(('first_order_coefficient', first[name]))
        entries.append(('first_order_derivative', critB[name]['d_omega_W2_dtau']))
        entries.append(('first_order_derivative', critB[name]['duhamel_coefficient']))
        for k in moment_table[name].values():
            entries.append(('moment', k))
    for name in ('SU(3)', 'SO(3)'):
        entries.append(('second_order_coefficient', obst[name]['omega_2_entry']))
        entries.append(('first_order_derivative', obst[name]['d_omega_W2_dtau_entry']))
    entries.append(('fourth_order_coefficient', su5['omega_4_entry']))
    record('tier_labels', all(validate_value_entry(k, e) for k, e in entries), entries_validated=len(entries),
           rule='first-order values carry exact_first_order with route weyl_integration; moments and higher-order coefficients carry the route and no tier')

    obstruction_value = {'SU(3)': rs['SU(3)']['W'][2], 'SO(3)': rs['SO(3)']['W'][2], 'SU(5)': w4}
    ledger = []
    for name in GROUP_ORDER:
        c = centre[name]
        if c['central_minus_one']:
            fe = {'group': name, 'column': 'flip', 'status': 'transfer', 'element': c['element'],
                  'models': ['H_FG(%s)' % name, 'H^{%s}_N' % name] + ([PATTERNED] if name == 'SU(2)' else []),
                  'reason': c['reason'] + '; E_3 verified', 'label': 'transfer_to_named_model'}
        else:
            order = 4 if name == 'SU(5)' else 2
            fe = {'group': name, 'column': 'flip', 'status': 'obstruction',
                  'counterexample': {'order': order, 'value': qs(obstruction_value[name]), 'model': 'H_FG(%s)' % name},
                  'reason': c['reason'], 'label': 'obstruction_recorded'}
        if e_w3[name] == 0:
            pe = {'group': name, 'column': 'parity', 'status': 'transfer', 'single_occurrence_orthogonality': True,
                  'models': ['H_FG(%s)' % name, 'H^{%s}_N' % name], 'reason': 'E[W^3]=0 exactly (every cubic moment vanishes)',
                  'label': 'transfer_to_named_model'}
        else:
            pe = {'group': name, 'column': 'parity', 'status': 'obstruction', 'derivative': qs(first_derivs[name]),
                  'counterexample': {'order': 1, 'value': qs(first_derivs[name]), 'model': 'H_FG(%s)' % name},
                  'reason': 'E[W^3]=%s nonzero' % qs(e_w3[name]), 'label': 'obstruction_recorded'}
        ce = {'group': name, 'column': 'first_order_coefficient', 'status': 'transfer', 'value': first[name]['value'],
              'tier': TIER, 'route_of_computation': ROUTE, 'models': first[name]['models'],
              'reason': 'derived in its own cell under the frozen convention' + ('; reproduces the admitted 1/144 as a convention check' if name == 'SU(2)' else ''),
              'label': 'transfer_to_named_model'}
        de = {'group': name, 'column': 'dictionary',
              'status': 'admitted_su2_only' if name == 'SU(2)' else 'not_asserted',
              'reason': 'the admitted SU(2) dictionary (AZ1 gate text: tau=24 lambda/alpha=96/g^4) is inherited, not re-derived' if name == 'SU(2)'
              else 'claim exclusion: no dictionary to a bare coupling for a group other than SU(2); recorded as an obligation'}
        chain = {'AM2': name == 'SU(2)', 'AV1': name == 'SU(2)', 'AQ': name == 'SU(2)', 'dictionary': name == 'SU(2)',
                 'transferred': ['first_order_coefficient'] + (['flip_lemma'] if fe['status'] == 'transfer' else [])
                 + (['parity_theorem'] if pe['status'] == 'transfer' else []),
                 'obligations': [] if name == 'SU(2)' else ['AM2 fixed point and simple ground', 'AV1 product split', 'AQ1 construction and dynamics',
                                                             'BB2-type whole-sequence convergence', 'dictionary to a bare coupling']}
        ledger.append({'group': name, 'wilson_representation': REP[name], 'flip_lemma': fe, 'parity_theorem': pe,
                       'first_order_coefficient': ce, 'dictionary': de, 'am2_aq_chain': chain})
    led_ok = True
    for row in ledger:
        led_ok = led_ok and certify_flip_entry(row['flip_lemma'], centre, obstruction_value, True)
        led_ok = led_ok and certify_parity_entry(row['parity_theorem'], e_w3, so_ok, first_derivs)
        led_ok = led_ok and certify_chain_claims(row['group'], row['am2_aq_chain'])
        led_ok = led_ok and certify_non_transfer(row['flip_lemma']) and certify_non_transfer(row['parity_theorem'])
    flip_t = [r['group'] for r in ledger if r['flip_lemma']['status'] == 'transfer']
    par_t = [r['group'] for r in ledger if r['parity_theorem']['status'] == 'transfer']
    record('transfer_ledger_complete', led_ok and len(ledger) == 7 and flip_t == ['SU(2)', 'SU(4)', 'U(1)', 'Z2']
           and par_t == ['SU(2)', 'SU(4)', 'SU(5)', 'U(1)', 'Z2'], rows=ledger, flip_transfer_groups=flip_t, parity_transfer_groups=par_t)

    err = {'moment_arithmetic': {'value': '0', 'reason': 'exact Fractions; two constant-term evaluations agree exactly'},
           'character_multiplicities': {'value': 'not_applicable', 'reason': 'the reverse route computes no tensor-product multiplicity; the cubic moments are constant terms whose integrality is checked'},
           'weyl_constant_terms': {'value': '0', 'reason': 'finite Laurent polynomials; the Weyl density is expanded completely and the constant term is exact'},
           'one_plaquette_truncation': {'value': '0', 'reason': 'no basis cutoff: the Weyl numerators carry every monomial, and the order-n coefficient involves finitely many'},
           'flip_set_enumeration': {'value': '0', 'reason': 'exhaustive on the named boxes, factors and tori; the residue-class count covers every plaquette of Z^3'},
           'bb2_limit_passage': {'value': '0', 'reason': 'an exact identity in every box passed through the admitted BB2 trace-norm convergence at each sign; no numerical term'},
           'arithmetic': {'value': '0', 'reason': 'exact rationals throughout; decimals are truncated previews only'}}
    must(list(err) == pre['error_terms_itemized'], 'error ledger names')
    record('error_ledger_itemized', True, ledger=err)

    gate_fields = dict(EXPECTED_GATE_FIELDS)
    gate_fields['flip_transfer_scope'] = ('SU(2), SU(4), U(1) and Z2 (central -I, -I, e^{i pi}, -1 acting as -1 on the Wilson representation), '
                                          'on their one-plaquette models H_FG(G) and group-G whole-star box models H^G_N (the operator identity in every box and cutoff; '
                                          'oddness of omega(W) in each box inside its Kato radius), with E_3 and E_2 verified; no AM2, AV1 or AQ statement for any group other than SU(2)')
    gate_fields['parity_transfer_scope'] = 'SU(2), SU(4), SU(5), U(1) and Z2 (E[W^3]=0), on H_FG(G) and on H^G_N in each box inside its Kato radius'
    gate_fields['obstructions'] = 'SU(3) and SO(3) (flip and parity), SU(5) (flip, by the fourth-order coefficient)'
    must(all(gate_fields[k] is v for k, v in EXPECTED_GATE_FIELDS.items()), 'gate fields')
    record('gate_fields_exported', True, gate_fields=gate_fields)

    # ---------------- K. report checks
    template = pre['mandatory_sentence_template']
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])
    report = (HERE / 'report.md').read_text()
    rep_ok = (certify_template_once(report, template) and certify_phrase_scan(report, forbidden, template)
              and certify_no_placeholder(report) and certify_no_forbidden_verbs(report.replace(template, ' ')))
    record('report_template_phrase_placeholder', rep_ok, template_occurrences=report.count(template),
           scans=['negation-aware phrase scan (round list and contract forbidden phrasings, template removed)', 'placeholder spans', 'forbidden verbs'])

    # ---------------- L. controls as damaging mutations
    def rehash(data):
        b = json.dumps(data, indent=1).encode('utf-8')
        return b, hashlib.sha256(b).hexdigest()
    base = json.loads(raw.decode('utf-8'))

    def tampered(fn):
        d = json.loads(raw.decode('utf-8'))
        fn(d)
        return rehash(d)
    t_groups = tampered(lambda d: d['parameters'].__setitem__('groups', d['parameters']['groups'][:-1]))
    t_conv = tampered(lambda d: d['parameters'].__setitem__('convention', d['parameters']['convention'].replace('face energy 32 C_F', 'face energy 24 C_F')))
    t_e3 = tampered(lambda d: d['parameters'].__setitem__('flip_sets', d['parameters']['flip_sets'].replace('{(p,x): p_y even}', '{(p,x): p_z even}', 1)))

    def drop_control(d):
        d['controls'] = d['controls'][:-1]
        d['preregistration']['controls_required']['ids'] = d['controls']
    t_ctrl = tampered(drop_control)
    t_gate = tampered(lambda d: d['preregistration']['gate_fields_required'].__setitem__('flip_transfer_claimed', False))
    t_tpl = tampered(lambda d: d['preregistration'].__setitem__('mandatory_sentence_template', d['preregistration']['mandatory_sentence_template'].replace(', and SU(5) is a recorded flip obstruction with an exact nonzero fourth-order coefficient', '')))
    bb2_raw = (INPUTS / BB2_GATE).read_bytes()
    bb2_t = json.loads(bb2_raw.decode('utf-8'))
    bb2_t['gate_fields']['whole_sequence_claimed'] = False
    bb2_tb, bb2_ts = rehash(bb2_t)
    flipped_checks = [dict(c) for c in CHECKS] + [{'id': cid, 'passed': True, 'kind': 'damaging_mutation_control', 'rejected_mutations': {'m': 'r'}} for cid in REQUIRED_CONTROLS]
    flipped_checks[-1] = dict(flipped_checks[-1], passed=False)
    control('coherent_evidence_tampering', [
        ('byte_change_without_rehash', validate_contract_bytes, (raw + b' ', CONTRACT_SHA256, derived)),
        ('rehashed_group_list_without_SO3', validate_contract_bytes, (t_groups[0], t_groups[1], derived)),
        ('rehashed_convention_face_energy_24_C_F', validate_contract_bytes, (t_conv[0], t_conv[1], derived)),
        ('rehashed_E3_x_links_keyed_to_p_z', validate_contract_bytes, (t_e3[0], t_e3[1], derived)),
        ('rehashed_control_removed_from_both_lists', validate_contract_bytes, (t_ctrl[0], t_ctrl[1], derived)),
        ('rehashed_gate_field_flip_transfer_false', validate_contract_bytes, (t_gate[0], t_gate[1], derived)),
        ('rehashed_template_without_SU5_clause', validate_contract_bytes, (t_tpl[0], t_tpl[1], derived)),
        ('rehashed_BB2_gate_whole_sequence_false', validate_gate, (BB2_GATE, bb2_tb, bb2_ts, cyclic)),
        ('declared_snapshot_removed', validate_inventory, (inventory[1:], contract)),
        ('required_control_boolean_flipped', validate_results_controls, (flipped_checks, REQUIRED_CONTROLS)),
    ], note='coherent tampers rebind every hash and are still rejected semantically')

    control('exact_arithmetic_admission', [
        ('float_moment', parse_q, (0.25,)),
        ('bool_value', parse_q, (True,)),
        ('nan_value', parse_q, (float('nan'),)),
        ('decimal_string', parse_q, ('0.0008680555',)),
        ('float_obstruction_coefficient_in_cell', certify_obstruction_cell,
         ('SU(3)', dict(obst['SU(3)'], omega_2=1.6954210069444444e-06), {n: (e_w3[n], first_derivs[n], rs[n]['W'][2]) for n in ('SU(3)', 'SO(3)')})),
    ])
    flags = {'continuum_claim': False, 'scientific_priority_verified': False, 'weak_coupling_claim': False,
             'rate_in_a_claimed': False, 'uniqueness_of_ground_state_claimed': False, 'transfers_to_aq': False,
             'uniform_wilson_claim': False, 'resolved_interaction_shift': False, 'historical_or_occult_provenance_premise': False,
             'model_is_finite_graph': True}
    must(validate_claim_flags(flags), 'claim flags')
    control('no_priority_or_continuum_claim', [
        ('continuum_true', validate_claim_flags, (dict(flags, continuum_claim=True),)),
        ('priority_true', validate_claim_flags, (dict(flags, scientific_priority_verified=True),)),
        ('weak_coupling_true', validate_claim_flags, (dict(flags, weak_coupling_claim=True),)),
        ('historical_provenance_as_premise', validate_claim_flags, (dict(flags, historical_or_occult_provenance_premise=True),)),
    ])
    table = {}
    for name in GROUP_ORDER:
        table[(name, 'first_order_coefficient')] = {'value': parse_q(first[name]['value']), 'models': first[name]['models']}
    for name in ('SU(3)', 'SO(3)'):
        table[(name, 'omega_2')] = {'value': rs[name]['W'][2], 'models': ['H_FG(%s)' % name]}
    table[('SU(5)', 'omega_4')] = {'value': w4, 'models': ['H_FG(SU(5))']}
    good = {'group': 'SU(3)', 'wilson_representation': 'fundamental', 'model': 'H_FG(SU(3))', 'quantity': 'omega_2',
            'value': qs(rs['SU(3)']['W'][2]), 'tau': 'symbolic', 'normalization': 'frozen'}
    must(validate_cell(good, table), 'positive cell')
    control('changed_model_relabelled', [
        ('su2_value_under_su3_label', validate_cell, (dict(good, quantity='first_order_coefficient', value='1/144', model='H_FG(SU(3))'), table)),
        ('one_plaquette_value_as_box_value', validate_cell, (dict(good, model='H^{SU(3)}_N'), table)),
        ('one_plaquette_value_as_limit_value', validate_cell, (dict(good, model='limit of the named constructions'), table)),
        ('group_box_value_under_su2_patterned_label', validate_cell, (dict(good, group='U(1)', wilson_representation='charge 1', model=PATTERNED, quantity='first_order_coefficient', value='1/96'), table)),
        ('z2_cell_other_normalization', validate_cell, ({'group': 'Z2', 'wilson_representation': 'sign', 'model': 'H_FG(Z2)', 'quantity': 'first_order_coefficient', 'value': '1/6', 'tau': 'symbolic', 'normalization': 'electric 1 on the odd state'}, table)),
    ])
    oc_inputs = {'criterion_A_proved': True, 'criterion_B_proved': True, 'su3_cell': True, 'so3_cell': True, 'su5_cell': True,
                 'all_groups_classified': len(ledger) == 7, 'internal_routes_agree': True, 'area_parity_limit': True,
                 'flip_sets_verified': True, 'ledger_complete': led_ok}
    outcome = producer_outcome(oc_inputs)
    must(outcome == 'accepted_within_scope', 'producer outcome')
    control('insufficient_verdict_retained', [
        ('accepted_with_su3_cell_missing', certify_outcome, ('accepted_within_scope', dict(oc_inputs, su3_cell=False))),
        ('accepted_with_criterion_B_unproved', certify_outcome, ('accepted_within_scope', dict(oc_inputs, criterion_B_proved=False))),
        ('accepted_with_box_level_area_parity_only', certify_outcome, ('accepted_within_scope', dict(oc_inputs, area_parity_limit=False))),
        ('accepted_with_route_disagreement', certify_outcome, ('accepted_within_scope', dict(oc_inputs, internal_routes_agree=False))),
        ('retuned_group_list_without_SO3', certify_group_list, (GROUP_ORDER[:-1],)),
    ], outcome_rule='insufficient if criterion A or B or an obstruction cell is missing; limited if a cell is missing or misclassified, routes disagree or only the box area parity is proved')
    control('placeholder_span_rejected', [
        ('group_name_placeholder', certify_no_placeholder, ('the coefficient of ' + chr(60) + 'group name' + chr(62) + ' is exact',)),
        ('vertical_bar_placeholder', certify_no_placeholder, ('status ' + chr(60) + 'transfer|obstruction' + chr(62),)),
        ('eg_placeholder', certify_no_placeholder, ('value ' + chr(60) + 'e.g.1/1152' + chr(62),)),
    ])
    neg_ok = certify_phrase_scan('This is not the thermodynamic limit and no correlation length is claimed.', forbidden, template)
    must(neg_ok, 'negated clause passes')
    control('negation_aware_phrase_scan', [
        ('affirmative_thermodynamic', certify_phrase_scan, ('The limit of the named constructions is the ' + 'thermodynamic limit.', forbidden, template)),
        ('affirmative_forbidden_verb', certify_phrase_scan, ('The SU(2) equation ' + 'pre' + 'dicts the SU(3) value.', forbidden, template)),
        ('affirmative_universality', certify_phrase_scan, ('The coefficient is ' + 'uni' + 'versal.', forbidden, template)),
        ('affirmative_uniformity', certify_phrase_scan, ('The bound is uniform ' + 'in a.', forbidden, template)),
    ], negated_clause_passes=True)
    p0 = dict(params)
    p_nw = {k: v for k, v in p0.items() if k != 'weights'}
    control('parameters_declare_metric_weights_window', [
        ('weights_missing', validate_parameters, (p_nw,)),
        ('window_not_applicable_without_reason', validate_parameters, (dict(p0, window='not applicable'),)),
        ('clock_empty', validate_parameters, (dict(p0, clock=''),)),
        ('d_X_declared', validate_parameters, (dict(p0, d_X='1'),)),
    ])
    fo = dict(first['SU(3)'])
    control('tier_mixing_rejected', [
        ('plan_route_label', validate_value_entry, ('first_order_coefficient', dict(fo, route_of_computation='polymer_kp'))),
        ('float_under_tier', validate_value_entry, ('first_order_coefficient', dict(fo, value=1.0 / 1152))),
        ('tier_on_moment', validate_value_entry, ('moment', dict(moment_table['SU(3)']['E[W^3]'], tier=TIER))),
        ('tier_on_fourth_order', validate_value_entry, ('fourth_order_coefficient', dict(su5['omega_4_entry'], tier=TIER))),
        ('unlisted_route', validate_value_entry, ('first_order_derivative', dict(critB['SO(3)']['d_omega_W2_dtau'], route_of_computation='numerics'))),
        ('hypothesis_source_attached', validate_value_entry, ('first_order_coefficient', dict(fo, hypothesis_source='bb1_frozen_targets'))),
        ('first_order_without_tier', validate_value_entry, ('first_order_coefficient', {k: v for k, v in fo.items() if k != 'tier'})),
    ])
    control('frozen_convention_used', [
        ('su3_face_energy_24_C_F', certify_first_order_cell, ('SU(3)', qs(first_order_from_convention(moments['SU(3)'][2], casimir_F['SU(3)'], per_link=6)), conv_derived)),
        ('u1_su2_value_copied', certify_first_order_cell, ('U(1)', '1/144', conv_derived)),
        ('z2_electric_1_on_odd_state', certify_first_order_cell, ('Z2', qs(first_order_from_convention(Q(1), Q(1), per_link=1)), conv_derived)),
        ('z2_one_minus_sigma_x', certify_first_order_cell, ('Z2', qs(first_order_from_convention(Q(1), Q(1), per_link=2)), conv_derived)),
        ('literal_display_sign', certify_first_order_cell, ('SU(3)', qs(-parse_q(first['SU(3)']['value'])), conv_derived)),
    ])
    computed_first = {n: parse_q(first[n]['value']) for n in GROUP_ORDER}
    control('su2_constants_not_transferred', [
        ('su3_coefficient_1_144', certify_no_su2_constant, ({'group': 'SU(3)', 'first_order_coefficient': '1/144'}, computed_first)),
        ('u1_dictionary_96_over_g4', certify_no_su2_constant, ({'group': 'U(1)', 'first_order_coefficient': '1/96', 'dictionary': 'tau=96/g^4'}, computed_first)),
        ('su4_alpha_g2_over_2a', certify_no_su2_constant, ({'group': 'SU(4)', 'first_order_coefficient': '1/2880', 'dictionary': 'alpha=g^2/(2a)'}, computed_first)),
        ('z2_value_sourced_from_su2', certify_no_su2_constant, ({'group': 'Z2', 'first_order_coefficient': '1/48', 'source_group': 'SU(2)'}, computed_first)),
    ])
    lf = {r['group']: r['flip_lemma'] for r in ledger}
    lp = {r['group']: r['parity_theorem'] for r in ledger}
    control('flip_criterion_central_minus_one', [
        ('su3_flip_transfer', certify_flip_entry, (dict(lf['SU(4)'], group='SU(3)'), centre, obstruction_value, True)),
        ('su5_obstruction_from_missing_centre_alone', certify_flip_entry, ({k: v for k, v in lf['SU(5)'].items() if k != 'counterexample'}, centre, obstruction_value, True)),
        ('su4_transfer_without_element', certify_flip_entry, (dict(lf['SU(4)'], element=None), centre, obstruction_value, True)),
        ('so3_counterexample_zero', certify_flip_entry, (dict(lf['SO(3)'], counterexample={'order': 2, 'value': '0'}), centre, obstruction_value, True)),
        ('u1_flip_outside_named_models', certify_flip_entry, (dict(lf['U(1)'], models=['limit of the named constructions']), centre, obstruction_value, True)),
        ('z2_flip_without_verified_flip_sets', certify_flip_entry, (lf['Z2'], centre, obstruction_value, False)),
    ])
    control('parity_criterion_third_moment', [
        ('su3_parity_transfer', certify_parity_entry, (dict(lp['SU(5)'], group='SU(3)'), e_w3, so_ok, first_derivs)),
        ('su5_parity_obstruction', certify_parity_entry, (dict(lp['SU(3)'], group='SU(5)'), e_w3, so_ok, first_derivs)),
        ('u1_without_single_occurrence', certify_parity_entry, (dict(lp['U(1)'], single_occurrence_orthogonality=False), e_w3, so_ok, first_derivs)),
        ('so3_derivative_zero', certify_parity_entry, (dict(lp['SO(3)'], derivative='0'), e_w3, so_ok, first_derivs)),
        ('columns_conflated', certify_parity_entry, (dict(lp['SU(5)'], column='flip'), e_w3, so_ok, first_derivs)),
    ])
    mc = moment_cells['SU(3) E[W^3]']
    mine = {'%s %s' % (n, k): v['value'] for n in GROUP_ORDER for k, v in moment_table[n].items()}
    other = dict(mine)
    other['SU(3) E[W^4]'] = '1/54'
    must(compare_route_tables(mine, dict(mine)), 'table self-comparison')
    control('moment_tables_two_routes', [
        ('single_route_cell', certify_moment_cell, ({'values': {'density_constant_term': mc['values']['density_constant_term']}, 'route_of_computation': ROUTE},)),
        ('float_moment_cell', certify_moment_cell, ({'values': {'a': 1.0 / 108, 'b': '1/108'}, 'route_of_computation': ROUTE},)),
        ('evaluations_disagree', certify_moment_cell, ({'values': {'a': '1/108', 'b': '1/54'}, 'route_of_computation': ROUTE},)),
        ('cross_route_table_disagrees', compare_route_tables, (mine, other)),
    ], exchange_note='the characters-route comparison is made at the exchange with the forward table; compare_route_tables requires exact equality cell by cell')
    comp_obs = {n: (e_w3[n], first_derivs[n], rs[n]['W'][2]) for n in ('SU(3)', 'SO(3)')}
    must(certify_obstruction_cell('SU(3)', obst['SU(3)'], comp_obs) and certify_obstruction_cell('SO(3)', obst['SO(3)'], comp_obs), 'obstruction cells')
    control('su3_obstruction_mandatory', [
        ('su3_cell_omitted', certify_obstruction_cell, ('SU(3)', None, comp_obs)),
        ('su3_called_transfer', certify_obstruction_cell, ('SU(3)', dict(obst['SU(3)'], status='transfer'), comp_obs)),
        ('su3_second_order_zero', certify_obstruction_cell, ('SU(3)', dict(obst['SU(3)'], omega_2='0'), comp_obs)),
        ('su3_with_su2_moment', certify_obstruction_cell, ('SU(3)', dict(obst['SU(3)'], E_W3='0'), comp_obs)),
    ])
    control('so3_obstruction_mandatory', [
        ('so3_cell_omitted', certify_obstruction_cell, ('SO(3)', None, comp_obs)),
        ('so3_called_transfer', certify_obstruction_cell, ('SO(3)', dict(obst['SO(3)'], status='transfer'), comp_obs)),
        ('so3_first_derivative_zero', certify_obstruction_cell, ('SO(3)', dict(obst['SO(3)'], d_omega_W2_dtau='0'), comp_obs)),
        ('so3_central_minus_one_claimed', certify_obstruction_cell, ('SO(3)', dict(obst['SO(3)'], central_minus_one=True), comp_obs)),
    ])
    plq_links = [face_links(f) for f in box_plaquettes(2)]
    minus_one = ((0, 0, 0), 0)
    faces2 = [face_links_2d((x, y)) for x in range(-2, 2) for y in range(-2, 2)]
    control('flip_sets_verified', [
        ('E3_minus_one_link', certify_flip_set, (lambda l: in_rule(e3, l) and l != minus_one, plq_links, 'odd')),
        ('E3_anticyclic_on_x_links_only', certify_flip_set, (lambda l: l[1] == 0 and l[0][2] % 2 == 0, plq_links, 'odd')),
        ('E2_plus_y_links', certify_flip_set, (lambda l: rule2d_member({0: (1, 0), 1: (0, 0)}, l), faces2, 'exactly_one')),
        ('E3_on_4x3x4_torus', certify_flip_set, (lambda l: l[0][cyclic[l[1]]] % 2 == 0, torus_faces((4, 3, 4)), 'odd')),
        ('periodic_odd_side_called_verified', certify_periodic_record, ('verified',)),
    ])
    claim = {'group': 'SU(2)', 'kappa': '0', 'family': 'zero-selected patterned family', 'boxes': list(AREA_BOXES),
             'sign_rule': 'spanning_surface_plaquette_count'}
    must(certify_area_parity_claim(claim, loop_records), 'area-parity claim')
    control('area_parity_scope', [
        ('nonzero_kappa', certify_area_parity_claim, (dict(claim, kappa='1/7'), loop_records)),
        ('periodic_odd_side_box', certify_area_parity_claim, (dict(claim, boxes=list(AREA_BOXES) + ['periodic box with an odd side']), loop_records)),
        ('F2_boxes', certify_area_parity_claim, (dict(claim, boxes=['F2 all-contained-face boxes']), loop_records)),
        ('literal_vertex_boxes', certify_area_parity_claim, (dict(claim, boxes=['literal vertex boxes']), loop_records)),
        ('perimeter_sign_rule', certify_area_parity_claim, (dict(claim, sign_rule='perimeter'), loop_records)),
        ('other_group', certify_area_parity_claim, (dict(claim, group='SU(3)'), loop_records)),
    ])
    fg = {'electric': '32 C_2(r) on chi_r', 'magnetic': '-(tau/3) W', 'model_is_finite_graph': True, 'transfers_to_aq': False,
          'free_reference_same_code_path': True, 'value_kind': 'finite_model_value'}
    must(certify_fg_model(fg), 'one-plaquette model')
    control('one_plaquette_model_terms', [
        ('single_link_electric', certify_fg_model, (dict(fg, electric='8 C_2(r) on chi_r'),)),
        ('alpha_unit_magnetic_as_delta', certify_fg_model, (dict(fg, magnetic='-(tau/24) W'),)),
        ('transfers_to_aq_true', certify_fg_model, (dict(fg, transfers_to_aq=True),)),
        ('free_reference_elsewhere', certify_fg_model, (dict(fg, free_reference_same_code_path=False),)),
        ('lattice_limit_value', certify_fg_model, (dict(fg, value_kind='lattice_limit_value'),)),
    ])
    control('no_transfer_called_prediction', [
        ('verb_one', certify_no_forbidden_verbs, ('The SU(4) flip lemma ' + 'pre' + 'dicts oddness.',)),
        ('verb_two', certify_no_forbidden_verbs, ('The SU(5) cell ' + 'con' + 'firms the transfer.',)),
        ('non_transfer_without_counterexample', certify_non_transfer, ({'status': 'obstruction', 'reason': 'no central -1'},)),
    ])
    control('am2_not_reinstantiated', [
        ('u1_am2', certify_chain_claims, ('U(1)', dict(ledger[4]['am2_aq_chain'], AM2=True))),
        ('z2_aq', certify_chain_claims, ('Z2', dict(ledger[5]['am2_aq_chain'], AQ=True))),
        ('su4_av1', certify_chain_claims, ('SU(4)', dict(ledger[2]['am2_aq_chain'], AV1=True))),
        ('z2_aq1_construction_transferred', certify_chain_claims, ('Z2', dict(ledger[5]['am2_aq_chain'], transferred=['flip_lemma', 'AQ1 construction']))),
        ('u1_dictionary', certify_chain_claims, ('U(1)', dict(ledger[4]['am2_aq_chain'], dictionary=True))),
    ])
    must(certify_su5_cell(su5, w4), 'SU(5) cell')
    control('su5_flip_obstruction_fourth_order', [
        ('su5_cell_omitted', certify_su5_cell, (None, w4)),
        ('su5_flip_transfer', certify_su5_cell, (dict(su5, flip_status='transfer'), w4)),
        ('su5_parity_obstruction', certify_su5_cell, (dict(su5, parity_status='obstruction'), w4)),
        ('su5_obstruction_from_missing_centre_alone', certify_su5_cell, (dict(su5, flip_counterexample=None), w4)),
        ('su5_fourth_order_zero', certify_su5_cell, (dict(su5, omega_4='0'), w4)),
        ('su5_fourth_order_float', certify_su5_cell, (dict(su5, omega_4=float(1) / 63403380965376), w4)),
        ('su5_route_missing', certify_su5_cell, (dict(su5, route_of_computation=None), w4)),
    ])

    ids = [c['id'] for c in CHECKS]
    missing = [c for c in contract['controls'] if c not in ids]
    must(missing == [], 'contract controls without a check: ' + ','.join(missing))
    must(validate_results_controls(CHECKS, contract['controls']), 'control records')
    n_mut = {c['id']: len(c['rejected_mutations']) for c in CHECKS if c.get('kind') == 'damaging_mutation_control'}

    headline = ('Reverse (weyl_integration), under the frozen convention: the flip lemma transfers to SU(2), SU(4), U(1) and Z2 (central -1) and the '
                'first-order parity to SU(2), SU(4), SU(5), U(1) and Z2 (E[W^3]=0) on H_FG(G) and on H^G_N box by box; first-order '
                'coefficients 1/144, 1/1152, 1/2880, 1/5760, 1/96, 1/48, 1/864; SU(3) obstruction d omega(W^2)/dtau=1/6912 and omega_2=1/589824; '
                'SO(3) 1/2592 and 1/331776; SU(5) flip obstruction omega_4=1/63403380965376; SU(2) area parity in every open centered '
                'whole-star box at kappa=0 and for the limit of the named constructions')
    result = {
        'loop': 'BD1', 'direction': 'reverse', 'human_author': HUMAN_AUTHOR,
        'contribution_alias': 'HNM-BD1-R reverse Weyl-integration transfer package',
        'label': 'HNM-BD1-R', 'route_of_computation': ROUTE, 'headline': headline,
        'proposed_reverse_verdict': outcome, 'sub_labels': ['transfer_to_named_model', 'obstruction_recorded'],
        'outcome_note': 'proposed for review; admission needs the forward characters route, the exact comparison of both tables and the skeptical review',
        'ai_assistance': 'derivations, check.py and report.md written by a Claude model agent acting as the BD1 reverse producer',
        'attribution': {'weyl_integration_and_character_formula': 'established (Weyl); constant-term evaluation is standard',
                        'casimir_eigenvalue': 'established ((|lambda+rho|^2-|rho|^2)/2, radial part of the Laplacian)',
                        'centre_flip_and_gradings': 'known kind of argument; no priority claimed',
                        'perturbation_theory': 'Rayleigh-Schroedinger, Hellmann-Feynman and Kato analytic perturbation theory, cited',
                        'scientific_priority': 'unverified'},
        'contract_snapshot_sha256': contract_sha, 'check_py_sha256': check_py_sha,
        'gate_snapshot_sha256': dict(sorted(GATE_SHA256.items())),
        'model': contract['model'], 'model_id': pre['model_id'],
        'target': {'quantity': target['quantity'], 'value': target['value'], 'comparators': comparators,
                   'read_from': 'contract preregistration.target',
                   'applied': 'internal: == between the two constant-term evaluations, RS, Hellmann-Feynman and closed forms; != 0 on the SU(3), SO(3) and SU(5) obstruction coefficients; the cross-route == with the forward table is for the exchange'},
        'reference_values': {'read_from': 'contract preregistration.observable', 'free_values_same_code_path': {
            n: {'omega_0(W)': qs(rs[n]['W'][0]), 'omega_0(W^2)': qs(rs[n]['W2'][0])} for n in GROUP_ORDER}},
        'moment_table': moment_table, 'cubic_moments': cubic, 'first_order_coefficients': first,
        'first_order_terms': critB, 'level_splitting': level, 'centre': centre, 'kato_radii': kato,
        'obstruction_cells': {'SU(3)': obst['SU(3)'], 'SO(3)': obst['SO(3)'], 'SU(5)': su5},
        'one_plaquette_series': {n: {'omega_W': [qs(v) for v in rs[n]['W'][:5]], 'omega_W2': [qs(v) for v in rs[n]['W2'][:3]],
                                     'energy': [qs(v) for v in rs[n]['E'][:6]]} for n in GROUP_ORDER},
        'one_plaquette_model': dict(fg, route_of_computation=ROUTE, hamiltonian='H_FG(G)=32 C_2 - (tau/3) W on class functions of the plaquette holonomy'),
        'flip_sets': {'E_3_boxes': box_stats, 'E_3_factors': fac, 'E_2_boxes': e2, 'tori': tor},
        'area_parity': {'claim': claim, 'fixture': fixture_rows, 'tau': qs(tau_cor)},
        'transfer_ledger': ledger, 'error_ledger': err,
        'gate_fields': gate_fields, 'mandatory_sentence': template,
        'exclusions': contract['claim_exclusions'],
        'contract_controls_covered': sorted(contract['controls']),
        'controls_with_damaging_mutations': len(n_mut),
        'damaging_mutations_per_control': dict(sorted(n_mut.items())),
        'damaging_mutations_total': sum(n_mut.values()),
        'checks': CHECKS,
    }
    for k, v in gate_fields.items():
        result[k] = v
    result.update(flags)
    text = json.dumps(result, indent=2, sort_keys=True)
    must(certify_phrase_scan(text, forbidden, template) is True, 'results text phrase scan')
    must(certify_no_placeholder(text) is True, 'results text placeholder scan')
    must(certify_no_forbidden_verbs(text.replace(json.dumps(template)[1:-1], ' ')) is True, 'results text verbs')
    record('results_text_scanned', True, scans=['negation-aware phrase scan', 'placeholder spans', 'forbidden verbs'])
    return result


def invert(M):
    n = len(M)
    A = [list(r) + [Q(1) if i == j else Q(0) for j in range(n)] for i, r in enumerate(M)]
    for col in range(n):
        piv = next(i for i in range(col, n) if A[i][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [v / pv for v in A[col]]
        for i in range(n):
            if i != col and A[i][col] != 0:
                f = A[i][col]
                A[i] = [a - f * b for a, b in zip(A[i], A[col])]
    return [r[n:] for r in A]


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0)) for j in range(len(b[0]))] for i in range(len(a))]


def main():
    ap = argparse.ArgumentParser(description='HNM-BD1 reverse producer checker (exact arithmetic, weyl_integration)')
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
    manifest = {'loop': 'BD1', 'direction': 'reverse', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'BD1', 'direction': 'reverse', 'checks': len(result['checks']),
                      'controls': result['controls_with_damaging_mutations'], 'mutations': result['damaging_mutations_total'],
                      'verdict': result['proposed_reverse_verdict']}, sort_keys=True))


if __name__ == '__main__':
    main()
