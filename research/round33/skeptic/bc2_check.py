#!/usr/bin/env python3
"""Round33 BC2 skeptic pre-comparison checker (single+skeptic; uniform route-B model).

Written after the BC2 contract froze (sha256 28abe377...6b98a, frozen 2026-09-25T04:21:44Z) from the frozen
contract, advisor/selection-bc2.md, advisor/plan.json (vocabulary recorded below, not read at run time) and the
declared premises (AX1/AX2 gates, reports and skeptic reviews; the admitted AX2 calculator; AV1/AV2, AM2, AQ1,
AQ2, AL1 gates; the I1 report; BA1 gate and reports; BB1 gate, reverse report and skeptic review; BB2 gate and
reports; the BA1/BA2/BB1/BB2 contracts for the inherited control semantics), plus the skeptic's own pre-freeze
review bc-contract-review.json (blocking edits and determinations only; its previews_recomputed block is never
read), before reading anything under research/round33/forward/bc2/ (only the file names of its inputs/ were listed
and hashed; the recorded inventory is embedded below) and without reading experts/modern/bc2-targets-proposal.md.
Nothing is imported from any producer, lens or tool; the admitted AX2 calculator (a declared premise) is executed
from its hash-pinned source bytes in a fresh namespace (no import, no cache written). Standard library only.
Every admission Boolean is decided with fractions.Fraction and directed enclosures; floats appear only in labelled
'previews'. Every check and control raises an explicit exception, so python -O cannot disable it. Model-agent
skeptic with correlated ancestry; not human peer review. Human project author: Hruday N M (BUNZEEY).

What is derived here, from the route-B inputs only (J'=29|tau|, 52 first-order faces and 5 groups per site):
  * the route-B incidence and grouping by enumeration (every plaquette in one group; 7 stars and 2 single groups
    meet R; 153 faces charged, 88 meeting R, 16 inside R, 72 straddling; 52 faces and 5 groups per site; support-one
    groups never straddle; first-order R-marginal nonzero exactly for the 16 faces inside R);
  * admissibility as exact rationals: disc rho=64|tau| (self-map 29 rho G(R) <= R, contraction 29 rho G'(R) < 1),
    split weight W=1024 (the same two tests, lambda=2/W < q), the route-A extremes rejected by the self-map test;
  * T_B(rho)=(52 rho/144)/(1-29*352 rho), pinned to the AX1 gate T' at rho=|tau|; K_B=2T_B(64|tau|); the route-B
    every-site common core and the order-versus-distance count on the route-B piece graph (single sites included);
  * the iterated_split constants C_B, c_site,B (covering-chain recursion, per-site charging, W=1024) with direct
    comparisons c1B, c4B, c5B; C'_B, c'_site,B under both assemblies; the exhaustion bound; coarse translations;
    the U_E flip set and the pointwise sign mirror premise; the tau/100 ratios; margins against the frozen targets;
  * the node: the admitted AX2 calculator replayed at its fixed design returns the AX2 gate datum and radius
    exactly; an own re-evaluation (labelled) satisfies r <= R';
  * exact finite fixtures for the traps and a packet validator executing all 52 contract controls as damaging
    mutations with positive cases.

Usage: python3 -B research/round33/skeptic/bc2_check.py --output /absolute/fresh/dir
"""
import argparse
import copy
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = 'research/round33/contracts/bc2.json'
CONTRACT_SHA256 = '28abe3775455087384b3c9dbbb2df67b923e31b964d40efa7ea9787ee8b6b98a'
REVIEW_REL = 'research/round33/skeptic/bc-contract-review.json'  # the skeptic's own pre-freeze review (not a premise)
REVIEW_SHA256 = '339a5f57fe53bb056476299f8cdca388259e445407308ff00960d982a8b01ff9'
CALCULATOR_REL = 'research/round32/forward/ax2/calculator.py'
CALCULATOR_SHA256 = 'f368a3e7e73afc52a14422dd253efbc50fa5d7b59c55b3be569f48043f031f5d'
I1_REL = 'research/round21/forward/i1/report.md'
AX1_F_REL = 'research/round32/forward/ax1/report.md'
EARLIER_CONTRACTS = {
    'research/round33/contracts/ba1.json': '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9',
    'research/round33/contracts/ba2.json': '275ba3b002529b7295d0f8b91dc1cc7a96451e3c7f936ee698a932fdca54fcff',
    'research/round33/contracts/bb1.json': '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018',
    'research/round33/contracts/bb2.json': 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35',
}
PLAN_RECORD = {  # recorded from plan.json as committed with the BC freeze (e4ffdf5); not read at run time
    'sha256_at_bc_freeze_commit': 'f69d45034df2b6c79986cbedcc8cb9473da3b9f2ec9453340cef0d4a412fb264',
    'gate_fields': ['coefficient_cauchy_claimed', 'common_limit_claimed', 'continuum_claim', 'correlation_shift_resolved',
                    'dynamics_level', 'dynamics_limit_identified_claimed', 'finite_box_node_claimed',
                    'finite_box_sign_claimed', 'finite_box_sign_scope', 'gns_dynamics_equality_claimed',
                    'model_is_finite_graph', 'node_certificate_restated_for_limit', 'rate_in_N_claimed',
                    'rate_in_a_claimed', 'resolved_interaction_shift', 'scientific_priority_verified',
                    'sign_certificate_restated_for_limit', 'state_convergence_claimed', 'state_decay_claimed',
                    'state_decay_scope', 'transfers_to_aq', 'translation_invariance_claimed',
                    'translation_invariance_scope', 'uniform_in_time_claimed', 'uniqueness_of_ground_state_claimed',
                    'weak_coupling_claim', 'whole_sequence_claimed', 'whole_sequence_scope'],
    'tier_names_allowed': ['analytic_disc', 'crude_majorant', 'duhamel_inner_f1', 'duhamel_inner_f2', 'exact_first_order',
                           'exponential_lieb_robinson', 'first_order_distance_from_product', 'iterated_split',
                           'polymer_kp', 'polynomial_lieb_robinson', 'weighted_norm'],
    'assembly_values': ['nested_telescoping', 'union_comparison'],
    'forbidden': ['the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
                  'the thermodynamic limit', 'correlation length', 'predicts', 'confirms', 'unique ground state',
                  'a unique limit', 'the unique limit', 'uniqueness of the ground state',
                  'uniquely determines the ground state'],
}
GATES = {
    'research/round32/advisor/ax1-gate.json': '1b8fb152696659439bb01fc7df429fc76fa3132d4936df450d8131256015d177',
    'research/round32/advisor/ax2-gate.json': '1db36627b9eab00915b0cb38a0e9fd9cf9dd4dbf3ceb7eab969336f3f9f44be4',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/av2-gate.json': '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/advisor/aq2-gate.json': '930b697db343ffd261c303c34e6ddd8c6e9c753ee6707931c55dc4171ee47575',
    'research/round29/advisor/al1-gate.json': 'e415203cc6b6ebca6cea5fcd1230a7eb0e20b7ab2d2e6c99dc8aa2dd3052a75b',
    'research/round33/advisor/ba1-gate.json': '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    'research/round33/advisor/bb1-gate.json': '18141fea672e5bae09024a5fddc56ea7102aae56ecca16fbb30d67a1354a3827',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
}
OBSERVED_INPUTS = {  # find + sha256 over research/round33/forward/bc2/inputs (names only), 2026-09-25; 42 files
    'AGENTS.md': '870e1a6b1ff81d6e09888d7084dada2dfdb8128048d97857d9c6b1ffce1b9285',
    'research/round21/forward/i1/report.md': '836a4c7d421f0ddf3589c159d2f057839421532c88157a054a61b51c25c781a9',
    'research/round29/advisor/al1-gate.json': 'e415203cc6b6ebca6cea5fcd1230a7eb0e20b7ab2d2e6c99dc8aa2dd3052a75b',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/advisor/aq2-gate.json': '930b697db343ffd261c303c34e6ddd8c6e9c753ee6707931c55dc4171ee47575',
    'research/round29/forward/am2/report.md': '1b58fb9c1a199f06b156d04c2a9e89f34ba63cf675a5f7c8bfc25bb568e4e019',
    'research/round29/forward/aq1/report.md': 'b091266f5db009fa967a2adea352fa1b190193cc4bcdc6c4c207e5872fc51da3',
    'research/round29/reverse/am2/report.md': 'e7313e6a591bacbf37b65c84d57049d2f05a67222cddb8073286e2cd4143d06e',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/av2-gate.json': '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33',
    'research/round32/advisor/ax1-gate.json': '1b8fb152696659439bb01fc7df429fc76fa3132d4936df450d8131256015d177',
    'research/round32/advisor/ax2-gate.json': '1db36627b9eab00915b0cb38a0e9fd9cf9dd4dbf3ceb7eab969336f3f9f44be4',
    'research/round32/forward/av1/report.md': '7f86e941933913584de2b9e542359e4a3b3c275c1bc8623dca3c367d88437353',
    'research/round32/forward/ax1/report.md': '2ba5e8360432755e87dab5a2c67c53617ce34494a394c3520e69818e20ce7a38',
    'research/round32/forward/ax2/calculator.py': 'f368a3e7e73afc52a14422dd253efbc50fa5d7b59c55b3be569f48043f031f5d',
    'research/round32/forward/ax2/report.md': '225fee6aad1f90bdd53bfdf0b9ce2a55027c4b05dbdb7e799f936d2c2b801ae6',
    'research/round32/reverse/av1/report.md': '02cd908e89b36a1bf377dcbb8f5bf0bdfdd3272375a95f898e71e8fc4aa16d65',
    'research/round32/reverse/ax1/report.md': '9ffe3b4af78537a66e194c0d3669edd8f9a5df4a0069bd1d82bea13dad349e8e',
    'research/round32/skeptic/ax1.md': '9729b61526c6c339f3d0a5793a35877fa9b93bf575d0aa4a25154d2f5abffda3',
    'research/round32/skeptic/ax2.md': '1217f61ae4cdc610cef0d3b7483318dff5ef04c5b93df8cb6d169bbe0fe0cef0',
    'research/round33/advisor/ba1-gate.json': '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    'research/round33/advisor/bb1-gate.json': '18141fea672e5bae09024a5fddc56ea7102aae56ecca16fbb30d67a1354a3827',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
    'research/round33/advisor/selection-bc2.md': '439841fb426627e1529bdc02dfeef487d5b49d4fa4cac41477591520b59cd784',
    'research/round33/contracts/ba1.json': '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9',
    'research/round33/contracts/ba2.json': '275ba3b002529b7295d0f8b91dc1cc7a96451e3c7f936ee698a932fdca54fcff',
    'research/round33/contracts/bb1.json': '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018',
    'research/round33/contracts/bb2.json': 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35',
    'research/round33/contracts/bc2.json': '28abe3775455087384b3c9dbbb2df67b923e31b964d40efa7ea9787ee8b6b98a',
    'research/round33/forward/ba1/report.md': 'd8ed5bfa780b95a57e5ba822b81f0fea5f71aaa7ea1a01bb4dbecb0d417aa769',
    'research/round33/forward/bb2/report.md': 'b925ad0720ecb24aeb9483401fe4cf299e713e1793bc2812752d5eca2d723c23',
    'research/round33/methods/historical-physics-panel/SKILL.md': 'a2b366bc661794ee89c29233d0887868b60c0853c85ec136e0529b6f1d5e223a',
    'research/round33/methods/newton-analysis-synthesis/SKILL.md': '2fa3dab9b2420d157457ad3ccaeb0723fb1952871be3e6140dcd3d3c9346ccef',
    'research/round33/methods/paired-physics-research/SKILL.md': '01cda7ee8f8e3eb65c68b0ac6ff0d9e87198f57ea2d997d810d7907b85f4278d',
    'research/round33/methods/paired-physics-research/references/complete-residual-and-error-scope.md': '9e387df64ae05738e740d2ff65973cef0672530e64344ab9e730a139b81b435d',
    'research/round33/methods/qeg-research-advisor/references/round32-state-lemma-and-window.md': '78dc75607920ae799331d6b27b725cba54139d9aceaf04ccbac32a20205a4977',
    'research/round33/methods/tesla-mechanism-resonance/SKILL.md': '81f6d760b3aa45d32db4ae31a3a3c9bec5e1d662e42529b5ae21a220deeb07c3',
    'research/round33/reverse/ba1/report.md': 'a986c205542376c2ad5058cdf88e082abe9c12eeba87b052abf3ad9cefebbb86',
    'research/round33/reverse/bb1/report.md': '7e34638de77c4e76410cc9982a91b44f49017d9a5ad8471a232904cb0d244e37',
    'research/round33/reverse/bb2/report.md': '6f48706c25ff25bce2ed8db40433416624d355797ec11ee5f34b4a3b7a4867a7',
    'research/round33/skeptic/bb1.md': '478582f2106e4f1ab623967602dc561a006eec1b1477e04aff2a93221d635715',
}
ISOLATION_FORBIDDEN_PREFIXES = ('research/round33/forward/bc1/', 'research/round33/forward/bc2/',
                                'research/round33/experts/', 'research/round33/skeptic/bc-contract-review',
                                'research/round33/advisor/plan.json', 'research/round33/advisor/deliberation',
                                'research/round33/advisor/panel')

MODEL_ID = 'AQ_uniform_routeB'
TAU = F(1, 10 ** 8)
Q = F(1, 64)
R_BALL = F(1, 64)
G_R, GP_R = F(148, 7), F(352)
J_B, FACES_B, GROUPS_B = 29, 52, 5          # route-B per-site sum (|tau| units), first-order faces, groups per site
J_A, FACES_A, GROUPS_A = 28, 49, 4          # route-A values (rejected under a route-B label)
W_SPLIT = 1024
DISC_OVER_TAU = 64
DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN, E_Z = (0, 0, 0), (0, 0, 1)
R_COVER = (ORIGIN, E_Z)
LABEL = 'uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling (g^4=9.6x10^9)'
GROUPING = 'whole stars phi_b (21 omitted faces, norm 7|tau|) and single-factor groups psi_b (3 selected faces, support {b})'
CLOCK = 's=alpha*t_E/hbar (node s=1); theta=alpha*t/hbar (inherited route-B limit dynamics only)'
TOPOLOGY = {'states': 'trace norm on B(H_Y)', 'representations': 'GNS strong'}
COMPARISONS = ('c1B', 'c4B', 'c5B')
UNIFORM_IN = 'N (volume) at fixed spacing'
RATE_UNIT = 'per coarse step at fixed spacing (a coarse step is (4a,2a,a)); not a length scale'
CUTOFF_ORDER = 'each Q_L uniformly in L; then L to infinity at fixed N (AV1 F20-F23, route-B gap 1/2); then N'
AX1_INHERITED = 'AX1 gate route-B re-instantiation'
SUB_LABELS = ['convergence_of_named_constructions', 'certificate_restated_for_limit', 'reference_unresolved',
              'static_not_dynamic']
REQUIRED_FIXTURES = ('coefficient_decay_not_marginal_decay', 'second_order_propagation', 'straddling_supports',
                     'normalization_spectators', 'global_fidelity', 'split_trace_and_lipschitz',
                     'split_per_site_charging', 'cutoff_eckart', 'cutoff_limit_order', 'fixed_versus_moving_vector',
                     'zero_free_region', 'outside_vector_not_ground_state', 'support_one_group',
                     'whole_sequence_versus_subsequence', 'flip_compression', 'region_factor_route_b')

ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state', 'uniquely determines the ground state',
    'the thermodynamic limit', 'correlation length',
]
EXTRA_FORBIDDEN = ['uniform in the lattice spacing', 'exponential decay in N', 'boundary conditions are irrelevant']
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


def fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def exp_bracket(x, n=40):
    """[lo, hi] for e^x, 0 <= x <= 8: Taylor partial sum and the geometric remainder bound."""
    x = F(x)
    if not (0 <= x <= 8):
        raise CheckFailure('exp domain')
    s = sum((x ** k / fact(k) for k in range(n + 1)), F(0))
    return s, s + x ** (n + 1) / fact(n + 1) / (1 - x / (n + 2))


def atan_bracket(z, terms=60):
    """Alternating partial sums of arctan for 0 < z <= 1/5: consecutive sums bracket the value."""
    s, prev = F(0), None
    for k in range(terms + 1):
        prev = s
        s += (-1) ** k * z ** (2 * k + 1) / (2 * k + 1)
    return (min(s, prev), max(s, prev))


def pi_bracket():
    a = atan_bracket(F(1, 5))
    b = atan_bracket(F(1, 239))
    return 16 * a[0] - 4 * b[1], 16 * a[1] - 4 * b[0]


def get_path(doc, path):
    cur = doc
    for part in re.findall(r'\.([A-Za-z_0-9]+)|\[(\d+)\]', path[1:]):
        key, idx = part
        cur = cur[int(idx)] if idx else cur[key]
    return cur


def has_key_path(doc, path):
    try:
        get_path(doc, path)
    except (KeyError, IndexError, TypeError):
        return False
    return True


# ---------------------------------------------------------------- route-B constants (route-B inputs only)
PINNED_T_PRIME = {}


def T_B(rho, faces=FACES_B, j=J_B):
    """Route-B circle bound (52 first-order faces, per-site sum 29|z|): (faces rho/144)/(1 - j rho G'(R)).
    Admissibility is checked on every call: self-map j rho G(R) <= R and contraction j rho G'(R) < 1."""
    rho = F(rho)
    if j * rho * G_R > R_BALL or j * rho * GP_R >= 1:
        raise CheckFailure('disc radius or weight outside the route-B self-map/contraction')
    val = F(faces, 144) * rho / (1 - j * rho * GP_R)
    if rho == TAU and PINNED_T_PRIME and faces == FACES_B and j == J_B and val != PINNED_T_PRIME['T']:
        raise CheckFailure('T_B(|tau|) differs from the AX1 gate T\'')
    return val


def T_crude(rho, j=J_B):
    return j * F(rho) * G_R


def split_constants(abs_tau, w=W_SPLIT, tier='exact_first_order', faces=FACES_B, j=J_B):
    """BB1-reverse covering-chain recursion re-instantiated with route-B inputs.
    t_0 = 2T_B(|tau|), t_W = 2T_B(W|tau|) (majorants of a comparison); c_1, c_2 of the chain closure;
    beta* = c_1/(1-c_2); S_lambda the l-infinity lattice sum at x = lambda/q = (2/W)/q."""
    if tier == 'exact_first_order':
        t0, tw = 2 * T_B(abs_tau, faces, j), 2 * T_B(w * abs_tau, faces, j)
    else:
        t0, tw = 2 * T_crude(abs_tau, j), 2 * T_crude(w * abs_tau, j)
    lam = F(2, w)
    if not lam < Q:
        raise CheckFailure('lambda >= q: lattice sum diverges')
    if 8 * tw >= 1 or t0 >= 1:
        raise CheckFailure('chain recursion does not close')
    c1 = 4 * t0 * tw + (4 * tw + 4 * t0 * tw / (1 - t0)) / (1 - 8 * tw)
    c2 = 16 * t0 * tw + 16 * t0 * tw / ((1 - t0) * (1 - 8 * tw))
    if c2 >= 1:
        raise CheckFailure('chain recursion does not close (c_2)')
    beta = c1 / (1 - c2)
    x = lam / Q
    s_lam = 1 + 24 * x * (1 + x) / (1 - x) ** 3 + 2 * x / (1 - x)
    return {'t0': t0, 'tW': tw, 'c1': c1, 'c2': c2, 'beta': beta, 'S_lambda': s_lam, 'lambda': lam,
            'per_level_factor': 8 * tw}


def route_b_constants(abs_tau, tier='exact_first_order', faces=FACES_B, j=J_B):
    rho = DISC_OVER_TAU * abs_tau
    k = 2 * T_B(rho, faces, j) if tier == 'exact_first_order' else 2 * T_crude(rho, j)
    sp = split_constants(abs_tau, tier=tier, faces=faces, j=j)
    cs = k * (2 + sp['beta'] * sp['S_lambda'])
    c = cs * (1 + Q)
    return {'K_B': k, 'c_site_B': cs, 'C_B': c, 'C_prime_B_nested': c / (1 - Q), 'C_prime_B_union': c,
            'c_prime_site_B_nested': cs / (1 - Q), 'c_prime_site_B_union': cs,
            'exhaustion_nested': cs + cs / (1 - Q), 'exhaustion_union': 2 * cs, 'split': sp}


# ---------------------------------------------------------------- geometry (I1 classes; route-B grouping)
def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def sub(a, b):
    return tuple(i - j for i, j in zip(a, b))


def dinf(p, r):
    return max(abs(x - y) for x, y in zip(p, r))


def norm_inf(p):
    return max(abs(x) for x in p)


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
            out.append({'orient': a + c, 'r': r, 's': s, 'rel': owner_set(p, a, c), 'selected': is_selected(p, a, c),
                        'base': p, 'a': a, 'c': c})
    return out


CLASSES = anchor_classes()
OMITTED = [k for k in CLASSES if not k['selected']]
SELECTED = [k for k in CLASSES if k['selected']]


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


def route_b_groups(sites):
    """Route-B retention on a finite complete-factor volume: stars b+S inside the volume, every single group."""
    groups = {}
    for b in sites:
        if all(add(b, s) in sites for s in S_STAR):
            groups[('star', b)] = [frozenset(add(b, d) for d in k['rel']) for k in OMITTED]
        groups[('single', b)] = [frozenset([b]) for _ in SELECTED]
    return groups


def source_sites(vol_a, vol_b):
    ga, gb = route_b_groups(vol_a), route_b_groups(vol_b)
    src = set()
    for key in set(ga) ^ set(gb):
        faces = ga.get(key) or gb.get(key)
        for own in faces:
            src |= own
    return src


# ---------------------------------------------------------------- qubit algebra (finite fixtures)
def mask_of(*sites):
    s = 0
    for i in sites:
        s |= 1 << i
    return s


def vac(n):
    v = [F(0)] * (2 ** n)
    v[0] = F(1)
    return v


def cre(vec, mask, amp):
    out = [F(0)] * len(vec)
    for s, x in enumerate(vec):
        if not (s & mask) and x != 0:
            out[s | mask] += amp * x
    return out


def state(n, creations):
    v = vac(n)
    for mask, amp in creations:
        c = cre(v, mask, amp)
        v = [x - y for x, y in zip(v, c)]
    return v


def ip(u, v):
    return sum((a * b for a, b in zip(u, v)), F(0))


def rdm(vec, sites, n):
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

    raw = [[sum((vec[idx(a, r_)] * vec[idx(b, r_)] for r_ in range(2 ** len(rest))), F(0)) for b in range(2 ** k)]
           for a in range(2 ** k)]
    z = sum(raw[a][a] for a in range(2 ** k))
    return [[x / z for x in row] for row in raw]


def psd(mat):
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


def sqrt_lo_hi(x, scale=10 ** 15):
    x = F(x)
    r = isqrt(x.numerator * x.denominator * scale * scale)
    lo, hi = F(r, x.denominator * scale), F(r + 1, x.denominator * scale)
    if not (lo * lo <= x <= hi * hi):
        raise CheckFailure('sqrt bracket')
    return lo, hi


def trace_norm_2x2(mat):
    p, r_, s = mat[0][0], mat[0][1], mat[1][1]
    if p * s - r_ * r_ >= 0:
        v = abs(p + s)
        return v, v
    return sqrt_lo_hi((p - s) ** 2 + 4 * r_ * r_)


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


def has_float(value):
    if isinstance(value, float):
        return True
    if isinstance(value, dict):
        return any(has_float(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(has_float(v) for v in value)
    return False


def packet_digest(pk):
    body = json.dumps({'inputs': sorted(pk['inputs']), 'controls': pk['controls']}, sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()


def rebind(pk):
    pk['freeze_digest'] = packet_digest(pk)
    return pk


def run_calculator(fixed=True, tau='1/100000000'):
    """Execute the hash-pinned admitted AX2 calculator from its source bytes (no import, no cache)."""
    src = (ROOT / CALCULATOR_REL).read_bytes()
    if hashlib.sha256(src).hexdigest() != CALCULATOR_SHA256:
        raise CheckFailure('calculator hash')
    ns = {'__name__': 'ax2_calculator_replay', '__file__': CALCULATOR_REL}
    exec(compile(src, CALCULATOR_REL, 'exec'), ns)
    return ns['certify'](tau=tau, fixed_design=fixed), ns


# ---------------------------------------------------------------- packet validator
def validate(pk, c):
    if pk['contract_sha256'] != CONTRACT_SHA256:
        raise Rejected('contract hash')
    if pk['freeze_digest'] != packet_digest(pk):
        raise Rejected('coherent evidence tampering: freeze digest')
    if sorted(pk['inputs']) != sorted(c['declared_inputs']):
        extra = sorted(set(pk['inputs']) - set(c['declared_inputs']))
        if any(p.startswith(pre) for p in extra for pre in ISOLATION_FORBIDDEN_PREFIXES):
            raise Rejected('coherent evidence tampering: undeclared read')
        raise Rejected('coherent evidence tampering: snapshot inventory')
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
    # model (route B)
    if (pk['model_id'] != MODEL_ID or pk['triple'] != ['tau/24', 'tau/24', 'tau/24'] or pk['tau'] != c['tau']
            or pk['signs'] != ['+', '-'] or pk['group'] != 'SU(2)' or pk['grouping'] != GROUPING
            or pk['model_is_finite_graph'] is not False or pk['boundary'] != 'centered whole-star-plus-single-group boxes'):
        raise Rejected('changed model relabelled')
    if pk['label'] != LABEL:
        raise Rejected('changed model relabelled: label')
    par = pk['parameters']
    for key in ('metric', 'weights', 'window', 'clock', 'node', 'N_min', 'cutoff'):
        if key not in par or par[key] in (None, ''):
            raise Rejected('parameters must declare metric weights window: ' + key)
    if par['metric'] != c['metric'] or par['window'] != c['window']:
        raise Rejected('changed model relabelled: metric or window')
    if pk['clock'] != CLOCK or pk['reference_energy'] != 3:
        raise Rejected('wrong delta alpha hbar clock')
    if pk['u_over_theta'] != F(1, 8) or pk['window_labelled_in'] != 'theta':
        raise Rejected('wrong delta alpha hbar clock: normalized u without conversion')
    if pk['clock_per_comparison'] != {k: CLOCK for k in COMPARISONS} \
            or pk['coupling_per_comparison'] != {k: c['tau'] for k in COMPARISONS}:
        raise Rejected('common clock')
    if pk['topology'] != TOPOLOGY or pk['fixtures'].get('fixed_versus_moving_vector', {}).get('exhibited') is not True:
        raise Rejected('topology named')
    fx = pk['fixtures']
    for name in REQUIRED_FIXTURES:
        row = fx.get(name)
        if row is None or row.get('exhibited') is not True:
            raise Rejected('fixture missing: ' + name)
        if row.get('model_is_finite_graph') is not True or row.get('transfers_to_aq') is not False:
            raise Rejected('fixture label: ' + name)
    # route-B inputs
    inp = pk['route_b_inputs']
    if inp['J_prime'] != J_B or inp['faces_per_factor'] != FACES_B or inp['groups_per_site'] != GROUPS_B:
        raise Rejected('route b constants not route a: inputs')
    if inp['T_B_at_tau'] != c['T_prime']:
        raise Rejected('route b constants not route a: T_B pin')
    if any(v in c['route_a_values'] for v in inp['values_used']):
        raise Rejected('route b constants not route a: route-A value used')
    # admissibility
    ad = pk['admissibility']
    if ad['declared_before_constants'] is not True:
        raise Rejected('rate constant pair prefrozen: weights declared after constants')
    rho, w = ad['disc_radius'], ad['W']
    for label, r_ in (('disc', rho), ('split weight', w * c['tau'])):
        if not (J_B * r_ * G_R <= R_BALL and J_B * r_ * GP_R < 1):
            raise Rejected('disc admissible under J prime: ' + label + ' fails the route-B self-map or contraction')
    if rho != DISC_OVER_TAU * c['tau'] or w != W_SPLIT or ad['lambda'] != F(2, w) or ad['q'] != Q:
        raise Rejected('rate constant pair prefrozen: rho, W, lambda or q not the frozen values')
    if ad['q_per_N'] is not False or ad['optimized_after_evaluation'] is not False:
        raise Rejected('rate constant pair prefrozen: optimized')
    if not (ad['lambda'] < Q):
        raise Rejected('rate constant pair prefrozen: lambda not below q')
    if ad['admissibility_per_site_sum'] != J_B:
        raise Rejected('disc admissible under J prime: tested under the route-A per-site sum')
    if ad['route_a_extremes_rejected_by'] != 'self-map' or ad['route_a_extremes_rejected'] is not True:
        raise Rejected('disc admissible under J prime: route-A extremes')
    # incidence
    inc = pk['incidence']
    if inc != c['incidence']:
        if inc.get('inside_R') != c['incidence']['inside_R']:
            raise Rejected('route b first order marginal')
        raise Rejected('route b constants not route a: incidence')
    if pk['support_one'] != {'straddle': False, 'clipped': False, 'first_order_creation_nonzero': True,
                             'piece_graph': 'cost one order, zero distance'}:
        raise Rejected('support one groups')
    if pk['first_order_marginal'] != {'faces_inside_R': 16, 'omitted_owner_R': 10, 'selected_single_sites': 6,
                                      'straddling_zero': 72}:
        raise Rejected('route b first order marginal')
    if pk['selected_face'] != {'site_energy': 24, 'kept_for_L_at_least': 24}:
        raise Rejected('selected face site energy')
    # coefficient input
    ci = pk['coefficient_input']
    if ci['route'] != 'analytic_disc' or ci['tier'] != 'exact_first_order':
        raise Rejected('tier mixing: coefficient input route')
    if ci['every_site'] is not True or ci['far_site_input'] != 'route-B every-site form':
        raise Rejected('every site coefficient input: R-only input at far sites')
    if ci['proved_in_full'] is not True or ci['cited_as_admitted'] is not False or ci['source'] != 'route-B disc lemma (this packet)':
        raise Rejected('every site coefficient input: cited instead of proved')
    if ci['exponent'] != '(N-|u|_inf)_+':
        raise Rejected('every site coefficient input: exponent')
    if ci['zero_free_region'] is not None or ci['density_analytic_claimed'] is not False:
        raise Rejected('zero free region required')
    if ci['untruncated_coefficients_claimed'] is not False or ci['uniform_in_L'] is not True:
        raise Rejected('cutoff uniform then removed: coefficients')
    if ci['lipschitz_as_decay'] is not None:
        raise Rejected('global lipschitz not decay')
    # split
    sp = pk['split']
    if sp['route'] != 'iterated_split':
        raise Rejected('tier mixing: density route')
    if sp['charging'] != 'per_site':
        raise Rejected('fixture split lipschitz and trace: charging')
    if sp['trace_N_ge_1_checked'] is not True or sp['lipschitz_checked'] is not True:
        raise Rejected('fixture split lipschitz and trace: unchecked')
    if sp['straddling_included'] is not True or sp['straddling_charged_beyond_first_order'] is not True \
            or sp['normalization'] != 'exact ratio (Tr N_c >= 1)':
        raise Rejected('normalization couples supports')
    if sp['outside_gap_argument'] is not False:
        raise Rejected('outside vector not ground state')
    if sp['locality_mechanism'] != 'coefficient input and covering-chain recursion':
        if sp['locality_mechanism'] == 'global overlap':
            raise Rejected('global fidelity orthogonality catastrophe')
        raise Rejected('coefficient decay not marginal decay')
    if sp['lipschitz_decay_factor'] is not None:
        raise Rejected('global lipschitz not decay')
    if sp['second_order_derivative'] != c['second_order_derivative']:
        raise Rejected('fixture second order propagation')
    if sp['state_decay_inferred_from_coefficients'] is not False:
        raise Rejected('coefficient decay not marginal decay')
    # constants
    ref = route_b_constants(c['tau'])
    want = {'K_B': ('exact_first_order', 'analytic_disc', None), 'C_B': ('exact_first_order', 'iterated_split', None),
            'c_site_B': ('exact_first_order', 'iterated_split', None),
            'C_prime_B': ('exact_first_order', 'iterated_split', 'assembly'),
            'c_prime_site_B': ('exact_first_order', 'iterated_split', 'assembly')}
    seen = set()
    for rec in pk['constants']:
        if rec['tier'] not in ('exact_first_order', 'crude_majorant'):
            raise Rejected('tier mixing: tier vocabulary')
        if rec['route'] in PLAN_RECORD['assembly_values']:
            raise Rejected('tier mixing: assembly recorded as a route')
        if rec['route'] not in ('analytic_disc', 'iterated_split'):
            raise Rejected('tier mixing: route')
        if rec.get('hypothesis_source') is not None:
            raise Rejected('tier mixing: hypothesis source')
        if rec.get('labelled') is True:
            continue
        name = rec['id']
        if name not in want:
            raise Rejected('tier mixing: unknown constant')
        tier, route, asm = want[name]
        if rec['tier'] != tier or rec['route'] != route:
            raise Rejected('tier mixing: ' + name)
        if asm and rec.get('assembly') not in PLAN_RECORD['assembly_values']:
            raise Rejected('tier mixing: assembly field')
        if not asm and rec.get('assembly') is not None:
            raise Rejected('tier mixing: assembly on a per-comparison constant')
        if rec['q'] != Q or rec['target'] != c['targets'][name]:
            raise Rejected('rate constant pair prefrozen: ' + name)
        if rec['value'] in c['route_a_values']:
            raise Rejected('route b constants not route a: gate value under a route-B label')
        key = {'C_prime_B': 'C_prime_B_' + ('nested' if rec.get('assembly') == 'nested_telescoping' else 'union'),
               'c_prime_site_B': 'c_prime_site_B_' + ('nested' if rec.get('assembly') == 'nested_telescoping'
                                                      else 'union')}.get(name, name)
        if rec['value'] < ref[key]:
            if name in ('C_prime_B', 'c_prime_site_B') and rec.get('assembly') == 'union_comparison' \
                    and rec.get('union_means') != 'one direct c4B comparison':
                raise Rejected('direct comparison required: union assembly')
            raise Rejected('coherent evidence tampering: constant below the derivable value')
        if rec['meets_target'] != (rec['value'] <= rec['target']):
            raise Rejected('insufficient verdict retained: target flag')
        if rec['signs'] != ['+', '-']:
            raise Rejected('changed model relabelled: one sign')
        seen.add(name)
    if seen != set(want):
        raise Rejected('rate constant pair prefrozen: constant missing')
    for rec in pk['constants']:
        if rec.get('labelled') is True and rec.get('used_for_target') is True:
            raise Rejected('direct comparison required: labelled value used for a target')
    # comparisons
    comps = pk['comparisons']
    if sorted(comps) != sorted(COMPARISONS):
        raise Rejected('direct comparison required: comparison set')
    for name, row in comps.items():
        if row['route'] != 'direct':
            raise Rejected('direct comparison required: ' + name)
        if row['signs'] != ['+', '-'] or row['regimes'] != ['Q_L', 'untruncated']:
            raise Rejected('cutoff uniform then removed: comparison regimes')
    reg = pk['region']
    if reg['Y_dependence'] != '|Y| e^{|Y|/10^8}' or reg['exponent'] != 'd_Y = N - max_y |y|_inf' \
            or reg['domain'] != 'finite complete-factor regions Y inside Lambda_N':
        raise Rejected('region constant scales with Y')
    if reg['R_constant_reused'] is not False:
        raise Rejected('region constant scales with Y: R constant reused on Y')
    cut = pk['cutoff']
    if cut['order'] != CUTOFF_ORDER or cut['uniform_in_L'] is not True:
        raise Rejected('cutoff uniform then removed')
    if cut['limits_swapped'] is not False:
        raise Rejected('cutoff limit order')
    if cut['vector_convergence'] is not True or cut['eigenvalue_only'] is not False:
        raise Rejected('cutoff vector removal')
    if cut['gap'] != 'route-B gap 1/2 (AX1)':
        raise Rejected('cutoff uniform then removed: gap source')
    # whole sequence
    ws = pk['whole_sequence']
    if ws['quantifier'] != 'all M greater than N' or ws['limit_kind'] != 'whole sequence':
        raise Rejected('subsequence versus whole sequence')
    if ws['limit_existence'] != 'Cauchy bound and completeness of the trace class':
        raise Rejected('cauchy estimate not compactness')
    if ws['regions'] != 'every finite complete-factor region Y inside Lambda_N':
        raise Rejected('region constant scales with Y: whole sequence')
    # exhaustion (item 2a)
    ex = pk['exhaustion']
    if ex['via'] != 'one direct c5B comparison of V_k with Lambda_{N_k} and item 1' \
            or ex['constant'] != 'c_site,B + c_prime_site,B':
        raise Rejected('exhaustion within prescription only: bound')
    if ex['prescription'] != 'route-B volumes: stars inside the volume, every single group kept' \
            or ex['boundary_comparison_claimed'] is not False:
        raise Rejected('exhaustion within prescription only')
    # sign mirror (item 2b)
    mi = pk['mirror']
    if mi['kind'] != 'pointwise on every finite region' or mi['premise'] != c['mirror_premise']:
        raise Rejected('sign mirror pointwise')
    if mi['real_g'] is not False or mi['counted_as_second_coupling'] is not False:
        raise Rejected('sign mirror pointwise: second coupling')
    # identification (item 3)
    idf = pk['identification']
    if idf['before_inheritance'] is not True:
        raise Rejected('identification before inheritance route b')
    if idf['identified_with'] != 'every AQ1-type subsequential state of the AX1 construction' \
            or idf['on'] != 'every finite region':
        raise Rejected('limit identified with aq1 limits')
    if idf['inherited_list'] != AX1_INHERITED:
        raise Rejected('limit identified with aq1 limits: inherited list')
    # translation (item 4)
    tr = pk['translation']
    if tr['separate_item'] is not True or tr['from_nested_cubes_only'] is not False \
            or tr['input'] != 'one direct comparison c5B' or tr['union_two_step_as_bound'] is not False:
        raise Rejected('translation invariance separate item')
    if tr['bound'] != 'C_B q^(N-|v|_inf-1)' or tr['N_condition'] != 'N >= |v|_inf+2':
        raise Rejected('translation invariance separate item: bound')
    if tr['non_coarse'] != 'no claim' or tr['non_coarse_reason'] is not None:
        raise Rejected('non coarse translation no claim')
    # node (item 5)
    nd = pk['node']
    if nd['s'] != [1] or nd.get('grid') is not None:
        raise Rejected('node values unchanged: node')
    if nd['datum'] != c['ax2']['d'] or nd['radius'] != c['ax2']['R']:
        raise Rejected('node values unchanged')
    cr = nd['calculator_replay']
    if cr['sha256'] != CALCULATOR_SHA256 or cr['reads_undeclared'] is not False:
        raise Rejected('node values unchanged: replay premise')
    if cr['datum'] != c['ax2']['d'] or cr['radius_outward'] != c['ax2']['R']:
        raise Rejected('node values unchanged: replay values')
    if nd['slope'] != '51|tau|/4' or nd['state_term'] != c['D_prime']:
        raise Rejected('node values unchanged: slope or state term')
    oc = nd['own_cross_check']
    if oc['labelled'] is not True or oc['headline'] is not False or not (oc['value'] <= c['ax2']['R']):
        raise Rejected('node values unchanged: own re-evaluation')
    if nd['region_form_proved'] is not True:
        raise Rejected('region form load bearing for node')
    if nd['reference_inside'] is not True or 'reference_unresolved' not in nd['sub_labels'] \
            or nd['shift_claimed'] is not False:
        raise Rejected('reference unresolved retained route b')
    if nd['finite_box_node_convergence_claimed'] is not False:
        raise Rejected('no finite box node convergence')
    if nd['minus_tau'] != 'mirror replay of the same |tau| formula':
        raise Rejected('sign mirror pointwise: node')
    # dynamics, common limit, model crossing
    if pk['dynamics'] != {'route_b_dynamics_claimed': False, 'dynamics_level_exported': False,
                          'correlation_functions_claimed': False}:
        raise Rejected('no route b dynamics claim')
    if pk['common_limit'] != {'claimed': False, 'families': 1, 'identified_with_all_contained': False}:
        raise Rejected('one family no common limit')
    if pk['model_crossing'] != {'identified_with_zero_selected_limit': False, 'bb_constants_applied': False,
                                'transfer_to_zero_selected': False}:
        raise Rejected('model crossing rejected')
    # rates, scaling, verdict
    for r in pk['rates']:
        if not r.get('range'):
            raise Rejected('rate range stated')
        if r.get('source') == 'BB2':
            raise Rejected('rate range stated: rate transferred from BB2')
        if r['what'] == 'correlation functions':
            raise Rejected('rate range stated: correlation rate claimed')
    for text in pk['statements']:
        if re.search(r'O\(1/N\)', text):
            raise Rejected('rate range stated: O(1/N)')
    if pk['uniform_in'] != UNIFORM_IN:
        raise Rejected('uniform in N not in a')
    if pk['rate_unit'] != RATE_UNIT or pk['rate_in_a'] is not False:
        raise Rejected('decay rate in N not a')
    if pk['brackets'] != c['brackets']:
        raise Rejected('tau scaling exponent: bracket changed')
    for name, ratio in pk['scaling'].items():
        lo, hi = c['bracket_values'][name]
        if not (lo <= ratio <= hi):
            raise Rejected('tau scaling exponent: ' + name)
    met = {r['id']: r['meets_target'] for r in pk['constants'] if not r.get('labelled')}
    if pk['verdict'] == 'accepted_within_scope' and not all(met.values()):
        raise Rejected('insufficient verdict retained')
    if pk['verdict'] != 'accepted_within_scope' and not pk.get('dominating_term'):
        raise Rejected('insufficient verdict retained: dominating term')
    if pk['retuned'] is not False:
        raise Rejected('insufficient verdict retained: retuned')
    # wording
    for text in strings([pk['statements'], pk['sentence']]):
        if placeholder_spans(text):
            raise Rejected('placeholder span')
    for text in pk['statements']:
        if re.search(r'\buniform in a\b', text, re.I) and not NEGATION.search(text):
            raise Rejected('uniform in N not in a: phrasing')
        hits = affirmative_hits(text, c['forbidden'], c['sentence'])
        if hits:
            if any('unique' in h or 'infinite-volume' in h or 'thermodynamic' in h for h in hits):
                raise Rejected('named construction not uniqueness: forbidden phrasing ' + hits[0])
            if any(h in ('uniform in a', 'uniform in the lattice spacing') for h in hits):
                raise Rejected('uniform in N not in a: phrasing')
            if any(h in ('boundary independent',) for h in hits):
                raise Rejected('exhaustion within prescription only: phrasing')
            raise Rejected('negation aware phrase scan: ' + hits[0])
    if pk['sentence'] != c['sentence'] or pk['sentence_count'] != 1:
        raise Rejected('mandatory sentence template')
    if pk['sub_labels'] != SUB_LABELS:
        raise Rejected('changed model relabelled: sub-labels')
    gf = pk['gate_fields']
    if 'dynamics_level' in gf:
        raise Rejected('no route b dynamics claim: dynamics_level exported')
    for key, want_v in sorted(c['gate_fields'].items()):
        if gf.get(key) != want_v:
            if key == 'uniqueness_of_ground_state_claimed':
                raise Rejected('named construction not uniqueness: ' + key)
            if key == 'common_limit_claimed':
                raise Rejected('one family no common limit: ' + key)
            if key == 'rate_in_a_claimed':
                raise Rejected('decay rate in N not a: ' + key)
            if key == 'resolved_interaction_shift':
                raise Rejected('reference unresolved retained route b: ' + key)
            if key in ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified'):
                raise Rejected('no priority or continuum claim: ' + key)
            raise Rejected('gate field: ' + key)
    if sorted(gf) != sorted(c['gate_fields']):
        raise Rejected('gate field: extra or missing field')
    for name in c['error_terms']:
        entry = pk['error_terms'].get(name)
        if entry is None:
            raise Rejected('error term missing: ' + name)
        if entry.startswith('not_applicable') and len(entry) <= len('not_applicable') + 3:
            raise Rejected('error term missing: not_applicable without a reason (' + name + ')')
    return True


# ---------------------------------------------------------------- execute
def execute():
    # 1. provenance ------------------------------------------------------------------------------------------------
    cb = (ROOT / CONTRACT_REL).read_bytes()
    c_sha = hashlib.sha256(cb).hexdigest()
    need(c_sha == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=c_sha)
    con = json.loads(cb)
    par, pre = con['parameters'], con['preregistration']
    need(con['status'] == 'frozen_before_production' and con['id'] == 'BC2' and con['direction'] == 'single+skeptic'
         and con['producers'] == ['forward'] and pre['model_id'] == MODEL_ID
         and pre['selected_triple_alpha_units'] == ['tau/24', 'tau/24', 'tau/24']
         and F(pre['tau']['value']) == TAU and con['selected_after'] == 'research/round33/advisor/bb2-gate.json',
         'contract_frozen_single_direction', frozen_at=con['frozen_at'])
    for rel, want in sorted(GATES.items()):
        if sha(rel) != want:
            raise CheckFailure('gate hash ' + rel)
    for rel, want in sorted(EARLIER_CONTRACTS.items()):
        if sha(rel) != want:
            raise CheckFailure('earlier contract hash ' + rel)
    need(sha(CALCULATOR_REL) == CALCULATOR_SHA256 and CALCULATOR_REL in con['shared_premises']
         and json.loads((ROOT / 'research/round32/advisor/ax2-gate.json').read_text())['bindings'].get(CALCULATOR_REL)
         == CALCULATOR_SHA256, 'admitted_gates_contracts_calculator_pinned', gates=sorted(GATES),
         note='the AX2 calculator is a declared BC2 premise and is bound by the AX2 gate with the same sha256')
    gates = {rel: json.loads((ROOT / rel).read_text()) for rel in GATES}
    need(all(g['verdict'] == 'accepted_within_scope' for g in gates.values()), 'every_premise_gate_accepted_within_scope')

    # 2. pre-freeze edits in the frozen bytes -------------------------------------------------------------------------
    need(sha(REVIEW_REL) == REVIEW_SHA256, 'bc_contract_review_pinned')
    rev = json.loads((ROOT / REVIEW_REL).read_text())
    applied = []
    for e in rev['blocking_edits'] + rev['non_blocking_edits']:
        if e['contract'] != 'bc2':
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
    need(len(applied) == 30, 'prefreeze_edits_verbatim_in_frozen_bytes', edits=len(applied), paths=applied,
         note='17 blocking and 13 non-blocking BC2 edits of the skeptic pre-freeze review; the review previews block is '
              'not read by this program')

    # 3. controls, semantics, inventory, vocabulary -----------------------------------------------------------------
    ids = con['controls']
    need(ids == pre['controls_required']['ids'] and len(ids) == 52 and len(set(ids)) == 52, 'control_mirror_52')
    earlier = {rel: json.loads((ROOT / rel).read_text()) for rel in EARLIER_CONTRACTS}
    own = [i for i in ids if i in con['new_control_semantics']]
    inherited = {}
    for i in ids:
        if i in own:
            continue
        src = [rel for rel in sorted(EARLIER_CONTRACTS) if i in earlier[rel].get('new_control_semantics', {})]
        if not src:
            raise CheckFailure('control without semantics ' + i)
        inherited[i] = src[-1]
    need(len(own) == 27 and len(inherited) == 25, 'control_semantics_coverage', own=len(own), inherited=inherited)
    declared = sorted(set(['AGENTS.md', CONTRACT_REL] + con['shared_premises']))
    for rel, want in OBSERVED_INPUTS.items():
        if sha(rel) != want:
            raise CheckFailure('inventory hash ' + rel)
    need(sorted(OBSERVED_INPUTS) == declared and len(declared) == 42
         and not any(p.startswith(ISOLATION_FORBIDDEN_PREFIXES) for p in declared), 'producer_inventory_equals_contract',
         files=len(declared))
    need(all(k in PLAN_RECORD['gate_fields'] for k in pre['gate_fields_required'])
         and all(t in PLAN_RECORD['tier_names_allowed'] for t in pre['tier_names_allowed']),
         'plan_vocabulary_covers_gate_fields', plan_sha256=PLAN_RECORD['sha256_at_bc_freeze_commit'])
    forbidden = sorted(set(ROUND_FORBIDDEN + pre['forbidden_phrasings'] + PLAN_RECORD['forbidden'] + EXTRA_FORBIDDEN))
    template = pre['mandatory_sentence_template']
    need(affirmative_hits(template, forbidden) == [] and placeholder_spans(template) == []
         and 'for every N at least 2' in template, 'mandatory_template_scans_clean')

    # 4. pinned admitted route-B values -----------------------------------------------------------------------------
    ax1 = gates['research/round32/advisor/ax1-gate.json']
    ax1_acc = ax1['accepted']
    t_prime = F(re.search(r"T'=t_1'/\(1-352J'\)=(\d+/\d+)", ax1_acc).group(1))
    d_prime = F(re.search(r"bound value D'_ii=(\d+/\d+)", ax1_acc).group(1))
    PINNED_T_PRIME['T'] = t_prime
    need(t_prime == F(13, 3599632512) and T_B(TAU) == t_prime and 'J\'=29|tau|' in ax1_acc
         and 'Exact first-order count 52 faces per factor (49+3)' in ax1_acc
         and 'exactly 7 whole stars (anchors R-S) and 2 single-factor groups meet R, charging 153 faces, 88 meeting R' in ax1_acc,
         'ax1_route_b_inputs_pinned', T_prime=q_(t_prime), D_prime=q_(d_prime),
         note='T_B(|tau|) computed from 52 faces and 29|tau| equals the AX1 gate T\' exactly; every T_B call at '
              '|tau| re-checks the pin, so a source edit substituting 49 or 28 aborts')
    eps = 2 * t_prime + t_prime ** 2
    need(2 * eps * (1 + eps) / (1 + eps * eps) == d_prime, 'ax1_d_prime_reproduced', D_prime=preview(d_prime))
    # G(R) < 148/7 and G'(R) < 352 from e^{1/8} < 8/7 (directed)
    e8 = exp_bracket(F(1, 8))
    need(e8[1] < F(8, 7) and 16 * e8[1] * (1 + F(10, 64)) < G_R and 16 * e8[1] * (18 + F(80, 64)) < GP_R,
         'majorant_constants_directed', exp_one_eighth_upper=preview(e8[1]))

    # 5. geometry: classes, grouping, incidence ---------------------------------------------------------------------
    i1 = parse_i1_table((ROOT / I1_REL).read_text())
    need(i1 == class_table() and len(CLASSES) == 24 and len(OMITTED) == 21 and len(SELECTED) == 3
         and all(k['rel'] == frozenset([ORIGIN]) for k in SELECTED), 'i1_classes_route_b',
         note='24 anchored classes per factor; the 3 selected xy faces have owner set {0} (support one)')
    # every plaquette of a fine region made of complete coarse blocks lies in exactly one route-B group
    fine = [(x, y, z) for x in range(12) for y in range(6) for z in range(3)]
    cnt = {}
    ok_sub = True
    for p in fine:
        for a, c in ORIENT:
            ends = [add(p, DIRS[a]), add(p, DIRS[c]), add(add(p, DIRS[a]), DIRS[c])]
            if any(not (0 <= e[0] < 12 and 0 <= e[1] < 6 and 0 <= e[2] < 3) for e in ends):
                continue
            b = pi_map(p)
            key = ('single', b) if is_selected(p, a, c) else ('star', b)
            cnt[key] = cnt.get(key, 0) + 1
            own = owner_set(p, a, c)
            if key[0] == 'single' and own != frozenset([b]):
                ok_sub = False
            if key[0] == 'star' and not own <= frozenset(add(b, s) for s in S_STAR):
                ok_sub = False
    interior = [b for b in product(range(3), repeat=3) if b[0] < 2 and b[1] < 2 and b[2] < 2]
    need(ok_sub and all(cnt.get(('star', b)) == 21 and cnt.get(('single', b)) == 3 for b in interior),
         'every_plaquette_in_one_group', plaquettes=sum(cnt.values()),
         note='anchor = pi(base) is unique; the selected predicate sends a face to the single group or the star, never '
              'both; interior groups are complete (21 and 3 faces) and every face support lies in its group support')
    box = cube(3)
    grp = route_b_groups(box)
    meet = {k: v for k, v in grp.items() if any(o & set(R_COVER) for o in v)}
    stars = sorted(k[1] for k in meet if k[0] == 'star')
    singles = sorted(k[1] for k in meet if k[0] == 'single')
    faces = [o for v in meet.values() for o in v]
    rset = frozenset(R_COVER)
    meeting = [o for o in faces if o & rset]
    inside = [o for o in meeting if o <= rset]
    stradd = [o for o in meeting if not o <= rset]
    strict = [o for o in meeting if o > rset]
    need(len(stars) == 7 and singles == sorted(R_COVER) and len(faces) == 153 and len(meeting) == 88
         and len(inside) == 16 and len(stradd) == 72 and len(strict) == 6
         and sum(1 for o in inside if len(o) == 1) == 6 and sum(1 for o in inside if o == rset) == 10,
         'incidence_on_R_route_b', stars=[list(b) for b in stars], faces_charged=153, meeting_R=88, inside_R=16,
         straddling=72, strictly_containing_R=6)
    faces_through_u = sum(1 for d in S_STAR for k in CLASSES if d in k['rel'])
    omitted_through_u = sum(1 for d in S_STAR for k in OMITTED if d in k['rel'])
    groups_through_u = len(S_STAR) + 1
    need(faces_through_u == FACES_B and omitted_through_u == FACES_A and groups_through_u == GROUPS_B
         and 4 * 7 + 1 == J_B, 'per_site_counts_route_b', faces_per_factor=faces_through_u,
         groups_per_site=groups_through_u, J_prime_over_tau=J_B,
         note='faces through u: offsets d in S with u-d an anchor: 24+4+8+16 = 52 (49 omitted + 3 selected); four '
              'incident stars and one single group: 5 groups, 4*7+1 = 29')
    # support-one groups never straddle; first-order R-marginal nonzero exactly for owner sets inside R
    need(all(frozenset([b]) <= rset or not (frozenset([b]) & rset) for b in box)
         and all((o <= rset) == (len(o - rset) == 0) for o in meeting), 'support_one_groups_never_straddle',
         note='a single group {b} meets a region only if it is contained in it; the first-order R-marginal of a face '
              'term |W_f Omega><Omega| + h.c. is nonzero exactly when its owner set lies in R (Haar mean of a spin-1/2 '
              'link outside R is zero): 16 faces (10 omitted with owner set R, 6 selected)')
    need(8 * 4 * F(3, 4) == 24, 'selected_face_site_energy_24',
         note='a selected face puts spin 1/2 on four links of one factor: h_b energy 8*4*(3/4)=24 on that factor; the '
              'first-order vector is kept in Q_L only for L at least 24')

    # 6. admissibility ------------------------------------------------------------------------------------------------
    rho = DISC_OVER_TAU * TAU
    wt = W_SPLIT * TAU
    tau_star_a = F(1, 37888)
    w_a = tau_star_a / TAU
    adm = {'disc_selfmap': J_B * rho * G_R, 'disc_contraction': J_B * rho * GP_R,
           'W_selfmap': J_B * wt * G_R, 'W_contraction': J_B * wt * GP_R, 'lambda': F(2, W_SPLIT),
           'routeA_disc_selfmap': J_B * tau_star_a * G_R, 'routeA_disc_contraction': J_B * tau_star_a * GP_R,
           'routeA_W_selfmap': J_B * w_a * TAU * G_R, 'W_max_route_B': R_BALL / (J_B * TAU * G_R)}
    need(adm['disc_selfmap'] <= R_BALL and adm['disc_contraction'] < 1 and adm['W_selfmap'] <= R_BALL
         and adm['W_contraction'] < 1 and adm['lambda'] < Q and adm['routeA_disc_selfmap'] > R_BALL
         and adm['routeA_disc_contraction'] < 1 and adm['routeA_W_selfmap'] > R_BALL
         and 28 * tau_star_a * G_R <= R_BALL and not (F(2, 64) < Q),
         'admissibility_under_J_prime', values={k: q_(v) for k, v in adm.items()},
         previews={k: preview(v) for k, v in adm.items()},
         note='rho=64|tau| and W=1024 pass the route-B self-map and contraction; the route-A extremes (disc 1/37888, '
              'weight 1/(37888|tau|)) pass the contraction but fail the self-map (29/1792 > 1/64), so the rejection '
              'must test the self-map; W=64 fails lambda < q')

    # 7. coefficient input: T_B, K_B, common core, piece graph ----------------------------------------------------------
    cst = route_b_constants(TAU)
    cst100 = route_b_constants(TAU / 100)
    need(cst['K_B'] == 2 * T_B(rho) == F(13, 27941256), 'K_B_route_b', K_B=q_(cst['K_B']), preview=preview(cst['K_B']),
         T_B_disc=q_(T_B(rho)), note='K_B = 2T_B(64|tau|), T_B(rho)=(52 rho/144)/(1-29*352 rho); exact_first_order, '
                                     'analytic_disc; never the BA1 gate value')
    src_rows = []
    ok_core = True
    for n in (2, 3):
        pairs = [('c1B', cube(n), cube(n + 1)), ('c4B', cube(n), cube(n + 2)),
                 ('c5B', cuboid((-n, -n, -n), (n + 1, n, n + 2)), cube(n)),
                 ('c5B', cuboid((-n - 1, -n, -n), (n, n + 1, n)), cuboid((-n, -n - 2, -n), (n + 1, n, n)))]
        for name, va, vb in pairs:
            src = source_sites(va, vb)
            core = cube(n)
            mind = min(norm_inf(p) for p in src)
            att = 0
            for u in core:
                d = min(dinf(u, p) for p in src)
                if d < n - norm_inf(u):
                    ok_core = False
                if d == n - norm_inf(u):
                    att += 1
            src_rows.append({'comparison': name, 'N': n, 'min_source_norm': mind, 'attained_sites': att,
                             'sites': len(core)})
            if mind < n:
                ok_core = False
    need(ok_core, 'every_site_common_core_route_b', rows=src_rows,
         note='every source face (of a star or single group present in one volume only) has all its sites at '
              '|p|_inf >= N, so d_inf(u, sources) >= N-|u|_inf at every u in Lambda_N; attained; single groups outside '
              'Lambda_N are sources at |b|_inf >= N+1')
    # order versus distance on the route-B piece graph (single sites included): pieces are face owner sets
    pieces = sorted({o for v in route_b_groups(cube(2)).values() for o in v}, key=lambda s: sorted(s))
    by_site = {}
    for i, o in enumerate(pieces):
        for x in o:
            by_site.setdefault(x, []).append(i)
    ok_ovd = True
    slack_min = None
    for u in (ORIGIN, E_Z, (1, 1, 1), (-2, 0, 1), (2, -2, 2)):
        dist = {i: 1 for i in by_site.get(u, [])}
        frontier = list(dist)
        while frontier:
            nxt = []
            for i in frontier:
                for x in pieces[i]:
                    for j in by_site[x]:
                        if j not in dist:
                            dist[j] = dist[i] + 1
                            nxt.append(j)
            frontier = nxt
        for i, npieces in dist.items():
            d = min(dinf(u, x) for x in pieces[i])
            if d >= 1:
                slack = npieces - (1 + d)
                if slack < 0:
                    ok_ovd = False
                slack_min = slack if slack_min is None else min(slack_min, slack)
    singles_pieces = sum(1 for o in pieces if len(o) == 1)
    need(ok_ovd and slack_min == 0 and singles_pieces == 125, 'order_versus_distance_piece_graph',
         pieces=len(pieces), single_site_pieces=singles_pieces, minimum_slack=slack_min,
         note='BFS on the intersection graph of the route-B pieces of Lambda_2 (single sites included): a connected '
              'family through u reaching a piece at l_inf distance d >= 1 has at least d+1 pieces; single-site pieces '
              'cost one order and zero distance; attained')

    # 8. iterated split: C_B, c_site,B, whole sequence, exhaustion ---------------------------------------------------
    sp = cst['split']
    targets = {'K_B': F(par['rate_constant_pair']['coefficient_input_T0']['K_B_target']),
               'C_B': F(par['rate_constant_pair']['R_form_T1']['C_B_target']),
               'c_site_B': F(par['rate_constant_pair']['region_form_T2']['c_site_B_target']),
               'C_prime_B': F(par['rate_constant_pair']['whole_sequence_T3']['C_prime_B_target']),
               'c_prime_site_B': F(par['rate_constant_pair']['whole_sequence_region_T4']['c_prime_site_B_target'])}
    need(targets == {'K_B': F(1, 10 ** 6), 'C_B': F(1, 250000), 'c_site_B': F(1, 500000), 'C_prime_B': F(1, 250000),
                     'c_prime_site_B': F(1, 400000)}, 'targets_read_from_contract',
         targets={k: q_(v) for k, v in targets.items()})
    need(sp['per_level_factor'] < 1 and sp['c2'] < 1 and sp['S_lambda'] == F(2169, 343),
         'split_recursion_route_b', t0=q_(sp['t0']), tW=q_(sp['tW']), beta=q_(sp['beta']),
         previews={k: preview(sp[k]) for k in ('t0', 'tW', 'c1', 'c2', 'beta', 'per_level_factor')},
         S_lambda=q_(sp['S_lambda']),
         note='t_0 = 2T_B(|tau|) = 13/1799816256, t_W = 2T_B(1024|tau|); c_1, c_2 of the covering-chain closure; '
              'beta* = c_1/(1-c_2); S_lambda at x = (2/W)/q = 1/8')
    margins = {
        'K_B': targets['K_B'] / cst['K_B'], 'C_B': targets['C_B'] / cst['C_B'],
        'c_site_B': targets['c_site_B'] / cst['c_site_B'],
        'C_prime_B_nested': targets['C_prime_B'] / cst['C_prime_B_nested'],
        'C_prime_B_union': targets['C_prime_B'] / cst['C_prime_B_union'],
        'c_prime_site_B_nested': targets['c_prime_site_B'] / cst['c_prime_site_B_nested'],
        'c_prime_site_B_union': targets['c_prime_site_B'] / cst['c_prime_site_B_union']}
    need(all(m >= 2 for m in margins.values()), 'constants_and_margins_route_b',
         constants={k: q_(v) for k, v in cst.items() if k != 'split'},
         previews={k: preview(v) for k, v in cst.items() if k != 'split'},
         margins={k: preview(v) for k, v in margins.items()},
         note='c_site,B = K_B(2 + beta* S_lambda), C_B = c_site,B (1+q); nested C\'_B = C_B/(1-q), union (one direct c4B) '
              'C\'_B = C_B; the binding margin is the coefficient/region pair (about 2.149)')
    crude = route_b_constants(TAU, tier='crude_majorant')
    need(crude['C_B'] > targets['C_B'] and crude['K_B'] > targets['K_B'], 'crude_tier_reported',
         K_B_crude=preview(crude['K_B']), C_B_crude=preview(crude['C_B']), c_site_B_crude=preview(crude['c_site_B']),
         note='crude_majorant reported separately, fails, retained; never a target')
    ra = route_b_constants(TAU, faces=FACES_A, j=J_A)
    rb_refined_tw = 2 * F(49 * W_SPLIT + 3, 144) * TAU / (1 - J_B * W_SPLIT * TAU * GP_R)
    need(ra['K_B'] == F(49, 111790368) and ra['K_B'] < cst['K_B'] and rb_refined_tw < sp['tW'],
         'route_a_values_differ', route_A_K=q_(ra['K_B']), route_A_c_site=preview(ra['c_site_B']),
         refined_tW_labelled=preview(rb_refined_tw),
         note='the same formulas with 49 faces and 28|tau| give the BA1/BB1 values, which a route-B label rejects; the '
              'weighted first order (49W+3)|tau|/144 is a labelled refinement of 52W|tau|/144')
    t_region = (1 + t_prime) ** 2
    t_region_cmp = (1 + 2 * t_prime) ** 2
    need(t_region <= 1 + F(1, 10 ** 8) and t_region_cmp > 1 + F(1, 10 ** 8), 'region_factor_route_b_fixture',
         per_box=preview(t_region - 1), comparison_majorant=preview(t_region_cmp - 1),
         model_is_finite_graph=True, transfers_to_aq=False,
         note='(1+T\')^2 <= 1+10^-8 with the per-box route-B anchored bound T\' (margin about 1.38); with the '
              'comparison majorant 2T\' it fails, so the fixture reads t as T\'; the split bound needs no such factor')
    ex_n, ex_u = cst['exhaustion_nested'], cst['exhaustion_union']
    need(ex_n == cst['c_site_B'] * F(127, 63) and ex_u == 2 * cst['c_site_B'], 'exhaustion_bound_route_b',
         nested=preview(ex_n), union=preview(ex_u),
         note='||rho^{V_k}_Y - rho^inf_Y||_1 <= (c_site,B + c\'_site,B)|Y| e^{|Y|/10^8} q^(N_k - max|y|_inf): one '
              'direct c5B comparison of V_k with Lambda_{N_k} plus item 1 with M to infinity')
    tel = sum((cst['C_B'] * Q ** (k - 1) for k in range(2, 2 + 60)), F(0))
    need(tel <= cst['C_prime_B_nested'] * Q and cst['C_prime_B_nested'] * Q - tel < F(1, 10 ** 100),
         'nested_telescoping_all_M', note='sum_{k>=N} C_B q^(k-1) = C_B q^(N-1)/(1-q); partial sums below the closed form')
    # coarse translations: box containment; non-coarse: uniform coefficients kept, partition broken
    ok_tr = True
    for vv in ((1, 0, 0), (0, -1, 1), (1, 1, -1)):
        nv = norm_inf(vv)
        for n in range(nv + 2, nv + 4):
            shifted = {add(p, vv) for p in cube(n)}
            if not (cube(n - nv) <= shifted and cube(n - nv) <= cube(n)):
                ok_tr = False
    coarse, partition_kept = 0, 0
    window = [(x, y, z) for x in range(8) for y in range(4) for z in range(2)]
    for sh in product(range(4), range(4), range(4)):
        diffs = {sub(pi_map(add(p, sh)), pi_map(p)) for p in window}
        if len(diffs) == 1:
            partition_kept += 1
        if sh[0] % 4 == 0 and sh[1] % 2 == 0:
            coarse += 1
    need(ok_tr and coarse == 8 and partition_kept == 8, 'translations_route_b',
         note='Lambda_N+v and Lambda_N both contain Lambda_{N-|v|_inf} for N >= |v|_inf+2 (one direct c5B); in a 4x4x4 '
              'fine window exactly the fine translations with x = 0 mod 4 and y = 0 mod 2 keep the factor partition '
              '(8 of 64); every fine translation keeps the uniform face coefficient tau/3, so the route-A rejection '
              'reason is false here and no claim is made for non-coarse translations')
    # flip set E meets every plaquette oddly; U_E is a product of one-link unitaries
    def in_e(p, d):
        return {'x': p[1] % 2 == 0, 'y': p[2] % 2 == 0, 'z': p[0] % 2 == 0}[d]
    odd = True
    for par_ in product(range(2), repeat=3):
        for a, c in ORIENT:
            k = sum(1 for tail, d in face_links(par_, a, c) if in_e(tail, d))
            if k not in (1, 3):
                odd = False
    ax1_f = (ROOT / AX1_F_REL).read_text()
    need(odd and 'HNM-AX1-F19' in ax1_f and 'HNM-AX1-F20' in ax1_f
         and 'U_E H_N(tau) U_E^*=H_N(-tau) in every box and cutoff' in ax1_acc, 'sign_mirror_premise',
         note='E meets every plaquette in 1 or 3 links (8 parity classes x 3 orientations); AX1 F19-F20 and gate item '
              '(7): U_E H_N(tau) U_E^* = H_N(-tau) in every centered box and cutoff; U_E restricted to Y is the product '
              'over E cap Y, independent of N, so whole-sequence convergence at both signs gives the pointwise mirror')

    # 9. node: calculator replay and own labelled re-evaluation ------------------------------------------------------
    ax2 = gates['research/round32/advisor/ax2-gate.json']
    ax2_acc = ax2['accepted']
    d_gate = F(int(re.search(r'exact datum d=(\d+)/\(4\*10\^40\)', ax2_acc).group(1)), 4 * 10 ** 40)
    r_gate = F(int(re.search(r"exact radius bound R'=(\d+)/10\^40", ax2_acc).group(1)), 10 ** 40)
    m = re.search(r'inside \[(\d+)/\(8\*10\^39\), (\d+)/\(4\*10\^40\)\]', ax2_acc)
    lo_gate, hi_gate = F(int(m.group(1)), 8 * 10 ** 39), F(int(m.group(2)), 4 * 10 ** 40)
    res, calc_ns = run_calculator()
    res_m, _ = run_calculator(tau='-1/100000000')
    res100, _ = run_calculator(fixed=False, tau='1/10000000000')
    need(F(res['certified_datum']) == d_gate and F(res['certified_absolute_error_outward_1e-40']) == r_gate
         and d_gate - r_gate == lo_gate and d_gate + r_gate == hi_gate and res['free_reference_included'] is True
         and res['sub_label'] == 'reference_unresolved' and res['state_bound_D_prime'] == q_(d_prime)
         and res['duhamel_slope_k_prime'] == q_(F(51, 4) * TAU),
         'node_calculator_replay', datum=q_(d_gate), radius=q_(r_gate), interval=[q_(lo_gate), q_(hi_gate)],
         note='the admitted AX2 calculator (hash-pinned, executed from source bytes) at its fixed design returns the '
              'AX2 gate datum and outward radius exactly; the interval is [d-R\', d+R\']')
    need(res_m['certified_datum'] == res['certified_datum'] and res_m['certified_absolute_error'] ==
         res['certified_absolute_error'] and res_m['mirrored_coupling_replay'] is True, 'node_minus_tau_replay',
         note='-10^-8: the U_E mirror (no real g), a replay of the same |tau| formula')
    pi_lo, pi_hi = pi_bracket()
    e3 = exp_bracket(3, 60)
    own_half = (1 / (4 * e3[0]) - 1 / (4 * e3[1])) / 2
    own_r = 2 * (d_prime + d_prime ** 2) + 51 * TAU / pi_lo + own_half
    need(F(333, 106) < pi_lo < pi_hi < F(355, 113) and own_r <= r_gate and 1 / (4 * e3[1]) > lo_gate
         and 1 / (4 * e3[0]) < hi_gate, 'node_own_cross_check_labelled', own_radius=preview(own_r),
         gap_to_R_prime=preview(r_gate - own_r),
         note='own re-evaluation r = 2(D\'+D\'^2) + 51|tau|/pi + half-width (own Machin pi, own e^{-3} bracket), '
              'labelled, r <= R\'; the free reference e^{-3}/4 lies inside the restated interval (reference_unresolved)')
    rej = []
    for bad in ({'selected': ('0', '0', '0')}, {'window': 'C1'}, {'state_tier': 'av1_forward_tier_ii'},
                {'tau': '1/100000000', 's': '2', 'fixed_design': True}):
        try:
            calc_ns['certify'](**bad)
        except ValueError:
            rej.append(sorted(bad))
    need(len(rej) == 4, 'calculator_rejects_model_crossing', rejected=rej,
         note='the admitted calculator refuses the zero triple, another window, the AV1 state tier and a changed '
              'fixed design')

    # 10. scaling ------------------------------------------------------------------------------------------------------
    ratios = {k: cst[k] / cst100[k] for k in ('K_B', 'C_B', 'c_site_B', 'C_prime_B_nested', 'C_prime_B_union',
                                               'c_prime_site_B_nested', 'c_prime_site_B_union')}
    node_ratio = F(res['certified_absolute_error']) / F(res100['certified_absolute_error'])
    need(all(F(95) <= v <= F(105) for v in ratios.values()) and F(res100['certified_datum']) == d_gate
         and F(95) <= node_ratio <= F(105), 'tau_over_100_ratios', ratios={k: preview(v) for k, v in ratios.items()},
         ratios_exact={k: q_(v) for k, v in ratios.items()}, node_radius_ratio=preview(node_ratio),
         note='same exact formulas at tau/100; q and rho/|tau| are exactly 1 (frozen); the node datum ratio is exactly '
              '1; the node radius replay ratio is recorded, not a target')

    # 11. fixtures -----------------------------------------------------------------------------------------------------
    fixtures = {}

    def fx(name, ok, cid, **kw):
        need(ok, 'exhibit_' + cid, model_is_finite_graph=True, transfers_to_aq=False, **kw)
        fixtures[name] = {'exhibited': True, 'model_is_finite_graph': True, 'transfers_to_aq': False}

    f13 = {}
    for bb in (F(1, 2), F(0)):
        psi = state(3, [(mask_of(0, 1), F(1, 3)), (mask_of(1), bb), (mask_of(2), F(2, 5))])
        f13[str(bb)] = rdm(psi, [0], 3)
    fx('coefficient_decay_not_marginal_decay', f13['1/2'] == [[F(45, 49), F(6, 49)], [F(6, 49), F(4, 49)]]
       and f13['0'] == [[F(9, 10), F(0)], [F(0), F(1, 10)]], 'fixture_coefficient_decay_not_marginal_decay',
       note='the coefficients meeting r are unchanged while the outside coefficient c_o changes rho_r (AV1 F13 type)')
    a0, b0 = F(1, 3), F(1, 4)
    vals = {}
    for e_ in (F(0), F(1, 5), F(1, 10)):
        psi = state(3, [(mask_of(0, 1), a0), (mask_of(1, 2), b0), (mask_of(2), e_)])
        vals[str(e_)] = rdm(psi, [0], 3)[0][1]
    z0 = (1 + a0 * a0) * (1 + F(1, 25)) + b0 * b0
    fx('second_order_propagation', vals['0'] == 0 and vals['1/5'] == -a0 * b0 * F(1, 5) / z0
       and vals['1/10'] != 0, 'fixture_second_order_propagation', offdiag_at_e_1_5=q_(vals['1/5']),
       note='chain r-o-o\'\' with straddlers a={r,o}, b={o,o\'\'}: changing only e={o\'\'} moves the off-diagonal '
            'R-marginal by -a b e/Z exactly (the product of the two straddling amplitudes)')
    psi = state(3, [(mask_of(0, 1), F(1, 3)), (mask_of(1), F(1, 2))])
    lin_zero = {}
    for lab, msk in (('{r}', mask_of(0)), ('{r,o} straddling', mask_of(0, 2)), ('{o} single outside', mask_of(2))):
        pa = state(3, [(msk, F(1, 1000))])
        pb = state(3, [(msk, F(1, 2000))])
        ra_, rb_ = rdm(pa, [0], 3), rdm(pb, [0], 3)
        lin_zero[lab] = ra_[0][1] == 0 and rb_[0][1] == 0
    fx('straddling_supports', lin_zero == {'{r}': False, '{r,o} straddling': True, '{o} single outside': True},
       'fixture_straddling_supports',
       note='a creation inside R moves the off-diagonal R-marginal at first order; a straddling one and a single-site '
            'creation outside R do not (Haar mean zero at the outside site)')
    base = [(mask_of(0), F(1, 60)), (mask_of(1), F(1, 70)), (mask_of(0, 1), F(1, 50)), (mask_of(0, 2), F(1, 9))]
    rhos = []
    weights = []
    infid = []
    for k in range(4):
        n_ = 3 + k
        pa = state(n_, base + [(mask_of(3 + j), F(1, 6)) for j in range(k)])
        pb = state(n_, base + [(mask_of(3 + j), F(-1, 6)) for j in range(k)])
        rhos.append(rdm(pa, [0, 1], n_))
        weights.append(ip(pa, pa))
        infid.append(1 - ip(pa, pb) ** 2 / (ip(pa, pa) * ip(pb, pb)))
    fx('normalization_spectators', all(r_ == rhos[0] for r_ in rhos) and len(set(weights)) == 4,
       'fixture_normalization_spectators', note='rho_R identical for 0..3 decoupled spectators while the norm changes')
    fx('global_fidelity', infid[0] == 0 and all(infid[k + 1] > infid[k] for k in range(3)),
       'fixture_global_fidelity', infidelities=[preview(x) for x in infid],
       note='flipping spectators changes the global overlap geometrically while every R-marginal is identical')
    xs = [(mask_of(0), F(1, 5)), (mask_of(0, 1), F(1, 4))]

    def x_apply(vec, crs):
        for mm, amp in crs:
            cc = cre(vec, mm, amp)
            vec = [x - y for x, y in zip(vec, cc)]
        return vec

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
    dl = [[a / tr1 - b / tr2 for a, b in zip(r1, r2)] for r1, r2 in zip(n1, n2)]
    nd_ = n_map([[a - b for a, b in zip(r1, r2)] for r1, r2 in zip(om1, om2)])
    fx('split_trace_and_lipschitz', tr1 >= 1 and tr2 >= 1 and trace_norm_2x2(dl)[1] <= 2 * trace_norm_2x2(nd_)[0]
       and psd(om1) and psd(om2), 'fixture_split_trace_and_lipschitz', trace_N=[q_(tr1), q_(tr2)])
    prod_b = [F(fact(k + 1), 10 ** k) for k in range(1, 16)]
    fx('split_per_site_charging', prod_b[9] > prod_b[8] and all(F(1, 2 ** (k + 1)) < F(1, 2 ** k) for k in range(14)),
       'fixture_split_per_site_charging',
       note='product of growing region sizes (k+1)!/10^k increases from k=9; per-site charging is geometric')
    ham = (F(0), F(1, 2), F(2))
    ek = []
    for sq in ((F(1, 9), F(4, 9), F(4, 9)), (F(5, 9), F(16, 45), F(4, 45))):
        ek.append((1 - sq[0], 2 * sum(h * s_ for h, s_ in zip(ham, sq))))
    fx('cutoff_eckart', all(a <= b for a, b in ek), 'fixture_cutoff_eckart',
       note='1-|<psi,psi_L>|^2 <= 2(E_L-E_0) with the route-B gap 1/2; without a gap no vector convergence')
    fx('cutoff_limit_order', min(F(1), F(3, 1000)) < F(1, 100) and min(F(1), F(1000, 3)) == 1,
       'fixture_cutoff_limit_order', note='x(N,L)=min(1,L/N): the iterated limits differ (0 and 1)')
    fx('fixed_versus_moving_vector', trace_norm_2x2([[F(-1), F(0)], [F(0), F(1)]])[0] == 2,
       'fixture_fixed_versus_moving_vector', note='||rho_n - rho_1||_1 = 2 while <e_1, rho_n e_1> = 0')
    fx('zero_free_region', 1 + 4 * (F(0) ** 2 - F(1, 2) ** 2) == 0, 'fixture_zero_free_region',
       note='the bilinear normalization 1+4z^2 of Omega-2z|11> vanishes at z=i/2')
    phi_out = state(2, [(mask_of(0), F(1, 2))])
    e_out = sum(phi_out[s] ** 2 * bin(s).count('1') for s in range(4)) / ip(phi_out, phi_out)
    fx('outside_vector_not_ground_state', e_out == F(1, 5), 'fixture_outside_vector_not_ground_state',
       note='phi_out=(1-c_o)Omega has number energy 1/5 > 0: not an outside ground state; no gap argument')
    single_in = rdm(state(2, [(mask_of(0), F(1, 7))]), [0], 2)
    single_out = rdm(state(2, [(mask_of(1), F(1, 7))]), [0], 2)
    fx('support_one_group', single_in[1][1] == F(1, 50) and single_out == [[F(1), F(0)], [F(0), F(0)]],
       'fixture_support_one_group',
       note='a single-site creation inside R changes rho_R at first order in the amplitude (diagonal 1/50 at 1/7); '
            'one at a site outside R leaves rho_R = P_R: support-one groups never straddle and are never clipped')
    seq = [F((-1) ** n_) + F(1, n_ + 2) for n_ in range(12)]
    fx('whole_sequence_versus_subsequence', seq[0] != seq[1] and abs(seq[10] - seq[11]) > F(1, 10),
       'fixture_whole_sequence_versus_subsequence',
       note='an alternating sequence has convergent subsequences but no whole-sequence limit; only a Cauchy bound over '
            'all M > N gives the whole sequence')
    tau_s = F(1, 100)
    hmat = lambda t, kap: [[F(0), -t / 6, -kap / 6], [-t / 6, F(24), F(0)], [-kap / 6, F(0), F(24)]]
    dg = [F(1), F(-1), F(-1)]
    flip = lambda m_: [[dg[i] * m_[i][j] * dg[j] for j in range(3)] for i in range(3)]
    fx('flip_compression', flip(hmat(tau_s, tau_s)) == hmat(-tau_s, -tau_s)
       and flip(hmat(tau_s, tau_s + F(1, 1000))) != hmat(-tau_s, -tau_s), 'fixture_flip_compression',
       note='the compression onto {Omega, 2W Omega, 2W_g Omega}: D H(tau,tau) D = H(-tau,-tau) with D=diag(1,-1,-1); a '
            'selected coefficient not tied to tau breaks it')
    fixtures['region_factor_route_b'] = {'exhibited': True, 'model_is_finite_graph': True, 'transfers_to_aq': False}
    need(sorted(fixtures) == sorted(REQUIRED_FIXTURES), 'fixtures_exhibited', fixtures=sorted(fixtures))

    # 12. packet, validator, controls ---------------------------------------------------------------------------------
    ba1_k = F(re.search(r'K=(\d+/\d+) \(about 4\.3832e-7', gates['research/round33/advisor/ba1-gate.json']['accepted']).group(1))
    bb1_acc = gates['research/round33/advisor/bb1-gate.json']['accepted']
    bb1_c = F(re.search(r'iterated_split route proves the smaller C=(\d+/\d+)', bb1_acc).group(1))
    bb1_cs = F(re.search(r'iterated_split proves the smaller c_site=(\d+/\d+)', bb1_acc).group(1))
    route_a_values = [ba1_k, bb1_c, bb1_cs, F(4, 984375), F(2, 984375), F(28), F(49), F(4), F(9856), F(37888)]
    need(ba1_k == F(49, 111790368) and bb1_c == ra['C_B'] and bb1_cs == ra['c_site_B'], 'route_a_gate_values_parsed',
         note='the BB1 gate iterated_split values equal this program\'s formula with route-A inputs (49 faces, 28|tau|): '
              'the route-B values differ only through the inputs')
    brackets = pre['scaling_brackets_per_constant']
    bracket_values = {'K_B': (F(95), F(105)), 'C_B': (F(95), F(105)), 'c_site_B': (F(95), F(105)),
                      'C_prime_B': (F(95), F(105)), 'c_prime_site_B': (F(95), F(105)), 'q': (F(1), F(1)),
                      'rho_over_tau': (F(1), F(1)), 'node_datum': (F(1), F(1)), 'node_radius_replay': (F(95), F(105))}
    ctx = {'declared_inputs': declared, 'control_ids': ids, 'tau': TAU, 'metric': par['metric'],
           'window': par['window'], 'T_prime': t_prime, 'D_prime': d_prime, 'route_a_values': route_a_values,
           'incidence': {'stars_meeting_R': 7, 'singles_meeting_R': 2, 'faces_charged': 153, 'meeting_R': 88,
                         'inside_R': 16, 'straddling': 72, 'faces_per_factor': 52, 'groups_per_site': 5},
           'targets': targets, 'ax2': {'d': d_gate, 'R': r_gate}, 'sentence': template, 'forbidden': forbidden,
           'gate_fields': pre['gate_fields_required'], 'error_terms': pre['error_terms_itemized'],
           'brackets': brackets, 'bracket_values': bracket_values, 'second_order_derivative': -a0 * b0,
           'mirror_premise': 'AX1 F19-F20: U_E H_N(tau) U_E^* = H_N(-tau) in every centered box and cutoff; '
                             'whole-sequence convergence at both signs'}

    def crec(cid, value, route, assembly=None, labelled=False):
        tgt = targets[cid] if cid in targets else None
        row = {'id': cid, 'value': value, 'tier': 'exact_first_order', 'route': route, 'q': Q, 'target': tgt,
               'meets_target': (value <= tgt) if tgt is not None else None, 'signs': ['+', '-']}
        if assembly:
            row['assembly'] = assembly
        if labelled:
            row['labelled'] = True
        return row

    statements = [
        'The reduced densities of the route-B named construction converge as a whole sequence on every finite region, '
        'at a rate in N for every N at least 2 with the region inside the box.',
        'Every exhausting sequence of finite complete-factor route-B volumes of the same prescription has the same '
        'limit; this is not a comparison of boundary conditions.',
        'The value at -10^-8 is the U_E mirror with no real g, a replay of the same |tau| formula.',
        'No route-B dynamics, no correlation-function rate in N and no uniqueness of any ground state is claimed.',
    ]
    base_pk = {
        'contract_sha256': CONTRACT_SHA256, 'inputs': list(declared), 'controls': {k: True for k in ids},
        'admission_reads_preview': False,
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False},
        'provenance_premises': [], 'model_id': MODEL_ID, 'triple': ['tau/24', 'tau/24', 'tau/24'], 'tau': TAU,
        'signs': ['+', '-'], 'group': 'SU(2)', 'grouping': GROUPING, 'model_is_finite_graph': False,
        'boundary': 'centered whole-star-plus-single-group boxes', 'label': LABEL,
        'parameters': {'metric': par['metric'], 'weights': par['weights'], 'window': par['window'],
                       'clock': par['clock'], 'node': par['node'], 'N_min': 2, 'cutoff': par['cutoff']},
        'clock': CLOCK, 'reference_energy': 3, 'u_over_theta': F(1, 8), 'window_labelled_in': 'theta',
        'clock_per_comparison': {k: CLOCK for k in COMPARISONS}, 'coupling_per_comparison': {k: TAU for k in COMPARISONS},
        'topology': dict(TOPOLOGY), 'fixtures': copy.deepcopy(fixtures),
        'route_b_inputs': {'J_prime': J_B, 'faces_per_factor': FACES_B, 'groups_per_site': GROUPS_B,
                           'T_B_at_tau': t_prime, 'values_used': [F(J_B), F(FACES_B), F(GROUPS_B), F(10208)]},
        'admissibility': {'declared_before_constants': True, 'disc_radius': rho, 'W': W_SPLIT, 'lambda': F(2, W_SPLIT),
                          'q': Q, 'q_per_N': False, 'optimized_after_evaluation': False,
                          'admissibility_per_site_sum': J_B, 'route_a_extremes_rejected_by': 'self-map',
                          'route_a_extremes_rejected': True},
        'incidence': dict(ctx['incidence']),
        'support_one': {'straddle': False, 'clipped': False, 'first_order_creation_nonzero': True,
                        'piece_graph': 'cost one order, zero distance'},
        'first_order_marginal': {'faces_inside_R': 16, 'omitted_owner_R': 10, 'selected_single_sites': 6,
                                 'straddling_zero': 72},
        'selected_face': {'site_energy': 24, 'kept_for_L_at_least': 24},
        'coefficient_input': {'route': 'analytic_disc', 'tier': 'exact_first_order', 'every_site': True,
                              'far_site_input': 'route-B every-site form', 'proved_in_full': True,
                              'cited_as_admitted': False, 'source': 'route-B disc lemma (this packet)',
                              'exponent': '(N-|u|_inf)_+', 'zero_free_region': None, 'density_analytic_claimed': False,
                              'untruncated_coefficients_claimed': False, 'uniform_in_L': True,
                              'lipschitz_as_decay': None},
        'split': {'route': 'iterated_split', 'charging': 'per_site', 'trace_N_ge_1_checked': True,
                  'lipschitz_checked': True, 'straddling_included': True, 'straddling_charged_beyond_first_order': True,
                  'normalization': 'exact ratio (Tr N_c >= 1)', 'outside_gap_argument': False,
                  'locality_mechanism': 'coefficient input and covering-chain recursion', 'lipschitz_decay_factor': None,
                  'second_order_derivative': -a0 * b0, 'state_decay_inferred_from_coefficients': False},
        'constants': [crec('K_B', cst['K_B'], 'analytic_disc'), crec('C_B', cst['C_B'], 'iterated_split'),
                      crec('c_site_B', cst['c_site_B'], 'iterated_split'),
                      crec('C_prime_B', cst['C_prime_B_nested'], 'iterated_split', 'nested_telescoping'),
                      crec('c_prime_site_B', cst['c_prime_site_B_nested'], 'iterated_split', 'nested_telescoping'),
                      crec('C_B_union_volume', 2 * cst['C_B'], 'iterated_split', labelled=True)],
        'comparisons': {k: {'route': 'direct', 'signs': ['+', '-'], 'regimes': ['Q_L', 'untruncated']}
                        for k in COMPARISONS},
        'region': {'Y_dependence': '|Y| e^{|Y|/10^8}', 'exponent': 'd_Y = N - max_y |y|_inf',
                   'domain': 'finite complete-factor regions Y inside Lambda_N', 'R_constant_reused': False},
        'cutoff': {'order': CUTOFF_ORDER, 'uniform_in_L': True, 'limits_swapped': False, 'vector_convergence': True,
                   'eigenvalue_only': False, 'gap': 'route-B gap 1/2 (AX1)'},
        'whole_sequence': {'quantifier': 'all M greater than N', 'limit_kind': 'whole sequence',
                           'limit_existence': 'Cauchy bound and completeness of the trace class',
                           'regions': 'every finite complete-factor region Y inside Lambda_N'},
        'exhaustion': {'via': 'one direct c5B comparison of V_k with Lambda_{N_k} and item 1',
                       'constant': 'c_site,B + c_prime_site,B',
                       'prescription': 'route-B volumes: stars inside the volume, every single group kept',
                       'boundary_comparison_claimed': False},
        'mirror': {'kind': 'pointwise on every finite region', 'premise': ctx['mirror_premise'], 'real_g': False,
                   'counted_as_second_coupling': False},
        'identification': {'before_inheritance': True,
                           'identified_with': 'every AQ1-type subsequential state of the AX1 construction',
                           'on': 'every finite region', 'inherited_list': AX1_INHERITED},
        'translation': {'separate_item': True, 'from_nested_cubes_only': False, 'input': 'one direct comparison c5B',
                        'union_two_step_as_bound': False, 'bound': 'C_B q^(N-|v|_inf-1)', 'N_condition': 'N >= |v|_inf+2',
                        'non_coarse': 'no claim', 'non_coarse_reason': None},
        'node': {'s': [1], 'grid': None, 'datum': d_gate, 'radius': r_gate,
                 'calculator_replay': {'sha256': CALCULATOR_SHA256, 'reads_undeclared': False, 'datum': d_gate,
                                       'radius_outward': r_gate},
                 'slope': '51|tau|/4', 'state_term': d_prime,
                 'own_cross_check': {'labelled': True, 'headline': False, 'value': own_r},
                 'region_form_proved': True, 'reference_inside': True, 'sub_labels': ['reference_unresolved'],
                 'shift_claimed': False, 'finite_box_node_convergence_claimed': False,
                 'minus_tau': 'mirror replay of the same |tau| formula'},
        'dynamics': {'route_b_dynamics_claimed': False, 'dynamics_level_exported': False,
                     'correlation_functions_claimed': False},
        'common_limit': {'claimed': False, 'families': 1, 'identified_with_all_contained': False},
        'model_crossing': {'identified_with_zero_selected_limit': False, 'bb_constants_applied': False,
                           'transfer_to_zero_selected': False},
        'rates': [{'what': 'densities (R and regions)', 'range': 'every N at least 2 (regions: Y inside Lambda_N)'},
                  {'what': 'Cauchy estimates', 'range': 'every N at least 2'},
                  {'what': 'exhaustion', 'range': 'every N_k at least 2 with Y inside Lambda_{N_k}'}],
        'uniform_in': UNIFORM_IN, 'rate_unit': RATE_UNIT, 'rate_in_a': False, 'brackets': dict(brackets),
        'scaling': {'K_B': ratios['K_B'], 'C_B': ratios['C_B'], 'c_site_B': ratios['c_site_B'],
                    'C_prime_B': ratios['C_prime_B_nested'], 'c_prime_site_B': ratios['c_prime_site_B_nested'],
                    'q': F(1), 'rho_over_tau': F(1), 'node_datum': F(1), 'node_radius_replay': node_ratio},
        'verdict': 'accepted_within_scope', 'retuned': False, 'statements': statements, 'sentence': template,
        'sentence_count': 1, 'sub_labels': list(SUB_LABELS), 'gate_fields': dict(pre['gate_fields_required']),
        'error_terms': {k: 'itemized: ' + k for k in pre['error_terms_itemized']},
    }
    rebind(base_pk)
    need(validate(copy.deepcopy(base_pk), ctx) is True, 'validator_accepts_skeptic_packet')

    def mk(fn, rebind_digest=True):
        def run():
            pk = copy.deepcopy(base_pk)
            fn(pk)
            if rebind_digest:
                rebind(pk)
            validate(pk, ctx)
        return run

    def setp(path, value, rebind_digest=True):
        def f(pk):
            cur = pk
            for k in path[:-1]:
                cur = cur[k]
            cur[path[-1]] = value
        return mk(f, rebind_digest)

    def add_statement(text):
        return mk(lambda pk: pk['statements'].append(text))

    def const_edit(cid, **kw):
        def f(pk):
            for r in pk['constants']:
                if r['id'] == cid and not r.get('labelled'):
                    r.update(kw)
        return mk(f)

    ctl, pos = {}, {}
    ctl['coherent_evidence_tampering'] = [
        ('control boolean flipped, digest rebound', setp(['controls', ids[5]], False), 'control booleans'),
        ('declared snapshot removed, digest rebound', mk(lambda pk: pk['inputs'].remove(CALCULATOR_REL)),
         'snapshot inventory'),
        ('digest not rebound', setp(['controls', ids[0]], 'true', rebind_digest=False), 'freeze digest'),
        ('undeclared proposal read', mk(lambda pk: pk['inputs'].append('research/round33/experts/modern/bc2-targets-proposal.md')),
         'undeclared read'),
        ('constant below the derivable value', const_edit('c_site_B', value=cst['c_site_B'] / 2),
         'below the derivable value'),
    ]
    ctl['exact_arithmetic_admission'] = [
        ('float constant', const_edit('K_B', value=4.65e-07), 'exact arithmetic'),
        ('preview read by admission', setp(['admission_reads_preview'], True), 'preview read by admission'),
    ]
    ctl['no_priority_or_continuum_claim'] = [
        ('priority', setp(['claims', 'scientific_priority_verified'], True), 'no priority or continuum claim'),
        ('continuum gate field', setp(['gate_fields', 'continuum_claim'], True), 'no priority or continuum claim'),
        ('historical provenance', setp(['provenance_premises'], ['Newton manuscript']), 'no priority or continuum claim'),
    ]
    ctl['changed_model_relabelled'] = [
        ('zero-selected triple under the route-B label', setp(['triple'], ['0', '0', '0']), 'changed model relabelled'),
        ('all-contained boundary', setp(['boundary'], 'all-contained-plaquette boxes'), 'changed model relabelled'),
        ('another group', setp(['group'], 'SU(3)'), 'changed model relabelled'),
        ('finite-graph result', setp(['model_is_finite_graph'], True), 'changed model relabelled'),
        ('weak-coupling label', setp(['label'], 'uniform Kogut-Susskind SU(2) near weak coupling'), 'label'),
    ]
    ctl['insufficient_verdict_retained'] = [
        ('missed target accepted', const_edit('K_B', value=F(1, 500000), meets_target=True), 'target flag'),
        ('limited without dominating term', setp(['verdict'], 'limited'), 'dominating term'),
        ('retuned', setp(['retuned'], True), 'retuned'),
    ]
    ctl['tau_scaling_exponent'] = [
        ('quadratic ratio', setp(['scaling', 'C_B'], F(10000)), 'tau scaling exponent'),
        ('bracket changed after evaluation', mk(lambda pk: pk['brackets'].update({'C_B': '[99,101]'})),
         'bracket changed'),
        ('q not frozen', setp(['scaling', 'q'], F(100)), 'tau scaling exponent'),
    ]
    ctl['wrong_delta_alpha_hbar_clock'] = [
        ('energy 24 with s', setp(['reference_energy'], 24), 'wrong delta alpha hbar clock'),
        ('u labelled theta', setp(['window_labelled_in'], 'u'), 'normalized u without conversion'),
    ]
    ctl['tier_mixing_rejected'] = [
        ('polymer_kp route', const_edit('C_B', route='polymer_kp'), 'tier mixing'),
        ('Lieb-Robinson tier', const_edit('C_B', tier='polynomial_lieb_robinson'), 'tier mixing: tier vocabulary'),
        ('assembly recorded as a route', const_edit('C_prime_B', route='nested_telescoping'), 'assembly recorded as a route'),
        ('hypothesis source', const_edit('C_prime_B', hypothesis_source='bb1_frozen_targets'), 'hypothesis source'),
        ('K_B under iterated_split', const_edit('K_B', route='iterated_split'), 'tier mixing: K_B'),
        ('weighted_norm as bound', const_edit('K_B', route='weighted_norm'), 'tier mixing: route'),
    ]
    ctl['uniform_in_N_not_in_a'] = [
        ('uniform in the lattice spacing', setp(['uniform_in'], 'N and the lattice spacing'), 'uniform in N not in a'),
        ('uniform in a in a statement', add_statement('The constants are uniform in a.'), 'uniform in N not in a'),
    ]
    ctl['placeholder_span_rejected'] = [
        ('placeholder', add_statement('K_B equals <the disc value here>.'), 'placeholder span'),
    ]
    ctl['negation_aware_phrase_scan'] = [
        ('affirmative correlation length', add_statement('The rate gives a correlation length.'), 'negation aware'),
        ('affirmative thermodynamic limit', add_statement('We obtain the thermodynamic limit.'),
         'named construction not uniqueness'),
    ]
    pos['negation_aware_phrase_scan'] = [
        ('negated phrase accepted', add_statement('This is not the thermodynamic limit of other boundary conditions.'))]
    ctl['parameters_declare_metric_weights_window'] = [
        ('metric missing', mk(lambda pk: pk['parameters'].pop('metric')), 'parameters must declare'),
        ('weights missing', mk(lambda pk: pk['parameters'].pop('weights')), 'parameters must declare'),
        ('cutoff missing', mk(lambda pk: pk['parameters'].pop('cutoff')), 'parameters must declare'),
    ]
    ctl['rate_constant_pair_prefrozen'] = [
        ('rho optimized to 32|tau|', setp(['admissibility', 'disc_radius'], 32 * TAU), 'rate constant pair prefrozen'),
        ('W changed after evaluation', setp(['admissibility', 'W'], 2048), 'rate constant pair prefrozen'),
        ('q per N', setp(['admissibility', 'q_per_N'], True), 'rate constant pair prefrozen'),
        ('weights declared after constants', setp(['admissibility', 'declared_before_constants'], False),
         'declared after constants'),
        ('target changed', const_edit('C_B', target=F(1, 100000)), 'rate constant pair prefrozen'),
    ]
    ctl['decay_rate_in_N_not_a'] = [
        ('rate in fm', setp(['rate_unit'], 'per 0.1 fm'), 'decay rate in N not a'),
        ('rate in a', setp(['gate_fields', 'rate_in_a_claimed'], True), 'decay rate in N not a'),
    ]
    ctl['topology_named'] = [
        ('weak topology', setp(['topology', 'states'], 'weak-*'), 'topology named'),
        ('moving vector fixture missing', mk(lambda pk: pk['fixtures'].pop('fixed_versus_moving_vector')),
         'topology named'),
    ]
    ctl['subsequence_versus_whole_sequence'] = [
        ('N to N+1 only', setp(['whole_sequence', 'quantifier'], 'N to N+1'), 'subsequence versus whole sequence'),
        ('subsequential limit', setp(['whole_sequence', 'limit_kind'], 'subsequence'), 'subsequence versus whole sequence'),
    ]
    ctl['common_clock'] = [
        ('c5B at another coupling', setp(['coupling_per_comparison', 'c5B'], TAU / 2), 'common clock'),
        ('c4B clock in u', setp(['clock_per_comparison', 'c4B'], 'u=theta/8'), 'common clock'),
    ]
    ctl['coefficient_decay_not_marginal_decay'] = [
        ('state decay inferred from coefficients', setp(['split', 'state_decay_inferred_from_coefficients'], True),
         'coefficient decay not marginal decay'),
        ('fixture missing', mk(lambda pk: pk['fixtures'].pop('coefficient_decay_not_marginal_decay')),
         'fixture missing'),
    ]
    ctl['normalization_couples_supports'] = [
        ('straddling dropped', setp(['split', 'straddling_included'], False), 'normalization couples supports'),
        ('straddling first order only', setp(['split', 'straddling_charged_beyond_first_order'], False),
         'normalization couples supports'),
        ('normalization 1+O(t^2)', setp(['split', 'normalization'], '1+O(t^2)'), 'normalization couples supports'),
        ('support containing R given a first-order marginal',
         setp(['first_order_marginal', 'straddling_zero'], 66), 'route b first order marginal'),
    ]
    ctl['outside_vector_not_ground_state'] = [
        ('gap argument on phi_out', setp(['split', 'outside_gap_argument'], True), 'outside vector not ground state'),
    ]
    ctl['global_fidelity_orthogonality_catastrophe'] = [
        ('global overlap route', setp(['split', 'locality_mechanism'], 'global overlap'),
         'global fidelity orthogonality catastrophe'),
        ('fixture missing', mk(lambda pk: pk['fixtures'].pop('global_fidelity')), 'fixture missing'),
    ]
    ctl['cutoff_uniform_then_removed'] = [
        ('limits in another order', setp(['cutoff', 'order'], 'N first inside Q_L'), 'cutoff uniform then removed'),
        ('zero-selected gap source', setp(['cutoff', 'gap'], 'AM2 gap for the patterned family'),
         'cutoff uniform then removed: gap source'),
        ('Q_L only', mk(lambda pk: pk['comparisons']['c1B'].__setitem__('regimes', ['Q_L'])), 'comparison regimes'),
    ]
    ctl['cutoff_vector_removal'] = [
        ('eigenvalue convergence only', setp(['cutoff', 'eigenvalue_only'], True), 'cutoff vector removal'),
        ('vector convergence not shown', setp(['cutoff', 'vector_convergence'], False), 'cutoff vector removal'),
    ]
    ctl['region_constant_scales_with_Y'] = [
        ('R constant reused on Y', setp(['region', 'R_constant_reused'], True), 'region constant scales with Y'),
        ('Y outside Lambda_N', setp(['region', 'domain'], 'every finite region Y'), 'region constant scales with Y'),
        ('|Y|^2 dependence', setp(['region', 'Y_dependence'], '|Y|^2 e^{|Y|/10^8}'), 'region constant scales with Y'),
    ]
    ctl['named_construction_not_uniqueness'] = [
        ('uniqueness field', setp(['gate_fields', 'uniqueness_of_ground_state_claimed'], True),
         'named construction not uniqueness'),
        ('the infinite-volume ground state', add_statement('The limit is the infinite-volume ground state.'),
         'named construction not uniqueness'),
    ]
    ctl['global_lipschitz_not_decay'] = [
        ('map Lipschitz constant as decay', setp(['coefficient_input', 'lipschitz_as_decay'], F(319, 3125000)),
         'global lipschitz not decay'),
        ('density Lipschitz as per-shell factor', setp(['split', 'lipschitz_decay_factor'], F(1, 10 ** 7)),
         'global lipschitz not decay'),
    ]
    ctl['fixture_second_order_propagation'] = [
        ('first-order propagation claimed', setp(['split', 'second_order_derivative'], F(0)),
         'fixture second order propagation'),
        ('fixture missing', mk(lambda pk: pk['fixtures'].pop('second_order_propagation')), 'fixture missing'),
    ]
    ctl['fixture_split_lipschitz_and_trace'] = [
        ('product of region sizes', setp(['split', 'charging'], 'product_of_region_sizes'),
         'fixture split lipschitz and trace'),
        ('trace unchecked', setp(['split', 'trace_N_ge_1_checked'], False), 'fixture split lipschitz and trace'),
        ('fixture label', mk(lambda pk: pk['fixtures']['split_trace_and_lipschitz'].__setitem__('transfers_to_aq', True)),
         'fixture label'),
    ]
    ctl['zero_free_region_required'] = [
        ('density analyticity claimed', setp(['coefficient_input', 'density_analytic_claimed'], True),
         'zero free region required'),
    ]
    ctl['every_site_coefficient_input'] = [
        ('R-only input at far sites', setp(['coefficient_input', 'far_site_input'], 'R-only gate input'),
         'every site coefficient input'),
        ('BA1 gate value cited', setp(['coefficient_input', 'source'], 'BA1 gate'), 'every site coefficient input'),
        ('route-B every-site form cited as admitted', setp(['coefficient_input', 'cited_as_admitted'], True),
         'every site coefficient input'),
        ('exponent N-|u| without the positive part', setp(['coefficient_input', 'exponent'], 'N-1'),
         'every site coefficient input'),
    ]
    ctl['cutoff_limit_order'] = [
        ('limits swapped', setp(['cutoff', 'limits_swapped'], True), 'cutoff limit order'),
    ]
    ctl['cauchy_estimate_not_compactness'] = [
        ('compactness plus closeness', setp(['whole_sequence', 'limit_existence'], 'compactness and closeness'),
         'cauchy estimate not compactness'),
    ]
    ctl['limit_identified_with_aq1_limits'] = [
        ('zero-selected list inherited', setp(['identification', 'inherited_list'], 'AQ1/AQ2 zero-selected list'),
         'limit identified with aq1 limits'),
        ('BB2 list inherited', setp(['identification', 'inherited_list'], 'BB2 item 3 list'),
         'limit identified with aq1 limits'),
        ('identified on R only', setp(['identification', 'on'], 'R'), 'limit identified with aq1 limits'),
    ]
    ctl['translation_invariance_separate_item'] = [
        ('from nested cubes', setp(['translation', 'from_nested_cubes_only'], True), 'translation invariance separate item'),
        ('two-step union as bound', setp(['translation', 'union_two_step_as_bound'], True),
         'translation invariance separate item'),
        ('bound without the shift', setp(['translation', 'bound'], 'C_B q^(N-1)'), 'translation invariance separate item'),
    ]
    ctl['route_b_constants_not_route_a'] = [
        ('28|tau| per-site sum', setp(['route_b_inputs', 'J_prime'], J_A), 'route b constants not route a'),
        ('49 faces', setp(['route_b_inputs', 'faces_per_factor'], FACES_A), 'route b constants not route a'),
        ('9856 used', mk(lambda pk: pk['route_b_inputs']['values_used'].append(F(9856))), 'route-A value used'),
        ('BA1 gate K under a route-B label', const_edit('K_B', value=ba1_k), 'route b constants not route a'),
        ('T_B pin broken', setp(['route_b_inputs', 'T_B_at_tau'], F(49, 14398580736)), 'T_B pin'),
    ]
    ctl['disc_admissible_under_J_prime'] = [
        ('route-A disc radius 1/37888', setp(['admissibility', 'disc_radius'], tau_star_a),
         'disc admissible under J prime: disc'),
        ('route-A split weight 1/(37888|tau|)', setp(['admissibility', 'W'], w_a), 'disc admissible under J prime: split'),
        ('tested under 28|tau|', setp(['admissibility', 'admissibility_per_site_sum'], J_A), 'disc admissible under J prime'),
        ('route-A extremes rejected by contraction', setp(['admissibility', 'route_a_extremes_rejected_by'], 'contraction'),
         'disc admissible under J prime'),
    ]
    ctl['support_one_groups'] = [
        ('single groups straddling', setp(['support_one', 'straddle'], True), 'support one groups'),
        ('single groups clipped', setp(['support_one', 'clipped'], True), 'support one groups'),
        ('omitted from the piece graph', setp(['support_one', 'piece_graph'], 'omitted'), 'support one groups'),
    ]
    ctl['route_b_first_order_marginal'] = [
        ('route-A ten faces', mk(lambda pk: pk['incidence'].update({'inside_R': 10})), 'route b first order marginal'),
        ('selected faces dropped', setp(['first_order_marginal', 'faces_inside_R'], 10), 'route b first order marginal'),
    ]
    ctl['selected_face_site_energy'] = [
        ('route-A energy 18', setp(['selected_face', 'site_energy'], 18), 'selected face site energy'),
        ('kept for every L', setp(['selected_face', 'kept_for_L_at_least'], 0), 'selected face site energy'),
    ]
    ctl['one_family_no_common_limit'] = [
        ('common limit claimed', setp(['gate_fields', 'common_limit_claimed'], True), 'one family no common limit'),
        ('identified with all-contained boundary', setp(['common_limit', 'identified_with_all_contained'], True),
         'one family no common limit'),
    ]
    ctl['exhaustion_within_prescription_only'] = [
        ('phrased as boundary comparison', setp(['exhaustion', 'boundary_comparison_claimed'], True),
         'exhaustion within prescription only'),
        ('other prescription', setp(['exhaustion', 'prescription'], 'any boundary condition'),
         'exhaustion within prescription only'),
        ('bound without c_site', setp(['exhaustion', 'constant'], 'c_prime_site,B'), 'exhaustion within prescription only'),
    ]
    ctl['sign_mirror_pointwise'] = [
        ('whole-set only', setp(['mirror', 'kind'], 'whole sets of subsequential limits'), 'sign mirror pointwise'),
        ('second coupling', setp(['mirror', 'counted_as_second_coupling'], True), 'sign mirror pointwise'),
        ('real g at -tau', setp(['mirror', 'real_g'], True), 'sign mirror pointwise'),
    ]
    ctl['identification_before_inheritance_route_b'] = [
        ('inherited first', setp(['identification', 'before_inheritance'], False),
         'identification before inheritance route b'),
    ]
    ctl['region_form_load_bearing_for_node'] = [
        ('node restated with only the R form', setp(['node', 'region_form_proved'], False),
         'region form load bearing for node'),
    ]
    ctl['node_values_unchanged'] = [
        ('re-derived smaller radius as headline', setp(['node', 'radius'], own_r), 'node values unchanged'),
        ('seven-star slope', setp(['node', 'slope'], '49|tau|/4'), 'node values unchanged'),
        ('smaller state term', setp(['node', 'state_term'], d_prime / 2), 'node values unchanged'),
        ('other node', setp(['node', 's'], [2]), 'node values unchanged'),
        ('replay reading an undeclared file', setp(['node', 'calculator_replay', 'reads_undeclared'], True),
         'replay premise'),
        ('own cross-check as headline', setp(['node', 'own_cross_check', 'headline'], True), 'own re-evaluation'),
    ]
    ctl['reference_unresolved_retained_route_b'] = [
        ('shift claimed', setp(['node', 'shift_claimed'], True), 'reference unresolved retained route b'),
        ('resolved_interaction_shift true', setp(['gate_fields', 'resolved_interaction_shift'], True),
         'reference unresolved retained route b'),
    ]
    ctl['no_finite_box_node_convergence'] = [
        ('finite-box node convergence', setp(['node', 'finite_box_node_convergence_claimed'], True),
         'no finite box node convergence'),
    ]
    ctl['no_route_b_dynamics_claim'] = [
        ('route-B dynamics', setp(['dynamics', 'route_b_dynamics_claimed'], True), 'no route b dynamics claim'),
        ('dynamics_level exported', mk(lambda pk: pk['gate_fields'].__setitem__('dynamics_level',
                                                                               'correlation_functions_compact_window')),
         'no route b dynamics claim'),
        ('correlation rate', mk(lambda pk: pk['rates'].append({'what': 'correlation functions', 'range': '5<=N<=14000'})),
         'rate range stated'),
    ]
    ctl['non_coarse_translation_no_claim'] = [
        ('non-coarse invariance claimed', setp(['translation', 'non_coarse'], 'invariant'),
         'non coarse translation no claim'),
        ('route-A rejection reason offered', setp(['translation', 'non_coarse_reason'],
                                                  'selected face mapped to an omitted face of another coefficient'),
         'non coarse translation no claim'),
    ]
    ctl['model_crossing_rejected'] = [
        ('identified with the zero-selected limit', setp(['model_crossing', 'identified_with_zero_selected_limit'], True),
         'model crossing rejected'),
        ('BB constants applied', setp(['model_crossing', 'bb_constants_applied'], True), 'model crossing rejected'),
        ('transfer to the zero-selected family', setp(['model_crossing', 'transfer_to_zero_selected'], True),
         'model crossing rejected'),
    ]
    ctl['direct_comparison_required'] = [
        ('union comparison for c5B', mk(lambda pk: pk['comparisons']['c5B'].__setitem__('route', 'union')),
         'direct comparison required'),
        ('telescoped comparison for c4B', mk(lambda pk: pk['comparisons']['c4B'].__setitem__('route', 'telescoped')),
         'direct comparison required'),
        ('labelled union value used for a target', mk(lambda pk: pk['constants'][-1].__setitem__('used_for_target', True)),
         'direct comparison required'),
    ]
    ctl['rate_range_stated'] = [
        ('rate without range', mk(lambda pk: pk['rates'][0].__setitem__('range', '')), 'rate range stated'),
        ('O(1/N)', add_statement('The densities converge at the rate O(1/N) in N.'), 'rate range stated'),
        ('rate transferred from BB2', mk(lambda pk: pk['rates'].append({'what': 'densities', 'range': 'every N at least 2',
                                                                         'source': 'BB2'})),
         'rate transferred from BB2'),
    ]
    pos['tier_mixing_rejected'] = [
        ('union_comparison assembly (one direct c4B) accepted',
         const_edit('C_prime_B', value=cst['C_prime_B_union'], assembly='union_comparison',
                    union_means='one direct c4B comparison'))]
    pos['insufficient_verdict_retained'] = [
        ('limited with a dominating term accepted',
         mk(lambda pk: pk.update({'verdict': 'limited', 'dominating_term': 'near term 2K_B'})))]
    pos['rate_range_stated'] = [
        ('rate in N with its range accepted',
         add_statement('The region bound holds at a rate in N for every N at least 2 with Y inside Lambda_N.'))]
    pos['direct_comparison_required'] = [
        ('labelled union-volume value kept as a label accepted', mk(lambda pk: None))]
    for cid in ids:
        control(cid, ctl[cid], positives=pos.get(cid, ()))
    need(sorted(ctl) == sorted(ids), 'every_control_executed', controls=len(ids),
         mutations=sum(len(v) for v in ctl.values()))

    readings = [
        'R1: the (1+t)^2 <= 1+10^-8 fixture holds with the per-box route-B anchored bound T\' (1+7.22e-9) and fails '
        'with the comparison majorant 2T\' (1+1.44e-8); the split route needs neither.',
        'R2: the weighted first order is (49W+3)|tau|/144 (selected faces have diameter 0); 52W|tau|/144 is the '
        'contract-form bound, the refinement is labelled.',
        'R3: every finite complete-factor route-B volume has a unique ground and gap 1/2 (AX1 gate item 2), so the '
        'untruncated passage for c5B general volumes is gated (no AY1-type reading as in BB1 R10).',
        'R4: the route-A extremes pass the route-B contraction test (319/1184 < 1) and fail only the self-map '
        '(29/1792 > 1/64).',
        'R5: the order-versus-distance count is attained (minimum slack 0 on Lambda_2); single-site pieces add order '
        'without distance, so they never lower the vanishing order.',
        'R6: C\'_B and c\'_site,B are consequences of C_B and c_site,B up to the assembly factor (64/63 nested, 1 for '
        'one direct c4B comparison); T4 at 1/400000 leaves room for 64/63 (margin 2.644).',
    ]
    return {
        'loop': 'BC2', 'stage': 'pre_comparison', 'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'skeptic (model agent, correlated ancestry; not human review)',
        'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'model': 'AQ_uniform_routeB: uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling (g^4=9.6x10^9), '
                 'route B (whole stars and single-factor groups), both signs |tau|<=10^-8 (-tau the U_E mirror); named '
                 'construction FB on Lambda_N, N at least 2; cover R={0,e_z}',
        'constants': {k: q_(v) for k, v in cst.items() if k != 'split'},
        'constants_preview': {k: preview(v) for k, v in cst.items() if k != 'split'},
        'split': {k: q_(v) for k, v in sp.items()},
        'margins': {k: preview(v) for k, v in margins.items()},
        'tau_over_100': {k: preview(v) for k, v in ratios.items()},
        'node': {'d': q_(d_gate), 'R_prime': q_(r_gate), 'own_labelled_r': preview(own_r)},
        'admissibility': {k: q_(v) for k, v in adm.items()},
        'contract_readings': readings,
        'predictions': {'K_B': preview(cst['K_B']), 'C_B': preview(cst['C_B']), 'c_site_B': preview(cst['c_site_B']),
                        'C_prime_B_nested': preview(cst['C_prime_B_nested']),
                        'C_prime_B_union': preview(cst['C_prime_B_union']),
                        'c_prime_site_B_nested': preview(cst['c_prime_site_B_nested']),
                        'c_prime_site_B_union': preview(cst['c_prime_site_B_union'])},
        'gate_fields': pre['gate_fields_required'], 'sentence': template,
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                   'common_limit_claimed': False, 'uniqueness_of_ground_state_claimed': False},
        'deferred_parts': {'inventory': 'recorded by find and sha256 (names only)', 'phrase_scan': 'mirror of the round tool',
                           'tampering': 'packet level (synthetic packet built from this derivation)',
                           'disc_lemma': 'the complexified fixed point, Weierstrass and the maximum principle are '
                                         'restated in the derivation, not machine-checked'},
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
                      'K_B': result['predictions']['K_B'], 'c_site_B': result['predictions']['c_site_B']}))


if __name__ == '__main__':
    main()
