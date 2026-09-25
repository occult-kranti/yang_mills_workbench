#!/usr/bin/env python3
"""Round33 BD1 skeptic pre-comparison checker (paired loop; centre-symmetry transfer across gauge groups).

Written after the BD1 contract froze (sha256 a5c84166...75c1fc, frozen 2026-09-25T05:09:10Z) from the frozen
contract, advisor/selection-bd1.md, advisor/plan.json (vocabulary recorded below, not read at run time), the declared
premises (AW1 gate, forward and reverse reports and skeptic review; AW2, AZ1, AZ2, AY2 and BB2 gates; the AZ2 and BB2
forward reports; the I1 report; the BA1 and BB2 contracts for the inherited control semantics) and the blocking edits
and determinations of the pre-freeze review skeptic/bd-contract-review.json (another skeptic session; its advisor-only
previews and previews_recomputed are never read by this program), before reading anything under
research/round33/forward/bd1/ or research/round33/reverse/bd1/ (only the file names of their inputs/ were listed and
hashed; the recorded inventory is embedded below). No code of /tmp/claude-0/skeptic-bd-private/ is reused. Nothing is
imported from any producer, lens, tool or earlier round. Standard library only. Every admission Boolean is decided with
fractions.Fraction; floats appear only in labelled 'previews'. Every check and control raises an explicit exception, so
python -O cannot disable it. Model-agent skeptic with correlated ancestry; not human peer review. Human project author:
Hruday N M (BUNZEEY).

What is derived here, for G in {SU(2), SU(3), SU(4), SU(5), U(1), Z2, SO(3)} under the frozen convention:
  * Haar moments E[W^k], k=1..5, by three routes: characters (Pieri/Clebsch-Gordan multiplicities, the trivial
    coefficient of W^k acting on the trivial character), Weyl integration by constant-term extraction on the maximal
    torus (one-sided Weyl factor; U(1) by constant term, Z2 by summation, SO(3) with the factor (1-z)), and a labelled
    third route (Frobenius/hook-length counts for SU(N), central binomials for U(1), the inverse binomial transform of
    the Catalan numbers for SO(3));
  * the first-order coefficient 2(1/3)E[W^2]/(32 C_F) (both routes) and the one-plaquette Rayleigh-Schroedinger series
    of omega(W) through order 4 and of omega(W^2) through order 1 on H_FG(G) = 32 C_2 - (tau/3) W, with zero
    truncation error (basis growth leaves every coefficient unchanged), the Pieri tables verified by the Weyl character
    formula at exact rational torus points;
  * the obstruction cells: closed forms (2/3)E[W^3]/(32 C_F) and E[W^3]/(3(32 C_F)^2) against the series for SU(3) and
    SO(3); for SU(5) the Z_5 column-path closed form of the fourth-order coefficient against the series;
  * criterion A (centre analysis and the one-plaquette grading U W U = -W) and criterion B (the level at 32 C_F and the
    cubic moments as nonnegative integers);
  * the flip sets E_3 (boxes N=2,3,4, retained whole-star faces, 24 classes, coarse factors) and E_2 (N=2,3,4), the
    odd periodic tori as obstructions, and the area-parity rule |C cap E_3| = A(S) mod 2 on enumerated loops and
    surfaces;
  * a packet validator executing all 22 contract controls as damaging mutations with positive cases.

Usage: python3 -B research/round33/skeptic/bd1_check.py --output /absolute/fresh/dir
"""
import argparse
import copy
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import permutations, product
from math import comb, factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = 'research/round33/contracts/bd1.json'
CONTRACT_SHA256 = 'a5c8416600c49b0728fdca05cd67c3ff2e53d9fd9e146d4305abcd2da775c1fc'
REVIEW_REL = 'research/round33/skeptic/bd-contract-review.json'  # pre-freeze review (blocking edits only are read)
REVIEW_SHA256 = 'b88dc7179cfcd5b90e659f4f06cbad815accbe7441462c1dae87f8a231577a1f'
AW1_F_REL = 'research/round32/forward/aw1/report.md'
GATES = {
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/aw2-gate.json': '640a3b0a74c7fcd66318ba7ce2a60942f837ad154f157bc1d69323589b24be62',
    'research/round32/advisor/az1-gate.json': '255ce6702628b26b082ceb0e03732c87be84c9ce6315b65c9792087d0cdc03ad',
    'research/round32/advisor/az2-gate.json': 'd36d53dcad8b1d3e4789d3be76b9e491e73cc5cf2ca88f281f66fd255f98b394',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
}
EARLIER_CONTRACTS = {
    'research/round33/contracts/ba1.json': '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9',
    'research/round33/contracts/bb2.json': 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35',
}
PLAN_RECORD = {  # recorded from plan.json as committed with the BD freeze (9ae1160); not read at run time
    'sha256_at_bd_freeze_commit': '7d71bfcb2feee038c9ccb9c9fec15bfb5989aba456501a16ec5625e622b775c9',
    'gate_fields': ['area_parity_limit_claimed', 'continuum_claim', 'flip_transfer_claimed', 'flip_transfer_scope',
                    'model_is_finite_graph', 'obstructions_recorded', 'parity_transfer_claimed', 'rate_in_a_claimed',
                    'scientific_priority_verified', 'transfers_to_aq', 'uniqueness_of_ground_state_claimed',
                    'weak_coupling_claim'],
    'tier_names_allowed': ['analytic_disc', 'crude_majorant', 'duhamel_inner_f1', 'duhamel_inner_f2', 'exact_first_order',
                           'exponential_lieb_robinson', 'first_order_distance_from_product', 'iterated_split',
                           'polymer_kp', 'polynomial_lieb_robinson', 'weighted_norm'],
    'plan_route_labels': ['weighted_norm', 'analytic_disc', 'polymer_kp', 'iterated_split', 'duhamel_inner_f1',
                          'duhamel_inner_f2'],
    'sub_labels': ['transfer_to_named_model', 'obstruction_recorded'],
    'forbidden': ['the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
                  'the thermodynamic limit', 'correlation length', 'predicts', 'confirms', 'unique ground state',
                  'a unique limit', 'the unique limit', 'uniqueness of the ground state',
                  'uniquely determines the ground state'],
}
OBSERVED_INPUTS = {  # find + sha256 over forward/bd1/inputs and reverse/bd1/inputs (names only), 2026-09-25; 23 each
    'AGENTS.md': '870e1a6b1ff81d6e09888d7084dada2dfdb8128048d97857d9c6b1ffce1b9285',
    'research/round21/forward/i1/report.md': '836a4c7d421f0ddf3589c159d2f057839421532c88157a054a61b51c25c781a9',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/aw2-gate.json': '640a3b0a74c7fcd66318ba7ce2a60942f837ad154f157bc1d69323589b24be62',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round32/advisor/az1-gate.json': '255ce6702628b26b082ceb0e03732c87be84c9ce6315b65c9792087d0cdc03ad',
    'research/round32/advisor/az2-gate.json': 'd36d53dcad8b1d3e4789d3be76b9e491e73cc5cf2ca88f281f66fd255f98b394',
    'research/round32/forward/aw1/report.md': 'ea3a936244a31c7ea4d2c8de65798b2bb0fc65a60437122b71a30465e089d883',
    'research/round32/forward/az2/report.md': '7521fd9486e081da00302e1ee6778f5f82920c72c80a39ca86c36876d366ac96',
    'research/round32/reverse/aw1/report.md': '4457c9410bb030b0a856c957e04ab3975bd8a0ffe51476c06edd9ef175f1156c',
    'research/round32/skeptic/aw1.md': '8944a79d72a2135d9a825ab46e7ff42e47781add41865c279f28d179f3547e65',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
    'research/round33/advisor/selection-bd1.md': '08af168f2f19dcee004d0ce893a0d710b96996c2496d73bbd456d276747f1dd9',
    'research/round33/contracts/ba1.json': '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9',
    'research/round33/contracts/bb2.json': 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35',
    'research/round33/contracts/bd1.json': 'a5c8416600c49b0728fdca05cd67c3ff2e53d9fd9e146d4305abcd2da775c1fc',
    'research/round33/forward/bb2/report.md': 'b925ad0720ecb24aeb9483401fe4cf299e713e1793bc2812752d5eca2d723c23',
    'research/round33/methods/historical-physics-panel/SKILL.md': 'a2b366bc661794ee89c29233d0887868b60c0853c85ec136e0529b6f1d5e223a',
    'research/round33/methods/newton-analysis-synthesis/SKILL.md': '2fa3dab9b2420d157457ad3ccaeb0723fb1952871be3e6140dcd3d3c9346ccef',
    'research/round33/methods/paired-physics-research/SKILL.md': '01cda7ee8f8e3eb65c68b0ac6ff0d9e87198f57ea2d997d810d7907b85f4278d',
    'research/round33/methods/paired-physics-research/references/complete-residual-and-error-scope.md': '9e387df64ae05738e740d2ff65973cef0672530e64344ab9e730a139b81b435d',
    'research/round33/methods/tesla-mechanism-resonance/SKILL.md': '81f6d760b3aa45d32db4ae31a3a3c9bec5e1d662e42529b5ae21a220deeb07c3',
    'research/round33/skeptic/bb2.md': 'd04279547212b83c09e314c25cdd50cffe53441bb05977c976115c10ef7d6749',
}
ISOLATION_FORBIDDEN_PREFIXES = ('research/round33/forward/bd1/', 'research/round33/reverse/bd1/',
                                'research/round33/forward/bd2/', 'research/round33/experts/',
                                'research/round33/skeptic/bd-contract-review', 'research/round33/advisor/plan.json',
                                'research/round33/advisor/deliberation', 'research/round33/advisor/panel')

MODEL_ID = 'FG(one_plaquette_group_cells: SU(2),SU(3),SU(4),SU(5),U(1),Z2,SO(3))'
GROUPS = ['SU(2)', 'SU(3)', 'SU(4)', 'SU(5)', 'U(1)', 'Z2', 'SO(3)']
WILSON_REP = {'SU(2)': 'fundamental', 'SU(3)': 'fundamental', 'SU(4)': 'fundamental', 'SU(5)': 'fundamental',
              'U(1)': 'charge 1', 'Z2': 'sign', 'SO(3)': 'vector'}
ONE_PLAQUETTE_TERMS = [{'term': 'electric 32 C_2 on chi_r', 'coefficient': '32'},
                       {'term': 'magnetic W = Re chi_fund/dim fund', 'coefficient': '-tau/3'}]
BOX_TERMS = [{'term': 'electric 8 C_2 per owned link', 'coefficient': '8'},
             {'term': 'W_f on every retained omitted face', 'coefficient': '-tau/3'}]
CONVENTION = {'per_link_electric': '8 C_2', 'Z2_casimir_odd': 1, 'face_energy': '32 C_F',
              'creation_sign': 'psi=e^{-C}Omega_0', 'omega_first_order': '-2 Re (W Omega_0, c^(1))'}
TAU_SU2 = F(1, 10 ** 8)
FLIP_SCOPE = ('groups: SU(2), SU(4), U(1), Z2; each has a central element acting as -1 on its Wilson representation; '
              'on the one-plaquette models H_FG(G) and the group-G whole-star box models H^G_N (the operator identity in '
              'every box and cutoff; oddness of omega(W) in each box inside its Kato radius), with the flip sets verified; '
              'no AM2, AV1 or AQ statement for any group other than SU(2)')
SUB_LABELS = ['transfer_to_named_model', 'obstruction_recorded']
ROUND_FORBIDDEN = [  # mirror of research/round33/tools/phrase_scan.py (not imported)
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


def q_(x):
    return str(x)


def preview(x):
    return format(float(x), '.12e')


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def get_path(doc, path):
    cur = doc
    for key, idx in re.findall(r'\.([A-Za-z_0-9]+)|\[(\d+)\]', path[1:]):
        cur = cur[int(idx)] if idx else cur[key]
    return cur


def has_key_path(doc, path):
    try:
        get_path(doc, path)
    except (KeyError, IndexError, TypeError):
        return False
    return True


# ------------------------------------------------------------------------------------------------ groups (route A)
def pieri_up(lam):
    out = []
    for i in range(len(lam)):
        mu = list(lam)
        mu[i] += 1
        if all(mu[j] >= mu[j + 1] for j in range(len(mu) - 1)):
            out.append(tuple(mu))
    return out


def pieri_down(lam):
    out = []
    for i in range(len(lam)):
        mu = list(lam)
        mu[i] -= 1
        if all(mu[j] >= mu[j + 1] for j in range(len(mu) - 1)):
            out.append(tuple(mu))
    return out


def norm_weight(lam):
    return tuple(x - lam[-1] for x in lam)


class SUN:
    """SU(N): irreps as U(N) highest weights modulo the determinant (normalized last entry 0)."""

    def __init__(self, n):
        self.n = n
        self.name = 'SU(%d)' % n
        self.triv = tuple([0] * n)
        self.dim = n
        self.CF = F(n * n - 1, 2 * n)

    def cas(self, lam):
        n, s = self.n, sum(lam)
        return F(sum(x * x for x in lam) + sum((n - 1 - 2 * i) * x for i, x in enumerate(lam)), 2) - F(s * s, 2 * n)

    def W(self, lam):
        out = {}
        for mu in pieri_up(lam) + pieri_down(lam):
            mu = norm_weight(mu)
            out[mu] = out.get(mu, 0) + F(1, 2 * self.n)
        return out

    def centre(self):
        """centre = {e^{2 pi i k/N} I}; acts as that scalar on the fundamental; -1 iff 2k = N for some k."""
        ks = [k for k in range(self.n) if 2 * k == self.n]
        return {'order': self.n, 'minus_one_element': ('exp(i pi) I = -I (k=%d)' % ks[0]) if ks else None,
                'reason': ('-I lies in SU(%d) (det(-I)=(-1)^%d=1) and acts as -1 on the fundamental' % (self.n, self.n))
                if ks else ('the centre is the %d-th roots of unity times I and -1 is not a %d-th root of unity '
                            '(det(-I)=-1)' % (self.n, self.n))}

    def charge(self, lam):  # N-ality: acts as omega^{|lam|} for the central element omega I
        return sum(lam) % self.n


class U1:
    name, triv, CF = 'U(1)', 0, F(1)

    def cas(self, n):
        return F(n * n)

    def W(self, n):
        return {n + 1: F(1, 2), n - 1: F(1, 2)}

    def centre(self):
        return {'order': 'U(1)', 'minus_one_element': 'z=-1', 'reason': 'U(1) is abelian; z=-1 acts on charge 1 as -1'}

    def charge(self, n):
        return n % 2


class Z2:
    name, triv, CF = 'Z2', 0, F(1)

    def cas(self, s):
        return F(s)  # frozen convention: C_2 = 0 even, 1 odd

    def W(self, s):
        return {1 - s: F(1)}

    def centre(self):
        return {'order': 2, 'minus_one_element': 'z=-1', 'reason': 'Z2 is abelian; the non-identity element acts on the sign '
                'representation as -1'}

    def charge(self, s):
        return s


class SO3:
    name, triv, CF = 'SO(3)', 0, F(2)

    def cas(self, l):
        return F(l * (l + 1))

    def W(self, l):
        if l == 0:
            return {1: F(1, 3)}
        return {l - 1: F(1, 3), l: F(1, 3), l + 1: F(1, 3)}

    def centre(self):
        return {'order': 1, 'minus_one_element': None,
                'reason': 'the centre of SO(3) is trivial (-I has determinant -1), and the identity acts as +1 on the vector '
                          'representation'}

    def charge(self, l):
        return None


def group(name):
    return {'SU(2)': SUN(2), 'SU(3)': SUN(3), 'SU(4)': SUN(4), 'SU(5)': SUN(5), 'U(1)': U1(), 'Z2': Z2(),
            'SO(3)': SO3()}[name]


def apply_W(g, vec, basis=None):
    out = {}
    for k, v in vec.items():
        for mu, c in g.W(k).items():
            if basis is not None and mu not in basis:
                continue
            out[mu] = out.get(mu, 0) + c * v
    return {k: v for k, v in out.items() if v != 0}


def moments_characters(g, kmax):
    vec, res = {g.triv: F(1)}, []
    for _ in range(kmax):
        vec = apply_W(g, vec)
        res.append(vec.get(g.triv, F(0)))
    return res


# ------------------------------------------------------------------------------------------------ route B (Weyl)
def lp_mul(a, b):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            out[e] = out.get(e, 0) + ca * cb
    return {k: v for k, v in out.items() if v != 0}


def perm_sign(p):
    s = 1
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s = -s
    return s


def moments_weyl(name, kmax, unitary_torus=False):
    """E[W^k] by constant-term extraction with the one-sided Weyl factor prod_{i<j}(1-z_j/z_i) (symmetric integrand).
    unitary_torus=True extracts only the exponent 0 (the U(N) torus): a labelled trap, not a route."""
    if name.startswith('SU('):
        n = int(name[3:-1])
        w = {}
        for i in range(n):
            for sgn in (1, -1):
                e = [0] * n
                e[i] = sgn
                w[tuple(e)] = w.get(tuple(e), 0) + F(1, 2 * n)
        delta = list(range(n - 1, -1, -1))
        weyl = {}
        for p in permutations(range(n)):
            e = tuple(delta[p[i]] - delta[i] for i in range(n))
            weyl[e] = weyl.get(e, 0) + perm_sign(p)
        const = lambda s: all(x == s[0] for x in s)  # SU(N) torus: z^{c(1,...,1)} is the trivial character
        if unitary_torus:
            const = lambda s: all(x == 0 for x in s)
    elif name == 'U(1)':
        w, weyl, const = {(1,): F(1, 2), (-1,): F(1, 2)}, {(0,): 1}, (lambda s: s[0] == 0)
    elif name == 'SO(3)':
        w, weyl, const = {(1,): F(1, 3), (0,): F(1, 3), (-1,): F(1, 3)}, {(0,): 1, (1,): -1}, (lambda s: s[0] == 0)
    else:  # Z2 by summation over the two elements, W the sign character
        return [F((1 + (-1) ** k), 2) for k in range(1, kmax + 1)]
    f, res = {tuple([0] * len(next(iter(w)))): F(1)}, []
    for _ in range(kmax):
        f = lp_mul(f, w)
        tot = F(0)
        for e, c in f.items():
            for e2, c2 in weyl.items():
                if const(tuple(x + y for x, y in zip(e, e2))):
                    tot += c * c2
        res.append(tot)
    return res


# ------------------------------------------------------------------------------------------------ route C (labelled)
def partitions(total, maxlen):
    def rec(nleft, mx, ln):
        if nleft == 0:
            yield ()
            return
        if ln == 0:
            return
        for part in range(min(nleft, mx), 0, -1):
            for rest in rec(nleft - part, part, ln - 1):
                yield (part,) + rest
    return list(rec(total, total, maxlen))


def hook_count(lam):
    size = sum(lam)
    if size == 0:
        return 1
    conj = [sum(1 for x in lam if x > j) for j in range(lam[0])]
    prod_h = 1
    for i, row in enumerate(lam):
        for j in range(row):
            prod_h *= (row - j - 1) + (conj[j] - i - 1) + 1
    return factorial(size) // prod_h


def mixed_moment_frobenius(n, a, b):
    """E[chi^a conj(chi)^b] on SU(n): sum of f^lam f^mu over lam|-a, mu|-b (<= n rows) with lam - mu = c(1^n)."""
    tot = 0
    for lam in partitions(a, n):
        for mu in partitions(b, n):
            d = [x - y for x, y in zip(list(lam) + [0] * (n - len(lam)), list(mu) + [0] * (n - len(mu)))]
            if all(x == d[0] for x in d):
                tot += hook_count(lam) * hook_count(mu)
    return tot


def catalan(m):
    return comb(2 * m, m) // (m + 1)


def moments_third(name, kmax):
    if name.startswith('SU('):
        n = int(name[3:-1])
        return [F(sum(comb(k, a) * mixed_moment_frobenius(n, a, k - a) for a in range(k + 1)), (2 * n) ** k)
                for k in range(1, kmax + 1)]
    if name == 'U(1)':
        return [F(comb(k, k // 2), 2 ** k) if k % 2 == 0 else F(0) for k in range(1, kmax + 1)]
    if name == 'SO(3)':  # chi_vector = chi_{1/2}^2 - 1 on SU(2); E[chi_{1/2}^{2i}] = Catalan(i)
        return [F(sum(comb(k, i) * (-1) ** (k - i) * catalan(i) for i in range(k + 1)), 3 ** k) for k in range(1, kmax + 1)]
    return [F(1 + (-1) ** k, 2) for k in range(1, kmax + 1)]


# ------------------------------------------------------------------------------------------------ one-plaquette RS
def reachable(g, steps):
    seen, front = {g.triv}, {g.triv}
    for _ in range(steps):
        new = set()
        for k in sorted(front, key=repr):
            for mu in g.W(k):
                if mu not in seen:
                    new.add(mu)
        seen |= new
        front = new
    return seen


def one_plaquette_rs(g, order, steps):
    """H_FG(G) = 32 C_2 - (tau/3) W on class functions (orthonormal characters), RS about the trivial character.
    Returns omega(W) coefficients 0..order, omega(W^2) coefficients 0..order, energies E_0..E_{order+1}."""
    basis = reachable(g, steps)
    en = {k: 32 * g.cas(k) for k in basis}
    triv = g.triv

    def V1(vec):
        return {k: -c / 3 for k, c in apply_W(g, vec, basis).items()}

    def ip(u, v):
        return sum((c * v[k] for k, c in u.items() if k in v), F(0))
    psi, E = [{triv: F(1)}], [F(0)]
    for nn in range(1, order + 2):
        v1 = V1(psi[nn - 1])
        E.append(v1.get(triv, F(0)))
        rhs = {k: -c for k, c in v1.items()}
        for kk in range(1, nn):
            for k, c in psi[nn - kk].items():
                rhs[k] = rhs.get(k, 0) + E[kk] * c
        new = {}
        for k, c in rhs.items():
            if k != triv and c != 0:
                if en[k] == 0:
                    raise CheckFailure('degenerate free level in one-plaquette RS')
                new[k] = c / en[k]
        psi.append(new)

    def series(op):
        num, den = [F(0)] * (order + 1), [F(0)] * (order + 1)
        for i in range(order + 1):
            for j in range(order + 1 - i):
                num[i + j] += ip(psi[i], op(psi[j]))
                den[i + j] += ip(psi[i], psi[j])
        out = []
        for m in range(order + 1):
            out.append((num[m] - sum((out[k] * den[m - k] for k in range(m)), F(0))) / den[0])
        return out
    om_w = series(lambda v: apply_W(g, v, basis))
    om_w2 = series(lambda v: apply_W(g, apply_W(g, v, basis), basis))
    return om_w, om_w2, E, len(basis)


# ------------------------------------------------------------------------------------------------ Weyl character formula
def det(mat):
    m = [list(r) for r in mat]
    n, d = len(m), F(1)
    for i in range(n):
        piv = next((r for r in range(i, n) if m[r][i] != 0), None)
        if piv is None:
            return F(0)
        if piv != i:
            m[i], m[piv] = m[piv], m[i]
            d = -d
        d *= m[i][i]
        for r in range(i + 1, n):
            f = m[r][i] / m[i][i]
            if f:
                for c in range(i, n):
                    m[r][c] -= f * m[i][c]
    return d


def schur_at(lam, z):
    n = len(z)
    num = det([[F(zi) ** (lam[j] + n - 1 - j) for j in range(n)] for zi in z])
    den = det([[F(zi) ** (n - 1 - j) for j in range(n)] for zi in z])
    return num / den


# ------------------------------------------------------------------------------------------------ lattice geometry
DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))


def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def pi_map(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    return ((p, a), (p, c), (add(p, DIRS[a]), c), (add(p, DIRS[c]), a))


def is_selected(p, a, c):
    return (a, c) == ('x', 'y') and p[0] % 4 in (0, 1, 2) and p[1] % 2 == 0


def in_E3(link):
    p, d = link
    return {'x': p[1] % 2 == 0, 'y': p[2] % 2 == 0, 'z': p[0] % 2 == 0}[d]


def in_E2(link):
    p, d = link
    return d == 'x' and p[1] % 2 == 0


def box_data(n):
    """Open centered whole-star box Lambda_N: plaquettes whose four links the box owns, and retained whole-star faces."""
    xs, ys, zs = range(-4 * n, 4 * n + 4), range(-2 * n, 2 * n + 2), range(-n, n + 1)
    owned = lambda p: -4 * n <= p[0] <= 4 * n + 3 and -2 * n <= p[1] <= 2 * n + 1 and -n <= p[2] <= n
    plaqs = []
    for p in product(xs, ys, zs):
        for a, c in ORIENT:
            if owned(add(p, DIRS[a])) and owned(add(p, DIRS[c])):
                plaqs.append((p, a, c))
    retained = [f for f in plaqs if all(-n <= b <= n - 1 for b in pi_map(f[0])) and not is_selected(*f)]
    # every retained face anchored at b with b+S inside Lambda_N (anchors in [-n, n-1]^3), whole stars complete
    return plaqs, retained


def loop_links(faces):
    cnt = {}
    for f in faces:
        for l in face_links(*f):
            cnt[l] = cnt.get(l, 0) + 1
    return frozenset(l for l, v in cnt.items() if v % 2)


def cube_faces(p):
    """the six plaquettes bounding the unit cube with lowest corner p"""
    out = []
    for a, c in ORIENT:
        other = [d for d in 'xyz' if d not in (a, c)][0]
        out.append((p, a, c))
        out.append((add(p, DIRS[other]), a, c))
    return out


# ------------------------------------------------------------------------------------------------ wording helpers
def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def clauses(text):
    return [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', text) if c.strip()]


def affirmative_hits(text, forbidden, template=None):
    body = normalize(text)
    if template:
        body = body.replace(normalize(template), ' ')
    hits = []
    for clause in clauses(body):
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I) and not NEGATION.search(clause):
                hits.append(phrase)
    return hits


def placeholder_spans(text):
    out = []
    for m in PLACEHOLDER.finditer(text):
        inner = m.group(1)
        if re.search(r'\s', inner) or '|' in inner or 'e.g.' in inner:
            out.append(m.group(0))
    return out


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for k in sorted(value):
            yield from strings(value[k])
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from strings(v)


def has_float(value):
    if isinstance(value, float):
        return True
    if isinstance(value, dict):
        return any(has_float(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(has_float(v) for v in value)
    return False


def packet_digest(pk):
    body = json.dumps({'inputs': pk['inputs'], 'controls': pk['controls']}, sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()


def rebind(pk):
    pk['freeze_digest'] = packet_digest(pk)
    return pk


# ------------------------------------------------------------------------------------------------ packet validator
def validate(pk, c):
    if pk['contract_sha256'] != CONTRACT_SHA256:
        raise Rejected('contract hash')
    if pk['freeze_digest'] != packet_digest(pk):
        raise Rejected('coherent evidence tampering: freeze digest')
    for side in ('forward', 'reverse'):
        inv = pk['inputs'][side]
        if sorted(inv) != sorted(c['declared_inputs']):
            extra = sorted(set(inv) - set(c['declared_inputs']))
            if any(p.startswith(pre) for p in extra for pre in ISOLATION_FORBIDDEN_PREFIXES):
                raise Rejected('coherent evidence tampering: undeclared read (' + side + ')')
            raise Rejected('coherent evidence tampering: snapshot inventory (' + side + ')')
        if any(inv[k] != c['declared_hashes'][k] for k in inv):
            raise Rejected('coherent evidence tampering: snapshot hash (' + side + ')')
    if sorted(pk['controls']) != sorted(c['control_ids']) or any(pk['controls'][k] is not True for k in pk['controls']):
        raise Rejected('coherent evidence tampering: control booleans')
    if has_float(pk):
        raise Rejected('exact arithmetic: float in packet')
    if pk['admission_reads_preview'] is not False:
        raise Rejected('exact arithmetic: preview read by admission')
    for key in ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified'):
        if pk['claims'].get(key) is not False:
            raise Rejected('no priority or continuum claim: ' + key)
    if pk['provenance_premises'] != []:
        raise Rejected('no priority or continuum claim: historical provenance as premise')
    if pk['model_id'] != MODEL_ID or pk['model_is_finite_graph'] is not True or pk['transfers_to_aq'] is not False:
        raise Rejected('one plaquette model terms: model label')
    par = pk['parameters']
    for key in ('metric', 'weights', 'window', 'clock'):
        if key not in par or not par[key]:
            raise Rejected('parameters must declare metric weights window: ' + key)
        if key != 'metric' and not par[key].startswith('not applicable'):
            raise Rejected('parameters must declare metric weights window: ' + key + ' without reason')
    if pk['convention'] != CONVENTION:
        raise Rejected('frozen convention used: convention')
    # cells ---------------------------------------------------------------------------------------------------
    cells = pk['cells']
    if sorted(cells) != sorted(GROUPS):
        missing = sorted(set(GROUPS) - set(cells))
        if 'SU(3)' in missing:
            raise Rejected('su3 obstruction mandatory: cell missing')
        if 'SO(3)' in missing:
            raise Rejected('so3 obstruction mandatory: cell missing')
        if 'SU(5)' in missing:
            raise Rejected('su5 flip obstruction fourth order: cell missing')
        raise Rejected('insufficient verdict retained: group cell missing')
    ref = c['cells']
    for name in GROUPS:
        cell, r = cells[name], ref[name]
        if cell['group'] != name or cell['wilson_rep'] != WILSON_REP[name]:
            raise Rejected('changed model relabelled: group or representation')
        if cell['model'] != 'H_FG(G)' or cell['model_is_finite_graph'] is not True or cell['transfers_to_aq'] is not False:
            if cell['model'] != 'H_FG(G)':
                raise Rejected('changed model relabelled: one-plaquette value under another model')
            raise Rejected('one plaquette model terms: cell labels')
        if cell['hamiltonian_terms'] != ONE_PLAQUETTE_TERMS or cell['free_reference_same_code_path'] is not True:
            raise Rejected('one plaquette model terms: terms or free reference')
        if cell['C_F'] != r['C_F']:
            raise Rejected('frozen convention used: C_F (' + name + ')')
        mom = cell['moments']
        if set(mom) != {'characters', 'weyl_integration'}:
            raise Rejected('moment tables two routes: single route (' + name + ')')
        if mom['characters'] != mom['weyl_integration']:
            raise Rejected('moment tables two routes: routes disagree (' + name + ')')
        if cell.get('moment_tier') is not None:
            raise Rejected('tier mixing: tier on a moment')
        if mom['characters'] != r['moments']:
            raise Rejected('coherent evidence tampering: moment value (' + name + ')')
        fo = cell['first_order']
        if fo.get('tier') != 'exact_first_order':
            raise Rejected('tier mixing: first-order coefficient without the exact_first_order tier')
        if fo.get('route_of_computation') not in ('characters', 'weyl_integration'):
            if fo.get('route_of_computation') in PLAN_RECORD['plan_route_labels']:
                raise Rejected('tier mixing: plan route label')
            raise Rejected('tier mixing: route of computation')
        if fo.get('hypothesis_source') is not None:
            raise Rejected('tier mixing: hypothesis source')
        if fo['value'] != r['first_order']:
            if name != 'SU(2)' and fo['value'] == F(1, 144):
                raise Rejected('su2 constants not transferred: 1/144 under ' + name)
            if name == 'Z2' and fo['value'] in (F(1, 6), F(1, 12)):
                raise Rejected('frozen convention used: Z2 normalization')
            if fo['value'] == -r['first_order']:
                raise Rejected('frozen convention used: creation sign')
            raise Rejected('frozen convention used: first-order value (' + name + ')')
        if cell.get('dictionary') is not None and name != 'SU(2)':
            raise Rejected('su2 constants not transferred: dictionary for ' + name)
        for k in ('second_order_omega_W', 'first_derivative_omega_W2', 'fourth_order_omega_W'):
            rec = cell['higher'][k]
            if k == 'first_derivative_omega_W2':  # a first-order tau-derivative: tier exact_first_order (frozen text)
                if rec.get('tier') != 'exact_first_order':
                    raise Rejected('tier mixing: first-order derivative without the exact_first_order tier')
            elif rec.get('tier') is not None:
                raise Rejected('tier mixing: tier on a higher-order coefficient')
            if rec.get('route_of_computation') not in ('characters', 'weyl_integration'):
                if rec.get('route_of_computation') in PLAN_RECORD['plan_route_labels']:
                    raise Rejected('tier mixing: plan route label')
                raise Rejected('tier mixing: route on a higher-order coefficient')
            if rec['value'] != r[k]:
                if name == 'SU(5)' and k == 'fourth_order_omega_W':
                    raise Rejected('su5 flip obstruction fourth order: fourth-order value')
                if name == 'SU(3)':
                    raise Rejected('su3 obstruction mandatory: coefficient value')
                if name == 'SO(3)':
                    raise Rejected('so3 obstruction mandatory: coefficient value')
                raise Rejected('coherent evidence tampering: higher-order value (' + name + ')')
        # criterion A (flip column)
        cz = cell['central_minus_one']
        if cz['exists'] != r['central_minus_one']:
            raise Rejected('flip criterion central minus one: centre analysis (' + name + ')')
        if cell['flip'] == 'transfer':
            if not cz['exists']:
                raise Rejected('flip criterion central minus one: flip claimed without a central -1 (' + name + ')')
            if cell['flip_models'] != ['H_FG(G)', 'H^G_N'] or cell['flip_commutes'] != ['Casimirs', 'gauge actions',
                                                                                        'on-site cutoffs']:
                raise Rejected('flip criterion central minus one: models or commutation list')
        elif cell['flip'] == 'obstruction':
            if cz['exists']:
                raise Rejected('flip criterion central minus one: obstruction with a central -1')
            ce = cell.get('flip_counterexample')
            if not ce or ce.get('coefficient') not in ('second_order_omega_W', 'fourth_order_omega_W') \
                    or cell['higher'][ce['coefficient']]['value'] == 0:
                if name == 'SU(5)':
                    raise Rejected('su5 flip obstruction fourth order: missing counterexample')
                raise Rejected('flip criterion central minus one: obstruction from the missing central element alone')
            if name == 'SU(5)' and ce['coefficient'] != 'fourth_order_omega_W':
                raise Rejected('su5 flip obstruction fourth order: counterexample order')
        else:
            raise Rejected('flip criterion central minus one: flip column')
        # criterion B (parity column)
        if cell['parity'] == 'transfer':
            if r['third_moment'] != 0:
                if name == 'SU(3)':
                    raise Rejected('su3 obstruction mandatory: SU(3) called a transfer')
                if name == 'SO(3)':
                    raise Rejected('so3 obstruction mandatory: SO(3) called a transfer')
                raise Rejected('parity criterion third moment: parity claimed with E[W^3] nonzero')
            if cell['single_occurrence_orthogonality'] is not True or cell['whole_level_splitting_zero'] is not True:
                raise Rejected('parity criterion third moment: single occurrence or whole level')
        elif cell['parity'] == 'obstruction':
            if r['third_moment'] == 0:
                if name == 'SU(5)':
                    raise Rejected('su5 flip obstruction fourth order: SU(5) called a parity obstruction')
                raise Rejected('parity criterion third moment: obstruction with E[W^3]=0')
        else:
            raise Rejected('parity criterion third moment: parity column')
        if cell.get('columns_merged') is not False:
            raise Rejected('parity criterion third moment: flip and parity merged')
        if cell['label'] == 'prediction' or cell['label'] == 'confirmation':
            raise Rejected('no transfer called prediction: label')
        if name != 'SU(2)' and cell['am2_chain'] is not False:
            raise Rejected('am2 not reinstantiated: ' + name)
    for name in ('SU(3)', 'SO(3)'):
        cell = cells[name]
        if cell['flip'] != 'obstruction' or cell['parity'] != 'obstruction':
            raise Rejected(('su3' if name == 'SU(3)' else 'so3') + ' obstruction mandatory: called a transfer')
    s5 = cells['SU(5)']
    if s5['flip'] != 'obstruction':
        raise Rejected('su5 flip obstruction fourth order: SU(5) called a flip transfer')
    if s5['higher']['fourth_order_omega_W'].get('route_of_computation') is None:
        raise Rejected('su5 flip obstruction fourth order: route')
    # flip sets ----------------------------------------------------------------------------------------------
    fs = pk['flip_sets']
    if fs['E3_boxes'] != c['flip_sets']['E3_boxes'] or fs['E2_boxes'] != c['flip_sets']['E2_boxes'] \
            or fs['E3_factors'] != c['flip_sets']['E3_factors'] or fs['classes_odd'] != 24:
        raise Rejected('flip sets verified: enumeration')
    if fs['periodic_odd_side'] != 'obstruction':
        raise Rejected('flip sets verified: periodic odd side verified')
    # area parity -----------------------------------------------------------------------------------------------
    ap = pk['area_parity']
    if ap['group'] != 'SU(2)' or ap['family'] != 'zero-selected patterned family' or ap['kappa'] != '0':
        raise Rejected('area parity scope: family or kappa')
    if ap['boxes'] != ['open centered whole-star boxes (F1)', 'every on-site cutoff']:
        raise Rejected('area parity scope: boxes')
    if ap['limit'] != 'limit of the named constructions through BB2 whole-sequence convergence at each sign':
        raise Rejected('area parity scope: limit passage')
    if ap['periodic_odd_side'] is not False or ap['kappa_nonzero'] is not False or ap['F2_or_literal'] is not False:
        raise Rejected('area parity scope: excluded boxes claimed')
    if ap['surface_independence'] != 'proved from |C cap E_3|' or ap['casimirs'] != 'bounded spectral cutoffs and monotone limit':
        raise Rejected('area parity scope: surface or Casimir step')
    # ledger, obligations, wording -------------------------------------------------------------------------------
    rows = pk['ledger']
    if sorted((r_['group'], r_['equation']) for r_ in rows) != sorted(c['ledger_keys']):
        raise Rejected('insufficient verdict retained: ledger incomplete')
    for r_ in rows:
        if r_['status'] == 'obstruction' and not r_.get('counterexample'):
            raise Rejected('no transfer called prediction: non-transfer without counterexample')
        if r_['equation'] == 'dictionary' and r_['group'] != 'SU(2)' and r_['status'] != 'not asserted':
            raise Rejected('su2 constants not transferred: dictionary row')
    if sorted(pk['obligations']) != sorted(c['obligations']):
        raise Rejected('am2 not reinstantiated: obligations')
    for text in strings([pk['statements'], pk['sentence']]):
        if placeholder_spans(text):
            raise Rejected('placeholder span')
    for text in pk['statements']:
        hits = affirmative_hits(text, c['forbidden'], c['sentence'])
        if hits:
            if any(h in ('predicts', 'confirms') for h in hits):
                raise Rejected('no transfer called prediction: ' + hits[0])
            raise Rejected('negation aware phrase scan: ' + hits[0])
    if pk['sentence'] != c['sentence'] or pk['sentence_count'] != 1:
        raise Rejected('mandatory sentence template')
    if pk['sub_labels'] != SUB_LABELS:
        raise Rejected('changed model relabelled: sub-labels')
    for name_, ratio in pk['scaling'].items():
        if ratio != c['scaling'][name_]:
            raise Rejected('insufficient verdict retained: scaling ratio ' + name_)
    gf = pk['gate_fields']
    agree = all(cells[g]['moments']['characters'] == ref[g]['moments'] for g in GROUPS)
    if pk['verdict'] == 'accepted_within_scope' and (not agree or pk['retuned'] is not False):
        raise Rejected('insufficient verdict retained: accepted with a failed item or retuning')
    if pk['verdict'] != 'accepted_within_scope' and not pk.get('dominating_reason'):
        raise Rejected('insufficient verdict retained: reason')
    want = c['gate_fields'] if pk['verdict'] == 'accepted_within_scope' else pk['gate_fields']
    for key in sorted(c['gate_fields']):
        if key not in gf:
            raise Rejected('gate field missing: ' + key)
        if key in ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified') and gf[key] is not False:
            raise Rejected('no priority or continuum claim: ' + key)
        if key == 'flip_transfer_scope':
            continue  # the frozen value is a description; gate_fields_rule: the exported scope names the groups found
        if gf[key] != want[key]:
            raise Rejected('gate field: ' + key)
    if gf['flip_transfer_claimed'] is True:
        m = re.match(r'groups: ([^;]*); ', gf['flip_transfer_scope'])
        named = [x.strip() for x in m.group(1).split(',')] if m else []
        if named != [n for n in GROUPS if ref[n]['central_minus_one']]:
            raise Rejected('flip criterion central minus one: gate scope does not name exactly the flip groups')
        if 'H_FG(G)' not in gf['flip_transfer_scope'] or 'H^G_N' not in gf['flip_transfer_scope'] \
                or 'no AM2, AV1 or AQ statement for any group other than SU(2)' not in gf['flip_transfer_scope']:
            raise Rejected('flip criterion central minus one: gate scope models')
    for name in c['error_terms']:
        entry = pk['error_terms'].get(name)
        if entry is None:
            raise Rejected('error term missing: ' + name)
        if entry.startswith('not_applicable') and len(entry) <= len('not_applicable') + 3:
            raise Rejected('error term missing: not_applicable without a reason (' + name + ')')
    return True


# ------------------------------------------------------------------------------------------------ execute
def execute():
    # 1. provenance --------------------------------------------------------------------------------------------------
    cb = (ROOT / CONTRACT_REL).read_bytes()
    c_sha = hashlib.sha256(cb).hexdigest()
    need(c_sha == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=c_sha)
    con = json.loads(cb)
    par, pre = con['parameters'], con['preregistration']
    need(con['status'] == 'frozen_before_production' and con['id'] == 'BD1' and con['direction'] == 'paired'
         and con['producers'] == ['forward', 'reverse'] and con['reverse_premise_isolation'] is True
         and par['groups'] == GROUPS and pre['model_id'] == MODEL_ID and pre['selected_triple_alpha_units'] == ['0', '0', '0']
         and con['selected_after'] == 'research/round33/advisor/bb2-gate.json',
         'contract_frozen_paired', frozen_at=con['frozen_at'])
    for rel, want in sorted(GATES.items()):
        if sha(rel) != want:
            raise CheckFailure('gate hash ' + rel)
    for rel, want in sorted(EARLIER_CONTRACTS.items()):
        if sha(rel) != want:
            raise CheckFailure('earlier contract hash ' + rel)
    gates = {rel: json.loads((ROOT / rel).read_text()) for rel in GATES}
    need(all(g['verdict'] == 'accepted_within_scope' for g in gates.values()) and all(rel in con['shared_premises']
                                                                                     for rel in GATES),
         'premise_gates_pinned_and_accepted', gates=sorted(GATES))
    declared = sorted(set(['AGENTS.md', CONTRACT_REL] + con['shared_premises']))
    for rel, want in OBSERVED_INPUTS.items():
        if sha(rel) != want:
            raise CheckFailure('inventory hash ' + rel)
    need(sorted(OBSERVED_INPUTS) == declared and len(declared) == 23
         and not any(p.startswith(ISOLATION_FORBIDDEN_PREFIXES) for p in declared),
         'producer_inventories_equal_contract', files=len(declared),
         note='forward/bd1/inputs and reverse/bd1/inputs were listed by find (names only) and hashed: both hold the same '
              '23 files, each byte-identical to the repository; no plan, panel, expert or skeptic review file')

    # 2. pre-freeze edits -------------------------------------------------------------------------------------------
    need(sha(REVIEW_REL) == REVIEW_SHA256, 'bd_contract_review_pinned')
    rev = json.loads((ROOT / REVIEW_REL).read_text())
    applied = []
    for e in rev['blocking_edits'] + rev['non_blocking_edits']:
        if e['contract'] != 'bd1':
            continue
        if e['op'] in ('replace', 'add'):
            ok = has_key_path(con, e['path']) and get_path(con, e['path']) == e['replacement']
        elif e['op'] == 'append':
            ok = e['replacement'] in get_path(con, e['path'])
        else:
            ok = False
        if not ok:
            raise CheckFailure('pre-freeze edit not in the frozen bytes: ' + e['path'])
        applied.append(e['path'])
    need(len(applied) == 24, 'prefreeze_edits_verbatim_in_frozen_bytes', edits=len(applied),
         note='15 blocking and 9 non-blocking BD1 edits of the pre-freeze review are verbatim; its previews are not read')

    # 3. controls, semantics, vocabulary, template ------------------------------------------------------------------
    ids = con['controls']
    need(ids == pre['controls_required']['ids'] and len(ids) == 22 and len(set(ids)) == 22, 'control_mirror_22')
    earlier = {rel: json.loads((ROOT / rel).read_text()) for rel in EARLIER_CONTRACTS}
    own = [i for i in ids if i in con['new_control_semantics']]
    inherited = {}
    for i in ids:
        if i in own:
            continue
        src = [rel for rel in sorted(EARLIER_CONTRACTS) if i in earlier[rel].get('new_control_semantics', {})]
        if not src:
            raise CheckFailure('control without semantics ' + i)
        inherited[i] = src[0]
    need(len(own) == 16 and len(inherited) == 6, 'control_semantics_coverage', own=len(own), inherited=inherited)
    need(sorted(pre['gate_fields_required']) == sorted(PLAN_RECORD['gate_fields'])
         and pre['tier_names_allowed'] == ['exact_first_order'] and pre['sub_labels_allowed'] == SUB_LABELS,
         'plan_vocabulary_covers_gate_fields', plan_sha256=PLAN_RECORD['sha256_at_bd_freeze_commit'])
    forbidden = sorted(set(ROUND_FORBIDDEN + pre['forbidden_phrasings'] + PLAN_RECORD['forbidden']))
    template = pre['mandatory_sentence_template']
    need(affirmative_hits(template, forbidden) == [] and placeholder_spans(template) == []
         and 'SU(5) is a recorded flip obstruction with an exact nonzero fourth-order coefficient' in template
         and 'not statements for periodic boxes with an odd side' in template, 'mandatory_template_scans_clean')
    need(all(par[k].startswith('not applicable') for k in ('weights', 'window', 'clock')) and 'metric' in par,
         'parameters_declare_metric_weights_window_frozen')

    # 4. anchors from the admitted record -----------------------------------------------------------------------------
    aw1 = gates['research/round32/advisor/aw1-gate.json']['accepted']
    need('E[W]=E[W^3]=0, E[W^2]=1/4, E[W^4]=1/8' in aw1 and 'omega_tau(W)=+tau/144+r(tau)' in aw1
         and 'E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even}' in aw1, 'aw1_su2_anchors_parsed')
    aw1_rep = (ROOT / AW1_F_REL).read_text()
    m3 = re.search(r'<W>=tau/144\+0\S*tau\^2-\((\d+)/(\d+)\)tau\^3', aw1_rep)
    su2_third = -F(int(m3.group(1)), int(m3.group(2)))
    need(su2_third == F(-5, 11943936), 'aw1_one_plaquette_third_order_parsed', value=q_(su2_third))
    az1 = gates['research/round32/advisor/az1-gate.json']['accepted']
    need('tau=24 lambda/alpha=96/g^4' in az1 and 'alpha=g^2/(2a)' in az1, 'su2_dictionary_located_in_az1',
         note='the SU(2) dictionary tau=96/g^4 and alpha=g^2/(2a) is an AZ1 (AL1) statement; it is never used for another group')

    # 5. group cells --------------------------------------------------------------------------------------------------
    cells_ref, table = {}, {}
    for name in GROUPS:
        g = group(name)
        mA, mB, mC = moments_characters(g, 5), moments_weyl(name, 5), moments_third(name, 5)
        if not (mA == mB == mC):
            raise CheckFailure('moment routes disagree for ' + name)
        c1A = F(2, 3) * mA[1] / (32 * g.CF)
        c1B = F(2, 3) * mB[1] / (32 * g.CF)
        om, om2, E, nb = one_plaquette_rs(g, 4, 6)
        om_b, om2_b, E_b, nb_b = one_plaquette_rs(g, 4, 7)
        if (om, om2, E) != (om_b, om2_b, E_b):
            raise CheckFailure('one-plaquette truncation dependence for ' + name)
        if name != 'Z2' and nb_b <= nb:
            raise CheckFailure('basis did not grow for ' + name)
        if not (om[0] == 0 and om2[0] == mA[1] and om[1] == c1A == c1B):
            raise CheckFailure('free reference or first order for ' + name)
        hf = all(om[n] == -3 * (n + 1) * E[n + 1] for n in range(5))  # Hellmann-Feynman omega(W) = -3 dE/dtau
        if not hf:
            raise CheckFailure('Hellmann-Feynman consistency for ' + name)
        cz = g.centre()
        third = mA[2]
        cells_ref[name] = {'C_F': g.CF, 'moments': mA[:4], 'fifth_moment': mA[4], 'first_order': c1A,
                           'second_order_omega_W': om[2], 'first_derivative_omega_W2': om2[1],
                           'third_order_omega_W': om[3], 'fourth_order_omega_W': om[4],
                           'central_minus_one': cz['minus_one_element'] is not None, 'third_moment': third,
                           'centre': cz, 'basis_size': nb}
        table[name] = {'moments_E[W^k]_k=1..5': [q_(x) for x in mA], 'C_F': q_(g.CF), 'face_energy_32C_F': q_(32 * g.CF),
                       'first_order_coefficient': q_(c1A), 'omega_W_series_0..4': [q_(x) for x in om],
                       'omega_W2_series_0..1': [q_(x) for x in om2[:2]], 'energy_series_0..5': [q_(x) for x in E],
                       'centre': cz, 'basis_irreps': nb}
    need(True, 'moments_three_routes_agree', table={n: table[n]['moments_E[W^k]_k=1..5'] for n in GROUPS},
         routes=['characters (Pieri/Clebsch-Gordan)', 'weyl_integration (constant-term extraction)',
                 'labelled third route (Frobenius hook lengths, central binomials, Catalan inverse binomial transform)'])
    trap = {n: moments_weyl(n, 5, unitary_torus=True) for n in ('SU(3)', 'SU(4)', 'SU(5)')}
    need(trap['SU(3)'][2] == 0 != cells_ref['SU(3)']['moments'][2] and trap['SU(5)'][4] == 0 != cells_ref['SU(5)']['fifth_moment']
         and trap['SU(4)'][:3] == cells_ref['SU(4)']['moments'][:3] and trap['SU(4)'][3] == F(3, 1024)
         and cells_ref['SU(4)']['moments'][3] == F(7, 2048), 'weyl_route_torus_trap',
         unitary_torus_moments={n: [q_(x) for x in v] for n, v in trap.items()},
         note='labelled trap: constant-term extraction on the U(N) torus (exponent 0 only) drops the determinant terms '
              'and gives E[W^3]=0 for SU(3), E[W^4]=3/1024 instead of 7/2048 for SU(4) and E[W^5]=0 for SU(5); the SU(N) '
              'torus keeps z^{c(1,...,1)}; a reverse '
              'route on the wrong torus would silently turn the SU(3) obstruction into a parity transfer')
    need(cells_ref['SU(2)']['moments'] == [0, F(1, 4), 0, F(1, 8)] and cells_ref['SU(2)']['first_order'] == F(1, 144)
         and cells_ref['SU(2)']['third_order_omega_W'] == su2_third and group('SU(2)').CF * 32 == 24,
         'su2_convention_check_reproduces_aw1',
         note='1/144, the AW1 moments and the AW1 one-plaquette third-order coefficient -5/11943936 are reproduced; a '
              'check of the frozen convention, not a transferred value')
    fo = {n: cells_ref[n]['first_order'] for n in GROUPS}
    need(fo == {'SU(2)': F(1, 144), 'SU(3)': F(1, 1152), 'SU(4)': F(1, 2880), 'SU(5)': F(1, 5760), 'U(1)': F(1, 96),
                'Z2': F(1, 48), 'SO(3)': F(1, 864)}
         and all(fo['SU(%d)' % n] == F(1, 48 * n * (n * n - 1)) for n in (3, 4, 5)),
         'first_order_coefficients_frozen_convention', values={k: q_(v) for k, v in fo.items()},
         note='tier exact_first_order; both routes of computation give the same rational; SU(N), N>=3: 1/(48N(N^2-1))')
    z2_alt = {'electric 1 on the odd link state (face energy 4)': F(2, 3) / 4, '1 - sigma^x (face energy 8)': F(2, 3) / 8}
    need(fo['Z2'] == F(1, 48) and all(v != fo['Z2'] for v in z2_alt.values()), 'z2_normalization_discriminates',
         rejected_readings={k: q_(v) for k, v in z2_alt.items()})
    # the literal AW1 display 2(W Omega_0, c^(1)) gives the opposite sign
    need(all(-2 * (-F(1, 3) / (32 * group(n).CF)) * cells_ref[n]['moments'][1] == fo[n] for n in GROUPS)
         and all(2 * (-F(1, 3) / (32 * group(n).CF)) * cells_ref[n]['moments'][1] == -fo[n] for n in GROUPS),
         'creation_sign_convention', note='omega(W) = -2 Re(W Omega_0, c^(1)) with c^(1) = -(tau/3)/(32C_F) W Omega_0; '
                                          'the literal display 2(W Omega_0, c^(1)) gives -c1 for every group')

    # Weyl character formula verification of the Pieri tables on the RS bases
    points = [(F(2), F(3), F(5), F(7), F(11)), (F(1, 2), F(-3), F(4, 3), F(5, 7), F(-2, 9))]
    verified = 0
    for n in (2, 3, 4, 5):
        g = group('SU(%d)' % n)
        for lam in sorted(reachable(g, 6)):
            for z in points:
                zz = z[:n]
                up = sum((schur_at(mu, zz) for mu in pieri_up(lam)), F(0))
                dn = sum((schur_at(mu, zz) for mu in pieri_down(lam)), F(0))
                s = schur_at(lam, zz)
                if sum(zz, F(0)) * s != up or sum((1 / zi for zi in zz), F(0)) * s != dn:
                    raise CheckFailure('Pieri table disagrees with the Weyl character formula')
                verified += 1
    need(True, 'pieri_tables_weyl_character_formula', identities_checked=2 * verified,
         note='chi_fund chi_lam and chi_antifund chi_lam equal the Pieri sums as GL(N) bialternant identities at two '
              'exact rational points for every irrep of the SU(N) Rayleigh-Schroedinger bases (N=2..5)')

    # obstruction cells
    ob = {}
    for name in ('SU(3)', 'SO(3)'):
        g, r = group(name), cells_ref[name]
        e3 = moments_weyl(name, 3)[2]
        d_w2 = F(2, 3) * e3 / (32 * g.CF)
        c2 = e3 / (3 * (32 * g.CF) ** 2)
        if not (e3 != 0 and d_w2 == r['first_derivative_omega_W2'] != 0 and c2 == r['second_order_omega_W'] != 0):
            raise CheckFailure('obstruction closed forms for ' + name)
        ob[name] = {'E[W^3]': q_(e3), 'd omega(W^2)/dtau at 0': q_(d_w2), 'second_order_omega_W': q_(c2)}
    need(ob['SU(3)'] == {'E[W^3]': '1/108', 'd omega(W^2)/dtau at 0': '1/6912', 'second_order_omega_W': '1/589824'}
         and ob['SO(3)'] == {'E[W^3]': '1/27', 'd omega(W^2)/dtau at 0': '1/2592', 'second_order_omega_W': '1/331776'},
         'su3_so3_obstruction_cells', cells=ob,
         note='closed forms (2/3)E[W^3]/(32C_F) and E[W^3]/(3(32C_F)^2) (W Omega_0 is an exact H_0 eigenvector) equal the '
              'Rayleigh-Schroedinger series; omega(W) is not odd in tau for SU(3) and SO(3)')
    # SU(5): Z_5 column path closed form for the fourth-order coefficient
    s5 = group('SU(5)')
    cols = [tuple([1] * k + [0] * (5 - k)) for k in range(1, 5)]
    path = F(1)
    for lam in cols:
        path /= 32 * s5.cas(lam)
    closed4 = 15 * F(1, 3) ** 5 * 2 * F(1, 10) ** 5 * path  # omega_4 = -15 E_5, E_5 = (-1/3)^5 <W Om, (R W)^4 Om>
    r5 = cells_ref['SU(5)']
    need(r5['moments'][2] == 0 and r5['second_order_omega_W'] == 0 and r5['first_derivative_omega_W2'] == 0
         and r5['fourth_order_omega_W'] == closed4 == F(1, 63403380965376) and r5['fifth_moment'] == F(1, 50000)
         and [s5.cas(l) for l in cols] == [F(12, 5), F(18, 5), F(18, 5), F(12, 5)],
         'su5_parity_transfer_flip_obstruction', fourth_order=q_(closed4), preview=preview(closed4),
         note='E[W^3]=0 (parity column a transfer); both SU(3)/SO(3) coefficients vanish by the Z_5 grading; the first '
              'possible nonzero even order is 4, and the column path 1 -> Lambda^1 -> ... -> Lambda^5 = 1 (and its '
              'conjugate) gives omega_4 = 30/(243*10^5*prod_k 32 C_2(Lambda^k)) exactly, equal to the series')
    need(all(cells_ref[n][k] == 0 for n in ('SU(2)', 'SU(4)', 'U(1)', 'Z2')
             for k in ('second_order_omega_W', 'fourth_order_omega_W', 'first_derivative_omega_W2')),
         'flip_groups_even_orders_vanish', note='consistent with the flip identity: omega(W) odd in tau on H_FG(G)')

    # criterion A: one-plaquette grading; criterion B: level at 32 C_F and cubic moments
    crit = {}
    for name in GROUPS:
        g, r = group(name), cells_ref[name]
        basis = reachable(g, 6)
        if r['central_minus_one']:
            if any(g.charge(lam) is None for lam in basis):
                raise CheckFailure('central -1 claimed for a group without a centre grading: ' + name)
            ok = all(g.charge(mu) % 2 != g.charge(lam) % 2 for lam in basis for mu in g.W(lam))
            if not ok:
                raise CheckFailure('flip grading fails for ' + name)
        level = sorted((lam for lam in basis if g.cas(lam) == g.CF), key=repr)
        nontriv_min = min(g.cas(lam) for lam in basis if lam != g.triv)
        comp = {repr(a): {repr(b): apply_W(g, {b: F(1)}, basis).get(a, F(0)) for b in level} for a in level}
        zero = all(v == 0 for row in comp.values() for v in row.values())
        if zero != (r['third_moment'] == 0) or nontriv_min != g.CF:
            raise CheckFailure('criterion B level for ' + name)
        crit[name] = {'level_irreps_at_C_F': [repr(x) for x in level], 'level_compression_zero': zero}
    cubic = {}
    for n in (2, 3, 4, 5):
        vals = [mixed_moment_frobenius(n, a, 3 - a) for a in range(4)]
        cubic['SU(%d)' % n] = vals
        if (sum(comb(3, a) * v for a, v in enumerate(vals)) == 0) != (cells_ref['SU(%d)' % n]['third_moment'] == 0):
            raise CheckFailure('cubic moments')
    need(all(v >= 0 for vals in cubic.values() for v in vals), 'criteria_a_b_one_plaquette', levels=crit,
         cubic_moments_E_chi_a_chibar_b={k: v for k, v in cubic.items()},
         note='criterion A: U = (-1)^{N-ality} anticommutes with W and commutes with 32 C_2 exactly for SU(2), SU(4), U(1), '
              'Z2; criterion B: the compression of W to the level at 32 C_F vanishes exactly iff E[W^3]=0, and E[W^3]=0 '
              'iff every cubic moment E[chi^a chibar^b] (a nonnegative integer) vanishes')
    need([n for n in GROUPS if cells_ref[n]['central_minus_one']] == ['SU(2)', 'SU(4)', 'U(1)', 'Z2']
         and [n for n in GROUPS if cells_ref[n]['third_moment'] == 0] == ['SU(2)', 'SU(4)', 'SU(5)', 'U(1)', 'Z2'],
         'transfer_columns', flip=['SU(2)', 'SU(4)', 'U(1)', 'Z2'], parity=['SU(2)', 'SU(4)', 'SU(5)', 'U(1)', 'Z2'],
         obstructions={'flip': ['SU(3)', 'SU(5)', 'SO(3)'], 'parity': ['SU(3)', 'SO(3)']})

    # 6. flip sets -----------------------------------------------------------------------------------------------------
    cls_ok = all(sum(1 for l in face_links(p, a, c) if in_E3(l)) in (1, 3)
                 for p in product(range(2), repeat=3) for a, c in ORIENT)
    e3_boxes = {}
    for nbox in (2, 3, 4):
        plaqs, retained = box_data(nbox)
        cnt = [sum(1 for l in face_links(*f) if in_E3(l)) for f in plaqs]
        if any(k % 2 == 0 for k in cnt):
            raise CheckFailure('E_3 meets a plaquette evenly')
        e3_boxes[str(nbox)] = {'plaquettes': len(plaqs), 'met_once': cnt.count(1), 'met_three_times': cnt.count(3),
                               'retained_whole_star_faces': len(retained)}
    need(cls_ok and e3_boxes['2'] == {'plaquettes': 2335, 'met_once': 1082, 'met_three_times': 1253,
                                      'retained_whole_star_faces': 1344}, 'flip_set_E3_boxes', boxes=e3_boxes,
         note='N=2 reproduces AW1 (2335 plaquettes, 1082/1253, 1344 retained faces); 24 classes odd')
    factors = {}
    for b in ((0, 0, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (1, 1, 1), (-1, -1, -1), (2, -3, 5)):
        links = [((4 * b[0] + r, 2 * b[1] + s, b[2]), d) for r in range(4) for s in range(2) for d in 'xyz']
        lset = set(links)
        faces = set()
        for (p, d) in links:
            for a, c in ORIENT:
                if d not in (a, c):
                    continue
                other = c if d == a else a
                for base in (p, add(p, tuple(-x for x in DIRS[other]))):
                    if (p, d) in face_links(base, a, c):
                        faces.add((base, a, c))
        if not all(any(l in lset for l in face_links(*f)) for f in faces):
            raise CheckFailure('factor faces')
        if any(sum(1 for l in face_links(*f) if in_E3(l)) % 2 == 0 for f in faces):
            raise CheckFailure('E_3 even on a factor face')
        factors[str(b)] = {'E3_links_in_factor': sum(1 for l in links if in_E3(l)), 'faces_meeting_factor': len(faces)}
    need(all(v['E3_links_in_factor'] == (16 if eval(k)[2] % 2 == 0 else 8) for k, v in factors.items())
         and all(v['faces_meeting_factor'] == 52 for v in factors.values()),
         'flip_set_E3_coarse_factors', factors=factors,
         note='E_3 meets a 24-link factor in 16 links (b_z even) or 8 (b_z odd): not invariant under odd coarse z '
              'translations, which the lemma does not need; every face meeting a factor meets E_3 oddly')
    e2_boxes = {}
    for nbox in (2, 3, 4):
        plaq2 = [((x, y, 0), 'x', 'y') for x in range(-nbox, nbox) for y in range(-nbox, nbox)]
        cnt = [sum(1 for l in face_links(*f) if in_E2(l)) for f in plaq2]
        if any(k != 1 for k in cnt):
            raise CheckFailure('E_2 does not meet a plaquette exactly once')
        e2_boxes[str(nbox)] = {'plaquettes': len(plaq2), 'met_exactly_once': len(plaq2)}
    need(True, 'flip_set_E2_boxes', boxes=e2_boxes)
    # periodic tori with an odd side: some seam plaquette meets the flip set evenly
    def torus_even(sides, flip):
        dims = len(sides)
        even = 0
        for p in product(*[range(L) for L in sides]):
            orients = ORIENT if dims == 3 else (('x', 'y'),)
            for a, c in orients:
                pp = p if dims == 3 else (p[0], p[1], 0)
                links = [(tuple(v % L for v, L in zip(q, sides + ((1,) if dims == 2 else ()))), d)
                         for q, d in face_links(pp, a, c)]
                if sum(1 for l in links if flip(l)) % 2 == 0:
                    even += 1
        return even
    seam = {'E3_sides_4_4_4': torus_even((4, 4, 4), in_E3), 'E3_sides_3_4_4': torus_even((3, 4, 4), in_E3),
            'E3_sides_4_3_4': torus_even((4, 3, 4), in_E3), 'E3_sides_4_4_3': torus_even((4, 4, 3), in_E3),
            'E2_sides_4_4': torus_even((4, 4), in_E2), 'E2_sides_4_3': torus_even((4, 3), in_E2),
            'E2_sides_3_4': torus_even((3, 4), in_E2)}
    need(seam == {'E3_sides_4_4_4': 0, 'E3_sides_3_4_4': 16, 'E3_sides_4_3_4': 16, 'E3_sides_4_4_3': 16,
                  'E2_sides_4_4': 0, 'E2_sides_4_3': 4, 'E2_sides_3_4': 0}, 'periodic_odd_side_obstruction',
         even_plaquettes=seam,
         note='on a periodic side of odd length the two parallel keyed links of a seam plaquette are both in (or both '
              'out of) the flip set, so seam plaquettes are met evenly; recorded as an obstruction, never verified; '
              'even sides give no even plaquette; E_2 is keyed to p_y only, so an odd x side alone is harmless')

    # 7. area parity -----------------------------------------------------------------------------------------------------
    loops = 0
    for a, c in ORIENT:
        for w in range(1, 4):
            for h in range(1, 4):
                for off in product(range(2), repeat=3):
                    surf = [(add(off, add(tuple(i * x for x in DIRS[a]), tuple(j * x for x in DIRS[c]))), a, c)
                            for i in range(w) for j in range(h)]
                    loop = loop_links(surf)
                    alt = set(surf) ^ set(cube_faces(off))
                    if loop_links(sorted(alt)) != loop:
                        raise CheckFailure('alternative surface boundary')
                    k = sum(1 for l in loop if in_E3(l))
                    if k % 2 != len(surf) % 2 or k % 2 != len(alt) % 2:
                        raise CheckFailure('area parity rule')
                    loops += 1
    bent = [((0, 0, 0), 'x', 'y'), ((1, 0, 0), 'x', 'y'), ((2, 0, 0), 'x', 'z'), ((2, 0, 1), 'x', 'z'), ((0, 1, 0), 'x', 'y')]
    lshape = [((0, 0, 0), 'x', 'z'), ((1, 0, 0), 'x', 'z'), ((0, 0, 1), 'x', 'z')]
    extra = []
    for surf in (bent, lshape, [((0, 0, 0), 'x', 'z')], [((0, 0, 0), 'x', 'z'), ((1, 0, 0), 'x', 'z')]):
        loop = loop_links(surf)
        k = sum(1 for l in loop if in_E3(l))
        other = set(surf) ^ set(cube_faces((0, 0, 0))) ^ set(cube_faces((1, -1, 0)))
        if loop_links(sorted(other)) != loop or k % 2 != len(surf) % 2 or len(other) % 2 != len(surf) % 2:
            raise CheckFailure('area parity rule (non-planar)')
        extra.append({'faces': len(surf), 'loop_links': len(loop), 'C_cap_E3': k})
    need(extra[2]['C_cap_E3'] == 3 and extra[3]['C_cap_E3'] == 6, 'area_parity_rule_enumerated', planar_loops=loops,
         nonplanar_and_named=extra,
         note='|C cap E_3| = A(S) mod 2 for every enumerated loop and for alternative surfaces differing by cube '
              'boundaries; the W face meets E_3 three times (odd) and the 1x2 rectangle six times (even)')

    # 8. scaling ---------------------------------------------------------------------------------------------------------
    t = F(1, 10 ** 8)
    scaling = {'first_order_terms': (fo['SU(3)'] * t) / (fo['SU(3)'] * t / 100),
               'obstruction_second_order_terms': (cells_ref['SU(3)']['second_order_omega_W'] * t ** 2)
               / (cells_ref['SU(3)']['second_order_omega_W'] * (t / 100) ** 2),
               'su5_fourth_order_term': (closed4 * t ** 4) / (closed4 * (t / 100) ** 4), 'moments': F(1)}
    need(scaling == {'first_order_terms': 100, 'obstruction_second_order_terms': 10000,
                     'su5_fourth_order_term': 100000000, 'moments': 1}, 'scaling_brackets_exact',
         ratios={k: q_(v) for k, v in scaling.items()})

    # 9. ledger and obligations --------------------------------------------------------------------------------------------
    ledger = []
    for name in GROUPS:
        r = cells_ref[name]
        ledger.append({'group': name, 'equation': 'flip lemma', 'status': 'transfer' if r['central_minus_one'] else 'obstruction',
                       'reason': r['centre']['reason'],
                       'counterexample': None if r['central_minus_one'] else
                       ('fourth_order_omega_W' if name == 'SU(5)' else 'second_order_omega_W')})
        ledger.append({'group': name, 'equation': 'parity theorem', 'status': 'transfer' if r['third_moment'] == 0
                       else 'obstruction', 'reason': 'E[W^3]=%s' % q_(r['third_moment']),
                       'counterexample': None if r['third_moment'] == 0 else 'first_derivative_omega_W2'})
        ledger.append({'group': name, 'equation': 'first-order coefficient', 'status': 'transfer',
                       'reason': 'own cell value %s' % q_(r['first_order']), 'counterexample': None})
        ledger.append({'group': name, 'equation': 'dictionary', 'status': 'admitted (AZ1)' if name == 'SU(2)'
                       else 'not asserted', 'reason': 'tau=96/g^4 is an SU(2) statement', 'counterexample': None})
    obligations = sorted(['AM2 re-instantiation for %s (finite-volume ground state and gap)' % n for n in GROUPS if n != 'SU(2)']
                         + ['AQ chain for every group other than SU(2)', 'dictionary to a bare coupling for every group other than SU(2)',
                            'flip or parity for SU(2) at a nonzero selected triple', 'periodic boxes with an odd side',
                            'F2 and literal vertex boxes'])
    need(len(ledger) == 28 and len(obligations) == 11, 'transfer_ledger_complete', rows=len(ledger))

    # 10. packet and controls -------------------------------------------------------------------------------------------
    c_ref = {
        'declared_inputs': declared, 'declared_hashes': dict(OBSERVED_INPUTS), 'control_ids': ids, 'cells': cells_ref,
        'flip_sets': {'E3_boxes': e3_boxes, 'E2_boxes': e2_boxes, 'E3_factors': factors},
        'ledger_keys': [(r['group'], r['equation']) for r in ledger], 'obligations': obligations,
        'forbidden': forbidden, 'sentence': template, 'scaling': scaling,
        'gate_fields': pre['gate_fields_required'], 'error_terms': pre['error_terms_itemized'],
    }

    def build_packet():
        cells = {}
        for name in GROUPS:
            r = cells_ref[name]
            cells[name] = {
                'group': name, 'wilson_rep': WILSON_REP[name], 'model': 'H_FG(G)', 'model_is_finite_graph': True,
                'transfers_to_aq': False, 'hamiltonian_terms': copy.deepcopy(ONE_PLAQUETTE_TERMS),
                'free_reference_same_code_path': True, 'C_F': r['C_F'],
                'moments': {'characters': list(r['moments']), 'weyl_integration': list(r['moments'])},
                'first_order': {'value': r['first_order'], 'tier': 'exact_first_order',
                                'route_of_computation': 'characters'},
                'higher': {k: {'value': r[k], 'route_of_computation': 'characters',
                               'tier': 'exact_first_order' if k == 'first_derivative_omega_W2' else None}
                           for k in ('second_order_omega_W', 'first_derivative_omega_W2', 'fourth_order_omega_W')},
                'central_minus_one': {'exists': r['central_minus_one'], 'reason': r['centre']['reason']},
                'flip': 'transfer' if r['central_minus_one'] else 'obstruction',
                'flip_models': ['H_FG(G)', 'H^G_N'], 'flip_commutes': ['Casimirs', 'gauge actions', 'on-site cutoffs'],
                'flip_counterexample': None if r['central_minus_one'] else
                {'coefficient': 'fourth_order_omega_W' if name == 'SU(5)' else 'second_order_omega_W'},
                'parity': 'transfer' if r['third_moment'] == 0 else 'obstruction',
                'single_occurrence_orthogonality': True, 'whole_level_splitting_zero': r['third_moment'] == 0,
                'columns_merged': False, 'label': 'transfer_to_named_model' if r['central_minus_one'] or
                r['third_moment'] == 0 else 'obstruction_recorded', 'am2_chain': name == 'SU(2)',
                'dictionary': 'tau=96/g^4 (AZ1)' if name == 'SU(2)' else None,
            }
        pk = {
            'contract_sha256': CONTRACT_SHA256,
            'inputs': {'forward': dict(OBSERVED_INPUTS), 'reverse': dict(OBSERVED_INPUTS)},
            'controls': {k: True for k in ids}, 'admission_reads_preview': False,
            'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False},
            'provenance_premises': [], 'model_id': MODEL_ID, 'model_is_finite_graph': True, 'transfers_to_aq': False,
            'parameters': {k: par[k] for k in ('metric', 'weights', 'window', 'clock')},
            'convention': dict(CONVENTION), 'cells': cells,
            'flip_sets': {'E3_boxes': copy.deepcopy(e3_boxes), 'E2_boxes': copy.deepcopy(e2_boxes),
                          'E3_factors': copy.deepcopy(factors), 'classes_odd': 24, 'periodic_odd_side': 'obstruction'},
            'area_parity': {'group': 'SU(2)', 'family': 'zero-selected patterned family', 'kappa': '0',
                            'boxes': ['open centered whole-star boxes (F1)', 'every on-site cutoff'],
                            'limit': 'limit of the named constructions through BB2 whole-sequence convergence at each sign',
                            'periodic_odd_side': False, 'kappa_nonzero': False, 'F2_or_literal': False,
                            'surface_independence': 'proved from |C cap E_3|',
                            'casimirs': 'bounded spectral cutoffs and monotone limit'},
            'ledger': copy.deepcopy(ledger), 'obligations': list(obligations),
            'statements': ['The SU(4) cell is a transfer of the flip lemma to the named models, not an AM2 statement.',
                           'No statement is made for periodic boxes with an odd side.'],
            'sentence': template, 'sentence_count': 1, 'sub_labels': list(SUB_LABELS),
            'scaling': dict(scaling), 'verdict': 'accepted_within_scope', 'retuned': False,
            'gate_fields': dict(copy.deepcopy(pre['gate_fields_required']), flip_transfer_scope=FLIP_SCOPE),
            'error_terms': {k: 'itemized: exact (' + k + ')' for k in pre['error_terms_itemized']},
        }
        return rebind(pk)

    base = build_packet()
    need(validate(base, c_ref) is True, 'packet_validator_accepts_own_derivation')

    def mk(fn, rebind_after=True):
        def run():
            pk = build_packet()
            fn(pk)
            if rebind_after:
                rebind(pk)
            validate(pk, c_ref)
        return run

    def cellset(name, path, value):
        def f(pk):
            cur = pk['cells'][name]
            for k in path[:-1]:
                cur = cur[k]
            cur[path[-1]] = value
        return mk(f)

    def addst(text):
        return mk(lambda pk: pk['statements'].append(text))

    ctl, pos = {}, {}
    ctl['coherent_evidence_tampering'] = [
        ('control Boolean flipped and rebound', mk(lambda pk: pk['controls'].__setitem__(ids[3], False)),
         'coherent evidence tampering: control booleans'),
        ('reverse snapshot removed and rebound', mk(lambda pk: pk['inputs']['reverse'].pop('research/round21/forward/i1/report.md')),
         'coherent evidence tampering: snapshot inventory'),
        ('forward read the reverse packet', mk(lambda pk: pk['inputs']['forward'].__setitem__(
            'research/round33/reverse/bd1/report.md', '0' * 64)), 'coherent evidence tampering: undeclared read'),
        ('snapshot hash edited and rebound', mk(lambda pk: pk['inputs']['forward'].__setitem__(CONTRACT_REL, '1' * 64)),
         'coherent evidence tampering: snapshot hash'),
        ('input edited without rebinding', mk(lambda pk: pk['controls'].__setitem__(ids[0], False), rebind_after=False),
         'coherent evidence tampering: freeze digest'),
        ('SU(4) moment coherently changed in both routes', mk(lambda pk: [pk['cells']['SU(4)']['moments'][r].__setitem__(
            3, F(1, 32)) for r in ('characters', 'weyl_integration')]), 'coherent evidence tampering: moment value'),
    ]
    ctl['exact_arithmetic_admission'] = [
        ('float moment', mk(lambda pk: pk['cells']['U(1)']['moments']['characters'].__setitem__(1, 0.5)),
         'exact arithmetic: float in packet'),
        ('preview read by admission', mk(lambda pk: pk.__setitem__('admission_reads_preview', True)),
         'exact arithmetic: preview read by admission'),
    ]
    ctl['no_priority_or_continuum_claim'] = [
        ('continuum claim', mk(lambda pk: pk['claims'].__setitem__('continuum_claim', True)), 'no priority or continuum claim'),
        ('priority verified', mk(lambda pk: pk['gate_fields'].__setitem__('scientific_priority_verified', True)),
         'no priority or continuum claim'),
        ('historical provenance as premise', mk(lambda pk: pk['provenance_premises'].append('Newton notebook')),
         'no priority or continuum claim'),
    ]
    ctl['changed_model_relabelled'] = [
        ('SU(2) value under the SU(3) label', cellset('SU(3)', ['first_order', 'value'], fo['SU(2)']),
         'su2 constants not transferred'),
        ('one-plaquette value as a box value', cellset('U(1)', ['model'], 'H^G_N'), 'changed model relabelled'),
        ('SO(3) under the spin-1 SU(2) label', cellset('SO(3)', ['wilson_rep'], 'spin-1 of SU(2)'), 'changed model relabelled'),
        ('Z2 under another normalization', cellset('Z2', ['C_F'], F(1, 8)), 'frozen convention used'),
        ('sub-labels changed', mk(lambda pk: pk.__setitem__('sub_labels', ['sign_certified_finite_graph'])),
         'changed model relabelled'),
    ]
    ctl['insufficient_verdict_retained'] = [
        ('accepted with disagreeing routes', mk(lambda pk: pk['cells']['SU(5)']['moments']['weyl_integration'].__setitem__(
            3, F(0))), 'moment tables two routes'),
        ('accepted after retuning', mk(lambda pk: pk.__setitem__('retuned', True)), 'insufficient verdict retained'),
        ('ledger row dropped', mk(lambda pk: pk['ledger'].pop()), 'insufficient verdict retained'),
        ('limited without a reason', mk(lambda pk: pk.update({'verdict': 'limited'})), 'insufficient verdict retained'),
    ]
    pos['insufficient_verdict_retained'] = [
        ('limited with its reason and the limited gate fields accepted',
         mk(lambda pk: pk.update({'verdict': 'limited', 'dominating_reason': 'area parity for the limit not proved',
                                  'gate_fields': dict(pk['gate_fields'], area_parity_limit_claimed=False)})))]
    ctl['placeholder_span_rejected'] = [
        ('placeholder in a statement', addst('The SU(5) coefficient is <value from the reverse route>.'), 'placeholder span'),
        ('placeholder in the sentence', mk(lambda pk: pk.__setitem__('sentence', template + ' <group | list>')),
         'placeholder span'),
    ]
    ctl['negation_aware_phrase_scan'] = [
        ('affirmative forbidden phrase', addst('The group cells describe the thermodynamic limit.'),
         'negation aware phrase scan'),
        ('affirmative uniqueness phrase', addst('Each box has a unique ground state for every group.'),
         'negation aware phrase scan'),
    ]
    pos['negation_aware_phrase_scan'] = [
        ('negated phrase accepted', addst('This is not a statement about the thermodynamic limit.'))]
    ctl['parameters_declare_metric_weights_window'] = [
        ('window removed', mk(lambda pk: pk['parameters'].pop('window')), 'parameters must declare metric weights window'),
        ('weights without reason', mk(lambda pk: pk['parameters'].__setitem__('weights', 'exponential')),
         'parameters must declare metric weights window'),
    ]
    ctl['tier_mixing_rejected'] = [
        ('first-order coefficient without tier', cellset('SU(4)', ['first_order', 'tier'], None), 'tier mixing'),
        ('plan route label as route of computation', cellset('U(1)', ['first_order', 'route_of_computation'], 'polymer_kp'),
         'tier mixing: plan route label'),
        ('hypothesis source attached', cellset('Z2', ['first_order', 'hypothesis_source'], 'bb1_frozen_targets'),
         'tier mixing: hypothesis source'),
        ('tier on a moment', cellset('SU(2)', ['moment_tier'], 'exact_first_order'), 'tier mixing: tier on a moment'),
        ('tier on the SU(5) fourth-order coefficient', cellset('SU(5)', ['higher', 'fourth_order_omega_W', 'tier'],
                                                             'exact_first_order'), 'tier mixing: tier on a higher-order'),
        ('first-order derivative of omega(W^2) without tier', cellset('SU(3)', ['higher', 'first_derivative_omega_W2',
                                                                               'tier'], None),
         'tier mixing: first-order derivative without'),
        ('route label rayleigh_schroedinger on the SO(3) second order', cellset(
            'SO(3)', ['higher', 'second_order_omega_W', 'route_of_computation'], 'rayleigh_schroedinger'),
         'tier mixing: route on a higher-order'),
        ('plan route label on the SU(5) fourth order', cellset(
            'SU(5)', ['higher', 'fourth_order_omega_W', 'route_of_computation'], 'analytic_disc'),
         'tier mixing: plan route label'),
        ('float under a tier', cellset('SU(3)', ['first_order', 'value'], 1 / 1152), 'exact arithmetic: float'),
    ]
    pos['tier_mixing_rejected'] = [('weyl_integration route accepted', cellset('SO(3)', ['first_order', 'route_of_computation'],
                                                                          'weyl_integration')),
                                   ('weyl_integration route on the SU(5) fourth order accepted', cellset(
                                       'SU(5)', ['higher', 'fourth_order_omega_W', 'route_of_computation'],
                                       'weyl_integration'))]
    ctl['frozen_convention_used'] = [
        ('Z2 electric term 1 on the odd state', cellset('Z2', ['first_order', 'value'], z2_alt[
            'electric 1 on the odd link state (face energy 4)']), 'frozen convention used: Z2 normalization'),
        ('Z2 as 1 - sigma^x', cellset('Z2', ['first_order', 'value'], z2_alt['1 - sigma^x (face energy 8)']),
         'frozen convention used: Z2 normalization'),
        ('literal display sign', cellset('SU(4)', ['first_order', 'value'], -fo['SU(4)']),
         'frozen convention used: creation sign'),
        ('SO(3) with C_2=l(l+1)/2', cellset('SO(3)', ['C_F'], F(1)), 'frozen convention used: C_F'),
        ('convention text changed', mk(lambda pk: pk['convention'].__setitem__('face_energy', '4 C_F')),
         'frozen convention used: convention'),
    ]
    ctl['su2_constants_not_transferred'] = [
        ('1/144 under U(1)', cellset('U(1)', ['first_order', 'value'], F(1, 144)), 'su2 constants not transferred'),
        ('dictionary asserted for SU(3)', cellset('SU(3)', ['dictionary'], 'tau=96/g^4'), 'su2 constants not transferred'),
        ('dictionary ledger row for Z2', mk(lambda pk: [r_.__setitem__('status', 'transfer') for r_ in pk['ledger']
                                                        if r_['group'] == 'Z2' and r_['equation'] == 'dictionary']),
         'su2 constants not transferred'),
    ]
    ctl['flip_criterion_central_minus_one'] = [
        ('flip claimed for SU(3)', cellset('SU(3)', ['flip'], 'transfer'), 'flip criterion central minus one'),
        ('SO(3) obstruction from the missing centre alone', cellset('SO(3)', ['flip_counterexample'], None),
         'flip criterion central minus one: obstruction from the missing central element alone'),
        ('central -1 claimed for SU(5)', cellset('SU(5)', ['central_minus_one', 'exists'], True),
         'flip criterion central minus one: centre analysis'),
        ('flip on the one-plaquette model only', cellset('SU(4)', ['flip_models'], ['H_FG(G)']),
         'flip criterion central minus one: models'),
        ('gate scope names SU(5)', mk(lambda pk: pk['gate_fields'].__setitem__(
            'flip_transfer_scope', FLIP_SCOPE.replace('Z2;', 'Z2, SU(5);'))), 'gate scope does not name exactly'),
        ('gate scope literal frozen description', mk(lambda pk: pk['gate_fields'].__setitem__(
            'flip_transfer_scope', pre['gate_fields_required']['flip_transfer_scope'])), 'gate scope does not name exactly'),
    ]
    ctl['parity_criterion_third_moment'] = [
        ('parity claimed for SO(3)', cellset('SO(3)', ['parity'], 'transfer'), 'so3 obstruction mandatory'),
        ('parity obstruction for U(1)', cellset('U(1)', ['parity'], 'obstruction'), 'parity criterion third moment'),
        ('parity without single-occurrence orthogonality', cellset('SU(4)', ['single_occurrence_orthogonality'], False),
         'parity criterion third moment'),
        ('complex level shown for W_g only', cellset('SU(5)', ['whole_level_splitting_zero'], False),
         'parity criterion third moment'),
        ('flip and parity merged', cellset('Z2', ['columns_merged'], True), 'parity criterion third moment'),
    ]
    ctl['moment_tables_two_routes'] = [
        ('single-route cell', mk(lambda pk: pk['cells']['SU(3)']['moments'].pop('weyl_integration')),
         'moment tables two routes: single route'),
        ('routes disagree', mk(lambda pk: pk['cells']['SO(3)']['moments']['weyl_integration'].__setitem__(2, F(0))),
         'moment tables two routes: routes disagree'),
        ('floating moment', mk(lambda pk: pk['cells']['SU(5)']['moments']['characters'].__setitem__(1, 0.02)),
         'exact arithmetic: float'),
    ]
    ctl['su3_obstruction_mandatory'] = [
        ('SU(3) cell omitted', mk(lambda pk: pk['cells'].pop('SU(3)')), 'su3 obstruction mandatory'),
        ('SU(3) called a transfer', mk(lambda pk: pk['cells']['SU(3)'].update({'parity': 'transfer'})),
         'su3 obstruction mandatory'),
        ('SU(3) second-order coefficient zeroed', cellset('SU(3)', ['higher', 'second_order_omega_W', 'value'], F(0)),
         'su3 obstruction mandatory: coefficient value'),
    ]
    ctl['so3_obstruction_mandatory'] = [
        ('SO(3) cell omitted', mk(lambda pk: pk['cells'].pop('SO(3)')), 'so3 obstruction mandatory'),
        ('SO(3) derivative of omega(W^2) zeroed', cellset('SO(3)', ['higher', 'first_derivative_omega_W2', 'value'], F(0)),
         'so3 obstruction mandatory: coefficient value'),
    ]
    ctl['flip_sets_verified'] = [
        ('E_3 count at N=2 changed', mk(lambda pk: pk['flip_sets']['E3_boxes']['2'].__setitem__('met_three_times', 1252)),
         'flip sets verified: enumeration'),
        ('E_2 with two links per plaquette', mk(lambda pk: pk['flip_sets']['E2_boxes']['3'].__setitem__(
            'met_exactly_once', 0)), 'flip sets verified: enumeration'),
        ('coarse factors not checked', mk(lambda pk: pk['flip_sets'].__setitem__('E3_factors', {})),
         'flip sets verified: enumeration'),
        ('odd periodic torus verified', mk(lambda pk: pk['flip_sets'].__setitem__('periodic_odd_side', 'verified')),
         'flip sets verified: periodic'),
    ]
    ctl['area_parity_scope'] = [
        ('periodic odd side claimed', mk(lambda pk: pk['area_parity'].__setitem__('periodic_odd_side', True)),
         'area parity scope: excluded boxes claimed'),
        ('kappa nonzero claimed', mk(lambda pk: pk['area_parity'].__setitem__('kappa', 'any')), 'area parity scope'),
        ('F2 boxes claimed', mk(lambda pk: pk['area_parity'].__setitem__('boxes', ['F1', 'F2'])), 'area parity scope'),
        ('limit through a common subsequence', mk(lambda pk: pk['area_parity'].__setitem__(
            'limit', 'AQ limits along a common subsequence')), 'area parity scope: limit passage'),
        ('Casimir evenness from trace-norm convergence', mk(lambda pk: pk['area_parity'].__setitem__(
            'casimirs', 'trace-norm convergence')), 'area parity scope: surface or Casimir step'),
    ]
    ctl['one_plaquette_model_terms'] = [
        ('free reference from another code path', cellset('SU(2)', ['free_reference_same_code_path'], False),
         'one plaquette model terms'),
        ('transfers_to_aq true', cellset('U(1)', ['transfers_to_aq'], True), 'one plaquette model terms'),
        ('electric term 8 C_2', cellset('SU(5)', ['hamiltonian_terms'], [{'term': 'electric 8 C_2 on chi_r',
                                                                         'coefficient': '8'}] + ONE_PLAQUETTE_TERMS[1:]),
         'one plaquette model terms'),
        ('packet model not a finite graph', mk(lambda pk: pk.__setitem__('model_is_finite_graph', False)),
         'one plaquette model terms'),
    ]
    ctl['no_transfer_called_prediction'] = [
        ('predicts', addst('The character route predicts the SU(4) coefficient.'), 'no transfer called prediction'),
        ('confirms', addst('The Weyl route confirms the SU(3) obstruction.'), 'no transfer called prediction'),
        ('non-transfer without counterexample', mk(lambda pk: [r_.__setitem__('counterexample', None) for r_ in pk['ledger']
                                                               if r_['group'] == 'SO(3)' and r_['status'] == 'obstruction']),
         'no transfer called prediction: non-transfer without counterexample'),
        ('cell labelled a prediction', cellset('SU(2)', ['label'], 'prediction'), 'no transfer called prediction'),
    ]
    ctl['am2_not_reinstantiated'] = [
        ('AM2 chain claimed for U(1)', cellset('U(1)', ['am2_chain'], True), 'am2 not reinstantiated'),
        ('AM2 obligation for Z2 dropped', mk(lambda pk: pk['obligations'].remove(
            'AM2 re-instantiation for Z2 (finite-volume ground state and gap)')), 'am2 not reinstantiated: obligations'),
    ]
    ctl['su5_flip_obstruction_fourth_order'] = [
        ('SU(5) cell omitted', mk(lambda pk: pk['cells'].pop('SU(5)')), 'su5 flip obstruction fourth order'),
        ('fourth-order coefficient zeroed', cellset('SU(5)', ['higher', 'fourth_order_omega_W', 'value'], F(0)),
         'su5 flip obstruction fourth order'),
        ('SU(5) called a flip transfer from its parity', mk(lambda pk: pk['cells']['SU(5)'].update({'flip': 'transfer'})),
         'flip criterion central minus one'),
        ('SU(5) called a parity obstruction', cellset('SU(5)', ['parity'], 'obstruction'),
         'su5 flip obstruction fourth order: SU(5) called a parity obstruction'),
        ('SU(5) obstruction from the missing centre alone', cellset('SU(5)', ['flip_counterexample'], None),
         'su5 flip obstruction fourth order: missing counterexample'),
        ('SU(5) counterexample at second order', cellset('SU(5)', ['flip_counterexample'], {'coefficient': 'second_order_omega_W'}),
         'su5 flip obstruction fourth order'),
        ('route of the fourth-order value missing', cellset('SU(5)', ['higher', 'fourth_order_omega_W', 'route_of_computation'],
                                                           None), 'tier mixing: route on a higher-order'),
    ]
    for cid in ids:
        control(cid, ctl[cid], positives=pos.get(cid, ()))
    need(sorted(ctl) == sorted(ids), 'every_control_executed', controls=len(ids),
         mutations=sum(len(v) for v in ctl.values()))

    readings = [
        'R1: flip and parity separate for SU(5) (parity without flip); SU(4) has both (central -I, Z_4 grading).',
        'R2: every obstruction coefficient has a closed form because W Omega_0 is an exact H_0 eigenvector; SU(5) needs the '
        'fourth order, fixed by the unique Z_5 column path.',
        'R3: criterion B for complex representations: the level at 32 C_F is {chi_f, chi_fbar}; its W-compression is a '
        'combination of cubic moments, each a nonnegative integer, so it vanishes iff E[W^3]=0.',
        'R4: surface independence of A(C) mod 2 needs no homology argument: |C cap E_3| depends on C alone and equals A(S) '
        'mod 2 for every spanning surface S.',
        'R5: E_3 on the coarse factors has two patterns by the parity of b_z; the flip lemma never needs translation '
        'invariance of E_3.',
    ]
    return {
        'loop': 'BD1', 'stage': 'pre_comparison', 'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'skeptic (model agent, correlated ancestry; not human review)',
        'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'model': 'FG one-plaquette models H_FG(G) = 32 C_2 - (tau/3) W for the seven listed groups under the frozen '
                 'convention (model_is_finite_graph true, transfers_to_aq false); group-G box models H^G_N for the flip and '
                 'parity statements (each box inside its Kato radius); SU(2) zero-selected family at kappa=0 for the area '
                 'parity (F1 boxes, every on-site cutoff, the limit of the named constructions through BB2)',
        'group_table': table, 'obstruction_cells': ob, 'su5_fourth_order': q_(closed4),
        'criteria': crit, 'flip_sets': {'E3_boxes': e3_boxes, 'E3_factors': factors, 'E2_boxes': e2_boxes,
                                        'periodic_even_plaquettes': seam},
        'ledger': ledger, 'obligations': obligations,
        'scaling': {k: q_(v) for k, v in scaling.items()},
        'contract_readings': readings,
        'predictions': {'first_order': {k: q_(v) for k, v in fo.items()},
                        'first_order_preview': {k: preview(v) for k, v in fo.items()},
                        'SU(3)': ob['SU(3)'], 'SO(3)': ob['SO(3)'],
                        'SU(5)_fourth_order_omega_W': q_(closed4), 'SU(5)_fourth_order_preview': preview(closed4),
                        'flip_transfer': ['SU(2)', 'SU(4)', 'U(1)', 'Z2'],
                        'parity_transfer': ['SU(2)', 'SU(4)', 'SU(5)', 'U(1)', 'Z2']},
        'gate_fields': pre['gate_fields_required'], 'sentence': template,
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                   'uniqueness_of_ground_state_claimed': False},
        'deferred_parts': {'inventory': 'recorded by find and sha256 (names only)', 'phrase_scan': 'mirror of the round tool',
                           'tampering': 'packet level (synthetic packet built from this derivation)',
                           'box_models': 'criteria A and B on H^G_N are restated in the derivation (Kato per box, single '
                                         'occurrence), not machine-checked beyond the one-plaquette models and the flip sets',
                           'area_parity_limit': 'the passage through BB2 item 1 is restated in the derivation, not '
                                                'machine-checked'},
        'checks': CHECKS,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    result = execute()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + '\n')
    n_controls = sum(1 for row in result['checks'] if row.get('kind') == 'control')
    n_mut = sum(len(row['mutations']) for row in result['checks'] if row.get('kind') == 'control')
    print(json.dumps({'checks': len(result['checks']), 'controls': n_controls, 'mutations': n_mut,
                      'su5_fourth_order': result['su5_fourth_order']}))


if __name__ == '__main__':
    main()
