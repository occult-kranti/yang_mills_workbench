#!/usr/bin/env python3
"""AW2 forward (single-direction) producer: exact checks for the Hruday
sign-certified enclosure of the Wilson mean at the AW1-frozen coupling.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

Model: zero-selected patterned AQ subfamily (selected triple exactly (0,0,0),
Haar product reference, whole stars phi_b=-(tau/3) sum W_f under I1.5,
centered whole-star boxes N>=2, cover R={0,e_z} of the original xz Wilson
loop W). The AW1 gate admits omega_tau(W)=+tau/144+r(tau), |r|<=K_2^+ tau^2
uniformly in N, cutoff and every AQ1 subsequential limit, |tau|<=10^-8.
This checker (1) reads K_2^+ from the hash-verified AW1 gate snapshot and
evaluates the frozen AW1 decade-grid rule, (2) encloses omega_tau(W) at
tau=+-tau_AW2 and proves strict exclusion of the free reference 0 with the
contract's exclusion margin, (3) records the static scope, and (4) runs every
contract control as a damaging mutation.

Standard library only (fractions, hashlib, inspect, json, argparse, re,
math.isqrt) plus calculator.py from the same closure. Every admission Boolean
is decided in exact Fraction arithmetic; decimal strings are outward-widened
previews. Conditions raise AdmissionError explicitly (never `assert`), so
every check stays active under `python -O`. Every number in results.json is a
string.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import inspect
import json
import re
import sys
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))
import calculator as calc  # noqa: E402  (same producer closure; no bytecode written)

CONTRACT_REL = 'research/round32/contracts/aw2.json'
CONTRACT_SHA256 = 'aa559b18231961b5bb9dc5b7d0dd3097a1a2753916b54639eb1fd573e08368f9'
AW1_GATE_REL = 'research/round32/advisor/aw1-gate.json'
AW1_GATE_SHA256 = '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae'
AW1_CONTRACT_REL = 'research/round32/contracts/aw1.json'
AV1_GATE_REL = 'research/round32/advisor/av1-gate.json'
AW1_FWD_REPORT_REL = 'research/round32/forward/aw1/report.md'
AW1_FWD_RESULTS_REL = 'research/round32/forward/aw1/output/results.json'
AW1_SKEPTIC_REL = 'research/round32/skeptic/aw1.md'
AV1_FWD_REPORT_REL = 'research/round32/forward/av1/report.md'
AQ1_REL = 'research/round29/forward/aq1/report.md'
I1_REL = 'research/round21/forward/i1/report.md'
SELECTION_REL = 'research/round32/advisor/selection-aw2.md'
PREVIEW_FILE = 'arb-preview.json'
DISCLOSED_EXTRA_READS = [
    'research/round32/tools/README.md (protocol)',
    'research/round32/tools/freeze.py (protocol)',
    'research/round32/forward/av2/check.py (code style; header and helper portions)',
    'research/round32/forward/av2/calculator.py (code style)',
    'research/round32/forward/aw1/check.py (code style; helper, fixture and packet portions)',
    'sha256 only (no content read) of the repository copies of research/round32/contracts/aw2.json and '
    'research/round32/advisor/aw1-gate.json, to confirm they equal the snapshots',
]


class AdmissionError(Exception):
    """An admission condition failed or a damaging mutation was accepted."""


def require(condition, message):
    if not condition:
        raise AdmissionError(message)


CHECKS = []
PENDING = []   # mutation labels rejected while the next check's condition is evaluated


def check(identity, condition, **details):
    require(condition, 'failed check ' + identity)
    require(all(c['id'] != identity for c in CHECKS), 'duplicate check id ' + identity)
    entry = {'id': identity, 'passed': True, 'mutations_rejected': list(PENDING)}
    PENDING.clear()
    entry.update(details)
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run a damaging mutation; it must raise AdmissionError (recorded on the next check)."""
    try:
        mutation()
    except AdmissionError:
        PENDING.append(label)
        return label
    raise AdmissionError('damaging mutation accepted: ' + label)


def calc_rejects(kwargs, label, errors=(ValueError,)):
    """A calculator call outside the proved domain must raise an input error."""
    try:
        calc.enclose(**kwargs)
    except errors:
        PENDING.append(label)
        return label
    raise AdmissionError('calculator accepted an invalid case: ' + label)


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
    return calc.textq(q)


def dec_down(q, digits=12):
    return calc.dec_down(q, digits)


def dec_up(q, digits=12):
    return calc.dec_up(q, digits)


def directed_ok(text, exact_value, upward, digits=12):
    """The decimal text is on the correct side and within one unit of its last digit."""
    back = Q(text)
    x = Q(exact_value)
    e = 0
    a = abs(x)
    while a >= Q(10) ** (e + 1):
        e += 1
    while a < Q(10) ** e:
        e -= 1
    ulp = Q(10) ** (e - digits + 1)
    return (back >= x and back - x < ulp) if upward else (back <= x and x - back < ulp)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def sqrt_up(n, scale=10 ** 30):
    n = Q(n)
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k, scale) ** 2 < n:
        k += 1
    up = Q(k, scale)
    require(up * up >= n and (up - Q(1, scale)) ** 2 < n, 'sqrt upper bracket')
    return up


def sqrt_lo(n, scale=10 ** 30):
    n = Q(n)
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k, scale) ** 2 > n:
        k -= 1
    lo = Q(k, scale)
    require(lo * lo <= n and (lo + Q(1, scale)) ** 2 > n, 'sqrt lower bracket')
    return lo


def exact_sqrt(q):
    q = Q(q)
    a, b = isqrt(q.numerator), isqrt(q.denominator)
    require(a * a == q.numerator and b * b == q.denominator, 'not a rational square')
    return Q(a, b)


def no_numbers(obj):
    """Every number in the packet is a string (Booleans allowed)."""
    if isinstance(obj, bool) or obj is None or isinstance(obj, str):
        return True
    if isinstance(obj, (int, float, Q)):
        return False
    if isinstance(obj, dict):
        return all(isinstance(k, str) for k in obj) and all(no_numbers(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(no_numbers(v) for v in obj)
    return False


def match(pattern, text, label):
    m = re.search(pattern, text)
    require(m is not None, 'premise text not parsed: ' + label)
    return m


# ---------------------------------------------------------------------------
# Contract and inherited premises: targets, references and constants are read
# from hash-checked snapshots, never typed into this file.
# ---------------------------------------------------------------------------
def read_input(rel):
    path = BASE / 'inputs' / rel
    require(path.is_file(), 'missing premise snapshot ' + rel)
    return path.read_bytes()


def parse_contract(raw):
    require(sha_bytes(raw) == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen AW2 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AW2' and c.get('status') == 'frozen_before_production' and c.get('round') == 32, 'wrong contract identity')
    return c


def contract_values(c):
    p, pre, req = c['parameters'], c['preregistration'], c['required']
    v = {}
    m = match(r'^(\d+)/(\d+) \(from the AW1 rule: largest decade-grid coupling with K_2\^\+ tau <= (\d+)/(\d+), '
              r'evaluated inside check\.py from the AW1 gate snapshot\)$', p['tau_AW2'], 'contract tau_AW2 text')
    v['tau_stated'] = Q(int(m.group(1)), int(m.group(2)))
    v['rule_bound_stated'] = Q(int(m.group(3)), int(m.group(4)))
    v['tau_text'] = p['tau_AW2']
    require(list(p['signs']) == ['+', '-'], 'both signs required')
    m = match(r'^(\d+)/(\d+) \(AW1 gate; about ([0-9.]+); outward ceiling (\d+)/10\^(\d+) acceptable as a directed bound\)$',
              p['K_2_plus'], 'contract K_2^+ text')
    v['K_stated'] = Q(int(m.group(1)), int(m.group(2)))
    v['K_about'] = m.group(3)
    v['K_ceiling_stated'] = Q(int(m.group(4)), 10 ** int(m.group(5)))
    m = match(r'^tau/(\d+) \(alpha units, I1\.5 convention: (phi_b=([+-])\(tau/(\d+)\) sum W_f, V_b=phi_b/(\d+))\)$',
              p['first_order'], 'contract first-order / I1.5 text')
    v['c1_stated'] = Q(1, int(m.group(1)))
    v['i15_frozen'] = m.group(2)
    v['i15_sign'] = -1 if m.group(3) == '-' else 1
    v['i15_den'], v['alpha_div'] = int(m.group(4)), int(m.group(5))
    m = match(r'^exclusion margin m = \(\|tau\|/(\d+) - K_2\^\+ tau\^2\)/\(K_2\^\+ tau\^2\) >= (\d+) \(equivalently '
              r'1/\((\d+) K_2\^\+ \|tau\|\) >= (\d+)\); report also the contract-defined sign margin '
              r'1/\((\d+) K_2\^\+ \|tau\|\) \(about (\d+)\)$', p['target'], 'contract target text')
    require(int(m.group(1)) == int(m.group(3)) == int(m.group(5)) == v['c1_stated'].denominator, 'target coefficient differs')
    v['margin_target_text'] = Q(int(m.group(2)))
    v['sign_equiv'] = Q(int(m.group(4)))
    v['sign_about'] = int(m.group(6))
    require(v['sign_equiv'] == v['margin_target_text'] + 1, 'm>=2 must be equivalent to S>=3 (m=S-1)')
    v['triple'] = [rat(x) for x in p['selected_coefficients_over_alpha']]
    require(v['triple'] == [0, 0, 0], 'zero-selected triple required')
    t = pre['target']
    require(t['quantity'] == 'exclusion_margin' and t['comparator'] == '>=', 'preregistered target quantity')
    v['target'] = rat(t['value'])
    require(v['target'] == v['margin_target_text'], 'preregistered target differs from the parameter target')
    ob = pre['observable']
    require(ob['id'] == 'omega(W)' and ob['centering'] == 'none' and ob['reference_route'] == 'haar', 'observable identity')
    v['reference'] = rat(ob['reference_value_exact'])
    v['centering'] = ob['centering']
    tau = pre['tau']
    require(rat(tau['value']) == v['tau_stated'] and list(tau['signs_evaluated']) == ['+', '-']
            and tau['is_model_change_vs_previous_loop'] is False, 'preregistered tau block')
    require(tau['rule_if_chosen_later'] == 'AW1 decade-grid rule, frozen in contracts/aw1.json and evaluated in check.py '
                                          'from advisor/aw1-gate.json', 'preregistered rule provenance')
    v['model_id'] = pre['model_id']
    require(v['model_id'] == 'AQ_patterned_zero_selected', 'model id')
    require([rat(x) for x in pre['selected_triple_alpha_units']] == [0, 0, 0], 'prereg triple')
    v['state_provenance'] = pre['state_provenance']
    v['reference_route'] = ob['reference_route']
    v['clock'] = pre['clock']
    require('u=s/8 and exponent 24 forbidden in packets' in v['clock'], 'clock prohibition')
    v['error_terms'] = list(pre['error_terms_itemized'])
    v['error_terms_rule'] = pre['error_terms_rule']
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['controls'] = list(c['controls'])
    require(list(pre['controls_required']['ids']) == v['controls'], 'controls list differs from the preregistration')
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['shared_premises'] = list(c['shared_premises'])
    v['producers'] = list(c['producers'])
    v['direction'] = c['direction']
    v['single_replay'] = c.get('single_direction_independent_replay')
    v['new_control_semantics'] = dict(c['new_control_semantics'])
    m = match(r'Enclose omega_tau\(W\) in \[tau/(\d+) - K_2\^\+ tau\^2, tau/(\d+) \+ K_2\^\+ tau\^2\] at tau=\+10\^-(\d+) and -10\^-(\d+)',
              req[1], 'item 2 enclosure')
    require(Q(1, int(m.group(1))) == Q(1, int(m.group(2))) == v['c1_stated'], 'item 2 coefficient')
    require(Q(1, 10 ** int(m.group(3))) == Q(1, 10 ** int(m.group(4))) == v['tau_stated'], 'item 2 couplings')
    for phrase in ('static equal-time effect in the whole set of AQ1 subsequential limits at the zero selected triple',
                   'passed by local trace-norm convergence', 'sub-label static_not_dynamic',
                   'no dynamical correction, mass shift or susceptibility is claimed',
                   'the centered correlation shift remains unresolved (AV2 reference_unresolved)'):
        require(phrase in req[2], 'item 3 scope phrase missing: ' + phrase)
    m = match(r'0 strictly excluded with margin >=(\d+) at both signs at tau_AW2=10\^-(\d+)\.', c['acceptance']['accepted_within_scope'],
              'acceptance')
    require(Q(int(m.group(1))) == v['target'] and Q(1, 10 ** int(m.group(2))) == v['tau_stated'], 'acceptance target')
    v['acceptance'] = dict(c['acceptance'])
    return v


def parse_gate(raw):
    """Everything AW2 takes from AW1 comes from this hash-verified gate text."""
    require(sha_bytes(raw) == AW1_GATE_SHA256, 'AW1 gate snapshot differs from the bound gate bytes')
    g = json.loads(raw.decode('utf-8'))
    require(g.get('loop') == 'AW1' and g.get('verdict') == 'accepted_within_scope', 'AW1 gate identity')
    acc, dcs = g['accepted'], g['decision']
    G = {'gate': g}
    m = match(r'Bind K_2\^\+ = (\d+)/(\d+) \(about ([0-9.]+); the largest of the three valid exact-tier upper bounds, '
              r'outward ceiling (\d+)/10\^(\d+)\) as the admitted constant for AW2', dcs, 'gate decision K_2^+')
    G['K'] = Q(int(m.group(1)), int(m.group(2)))
    G['K_about_decision'] = m.group(3)
    G['ceiling'] = Q(int(m.group(4)), 10 ** int(m.group(5)))
    m = match(r'the bound value is K_2\^\+=(\d+)/(\d+) \(~([0-9.]+), outward (\d+)/10\^(\d+);', acc, 'gate accepted K_2^+')
    G['K_accepted'] = Q(int(m.group(1)), int(m.group(2)))
    G['K_about_accepted'] = m.group(3)
    G['ceiling_accepted'] = Q(int(m.group(4)), 10 ** int(m.group(5)))
    require('the skeptic itemization, identical to the forward\'s labelled unpinned_t_bounds variant' in acc, 'gate K provenance')
    G['c1'] = Q(1, int(match(r'\(3\) omega_tau\(W\)=\+tau/(\d+)\+r\(tau\) under I1\.5', acc, 'gate first order').group(1)))
    m = match(r'first-order values \+-1/(\d+) at tau=\+-10\^-(\d+)', acc, 'gate first-order values')
    G['first_value'], G['first_value_tau'] = Q(1, int(m.group(1))), Q(1, 10 ** int(m.group(2)))
    G['cap'] = Q(1, 10 ** int(match(r'at both signs of tau with \|tau\|<=10\^-(\d+):', acc, 'gate cap').group(1)))
    match(r'\(4\) \|r\(tau\)\|<=K_2\^\+ tau\^2 uniformly in N, cutoff and every AQ1 subsequential limit at the exact tier', acc, 'gate (4)')
    m = match(r'\(t<=T=\((\d+)\|tau\|/(\d+)\)/\(1-(\d+)J\), rho=(\d+)JT, J=(\d+)\|tau\|\)', acc, 'gate exact-tier constants')
    G['faces'], G['face_den'], G['L'], G['L_rho'], G['Jc'] = (int(m.group(i)) for i in range(1, 6))
    require(G['L'] == G['L_rho'], 'remainder coefficient mismatch')
    m = match(r'\(5\) K_2\^\+ tau<=1/(\d+) at tau=10\^-(\d+), so the frozen decade-grid rule gives tau_AW2=10\^-(\d+) \(the cap\) '
              r'with sign margin 1/\((\d+) K_2\^\+ tau\)~([0-9.]+) \(directed floor (\d+)/(\d+)\)', acc, 'gate (5)')
    G['rule_bound_gate'] = Q(1, int(m.group(1)))
    G['tau_gate_eval'], G['tau_aw2_gate'] = Q(1, 10 ** int(m.group(2))), Q(1, 10 ** int(m.group(3)))
    G['sign_about_gate'] = m.group(5)
    G['sign_floor_gate'] = Q(int(m.group(6)), int(m.group(7)))
    m = match(r'The crude tier \(t_c=(\d+)\|tau\|, K_2~([0-9.]+)e(\d+), margin ([0-9.]+)\) fails at the cap and is retained as a '
              r'limited-tier value', acc, 'gate crude tier')
    G['crude_tc'], G['crude_about'], G['crude_margin_about'] = int(m.group(1)), Q(m.group(2)) * 10 ** int(m.group(3)), Q(m.group(4))
    for phrase in ('at kappa=0 omega_{N,-tau}(W)=-omega_{N,tau}(W)', 'S(-tau)=S(tau)o alpha_E as whole sets of subsequential limits',
                   'oddness gives no O(tau^3) remainder', 'cover R={0,e_z}', 'phi_b=-(tau/3) sum W_f in normalized units delta=alpha/8'):
        require(phrase in acc, 'gate phrase missing: ' + phrase)
    m = match(r'The frozen AW2 coupling rule gives tau_AW2 = 10\^-(\d+) with sign margin about (\d+)\.', dcs, 'gate decision rule')
    G['tau_aw2_decision'], G['sign_about_decision'] = Q(1, 10 ** int(m.group(1))), int(m.group(2))
    G['bindings'] = dict(g['bindings'])
    G['limitations'] = list(g['limitations'])
    return G


def parse_aw1_rule(raw, G):
    require(sha_bytes(raw) == G['bindings'][AW1_CONTRACT_REL], 'AW1 contract snapshot differs from the AW1 gate binding')
    c = json.loads(raw.decode('utf-8'))
    rule = c['parameters']['aw2_coupling_rule']
    m = match(r'^tau_AW2 = the largest element of the decade grid \{10\^-(\d+), 10\^-(\d+), \.\.\.\} with K_2\^\+ \* tau <= '
              r'(\d+)/(\d+) \(half the first-order coefficient\), K_2\^\+ the admitted exact-tier remainder constant; '
              r'frozen here, never chosen after K_2 is seen$', rule, 'AW1 frozen rule')
    start = int(m.group(1))
    require(int(m.group(2)) == start + 1, 'decade grid step')
    return {'text': rule, 'start': start, 'bound': Q(int(m.group(3)), int(m.group(4))), 'tau_cap_aw1': rat(c['parameters']['tau_cap'])}


def validate_rule_premise(R, c1):
    """Semantic tie (AW1 review N7): the rule bound is half the first-order coefficient; the grid starts at the cap."""
    require(R['bound'] == c1 / 2, 'rule bound is not half the first-order coefficient')
    require(Q(1, 10 ** R['start']) == R['tau_cap_aw1'], 'rule grid does not start at the AW1 cap')
    return True


def av1_values(raw, G):
    require(sha_bytes(raw) == G['bindings'][AV1_GATE_REL], 'AV1 gate snapshot differs from the AW1 gate binding')
    g = json.loads(raw.decode('utf-8'))
    require(g.get('loop') == 'AV1' and g.get('verdict') == 'accepted_within_scope', 'AV1 gate identity')
    m = match(r'D_ii=(\d+)/(\d+) \(~1\.3612e-8; exact rational, certified by both inequalities\)', g['accepted'], 'AV1 D_ii')
    require('the explicit-density bound 2eps(1+eps)/(1+eps^2) (forward)' in g['accepted'], 'AV1 density inequality')
    return {'D_ii': Q(int(m.group(1)), int(m.group(2))), 'sha256': sha_bytes(raw)}


# ---------------------------------------------------------------------------
# Rule, enclosure, margins.
# ---------------------------------------------------------------------------
def aw2_rule(K, R):
    k = R['start']
    steps = []
    while True:
        tau = Q(1, 10 ** k)
        steps.append((tau, K * tau, K * tau <= R['bound']))
        if K * tau <= R['bound']:
            return tau, steps
        k += 1
        require(k <= R['start'] + 60, 'decade grid exhausted')


def enclosure(tau, K, c1):
    first = c1 * tau
    radius = K * tau * tau
    return {'tau': tau, 'first': first, 'radius': radius, 'lower': first - radius, 'upper': first + radius}


def margins(E):
    f, r = abs(E['first']), E['radius']
    return {'sign_margin': f / r, 'exclusion_margin': (f - r) / r}


def enc_record(E):
    M = margins(E)
    return {'tau': s(E['tau']), 'first_order_value': s(E['first']), 'second_order_radius': s(E['radius']),
            'lower': s(E['lower']), 'upper': s(E['upper']),
            'lower_decimal_outward_down': dec_down(E['lower']), 'upper_decimal_outward_up': dec_up(E['upper']),
            'excludes_zero_strictly': E['lower'] > 0 or E['upper'] < 0,
            'sign_of_omega_W': '+' if E['lower'] > 0 else ('-' if E['upper'] < 0 else 'undetermined'),
            'sign_margin': s(M['sign_margin']), 'sign_margin_decimal_down': dec_down(M['sign_margin']),
            'exclusion_margin': s(M['exclusion_margin']), 'exclusion_margin_decimal_down': dec_down(M['exclusion_margin'])}


# ---------------------------------------------------------------------------
# Geometry: I1 table parsed from its snapshot; faces, links, owners (I1.1, I1.4).
# ---------------------------------------------------------------------------
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIENT = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}
OFFSET = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN, EX, EZ = (0, 0, 0), (1, 0, 0), (0, 0, 1)
WILSON = ((0, 0, 0), (0, 2))   # W=(1/2)Tr[U_{0,x}U_{e_x,z}U_{e_z,x}^{-1}U_{0,z}^{-1}], the xz face at the fine origin


def vadd(p, q):
    return tuple(a + b for a, b in zip(p, q))


def vsub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def pt(p):
    return '(' + ','.join(str(x) for x in p) + ')'


def face_text(face):
    return 'face at fine point %s, plane %s' % (pt(face[0]), 'xyz'[face[1][0]] + 'xyz'[face[1][1]])


def face_links(face):
    """I1.4: the face at p in directions a<c has links (p,a),(p+e_a,c),(p+e_c,a),(p,c)."""
    p, (a, c) = face
    return ((p, a), (vadd(p, UNIT[a]), c), (vadd(p, UNIT[c]), a), (p, c))


def owners(face):
    return frozenset(owner(l[0]) for l in face_links(face))


def parse_i1_table(text):
    rows = re.findall(r'^\| (xy|xz|yz): r=([0-9,]+); s=([0-9,]+) \| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|$', text, re.M)
    require(len(rows) == 8, 'I1 table rows')
    classes = []
    for orient, rs_, ss_, count, supp, role in rows:
        r_vals = [int(x) for x in rs_.split(',')]
        s_vals = [int(x) for x in ss_.split(',')]
        require(len(r_vals) * len(s_vals) == int(count), 'I1 row count')
        support = frozenset(OFFSET[t.strip()] for t in supp.split(','))
        for r in r_vals:
            for q in s_vals:
                classes.append({'orient': orient, 'r': r, 's': q, 'support': support, 'role': role})
    return classes


def class_face(anchor, cls):
    return ((4 * anchor[0] + cls['r'], 2 * anchor[1] + cls['s'], anchor[2]), ORIENT[cls['orient']])


def trivial_multiplicity(n):
    """Multiplicity of spin 0 in (1/2)^{x n} by Clebsch-Gordan recursion (key 2j)."""
    mult = {0: 1}
    for _ in range(n):
        new = {}
        for tj, m in mult.items():
            for nj in (tj - 1, tj + 1):
                if nj >= 0:
                    new[nj] = new.get(nj, 0) + m
        mult = new
    return mult.get(0, 0)


def moment(n):
    """E_Haar[W^n] = 2^-n x multiplicity of spin 0 in (1/2)^{x n} (one face; its holonomy is Haar)."""
    return Q(trivial_multiplicity(n), 2 ** n)


def moment_sphere(n):
    """Free-link route (AQ2 section 5): W=q_0 for q uniform on S^3; E[q_0^{2m}]=prod_{i<m}(2i+1)/(4+2i)."""
    if n % 2:
        return Q(0)
    out = Q(1)
    for i in range(n // 2):
        out *= Q(2 * i + 1, 4 + 2 * i)
    return out


def expect_pair(f, g):
    """E_Haar[W_f W_g]: zero unless every link carries an even number of spin-1/2 factors (per-link parity)."""
    counts = {}
    for face in (f, g):
        for l in face_links(face):
            counts[l] = counts.get(l, 0) + 1
    if any(trivial_multiplicity(k) == 0 for k in counts.values()):
        return Q(0)
    require(f == g, 'two distinct plaquettes cannot pair every link')
    return moment(2)


# ---------------------------------------------------------------------------
# The admitted K_2^+ itemization (consistency replay; the gate value binds).
# ---------------------------------------------------------------------------
def k2_replay(tau, G, stars_per_site=4, faces_per_factor=None, overlap=Q(1), drop=None, tier='exact', crude=False):
    """Skeptic itemization = forward labelled variant unpinned_t_bounds (AW1 gate):
    am2_remainder rho=L J T, straddling T*T, two_creation T*T, density eps^2, normalization a eps^2 (3rd order)."""
    a = abs(tau) / G['face_den']
    star_norm = Q(21, 3) * abs(tau)          # I1.2: ||phi_b||=21 faces x |tau|/3 = 7|tau|
    J = stars_per_site * star_norm
    if crude:
        T = G['crude_tc'] * abs(tau)
    else:
        T = (faces_per_factor if faces_per_factor is not None else G['faces']) * a / (1 - G['L'] * J)
    rho = G['L'] * J * T
    eps = 2 * T + T * T
    terms = {'am2_remainder': (overlap * rho, 2), 'straddling': (T * T, 2), 'two_creation': (T * T, 2),
             'density': (eps * eps, 2), 'normalization_order': (a * eps * eps, 3)}
    if drop:
        terms.pop(drop)
    require(sorted(terms) == sorted(('am2_remainder', 'straddling', 'two_creation', 'density', 'normalization_order')),
            'itemized remainder terms incomplete')
    total = sum((v for v, _ in terms.values()), Q(0))
    return {'tier': tier, 'J': J, 'T': T, 'rho': rho, 'eps': eps, 'a': a, 'terms': terms, 'total': total, 'K': total / (tau * tau)}


# ---------------------------------------------------------------------------
# One-plaquette finite fixture under I1.5 (a finite graph; transfers_to_aq false).
# ---------------------------------------------------------------------------
def plaquette_rs_series(kmax, order, phi_sign, phi_den):
    """Rayleigh-Schrodinger series of <W> for H=H_0+V on |k>=chi_{k/2}(U_P):
    H_0=32 j(j+1)=8k(k+2) (normalized delta=alpha/8 units), W|k>=(|k-1>+|k+1>)/2, V=phi_sign (tau/phi_den) W."""
    n = kmax + 1
    H0 = [Q(8 * k * (k + 2)) for k in range(n)]

    def Wv(vec):
        out = [Q(0)] * n
        for k, x in enumerate(vec):
            if x:
                if k >= 1:
                    out[k - 1] += x / 2
                if k + 1 < n:
                    out[k + 1] += x / 2
        return out

    def V1(vec):
        return [phi_sign * x / phi_den for x in Wv(vec)]

    def ip(u, w):
        return sum((x * y for x, y in zip(u, w)), Q(0))
    psi = [[Q(1)] + [Q(0)] * (n - 1)]
    energies = [Q(0)]
    for m in range(1, order + 1):
        energies.append(ip(psi[0], V1(psi[m - 1])))
        rhs = [-x for x in V1(psi[m - 1])]
        for i in range(1, m + 1):
            rhs = [r + energies[i] * y for r, y in zip(rhs, psi[m - i])]
        psi.append([Q(0)] + [rhs[k] / H0[k] for k in range(1, n)])
    num = [sum((ip(psi[i], Wv(psi[m - i])) for i in range(m + 1)), Q(0)) for m in range(order + 1)]
    den = [sum((ip(psi[i], psi[m - i]) for i in range(m + 1)), Q(0)) for m in range(order + 1)]
    series = []
    for m in range(order + 1):
        series.append((num[m] - sum((series[i] * den[m - i] for i in range(m)), Q(0))) / den[0])
    return series, energies


def two_level_mean(tau, phi_sign, phi_den):
    """j<=1/2 plaquette truncation H=[[0,b],[b,24]], b=<0|V|1>=phi_sign tau/(2 phi_den).
    det=-b^2<0 gives one negative eigenvalue E0; the ground mean is <W>=b E0/(b^2+E0^2)."""
    b = phi_sign * tau / (2 * phi_den)
    require(b != 0, 'nonzero coupling')
    det = -b * b
    require(det < 0, 'exactly one negative eigenvalue')
    disc = 144 + b * b
    e_lo, e_hi = 12 - sqrt_up(disc), 12 - sqrt_lo(disc)
    require(e_lo <= e_hi < 0 and e_lo * e_lo < b * b, 'ground energy bracket inside the monotone window |E0|<|b|')
    vals = [b * e / (b * b + e * e) for e in (e_lo, e_hi)]
    lo, hi = min(vals), max(vals)
    sign_from_det = 1 if -b > 0 else -1          # sign(b E0) with E0<0
    return lo, hi, sign_from_det


# ===========================================================================
def compute(check_sha, calc_sha):
    contract_raw = read_input(CONTRACT_REL)
    c = parse_contract(contract_raw)
    V = contract_values(c)
    gate_raw = read_input(AW1_GATE_REL)
    G = parse_gate(gate_raw)
    R = parse_aw1_rule(read_input(AW1_CONTRACT_REL), G)
    A1 = av1_values(read_input(AV1_GATE_REL), G)
    K, c1, cap = G['K'], G['c1'], G['cap']

    # -------------------- contract and premise binding --------------------
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    expected_inputs = sorted(set(['AGENTS.md', CONTRACT_REL] + V['shared_premises']))
    gate_bound = [rel for rel in inventory if rel in G['bindings']]
    gate_bound_ok = all(inventory[rel] == G['bindings'][rel] for rel in gate_bound)
    forbidden_current = [rel for rel in inventory if re.search(r'round32/(forward|reverse|skeptic)/aw2|skeptic/aw2', rel)]
    check('contract_binding',
          sorted(inventory) == expected_inputs and inventory[CONTRACT_REL] == CONTRACT_SHA256 and not forbidden_current
          and V['producers'] == ['forward'] and V['direction'] == 'single+skeptic' and V['single_replay'] is True
          and c['preregistration']['hash_binding'] == {'contract_sha256_in_producer_inputs': True,
                                                       'check_py_reads_target_and_reference_from_contract': True,
                                                       'check_py_sha256_recorded_before_full_size_evaluation': True},
          contract_sha256=CONTRACT_SHA256, check_py_sha256_recorded_before_evaluation=check_sha,
          calculator_py_sha256_recorded_before_evaluation=calc_sha,
          target_read_from_contract={'quantity': 'exclusion_margin', 'comparator': '>=', 'value': s(V['target'])},
          reference_read_from_contract={'omega_0(W)': s(V['reference']), 'route': V['reference_route'], 'centering': V['centering']},
          premise_snapshot_files=str(len(inventory)), premises_expected=str(len(expected_inputs)),
          current_aw2_work_in_inputs=forbidden_current)

    skeptic_text = read_input(AW1_SKEPTIC_REL).decode('utf-8')
    m = match(r'\*\*Skeptic:\*\* `(\d+)/(\d+)`, with outward `10\^-12` ceiling `(\d+)/10\^(\d+)`\. It equals, exactly, '
              r'the forward\'s labelled variant `unpinned_t_bounds`\.', skeptic_text, 'skeptic K_2^+')
    K_skeptic = Q(int(m.group(1)), int(m.group(2)))
    ceil_skeptic = Q(int(m.group(3)), 10 ** int(m.group(4)))
    fwd_text = read_input(AW1_FWD_REPORT_REL).decode('utf-8')
    unpinned_preview = match(r'unpinned `t`-bounds: `([0-9.]+)`', fwd_text, 'forward unpinned variant preview').group(1)
    m = match(r'Exact tier: `K_2\^\+ = (\d+)/(\d+) ≈ ([0-9.]+)`', fwd_text, 'forward headline K_2^+')
    K_forward_headline = Q(int(m.group(1)), int(m.group(2)))
    m = match(r'\| \*\*K_2 \(crude\)\*\* \| crude \| `(\d+)/(\d+)` \|', fwd_text, 'forward crude K_2')
    K_crude = Q(int(m.group(1)), int(m.group(2)))
    fwd_results_present = (BASE / 'inputs' / AW1_FWD_RESULTS_REL).is_file()
    ceiling_tight = G['ceiling'] >= K and G['ceiling'] - K < Q(1, 10 ** 12)
    check('aw1_gate_binding',
          gate_bound_ok and len(gate_bound) == len(inventory) - 3 and AW1_CONTRACT_REL in gate_bound and AV1_GATE_REL in gate_bound
          and AW1_FWD_REPORT_REL in gate_bound and AW1_SKEPTIC_REL in gate_bound and I1_REL in gate_bound
          and G['K'] == G['K_accepted'] == V['K_stated'] == K_skeptic
          and G['ceiling'] == G['ceiling_accepted'] == V['K_ceiling_stated'] == ceil_skeptic and ceiling_tight
          and abs(Q(G['K_about_decision']) - K) < Q(1, 10 ** 5) and G['K_about_decision'] == V['K_about']
          and abs(Q(G['K_about_accepted']) - K) < Q(1, 10 ** 8)
          and str(K.numerator * 10 ** 8 // K.denominator) == unpinned_preview.replace('.', '')
          and G['c1'] == V['c1_stated'] and G['cap'] == R['tau_cap_aw1'] == V['tau_stated']
          and G['first_value'] == G['c1'] * G['first_value_tau'] and not fwd_results_present
          and calc.AW1_GATE_SHA256 == AW1_GATE_SHA256,
          aw1_gate_sha256=AW1_GATE_SHA256, snapshots_verified_against_aw1_gate_bindings=str(len(gate_bound)),
          snapshots_not_bound_by_aw1_gate=sorted(set(inventory) - set(gate_bound)),
          K_2_plus=s(K), K_2_plus_decimal_down=dec_down(K), K_2_plus_decimal_up=dec_up(K),
          K_2_plus_outward_ceiling=s(G['ceiling']),
          K_2_plus_parsed_from='gate decision string; equal to the gate accepted string, the contract parameter and the skeptic review exact rational',
          forward_aw1_results_snapshot=('absent from the AW2 input closure (not a declared premise); the labelled-variant cross-check is made '
                                        'instead against the forward AW1 report snapshot preview unpinned `t`-bounds %s (truncation of K_2^+) '
                                        'and the skeptic review statement that K_2^+ equals that variant exactly' % unpinned_preview),
          first_order_coefficient_from_gate=s(G['c1']))

    D_ii = A1['D_ii']
    Tg = G['faces'] * cap / G['face_den'] / (1 - G['L'] * G['Jc'] * cap)
    eps_g = 2 * Tg + Tg * Tg
    check('av1_gate_binding',
          2 * eps_g * (1 + eps_g) / (1 + eps_g * eps_g) == D_ii and A1['sha256'] == G['bindings'][AV1_GATE_REL],
          av1_gate_sha256=A1['sha256'], D_ii=s(D_ii), D_ii_decimal_up=dec_up(D_ii),
          note='the exact-tier T=(49|tau|/144)/(1-352J), J=28|tau| read from the AW1 gate reproduces the AV1 gate D_ii exactly')

    # -------------------- item 1: the frozen coupling rule --------------------
    tau_aw2, steps = aw2_rule(K, R)

    def validate_coupling(choice, provenance, K_used, tier, Rule=R):
        require(provenance == 'aw1_rule_evaluated_from_gate', 'literal or non-rule coupling rejected: ' + provenance)
        require(tier == 'exact', 'the rule must use the exact-tier gate constant')
        require(K_used == G['K'], 'the rule must use the AW1-gate-bound K_2^+, not a recomputed or other constant')
        validate_rule_premise(Rule, c1)
        require(choice == aw2_rule(K_used, Rule)[0], 'coupling differs from the frozen decade-grid rule')
        return True
    bad_rule = dict(R, bound=c1)
    lhs = K * tau_aw2
    check('aw2_coupling_rule_prefrozen',
          validate_coupling(tau_aw2, 'aw1_rule_evaluated_from_gate', K, 'exact') and tau_aw2 == cap
          and tau_aw2 == V['tau_stated'] == G['tau_aw2_gate'] == G['tau_aw2_decision'] and R['bound'] == V['rule_bound_stated'] == G['rule_bound_gate']
          and len(steps) == 1 and steps[0][2] is True
          and rejected(lambda: validate_coupling(Q(1, 10 ** 8), 'literal', K, 'exact'), 'literal_coupling_supplied')
          and rejected(lambda: validate_coupling(V['tau_stated'], 'contract_parameter_text', K, 'exact'), 'contract_text_used_as_coupling')
          and rejected(lambda: validate_coupling(Q(1, 10 ** 9), 'aw1_rule_evaluated_from_gate', K, 'exact'), 'not_the_largest_decade')
          and rejected(lambda: validate_coupling(Q(5, 10 ** 9), 'aw1_rule_evaluated_from_gate', K, 'exact'), 'off_grid_coupling')
          and rejected(lambda: validate_coupling(tau_aw2, 'aw1_rule_evaluated_from_gate', K_forward_headline, 'exact'), 'recomputed_forward_headline_constant')
          and rejected(lambda: validate_coupling(Q(1, 10 ** 10), 'aw1_rule_evaluated_from_gate', K_crude, 'crude'), 'crude_constant_fed_to_rule')
          and rejected(lambda: validate_coupling(tau_aw2, 'aw1_rule_evaluated_from_gate', K, 'exact', bad_rule), 'rule_bound_not_half_coefficient'),
          rule_text=R['text'], rule_source='AW1 contract snapshot (hash = AW1 gate binding)',
          rule_arithmetic={'grid_start': '1/10^%d (the AW1 cap; no larger grid element exists)' % R['start'],
                           'steps': [{'tau': s(t), 'K_2_plus_tau': s(l), 'bound': s(R['bound']), 'satisfied': ok} for t, l, ok in steps],
                           'K_2_plus_tau': s(lhs), 'K_2_plus_tau_decimal_up': dec_up(lhs), 'bound': s(R['bound']),
                           'slack': s(R['bound'] - lhs), 'bound_over_K_2_plus_tau': s(R['bound'] / lhs),
                           'bound_over_K_2_plus_tau_decimal_down': dec_down(R['bound'] / lhs),
                           'note': 'the ratio to 1/288 (~103.50) is not the sign margin (AW1 review N4); the sign margin is 1/(144 K_2^+ tau)'},
          tau_AW2=s(tau_aw2), contract_stated_tau=s(V['tau_stated']), gate_stated_tau=s(G['tau_aw2_gate']),
          literal_coupling_policy='the contract and gate texts are cross-checks only; the coupling is the rule evaluated from the gate constant')

    # -------------------- item 2: enclosures and exclusion --------------------
    E = {'+': enclosure(tau_aw2, K, c1), '-': enclosure(-tau_aw2, K, c1)}
    Ep, Em = E['+'], E['-']
    Mp, Mm = margins(Ep), margins(Em)
    rec = {sg: enc_record(E[sg]) for sg in E}
    dec_ok = all(directed_ok(rec[sg]['lower_decimal_outward_down'], E[sg]['lower'], False)
                 and directed_ok(rec[sg]['upper_decimal_outward_up'], E[sg]['upper'], True) for sg in E)
    check('enclosure_at_plus_tau',
          Ep['first'] == c1 * tau_aw2 == G['first_value'] and Ep['radius'] == K * tau_aw2 ** 2 and Ep['lower'] > 0 and dec_ok
          and Ep['upper'] - Ep['lower'] == 2 * Ep['radius'],
          enclosure=rec['+'], statement='omega_tau(W) in [tau/144 - K_2^+ tau^2, tau/144 + K_2^+ tau^2] at tau=+tau_AW2 (exact endpoints; decimals widened outward)')
    check('enclosure_at_minus_tau_mirrored_replay',
          Em['lower'] == -Ep['upper'] and Em['upper'] == -Ep['lower'] and Em['upper'] < 0 and Mm == Mp,
          enclosure=rec['-'],
          status='replay: the AW1 remainder bound holds at both signs and the flip lemma at the zero triple gives '
                 'S(-tau)=S(tau) o alpha_E, so the -tau enclosure is the mirror image of the +tau enclosure; it is not a second confirmation')
    S_p, m_p = Mp['sign_margin'], Mp['exclusion_margin']
    check('zero_exclusion_and_margins',
          Ep['lower'] > V['reference'] > Em['upper'] and m_p == S_p - 1 and m_p >= V['target'] and S_p >= V['sign_equiv']
          and G['sign_floor_gate'] <= S_p and V['sign_about'] < S_p < V['sign_about'] + Q(1, 1000)
          and S_p == 1 / (c1.denominator * K * tau_aw2) and m_p == (tau_aw2 / c1.denominator - K * tau_aw2 ** 2) / (K * tau_aw2 ** 2),
          exclusion_margin=s(m_p), exclusion_margin_decimal_down=dec_down(m_p), exclusion_margin_target=s(V['target']),
          sign_margin=s(S_p), sign_margin_decimal_down=dec_down(S_p), sign_margin_gate_directed_floor=s(G['sign_floor_gate']),
          lower_over_first_order=s(Ep['lower'] / Ep['first']), margin_identity='m = S - 1; m >= 2 iff S >= 3',
          zero_excluded_strictly={'+': Ep['lower'] > 0, '-': Em['upper'] < 0})

    def validate_exclusion(lo, hi, sign, margin, label='exact'):
        require(label == 'exact', 'only the exact-tier enclosure can resolve the shift')
        if sign > 0:
            require(lo > V['reference'], 'free reference 0 not strictly excluded (lower endpoint must be > 0)')
        else:
            require(hi < V['reference'], 'free reference 0 not strictly excluded (upper endpoint must be < 0)')
        require(margin >= V['target'], 'exclusion margin below the contract target')
        return True
    Ec = enclosure(tau_aw2, K_crude, c1)
    Mc = margins(Ec)
    K_mid = 1 / (c1.denominator * Q(5, 2) * tau_aw2)     # synthetic: S=5/2, m=3/2 (margin in [1,2))
    Emid = enclosure(tau_aw2, K_mid, c1)
    check('free_reference_exclusion',
          validate_exclusion(Ep['lower'], Ep['upper'], 1, m_p) and validate_exclusion(Em['lower'], Em['upper'], -1, Mm['exclusion_margin'])
          and Ec['lower'] < 0 < Ec['upper']
          and rejected(lambda: validate_exclusion(Ec['lower'], Ec['upper'], 1, Mc['exclusion_margin']), 'crude_enclosure_contains_zero_claimed_resolved')
          and rejected(lambda: validate_exclusion(Ep['lower'], Ep['upper'], 1, m_p, 'crude'), 'crude_label_on_exclusion_claim')
          and rejected(lambda: validate_exclusion(Q(0), Ep['upper'], 1, m_p), 'non_strict_lower_endpoint_zero')
          and rejected(lambda: validate_exclusion(Emid['lower'], Emid['upper'], 1, margins(Emid)['exclusion_margin']), 'margin_three_halves_claimed_accepted'),
          reference='omega_0(W)=0 (Haar; read from the contract), strictly outside both enclosures',
          crude_tier_enclosure_at_cap={'lower': s(Ec['lower']), 'upper': s(Ec['upper']), 'contains_zero': Ec['lower'] < 0 < Ec['upper'],
                                       'sign_margin_decimal_down': dec_down(Mc['sign_margin'])},
          preregistered_exclusion='free reference inside enclosure => no interaction claim')

    def validate_sign_flip(fn):
        lp, hp = fn(tau_aw2)
        lm, hm = fn(-tau_aw2)
        require(lm == -hp and hm == -lp, 'the enclosure must flip with tau (mirror image)')
        require(lp > 0 and hm < 0, 'the sign of omega(W) must follow sign(tau)')
        return True

    def signed(t):
        e = enclosure(t, K, c1)
        return e['lower'], e['upper']

    def sign_blind(t):
        e = enclosure(abs(t), K, c1)
        return e['lower'], e['upper']

    def validate_replay_status(status):
        require(status == 'replay', 'the -tau enclosure is a replay of the flip lemma, not a second confirmation')
        return True
    check('sign_flip_tau',
          validate_sign_flip(signed) and validate_replay_status('replay')
          and rejected(lambda: validate_sign_flip(sign_blind), 'sign_blind_abs_tau_enclosure')
          and rejected(lambda: validate_replay_status('second_independent_confirmation'), 'minus_tau_counted_as_second_confirmation'),
          plus={'lower': s(Ep['lower']), 'upper': s(Ep['upper'])}, minus={'lower': s(Em['lower']), 'upper': s(Em['upper'])},
          flip_lemma='U_E H_N(tau,0) U_E^* = H_N(-tau,0); omega_{N,-tau}(W)=-omega_{N,tau}(W); S(-tau)=S(tau) o alpha_E (AW1 gate, zero triple only)')

    # -------------------- first-order structure (geometry and Haar parity) --------------------
    i1_text = read_input(I1_REL).decode('utf-8')
    classes = parse_i1_table(i1_text)
    omitted = [cl for cl in classes if cl['role'] == 'omitted']
    selected = [cl for cl in classes if cl['role'] == 'selected']
    support_ok = all(owners(class_face(b, cl)) == frozenset(vadd(b, d) for d in cl['support'])
                     for cl in classes for b in (ORIGIN, (-1, -1, -1), (2, -3, 5)))
    R_cover = owners(WILSON)
    meet = {}
    for u in sorted(R_cover):
        for cl in omitted:
            for d in sorted(cl['support']):
                b = vsub(u, d)
                f = class_face(b, cl)
                meet[f] = {'anchor': b, 'owners': owners(f), 'class': cl}
    inside = [f for f, x in meet.items() if x['owners'] == R_cover]
    both = [f for f, x in meet.items() if R_cover <= x['owners']]
    at0 = {class_face(vsub(ORIGIN, d), cl) for cl in omitted for d in cl['support']}
    pairs = {f: expect_pair(WILSON, f) for f in meet}
    shared_links = max(len(set(face_links(WILSON)) & set(face_links(f))) for f in meet if f != WILSON)
    coef = V['i15_sign'] * Q(1, V['i15_den']) / 24          # per-face coefficient of L_0 per tau (normalized units)

    def omega1(tau, faces, pairing=None):
        pr = pairing if pairing is not None else (lambda f: expect_pair(WILSON, f))
        return -2 * sum((coef * tau * pr(f) for f in faces), Q(0))
    om1 = omega1(tau_aw2, meet)
    moments = {n: (moment(n), moment_sphere(n)) for n in range(9)}

    def validate_reference(ref):
        require(ref == moment(1) == moment_sphere(1), 'the Haar reference omega_0(W) must be E[W]=0')
        return True

    def odd_power_invariant():
        require(trivial_multiplicity(3) == 1, 'odd tensor power has no invariant')
    check('haar_parity_exact',
          [moments[n][0] for n in range(9)] == [Q(1), 0, Q(1, 4), 0, Q(1, 8), 0, Q(5, 64), 0, Q(7, 128)]
          and all(a == b for a, b in moments.values()) and validate_reference(V['reference'])
          and sum(1 for v in pairs.values() if v != 0) == 1 and pairs[WILSON] == Q(1, 4) and shared_links <= 1
          and rejected(odd_power_invariant, 'odd_tensor_power_given_an_invariant')
          and rejected(lambda: validate_reference(Q(1, 144)), 'reference_value_nonzero'),
          moments_character_route={str(n): s(moments[n][0]) for n in range(9)},
          moments_free_link_sphere_route={str(n): s(moments[n][1]) for n in range(9)},
          faces_meeting_R=str(len(meet)), nonzero_pairings_with_W=str(sum(1 for v in pairs.values() if v != 0)),
          max_links_shared_with_W=str(shared_links))

    def validate_first_order(value, tau):
        require(value == c1 * tau, 'first-order value differs from the AW1-gate coefficient +tau/144')
        require(value == V['c1_stated'] * tau, 'first-order value differs from the contract tau/144')
        require(value == omega1(tau, meet), 'first-order value differs from the exact face sum')
        return True
    display_literal = 2 * coef * tau_aw2 * moment(2)            # the AW1 contract's literal 2<W Omega_0, c^(1)> with c^(1)=L_0
    check('wilson_mean_first_order_coefficient',
          validate_first_order(om1, tau_aw2) and validate_first_order(omega1(-tau_aw2, meet), -tau_aw2) and coef == Q(-1, 72)
          and rejected(lambda: validate_first_order(tau_aw2 / 72, tau_aw2), 'tau_over_72')
          and rejected(lambda: validate_first_order(tau_aw2 / 288, tau_aw2), 'tau_over_288')
          and rejected(lambda: validate_first_order(display_literal, tau_aw2), 'literal_plus_two_L0_display_gives_minus_tau_over_144'),
          first_order_plus=s(om1), first_order_minus=s(omega1(-tau_aw2, meet)), per_face_coefficient_of_L0_per_tau=s(coef),
          formula='omega_tau(W)=-2 Re<W Omega_0, L_0>+O(tau^2), L_0=-(tau/72) sum_f W_f Omega_0 (AV1 creation convention)',
          face_sum_over=str(len(meet)) + ' omitted faces meeting R')

    alt = [f for f in inside if f != WILSON][0]

    def validate_pairing(f, value):
        require(value == expect_pair(WILSON, f), 'pairing differs from the per-link Haar parity')
        return True
    check('wrong_face_control',
          len(omitted) == 21 and len(selected) == 3 and support_ok and len(at0) == 49 and len(meet) == 82 and len(inside) == 10
          and len(both) == 16 and all(pairs[f] == 0 for f in meet if f != WILSON) and omega1(tau_aw2, [WILSON]) == om1
          and all(validate_pairing(f, pairs[f]) for f in meet)
          and rejected(lambda: validate_pairing(alt, moment(2)), 'another_face_with_owner_set_R_claimed_to_pair_with_W')
          and rejected(lambda: validate_first_order(omega1(tau_aw2, inside, lambda f: moment(2)), tau_aw2), 'all_ten_inside_faces_counted')
          and rejected(lambda: validate_first_order(omega1(tau_aw2, [f for f in meet if f != WILSON]), tau_aw2), 'W_excluded_from_omitted_set'),
          omitted_classes=str(len(omitted)), faces_per_factor=str(len(at0)), faces_meeting_R=str(len(meet)),
          faces_with_owner_set_R=str(len(inside)), faces_touching_both_sites_of_R=str(len(both)),
          wrong_face_example={'face': face_text(alt), 'E[W W_f]': s(pairs[alt])},
          statement='every omitted face other than W contributes zero at first order (E[W W_f]=0 by per-link parity)')

    w_links_by_owner = {}
    for l in face_links(WILSON):
        w_links_by_owner[owner(l[0])] = w_links_by_owner.get(owner(l[0]), 0) + 1
    contraction_zero = {x: k >= 1 and trivial_multiplicity(1) == 0 for x, k in w_links_by_owner.items()}
    norm_WR = exact_sqrt(moment(2))
    multiplier = 2 * norm_WR
    K_rep = k2_replay(tau_aw2, G)

    def validate_overlap(mult, label, overlapping_supports):
        require(overlapping_supports == ['R'], 'only the creation supported exactly on R overlaps W Omega_R')
        require(mult == 1 or (mult == 4 and label == 'conservative'), 'overlap multiplier must be 2||W Omega_R||=1 (4 only if labelled conservative)')
        require(k2_replay(tau_aw2, G, overlap=mult)['K'] == K, 'the gate-bound K_2^+ uses multiplier 1')
        return True
    check('wilson_overlap_single_component',
          w_links_by_owner == {ORIGIN: 3, EZ: 1} and all(contraction_zero.values()) and norm_WR == Q(1, 2) and multiplier == 1
          and validate_overlap(multiplier, 'exact', ['R'])
          and rejected(lambda: validate_overlap(Q(4), 'unlabelled', ['R']), 'factor_4_unlabelled')
          and rejected(lambda: validate_overlap(Q(1, 2), 'exact', ['R']), 'multiplier_one_half_undercount')
          and rejected(lambda: validate_overlap(multiplier, 'exact', ['R', '{0}', '{e_z}']), 'single_site_creations_claimed_to_overlap'),
          W_links_per_owner={'0': str(w_links_by_owner[ORIGIN]), 'e_z': str(w_links_by_owner[EZ])},
          norm_W_Omega_R=s(norm_WR), overlap_multiplier=s(multiplier),
          conservative_variant_K_2_decimal_up=dec_up(k2_replay(tau_aw2, G, overlap=Q(4))['K']),
          reason='each link of W owned by x in R carries one spin-1/2 factor; mult(1)=0, so <Omega_x|W Omega_R>=0')

    def validate_cover(cover):
        require(cover == R_cover == frozenset((ORIGIN, EZ)), 'the cover must be the owners of all four links of W: R={0,e_z}')
        return True
    drawn_vertices = frozenset(((0, 0, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1)))
    check('full_original_wilson_cover',
          validate_cover(R_cover)
          and rejected(lambda: validate_cover(frozenset([ORIGIN])), 'cover_missing_e_z')
          and rejected(lambda: validate_cover(frozenset([ORIGIN, EX])), 'cover_shifted_to_e_x')
          and rejected(lambda: validate_cover(drawn_vertices), 'fine_drawn_vertices_as_cover'),
          cover=[pt(x) for x in sorted(R_cover)], W_link_owners=[pt(owner(l[0])) for l in face_links(WILSON)])

    # incoming stars at the sites of R, in bulk and in boxes
    def incoming(u, N=None):
        out = []
        for d in S_STAR:
            b = vsub(u, d)
            if N is None or all(-N <= b[i] and b[i] + 1 <= N for i in range(3)):
                out.append(b)
        return out
    aq1_text = read_input(AQ1_REL).decode('utf-8')
    require('J\\le4M=28|\\tau|' in aq1_text and '\\epsilon=\\sup_b\\|\\phi_b\\|=7|\\tau|' in i1_text, 'J=4M=28|tau| (AQ1) and 7|tau| (I1)')

    def validate_J(stars):
        require(k2_replay(tau_aw2, G, stars_per_site=stars)['K'] == K, 'J must count all four incoming stars (J=28|tau|)')
        return True
    check('missing_incoming_stars',
          all(len(incoming(u)) == 4 for u in R_cover) and all(len(incoming(u, N)) == 4 for u in R_cover for N in (2, 3))
          and 4 * Q(len(omitted), 3) == G['Jc'] and validate_J(4)
          and rejected(lambda: validate_J(1), 'one_star_J_7_tau') and rejected(lambda: validate_J(3), 'three_stars_J_21_tau'),
          incoming_stars_per_site_of_R='4 (bulk, N=2, N=3)', star_norm='21 faces x |tau|/3 = 7|tau|', J='28|tau|')

    # -------------------- sign convention (I1.5) and the one-plaquette fixture --------------------
    series8, energies8 = plaquette_rs_series(8, 5, V['i15_sign'], V['i15_den'])
    series10, _ = plaquette_rs_series(10, 5, V['i15_sign'], V['i15_den'])
    m = match(r'`<W>=tau/(\d+)\+0·tau\^2-(\d+)tau\^3/(\d+)\+0·tau\^4\+(\d+)tau\^5/(\d+)`, with `E_2=-tau\^2/(\d+)`', skeptic_text,
              'reviewed one-plaquette series')
    reviewed = [Q(0), Q(1, int(m.group(1))), Q(0), -Q(int(m.group(2)), int(m.group(3))), Q(0), Q(int(m.group(4)), int(m.group(5)))]
    E2_alpha = energies8[2] / V['alpha_div']
    fixture = {}
    for sg, t in (('+', tau_aw2), ('-', -tau_aw2)):
        lo, hi, sgn = two_level_mean(t, V['i15_sign'], V['i15_den'])
        fixture[sg] = {'lower': lo, 'upper': hi, 'sign_from_determinant': sgn}
    fixture_labels = {'id': 'FG(one_plaquette, character basis |k>=chi_{k/2}(U_P), H_0=8k(k+2), V=-(tau/3)W, I1.5)',
                      'finite_graph': True, 'transfers_to_aq': False}
    i15_in_i1 = '=-{\\tau\\over3}\\sum_{f\\in O_b}W_f' in i1_text

    def validate_convention(phi_text, frozen_text):
        require(phi_text == V['i15_frozen'], 'I1.5 string differs from the frozen contract string')
        mm = re.fullmatch(r'phi_b=([+-])\(tau/(\d+)\) sum W_f, V_b=phi_b/(\d+)', frozen_text)
        require(mm is not None, 'unparsed convention')
        sgn = -1 if mm.group(1) == '-' else 1
        derived = -2 * (sgn * Q(1, int(mm.group(2))) / 24) * moment(2)
        fix = plaquette_rs_series(4, 1, sgn, int(mm.group(2)))[0][1]
        require(derived == fix, 'perturbative sign disagrees with the one-plaquette fixture')
        require(derived == c1 == V['c1_stated'], 'convention gives a first-order coefficient other than the admitted +1/144')
        return True
    flipped = V['i15_frozen'].replace('phi_b=-(', 'phi_b=+(')
    check('sign_convention_fixture',
          validate_convention(V['i15_frozen'], V['i15_frozen']) and i15_in_i1 and V['i15_sign'] == -1 and V['alpha_div'] == 8
          and series8 == series10 == reviewed and E2_alpha == -Q(1, int(m.group(6)))
          and fixture['+']['lower'] > 0 and fixture['-']['upper'] < 0
          and fixture['+']['sign_from_determinant'] == 1 and fixture['-']['sign_from_determinant'] == -1
          and fixture['+']['lower'] == -fixture['-']['upper'] and fixture['+']['upper'] == -fixture['-']['lower']
          and rejected(lambda: validate_convention(flipped, flipped), 'phi_b_sign_flipped_string')
          and rejected(lambda: validate_convention(V['i15_frozen'], flipped), 'phi_b_sign_flipped_coherently_in_derivation_and_fixture'),
          frozen_I1_5_string=V['i15_frozen'], I1_report_equation='phi_b=-{tau over 3} sum_{f in O_b} W_f (I1.5 snapshot)',
          one_plaquette_series={str(k): s(x) for k, x in enumerate(series8)}, one_plaquette_E2_alpha_units=s(E2_alpha),
          two_level_ground_mean={sg: {'lower': s(fixture[sg]['lower']), 'upper': s(fixture[sg]['upper']),
                                      'lower_decimal_down': dec_down(fixture[sg]['lower']), 'upper_decimal_up': dec_up(fixture[sg]['upper'])}
                                 for sg in fixture},
          sign_rule='det[[0,b],[b,24]]=-b^2<0 so E0<0; <W>=b E0/(b^2+E0^2) has the sign of -b=sign(tau)',
          fixture_labels=fixture_labels)

    # -------------------- units and clock --------------------
    per_face_norm = Q(1, V['i15_den']) / 24
    per_face_alpha = Q(1, V['i15_den'] * V['alpha_div']) / 3
    mixed_alpha_V_norm_E = Q(1, V['i15_den'] * V['alpha_div']) / 24
    mixed_norm_V_alpha_E = Q(1, V['i15_den']) / 3
    base_cert = calc.enclose(tau=s(tau_aw2), fixed_design=True)
    scaled_cert = calc.enclose(tau=s(tau_aw2), fixed_design=True, alpha='5', hbar='7', E_star='11/2', lattice_spacing='3')
    s_clock = Q(5) * Q(3, 2) / Q(7)

    def validate_scale_free(cert):
        require(cert['enclosure'] == base_cert['enclosure'], 'the static dimensionless mean cannot depend on physical scales')
        return True

    def validate_clock(packet_clock):
        require(packet_clock == 'none: static equal-time mean (no s, theta or u enters)', 'a static packet carries no clock; u=s/8 and exponent 24 are forbidden')
        return True
    check('wrong_delta_alpha_hbar_clock',
          per_face_norm == per_face_alpha == Q(1, 72) and validate_scale_free(scaled_cert)
          and validate_clock('none: static equal-time mean (no s, theta or u enters)')
          and rejected(lambda: validate_first_order(2 * mixed_alpha_V_norm_E * moment(2) * tau_aw2, tau_aw2), 'alpha_V_with_normalized_energy_tau_over_1152')
          and rejected(lambda: validate_first_order(2 * mixed_norm_V_alpha_E * moment(2) * tau_aw2, tau_aw2), 'normalized_V_with_alpha_energy_tau_over_18')
          and rejected(lambda: validate_scale_free(calc.enclose(tau=s(tau_aw2 * 5 / Q(11, 2)))), 'tau_rescaled_by_alpha_over_E_star')
          and rejected(lambda: validate_clock('u=s/8 with exponent 24'), 'eightfold_clock_in_packet'),
          per_face_coefficient={'normalized': '(1/3)/24', 'alpha_units': '(1/24)/3', 'value': s(per_face_norm)},
          mixed_units_rejected={'alpha_V_normalized_E': s(2 * mixed_alpha_V_norm_E * moment(2)), 'normalized_V_alpha_E': s(2 * mixed_norm_V_alpha_E * moment(2))},
          nonunit_scale_fixture={'alpha': '5', 'hbar': '7', 'E_star': '11/2', 'lattice_spacing': '3', 't_E': '3/2', 's': s(s_clock),
                                 'enclosure_unchanged': True},
          contract_clock=V['clock'], packet_clock='none: static equal-time mean (no s, theta or u enters)')

    def validate_center(center, tau):
        require(center == c1 * tau and center != 0, 'the enclosure centre must be the full nonzero first-order mean tau/144')
        return True

    def parity_applied_to_mean():
        validate_center(Q(0), tau_aw2)
    check('first_order_mean_charged',
          validate_center(Ep['first'], tau_aw2) and validate_center(Em['first'], -tau_aw2) and Ep['first'] != 0
          and rejected(lambda: validate_center(Q(0), tau_aw2), 'zero_mean_at_first_order')
          and rejected(parity_applied_to_mean, 'centered_correlation_parity_applied_to_uncentered_mean'),
          first_order_mean=s(Ep['first']), zero_centred_enclosure_would_contain_zero=True,
          note='the parity theorem kills the first-order term of the vector-centred C(s), not of the uncentered mean omega(W)')

    # vector/scalar centring identities (fixtures) and no m_hat in the omega(W) path
    a1, a2 = Q(1, 20), Q(1, 150)
    Wm = [[Q(1, 5), Q(1, 3), Q(1, 7)], [Q(1, 3), Q(1, 2), Q(1, 11)], [Q(1, 7), Q(1, 11), Q(1, 4)]]
    Adiag = [Q(1), a1, a2]
    m_true = Wm[0][0]
    m_hat = m_true + Q(1, 100)

    def quad(vec):
        return sum((Adiag[i] * vec[i] * vec[i] for i in range(3)), Q(0))
    Wpsi = [Wm[i][0] for i in range(3)]
    truth = quad([Wpsi[0] - m_true, Wpsi[1], Wpsi[2]])
    vector_hat = quad([Wpsi[0] - m_hat, Wpsi[1], Wpsi[2]])
    scalar_hat = quad(Wpsi) - m_hat * m_hat
    d = m_hat - m_true

    def validate_centering_identity(vec_res, sc_res):
        require(vec_res == d * d and sc_res == -(2 * m_true * d + d * d), 'centring residues differ from the exact identities')
        return True

    def scalar_as_vector():
        require(scalar_hat - truth == vector_hat - truth, 'scalar subtraction is not vector centring when m_hat differs from m')

    def validate_observable_path(path):
        require(path == {'observable': 'omega(W)', 'centering': V['centering'], 'm_hat': None}, 'the omega(W) path is uncentered; no m_hat enters')
        return True
    enclose_params = sorted(inspect.signature(calc.enclose).parameters)
    check('vector_versus_scalar_centering',
          validate_centering_identity(vector_hat - truth, scalar_hat - truth) and quad(Wpsi) - m_true ** 2 == truth
          and validate_observable_path({'observable': 'omega(W)', 'centering': 'none', 'm_hat': None})
          and not any(p in enclose_params for p in ('m_hat', 'centering', 'mean_estimate'))
          and sorted(inspect.signature(enclosure).parameters) == ['K', 'c1', 'tau']
          and rejected(scalar_as_vector, 'scalar_subtraction_as_vector_centering')
          and rejected(lambda: validate_observable_path({'observable': 'omega(W)', 'centering': 'vector', 'm_hat': s(Ep['first'])}), 'm_hat_inserted_in_omega_W_path')
          and calc_rejects({'tau': s(tau_aw2), 'm_hat': s(Ep['first'])}, 'calculator_m_hat_argument', (TypeError,)),
          fixture={'m': s(m_true), 'm_hat': s(m_hat), 'vector_residue': s(vector_hat - truth), 'scalar_residue': s(scalar_hat - truth)},
          calculator_parameters=enclose_params, observable_centering=V['centering'],
          note='vector centring (W-m_hat)psi has residue (m-m_hat)^2; scalar subtraction has m^2-m_hat^2; omega(W) itself is uncentered')

    # -------------------- second-order remainder, tiers and scaling --------------------
    ledger = {
        'first_order_exact': {'value': '0', 'status': 'exact',
                              'reason': 'tau/144 is the exact first-order coefficient (AW1 gate item 3); the first-order term carries no truncation'},
        'second_order_remainder': {'value': s(Ep['radius']), 'K_2_plus': s(K), 'status': 'charged in full as the enclosure half-width',
                                   'source': 'AW1 gate decision (exact tier; the skeptic itemization = forward labelled unpinned_t_bounds)',
                                   'itemized_in_aw1': {n: {'value_at_cap': s(v), 'order_in_tau': str(o)} for n, (v, o) in K_rep['terms'].items()}},
        'arithmetic': {'value': '0', 'status': 'not_applicable',
                       'reason': 'exact Fraction arithmetic end to end; decimals are outward-widened previews and never decide admission'},
    }

    def validate_ledger(led, K_used, radius):
        require(sorted(led) == sorted(V['error_terms']), 'error ledger differs from the preregistered items')
        for name, entry in led.items():
            if entry.get('status') == 'not_applicable':
                require(bool(entry.get('reason')), 'not_applicable entry without a stated reason: ' + name)
        require(K_used == G['K'], 'the remainder constant must be the AW1-gate-bound K_2^+')
        require(radius == K_used * tau_aw2 ** 2 and radius > 0, 'the second-order remainder must be charged in full')
        return True
    led_no_reason = json.loads(json.dumps(ledger))
    led_no_reason['arithmetic'].pop('reason')
    led_missing = {k: v for k, v in ledger.items() if k != 'second_order_remainder'}
    check('second_order_remainder_itemized',
          validate_ledger(ledger, K, Ep['radius']) and K_rep['K'] == K and all(t[0] > 0 for t in K_rep['terms'].values())
          and k2_replay(tau_aw2, G, drop=None)['total'] == Ep['radius']
          and rejected(lambda: validate_ledger(ledger, K, Q(0)), 'second_order_term_dropped')
          and rejected(lambda: validate_ledger(ledger, k2_replay(tau_aw2, G, drop='density')['K'], Ep['radius']), 'density_term_dropped')
          and rejected(lambda: validate_ledger(ledger, K_forward_headline, K_forward_headline * tau_aw2 ** 2), 'recomputed_smaller_constant_substituted')
          and rejected(lambda: validate_ledger(ledger, K / 2, K / 2 * tau_aw2 ** 2), 'K_halved')
          and rejected(lambda: validate_ledger(led_no_reason, K, Ep['radius']), 'not_applicable_without_reason')
          and rejected(lambda: validate_ledger(led_missing, K, Ep['radius']), 'ledger_item_missing'),
          error_ledger=ledger, replay_constants={'J': s(K_rep['J']), 'T': s(K_rep['T']), 'rho': s(K_rep['rho']), 'eps': s(K_rep['eps'])},
          replay_status='consistency replay of the gate-bound value from the constants named in the gate text; the gate value binds',
          dominant_term='am2_remainder (%s of K_2^+)' % dec_down(K_rep['terms']['am2_remainder'][0] / K_rep['total'], 6))

    K_crude_replay = k2_replay(tau_aw2, G, crude=True, tier='crude')

    def validate_tier(K_used, label):
        require(label == 'exact', 'tier mixing rejected: only the exact tier certifies')
        require(K_used == G['K'], 'the exact-tier constant is the gate-bound K_2^+')
        return True
    mixed = k2_replay(tau_aw2, G)
    mixed_terms = dict(mixed['terms'])
    mixed_terms['straddling'] = K_crude_replay['terms']['straddling']
    K_mixed = sum((v for v, _ in mixed_terms.values()), Q(0)) / tau_aw2 ** 2
    check('tier_mixing_rejected',
          validate_tier(K, 'exact') and K_crude_replay['K'] == K_crude and abs(K_crude - G['crude_about']) <= 50
          and Mc['sign_margin'] < 1 and abs(Mc['sign_margin'] - G['crude_margin_about']) <= Q(5, 10 ** 5)
          and rejected(lambda: validate_tier(K_crude, 'exact'), 'crude_constant_labelled_exact')
          and rejected(lambda: validate_tier(K_mixed, 'exact'), 'crude_straddling_term_mixed_into_exact_sum')
          and rejected(lambda: validate_tier(K_crude, 'crude'), 'crude_tier_used_to_certify'),
          crude_K_2=s(K_crude), crude_K_2_decimal_down=dec_down(K_crude), crude_t='592|tau| (J G(R); AW1 gate)',
          crude_enclosure_at_cap={'lower': s(Ec['lower']), 'upper': s(Ec['upper'])},
          crude_status='fails at the cap (enclosure contains 0; sign margin %s < 1); retained as a limited-tier control' % dec_down(Mc['sign_margin']))

    def classify(K_used, tier):
        if tier != 'exact':
            return 'limited_tier_control_only'
        t, _ = aw2_rule(K_used, R)
        e = enclosure(t, K_used, c1)
        if not (e['lower'] > 0):
            return 'insufficient'
        mm = margins(e)['exclusion_margin']
        if t == cap and mm >= V['target']:
            return 'accepted_within_scope'
        return 'limited'

    def crude_at_cap_excludes():
        return Ec['lower'] > 0

    def validate_retained(report):
        require(report['crude_excludes_zero_at_cap'] is crude_at_cap_excludes(), 'crude-tier exclusion at the cap misreported')
        require(report['crude_tau'] == cap, 'crude tier retuned below the cap under the cap label')
        require(report['verdict_mid'] == classify(K_mid, 'exact'), 'a limited outcome upgraded')
        return True
    rep = {'crude_excludes_zero_at_cap': False, 'crude_tau': cap, 'verdict_mid': 'limited'}
    tau_crude_info = aw2_rule(K_crude, R)[0]
    check('insufficient_verdict_retained',
          classify(K, 'exact') == 'accepted_within_scope' and classify(K_mid, 'exact') == 'limited'
          and classify(K_crude, 'crude') == 'limited_tier_control_only' and validate_retained(rep) and not crude_at_cap_excludes()
          and rejected(lambda: validate_retained(dict(rep, crude_excludes_zero_at_cap=True)), 'crude_tier_reported_excluding_zero_at_cap')
          and rejected(lambda: validate_retained(dict(rep, crude_tau=tau_crude_info)), 'crude_retuned_to_smaller_tau_under_cap_label')
          and rejected(lambda: validate_retained(dict(rep, verdict_mid='accepted_within_scope')), 'margin_in_1_2_upgraded_to_accepted'),
          retained_outcomes={'crude_tier_at_cap': 'no exclusion (limited-tier control, retained)',
                             'crude_rule_decade_information_only': s(tau_crude_info),
                             'synthetic_margin_three_halves': 'limited'},
          acceptance=V['acceptance'])

    small = tau_aw2 / 100
    Es = enclosure(small, K, c1)
    K_small = k2_replay(small, G)
    term_ratio = {n: K_rep['terms'][n][0] / K_small['terms'][n][0] for n in K_rep['terms']}
    at4_ratio = exact_sqrt(Q(100))
    require('The AT4 bound `2 sqrt(49|tau|/3)` has a ratio of exactly `10`' in read_input(AV1_FWD_REPORT_REL).decode('utf-8'), 'AT4 ratio text')

    def exponent_ok(ratio, order):
        lo, hi = {1: (99, 101), 2: (9900, 10100), 3: (990000, 1010000)}[order]
        require(lo <= ratio <= hi, 'scaling ratio outside the declared order %d' % order)
        return True
    check('tau_scaling_exponent',
          Ep['first'] / Es['first'] == 100 and Ep['radius'] / Es['radius'] == 10000
          and exponent_ok(Ep['first'] / Es['first'], 1) and exponent_ok(Ep['radius'] / Es['radius'], 2)
          and all(exponent_ok(term_ratio[n], K_rep['terms'][n][1]) for n in term_ratio) and K_small['K'] <= K
          and margins(Es)['sign_margin'] == 100 * S_p
          and rejected(lambda: exponent_ok(Ep['radius'] / Es['radius'], 1), 'second_order_term_relabelled_first_order')
          and rejected(lambda: exponent_ok(Ep['first'] / Es['first'], 2), 'first_order_term_relabelled_second_order')
          and rejected(lambda: exponent_ok(at4_ratio, 1), 'square_root_relabelled_linear'),
          first_order_ratio=s(Ep['first'] / Es['first']), remainder_ratio=s(Ep['radius'] / Es['radius']),
          exponents={'first_order': '1', 'second_order_remainder': '2'},
          replay_K2_at_tau_over_100_decimal_up=dec_up(K_small['K']), replay_monotone_in_abs_tau=K_small['K'] <= K,
          sign_margin_at_tau_over_100=s(margins(Es)['sign_margin']))

    linear = sum((v for v, _ in K_rep['terms'].values()), Q(0))
    rss_sq = sum((v * v for v, _ in K_rep['terms'].values()), Q(0))

    def validate_radius(radius):
        require(radius == K * tau_aw2 ** 2 == linear, 'the half-width is the full linear sum K_2^+ tau^2 (coherent worst case)')
        return True
    check('root_n_misuse',
          validate_radius(Ep['radius']) and rss_sq < linear * linear
          and rejected(lambda: validate_radius(sqrt_up(rss_sq)), 'root_sum_of_squares')
          and rejected(lambda: validate_radius(Ep['radius'] / sqrt_lo(len(meet))), 'divided_by_sqrt_N_faces')
          and rejected(lambda: validate_radius(Ep['radius'] / 64), 'divided_by_64'),
          linear_half_width=s(linear), rss_preview_decimal_up=dec_up(sqrt_up(rss_sq)))

    # -------------------- item 3: scope --------------------
    scope = {
        'statement': 'for every state omega in the whole set S(tau) of AQ1 subsequential limits (local trace-norm limits of centered '
                     'whole-star box ground states, N>=2) at the zero selected triple, and for every such box and on-site cutoff, '
                     'omega_tau(W) lies in [tau/144 - K_2^+ tau^2, tau/144 + K_2^+ tau^2]',
        'set': 'whole set of AQ1 subsequential limits', 'triple': ['0', '0', '0'], 'uniform_in_N': True,
        'passage': 'local trace-norm convergence on R (|omega(W)-omega_{N_k}(W)|<=||W|| ||rho_R-rho_{N_k,R}||_1, ||W||<=1; closed interval)',
        'effect': 'static equal-time mean', 'sub_label': 'static_not_dynamic',
        'uniqueness_claimed': False, 'rate_in_N_claimed': False, 'whole_sequence_convergence_claimed': False,
        'minus_tau_pointwise': 'only along a common subsequence (flip lemma: S(-tau)=S(tau) o alpha_E as sets)',
        'finite_graph_transfer': False,
    }

    def validate_scope(sc):
        require(sc['set'] == 'whole set of AQ1 subsequential limits' and sc['triple'] == ['0', '0', '0'], 'scope set or triple changed')
        require(sc['uniform_in_N'] is True and sc['passage'].startswith('local trace-norm convergence'), 'passage must be uniform-in-N local trace norm')
        require(sc['uniqueness_claimed'] is False and sc['rate_in_N_claimed'] is False and sc['whole_sequence_convergence_claimed'] is False,
                'uniqueness, rate or whole-sequence convergence claimed')
        require(sc['minus_tau_pointwise'].startswith('only along a common subsequence'), 'pointwise -tau pairing needs a common subsequence')
        require(sc['finite_graph_transfer'] is False and sc['sub_label'] == 'static_not_dynamic', 'finite-graph transfer or dynamical relabel')
        return True
    lo_p, hi_p = Ep['lower'], Ep['upper']
    seq_a = [hi_p - (hi_p - lo_p) / (k + 2) for k in range(6)]      # synthetic local expectations along two subsequences
    seq_b = [lo_p + (hi_p - lo_p) / (k + 2) for k in range(6)]
    check('aq1_whole_set_scope',
          validate_scope(scope) and all(lo_p <= x <= hi_p for x in seq_a + seq_b) and hi_p != lo_p
          and rejected(lambda: validate_scope(dict(scope, uniqueness_claimed=True)), 'uniqueness_claimed')
          and rejected(lambda: validate_scope(dict(scope, minus_tau_pointwise='pointwise for AQ1 chosen states')), 'pointwise_minus_tau_without_common_subsequence')
          and rejected(lambda: validate_scope(dict(scope, rate_in_N_claimed=True)), 'rate_in_N_claimed')
          and rejected(lambda: validate_scope(dict(scope, triple=['0', '1/100', '0'])), 'nonzero_triple')
          and rejected(lambda: validate_scope(dict(scope, finite_graph_transfer=True)), 'finite_graph_transfer'),
          scope=scope,
          synthetic_two_limit_fixture={'limits': [s(hi_p), s(lo_p)], 'both_in_closed_interval': True, 'distinct': True,
                                       'label': 'synthetic sequences; illustrates that the statement covers every subsequential limit without uniqueness'})

    def box_inputs(N):
        anchors_ok = all(all(-N <= b[i] and b[i] + 1 <= N for i in range(3)) for b in (x['anchor'] for x in meet.values()))
        return {'N': N, 'faces_meeting_R_retained': sum(1 for x in meet.values() if all(-N <= x['anchor'][i] and x['anchor'][i] + 1 <= N for i in range(3))),
                'stars': min(len(incoming(u, N)) for u in R_cover), 'faces_per_factor': len(at0), 'all_R_stars_retained': anchors_ok}

    def box_enclosure(bi):
        require(bi['N'] >= 2 and bi['stars'] == 4 and bi['all_R_stars_retained'], 'centered whole-star boxes N>=2 retain every star meeting R')
        Kb = k2_replay(tau_aw2, G, stars_per_site=bi['stars'], faces_per_factor=bi['faces_per_factor'])['K']
        require(Kb == K, 'box replay differs from the bulk constant')
        return enclosure(tau_aw2, K, c1)

    def validate_uniform(encs):
        require(all(e == encs[0] for e in encs), 'the enclosure must be the same formula at every box size (volume-uniform)')
        return True

    def extensive(N):
        # wrong: a half-width built from the total interaction norm 7|tau| x (number of retained anchors), which grows with N
        return dict(enclosure(tau_aw2, K, c1), radius=Q(7) * tau_aw2 * (2 * N) ** 3)
    b2, b3 = box_inputs(2), box_inputs(3)
    check('boundary_state_volume_uniform',
          b2['faces_meeting_R_retained'] == b3['faces_meeting_R_retained'] == 82 and b2['stars'] == b3['stars'] == 4
          and validate_uniform([box_enclosure(b2), box_enclosure(b3), Ep])
          and rejected(lambda: validate_uniform([extensive(2), extensive(3)]), 'extensive_N_dependent_radius')
          and rejected(lambda: box_enclosure(box_inputs(1)), 'N1_box_missing_incoming_stars_claimed_in_scope'),
          boxes={'N=2': {k: (str(v) if not isinstance(v, bool) else v) for k, v in b2.items()},
                 'N=3': {k: (str(v) if not isinstance(v, bool) else v) for k, v in b3.items()},
                 'N=1': {'stars_at_e_z': str(len(incoming(EZ, 1)))}},
          state='every AQ1 subsequential limit inherits the same closed enclosure (volume-uniform constant; local trace-norm passage)')

    def validate_effect_label(label):
        require(label == 'static_not_dynamic', 'a static equal-time mean is not a dynamical, mass-gap or susceptibility statement')
        return True

    def validate_below_cap_label(labels, t):
        require(('sign_certified_below_cap' in labels) == (t < cap), 'sign_certified_below_cap applies only when tau_AW2 is below the cap')
        return True
    sub_labels = ['static_not_dynamic']
    check('static_not_dynamic_effect',
          validate_effect_label('static_not_dynamic') and all(x in V['sub_labels'] for x in sub_labels) and validate_below_cap_label(sub_labels, tau_aw2)
          and rejected(lambda: validate_effect_label('dynamical_correction'), 'dynamical_relabel')
          and rejected(lambda: validate_effect_label('mass_gap_correction'), 'mass_shift_relabel')
          and rejected(lambda: validate_effect_label('susceptibility'), 'susceptibility_relabel')
          and rejected(lambda: validate_effect_label('centered_correlation_shift_resolved'), 'correlation_shift_resolved_relabel')
          and rejected(lambda: validate_below_cap_label(sub_labels + ['sign_certified_below_cap'], tau_aw2), 'below_cap_label_at_the_cap'),
          sub_labels=sub_labels, sign_certified_below_cap=False,
          centered_correlation_shift='unresolved (AV2 reference_unresolved)',
          note='omega(W) is an equal-time expectation in the ground/AQ state; no dynamics, mass shift or susceptibility is inferred')

    packet_model = {'model_id': V['model_id'], 'tau': s(tau_aw2), 'triple': ['0', '0', '0'], 'reference_route': V['reference_route'],
                    'state_provenance': V['state_provenance'], 'cover': 'R={0,e_z}'}

    def validate_model(pk):
        require(pk['model_id'] == 'AQ_patterned_zero_selected', 'model id')
        require(rat(pk['tau']) == tau_aw2, 'coupling changed')
        require([rat(x) for x in pk['triple']] == [0, 0, 0], 'selected triple changed')
        require(pk['reference_route'] == 'haar', 'reference route changed')
        require(pk['state_provenance'].startswith('AQ1_centered_whole_star_subsequence'), 'state provenance changed')
        require(pk['cover'] == 'R={0,e_z}', 'cover changed')
        return True
    muts = []
    for key, val in (('tau', '1/1000000000'), ('triple', ['0', '1/100', '0']), ('reference_route', 'selected_strip'),
                     ('model_id', 'FG_one_plaquette'), ('state_provenance', 'finite_volume_N=2'), ('cover', 'R={0}')):
        muts.append(rejected(lambda k=key, x=val: validate_model(dict(packet_model, **{k: x})), 'relabel_' + key))
    check('changed_model_relabelled',
          validate_model(packet_model) and len(muts) == 6 and fixture_labels['transfers_to_aq'] is False,
          packet_model=packet_model, rejected_relabels=muts)

    check('av1_compatibility',
          max(abs(Ep['lower']), abs(Ep['upper']), abs(Em['lower']), abs(Em['upper'])) <= D_ii,
          D_ii=s(D_ii), ratio_D_ii_over_upper_decimal_down=dec_down(D_ii / Ep['upper']),
          note='the AV1 admitted |omega(W)|<=D_ii contains both enclosures')

    # -------------------- arithmetic, preview and calculator --------------------
    forbidden = ('mp' + 'math', 'num' + 'py', 'fl' + 'int', 'sym' + 'py', 'sci' + 'py', 'arb_' + 'preview')
    imports = []
    for name in ('check.py', 'calculator.py'):
        imports += [name + ': ' + ln.strip() for ln in (BASE / name).read_text(encoding='utf-8').splitlines()
                    if ln.startswith('import ') or ln.startswith('from ')]
    check('exact_arithmetic_admission',
          not any(any(fb in ln for fb in forbidden) for ln in imports)
          and rejected(lambda: rat(1e-08), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('NaN'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator')
          and calc_rejects({'tau': 1e-08}, 'calculator_float_tau') and calc_rejects({'tau': True}, 'calculator_bool_tau'),
          imports=imports, admission='fractions.Fraction only; decimals are directed previews (lower endpoints rounded down, upper up)')

    preview_raw = (BASE / PREVIEW_FILE).read_bytes()
    preview = json.loads(preview_raw.decode('utf-8'))
    exact_q = {sg: {'lower': E[sg]['lower'], 'upper': E[sg]['upper'], 'sign_margin': margins(E[sg])['sign_margin'],
                    'exclusion_margin': margins(E[sg])['exclusion_margin']} for sg in E}

    def validate_preview(pv):
        require(pv['preview_only'] is True and pv['used_for_admission'] is False and pv['label'].startswith('PREVIEW ONLY'), 'preview label')
        for sg in ('+', '-'):
            for name, xq in exact_q[sg].items():
                qq = pv['quantities'][sg][name]
                for backend in ('arb_ball_bounds', 'mpmath_iv_bounds'):
                    lo_, hi_ = rat(qq[backend]['lower']), rat(qq[backend]['upper'])
                    require(lo_ <= xq <= hi_, 'exact value outside the %s preview (%s %s)' % (backend, sg, name))
                    require(hi_ - lo_ <= abs(xq) / Q(10) ** 60, 'preview interval too wide')
        return True
    pv_promoted = json.loads(preview_raw.decode('utf-8'))
    pv_promoted['used_for_admission'] = True
    pv_shifted = json.loads(preview_raw.decode('utf-8'))
    pv_shifted['quantities']['+']['lower']['arb_ball_bounds']['lower'] = s(Ep['lower'] + Q(1, 10 ** 20))
    pv_shifted['quantities']['+']['lower']['arb_ball_bounds']['upper'] = s(Ep['lower'] + Q(2, 10 ** 20))
    check('arb_mpmath_preview_labelled',
          validate_preview(preview)
          and rejected(lambda: validate_preview(pv_promoted), 'preview_promoted_to_admission')
          and rejected(lambda: validate_preview(pv_shifted), 'preview_excluding_exact_endpoint'),
          preview_file=PREVIEW_FILE, preview_sha256=sha_bytes(preview_raw), preview_libraries=preview['libraries'],
          preview_precision_bits=preview['precision_bits'],
          preview_text={sg: {n: preview['quantities'][sg][n]['arb_text'] for n in ('lower', 'upper', 'exclusion_margin', 'sign_margin')} for sg in ('+', '-')},
          label='labelled Arb/mpmath comparison (stored by arb_preview.py); never admission arithmetic')

    cases = [({'tau': s(2 * tau_aw2)}, 'tau_above_cap'), ({'tau': '0'}, 'tau_zero_free_reference'),
             ({'tau': s(tau_aw2), 'selected': ('0', '1/100', '0')}, 'nonzero_triple'),
             ({'tau': s(tau_aw2), 'selected': ('0', '0')}, 'triple_wrong_length'),
             ({'tau': s(tau_aw2), 'selected': ('0', 0.0, '0')}, 'float_in_triple'),
             ({'tau': s(tau_aw2 / 10), 'fixed_design': True}, 'fixed_design_changed_tau'),
             ({'tau': s(tau_aw2), 'fixed_design': 'yes'}, 'fixed_design_not_boolean'),
             ({'tau': s(tau_aw2), 'alpha': '-1'}, 'negative_alpha'), ({'tau': 'abc'}, 'malformed_tau'),
             ({'tau': '1/0'}, 'zero_denominator_tau'), ({'tau': s(tau_aw2), 'tier': 'crude'}, 'crude_tier_certificate'),
             ({'tau': s(tau_aw2), 'K_2_plus': s(K)}, 'user_supplied_K_2_plus'), ({'tau': s(tau_aw2), 'K': '1'}, 'user_supplied_K')]
    rej = [calc_rejects(kw, 'calculator_' + lab, (ValueError, TypeError)) for kw, lab in cases]
    check('calculator_domain_rejections', len(rej) == len(cases), rejected_cases=rej)

    GC = calc.gate_constants()
    cert = {'+': calc.enclose(tau=s(tau_aw2), fixed_design=True), '-': calc.enclose(tau=s(-tau_aw2), fixed_design=True)}
    below = calc.enclose(tau=s(tau_aw2 / 10))
    cert_ok = all(cert[sg]['enclosure'] == {'lower': s(E[sg]['lower']), 'upper': s(E[sg]['upper'])}
                  and cert[sg]['exclusion_margin'] == s(margins(E[sg])['exclusion_margin']) and cert[sg]['sign_margin'] == s(margins(E[sg])['sign_margin'])
                  and cert[sg]['sub_labels'] == ['static_not_dynamic'] and cert[sg]['sign_certified_below_cap'] is False
                  and cert[sg]['resolved_interaction_shift_at_cap'] is True and cert[sg]['excludes_zero'] is True
                  and cert[sg]['coupling_rule']['tau_AW2'] == s(tau_aw2) for sg in cert)
    check('calculator_fixed_design_matches',
          cert_ok and GC['K'] == K and GC['c1'] == c1 and GC['cap'] == cap and GC['rule_bound'] == R['bound']
          and cert['-']['mirrored_coupling_replay'] is True and cert['+']['sign_of_omega_W'] == '+' and cert['-']['sign_of_omega_W'] == '-'
          and below['sub_labels'] == ['static_not_dynamic', 'sign_certified_below_cap'] and below['resolved_interaction_shift_at_cap'] is False
          and below['fixed_design'] is False,
          calculator_sha256=calc_sha, fixed_design={sg: {'enclosure': cert[sg]['enclosure'], 'decimal_outward': cert[sg]['enclosure_decimal_outward'],
                                                        'exclusion_margin_decimal_down': cert[sg]['exclusion_margin_decimal_down'],
                                                        'sign_margin_decimal_down': cert[sg]['sign_margin_decimal_down']} for sg in cert},
          reusable_mode_example={'tau': below['tau'], 'sub_labels': below['sub_labels'], 'note': 'reusable mode below the cap; not the AW2 design'})

    verdict = classify(K, 'exact')
    check('aw2_verdict_classification',
          verdict == 'accepted_within_scope' and tau_aw2 == cap and m_p >= V['target'] and validate_below_cap_label(sub_labels, tau_aw2),
          proposed_verdict=verdict, sub_labels=sub_labels, sign_certified_below_cap=False,
          reason='0 strictly excluded at both signs at tau_AW2=10^-8 (the cap) with exclusion margin %s >= %s' % (dec_down(m_p), s(V['target'])))

    # -------------------- single producer, claims and coherent tampering --------------------
    reverse_isolation = ('not_applicable: single producer (contract producers=[forward], direction single+skeptic); admission requires '
                         'the skeptic\'s independent pre-comparison replay from the contract alone')

    def validate_producers(pk):
        require(pk['producers'] == ['forward'], 'single-direction loop: producers must be exactly [forward]')
        require(pk['single_direction_independent_replay_required'] is True, 'admission requires the skeptic independent replay')
        require('reverse_results_sha256' not in pk and 'reverse' not in pk, 'a fabricated reverse package is rejected')
        require(pk['reverse_premise_isolation'].startswith('not_applicable: single producer'), 'reverse premise isolation is not applicable here')
        require(pk['minus_tau_status'] == 'replay', 'the mirrored enclosure is a replay, not an independent confirmation')
        return True
    prod = {'producers': ['forward'], 'single_direction_independent_replay_required': True,
            'reverse_premise_isolation': reverse_isolation, 'minus_tau_status': 'replay'}
    check('single_producer_declared',
          validate_producers(prod) and V['producers'] == ['forward'] and V['direction'] == 'single+skeptic' and V['single_replay'] is True
          and c.get('reverse_premise_isolation') is None and not forbidden_current
          and rejected(lambda: validate_producers(dict(prod, producers=['forward', 'reverse'], reverse_results_sha256='0' * 64)), 'fabricated_reverse_package')
          and rejected(lambda: validate_producers(dict(prod, single_direction_independent_replay_required=False)), 'skeptic_replay_requirement_dropped')
          and rejected(lambda: validate_producers(dict(prod, reverse_premise_isolation='satisfied')), 'reverse_isolation_claimed_satisfied')
          and rejected(lambda: validate_producers(dict(prod, minus_tau_status='independent_confirmation')), 'mirror_claimed_independent'),
          producers=['forward'], reverse_premise_isolation=reverse_isolation,
          semantics=V['new_control_semantics']['single_producer_declared'])

    excludes_at_cap = Ep['lower'] > 0 and Em['upper'] < 0 and tau_aw2 == cap
    claim_flags = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': excludes_at_cap,
                   'static_not_dynamic': True, 'sign_certified_below_cap': False, 'dynamical_correction_claim': False,
                   'scientific_priority_verified': False, 'mass_shift_claim': False, 'susceptibility_claim': False,
                   'correlation_shift_resolved': False, 'uniqueness_claim': False, 'whole_sequence_convergence_claim': False,
                   'rate_in_N_claim': False, 'third_order_remainder_claim': False}
    must_false = ('continuum_claim', 'uniform_wilson_claim', 'sign_certified_below_cap', 'dynamical_correction_claim',
                  'scientific_priority_verified', 'mass_shift_claim', 'susceptibility_claim', 'correlation_shift_resolved',
                  'uniqueness_claim', 'whole_sequence_convergence_claim', 'rate_in_N_claim', 'third_order_remainder_claim')

    def validate_flags(fl, exclusion_holds=excludes_at_cap):
        for k in must_false:
            require(fl[k] is False, 'claim flag must be false: ' + k)
        require(fl['static_not_dynamic'] is True, 'static_not_dynamic must be true')
        require(fl['resolved_interaction_shift'] is exclusion_holds, 'resolved_interaction_shift only if the exclusion holds at the cap')
        return True
    check('no_priority_or_continuum_claim',
          validate_flags(claim_flags) and claim_flags['resolved_interaction_shift'] is True
          and rejected(lambda: validate_flags(dict(claim_flags, continuum_claim=True)), 'continuum_claim_true')
          and rejected(lambda: validate_flags(dict(claim_flags, scientific_priority_verified=True)), 'priority_true')
          and rejected(lambda: validate_flags(dict(claim_flags, uniform_wilson_claim=True)), 'uniform_wilson_true')
          and rejected(lambda: validate_flags(dict(claim_flags, dynamical_correction_claim=True)), 'dynamical_correction_true')
          and rejected(lambda: validate_flags(claim_flags, Ec['lower'] > 0), 'shift_resolved_with_crude_enclosure_containing_zero'),
          flags=claim_flags, historical_or_occult_numeric_premise=False, claim_exclusions=V['claim_exclusions'])

    # -------------------- assemble packet and tampering control --------------------
    headline = {'tau_AW2': s(tau_aw2), 'K_2_plus': s(K), 'K_2_plus_decimal_up': dec_up(K), 'first_order_coefficient': '+tau/' + str(c1.denominator),
                'enclosure_plus': {'lower': s(Ep['lower']), 'upper': s(Ep['upper'])},
                'enclosure_minus': {'lower': s(Em['lower']), 'upper': s(Em['upper'])},
                'enclosure_plus_decimal_outward': {'lower': rec['+']['lower_decimal_outward_down'], 'upper': rec['+']['upper_decimal_outward_up']},
                'enclosure_minus_decimal_outward': {'lower': rec['-']['lower_decimal_outward_down'], 'upper': rec['-']['upper_decimal_outward_up']},
                'exclusion_margin': s(m_p), 'exclusion_margin_decimal_down': dec_down(m_p),
                'sign_margin': s(S_p), 'sign_margin_decimal_down': dec_down(S_p), 'target_exclusion_margin': s(V['target'])}
    packet = {
        'loop': 'AW2', 'direction': 'forward', 'human_author': 'Hruday N M (BUNZEEY)',
        'contribution_alias': 'HNM-AW2-F forward sign-certified enclosure of the Wilson mean at the AW1-frozen coupling',
        'producers': ['forward'], 'single_direction_independent_replay_required': True,
        'reverse_premise_isolation': reverse_isolation, 'minus_tau_status': 'replay',
        'contract_sha256': CONTRACT_SHA256, 'aw1_gate_sha256': AW1_GATE_SHA256, 'av1_gate_sha256': A1['sha256'],
        'check_py_sha256_recorded_before_evaluation': check_sha, 'calculator_py_sha256_recorded_before_evaluation': calc_sha,
        'model': packet_model, 'tau_values': {'+': s(tau_aw2), '-': s(-tau_aw2)},
        'headline': headline, 'enclosures': rec, 'error_terms_itemized': ledger, 'scope': scope,
        'sub_labels': sub_labels, 'proposed_verdict': verdict + ' (forward, single direction; admission requires the skeptic independent replay)',
        'premise_snapshots': {k: inventory[k] for k in sorted(inventory)},
        'disclosed_extra_reads': DISCLOSED_EXTRA_READS,
        'finite_fixture_labels': fixture_labels,
        'claim_exclusions_contract': V['claim_exclusions'], 'claim_exclusions_preregistration': V['prereg_exclusions'],
    }
    packet.update(claim_flags)

    def packet_hash(pk):
        body = {k: v for k, v in pk.items() if k != 'packet_sha256'}
        return sha_bytes(json.dumps(body, sort_keys=True).encode('utf-8'))

    def validate_packet(pk, inv, contract_bytes=contract_raw, gate_bytes=gate_raw):
        require(pk.get('packet_sha256') == packet_hash(pk), 'packet hash mismatch')
        ids = {ch['id']: ch for ch in pk['checks']}
        for cid in V['controls']:
            if cid == 'coherent_evidence_tampering':
                continue
            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)
        validate_flags(pk)
        validate_producers(pk)
        require(sorted(inv) == expected_inputs and all(pk['premise_snapshots'].get(k) == inv[k] for k in inv)
                and sorted(pk['premise_snapshots']) == expected_inputs, 'premise snapshot inventory incomplete or rebound')
        require(pk['contract_sha256'] == CONTRACT_SHA256 == sha_bytes(contract_bytes), 'contract snapshot hash mismatch')
        parse_contract(contract_bytes)
        Gx = parse_gate(gate_bytes)
        require(pk['aw1_gate_sha256'] == AW1_GATE_SHA256, 'gate hash rebound')
        require(rat(pk['headline']['K_2_plus']) == Gx['K'], 'headline K_2^+ differs from the hash-verified gate')
        tx = aw2_rule(Gx['K'], R)[0]
        require(rat(pk['headline']['tau_AW2']) == tx, 'tau_AW2 differs from the frozen rule')
        ex = enclosure(tx, Gx['K'], Gx['c1'])
        require(rat(pk['headline']['enclosure_plus']['lower']) == ex['lower'] and rat(pk['headline']['enclosure_plus']['upper']) == ex['upper'],
                'enclosure differs from recomputation')
        require(rat(pk['headline']['exclusion_margin']) == margins(ex)['exclusion_margin'], 'margin differs from recomputation')
        return True

    base_packet = dict(packet)
    base_packet['checks'] = [dict(ch) for ch in CHECKS]
    base_packet['packet_sha256'] = packet_hash(base_packet)

    def tampered(edit, inv=None, contract_bytes=contract_raw, gate_bytes=gate_raw):
        pk = json.loads(json.dumps(base_packet))
        edit(pk)
        pk['packet_sha256'] = packet_hash(pk)
        return validate_packet(pk, inventory if inv is None else inv, contract_bytes, gate_bytes)

    def flip_control(pk):
        for ch in pk['checks']:
            if ch['id'] == 'free_reference_exclusion':
                ch['passed'] = False

    def drop_snapshot(pk):
        pk['premise_snapshots'].pop('research/round32/skeptic/aw1.md')
    inv_missing = dict(inventory)
    inv_missing.pop('research/round32/skeptic/aw1.md')
    contract_edit = contract_raw.replace(b'"value": "2"', b'"value": "1"')
    require(contract_edit != contract_raw, 'contract edit fixture')
    gate_edit = gate_raw.replace(str(K.numerator).encode(), str(2 * K.numerator).encode())
    require(gate_edit != gate_raw, 'gate edit fixture')
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory) and sha_bytes(contract_raw) == CONTRACT_SHA256 and sha_bytes(gate_raw) == AW1_GATE_SHA256
          and rejected(lambda: tampered(flip_control), 'control_boolean_flipped_hash_rebound')
          and rejected(lambda: tampered(drop_snapshot, inv_missing), 'snapshot_removed_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline'].update(K_2_plus=s(K / 2))), 'K_2_plus_halved_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline'].update(K_2_plus=s(K_forward_headline))), 'K_2_plus_forward_headline_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline'].update(tau_AW2=s(tau_aw2 / 10))), 'tau_AW2_changed_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline']['enclosure_plus'].update(lower=s(Q(0)))), 'lower_endpoint_changed_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk.update(sign_certified_below_cap=True)), 'below_cap_flag_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk.update(producers=['forward', 'reverse'])), 'reverse_producer_added_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk.update(contract_sha256=sha_bytes(contract_edit)), contract_bytes=contract_edit), 'contract_target_edited_and_rehashed')
          and rejected(lambda: tampered(lambda pk: pk['headline'].update(K_2_plus=s(2 * K)), gate_bytes=gate_edit), 'gate_K_doubled_and_rehashed'),
          contract_snapshot_sha256_matches=sha_bytes(contract_raw) == CONTRACT_SHA256,
          aw1_gate_snapshot_sha256_matches=sha_bytes(gate_raw) == AW1_GATE_SHA256)

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    no_mutation = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch['mutations_rejected']]
    require(not no_mutation, 'contract controls without a damaging mutation: ' + ','.join(no_mutation))
    require(not PENDING, 'mutations evaluated outside a check')
    packet['checks'] = CHECKS
    packet['check_count'] = str(len(CHECKS))
    packet['mutations_rejected_count'] = str(sum(len(ch['mutations_rejected']) for ch in CHECKS))
    packet['contract_controls_covered'] = sorted(V['controls'])
    return packet


def main():
    ap = argparse.ArgumentParser(description='AW2 forward exact checker')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    require(out.is_absolute(), 'absolute output directory required')
    out = out.resolve()
    require(not out.exists(), 'fresh (non-existent) output directory required')
    require(ROOT not in out.parents and out != ROOT, 'output directory must be outside the checkout')
    check_sha = sha(BASE / 'check.py')          # recorded before any evaluation
    calc_sha = sha(BASE / 'calculator.py')
    result = compute(check_sha, calc_sha)
    require(no_numbers(result), 'a non-string number in results')
    out.mkdir(parents=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    sources = {}
    for p in sorted(BASE.rglob('*')):
        rel = p.relative_to(BASE)
        if p.is_file() and (rel.parts[0] == 'inputs' or p.name in ('check.py', 'calculator.py', 'arb_preview.py', PREVIEW_FILE)):
            sources[rel.as_posix()] = sha(p)
    manifest = {'loop': 'AW2', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')},
                'note': 'report.md is bound by freeze.json, not by this manifest'}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AW2', 'direction': 'forward', 'checks': result['check_count'],
                      'tau_AW2': result['headline']['tau_AW2'],
                      'enclosure_plus': result['headline']['enclosure_plus_decimal_outward'],
                      'exclusion_margin': result['headline']['exclusion_margin_decimal_down'],
                      'sign_margin': result['headline']['sign_margin_decimal_down'],
                      'verdict': result['proposed_verdict']}, sort_keys=True))


if __name__ == '__main__':
    main()
