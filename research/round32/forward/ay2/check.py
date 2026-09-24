#!/usr/bin/env python3
"""AY2 forward producer (single producer of a statement+skeptic loop): exact checks for the
Hruday statement on state identification -- what the AY1 closeness lemma does and does not
establish -- and for the two-sided first-order distance tier `first_order_distance_from_product`.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production (a Claude model agent).

Standard library only (argparse, fractions, hashlib, json, math, pathlib, re).  Every admission
Boolean is decided in exact Fraction arithmetic; decimal strings are truncated previews.  Conditions
raise AdmissionError explicitly (never `assert`), so every check stays active under `python -O`.
Every admitted constant is read from the sha256-bound snapshots in inputs/ (the frozen AY2 contract
and the AY1 gate) and recomputed from the gate's own itemization; none is typed in.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round32/contracts/ay2.json'
CONTRACT_SHA256 = '8e55e8e9d54b26520ab0fa10c1c6a967a616aabb4dc8c47988ff687d14d96b38'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'

P_AY1_GATE = 'research/round32/advisor/ay1-gate.json'
P_AM2_GATE = 'research/round29/advisor/am2-gate.json'
P_AY1F = 'research/round32/forward/ay1/report.md'
P_AY1R = 'research/round32/reverse/ay1/report.md'
P_AY1S = 'research/round32/skeptic/ay1.md'
P_SEL = 'research/round32/advisor/selection-ay2.md'
P_I1 = 'research/round21/forward/i1/report.md'
P_AQ1 = 'research/round29/forward/aq1/report.md'
P_AT4 = 'research/round31/forward/at4/report.md'


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


def preview_value(text):
    """Parse a decimal preview string from a premise into an exact Fraction (comparison only, never admission)."""
    require(re.fullmatch(r'-?\d+(\.\d+)?(e-?\d+)?', text) is not None, 'malformed preview ' + text)
    mant, _, ex = text.partition('e')
    return Q(mant) * Q(10) ** int(ex or '0')


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


SQRT_SCALE = 10 ** 30


def sqrt_bracket(n, scale=SQRT_SCALE):
    """Directed rational bracket lo <= sqrt(n) <= hi of a nonnegative rational, from integer square roots."""
    n = rat(n)
    require(n >= 0, 'square root of a negative number')
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k + 1, scale) ** 2 <= n:
        k += 1
    while Q(k, scale) ** 2 > n:
        k -= 1
    lo = Q(k, scale)
    hi = lo if lo * lo == n else Q(k + 1, scale)
    require(lo * lo <= n <= hi * hi and hi - lo <= Q(1, scale), 'directed square-root bracket')
    return lo, hi


def read_input(rel):
    return (BASE / 'inputs' / rel).read_text(encoding='utf-8')


def load_json_input(rel):
    return json.loads(read_input(rel))


def match(pattern, text, label, flags=0):
    m = re.search(pattern, text, flags)
    require(m is not None, 'premise text not parsed: ' + label)
    return m


def frac_of(m, i):
    return Q(int(m.group(i)), int(m.group(i + 1)))


# ---------------------------------------------------------------------------
# Contract: every target, control id, obligation name and reference is read from the sha256-bound snapshot.
# ---------------------------------------------------------------------------
def load_contract():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen AY2 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AY2' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


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


def contract_values(c):
    pre = c['preregistration']
    v = {}
    v['model'] = c['model']
    require('|tau|<=10^-8' in v['model'] and 'R={0,e_z}' in v['model'] and 'zero-selected patterned family' in v['model'], 'model string')
    v['tau_cap'] = rat(pre['tau']['value'])
    require(v['tau_cap'] == Q(1, 10 ** 8), 'preregistered tau')
    v['signs'] = list(pre['tau']['signs_evaluated'])
    require(v['signs'] == ['+', '-'], 'both signs required')
    require(pre['tau']['is_model_change_vs_previous_loop'] is False and pre['tau']['rule_if_chosen_later'] is None, 'tau rule')
    v['triple'] = [rat(x) for x in pre['selected_triple_alpha_units']]
    require(v['triple'] == [0, 0, 0], 'zero selected triple')
    v['model_id'] = pre['model_id']
    require(v['model_id'] == 'AQ_patterned_zero_selected', 'model id')
    v['state_provenance'] = pre['state_provenance']
    require('AQ1' in v['state_provenance'] and 'I1' in v['state_provenance'], 'state provenance names both families')
    obs = pre['observable']
    v['observable_id'] = obs['id']
    v['centering'] = obs['centering']
    v['reference_value'] = obs['reference_value_exact']
    v['reference_route'] = obs['reference_route']
    require(v['centering'] == 'none' and v['reference_value'] == 'P_R' and v['reference_route'] == 'haar', 'observable block')
    v['clock'] = pre['clock']
    m = match(r'^(s=alpha\*t_E/hbar, theta=alpha\*t/hbar); u=s/(\d+) and exponent (\d+) forbidden in packets$', v['clock'], 'clock')
    v['clock_common'], v['forbidden_u_div'], v['forbidden_exponent'] = m.group(1), int(m.group(2)), int(m.group(3))
    tg = pre['target']
    v['target'] = rat(tg['value'])
    v['target_quantity'] = tg['quantity']
    require(tg['comparator'] == '<=' and 'two-sided tier width relative to its centre' in tg['quantity'], 'target comparator/quantity')
    v['error_terms'] = list(pre['error_terms_itemized'])
    require(len(v['error_terms']) == 3, 'three preregistered error terms')
    v['error_terms_rule'] = pre['error_terms_rule']
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['outcomes'] = list(pre['expected_outcome_types'])
    v['gate_fields'] = dict(pre['gate_fields_required'])
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']) and len(v['controls']) == 21, 'controls list equals the preregistered ids')
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['acceptance'] = dict(c['acceptance'])
    v['shared'] = list(c['shared_premises'])
    v['required'] = list(c['required'])
    require(len(v['required']) == 6, 'six required items')
    v['hash_binding'] = dict(pre['hash_binding'])
    require(all(v['hash_binding'].get(k) is True for k in ('contract_sha256_in_producer_inputs', 'check_py_reads_target_and_reference_from_contract',
                                                          'check_py_sha256_recorded_before_full_size_evaluation')), 'hash binding')
    require(c['direction'] == 'statement+skeptic' and pre['direction'] == 'statement+skeptic' and c['producers'] == ['forward'], 'direction')
    require(c.get('single_direction_independent_replay') is True, 'single-direction independent replay declared')
    v['tier_param'] = c['parameters']['first_order_distance_tier']
    require('first_order_distance_from_product' in v['tier_param'] and 'never as an interaction-shift or dynamical claim' in v['tier_param'], 'tier parameter')
    v['constants_from_ay1'] = dict(c['parameters']['constants_from_ay1'])
    require(sorted(v['constants_from_ay1']) == ['D', 'K2_prime', 'rho1_R', 'second_order_difference', 'two_D'], 'constants_from_ay1 keys')
    # the six obligations, read from required item 2 (parenthesis-aware split)
    item2 = v['required'][1]
    tail = item2.split('with the missing premise and a candidate route: ', 1)
    require(len(tail) == 2, 'item 2 parsed')
    pieces = split_top_level(tail[1].rstrip('.'))
    names, hints = [], []
    for p in pieces:
        m = re.match(r'^([^()]+?)(?: \((.*)\))?$', p)
        require(m is not None, 'obligation parsed: ' + p)
        names.append(m.group(1).strip())
        hints.append(m.group(2) or '')
    require(len(names) == 6, 'six obligations in item 2')
    v['obligation_names'] = names
    v['obligation_hints'] = hints
    v['selected_after'] = c.get('selected_after')
    v['selection_reason'] = c.get('selection_reason', '')
    v['nodes'] = pre['nodes']
    require(pre['nodes']['s_values'] == [] and pre['nodes']['post_hoc_node_selection'] == 'forbidden', 'no Euclidean nodes (static loop)')
    return v


# ---------------------------------------------------------------------------
# Fine-lattice geometry and the I1 anchored face table (parsed from the I1 snapshot).
# ---------------------------------------------------------------------------
E_UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIENT = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
TOKEN = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}


def vadd(p, q):
    return tuple(x + y for x, y in zip(p, q))


def vsub(p, q):
    return tuple(x - y for x, y in zip(p, q))


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    return ((p, a), (vadd(p, E_UNIT[a]), c), (vadd(p, E_UNIT[c]), a), (p, c))


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


def face_base(anchor, cls):
    return (4 * anchor[0] + cls[1], 2 * anchor[1] + cls[2], anchor[2]), ORIENT[cls[0]]


def face_linkset(face):
    base, (a, c) = face_base(*face)
    return frozenset(face_links(base, a, c))


def face_owner_set(face):
    return frozenset(owner(link[0]) for link in face_linkset(face))


def label_of(face):
    b, cls = face
    return '%s r=%d s=%d anchored at (%d,%d,%d)' % (cls[0], cls[1], cls[2], b[0], b[1], b[2])


def faces_meeting(region, omitted, anchors):
    out = []
    for b in anchors:
        for cls in omitted:
            f = (b, cls)
            if face_owner_set(f) & region:
                out.append(f)
    return out


def factor_links(b):
    return [((4 * b[0] + r, 2 * b[1] + q, b[2]), d) for r in range(4) for q in range(2) for d in range(3)]


# ---------------------------------------------------------------------------
# Exact SU(2) Haar moments of W=(1/2)Tr U: two routes (Clebsch-Gordan count; Weyl/Wallis).
# ---------------------------------------------------------------------------
def spin_half_invariants(n):
    dist = {0: 1}
    for _ in range(n):
        new = {}
        for j2, mult in dist.items():
            for j2n in (j2 - 1, j2 + 1):
                if j2n >= 0:
                    new[j2n] = new.get(j2n, 0) + mult
        dist = new
    return dist.get(0, 0)


def haar_W_moment(n):
    return Q(spin_half_invariants(n), 2 ** n)


def weyl_W_moment(n):
    """E[cos^n theta] for the SU(2) Weyl density (2/pi) sin^2 theta on [0,pi]: 2[w(n)-w(n+2)], w(m)=(1/pi)int cos^m."""
    if n % 2:
        return Q(0)

    def wallis(m2):
        num, den = 1, 1
        for k in range(1, m2 + 1):
            if k % 2:
                num *= k
            else:
                den *= k
        return Q(num, den)
    return 2 * (wallis(n) - wallis(n + 2))


def odd_link_vanishes(linksets):
    """Centre (Z2) grading: a Haar product of spin-1/2 plaquette traces vanishes if some link occurs an odd number of times."""
    count = {}
    for ls in linksets:
        for link in ls:
            count[link] = count.get(link, 0) + 1
    return any(k % 2 for k in count.values())


def haar_product(faces_list, EW2):
    """Exact Haar expectation of a product of one, two or three plaquette traces with 4 distinct links each."""
    lsets = [face_linkset(f) for f in faces_list]
    require(all(len(ls) == 4 for ls in lsets), 'every plaquette has four distinct links')
    if odd_link_vanishes(lsets):
        return Q(0)
    require(len(faces_list) == 2 and lsets[0] == lsets[1], 'only the diagonal pair survives the parity rule here')
    return EW2   # the holonomy of four distinct Haar links is Haar distributed


# ---------------------------------------------------------------------------
# Small exact real-symmetric matrix algebra on the span {Omega_R, e_f} (e_f = 2 W_f Omega_R).
# ---------------------------------------------------------------------------
def outer(x, y):
    return [[xi * yj for yj in y] for xi in x]


def sym_outer(x, y):
    """|x><y| + |y><x| (real coordinates)."""
    return [[x[i] * y[j] + y[i] * x[j] for j in range(len(y))] for i in range(len(x))]


def madd(*mats):
    n = len(mats[0])
    return [[sum((M[i][j] for M in mats), Q(0)) for j in range(n)] for i in range(n)]


def mscale(A, c):
    return [[c * x for x in row] for row in A]


def mmul(A, B):
    n = len(A)
    return [[sum((A[i][k] * B[k][j] for k in range(n) if A[i][k]), Q(0)) for j in range(n)] for i in range(n)]


def mtrace(A):
    return sum((A[i][i] for i in range(len(A))), Q(0))


def meq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A)))


def mzero(A):
    return all(x == 0 for row in A for x in row)


def symmetric(A):
    return all(A[i][j] == A[j][i] for i in range(len(A)) for j in range(len(A)))


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def rank_two_c2(A):
    """For real symmetric A with A^3 = c^2 A, Tr A = 0 and Tr A^2 = 2c^2 > 0, the spectrum is {+c, -c, 0,...,0}
    with +c and -c simple, so ||A||_1 = 2c.  Returns c^2 exactly."""
    require(symmetric(A), 'not symmetric')
    require(mtrace(A) == 0, 'not traceless')
    A2 = mmul(A, A)
    c2 = mtrace(A2) / 2
    require(c2 > 0, 'zero operator')
    require(meq(mmul(A, A2), mscale(A, c2)), 'cube identity A^3 = (Tr A^2/2) A fails')
    return c2


def trace_norm_upper_rank_two(A):
    c2 = rank_two_c2(A)
    return 2 * sqrt_bracket(c2)[1]


# ---------------------------------------------------------------------------
# AY1 gate itemization (read from the gate text) and its exact recomputation.
# ---------------------------------------------------------------------------
def ay1_items(tau, F, pins, am2_factor=None, remainder='admitted', density_eps='R'):
    """R-local trace-norm remainder items of the AY1 gate: 4rho+2T(72a+2rho)+2(33a+rho)^2+2eps_R^2+20a eps_R^2."""
    a = abs(tau) / F['a_den']
    J = F['J_per_tau'] * abs(tau)
    require(F['GpR'] * J < 1, 'self-consistent remainder needs 352J<1')
    T = F['T_num'] * a / (1 - F['GpR'] * J)
    r_am2 = F['GpR'] * J * T
    if remainder == 'admitted':
        rr = r_am2
    elif remainder == '288':
        rr = 288 * J * T / (1 - 8 * T)
    else:
        raise AdmissionError('unknown remainder form')
    epsR = pins['meet'] * a + F['epsR_rho'] * rr + (pins['single'] * a + rr) ** 2
    eps_adm = 2 * T + T * T
    e_use = epsR if density_eps == 'R' else eps_adm
    am2 = (F['c_am2'] * rr) if am2_factor is None else am2_factor * rr
    items = {
        'am2_remainder': am2,
        'straddling': F['c_str'] * T * (pins['straddling'] * a + F['str_rho'] * rr),
        'two_creation': F['c_two'] * (pins['single'] * a + rr) ** 2,
        'density': F['c_den'] * e_use ** 2,
        'normalization_third_order': F['c_norm'] * a * e_use ** 2,
    }
    require(all(isinstance(x, Q) and x >= 0 for x in items.values()), 'items exact and nonnegative')
    total = sum(items.values(), Q(0))
    return {'items': items, 'total': total, 'a': a, 'J': J, 'T': T, 'r_am2': r_am2, 'epsR': epsR, 'eps': eps_adm}


def D_from(T):
    eps = 2 * T + T * T
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def K2plus_from(it):
    T, r_am2, a = it['T'], it['r_am2'], it['a']
    eps = 2 * T + T * T
    return r_am2 + T * T + T * T + eps * eps + a * eps * eps


def forward_verdict(tier_certified, rows_complete, constants_exact, overclaim):
    if overclaim:
        return 'insufficient'
    if not (tier_certified and rows_complete and constants_exact):
        return 'limited'
    return 'accepted_within_scope'


def strip_code(text):
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    return re.sub(r'`[^`\n]*`', ' ', text)


# ---------------------------------------------------------------------------
def compute(check_sha):
    c, contract_digest = load_contract()          # sha256 verified before any evaluation
    V = contract_values(c)
    tau_cap = V['tau_cap']
    target = V['target']
    check('contract_snapshot_sha256',
          contract_digest == CONTRACT_SHA256 and target == Q(1, 100) and len(V['controls']) == 21 and len(V['obligation_names']) == 6,
          contract_sha256=contract_digest, contract_path=CONTRACT_REL, target_read_from_contract=s(target),
          target_quantity=V['target_quantity'], tau_read_from_contract=s(tau_cap), signs=V['signs'],
          reference_read_from_contract=V['reference_value'] + ' via ' + V['reference_route'],
          obligation_names_read_from_contract=V['obligation_names'], controls_read_from_contract=len(V['controls']),
          hash_binding=V['hash_binding'])

    # ======================= premise inventory and the AY1 gate =======================
    expected_inputs = ['AGENTS.md', CONTRACT_REL] + V['shared']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    gate_sha = inventory.get(P_AY1_GATE)
    check('premise_inventory_bound',
          sorted(inventory) == sorted(set(expected_inputs)) and len(inventory) == 23 and gate_sha is not None
          and not any('__pycache__' in k or k.endswith('.pyc') for k in inventory),
          inventory_files=len(inventory), ay1_gate_sha256=gate_sha, inputs_sha256=inventory,
          isolation='inputs equal AGENTS.md + the AY2 contract + its 21 shared premises; no current skeptic, expert, deliberation or panel file')

    gate = load_json_input(P_AY1_GATE)
    acc, dcs, lims = gate['accepted'], gate['decision'], ' '.join(gate['limitations'])
    gf = gate['gate_fields']
    check('ay1_gate_fields_and_verdict',
          gate['loop'] == 'AY1' and gate['verdict'] == 'accepted_within_scope' and gate['sub_label'] == 'uniform_local_closeness_not_uniqueness'
          and all(gf[k] is False for k in ('uniqueness_claimed', 'whole_sequence_claimed', 'rate_claimed', 'rate_in_N_claimed',
                                           'translation_invariance_claimed', 'boundary_independence_of_dynamics_claimed'))
          and gf['closeness_order'] == [1, 2] and gf['topology'].startswith('trace norm on B(H_R)')
          and all(k in gate['bindings'] for k in (P_AY1F, P_AY1R, P_AY1S))
          and gate['bindings'][P_AY1F] == inventory[P_AY1F] and gate['bindings'][P_AY1R] == inventory[P_AY1R]
          and gate['bindings'][P_AY1S] == inventory[P_AY1S],
          ay1_gate_sha256=gate_sha, ay1_verdict=gate['verdict'], ay1_sub_label=gate['sub_label'], ay1_gate_fields=gf,
          note='the AY1 forward and reverse reports and the AY1 skeptic review snapshotted here are the bytes the AY1 gate binds')

    # exact constants from the gate text
    m = match(r'Constants: 2D=(\d+)/(\d+) \(~([\d.e-]+); D=(\d+)/(\d+) the AV1 gate forward tier \(ii\)\)', acc, 'gate 2D and D')
    twoD_g, D_g, twoD_prev = frac_of(m, 1), frac_of(m, 4), m.group(3)
    m = match(r"R-local trace-norm constant K_2'=(\d+)/(\d+) \(~([\d.]+); items (\d+)rho\+(\d+)T\((\d+)a\+(\d+)rho\)\+(\d+)\((\d+)a\+rho\)\^2\+(\d+)eps_R\^2\+(\d+)a eps_R\^2, "
              r"a=\|tau\|/(\d+), T=\((\d+)a\)/\(1-(\d+)J\), rho=(\d+)JT, eps_R=(\d+)a\+(\d+)rho\+\((\d+)a\+rho\)\^2\)", acc, 'gate K_2prime itemization')
    K2p_g, K2p_prev = frac_of(m, 1), m.group(3)
    F = {'c_am2': int(m.group(4)), 'c_str': int(m.group(5)), 'str_pin': int(m.group(6)), 'str_rho': int(m.group(7)), 'c_two': int(m.group(8)),
         'single_pin': int(m.group(9)), 'c_den': int(m.group(10)), 'c_norm': int(m.group(11)), 'a_den': int(m.group(12)),
         'T_num': int(m.group(13)), 'GpR': int(m.group(14)), 'GpR_rho': int(m.group(15)), 'meet_pin': int(m.group(16)),
         'epsR_rho': int(m.group(17)), 'single_pin2': int(m.group(18))}
    require(F['GpR'] == F['GpR_rho'] and F['single_pin'] == F['single_pin2'], 'gate itemization consistent')
    m = match(r'per-site sum J<=(\d+)\|tau\|=J_0=(\d+)/(\d+) at the cap', acc, 'gate J')
    F['J_per_tau'] = int(m.group(1))
    J0_g = frac_of(m, 2)
    m = match(r"so any two such limits satisfy \|\|rho_R-rho'_R\|\|_1<=2K_2' tau\^2=(\d+)/(\d+) ?\(~([\d.e-]+)\)", acc, 'gate 2K_2prime tau^2')
    two_K2_g, two_K2_prev = frac_of(m, 1), m.group(3)
    m = match(r'K_2\^\+=(\d+)/(\d+) \(~([\d.]+)\) by the factor ~([\d.]+)', acc, 'gate K_2^+')
    K2plus_g, K2plus_prev, ratio_prev = frac_of(m, 1), m.group(3), m.group(4)
    m = match(r'over the (\d+) faces F_R with owner set exactly R \(xz r=0,1,2, s=0,1 and yz r=0\.\.3, s=0, anchored at 0; the (\d+) straddling faces among the (\d+) meeting R have zero R-marginal', acc, 'gate pins')
    pins_g = {'inside': int(m.group(1)), 'straddling': int(m.group(2)), 'meet': int(m.group(3))}
    require(pins_g['straddling'] == F['str_pin'] and pins_g['meet'] == F['meet_pin'] and F['c_norm'] == 2 * pins_g['inside'], 'pins consistent within the gate')
    pins_g['single'] = F['single_pin']
    rho1_text = 'rho^(1)_R=(tau/72) sum_{f in F_R}(|W_f Omega_R><Omega_R|+|Omega_R><W_f Omega_R|)'
    tn_text = '||rho^(1)_R||_1=sqrt(10)|tau|/72'
    trw_text = 'Tr(rho^(1)_R W)=+tau/144'
    single_text = "for every subsequential limit of either family ||rho_R-P_R-rho^(1)_R||_1<=K_2' tau^2"
    obs = match(r'\|\|rho_R-P_R\|\|_1 in \[([\d.e-]+), ([\d.e-]+)\] for every limit of either family', dcs, 'gate recorded observation')
    obs_lo_prev, obs_hi_prev = obs.group(1), obs.group(2)
    m = match(r'labelled variants \(sqrt-2 sectors ~([\d.]+), 288-majorant ~([\d.]+), both ~([\d.]+), admitted-eps ~([\d.]+)\)', lims, 'gate variants')
    variant_prev = {'sqrt2_sectors': m.group(1), 'majorant_288': m.group(2), 'both': m.group(3), 'admitted_eps': m.group(4)}
    floor_prev = match(r'is at least 2rho/tau\^2~(\d+\.\d+)', acc, 'gate floor').group(1)
    check('ay1_gate_constants_parsed_exact',
          rho1_text in acc and tn_text in acc and trw_text in acc and single_text in acc and twoD_g == 2 * D_g
          and two_K2_g == 2 * K2p_g * tau_cap ** 2 and J0_g == F['J_per_tau'] * tau_cap and 'K_2^+ is volume-uniform and W-specific' in dcs
          and "the contract's 'not the whole-box K_2^+' is read as 'built from R-local face counts'" in dcs,
          two_D=s(twoD_g), D=s(D_g), K2_prime=s(K2p_g), two_K2_prime_tau2=s(two_K2_g), K2_plus=s(K2plus_g), J0=s(J0_g),
          itemization_coefficients=F, pins_from_gate=pins_g, recorded_observation_previews=[obs_lo_prev, obs_hi_prev],
          read_from='the accepted/decision/limitations strings of the hash-bound AY1 gate snapshot; no constant is typed in')

    # ======================= recomputation of every gate constant from the gate's own itemization =======================
    ay1f, ay1r, ay1s = read_input(P_AY1F), read_input(P_AY1R), read_input(P_AY1S)
    require('\\varepsilon=2T+T^2=' in ay1f and 'D=\\tfrac{2\\varepsilon(1+\\varepsilon)}{1+\\varepsilon^2}' in ay1f, 'AY1 forward eps and D formulas')
    require('K_2^+ tau^2 = r_AM2 + T·T + T^2 + eps^2 + a·eps^2' in ay1r, 'AW1 skeptic itemization of K_2^+ as quoted in the AY1 reverse report')
    it = {sg: ay1_items(t, F, pins_g) for sg, t in (('+', tau_cap), ('-', -tau_cap))}
    K2p = it['+']['total'] / tau_cap ** 2
    D = D_from(it['+']['T'])
    K2plus = K2plus_from(it['+']) / tau_cap ** 2
    K2p_tau2 = K2p * tau_cap ** 2
    two_K2 = 2 * K2p_tau2
    twoD = 2 * D

    def validate_constants(k2p, d_, k2plus):
        require(k2p == K2p_g, "K_2' differs from the AY1 gate value")
        require(d_ == D_g, 'D differs from the AY1 gate value')
        require(k2plus == K2plus_g, 'K_2^+ differs from the AY1 gate value')
        return True
    F_bad = dict(F, c_am2=2)
    pins_bad = dict(pins_g, straddling=66)
    check('ay1_gate_constants_recomputed',
          validate_constants(K2p, D, K2plus) and it['-']['total'] == it['+']['total']
          and rejected(lambda: validate_constants(ay1_items(tau_cap, F_bad, pins_g)['total'] / tau_cap ** 2, D, K2plus), 'am2_item_4rho_replaced_by_2rho')
          and rejected(lambda: validate_constants(ay1_items(tau_cap, F, pins_bad)['total'] / tau_cap ** 2, D, K2plus), 'straddling_pin_72_replaced_by_66')
          and rejected(lambda: validate_constants(K2p, D_from(it['+']['a'] * 49), K2plus), 'D_with_t1_without_remainder'),
          T=s(it['+']['T']), r_am2=s(it['+']['r_am2']), eps=s(it['+']['eps']), eps_R=s(it['+']['epsR']),
          items_over_tau2={k: s(x / tau_cap ** 2) for k, x in it['+']['items'].items()},
          items_preview={k: dec(x / tau_cap ** 2) for k, x in it['+']['items'].items()},
          K2_prime=s(K2p), K2_prime_preview=dec(K2p), D=s(D), K2_plus=s(K2plus), K2_plus_preview=dec(K2plus),
          minus_tau='the -tau evaluation replays the same |tau| formula (not a second confirmation)')

    # ======================= I1 geometry: faces meeting R, the ten faces with owner set R, the cover =======================
    i1 = read_input(P_I1)
    classes = parse_i1_table(i1)
    omitted = [k for k in classes if k[4] == 'omitted']
    geo_ok = True
    for cls in classes:
        f = (ORIGIN, cls)
        geo_ok = geo_ok and face_owner_set(f) == cls[3]
    require(geo_ok and len(omitted) == 21, 'I1 table supports reproduced from link tails')
    R = frozenset((ORIGIN, EZ))
    cube = [(x, y, z) for x in range(-2, 3) for y in range(-2, 3) for z in range(-2, 3)]
    meet = faces_meeting(R, omitted, cube)
    anchors = sorted({f[0] for f in meet})
    inside = [f for f in meet if face_owner_set(f) == R]
    straddling = [f for f in meet if not face_owner_set(f) <= R]
    one_site = [f for f in straddling if len(face_owner_set(f) & R) == 1]
    contain_strict = [f for f in meet if face_owner_set(f) > R]
    single0 = [f for f in meet if ORIGIN in face_owner_set(f) and EZ not in face_owner_set(f)]
    singlez = [f for f in meet if EZ in face_owner_set(f) and ORIGIN not in face_owner_set(f)]
    pins = {'meet': len(meet), 'inside': len(inside), 'straddling': len(straddling), 'single': len(single0)}
    expected_anchors = sorted(vsub(u, d) for u in R for d in S_STAR)
    all_ls = [face_linkset(f) for f in meet]
    share_ok = all(len(all_ls[i] & all_ls[j]) <= 1 for i in range(len(all_ls)) for j in range(i + 1, len(all_ls)))
    straddle_outside_link = all(any(owner(l[0]) not in R for l in face_linkset(f)) for f in straddling)
    inside_labels = sorted(label_of(f) for f in inside)
    inside_expected = sorted(['xz r=%d s=%d anchored at (0,0,0)' % (r, q) for r in (0, 1, 2) for q in (0, 1)]
                             + ['yz r=%d s=0 anchored at (0,0,0)' % r for r in range(4)])
    check('i1_face_enumeration_R_local',
          pins == pins_g and len(one_site) == 66 and len(contain_strict) == 6 and len(singlez) == len(single0)
          and anchors == sorted(set(expected_anchors)) and len(anchors) == 7 and share_ok and straddle_outside_link
          and inside_labels == inside_expected,
          pins=pins, one_site_straddling=len(one_site), strictly_containing_R=len(contain_strict), anchors=[list(b) for b in anchors],
          faces_owner_set_R=inside_labels, pairwise_shared_links_at_most_one=share_ok,
          note='pins derived from the parsed I1 table and the fine-lattice link tails; they equal the pins in the AY1 gate itemization')

    # control: missing_incoming_stars
    def validate_pins(p):
        require(p == pins_g, 'R-local pins differ from the gate itemization (incoming stars must be counted)')
        require(ay1_items(tau_cap, F, p)['total'] == it['+']['total'], "K_2' recomputed from these pins differs from the gate")
        return True
    outgoing = faces_meeting(R, omitted, sorted(R))
    pins_out = {'meet': len(outgoing), 'inside': len([f for f in outgoing if face_owner_set(f) == R]),
                'straddling': len([f for f in outgoing if not face_owner_set(f) <= R]),
                'single': len([f for f in outgoing if ORIGIN in face_owner_set(f) and EZ not in face_owner_set(f)])}
    one_star = faces_meeting(R, omitted, [ORIGIN])
    pins_one = {'meet': len(one_star), 'inside': 10, 'straddling': len([f for f in one_star if not face_owner_set(f) <= R]), 'single': 0}
    check('missing_incoming_stars',
          validate_pins(pins) and pins_out['meet'] == 42
          and rejected(lambda: validate_pins(pins_out), 'outgoing_stars_only_42_faces_meeting_R')
          and rejected(lambda: validate_pins(pins_one), 'single_star_at_0_only'),
          anchors_required=len(anchors), faces_meeting_R_all_anchors=pins['meet'], faces_meeting_R_outgoing_only=pins_out['meet'])

    # control: full_original_wilson_cover
    Wface = (ORIGIN, next(k for k in omitted if (k[0], k[1], k[2]) == ('xz', 0, 0)))
    cover_links = set(factor_links(ORIGIN)) | set(factor_links(EZ))
    endpoints = {l[0] for l in cover_links} | {vadd(l[0], E_UNIT[l[1]]) for l in cover_links}

    def validate_cover(region, links):
        require(face_owner_set(Wface) <= region, 'the original xz Wilson loop is not covered by complete factors of the region')
        require(set(links) == set(l for b in region for l in factor_links(b)), 'the cover must consist of complete 24-link factors')
        return True
    drawn = sorted(face_linkset(Wface))
    check('full_original_wilson_cover',
          validate_cover(R, cover_links) and len(cover_links) == 48 and len(endpoints) == 36 and face_owner_set(Wface) == R
          and rejected(lambda: validate_cover(frozenset([ORIGIN]), factor_links(ORIGIN)), 'single_factor_cover_0')
          and rejected(lambda: validate_cover(R, drawn), 'four_drawn_links_as_cover'),
          cover='R={0,e_z}', links=len(cover_links), endpoints=len(endpoints), wilson_face='xz r=0 s=0 anchored at 0, owner set R')

    # ======================= Haar orthogonality, norms and the rank-two first-order density =======================
    moments = [(n, haar_W_moment(n), weyl_W_moment(n)) for n in range(9)]
    EW, EW2 = haar_W_moment(1), haar_W_moment(2)
    check('haar_moments_two_routes',
          all(a1 == b1 for _, a1, b1 in moments) and EW == 0 and EW2 == Q(1, 4) and haar_W_moment(4) == Q(1, 8),
          moments={str(n): s(a1) for n, a1, _ in moments}, routes='Clebsch-Gordan invariant count and Weyl/Wallis integration',
          bounded_by_one='I1: the normalized SU(2) trace W=(1/2)Tr U is real and bounded by one, so ||W||<=1')
    require('The normalized SU(2) trace is real and bounded by one.' in i1, 'I1 norm statement')

    FR = sorted(inside, key=label_of)
    nF = len(FR)
    G = [[haar_product([FR[i], FR[j]], EW2) for j in range(nF)] for i in range(nF)]

    def validate_gram(face_list):
        g = [[haar_product([face_list[i], face_list[j]], EW2) for j in range(len(face_list))] for i in range(len(face_list))]
        require(all(g[i][j] == (EW2 if i == j else 0) for i in range(len(g)) for j in range(len(g))), 'W_f Omega_R not orthogonal with norm^2 1/4')
        return True
    check('first_order_vectors_orthonormal',
          validate_gram(FR) and EW == 0 and all(len(face_linkset(f)) == 4 for f in FR)
          and rejected(lambda: validate_gram(FR[:9] + [FR[0]]), 'duplicated_face_not_orthogonal'),
          gram='E[W_f W_g] = (1/4) delta_fg for the ten faces with owner set R; <Omega_R, W_f Omega_R> = E[W] = 0',
          reason='f != g: a link of f not in g occurs once, so the centre grading kills the Haar integral; f = g: the holonomy of four distinct Haar links is Haar, E[W^2]=1/4',
          orthonormal_basis='Omega_R and e_f = 2 W_f Omega_R (f in F_R)')

    # 11-dim coordinates: index 0 = Omega_R, 1..10 = e_f.  W_f Omega_R has coordinate 1/2 on e_f.
    dim = nF + 1
    Om = [Q(1)] + [Q(0)] * nF

    def wvec(i):
        x = [Q(0)] * dim
        x[i + 1] = Q(1, 2)
        return x
    coef = Q(1, 72)
    require('the coefficient `-tau/72` is the same in both unit systems' in ay1f.replace('The coefficient', 'the coefficient'), 'AY1 first-order coefficient statement')
    pieces = [mscale(sym_outer(wvec(i), Om), coef) for i in range(nF)]
    rho_hat = madd(*pieces)
    c2 = rank_two_c2(rho_hat)
    piece_c2 = [rank_two_c2(pc) for pc in pieces]
    tn_sq = 4 * c2                                     # ||rho_hat||_1^2
    iW = FR.index(Wface)
    # compressed W on the span: <Omega,W e_f> = 2E[W W_f], <e_f,W e_g> = 4E[W_f W W_g], <Omega,W Omega> = E[W]
    MW = [[Q(0)] * dim for _ in range(dim)]
    MW[0][0] = EW
    for i in range(nF):
        MW[0][i + 1] = MW[i + 1][0] = 2 * haar_product([Wface, FR[i]], EW2)
        for j in range(nF):
            require(odd_link_vanishes([face_linkset(FR[i]), face_linkset(Wface), face_linkset(FR[j])]),
                    'three-face Haar moment E[W_f W W_g] must vanish by the centre grading')
            MW[i + 1][j + 1] = Q(0)
    trW = mtrace(mmul(rho_hat, MW))

    def validate_eigen_claim(c2_claim):
        require(c2_claim == c2, 'claimed eigenvalue of rho^(1)_R/tau differs from the exact +-sqrt(Tr rho^2/2)')
        return True

    def validate_rank_one(pc):
        require(mtrace(pc) != 0 or mzero(pc), 'a nonzero traceless Hermitian operator is not rank one')
        return True

    def validate_centre(tn_sq_claim):
        require(tn_sq_claim == tn_sq, 'trace norm of rho^(1)_R differs from sqrt(10)|tau|/72')
        return True
    check('first_order_density_rank_two',
          c2 == Q(10, 144 ** 2) and tn_sq == Q(10, 72 ** 2) and all(pc == Q(1, 144 ** 2) for pc in piece_c2) and trW == Q(1, 144)
          and iW >= 0 and validate_eigen_claim(Q(10, 144 ** 2)) and validate_centre(Q(10, 5184))
          and rejected(lambda: validate_eigen_claim(Q(10, 72 ** 2)), 'relayed_claim_eigenvalues_pm_sqrt10_tau_over_72')
          and rejected(lambda: validate_rank_one(pieces[0]), 'each_face_piece_called_rank_one')
          and rejected(lambda: validate_centre(Q(10 * 10, 72 ** 2)), 'linear_sum_10_tau_over_72_as_trace_norm')
          and rejected(lambda: rank_two_c2(madd(rho_hat, mscale(outer(Om, Om), Q(1, 144)))), 'scalar_diagonal_first_order_term_added'),
          rho1_over_tau='(1/72) sum_f (|W_f Omega_R><Omega_R| + h.c.) = (1/144) sum_f (|e_f><Omega_R| + h.c.)',
          spectrum_over_tau='+sqrt(10)/144 and -sqrt(10)/144 (each simple) and 0; c^2 = %s' % s(c2),
          each_face_piece='rank two (a rank-one operator plus its adjoint), eigenvalues +-1/144, trace zero',
          trace_norm_over_abs_tau_squared=s(tn_sq), trace_norm_over_abs_tau='sqrt(10)/72', tr_rho1_W_over_tau=s(trW),
          correction_to_relayed_wording='the eigenvalues are +-sqrt(10)tau/144, not +-sqrt(10)tau/72; the trace norm sqrt(10)|tau|/72 is their absolute sum; each of the ten pieces is itself rank two, and the sum is rank two because all ten share Omega_R')

    # ======================= sqrt(10) enclosure and the two-sided first-order distance tier =======================
    lo10, hi10 = sqrt_bracket(10)
    check('sqrt10_enclosure',
          lo10 * lo10 < 10 < hi10 * hi10 and hi10 - lo10 == Q(1, SQRT_SCALE)
          and rejected(lambda: sqrt_bracket(10.0), 'float_sqrt10_input')
          and rejected(lambda: require(Q(316227766, 10 ** 8) ** 2 >= 10, 'rounded-down value used as an upper bracket'), 'truncated_decimal_as_upper_bracket'),
          sqrt10_lower=s(lo10), sqrt10_upper=s(hi10), width='10^-30', method='integer square root of 10*10^60, directed')

    # single-state remainder: justified from the AY1 report items, not assumed
    items_ok = ('\\tag{HNM-AY1-F13}' in ay1f and '\\tag{HNM-AY1-F14}' in ay1f and '\\tag{HNM-AY1-F11}' in ay1f
                and 'It passes to the untruncated ground (AV1 F22) and to every subsequential limit (closed ball).' in ay1f
                and 'It passes to the untruncated ground and then to every subsequential limit, because the ball is closed in trace norm.' in ay1r
                and 'I verified each end exactly as a directed bound' in ay1s)
    Kseq = [ay1_items(tau_cap / k, F, pins_g)['total'] / (tau_cap / k) ** 2 for k in (1, 10, 100, 1000)]

    def tier(k_single, sqrt_lo, sqrt_hi, tau=tau_cap):
        lower = sqrt_lo * abs(tau) / 72 - k_single * tau * tau
        upper = sqrt_hi * abs(tau) / 72 + k_single * tau * tau
        return lower, upper

    def validate_tier(lower, upper, tau=tau_cap):
        require(isinstance(lower, Q) and isinstance(upper, Q), 'tier ends must be exact rationals')
        rt = K2p * tau * tau
        exact_sq = tn_sq * tau * tau                    # (sqrt(10)|tau|/72)^2
        require(lower + rt >= 0 and (lower + rt) ** 2 <= exact_sq, 'lower end is not a lower bound of sqrt(10)|tau|/72 - K_2prime tau^2')
        require(upper - rt >= 0 and (upper - rt) ** 2 >= exact_sq, 'upper end is not an upper bound of sqrt(10)|tau|/72 + K_2prime tau^2')
        require(lower > 0, 'lower end must be positive (first order charged)')
        return True
    lower, upper = tier(K2p, lo10, hi10)
    lower_m, upper_m = tier(K2p, lo10, hi10, -tau_cap)
    check('single_state_remainder_justified',
          items_ok and single_text in acc and all(Kseq[i] >= Kseq[i + 1] for i in range(3)) and validate_tier(lower, upper)
          and rejected(lambda: validate_tier(*tier(K2p / 2, lo10, hi10)), 'single_state_remainder_halved')
          and rejected(lambda: validate_tier(lo10 * tau_cap / 72, hi10 * tau_cap / 72), 'remainder_dropped'),
          single_state_bound="||rho_R - P_R - rho^(1)_R||_1 <= K_2' tau^2 for every subsequential limit of either family (AY1 gate)",
          derivation=['AY1 F13: exact R-marginal decomposition r_R = rho_R - P_R - rho^(1)_R in every box of either family at every cutoff L>=24',
                      'AY1 F14: ||r_R||_1 <= 4rho + 2T(72a+2rho) + 2(33a+rho)^2 + 2eps_R^2 + 20a eps_R^2 = K_2prime tau^2, uniform in N, cutoff and family',
                      'AV1 F22 cutoff-vector removal: the bound passes to the untruncated ground',
                      'closed trace-norm ball around the family-independent centre P_R + rho^(1)_R: the bound passes to every subsequential limit',
                      'the centre is the same for every box: both families retain the same ten faces with owner set R for N>=2'],
          single_versus_pair='K_2prime tau^2 bounds one state against the product plus the common first-order density; 2K_2prime tau^2 bounds a pair of limits',
          K2_prime_at_tau_over_1_10_100_1000_preview=[dec(k1, 10) for k1 in Kseq],
          monotone='K_2prime(|tau|) is nondecreasing in |tau| (every item divided by tau^2 is a sum of products of nonnegative increasing functions of |tau|), so the cap value bounds every smaller |tau|')

    centre_lo = lo10 * tau_cap / 72
    rel_width = (upper - lower) / centre_lo
    rel_width_ideal = 2 * K2p_tau2 / centre_lo
    tier_lo_ok = abs(lower - preview_value(obs_lo_prev)) < Q(1, 10 ** 14) and abs(upper - preview_value(obs_hi_prev)) < Q(1, 10 ** 14)
    mS = match(r'\| forward lower \| `(\d+)/(\d+)` \|', ay1s, 'skeptic forward lower')
    mU = match(r'\| forward upper \| `(\d+)/(\d+)` \|', ay1s, 'skeptic forward upper')
    sk_lo, sk_hi = frac_of(mS, 1), frac_of(mU, 1)
    per_tau_lower = lo10 / 72 - K2p * tau_cap          # lower/|tau| at every 0<|tau|<=cap is at least this

    def validate_relwidth(rw):
        require(rw <= target, 'relative width exceeds the preregistered target')
        return True
    check('first_order_distance_tier_certified',
          validate_tier(lower, upper) and validate_tier(lower_m, upper_m, -tau_cap) and lower == lower_m and upper == upper_m
          and validate_relwidth(rel_width) and rel_width_ideal <= rel_width and tier_lo_ok
          and abs(lower - sk_lo) < Q(1, 10 ** 22) and abs(upper - sk_hi) < Q(1, 10 ** 22) and per_tau_lower > 0
          and rejected(lambda: validate_tier(*tier(K2p, hi10, lo10)), 'sqrt10_rounded_the_wrong_way')
          and rejected(lambda: validate_relwidth((upper - lower + D) / centre_lo), 'width_with_D_added'),
          tier='first_order_distance_from_product', lower=s(lower), lower_preview=dec(lower), upper=s(upper), upper_preview=dec(upper),
          relative_width_upper=s(rel_width), relative_width_preview=dec(rel_width), target=s(target), comparator='<=',
          margin_preview=dec(target / rel_width, 8), relative_width_ideal_upper=s(rel_width_ideal),
          both_signs='tau=+1/100000000 and -1/100000000 give the same interval (the -tau value replays the same |tau| formula)',
          ay1_recorded_observation=[obs_lo_prev, obs_hi_prev], matches_skeptic_exact_ends_within='1e-22',
          positivity_below_cap='for every 0<|tau|<=1/100000000: ||rho_R-P_R||_1 >= |tau| (sqrt10_lo/72 - K_2prime/10^8) = |tau| * %s > 0' % dec(per_tau_lower))

    # ======================= the pair statement, the falsifying scenario, the +-tau separation =======================
    def validate_pair_bound(total, parts):
        require(total == sum(parts, Q(0)), 'deterministic remainders add linearly')
        return True
    check('two_limits_second_order_bound',
          validate_pair_bound(two_K2, [K2p_tau2, K2p_tau2]) and two_K2 == two_K2_g and twoD == twoD_g and two_K2 < twoD,
          two_K2_prime_tau2=s(two_K2), preview=dec(two_K2), two_D=s(twoD), two_D_preview=dec(twoD),
          ratio_two_D_over_two_K2_preview=dec(twoD / two_K2, 8),
          statement="for every pair of subsequential limits of F1/F2 at the same tau: ||rho_R-rho'_R||_1 <= 2D (order tau) and <= 2K_2' tau^2 (order tau^2, the common rho^(1)_R cancels)")

    # falsifying witness on H_R: psi_pm = Omega + (tau/144) v +- nu w', v = sum e_f, w' = e_a - e_b + e_c - e_d (yz faces)
    tau = tau_cap
    v = [Q(0)] + [Q(1)] * nF
    yz_idx = [i for i, f in enumerate(FR) if f[1][0] == 'yz']
    require(len(yz_idx) == 4 and iW not in yz_idx, 'four yz faces, none the Wilson face')
    wp = [Q(0)] * dim
    for sign_, i in zip((1, -1, 1, -1), yz_idx):
        wp[i + 1] = Q(sign_)
    nu = K2p_tau2 * (1 - Q(1, 10 ** 6)) / 4
    t144 = tau / 144
    sigma = madd(outer(Om, Om), mscale(rho_hat, tau))

    def witness(sgn, nu_=nu):
        psi = [Om[i] + t144 * v[i] + sgn * nu_ * wp[i] for i in range(dim)]
        n2 = dot(psi, psi)
        return psi, n2, mscale(outer(psi, psi), 1 / n2)

    def witness_constraints(sgn, nu_=nu):
        psi, n2, rho = witness(sgn, nu_)
        require(mtrace(rho) == 1 and n2 > 0, 'witness is a normalized pure state')
        pcs = [mscale(outer(Om, Om), 1 - n2), mscale(sym_outer(v, Om), t144 * (1 - n2)), mscale(sym_outer(wp, Om), sgn * nu_),
               mscale(outer(v, v), t144 * t144), mscale(sym_outer(v, wp), sgn * t144 * nu_), mscale(outer(wp, wp), nu_ * nu_)]
        require(meq(madd(*pcs), mscale(madd(rho, mscale(sigma, -1)), n2)), 'decomposition of n^2(rho - sigma)')
        ub = (abs(1 - n2) + trace_norm_upper_rank_two(pcs[1]) + trace_norm_upper_rank_two(pcs[2]) + t144 * t144 * dot(v, v)
              + trace_norm_upper_rank_two(pcs[4]) + nu_ * nu_ * dot(wp, wp)) / n2
        require(ub <= K2p_tau2, "witness outside the AY1 ball ||rho - P_R - rho^(1)_R||_1 <= K_2' tau^2")
        require(hi10 * abs(tau) / 72 + ub <= D, 'witness outside the AV1 ball ||rho - P_R||_1 <= D')
        wmean = dot(psi, [dot(MW[i], psi) for i in range(dim)]) / n2
        require(abs(wmean - tau / 144) <= K2plus * tau * tau, 'witness outside the AW1 band |omega(W) - tau/144| <= K_2^+ tau^2')
        energy_alpha = 3 * (n2 - 1) / n2              # each W_f Omega_R excitation carries 3 alpha (four spin-1/2 Casimirs 3/4)
        require(energy_alpha <= Q(98, 8) * abs(tau), 'witness exceeds the reset energy 98|tau| delta-units = 98|tau|/8 alpha-units')
        return {'n2': n2, 'ball_upper': ub, 'wilson_mean': wmean, 'energy_alpha_units': energy_alpha}
    wp_c = witness_constraints(1)
    wm_c = witness_constraints(-1)
    psi_p, n2p, rho_p = witness(1)
    psi_m, n2m, rho_m = witness(-1)
    x_vec = [Om[i] + t144 * v[i] for i in range(dim)]
    diff_scaled = mscale(sym_outer(wp, x_vec), 2 * nu)
    require(meq(diff_scaled, mscale(madd(rho_p, mscale(rho_m, -1)), n2p)) and n2p == n2m, 'difference identity')
    diff_c2 = rank_two_c2(mscale(diff_scaled, 1 / n2p))          # ||rho_+ - rho_-||_1 = 2 sqrt(diff_c2)
    L_target = (1 - Q(2, 10 ** 6)) * two_K2

    def validate_separation(Lclaim, c2_):
        require(Lclaim >= 0 and (Lclaim / 2) ** 2 <= c2_, 'claimed lower bound on the witness separation not certified')
        return True
    check('falsifying_scenario_witness',
          validate_separation(L_target, diff_c2) and rho_p != rho_m
          and rejected(lambda: witness_constraints(1, nu * 3), 'witness_pushed_outside_the_K2prime_ball')
          and rejected(lambda: validate_separation(two_K2 * Q(1000001, 1000000), diff_c2), 'separation_claimed_beyond_2K2prime_tau2'),
          model_is_finite_graph=False, transfers_to_aq=False, on_hilbert_space='H_R (the 11-dim span of Omega_R and the ten e_f)',
          nu=s(nu), separation_lower=s(L_target), separation_lower_preview=dec(L_target), separation_over_two_K2_at_least='1 - 2e-6',
          constraints_satisfied=['||rho - P_R - rho^(1)_R||_1 <= K_2prime tau^2 (upper %s)' % dec(wp_c['ball_upper']),
                                 '||rho - P_R||_1 <= D', '|Tr(rho W) - tau/144| <= K_2^+ tau^2 (Tr rho W = (tau/144)/n^2)',
                                 'reset energy <= 98|tau| delta-units', 'gauge invariant (Omega_R and the W_f Omega_R are gauge-invariant functions)',
                                 'hence also the two-sided tier and the pair bounds 2D and 2K_2prime tau^2'],
          meaning='two density matrices on H_R obey every constraint the admitted AY1 material places on a subsequential limit and differ by at least (1-2e-6) 2K_2prime tau^2; the present one-state bounds cannot exclude two limits that differ this much',
          not_a_claim='no claim that such limits exist; the witness shows only what the admitted bounds leave open')

    # +-tau separation and 2D across couplings
    sep_formula = 'sqrt(10)|tau|/36'
    require("||rho^(1)_R(tau)-rho^(1)_R(-tau)||_1=sqrt(10)|tau|/36" in ay1f, 'AY1 +-tau first-order separation')
    sep_lower = lo10 * tau_cap / 36 - two_K2
    check('plus_minus_tau_separation',
          sep_lower > two_K2 and sep_lower > 0 and upper <= D and sep_lower <= twoD
          and (sep_lower + two_K2) ** 2 <= 4 * tn_sq * tau_cap ** 2,
          separation_lower=s(sep_lower), separation_lower_preview=dec(sep_lower), first_order_separation=sep_formula,
          both_within_D_of_P_R='each limit (at +tau and at -tau) lies within D (~%s) of P_R, so the pair lies within 2D of each other' % dec(D, 6),
          meaning='2D alone also holds across opposite couplings, so 2D is a common enclosing ball, not a boundary comparison; the comparison content is the matching first-order term rho^(1)_R with the 2K_2prime tau^2 difference',
          tier_is_sign_blind='both the +tau and the -tau limits lie in the same two-sided tier, yet they differ by at least the value above')

    # ======================= K_2' versus K_2^+ =======================
    r_over = it['+']['r_am2'] / tau_cap ** 2
    floor = 2 * r_over
    s2lo, s2hi = sqrt_bracket(2)
    variants = {
        'sqrt2_sectors': ay1_items(tau_cap, F, pins_g, am2_factor=2 * s2hi)['total'] / tau_cap ** 2,
        'majorant_288': ay1_items(tau_cap, F, pins_g, remainder='288')['total'] / tau_cap ** 2,
        'both': ay1_items(tau_cap, F, pins_g, am2_factor=2 * s2hi, remainder='288')['total'] / tau_cap ** 2,
        'admitted_eps': ay1_items(tau_cap, F, pins_g, density_eps='adm')['total'] / tau_cap ** 2,
    }
    var_ok = all(abs(variants[k] - preview_value(variant_prev[k])) < Q(1, 100) for k in variants)
    duality = abs(trW * tau_cap) <= 1 and trW == Q(1, 144)

    def validate_comparison(kind_trace, kind_w):
        require(kind_trace == 'sup over ||A||<=1 in B(H_R) of |Tr(r_R A)|', "K_2' is a trace-norm constant over all of B(H_R)")
        require(kind_w == 'the single observable W', 'K_2^+ bounds the single observable W')
        return True
    check('k2prime_versus_k2plus',
          K2p > K2plus and floor > K2plus and floor_prev == '6708.2' and dec(floor, 5) == '6.7082e3' and var_ok and duality
          and all(val > K2plus for val in variants.values()) and 4 * r_over / K2p > Q(9999, 10000) and r_over / K2plus > Q(9997, 10000)
          and validate_comparison('sup over ||A||<=1 in B(H_R) of |Tr(r_R A)|', 'the single observable W')
          and rejected(lambda: validate_comparison('the single observable W', 'the single observable W'), 'K2prime_read_as_a_W_constant')
          and rejected(lambda: validate_comparison('sup over ||A||<=1 in B(H_R) of |Tr(r_R A)|', 'whole-box volume-dependent constant'), 'K2plus_read_as_whole_box'),
          K2_prime=s(K2p), K2_plus=s(K2plus), ratio=s(K2p / K2plus), ratio_preview=dec(K2p / K2plus, 8), gate_ratio_preview=ratio_prev,
          am2_floor_2rho_over_tau2=s(floor), am2_floor_preview=dec(floor), am2_share_of_K2prime_preview=dec(4 * r_over / K2p, 6),
          am2_share_of_K2plus_preview=dec(r_over / K2plus, 6),
          duality='||W||<=1, Tr(P_R W)=0 and Tr(rho^(1)_R W)=tau/144, so |omega(W)-tau/144| <= ||r_R||_1: every valid trace-norm constant is also a valid W constant, and the smallest valid trace-norm constant is at least the smallest valid W constant',
          labelled_variants_previews_only={k: dec(val, 9) for k, val in variants.items()}, gate_variant_previews=variant_prev,
          variants_admitted=False,
          wording_correction="the AY1 contract's 'not the whole-box K_2^+' is corrected: K_2^+ is volume-uniform (uniform in N) and W-specific; K_2' is built from R-local face pins and is larger, not smaller")

    # ======================= report: mandatory sentence, obligations table, phrasing =======================
    report_text = (BASE / 'report.md').read_text(encoding='utf-8')
    line = next((ln for ln in ay1f.splitlines() if ln.startswith("> For every pair of subsequential limits `omega'`")), None)
    require(line is not None, 'template sentence in the AY1 forward snapshot')
    k1 = line.index("`|omega'(A) - omega''(A)| <=")
    k2 = line.index('This is uniform local closeness')
    t_prefix, t_suffix = line[2:k1], line[k2:]
    require(t_prefix.replace('`', '') in ay1r and t_suffix.replace('`', '') in ay1r, 'template fixed text identical in the AY1 reverse snapshot')
    slot = ("`|omega'(A) - omega''(A)| <= 2D = " + s(twoD) + '` (about ' + dec(twoD) + "; order `tau^1`), and `<= 2K_2' tau^2 = "
            + s(two_K2) + '` (about ' + dec(two_K2) + '; order `tau^2` after subtracting the common first-order density `rho^(1)_R`)')
    sentence = t_prefix + slot + '. ' + t_suffix
    required_phrase = 'a chosen subsequential'

    def scan_report(text):
        require(sentence in text, 'mandatory sentence (filled template) missing from the report')
        body = strip_code(text)
        require(required_phrase in body, 'required phrase missing: ' + required_phrase)
        low = body.lower()
        require('the aq state' not in low and 'the thermodynamic limit' not in low, 'forbidden phrasing in the report')
        for sent in re.split(r'(?<=[.;:!?])\s+|\n', low):
            if 'unique' in sent:
                require(re.search(r'\bnot\b', sent) is not None, '"unique" without "not" in the report: ' + sent[:90])
        for val in (s(twoD), s(K2p), s(two_K2), s(lower), s(upper), s(rel_width)):
            require(val in text, 'report does not carry the exact value ' + val[:30])
        require('first_order_distance_from_product' in text, 'tier label missing from the report')
        return True

    def parse_obligations(text):
        sec = text.split('## 2. ', 1)
        require(len(sec) == 2, 'obligations section missing')
        body = sec[1].split('\n## 3. ', 1)[0]
        rows = [ln for ln in body.splitlines() if re.match(r'^\| O\d \|', ln)]
        out = []
        for ln in rows:
            cols = [x.strip() for x in ln.strip().strip('|').split(' | ')]
            require(len(cols) == 6, 'obligation row must have six columns')
            out.append({'id': cols[0], 'obligation': cols[1], 'status': cols[2], 'missing_premise': cols[3],
                        'candidate_route': cols[4], 'constant_to_evaluate': cols[5]})
        return out
    KEYS = [('HTW', 'Dobrushin'), ('Cauchy',), ('translation covariance',), ('N-dependent',), ('Lieb-Robinson', 'AM2'), ('Nachtergaele', 'padded')]

    def validate_obligations(rows):
        require(len(rows) == 6, 'the obligations table must have exactly six rows')
        for k, (row, name, keys) in enumerate(zip(rows, V['obligation_names'], KEYS)):
            require(row['id'] == 'O%d' % (k + 1) and row['obligation'] == name, 'obligation row name/order differs from contract item 2: ' + row['obligation'])
            require(row['status'] == 'unproved', 'every obligation stays unproved')
            require(len(row['missing_premise']) > 20 and len(row['candidate_route']) > 20 and len(row['constant_to_evaluate']) > 10, 'empty column')
            joined = row['missing_premise'] + ' ' + row['candidate_route'] + ' ' + row['constant_to_evaluate']
            require(all(key in joined for key in keys), 'obligation row lacks its contract route: ' + name)
        return True
    obligations = parse_obligations(report_text)
    check('mandatory_sentence_and_phrasing',
          scan_report(report_text)
          and rejected(lambda: scan_report(report_text + '\nThe limits define the thermodynamic limit.\n'), 'report_phrase_the_thermodynamic_limit')
          and rejected(lambda: scan_report(report_text + '\nThe AQ state is fixed.\n'), 'report_phrase_the_AQ_state')
          and rejected(lambda: scan_report(report_text + '\nThe limit on R is unique.\n'), 'report_unique_without_not')
          and rejected(lambda: scan_report(report_text.replace(sentence, sentence.replace('It does not assert', 'It asserts'))), 'mandatory_sentence_negation_removed'),
          mandatory_sentence_filled=sentence, required_phrase=required_phrase,
          template_source='fixed text parsed from the AY1 forward report snapshot and found identical (code spans removed) in the AY1 reverse report snapshot',
          report_scan='report.md scanned with code spans removed: no "the AQ state", no "the thermodynamic limit", every sentence containing "unique" contains "not", "a chosen subsequential" present, exact constants present')

    def drop_row(rows, k):
        return [r1 for i, r1 in enumerate(rows) if i != k]
    check('obligations_table_complete',
          validate_obligations(obligations)
          and rejected(lambda: validate_obligations(drop_row(obligations, 5)), 'padded_family_dynamics_row_removed')
          and rejected(lambda: validate_obligations([dict(r1, status='proved') if i == 0 else r1 for i, r1 in enumerate(obligations)]), 'uniqueness_row_marked_proved')
          and rejected(lambda: validate_obligations([dict(r1, candidate_route='') if i == 1 else r1 for i, r1 in enumerate(obligations)]), 'cauchy_route_missing')
          and rejected(lambda: validate_obligations(obligations + [dict(obligations[0], id='O7')]), 'seventh_row_added')
          and rejected(lambda: validate_obligations([obligations[1], obligations[0]] + obligations[2:]), 'rows_reordered_or_renamed'),
          rows=len(obligations), names=[r1['obligation'] for r1 in obligations], statuses=[r1['status'] for r1 in obligations],
          source='the six names are read from contract item 2; the table is parsed from report.md section 2')

    # ======================= gate fields and claim flags =======================
    FLAGS = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
             'scientific_priority_verified': False, 'weak_coupling_claim': False}
    CLAIMS = {'uniqueness_claimed': False, 'whole_sequence_claimed': False, 'rate_claimed': False, 'rate_in_N_claimed': False,
              'translation_invariance_claimed': False, 'boundary_independence_of_dynamics_claimed': False}
    require(all(CLAIMS[k] is v1 for k, v1 in V['gate_fields'].items()), 'preregistered gate fields exported unchanged')
    GATE = dict(CLAIMS)
    GATE.update({'states_compared': 'all subsequential limits of F1 and F2 at the same tau (every pair, same or different family); for the tier, each single subsequential limit of either family against the Haar product P_R',
                 'region': 'R={0,e_z} fixed before production (complete cover of the original xz Wilson loop; 48 links, 36 endpoints)',
                 'topology': 'trace norm on B(H_R)', 'dynamics_topology_named': 'norm on compact time windows (named only; no dynamical statement)',
                 'closeness_order': [1, 2]})

    def validate_claims(g):
        for k1 in CLAIMS:
            require(g.get(k1) is False, 'gate field ' + k1 + ' must be false')
        return True

    def validate_gate(g):
        validate_claims(g)
        for k1 in ('states_compared', 'region', 'topology', 'closeness_order'):
            require(k1 in g, 'missing gate field ' + k1)
        require(g['topology'] == 'trace norm on B(H_R)' and g['closeness_order'] == [1, 2], 'gate topology/order')
        return True

    def gmut(**kw):
        g2 = dict(GATE)
        g2.update(kw)
        return lambda: validate_gate(g2)
    check('gate_fields_exported',
          validate_gate(GATE)
          and rejected(gmut(rate_in_N_claimed=True), 'rate_in_N_true')
          and rejected(gmut(translation_invariance_claimed=True), 'translation_invariance_true')
          and rejected(gmut(boundary_independence_of_dynamics_claimed=True), 'boundary_independence_of_dynamics_true')
          and rejected(gmut(closeness_order=[1]), 'closeness_order_first_only')
          and rejected(lambda: validate_gate({k1: v1 for k1, v1 in GATE.items() if k1 != 'region'}), 'region_missing'),
          gate_fields=GATE)

    # ======================= error ledger =======================
    ledger = {
        'first_order_term': {'value': 'sqrt(10)|tau|/72', 'bracket': [s(lo10 * tau_cap / 72), s(hi10 * tau_cap / 72)],
                             'preview': dec(lo10 * tau_cap / 72), 'rounding': 'directed: lower end uses sqrt10_lower, upper end uses sqrt10_upper'},
        'second_order_remainder': {'single_state': s(K2p_tau2), 'single_state_preview': dec(K2p_tau2), 'two_limits': s(two_K2),
                                   'two_limits_preview': dec(two_K2), 'source': "AY1 gate K_2' (triangle headline), items added linearly"},
        'no_other_terms': {'status': 'not_applicable', 'reason': 'statement loop: the only new certificate is the two-sided tier; all arithmetic is exact except the directed sqrt(10) bracket, whose width 10^-30 is charged in the tier ends'},
    }
    names_pre = [t.split(':')[0].strip() for t in V['error_terms']]
    check('error_ledger_itemized',
          names_pre[:2] == ['first_order_term', 'second_order_remainder'] and V['error_terms'][2].startswith('no other terms')
          and len(ledger) == 3 and 'reason' in ledger['no_other_terms'] and 'stated reason' in V['error_terms_rule'],
          ledger=ledger, preregistered=V['error_terms'])

    # ======================= remaining contract controls =======================
    def validate_coeff(cf):
        require(cf == Q(-1, 72), 'first-order coefficient per face must be -tau/72 (normalized -(tau/3)/24 = alpha units -(tau/24)/3)')
        return True

    def validate_clock(clk):
        require(clk == V['clock_common'], 'common physical clock s=alpha*t_E/hbar, theta=alpha*t/hbar required')
        return True
    alpha_fx, hbar_fx, tE_fx = Q(5), Q(7), Q(7, 5)
    s_fx = alpha_fx * tE_fx / hbar_fx
    check('wrong_delta_alpha_hbar_clock',
          validate_coeff(Q(-1, 3) / 24) and validate_coeff(Q(-1, 24) / 3) and validate_clock(V['clock_common']) and s_fx == 1
          and V['forbidden_u_div'] == 8 and V['forbidden_exponent'] == 24
          and rejected(lambda: validate_coeff(Q(-1, 24) / 24), 'tau_over_576_mixed_units')
          and rejected(lambda: validate_coeff(Q(-1, 3) / 3), 'tau_over_9_mixed_units')
          and rejected(lambda: validate_clock('normalized clock s over %d' % V['forbidden_u_div']), 'normalized_clock')
          and rejected(lambda: validate_centre(Q(10, 576 ** 2)), 'tier_centre_with_mixed_unit_coefficient'),
          clock=V['clock_common'], nonunit_fixture={'alpha': '5', 'hbar': '7', 't_E': '7/5', 's': s(s_fx)},
          note='the tier is static; the clock fixes G=H/alpha and theta, s for any later dynamical use')

    at4 = read_input(P_AT4)
    require('For the exact control `m=1/4,d=1/100`, they are respectively `+1/10000` and `-51/10000`.' in at4
            and 'retains the vacuum residue `m²=1/16`' in at4, 'AT4 centering control')
    mm, dd = Q(1, 4), Q(1, 100)
    vec_res, scal_res, unc_res = dd * dd, -2 * mm * dd - dd * dd, mm * mm

    def validate_centering(kind):
        require(kind == V['centering'], 'the tier concerns the uncentered density ||rho_R-P_R||_1 (contract centering: none)')
        return True

    def validate_tier_centre(centre_sq):
        require(centre_sq == tn_sq * tau_cap ** 2, 'tier centre must be the trace norm of the vector-type density rho^(1)_R, not a scalar mean')
        return True
    check('vector_versus_scalar_centering',
          validate_centering('none') and vec_res == Q(1, 10000) and scal_res == Q(-51, 10000) and unc_res == Q(1, 16)
          and validate_tier_centre(tn_sq * tau_cap ** 2)
          and rejected(lambda: validate_centering('vector'), 'vector_centering_imposed_on_the_static_density')
          and rejected(lambda: validate_centering('scalar'), 'scalar_subtraction_imposed')
          and rejected(lambda: validate_tier_centre((tau_cap / 144) ** 2), 'scalar_Wilson_mean_as_tier_centre'),
          residues={'vector': s(vec_res), 'scalar': s(scal_res), 'uncentered': s(unc_res)},
          note='rho^(1)_R is off-diagonal (|eta><Omega_R| + h.c.); a scalar mean such as tau/144 is one observable, and the trace norm is sqrt(10) times larger per unit')

    lower_W = tau_cap / 144 - K2plus * tau_cap ** 2

    def validate_first_order(tsq, lower_end):
        require(tsq > 0, 'first-order density must be charged')
        require(lower_W > K2p_tau2, 'a zero first-order density contradicts omega(W) >= tau/144 - K_2^+ tau^2')
        require(lower_end > 0, 'the tier lower end must be positive')
        return True
    check('first_order_mean_charged',
          validate_first_order(tn_sq, lower) and trW == Q(1, 144)
          and rejected(lambda: validate_first_order(Q(0), lower), 'first_order_density_set_to_zero')
          and rejected(lambda: validate_first_order(tn_sq, Q(0)), 'tier_lower_end_set_to_zero'),
          omega_W_lower_from_AW1=s(lower_W), omega_W_lower_preview=dec(lower_W), K2_prime_tau2=s(K2p_tau2))

    Ks100 = ay1_items(tau_cap / 100, F, pins_g)['total']
    ratio_first_sq = (tn_sq * tau_cap ** 2) / (tn_sq * (tau_cap / 100) ** 2)
    ratio_second = it['+']['total'] / Ks100
    ratio_rel = (2 * it['+']['total'] / (lo10 * tau_cap / 72)) / (2 * Ks100 / (lo10 * tau_cap / 100 / 72))

    def validate_exponent(label, ratio):
        lo_, hi_ = {'linear': (99, 101), 'quadratic': (9900, 10100), 'linear_squared': (9900, 10100), 'constant': (Q(99, 100), Q(101, 100))}[label]
        require(lo_ <= ratio <= hi_, 'scaling exponent does not match its label ' + label)
        return True
    check('tau_scaling_exponent',
          validate_exponent('linear_squared', ratio_first_sq) and ratio_first_sq == 10000 and validate_exponent('quadratic', ratio_second)
          and validate_exponent('linear', ratio_rel)
          and rejected(lambda: validate_exponent('quadratic', 100), 'first_order_term_labelled_second_order')
          and rejected(lambda: validate_exponent('linear', ratio_second), 'second_order_remainder_labelled_first_order')
          and rejected(lambda: validate_exponent('constant', ratio_rel), 'relative_width_labelled_tau_independent'),
          ratios={'first_order_term_squared': s(ratio_first_sq), 'second_order_remainder': dec(ratio_second, 10), 'relative_width': dec(ratio_rel, 10)})

    fam_m = match(r'two named construction families F1 = centered whole-star boxes Lambda_N \(AQ1\) and F2 = all-contained-face boxes with padding \(I1 section 6\)', acc, 'gate families')
    FAMS = ('F1 = centered whole-star boxes Lambda_N (AQ1)', 'F2 = all-contained-face boxes with padding (I1 section 6)')
    MODEL = {'model_id': V['model_id'], 'tau': tau_cap, 'triple': (0, 0, 0), 'reference': V['reference_route'], 'families': FAMS,
             'J_per_abs_tau': F['J_per_tau'], 'transfers_to_aq_from_fixture': False}

    def validate_model(mdl):
        require(mdl['model_id'] == 'AQ_patterned_zero_selected', 'model id')
        require(abs(mdl['tau']) == tau_cap, 'coupling differs from the preregistered cap')
        require(mdl['triple'] == (0, 0, 0), 'nonzero selected triple is another model')
        require(mdl['reference'] == 'haar', 'selected-strip reference is another model')
        require(mdl['families'] == FAMS, 'families relabelled')
        require(mdl['J_per_abs_tau'] == 28, 'per-site sum of a different model')
        require(mdl['transfers_to_aq_from_fixture'] is False, 'a finite fixture is not AQ data')
        return True

    def mmut(**kw):
        m2 = dict(MODEL)
        m2.update(kw)
        return lambda: validate_model(m2)
    check('changed_model_relabelled',
          fam_m is not None and validate_model(MODEL) and validate_model(dict(MODEL, tau=-tau_cap))
          and rejected(mmut(tau=Q(1, 10 ** 7)), 'tau_above_the_cap')
          and rejected(mmut(triple=(Q(1, 100), 0, 0)), 'nonzero_triple')
          and rejected(mmut(reference='selected_strip'), 'selected_strip_reference')
          and rejected(mmut(model_id='AQ_uniform_routeB', J_per_abs_tau=29), 'uniform_route_B_model')
          and rejected(mmut(families=(FAMS[0], 'literal vertex boxes (I1 section 7)')), 'literal_vertex_boxes_family')
          and rejected(mmut(transfers_to_aq_from_fixture=True), 'falsifier_fixture_relabelled_as_AQ_data'),
          model_id=V['model_id'], families=list(FAMS), state_provenance=V['state_provenance'])

    rows_complete = True
    constants_exact = True
    tier_certified = True
    verdict = forward_verdict(tier_certified, rows_complete, constants_exact, False)
    D_only_rel = (D - 0) / centre_lo
    W_lower_rel = (D - lower_W) / centre_lo

    def validate_verdict(reported, *args):
        require(reported == forward_verdict(*args), 'reported verdict differs from the contract acceptance rule')
        return True
    check('insufficient_verdict_retained',
          verdict == 'accepted_within_scope' and forward_verdict(True, False, True, False) == 'limited'
          and forward_verdict(False, True, True, False) == 'limited' and forward_verdict(True, True, True, True) == 'insufficient'
          and D_only_rel > target and W_lower_rel > target
          and rejected(lambda: validate_verdict('accepted_within_scope', True, False, True, False), 'missing_obligation_relabelled_accepted')
          and rejected(lambda: validate_verdict('limited', True, True, True, True), 'overclaim_relabelled_limited')
          and rejected(lambda: validate_verdict('accepted_within_scope', False, True, True, False), 'uncertified_tier_relabelled_accepted')
          and rejected(lambda: validate_relwidth(D_only_rel), 'D_ball_tier_retuned_to_pass'),
          retained_failures={'AV1_D_ball_only_[0,D]': {'relative_width_preview': dec(D_only_rel, 6), 'meets_target': False},
                             'W_mean_lower_end_[tau/144-K2plus tau^2, D]': {'relative_width_preview': dec(W_lower_rel, 6), 'meets_target': False}},
          rule='insufficient on any overclaim; limited if an obligation row is missing, a constant is inexact or the tier is uncertified')

    check('exact_arithmetic_admission',
          rat('1/100') == target and isinstance(lower, Q) and isinstance(upper, Q)
          and rejected(lambda: rat(1e-8), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('nan'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator')
          and rejected(lambda: rat(obs_lo_prev), 'decimal_preview_as_admission_value'),
          arithmetic='fractions.Fraction throughout; sqrt(10) and sqrt(2) by integer square roots with directed rounding; previews truncated from exact rationals')

    def validate_trace_norm_route(value_sq, kind):
        require(kind == 'exact orthogonality (Pythagoras over the ten orthonormal e_f)', 'the square root must come from exact orthogonality')
        require(value_sq == tn_sq, 'trace norm differs from the exact rank-two value')
        return True
    check('root_n_misuse',
          validate_pair_bound(two_K2, [K2p_tau2, K2p_tau2]) and validate_pair_bound(upper - lower, [K2p_tau2, K2p_tau2, (hi10 - lo10) * tau_cap / 72])
          and validate_trace_norm_route(tn_sq, 'exact orthogonality (Pythagoras over the ten orthonormal e_f)')
          and rejected(lambda: validate_pair_bound(K2p_tau2 * s2lo, [K2p_tau2, K2p_tau2]), 'rss_of_two_single_state_remainders')
          and rejected(lambda: validate_pair_bound(two_K2 / sqrt_bracket(10)[0], [K2p_tau2, K2p_tau2]), 'division_by_sqrt_of_face_count')
          and rejected(lambda: validate_trace_norm_route(tn_sq, 'random-phase root-N heuristic'), 'sqrt10_as_statistical_root_N')
          and rejected(lambda: validate_trace_norm_route(Q(100, 5184), 'exact orthogonality (Pythagoras over the ten orthonormal e_f)'), 'linear_face_sum_10_as_trace_norm'),
          note='sqrt(10) is ||sum_f e_f|| for ten exactly orthonormal vectors, not a statistical root-N; deterministic remainders add linearly')

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
          and rejected(fmut(uniform_wilson_claim=True), 'uniform_wilson_true') and rejected(fmut(resolved_interaction_shift=True), 'shift_true')
          and rejected(fmut(weak_coupling_claim=True), 'weak_coupling_true'),
          historical_or_occult_numeric_premise=False)

    TOP = {'states': 'trace norm on B(H_R)', 'dynamics': 'norm on compact time windows (named only; no dynamical statement)',
           'tier': 'trace norm on B(H_R)'}

    def validate_topology(tp):
        require(tp['states'] == 'trace norm on B(H_R)' and tp['tier'] == 'trace norm on B(H_R)', 'states and the tier use the trace norm on B(H_R)')
        require(tp['dynamics'].startswith('norm on compact time windows') and 'no dynamical statement' in tp['dynamics'], 'dynamics named only')
        require(tp['states'] != tp['dynamics'], 'two topologies named separately')
        return True

    def tmut(**kw):
        t2 = dict(TOP)
        t2.update(kw)
        return lambda: validate_topology(t2)
    check('topology_named',
          validate_topology(TOP)
          and rejected(tmut(states='weak-* on finite-rank observables'), 'weak_star_for_states')
          and rejected(tmut(tier='norm on compact time windows'), 'tier_claimed_in_the_dynamics_topology')
          and rejected(tmut(dynamics='trace norm on B(H_R)'), 'one_topology_for_both')
          and rejected(tmut(dynamics='norm on compact time windows (boundary independent)'), 'dynamical_statement_added'),
          topology=TOP)

    def validate_families(fams):
        require(tuple(fams) == FAMS, 'exactly the two named construction families F1 and F2')
        return True
    check('two_families_named',
          validate_families(FAMS) and '28N(5N+1) boundary faces more than F1' in acc
          and rejected(lambda: validate_families(FAMS[:1]), 'one_family_only')
          and rejected(lambda: validate_families(FAMS + ('literal vertex boxes (I1 section 7)',)), 'third_family_added')
          and rejected(lambda: validate_families(('all boundary conditions',)), 'all_boundary_conditions'),
          families=list(FAMS), difference='F2 retains 28N(5N+1) boundary faces more than F1; both retain the same 82 faces meeting R for N>=2')

    seq = [rho_p if k % 2 == 0 else rho_m for k in range(6)]

    def validate_sequence_claim(claim):
        require(claim == 'subsequential', 'only subsequential limits are constructed; whole-sequence convergence needs a Cauchy estimate in N')
        return True
    check('subsequence_versus_whole_sequence',
          validate_sequence_claim('subsequential') and all(seq[k] != seq[k + 1] for k in range(5)) and seq[0] == seq[2] == seq[4]
          and rejected(lambda: validate_sequence_claim('whole sequence converges'), 'whole_sequence_inferred_from_uniform_bounds')
          and rejected(lambda: validate_sequence_claim('rate 1/N'), 'rate_in_N_inferred')
          and rejected(gmut(whole_sequence_claimed=True), 'whole_sequence_flag_true'),
          example='the alternating sequence rho_+, rho_-, rho_+, ... (falsifier witness) satisfies every admitted one-state bound at every step and has two distinct subsequential limits',
          separation_lower_preview=dec(L_target))

    def validate_identification(claim):
        require(claim == 'closeness', 'closeness, a common tier or a common first-order density does not identify two limits')
        return True
    check('local_closeness_not_uniqueness',
          validate_identification('closeness') and rho_p != rho_m
          and rejected(lambda: validate_identification('equal because 2K_2prime tau^2-close'), 'equality_from_closeness')
          and rejected(lambda: validate_identification('equal because both lie in the two-sided tier'), 'equality_from_common_tier')
          and rejected(gmut(uniqueness_claimed=True), 'uniqueness_flag_true'),
          witness='rho_+ != rho_- both satisfy every admitted constraint (falsifying_scenario_witness)')

    PAIR = {'tau': (tau_cap, tau_cap), 'units': ('normalized delta=alpha/8',) * 2, 'clock': (V['clock_common'],) * 2}

    def validate_pair(pk):
        require(pk['tau'][0] == pk['tau'][1], 'the two limits must be compared at the same coupling tau')
        require(pk['units'][0] == pk['units'][1], 'common unit convention')
        require(pk['clock'][0] == pk['clock'][1] == V['clock_common'], 'common physical clock')
        return True

    def pmut(**kw):
        p2 = dict(PAIR)
        p2.update(kw)
        return lambda: validate_pair(p2)
    check('common_clock',
          validate_pair(PAIR) and sep_lower > two_K2
          and rejected(pmut(tau=(tau_cap, -tau_cap)), 'opposite_signs_first_order_densities_differ')
          and rejected(pmut(tau=(tau_cap, tau_cap / 2)), 'different_couplings')
          and rejected(pmut(units=('normalized delta=alpha/8', 'alpha units')), 'mixed_units_for_one_family')
          and rejected(pmut(clock=(V['clock_common'], 'normalized clock')), 'normalized_clock_for_one_family'),
          plus_minus_separation_lower=s(sep_lower), note='same coupling, same units, same clock; the +-tau limits differ by far more than 2K_2prime tau^2')

    def validate_tier_constant(kind, value):
        require(kind == "K_2' (AY1 gate, triangle headline, single state)", 'only the gate headline K_2prime enters the single-state tier')
        require(value == K2p_g, 'value differs from the gate headline')
        return True
    check('tier_mixing_rejected',
          validate_tier_constant("K_2' (AY1 gate, triangle headline, single state)", K2p)
          and rejected(lambda: validate_tier_constant("K_2' (AY1 gate, triangle headline, single state)", K2plus), 'W_only_K2plus_as_trace_norm_remainder')
          and rejected(lambda: validate_tier_constant("sqrt-2 sector variant (labelled preview)", variants['sqrt2_sectors']), 'labelled_variant_as_headline')
          and rejected(lambda: validate_tier_constant("pair constant 2K_2'", 2 * K2p), 'pair_constant_as_single_state_remainder')
          and rejected(lambda: validate_tier_constant('AV1 D (order tau)', D / tau_cap ** 2), 'first_order_ball_D_as_second_order_remainder')
          and rejected(lambda: validate_tier(tier(K2plus, lo10, hi10)[0], upper), 'lower_end_from_K2plus_upper_end_from_K2prime'),
          note='the tier uses exactly the AY1 gate K_2prime; K_2^+, the labelled variants, 2K_2prime and D are other tiers')

    g4_cap = 96 / tau_cap
    require('The AL1 dictionary (read through the AX1 gate) is `tau=96/g^4`' in ay1f, 'AL1 dictionary sentence')

    def validate_uniformity(kind):
        require(kind == 'N at fixed lattice spacing a and fixed tau', 'the bounds are uniform in N only, never in a')
        return True
    check('not_uniform_in_a',
          validate_uniformity('N at fixed lattice spacing a and fixed tau') and g4_cap == 9600000000
          and rejected(lambda: validate_uniformity('lattice spacing a'), 'uniform_in_a_claimed')
          and rejected(lambda: validate_uniformity('continuum limit'), 'uniform_in_N_read_as_continuum'),
          dictionary='tau=96/g^4 (AL1, a different model, as quoted in the AY1 forward report); |tau|<=10^-8 means g^4>=%s (strong bare coupling)' % s(g4_cap),
          region_note='R is two coarse factors: fixed in lattice units, shrinking in physical units as a->0')

    LABEL = {'tier': 'first_order_distance_from_product', 'kind': 'static property of the state on R',
             'dynamical_claim': False, 'interaction_shift_claim': False, 'euclidean_node_claim': False, 'identifies_the_limit': False,
             'excludes_P_R_on_R': True}

    def validate_label(lb):
        require(lb['tier'] == 'first_order_distance_from_product' and lb['kind'] == 'static property of the state on R', 'tier label and kind')
        for k1 in ('dynamical_claim', 'interaction_shift_claim', 'euclidean_node_claim', 'identifies_the_limit'):
            require(lb[k1] is False, 'the static tier carries no ' + k1)
        return True

    def lmut(**kw):
        l2 = dict(LABEL)
        l2.update(kw)
        return lambda: validate_label(l2)
    check('lower_bound_is_static_not_dynamic',
          validate_label(LABEL) and 'static_not_dynamic' in V['sub_labels'] and 'uniform_local_closeness_not_uniqueness' in V['sub_labels']
          and rejected(lmut(kind='dynamical'), 'tier_relabelled_dynamical')
          and rejected(lmut(interaction_shift_claim=True), 'tier_relabelled_interaction_shift')
          and rejected(lmut(euclidean_node_claim=True), 'tier_relabelled_euclidean_node')
          and rejected(lmut(identifies_the_limit=True), 'lower_bound_read_as_identification')
          and rejected(fmut(resolved_interaction_shift=True), 'resolved_interaction_shift_true'),
          label=LABEL, sub_labels=['uniform_local_closeness_not_uniqueness', 'static_not_dynamic'])

    # contract wording defects (non-blocking), each a verified fact about the frozen text
    defects = []
    if V['selected_after'] == '<preceding gate>':
        defects.append({'id': 'D1', 'field': 'selected_after', 'defect': "unfilled placeholder '<preceding gate>' (the preceding gate is AY1)"})
    if 'uniqueness of the AQ state' in V['prereg_exclusions']:
        defects.append({'id': 'D2', 'field': 'preregistration.claim_exclusions', 'defect': "contains the definite phrase forbidden by item 1 ('uniqueness of the AQ state'); quoted only verbatim in code spans, never asserted"})
    if 'rate_in_N_claimed' not in V['gate_fields'] and 'rate_in_N_claimed:false' in V['required'][5]:
        defects.append({'id': 'D3', 'field': 'preregistration.gate_fields_required', 'defect': 'lacks rate_in_N_claimed although item 6 requires it; both rate fields are exported false'})
    if 'while both lie within 2D of the product' in V['required'][2]:
        defects.append({'id': 'D4', 'field': 'required[2]', 'defect': "'both lie within 2D of the product': each limit lies within D of P_R (so the pair is within 2D of each other); 'at least 8.7e-10' is the preview of sqrt(10)|tau|/36 - 2K_2prime tau^2 (about 8.757e-10)"})
    if "'not the whole-box K_2^+'" in V['required'][4]:
        defects.append({'id': 'D5', 'field': 'required[4]', 'defect': "the AY1 wording 'not the whole-box K_2^+' is corrected as instructed: K_2^+ is volume-uniform and W-specific; K_2' is larger"})
    if 'certified two-sided distance' in V['selection_reason']:
        defects.append({'id': 'D6', 'field': 'selection_reason', 'defect': "'a certified two-sided distance' anticipates AY2: the AY1 gate recorded it as a labelled observation only; it is certified here under the AY2 contract"})
    relayed = {'id': 'R1', 'source': 'relayed task instruction (not contract text)', 'defect': "'ten rank-one pieces ... eigenvalues +-sqrt(10) tau/72' corrected: each piece is rank two with eigenvalues +-|tau|/144; the sum is rank two with eigenvalues +-sqrt(10) tau/144; the trace norm sqrt(10)|tau|/72 is unchanged"}
    check('contract_wording_defects_recorded', len(defects) == 6, defects=defects, relayed_instruction_correction=relayed,
          blocking=False)

    # ======================= map table in the report =======================
    def map_rows(text):
        sec = text.split('### 6.7 ', 1)
        require(len(sec) == 2, 'map section 6.7 missing')
        return [ln for ln in sec[1].split('\n### ', 1)[0].splitlines() if ln.startswith('| ')]

    def validate_map(rows):
        missing_ids = [cid for cid in V['controls'] if not any(r1.startswith('| `' + cid + '` |') for r1 in rows)]
        missing_items = [k for k in range(1, 7) if not any(r1.startswith('| item %d ' % k) for r1 in rows)]
        require(not missing_ids and not missing_items, 'map lacks rows for ' + ','.join(missing_ids + ['item %d' % k for k in missing_items]))
        return True
    mrows = map_rows(report_text)
    check('report_item_and_control_map',
          validate_map(mrows)
          and rejected(lambda: validate_map([r1 for r1 in mrows if not r1.startswith('| `root_n_misuse` |')]), 'control_row_removed_from_map')
          and rejected(lambda: validate_map([r1 for r1 in mrows if not r1.startswith('| item 4 ')]), 'item_4_row_removed_from_map'),
          controls_in_map=len(V['controls']), items_in_map=6, map_section='report.md section 6.7')

    # ======================= packet, tampering =======================
    headline = {
        'two_D': s(twoD), 'two_D_preview': dec(twoD), 'D': s(D), 'D_preview': dec(D),
        'K2_prime': s(K2p), 'K2_prime_preview': dec(K2p), 'K2_prime_tau2': s(K2p_tau2), 'K2_prime_tau2_preview': dec(K2p_tau2),
        'two_K2_prime_tau2': s(two_K2), 'two_K2_prime_tau2_preview': dec(two_K2),
        'rho1_R': '(tau/72) sum over the 10 faces with owner set R of (|W_f Omega_R><Omega_R| + h.c.)',
        'rho1_R_trace_norm': 'sqrt(10)|tau|/72', 'rho1_R_trace_norm_squared_at_cap': s(tn_sq * tau_cap ** 2),
        'rho1_R_trace_norm_bracket': [s(lo10 * tau_cap / 72), s(hi10 * tau_cap / 72)], 'rho1_R_trace_norm_preview': dec(lo10 * tau_cap / 72),
        'rho1_R_eigenvalues': '+-sqrt(10) tau/144 (simple), 0 otherwise', 'tr_rho1_W': '+tau/144',
        'tier_lower': s(lower), 'tier_lower_preview': dec(lower), 'tier_upper': s(upper), 'tier_upper_preview': dec(upper),
        'relative_width_upper': s(rel_width), 'relative_width_preview': dec(rel_width), 'target_relative_width': s(target),
        'target_met': rel_width <= target, 'margin_preview': dec(target / rel_width, 8),
        'plus_minus_tau_separation_lower': s(sep_lower), 'plus_minus_tau_separation_preview': dec(sep_lower),
        'falsifier_separation_lower': s(L_target), 'falsifier_separation_preview': dec(L_target),
        'K2_plus': s(K2plus), 'K2_plus_preview': dec(K2plus), 'ratio_K2prime_over_K2plus_preview': dec(K2p / K2plus, 8),
        'am2_floor_2rho_over_tau2_preview': dec(floor),
    }
    label_block = dict(LABEL)
    label_block.update({'lower': s(lower), 'lower_preview': dec(lower), 'upper': s(upper), 'upper_preview': dec(upper),
                        'sqrt10_enclosure': [s(lo10), s(hi10)], 'relative_width_upper': s(rel_width), 'relative_width_preview': dec(rel_width),
                        'relative_width_definition': '(upper - lower)/(sqrt10_lower |tau|/72); ideal 2K_2prime tau^2/(sqrt(10)|tau|/72) <= ' + dec(rel_width_ideal),
                        'target': s(target), 'comparator': '<=', 'target_met': rel_width <= target, 'tau': s(tau_cap), 'signs': ['+', '-'],
                        'minus_tau': 'replay of the same |tau| formula', 'statement': 'for every subsequential limit of either family: sqrt(10)|tau|/72 - K_2prime tau^2 <= ||rho_R - P_R||_1 <= sqrt(10)|tau|/72 + K_2prime tau^2'})
    verdict_line = verdict + " (forward half of a statement+skeptic loop; admission requires the skeptic's independent derivation and replays); sub-labels uniform_local_closeness_not_uniqueness, static_not_dynamic"
    packet = {
        'loop': 'AY2', 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'contribution_alias': 'HNM-AY2-F forward statement on state identification (what the AY1 closeness lemma does and does not establish) with the certified first_order_distance_from_product tier',
        'ai_assistance': 'AI-assisted forward production (a Claude model agent); correlated model-agent work, not independent human review',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha, 'ay1_gate_sha256': gate_sha,
        'model': {'model_id': V['model_id'], 'statement': V['model'], 'families': {'F1': FAMS[0], 'F2': FAMS[1]}, 'region': 'R={0,e_z}',
                  'observable_class': 'B(H_R)', 'reference': 'P_R (Haar product)', 'clock': V['clock_common'],
                  'boxes': 'centered Lambda_N=[-N,N]^3, N>=2, both families', 'tau': s(tau_cap), 'signs': ['+', '-']},
        'headline': headline, 'label': label_block, 'sub_labels': ['uniform_local_closeness_not_uniqueness', 'static_not_dynamic'],
        'obligations': obligations, 'mandatory_sentence_filled': sentence, 'error_terms_itemized': ledger,
        'states_compared': GATE['states_compared'], 'region': GATE['region'], 'topology': GATE['topology'],
        'dynamics_topology_named': GATE['dynamics_topology_named'], 'closeness_order': [1, 2],
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions'],
                       'additional': ['no identification of any limit', 'no dynamical, Euclidean-node or interaction-shift reading of the tier',
                                      'not uniform in the lattice spacing a', 'no statement outside R']},
        'contract_wording_defects': defects, 'relayed_instruction_correction': relayed,
        'routes_executed': ['forward: statement assembled from the AY1 gate constants, read as exact rationals and recomputed from the gate itemization',
                            'forward: exact rank-two verification of rho^(1)_R from the I1 geometry and SU(2) Haar orthogonality',
                            'forward: two-sided tier by the reverse triangle inequality with a directed sqrt(10) enclosure',
                            'forward: falsifying-scenario witness on H_R and the +-tau separation',
                            'forward: obligations table (six rows, all unproved) with missing premises, candidate routes and constants'],
        'routes_not_executed': ['skeptic independent derivation and replays (single_direction_independent_replay; outside this producer)'],
        'controls_deferred': {},
        'protocol_steps_outside_check_py': {'freeze_and_byte_identical_replays': 'research/round32/tools/freeze.py',
                                            'skeptic_review': 'independent derivation and replays by the skeptic'},
        'proposed_forward_verdict': verdict_line,
    }
    packet.update(FLAGS)
    packet.update(CLAIMS)

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
        validate_claims({k1: pk[k1] for k1 in CLAIMS})
        require(sorted(inv) == sorted(set(expected_inputs)), 'premise snapshot inventory incomplete')
        require(pk['ay1_gate_sha256'] == inv[P_AY1_GATE] == gate_sha, 'AY1 gate hash changed')
        require(rat(pk['headline']['K2_prime']) == K2p_g, "K_2' differs from the gate")
        lo_, up_ = tier(rat(pk['headline']['K2_prime']), lo10, hi10)
        require(rat(pk['headline']['tier_lower']) == lo_ and rat(pk['headline']['tier_upper']) == up_, 'tier ends differ from recomputation')
        require(rat(pk['headline']['relative_width_upper']) == (up_ - lo_) / centre_lo, 'relative width differs from recomputation')
        require(rat(pk['headline']['falsifier_separation_lower']) == L_target, 'falsifier separation differs')
        validate_obligations(pk['obligations'])
        hd, lb = pk['headline'], pk['label']
        require(lb['lower'] == hd['tier_lower'] and lb['upper'] == hd['tier_upper'] and lb['relative_width_upper'] == hd['relative_width_upper'],
                'label block differs from the headline')
        require(lb['sqrt10_enclosure'] == [s(lo10), s(hi10)] and lb['tier'] == 'first_order_distance_from_product', 'label enclosure or tier name changed')
        validate_label(lb)
        tc = ids['first_order_distance_tier_certified']
        require(tc['lower'] == hd['tier_lower'] and tc['upper'] == hd['tier_upper'] and tc['relative_width_upper'] == hd['relative_width_upper'],
                'tier check details differ from the headline')
        require(ids['falsifying_scenario_witness']['separation_lower'] == hd['falsifier_separation_lower'], 'falsifier details differ')
        require(ids['plus_minus_tau_separation']['separation_lower'] == hd['plus_minus_tau_separation_lower']
                and rat(hd['plus_minus_tau_separation_lower']) == lo10 * tau_cap / 36 - 2 * K2p_g * tau_cap ** 2, 'plus-minus separation differs')
        require(ids['ay1_gate_constants_recomputed']['K2_prime'] == hd['K2_prime'] and rat(hd['two_K2_prime_tau2']) == 2 * K2p_g * tau_cap ** 2
                and rat(hd['two_D']) == twoD_g, 'headline constants differ from the gate')
        ld = pk['error_terms_itemized']['second_order_remainder']
        require(rat(ld['single_state']) == K2p_g * tau_cap ** 2 and rat(ld['two_limits']) == 2 * K2p_g * tau_cap ** 2, 'ledger remainders differ')
        require(pk['proposed_forward_verdict'].startswith(forward_verdict(True, True, True, False)), 'verdict changed')
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
            if ch['id'] == 'obligations_table_complete':
                ch['passed'] = False

    def t_lower(pk, inv):
        pk['headline']['tier_lower'] = s(rat(pk['headline']['tier_lower']) + Q(1, 10 ** 20))

    def t_K2(pk, inv):
        pk['headline']['K2_prime'] = s(rat(pk['headline']['K2_prime']) / 4)

    def t_rel(pk, inv):
        pk['headline']['relative_width_upper'] = s(rat(pk['headline']['relative_width_upper']) / 2)

    def t_row(pk, inv):
        pk['obligations'] = pk['obligations'][:5]

    def t_unique(pk, inv):
        pk['uniqueness_claimed'] = True

    def t_gate(pk, inv):
        inv[P_AY1_GATE] = '0' * 64
        pk['ay1_gate_sha256'] = '0' * 64

    def t_snapshot(pk, inv):
        inv.pop(P_AY1S)

    def t_falsifier(pk, inv):
        pk['headline']['falsifier_separation_lower'] = s(two_K2 * 2)

    def t_label(pk, inv):
        pk['label']['lower'] = s(rat(pk['label']['lower']) * 2)

    def t_ledger(pk, inv):
        pk['error_terms_itemized']['second_order_remainder']['single_state'] = s(rat(pk['error_terms_itemized']['second_order_remainder']['single_state']) / 2)
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_lower), 'tier_lower_end_raised_hash_rebound')
          and rejected(tamper(t_K2), 'K2_prime_quartered_hash_rebound')
          and rejected(tamper(t_rel), 'relative_width_halved_hash_rebound')
          and rejected(tamper(t_row), 'obligation_row_removed_hash_rebound')
          and rejected(tamper(t_unique), 'uniqueness_flag_hash_rebound')
          and rejected(tamper(t_gate), 'ay1_gate_hash_replaced_hash_rebound')
          and rejected(tamper(t_snapshot), 'skeptic_ay1_snapshot_removed_hash_rebound')
          and rejected(tamper(t_falsifier), 'falsifier_separation_doubled_hash_rebound')
          and rejected(tamper(t_label), 'label_block_lower_end_doubled_hash_rebound')
          and rejected(tamper(t_ledger), 'ledger_single_state_remainder_halved_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    positive_only = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch.get('rejected_mutations')]
    require(not positive_only, 'contract controls without a damaging mutation: ' + ','.join(positive_only))
    require(not PENDING, 'rejected mutations not attached to a check')
    packet['checks'] = CHECKS
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['controls_with_damaging_mutations'] = sum(1 for ch in CHECKS if ch['id'] in V['controls'] and ch.get('rejected_mutations'))
    packet['rejected_mutations_in_control_checks'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS if ch['id'] in V['controls'])
    packet['rejected_mutation_total'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS)
    packet['check_count'] = len(CHECKS)
    require('u=s/' not in json.dumps(packet, sort_keys=True), 'forbidden normalized clock in the packet')
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
    ap = argparse.ArgumentParser(description='AY2 forward exact checker')
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
    manifest = {'loop': 'AY2', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AY2', 'direction': 'forward', 'checks': len(result['checks']),
                      'tier_lower_preview': result['headline']['tier_lower_preview'], 'tier_upper_preview': result['headline']['tier_upper_preview'],
                      'relative_width_preview': result['headline']['relative_width_preview'], 'target_met': result['headline']['target_met']},
                     sort_keys=True))


if __name__ == '__main__':
    main()
