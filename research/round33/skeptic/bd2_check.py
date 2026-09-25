#!/usr/bin/env python3
"""Round33 BD2 skeptic pre-comparison checker (single+skeptic; new observables and a new dimension in SU(2)).

Written after the BD2 contract froze (sha256 783cad80...46f41e, frozen 2026-09-25T05:09:10Z) from the frozen contract,
advisor/selection-bd2.md, advisor/plan.json (vocabulary recorded below, not read at run time) and the declared premises
(the Round11 README, advisor note and solver README; the AZ2 gate, report and skeptic review; AW1, AV1, AV2, AY1, AY2,
AM2, AQ1 and BB2 gates; the AY1, AY2, AM2, AQ1, AV1, AW1 and BB2 reports; the I1 report; the BA1 and BB2 contracts
for the inherited control semantics), plus the blocking edits and determinations of the pre-freeze review
skeptic/bd-contract-review.json (another skeptic session; its advisor-only previews and previews_recomputed are never
read). Nothing under research/round33/forward/bd2/ was read (only the file names of its inputs/ were listed and hashed;
the recorded inventory is embedded below). The admitted AZ2 checker and the Round11 solver are declared premises that
this program hashes but never opens, imports or executes: the two-plaquette algebra below is written from the Round11
README/advisor equations (Q4, K4, E1-E4) and the AZ2 report. No code of /tmp/claude-0/skeptic-bd-private/ is reused.
Standard library only. Every admission Boolean is decided with fractions.Fraction and directed rational enclosures;
floats appear only in labelled 'previews'. Every check and control raises an explicit exception, so python -O cannot
disable it. Model-agent skeptic with correlated ancestry; not human peer review. Human project author: Hruday N M
(BUNZEEY).

What is derived here:
  * the two-plaquette graph (gauge-invariant sector) in the monic spin-network basis s_abc = x^a y^b z^c + lower
    degree, orthogonal to lower degree: exact Haar moments by two routes (Round11 Q4 and a conditioning on U2 with
    S^3 coordinate moments), the three edge Casimirs from the S^3 Laplace-Beltrami operator (K = 3C_1 + C_vM + 3C_2
    equal to Round11 K4), the basis by triangular back-substitution with a nondegenerate weighted Casimir, the exact
    norms and the four-term multiplication tables of x, y and z;
  * the Rayleigh-Schroedinger tables of <W_1>, <W_2>, <z>, <C_shared> and E_0 in (l1,l2) through total order 4 (and
    beyond, to exhibit where the cutoffs differ) at D=6 and D=8, the one-link flips per coupling, the AZ2 anchors;
  * certified enclosures of <z> at l1=l2 in {+-1/1000, +-1/100, +-1/10} at D=6 and D=8 from a rational Ritz vector,
    with the five-part itemized residual (per-link rows, joint channel, gauge projection, Ritz with Davis-Kahan and a
    tail-comparison angle, directed arithmetic), relative widths against the frozen 1/10^16;
  * the Z^3 1x2 rectangle (six links owned by R, first order 0, |omega| <= K_2' tau^2, evenness from E_3), its formal
    second-order coefficient by two routes; the electric band on R at tau=+-10^-8 (lower (3/2)L^2 from AY2/AY1 with the
    inline Fuchs-van de Graaf step, upper 98|tau| from AQ1 with seven incident anchors), the formal per-link values;
  * the 2+1D AM2 recount (owner sets, stars, faces per site, per-site sum, p=3 numerators, G_3, G_3', termination order
    6 with an exact creation-algebra fixture, the directed coupling cap);
  * a packet validator executing all 21 contract controls as damaging mutations with positive cases.

Usage: python3 -B research/round33/skeptic/bd2_check.py --output /absolute/fresh/dir
"""
import argparse
import copy
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = 'research/round33/contracts/bd2.json'
CONTRACT_SHA256 = '783cad8054a9b7ed3f741e0c06fffd94cfa0d6fda0dcbb7aa0b464058e46f41e'
REVIEW_REL = 'research/round33/skeptic/bd-contract-review.json'
REVIEW_SHA256 = 'b88dc7179cfcd5b90e659f4f06cbad815accbe7441462c1dae87f8a231577a1f'
NOT_OPENED = {  # declared premises hashed only; never opened, imported or executed by this program
    'research/round32/forward/az2/check.py': '4ad3a9f8127ed983a3af9343a4697b77a35bec26f4cd75f1683e32307cab1c7d',
    'research/round11/solver/two_plaquette.py': 'ae9084850538ebf523f8c34564352b48ce0b30d07955991d4b4d1980ab36ce43',
}
GATES = {
    'research/round32/advisor/az2-gate.json': 'd36d53dcad8b1d3e4789d3be76b9e491e73cc5cf2ca88f281f66fd255f98b394',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/av2-gate.json': '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
}
EARLIER_CONTRACTS = {
    'research/round33/contracts/ba1.json': '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9',
    'research/round33/contracts/bb2.json': 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35',
}
R11_README = 'research/round11/solver/README.md'
AZ2_REPORT = 'research/round32/forward/az2/report.md'
AM2_REPORT = 'research/round29/forward/am2/report.md'
AQ1_REPORT = 'research/round29/forward/aq1/report.md'
AY1_REPORT = 'research/round32/forward/ay1/report.md'
I1_REPORT = 'research/round21/forward/i1/report.md'
PLAN_RECORD = {  # recorded from plan.json as committed with the BD freeze (9ae1160); not read at run time
    'sha256_at_bd_freeze_commit': '7d71bfcb2feee038c9ccb9c9fec15bfb5989aba456501a16ec5625e622b775c9',
    'gate_fields': ['area_law_claimed', 'continuum_claim', 'electric_band_claimed', 'electric_band_scope',
                    'graph_sign_certified', 'model_is_finite_graph', 'rate_in_a_claimed', 'scientific_priority_verified',
                    'transfers_to_aq', 'uniqueness_of_ground_state_claimed', 'weak_coupling_claim', 'z3_1x2_formal_only'],
    'plan_route_labels': ['weighted_norm', 'analytic_disc', 'polymer_kp', 'iterated_split', 'duhamel_inner_f1',
                          'duhamel_inner_f2'],
    'lieb_robinson_tiers': ['polynomial_lieb_robinson', 'exponential_lieb_robinson'],
    'forbidden': ['the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
                  'the thermodynamic limit', 'correlation length', 'predicts', 'confirms', 'unique ground state',
                  'a unique limit', 'the unique limit', 'uniqueness of the ground state',
                  'uniquely determines the ground state'],
}
OBSERVED_INPUTS = {  # find + sha256 over research/round33/forward/bd2/inputs (names only), 2026-09-25; 35 files
    'AGENTS.md': '870e1a6b1ff81d6e09888d7084dada2dfdb8128048d97857d9c6b1ffce1b9285',
    'research/round11/README.md': '9ba56b068cbfd3af6654c1997123061ebf20a0f02c25f5cb7205b5146ee7a9be',
    'research/round11/advisor/advisor.md': '5a4853e4bbec267c7320457632c7e9346f85e3e3aa781acefd3291f4a9d1bb32',
    'research/round11/solver/README.md': '9439177f8213c4c2b72ee7ac81236ee4b485d585591fbfde0a8fe1aceb5918c4',
    'research/round11/solver/two_plaquette.py': 'ae9084850538ebf523f8c34564352b48ce0b30d07955991d4b4d1980ab36ce43',
    'research/round21/forward/i1/report.md': '836a4c7d421f0ddf3589c159d2f057839421532c88157a054a61b51c25c781a9',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/forward/am2/report.md': '1b58fb9c1a199f06b156d04c2a9e89f34ba63cf675a5f7c8bfc25bb568e4e019',
    'research/round29/forward/aq1/report.md': 'b091266f5db009fa967a2adea352fa1b190193cc4bcdc6c4c207e5872fc51da3',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/av2-gate.json': '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round32/advisor/az2-gate.json': 'd36d53dcad8b1d3e4789d3be76b9e491e73cc5cf2ca88f281f66fd255f98b394',
    'research/round32/forward/av1/report.md': '7f86e941933913584de2b9e542359e4a3b3c275c1bc8623dca3c367d88437353',
    'research/round32/forward/aw1/report.md': 'ea3a936244a31c7ea4d2c8de65798b2bb0fc65a60437122b71a30465e089d883',
    'research/round32/forward/ay1/report.md': '7cb1e844d75ee1f3d69de2bccb9a684c791e34bf64f3bb9e2d5061221f75dac1',
    'research/round32/forward/ay2/report.md': '527ce2f2700764d76f98efd245fd5f5fa95444f97ca81e323aaff48fac781e6b',
    'research/round32/forward/az2/check.py': '4ad3a9f8127ed983a3af9343a4697b77a35bec26f4cd75f1683e32307cab1c7d',
    'research/round32/forward/az2/report.md': '7521fd9486e081da00302e1ee6778f5f82920c72c80a39ca86c36876d366ac96',
    'research/round32/skeptic/az2.md': '0d0bc350814010560dea9ab8f0c67f04bdd411416c08f9981394df2c601107f3',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
    'research/round33/advisor/selection-bd2.md': 'ec4768c7e8dd7f8245f56232671f0031dc5182fe3b3b06292022476fe4272941',
    'research/round33/contracts/ba1.json': '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9',
    'research/round33/contracts/bb2.json': 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35',
    'research/round33/contracts/bd2.json': '783cad8054a9b7ed3f741e0c06fffd94cfa0d6fda0dcbb7aa0b464058e46f41e',
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

MODEL_ID = 'FG(round11_two_plaquette_independent_couplings)'
GRAPH_TERMS = [{'term': 'K: sum of the seven link Casimirs (rho=1)', 'coefficient': '1'},
               {'term': 'W_1 = (1/2) Tr U_1', 'coefficient': '-l1'}, {'term': 'W_2 = (1/2) Tr U_2', 'coefficient': '-l2'}]
GRID = [F(1, 1000), F(-1, 1000), F(1, 100), F(-1, 100), F(1, 10), F(-1, 10)]
CUTOFFS = (6, 8)
TAU = F(1, 10 ** 8)
ROUND_OUT = 10 ** 50
SUB_LABELS = ['transfer_to_named_model', 'obstruction_recorded', 'sign_certified_finite_graph', 'static_not_dynamic']
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


def sqrt_hi(x, scale=10 ** 70):
    """directed upper bound of sqrt(x) for rational x >= 0 (integer isqrt, rounded up)"""
    x = F(x)
    if x < 0:
        raise CheckFailure('sqrt of a negative number')
    n = isqrt(x.numerator * scale * scale // x.denominator) + 1
    return F(n, scale)


def sqrt_lo(x, scale=10 ** 70):
    x = F(x)
    n = isqrt(x.numerator * scale * scale // x.denominator)
    return F(max(n - 1, 0), scale)


def fact(n):
    return factorial(n)


def exp_bracket(x, n=40):
    """[lo, hi] for e^x, 0 <= x <= 8: Taylor partial sum and the geometric remainder bound."""
    x = F(x)
    if not (0 <= x <= 8):
        raise CheckFailure('exp domain')
    s = sum((x ** k / fact(k) for k in range(n + 1)), F(0))
    return s, s + x ** (n + 1) / fact(n + 1) / (1 - x / (n + 2))


def floor_to(x, den):
    return F((x.numerator * den) // x.denominator, den)


def ceil_to(x, den):
    return F(-((-x.numerator * den) // x.denominator), den)


# ------------------------------------------------------------------------------------------------ moments (two routes)
def catalan(m):
    return comb(2 * m, m) // (m + 1)


def mu_sc(n):
    """semicircle moments E[x^n] of x = Tr(U)/2 under Haar"""
    return F(0) if n % 2 else F(catalan(n // 2), 4 ** (n // 2))


def J_r11(n, h):
    return sum((F((-1) ** r * comb(h, r)) * mu_sc(n + 2 * r) for r in range(h + 1)), F(0))


MOM = {}


def moment(a, b, c):
    """Round11 (Q4): z = xy - sqrt(1-x^2) sqrt(1-y^2) t, t uniform on [-1,1]"""
    key = (a, b, c)
    if key not in MOM:
        MOM[key] = sum((F(comb(c, 2 * h), 2 * h + 1) * J_r11(a + c - 2 * h, h) * J_r11(b + c - 2 * h, h)
                        for h in range(c // 2 + 1)), F(0))
    return MOM[key]


def dfact(n):
    out = 1
    while n > 1:
        out *= n
        n -= 2
    return out


def s3_moment(m, k):
    if m % 2 or k % 2:
        return F(0)
    i, j = m // 2, k // 2
    return F(dfact(2 * i - 1) * dfact(2 * j - 1), 2 ** (i + j) * factorial(i + j + 1))


def moment_own(a, b, c):
    """own route: condition on U2 (y = Re U2); z = <U1, conj U2> = y x + sqrt(1-y^2) u', (x, u') coordinates of S^3"""
    tot = F(0)
    for k in range(0, c + 1, 2):
        ey = sum((F((-1) ** r * comb(k // 2, r)) * mu_sc(b + c - k + 2 * r) for r in range(k // 2 + 1)), F(0))
        tot += comb(c, k) * ey * s3_moment(a + c - k, k)
    return tot


def monos(d):
    return [(a, b, n - a - b) for n in range(d + 1) for a in range(n, -1, -1) for b in range(n - a, -1, -1)]


def deg(m):
    return m[0] + m[1] + m[2]


def spins(m):
    """(edge 1 = the three nonshared links of square 1, shared link vM, edge 2 = nonshared links of square 2)"""
    a, b, c = m
    return F(a + c, 2), F(a + b, 2), F(b + c, 2)


def jj(j):
    return j * (j + 1)


def lam_K(m):
    j1, js, j2 = spins(m)
    return 3 * jj(j1) + jj(js) + 3 * jj(j2)


# ------------------------------------------------------------------------------------------------ edge Casimirs
Q4 = F(1, 4)
EDGE_OPS = {
    # C = -(1/4) Laplace-Beltrami on S^3 in the two loop traces through the edge; the third trace is a parameter
    'e1': [({(0, 0, 0): -Q4, (2, 0, 0): Q4}, (2, 0, 0)), ({(0, 0, 0): -Q4, (0, 0, 2): Q4}, (0, 0, 2)),
           ({(0, 1, 0): -2 * Q4, (1, 0, 1): 2 * Q4}, (1, 0, 1)), ({(1, 0, 0): 3 * Q4}, (1, 0, 0)),
           ({(0, 0, 1): 3 * Q4}, (0, 0, 1))],
    'vM': [({(0, 0, 0): -Q4, (2, 0, 0): Q4}, (2, 0, 0)), ({(0, 0, 0): -Q4, (0, 2, 0): Q4}, (0, 2, 0)),
           ({(0, 0, 1): -2 * Q4, (1, 1, 0): 2 * Q4}, (1, 1, 0)), ({(1, 0, 0): 3 * Q4}, (1, 0, 0)),
           ({(0, 1, 0): 3 * Q4}, (0, 1, 0))],
    'e2': [({(0, 0, 0): -Q4, (0, 2, 0): Q4}, (0, 2, 0)), ({(0, 0, 0): -Q4, (0, 0, 2): Q4}, (0, 0, 2)),
           ({(1, 0, 0): -2 * Q4, (0, 1, 1): 2 * Q4}, (0, 1, 1)), ({(0, 1, 0): 3 * Q4}, (0, 1, 0)),
           ({(0, 0, 1): 3 * Q4}, (0, 0, 1))],
}
K4_R11 = [  # Round11 (K4), written independently of EDGE_OPS
    ({(0, 0, 0): F(-1), (2, 0, 0): F(1)}, (2, 0, 0)), ({(0, 0, 0): F(-1), (0, 2, 0): F(1)}, (0, 2, 0)),
    ({(0, 0, 0): F(-3, 2), (0, 0, 2): F(3, 2)}, (0, 0, 2)), ({(0, 0, 1): F(-1, 2), (1, 1, 0): F(1, 2)}, (1, 1, 0)),
    ({(0, 1, 0): F(-3, 2), (1, 0, 1): F(3, 2)}, (1, 0, 1)), ({(1, 0, 0): F(-3, 2), (0, 1, 1): F(3, 2)}, (0, 1, 1)),
    ({(1, 0, 0): F(3)}, (1, 0, 0)), ({(0, 1, 0): F(3)}, (0, 1, 0)), ({(0, 0, 1): F(9, 2)}, (0, 0, 1))]


def ff(n, k):
    out = 1
    for i in range(k):
        out *= (n - i)
    return out


def apply_op(op, poly):
    out = {}
    for (a, b, c), v in poly.items():
        for coef, (da, db, dc) in op:
            f = ff(a, da) * ff(b, db) * ff(c, dc)
            if f == 0:
                continue
            for (p, r, s), cv in coef.items():
                m = (a - da + p, b - db + r, c - dc + s)
                out[m] = out.get(m, 0) + cv * f * v
    return {k: v for k, v in out.items() if v != 0}


def lin(*pairs):
    out = {}
    for c, p in pairs:
        for k, v in p.items():
            out[k] = out.get(k, 0) + c * v
    return {k: v for k, v in out.items() if v != 0}


def K_mono(poly):
    return lin((3, apply_op(EDGE_OPS['e1'], poly)), (1, apply_op(EDGE_OPS['vM'], poly)), (3, apply_op(EDGE_OPS['e2'], poly)))


def ip_mono(p, q):
    return sum((u * v * moment(a + a2, b + b2, c + c2) for (a, b, c), u in p.items() for (a2, b2, c2), v in q.items()),
               F(0))


def build_basis(dmax):
    """monic s_abc: eigenvector of the nondegenerate weighted Casimir C_e1 + 121 C_vM + 14641 C_e2 with top x^a y^b z^c"""
    wts = {'e1': 1, 'vM': 121, 'e2': 14641}
    op = []
    for e, w in wts.items():
        op += [({k: w * v for k, v in coef.items()}, d) for coef, d in EDGE_OPS[e]]
    kap = lambda m: sum(w * jj(s) for w, s in zip((1, 121, 14641), spins(m)))
    ms = monos(dmax)
    img = {}
    for m in ms:
        im = apply_op(op, {m: F(1)})
        if im.get(m, 0) != kap(m) or any(k != m and deg(k) >= deg(m) for k in im):
            raise CheckFailure('weighted Casimir not triangular with the spin diagonal')
        img[m] = im
    if len({kap(m) for m in ms}) != len(ms):
        raise CheckFailure('weighted Casimir degenerate')
    S = {}
    for m in ms:
        lam = kap(m)
        s, layers = {m: F(1)}, {}
        for k, v in img[m].items():
            if k != m:
                layers.setdefault(deg(k), {})[k] = v
        for d in range(deg(m) - 1, -1, -1):
            for k, r in sorted(layers.pop(d, {}).items()):
                if r == 0:
                    continue
                cc = -r / (kap(k) - lam)
                s[k] = cc
                for k2, v in img[k].items():
                    if k2 != k:
                        lay = layers.setdefault(deg(k2), {})
                        lay[k2] = lay.get(k2, 0) + cc * v
        S[m] = s
    return S


def decompose(poly, S):
    rem, out = dict(poly), {}
    while rem:
        top = max(rem, key=lambda k: (deg(k), k))
        c = rem[top]
        out[top] = c
        for k, v in S[top].items():
            nv = rem.get(k, 0) - c * v
            if nv == 0:
                rem.pop(k, None)
            else:
                rem[k] = nv
    return out


SHIFT = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}


# ------------------------------------------------------------------------------------------------ Z^3 geometry
DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
R_COVER = ((0, 0, 0), (0, 0, 1))


def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def pi_map(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    return ((p, a), (p, c), (add(p, DIRS[a]), c), (add(p, DIRS[c]), a))


def owner_set(p, a, c):
    return frozenset(pi_map(t) for t, _ in face_links(p, a, c))


def is_selected(p, a, c):
    return (a, c) == ('x', 'y') and p[0] % 4 in (0, 1, 2) and p[1] % 2 == 0


def in_E3(link):
    p, d = link
    return {'x': p[1] % 2 == 0, 'y': p[2] % 2 == 0, 'z': p[0] % 2 == 0}[d]


def loop_links(faces):
    cnt = {}
    for f in faces:
        for l in face_links(*f):
            cnt[l] = cnt.get(l, 0) + 1
    return frozenset(l for l, v in cnt.items() if v % 2)


# ------------------------------------------------------------------------------------------------ quaternions (gauge fixture)
def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def qinv(p):
    return (p[0], -p[1], -p[2], -p[3])


def unit_q(a, b, c, d):
    n = a * a + b * b + c * c + d * d
    r = isqrt(n)
    if r * r != n:
        raise CheckFailure('not a Pythagorean quadruple')
    return (F(a, r), F(b, r), F(c, r), F(d, r))


def graph_traces(L):
    """Round11 graph: U = vM h3^-1 vL^-1 h1, V = h2 vR h4^-1 vM^-1; x=Tr U/2, y=Tr V/2, z=Tr UV/2 (real parts)."""
    U = qmul(qmul(qmul(L['vM'], qinv(L['h3'])), qinv(L['vL'])), L['h1'])
    V = qmul(qmul(qmul(L['h2'], L['vR']), qinv(L['h4'])), qinv(L['vM']))
    return U[0], V[0], qmul(U, V)[0]


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
    inv = pk['inputs']
    if sorted(inv) != sorted(c['declared_inputs']):
        extra = sorted(set(inv) - set(c['declared_inputs']))
        if any(p.startswith(pre) for p in extra for pre in ISOLATION_FORBIDDEN_PREFIXES):
            raise Rejected('coherent evidence tampering: undeclared read')
        raise Rejected('coherent evidence tampering: snapshot inventory')
    if any(inv[k] != c['declared_hashes'][k] for k in inv):
        raise Rejected('coherent evidence tampering: snapshot hash')
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
    par = pk['parameters']
    for key in ('metric', 'weights', 'window', 'clock'):
        if key not in par or not par[key]:
            raise Rejected('parameters must declare metric weights window: ' + key)
        if key != 'metric' and not par[key].startswith('not applicable'):
            raise Rejected('parameters must declare metric weights window: ' + key + ' without reason')
    # graph -----------------------------------------------------------------------------------------------------------
    gr = pk['graph']
    if gr['model_id'] != MODEL_ID or gr['couplings'] != ['l1', 'l2'] or gr['independent'] is not True:
        raise Rejected('changed model relabelled: graph coupling label')
    if gr['hamiltonian_terms'] != GRAPH_TERMS or gr['free_reference_same_code_path'] is not True \
            or gr['model_is_finite_graph'] is not True or gr['transfers_to_aq'] is not False:
        raise Rejected('graph couplings named')
    if gr['units'] != 'alpha' or gr['rho'] != 1 or gr['sector'] != 'gauge-invariant':
        raise Rejected('graph couplings named: units, rho or sector')
    tabs = gr['tables']
    if sorted(tabs) != ['6', '8']:
        raise Rejected('exact rs zero truncation: cutoff missing')
    if tabs['6'] != tabs['8']:
        raise Rejected('exact rs zero truncation: coefficient differs between cutoffs')
    if gr['fitted'] is not False or gr['truncation_error'] != '0':
        raise Rejected('exact rs zero truncation: fitted or truncated')
    for obs, ref in c['tables'].items():
        if tabs['8'].get(obs) != ref:
            if obs == 'W_1' and tabs['8'].get(obs) == c['one_face_W1']:
                raise Rejected('changed model relabelled: one-face graph value under the independent-coupling label')
            raise Rejected('exact rs zero truncation: coefficient value (' + obs + ')')
        if any(rec.get('tier') is not None for rec in gr['coefficient_meta'].get(obs, [])):
            raise Rejected('tier mixing: tier on a graph coefficient')
    fl = gr['flips']
    if fl.get('l1') != 'nonshared link of face 1 (h1, vL or h3)' or fl.get('l2') != 'nonshared link of face 2 (h2, vR or h4)':
        raise Rejected('independent coupling flip: flip per coupling')
    if gr['parity_checked_on'] != 'two-variable coefficient table':
        raise Rejected('independent coupling flip: parity checked at l1=l2 only')
    if gr['parities'] != c['parities']:
        raise Rejected('independent coupling flip: parities')
    if gr['second_order_at_equal_couplings'] != c['second_order_diag']:
        raise Rejected('exact rs zero truncation: second-order values')
    # enclosures ------------------------------------------------------------------------------------------------------
    enc = pk['enclosures']
    if sorted(enc) != sorted(c['enclosure_keys']):
        raise Rejected('insufficient verdict retained: enclosure missing')
    for key, row in enc.items():
        led = row.get('residual')
        if not led or sorted(led) != ['a_per_link_rows', 'b_joint_channel', 'c_gauge_projection', 'd_ritz', 'e_arithmetic']:
            raise Rejected('enclosure itemized residual: ' + key)
        if len(led['a_per_link_rows']) != 7 or led['c_gauge_projection'] != '0':
            raise Rejected('enclosure itemized residual: per-link rows or gauge projection ' + key)
        if row.get('tier') is not None:
            raise Rejected('tier mixing: tier on a graph enclosure')
        lo, hi = row['lower'], row['upper']
        mlo, mhi = c['enclosures'][key]
        if hi < mlo or lo > mhi:
            raise Rejected('coherent evidence tampering: enclosure disjoint from the certified one (' + key + ')')
        if not (lo > 0 or hi < 0) or row['sign_certified'] is not True:
            raise Rejected('insufficient verdict retained: enclosure does not exclude 0 (' + key + ')')
        if key.startswith('8,'):
            rel = (hi - lo) / min(abs(lo), abs(hi))
            if row['meets_target'] != (rel <= c['target']):
                raise Rejected('insufficient verdict retained: target flag (' + key + ')')
    if pk['target'] != c['target']:
        raise Rejected('insufficient verdict retained: target retuned')
    # Z^3 1x2 ----------------------------------------------------------------------------------------------------------
    z3 = pk['z3_1x2']
    if z3['rectangle_links_owned_by'] != ['0', 'e_z'] or z3['rectangle'] != c['rectangle']:
        raise Rejected('formal coefficient labelled: rectangle not contained in R')
    if z3['first_order'] != 0:
        raise Rejected('formal coefficient labelled: first order')
    fc = z3['formal']
    if fc['label'] != 'formal_second_order_coefficient' or fc['sign_claimed'] is not False \
            or fc['third_order_remainder'] is not None or fc.get('value_at_cap_claimed') is not False:
        raise Rejected('formal coefficient labelled')
    if fc['value'] != c['formal_1x2'] or fc.get('tier') is not None:
        if fc.get('tier') is not None:
            raise Rejected('tier mixing: tier on the formal coefficient')
        raise Rejected('formal coefficient labelled: value')
    bd = z3['bound']
    if bd['tier'] != 'exact_first_order' or bd['source'] != 'AY1' or bd['constant'] != c['K2p']:
        if bd['tier'] in PLAN_RECORD['plan_route_labels'] or bd['tier'] in PLAN_RECORD['lieb_robinson_tiers']:
            raise Rejected('tier mixing: bound tier')
        raise Rejected('tier mixing: bound tier or source')
    if bd['encloses_formal_coefficient'] is not False or bd['sign'] is not None:
        raise Rejected('formal coefficient labelled: bound presented as an enclosure')
    if sorted(bd['scope']) != ['F1 boxes', 'F2 boxes', 'limit of the named constructions']:
        raise Rejected('changed model relabelled: bound scope')
    ev = z3['evenness']
    if ev['scope'] != ['open centered whole-star boxes (F1)', 'every on-site cutoff',
                       'limit of the named constructions (BB2 at each sign)']:
        if any('F2' in s_ for s_ in ev['scope']):
            raise Rejected('evenness from flip: F2 boxes claimed')
        raise Rejected('evenness from flip: scope')
    if ev['source'] != 'AW1 flip lemma, |C cap E_3|=6 (area 2)' or ev['remainder_bound'] is not None:
        raise Rejected('evenness from flip: source or remainder')
    # band ------------------------------------------------------------------------------------------------------------
    band = pk['band']
    if band['observable'] != 'omega(h_R), h_R = sum of 8 C_e over the 48 links of R':
        raise Rejected('changed model relabelled: band observable')
    if band['passage'] != 'monotone limit over the spectral cutoffs of h_R':
        raise Rejected('unbounded observable handled: passage')
    low = band['lower']
    if low['tier'] != 'first_order_distance_from_product':
        raise Rejected('tier mixing: lower endpoint tier')
    if low['steps'] != ['h_R >= 6 Q_R (I1)', 'Fuchs-van de Graaf, pure reference, proved inline',
                        'lower bound on ||rho_R - P_R||_1']:
        raise Rejected('unbounded observable handled: lower endpoint steps')
    if low['source_limit'] != 'AY2 gate item (2) with BB2 items 2-3' or low['source_boxes'] != 'AY1 forward F11-F14 per box':
        raise Rejected('unbounded observable handled: limit-level distance for a finite box')
    up = band['upper']
    if up['tier'] != 'crude_majorant':
        raise Rejected('tier mixing: upper endpoint tier')
    if up['budget_over_abs_tau'] != 98 or up['source'] != 'AQ1 HNM-AQ1.1, 7 incident anchors':
        raise Rejected('unbounded observable handled: upper budget')
    if up['limit_passage'] != 'lower semicontinuity of the monotone cutoff limit':
        raise Rejected('unbounded observable handled: limit passage')
    if band['bounded_constant_applied_to_h_R'] is not False:
        raise Rejected('unbounded observable handled: bounded constant applied to h_R')
    if sorted(band['signs']) != ['+', '-']:
        raise Rejected('band both signs: sign missing')
    if sorted(band['scope']) != ['F1 boxes', 'F2 boxes', 'limit of the named constructions']:
        raise Rejected('band both signs: scope')
    for sgn in ('+', '-'):
        vals = band['endpoints'][sgn]
        if vals != c['band_endpoints']:
            if vals['upper'] == 112 * TAU:
                raise Rejected('unbounded observable handled: upper budget other than the frozen one')
            raise Rejected('band both signs: endpoints (' + sgn + ')')
    if band['formal_per_link']['label'] != 'formal' or band['formal_per_link']['total'] != c['formal_band']:
        raise Rejected('changed model relabelled: formal band value')
    # 2+1 dimensions ----------------------------------------------------------------------------------------------------
    d3 = pk['dimension_2p1']
    for key, want in c['dim_constants'].items():
        if d3['constants'].get(key) != want:
            raise Rejected('dimension recount: ' + key)
    if d3['label'] != '2+1D declared model (single-site factors on Z^2)' or d3.get('tier') is not None:
        if d3.get('tier') is not None:
            raise Rejected('tier mixing: tier on a 2+1D constant')
        raise Rejected('changed model relabelled: 2+1D label')
    if d3['finite_volume_theorem_claimed'] is not False or d3['dictionary'] != 'own contract (g^2 has mass dimension)':
        raise Rejected('dimension recount: theorem or dictionary')
    # obligations, rates, area law, eqed -----------------------------------------------------------------------------------
    if sorted(pk['obligations']) != sorted(c['obligations']):
        raise Rejected('insufficient verdict retained: obligations')
    if pk['no_transfer'] != c['no_transfer']:
        if 'Einstein-QED' in json.dumps(pk.get('comparisons', [])):
            raise Rejected('no transfer to eqed')
        raise Rejected('no transfer to eqed: row')
    if pk.get('comparisons'):
        raise Rejected('no transfer to eqed: comparison')
    for r in pk['rates']:
        if not r.get('range'):
            raise Rejected('rate range stated')
    for text in pk['statements']:
        if re.search(r'O\(1/N\)', text):
            raise Rejected('rate range stated: O(1/N)')
        if re.search(r'\brates?\b', text) and not re.search(r'\brates? in (N|a)\b', text) and not NEGATION.search(text):
            raise Rejected('rate range stated: unqualified rate')
    # wording ----------------------------------------------------------------------------------------------------------------
    for text in strings([pk['statements'], pk['sentence']]):
        if placeholder_spans(text):
            raise Rejected('placeholder span')
    for text in pk['statements']:
        hits = affirmative_hits(text, c['forbidden'], c['sentence'])
        if hits:
            if any(h in ('string tension', 'confinement') for h in hits):
                raise Rejected('no area law claim: ' + hits[0])
            raise Rejected('negation aware phrase scan: ' + hits[0])
        if re.search(r'\barea law\b', text, re.I) and not NEGATION.search(text):
            raise Rejected('no area law claim: statement')
    if pk['sentence'] != c['sentence'] or pk['sentence_count'] != 1:
        raise Rejected('mandatory sentence template')
    if pk['sub_labels'] != SUB_LABELS:
        raise Rejected('changed model relabelled: sub-labels')
    for name_, ratio in pk['scaling'].items():
        lo_, hi_ = c['brackets'][name_]
        if not (lo_ <= ratio <= hi_):
            raise Rejected('insufficient verdict retained: scaling bracket ' + name_)
    gf = pk['gate_fields']
    if gf.get('area_law_claimed') is not False:
        raise Rejected('no area law claim: gate field')
    met = all(r_['meets_target'] for k_, r_ in enc.items() if k_.startswith('8,'))
    if pk['verdict'] == 'accepted_within_scope' and (not met or pk['retuned'] is not False):
        raise Rejected('insufficient verdict retained: accepted with a missed target or retuning')
    if pk['verdict'] != 'accepted_within_scope' and not pk.get('dominating_reason'):
        raise Rejected('insufficient verdict retained: reason')
    want = c['gate_fields'] if pk['verdict'] == 'accepted_within_scope' else pk['gate_fields']
    for key in sorted(c['gate_fields']):
        if key not in gf:
            raise Rejected('gate field missing: ' + key)
        if key in ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified') and gf[key] is not False:
            raise Rejected('no priority or continuum claim: ' + key)
        if gf[key] != want[key]:
            raise Rejected('gate field: ' + key)
    for name in c['error_terms']:
        entry = pk['error_terms'].get(name)
        if entry is None:
            raise Rejected('error term missing: ' + name)
        if entry.startswith('not_applicable') and len(entry) <= len('not_applicable') + 3:
            raise Rejected('error term missing: not_applicable without a reason (' + name + ')')
    return True


# ------------------------------------------------------------------------------------------------ execute
def execute():
    # 1. provenance ------------------------------------------------------------------------------------------------------
    cb = (ROOT / CONTRACT_REL).read_bytes()
    c_sha = hashlib.sha256(cb).hexdigest()
    need(c_sha == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=c_sha)
    con = json.loads(cb)
    par, pre = con['parameters'], con['preregistration']
    need(con['status'] == 'frozen_before_production' and con['id'] == 'BD2' and con['direction'] == 'single+skeptic'
         and con['producers'] == ['forward'] and pre['model_id'] == MODEL_ID
         and pre['selected_triple_alpha_units'] == ['0', '0', '0'] and pre['target']['value'] == '1/10000000000000000'
         and pre['target']['comparator'] == '<=' and con['selected_after'] == 'research/round33/advisor/bb2-gate.json',
         'contract_frozen_single_direction', frozen_at=con['frozen_at'])
    target = F(pre['target']['value'])
    for rel, want in sorted(GATES.items()):
        if sha(rel) != want:
            raise CheckFailure('gate hash ' + rel)
    for rel, want in sorted(EARLIER_CONTRACTS.items()):
        if sha(rel) != want:
            raise CheckFailure('earlier contract hash ' + rel)
    for rel, want in sorted(NOT_OPENED.items()):
        if sha(rel) != want:
            raise CheckFailure('premise hash ' + rel)
    gates = {rel: json.loads((ROOT / rel).read_text()) for rel in GATES}
    need(all(g['verdict'] == 'accepted_within_scope' for g in gates.values())
         and all(rel in con['shared_premises'] for rel in list(GATES) + list(NOT_OPENED)),
         'premise_gates_pinned_and_accepted', gates=sorted(GATES), hashed_not_opened=sorted(NOT_OPENED))
    declared = sorted(set(['AGENTS.md', CONTRACT_REL] + con['shared_premises']))
    for rel, want in OBSERVED_INPUTS.items():
        if sha(rel) != want:
            raise CheckFailure('inventory hash ' + rel)
    need(sorted(OBSERVED_INPUTS) == declared and len(declared) == 35
         and not any(p.startswith(ISOLATION_FORBIDDEN_PREFIXES) for p in declared), 'producer_inventory_equals_contract',
         files=len(declared))

    # 2. pre-freeze edits ---------------------------------------------------------------------------------------------------
    need(sha(REVIEW_REL) == REVIEW_SHA256, 'bd_contract_review_pinned')
    rev = json.loads((ROOT / REVIEW_REL).read_text())
    applied, superseded = [], []
    for e in rev['blocking_edits'] + rev['non_blocking_edits']:
        if e['contract'] != 'bd2':
            continue
        if e['op'] in ('replace', 'add'):
            ok = has_key_path(con, e['path']) and get_path(con, e['path']) == e['replacement']
        elif e['op'] == 'append':
            ok = e['replacement'] in get_path(con, e['path'])
        else:
            ok = False
        if ok:
            applied.append(e['path'])
        elif e['path'] == '$.preregistration.target.note' and e in rev['non_blocking_edits']:
            note = pre['target']['note']
            if not ('relative width means (upper - lower)/min(|lower|, |upper|)' in note
                    and 'nesting of the D=8 enclosure inside the D=6 one is an observed consistency check' in note
                    and 'blind discriminating threshold at D=8' in note):
                raise CheckFailure('superseded target note lost its definitions')
            superseded.append(e['path'])
        else:
            raise CheckFailure('pre-freeze edit not in the frozen bytes: ' + e['path'])
    need(len(applied) == 28 and superseded == ['$.preregistration.target.note'], 'prefreeze_edits_in_frozen_bytes',
         verbatim=len(applied), superseded=superseded,
         note='19 blocking and 9 non-blocking BD2 edits are verbatim; the non-blocking target-note edit was superseded by '
              'the advisor tightening the target to 1/10^16 (the review offered relabel or tighten); the frozen note keeps '
              'the relative-width definition and the observed-nesting clause')

    # 3. controls, semantics, vocabulary, template --------------------------------------------------------------------------
    ids = con['controls']
    need(ids == pre['controls_required']['ids'] and len(ids) == 21 and len(set(ids)) == 21, 'control_mirror_21')
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
    need(len(own) == 15 and len(inherited) == 6, 'control_semantics_coverage', own=len(own), inherited=inherited)
    need(sorted(pre['gate_fields_required']) == sorted(PLAN_RECORD['gate_fields']) and pre['sub_labels_allowed'] == SUB_LABELS
         and pre['tier_names_allowed'] == ['exact_first_order', 'first_order_distance_from_product', 'crude_majorant'],
         'plan_vocabulary_covers_gate_fields', plan_sha256=PLAN_RECORD['sha256_at_bd_freeze_commit'])
    forbidden = sorted(set(ROUND_FORBIDDEN + pre['forbidden_phrasings'] + PLAN_RECORD['forbidden']))
    template = pre['mandatory_sentence_template']
    need(affirmative_hits(template, forbidden) == [] and placeholder_spans(template) == []
         and 'not a certified sign of the 1x2 mean' in template, 'mandatory_template_scans_clean')
    need(all(par[k].startswith('not applicable') for k in ('weights', 'window', 'clock')) and 'metric' in par,
         'parameters_declare_metric_weights_window_frozen')

    # 4. two-plaquette graph: moments, operators, basis ----------------------------------------------------------------------
    readme = (ROOT / R11_README).read_text()
    need(all(moment(*m) == moment_own(*m) for m in monos(18))
         and 'E[x²]=E[y²]=E[z²]=1/4 and E[xyz]=1/16' in readme
         and moment(2, 0, 0) == moment(0, 2, 0) == moment(0, 0, 2) == F(1, 4) and moment(1, 1, 1) == F(1, 16)
         and moment(2, 2, 0) == F(1, 16), 'haar_moments_two_routes', monomials=len(monos(18)),
         note='Round11 (Q4) and an own conditioning on U2 with S^3 coordinate moments agree on every monomial of degree '
              'at most 18; Round11 fixtures E[x^2]=E[y^2]=E[z^2]=1/4, E[xyz]=E[x^2y^2]=1/16')
    k_ok = all(K_mono({m: F(1)}) == apply_op(K4_R11, {m: F(1)}) for m in monos(10))
    ident = (K_mono({(0, 0, 0): F(1)}) == {} and K_mono({(1, 0, 0): F(1)}) == {(1, 0, 0): F(3)}
             and K_mono({(0, 1, 0): F(1)}) == {(0, 1, 0): F(3)} and K_mono({(0, 0, 1): F(1)}) == {(0, 0, 1): F(9, 2)}
             and K_mono({(1, 1, 0): F(1)}) == {(1, 1, 0): F(13, 2), (0, 0, 1): F(-1, 2)})
    need(k_ok and ident and 'K(xy)=13xy/2−z/2' in readme, 'kinetic_operator_equals_round11_k4',
         note='3 C_e1 + C_vM + 3 C_e2 from the S^3 Laplace-Beltrami operator equals Round11 (K4) on all monomials of degree '
              '<= 10; K1=0, Kx=3x, Ky=3y, Kz=9z/2, K(xy)=13xy/2-z/2')
    small = monos(4)
    sym = all(ip_mono({a: F(1)}, apply_op(EDGE_OPS[e], {b: F(1)})) == ip_mono(apply_op(EDGE_OPS[e], {a: F(1)}), {b: F(1)})
              for e in EDGE_OPS for a in small for b in small)
    need(sym, 'edge_casimirs_symmetric_under_haar', pairs=len(small) ** 2 * 3)
    S = build_basis(9)
    NORM = {m: ip_mono(S[m], {m: F(1)}) for m in S}
    eig = all(apply_op(EDGE_OPS[e], S[m]) == {k: jj(sp) * v for k, v in S[m].items() if jj(sp) != 0}
              for m in S for e, sp in zip(('e1', 'vM', 'e2'), spins(m)))
    orth = all(ip_mono(S[m], {k: F(1)}) == 0 for m in monos(6) for k in monos(deg(m)) if k != m)
    need(eig and orth and all(v > 0 for v in NORM.values()), 'monic_spin_network_basis', size=len(S),
         norms_low={str(m): q_(NORM[m]) for m in monos(2)},
         note='every s_abc (degree <= 9) is a joint eigenvector of the three edge Casimirs with j(j+1) eigenvalues; '
              'orthogonality to every other monomial of degree <= its own verified with exact moments through degree 6; '
              'all norms positive')
    e1_formula = all(lam_K(m) == F(m[0] ** 2 + m[1] ** 2) + F(3, 2) * m[2] ** 2 + F(1, 2) * m[0] * m[1]
                     + F(3, 2) * m[2] * (m[0] + m[1]) + 2 * m[0] + 2 * m[1] + 3 * m[2] for m in monos(12))
    shell_min = {d: min(lam_K(m) for m in monos(d) if deg(m) == d) for d in range(1, 13)}
    need(e1_formula and all(shell_min[d] == F(5 * d * d, 8) + 2 * d + F(3 * (d % 2), 8) for d in shell_min)
         and all(shell_min[d] < shell_min[d + 1] for d in range(1, 12)) and shell_min[1] == 3
         and shell_min[7] == 45 and shell_min[9] == 69, 'spectrum_e1_e3', tail_lower={'6': '45', '8': '69'},
         note='Round11 (E1) and (E3): shell minima 5d^2/8+2d+3(d mod 2)/8, strictly increasing; free gap 3 on span{x,y}')
    TAB = {v: {m: decompose({add(k, SHIFT[v]): c for k, c in S[m].items()}, S) for m in monos(8)} for v in 'xyz'}
    pred = {'x': [(1, 0, 0), (-1, 0, 0), (0, -1, 1), (0, 1, -1)], 'y': [(0, 1, 0), (0, -1, 0), (1, 0, -1), (-1, 0, 1)],
            'z': [(0, 0, 1), (0, 0, -1), (1, -1, 0), (-1, 1, 0)]}
    sel = all(set(tuple(k2[i] - m[i] for i in range(3)) for k2 in TAB[v][m]) <= set(pred[v]) and
              TAB[v][m].get(add(m, SHIFT[v])) == 1 for v in 'xyz' for m in monos(8))
    selfadj = all(TAB[v][m][k2] * NORM[k2] == TAB[v][k2].get(m, F(0)) * NORM[m]
                  for v in 'xyz' for m in monos(8) for k2 in TAB[v][m] if deg(k2) <= 8)
    need(sel and selfadj, 'multiplication_tables_four_terms',
         note='x, y and z act on s_abc by at most four spin-network moves (Clebsch-Gordan on the two edges of the loop), '
              'the raising move with coefficient 1; the tables satisfy the self-adjointness identity c(k->k2)N(k2) = '
              'c(k2->k)N(k) exactly')

    def mul(v, vec, D):
        out = {}
        for k, val in vec.items():
            for k2, c in TAB[v][k].items():
                if deg(k2) <= D:
                    out[k2] = out.get(k2, 0) + c * val
        return {k: w for k, w in out.items() if w != 0}

    def ipv(u, v):
        return sum((c * v[k] * NORM[k] for k, c in u.items() if k in v), F(0))

    # flips on the basis: U_h1 = (-1)^(2 j_edge1) = (-1)^(a+c), U_h2 = (-1)^(b+c), U_vM = (-1)^(a+b)
    flipsign = {'h1': lambda m: (-1) ** (m[0] + m[2]), 'h2': lambda m: (-1) ** (m[1] + m[2]),
                'vM': lambda m: (-1) ** (m[0] + m[1])}
    expect = {'h1': {'x': -1, 'y': 1, 'z': -1}, 'h2': {'x': 1, 'y': -1, 'z': -1}, 'vM': {'x': -1, 'y': -1, 'z': 1}}
    fl_ok = all(flipsign[f](m) * flipsign[f](k2) == expect[f][v] for f in flipsign for v in 'xyz' for m in monos(8)
                for k2 in TAB[v][m])
    # rational-quaternion gauge fixture
    base = {'h1': unit_q(1, 2, 2, 4), 'h2': unit_q(2, 1, 4, 2), 'h3': unit_q(4, 2, 1, 2), 'h4': unit_q(1, 4, 2, 2),
            'vL': unit_q(2, 3, 6, 0), 'vM': unit_q(6, 2, 3, 0), 'vR': unit_q(3, 0, 2, 6)}
    ends = {'h1': ('TL', 'TM'), 'h2': ('TM', 'TR'), 'h3': ('BL', 'BM'), 'h4': ('BM', 'BR'), 'vL': ('TL', 'BL'),
            'vM': ('TM', 'BM'), 'vR': ('TR', 'BR')}
    tr0 = graph_traces(base)
    gauge_ok = True
    for seed in range(4):
        g = {v: unit_q(*q) for v, q in zip(('TL', 'TM', 'TR', 'BL', 'BM', 'BR'),
                                           [(1, 2, 2, 4), (2, 3, 6, 0), (0, 2, 3, 6), (4, 2, 1, 2), (6, 0, 2, 3),
                                            (2, 4, 1, 2)][seed:] + [(1, 2, 2, 4), (2, 3, 6, 0), (0, 2, 3, 6),
                                                                     (4, 2, 1, 2)][:seed])}
        gl = {e: qmul(qmul(g[ends[e][0]], base[e]), qinv(g[ends[e][1]])) for e in base}
        gauge_ok = gauge_ok and graph_traces(gl) == tr0
    minus = (F(-1), F(0), F(0), F(0))
    flipped = {f: graph_traces(dict(base, **{f: qmul(minus, base[f])})) for f in ('h1', 'h2', 'vM')}
    need(fl_ok and gauge_ok and flipped['h1'] == (-tr0[0], tr0[1], -tr0[2]) and flipped['h2'] == (tr0[0], -tr0[1], -tr0[2])
         and flipped['vM'] == (-tr0[0], -tr0[1], tr0[2]), 'one_link_flips_and_gauge_fixture', traces=[q_(v) for v in tr0],
         note='the h1 flip reverses W_1 and z and fixes W_2; the h2 flip reverses W_2 and z and fixes W_1; the vM flip '
              'reverses both faces; operator level on the basis and on exact rational quaternions; (x,y,z) are invariant '
              'under four sets of six rational vertex gauge transformations (gauge projection exactly 0)')

    # 5. RS tables in (l1, l2) -------------------------------------------------------------------------------------------------
    Z0 = (0, 0, 0)
    CSH = {m: jj(spins(m)[1]) for m in S}

    def rs2(D, order):
        psi, E = {(0, 0): {Z0: F(1)}}, {(0, 0): F(0)}
        for n in range(1, order + 1):
            for i in range(n, -1, -1):
                j = n - i
                rhs = {}
                if i:
                    for k, v in mul('x', psi[(i - 1, j)], D).items():
                        rhs[k] = rhs.get(k, 0) + v
                if j:
                    for k, v in mul('y', psi[(i, j - 1)], D).items():
                        rhs[k] = rhs.get(k, 0) + v
                E[(i, j)] = -rhs.get(Z0, F(0))
                for p_ in range(i + 1):
                    for q in range(j + 1):
                        if (p_, q) not in ((0, 0), (i, j)):
                            for k, v in psi[(i - p_, j - q)].items():
                                rhs[k] = rhs.get(k, 0) + E[(p_, q)] * v
                psi[(i, j)] = {k: v / lam_K(k) for k, v in rhs.items() if k != Z0 and v != 0}
        return psi, E

    def series2(psi, op, order):
        num, den = {}, {}
        for a in psi:
            for b in psi:
                t = (a[0] + b[0], a[1] + b[1])
                if t[0] + t[1] <= order:
                    num[t] = num.get(t, 0) + ipv(psi[a], op(psi[b]))
                    den[t] = den.get(t, 0) + ipv(psi[a], psi[b])
        out = {}
        for n in range(order + 1):
            for i in range(n, -1, -1):
                t = (i, n - i)
                val = num.get(t, F(0))
                for u, cu in out.items():
                    r = (t[0] - u[0], t[1] - u[1])
                    if r[0] >= 0 and r[1] >= 0 and r != (0, 0):
                        val -= cu * den.get(r, F(0))
                out[t] = val / den[(0, 0)]
        return out

    tables, full = {}, {}
    for D in CUTOFFS:
        psi, E = rs2(D, 9)
        obs = {'W_1': lambda v, D=D: mul('x', v, D), 'W_2': lambda v, D=D: mul('y', v, D),
               'z': lambda v, D=D: mul('z', v, D),
               'C_shared': lambda v: {k: c * CSH[k] for k, c in v.items() if CSH[k] != 0}}
        ser = {name: series2(psi, op, 9) for name, op in obs.items()}
        ser['E_0'] = {k: v for k, v in E.items()}
        full[D] = ser
        tables[str(D)] = {name: {'%d,%d' % k: q_(v) for k, v in sorted(s_.items()) if sum(k) <= 4 and v != 0}
                          for name, s_ in ser.items()}
        tables[str(D)]['psi'] = psi if D == 8 else None
    psi8 = tables['8'].pop('psi')
    tables['6'].pop('psi')
    same9 = all(full[6][name] == full[8][name] for name in full[6])

    def rs_diag(D, order):  # l1 = l2 = l, H = K - l(x + y); omega(z) coefficients
        psi, E = [{Z0: F(1)}], [F(0)]
        for n in range(1, order + 1):
            rhs = {}
            for v in 'xy':
                for k, w in mul(v, psi[n - 1], D).items():
                    rhs[k] = rhs.get(k, 0) + w
            E.append(-rhs.get(Z0, F(0)))
            for kk in range(1, n):
                for k, w in psi[n - kk].items():
                    rhs[k] = rhs.get(k, 0) + E[kk] * w
            psi.append({k: w / lam_K(k) for k, w in rhs.items() if k != Z0 and w != 0})
        num = [sum((ipv(psi[i], mul('z', psi[m - i], D)) for i in range(m + 1)), F(0)) for m in range(order + 1)]
        den = [sum((ipv(psi[i], psi[m - i]) for i in range(m + 1)), F(0)) for m in range(order + 1)]
        out = []
        for m in range(order + 1):
            out.append((num[m] - sum((out[k] * den[m - k] for k in range(m)), F(0))) / den[0])
        return out
    z6, z8 = rs_diag(6, 16), rs_diag(8, 16)
    first_diff = min(n for n in range(17) if z6[n] != z8[n])
    need(tables['6'] == tables['8'] and same9 and first_diff > 9, 'rs_tables_zero_truncation',
         first_order_where_cutoffs_differ_z_diag=first_diff,
         note='every coefficient through total order 9 is identical at D=6 and D=8 (psi_ij lies in P_{i+j} and K is '
              'diagonal in the orthogonal basis, so truncation first enters psi at order D+1 and the expectations much '
              'later); along l1=l2 the <z> series first differs at order %d, so the comparison discriminates' % first_diff)
    T8 = tables['8']
    want_tab = {'W_1': {'1,0': '1/6', '3,0': '-5/864', '1,2': '1/4212'},
                'z': {'1,1': '7/216', '3,1': '-349/303264', '1,3': '-349/303264'},
                'C_shared': {'2,0': '1/48', '0,2': '1/48', '4,0': '-5/4608', '2,2': '-49/438048', '0,4': '-5/4608'},
                'E_0': {'2,0': '-1/12', '0,2': '-1/12', '4,0': '5/3456', '2,2': '-1/8424', '0,4': '5/3456'}}
    need(all(T8[k] == v for k, v in want_tab.items()) and T8['W_2'] == {'0,1': '1/6', '0,3': '-5/864', '2,1': '1/4212'},
         'rs_two_variable_tables', tables={k: T8[k] for k in ('W_1', 'W_2', 'z', 'C_shared', 'E_0')})

    def parity_ok(tab, p1, p2):
        return all((int(k.split(',')[0]) % 2 == p1) and (int(k.split(',')[1]) % 2 == p2) for k in tab)
    parities = {'W_1': 'odd in l1, even in l2', 'z': 'odd in l1, odd in l2', 'C_shared': 'even in l1, even in l2',
                'W_2': 'even in l1, odd in l2'}
    nz9 = {name: {'%d,%d' % k: 1 for k, v in full[8][name].items() if v != 0} for name in ('W_1', 'W_2', 'z', 'C_shared')}
    need(parity_ok(T8['W_1'], 1, 0) and parity_ok(T8['z'], 1, 1) and parity_ok(T8['C_shared'], 0, 0)
         and parity_ok(T8['W_2'], 0, 1) and parity_ok(nz9['W_1'], 1, 0) and parity_ok(nz9['W_2'], 0, 1)
         and parity_ok(nz9['z'], 1, 1) and parity_ok(nz9['C_shared'], 0, 0), 'parities_on_two_variable_table',
         parities=parities, note='checked on the coefficient table through order 9 (not only at l1=l2); every even-order '
                                 'coefficient of <W_1> at l1=l2 vanishes')

    def diag(ser, n):
        return sum((v for k, v in ser.items() if sum(k) == n), F(0))
    az2 = gates['research/round32/advisor/az2-gate.json']['accepted'] + gates['research/round32/advisor/az2-gate.json']['decision']
    az2rep = (ROOT / AZ2_REPORT).read_text()
    dW = [diag(full[8]['W_1'], n) for n in range(6)]
    dE = [diag(full[8]['E_0'], n) for n in range(6)]
    dz = [diag(full[8]['z'], n) for n in range(5)]
    dC = [diag(full[8]['C_shared'], n) for n in range(5)]
    psi2 = {}
    for key in ((2, 0), (1, 1), (0, 2)):
        for k, v in psi8[key].items():
            for m, c in S[k].items():
                psi2[m] = psi2.get(m, 0) + v * c
    psi2 = {k: v for k, v in psi2.items() if v != 0}
    need(dW == [0, F(1, 6), 0, F(-187, 33696), 0, F(767713, 2523156480)] and dE == [0, 0, F(-1, 6), 0, F(187, 67392), 0]
         and dz == [0, 0, F(7, 216), 0, F(-349, 151632)]
         and 'tau_FG/6 - (187/33696) tau_FG^3 + (767713/2523156480) tau_FG^5' in az2
         and '-tau_FG^2/6 + (187/67392) tau_FG^4' in az2 and '7/576, 79/2808, 7/216' in az2 and 'tau^3/4212' in az2
         and 'a_3 = -5/864' in az2 and psi2 == {(2, 0, 0): F(1, 24), (1, 1, 0): F(4, 39), (0, 2, 0): F(1, 24),
                                                (0, 0, 1): F(4, 351), (0, 0, 0): F(-1, 48)}
         and 'psi_2 = x^2/24 + 4xy/39 + y^2/24 + 4z/351 - 1/48' in az2rep and '-349/151632' in az2rep,
         'az2_anchors_reproduced', second_order_z_diag=q_(dz[2]), second_order_Cshared_diag=q_(dC[2]),
         note='at l1=l2 the AZ2 series of <W_1>, E_0 and <z> and the AZ2 psi_2 are reproduced exactly; the one-face value '
              '-5/864 is the l1^3 coefficient and the second-square shift 1/4212 the l1 l2^2 coefficient')
    ww = series2(psi8, lambda v: mul('x', mul('x', v, 9), 9), 4)
    wwy = series2(psi8, lambda v: mul('x', mul('y', v, 9), 9), 4)
    need(diag(ww, 2) == F(7, 576) and diag(ww, 4) == F(-787717, 1261578240) and diag(wwy, 2) == F(79, 2808)
         and diag(wwy, 4) == F(-20159, 10513152) and '-787717/1261578240' in az2rep and '-20159/10513152' in az2rep
         and dC[2] == F(1, 24), 'az2_second_moments_reproduced',
         note='<W_1^2> and <W_1 W_2> through order 4 at l1=l2 equal the AZ2 report; <C_shared> second order 1/24 at l1=l2')

    # 6. certified enclosures of <z> at l1=l2 -----------------------------------------------------------------------------------
    def ritz(l, D):
        phi = {Z0: F(1)}
        scale = 10 ** 130
        for it in range(600):
            vphi = {}
            for v in 'xy':
                for k, w in mul(v, phi, D).items():
                    vphi[k] = vphi.get(k, 0) - l * w
            mu = vphi.get(Z0, F(0))
            new = {Z0: F(1)}
            for k in sorted(set(phi) | set(vphi)):
                if k != Z0:
                    val = (mu * phi.get(k, F(0)) - vphi.get(k, F(0))) / lam_K(k)
                    val = F(round(val * scale), scale)
                    if val:
                        new[k] = val
            diff = max(abs(new.get(k, 0) - phi.get(k, 0)) for k in set(new) | set(phi))
            phi = new
            if diff < F(1, 10 ** 120):
                return phi, it
        raise CheckFailure('Ritz iteration did not converge')

    tail_lower_gate = {int(d): F(v_) for v_, d in re.findall(r'tail_lower is (\d+) \(D=(\d+)\)', az2)}
    tail_lower_gate.update({int(d): F(v_) for v_, d in re.findall(r'and (\d+) \(D=(\d+)\)', az2)})
    need(tail_lower_gate == {6: 45, 8: 69} == {D: shell_min[D + 1] for D in CUTOFFS}, 'tail_lower_pinned_to_az2_gate')

    def certify(l, D):
        phi, it = ritz(l, D)
        n2 = ipv(phi, phi)
        hphi = {k: lam_K(k) * v for k, v in phi.items() if lam_K(k)}
        xp, yp = mul('x', phi, D + 1), mul('y', phi, D + 1)
        for k, w in list(xp.items()) + list(yp.items()):
            hphi[k] = hphi.get(k, 0) - l * w
        mu = ipv(phi, hphi) / n2
        r = {k: hphi.get(k, 0) - mu * phi.get(k, 0) for k in set(hphi) | set(phi)}
        rP = {k: v for k, v in r.items() if deg(k) <= D and v != 0}
        rQ = {k: v for k, v in r.items() if deg(k) > D and v != 0}
        eP2, eQ2 = ipv(rP, rP) / n2, ipv(rQ, rQ) / n2
        xq = {k: -l * v for k, v in xp.items() if deg(k) > D}
        yq = {k: -l * v for k, v in yp.items() if deg(k) > D}
        chan = {'x_face': ipv(xq, xq) / n2, 'y_face': ipv(yq, yq) / n2, 'interference_2XY': 2 * ipv(xq, yq) / n2}
        if chan['x_face'] + chan['y_face'] + chan['interference_2XY'] != eQ2:
            raise CheckFailure('joint channel decomposition')
        v = abs(l) + abs(l)  # ||l1 x + l2 y|| <= |l1| + |l2| at l1 = l2 = l
        lamD = shell_min[D + 1]
        if lamD != tail_lower_gate[D]:
            raise CheckFailure('tail threshold differs from the AZ2 gate tail_lower')
        g1 = shell_min[1] - v - mu  # Weyl: E_1(H) >= E_1(K) - v, and Cauchy interlacing for the Ritz values
        gQ = lamD - v - mu
        if not (g1 > 0 and gQ > v * v / g1):
            raise CheckFailure('separations')
        eP, eQ = sqrt_hi(eP2), sqrt_hi(eQ2)
        sP = eP / g1
        eQphi = eQ + v * sqrt_hi(2) * sP
        b_ = eQphi / (gQ - v * v / g1)
        s_tail = b_ * sqrt_hi(1 + v * v / (g1 * g1))
        s = sP + s_tail
        sA = sqrt_hi(eP2 + eQ2) / g1  # Davis-Kahan with the full residual (labelled comparison)
        q = ipv(phi, mul('z', phi, D + 1)) / n2
        hw = 2 * s
        lo, hi = floor_to(q - hw, ROUND_OUT), ceil_to(q + hw, ROUND_OUT)
        # per-link rows on the first omitted shell (sector weights of r)
        shell = [m for m in monos(D + 1) if deg(m) == D + 1]
        wt = {m: rQ.get(m, F(0)) ** 2 * NORM[m] / n2 for m in shell}
        classes = {'e1': lambda m: m[0] + m[2] > D, 'vM': lambda m: m[0] + m[1] > D, 'e2': lambda m: m[1] + m[2] > D}
        thr = {e: min(lam_K(m) for m in shell if f(m)) for e, f in classes.items()}
        cls_w = {e: sum((wt[m] for m in shell if f(m)), F(0)) for e, f in classes.items()}
        prod_w = sum((wt[m] for m in shell if min(m) >= 1), F(0))
        corners = {'e1&e2': wt[(0, 0, D + 1)], 'e1&vM': wt[(D + 1, 0, 0)], 'e2&vM': wt[(0, D + 1, 0)]}
        if sum(cls_w.values()) - sum(corners.values()) + prod_w != eQ2:
            raise CheckFailure('per-link classes plus product channel minus corners')
        link_rows = []
        for link, e in (('h1', 'e1'), ('vL', 'e1'), ('h3', 'e1'), ('vM', 'vM'), ('h2', 'e2'), ('vR', 'e2'), ('h4', 'e2')):
            link_rows.append({'link': link, 'retained_max_spin': q_(F(D, 2)), 'threshold': q_(thr[e]),
                              'residual_weight_preview': preview(cls_w[e]), 'leakage_from_kinetic': '0'})
        ledger = {'a_per_link_rows': link_rows,
                  'b_joint_channel': {'rho_Q2_preview': preview(eQ2), 'product_channel_preview': preview(prod_w),
                                      'product_threshold': q_(min(lam_K(m) for m in shell if min(m) >= 1)),
                                      'x_face_preview': preview(chan['x_face']), 'y_face_preview': preview(chan['y_face']),
                                      'interference_2XY_preview': preview(chan['interference_2XY']),
                                      'corners_preview': {k: preview(v_) for k, v_ in corners.items()}},
                  'c_gauge_projection': '0',
                  'd_ritz': {'rho_P2_preview': preview(eP2), 'mu_preview': preview(mu), 'g1_weyl_preview': preview(g1),
                             'gQ_tail_preview': preview(gQ), 'tail_lower': q_(lamD), 's_P_preview': preview(sP),
                             's_tail_preview': preview(s_tail), 'sin_theta_preview': preview(s),
                             'davis_kahan_full_residual_preview': preview(sA)},
                  'e_arithmetic': {'sqrt': 'integer isqrt rounded upward at 10^-70',
                                   'endpoints': 'rounded outward to denominators 10^50', 'ritz_proposal_rounding': '10^-130'}}
        return {'q': q, 'hw': hw, 'lower': lo, 'upper': hi, 'iterations': it, 'ledger': ledger, 'sA': sA,
                's': s, 'eQ2': eQ2, 'eP2': eP2, 'mu': mu}

    certs = {}
    for D in CUTOFFS:
        for l in GRID:
            certs['%d,%s' % (D, l)] = certify(l, D)
    rel = {}
    for key, cc in certs.items():
        rel[key] = (cc['upper'] - cc['lower']) / min(abs(cc['lower']), abs(cc['upper']))
    nested = all(certs['6,%s' % l]['lower'] <= certs['8,%s' % l]['lower'] and certs['8,%s' % l]['upper']
                 <= certs['6,%s' % l]['upper'] for l in GRID)
    mirror = all(certs['%d,%s' % (D, l)]['lower'] == certs['%d,%s' % (D, -l)]['lower'] and certs['%d,%s' % (D, l)]['upper']
                 == certs['%d,%s' % (D, -l)]['upper'] for D in CUTOFFS for l in GRID)
    need(all(cc['lower'] > 0 for cc in certs.values()) and nested and mirror
         and all(rel['8,%s' % l] <= target for l in GRID), 'certified_z_enclosures',
         enclosures={k: [q_(cc['lower']), q_(cc['upper'])] for k, cc in sorted(certs.items())},
         relative_width_preview={k: preview(v) for k, v in sorted(rel.items())},
         max_relative_width_D8_preview=preview(max(rel['8,%s' % l] for l in GRID)), target=q_(target),
         margin_D8_preview=preview(target / max(rel['8,%s' % l] for l in GRID)),
         note='every enclosure is positive (sign certified at every grid point; <z> is even in l at l1=l2); D=8 inside '
              'D=6 at every point (observed); the -l certificate equals the +l one exactly')
    comp = {k: {'hw_preview': preview(cc['hw']), 'davis_kahan_full_residual_hw_preview': preview(2 * cc['sA']),
                'rel_width_if_davis_kahan_preview': preview(4 * cc['sA'] / cc['q'])}
            for k, cc in sorted(certs.items())}
    dk_rel = max(4 * certs['8,%s' % l]['sA'] / certs['8,%s' % l]['q'] for l in GRID)
    need(target * F(80, 100) <= dk_rel <= target * F(95, 100)
         and all(certs['8,%s' % l]['s'] * 20 < certs['8,%s' % l]['sA'] for l in GRID),
         'angle_bound_comparison', comparison=comp, davis_kahan_only_max_rel_D8_preview=preview(dk_rel),
         note='labelled: the tail-comparison angle is more than 20 times smaller than the Davis-Kahan angle with the full '
              'residual (Weyl separation 3-2|l| only); with Davis-Kahan alone the D=8 relative width at l=+-1/10 would be '
              'between 0.80 and 0.95 of the frozen 1/10^16, so the target is discriminating')

    # 7. Z^3: the 1x2 rectangle, band, formal values ------------------------------------------------------------------------------
    f1, f2 = ((0, 0, 0), 'x', 'z'), ((1, 0, 0), 'x', 'z')
    rect = loop_links([f1, f2])
    rect_owners = sorted(set(pi_map(p) for p, _ in rect))
    anchors = sorted(b for b in product(range(-2, 3), repeat=3) if any(add(b, s_) in R_COVER for s_ in S_STAR))
    faces_R = []
    for b in anchors:
        for r_, s_, a, c in product(range(4), range(2), 'xyz', 'xyz'):
            if (a, c) not in ORIENT:
                continue
            p = (4 * b[0] + r_, 2 * b[1] + s_, b[2])
            if not is_selected(p, a, c) and owner_set(p, a, c) & set(R_COVER):
                faces_R.append((p, a, c))
    inside = [f for f in faces_R if owner_set(*f) == frozenset(R_COVER)]
    need(len(rect) == 6 and rect_owners == list(R_COVER) and not is_selected(*f1) and not is_selected(*f2)
         and f1 in inside and f2 in inside and len(anchors) == 7 and len(faces_R) == 82 and len(inside) == 10
         and all(frozenset(face_links(*f)) != rect for f in faces_R)
         and sum(1 for l in rect if in_E3(l)) == 6 and sum(1 for l in face_links(*f1) if in_E3(l)) == 3,
         'z3_rectangle_geometry', rectangle=sorted([list(p) + [d] for p, d in rect]),
         note='the rectangle W + (xz face at e_x) has six links owned by R={0,e_z}; both faces are omitted, anchored at 0, '
              'among the 10 faces with owner set exactly R; 7 incident anchors, 82 omitted faces meet R; no face has the '
              'rectangle as its link set, so E[W_1x2 W_f]=0 and the first-order coefficient is 0; |C cap E_3|=6 (area 2, '
              'even), the W face meets E_3 three times')
    e_xyz = moment(1, 1, 1)
    formal_a = 7 * e_xyz / 7776  # 2<W12 Om, psi_2> + <psi_1, W12 psi_1>, energies 24 and 36 (delta units)
    formal_b = full[8]['z'][(1, 1)] / 24 ** 2  # graph <z> coefficient under tau_FG = tau/24
    need(formal_a == formal_b == F(7, 124416), 'z3_formal_second_order_two_routes', value=q_(formal_a),
         preview=preview(formal_a), label='formal_second_order_coefficient',
         note='route 1: Z^3 Rayleigh-Schroedinger with the two omitted faces at -(tau/3)W_f, R W_1x2 Omega = W_1x2 Omega/36, '
              'E[W_f1 W_f2 W_1x2]=1/16; route 2: the graph coefficient 7/216 of l1 l2 under tau_FG=tau/24; no sign, no '
              'third-order remainder')
    ay1 = gates['research/round32/advisor/ay1-gate.json']['accepted']
    k2p = F(re.search(r"K_2'=(\d+/\d+)", ay1).group(1))
    a_ = TAU / 144
    Jt = 28 * TAU
    T_ = 49 * a_ / (1 - 352 * Jt)
    rho_ = 352 * Jt * T_
    epsR = 82 * a_ + 2 * rho_ + (33 * a_ + rho_) ** 2
    k2p_re = (4 * rho_ + 2 * T_ * (72 * a_ + 2 * rho_) + 2 * (33 * a_ + rho_) ** 2 + 2 * epsR ** 2 + 20 * a_ * epsR ** 2) / TAU ** 2
    bound_1x2 = k2p * TAU ** 2
    need(k2p_re == k2p and 'reset omega(h_R)<=98|tau|' in ay1 and '7 incident anchors' in ay1, 'ay1_constants_pinned',
         K2_prime=q_(k2p), bound_1x2_at_cap=q_(bound_1x2), bound_preview=preview(bound_1x2),
         note='K_2\' recomputed from the AY1 items equals the gate rational; |omega(W_1x2)| <= K_2\' tau^2 for every F1 and F2 '
              'box and the limit (tier exact_first_order), with Tr(P_R W_1x2)=Tr(rho^(1)_R W_1x2)=0')
    ay2 = gates['research/round32/advisor/ay2-gate.json']['accepted']
    m10 = re.search(r'sqrt\(10\) in \[(\d+/\d+), (\d+/\d+)\]', ay2)
    s10 = (F(m10.group(1)), F(m10.group(2)))
    L_ay2 = F(re.search(r'certified at \|tau\|=10\^-8 with the directed bracket sqrt\(10\) in \[[^\]]*\] as (\d+/\d+)', ay2).group(1))
    L_own = s10[0] * TAU / 72 - k2p * TAU ** 2
    need(s10[0] ** 2 < 10 < s10[1] ** 2 and L_own == L_ay2, 'ay2_distance_lower_end',
         L=q_(L_ay2), L_preview=preview(L_ay2),
         note='L = sqrt10_lo |tau|/72 - K_2\' tau^2 equals the AY2 gate lower end exactly; the same rational bounds the '
              'per-box distance through AY1 forward F11-F14 (uniform in N, cutoff, both families; AV1 F22)')

    def band(t):
        L = s10[0] * abs(t) / 72 - k2p * t ** 2
        return F(3, 2) * L * L, 98 * abs(t)
    lowp, upp = band(TAU)
    lowm, upm = band(-TAU)
    i1 = (ROOT / I1_REPORT).read_text()
    aq1 = (ROOT / AQ1_REPORT).read_text()
    need(lowp == lowm == F(3, 2) * L_ay2 ** 2 and upp == upm == 2 * len(anchors) * 7 * TAU and 'gap `3alpha/4=6delta`' in i1 and '8M|F|=56|\\tau||F|' in aq1
         and 8 * F(3, 4) == 6 and 2 * len(anchors) * 7 == 98 and 56 * 2 == 112 and lowp > 0,
         'electric_band_endpoints', lower=q_(lowp), upper=q_(upp), lower_preview=preview(lowp), upper_preview=preview(upp),
         note='omega(h_R) >= 6 Tr(Q_R rho_R) >= 6((1/2)||rho_R - P_R||_1)^2 >= (3/2)L^2 (tier first_order_distance_from_'
              'product) and omega(h_R) <= 2*7*(7|tau|) = 98|tau| (tier crude_majorant, AQ1 HNM-AQ1.1 with the 7 incident '
              'anchors; the generic 56|tau||R| = 112|tau| is valid but not frozen); identical at both signs; the upper end '
              'passes to the limit by lower semicontinuity of the monotone cutoff limit')
    # Fuchs-van de Graaf (pure reference) on exact qubit fixtures: -det(rho - P) <= Tr(Q rho)
    fvdg = []
    for p_, c2 in ((F(9, 10), F(9, 100)), (F(3, 4), F(1, 10)), (F(1, 2), F(1, 4)), (F(99, 100), F(0))):
        if c2 > p_ * (1 - p_):
            raise CheckFailure('fixture not a state')
        fvdg.append((1 - p_) ** 2 + c2 <= 1 - p_)
    need(all(fvdg), 'fuchs_van_de_graaf_pure_reference_fixtures', cases=len(fvdg),
         note='(1/2)||rho-P||_1 = sqrt(-det(rho-P)) for qubit rho, and -det = (1-p)^2+|c|^2 <= 1-p = Tr(Q rho) iff '
              '|c|^2 <= p(1-p) (positivity); equality for pure rho; the mixed case follows by convexity and concavity of sqrt')
    lscal = band(TAU / 100)
    ratios = {'band_lower': lowp / lscal[0], 'band_upper': upp / lscal[1],
              'z3_formal': (formal_a * TAU ** 2) / (formal_a * (TAU / 100) ** 2), 'graph_coefficients': F(1),
              'dimension_constants': F(1)}
    need(9500 <= ratios['band_lower'] <= 10500 and ratios['band_upper'] == 100 and ratios['z3_formal'] == 10000,
         'scaling_brackets', ratios={k: preview(v) for k, v in ratios.items()})
    n_e = {}
    for b in R_COVER:
        for r_, s_, d in product(range(4), range(2), 'xyz'):
            p = (4 * b[0] + r_, 2 * b[1] + s_, b[2])
            cnt = 0
            for a, c in ORIENT:
                if d not in (a, c):
                    continue
                other = c if d == a else a
                for base_p in (p, add(p, tuple(-x for x in DIRS[other]))):
                    if (p, d) in face_links(base_p, a, c) and not is_selected(base_p, a, c):
                        cnt += 1
            n_e[(p, d)] = cnt
    formal_band = sum(n_e.values(), 0) * F(1, 3456)
    hist = {k: sum(1 for v in n_e.values() if v == k) for k in (2, 3, 4)}
    need(len(n_e) == 48 and sum(n_e.values()) == 168 and hist == {2: 4, 3: 16, 4: 28} and formal_band == F(7, 144)
         and lowp < formal_band * TAU ** 2 < upp, 'electric_formal_per_link', histogram_n_e=hist,
         formal_total=q_(formal_band), formal_at_cap_preview=preview(formal_band * TAU ** 2),
         note='formal second-order value per link 8C_e: n_e tau^2/3456 with n_e in {2,3,4} omitted faces (selected faces '
              'carry 0); total 168/3456 = 7/144 (labelled formal); the band [(3/2)L^2, 98|tau|] contains it; no second-order '
              'upper bound is admitted for the unbounded h_R (the obstruction to a tight enclosure)')

    # 8. 2+1 dimensions -----------------------------------------------------------------------------------------------------------
    am2 = (ROOT / AM2_REPORT).read_text()
    need(all(s_ in am2 for s_ in ('L_k^{\\rm num}=16\\,8^k(1+5k/4)', '=16e^{8t}(1+10t),\\quad', "G'(t)=16e^{8t}(18+80t)",
                                   'k>2p=8', 'exp(1/8)<8/7', "G(R)<148/7,\\quad G'(R)<352", '2^p=16',
                                   '1/|M| <= (p+1)/|I_l|', 'This contributes `2^p(2p)^k k(p+1)/p`')),
         'am2_counting_located')

    def Lnum(p_, k):
        return 2 ** p_ * (2 * p_) ** k * (1 + F(k * (p_ + 1), p_))

    def G_coeff(p_, k):  # t^k coefficient of 2^p e^{2pt}(1 + 2(p+1)t)
        return 2 ** p_ * (F((2 * p_) ** k, factorial(k)) + (2 * (p_ + 1) * F((2 * p_) ** (k - 1), factorial(k - 1)) if k else 0))

    def Gp_coeff(p_, k):  # t^k coefficient of 2^p e^{2pt}((4p+2) + 4p(p+1)t)
        return 2 ** p_ * ((4 * p_ + 2) * F((2 * p_) ** k, factorial(k)) +
                          (4 * p_ * (p_ + 1) * F((2 * p_) ** (k - 1), factorial(k - 1)) if k else 0))
    series_ok = all(F(Lnum(p_, k), factorial(k)) == G_coeff(p_, k) and F(Lnum(p_, k + 1), factorial(k)) == Gp_coeff(p_, k)
                    for p_ in (3, 4) for k in range(30))
    need(series_ok and all(Lnum(4, k) == 16 * 8 ** k * (1 + F(5 * k, 4)) for k in range(12))
         and all(Lnum(3, k) == 8 * 6 ** k * (1 + F(4 * k, 3)) for k in range(12)), 'am2_numerators_general_p',
         note='L_k(p) = 2^p (2p)^k (1 + k(p+1)/p) from the AM2 counting (2^p outputs, p||c||_a per collection, (p+1)/|I_l|); '
              'p=4 gives AM2 16*8^k(1+5k/4); G_p = 2^p e^{2pt}(1+2(p+1)t), G_p\' its derivative, coefficient-wise')
    # declared 2D factorization
    sites = list(product(range(-3, 4), repeat=2))
    owners = {}
    for p in sites:
        owners[p] = frozenset([p, (p[0] + 1, p[1]), (p[0], p[1] + 1)])
    per_site = {u: [p for p in sites if u in owners[p]] for u in product(range(-1, 2), repeat=2)}
    star = {u: frozenset().union(*[owners[p] for p in per_site[u]]) for u in per_site}
    link_faces = {}
    for p in sites:
        for l in (((p[0], p[1]), 'x'), ((p[0], p[1]), 'y'), ((p[0] + 1, p[1]), 'y'), ((p[0], p[1] + 1), 'x')):
            link_faces[l] = link_faces.get(l, 0) + 1
    interior_links = [l for l in link_faces if all(-2 <= v <= 2 for v in l[0])]
    need(all(len(v) == 3 for v in per_site.values()) and all(len(v) == 7 for v in star.values())
         and all(link_faces[l] == 2 for l in interior_links) and max(len(o) for o in owners.values()) == 3,
         'dimension_2p1_factorization', owner_set='{p, p+e_x, p+e_y}', faces_per_site=3, star_sites=7, links_per_site=2,
         faces_per_link=2, per_site_sum_over_abs_tau='1', maximal_support=3)
    # termination order: exact creation-algebra fixtures (p=3: order 6; p=4: order 8)

    def ad_fixture(p_):
        dim = 2 ** p_
        C = [[0] * dim for _ in range(dim)]
        for st in range(dim):
            for i in range(p_):
                if not (st >> i) & 1:
                    C[st | (1 << i)][st] += 1
        V = [[0] * dim for _ in range(dim)]
        V[0][dim - 1] = 1
        V[dim - 1][0] = 1

        def mm(A, B):
            return [[sum(A[i][k] * B[k][j] for k in range(dim)) for j in range(dim)] for i in range(dim)]

        def sub(A, B):
            return [[A[i][j] - B[i][j] for j in range(dim)] for i in range(dim)]
        X, outs = V, []
        for _ in range(2 * p_ + 1):
            X = sub(mm(C, X), mm(X, C))
            outs.append(X)
        return abs(outs[2 * p_ - 1][dim - 1][0]), all(v == 0 for row in outs[2 * p_] for v in row)
    t3, t4 = ad_fixture(3), ad_fixture(4)
    need(t3 == (720, True) and t4 == (40320, True), 'termination_order_fixtures', p3='ad_C^6(V)Omega = -6!|111> (sign (-1)^p), ad_C^7(V)=0',
         p4='ad_C^8(V)Omega = 8!|1111>, ad_C^9(V)=0 (the AM2 fixture)')
    R_ = F(1, 64)
    e_lo, e_hi = exp_bracket(6 * R_)
    e8 = exp_bracket(8 * R_)
    G3 = (8 * e_lo * (1 + 8 * R_), 8 * e_hi * (1 + 8 * R_))
    G3p = (8 * e_lo * (14 + 48 * R_), 8 * e_hi * (14 + 48 * R_))
    cap = 1 / (576 * e_hi)
    e3 = exp_bracket(F(3), 80)
    need(e_lo ** 32 <= e3[1] and e_hi ** 32 >= e3[0], 'exponential_bracket_consistent', exponent='3/32',
         note='the bracket of e^{3/32} raised to the 32nd power brackets e^3 (a 80-term bracket): the exponent 6R=3/32 is '
              'the p=3 value, not the 3+1D 8R=1/8')
    need(G3 == (9 * e_lo, 9 * e_hi) and G3p == (118 * e_lo, 118 * e_hi) and cap * G3[1] <= R_
         and 2 * cap * G3p[1] < 1 and 1 / (576 * e_lo) - cap < F(1, 10 ** 40)
         and 16 * e8[1] * (1 + 10 * R_) < F(148, 7) and 16 * e8[1] * (18 + 80 * R_) < 352 and e8[1] < F(8, 7),
         'dimension_2p1_constants', G3_R=[q_(G3[0]), q_(G3[1])], G3p_R=[q_(G3p[0]), q_(G3p[1])],
         G3_preview=preview(G3[1]), G3p_preview=preview(G3p[1]), cap=q_(cap), cap_preview=preview(cap),
         exclusion_cap_preview=preview(1 / (236 * e_hi)), termination_order=6,
         note='J = |tau| (three faces per site at |tau|/3), R = 1/64, unit on-site gap (AM2 normalization); G_3(R) = '
              '9e^{3/32}, G_3\'(R) = 118e^{3/32}; the self-map J G_3(R) <= R binds: cap = 1/(576 e^{3/32}) (directed lower '
              'bound with a 40-term Taylor bracket); the exclusion 2J G_3\'(R) < 1 allows up to 1/(236 e^{3/32}); the '
              'AM2 3+1D values 148/7, 352 are re-derived from e^{1/8} < 8/7 as an anchor')

    # 9. obligations and no-transfer rows ---------------------------------------------------------------------------------------
    obligations = sorted([
        'area law: no zero-free region of the reduced density is admitted',
        'certified sign of the Z^3 1x2 mean: a uniform fourth-order remainder (the third order vanishes by evenness)',
        'tight electric-energy enclosure: a second-order upper bound for the unbounded h_R',
        'site-blocked uniform 3+1D regime: its own contract',
        '2+1D finite-volume ground-state and gap theorem: a 2D finite-volume prescription, the on-site domains and AM2 '
        'sections 4-6 re-verified',
        '2+1D AQ chain, node and dictionary (g^2 has mass dimension): their own contracts'])
    no_transfer = [{'from': 'Einstein-QED evidence rounds', 'status': 'no shared equation', 'comparison': None}]
    transfer_table = {'verbatim (algebraic)': ['E_2 flip set and the flip identity on Z^2 (one link per plaquette)',
                                               'SU(2) Peter-Weyl parity algebra', 'AM2 counting (recounted at p=3)',
                                               'AV2 window kernel constants (one-dimensional spectral identity)'],
                      'own contract': ['finite-volume theorem', 'AQ chain', 'Euclidean node', 'dictionary']}
    need(len(obligations) == 6, 'obligations_and_no_transfer_rows', obligations=obligations, no_transfer=no_transfer,
         transfers_2p1=transfer_table)

    # 10. packet and controls --------------------------------------------------------------------------------------------------
    enc_ref = {k: (cc['lower'], cc['upper']) for k, cc in certs.items()}
    one_face_W1 = dict(T8['W_1'])
    one_face_W1.pop('1,2')
    dim_constants = {'owner_set': '{p, p+e_x, p+e_y}', 'faces_per_site': 3, 'star_sites': 7, 'per_site_sum': '|tau|',
                     'maximal_support': 3, 'L_k': '8*6^k*(1+4k/3)', 'G_3': '8e^{6t}(1+8t)', "G_3'": '8e^{6t}(14+48t)',
                     'termination_order': 6, 'R': R_, 'G_3(R)_upper': G3[1], "G_3'(R)_upper": G3p[1], 'cap_lower': cap}
    c_ref = {
        'declared_inputs': declared, 'declared_hashes': dict(OBSERVED_INPUTS), 'control_ids': ids,
        'tables': {k: T8[k] for k in ('W_1', 'z', 'C_shared')}, 'one_face_W1': one_face_W1,
        'parities': {k: parities[k] for k in ('W_1', 'z', 'C_shared')},
        'second_order_diag': {'z': F(7, 216), 'C_shared': F(1, 24)},
        'enclosure_keys': sorted(certs), 'enclosures': enc_ref, 'target': target,
        'rectangle': sorted([list(p) + [d] for p, d in rect]), 'formal_1x2': formal_a, 'K2p': k2p,
        'band_endpoints': {'lower': lowp, 'upper': upp}, 'formal_band': formal_band, 'dim_constants': dim_constants,
        'obligations': obligations, 'no_transfer': no_transfer, 'forbidden': forbidden, 'sentence': template,
        'brackets': {'band_lower': (9500, 10500), 'band_upper': (100, 100), 'z3_formal': (10000, 10000),
                     'graph_coefficients': (1, 1), 'dimension_constants': (1, 1)},
        'gate_fields': pre['gate_fields_required'], 'error_terms': pre['error_terms_itemized'],
    }

    def build_packet():
        enc = {}
        for k, cc in certs.items():
            enc[k] = {'lower': cc['lower'], 'upper': cc['upper'], 'sign_certified': True, 'tier': None,
                      'meets_target': ((cc['upper'] - cc['lower']) / min(abs(cc['lower']), abs(cc['upper'])) <= target)
                      if k.startswith('8,') else None,
                      'residual': copy.deepcopy(cc['ledger'])}
        pk = {
            'contract_sha256': CONTRACT_SHA256, 'inputs': dict(OBSERVED_INPUTS), 'controls': {k: True for k in ids},
            'admission_reads_preview': False,
            'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False},
            'provenance_premises': [], 'parameters': {k: par[k] for k in ('metric', 'weights', 'window', 'clock')},
            'graph': {'model_id': MODEL_ID, 'couplings': ['l1', 'l2'], 'independent': True,
                      'hamiltonian_terms': copy.deepcopy(GRAPH_TERMS), 'free_reference_same_code_path': True,
                      'model_is_finite_graph': True, 'transfers_to_aq': False, 'units': 'alpha', 'rho': 1,
                      'sector': 'gauge-invariant', 'tables': copy.deepcopy({'6': {k: tables['6'][k] for k in ('W_1', 'z', 'C_shared')},
                                                                              '8': {k: T8[k] for k in ('W_1', 'z', 'C_shared')}}),
                      'coefficient_meta': {k: [{'tier': None}] for k in ('W_1', 'z', 'C_shared')},
                      'fitted': False, 'truncation_error': '0',
                      'flips': {'l1': 'nonshared link of face 1 (h1, vL or h3)', 'l2': 'nonshared link of face 2 (h2, vR or h4)'},
                      'parity_checked_on': 'two-variable coefficient table',
                      'parities': {k: parities[k] for k in ('W_1', 'z', 'C_shared')},
                      'second_order_at_equal_couplings': {'z': F(7, 216), 'C_shared': F(1, 24)}},
            'enclosures': enc, 'target': target,
            'z3_1x2': {'rectangle': sorted([list(p) + [d] for p, d in rect]), 'rectangle_links_owned_by': ['0', 'e_z'],
                       'first_order': 0,
                       'formal': {'label': 'formal_second_order_coefficient', 'value': formal_a, 'sign_claimed': False,
                                  'third_order_remainder': None, 'value_at_cap_claimed': False},
                       'bound': {'constant': k2p, 'tier': 'exact_first_order', 'source': 'AY1',
                                 'encloses_formal_coefficient': False, 'sign': None,
                                 'scope': ['F1 boxes', 'F2 boxes', 'limit of the named constructions']},
                       'evenness': {'scope': ['open centered whole-star boxes (F1)', 'every on-site cutoff',
                                              'limit of the named constructions (BB2 at each sign)'],
                                    'source': 'AW1 flip lemma, |C cap E_3|=6 (area 2)', 'remainder_bound': None}},
            'band': {'observable': 'omega(h_R), h_R = sum of 8 C_e over the 48 links of R',
                     'passage': 'monotone limit over the spectral cutoffs of h_R',
                     'lower': {'tier': 'first_order_distance_from_product',
                               'steps': ['h_R >= 6 Q_R (I1)', 'Fuchs-van de Graaf, pure reference, proved inline',
                                         'lower bound on ||rho_R - P_R||_1'],
                               'source_limit': 'AY2 gate item (2) with BB2 items 2-3',
                               'source_boxes': 'AY1 forward F11-F14 per box'},
                     'upper': {'tier': 'crude_majorant', 'budget_over_abs_tau': 98,
                               'source': 'AQ1 HNM-AQ1.1, 7 incident anchors',
                               'limit_passage': 'lower semicontinuity of the monotone cutoff limit'},
                     'bounded_constant_applied_to_h_R': False, 'signs': ['+', '-'],
                     'scope': ['F1 boxes', 'F2 boxes', 'limit of the named constructions'],
                     'endpoints': {'+': {'lower': lowp, 'upper': upp}, '-': {'lower': lowm, 'upper': upm}},
                     'formal_per_link': {'label': 'formal', 'total': formal_band}},
            'dimension_2p1': {'label': '2+1D declared model (single-site factors on Z^2)', 'tier': None,
                              'constants': dict(dim_constants), 'finite_volume_theorem_claimed': False,
                              'dictionary': 'own contract (g^2 has mass dimension)'},
            'obligations': list(obligations), 'no_transfer': copy.deepcopy(no_transfer), 'comparisons': [],
            'rates': [],
            'statements': ['BD2 makes no new claim of a rate in N.',
                           'No area-law bound and no string-tension statement is made.'],
            'sentence': template, 'sentence_count': 1, 'sub_labels': list(SUB_LABELS),
            'scaling': {k: ratios[k] for k in ('band_lower', 'band_upper', 'z3_formal', 'graph_coefficients',
                                               'dimension_constants')},
            'verdict': 'accepted_within_scope', 'retuned': False,
            'gate_fields': copy.deepcopy(pre['gate_fields_required']),
            'error_terms': {k: 'itemized: exact (' + k + ')' for k in pre['error_terms_itemized']},
        }
        return rebind(pk)

    base_pk = build_packet()
    need(validate(base_pk, c_ref) is True, 'packet_validator_accepts_own_derivation')

    def mk(fn, rebind_after=True):
        def run():
            pk = build_packet()
            fn(pk)
            if rebind_after:
                rebind(pk)
            validate(pk, c_ref)
        return run

    def setp(path, value):
        def f(pk):
            cur = pk
            for k in path[:-1]:
                cur = cur[k]
            cur[path[-1]] = value
        return mk(f)

    def addst(text):
        return mk(lambda pk: pk['statements'].append(text))

    k8 = '8,1/10'
    ctl, pos = {}, {}
    ctl['coherent_evidence_tampering'] = [
        ('control Boolean flipped and rebound', mk(lambda pk: pk['controls'].__setitem__(ids[5], False)),
         'coherent evidence tampering: control booleans'),
        ('snapshot removed and rebound', mk(lambda pk: pk['inputs'].pop('research/round11/solver/README.md')),
         'coherent evidence tampering: snapshot inventory'),
        ('undeclared read of the BD1 packet', mk(lambda pk: pk['inputs'].__setitem__('research/round33/forward/bd1/report.md',
                                                                                    '0' * 64)),
         'coherent evidence tampering: undeclared read'),
        ('snapshot hash edited and rebound', mk(lambda pk: pk['inputs'].__setitem__('research/round32/forward/az2/check.py',
                                                                                   '2' * 64)),
         'coherent evidence tampering: snapshot hash'),
        ('control flipped without rebinding', mk(lambda pk: pk['controls'].__setitem__(ids[0], False), rebind_after=False),
         'coherent evidence tampering: freeze digest'),
        ('enclosure shifted off the certified one', mk(lambda pk: pk['enclosures'][k8].update(
            {'lower': pk['enclosures'][k8]['lower'] * 2, 'upper': pk['enclosures'][k8]['upper'] * 2})),
         'coherent evidence tampering: enclosure disjoint'),
    ]
    ctl['exact_arithmetic_admission'] = [
        ('float band endpoint', mk(lambda pk: pk['band']['endpoints']['+'].__setitem__('upper', 9.8e-07)),
         'exact arithmetic: float in packet'),
        ('preview read by admission', mk(lambda pk: pk.__setitem__('admission_reads_preview', True)),
         'exact arithmetic: preview read by admission'),
    ]
    ctl['no_priority_or_continuum_claim'] = [
        ('continuum claim', mk(lambda pk: pk['claims'].__setitem__('continuum_claim', True)), 'no priority or continuum claim'),
        ('weak coupling gate field', mk(lambda pk: pk['gate_fields'].__setitem__('weak_coupling_claim', True)),
         'no priority or continuum claim'),
        ('historical provenance as premise', mk(lambda pk: pk['provenance_premises'].append('Tesla lecture')),
         'no priority or continuum claim'),
    ]
    ctl['changed_model_relabelled'] = [
        ('one-face value under the independent-coupling label', mk(lambda pk: pk['graph']['tables']['8'].__setitem__(
            'W_1', dict(one_face_W1)) or pk['graph']['tables']['6'].__setitem__('W_1', dict(one_face_W1))),
         'changed model relabelled: one-face graph value'),
        ('equal-coupling model labelled independent', mk(lambda pk: pk['graph'].__setitem__('couplings', ['tau_FG'])),
         'changed model relabelled: graph coupling label'),
        ('F1-only bound under the F2 label', setp(['z3_1x2', 'bound', 'scope'], ['F1 boxes', 'F1 boxes (as F2)',
                                                                             'limit of the named constructions']),
         'changed model relabelled: bound scope'),
        ('graph value presented as a Z^3 value', setp(['band', 'observable'], '<C_shared> on the two-plaquette graph'),
         'changed model relabelled: band observable'),
        ('3+1D model under the 2+1D label', setp(['dimension_2p1', 'label'], '3+1D whole-star model'),
         'changed model relabelled: 2+1D label'),
        ('sub-labels changed', mk(lambda pk: pk.__setitem__('sub_labels', ['static_not_dynamic'])),
         'changed model relabelled: sub-labels'),
    ]
    ctl['insufficient_verdict_retained'] = [
        ('accepted with a missed width target', mk(lambda pk: pk['enclosures'][k8].update(
            {'lower': pk['enclosures'][k8]['lower'] - F(1, 10 ** 8), 'meets_target': True})),
         'insufficient verdict retained: target flag'),
        ('target retuned', mk(lambda pk: pk.__setitem__('target', F(1, 10 ** 10))), 'insufficient verdict retained: target retuned'),
        ('accepted after retuning', mk(lambda pk: pk.__setitem__('retuned', True)), 'insufficient verdict retained'),
        ('enclosure missing', mk(lambda pk: pk['enclosures'].pop('6,-1/100')), 'insufficient verdict retained: enclosure missing'),
        ('obligation dropped', mk(lambda pk: pk['obligations'].pop(0)), 'insufficient verdict retained: obligations'),
    ]
    pos['insufficient_verdict_retained'] = [
        ('limited with the missed-target flag and its reason accepted',
         mk(lambda pk: (pk['enclosures'][k8].update({'lower': pk['enclosures'][k8]['lower'] - F(1, 10 ** 8),
                                                     'meets_target': False}),
                        pk.update({'verdict': 'limited', 'dominating_reason': 'D=8 width at l=1/10 misses 1/10^16'}))))]
    ctl['placeholder_span_rejected'] = [
        ('placeholder in a statement', addst('The enclosure at <grid point> is certified.'), 'placeholder span'),
        ('placeholder in the sentence', mk(lambda pk: pk.__setitem__('sentence', template + ' <value | bound>')),
         'placeholder span'),
    ]
    ctl['negation_aware_phrase_scan'] = [
        ('affirmative forbidden phrase', addst('The band holds in the thermodynamic limit.'), 'negation aware phrase scan'),
        ('predicts', addst('The graph predicts the Z^3 1x2 coefficient.'), 'negation aware phrase scan'),
    ]
    pos['negation_aware_phrase_scan'] = [('negated phrase accepted', addst('This is not a statement about the '
                                                                            'thermodynamic limit.'))]
    ctl['parameters_declare_metric_weights_window'] = [
        ('window removed', mk(lambda pk: pk['parameters'].pop('window')), 'parameters must declare metric weights window'),
        ('clock without reason', mk(lambda pk: pk['parameters'].__setitem__('clock', 's=alpha t_E/hbar')),
         'parameters must declare metric weights window'),
    ]
    ctl['tier_mixing_rejected'] = [
        ('tier on a graph coefficient', mk(lambda pk: pk['graph']['coefficient_meta']['z'][0].__setitem__(
            'tier', 'exact_first_order')), 'tier mixing: tier on a graph coefficient'),
        ('tier on a graph enclosure', mk(lambda pk: pk['enclosures'][k8].__setitem__('tier', 'crude_majorant')),
         'tier mixing: tier on a graph enclosure'),
        ('lower endpoint under the upper tier', setp(['band', 'lower', 'tier'], 'crude_majorant'),
         'tier mixing: lower endpoint tier'),
        ('upper endpoint under the lower tier', setp(['band', 'upper', 'tier'], 'first_order_distance_from_product'),
         'tier mixing: upper endpoint tier'),
        ('plan route label on the 1x2 bound', setp(['z3_1x2', 'bound', 'tier'], 'polymer_kp'), 'tier mixing: bound tier'),
        ('Lieb-Robinson tier on the 1x2 bound', setp(['z3_1x2', 'bound', 'tier'], 'polynomial_lieb_robinson'),
         'tier mixing: bound tier'),
        ('tier on a 2+1D constant', setp(['dimension_2p1', 'tier'], 'exact_first_order'), 'tier mixing: tier on a 2+1D'),
        ('tier on the formal coefficient', setp(['z3_1x2', 'formal', 'tier'], 'exact_first_order'),
         'tier mixing: tier on the formal coefficient'),
    ]
    ctl['graph_couplings_named'] = [
        ('a Hamiltonian term dropped', mk(lambda pk: pk['graph']['hamiltonian_terms'].pop()), 'graph couplings named'),
        ('free reference from another code path', setp(['graph', 'free_reference_same_code_path'], False),
         'graph couplings named'),
        ('transfers_to_aq true', setp(['graph', 'transfers_to_aq'], True), 'graph couplings named'),
        ('rho changed', setp(['graph', 'rho'], 2), 'graph couplings named: units, rho or sector'),
    ]
    ctl['exact_rs_zero_truncation'] = [
        ('coefficient differs between cutoffs', mk(lambda pk: pk['graph']['tables']['6']['z'].__setitem__('3,1', '-1/2000')),
         'exact rs zero truncation: coefficient differs between cutoffs'),
        ('fitted coefficients', setp(['graph', 'fitted'], True), 'exact rs zero truncation: fitted'),
        ('coefficient value changed at both cutoffs', mk(lambda pk: [pk['graph']['tables'][d]['C_shared'].__setitem__(
            '2,2', '0') for d in ('6', '8')]), 'exact rs zero truncation: coefficient value'),
        ('cutoff D=6 missing', mk(lambda pk: pk['graph']['tables'].pop('6')), 'exact rs zero truncation: cutoff missing'),
    ]
    ctl['independent_coupling_flip'] = [
        ('shared-link flip for both couplings', setp(['graph', 'flips'], {'l1': 'shared link vM', 'l2': 'shared link vM'}),
         'independent coupling flip: flip per coupling'),
        ('parity checked at l1=l2 only', setp(['graph', 'parity_checked_on'], 'l1=l2 series'),
         'independent coupling flip: parity checked at l1=l2 only'),
        ('two-variable parity from a single flip', setp(['graph', 'flips'], {'l1': 'nonshared link of face 1 (h1, vL or h3)',
                                                                            'l2': 'nonshared link of face 1 (h1, vL or h3)'}),
         'independent coupling flip: flip per coupling'),
        ('wrong parity recorded', mk(lambda pk: pk['graph']['parities'].__setitem__('W_1', 'odd in l1, odd in l2')),
         'independent coupling flip: parities'),
    ]
    ctl['enclosure_itemized_residual'] = [
        ('joint channel dropped', mk(lambda pk: pk['enclosures'][k8]['residual'].pop('b_joint_channel')),
         'enclosure itemized residual'),
        ('Ritz part dropped', mk(lambda pk: pk['enclosures']['6,1/1000']['residual'].pop('d_ritz')),
         'enclosure itemized residual'),
        ('per-link rows incomplete', mk(lambda pk: pk['enclosures']['8,-1/100']['residual']['a_per_link_rows'].pop()),
         'enclosure itemized residual: per-link rows'),
        ('gauge projection nonzero', mk(lambda pk: pk['enclosures']['8,1/100']['residual'].__setitem__(
            'c_gauge_projection', 'bounded by 1e-30')), 'enclosure itemized residual: per-link rows or gauge'),
        ('enclosure without residual', mk(lambda pk: pk['enclosures']['6,1/10'].pop('residual')),
         'enclosure itemized residual'),
    ]
    ctl['formal_coefficient_labelled'] = [
        ('formal coefficient called certified', setp(['z3_1x2', 'formal', 'label'], 'certified_second_order_coefficient'),
         'formal coefficient labelled'),
        ('sign claimed', setp(['z3_1x2', 'formal', 'sign_claimed'], True), 'formal coefficient labelled'),
        ('bound presented as an enclosure of the formal coefficient', setp(['z3_1x2', 'bound', 'encloses_formal_coefficient'],
                                                                          True),
         'formal coefficient labelled: bound presented as an enclosure'),
        ('rectangle not contained in R', setp(['z3_1x2', 'rectangle_links_owned_by'], ['-e_x', '0', 'e_z']),
         'formal coefficient labelled: rectangle not contained in R'),
        ('formal value changed', setp(['z3_1x2', 'formal', 'value'], F(7, 5184)), 'formal coefficient labelled: value'),
        ('value at the cap claimed', setp(['z3_1x2', 'formal', 'value_at_cap_claimed'], True), 'formal coefficient labelled'),
    ]
    ctl['evenness_from_flip'] = [
        ('F2 boxes claimed', setp(['z3_1x2', 'evenness', 'scope'], ['open centered whole-star boxes (F1)', 'F2 boxes',
                                                                   'limit of the named constructions (BB2 at each sign)']),
         'evenness from flip: F2 boxes claimed'),
        ('limit without BB2', setp(['z3_1x2', 'evenness', 'scope'], ['open centered whole-star boxes (F1)',
                                                                    'every on-site cutoff', 'AQ subsequential limits']),
         'evenness from flip: scope'),
        ('remainder claimed from evenness', setp(['z3_1x2', 'evenness', 'remainder_bound'], 'O(tau^3)'),
         'evenness from flip: source or remainder'),
    ]
    ctl['unbounded_observable_handled'] = [
        ('bounded-observable constant applied to h_R', setp(['band', 'bounded_constant_applied_to_h_R'], True),
         'unbounded observable handled: bounded constant'),
        ('limit-level AY2 distance used for a finite box', setp(['band', 'lower', 'source_boxes'], 'AY2 gate item (2)'),
         'unbounded observable handled: limit-level distance for a finite box'),
        ('upper budget 112|tau| (generic AQ1)', mk(lambda pk: [pk['band']['endpoints'][s_].__setitem__('upper', 112 * TAU)
                                                             for s_ in ('+', '-')]),
         'unbounded observable handled: upper budget other than the frozen one'),
        ('upper budget passed to the limit by trace-norm continuity', setp(['band', 'upper', 'limit_passage'],
                                                                          'trace-norm continuity'),
         'unbounded observable handled: limit passage'),
        ('Fuchs-van de Graaf cited, not proved', setp(['band', 'lower', 'steps'], ['h_R >= 6 Q_R (I1)',
                                                                                 'Fuchs-van de Graaf (cited)',
                                                                                 'lower bound on ||rho_R - P_R||_1']),
         'unbounded observable handled: lower endpoint steps'),
        ('no cutoff passage', setp(['band', 'passage'], 'direct expectation'), 'unbounded observable handled: passage'),
    ]
    ctl['band_both_signs'] = [
        ('one sign only', setp(['band', 'signs'], ['+']), 'band both signs: sign missing'),
        ('finite boxes only', setp(['band', 'scope'], ['F1 boxes', 'F2 boxes']), 'band both signs: scope'),
        ('minus-sign endpoint changed', mk(lambda pk: pk['band']['endpoints']['-'].__setitem__('lower', lowm / 2)),
         'band both signs: endpoints'),
    ]
    ctl['dimension_recount'] = [
        ('3+1D per-site sum reused', mk(lambda pk: pk['dimension_2p1']['constants'].__setitem__('per_site_sum', '28|tau|')),
         'dimension recount: per_site_sum'),
        ('3+1D termination order reused', mk(lambda pk: pk['dimension_2p1']['constants'].__setitem__('termination_order', 8)),
         'dimension recount: termination_order'),
        ('3+1D G(R) bound reused', mk(lambda pk: pk['dimension_2p1']['constants'].__setitem__('G_3(R)_upper', F(148, 7))),
         'dimension recount: G_3(R)_upper'),
        ('cap from the self-map alone at the optimal radius', mk(lambda pk: pk['dimension_2p1']['constants'].__setitem__(
            'cap_lower', cap * 2)), 'dimension recount: cap_lower'),
        ('finite-volume theorem claimed', setp(['dimension_2p1', 'finite_volume_theorem_claimed'], True),
         'dimension recount: theorem or dictionary'),
        ('3+1D dictionary', setp(['dimension_2p1', 'dictionary'], 'tau=96/g^4'), 'dimension recount: theorem or dictionary'),
    ]
    ctl['no_area_law_claim'] = [
        ('area law gate field', mk(lambda pk: pk['gate_fields'].__setitem__('area_law_claimed', True)), 'no area law claim'),
        ('string tension statement', addst('The 1x2 mean gives the string tension.'), 'no area law claim'),
        ('area law statement', addst('The Wilson loops obey an area law.'), 'no area law claim'),
    ]
    pos['no_area_law_claim'] = [('negated area-law sentence accepted', addst('No area law is claimed.'))]
    ctl['no_transfer_to_eqed'] = [
        ('Einstein-QED row dropped', mk(lambda pk: pk.__setitem__('no_transfer', [])), 'no transfer to eqed'),
        ('Einstein-QED as a comparison', mk(lambda pk: pk['comparisons'].append({'with': 'Einstein-QED round 5'})),
         'no transfer to eqed'),
    ]
    ctl['rate_range_stated'] = [
        ('rate without range', mk(lambda pk: pk['rates'].append({'what': 'band', 'range': ''})), 'rate range stated'),
        ('O(1/N)', addst('The band converges at O(1/N).'), 'rate range stated: O(1/N)'),
        ('unqualified rate', addst('The enclosures shrink at a geometric rate.'), 'rate range stated: unqualified rate'),
    ]
    pos['rate_range_stated'] = [('rate in N with range accepted', mk(lambda pk: pk['rates'].append(
        {'what': 'inherited BB2 correlation rate', 'range': '5<=N<=14000'})))]
    for cid in ids:
        control(cid, ctl[cid], positives=pos.get(cid, ()))
    need(sorted(ctl) == sorted(ids), 'every_control_executed', controls=len(ids),
         mutations=sum(len(v) for v in ctl.values()))

    readings = [
        'R1: the frozen AZ2-type ledger is met by a Ritz vector with the tail comparison; with the full-residual '
        'Davis-Kahan angle alone the D=8 relative width at l=1/10 sits within about 15 per cent of 1/10^16.',
        'R2: the independent-coupling tables need two flips (h1 for l1, h2 for l2); the vM flip only gives the l1=l2 '
        'statement; <W_1> has only (odd, even) monomials, <z> (odd, odd), <C_shared> (even, even).',
        'R3: the formal Z^3 1x2 coefficient 7/124416 equals the graph <z> coefficient 7/216 under tau_FG=tau/24 exactly.',
        'R4: the band lower end (3/2)L^2 is second order and the upper end 98|tau| first order; the formal value 7tau^2/144 '
        'lies inside; a tight enclosure needs a second-order upper bound for the unbounded h_R.',
        'R5: in 2+1D the self-map binds at R=1/64: cap 1/(576 e^{3/32}); the exclusion condition allows 1/(236 e^{3/32}).',
        'R6: the target note edit of the pre-freeze review was superseded by the advisor tightening the target; the '
        'definitions it carried are in the frozen note.',
    ]
    return {
        'loop': 'BD2', 'stage': 'pre_comparison', 'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'skeptic (model agent, correlated ancestry; not human review)',
        'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'model': 'FG(round11_two_plaquette_independent_couplings): H = K - l1 W_1 - l2 W_2 in alpha units (rho=1, '
                 'gauge-invariant sector, D in {6,8}); the zero-selected SU(2) family (F1, F2, the limit of the named '
                 'constructions) at tau=+-10^-8 for the 1x2 loop and the electric band on R={0,e_z}; the declared 2+1D model '
                 'for the AM2 constants',
        'graph_tables': {k: T8[k] for k in ('W_1', 'W_2', 'z', 'C_shared', 'E_0')},
        'enclosures': {k: {'lower': q_(cc['lower']), 'upper': q_(cc['upper']), 'relative_width_preview': preview(rel[k]),
                           'half_width_preview': preview(cc['hw']), 'center_preview': format(float(cc['q']), '.20e'),
                           'ritz_iterations': cc['iterations'], 'residual_ledger': cc['ledger']}
                       for k, cc in sorted(certs.items())},
        'z3_1x2': {'formal_second_order_coefficient': q_(formal_a), 'bound_K2p_tau2': q_(bound_1x2),
                   'first_order': '0', 'C_cap_E3': 6},
        'band': {'lower': q_(lowp), 'upper': q_(upp), 'formal_total_coefficient': q_(formal_band),
                 'n_e_histogram': {str(k): v for k, v in hist.items()}},
        'dimension_2p1': {k: q_(v) if isinstance(v, F) else v for k, v in dim_constants.items()},
        'obligations': obligations, 'no_transfer': no_transfer, 'transfers_2p1': transfer_table,
        'scaling': {k: q_(v) for k, v in ratios.items()},
        'contract_readings': readings,
        'predictions': {'graph_W1': T8['W_1'], 'graph_z': T8['z'], 'graph_C_shared': T8['C_shared'],
                        'z_second_order_diag': '7/216', 'C_shared_second_order_diag': '1/24',
                        'max_relative_width_D8': preview(max(rel['8,%s' % l] for l in GRID)),
                        'z3_formal': q_(formal_a), 'band_lower': preview(lowp), 'band_upper': preview(upp),
                        'G3_R': preview(G3[1]), 'G3p_R': preview(G3p[1]), 'cap_2p1': preview(cap)},
        'gate_fields': pre['gate_fields_required'], 'sentence': template,
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                   'uniqueness_of_ground_state_claimed': False, 'area_law_claimed': False},
        'deferred_parts': {'inventory': 'recorded by find and sha256 (names only)', 'phrase_scan': 'mirror of the round tool',
                           'tampering': 'packet level (synthetic packet built from this derivation)',
                           'z3_band_limit': 'the BB2 identification and lower semicontinuity steps are restated in the '
                                            'derivation, not machine-checked',
                           'enclosure_theorem': 'the angle lemmas (Q- and P\'-projected eigen-equations, interlacing) are '
                                                'restated in the derivation; their inputs are exact here'},
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
                      'max_relative_width_D8': result['predictions']['max_relative_width_D8']}))


if __name__ == '__main__':
    main()
