#!/usr/bin/env python3
"""BB1 forward producer (route polymer_kp): exact checks for the locality of the reduced
densities of the named construction families F1 and F2 (zero-selected patterned family)
at the frozen rate q=1/64 in N, from the BA1 coefficient differences at every site.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production (a Claude
model agent); correlated model-agent work, not independent human review and not formal
verification.

Route: hard-core polymer representation of the norm and of the Y-marginal (Y-clusters),
activity bound by the product of creation norms, exploration-tree majorant, a new
mixed-weight contraction lemma (weight w^{diam I} e^{b|I|}, loss w e^{4b} per interaction),
the Kotecky-Preiss condition with an explicit parameter a, truncated vacuum probabilities,
and the real-parameter derivative along c + lambda (c' - c).  The every-site coefficient
input is form (b) of the contract (the BA1 reverse disc theorem restated for every site u),
proved in full in report.md section 8 and audited here.

Standard library only.  Every admission Boolean is decided in exact Fraction arithmetic with
directed (upward) enclosures; decimal strings are truncated previews and never admission
values.  Conditions raise AdmissionError explicitly (never `assert`), so every check stays
active under `python -O`.

Usage: python3 -B check.py --output /absolute/fresh/non-existent/directory
"""
import argparse
import hashlib
import itertools
import json
import re
from fractions import Fraction as Q
from math import factorial
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round33/contracts/bb1.json'
CONTRACT_SHA256 = '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'

P_AM2_GATE = 'research/round29/advisor/am2-gate.json'
P_AQ1_GATE = 'research/round29/advisor/aq1-gate.json'
P_AV1_GATE = 'research/round32/advisor/av1-gate.json'
P_AW1_GATE = 'research/round32/advisor/aw1-gate.json'
P_AY1_GATE = 'research/round32/advisor/ay1-gate.json'
P_AY2_GATE = 'research/round32/advisor/ay2-gate.json'
P_BA1_GATE = 'research/round33/advisor/ba1-gate.json'
P_BA2_GATE = 'research/round33/advisor/ba2-gate.json'
P_SEL = 'research/round33/advisor/selection-bb1.md'
P_I1 = 'research/round21/forward/i1/report.md'
P_AM2 = 'research/round29/forward/am2/report.md'
P_AV1F = 'research/round32/forward/av1/report.md'
P_AY1F = 'research/round32/forward/ay1/report.md'
P_BA1F = 'research/round33/forward/ba1/report.md'
P_BA1R = 'research/round33/reverse/ba1/report.md'

# sha256 of every admitted gate and of every report from which a constant is parsed, pinned
# before any evaluation (preregistration.hash_binding.admitted_gate_sha256_pinned_in_check_py).
PINNED = {
    P_AM2_GATE: 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    P_AQ1_GATE: 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    P_AV1_GATE: '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    P_AW1_GATE: '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    P_AY1_GATE: 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    P_AY2_GATE: 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    P_BA1_GATE: '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc',
    P_BA2_GATE: 'e6b163fc8f80de28c51609f77d0bef21dcdc1286638c862ad67202e6f7b0ca35',
    P_SEL: 'dd6057b59020e0bbb6cb29e046037a60b0d4c2dd538dd3af9800d8644af5236c',
    P_I1: '836a4c7d421f0ddf3589c159d2f057839421532c88157a054a61b51c25c781a9',
    P_AM2: '1b58fb9c1a199f06b156d04c2a9e89f34ba63cf675a5f7c8bfc25bb568e4e019',
    P_AV1F: '7f86e941933913584de2b9e542359e4a3b3c275c1bc8623dca3c367d88437353',
    P_AY1F: '7cb1e844d75ee1f3d69de2bccb9a684c791e34bf64f3bb9e2d5061221f75dac1',
    P_BA1F: 'd8ed5bfa780b95a57e5ba822b81f0fea5f71aaa7ea1a01bb4dbecb0d417aa769',
    P_BA1R: 'a986c205542376c2ad5058cdf88e082abe9c12eeba87b052abf3ad9cefebbb86',
}

# Round33 forbidden-phrase list (copied from the shared infrastructure tool
# research/round33/tools/phrase_scan.py; it carries no scientific content).
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
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value.strip()):
        num, _, den = value.strip().partition('/')
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


def input_bytes(rel):
    return (BASE / 'inputs' / rel).read_bytes()


def read_input(rel):
    return input_bytes(rel).decode('utf-8')


def match(pattern, text, label, flags=0):
    m = re.search(pattern, text, flags)
    require(m is not None, 'text not parsed: ' + label)
    return m


def contains(text, token, label):
    require(token in text, 'text lacks ' + label + ': ' + token[:80])
    return True


# ---------------------------------------------------------------------------
# Text scans (negation-aware phrase scan, placeholder spans, uniformity qualifiers).
# ---------------------------------------------------------------------------
def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def clauses(text):
    return [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', text) if c.strip()]


def phrase_hits(text, forbidden, template):
    body = normalize(text)
    if template:
        body = body.replace(normalize(template), ' ')
    hits = []
    for clause in clauses(body):
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                hits.append({'phrase': phrase, 'clause': clause[:200], 'negated': bool(NEGATION.search(clause))})
    return hits


def require_no_affirmative(text, forbidden, template, label):
    bad = [h for h in phrase_hits(text, forbidden, template) if not h['negated']]
    require(not bad, 'affirmative forbidden phrase in ' + label + ': ' + json.dumps(bad[:2]))
    return True


def require_no_placeholder(text, template, label):
    body = str(text)
    if template:
        body = body.replace(template, ' ')
    for inner in re.findall(r'<([^<>]*)>', body):
        require(not (re.search(r'\s', inner) or '|' in inner or 'e.g.' in inner),
                'placeholder angle-bracket span in ' + label + ': ' + inner[:60])
    return True


UNIFORM_QUALIFIERS = ('in N at fixed spacing', 'at fixed spacing', 'in the cutoff', 'cutoff', 'in L,', 'in L ')


def require_uniformity_qualified(text, template, label):
    body = normalize(text)
    if template:
        body = body.replace(normalize(template), ' ')
    body = re.sub(r'`[^`]*`', ' ', body)   # code spans quote ids or verbatim contract text, not statements
    for sentence in re.split(r'(?<=[.!?])\s+', body):
        if re.search(r'\buniform', sentence, re.I):
            ok = any(qf in sentence for qf in UNIFORM_QUALIFIERS)
            ok = ok or ('lattice spacing' in sentence and NEGATION.search(sentence) is not None)
            require(ok, 'unqualified uniformity statement in ' + label + ': ' + sentence[:160])
    return True


def all_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k in sorted(obj):
            yield str(k)
            for x in all_strings(obj[k]):
                yield x
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            for x in all_strings(v):
                yield x


def float_free(obj):
    if isinstance(obj, float):
        return False
    if isinstance(obj, dict):
        return all(float_free(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(float_free(v) for v in obj)
    return True


# ---------------------------------------------------------------------------
# Contract: every target, bracket, parameter, template and control id is read from the
# sha256-bound snapshot.  The hash is verified before any evaluation.
# ---------------------------------------------------------------------------
def load_contract():
    raw = input_bytes(CONTRACT_REL)
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen BB1 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'BB1' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


def contract_values(c):
    p = c['parameters']
    pre = c['preregistration']
    sem = c['new_control_semantics']
    v = {'contract': c}
    v['model'] = c['model']
    for token in ('Zero-selected patterned family (AM2/AQ1), both signs |tau|<=10^-8',
                  'AM2 creation expansion in each on-site cutoff space',
                  'F1 (AQ1 centered whole-star boxes)', 'F2 (I1 section 6 all-contained-face boxes with padding)',
                  'centered coarse cubes Lambda_N, N at least 2', 'the cover R={0,e_z}', 'trace norm on B(H_Y)'):
        contains(v['model'], token, 'contract model')
    v['metric'] = p['metric']
    contains(p['metric'], 'coarse l-infinity metric on factor sites (star diameter 1)', 'metric')
    v['weights'] = p['weights']
    m = match(r'the BA1 diameter weight at w up to 1/\((\d+)\|tau\|\)', p['weights'], 'weights w_max')
    v['wmax_den'] = int(m.group(1))
    for token in ('forward (polymer_kp)', 'w^{diam I} e^{b|I|}', 'loss w e^{4b} per interaction', 'proved in full'):
        contains(p['weights'], token, 'weights')
    rcp = p['rate_constant_pair']
    v['rcp'] = rcp
    v['q_head'] = rat(rcp['headline']['q'])
    v['C_target'] = rat(rcp['headline']['C_target'])
    require(rcp['headline']['tier'] == 'exact_first_order', 'headline tier frozen as exact_first_order')
    contains(rcp['headline']['routes'], 'polymer_kp (forward)', 'headline routes')
    v['q_region'] = rat(rcp['region_form']['q'])
    require(v['q_region'] == v['q_head'], 'region form at the headline q')
    v['cs_target'] = rat(rcp['region_form']['c_site_target'])
    form = rcp['region_form']['form']
    contains(form, 'c_site |Y| e^{|Y|/10^8} q^{d_Y}', 'region form')
    contains(form, 'd_Y = N - max_{y in Y} |y|_inf (so d_R = N-1)', 'region exponent')
    v['region_rate'] = Q(1, 10 ** int(match(r'e\^\{\|Y\|/10\^(\d+)\}', form, 'region rate').group(1)))
    sec = rcp['secondary']
    v['q2_per_tau'] = rat(match(r'^(\d+)\|tau\| \(labelled secondary pair; the headline decides the loop\)', sec['q'], 'secondary q').group(1))
    v['C2_target'] = rat(sec['C_target'])
    v['cs2_target'] = rat(sec['c_site_target'])
    contains(sec['coefficient_input'], 'rho=|tau|/q_2 (1/' + str(v['q2_per_tau']) + ' at the cap)', 'secondary input radius')
    contains(rcp['crude_tier_reported'], 'never a target', 'crude tier')
    contains(rcp['floor_not_frozen'], 'is not a target for reduced densities', 'floor not frozen')
    v['comparisons'] = list(p['comparisons'])
    require(len(v['comparisons']) == 5, 'five comparisons')
    contains(v['comparisons'][2], 'F1 versus F2 on the same Lambda_N', 'fixed-N comparison')
    contains(v['comparisons'][3], 'compared directly, not by telescoping', 'general boxes directly')
    contains(v['comparisons'][4], 'a comparison of the reduced densities through the union costs a factor 2 and is labelled only', 'union labelled')
    v['cutoff'] = p['cutoff']
    contains(v['cutoff'], 'each on-site cutoff space Q_L, every L, constants uniform in L', 'cutoff')
    contains(v['cutoff'], 'the N and L limits are never exchanged', 'cutoff order')
    contains(v['cutoff'], 'AV1 cutoff-vector removal (F20-F23)', 'cutoff-vector removal')
    v['N_min'] = int(p['N_min'])
    v['window'] = p['window']
    require(v['window'].startswith('not applicable'), 'window parameter')
    v['clock_param'] = p['clock']
    v['coefficient_input'] = p['coefficient_input']
    contains(v['coefficient_input'], 'K=49/111790368 at q=1/64', 'coefficient input K')
    contains(v['coefficient_input'], 'form (b) is a BB1 lemma proved in full in each packet', 'form (b) status')
    contains(v['coefficient_input'], 'The BA1 gate admits the bound for u in R only', 'gate scope')
    v['parameters_keys'] = sorted(p)
    v['tau'] = rat(pre['tau']['value'])
    v['signs'] = list(pre['tau']['signs_evaluated'])
    require(v['signs'] == ['+', '-'], 'both signs required')
    require(pre['tau']['is_model_change_vs_previous_loop'] is False and pre['tau']['rule_if_chosen_later'] is None, 'tau rule')
    v['triple'] = [rat(x) for x in pre['selected_triple_alpha_units']]
    require(v['triple'] == [0, 0, 0], 'zero selected triple')
    v['model_id'] = pre['model_id']
    require(v['model_id'] == 'AQ_patterned_zero_selected', 'model id')
    v['clock'] = pre['clock']
    require(v['clock'].startswith('s=alpha*t_E/hbar (Euclidean), theta=alpha*t/hbar (real time); normalized u=theta/8'), 'clock')
    tg = pre['target']
    m = match(r'^(\d+/\d+) and (\d+/\d+)$', tg['value'], 'target values')
    require(rat(m.group(1)) == v['C_target'] and rat(m.group(2)) == v['cs_target'], 'targets equal the frozen pair')
    require(tg['comparator'] == '<=', 'target comparator')
    sb = pre['scaling_brackets_per_constant']
    m = match(r'^\[(\d+),(\d+)\]', sb['C_headline'], 'C bracket')
    v['bracket_C'] = (rat(m.group(1)), rat(m.group(2)))
    m = match(r'^\[(\d+),(\d+)\]', sb['c_site'], 'c_site bracket')
    v['bracket_cs'] = (rat(m.group(1)), rat(m.group(2)))
    m = match(r'^\[(\d+)/(\d+),(\d+)/(\d+)\]', sb['secondary_constants'], 'secondary bracket')
    v['bracket_sec'] = (Q(int(m.group(1)), int(m.group(2))), Q(int(m.group(3)), int(m.group(4))))
    v['bracket_q2'] = rat(match(r'^exactly (\d+)$', sb['q_secondary'], 'q secondary bracket').group(1))
    v['template'] = pre['mandatory_sentence_template']
    v['gate_fields'] = dict(pre['gate_fields_required'])
    v['forbidden'] = list(pre['forbidden_phrasings'])
    v['error_terms'] = list(pre['error_terms_itemized'])
    v['error_terms_rule'] = pre['error_terms_rule']
    v['tier_label_rule'] = pre['tier_label_rule']
    v['tier_names'] = list(pre['tier_names_allowed'])
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['outcomes'] = list(pre['expected_outcome_types'])
    v['hash_binding'] = dict(pre['hash_binding'])
    require(all(v['hash_binding'].values()), 'hash binding requirements')
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']), 'controls list equals the preregistered ids')
    require(set(sem) <= set(v['controls']), 'control semantics cover only contract controls')
    v['semantics'] = sem
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['acceptance'] = dict(c['acceptance'])
    v['shared'] = list(c['shared_premises'])
    require('forward_additional_premises' not in c, 'no forward-only premises declared for BB1')
    v['reverse_isolation'] = c['reverse_premise_isolation']
    v['required'] = list(c['required'])
    require(len(v['required']) == 6, 'six required items')
    gl = sem['global_lipschitz_not_decay']
    v['lip_map'] = rat(match(r"J_0G'\(R\) below (\d+/\d+)", gl, 'map Lipschitz').group(1))
    v['lip_excl'] = rat(match(r"2J_0G'\(R\) below (\d+/\d+) is AM2's exclusion constant", gl, 'exclusion constant').group(1))
    v['no_decay'] = rat(match(r'only by (\d+/\d+) with no decay', gl, 'no-decay bound').group(1))
    contains(sem['mixed_weight_lemma_proved'], 'citing BA1 for it is rejected', 'mixed lemma semantics')
    contains(sem['zero_free_region_required'], 'without a proved zero-free region', 'zero-free semantics')
    contains(sem['marginal_locality_constants_explicit'], 'kappa(I) at most kappa_0 (w\')^(-d_inf(I,Y)) p(|I|)', 'lemma form')
    return v


# ---------------------------------------------------------------------------
# Admitted premises: every gate and parsed report is sha256-pinned; constants are parsed.
# ---------------------------------------------------------------------------
def load_premises():
    got = {}
    for rel, dig in sorted(PINNED.items()):
        h = sha_bytes(input_bytes(rel))
        require(h == dig, 'pinned premise hash differs: ' + rel)
        got[rel] = h
    P = {'pinned_sha256': got}
    gates = {}
    for rel in (P_AM2_GATE, P_AQ1_GATE, P_AV1_GATE, P_AW1_GATE, P_AY1_GATE, P_AY2_GATE, P_BA1_GATE, P_BA2_GATE):
        g = json.loads(read_input(rel))
        require(g.get('verdict') == 'accepted_within_scope', 'premise gate not accepted: ' + rel)
        gates[rel] = g
    P['gates'] = gates
    # AM2: multilinear majorant, ball, enclosures
    am2 = read_input(P_AM2)
    m = match(r'J_0=\{(\d+)\\over(\d+)\}', am2, 'AM2 J_0')
    P['J0'] = Q(int(m.group(1)), int(m.group(2)))
    P['R'] = Q(1, int(match(r'For R=1/(\d+)', am2, 'AM2 R').group(1)))
    m = match(r"G\(R\)<(\d+)/(\d+),\\quad G'\(R\)<(\d+)", am2, 'AM2 G bounds')
    P['GR'] = Q(int(m.group(1)), int(m.group(2)))
    P['GpR'] = Q(int(m.group(3)))
    m = match(r"J_0G'\(R\)<(\d+)/(\d+),\\quad 2J_0G'\(R\)<(\d+)/(\d+)<1", am2, 'AM2 Lipschitz')
    P['JGp'] = Q(int(m.group(1)), int(m.group(2)))
    P['twoJGp'] = Q(int(m.group(3)), int(m.group(4)))
    contains(am2, 'L_k^{\\rm num}=16\\,8^k(1+5k/4)', 'AM2 multilinear constant')
    P['termination'] = int(match(r'zero for k>2p=(\d+)', am2, 'AM2 termination').group(1))
    contains(am2, 'Every I_j must meet X', 'AM2 support localization')
    contains(am2, 'Therefore `N\\X subset M subset N union X`', 'AM2 output support')
    contains(gates[P_AM2_GATE]['accepted'], 'G(t)=16 exp(8t)(1+10t)', 'AM2 gate majorant')
    # AV1: first-order coefficient, t_1, cutoff-vector removal
    av1 = read_input(P_AV1F)
    m = match(r'\\frac\{(\d+)\|\\tau\|\}\{(\d+)\}=:t_1', av1, 'AV1 t_1')
    P['t1_per_tau'] = Q(int(m.group(1)), int(m.group(2)))
    P['c1_den'] = int(match(r'c\^\{\(1\)\}_M=-\\frac\{\\tau\}\{(\d+)\}', av1, 'AV1 first-order coefficient').group(1))
    P['L_exact'] = int(match(r'For `L>=(\d+)` each vector `W_f Omega_0`', av1, 'AV1 cutoff exactness').group(1))
    contains(av1, '1-|\\langle\\psi,\\psi_L\\rangle|^2\\le\\frac{E_{0,L}-E_0}{E_1-E_0}\\le2(E_{0,L}-E_0)\\longrightarrow0', 'AV1 Eckart F22')
    contains(av1, 'e^{-C}=\\prod_{I}(1-\\hat c_I)', 'AV1 product ordering F06')
    contains(gates[P_AV1_GATE]['accepted'], 'The on-site cutoff is removed for the ground vector itself in each fixed box', 'AV1 gate cutoff vector')
    contains(gates[P_AW1_GATE]['accepted'], 'c^(1)=L_0=-(tau/72) sum W_f Omega_0', 'AW1 gate first-order coefficient')
    # AY1: F2 item by item, including cutoff-vector removal
    ay1g = gates[P_AY1_GATE]['accepted']
    contains(ay1g, 'F2 item by item (anchor groups of the retained faces supported in (b+S) cap Lambda_N, |X|<=4, termination order 8, '
                   'per-site sum J<=28|tau|=J_0=7/25000000', 'AY1 F2 items')
    contains(ay1g, 'at most 49 first-order faces per site, cutoff-vector removal', 'AY1 cutoff-vector removal')
    contains(ay1g, 'F2 retains 28N(5N+1) boundary faces more than F1', 'AY1 28N(5N+1)')
    contains(gates[P_AY1_GATE]['model'], 'F2 = I1 all-contained-face boxes with padding', 'AY1 family F2')
    contains(gates[P_AQ1_GATE]['accepted'], 'centered full-Z3 whole-star boxes have a subsequence', 'AQ1 family F1')
    # BA1 gate: the bound value, its rate, its route and its R-only scope
    ba1 = gates[P_BA1_GATE]
    m = match(r'headline pair q=1/(\d+) with K=(\d+)/(\d+) \(about 4\.3832e-7; exact_first_order tier, analytic_disc route on the disc of radius (\d+)\|tau\|',
              ba1['accepted'], 'BA1 gate headline')
    P['ba1_q'] = Q(1, int(m.group(1)))
    P['ba1_K'] = Q(int(m.group(2)), int(m.group(3)))
    P['ba1_rho_per_tau'] = Q(int(m.group(4)))
    contains(ba1['decision'], 'for u in R, sum over supports I containing u of ||c_I^{box1}-c_I^{box2}|| <= K q^(N-1)', 'BA1 R-only scope')
    require(ba1['gate_fields']['state_decay_claimed'] is False, 'BA1 is coefficient decay only')
    # BA1 reverse report: Theorem 4.1 ingredients (restated here for every site u and proved in full)
    ba1r = read_input(P_BA1R)
    contains(ba1r, "| `T(rho)` | `t_1(rho)/(1-28 rho G'(R))` (exact_first_order tier) |", 'BA1 reverse T(rho)')
    contains(ba1r, '| `t_1(rho)` | first-order anchored norm on the circle, `49 rho/144` |', 'BA1 reverse t_1(rho)')
    contains(ba1r, "| `t_i(rho)` | crude circle bound `28 rho G(R)` |", 'BA1 reverse crude circle')
    P['tau_star'] = Q(1, int(match(r'`R/\(28\*148/7\)=1/(\d+)`', ba1r, 'tau_star').group(1)))
    contains(ba1r, '**Theorem 4.1.** Let `N>=2`.', 'BA1 reverse Theorem 4.1')
    contains(ba1r, 'Then, for `u` in `R`,', 'BA1 reverse Theorem 4.1 is stated for u in R')
    contains(ba1r, '**Lemma 3.1 (common core).**', 'BA1 reverse Lemma 3.1')
    contains(ba1r, '**Lemma 2.2 (order versus distance).**', 'BA1 reverse Lemma 2.2')
    ba1f = read_input(P_BA1F)
    P['wmax_cap'] = rat(match(r'`w ≤ w_max = R/\(J_0·148/7\) = (\d+/\d+)`', ba1f, 'BA1 forward w_max').group(1))
    # I1 anchored face table
    P['i1'] = read_input(P_I1)
    # internal consistency of the parsed constants
    require(P['J0'] * P['GpR'] == P['JGp'] and 2 * P['JGp'] == P['twoJGp'], 'AM2 Lipschitz constants')
    require(P['c1_den'] == 72 and P['t1_per_tau'] == Q(49, 144), 'first-order pins')
    require(P['tau_star'] == P['R'] / (28 * P['GR']), 'tau_star = R/(28 G(R))')
    require(P['wmax_cap'] == P['R'] / (P['J0'] * P['GR']), 'w_max = R/(J_0 G(R))')
    return P


# ---------------------------------------------------------------------------
# Coarse geometry and the I1 anchored face table (parsed from the I1 snapshot).
# ---------------------------------------------------------------------------
E_UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
COVER_R = (ORIGIN, EZ)
TOKEN = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}
ORIENT = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}


def add(p, q):
    return tuple(a + b for a, b in zip(p, q))


def d_inf(p, q):
    return max(abs(a - b) for a, b in zip(p, q))


def norm_inf(p):
    return max(abs(a) for a in p)


def diam(A):
    A = list(A)
    return max((d_inf(a, b) for a in A for b in A), default=0)


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


def box(lo, hi):
    return frozenset(itertools.product(*[range(a, b + 1) for a, b in zip(lo, hi)]))


def coarse_box(N):
    return box((-N, -N, -N), (N, N, N))


def family_faces(volume, omitted, family):
    """F1: whole stars b+S inside the volume (AQ1, I1.6).  F2: every omitted face whose owner set lies in it (I1 section 6)."""
    out = {}
    for b in sorted(volume):
        whole = all(add(b, d) in volume for d in S_STAR)
        for k, cls in enumerate(omitted):
            M = frozenset(add(b, d) for d in cls[3])
            if family == 'F1':
                if whole:
                    out[(b, k)] = M
            elif family == 'F2':
                if M <= volume:
                    out[(b, k)] = M
            else:
                raise AdmissionError('unknown family ' + str(family))
    return out


def face_link_owner_counts(cls):
    """Fine-lattice links of the class face anchored at coarse 0 and the number owned by each coarse factor."""
    orient, r, sph, support, role = cls
    a, c = ORIENT[orient]
    p = (r, sph, 0)
    ea, ec = E_UNIT[a], E_UNIT[c]
    tails = (p, add(p, ea), add(p, ec), p)
    cnt = {}
    for t in tails:
        o = (t[0] // 4, t[1] // 2, t[2])
        cnt[o] = cnt.get(o, 0) + 1
    return cnt


def source_sites(faces_a, faces_b):
    """Sites of the owner sets of every face present in one volume's interaction and not the other's."""
    src = set()
    for key in set(faces_a) ^ set(faces_b):
        src |= (faces_a.get(key) or faces_b.get(key))
    return src


def lattice_shell_count(r):
    return 1 if r == 0 else (2 * r + 1) ** 3 - (2 * r - 1) ** 3


def S_sum(x):
    """sum over y in Z^3 of x^{d_inf(y,0)} = 1 + sum_{r>=1} (24 r^2 + 2) x^r, exact for rational 0 <= x < 1."""
    x = Q(x)
    require(0 <= x < 1, 'lattice sum needs 0 <= x < 1')
    return 1 + 24 * x * (1 + x) / (1 - x) ** 3 + 2 * x / (1 - x)


# ---------------------------------------------------------------------------
# Creation-expansion engine on small finite graphs (exact rationals; fixtures only).
# Sites carry local levels 0 (vacuum) .. d-1; a creation vector on I has excited levels
# (>=1) at every site of I (the premise c_I in tensor Q_x H_x).
# ---------------------------------------------------------------------------
def fam_list(sups):
    """All families of pairwise disjoint supports drawn from the ordered list sups."""
    out = []
    sups = list(sups)

    def rec(i, cur, used):
        if i == len(sups):
            out.append(tuple(cur))
            return
        rec(i + 1, cur, used)
        if not (sups[i] & used):
            rec(i + 1, cur + [sups[i]], used | sups[i])
    rec(0, [], frozenset())
    return out


def exc(F):
    return frozenset().union(*F) if F else frozenset()


def fam_vec(F, C, sitelist):
    """c_F = (tensor_{I in F} c_I) tensor vacuum, as a dict over basis tuples on sitelist."""
    items = [(sorted(I), C[I]) for I in F]
    res = {}

    def rec(k, assign, coef):
        if k == len(items):
            key = tuple(assign.get(x, 0) for x in sitelist)
            res[key] = res.get(key, 0) + coef
            return
        I, vec = items[k]
        for lv in sorted(vec):
            a = vec[lv]
            if a == 0:
                continue
            na = dict(assign)
            for x, l in zip(I, lv):
                na[x] = l
            rec(k + 1, na, coef * a)
    rec(0, {}, Q(1))
    return res


def inner(u, v):
    return sum(a * v.get(k, 0) for k, a in u.items())


def sorted_sups(C, region):
    region = frozenset(region)
    return sorted((I for I in C if I <= region), key=lambda I: (len(I), sorted(I)))


def psi_vec(C, region, sitelist):
    out = {}
    for F in fam_list(sorted_sups(C, region)):
        sg = (-1) ** len(F)
        for k, a in fam_vec(F, C, sitelist).items():
            out[k] = out.get(k, 0) + sg * a
    return out


def rho_brute(C, Y, sitelist):
    p = psi_vec(C, sitelist, sitelist)
    Z = inner(p, p)
    idx = [sitelist.index(y) for y in sorted(Y)]
    rest = [i for i in range(len(sitelist)) if i not in idx]
    rho = {}
    for k1, a1 in p.items():
        for k2, a2 in p.items():
            if all(k1[i] == k2[i] for i in rest):
                key = (tuple(k1[i] for i in idx), tuple(k2[i] for i in idx))
                rho[key] = rho.get(key, 0) + a1 * a2 / Z
    return {k: v for k, v in rho.items() if v != 0}


def overlap_connected(F, G, Y=None):
    """Bipartite overlap graph of (F, G), with the formal Y-vertex when Y is given, is connected."""
    nodes = [('a', I) for I in F] + [('b', I) for I in G] + ([('Y', frozenset(Y))] if Y is not None else [])
    if not nodes:
        return True
    adj = {i: set() for i in range(len(nodes))}
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[i][0] == nodes[j][0] and nodes[i][0] != 'Y':
                continue
            if nodes[i][1] & nodes[j][1]:
                adj[i].add(j)
                adj[j].add(i)
    seen, stack = {0}, [0]
    while stack:
        u = stack.pop()
        for x in sorted(adj[u]):
            if x not in seen:
                seen.add(x)
                stack.append(x)
    return len(seen) == len(nodes)


def polymer_list(sups, connected=True):
    fams = [F for F in fam_list(sups) if F]
    by_e = {}
    for F in fams:
        by_e.setdefault(exc(F), []).append(F)
    out = []
    for e in sorted(by_e, key=lambda z: (len(z), sorted(z))):
        for F in by_e[e]:
            for G in by_e[e]:
                if (not connected) or overlap_connected(F, G):
                    out.append((F, G))
    return out


def activity(C, F, G):
    e = sorted(exc(F))
    return (-1) ** (len(F) + len(G)) * inner(fam_vec(F, C, e), fam_vec(G, C, e))


def l1_product_bound(C, F, G):
    """A majorant of |activity| (product over members of the l1 norms of the creation vectors); not an activity."""
    out = Q(1)
    for I in list(F) + list(G):
        out *= sum(abs(x) for x in C[I].values())
    return out


def compatible_sum(items):
    """sum over families of pairwise disjoint supports of the product of weights; items = [(support, weight)]."""
    items = sorted(items, key=lambda t: (len(t[0]), sorted(t[0])))
    memo = {}

    def rec(i, used):
        key = (i, used)
        if key in memo:
            return memo[key]
        if i == len(items):
            return Q(1)
        tot = rec(i + 1, used)
        sup, wt = items[i]
        if not (sup & used):
            tot += wt * rec(i + 1, used | sup)
        memo[key] = tot
        return tot
    return rec(0, frozenset())


def Z_polymer(C, region, connected=True, activity_fn=None):
    act = activity_fn or activity
    polys = polymer_list(sorted_sups(C, region), connected)
    return compatible_sum([(exc(F), act(C, F, G)) for F, G in polys])


def y_cluster_list(sups, Y):
    fams = fam_list(sups)
    out = []
    for F in fams:
        for G in fams:
            if (exc(F) - Y) == (exc(G) - Y) and overlap_connected(F, G, Y):
                out.append((F, G))
    return out


def rho_polymer(C, Y, sitelist):
    """rho_Y = sum over Y-clusters eta of rho_eta * Z(Lambda minus supp eta) / Z(Lambda)."""
    Y = frozenset(Y)
    sups = sorted_sups(C, sitelist)
    ZL = Z_polymer(C, sitelist)
    rho = {}
    for F, G in y_cluster_list(sups, Y):
        S = Y | exc(F) | exc(G)
        zr = Z_polymer(C, [x for x in sitelist if x not in S])
        Sl = sorted(S)
        u, v = fam_vec(F, C, Sl), fam_vec(G, C, Sl)
        sg = (-1) ** (len(F) + len(G))
        idx = [Sl.index(y) for y in sorted(Y)]
        rest = [i for i in range(len(Sl)) if i not in idx]
        for k1, a1 in v.items():
            for k2, a2 in u.items():
                if all(k1[i] == k2[i] for i in rest):
                    key = (tuple(k1[i] for i in idx), tuple(k2[i] for i in idx))
                    rho[key] = rho.get(key, 0) + sg * a1 * a2 * zr / ZL
    return {k: v for k, v in rho.items() if v != 0}


# Qubit chains with scalar creation amplitudes (one excited level): norms are exact rationals.
def psi_qubit(c, region):
    region = frozenset(region)
    ss = sorted((I for I in c if I <= region and c[I] != 0), key=lambda I: (len(I), sorted(I)))
    out = {}

    def rec(i, used, coef):
        if i == len(ss):
            out[used] = out.get(used, 0) + coef
            return
        rec(i + 1, used, coef)
        if not (ss[i] & used):
            rec(i + 1, used | ss[i], -coef * c[ss[i]])
    rec(0, frozenset(), Q(1))
    return out


def Z_qubit(c, region):
    return sum(a * a for a in psi_qubit(c, region).values())


def rho_qubit(c, Y, sites):
    p = psi_qubit(c, sites)
    Z = sum(a * a for a in p.values())
    Y = sorted(Y)
    ys = frozenset(Y)
    r = {}
    for e1, a1 in p.items():
        for e2, a2 in p.items():
            if (e1 - ys) == (e2 - ys):
                k = (tuple(int(y in e1) for y in Y), tuple(int(y in e2) for y in Y))
                r[k] = r.get(k, 0) + a1 * a2 / Z
    return r


def mat_diff(r1, r2):
    keys = sorted(set(r1) | set(r2))
    return {k: r1.get(k, 0) - r2.get(k, 0) for k in keys}


def hs2(m):
    return sum(x * x for x in m.values())


def trace_norm_sq_2x2_hermitian(m):
    """Exact square of the trace norm of a real symmetric 2x2 matrix given as {(i,j): value} with i,j in {(0,),(1,)}."""
    a = m.get(((0,), (0,)), 0)
    d = m.get(((1,), (1,)), 0)
    b = m.get(((0,), (1,)), 0)
    tr = a + d
    det = a * d - b * b
    disc = tr * tr - 4 * det            # (lambda1 - lambda2)^2
    return max(tr * tr, disc)           # ||.||_1 = max(|tr|, |lambda1 - lambda2|)


# ---------------------------------------------------------------------------
# Proof weights (declared before any constant is evaluated; report section 0).
# ---------------------------------------------------------------------------
BETA = Q(1001, 1000)          # cardinality factor e^b
W_OVER_Q = Q(3)               # creation (diameter) weight w = 3/q
V_OVER_Q = Q(2)               # Kotecky-Preiss cluster (distance) weight v = e^mu = 2/q
DECLARED_WEIGHTS = {
    'creation_weight_w': 'w = 3/q (headline 192; secondary 3/(151552|tau|))',
    'cluster_weight_v': 'v = e^mu = 2/q (headline 128; secondary 2/(151552|tau|))',
    'cardinality_factor_e_b': '1001/1000',
    'kp_parameter_a': 'a = taubar^2, taubar the proved bound of ||c||_{w,b} in the tier of the constant',
    'loss_per_interaction': 'w e^{4b} = w (1001/1000)^4, at most 1/(37888|tau|)',
    'declared_before_constants': True,
}


def ceil_log_free_b_lower(beta):
    """Directed lower bound b >= (beta-1)/beta for b = ln(beta) (ln(1+x) >= x/(1+x))."""
    return (Q(beta) - 1) / Q(beta)


def ba1_disc_input(P, tau, rho, tier):
    """Form (b): K = 2 T(rho) (exact_first_order) or 2 t_i(rho) (crude_majorant); q = |tau|/rho."""
    rho = Q(rho)
    tau = abs(Q(tau))
    require(0 < tau < rho <= P['tau_star'], 'disc radius outside (|tau|, tau_star]')
    kappa = 28 * rho * P['GpR']
    require(kappa < 1, 'disc contraction')
    require(28 * rho * P['GR'] <= P['R'], 'disc self-map')
    if tier == 'exact_first_order':
        K = 2 * (P['t1_per_tau'] * rho) / (1 - kappa)
    elif tier == 'crude_majorant':
        K = 2 * 28 * rho * P['GR']
    else:
        raise AdmissionError('unknown tier ' + str(tier))
    return {'rho': rho, 'q': tau / rho, 'K': K, 'kappa_disc': kappa}


def pair_constants(P, V, tau, pair, tier, beta=BETA, w_over_q=W_OVER_Q, v_over_q=V_OVER_Q):
    """All constants of the polymer_kp route for one frozen pair, one tier and one coupling."""
    tau = Q(tau)
    at = abs(tau)
    J = 28 * at
    t1 = P['t1_per_tau'] * at
    if pair == 'headline':
        rho = P['ba1_rho_per_tau'] * at
    elif pair == 'secondary':
        rho = 1 / V['q2_per_tau']          # rho = |tau|/q_2 = 1/151552, independent of tau
    else:
        raise AdmissionError('unknown pair ' + str(pair))
    inp = ba1_disc_input(P, tau, rho, tier)
    q, K = inp['q'], inp['K']
    w = w_over_q / q
    v = v_over_q / q
    what = w * Q(beta) ** 4
    wmax = P['R'] / (J * P['GR'])
    require(what <= wmax, 'proof weight outside the admissible range after the cardinality loss')
    gamma = J * what * P['GpR']
    require(gamma < 1, 'mixed-weight contraction')
    if tier == 'exact_first_order':
        t = t1 / (1 - J * P['GpR'])
        taub = w * Q(beta) ** 3 * t1 / (1 - gamma)
    else:
        t = J * P['GR']
        taub = J * what * P['GR']
    require(taub <= P['R'] and t <= P['R'], 'tier bounds inside the ball')
    a = taub ** 2
    b_low = ceil_log_free_b_lower(beta)
    require(a <= 2 * b_low, 'Kotecky-Preiss parameter a exceeds 2b')
    require(1 <= v <= w, 'cluster weight v between 1 and w')
    require(q * v > 1, 'site sum needs q v > 1')
    Svw = S_sum(v / w)
    Sq = S_sum(1 / (q * v))
    A = 2 * taub ** 2 + a * (1 + 2 * taub ** 2 * Svw)
    k0 = 4 * taub + 2 * A * (t + taub * (Svw - 1))
    NR = (1 + t) ** 4
    far = K * (1 + q) * NR * (Sq - 1)
    L1 = 2 * K * (1 + q)
    L2 = 2 * K * (1 + q) * t
    L3 = far * 2 * taub
    L4 = far * (2 * taub + 4 * taub ** 2 * (t + taub * (Svw - 1)))
    L5 = far * 2 * a * (1 + 2 * taub ** 2 * Svw) * (t + taub * (Svw - 1))
    C = K * (1 + q) * (2 * (1 + t) + NR * k0 * (Sq - 1))
    require(C == L1 + L2 + L3 + L4 + L5, 'ledger pieces add to C')
    cs = K * (2 + k0 * (Sq - 1))
    rate_ok = (1 + t) ** 2 <= 1 + V['region_rate']
    return {'tau': tau, 'tier': tier, 'pair': pair, 'rho': rho, 'q': q, 'K': K, 'J': J, 't1': t1, 't': t,
            'w': w, 'v': v, 'what': what, 'wmax': wmax, 'gamma': gamma, 'taub': taub, 'a': a, 'b_low': b_low,
            'Svw': Svw, 'Sq': Sq, 'A': A, 'kappa0': k0, 'NR': NR, 'C': C, 'c_site': cs,
            'ledger': {'L1': L1, 'L2': L2, 'L3': L3, 'L4': L4, 'L5': L5},
            'eta_R': t, 'kappa0_contract_R': NR * 2 * k0, 'region_rate_ok': rate_ok,
            'kappa_disc': inp['kappa_disc']}


def region_bound(pc, Y_norms, N):
    """Proved bound for a region Y (given the l_inf norms of its sites) inside Lambda_N."""
    nY = len(Y_norms)
    t, K, q, k0, Sq = pc['t'], pc['K'], pc['q'], pc['kappa0'], pc['Sq']
    require(all(0 <= m <= N for m in Y_norms), 'region inside Lambda_N')
    return sum(K * q ** (N - m) for m in Y_norms) * (2 * (1 + t) ** (nY - 1) + (1 + t) ** (2 * nY) * k0 * (Sq - 1))


def region_target_ok(pc, Y_norms, N, cs, rate):
    """bound <= c_site |Y| e^{|Y| rate} q^{d_Y}, using e^{x} >= 1+x and (1+t)^2 <= 1+rate."""
    nY = len(Y_norms)
    dY = N - max(Y_norms)
    lhs = region_bound(pc, Y_norms, N)
    require((1 + pc['t']) ** 2 <= 1 + rate, 'region exponential rate exceeds the frozen 1/10^8')
    rhs_lower = cs * nY * (1 + rate) ** nY * pc['q'] ** dY    # (1+rate)^n <= e^{n rate}
    require(lhs <= rhs_lower, 'region bound exceeds c_site |Y| e^{|Y|/10^8} q^{d_Y}')
    return True


# ---------------------------------------------------------------------------
# Small exact algebra helpers for the fixtures.
# ---------------------------------------------------------------------------
def padd(p, q):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v != 0}


def pmul(p, q):
    out = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            out[k] = out.get(k, 0) + v1 * v2
    return {k: v for k, v in out.items() if v != 0}


def pscale(p, c):
    return {k: v * c for k, v in p.items() if v * c != 0}


def peval(p, vals):
    tot = Q(0)
    for k, v in p.items():
        term = Q(v)
        for e, x in zip(k, vals):
            term *= Q(x) ** e
        tot += term
    return tot


def psi_symbolic(amps, nvars):
    """Qubit ground-vector expansion prod (1 - c_I) Omega with symbolic amplitudes: amps = {I: polynomial}."""
    sups = sorted(amps, key=lambda I: (len(I), sorted(I)))
    out = {}
    for F in fam_list(sups):
        poly = {tuple([0] * nvars): Q(1)}
        for I in F:
            poly = pmul(poly, pscale(amps[I], -1))
        e = exc(F)
        out[e] = padd(out.get(e, {}), poly)
    return out


def marginal_numerators(psi, Y):
    """Unnormalized Y-marginal entries (polynomials) of a qubit expansion; keys ((y bits), (y bits))."""
    ys = frozenset(Y)
    Yl = sorted(Y)
    num = {}
    for e1, p1 in psi.items():
        for e2, p2 in psi.items():
            if (e1 - ys) == (e2 - ys):
                k = (tuple(int(y in e1) for y in Yl), tuple(int(y in e2) for y in Yl))
                num[k] = padd(num.get(k, {}), pmul(p1, p2))
    return num


def mzeros(n):
    return [[Q(0)] * n for _ in range(n)]


def mmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def mT(A):
    return [list(r) for r in zip(*A)]


def kron(A, B):
    return [[A[i // len(B)][j // len(B)] * B[i % len(B)][j % len(B)] for j in range(len(A) * len(B))] for i in range(len(A) * len(B))]


def creation_matrix(nq, I, amp):
    """hat c_I = amp |1_I><0_I| (x) 1 on nq qubits (qubit 0 most significant)."""
    dim = 2 ** nq
    M = mzeros(dim)
    for col in range(dim):
        bits = [(col >> (nq - 1 - i)) & 1 for i in range(nq)]
        if all(bits[i] == 0 for i in I):
            nb = list(bits)
            for i in I:
                nb[i] = 1
            row = sum(b << (nq - 1 - i) for i, b in enumerate(nb))
            M[row][col] += amp
    return M


def partial_trace_keep_first(M, dim_keep, dim_trace):
    out = mzeros(dim_keep)
    for i in range(dim_keep):
        for j in range(dim_keep):
            out[i][j] = sum(M[i * dim_trace + k][j * dim_trace + k] for k in range(dim_trace))
    return out


def density_from(vectors, weights):
    n = len(vectors[0])
    D = mzeros(n)
    for v, w in zip(vectors, weights):
        nrm = sum(x * x for x in v)
        for i in range(n):
            for j in range(n):
                D[i][j] += w * v[i] * v[j] / nrm
    return D


def tn2_sq(M):
    """Exact square of the trace norm of a real symmetric 2x2 matrix (list form)."""
    a, b, d = M[0][0], M[0][1], M[1][1]
    return max((a + d) ** 2, (a + d) ** 2 - 4 * (a * d - b * b))


def rs_ground(nsites, bonds, order):
    """Intermediate-normalized Rayleigh-Schroedinger ground vector of sum n_x + g sum_bonds X_i X_j (exact)."""
    zero = tuple([0] * nsites)

    def vapply(vec):
        out = {}
        for k, a in vec.items():
            for (i, j) in bonds:
                kk = list(k)
                kk[i] ^= 1
                kk[j] ^= 1
                kk = tuple(kk)
                out[kk] = out.get(kk, 0) + a
        return out
    psis, Es = [{zero: Q(1)}], [Q(0)]
    for n in range(1, order + 1):
        vp = vapply(psis[n - 1])
        Es.append(vp.get(zero, Q(0)))
        rhs = dict(vp)
        for k in range(1, n + 1):
            for kk, a in psis[n - k].items():
                rhs[kk] = rhs.get(kk, 0) - Es[k] * a
        psis.append({kk: -a / sum(kk) for kk, a in rhs.items() if kk != zero and a != 0})
    return psis


# ---------------------------------------------------------------------------
# Main computation.
# ---------------------------------------------------------------------------
MODEL = {'model_id': 'AQ_patterned_zero_selected', 'gauge_group': 'SU(2)', 'dimension': 3, 'selected_triple': ['0', '0', '0'],
         'tau_cap': '1/100000000', 'signs': ['+', '-'], 'metric': 'coarse l_inf on factor sites, star diameter 1',
         'families': ['F1', 'F2'], 'cover': 'R={0,e_z}', 'weights': dict((k, v) for k, v in DECLARED_WEIGHTS.items() if k != 'declared_before_constants')}
FAMILIES = {'F1': 'AQ1 centered whole-star boxes Lambda_N=[-N,N]^3 (whole stars b+S inside the volume)',
            'F2': 'I1 section 6 all-contained-face boxes with padding on the same Lambda_N (faces with owner set inside the volume; padding decouples)'}
TOPOLOGY = 'trace norm on B(H_Y) for states; norm on compact theta windows for dynamics (not used); GNS strong for representations (not used)'
RATE_UNIT = 'per coarse l-infinity step in N at fixed spacing (a coarse step is (4a,2a,a) in fine units); not a rate in the lattice spacing a'


def model_ok(m):
    require(m.get('model_id') == 'AQ_patterned_zero_selected', 'model id changed')
    require(m.get('gauge_group') == 'SU(2)' and m.get('dimension') == 3, 'gauge group or dimension changed')
    require(m.get('selected_triple') == ['0', '0', '0'], 'selected triple changed')
    require(m.get('tau_cap') == '1/100000000' and m.get('signs') == ['+', '-'], 'coupling changed')
    require(m.get('metric') == 'coarse l_inf on factor sites, star diameter 1', 'metric changed')
    require(m.get('families') == ['F1', 'F2'], 'families changed')
    require(m.get('weights') == MODEL['weights'], 'proof weights changed after the constants')
    return True


def compute(check_sha):
    contract, contract_digest = load_contract()          # sha256 verified before any evaluation
    V = contract_values(contract)
    template = V['template']
    check('contract_snapshot_sha256', contract_digest == CONTRACT_SHA256, sha256=contract_digest,
          check_py_sha256_recorded_before_evaluation=check_sha)
    P = load_premises()
    omitted = [cl for cl in parse_i1_table(P['i1']) if cl[4] == 'omitted']
    require(len(omitted) == 21, 'twenty-one omitted face classes')
    check('premise_gates_pinned_and_parsed', True, pinned=P['pinned_sha256'],
          parsed={'J_0': s(P['J0']), 'R': s(P['R']), 'G_R_upper': s(P['GR']), "G'_R_upper": s(P['GpR']),
                  't_1_per_tau': s(P['t1_per_tau']), 'c1_denominator': P['c1_den'], 'L_exact': P['L_exact'],
                  'tau_star': s(P['tau_star']), 'w_max_cap': s(P['wmax_cap']), 'ba1_K_gate_bound_value': s(P['ba1_K']),
                  'ba1_q': s(P['ba1_q']), 'ba1_disc_radius_per_tau': s(P['ba1_rho_per_tau']), 'termination_order': P['termination']})
    tau_cap = V['tau']
    taus = {'+': tau_cap, '-': -tau_cap}

    # ---------------- form (b): every-site analytic-disc input, proved in report section 8 -----------
    head_in = {sg: ba1_disc_input(P, t, P['ba1_rho_per_tau'] * abs(t), 'exact_first_order') for sg, t in taus.items()}
    require(head_in['+']['K'] == P['ba1_K'] and head_in['-']['K'] == P['ba1_K'], 'form (b) at rho=64|tau| reproduces the gate bound value')
    require(head_in['+']['q'] == V['q_head'] == P['ba1_q'], 'headline q = |tau|/rho = 1/64')
    sec_in = {sg: ba1_disc_input(P, t, 1 / V['q2_per_tau'], 'exact_first_order') for sg, t in taus.items()}
    require(sec_in['+']['q'] == V['q2_per_tau'] * tau_cap, 'secondary q = 151552|tau|')
    crude_in = ba1_disc_input(P, tau_cap, P['ba1_rho_per_tau'] * tau_cap, 'crude_majorant')
    # geometry of the every-site statement: every source face of every comparison lies at l_inf distance at
    # least N-|u|_inf from every site u of Lambda_N (common-core lemma restated for every u), enumerated.
    geom_rows = []

    def every_site_rows(label, N, fa, fb):
        src = source_sites(fa, fb)
        require(src, 'comparison has source terms')
        worst_slack = None
        for u in sorted(coarse_box(N)):
            dmin = min(d_inf(u, x) for x in src)
            slack = dmin - (N - norm_inf(u))
            require(slack >= 0, 'every-site common core violated at ' + str(u) + ' in ' + label)
            worst_slack = slack if worst_slack is None else min(worst_slack, slack)
        d_ez = min(d_inf(EZ, x) for x in src)
        d_0 = min(d_inf(ORIGIN, x) for x in src)
        require(d_ez == N - 1 and d_0 == N, 'distances from R: N-1 at e_z, N at 0 (attained)')
        geom_rows.append({'comparison': label, 'N': N, 'source_sites': len(src), 'min_slack_over_sites_of_Lambda_N': worst_slack,
                          'distance_e_z': d_ez, 'distance_0': d_0})
        return True
    for N in (2, 3):
        F1N, F2N = family_faces(coarse_box(N), omitted, 'F1'), family_faces(coarse_box(N), omitted, 'F2')
        F1N1, F2N1 = family_faces(coarse_box(N + 1), omitted, 'F1'), family_faces(coarse_box(N + 1), omitted, 'F2')
        every_site_rows('F1 Lambda_N vs F1 Lambda_(N+1)', N, F1N, F1N1)
        every_site_rows('F2 Lambda_N vs F2 Lambda_(N+1)', N, F2N, F2N1)
        every_site_rows('F1 vs F2 on Lambda_N', N, F1N, F2N)
        every_site_rows('F1 Lambda_N vs F2 Lambda_(N+2) (any two centered boxes, directly)', N,
                        F1N, family_faces(coarse_box(N + 2), omitted, 'F2'))
        require(set(F1N) <= set(F2N) and len(F2N) - len(F1N) == 28 * N * (5 * N + 1), '28N(5N+1) extra F2 faces')
    VA, VB = box((-2, -2, -2), (3, 2, 4)), box((-3, -2, -2), (2, 3, 2))
    require(coarse_box(2) <= VA and coarse_box(2) <= VB, 'general volumes contain Lambda_2')
    for fam in ('F1', 'F2'):
        every_site_rows(fam + ' on [-2,3]x[-2,2]x[-2,4] vs ' + fam + ' on [-3,2]x[-2,3]x[-2,2] (one prescription, directly)', 2,
                        family_faces(VA, omitted, fam), family_faces(VB, omitted, fam))
    F24 = family_faces(coarse_box(4), omitted, 'F2')
    F14 = family_faces(coarse_box(4), omitted, 'F1')
    require(len(F24) - len(F14) == 28 * 4 * 21, '28N(5N+1) at N=4')
    max_per_site = 0
    for vol_faces in (family_faces(coarse_box(3), omitted, 'F2'), family_faces(VA, omitted, 'F2'), family_faces(coarse_box(3), omitted, 'F1')):
        per_site = {}
        for M in vol_faces.values():
            for x in M:
                per_site[x] = per_site.get(x, 0) + 1
        max_per_site = max(max_per_site, max(per_site.values()))
    require(max_per_site == 49, 'at most 49 faces per site (first-order input), bulk value attained')
    face_energy_max = 0
    for cl in omitted:
        cnt = face_link_owner_counts(cl)
        require(frozenset(cnt) == cl[3], 'owner set from fine links equals the I1 support')
        face_energy_max = max(face_energy_max, 6 * max(cnt.values()))
    require(face_energy_max <= P['L_exact'], 'face vectors kept for L at least 24')
    every_site = {
        'form': '(b)', 'statement': 'sum_{I ni u} ||c^A_I - c^B_I|| <= K q^((N-|u|_inf)_+) for every site u of the union volume, '
                                   'K = 2T(rho), q = |tau|/rho, both signs, every Q_L, every comparison',
        'proved_in': 'report.md section 8 (Theorem 8.1 with Lemmas 8.2-8.6), proved in full in this packet',
        'scope': 'every site u of the smaller box and every site of the union volume (exponent 0 outside Lambda_N)',
        'ba1_gate_scope': 'u in R only (not used as the every-site statement)',
        'headline': {'rho': '64|tau|', 'q': s(head_in['+']['q']), 'K': s(head_in['+']['K']), 'K_preview': dec(head_in['+']['K']),
                     'equals_gate_bound_value': True, 'tier': 'exact_first_order', 'ba1_input': 'gate bound value K=49/111790368 (analytic_disc)'},
        'secondary': {'rho': '1/151552', 'q': '151552|tau|', 'K': s(sec_in['+']['K']), 'K_preview': dec(sec_in['+']['K']),
                      'tier': 'exact_first_order', 'ba1_input': 'analytic_disc re-instantiated at rho=1/151552 (labelled)'},
        'crude': {'rho': '64|tau|', 'K': s(crude_in['K']), 'tier': 'crude_majorant', 'ba1_input': 'analytic_disc crude circle bound 2 t_i(rho)'},
        'geometry_rows': geom_rows, 'max_faces_per_site': max_per_site, 'max_face_vector_site_energy': face_energy_max,
    }

    def every_site_ok(rec):
        require(rec.get('form') in ('(a)', '(b)'), 'coefficient input form named')
        require(rec.get('scope', '').startswith('every site u of the smaller box'), 'coefficient input used at every site')
        require('proved in full in this packet' in rec.get('proved_in', ''), 'form (b) must be proved in full in the packet')
        require(rec.get('ba1_gate_scope') == 'u in R only (not used as the every-site statement)', 'R-only gate statement not used at far sites')
        require(rat(rec['headline']['K']) == P['ba1_K'], 'headline input is the gate bound value')
        return True
    check('every_site_coefficient_input',
          every_site_ok(every_site)
          and rejected(lambda: every_site_ok(dict(every_site, scope='u in R only, used at every site of Lambda_N')), 'r_only_input_used_at_far_sites')
          and rejected(lambda: every_site_ok(dict(every_site, proved_in='cited as an admitted BA1 statement')), 'form_b_cited_as_admitted')
          and rejected(lambda: every_site_rows('shifted source (exponent N-|u|+1 claimed in the contract form)', 3,
                                               family_faces(coarse_box(2), omitted, 'F1'), family_faces(coarse_box(3), omitted, 'F1')), 'wrong_box_size_for_exponent')
          and rejected(lambda: every_site_ok(dict(every_site, headline=dict(every_site['headline'], K=s(P['ba1_K'] / 2)))), 'input_K_halved'),
          record=every_site)

    # ---------------- the mixed-weight contraction lemma (report section 5), audited ----------------
    p_sup = 4
    for k in range(0, P['termination'] + 1):
        root_x = 2 ** p_sup * (2 * p_sup) ** k
        root_c = 2 ** p_sup * (2 * p_sup) ** k * Q(k * (p_sup + 1), p_sup)
        require(root_x + root_c == 16 * 8 ** k * (1 + Q(5 * k, 4)), 'L_k^num decomposition')
        taylor = 16 * (Q(8 ** k, factorial(k)) + (10 * Q(8 ** (k - 1), factorial(k - 1)) if k >= 1 else 0))
        require(factorial(k) * taylor == 16 * 8 ** k * (1 + Q(5 * k, 4)), 'k! times Taylor coefficient of G')

    def W(I, w, beta):
        return Q(w) ** diam(I) * Q(beta) ** len(I)

    def weight_inequality_ok(w, beta, loss_fn, configs):
        for X, Is, M in configs:
            bound = loss_fn(X, w, beta)
            for I in Is:
                bound *= W(I, w, beta)
            require(W(M, w, beta) <= bound, 'mixed weight inequality W(M) <= loss * prod W(I_j) violated')
        return True
    star = frozenset(S_STAR)
    Xs = [star, frozenset({ORIGIN, EZ}), frozenset({ORIGIN, (1, 0, 0), (0, 0, 1)})]
    cube = sorted(box((-1, -1, -1), (2, 1, 1)))
    small_sups = sorted({frozenset(c) for r in (1, 2) for c in itertools.combinations(cube, r) if diam(c) <= 2},
                        key=lambda I: (len(I), sorted(I)))
    configs = []
    for X in Xs:
        meet = [I for I in small_sups if I & X]
        few = [I for I in meet if len(I) == 1 or (len(I) == 2 and diam(I) == 1)][:24]
        for Is in [()] + [(I,) for I in meet] + [(I1, I2) for I1 in few for I2 in few]:
            Nset = exc(Is)
            base, extra = Nset - X, sorted((Nset | X) - (Nset - X))
            for r in range(len(extra) + 1):
                for add_ in itertools.combinations(extra, r):
                    M = base | frozenset(add_)
                    if M:
                        configs.append((X, Is, M))
    loss_interaction = lambda X, w, beta: Q(w) ** diam(X) * Q(beta) ** len(X)
    for (w_t, b_t) in ((Q(192), BETA), (Q(3), Q(5, 4)), (Q(390625, 148), BETA)):
        weight_inequality_ok(w_t, b_t, loss_interaction, configs)
    # attained loss: V_X = X (x) X (x) X (x) X on the four-site star, L_0 = H^{-1} P V_X Omega = (1/4)|1111>
    attained = [(star, (), star)]
    require(W(star, 192, BETA) == loss_interaction(star, 192, BETA), 'loss w e^{4b} attained at order zero')
    disc = [(frozenset({ORIGIN, (1, 0, 0)}), (frozenset({(-1, 0, 0), ORIGIN}), frozenset({(1, 0, 0), (2, 0, 0)})),
             frozenset({(-1, 0, 0), (2, 0, 0)}))]
    require(diam(disc[0][2]) == 3, 'disconnected output has diameter 3 = d_X + 1 + 1')
    mixed_record = {
        'lemma': "||L_k(c_1..c_k)||_{w,b} <= w e^{4b} J L_k^num prod_j ||c_j||_{w,b}, ||c||_{w,b} = max_u sum_{I ni u} w^{diam I} e^{b|I|} ||c_I||",
        'loss': 'w e^{4b} once per interaction term (|X| at most 4, diam X at most 1), never per creation',
        'first_order_factor': 'w e^{3b} (owner sets have at most 3 sites and diameter 1)',
        'self_map_and_tiers': 'taubar = w e^{3b} t_1/(1 - J w e^{4b} G\'(R)) (exact_first_order); J w e^{4b} G(R) (crude_majorant); admissible iff w e^{4b} <= R/(J G(R)) = 1/(37888|tau|)',
        'source': 'proved in full in this packet (report section 5); not cited from BA1',
        'configurations_checked': len(configs), 'weights_checked': ['192, 1001/1000', '3, 5/4', '390625/148, 1001/1000'],
    }

    def mixed_ok(rec):
        require(rec['source'].startswith('proved in full in this packet'), 'mixed-weight lemma must be proved here, not cited')
        require(rec['loss'].startswith('w e^{4b} once per interaction term'), 'loss w e^{4b} per interaction')
        return True
    check('mixed_weight_lemma_proved',
          mixed_ok(mixed_record)
          and rejected(lambda: mixed_ok(dict(mixed_record, source='cited from BA1 forward F03/F04')), 'mixed_lemma_cited_from_ba1')
          and rejected(lambda: weight_inequality_ok(Q(192), BETA, lambda X, w, beta: Q(w) * Q(beta) ** 3, attained), 'loss_w_e3b_instead_of_w_e4b')
          and rejected(lambda: weight_inequality_ok(Q(192), BETA, lambda X, w, beta: Q(1), attained), 'loss_charged_per_creation_only')
          and rejected(lambda: weight_inequality_ok(Q(192), BETA, lambda X, w, beta: Q(w) ** (diam(X) + max([0])) * Q(beta) ** len(X)
                                                    / Q(w) ** (sum(diam(I) for I in disc[0][1]) - max(diam(I) for I in disc[0][1])), disc),
                       'max_instead_of_sum_diameter_shortcut')
          and rejected(lambda: pair_constants(P, V, tau_cap, 'secondary', 'exact_first_order', beta=Q(2)), 'cardinality_factor_2_beyond_admissible_range')
          and rejected(lambda: pair_constants(P, V, tau_cap, 'headline', 'exact_first_order', w_over_q=Q(42)), 'creation_weight_beyond_w_max'),
          record=mixed_record)

    # ---------------- polymer representation on a four-site collection (report section 3) ------------
    sites4 = [0, 1, 2, 3]
    C4 = {}
    for r in range(1, 5):
        for I in itertools.combinations(sites4, r):
            vec = {}
            for lv in itertools.product((1, 2), repeat=r):
                num = (7 * sum((x + 1) * (i + 2) for i, x in enumerate(I)) + 5 * sum(l * (j + 1) for j, l in enumerate(lv)) + 3 * r) % 17 - 8
                vec[lv] = Q(num, 40)
            C4[frozenset(I)] = vec
    psi4 = psi_vec(C4, sites4, sites4)
    Z4_brute = inner(psi4, psi4)
    Z4_poly = Z_polymer(C4, sites4)
    fams4 = fam_list(sorted_sups(C4, sites4))
    mismatched_zero = all(inner(fam_vec(F, C4, sites4), fam_vec(G, C4, sites4)) == 0
                          for F in fams4 for G in fams4 if exc(F) != exc(G))
    ident = {}
    for Yt in ((1,), (1, 2)):
        rb, rp = rho_brute(C4, frozenset(Yt), sites4), rho_polymer(C4, frozenset(Yt), sites4)
        ident[str(list(Yt))] = (rb == rp)
    vac = {}
    for St in ((0,), (0, 3), (1, 2)):
        Sx = frozenset(St)
        num = sum(a * a for k, a in psi4.items() if all(k[x] == 0 for x in Sx))
        vac[str(list(St))] = (Z_polymer(C4, [x for x in sites4 if x not in Sx]) / Z4_poly == num / Z4_brute)

    def polymer_identity_ok(Zp, identities, mism, vacp):
        require(Zp == Z4_brute, 'polymer sum differs from the brute-force norm')
        require(all(identities.values()), 'Y-cluster representation of the reduced density fails')
        require(mism, 'families with different excitation sets must pair to zero')
        require(all(vacp.values()), 'vacuum probability identity fails')
        return True
    # a creation with a vacuum component (violating c_I in tensor Q_x H_x) pairs mismatched families nonzero
    C4v = dict(C4)
    C4v[frozenset({0})] = dict(C4[frozenset({0})])
    C4v[frozenset({0})][(0,)] = Q(1, 4)
    F_a = (frozenset({0}),)
    mism_bad = inner(fam_vec(F_a, C4v, sites4), fam_vec((), C4v, sites4)) == 0
    # cardinality factor in the tree majorant: single-site qubit creations c_x = 1/3 on the four sites give
    # polymers ({x},{x}) of activity eps = 1/9; the clusters meeting a set S are repeated copies of one polymer,
    # sum |Phi^T| = |S| (-log(1-eps)) in [|S|(eps + eps^2/2), |S| eps/(1-eps)].
    eps = Q(1, 9)
    a_card = Q(1, 7)
    require(eps * Q(7, 6) <= a_card, 'KP condition eps e^{a} <= a with e^{1/7} <= 7/6')
    require(Z_qubit({frozenset({x}): Q(1, 3) for x in sites4}, sites4) == Q(10, 9) ** 4, 'single-site polymer gas norm')
    S_card = 4
    cluster_lower, cluster_upper = S_card * (eps + eps ** 2 / 2), S_card * eps / (1 - eps)

    def tree_majorant_ok(majorant):
        require(cluster_lower <= majorant, 'tree majorant below the exact cluster sum (cardinality factor dropped)')
        return True
    require(cluster_upper <= a_card * S_card, 'majorant a|S| dominates the exact cluster sum')
    polymer_record = {'model_is_finite_graph': True, 'transfers_to_aq': False,
                      'collection': 'four qutrit sites, all 15 supports, rational creation vectors (80 components)',
                      'norm_brute': s(Z4_brute), 'norm_polymer_sum': s(Z4_poly), 'y_cluster_identities': ident,
                      'vacuum_probability_identities': vac, 'mismatched_excitation_pairs_zero': mismatched_zero,
                      'cardinality_fixture': {'activity': s(eps), 'a': s(a_card), 'exact_cluster_sum_bracket': [s(cluster_lower), s(cluster_upper)],
                                              'majorant_with_cardinality_a_S': s(a_card * S_card), 'majorant_without_cardinality': s(a_card)}}
    check('fixture_polymer_identity',
          polymer_identity_ok(Z4_poly, ident, mismatched_zero, vac) and tree_majorant_ok(a_card * S_card)
          and rejected(lambda: polymer_identity_ok(Z_polymer(C4, sites4, connected=False), ident, mismatched_zero, vac), 'polymers_without_overlap_connectivity')
          and rejected(lambda: polymer_identity_ok(Z_polymer(C4, sites4, activity_fn=l1_product_bound), ident, mismatched_zero, vac),
                       'activity_replaced_by_its_bound')
          and rejected(lambda: polymer_identity_ok(Z4_poly, ident, mism_bad, vac), 'creation_with_vacuum_component_pairs_mismatched_families')
          and rejected(lambda: tree_majorant_ok(a_card), 'cardinality_factor_dropped_in_tree_majorant'),
          record=polymer_record)

    # ---------------- exploration-tree majorants, KP truncation and Lemma 7.1 on finite graphs --------
    def chain_sups(n, maxdiam, maxsize):
        return sorted({frozenset(c) for r in range(1, maxsize + 1) for c in itertools.combinations(range(n), r)
                       if max(c) - min(c) <= maxdiam}, key=lambda I: (len(I), sorted(I)))
    d1 = lambda x, y: abs(x - y)
    n5 = 5
    sups5 = chain_sups(n5, 2, 3)
    fams5 = fam_list(sups5)
    polys5 = polymer_list(sups5)
    nrm5 = {K: Q((13 * sum((i + 1) ** 2 for i in K) + 7 * len(K)) % 11 + 1, 240) for K in sups5}
    w_t = Q(2)
    u5 = {K: w_t ** (max(K) - min(K)) * nrm5[K] for K in sups5}
    t5 = max(sum(nrm5[K] for K in sups5 if x in K) for x in range(n5))
    tw5 = max(sum(u5[K] for K in sups5 if x in K) for x in range(n5))
    require(tw5 <= 1, 'exploration audit needs taubar <= 1')

    def prodn(F, G, skip=None, wt=None):
        out = Q(1)
        items = [('a', K) for K in F] + [('b', K) for K in G]
        for side, K in items:
            if skip is not None and (side, K) == skip:
                continue
            out *= (wt or nrm5)[K]
        return out
    audit = {'model_is_finite_graph': True, 'transfers_to_aq': False, 'chain_sites': n5, 'supports': len(sups5),
             'polymers': len(polys5), 'taubar_w2': s(tw5), 't': s(t5)}
    for x in range(n5):
        require(sum(prodn(F, G, wt=u5) for F, G in polys5 if x in exc(F)) <= tw5 ** 2, '(P) polymer exploration bound')
    for I in sups5:
        for side in ('a', 'b'):
            for z in range(n5):
                tot = sum(prodn(F, G, skip=(side, I)) for F, G in polys5
                          if I in (F if side == 'a' else G) and z in exc(F))
                if z in I:
                    require(tot <= t5, '(P) marked polymer bound at z in I')
                else:
                    require(tot <= tw5 * w_t ** (-min(d1(z, i) for i in I)), '(P) marked polymer bound with distance')
    for Yt in ((2,), (1, 2)):
        Y5 = frozenset(Yt)
        ycl = y_cluster_list(sups5, Y5)
        NY = (1 + t5) ** (2 * len(Y5))
        require(sum(prodn(F, G) for F, G in ycl) <= NY, '(Y0) Y-cluster total bound')
        for J in sups5:
            if J & Y5:
                continue
            dJ = min(d1(j, y) for j in J for y in Y5)
            for side in ('a', 'b'):
                tot = sum(prodn(F, G, skip=(side, J)) for F, G in ycl if J in (F if side == 'a' else G))
                require(tot <= tw5 * w_t ** (-dJ) * NY, '(YJ) rooted Y-cluster bound')
        for sx in range(n5):
            if sx in Y5:
                continue
            ds = min(d1(sx, y) for y in Y5)
            tot = sum(prodn(F, G) for F, G in ycl if sx in (Y5 | exc(F) | exc(G)))
            require(tot <= 2 * tw5 ** 2 * w_t ** (-ds) * NY, '(YS) site-reach Y-cluster bound')
        audit['Y=' + str(list(Yt))] = {'y_clusters': len(ycl), 'total_over_bound': dec(sum(prodn(F, G) for F, G in ycl) / NY, 6)}
    # KP truncation: |pi_{Lambda minus S}(G) - pi_Lambda(G)| <= sum_{z in G, s in S} a v^{-d(z,s)} on a six-site chain
    n6 = 6
    sups6 = chain_sups(n6, 1, 2)
    c6 = {K: Q((5 * sum(i + 1 for i in K) + 3 * len(K)) % 19 - 9, 150) for K in sups6}
    wk, vk, bk = Q(4), Q(2), Q(11, 10)
    tau6 = max(sum(wk ** (max(K) - min(K)) * bk ** len(K) * abs(c6[K]) for K in sups6 if x in K) for x in range(n6))
    a6 = tau6 ** 2
    require(tau6 <= 1 and a6 <= 2 * ceil_log_free_b_lower(bk), 'KP condition for the truncation audit')
    ZL6 = Z_qubit(c6, range(n6))
    worst = Q(0)
    sets6 = [frozenset(range(i, i + r)) for r in range(1, 5) for i in range(n6 - r + 1)]
    for S6 in [G for G in sets6 if len(G) <= 2]:
        ZS = Z_qubit(c6, [x for x in range(n6) if x not in S6])
        for G6 in sets6:
            if G6 & S6:
                continue
            lhs = abs(Z_qubit(c6, [x for x in range(n6) if x not in S6 | G6]) / ZS - Z_qubit(c6, [x for x in range(n6) if x not in G6]) / ZL6)
            rhs = sum(a6 * vk ** (-d1(z, y)) for z in G6 for y in S6)
            require(lhs <= rhs, 'truncated vacuum-probability bound')
            worst = max(worst, lhs / rhs)
    audit['kp_truncation'] = {'taubar': s(tau6), 'a': s(a6), 'v': s(vk), 'max_ratio_lhs_over_bound': dec(worst, 6)}
    # Lemma 7.1 (marginal locality) on a six-site chain, exact both sides
    sups6b = chain_sups(n6, 2, 3)
    cA6 = {K: Q((11 * sum((i + 2) ** 2 for i in K) + 5 * len(K)) % 19 - 9, 3000) for K in sups6b}

    def ml_case(Yt, outside_only):
        Y6 = frozenset(Yt)
        cB6 = {K: (cA6[K] if (outside_only and (K & Y6)) else cA6[K] + Q((7 * sum(i + 1 for i in K) + len(K)) % 13 - 6, 30000)) for K in sups6b}
        dlt = {K: abs(cB6[K] - cA6[K]) for K in sups6b}
        tt = max(max(sum(abs(c[K]) for K in sups6b if x in K) for x in range(n6)) for c in (cA6, cB6))
        tb = max(max(sum(wk ** (max(K) - min(K)) * bk ** len(K) * abs(c[K]) for K in sups6b if x in K) for x in range(n6)) for c in (cA6, cB6))
        aa = tb ** 2
        require(tb <= 1 and aa <= 2 * ceil_log_free_b_lower(bk), 'KP condition for the Lemma 7.1 audit')
        Svw_t = S_sum(vk / wk)
        A_t = 2 * tb ** 2 + aa * (1 + 2 * tb ** 2 * Svw_t)
        k0_t = 4 * tb + 2 * A_t * (tt + tb * (Svw_t - 1))
        D = {x: sum(dlt[K] for K in sups6b if x in K) for x in range(n6)}
        lead = 2 * (1 + tt) ** (len(Y6) - 1) * sum(dlt[K] for K in sups6b if K & Y6)
        far = (1 + tt) ** (2 * len(Y6)) * k0_t * sum(sum(vk ** (-d1(x, y)) for y in Y6) * D[x] for x in range(n6) if x not in Y6)
        diff = mat_diff(rho_qubit(cA6, Y6, range(n6)), rho_qubit(cB6, Y6, range(n6)))
        lhs_sq = trace_norm_sq_2x2_hermitian(diff) if len(Y6) == 1 else 2 ** len(Y6) * hs2(diff)
        require(lhs_sq <= (lead + far) ** 2, 'Lemma 7.1 bound violated on the finite chain')
        return {'Y': list(Yt), 'outside_only': outside_only, 'lhs_squared_upper': dec(lhs_sq, 6), 'bound': dec(lead + far, 6)}
    audit['lemma_7_1'] = [ml_case((2,), True), ml_case((2,), False), ml_case((2, 3), True)]
    check('polymer_kp_lemmas_audited_on_finite_graphs', True, record=audit)

    # ---------------- constants of the frozen pairs (report sections 6-10), both signs ---------------
    head = {sg: pair_constants(P, V, t, 'headline', 'exact_first_order') for sg, t in taus.items()}
    sec = {sg: pair_constants(P, V, t, 'secondary', 'exact_first_order') for sg, t in taus.items()}
    head_crude = {sg: pair_constants(P, V, t, 'headline', 'crude_majorant') for sg, t in taus.items()}
    sec_crude = {sg: pair_constants(P, V, t, 'secondary', 'crude_majorant') for sg, t in taus.items()}
    for grp in (head, sec, head_crude, sec_crude):
        for key in ('C', 'c_site', 'K', 'taub', 'a', 'kappa0'):
            require(grp['+'][key] == grp['-'][key], 'the -tau value replays the same |tau| formula')
    hp, sp, hc, sc = head['+'], sec['+'], head_crude['+'], sec_crude['+']
    require(hp['K'] == P['ba1_K'], 'headline input = gate bound value')
    require(hp['q'] == V['q_head'] and sp['q'] == V['q2_per_tau'] * tau_cap, 'frozen rates')
    require(hp['region_rate_ok'] and sp['region_rate_ok'], 'exact-tier region exponential rate 2t + t^2 <= 1/10^8')
    require(not hc['region_rate_ok'], 'crude-tier anchored norm exceeds the region rate (reported)')
    kp_rec = {}
    for name, pc in (('headline', hp), ('secondary', sp), ('headline_crude', hc), ('secondary_crude', sc)):
        kp_rec[name] = {'tier': pc['tier'], 'route': 'polymer_kp', 'w': s(pc['w']), 'v': s(pc['v']), 'e_b': s(BETA),
                        'loss_w_e4b': s(pc['what']), 'w_max': s(pc['wmax']), 'Gamma': s(pc['gamma']),
                        't_anchored': s(pc['t']), 'taubar_mixed': s(pc['taub']), 'taubar_preview': dec(pc['taub']),
                        'a': s(pc['a']), 'a_preview': dec(pc['a']), 'b_lower': s(pc['b_low']),
                        'kp_condition': 'sum_{gamma ni x} |w(gamma)| e^{a|supp gamma| + mu sum diam} <= taubar^2 <= a, a <= 2b, v <= w',
                        'S_v_over_w': s(pc['Svw']), 'S_1_over_qv': s(pc['Sq'])}
    check('kotecky_preiss_condition_and_tree_majorant', True, record=kp_rec,
          activity_bound='|w(gamma)| <= product over the members of gamma of the creation norms (Cauchy-Schwarz)',
          tree_majorant='exploration tree: at each step the member containing the least unbalanced site is summed at cost <= taubar (Lemma 4.1); '
                        'polymers through a site cost <= taubar^2; the KP tree-graph majorant carries the cardinality factor a|supp gamma|')

    lemma = {'form': "||rho_Y(c)-rho_Y(c')||_1 <= 2(1+eta) sum_{I meets Y} ||c_I-c'_I|| + sum_{I misses Y} kappa(I) ||c_I-c'_I||",
             'eta': '(1+t)^{|Y|-1} - 1 (eta_R = t)', 'kappa': 'kappa(I) <= (1+t)^{2|Y|} kappa_0 sum_{x in I} sum_{y in Y} v^{-d(x,y)} <= kappa_0(Y) |I| v^{-d_inf(I,Y)}',
             'kappa0': '4 taubar + 2 A (t + taubar (S_{v/w} - 1)), A = 2 taubar^2 + a (1 + 2 taubar^2 S_{v/w})',
             'kappa0_Y': '(1+t)^{2|Y|} |Y| kappa_0', "w_prime": 'v', 'p': 'p(s) = s',
             'activity_bounds': True, 'combinatorial_counts': 'exploration tree (Lemma 4.1) and lattice sums S_x = 1 + 24x(1+x)/(1-x)^3 + 2x/(1-x)',
             'values': {name: {'eta_R': s(pc['eta_R']), 'kappa0': s(pc['kappa0']), 'kappa0_preview': dec(pc['kappa0']),
                               'kappa0_R_contract': s(pc['kappa0_contract_R']), 'w_prime': s(pc['v']), 'p': 's', 'tier': pc['tier'],
                               'route': 'polymer_kp'} for name, pc in (('headline', hp), ('secondary', sp), ('headline_crude', hc))}}

    def lemma_ok(rec):
        for key in ('eta', 'kappa0', 'w_prime', 'p', 'activity_bounds', 'combinatorial_counts'):
            require(rec.get(key), 'marginal-locality lemma constant missing: ' + key)
        require(rec['p'] == 'p(s) = s' and rec['w_prime'] == 'v', 'explicit polynomial and rate')
        for name in ('headline', 'secondary'):
            val = rec['values'][name]
            require(rat(val['kappa0']) > 0 and rat(val['w_prime']) > 1, 'positive constants')
        return True
    check('marginal_locality_constants_explicit',
          lemma_ok(lemma)
          and rejected(lambda: lemma_ok(dict(lemma, activity_bounds=False)), 'kp_criterion_asserted_without_activity_bounds')
          and rejected(lambda: lemma_ok(dict(lemma, combinatorial_counts='')), 'kp_criterion_without_combinatorial_counts')
          and rejected(lambda: lemma_ok({k: v for k, v in lemma.items() if k != 'p'}), 'polynomial_p_not_named')
          and rejected(lambda: lemma_ok(dict(lemma, eta='')), 'eta_not_named'),
          lemma=lemma)

    # ---------------- zero-free region: analyticity of the reduced density is never claimed ---------
    zf_point = (Q(0), Q(1, 2))                      # z = i/2 as a Gaussian rational (re, im)
    z2 = (zf_point[0] ** 2 - zf_point[1] ** 2, 2 * zf_point[0] * zf_point[1])
    norm_cont = (1 + 4 * z2[0], 4 * z2[1])          # continuation of ||Omega - 2 z |11>||^2 = 1 + 4 z^2
    require(norm_cont == (0, 0) and zf_point[1] ** 2 + zf_point[0] ** 2 <= 1, 'normalization vanishes inside the unit disc')
    ANALYTIC = {'reduced_density_analyticity_claimed': False, 'zero_free_region_proved': False,
                'parameter': 'real lambda in [0,1] along c + lambda (c\' - c) only; Z_lambda(Lambda) >= 1 on real lambda'}

    def analytic_ok(rec):
        require(not (rec['reduced_density_analyticity_claimed'] and not rec['zero_free_region_proved']),
                'analyticity of the reduced density without a proved zero-free region')
        require(rec['parameter'].startswith('real lambda'), 'real-parameter derivative only')
        return True
    check('zero_free_region_required',
          analytic_ok(ANALYTIC)
          and rejected(lambda: analytic_ok(dict(ANALYTIC, reduced_density_analyticity_claimed=True)), 'analyticity_claimed_without_zero_free_region')
          and rejected(lambda: analytic_ok(dict(ANALYTIC, parameter='complex lambda in the unit disc')), 'complex_parameter_derivative'),
          model_is_finite_graph=True, transfers_to_aq=False, fixture='psi(z) = Omega - 2z|11>: the continuation 1 + 4z^2 of the norm vanishes at z = i/2',
          record=ANALYTIC)

    # ---------------- headline R form, region form, secondary pair, crude tier (report section 9) -----
    head_met = hp['C'] <= V['C_target'] and hp['c_site'] <= V['cs_target']
    sec_met = sp['C'] <= V['C2_target'] and sp['c_site'] <= V['cs2_target']
    crude_met = hc['C'] <= V['C_target'] and hc['c_site'] <= V['cs_target'] and hc['region_rate_ok']
    require(head_met and sec_met and not crude_met, 'target outcomes')
    comp_notes = [
        'sources: whole stars b+S in Lambda_(N+1) not in Lambda_N; nearest source site (0,0,N), distance N-1 from e_z',
        'sources: faces with owner set in Lambda_(N+1) and not in Lambda_N, charged face by face; distance N-1 from e_z',
        'fixed N, changed exterior: the 28N(5N+1) extra F2 faces on the outer layer of Lambda_N; distance N-1 from e_z',
        'compared directly on the union volume (no telescoping); every source face at distance at least N-|u|_inf from u',
        'compared directly on the union volume; the union route (each volume against the union) costs a factor 2 and is labelled only',
    ]
    comparisons = {}
    for i, name in enumerate(V['comparisons']):
        comparisons[name] = {'C': s(hp['C']), 'C_preview': dec(hp['C']), 'c_site': s(hp['c_site']), 'c_site_preview': dec(hp['c_site']),
                             'per_sign': {sg: {'C': s(head[sg]['C']), 'c_site': s(head[sg]['c_site'])} for sg in taus},
                             'secondary': {'C': s(sp['C']), 'c_site': s(sp['c_site'])}, 'crude': {'C': s(hc['C'])},
                             'exponent_at_e_z': 'N-1', 'note': comp_notes[i]}
    comparisons[V['comparisons'][4]]['labelled_union_form'] = {'C': s(2 * hp['C']), 'c_site': s(2 * hp['c_site']), 'status': 'labelled only'}

    def pair_ok(C, cs, Ct, cst):
        require(C <= Ct and cs <= cst, 'constant above its frozen target')
        return True
    check('headline_R_form_every_comparison_both_signs',
          all(pair_ok(head[sg]['C'], head[sg]['c_site'], V['C_target'], V['cs_target']) for sg in taus),
          C=s(hp['C']), C_preview=dec(hp['C']), target=s(V['C_target']), margin=dec(V['C_target'] / hp['C'], 6),
          tier='exact_first_order', route='polymer_kp', ba1_input='gate bound value K=49/111790368 (analytic_disc), every-site form (b)',
          comparisons=sorted(comparisons))
    region_cases = []
    for N in (2, 3, 4, 6):
        for label, norms in (('R', [0, 1]), ('{0}', [0]), ('Lambda_1', [0] + [1] * 26)):
            region_target_ok(hp, norms, N, hp['c_site'], V['region_rate'])
            region_target_ok(sp, norms, N, sp['c_site'], V['region_rate'])
            region_cases.append(label + ' at N=' + str(N))
    region_target_ok(hp, [0] + [1] * 26 + [2] * 98, 2, hp['c_site'], V['region_rate'])
    region_cases.append('Lambda_2 at N=2 (d_Y = 0)')
    require(region_bound(hp, [0, 1], 5) == hp['C'] * hp['q'] ** 4, 'region bound on R equals the R form')
    check('region_form_every_comparison_both_signs',
          all(pair_ok(head[sg]['C'], head[sg]['c_site'], V['C_target'], V['cs_target']) for sg in taus),
          c_site=s(hp['c_site']), c_site_preview=dec(hp['c_site']), target=s(V['cs_target']), margin=dec(V['cs_target'] / hp['c_site'], 6),
          rate_condition='(1+t)^2 <= 1 + 1/10^8 with t = ' + s(hp['t']), exact_region_cases=region_cases)
    check('fixed_N_F1_versus_F2_item', pair_ok(hp['C'], hp['c_site'], V['C_target'], V['cs_target']),
          comparison=V['comparisons'][2], C=s(hp['C']), c_site=s(hp['c_site']),
          source='the 28N(5N+1) extra F2 faces (616, 1344, 2352 at N=2,3,4), all on the outer layer of Lambda_N, at distance N-1 from e_z and N from 0')
    check('one_prescription_volumes_compared_directly', pair_ok(hp['C'], hp['c_site'], V['C_target'], V['cs_target']),
          comparison=V['comparisons'][4], C=s(hp['C']), labelled_union_C=s(2 * hp['C']), labelled_union_c_site=s(2 * hp['c_site']),
          enumerated=[r['comparison'] for r in geom_rows if 'one prescription' in r['comparison']])
    check('secondary_pair_labelled', all(pair_ok(sec[sg]['C'], sec[sg]['c_site'], V['C2_target'], V['cs2_target']) for sg in taus),
          q='151552|tau|', C=s(sp['C']), C_preview=dec(sp['C']), c_site=s(sp['c_site']), c_site_preview=dec(sp['c_site']),
          targets=[s(V['C2_target']), s(V['cs2_target'])], margins=[dec(V['C2_target'] / sp['C'], 6), dec(V['cs2_target'] / sp['c_site'], 6)],
          status='labelled secondary pair; the headline decides the loop', ba1_input='analytic_disc re-instantiated at rho=1/151552, K=' + s(sp['K']))
    check('crude_tier_reported_separately', not crude_met,
          C_crude=s(hc['C']), C_crude_preview=dec(hc['C']), c_site_crude_formula=s(hc['c_site']),
          region_rate_condition_fails='(1+t_crude)^2 > 1 + 1/10^8, t_crude = ' + s(hc['t']),
          secondary_crude_C=s(sc['C']), status='reported, never a target; fails 1/250000 and has no c_site in the frozen form')

    # ---------------- cutoff: uniform in L, then removed at fixed N (never exchanged) -----------------
    CUTOFF = {'order': ['each on-site cutoff space Q_L with constants independent of L', 'then L to infinity at fixed N and fixed volumes',
                        'no limit in N is taken in this loop'],
              'vector_removal': 'AV1 F20-F23 (Eckart with the untruncated gap 1/2) for F1; AY1 itemization for F2 with padding and general volumes',
              'constants_depend_on_L': False}

    def cutoff_ok(rec):
        require(rec['order'][0].startswith('each on-site cutoff space Q_L') and rec['order'][1].startswith('then L to infinity at fixed N'),
                'cutoff bound first, removal at fixed N second')
        require(rec['constants_depend_on_L'] is False, 'constants must be uniform in L')
        return True
    check('cutoff_uniform_then_removed',
          cutoff_ok(CUTOFF)
          and rejected(lambda: cutoff_ok(dict(CUTOFF, order=list(reversed(CUTOFF['order'][:2])) + CUTOFF['order'][2:])), 'limits_reversed')
          and rejected(lambda: cutoff_ok(dict(CUTOFF, constants_depend_on_L=True)), 'cutoff_dependent_constant'),
          record=CUTOFF, face_vector_site_energy_max=face_energy_max, L_exact=P['L_exact'])
    # Eckart-type vector bound 1 - |<psi, v>|^2/|v|^2 <= (E(v) - E_0)/gap on a rational 3x3 fixture with gap 1/2
    Hdiag = [Q(0), Q(1, 2), Q(1)]
    eck = []
    for vv in ((Q(1), Q(1, 3), Q(1, 4)), (Q(1), Q(1), Q(0)), (Q(1, 2), Q(0), Q(1)), (Q(0), Q(1), Q(0))):
        nrm = sum(x * x for x in vv)
        lhs = 1 - vv[0] ** 2 / nrm
        energy = sum(h * x * x for h, x in zip(Hdiag, vv)) / nrm
        require(lhs <= (energy - Hdiag[0]) / (Hdiag[1] - Hdiag[0]), 'Eckart bound')
        eck.append([s(lhs), s((energy - Hdiag[0]) / (Hdiag[1] - Hdiag[0]))])

    def vector_removal_ok(gap, overlap_defect, energy_excess):
        require(gap > 0, 'vector removal needs a positive untruncated gap')
        require(overlap_defect <= energy_excess / gap, 'overlap defect above the Eckart bound')
        return True
    check('cutoff_vector_removal',
          vector_removal_ok(Q(1, 2), Q(0), Q(0))
          and rejected(lambda: vector_removal_ok(Q(0), Q(1), Q(0)), 'eigenvalue_convergence_used_for_vectors_without_gap'),
          model_is_finite_graph=True, transfers_to_aq=False, eckart_pairs=eck,
          counterexample="H' = diag(0,0,1): e_2 has the ground energy and is orthogonal to e_1 (gap 0)")
    # cutoff-limit order: a(N,L) = (1 - 2^-L)^((2N+1)^3); lim_L then lim_N gives 1, lim_N then lim_L gives 0
    a_NL = lambda N, L: (1 - Q(1, 2 ** L)) ** ((2 * N + 1) ** 3)
    lower_fixedN = 1 - Q(27, 2 ** 60)
    require(a_NL(1, 60) >= lower_fixedN, 'fixed N: a -> 1 as L grows (Bernoulli)')
    require(a_NL(6, 6) < Q(1, 10 ** 14), 'fixed L: a -> 0 as N grows')

    def limit_order_ok(rec):
        require(rec == ['L to infinity at fixed N', 'bound passes to the untruncated vector', 'N fixed throughout'], 'limit order')
        return True
    check('cutoff_limit_order',
          limit_order_ok(['L to infinity at fixed N', 'bound passes to the untruncated vector', 'N fixed throughout'])
          and rejected(lambda: limit_order_ok(['N to infinity at fixed L', 'then L to infinity', 'limits exchanged']), 'n_and_l_limits_exchanged'),
          model_is_finite_graph=True, transfers_to_aq=False,
          fixture='a(N,L) = (1-2^-L)^((2N+1)^3): a(1,60) >= 1 - 27/2^60, a(6,6) < 10^-14')
    UNTRUNC = {'statement': 'for fixed N and fixed volumes A, B: ||rho^A_Y - rho^B_Y||_1 <= ||rho^A_Y - rho^A_{L,Y}||_1 + C q^(N-1) '
                            '+ ||rho^B_{L,Y} - rho^B_Y||_1 for every L, and the outer terms tend to 0 as L grows at fixed N (F22)',
               'inputs': ['AM2 section 6 (untruncated simple ground, gap >= 1/2) for every finite volume of F1',
                          'AY1 item-by-item verification for F2 with padding (includes cutoff-vector removal)',
                          'AV1 F22: 1 - |(psi, psi_L)|^2 is at most 2 (E_{0,L} - E_0), which tends to 0; pure-state trace distance and partial-trace contraction']}
    check('untruncated_ground_vectors_at_fixed_N', True, record=UNTRUNC, C=s(hp['C']), c_site=s(hp['c_site']))

    # ---------------- trap fixtures (all model_is_finite_graph: true, transfers_to_aq: false) -----------
    FIX = {'model_is_finite_graph': True, 'transfers_to_aq': False}
    # coefficient decay is not marginal decay (AV1 F13 type)
    def f13(bval):
        return rho_qubit({frozenset({0, 1}): Q(1, 3), frozenset({1}): bval, frozenset({2}): Q(2, 5)}, {0}, [0, 1, 2])
    rho_b, rho_0 = f13(Q(1, 2)), f13(Q(0))
    require(rho_b == {((0,), (0,)): Q(45, 49), ((0,), (1,)): Q(6, 49), ((1,), (0,)): Q(6, 49), ((1,), (1,)): Q(4, 49)}, 'F13 marginal b=1/2')
    require(rho_0 == {((0,), (0,)): Q(9, 10), ((1,), (1,)): Q(1, 10)}, 'F13 marginal b=0')

    def infer_marginal_from_coefficients(r1, r2, coeff_diff_on_R):
        require(not (coeff_diff_on_R == 0 and r1 != r2), 'equal coefficients on supports meeting R do not give equal marginals')
        return True
    check('coefficient_decay_not_marginal_decay',
          infer_marginal_from_coefficients(rho_b, rho_b, 0)
          and rejected(lambda: infer_marginal_from_coefficients(rho_b, rho_0, 0), 'state_decay_inferred_from_equal_coefficients'),
          fixture=dict(FIX, sites='r, o, o\'', creations='c_{r,o}=1/3 (straddling), c_o=b, c_{o\'}=2/5',
                       rho_b_half=[['45/49', '6/49'], ['6/49', '4/49']], rho_b_zero=[['9/10', '0'], ['0', '1/10']],
                       trace_norm_squared_difference=s(tn2_sq([[Q(45, 49) - Q(9, 10), Q(6, 49)], [Q(6, 49), Q(4, 49) - Q(1, 10)]]))))
    # second-order propagation along the chain r - o1 - o2 (c_{r o1} = a, c_{o1 o2} = b, c_{o2} = g)
    amps = {frozenset({0, 1}): {(1, 0, 0): Q(1)}, frozenset({1, 2}): {(0, 1, 0): Q(1)}, frozenset({2}): {(0, 0, 1): Q(1)}}
    num = marginal_numerators(psi_symbolic(amps, 3), {0})
    N01 = num[((0,), (1,))]
    require(N01 == {(1, 1, 1): Q(-1)}, 'off-diagonal numerator is exactly -a b g')
    dN01_dg = {(1, 1, 0): Q(-1)}
    Zpoly = padd(num[((0,), (0,))], num[((1,), (1,))])

    def rho_at(av, bv, gv):
        z = peval(Zpoly, (av, bv, gv))
        return [[peval(num[((i,), (j,))], (av, bv, gv)) / z for j in (0, 1)] for i in (0, 1)]
    r1, r2 = rho_at(Q(1, 3), Q(1, 4), Q(1, 2)), rho_at(Q(1, 3), Q(1, 4), Q(0))
    dmat = [[r1[i][j] - r2[i][j] for j in (0, 1)] for i in (0, 1)]
    require(tn2_sq(dmat) > 0, 'the change two supports away moves the R-marginal')
    require(rho_at(Q(1, 3), Q(0), Q(1, 2)) == rho_at(Q(1, 3), Q(0), Q(0)), 'no middle link: no propagation')

    def propagation_claim_ok(claimed):
        require(claimed == dN01_dg, 'claimed propagation polynomial differs from the exact -a b')
        return True

    def per_link_factor_ok(factor):
        require(factor >= 1, 'per-link factor below the exact one (the coefficient of a b is exactly 1)')
        return True
    check('fixture_second_order_propagation',
          propagation_claim_ok({(1, 1, 0): Q(-1)}) and per_link_factor_ok(Q(1))
          and rejected(lambda: propagation_claim_ok({(1, 0, 0): Q(-1)}), 'first_order_propagation_claim')
          and rejected(lambda: per_link_factor_ok(Q(1, 2)), 'per_link_factor_below_exact'),
          fixture=dict(FIX, chain='r - o1 - o2', off_diagonal_numerator='-a b g', derivative_in_g='-a b',
                       change_trace_norm_squared=s(tn2_sq(dmat)), at='a=1/3, b=1/4, g: 1/2 -> 0', middle_link_zero='b=0 gives no change'))
    # straddling supports and the normalization (R = {r0, r1}, outside o; single amplitude eps)
    strad = {}
    for label, I in (('one_site_straddling', frozenset({0, 2})), ('strictly_containing_R', frozenset({0, 1, 2})), ('equal_to_R', frozenset({0, 1}))):
        nm = marginal_numerators(psi_symbolic({I: {(1,): Q(1)}}, 1), {0, 1})
        first = {str(k): s(v.get((1,), 0)) for k, v in sorted(nm.items()) if v.get((1,), 0) != 0}
        second = {str(k): s(v.get((2,), 0)) for k, v in sorted(nm.items()) if v.get((2,), 0) != 0}
        strad[label] = {'first_order_R_marginal': first, 'second_order_R_marginal': second}
    require(not strad['one_site_straddling']['first_order_R_marginal'] and not strad['strictly_containing_R']['first_order_R_marginal'],
            'straddling supports have zero first-order R-marginal')
    require(strad['equal_to_R']['first_order_R_marginal'], 'a support equal to R has a first-order R-marginal')
    require(strad['one_site_straddling']['second_order_R_marginal'] == {'((1, 0), (1, 0))': '1'}
            and strad['strictly_containing_R']['second_order_R_marginal'] == {'((1, 1), (1, 1))': '1'}, 'second-order blocks')
    # e is first order in the straddling amplitude a while the off-diagonal element is second order (a b)
    amps2 = {frozenset({0, 1}): {(1, 0): Q(1)}, frozenset({1}): {(0, 1): Q(1)}}
    num2 = marginal_numerators(psi_symbolic(amps2, 2), {0})
    require(num2[((0,), (1,))] == {(1, 1): Q(1)} and num2[((1,), (1,))] == {(2, 0): Q(1)}, 'off-diagonal a b, excited block a^2')
    psi_full2 = psi_symbolic(amps2, 2)
    psi_out2 = psi_symbolic({frozenset({1}): {(0, 1): Q(1)}}, 2)
    delta2 = {e: padd(psi_full2.get(e, {}), pscale(psi_out2.get(e, {}), -1)) for e in set(psi_full2) | set(psi_out2)}
    e_sq_num = {}
    for pol in delta2.values():
        e_sq_num = padd(e_sq_num, pmul(pol, pol))
    require(e_sq_num == {(2, 0): Q(1)}, '||delta||^2 = a^2: e = |a|/sqrt(1+b^2) is first order in a')

    def split_ok(keep_straddling, normalization):
        require(keep_straddling, 'straddling supports dropped from the split')
        require(normalization == 'product split: outside vector common factor', 'normalization by 1+O(t^2) without the split')
        return True
    naive = lambda gv: Q(1) / ((1 + gv ** 2) * (1 + Q(1, 9) + Q(1, 4)))
    require(naive(Q(0)) != naive(Q(2, 5)), 'numerator restricted to supports meeting R over the full norm depends on a decoupled spectator')

    def straddle_order_ok(claimed_degree):
        require(claimed_degree == 2, 'the straddling creation enters the off-diagonal element at second order (a b)')
        return True
    check('normalization_couples_supports',
          split_ok(True, 'product split: outside vector common factor') and straddle_order_ok(2)
          and rejected(lambda: split_ok(False, 'product split: outside vector common factor'), 'straddling_supports_dropped')
          and rejected(lambda: split_ok(True, '1+O(t^2) without the split'), 'normalized_by_one_plus_t_squared')
          and rejected(lambda: straddle_order_ok(1), 'straddling_charged_only_at_first_order'),
          fixture=dict(FIX, straddling=strad, e_squared_numerator='a^2 (e first order in a)', off_diagonal_numerator='a b',
                       spectator_dependence_of_naive_value=[s(naive(Q(0))), s(naive(Q(2, 5)))]))
    # split route: Tr N_c(omega) >= 1 and ||rho(omega)-rho(omega')||_1 <= 2||N(omega-omega')||_1 on a mixed outside state
    amps_r = [((0,), Q(1, 5)), ((0, 1), Q(1, 4)), ((0, 2), Q(-1, 6)), ((0, 1, 2), Q(1, 7))]
    Tm = [[Q(1) if i == j else Q(0) for j in range(8)] for i in range(8)]
    for I, amp in amps_r:
        Cm = creation_matrix(3, I, amp)
        Tm = mmul(Tm, [[(Q(1) if i == j else Q(0)) - Cm[i][j] for j in range(8)] for i in range(8)])
    Dm = [[Tm[i][j] - (1 if i == j else 0) for j in range(8)] for i in range(8)]
    Pr = [[Q(1), Q(0)], [Q(0), Q(0)]]
    om1 = density_from([(Q(1), Q(1, 2), Q(0), Q(1, 3)), (Q(1, 2), Q(0), Q(1), Q(-1, 4))], [Q(1, 2), Q(1, 2)])
    om2 = density_from([(Q(1), Q(0), Q(1, 5), Q(0)), (Q(0), Q(1), Q(1, 3), Q(1, 2))], [Q(2, 3), Q(1, 3)])

    def Nmap(om):
        return partial_trace_keep_first(mmul(mmul(Tm, kron(Pr, om)), mT(Tm)), 2, 4)
    N1, N2 = Nmap(om1), Nmap(om2)
    tr1, tr2 = N1[0][0] + N1[1][1], N2[0][0] + N2[1][1]
    DPD = partial_trace_keep_first(mmul(mmul(Dm, kron(Pr, om1)), mT(Dm)), 2, 4)
    require(tr1 == 1 + DPD[0][0] + DPD[1][1] and tr1 >= 1 and tr2 >= 1, 'Tr N_c(omega) = 1 + Tr[D (P x omega) D*] >= 1')
    dom = [[om1[i][j] - om2[i][j] for j in range(4)] for i in range(4)]
    Nd = Nmap(dom)
    drho = [[N1[i][j] / tr1 - N2[i][j] / tr2 for j in range(2)] for i in range(2)]
    epsY = sum(abs(a) for _, a in amps_r)
    hs_dom = sum(x * x for row in dom for x in row)

    def split_lipschitz_ok(factor):
        require(tn2_sq(drho) <= factor ** 2 * tn2_sq(Nd), 'normalization Lipschitz ||rho(w)-rho(w\')|| <= 2||N(w-w\')||')
        require(tn2_sq(Nd) <= (2 * epsY + epsY ** 2) ** 2 * hs_dom, 'omega-Lipschitz ||N(X)||_1 <= (2 eps + eps^2)||X||')
        return True
    theta = Q(1, 64)
    per_site_charge = [sum(lattice_shell_count(j) * theta ** j for j in range(k + 1)) for k in range(9)]
    prod_charge = []
    acc = Q(1)
    for k in range(9):
        acc *= (2 * k + 1) ** 3
        prod_charge.append(acc * theta ** k)
    cap = S_sum(theta)

    def charging_ok(charges):
        require(all(c <= cap for c in charges), 'split charge exceeds the uniform per-site bound (growing region sizes)')
        return True
    check('fixture_split_lipschitz_and_trace',
          split_lipschitz_ok(Q(2)) and charging_ok(per_site_charge)
          and rejected(lambda: split_lipschitz_ok(Q(1, 4)), 'normalization_lipschitz_factor_quartered')
          and rejected(lambda: charging_ok(prod_charge), 'product_of_growing_region_sizes_charged'),
          fixture=dict(FIX, Y='{r}', outside='{o1,o2}', creations_meeting_Y={str(list(I)): s(a) for I, a in amps_r},
                       trace_N=[s(tr1), s(tr2)], lhs_squared=s(tn2_sq(drho)), rhs_squared=s(4 * tn2_sq(Nd)), eps_Y=s(epsY),
                       per_site_charge_cap=s(cap), product_charge_depth_8=dec(prod_charge[-1], 6)))
    # global fidelity: product states, the global overlap collapses while one-site marginals stay close
    F1f = Q(6561, 6565)
    require(F1f == (1 + Q(1, 80)) ** 2 / ((1 + Q(1, 100)) * (1 + Q(1, 64))), 'one-site fidelity')
    glob = {n: 4 * (1 - F1f ** n) for n in (1, 100, 200, 400)}
    require(glob[1] < glob[100] < glob[200] < glob[400] and glob[400] > 100 * glob[1], 'global bound grows with the volume')

    def global_overlap_bound_ok(values):
        ks = sorted(values)
        require(all(values[ks[i + 1]] <= values[ks[i]] for i in range(len(ks) - 1)), 'a bound through the global overlap does not decay in N')
        return True
    check('global_fidelity_orthogonality_catastrophe',
          global_overlap_bound_ok({1: Q(1), 2: Q(1, 64)})
          and rejected(lambda: global_overlap_bound_ok(glob), 'bound_through_global_overlap'),
          fixture=dict(FIX, phi='(1, 1/10)', phi_prime='(1, 1/8)', one_site_fidelity=s(F1f),
                       squared_marginal_distance=s(glob[1]), squared_global_bound_n400_preview=dec(glob[400], 6)))
    # the outside vector is not a ground state: chain y - o1 - o2, bonds g X X, orders 1..3
    full = rs_ground(3, [(0, 1), (1, 2)], 3)
    outs = rs_ground(2, [(0, 1)], 3)
    c_full = [-full[n].get((0, 1, 1), Q(0)) for n in (1, 2, 3)]
    c_out = [-outs[n].get((1, 1), Q(0)) for n in (1, 2, 3)]
    require(c_full[0] == c_out[0] and c_full[2] != c_out[2], 'restricted coefficient differs from the outside ground coefficient at order 3')

    def outside_vector_ok(rec):
        require(not rec.get('gap_argument_applied_to_phi_out'), 'a gap argument applied to the outside vector')
        require(rec.get('phi_out') == 'restriction of the box coefficient family to supports missing Y', 'phi_out definition')
        return True
    OUTREC = {'phi_out': 'restriction of the box coefficient family to supports missing Y', 'gap_argument_applied_to_phi_out': False}
    check('outside_vector_not_ground_state',
          outside_vector_ok(OUTREC)
          and rejected(lambda: outside_vector_ok(dict(OUTREC, gap_argument_applied_to_phi_out=True)), 'outside_gap_argument')
          and rejected(lambda: outside_vector_ok(dict(OUTREC, phi_out='ground state of the outside Hamiltonian')), 'phi_out_called_ground_state'),
          fixture=dict(FIX, chain='y - o1 - o2 with g X X bonds', c_o1o2_full_orders_1_to_3=[s(x) for x in c_full],
                       c_o1o2_outside_ground_orders_1_to_3=[s(x) for x in c_out]))
    # global Lipschitz constants are not decay factors
    no_decay = P['J0'] * P['GR'] / (1 - P['J0'] * P['GpR'])
    require(no_decay == V['no_decay'] and P['JGp'] == V['lip_map'] and P['twoJGp'] == V['lip_excl'], 'no-decay bound and Lipschitz constants')
    omega_lip_R = 2 * (2 * ((1 + hp['t']) ** 2 - 1) + ((1 + hp['t']) ** 2 - 1) ** 2)
    mf = []
    for pos in range(1, 6):
        s_vec = [Q(1) if i == pos else Q(0) for i in range(6)]
        mean_c = 2 * sum(s_vec) / 6
        mf.append(mean_c / 2 + s_vec[0])
    require(all(x == Q(1, 6) for x in mf), 'mean-field fixture: c_0 = 1/6 for every source position')

    def decay_factor_ok(source):
        require(source == 'q from the every-site coefficient input and v^{-d} from the polymer weights', 'decay must not come from a Lipschitz constant')
        return True
    check('global_lipschitz_not_decay',
          decay_factor_ok('q from the every-site coefficient input and v^{-d} from the polymer weights')
          and rejected(lambda: decay_factor_ok('J_0 G\'(R) per shell'), 'map_lipschitz_as_per_shell_factor')
          and rejected(lambda: decay_factor_ok('omega-Lipschitz 2(2 eps_R + eps_R^2) per shell'), 'omega_lipschitz_as_decay')
          and rejected(lambda: require(all(x <= Q(1, 2) ** 5 for x in mf), 'mean-field decay claim false'), 'lipschitz_half_claimed_decay'),
          no_decay_bound=s(no_decay), map_lipschitz=s(P['JGp']), exclusion_constant=s(P['twoJGp']), omega_lipschitz_R=s(omega_lip_R),
          fixture=dict(FIX, map='T(c)_i = (1/2) mean(c) + s_i on six sites', c_0_for_every_source_position='1/6'))
    # topology: trace norm on B(H_Y); fixed-vector versus moving-vector fixture
    fixed = [Q(1, 4) ** n for n in range(1, 12)]
    moving = [Q(1) for n in range(1, 12)]
    require(fixed[-1] < Q(1, 10 ** 6) and all(x == 1 for x in moving), 'fixed vector decays, moving vector does not')

    def topology_ok(top, moving_claim):
        require(top.startswith('trace norm on B(H_Y)'), 'state topology must be the trace norm on B(H_Y)')
        require(moving_claim is False, 'strong convergence does not give convergence along moving vectors')
        return True
    check('topology_named',
          topology_ok(TOPOLOGY, False)
          and rejected(lambda: topology_ok('Hilbert-Schmidt norm of the global vectors', False), 'wrong_state_topology')
          and rejected(lambda: topology_ok(TOPOLOGY, True), 'moving_vector_convergence_claimed'),
          topology=TOPOLOGY, fixture=dict(FIX, operators='A_n = |e_n><e_n| on C^12', fixed='||A_n psi||^2 = 4^-n', moving='||A_n e_n|| = 1'))
    # subsequence versus whole sequence
    xs = [(-1) ** n * (1 + Q(1, n)) for n in range(1, 41)]
    require(all(abs(xs[i + 1] - xs[i]) >= 2 for i in range(len(xs) - 1)), 'alternating sequence is not Cauchy')
    require(abs(xs[-1] - 1) < Q(1, 30) and abs(xs[-2] + 1) < Q(1, 30), 'its even and odd subsequences converge')

    # ---------------- claim flags and gate fields -------------------------------------------------------
    GATE = dict(V['gate_fields'])
    CLAIMS = {'continuum_claim': False, 'uniqueness_of_ground_state_claimed': False, 'rate_in_a_claimed': False,
              'scientific_priority_verified': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
              'reduced_density_analyticity_claimed': False}

    def claims_ok(cl, gf):
        for k, val in CLAIMS.items():
            require(cl.get(k) is val, 'claim flag ' + k + ' must be ' + str(val))
        require(gf == V['gate_fields'], 'gate fields differ from the contract gate_fields_required')
        require(gf['whole_sequence_claimed'] is False and gf['common_limit_claimed'] is False, 'no whole-sequence or common-limit claim')
        require(gf['uniqueness_of_ground_state_claimed'] is False, 'no uniqueness claim')
        return True
    check('no_priority_or_continuum_claim',
          claims_ok(dict(CLAIMS), dict(GATE))
          and rejected(lambda: claims_ok(dict(CLAIMS, continuum_claim=True), GATE), 'continuum_claim_true')
          and rejected(lambda: claims_ok(dict(CLAIMS, scientific_priority_verified=True), GATE), 'priority_verified_true'),
          flags=CLAIMS)
    check('subsequence_versus_whole_sequence',
          claims_ok(CLAIMS, GATE)
          and rejected(lambda: claims_ok(CLAIMS, dict(GATE, whole_sequence_claimed=True)), 'whole_sequence_claimed_from_per_comparison_bounds')
          and rejected(lambda: claims_ok(CLAIMS, dict(GATE, common_limit_claimed=True)), 'common_limit_claimed'),
          fixture=dict(FIX, sequence='x_N = (-1)^N (1 + 1/N)', note='convergent subsequences, no whole-sequence limit'),
          reading='per-comparison bounds are recorded; no limit object is formed (BB2)')
    check('named_construction_not_uniqueness',
          claims_ok(CLAIMS, GATE)
          and rejected(lambda: claims_ok(dict(CLAIMS, uniqueness_of_ground_state_claimed=True), dict(GATE, uniqueness_of_ground_state_claimed=True)), 'uniqueness_claimed')
          and rejected(lambda: require_no_affirmative('The two families reach the thermodynamic limit.', ROUND_FORBIDDEN + V['forbidden'], template, 'fx'), 'thermodynamic_limit_phrase')
          and rejected(lambda: require_no_affirmative('This is the infinite-volume ground state.', ROUND_FORBIDDEN + V['forbidden'], template, 'fx'), 'infinite_volume_ground_state_phrase'))
    check('two_families_named',
          set(FAMILIES) == {'F1', 'F2'} and model_ok(MODEL)
          and rejected(lambda: model_ok(dict(MODEL, families=['F1'])), 'one_family_only')
          and rejected(lambda: model_ok(dict(MODEL, families=['F1', 'F2', 'literal vertex boxes'])), 'literal_vertex_boxes_added'),
          families=FAMILIES)
    check('changed_model_relabelled',
          model_ok(MODEL)
          and rejected(lambda: model_ok(dict(MODEL, tau_cap='1/100000000000000')), 'tau_changed')
          and rejected(lambda: model_ok(dict(MODEL, selected_triple=['1', '0', '0'])), 'nonzero_selected_triple')
          and rejected(lambda: model_ok(dict(MODEL, gauge_group='SU(3)')), 'su3_relabelled')
          and rejected(lambda: model_ok(dict(MODEL, dimension=2)), 'two_dimensional')
          and rejected(lambda: model_ok(dict(MODEL, model_id='finite_graph_fixture')), 'finite_graph_model_id')
          and rejected(lambda: model_ok(dict(MODEL, metric='coarse l1 on factor sites, star diameter 2')), 'l1_metric_relabelled')
          and rejected(lambda: model_ok(dict(MODEL, weights=dict(MODEL['weights'], creation_weight_w='w = 4/q'))), 'weights_retuned_after_constants'),
          model=MODEL)
    CLOCK = {'clock': V['clock'], 'coupling': 'the same tau for both boxes of every comparison', 'units': 'normalized delta=alpha/8, face coefficient -tau/3, c^(1) = -tau/72',
             'static': 'densities are static; theta=alpha t/hbar is named, no evolution is used'}

    def clock_ok(rec, first_order_den=72):
        require(rec['clock'].startswith('s=alpha*t_E/hbar (Euclidean), theta=alpha*t/hbar (real time)'), 'round clock')
        require(rec['coupling'] == 'the same tau for both boxes of every comparison', 'common coupling')
        require(first_order_den == P['c1_den'], 'first-order coefficient -tau/72 in normalized units')
        return True
    check('common_clock',
          clock_ok(CLOCK)
          and rejected(lambda: clock_ok(dict(CLOCK, coupling='box 1 at tau, box 2 at tau/2')), 'different_couplings_per_box'),
          record=CLOCK)
    check('wrong_delta_alpha_hbar_clock',
          clock_ok(CLOCK)
          and rejected(lambda: clock_ok(CLOCK, first_order_den=576), 'tau_over_576_units_mixed')
          and rejected(lambda: clock_ok(CLOCK, first_order_den=9), 'tau_over_9_units_mixed')
          and rejected(lambda: clock_ok(dict(CLOCK, clock='u=theta/8 labelled theta')), 'normalized_u_labelled_theta'))

    # ---------------- tiers and routes ---------------------------------------------------------------
    TIERS = {'C_headline': ('exact_first_order', 'polymer_kp', 'gate bound value K=49/111790368 (analytic_disc)', '(b)'),
             'c_site_headline': ('exact_first_order', 'polymer_kp', 'gate bound value K=49/111790368 (analytic_disc)', '(b)'),
             'C_secondary': ('exact_first_order', 'polymer_kp', 'analytic_disc re-instantiated at rho=1/151552 (labelled)', '(b)'),
             'c_site_secondary': ('exact_first_order', 'polymer_kp', 'analytic_disc re-instantiated at rho=1/151552 (labelled)', '(b)'),
             'C_crude': ('crude_majorant', 'polymer_kp', 'analytic_disc crude circle bound 2 t_i(rho) (crude_majorant)', '(b)')}

    def tier_ok(entry, components):
        tier, route, ba1_input, form = entry
        require(tier in ('exact_first_order', 'crude_majorant'), 'BB1 tier must be exact_first_order or crude_majorant')
        require(route == 'polymer_kp', 'forward BB1 route is polymer_kp (a BA1 route label is an input, never the BB1 route)')
        require(ba1_input and form in ('(a)', '(b)'), 'BA1 input and every-site form named')
        if tier == 'exact_first_order':
            require(all(c == 'exact_first_order' for c in components), 'exact constant with a crude component')
            require('crude' not in ba1_input, 'exact constant with a crude BA1 input')
        return True
    exact_components = ['exact_first_order'] * 3          # BA1 input K, anchored t, mixed taubar
    check('tier_mixing_rejected',
          all(tier_ok(e, exact_components if e[0] == 'exact_first_order' else ['crude_majorant'] * 3) for e in TIERS.values())
          and rejected(lambda: tier_ok(TIERS['C_headline'], ['exact_first_order', 'crude_majorant', 'exact_first_order']), 'crude_anchored_norm_in_exact_constant')
          and rejected(lambda: tier_ok(('exact_first_order', 'analytic_disc', TIERS['C_headline'][2], '(b)'), exact_components), 'ba1_route_used_as_bb1_route')
          and rejected(lambda: tier_ok(('polynomial_lieb_robinson', 'polymer_kp', TIERS['C_headline'][2], '(b)'), exact_components), 'lieb_robinson_tier')
          and rejected(lambda: tier_ok(('exact_first_order', 'polymer_kp', TIERS['C_crude'][2], '(b)'), exact_components), 'crude_ba1_input_in_exact_constant')
          and rejected(lambda: tier_ok(('exact_first_order', 'polymer_kp', '', '(b)'), exact_components), 'ba1_input_not_named'),
          tiers={k: list(v) for k, v in TIERS.items()})

    # ---------------- rate-constant pairs, weights, parameters ---------------------------------------
    def prefrozen_ok(q_reported, weights_declared_first, what, wmax):
        require(q_reported in (V['q_head'], 'secondary'), 'reported rate must be a frozen pair')
        require(weights_declared_first, 'proof weights must be declared before the constants')
        require(what <= wmax, 'proof weight outside the admissible range')
        return True
    check('rate_constant_pair_prefrozen',
          prefrozen_ok(hp['q'], True, hp['what'], hp['wmax']) and prefrozen_ok('secondary', True, sp['what'], sp['wmax'])
          and rejected(lambda: prefrozen_ok(Q(1, 128), True, hp['what'], hp['wmax']), 'rate_optimized_after_constants')
          and rejected(lambda: prefrozen_ok(hp['q'], False, hp['what'], hp['wmax']), 'weights_chosen_after_constants')
          and rejected(lambda: prefrozen_ok(hp['q'], True, 5 * sp['what'] / 3, sp['wmax']), 'secondary_weight_5_over_q_inadmissible'),
          declared_weights=DECLARED_WEIGHTS, admissible={'headline': [s(hp['what']), s(hp['wmax'])], 'secondary': [s(sp['what']), s(sp['wmax'])]})

    def params_ok(c):
        p = c['parameters']
        for key in ('metric', 'weights', 'window', 'rate_constant_pair', 'comparisons', 'cutoff', 'coefficient_input'):
            require(key in p and p[key], 'contract parameters lack ' + key)
        return True
    check('parameters_declare_metric_weights_window',
          params_ok(contract)
          and rejected(lambda: params_ok(dict(contract, parameters={k: v for k, v in contract['parameters'].items() if k != 'metric'})), 'metric_removed')
          and rejected(lambda: params_ok(dict(contract, parameters={k: v for k, v in contract['parameters'].items() if k != 'weights'})), 'weights_removed')
          and rejected(lambda: params_ok(dict(contract, parameters={k: v for k, v in contract['parameters'].items() if k != 'window'})), 'window_removed'),
          parameters=V['parameters_keys'])

    def rate_unit_ok(unit, rate_in_a):
        require(unit.startswith('per coarse l-infinity step in N at fixed spacing'), 'rate unit must be per coarse step in N at fixed spacing')
        require(rate_in_a is False, 'no rate in the lattice spacing')
        return True
    check('decay_rate_in_N_not_a',
          rate_unit_ok(RATE_UNIT, CLAIMS['rate_in_a_claimed'])
          and rejected(lambda: rate_unit_ok('per fm', False), 'rate_per_fm')
          and rejected(lambda: rate_unit_ok('per lattice spacing a', False), 'rate_per_lattice_spacing')
          and rejected(lambda: rate_unit_ok(RATE_UNIT, True), 'rate_in_a_claimed_true'),
          rate_unit=RATE_UNIT)
    check('uniform_in_N_not_in_a',
          require_uniformity_qualified('The constants are uniform in N at fixed spacing and in the cutoff.', template, 'fx')
          and rejected(lambda: require_uniformity_qualified('The bound is uniform.', template, 'fx'), 'unqualified_uniform_rate')
          and rejected(lambda: require_no_affirmative('The estimate holds uniform in a.', ROUND_FORBIDDEN + V['forbidden'], template, 'fx'), 'uniform_in_a_claim'))

    # ---------------- scaling tau -> tau/100 ------------------------------------------------------------
    h100 = pair_constants(P, V, tau_cap / 100, 'headline', 'exact_first_order')
    s100 = pair_constants(P, V, tau_cap / 100, 'secondary', 'exact_first_order')
    ratios = {'C_headline': hp['C'] / h100['C'], 'c_site': hp['c_site'] / h100['c_site'],
              'C_secondary': sp['C'] / s100['C'], 'c_site_secondary': sp['c_site'] / s100['c_site'], 'q_secondary': sp['q'] / s100['q']}

    def scaling_ok(r, brackets):
        require(brackets['C_headline'] == V['bracket_C'] and brackets['c_site'] == V['bracket_cs']
                and brackets['secondary'] == V['bracket_sec'] and brackets['q2'] == V['bracket_q2'], 'brackets must be the frozen ones')
        require(V['bracket_C'][0] <= r['C_headline'] <= V['bracket_C'][1], 'C headline ratio outside its bracket')
        require(V['bracket_cs'][0] <= r['c_site'] <= V['bracket_cs'][1], 'c_site ratio outside its bracket')
        require(V['bracket_sec'][0] <= r['C_secondary'] <= V['bracket_sec'][1] and V['bracket_sec'][0] <= r['c_site_secondary'] <= V['bracket_sec'][1],
                'secondary ratios outside their bracket')
        require(r['q_secondary'] == V['bracket_q2'], 'q secondary ratio must be exactly 100')
        return True
    BR = {'C_headline': V['bracket_C'], 'c_site': V['bracket_cs'], 'secondary': V['bracket_sec'], 'q2': V['bracket_q2']}
    sqrt_like = dict(ratios, C_headline=Q(10))
    check('tau_scaling_exponent',
          scaling_ok(ratios, BR)
          and rejected(lambda: scaling_ok(sqrt_like, BR), 'square_root_bound_labelled_linear')
          and rejected(lambda: scaling_ok(ratios, dict(BR, C_headline=(Q(1007, 10), Q(105)))), 'bracket_narrowed_after_evaluation')
          and rejected(lambda: scaling_ok(dict(ratios, C_secondary=ratios['C_secondary'] * 100), BR), 'secondary_constant_written_in_headline_q_form'),
          ratios={k: s(v) for k, v in ratios.items()}, previews={k: dec(v, 9) for k, v in ratios.items()},
          brackets={'C_headline': [s(x) for x in V['bracket_C']], 'c_site': [s(x) for x in V['bracket_cs']],
                    'secondary': [s(x) for x in V['bracket_sec']], 'q_secondary': s(V['bracket_q2'])})

    # ---------------- region constant scales with |Y| ---------------------------------------------------
    def region_claim_ok(pc, norms, N, const, with_Y_factor, rate):
        nY = len(norms)
        lhs = region_bound(pc, norms, N)
        rhs = const * (nY if with_Y_factor else 1) * (1 + rate) ** nY * pc['q'] ** (N - max(norms))
        require((1 + pc['t']) ** 2 <= 1 + rate, 'region exponential rate exceeds 1/10^8')
        require(lhs <= rhs, 'claimed region constant does not bound the proved region estimate')
        return True
    lam1 = [0] + [1] * 26
    hybrid = dict(hp, t=2 * hp['t'])        # anchored norm of a hybrid collection (supports split between two boxes)
    check('region_constant_scales_with_Y',
          region_claim_ok(hp, lam1, 3, hp['c_site'], True, V['region_rate'])
          and rejected(lambda: region_claim_ok(hp, lam1, 3, hp['C'], False, V['region_rate']), 'r_constant_reused_on_Y_without_Y_factor')
          and rejected(lambda: region_claim_ok(hybrid, lam1, 3, hp['c_site'], True, V['region_rate']), 'hybrid_collection_rate_4t_exceeds_frozen_rate')
          and rejected(lambda: require(region_bound(hp, [0, 1, 2], 3) <= hp['c_site'] * 3 * (1 + V['region_rate']) ** 3 * hp['q'] ** 2,
                                       'exponent d(R) used for a region reaching |y|=2'), 'exponent_of_R_reused_for_Y'),
          form='||rho^1_Y - rho^2_Y||_1 <= c_site |Y| e^{|Y|/10^8} q^{d_Y}, d_Y = N - max_y |y|_inf',
          proof='sum_y K q^{N-|y|} [2(1+t)^{|Y|-1} + (1+t)^{2|Y|} kappa_0 (S_{1/(qv)}-1)] with (1+t)^2 <= 1 + 1/10^8 <= e^{1/10^8}')

    # ---------------- root-N misuse, arithmetic, verdict ------------------------------------------------
    led = hp['ledger']

    def combine_ok(total):
        require(total == led['L1'] + led['L2'] + led['L3'] + led['L4'] + led['L5'], 'deterministic terms add linearly')
        return True
    check('root_n_misuse',
          combine_ok(hp['C'])
          and rejected(lambda: combine_ok(led['L1'] + (led['L2'] ** 2 + led['L3'] ** 2 + led['L4'] ** 2 + led['L5'] ** 2) / (led['L2'] + led['L3'] + led['L4'] + led['L5'])), 'root_sum_of_squares_style_combination')
          and rejected(lambda: combine_ok(hp['C'] / 2), 'divided_by_sqrt_4_sites')
          and rejected(lambda: require(region_bound(hp, lam1, 3) / 27 * 5 >= region_bound(hp, lam1, 3), 'region divided by sqrt|Y|'), 'region_divided_by_sqrt_Y'))
    check('exact_arithmetic_admission',
          rat('49/111790368') == P['ba1_K']
          and rejected(lambda: rat(4.3832e-7), 'float_constant')
          and rejected(lambda: rat(True), 'bool_constant')
          and rejected(lambda: rat('nan'), 'nan_string')
          and rejected(lambda: rat('1/0'), 'zero_denominator'))

    def verdict_for(C, cs, rate_ok, untruncated, every_comparison):
        if C is None:
            return 'insufficient'          # no control of the outside-state dependence
        if C <= V['C_target'] and cs <= V['cs_target'] and rate_ok and untruncated and every_comparison:
            return 'accepted_within_scope'
        return 'limited'                   # a proved bound whose dominating term misses a frozen target
    verdict = verdict_for(hp['C'], hp['c_site'], hp['region_rate_ok'], True, True)
    require(verdict == 'accepted_within_scope', 'forward verdict follows from the constants')

    def retained(C, cs, rate_ok, claimed):
        require(verdict_for(C, cs, rate_ok, True, True) == claimed, 'verdict does not follow from the constants')
        return True
    check('insufficient_verdict_retained',
          retained(hp['C'], hp['c_site'], True, 'accepted_within_scope') and retained(hc['C'], hc['c_site'], False, 'limited')
          and rejected(lambda: retained(hc['C'], hc['c_site'], False, 'accepted_within_scope'), 'crude_tier_relabelled_accepted')
          and rejected(lambda: model_ok(dict(MODEL, tau_cap='1/10000000000')), 'tau_retuned_for_crude_tier'),
          crude_outcome='crude_majorant tier fails 1/250000 and has no c_site in the frozen form; retained as a reported value')

    # ---------------- reverse premise isolation (inventory rule), own inventory -------------------------
    expected = sorted(['AGENTS.md', CONTRACT_REL] + V['shared'])
    inv = sorted(p.relative_to(BASE / 'inputs').as_posix() for p in (BASE / 'inputs').rglob('*') if p.is_file())
    require(inv == expected, 'forward inputs inventory equals AGENTS.md + contract + shared premises')
    for rel in inv:
        require(input_bytes(rel) == input_bytes(rel), 'snapshot readable')

    def reverse_inventory_ok(invlist):
        require(sorted(invlist) == expected, 'reverse inventory must equal AGENTS.md, the contract and shared_premises exactly')
        bad = [x for x in invlist if ('/skeptic/' in x and x not in ('research/round33/skeptic/ba1.md', 'research/round33/skeptic/ba2.md', 'research/round29/skeptic/am2.md'))
               or '/forward/bb1/' in x or '/bb2/' in x or 'deliberation' in x or '/experts/' in x]
        require(not bad, 'forbidden file in the reverse inventory')
        return True
    check('reverse_premise_isolation',
          reverse_inventory_ok(expected)
          and rejected(lambda: reverse_inventory_ok(expected + ['research/round33/skeptic/bb1-triage.md']), 'skeptic_triage_added')
          and rejected(lambda: reverse_inventory_ok(expected + ['research/round33/forward/bb1/report.md']), 'forward_bb1_file_added')
          and rejected(lambda: reverse_inventory_ok(expected + ['research/round33/forward/bb2/report.md']), 'bb2_producer_file_added')
          and rejected(lambda: reverse_inventory_ok(expected + ['research/round33/advisor/deliberation-bb.md']), 'deliberation_added'),
          inventory_files=len(inv), note='the rule is checked on the declared inventory; the reverse directory was never opened by this producer')

    # ---------------- error ledger (preregistered terms) -------------------------------------------------
    def ledger_for(pc):
        lg = pc['ledger']
        return {'L1': lg['L1'], 'L2': lg['L2'], 'L3': lg['L3'], 'L4': lg['L4'], 'L5': lg['L5']}
    lh, ls = ledger_for(hp), ledger_for(sp)
    ledger = {
        'coefficient_input_every_site': {'status': 'charged', 'headline': s(lh['L1']), 'headline_preview': dec(lh['L1']),
                                         'secondary': s(ls['L1']),
                                         'note': 'form (b) at the sites of Y: sum_{I meets R} ||delta_I|| <= D(0) + D(e_z) <= K(1+q) q^(N-1), times 2; '
                                                 'the far-site input D(x) <= K q^((N-|x|)_+) enters the three following items through S_{1/(qv)} - 1 = 146'},
        'straddling_supports': {'status': 'charged', 'headline': s(lh['L3']), 'headline_preview': dec(lh['L3']), 'secondary': s(ls['L3']),
                                'note': 'Y-cluster derivative (straddling families through a support missing Y): 2 taubar v^{-d} per site'},
        'normalization': {'status': 'charged', 'headline': s(lh['L2'] + lh['L4']), 'headline_preview': dec(lh['L2'] + lh['L4']),
                          'secondary': s(ls['L2'] + ls['L4']),
                          'parts': {'eta_leading_(1+t)^{|Y|-1}-1': s(lh['L2']), 'vacuum_probability_derivative': s(lh['L4'])},
                          'note': 'the other creations meeting Y (eta = t) and the derivative of the vacuum probabilities pi(supp eta) (polymers touching Y or a Y-cluster)'},
        'polymer_or_split_remainder': {'status': 'charged', 'headline': s(lh['L5']), 'headline_preview': dec(lh['L5']), 'secondary': s(ls['L5']),
                                       'note': 'Kotecky-Preiss clusters in the truncated vacuum probabilities: a (1 + 2 taubar^2 S_{v/w}) terms'},
        'cutoff_removal_at_fixed_N': {'status': 'not_applicable',
                                      'reason': 'not a numeric cost: at fixed N the terms ||rho_{L,Y} - rho_Y||_1 tend to 0 as L grows (AV1 F22 with the untruncated gap 1/2; AY1 for F2) and the closed bound passes; no constant depends on L'},
        'arithmetic': {'status': 'not_applicable',
                       'reason': "not a numeric cost: exact Fractions; directed enclosures only (e^{1/8} at most 8/7, so G(R) at most 148/7 and G'(R) at most 352; ln(1001/1000) at least 1/1001; e^x at least 1+x)"},
    }
    require(sorted(ledger) == sorted(V['error_terms']), 'ledger names equal error_terms_itemized')
    require(all(e['status'] == 'charged' or e.get('reason') for e in ledger.values()), 'not_applicable only with a reason')
    require(lh['L1'] + lh['L2'] + lh['L3'] + lh['L4'] + lh['L5'] == hp['C'], 'ledger adds to the headline C')
    check('error_ledger_itemized', True, items=sorted(ledger), headline_total=s(hp['C']))

    # ---------------- report binding, sentence, phrase scans -------------------------------------------
    report = (BASE / 'report.md').read_text(encoding='utf-8')
    require(report.count(template) == 1, 'mandatory sentence template quoted exactly once as one unbroken span')
    require_no_affirmative(report, ROUND_FORBIDDEN + V['forbidden'], template, 'report.md')
    require_no_placeholder(report, template, 'report.md')
    require_uniformity_qualified(report, template, 'report.md')
    for et in V['error_terms']:
        contains(report, '`' + et + '`', 'error ledger item in report')
    for cid in V['controls']:
        contains(report, '`' + cid + '`', 'control id in the report map')
    bound_values = {'C_headline': hp['C'], 'c_site_headline': hp['c_site'], 'C_secondary': sp['C'], 'c_site_secondary': sp['c_site'],
                    'C_crude': hc['C'], 'K_headline_gate': P['ba1_K'], 'K_secondary': sp['K'], 'K_crude': hc['K'], 't_exact': hp['t'],
                    'taubar_headline': hp['taub'], 'taubar_secondary': sp['taub'], 'taubar_crude': hc['taub'],
                    'a_headline': hp['a'], 'a_secondary': sp['a'], 'kappa0_headline': hp['kappa0'], 'kappa0_secondary': sp['kappa0'],
                    'loss_headline': hp['what'], 'loss_secondary': sp['what'], 'Gamma_headline': hp['gamma'], 'Gamma_secondary': sp['gamma'],
                    'L1': lh['L1'], 'no_decay': no_decay, 'omega_lipschitz_R': omega_lip_R}
    previews_required = {'L2': lh['L2'], 'L3': lh['L3'], 'L4': lh['L4'], 'L5': lh['L5'], 'kappa0_R_contract': hp['kappa0_contract_R'],
                         'c_site_crude_formula': hc['c_site'], 'C_secondary_crude': sc['C']}
    for name, val in previews_required.items():
        contains(report, dec(val), 'labelled decimal preview ' + name)
    for name, val in bound_values.items():
        contains(report, s(val), 'exact rational ' + name)
    for name, val in ratios.items():
        contains(report, dec(val, 9), 'scaling ratio preview ' + name)
    check('negation_aware_phrase_scan',
          rejected(lambda: require_no_affirmative('The construction gives the thermodynamic limit.', ROUND_FORBIDDEN + V['forbidden'], template, 'fx'), 'affirmative_thermodynamic_limit')
          and require_no_affirmative('This is not the thermodynamic limit.', ROUND_FORBIDDEN + V['forbidden'], template, 'fx')
          and rejected(lambda: require_no_affirmative('The bound confirms boundary independent behaviour.', ROUND_FORBIDDEN + V['forbidden'], template, 'fx'), 'affirmative_boundary_independent'),
          scanned=['report.md', 'results.json strings'], template_removed_as_one_literal=True)
    check('placeholder_span_rejected',
          rejected(lambda: require_no_placeholder('C = <value to fill>', template, 'fx'), 'angle_span_with_whitespace')
          and rejected(lambda: require_no_placeholder('<a|b>', template, 'fx'), 'angle_span_with_bar')
          and rejected(lambda: require_no_placeholder('<e.g.x>', template, 'fx'), 'angle_span_with_eg'))
    check('mandatory_sentence_and_gate_fields', True, mandatory_sentence=template, occurrences_in_report=1, gate_fields=GATE,
          constants_for_the_template={'C': s(hp['C']), 'q': s(hp['q']), 'R': '{0,e_z}', 'N': 'smaller box size, at least 2'})
    check('report_bound_to_results', True, exact_values_in_report=sorted(bound_values))

    # ---------------- packet assembly and coherent tampering ---------------------------------------------
    headline = {
        'R_form': {'q': s(hp['q']), 'C': s(hp['C']), 'C_preview': dec(hp['C']), 'C_target': s(V['C_target']), 'target_met': hp['C'] <= V['C_target'],
                   'margin': dec(V['C_target'] / hp['C'], 6), 'tier': 'exact_first_order', 'route': 'polymer_kp',
                   'ba1_input': 'gate bound value K=49/111790368 (analytic_disc), every-site form (b) proved here',
                   'per_sign': {sg: {'C': s(head[sg]['C']), 'C_preview': dec(head[sg]['C'])} for sg in taus}},
        'region_form': {'q': s(hp['q']), 'c_site': s(hp['c_site']), 'c_site_preview': dec(hp['c_site']), 'c_site_target': s(V['cs_target']),
                        'target_met': hp['c_site'] <= V['cs_target'], 'margin': dec(V['cs_target'] / hp['c_site'], 6),
                        'form': 'c_site |Y| e^{|Y|/10^8} q^{d_Y}', 'tier': 'exact_first_order', 'route': 'polymer_kp',
                        'per_sign': {sg: {'c_site': s(head[sg]['c_site'])} for sg in taus}},
        'secondary_pair': {'q': '151552|tau|', 'q_at_cap': s(sp['q']), 'C': s(sp['C']), 'C_preview': dec(sp['C']), 'C_target': s(V['C2_target']),
                           'c_site': s(sp['c_site']), 'c_site_preview': dec(sp['c_site']), 'c_site_target': s(V['cs2_target']),
                           'targets_met': sec_met, 'tier': 'exact_first_order', 'route': 'polymer_kp', 'status': 'labelled',
                           'ba1_input': 'analytic_disc re-instantiated at rho=1/151552, K=' + s(sp['K']),
                           'per_sign': {sg: {'C': s(sec[sg]['C']), 'c_site': s(sec[sg]['c_site'])} for sg in taus}},
        'crude_tier': {'q': s(hc['q']), 'C': s(hc['C']), 'C_preview': dec(hc['C']), 'tier': 'crude_majorant', 'route': 'polymer_kp',
                       'meets_C_target': hc['C'] <= V['C_target'], 'region_form_available': hc['region_rate_ok'],
                       'secondary_crude_C': s(sc['C']), 'status': 'reported separately, never a target'},
        'comparisons': comparisons,
        'scaling': {k: s(v) for k, v in ratios.items()},
        'kp': kp_rec, 'lemma': lemma['values'],
    }
    label = 'static_not_dynamic'
    verdict_line = (verdict + ' (forward half; the contract acceptance also requires the reverse iterated_split route and skeptical review); '
                    'sub-label static_not_dynamic')
    packet = {
        'loop': 'BB1', 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'ai_assistance': 'AI-assisted forward production (Claude model agent); correlated model-agent work, not independent human review',
        'contribution_alias': 'HNM-BB1-F forward polymer_kp marginal locality of the reduced densities of F1 and F2 from every-site coefficient decay',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'label': label, 'model': MODEL, 'model_statement': V['model'], 'families': FAMILIES, 'topology': TOPOLOGY, 'rate_unit': RATE_UNIT,
        'metric': 'coarse l_inf on factor sites, star diameter 1', 'weights': DECLARED_WEIGHTS,
        'tau_values': {sg: s(t) for sg, t in taus.items()},
        'headline': headline, 'error_terms_itemized': ledger, 'gate_fields': GATE,
        'mandatory_sentence': template,
        'statement': ('For every comparison of the named families (including F1 versus F2 at fixed N and two one-prescription volumes compared directly), '
                      'both signs and every on-site cutoff space, and at fixed N for the untruncated ground vectors: ||rho^1_R - rho^2_R||_1 <= C q^(N-1) with q=1/64, '
                      'C=' + s(hp['C']) + ' (exact_first_order, polymer_kp); ||rho^1_Y - rho^2_Y||_1 <= c_site |Y| e^{|Y|/10^8} q^{d_Y} with c_site=' + s(hp['c_site']) +
                      '; labelled secondary pair at q=151552|tau|: C=' + s(sp['C']) + ', c_site=' + s(sp['c_site']) + '.'),
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions'],
                       'additional': ['no limit object, whole-sequence convergence or common limit (BB2)', 'no dynamics',
                                      'no analyticity of the reduced density (no zero-free region proved)', 'no estimate in the lattice spacing a']},
        'routes_executed': ['forward polymer_kp: hard-core polymer representation of the norm and of the Y-marginal (Y-clusters, vacuum probabilities)',
                            'forward polymer_kp: mixed-weight contraction lemma (w^{diam I} e^{b|I|}, loss w e^{4b}) proved in full',
                            'forward polymer_kp: Kotecky-Preiss condition with a = taubar^2, exploration-tree majorant, truncated vacuum probabilities',
                            'forward polymer_kp: real-parameter derivative along c + lambda (c\' - c), marginal-locality lemma in the contract form',
                            'every-site coefficient input form (b): BA1 reverse disc theorem restated for every site u and proved in full'],
        'routes_not_executed': ['reverse iterated_split route (outside this producer)', 'skeptic review'],
        'contract_wording_defects': [
            'D1: normalization_couples_supports says a one-site straddling first-order face has zero R-marginal while a support strictly containing R does not; at first order a support strictly containing R also has zero R-marginal (AY1 gate: all 72 straddling faces among the 82 meeting R vanish, 6 of them strictly contain R); the nonzero first-order R-marginal belongs to supports equal to R, and a support strictly containing R differs at second order (fully excited R block); the fixture records all three kinds'],
        'contract_readings': [
            'R1: coefficient_input form (b) is stated for u in Lambda_N with exponent N-|u|_inf; the polymer route also needs the sites of the union volume outside Lambda_N, where the same theorem gives the bound K (exponent (N-|u|_inf)_+ = 0)',
            'R2: required item 1 names omega_O the outside marginal on the straddle region; the decomposition is exact for the region O = union of I minus Y over supports I meeting Y (or any larger outside region), and N_c depends on omega only through its marginal on O',
            'R3: the marginal-locality lemma form kappa(I) <= kappa_0 (w\')^(-d_inf(I,Y)) p(|I|) is implied by the sharper site form kappa(I) <= (1+t)^{2|Y|} kappa_0 sum_{x in I} sum_{y in Y} v^{-d(x,y)} with p(s)=s, w\'=v and kappa_0(Y) = (1+t)^{2|Y|} |Y| kappa_0; the constants use the site form',
            'R4: the AY1 item-by-item verification (H1-H5, including cutoff-vector removal) is stated for F2 on Lambda_N; no step uses the cube shape, so it applies verbatim to the one-prescription volumes, as the BA1 accepted statement already uses'],
        'proposed_forward_verdict': verdict_line,
    }
    packet.update(CLAIMS)
    for k, val in GATE.items():
        if isinstance(val, bool):
            packet[k] = val
    forward_inventory = expected

    def packet_hash(pk):
        body = {k1: v1 for k1, v1 in pk.items() if k1 != 'packet_sha256'}
        return sha_bytes(json.dumps(body, sort_keys=True).encode('utf-8'))

    def validate_packet(pk, inventory):
        require(pk.get('packet_sha256') == packet_hash(pk), 'packet hash mismatch')
        ids = {ch['id']: ch for ch in pk['checks']}
        for cid in V['controls']:
            if cid == 'coherent_evidence_tampering':
                continue
            require(cid in ids and ids[cid]['passed'] is True and ids[cid].get('rejected_mutations'), 'required control missing or failed: ' + cid)
        claims_ok({k1: pk[k1] for k1 in CLAIMS}, pk['gate_fields'])
        require(sorted(inventory) == forward_inventory, 'premise snapshot inventory incomplete')
        require(rat(pk['headline']['R_form']['C']) == pair_constants(P, V, tau_cap, 'headline', 'exact_first_order')['C'], 'headline C differs from recomputation')
        require(pk['headline']['R_form']['target_met'] is (rat(pk['headline']['R_form']['C']) <= V['C_target']), 'target Boolean')
        require(pk['families'] == FAMILIES and pk['model'] == MODEL, 'families or model changed')
        require(pk['mandatory_sentence'] == template, 'mandatory sentence changed')
        require(pk['proposed_forward_verdict'].startswith(verdict_for(rat(pk['headline']['R_form']['C']), rat(pk['headline']['region_form']['c_site']), True, True, True)),
                'verdict changed')
        for text in all_strings(pk):
            require_no_affirmative(text, ROUND_FORBIDDEN + V['forbidden'], template, 'packet')
            require_no_placeholder(text, template, 'packet')
        return True

    base_packet = dict(packet)
    base_packet['checks'] = [dict(ch) for ch in CHECKS]
    base_packet['packet_sha256'] = packet_hash(base_packet)
    inventory = {rel: True for rel in inv}

    def tamper(fn):
        def run():
            pk = json.loads(json.dumps(base_packet))
            invc = dict(inventory)
            fn(pk, invc)
            pk['packet_sha256'] = packet_hash(pk)
            return validate_packet(pk, invc)
        return run

    def t_control(pk, invc):
        for ch in pk['checks']:
            if ch['id'] == 'fixture_polymer_identity':
                ch['passed'] = False

    def t_snapshot(pk, invc):
        invc.pop(P_BA1_GATE)

    def t_C(pk, invc):
        pk['headline']['R_form']['C'] = s(rat(pk['headline']['R_form']['C']) / 2)

    def t_whole(pk, invc):
        pk['whole_sequence_claimed'] = True
        pk['gate_fields']['whole_sequence_claimed'] = True

    def t_family(pk, invc):
        pk['families'] = {'F1': FAMILIES['F1']}

    def t_sentence(pk, invc):
        pk['mandatory_sentence'] = template.replace('not uniqueness of any ground state, ', '')

    def t_phrase(pk, invc):
        pk['statement'] = pk['statement'] + ' This gives the thermodynamic limit.'
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_snapshot), 'ba1_gate_snapshot_removed_hash_rebound')
          and rejected(tamper(t_C), 'headline_C_halved_hash_rebound')
          and rejected(tamper(t_whole), 'whole_sequence_flag_hash_rebound')
          and rejected(tamper(t_family), 'one_family_hash_rebound')
          and rejected(tamper(t_sentence), 'mandatory_sentence_trimmed_hash_rebound')
          and rejected(tamper(t_phrase), 'forbidden_phrase_added_hash_rebound'))

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
    for text in all_strings(packet):
        require_no_affirmative(text, ROUND_FORBIDDEN + V['forbidden'], template, 'results')
        require_no_placeholder(text, template, 'results')
    return packet


def main():
    ap = argparse.ArgumentParser(description='BB1 forward exact checker (route polymer_kp)')
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
        if p.is_file() and (rel.parts[0] == 'inputs' or p.name in ('check.py', 'report.md')) and rel.parts[0] != 'output':
            sources[rel.as_posix()] = sha(p)
    manifest = {'loop': 'BB1', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'BB1', 'direction': 'forward', 'checks': len(result['checks']),
                      'C_headline_preview': result['headline']['R_form']['C_preview'],
                      'c_site_preview': result['headline']['region_form']['c_site_preview'],
                      'controls_with_damaging_mutations': result['controls_with_damaging_mutations'],
                      'rejected_mutation_total': result['rejected_mutation_total']}, sort_keys=True))


if __name__ == '__main__':
    main()
