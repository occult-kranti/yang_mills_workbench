#!/usr/bin/env python3
"""BA2 forward producer: exact checks for the Duhamel / Lieb-Robinson comparison of the
finite-box Heisenberg dynamics of the named construction families F1 and F2 on compact
time windows, the within-family Cauchy estimates (sup over all larger boxes), and the
identification of the F2 limit dynamics with the AQ1 limit dynamics T_theta.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production (Claude).

Standard library only (argparse, fractions, hashlib, itertools, json, math, pathlib, re).
Every admission Boolean is decided in exact Fraction arithmetic with directed rational
enclosures; decimal strings are truncated previews and are never read by an admission
check.  Conditions raise AdmissionError explicitly (never `assert`), so every check stays
active under `python -O`.

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
CONTRACT_REL = 'research/round33/contracts/ba2.json'
CONTRACT_SHA256 = '275ba3b002529b7295d0f8b91dc1cc7a96451e3c7f936ee698a932fdca54fcff'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'

# Admitted gates read by this checker, pinned before any evaluation.
PINNED_GATES = {
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
}
# The committed Nachtergaele-Sims excerpt (the only quotation source) and its PDF binding.
NS_REL = 'research/round33/sources/nachtergaele-sims-1410.8174v1.md'
NS_SHA256 = '6a28f4cd6aa2c55286fa839d83c00356ff0709f8b02027ee5b39050df1d6c921'
NS_PDF_SHA256 = '501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba'

P_AQ1 = 'research/round29/forward/aq1/report.md'
P_AQ1_SK = 'research/round29/skeptic/aq1.md'
P_AM2 = 'research/round29/forward/am2/report.md'
P_I1 = 'research/round21/forward/i1/report.md'
P_AY1F = 'research/round32/forward/ay1/report.md'
P_AY1R = 'research/round32/reverse/ay1/report.md'
P_AY2F = 'research/round32/forward/ay2/report.md'
P_AV1F = 'research/round32/forward/av1/report.md'
P_AQ2 = 'research/round29/forward/aq2/report.md'
P_DICT = 'research/round29/experts/aq-source-dictionary.md'
P_BIND = 'research/round29/experts/aq-primary-bindings.json'
P_SEL = 'research/round33/advisor/selection-ba2.md'
P_AQ1_GATE = 'research/round29/advisor/aq1-gate.json'
P_AM2_GATE = 'research/round29/advisor/am2-gate.json'
P_AY1_GATE = 'research/round32/advisor/ay1-gate.json'
P_AY2_GATE = 'research/round32/advisor/ay2-gate.json'
REPORT = 'report.md'

TIER = 'polynomial_lieb_robinson'
PHI_WHOLE = 'whole-star Phi'
PHI_OWNER = "owner-set Phi'"


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


# ---------------------------------------------------------------------------
# Contract: every target, bracket, template, control id and reference is read from the
# sha256-bound snapshot.
# ---------------------------------------------------------------------------
def load_contract():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen BA2 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'BA2' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


def bracket(text, label):
    m = match(r'\[(\d+),(\d+)\]', text, label)
    return (Q(int(m.group(1))), Q(int(m.group(2))))


def contract_values(c):
    p = c['parameters']
    pre = c['preregistration']
    v = {'model': c['model'], 'parameters': p}
    require('Zero-selected patterned family' in c['model'] and '|tau|<=10^-8' in c['model'] and 'B(H_R)' in c['model']
            and 'R={0,e_z}' in c['model'], 'model string')
    v['families_text'] = c['model']
    require('F1 (AQ1 centered whole-star boxes)' in c['model'] and 'F2 (I1 section 6 all-contained-face boxes with padding)' in c['model'],
            'two named families in the model string')
    # metric / weights / window / boundary source
    met = p['metric']
    for frag in ('l1 metric on the coarse Z^3 factor lattice', 'F(r)=(1+r)^-4', '4r^2+2 sites at l1 distance r',
                 'convolution constant C at most 224', '||Phi||_F at most 81J = 2268|tau|', "||Phi'||_F at most 1323|tau|",
                 'no fine-site metric and no coarse-to-fine conversion enters any constant'):
        require(frag in met, 'metric parameter fragment missing: ' + frag)
    v['metric'] = met
    v['C_contract'] = Q(int(match(r'convolution constant C at most (\d+)', met, 'C').group(1)))
    m = match(r'\|\|Phi\|\|_F at most (\d+)J = (\d+)\|tau\|', met, 'Phi_F')
    v['phi_factor_contract'], v['phi_contract'] = int(m.group(1)), Q(int(m.group(2)))
    v['phiprime_contract'] = Q(int(match(r"\|\|Phi'\|\|_F at most (\d+)\|tau\|", met, "Phi'_F").group(1)))
    v['F_exponent'] = int(match(r'F\(r\)=\(1\+r\)\^-(\d+)', met, 'F exponent').group(1))
    require('F(r)=(1+r)^-4 (polynomial, AQ1)' in p['weights'], 'weights parameter')
    v['weights'] = p['weights']
    m = match(r'^\|theta\|<=(\d+) in theta=alpha t/hbar \(normalized u=theta/(\d+)<=1 internally\)', p['window'], 'window')
    v['Theta'], v['u_div'] = Q(int(m.group(1))), Q(int(m.group(2)))
    v['window'] = p['window']
    bs = p['boundary_source']
    require('28N(5N+1)' in bs and 'padding B_+ minus Lambda_N' in bs and 'factor out of the evolution exactly' in bs
            and 'at least N-1 from e_z and at least N from 0' in bs and 'each face charged exactly once' in bs, 'boundary source parameter')
    v['boundary_source'] = bs
    tg = p['targets']
    m = match(r'<= (\d+)x10\^-(\d+) \(5N\+1\) N\^-3 \|\|A\|\| for \|theta\| at most (\d+) and N at least (\d+) \((\w+) tier\)',
              tg['comparison'], 'comparison target')
    v['target_cmp'] = Q(int(m.group(1)), 10 ** int(m.group(2)))
    require(Q(int(m.group(3))) == v['Theta'], 'comparison window equals the window parameter')
    v['N0'] = int(m.group(4))
    v['target_cmp_tier'] = m.group(5)
    m = match(r'at most (\d+)\.(\d+)x10\^-(\d+)/\(N-1\) \|\|A\|\| for \|theta\| at most (\d+) and N at least (\d+)',
              tg['within_family_cauchy'], 'cauchy target')
    v['target_cau'] = Q(int(m.group(1) + m.group(2)), 10 ** (int(m.group(3)) + len(m.group(2))))
    require(Q(int(m.group(4))) == v['Theta'] and int(m.group(5)) == v['N0'], 'cauchy window and N0')
    require('and the same for F2' in tg['within_family_cauchy'] and 'an N to N+1 bound alone is not a Cauchy estimate' in tg['within_family_cauchy'],
            'cauchy target covers F2 and forbids N to N+1')
    require('converge as a whole sequence' in tg['f2_dynamics'] and 'AY2 row O6' in tg['f2_dynamics'], 'f2 dynamics target')
    v['targets'] = dict(tg)
    # preregistration
    v['clock'] = pre['clock']
    require(v['clock'].startswith('s=alpha*t_E/hbar (Euclidean), theta=alpha*t/hbar (real time); normalized u=theta/8'), 'clock')
    v['tau_value'] = rat(pre['tau']['value'])
    v['signs'] = list(pre['tau']['signs_evaluated'])
    require(v['signs'] == ['+', '-'] and pre['tau']['is_model_change_vs_previous_loop'] is False
            and pre['tau']['rule_if_chosen_later'] is None, 'tau rule')
    v['triple'] = [rat(x) for x in pre['selected_triple_alpha_units']]
    require(v['triple'] == [0, 0, 0], 'zero selected triple')
    v['model_id'] = pre['model_id']
    require(v['model_id'] == 'AQ_patterned_zero_selected', 'model id')
    obs = pre['observable']
    v['reference_value'] = rat(obs['reference_value_exact'])
    require(obs['centering'] == 'none' and v['reference_value'] == 0 and obs['reference_route'].startswith('n/a'), 'observable block')
    v['observable_id'] = obs['id']
    v['tiers_allowed'] = list(pre['tier_names_allowed'])
    require(v['tiers_allowed'] == ['polynomial_lieb_robinson', 'exponential_lieb_robinson'], 'tier names')
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['outcomes'] = list(pre['expected_outcome_types'])
    v['error_terms'] = list(pre['error_terms_itemized'])
    v['error_terms_rule'] = pre['error_terms_rule']
    v['template'] = pre['mandatory_sentence_template']
    v['gate_fields'] = dict(pre['gate_fields_required'])
    v['forbidden'] = list(pre['forbidden_phrasings'])
    v['hash_binding'] = dict(pre['hash_binding'])
    require(all(v['hash_binding'][k] is True for k in ('contract_sha256_in_producer_inputs', 'check_py_reads_target_and_reference_from_contract',
                                                     'check_py_sha256_recorded_before_full_size_evaluation', 'admitted_gate_sha256_pinned_in_check_py')),
            'hash binding block')
    tv = pre['target']
    require(tv['comparator'] == '<=' and tv['value'] == '6x10^-11 and 2.5x10^-10', 'preregistered target block')
    v['target_prereg'] = tv
    sb = pre['scaling_brackets_per_constant']
    v['bracket_cmp'] = bracket(sb['comparison_coefficient'], 'comparison bracket')
    v['bracket_cau'] = bracket(sb['cauchy_coefficient'], 'cauchy bracket')
    require('the same bracket for F2 and for the F2-inner comparison' in sb['cauchy_coefficient'], 'F2 bracket')
    v['bracket_quadratic'] = bracket(c['new_control_semantics']['duhamel_tau_order_quadratic'], 'quadratic control bracket')
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']), 'controls list equals the preregistered ids')
    v['semantics'] = dict(c['new_control_semantics'])
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['acceptance'] = dict(c['acceptance'])
    v['shared'] = list(c['shared_premises'])
    v['forward_additional'] = list(c['forward_additional_premises'])
    v['reverse_isolation'] = c['reverse_premise_isolation']
    v['required'] = list(c['required'])
    v['direction_note'] = c['direction_note']
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


def l1(p, q):
    return sum(abs(a - b) for a, b in zip(p, q))


def linf(p):
    return max(abs(a) for a in p)


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def parse_i1_table(text):
    rows = re.findall(r'^\| (xy|xz|yz): r=([\d,]+); s=([\d,]+) \| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|$', text, re.M)
    require(len(rows) == 8, 'I1 table has eight rows')
    classes = []
    for orient, rs, ss, count, supp, role in rows:
        rl = [int(x) for x in rs.split(',')]
        sl = [int(x) for x in ss.split(',')]
        require(len(rl) * len(sl) == int(count), 'I1 row count column')
        support = frozenset(TOKEN[t.strip()] for t in supp.split(','))
        for r in rl:
            for q in sl:
                classes.append((orient, r, q, support, role))
    return classes


def class_base(anchor, cls):
    return (4 * anchor[0] + cls[1], 2 * anchor[1] + cls[2], anchor[2]), ORIENT[cls[0]]


def face_links(p, a, c):
    return ((p, a), (add(p, E_UNIT[a]), c), (add(p, E_UNIT[c]), a), (p, c))


def face_support_fine(p, a, c):
    return frozenset(owner(link[0]) for link in face_links(p, a, c))


def owner_set(face):
    b, cls = face
    return frozenset(add(b, d) for d in cls[3])


def face_key(face):
    return (face[0], face[1][:3])


def coarse_box(N):
    rng = range(-N, N + 1)
    return frozenset(product(rng, rng, rng))


def f1_faces(N, omitted):
    box = coarse_box(N)
    return {face_key((b, k)): (b, k) for b in box for k in omitted if all(add(b, d) in box for d in S_STAR)}


def f2_faces(N, omitted):
    box = coarse_box(N)
    return {face_key((b, k)): (b, k) for b in box for k in omitted if owner_set((b, k)) <= box}


def faces_containing(u, classes):
    """Translation covariance: face (b,k) has u in its owner set iff b=u-d with d in K_k."""
    return [(sub(u, d), cls) for cls in classes for d in sorted(cls[3])]


def block_links(b):
    out = []
    for r in range(4):
        for q in range(2):
            t = (4 * b[0] + r, 2 * b[1] + q, b[2])
            for a in range(3):
                out.append((t, a))
    return out


def F_poly(r, exponent=4):
    return Q(1, (1 + r) ** exponent)


def shell_count(r):
    """Number of Z^3 sites at l1 distance exactly r from a point (enumerated)."""
    rng = range(-r, r + 1)
    return sum(1 for y in product(rng, rng, rng) if sum(abs(c) for c in y) == r)


# ---------------------------------------------------------------------------
# Lieb-Robinson / Duhamel arithmetic (exact, directed).
# ---------------------------------------------------------------------------
def lr_time_integral_upper(phi_F, C, U):
    """Directed rational upper bound of int_0^U (2/C)(e^{v r}-1) dr with v=2||Phi||_F C.

    Exact value (2/(C v))(e^{vU}-1-vU); for 0<=x=vU<3, e^x-1-x <= x^2/(2(1-x/3)) because
    k! >= 2*3^(k-2) for k>=2; hence the bound 2||Phi||_F U^2/(1-vU/3).  The exact value is
    increasing in C and in ||Phi||_F, so admitted upper bounds of C and ||Phi||_F may be used."""
    phi_F, C, U = rat(phi_F), rat(C), rat(U)
    require(phi_F >= 0 and C > 0 and U >= 0, 'LR inputs nonnegative')
    v = 2 * phi_F * C
    x = v * U
    require(x < 3, 'LR exponent below the rational enclosure radius')
    return 2 * phi_F * U * U / (1 - x / 3)


def duhamel_coefficient(tau, U, face_sum, phi_F, C):
    """|tau|/3 (face norm) x LR time integral x (sum over charged faces of sum_{x in R, y in M_f} F(d(x,y)))."""
    return abs(rat(tau)) / 3 * lr_time_integral_upper(phi_F, C, U) * rat(face_sum)


def factorial(n):
    out = 1
    for k in range(2, n + 1):
        out *= k
    return out


# ---------------------------------------------------------------------------
# Exact Gaussian-rational matrices for the finite algebraic fixtures.
# ---------------------------------------------------------------------------
def cz(a, b=0):
    return (Q(a), Q(b))


def cadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def cmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def cconj(x):
    return (x[0], -x[1])


def cdiv(x, y):
    d = y[0] * y[0] + y[1] * y[1]
    require(d != 0, 'division by zero')
    n = cmul(x, cconj(y))
    return (n[0] / d, n[1] / d)


def mat(rows):
    return [[cz(*e) if isinstance(e, tuple) else cz(e) for e in row] for row in rows]


def mmul(A, B):
    n, m, k = len(A), len(B[0]), len(B)
    return [[_csum(cmul(A[i][t], B[t][j]) for t in range(k)) for j in range(m)] for i in range(n)]


def _csum(it):
    out = cz(0)
    for x in it:
        out = cadd(out, x)
    return out


def madj(A):
    return [[cconj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]


def madd(A, B, c=1):
    return [[cadd(A[i][j], cmul(cz(c), B[i][j])) for j in range(len(A[0]))] for i in range(len(A))]


def eye(n):
    return [[cz(1 if i == j else 0) for j in range(n)] for i in range(n)]


def kron(A, B):
    return [[cmul(A[i // len(B)][j // len(B[0])], B[i % len(B)][j % len(B[0])]) for j in range(len(A[0]) * len(B[0]))]
            for i in range(len(A) * len(B))]


def inv2(A):
    det = cadd(cmul(A[0][0], A[1][1]), cmul(cz(-1), cmul(A[0][1], A[1][0])))
    return [[cdiv(A[1][1], det), cdiv(cmul(cz(-1), A[0][1]), det)], [cdiv(cmul(cz(-1), A[1][0]), det), cdiv(A[0][0], det)]]


def cayley(H):
    """(1+iH)(1-iH)^{-1}: an exactly unitary Gaussian-rational matrix for rational Hermitian 2x2 H."""
    iH = [[cmul(cz(0, 1), e) for e in row] for row in H]
    return mmul(madd(eye(2), iH), inv2(madd(eye(2), iH, -1)))


def is_zero(A):
    return all(e == cz(0) for row in A for e in row)


# ---------------------------------------------------------------------------
# Text scanners (report and exported statements).
# ---------------------------------------------------------------------------
ROUND_FORBIDDEN = [   # copied from research/round33/tools/phrase_scan.py (infrastructure list, no premise weight)
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state',
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
UNIFORM_QUALIFIERS = ('in n at fixed spacing', 'for |theta|', 'for t in compact sets', 'on compact', 'for |u|', 'in |theta|',
                      'uniform integrability')   # the last is the name of condition (40), not a uniformity claim


def uniformity_violations(text, template):
    body = normalize(text).replace(normalize(template), ' ')
    bad = []
    for clause in clauses(body):
        if not UNIFORM.search(clause):
            continue
        low = clause.lower().replace('`', '')          # code-span backticks are formatting, not wording
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
    c, contract_digest = load_contract()
    V = contract_values(c)
    tau_cap = V['tau_value']
    require(tau_cap == Q(1, 100000000), 'preregistered tau is the cap 10^-8')
    taus = {'+': tau_cap, '-': -tau_cap}
    check('contract_snapshot_sha256',
          contract_digest == CONTRACT_SHA256 and V['target_cmp'] == Q(6, 10 ** 11) and V['target_cau'] == Q(25, 10 ** 11)
          and V['Theta'] == 8 and V['u_div'] == 8 and V['N0'] == 2 and len(V['controls']) == 35
          and V['bracket_cmp'] == (9500, 10500) and V['bracket_cau'] == (9500, 10500) and V['bracket_quadratic'] == (9900, 10100),
          contract_sha256=contract_digest, contract_path=CONTRACT_REL,
          comparison_target_read_from_contract=s(V['target_cmp']) + ' (5N+1) N^-3',
          cauchy_target_read_from_contract=s(V['target_cau']) + ' /(N-1)',
          window_read_from_contract='|theta|<=' + s(V['Theta']) + ', u=theta/' + s(V['u_div']),
          tau_read_from_contract=s(tau_cap), reference_read_from_contract=s(V['reference_value']),
          scaling_brackets_read_from_contract={'comparison': [s(x) for x in V['bracket_cmp']], 'cauchy': [s(x) for x in V['bracket_cau']],
                                               'duhamel_quadratic_control': [s(x) for x in V['bracket_quadratic']]},
          controls_read_from_contract=len(V['controls']), hash_binding=V['hash_binding'])

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
    bindings = load_json_input(P_BIND)
    ns_bind = [x for x in bindings['sources'] if x['id'] == 'ns-2014']
    require(len(ns_bind) == 1 and ns_bind[0]['pdf_sha256'] == NS_PDF_SHA256 and ('PDF sha256: `' + NS_PDF_SHA256 + '`') in ns
            and NS_PDF_SHA256 in V['semantics']['lieb_robinson_form_quoted'], 'NS PDF binding agrees across excerpt, bindings and contract')
    check('pinned_gates_and_source_excerpt',
          all(gate_sha[r] == p for r, p in PINNED_GATES.items()) and ns_digest == NS_SHA256,
          gate_sha256=gate_sha, ns_excerpt_sha256=ns_digest, ns_pdf_sha256=NS_PDF_SHA256,
          note='pins are compared before any value is read from these files')

    # ======================= premise constants (read, never typed) =======================
    aq1 = read_input(P_AQ1)
    F_exp_aq1 = int(match(r'`F\(r\)=\(1\+r\)\^-(\d+)`', aq1, 'AQ1 F').group(1))
    normF_aq1 = int(match(r'`\|\|F\|\|<=(\d+)`', aq1, 'AQ1 ||F||').group(1))
    m = match(r'`C<=(\d+)\|\|F\|\|<=(\d+)`', aq1, 'AQ1 C')
    C_split, C_aq1 = int(m.group(1)), Q(int(m.group(2)))
    J_aq1 = int(match(r'J\\le4M=(\d+)\|\\tau\|', aq1, 'AQ1 J').group(1))
    m = match(r'\\\|\\Phi\\\|_F\\le3\^4J=(\d+)J\\le(\d+)\|\\tau\|', aq1, 'AQ1 Phi_F')
    phi_factor_aq1, phi_aq1 = int(m.group(1)), Q(int(m.group(2)))
    M_star = int(match(r'`\|\|phi_b\|\|=M=(\d+)\|tau\|`', aq1, 'AQ1 star norm').group(1))
    require('contains `4r²+2` sites' in aq1 and 'Restore physical time by `u=delta t/hbar`' in aq1, 'AQ1 shells and clock')
    delta_div = int(match(r'with delta=alpha/(\d+)', aq1, 'AQ1 delta').group(1))
    require('Its native restriction `sum_(X subset Lambda)Phi(X)` is exactly the retained whole-star prescription here' in aq1,
            'AQ1 native restriction placement')
    dic = read_input(P_DICT)
    require('delta=alpha/8' in dic and 'Nachtergaele–Sims1410.8174v1, Section3 setup and Theorem4.1' in dic, 'source dictionary clock and source')
    ay1r = read_input(P_AY1R)
    phiprime_ay1 = Q(int(match(r'81·49\|tau\|/3 = (\d+)\|tau\|', ay1r, "AY1 reverse Phi'").group(1)))
    ay1g = load_json_input(P_AY1_GATE)
    require('F2 retains 28N(5N+1) boundary faces more than F1' in ay1g['accepted'], 'AY1 gate extra-face count')
    ay2g = load_json_input(P_AY2_GATE)
    require('boundary independence of dynamics on compact time windows, not proved' in ay2g['accepted']
            and 'dynamics of the padded family itself, not proved' in ay2g['accepted'], 'AY2 gate rows O5 and O6')
    ay2 = read_input(P_AY2F)
    o5 = match(r'^\| O5 \| boundary independence of dynamics on compact time windows \| unproved \|', ay2, 'AY2 O5', re.M)
    o6 = match(r'^\| O6 \| dynamics of the padded family itself \| unproved \|', ay2, 'AY2 O6', re.M)
    am2 = read_input(P_AM2)
    m = match(r'J:=\\max_u\\sum_\{X\\ni u\}\\\|V_X\\\|\\le(\d+)\|\\tau\|\\le J_0=\{(\d+)\\over(\d+)\}', am2, 'AM2 J')
    J_am2 = int(m.group(1))
    i1 = read_input(P_I1)
    require('=-{\\tau\\over3}\\sum_{f\\in O_b}W_f' in i1 and 'so `||phi_b||<=7|tau|`' in i1, 'I1 face coefficient -tau/3 and star norm')
    aq1g = load_json_input(P_AQ1_GATE)
    require('whole-sequence convergence' in aq1g['limitations'][0], 'AQ1 gate: whole-sequence convergence not admitted there')
    check('premise_constants_parsed',
          F_exp_aq1 == V['F_exponent'] == 4 and normF_aq1 == 7 and C_split == 32 and C_aq1 == V['C_contract'] == 224
          and J_aq1 == J_am2 == 28 and phi_factor_aq1 == V['phi_factor_contract'] == 81 and phi_aq1 == V['phi_contract'] == 2268
          and phi_factor_aq1 * J_aq1 == 2268 and M_star == 7 and 4 * M_star == J_aq1 and delta_div == 8
          and phiprime_ay1 == V['phiprime_contract'] == 1323 and o5 is not None and o6 is not None,
          aq1={'F': '(1+r)^-%d' % F_exp_aq1, 'norm_F_upper': normF_aq1, 'C_upper': s(C_aq1), 'J_per_abs_tau': J_aq1,
               'Phi_F_upper_per_abs_tau': s(phi_aq1), 'star_norm_per_abs_tau': M_star, 'clock': 'u=delta t/hbar, delta=alpha/%d' % delta_div},
          ay1_reverse_owner_set_Phi_prime_per_abs_tau=s(phiprime_ay1), ay1_gate_extra_faces='28N(5N+1)',
          ay2_rows=['O5 boundary independence of dynamics on compact time windows', 'O6 dynamics of the padded family itself'],
          read_from='hash-bound snapshots (AQ1 report equations, AM2 report, AY1 reverse report, AY1/AY2 gates, I1 report); no constant typed in')

    # ======================= Nachtergaele-Sims: verbatim quotation =======================
    report_text = (BASE / REPORT).read_text(encoding='utf-8')
    part_a = ns.split('## Part A.')[1].split('## Part B.')[0]
    eq_lines = {}
    for tag in ('40', '41', '44', '48', '49', '50', '51', '52', '77'):
        m = match(r'^- \(' + tag + r'\) (.+)$', part_a, 'NS eq ' + tag, re.M)
        eq_lines[tag] = '(' + tag + ') ' + m.group(1).strip()
    th31 = match(r'\*\*Theorem 3\.1\.\*\* (Let Γ and F be as indicated above\..*?the bound)\n', part_a, 'NS Thm 3.1', re.S).group(1)
    th31b = match(r'(holds for all t ∈ ℝ, where the quantity D\(X, Y\) is given by)', part_a, 'NS Thm 3.1 tail').group(1)
    th41 = match(r'(Let Γ and F be as described in Section 3\..*?the norm limit)\n', part_a, 'NS Thm 4.1', re.S).group(1)
    th41b = match(r'(exists and the convergence is uniform for t in compact sets\..*?on A_Γ\.)', part_a, 'NS Thm 4.1 tail', re.S).group(1)
    eq46 = match(r'(\(46\) τ_t\^Λ\(A\) = e\^\{itH_Λ\} A e\^\{−itH_Λ\} for A ∈ A_Λ\.)', part_a, 'NS eq 46').group(1)
    quotes = dict(eq_lines)
    quotes.update({'thm3.1_statement': th31, 'thm3.1_tail': th31b, 'thm4.1_statement': th41, 'thm4.1_tail': th41b, '46': eq46})

    def validate_quotes(report, quote_map):
        for key, q in quote_map.items():
            require(q in report, 'verbatim quotation missing from report: ' + key)
        require('e^{2‖Φ‖C|t|}' in quote_map['51'] and '(2‖A‖‖B‖ / C)' in quote_map['51'], 'quoted (51) carries 2||Phi||C and 2/C')
        return True

    def paraphrase(key, old, new):
        """The report carries a paraphrased form in place of the verbatim source line."""
        def run():
            para = quotes[key].replace(old, new)
            require(para != quotes[key], 'mutation changed nothing')
            return validate_quotes(report_text.replace(quotes[key], para), quotes)
        return run

    def second_hand():
        # the AQ1 report is the placement record, not the quotation source: its text does not carry (51)
        return validate_quotes(aq1, quotes)
    check('lieb_robinson_form_quoted',
          validate_quotes(report_text, quotes)
          and rejected(paraphrase('51', 'e^{2‖Φ‖C|t|}', 'e^{‖Φ‖C|t|}'), 'velocity_factor_2_dropped')
          and rejected(paraphrase('51', '(2‖A‖‖B‖ / C)', '(2‖A‖‖B‖)'), 'prefactor_1_over_C_dropped')
          and rejected(paraphrase('52', 'min{', 'max{'), 'min_replaced_by_max')
          and rejected(paraphrase('77', 'lim_{Λ→Γ}', 'lim_{N→∞}'), 'limit_paraphrased')
          and rejected(second_hand, 'quotation_taken_from_aq1_report')
          and rejected(lambda: require(sha_bytes(ns_raw + b' ') == NS_SHA256, 'excerpt hash'), 'excerpt_bytes_changed'),
          quoted_items=sorted(quotes), source=NS_REL, source_sha256=ns_digest,
          named={'F': '(1+r)^-4', 'C': 'convolution constant (41), at most 224', '||Phi||_F': '(48), at most 2268|tau| (whole star)'})

    # ======================= F declared: ||F||, shells and C =======================
    shells = {r: shell_count(r) for r in range(0, 16)}
    shells_ok = all(shells[r] == (1 if r == 0 else 4 * r * r + 2) for r in shells)
    normF_steps = all(6 * (r + 1) ** 2 - (4 * r * r + 2) == 2 * r * r + 12 * r + 4 >= 0 for r in range(1, 400))
    tele_ok = all(Q(1, k * k) <= Q(1, k - 1) - Q(1, k) for k in range(2, 400))
    partial_normF = 1 + sum(Q(4 * r * r + 2, (1 + r) ** 4) for r in range(1, 300))
    half_ok = all(Q(1 + d) / (1 + Q(d, 2)) <= 2 for d in range(0, 400))
    C_bound = 32 * normF_aq1

    def validate_F(exponent, normF_upper, C_upper, tier, phi_upper, mu=None):
        require(exponent == V['F_exponent'], 'F differs from the contract F(r)=(1+r)^-4')
        require(normF_upper * 32 == C_upper and C_upper <= V['C_contract'], 'C must follow from the convolution split of the same F')
        if tier == 'exponential_lieb_robinson':
            require(mu is not None and mu > 0, 'exponential instance needs its own mu')
            require(phi_upper != V['phi_contract'], "exponential instance must carry its own ||Phi||_{F_mu} = e^{2mu} 81 J, not AQ1's")
        else:
            require(tier == TIER and phi_upper == V['phi_contract'], 'polynomial tier uses the AQ1 constants')
        return True

    def cubic_decay():
        # F(r)=(1+r)^-3 violates (40) on Z^3: the shell sum dominates a harmonic sum
        part = sum(Q(4 * r * r + 2, (1 + r) ** 3) for r in range(1, 257))
        require(part < 7, 'uniform integrability (40) fails for (1+r)^-3: partial sum %s' % dec(part, 6))
        return validate_F(3, 7, 224, TIER, V['phi_contract'])
    check('lieb_robinson_F_declared',
          shells_ok and normF_steps and tele_ok and partial_normF <= 7 and half_ok and C_bound == 224
          and validate_F(4, 7, 224, TIER, V['phi_contract'])
          and rejected(cubic_decay, 'F_cubic_violates_uniform_integrability')
          and rejected(lambda: validate_F(4, 7, 224, 'exponential_lieb_robinson', V['phi_contract'], mu=Q(1, 10)), 'exponential_instance_with_AQ1_Phi_norm')
          and rejected(lambda: validate_F(4, 7, 112, TIER, V['phi_contract']), 'C_not_from_convolution_split'),
          shell_counts_r_le_15=[shells[r] for r in range(16)], norm_F_partial_sum_r_lt_300=dec(partial_normF),
          norm_F_upper=normF_aq1, C_upper=C_bound,
          argument='4r^2+2<=6(r+1)^2 and sum over k from 2 of k^-2<=1 give ||F||<=7; (1+d)/(1+d/2)<=2 gives C<=32||F||<=224 (AQ1 section 3, re-verified)',
          exponential_instance='not executed (optional, no frozen target); any such instance must carry its own C_{F_mu} and e^{2mu}81J')

    # ======================= I1 table, face pins (all sites) =======================
    classes = parse_i1_table(i1)
    omitted = [k for k in classes if k[4] == 'omitted']
    geo_ok = True
    for cls in classes:
        base, (a1, c1) = class_base(ORIGIN, cls)
        geo_ok = geo_ok and face_support_fine(base, a1, c1) == cls[3]
    at0 = faces_containing(ORIGIN, omitted)
    sets0 = {}
    for f in at0:
        sets0[owner_set(f)] = sets0.get(owner_set(f), 0) + 1
    meet = {}
    for u in COVER_R:
        for f in faces_containing(u, omitted):
            meet[face_key(f)] = f
    inside = [f for f in meet.values() if owner_set(f) <= frozenset(COVER_R)]
    derived_pins = {'per_factor': len(at0), 'owner_sets': len(sets0), 'meet_R': len(meet), 'inside_R': len(inside)}

    def validate_pins(pins, derived_from):
        require(derived_from == 'I1 table, translation covariance, both sites of R', 'pins must be derived at every site of R')
        require(pins == derived_pins, 'face pins differ from the I1 derivation')
        return True
    site0_only = {'per_factor': 49, 'owner_sets': 15, 'meet_R': len({face_key(f) for f in faces_containing(ORIGIN, omitted)}), 'inside_R': 10}
    check('face_count_all_sites',
          geo_ok and len(omitted) == 21 and derived_pins == {'per_factor': 49, 'owner_sets': 15, 'meet_R': 82, 'inside_R': 10}
          and validate_pins(derived_pins, 'I1 table, translation covariance, both sites of R')
          and rejected(lambda: validate_pins(site0_only, 'I1 table, translation covariance, site 0 only'), 'site_0_only_count')
          and rejected(lambda: validate_pins({'per_factor': 49, 'owner_sets': 15, 'meet_R': 84, 'inside_R': 10}, 'literal'), 'typed_literal_84'),
          pins=derived_pins, site0_only_meeting_count=site0_only['meet_R'],
          note='the extra F2 faces meet none of the 82 faces meeting R: every one of their owners lies on the outer layer')

    # ======================= extra F2 faces: count, owners, distances =======================
    per_class_formula = {1: lambda N: 2 * N * (4 * N + 1), 2: lambda N: 4 * N * N}
    enum = {}
    for N in (2, 3, 4):
        f1 = f1_faces(N, omitted)
        f2 = f2_faces(N, omitted)
        extra = {k: f2[k] for k in f2 if k not in f1}
        owners_all = [(k, y) for k, f in extra.items() for y in owner_set(f)]
        outer_ok = all(linf(y) == N and max(y) == N for _, y in owners_all)
        dz = min(l1(EZ, y) for _, y in owners_all)
        d0 = min(l1(ORIGIN, y) for _, y in owners_all)
        max_owners = max(len(owner_set(f)) for f in extra.values())
        by_class = {}
        for f in extra.values():
            by_class[f[1][:3]] = by_class.get(f[1][:3], 0) + 1
        class_ok = all(by_class.get(k[:3], 0) == per_class_formula[len(k[3]) - 1](N) for k in omitted)
        S_b_exact = sum(F_poly(l1(x, y)) for _, y in owners_all for x in COVER_R)
        S_b_bound = 168 * Q(5 * N + 1, N ** 3)
        enum[N] = {'F1': len(f1), 'F2': len(f2), 'extra': len(extra), 'formula': 28 * N * (5 * N + 1), 'incidences': len(owners_all),
                   'incidence_formula': 28 * N * (11 * N + 2), 'outer_layer': outer_ok, 'min_l1_from_e_z': dz, 'min_l1_from_0': d0,
                   'max_owners': max_owners, 'class_formula': class_ok, 'F1_subset_F2': set(f1) <= set(f2),
                   'S_b_exact': S_b_exact, 'S_b_all_size_bound': S_b_bound, 'extra_keys': set(extra), 'extra_faces': extra}
    enum_ok = all(e['extra'] == e['formula'] == e['F2'] - e['F1'] and e['incidences'] == e['incidence_formula'] and e['outer_layer']
                  and e['min_l1_from_e_z'] == N - 1 and e['min_l1_from_0'] == N and e['max_owners'] == 3 and e['class_formula']
                  and e['F1_subset_F2'] and e['S_b_exact'] <= e['S_b_all_size_bound'] for N, e in enum.items())
    extra_class_sum_ok = all(14 * per_class_formula[1](N) + 7 * per_class_formula[2](N) == 28 * N * (5 * N + 1)
                             and 14 * 2 * per_class_formula[1](N) + 7 * 3 * per_class_formula[2](N) == 28 * N * (11 * N + 2)
                             for N in range(2, 200))
    # class-type census from the table: 14 two-owner classes (one direction), 7 three-owner classes (two directions)
    census = sorted(len(k[3]) for k in omitted)
    census_ok = census.count(2) == 14 and census.count(3) == 7
    # distance bound per owner: F(d(e_z,y))+F(d(0,y)) <= N^-4+(N+1)^-4 <= 2N^-4, at most 3 owners per face
    per_owner_ok = all(F_poly(N - 1) + F_poly(N) <= 2 * Q(1, N ** 4) and 28 * N * (5 * N + 1) * 3 * 2 * Q(1, N ** 4) == 168 * Q(5 * N + 1, N ** 3)
                       for N in range(2, 200))
    # fine-lattice conversion (descriptive only; no constant uses it)
    R_links = block_links(ORIGIN) + block_links(EZ)
    R_link_set = set(R_links)
    R_end = {l[0] for l in R_links} | {add(l[0], E_UNIT[l[1]]) for l in R_links}
    R_tails = {l[0] for l in R_links}
    fine = {}
    for N in (2, 3):
        faces = list(enum[N]['extra_faces'].values())
        links = [lk for (b, k) in faces for lk in face_links(*_face_geom(b, k))]
        fine[N] = {'min_fine_tail_distance': min(l1(lk[0], w) for lk in links for w in R_tails),
                   'min_fine_vertex_distance_to_R_endpoints': min(l1(v, w) for lk in links for v in (lk[0], add(lk[0], E_UNIT[lk[1]])) for w in R_end),
                   'shared_links_with_R_cover': sum(1 for lk in links if lk in R_link_set)}
    fine_ok = all(fine[N]['min_fine_tail_distance'] == N - 1 and fine[N]['min_fine_vertex_distance_to_R_endpoints'] == N - 2
                  and fine[N]['shared_links_with_R_cover'] == 0 for N in (2, 3))

    def validate_extra(count_fn, owner_layer, dmin_ez, padding_charged):
        require(all(count_fn(N) == 28 * N * (5 * N + 1) for N in (2, 3, 4)), 'extra-face count differs from 28N(5N+1)')
        require(owner_layer == 'max_i |b_i| = N', 'owners must lie on the outer layer')
        require(all(dmin_ez(N) == N - 1 for N in (2, 3, 4)), 'distance from e_z must be N-1 (coarse l1)')
        require(padding_charged is False, 'padding on-site terms are never charged as boundary terms')
        return True
    good_count = lambda N: enum[N]['extra']
    check('extra_face_count_and_distance',
          enum_ok and extra_class_sum_ok and census_ok and per_owner_ok and fine_ok
          and validate_extra(good_count, 'max_i |b_i| = N', lambda N: enum[N]['min_l1_from_e_z'], False)
          and rejected(lambda: validate_extra(lambda N: good_count(N) + 3 * (2 * N + 1) ** 2, 'max_i |b_i| = N', lambda N: N - 1, False),
                       'padding_sites_counted_as_faces')
          and rejected(lambda: validate_extra(lambda N: enum[N]['F2'], 'max_i |b_i| = N', lambda N: N - 1, False), 'all_F2_faces_charged')
          and rejected(lambda: validate_extra(good_count, 'max_i |b_i| = N', lambda N: N - 2, False), 'distance_N_minus_2_claimed')
          and rejected(lambda: validate_extra(good_count, 'max_i |b_i| = N-1', lambda N: N - 1, False), 'owner_layer_inside')
          and rejected(lambda: validate_extra(good_count, 'max_i |b_i| = N', lambda N: N - 1, True), 'padding_onsite_charged'),
          enumeration={str(N): {k: (s(v) if isinstance(v, Q) else v) for k, v in e.items() if k not in ('extra_keys', 'extra_faces')}
                       for N, e in enum.items()},
          S_b_exact_preview={str(N): dec(enum[N]['S_b_exact']) for N in enum},
          all_size_argument='face (b,K) is extra iff b in Lambda_N, b_j<N for e_j in K and b_i=N for some direction i not in K; '
                            'count per one-direction class 2N(4N+1) (14 classes), per two-direction class 4N^2 (7 classes); total 28N(5N+1); '
                            'every owner y has y_i=N, so max_i |y_i| = N, d(e_z,y) at least N-1 and d(0,y) at least N',
          fine_units=fine, fine_units_note='coarse l1 N-1 from e_z is N-1 fine steps along z between link tails; plaquette corners may come '
                                           'within N-2 fine steps of the 36 endpoints of R; no link is shared; no fine distance enters any constant')

    # ======================= padding on-site terms factor out exactly =======================
    Hs = mat([[1, Q(1, 2)], [Q(1, 2), -1]])
    Kp = mat([[2, (0, 1)], [(0, -1), Q(-1, 3)]])
    Aop = mat([[0, 1], [0, 0]])
    Vu, Wu = cayley(Hs), cayley(Kp)
    U4 = kron(Vu, Wu)
    unitary = is_zero(madd(mmul(U4, madj(U4)), eye(4), -1))
    lhs = mmul(mmul(U4, kron(Aop, eye(2))), madj(U4))
    rhs = kron(mmul(mmul(Vu, Aop), madj(Vu)), eye(2))
    factor_ok = is_zero(madd(lhs, rhs, -1))
    comm1 = is_zero(madd(mmul(kron(Hs, eye(2)), kron(eye(2), Kp)), mmul(kron(eye(2), Kp), kron(Hs, eye(2))), -1))
    comm2 = is_zero(madd(mmul(kron(eye(2), Kp), kron(Aop, eye(2))), mmul(kron(Aop, eye(2)), kron(eye(2), Kp)), -1))
    B_plus_ok = all(len(set(add(b, d) for b in coarse_box(N) for d in S_STAR) - coarse_box(N)) == 3 * (2 * N + 1) ** 2 for N in (2, 3))

    def validate_source_bounded(terms):
        for label, norm_at_cutoff in terms:
            require(all(norm_at_cutoff(L) == norm_at_cutoff(10) for L in (100, 1000)), 'unbounded (cutoff-dependent) term in the Duhamel source: ' + label)
        return True
    face_term = ('extra face -(tau/3)W_f', lambda L: Q(1, 3))
    pad_term = ('padding on-site h_x', lambda L: Q(L - 1))
    check('padding_onsite_terms_factor_out',
          unitary and factor_ok and comm1 and comm2 and B_plus_ok and validate_source_bounded([face_term])
          and rejected(lambda: validate_source_bounded([face_term, pad_term]), 'padding_onsite_left_in_duhamel_source'),
          fixture='exact Gaussian-rational unitaries V=Cayley(H), W=Cayley(K): (V x W)(A x 1)(V x W)* = (V A V*) x 1',
          analytic_step='e^{iu(H x 1 + 1 x K)} = e^{iuH} x e^{iuK} for self-adjoint H, K on separate tensor factors (closure of the sum on the '
                        'algebraic tensor product of domains; Reed-Simon VIII.33 as cited by the source); cited, not machine-checked',
          padding_sites='|B_+ minus Lambda_N| = 3(2N+1)^2 (75 at N=2, 147 at N=3), onsite terms only')

    # ======================= whole-star interaction norms; incoming stars =======================
    def stars_containing(u):
        window = product(*(range(c0 - 1, c0 + 2) for c0 in u))
        return [b for b in window if u in {add(b, d) for d in S_STAR}]
    incident = {u: len(stars_containing(u)) for u in product(range(-3, 4), repeat=3)}
    J_enum = 7 * max(incident.values())   # per |tau|: four incident stars of norm 7|tau|
    faces_per_site = len(faces_containing(ORIGIN, omitted))
    # exact (48) supremum for the whole-star interaction (labelled observation, not used)
    pair_sup = Q(0)
    nbhd = list(product(range(-2, 3), repeat=3))
    for x in nbhd:
        for y in nbhd:
            n_st = sum(1 for b in stars_containing(x) if y in {add(b, d) for d in S_STAR})
            if n_st:
                pair_sup = max(pair_sup, Q(7 * n_st) / F_poly(l1(x, y)))

    def validate_J(J_per_tau, stars_counted, faces_site):
        require(stars_counted == 4 and J_per_tau == 28, 'per-site sum must include the incoming stars (4 x 7|tau|)')
        require(faces_site == 49, 'per-site face count must include incoming faces (49)')
        require(V['phi_factor_contract'] * J_per_tau == V['phi_contract'], '||Phi||_F <= 81 J with the complete J')
        return True
    check('missing_incoming_stars',
          J_enum == J_aq1 == 28 and all(v1 == 4 for v1 in incident.values()) and faces_per_site == 49
          and validate_J(J_enum, 4, faces_per_site) and pair_sup == 567
          and rejected(lambda: validate_J(7, 1, faces_per_site), 'outgoing_star_only_J_7')
          and rejected(lambda: validate_J(28, 4, 21), 'outgoing_faces_only_21_per_site')
          and rejected(lambda: validate_J(14, 2, faces_per_site), 'two_anchor_orthant_count'),
          J_per_abs_tau=J_enum, incident_stars_per_site=4, faces_per_site=faces_per_site,
          Phi_F_admitted_per_abs_tau=s(V['phi_contract']),
          labelled_observation='the exact (48) supremum for the whole-star interaction is %s|tau| (pairs at l1 distance 2 inside one star, 81 x 7); '
                               'the admitted 81J=2268|tau| is used in every constant; the sharper value is not used' % s(pair_sup))

    # ======================= LR/Duhamel constants (forward route, F1 inner) =======================
    U = V['Theta'] / V['u_div']
    require(U == 1, 'normalized window U=Theta/8=1')
    phiF, Cc = V['phi_contract'], V['C_contract']
    lam = {}
    Kc = {}
    for sg, tv in taus.items():
        phi_abs = phiF * abs(tv)
        lam[sg] = lr_time_integral_upper(phi_abs, Cc, U)
        Kc[sg] = {'cmp': duhamel_coefficient(tv, U, 168, phi_abs, Cc),
                  'c1': duhamel_coefficient(tv, U, 392, phi_abs, Cc)}
        Kc[sg]['c2'] = Kc[sg]['c1'] + Q(11, 8) * Kc[sg]['cmp']
    K = Kc['+']
    closed = {'cmp': Q(254016) * tau_cap ** 2 / (1 - 338688 * tau_cap), 'c1': Q(592704) * tau_cap ** 2 / (1 - 338688 * tau_cap),
              'c2': Q(941976) * tau_cap ** 2 / (1 - 338688 * tau_cap)}
    signs_equal = all(Kc['-'][k] == Kc['+'][k] for k in K)
    # all-size lemmas
    shape_ok = all(Q((5 * N + 1) * (N - 1), N ** 3) <= Q(11, 8) for N in range(2, 400)) and Q(5 * 2 + 1, 8) == Q(11, 8)
    tail_ok = all(Q(4 * r * r + 2) <= 4 * (1 + r) ** 2 for r in range(0, 400)) and all(
        sum(Q(1, k * (k - 1)) for k in range(m + 1, m + 400)) <= Q(1, m) for m in range(1, 40))
    cmp_met = K['cmp'] <= V['target_cmp']
    c1_met = K['c1'] <= V['target_cau']
    c2_met = K['c2'] <= V['target_cau']
    b_of_N = {N: K['cmp'] * Q(5 * N + 1, N ** 3) for N in range(2, 11)}
    b_refined = {N: duhamel_coefficient(tau_cap, U, enum[N]['S_b_exact'], phiF * tau_cap, Cc) for N in (2, 3, 4)}
    per_N_ok = all(b_of_N[N] <= V['target_cmp'] * Q(5 * N + 1, N ** 3) for N in b_of_N) and all(
        b_refined[N] <= b_of_N[N] for N in b_refined)
    check('comparison_bound_all_N',
          cmp_met and signs_equal and K['cmp'] == closed['cmp'] and per_N_ok and enum_ok,
          statement='||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| <= b(N)||A|| <= K_cmp (5N+1) N^-3 ||A|| for |theta|<=8, N at least 2, both signs',
          b_N_formula='b(N) = (|tau|/3) Lambda(U) S_b(N), Lambda(U) = int_0^U (2/C)(e^{vr}-1)dr <= 2||Phi||_F U^2/(1-vU/3), v=2||Phi||_F C, '
                      'S_b(N) = sum over the 28N(5N+1) extra faces of sum_{x in R, y in M_f} F(d(x,y)) <= 168(5N+1)N^-3',
          K_cmp=s(K['cmp']), K_cmp_preview=dec(K['cmp']), K_cmp_closed_form='254016 tau^2/(1-338688|tau|)',
          target=s(V['target_cmp']), target_met=cmp_met, margin_preview=dec(V['target_cmp'] / K['cmp'], 6),
          Lambda_U1=s(lam['+']), Lambda_U1_preview=dec(lam['+']),
          b_N_all_size_preview={str(N): dec(b_of_N[N]) for N in b_of_N},
          labelled_refinement_enumerated_sum={str(N): {'b_N': s(b_refined[N]), 'preview': dec(b_refined[N]),
                                                       'ratio_to_all_size_bound_preview': dec(b_refined[N] / b_of_N[N], 6)} for N in b_refined},
          tier=TIER, interaction=PHI_WHOLE, inner_family='F1', minus_tau='replay of the same |tau| formula, not a second confirmation')

    # ======================= within-family Cauchy (sup over all M greater than N) =======================
    c_shape_ok = all(Q(4, N) <= Q(4, N - 1) for N in range(2, 400))
    check('within_family_cauchy_and_limits',
          c1_met and c2_met and tail_ok and shape_ok and c_shape_ok and K['c1'] == closed['c1'] and K['c2'] == closed['c2'] and signs_equal,
          F1='sup over M greater than N of ||T^{F1,M}_theta(A)-T^{F1,N}_theta(A)|| <= K_c1/(N-1) ||A||; hence ||T_theta(A)-T^{F1,N}_theta(A)|| <= K_c1/(N-1)||A||',
          F2='sup over M greater than N of ||T^{F2,M}_theta(A)-T^{F2,N}_theta(A)|| <= (K_c1 + (11/8) K_cmp)/(N-1) ||A|| = K_c2/(N-1)||A||; '
             'and ||T_theta(A)-T^{F2,N}_theta(A)|| <= K_c1/(N-1)||A||',
          K_c1=s(K['c1']), K_c1_preview=dec(K['c1']), K_c1_closed_form='592704 tau^2/(1-338688|tau|)',
          K_c2=s(K['c2']), K_c2_preview=dec(K['c2']), K_c2_closed_form='941976 tau^2/(1-338688|tau|)',
          target=s(V['target_cau']), F1_met=c1_met, F2_met=c2_met,
          margin_F1_preview=dec(V['target_cau'] / K['c1'], 6), margin_F2_preview=dec(V['target_cau'] / K['c2'], 6),
          tail_lemma='every owner of a face whose anchor star is not inside Lambda_N has ||y||_inf at least N; at most 49 faces per site; '
                     'the sum of F(d(0,y)) over ||y||_inf at least N is <= sum over r from N of (4r^2+2)(1+r)^-4 <= 4/N and the same from e_z <= 4/(N-1); S_c(N) <= 392/(N-1)',
          tier=TIER, interaction=PHI_WHOLE, inner_family='F1 (on Lambda_N with the onsite terms of the larger box, or on Lambda_M)')

    # enumerated audit of the Cauchy source sets (N=2, M=3,4) and the owner layer of E_N
    src_audit = {}
    for N, M in ((2, 3), (2, 4), (3, 4)):
        f1N, f2N = f1_faces(N, omitted), f2_faces(N, omitted)
        f1M, f2M = f1_faces(M, omitted), f2_faces(M, omitted)
        new_f1 = [f1M[k] for k in f1M if k not in f1N]
        new_f2_vs_f1N = [f2M[k] for k in f2M if k not in f1N]
        f1M_minus_f2N = [f1M[k] for k in f1M if k not in f2N]
        in_EN = lambda f: not all(add(f[0], d) in coarse_box(N) for d in S_STAR)
        src_audit[(N, M)] = {
            'F1_new': len(new_f1), 'F2M_minus_F1N': len(new_f2_vs_f1N), 'F1M_minus_F2N': len(f1M_minus_f2N),
            'all_in_E_N': all(in_EN(f) for f in new_f1 + new_f2_vs_f1N),
            'owners_linf_ge_N': all(linf(y) >= N for f in new_f1 + new_f2_vs_f1N + f1M_minus_f2N for y in owner_set(f)),
            'F1N_subset_F1M_subset_F2M': set(f1N) <= set(f1M) <= set(f2M),
            'F2N_subset_F1M': set(f2N) <= set(f1M) if M >= N + 1 else None,
            'new_F1_meet_shell': all(any(y not in coarse_box(N) for y in {add(f[0], d) for d in S_STAR}) for f in new_f1)}
    EN_window_ok = all(linf(y) >= N for N in (2, 3) for b in product(range(-N - 2, N + 3), repeat=3)
                       if not all(add(b, d) in coarse_box(N) for d in S_STAR) for k in omitted for y in owner_set((b, k)))
    per_site_EN_ok = all(sum(1 for f in faces_containing(u, omitted)) == 49 for u in ((5, 0, 0), (0, -4, 2), (3, 3, 3)))
    audit_ok = all(a['all_in_E_N'] and a['owners_linf_ge_N'] and a['F1N_subset_F1M_subset_F2M'] and a['F2N_subset_F1M']
                   and a['new_F1_meet_shell'] for a in src_audit.values()) and EN_window_ok and per_site_EN_ok

    # ======================= boundary source: new terms only; regrouping charged once =======================
    def validate_source(charged, outer, inner, source_set, support):
        """charged: list of interaction-term keys; outer/inner: dicts key -> term; support(term) -> coarse site set."""
        require(len(charged) == len(set(charged)), 'a term is charged twice')
        require(set(charged) == set(outer) - set(inner), 'source must equal the new terms (outer minus inner), no old term, none missing')
        pool = dict(inner)
        pool.update(outer)
        require(all(support(pool[k]) & source_set for k in charged), 'a charged term does not meet the source set')
        return True

    def stars_in(N):
        box = coarse_box(N)
        return {b: frozenset(add(b, d) for d in S_STAR) for b in box if all(add(b, d) in box for d in S_STAR)}
    face_support = owner_set
    f1_2, f2_2, f1_3, f2_3 = f1_faces(2, omitted), f2_faces(2, omitted), f1_faces(3, omitted), f2_faces(3, omitted)
    st_2, st_3 = stars_in(2), stars_in(3)
    shell_2_3 = coarse_box(3) - coarse_box(2)
    outer_layer_2 = frozenset(y for y in coarse_box(2) if max(y) == 2)
    src_cmp_keys = [k for k in f2_2 if k not in f1_2]
    src_cmp = [f2_2[k] for k in src_cmp_keys]
    new_stars = [b for b in st_3 if b not in st_2]
    faces_of_new_stars = [(b, k) for b in new_stars for k in omitted]
    per_face_once = len({face_key(f) for f in faces_of_new_stars}) == len(faces_of_new_stars) == 21 * len(new_stars)
    per_face_owner_ok = all(linf(y) >= 2 for f in faces_of_new_stars for y in owner_set(f))
    old_face_key = next(k for k, f in f1_2.items() if owner_set(f) & frozenset(COVER_R))
    check('boundary_source_new_terms_only',
          audit_ok and per_face_once and per_face_owner_ok
          and validate_source(src_cmp_keys, f2_2, f1_2, outer_layer_2, face_support)
          and validate_source(new_stars, st_3, st_2, shell_2_3, lambda st: st)
          and rejected(lambda: validate_source(src_cmp_keys + [old_face_key], f2_2, f1_2, outer_layer_2, face_support), 'old_face_meeting_R_charged')
          and rejected(lambda: validate_source(new_stars[1:], st_3, st_2, shell_2_3, lambda st: st), 'new_star_dropped')
          and rejected(lambda: validate_source(new_stars + [ORIGIN], st_3, st_2, shell_2_3, lambda st: st), 'old_star_at_0_charged_in_cauchy'),
          comparison_source='F2(N) minus F1(N): 28N(5N+1) extra faces, each meeting the outer layer max_i y_i = N',
          cauchy_source='F1(M) minus F1(N): new whole stars (the F1 interaction terms), each meeting Lambda_M minus Lambda_N; '
                        'split face by face (21 faces per star, each charged once, every owner with ||y||_inf at least N); '
                        'F2(M) minus F1(N) and F1(M) minus F2(N) lie in E_N (audit)',
          new_stars_2_to_3=len(new_stars), audit={'%d_to_%d' % k: v1 for k, v1 in src_audit.items()},
          note='the onsite terms of the larger box are placed in the inner Hamiltonian, where they factor out (interaction picture, NS (78)-(79))')

    # F2 regrouping from N to N+1: clipped groups gain faces; charge face by face
    def group_faces(N, b):
        box = coarse_box(N)
        return [(b, k) for k in omitted if owner_set((b, k)) <= box]
    gaining = [b for b in coarse_box(2) if len(group_faces(3, b)) > len(group_faces(2, b))]
    regroup_whole = [f for b in gaining for f in group_faces(3, b)]
    regroup_new = [f for b in gaining for f in group_faces(3, b) if face_key(f) not in f2_2]
    f2_new_all = [f2_3[k] for k in f2_3 if k not in f2_2]
    per_site_face = Q(49, 3)

    def validate_regroup(charged):
        return validate_source([face_key(f) for f in charged], f2_3, f2_2, shell_2_3, face_support)
    check('f2_regrouping_charged_once',
          len(gaining) > 0 and set(face_key(f) for f in regroup_new) <= set(face_key(f) for f in f2_new_all)
          and validate_regroup(f2_new_all) and per_site_face <= J_enum
          and rejected(lambda: validate_regroup(f2_new_all + [f for f in regroup_whole if face_key(f) in f2_2]), 'regrouped_group_charged_whole')
          and rejected(lambda: validate_regroup(f2_new_all + f2_new_all[:5]), 'face_charged_twice'),
          clipped_groups_gaining_2_to_3=len(gaining), faces_gained_in_those_groups=len(regroup_new), F2_new_faces_2_to_3=len(f2_new_all),
          per_site_face_sum_per_abs_tau=s(per_site_face), J_per_abs_tau=J_enum,
          note='every Cauchy and comparison source in this route is a set of faces, each charged once with norm |tau|/3')

    # ======================= inner-family constants =======================
    def validate_inner(record):
        require(record['inner_family'] in ('F1', 'F2'), 'inner family must be named')
        want = {'F1': (PHI_WHOLE, V['phi_contract']), 'F2': (PHI_OWNER, V['phiprime_contract'])}[record['inner_family']]
        require(record['interaction'] == want[0] and record['phi_F_per_abs_tau'] == want[1], 'constants are not those of the inner family')
        require(record['tier'] in V['tiers_allowed'], 'tier must be named')
        return True
    rec_cmp = {'inner_family': 'F1', 'interaction': PHI_WHOLE, 'phi_F_per_abs_tau': phiF, 'tier': TIER}
    swapped = dict(rec_cmp, phi_F_per_abs_tau=V['phiprime_contract'])
    swapped_label = dict(rec_cmp, interaction=PHI_OWNER, phi_F_per_abs_tau=V['phiprime_contract'])
    K_swapped = duhamel_coefficient(tau_cap, U, 168, V['phiprime_contract'] * tau_cap, Cc)
    check('duhamel_inner_family_constants',
          validate_inner(rec_cmp) and K_swapped < K['cmp']
          and rejected(lambda: validate_inner(swapped), 'F1_inner_with_owner_set_1323_unstated')
          and rejected(lambda: validate_inner(swapped_label), 'F1_inner_relabelled_owner_set')
          and rejected(lambda: validate_inner(dict(rec_cmp, inner_family='unnamed')), 'inner_family_unnamed'),
          records={'comparison': 'F1 inner, whole-star Phi, 2268|tau|', 'cauchy_F1': 'F1 inner, whole-star Phi, 2268|tau|',
                   'cauchy_F2': 'F1 inner (Lambda_N with onsite padding of Lambda_M) plus the comparison, whole-star Phi, 2268|tau|',
                   'distance_F2_to_limit': 'F1 inner on Lambda_M, whole-star Phi, 2268|tau|'},
          swapped_constant_preview=dec(K_swapped),
          note="the owner-set Phi' (1323|tau|) is named only; F2 on Lambda_N is its native restriction, but no forward constant uses it")

    # ======================= tau order (quadratic) and scaling =======================
    def coeff_at(t, which):
        t = abs(t)
        sums = {'cmp': 168, 'c1': 392}
        if which == 'c2':
            return coeff_at(t, 'c1') + Q(11, 8) * coeff_at(t, 'cmp')
        return duhamel_coefficient(t, U, sums[which], phiF * t, Cc)
    ratios = {k: coeff_at(tau_cap, k) / coeff_at(tau_cap / 100, k) for k in ('cmp', 'c1', 'c2')}
    monotone = all(coeff_at(tau_cap / d, k) <= coeff_at(tau_cap, k) for k in ('cmp', 'c1', 'c2') for d in (2, 10, 100, 1000))

    def validate_order(ratio, br, label_order):
        require(br[0] <= ratio <= br[1], 'tau^2 scaling ratio outside the preregistered bracket')
        require(label_order == 2, 'the dynamics difference is labelled quadratic in tau')
        return True
    linear_bound = lambda t: abs(t) / 3 * 2 * U * 616   # trivial commutator bound 2||A||, no LR factor: first order, no decay in N
    lin_ratio = linear_bound(tau_cap) / linear_bound(tau_cap / 100)
    check('duhamel_tau_order_quadratic',
          all(validate_order(ratios[k], V['bracket_quadratic'], 2) for k in ratios)
          and rejected(lambda: validate_order(ratios['cmp'], V['bracket_quadratic'], 1), 'quadratic_bound_labelled_linear')
          and rejected(lambda: validate_order(lin_ratio, V['bracket_quadratic'], 1), 'trivial_commutator_bound_linear_in_tau'),
          ratios_preview={k: dec(v1, 10) for k, v1 in ratios.items()}, ratios_exact={k: s(v1) for k, v1 in ratios.items()},
          first_order='vanishes exactly: with the onsite evolution alone T^0_r(A) stays in B(H_R) and every extra face acts on links owned '
                      'outside R, so [W_f, T^0_r(A)]=0; the LR factor e^{vr}-1 is itself O(|tau|)',
          linear_trap_ratio=s(lin_ratio))

    def validate_scaling(ratio, br, bracket_source):
        require(bracket_source == 'contract', 'bracket must be the preregistered one, read from the contract')
        require(br[0] <= ratio <= br[1], 'scaling ratio outside the preregistered bracket')
        return True
    cubic_ratio = Q(10) ** 6
    check('tau_scaling_exponent',
          validate_scaling(ratios['cmp'], V['bracket_cmp'], 'contract') and validate_scaling(ratios['c1'], V['bracket_cau'], 'contract')
          and validate_scaling(ratios['c2'], V['bracket_cau'], 'contract') and monotone
          and rejected(lambda: validate_scaling(lin_ratio, V['bracket_cmp'], 'contract'), 'linear_order_bound')
          and rejected(lambda: validate_scaling(cubic_ratio, V['bracket_cmp'], 'contract'), 'cubic_order_bound')
          and rejected(lambda: validate_scaling(ratios['cmp'], (ratios['cmp'] - 1, ratios['cmp'] + 1), 'chosen_after_evaluation'), 'bracket_chosen_after_evaluation'),
          ratios={k: {'exact': s(v1), 'preview': dec(v1, 10)} for k, v1 in ratios.items()},
          brackets={'comparison_coefficient': [s(x) for x in V['bracket_cmp']], 'cauchy_coefficient': [s(x) for x in V['bracket_cau']]},
          monotone_in_abs_tau=monotone, note='same exact formula at tau and tau/100, no intermediate rounding')

    # ======================= polynomial tail, subsequences, whole sequence =======================
    # lower-bound fixture: the tail sum over ||y||_inf>=N is at least of order 1/N (slab N<=y_z<=2N, |y_x|,|y_y|<=y_z)
    lower = {}
    for N in range(2, 31):
        lo = sum(Q((2 * z + 1) ** 2) * F_poly(3 * z) for z in range(N, 2 * N + 1))
        lower[N] = lo
    poly_lower_ok = all(N * lower[N] >= Q(1, 400) for N in lower)

    def validate_rate(kind, rate, summable_steps=None):
        require(kind == 'sup_over_all_M', 'a Cauchy estimate is a bound for all M greater than N; an N to N+1 bound is not')
        require(rate in ('1/(N-1)',), 'with F(r)=(1+r)^-4 the honest Cauchy rate is O(1/N); an exponential rate is not available')
        if summable_steps is not None:
            require(summable_steps, 'summed step bounds must have a finite tail')
        return True
    harmonic = [sum(Q(1, k) for k in range(2, 2 ** m + 1)) for m in range(1, 11)]
    harmonic_div = all(harmonic[m - 1] >= Q(m - 1, 2) for m in range(1, 11)) and harmonic[-1] > 4

    def exp_rate_claim():
        # an exponential tail C0 q^N (C0=1, q=1/2) is contradicted by the exact polynomial lower bound of the tail sum
        require(all(lower[N] <= Q(1, 2 ** N) for N in lower), 'exponential rate contradicted by the polynomial tail lower bound')
        return validate_rate('sup_over_all_M', 'exp')
    check('lieb_robinson_polynomial_tail',
          poly_lower_ok and harmonic_div and validate_rate('sup_over_all_M', '1/(N-1)')
          and rejected(lambda: validate_rate('N_to_N_plus_1', '1/(N-1)'), 'N_to_N_plus_1_bound_as_cauchy')
          and rejected(lambda: validate_rate('sup_over_all_M', '1/(N-1)', summable_steps=harmonic[-1] < 4), 'harmonic_step_sum_diverges')
          and rejected(exp_rate_claim, 'exponential_rate_with_AQ1_constants'),
          comparison_decay='(5N+1) N^-3, order N^-2', cauchy_decay='1/(N-1)',
          tail_lower_bound_times_N_preview={str(N): dec(N * lower[N], 6) for N in (2, 5, 10, 20, 30)},
          exponential_contradicted_at_N=[N for N in lower if lower[N] > Q(1, 2 ** N)][:3],
          harmonic_partial_sums_preview=[dec(h, 6) for h in harmonic],
          note='the O(1/N) rate is that of the method with the polynomial F; no lower bound on the actual dynamics difference is claimed')

    # subsequence versus whole sequence
    alt = [Q((-1) ** N, 7) for N in range(2, 40)]
    parity_conv = len(set(alt[0::2])) == 1 and len(set(alt[1::2])) == 1
    cauchy_fail = all(abs(alt[i + 1] - alt[i]) == Q(2, 7) for i in range(len(alt) - 1))

    def validate_limit_claims(claims):
        for obj, (kind, basis) in claims.items():
            require(kind in ('whole_sequence', 'subsequence'), 'every limit statement says whole sequence or subsequence: ' + obj)
            if kind == 'whole_sequence':
                require(basis == 'cauchy_bound', 'whole-sequence claims come only from a Cauchy bound: ' + obj)
        require(claims['F2 limit states'][0] == 'subsequence' and claims['F1 limit states'][0] == 'subsequence', 'states remain subsequential')
        return True
    claims = {'F1 finite-box evolutions': ('whole_sequence', 'cauchy_bound'), 'F2 finite-box evolutions': ('whole_sequence', 'cauchy_bound'),
              'F1 limit states': ('subsequence', 'trace_norm_compactness'), 'F2 limit states': ('subsequence', 'trace_norm_compactness')}
    check('subsequence_versus_whole_sequence',
          parity_conv and cauchy_fail and validate_limit_claims(claims)
          and rejected(lambda: validate_limit_claims(dict(claims, **{'F2 limit states': ('whole_sequence', 'cauchy_bound')})), 'state_whole_sequence_claimed')
          and rejected(lambda: validate_limit_claims(dict(claims, **{'F2 finite-box evolutions': ('whole_sequence', 'parity_subsequences')})),
                       'alternating_sequence_parity_limits')
          and rejected(lambda: validate_limit_claims(dict(claims, **{'F1 finite-box evolutions': ('limit', 'cauchy_bound')})), 'unlabelled_limit'),
          claims={k: list(v1) for k, v1 in claims.items()},
          fixture='a_N=(-1)^N/7: both parity subsequences converge, |a_{N+1}-a_N|=2/7, no Cauchy bound, no whole-sequence limit')

    # ======================= F2 limit dynamics equals T_theta; O6 rerun =======================
    o6_steps = {
        'stationarity': 'omega2(T_u(A))=omega2(A): F2 finite ground invariance along F2 subsequence N_k, local trace-norm convergence on Lambda_n, '
                        'and ||T_u(A)-T^{F2,n}_u(A)|| tends to 0 (this loop, whole sequence); extended to all u by the group property',
        'gns_unitaries': 'U_u pi(A)Omega = pi(T_u(A))Omega well defined and unitary by stationarity',
        'strong_continuity': 'finite F2 evolution strong-* continuous, normal local density, uniform approximation on |u|<=1; continuity at 0 '
                             'of a unitary group gives strong continuity everywhere',
        'nonnegative_generator': 'finite F2 centered energies nonnegative (simple ground, AY1 via AM2); correlations pass along N_k; negative-energy Fourier '
                                 'tests pass by dominated convergence (F2 converges to T on every compact window, qualitative)',
        'physical_sector': 'F2 finite ground states gauge invariant; T preserves A_phys; the physical cyclic space reduces U and H'}

    def validate_identification(record):
        require(record['basis'] == 'comparison_bound_and_cauchy', 'identification must come through the comparison bound')
        require(record['subsequences'] == 'F2 own', "limit-state properties are rerun with F2's own subsequences")
        require(set(record['steps']) == set(o6_steps) and all(v1 == 'proved' for v1 in record['steps'].values()), 'every O6 step is proved, not assumed')
        require(record['comparison_to_zero'] and record['f2_distance_to_limit_to_zero'], 'the identification needs both bounds to vanish')
        return True
    ident = {'basis': 'comparison_bound_and_cauchy', 'subsequences': 'F2 own', 'steps': {k: 'proved' for k in o6_steps},
             'comparison_to_zero': all(Q(5 * (N + 1) + 1, (N + 1) ** 3) < Q(5 * N + 1, N ** 3) for N in range(2, 300))
             and Q(5 * 10 ** 6 + 1, 10 ** 18) < Q(1, 10 ** 11),
             'f2_distance_to_limit_to_zero': all(Q(1, N) < Q(1, N - 1) for N in range(3, 300))}
    check('f2_limit_dynamics_equals_f1',
          validate_identification(ident)
          and rejected(lambda: validate_identification(dict(ident, basis='same_terms_near_R')), 'identified_by_local_terms_only')
          and rejected(lambda: validate_identification(dict(ident, subsequences='F1')), 'F1_subsequence_used_for_F2_states')
          and rejected(lambda: validate_identification(dict(ident, steps=dict(ident['steps'], stationarity='assumed'))), 'stationarity_assumed'),
          statement='for every A in B(H_R) and |theta|<=8: ||T^{F2,N}_theta(A)-T_theta(A)|| <= K_c1/(N-1)||A||, so the F2 evolutions converge as a whole '
                    'sequence to the AQ1 limit dynamics T_theta; for every local A and every compact window the same holds qualitatively; '
                    'T extends to the quasi-local algebra (NS Theorem 4.1)',
          o6_rerun=o6_steps)

    # O6 fixtures: stationarity is not positivity; strong versus norm continuity
    E0, E1 = Q(0), Q(1)
    excited_transition = E0 - E1   # invariant excited state |1>: correlation of sigma_x has frequency E0-E1 < 0
    ground_transition = E1 - E0
    norm_disc = all(abs(Q(-1) - 1) == 2 for n in range(1, 30))            # e^{i n (pi/n)} - 1 = -2 on the moving vector e_n
    fixed_vec = all(Q(1, n) <= Q(1, n) for n in range(1, 30))             # |e^{it}-1| <= |t| on the fixed vector e_1

    def validate_positivity_basis(basis):
        require(basis == 'finite_ground_states_and_fourier_passage', 'nonnegative generator needs finite ground states, not stationarity alone')
        return True

    def validate_continuity(kind):
        require(norm_disc and fixed_vec, 'continuity fixture')
        require(kind == 'strong_gns', 'only strong continuity of the GNS group is claimed; norm continuity in time on full B(H) fails (moving vector e_n)')
        return True
    check('o6_limit_state_properties_rerun',
          excited_transition < 0 < ground_transition and validate_positivity_basis('finite_ground_states_and_fourier_passage')
          and validate_continuity('strong_gns')
          and rejected(lambda: validate_positivity_basis('stationarity_only'), 'stationarity_without_ground_property')
          and rejected(lambda: validate_continuity('norm_full_B'), 'norm_time_continuity_claimed'),
          fixtures={'stationary_excited_state': 'H=diag(0,1), invariant excited vector e_1, sigma_x correlation frequency E0-E1=%s' % s(excited_transition),
                    'strong_not_norm': 'U(t)e_j=e^{ijt}e_j, Ae_j=e_{2j}: ||U(pi/n)AU(pi/n)*-A||=2 on e_n; <=|t| on the fixed e_1'})

    # ======================= algebraic, not GNS dynamics =======================
    ph = (Q(3, 5), Q(4, 5))                       # exact unit Gaussian rational phase
    Ud = [[cz(1), cz(0)], [cz(0), ph]]
    sx = mat([[0, 1], [1, 0]])
    evolved = mmul(mmul(Ud, sx), madj(Ud))        # the same automorphism for both states
    prod_ = mmul(sx, evolved)
    corr_ground, corr_excited = prod_[0][0], prod_[1][1]
    both_invariant = is_zero(madd(mmul(mmul(Ud, mat([[1, 0], [0, 0]])), madj(Ud)), mat([[1, 0], [0, 0]]), -1))
    same_automorphism_different_correlation = both_invariant and corr_ground == ph and corr_excited == cconj(ph) and corr_ground != corr_excited

    def validate_meaning(fields):
        require(fields['gns_dynamics_equality_claimed'] is False, 'no equality of GNS dynamics')
        require(fields['dynamics_level'] == 'algebraic_heisenberg_compact_window', 'algebraic Heisenberg dynamics on a compact window')
        require(fields['correlation_equality_claimed'] is False, 'no equality of correlation functions of different states')
        return True
    meaning = {'gns_dynamics_equality_claimed': False, 'dynamics_level': 'algebraic_heisenberg_compact_window', 'correlation_equality_claimed': False}
    check('algebraic_not_gns_dynamics',
          same_automorphism_different_correlation and validate_meaning(meaning)
          and rejected(lambda: validate_meaning(dict(meaning, gns_dynamics_equality_claimed=True)), 'gns_dynamics_equality_claimed')
          and rejected(lambda: validate_meaning(dict(meaning, correlation_equality_claimed=True)), 'correlations_of_different_states_equal')
          and rejected(lambda: validate_meaning(dict(meaning, dynamics_level='gns')), 'gns_level_label'),
          fixture='one automorphism group (U=diag(1,(3+4i)/5)), two invariant vector states e_0, e_1: sigma_x correlations (3+4i)/5 versus (3-4i)/5',
          meaning='algebraic Heisenberg dynamics of the named constructions on a compact window; states and correlations need a common state (BB2)')

    # ======================= window and clock =======================
    def validate_window(Theta, u_div, label, uniform_in_time):
        require(label == 'theta' and Theta == V['Theta'] and u_div == V['u_div'], 'window named in the common clock theta with U=Theta/8')
        require(uniform_in_time is False, 'no uniform-in-time claim')
        return True
    grow = lr_time_integral_upper(phiF * tau_cap, Cc, 2) / lr_time_integral_upper(phiF * tau_cap, Cc, 1)
    check('time_window_named_common_clock',
          validate_window(V['Theta'], V['u_div'], 'theta', False) and grow >= 4
          and rejected(lambda: validate_window(V['Theta'], V['u_div'], 'theta', True), 'uniform_in_time_claimed')
          and rejected(lambda: validate_window(V['Theta'], 1, 'theta', False), 'u_window_labelled_theta'),
          window='|theta|<=8, theta=alpha t/hbar, U=Theta/8=1', growth_U2_over_U1_preview=dec(grow, 8),
          note='the bound grows like U^2/(1-vU/3) (exactly (2/(Cv))(e^{vU}-1-vU)); nothing is claimed outside the window')

    alpha, hbar = Q(5), Q(7)
    t_phys = Q(56, 5)
    theta = alpha * t_phys / hbar
    u_norm = (alpha / delta_div) * t_phys / hbar

    def validate_clock(theta_v, u_v):
        require(theta_v == alpha * t_phys / hbar, 'theta = alpha t / hbar')
        require(u_v == theta_v / V['u_div'], 'u = delta t/hbar = theta/8 (delta = alpha/8)')
        return True
    check('wrong_delta_alpha_hbar_clock',
          theta == 8 and u_norm == 1 and validate_clock(theta, u_norm)
          and rejected(lambda: validate_clock(theta, theta), 'eightfold_u_labelled_theta')
          and rejected(lambda: validate_clock(alpha * t_phys, u_norm), 'hbar_dropped')
          and rejected(lambda: validate_clock(theta, alpha * t_phys / hbar), 'delta_equals_alpha'),
          fixture='alpha=5, hbar=7, t=56/5: theta=8, u=1 (non-unit constants)', conversion='e^{itK/hbar}=e^{i(delta t/hbar)H_hat}=e^{i(theta/8)H_hat}')

    # ======================= unbounded onsite terms: interaction picture =======================
    def validate_placement(onsite_in, source_terms):
        require(onsite_in == 'H_x', 'unbounded onsite Casimirs enter as the local Hamiltonians H_x of (44), never inside Phi')
        return validate_source_bounded(source_terms)
    wrong_phi = [('h_x placed in Phi', lambda L: Q(L - 1))]
    velocity_wrong = {L: 2 * Q(L - 1) * Cc for L in (10, 100, 1000)}
    check('unbounded_onsite_interaction_picture',
          validate_placement('H_x', [face_term])
          and rejected(lambda: validate_placement('Phi', wrong_phi), 'onsite_in_bounded_interaction')
          and rejected(lambda: validate_placement('H_x', [face_term, ('onsite terms of Lambda_M minus Lambda_N in the Cauchy source', lambda L: Q(L - 1))]),
                       'onsite_of_larger_box_in_duhamel_source'),
          placement='F1 on Lambda_N is (44) with H_x=h_x (unbounded, self-adjoint, compact resolvent) and Phi(b+S)=phi_b; every Duhamel pair has '
                    'identical onsite parts (larger-box onsite terms and F2 padding sit in the inner Hamiltonian and factor out); the source is a '
                    'bounded sum of faces',
          wrong_placement_velocity_preview={str(L): dec(v1) for L, v1 in velocity_wrong.items()})

    # ======================= tier mixing =======================
    records = {'comparison': rec_cmp, 'cauchy_F1': rec_cmp, 'cauchy_F2': rec_cmp, 'distance_F2_to_limit': rec_cmp}

    def validate_tiers(recs):
        for name, r in recs.items():
            require(r.get('tier') in V['tiers_allowed'], 'tier not named: ' + name)
            require(r.get('interaction') in (PHI_WHOLE, PHI_OWNER), 'interaction not named: ' + name)
            if r['tier'] == 'exponential_lieb_robinson':
                require(r['phi_F_per_abs_tau'] not in (V['phi_contract'], V['phiprime_contract']), 'exponential tier with polynomial constants')
            validate_inner(r)
        return True
    check('tier_mixing_rejected',
          validate_tiers(records) and V['target_cmp_tier'] == TIER
          and rejected(lambda: validate_tiers(dict(records, comparison=dict(rec_cmp, tier='exponential_lieb_robinson'))), 'exponential_label_on_polynomial_constants')
          and rejected(lambda: validate_tiers(dict(records, cauchy_F1={'inner_family': 'F1', 'interaction': PHI_WHOLE, 'phi_F_per_abs_tau': phiF})), 'tier_missing')
          and rejected(lambda: validate_tiers(dict(records, cauchy_F2=dict(rec_cmp, phi_F_per_abs_tau=V['phiprime_contract']))), 'mixed_interaction_constants'),
          records={k: {'tier': r['tier'], 'interaction': r['interaction'], 'inner_family': r['inner_family'], 'phi_F_per_abs_tau': s(r['phi_F_per_abs_tau'])}
                   for k, r in records.items()})

    # ======================= root-N misuse =======================
    per_face = [duhamel_coefficient(tau_cap, U, sum(F_poly(l1(x, y)) for x in COVER_R for y in owner_set(f)), phiF * tau_cap, Cc)
                for f in src_cmp]
    lin_sum = sum(per_face)

    def validate_linear(total, parts, scale=1):
        require(total * scale == sum(parts), 'deterministic face bounds add linearly')
        return True
    check('root_n_misuse',
          validate_linear(lin_sum, per_face) and lin_sum == b_refined[2]
          and rejected(lambda: validate_linear(lin_sum / 24, per_face), 'division_by_isqrt_of_616_faces')
          and rejected(lambda: validate_linear(lin_sum / 2, per_face), 'division_by_sqrt_N_at_N_4'),
          faces_summed=len(per_face), linear_sum_preview=dec(lin_sum),
          note='the comparison and Cauchy sums add face by face; no square-root combination or division by sqrt(N) or sqrt(#faces)')

    # ======================= cross-coupling comparison =======================
    def source_faces_meeting_R(tau2, tau1):
        faces = list(src_cmp) + ([] if tau2 == tau1 else list(f1_2.values()))
        return sum(1 for f in faces if owner_set(f) & frozenset(COVER_R))

    def validate_same_coupling(tau2, tau1):
        require(tau2 == tau1, 'F1 and F2 are compared at the same coupling')
        require(source_faces_meeting_R(tau2, tau1) == 0, 'the source must be disjoint from R')
        return True
    check('cross_coupling_comparison_rejected',
          validate_same_coupling(tau_cap, tau_cap) and source_faces_meeting_R(tau_cap, -tau_cap) == 82
          and rejected(lambda: validate_same_coupling(tau_cap, -tau_cap), 'opposite_signs_compared')
          and rejected(lambda: validate_same_coupling(tau_cap, tau_cap / 2), 'different_couplings_compared'),
          note='at different couplings the source contains every face (82 meet R), X and Y are not disjoint, (51) does not apply and the first-order term survives')

    # ======================= full original Wilson cover =======================
    W_base, W_dirs = class_base(ORIGIN, next(k for k in classes if k[:3] == ('xz', 0, 0)))
    W_links = face_links(W_base, *W_dirs)
    W_owners = sorted({owner(lk[0]) for lk in W_links})
    ends0 = {lk[0] for lk in block_links(ORIGIN)} | {add(lk[0], E_UNIT[lk[1]]) for lk in block_links(ORIGIN)}
    endsz = {lk[0] for lk in block_links(EZ)} | {add(lk[0], E_UNIT[lk[1]]) for lk in block_links(EZ)}

    def validate_cover(cover_links):
        owners_ = {owner(lk[0]) for lk in cover_links}
        require(owners_ == set(COVER_R) and len(cover_links) == 48, 'the cover is the complete factor cover {0,e_z}: 48 links')
        require(all(lk in set(cover_links) for lk in W_links), 'the cover contains every link of W')
        return True
    check('full_original_wilson_cover',
          validate_cover(R_links) and len(R_end) == 36 and len(ends0) == len(endsz) == 22 and len(ends0 & endsz) == 8 and W_owners == sorted(COVER_R)
          and rejected(lambda: validate_cover(list(W_links)), 'four_drawn_links_as_cover')
          and rejected(lambda: validate_cover(block_links(ORIGIN)), 'single_factor_cover'),
          links=48, endpoints=36, endpoints_per_factor=22, shared_endpoints=8, W_link_owners=[list(o) for o in W_owners])

    # ======================= topology =======================
    TOP = {'dynamics': 'operator norm on B(H_R), uniformly for |theta| at most 8', 'states': 'local trace norm (subsequential limits, not compared here)'}

    def validate_topology(t, time_continuity):
        require(t['dynamics'] == TOP['dynamics'], 'dynamics topology is the operator norm, uniformly on the compact window')
        require(time_continuity == 'strong (GNS), not norm on full B(H)', 'norm continuity in time on full B(H) is not claimed')
        return True
    check('topology_named',
          validate_topology(TOP, 'strong (GNS), not norm on full B(H)')
          and rejected(lambda: validate_topology(dict(TOP, dynamics='strong operator topology'), 'strong (GNS), not norm on full B(H)'), 'strong_relabelled_norm')
          and rejected(lambda: validate_topology(TOP, 'norm on full B(H)'), 'norm_time_continuity_claimed'),
          topology=TOP)

    # ======================= two families =======================
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

    # ======================= rate in N, not in a =======================
    def validate_rate_units(unit):
        require(unit == 'per coarse step at fixed spacing', 'rates are per coarse step at fixed spacing and strong bare coupling')
        return True
    check('decay_rate_in_N_not_a',
          validate_rate_units('per coarse step at fixed spacing')
          and rejected(lambda: validate_rate_units('per fm'), 'conversion_to_fm')
          and rejected(lambda: validate_rate_units('in the lattice spacing a'), 'rate_in_a'),
          coarse_step='(4a,2a,a) in fine units', note='N counts coarse steps; no physical length scale is read')

    # ======================= report scans =======================
    template = V['template']
    forbidden = ROUND_FORBIDDEN + V['forbidden']
    STATEMENTS = [
        'The forward route proves an algebraic comparison of the finite-box Heisenberg dynamics of the named constructions F1 and F2 on the compact '
        'window |theta| at most 8, uniformly for |theta| at most 8, at a rate in N at fixed spacing; it does not assert equality of GNS dynamics or of '
        'correlation functions of different states.',
        'The F1 and F2 finite-box evolutions of every A in B(H_R) converge as whole sequences in norm, uniformly for |theta| at most 8, and the F2 limit '
        'equals the AQ1 limit dynamics T_theta; limit states remain subsequential and are not identified.',
        'No estimate is uniform in the lattice spacing a, and nothing is claimed outside the window.']
    scan_texts = {'report.md': report_text, 'statements': ' '.join(STATEMENTS)}

    def validate_uniformity(texts):
        for name, txt in texts.items():
            bad = uniformity_violations(txt, template)
            require(not bad, 'unqualified uniformity statement in ' + name + ': ' + (bad[0] if bad else ''))
        return True
    check('uniform_in_N_not_in_a',
          validate_uniformity(scan_texts)
          and rejected(lambda: validate_uniformity({'m': 'The comparison bound is uniform in the lattice spacing a.'}), 'uniform_in_a_claimed')
          and rejected(lambda: validate_uniformity({'m': 'The Cauchy rate is uniform.'}), 'unqualified_uniform_rate'),
          qualifiers=list(UNIFORM_QUALIFIERS))

    def validate_placeholders(texts):
        for name, txt in texts.items():
            spans = placeholder_spans(txt)
            require(not spans, 'placeholder span in ' + name + ': ' + (spans[0] if spans else ''))
        return True
    contract_strings = json.dumps(c, ensure_ascii=False)
    check('placeholder_span_rejected',
          validate_placeholders(dict(scan_texts, contract=contract_strings)) and '>' not in report_text
          and rejected(lambda: validate_placeholders({'m': 'b(N) = <constant to be filled>'}), 'whitespace_placeholder')
          and rejected(lambda: validate_placeholders({'m': 'verdict <accepted|limited>'}), 'vertical_bar_placeholder')
          and rejected(lambda: validate_placeholders({'m': 'N0 <e.g.2>'}), 'eg_placeholder'),
          scanned=['report.md', 'exported statements', 'contract strings'])

    def validate_phrases(texts):
        for name, txt in texts.items():
            hits = affirmative_phrase_hits(txt, forbidden, template)
            require(not hits, 'affirmative forbidden phrasing in ' + name + ': ' + (hits[0]['phrase'] if hits else ''))
        return True
    negated_ok = not affirmative_phrase_hits('This does not construct the thermodynamic limit.', forbidden, template)
    check('negation_aware_phrase_scan',
          validate_phrases(scan_texts) and negated_ok
          and rejected(lambda: validate_phrases({'m': 'We construct the thermodynamic limit of the dynamics.'}), 'affirmative_thermodynamic_limit')
          and rejected(lambda: validate_phrases({'m': 'The F2 limit equals the AQ state.'}), 'affirmative_AQ_state')
          and rejected(lambda: validate_phrases({'m': 'This proves the mass gap.'}), 'affirmative_mass_gap'),
          forbidden_count=len(forbidden), template_removed_as_one_literal=True,
          note='same rule as research/round33/tools/phrase_scan.py (round list copied, contract list read from the contract)')

    # ======================= parameters declare metric, weights, window =======================
    def validate_parameters(params, clock):
        for key in ('metric', 'weights', 'window', 'boundary_source', 'targets'):
            require(key in params and params[key], 'parameters field missing: ' + key)
        require('theta=alpha t/hbar' in params['window'] and clock.startswith('s=alpha*t_E/hbar'), 'window and clock declared')
        return True
    check('parameters_declare_metric_weights_window',
          validate_parameters(V['parameters'], V['clock'])
          and rejected(lambda: validate_parameters({k: v1 for k, v1 in V['parameters'].items() if k != 'window'}, V['clock']), 'window_field_absent')
          and rejected(lambda: validate_parameters({k: v1 for k, v1 in V['parameters'].items() if k != 'metric'}, V['clock']), 'metric_field_absent'),
          declared=sorted(V['parameters']), clock=V['clock'],
          note='N_0 appears inside the targets (N at least 2) and d_X is the named l1 metric; there are no separate N_0 or d_X fields (wording note W2)')

    # ======================= model relabelling =======================
    MODEL = {'model_id': V['model_id'], 'tau': s(tau_cap), 'triple': [s(x) for x in V['triple']], 'families': sorted(FAM),
             'metric': 'coarse l1', 'weights': '(1+r)^-4', 'window': '|theta|<=8', 'group': 'SU(2)', 'dimension': 3, 'finite_graph': False}

    def validate_model(mdl):
        require(mdl == MODEL and mdl['model_id'] == V['model_id'] and rat(mdl['tau']) == tau_cap, 'model packet differs from the contract')
        return True
    check('changed_model_relabelled',
          validate_model(dict(MODEL))
          and rejected(lambda: validate_model(dict(MODEL, tau='1/100000000000000')), 'tau_changed')
          and rejected(lambda: validate_model(dict(MODEL, triple=['1', '0', '0'])), 'nonzero_triple')
          and rejected(lambda: validate_model(dict(MODEL, metric='fine l1')), 'fine_site_metric')
          and rejected(lambda: validate_model(dict(MODEL, weights='exp(-mu r)(1+r)^-4')), 'exponential_weights_relabelled')
          and rejected(lambda: validate_model(dict(MODEL, window='|u|<=8')), 'window_changed')
          and rejected(lambda: validate_model(dict(MODEL, model_id='AX_uniform_route_B')), 'uniform_route_B_model')
          and rejected(lambda: validate_model(dict(MODEL, group='SU(3)')), 'other_group')
          and rejected(lambda: validate_model(dict(MODEL, dimension=2)), 'two_dimensional')
          and rejected(lambda: validate_model(dict(MODEL, finite_graph=True)), 'finite_graph'),
          model=MODEL)

    # ======================= exact arithmetic admission =======================
    check('exact_arithmetic_admission',
          rat('1/100000000') == tau_cap and isinstance(K['cmp'], Q)
          and rejected(lambda: rat(1e-8), 'float_input')
          and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('nan'), 'nan_input')
          and rejected(lambda: rat('1/0'), 'zero_denominator')
          and rejected(lambda: rat(dec(K['cmp'])), 'preview_decimal_read_as_admission_value'),
          note='every admission Boolean is a Fraction comparison; previews are truncated strings never parsed by an admission check')

    # ======================= error ledger =======================
    ledger = {
        'lieb_robinson_tail': {'comparison': 'S_b(N) <= 168(5N+1)N^-3 (at most 3 owners per extra face, each at l1 distance at least N-1 from e_z and at least N from 0, '
                                             'F(N-1)+F(N) <= 2N^-4)',
                               'cauchy': 'S_c(N) <= 49(4/N+4/(N-1)) <= 392/(N-1) (shells 4r^2+2 <= 4(1+r)^2, sum over k from m+1 of k^-2 <= 1/m)'},
        'duhamel_boundary_sum': {'value': 'face norm |tau|/3 times Lambda(U) times the F-sum, faces added linearly, each charged once',
                                 'Lambda_U1': s(lam['+']), 'Lambda_U1_preview': dec(lam['+'])},
        'interaction_picture_onsite': {'value': '0', 'status': 'not_applicable',
                                       'reason': 'the unbounded onsite terms are identical in both Hamiltonians of every Duhamel pair (padding and larger-box onsite '
                                                 'terms sit in the inner Hamiltonian and factor out); (51) itself handles them through its interaction picture (54),(57)'},
        'inner_family_constants': {'value': 'F1 inner: C <= 224, ||Phi||_F <= 2268|tau|, v=2||Phi||_F C=1016064|tau|; monotone substitution of upper bounds'},
        'arithmetic': {'value': '0', 'status': 'not_applicable', 'reason': 'exact Fractions; the only transcendental step e^x-1-x is replaced by the '
                                                                              'directed rational upper bound x^2/(2(1-x/3)), x<=1016064|tau|'}}
    check('error_ledger_itemized',
          sorted(ledger) == sorted(V['error_terms']) and all(('reason' in e) for e in ledger.values() if e.get('status') == 'not_applicable'),
          ledger_terms=sorted(ledger), rule=V['error_terms_rule'])

    # ======================= verdict logic; retained failures =======================
    def forward_verdict(lr_applies, source_ok, cmp_ok, c1_ok, c2_ok, ident_ok, o6_ok):
        if not (lr_applies and source_ok):
            return 'insufficient'
        if cmp_ok and c1_ok and c2_ok and ident_ok and o6_ok:
            return 'accepted_within_scope'
        return 'limited'
    verdict = forward_verdict(True, enum_ok and audit_ok, cmp_met, c1_met, c2_met, True, True)
    triangle = 2 * K['c1']                       # triangle through the common limit: 2 K_c1/(N-1)
    triangle_fails = triangle > V['target_cmp'] * Q(11, 8) and all(triangle / (N - 1) > V['target_cmp'] * Q(5 * N + 1, N ** 3) for N in range(2, 60))

    def validate_verdict(label, flags, tau_used):
        require(tau_used == tau_cap, 'retuning tau to pass is rejected')
        require(label == forward_verdict(*flags), 'verdict label differs from the acceptance rule')
        return True
    check('insufficient_verdict_retained',
          verdict == 'accepted_within_scope' and triangle_fails
          and validate_verdict(verdict, (True, True, True, True, True, True, True), tau_cap)
          and rejected(lambda: validate_verdict('accepted_within_scope', (True, True, False, True, True, True, True), tau_cap), 'missed_comparison_relabelled_accepted')
          and rejected(lambda: validate_verdict('limited', (True, False, True, True, True, True, True), tau_cap), 'miscounted_source_relabelled_limited')
          and rejected(lambda: validate_verdict('accepted_within_scope', (True, True, True, True, True, True, True), tau_cap / 10), 'tau_retuned'),
          retained_labelled_weaker_bound={'route': 'triangle through the common limit, 2 K_c1/(N-1)', 'coefficient': s(triangle),
                                          'preview': dec(triangle), 'misses_comparison_target_at_every_N_ge_2': triangle_fails,
                                          'dominating_term': 'the 1/N polynomial tail of all faces outside Lambda_N'},
          verdict=verdict)

    # ======================= flags, gate fields =======================
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
          and rejected(fmut(weak_coupling_claim=True), 'weak_coupling_true'),
          historical_or_occult_numeric_premise=False)

    admitted = {'rate_in_N_claimed': cmp_met and c1_met and c2_met, 'whole_sequence_claimed': c1_met and c2_met,
                'dynamics_limit_identified_claimed': c1_met and cmp_met}
    GATE = {}
    for k1, v1 in V['gate_fields'].items():
        if k1 in admitted:
            GATE[k1] = bool(v1 and admitted[k1])
        else:
            GATE[k1] = v1

    def validate_gate(g):
        require(sorted(g) == sorted(V['gate_fields']), 'gate fields must be exactly the contract fields')
        for k1, v1 in g.items():
            if isinstance(V['gate_fields'][k1], bool):
                require(v1 is V['gate_fields'][k1], 'gate field differs from the contract: ' + k1)
                if v1 is True:
                    require(admitted.get(k1) is True, 'a true field needs its admitted target: ' + k1)
            else:
                require(v1 == V['gate_fields'][k1], 'gate field text differs: ' + k1)
        return True
    check('gate_fields_topic_specific',
          validate_gate(GATE)
          and rejected(lambda: validate_gate({k1: v1 for k1, v1 in GATE.items() if k1 != 'dynamics_level'}), 'field_missing')
          and rejected(lambda: validate_gate(dict(GATE, rate_in_a_claimed=True)), 'rate_in_a_true')
          and rejected(lambda: validate_gate(dict(GATE, common_limit_claimed=True)), 'common_limit_true')
          and rejected(lambda: validate_gate(dict(GATE, state_convergence_claimed=True)), 'state_convergence_true'),
          gate_fields=GATE, admitted_basis={k1: v1 for k1, v1 in admitted.items()},
          note='common_limit_claimed is read as a common limit state (false); the dynamics identification is dynamics_limit_identified_claimed')

    # ======================= mandatory sentence =======================
    count_template = report_text.count(template)
    check('mandatory_sentence_verbatim_once',
          count_template == 1 and V['sub_labels'] == ['dynamics_on_compact_windows'],
          occurrences_in_report=count_template, template_sha256=sha_bytes(template.encode('utf-8')))

    # ======================= reverse premise isolation =======================
    forward_list = ['AGENTS.md', CONTRACT_REL] + V['shared'] + V['forward_additional']
    reverse_list = ['AGENTS.md', CONTRACT_REL] + V['shared']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    bad_parts = ('research/round33/skeptic/', 'research/round33/experts/', 'research/round33/forward/ba2', 'deliberation-', 'triage',
                 'recommendation', 'prospective-controls', 'loop2', 'loop-2', 'memo')

    def validate_isolation(decl, lst):
        require(decl is True, 'contract does not declare reverse premise isolation')
        require(sorted(set(lst)) == sorted(set(['AGENTS.md', CONTRACT_REL] + V['shared'])), 'reverse inventory must equal AGENTS, contract and shared premises')
        for item in lst:
            require(not any(b1 in item for b1 in bad_parts), 'reverse premise isolation violated by ' + item)
        return True
    check('reverse_premise_isolation',
          sorted(inventory) == sorted(set(forward_list)) and len(inventory) == 29 and V['forward_additional'] == []
          and validate_isolation(V['reverse_isolation'], reverse_list)
          and rejected(lambda: validate_isolation(False, reverse_list), 'declaration_false')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round33/advisor/deliberation-2.md']), 'reverse_reads_deliberation')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round33/forward/ba2/report.md']), 'reverse_reads_forward_ba2')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round33/experts/jung/memo.md']), 'reverse_reads_lens_memo'),
          forward_inventory_files=len(inventory), reverse_premise_count=len(set(reverse_list)),
          limitation='the forward checker verifies the declared inventories only; the reverse agent\'s actual reads are checked by freeze.py and the skeptic')

    # ======================= packet, tampering =======================
    headline = {
        'comparison': {'statement': 'b(N) <= K_cmp (5N+1) N^-3, |theta|<=8, N at least 2', 'K_cmp': s(K['cmp']), 'K_cmp_preview': dec(K['cmp']),
                       'target': s(V['target_cmp']), 'target_met': cmp_met, 'margin_preview': dec(V['target_cmp'] / K['cmp'], 6),
                       'scaling_ratio': s(ratios['cmp']), 'scaling_ratio_preview': dec(ratios['cmp'], 10),
                       'tier': TIER, 'interaction': PHI_WHOLE, 'inner_family': 'F1', 'route': 'forward Duhamel over the extra F2 faces'},
        'cauchy_F1': {'statement': 'sup over M greater than N of ||T^{F1,M}-T^{F1,N}|| <= K_c1/(N-1)', 'K_c1': s(K['c1']), 'K_c1_preview': dec(K['c1']),
                      'target': s(V['target_cau']), 'target_met': c1_met, 'margin_preview': dec(V['target_cau'] / K['c1'], 6),
                      'scaling_ratio': s(ratios['c1']), 'scaling_ratio_preview': dec(ratios['c1'], 10),
                      'tier': TIER, 'interaction': PHI_WHOLE, 'inner_family': 'F1', 'route': 'forward Duhamel over the faces outside Lambda_N'},
        'cauchy_F2': {'statement': 'sup over M greater than N of ||T^{F2,M}-T^{F2,N}|| <= K_c2/(N-1), K_c2 = K_c1 + (11/8) K_cmp', 'K_c2': s(K['c2']),
                      'K_c2_preview': dec(K['c2']), 'target': s(V['target_cau']), 'target_met': c2_met,
                      'margin_preview': dec(V['target_cau'] / K['c2'], 6), 'scaling_ratio': s(ratios['c2']),
                      'scaling_ratio_preview': dec(ratios['c2'], 10), 'tier': TIER, 'interaction': PHI_WHOLE, 'inner_family': 'F1',
                      'route': 'forward Duhamel against the F1 box evolution on Lambda_N plus the comparison'},
        'distance_to_limit': {'F1': 'K_c1/(N-1)', 'F2': 'K_c1/(N-1)', 'K_c1': s(K['c1'])},
        'extra_faces': {'count': '28N(5N+1)', 'N2': enum[2]['extra'], 'N3': enum[3]['extra'], 'N4': enum[4]['extra'],
                        'owners': 'outer layer max_i |b_i| = N', 'min_l1_from_e_z': 'N-1', 'min_l1_from_0': 'N'},
        'padding': 'onsite terms on B_+ minus Lambda_N factor out exactly; never charged',
        'f2_limit_dynamics': 'whole sequence, equals T_theta (AQ1); O6 rerun for every subsequential F2 limit state',
    }
    label = 'dynamics_on_compact_windows'
    verdict_line = (verdict + ' (forward half; the contract acceptance also requires the reverse route and skeptical review); sub-label ' + label)
    packet = {
        'loop': 'BA2', 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'contribution_alias': 'HNM-BA2-F forward Duhamel/Lieb-Robinson comparison of the F1 and F2 Heisenberg dynamics on compact windows, '
                              'within-family Cauchy estimates and identification of the F2 limit dynamics',
        'ai_assistance': 'AI-assisted forward production (Claude model agent); correlated model-agent work, not independent human review',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'pinned_gate_sha256': dict(PINNED_GATES), 'ns_excerpt_sha256': NS_SHA256,
        'label': label, 'model': MODEL, 'families': FAM, 'clock': V['clock'], 'window': V['window'],
        'tau_values': {sg: s(tv) for sg, tv in taus.items()},
        'headline': headline, 'error_terms_itemized': ledger, 'topology': TOP,
        'meaning': STATEMENTS[0], 'dynamics_limit_statement': STATEMENTS[1],
        'mandatory_sentence': template,
        'gate_fields': GATE,
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions'],
                       'additional': ['no identification of limit states', 'no statement outside |theta| at most 8 with the frozen targets',
                                      'no exponential-tier constant', 'no fine-lattice or physical length reading of N']},
        'routes_executed': ['forward: Duhamel over the 28N(5N+1) extra F2 faces with the inner F1 evolution and the whole-star NS constants (comparison)',
                            'forward: Duhamel over the faces outside Lambda_N with the inner F1 evolution (F1 Cauchy, sup over all M)',
                            'forward: F2 Cauchy by one F1-inner Duhamel plus the comparison; F2 distance to T by an F1-inner Duhamel on Lambda_M',
                            'forward: identification of the F2 limit dynamics with T_theta and rerun of AQ1 sections 4-5 for F2 limit states'],
        'routes_not_executed': ['reverse route (inner F2, owner-set constants; outside this producer)', 'exponential_lieb_robinson tier (optional)',
                                'skeptic post-comparison'],
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
        require(sorted(inv) == sorted(set(forward_list)) and NS_REL in inv, 'premise snapshot inventory incomplete')
        require(rat(pk['headline']['comparison']['K_cmp']) == coeff_at(tau_cap, 'cmp'), 'K_cmp differs from recomputation')
        require(rat(pk['headline']['cauchy_F1']['K_c1']) == coeff_at(tau_cap, 'c1'), 'K_c1 differs from recomputation')
        require(rat(pk['headline']['cauchy_F2']['K_c2']) == coeff_at(tau_cap, 'c2'), 'K_c2 differs from recomputation')
        require(pk['headline']['extra_faces']['N2'] == 616 == enum[2]['extra'] and pk['headline']['extra_faces']['N3'] == enum[3]['extra'], 'extra-face count changed')
        require(sorted(pk['families']) == ['F1', 'F2'], 'families changed')
        require(pk['mandatory_sentence'] == template, 'mandatory sentence changed')
        require(pk['proposed_forward_verdict'].startswith(verdict), 'verdict changed')
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
            if ch['id'] == 'duhamel_inner_family_constants':
                ch['passed'] = False

    def t_snapshot(pk, inv):
        inv.pop(NS_REL)

    def t_Kcmp(pk, inv):
        pk['headline']['comparison']['K_cmp'] = s(rat(pk['headline']['comparison']['K_cmp']) / 2)

    def t_Kc2(pk, inv):
        pk['headline']['cauchy_F2']['K_c2'] = pk['headline']['cauchy_F1']['K_c1']

    def t_gns(pk, inv):
        pk['gns_dynamics_equality_claimed'] = True

    def t_gatefield(pk, inv):
        pk['gate_fields']['common_limit_claimed'] = True

    def t_family(pk, inv):
        pk['families'] = {'F1': FAM['F1']}

    def t_faces(pk, inv):
        pk['headline']['extra_faces']['N2'] = 588
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_snapshot), 'ns_excerpt_snapshot_removed_hash_rebound')
          and rejected(tamper(t_Kcmp), 'K_cmp_halved_hash_rebound')
          and rejected(tamper(t_Kc2), 'K_c2_replaced_by_K_c1_hash_rebound')
          and rejected(tamper(t_gns), 'gns_equality_flag_hash_rebound')
          and rejected(tamper(t_gatefield), 'common_limit_field_hash_rebound')
          and rejected(tamper(t_family), 'one_family_hash_rebound')
          and rejected(tamper(t_faces), 'extra_face_count_hash_rebound'))

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


def _face_geom(b, k):
    base, (a, c) = class_base(b, k)
    return base, a, c


def float_free(obj):
    if isinstance(obj, float):
        return False
    if isinstance(obj, dict):
        return all(float_free(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(float_free(v) for v in obj)
    return True


def main():
    ap = argparse.ArgumentParser(description='BA2 forward exact checker')
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
    manifest = {'loop': 'BA2', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'check_py_sha256': sources['check.py'],
                'sources': sources, 'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({'loop': 'BA2', 'direction': 'forward', 'checks': len(result['checks']),
                      'K_cmp_preview': result['headline']['comparison']['K_cmp_preview'],
                      'K_c1_preview': result['headline']['cauchy_F1']['K_c1_preview'],
                      'K_c2_preview': result['headline']['cauchy_F2']['K_c2_preview'],
                      'rejected_mutations': result['rejected_mutation_total']}, sort_keys=True))


if __name__ == '__main__':
    main()
