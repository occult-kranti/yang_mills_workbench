#!/usr/bin/env python3
"""AX2 forward (single producer): exact checks for the Hruday uniform-model window certificate.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

The AV2 window lemma is applied verbatim to the uniform Kogut-Susskind SU(2)
model at fixed spacing and strong bare coupling (route B of AX1): the same C^2
window and conventions (M_0=2, M_1=4s/pi), the uniform slope k'=51|tau|/4 (seven
whole stars and two single-factor selected groups meeting the cover) and the
uniform state bound D' bound by the AX1 gate. tau=+10^-8, s=1; the -10^-8 value
is the U_E mirror and a replay.

Standard library only (fractions, hashlib, json, argparse, re, math via
calculator.py). Every admission Boolean is decided in exact Fraction arithmetic;
decimal strings are outward-rounded previews. Conditions raise AdmissionError
explicitly (never `assert`), so every check stays active under `python -O`.
Every number in results.json is a string.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction as Q
from math import comb
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))
import calculator as calc  # noqa: E402  (same producer closure; no bytecode written)

CONTRACT_REL = 'research/round32/contracts/ax2.json'
CONTRACT_SHA256 = 'da72afe377d7601e6b6ec3835ab69d05813cb26c4b46f67485a4d8e0c055992b'
AX1_GATE_REL = 'research/round32/advisor/ax1-gate.json'
AX1_GATE_SHA256 = '1b8fb152696659439bb01fc7df429fc76fa3132d4936df450d8131256015d177'
SELECTION_REL = 'research/round32/advisor/selection-ax2.md'
SELECTION_SHA256 = '9ffe2c02a6c8586a5ebf9ba2fb24f948bc885eb306036290cc5f723d4d15a980'
AV2_GATE_REL = 'research/round32/advisor/av2-gate.json'
AV2_CONTRACT_REL = 'research/round32/contracts/av2.json'
AX1_CONTRACT_REL = 'research/round32/contracts/ax1.json'
AX1_FWD_REL = 'research/round32/forward/ax1/report.md'
AT4_FWD_REL = 'research/round31/forward/at4/report.md'
AV2_CALC_REL = 'research/round32/forward/av2/calculator.py'
TIER = calc.STATE_TIER


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
    entry = {'id': identity, 'passed': True}
    entry.update(details)
    if PENDING:
        entry['rejected_mutations'] = list(PENDING)
        PENDING.clear()
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run a damaging mutation; it must raise AdmissionError."""
    try:
        mutation()
    except AdmissionError:
        PENDING.append(label)
        return label
    raise AdmissionError('damaging mutation accepted: ' + label)


def calc_rejects(kwargs, label, errors=(ValueError,)):
    """A calculator call outside the proved domain must raise an input error."""
    try:
        calc.certify(**kwargs)
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


def s_(q):
    return calc.textq(q)


def dec(q, digits=12, mode='up'):
    """Scientific decimal of an exact rational rounded outward (display only)."""
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
    magnitude_up = (mode == 'up') != neg
    if magnitude_up and m * scaled.denominator != scaled.numerator:
        m += 1
    if m >= 10 ** digits:
        m //= 10
        e += 1
    t = str(m)
    return ('-' if neg else '') + t[0] + '.' + t[1:] + 'e' + str(e)


def fixed(q, places, mode):
    """Fixed-point decimal rounded down or up (display only)."""
    q = Q(q) * 10 ** places
    n = q.numerator // q.denominator
    if mode == 'up' and n * q.denominator != q.numerator:
        n += 1
    sign = '-' if n < 0 else ''
    n = abs(n)
    t = str(n).rjust(places + 1, '0')
    return sign + t[:-places] + '.' + t[-places:]


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def match(pattern, text, label):
    m = re.search(pattern, text)
    require(m is not None, 'text not parsed: ' + label)
    return m


def dec_ratio(text):
    """Decimal like 0.000841519 or 1.91e-7 as an exact rational."""
    require(re.fullmatch(r'\d+(\.\d+)?(e-?\d+)?', text) is not None, 'bad decimal ' + text)
    return Q(text)


def snapshot(rel):
    path = BASE / 'inputs' / rel
    require(path.is_file(), 'missing premise snapshot ' + rel)
    return path.read_bytes()


# ---------------------------------------------------------------------------
# Contract, gates and inherited reports (every target/reference/state value).
# ---------------------------------------------------------------------------
def load_contract():
    raw = snapshot(CONTRACT_REL)
    require(sha_bytes(raw) == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen AX2 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AX2' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return raw, c


def contract_values(c):
    p = c['parameters']
    pre = c['preregistration']
    V = {}
    V['tau'] = rat(p['tau'])
    require(V['tau'] > 0, 'frozen coupling must be the positive cap')
    V['s'] = rat(p['s'])
    kp = match(r'^(\d+)\|tau\|/(\d+)$', p['k_prime'], 'k_prime')
    V['k_over_tau'] = Q(int(kp.group(1)), int(kp.group(2)))
    dp = match(r'^(\d+)/(\d+) \(forward AX1 tier ii, admitted in research/round32/advisor/ax1-gate\.json; '
               r'the AX1 target value and the reverse refinement are never substituted\)$', p['D_prime'], 'D_prime')
    V['D_prime'] = Q(int(dp.group(1)), int(dp.group(2)))
    require(p['window'] == 'AV2 C^2 window', 'window must be the AV2 C^2 window')
    V['target'] = rat(p['target'])
    pv = match(r'^about 2\((\d\.\d+e-\d+)\)\+(\d+)e-(\d+)/pi ~ (\d\.\d+e-\d+) \(planning preview; not a result\)$',
               p['preview_radius'], 'preview')
    V['preview_D'] = dec_ratio(pv.group(1))
    V['preview_slope_numerator'] = Q(int(pv.group(2)), 10 ** int(pv.group(3)))
    V['preview_radius'] = dec_ratio(pv.group(4))
    V['K2_note'] = p['K_2_note']
    require('no uniform-model K_2 is admitted' in V['K2_note'] and 'no sign certificate rider' in V['K2_note'], 'K_2 note')
    model = c['model']
    V['model_text'] = model
    g4 = match(r'g\^4=(\d+(?:\.\d+)?)x10\^(\d+)', model, 'g^4')
    V['g4'] = Q(g4.group(1)) * 10 ** int(g4.group(2))
    for phrase in ('Uniform Kogut-Susskind SU(2) at fixed spacing (route B, AX1)', 'tau=+10^-8 (and -10^-8 as a replay)',
                   's=1', 'original xz Wilson', 'Haar reference'):
        require(phrase in model, 'model string lacks ' + phrase)
    V['model_id'] = pre['model_id']
    require(V['model_id'] == 'AQ_uniform_routeB', 'model id')
    V['triple_symbolic'] = list(pre['selected_triple_alpha_units'])
    require(V['triple_symbolic'] == ['tau/24'] * 3, 'uniform selected triple tau/24 required')
    require(rat(pre['tau']['value']) == V['tau'] and pre['tau']['signs_evaluated'] == ['+', '-']
            and pre['tau']['is_model_change_vs_previous_loop'] is False, 'preregistered coupling block')
    V['state_provenance'] = pre['state_provenance']
    ob = pre['observable']
    rf = match(r'^exp\(-(\d+)\)/(\d+) enclosed$', ob['reference_value_exact'], 'reference exact')
    V['free_energy'], V['free_den'] = int(rf.group(1)), int(rf.group(2))
    require(ob['id'] == 'C(s)' and ob['centering'] == 'vector' and ob['reference_route'] == 'haar', 'observable block')
    V['node_s_values'] = [rat(x) for x in pre['nodes']['s_values']]
    require(V['node_s_values'] == [V['s']] and pre['nodes']['post_hoc_node_selection'] == 'forbidden', 'node declaration')
    V['error_terms'] = list(pre['error_terms_itemized'])
    tg = pre['target']
    require(tg['quantity'] == 'radius' and tg['comparator'] == '<=' and rat(tg['value']) == V['target'], 'preregistered target differs')
    V['controls'] = list(c['controls'])
    V['controls_mirror'] = list(pre['controls_required']['ids'])
    V['sub_labels_allowed'] = list(pre['sub_labels_allowed'])
    V['claim_exclusions'] = list(c['claim_exclusions'])
    V['prereg_exclusions'] = list(pre['claim_exclusions'])
    V['shared_premises'] = list(c['shared_premises'])
    V['forward_additional'] = list(c.get('forward_additional_premises', []))
    V['producers'] = list(c['producers'])
    V['direction'] = c['direction']
    V['single_replay'] = c.get('single_direction_independent_replay')
    V['semantics'] = dict(c['new_control_semantics'])
    V['acceptance'] = dict(c['acceptance'])
    V['required'] = list(c['required'])
    return V


def load_ax1_gate():
    raw = snapshot(AX1_GATE_REL)
    require(sha_bytes(raw) == AX1_GATE_SHA256, 'AX1 gate snapshot bytes differ from the admitted gate')
    g = json.loads(raw.decode('utf-8'))
    require(g.get('loop') == 'AX1' and g.get('verdict') == 'accepted_within_scope', 'AX1 gate identity/verdict')
    a, d = g['accepted'], g['decision']
    G = {'raw_sha256': sha_bytes(raw), 'bindings': dict(g['bindings'])}
    dm = match(r"Bind the forward D'_ii = (\d+)/(\d+) \(about 1\.4446e-8; certified by both inequalities\) "
               r"as the admitted uniform state bound for AX2", d, 'gate decision D\'')
    G['D_prime'] = Q(int(dm.group(1)), int(dm.group(2)))
    da = match(r"tier \(ii\) with t_1'=(\d+)\|tau\|/(\d+), T'=t_1'/\(1-(\d+)J'\)=(\d+)/(\d+), rho'=352J'T' gives the bound value "
               r"D'_ii=(\d+)/(\d+) \(~1\.44459e-8; 2eps\(1\+eps\)/\(1\+eps\^2\) with eps=2T'\+T'\^2", a, 'gate tier ii formula')
    G['t1_over_tau'] = Q(int(da.group(1)), int(da.group(2)))
    G['remainder_factor'] = int(da.group(3))
    G['T_prime_cap'] = Q(int(da.group(4)), int(da.group(5)))
    G['D_prime_accepted'] = Q(int(da.group(6)), int(da.group(7)))
    rr = match(r"the reverse's labelled R-refinement D'_ii=(\d+)/(\d+) \(~1\.22237e-8", a, 'gate reverse refinement')
    G['D_reverse_refinement'] = Q(int(rr.group(1)), int(rr.group(2)))
    ti = match(r"tier \(i\) D'_i~(\d\.\d+e-\d+) fails and is retained", a, 'gate tier i')
    G['D_tier_i_decimal'] = dec_ratio(ti.group(1))
    G['J_over_tau'] = int(match(r"every face charged once; J'=(\d+)\|tau\|;", a, 'gate J\'').group(1))
    j0 = match(r"J' exceeds AM2's J_0=(\d+)/(\d+) at the cap; with the re-frozen J_0'=(\d+)/10\^(\d+) \(R1\) the exact inequalities "
               r"J_0'G\(R\)<(\d+)/(\d+)<1/64 and 2J_0'G'\(R\)<(\d+)/(\d+)<1 hold", a, 'gate J_0 resolution')
    G['J0_old'] = Q(int(j0.group(1)), int(j0.group(2)))
    G['J0_prime'] = Q(int(j0.group(3)), 10 ** int(j0.group(4)))
    G['self_map'] = Q(int(j0.group(5)), int(j0.group(6)))
    G['contraction'] = Q(int(j0.group(7)), int(j0.group(8)))
    G['gap_statement'] = 'full-space gap >=1/2 normalized (alpha/16 physical)' in a
    rs = match(r"reset omega\(h_R\)<=(\d+)\|tau\|; with the Haar gap six epsilon_R<=(\d+)\|tau\| and 2sqrt\((\d+)\|tau\|\)<=1/500 "
               r"\(square-root control only; gap one fails\)", a, 'gate reset')
    G['reset'], G['eps_R'], G['sqrt_arg'] = int(rs.group(1)), int(rs.group(2)), int(rs.group(3))
    G['verbatim_steps'] = ('compactness, stationarity, GNS, nonnegativity, gauge averaging, the gap alpha/16, '
                           'cutoff-vector removal and AQ passage re-apply verbatim') in a
    inc = match(r"exactly (\d+) whole stars \(anchors R-S\) and (\d+) single-factor groups meet R, charging (\d+) faces, "
                r"(\d+) meeting R \((\d+) omitted \+ (\d+) selected, the 6 selected being the two single groups\) and (\d+) inside R, "
                r"none twice; \|\|B_N\|\|<=(\d+)\|tau\|/(\d+), k'=(\d+)\|tau\|/(\d+) in G units", a, 'gate incidence')
    G['inc'] = {'stars': int(inc.group(1)), 'groups': int(inc.group(2)), 'faces': int(inc.group(3)), 'meeting': int(inc.group(4)),
                'omitted_meeting': int(inc.group(5)), 'selected_meeting': int(inc.group(6)), 'inside': int(inc.group(7))}
    G['B_over_tau'] = Q(int(inc.group(8)), int(inc.group(9)))
    G['k_over_tau'] = Q(int(inc.group(10)), int(inc.group(11)))
    G['state_consequences'] = ("|omega(W)|<=D', |omega(W^2)-1/4|<=D'/2, m^2<=D'^2, passing to every AQ1 subsequential limit "
                               "as uniform local closeness") in a
    G['flip'] = ("U_E H_N(tau) U_E^*=H_N(-tau) in every box and cutoff" in a and "C_N, c_N even" in a
                 and 'S(-tau)=S(tau) o alpha_E as whole sets' in a)
    G['first_order_den'] = int(match(r"omega\(W\)\^\{\(1\)\}=\+tau/(\d+)", a, 'gate first order').group(1))
    G['no_node_no_K2'] = ('No Euclidean node, K_2 or uniform omega(W^2) constant (not transferred), uniform Wilson-mean sign '
                          'certificate, weak-coupling, continuum, uniqueness, rate or priority statement is admitted') in a
    G['model'] = g['model']
    require('tau=96/g^4; g^4=9.6x10^9 at the cap' in g['model'], 'gate model dictionary')
    G['limitations'] = list(g['limitations'])
    return G


def bound_snapshot(rel, G1):
    """A premise snapshot whose sha256 is bound by the hash-pinned AX1 gate."""
    raw = snapshot(rel)
    require(G1['bindings'].get(rel) == sha_bytes(raw), 'snapshot not bound by the AX1 gate: ' + rel)
    return raw


def load_av2_gate(G1):
    raw = bound_snapshot(AV2_GATE_REL, G1)
    g = json.loads(raw.decode('utf-8'))
    require(g.get('loop') == 'AV2' and g.get('verdict') == 'accepted_within_scope', 'AV2 gate identity/verdict')
    a = g['accepted']
    G = {'sha256': sha_bytes(raw), 'bindings': dict(g['bindings'])}
    w = match(r"the frozen C\^2 window g\(x\)=e\^\{-sx\} \(x>=0\), e\^\{sx\}\(1-(\d)sx\+(\d)s\^2x\^2\) \(x<0\) has "
              r"ghat=(\d)s\^3/\(pi\(s-i theta\)\^3\(s\+i theta\)\) in L\^1 with M_0=\|\|ghat\|\|_1=(\d), M_1=(\d)s/pi, M_2=(\d)s\^2", a, 'AV2 window')
    G['c1_over_s'], G['c2_over_s2'], G['ghat_coeff'], G['M0'], G['M1_coeff'], G['M2_coeff'] = (int(w.group(i)) for i in range(1, 7))
    G['lemma'] = 'the window lemma C(s)=int ghat c uses L^1 inversion, Fubini and AQ1 nonnegativity only (no AQ2 gap)' in a
    k = match(r"the seven-star relative-unitary Duhamel slope k=(\d+)\|tau\|/(\d+) holds for every real theta uniformly in the box", a, 'AV2 k')
    G['k_over_tau'] = Q(int(k.group(1)), int(k.group(2)))
    dd = match(r"forward tier-\(ii\) bound D=(\d+)/(\d+) \(~1\.3612e-8\) by trace duality with no D/2 effect refinement", a, 'AV2 D')
    G['D_av1_zero_selected'] = Q(int(dd.group(1)), int(dd.group(2)))
    G['datum'] = Q(int(match(r"exact rational datum d=(\d+)/\(4\*10\^40\)", a, 'AV2 datum').group(1)), 4 * 10 ** 40)
    G['R'] = Q(int(match(r"r<=R=(\d+)/10\^40", a, 'AV2 R').group(1)), 10 ** 40)
    ss = match(r"s\* in \[(\d+\.\d+), (\d+\.\d+)\]", a, 'AV2 s*')
    G['s_star'] = (Q(ss.group(1)), Q(ss.group(2)))
    G['floor_decimal'] = dec_ratio(match(r"at least (\d\.\d+e-\d+) for every cutoff L even with D->0", a, 'AV2 floor').group(1))
    return G


def load_av2_contract(G1):
    raw = bound_snapshot(AV2_CONTRACT_REL, G1)
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AV2', 'AV2 contract identity')
    p = c['parameters']
    W = {}
    w = match(r'^g\(x\)=e\^\{-sx\} for x>=0; g\(x\)=e\^\{sx\}\(1-(\d+)sx\+(\d+)s\^2x\^2\) for x<0$', p['window'], 'AV2 contract window')
    W['c1_over_s'], W['c2_over_s2'] = int(w.group(1)), int(w.group(2))
    t = match(r'^ghat\(theta\)=(\d+)s\^3/\(pi\(s-i theta\)\^3\(s\+i theta\)\), \|ghat\|=\((\d+)s\^3/pi\)\(s\^2\+theta\^2\)\^-2, '
              r'\|\|ghat\|\|_1=(\d+), int\|theta\|\|ghat\|=(\d+)s/pi, int theta\^2\|ghat\|=(\d+)s\^2$', p['window_transform'], 'AV2 transform')
    W['ghat_coeff'], W['abs_coeff'], W['M0'], W['M1_coeff'], W['M2_coeff'] = (int(t.group(i)) for i in range(1, 6))
    sem = c['new_control_semantics']['window_fourier_sign_convention']
    W['sign_mutation_multiplier'] = int(match(r'returns g\(-3\)/4=(\d+)e\^\{-3\}/4 on the free atom', sem, 'AV2 sign').group(1))
    W['convention_required'] = c['required'][0]
    require("c(theta)=<chi,e^{i theta G}chi> and ghat(theta)=(2pi)^-1 int g(x)e^{-i theta x}dx" in W['convention_required'],
            'AV2 frozen conventions')
    return W


def load_ax1_contract(G1):
    raw = bound_snapshot(AX1_CONTRACT_REL, G1)
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AX1', 'AX1 contract identity')
    note = c['parameters']['d_prime_note']
    th = match(r"i\.e\. D'<=(\d\.\d+)x10\^-(\d+);", note, 'AX1 d_prime_note')
    return {'target': rat(c['preregistration']['target']['value']),
            'note_threshold': Q(th.group(1)) / 10 ** int(th.group(2)),
            'J0_resolution': c['parameters']['J0_resolution']}


def load_ax1_forward_tier_i(G1):
    text = bound_snapshot(AX1_FWD_REL, G1).decode('utf-8')
    m = match(r"D'_i=\\tfrac\{(\d+)\}\{(\d+)\}\\approx2\.45260902280", text, 'AX1 forward tier (i) exact')
    return Q(int(m.group(1)), int(m.group(2)))


def load_at4_decimal(G1):
    text = bound_snapshot(AT4_FWD_REL, G1).decode('utf-8')
    return dec_ratio(match(r'Their sum is `mathcal E\^\+≈(0\.\d+)`', text, 'AT4 radius decimal').group(1))


# ---------------------------------------------------------------------------
# Gaussian rationals and univariate polynomials (exact algebra).
# ---------------------------------------------------------------------------
def cx(re_, im_=0):
    return (Q(re_), Q(im_))


def cadd(u, v):
    return (u[0] + v[0], u[1] + v[1])


def cmul(u, v):
    return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def cscale(u, q):
    return (u[0] * q, u[1] * q)


def cinv(u):
    n = u[0] * u[0] + u[1] * u[1]
    require(n != 0, 'division by zero in Gaussian rationals')
    return (u[0] / n, -u[1] / n)


def cpow(u, n):
    r = (Q(1), Q(0))
    for _ in range(n):
        r = cmul(r, u)
    return r


def cabs2(u):
    return u[0] * u[0] + u[1] * u[1]


def ptrim(p):
    p = [Q(x) for x in p]
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(p, q):
    n = max(len(p), len(q))
    return ptrim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def pscale(p, a):
    return ptrim([Q(a) * x for x in p])


def pmul(p, q):
    p, q = ptrim(p), ptrim(q)
    if not p or not q:
        return []
    r = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i + j] += x * y
    return ptrim(r)


def pder(p):
    p = ptrim(p)
    return ptrim([i * p[i] for i in range(1, len(p))])


def peval(p, x):
    return sum((c * Q(x) ** i for i, c in enumerate(ptrim(p))), Q(0))


def rderiv(r):
    num, den = r
    return (padd(pmul(pder(num), den), pscale(pmul(num, pder(den)), -1)), pmul(den, den))


def requal(r1, r2):
    return ptrim(pmul(r1[0], r2[1])) == ptrim(pmul(r2[0], r1[1]))


# ---------------------------------------------------------------------------
# Window algebra (audit of the admitted AV2 lemma constants, same conventions).
# ---------------------------------------------------------------------------
def family_numerator(s, c1, c2):
    """2 pi ghat * a^3 b for the left polynomial 1+c1 y+c2 y^2 (y=-x>0), a=s-i theta, b=s+i theta.

    Half-line transforms int_0^inf e^{-b x}dx=1/b and int_0^inf y^n e^{-a y}dy=n!/a^{n+1}
    with b=2s-a give (2s-c1)a^2+(2s c1-2c2)a+4s c2 (coefficients in a, ascending).
    """
    return [4 * s * c2, 2 * s * c1 - 2 * c2, 2 * s - c1]


def family_identity_gaussian(s, c1, c2, theta):
    a, b = cx(s, -theta), cx(s, theta)
    lhs = cadd(cadd(cinv(b), cinv(a)), cadd(cscale(cinv(cpow(a, 2)), c1), cscale(cinv(cpow(a, 3)), 2 * c2)))
    n = family_numerator(s, c1, c2)
    num = cadd(cadd(cx(n[0]), cscale(a, n[1])), cscale(cpow(a, 2), n[2]))
    return lhs == cmul(num, cinv(cmul(cpow(a, 3), b)))


def family_identity_in_a(s, c1, c2):
    lhs = padd(pmul([2 * s, -1], [2 * c2, c1, 1]), [0, 0, 0, 1])
    return ptrim(lhs) == ptrim(family_numerator(s, c1, c2))


def one_sided_derivatives(s, c1, c2, order=3):
    """g^{(n)}(0+) for e^{-sx} and g^{(n)}(0-) for e^{sx}(1-c1 x+c2 x^2), n=0..order."""
    p_derivs = [Q(1), Q(-c1), Q(2 * c2), Q(0)]
    right = [(-s) ** n for n in range(order + 1)]
    left = [sum((comb(n, j) * s ** (n - j) * p_derivs[j] for j in range(n + 1)), Q(0)) for n in range(order + 1)]
    return right, left


def window_moments_exact(s):
    """M_j=(4s^3/pi) int |t|^j (s^2+t^2)^-2 dt and int ghat, via exact antiderivatives F=R+B arctan(t/s).

    Returns (all identities hold, {name: coefficient}) where M0 and M2 and int ghat are
    coefficient*pi^0 and M1 is coefficient/pi.
    """
    S2 = [s * s, 0, 1]
    S4 = pmul(S2, S2)
    S6 = pmul(S4, S2)
    table = {
        'M0': (([1], S4), ([0, 1], pscale(S2, 2 * s * s)), 1 / (2 * s ** 3)),
        'M1_half': (([0, 1], S4), ([Q(-1, 2)], S2), Q(0)),
        'M2': (([0, 0, 1], S4), ([0, Q(-1, 2)], S2), 1 / (2 * s)),
        'int_ghat': (([s * s, 0, -1], S6), ([0, 3 * s * s, 0, 1], pscale(S4, 4 * s * s)), 1 / (4 * s ** 3)),
    }
    ok = True
    out = {}
    for name, (f, R, B) in table.items():
        deriv = rderiv(R)
        total = (padd(pmul(deriv[0], S2), pmul([s * B], deriv[1])), pmul(deriv[1], S2)) if B else deriv
        ok = ok and requal(total, f) and len(ptrim(R[0])) < len(ptrim(R[1]))
        if name == 'M1_half':
            out[name] = -peval(R[0], 0) / peval(R[1], 0)     # int_0^inf = R(inf)-R(0) = -R(0)
        else:
            out[name] = B                                     # full line: B*pi
    pref = 4 * s ** 3
    return ok, {'M0': pref * out['M0'], 'M1': pref * 2 * out['M1_half'], 'M2': pref * out['M2'], 'int_ghat': pref * out['int_ghat']}


# ---------------------------------------------------------------------------
# Fine-lattice geometry: Wilson cover, route-B groups, incidence.
# ---------------------------------------------------------------------------
DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENTATIONS = [('x', 'y'), ('x', 'z'), ('y', 'z')]
S_STAR = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def vadd(p, q):
    return tuple(a + b for a, b in zip(p, q))


def vsub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def face_links(p, a, c):
    return [(p, a), (vadd(p, DIRS[a]), c), (vadd(p, DIRS[c]), a), (p, c)]


def face_support(p, a, c):
    return frozenset(owner(t) for t, _ in face_links(p, a, c))


def is_selected(p, a, c):
    """Selected xy faces (I1 table): xy orientation, p_y even, p_x mod 4 in {0,1,2}."""
    return (a, c) == ('x', 'y') and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


def anchored_faces(b):
    return [((4 * b[0] + r, 2 * b[1] + q, b[2]), a, c) for r in range(4) for q in range(2) for a, c in ORIENTATIONS]


def factor_links(b):
    return [((4 * b[0] + r, 2 * b[1] + q, b[2]), d) for r in range(4) for q in range(2) for d in 'xyz']


WILSON = ((0, 0, 0), 'x', 'z')


def wilson_geometry():
    links = face_links(*WILSON)
    owners = [owner(t) for t, _ in links]
    R = sorted(set(owners))
    cover = {lk for b in R for lk in factor_links(b)}
    endpoints, per_factor = set(), {}
    for b in R:
        e = set()
        for t, d in factor_links(b):
            e.add(t)
            e.add(vadd(t, DIRS[d]))
        per_factor[b] = e
        endpoints |= e
    anchors = sorted({vsub(r, d) for r in R for d in S_STAR})
    return {'links': links, 'owners': owners, 'R': R, 'cover': cover, 'cover_links': len(cover), 'endpoints': len(endpoints),
            'per_factor': [len(per_factor[b]) for b in R], 'shared': len(per_factor[R[0]] & per_factor[R[1]]),
            'anchors': anchors, 'drawn_links': len(set(links))}


def route_b_incidence(R):
    """Brute-force route-B grouping over every anchor near R, from the fine geometry only."""
    Rset = set(R)
    anchors = [(x, y, z) for x in range(-2, 2) for y in range(-2, 2) for z in range(-2, 3)]
    stars, singles, faces = [], [], []
    partition_ok = True
    for b in anchors:
        star_faces, single_faces = [], []
        for p, a, c in anchored_faces(b):
            sup = face_support(p, a, c)
            if is_selected(p, a, c):
                partition_ok = partition_ok and sup == frozenset([b])
                single_faces.append((p, a, c))
            else:
                partition_ok = partition_ok and sup <= frozenset(vadd(b, d) for d in S_STAR)
                star_faces.append((p, a, c))
        partition_ok = partition_ok and len(star_faces) == 21 and len(single_faces) == 3
        if any(vadd(b, d) in Rset for d in S_STAR):
            stars.append(b)
            faces += [('star', b, f) for f in star_faces]
        if b in Rset:
            singles.append(b)
            faces += [('single', b, f) for f in single_faces]
    meeting = [f for f in faces if face_support(*f[2]) & Rset]
    inside = [f for f in faces if face_support(*f[2]) <= Rset]
    sel_meeting = [f for f in meeting if f[0] == 'single']
    return {'stars': sorted(stars), 'singles': sorted(singles), 'faces': len(faces), 'meeting': len(meeting),
            'inside': len(inside), 'selected_meeting': len(sel_meeting), 'omitted_meeting': len(meeting) - len(sel_meeting),
            'selected_faces': [f[2] for f in sel_meeting], 'partition_ok': partition_ok,
            'per_star_meeting': {s_star_key(b): str(sum(1 for f in meeting if f[0] == 'star' and f[1] == b)) for b in sorted(stars)}}


def s_star_key(b):
    return '(' + ','.join(str(x) for x in b) + ')'


def box_incidence(N, R):
    """Centered whole-star box Lambda_N=[-N,N]^3: stars b with b+S inside, all single groups."""
    Rset = set(R)
    star_anchors = [(x, y, z) for x in range(-N, N) for y in range(-N, N) for z in range(-N, N)]
    single_anchors = [(x, y, z) for x in range(-N, N + 1) for y in range(-N, N + 1) for z in range(-N, N + 1)]
    stars = [b for b in star_anchors if any(vadd(b, d) in Rset for d in S_STAR)]
    singles = [b for b in single_anchors if b in Rset]
    return len(stars), len(singles), len(star_anchors), len(single_anchors)


# ---------------------------------------------------------------------------
# Main computation.
# ---------------------------------------------------------------------------
def compute(check_sha, calc_sha):
    raw, c = load_contract()
    check('contract_snapshot_sha256', sha_bytes(raw) == CONTRACT_SHA256, contract=CONTRACT_REL, sha256=CONTRACT_SHA256,
          note='target, reference, tau, s, k\', D\' and the control list are read from this hash-checked snapshot')
    V = contract_values(c)
    G1 = load_ax1_gate()
    G2 = load_av2_gate(G1)
    WC = load_av2_contract(G1)
    X1 = load_ax1_contract(G1)
    D_i_exact = load_ax1_forward_tier_i(G1)
    at4_report = load_at4_decimal(G1)
    tau, s1, target = V['tau'], V['s'], V['target']
    pi_lo, pi_hi = calc.pi_interval()

    # -------------------- premise bindings --------------------
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    declared = ['AGENTS.md', CONTRACT_REL] + V['shared_premises'] + V['forward_additional']
    pinned = {CONTRACT_REL: CONTRACT_SHA256, AX1_GATE_REL: AX1_GATE_SHA256, SELECTION_REL: SELECTION_SHA256}
    binding_source = {}
    for rel in sorted(inventory):
        if rel in pinned:
            require(inventory[rel] == pinned[rel], 'pinned snapshot differs: ' + rel)
            binding_source[rel] = 'pinned_in_check_py'
        elif G1['bindings'].get(rel) == inventory[rel]:
            binding_source[rel] = 'ax1_gate_bindings'
        elif G2['bindings'].get(rel) == inventory[rel]:
            binding_source[rel] = 'av2_gate_bindings'
        else:
            raise AdmissionError('premise snapshot not bound by a pinned hash or an admitted gate: ' + rel)
    check('premise_snapshots_bound',
          sorted(inventory) == sorted(set(declared)) and V['forward_additional'] == [] and len(inventory) == 30
          and G1['raw_sha256'] == AX1_GATE_SHA256,
          inventory_files=str(len(inventory)), ax1_gate_sha256=AX1_GATE_SHA256, av2_gate_sha256=G2['sha256'],
          binding_source=binding_source,
          note='inputs are exactly AGENTS.md, the AX2 contract and its 28 shared premises; every snapshot hash is pinned here or bound by the hash-pinned AX1 gate (or the AX1-bound AV2 gate)')
    check('preregistration_mirror_equal', V['controls'] == V['controls_mirror'] and len(V['controls']) == 25,
          controls=str(len(V['controls'])), note='contract controls equal preregistration.controls_required.ids (AV2 N1 lesson)')

    # -------------------- window lemma transfer: same window, same conventions --------------------
    require((WC['c1_over_s'], WC['c2_over_s2']) == (G2['c1_over_s'], G2['c2_over_s2']) == (2, 2), 'AV2 window coefficients')
    require((WC['M0'], WC['M1_coeff'], WC['M2_coeff']) == (G2['M0'], G2['M1_coeff'], G2['M2_coeff']) == (2, 4, 2), 'AV2 constants')
    svals = [Q(1, 2), Q(1), Q(2), Q(7, 3)]
    thetas = [Q(0), Q(1, 3), Q(1), Q(2), Q(-5, 7), Q(10), Q(-31, 4)]
    match_ok, jumps = True, []
    for sv in svals:
        right, left = one_sided_derivatives(sv, WC['c1_over_s'] * sv, WC['c2_over_s2'] * sv * sv)
        match_ok = match_ok and right[:3] == left[:3] and right[3] != left[3]
        jumps.append(right[3] - left[3])
    check('window_c2_matching_verbatim', match_ok and all(j == -8 * sv ** 3 for j, sv in zip(jumps, svals)),
          window='g(x)=e^{-sx} (x>=0); g(x)=e^{sx}(1-2sx+2s^2x^2) (x<0), parsed from the AV2 contract and the AV2 gate',
          third_derivative_jump='-8s^3', l1_norm_of_g='8/s')
    fam_ok = True
    for sv in svals:
        for c1v, c2v in ((Q(0), Q(0)), (2 * sv, Q(0)), (2 * sv, 2 * sv * sv), (Q(1), Q(3))):
            fam_ok = fam_ok and family_identity_in_a(sv, c1v, c2v)
            for th in thetas:
                fam_ok = fam_ok and family_identity_gaussian(sv, c1v, c2v, th)
    mod_ok = True
    for sv in svals:
        for th in thetas:
            a_, b_ = cx(sv, -th), cx(sv, th)
            den = cmul(cpow(a_, 3), b_)
            mod_ok = mod_ok and cabs2(den) == (sv * sv + th * th) ** 4
    check('half_line_transform_and_modulus',
          fam_ok and mod_ok and all(ptrim(family_numerator(sv, 2 * sv, 2 * sv * sv)) == [8 * sv ** 3] for sv in svals)
          and WC['ghat_coeff'] == G2['ghat_coeff'] == 4 and WC['abs_coeff'] == 4,
          ghat='4s^3/(pi(s-i theta)^3(s+i theta))', modulus='(4s^3/pi)(s^2+theta^2)^-2',
          verified='polynomial identity in a (b=2s-a) and Gaussian-rational evaluation at 7 theta, 4 s, 4 left polynomials')
    anti_ok, moments = True, {}
    for sv in svals:
        ok, mm = window_moments_exact(sv)
        anti_ok = anti_ok and ok
        moments[sv] = mm
    check('window_constants_exact',
          anti_ok and all(moments[sv]['M0'] == 2 and moments[sv]['M1'] == 4 * sv and moments[sv]['M2'] == 2 * sv * sv
                          and moments[sv]['int_ghat'] == 1 for sv in svals),
          M0='2', M1='4s/pi', M2='2s^2', int_ghat='1 = g(0) (ghat is complex; ||ghat||_1=2)',
          method='exact antiderivatives F=R+B arctan(theta/s), F\'=f verified as rational-function identities at s in {1/2,1,2,7/3}')
    check('pi_machin_directed', Q(333, 106) < pi_lo < pi_hi < Q(355, 113) and pi_hi - pi_lo <= Q(3, 10 ** 39),
          pi_interval=[s_(pi_lo), s_(pi_hi)], method='Machin, 80-term alternating arctan brackets, outward to 10^-40')

    # -------------------- reference unchanged in route B --------------------
    geo = wilson_geometry()
    inc = route_b_incidence(geo['R'])
    w_links = geo['links']
    w_z_links = [lk for lk in w_links if lk[1] == 'z']
    sel_links = [set(face_links(*f)) for f in inc['selected_faces']]
    no_z_in_selected = all(lk[1] != 'z' for L in sel_links for lk in L)
    parity_ok = True
    for mask in range(1 << len(sel_links)):
        mult = {}
        for lk in w_links:
            mult[lk] = mult.get(lk, 0) + 1
        for i, L in enumerate(sel_links):
            if mask >> i & 1:
                for lk in L:
                    mult[lk] = mult.get(lk, 0) + 1
        parity_ok = parity_ok and all(mult[lk] % 2 == 1 for lk in w_z_links)
    sharing = sum(1 for L in sel_links if L & set(w_links))
    free_lo, free_hi = calc.exp_negative(V['free_energy'] * s1)
    free_lo, free_hi = free_lo / V['free_den'], free_hi / V['free_den']
    datum = (free_lo + free_hi) / 2
    casimir_energy = 4 * Q(3, 4)
    check('reference_unchanged_route_b',
          no_z_in_selected and parity_ok and len(w_z_links) == 2 and sharing == 2 and casimir_energy == V['free_energy'] == 3
          and V['free_den'] == 4 and datum == G2['datum'] and not is_selected(*WILSON),
          statement=('route B keeps the Haar P_R and the tau-independent on-site h_b=8 sum C_e; both single-factor groups and all seven stars '
                     'meeting R sit in B_N, so A_N acts on R by the free Casimir generator and c_0(theta)=e^{3i theta}/4, C_0(s)=e^{-3s}/4 exactly as in AV2'),
          free_z_link=('W has two z links ((0,0,0),z) and ((1,0,0),z); selected faces are xy faces with no z link, so in W times any product of the '
                       'six selected faces of R each z link of W occurs once and the Haar mean vanishes (AW1 grading): the Haar reference sees no selected-face correlation with W'),
          subsets_checked=str(1 << len(sel_links)), selected_faces_sharing_a_link_with_W='2 (links (0,x) and (e_z,x))',
          reference_moments='E_0[W]=0, E_0[W^2]=1/4, G_{0,R}W=3W (four links, Casimir 3/4 each)',
          datum_equals_av2_gate_datum=True, datum=s_(datum))

    # -------------------- incidence, slope, state bound --------------------
    stars_n, singles_n = len(inc['stars']), len(inc['singles'])
    B_norm_over_tau = Q(stars_n * 7 + singles_n * 1, 8)
    k_prime = V['k_over_tau'] * tau
    check('incidence_enumerated_route_b',
          inc['partition_ok'] and inc['stars'] == geo['anchors'] and stars_n == G1['inc']['stars'] == 7
          and singles_n == G1['inc']['groups'] == 2 and inc['singles'] == geo['R'] and inc['faces'] == G1['inc']['faces'] == 153
          and inc['meeting'] == G1['inc']['meeting'] == 88 and inc['omitted_meeting'] == G1['inc']['omitted_meeting'] == 82
          and inc['selected_meeting'] == G1['inc']['selected_meeting'] == 6 and inc['inside'] == G1['inc']['inside'] == 16,
          stars=[s_star_key(b) for b in inc['stars']], single_groups=[s_star_key(b) for b in inc['singles']],
          faces_charged=str(inc['faces']), faces_meeting_R=str(inc['meeting']), faces_inside_R=str(inc['inside']),
          selected_faces_meeting_R=str(inc['selected_meeting']), star_faces_meeting_R=inc['per_star_meeting'],
          method='fine-lattice brute force over 80 anchors: every anchored face is in exactly one group (21-face star or 3-face single group) with support inside the group support')
    check('duhamel_slope_uniform',
          B_norm_over_tau == G1['B_over_tau'] == calc.B_N_OVER_TAU_G_UNITS == Q(51, 8) and 2 * B_norm_over_tau == V['k_over_tau']
          == G1['k_over_tau'] == calc.K_PRIME_OVER_TAU == Q(51, 4),
          B_N='||B_N||<=7*(7|tau|/8)+2*(|tau|/8)=51|tau|/8 in G=H/alpha units', k_prime=s_(k_prime),
          conjugation='||alpha^N_theta(W)-alpha^0_theta(W)||<=2|theta| ||B_N|| for every real theta, uniformly in N>=2 (AT4 F10-F12 with the route-B groups; AX1 gate item 4)')
    D_formula_cap = calc.ax1_tier_ii_D_prime(tau)
    t1 = G1['t1_over_tau'] * tau
    T = t1 / (1 - G1['remainder_factor'] * G1['J_over_tau'] * tau)
    eps = 2 * T + T * T
    D_gate_formula = 2 * eps * (1 + eps) / (1 + eps * eps)
    D_prime = V['D_prime']
    check('ax1_gate_state_bound_bound',
          D_prime == G1['D_prime'] == G1['D_prime_accepted'] == calc.AX1_GATE_D_PRIME == D_formula_cap == D_gate_formula
          and D_prime <= X1['target'] and T == G1['T_prime_cap'] == Q(13, 3599632512) and G1['J_over_tau'] == 29 and G1['remainder_factor'] == 352,
          D_prime=s_(D_prime), D_prime_preview=dec(D_prime), gate_sha256=AX1_GATE_SHA256,
          binding='read from the AX1 gate decision (hash-pinned), equal to the contract parameter, the gate accepted text and the pinned calculator constant; '
                  'the gate formula t_1\'=52|tau|/144, T\'=t_1\'/(1-352J\'), eps=2T\'+T\'^2, 2eps(1+eps)/(1+eps^2) reproduces it (pair term and density form pinned)',
          consequences='|m|=|omega(W)|<=D\', m^2<=D\'^2, passing to every AQ1 subsequential limit (AX1 gate item 6)')

    # -------------------- the certificate --------------------
    cert_p = calc.certify(fixed_design=True)
    cert_m = calc.certify(tau=s_(-tau), fixed_design=True)
    M0 = Q(2)
    M1_up = 4 * s1 / pi_lo
    terms = {'state': M0 * D_prime, 'mean_square': M0 * D_prime ** 2, 'kernel_dynamics': k_prime * M1_up,
             'arithmetic': (free_hi - free_lo) / 2}
    radius = sum(terms.values(), Q(0))
    radius_out = calc.up(radius)
    lo_C, hi_C = datum - radius, datum + radius
    cert_terms = {kk: rat(v) for kk, v in cert_p['costs'].items()}
    check('radius_itemized_tau_plus',
          cert_terms == terms and rat(cert_p['certified_absolute_error']) == radius and rat(cert_p['certified_datum']) == datum
          and rat(cert_p['state_bound_D_prime']) == D_prime and rat(cert_p['duhamel_slope_k_prime']) == k_prime
          and rat(cert_p['certified_absolute_error_outward_1e-40']) == radius_out,
          formula="E'=M_0(D'+D'^2)+k' M_1, M_0=2, M_1=4s/pi (pi lower bound), k'=51|tau|/4; plus the midpoint arithmetic radius",
          terms={kk: s_(v) for kk, v in terms.items()}, radius=s_(radius), radius_outward_1e_minus_40=s_(radius_out),
          radius_preview=dec(radius, 12, 'up'))
    check('mirrored_coupling_replay_U_E',
          cert_m['certified_absolute_error'] == cert_p['certified_absolute_error'] and cert_m['certified_datum'] == cert_p['certified_datum']
          and cert_m['mirrored_coupling_replay'] is True and cert_p['mirrored_coupling_replay'] is False and G1['flip'],
          tau=s_(-tau), note=('tau=-10^-8 has no real g; it is the U_E image of +10^-8 (U_E H_N(tau)U_E^*=H_N(-tau), C_N even, S(-tau)=S(tau) o alpha_E '
                              'as whole sets); the value is a replay of the same |tau| formula, not a second confirmation'))
    target_met = radius <= target
    check('target_boolean_1e-6', target_met is True and cert_p['target_met'] is True and cert_m['target_met'] is True,
          target=s_(target), radius=s_(radius), margin_target_over_radius_lower=dec(target / radius, 6, 'down'))
    check('free_reference_inside_reference_unresolved',
          lo_C <= free_lo and free_hi <= hi_C and cert_p['free_reference_included'] is True and cert_p['sub_label'] == 'reference_unresolved'
          and 'reference_unresolved' in V['sub_labels_allowed'] and cert_p['resolved_interaction_shift'] is False,
          free_interval=[s_(free_lo), s_(free_hi)], sub_label='reference_unresolved')
    check('rational_datum_and_arithmetic',
          datum == (free_lo + free_hi) / 2 and 0 < terms['arithmetic'] <= Q(1, 10 ** 40) and hi_C - lo_C == 2 * radius,
          datum=s_(datum), arithmetic=s_(terms['arithmetic']),
          exp_method='alternating Taylor P_41<=e^-z<=P_40 on [0,1/2], halving 3->3/8 three times, outward squaring to 10^-40 (AV2 routine)')
    check('preview_radius_consistency',
          abs(radius - V['preview_radius']) <= Q(1, 10 ** 9) and abs(D_prime - V['preview_D']) <= Q(1, 10 ** 12)
          and V['preview_slope_numerator'] == 4 * k_prime,
          contract_preview=s_(V['preview_radius']), computed_preview=dec(radius, 6, 'up'), note='the contract preview is not a result')
    E_av2 = G2['R']
    check('comparison_with_av2_zero_selected',
          radius > E_av2 and D_prime > G2['D_av1_zero_selected'] and V['k_over_tau'] - G2['k_over_tau'] == Q(1, 2),
          av2_common_radius=s_(E_av2), ax2_radius=s_(radius), difference_lower=dec(radius - E_av2, 8, 'down'),
          reason='the uniform model adds the two single-factor groups to B_N (k: 49|tau|/4 -> 51|tau|/4) and uses the larger uniform D\'; a different model, not a refinement of AV2')

    # -------------------- lemma transfer checklist --------------------
    transfer = {
        'window_g_and_conventions': 'verbatim (AV2 contract/gate strings parsed and compared)',
        'constants_M0_M1_M2': 'verbatim (re-verified: 2, 4s/pi, 2s^2)',
        'spectral_support_G>=0': 'verbatim: AQ1 nonnegativity re-applies to the uniform route-B state (AX1 gate item 3)',
        'finite_centered_measure': 'verbatim: eta([0,inf))=||chi||^2=omega(W^2)-m^2<=1',
        'inversion_and_fubini': 'verbatim: depends on g only',
        'reference_c0': 'verbatim value e^{3i theta}/4: Haar P_R, free Casimir on R, W has free z links',
        'real_time_slope': 'new constant k\'=51|tau|/4 (7 stars + 2 single-factor groups; AX1 gate item 4)',
        'state_term': 'new constant D\' (AX1 gate decision), trace duality, no D/2',
        'mean_square': 'new constant m^2<=D\'^2 (AX1 gate item 6)',
        'AQ_limit_passage': 'verbatim with the route-B constants (AX1 gate items 3 and 6)',
        'AQ2_gap': 'not used',
    }
    check('lemma_transfer_checklist',
          G2['lemma'] and G1['verbatim_steps'] and G1['state_consequences'] and G1['gap_statement'] and G1['no_node_no_K2']
          and G1['first_order_den'] == 144,
          checklist=transfer, outcome='the transfer holds; acceptance clause "insufficient: the transfer of the window lemma fails" is not triggered')

    # -------------------- retained failures at the uniform slope --------------------
    L4 = Q(10) ** 4

    def poisson_radius(Dv, kv, sv, Lv, lg, pi_div, pi_tail):
        return Dv + Dv * Dv + kv * sv * lg / pi_div + (Q(1, 2) + Dv / 2) * 2 * sv / (pi_tail * Lv)
    lg_lo, lg_hi = calc.log_positive(1 + (L4 / s1) ** 2)
    D4_lo, D4_hi = calc.sqrt_interval(Q(49, 3) * tau)
    k_av2 = G2['k_over_tau'] * tau
    at4_hi = poisson_radius(2 * D4_hi, k_av2, s1, L4, lg_hi, pi_lo, pi_lo)
    Dsq_lo, Dsq_hi = calc.sqrt_interval(G1['sqrt_arg'] * tau)
    Dsq_lo, Dsq_hi = 2 * Dsq_lo, 2 * Dsq_hi
    at4u_hi = poisson_radius(Dsq_hi, k_prime, s1, L4, lg_hi, pi_lo, pi_lo)
    at4u_lo = poisson_radius(Dsq_lo, k_prime, s1, L4, lg_lo, pi_hi, pi_hi)
    check('retained_at4_poisson_uniform_slope',
          abs(at4_hi - at4_report) <= Q(1, 10 ** 15) and at4u_lo > target and at4u_lo > at4_hi,
          formula='AT4 F16: D+D^2+(ks/pi)log(1+L^2/s^2)+(1/2+D/2)(2s/(pi L)), reproducing the frozen AT4 decimal with D=2sqrt(49|tau|/3), k=49|tau|/4',
          uniform_inputs="D=2sqrt(17|tau|) (AX1 square-root control), k'=51|tau|/4, L=10^4, s=1",
          radius_interval=[s_(at4u_lo), s_(at4u_hi)], radius_preview=[dec(at4u_lo, 8, 'down'), dec(at4u_hi, 8, 'up')],
          at4_frozen_decimal=s_(at4_report), target_met=False, verdict='insufficient, retained')
    kk2 = 2 * k_prime
    inv2k = 1 / kk2
    lgk_lo, _ = calc.log_positive(inv2k / s1)
    floor_lo = kk2 * s1 * (1 + lgk_lo) / pi_hi
    L_star = Q(inv2k.numerator // inv2k.denominator + 1)
    lgs_lo, lgs_hi = calc.log_positive(1 + (L_star / s1) ** 2)
    floor_hi = k_prime * s1 * lgs_hi / pi_lo + s1 / (pi_lo * L_star)
    floor_with_D_lo = floor_lo + D_prime + D_prime ** 2
    L32 = Q(10) ** 32
    l32_lo, _ = calc.log_positive(1 + L32 ** 2)
    moment_32_lo = s1 * l32_lo / pi_hi
    check('retained_poisson_floor_uniform_slope',
          target < floor_lo <= floor_hi and floor_with_D_lo > target and floor_lo > G2['floor_decimal'] and k_prime * moment_32_lo > target
          and 4 * s1 / pi_lo < moment_32_lo,
          lower_bound="for every L>0: (k's/pi)log(1+L^2/s^2)+s/(pi L) >= (2k's/pi)(1+log(1/(2k's))), minimized at L=1/(2k')",
          floor_interval=[s_(floor_lo), s_(floor_hi)], floor_preview=[dec(floor_lo, 10, 'down'), dec(floor_hi, 10, 'up')],
          L_evaluated=s_(L_star), with_admitted_D_prime_lower=dec(floor_with_D_lo, 8, 'down'),
          poisson_partial_first_moment_L_1e32_lower=dec(moment_32_lo, 8, 'down'), window_first_moment='4s/pi (finite)',
          av2_floor_decimal=s_(G2['floor_decimal']), target_met=False, verdict='insufficient for every L, retained')
    t_i = G1['J_over_tau'] * tau * Q(148, 7)
    eps_i = 2 * t_i + t_i ** 2
    D_i = 2 * eps_i * (1 + eps_i) / (1 + eps_i ** 2)
    E_tier_i_lo = 2 * (D_i + D_i ** 2) + k_prime * 4 * s1 / pi_hi
    check('retained_tier_i_window',
          D_i == D_i_exact and abs(D_i - G1['D_tier_i_decimal']) <= Q(1, 10 ** 9) and E_tier_i_lo > target,
          D_prime_i=s_(D_i), D_prime_i_preview=dec(D_i), window_radius_lower=dec(E_tier_i_lo, 10, 'down'),
          label='limited-tier value (AX1 tier i, t<=J\'G(R)=1073/175000000); fails 10^-6; retained, never the bound premise')

    # -------------------- crossover --------------------
    A = 2 * (D_prime + D_prime ** 2)
    slope_const = V['k_over_tau'] * 4 * tau          # k'*M_1/s times pi = 51|tau|
    s_star_lo = pi_lo * (target - A) / slope_const
    s_star_hi = pi_hi * (target - A) / slope_const

    def E_up(sv):
        return A + slope_const * sv / pi_lo

    def E_low(sv):
        return A + slope_const * sv / pi_hi
    check('crossover_s_star_uniform',
          E_up(s_star_lo) == target and E_low(s_star_hi) == target and s_star_lo <= s_star_hi and E_up(Q(5)) <= target
          and E_low(Q(6)) > target and s_star_hi < G2['s_star'][0] and E_low(Q(128)) > target,
          s_star_interval=[s_(s_star_lo), s_(s_star_hi)], s_star_preview=[dec(s_star_lo, 11, 'down'), dec(s_star_hi, 11, 'up')],
          E_of_s="2(D'+D'^2)+51|tau|s/pi (analytic radius, linear in s)", av2_s_star=[s_(G2['s_star'][0]), s_(G2['s_star'][1])],
          E_at_128_lower=dec(E_low(Q(128)), 6, 'down'), grid_claim=False,
          note='no node other than s=1 is evaluated or certified; no grid and no [0,128] claim')

    # ======================= contract controls =======================
    # kernel_identity_on_support
    xs = [Q(0), Q(1, 32), Q(1, 3), Q(1), Q(3), Q(17, 2)]

    def window_on_support(mult, sv):
        for x in xs:
            require(mult(x, sv) == 1, 'window differs from e^{-sx} on the AQ1 support [0,inf) at x=' + s_(x))
        return True

    def symmetric_window(x, sv):
        y = abs(Q(x))
        return 1 + 2 * sv * y + 2 * sv * sv * y * y

    def gap_window(x, sv):
        return Q(1) if Q(x) >= Q(1, 16) else Q(2)
    check('kernel_identity_on_support',
          all(window_on_support(calc.window_multiplier, sv) for sv in svals) and calc.window_multiplier(V['free_energy'], s1) == 1
          and G1['verbatim_steps']
          and rejected(lambda: window_on_support(symmetric_window, s1), 'symmetric_window_misreads_support')
          and rejected(lambda: window_on_support(gap_window, s1), 'window_matched_only_above_AQ2_gap'),
          sampled_x=[s_(x) for x in xs], premise='uniform-model AQ1 nonnegativity (verbatim, AX1 gate item 3); AQ2 gap not used')

    # kernel_negative_atom_misread
    em_lo, em_hi = calc.exp_negative(Q(1))
    e_lo, _ = calc.exp_positive(Q(1))
    mult_m1 = calc.window_multiplier(Q(-1), s1)

    def lemma_measure(atoms):
        for x, w in atoms:
            require(x >= 0 and w >= 0, 'window lemma needs a positive measure on [0,inf): atom at ' + s_(x))
        return True
    eta_uniform = [(Q(3), Q(1, 4))]
    check('kernel_negative_atom_misread',
          mult_m1 == 5 and mult_m1 * em_hi < e_lo and lemma_measure(eta_uniform)
          and rejected(lambda: lemma_measure([(Q(-1), Q(1))]), 'negative_atom_admitted'),
          window_value='g(-1)=5/e at s=1', heat_value='e', window_upper=s_(5 * em_hi), heat_lower=s_(e_lo),
          reason='the window under-reads every negative atom; the uniform route-B generator is nonnegative (AQ1, AX1 gate item 3)')

    # kernel_l1_and_first_moment
    def validate_constants(M0v, M1v, sv):
        require(M0v == moments[sv]['M0'], 'M_0 differs from ||ghat||_1')
        require(M1v == moments[sv]['M1'], 'M_1 differs from int|theta||ghat|')
        return True
    check('kernel_l1_and_first_moment',
          all(validate_constants(Q(2), 4 * sv, sv) for sv in svals)
          and rejected(lambda: validate_constants(Q(1), Q(4), Q(1)), 'positive_kernel_mass_one')
          and rejected(lambda: validate_constants(moments[Q(1)]['int_ghat'], Q(4), Q(1)), 'signed_integral_as_l1_norm')
          and rejected(lambda: validate_constants(Q(2), Q(4), Q(2)), 'first_moment_without_s'),
          M0='2', M1='4s/pi', fubini='int int |ghat e^{i theta x}| dtheta d eta = M_0 eta([0,inf)) < inf')

    # window_linear_in_s
    Es = {sv: calc.certify(s=s_(sv)) for sv in (Q(1, 2), Q(1), Q(2), Q(5))}
    lin_ok = all(rat(Es[sv]['analytic_radius']) == A + slope_const * sv / pi_lo for sv in Es)

    def validate_node_claim(sv, claimed):
        require(sv in V['node_s_values'], 'post-hoc node selection is forbidden')
        require(claimed == rat(calc.certify(s=s_(sv))['analytic_radius']), 'claimed radius differs from E\'(s)')
        return True
    check('window_linear_in_s',
          lin_ok and validate_node_claim(s1, rat(cert_p['analytic_radius']))
          and rejected(lambda: validate_node_claim(Q(5), rat(cert_p['analytic_radius'])), 'node_s5_with_s1_radius')
          and rejected(lambda: validate_node_claim(s1, A), 'dynamics_term_dropped'),
          E_of_s="2(D'+D'^2)+(51|tau|/pi)s", E_preview={s_(sv): dec(rat(Es[sv]['analytic_radius']), 8, 'up') for sv in Es})

    # local_not_extensive_duhamel
    box = {N: box_incidence(N, geo['R']) for N in (1, 2, 3, 4)}
    star_norm = Q(7, 8) * tau
    single_norm = Q(1, 8) * tau

    def validate_slope(k_by_N):
        vals = set(k_by_N.values())
        require(len(vals) == 1, 'Duhamel slope depends on the box: extensive norm used')
        require(vals == {k_prime}, 'slope differs from 2*(7 stars*7|tau|/8 + 2 groups*|tau|/8)=51|tau|/4')
        return True
    local_k = {N: 2 * (box[N][0] * star_norm + box[N][1] * single_norm) for N in (2, 3, 4)}
    ext_k = {N: 2 * (box[N][2] * star_norm + box[N][3] * single_norm) for N in (2, 3, 4)}
    seven_only = {N: 2 * box[N][0] * star_norm for N in (2, 3, 4)}
    u = cx(Q(3, 5), Q(4, 5))
    ratio_fixture = cabs2(cadd(cmul(u, u), cx(-1))) / cabs2(cadd(u, cx(-1)))
    check('local_not_extensive_duhamel',
          all(box[N][:2] == (7, 2) for N in (2, 3, 4)) and box[1][:2] == (4, 2) and validate_slope(local_k) and 1 < ratio_fixture <= 4
          and rejected(lambda: validate_slope(ext_k), 'extensive_total_norm')
          and rejected(lambda: validate_slope(seven_only), 'seven_star_only_slope_changed_model')
          and rejected(lambda: validate_slope({N: v / 2 for N, v in local_k.items()}), 'conjugation_factor_two_dropped'),
          incident_by_N={str(N): {'stars': str(box[N][0]), 'single_groups': str(box[N][1])} for N in (1, 2, 3, 4)},
          retained_by_N={str(N): {'stars': str(box[N][2]), 'single_groups': str(box[N][3])} for N in (2, 3, 4)},
          seven_star_only='49|tau|/4 is the AV2 zero-selected slope: using it for the uniform model drops the two single-factor groups (a changed model)',
          conjugation_fixture='U=diag(u,conj u), u=(3+4i)/5, X=sigma_x: ratio 16/5 in (1,4]')

    # uniform_label_strong_coupling
    label = cert_p['label']
    g4_cap = 96 / tau

    def validate_label(fields, g4):
        require(calc.LABEL_STEM in fields['label'] and '(g^4=9.6x10^9)' in fields['label'], 'label must name uniform KS SU(2), fixed spacing, strong bare coupling, g^4=9.6x10^9')
        for key, text in fields.items():
            low = text.lower()
            require('weak' not in low and 'continuum' not in low, 'weak-coupling or continuum wording in ' + key)
        require(g4 == V['g4'] == Q(9600000000) and g4 > 0, 'g^4 differs from 96/tau at the cap')
        return True
    base_fields = {'label': label, 'contract_model': V['model_text'], 'scope': cert_p['scope'],
                   'verdict': 'accepted_within_scope proposed (forward single producer; admission requires the skeptic replay)'}

    def with_field(key, value):
        f = dict(base_fields)
        f[key] = value
        return f
    check('uniform_label_strong_coupling',
          validate_label(base_fields, g4_cap) and 'tau=96/g^4' in G1['model']
          and rejected(lambda: validate_label(with_field('label', label.replace('strong bare coupling', 'weak coupling')), g4_cap), 'weak_coupling_label')
          and rejected(lambda: validate_label(with_field('verdict', 'certificate toward the continuum'), g4_cap), 'continuum_in_verdict')
          and rejected(lambda: validate_label(with_field('label', label.replace(' at fixed spacing', '')), g4_cap), 'fixed_spacing_missing')
          and rejected(lambda: validate_label(with_field('label', label.replace('strong bare coupling', 'coupling')), g4_cap), 'strong_bare_coupling_missing')
          and rejected(lambda: validate_label(base_fields, 96 / (-tau)), 'negative_tau_as_real_g')
          and rejected(lambda: validate_label(base_fields, 96 / (8 * tau)), 'tau_read_in_delta_units'),
          label=label, g4=s_(g4_cap), dictionary='tau=96/g^4 (AL1/AX1); g^4=9.6x10^9 at the cap; tau<0 has no real g (U_E mirror)')

    # selected_incidence_count
    def validate_groups(n_stars, n_groups, n_selected, B_over_tau):
        require(n_stars == 7 and n_groups == 2 and n_selected == 6, 'route-B incidence must be 7 stars, 2 single-factor groups, 6 selected faces')
        require(B_over_tau == Q(7 * n_stars + n_groups, 8) == Q(51, 8), '||B_N|| differs from 51|tau|/8')
        return True
    check('selected_incidence_count',
          validate_groups(stars_n, singles_n, inc['selected_meeting'], B_norm_over_tau)
          and rejected(lambda: validate_groups(7, 0, 0, Q(49, 8)), 'selected_groups_forgotten')
          and rejected(lambda: validate_groups(7, 6, 6, Q(55, 8)), 'faces_counted_as_groups')
          and rejected(lambda: validate_groups(7, 7, 21, Q(56, 8)), 'single_groups_at_the_seven_star_anchors')
          and rejected(lambda: validate_groups(7, 2, 6, Q(49, 8) + 2 * Q(3, 24) / 8), 'selected_norm_tau_over_24_delta_units'),
          single_groups=[s_star_key(b) for b in inc['singles']], selected_faces=[s_star_key(f[0]) + f[1] + f[2] for f in inc['selected_faces']],
          note='both single-factor groups lie inside R ({0} and {e_z}) and enter B_N in full')

    # j0_resolution_declared
    exp8_lo, exp8_hi = calc.exp_positive(Q(1, 8))
    G_R = 16 * exp8_hi * (1 + Q(10, 64))
    Gp_R = 16 * exp8_hi * (18 + Q(80, 64))

    def validate_j0(res):
        require(res.get('id') == 'R1', 'J_0 resolution missing or not R1')
        require(res['tau_cap'] == calc.CAP, 'R2 changes the coupling cap: a changed model under the cap label')
        require(res['J0'] >= G1['J_over_tau'] * res['tau_cap'], 'J_0 below the route-B per-site sum J\'=29|tau| at the cap')
        require(res['J0'] * Q(148, 7) < Q(1, 64) and 2 * res['J0'] * 352 < 1, 'AM2 contraction fails')
        return True
    j0 = {'id': 'R1', 'J0': G1['J0_prime'], 'tau_cap': calc.CAP}
    check('j0_resolution_declared',
          validate_j0(j0) and exp8_hi < Q(8, 7) and G_R < Q(148, 7) and Gp_R < 352
          and G1['J0_prime'] * Q(148, 7) == G1['self_map'] == Q(1073, 175000000) and 2 * G1['J0_prime'] * 352 == G1['contraction'] == Q(319, 1562500)
          and 'R1: re-freeze' in X1['J0_resolution']
          and rejected(lambda: validate_j0({'id': 'R1', 'J0': G1['J0_old'], 'tau_cap': calc.CAP}), 'old_J0_at_the_cap')
          and rejected(lambda: validate_j0({'J0': G1['J0_prime'], 'tau_cap': calc.CAP}), 'resolution_missing')
          and rejected(lambda: validate_j0({'id': 'R2', 'J0': G1['J0_old'], 'tau_cap': Q(7, 725000000)}), 'R2_cap_under_cap_label'),
          J0_prime=s_(G1['J0_prime']), self_map=s_(G1['self_map']), contraction=s_(G1['contraction']), exp_one_eighth_upper=s_(exp8_hi),
          role='the uniform AQ state, its nonnegative generator and D\' rest on the route-B AM2 gap with J_0\'=29/10^8 (AX1 gate item 2)')

    # av1_tier_bound  (semantics: D' equals the AX1 gate's admitted forward tier-(ii) value; any other D is rejected)
    def validate_state_bound(Dv):
        require(Dv == G1['D_prime'] == V['D_prime'] == calc.AX1_GATE_D_PRIME, 'state bound is not the AX1 gate forward tier-(ii) D\'')
        return True
    T_nopair = t1 / (1 - 352 * 29 * tau)
    eps_nopair = 2 * T_nopair
    D_nopair = 2 * eps_nopair * (1 + eps_nopair) / (1 + eps_nopair ** 2)
    D_2eps = 2 * eps
    check('av1_tier_bound',
          validate_state_bound(D_prime) and validate_state_bound(rat(cert_p['state_bound_D_prime'])) and cert_p['state_bound_equals_ax1_gate_value'] is True
          and rejected(lambda: validate_state_bound(G1['D_reverse_refinement']), 'ax1_reverse_R_refinement')
          and rejected(lambda: validate_state_bound(X1['target']), 'ax1_target_4e-7')
          and rejected(lambda: validate_state_bound(G2['D_av1_zero_selected']), 'av1_zero_selected_D')
          and rejected(lambda: validate_state_bound(X1['note_threshold']), 'ax1_d_prime_note_4.19e-7')
          and rejected(lambda: validate_state_bound(D_i), 'ax1_tier_i')
          and rejected(lambda: validate_state_bound(D_nopair), 'pair_term_dropped_recomputation')
          and rejected(lambda: validate_state_bound(D_2eps), 'density_form_replaced_by_2eps')
          and calc_rejects({'D': '1/100000000'}, 'calculator_supplied_D', (ValueError, TypeError))
          and calc_rejects({'state_tier': 'ax1_reverse_R_refinement'}, 'calculator_reverse_refinement_tier')
          and calc_rejects({'state_tier': 'av1_forward_tier_ii'}, 'calculator_av1_zero_selected_tier'),
          D_prime=s_(D_prime), rejected_values={'reverse_refinement': dec(G1['D_reverse_refinement']), 'ax1_target': s_(X1['target']),
                                                'av1_zero_selected': dec(G2['D_av1_zero_selected']), 'd_prime_note': s_(X1['note_threshold']),
                                                'tier_i': dec(D_i), 'pair_term_dropped': dec(D_nopair, 14), 'two_eps': dec(D_2eps, 14)},
          note='AX1 N5 closed here: the gate rational is bound; a recomputation dropping T\'^2 or replacing the density form is rejected')

    # state_term_not_effect
    Delta, X_ne, A_eff = [Q(1, 2), Q(-1, 2)], [Q(1), Q(-1)], [Q(1), Q(0)]
    tr_ne = sum(d_ * x_ for d_, x_ in zip(Delta, X_ne))
    tr_eff = sum(d_ * x_ for d_, x_ in zip(Delta, A_eff))
    norm1 = sum(abs(d_) for d_ in Delta)

    def validate_state_term(state_term):
        require(state_term == M0 * D_prime, 'state term must be M_0*D\' (trace duality for the non-effect W alpha^0_theta(W))')
        return True
    check('state_term_not_effect',
          abs(tr_ne) == norm1 > norm1 / 2 and abs(tr_eff) <= norm1 / 2 and validate_state_term(terms['state'])
          and rejected(lambda: validate_state_term(M0 * D_prime / 2), 'effect_refinement_D_over_2'),
          fixture='Delta=diag(1/2,-1/2): |Tr(Delta diag(1,-1))|=1>1/2', reason='W alpha^0_theta(W) has free expectation e^{3i theta}/4: not an effect (AT4 F12)')

    # window_fourier_sign_convention
    def validate_reference(mult):
        require(mult == 1, 'reference differs from e^{-3s}/4: wrong Fourier sign convention')
        return True
    check('window_fourier_sign_convention',
          validate_reference(calc.window_multiplier(V['free_energy'], s1))
          and calc.window_multiplier(-V['free_energy'], s1) == WC['sign_mutation_multiplier'] == 25
          and rejected(lambda: validate_reference(calc.window_multiplier(-V['free_energy'], s1)), 'theta_to_minus_theta'),
          frozen='c(theta)=<chi,e^{i theta G}chi>, ghat(theta)=(2pi)^-1 int g(x)e^{-i theta x}dx (AV2 item 1, verbatim)',
          mutation_value='g(-3)/4=25e^{-3}/4 at s=1')

    # tier_mixing_rejected
    T_norem = t1
    eps_norem = 2 * T_norem + T_norem ** 2
    D_norem = 2 * eps_norem * (1 + eps_norem) / (1 + eps_norem ** 2)

    def validate_tier_mix(comp):
        for name, (tier, value) in comp.items():
            require(tier == TIER, 'tier mixing: ' + name + ' uses ' + tier)
        require(comp['state'][1] == M0 * D_prime and comp['mean_square'][1] == M0 * D_prime ** 2, 'state and mean-square terms not from one D\'')
        return True
    base_mix = {'state': (TIER, terms['state']), 'mean_square': (TIER, terms['mean_square'])}
    check('tier_mixing_rejected',
          validate_tier_mix(base_mix)
          and rejected(lambda: validate_tier_mix({'state': (TIER, terms['state']), 'mean_square': ('ax1_forward_tier_i', M0 * D_i ** 2)}), 'tier_i_mean_square_with_tier_ii_state')
          and rejected(lambda: validate_tier_mix({'state': ('ax1_reverse_R_refinement', M0 * G1['D_reverse_refinement']), 'mean_square': (TIER, terms['mean_square'])}), 'reverse_state_with_forward_mean_square')
          and rejected(lambda: validate_tier_mix({'state': (TIER, M0 * D_norem), 'mean_square': (TIER, M0 * D_norem ** 2)}), 'exact_first_order_without_am2_remainder')
          and rejected(lambda: validate_tier_mix({'state': ('av1_forward_tier_ii', M0 * G2['D_av1_zero_selected']), 'mean_square': (TIER, terms['mean_square'])}), 'zero_selected_state_with_uniform_slope'),
          tier=TIER, note='one tier (AX1 forward tier ii) supplies both D\' and m^2<=D\'^2; no component is taken from another tier or model')

    # single_producer_declared
    def validate_single(pk):
        require(pk['producers'] == ['forward'] == V['producers'], 'single forward producer required')
        require(V['direction'] == 'single+skeptic' and V['single_replay'] is True, 'contract direction')
        require(pk['single_direction_independent_replay_required'] is True, 'admission requires the skeptic independent replay')
        require(pk['independent_review_claimed'] is False and pk['mirror_is_second_confirmation'] is False, 'self-replay relabelled as independent')
        require('skeptic' in pk['proposed_forward_verdict'] and 'independent replay' in pk['proposed_forward_verdict'], 'verdict must name the pending skeptic replay')
        return True
    single_decl = {'producers': ['forward'], 'single_direction_independent_replay_required': True, 'independent_review_claimed': False,
                   'mirror_is_second_confirmation': False,
                   'proposed_forward_verdict': 'accepted_within_scope proposed; admission requires the skeptic\'s independent replay from the contract alone'}

    def mut_single(key, value):
        d = dict(single_decl)
        d[key] = value
        return d
    check('single_producer_declared',
          validate_single(single_decl) and V['semantics']['single_producer_declared'].startswith('producers=[forward]')
          and rejected(lambda: validate_single(mut_single('producers', ['forward', 'reverse'])), 'reverse_route_claimed')
          and rejected(lambda: validate_single(mut_single('single_direction_independent_replay_required', False)), 'replay_requirement_dropped')
          and rejected(lambda: validate_single(mut_single('independent_review_claimed', True)), 'self_review_called_independent')
          and rejected(lambda: validate_single(mut_single('mirror_is_second_confirmation', True)), 'mirror_as_second_confirmation')
          and rejected(lambda: validate_single(mut_single('proposed_forward_verdict', 'accepted_within_scope')), 'verdict_without_pending_replay'),
          declaration=single_decl)

    # missing_incoming_stars
    orth = [b for b in geo['anchors'] if all(x_ >= 0 for x_ in b)]

    def validate_star_count(n):
        require(n == 7, 'incident star count differs from seven')
        return True
    check('missing_incoming_stars',
          validate_star_count(len(geo['anchors'])) and len(orth) == 2 and box[1][0] == 4
          and rejected(lambda: validate_star_count(len(orth)), 'orthant_two_anchors')
          and rejected(lambda: validate_star_count(box[1][0]), 'box_N1_truncated'),
          anchors=[s_star_key(b) for b in geo['anchors']], orthant_count='2', N1_count='4 (N>=2 required)')

    # full_original_wilson_cover
    def validate_cover(nlinks, nend):
        require(nlinks == 48 and nend == 36, 'cover is not the complete 48-link, 36-endpoint R={0,e_z}')
        return True
    sel_in_cover = all(lk in geo['cover'] for L in sel_links for lk in L)
    check('full_original_wilson_cover',
          geo['owners'] == [(0, 0, 0), (0, 0, 0), (0, 0, 1), (0, 0, 0)] and geo['R'] == [(0, 0, 0), (0, 0, 1)]
          and validate_cover(geo['cover_links'], geo['endpoints']) and geo['per_factor'] == [22, 22] and geo['shared'] == 8 and sel_in_cover
          and rejected(lambda: validate_cover(geo['drawn_links'], 4), 'four_drawn_links'),
          owners='0,0,e_z,0', links='48', endpoints='36 (22 per factor, 8 shared)', selected_faces_inside_cover='6 (all links in the cover)')

    # wrong_delta_alpha_hbar_clock
    alpha_, hbar_, tE = Q(5), Q(7), Q(3, 2)
    s_clock = alpha_ * tE / hbar_
    u_clock = s_clock / 8
    wilson_G = 4 * Q(3, 4)
    wilson_delta = 8 * wilson_G

    def validate_clock(exponent_per_s, k_value):
        require(exponent_per_s == V['free_energy'], 'reference exponent differs from 3 per unit s')
        require(k_value == k_prime, 'Duhamel slope not in G=H/alpha units')
        return True
    scaled = calc.certify(alpha='5', hbar='7', E_star='3', lattice_spacing='2', fixed_design=True)
    check('wrong_delta_alpha_hbar_clock',
          wilson_G == 3 and wilson_delta == 24 and 3 * s_clock == 24 * u_clock and validate_clock(wilson_G, k_prime)
          and scaled['physical_Euclidean_time'] == '7/5' and scaled['certified_datum'] == cert_p['certified_datum']
          and rejected(lambda: validate_clock(wilson_delta, k_prime), 'exponent_24_with_s')
          and rejected(lambda: validate_clock(wilson_G, 2 * (7 * 7 + 2) * tau), 'normalized_group_norms_in_G_clock'),
          nonunit_fixture={'alpha': '5', 'hbar': '7', 't_E': '3/2', 's': s_(s_clock), 'u': s_(u_clock)},
          G_units='group norms /8: stars 7|tau|/8, single groups |tau|/8')

    # vector_versus_scalar_centering
    m_, d_ = Q(1, 4), Q(1, 100)

    def validate_centering(residue):
        require(residue == d_ ** 2, 'scalar subtraction used as vector centering')
        return True
    check('vector_versus_scalar_centering',
          validate_centering(d_ ** 2) and -2 * m_ * d_ - d_ ** 2 == Q(-51, 10000)
          and rejected(lambda: validate_centering(-2 * m_ * d_ - d_ ** 2), 'scalar_as_vector'),
          vector_residue=s_(d_ ** 2), scalar_residue=s_(-2 * m_ * d_ - d_ ** 2), ax2_centering='chi=(W-m)Omega with the true mean; m^2<=D\'^2 charged with M_0')

    # first_order_mean_charged
    def validate_mean_square(ms):
        require(ms == M0 * D_prime ** 2 and ms > 0, 'mean-square centering not charged at M_0*D\'^2')
        return True
    first_order = tau / G1['first_order_den']
    check('first_order_mean_charged',
          validate_mean_square(terms['mean_square']) and first_order <= D_prime and G1['no_node_no_K2']
          and rejected(lambda: validate_mean_square(Q(0)), 'zero_mean_assumed')
          and rejected(lambda: validate_mean_square(M0 * first_order ** 2), 'finite_box_first_order_mean_as_uniform_bound'),
          mean_square_term=s_(terms['mean_square']), finite_box_first_order_mean=s_(first_order),
          reason='the uniform model has omega(W)^(1)=+tau/144 in every finite box, but no uniform K_2 is admitted (loop-2 veto): only |m|<=D\' is uniform')

    # tau_scaling_exponent
    E_cap = rat(calc.certify(tau=s_(tau))['analytic_radius'])
    E_100 = rat(calc.certify(tau=s_(tau / 100))['analytic_radius'])
    ratio = E_cap / E_100
    Dq_lo, Dq_hi = calc.sqrt_interval(17 * tau)
    Dq100_lo, _ = calc.sqrt_interval(17 * tau / 100)
    E_sq_cap = 2 * (2 * Dq_hi + 4 * Dq_hi ** 2) + slope_const / pi_lo
    E_sq_100 = 2 * (2 * Dq100_lo + 4 * Dq100_lo ** 2) + slope_const / 100 / pi_hi
    ratio_sq = E_sq_cap / E_sq_100

    def validate_linear(rv):
        require(99 <= rv <= 101, 'radius does not scale linearly in tau')
        return True
    check('tau_scaling_exponent',
          validate_linear(ratio) and Q(99, 10) <= ratio_sq <= Q(101, 10)
          and rejected(lambda: validate_linear(ratio_sq), 'sqrt_route_b_bound_relabelled_linear'),
          ratio_E_tau_over_tau_100=dec(ratio, 10, 'down'), ratio_with_2sqrt_17tau=dec(ratio_sq, 8, 'down'))

    # changed_model_relabelled
    packet_model = {'model_id': V['model_id'], 'tau': s_(tau), 's': s_(s1), 'triple': list(V['triple_symbolic']), 'route': 'B',
                    'kernel': cert_p['window']['id'], 'reference_route': 'haar', 'state_provenance': V['state_provenance'],
                    'k_prime_over_abs_tau': s_(k_prime / tau), 'label': label}

    def validate_model(pk):
        require(pk['model_id'] == 'AQ_uniform_routeB', 'model id')
        require(rat(pk['tau']) == tau, 'coupling changed')
        require(rat(pk['s']) == s1, 'Euclidean node changed')
        require(pk['triple'] == ['tau/24'] * 3, 'selected triple changed (uniform model ties it to tau)')
        require(pk['route'] == 'B' and pk['reference_route'] == 'haar', 'reference route changed')
        require(pk['kernel'] == 'C2_frozen_AV2', 'kernel changed')
        require(pk['state_provenance'] == 'AQ1_centered_whole_star_subsequence via finite_volume uniform bound', 'state provenance changed')
        require(rat(pk['k_prime_over_abs_tau']) == Q(51, 4), 'Duhamel slope changed')
        require(pk['label'] == label, 'label changed')
        return True
    muts = []
    for key, val in (('tau', '1/100000000000000'), ('tau', '7/725000000'), ('s', '1/2'), ('triple', ['0', '0', '0']),
                     ('reference_route', 'selected_strip'), ('route', 'A'), ('model_id', 'AQ_patterned_zero_selected'),
                     ('model_id', 'FG(two_plaquette,1/2,24,I1.5,physical)'), ('kernel', 'C1_preview'), ('kernel', 'poisson_L_3921569'),
                     ('k_prime_over_abs_tau', '49/4'), ('state_provenance', 'finite_volume_N=3')):
        mutated = dict(packet_model)
        mutated[key] = val
        muts.append(rejected(lambda m=mutated: validate_model(m), 'relabel_' + key + '_' + str(len(muts))))
    check('changed_model_relabelled', validate_model(packet_model) and len(muts) == 12, packet_model=packet_model, rejected=muts)

    # insufficient_verdict_retained
    retained = {
        'at4_poisson_L10000_uniform_slope': {'radius_lower': s_(at4u_lo), 'radius_upper': s_(at4u_hi), 'target_met': False,
                                             'inputs': "D=2sqrt(17|tau|), k'=51|tau|/4"},
        'poisson_floor_uniform_slope_D_to_0': {'floor_lower': s_(floor_lo), 'floor_upper': s_(floor_hi), 'target_met': False},
        'poisson_floor_uniform_slope_with_D_prime': {'floor_lower': s_(floor_with_D_lo), 'target_met': False},
        'window_with_tier_i': {'radius_lower': s_(E_tier_i_lo), 'target_met': False,
                               'label': 'limited-tier value; tier (i) is not the bound premise'},
    }

    def validate_retained(rec):
        require(rec['at4_poisson_L10000_uniform_slope']['target_met'] is (at4u_lo <= target), 'AT4-type insufficiency relabelled')
        require(rec['poisson_floor_uniform_slope_D_to_0']['target_met'] is (floor_lo <= target), 'Poisson floor relabelled')
        require(rec['window_with_tier_i']['target_met'] is (E_tier_i_lo <= target), 'tier (i) relabelled')
        return True

    def validate_design(tv):
        require(tv == tau, 'coupling retuned after outcome')
        return True
    relab = json.loads(json.dumps(retained))
    relab['at4_poisson_L10000_uniform_slope']['target_met'] = True
    relab_i = json.loads(json.dumps(retained))
    relab_i['window_with_tier_i']['target_met'] = True
    tau_th = Q(7478, 10 ** 12)                       # coupling where the D->0 Poisson floor at the uniform slope would meet 10^-6
    k_th = V['k_over_tau'] * tau_th
    L_th = Q((1 / (2 * k_th)).numerator // (1 / (2 * k_th)).denominator + 1)
    floor_th_hi = k_th * calc.log_positive(1 + L_th ** 2)[1] / pi_lo + 1 / (pi_lo * L_th)
    check('insufficient_verdict_retained',
          validate_retained(retained) and validate_design(tau)
          and rejected(lambda: validate_retained(relab), 'at4_uniform_relabelled_met')
          and rejected(lambda: validate_retained(relab_i), 'tier_i_relabelled_met')
          and floor_th_hi <= target
          and rejected(lambda: validate_design(tau_th), 'tau_retuned_to_poisson_floor_threshold'),
          retained=retained, retuned_tau=s_(tau_th), poisson_floor_upper_at_retuned_tau=dec(floor_th_hi, 8, 'up'))

    # exact_arithmetic_admission
    forbidden = ('mp' + 'math', 'num' + 'py', 'fl' + 'int', 'sym' + 'py', 'dec' + 'imal')
    own = (BASE / 'check.py').read_text(encoding='utf-8') + (BASE / 'calculator.py').read_text(encoding='utf-8')
    imports = sorted({ln.strip() for ln in own.splitlines() if ln.startswith('import ') or ln.startswith('from ')})
    check('exact_arithmetic_admission',
          not any(any(fb in ln for fb in forbidden) for ln in imports)
          and rejected(lambda: rat(1e-08), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('NaN'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator')
          and calc_rejects({'tau': 1e-8}, 'calculator_float_tau') and calc_rejects({'s': True}, 'calculator_bool_s'),
          imports=imports, decimals='outward-rounded display strings only')

    # root_n_misuse
    rss_sq = sum(v * v for v in terms.values())
    group_rss_sq = 7 * 7 ** 2 + 2 * 1 ** 2

    def validate_radius_sum(rv):
        require(rv == sum(terms.values(), Q(0)), 'radius is not the linear sum of the itemized terms')
        return True

    def validate_B(bv):
        require(bv == Q(51, 8), '||B_N|| is not the linear sum of the nine group norms')
        return True
    sq345_lo, sq345_hi = calc.sqrt_interval(Q(group_rss_sq))
    check('root_n_misuse',
          validate_radius_sum(radius) and validate_B(B_norm_over_tau) and group_rss_sq == 345
          and rejected(lambda: validate_radius_sum(calc.sqrt_interval(rss_sq)[1]), 'root_sum_of_squares_of_terms')
          and rejected(lambda: validate_radius_sum(radius / 2), 'divided_by_sqrt_4')
          and rejected(lambda: validate_B(sq345_hi / 8), 'root_sum_of_squares_of_nine_group_norms')
          and rejected(lambda: validate_B(Q(51, 8) / 3), 'divided_by_sqrt_9'),
          rss_preview=dec(calc.sqrt_interval(rss_sq)[1], 8, 'up'), linear_sum=dec(radius, 8, 'up'), group_rss='sqrt(345)/8 |tau| (rejected)')

    # no_priority_or_continuum_claim
    claim_flags = {'continuum_claim': False, 'uniform_wilson_claim': True, 'weak_coupling_claim': False,
                   'resolved_interaction_shift': False, 'scientific_priority_verified': False, 'grid_claim': False,
                   'euclidean_node_certified': target_met, 'wilson_mean_sign_certified': False, 'k2_uniform_claimed': False,
                   'state_uniqueness_claim': False}
    false_flags = ('continuum_claim', 'weak_coupling_claim', 'resolved_interaction_shift', 'scientific_priority_verified',
                   'grid_claim', 'wilson_mean_sign_certified', 'k2_uniform_claimed', 'state_uniqueness_claim')

    def validate_claims(fl, scope):
        for name in false_flags:
            require(fl[name] is False, 'forbidden claim flag set: ' + name)
        require(fl['uniform_wilson_claim'] is True and 'fixed-spacing' in scope and 'no uniform Wilson-mean sign certificate' in scope,
                'uniform_wilson_claim must be true and scoped to the fixed-spacing model')
        require(fl['euclidean_node_certified'] is (radius <= target), 'node flag inconsistent with the radius')
        return True
    claim_muts = []
    for name in false_flags:
        fl = dict(claim_flags)
        fl[name] = True
        claim_muts.append(rejected(lambda f=fl: validate_claims(f, calc.UNIFORM_WILSON_SCOPE), 'flag_' + name))
    claim_muts.append(rejected(lambda: validate_claims(claim_flags, 'uniform Wilson theory'), 'uniform_wilson_without_fixed_spacing_scope'))
    flip = dict(claim_flags)
    flip['euclidean_node_certified'] = not target_met
    claim_muts.append(rejected(lambda: validate_claims(flip, calc.UNIFORM_WILSON_SCOPE), 'node_flag_flipped'))
    check('no_priority_or_continuum_claim', validate_claims(claim_flags, calc.UNIFORM_WILSON_SCOPE) and len(claim_muts) == 10,
          rejected=claim_muts, uniform_wilson_claim_scope=calc.UNIFORM_WILSON_SCOPE, historical_or_occult_numeric_premise=False)

    # -------------------- calculator domain --------------------
    cases = [
        ('zero_selected_triple_av2_model', {'selected': ('0', '0', '0')}), ('non_uniform_triple', {'selected': ('tau/24', 'tau/24', '0')}),
        ('selected_wrong_length', {'selected': ('tau/24', 'tau/24')}), ('selected_float', {'selected': ('tau/24', 0.0, 'tau/24')}),
        ('selected_tau_over_3', {'selected': ('1/300000000',) * 3}),
        ('positive_cap_exceeded', {'tau': '1/10000000'}), ('negative_cap_exceeded', {'tau': '-1/10000000'}),
        ('tau_float', {'tau': 1e-8}), ('tau_bool', {'tau': True}), ('tau_nan', {'tau': 'NaN'}),
        ('tau_infinity', {'tau': 'Infinity'}), ('tau_empty', {'tau': ''}), ('tau_zero_denominator', {'tau': '1/0'}),
        ('tau_bad_separator', {'tau': '1//2'}), ('tau_object', {'tau': None}),
        ('s_zero', {'s': '0'}), ('s_negative', {'s': '-1'}), ('alpha_zero', {'alpha': '0'}), ('hbar_negative', {'hbar': '-1'}),
        ('E_star_zero', {'E_star': '0'}), ('lattice_spacing_zero', {'lattice_spacing': '0'}),
        ('target_zero', {'target': '0'}), ('target_float', {'target': 1e-6}),
        ('fixed_design_changed_tau', {'fixed_design': True, 'tau': '1/1000000000'}),
        ('fixed_design_changed_s', {'fixed_design': True, 's': '2'}),
        ('fixed_design_changed_target', {'fixed_design': True, 'target': '1/100'}),
        ('fixed_design_not_boolean', {'fixed_design': 'true'}),
        ('state_tier_tier_i', {'state_tier': 'ax1_forward_tier_i'}), ('window_C1', {'window': 'C1'}), ('window_poisson', {'window': 'poisson'}),
        ('model_zero_selected', {'model': 'AQ_patterned_zero_selected'}),
    ]
    rej = [calc_rejects(kw, name) for name, kw in cases]
    check('calculator_domain_rejections', len(rej) == len(cases), rejected_cases=rej)
    below = calc.certify(tau='1/1000000000')
    check('calculator_exact_input_forms',
          calc.exact(Q(1, 10), 'q') == calc.exact('0.1', 'decimal') == calc.exact('1/10', 'ratio') and calc.exact(1, 'int') == Q(1)
          and calc.certify(tau=Q(1, 10 ** 8))['certified_absolute_error'] == calc.certify(tau='0.00000001')['certified_absolute_error']
          == calc.certify(selected=(Q(1, 2400000000),) * 3)['certified_absolute_error'] == cert_p['certified_absolute_error']
          and rat(below['state_bound_D_prime']) < D_prime and below['state_bound_equals_ax1_gate_value'] is False)
    check('calculator_fixed_design_matches',
          cert_p['fixed_design'] is True and rat(cert_p['certified_absolute_error']) == radius and cert_p['grid_claim'] is False
          and cert_p['continuum_claim'] is False and cert_p['weak_coupling_claim'] is False and cert_p['uniform_wilson_claim'] is True,
          calculator_sha256=calc_sha, reusable_mode='below the cap D\' is the gate\'s admitted tier-(ii) |tau|-form, pinned to the gate rational at the cap and never above it')

    # -------------------- error ledger --------------------
    error_terms = {
        'state': {'value': s_(terms['state']), 'preview': dec(terms['state'], 12, 'up'),
                  'source': "M_0*D', D' the AX1 gate forward tier-(ii) trace-distance bound; trace duality with ||W alpha^0_theta(W)||<=1 (no D/2)"},
        'mean_square': {'value': s_(terms['mean_square']), 'preview': dec(terms['mean_square'], 12, 'up'),
                        'source': "M_0*m^2 with m^2<=D'^2 (AX1 gate item 6)"},
        'kernel_dynamics': {'value': s_(terms['kernel_dynamics']), 'preview': dec(terms['kernel_dynamics'], 12, 'up'),
                            'source': "k'*M_1=(51|tau|/4)(4s/pi) with the Machin pi lower bound; no cutoff, no tail"},
        'arithmetic': {'value': s_(terms['arithmetic']), 'preview': dec(terms['arithmetic'], 4, 'up'),
                       'source': 'half-width of the directed enclosure of e^{-3}/4 about the exact rational datum'},
    }
    check('error_terms_itemized_preregistered', sorted(error_terms) == sorted(V['error_terms']), terms=sorted(error_terms), not_applicable='none')

    # -------------------- packet --------------------
    headline = {
        'certified_datum': s_(datum), 'certified_absolute_error': s_(radius), 'certified_absolute_error_outward_1e-40': s_(radius_out),
        'radius_preview_up': dec(radius, 12, 'up'), 'datum_preview': fixed(datum, 30, 'down'),
        'interval': {'lower': s_(lo_C), 'upper': s_(hi_C)},
        'interval_preview': {'lower_down': fixed(lo_C, 18, 'down'), 'upper_up': fixed(hi_C, 18, 'up')},
        'free_interval_preview': {'lower_down': fixed(free_lo, 30, 'down'), 'upper_up': fixed(free_hi, 30, 'up')},
        'width': s_(hi_C - lo_C), 'target': s_(target), 'target_met': target_met,
        'margin_target_over_radius_lower': dec(target / radius, 6, 'down'),
        'D_prime': s_(D_prime), 'k_prime': s_(k_prime), 'M0': '2', 'M1': '4s/pi', 'M2': '2s^2',
        'terms_preview_up': {kk: dec(v, 12, 'up') for kk, v in terms.items()},
    }
    packet = {
        'loop': 'AX2', 'direction': 'forward', 'human_author': 'Hruday N M (BUNZEEY)',
        'contribution_alias': 'HNM-AX2-F uniform-model window certificate (single forward producer)',
        'contract_sha256': CONTRACT_SHA256, 'ax1_gate_sha256': AX1_GATE_SHA256, 'av2_gate_sha256': G2['sha256'],
        'check_py_sha256_recorded_before_evaluation': check_sha, 'calculator_py_sha256_recorded_before_evaluation': calc_sha,
        'model': packet_model, 'label': label, 'tau_values': {'+': s_(tau), '-': s_(-tau)},
        'window': {'definition': 'g(x)=e^{-sx} (x>=0); g(x)=e^{sx}(1-2sx+2s^2x^2) (x<0)',
                   'transform': 'ghat(theta)=4s^3/(pi(s-i theta)^3(s+i theta))', 'M0': '2', 'M1': '4s/pi', 'M2': '2s^2',
                   'convention': 'ghat(theta)=(2pi)^-1 int g(x)e^{-i theta x}dx; c(theta)=<chi,e^{i theta G}chi>', 'source': 'AV2 gate, verbatim'},
        'pi_interval': {'lower': s_(pi_lo), 'upper': s_(pi_hi)},
        'certificate_plus': cert_p, 'certificate_minus_U_E_mirror_replay': cert_m,
        'headline': headline, 'error_terms_itemized': error_terms, 'retained_failures': retained,
        'crossover': {'s_star_lower': s_(s_star_lo), 's_star_upper': s_(s_star_hi),
                      'preview': [dec(s_star_lo, 11, 'down'), dec(s_star_hi, 11, 'up')], 'grid_claim': False},
        'lemma_transfer': transfer,
        'sub_labels': ['reference_unresolved'],
        'claim_exclusions': V['claim_exclusions'], 'preregistration_claim_exclusions': V['prereg_exclusions'],
        'K_2_note': V['K2_note'],
        'proposed_forward_verdict': single_decl['proposed_forward_verdict'],
        'producers': ['forward'], 'single_direction_independent_replay_required': True,
        'independent_review_claimed': False, 'mirror_is_second_confirmation': False,
        'uniform_wilson_claim_scope': calc.UNIFORM_WILSON_SCOPE,
    }
    packet.update(claim_flags)

    # -------------------- coherent evidence tampering --------------------
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
        validate_claims({k1: pk[k1] for k1 in claim_flags}, pk['uniform_wilson_claim_scope'])
        validate_single(pk)
        require(sorted(inv) == sorted(set(declared)), 'premise snapshot inventory incomplete')
        recomputed = calc.certify(fixed_design=True)
        require(pk['headline']['certified_absolute_error'] == recomputed['certified_absolute_error'], 'radius differs from recomputation')
        require(pk['headline']['certified_datum'] == recomputed['certified_datum'], 'datum differs from recomputation')
        require(pk['headline']['target_met'] is recomputed['target_met'], 'target Boolean differs from recomputation')
        validate_state_bound(rat(pk['headline']['D_prime']))
        require(rat(pk['headline']['k_prime']) == k_prime, 'slope differs')
        validate_retained(pk['retained_failures'])
        validate_model(pk['model'])
        return True

    base_packet = dict(packet)
    base_packet['checks'] = [dict(ch) for ch in CHECKS]
    base_packet['packet_sha256'] = packet_hash(base_packet)

    def rebound(edit, inv=None):
        def run():
            pk = json.loads(json.dumps(base_packet))
            edit(pk)
            pk['packet_sha256'] = packet_hash(pk)
            return validate_packet(pk, inventory if inv is None else inv)
        return run

    def flip_control(pk):
        for ch in pk['checks']:
            if ch['id'] == 'selected_incidence_count':
                ch['passed'] = False

    def halve_radius(pk):
        pk['headline']['certified_absolute_error'] = s_(rat(pk['headline']['certified_absolute_error']) / 2)

    def reverse_D(pk):
        pk['headline']['D_prime'] = s_(G1['D_reverse_refinement'])

    def av2_slope(pk):
        pk['headline']['k_prime'] = s_(G2['k_over_tau'] * tau)

    def at4_met(pk):
        pk['retained_failures']['at4_poisson_L10000_uniform_slope']['target_met'] = True

    def weak(pk):
        pk['weak_coupling_claim'] = True

    def reverse_claimed(pk):
        pk['producers'] = ['forward', 'reverse']

    def zero_triple(pk):
        pk['model']['triple'] = ['0', '0', '0']
    inv_missing = dict(inventory)
    inv_missing.pop(AX1_GATE_REL)
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(rebound(flip_control), 'control_boolean_flipped_hash_rebound')
          and rejected(rebound(lambda pk: None, inv_missing), 'ax1_gate_snapshot_removed_hash_rebound')
          and rejected(rebound(halve_radius), 'radius_halved_hash_rebound')
          and rejected(rebound(reverse_D), 'reverse_refinement_D_hash_rebound')
          and rejected(rebound(av2_slope), 'seven_star_slope_hash_rebound')
          and rejected(rebound(at4_met), 'at4_uniform_target_flipped_hash_rebound')
          and rejected(rebound(weak), 'weak_coupling_flag_hash_rebound')
          and rejected(rebound(reverse_claimed), 'reverse_producer_claimed_hash_rebound')
          and rejected(rebound(zero_triple), 'zero_selected_model_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    unmutated = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch.get('rejected_mutations')]
    require(not unmutated, 'contract controls without a rejected damaging mutation: ' + ','.join(unmutated))
    require(not PENDING, 'mutation labels not attached to a check')
    packet['checks'] = CHECKS
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['check_count'] = str(len(CHECKS))
    packet['rejected_mutation_count'] = str(sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS))
    return packet


def numbers_are_strings(obj):
    """No JSON number anywhere: every numeric value is an exact rational string."""
    if isinstance(obj, bool) or obj is None:
        return True
    if isinstance(obj, (int, float)):
        return False
    if isinstance(obj, dict):
        return all(isinstance(k, str) for k in obj) and all(numbers_are_strings(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(numbers_are_strings(v) for v in obj)
    return isinstance(obj, str)


def main():
    ap = argparse.ArgumentParser(description='AX2 forward exact checker')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    require(out.is_absolute(), 'absolute output directory required')
    out = out.resolve()
    require(not out.exists(), 'fresh (non-existent) output directory required')
    require(ROOT not in out.parents and out != ROOT, 'output directory must be outside the checkout')
    check_sha = sha(BASE / 'check.py')        # recorded before any evaluation
    calc_sha = sha(BASE / 'calculator.py')
    result = compute(check_sha, calc_sha)
    require(numbers_are_strings(result), 'non-string number in results')
    out.mkdir(parents=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    sources = {}
    for p in sorted(BASE.rglob('*')):
        rel = p.relative_to(BASE)
        require('__pycache__' not in rel.parts and p.suffix != '.pyc', 'interpreter cache inside the producer closure')
        if p.is_file() and (rel.parts[0] == 'inputs' or p.name in ('check.py', 'calculator.py', 'report.md')) and rel.parts[0] != 'output':
            sources[rel.as_posix()] = sha(p)
    manifest = {'loop': 'AX2', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AX2', 'direction': 'forward', 'checks': str(len(result['checks'])),
                      'radius_preview': result['headline']['radius_preview_up'], 'target_met': result['headline']['target_met'],
                      'euclidean_node_certified': result['euclidean_node_certified']}, sort_keys=True))


if __name__ == '__main__':
    main()
