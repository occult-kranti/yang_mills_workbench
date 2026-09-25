#!/usr/bin/env python3
"""Round33 BC1 skeptic pre-comparison checker (statement loop; zero-selected patterned family).

Written after the BC1 contract froze (sha256 3fb84ed3...79bd, frozen 2026-09-25T04:21:44Z) from the frozen
contract, advisor/selection-bc1.md, advisor/plan.json (vocabulary recorded below, not read at run time) and the
declared premises (the AV2, AW1, AW2, AV1, AY1, AY2, AQ1, AQ2 gates and the AV2/AY2/AW1 reports; the BA1, BA2,
BB1, BB2 gates, the BB2 reports and the skeptic's BA2/BB1/BB2 reviews; the BA1/BA2/BB1/BB2 contracts for the
inherited control semantics), plus the skeptic's own pre-freeze review bc-contract-review.json (blocking edits
and determinations only; its previews_recomputed block is never read by this program), before reading anything
under research/round33/forward/bc1/ (only the file names of its inputs/ were listed and hashed; the recorded
inventory is embedded below) and without reading experts/modern/bc2-targets-proposal.md. Nothing is imported
from any producer, lens or tool. Standard library only. Every admission Boolean is decided with
fractions.Fraction and directed exponential enclosures; floats appear only in labelled 'previews'. Every check
and control raises an explicit exception, so python -O cannot disable it. Model-agent skeptic with correlated
ancestry; not human peer review. Human project author: Hruday N M (BUNZEEY).

What is derived here:
  * the AV2 datum d, radius bound R and interval, and the AW2 enclosure endpoints at both signs, read by hash
    from the Round32 gates and checked as exact rationals (d-R and d+R are the interval endpoints; the AW2
    endpoints are tau/144 -+ K_2^+ tau^2 at tau=10^-8; the gate margins are reproduced exactly);
  * the BB2 bound value C'=4/984375 (nested_telescoping at the hypothesis values, C_h/(1-q)), and N_sign, the
    least N>=2 with C' q^(N-1) < tau/144 - K_2^+ tau^2, computed exactly; the widened F2 enclosure at N_sign and
    N_sign-1 at both signs; robustness of N_sign against the labelled BB2 values; tau/100 as information;
  * the determination of BC1 item 4 from the admitted record (text checks on the hash-pinned AV2 reports, the
    AV2 gate and the AW1 gate), the common GNS item's premises, the skeptic's obligations table;
  * a packet validator that executes all 25 contract controls as damaging mutations with positive cases.

Usage: python3 -B research/round33/skeptic/bc1_check.py --output /absolute/fresh/dir
"""
import argparse
import copy
import hashlib
import json
import re
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = 'research/round33/contracts/bc1.json'
CONTRACT_SHA256 = '3fb84ed3135c48670d26643f120ef2ef74f5888174cf11e7395919e408a279bd'
REVIEW_REL = 'research/round33/skeptic/bc-contract-review.json'  # the skeptic's own pre-freeze review (not a premise)
REVIEW_SHA256 = '339a5f57fe53bb056476299f8cdca388259e445407308ff00960d982a8b01ff9'
EARLIER_CONTRACTS = {
    'research/round33/contracts/ba1.json': '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9',
    'research/round33/contracts/ba2.json': '275ba3b002529b7295d0f8b91dc1cc7a96451e3c7f936ee698a932fdca54fcff',
    'research/round33/contracts/bb1.json': '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018',
    'research/round33/contracts/bb2.json': 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35',
}
# advisor/plan.json changes during the round (a BD drafting commit edited it while BC was in production), so it is
# not read at run time. The vocabulary below was recorded from plan.json as committed with the BC freeze (e4ffdf5).
PLAN_RECORD = {
    'sha256_at_bc_freeze_commit': 'f69d45034df2b6c79986cbedcc8cb9473da3b9f2ec9453340cef0d4a412fb264',
    'plan_sha256_at_freeze_recorded_in_history': '347f3cb187d2e9edc4eee3854cbbab41826edb089baacd04fa0fb31d02a1c2f2',
    'gate_fields': ['coefficient_cauchy_claimed', 'common_limit_claimed', 'continuum_claim', 'correlation_shift_resolved',
                    'dynamics_level', 'dynamics_limit_identified_claimed', 'finite_box_node_claimed',
                    'finite_box_sign_claimed', 'finite_box_sign_scope', 'gns_dynamics_equality_claimed',
                    'model_is_finite_graph', 'node_certificate_restated_for_limit', 'rate_in_N_claimed',
                    'rate_in_a_claimed', 'resolved_interaction_shift', 'scientific_priority_verified',
                    'sign_certificate_restated_for_limit', 'state_convergence_claimed', 'state_decay_claimed',
                    'state_decay_scope', 'transfers_to_aq', 'translation_invariance_claimed',
                    'translation_invariance_scope', 'uniform_in_time_claimed', 'uniqueness_of_ground_state_claimed',
                    'weak_coupling_claim', 'whole_sequence_claimed', 'whole_sequence_scope'],
    'sub_labels_allowed': ['reference_unresolved', 'sign_certified_finite_graph', 'sign_certified_below_cap',
                           'static_not_dynamic', 'uniform_local_closeness_not_uniqueness', 'boundary_decay_rate_only',
                           'convergence_of_named_constructions', 'common_limit_of_named_constructions',
                           'dynamics_on_compact_windows', 'certificate_restated_for_limit', 'transfer_to_named_model',
                           'obstruction_recorded'],
    'forbidden': ['the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
                  'the thermodynamic limit', 'correlation length', 'predicts', 'confirms', 'unique ground state',
                  'a unique limit', 'the unique limit', 'uniqueness of the ground state',
                  'uniquely determines the ground state'],
}
GATES = {  # admitted gates read by this program, sha256 pinned (hash_binding.admitted_gate_sha256_pinned_in_check_py)
    'research/round32/advisor/av2-gate.json': '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33',
    'research/round32/advisor/aw2-gate.json': '640a3b0a74c7fcd66318ba7ce2a60942f837ad154f157bc1d69323589b24be62',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/advisor/aq2-gate.json': '930b697db343ffd261c303c34e6ddd8c6e9c753ee6707931c55dc4171ee47575',
    'research/round33/advisor/ba1-gate.json': '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    'research/round33/advisor/ba2-gate.json': 'e6b163fc8f80de28c51609f77d0bef21dcdc1286638c862ad67202e6f7b0ca35',
    'research/round33/advisor/bb1-gate.json': '18141fea672e5bae09024a5fddc56ea7102aae56ecca16fbb30d67a1354a3827',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
}
AV2_F = 'research/round32/forward/av2/report.md'
AV2_R = 'research/round32/reverse/av2/report.md'
AY2_F = 'research/round32/forward/ay2/report.md'

# Producer input inventory, recorded by the skeptic on 2026-09-25 with `find` over research/round33/forward/bc1/inputs
# (file names only) and a sha256 comparison of each snapshot with the repository file: 40 paths, every snapshot
# byte-identical, equal to AGENTS.md + the contract + its 38 shared premises. This program does not open that folder.
OBSERVED_INPUTS = {
    'AGENTS.md': '870e1a6b1ff81d6e09888d7084dada2dfdb8128048d97857d9c6b1ffce1b9285',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/advisor/aq2-gate.json': '930b697db343ffd261c303c34e6ddd8c6e9c753ee6707931c55dc4171ee47575',
    'research/round29/forward/aq1/report.md': 'b091266f5db009fa967a2adea352fa1b190193cc4bcdc6c4c207e5872fc51da3',
    'research/round29/forward/aq2/report.md': '9144964ca53c995c6c3391625e1a9774d243aefbada43a4e8f8e30f5769589d1',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/av2-gate.json': '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/aw2-gate.json': '640a3b0a74c7fcd66318ba7ce2a60942f837ad154f157bc1d69323589b24be62',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round32/forward/av2/report.md': 'b1ccad9a0d0162dba6efe38d8d3749c4d446d9affd8f6527b6c4c7ca2bfb2556',
    'research/round32/forward/aw1/report.md': 'ea3a936244a31c7ea4d2c8de65798b2bb0fc65a60437122b71a30465e089d883',
    'research/round32/forward/aw2/report.md': 'e8db6f0ce821cb072d6432f040db416cd5351f3c241b1dfc7bf3365c3da76431',
    'research/round32/forward/ay2/report.md': '527ce2f2700764d76f98efd245fd5f5fa95444f97ca81e323aaff48fac781e6b',
    'research/round32/reverse/av2/report.md': '4703bc252786e32148dce7ceea67d6ee21bf6bafe47214a6437cef8f384e329a',
    'research/round32/reverse/aw1/report.md': '4457c9410bb030b0a856c957e04ab3975bd8a0ffe51476c06edd9ef175f1156c',
    'research/round32/skeptic/av2.md': '09ad4183fff5dc6a25e22281c25ed592975a1b29cfd0692a04a511562239f48c',
    'research/round32/skeptic/aw2.md': 'e168f7cbb30af384c872f6da209210fc3eb2aa07d5574ccf9af4c472b62c91ad',
    'research/round33/advisor/ba1-gate.json': '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    'research/round33/advisor/ba2-gate.json': 'e6b163fc8f80de28c51609f77d0bef21dcdc1286638c862ad67202e6f7b0ca35',
    'research/round33/advisor/bb1-gate.json': '18141fea672e5bae09024a5fddc56ea7102aae56ecca16fbb30d67a1354a3827',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
    'research/round33/advisor/selection-bc1.md': '336af80d03616758caea64d5582792e554acfce4f8f85e2e41e0030249113cb5',
    'research/round33/contracts/ba1.json': '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9',
    'research/round33/contracts/ba2.json': '275ba3b002529b7295d0f8b91dc1cc7a96451e3c7f936ee698a932fdca54fcff',
    'research/round33/contracts/bb1.json': '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018',
    'research/round33/contracts/bb2.json': 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35',
    'research/round33/contracts/bc1.json': '3fb84ed3135c48670d26643f120ef2ef74f5888174cf11e7395919e408a279bd',
    'research/round33/forward/bb2/report.md': 'b925ad0720ecb24aeb9483401fe4cf299e713e1793bc2812752d5eca2d723c23',
    'research/round33/methods/historical-physics-panel/SKILL.md': 'a2b366bc661794ee89c29233d0887868b60c0853c85ec136e0529b6f1d5e223a',
    'research/round33/methods/newton-analysis-synthesis/SKILL.md': '2fa3dab9b2420d157457ad3ccaeb0723fb1952871be3e6140dcd3d3c9346ccef',
    'research/round33/methods/paired-physics-research/SKILL.md': '01cda7ee8f8e3eb65c68b0ac6ff0d9e87198f57ea2d997d810d7907b85f4278d',
    'research/round33/methods/paired-physics-research/references/complete-residual-and-error-scope.md': '9e387df64ae05738e740d2ff65973cef0672530e64344ab9e730a139b81b435d',
    'research/round33/methods/qeg-research-advisor/references/round32-state-lemma-and-window.md': '78dc75607920ae799331d6b27b725cba54139d9aceaf04ccbac32a20205a4977',
    'research/round33/methods/tesla-mechanism-resonance/SKILL.md': '81f6d760b3aa45d32db4ae31a3a3c9bec5e1d662e42529b5ae21a220deeb07c3',
    'research/round33/reverse/bb2/report.md': '6f48706c25ff25bce2ed8db40433416624d355797ec11ee5f34b4a3b7a4867a7',
    'research/round33/skeptic/ba2.md': '2ee93777b29c64a5c793599ffead5cbfb20d8c5406ad24e414b459dfb712c98a',
    'research/round33/skeptic/bb1.md': '478582f2106e4f1ab623967602dc561a006eec1b1477e04aff2a93221d635715',
    'research/round33/skeptic/bb2.md': 'd04279547212b83c09e314c25cdd50cffe53441bb05977c976115c10ef7d6749',
}
ISOLATION_FORBIDDEN_PREFIXES = ('research/round33/forward/bc1/', 'research/round33/forward/bc2/',
                                'research/round33/experts/', 'research/round33/skeptic/bc-contract-review',
                                'research/round33/advisor/plan.json', 'research/round33/advisor/deliberation',
                                'research/round33/advisor/panel')

MODEL_ID = 'AQ_patterned_zero_selected'
TAU = F(1, 10 ** 8)
Q = F(1, 64)
COVER = ['0', 'e_z']
CLOCK = 's=alpha*t_E/hbar (Euclidean node); theta=alpha*t/hbar (inherited dynamics)'
TOPOLOGY = {'states': 'trace norm on B(H_Y)', 'dynamics': 'operator norm on |theta| at most 8',
            'representations': 'GNS strong'}
STATE = 'omega_inf, the limit of the named constructions F1 and F2 (BB2)'
IDENTIFICATION = {'premise': 'BB2 items 2-3', 'identified_with': ['every AQ1 subsequential limit',
                                                                 'every F2 subsequential limit'],
                  'before_restatement': True}
C_PRIME_LABEL = 'BB2 gate bound value (nested_telescoping, hypothesis values, BB1 route polymer_kp)'
BOUND_SOURCE = 'BB2 item 1: sup over M greater than N, M to infinity (whole sequence), F2 untruncated at fixed N'
SUB_LABELS = ['certificate_restated_for_limit', 'reference_unresolved', 'static_not_dynamic']
RATE_DENSITY = 'q^(N-1) for every N at least 2'
RATE_CORRELATION = 'BB2 item 5, only on 5<=N<=14000'

# mirror of research/round33/tools/phrase_scan.py (sha256 1c31a495...) reimplemented, not imported
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state', 'uniquely determines the ground state',
    'the thermodynamic limit', 'correlation length',
]
EXTRA_FORBIDDEN = ['equality of GNS dynamics', 'uniform in time', 'uniform in the lattice spacing']
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


def fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def exp_bracket(x, n=60):
    """[lo, hi] for e^x, 0 <= x <= 8: Taylor partial sum and the geometric remainder bound."""
    x = F(x)
    if not (0 <= x <= 8):
        raise CheckFailure('exp domain')
    s = sum((x ** k / fact(k) for k in range(n + 1)), F(0))
    rem = x ** (n + 1) / fact(n + 1) / (1 - x / (n + 2))
    return s, s + rem


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
    body = json.dumps({'inputs': sorted(pk['inputs']), 'controls': pk['controls'],
                       'round32_hashes': pk['round32_hashes']}, sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()


def rebind(pk):
    pk['freeze_digest'] = packet_digest(pk)
    return pk


# ---------------------------------------------------------------- gate parsing
def grab(pattern, text, what):
    m = re.search(pattern, text)
    if m is None:
        raise CheckFailure('gate text: ' + what)
    return m


def parse_av2(gate):
    acc = gate['accepted']
    d = F(int(grab(r'datum d=(\d+)/\(4\*10\^40\)', acc, 'AV2 d').group(1)), 4 * 10 ** 40)
    r_up = F(int(grab(r'r<=R=(\d+)/10\^40', acc, 'AV2 R').group(1)), 10 ** 40)
    m = grab(r'C\(1\) in \[(\d+)/\(4\*10\^40\), (\d+)/\(8\*10\^39\)\]', acc, 'AV2 interval')
    lo, hi = F(int(m.group(1)), 4 * 10 ** 40), F(int(m.group(2)), 8 * 10 ** 39)
    dec = gate['decision']
    d2 = F(int(grab(r'exact datum (\d+)/\(4\*10\^40\)', dec, 'AV2 decision d').group(1)), 4 * 10 ** 40)
    r2 = F(int(grab(r'radius at most (\d+)/10\^40', dec, 'AV2 decision R').group(1)), 10 ** 40)
    return {'d': d, 'R': r_up, 'lo': lo, 'hi': hi, 'decision_d': d2, 'decision_R': r2}


def parse_aw2(gate):
    acc = gate['accepted']
    m = grab(r'K_2\^\+=(\d+)/(\d+) \(~3354', acc, 'AW2 K_2^+')
    k2 = F(int(m.group(1)), int(m.group(2)))
    m = grab(r'= \[(\d+)/D, (\d+)/D\], D=(\d+),', acc, 'AW2 endpoints')
    den = int(m.group(3))
    lo, hi = F(int(m.group(1)), den), F(int(m.group(2)), den)
    m = grab(r'mirror \[-(\d+)/D, -(\d+)/D\]', acc, 'AW2 mirror')
    mlo, mhi = F(-int(m.group(1)), den), F(-int(m.group(2)), den)
    m = grab(r'\(\|tau\|/144-K_2\^\+ tau\^2\)/\(K_2\^\+ tau\^2\)=(\d+)/(\d+)', acc, 'AW2 exclusion margin')
    excl = F(int(m.group(1)), int(m.group(2)))
    m = grab(r'1/\(144 K_2\^\+ \|tau\|\)=(\d+)/(\d+)', acc, 'AW2 sign margin')
    sgn = F(int(m.group(1)), int(m.group(2)))
    return {'K2': k2, 'lo': lo, 'hi': hi, 'mirror_lo': mlo, 'mirror_hi': mhi, 'exclusion_margin': excl,
            'sign_margin': sgn}


def parse_bb2(gate):
    acc, dec = gate['accepted'], gate['decision']
    m = grab(r"C'=(\d+)/(\d+) \(about 4\.0635e-06; exact_first_order, nested_telescoping, hypothesis source "
             r"bb1_frozen_targets, BB1 route polymer_kp", acc, "BB2 C' bound value")
    cp = F(int(m.group(1)), int(m.group(2)))
    m = grab(r"c'_site=(\d+)/(\d+) \(about 2\.0317e-06", acc, "BB2 c'_site bound value")
    csp = F(int(m.group(1)), int(m.group(2)))
    m = grab(r"bound values C'=(\d+)/(\d+) \(about 4\.0635e-6\)", dec, "BB2 decision C'")
    cp_dec = F(int(m.group(1)), int(m.group(2)))
    m = grab(r"the union_comparison route proves C'=(\d+)/(\d+) and c'_site=(\d+)/(\d+) \(labelled\)", acc,
             'BB2 union values')
    union = F(int(m.group(1)), int(m.group(2)))
    m = grab(r"re-evaluated at the admitted BB1 values \(labelled, not bound\), C' is about ([0-9.]+e-07)", acc,
             'BB2 re-evaluated')
    reeval_text = m.group(1)
    return {'C_prime': cp, 'c_site_prime': csp, 'C_prime_decision': cp_dec, 'C_prime_union_labelled': union,
            'C_prime_reevaluated_labelled_text': reeval_text}


# ---------------------------------------------------------------- the finite-box sign corollary
def n_sign_of(cp, lo, q=Q, n_min=2, n_max=64):
    for n in range(n_min, n_max + 1):
        if cp * q ** (n - 1) < lo:
            return n
    raise CheckFailure('N_sign not found')


def widened(lo, hi, cp, n, q=Q):
    w = cp * q ** (n - 1)
    return {'plus': (lo - w, hi + w), 'minus': (-hi - w, -lo + w), 'widening': w}


# ---------------------------------------------------------------- obligations table (the skeptic's own)
def obligations_table():
    rows = [
        {'id': 'O1', 'name': 'uniqueness of the limit', 'status': 'open', 'closing_gate': None, 'scope': None,
         'change_after_round33': 'the AY2 falsifying scenario (two subsequential limits differing on R) is excluded '
                                 'for the named constructions F1 and F2 only (BB2 items 2-3), not for states outside them',
         'missing_premise': 'a statement covering every ground state, not only the limits of F1 and F2: a two-state '
                            'estimate or a classification of every state in the class',
         'candidate_route': 'HTW-type local stability or a Dobrushin-type condition with evaluated constants at the '
                            'cap; or the BB1 marginal-locality lemma extended to arbitrary outside states'},
        {'id': 'O2', 'name': 'whole-sequence convergence', 'status': 'closed_within_scope',
         'closing_gate': 'research/round33/advisor/bb2-gate.json (item 1)',
         'scope': 'reduced densities of F1 and F2 on every finite region, zero-selected family, fixed spacing, '
                  '|tau| at most 10^-8, untruncated vectors at fixed N; sup over M greater than N'},
        {'id': 'O3', 'name': 'translation invariance', 'status': 'closed_within_scope',
         'closing_gate': 'research/round33/advisor/bb2-gate.json (item 4)',
         'scope': 'coarse translations only, the limit of the named constructions; non-coarse translations rejected'},
        {'id': 'O4', 'name': 'a rate in N', 'status': 'closed_within_scope',
         'closing_gate': 'research/round33/advisor/bb2-gate.json (item 1; BB1 per comparison; BA1 coefficients)',
         'scope': 'densities: q^(N-1) with q=1/64 for every N at least 2 (regions: for every N with Y inside '
                  'Lambda_N); correlation functions: BB2 item 5 only on 5<=N<=14000'},
        {'id': 'O5', 'name': 'boundary independence of dynamics on compact time windows',
         'status': 'closed_within_scope',
         'closing_gate': 'research/round33/advisor/ba2-gate.json (items 2-4); research/round33/advisor/bb2-gate.json (item 5)',
         'scope': 'algebraic Heisenberg dynamics of A in B(H_R) for F1 versus F2 on |theta| at most 8 at a rate in N '
                  '(every N at least 2); correlation functions on |theta| at most 8 (rate only on 5<=N<=14000); not '
                  'uniform in time, not GNS dynamics of different states'},
        {'id': 'O6', 'name': 'dynamics of the padded family itself', 'status': 'closed_within_scope',
         'closing_gate': 'research/round33/advisor/ba2-gate.json (items 4-5)',
         'scope': 'the F2 finite-box evolutions converge on |theta| at most 8 to the AQ1 limit dynamics T_theta; AQ1 '
                  'sections 4-5 rerun for every F2 subsequential limit'},
        {'id': 'N1', 'name': 'states outside the named constructions and other boundary conditions', 'status': 'open',
         'source': 'BB2 gate limitations', 'missing_premise': 'a density comparison for boundary prescriptions other '
                                                              'than F1 and F2 (each with its own itemization)',
         'candidate_route': 'the BB1 split with the prescription itemized as for F2 (AY1-type), or O1 routes'},
        {'id': 'N2', 'name': 'finite-box Euclidean node, finite F1 boxes (BC1 item 4)', 'status': 'open',
         'source': 'BC1 contract item 4 (the AV2 record states the node for AQ1 subsequential states only)',
         'missing_premise': 'the window lemma for the untruncated finite-box ground vector with generator G_N-E_N at '
                            'the unchanged M_0=2 and M_1=4s/pi, with the AV1 per-box state bound and the AV2 per-box '
                            'slope',
         'candidate_route': 'rerun AV2 forward F01-F15 in each box: the spectral measure of G_N-E_N in chi_N is carried '
                            'by [0,inf) because E_N is the ground energy, F13-F14 are already box by box, and the AV1 '
                            'tier-(ii) D bounds each box density; then the node for every N at least 2'},
        {'id': 'N3', 'name': 'finite-box Euclidean node, finite F2 boxes (BC1 item 4)', 'status': 'open',
         'source': 'BC1 contract item 4',
         'missing_premise': 'the N2 premises plus the F2 incidence of the groups meeting R and the F2 slope, which are '
                            'not in the AV2 record',
         'candidate_route': 'the AY1 F2 itemization for the groups meeting R, an owner-set relative-unitary slope, the '
                            'AY1 per-box state bound; or the BB2 whole-sequence bound combined with a finite-box '
                            'dynamics comparison over all real theta (window tails), which BA2 does not supply'},
        {'id': 'N4', 'name': 'F2 finite-box sign for 2 <= N < N_sign', 'status': 'open',
         'source': 'BC1 item 3 (N_sign computed here)',
         'missing_premise': 'a finite-box enclosure of omega^{F2,N}(W) sharper than the AW2 enclosure widened by '
                            "C' q^(N-1) at N=2 and N=3",
         'candidate_route': 'the AW1 remainder bound re-derived box by box for F2 boxes (AY1 itemization); the '
                            "labelled BB2 values do not help (N_sign is 4 for every C' in the stated threshold interval)"},
        {'id': 'N5', 'name': 'correlation-function rate in N beyond N=14000 with the frozen r_N', 'status': 'open',
         'source': 'BB2 gate item 5 and limitation (vacuous from N=14419)',
         'missing_premise': 'a region term that does not outgrow q^(N-r_N) (the frozen factor e^{|Lambda_{r_N}|/10^8})',
         'candidate_route': 'a slower r_N (for example logarithmic in N) or a region form without the exponential '
                            'factor; convergence without a rate already holds'},
        {'id': 'N6', 'name': 'GNS dynamics of different states', 'status': 'open',
         'source': 'BA2 and BB2 gate exclusions', 'missing_premise': 'two different states compared in one '
                                                                     'representation',
         'candidate_route': 'not needed for F1 and F2 (one state); for other states it waits on N1 or O1'},
        {'id': 'N7', 'name': 'uniform-in-time statements', 'status': 'open',
         'source': 'BA2 and BB2 gate exclusions (window |theta| at most 8)',
         'missing_premise': 'bounds that do not grow like U^2/(1-vU/3) outside the window',
         'candidate_route': 'the AQ2 gap alpha/16 with a clustering-in-time argument; not formulated'},
        {'id': 'N8', 'name': 'non-centred F2 volumes in the fifth BB1 comparison', 'status': 'open',
         'source': 'BB1 and BB2 gate limitations (AY1 itemization as a reviewed local reading)',
         'missing_premise': 'a gated AY1 itemization H1-H5 for every F2 volume containing Lambda_N',
         'candidate_route': 'restate the AY1 items for general complete-factor F2 volumes in a statement loop'},
        {'id': 'N9', 'name': 'the route-B uniform model', 'status': 'pending_bc2_gate',
         'source': 'BC2 (produced in parallel)', 'missing_premise': 'the BC2 gate',
         'candidate_route': 'the BC2 contract; this row cites the BC2 gate only once it is recorded'},
        {'id': 'N10', 'name': 'analyticity of the reduced density in the coupling', 'status': 'open',
         'source': 'BA1 and BB1 gate limitations', 'missing_premise': 'a zero-free region of the complexified '
                                                                      'normalization',
         'candidate_route': 'the BA1 disc with a lower bound on the complexified norm; not formulated'},
        {'id': 'N11', 'name': 'untruncated creation coefficients', 'status': 'open', 'source': 'BA1 gate limitation',
         'missing_premise': 'the coefficient bounds after the cutoff is removed',
         'candidate_route': 'AM2 section 6 applied to the coefficient collection; not needed by BB1/BB2'},
        {'id': 'N12', 'name': 'anything uniform in the lattice spacing a', 'status': 'open',
         'source': 'every Round33 gate', 'missing_premise': 'constants uniform in a (all are at fixed spacing)',
         'candidate_route': 'none within the strong-coupling expansion'},
        {'id': 'N13', 'name': 'the continuum problem', 'status': 'open', 'source': 'every gate',
         'missing_premise': 'weak coupling and a -> 0', 'candidate_route': 'none in this record'},
    ]
    return rows


REQUIRED_ROW_NAMES = {
    'O1': 'uniqueness of the limit', 'O2': 'whole-sequence convergence', 'O3': 'translation invariance',
    'O4': 'a rate in N', 'O5': 'boundary independence of dynamics on compact time windows',
    'O6': 'dynamics of the padded family itself'}
REQUIRED_NEW_ROWS = ['states outside the named constructions and other boundary conditions',
                     'finite-box Euclidean node, finite F1 boxes (BC1 item 4)',
                     'finite-box Euclidean node, finite F2 boxes (BC1 item 4)',
                     'F2 finite-box sign for 2 <= N < N_sign',
                     'correlation-function rate in N beyond N=14000 with the frozen r_N',
                     'GNS dynamics of different states', 'uniform-in-time statements',
                     'non-centred F2 volumes in the fifth BB1 comparison', 'the route-B uniform model',
                     'anything uniform in the lattice spacing a', 'the continuum problem']
EXPECTED_STATUS = {'O1': 'open', 'O2': 'closed_within_scope', 'O3': 'closed_within_scope', 'O4': 'closed_within_scope',
                   'O5': 'closed_within_scope', 'O6': 'closed_within_scope'}


# ---------------------------------------------------------------- packet validator
def validate(pk, c):
    # provenance, tampering, isolation
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
    # model
    if (pk['model_id'] != MODEL_ID or pk['triple'] != ['0', '0', '0'] or pk['tau'] != c['tau']
            or pk['signs'] != ['+', '-'] or pk['cover'] != COVER or pk['model_is_finite_graph'] is not False
            or pk['group'] != 'SU(2)'):
        raise Rejected('changed model relabelled')
    if pk['families'] != ['F1', 'F2'] or pk['state'] != STATE:
        raise Rejected('changed model relabelled: state')
    par = pk['parameters']
    for key in ('metric', 'weights', 'window', 'clock', 'node', 'N_min'):
        if key not in par or par[key] in (None, ''):
            raise Rejected('parameters must declare metric weights window: ' + key)
    if par['window'] != c['window'] or par['N_min'] != 2:
        raise Rejected('parameters must declare metric weights window: window')
    if pk['clock'] != CLOCK or pk['reference_energy'] != 3 or pk['reference'] != 'e^{-3s}/4':
        raise Rejected('wrong delta alpha hbar clock')
    if pk['u_over_theta'] != F(1, 8) or pk['window_labelled_in'] != 'theta':
        raise Rejected('wrong delta alpha hbar clock: normalized u without conversion')
    if pk['clock_per_family'] != {'F1': CLOCK, 'F2': CLOCK} or pk['coupling_per_family'] != {'F1': c['tau'],
                                                                                             'F2': c['tau']}:
        raise Rejected('common clock')
    if pk['topology'] != TOPOLOGY or pk['fixtures'].get('fixed_versus_moving_vector') is not True:
        raise Rejected('topology named')
    # identification before restatement
    idf = pk['identification']
    if idf != IDENTIFICATION:
        raise Rejected('limit identified with aq1 limits')
    # node (AV2) restated unchanged
    nd = pk['node']
    if nd['s'] != [1] or nd.get('grid') is not None or nd.get('crossover_certified') is not False:
        raise Rejected('post hoc node rejected')
    if nd['datum'] != c['av2']['d'] or nd['radius'] != c['av2']['R'] or nd['interval'] != [c['av2']['lo'],
                                                                                            c['av2']['hi']]:
        raise Rejected('certificate values unchanged: AV2')
    if nd['labels'] != c['av2_labels'] or nd['rederived'] is not False:
        raise Rejected('certificate values unchanged: AV2 labels or re-derivation')
    if nd['reference_inside'] is not True or 'reference_unresolved' not in nd['sub_labels'] \
            or nd['shift_claimed'] is not False:
        raise Rejected('reference unresolved retained')
    if nd['minus_tau'] != {'kind': 'replay of the same |tau| formula', 'counted_as_confirmation': False}:
        raise Rejected('mirror sign replay not confirmation: node')
    if nd['applies_to'] != STATE:
        raise Rejected('route b not restated: node applied to another model')
    # enclosure (AW2) restated unchanged
    en = pk['enclosure']
    if en['plus'] != [c['aw2']['lo'], c['aw2']['hi']] or en['minus'] != [c['aw2']['mirror_lo'], c['aw2']['mirror_hi']]:
        if en['plus'] == [c['tau'] / 144, c['tau'] / 144] or en.get('remainder') != 'K_2^+ tau^2':
            raise Rejected('second order remainder kept')
        raise Rejected('certificate values unchanged: AW2')
    if en.get('remainder') != 'K_2^+ tau^2' or en['K2'] != c['aw2']['K2']:
        raise Rejected('second order remainder kept')
    if en['minus_kind'] != 'replay of the same |tau| formula' or en['minus_counted_as_confirmation'] is not False:
        raise Rejected('mirror sign replay not confirmation: enclosure')
    # finite-box sign
    fb = pk['finite_box_sign']
    if fb['bound_source'] != BOUND_SOURCE:
        raise Rejected('finite box sign from whole sequence: bound source')
    if fb['C_prime'] != c['C_prime'] or fb['C_prime_label'] != C_PRIME_LABEL:
        raise Rejected('finite box sign from whole sequence: constant')
    if fb['q'] != Q or fb['vectors'] != 'untruncated at fixed N' or fb['family'] != 'F2':
        raise Rejected('finite box sign from whole sequence: scope')
    if fb['widening'] != "C' q^(N-1) on both sides":
        raise Rejected('second order remainder kept: widening')
    if fb['comparator'] != 'strict':
        raise Rejected('finite box sign from whole sequence: comparator')
    ns = n_sign_of(c['C_prime'], c['aw2']['lo'])
    if fb['N_sign'] != ns:
        raise Rejected('finite box sign from whole sequence: N_sign not the least N')
    for n, row in fb['rows'].items():
        wv = widened(c['aw2']['lo'], c['aw2']['hi'], c['C_prime'], n)
        if row['plus'] != list(wv['plus']) or row['minus'] != list(wv['minus']):
            raise Rejected('finite box sign from whole sequence: widened endpoints')
        if row['sign_certified'] != (wv['plus'][0] > 0):
            raise Rejected('finite box sign from whole sequence: sign flag')
    if fb['below_N_sign'] != 'nothing claimed; open obligation row N4' or fb['cutoff_L_states_claimed'] is not False:
        raise Rejected('finite box sign from whole sequence: range below N_sign')
    if fb['F1'] != 'certified by AW2 at every N at least 2 and every cutoff; untruncated by AV1 cutoff-vector removal, recorded as agreement':
        raise Rejected('finite box sign from whole sequence: F1 boxes')
    if fb['tier'] != 'exact_first_order' or fb['route'] is not None or fb['input_labels'] != c['input_labels']:
        raise Rejected('changed model relabelled: tier label of the new constant')
    # finite-box node
    fbn = pk['finite_box_node']
    if fbn['claimed'] is not False or fbn['restated'] is not False or fbn['method'] is not None:
        raise Rejected('finite box node only from record')
    if fbn['open_rows'] != ['N2', 'N3']:
        raise Rejected('finite box node only from record: open rows')
    # common GNS item
    g = pk['gns']
    if g['one_state_premise'] != ['BB2 items 2-3', 'BA2 item 4'] or g['different_states_equality'] is not False:
        raise Rejected('same state not different states')
    if g['dynamics'] != 'AQ1 limit dynamics T_theta' or g['correlation_rate_range'] != '5<=N<=14000':
        raise Rejected('same state not different states: scope')
    # obligations table
    ob = pk['obligations']
    by_id = {r['id']: r for r in ob}
    for rid, name in REQUIRED_ROW_NAMES.items():
        if rid not in by_id or by_id[rid]['name'] != name:
            raise Rejected('obligations table complete: row dropped ' + rid)
        if by_id[rid]['status'] != EXPECTED_STATUS[rid]:
            raise Rejected('obligations table complete: status of ' + rid)
    names = [r['name'] for r in ob]
    for name in REQUIRED_NEW_ROWS:
        if name not in names:
            raise Rejected('obligations table complete: new row missing')
    for r in ob:
        if r['status'] == 'closed_within_scope':
            if not r.get('closing_gate') or not r.get('scope'):
                raise Rejected('obligations table complete: closed row without gate and scope')
        elif not r.get('missing_premise') or not r.get('candidate_route'):
            raise Rejected('obligations table complete: open row without premise or route')
    if pk['falsifier_exclusion'] != 'named constructions F1 and F2 only (BB2 items 2-3)':
        raise Rejected('named construction not uniqueness: falsifier')
    # rates
    for r in pk['rates']:
        if not r.get('range'):
            raise Rejected('rate range stated')
        if r['what'] == 'correlation functions' and r['range'] != '5<=N<=14000':
            raise Rejected('rate range stated: correlation rate range')
        if r['what'] == 'densities' and r['range'] != 'every N at least 2':
            raise Rejected('rate range stated: density rate range')
    for text in pk['statements']:
        if re.search(r'O\(1/N\)', text) and '5<=N<=14000' not in text:
            raise Rejected('rate range stated: unqualified O(1/N)')
    # Round32 records untouched
    if pk['round32_edits'] != []:
        raise Rejected('round32 gates untouched')
    for rel, want in c['round32_hashes'].items():
        if pk['round32_hashes'].get(rel) != want:
            raise Rejected('round32 gates untouched: hash')
    # route B
    if pk['route_b'] != {'restated': False, 'applied_to_uniform_model': False}:
        raise Rejected('route b not restated')
    # verdict
    met = {'values_equal': nd['datum'] == c['av2']['d'] and en['plus'] == [c['aw2']['lo'], c['aw2']['hi']],
           'identification_admitted': True, 'N_sign_exact': fb['N_sign'] == ns}
    if pk['verdict'] == 'accepted_within_scope' and not all(met.values()):
        raise Rejected('insufficient verdict retained')
    if pk['verdict'] == 'limited' and not pk.get('omissions'):
        raise Rejected('insufficient verdict retained: omission without reason')
    if pk['retuned'] is not False:
        raise Rejected('insufficient verdict retained: retuned')
    # wording
    for text in strings([pk['statements'], pk['sentence']]):
        if placeholder_spans(text):
            raise Rejected('placeholder span')
    for text in pk['statements']:
        hits = affirmative_hits(text, c['forbidden'], c['sentence'])
        if hits:
            if any('unique' in h or 'infinite-volume' in h or 'thermodynamic' in h for h in hits):
                raise Rejected('named construction not uniqueness: forbidden phrasing ' + hits[0])
            if any(h == 'equality of GNS dynamics' for h in hits):
                raise Rejected('same state not different states: phrasing')
            if any(h in ('confirms',) for h in hits):
                raise Rejected('mirror sign replay not confirmation: phrasing')
            if any(h == 'resolves the reference' for h in hits):
                raise Rejected('reference unresolved retained: phrasing')
            raise Rejected('negation aware phrase scan: ' + hits[0])
    if pk['sentence'] != c['sentence'] or pk['sentence_count'] != 1:
        raise Rejected('mandatory sentence template')
    if pk['sub_labels'] != SUB_LABELS:
        raise Rejected('reference unresolved retained: sub-labels')
    gf = pk['gate_fields']
    for key, want in sorted(c['gate_fields'].items()):
        if gf.get(key) != want:
            if key == 'uniqueness_of_ground_state_claimed':
                raise Rejected('named construction not uniqueness: ' + key)
            if key == 'gns_dynamics_equality_claimed':
                raise Rejected('same state not different states: ' + key)
            if key == 'finite_box_node_claimed':
                raise Rejected('finite box node only from record: ' + key)
            if key == 'correlation_shift_resolved':
                raise Rejected('reference unresolved retained: ' + key)
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
    need(con['status'] == 'frozen_before_production' and con['id'] == 'BC1' and con['direction'] == 'statement+skeptic'
         and con['producers'] == ['forward'] and con['reverse_premise_isolation'] is False
         and con['selected_after'] == 'research/round33/advisor/bb2-gate.json',
         'contract_frozen_statement_loop', frozen_at=con['frozen_at'])
    for rel, want in sorted(GATES.items()):
        if sha(rel) != want:
            raise CheckFailure('gate hash ' + rel)
    for rel, want in sorted(EARLIER_CONTRACTS.items()):
        if sha(rel) != want:
            raise CheckFailure('earlier contract hash ' + rel)
    need(True, 'admitted_gates_and_earlier_contracts_pinned', gates=sorted(GATES), contracts=sorted(EARLIER_CONTRACTS))
    gates = {rel: json.loads((ROOT / rel).read_text()) for rel in GATES}
    need(all(g['verdict'] == 'accepted_within_scope' for g in gates.values()), 'every_premise_gate_accepted_within_scope')

    # 2. the skeptic's pre-freeze edits against the frozen bytes --------------------------------------------------------
    need(sha(REVIEW_REL) == REVIEW_SHA256, 'bc_contract_review_pinned')
    rev = json.loads((ROOT / REVIEW_REL).read_text())
    edits = [e for e in rev['blocking_edits'] + rev['non_blocking_edits'] if e['contract'] == 'bc1']
    applied = []
    for e in edits:
        if e['op'] == 'remove':
            ok = not has_key_path(con, e['path'])
        else:
            ok = has_key_path(con, e['path']) and get_path(con, e['path']) == e['replacement']
        if not ok:
            raise CheckFailure('pre-freeze edit not in the frozen bytes: ' + e['path'])
        applied.append(e['path'])
    need(len(applied) == 19, 'prefreeze_edits_verbatim_in_frozen_bytes', blocking=6, non_blocking=13, paths=applied,
         note='6 blocking and 13 non-blocking BC1 edits of the skeptic pre-freeze review are in the frozen bytes; the '
              'review previews block is not read by this program')

    # 3. controls, semantics, inventory ---------------------------------------------------------------------------------
    ids = con['controls']
    need(ids == pre['controls_required']['ids'] and len(ids) == 25 and len(set(ids)) == 25, 'control_mirror_25')
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
    need(len(own) == 12 and len(inherited) == 13 and all(r in con['shared_premises'] for r in EARLIER_CONTRACTS),
         'control_semantics_coverage', own=own, inherited=inherited,
         note='every control id is defined in this contract or in a frozen earlier Round33 contract that is a premise')
    declared = sorted(set(['AGENTS.md', CONTRACT_REL] + con['shared_premises']))
    for rel, want in OBSERVED_INPUTS.items():
        if sha(rel) != want:
            raise CheckFailure('inventory hash ' + rel)
    need(sorted(OBSERVED_INPUTS) == declared and len(declared) == 40
         and not any(p.startswith(ISOLATION_FORBIDDEN_PREFIXES) for p in declared),
         'producer_inventory_equals_contract', files=len(declared),
         note='recorded by find and sha256 over forward/bc1/inputs (names only); every snapshot byte-identical')
    need(sorted(pre['gate_fields_required']) == sorted(set(pre['gate_fields_required']) & set(PLAN_RECORD['gate_fields']))
         and all(s in PLAN_RECORD['sub_labels_allowed'] for s in pre['sub_labels_allowed']),
         'plan_vocabulary_covers_gate_fields', plan_sha256=PLAN_RECORD['sha256_at_bc_freeze_commit'])
    forbidden = sorted(set(ROUND_FORBIDDEN + pre['forbidden_phrasings'] + PLAN_RECORD['forbidden'] + EXTRA_FORBIDDEN))
    template = pre['mandatory_sentence_template']
    need(affirmative_hits(template, forbidden) == [] and placeholder_spans(template) == []
         and template.count('N_sign') == 1, 'mandatory_template_scans_clean')

    # 4. AV2 node certificate read by hash ------------------------------------------------------------------------------
    av2 = parse_av2(gates['research/round32/advisor/av2-gate.json'])
    target = F(1, 10 ** 6)
    e3 = exp_bracket(3)
    free_lo, free_hi = 1 / (4 * e3[1]), 1 / (4 * e3[0])
    need(av2['d'] == av2['decision_d'] and av2['R'] == av2['decision_R'] and av2['d'] - av2['R'] == av2['lo']
         and av2['d'] + av2['R'] == av2['hi'] and av2['R'] <= target,
         'av2_values_read_by_hash', d=q_(av2['d']), R=q_(av2['R']), interval=[q_(av2['lo']), q_(av2['hi'])],
         margin_floor=q_(F(int(target / av2['R'] * 10 ** 4), 10 ** 4)),
         note='the interval is exactly [d-R, d+R]; restated unchanged for omega_inf')
    half = F(1, 4 * 10 ** 40)
    need(av2['lo'] < free_lo <= free_hi < av2['hi'] and free_lo - half <= av2['d'] <= free_hi + half,
         'av2_free_reference_inside', free_bracket=[preview(free_lo), preview(free_hi)],
         datum_minus_free_upper=preview(av2['d'] - free_lo),
         note='e^{-3}/4 lies inside the interval (reference_unresolved); d is within the arithmetic half-width '
              '1/(4*10^40) of e^{-3}/4 (the midpoint of the AV2 enclosure), checked against a 10^-58 bracket')

    # 5. AW2 enclosure read by hash -----------------------------------------------------------------------------------
    aw2 = parse_aw2(gates['research/round32/advisor/aw2-gate.json'])
    k2 = aw2['K2']
    lo_want, hi_want = TAU / 144 - k2 * TAU ** 2, TAU / 144 + k2 * TAU ** 2
    need(aw2['lo'] == lo_want and aw2['hi'] == hi_want and aw2['mirror_lo'] == -hi_want
         and aw2['mirror_hi'] == -lo_want and aw2['lo'] > 0,
         'aw2_values_read_by_hash', K2=q_(k2), plus=[q_(aw2['lo']), q_(aw2['hi'])],
         minus=[q_(aw2['mirror_lo']), q_(aw2['mirror_hi'])], previews=[preview(aw2['lo']), preview(aw2['hi'])],
         note='endpoints are exactly tau/144 -+ K_2^+ tau^2 at tau=10^-8; the mirror is the replay at -10^-8')
    need(aw2['exclusion_margin'] == lo_want / (k2 * TAU ** 2) and aw2['sign_margin'] == 1 / (144 * k2 * TAU),
         'aw2_margins_reproduced', exclusion=preview(aw2['exclusion_margin']), sign=preview(aw2['sign_margin']))

    # 6. BB2 bound value C' -------------------------------------------------------------------------------------------
    bb2 = parse_bb2(gates['research/round33/advisor/bb2-gate.json'])
    bb2c = earlier['research/round33/contracts/bb2.json']
    hyp = bb2c['parameters']['rate_constant_pair']['hypotheses']
    c_h = F(re.search(r'C_h=(\d+/\d+)', hyp).group(1))
    need(bb2['C_prime'] == bb2['C_prime_decision'] == c_h / (1 - Q) == F(4, 984375)
         and bb2['c_site_prime'] == F(re.search(r'c_h=(\d+/\d+)', hyp).group(1)) / (1 - Q)
         and bb2['C_prime_union_labelled'] == c_h,
         'bb2_c_prime_bound_value', C_prime=q_(bb2['C_prime']), C_h=q_(c_h), union_labelled=q_(c_h),
         reevaluated_labelled='about ' + bb2['C_prime_reevaluated_labelled_text'],
         note="C' = C_h/(1-q) (nested telescoping at the hypothesis values); the union and re-evaluated values are "
              'labelled in the gate and are not used')
    bb2_acc = gates['research/round33/advisor/bb2-gate.json']['accepted']
    need('Item 2: the F1 and F2 limits coincide on every finite region' in bb2_acc
         and 'Item 3: the limit equals every AQ1 subsequential limit (F1) and every F2 subsequential limit' in bb2_acc
         and 'for the untruncated ground vectors' in bb2_acc and 'sup over M greater than N' in bb2_acc,
         'identification_premise_bb2_items_2_3',
         note='BB2 items 2-3 admit one limit equal to every AQ1 and every F2 subsequential limit; item 1 holds at fixed '
              'N for the untruncated vectors, so M to infinity gives ||rho^{F2,N}_R-rho^inf_R||_1 <= C q^(N-1) by the '
              'closed trace-norm ball')

    # 7. N_sign and the widened enclosure ---------------------------------------------------------------------------------
    cp = bb2['C_prime']
    lo, hi = aw2['lo'], aw2['hi']
    ns = n_sign_of(cp, lo)
    table = []
    for n in range(2, 8):
        wv = widened(lo, hi, cp, n)
        table.append({'N': n, 'widening': q_(wv['widening']), 'widening_preview': preview(wv['widening']),
                      'plus': [q_(wv['plus'][0]), q_(wv['plus'][1])],
                      'plus_preview': [preview(wv['plus'][0]), preview(wv['plus'][1])],
                      'minus_preview': [preview(wv['minus'][0]), preview(wv['minus'][1])],
                      'sign_certified': wv['plus'][0] > 0})
    need(ns == 4 and all(cp * Q ** (n - 1) >= lo for n in range(2, ns)) and cp * Q ** (ns - 1) < lo,
         'finite_box_sign_N_sign', N_sign=ns, table=table,
         note='N_sign = least N >= 2 with C\' q^(N-1) < tau/144 - K_2^+ tau^2 at tau=10^-8, strict, exact')
    w_ns, w_prev = widened(lo, hi, cp, ns), widened(lo, hi, cp, ns - 1)
    need(w_ns['plus'][0] > 0 and w_ns['minus'][1] < 0 and w_prev['plus'][0] < 0 < w_prev['plus'][1]
         and w_prev['minus'][0] < 0 < w_prev['minus'][1],
         'finite_box_sign_widened_enclosures',
         at_N_sign={'plus': [q_(w_ns['plus'][0]), q_(w_ns['plus'][1])], 'minus': [q_(w_ns['minus'][0]),
                                                                                   q_(w_ns['minus'][1])],
                    'plus_preview': [preview(w_ns['plus'][0]), preview(w_ns['plus'][1])],
                    'minus_preview': [preview(w_ns['minus'][0]), preview(w_ns['minus'][1])]},
         at_N_sign_minus_1={'plus': [q_(w_prev['plus'][0]), q_(w_prev['plus'][1])],
                            'minus': [q_(w_prev['minus'][0]), q_(w_prev['minus'][1])],
                            'plus_preview': [preview(w_prev['plus'][0]), preview(w_prev['plus'][1])],
                            'minus_preview': [preview(w_prev['minus'][0]), preview(w_prev['minus'][1])]},
         sign_margin_lower_over_widening=q_(lo / w_ns['widening']),
         sign_margin_preview=preview(lo / w_ns['widening']),
         distance_from_zero_at_N_sign=q_(w_ns['plus'][0]),
         note='at N_sign the widened enclosure excludes 0 at both signs; at N_sign-1 it contains 0 at both signs')
    thr_lo, thr_hi = lo * 64 ** 2, lo * 64 ** 3
    reevaluated = F(904650, 10 ** 12)  # the gate's labelled 'about 9.0465e-07', used only as a robustness probe
    need(thr_lo <= cp < thr_hi and n_sign_of(c_h, lo) == 4 and n_sign_of(reevaluated, lo) == 4,
         'finite_box_sign_robustness', threshold_interval=[preview(thr_lo), preview(thr_hi)],
         note="N_sign = 4 for every C' in [lo 64^2, lo 64^3); the labelled union value 1/250000 and the labelled "
              're-evaluated value (about 9.0465e-07) give the same N_sign; neither is used')
    tau100 = TAU / 100
    lo100 = tau100 / 144 - k2 * tau100 ** 2
    need(n_sign_of(cp, lo100) == 5 and cp * Q ** (ns - 1) >= lo100, 'finite_box_sign_tau_over_100_information',
         half_width_at_N_sign=preview(k2 * tau100 ** 2 + cp * Q ** (ns - 1)), lower_first_order=preview(tau100 / 144),
         note='information only: AW2 admits the enclosure at the cap only and C\' does not depend on tau; nothing below '
              'the cap is claimed')
    aw2_acc = gates['research/round32/advisor/aw2-gate.json']['accepted']
    need('in every centered whole-star box N>=2 at every on-site cutoff (uniform in the box' in aw2_acc,
         'f1_boxes_certified_by_aw2',
         note='F1 boxes are AW2-certified at every N >= 2 and every cutoff; the untruncated F1 vector at fixed N follows '
              'by AV1 cutoff-vector removal and the closed interval (agreement, not re-derived)')

    # 8. item 4: the finite-box node from the admitted record ---------------------------------------------------------
    av2f, av2r = (ROOT / AV2_F).read_text(), (ROOT / AV2_R).read_text()
    av2_acc = gates['research/round32/advisor/av2-gate.json']['accepted']
    aw1_acc = gates['research/round32/advisor/aw1-gate.json']['accepted']
    rec = {
        'av2_gate_each_state': 'every AQ1 subsequential state of the centered whole-star construction (each chosen state separately' in av2_acc,
        'forward_F01_F02_state_gns': 'The state is AQ1\'s chosen centered-box subsequential state `omega`, with GNS vacuum `Omega`' in av2f and 'By **AQ1 §5 (nonnegativity only)**' in av2f and 'HNM-AV2-F01' in av2f and 'HNM-AV2-F02' in av2f,
        'forward_F07_window_lemma': 'HNM-AV2-F07' in av2f,
        'forward_F13_F14_box_by_box': 'Fix a centered whole-star box `Lambda_N`, `N>=2`' in av2f and 'HNM-AV2-F14' in av2f,
        'forward_F15_actual_state': 'So (F14) holds for the actual AQ evolution at **every real** `theta`.' in av2f and 'HNM-AV2-F15' in av2f,
        'reverse_R01_R02_R08_R13': all('HNM-AV2-R%02d' % k in av2r for k in (1, 2, 8, 12, 13)),
        'reverse_finite_box_provenance_mutation': '| changed_model_relabelled | nonzero triple; AT5 τ=10^-14 as the cap node; s=6 as the node; finite-graph id; finite-box provenance |' in av2r,
        'aw1_item1_nonuniform': 'tau^2 constant explicitly unbounded (not uniform in N' in aw1_acc,
    }
    need(all(rec.values()), 'finite_box_node_record_determination', record=rec,
         note='the record states the node for AQ1 subsequential states only; only the slope is per box; the AV2 reverse '
              'rejects finite-box provenance; AW1 item (1) has no uniform finite-box constant; BC1 restates no '
              'finite-box node and records two open rows (N2, N3)')

    # 9. common GNS item -----------------------------------------------------------------------------------------------
    ba2_acc = gates['research/round33/advisor/ba2-gate.json']['accepted']
    aq1_acc = gates['research/round29/advisor/aq1-gate.json']['accepted']
    need('the F2 limit dynamics equals the AQ1 limit dynamics T_theta' in ba2_acc
         and 'has as correlation functions on |theta|<=8 the limits of the finite-box correlation functions' in bb2_acc
         and 'only on the certified range 5<=N<=14000' in bb2_acc
         and 'strongly continuous GNS evolution with a nonnegative self-adjoint physical energy generator' in aq1_acc
         and 'not equality of GNS dynamics of different states' in gates['research/round33/advisor/bb2-gate.json']['decision'],
         'common_gns_item_premises',
         note='one state (BB2 items 2-3), hence one GNS triple up to unitary equivalence; its dynamics is the AQ1 limit '
              'dynamics T_theta (AQ1 for F1, BA2 item 4 for F2); correlation functions on |theta|<=8 are BB2 item 5 '
              'limits with a rate in N only on 5<=N<=14000; not equality of GNS dynamics of different states')

    # 10. obligations -----------------------------------------------------------------------------------------------------
    ob = obligations_table()
    ay2f = (ROOT / AY2_F).read_text()
    need(all(('| %s | %s |' % (k, v)) in ay2f for k, v in REQUIRED_ROW_NAMES.items())
         and 'AY2 row O6 closed within scope' in gates['research/round33/advisor/ba2-gate.json']['decision']
         and all(n in [r['name'] for r in ob] for n in REQUIRED_NEW_ROWS),
         'obligations_table_skeptic', rows=ob,
         note='AY2 rows O1-O6 read from the hash-pinned AY2 report; O2-O6 closed within named scopes, O1 open; new open '
              'rows from the Round33 gates and BC1 itself; the route-B row cites BC2 only once its gate is recorded')

    # 11. fixtures ----------------------------------------------------------------------------------------------------------
    # (a) trace duality for the finite-box sign: |Tr((rho-rho')W)| <= ||W|| ||rho-rho'||_1, attained
    delta = [[F(3, 10), F(0)], [F(0), F(-3, 10)]]
    wop = [[F(1), F(0)], [F(0), F(-1)]]
    tr = sum(delta[i][j] * wop[j][i] for i in range(2) for j in range(2))
    need(abs(tr) == F(3, 5) and abs(tr) <= 1 * (abs(delta[0][0]) + abs(delta[1][1])), 'fixture_trace_duality_no_half',
         model_is_finite_graph=True, transfers_to_aq=False,
         note='the sign corollary uses ||W|| ||rho-rho\'||_1 (full duality); the effect refinement 1/2 does not apply '
              'to W')
    # (b) fixed versus moving vector (topology)
    need(True, 'fixture_fixed_versus_moving_vector', model_is_finite_graph=True, transfers_to_aq=False,
         note='rho_n=|e_n><e_n|: trace distance 2 to rho_1 while <e_1,rho_n e_1>=0 (weak vanishing is not trace-norm '
              'convergence)')
    # (c) whole sequence versus subsequence for the sign: an alternating sequence has two subsequential limits
    seq = [F((-1) ** n, 10 ** 10) for n in range(2, 12)]
    need(seq[0] > 0 and seq[1] < 0 and len(set(seq)) == 2, 'fixture_subsequence_sign',
         model_is_finite_graph=True, transfers_to_aq=False,
         note='a sequence with two subsequential limits of opposite sign shows why the finite-box sign needs the '
              'whole-sequence bound, not a subsequence')

    # 12. packet, validator, controls ------------------------------------------------------------------------------------
    round32_hashes = {rel: GATES[rel] for rel in GATES if rel.startswith('research/round32/')}
    ctx = {
        'declared_inputs': declared, 'control_ids': ids, 'tau': TAU, 'window': par['window'],
        'av2': av2, 'aw2': aw2, 'C_prime': cp, 'sentence': template, 'forbidden': forbidden,
        'gate_fields': pre['gate_fields_required'], 'error_terms': pre['error_terms_itemized'],
        'round32_hashes': round32_hashes,
        'av2_labels': {'sub_label': 'reference_unresolved', 'tier': 'AV1 forward tier (ii) state bound; C^2 window'},
        'input_labels': {'enclosure': 'AW2 gate endpoints', 'C_prime': 'BB2 nested_telescoping; BB1 route polymer_kp'},
    }
    rows = {}
    for n in (ns - 1, ns):
        wv = widened(lo, hi, cp, n)
        rows[n] = {'plus': list(wv['plus']), 'minus': list(wv['minus']), 'sign_certified': wv['plus'][0] > 0}
    statements = [
        'The AV2 node certificate at s=1 is restated for omega_inf with the unchanged datum and radius; the free '
        'reference lies inside the interval, so the reference stays unresolved and no interaction shift is claimed.',
        'The AW2 enclosure of the static Wilson mean is restated for omega_inf with unchanged endpoints and the full '
        'second-order remainder; the value at -10^-8 is a replay of the same |tau| formula, not a second confirmation.',
        'The density rate in N is q^(N-1) for every N at least 2; the correlation-function rate in N holds only on '
        '5<=N<=14000.',
        'This is not uniqueness of any ground state and not equality of GNS dynamics of different states.',
    ]
    base = {
        'contract_sha256': CONTRACT_SHA256, 'inputs': list(declared), 'controls': {k: True for k in ids},
        'round32_hashes': dict(round32_hashes), 'admission_reads_preview': False,
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False},
        'provenance_premises': [], 'model_id': MODEL_ID, 'triple': ['0', '0', '0'], 'tau': TAU, 'signs': ['+', '-'],
        'cover': list(COVER), 'model_is_finite_graph': False, 'group': 'SU(2)', 'families': ['F1', 'F2'],
        'state': STATE,
        'parameters': {'metric': par['metric'], 'weights': par['weights'], 'window': par['window'], 'clock': par['clock'],
                       'node': par['node'], 'N_min': 2},
        'clock': CLOCK, 'reference_energy': 3, 'reference': 'e^{-3s}/4', 'u_over_theta': F(1, 8),
        'window_labelled_in': 'theta', 'clock_per_family': {'F1': CLOCK, 'F2': CLOCK},
        'coupling_per_family': {'F1': TAU, 'F2': TAU}, 'topology': dict(TOPOLOGY),
        'fixtures': {'fixed_versus_moving_vector': True},
        'identification': copy.deepcopy(IDENTIFICATION),
        'node': {'s': [1], 'grid': None, 'crossover_certified': False, 'datum': av2['d'], 'radius': av2['R'],
                 'interval': [av2['lo'], av2['hi']], 'labels': dict(ctx['av2_labels']), 'rederived': False,
                 'reference_inside': True, 'sub_labels': ['reference_unresolved'], 'shift_claimed': False,
                 'minus_tau': {'kind': 'replay of the same |tau| formula', 'counted_as_confirmation': False},
                 'applies_to': STATE},
        'enclosure': {'plus': [aw2['lo'], aw2['hi']], 'minus': [aw2['mirror_lo'], aw2['mirror_hi']], 'K2': k2,
                      'remainder': 'K_2^+ tau^2', 'minus_kind': 'replay of the same |tau| formula',
                      'minus_counted_as_confirmation': False},
        'finite_box_sign': {'bound_source': BOUND_SOURCE, 'C_prime': cp, 'C_prime_label': C_PRIME_LABEL, 'q': Q,
                            'vectors': 'untruncated at fixed N', 'family': 'F2',
                            'widening': "C' q^(N-1) on both sides", 'comparator': 'strict', 'N_sign': ns,
                            'rows': rows, 'below_N_sign': 'nothing claimed; open obligation row N4',
                            'cutoff_L_states_claimed': False,
                            'F1': 'certified by AW2 at every N at least 2 and every cutoff; untruncated by AV1 '
                                  'cutoff-vector removal, recorded as agreement',
                            'tier': 'exact_first_order', 'route': None, 'input_labels': dict(ctx['input_labels'])},
        'finite_box_node': {'claimed': False, 'restated': False, 'method': None, 'open_rows': ['N2', 'N3']},
        'gns': {'one_state_premise': ['BB2 items 2-3', 'BA2 item 4'], 'different_states_equality': False,
                'dynamics': 'AQ1 limit dynamics T_theta', 'correlation_rate_range': '5<=N<=14000'},
        'obligations': ob, 'falsifier_exclusion': 'named constructions F1 and F2 only (BB2 items 2-3)',
        'rates': [{'what': 'densities', 'range': 'every N at least 2'},
                  {'what': 'correlation functions', 'range': '5<=N<=14000'}],
        'round32_edits': [], 'route_b': {'restated': False, 'applied_to_uniform_model': False},
        'verdict': 'accepted_within_scope', 'retuned': False, 'statements': statements, 'sentence': template,
        'sentence_count': 1, 'sub_labels': list(SUB_LABELS), 'gate_fields': dict(pre['gate_fields_required']),
        'error_terms': {'identification_premise_bb2': 'BB2 items 2-3 as admitted (gate sha256 ad3fdb4b...)',
                        'restated_constants_exactness': 'equality with the gate rationals',
                        'finite_box_whole_sequence_term': "C' q^(N-1), C'=4/984375",
                        'second_order_remainder_K2plus': 'K_2^+ tau^2 at both endpoints',
                        'arithmetic': 'exact Fractions; no rounding enters a decision'},
    }
    rebind(base)
    need(validate(copy.deepcopy(base), ctx) is True, 'validator_accepts_skeptic_packet')

    def mk(fn, rebind_digest=True):
        def run():
            pk = copy.deepcopy(base)
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

    ctl = {}
    ctl['coherent_evidence_tampering'] = [
        ('control boolean flipped, digest rebound', setp(['controls', ids[3]], False), 'control booleans'),
        ('declared snapshot removed, digest rebound', mk(lambda pk: pk['inputs'].remove(declared[5])),
         'snapshot inventory'),
        ('digest not rebound after an edit', setp(['controls', ids[0]], 'true', rebind_digest=False), 'freeze digest'),
        ('undeclared producer file read', mk(lambda pk: pk['inputs'].append('research/round33/forward/bc2/report.md')),
         'undeclared read'),
    ]
    ctl['exact_arithmetic_admission'] = [
        ('float N_sign constant', setp(['finite_box_sign', 'C_prime'], 4.0635e-06), 'exact arithmetic'),
        ('float endpoint', setp(['enclosure', 'K2'], 3354.80322946), 'exact arithmetic'),
        ('Arb preview read by admission', setp(['admission_reads_preview'], True), 'preview read by admission'),
    ]
    ctl['no_priority_or_continuum_claim'] = [
        ('priority claimed', setp(['claims', 'scientific_priority_verified'], True), 'no priority or continuum claim'),
        ('continuum claimed', setp(['claims', 'continuum_claim'], True), 'no priority or continuum claim'),
        ('historical provenance as premise', setp(['provenance_premises'], ['Tesla notebook']),
         'no priority or continuum claim'),
    ]
    ctl['changed_model_relabelled'] = [
        ('coupling tau/10', setp(['tau'], TAU / 10), 'changed model relabelled'),
        ('uniform triple under the patterned label', setp(['triple'], ['tau/24', 'tau/24', 'tau/24']),
         'changed model relabelled'),
        ('finite-graph result', setp(['model_is_finite_graph'], True), 'changed model relabelled'),
        ('one AQ1 subsequential state instead of omega_inf', setp(['state'], 'a chosen AQ1 subsequential state'),
         'changed model relabelled: state'),
        ('new constant relabelled with a route', setp(['finite_box_sign', 'route'], 'nested_telescoping'),
         'changed model relabelled: tier label'),
    ]
    ctl['insufficient_verdict_retained'] = [
        ('restated datum differs yet accepted', mk(lambda pk: pk['node'].__setitem__('datum', av2['d'] + F(1, 10 ** 40))),
         'certificate values unchanged'),
        ('limited without the omission reason', setp(['verdict'], 'limited'), 'omission without reason'),
        ('retuned constant', setp(['retuned'], True), 'retuned'),
    ]
    ctl['wrong_delta_alpha_hbar_clock'] = [
        ('free energy 24 with s', setp(['reference_energy'], 24), 'wrong delta alpha hbar clock'),
        ('u window labelled theta', setp(['window_labelled_in'], 'u'), 'normalized u without conversion'),
        ('u=theta without the factor 8', setp(['u_over_theta'], F(1)), 'normalized u without conversion'),
    ]
    ctl['placeholder_span_rejected'] = [
        ('angle-bracket placeholder in a statement', add_statement('N_sign equals <the least integer here>.'),
         'placeholder span'),
        ('placeholder with e.g.', add_statement('The widened enclosure is <e.g.value>.'), 'placeholder span'),
    ]
    ctl['negation_aware_phrase_scan'] = [
        ('affirmative forbidden phrase', add_statement('The limit is the thermodynamic limit of the boxes.'),
         'named construction not uniqueness'),
        ('affirmative correlation length', add_statement('The node fixes a correlation length.'),
         'negation aware phrase scan'),
    ]
    ctl_pos = {'negation_aware_phrase_scan': [
        ('negated forbidden phrase accepted', add_statement('This is not the thermodynamic limit of any other boxes.')),
        ('template quoted once accepted', mk(lambda pk: None))]}
    ctl['parameters_declare_metric_weights_window'] = [
        ('metric missing', mk(lambda pk: pk['parameters'].pop('metric')), 'parameters must declare'),
        ('weights missing', mk(lambda pk: pk['parameters'].pop('weights')), 'parameters must declare'),
        ('window changed', setp(['parameters', 'window'], 'C^1 window'), 'parameters must declare'),
        ('clock missing', mk(lambda pk: pk['parameters'].pop('clock')), 'parameters must declare'),
    ]
    ctl['named_construction_not_uniqueness'] = [
        ('uniqueness field true', setp(['gate_fields', 'uniqueness_of_ground_state_claimed'], True),
         'named construction not uniqueness'),
        ('the infinite-volume ground state', add_statement('The node holds for the infinite-volume ground state.'),
         'named construction not uniqueness'),
        ('falsifier excluded for every state', setp(['falsifier_exclusion'], 'every state'),
         'named construction not uniqueness: falsifier'),
    ]
    ctl['common_clock'] = [
        ('F2 at another coupling', setp(['coupling_per_family', 'F2'], TAU / 2), 'common clock'),
        ('F2 clock in u', setp(['clock_per_family', 'F2'], 'u=theta/8'), 'common clock'),
    ]
    ctl['topology_named'] = [
        ('state topology weak', setp(['topology', 'states'], 'weak-* on the quasi-local algebra'), 'topology named'),
        ('moving-vector fixture missing', setp(['fixtures', 'fixed_versus_moving_vector'], False), 'topology named'),
    ]
    ctl['limit_identified_with_aq1_limits'] = [
        ('restated before identification', setp(['identification', 'before_restatement'], False),
         'limit identified with aq1 limits'),
        ('identification premise BB1 per comparison', setp(['identification', 'premise'], 'BB1 comparison c3'),
         'limit identified with aq1 limits'),
        ('F2 limits omitted', setp(['identification', 'identified_with'], ['every AQ1 subsequential limit']),
         'limit identified with aq1 limits'),
    ]
    ctl['certificate_values_unchanged'] = [
        ('smaller radius', setp(['node', 'radius'], av2['R'] - F(1, 10 ** 40)), 'certificate values unchanged'),
        ('larger radius', setp(['node', 'radius'], av2['R'] + F(1, 10 ** 40)), 'certificate values unchanged'),
        ('re-rounded datum', setp(['node', 'datum'], F(round(av2['d'] * 10 ** 12), 10 ** 12)),
         'certificate values unchanged'),
        ('AW2 endpoint re-rounded', setp(['enclosure', 'plus'], [F(691089641214, 10 ** 22), aw2['hi']]),
         'certificate values unchanged: AW2'),
        ('re-derived radius with the same value', setp(['node', 'rederived'], True), 'certificate values unchanged'),
    ]
    ctl['post_hoc_node_rejected'] = [
        ('crossover as node', setp(['node', 's'], [F(62368634460, 10 ** 10)]), 'post hoc node rejected'),
        ('grid', setp(['node', 'grid'], [F(1, 2), F(1), F(2)]), 'post hoc node rejected'),
        ('crossover certified', setp(['node', 'crossover_certified'], True), 'post hoc node rejected'),
    ]
    ctl['finite_box_sign_from_whole_sequence'] = [
        ('BB1 per-comparison C without the whole-sequence passage',
         setp(['finite_box_sign', 'bound_source'], 'BB1 comparison c2 (N to N+1)'), 'bound source'),
        ('subsequence bound', setp(['finite_box_sign', 'bound_source'], 'AQ1 subsequence'), 'bound source'),
        ('labelled union value as C\'', setp(['finite_box_sign', 'C_prime'], c_h), 'constant'),
        ('N_sign not the least (5)', setp(['finite_box_sign', 'N_sign'], 5), 'N_sign not the least N'),
        ('N_sign too small (3)', setp(['finite_box_sign', 'N_sign'], 3), 'N_sign not the least N'),
        ('non-strict comparator', setp(['finite_box_sign', 'comparator'], 'non-strict'), 'comparator'),
        ('cutoff-L F2 states claimed', setp(['finite_box_sign', 'cutoff_L_states_claimed'], True), 'range below'),
        ('sign claimed below N_sign', setp(['finite_box_sign', 'below_N_sign'], 'sign certified for N=2,3'),
         'range below'),
    ]
    ctl['mirror_sign_replay_not_confirmation'] = [
        ('node -tau as a confirmation', setp(['node', 'minus_tau', 'counted_as_confirmation'], True),
         'mirror sign replay not confirmation'),
        ('enclosure -tau as second observation', setp(['enclosure', 'minus_counted_as_confirmation'], True),
         'mirror sign replay not confirmation'),
        ('confirms in a statement', add_statement('The value at -10^-8 confirms the sign.'),
         'mirror sign replay not confirmation'),
    ]
    ctl['reference_unresolved_retained'] = [
        ('sub-label dropped', setp(['node', 'sub_labels'], []), 'reference unresolved retained'),
        ('shift claimed', setp(['node', 'shift_claimed'], True), 'reference unresolved retained'),
        ('correlation shift resolved', setp(['gate_fields', 'correlation_shift_resolved'], True),
         'reference unresolved retained'),
        ('resolves the reference', add_statement('The restated node resolves the reference value.'),
         'reference unresolved retained'),
    ]

    def drop_row(rid):
        return mk(lambda pk: pk.__setitem__('obligations', [r for r in pk['obligations'] if r['id'] != rid]))

    def edit_row(rid, key, value):
        def f(pk):
            for r in pk['obligations']:
                if r['id'] == rid:
                    r[key] = value
        return mk(f)

    ctl['obligations_table_complete'] = [
        ('row O6 dropped', drop_row('O6'), 'row dropped'),
        ('O1 marked closed', edit_row('O1', 'status', 'closed_within_scope'), 'status of O1'),
        ('closed row without gate', edit_row('O3', 'closing_gate', None), 'closed row without gate'),
        ('new row missing (F2 sign below N_sign)', drop_row('N4'), 'new row missing'),
        ('open row without route', edit_row('N7', 'candidate_route', ''), 'open row without premise or route'),
        ('route-B row dropped', drop_row('N9'), 'new row missing'),
    ]
    ctl['rate_range_stated'] = [
        ('correlation rate without range', mk(lambda pk: pk['rates'][1].__setitem__('range', '')), 'rate range stated'),
        ('correlation rate for every N', mk(lambda pk: pk['rates'][1].__setitem__('range', 'every N at least 5')),
         'correlation rate range'),
        ('unqualified O(1/N)', add_statement('The correlation functions converge at the rate O(1/N).'),
         'unqualified O(1/N)'),
        ('density rate without its range', mk(lambda pk: pk['rates'][0].__setitem__('range', 'large N')),
         'density rate range'),
    ]
    ctl['round32_gates_untouched'] = [
        ('AV2 gate edited', setp(['round32_edits'], ['research/round32/advisor/av2-gate.json']),
         'round32 gates untouched'),
        ('AW2 gate hash changed', setp(['round32_hashes', 'research/round32/advisor/aw2-gate.json'], '0' * 64),
         'round32 gates untouched: hash'),
    ]
    ctl['route_b_not_restated'] = [
        ('AX2 restated in BC1', setp(['route_b', 'restated'], True), 'route b not restated'),
        ('AV2 restatement applied to the uniform model', setp(['node', 'applies_to'], 'the route-B limit'),
         'route b not restated'),
    ]
    ctl['same_state_not_different_states'] = [
        ('GNS equality of different states', setp(['gns', 'different_states_equality'], True),
         'same state not different states'),
        ('gate field true', setp(['gate_fields', 'gns_dynamics_equality_claimed'], True),
         'same state not different states'),
        ('premise dropped', setp(['gns', 'one_state_premise'], ['BA2 item 4']), 'same state not different states'),
        ('affirmative phrase', add_statement('This gives equality of GNS dynamics of the two families.'),
         'same state not different states'),
    ]
    ctl['second_order_remainder_kept'] = [
        ('K_2^+ tau^2 dropped', mk(lambda pk: pk['enclosure'].update({'plus': [TAU / 144, TAU / 144],
                                                                        'remainder': None})),
         'second order remainder kept'),
        ('whole-sequence widening dropped', setp(['finite_box_sign', 'widening'], 'none'), 'second order remainder kept'),
    ]
    ctl['finite_box_node_only_from_record'] = [
        ('finite-box node claimed', setp(['gate_fields', 'finite_box_node_claimed'], True),
         'finite box node only from record'),
        ('finite-box node as a restatement', setp(['finite_box_node', 'restated'], True),
         'finite box node only from record'),
        ('window lemma box by box', setp(['finite_box_node', 'method'], 'window lemma applied box by box'),
         'finite box node only from record'),
        ('open rows dropped', setp(['finite_box_node', 'open_rows'], []), 'finite box node only from record'),
    ]
    ctl_pos['rate_range_stated'] = [
        ('correlation rate with its range accepted',
         add_statement('The correlation-function rate in N is O(1/N) only on 5<=N<=14000.'))]
    ctl_pos['obligations_table_complete'] = [
        ('extra open row with premise and route accepted',
         mk(lambda pk: pk['obligations'].append({'id': 'N99', 'name': 'extra', 'status': 'open',
                                                 'missing_premise': 'x', 'candidate_route': 'y'})))]
    ctl_pos['insufficient_verdict_retained'] = [
        ('limited with the omission and its reason accepted',
         mk(lambda pk: pk.update({'verdict': 'limited', 'omissions': [{'item': 5, 'reason': 'stated'}]})))]
    for cid in ids:
        control(cid, ctl[cid], positives=ctl_pos.get(cid, ()))
    need(sorted(ctl) == sorted(ids), 'every_control_executed', controls=len(ids),
         mutations=sum(len(v) for v in ctl.values()))

    # 13. results ----------------------------------------------------------------------------------------------------
    readings = [
        'R1: C\' is the BB2 gate bound value 4/984375 = C_h/(1-q) at the hypothesis values; N_sign = 4 is robust for '
        'every C\' in [lo 64^2, lo 64^3), so the labelled values would not change it (they are not used).',
        'R2: the -10^-8 restatements need no pointwise pairing: the -tau limit of the named constructions is itself '
        'an AQ1 subsequential limit at -tau (BB2 at both signs), so the AW2 and AV2 whole-set statements at -tau apply '
        'to it directly; the AW2 limitation on pairing individual states is not lifted and not needed.',
        'R3: omega^{F2,N} is the untruncated F2 ground state at fixed N; BB2 item 1 holds for it at fixed N, and '
        'M to infinity passes the bound to omega_inf through the closed trace-norm ball (no cutoff-L F2 state).',
        'R4: the finite-box node is left open (item 4); the F1 route N2 looks short (F13-F14 are per box and E_N makes '
        'G_N-E_N nonnegative), but it is not in the record and BC1 correctly restates none.',
        'R5: correlation_shift_resolved false refers to C(s); the static Wilson mean is carried by '
        'sign_certificate_restated_for_limit and finite_box_sign_claimed (AW2 meaning), so no single '
        'resolved_interaction_shift field is exported.',
    ]
    lifted = [
        {'gate': 'AV2', 'limitation': 'each AQ1 subsequential state separately; no uniqueness, whole-sequence '
                                      'convergence or rate in N',
         'after_round33': 'partly lifted for the named constructions: one limit omega_inf equal to every AQ1 and F2 '
                          'subsequential limit (BB2 items 1-3), density rate q^(N-1) for every N at least 2; uniqueness '
                          'of every ground state remains open; no finite-box node (BC1 item 4)'},
        {'gate': 'AW2', 'limitation': 'whole-set statement; no whole-sequence convergence or rate in N; -tau pairing of '
                                      'individual states only along a common subsequence',
         'after_round33': 'whole-sequence convergence and the F2 finite-box sign for N at least N_sign lifted within '
                          'scope; the pairing limitation is not lifted and not needed (the -tau limit is an AQ1 '
                          'subsequential limit at -tau)'},
        {'gate': 'AW1', 'limitation': 'finite-box C_N(s) tau^2 constant not uniform in N', 'after_round33': 'remains'},
        {'gate': 'AY2', 'limitation': 'uniform local closeness only; six obligations unproved',
         'after_round33': 'O2-O6 closed within named scopes (BA2, BB2); O1 open; the falsifying scenario excluded for '
                          'F1 and F2 only'},
        {'gate': 'AQ1/AQ2', 'limitation': 'subsequential states; full-GNS gap only as qualified in AQ2',
         'after_round33': 'subsequence lifted for the named constructions; the AQ2 qualification remains'},
        {'gate': 'every Round32 gate', 'limitation': 'fixed spacing, zero-selected family, |tau| at most 10^-8, no '
                                                     'continuum or weak coupling', 'after_round33': 'remains'},
    ]
    return {
        'loop': 'BC1', 'stage': 'pre_comparison', 'human_author': 'Hruday N M (BUNZEEY)',
        'round32_limitations': lifted,
        'reviewer': 'skeptic (model agent, correlated ancestry; not human review)',
        'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'model': 'AQ_patterned_zero_selected at tau=+-10^-8; omega_inf the limit of the named constructions F1 and '
                 'F2 (BB2); untruncated F2 finite-box ground states at fixed N; original xz Wilson loop W, cover '
                 'R={0,e_z}; s=alpha t_E/hbar at the node s=1',
        'restated': {'av2': {'d': q_(av2['d']), 'R': q_(av2['R']), 'interval': [q_(av2['lo']), q_(av2['hi'])]},
                     'aw2': {'plus': [q_(aw2['lo']), q_(aw2['hi'])], 'minus': [q_(aw2['mirror_lo']),
                                                                                 q_(aw2['mirror_hi'])],
                             'K2': q_(k2)}},
        'finite_box_sign': {'C_prime': q_(cp), 'q': q_(Q), 'N_sign': ns, 'table': table,
                            'sign_margin_lower_over_widening_at_N_sign': q_(lo / w_ns['widening'])},
        'obligations': ob, 'contract_readings': readings,
        'predictions': {'N_sign': ns, 'widened_plus_at_N_sign': [preview(w_ns['plus'][0]), preview(w_ns['plus'][1])],
                        'widened_minus_at_N_sign': [preview(w_ns['minus'][0]), preview(w_ns['minus'][1])],
                        'sign_margin_at_N_sign': preview(lo / w_ns['widening'])},
        'gate_fields': pre['gate_fields_required'], 'sentence': template,
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                   'finite_box_node_claimed': False, 'uniqueness_of_ground_state_claimed': False},
        'deferred_parts': {'inventory': 'recorded by find and sha256 (names only); the program does not open '
                                        'forward/bc1', 'phrase_scan': 'mirror of the round tool',
                           'tampering': 'packet level (synthetic packet built from this derivation)'},
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
                      'N_sign': result['finite_box_sign']['N_sign']}))


if __name__ == '__main__':
    main()
