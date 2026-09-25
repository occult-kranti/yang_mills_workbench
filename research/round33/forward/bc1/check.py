#!/usr/bin/env python3
"""BC1 forward producer (single producer of a statement+skeptic loop): exact checks for the
restatement of the AV2 node certificate and of the AW2 enclosure for the limit of the named
constructions omega_inf, the F2 finite-box sign corollary with N_sign, the finite-box node record,
the common GNS item and the updated obligations table.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production (a Claude model agent).

Standard library only (argparse, fractions, hashlib, json, pathlib, re).  Every admission Boolean is
decided in exact Fraction arithmetic; decimal strings are truncated or directed previews and are
never admission values.  Conditions raise AdmissionError explicitly (never `assert`), so every
check stays active under `python -O`.  Every constant is read from the sha256-pinned gate snapshots
in inputs/ and compared with the gate rationals; none is typed in.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round33/contracts/bc1.json'
CONTRACT_SHA256 = '3fb84ed3135c48670d26643f120ef2ef74f5888174cf11e7395919e408a279bd'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'
OWN_DIR = 'research/round33/forward/bc1/'

# Admitted gates: snapshot path and pinned sha256 (every one also cross-checked below).
GATES = {
    'AQ1': ('research/round29/advisor/aq1-gate.json', 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e'),
    'AQ2': ('research/round29/advisor/aq2-gate.json', '930b697db343ffd261c303c34e6ddd8c6e9c753ee6707931c55dc4171ee47575'),
    'AV1': ('research/round32/advisor/av1-gate.json', '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0'),
    'AV2': ('research/round32/advisor/av2-gate.json', '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33'),
    'AW1': ('research/round32/advisor/aw1-gate.json', '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae'),
    'AW2': ('research/round32/advisor/aw2-gate.json', '640a3b0a74c7fcd66318ba7ce2a60942f837ad154f157bc1d69323589b24be62'),
    'AY1': ('research/round32/advisor/ay1-gate.json', 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5'),
    'AY2': ('research/round32/advisor/ay2-gate.json', 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6'),
    'BA1': ('research/round33/advisor/ba1-gate.json', '15546f9ec0ab130cdf216ab63b17e6e0ebd7a28c1aefc7ce232f93b77730ebcc'),
    'BA2': ('research/round33/advisor/ba2-gate.json', 'e6b163fc8f80de28c51609f77d0bef21dcdc1286638c862ad67202e6f7b0ca35'),
    'BB1': ('research/round33/advisor/bb1-gate.json', '18141fea672e5bae09024a5fddc56ea7102aae56ecca16fbb30d67a1354a3827'),
    'BB2': ('research/round33/advisor/bb2-gate.json', 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca'),
}
ROUND32_GATES = ('AV1', 'AV2', 'AW1', 'AW2', 'AY1', 'AY2')
P_AV2F = 'research/round32/forward/av2/report.md'
P_AV2R = 'research/round32/reverse/av2/report.md'
P_AV2S = 'research/round32/skeptic/av2.md'
P_AW2F = 'research/round32/forward/aw2/report.md'
P_AY2F = 'research/round32/forward/ay2/report.md'
P_BB2F = 'research/round33/forward/bb2/report.md'
P_BB2R = 'research/round33/reverse/bb2/report.md'
P_BB2S = 'research/round33/skeptic/bb2.md'
P_SEL = 'research/round33/advisor/selection-bc1.md'


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


def _digits(q, digits, up):
    q = Q(q)
    if q == 0:
        return '0'
    neg = q < 0
    a = abs(q)
    e = 0
    while a >= Q(10) ** (e + 1):
        e += 1
    while a < Q(10) ** e:
        e -= 1
    scaled = a / Q(10) ** (e - digits + 1)
    m = scaled.numerator // scaled.denominator
    away = (up and not neg) or (not up and neg)
    if away and Q(m) != scaled:
        m += 1
    txt = str(m)
    if len(txt) > digits:        # carry to the next power of ten
        e += 1
        txt = txt[:digits]
    return ('-' if neg else '') + txt[0] + '.' + txt[1:] + 'e' + str(e)


def dec(q, digits=12):
    """Truncated scientific decimal preview (toward zero); never an admission value."""
    q = Q(q)
    if q < 0:
        return '-' + _digits(-q, digits, False)
    return _digits(q, digits, False)


def dec_down(q, digits=12):
    return _digits(q, digits, False)


def dec_up(q, digits=12):
    return _digits(q, digits, True)


def preview_value(text):
    """Parse a decimal preview string into an exact Fraction (comparison only, never admission)."""
    require(re.fullmatch(r'-?\d+(\.\d+)?(e-?\d+)?', text) is not None, 'malformed preview ' + text)
    mant, _, ex = text.partition('e')
    return Q(mant) * Q(10) ** int(ex or '0')


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def read_input(rel):
    return (BASE / 'inputs' / rel).read_text(encoding='utf-8')


def norm(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def match(pattern, text, label, flags=0):
    m = re.search(pattern, text, flags)
    require(m is not None, 'premise text not parsed: ' + label)
    return m


def frac_of(m, i):
    return Q(int(m.group(i)), int(m.group(i + 1)))


def split_top_level(text, sep=';'):
    parts, depth, cur = [], 0, ''
    for ch in text:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == sep and depth == 0:
            parts.append(cur.strip())
            cur = ''
        else:
            cur += ch
    parts.append(cur.strip())
    return parts


# ---------------------------------------------------------------------------
# Negation-aware phrase scan: infrastructure copied from research/round33/tools/phrase_scan.py
# (rule R6 of the Round32 closing panel).  It computes no scientific result.
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


def clauses(text):
    return [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', text) if c.strip()]


def phrase_hits(text, forbidden, template=None):
    body = norm(text)
    if template:
        body = body.replace(norm(template), ' ')
    hits = []
    for clause in clauses(body):
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                hits.append({'phrase': phrase, 'clause': clause[:200], 'negated': bool(NEGATION.search(clause))})
    return hits


def affirmative(hits):
    return [h for h in hits if not h['negated']]


# ---------------------------------------------------------------------------
# Directed enclosures of pi (Machin) and of e^{-3} (Taylor series of e^3 with a geometric tail).
# ---------------------------------------------------------------------------
def atan_inv_bracket(x, terms):
    total, partial = Q(0), []
    for k in range(terms + 1):
        total += Q((-1) ** k, (2 * k + 1) * x ** (2 * k + 1))
        partial.append(total)
    return min(partial[-1], partial[-2]), max(partial[-1], partial[-2])


def pi_bracket():
    a5 = atan_inv_bracket(5, 60)
    a239 = atan_inv_bracket(239, 20)
    lo, hi = 16 * a5[0] - 4 * a239[1], 16 * a5[1] - 4 * a239[0]
    require(lo < hi and hi - lo < Q(1, 10 ** 60), 'pi bracket width')
    return lo, hi


def exp_minus3_bracket(terms=80):
    total, term = Q(0), Q(1)
    for k in range(terms):
        total += term
        term = term * 3 / (k + 1)
    tail = term / (1 - Q(3, terms + 1))           # geometric majorant of the remaining terms
    lo, hi = 1 / (total + tail), 1 / total
    require(lo < hi and hi - lo < Q(1, 10 ** 80), 'e^{-3} bracket width')
    return lo, hi


# ---------------------------------------------------------------------------
# Contract: every target, reference, node, parameter, control id and obligation name is read here.
# ---------------------------------------------------------------------------
def load_contract():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen BC1 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'BC1' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


def contract_values(c):
    pre = c['preregistration']
    par = c['parameters']
    v = {'contract': c}
    v['tau'] = rat(pre['tau']['value'])
    require(v['tau'] == Q(1, 10 ** 8), 'preregistered tau')
    v['signs'] = list(pre['tau']['signs_evaluated'])
    require(v['signs'] == ['+', '-'], 'both signs required')
    require(pre['tau']['is_model_change_vs_previous_loop'] is False and pre['tau']['rule_if_chosen_later'] is None, 'tau rule')
    v['triple'] = [rat(x) for x in pre['selected_triple_alpha_units']]
    require(v['triple'] == [0, 0, 0], 'zero selected triple')
    v['model_id'] = pre['model_id']
    require(v['model_id'] == 'AQ_patterned_zero_selected', 'model id')
    v['model'] = c['model']
    require('R={0,e_z}' in v['model'] and 'omega_inf' in v['model'] and 'F2 = I1 section 6' in v['model'], 'model string')
    v['nodes'] = [rat(x) for x in pre['nodes']['s_values']]
    require(v['nodes'] == [1] and pre['nodes']['post_hoc_node_selection'] == 'forbidden', 'single preregistered node s=1')
    v['N_min'] = int(par['N_min'])
    require(v['N_min'] == 2, 'N_min')
    m = match(r'with q=(\d+)/(\d+) and C\' the nested_telescoping bound value of the BB2 gate decision', par['finite_box_sign'], 'contract q and C source')
    v['q'] = frac_of(m, 1)
    require(v['q'] == Q(1, 64), 'contract q')
    require('the labelled union_comparison value and the labelled re-evaluated values are not used' in par['finite_box_sign'], 'labelled values excluded')
    v['finite_box_sign'] = par['finite_box_sign']
    obs = pre['observable']
    v['reference'] = obs['reference_value_exact']
    require(v['reference'].startswith('e^{-3}/4 for C(1)') and '0 for the static mean (Haar)' in v['reference'], 'references read from the contract')
    v['reference_route'] = obs['reference_route']
    tg = pre['target']
    v['target'] = tg
    require(tg['comparator'] == '==' and 'feasibility/format check' in tg['note'] and 'N_sign computed exactly' in tg['value'], 'target block')
    v['clock'] = pre['clock']
    require(v['clock'].startswith('s=alpha*t_E/hbar (Euclidean), theta=alpha*t/hbar (real time); normalized u=theta/8 only internally'), 'clock')
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']) and len(v['controls']) == 25, 'controls mirror')
    v['error_terms'] = list(pre['error_terms_itemized'])
    require(len(v['error_terms']) == 5, 'five error terms')
    v['error_terms_rule'] = pre['error_terms_rule']
    v['gate_fields'] = dict(pre['gate_fields_required'])
    v['template'] = pre['mandatory_sentence_template']
    v['forbidden'] = list(pre['forbidden_phrasings'])
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['tiers'] = list(pre['tier_names_allowed'])
    v['required'] = list(c['required'])
    require(len(v['required']) == 7, 'seven required items')
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['shared'] = list(c['shared_premises'])
    v['params'] = dict(par)
    v['new_semantics'] = dict(c['new_control_semantics'])
    v['hash_binding'] = dict(pre['hash_binding'])
    require(all(v['hash_binding'][k] is True for k in v['hash_binding']), 'hash binding flags')
    require(c['direction'] == 'statement+skeptic' and c['producers'] == ['forward'], 'direction')
    ob = par['obligations']
    k1 = ob.index('(at least: ')
    body = ob[k1 + len('(at least: '):]
    require(body.endswith(')'), 'obligations list closes')
    v['new_rows'] = split_top_level(body[:-1])
    require(len(v['new_rows']) == 10, 'ten new obligation entries in the contract')
    v['selection_reason'] = c['selection_reason']
    v['selected_after'] = c['selected_after']
    return v


def strings_of(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, val in obj.items():
            yield k
            yield from strings_of(val)
    elif isinstance(obj, (list, tuple)):
        for val in obj:
            yield from strings_of(val)


R1_SPAN = re.compile(r'<[^<>]*>')
REPORT_PLACEHOLDER = re.compile(r'<[A-Za-z][^<>\n]*>')


def placeholder_spans(strings):
    out = []
    for st in strings:
        for m in R1_SPAN.finditer(st):
            if re.search(r'\s|\||e\.g\.', m.group(0)):
                out.append(m.group(0)[:80])
    return out


def report_placeholders(text):
    return [m.group(0)[:80] for m in REPORT_PLACEHOLDER.finditer(text) if re.search(r'\s|\||e\.g\.', m.group(0))]


def forward_verdict(identification_admitted, constants_equal, corollary_done, gns_item_done, table_complete, overclaim):
    if overclaim or not identification_admitted or not constants_equal:
        return 'insufficient'
    if not (corollary_done and gns_item_done and table_complete):
        return 'limited'
    return 'accepted_within_scope'


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cconj(a):
    return (a[0], -a[1])


def cadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


# ---------------------------------------------------------------------------
def compute(check_sha):
    c, contract_digest = load_contract()          # sha256 verified before any evaluation
    V = contract_values(c)
    tau = V['tau']
    q = V['q']
    check('contract_snapshot_sha256',
          contract_digest == CONTRACT_SHA256 and len(V['controls']) == 25 and V['nodes'] == [1],
          contract_sha256=contract_digest, contract_path=CONTRACT_REL, check_py_sha256_recorded_before_evaluation=check_sha,
          tau_read_from_contract=s(tau), signs=V['signs'], node_read_from_contract=[s(x) for x in V['nodes']],
          N_min_read_from_contract=V['N_min'], q_read_from_contract=s(q),
          target_read_from_contract={'quantity': V['target']['quantity'], 'value': V['target']['value'], 'comparator': V['target']['comparator']},
          reference_read_from_contract=V['reference'], reference_route=V['reference_route'], hash_binding=V['hash_binding'])

    # ======================= premise inventory, gate hashes, cross-bindings =======================
    expected_inputs = ['AGENTS.md', CONTRACT_REL] + V['shared']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    check('premise_inventory_bound',
          sorted(inventory) == sorted(set(expected_inputs)) and len(inventory) == 40
          and not any('__pycache__' in k or k.endswith('.pyc') for k in inventory)
          and not any('/bc2' in k or 'bc2-gate' in k for k in inventory),
          inventory_files=len(inventory), inputs_sha256=inventory,
          isolation='inputs equal AGENTS.md + the BC1 contract + its 38 shared premises; no BC2, current skeptic, expert or advisor-working file')

    G = {}
    for name, (rel, pin) in GATES.items():
        require(inventory.get(rel) == pin, 'gate snapshot hash differs from the pinned value: ' + name)
        G[name] = json.loads(read_input(rel))
        require(G[name]['loop'] == name and G[name]['verdict'] == 'accepted_within_scope', 'gate identity or verdict: ' + name)

    def gtext(name):
        g = G[name]
        return norm(g['accepted'] + ' ' + g['decision'])

    def glims(name):
        return norm(' '.join(G[name]['limitations']))

    m = match(r'BB1 gate \(sha256 ([0-9a-f]{64}), accepted_within_scope\)', G['BB2']['accepted'], 'BB1 sha quoted in BB2')
    bb1_quoted = m.group(1)
    cross = {}
    for name, (rel, pin) in GATES.items():
        binders = sorted(other for other in G if G[other].get('bindings', {}).get(rel) == pin)
        cross[name] = binders
    cross['BB1'] = sorted(set(cross['BB1']) | {'BB2 (sha256 quoted in its accepted text)'}) if bb1_quoted == GATES['BB1'][1] else cross['BB1']

    def validate_cross(cr):
        for name in GATES:
            if name == 'BB2':
                continue
            require(len(cr[name]) >= 1, 'gate not bound by any later admitted gate: ' + name)
        return True
    check('gate_hashes_pinned_and_cross_bound',
          validate_cross(cross) and bb1_quoted == GATES['BB1'][1],
          pinned={k: v1[1] for k, v1 in GATES.items()}, bound_by=cross,
          note='every pinned gate except BB2 (the latest) is bound by hash in a later admitted gate or quoted by it; BB2 is pinned here')

    bound_anywhere = {}
    for rel, h in inventory.items():
        bound_anywhere[rel] = sorted(name for name in G if G[name].get('bindings', {}).get(rel) == h)
    unbound = sorted(rel for rel, b in bound_anywhere.items() if not b)
    check('snapshot_bytes_equal_gate_bindings',
          set(unbound) == {CONTRACT_REL, P_SEL, GATES['BB1'][0], GATES['BB2'][0]}
          and bound_anywhere[P_AV2F] and bound_anywhere[P_AV2R] and bound_anywhere[P_AV2S]
          and bound_anywhere[P_AW2F] and bound_anywhere[P_BB2F] and bound_anywhere[P_BB2R] and bound_anywhere[P_BB2S],
          unbound_snapshots=unbound, bound_by_counts={k: len(v1) for k, v1 in bound_anywhere.items()},
          note='every snapshot except the BC1 contract (sha256 pinned), the selection note, the BB1 gate (quoted by BB2) and the BB2 gate (pinned) is byte-identical to a binding of an admitted gate')

    # ======================= identification premise (BB2 items 1-3, BA2 item 4) =======================
    bb2 = gtext('BB2')
    gf2 = G['BB2']['gate_fields']
    ID_ANCHORS = {
        'item1': 'the reduced densities of the named construction families F1 and F2 on centered coarse cubes converge as whole sequences',
        'item2': 'Item 2: the F1 and F2 limits coincide on every finite region',
        'item3': 'this limit coincides with every AQ1 subsequential limit and every F2 subsequential limit',
        'item3b': 'Item 3: the limit equals every AQ1 subsequential limit (F1) and every F2 subsequential limit on every finite region',
    }
    ba2 = gtext('BA2')
    identification = {
        'bb2_items_admitted': all(a in bb2 for a in ID_ANCHORS.values()) and gf2['common_limit_claimed'] is True
        and gf2['whole_sequence_claimed'] is True and gf2['state_convergence_claimed'] is True
        and gf2['uniqueness_of_ground_state_claimed'] is False and gf2['gns_dynamics_equality_claimed'] is False,
        'ba2_limit_dynamics': 'the F2 limit dynamics equals the AQ1 limit dynamics T_theta' in ba2
        and G['BA2']['gate_fields']['dynamics_limit_identified_claimed'] is True,
        'aq1_nonempty': 'have a subsequence defining a compatible locally normal gauge-invariant stationary state' in norm(G['AQ1']['accepted']),
        'both_signs': 'both signs' in bb2,
    }
    check('bb2_identification_premise',
          all(identification.values()) and G['BB2']['sub_label'] == 'convergence_of_named_constructions',
          identification=identification, anchors=ID_ANCHORS, bb2_gate_sha256=GATES['BB2'][1],
          lemma='HNM-BC1-F01: at each sign the set of AQ1 subsequential limits, and the set of F2 subsequential limits, is exactly {omega_inf}',
          order='identification (BB2 items 2-3) precedes every inheritance')

    # ======================= AV2 certificate, parsed exactly from the AV2 gate =======================
    av2a, av2d = norm(G['AV2']['accepted']), norm(G['AV2']['decision'])
    m = match(r'exact rational datum d=(\d+)/\(4\*10\^40\)', av2a, 'AV2 datum')
    d_g = Q(int(m.group(1)), 4 * 10 ** 40)
    m = match(r'r<=R=(\d+)/10\^40', av2a, 'AV2 R')
    R_g = Q(int(m.group(1)), 10 ** 40)
    m = match(r'so C\(1\) in \[(\d+)/\(4\*10\^40\), (\d+)/\(8\*10\^39\)\] ~ \[([\d.]+), ([\d.]+)\]', av2a, 'AV2 interval')
    lo_g, hi_g = Q(int(m.group(1)), 4 * 10 ** 40), Q(int(m.group(2)), 8 * 10 ** 39)
    av2_prev = (m.group(3), m.group(4))
    m = match(r'exact datum (\d+)/\(4\*10\^40\) with complete point-error radius at most (\d+)/10\^40', av2d, 'AV2 decision d, R')
    d_dec, R_dec = Q(int(m.group(1)), 4 * 10 ** 40), Q(int(m.group(2)), 10 ** 40)
    m = match(r'D=(\d+)/(\d+) \(~1\.3612e-8\) by trace duality', av2a, 'AV2 state bound D')
    D_av2 = frac_of(m, 1)
    m = match(r'D_ii=(\d+)/(\d+) \(~1\.3612e-8; exact rational', norm(G['AV1']['accepted']), 'AV1 D_ii')
    D_av1 = frac_of(m, 1)
    arith_half = Q(1, 4 * 10 ** 40)
    require('plus the arithmetic half-width 1/(4*10^40)' in av2a, 'AV2 arithmetic half-width')
    require('M_0=||ghat||_1=2, M_1=4s/pi' in av2a and 'k=49|tau|/4 holds for every real theta uniformly in the box' in av2a, 'AV2 window constants and slope')
    m = match(r'crosses 10\^-6 at s\* in \[([\d.]+), ([\d.]+)\]', av2a, 'AV2 crossover')
    sstar_lo, sstar_hi = Q(m.group(1)), Q(m.group(2))
    check('av2_certificate_parsed_exact',
          d_g == d_dec and R_g == R_dec and d_g - R_g == lo_g and d_g + R_g == hi_g and D_av2 == D_av1
          and abs(preview_value(av2_prev[0]) - lo_g) < Q(1, 10 ** 15) and abs(preview_value(av2_prev[1]) - hi_g) < Q(1, 10 ** 15),
          d=s(d_g), d_gate_form='497870683678639429793424156500617766317/(4*10^40)' if d_g * 4 * 10 ** 40 == 497870683678639429793424156500617766317 else 'parsed',
          R=s(R_g), interval=[s(lo_g), s(hi_g)], D_av1=s(D_av1), window={'M_0': '2', 'M_1': '4s/pi', 'k': '49|tau|/4'},
          previews={'d': dec(d_g), 'R': dec(R_g), 'lo': dec(lo_g), 'hi': dec(hi_g), 'D': dec(D_av1)},
          read_from='AV2 gate accepted and decision strings (hash pinned); D equal to the AV1 gate D_ii')

    # consistency replays (exact; never a source of any restated value)
    pi_lo, pi_hi = pi_bracket()
    E_pi_lo = 2 * (D_av1 + D_av1 * D_av1) + 49 * tau / pi_lo + arith_half
    E_pi = 2 * (D_av1 + D_av1 * D_av1) + 49 * tau / pi_hi + arith_half
    av2f = read_input(P_AV2F)
    m = match(r'\| `kernel_dynamics` = `k M_1\^\+` = `49\|tau\|/pi\^-` \| `(\d+)/(\d+)` \|', av2f, 'AV2 forward kernel term')
    kF = frac_of(m, 1)
    r_fwd = 2 * (D_av1 + D_av1 * D_av1) + kF + arith_half
    e3_lo, e3_hi = exp_minus3_bracket()
    ref_lo, ref_hi = e3_lo / 4, e3_hi / 4
    check('av2_consistency_replays',
          E_pi_lo <= R_g and R_g - E_pi < Q(1, 10 ** 40) and E_pi <= r_fwd <= R_g and R_g - r_fwd < Q(1, 10 ** 40)
          and max(abs(d_g - ref_lo), abs(d_g - ref_hi)) <= arith_half and lo_g <= ref_lo and ref_hi <= hi_g,
          pi_bracket_width_below='1e-60', R_minus_formula_with_pi_upper=dec(R_g - E_pi, 4),
          forward_radius=s(r_fwd), R_minus_forward_radius=dec(R_g - r_fwd, 4),
          d_minus_reference_bound=dec(max(abs(d_g - ref_lo), abs(d_g - ref_hi)), 4),
          reference_enclosure=[dec_down(ref_lo, 20), dec_up(ref_hi, 20)],
          label='consistency replays of the gate formula; the restated d and R are the gate values, never these')

    RESTATED_NODE = {'state': 'omega_inf (limit of the named constructions, BB2 items 1-3)', 'node_s': Q(1), 'signs': ['+', '-'],
                     'd': d_g, 'R': R_g, 'interval': (lo_g, hi_g), 'minus_tau': 'replay of the same |tau| formula',
                     'sub_label': 'reference_unresolved', 'identification': 'BB2 items 2-3'}

    def validate_node_restatement(rs):
        require(rs['identification'] == 'BB2 items 2-3', 'the restatement rests on the BB2 identification')
        require(rs['node_s'] == V['nodes'][0], 'only the preregistered node')
        require(rs['d'] == d_g and rs['R'] == R_g and rs['interval'] == (lo_g, hi_g), 'restated AV2 values differ from the gate')
        require(rs['interval'] == (rs['d'] - rs['R'], rs['d'] + rs['R']), 'interval is [d-R, d+R]')
        return True
    check('av2_node_restated_for_limit',
          validate_node_restatement(RESTATED_NODE) and identification['bb2_items_admitted'],
          statement='at s=1 and tau=+10^-8, C(1)=<chi,e^{-G}chi> of omega_inf satisfies |C(1)-d|<=R; tau=-10^-8 is a replay of the same |tau| formula',
          d=s(d_g), R=s(R_g), interval=[s(lo_g), s(hi_g)], sub_label='reference_unresolved')

    # ======================= AW2 enclosure, parsed exactly from the AW2 and AW1 gates =======================
    aw2a, aw2d = norm(G['AW2']['accepted']), norm(G['AW2']['decision'])
    m = match(r'K_2\^\+=(\d+)/(\d+) \(~3354\.80322946, outward (\d+)/10\^12\)', aw2a, 'AW2 K_2^+')
    K_aw2 = frac_of(m, 1)
    K_ceiling = Q(int(m.group(3)), 10 ** 12)
    m = match(r'the bound value is K_2\^\+=(\d+)/(\d+)', norm(G['AW1']['accepted']), 'AW1 K_2^+')
    K_aw1 = frac_of(m, 1)
    m = match(r'Bind K_2\^\+ = (\d+)/(\d+)', norm(G['AW1']['decision']), 'AW1 decision K_2^+')
    K_aw1d = frac_of(m, 1)
    m = match(r'= \[(\d+)/D, (\d+)/D\], D=(\d+), contained in \[([\d.e-]+), ([\d.e-]+)\]', aw2a, 'AW2 endpoints')
    Den = int(m.group(3))
    L_g, U_g = Q(int(m.group(1)), Den), Q(int(m.group(2)), Den)
    aw2_prev = (m.group(4), m.group(5))
    m = match(r'the mirror \[-(\d+)/D, -(\d+)/D\]', aw2a, 'AW2 mirror')
    mirror_g = (-Q(int(m.group(1)), Den), -Q(int(m.group(2)), Den))
    m = match(r'exact endpoints (\d+)/D and (\d+)/D with D=(\d+)', aw2d, 'AW2 decision endpoints')
    L_dec, U_dec = Q(int(m.group(1)), int(m.group(3))), Q(int(m.group(2)), int(m.group(3)))
    m = match(r'exclusion margin \(\|tau\|/144-K_2\^\+ tau\^2\)/\(K_2\^\+ tau\^2\)=(\d+)/(\d+) \(~206\.00005', aw2a, 'AW2 exclusion margin')
    excl_g = frac_of(m, 1)
    m = match(r'sign margin 1/\(144 K_2\^\+ \|tau\|\)=(\d+)/(\d+) \(~207\.00005', aw2a, 'AW2 sign margin')
    signm_g = frac_of(m, 1)
    K2 = K_aw2
    Kt2 = K2 * tau ** 2
    check('aw2_enclosure_parsed_exact',
          K_aw2 == K_aw1 == K_aw1d and L_g == L_dec and U_g == U_dec
          and L_g == tau / 144 - Kt2 and U_g == tau / 144 + Kt2 and (L_g + U_g) / 2 == tau / 144
          and mirror_g == (-U_g, -L_g) and excl_g == (tau / 144 - Kt2) / Kt2 and signm_g == 1 / (144 * K2 * tau)
          and K_ceiling >= K2 and K_ceiling - K2 < Q(1, 10 ** 12)
          and preview_value(aw2_prev[0]) <= L_g and U_g <= preview_value(aw2_prev[1]),
          K2_plus=s(K2), K2_plus_preview=dec(K2), K2_plus_tau2=s(Kt2), L=s(L_g), U=s(U_g), mirror=[s(mirror_g[0]), s(mirror_g[1])],
          gate_outward_decimals=list(aw2_prev), exclusion_margin=s(excl_g), exclusion_margin_preview=dec(excl_g, 8),
          sign_margin=s(signm_g), sign_margin_preview=dec(signm_g, 8),
          read_from='AW2 gate accepted and decision strings and the AW1 gate bound value (hash pinned); endpoints recomputed as tau/144 -+ K_2^+ tau^2')

    RESTATED_SIGN = {'state': 'omega_inf (limit of the named constructions, BB2 items 1-3)', 'plus': (L_g, U_g), 'minus': mirror_g,
                     'K2_plus': K2, 'minus_tau': 'mirror replay (AW1 remainder at both signs, AW1 flip lemma)',
                     'sub_label': 'static_not_dynamic', 'identification': 'BB2 items 2-3'}

    def validate_sign_restatement(rs):
        require(rs['identification'] == 'BB2 items 2-3', 'the restatement rests on the BB2 identification')
        require(rs['K2_plus'] == K2 and rs['plus'] == (L_g, U_g) and rs['minus'] == mirror_g, 'restated AW2 values differ from the gate')
        require(rs['plus'][0] > 0 and rs['minus'][1] < 0, 'zero excluded at both signs')
        return True
    check('aw2_enclosure_restated_for_limit',
          validate_sign_restatement(RESTATED_SIGN),
          statement='omega_inf(W) lies in [L,U] at tau=+10^-8 and in [-U,-L] at tau=-10^-8 (mirror replay); sign(omega_inf(W))=sign(tau)',
          sub_label='static_not_dynamic')

    # ======================= BB2 whole-sequence constant C' =======================
    m = match(r"Item 1: sup over M greater than N of \|\|rho\^\{F,M\}_R-rho\^\{F,N\}_R\|\|_1 <= C' q\^\(N-1\) with C'=(\d+)/(\d+) "
              r"\(about ([\d.e-]+); exact_first_order, nested_telescoping, hypothesis source bb1_frozen_targets, BB1 route polymer_kp", bb2, 'BB2 item 1 C\'')
    Cp_acc = frac_of(m, 1)
    m = match(r"bound values C'=(\d+)/(\d+) \(about [\d.e-]+\) and c'_site=(\d+)/(\d+)", bb2, 'BB2 decision bound values')
    Cp_dec = frac_of(m, 1)
    m = match(r'forward nested_telescoping over the hypotheses C_h=(\d+)/(\d+)', bb2, 'BB2 C_h')
    C_h = frac_of(m, 1)
    m = match(r'the R form C q\^\(N-1\) with q=(\d+)/(\d+)', bb2, 'BB2 q')
    q_bb2 = frac_of(m, 1)
    m = match(r"the union_comparison route proves C'=(\d+)/(\d+)", bb2, 'BB2 union C\'')
    Cp_union = frac_of(m, 1)
    m = match(r"re-evaluated at the admitted BB1 values \(labelled, not bound\), C' is about ([\d.e-]+)", bb2, 'BB2 re-evaluated C\'')
    Cp_reeval = preview_value(m.group(1))
    m = match(r'q=1/64 and C=(\d+)/(\d+) \(about 8\.9051e-07', norm(G['BB1']['accepted']), 'BB1 bound value C')
    C_bb1 = frac_of(m, 1)
    m = match(r'certified range 5<=N<=(\d+)', bb2, 'BB2 certified range')
    N_rate_max = int(m.group(1))
    m = match(r'vacuous from N=(\d+)', bb2, 'BB2 vacuity')
    N_vacuous = int(m.group(1))
    m = match(r'K5 about ([\d.e-]+)', bb2, 'BB2 K5')
    K5_prev = m.group(1)
    Cp = Cp_acc
    check('bb2_whole_sequence_constant',
          Cp_acc == Cp_dec and Cp == C_h / (1 - q_bb2) and q_bb2 == q and Cp_union == C_h and Cp_union != Cp
          and Cp_reeval < Cp and C_bb1 < C_h and N_rate_max == 14000 and N_vacuous == 14419,
          C_prime=s(Cp), C_prime_preview=dec(Cp), C_h=s(C_h), q=s(q_bb2), C_prime_equals='C_h/(1-q)=(64/63)C_h',
          labelled_not_used={'union_comparison': s(Cp_union), 're_evaluated_preview': dec(Cp_reeval, 5), 'BB1_per_comparison_C_preview': dec(C_bb1, 5)},
          correlation_rate_range=[5, N_rate_max], vacuous_from=N_vacuous, K5_preview=K5_prev,
          labels={'tier': 'exact_first_order', 'assembly': 'nested_telescoping', 'hypothesis_source': 'bb1_frozen_targets', 'bb1_route': 'polymer_kp'})

    # ======================= Item 3: the F2 finite-box sign corollary =======================
    def widen(N, C=Cp, qq=q):
        return C * qq ** (N - 1)

    def least_N(C, qq, lower):
        N = V['N_min']
        while not (widen(N, C, qq) < lower):
            N += 1
            require(N < 200, 'no N_sign below 200')
        return N
    N_sign = least_N(Cp, q, L_g)
    table = []
    for N in range(V['N_min'], 9):
        w = widen(N)
        table.append({'N': N, 'widening': s(w), 'widening_preview': dec(w), 'lower_plus': s(L_g - w), 'lower_plus_preview': dec(L_g - w),
                      'upper_plus': s(U_g + w), 'upper_minus': s(-L_g + w), 'certified': (L_g - w) > 0 and (-L_g + w) < 0})
    monotone = all(widen(N + 1) < widen(N) for N in range(V['N_min'], 40))
    lo4, hi4 = L_g - widen(N_sign), U_g + widen(N_sign)
    FINITE_BOX = {'kind': 'bb2_whole_sequence_sup_over_M_then_M_to_infinity', 'C': Cp, 'q': q, 'N_sign': N_sign,
                  'source': "BB2 gate decision: nested_telescoping bound value C'", 'observable_norm_at_most': Q(1)}
    check('f2_finite_box_sign_corollary',
          N_sign == 4 and all(t['certified'] == (t['N'] >= N_sign) for t in table) and monotone and lo4 > 0 and -lo4 < 0
          and widen(N_sign) == Q(1, 64512000000) and widen(2) == Q(1, 15750000) and widen(3) == Q(1, 1008000000),
          theorem='HNM-BC1-F04: for every N at least 2 the untruncated F2 ground state has omega^{F2,N}(W) in [L-C q^(N-1), U+C q^(N-1)] at +tau and in the mirror at -tau; sign certified for every N at least N_sign at both signs',
          N_sign=N_sign, table=table, widened_at_N_sign=[s(lo4), s(hi4)], widened_at_N_sign_directed=[dec_down(lo4), dec_up(hi4)],
          widened_mirror_at_N_sign=[s(-hi4), s(-lo4)], ratio_L_over_widening_preview=dec(L_g / widen(N_sign), 8),
          widened_exclusion_margin_preview=dec(lo4 / (Kt2 + widen(N_sign)), 8),
          rate_in_N='q^(N-1) with q=1/64, for every N at least 2', proof_steps=['BB2 item 1 (F=F2, untruncated, every M greater than N)',
                                                                              'M to infinity by BB2 items 1-2 and continuity of the trace norm',
                                                                              'trace duality with ||W|| at most 1', 'AW2 enclosure for omega_inf (item 2)',
                                                                              'strict decrease of C q^(N-1) in N'])

    check('f1_boxes_recorded',
          'and in every centered whole-star box N>=2 at every on-site cutoff' in aw2a
          and 'The on-site cutoff is removed for the ground vector itself in each fixed box' in norm(G['AV1']['accepted']),
          statement='F1 boxes: AW2 certifies the enclosure at every N at least 2 at every on-site cutoff; the untruncated F1 vector follows by the AV1 cutoff-vector removal and the closed interval (recorded as agreement, not re-derived)')

    t100 = tau / 100
    half100 = K2 * t100 ** 2 + widen(N_sign)
    check('tau_over_100_information_only',
          half100 > t100 / 144,
          half_width_at_tau_over_100_preview=dec(half100, 5), first_order_at_tau_over_100_preview=dec(t100 / 144, 5), claimed=False,
          note='information only: AW2 admits the enclosure at the cap only and C at the hypothesis values does not depend on tau; nothing is claimed below the cap')

    # trap fixtures (exact)
    harm, n_h = Q(0), 1
    while harm <= 4:
        n_h += 1
        harm += Q(1, n_h)
    alt = [Q(1, 2) + Q((-1) ** n, 100) for n in range(2, 12)]
    ball_ok = all(abs(x - Q(1, 2)) <= Q(1, 50) for x in alt) and len(set(alt)) == 2
    dl, dx = [Q(1, 2), Q(-1, 2)], [Q(1), Q(-1)]
    dual = sum(a * b for a, b in zip(dl, dx))
    dual2 = sum(a * 2 * b for a, b in zip(dl, dx))
    tn = sum(abs(a) for a in dl)
    bb2f = read_input(P_BB2F)
    bb2f_harm_text = 'has steps `1/(N+1) → 0` and exceeds 4 at `N=119`'
    check('trap_fixtures',
          n_h == 83 and ball_ok and dual == tn and dual2 == 2 * tn and dual2 > tn and (L_g - widen(3)) < 0 and bb2f_harm_text in bb2f,
          harmonic={'a_N': 'sum_{k=2}^N 1/k', 'steps': '1/N tending to 0', 'first_N_exceeding_4': n_h},
          alternating={'sequence': 'diag(1/2+(-1)^N/100, 1/2-(-1)^N/100)', 'within_1/50_of_diag(1/2,1/2)': ball_ok, 'subsequential_limits': 2},
          duality={'Delta': 'diag(1/2,-1/2)', 'X': 'diag(1,-1)', 'Tr(Delta X)': s(dual), 'trace_norm': s(tn), 'Tr(Delta 2X)': s(dual2), 'meaning': 'duality is attained, so the factor ||W|| at most 1 is needed'},
          off_by_one={'N': 3, 'widened_lower_end': s(L_g - widen(3)), 'preview': dec(L_g - widen(3))},
          premise_observation='the BB2 forward report section 9 states that the harmonic partial sums exceed 4 at N=119; the exact first exceedance is N=83 (a fixture description only; no BB2 constant or gate statement depends on it)')

    # ======================= Item 4: finite-box node record =======================
    av2r = read_input(P_AV2R)
    sec12 = av2r.split('## 12. ', 1)[1].split('\n## 13. ', 1)[0]
    cmr = [ln for ln in sec12.splitlines() if ln.startswith('| changed_model_relabelled |')]
    RECORD = {
        'av2_gate_each_aq1_state': 'every AQ1 subsequential state of the centered whole-star construction (each chosen state separately' in av2a,
        'forward_tags': all('\\tag{HNM-AV2-F%02d}' % k in av2f for k in (1, 2, 7, 13, 14, 15)),
        'forward_nonnegativity_only': 'By **AQ1 §5 (nonnegativity only)**' in av2f,
        'forward_slope_passed_to_AQ': 'So (F14) holds for the actual AQ evolution at **every real** `theta`.' in av2f,
        'reverse_tags': all('\\tag{HNM-AV2-R%02d}' % k in av2r for k in (1, 2, 8, 12, 13)),
        'reverse_nonnegativity_only': '**Only this nonnegativity is used; AQ2\'s gap is not.**' in av2r,
        'reverse_finite_box_provenance_mutation': len(cmr) == 1 and 'finite-box provenance' in cmr[0],
        'aw1_nonuniform_tau2': 'with the tau^2 constant explicitly unbounded (not uniform in N' in norm(G['AW1']['accepted']),
    }
    check('finite_box_node_record_facts',
          all(RECORD.values()),
          record=RECORD, conclusion='the admitted record does not prove a finite-box node; BC1 restates none, for F1 or for F2 boxes; rows N2 and N3 are open')

    # ======================= Item 5: common GNS item =======================
    GNS = {'states': 1, 'basis': 'BB2 items 2-3', 'triple': 'one GNS triple (pi_inf, H_inf, Omega_inf), determined up to unitary equivalence',
           'dynamics': 'the AQ1 limit dynamics T_theta implemented in that representation (AQ1 for F1; BA2 item (4) for F2)',
           'correlations': 'limits of the finite-box correlation functions of either family on theta in [-8,8] (BB2 item 5)',
           'rate': 'K5/N only on 5<=N<=%d; vacuous from N=%d; convergence without a rate beyond' % (N_rate_max, N_vacuous),
           'gns_dynamics_equality_claimed': False}

    def validate_gns(gg):
        require(gg['states'] == 1 and gg['basis'] == 'BB2 items 2-3', 'one state, by the BB2 identification')
        require(identification['bb2_items_admitted'] and identification['ba2_limit_dynamics'], 'BB2 identification and BA2 limit dynamics admitted')
        require(gg['gns_dynamics_equality_claimed'] is False, 'no equality of GNS dynamics of different states')
        require('different states' not in gg['triple'] + gg['dynamics'], 'phrased as one state, never as different states')
        require('5<=N<=14000' in gg['rate'], 'correlation rate with its range')
        return True
    check('common_gns_item_scope',
          validate_gns(GNS) and 'Item 5: for N at least 5, r_N=floor((N-1)/2), |theta| at most 8 and A in B(H_R)' in bb2,
          gns_item=GNS)

    # ======================= Item 6: obligations table, falsifying scenario, limitations =======================
    report_text = (BASE / 'report.md').read_text(encoding='utf-8')
    ay2a = norm(G['AY2']['accepted'])
    m = match(r'\(5\) Six obligations, all unproved, each with its missing premise and candidate route: (.*?)\. \(6\)', ay2a, 'AY2 item (5)')
    o_names = [p.split(', not proved')[0].strip() for p in split_top_level(m.group(1))]
    require(len(o_names) == 6, 'six AY2 obligations')
    nr = V['new_rows']
    require(nr[1] == 'the finite-box Euclidean node for F2 boxes and for finite F1 boxes (item 4)', 'item-4 entry of the contract list')
    n_names = [nr[0], 'the finite-box Euclidean node for finite F1 boxes (item 4)', 'the finite-box Euclidean node for F2 boxes (item 4)'] + nr[2:]
    n12 = V['claim_exclusions'][2] + ' (carried from Round32, not a Round33 gate row)'
    n_names.append(n12)
    CLOSE = {
        'O1': ('BB2', ['this limit coincides with every AQ1 subsequential limit and every F2 subsequential limit'], ['BB2 gate items 2-3']),
        'O2': ('BB2', ['converge as whole sequences'], ['BB2 gate item 1', 'BA2 gate']),
        'O3': ('BB2', ['is invariant under coarse translations'], ['BB2 gate item 4']),
        'O4': ('BB2', ["C'=4/984375", '5<=N<=14000'], ['BB2 gate item 1', 'every N at least 2', '5<=N<=14000']),
        'O5': ('BA2', ['the F2 limit dynamics equals the AQ1 limit dynamics T_theta'], ['BA2 gate items (1)-(4)']),
        'O6': ('BA2', ['AY2 row O6 closed within scope'], ['BA2 gate', 'AY2 row O6 closed within scope']),
    }
    have_bc2_gate = any('bc2-gate' in k for k in inventory)

    def parse_obligations(text):
        sec = text.split('### 8.1 Table', 1)
        require(len(sec) == 2, 'obligations section 8.1 missing')
        body = sec[1].split('\n### 8.2', 1)[0]
        out = []
        for ln in body.splitlines():
            if re.match(r'^\| [ON]\d+ \|', ln):
                cols = [x.strip() for x in ln.strip().strip('|').split(' | ')]
                require(len(cols) == 6, 'obligation row must have six columns: ' + ln[:40])
                out.append({'id': cols[0], 'obligation': cols[1], 'status': cols[2], 'closing_gate_and_scope': cols[3],
                            'missing_premise': cols[4], 'candidate_route': cols[5]})
        return out

    def validate_obligations(rows):
        ids = ['O%d' % k for k in range(1, 7)] + ['N%d' % k for k in range(1, 13)]
        require([r1['id'] for r1 in rows] == ids, 'obligation rows missing, added or reordered')
        for r1, name in zip(rows[:6], o_names):
            require(r1['obligation'] == name, 'AY2 row renamed: ' + r1['id'])
            require(r1['status'] == 'closed_within_scope', 'AY2 row status: ' + r1['id'])
            gate, anchors, cell_needs = CLOSE[r1['id']]
            require(all(a in gtext(gate) for a in anchors), 'closing gate text lacks the anchor: ' + r1['id'])
            require(all(x in r1['closing_gate_and_scope'] for x in cell_needs) and 'scope:' in r1['closing_gate_and_scope'],
                    'closed row without its closing gate and scope: ' + r1['id'])
        for r1, name in zip(rows[6:], n_names):
            require(r1['obligation'] == name, 'new row renamed: ' + r1['id'])
            require(r1['status'] == 'open' and r1['closing_gate_and_scope'] == 'none (open)', 'new row must be open: ' + r1['id'])
        for r1 in rows:
            require(len(r1['missing_premise']) > 12 and len(r1['candidate_route']) > 12, 'empty premise or route: ' + r1['id'])
        n4, n5, n9 = rows[9], rows[10], rows[14]
        require('N_sign=4' in n4['missing_premise'] and 'N=2 and N=3' in n4['missing_premise']
                and '1/15750000' in n4['missing_premise'] and '1/1008000000' in n4['missing_premise'], 'N4 row values')
        require('5<=N<=14000' in n5['missing_premise'] and 'N=14419' in n5['missing_premise'], 'N5 row range')
        if not have_bc2_gate:
            require(all('bc2-gate' not in (r1['closing_gate_and_scope'] + r1['missing_premise'] + r1['candidate_route']) for r1 in rows),
                    'a BC2 gate is cited before it is recorded')
        require('only once it is recorded' in n9['candidate_route'], 'N9 cites the BC2 gate only once recorded')
        return True
    obligations = parse_obligations(report_text)

    def mut_rows(k, **kw):
        return [dict(r1, **kw) if i == k else r1 for i, r1 in enumerate(obligations)]
    check('obligations_table_complete',
          validate_obligations(obligations)
          and rejected(lambda: validate_obligations([r1 for r1 in obligations if r1['id'] != 'N3']), 'finite_F2_box_node_row_removed')
          and rejected(lambda: validate_obligations(mut_rows(0, closing_gate_and_scope='executed')), 'O1_closed_without_its_gate_and_scope')
          and rejected(lambda: validate_obligations(mut_rows(6, status='closed_within_scope')), 'N1_states_outside_marked_closed')
          and rejected(lambda: validate_obligations(mut_rows(7, candidate_route='')), 'N2_candidate_route_emptied')
          and rejected(lambda: validate_obligations(mut_rows(14, candidate_route='cites research/round33/advisor/bc2-gate.json; only once it is recorded')),
                        'N9_cites_an_unrecorded_BC2_gate')
          and rejected(lambda: validate_obligations([obligations[1], obligations[0]] + obligations[2:]), 'rows_reordered'),
          rows=len(obligations), ay2_rows_closed=[r1['id'] for r1 in obligations if r1['status'] == 'closed_within_scope'],
          open_rows=[r1['id'] for r1 in obligations if r1['status'] == 'open'],
          source='O-row names from the AY2 gate item (5); N-row names from the contract parameters.obligations (item-4 entry split in two) plus the carried Round32 row N12')

    fs = 'The falsifying scenario is not excluded' in ay2a
    FALSIFIER = {'excluded_for': ['F1', 'F2'], 'by': 'BB2 items 2-3', 'states_outside_excluded': False, 'witness_still_admissible_pair': True}
    check('falsifying_scenario_named_constructions_only',
          fs and FALSIFIER['states_outside_excluded'] is False and identification['bb2_items_admitted'],
          falsifying_scenario=FALSIFIER, ay2_anchor='(4) The falsifying scenario is not excluded')

    def parse_limitations(text):
        sec = text.split('### 8.3 ', 1)[1].split('\n## 9. ', 1)[0]
        out = []
        for ln in sec.splitlines():
            if re.match(r'^\| L\d+ \|', ln):
                cols = [x.strip() for x in ln.strip().strip('|').split(' | ')]
                require(len(cols) == 5, 'limitation row must have five columns')
                out.append({'id': cols[0], 'gate': cols[1], 'anchor': cols[2], 'status': cols[3], 'by': cols[4]})
        return out

    def validate_limitations(rows):
        require(len(rows) == 13, 'thirteen limitation rows')
        for r1 in rows:
            require(r1['gate'] in ROUND32_GATES, 'limitation row names a Round32 gate')
            require(r1['anchor'] in glims(r1['gate']), 'anchor is not a verbatim substring of the gate limitations: ' + r1['id'])
            require(r1['status'] in ('lifted_in_part', 'lifted_within_scope', 'remains', 'updated'), 'status vocabulary')
            if r1['status'] == 'remains':
                require(r1['by'].startswith('no Round33 gate'), 'a remaining limitation cites no lifting gate')
            else:
                require('BB2' in r1['by'] or 'BA2' in r1['by'], 'a lifted limitation names its Round33 gate')
        return True
    lim_rows = parse_limitations(report_text)
    check('round32_limitations_lifted_or_remaining',
          validate_limitations(lim_rows)
          and rejected(lambda: validate_limitations([dict(r1, anchor=r1['anchor'] + ' and uniqueness') if r1['id'] == 'L1' else r1 for r1 in lim_rows]), 'anchor_not_in_gate')
          and rejected(lambda: validate_limitations([dict(r1, status='lifted_in_part', by='no Round33 gate') if r1['id'] == 'L2' else r1 for r1 in lim_rows]), 'lifted_without_gate'),
          rows=[{k: r1[k] for k in ('id', 'gate', 'status')} for r1 in lim_rows])

    # ======================= mandatory sentence, phrasing, rates, placeholders =======================
    template = V['template']
    nrep = norm(report_text)

    def validate_template(text):
        require(norm(text).count(norm(template)) == 1, 'the template must appear exactly once')
        require(any(ln.strip() == template for ln in text.splitlines()), 'the template must be one unbroken line')
        return True
    check('mandatory_sentence_once',
          validate_template(report_text) and nrep.count(norm(template)) == 1,
          template=template, values={'d': s(d_g), 'R': s(R_g), 'L': s(L_g), 'U': s(U_g), 'N_sign': N_sign})

    # ======================= gate fields, flags, labels, ledger =======================
    GF = dict(V['gate_fields'])
    GATE_FIELDS = {'node_certificate_restated_for_limit': True, 'sign_certificate_restated_for_limit': True, 'finite_box_sign_claimed': True,
                   'finite_box_sign_scope': V['gate_fields']['finite_box_sign_scope'], 'dynamics_limit_identified_claimed': True,
                   'rate_in_N_claimed': True, 'uniqueness_of_ground_state_claimed': False, 'gns_dynamics_equality_claimed': False,
                   'uniform_in_time_claimed': False, 'rate_in_a_claimed': False, 'continuum_claim': False, 'weak_coupling_claim': False,
                   'scientific_priority_verified': False, 'finite_box_node_claimed': False, 'correlation_shift_resolved': False}

    def validate_gate_fields(g):
        require(sorted(g) == sorted(GF), 'gate field set differs from gate_fields_required')
        for k1, v1 in GF.items():
            require(g[k1] == v1, 'gate field ' + k1 + ' differs from the preregistered value')
        return True

    def gfm(**kw):
        g2 = dict(GATE_FIELDS)
        g2.update(kw)
        return lambda: validate_gate_fields(g2)
    check('gate_fields_exported',
          validate_gate_fields(GATE_FIELDS)
          and rejected(gfm(correlation_shift_resolved=True), 'correlation_shift_resolved_true')
          and rejected(gfm(finite_box_sign_scope='F2 boxes at every N at least 2'), 'finite_box_sign_scope_widened')
          and rejected(lambda: validate_gate_fields({k1: v1 for k1, v1 in GATE_FIELDS.items() if k1 != 'rate_in_a_claimed'}), 'field_missing'),
          gate_fields=GATE_FIELDS, rule=c['preregistration']['gate_fields_rule'])

    ledger = {
        'identification_premise_bb2': {'value': '0', 'kind': 'exact identification (admitted premise, BB2 items 2-3)'},
        'restated_constants_exactness': {'value': '0', 'kind': 'restated d, R, interval, K_2^+ and endpoints equal the gate rationals'},
        'finite_box_whole_sequence_term': {'value': "C' q^(N-1)", 'C_prime': s(Cp), 'q': s(q), 'at_N_sign': s(widen(N_sign)),
                                           'at_N_sign_preview': dec(widen(N_sign)), 'sides': 'both'},
        'second_order_remainder_K2plus': {'value': s(Kt2), 'preview': dec(Kt2), 'sides': 'both endpoints'},
        'arithmetic': {'status': 'not_applicable', 'reason': 'every value is an exact rational; e^{-3}/4 and pi enter only through the AV2 gate datum and radius, whose arithmetic half-width 1/(4*10^40) is inside R; BC1 rounds nothing; decimals are labelled previews'},
    }
    check('error_ledger_itemized',
          list(ledger) == V['error_terms'] and 'stated reason' in V['error_terms_rule'] and 'reason' in ledger['arithmetic'],
          ledger=ledger, preregistered=V['error_terms'])

    LABEL = {'new_constant_family': 'widened finite-box enclosure and N_sign', 'tier': 'exact_first_order',
             'inputs_in_place_of_a_route': {'AW2_endpoints': 'AW2 gate (static_not_dynamic; K_2^+ at the AW1 exact tier)',
                                            'C_prime': {'assembly': 'nested_telescoping', 'hypothesis_source': 'bb1_frozen_targets', 'bb1_route': 'polymer_kp'}},
             'restated_labels_unchanged': {'AV2': 'reference_unresolved', 'AW2': 'static_not_dynamic'},
             'sub_labels': ['certificate_restated_for_limit', 'reference_unresolved', 'static_not_dynamic']}

    def validate_label(lb):
        require(lb['tier'] in V['tiers'] and lb['tier'] == 'exact_first_order', 'tier of the new constant family')
        require(all(x in V['sub_labels'] for x in lb['sub_labels']), 'sub-labels from the allowed list')
        require(lb['restated_labels_unchanged'] == {'AV2': 'reference_unresolved', 'AW2': 'static_not_dynamic'}, 'restated labels never relabelled')
        require(lb['inputs_in_place_of_a_route']['C_prime']['assembly'] == 'nested_telescoping', 'C assembly label')
        return True
    check('label_block_and_tier',
          validate_label(LABEL)
          and rejected(lambda: validate_label(dict(LABEL, tier='first_order_distance_from_product')), 'wrong_tier_for_the_new_family')
          and rejected(lambda: validate_label(dict(LABEL, restated_labels_unchanged={'AV2': 'certificate_restated_for_limit', 'AW2': 'static_not_dynamic'})), 'restated_constant_relabelled'),
          label=LABEL)

    # ======================= the 25 contract controls =======================
    FLAGS = {'continuum_claim': False, 'scientific_priority_verified': False, 'weak_coupling_claim': False, 'rate_in_a_claimed': False,
             'uniqueness_of_ground_state_claimed': False}

    def validate_flags(fl):
        for k1, v1 in FLAGS.items():
            require(fl.get(k1) is v1, 'claim flag ' + k1 + ' must be false')
        return True

    def fmut(**kw):
        f2 = dict(FLAGS)
        f2.update(kw)
        return lambda: validate_flags(f2)
    check('no_priority_or_continuum_claim',
          validate_flags(FLAGS)
          and rejected(fmut(continuum_claim=True), 'continuum_true') and rejected(fmut(scientific_priority_verified=True), 'priority_true')
          and rejected(fmut(weak_coupling_claim=True), 'weak_coupling_true') and rejected(fmut(rate_in_a_claimed=True), 'rate_in_a_true'),
          flags=FLAGS, historical_or_occult_numeric_premise=False)

    check('exact_arithmetic_admission',
          isinstance(d_g, Q) and isinstance(R_g, Q) and isinstance(Cp, Q) and rat('4/984375') == Cp
          and rejected(lambda: rat(1e-8), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('nan'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator')
          and rejected(lambda: rat(dec(R_g)), 'decimal_preview_as_admission_value'),
          arithmetic='fractions.Fraction throughout; pi and e^{-3} only in consistency replays, by directed series enclosures; previews are truncations or directed decimals')

    FAMS = ('F1 = AQ1 centered whole-star boxes', 'F2 = I1 section 6 all-contained-face boxes with padding')
    MODEL = {'model_id': V['model_id'], 'tau': tau, 'triple': (0, 0, 0), 'families': FAMS, 'cover': 'R={0,e_z}',
             'node_provenance': 'GNS vector of omega_inf', 'finite_graph': False}

    def validate_model(mdl):
        require(mdl['model_id'] == 'AQ_patterned_zero_selected', 'model id')
        require(abs(mdl['tau']) == tau, 'coupling differs from the preregistered value')
        require(mdl['triple'] == (0, 0, 0), 'nonzero selected triple is another model')
        require(mdl['families'] == FAMS, 'families relabelled')
        require(mdl['cover'] == 'R={0,e_z}', 'cover')
        require(mdl['node_provenance'] == 'GNS vector of omega_inf', 'finite-box provenance is a changed model (AV2 reverse section 12)')
        require(mdl['finite_graph'] is False, 'a finite graph is not the family')
        return True

    def mmut(**kw):
        m2 = dict(MODEL)
        m2.update(kw)
        return lambda: validate_model(m2)
    check('changed_model_relabelled',
          validate_model(MODEL) and validate_model(dict(MODEL, tau=-tau))
          and rejected(mmut(model_id='AQ_uniform_routeB'), 'uniform_route_B_model')
          and rejected(mmut(triple=(Q(1, 100), 0, 0)), 'nonzero_triple')
          and rejected(mmut(tau=Q(1, 10 ** 7)), 'tau_above_the_cap')
          and rejected(mmut(families=(FAMS[0], 'literal vertex boxes (I1 section 7)')), 'literal_vertex_boxes_family')
          and rejected(mmut(node_provenance='untruncated F1 box ground vector'), 'finite_box_provenance_for_the_node')
          and rejected(mmut(finite_graph=True), 'finite_graph_result_under_the_family_label'),
          model=dict(MODEL, tau=s(tau)))

    verdict = forward_verdict(True, True, True, True, True, False)

    def validate_verdict(reported, *args):
        require(reported == forward_verdict(*args), 'reported verdict differs from the contract acceptance rule')
        return True

    def validate_open_rows_not_failure(label_for_N23):
        require(label_for_N23 == 'open obligation row', 'N=2,3 of F2 is an open obligation, not a failure')
        return True

    def validate_retained(sign_claimed_Ns):
        for N in sign_claimed_Ns:
            require(L_g - widen(N) > 0, 'sign claimed at N=%d where the widened interval at unchanged tau, q and C contains 0' % N)
        return True
    check('insufficient_verdict_retained',
          verdict == 'accepted_within_scope' and forward_verdict(True, False, True, True, True, False) == 'insufficient'
          and forward_verdict(True, True, False, True, True, False) == 'limited' and forward_verdict(False, True, True, True, True, False) == 'insufficient'
          and validate_open_rows_not_failure('open obligation row')
          and rejected(lambda: validate_verdict('accepted_within_scope', True, False, True, True, True, False), 'differing_constant_relabelled_accepted')
          and rejected(lambda: validate_verdict('accepted_within_scope', True, True, False, True, True, False), 'omitted_corollary_relabelled_accepted')
          and rejected(lambda: validate_verdict('limited', True, True, True, True, True, True), 'overclaim_relabelled_limited')
          and validate_retained(list(range(N_sign, 12)))
          and rejected(lambda: validate_open_rows_not_failure('failure'), 'open_rows_N2_N3_counted_as_failure')
          and rejected(lambda: validate_retained(list(range(2, 12))), 'sign_claimed_for_N_2_3_retuned'),
          rule='insufficient if the identification is not admitted, a restated constant differs or a flag overreaches; limited if the corollary, the GNS item or the table is missing',
          verdict=verdict)

    m_coef = match(r'\(3\) omega_tau\(W\)=\+tau/144\+r\(tau\)', norm(G['AW1']['accepted']), 'AW1 first-order coefficient')
    coef = Q(1, 144)
    alpha_fx, hbar_fx, tE_fx, t_fx = Q(5), Q(7), Q(7, 5), Q(56, 5)
    s_fx, theta_fx = alpha_fx * tE_fx / hbar_fx, alpha_fx * t_fx / hbar_fx

    def validate_clock(exponent, clock):
        require(clock == 's=alpha*t_E/hbar' and exponent == 3, 'free Wilson energy 3 in the alpha clock (24 only with u=s/8)')
        return True

    def validate_window(theta_max):
        require(theta_max == 8, 'the BA2 window is theta in [-8,8], i.e. u in [-1,1]')
        return True

    def validate_coef(cf):
        require(cf == coef and (L_g + U_g) / 2 == cf * tau, 'first-order Wilson coefficient tau/144 (normalized delta=alpha/8)')
        return True
    check('wrong_delta_alpha_hbar_clock',
          m_coef is not None and validate_clock(3, 's=alpha*t_E/hbar') and validate_window(8) and validate_coef(coef)
          and s_fx == 1 and theta_fx == 8 and theta_fx / 8 == 1
          and rejected(lambda: validate_clock(24, 's=alpha*t_E/hbar'), 'exponent_24_with_the_s_clock')
          and rejected(lambda: validate_window(1), 'window_in_u_labelled_theta')
          and rejected(lambda: validate_coef(Q(1, 1152)), 'coefficient_tau_over_1152')
          and rejected(lambda: validate_coef(Q(1, 18)), 'coefficient_tau_over_18'),
          clock=V['clock'], nonunit_fixture={'alpha': '5', 'hbar': '7', 't_E': '7/5', 's': s(s_fx), 't': '56/5', 'theta': s(theta_fx), 'u': s(theta_fx / 8)})

    packet_strings_probe = [V['template'], GATE_FIELDS['finite_box_sign_scope'], GNS['rate'], GNS['dynamics']]

    def validate_placeholders(contract_obj, report, extra):
        require(not placeholder_spans(list(strings_of(contract_obj)) + extra), 'placeholder span in the contract or packet strings')
        require(not report_placeholders(report), 'placeholder span in the report')
        return True
    c_bad = json.loads(json.dumps(c))
    c_bad['selected_after'] = '<preceding gate>'
    check('placeholder_span_rejected',
          validate_placeholders(c, report_text, packet_strings_probe)
          and rejected(lambda: validate_placeholders(c_bad, report_text, packet_strings_probe), 'preceding_gate_placeholder_in_contract')
          and rejected(lambda: validate_placeholders(c, report_text + '\nThe value is <fill in N_sign>.\n', packet_strings_probe), 'placeholder_span_in_report'),
          rule='angle-bracket spans with whitespace, a vertical bar or e.g. (freezer R1) in contract and packet strings; letter-led spans in the report')

    FORBIDDEN = ROUND_FORBIDDEN + V['forbidden']

    def validate_phrasing(text):
        require(not affirmative(phrase_hits(text, FORBIDDEN, template)), 'affirmative forbidden phrasing')
        validate_template(text)
        return True
    neg_fixture = phrase_hits('This is not the thermodynamic limit.', FORBIDDEN)
    check('negation_aware_phrase_scan',
          validate_phrasing(report_text) and neg_fixture and not affirmative(neg_fixture)
          and rejected(lambda: validate_phrasing(report_text + '\nThe limit of the named constructions is the thermodynamic limit.\n'), 'affirmative_thermodynamic_limit')
          and rejected(lambda: validate_phrasing(report_text + '\nThe limit is the infinite-volume ground state.\n'), 'affirmative_definite_infinite_volume_state')
          and rejected(lambda: validate_phrasing(report_text + '\nThe replay confirms the node.\n'), 'affirmative_confirms')
          and rejected(lambda: validate_phrasing(report_text + '\nThe restated node resolves the reference.\n'), 'affirmative_resolves_the_reference')
          and rejected(lambda: validate_phrasing(report_text + '\n' + template + '\n'), 'template_twice'),
          forbidden_list_size=len(FORBIDDEN), template_removed_as_one_literal=True, negated_fixture_passes=True)

    PARAMS = dict(V['params'])

    def validate_params(p):
        for k1 in ('metric', 'weights', 'window', 'clock', 'node', 'N_min'):
            require(k1 in p and str(p[k1]).strip(), 'parameters must declare ' + k1)
        require(p['weights'].startswith('not applicable:') and len(p['weights']) > 20, 'weights not applicable only with a reason')
        return True

    def pdrop(k1):
        return lambda: validate_params({k2: v2 for k2, v2 in PARAMS.items() if k2 != k1})
    check('parameters_declare_metric_weights_window',
          validate_params(PARAMS)
          and rejected(pdrop('window'), 'window_removed') and rejected(pdrop('metric'), 'metric_removed') and rejected(pdrop('clock'), 'clock_removed')
          and rejected(lambda: validate_params(dict(PARAMS, weights='')), 'weights_emptied_without_reason'),
          parameters={k1: PARAMS[k1] for k1 in ('metric', 'weights', 'window', 'clock', 'node', 'N_min')})

    NAMING = {'uniqueness_of_ground_state_claimed': False, 'description': 'the limit of the named constructions (one state for F1 and F2)'}

    def validate_naming(nm, text):
        require(nm['uniqueness_of_ground_state_claimed'] is False, 'no uniqueness of any ground state')
        require('uniqueness' not in nm['description'], 'the limit is named as the limit of the named constructions')
        require(not affirmative(phrase_hits(text, FORBIDDEN, template)), 'affirmative definite phrasing in the report')
        return True
    check('named_construction_not_uniqueness',
          validate_naming(NAMING, report_text)
          and rejected(lambda: validate_naming(dict(NAMING, uniqueness_of_ground_state_claimed=True), report_text), 'uniqueness_flag_true')
          and rejected(lambda: validate_naming(dict(NAMING, description='uniqueness of every infinite-volume ground state'), report_text), 'limit_called_uniqueness')
          and rejected(lambda: validate_naming(NAMING, report_text + '\nThus omega_inf is the infinite-volume ground state.\n'), 'definite_phrase_appended'),
          naming=NAMING)

    PAIR = {'node': {'tau': tau, 'clock': 's=alpha*t_E/hbar'}, 'enclosure': {'tau': tau, 'clock': 's=alpha*t_E/hbar'},
            'finite_box': {'q': q, 'q_depends_on_tau': False}}

    def validate_pair(pk):
        require(pk['node']['tau'] == pk['enclosure']['tau'] == tau, 'same coupling for the node and the enclosure')
        require(pk['node']['clock'] == pk['enclosure']['clock'] == 's=alpha*t_E/hbar', 'common physical clock')
        require(pk['finite_box']['q'] == q and pk['finite_box']['q_depends_on_tau'] is False, 'the primary q=1/64 at the same coupling')
        return True
    check('common_clock',
          validate_pair(PAIR)
          and rejected(lambda: validate_pair(dict(PAIR, enclosure={'tau': tau / 10, 'clock': 's=alpha*t_E/hbar'})), 'enclosure_at_tau_over_10')
          and rejected(lambda: validate_pair(dict(PAIR, node={'tau': tau, 'clock': 'u=s/8'})), 'normalized_clock_for_one_statement')
          and rejected(lambda: validate_pair(dict(PAIR, finite_box={'q': 151552 * tau, 'q_depends_on_tau': True})), 'secondary_pair_q2'),
          pair={'tau': s(tau), 'clock': 's=alpha*t_E/hbar, theta=alpha*t/hbar', 'q': s(q)})

    TOP = {'states': 'trace norm on B(H_R)', 'observables': 'operator norm, ||W|| at most 1',
           'dynamics': 'norm on the compact window theta in [-8,8]', 'representations': 'GNS strong topology'}
    u = (Q(0), Q(1))    # the phase i: U e_j = i^j e_j, A e_j = e_{2j}

    def phase(j):
        z = (Q(1), Q(0))
        for _ in range(j):
            z = cmul(z, u)
        return z

    def diff_sq(j):     # ||(U A U* - A) e_j||^2 = |i^j - 1|^2
        z = phase(j)
        return (z[0] - 1) ** 2 + z[1] ** 2

    def validate_topology(tp, claim_norm_from_fixed_vector=False):
        require(tp['states'] == 'trace norm on B(H_R)' and tp['representations'] == 'GNS strong topology', 'state and representation topologies')
        require(tp['dynamics'] != tp['states'], 'two topologies named separately')
        require(not claim_norm_from_fixed_vector, 'a moving vector shows that strong convergence on a fixed vector is not norm convergence')
        return True
    check('topology_named',
          validate_topology(TOP) and diff_sq(0) == 0 and diff_sq(2) == 4
          and rejected(lambda: validate_topology(dict(TOP, states='weak-* on finite-rank observables')), 'weak_star_for_states')
          and rejected(lambda: validate_topology(dict(TOP, dynamics='trace norm on B(H_R)')), 'one_topology_for_both')
          and rejected(lambda: validate_topology(TOP, claim_norm_from_fixed_vector=True), 'norm_claim_from_fixed_vector'),
          topology=TOP, fixture={'U': 'e_j to i^j e_j', 'A': 'e_j to e_{2j}', 'fixed_vector_e0_difference_sq': s(diff_sq(0)), 'moving_vector_e2_difference_sq': s(diff_sq(2))})

    def validate_inheritance(steps):
        require(steps[0] == ('identify', 'BB2 items 2-3'), 'identification (BB2 items 2-3) first')
        require(steps[1][0] == 'inherit' and steps[1][1] in ('AV2 gate', 'AW2 gate'), 'then inheritance of the admitted certificate')
        require(identification['bb2_items_admitted'], 'the identification is admitted')
        return True
    STEPS = [('identify', 'BB2 items 2-3'), ('inherit', 'AV2 gate')]
    check('limit_identified_with_aq1_limits',
          validate_inheritance(STEPS) and validate_inheritance([STEPS[0], ('inherit', 'AW2 gate')])
          and rejected(lambda: validate_inheritance([('identify', "AV1/AY1 uniform local closeness 2D"), ('inherit', 'AV2 gate')]), 'restatement_from_uniform_local_closeness')
          and rejected(lambda: validate_inheritance([('identify', 'one AQ1 subsequence'), ('inherit', 'AV2 gate')]), 'restatement_from_a_subsequence')
          and rejected(lambda: validate_inheritance([STEPS[1], STEPS[0]]), 'inheritance_before_identification'),
          order=[list(x) for x in STEPS])

    RESTATED = {'d': d_g, 'R': R_g, 'lo': lo_g, 'hi': hi_g, 'L': L_g, 'U': U_g, 'K2': K2, 'mirror': mirror_g}

    def validate_restated(rs):
        require(rs['d'] == d_g and rs['R'] == R_g, 'restated datum or radius differs from the AV2 gate')
        require(rs['lo'] == lo_g and rs['hi'] == hi_g, 'restated interval differs from the AV2 gate')
        require(rs['K2'] == K2 and rs['L'] == L_g and rs['U'] == U_g and rs['mirror'] == mirror_g, 'restated enclosure differs from the AW2 gate')
        return True

    def rmut(**kw):
        r2 = dict(RESTATED)
        r2.update(kw)
        return lambda: validate_restated(r2)
    check('certificate_values_unchanged',
          validate_restated(RESTATED)
          and rejected(rmut(R=R_g + Q(1, 10 ** 40)), 'radius_rerounded_up')
          and rejected(rmut(R=r_fwd), 'smaller_forward_radius_restated')
          and rejected(rmut(d=d_g + Q(1, 10 ** 40)), 'datum_shifted')
          and rejected(rmut(lo=preview_value(dec(lo_g)), hi=preview_value(dec(hi_g))), 'interval_rounded_to_12_digits')
          and rejected(rmut(L=L_g + Q(1, Den)), 'aw2_endpoint_shifted')
          and rejected(rmut(K2=K_ceiling), 'K2_plus_replaced_by_outward_ceiling'),
          restated={k1: s(v1) if not isinstance(v1, tuple) else [s(x) for x in v1] for k1, v1 in RESTATED.items()})

    sstar_exact = pi_lo * (Q(1, 10 ** 6) - 2 * (D_av1 + D_av1 * D_av1)) / (49 * tau)

    def validate_nodes(nodes, grid=None):
        require(nodes == V['nodes'], 'only the preregistered node s=1')
        require(grid is None, 'no grid')
        return True
    check('post_hoc_node_rejected',
          validate_nodes([Q(1)]) and sstar_lo <= sstar_exact <= sstar_hi
          and rejected(lambda: validate_nodes([Q(2)]), 'node_s_2')
          and rejected(lambda: validate_nodes([sstar_exact]), 'crossover_s_star_as_node')
          and rejected(lambda: validate_nodes([Q(1)], grid=list(range(0, 129))), 'grid_0_to_128'),
          nodes=['1'], crossover_preview=dec(sstar_exact, 11), crossover_note='the analytic crossover of the radius formula, not a node')

    def validate_fbs(kind, C, qq, N_claimed):
        require(kind == FINITE_BOX['kind'], 'only the BB2 whole-sequence bound (sup over M, then M to infinity) reaches omega_inf')
        require(C == Cp, 'C must be the BB2 gate nested_telescoping bound value')
        require(qq == q, 'q=1/64 from the contract')
        require(N_claimed == least_N(C, qq, L_g), 'N_sign must be the least N at least 2 with C q^(N-1) strictly below L')
        return True
    K_ = FINITE_BOX['kind']
    check('finite_box_sign_from_whole_sequence',
          validate_fbs(K_, Cp, q, N_sign)
          and rejected(lambda: validate_fbs('bb1_per_comparison', C_bb1, q, least_N(C_bb1, q, L_g)), 'bb1_per_comparison_constant')
          and rejected(lambda: validate_fbs('n_to_n_plus_1_comparison', Cp, q, N_sign), 'n_to_n_plus_1_bound_alone')
          and rejected(lambda: validate_fbs('subsequence', Cp, q, N_sign), 'subsequence_bound')
          and rejected(lambda: validate_fbs(K_, Cp_union, q, least_N(Cp_union, q, L_g)), 'labelled_union_value')
          and rejected(lambda: validate_fbs(K_, Cp_reeval, q, least_N(Cp_reeval, q, L_g)), 'labelled_re_evaluated_value')
          and rejected(lambda: validate_fbs(K_, Cp, Q(1, 32), least_N(Cp, Q(1, 32), L_g)), 'q_one_over_32')
          and rejected(lambda: validate_fbs(K_, Cp, q, 3), 'N_sign_3')
          and rejected(lambda: validate_fbs(K_, Cp, q, 5), 'N_sign_5'),
          N_sign=N_sign, same_N_sign_with_labelled_values={'union': least_N(Cp_union, q, L_g), 're_evaluated': least_N(Cp_reeval, q, L_g)},
          rule='the labelled values give the same N_sign here, yet they are rejected: the contract fixes C as the bound value')

    MIRROR = {'confirmations': 1, 'minus_node': (d_g, R_g), 'minus_enclosure': mirror_g, 'minus_N_sign': N_sign, 'kind': 'replay of the same |tau| formula'}

    def validate_mirror(mr):
        require(mr['confirmations'] == 1, 'the minus sign is a replay, never a second confirmation')
        require(mr['minus_node'] == (d_g, R_g), 'the AV2 datum and radius depend on |tau| only')
        require(mr['minus_enclosure'] == (-U_g, -L_g), 'the minus-sign enclosure is the mirror')
        require(mr['minus_N_sign'] == least_N(Cp, q, -mr['minus_enclosure'][1]), 'mirrored N_sign')
        return True
    check('mirror_sign_replay_not_confirmation',
          validate_mirror(MIRROR)
          and rejected(lambda: validate_mirror(dict(MIRROR, confirmations=2)), 'minus_sign_counted_as_second_confirmation')
          and rejected(lambda: validate_mirror(dict(MIRROR, minus_enclosure=(L_g, U_g))), 'sign_blind_minus_enclosure'),
          mirror={'confirmations': 1, 'minus_enclosure': [s(mirror_g[0]), s(mirror_g[1])], 'minus_N_sign': N_sign})

    REF = {'correlation_shift_resolved': False, 'sub_label': 'reference_unresolved', 'reference_inside': lo_g <= ref_lo and ref_hi <= hi_g}

    def validate_reference(rf):
        require(rf['correlation_shift_resolved'] is False, 'no interaction shift of C(s)')
        require(rf['reference_inside'] is True and (lo_g <= ref_lo and ref_hi <= hi_g), 'the free value lies inside the restated interval')
        require(rf['sub_label'] == 'reference_unresolved', 'the sub-label reference_unresolved is kept')
        return True
    check('reference_unresolved_retained',
          validate_reference(REF)
          and rejected(lambda: validate_reference(dict(REF, correlation_shift_resolved=True)), 'correlation_shift_resolved_true')
          and rejected(lambda: validate_reference(dict(REF, sub_label='node_decides_the_reference')), 'node_reported_as_deciding_the_reference')
          and rejected(lambda: validate_reference(dict(REF, reference_inside=False)), 'free_value_claimed_outside'),
          reference='e^{-3}/4', reference_enclosure=[dec_down(ref_lo, 20), dec_up(ref_hi, 20)])

    RANGE_MARKERS = ('every `N` at least 2', 'every N at least 2', '`N` at least 2', 'N at least 2', '5<=N<=14000', 'N_sign')

    def rate_scan(text):
        prose = '\n'.join(ln for ln in text.splitlines() if not ln.lstrip().startswith('|'))
        bad = []
        for cl in clauses(norm(prose)):
            if 'O(1/N)' in cl or re.search(r'K5/N', cl):
                if '5<=N<=14000' not in cl and not NEGATION.search(cl):
                    bad.append(cl[:120])
            elif re.search(r'\brate\b', cl, re.I) and re.search(r'\bin `?N`?\b', cl):
                if not any(mk in cl for mk in RANGE_MARKERS) and not NEGATION.search(cl):
                    bad.append(cl[:120])
        return bad
    RATE_CLAIMS = [{'quantity': 'reduced densities (BB2 item 1) and the finite-box widening', 'rate': 'q^(N-1)', 'range': (2, None)},
                   {'quantity': 'correlation functions (BB2 item 5)', 'rate': 'K5/N', 'range': (5, N_rate_max)}]

    def validate_rates(claims, text):
        require(claims[0]['range'] == (V['N_min'], None), 'density rate for every N at least 2')
        require(claims[1]['range'] == (5, 14000) and N_rate_max == 14000, 'correlation rate only on 5<=N<=14000')
        require(not rate_scan(text), 'a rate in N stated without its range: ' + '; '.join(rate_scan(text))[:200])
        return True
    check('rate_range_stated',
          validate_rates(RATE_CLAIMS, report_text)
          and rejected(lambda: validate_rates(RATE_CLAIMS, report_text + '\nThe correlation functions converge at the rate O(1/N).\n'), 'unqualified_O_1_over_N')
          and rejected(lambda: validate_rates(RATE_CLAIMS, report_text + '\nThe densities converge at a rate in N.\n'), 'density_rate_without_range')
          and rejected(lambda: validate_rates([RATE_CLAIMS[0], dict(RATE_CLAIMS[1], range=(5, 14418))], report_text), 'correlation_range_extended_to_14418')
          and rejected(lambda: validate_rates([dict(RATE_CLAIMS[0], range=(5, None)), RATE_CLAIMS[1]], report_text), 'density_rate_restricted_to_N_at_least_5'),
          rate_claims=[{'quantity': x['quantity'], 'rate': x['rate'], 'range': [x['range'][0], x['range'][1]]} for x in RATE_CLAIMS])

    DECLARED_WRITES = [OWN_DIR + 'report.md', OWN_DIR + 'check.py', OWN_DIR + 'output/results.json', OWN_DIR + 'output/source-manifest.json', OWN_DIR + 'freeze.json']
    r32_bytes = {name: (BASE / 'inputs' / GATES[name][0]).read_bytes() for name in ROUND32_GATES}

    def validate_round32(byts, writes):
        for name in ROUND32_GATES:
            require(sha_bytes(byts[name]) == GATES[name][1] and cross[name], 'Round32 gate bytes differ from the pinned and cross-bound value: ' + name)
        require(all(w.startswith(OWN_DIR) for w in writes), 'a Round32 file is declared edited')
        return True
    av2_edit = json.loads(r32_bytes['AV2'].decode('utf-8'))
    av2_edit['restated_for_limit'] = 'omega_inf'
    bad_bytes = dict(r32_bytes, AV2=json.dumps(av2_edit, indent=1).encode('utf-8'))
    check('round32_gates_untouched',
          validate_round32(r32_bytes, DECLARED_WRITES)
          and rejected(lambda: validate_round32(bad_bytes, DECLARED_WRITES), 'restatement_written_into_the_AV2_gate')
          and rejected(lambda: validate_round32(r32_bytes, DECLARED_WRITES + ['research/round32/advisor/aw2-gate.json']), 'round32_file_declared_edited'),
          declared_writes=DECLARED_WRITES, round32_gates_bound_by=[cross[n] for n in ROUND32_GATES],
          note='the repository copies equal the snapshots (freeze.py check_snapshots); this is a new Round33 record citing the gates by hash')

    TARGETS = {'node': 'omega_inf of F1 and F2 (AQ_patterned_zero_selected)', 'enclosure': 'omega_inf of F1 and F2 (AQ_patterned_zero_selected)'}

    def validate_targets(tg, rows):
        for k1, v1 in tg.items():
            require(v1 == 'omega_inf of F1 and F2 (AQ_patterned_zero_selected)', 'restated only for the limit of the named constructions: ' + k1)
        require(not have_bc2_gate and all('bc2-gate' not in json.dumps(r1) for r1 in rows), 'no BC2 gate is cited before it is recorded')
        return True
    check('route_b_not_restated',
          validate_targets(TARGETS, obligations)
          and rejected(lambda: validate_targets(dict(TARGETS, node='uniform route-B limit (AX2)'), obligations), 'av2_restated_for_route_B')
          and rejected(lambda: validate_targets(dict(TARGETS, enclosure='uniform route-B limit (AX2)'), obligations), 'aw2_restated_for_route_B')
          and rejected(lambda: validate_targets(TARGETS, obligations + [{'candidate_route': 'research/round33/advisor/bc2-gate.json'}]), 'bc2_gate_cited_before_recorded'),
          targets=TARGETS, bc2_gate_in_inputs=have_bc2_gate)

    v_ph = (Q(3, 5), Q(4, 5))                        # rational phase, |v|^2 = 1
    ONE, ZERO = (Q(1), Q(0)), (Q(0), Q(0))

    def mm(A, B):
        return [[cadd(cmul(A[i][0], B[0][j]), cmul(A[i][1], B[1][j])) for j in range(2)] for i in range(2)]

    def dag(A):
        return [[cconj(A[j][i]) for j in range(2)] for i in range(2)]
    Uv = [[ONE, ZERO], [ZERO, v_ph]]
    Ax = [[ZERO, ONE], [ONE, ZERO]]

    def evolve(B):     # T(B) = U* B U
        return mm(mm(dag(Uv), B), Uv)

    def corr(state):   # omega_state(A* T(A)), A = sigma_x self-adjoint
        return mm(dag(Ax), evolve(Ax))[state][state]
    Bgen = [[(Q(2), Q(1)), (Q(-3), Q(5))], [(Q(7), Q(-2)), (Q(1, 3), Q(0))]]
    invariant = all(evolve(Bgen)[k][k] == Bgen[k][k] for k in range(2))
    fixture_ok = v_ph[0] ** 2 + v_ph[1] ** 2 == 1 and invariant and corr(0) == cconj(v_ph) and corr(1) == v_ph and corr(0) != corr(1)
    check('same_state_not_different_states',
          validate_gns(GNS) and fixture_ok
          and rejected(lambda: validate_gns(dict(GNS, gns_dynamics_equality_claimed=True)), 'gns_dynamics_equality_true')
          and rejected(lambda: validate_gns(dict(GNS, basis=None)), 'common_gns_item_without_the_bb2_identification')
          and rejected(lambda: validate_gns(dict(GNS, states=2, triple='equality of GNS dynamics of different states')), 'phrased_as_different_states'),
          fixture={'dynamics': 'T(A)=U* A U, U=diag(1,v), v=(3+4i)/5', 'A': 'sigma_x', 'correlation_state_e0': [s(corr(0)[0]), s(corr(0)[1])],
                   'correlation_state_e1': [s(corr(1)[0]), s(corr(1)[1])], 'meaning': 'one algebraic dynamics, two invariant states, two different GNS dynamics'})

    def validate_enclosure(lo, hi, N):
        w = widen(N) if N else Q(0)
        require(lo == tau / 144 - Kt2 - w, 'lower endpoint must keep K_2^+ tau^2 and the widening')
        require(hi == tau / 144 + Kt2 + w, 'upper endpoint must keep K_2^+ tau^2 and the widening')
        return True
    check('second_order_remainder_kept',
          validate_enclosure(L_g, U_g, None) and validate_enclosure(lo4, hi4, N_sign)
          and rejected(lambda: validate_enclosure(tau / 144 - widen(N_sign), hi4, N_sign), 'K2_plus_dropped_at_lower_end')
          and rejected(lambda: validate_enclosure(tau / 144 - Kt2 / 2, tau / 144 + Kt2 / 2, None), 'K2_plus_halved')
          and rejected(lambda: validate_enclosure(lo4, U_g, N_sign), 'widening_on_one_side_only'),
          remainder=s(Kt2), widening_at_N_sign=s(widen(N_sign)))

    NODE_CLAIMS = {'finite_box_node_claimed': False, 'restated_nodes': [{'state': 'omega_inf', 'provenance': 'AV2 gate via BB2 items 2-3', 'R': R_g}]}

    def validate_node_claims(nc):
        require(nc['finite_box_node_claimed'] is False, 'no finite-box node is claimed')
        require(all(RECORD.values()), 'the record facts hold')
        for rn in nc['restated_nodes']:
            require(rn['state'] == 'omega_inf' and rn['provenance'] == 'AV2 gate via BB2 items 2-3', 'only the limit state is restated')
            require(rn['R'] == R_g, 'no AV2 constant re-derived or retuned')
        return True
    radius_Dhalf = 2 * (D_av1 / 2 + D_av1 * D_av1) + kF + arith_half
    check('finite_box_node_only_from_record',
          validate_node_claims(NODE_CLAIMS)
          and rejected(lambda: validate_node_claims({'finite_box_node_claimed': False, 'restated_nodes': NODE_CLAIMS['restated_nodes'] + [{'state': 'F1 box N=4', 'provenance': 'restatement', 'R': R_g}]}), 'finite_box_node_presented_as_restatement')
          and rejected(lambda: validate_node_claims({'finite_box_node_claimed': False, 'restated_nodes': [{'state': 'F2 box N=4', 'provenance': 'window lemma applied box by box', 'R': R_g}]}), 'window_lemma_box_by_box')
          and rejected(lambda: validate_node_claims({'finite_box_node_claimed': False, 'restated_nodes': [{'state': 'omega_inf', 'provenance': 'AV2 gate via BB2 items 2-3', 'R': radius_Dhalf}]}), 'state_term_retuned_to_D_over_2')
          and rejected(lambda: validate_node_claims(dict(NODE_CLAIMS, finite_box_node_claimed=True)), 'finite_box_node_claimed_true'),
          radius_with_retuned_state_term_preview=dec(radius_Dhalf), open_rows=['N2', 'N3'])

    # ======================= contract wording notes, map, report values =======================
    notes = []
    if 'were stated for each AQ1 subsequential state separately' in V['selection_reason'] and 'and in every centered whole-star box N>=2 at every on-site cutoff' in aw2a:
        notes.append({'id': 'W1', 'field': 'selection_reason', 'note': 'AW2 was also stated in every centered whole-star box at every on-site cutoff (the F1 boxes), not only for each AQ1 subsequential state'})
    if V['claim_exclusions'][2] != V['prereg_exclusions'][2] and V['prereg_exclusions'][2] == 'an interaction shift of C(s)':
        notes.append({'id': 'W2', 'field': 'claim_exclusions versus preregistration.claim_exclusions', 'note': 'the two lists differ in one entry; the wider contract entry is applied'})
    if 'd_X' not in V['params']:
        notes.append({'id': 'W3', 'field': 'parameters', 'note': 'no d_X field; no decay estimate is derived; the inherited bounds carry their metric; N_min plays the role of N_0'})
    if nr[1] == 'the finite-box Euclidean node for F2 boxes and for finite F1 boxes (item 4)' and 'Record two open obligation rows' in V['required'][3]:
        notes.append({'id': 'W4', 'field': 'parameters.obligations', 'note': 'one entry for two rows; the table carries N2 and N3'})
    if 'every padded box Lambda_N with N at least the exactly computed N_sign has a static Wilson mean of certified sign' in template:
        notes.append({'id': 'W5', 'field': 'mandatory_sentence_template', 'note': 'the state is implicit; the scope is the untruncated F2 ground vector at fixed N (finite_box_sign_scope); cutoff-L F2 states are not claimed'})
    premise_obs = [{'id': 'P1', 'source': P_BB2F + ' section 9', 'note': 'harmonic fixture: first exceedance of 4 is N=83, not N=119 (fixture wording only)', 'exact_first_N': n_h}]
    check('contract_wording_defects_recorded', len(notes) == 5 and n_h == 83, notes=notes, premise_observations=premise_obs, blocking=False)

    def map_rows(text):
        sec = text.split('## 15. ', 1)
        require(len(sec) == 2, 'map section 15 missing')
        return [ln for ln in sec[1].split('\n## 16. ', 1)[0].splitlines() if ln.startswith('| ')]

    def validate_map(rows):
        missing_ids = [cid for cid in V['controls'] if not any(r1.startswith('| `' + cid + '` |') for r1 in rows)]
        missing_items = [k for k in range(1, 8) if not any(r1.startswith('| item %d ' % k) for r1 in rows)]
        require(not missing_ids and not missing_items, 'map lacks rows for ' + ','.join(missing_ids + ['item %d' % k for k in missing_items]))
        ids_in_code = {ch['id'] for ch in CHECKS} | set(V['controls']) | {'report_item_and_control_map'}
        cited = set(re.findall(r'`([a-z0-9_]+)`', '\n'.join(r1.split(' | ')[-1] for r1 in rows)))
        require(cited <= ids_in_code | {'check.py'}, 'map cites an unknown check id: ' + ','.join(sorted(cited - ids_in_code)))
        return True
    mrows = map_rows(report_text)
    EXACT_IN_REPORT = [s(d_g), s(R_g), s(lo_g), s(hi_g), s(K2), s(Kt2), s(L_g), s(U_g), s(lo4), s(hi4), s(widen(N_sign)), s(D_av1), s(excl_g), s(Cp)]
    PREVIEWS_IN_REPORT = ([dec(x) for x in (d_g, R_g, lo_g, hi_g, D_av1, K2, Kt2)] + [dec(widen(N)) for N in range(2, 7)]
                          + [dec(L_g - widen(N)) for N in range(2, 7)] + [dec_down(lo4), dec_up(hi4)] + list(aw2_prev))
    missing_previews = [x for x in PREVIEWS_IN_REPORT if not re.search(r'(?<![\d.])' + re.escape(x) + r'(?![\d])', report_text)]
    require(not missing_previews, 'report previews differ from the exact truncations: ' + ','.join(missing_previews))
    stray_previews = sorted(set(re.findall(r'(?<![\d.])-?\d\.\d{11}e-?\d+', report_text)) - set(PREVIEWS_IN_REPORT))
    require(not stray_previews, 'a 12-digit preview in the report is not an exact truncation or a quoted gate decimal: ' + ','.join(stray_previews))
    ctl_table = report_text.split('## 11. ', 1)[1].split('\n## 12. ', 1)[0]
    outside = report_text.replace(ctl_table, '')
    n_sign_claims = [int(x) for cl in clauses(norm(outside)) if 'rejected' not in cl for x in re.findall(r'N_sign ?= ?(\d+)', cl)]
    require(n_sign_claims and all(x == N_sign for x in n_sign_claims), 'the report states an N_sign other than the computed value')
    check('report_item_and_control_map',
          validate_map(mrows) and all(x in report_text for x in EXACT_IN_REPORT) and '**`N_sign = 4`**' in report_text
          and rejected(lambda: validate_map([r1 for r1 in mrows if not r1.startswith('| `rate_range_stated` |')]), 'control_row_removed_from_map')
          and rejected(lambda: validate_map([r1 for r1 in mrows if not r1.startswith('| item 4 ')]), 'item_4_row_removed_from_map'),
          controls_in_map=len(V['controls']), items_in_map=7, exact_values_in_report=len(EXACT_IN_REPORT), previews_in_report=len(PREVIEWS_IN_REPORT),
          n_sign_statements_in_report=len(n_sign_claims))

    # ======================= packet and coherent tampering =======================
    headline = {
        'av2_node': {'d': s(d_g), 'd_preview': dec(d_g), 'R': s(R_g), 'R_preview': dec(R_g), 'interval': [s(lo_g), s(hi_g)],
                     'interval_preview': [dec(lo_g), dec(hi_g)], 'node_s': '1', 'minus_tau': 'replay of the same |tau| formula',
                     'reference': 'e^{-3}/4 inside (reference_unresolved)'},
        'aw2_enclosure': {'K2_plus': s(K2), 'K2_plus_preview': dec(K2), 'plus': [s(L_g), s(U_g)], 'plus_gate_outward': list(aw2_prev),
                          'minus': [s(mirror_g[0]), s(mirror_g[1])], 'minus_tau': 'mirror replay', 'exclusion_margin_preview': dec(excl_g, 8),
                          'sign_margin_preview': dec(signm_g, 8)},
        'finite_box_sign': {'C_prime': s(Cp), 'q': s(q), 'N_sign': N_sign, 'widening_at_N_sign': s(widen(N_sign)),
                            'widened_plus_at_N_sign': [s(lo4), s(hi4)], 'widened_plus_directed': [dec_down(lo4), dec_up(hi4)],
                            'widened_minus_at_N_sign': [s(-hi4), s(-lo4)], 'rate_in_N': 'q^(N-1) for every N at least 2',
                            'F1_boxes': 'certified by AW2 at every N at least 2', 'open_F2_boxes': [2, 3]},
        'common_gns': GNS,
    }
    sentence_block = {'template_verbatim': template, 'N_sign': N_sign}
    packet = {
        'loop': 'BC1', 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'contribution_alias': 'HNM-BC1-F forward statement: the AV2 node and AW2 sign certificates restated for the limit of the named constructions, the F2 finite-box sign corollary with N_sign, the finite-box node record, the common GNS item and the updated obligations table',
        'ai_assistance': 'AI-assisted forward production (a Claude model agent); correlated model-agent work, not independent human review',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'gate_sha256': {k1: v1[1] for k1, v1 in GATES.items()},
        'model': {'model_id': V['model_id'], 'statement': V['model'], 'families': list(FAMS), 'cover': 'R={0,e_z}', 'tau': s(tau), 'signs': ['+', '-'],
                  'clock': 's=alpha*t_E/hbar, theta=alpha*t/hbar, G=H/alpha', 'node': 's=1'},
        'headline': headline, 'label': LABEL, 'gate_fields': GATE_FIELDS, 'obligations_table': obligations,
        'round32_limitations': lim_rows, 'falsifying_scenario': FALSIFIER, 'error_terms_itemized': ledger, 'mandatory_sentence': sentence_block,
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions'],
                       'additional': ['no finite-box node for F1 or F2 boxes', 'no F2 finite-box sign for N=2,3', 'no cutoff-L F2 state',
                                      'nothing below the cap', 'no node other than s=1', 'no correlation rate outside 5<=N<=14000']},
        'contract_wording_notes': notes, 'premise_observations': premise_obs,
        'routes_executed': ['forward: restatement from the hash-pinned AV2/AW2 gates through the BB2 identification (exact equality)',
                            'forward: F2 finite-box corollary from the BB2 item-1 bound value and the AW2 endpoints (exact N_sign)',
                            'forward: finite-box node record facts verified in the AV2/AW1 snapshots',
                            'forward: common GNS item and obligations table'],
        'routes_not_executed': ['skeptic replay from the contract and the gates (outside this producer)'],
        'controls_deferred': {},
        'proposed_forward_verdict': verdict + ' (forward half of a statement+skeptic loop; admission requires the skeptic replay); sub-labels certificate_restated_for_limit, reference_unresolved, static_not_dynamic; N_sign=4',
    }
    for k1, v1 in GATE_FIELDS.items():
        packet[k1] = v1

    def packet_hash(pk):
        body = {k1: v1 for k1, v1 in pk.items() if k1 != 'packet_sha256'}
        return sha_bytes(json.dumps(body, sort_keys=True, default=str).encode('utf-8'))

    def validate_packet(pk, inv):
        require(pk.get('packet_sha256') == packet_hash(pk), 'packet hash mismatch')
        ids = {ch['id']: ch for ch in pk['checks']}
        for cid in V['controls']:
            if cid == 'coherent_evidence_tampering':
                continue
            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)
        require(sorted(inv) == sorted(set(expected_inputs)), 'premise snapshot inventory incomplete')
        for name, (rel, pin) in GATES.items():
            require(inv.get(rel) == pin and pk['gate_sha256'][name] == pin, 'gate hash changed: ' + name)
        hd = pk['headline']
        require(rat(hd['av2_node']['R']) == R_g and rat(hd['av2_node']['d']) == d_g, 'AV2 values differ from the gate')
        require([rat(x) for x in hd['aw2_enclosure']['plus']] == [L_g, U_g] and [rat(x) for x in hd['aw2_enclosure']['minus']] == [-U_g, -L_g], 'AW2 values differ')
        fb = hd['finite_box_sign']
        require(rat(fb['C_prime']) == Cp and rat(fb['q']) == q and fb['N_sign'] == least_N(rat(fb['C_prime']), rat(fb['q']), L_g), 'finite-box constants')
        w = widen(fb['N_sign'], rat(fb['C_prime']), rat(fb['q']))
        require([rat(x) for x in fb['widened_plus_at_N_sign']] == [L_g - w, U_g + w], 'widened enclosure differs from recomputation')
        require([rat(x) for x in fb['widened_minus_at_N_sign']] == [-(U_g + w), -(L_g - w)], 'widened mirror differs')
        validate_obligations(pk['obligations_table'])
        validate_gate_fields(pk['gate_fields'])
        for k1, v1 in GATE_FIELDS.items():
            require(pk[k1] == v1 and type(pk[k1]) is type(v1), 'top-level gate field differs: ' + k1)
        require(pk['proposed_forward_verdict'].startswith(forward_verdict(True, True, True, True, True, False)), 'verdict changed')
        return True

    base_packet = json.loads(json.dumps(dict(packet, checks=[dict(ch) for ch in CHECKS]), default=str))
    base_packet['packet_sha256'] = packet_hash(base_packet)

    def tamper(fn, drop=None):
        def run():
            pk = json.loads(json.dumps(base_packet))
            inv = dict(inventory)
            fn(pk, inv)
            pk['packet_sha256'] = packet_hash(pk)
            return validate_packet(pk, inv)
        return run

    def t_control(pk, inv):
        for ch in pk['checks']:
            if ch['id'] == 'finite_box_sign_from_whole_sequence':
                ch['passed'] = False

    def t_R(pk, inv):
        pk['headline']['av2_node']['R'] = s(R_g + Q(1, 10 ** 40))

    def t_Nsign(pk, inv):
        pk['headline']['finite_box_sign']['N_sign'] = 3

    def t_Cunion(pk, inv):
        pk['headline']['finite_box_sign']['C_prime'] = s(Cp_union)

    def t_row(pk, inv):
        pk['obligations_table'] = pk['obligations_table'][:-1]

    def t_node(pk, inv):
        pk['finite_box_node_claimed'] = True

    def t_gate(pk, inv):
        inv[GATES['BB2'][0]] = '0' * 64
        pk['gate_sha256']['BB2'] = '0' * 64

    def t_snapshot(pk, inv):
        inv.pop(GATES['AV2'][0])

    def t_lower(pk, inv):
        pk['headline']['finite_box_sign']['widened_plus_at_N_sign'][0] = s(lo4 + Q(1, 10 ** 30))

    def t_minus(pk, inv):
        pk['headline']['aw2_enclosure']['minus'][0] = s(-L_g)
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_R), 'R_rerounded_hash_rebound')
          and rejected(tamper(t_Nsign), 'N_sign_lowered_to_3_hash_rebound')
          and rejected(tamper(t_Cunion), 'C_replaced_by_labelled_union_value_hash_rebound')
          and rejected(tamper(t_row), 'obligation_row_removed_hash_rebound')
          and rejected(tamper(t_node), 'finite_box_node_claimed_true_hash_rebound')
          and rejected(tamper(t_gate), 'bb2_gate_hash_replaced_hash_rebound')
          and rejected(tamper(t_snapshot), 'av2_gate_snapshot_removed_hash_rebound')
          and rejected(tamper(t_lower), 'widened_lower_end_raised_hash_rebound')
          and rejected(tamper(t_minus), 'minus_sign_endpoint_changed_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    positive_only = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch.get('rejected_mutations')]
    require(not positive_only, 'contract controls without a damaging mutation: ' + ','.join(positive_only))
    require(not PENDING, 'rejected mutations not attached to a check')
    out = json.loads(json.dumps(packet, default=str))
    out['checks'] = CHECKS
    out['contract_controls_covered'] = sorted(V['controls'])
    out['controls_with_damaging_mutations'] = sum(1 for ch in CHECKS if ch['id'] in V['controls'] and ch.get('rejected_mutations'))
    out['rejected_mutations_in_control_checks'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS if ch['id'] in V['controls'])
    out['rejected_mutation_total'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS)
    out['check_count'] = len(CHECKS)
    out['direction'] = 'forward'
    out['loop'] = 'BC1'
    exported = '\n'.join(x for x in strings_of(out) if isinstance(x, str))
    require(not affirmative(phrase_hits(exported, FORBIDDEN, template)), 'forbidden phrasing in exported strings')
    return out


def float_free(obj):
    if isinstance(obj, float):
        return False
    if isinstance(obj, dict):
        return all(float_free(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(float_free(v) for v in obj)
    return True


def main():
    ap = argparse.ArgumentParser(description='BC1 forward exact checker')
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
    manifest = {'loop': 'BC1', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'BC1', 'direction': 'forward', 'checks': result['check_count'], 'N_sign': result['headline']['finite_box_sign']['N_sign'],
                      'controls_with_damaging_mutations': result['controls_with_damaging_mutations'],
                      'rejected_in_controls': result['rejected_mutations_in_control_checks'], 'rejected_total': result['rejected_mutation_total'],
                      'verdict': result['proposed_forward_verdict'][:22]}, sort_keys=True))


if __name__ == '__main__':
    main()
