#!/usr/bin/env python3
"""BB2 forward producer (assembly: nested_telescoping): exact checks for the whole-sequence
convergence of the reduced densities of the named construction families F1 and F2, their
common limit, its identification with every AQ1 and every F2 subsequential limit, its coarse
translation invariance, and the convergence of its correlation functions on |theta| <= 8.

Every conclusion that uses BB1 is derived from the BB1 FROZEN TARGETS as explicit hypotheses
(control conditional_on_bb1_targets); nothing here reads a BB1 producer, skeptic or gate file.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production (Claude model agent).

Standard library only (argparse, fractions, hashlib, itertools, json, pathlib, re).  Every
admission Boolean is decided in exact Fraction arithmetic; decimal strings are truncated
previews and are never read by an admission check.  Conditions raise AdmissionError explicitly
(never `assert`), so every check stays active under `python -O`.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round33/contracts/bb2.json'
CONTRACT_SHA256 = 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35'
BB1_REL = 'research/round33/contracts/bb1.json'
BB1_SHA256 = '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'

# Admitted gates read by this checker, pinned before any value is read from them.
PINNED_GATES = {
    'research/round33/advisor/ba2-gate.json': 'e6b163fc8f80de28c51609f77d0bef21dcdc1286638c862ad67202e6f7b0ca35',
    'research/round33/advisor/ba1-gate.json': '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/advisor/aq2-gate.json': '930b697db343ffd261c303c34e6ddd8c6e9c753ee6707931c55dc4171ee47575',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
}
NS_REL = 'research/round33/sources/nachtergaele-sims-1410.8174v1.md'
NS_SHA256 = '6a28f4cd6aa2c55286fa839d83c00356ff0709f8b02027ee5b39050df1d6c921'
NS_PDF_SHA256 = '501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba'

P_BA2_GATE = 'research/round33/advisor/ba2-gate.json'
P_BA1_GATE = 'research/round33/advisor/ba1-gate.json'
P_AQ1_GATE = 'research/round29/advisor/aq1-gate.json'
P_AQ2_GATE = 'research/round29/advisor/aq2-gate.json'
P_AM2_GATE = 'research/round29/advisor/am2-gate.json'
P_AV1_GATE = 'research/round32/advisor/av1-gate.json'
P_AY1_GATE = 'research/round32/advisor/ay1-gate.json'
P_AY2_GATE = 'research/round32/advisor/ay2-gate.json'
P_BA2F = 'research/round33/forward/ba2/report.md'
P_BA1R = 'research/round33/reverse/ba1/report.md'
P_AQ1 = 'research/round29/forward/aq1/report.md'
P_AQ2 = 'research/round29/forward/aq2/report.md'
P_AV1F = 'research/round32/forward/av1/report.md'
P_AY1F = 'research/round32/forward/ay1/report.md'
P_I1 = 'research/round21/forward/i1/report.md'
P_SEL = 'research/round33/advisor/selection-bb2.md'
REPORT = 'report.md'

ASSEMBLY = 'nested_telescoping'
STATE_TIER = 'exact_first_order'
DYN_TIER = 'polynomial_lieb_robinson'
DYN_ROUTE = 'duhamel_inner_f1'
HYP_SOURCE = 'bb1_frozen_targets'
COND = 'conditional_on_bb1_targets'

# Verbatim quotations from the committed Nachtergaele-Sims excerpt (Part A, and one Part B block).
NS_QUOTES = {
    'eq77': '(77) τ_t(A) = lim_{Λ→Γ} τ_t^Λ(A)',
    'thm41_tail': ('exists and the convergence is uniform for t in compact sets. The limit may be taken along any increasing '
                   'sequence of finite sets Λ which tend to Γ, and the result is independent of the particular sequence. This '
                   'limiting dynamics τ_t(·) can be uniquely extended to a one-parameter group of *-automorphisms on A_Γ.'),
    'eq51': '(51) ‖[τ_t^Λ(A), B]‖ ≤ (2‖A‖‖B‖ / C) (e^{2‖Φ‖C|t|} − 1) D(X, Y)',
    'eq53_condition': 'If Φ ∈ B(Γ, F_a) with F_a(r) = e^{−ar}F(r) for some a > 0, then (53)',
    'quasi_local_partB': ('where the union taken over all finite subsets of Γ. The completion of AlocΓ with respect to the\n'
                          'operator norm, which we denote by AΓ , is a C ∗ -algebra, and it will be called the algebra of all\n'
                          'quasi-local observables.'),
}


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


def rat(value):
    """Exact rational input only: int, Fraction or an integer/ratio string."""
    if isinstance(value, bool) or isinstance(value, float):
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
    e = 0
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


def read_input(rel):
    return (BASE / 'inputs' / rel).read_text(encoding='utf-8')


def load_json_input(rel):
    return json.loads(read_input(rel))


def match(pattern, text, label, flags=0):
    m = re.search(pattern, text, flags)
    require(m is not None, 'premise text not parsed: ' + label)
    return m


def exp_upper(x):
    """Directed rational upper bound of e^x for 0 <= x < 1: e^x <= 1/(1-x) because e^(-x) >= 1-x."""
    x = rat(x)
    require(0 <= x < 1, 'exp enclosure radius')
    return 1 / (1 - x)


# ---------------------------------------------------------------------------
# Contracts: both sha256 values are verified before any field is parsed.
# ---------------------------------------------------------------------------
def load_contracts():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen BB2 contract')
    raw1 = (BASE / 'inputs' / BB1_REL).read_bytes()
    digest1 = sha_bytes(raw1)
    require(digest1 == BB1_SHA256, 'BB1 contract snapshot bytes differ from the frozen BB1 contract')
    c = json.loads(raw.decode('utf-8'))
    b1 = json.loads(raw1.decode('utf-8'))
    require(c.get('id') == 'BB2' and c.get('status') == 'frozen_before_production', 'wrong BB2 contract identity')
    require(b1.get('id') == 'BB1' and b1.get('status') == 'frozen_before_production', 'wrong BB1 contract identity')
    return c, digest, b1, digest1


def bracket(text, label):
    m = match(r'\[(\d+(?:/\d+)?),(\d+(?:/\d+)?)\]', text, label)
    return (rat(m.group(1)), rat(m.group(2)))


def contract_values(c, b1):
    p = c['parameters']
    pre = c['preregistration']
    v = {'model': c['model'], 'parameters': p}
    for frag in ('Zero-selected patterned family', '|tau|<=10^-8', 'F1 (AQ1 centered whole-star boxes)',
                 'F2 (I1 section 6 all-contained-face boxes with padding)', 'R={0,e_z}', 'trace norm on B(H_Y)',
                 '|theta| at most 8 in theta=alpha t/hbar'):
        require(frag in c['model'], 'model string fragment missing: ' + frag)
    rcp = p['rate_constant_pair']
    hyp = rcp['hypotheses']
    require('for every BB1 comparison, both signs, in each on-site cutoff space and at fixed N for the untruncated ground vectors' in hyp,
            'hypothesis quantifiers')
    m = match(r'q=(\d+/\d+), C_h=(\d+/\d+) and c_h=(\d+/\d+)', hyp, 'hypothesis pair')
    v['q'], v['C_h'], v['c_h'] = rat(m.group(1)), rat(m.group(2)), rat(m.group(3))
    m = match(r'secondary q_2=(\d+)\|tau\|, C_2h=(\d+/\d+), c_2h=(\d+/\d+)', hyp, 'secondary hypothesis pair')
    v['q2_per_tau'], v['C_2h'], v['c_2h'] = rat(m.group(1)), rat(m.group(2)), rat(m.group(3))
    require('||rho^{box1}_R-rho^{box2}_R||_1 at most C_h q^(N-1)' in hyp
            and '||rho^{box1}_Y-rho^{box2}_Y||_1 at most c_h |Y| e^{|Y|/10^8} q^{d_Y}' in hyp, 'hypothesis forms')
    hd = rcp['headline']
    v['q_head'] = rat(hd['q'])
    v['target_Cp'] = rat(hd['C_prime_target'])
    v['target_cp'] = rat(hd['c_site_prime_target'])
    require(hd['tier'] == STATE_TIER and 'nested_telescoping (forward)' in hd['assembly']
            and 'nondecreasing in each' in hd['note'], 'headline tier, assembly and monotonicity note')
    dy = rcp['dynamics']
    v['target_Cdyn'] = rat(dy['C_dyn_target'])
    require(dy['tier'] == DYN_TIER and 'duhamel_inner_f1 or duhamel_inner_f2' in dy['routes']
            and 'read exactly from the BA2 gate' in dy['routes'], 'dynamics tier and routes')
    sc = rcp['secondary']
    require(sc['q'].startswith('151552|tau|') and 'conditional on the BB1 secondary pair' in sc['q'], 'secondary q')
    v['target_Cp2'] = rat(sc['C_prime_target'])
    items = p['items']
    require(sorted(items) == ['1_whole_sequence', '2_common_limit', '3_identification', '4_translations', '5_correlations'], 'five items')
    v['items'] = dict(items)
    i1 = items['1_whole_sequence']
    require('sup over M greater than N of ||rho^{F,M}_R-rho^{F,N}_R||_1 <= C\' q^(N-1)' in i1
            and "c'_site |Y| e^{|Y|/10^8} q^{d_Y}" in i1 and 'for F in {F1,F2}, N at least 2' in i1, 'item 1 form')
    i4 = items['4_translations']
    require('(4v_x,2v_y,v_z)' in i4 and '||rho^{Lambda_N+v}_R-rho^{Lambda_N}_R||_1 <= C_h q^(N-|v|_inf-1) for N at least |v|_inf+2' in i4
            and 'applied with Lambda_{N-|v|_inf}' in i4, 'item 4 form')
    i5 = items['5_correlations']
    m = match(r'for N at least (\d+), r_N=floor\(\(N-1\)/2\), \|theta\| at most (\d+)', i5, 'item 5 quantifiers')
    v['N5'], v['Theta'] = int(m.group(1)), Q(int(m.group(2)))
    v['i5_formula'] = "[C_dyn/(r_N-1) + c'_site |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N-r_N) + 2C' q^(N-1)]"
    require(v['i5_formula'] in i5 and '-|omega^{F,N}(A)|^2' in i5 and '-|omega_inf(A)|^2' in i5, 'item 5 formula and complex centering')
    v['cutoff'] = p['cutoff']
    require('constants uniform in L' in p['cutoff'] and 'AV1 cutoff-vector removal (F20-F23)' in p['cutoff']
            and 'the N and L limits are never exchanged' in p['cutoff'], 'cutoff parameter')
    require(p['N_min'] == '2 (item 5: N at least 5)' and p['clock'] == 'theta=alpha t/hbar for item 5'
            and p['window'] == '|theta| at most 8 (item 5)', 'N_min, clock, window')
    require('coarse l-infinity metric on factor sites (star diameter 1) for states' in p['metric']
            and 'F(r)=(1+r)^-4' in p['metric'], 'metric')
    v['assembly_text'] = p['assembly']
    require(p['assembly'].startswith('forward: nested telescoping with BB1 and BA1 and cutoff removal at fixed N'), 'assembly parameter')
    # preregistration
    v['clock'] = pre['clock']
    require(v['clock'].startswith('s=alpha*t_E/hbar (Euclidean), theta=alpha*t/hbar (real time); normalized u=theta/8'), 'clock')
    v['tau_value'] = rat(pre['tau']['value'])
    require(pre['tau']['signs_evaluated'] == ['+', '-'] and pre['tau']['is_model_change_vs_previous_loop'] is False
            and pre['tau']['rule_if_chosen_later'] is None, 'tau rule')
    v['triple'] = [rat(x) for x in pre['selected_triple_alpha_units']]
    require(v['triple'] == [0, 0, 0] and pre['model_id'] == 'AQ_patterned_zero_selected', 'model id and zero triple')
    v['model_id'] = pre['model_id']
    obs = pre['observable']
    require(obs['centering'] == 'complex-mean |omega(A)|^2 for correlations' and rat(obs['reference_value_exact']) == 0, 'observable block')
    v['tiers_allowed'] = list(pre['tier_names_allowed'])
    v['tier_rule'] = pre['tier_label_rule']
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    require(v['sub_labels'] == ['convergence_of_named_constructions', 'common_limit_of_named_constructions'], 'sub-labels')
    v['error_terms'] = list(pre['error_terms_itemized'])
    v['error_terms_rule'] = pre['error_terms_rule']
    v['template'] = pre['mandatory_sentence_template']
    v['gate_fields'] = dict(pre['gate_fields_required'])
    v['gate_fields_rule'] = pre['gate_fields_rule']
    v['forbidden'] = list(pre['forbidden_phrasings'])
    v['hash_binding'] = dict(pre['hash_binding'])
    require(all(v['hash_binding'][k] is True for k in ('contract_sha256_in_producer_inputs', 'check_py_reads_target_and_reference_from_contract',
                                                     'check_py_sha256_recorded_before_full_size_evaluation', 'admitted_gate_sha256_pinned_in_check_py')),
            'hash binding block')
    tv = pre['target']
    require(tv['comparator'] == '<=' and tv['value'] == '1/100000, 1/200000 and 1/2000000000', 'preregistered target block')
    tvals = [rat(x) for x in re.findall(r'\d+/\d+', tv['value'])]
    require(tvals == [v['target_Cp'], v['target_cp'], v['target_Cdyn']], 'target block equals the rate_constant_pair targets')
    sb = pre['scaling_brackets_per_constant']
    require(sb['C_prime'].startswith('exactly 1 at the hypothesis values') and sb['c_site_prime'].startswith('exactly 1 at the hypothesis values'),
            'state-constant scaling brackets')
    v['bracket_Cdyn'] = bracket(sb['C_dyn'], 'C_dyn bracket')
    v['bracket_secondary'] = bracket(sb['secondary_constants'], 'secondary bracket')
    require(sb['q_secondary'] == 'exactly 100' and sb['item_5_sum'].startswith('no single bracket'), 'q_secondary and item 5 bracket rule')
    v['brackets_text'] = dict(sb)
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']), 'controls list equals the preregistered ids')
    v['semantics'] = dict(c['new_control_semantics'])
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['acceptance'] = dict(c['acceptance'])
    v['shared'] = list(c['shared_premises'])
    v['reverse_isolation'] = c['reverse_premise_isolation']
    v['required'] = list(c['required'])
    # BB1 contract: the frozen targets that BB2 uses as hypotheses (read, never retyped)
    r1 = b1['parameters']['rate_constant_pair']
    v['bb1_q'] = rat(r1['headline']['q'])
    v['bb1_C'] = rat(r1['headline']['C_target'])
    v['bb1_c'] = rat(r1['region_form']['c_site_target'])
    v['bb1_q_region'] = rat(r1['region_form']['q'])
    require('c_site |Y| e^{|Y|/10^8} q^{d_Y}, d_Y = N - max_{y in Y} |y|_inf (so d_R = N-1)' in r1['region_form']['form'], 'BB1 region form')
    v['bb1_C2'] = rat(r1['secondary']['C_target'])
    v['bb1_c2'] = rat(r1['secondary']['c_site_target'])
    v['bb1_q2_per_tau'] = rat(match(r'^(\d+)\|tau\|', r1['secondary']['q'], 'BB1 secondary q').group(1))
    v['bb1_comparisons'] = list(b1['parameters']['comparisons'])
    require(len(v['bb1_comparisons']) == 5, 'five BB1 comparisons')
    v['bb1_cutoff'] = b1['parameters']['cutoff']
    v['bb1_template'] = b1['preregistration']['mandatory_sentence_template']
    return v


# ---------------------------------------------------------------------------
# Coarse geometry and the I1 anchored face table (parsed from the I1 snapshot).
# ---------------------------------------------------------------------------
E_UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIENT = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
COVER_R = (ORIGIN, EZ)
TOKEN = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}


def add(p, q):
    return tuple(a + b for a, b in zip(p, q))


def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def linf(p):
    return max(abs(a) for a in p)


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def coarse_box(N, shift=(0, 0, 0)):
    rng = range(-N, N + 1)
    return frozenset(add(y, shift) for y in product(rng, rng, rng))


def parse_i1_table(text):
    rows = re.findall(r'^\| (xy|xz|yz): r=([\d,]+); s=([\d,]+) \| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|$', text, re.M)
    require(len(rows) == 8, 'I1 table has eight rows')
    classes = {}
    for orient, rs, ss, count, supp, role in rows:
        rl = [int(x) for x in rs.split(',')]
        sl = [int(x) for x in ss.split(',')]
        require(len(rl) * len(sl) == int(count), 'I1 row count column')
        support = frozenset(TOKEN[t.strip()] for t in supp.split(','))
        for r in rl:
            for q in sl:
                classes[(orient, r, q)] = (support, role)
    require(len(classes) == 24 and sum(1 for x in classes.values() if x[1] == 'omitted') == 21, '24 classes, 21 omitted')
    return classes


def face_class(p, orient):
    return (orient, p[0] % 4, p[1] % 2)


def face_owner_set(p, orient):
    a, c = ORIENT[orient]
    return frozenset(owner(t) for t in (p, add(p, E_UNIT[a]), add(p, E_UNIT[c])))


def fine_to_coarse_shift(w):
    """A fine translation is coarse iff it preserves the residues x mod 4 and y mod 2."""
    if w[0] % 4 == 0 and w[1] % 2 == 0:
        return (w[0] // 4, w[1] // 2, w[2])
    return None


def coarse_to_fine(v):
    return (4 * v[0], 2 * v[1], v[2])


# ---------------------------------------------------------------------------
# Exact Gaussian-rational scalars and matrices for the finite algebraic fixtures.
# ---------------------------------------------------------------------------
def cz(a, b=0):
    return (Q(a), Q(b))


def cadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def csub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def cmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def cconj(x):
    return (x[0], -x[1])


def cabs2(x):
    return x[0] * x[0] + x[1] * x[1]


def mat(rows):
    return [[cz(*e) if isinstance(e, tuple) else cz(e) for e in row] for row in rows]


def _csum(it):
    out = cz(0)
    for x in it:
        out = cadd(out, x)
    return out


def mmul(A, B):
    n, m, k = len(A), len(B[0]), len(B)
    return [[_csum(cmul(A[i][t], B[t][j]) for t in range(k)) for j in range(m)] for i in range(n)]


def madj(A):
    return [[cconj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]


def madd(A, B, c=1):
    return [[cadd(A[i][j], cmul(cz(c), B[i][j])) for j in range(len(A[0]))] for i in range(len(A))]


def mtrace(A):
    return _csum(A[i][i] for i in range(len(A)))


def is_zero(A):
    return all(e == cz(0) for row in A for e in row)


def eye(n):
    return [[cz(1 if i == j else 0) for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------------------
# Text scanners (report and exported statements).
# ---------------------------------------------------------------------------
ROUND_FORBIDDEN = [   # copied from research/round33/tools/phrase_scan.py (infrastructure list, no premise weight)
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


def phrase_hits(text, forbidden, template):
    body = normalize(text).replace(normalize(template), ' ')
    hits = []
    for clause in clauses(body):
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                hits.append({'phrase': phrase, 'clause': clause[:200], 'negated': bool(NEGATION.search(clause))})
    return hits


def affirmative_phrase_hits(text, forbidden, template):
    return [h for h in phrase_hits(text, forbidden, template) if not h['negated']]


UNIFORM = re.compile(r'\buniform(?:ly|ity)?\b|\buniform-in-', re.I)
UNIFORM_QUALIFIERS = ('cutoff', 'for |theta|', 'for t in compact sets', 'on compact', 'at fixed spacing', 'uniform integrability',
                      'in n and in the', 'in l ')


def uniformity_violations(text, template):
    body = normalize(text).replace(normalize(template), ' ')
    bad = []
    for clause in clauses(body):
        if not UNIFORM.search(clause):
            continue
        low = clause.lower().replace('`', '')
        negated = bool(NEGATION.search(clause))
        qualified = any(q in low for q in UNIFORM_QUALIFIERS)
        spacing = re.search(r'lattice spacing|spacing a\b|\bin a\b', low)
        if spacing and not negated:
            bad.append(clause[:200])
        elif not (negated or qualified):
            bad.append(clause[:200])
    return bad


def placeholder_spans(text):
    return [m.group(0) for m in re.finditer(r'<[^<>]*>', text) if re.search(r'\s|\||e\.g\.', m.group(0))]


# ===========================================================================
def compute(check_sha):
    c, contract_digest, b1, bb1_digest = load_contracts()
    V = contract_values(c, b1)
    tau_cap = V['tau_value']
    require(tau_cap == Q(1, 100000000), 'preregistered tau is the cap 10^-8')
    taus = {'+': tau_cap, '-': -tau_cap}
    q = V['q']
    check('contract_snapshots_sha256',
          contract_digest == CONTRACT_SHA256 and bb1_digest == BB1_SHA256 and q == Q(1, 64)
          and V['target_Cp'] == Q(1, 100000) and V['target_cp'] == Q(1, 200000) and V['target_Cdyn'] == Q(1, 2000000000)
          and V['N5'] == 5 and V['Theta'] == 8 and len(V['controls']) == 34 and V['bracket_Cdyn'] == (9500, 10500)
          and V['bracket_secondary'] == (Q(99, 100), Q(101, 100)),
          contract_sha256=contract_digest, bb1_contract_sha256=bb1_digest, contract_path=CONTRACT_REL, bb1_contract_path=BB1_REL,
          targets_read_from_contract={'C_prime': s(V['target_Cp']), 'c_site_prime': s(V['target_cp']), 'C_dyn': s(V['target_Cdyn']),
                                      'secondary_C_prime': s(V['target_Cp2'])},
          hypotheses_read_from_contract={'q': s(q), 'C_h': s(V['C_h']), 'c_h': s(V['c_h']), 'q_2_per_abs_tau': s(V['q2_per_tau']),
                                         'C_2h': s(V['C_2h']), 'c_2h': s(V['c_2h'])},
          scaling_brackets_read_from_contract={'C_prime': 'exactly 1', 'c_site_prime': 'exactly 1',
                                               'C_dyn': [s(x) for x in V['bracket_Cdyn']],
                                               'secondary_constants': [s(x) for x in V['bracket_secondary']], 'q_secondary': 'exactly 100'},
          tau_read_from_contract=s(tau_cap), item5_quantifiers={'N_at_least': V['N5'], 'theta_window': s(V['Theta']),
                                                                 'r_N': 'floor((N-1)/2)'},
          controls_read_from_contract=len(V['controls']), hash_binding=V['hash_binding'],
          note='both contract sha256 values are compared before any contract field is parsed')

    # ======================= pinned gates and the committed source excerpt =======================
    gate_sha = {}
    for rel, pin in PINNED_GATES.items():
        gate_sha[rel] = sha(BASE / 'inputs' / rel)
        require(gate_sha[rel] == pin, 'admitted gate snapshot differs from its pinned sha256: ' + rel)
        require(load_json_input(rel).get('verdict') == 'accepted_within_scope', 'gate verdict ' + rel)
    ns_raw = (BASE / 'inputs' / NS_REL).read_bytes()
    ns_digest = sha_bytes(ns_raw)
    require(ns_digest == NS_SHA256, 'Nachtergaele-Sims excerpt differs from its pinned sha256')
    ns = ns_raw.decode('utf-8')
    require(('PDF sha256: `' + NS_PDF_SHA256 + '`') in ns, 'NS PDF binding in the excerpt')
    ba2g = load_json_input(P_BA2_GATE)
    require(NS_PDF_SHA256 in ba2g['accepted'], 'NS PDF binding in the BA2 gate')
    check('pinned_gates_and_source_excerpt',
          all(gate_sha[r] == p for r, p in PINNED_GATES.items()) and ns_digest == NS_SHA256,
          gate_sha256=gate_sha, ns_excerpt_sha256=ns_digest, ns_pdf_sha256=NS_PDF_SHA256,
          note='pins are compared before any value is read from these files; no BB1 producer, skeptic or gate file is read')

    # ======================= BA2 dynamics constants (read from the gate as exact rationals) =======================
    acc2 = ba2g['accepted']
    K_cmp = rat(match(r'K_cmp = (\d+/\d+) \(about', acc2, 'BA2 K_cmp').group(1))
    K_F1 = rat(match(r'F1 with K_F1 = (\d+/\d+)', acc2, 'BA2 K_F1').group(1))
    K_F2 = rat(match(r'F2 with K_F2 = (\d+/\d+)', acc2, 'BA2 K_F2').group(1))
    K_cmp_rev = rat(match(r"second-route constant K'_cmp = (\d+/\d+)", acc2, 'BA2 K\'_cmp').group(1))
    K_F2_rev = rat(match(r'the second route (\d+/\d+) \(about 3\.46428e-11, reverse, owner-set', acc2, 'BA2 reverse K_F2').group(1))
    for frag in ('b(N) = K_cmp (5N+1) N^-3', 'route duhamel_inner_f1', 'route duhamel_inner_f2', 'tier polynomial_lieb_robinson',
                 'sup over M greater than N of ||T^{F,M}_theta(A)-T^{F,N}_theta(A)|| <= K_F/(N-1) ||A|| for |theta|<=8 and N at least 2',
                 '||T^{F2,N}_theta(A)-T_theta(A)|| <= min(K_F1, second-route K_F2)/(N-1) ||A||', 'C<=224, ||Phi||_F<=2268|tau|',
                 'every A in B(H_R) with ||A||<=1 on the fixed cover R', '1953058850/194651',
                 'faces charged once, inner F1', 'the F2 limit dynamics equals the AQ1 limit dynamics T_theta'):
        require(frag in acc2, 'BA2 gate fragment missing: ' + frag)
    require('equality of GNS dynamics or of correlation functions of different states' in acc2
            and ba2g['gate_fields']['whole_sequence_claimed'] is True and ba2g['gate_fields']['common_limit_claimed'] is False
            and ba2g['gate_fields']['dynamics_level'] == 'algebraic_heisenberg_compact_window', 'BA2 gate scope')
    ba2f = read_input(P_BA2F)
    m = match(r'K_cmp = (\d+) tau\^2/\(1-(\d+)\|tau\|\) = (\d+/\d+)', ba2f, 'BA2 K_cmp closed form')
    a_cmp, den_cmp, K_cmp_rep = Q(int(m.group(1))), Q(int(m.group(2))), rat(m.group(3))
    m = match(r'K_c1 = (\d+) tau\^2/\(1-(\d+)\|tau\|\) = (\d+/\d+)', ba2f, 'BA2 K_c1 closed form')
    a_c1, den_c1, K_c1_rep = Q(int(m.group(1))), Q(int(m.group(2))), rat(m.group(3))
    require(den_cmp == den_c1, 'common velocity denominator')
    lemma_118 = '`(5N+1)(N-1)N^-3` is at most `11/8` for `N` at least 2' in ba2f

    def closed(a, t):
        t = abs(rat(t))
        return a * t * t / (1 - den_c1 * t)
    # independent reconstruction of the same closed forms from the admitted AQ1 constants C<=224, ||Phi||_F<=2268|tau|
    phi_per_tau, C_conv = Q(2268), Q(224)

    def lr_coeff(t, S):
        t = abs(t)
        phiF = phi_per_tau * t
        vel = 2 * phiF * C_conv
        return t / 3 * (2 * phiF / (1 - vel / 3)) * S
    recon_ok = all(lr_coeff(t, 392) == closed(a_c1, t) and lr_coeff(t, 168) == closed(a_cmp, t) for t in (tau_cap, tau_cap / 100, tau_cap / 7))
    check('ba2_dynamics_constants_read_from_gate',
          K_cmp == K_cmp_rep == closed(a_cmp, tau_cap) and K_F1 == K_c1_rep == closed(a_c1, tau_cap)
          and K_F2 == K_F1 + Q(11, 8) * K_cmp and recon_ok and lemma_118
          and all(k <= Q(25, 10 ** 11) for k in (K_F1, K_F2, K_F2_rev)) and K_cmp <= Q(6, 10 ** 11),
          K_cmp=s(K_cmp), K_cmp_preview=dec(K_cmp), K_F1=s(K_F1), K_F1_preview=dec(K_F1), K_F2=s(K_F2), K_F2_preview=dec(K_F2),
          K_cmp_second_route=s(K_cmp_rev), K_F2_second_route=s(K_F2_rev),
          closed_forms={'K_cmp': s(a_cmp) + ' tau^2/(1-' + s(den_cmp) + '|tau|)', 'K_F1': s(a_c1) + ' tau^2/(1-' + s(den_c1) + '|tau|)'},
          routes={'K_cmp': 'duhamel_inner_f1', 'K_F1': 'duhamel_inner_f1', 'K_F2': 'duhamel_inner_f1 (F1-inner Duhamel plus the comparison)',
                  'second routes': 'duhamel_inner_f2 (labelled, not used by this producer)'},
          note='gate values are read as exact rationals and compared with the BA2 forward closed forms and with a reconstruction from '
               'C<=224, ||Phi||_F<=2268|tau|; no recomputed or smaller value replaces a gate value')

    # ======================= other premise statements parsed =======================
    ba1g = load_json_input(P_BA1_GATE)
    ba1_general = 'any two complete-factor volumes of one prescription containing Lambda_N' in ba1g['accepted']
    ba1r = read_input(P_BA1R)
    ba1_prescr = ('F1 whole stars `b+S` inside `Lambda`, or F2 clipped groups `X_b` inside `(b+S) cap Lambda`' in ba1r)
    aq1g = load_json_input(P_AQ1_GATE)
    aq1_state = ('have a subsequence defining a compatible locally normal gauge-invariant stationary state on the norm closure of full bounded local algebras'
                 in aq1g['accepted'] and 'strongly continuous GNS evolution with a nonnegative self-adjoint physical energy generator' in aq1g['accepted']
                 and 'The forward physical cyclic restriction is reducing' in aq1g['accepted'] and 'whole-sequence convergence' in aq1g['limitations'][0])
    aq1 = read_input(P_AQ1)
    aq1_extract = 'Diagonal extraction over the countable nested coarse cubes produces a subsequence N_k whose densities converge in trace norm on every finite F.' in aq1
    aq2g = load_json_input(P_AQ2_GATE)
    aq2_stmt = ('For the actual AQ1 centered full-Z3 subsequential state' in aq2g['accepted']
                and 'the complete original-endpoint gauge-fixed space equals the invariant-local cyclic completion and reduces the physical energy generator'
                in aq2g['accepted'] and 'H_phys >= (alpha/16)(I-P_Omega) and a simple vacuum in this representation' in aq2g['accepted'])
    aq2_qual = "The full-GNS strengthening explicitly uses AM2's separately reviewed full-Hilbert finite gap." in aq2g['accepted']
    aq2_limit = 'Vacuum simplicity there does not establish uniqueness of all thermodynamic ground states' in aq2g['limitations'][0]
    aq2 = read_input(P_AQ2)
    aq2_complex = 'Complex means require the absolute square.' in aq2
    av1g = load_json_input(P_AV1_GATE)
    av1_cut = 'The on-site cutoff is removed for the ground vector itself in each fixed box' in av1g['accepted']
    av1 = read_input(P_AV1F)
    av1_eckart = ('\\tag{HNM-AV1-F22}' in av1 and '1-|\\langle\\psi,\\psi_L\\rangle|^2\\le\\frac{E_{0,L}-E_0}{E_1-E_0}\\le2(E_{0,L}-E_0)' in av1
                  and 'A coarse translation by `(N,N,N)` is the fine translation `(4N,2N,N)`. It preserves the residues `x mod 4` and `y mod 2`' in av1)
    ay1g = load_json_input(P_AY1_GATE)
    ay1_f2 = ('cutoff-vector removal' in ay1g['accepted'] and 'local trace-norm compactness and a diagonal extraction of its own' in ay1g['accepted'])
    ay1f = read_input(P_AY1F)
    ay1_pad = 'so the padded ground is `psi^(2)_N ⊗ Omega_pad`' in ay1f
    am2g = load_json_input(P_AM2_GATE)
    am2_simple = 'For every nonempty finite I1 complete-factor volume' in am2g['accepted'] and 'removal of onsite representation cutoffs' in am2g['accepted']
    ay2g = load_json_input(P_AY2_GATE)
    ay2_rows = ('whole-sequence convergence, not proved (a Cauchy estimate in N' in ay2g['accepted']
                and 'translation invariance under coarse translations, not proved' in ay2g['accepted'])
    sel = read_input(P_SEL)
    sel_ok = 'forward by nested telescoping, reverse through unions' in sel and 'never uniqueness of every ground state' in sel
    i1 = read_input(P_I1)
    classes = parse_i1_table(i1)
    i1_owner = '\\pi(x,y,z)=(\\lfloor x/4\\rfloor,\\lfloor y/2\\rfloor,z)' in i1
    check('premise_statements_parsed',
          ba1_general and ba1_prescr and aq1_state and aq1_extract and aq2_stmt and aq2_qual and aq2_limit and aq2_complex and av1_cut
          and av1_eckart and ay1_f2 and ay1_pad and am2_simple and ay2_rows and sel_ok and i1_owner,
          parsed={'BA1 gate': 'accepted comparison includes any two complete-factor volumes of one prescription containing Lambda_N',
                  'BA1 reverse Thm 4.1': 'prescriptions on general complete-factor volumes: F1 whole stars inside the volume, F2 clipped groups',
                  'AQ1': 'subsequence with trace-norm convergence on every finite F; locally normal stationary state; strongly continuous GNS evolution; '
                         'nonnegative generator; reducing physical cyclic restriction; whole-sequence convergence not admitted there',
                  'AQ2 gate': "for the actual AQ1 centered subsequential state: H_phys >= (alpha/16)(I-P_Omega), simple vacuum in this representation; "
                              "full-GNS strengthening explicitly uses AM2's separately reviewed full-Hilbert finite gap",
                  'AV1': 'ground-vector cutoff removal in each fixed box (F20-F23, Eckart F22); coarse translations are (4N,2N,N)',
                  'AY1': 'F2: cutoff-vector removal, local trace-norm compactness and a diagonal extraction of its own; padded ground is a product',
                  'AM2 gate': 'every nonempty finite I1 complete-factor volume (hence translated boxes): simple ground, onsite cutoff removal',
                  'AY2 gate': 'whole-sequence convergence and coarse translation invariance were open obligations',
                  'I1': 'ownership pi(x,y,z)=(floor(x/4),floor(y/2),z) and the 24-class face table'})

    # ======================= BB1 hypotheses: the frozen targets, both contracts =======================
    hyp_equal = (V['C_h'] == V['bb1_C'] and V['c_h'] == V['bb1_c'] and q == V['bb1_q'] == V['bb1_q_region'] == V['q_head']
                 and V['C_2h'] == V['bb1_C2'] and V['c_2h'] == V['bb1_c2'] and V['q2_per_tau'] == V['bb1_q2_per_tau'])
    CMP = V['bb1_comparisons']
    require(CMP[0] == 'F1 on Lambda_N versus F1 on Lambda_{N+1}' and CMP[1] == 'F2 on Lambda_N versus F2 on Lambda_{N+1}'
            and CMP[2].startswith('F1 versus F2 on the same Lambda_N') and CMP[3].startswith('any two centered boxes Lambda_M, Lambda_M')
            and CMP[4].startswith('two finite complete-factor volumes of one prescription both containing Lambda_N'), 'BB1 comparison list')
    CUT_Q = 'each on-site cutoff space Q_L, every L, constants uniform in L'
    CUT_U = 'fixed N, untruncated ground vectors (reached from the Q_L form by AV1 F20-F23 / AY1; the untruncated form is the same hypothesis at L=infinity)'
    HYP = [
        {'id': 'H1', 'comparison': CMP[0], 'forms': ['R', 'region'], 'cutoff_regimes': [CUT_Q, CUT_U], 'signs': ['+', '-'],
         'constants': {'q': s(q), 'C_h': s(V['C_h']), 'c_h': s(V['c_h'])}, 'items': ['1', '2', '3', '4', '5'],
         'use': 'every nested step k to k+1 with k at least N of the F1 telescoping sum (item 1); hence items 2, 3, 5 and the limit in item 4'},
        {'id': 'H2', 'comparison': CMP[1], 'forms': ['R', 'region'], 'cutoff_regimes': [CUT_Q, CUT_U], 'signs': ['+', '-'],
         'constants': {'q': s(q), 'C_h': s(V['C_h']), 'c_h': s(V['c_h'])}, 'items': ['1', '2', '3', '5'],
         'use': 'every nested step of the F2 telescoping sum (item 1); hence the F2 parts of items 2, 3, 5'},
        {'id': 'H3', 'comparison': CMP[2], 'forms': ['R', 'region'], 'cutoff_regimes': [CUT_Q, CUT_U], 'signs': ['+', '-'],
         'constants': {'q': s(q), 'C_h': s(V['C_h']), 'c_h': s(V['c_h'])}, 'items': ['2', '3', '5'],
         'use': 'fixed-N F1 versus F2 difference tends to 0 (item 2); identifies F2 subsequential limits (item 3) and the F2 limit used in item 5'},
        {'id': 'H4', 'comparison': CMP[4], 'forms': ['R', 'region'], 'cutoff_regimes': [CUT_Q, CUT_U], 'signs': ['+', '-'],
         'constants': {'q': s(q), 'C_h': s(V['C_h']), 'c_h': s(V['c_h'])}, 'items': ['4'],
         'use': 'Lambda_N+v versus Lambda_N, both containing Lambda_{N-|v|_inf}: the R form gives the quantitative bound and invariance on '
                'translates of R; the region form gives invariance on every finite region',
         'coefficient_input': 'BA1 accepted comparison of any two complete-factor volumes of one prescription containing Lambda_N'},
        {'id': 'H1s-H3s', 'comparison': 'as H1-H3, secondary pair', 'forms': ['R', 'region'], 'cutoff_regimes': [CUT_Q, CUT_U],
         'signs': ['+', '-'], 'constants': {'q_2': s(V['q2_per_tau']) + '|tau|', 'C_2h': s(V['C_2h']), 'c_2h': s(V['c_2h'])},
         'items': ['labelled secondary constants only'], 'use': 'labelled secondary C_prime and c_site_prime; decides nothing'},
    ]
    NOT_USED = [{'comparison': CMP[3], 'reason': 'not used by the forward assembly (nested telescoping); used directly it would give the '
                                                  'labelled value C_prime = C_h (factor 1 instead of 1/(1-q))'}]
    check('bb1_hypotheses_read_from_contracts',
          hyp_equal and len(HYP) == 5 and all(h['signs'] == ['+', '-'] for h in HYP),
          hypotheses={'q': s(q), 'C_h': s(V['C_h']), 'c_h': s(V['c_h']), 'secondary': {'q_2': s(V['q2_per_tau']) + '|tau|', 'C_2h': s(V['C_2h']),
                                                                                         'c_2h': s(V['c_2h'])}},
          source='BB2 rate_constant_pair.hypotheses and BB1 frozen targets (headline C_target, region_form c_site_target, secondary); equal',
          status=COND, note='frozen targets used as explicit hypotheses; no BB1 producer, skeptic or gate value is read')

    # ======================= NS quotations verbatim =======================
    report_path = BASE / REPORT
    require(report_path.is_file(), 'report.md missing')
    report_text = report_path.read_text(encoding='utf-8')

    def validate_quotes(report, quotes):
        for key, qt in quotes.items():
            require(qt in ns, 'quotation is not a verbatim substring of the committed excerpt: ' + key)
            require(qt in report, 'quotation missing verbatim from report.md: ' + key)
        return True
    ns_forbidden_in_quotes = [k for k, qt in NS_QUOTES.items() if 'thermodynamic' in qt]
    check('ns_quotes_verbatim',
          validate_quotes(report_text, NS_QUOTES) and not ns_forbidden_in_quotes
          and rejected(lambda: validate_quotes(report_text, dict(NS_QUOTES, eq77=NS_QUOTES['eq77'].replace('lim', 'limit'))), 'paraphrased_eq77')
          and rejected(lambda: validate_quotes(report_text + '\nthe finite evolutions converge in norm on compact time sets',
                                               dict(NS_QUOTES, thm41_tail='the finite evolutions converge in norm on compact time sets')),
                       'paraphrase_not_in_excerpt'),
          quotes=sorted(NS_QUOTES), source=NS_REL, source_sha256=NS_SHA256,
          use={'eq77/thm41_tail': 'T_theta exists as a norm limit on local observables and extends to a group of *-automorphisms of the '
                                  'quasi-local algebra (item 5 needs omega_inf(A* T_theta(A)))',
               'quasi_local_partB': 'the quasi-local algebra is the norm completion of the local algebra; omega_inf extends to it',
               'eq51': 'the polynomial Lieb-Robinson bound behind the BA2 constants (named, not re-derived)',
               'eq53_condition': 'an exponential form requires Phi in B(Gamma, F_a); the admitted constants use the polynomial F only'})

    # ======================= item 1: whole-sequence Cauchy estimate by nested telescoping =======================
    C_h, c_h = V['C_h'], V['c_h']

    def Cprime(Ch, ch):
        return Ch / (1 - q)

    def cprime(Ch, ch):
        return ch / (1 - q)
    Cp, cp = Cprime(C_h, c_h), cprime(C_h, c_h)
    Cp_met, cp_met = Cp <= V['target_Cp'], cp <= V['target_cp']

    def telescoped(N, M, const):
        return sum(const * q ** (k - 1) for k in range(N, M))
    tele_ok = True
    for N in range(2, 26):
        for M in range(N + 1, N + 30):
            T = telescoped(N, M, C_h)
            tele_ok = tele_ok and T == C_h * q ** (N - 1) * (1 - q ** (M - N)) / (1 - q) and T < Cp * q ** (N - 1) \
                and Cp * q ** (N - 1) - T == Cp * q ** (M - 1)
    sup_is_limit = all(Cp * q ** (N - 1) - telescoped(N, N + 40, C_h) == Cp * q ** (N + 39) for N in (2, 5, 9))

    def validate_cauchy(kind, const_R, steps_summed):
        require(kind == 'sup_over_all_M', 'a Cauchy estimate bounds every M greater than N at once; an N to N+1 bound alone is not one')
        require(steps_summed == 'all_steps_k_from_N_with_geometric_tail', 'the telescoping sum charges every step k from N, with its full tail')
        require(const_R >= C_h / (1 - q), 'the telescoped constant is at least C_h/(1-q) (the full geometric tail)')
        return True
    check('item1_whole_sequence_cauchy_R',
          tele_ok and sup_is_limit and Cp_met and validate_cauchy('sup_over_all_M', Cp, 'all_steps_k_from_N_with_geometric_tail')
          and rejected(lambda: validate_cauchy('N_to_N_plus_1', Cp, 'all_steps_k_from_N_with_geometric_tail'), 'N_to_N_plus_1_bound_as_cauchy')
          and rejected(lambda: validate_cauchy('sup_over_all_M', C_h, 'first_step_only'), 'geometric_tail_dropped'),
          statement='for F in {F1,F2}, N at least 2, every M greater than N, each sign, in each Q_L and then for the untruncated vectors: '
                    '||rho^{F,M}_R-rho^{F,N}_R||_1 <= sum_{k=N}^{M-1} C_h q^(k-1) = C_h q^(N-1)(1-q^(M-N))/(1-q) < C_prime q^(N-1)',
          C_prime_function='C_prime(C_h,c_h) = C_h/(1-q) = (64/63) C_h', C_prime=s(Cp), C_prime_preview=dec(Cp),
          target=s(V['target_Cp']), target_met=Cp_met, margin_preview=dec(V['target_Cp'] / Cp, 6),
          tier=STATE_TIER, assembly=ASSEMBLY, hypothesis_source=HYP_SOURCE, hypotheses=['H1', 'H2'], status=COND,
          audit='exact telescoped sums for N=2..25, M=N+1..N+29; the supremum over M equals C_prime q^(N-1) and is not attained')

    # regions Y: |Y| factor, exponent d_Y
    def dY(Y, N):
        return N - max(linf(y) for y in Y)
    L_shape = frozenset([(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1), (-1, 0, 2)])
    regions = {'R': frozenset(COVER_R), 'Lambda_1': coarse_box(1), 'Lambda_2': coarse_box(2), 'L_shape': L_shape,
               'far_pair': frozenset([(3, 0, 0), (3, 0, 1)])}
    region_ok = True
    region_tab = {}
    for name, Y in regions.items():
        mY = max(linf(y) for y in Y)
        EY = exp_upper(Q(len(Y), 10 ** 8))
        for N in range(max(2, mY), max(2, mY) + 12):
            for M in range(N + 1, N + 15):
                T = sum(c_h * len(Y) * EY * q ** (k - mY) for k in range(N, M))
                region_ok = region_ok and T < cp * len(Y) * EY * q ** dY(Y, N)
        region_tab[name] = {'|Y|': len(Y), 'max_linf': mY, 'd_Y_at_N': 'N-' + str(mY)}
    R_value_on_L2 = Cp * q ** (5 - 1)
    Y_value_on_L2 = cp * 125 * q ** (5 - 2)

    def validate_region_form(form):
        require(form['size_factor'] == '|Y| e^{|Y|/10^8}' and form['exponent'] == 'd_Y = N - max_{y in Y}|y|_inf', 'region bound states |Y| and d_Y')
        require(form['constant'] == 'c_site_prime', 'the region constant is c_site_prime, not the R constant')
        return True
    RF = {'size_factor': '|Y| e^{|Y|/10^8}', 'exponent': 'd_Y = N - max_{y in Y}|y|_inf', 'constant': 'c_site_prime'}
    check('item1_whole_sequence_cauchy_regions',
          region_ok and cp_met and R_value_on_L2 < Y_value_on_L2 and validate_region_form(RF)
          and rejected(lambda: validate_region_form(dict(RF, constant='C_prime', size_factor='1', exponent='N-1')), 'R_constant_reused_on_Y'),
          statement="for every finite complete-factor region Y inside Lambda_N: sup over M greater than N of ||rho^{F,M}_Y-rho^{F,N}_Y||_1 <= "
                    "sum_{k=N}^{M-1} c_h |Y| e^{|Y|/10^8} q^(k-max|y|_inf) < c_site_prime |Y| e^{|Y|/10^8} q^{d_Y}",
          c_site_prime_function='c_site_prime(C_h,c_h) = c_h/(1-q) = (64/63) c_h', c_site_prime=s(cp), c_site_prime_preview=dec(cp),
          target=s(V['target_cp']), target_met=cp_met, margin_preview=dec(V['target_cp'] / cp, 6), regions=region_tab,
          R_form_on_Lambda_2_at_N5_preview=dec(R_value_on_L2), region_form_on_Lambda_2_at_N5_preview=dec(Y_value_on_L2),
          tier=STATE_TIER, assembly=ASSEMBLY, hypothesis_source=HYP_SOURCE, hypotheses=['H1', 'H2'], status=COND,
          exp_enclosure='e^x <= 1/(1-x) for 0 <= x < 1 (directed), x=|Y|/10^8')

    # existence without compactness; consistency; the state omega_inf
    def validate_existence(basis):
        require(basis == 'explicit_cauchy_bound_and_trace_class_completeness', 'existence must come from the Cauchy bound and completeness of the trace class')
        return True
    part_trace_contraction = True   # checked on a fixture below (exact 4x4 partial trace of a rank-two density)
    rho4 = [[Q(0)] * 4 for _ in range(4)]
    vecs = [(Q(1, 2), Q(1, 2), Q(1, 2), Q(1, 2)), (Q(3, 5), Q(0), Q(4, 5), Q(0))]
    for w, vv in zip((Q(1, 3), Q(2, 3)), vecs):
        for i in range(4):
            for j in range(4):
                rho4[i][j] += w * vv[i] * vv[j]
    ptr = [[rho4[0][0] + rho4[1][1], rho4[0][2] + rho4[1][3]], [rho4[2][0] + rho4[3][1], rho4[2][2] + rho4[3][3]]]
    part_trace_contraction = (ptr[0][0] + ptr[1][1] == 1 and ptr[0][1] == ptr[1][0])
    check('item1_limit_exists_without_compactness',
          validate_existence('explicit_cauchy_bound_and_trace_class_completeness') and part_trace_contraction
          and rejected(lambda: validate_existence('aq1_compactness_plus_ay1_closeness'), 'compactness_plus_closeness_basis'),
          statement='the reduced densities rho^{F,N}_Y form a Cauchy sequence in the Banach space T_1(H_Y) (item 1); the limit rho^{F,inf}_Y exists '
                    'without any compactness, is positive with trace one (closed conditions), and the limits are consistent under partial trace '
                    '(a trace-norm contraction); omega^F_inf(B)=Tr(rho^{F,inf}_Y B) is a state on the local algebra and extends by norm continuity '
                    'to the quasi-local algebra', fixture='exact partial trace of a rank-two 4x4 density keeps trace one', status=COND)

    # cutoff order
    dbl = {(N, L): (1 if L >= N else 0) for N in range(1, 30) for L in range(1, 30)}
    lim_L_then_N = all(dbl[(N, 29)] == 1 for N in range(1, 29))       # for fixed N, L large: 1
    lim_N_then_L = all(dbl[(29, L)] == 0 for L in range(1, 29))       # for fixed L, N large: 0

    def validate_cutoff_order(order, uniform):
        require(uniform is True, 'the bounds must hold in every Q_L with the same constant (uniform in the on-site cutoff L)')
        require(order == ['bound in each Q_L', 'L to infinity at fixed N and M', 'sup over M', 'N to infinity'], 'L is removed at fixed N before any N limit')
        return True
    ORDER = ['bound in each Q_L', 'L to infinity at fixed N and M', 'sup over M', 'N to infinity']
    H = [Q(0), Q(1, 2), Q(1)]                 # gap 1/2
    ecks = []
    for vv in ((Q(3, 5), Q(4, 5), Q(0)), (Q(2, 3), Q(2, 3), Q(1, 3)), (Q(1), Q(0), Q(0))):
        E = sum(H[i] * vv[i] ** 2 for i in range(3))
        ecks.append((1 - vv[0] ** 2, 2 * (E - H[0])))
    eckart_ok = all(a <= b for a, b in ecks)
    Hdeg = [Q(0), Q(0), Q(1)]   # H'=diag(0,0,1): e_1 has the ground energy and overlap 0 with e_0 (no gap, no vector convergence)
    degenerate = Hdeg[1] == Hdeg[0] and 1 - Q(0) ** 2 == 1 and 2 * (Hdeg[1] - Hdeg[0]) == 0
    check('cutoff_uniform_then_removed',
          lim_L_then_N and lim_N_then_L and eckart_ok and degenerate and validate_cutoff_order(ORDER, True)
          and rejected(lambda: validate_cutoff_order(['bound in each Q_L', 'N to infinity', 'L to infinity'], True), 'N_limit_taken_in_Q_L_first')
          and rejected(lambda: validate_cutoff_order(ORDER, False), 'constant_depends_on_L'),
          order=ORDER, fixture_double_sequence='a_{N,L}=1 if L>=N else 0: lim_N lim_L = 1, lim_L lim_N = 0 (limits do not commute)',
          eckart_pairs=[[s(a), s(b)] for a, b in ecks],
          passage='||rho^{B,L}_Y-rho^B_Y||_1 <= 2 sqrt(1-|<psi,psi_L>|^2) <= 2 sqrt(2(E_{0,L}-E_0)) -> 0 at fixed box B (AV1 F21-F22; F2 by AY1; '
                  'translated boxes by covariance); a bound holding for every L with the same constant passes to the untruncated vectors')

    # ======================= item 2: the common limit =======================
    def f1f2_limit_bound_R(N):
        return (2 * Cp + C_h) * q ** (N - 1)

    def f1f2_limit_bound_Y(Y, N):
        return (2 * cp + c_h) * len(Y) * exp_upper(Q(len(Y), 10 ** 8)) * q ** dY(Y, N)
    to_zero = all(any(f1f2_limit_bound_R(N) < Q(1, 10 ** k) for N in range(2, 200)) for k in range(1, 60)) \
        and all(any(f1f2_limit_bound_Y(Y, N) < Q(1, 10 ** k) for N in range(max(2, max(linf(y) for y in Y)), 200))
                for Y in regions.values() for k in (5, 20, 40))

    def validate_common(basis):
        require(basis == 'fixed_N_F1_vs_F2_hypothesis_tends_to_0_plus_item1', 'the common limit needs the fixed-N F1 versus F2 comparison')
        return True
    check('item2_common_limit',
          to_zero and validate_common('fixed_N_F1_vs_F2_hypothesis_tends_to_0_plus_item1')
          and rejected(lambda: validate_common('same_faces_meet_R'), 'common_limit_from_shared_faces_near_R')
          and rejected(lambda: validate_common('ay1_2D_closeness'), 'common_limit_from_2D_closeness'),
          statement='for every finite region Y and N at least max(2, max|y|_inf): ||rho^{F1,inf}_Y-rho^{F2,inf}_Y||_1 <= (2 c_site_prime + c_h)|Y| '
                    'e^{|Y|/10^8} q^{d_Y} for every N, hence 0; on R the same with (2 C_prime + C_h) q^(N-1); the common limit rho^inf_Y is the '
                    'limit of the named constructions and ||rho^{F,N}_Y-rho^inf_Y||_1 <= c_site_prime |Y| e^{|Y|/10^8} q^{d_Y} for both F',
          R_factor=s(2 * Cp + C_h), R_factor_preview=dec(2 * Cp + C_h), hypotheses=['H1', 'H2', 'H3'], status=COND)

    # ======================= item 3: identification and inheritance =======================
    INHERIT = {
        'AQ1': ['locally normal gauge-invariant state on the norm closure of the full bounded local algebras', 'stationarity under T_theta',
                'strongly continuous GNS evolution', 'nonnegative self-adjoint physical energy generator', 'reducing physical cyclic restriction'],
        'BA2 (F2 rerun of AQ1 sections 4-5)': ['stationarity under T_theta', 'strongly continuous GNS evolution', 'nonnegative generator',
                                               'physical cyclic space reduces it'],
        'AQ2': ['complete original-endpoint gauge-fixed space equals the invariant-local cyclic completion and reduces the generator',
                'H_phys >= (alpha/16)(I-P_Omega) on that completion', 'simple vacuum in that representation',
                "full-GNS strengthening only as qualified in the AQ2 gate (explicitly uses AM2's separately reviewed full-Hilbert finite gap)"],
    }

    def validate_identification(rec):
        require(rec['order'] == ['identify every subsequential limit with omega_inf on every finite region', 'extend to the quasi-local algebra',
                                 'inherit'], 'identification must precede inheritance')
        require(rec['basis'] == 'whole-sequence trace-norm convergence: every subsequence has the same local limits', 'identification basis')
        require(rec['representation'] == 'GNS representation of omega_inf, canonically unitarily equivalent to that of each identified subsequential state',
                'representation named')
        require(rec['full_gns'] == 'as qualified in the AQ2 gate', 'full-GNS strengthening only as qualified')
        require(rec['uniqueness'] is False and rec['other_states'] is False, 'no uniqueness, no states outside the named constructions')
        return True
    IDENT = {'order': ['identify every subsequential limit with omega_inf on every finite region', 'extend to the quasi-local algebra', 'inherit'],
             'basis': 'whole-sequence trace-norm convergence: every subsequence has the same local limits',
             'representation': 'GNS representation of omega_inf, canonically unitarily equivalent to that of each identified subsequential state',
             'full_gns': 'as qualified in the AQ2 gate', 'uniqueness': False, 'other_states': False}
    # fixture: a trace-norm convergent sequence has one limit along every subsequence
    seq = [Q(1, 2) + Q(1, 3) * q ** n for n in range(40)]
    subseq_limits_agree = abs(seq[-1] - Q(1, 2)) < Q(1, 10 ** 60) and abs(seq[-2] - Q(1, 2)) < Q(1, 10 ** 60)
    check('item3_identification_and_inheritance',
          validate_identification(IDENT) and subseq_limits_agree and aq1_state and aq2_stmt and aq2_qual
          and rejected(lambda: validate_identification(dict(IDENT, order=['inherit', 'identify every subsequential limit with omega_inf on every finite region'])),
                       'inherited_before_identification')
          and rejected(lambda: validate_identification(dict(IDENT, full_gns='unconditional')), 'full_gns_strengthening_unqualified')
          and rejected(lambda: validate_identification(dict(IDENT, uniqueness=True)), 'vacuum_simplicity_read_as_uniqueness'),
          identification=IDENT, inherited=INHERIT, hypotheses=['H1', 'H2', 'H3'], status=COND,
          not_inherited=['uniqueness of every infinite-volume state', 'any statement about states outside the named constructions',
                         'equality of GNS dynamics of different states', 'anything uniform in the lattice spacing a'])

    # ======================= item 4: coarse translations through the general-volume comparison =======================
    incl_ok = True
    sharp_ok = True
    for N in range(2, 6):
        for vv in ((1, 0, 0), (0, -1, 1), (1, 1, 1), (-2, 0, 1), (0, 0, 2)):
            n = N - linf(vv)
            if n < 2:
                continue
            both = coarse_box(N) & coarse_box(N, vv)
            incl_ok = incl_ok and coarse_box(n) <= both
            sharp_ok = sharp_ok and not (coarse_box(n + 1) <= both)
    # covariance of both prescriptions under a coarse translation (F1 stars; F2 faces with owner sets inside the volume)
    omitted = [k for k, x in classes.items() if x[1] == 'omitted']

    def f1_stars(Vset):
        return frozenset(b for b in Vset if all(add(b, d) in Vset for d in S_STAR))

    def f2_faces(Vset):
        return frozenset((b, k) for b in Vset for k in omitted if frozenset(add(b, d) for d in classes[k][0]) <= Vset)
    cov_ok = True
    for vv in ((1, 0, 0), (0, -1, 1)):
        B0, B1 = coarse_box(2), coarse_box(2, vv)
        cov_ok = cov_ok and f1_stars(B1) == frozenset(add(b, vv) for b in f1_stars(B0))
        cov_ok = cov_ok and f2_faces(B1) == frozenset((add(b, vv), k) for (b, k) in f2_faces(B0))
    item4_bound = {(N, vl): C_h * q ** (N - vl - 1) for N in range(2, 9) for vl in range(0, N - 1)}
    item4_ok = all(N - vl >= 2 for (N, vl) in item4_bound) and item4_bound[(2, 0)] == C_h * q

    def validate_translation(rec):
        require(rec['basis'] == 'general_volume_comparison_H4', 'coarse translation invariance only from the general-volume comparison')
        require(rec['translation'] == 'coarse', 'only coarse translations (fine (4v_x,2v_y,v_z))')
        require(rec['N_condition'] == 'N >= |v|_inf+2', 'the contained cube Lambda_{N-|v|_inf} must have size at least 2')
        return True
    TR = {'basis': 'general_volume_comparison_H4', 'translation': 'coarse', 'N_condition': 'N >= |v|_inf+2'}
    check('item4_coarse_translation_invariance',
          incl_ok and sharp_ok and cov_ok and item4_ok and ba1_general and validate_translation(TR)
          and rejected(lambda: validate_translation(dict(TR, basis='nested_centered_cubes_only')), 'invariance_from_nested_cubes')
          and rejected(lambda: validate_translation(dict(TR, N_condition='N >= |v|_inf+1')), 'contained_cube_below_N_min'),
          statement='for every coarse v and N at least |v|_inf+2: ||rho^{Lambda_N+v}_R-rho^{Lambda_N}_R||_1 <= C_h q^(N-|v|_inf-1) (H4, R form, '
                    'applied with Lambda_{N-|v|_inf} inside both volumes); by covariance rho^{Lambda_N+v}_{Y+v} is the translate of rho^{Lambda_N}_Y; '
                    'hence the limit on every translate R+u exists and is the translate of rho^inf_R, and with the region form of H4 '
                    'omega_inf(tau_v(B))=omega_inf(B) for every finite region Y and B in B(H_Y)',
          constant='C_h (the hypothesis constant, factor 1)', value_at_N2_v0=s(item4_bound[(2, 0)]),
          inclusion_audit='Lambda_{N-|v|_inf} is contained in Lambda_N and in Lambda_N+v, and Lambda_{N-|v|_inf+1} is not (N=2..5, five shifts)',
          covariance_audit='F1 stars and F2 owner-set-contained faces of Lambda_2+v are the translates of those of Lambda_2 (v=(1,0,0),(0,-1,1))',
          tier=STATE_TIER, assembly=ASSEMBLY, hypothesis_source=HYP_SOURCE, hypotheses=['H4', 'H1', 'H2'], status=COND)

    # ======================= item 5: correlation functions =======================
    def rN(N):
        return (N - 1) // 2
    Cdyn_F1 = 2 * K_F1
    Cdyn_F2 = 2 * K_F1 + K_cmp / 4
    Cdyn = max(Cdyn_F1, Cdyn_F2)
    Cdyn_met = Cdyn <= V['target_Cdyn']
    # lemma: for N >= 5, (5N+1)(r_N-1) <= N^3/4, so b(N) = K_cmp (5N+1) N^-3 <= (K_cmp/4)/(r_N-1)
    lem_exact = all(Q((5 * N + 1) * (rN(N) - 1)) <= Q(N ** 3, 4) for N in range(5, 3001))
    g = lambda N: N ** 3 - 10 * N ** 2 + 28 * N + 6
    gp = lambda N: 3 * N ** 2 - 20 * N + 28
    lem_poly = g(5) == 21 and gp(5) == 3 and all(gp(N) > 0 for N in range(5, 50)) and all(2 * (rN(N) - 1) <= N - 3 for N in range(5, 3001))
    step_ok = all(rN(N) >= 2 and N - 1 >= 2 * (rN(N) - 1) and N - rN(N) >= 3 for N in range(5, 3001))

    def bracket_sum(N, Cd):
        r = rN(N)
        Y = (2 * r + 1) ** 3
        dyn = Cd / (r - 1)
        reg = cp * Y * exp_upper(Q(Y, 10 ** 8)) * q ** (N - r)
        mean = 2 * Cp * q ** (N - 1)
        return dyn, reg, mean, dyn + reg + mean
    sums = {N: bracket_sum(N, Cdyn) for N in range(5, 13)}
    sums_F1 = {N: bracket_sum(N, Cdyn_F1) for N in (5, 10)}
    rate_ok = all(Cdyn / (rN(N) - 1) <= 2 * Cdyn / (N - 4) for N in range(5, 400)) \
        and all(N * bracket_sum(N, Cdyn)[3] <= Q(6, 10 ** 9) for N in range(5, 60))

    def validate_item5(rec):
        require(rec['r_N'] == 'floor((N-1)/2)' and rec['N_min'] == 5, 'r_N frozen as written and N at least 5')
        require(rec['centering'] == 'complex_mean_abs_square', 'complex-mean centering |omega(A)|^2')
        require(rec['dynamics_term'] == 'C_dyn/(r_N-1)', 'polynomial dynamics term')
        require(rec['local_approximant'] == 'T^{F1,r_N}_theta(A) in B(H_{Lambda_{r_N}})', 'local approximant on Lambda_{r_N}')
        require(rec['state_region'] == 'Lambda_{r_N}', 'state difference on the region the approximant reaches, not only on R')
        return True
    I5 = {'r_N': 'floor((N-1)/2)', 'N_min': 5, 'centering': 'complex_mean_abs_square', 'dynamics_term': 'C_dyn/(r_N-1)',
          'local_approximant': 'T^{F1,r_N}_theta(A) in B(H_{Lambda_{r_N}})', 'state_region': 'Lambda_{r_N}'}
    check('item5_correlation_bound',
          Cdyn_met and lem_exact and lem_poly and step_ok and validate_item5(I5)
          and rejected(lambda: validate_item5(dict(I5, state_region='R')), 'state_difference_only_on_R')
          and rejected(lambda: validate_item5(dict(I5, N_min=4)), 'N4_r_N_minus_1_zero'),
          statement="for F in {F1,F2}, N at least 5, r=r_N=floor((N-1)/2), |theta|<=8, A in B(H_R): |c^{F,N}_A(theta)-c^inf_A(theta)| <= ||A||^2 "
                    "[C_dyn/(r_N-1) + c_site_prime |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N-r_N) + 2 C_prime q^(N-1)]",
          decomposition={'term_1': 'omega^{F,N}(A*[T^{F,N}(A)-T^{F1,r}(A)]): F1 <= K_F1/(r-1) (BA2 Cauchy, M=N); F2 <= b(N)+K_F1/(r-1)',
                         'term_2': '[omega^{F,N}-omega_inf](A* T^{F1,r}(A)) <= ||rho^{F,N}_{Lambda_r}-rho^inf_{Lambda_r}||_1 ||A||^2 (item 1 region form)',
                         'term_3': 'omega_inf(A*[T^{F1,r}(A)-T(A)]) <= K_F1/(r-1) (BA2 limit bound)',
                         'means': '||omega^{F,N}(A)|^2-|omega_inf(A)|^2| <= 2||A|| |omega^{F,N}(A)-omega_inf(A)| <= 2 C_prime q^(N-1) ||A||^2'},
          lemma='(5N+1)(r_N-1) <= N^3/4 for N at least 5 (g(N)=N^3-10N^2+28N+6 >= 21 at 5 and increasing), so b(N) <= (K_cmp/4)/(r_N-1)',
          C_dyn_F1_formula='2 K_F1', C_dyn_F1=s(Cdyn_F1), C_dyn_F1_preview=dec(Cdyn_F1),
          C_dyn_F2_formula='2 K_F1 + K_cmp/4', C_dyn_F2=s(Cdyn_F2), C_dyn_F2_preview=dec(Cdyn_F2),
          C_dyn=s(Cdyn), C_dyn_preview=dec(Cdyn), target=s(V['target_Cdyn']), target_met=Cdyn_met,
          margin_preview=dec(V['target_Cdyn'] / Cdyn, 6), tier=DYN_TIER, route=DYN_ROUTE, hypotheses=['H1', 'H2', 'H3'], status=COND)
    check('item5_rate_and_sums',
          rate_ok and all(sums[N][3] > 0 for N in sums),
          sums_headline={str(N): {'dynamics': dec(sums[N][0]), 'region': dec(sums[N][1]), 'mean': dec(sums[N][2]), 'total': dec(sums[N][3]),
                                  'total_exact': s(sums[N][3])} for N in (5, 10)},
          sums_headline_preview={str(N): dec(sums[N][3]) for N in sums},
          sums_F1={str(N): {'total': dec(sums_F1[N][3]), 'total_exact': s(sums_F1[N][3])} for N in sums_F1},
          rate='O(1/N): C_dyn/(r_N-1) <= 2 C_dyn/(N-4); the state terms decay geometrically in N; N times the bracket is at most 6x10^-9 for N=5..59',
          note='each constant is checked separately against its own target; no single bracket for the item-5 sum')

    # ======================= tau -> tau/100 scaling, per constant =======================
    def Cp_at(t):
        return Cprime(C_h, c_h)             # hypothesis constants and 1/(1-q) at fixed q are tau-independent

    def cp_at(t):
        return cprime(C_h, c_h)

    def Cdyn_at(t):
        return 2 * closed(a_c1, t) + closed(a_cmp, t) / 4

    def q2_at(t):
        return V['q2_per_tau'] * abs(t)

    def Cp2_at(t):
        return V['C_2h'] / (1 - q2_at(t))

    def cp2_at(t):
        return V['c_2h'] / (1 - q2_at(t))
    ratios = {'C_prime': Cp_at(tau_cap) / Cp_at(tau_cap / 100), 'c_site_prime': cp_at(tau_cap) / cp_at(tau_cap / 100),
              'C_dyn': Cdyn_at(tau_cap) / Cdyn_at(tau_cap / 100), 'secondary_C_prime': Cp2_at(tau_cap) / Cp2_at(tau_cap / 100),
              'secondary_c_site_prime': cp2_at(tau_cap) / cp2_at(tau_cap / 100), 'q_secondary': q2_at(tau_cap) / q2_at(tau_cap / 100)}
    BRK = {'C_prime': (Q(1), Q(1)), 'c_site_prime': (Q(1), Q(1)), 'C_dyn': V['bracket_Cdyn'], 'secondary_C_prime': V['bracket_secondary'],
           'secondary_c_site_prime': V['bracket_secondary'], 'q_secondary': (Q(100), Q(100))}

    def validate_scaling(name, ratio, br, source):
        require(source == 'contract', 'brackets are the preregistered ones, read from the contract')
        require(name in BRK and name != 'item_5_sum', 'each constant is checked separately; no single bracket for the item-5 sum')
        require(br[0] <= ratio <= br[1], 'scaling ratio outside its bracket: ' + name)
        return True
    lin_ratio = Q(100)
    check('tau_scaling_exponent',
          all(validate_scaling(k, ratios[k], BRK[k], 'contract') for k in ratios) and Cdyn_at(tau_cap) == Cdyn
          and ratios['C_dyn'] == Q(1953058850, 194651)
          and rejected(lambda: validate_scaling('C_dyn', lin_ratio, BRK['C_dyn'], 'contract'), 'C_dyn_linear_order')
          and rejected(lambda: validate_scaling('item_5_sum', ratios['C_dyn'], (Q(1), Q(20000)), 'contract'), 'single_lumped_item5_bracket')
          and rejected(lambda: validate_scaling('C_prime', Q(100), BRK['C_prime'], 'contract'), 'C_prime_scaled_like_BB1_constant')
          and rejected(lambda: validate_scaling('C_dyn', ratios['C_dyn'], (ratios['C_dyn'] - 1, ratios['C_dyn'] + 1), 'chosen_after_evaluation'),
                       'bracket_chosen_after_evaluation'),
          ratios={k: {'exact': s(x), 'preview': dec(x, 10), 'bracket': [s(BRK[k][0]), s(BRK[k][1])]} for k, x in ratios.items()},
          C_dyn_closed_form='(2*' + s(a_c1) + ' + ' + s(a_cmp) + '/4) tau^2/(1-' + s(den_c1) + '|tau|) = ' + s(2 * a_c1 + a_cmp / 4)
                            + ' tau^2/(1-' + s(den_c1) + '|tau|)',
          note='C_prime and c_site_prime are exactly tau-independent at the hypothesis values; the linear tau-scaling of the BB1 constants '
               'is checked in BB1 and recorded at the BB2 gate with the discharge; same exact formula at tau and tau/100')

    # ======================= secondary pair (labelled) =======================
    Cp2, cp2 = Cp2_at(tau_cap), cp2_at(tau_cap)
    check('secondary_pair_labelled',
          Cp2 <= V['target_Cp2'] and q2_at(tau_cap) == Q(151552, 10 ** 8),
          q_2=s(q2_at(tau_cap)), C_prime_2=s(Cp2), C_prime_2_preview=dec(Cp2), target=s(V['target_Cp2']),
          margin_preview=dec(V['target_Cp2'] / Cp2, 6), c_site_prime_2=s(cp2), c_site_prime_2_preview=dec(cp2),
          label='secondary, conditional on the BB1 secondary pair; decides nothing', status=COND)

    # ======================= controls =======================
    # conditional_on_bb1_targets
    def validate_conditional(rec):
        require(rec['C_h'] == V['C_h'] and rec['c_h'] == V['c_h'], 'BB1 values must be the frozen targets')
        require(rec['status'] == COND, 'every BB1-dependent conclusion is labelled conditional_on_bb1_targets')
        require(rec['unconditional_before_discharge'] is False, 'no conclusion is unconditional before the BB1 gate discharge')
        f = rec['fn']
        grid = [rat(k) * V['C_h'] / 4 for k in range(1, 9)]
        gridc = [rat(k) * V['c_h'] / 4 for k in range(1, 9)]
        for a in range(len(grid) - 1):
            for b in range(len(gridc)):
                require(f(grid[a + 1], gridc[b]) >= f(grid[a], gridc[b]), 'constant decreases in C_h')
        for a in range(len(grid)):
            for b in range(len(gridc) - 1):
                require(f(grid[a], gridc[b + 1]) >= f(grid[a], gridc[b]), 'constant decreases in c_h')
        return True
    CREC = {'C_h': V['C_h'], 'c_h': V['c_h'], 'status': COND, 'unconditional_before_discharge': False, 'fn': Cprime}
    check('conditional_on_bb1_targets',
          validate_conditional(CREC) and validate_conditional(dict(CREC, fn=cprime))
          and rejected(lambda: validate_conditional(dict(CREC, C_h=Q(1, 300000))), 'bb1_value_other_than_frozen_target')
          and rejected(lambda: validate_conditional(dict(CREC, status='unconditional')), 'condition_dropped')
          and rejected(lambda: validate_conditional(dict(CREC, unconditional_before_discharge=True)), 'unconditional_before_discharge')
          and rejected(lambda: validate_conditional(dict(CREC, fn=lambda a, b: Q(1, 100000) - a)), 'constant_decreasing_in_C_h'),
          functions={'C_prime': 'C_h/(1-q), nondecreasing in C_h (coefficient 64/63), independent of c_h',
                     'c_site_prime': 'c_h/(1-q), nondecreasing in c_h (coefficient 64/63), independent of C_h',
                     'item4_constant': 'C_h (identity)'},
          monotonicity='checked exactly on an 8x8 rational grid around the hypothesis values', status=COND,
          discharge='unconditional only when the BB1 gate admits, for H1-H4 in the forms, cutoff regimes and signs listed in hypotheses_used, '
                    'constants at most C_h=1/250000 (R form) and c_h=1/500000 (region form)')

    # r_N prefrozen
    def best_r(N):
        best = None
        for r in range(2, N - 1):
            val = bracket_sum_r(N, r)
            if best is None or val < best[0]:
                best = (val, r)
        return best[1]

    def bracket_sum_r(N, r):
        Y = (2 * r + 1) ** 3
        return Cdyn / (r - 1) + cp * Y * exp_upper(Q(Y, 10 ** 8)) * q ** (N - r) + 2 * Cp * q ** (N - 1)
    posthoc = {N: best_r(N) for N in range(5, 16)}
    differs = [N for N in posthoc if posthoc[N] != rN(N)]

    def validate_rN(fn):
        require(all(fn(N) == (N - 1) // 2 for N in range(5, 300)), 'r_N must be floor((N-1)/2) as frozen')
        return True
    check('r_N_prefrozen',
          validate_rN(rN) and len(differs) > 0
          and rejected(lambda: validate_rN(lambda N: posthoc.get(N, (N - 1) // 2)), 'post_hoc_optimized_r_N')
          and rejected(lambda: validate_rN(lambda N: N // 2), 'r_N_equals_floor_N_over_2'),
          r_N='floor((N-1)/2), read from the contract item 5', posthoc_optimum_differs_at_N=differs[:6],
          note='the frozen r_N is used even where another r would give a smaller bound')

    # tier mixing
    STATE_RECS = {'C_prime': {'tier': STATE_TIER, 'assembly': ASSEMBLY, 'hypothesis_source': HYP_SOURCE},
                  'c_site_prime': {'tier': STATE_TIER, 'assembly': ASSEMBLY, 'hypothesis_source': HYP_SOURCE},
                  'item4_C_h': {'tier': STATE_TIER, 'assembly': ASSEMBLY, 'hypothesis_source': HYP_SOURCE,
                                'note': 'direct application of H4 through the nested cube Lambda_{N-|v|_inf} inside both volumes; factor 1'}}
    DYN_RECS = {'C_dyn': {'tier': DYN_TIER, 'route': DYN_ROUTE, 'ba2_values': {'K_F1': s(K_F1), 'K_cmp': s(K_cmp)}}}

    def validate_tiers(st, dy, item5_brackets='separate'):
        for n_, r in st.items():
            require(r.get('tier') in ('exact_first_order', 'crude_majorant'), 'state constant tier: ' + n_)
            require(r.get('assembly') in ('nested_telescoping', 'union_comparison'), 'state constant assembly: ' + n_)
            require(r.get('hypothesis_source') == HYP_SOURCE, 'hypothesis source: ' + n_)
            require('route' not in r, 'a BB1 route is attached at the BB2 gate, never claimed by a BB2 producer: ' + n_)
        for n_, r in dy.items():
            require(r.get('tier') == DYN_TIER, 'dynamics constant tier: ' + n_)
            require(r.get('route') in ('duhamel_inner_f1', 'duhamel_inner_f2'), 'dynamics constant route: ' + n_)
            require(rat(r['ba2_values']['K_F1']) == K_F1 and rat(r['ba2_values']['K_cmp']) == K_cmp, 'exact BA2 gate values')
        require(item5_brackets == 'separate', 'no single lumped bracket for item 5')
        return True
    check('tier_mixing_rejected',
          validate_tiers(STATE_RECS, DYN_RECS) and V['tiers_allowed'] == ['crude_majorant', 'exact_first_order', 'polymer_kp', 'iterated_split',
                                                                           'polynomial_lieb_robinson', 'duhamel_inner_f1', 'duhamel_inner_f2']
          and rejected(lambda: validate_tiers(dict(STATE_RECS, C_prime=dict(STATE_RECS['C_prime'], tier=DYN_TIER)), DYN_RECS), 'state_constant_LR_tier')
          and rejected(lambda: validate_tiers(STATE_RECS, {'C_dyn': dict(DYN_RECS['C_dyn'], tier=STATE_TIER)}), 'dynamics_constant_state_tier')
          and rejected(lambda: validate_tiers(dict(STATE_RECS, c_site_prime=dict(STATE_RECS['c_site_prime'], route='polymer_kp')), DYN_RECS),
                       'bb1_route_claimed_by_bb2_producer')
          and rejected(lambda: validate_tiers(STATE_RECS, DYN_RECS, 'lumped'), 'single_lumped_item5_bracket')
          and rejected(lambda: validate_tiers(STATE_RECS, {'C_dyn': dict(DYN_RECS['C_dyn'], route=None)}), 'dynamics_route_missing'),
          state_constants=STATE_RECS, dynamics_constants=DYN_RECS, rule=V['tier_rule'])

    # rate constant pair prefrozen
    def validate_pair(qq, target_Cp, target_cp, hyp_pair):
        require(qq == V['q'] and target_Cp == V['target_Cp'] and target_cp == V['target_cp'], 'q and targets are the frozen ones')
        require(hyp_pair == (V['C_h'], V['c_h']), 'hypothesis pair is the frozen one')
        return True
    check('rate_constant_pair_prefrozen',
          validate_pair(q, V['target_Cp'], V['target_cp'], (C_h, c_h))
          and rejected(lambda: validate_pair(Q(1, 128), V['target_Cp'], V['target_cp'], (C_h, c_h)), 'q_retuned')
          and rejected(lambda: validate_pair(q, Cp * 2, V['target_cp'], (C_h, c_h)), 'target_moved_after_evaluation')
          and rejected(lambda: validate_pair(q, V['target_Cp'], V['target_cp'], (C_h / 2, c_h)), 'smaller_hypothesis_value'),
          pair={'q': s(q), 'C_prime_target': s(V['target_Cp']), 'c_site_prime_target': s(V['target_cp']), 'C_dyn_target': s(V['target_Cdyn'])})

    # subsequence versus whole sequence
    def validate_limit_claims(claims):
        for obj, (kind, basis) in claims.items():
            require(kind in ('whole_sequence', 'subsequence'), 'every limit statement says whole sequence or subsequence: ' + obj)
            if kind == 'whole_sequence':
                require(basis == 'cauchy_bound', 'whole-sequence claims come only from a Cauchy bound: ' + obj)
        return True
    CLAIMS = {'F1 reduced densities': ('whole_sequence', 'cauchy_bound'), 'F2 reduced densities': ('whole_sequence', 'cauchy_bound'),
              'AQ1 limit states (identified here)': ('subsequence', 'trace_norm_compactness'),
              'F2 limit states (identified here)': ('subsequence', 'trace_norm_compactness'),
              'F1 and F2 finite-box evolutions (BA2)': ('whole_sequence', 'cauchy_bound')}
    check('subsequence_versus_whole_sequence',
          validate_limit_claims(CLAIMS)
          and rejected(lambda: validate_limit_claims(dict(CLAIMS, **{'F1 reduced densities': ('whole_sequence', 'trace_norm_compactness')})),
                       'whole_sequence_from_compactness')
          and rejected(lambda: validate_limit_claims(dict(CLAIMS, **{'F2 reduced densities': ('limit', 'cauchy_bound')})), 'unlabelled_limit'),
          claims={k: list(x) for k, x in CLAIMS.items()})

    # fixture: whole sequence versus subsequence
    eps = Q(1, 100)
    osc = [(Q(1, 2) + (-1) ** N * eps, Q(1, 2) - (-1) ** N * eps) for N in range(2, 40)]   # diagonal 2x2 densities
    ball_ok = all(abs(a - Q(1, 2)) + abs(b - Q(1, 2)) <= 2 * eps for a, b in osc)          # one-state ball around diag(1/2,1/2)
    two_limits = len(set(osc[0::2])) == 1 and len(set(osc[1::2])) == 1 and osc[0] != osc[1]
    no_cauchy = all(abs(osc[i + 1][0] - osc[i][0]) + abs(osc[i + 1][1] - osc[i][1]) == 4 * eps for i in range(len(osc) - 1))
    Hs = [Q(0)]
    for k in range(2, 120):
        Hs.append(Hs[-1] + Q(1, k))                                                           # harmonic partial sums from k=2
    steps_to_zero = all(Hs[i + 1] - Hs[i] == Q(1, i + 2) for i in range(len(Hs) - 1))
    unbounded = Hs[-1] > 4

    def validate_convergence(evidence):
        require(evidence in ('sup_over_M_cauchy_bound',), 'convergence needs a sup-over-M Cauchy bound')
        return True
    check('fixture_whole_sequence_vs_subsequence',
          ball_ok and two_limits and no_cauchy and steps_to_zero and unbounded and validate_convergence('sup_over_M_cauchy_bound')
          and rejected(lambda: validate_convergence('one_state_ball_in_every_box'), 'one_state_ball_read_as_convergence')
          and rejected(lambda: validate_convergence('N_to_N_plus_1_steps_to_zero'), 'N_to_N_plus_1_bound_as_cauchy'),
          fixture_ball='rho_N=diag(1/2+(-1)^N/100, 1/2-(-1)^N/100): every rho_N within 1/50 of diag(1/2,1/2) (one-state ball), two subsequential '
                       'limits, ||rho_{N+1}-rho_N||_1=1/25 for every N',
          fixture_steps='a_N=sum_{k=2}^N 1/k: |a_{N+1}-a_N|=1/(N+1) tends to 0, a_N exceeds 4 at N=119 (no limit)',
          model_is_finite_graph=True, transfers_to_aq=False)

    # fixture: translation residues and face classes
    def role(p, o):
        return classes[face_class(p, o)][1]
    window = [(x, y, z) for x in range(0, 16) for y in range(0, 8) for z in range(0, 3)]

    def is_symmetry(w):
        vcoarse = fine_to_coarse_shift(w)
        roles_ok = all(role(p, o) == role(add(p, w), o) for p in window for o in ORIENT)
        own_shift = {sub(owner(add(p, w)), owner(p)) for p in window}
        owners_ok = len(own_shift) == 1
        classes_ok = all(face_class(p, o) == face_class(add(p, w), o) for p in window for o in ORIENT)
        return roles_ok and owners_ok and classes_ok, vcoarse
    coarse_ws = [(4, 0, 0), (0, 2, 0), (0, 0, 1), (4, 2, 1), (-8, 2, -3)]
    fine_ws = [(1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 1)]
    coarse_res = {str(w): is_symmetry(w) for w in coarse_ws}
    fine_res = {str(w): is_symmetry(w) for w in fine_ws}

    def validate_translation_symmetry(w):
        ok, vc = is_symmetry(w)
        require(ok and vc is not None, 'not a coarse translation: residues or face classes broken by ' + str(w))
        return True
    check('fixture_translation_residues',
          all(validate_translation_symmetry(w) for w in coarse_ws) and all(not fine_res[str(w)][0] for w in fine_ws)
          and rejected(lambda: validate_translation_symmetry((1, 0, 0)), 'fine_x_shift_by_1')
          and rejected(lambda: validate_translation_symmetry((0, 1, 0)), 'fine_y_shift_by_1')
          and rejected(lambda: validate_translation_symmetry((2, 0, 0)), 'fine_x_shift_by_2'),
          coarse=[str(w) + ' -> coarse ' + str(fine_to_coarse_shift(w)) for w in coarse_ws],
          non_coarse_rejected=[str(w) for w in fine_ws],
          detail='(1,0,0) maps the selected xy face at r=2 to the omitted class r=3 and splits the links of one factor between two factors; '
                 '(0,1,0) maps the selected s=0 row to the omitted s=1 row',
          model_is_finite_graph=True, transfers_to_aq=False)

    # translation invariance as a separate item: nested cubes alone do not give it (domain-wall fixture)
    def wall_marginal(box, x):
        a, b = box
        return 0 if 2 * x >= a + b else 1       # covariant rule: wall at the box centre
    nested_constant = all(wall_marginal((-N, N), x) == wall_marginal((-N - 1, N + 1), x) for N in range(2, 30) for x in range(-N, N + 1))
    translated_differs = all(wall_marginal((-N, N), 0) != wall_marginal((-N + 1, N + 1), 0) for N in range(2, 30))

    def validate_invariance(basis, general_volume_holds):
        require(basis == 'general_volume_comparison', 'translation invariance only from the general-volume comparison')
        require(general_volume_holds, 'the general-volume comparison must hold')
        return True
    check('translation_invariance_separate_item',
          nested_constant and translated_differs and validate_invariance('general_volume_comparison', True)
          and rejected(lambda: validate_invariance('nested_centered_cubes', True), 'invariance_from_nested_cubes')
          and rejected(lambda: validate_invariance('general_volume_comparison', not translated_differs), 'domain_wall_passes_general_volume'),
          fixture='1D covariant domain wall at the box centre: nested centered marginals are constant (a Cauchy sequence), the translated box '
                  '[-N+1,N+1] has the other marginal at 0 for every N (trace distance 2), and the limit is not translation invariant',
          model_is_finite_graph=True, transfers_to_aq=False)

    # fixture: correlation centering
    rho = mat([[Q(1, 2), 0], [0, Q(1, 2)]])
    A = mat([[(Q(3, 5), Q(4, 5)), 0], [0, 0]])
    AstarA = mmul(madj(A), A)
    mean = mtrace(mmul(rho, A))
    second = mtrace(mmul(rho, AstarA))
    centred_ok = csub(second, cz(cabs2(mean)))
    Ac = [[csub(A[i][j], mean if i == j else cz(0)) for j in range(2)] for i in range(2)]     # A - omega(A) I
    variance = mtrace(mmul(rho, mmul(madj(Ac), Ac)))
    wrong = csub(second, cmul(mean, mean))

    def validate_centering(val):
        require(val[1] == 0 and val == variance and val[0] >= 0, 'centering must use |omega(A)|^2: the value at theta=0 is the variance')
        return True
    a_, b_ = (Q(3, 10), Q(4, 10)), (Q(1, 5), Q(1, 10))
    # (|a|^2-|b|^2)^2 = (|a|+|b|)^2 (|a|-|b|)^2 <= 4 max(|a|^2,|b|^2) |a-b|^2, and max(|a|,|b|) <= ||A||
    mean_ineq = (cabs2(a_) - cabs2(b_)) ** 2 <= 4 * max(cabs2(a_), cabs2(b_)) * cabs2(csub(a_, b_))
    check('fixture_correlation_centering',
          validate_centering(centred_ok) and mean_ineq
          and rejected(lambda: validate_centering(wrong), 'centering_with_omega_A_squared')
          and rejected(lambda: validate_centering(second), 'uncentred_correlation'),
          fixture='rho=diag(1/2,1/2), A=diag((3+4i)/5,0): omega(A)=(3+4i)/10, omega(A*A)=1/2; omega(A*A)-|omega(A)|^2=1/4 (the variance); '
                  'omega(A*A)-omega(A)^2=(57-24i)/100 is not real',
          values={'mean': [s(mean[0]), s(mean[1])], 'correct': [s(centred_ok[0]), s(centred_ok[1])], 'wrong': [s(wrong[0]), s(wrong[1])]},
          mean_term='||a|^2-|b|^2| <= (|a|+|b|)|a-b| <= 2||A|| |a-b| (checked on a=(3+4i)/10, b=(2+i)/10)',
          also_rejected='a post-hoc r_N (r_N_prefrozen) and an exponential Lieb-Robinson tail with the polynomial F (lieb_robinson_polynomial_tail)',
          model_is_finite_graph=True, transfers_to_aq=False)

    # Lieb-Robinson polynomial tail
    def F_poly(r):
        return Q(1, (1 + r) ** 4)
    lower = {n: sum(Q((2 * z + 1) ** 2) * F_poly(3 * z) for z in range(n, 2 * n + 1)) for n in range(2, 31)}
    poly_lower_ok = all(n * lower[n] >= Q(1, 400) for n in lower)
    exp_contradicted = [n for n in lower if lower[n] > Q(1, 2 ** n)]

    def validate_dyn_rate(form):
        require(form == 'C_dyn/(r_N-1)', 'with F(r)=(1+r)^-4 the dynamics term is polynomial in N; an exponential tail is not available')
        return True
    check('lieb_robinson_polynomial_tail',
          poly_lower_ok and len(exp_contradicted) > 0 and validate_dyn_rate('C_dyn/(r_N-1)') and NS_QUOTES['eq53_condition'] in ns
          and rejected(lambda: validate_dyn_rate('C_dyn q^(r_N)'), 'exponential_tail_with_polynomial_F')
          and rejected(lambda: validate_dyn_rate('C_dyn e^(-r_N)'), 'exponential_decay_in_r_N'),
          tail_lower_bound_times_n_preview={str(n): dec(n * lower[n], 6) for n in (2, 5, 10, 20, 30)},
          exponential_contradicted_from_n=exp_contradicted[0],
          note='NS (53) needs Phi in B(Gamma,F_a) with F_a=e^{-ar}F; the admitted BA2 constants use F(r)=(1+r)^-4 only')

    # algebraic, not GNS dynamics
    ph = (Q(3, 5), Q(4, 5))
    Ud = [[cz(1), cz(0)], [cz(0), ph]]
    sx = mat([[0, 1], [1, 0]])
    evolved = mmul(mmul(Ud, sx), madj(Ud))
    prod_ = mmul(sx, evolved)
    corr0, corr1 = prod_[0][0], prod_[1][1]
    diff_states = corr0 == ph and corr1 == cconj(ph) and corr0 != corr1

    def validate_meaning(fields):
        require(fields['gns_dynamics_equality_claimed'] is False, 'no equality of GNS dynamics of different states')
        require(fields['dynamics_level'] == 'correlation_functions_compact_window', 'correlation functions of one limit state on a compact window')
        require(fields['uniform_in_time_claimed'] is False, 'no uniform-in-time claim')
        return True
    MEAN = {'gns_dynamics_equality_claimed': False, 'dynamics_level': 'correlation_functions_compact_window', 'uniform_in_time_claimed': False}
    check('algebraic_not_gns_dynamics',
          diff_states and validate_meaning(MEAN)
          and rejected(lambda: validate_meaning(dict(MEAN, gns_dynamics_equality_claimed=True)), 'gns_dynamics_equality_claimed')
          and rejected(lambda: validate_meaning(dict(MEAN, dynamics_level='gns_dynamics')), 'gns_level_label')
          and rejected(lambda: validate_meaning(dict(MEAN, uniform_in_time_claimed=True)), 'uniform_in_time'),
          fixture='one automorphism group (U=diag(1,(3+4i)/5)), two invariant vector states e_0, e_1: sigma_x correlations (3+4i)/5 versus (3-4i)/5',
          meaning='item 5 compares correlation functions of the finite-box states with those of the one common limit state omega_inf under the '
                  'algebraic dynamics T_theta; nothing identifies GNS dynamics of different states')

    # window and clock
    def validate_window(Theta, label, uniform_in_time):
        require(label == 'theta' and Theta == V['Theta'], 'window named in the common clock theta')
        require(uniform_in_time is False, 'no uniform-in-time claim')
        return True
    check('time_window_named_common_clock',
          validate_window(V['Theta'], 'theta', False)
          and rejected(lambda: validate_window(V['Theta'], 'theta', True), 'uniform_in_time_claimed')
          and rejected(lambda: validate_window(V['Theta'], 'u', False), 'u_window_labelled_theta'),
          window='|theta| at most 8, theta=alpha t/hbar; u=theta/8 internally (BA2 U=1)')
    alpha, hbar = Q(5), Q(7)
    t_phys = Q(56, 5)
    theta = alpha * t_phys / hbar
    u_norm = (alpha / 8) * t_phys / hbar

    def validate_clock(theta_v, u_v):
        require(theta_v == alpha * t_phys / hbar, 'theta = alpha t / hbar')
        require(u_v == theta_v / 8, 'u = delta t/hbar = theta/8 (delta = alpha/8)')
        return True
    check('wrong_delta_alpha_hbar_clock',
          theta == 8 and u_norm == 1 and validate_clock(theta, u_norm)
          and rejected(lambda: validate_clock(theta, theta), 'eightfold_u_labelled_theta')
          and rejected(lambda: validate_clock(alpha * t_phys, u_norm), 'hbar_dropped')
          and rejected(lambda: validate_clock(theta, alpha * t_phys / hbar), 'delta_equals_alpha'),
          fixture='alpha=5, hbar=7, t=56/5: theta=8, u=1 (non-unit constants)')

    def validate_common_clock(rec):
        require(rec['tau_F1'] == rec['tau_F2'] == rec['tau_limit'], 'both families and the limit at the same coupling')
        require(rec['clock_finite'] == rec['clock_limit'] == 'theta=alpha t/hbar', 'finite-box and limit dynamics in the same clock')
        return True
    CC = {'tau_F1': tau_cap, 'tau_F2': tau_cap, 'tau_limit': tau_cap, 'clock_finite': 'theta=alpha t/hbar', 'clock_limit': 'theta=alpha t/hbar'}
    check('common_clock',
          validate_common_clock(CC) and validate_common_clock(dict(CC, tau_F1=-tau_cap, tau_F2=-tau_cap, tau_limit=-tau_cap))
          and rejected(lambda: validate_common_clock(dict(CC, tau_F2=-tau_cap)), 'F2_at_opposite_sign')
          and rejected(lambda: validate_common_clock(dict(CC, clock_limit='u=alpha t/(8 hbar)')), 'limit_in_other_clock'),
          note='each sign has its own limit state; limits at +tau and -tau are never compared')

    # root-N misuse
    steps = [C_h * q ** (k - 1) for k in range(2, 12)]

    def validate_linear(total, parts):
        require(total == sum(parts), 'deterministic step bounds add linearly')
        return True
    check('root_n_misuse',
          validate_linear(sum(steps), steps)
          and rejected(lambda: validate_linear(sum(steps) / 3, steps), 'division_by_isqrt_of_10_steps')
          and rejected(lambda: validate_linear(max(steps), steps), 'largest_step_only'),
          note='the telescoping steps and the three item-5 terms add linearly; no square-root combination')

    # uniform in N, not in a (text scan below), rate in N not in a
    def validate_rate_units(unit):
        require(unit == 'per coarse step at fixed spacing', 'rates are per coarse step at fixed spacing')
        return True
    check('decay_rate_in_N_not_a',
          validate_rate_units('per coarse step at fixed spacing')
          and rejected(lambda: validate_rate_units('per fm'), 'conversion_to_fm')
          and rejected(lambda: validate_rate_units('in the lattice spacing a'), 'rate_in_a'),
          coarse_step='(4a,2a,a) in fine units; q=1/64 per coarse l-infinity step; 1/N for the dynamics term')

    # topology
    TOP = {'states': 'trace norm on B(H_Y) (local trace norm)', 'dynamics': 'operator norm on B(H_R), uniformly for |theta| at most 8',
           'representations': 'GNS strong (strongly continuous unitary group)'}
    def proj(n, dim):
        return [[cz(1 if (i == j == n) else 0) for j in range(dim)] for i in range(dim)]
    escape = all(mtrace(mmul(proj(n, n + 1), proj(1, n + 1))) == cz(0) and mtrace(proj(n, n + 1)) == cz(1) for n in range(2, 12))
    # Tr(|e_n><e_n| K)=0 for K=|e_1><e_1| while the positive |e_n><e_n| has trace norm 1: weak-* convergence is not trace-norm convergence

    def validate_topology(t):
        require(t == TOP, 'topologies named: trace norm for states, operator norm on the window for dynamics, GNS strong for representations')
        return True
    check('topology_named',
          escape and validate_topology(dict(TOP))
          and rejected(lambda: validate_topology(dict(TOP, states='weak-* on B(H_Y)')), 'weak_star_relabelled_trace_norm')
          and rejected(lambda: validate_topology(dict(TOP, representations='norm continuity in time on full B(H)')), 'norm_time_continuity_claimed'),
          topology=TOP,
          fixtures={'fixed_vs_moving_vector': 'U(t)e_j=e^{ijt}e_j, Ae_j=e_{2j}: ||(U(pi/n)AU(pi/n)*-A)e_n||=2 on the moving vector e_n; '
                                              '<= |t| on the fixed e_1',
                    'mass_escape': '|e_n><e_n| tends to 0 against every finite-rank observable but has trace norm 1'})

    # two families
    FAM = {'F1': 'AQ1 centered whole-star boxes Lambda_N=[-N,N]^3, N at least 2',
           'F2': 'I1 section 6 all-contained-face boxes with padding on the same Lambda_N, N at least 2'}

    def validate_families(fam):
        require(sorted(fam) == ['F1', 'F2'], 'exactly the two named families')
        require('whole-star' in fam['F1'] and 'all-contained-face' in fam['F2'] and 'padding' in fam['F2'], 'family definitions')
        require(all('Lambda_N' in x and 'orthant' not in x and 'literal' not in x for x in fam.values()), 'centered boxes only')
        return True
    check('two_families_named',
          validate_families(FAM)
          and rejected(lambda: validate_families({'F1': FAM['F1']}), 'one_family_only')
          and rejected(lambda: validate_families(dict(FAM, F3='I1 section 7 literal vertex boxes Lambda_N')), 'third_family_literal_boxes')
          and rejected(lambda: validate_families(dict(FAM, F2='I1 section 6 all-contained-face orthant boxes Lambda_N with padding')), 'orthant_boxes'),
          families=FAM)

    # named construction, not uniqueness
    Hd = [Q(0), Q(0), Q(1)]
    constructed = (1, 0, 0)                  # the named construction (boundary field -|e_0><e_0|/N) selects e_0 for every N
    other_ground = (0, 1, 0)
    other_is_ground = sum(Hd[i] * other_ground[i] for i in range(3)) == min(Hd)

    def validate_naming(rec):
        require(rec['label'] in V['sub_labels'], 'sub-label from the contract')
        require(rec['uniqueness_of_ground_state_claimed'] is False, 'no uniqueness of any ground state')
        require(rec['object'] == 'the limit of the named constructions F1 and F2', 'the object is the limit of the named constructions')
        return True
    NM = {'label': 'convergence_of_named_constructions', 'uniqueness_of_ground_state_claimed': False,
          'object': 'the limit of the named constructions F1 and F2'}
    check('named_construction_not_uniqueness',
          other_is_ground and constructed != other_ground and validate_naming(NM)
          and rejected(lambda: validate_naming(dict(NM, uniqueness_of_ground_state_claimed=True)), 'uniqueness_claimed')
          and rejected(lambda: validate_naming(dict(NM, object='every infinite-volume ground state')), 'object_widened'),
          fixture='H=diag(0,0,1): the named construction (field -|e_0><e_0|/N) converges to e_0 as a whole sequence, while e_1 is another '
                  'ground vector of the limit operator; convergence of a named construction is not uniqueness',
          model_is_finite_graph=True, transfers_to_aq=False)

    # Cauchy estimate, not compactness
    ay2_scenario = 'differ by at least (1-2*10^-6)2K_2' in ay2g['accepted'] or 'falsifying scenario is not excluded' in ay2g['accepted']

    def validate_basis(b):
        require(b == 'explicit_cauchy_bound_and_trace_class_completeness', 'whole-sequence convergence from an explicit Cauchy bound')
        return True
    check('cauchy_estimate_not_compactness',
          ay2_scenario and validate_basis('explicit_cauchy_bound_and_trace_class_completeness')
          and rejected(lambda: validate_basis('compactness_plus_closeness'), 'compactness_plus_closeness')
          and rejected(lambda: validate_basis('compactness_plus_first_order_agreement'), 'compactness_plus_first_order_agreement'),
          note='AY2 exhibits two admissible densities within every one-state bound that differ by about 2K_2 tau^2: closeness plus compactness '
               'cannot identify limits; the explicit bound sup_M ||rho^M-rho^N||_1 <= C q^N does')

    # limit identified with AQ1 limits (separate control)
    def validate_inherit_order(steps_):
        require(steps_.index('identify') < steps_.index('inherit'), 'inherit only after identification')
        require('extend_by_norm_continuity' in steps_, 'identification on local algebras extends to the quasi-local algebra')
        return True
    check('limit_identified_with_aq1_limits',
          validate_inherit_order(['identify', 'extend_by_norm_continuity', 'inherit']) and aq1_extract
          and rejected(lambda: validate_inherit_order(['inherit', 'identify', 'extend_by_norm_continuity']), 'inherit_first')
          and rejected(lambda: validate_inherit_order(['identify', 'inherit']), 'no_extension_to_quasi_local'),
          statement='every AQ1 subsequential limit (trace-norm limits along N_k on every finite F) equals omega_inf on every finite region, hence on '
                    'the quasi-local algebra; the same for every F2 subsequential limit (AY1 extraction) through item 2', status=COND)

    # region constant scales with Y (separate control)
    def validate_region_scaling(form_Y, N):
        Y = coarse_box(2)
        val = form_Y(Y, N)
        honest = cp * len(Y) * q ** dY(Y, N)
        require(val >= honest, 'a region bound must carry |Y| and d_Y (a constant proved for R reused on Y is rejected)')
        return True
    check('region_constant_scales_with_Y',
          validate_region_scaling(lambda Y, N: cp * len(Y) * exp_upper(Q(len(Y), 10 ** 8)) * q ** dY(Y, N), 5)
          and rejected(lambda: validate_region_scaling(lambda Y, N: Cp * q ** (N - 1), 5), 'R_constant_reused_on_Lambda_2')
          and rejected(lambda: validate_region_scaling(lambda Y, N: cp * q ** dY(Y, N), 5), 'size_factor_dropped'),
          example='Y=Lambda_2 at N=5: region form ' + dec(cp * 125 * exp_upper(Q(125, 10 ** 8)) * q ** 3) + ' versus the R form '
                  + dec(Cp * q ** 4))

    # parameters declare metric, weights, window
    def validate_parameters(params):
        for key in ('metric', 'weights', 'rate_constant_pair', 'assembly', 'items', 'cutoff', 'N_min', 'clock', 'window'):
            require(key in params and params[key], 'parameters field missing: ' + key)
        return True
    check('parameters_declare_metric_weights_window',
          validate_parameters(V['parameters'])
          and rejected(lambda: validate_parameters({k: x for k, x in V['parameters'].items() if k != 'window'}), 'window_field_absent')
          and rejected(lambda: validate_parameters({k: x for k, x in V['parameters'].items() if k != 'metric'}), 'metric_field_absent'),
          declared=sorted(V['parameters']))

    # model relabelling
    MODEL = {'model_id': V['model_id'], 'tau': s(tau_cap), 'triple': [s(x) for x in V['triple']], 'families': sorted(FAM),
             'state_metric': 'coarse l-infinity', 'dynamics_metric': 'coarse l1, F(r)=(1+r)^-4', 'window': '|theta|<=8', 'group': 'SU(2)',
             'dimension': 3, 'finite_graph': False, 'cover': 'R={0,e_z}'}

    def validate_model(mdl):
        require(mdl == MODEL and rat(mdl['tau']) == tau_cap, 'model packet differs from the contract')
        return True
    check('changed_model_relabelled',
          validate_model(dict(MODEL))
          and rejected(lambda: validate_model(dict(MODEL, tau='1/100000000000000')), 'tau_changed')
          and rejected(lambda: validate_model(dict(MODEL, triple=['1', '0', '0'])), 'nonzero_triple')
          and rejected(lambda: validate_model(dict(MODEL, state_metric='coarse l1')), 'state_metric_changed')
          and rejected(lambda: validate_model(dict(MODEL, model_id='AX_uniform_route_B')), 'uniform_route_B_model')
          and rejected(lambda: validate_model(dict(MODEL, group='SU(3)')), 'other_group')
          and rejected(lambda: validate_model(dict(MODEL, finite_graph=True)), 'finite_graph'),
          model=MODEL)

    # exact arithmetic
    check('exact_arithmetic_admission',
          rat('1/100000000') == tau_cap and isinstance(Cp, Q) and isinstance(Cdyn, Q)
          and rejected(lambda: rat(1e-8), 'float_input')
          and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('nan'), 'nan_input')
          and rejected(lambda: rat('1/0'), 'zero_denominator')
          and rejected(lambda: rat(dec(Cdyn)), 'preview_decimal_read_as_admission_value')
          and rejected(lambda: exp_upper(Q(1)), 'exp_enclosure_outside_radius'),
          note='every admission Boolean is a Fraction comparison; e^x is replaced by the directed bound 1/(1-x)')

    # error ledger
    ledger = {
        'bb1_hypothesis_constants': {'value': 'C_h=' + s(C_h) + ', c_h=' + s(c_h) + ' at q=' + s(q) + ' (frozen targets, hypotheses)',
                                     'status': COND, 'note': 'not proved here; discharged only by the BB1 gate'},
        'cauchy_telescoping_or_union': {'value': 'factor 1/(1-q) = ' + s(1 / (1 - q)) + ' (nested telescoping, full geometric tail)',
                                        'dropped': 'the nonnegative remainder C_h q^(M-1)/(1-q) is kept as slack; nothing is dropped from the bound'},
        'identification_with_subsequential_limits': {'value': '0', 'status': 'not_applicable',
                                                      'reason': 'exact equality: a trace-norm limit of the whole sequence is the limit of every '
                                                                'subsequence; no estimate enters'},
        'translation_general_volume': {'value': 'C_h q^(N-|v|_inf-1) (H4, R form); region form c_h |Y| e^{|Y|/10^8} q^(N-|v|_inf-max|y|_inf)',
                                       'status': COND},
        'dynamics_constant_from_ba2': {'value': 'C_dyn = 2K_F1 + K_cmp/4 = ' + s(Cdyn), 'preview': dec(Cdyn),
                                       'F1_value': s(Cdyn_F1), 'lemma': '(5N+1)(r_N-1) <= N^3/4 for N at least 5', 'status': 'admitted BA2 values'},
        'region_form_on_Lambda_rN': {'value': "c_site_prime |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N-r_N), |Lambda_r|=(2r+1)^3",
                                     'enclosure': 'e^x <= 1/(1-x)', 'status': COND},
        'arithmetic': {'value': '0', 'status': 'not_applicable',
                       'reason': 'exact Fractions throughout; the only transcendental factor e^{|Y|/10^8} is replaced by the directed upper bound 1/(1-|Y|/10^8)'},
    }
    check('error_ledger_itemized',
          sorted(ledger) == sorted(V['error_terms']) and all(('reason' in e) for e in ledger.values() if e.get('status') == 'not_applicable'),
          ledger_terms=sorted(ledger), rule=V['error_terms_rule'])

    # verdict logic
    def forward_verdict(cauchy_closed, items_met, discharge):
        if not cauchy_closed:
            return 'insufficient'
        if not all(items_met.values()):
            return 'limited'
        return 'accepted_within_scope' if discharge == 'pending_bb1_gate' else 'limited'
    items_met = {'1': Cp_met and cp_met, '2': True, '3': True, '4': True, '5': Cdyn_met}
    verdict = forward_verdict(True, items_met, 'pending_bb1_gate')

    def validate_verdict(label, cauchy_closed, im, discharge, hyp_values):
        require(hyp_values == (V['C_h'], V['c_h']), 'retuning the hypotheses is rejected')
        require(label == forward_verdict(cauchy_closed, im, discharge), 'verdict label differs from the acceptance rule')
        require(discharge in ('pending_bb1_gate', 'partial'), 'the producer cannot record a discharge')
        return True
    check('insufficient_verdict_retained',
          verdict == 'accepted_within_scope' and validate_verdict(verdict, True, items_met, 'pending_bb1_gate', (C_h, c_h))
          and rejected(lambda: validate_verdict('accepted_within_scope', True, dict(items_met, **{'5': False}), 'pending_bb1_gate', (C_h, c_h)),
                       'missed_item_relabelled_accepted')
          and rejected(lambda: validate_verdict('limited', False, items_met, 'pending_bb1_gate', (C_h, c_h)), 'open_cauchy_relabelled_limited')
          and rejected(lambda: validate_verdict('accepted_within_scope', True, items_met, 'discharged_by_producer', (C_h, c_h)),
                       'producer_declares_discharge')
          and rejected(lambda: validate_verdict('accepted_within_scope', True, items_met, 'pending_bb1_gate', (C_h / 2, c_h)), 'hypothesis_retuned'),
          verdict=verdict, retained_outcomes={'limited': 'region form or general-volume comparison not admitted by the BB1 gate (items dropped as '
                                                         'the contract lists), or a partial discharge',
                                              'insufficient': 'BB1 insufficient: every item stays a labelled conditional statement'})

    # claim flags
    FLAGS = {'continuum_claim': False, 'scientific_priority_verified': False, 'uniqueness_of_ground_state_claimed': False,
             'gns_dynamics_equality_claimed': False, 'uniform_in_time_claimed': False, 'rate_in_a_claimed': False, 'weak_coupling_claim': False}

    def validate_flags(fl):
        for k1, v1 in FLAGS.items():
            require(fl.get(k1) is v1, 'claim flag ' + k1 + ' must be false')
        return True

    def fmut(**kw):
        f2_ = dict(FLAGS)
        f2_.update(kw)
        return lambda: validate_flags(f2_)
    check('no_priority_or_continuum_claim',
          validate_flags(FLAGS)
          and rejected(fmut(continuum_claim=True), 'continuum_true') and rejected(fmut(scientific_priority_verified=True), 'priority_true')
          and rejected(fmut(weak_coupling_claim=True), 'weak_coupling_true') and rejected(fmut(rate_in_a_claimed=True), 'rate_in_a_true'),
          historical_or_occult_numeric_premise=False)

    # gate fields: exactly the contract fields, proposed conditional on the BB1 discharge
    dependent = [k for k, x in V['gate_fields'].items() if x is True] + ['dynamics_level', 'whole_sequence_scope', 'translation_invariance_scope']
    GATE = dict(V['gate_fields'])
    UNDISCHARGED = {k: (False if isinstance(x, bool) and x is True else x) for k, x in V['gate_fields'].items()}
    UNDISCHARGED['dynamics_level'] = 'not_set (conditional_on_bb1_targets)'

    def validate_gate(g):
        require(sorted(g) == sorted(V['gate_fields']), 'gate fields must be exactly the contract fields')
        for k1, v1 in g.items():
            require(v1 == V['gate_fields'][k1] and type(v1) is type(V['gate_fields'][k1]), 'gate field differs from the contract: ' + k1)
        return True
    check('gate_fields_exported',
          validate_gate(GATE) and all(UNDISCHARGED[k] is False for k in V['gate_fields'] if V['gate_fields'][k] is True)
          and rejected(lambda: validate_gate({k1: v1 for k1, v1 in GATE.items() if k1 != 'dynamics_level'}), 'field_missing')
          and rejected(lambda: validate_gate(dict(GATE, uniqueness_of_ground_state_claimed=True)), 'uniqueness_true')
          and rejected(lambda: validate_gate(dict(GATE, gns_dynamics_equality_claimed=True)), 'gns_equality_true'),
          gate_fields_proposed=GATE, gate_fields_if_undischarged=UNDISCHARGED, dependent_on_bb1=sorted(dependent),
          rule=V['gate_fields_rule'], status=COND)

    # mandatory sentence
    template = V['template']
    count_template = report_text.count(template)
    check('mandatory_sentence_verbatim_once',
          count_template == 1, occurrences_in_report=count_template, template_sha256=sha_bytes(template.encode('utf-8')))

    # text scans
    forbidden = ROUND_FORBIDDEN + V['forbidden']
    STATEMENTS = [
        'Conditional on the BB1 frozen targets as hypotheses, the reduced densities of the named construction families F1 and F2 converge as '
        'whole sequences at a rate in N, to one common limit on every finite region; this is convergence of the named constructions, not '
        'uniqueness of any ground state.',
        'The limit coincides with every AQ1 subsequential limit and every F2 subsequential limit and inherits exactly the admitted AQ1, BA2 and '
        'AQ2 properties in its own GNS representation, the full-GNS strengthening only as qualified in the AQ2 gate.',
        'Its correlation functions on |theta| at most 8 are limits of the finite-box correlation functions with three separate constants; '
        'nothing is claimed uniformly in time, no GNS dynamics of different states are equated, and no estimate is uniform in the lattice spacing a.']
    scan_texts = {'report.md': report_text, 'statements': ' '.join(STATEMENTS)}

    def validate_uniformity(texts):
        for name, txt in texts.items():
            bad = uniformity_violations(txt, template)
            require(not bad, 'unqualified uniformity statement in ' + name + ': ' + (bad[0] if bad else ''))
        return True
    check('uniform_in_N_not_in_a',
          validate_uniformity(scan_texts)
          and rejected(lambda: validate_uniformity({'m': 'The Cauchy constant is uniform in the lattice spacing a.'}), 'uniform_in_a_claimed')
          and rejected(lambda: validate_uniformity({'m': 'The convergence is uniform.'}), 'unqualified_uniform'),
          qualifiers=list(UNIFORM_QUALIFIERS))

    def validate_placeholders(texts):
        for name, txt in texts.items():
            body = normalize(txt).replace(normalize(template), ' ')     # the template is removed as one literal first
            spans = placeholder_spans(body)
            require(not spans and '<' not in body, 'placeholder span in ' + name + ': ' + (spans[0] if spans else '<'))
        return True
    check('placeholder_span_rejected',
          validate_placeholders(scan_texts)
          and rejected(lambda: validate_placeholders({'m': "C' = <constant to be filled>"}), 'whitespace_placeholder')
          and rejected(lambda: validate_placeholders({'m': 'verdict <accepted|limited>'}), 'vertical_bar_placeholder')
          and rejected(lambda: validate_placeholders({'m': 'N_min <e.g.5>'}), 'eg_placeholder'),
          scanned=['report.md', 'exported statements'])

    def validate_phrases(texts):
        for name, txt in texts.items():
            hits = affirmative_phrase_hits(txt, forbidden, template)
            require(not hits, 'affirmative forbidden phrasing in ' + name + ': ' + (hits[0]['phrase'] if hits else ''))
        return True
    negated_ok = not affirmative_phrase_hits('This is not the thermodynamic limit of any state.', forbidden, template)
    check('negation_aware_phrase_scan',
          validate_phrases(scan_texts) and negated_ok
          and rejected(lambda: validate_phrases({'m': 'We construct the thermodynamic limit.'}), 'affirmative_thermodynamic_limit')
          and rejected(lambda: validate_phrases({'m': 'The common limit is the infinite-volume ground state.'}), 'affirmative_infinite_volume_ground_state')
          and rejected(lambda: validate_phrases({'m': 'The limit confirms translation invariance.'}), 'affirmative_confirms'),
          forbidden_count=len(forbidden), template_removed_as_one_literal=True,
          note='same rule as research/round33/tools/phrase_scan.py (round list copied, contract list read from the contract)')

    # reverse premise isolation (declared inventories)
    forward_list = ['AGENTS.md', CONTRACT_REL] + V['shared']
    reverse_list = ['AGENTS.md', CONTRACT_REL] + V['shared']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    allowed_skeptic = {'research/round33/skeptic/ba1.md', 'research/round33/skeptic/ba2.md'}
    bad_parts = ('research/round33/forward/bb1', 'research/round33/reverse/bb1', 'research/round33/advisor/bb1', 'research/round33/skeptic/bb',
                 'research/round33/forward/bb2', 'research/round33/experts/', 'deliberation', 'triage', 'recommendation', 'prospective-controls',
                 'loop2', 'loop-2', 'memo', 'advisor/plan', 'advisor/panel', 'contract-review')

    def validate_isolation(decl, lst):
        require(decl is True, 'contract does not declare reverse premise isolation')
        require(sorted(set(lst)) == sorted(set(['AGENTS.md', CONTRACT_REL] + V['shared'])), 'reverse inventory must equal AGENTS, contract and shared premises')
        for item in lst:
            require(not any(b1_ in item for b1_ in bad_parts), 'reverse premise isolation violated by ' + item)
            if item.startswith('research/round33/skeptic/'):
                require(item in allowed_skeptic, 'only the declared BA1 and BA2 reviews: ' + item)
        return True
    check('reverse_premise_isolation',
          sorted(inventory) == sorted(set(forward_list)) and len(inventory) == 38 and 'forward_additional_premises' not in c
          and validate_isolation(V['reverse_isolation'], reverse_list)
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round33/forward/bb1/report.md']), 'reads_bb1_producer')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round33/advisor/bb1-gate.json']), 'reads_bb1_gate')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round33/skeptic/bb1.md']), 'reads_bb1_skeptic')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round33/forward/bb2/report.md']), 'reverse_reads_forward_bb2')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round33/experts/jung/memo.md']), 'reads_lens_memo')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round33/skeptic/ba2-contract-review.md']), 'reads_other_skeptic_file'),
          forward_inventory_files=len(inventory), reverse_premise_count=len(set(reverse_list)),
          limitation="the forward checker verifies the declared inventories only; the reverse agent's actual reads are checked by freeze.py and the skeptic")

    # ======================= packet and coherent tampering =======================
    HEAD = {
        'C_prime': {'function': 'C_h/(1-q)', 'value': s(Cp), 'preview': dec(Cp), 'target': s(V['target_Cp']), 'target_met': Cp_met,
                    'tier': STATE_TIER, 'assembly': ASSEMBLY, 'hypothesis_source': HYP_SOURCE, 'bb1_route': 'attached at the BB2 gate'},
        'c_site_prime': {'function': 'c_h/(1-q)', 'value': s(cp), 'preview': dec(cp), 'target': s(V['target_cp']), 'target_met': cp_met,
                         'tier': STATE_TIER, 'assembly': ASSEMBLY, 'hypothesis_source': HYP_SOURCE, 'bb1_route': 'attached at the BB2 gate'},
        'C_dyn': {'function': '2 K_F1 + K_cmp/4 (F2; F1 needs only 2 K_F1)', 'value': s(Cdyn), 'preview': dec(Cdyn), 'F1_value': s(Cdyn_F1),
                  'F1_preview': dec(Cdyn_F1), 'target': s(V['target_Cdyn']), 'target_met': Cdyn_met, 'tier': DYN_TIER, 'route': DYN_ROUTE,
                  'ba2_gate_values': {'K_F1': s(K_F1), 'K_cmp': s(K_cmp)}},
        'item4': {'bound': 'C_h q^(N-|v|_inf-1), N at least |v|_inf+2', 'constant': s(C_h), 'tier': STATE_TIER, 'assembly': ASSEMBLY,
                  'hypothesis_source': HYP_SOURCE},
        'item5_sums': {'N5': s(sums[5][3]), 'N5_preview': dec(sums[5][3]), 'N10': s(sums[10][3]), 'N10_preview': dec(sums[10][3])},
        'secondary': {'C_prime_2': s(Cp2), 'C_prime_2_preview': dec(Cp2), 'target': s(V['target_Cp2']), 'c_site_prime_2': s(cp2),
                      'label': 'labelled; conditional on the BB1 secondary pair'},
    }
    label = 'convergence_of_named_constructions'
    verdict_line = (verdict + ' (forward half, ' + COND + ': unconditional only after the BB1 gate admits, for comparisons H1-H4 in the R and '
                    'region forms, both signs, each on-site cutoff space uniformly in L and at fixed N for the untruncated vectors, constants at most '
                    'C_h=1/250000 and c_h=1/500000; otherwise limited or insufficient as the contract acceptance lists; the contract acceptance also '
                    'requires the reverse route, the skeptical review and the BB1 gate); sub-labels convergence_of_named_constructions, '
                    'common_limit_of_named_constructions')
    packet = {
        'loop': 'BB2', 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'contribution_alias': 'HNM-BB2-F nested-telescoping whole-sequence convergence of the reduced densities of the named constructions, their '
                              'common limit, its identification with every AQ1 and F2 subsequential limit, coarse translation invariance and '
                              'correlation functions on |theta| at most 8 (conditional_on_bb1_targets)',
        'ai_assistance': 'AI-assisted forward production (Claude model agent); correlated model-agent work, not independent human review',
        'contract_sha256': contract_digest, 'bb1_contract_sha256': bb1_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'pinned_gate_sha256': dict(PINNED_GATES), 'ns_excerpt_sha256': NS_SHA256,
        'assembly': ASSEMBLY, 'label': label, 'secondary_sub_labels': ['common_limit_of_named_constructions'],
        'model': MODEL, 'families': FAM, 'clock': V['clock'], 'topology': TOP,
        'tau_values': {sg: s(tv) for sg, tv in taus.items()},
        'headline': HEAD, 'hypotheses_used': HYP, 'hypotheses_not_used': NOT_USED, 'conditional_on_bb1_targets': True,
        'unconditional_claims': ['BA2 dynamics constants (admitted)', 'fixtures (finite, transfers_to_aq false)'],
        'error_terms_itemized': ledger, 'statements': STATEMENTS, 'mandatory_sentence': template,
        'gate_fields': GATE, 'gate_fields_status': 'proposed; every dependent field holds only after the BB1 gate discharge (gate_fields_rule)',
        'gate_fields_if_undischarged': UNDISCHARGED,
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions'],
                       'additional': ['no BB1 value other than the frozen targets', 'no statement at fixed N beyond the hypotheses',
                                      'no comparison of limits at different couplings or signs', 'no non-coarse translation',
                                      'no fine-lattice or physical length reading of N', 'no statement outside |theta| at most 8 for item 5']},
        'routes_executed': ['forward nested telescoping over the BB1 nested comparisons H1, H2 (item 1), in each Q_L, then AV1/AY1 cutoff-vector removal at fixed N',
                            'fixed-N F1 versus F2 hypothesis H3 plus item 1 (item 2)',
                            'identification of every AQ1 and F2 subsequential limit, extension to the quasi-local algebra, inheritance (item 3)',
                            'covariance plus the general-volume hypothesis H4 with Lambda_{N-|v|_inf} (item 4)',
                            'local approximant T^{F1,r_N}_theta(A), BA2 Cauchy/limit/comparison bounds, item-1 region form on Lambda_{r_N} (item 5)'],
        'routes_not_executed': ['reverse union comparison (outside this producer)', 'direct comparison of any two centered boxes (labelled only)',
                                'duhamel_inner_f2 dynamics route (labelled BA2 second route, not used)', 'skeptic post-comparison', 'BB1 discharge'],
        'proposed_forward_verdict': verdict_line,
    }
    packet.update(FLAGS)
    packet.update(GATE)

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
        validate_gate(pk['gate_fields'])
        require(sorted(inv) == sorted(set(forward_list)) and NS_REL in inv and BB1_REL in inv, 'premise snapshot inventory incomplete')
        require(rat(pk['headline']['C_prime']['value']) == Cprime(V['C_h'], V['c_h']), 'C_prime differs from recomputation')
        require(rat(pk['headline']['c_site_prime']['value']) == cprime(V['C_h'], V['c_h']), 'c_site_prime differs from recomputation')
        require(rat(pk['headline']['C_dyn']['value']) == 2 * K_F1 + K_cmp / 4, 'C_dyn differs from the BA2 gate values')
        require(pk['conditional_on_bb1_targets'] is True and pk['headline']['C_prime']['hypothesis_source'] == HYP_SOURCE, 'condition dropped')
        require(pk['assembly'] == ASSEMBLY, 'assembly changed')
        require(sorted(pk['families']) == ['F1', 'F2'], 'families changed')
        require(pk['mandatory_sentence'] == template, 'mandatory sentence changed')
        require(pk['proposed_forward_verdict'].startswith(verdict) and COND in pk['proposed_forward_verdict'], 'verdict changed')
        require([h['id'] for h in pk['hypotheses_used']] == ['H1', 'H2', 'H3', 'H4', 'H1s-H3s'], 'hypotheses list changed')
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
            if ch['id'] == 'conditional_on_bb1_targets':
                ch['passed'] = False

    def t_snapshot(pk, inv):
        inv.pop(BB1_REL)

    def t_Cp(pk, inv):
        pk['headline']['C_prime']['value'] = s(V['C_h'])

    def t_Cdyn(pk, inv):
        pk['headline']['C_dyn']['value'] = s(K_F1)

    def t_cond(pk, inv):
        pk['conditional_on_bb1_targets'] = False

    def t_gate(pk, inv):
        pk['gate_fields']['uniqueness_of_ground_state_claimed'] = True

    def t_hyp(pk, inv):
        pk['hypotheses_used'] = pk['hypotheses_used'][:3]

    def t_assembly(pk, inv):
        pk['assembly'] = 'union_comparison'
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_snapshot), 'bb1_contract_snapshot_removed_hash_rebound')
          and rejected(tamper(t_Cp), 'C_prime_replaced_by_C_h_hash_rebound')
          and rejected(tamper(t_Cdyn), 'C_dyn_replaced_hash_rebound')
          and rejected(tamper(t_cond), 'condition_dropped_hash_rebound')
          and rejected(tamper(t_gate), 'uniqueness_field_hash_rebound')
          and rejected(tamper(t_hyp), 'hypothesis_H4_dropped_hash_rebound')
          and rejected(tamper(t_assembly), 'assembly_relabelled_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    positive_only = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch.get('rejected_mutations')]
    require(not positive_only, 'contract controls without a damaging mutation: ' + ','.join(positive_only))
    require(not PENDING, 'rejected mutations not attached to a check')
    packet['checks'] = CHECKS
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['controls_with_damaging_mutations'] = sum(1 for ch in CHECKS if ch['id'] in V['controls'] and ch.get('rejected_mutations'))
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
    ap = argparse.ArgumentParser(description='BB2 forward exact checker')
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
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8')
    sources = {}
    for p in sorted(BASE.rglob('*')):
        rel = p.relative_to(BASE)
        if p.is_file() and (rel.parts[0] == 'inputs' or p.name in ('check.py', 'report.md')) and rel.parts[0] != 'output':
            sources[rel.as_posix()] = sha(p)
    manifest = {'loop': 'BB2', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'bb1_contract_sha256': BB1_SHA256,
                'check_py_sha256': sources['check.py'], 'sources': sources, 'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    h = result['headline']
    print(json.dumps({'loop': 'BB2', 'direction': 'forward', 'checks': len(result['checks']),
                      'C_prime_preview': h['C_prime']['preview'], 'c_site_prime_preview': h['c_site_prime']['preview'],
                      'C_dyn_preview': h['C_dyn']['preview'], 'rejected_mutations': result['rejected_mutation_total'],
                      'controls_with_damaging_mutations': result['controls_with_damaging_mutations']}, sort_keys=True))


if __name__ == '__main__':
    main()
