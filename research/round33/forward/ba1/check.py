#!/usr/bin/env python3
"""BA1 forward producer: exact checks for the boundary decay of the AM2 creation
coefficients of the named construction families F1 and F2 (zero-selected patterned
family), by the diameter-weighted anchored norm with the loss charged once per
interaction term and a difference weight that grows with distance from the boundary
source set of each comparison.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production (a Claude
model agent); correlated model-agent work, not independent human review.

Standard library only (argparse, fractions, hashlib, json, math, pathlib, re, itertools).
Every admission Boolean is decided in exact Fraction arithmetic with directed
(upward) enclosures; decimal strings are truncated previews and are never read by an
admission check.  Conditions raise AdmissionError explicitly (never `assert`), so
every check stays active under `python -O`.

Usage: python3 -B check.py --output /absolute/fresh/non-existent/directory
"""
import argparse
import hashlib
import itertools
import json
import re
from fractions import Fraction as Q
from math import factorial, isqrt
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round33/contracts/ba1.json'
CONTRACT_SHA256 = '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'

P_AM2_GATE = 'research/round29/advisor/am2-gate.json'
P_AQ1_GATE = 'research/round29/advisor/aq1-gate.json'
P_AV1_GATE = 'research/round32/advisor/av1-gate.json'
P_AW1_GATE = 'research/round32/advisor/aw1-gate.json'
P_AY1_GATE = 'research/round32/advisor/ay1-gate.json'
P_AY2_GATE = 'research/round32/advisor/ay2-gate.json'
P_I1 = 'research/round21/forward/i1/report.md'
P_AM2 = 'research/round29/forward/am2/report.md'
P_AV1F = 'research/round32/forward/av1/report.md'
P_AY1F = 'research/round32/forward/ay1/report.md'
P_AY2F = 'research/round32/forward/ay2/report.md'

# sha256 of every admitted gate and of every report from which a constant is parsed,
# pinned before any evaluation (hash_binding.admitted_gate_sha256_pinned_in_check_py).
PINNED = {
    P_AM2_GATE: 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    P_AQ1_GATE: 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    P_AV1_GATE: '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    P_AW1_GATE: '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    P_AY1_GATE: 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    P_AY2_GATE: 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    P_I1: '836a4c7d421f0ddf3589c159d2f057839421532c88157a054a61b51c25c781a9',
    P_AM2: '1b58fb9c1a199f06b156d04c2a9e89f34ba63cf675a5f7c8bfc25bb568e4e019',
    P_AV1F: '7f86e941933913584de2b9e542359e4a3b3c275c1bc8623dca3c367d88437353',
    P_AY1F: '7cb1e844d75ee1f3d69de2bccb9a684c791e34bf64f3bb9e2d5061221f75dac1',
    P_AY2F: '527ce2f2700764d76f98efd245fd5f5fa95444f97ca81e323aaff48fac781e6b',
}

# Round33 forbidden-phrase list (copied from the shared infrastructure tool
# research/round33/tools/phrase_scan.py; it carries no scientific content).
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state',
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


def ceil_div(a, b):
    return -(-a // b)


def root_bracket(x, k, scale=10 ** 12):
    """Directed rational bracket [lo, hi] of the k-th root of a positive rational x (hi-lo=1/scale)."""
    x = Q(x)
    lo, hi = 0, scale
    while Q(hi, scale) ** k <= x:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if Q(mid, scale) ** k <= x:
            lo = mid
        else:
            hi = mid
    a, b = Q(lo, scale), Q(hi, scale)
    require(a ** k <= x < b ** k, 'root bracket')
    return a, b


# ---------------------------------------------------------------------------
# Contract: every target, bracket, parameter, template and control id is read from
# the sha256-bound snapshot.  The hash is verified before any evaluation.
# ---------------------------------------------------------------------------
def load_contract():
    raw = input_bytes(CONTRACT_REL)
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen BA1 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'BA1' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


def contract_values(c):
    p = c['parameters']
    pre = c['preregistration']
    sem = c['new_control_semantics']
    v = {}
    v['model'] = c['model']
    for token in ('Zero-selected patterned family', 'selected triple exactly (0,0,0)', 'both signs |tau|<=10^-8',
                  'J<=28|tau|, R=1/64, G(t)=16e^{8t}(1+10t)', 'F1 (AQ1 centered whole-star boxes Lambda_N=[-N,N]^3',
                  'F2 (I1 section 6 all-contained-face boxes with padding on the same Lambda_N)', 'N at least 2',
                  'cover R={0,e_z}', 'coefficients on supports meeting the padding vanish'):
        require(token in v['model'], 'contract model string lacks: ' + token)
    v['metric'] = p['metric']
    require('coarse l-infinity metric on factor sites' in p['metric'] and 'd_X=1' in p['metric']
            and 'an l1 reading with diameter 2 is a labelled alternative, never mixed' in p['metric']
            and 'd_inf at most d_1 at most 3 d_inf' in p['metric'], 'metric parameter')
    v['weights'] = p['weights']
    m = match(r'headline w = e\^mu = (\d+) \(q = 1/w = 1/(\d+)\); admissible w from 1 to (\d+/\d+) '
              r'\(self-map J_0 w G\(R\) at most R\); loss factor w\^\{d_X\} = w charged once per interaction term, never per creation',
              p['weights'], 'weights headline')
    v['w_head'] = rat(m.group(1))
    require(Q(1, int(m.group(2))) == 1 / v['w_head'], 'q = 1/w in the weights parameter')
    v['w_max'] = rat(m.group(3))
    v['e_beta_head'] = rat(match(r'e\^beta = (\d+) with beta at most mu', p['weights'], 'e^beta').group(1))
    require('rho_B(I) = max over p in I of d_inf(p,B)' in p['weights'], 'difference weight rho_B')
    require('the weight grows with distance from B, that is towards R' in p['weights'], 'weight direction')
    v['tau_star'] = Q(1, int(match(r'tau_star = 1/(\d+)', p['weights'], 'tau_star').group(1)))
    v['rho_head_per_tau'] = rat(match(r'rho = tau_star for the floor pair, rho = (\d+)\|tau\| for the headline pair',
                                      p['weights'], 'disc radii').group(1))
    rcp = p['rate_constant_pair']
    v['rcp'] = rcp
    v['q_head'] = rat(rcp['headline']['q'])
    v['K_head_target'] = rat(rcp['headline']['K_target'])
    v['tier_head'] = rcp['headline']['tier']
    require(v['tier_head'] == 'exact_first_order', 'headline tier frozen as exact_first_order')
    v['q_floor'] = rat(rcp['rate_floor']['q'])
    v['K_floor_target'] = rat(rcp['rate_floor']['K_target'])
    require('crude_majorant or exact_first_order' in rcp['rate_floor']['tier'], 'floor tier named by the producer')
    require(v['q_head'] == 1 / v['w_head'] and v['q_floor'] == 1 / v['w_max'], 'rates equal 1/w')
    v['tier_label_rule'] = rcp['tier_label_rule']
    v['comparisons'] = list(p['comparisons'])
    require(len(v['comparisons']) == 4, 'four comparisons')
    v['cutoff'] = p['cutoff']
    require('each on-site cutoff space Q_L' in v['cutoff'] and 'no untruncated creation expansion is asserted' in v['cutoff'], 'cutoff')
    v['window'] = p['window']
    require(v['window'].startswith('not applicable'), 'window parameter')
    v['N_min'] = int(match(r'^(\d+) ', p['N_min'], 'N_min').group(1))
    v['clock_param'] = p['clock']
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
    require(rat(m.group(1)) == v['K_head_target'] and rat(m.group(2)) == v['K_floor_target'], 'targets equal the frozen pair')
    require(tg['comparator'] == '<=', 'target comparator')
    sb = pre['scaling_brackets_per_constant']
    m = match(r'^\[(\d+),(\d+)\]', sb['K_exact_first_order_at_q_1_64'], 'headline bracket')
    v['bracket_head'] = (rat(m.group(1)), rat(m.group(2)))
    m = match(r'^\[(\d+)/(\d+), (\d+)/(\d+)\]', sb['K_floor_pair'], 'floor bracket')
    v['bracket_floor'] = (Q(int(m.group(1)), int(m.group(2))), Q(int(m.group(3)), int(m.group(4))))
    v['bracket_qmin'] = rat(match(r'^exactly (\d+) ', sb['q_min'], 'q_min bracket').group(1))
    v['template'] = pre['mandatory_sentence_template']
    v['gate_fields'] = dict(pre['gate_fields_required'])
    v['forbidden'] = list(pre['forbidden_phrasings'])
    v['error_terms'] = list(pre['error_terms_itemized'])
    v['error_terms_rule'] = pre['error_terms_rule']
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']), 'controls list equals the preregistered ids')
    require(set(sem) <= set(v['controls']), 'control semantics cover only contract controls')
    v['semantics'] = sem
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['acceptance'] = dict(c['acceptance'])
    v['shared'] = list(c['shared_premises'])
    v['forward_additional'] = list(c['forward_additional_premises'])
    v['reverse_isolation'] = c['reverse_premise_isolation']
    v['required'] = list(c['required'])
    v['tier_names'] = list(pre['tier_names_allowed'])
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['outcomes'] = list(pre['expected_outcome_types'])
    v['hash_binding'] = dict(pre['hash_binding'])
    require(all(v['hash_binding'].values()), 'hash binding requirements')
    # numbers named in control semantics (read, never typed in)
    v['global_lip_bound'] = rat(match(r'only by (\d+/\d+) with no decay', sem['global_lipschitz_not_decay'], 'no-decay bound').group(1))
    v['global_lip_const'] = rat(match(r'2J_0G\'\(R\) below (\d+/\d+)', sem['global_lipschitz_not_decay'], 'global Lipschitz').group(1))
    m = match(r'^(\d+) faces per factor, (\d+) owner sets, (\d+) meeting R, (\d+) inside R', sem['face_count_all_sites'], 'face pins')
    v['pins'] = {'per_factor': int(m.group(1)), 'owner_sets': int(m.group(2)), 'meet': int(m.group(3)), 'inside': int(m.group(4))}
    m = match(r'the loss e\^\{4 mu\} and the rate q at least 0\.(\d+) per site', sem['cardinality_weight_rate_labelled'], 'cardinality')
    v['q_card_floor_stated'] = Q(int(m.group(1)), 10 ** len(m.group(1)))
    v['qmin_stated'] = rat(match(r'\((\d+/\d+) at r = R = 1/64\)', sem['q_min_not_crossed'], 'q_min stated').group(1))
    require('per-site face sum 49|tau|/3 at most J' in sem['f2_regrouping_charged_once'], 'F2 per-site face sum')
    require('shell Lambda_{N+1} minus Lambda_N at l_inf distance N from e_z (N+1 from 0), F2 outer layer at N-1'
            in sem['boundary_distance_exact'], 'boundary distances stated')
    require('J=28|tau|, four stars' in sem['missing_incoming_stars'] and 'outgoing-star-only 7|tau|' in sem['missing_incoming_stars'],
            'incoming stars semantics')
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
    for rel in (P_AM2_GATE, P_AQ1_GATE, P_AV1_GATE, P_AW1_GATE, P_AY1_GATE, P_AY2_GATE):
        g = json.loads(read_input(rel))
        require(g.get('verdict') == 'accepted_within_scope', 'premise gate not accepted: ' + rel)
        gates[rel] = g
    am2 = read_input(P_AM2)
    m = match(r'J_0=\{(\d+)\\over(\d+)\}', am2, 'AM2 J_0')
    P['J0'] = Q(int(m.group(1)), int(m.group(2)))
    P['R'] = Q(1, int(match(r'For R=1/(\d+)', am2, 'AM2 R').group(1)))
    m = match(r"G\(R\)<(\d+)/(\d+),\\quad G'\(R\)<(\d+)", am2, 'AM2 G bounds')
    P['GR_up'] = Q(int(m.group(1)), int(m.group(2)))
    P['GpR_up'] = Q(int(m.group(3)))
    m = match(r"J_0G'\(R\)<(\d+)/(\d+),\\quad 2J_0G'\(R\)<(\d+)/(\d+)<1", am2, 'AM2 Lipschitz')
    P['JGp'] = Q(int(m.group(1)), int(m.group(2)))
    P['twoJGp'] = Q(int(m.group(3)), int(m.group(4)))
    require('L_k^{\\rm num}=16\\,8^k(1+5k/4)' in am2, 'AM2 multilinear constant')
    P['termination'] = int(match(r'zero for k>2p=(\d+)', am2, 'AM2 termination').group(1))
    require('G(t)=16 exp(8t)(1+10t)' in gates[P_AM2_GATE]['accepted'], 'AM2 gate majorant')
    av1 = read_input(P_AV1F)
    m = match(r'\\frac\{(\d+)\|\\tau\|\}\{(\d+)\}=:t_1', av1, 'AV1 t_1')
    P['t1_per_tau'] = Q(int(m.group(1)), int(m.group(2)))
    P['c1_den'] = int(match(r'c\^\{\(1\)\}_M=-\\frac\{\\tau\}\{(\d+)\}', av1, 'AV1 first-order coefficient').group(1))
    P['L_exact'] = int(match(r'For `L>=(\d+)`', av1, 'AV1 cutoff exactness').group(1))
    m = match(r'exact first-order face coefficient \|tau\|/(\d+) and the self-consistent AM2 remainder t<=t_1/\(1-(\d+)J\)',
              gates[P_AV1_GATE]['accepted'], 'AV1 gate tier ii')
    P['face_norm_den'] = int(m.group(1))
    P['GpR_av1'] = Q(int(m.group(2)))
    require('c^(1)=L_0=-(tau/72) sum W_f Omega_0' in gates[P_AW1_GATE]['accepted'], 'AW1 gate first-order coefficient')
    ay1g = gates[P_AY1_GATE]['accepted']
    require('F2 retains 28N(5N+1) boundary faces more than F1, and both retain the same 82 faces meeting R for N>=2' in ay1g, 'AY1 28N(5N+1)')
    m = match(r'per-site sum J<=(\d+)\|tau\|=J_0=(\d+)/(\d+)', ay1g, 'AY1 J')
    P['J_per_tau'] = Q(int(m.group(1)))
    require(Q(int(m.group(2)), int(m.group(3))) == P['J0'], 'AY1 J_0 equals AM2 J_0')
    require('|X|<=4, termination order 8' in ay1g, 'AY1 supports and termination')
    require('28N(5N+1) boundary faces at distance N-1' in gates[P_AY2_GATE]['accepted'], 'AY2 source statement')
    require("the AM2 contraction constant 2J_0G'(R)<77/390625 is a global Lipschitz bound and does not by itself give decay in distance"
            in read_input(P_AY2F), 'AY2 global Lipschitz remark')
    require('centered full-Z3 whole-star boxes have a subsequence' in gates[P_AQ1_GATE]['accepted'], 'AQ1 family F1')
    require('contains ten actual omitted faces' in read_input(P_I1), 'I1 section 6 example')
    require('F2 = I1 all-contained-face boxes with padding' in gates[P_AY1_GATE]['model'], 'AY1 family F2')
    # internal consistency of the parsed constants
    require(P['GpR_av1'] == P['GpR_up'], 'AV1 352 equals AM2 G\'(R) bound')
    require(P['J0'] * P['GpR_up'] == P['JGp'] and 2 * P['JGp'] == P['twoJGp'], 'AM2 Lipschitz constants')
    require(P['J_per_tau'] * Q(1, 10 ** 8) == P['J0'], 'J_0 = 28|tau| at the cap')
    require(P['c1_den'] == 72 and P['face_norm_den'] == 144 and P['t1_per_tau'] == Q(49, 144), 'first-order pins')
    P['gates'] = gates
    return P


# ---------------------------------------------------------------------------
# Fine-lattice geometry and the I1 anchored face table (parsed from the I1 snapshot).
# ---------------------------------------------------------------------------
E_UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
COVER_R = (ORIGIN, EZ)
TOKEN = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}


def add(p, q):
    return tuple(a + b for a, b in zip(p, q))


def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def d_inf(p, q):
    return max(abs(a - b) for a, b in zip(p, q))


def d_one(p, q):
    return sum(abs(a - b) for a, b in zip(p, q))


def diam(A, metric):
    A = list(A)
    return max((metric(a, b) for a in A for b in A), default=0)


def dist_set(A, B, metric):
    return min(metric(a, b) for a in A for b in B)


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    return ((p, a), (add(p, E_UNIT[a]), c), (add(p, E_UNIT[c]), a), (p, c))


def face_support(p, a, c):
    return frozenset(owner(link[0]) for link in face_links(p, a, c))


def is_selected(p, a, c):
    return (a, c) == (0, 1) and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


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


def coarse_box(N):
    rng = range(-N, N + 1)
    return frozenset(itertools.product(rng, rng, rng))


def shell(N):
    return coarse_box(N + 1) - coarse_box(N)


def outer_layer(N):
    return frozenset(x for x in coarse_box(N) if max(abs(c) for c in x) == N)


def family_faces(N, omitted, family, box=None):
    """F1: whole stars b+S inside the volume (AQ1).  F2: every omitted face whose owner set lies in it (I1 section 6)."""
    bx = coarse_box(N) if box is None else box
    out = []
    for b in sorted(bx):
        whole = all(add(b, d) in bx for d in S_STAR)
        for k, cls in enumerate(omitted):
            M = frozenset(add(b, d) for d in cls[3])
            if family == 'F1':
                if whole:
                    out.append((b, k, M))
            elif family == 'F2':
                if M <= bx:
                    out.append((b, k, M))
            else:
                raise AdmissionError('unknown family ' + str(family))
    return out


def group_terms(faces):
    """Anchor grouping: term support = union of retained owner sets (actual-support convention), face count."""
    g = {}
    for b, k, M in faces:
        sup, n = g.get(b, (frozenset(), 0))
        g[b] = (sup | M, n + 1)
    return g


def per_site_counts(sets):
    cnt = {}
    for X in sets:
        for x in X:
            cnt[x] = cnt.get(x, 0) + 1
    return cnt


def order_distance_table(terms, metric, diam_c):
    """Least tree order at which a term at distance d from R can reach a coefficient meeting R."""
    keys = sorted(terms)
    inc = {}
    for b in keys:
        for x in sorted(terms[b]):
            inc.setdefault(x, []).append(b)
    rset = set(COVER_R)
    dist = {}
    queue = []
    for b in keys:
        if terms[b] & rset:
            dist[b] = 0
            queue.append(b)
    i = 0
    while i < len(queue):
        b = queue[i]
        i += 1
        for x in sorted(terms[b]):
            for b2 in inc[x]:
                if b2 not in dist:
                    dist[b2] = dist[b] + 1
                    queue.append(b2)
    require(len(dist) == len(keys), 'overlap graph of the terms is connected')
    rows = {}
    for b in keys:
        d = dist_set(terms[b], COVER_R, metric)
        rows.setdefault(d, []).append(dist[b] + 1)
    table = []
    for d in sorted(rows):
        orders = rows[d]
        c = ceil_div(d, diam_c)
        require(min(orders) >= 1 + c, 'order-versus-distance lemma violated at distance %d' % d)
        table.append({'distance': d, 'terms': len(orders), 'min_order': min(orders), 'max_order': max(orders),
                      'bound_one_plus_ceil': 1 + c, 'contract_ceil_d_over_diam': c, 'attained': min(orders) == 1 + c})
    return table


OVD_KEYS = (('F1', 2), ('F1', 3), ('F1', 4), ('F2', 2), ('F2', 3), ('F2', 4))


def render_ovd_rows(tables, diam_c):
    ds = sorted(set(r['distance'] for key in OVD_KEYS for r in tables[key]))
    lines = []
    for d in ds:
        cells = []
        for key in OVD_KEYS:
            row = [r for r in tables[key] if r['distance'] == d]
            cells.append('%d/%d' % (row[0]['terms'], row[0]['min_order']) if row else '-')
        lines.append('| %d | %d | %s |' % (d, 1 + ceil_div(d, diam_c), ' | '.join(cells)))
    return lines


# ---------------------------------------------------------------------------
# AM2 constants re-derived exactly; the weighted majorant; tiers and routes.
# ---------------------------------------------------------------------------
def exp_eighth_bracket():
    """e^{1/8} bracket: partial sum to k=12 (lower) plus a geometric tail bound (upper)."""
    x = Q(1, 8)
    partial = sum(x ** k / factorial(k) for k in range(13))
    tail = x ** 13 / factorial(13) / (1 - x / 14)
    return partial, partial + tail


def Lnum(k, p=4):
    """Itemized AM2 multilinear constant: 2^p output sets, 2^k products, p^k collection sums, root placements."""
    return Q(2 ** p) * Q(2 * p) ** k * (1 + Q(k * (p + 1), p))


def taylor_G(k):
    """k-th Taylor coefficient of G(t)=16 e^{8t}(1+10t), times k!."""
    val = Q(16) * Q(8) ** k
    if k >= 1:
        val += Q(16) * 10 * k * Q(8) ** (k - 1)
    return val


TIERS = ('crude_majorant', 'exact_first_order')
ROUTES = ('weighted_norm', 'analytic_disc')


def assemble_tier(tier, route, components):
    require(tier in TIERS, 'tier outside the closed vocabulary: ' + str(tier))
    require(route in ROUTES, 'route outside the closed vocabulary: ' + str(route))
    require(route == 'weighted_norm', 'the forward producer executes only the weighted_norm route')
    for name, label, value in components:
        require(label in TIERS, 'component tier outside the closed vocabulary: ' + name)
        require(isinstance(value, Q) and value >= 0, 'non-exact or negative component ' + name)
    # exact_first_order only when every component is exact first order; any crude component makes it crude_majorant
    derived = 'exact_first_order' if all(label == 'exact_first_order' for _, label, _ in components) else 'crude_majorant'
    require(derived == tier, 'tier mixing rejected: components give ' + derived + ' but the constant is labelled ' + tier)
    return True


def weighted_pair(tau, w, e_beta, tier, C, route='weighted_norm', t_label=None, source_label=None, self_consistent=True,
                  J_per_tau=None):
    """Coefficient-difference constants in the diameter-weighted norm at weight w and difference weight e^beta.

    Returns, per comparison, K in `sum_{I ni u} ||c_I-c'_I|| <= K q^(N-1)` (u in R), q=1/e^beta.
    """
    tau = rat(tau)
    w = rat(w)
    e_beta = rat(e_beta)
    require(w >= 1 and 1 <= e_beta <= w, 'weights: 1 <= e^beta <= w (beta at most mu)')
    J = (C['J_per_tau'] if J_per_tau is None else J_per_tau) * abs(tau)
    GR, GpR, R = C['GR_up'], C['GpR_up'], C['R']
    selfmap = J * w * GR
    require(selfmap <= R, 'weighted self-map J w G(R) at most R fails at w=' + s(w))
    gam_w = J * w * GpR
    gam_b = J * e_beta * GpR
    require(gam_w < 1 and gam_b < 1, 'weighted Lipschitz factor below one')
    t1 = C['t1_per_tau'] * abs(tau)
    t_label = tier if t_label is None else t_label
    source_label = tier if source_label is None else source_label
    if t_label == 'exact_first_order':
        T = w * t1 / (1 - gam_w) if self_consistent else w * t1
        require(self_consistent, 'exact first-order tier requires the self-consistent inequality t_w at most w t_1/(1-J w G\'(R))')
    else:
        T = selfmap
    require(T <= R, 'weighted fixed point stays in the ball')
    if source_label == 'exact_first_order':
        first = e_beta * t1
        remainder = gam_b * T
        S = first + remainder
    else:
        first = e_beta * J * 16
        remainder = e_beta * J * (GR - 16)
        S = e_beta * J * GR
    assemble_tier(tier, route, [('t_w', t_label, T), ('source', source_label, S)])
    q = 1 / e_beta
    K_own = S / (1 - gam_b)
    K12 = K_own
    Kn = q * K_own
    Kgen = K12 + Kn / (1 - q)
    return {'tau': tau, 'w': w, 'e_beta': e_beta, 'q': q, 'tier': tier, 'route': route, 'J': J, 'selfmap': selfmap,
            'Gamma_w': gam_w, 'Gamma_beta': gam_b, 't1': t1, 'T_w': T, 'source_first_order': first,
            'source_remainder': remainder, 'source': S, 'K_own': K_own, 'K_F1_vs_F2': K12, 'K_nested': Kn,
            'K_general_telescoping': Kgen, 'K_general_direct': K12 + Kn, 'K_union': 2 * Kn,
            'K_pair': max(K12, Kn, Kgen)}


def pair_record(d):
    out = {}
    for k in ('w', 'e_beta', 'q', 'J', 'selfmap', 'Gamma_w', 'Gamma_beta', 't1', 'T_w', 'source_first_order',
              'source_remainder', 'source', 'K_own', 'K_F1_vs_F2', 'K_nested', 'K_general_telescoping',
              'K_general_direct', 'K_union', 'K_pair'):
        out[k] = s(d[k])
        out[k + '_preview'] = dec(d[k])
    out['tier'] = d['tier']
    out['route'] = d['route']
    out['tau'] = s(d['tau'])
    return out


# ---------------------------------------------------------------------------
# Exact qubit creation-algebra engine (finite fixtures only; transfers_to_aq false).
# Basis states are frozensets of excited sites; h_x = Q_x so H_M = |M| on sector M.
# ---------------------------------------------------------------------------
def q_add(u, v, c=Q(1)):
    out = dict(u)
    for k, a in v.items():
        out[k] = out.get(k, Q(0)) + c * a
    return {k: a for k, a in out.items() if a != 0}


def q_create(I, gamma):
    I = frozenset(I)

    def op(vec):
        return {E | I: gamma * a for E, a in vec.items() if not (E & I)}
    return op


def q_flip(X, coef):
    X = frozenset(X)

    def op(vec):
        return {E ^ X: coef * a for E, a in vec.items()}
    return op


def q_word(creators, V, vec):
    """ad_{C_1} ... ad_{C_k}(V) applied to vec (creations commute)."""
    if not creators:
        return V(vec)
    C = creators[0]
    return q_add(C(q_word(creators[1:], V, vec)), q_word(creators[1:], V, C(vec)), Q(-1))


def q_Lk(creators, V):
    out = q_word(creators, V, {frozenset(): Q(1)})
    return {M: a / len(M) for M, a in out.items() if M}


def q_weighted_norm(coll, w, metric=d_inf):
    sites = set()
    for M in coll:
        sites |= set(M)
    return max((sum((Q(w) ** diam(M, metric)) * abs(a) for M, a in coll.items() if u in M) for u in sites), default=Q(0))


def q_ground(creations):
    vec = {frozenset(): Q(1)}
    for I, g in creations:
        vec = q_add(vec, q_create(I, g)(vec), Q(-1))
    return vec


def q_reduced_one_site(vec, r):
    groups = {}
    for E, a in vec.items():
        x = 1 if r in E else 0
        groups.setdefault(E - {r}, [Q(0), Q(0)])[x] += a
    rho = [[Q(0), Q(0)], [Q(0), Q(0)]]
    for amps in groups.values():
        for i in range(2):
            for j in range(2):
                rho[i][j] += amps[i] * amps[j]
    z = rho[0][0] + rho[1][1]
    return [[rho[i][j] / z for j in range(2)] for i in range(2)]


def solve_linear(A, b):
    """Exact Gaussian elimination for (I - A) x = b."""
    n = len(b)
    M = [[(Q(1) if i == j else Q(0)) - A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col] / M[col][col]
                M[r] = [a - f * c for a, c in zip(M[r], M[col])]
    return [M[i][n] / M[i][i] for i in range(n)]


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
# Main computation.
# ---------------------------------------------------------------------------
def compute(check_sha):
    contract, contract_digest = load_contract()          # sha256 verified before any evaluation
    V = contract_values(contract)
    check('contract_snapshot_sha256', contract_digest == CONTRACT_SHA256, contract_sha256=contract_digest,
          check_py_sha256_recorded_before_evaluation=check_sha)
    P = load_premises()
    check('premise_gates_pinned_and_parsed', True, pinned_sha256=P['pinned_sha256'],
          parsed={'J_0': s(P['J0']), 'R': s(P['R']), 'G_R_upper': s(P['GR_up']), 'Gprime_R_upper': s(P['GpR_up']),
                  'J0_Gprime_R': s(P['JGp']), 'two_J0_Gprime_R': s(P['twoJGp']), 'termination_order': P['termination'],
                  't1_per_abs_tau': s(P['t1_per_tau']), 'first_order_face_coefficient': '-tau/%d' % P['c1_den'],
                  'first_order_face_norm': '|tau|/%d' % P['face_norm_den'], 'cutoff_exact_from_L': P['L_exact'],
                  'J_per_abs_tau': s(P['J_per_tau'])})
    tau_cap = V['tau']
    require(P['J_per_tau'] * tau_cap == P['J0'], 'contract tau cap equals the AM2 cap')

    # ---------------- geometry: I1 table, supports, counts --------------------------------------
    classes = parse_i1_table(read_input(P_I1))
    omitted = [c for c in classes if c[4] == 'omitted']
    selected = [c for c in classes if c[4] == 'selected']
    require(len(classes) == 24 and len(omitted) == 21 and len(selected) == 3, 'I1 24 = 3 selected + 21 omitted')
    union_support = frozenset().union(*[c[3] for c in omitted])
    require(union_support == frozenset(S_STAR), 'union of omitted supports is the star S')
    # brute force: every class support re-derived from I1.4 at several anchors (negative coordinates included)
    for anchor in ((0, 0, 0), (-3, 2, -1), (5, -4, 7)):
        for cls in classes:
            base = (4 * anchor[0] + cls[1], 2 * anchor[1] + cls[2], anchor[2])
            a, cc = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}[cls[0]]
            require(face_support(base, a, cc) == frozenset(add(anchor, d) for d in cls[3]), 'I1.4 support re-derived')
            require(is_selected(base, a, cc) == (cls[4] == 'selected'), 'selected role re-derived')
    per_offset = {d: sum(1 for c in omitted if d in c[3]) for d in S_STAR}
    per_factor = sum(per_offset.values())
    owner_sets_0 = set()
    for c in omitted:
        for d in c[3]:
            owner_sets_0.add(frozenset(sub(x, d) for x in c[3]))
    both = sum(1 for c in omitted if EZ in c[3])          # faces containing 0 and e_z are anchored at 0 with e_z in K
    meet = 2 * per_factor - both
    inside = sum(1 for c in omitted if c[3] == frozenset(COVER_R))
    pins = {'per_factor': per_factor, 'owner_sets': len(owner_sets_0), 'meet': meet, 'inside': inside}
    # brute-force fine-lattice count, without the class table
    bf_meet = set()
    bf_per0 = set()
    for x in range(-8, 8):
        for y in range(-4, 4):
            for z in range(-2, 3):
                for a, cc in ((0, 1), (0, 2), (1, 2)):
                    p = (x, y, z)
                    if is_selected(p, a, cc):
                        continue
                    M = face_support(p, a, cc)
                    if ORIGIN in M:
                        bf_per0.add((p, a, cc))
                    if M & set(COVER_R):
                        bf_meet.add((p, a, cc))
    require(len(bf_per0) == per_factor and len(bf_meet) == meet, 'brute-force face counts agree with translation covariance')
    require(pins == V['pins'], 'derived face pins equal the contract pins')

    # ---------------- AM2 constants re-derived ----------------------------------------------------
    e_lo, e_up = exp_eighth_bracket()
    R = P['R']
    GR_true_up = 16 * e_up * (1 + 10 * R)
    GpR_true_up = 16 * e_up * (18 + 80 * R)
    GR_true_lo = 16 * e_lo * (1 + 10 * R)
    require(e_up < Q(8, 7) and GR_true_up < P['GR_up'] and GpR_true_up < P['GpR_up'], 'directed enclosure e^{1/8} < 8/7')
    for k in range(0, 9):
        require(Lnum(k) == 16 * Q(8) ** k * (1 + Q(5 * k, 4)) == taylor_G(k), 'L_k^num itemization at k=%d' % k)
    require(P['termination'] == 2 * 4, 'termination order 2p=8')
    C = {'J_per_tau': P['J_per_tau'], 'GR_up': P['GR_up'], 'GpR_up': P['GpR_up'], 'R': R, 't1_per_tau': P['t1_per_tau']}
    check('am2_constants_reverified', True, exp_eighth_upper=s(e_up), exp_eighth_lower=s(e_lo),
          G_R_upper_used=s(P['GR_up']), Gprime_R_upper_used=s(P['GpR_up']), G_R_lower=s(GR_true_lo),
          Lnum_itemized='2^p (2p)^k (1 + k(p+1)/p) = 16 8^k (1+5k/4) = k! [t^k] G, k=0..8, p=4')

    # ---------------- item 1: weighted multilinear estimate and weighted contraction --------------
    # itemization of the weighted estimate: output sets, products, collection sums, the loss per interaction
    item_rows = []
    for k in range(0, 9):
        root_in_X = Q(2 ** 4) * Q(2) ** k * Q(4) ** k
        root_in_I = Q(2 ** 4) * Q(2) ** k * k * 5 * Q(4) ** max(k - 1, 0) if k >= 1 else Q(0)
        require(root_in_X + root_in_I == Lnum(k), 'root placements add to L_k^num at k=%d' % k)
        item_rows.append({'k': k, 'root_in_X': s(root_in_X), 'root_in_creation': s(root_in_I), 'Lnum': s(Lnum(k)),
                          'loss_factor': 'w^{d_X} <= w, once per L_k (independent of k)'})
    w_max = V['w_max']
    require(w_max == P['R'] / (P['J0'] * P['GR_up']), 'w_max = R/(J_0 G(R)) with the admitted G(R) bound')
    grid = [Q(1), Q(2), Q(8), V['w_head'], Q(512), w_max]
    rows = []
    for w in grid:
        sm = P['J0'] * w * P['GR_up']
        lip = P['J0'] * w * P['GpR_up']
        require(sm <= R and lip < 1, 'weighted self-map and Lipschitz at w=' + s(w))
        rows.append({'w': s(w), 'selfmap_J0_w_G_R': s(sm), 'lipschitz_J0_w_Gprime_R': s(lip), 'lipschitz_preview': dec(lip)})
    lip_max = P['J0'] * w_max * P['GpR_up']
    require(lip_max == Q(77, 296) and P['J0'] * w_max * P['GR_up'] == R, 'cap values at w_max')
    check('weighted_multilinear_estimate_and_contraction', True, itemization=item_rows, weight_grid=rows,
          w_max=s(w_max), lipschitz_at_w_max=s(lip_max),
          statement="||L_k(c_1..c_k)||_w at most w J L_k^num prod ||c_j||_w; ||Phi(c)||_w at most J w G(||c||_w); "
                    "Lipschitz J w G'(R) on the weighted R-ball; the weighted ball lies in the unweighted AM2 ball (w at least 1), "
                    "so the weighted fixed point is the AM2 fixed point")

    # ---------------- item 2: diameters, incidence, order-versus-distance tables -------------------
    SS = [sub(a, b) for a in S_STAR for b in S_STAR]
    require(max(d_inf(x, ORIGIN) for x in SS) == 1 and max(d_one(x, ORIGIN) for x in SS) == 2, 'S-S all-size diameters')
    diam_audit = {}
    for N in (2, 3):
        for fam in ('F1', 'F2'):
            fs = family_faces(N, omitted, fam)
            terms = group_terms(fs)
            require(all(diam(M, d_inf) == 1 for _, _, M in fs), 'every owner set has l_inf diameter 1')
            require(all(diam(M, d_one) in (1, 2) for _, _, M in fs), 'owner-set l1 diameters in {1,2}')
            require(all(diam(X, d_inf) <= 1 for X, _ in terms.values()), 'every term has l_inf diameter at most 1')
            if fam == 'F1':
                require(all(X == frozenset(add(b, d) for d in S_STAR) for b, (X, _) in terms.items()), 'F1 terms are whole stars')
                require(all(diam(X, d_inf) == 1 and diam(X, d_one) == 2 for X, _ in terms.values()), 'star diameters 1 and 2')
            cnt = per_site_counts([X for X, _ in terms.values()])
            require(max(cnt.values()) == 4, 'at most four terms per site (incoming anchors included)')
            fcnt = per_site_counts([M for _, _, M in fs])
            require(max(fcnt.values()) == per_factor, 'bulk per-site face count 49 attained')
            diam_audit['%s_N%d' % (fam, N)] = {'terms': len(terms), 'faces': len(fs), 'max_terms_per_site': max(cnt.values()),
                                               'max_faces_per_site': max(fcnt.values()), 'term_linf_diam_max': 1}
    ovd = {'l_inf': {}, 'l1': {}}
    for fam, N in OVD_KEYS:
        terms = {b: X for b, (X, _) in group_terms(family_faces(N, omitted, fam)).items()}
        ovd['l_inf'][(fam, N)] = order_distance_table(terms, d_inf, 1)
        ovd['l1'][(fam, N)] = order_distance_table(terms, d_one, 2)
    ovd_rows = {'l_inf': render_ovd_rows(ovd['l_inf'], 1), 'l1': render_ovd_rows(ovd['l1'], 2)}
    sharp_linf = all(r['attained'] for key in OVD_KEYS for r in ovd['l_inf'][key] if r['distance'] <= key[1] - 1)
    require(sharp_linf, 'l_inf bound attained for every distance up to N-1')
    check('diameter_convention_and_order_versus_distance', True, diameter_audit=diam_audit,
          convention_used_in_proof='coarse l_inf, d_X=1', labelled_alternative='l1, d_X=2 (never mixed)',
          ovd_rows_l_inf=ovd_rows['l_inf'], ovd_rows_l1=ovd_rows['l1'],
          lemma='a coefficient on a support meeting R depends on a term at distance d from R only at order at least 1+ceil(d/diam) (hence at least ceil(d/diam))',
          l_inf_bound_attained_for_d_up_to_N_minus_1=sharp_linf)

    # ---------------- item 3: boundary sources, exact distances ----------------------------------
    src = {}
    for N in (2, 3, 4):
        bxA, bxB = coarse_box(N), coarse_box(N + 1)
        F1a = family_faces(N, omitted, 'F1')
        F1b = family_faces(N + 1, omitted, 'F1')
        F2a = family_faces(N, omitted, 'F2')
        F2b = family_faces(N + 1, omitted, 'F2')
        sF1a = set((b, k) for b, k, _ in F1a)
        sF1b = set((b, k) for b, k, _ in F1b)
        sF2a = set((b, k) for b, k, _ in F2a)
        sF2b = set((b, k) for b, k, _ in F2b)
        Mof = {(b, k): M for b, k, M in F2b}
        Mof.update({(b, k): M for b, k, M in F2a})
        require(sF1a <= sF1b and sF2a <= sF2b and sF1a <= sF2a and sF1b <= sF2b, 'old terms retained in the larger volume')
        SH, LY = shell(N), outer_layer(N)
        dmap = {}

        def dB(x, B, tag):
            key = (x, tag)
            if key not in dmap:
                dmap[key] = min(d_inf(x, y) for y in B)
            return dmap[key]
        starsA = set(b for b in bxA if all(add(b, d) in bxA for d in S_STAR))
        starsB = set(b for b in bxB if all(add(b, d) in bxB for d in S_STAR))
        new_stars = sorted(starsB - starsA)
        require(len(new_stars) == (2 * N + 2) ** 3 - (2 * N) ** 3, 'new F1 star count')
        star_sup = {b: frozenset(add(b, d) for d in S_STAR) for b in new_stars}
        require(all(star_sup[b] & SH for b in new_stars), 'every new F1 star meets the shell')
        rho_F1 = max(max(dB(x, SH, 'sh') for x in star_sup[b]) for b in new_stars)
        new_faces_F1 = sorted(sF1b - sF1a)
        require(set(new_faces_F1) == set((b, k) for b in new_stars for k in range(21)), 'F1 source = faces of new stars only')
        c_F1 = per_site_counts([Mof[f] for f in new_faces_F1])
        stars_per_site = per_site_counts(star_sup.values())
        met_sites = frozenset().union(*star_sup.values())
        new_faces_F2 = sorted(sF2b - sF2a)
        require(all(Mof[f] & SH for f in new_faces_F2), 'every new F2 face meets the shell')
        rho_F2 = max(max(dB(x, SH, 'sh') for x in Mof[f]) for f in new_faces_F2)
        c_F2 = per_site_counts([Mof[f] for f in new_faces_F2])
        # regrouping: faces at each anchor of the larger F2 box = old faces + new faces, disjointly
        by_anchor_old, by_anchor_new, by_anchor_big = {}, {}, {}
        for (b, k) in sF2a:
            by_anchor_old.setdefault(b, set()).add(k)
        for (b, k) in new_faces_F2:
            by_anchor_new.setdefault(b, set()).add(k)
        for (b, k) in sF2b:
            by_anchor_big.setdefault(b, set()).add(k)
        for b in by_anchor_big:
            o, n = by_anchor_old.get(b, set()), by_anchor_new.get(b, set())
            require(not (o & n) and (o | n) == by_anchor_big[b], 'F2 regrouping charges each face once')
        gained = sorted(b for b in by_anchor_old if b in by_anchor_new)
        extra = sorted(sF2a - sF1a)
        require(len(extra) == 28 * N * (5 * N + 1), 'F1 versus F2 extra faces 28N(5N+1)')
        require(all(Mof[f] <= LY and Mof[f] & LY for f in extra), 'extra F2 faces lie in the outer layer')
        require(all(all(x[i] == N for x in Mof[f]) for f in extra for i in [next(i for i in range(3) if f[0][i] == N)]),
                'extra faces sit on the positive outer faces')
        c_ext = per_site_counts([Mof[f] for f in extra])
        # per-site J (face units |tau|/3) of the mixed decompositions of the larger interaction
        J_units = {}
        for tag, oldterms, newterms in (
                ('F1_nested', [(frozenset(add(b, d) for d in S_STAR), 21) for b in sorted(starsA)],
                 [(star_sup[b], 21) for b in new_stars]),
                ('F2_nested', [(X, n) for X, n in group_terms(F2a).values()], [(Mof[f], 1) for f in new_faces_F2]),
                ('F1_vs_F2', [(frozenset(add(b, d) for d in S_STAR), 21) for b in sorted(starsA)], [(Mof[f], 1) for f in extra])):
            load = {}
            for X, n in oldterms + newterms:
                for x in X:
                    load[x] = load.get(x, 0) + n
            J_units[tag] = max(load.values())
            require(J_units[tag] <= 84, 'per-site sum of the mixed decomposition at most 28|tau| (' + tag + ')')
        dist = {'shell_from_0': min(d_inf(ORIGIN, y) for y in SH), 'shell_from_e_z': min(d_inf(EZ, y) for y in SH),
                'layer_from_0': min(d_inf(ORIGIN, y) for y in LY), 'layer_from_e_z': min(d_inf(EZ, y) for y in LY),
                'shell_from_e_z_l1': min(d_one(EZ, y) for y in SH), 'layer_from_e_z_l1': min(d_one(EZ, y) for y in LY),
                'met_sites_from_e_z': min(d_inf(EZ, y) for y in met_sites)}
        require(dist['shell_from_0'] == N + 1 and dist['shell_from_e_z'] == N and dist['layer_from_0'] == N
                and dist['layer_from_e_z'] == N - 1 and dist['shell_from_e_z_l1'] == N and dist['layer_from_e_z_l1'] == N - 1,
                'exact boundary distances at N=%d' % N)
        require(dist['met_sites_from_e_z'] == N - 1 and len(met_sites & bxA) > 0, 'new F1 stars also meet outer-layer sites of Lambda_N')
        src[N] = {'F1_nested_new_stars': len(new_stars), 'F1_nested_new_faces': len(new_faces_F1),
                  'F1_nested_rho_B_max': rho_F1, 'F1_nested_new_faces_per_site_max': max(c_F1.values()),
                  'F1_nested_new_stars_per_site_max': max(stars_per_site.values()),
                  'F1_nested_sites_met_inside_Lambda_N': len(met_sites & bxA),
                  'F2_nested_new_faces': len(new_faces_F2), 'F2_nested_rho_B_max': rho_F2,
                  'F2_nested_new_faces_per_site_max': max(c_F2.values()), 'F2_nested_groups_gaining_faces': len(gained),
                  'F1_vs_F2_extra_faces': len(extra), 'F1_vs_F2_formula_28N_5N_plus_1': 28 * N * (5 * N + 1),
                  'F1_vs_F2_rho_B_max': max(max(dB(x, LY, 'ly') for x in Mof[f]) for f in extra),
                  'F1_vs_F2_extra_faces_per_site_max': max(c_ext.values()),
                  'per_site_J_face_units_of_mixed_decomposition': J_units, 'distances': dist}
        require(src[N]['F1_vs_F2_rho_B_max'] == 0 and rho_F1 == 1 and rho_F2 == 1, 'source loss exponents rho_B')
        require(max(c_F1.values()) <= per_factor and max(c_F2.values()) <= per_factor and max(c_ext.values()) <= per_factor,
                'new faces per site at most 49')
    # all-size count of the extra F2 faces from the class table: anchors with A={i: b_i=N} nonempty
    def extra_formula(N):
        tot = 0
        for r in range(1, 4):
            for A in itertools.combinations(range(3), r):
                avoid = sum(1 for c in omitted if not any(E_UNIT[i] in c[3] for i in A))
                tot += (2 * N) ** (3 - r) * avoid
        return tot
    require(all(extra_formula(N) == 28 * N * (5 * N + 1) for N in range(2, 30)), 'all-size 28N(5N+1) from the class table')
    require(all(extra_formula(N) == src[N]['F1_vs_F2_extra_faces'] for N in (2, 3, 4)), 'formula equals enumeration')
    check('boundary_sources_enumerated', True, sources=src,
          source_sets={'F1 N vs N+1': 'shell Lambda_{N+1} minus Lambda_N (every new star meets it)',
                       'F2 N vs N+1': 'shell Lambda_{N+1} minus Lambda_N (every new face meets it)',
                       'F1 vs F2 same N': 'outer layer max|b_i|=N of Lambda_N (every extra face lies in it)',
                       'general': 'telescoping plus the same-N comparison; union comparison labelled'},
          all_size_extra_faces='sum over nonempty A of (2N)^(3-|A|) times the classes avoiding e_i, i in A: 140N^2+28N=28N(5N+1)')

    # ---------------- item 4: the constants ------------------------------------------------------
    taus = {'+': tau_cap, '-': -tau_cap}
    head = {sg: weighted_pair(t, V['w_head'], V['e_beta_head'], 'exact_first_order', C) for sg, t in taus.items()}
    floor = {sg: weighted_pair(t, w_max, w_max, 'exact_first_order', C) for sg, t in taus.items()}
    head_crude = {sg: weighted_pair(t, V['w_head'], V['e_beta_head'], 'crude_majorant', C) for sg, t in taus.items()}
    floor_crude = {sg: weighted_pair(t, w_max, w_max, 'crude_majorant', C) for sg, t in taus.items()}
    for d in list(head.values()) + list(floor.values()) + list(head_crude.values()) + list(floor_crude.values()):
        require(d['K_pair'] == d['K_general_telescoping'], 'the general comparison is the largest constant')
    Kh, Kf = head['+']['K_pair'], floor['+']['K_pair']
    require(head['+'] == dict(head['-'], tau=tau_cap) and floor['+'] == dict(floor['-'], tau=tau_cap), 'both signs identical (|tau| only)')
    head_met = Kh <= V['K_head_target']
    floor_met = Kf <= V['K_floor_target']
    floor_crude_met = floor_crude['+']['K_pair'] <= V['K_floor_target']
    head_crude_met = head_crude['+']['K_pair'] <= V['K_head_target']
    require(head_met and floor_met and floor_crude_met and not head_crude_met, 'target outcomes')
    require(head['+']['q'] == V['q_head'] and floor['+']['q'] == V['q_floor'], 'rates equal the frozen pair')
    # the q^(N-1) statement per comparison at each u in R, verified against the enumerated distances
    for N in (2, 3, 4):
        dist = src[N]['distances']
        for d in (head['+'], floor['+']):
            q = d['q']
            for u_key, dn, dl in (('e_z', dist['shell_from_e_z'], dist['layer_from_e_z']), ('0', dist['shell_from_0'], dist['layer_from_0'])):
                require(d['K_own'] * q ** dn <= d['K_nested'] * q ** (N - 1), 'nested bound at exponent N')
                require(d['K_own'] * q ** dl <= d['K_F1_vs_F2'] * q ** (N - 1), 'F1/F2 bound at exponent N-1')
    check('coefficient_difference_headline_pair', head_met, tier='exact_first_order', route='weighted_norm',
          q=s(V['q_head']), K_target=s(V['K_head_target']), K_pair=s(Kh), K_pair_preview=dec(Kh),
          margin_preview=dec(V['K_head_target'] / Kh, 6), per_sign={sg: pair_record(d) for sg, d in head.items()})
    check('coefficient_difference_floor_pair', floor_met and floor_crude_met, tier_named='exact_first_order', route='weighted_norm',
          q=s(V['q_floor']), K_target=s(V['K_floor_target']), K_pair=s(Kf), K_pair_preview=dec(Kf),
          margin_preview=dec(V['K_floor_target'] / Kf, 6), crude_tier_K_pair=s(floor_crude['+']['K_pair']),
          crude_tier_K_pair_preview=dec(floor_crude['+']['K_pair']),
          crude_tier_margin_preview=dec(V['K_floor_target'] / floor_crude['+']['K_pair'], 6),
          per_sign={sg: pair_record(d) for sg, d in floor.items()},
          per_sign_crude={sg: pair_record(d) for sg, d in floor_crude.items()})
    check('crude_tier_reported_separately', not head_crude_met, tier='crude_majorant', q=s(V['q_head']),
          K_pair=s(head_crude['+']['K_pair']), K_pair_preview=dec(head_crude['+']['K_pair']),
          fails_headline_target=True, status='reported, not a target (contract crude_tier_reported)',
          per_sign={sg: pair_record(d) for sg, d in head_crude.items()})

    # labelled refinements and alternatives (never the bound)
    hp = head['+']
    K_ref = (hp['t1'] + Q(per_factor, 3) * abs(tau_cap) * P['GpR_up'] * hp['T_w']) / (1 - hp['Gamma_beta'])
    require(K_ref < hp['K_F1_vs_F2'], 'refined source loss is smaller')
    q1_lo, q1_hi = root_bracket(V['q_floor'], 2)
    qc_lo, qc_hi = root_bracket(V['q_floor'], 4)
    w1_sq_max = V['w_max']
    require(V['w_head'] ** 2 > w1_sq_max, 'l1 convention cannot carry w=64 (loss w^2 per interaction)')
    require(q1_lo > V['q_head'], 'the l1 minimal rate is slower than 1/64')
    require(qc_lo >= V['q_card_floor_stated'] and qc_lo > Q(1395, 10000) and qc_lo < Q(1396, 10000), 'cardinality rate bracket')
    family_rows = []
    for w in (Q(2), Q(8), Q(64), Q(512), w_max):
        d = weighted_pair(tau_cap, w, w, 'exact_first_order', C)
        family_rows.append({'w': s(w), 'q': s(d['q']), 'K_pair': s(d['K_pair']), 'K_pair_preview': dec(d['K_pair'])})
    check('labelled_refinements_and_alternatives', True,
          refined_source_loss_F1_vs_F2={'K': s(K_ref), 'K_preview': dec(K_ref),
                                         'reason': 'every extra F2 face lies inside the outer layer (rho_B=0), so its loss is 1, not w; labelled, not the bound'},
          general_direct={'K': s(hp['K_general_direct']), 'K_preview': dec(hp['K_general_direct'])},
          union_one_prescription={'K': s(hp['K_union']), 'K_preview': dec(hp['K_union']),
                                  'statement': 'two finite complete-factor volumes of one prescription both containing Lambda_N, each compared with their union (new terms outside Lambda_N, distance at least N from e_z)'},
          l1_alternative={'w1_squared_max': s(w1_sq_max), 'q1_min_bracket': [s(q1_lo), s(q1_hi)],
                          'q1_min_preview': dec(q1_lo), 'closes_at_q_1_64': False},
          cardinality_weight={'loss': 'e^{4 mu}', 'q_min_bracket': [s(qc_lo), s(qc_hi)], 'q_min_preview': dec(qc_lo)},
          star_count_weight='labelled alternative, not evaluated, never mixed with the diameter weight',
          proved_family_q_in_qmin_to_1=family_rows)

    # ---------------- cutoff uniformity ----------------------------------------------------------
    # W_f Omega_0 lies in a tensor product of on-site eigenspaces with energies 6 j_x (j_x links of f owned by x); it is kept by
    # 1_[0,L](h_x) iff 6 j_x <= L, so Q_L c^(1) keeps or annihilates each face vector; for L >= 24 all are kept.
    link_counts = []
    for cls in omitted:
        base = (cls[1], cls[2], 0)
        a, cc = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}[cls[0]]
        per = {}
        for link in face_links(base, a, cc):
            per[owner(link[0])] = per.get(owner(link[0]), 0) + 1
        link_counts.append(max(per.values()))
    face_energy = 8 * 4 * Q(3, 4)
    require(face_energy == 24 and max(6 * j for j in link_counts) <= P['L_exact'] == 24, 'cutoff exactness from L=24')
    check('cutoff_uniformity', True, face_energy_normalized=s(face_energy), max_on_site_energy_of_a_face_vector=max(6 * j for j in link_counts),
          statement='every constant is independent of the on-site cutoff L; Q_L c^(1) keeps or annihilates each face vector; exact for L at least 24')

    # ---------------- scaling tau -> tau/100 ------------------------------------------------------
    t2 = tau_cap / 100
    ratios = {}
    h2 = weighted_pair(t2, V['w_head'], V['e_beta_head'], 'exact_first_order', C)
    for key in ('K_own', 'K_F1_vs_F2', 'K_nested', 'K_general_telescoping', 'K_pair'):
        ratios['headline_' + key] = hp[key] / h2[key]
        require(V['bracket_head'][0] <= ratios['headline_' + key] <= V['bracket_head'][1], 'headline scaling bracket ' + key)
    qmin = lambda t: P['J_per_tau'] * abs(t) * P['GR_up'] / R
    f1 = weighted_pair(tau_cap, 1 / qmin(tau_cap), 1 / qmin(tau_cap), 'exact_first_order', C)
    f2 = weighted_pair(t2, 1 / qmin(t2), 1 / qmin(t2), 'exact_first_order', C)
    for key in ('K_own', 'K_F1_vs_F2', 'K_general_telescoping', 'K_pair'):
        ratios['floor_' + key] = f1[key] / f2[key]
        require(V['bracket_floor'][0] <= ratios['floor_' + key] <= V['bracket_floor'][1], 'floor scaling bracket ' + key)
    ratios['floor_K_nested_contract_form'] = f1['K_nested'] / f2['K_nested']
    require(ratios['floor_K_nested_contract_form'] == 100, 'nested floor constant in the q^(N-1) form carries one factor q_min')
    ratios['q_min'] = qmin(tau_cap) / qmin(t2)
    require(ratios['q_min'] == V['bracket_qmin'] and qmin(tau_cap) == V['q_floor'] == V['qmin_stated'], 'q_min exactly linear')
    hc2 = weighted_pair(t2, V['w_head'], V['e_beta_head'], 'crude_majorant', C)
    ratios['crude_headline_K_pair'] = head_crude['+']['K_pair'] / hc2['K_pair']
    scaling_record = {k: {'exact': s(v), 'preview': dec(v, 9)} for k, v in sorted(ratios.items())}

    # ---------------- controls (each a damaging mutation) -----------------------------------------
    # coarse_metric_named
    check('coarse_metric_named',
          'coarse l-infinity metric' in V['metric']
          and rejected(lambda: require(all(dist_set([p], [(1, 0, 0)], d_one) <= 0 + diam(S_STAR, d_inf) for p in S_STAR),
                                       'mixed metrics: l1 distance with l_inf diameter'), 'l1_distance_with_l_inf_diameter')
          and rejected(lambda: require(diam(S_STAR, d_one) == 1, 'l1 star diameter is 2, not 1'), 'l1_reading_with_diameter_1'),
          metric='coarse l_inf on factor indices', d_X=1,
          mixing_fixture='star X, B={e_x}, p=e_y: d_1(p,B)=2 exceeds rho_B(I)+diam_inf(X)=1')

    # parameters_declare_metric_weights_window
    def params_ok(keys):
        for k in ('metric', 'weights', 'rate_constant_pair', 'window', 'N_min', 'clock', 'cutoff', 'comparisons'):
            require(k in keys, 'parameters lack ' + k)
        return True
    check('parameters_declare_metric_weights_window',
          params_ok(V['parameters_keys'])
          and rejected(lambda: params_ok([k for k in V['parameters_keys'] if k != 'weights']), 'weights_removed_from_parameters')
          and rejected(lambda: params_ok([k for k in V['parameters_keys'] if k != 'window']), 'window_removed_from_parameters')
          and rejected(lambda: params_ok([k for k in V['parameters_keys'] if k != 'metric']), 'metric_removed_from_parameters'),
          parameters=V['parameters_keys'], w=s(V['w_head']), e_beta=s(V['e_beta_head']), N_min=V['N_min'])

    # weighted_norm_contraction_rechecked
    def weighted_selfmap(w, value):
        require(value == P['J0'] * w * P['GR_up'], 'weighted self-map value must carry the weight w')
        require(value <= R, 'weighted self-map fails')
        return True
    check('weighted_norm_contraction_rechecked',
          weighted_selfmap(V['w_head'], P['J0'] * V['w_head'] * P['GR_up'])
          and weighted_selfmap(w_max, P['J0'] * w_max * P['GR_up'])
          and rejected(lambda: weighted_selfmap(V['w_head'], P['J0'] * P['GR_up']), 'unweighted_am2_selfmap_cited_for_weighted_ball')
          and rejected(lambda: weighted_pair(tau_cap, 2 * w_max, 2 * w_max, 'exact_first_order', C), 'weight_beyond_w_max'),
          selfmap_headline=s(P['J0'] * V['w_head'] * P['GR_up']), lipschitz_headline=s(head['+']['Gamma_w']),
          selfmap_floor=s(P['J0'] * w_max * P['GR_up']), lipschitz_floor=s(floor['+']['Gamma_w']))

    # q_min_not_crossed
    check('q_min_not_crossed',
          V['q_floor'] == qmin(tau_cap)
          and rejected(lambda: weighted_pair(tau_cap, 1 / (V['q_floor'] / 2), 1 / (V['q_floor'] / 2), 'exact_first_order', C), 'rate_half_of_q_min')
          and rejected(lambda: require(P['J0'] * (2 * w_max) * GR_true_lo <= R, 'self-map fails below q_min (lower bound of G(R))'),
                       'rate_below_q_min_with_true_G_lower_bound'),
          q_min=s(qmin(tau_cap)), radius='R=1/64')

    # ball_radius_not_used_as_tree_decay_ratio
    def rate_basis_ok(basis, w):
        require(basis == 'chosen weight w with its own weighted contraction check', 'rate basis must be a chosen weight: ' + basis)
        require(P['J0'] * w * P['GR_up'] <= R and P['J0'] * w * P['GpR_up'] < 1, 'weighted contraction at the chosen weight')
        return True
    check('ball_radius_not_used_as_tree_decay_ratio',
          rate_basis_ok('chosen weight w with its own weighted contraction check', V['w_head'])
          and rejected(lambda: rate_basis_ok('ball radius R=1/64 as per-step tree ratio', 1 / R), 'ball_radius_as_tree_ratio'),
          basis='q=1/w, w=64 chosen; R=1/64 is the ball radius of the anchored norm, a different object with the same value')

    # rate_constant_pair_prefrozen
    def rate_is_frozen(q, K_target, w):
        require(q == V['q_head'] and K_target == V['K_head_target'] and w == V['w_head'], 'rate/constant/weight differ from the frozen pair')
        return True

    def per_N_optimized():
        best = min((weighted_pair(tau_cap, w, w, 'exact_first_order', C)['q'] for w in (Q(64), Q(512), w_max)))
        return rate_is_frozen(best, V['K_head_target'], 1 / best)
    check('rate_constant_pair_prefrozen',
          rate_is_frozen(head['+']['q'], V['K_head_target'], head['+']['w'])
          and rejected(per_N_optimized, 'q_optimized_after_constants_reported_as_headline')
          and rejected(lambda: rate_is_frozen(Q(1, 128), V['K_head_target'], Q(128)), 'weight_retuned_to_128'),
          frozen={'q': s(V['q_head']), 'K_target': s(V['K_head_target']), 'floor_q': s(V['q_floor']), 'floor_K_target': s(V['K_floor_target'])})

    # tier_mixing_rejected
    check('tier_mixing_rejected',
          rejected(lambda: weighted_pair(tau_cap, 64, 64, 'exact_first_order', C, t_label='crude_majorant'), 'exact_source_with_crude_t_labelled_exact')
          and rejected(lambda: weighted_pair(tau_cap, 64, 64, 'exact_first_order', C, self_consistent=False), 't_equal_w_t1_without_self_consistency')
          and rejected(lambda: weighted_pair(tau_cap, 64, 64, 'weighted_ii', C), 'prospective_id_used_as_tier_name')
          and rejected(lambda: weighted_pair(tau_cap, 64, 64, 'exact_first_order', C, route='analytic_disc'), 'forward_constant_labelled_analytic_disc')
          and rejected(lambda: assemble_tier('exact_first_order', 'weighted_norm', [('crude_source', 'crude_majorant', Q(1))]), 'crude_component_inside_exact'),
          mixed_labelled=s(weighted_pair(tau_cap, 64, 64, 'crude_majorant', C, source_label='crude_majorant')['K_pair']),
          mapping={'weighted_i': 'weighted_norm + crude_majorant', 'weighted_ii': 'weighted_norm + exact_first_order'})

    # tau_scaling_exponent
    def scaling_ok(ratio, bracket, source='contract preregistration.scaling_brackets_per_constant'):
        require(source == 'contract preregistration.scaling_brackets_per_constant', 'bracket not read from the frozen contract')
        require(bracket[0] <= ratio <= bracket[1], 'ratio outside its preregistered bracket')
        return True
    sqrt_like = Q(10)   # a square-root bound has ratio exactly 10 under tau -> tau/100
    check('tau_scaling_exponent',
          all(scaling_ok(ratios['headline_' + k], V['bracket_head']) for k in ('K_F1_vs_F2', 'K_nested', 'K_general_telescoping', 'K_pair'))
          and all(scaling_ok(ratios['floor_' + k], V['bracket_floor']) for k in ('K_own', 'K_F1_vs_F2', 'K_general_telescoping', 'K_pair'))
          and ratios['q_min'] == V['bracket_qmin']
          and rejected(lambda: scaling_ok(sqrt_like, V['bracket_head']), 'square_root_bound_labelled_linear')
          and rejected(lambda: scaling_ok(ratios['headline_K_pair'], (Q(101), Q(102)), source='chosen after evaluation'), 'bracket_chosen_after_evaluation')
          and rejected(lambda: scaling_ok(ratios['headline_K_pair'], (Q(99), Q(101))), 'narrowed_bracket_misses_positive_correction')
          and rejected(lambda: scaling_ok(ratios['floor_K_nested_contract_form'], V['bracket_floor']), 'nested_floor_contract_form_as_tau_independent'),
          ratios=scaling_record, brackets={'headline': [s(x) for x in V['bracket_head']], 'floor': [s(x) for x in V['bracket_floor']],
                                           'q_min': s(V['bracket_qmin'])})

    # global_lipschitz_not_decay
    no_decay = P['J0'] * P['GR_up'] / (1 - P['JGp'])
    require(no_decay == V['global_lip_bound'] and V['global_lip_const'] == P['twoJGp'], 'global Lipschitz values')
    chain = {}
    for n in range(1, 7):
        L = Q(1, 2)
        A = [[Q(0)] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            A[i][n] = L
        x = solve_linear(A, [Q(0)] * n + [Q(1)])
        chain[n] = x[0]
        require(x[0] == L / (1 - L), 'nonlocal contraction: no decay')

    def decay_derivation_ok(derivation):
        require(derivation == 'weighted difference norm with the boundary-distance weight',
                'decay must come from the weighted difference norm, never from the global Lipschitz constant')
        return True

    def lipschitz_decay_claim(n):
        L = Q(1, 2)
        require(chain[n] <= L ** n / (1 - L), 'global Lipschitz constant used as a per-step decay factor is false')
        return True
    check('global_lipschitz_not_decay',
          all(no_decay == P['J0'] * P['GR_up'] / (1 - P['JGp']) for _ in range(2, 7))
          and rejected(lambda: lipschitz_decay_claim(3), 'lipschitz_as_decay_nonlocal_chain_n3')
          and rejected(lambda: lipschitz_decay_claim(6), 'lipschitz_as_decay_nonlocal_chain_n6')
          and decay_derivation_ok('weighted difference norm with the boundary-distance weight')
          and rejected(lambda: decay_derivation_ok('global Lipschitz constant as a per-shell factor'), 'global_constant_as_per_shell_decay_factor'),
          global_bound_every_N=s(no_decay), global_bound_preview=dec(no_decay), global_lipschitz=s(P['twoJGp']),
          chain_fixture={'L': '1/2', 'delta_0': s(Q(1)), 'claimed_L^n/(1-L)_at_n6': s(Q(1, 2) ** 6 / Q(1, 2))})

    # weight_direction_toward_source (chain fixture) and the non-submultiplicative weight
    def chain_bounds(n, direction):
        a, eb = Q(1, 10), Q(2)
        A = [[Q(0)] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in (i - 1, i, i + 1):
                if 0 <= j <= n:
                    A[i][j] = a
        x = solve_linear(A, [Q(0)] * n + [Q(1)])
        gam = 3 * a * eb
        if direction == 'toward_R':
            weight = [eb ** (n - i) for i in range(n + 1)]
        else:
            weight = [eb ** i for i in range(n + 1)]
        src_norm = weight[n] * 1
        bound0 = src_norm / (1 - gam) / weight[0]
        return abs(x[0]), bound0
    fixture_dir = {}
    for n in range(1, 7):
        true0, good = chain_bounds(n, 'toward_R')
        _, bad = chain_bounds(n, 'from_R')
        require(true0 <= good, 'correct weight certifies the chain')
        fixture_dir[n] = {'true': s(true0), 'weight_toward_R': s(good), 'weight_from_R': s(bad)}

    def decay_certified(direction):
        K1 = chain_bounds(1, direction)[1] * 2
        for n in range(1, 7):
            require(chain_bounds(n, direction)[1] <= K1 * Q(1, 2) ** n, 'no decay certified by the ' + direction + ' weight')
        return True

    def submultiplicative(f, eb):
        for r in range(0, 6):
            require(f(r + 1) <= eb * f(r), 'difference weight not submultiplicative with loss e^beta')
        return True

    def extraction_ok(rho_of, n):
        # support I={0,n} contains u=0 at distance n from B={n}: the weight must dominate e^{beta d(u,B)}
        require(rho_of((0, n), n) >= n, 'weight fails to dominate the distance of u from B')
        return True
    check('weight_direction_toward_source',
          decay_certified('toward_R')
          and submultiplicative(lambda r: Q(2) ** r, Q(2))
          and extraction_ok(lambda I, n: max(abs(p - n) for p in I), 5)
          and rejected(lambda: decay_certified('from_R'), 'weight_growing_with_distance_from_R')
          and rejected(lambda: submultiplicative(lambda r: Q(2) ** (r * r), Q(2)), 'non_submultiplicative_weight_2^(r^2)')
          and rejected(lambda: extraction_ok(lambda I, n: min(abs(p - n) for p in I), 5), 'min_distance_weight'),
          chain_fixture=fixture_dir, weight='e^{beta rho_B(I)}, rho_B(I)=max over p in I of d_inf(p,B)')

    # loss_per_interaction_not_per_creation and diameter_subadditivity_through_interaction (exact qubit fixtures)
    Xr = frozenset(COVER_R)
    L0 = q_Lk([], q_flip(Xr, Q(1)))
    require(L0 == {Xr: Q(1, 2)}, 'first-order fixture output')
    w64 = V['w_head']
    L0_w = q_weighted_norm(L0, w64)

    def per_interaction_bound(k, actual_w, cnorms, charge):
        J = Q(1)
        loss = w64 if charge == 'per_interaction' else Q(1)
        bound = loss * J * Lnum(k)
        for c in cnorms:
            bound *= c
        require(actual_w <= bound, 'weighted estimate violated with the ' + charge + ' charge')
        return True
    a_, b_, c_, d_ = (-1, 0, 0), (0, 0, 0), (1, 0, 0), (2, 0, 0)
    Xl = frozenset([b_, c_])
    I1, I2 = frozenset([a_, b_]), frozenset([c_, d_])
    L2 = q_Lk([q_create(I1, Q(1)), q_create(I2, Q(1))], q_flip(Xl, Q(1)))
    L1 = q_Lk([q_create(I1, Q(1))], q_flip(Xl, Q(1)))
    Ldisj = q_word([q_create(frozenset([(5, 0, 0)]), Q(1))], q_flip(Xl, Q(1)), {frozenset(): Q(1)})
    require(L2 == {frozenset([a_, d_]): Q(1, 2)} and L1 == {frozenset([a_, c_]): Q(-1, 2)} and Ldisj == {}, 'creation fixtures')
    Mout = frozenset([a_, d_])
    require(Mout == (I1 | I2) - Xl, 'output M = N minus X (disconnected)')
    dX = diam(Xl, d_inf)
    dM = diam(Mout, d_inf)

    def subadditive(form):
        if form == 'sum':
            require(dM <= dX + diam(I1, d_inf) + diam(I2, d_inf), 'diameter subadditivity (sum)')
        else:
            require(dM <= dX + max(diam(I1, d_inf), diam(I2, d_inf)), 'max-instead-of-sum shortcut')
        return True
    check('loss_per_interaction_not_per_creation',
          per_interaction_bound(0, L0_w, [], 'per_interaction')
          and diam(Xr, d_inf) == 1 and L0_w == w64 / 2
          and dM == dX + diam(I1, d_inf) + diam(I2, d_inf)
          and rejected(lambda: per_interaction_bound(0, L0_w, [], 'per_creation_only'), 'loss_charged_only_per_creation_k0')
          and rejected(lambda: require(w64 ** 0 >= w64 ** diam(Xr, d_inf), 'per-creation weight covers the output'), 'omitted_loss_first_order_output'),
          fixture_k0={'X': 'R={0,e_z}', 'output_diam': 1, 'creation_diam_sum': 0, 'weighted_norm': s(L0_w), 'per_creation_bound': s(Lnum(0)),
                      'per_interaction_bound': s(w64 * Lnum(0))},
          fixture_k2={'X_diam': dX, 'creation_diams': [1, 1], 'output_diam': dM, 'excess_over_creation_sum': dM - 2})
    check('diameter_subadditivity_through_interaction',
          subadditive('sum') and Ldisj == {} and diam(frozenset([a_, c_]), d_inf) == dX + diam(I1, d_inf)
          and rejected(lambda: subadditive('max'), 'max_instead_of_sum_disconnected_output'),
          fixture={'X': '{0,e_x}', 'I_1': '{-e_x,0}', 'I_2': '{e_x,2e_x}', 'output': '{-e_x,2e_x}=N minus X', 'diam_output': dM,
                   'bound_sum': dX + 2, 'max_shortcut': dX + 1, 'disjoint_creation_word': 'zero (creations disjoint from X commute out)'})

    # missing_incoming_stars
    anchors_R = sorted(set(sub(r, d) for r in COVER_R for d in S_STAR))

    def J_from(stars_per_site):
        J = stars_per_site * 7
        require(J == P['J_per_tau'], 'per-site sum must include incoming anchors (28|tau|)')
        return True
    check('missing_incoming_stars',
          len(anchors_R) == 7 and J_from(4) and pins['per_factor'] == 49 and per_offset[ORIGIN] == 21
          and rejected(lambda: J_from(1), 'outgoing_star_only_7tau')
          and rejected(lambda: weighted_pair(tau_cap, 64, 64, 'exact_first_order', C, J_per_tau=Q(7)) and J_from(1), 'outgoing_only_in_contraction')
          and rejected(lambda: require(per_offset[ORIGIN] == pins['per_factor'], 'source count from outgoing faces only'), 'outgoing_faces_only_in_source_21'),
          anchors_R=[list(a) for a in anchors_R], per_site_faces=pins['per_factor'], outgoing_faces=per_offset[ORIGIN])

    # boundary_source_new_terms_only
    def source_ok(new_terms, B):
        require(all(X & B for X in new_terms), 'a source term does not meet the source set')
        return True
    N0 = 2
    F1a, F2a = family_faces(N0, omitted, 'F1'), family_faces(N0, omitted, 'F2')
    ext2 = [M for (b, k, M) in F2a if not all(add(b, d) in coarse_box(N0) for d in S_STAR)]
    old2 = [M for (b, k, M) in F1a]
    check('boundary_source_new_terms_only',
          source_ok(ext2, outer_layer(N0))
          and rejected(lambda: source_ok(ext2 + old2, outer_layer(N0)), 'old_terms_charged_in_source')
          and rejected(lambda: source_ok(ext2, frozenset(x for x in coarse_box(N0) if max(abs(c) for c in x) == N0 - 1)), 'source_set_one_layer_inside'),
          extra_faces_N2=len(ext2))

    # f2_regrouping_charged_once
    def charged_once(old_faces, source_faces, big_faces):
        pool = sorted(old_faces) + sorted(source_faces)
        require(len(pool) == len(set(pool)) and set(pool) == set(big_faces), 'a face charged twice or missing')
        return True
    F2b3 = family_faces(3, omitted, 'F2')
    s2, s3 = set((b, k) for b, k, _ in F2a), set((b, k) for b, k, _ in F2b3)
    new23 = s3 - s2
    gaining = set(b for b, k in new23) & set(b for b, k in s2)
    regroup_whole = set((b, k) for (b, k) in s3 if b in gaining)
    check('f2_regrouping_charged_once',
          charged_once(s2, new23, s3)
          and Q(pins['per_factor'], 3) <= P['J_per_tau']
          and rejected(lambda: charged_once(s2, new23 | regroup_whole, s3), 'regrouped_groups_charged_whole'),
          groups_gaining_faces_N2_to_N3=len(gaining), per_site_face_sum='49|tau|/3 at most 28|tau|')

    # boundary_distance_exact
    def exponent_ok(comparison, N, exponent):
        want = {'nested_e_z': N, 'nested_0': N + 1, 'F1_vs_F2_e_z': N - 1, 'F1_vs_F2_0': N}[comparison]
        require(exponent == want, 'off-by-one exponent for ' + comparison)
        return True
    dist_rows = {}
    for N in (2, 3, 4, 5):
        SH, LY = shell(N), outer_layer(N)
        dist_rows[N] = [min(d_inf(EZ, y) for y in SH), min(d_inf(ORIGIN, y) for y in SH),
                        min(d_inf(EZ, y) for y in LY), min(d_inf(ORIGIN, y) for y in LY)]
        exponent_ok('nested_e_z', N, dist_rows[N][0])
        exponent_ok('nested_0', N, dist_rows[N][1])
        exponent_ok('F1_vs_F2_e_z', N, dist_rows[N][2])
        exponent_ok('F1_vs_F2_0', N, dist_rows[N][3])
    check('boundary_distance_exact',
          rejected(lambda: exponent_ok('F1_vs_F2_e_z', 3, 3), 'F1_vs_F2_exponent_N_instead_of_N_minus_1')
          and rejected(lambda: exponent_ok('nested_e_z', 3, 2), 'nested_exponent_N_minus_1_mislabelled'),
          distances={str(N): {'shell_e_z': r[0], 'shell_0': r[1], 'layer_e_z': r[2], 'layer_0': r[3]} for N, r in dist_rows.items()},
          all_size='d_inf(e_z, shell)=N via (0,0,N+1); d_inf(0,shell)=N+1; d_inf(e_z, layer)=N-1 via (0,0,N); d_inf(0,layer)=N')

    # face_count_all_sites
    def pins_ok(pp):
        require(pp == V['pins'], 'face pins differ')
        return True
    site0_only = {'per_factor': per_offset[ORIGIN], 'owner_sets': 6, 'meet': 2 * per_offset[ORIGIN], 'inside': inside}
    check('face_count_all_sites',
          pins_ok(pins)
          and rejected(lambda: pins_ok(site0_only), 'site_0_only_counts')
          and rejected(lambda: pins_ok(dict(pins, per_factor=84)), 'labelled_bound_84_as_count'),
          derived=pins, per_offset={'0': per_offset[ORIGIN], 'e_x': per_offset[(1, 0, 0)], 'e_y': per_offset[(0, 1, 0)], 'e_z': per_offset[EZ]})

    # full_original_wilson_cover
    def factor_links(bf):
        out = []
        for r in range(4):
            for q in range(2):
                tail = (4 * bf[0] + r, 2 * bf[1] + q, bf[2])
                for a in range(3):
                    out.append((tail, a))
        return out
    cover_links = factor_links(ORIGIN) + factor_links(EZ)
    ends = {}
    for bf in COVER_R:
        e = set()
        for tail, a in factor_links(bf):
            e.add(tail)
            e.add(add(tail, E_UNIT[a]))
        ends[bf] = e
    W_links = face_links((0, 0, 0), 0, 2)
    W_owners = [owner(l[0]) for l in W_links]

    def cover_ok(links, endpoints):
        require(len(set(links)) == 48 and len(endpoints) == 36, 'complete cover has 48 links and 36 endpoints')
        return True
    check('full_original_wilson_cover',
          cover_ok(cover_links, ends[ORIGIN] | ends[EZ]) and len(ends[ORIGIN]) == 22 and len(ends[ORIGIN] & ends[EZ]) == 8
          and W_owners == [ORIGIN, ORIGIN, EZ, ORIGIN]
          and rejected(lambda: cover_ok(list(W_links), set(x[0] for x in W_links)), 'four_drawn_links_as_cover')
          and rejected(lambda: cover_ok(factor_links(ORIGIN), ends[ORIGIN]), 'single_factor_cover'),
          links=48, endpoints=36, per_factor_endpoints=22, shared_endpoints=8, W_link_owners=['0', '0', 'e_z', '0'])

    # coefficient_decay_not_marginal_decay (AV1 F13 type fixture)
    r_, o_, o2_ = (0, 0, 0), (1, 0, 0), (2, 0, 0)

    def marginal(a, b, g):
        vec = q_ground([(frozenset([r_, o_]), a), (frozenset([o_]), b), (frozenset([o2_]), g)])
        return q_reduced_one_site(vec, r_)
    rho_b = marginal(Q(1, 3), Q(1, 2), Q(2, 5))
    rho_0 = marginal(Q(1, 3), Q(0), Q(2, 5))
    require(rho_b == [[Q(45, 49), Q(6, 49)], [Q(6, 49), Q(4, 49)]] and rho_0 == [[Q(9, 10), Q(0)], [Q(0), Q(1, 10)]], 'F13 fixture values')

    def state_decay_from_coefficients(ra, rb):
        require(ra == rb, 'equal coefficients meeting R do not give equal marginals')
        return True
    check('coefficient_decay_not_marginal_decay',
          rho_b != rho_0
          and rejected(lambda: state_decay_from_coefficients(rho_b, rho_0), 'state_decay_inferred_from_coefficient_decay'),
          fixture={'coefficient_meeting_R': '1/3 (straddling {r,o}) in both', 'outside_coefficient_b': ['1/2', '0'],
                   'rho_r_b_half': [[s(x) for x in row] for row in rho_b], 'rho_r_b_zero': [[s(x) for x in row] for row in rho_0]},
          statement='coefficient decay is not decay of the reduced density on R: the normalization couples all supports (BB1)')

    # wrong_delta_alpha_hbar_clock
    def first_order_coefficient(coef_face, energy):
        val = coef_face / energy
        require(val == Q(-1, 72), 'first-order face amplitude must be -tau/72 per unit tau')
        return True
    alpha, hbar, t_phys = Q(5), Q(7), Q(7, 5)
    theta = alpha * t_phys / hbar
    u_norm = theta / 8

    def window_label_ok(value, label):
        require((label == 'theta' and value == theta) or (label == 'u' and value == u_norm), 'clock label mismatch (eightfold error)')
        return True
    check('wrong_delta_alpha_hbar_clock',
          first_order_coefficient(Q(-1, 3), face_energy) and first_order_coefficient(Q(-1, 24), Q(3))
          and window_label_ok(theta, 'theta') and window_label_ok(u_norm, 'u')
          and rejected(lambda: first_order_coefficient(Q(-1, 3), face_energy * 8), 'tau_over_576_mixed_units')
          and rejected(lambda: first_order_coefficient(Q(-1, 3), Q(3)), 'tau_over_9_mixed_units')
          and rejected(lambda: window_label_ok(u_norm, 'theta'), 'window_in_u_labelled_theta'),
          clock=V['clock'], window=V['window'], fixture={'alpha': '5', 'hbar': '7', 't': '7/5', 'theta': s(theta), 'u': s(u_norm)})

    # root_n_misuse
    aligned = [Q(1, 7)] * 49
    linear = sum(aligned)

    def deterministic_sum(total, parts):
        require(total >= sum(parts), 'deterministic bounds add linearly')
        return True
    rss_up = root_bracket(sum(x * x for x in aligned), 2)[1]
    tele = sum(hp['K_nested'] * hp['q'] ** (n - 1) for n in range(2, 40))
    check('root_n_misuse',
          deterministic_sum(linear, aligned) and tele <= hp['K_nested'] * hp['q'] / (1 - hp['q'])
          and rejected(lambda: deterministic_sum(rss_up, aligned), 'root_sum_of_squares_over_49_aligned_faces')
          and rejected(lambda: deterministic_sum(linear / root_bracket(49, 2)[1], aligned), 'division_by_sqrt_faces')
          and rejected(lambda: deterministic_sum(tele / 2, [hp['K_nested'] * hp['q'] ** (n - 1) for n in range(2, 40)]), 'telescoping_divided_by_sqrt_4'),
          note='the first-order source is charged face by face linearly (49 per site); the orthogonal grouped value is not used')

    # exact_arithmetic_admission
    check('exact_arithmetic_admission',
          rat('1/64') == Q(1, 64)
          and rejected(lambda: rat(0.015625), 'float_input')
          and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('nan'), 'nan_input')
          and rejected(lambda: rat('1/0'), 'zero_denominator'),
          arithmetic='fractions.Fraction; directed upward enclosure e^{1/8} at most 8/7; decimal previews are never read by admissions')

    # changed_model_relabelled
    MODEL = {'model_id': V['model_id'], 'tau': s(tau_cap), 'triple': ['0', '0', '0'], 'families': ['F1', 'F2'], 'metric': 'coarse l_inf',
             'd_X': 1, 'w': s(V['w_head']), 'e_beta': s(V['e_beta_head']), 'window': V['window'], 'group': 'SU(2)', 'dimension': 3,
             'cover': 'R={0,e_z}'}

    def model_ok(m):
        require(m == MODEL, 'packet model differs from the contract')
        require(rat(m['tau']) == V['tau'] and [rat(x) for x in m['triple']] == V['triple'] and m['model_id'] == V['model_id'], 'contract fields')
        return True
    check('changed_model_relabelled',
          model_ok(dict(MODEL))
          and rejected(lambda: model_ok(dict(MODEL, tau='1/100000000000000')), 'tau_1e-14')
          and rejected(lambda: model_ok(dict(MODEL, triple=['1', '0', '0'])), 'nonzero_selected_triple')
          and rejected(lambda: model_ok(dict(MODEL, group='SU(3)')), 'other_group')
          and rejected(lambda: model_ok(dict(MODEL, dimension=2)), 'two_dimensional')
          and rejected(lambda: model_ok(dict(MODEL, model_id='finite_graph_fixture')), 'finite_graph_relabelled')
          and rejected(lambda: model_ok(dict(MODEL, model_id='uniform_route_B')), 'uniform_model_relabelled')
          and rejected(lambda: model_ok(dict(MODEL, metric='coarse l1', d_X=2)), 'l1_metric_relabelled')
          and rejected(lambda: model_ok(dict(MODEL, w='128')), 'weight_retuned'),
          model=MODEL)

    # insufficient_verdict_retained
    def verdict_for(k_head, k_floor):
        if k_head <= V['K_head_target'] and k_floor <= V['K_floor_target']:
            return 'accepted_within_scope'
        if k_floor <= V['K_floor_target']:
            return 'limited'
        return 'insufficient'

    def retained(tier_value, claimed):
        require(verdict_for(tier_value, Kf) == claimed, 'verdict does not follow from the constants')
        return True
    check('insufficient_verdict_retained',
          retained(Kh, 'accepted_within_scope') and retained(head_crude['+']['K_pair'], 'limited')
          and rejected(lambda: retained(head_crude['+']['K_pair'], 'accepted_within_scope'), 'crude_tier_relabelled_accepted')
          and rejected(lambda: model_ok(dict(MODEL, tau=s(tau_cap / 100))), 'tau_retuned_for_crude_tier'),
          crude_headline_outcome='limited-tier value retained (fails 1/2000000)', crude_K=dec(head_crude['+']['K_pair']))

    # no_priority_or_continuum_claim, untruncated, decay-in-N, two families, subsequence, uniform-in-N
    CLAIMS = {'continuum_claim': False, 'uniqueness_of_ground_state_claimed': False, 'state_decay_claimed': False,
              'rate_in_a_claimed': False, 'scientific_priority_verified': False, 'rate_in_N_claimed': True,
              'untruncated_coefficients_asserted': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False}
    GATE = dict(V['gate_fields'])

    def claims_ok(cl, gf):
        for k, val in CLAIMS.items():
            require(cl.get(k) is val, 'claim flag ' + k + ' must be ' + str(val))
        require(gf == V['gate_fields'], 'gate fields differ from the contract gate_fields_required')
        for k, val in gf.items():
            if isinstance(val, bool):
                require(cl.get(k, val) is val, 'claim flag disagrees with gate field ' + k)
        return True
    check('no_priority_or_continuum_claim',
          claims_ok(dict(CLAIMS), dict(GATE))
          and rejected(lambda: claims_ok(dict(CLAIMS, continuum_claim=True), GATE), 'continuum_claim_true')
          and rejected(lambda: claims_ok(dict(CLAIMS, scientific_priority_verified=True), GATE), 'priority_verified_true'),
          flags=CLAIMS)
    check('gate_fields_topic_specific',
          claims_ok(CLAIMS, dict(GATE))
          and rejected(lambda: claims_ok(CLAIMS, {k: v for k, v in GATE.items() if k != 'rate_in_N_claimed'}), 'rate_in_N_field_dropped')
          and rejected(lambda: claims_ok(CLAIMS, dict(GATE, common_limit_claimed=True)), 'common_limit_flag_flipped')
          and rejected(lambda: claims_ok(CLAIMS, dict(GATE, coefficient_cauchy_scope='all supports, untruncated')), 'cauchy_scope_widened'),
          gate_fields=GATE)
    COEFF_SCOPE = 'each on-site cutoff space Q_L, constants independent of L; no untruncated creation expansion'

    def coefficient_scope_ok(scope):
        require(scope.startswith('each on-site cutoff space Q_L'), 'coefficient statement must be made in each Q_L')
        return True
    check('untruncated_coefficients_not_asserted',
          claims_ok(CLAIMS, GATE)
          and rejected(lambda: claims_ok(dict(CLAIMS, untruncated_coefficients_asserted=True), GATE), 'untruncated_coefficients_asserted')
          and coefficient_scope_ok(COEFF_SCOPE)
          and rejected(lambda: coefficient_scope_ok('untruncated creation coefficients after cutoff removal'), 'cutoff_removed_for_coefficients'),
          scope='every coefficient statement holds in each Q_L with constants independent of L')

    def rate_label_ok(label):
        require(label == 'per coarse step in N at fixed spacing', 'rate must be per coarse step in N at fixed spacing')
        return True
    check('decay_rate_in_N_not_a',
          rate_label_ok('per coarse step in N at fixed spacing')
          and rejected(lambda: rate_label_ok('per fm'), 'rate_converted_to_fm')
          and rejected(lambda: rate_label_ok('per lattice spacing a'), 'rate_in_lattice_spacing')
          and rejected(lambda: claims_ok(dict(CLAIMS, rate_in_a_claimed=True), GATE), 'rate_in_a_flag'),
          coarse_step='(4a,2a,a) in fine lattice units', rate='q per coarse step in N at fixed spacing and strong bare coupling')

    FAMILIES = {'F1': 'AQ1 centered whole-star boxes Lambda_N=[-N,N]^3, N at least 2',
                'F2': 'I1 section 6 all-contained-face boxes with padding on the same Lambda_N, N at least 2'}

    def families_ok(fam):
        require(sorted(fam) == ['F1', 'F2'] and fam == FAMILIES, 'exactly the two named families')
        return True
    check('two_families_named',
          families_ok(dict(FAMILIES))
          and rejected(lambda: families_ok({'F1': FAMILIES['F1']}), 'one_family_only')
          and rejected(lambda: families_ok(dict(FAMILIES, F3='I1 section 7 literal vertex boxes')), 'literal_vertex_boxes_added'),
          families=FAMILIES)

    def cauchy_statement(seq, K, q):
        for i in range(len(seq)):
            for j in range(i + 1, len(seq)):
                require(abs(seq[i] - seq[j]) <= K * q ** i, 'whole-sequence claim needs a Cauchy bound')
        return True
    geometric = [1 - Q(1, 64) ** n for n in range(8)]
    alternating = [Q((-1) ** n) for n in range(8)]
    check('subsequence_versus_whole_sequence',
          cauchy_statement(geometric, Q(2), Q(1, 64))
          and rejected(lambda: cauchy_statement(alternating, Q(2), Q(1, 64)), 'alternating_sequence_with_convergent_subsequences')
          and rejected(lambda: claims_ok(dict(CLAIMS, whole_sequence_claimed=True), dict(GATE, whole_sequence_claimed=True)), 'whole_sequence_state_claim'),
          statement='the coefficient bound is a whole-sequence Cauchy bound in N for the coefficients on supports meeting R in each Q_L; no state limit statement')

    def uniformity_text_ok(text):
        return require_uniformity_qualified(text, V['template'], 'fixture')
    check('uniform_in_N_not_in_a',
          uniformity_text_ok('Every constant is uniform in N at fixed spacing and uniform in the cutoff.')
          and rejected(lambda: uniformity_text_ok('The rate is uniform.'), 'unqualified_uniformity_next_to_rate')
          and rejected(lambda: uniformity_text_ok('The bound is uniform in the lattice spacing a.'), 'uniform_in_lattice_spacing'))

    # cardinality_weight_rate_labelled
    def card_label_ok(q_value, label):
        if label == 'cardinality':
            require(q_value ** 4 >= V['q_floor'], 'cardinality rate below (q_min)^(1/4)')
        return True
    check('cardinality_weight_rate_labelled',
          card_label_ok(qc_hi, 'cardinality') and qc_lo > V['q_card_floor_stated'] - Q(1, 10 ** 4)
          and rejected(lambda: card_label_ok(V['q_floor'], 'cardinality'), 'diameter_rate_relabelled_as_cardinality_rate'),
          cardinality_q_min_bracket=[s(qc_lo), s(qc_hi)], stated='0.1395', loss='e^{4 mu}', used=False)

    # analytic_route_disc_radius (forward: consistency of the frozen disc parameters with the weights; route not executed)
    def disc_ok(rho):
        require(28 * rho * P['GR_up'] <= R, 'disc self-map 28 rho G(R) at most R fails')
        return True
    check('analytic_route_disc_radius',
          disc_ok(V['tau_star']) and disc_ok(V['rho_head_per_tau'] * tau_cap)
          and abs(tau_cap) / V['tau_star'] == V['q_floor'] and abs(tau_cap) / (V['rho_head_per_tau'] * tau_cap) == V['q_head']
          and V['tau_star'] / abs(tau_cap) == w_max
          and rejected(lambda: disc_ok(2 * V['tau_star']), 'disc_radius_beyond_tau_star'),
          dictionary='w = rho/|tau|: rho=64|tau| gives w=64, rho=tau_star gives w=390625/148', executed=False,
          note='the analytic_disc route belongs to the reverse producer; only the parameter dictionary is checked here')

    # reverse_premise_isolation
    inv = sorted(p.relative_to(BASE / 'inputs').as_posix() for p in (BASE / 'inputs').rglob('*') if p.is_file())
    forward_list = sorted(set(['AGENTS.md', CONTRACT_REL] + V['shared'] + V['forward_additional']))
    reverse_list = sorted(set(['AGENTS.md', CONTRACT_REL] + V['shared']))
    banned = re.compile(r'(skeptic/(triage|.*prospective|.*loop2)|deliberation|experts/|recommendation|loop2-|round33/forward/ba1)')

    def reverse_ok(lst):
        require(V['reverse_isolation'] is True, 'reverse isolation declared')
        require(not [x for x in lst if banned.search(x)], 'reverse inventory contains an excluded file')
        require(sorted(lst) == reverse_list, 'reverse inventory differs from AGENTS + contract + shared premises')
        return True
    check('reverse_premise_isolation',
          inv == forward_list and reverse_ok(reverse_list) and not V['forward_additional']
          and rejected(lambda: reverse_ok(reverse_list + ['research/round33/advisor/deliberation-2.md']), 'deliberation_added')
          and rejected(lambda: reverse_ok(reverse_list + ['research/round33/forward/ba1/report.md']), 'forward_ba1_report_added')
          and rejected(lambda: reverse_ok(reverse_list + ['research/round33/skeptic/triage.md']), 'skeptic_triage_added'),
          forward_inventory_files=len(inv), reverse_inventory_files=len(reverse_list),
          note='the reverse agent\'s actual reads are checked by freeze.py and the skeptic; this producer never opened the reverse directory')

    # ---------------- report binding, mandatory sentence, scans -----------------------------------
    report = (BASE / 'report.md').read_text(encoding='utf-8')
    template = V['template']
    require(report.count(template) == 1, 'mandatory sentence template quoted exactly once as one unbroken span')
    exported_sentence = template
    require_no_affirmative(report, ROUND_FORBIDDEN + V['forbidden'], template, 'report.md')
    require_no_placeholder(report, template, 'report.md')
    require_uniformity_qualified(report, template, 'report.md')
    for token in ('Hruday N M (BUNZEEY)', 'AI-assisted', '/tmp/claude-0/ba1-forward-private/'):
        require(token in report, 'report lacks ' + token)
    for et in V['error_terms']:
        require('`' + et + '`' in report, 'error ledger item missing from report: ' + et)
    for cid in V['controls']:
        require('`' + cid + '`' in report, 'control missing from the report map: ' + cid)
    bound_values = {'K_head_pair': Kh, 'K_floor_pair': Kf, 'K_head_F1_vs_F2': hp['K_F1_vs_F2'], 'K_head_nested': hp['K_nested'],
                    'K_floor_crude_pair': floor_crude['+']['K_pair'], 'K_head_crude_pair': head_crude['+']['K_pair'],
                    'T_w_head': hp['T_w'], 'Gamma_head': hp['Gamma_w'], 'K_refined': K_ref, 'global_no_decay': no_decay}
    for name, val in bound_values.items():
        require(s(val) in report, 'report lacks the exact rational ' + name + ' = ' + s(val))
    for conv in ('l_inf', 'l1'):
        for line in ovd_rows[conv]:
            require(line in report, 'report order-versus-distance row missing (' + conv + '): ' + line)
    check('negation_aware_phrase_scan',
          rejected(lambda: require_no_affirmative('The construction gives the thermodynamic limit.', ROUND_FORBIDDEN + V['forbidden'], template, 'fx'), 'affirmative_thermodynamic_limit')
          and require_no_affirmative('This is not the thermodynamic limit.', ROUND_FORBIDDEN + V['forbidden'], template, 'fx')
          and rejected(lambda: require_no_affirmative('The bound predicts the gap.', ROUND_FORBIDDEN + V['forbidden'], template, 'fx'), 'affirmative_predicts'),
          scanned=['report.md', 'results.json strings'], template_removed_as_one_literal=True)
    check('placeholder_span_rejected',
          rejected(lambda: require_no_placeholder('K = <value to fill>', template, 'fx'), 'angle_span_with_whitespace')
          and rejected(lambda: require_no_placeholder('<a|b>', template, 'fx'), 'angle_span_with_bar')
          and rejected(lambda: require_no_placeholder('<e.g.x>', template, 'fx'), 'angle_span_with_eg'))
    check('mandatory_sentence_and_gate_fields', True, mandatory_sentence=exported_sentence, occurrences_in_report=1,
          gate_fields=GATE)
    check('report_bound_to_results', True, exact_values_in_report=sorted(bound_values), ovd_rows_bound=len(ovd_rows['l_inf']) + len(ovd_rows['l1']))

    # ---------------- error ledger ----------------------------------------------------------------
    fp = floor['+']
    ledger = {
        'weighted_contraction_loss': {'status': 'charged',
                                      'headline': {'Gamma': s(hp['Gamma_w']), 'Gamma_preview': dec(hp['Gamma_w']),
                                                   'amplification_1_over_1_minus_Gamma_squared': s(1 / (1 - hp['Gamma_w']) ** 2)},
                                      'floor': {'Gamma': s(fp['Gamma_w']), 'amplification_1_over_1_minus_Gamma_squared': s(1 / (1 - fp['Gamma_w']) ** 2)},
                                      'note': "loss w^{d_X}=w once per interaction term inside Gamma=J w G'(R), paid in the self-consistent t_w and in the difference"},
        'boundary_source_terms': {'status': 'charged',
                                  'headline': {'first_order': s(hp['source_first_order']), 'remainder': s(hp['source_remainder']), 'total': s(hp['source'])},
                                  'floor': {'first_order': s(fp['source_first_order']), 'remainder': s(fp['source_remainder']), 'total': s(fp['source'])},
                                  'note': 'new terms only (each meets B), at most 49 faces per site, J_new at most 28|tau|, loss e^{beta rho_B} at most e^beta'},
        'order_versus_distance_count': {'status': 'not_applicable',
                                        'reason': 'not a numeric cost: the enumeration fixes d_X=1 (loss w per interaction) and the exact exponents N-1, N, N+1; it enters the constants only through these integers'},
        'exact_first_order_remainder': {'status': 'charged',
                                        'headline': {'weighted_remainder_Gamma_T_w': s(hp['Gamma_w'] * hp['T_w']), 'preview': dec(hp['Gamma_w'] * hp['T_w'])},
                                        'floor': {'weighted_remainder_Gamma_T_w': s(fp['Gamma_w'] * fp['T_w']), 'preview': dec(fp['Gamma_w'] * fp['T_w'])}},
        'cutoff_uniformity': {'status': 'not_applicable',
                              'reason': 'not a numeric cost: every estimate is dimension-free and holds in each Q_L with the same constants; Q_L c^(1) keeps or annihilates face vectors (exact for L at least 24)'},
        'arithmetic': {'status': 'not_applicable',
                       'reason': 'not a numeric cost: exact Fractions throughout; the only enclosures are directed upward (e^{1/8} at most 8/7, hence G(R) at most 148/7, G\'(R) at most 352)'},
    }
    require(sorted(ledger) == sorted(V['error_terms']), 'ledger names equal error_terms_itemized')
    require(all(e['status'] == 'charged' or e.get('reason') for e in ledger.values()), 'not_applicable only with a reason')
    check('error_ledger_itemized', True, items=sorted(ledger))

    # ---------------- packet assembly and coherent tampering --------------------------------------
    headline = {
        'headline_pair': {'q': s(V['q_head']), 'w': s(V['w_head']), 'e_beta': s(V['e_beta_head']), 'tier': 'exact_first_order',
                          'route': 'weighted_norm', 'K_target': s(V['K_head_target']), 'K_pair': s(Kh), 'K_pair_preview': dec(Kh),
                          'target_met': head_met, 'per_sign': {sg: pair_record(d) for sg, d in head.items()}},
        'floor_pair': {'q': s(V['q_floor']), 'w': s(w_max), 'e_beta': s(w_max), 'tier': 'exact_first_order', 'route': 'weighted_norm',
                       'K_target': s(V['K_floor_target']), 'K_pair': s(Kf), 'K_pair_preview': dec(Kf), 'target_met': floor_met,
                       'per_sign': {sg: pair_record(d) for sg, d in floor.items()},
                       'crude_majorant_tier': {'K_pair': s(floor_crude['+']['K_pair']), 'K_pair_preview': dec(floor_crude['+']['K_pair']),
                                               'target_met': floor_crude_met}},
        'crude_tier_at_q_1_64': {'tier': 'crude_majorant', 'route': 'weighted_norm', 'K_pair': s(head_crude['+']['K_pair']),
                                 'K_pair_preview': dec(head_crude['+']['K_pair']), 'meets_headline_target': head_crude_met,
                                 'status': 'reported, not a target'},
        'comparisons': {
            'F1 on Lambda_N versus F1 on Lambda_{N+1}': {'source_set': 'shell Lambda_{N+1} minus Lambda_N', 'distance_e_z': 'N', 'distance_0': 'N+1',
                                                         'K_headline': s(hp['K_nested']), 'K_floor': s(fp['K_nested']),
                                                         'K_own_exponent_N_headline': s(hp['K_own']), 'new_terms': 'whole stars b+S in Lambda_{N+1} not in Lambda_N'},
            'F2 on Lambda_N versus F2 on Lambda_{N+1}': {'source_set': 'shell Lambda_{N+1} minus Lambda_N', 'distance_e_z': 'N', 'distance_0': 'N+1',
                                                         'K_headline': s(hp['K_nested']), 'K_floor': s(fp['K_nested']),
                                                         'K_own_exponent_N_headline': s(hp['K_own']), 'new_terms': 'faces with owner set in Lambda_{N+1}, not in Lambda_N, charged face by face'},
            'F1 versus F2 on the same Lambda_N': {'source_set': 'outer layer max|b_i|=N', 'distance_e_z': 'N-1', 'distance_0': 'N',
                                                  'K_headline': s(hp['K_F1_vs_F2']), 'K_floor': s(fp['K_F1_vs_F2']),
                                                  'new_terms': '28N(5N+1) extra F2 faces, charged face by face once'},
            'any two centered boxes Lambda_M, Lambda_M\' (M, M\' at least N) of F1 or F2': {'route': 'telescoping plus the same-N comparison',
                                                                                         'K_headline': s(hp['K_general_telescoping']), 'K_floor': s(fp['K_general_telescoping'])},
            'two finite complete-factor volumes of one prescription both containing Lambda_N (labelled)': {'route': 'each compared with the union',
                                                                                                          'K_headline': s(hp['K_union']), 'K_floor': s(fp['K_union'])}},
        'scaling': scaling_record,
    }
    label = 'boundary_decay_rate_only'
    verdict = verdict_for(Kh, Kf)
    require(verdict == 'accepted_within_scope', 'forward verdict')
    verdict_line = (verdict + ' (forward half; the contract acceptance also requires the reverse analytic-disc route and skeptical review); '
                    'sub-labels boundary_decay_rate_only, static_not_dynamic')
    packet = {
        'loop': 'BA1', 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'ai_assistance': 'AI-assisted forward production (Claude model agent); correlated model-agent work, not independent human review',
        'contribution_alias': 'HNM-BA1-F forward diameter-weighted anchored-norm boundary decay of the AM2 creation coefficients of F1 and F2',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'label': label, 'secondary_sub_labels': ['static_not_dynamic'],
        'model': MODEL, 'model_statement': V['model'], 'families': FAMILIES,
        'metric': 'coarse l_inf on factor sites, d_X=1 (verified by enumeration); l1 with d_X=2 labelled alternative, never mixed',
        'weights': {'norm': '||c||_w = max_u sum_{I ni u} w^{diam(I)} ||c_I||', 'w_headline': s(V['w_head']), 'w_max': s(w_max),
                    'loss': 'w^{d_X}=w once per interaction term', 'difference_weight': 'e^{beta rho_B(I)}, rho_B(I)=max_{p in I} d_inf(p,B)',
                    'e_beta_headline': s(V['e_beta_head']), 'e_beta_floor': s(w_max)},
        'tau_values': {sg: s(t) for sg, t in taus.items()},
        'headline': headline, 'error_terms_itemized': ledger, 'gate_fields': GATE,
        'mandatory_sentence': exported_sentence,
        'statement': ('For u in R={0,e_z} and every comparison of the named families, sum over supports I containing u of ||c_I^{box1}-c_I^{box2}|| '
                      'is at most K q^(N-1) in each on-site cutoff space Q_L, with K independent of the cutoff, at both signs of tau; '
                      'headline pair q=1/64, K=' + s(Kh) + ' (exact_first_order, weighted_norm); floor pair q=148/390625, K=' + s(Kf) +
                      ' (exact_first_order, weighted_norm; crude_majorant ' + s(floor_crude['+']['K_pair']) + ').'),
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions'],
                       'additional': ['no reduced-density or state statement (BB1/BB2)', 'no dynamics', 'no uniformity in the lattice spacing a',
                                      'no limit object and no common limit of coefficients is claimed; only the Cauchy bound']},
        'routes_executed': ['forward: diameter-weighted anchored norm (coarse l_inf, loss w per interaction) with the weighted AM2 contraction re-derived',
                            'forward: boundary-distance difference weight e^{beta rho_B} and the contraction of the difference in that norm',
                            'forward: order-versus-distance lemma with enumeration on Lambda_2, Lambda_3, Lambda_4 in both conventions'],
        'routes_not_executed': ['reverse analytic_disc route (outside this producer)', 'skeptic post-comparison'],
        'contract_wording_defects': [
            'W1: parameters.weights calls B the sites met by the new terms and names the shell; new F1 stars also meet outer-layer sites of Lambda_N (distance N-1 from e_z); the proof uses only that every new term meets the shell',
            'W2: parameters.weights fixes e^beta = 64; the floor pair needs e^beta = w = 390625/148 (beta = mu), which the rule beta at most mu allows',
            'W3: global_lipschitz_not_decay calls 2J_0G\'(R) the sup-norm Lipschitz constant; the fixed-point map has Lipschitz J_0G\'(R) at most 77/781250 (2J_0G\'(R) is the exclusion constant); 37/6249384 = J_0G(R)/(1-J_0G\'(R)) uses the former',
            'W4: required item 2 states order at least ceil(d/diam); the proof gives the sharper 1+ceil(d/diam) since the far term itself is one order',
            'W5: the nested comparisons have exponent N (one better than N-1); their constants in the q^(N-1) form carry one factor q, so the floor nested constant scales with q_min',
            'W6: missing_incoming_stars mentions a Lieb-Robinson norm; this loop has none (BA2)'],
        'proposed_forward_verdict': verdict_line,
    }
    packet.update(CLAIMS)
    for k, val in GATE.items():
        if isinstance(val, bool):
            packet[k] = val

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
        require(sorted(inventory) == forward_list, 'premise snapshot inventory incomplete')
        require(rat(pk['headline']['headline_pair']['K_pair']) == weighted_pair(tau_cap, V['w_head'], V['e_beta_head'], 'exact_first_order', C)['K_pair'],
                'headline K differs from recomputation')
        require(rat(pk['headline']['floor_pair']['K_pair']) == weighted_pair(tau_cap, w_max, w_max, 'exact_first_order', C)['K_pair'],
                'floor K differs from recomputation')
        require(pk['headline']['headline_pair']['target_met'] is (rat(pk['headline']['headline_pair']['K_pair']) <= V['K_head_target']), 'target Boolean')
        require(pk['families'] == FAMILIES and pk['model'] == MODEL, 'families or model changed')
        require(pk['mandatory_sentence'] == template, 'mandatory sentence changed')
        require(pk['proposed_forward_verdict'].startswith(verdict_for(rat(pk['headline']['headline_pair']['K_pair']), Kf)), 'verdict changed')
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
            if ch['id'] == 'weight_direction_toward_source':
                ch['passed'] = False

    def t_snapshot(pk, invc):
        invc.pop(P_AY1_GATE)

    def t_K(pk, invc):
        pk['headline']['headline_pair']['K_pair'] = s(rat(pk['headline']['headline_pair']['K_pair']) / 2)

    def t_state(pk, invc):
        pk['state_decay_claimed'] = True

    def t_family(pk, invc):
        pk['families'] = {'F1': FAMILIES['F1']}

    def t_sentence(pk, invc):
        pk['mandatory_sentence'] = template.replace('not decay of the reduced density, ', '')

    def t_phrase(pk, invc):
        pk['statement'] = pk['statement'] + ' This gives the thermodynamic limit.'
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_snapshot), 'ay1_gate_snapshot_removed_hash_rebound')
          and rejected(tamper(t_K), 'headline_K_halved_hash_rebound')
          and rejected(tamper(t_state), 'state_decay_flag_hash_rebound')
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
    ap = argparse.ArgumentParser(description='BA1 forward exact checker')
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
    manifest = {'loop': 'BA1', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'BA1', 'direction': 'forward', 'checks': len(result['checks']),
                      'K_headline_preview': result['headline']['headline_pair']['K_pair_preview'],
                      'K_floor_preview': result['headline']['floor_pair']['K_pair_preview'],
                      'controls_with_damaging_mutations': result['controls_with_damaging_mutations'],
                      'rejected_mutation_total': result['rejected_mutation_total']}, sort_keys=True))


if __name__ == '__main__':
    main()
