#!/usr/bin/env python3
"""Round33 BB2 skeptic pre-comparison checker (zero-selected patterned family).

Written after the BB2 contract froze (sha256 ed5c0b24...) together with BB1 (sha256 30400d2e...), from
the frozen contracts, advisor/selection-bb2.md, advisor/plan.json, experts/modern/bb-targets-proposal.md
and advisor/deliberation-2.md (advisor-only previews), the skeptic's own bb-contract-review, and the
premises (BA1/BA2 gates and reports, the skeptic BA1/BA2 reviews, AQ1/AQ2 reports and gates, AV1, AY1,
AY2, AW1, the committed Nachtergaele-Sims excerpt), before reading research/round33/{forward,reverse}/bb1/
or research/round33/{forward,reverse}/bb2/ (only the BB2 inputs/ file names were listed and hashed; the
recorded inventory is embedded below). Nothing is imported from any producer, lens or tool. Standard
library only. Every admission Boolean is decided with fractions.Fraction and directed exponential
enclosures; floats appear only in the labelled 'previews' block. Every check and control raises an
explicit exception, so python -O cannot disable it. Model-agent skeptic with correlated ancestry; not
human peer review. Human project author: Hruday N M (BUNZEEY).

What is derived here:
  * the BB2 state constants as explicit nondecreasing functions of the BB1 hypothesis constants
    (C_h, c_h) under nested telescoping (factor 1/(1-q)) and the direct union/general-volume
    comparison (factor 1), evaluated at C_h=1/250000, c_h=1/500000, q=1/64 and at the secondary pair;
  * exact telescoping sums over all M > N, the region exponent shift d_Y(k)=d_Y(N)+(k-N), the common
    limit bound, the coarse translation bound C_h q^(N-|v|_inf-1) with the box containment checked by
    enumeration, and the non-coarse translation counter-fixture from fine coordinates;
  * C_dyn from the six BA2 gate constants (parsed from the pinned gate, each reproduced from its exact
    formula), for every natural assembly, with tau/100 ratios; the item-5 three-term sum at N=5,10,20;
  * exact fixtures (whole sequence versus subsequence, translation residues, complex-mean centering,
    cutoff-limit order, cross-coupling, polynomial tail, fixed versus moving vector);
  * a discharge engine that maps a BB1 gate outcome (comparison, form, cutoff regime, sign, constant,
    bound shape) to the BB2 items, exercised on labelled synthetic BB1 outcomes (not BB1 results);
  * a packet validator that executes the 34 contract controls (and extras) as damaging mutations.

Usage: python3 -B research/round33/skeptic/bb2_check.py --output /absolute/fresh/dir
"""
import argparse
import copy
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = 'research/round33/contracts/bb2.json'
CONTRACT_SHA256 = 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35'
BB1_CONTRACT_REL = 'research/round33/contracts/bb1.json'
BB1_CONTRACT_SHA256 = '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018'
REVIEW_REL = 'research/round33/skeptic/bb-contract-review.json'  # the skeptic's own pre-freeze review (not a premise)
REVIEW_SHA256 = 'c43549ef9deffd9e84c10e4266ff322c897b3d8e5f175ab52d68bdbdcd5f4ea2'
# advisor/plan.json is edited by the advisor during the round, so it is not read at run time (a release replay
# would fail). The vocabulary this program needs was recorded from plan.json at sha256 fb018ac5... on 2026-09-24.
PLAN_RECORD = {
    'sha256': 'fb018ac54de3b2153e4af70aea93703a07ab1955ee1e1f102c73732cef694713',
    'gate_fields': ['coefficient_cauchy_claimed', 'common_limit_claimed', 'continuum_claim', 'dynamics_level',
                    'dynamics_limit_identified_claimed', 'gns_dynamics_equality_claimed', 'model_is_finite_graph',
                    'rate_in_N_claimed', 'rate_in_a_claimed', 'scientific_priority_verified', 'state_convergence_claimed',
                    'state_decay_claimed', 'state_decay_scope', 'transfers_to_aq', 'translation_invariance_claimed',
                    'translation_invariance_scope', 'uniform_in_time_claimed', 'uniqueness_of_ground_state_claimed',
                    'weak_coupling_claim', 'whole_sequence_claimed', 'whole_sequence_scope'],
    'sub_labels_allowed': ['boundary_decay_rate_only', 'certificate_restated_for_limit', 'common_limit_of_named_constructions',
                           'convergence_of_named_constructions', 'dynamics_on_compact_windows', 'obstruction_recorded',
                           'reference_unresolved', 'sign_certified_below_cap', 'sign_certified_finite_graph',
                           'static_not_dynamic', 'transfer_to_named_model', 'uniform_local_closeness_not_uniqueness'],
    'tier_names_allowed': ['analytic_disc', 'crude_majorant', 'duhamel_inner_f1', 'duhamel_inner_f2', 'exact_first_order',
                           'exponential_lieb_robinson', 'first_order_distance_from_product', 'iterated_split', 'polymer_kp',
                           'polynomial_lieb_robinson', 'weighted_norm'],
    'assembly_values': ['nested_telescoping', 'union_comparison'],
    'history_events_with_plan_sha256_at_freeze': ['BA1 and BA2 frozen'],
}
# contracts frozen before BB2 (semantics inheritance is judged against these only; later contracts cannot change it)
EARLIER_ROUND33_CONTRACTS = ('research/round33/contracts/ba1.json', 'research/round33/contracts/ba2.json', BB1_CONTRACT_REL)
PHRASE_SCAN_MIRRORED_SHA256 = '1c31a4958c4a44144c5d4f256db551385d216b86309eadc54a608c5e2a4ff0e2'
FREEZER_MIRRORED_SHA256 = 'a33517170edb2ef9f8a1aada0e45b30f837482f3c29958e0c332dee4bea2b923'
GATES = {  # admitted gates read by this program, sha256 pinned (hash_binding.admitted_gate_sha256_pinned_in_check_py)
    'research/round33/advisor/ba1-gate.json': '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    'research/round33/advisor/ba2-gate.json': 'e6b163fc8f80de28c51609f77d0bef21dcdc1286638c862ad67202e6f7b0ca35',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/advisor/aq2-gate.json': '930b697db343ffd261c303c34e6ddd8c6e9c753ee6707931c55dc4171ee47575',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
}
AQ1_REPORT_REL = 'research/round29/forward/aq1/report.md'
AV1_REPORT_REL = 'research/round32/forward/av1/report.md'

# Producer input inventories, recorded by the skeptic on 2026-09-24 with `find` over
# research/round33/{forward,reverse}/bb2/inputs (file names only) and a sha256 comparison of each snapshot
# with the repository file: 38 paths per producer, the same 38 for both, every snapshot byte-identical to the
# repository, the bb1.json snapshot equal to the frozen BB1 sha256. This program does not open those folders.
OBSERVED_INPUTS = {
    'AGENTS.md': '870e1a6b1ff81d6e09888d7084dada2dfdb8128048d97857d9c6b1ffce1b9285',
    'research/round21/forward/i1/report.md': '836a4c7d421f0ddf3589c159d2f057839421532c88157a054a61b51c25c781a9',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/advisor/aq2-gate.json': '930b697db343ffd261c303c34e6ddd8c6e9c753ee6707931c55dc4171ee47575',
    'research/round29/forward/am2/report.md': '1b58fb9c1a199f06b156d04c2a9e89f34ba63cf675a5f7c8bfc25bb568e4e019',
    'research/round29/forward/aq1/report.md': 'b091266f5db009fa967a2adea352fa1b190193cc4bcdc6c4c207e5872fc51da3',
    'research/round29/forward/aq2/report.md': '9144964ca53c995c6c3391625e1a9774d243aefbada43a4e8f8e30f5769589d1',
    'research/round29/reverse/am2/report.md': 'e7313e6a591bacbf37b65c84d57049d2f05a67222cddb8073286e2cd4143d06e',
    'research/round29/skeptic/am2.md': '2aa921a651a49d043fd30d3e52b845c38a668cc5c2a2f4bf18d4f003bb2f74a7',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round32/forward/av1/report.md': '7f86e941933913584de2b9e542359e4a3b3c275c1bc8623dca3c367d88437353',
    'research/round32/forward/aw1/report.md': 'ea3a936244a31c7ea4d2c8de65798b2bb0fc65a60437122b71a30465e089d883',
    'research/round32/forward/ay1/report.md': '7cb1e844d75ee1f3d69de2bccb9a684c791e34bf64f3bb9e2d5061221f75dac1',
    'research/round32/forward/ay2/report.md': '527ce2f2700764d76f98efd245fd5f5fa95444f97ca81e323aaff48fac781e6b',
    'research/round32/reverse/av1/report.md': '02cd908e89b36a1bf377dcbb8f5bf0bdfdd3272375a95f898e71e8fc4aa16d65',
    'research/round32/reverse/ay1/report.md': 'd54e2c073f2510091ca091cf84e4a2e1dbbfbc7c051e8b307b272edbf5eeec8b',
    'research/round33/advisor/ba1-gate.json': '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    'research/round33/advisor/ba2-gate.json': 'e6b163fc8f80de28c51609f77d0bef21dcdc1286638c862ad67202e6f7b0ca35',
    'research/round33/advisor/selection-bb2.md': '639a6054ab1dabb4ae17c85981135e6b11eee83caae611377e5ebcfe02ec9a47',
    'research/round33/contracts/bb1.json': '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018',
    'research/round33/contracts/bb2.json': 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35',
    'research/round33/forward/ba1/report.md': 'd8ed5bfa780b95a57e5ba822b81f0fea5f71aaa7ea1a01bb4dbecb0d417aa769',
    'research/round33/forward/ba2/report.md': '101b404ce2aea29ed6bfd7264f6b4527c7decb73aea9386ce0885fa9b72f7d98',
    'research/round33/methods/historical-physics-panel/SKILL.md': 'a2b366bc661794ee89c29233d0887868b60c0853c85ec136e0529b6f1d5e223a',
    'research/round33/methods/newton-analysis-synthesis/SKILL.md': '2fa3dab9b2420d157457ad3ccaeb0723fb1952871be3e6140dcd3d3c9346ccef',
    'research/round33/methods/paired-physics-research/SKILL.md': '01cda7ee8f8e3eb65c68b0ac6ff0d9e87198f57ea2d997d810d7907b85f4278d',
    'research/round33/methods/paired-physics-research/references/complete-residual-and-error-scope.md': '9e387df64ae05738e740d2ff65973cef0672530e64344ab9e730a139b81b435d',
    'research/round33/methods/qeg-research-advisor/references/round32-state-lemma-and-window.md': '78dc75607920ae799331d6b27b725cba54139d9aceaf04ccbac32a20205a4977',
    'research/round33/methods/tesla-mechanism-resonance/SKILL.md': '81f6d760b3aa45d32db4ae31a3a3c9bec5e1d662e42529b5ae21a220deeb07c3',
    'research/round33/reverse/ba1/report.md': 'a986c205542376c2ad5058cdf88e082abe9c12eeba87b052abf3ad9cefebbb86',
    'research/round33/reverse/ba2/report.md': 'b6615292a7c1f418d567cd17b989605634b2610fc8b1fe30c313d4a3a6cb1ff4',
    'research/round33/skeptic/ba1.md': '4f0364a9acbf031547b7d1765687695e15f296d72c230bdea79ce94bd9fa10f8',
    'research/round33/skeptic/ba2.md': '2ee93777b29c64a5c793599ffead5cbfb20d8c5406ad24e414b459dfb712c98a',
    'research/round33/sources/nachtergaele-sims-1410.8174v1.md': '6a28f4cd6aa2c55286fa839d83c00356ff0709f8b02027ee5b39050df1d6c921',
}
OBSERVED_FORWARD_EQUALS_REVERSE = True
ISOLATION_FORBIDDEN_PREFIXES = (
    'research/round33/forward/bb1/', 'research/round33/reverse/bb1/', 'research/round33/forward/bb2/',
    'research/round33/advisor/bb1-gate.json', 'research/round33/skeptic/bb1', 'research/round33/skeptic/triage',
    'research/round33/skeptic/recommendation', 'research/round33/skeptic/prospective-controls',
    'research/round33/skeptic/loop2-review', 'research/round33/skeptic/bb-contract-review', 'research/round33/experts/',
    'research/round33/advisor/deliberation', 'research/round33/advisor/plan.json', 'research/round33/advisor/panel',
)

MODEL_ID = 'AQ_patterned_zero_selected'
E = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
R_COVER = [(0, 0, 0), (0, 0, 1)]
CLOCK = 'theta=alpha*t/hbar (s=alpha*t_E/hbar Euclidean); u=theta/8=delta*t/hbar internally, delta=alpha/8'
METRIC_STATES = 'coarse l-infinity on factor sites (star diameter 1)'
METRIC_DYNAMICS = 'l1 on the coarse factor lattice, F(r)=(1+r)^-4'
WEIGHTS = 'BB1 frozen targets at q=1/64 as hypotheses; BA2 admitted dynamics constants'
FAMILIES = ['F1: AQ1 centered whole-star boxes on Lambda_N', 'F2: I1 section 6 all-contained-face boxes with padding on Lambda_N']
TOPOLOGY = {'states': 'trace norm on B(H_Y)', 'dynamics': 'operator norm uniformly for |theta| at most 8, per fixed local A',
            'representations': 'GNS strong'}
UNIFORM_IN = 'N (volume) at fixed spacing'
RATE_UNIT = 'per coarse step at fixed spacing (a coarse step is (4a,2a,a)); not a length scale'
SUB_LABELS = ['convergence_of_named_constructions', 'common_limit_of_named_constructions']
STATE_TIERS = ('exact_first_order', 'crude_majorant')
ASSEMBLY_OF_ROUTE = {'forward': 'nested_telescoping', 'reverse': 'union_comparison'}
DYN_ROUTES = ('duhamel_inner_f1', 'duhamel_inner_f2')
BB1_ROUTES = ('polymer_kp', 'iterated_split')
LIMIT_NAME = 'the limit of the named constructions'
CUTOFF_ORDER = 'each Q_L uniformly in L; then L to infinity at fixed N (AV1 F20-F23; F2 via the AY1 itemization); then N to infinity'
CENTERING = 'complex mean |omega(A)|^2'
AQ_INHERITED = {
    'aq1': ['stationarity under T_theta', 'strong continuity of the GNS evolution', 'nonnegative generator'],
    'f2_ba2_rerun': ['stationarity under T_theta', 'strong continuity of the GNS evolution', 'nonnegative generator'],
    'aq2': 'H_phys at least (alpha/16)(I-P_Omega) with a simple vacuum on the invariant-local cyclic completion',
    'aq2_full_gns': 'only as qualified in the AQ2 gate (uses AM2 full-Hilbert finite gap)',
}
COMPARISONS = ('c1_F1_nested', 'c2_F2_nested', 'c3_F1_vs_F2_same_N', 'c4_centered_any_two', 'c5_one_prescription_volumes')

# mirror of research/round33/tools/phrase_scan.py (sha256 above), reimplemented so that this program depends on
# no repository module, plus the skeptic's extra list for this loop
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state', 'uniquely determines the ground state',
    'the thermodynamic limit', 'correlation length',
]
EXTRA_FORBIDDEN = ['uniform in the lattice spacing', 'exponential decay in N', 'equality of GNS dynamics', 'uniform in time',
                   'unconditionally']
NEGATION = re.compile(r"\b(not|never|no|nor|neither|without|excludes?|excluded|exclusion|forbidden|"
                      r"cannot|does not|is not|are not|nothing|none)\b", re.I)
PLACEHOLDER = re.compile(r'<(?![=<>])([^<>=]*)(?<![-=|])>(?!=)')  # mirror of freezer rule R1


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


def rup(x, den=10 ** 30):
    n = x * den
    fl = n.numerator // n.denominator
    return F(fl if fl == n else fl + 1, den)


# ---------------------------------------------------------------- exact exponential enclosure
def exp_enclosure(x, n=30):
    """[lo, hi] for e^x with 0 <= x <= 1: Taylor sum to order n plus the geometric remainder bound."""
    if not (F(0) <= x <= 1):
        raise CheckFailure('exp enclosure domain')
    s, t = F(0), F(1)
    for k in range(n + 1):
        s += t
        t = t * x / (k + 1)
    return s, s + t * F(n + 2) / (F(n + 2) - x)


def e_region_hi(ysize):
    """Directed upper bound of e^{|Y|/10^8} (the frozen region factor)."""
    return exp_enclosure(F(ysize, 10 ** 8))[1]


# ---------------------------------------------------------------- BB2 constants as functions of the hypotheses
def cprime(assembly, ch, q):
    """Item-1 R constant C' as a function of the BB1 R-form constant (nondecreasing: coefficient >= 1)."""
    if assembly == 'nested_telescoping':
        return ch / (1 - q)
    if assembly == 'union_comparison':
        return ch
    raise CheckFailure('assembly')


def csite_prime(assembly, csite, q):
    """Item-1 region constant c'_site as a function of the BB1 region constant (same factor as C')."""
    return cprime(assembly, csite, q)


def item5_terms(n, cdyn, csp, cp, q):
    r = (n - 1) // 2
    lam = (2 * r + 1) ** 3
    dyn = cdyn / (r - 1)
    state = csp * lam * e_region_hi(lam) * q ** (n - r)
    mean = 2 * cp * q ** (n - 1)
    return {'N': n, 'r_N': r, 'Lambda_r_sites': lam, 'dynamics': dyn, 'state': state, 'mean': mean,
            'sum': dyn + state + mean}


# ---------------------------------------------------------------- lattice geometry (fine coordinates)
def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def sub(a, b):
    return tuple(i - j for i, j in zip(a, b))


def pi_map(p):
    return (p[0] // 4, p[1] // 2, p[2])  # Euclidean (floor) division, valid for negative coordinates


def dinf(a):
    return max(abs(i) for i in a)


def face_list(b):
    out = []
    for r, s in product(range(4), range(2)):
        p = (4 * b[0] + r, 2 * b[1] + s, b[2])
        for a, c in ORIENT:
            out.append((p, a, c))
    return out


def owner_type(p, a, c):
    anchor = pi_map(p)
    owners = {pi_map(p), pi_map(add(p, E[a])), pi_map(add(p, E[c]))}
    return tuple(sorted(sub(o, anchor) for o in owners))


def type_histogram(b, shift=(0, 0, 0)):
    """Relative owner types of the 24 faces of anchor b after a fine translation by `shift`."""
    hist = {}
    for p, a, c in face_list(b):
        t = owner_type(add(p, shift), a, c)
        hist[t] = hist.get(t, 0) + 1
    return hist


def classes_preserved(shift, anchors):
    """Face-by-face: the owner type of every face equals that of its translate (the per-anchor histogram is blind)."""
    for b in anchors:
        for p, a, c in face_list(b):
            if owner_type(p, a, c) != owner_type(add(p, shift), a, c):
                return False
    return True


def block_points(b):
    return {(4 * b[0] + r, 2 * b[1] + s, b[2]) for r in range(4) for s in range(2)}


def maps_blocks_to_blocks(shift, anchors):
    for b in anchors:
        img = {add(p, shift) for p in block_points(b)}
        if len({pi_map(p) for p in img}) != 1:
            return False
        if img != block_points(pi_map(next(iter(img)))):
            return False
    return True


def box(n, centre=(0, 0, 0)):
    return {add(centre, v) for v in product(range(-n, n + 1), repeat=3)}


# ---------------------------------------------------------------- Gaussian rationals (centering fixture)
def gmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gconj(a):
    return (a[0], -a[1])


def gabs2(a):
    return a[0] * a[0] + a[1] * a[1]


def gtrace_prod(rho, a):
    """Tr(rho A) for 2x2 Gaussian-rational matrices."""
    tot = (F(0), F(0))
    for i in range(2):
        for k in range(2):
            t = gmul(rho[i][k], a[k][i])
            tot = (tot[0] + t[0], tot[1] + t[1])
    return tot


def gadjoint(a):
    return [[gconj(a[j][i]) for j in range(2)] for i in range(2)]


def gmatmul(a, b):
    out = [[(F(0), F(0)), (F(0), F(0))], [(F(0), F(0)), (F(0), F(0))]]
    for i in range(2):
        for j in range(2):
            s = (F(0), F(0))
            for k in range(2):
                t = gmul(a[i][k], b[k][j])
                s = (s[0] + t[0], s[1] + t[1])
            out[i][j] = s
    return out


# ---------------------------------------------------------------- phrase scan and placeholders
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


def numbers(value):
    if isinstance(value, (int, float, F)) and not isinstance(value, bool):
        yield value
    elif isinstance(value, dict):
        for k in sorted(value):
            yield from numbers(value[k])
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from numbers(v)


def packet_digest(pk):
    body = json.dumps({'inputs': sorted(pk['inputs']), 'controls': pk['controls']}, sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()


# ---------------------------------------------------------------- discharge engine (BB2 post-review protocol)
def dominated(entry, form, hyp):
    """True when an admitted BB1 bound implies the hypothesis bound pointwise for every N >= 2 and Y."""
    if entry is None:
        return False
    shp = entry['shape']
    want = hyp['shape'][form]
    return (shp['q'] <= want['q'] and shp['exponent_shift'] >= 0 and shp['Y_power'] <= want['Y_power']
            and shp['Y_exp_rate'] <= want['Y_exp_rate'] and entry['c'] <= hyp['const'][form])


def discharge(record, hyp, cutoff_routes=('forward',)):
    """Map a BB1 gate outcome to BB2 items: status per item, discharging routes and re-evaluated constants."""
    q = hyp['q']
    items = {k: None for k in ('1', '2', '3', '4', '5')}
    per_sign = {}
    reeval = {}
    for sign in ('+', '-'):
        st = {}
        if record['verdict'] == 'insufficient' or sign not in record['signs']:
            per_sign[sign] = {'1': 'conditional', '2': 'conditional', '3': 'conditional', '4': 'conditional',
                              '5': 'conditional', 'routes': {}}
            continue

        def ok(comp, form, route):
            entry = (record['admitted'].get(comp) or {}).get(form)
            regime = 'untruncated' in record['regimes'] or ('Q_L' in record['regimes'] and route in cutoff_routes)
            return regime and dominated(entry, form, hyp)

        routes = {}
        for fam, nested in (('F1', 'c1_F1_nested'), ('F2', 'c2_F2_nested')):
            for form in ('R', 'Y'):
                rts = []
                if ok(nested, form, 'forward'):
                    rts.append('forward')
                    val = csite_prime('nested_telescoping', record['admitted'][nested][form]['c'], q)
                    reeval[(fam, form, 'forward')] = max(val, reeval.get((fam, form, 'forward'), F(0)))
                if ok('c4_centered_any_two', form, 'reverse'):
                    rts.append('reverse')
                    val = record['admitted']['c4_centered_any_two'][form]['c']
                    reeval[(fam, form, 'reverse')] = max(val, reeval.get((fam, form, 'reverse'), F(0)))
                routes[(fam, form)] = rts
        i1 = {form: bool(routes[('F1', form)]) and bool(routes[('F2', form)]) for form in ('R', 'Y')}
        c3 = {form: ok('c3_F1_vs_F2_same_N', form, 'forward') or ok('c3_F1_vs_F2_same_N', form, 'reverse')
              for form in ('R', 'Y')}
        c5 = {form: ok('c5_one_prescription_volumes', form, 'forward') or ok('c5_one_prescription_volumes', form, 'reverse')
              for form in ('R', 'Y')}
        st['1'] = 'full' if i1['R'] and i1['Y'] else ('R_only' if i1['R'] else 'conditional')
        st['2'] = 'full' if i1['R'] and i1['Y'] and c3['R'] and c3['Y'] else (
            'R_only' if i1['R'] and c3['R'] else 'conditional')
        if st['2'] == 'full':
            st['3'] = 'full'
        elif st['1'] == 'full':
            st['3'] = 'per_family'  # each family's limit equals its own subsequential limits; no common limit
        else:
            st['3'] = 'R_marginals' if i1['R'] else 'conditional'
        st['4'] = 'full' if c5['R'] and c5['Y'] and st['1'] == 'full' else (
            'R_translate_covariance' if c5['R'] and i1['R'] else 'dropped')
        st['5'] = 'full' if st['2'] == 'full' else ('per_family' if st['1'] == 'full' else 'dropped')
        st['routes'] = {'%s_%s' % k: v for k, v in sorted(routes.items())}
        per_sign[sign] = st
    rank = {'full': 3, 'R_only': 2, 'R_marginals': 2, 'R_translate_covariance': 2, 'per_family': 2, 'dropped': 1,
            'conditional': 0}
    for k in items:
        vals = [per_sign[s][k] for s in ('+', '-')]
        items[k] = min(vals, key=lambda v: rank[v])
    if record['verdict'] == 'insufficient' or all(per_sign[s]['1'] == 'conditional' for s in ('+', '-')):
        verdict = 'insufficient'
    elif all(items[k] == 'full' for k in items):
        verdict = 'accepted_within_scope'
    else:
        verdict = 'limited'
    gf = {
        'whole_sequence_claimed': items['1'] == 'full', 'common_limit_claimed': items['2'] == 'full',
        'state_convergence_claimed': items['1'] == 'full', 'translation_invariance_claimed': items['4'] == 'full',
        'rate_in_N_claimed': items['1'] in ('full', 'R_only'),
        'dynamics_level': 'correlation_functions_compact_window' if items['5'] == 'full' else None,
        'uniqueness_of_ground_state_claimed': False, 'rate_in_a_claimed': False, 'continuum_claim': False,
        'gns_dynamics_equality_claimed': False, 'uniform_in_time_claimed': False, 'weak_coupling_claim': False,
        'scientific_priority_verified': False,
    }
    return {'items': items, 'verdict': verdict, 'gate_fields': gf,
            'items_by_sign': {s: {k: per_sign[s][k] for k in ('1', '2', '3', '4', '5')} for s in ('+', '-')},
            'reevaluated': {'%s_%s_%s' % k: v for k, v in sorted(reeval.items())},
            'routes_plus': per_sign['+'].get('routes', {}), 'unconditional': verdict == 'accepted_within_scope'}


def validate_discharge_claim(claim, record, hyp):
    """The BB2 skeptic post-review record: the BB1 gate sha256, item-by-item discharge and re-evaluated constants."""
    if not re.fullmatch(r'[0-9a-f]{64}', claim.get('bb1_gate_sha256') or ''):
        raise Rejected('conditional on bb1 targets: bb1 gate sha256 not recorded')
    truth = discharge(record, hyp)
    for k in ('1', '2', '3', '4', '5'):
        if claim['items'][k] != truth['items'][k]:
            raise Rejected('conditional on bb1 targets: undischarged item claimed (item %s)' % k)
    if claim['verdict'] != truth['verdict']:
        raise Rejected('conditional on bb1 targets: verdict')
    if claim['unconditional'] != truth['unconditional']:
        raise Rejected('conditional on bb1 targets: unconditional before discharge')
    for key, want in truth['gate_fields'].items():
        if claim['gate_fields'].get(key) != want:
            raise Rejected('conditional on bb1 targets: gate field ' + key)
    if claim['reevaluated'] != truth['reevaluated']:
        raise Rejected('conditional on bb1 targets: re-evaluation at admitted values')
    if truth['verdict'] != 'accepted_within_scope' and not claim.get('retained_conditional'):
        raise Rejected('conditional on bb1 targets: conditional statements not retained')
    return True


# ---------------------------------------------------------------- packet validator
def validate(pk, c):
    # provenance and coherent tampering
    if pk['contract_sha256'] != CONTRACT_SHA256:
        raise Rejected('contract hash')
    if pk['bb1_contract_sha256'] != BB1_CONTRACT_SHA256:
        raise Rejected('bb1 contract hash')
    if pk['freeze_digest'] != packet_digest(pk):
        raise Rejected('coherent evidence tampering: freeze digest')
    if sorted(pk['inputs']) != sorted(c['declared_inputs']):
        extra = sorted(set(pk['inputs']) - set(c['declared_inputs']))
        if any(p.startswith(pre) for p in extra for pre in ('research/round33/forward/bb1/', 'research/round33/reverse/bb1/',
                                                            'research/round33/advisor/bb1-gate', 'research/round33/skeptic/bb1')):
            raise Rejected('conditional on bb1 targets: BB1 production file read')
        if any(p.startswith(pre) for p in extra for pre in ISOLATION_FORBIDDEN_PREFIXES):
            raise Rejected('reverse premise isolation')
        raise Rejected('coherent evidence tampering: snapshot inventory')
    if sorted(pk['controls']) != sorted(c['control_ids']) or any(pk['controls'][k] is not True for k in pk['controls']):
        raise Rejected('coherent evidence tampering: control booleans')
    if any(isinstance(v, float) for v in numbers(pk)):
        raise Rejected('exact arithmetic')
    # model
    if (pk['model_id'] != MODEL_ID or pk['triple'] != ['0', '0', '0'] or pk['group'] != 'SU(2)'
            or pk['lattice'] != 'Z^3 coarse 24-link factors' or pk['model_is_finite_graph'] is not False):
        raise Rejected('changed model relabelled')
    if pk['tau_abs'] != c['tau'] or sorted(pk['signs']) != ['+', '-'] or pk['cover'] != R_COVER:
        raise Rejected('changed model relabelled: coupling or cover')
    if pk['same_coupling'] is not True or pk['compared_couplings'] != ['same tau'] or pk['clock_per_family'] != [CLOCK, CLOCK]:
        raise Rejected('common clock')
    if pk['families'] != FAMILIES or pk['N_min'] != 2:
        raise Rejected('two families not named')
    par = pk['parameters']
    for key in ('metric_states', 'metric_dynamics', 'weights', 'window', 'clock', 'N_min'):
        if key not in par:
            raise Rejected('parameters must declare metric weights window: ' + key)
    if par['metric_states'] != METRIC_STATES or par['metric_dynamics'] != METRIC_DYNAMICS:
        raise Rejected('changed model relabelled: metric')
    if par['weights'] != WEIGHTS:
        raise Rejected('parameters must declare metric weights window: weights')
    if pk['topology'] != TOPOLOGY:
        raise Rejected('topology named')
    # rate-constant pair and hypotheses (conditional_on_bb1_targets)
    hy = pk['hypotheses']
    if hy['q'] != c['q'] or pk['targets'] != c['targets'] or pk.get('q_per_N') is not False or pk['rate_reported'] != 'q=1/64 frozen':
        raise Rejected('rate constant pair prefrozen')
    if hy['source'] != 'bb1_frozen_targets' or hy['C_h'] != c['C_h'] or hy['c_h'] != c['c_h'] \
            or hy['C_2h'] != c['C_2h'] or hy['c_2h'] != c['c_2h']:
        raise Rejected('conditional on bb1 targets: BB1 value other than the frozen targets')
    if hy['comparisons'] != list(COMPARISONS) or hy['forms'] != ['R', 'Y'] or hy['regimes'] != ['Q_L', 'untruncated'] \
            or hy['signs'] != ['+', '-']:
        raise Rejected('conditional on bb1 targets: hypothesis scope narrowed')
    cond = pk['conditional']
    if cond['label'] != 'conditional_on_bb1_targets' or cond['unconditional_claimed'] is not False:
        raise Rejected('conditional on bb1 targets: condition dropped or unconditional before discharge')
    # item 1
    i1 = pk['item1']
    if i1['quantifier'] == 'N to N+1':
        raise Rejected('subsequence versus whole sequence: N to N+1 bound is not a Cauchy estimate')
    if i1['quantifier'] != 'all M greater than N':
        raise Rejected('subsequence versus whole sequence')
    if i1['limit_kind'] != 'whole sequence' or i1['whole_sequence_via'] != 'Cauchy bound over all M greater than N':
        raise Rejected('subsequence versus whole sequence')
    if i1['limit_existence'] != 'Cauchy bound and completeness of the trace class':
        raise Rejected('cauchy estimate not compactness')
    if i1['assembly'] not in ASSEMBLY_OF_ROUTE.values() or i1['tier'] not in STATE_TIERS \
            or i1['hypothesis_source'] != 'bb1_frozen_targets' or i1.get('bb1_route') is not None:
        raise Rejected('tier mixing: state constant labels')
    if i1['assembly'] != ASSEMBLY_OF_ROUTE[pk['route']]:
        raise Rejected('tier mixing: assembly of the route')
    if i1['combine'] != 'linear':
        raise Rejected('root-N misuse')
    fn = i1['function']  # C' = aR*C_h + aY*c_h ; c'_site = bR*C_h + bY*c_h
    if min(fn['C_prime']) < 0 or min(fn['c_site_prime']) < 0 or fn['monotone_checked'] is not True:
        raise Rejected('conditional on bb1 targets: constant decreases when a hypothesis constant increases')
    cp = fn['C_prime'][0] * hy['C_h'] + fn['C_prime'][1] * hy['c_h']
    csp = fn['c_site_prime'][0] * hy['C_h'] + fn['c_site_prime'][1] * hy['c_h']
    if cp != i1['C_prime'] or csp != i1['c_site_prime']:
        raise Rejected('coherent evidence tampering: constant is not its stated function')
    if cp < c['C_min'][i1['assembly']] or csp < c['c_min'][i1['assembly']]:
        raise Rejected('coherent evidence tampering: constant below the derivable value')
    if i1['region_factor'] != '|Y| e^{|Y|/10^8} q^{d_Y}' or i1['d_Y'] != 'N - max_{y in Y}|y|_inf':
        raise Rejected('region constant scales with Y')
    if pk['cutoff']['order'] != CUTOFF_ORDER or pk['cutoff']['uniform_in_L'] is not True \
            or pk['cutoff']['vector_removal'] is not True:
        raise Rejected('cutoff uniform then removed')
    # item 2
    i2 = pk['item2']
    if i2['via'] != ['c3_F1_vs_F2_same_N', 'item1'] or i2['scope'] != 'every finite region' or i2['name'] != LIMIT_NAME:
        raise Rejected('named construction not uniqueness: common limit')
    # item 3
    i3 = pk['item3']
    if i3['identified_before_inheritance'] is not True or i3['identified_with'] != ['every AQ1 subsequential limit',
                                                                                   'every F2 subsequential limit']:
        raise Rejected('limit identified with aq1 limits')
    if i3['inherited'] != AQ_INHERITED:
        raise Rejected('limit identified with aq1 limits: inherited scope')
    # item 4
    i4 = pk['item4']
    if i4['separate_item'] is not True or i4['from_nested_cubes_only'] is not False:
        raise Rejected('translation invariance separate item')
    if i4['input'] != 'BB1 general-volume comparison of reduced densities (c5), direct':
        raise Rejected('translation invariance separate item: input')
    if i4['translations'] != 'coarse: fine (4v_x,2v_y,v_z)' or i4['noncoarse_accepted'] is not False:
        raise Rejected('fixture translation residues')
    if i4['via_box'] != 'Lambda_{N-|v|_inf}' or i4['bound'] != 'C_h q^(N-|v|_inf-1)' or i4['N_condition'] != 'N >= |v|_inf+2':
        raise Rejected('translation invariance separate item: bound')
    if i4['union_two_step'] is not None and (i4['union_two_step'].get('labelled') is not True
                                            or i4['union_two_step'].get('factor') != '1+q^|v|_inf'):
        raise Rejected('union two-step labelled only')
    # item 5
    i5 = pk['item5']
    if i5['N_min'] != 5 or i5['r_N'] != 'floor((N-1)/2)' or i5['r_N_post_hoc'] is not False:
        raise Rejected('r_N prefrozen')
    if i5['centering'] != CENTERING:
        raise Rejected('fixture correlation centering')
    if i5['combine'] != 'linear':
        raise Rejected('root-N misuse')
    if i5['rate'] != 'O(1/N)' or i5['exponential_claimed'] is not False:
        raise Rejected('lieb-robinson polynomial tail')
    if i5['window'] != '|theta| at most 8' or i5['U'] != 1 or i5['u_over_theta'] != F(1, 8):
        raise Rejected('wrong delta alpha hbar clock: window')
    if pk['clock'] != CLOCK or par['clock'] != CLOCK:
        raise Rejected('wrong delta alpha hbar clock')
    if i5['uniform_in_time_claimed'] is not False:
        raise Rejected('time window named: uniform in time')
    if i5['gns_dynamics_equality_claimed'] is not False or i5['dynamics_level'] != 'correlation_functions_compact_window':
        raise Rejected('algebraic not gns dynamics')
    if i5['state_constant'] != 'c_site_prime on Lambda_{r_N}, exponent N-r_N' or i5['mean_constant'] != '2 C_prime q^(N-1)':
        raise Rejected('region constant scales with Y: item 5')
    if i5['lumped_bracket'] is not None:
        raise Rejected('tier mixing: lumped item-5 bracket')
    comps, gate_vals = i5['C_dyn_components'], c['ba2']
    routes = set()
    fam_sum = {}
    for fam in ('F1', 'F2'):
        tot = F(0)
        for mult, key in comps[fam]:
            if key not in gate_vals:
                raise Rejected('tier mixing: dynamics constant not a BA2 gate value')
            tot += mult * gate_vals[key]['value']
            routes.add(gate_vals[key]['route'])
        fam_sum[fam] = tot
    cdyn = max(fam_sum.values())
    if i5['C_dyn'] != cdyn:
        raise Rejected('coherent evidence tampering: C_dyn is not its BA2 assembly')
    if cdyn < c['C_dyn_min']:
        raise Rejected('coherent evidence tampering: constant below the derivable value')
    if i5['C_dyn_tier'] != 'polynomial_lieb_robinson':
        raise Rejected('tier mixing: dynamics tier')
    if len(routes) == 1:
        if i5['C_dyn_route'] != next(iter(routes)):
            raise Rejected('tier mixing: dynamics route')
    elif i5['C_dyn_route'] != 'composite' or i5.get('component_routes_listed') is not True:
        raise Rejected('tier mixing: mixed-route composite labelled as one route')
    # scaling
    br = pk['brackets']
    if br != c['brackets']:
        raise Rejected('tau scaling: bracket changed')
    sc = pk['scaling']
    if sc['C_prime'] != 1 or sc['c_site_prime'] != 1 or sc['q_secondary'] != 100:
        raise Rejected('tau scaling exponent')
    if not (F(9500) <= sc['C_dyn'] <= F(10500)) or not (F(99, 100) <= sc['secondary'] <= F(101, 100)):
        raise Rejected('tau scaling exponent')
    # targets, verdict
    sec = pk['secondary']
    if sec['labelled'] is not True or sec['conditional_on'] != 'BB1 secondary pair':
        raise Rejected('rate constant pair prefrozen: secondary')
    met = {'C_prime': cp <= c['targets']['C_prime'], 'c_site_prime': csp <= c['targets']['c_site_prime'],
           'C_dyn': cdyn <= c['targets']['C_dyn']}
    if pk['targets_met'] != met:
        raise Rejected('insufficient verdict retained: targets_met inconsistent')
    if pk['verdict'] == 'accepted_within_scope' and not all(met.values()):
        raise Rejected('insufficient verdict retained')
    if pk['verdict'] != 'accepted_within_scope' and not pk.get('dominating_term'):
        raise Rejected('insufficient verdict retained: dominating term')
    if pk['retuned'] is not False:
        raise Rejected('insufficient verdict retained: retuned')
    # fixtures
    fx = pk['fixtures']
    if fx['alternating_ball_sequence'] != 'rejected as convergence' or fx['n_to_n_plus_1_only'] != 'rejected as Cauchy':
        raise Rejected('fixture whole sequence vs subsequence')
    if fx['fine_translation_1_0_0'] != 'rejected: residues and face classes broken':
        raise Rejected('fixture translation residues')
    if fx['centering'] != 'complex mean; omega(A)^2 and (Re omega(A))^2 rejected':
        raise Rejected('fixture correlation centering')
    if fx['fixed_vs_moving_vector'] is not True:
        raise Rejected('topology named: fixture')
    # wording
    if pk['uniform_in'] != UNIFORM_IN:
        raise Rejected('uniform in N not in a')
    if pk['rate_unit'] != RATE_UNIT:
        raise Rejected('decay rate in N not a')
    if pk['sub_labels'] != SUB_LABELS:
        raise Rejected('changed model relabelled: sub-label')
    for text in strings([pk['statements'], pk['sentence']]):
        if placeholder_spans(text):
            raise Rejected('placeholder span')
    for text in pk['statements']:
        hits = affirmative_hits(text, c['forbidden'], c['sentence'])
        if hits:
            if any(h in ('uniform in a', 'uniform in the lattice spacing') for h in hits):
                raise Rejected('uniform in N not in a: forbidden phrasing')
            if any('unique' in h or 'infinite-volume' in h or 'thermodynamic' in h for h in hits):
                raise Rejected('named construction not uniqueness: forbidden phrasing ' + hits[0])
            raise Rejected('forbidden phrasing: ' + hits[0])
    if pk['sentence'] != c['sentence'] or pk['sentence_count'] != 1:
        raise Rejected('mandatory sentence template')
    gf = pk['gate_fields']
    for key in sorted(c['gate_fields']):
        if key not in gf:
            raise Rejected('gate fields: missing ' + key)
    if pk['gate_fields_status'] != 'conditional_on_bb1_discharge':
        raise Rejected('conditional on bb1 targets: gate fields exported as unconditional')
    for key, want in sorted(c['gate_fields'].items()):
        if gf[key] != want:
            if key == 'uniqueness_of_ground_state_claimed':
                raise Rejected('named construction not uniqueness: ' + key)
            if key == 'gns_dynamics_equality_claimed':
                raise Rejected('algebraic not gns dynamics: ' + key)
            if key == 'rate_in_a_claimed':
                raise Rejected('decay rate in N not a')
            if key == 'uniform_in_time_claimed':
                raise Rejected('time window named: uniform in time')
            raise Rejected('gate field: ' + key)
    for key in ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified', 'uniform_in_a_claimed'):
        if pk['claims'].get(key) is not False:
            raise Rejected('forbidden claim ' + key)
    for name in c['error_terms']:
        entry = pk['error_terms'].get(name)
        if entry is None:
            raise Rejected('error term missing: ' + name)
        if entry.startswith('not_applicable') and len(entry) <= len('not_applicable') + 3:
            raise Rejected('error term missing: not_applicable without a reason (' + name + ')')
    return True


# ---------------------------------------------------------------- execute
def execute():
    # 1. provenance -------------------------------------------------------------------------------------------------
    cb = (ROOT / CONTRACT_REL).read_bytes()
    c_sha = hashlib.sha256(cb).hexdigest()
    need(c_sha == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=c_sha)
    con = json.loads(cb)
    b1b = (ROOT / BB1_CONTRACT_REL).read_bytes()
    b1_sha = hashlib.sha256(b1b).hexdigest()
    need(b1_sha == BB1_CONTRACT_SHA256, 'bb1_contract_sha256_pinned', sha256=b1_sha)
    bb1 = json.loads(b1b)
    par, pre = con['parameters'], con['preregistration']
    need(con['status'] == 'frozen_before_production' and bb1['status'] == 'frozen_before_production'
         and bb1['frozen_at'] < con['frozen_at'] and con['id'] == 'BB2' and con['direction'] == 'paired'
         and con['reverse_premise_isolation'] is True,
         'contracts_frozen_bb1_first', bb1_frozen_at=bb1['frozen_at'], bb2_frozen_at=con['frozen_at'])
    for rel, want in sorted(GATES.items()):
        got = sha(rel)
        if got != want:
            raise CheckFailure('gate hash ' + rel)
    need(True, 'admitted_gates_pinned', gates=sorted(GATES))

    # 2. the skeptic's pre-freeze edits against the frozen bytes -----------------------------------------------------
    need(sha(REVIEW_REL) == REVIEW_SHA256, 'bb_contract_review_pinned')
    review = json.loads((ROOT / REVIEW_REL).read_text())

    def get(obj, path):
        cur = obj
        for tok in re.findall(r'[^.\[\]]+|\[\d+\]', path[2:]):
            cur = cur[int(tok[1:-1])] if tok.startswith('[') else cur[tok]
        return cur

    applied = {}
    for loop, doc in (('bb2', con), ('bb1', bb1)):
        rows = []
        for kind in ('blocking', 'non_blocking'):
            for e in review[loop][kind]:
                if not e['path'].startswith('$'):
                    rows.append((kind, e['path'], 'no field'))
                    continue
                rows.append((kind, e['path'], 'verbatim' if get(doc, e['path']) == e['replacement'] else 'DIFFERENT'))
        applied[loop] = rows
    bad = [r for loop in applied for r in applied[loop] if r[2] == 'DIFFERENT']
    n_blocking = {loop: sum(1 for r in applied[loop] if r[0] == 'blocking') for loop in applied}
    need(not bad and n_blocking == {'bb2': 15, 'bb1': 7}, 'prefreeze_edits_applied_verbatim',
         bb2_field_edits=[r[1] for r in applied['bb2'] if r[2] == 'verbatim'],
         bb1_field_edits=len([r for r in applied['bb1'] if r[2] == 'verbatim']),
         not_field_edits=[r[1] for loop in applied for r in applied[loop] if r[2] == 'no field'])

    # 3. controls, semantics, premises, inputs ---------------------------------------------------------------------
    control_ids = list(con['controls'])
    need(control_ids == list(pre['controls_required']['ids']) and len(control_ids) == 34
         and len(set(control_ids)) == 34, 'control_mirror', controls=len(control_ids))
    earlier = {}
    for p_ in sorted((ROOT / 'research').glob('round*/contracts/*.json')):
        rel = p_.relative_to(ROOT).as_posix()
        if rel.startswith('research/round33/') and rel not in EARLIER_ROUND33_CONTRACTS:
            continue
        if int(re.match(r'research/round(\d+)/', rel).group(1)) > 33:
            continue
        try:
            d_ = json.loads(p_.read_text())
        except ValueError:
            continue
        for k in (d_.get('new_control_semantics') or {}):
            earlier.setdefault(k, rel)
    sem = con['new_control_semantics']
    own = [k for k in control_ids if k in sem]
    inherited = {k: earlier[k] for k in control_ids if k not in sem and k in earlier}
    undefined = [k for k in control_ids if k not in sem and k not in earlier]
    need(not undefined and len(own) == 15 and len(inherited) == 19 and all(k in control_ids for k in sem),
         'control_semantics_coverage', own=len(own), inherited=len(inherited),
         inherited_from=sorted(set(inherited.values())),
         reading='inherited texts written for BA2/BB1 (rate_constant_pair_prefrozen names BB1 proof weights; '
                 'parameters_declare_metric_weights_window names w=e^mu, e^beta) are read by name for BB2 (defect D6)')
    premises = list(con['shared_premises'])
    need(all((ROOT / p_).exists() for p_ in premises) and len(premises) == 36 and len(set(premises)) == 36
         and BB1_CONTRACT_REL in premises and 'research/round29/advisor/aq2-gate.json' in premises,
         'premises_exist', count=len(premises))
    declared_inputs = sorted(['AGENTS.md', CONTRACT_REL] + premises)
    obs_ok = sorted(OBSERVED_INPUTS) == declared_inputs and OBSERVED_FORWARD_EQUALS_REVERSE
    obs_ok = obs_ok and all(sha(p_) == h for p_, h in OBSERVED_INPUTS.items())
    obs_ok = obs_ok and OBSERVED_INPUTS[BB1_CONTRACT_REL] == BB1_CONTRACT_SHA256 and OBSERVED_INPUTS[CONTRACT_REL] == CONTRACT_SHA256
    obs_ok = obs_ok and not any(p_.startswith(pre_) for p_ in OBSERVED_INPUTS for pre_ in ISOLATION_FORBIDDEN_PREFIXES)
    need(obs_ok, 'producer_inputs_recorded_isolated', count=len(OBSERVED_INPUTS),
         note='both producers: the same 38 paths, byte-identical to the repository; the only skeptic files are ba1.md '
              'and ba2.md; no BB1 producer, skeptic or gate file; no triage, plan, deliberation, lens file or proposal')
    vocab = PLAN_RECORD
    gfr = dict(pre['gate_fields_required'])
    need(all(k in vocab['gate_fields'] for k in gfr) and set(pre['sub_labels_allowed']) <= set(vocab['sub_labels_allowed'])
         and set(pre['tier_names_allowed']) <= set(vocab['tier_names_allowed'])
         and set(vocab['assembly_values']) == {'nested_telescoping', 'union_comparison'},
         'vocabulary_closed_over_plan', gate_fields=len(gfr))
    freeze_events = PLAN_RECORD['history_events_with_plan_sha256_at_freeze']
    need(any('BA1' in h for h in freeze_events), 'plan_history_freeze_records', plan_sha256_recorded=PLAN_RECORD['sha256'],
         ba_freeze_recorded=True, bb_freeze_recorded=any('BB' in h for h in freeze_events),
         defect='at review time no plan-history entry records plan.json sha256 at the BB1/BB2 freeze (P5; defect D8)')

    # 4. hypotheses and targets read from the contracts ----------------------------------------------------------------
    rcp = par['rate_constant_pair']
    m = re.search(r'q=1/64, C_h=(1/\d+) and c_h=(1/\d+); secondary q_2=151552\|tau\|, C_2h=(1/\d+), c_2h=(1/\d+)', rcp['hypotheses'])
    C_h, c_h, C_2h, c_2h = (F(g) for g in m.groups())
    q = F(rcp['headline']['q'])
    tau = F(pre['tau']['value'])
    b1r = bb1['parameters']['rate_constant_pair']
    need(q == F(1, 64) == F(b1r['headline']['q']) == F(b1r['region_form']['q']) and C_h == F(b1r['headline']['C_target'])
         and c_h == F(b1r['region_form']['c_site_target']) and C_2h == F(b1r['secondary']['C_target'])
         and c_2h == F(b1r['secondary']['c_site_target']) and b1r['secondary']['q'].startswith('151552|tau|')
         and tau == F(1, 10 ** 8), 'hypotheses_equal_bb1_frozen_targets',
         C_h=q_(C_h), c_h=q_(c_h), C_2h=q_(C_2h), c_2h=q_(c_2h), q=q_(q))
    tgt = {'C_prime': F(rcp['headline']['C_prime_target']), 'c_site_prime': F(rcp['headline']['c_site_prime_target']),
           'C_dyn': F(rcp['dynamics']['C_dyn_target'])}
    tgt_sec = F(rcp['secondary']['C_prime_target'])
    tv = [F(x.strip()) for x in re.split(r',|and', pre['target']['value'])]
    need(tv == [tgt['C_prime'], tgt['c_site_prime'], tgt['C_dyn']] and tgt_sec == F(1, 8000)
         and tgt == {'C_prime': F(1, 100000), 'c_site_prime': F(1, 200000), 'C_dyn': F(1, 2000000000)},
         'targets_read_from_contract', targets={k: q_(v) for k, v in tgt.items()}, secondary=q_(tgt_sec))
    q2 = 151552 * tau
    need(q2 == F(592, 390625), 'secondary_rate_value', q2=q_(q2))

    # 5. item 1: C', c'_site as functions of the hypotheses -------------------------------------------------------------
    consts = {}
    for asm in ('nested_telescoping', 'union_comparison'):
        consts[asm] = {'C_prime': cprime(asm, C_h, q), 'c_site_prime': csite_prime(asm, c_h, q),
                       'C_prime_2': cprime(asm, C_2h, q2), 'c_site_prime_2': csite_prime(asm, c_2h, q2)}
    tel, uni = consts['nested_telescoping'], consts['union_comparison']
    need(tel['C_prime'] == F(4, 984375) and tel['c_site_prime'] == F(2, 984375) and uni['C_prime'] == C_h
         and uni['c_site_prime'] == c_h and tel['C_prime_2'] == F(625, 12481056) and uni['C_prime_2'] == C_2h,
         'item1_constants_at_hypothesis_values',
         telescoped={k: q_(v) for k, v in tel.items()}, union={k: q_(v) for k, v in uni.items()})
    margins = {asm: {'C_prime': tgt['C_prime'] / consts[asm]['C_prime'], 'c_site_prime': tgt['c_site_prime'] / consts[asm]['c_site_prime'],
                     'C_prime_2': tgt_sec / consts[asm]['C_prime_2']} for asm in consts}
    need(margins['nested_telescoping']['C_prime'] == F(315, 128) == margins['nested_telescoping']['c_site_prime']
         and margins['union_comparison']['C_prime'] == F(5, 2) == margins['union_comparison']['c_site_prime']
         and margins['nested_telescoping']['C_prime_2'] == F(390033, 156250) and margins['union_comparison']['C_prime_2'] == F(5, 2)
         and all(v >= 2 for mm in margins.values() for v in mm.values()),
         'item1_margins', margins={a: {k: q_(v) for k, v in mm.items()} for a, mm in margins.items()})
    grid = [F(0), F(1, 10 ** 9), F(1, 10 ** 6), c_h, C_h, F(1, 100000), F(1, 1000)]
    mono = all(cprime(a, x, q) <= cprime(a, y, q) for a in consts for x in grid for y in grid if x <= y)
    mono = mono and 1 / (1 - q) >= 1 and 1 / (1 - q2) >= 1
    need(mono, 'item1_constants_nondecreasing', statement="C'=C_h/(1-q) or C_h, c'_site=c_h/(1-q) or c_h: linear with "
         "coefficients 64/63 or 1 (>0), independent of the other hypothesis constant; checked exactly on a grid")
    # telescoping over all M > N (exact partial sums against the closed form), region exponent shift
    tel_ok = True
    for n in range(2, 13):
        tail = F(0)
        for mm in range(n + 1, 61):
            tail += C_h * q ** (mm - 2)  # step k=mm-1 -> mm contributes C_h q^(k-1)
            tel_ok = tel_ok and tail <= cprime('nested_telescoping', C_h, q) * q ** (n - 1)
        tel_ok = tel_ok and cprime('nested_telescoping', C_h, q) * q ** (n - 1) - tail == C_h * q ** 59 / (1 - q)
    shift_ok = all((k - max(abs(x) for x in y)) == (n - max(abs(x) for x in y)) + (k - n)
                   for n in range(2, 6) for k in range(n, 9) for y in [(0, 0, 0), (0, 0, 1), (1, -1, 2), (n, 0, 0)])
    need(tel_ok and shift_ok, 'item1_telescoping_sup_over_all_M',
         statement='sum_{k=N}^{M-1} C_h q^(k-1) = C_h q^(N-1)(1-q^(M-N))/(1-q) <= C_h q^(N-1)/(1-q) for every M>N '
                   '(exact partial sums for N<=12, M<=60, the gap to the closed form at M=60 being C_h q^59/(1-q)); '
                   'region steps: Y in Lambda_k gives '
                   'd_Y(k)=d_Y(N)+(k-N), so the same factor 1/(1-q) multiplies c_h|Y|e^{|Y|/10^8}q^{d_Y}')
    # region form at R versus the R form
    reg_at_R = c_h * 2 * e_region_hi(2)
    need(reg_at_R > C_h and reg_at_R - C_h < F(1, 10 ** 13), 'region_form_at_R_is_weaker',
         statement='c_h|R|e^{|R|/10^8} = C_h e^{2/10^8} exceeds C_h by less than 10^-13: the R form is the sharper '
                   'statement on R; a producer may use either, labelled')

    # 6. common limit, identification, AQ2 scope ---------------------------------------------------------------------
    common = [(n, (2 * tel['C_prime'] + C_h) * q ** (n - 1)) for n in range(2, 8)]
    need(all(a[1] > b[1] for a, b in zip(common, common[1:])) and common[0][1] == (2 * tel['C_prime'] + C_h) / 64,
         'item2_common_limit_bound', bound_R='(2C\'+C_h)q^(N-1) -> 0', values={str(n): preview(v) for n, v in common},
         statement='||rho^{F1,inf}_Y-rho^{F2,inf}_Y||_1 <= (2c\'_site+c_h)|Y|e^{|Y|/10^8}q^{d_Y(N)} for every N, hence 0')
    aq1_text = (ROOT / AQ1_REPORT_REL).read_text()
    aq1_gate = json.loads((ROOT / 'research/round29/advisor/aq1-gate.json').read_text())['accepted']
    aq2_gate = json.loads((ROOT / 'research/round29/advisor/aq2-gate.json').read_text())['accepted']
    need('converge in trace norm on every finite F' in aq1_text and 'subsequence' in aq1_gate and 'locally normal' in aq1_gate
         and 'stationary' in aq1_gate and 'nonnegative self-adjoint physical energy generator' in aq1_gate,
         'item3_aq1_limit_topology', statement='AQ1 subsequential limits are trace-norm limits of the F1 box densities on '
         'every finite complete-factor region; a whole-sequence trace-norm limit equals every one of them')
    need('H_phys >= (alpha/16)(I-P_Omega)' in aq2_gate and 'simple vacuum' in aq2_gate
         and 'invariant-local cyclic completion' in aq2_gate and 'full-GNS strengthening explicitly uses AM2' in aq2_gate
         and 'actual AQ1 centered full-Z3 subsequential state' in aq2_gate, 'item3_aq2_scope',
         inherited=AQ_INHERITED['aq2'], full_gns=AQ_INHERITED['aq2_full_gns'])

    # 7. item 4: translations ----------------------------------------------------------------------------------------
    cont_ok = True
    for n in range(2, 6):
        for v in product(range(-2, 3), repeat=3):
            k = dinf(v)
            if k == 0 or n < k + 2:
                continue
            inter = box(n) & box(n, v)
            cont_ok = cont_ok and box(n - k) <= inter and not box(n - k + 1) <= inter
    tr_vals = {'|v|=1,N=3': C_h * q ** 1, '|v|=1,N=5': C_h * q ** 3, '|v|=2,N=4': C_h * q ** 1, '|v|=3,N=10': C_h * q ** 6}
    union_factor = {k_: 1 + q ** k_ for k_ in (1, 2, 3)}
    need(cont_ok and tr_vals['|v|=1,N=3'] == F(1, 16000000) and union_factor[1] == F(65, 64),
         'item4_translation_bound', values={k_: q_(v_) for k_, v_ in tr_vals.items()},
         union_two_step_factor={str(k_): q_(v_) for k_, v_ in union_factor.items()},
         statement='Lambda_{N-|v|} is the largest centered cube inside Lambda_N and Lambda_N+v (enumerated N<=5, |v|<=2); '
                   'the direct BB1 c5 comparison gives C_h q^(N-|v|-1); through the union U=Lambda_N u (Lambda_N+v) the '
                   'bound is C_h q^(N-|v|-1)(1+q^|v|), above the frozen item-4 constant (labelled only)')
    anchors = [b for b in product(range(-2, 3), repeat=3)]
    std = type_histogram((0, 0, 0))
    coarse_ok = all(maps_blocks_to_blocks((4 * a, 2 * b_, c_), anchors[:20]) for a, b_, c_ in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 2, 3)])
    coarse_ok = coarse_ok and all(classes_preserved((4 * a, 2 * b_, c_), anchors) for a, b_, c_ in
                                  [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (-2, 1, 3)])
    coarse_ok = coarse_ok and all(type_histogram(b) == std for b in anchors) and classes_preserved((0, 0, 1), anchors)
    bad_shifts = [(1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0), (1, 1, 0)]
    noncoarse = {str(s_): (maps_blocks_to_blocks(s_, anchors[:5]), classes_preserved(s_, anchors[:5]),
                           type_histogram((0, 0, 0), s_) == std) for s_ in bad_shifts}
    need(coarse_ok and all(v_[:2] == (False, False) for v_ in noncoarse.values())
         and all(v_[2] is True for v_ in noncoarse.values()), 'fixture_translation_residues_exact',
         standard_histogram={' '.join(str(t) for t in k_): v_ for k_, v_ in sorted(std.items())},
         noncoarse={k_: {'blocks_to_blocks': v_[0], 'face_classes_kept_face_by_face': v_[1],
                         'per_anchor_histogram_unchanged': v_[2]} for k_, v_ in sorted(noncoarse.items())},
         statement='coarse translations (4v_x,2v_y,v_z) map factor blocks to blocks and keep the owner type of every '
                   'face; fine (1,0,0),(2,0,0),(3,0,0),(0,1,0),(1,1,0) break both. Pitfall recorded: the per-anchor '
                   '24-face histogram is unchanged by every fine shift (the translated faces of one anchor reassemble '
                   'the same multiset), so a histogram-level residue check accepts non-coarse translations; the '
                   'face-by-face class map is required')

    # 8. item 5: BA2 gate constants, C_dyn assemblies, r_N and the three-term sum -------------------------------------
    ba2 = json.loads((ROOT / 'research/round33/advisor/ba2-gate.json').read_text())['accepted']

    def fwd(L, t):
        return L * t * t / (1 - 338688 * t)

    def eup(y):
        return 1 + y / 3 + y * y / (12 * (1 - y / 5))

    def rev(L, v, t):
        return L * t * t * eup(v * t)

    formulas = {
        'K_cmp_fwd': (lambda t: fwd(254016, t), 'duhamel_inner_f1', '254016 tau^2/(1-338688|tau|)'),
        'K_cmp_rev': (lambda t: rev(148176, 592704, t), 'duhamel_inner_f2', '148176 tau^2 E_up(592704|tau|)'),
        'K_c1_fwd': (lambda t: fwd(592704, t), 'duhamel_inner_f1', '592704 tau^2/(1-338688|tau|) (faces charged once)'),
        'K_c1_rev': (lambda t: rev(1016064, 1016064, t), 'duhamel_inner_f1', '1016064 tau^2 E_up(1016064|tau|) (whole stars)'),
        'K_c2_fwd': (lambda t: fwd(941976, t), 'duhamel_inner_f1', '941976 tau^2/(1-338688|tau|) = K_c1+(11/8)K_cmp'),
        'K_c2_rev': (lambda t: rev(345744, 592704, t), 'duhamel_inner_f2', '345744 tau^2 E_up(592704|tau|) (own family)'),
    }
    gate_vals = {}
    for key, (fn_, route, form) in formulas.items():
        val = fn_(tau)
        if q_(val) not in ba2:
            raise CheckFailure('BA2 gate value missing: ' + key)
        gate_vals[key] = {'value': val, 'route': route, 'formula': form,
                          'ratio': fn_(tau) / fn_(tau / 100)}
    need(gate_vals['K_c2_fwd']['value'] == gate_vals['K_c1_fwd']['value'] + F(11, 8) * gate_vals['K_cmp_fwd']['value']
         and 'min(K_F1, second-route K_F2)' in ba2, 'ba2_gate_constants_exact',
         values={k: q_(v['value']) for k, v in gate_vals.items()},
         routes={k: v['route'] for k, v in gate_vals.items()},
         reading='gate item (4) ||T^{F2,N}-T|| <= min(K_F1, second-route K_F2)/(N-1): the K_F1 there is the forward '
                 'Duhamel pair with inner F1(Lambda_M), source F1(M) minus F2(N); the min equals K_c2_rev')
    r_ok = all(F(5 * r + 1, r ** 3) <= F(11, 8) / (r - 1) for r in range(2, 400))
    r_ok = r_ok and all(F(5 * n + 1, n ** 3) > F(5 * n + 6, (n + 1) ** 3) for n in range(2, 400))
    r_ok = r_ok and F(5 * 2 + 1, 8) == F(11, 8)
    need(r_ok, 'item5_ratio_inequality', statement='(5r+1)/r^3 <= (11/8)/(r-1) for r>=2 (equality at r=2; checked r<400 '
         'and (r-1)(5r+1)/r^3 = 5/r-4/r^2-1/r^3 decreasing for r>=2), and (5N+1)/N^3 decreasing')
    assemblies = {
        'inner_f1_forward_values': {'F1': [(2, 'K_c1_fwd')], 'F2': [(2, 'K_c1_fwd'), (F(11, 8), 'K_cmp_fwd')]},
        'inner_f1_whole_star_c1': {'F1': [(2, 'K_c1_rev')], 'F2': [(2, 'K_c1_rev'), (F(11, 8), 'K_cmp_fwd')]},
        'advisor_proposal_form': {'F1': [(2, 'K_c1_rev')], 'F2': [(1, 'K_c1_rev'), (1, 'K_c2_fwd'), (F(11, 8), 'K_cmp_fwd')]},
        'inner_f2_reverse_values': {'F1': [(2, 'K_c2_rev'), (F(11, 8), 'K_cmp_rev')], 'F2': [(2, 'K_c2_rev')]},
        'per_family_same_family_intermediate': {'F1': [(2, 'K_c1_fwd')], 'F2': [(2, 'K_c2_rev')]},
        'refined_inner_f1_labelled': {'F1': [(2, 'K_c1_fwd')], 'F2': [(2, 'K_c1_fwd'), (F(72, 343), 'K_cmp_fwd')]},
        'refined_inner_f2_labelled': {'F1': [(2, 'K_c2_rev'), (F(72, 343), 'K_cmp_rev')], 'F2': [(2, 'K_c2_rev')]},
    }
    cdyn = {}
    for name, a_ in assemblies.items():
        fam = {f_: sum((mu * gate_vals[k_]['value'] for mu, k_ in terms), F(0)) for f_, terms in a_.items()}
        rts = sorted({gate_vals[k_]['route'] for terms in a_.values() for _, k_ in terms})

        def at(t, a_=a_):
            return max(sum((mu * formulas[k_][0](t) for mu, k_ in terms), F(0)) for terms in a_.values())
        cdyn[name] = {'value': max(fam.values()), 'families': fam, 'routes': rts,
                      'ratio': at(tau) / at(tau / 100), 'margin': tgt['C_dyn'] / max(fam.values())}
    g_ok = all((r - 1) * F(10 * r + 6, (2 * r + 1) ** 3) <= F(72, 343) for r in range(2, 7))
    g_ok = g_ok and F(10 * 7 + 6, 8 * 49) <= F(72, 343)  # r>=7: (r-1)(10r+6)/(2r+1)^3 <= (10r+6)/(8r^2), decreasing
    g_ok = g_ok and all(F(5 * n + 1, n ** 3) <= F(10 * r + 6, (2 * r + 1) ** 3) for r in range(2, 40) for n in range(2 * r + 1, 2 * r + 4))
    need(g_ok, 'item5_refined_ratio_inequality',
         statement='for N >= 2r+1: (5N+1)/N^3 <= (10r+6)/(2r+1)^3 and (r-1)(10r+6)/(2r+1)^3 <= 72/343 (max at r=3; '
                   'for r>=7 it is below (10r+6)/(8r^2) <= 76/392); labelled refinement of the frozen 11/8 step')
    cfloor = 2 * min(v['value'] for k, v in gate_vals.items() if not k.startswith('K_cmp'))
    cmin = min(v['value'] for k, v in cdyn.items() if not k.startswith('refined'))
    need(cfloor == 2 * gate_vals['K_c2_rev']['value'] and all(v['value'] >= cfloor for v in cdyn.values()),
         'item5_C_dyn_floor', floor=q_(cfloor), preview=preview(cfloor),
         statement='every assembly bounds ||B_N-B_r|| and ||B_r-B_inf|| by admitted Cauchy or limit constants over '
                   '(r-1), each at least K_c2_rev: a producer C_dyn below 2K_c2_rev without a labelled refinement is an error')
    need(all(v['value'] <= tgt['C_dyn'] and v['margin'] >= 2 and F(9500) <= v['ratio'] <= F(10500) for v in cdyn.values())
         and cmin == cdyn['inner_f2_reverse_values']['value'] and cdyn['advisor_proposal_form']['value']
         == F('175777236988465912821/759247655761718750000000000000'), 'item5_C_dyn_assemblies',
         assemblies={k: {'value': q_(v['value']), 'preview': preview(v['value']), 'routes': v['routes'],
                         'margin': preview(v['margin']), 'ratio_tau_over_100': preview(v['ratio'])} for k, v in cdyn.items()},
         statement='each family: ||B_N-B_r|| + ||B_r-B_inf|| with B_r a Lambda_{r_N} box evolution; every step an '
                   'admitted BA2 statement; (5N+1)/N^3 <= (5r+1)/r^3 <= (11/8)/(r-1)')
    rn = {n: (n - 1) // 2 for n in (5, 6, 7, 9, 10, 20)}
    need(rn == {5: 2, 6: 2, 7: 3, 9: 4, 10: 4, 20: 9}, 'item5_r_N_frozen', r_N={str(k): v for k, v in rn.items()})
    terms = {}
    for label, cp_, csp_, cd_ in (('telescoped_inner_f1_forward', tel['C_prime'], tel['c_site_prime'], cdyn['inner_f1_forward_values']['value']),
                                  ('union_inner_f2', uni['C_prime'], uni['c_site_prime'], cdyn['inner_f2_reverse_values']['value']),
                                  ('telescoped_worst_assembly', tel['C_prime'], tel['c_site_prime'], cdyn['inner_f1_whole_star_c1']['value']),
                                  ('at_targets', tgt['C_prime'], tgt['c_site_prime'], tgt['C_dyn'])):
        terms[label] = [item5_terms(n, cd_, csp_, cp_, q) for n in (5, 10, 20)]
    t5 = terms['telescoped_inner_f1_forward'][0]
    need(t5['r_N'] == 2 and t5['Lambda_r_sites'] == 125 and t5['state'] > t5['dynamics'] > t5['mean']
         and terms['at_targets'][0]['state'] > terms['at_targets'][0]['dynamics']
         and all(row['dynamics'] > row['state'] for lab in terms for row in terms[lab][1:]),
         'item5_three_terms', terms={lab: [{k: (preview(v) if isinstance(v, F) else v) for k, v in row.items()}
                                           for row in rows] for lab, rows in terms.items()},
         statement='at N=5 the state term (c\'_site on Lambda_2, 125 sites, q^3) exceeds the dynamics term; from N=10 on '
                   'the O(1/N) dynamics term dominates; the constants are kept separate')

    # 9. scaling ---------------------------------------------------------------------------------------------------------
    ratio_sec = (C_2h / (1 - q2)) / (C_2h / (1 - q2 / 100))
    need(ratio_sec == F(1085053, 1083425) and F(99, 100) <= ratio_sec <= F(101, 100)
         and (151552 * tau) / (151552 * tau / 100) == 100, 'scaling_ratios',
         C_prime='exactly 1 (C_h, q fixed)', c_site_prime='exactly 1', secondary_telescoped=q_(ratio_sec),
         secondary_union='exactly 1', q_secondary='exactly 100',
         C_dyn={k: preview(v['ratio']) for k, v in cdyn.items()},
         components={k: preview(v['ratio']) for k, v in gate_vals.items()},
         brackets=pre['scaling_brackets_per_constant'])

    # 10. fixtures ------------------------------------------------------------------------------------------------------
    # (a) one-state ball, alternating: two subsequential limits; N to N+1 steps 1/(2(N+1)) with a zigzag
    eps = F(1, 10 ** 8)
    alt = [(F(1, 2) + (-1) ** n * eps, F(1, 2) - (-1) ** n * eps) for n in range(2, 12)]
    ball = all(abs(a - F(1, 2)) + abs(b - F(1, 2)) == 2 * eps for a, b in alt)
    two_limits = alt[0] != alt[1] and all(alt[i] == alt[i + 2] for i in range(len(alt) - 2))
    p_, up, turns = F(1, 4), True, []
    for n in range(2, 400):
        step = F(1, 2 * (n + 1))
        p_ = p_ + step if up else p_ - step
        if up and p_ >= F(3, 4) or (not up) and p_ <= F(1, 4):
            turns.append(n)
            up = not up
    zig = len(turns) >= 3 and all(F(1, 2 * (n + 1)) < F(1, 50) for n in turns[2:])
    geo = all(max(abs(sum(((-1) ** k) * C_h * q ** (k - 1) for k in range(n, mm))) for mm in range(n + 1, 30))
              <= cprime('nested_telescoping', C_h, q) * q ** (n - 1) for n in range(2, 8))
    need(ball and two_limits and zig and geo, 'fixture_whole_sequence_vs_subsequence_exact', zigzag_turns=turns[:6],
         statement='(i) rho_N = diag(1/2+(-1)^N eps, 1/2-(-1)^N eps) stays in the trace-norm ball 2eps about P for every N '
                   'yet has two subsequential limits; (ii) steps 1/(2(N+1)) tend to 0 while p_N turns between 1/4 and 3/4 '
                   'at N=%s...: a per-step bound is not a Cauchy estimate; (iii) geometric steps C_h q^(k-1) with any signs '
                   'give sup over M>N at most C_h q^(N-1)/(1-q)' % turns[:3])
    # (b) complex-mean centering
    half, quarter = F(1, 2), F(1, 4)
    rho = [[(half, F(0)), (quarter, quarter)], [(quarter, -quarter), (half, F(0))]]
    det = half * half - gabs2((quarter, quarter))
    a_op = [[(F(0), F(0)), (F(1), F(0))], [(F(0), F(0)), (F(0), F(0))]]
    mean = gtrace_prod(rho, a_op)
    a_star_a = gmatmul(gadjoint(a_op), a_op)
    second = gtrace_prod(rho, a_star_a)
    var_ok = (second[0] - gabs2(mean), second[1])
    wrong_sq = gmul(mean, mean)
    wrong = (second[0] - wrong_sq[0], second[1] - wrong_sq[1])
    re_only = second[0] - mean[0] ** 2
    rho2 = [[(half, F(0)), (F(0), F(0))], [(F(0), F(0)), (half, F(0))]]
    mean2 = gtrace_prod(rho2, a_op)
    lip = (gabs2(mean) - gabs2(mean2)) ** 2 <= 4 * gabs2((mean[0] - mean2[0], mean[1] - mean2[1]))  # ||A||=1
    need(det > 0 and mean == (quarter, -quarter) and var_ok == (F(3, 8), F(0)) and wrong == (F(1, 2), F(1, 8))
         and re_only == F(7, 16) and gabs2(mean) == F(1, 8) and lip, 'fixture_correlation_centering_exact',
         statement='rho=[[1/2,(1+i)/4],[(1-i)/4,1/2]] (det 1/8>0), A=sigma_+: omega(A)=(1-i)/4, |omega(A)|^2=1/8, '
                   'c_A(0)=omega(A*A)-|omega(A)|^2=3/8 (a variance); omega(A)^2 centering gives 1/2+i/8 (complex), '
                   '(Re omega(A))^2 centering gives 7/16; the mean term obeys ||a|^2-|b|^2| <= 2||A|| |a-b|')
    # (c) cutoff-limit order: Eckart with gap 1/2 and the non-uniform double sequence
    hdiag = [F(0), F(1, 2), F(2)]
    eck = []
    for vec in ([F(1, 3), F(2, 3), F(2, 3)], [F(2, 3), F(2, 3), F(1, 3)], [F(1), F(0), F(0)]):
        if sum(x * x for x in vec) != 1:
            raise CheckFailure('eckart vector norm')
        energy = sum(h * x * x for h, x in zip(hdiag, vec))
        eck.append((1 - vec[0] ** 2, 2 * energy))
    gapless = (1 - F(0), 2 * (F(0) - F(0)))  # H'=diag(0,0,1), e_2 has the ground energy, overlap 0
    dbl = {(n, l): 1 if l >= n else 0 for n in range(1, 30) for l in range(1, 30)}
    lim_l_then_n = all(dbl[(n, 29)] == 1 for n in range(1, 29))
    lim_n_then_l = all(dbl[(29, l)] == 0 for l in range(1, 29))
    need(all(a <= b for a, b in eck) and eck[0] == (F(8, 9), F(20, 9)) and gapless[0] > gapless[1]
         and lim_l_then_n and lim_n_then_l, 'fixture_cutoff_limit_order_exact', eckart_pairs=[[q_(a), q_(b)] for a, b in eck],
         statement='1-|<psi,psi_L>|^2 <= 2(E_L-E_0) with gap 1/2 (AV1 F22 form, own vectors; the pair (8/9,20/9) '
                   'reproduces AV1); without the gap a ground-energy vector can be orthogonal; a_{N,L}=[L>=N] has '
                   'lim_N lim_L = 1 and lim_L lim_N = 0, so the order L then N is part of the statement')
    # (d) cross-coupling: +tau and -tau limits separated (AY2) while a BB1 comparison bound tends to 0
    ay2 = json.loads((ROOT / 'research/round32/advisor/ay2-gate.json').read_text())['accepted']
    sep = F(re.search(r"sqrt\(10\)\|tau\|/36-2K_2' tau\^2 >= (\d+/\d+)", ay2).group(1))
    n_contra = min(n for n in range(2, 40) if (2 * tel['C_prime'] + C_h) * q ** (n - 1) < sep)
    need(sep > F(8, 10 ** 10) and n_contra == 4, 'fixture_cross_coupling_not_a_comparison', separation=preview(sep),
         first_N=n_contra, statement='the +tau and -tau subsequential limits differ on R by at least 8.757e-10 (AY2 gate); '
         'treating that pair as a BB1 comparison would force (2C\'+C_h)q^(N-1) >= 8.757e-10, false from N=4')
    # (e) polynomial tail: the Lieb-Robinson shell tail from distance k is at least 1/(4k)
    poly_ok = all(k * F(4 * (2 * k - 1) ** 2 + 2, (2 * k) ** 4) >= F(1, 4 * k) for k in range(1, 300))
    need(poly_ok, 'fixture_polynomial_tail', statement='with F(r)=(1+r)^-4 the shell tail is at least 1/(4k): the item-5 '
         'dynamics term is O(1/N) (C_dyn/(r_N-1)); an exponential rate in N is not available from these constants')
    # (f) fixed versus moving vector (topology)
    ok_fm = True
    for n_ in range(1, 41):
        k_uau = n_ % (2 * n_)
        ok_fm = ok_fm and k_uau == n_ and (F(22, 7 * n_) < F(1, 10)) == (n_ >= 32)
    need(ok_fm, 'fixture_fixed_versus_moving_vector', statement='||U(pi/n)AU(pi/n)*-A|| = 2 for every n (witness e_n, '
         'A e_j = e_{2j}), while U(t)e_1 -> e_1: dynamics is per fixed local A on compact windows; states in trace norm')

    # 11. discharge engine on labelled synthetic BB1 outcomes ------------------------------------------------------------
    hyp = {'q': q, 'const': {'R': C_h, 'Y': c_h},
           'shape': {'R': {'q': q, 'exponent_shift': 0, 'Y_power': 0, 'Y_exp_rate': F(0)},
                     'Y': {'q': q, 'exponent_shift': 0, 'Y_power': 1, 'Y_exp_rate': F(1, 10 ** 8)}}}
    c_prev = F(352765230433, 201124673670833280)  # advisor-recorded split preview (advisor-only; not a BB1 result)

    def entry(cval, form, **kw):
        shp = dict(hyp['shape'][form])
        shp.update(kw)
        return {'c': cval, 'shape': shp}

    def record(verdict='accepted_within_scope', cR=c_prev, cY=c_prev / 2, drop=(), dropY=False, over=None,
               regimes=('Q_L', 'untruncated'), signs=('+', '-'), shapeY=None):
        adm = {}
        for comp in COMPARISONS:
            if comp in drop:
                adm[comp] = None
                continue
            r_ = entry(cR, 'R')
            y_ = None if dropY else entry(cY, 'Y', **(shapeY or {}))
            if over and comp in over:
                r_ = entry(over[comp], 'R')
                y_ = None if dropY else entry(over[comp] / 2, 'Y')
            adm[comp] = {'R': r_, 'Y': y_}
        return {'verdict': verdict, 'admitted': adm, 'regimes': list(regimes), 'signs': list(signs),
                'label': 'synthetic BB1 outcome for the discharge protocol; not a BB1 result'}

    synth = {
        'S1_accepted_preview_values': record(),
        'S2_region_form_missing': record(verdict='limited', dropY=True),
        'S3_general_volume_missing': record(verdict='limited', drop=('c5_one_prescription_volumes',)),
        'S4_bb1_insufficient': record(verdict='insufficient', drop=COMPARISONS),
        'S5_same_N_constant_above_hypothesis': record(verdict='limited', over={'c3_F1_vs_F2_same_N': F(1, 200000)}),
        'S6_cutoff_spaces_only': record(verdict='limited', regimes=('Q_L',)),
        'S7_one_sign_only': record(signs=('+',)),
        'S8_centered_any_two_missing': record(drop=('c4_centered_any_two',)),
        'S9_admitted_equal_to_hypothesis': record(cR=C_h, cY=c_h),
        'S10_sharper_exponent': record(shapeY={'exponent_shift': 1}),
        'S11_region_power_two': record(verdict='limited', shapeY={'Y_power': 2}),
        'S12_other_rate': record(verdict='limited', shapeY={'q': F(1, 32)}),
    }
    expected = {
        'S1_accepted_preview_values': ('accepted_within_scope', {'1': 'full', '2': 'full', '3': 'full', '4': 'full', '5': 'full'}),
        'S2_region_form_missing': ('limited', {'1': 'R_only', '2': 'R_only', '3': 'R_marginals', '4': 'R_translate_covariance', '5': 'dropped'}),
        'S3_general_volume_missing': ('limited', {'1': 'full', '2': 'full', '3': 'full', '4': 'dropped', '5': 'full'}),
        'S4_bb1_insufficient': ('insufficient', {'1': 'conditional', '2': 'conditional', '3': 'conditional', '4': 'conditional', '5': 'conditional'}),
        'S5_same_N_constant_above_hypothesis': ('limited', {'1': 'full', '2': 'conditional', '3': 'per_family', '4': 'full', '5': 'per_family'}),
        'S6_cutoff_spaces_only': ('accepted_within_scope', {'1': 'full', '2': 'full', '3': 'full', '4': 'full', '5': 'full'}),
        'S7_one_sign_only': ('limited', {'1': 'conditional', '2': 'conditional', '3': 'conditional', '4': 'conditional', '5': 'conditional'}),  # full at +
        'S8_centered_any_two_missing': ('accepted_within_scope', {'1': 'full', '2': 'full', '3': 'full', '4': 'full', '5': 'full'}),
        'S9_admitted_equal_to_hypothesis': ('accepted_within_scope', {'1': 'full', '2': 'full', '3': 'full', '4': 'full', '5': 'full'}),
        'S10_sharper_exponent': ('accepted_within_scope', {'1': 'full', '2': 'full', '3': 'full', '4': 'full', '5': 'full'}),
        'S11_region_power_two': ('limited', {'1': 'R_only', '2': 'R_only', '3': 'R_marginals', '4': 'R_translate_covariance', '5': 'dropped'}),
        'S12_other_rate': ('limited', {'1': 'R_only', '2': 'R_only', '3': 'R_marginals', '4': 'R_translate_covariance', '5': 'dropped'}),
    }
    outcomes = {}
    for name, rec in synth.items():
        res = discharge(rec, hyp)
        want_v, want_i = expected[name]
        if res['verdict'] != want_v or res['items'] != want_i:
            raise CheckFailure('discharge fixture ' + name + ' ' + json.dumps(res['items']) + ' ' + res['verdict'])
        outcomes[name] = res
    s1 = outcomes['S1_accepted_preview_values']['reevaluated']
    need(s1['F1_R_forward'] == c_prev / (1 - q) and s1['F1_R_reverse'] == c_prev
         and outcomes['S6_cutoff_spaces_only']['routes_plus']['F1_R'] == ['forward']
         and outcomes['S8_centered_any_two_missing']['routes_plus']['F1_Y'] == ['forward']
         and outcomes['S2_region_form_missing']['gate_fields']['translation_invariance_claimed'] is False
         and outcomes['S2_region_form_missing']['gate_fields']['dynamics_level'] is None
         and all(v == 'full' for v in outcomes['S7_one_sign_only']['items_by_sign']['+'].values()),
         'discharge_engine_fixtures',
         outcomes={k: {'verdict': v['verdict'], 'items': v['items'],
                       'gate_fields_true': sorted(g for g, x in v['gate_fields'].items() if x is True),
                       'reevaluated': {r: preview(x) for r, x in v['reevaluated'].items()}} for k, v in outcomes.items()},
         labelled='synthetic BB1 outcomes; S1 uses the advisor-recorded split preview C=352765230433/201124673670833280 '
                  'and C/2 per site, not a BB1 result; S7: items full at +tau, conditional at -tau (limited, both-sign '
                  'fields false, the -tau implications retained as conditional)')

    # 12. validator and controls -----------------------------------------------------------------------------------------
    sentence = pre['mandatory_sentence_template']
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings']) + EXTRA_FORBIDDEN
    need(not affirmative_hits(sentence, forbidden) and not placeholder_spans(sentence)
         and 'under the BB1 locality bounds at their frozen targets as hypotheses' in sentence,
         'template_scan_clean', phrase_scan_sha256_mirrored=PHRASE_SCAN_MIRRORED_SHA256,
         freezer_sha256_mirrored=FREEZER_MIRRORED_SHA256)
    brackets = dict(pre['scaling_brackets_per_constant'])
    ctx = {'tau': tau, 'declared_inputs': declared_inputs, 'control_ids': control_ids, 'q': q, 'C_h': C_h, 'c_h': c_h,
           'C_2h': C_2h, 'c_2h': c_2h, 'targets': tgt, 'ba2': gate_vals, 'C_dyn_min': cfloor,
           'C_min': {a: consts[a]['C_prime'] for a in consts}, 'c_min': {a: consts[a]['c_site_prime'] for a in consts},
           'brackets': brackets, 'sentence': sentence, 'forbidden': forbidden, 'gate_fields': gfr,
           'error_terms': list(pre['error_terms_itemized'])}
    statements = [
        'For each family the reduced densities on every finite region form a Cauchy sequence over all M greater than N at '
        'the rate q^(d_Y) in N; the limit exists by completeness of the trace class, without compactness.',
        'The F1 and F2 limits coincide on every finite region; this is the limit of the named constructions and not '
        'uniqueness of any ground state.',
        'Every conclusion is an implication from the BB1 frozen targets, labelled conditional_on_bb1_targets until the '
        'BB1 gate discharges it; the rate is in N at fixed spacing and not uniform in the lattice spacing a.',
    ]

    def packet(route):
        asm = ASSEMBLY_OF_ROUTE[route]
        coef = 1 / (1 - q) if asm == 'nested_telescoping' else F(1)
        comps = assemblies['inner_f1_forward_values'] if route == 'forward' else assemblies['inner_f2_reverse_values']
        cd_name = 'inner_f1_forward_values' if route == 'forward' else 'inner_f2_reverse_values'
        pk = {
            'route': route, 'contract_sha256': CONTRACT_SHA256, 'bb1_contract_sha256': BB1_CONTRACT_SHA256,
            'inputs': list(declared_inputs), 'controls': {k: True for k in control_ids},
            'model_id': MODEL_ID, 'triple': ['0', '0', '0'], 'group': 'SU(2)', 'lattice': 'Z^3 coarse 24-link factors',
            'model_is_finite_graph': False, 'tau_abs': tau, 'signs': ['+', '-'], 'cover': list(R_COVER),
            'same_coupling': True, 'compared_couplings': ['same tau'], 'clock_per_family': [CLOCK, CLOCK],
            'families': list(FAMILIES), 'N_min': 2,
            'parameters': {'metric_states': METRIC_STATES, 'metric_dynamics': METRIC_DYNAMICS, 'weights': WEIGHTS,
                           'window': '|theta| at most 8', 'clock': CLOCK, 'N_min': 2},
            'topology': dict(TOPOLOGY), 'clock': CLOCK,
            'hypotheses': {'source': 'bb1_frozen_targets', 'q': q, 'C_h': C_h, 'c_h': c_h, 'C_2h': C_2h, 'c_2h': c_2h,
                           'comparisons': list(COMPARISONS), 'forms': ['R', 'Y'], 'regimes': ['Q_L', 'untruncated'],
                           'signs': ['+', '-']},
            'targets': dict(tgt), 'q_per_N': False, 'rate_reported': 'q=1/64 frozen',
            'conditional': {'label': 'conditional_on_bb1_targets', 'unconditional_claimed': False},
            'item1': {'quantifier': 'all M greater than N', 'limit_kind': 'whole sequence',
                      'whole_sequence_via': 'Cauchy bound over all M greater than N',
                      'limit_existence': 'Cauchy bound and completeness of the trace class', 'assembly': asm,
                      'tier': 'exact_first_order', 'hypothesis_source': 'bb1_frozen_targets', 'bb1_route': None,
                      'combine': 'linear',
                      'function': {'C_prime': [coef, F(0)], 'c_site_prime': [F(0), coef], 'monotone_checked': True},
                      'C_prime': consts[asm]['C_prime'], 'c_site_prime': consts[asm]['c_site_prime'],
                      'region_factor': '|Y| e^{|Y|/10^8} q^{d_Y}', 'd_Y': 'N - max_{y in Y}|y|_inf'},
            'cutoff': {'order': CUTOFF_ORDER, 'uniform_in_L': True, 'vector_removal': True},
            'item2': {'via': ['c3_F1_vs_F2_same_N', 'item1'], 'scope': 'every finite region', 'name': LIMIT_NAME},
            'item3': {'identified_before_inheritance': True,
                      'identified_with': ['every AQ1 subsequential limit', 'every F2 subsequential limit'],
                      'inherited': copy.deepcopy(AQ_INHERITED)},
            'item4': {'separate_item': True, 'from_nested_cubes_only': False,
                      'input': 'BB1 general-volume comparison of reduced densities (c5), direct',
                      'translations': 'coarse: fine (4v_x,2v_y,v_z)', 'noncoarse_accepted': False,
                      'via_box': 'Lambda_{N-|v|_inf}', 'bound': 'C_h q^(N-|v|_inf-1)', 'N_condition': 'N >= |v|_inf+2',
                      'union_two_step': None},
            'item5': {'N_min': 5, 'r_N': 'floor((N-1)/2)', 'r_N_post_hoc': False, 'centering': CENTERING,
                      'combine': 'linear', 'rate': 'O(1/N)', 'exponential_claimed': False, 'window': '|theta| at most 8',
                      'U': 1, 'u_over_theta': F(1, 8), 'uniform_in_time_claimed': False,
                      'gns_dynamics_equality_claimed': False, 'dynamics_level': 'correlation_functions_compact_window',
                      'state_constant': 'c_site_prime on Lambda_{r_N}, exponent N-r_N', 'mean_constant': '2 C_prime q^(N-1)',
                      'lumped_bracket': None, 'C_dyn_components': copy.deepcopy(comps), 'C_dyn': cdyn[cd_name]['value'],
                      'C_dyn_tier': 'polynomial_lieb_robinson', 'C_dyn_route': cdyn[cd_name]['routes'][0]},
            'brackets': dict(brackets),
            'scaling': {'C_prime': F(1), 'c_site_prime': F(1), 'q_secondary': F(100), 'C_dyn': cdyn[cd_name]['ratio'],
                        'secondary': ratio_sec if asm == 'nested_telescoping' else F(1)},
            'secondary': {'labelled': True, 'conditional_on': 'BB1 secondary pair', 'C_prime_2': consts[asm]['C_prime_2']},
            'targets_met': {'C_prime': True, 'c_site_prime': True, 'C_dyn': True},
            'verdict': 'accepted_within_scope', 'dominating_term': None, 'retuned': False,
            'fixtures': {'alternating_ball_sequence': 'rejected as convergence', 'n_to_n_plus_1_only': 'rejected as Cauchy',
                         'fine_translation_1_0_0': 'rejected: residues and face classes broken',
                         'centering': 'complex mean; omega(A)^2 and (Re omega(A))^2 rejected', 'fixed_vs_moving_vector': True},
            'uniform_in': UNIFORM_IN, 'rate_unit': RATE_UNIT, 'sub_labels': list(SUB_LABELS),
            'statements': list(statements), 'sentence': sentence, 'sentence_count': 1,
            'gate_fields': dict(gfr), 'gate_fields_status': 'conditional_on_bb1_discharge',
            'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                       'uniform_in_a_claimed': False},
            'error_terms': {'bb1_hypothesis_constants': 'C_h=1/250000, c_h=1/500000 at q=1/64 (frozen targets)',
                            'cauchy_telescoping_or_union': 'factor 1/(1-q)=64/63 (telescoping) or 1 (direct)',
                            'identification_with_subsequential_limits': 'exact (trace-norm limits coincide)',
                            'translation_general_volume': 'C_h q^(N-|v|-1) via Lambda_{N-|v|}',
                            'dynamics_constant_from_ba2': 'BA2 gate values, assembly stated',
                            'region_form_on_Lambda_rN': "c'_site (2r_N+1)^3 e^{(2r_N+1)^3/10^8} q^(N-r_N)",
                            'arithmetic': 'exact rationals; e^x by Taylor enclosure with geometric remainder'},
        }
        pk['freeze_digest'] = packet_digest(pk)
        return pk

    base = packet('forward')
    base_rev = packet('reverse')
    need(validate(base, ctx) and validate(base_rev, ctx), 'reference_packets_accepted', routes=['forward', 'reverse'])

    def mut(src=None, rebind=True, **kw):
        src = base if src is None else src
        pk = copy.deepcopy(src)
        for k, val in kw.items():
            parts = k.split('__')
            tgt_ = pk
            for p_ in parts[:-1]:
                tgt_ = tgt_[p_]
            tgt_[parts[-1]] = val
        if rebind:
            pk['freeze_digest'] = packet_digest(pk)
        return lambda: validate(pk, ctx)

    def mut_rev(**kw):
        return mut(src=base_rev, **kw)

    ok = [('forward reference packet', lambda: validate(base, ctx)), ('reverse reference packet', lambda: validate(base_rev, ctx))]
    control('coherent_evidence_tampering',
            [('control Boolean flipped, digest rebound', mut(controls__conditional_on_bb1_targets=False), 'control booleans'),
             ('snapshot removed, digest rebound', mut(inputs=declared_inputs[1:]), 'snapshot inventory'),
             ('digest not rebound', mut(rebind=False, controls__r_N_prefrozen=False), 'freeze digest'),
             ("C' below the telescoped value", mut(item1__C_prime=C_h, item1__function={'C_prime': [F(1), F(0)],
                                                                                         'c_site_prime': [F(0), 1 / (1 - q)],
                                                                                         'monotone_checked': True}),
              'below the derivable'),
             ("C' not its stated function", mut(item1__C_prime=F(1, 200000)), 'not its stated function'),
             ('C_dyn not its assembly', mut(item5__C_dyn=cdyn['inner_f1_forward_values']['value'] / 2), 'not its BA2 assembly'),
             ('contract rehashed', mut(contract_sha256='0' * 64), 'contract hash'),
             ('bb1 contract rehashed', mut(bb1_contract_sha256='1' * 64), 'bb1 contract hash')], ok)
    control('exact_arithmetic_admission',
            [("float C'", mut(item1__C_prime=float(tel['C_prime'])), 'exact arithmetic'),
             ('float tau', mut(tau_abs=1e-8), 'exact arithmetic'),
             ('float C_dyn', mut(item5__C_dyn=1.54e-10), 'exact arithmetic')], ok)
    control('no_priority_or_continuum_claim',
            [('continuum', mut(claims__continuum_claim=True), 'forbidden claim continuum_claim'),
             ('priority', mut(claims__scientific_priority_verified=True), 'forbidden claim scientific_priority'),
             ('weak coupling', mut(claims__weak_coupling_claim=True), 'forbidden claim weak_coupling_claim')], ok)
    control('changed_model_relabelled',
            [('tau 1e-9 under the label', mut(tau_abs=F(1, 10 ** 9)), 'changed model'),
             ('uniform triple', mut(triple=['tau/24', 'tau/24', 'tau/24']), 'changed model'),
             ('SU(3)', mut(group='SU(3)'), 'changed model'),
             ('finite graph', mut(model_is_finite_graph=True), 'changed model'),
             ('state metric l1', mut(parameters__metric_states='l1 on the coarse factor lattice'), 'changed model relabelled: metric'),
             ('cover moved', mut(cover=[(0, 0, 0), (1, 0, 0)]), 'coupling or cover'),
             ('sub-label uniqueness', mut(sub_labels=['uniform_local_closeness_not_uniqueness']), 'sub-label')], ok)
    limited_ok = mut(item1__function={'C_prime': [F(3), F(0)], 'c_site_prime': [F(0), 1 / (1 - q)], 'monotone_checked': True},
                     item1__C_prime=3 * C_h, targets_met={'C_prime': False, 'c_site_prime': True, 'C_dyn': True},
                     verdict='limited', dominating_term='cauchy_telescoping_or_union: factor 3 route at the frozen q')
    control('insufficient_verdict_retained',
            [('missed target accepted', mut(item1__function={'C_prime': [F(3), F(0)], 'c_site_prime': [F(0), 1 / (1 - q)],
                                                             'monotone_checked': True}, item1__C_prime=3 * C_h,
                                            targets_met={'C_prime': False, 'c_site_prime': True, 'C_dyn': True}),
              'insufficient verdict'),
             ('limited without dominating term', mut(item1__function={'C_prime': [F(3), F(0)], 'c_site_prime': [F(0), 1 / (1 - q)],
                                                                      'monotone_checked': True}, item1__C_prime=3 * C_h,
                                                     targets_met={'C_prime': False, 'c_site_prime': True, 'C_dyn': True},
                                                     verdict='limited'), 'dominating term'),
             ('retuned', mut(retuned=True), 'retuned'),
             ('targets_met misreported', mut(targets_met={'C_prime': True, 'c_site_prime': False, 'C_dyn': True}),
              'targets_met inconsistent')],
            ok + [('limited packet with missed target and dominating term', limited_ok)])
    control('tau_scaling_exponent',
            [("C' ratio of a BB1 formula (linear, about 100)", mut(scaling__C_prime=F(4340004, 43129)), 'tau scaling'),
             ('C_dyn ratio of a linear bound', mut(scaling__C_dyn=F(100)), 'tau scaling'),
             ('secondary ratio 100', mut(scaling__secondary=F(100)), 'tau scaling'),
             ('bracket chosen after evaluation', mut(brackets=dict(brackets, C_dyn='[9900,10100]')), 'bracket changed'),
             ('q_2 ratio 1', mut(scaling__q_secondary=F(1)), 'tau scaling')], ok,
            note="C' and c'_site: exactly 1 at the hypothesis values; secondary 1085053/1083425 (telescoped) or 1 (union)")
    control('wrong_delta_alpha_hbar_clock',
            [('u window labelled theta (U=8)', mut(item5__U=8), 'window'),
             ('Round29 dictionary label s=delta*t/hbar', mut(clock='s=delta*t/hbar', parameters__clock='s=delta*t/hbar'),
              'wrong delta alpha hbar clock'),
             ('u over theta = 8', mut(item5__u_over_theta=F(8)), 'window')], ok)
    control('root_n_misuse',
            [('item-5 terms in quadrature', mut(item5__combine='rss'), 'root-N'),
             ('telescoping steps in quadrature', mut(item1__combine='rss'), 'root-N')], ok)
    control('tier_mixing_rejected',
            [('state constant with a Lieb-Robinson tier', mut(item1__tier='polynomial_lieb_robinson'), 'tier mixing'),
             ('BB1 route claimed by a BB2 producer', mut(item1__bb1_route='iterated_split'), 'tier mixing'),
             ('assembly of the other route', mut(item1__assembly='union_comparison', item1__C_prime=C_h,
                                                 item1__c_site_prime=c_h,
                                                 item1__function={'C_prime': [F(1), F(0)], 'c_site_prime': [F(0), F(1)],
                                                                  'monotone_checked': True}), 'assembly of the route'),
             ('dynamics constant with a state tier', mut(item5__C_dyn_tier='exact_first_order'), 'dynamics tier'),
             ('dynamics route mislabelled', mut(item5__C_dyn_route='duhamel_inner_f2'), 'dynamics route'),
             ('mixed-route composite labelled as one route',
              mut(item5__C_dyn_components=copy.deepcopy(assemblies['per_family_same_family_intermediate']),
                  item5__C_dyn=cdyn['per_family_same_family_intermediate']['value'], item5__C_dyn_route='duhamel_inner_f1'),
              'mixed-route composite'),
             ('lumped item-5 bracket', mut(item5__lumped_bracket='[95,105]'), 'lumped'),
             ('dynamics constant not from the BA2 gate', mut(item5__C_dyn_components={'F1': [(2, 'K_preview')], 'F2': [(2, 'K_c2_rev')]}),
              'not a BA2 gate value')],
            ok + [('mixed-route composite with component routes listed',
                   mut(item5__C_dyn_components=copy.deepcopy(assemblies['per_family_same_family_intermediate']),
                       item5__C_dyn=cdyn['per_family_same_family_intermediate']['value'], item5__C_dyn_route='composite',
                       item5__component_routes_listed=True))],
            reading='contract: exactly one route per dynamics constant; a composite of BA2 constants of both routes is '
                    'accepted only as a labelled composite listing each component route (defect D3)')
    iso_bad = ['research/round33/skeptic/triage.md', 'research/round33/skeptic/bb-contract-review.json',
               'research/round33/experts/modern/bb-targets-proposal.md', 'research/round33/forward/bb2/report.md',
               'research/round33/advisor/deliberation-2.md', 'research/round33/advisor/plan.json']
    control('reverse_premise_isolation',
            [('reverse with ' + p_.split('/')[-1], mut_rev(inputs=declared_inputs + [p_]), 'reverse premise isolation')
             for p_ in iso_bad], ok)
    control('uniform_in_N_not_in_a',
            [('uniform in a', mut(uniform_in='the lattice spacing a'), 'uniform in N not in a'),
             ('statement uniform in a', mut(statements=statements + ['The Cauchy constants are uniform in a.']),
              'uniform in N not in a')], ok)
    control('placeholder_span_rejected',
            [('placeholder in a statement', mut(statements=statements + ["C' equals <value of the telescoped constant>."]),
              'placeholder span')],
            ok + [('inequality text kept', mut(statements=statements + ["C'<=1/100000 holds for N>=2 and M>N."]))])
    control('negation_aware_phrase_scan',
            [('affirmative thermodynamic limit', mut(statements=statements + ['This gives the thermodynamic limit of F1.']),
              'forbidden phrasing'),
             ('affirmative confirms', mut(statements=statements + ['The union route confirms the forward constant.']),
              'forbidden phrasing'),
             ('affirmative boundary independent', mut(statements=statements + ['The limit is boundary independent.']),
              'forbidden phrasing')],
            ok + [('negated phrase', mut(statements=statements + ['This is not the thermodynamic limit of all boundary conditions.']))])
    control('parameters_declare_metric_weights_window',
            [('no window', mut(parameters={k: v for k, v in base['parameters'].items() if k != 'window'}), 'window'),
             ('no clock', mut(parameters={k: v for k, v in base['parameters'].items() if k != 'clock'}), 'clock'),
             ('no weights', mut(parameters={k: v for k, v in base['parameters'].items() if k != 'weights'}), 'weights'),
             ('no N_min', mut(parameters={k: v for k, v in base['parameters'].items() if k != 'N_min'}), 'N_min'),
             ('weights other than the hypotheses', mut(parameters__weights='BB1 previews'), 'weights')], ok)
    control('rate_constant_pair_prefrozen',
            [('q changed to 1/32', mut(hypotheses__q=F(1, 32)), 'rate constant pair'),
             ("C' target moved", mut(targets=dict(tgt, C_prime=F(1, 50000))), 'rate constant pair'),
             ('q optimized per N', mut(q_per_N=True), 'rate constant pair'),
             ('other rate reported as the result', mut(rate_reported='q=1/128 proved'), 'rate constant pair'),
             ('secondary unlabelled', mut(secondary__labelled=False), 'secondary')], ok)
    control('decay_rate_in_N_not_a',
            [('rate in fm', mut(rate_unit='q per 0.1 fm'), 'decay rate in N not a'),
             ('rate in a claimed', mut(gate_fields=dict(gfr, rate_in_a_claimed=True)), 'decay rate in N not a')], ok)
    control('topology_named',
            [('states in the weak* topology only', mut(topology=dict(TOPOLOGY, states='weak* on B(H_Y)')), 'topology named'),
             ('norm continuity on all B(H)', mut(topology=dict(TOPOLOGY, dynamics='norm continuity in time on all of B(H)')),
              'topology named'),
             ('fixture missing', mut(fixtures__fixed_vs_moving_vector=False), 'topology named')], ok)
    control('two_families_named',
            [('F2 missing', mut(families=FAMILIES[:1]), 'two families'),
             ('N_min 1', mut(N_min=1), 'two families')], ok)
    control('subsequence_versus_whole_sequence',
            [('limit along a subsequence', mut(item1__limit_kind='subsequence'), 'subsequence versus whole sequence'),
             ('whole sequence via the AQ1 subsequence', mut(item1__whole_sequence_via='AQ1 diagonal extraction'),
              'subsequence versus whole sequence'),
             ('N to N+1 bound only', mut(item1__quantifier='N to N+1'), 'not a Cauchy estimate')], ok)
    control('common_clock',
            [('+tau versus -tau as a comparison', mut(compared_couplings=['+tau', '-tau']), 'common clock'),
             ('different clocks per family', mut(clock_per_family=[CLOCK, 'theta=alpha t/(8 hbar)']), 'common clock')], ok,
            fixture='+tau and -tau limits separated by at least 8.757e-10 on R (AY2); the hypothesis bound fails from N=4')
    control('named_construction_not_uniqueness',
            [('the infinite-volume ground state', mut(statements=statements + ['We obtain the infinite-volume ground state.']),
              'named construction not uniqueness'),
             ('uniqueness field', mut(gate_fields=dict(gfr, uniqueness_of_ground_state_claimed=True)),
              'named construction not uniqueness'),
             ('a unique limit', mut(statements=statements + ['The sequences have a unique limit for all boundary conditions.']),
              'named construction not uniqueness'),
             ('common limit named otherwise', mut(item2__name='the thermodynamic state'), 'named construction not uniqueness')], ok)
    control('cauchy_estimate_not_compactness',
            [('compactness plus closeness', mut(item1__limit_existence='local trace-norm compactness plus closeness of limits'),
              'cauchy estimate not compactness')], ok)
    control('limit_identified_with_aq1_limits',
            [('inherited before identification', mut(item3__identified_before_inheritance=False), 'limit identified'),
             ('identified with AQ1 only', mut(item3__identified_with=['every AQ1 subsequential limit']), 'limit identified'),
             ('full-GNS gap unqualified', mut(item3__inherited=dict(AQ_INHERITED, aq2_full_gns='gap alpha/16 in the full GNS space')),
              'inherited scope'),
             ('uniqueness inherited', mut(item3__inherited=dict(AQ_INHERITED, aq1=AQ_INHERITED['aq1'] + ['uniqueness'])),
              'inherited scope')], ok)
    control('translation_invariance_separate_item',
            [('from nested cubes alone', mut(item4__from_nested_cubes_only=True), 'translation invariance separate item'),
             ('folded into item 1', mut(item4__separate_item=False), 'translation invariance separate item'),
             ('BA1 coefficient comparison as input', mut(item4__input='BA1 general-volume coefficient comparison'), 'input'),
             ('bound through Lambda_N', mut(item4__via_box='Lambda_N'), 'bound'),
             ('N condition dropped', mut(item4__N_condition='N >= 2'), 'bound')], ok)
    control('region_constant_scales_with_Y',
            [('no |Y| factor', mut(item1__region_factor='q^{d_Y}'), 'region constant scales with Y'),
             ('d_Y = N-1 for every Y', mut(item1__d_Y='N-1'), 'region constant scales with Y'),
             ("C' reused on Lambda_r in item 5", mut(item5__state_constant='C_prime q^(N-1)'), 'region constant scales with Y')], ok)
    control('cutoff_uniform_then_removed',
            [('limits exchanged', mut(cutoff__order='N to infinity in each Q_L, then L to infinity'), 'cutoff uniform then removed'),
             ('not uniform in L', mut(cutoff__uniform_in_L=False), 'cutoff uniform then removed'),
             ('eigenvalues only', mut(cutoff__vector_removal=False), 'cutoff uniform then removed')], ok)
    control('algebraic_not_gns_dynamics',
            [('GNS dynamics equality', mut(item5__gns_dynamics_equality_claimed=True), 'algebraic not gns dynamics'),
             ('gate field', mut(gate_fields=dict(gfr, gns_dynamics_equality_claimed=True)), 'algebraic not gns dynamics'),
             ('dynamics level algebraic only', mut(item5__dynamics_level='algebraic_heisenberg_compact_window'),
              'algebraic not gns dynamics')], ok)
    control('lieb_robinson_polynomial_tail',
            [('exponential rate claimed', mut(item5__exponential_claimed=True), 'lieb-robinson polynomial tail'),
             ('rate q^N for dynamics', mut(item5__rate='O(q^N)'), 'lieb-robinson polynomial tail')], ok)
    control('time_window_named_common_clock',
            [('uniform in time', mut(item5__uniform_in_time_claimed=True), 'uniform in time'),
             ('window unnamed', mut(item5__window='all theta'), 'window'),
             ('gate field uniform in time', mut(gate_fields=dict(gfr, uniform_in_time_claimed=True)), 'uniform in time')], ok)
    control('fixture_whole_sequence_vs_subsequence',
            [('alternating sequence accepted', mut(fixtures__alternating_ball_sequence='accepted'), 'fixture whole sequence'),
             ('per-step bound accepted', mut(fixtures__n_to_n_plus_1_only='accepted'), 'fixture whole sequence')], ok)
    control('fixture_translation_residues',
            [('fine translation accepted', mut(item4__noncoarse_accepted=True), 'fixture translation residues'),
             ('translations named in fine units', mut(item4__translations='fine (1,0,0) steps'), 'fixture translation residues'),
             ('fixture missing', mut(fixtures__fine_translation_1_0_0='not run'), 'fixture translation residues')], ok)
    control('fixture_correlation_centering',
            [('omega(A)^2 centering', mut(item5__centering='omega(A)^2'), 'fixture correlation centering'),
             ('real-part centering', mut(item5__centering='(Re omega(A))^2'), 'fixture correlation centering'),
             ('fixture missing', mut(fixtures__centering='not run'), 'fixture correlation centering')], ok)
    control('conditional_on_bb1_targets',
            [('BB1 preview value used', mut(hypotheses__C_h=c_prev), 'BB1 value other than the frozen targets'),
             ('condition dropped', mut(conditional__label=None), 'condition dropped'),
             ('unconditional before discharge', mut(conditional__unconditional_claimed=True), 'unconditional before discharge'),
             ('decreasing in c_h, equal at the hypothesis values',
              mut(item1__function={'C_prime': [2 / (1 - q), -2 / (1 - q)], 'c_site_prime': [F(0), 1 / (1 - q)],
                                   'monotone_checked': True}), 'decreases'),
             ('BB1 value above the frozen target, self-consistent',
              mut(hypotheses__C_h=F(1, 200000), item1__C_prime=F(1, 200000) / (1 - q),
                  targets_met={'C_prime': True, 'c_site_prime': True, 'C_dyn': True}),
              'BB1 value other than the frozen targets'),
             ('hypothesis scope narrowed to R', mut(hypotheses__forms=['R']), 'scope narrowed'),
             ('gate fields exported unconditionally', mut(gate_fields_status='unconditional'), 'unconditional'),
             ('BB1 gate file read', mut(inputs=declared_inputs + ['research/round33/advisor/bb1-gate.json']),
              'BB1 production file read'),
             ('BB1 forward report read', mut_rev(inputs=declared_inputs + ['research/round33/forward/bb1/report.md']),
              'BB1 production file read')], ok)
    control('r_N_prefrozen',
            [('r_N = floor(N/2)', mut(item5__r_N='floor(N/2)'), 'r_N prefrozen'),
             ('r_N chosen after evaluation', mut(item5__r_N_post_hoc=True), 'r_N prefrozen'),
             ('item 5 from N=4', mut(item5__N_min=4), 'r_N prefrozen')], ok)
    # extras
    control('union_two_step_labelled',
            [('union two-step as the item-4 bound', mut_rev(item4__union_two_step={'labelled': False, 'factor': '1+q^|v|_inf'}),
              'union two-step'),
             ('union factor understated', mut_rev(item4__union_two_step={'labelled': True, 'factor': '1'}), 'union two-step')],
            ok + [('labelled union two-step', mut_rev(item4__union_two_step={'labelled': True, 'factor': '1+q^|v|_inf'}))])
    control('mandatory_sentence_once',
            [('quoted twice', mut(sentence_count=2), 'mandatory sentence'),
             ('hypothesis clause dropped', mut(sentence=sentence.replace(
                 ', under the BB1 locality bounds at their frozen targets as hypotheses (discharged only when the BB1 gate '
                 'admits constants at most those targets),', ',')), 'mandatory sentence')], ok)
    control('error_terms_itemized',
            [('region term missing', mut(error_terms={k: v for k, v in base['error_terms'].items() if k != 'region_form_on_Lambda_rN'}),
              'error term missing'),
             ('not_applicable without reason', mut(error_terms=dict(base['error_terms'], translation_general_volume='not_applicable')),
              'without a reason')], ok)
    # discharge protocol as damaging mutations of the post-review record
    s_rec = synth

    def claim_of(name, **kw):
        tr = discharge(s_rec[name], hyp)
        cl = {'bb1_gate_sha256': 'a' * 64, 'items': dict(tr['items']), 'verdict': tr['verdict'],
              'unconditional': tr['unconditional'], 'gate_fields': dict(tr['gate_fields']),
              'reevaluated': dict(tr['reevaluated']), 'retained_conditional': tr['verdict'] != 'accepted_within_scope'}
        for k, v in kw.items():
            parts = k.split('__')
            t_ = cl
            for p_ in parts[:-1]:
                t_ = t_[p_]
            t_[parts[-1]] = v
        return lambda: validate_discharge_claim(cl, s_rec[name], hyp)

    def items_with(name, **kv):
        it = dict(discharge(s_rec[name], hyp)['items'])
        it.update({k.lstrip('_'): v for k, v in kv.items()})
        return it

    control('discharge_protocol_executable',
            [('item 4 claimed without the general-volume comparison',
              claim_of('S3_general_volume_missing', items=items_with('S3_general_volume_missing', _4='full')), 'undischarged item'),
             ('accepted with the region form missing', claim_of('S2_region_form_missing', verdict='accepted_within_scope'), 'verdict'),
             ('unconditional with BB1 insufficient', claim_of('S4_bb1_insufficient', unconditional=True), 'unconditional before discharge'),
             ('common limit claimed with the same-N constant above the hypothesis',
              claim_of('S5_same_N_constant_above_hypothesis', items=items_with('S5_same_N_constant_above_hypothesis', _2='full')),
              'undischarged item'),
             ('region power two treated as dominated',
              claim_of('S11_region_power_two', items=items_with('S11_region_power_two', _5='full')), 'undischarged item'),
             ('other rate treated as dominated', claim_of('S12_other_rate', items=items_with('S12_other_rate', _3='full')),
              'undischarged item'),
             ('re-evaluated at the hypothesis values', claim_of('S1_accepted_preview_values',
                                                                 reevaluated=dict(outcomes['S1_accepted_preview_values']['reevaluated'],
                                                                                  F1_R_forward=tel['C_prime'])), 're-evaluation'),
             ('translation field true with the region form missing',
              claim_of('S2_region_form_missing', gate_fields=dict(outcomes['S2_region_form_missing']['gate_fields'],
                                                                   translation_invariance_claimed=True)), 'gate field'),
             ('BB1 gate sha256 not recorded', claim_of('S1_accepted_preview_values', bb1_gate_sha256=None), 'sha256 not recorded'),
             ('conditional statements dropped', claim_of('S3_general_volume_missing', retained_conditional=False), 'not retained'),
             ('one-sign admission promoted', claim_of('S7_one_sign_only', verdict='accepted_within_scope'), 'verdict')],
            [(name, claim_of(name)) for name in sorted(s_rec)],
            protocol='item discharged when at least one route uses only admitted comparisons at constants at most the '
                     'hypothesis values (same q, form dominated pointwise), in the needed regime and at both signs')

    ids = set(control_ids)
    done = {row['id'] for row in CHECKS if row.get('kind') == 'control'}
    missing = sorted(ids - done)
    need(not missing, 'contract_controls_covered', implemented=len(ids & done), of=len(ids), deferred=missing,
         extras=sorted(done - ids))

    predictions = {
        'forward_nested_telescoping': {"C'": q_(tel['C_prime']), "c'_site": q_(tel['c_site_prime']),
                                       'margins': '315/128 = 2.4609375 each', "C'_2": q_(tel['C_prime_2']),
                                       'margin_secondary': q_(margins['nested_telescoping']['C_prime_2']),
                                       'tau_ratio': 'exactly 1 (secondary 1085053/1083425)'},
        'reverse_union_comparison': {"C'": q_(uni['C_prime']), "c'_site": q_(uni['c_site_prime']), 'margins': '5/2 each',
                                     "C'_2": q_(uni['C_prime_2']), 'tau_ratio': 'exactly 1 (secondary exactly 1)'},
        'C_dyn': {k: {'value': q_(v['value']), 'preview': preview(v['value']), 'margin': preview(v['margin']),
                      'routes': v['routes'], 'ratio': preview(v['ratio'])} for k, v in cdyn.items()},
        'item4': 'C_h q^(N-|v|_inf-1), N >= |v|_inf+2, via Lambda_{N-|v|_inf} and the direct c5 comparison; union two-step '
                 'factor 1+q^|v|_inf labelled',
        'item5_N5_N10_N20': {lab: [preview(row['sum']) for row in rows] for lab, rows in terms.items()},
    }
    return {
        'loop': 'BB2', 'stage': 'pre_comparison', 'reviewer': 'skeptic (model agent, correlated ancestry)',
        'human_author': 'Hruday N M (BUNZEEY)', 'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'bb1_contract_sha256': b1_sha, 'bb1_frozen_at': bb1['frozen_at'],
        'model': MODEL_ID + ': SU(2) Kogut-Susskind form on Z^3 at fixed spacing, coarse 24-link factors, selected triple '
                 '(0,0,0), 21 omitted faces per anchor entering as -(tau/3)W_f (delta=alpha/8); both signs |tau|<=10^-8; '
                 'families F1 (AQ1 whole-star boxes) and F2 (I1 section 6 all-contained-face boxes with padding) on '
                 'Lambda_N=[-N,N]^3, N at least 2; reduced densities on finite complete-factor regions, cover R={0,e_z}',
        'hypotheses': {'q': q_(q), 'C_h': q_(C_h), 'c_h': q_(c_h), 'q_2': '151552|tau| = ' + q_(q2), 'C_2h': q_(C_2h),
                       'c_2h': q_(c_2h), 'source': 'bb1_frozen_targets'},
        'targets': {k: q_(v) for k, v in tgt.items()}, 'target_secondary': q_(tgt_sec),
        'item1': {a: {k: q_(v) for k, v in cc.items()} for a, cc in consts.items()},
        'item1_margins': {a: {k: q_(v) for k, v in mm.items()} for a, mm in margins.items()},
        'ba2_constants': {k: {'value': q_(v['value']), 'route': v['route'], 'formula': v['formula'],
                              'ratio': q_(v['ratio'])} for k, v in gate_vals.items()},
        'C_dyn': {k: {'value': q_(v['value']), 'routes': v['routes'], 'ratio': q_(v['ratio']),
                      'families': {f_: q_(x) for f_, x in v['families'].items()}} for k, v in cdyn.items()},
        'item5_terms': {lab: [{k: (q_(v) if isinstance(v, F) else v) for k, v in row.items()} for row in rows]
                        for lab, rows in terms.items()},
        'discharge_protocol': {
            'rule': 'an item is unconditional only when, at both signs, at least one BB2 route proves it from BB1 '
                    'comparisons that the BB1 gate admits at q=1/64 with a bound dominated pointwise by the hypothesis '
                    'form and constant at most the hypothesis value, in the untruncated regime (or in each Q_L when the '
                    'route itself removes the cutoff at fixed N); the gate records the BB1 gate sha256, the BB1 route of '
                    'the bound value, the item-by-item status and the BB2 constants re-evaluated at the admitted values',
            'uses': {'1_forward': 'c1 (F1), c2 (F2): R form for C\', region form for c\'_site; factor 1/(1-q)',
                     '1_reverse': 'c4 (F1 and F2, same family): R and region forms; factor 1',
                     '2': 'item 1 for both families and c3 (same N), R and region forms',
                     '3': 'item 2 in region form (full states); item 1 in R form gives R-marginals only',
                     '4': 'c5 in R form (quantitative bound) and region form plus item 1 region form (invariance of the state)',
                     '5': 'items 1-2 in region form on Lambda_{r_N}, item 1 R form (mean term), BA2 gate constants'},
            'outcomes': {k: {'verdict': v['verdict'], 'items': v['items']} for k, v in outcomes.items()},
        },
        'contract_readings': [
            'R1 union_comparison = one direct application of a BB1 general-volume hypothesis (c4 or c5); a two-step '
            'comparison through a third volume is labelled (item 4: factor 1+q^|v|)',
            'R2 C_dyn: any assembly of admitted BA2 statements; single route when all components share it, otherwise a '
            'labelled composite with component routes',
            'R3 item-level discharge through at least one route; a route whose comparison is undischarged is retained '
            'conditional and recorded',
            'R4 item 4 with the region form missing keeps only the R bound and R-translate covariance',
            'R5 required[2] "in its own GNS representation" is read through items.3 (invariant-local cyclic completion; '
            'full-GNS only as qualified)',
            'R6 d_Y as in BB1 region_form; c4 "of F1 or F2" read to include cross-family pairs (labelled if used)',
            'R7 inherited control semantics (BA2, BB1 texts) read by name for BB2',
            'R8 at a limited verdict the template is quoted inside the frame "established except for item k"'],
        'gate_fields': gfr, 'sentence': sentence,
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                   'uniform_in_a_claimed': False, 'uniqueness_of_ground_state_claimed': False},
        'deferred_parts': {
            'reverse_premise_isolation': 'actual inventories recorded by name and hash (38 files each, identical to the '
                                         'repository); report contents checked at post-comparison',
            'conditional_on_bb1_targets': 'the discharge itself needs the BB1 gate (not yet recorded); the protocol is '
                                          'executable now on labelled synthetic outcomes',
            'limit_identified_with_aq1_limits': 'the producers\' inheritance texts are checked at post-comparison'},
        'checks': CHECKS,
        'previews': {'C_prime_telescoped': preview(tel['C_prime']), 'c_site_prime_telescoped': preview(tel['c_site_prime']),
                     'C_prime_2_telescoped': preview(tel['C_prime_2']),
                     'C_dyn_inner_f1_forward_values': preview(cdyn['inner_f1_forward_values']['value']),
                     'C_dyn_inner_f2': preview(cdyn['inner_f2_reverse_values']['value']),
                     'C_dyn_worst_natural': preview(cdyn['inner_f1_whole_star_c1']['value'])},
        'predictions': predictions,
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
                      "C'": result['previews']['C_prime_telescoped'], 'C_dyn_f1': result['previews']['C_dyn_inner_f1_forward_values']}))


if __name__ == '__main__':
    main()
