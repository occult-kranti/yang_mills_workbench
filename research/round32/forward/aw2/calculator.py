#!/usr/bin/env python3
"""Exact-rational AW2 enclosure calculator for the Wilson mean (forward producer).

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

Model: the zero-selected patterned AQ subfamily (SU(2) Kogut-Susskind form on
Z^3 at fixed spacing, coarse 24-link factors, selected triple exactly (0,0,0),
Haar product reference, whole stars phi_b=-(tau/3) sum W_f under I1.5, centered
whole-star boxes N>=2, original xz Wilson loop W with cover R={0,e_z}).

For every state in the whole set S(tau) of AQ1 subsequential limits (and every
centered box N>=2 and on-site cutoff) the AW1 gate admits

    omega_tau(W) = +tau/144 + r(tau),   |r(tau)| <= K_2^+ tau^2,   |tau| <= 10^-8,

so omega_tau(W) lies in [tau/144 - K_2^+ tau^2, tau/144 + K_2^+ tau^2].

Inputs are exact only (int, Fraction, 'p/q' or plain decimal text); floats and
Booleans are rejected. K_2^+ and the first-order coefficient cannot be
supplied: both are parsed from the hash-verified AW1 gate snapshot in
inputs/. The frozen AW2 coupling rule is parsed from the AW1 contract snapshot,
whose hash is the AW1 gate's binding. Domain: selected triple zero,
0<|tau|<=10^-8, exact-tier constant only. `fixed_design=True` enforces
|tau|=tau_AW2 as evaluated by the rule (the negative sign is the mirrored
replay of the flip lemma, not a second confirmation).

This is a static equal-time statement (sub-label static_not_dynamic): no
dynamical correction, mass shift, susceptibility or centered-correlation shift.
Standard library only; no binary floating value enters a returned number.
"""
import hashlib
import json
import re
from fractions import Fraction as Q
from pathlib import Path

BASE = Path(__file__).resolve().parent
AW1_GATE_REL = 'research/round32/advisor/aw1-gate.json'
AW1_GATE_SHA256 = '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae'
AW1_CONTRACT_REL = 'research/round32/contracts/aw1.json'
DECIMAL_DIGITS = 12
TIER = 'exact'


class CalculatorError(RuntimeError):
    """An internal invariant or a premise binding of the calculator failed."""


def require(condition, message):
    if not condition:
        raise CalculatorError(message)


def textq(x):
    x = Q(x)
    return str(x.numerator) if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)


def _decimal(x, digits, upward):
    """Directed decimal text of an exact rational: rounded toward +inf (upward) or -inf."""
    x = Q(x)
    if x == 0:
        return '0'
    a = abs(x)
    e = 0
    while a >= Q(10) ** (e + 1):
        e += 1
    while a < Q(10) ** e:
        e -= 1
    shift = e - digits + 1
    scaled = x / Q(10) ** shift
    n = -((-scaled.numerator) // scaled.denominator) if upward else scaled.numerator // scaled.denominator
    sign = '-' if n < 0 else ''
    body = str(abs(n))
    out = sign + body[0] + ('.' + body[1:] if len(body) > 1 else '') + 'e' + str(shift + len(body) - 1)
    back = Q(out)
    require((back >= x) if upward else (back <= x), 'directed decimal rounding failed')
    return out


def dec_up(x, digits=DECIMAL_DIGITS):
    return _decimal(x, digits, True)


def dec_down(x, digits=DECIMAL_DIGITS):
    return _decimal(x, digits, False)


def exact(value, name):
    """Exact rational input: int, Fraction, 'p/q' or plain decimal text. float/bool rejected."""
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError(name + ': exact rational input required; bool/float rejected')
    if isinstance(value, Q):
        return value
    if isinstance(value, int):
        return Q(value)
    if not isinstance(value, str) or not re.fullmatch(r'[+-]?(?:[0-9]+/[0-9]+|[0-9]+(?:\.[0-9]+)?)', value):
        raise ValueError(name + ': expected integer, plain decimal or numerator/denominator text')
    num, _, den = value.partition('/')
    if den and int(den) == 0:
        raise ValueError(name + ': zero denominator')
    return Q(value)


# ---------------------------------------------------------------------------
# Admitted premises: read from the hash-verified AW1 gate snapshot only.
# ---------------------------------------------------------------------------
def _snapshot(rel):
    path = BASE / 'inputs' / rel
    require(path.is_file(), 'missing premise snapshot ' + rel)
    return path.read_bytes()


def _match(pattern, text, label):
    m = re.search(pattern, text)
    require(m is not None, 'premise text not parsed: ' + label)
    return m


def gate_constants():
    """K_2^+, the first-order coefficient, the cap and the frozen rule, from the AW1 gate chain."""
    raw = _snapshot(AW1_GATE_REL)
    require(hashlib.sha256(raw).hexdigest() == AW1_GATE_SHA256, 'AW1 gate snapshot differs from the bound gate bytes')
    gate = json.loads(raw.decode('utf-8'))
    require(gate.get('loop') == 'AW1' and gate.get('verdict') == 'accepted_within_scope', 'AW1 gate identity')
    m = _match(r'Bind K_2\^\+ = (\d+)/(\d+) \(about [0-9.]+; the largest of the three valid exact-tier upper bounds, '
               r'outward ceiling (\d+)/10\^(\d+)\) as the admitted constant for AW2', gate['decision'], 'gate decision K_2^+')
    K = Q(int(m.group(1)), int(m.group(2)))
    ceiling = Q(int(m.group(3)), 10 ** int(m.group(4)))
    m2 = _match(r'the bound value is K_2\^\+=(\d+)/(\d+) \(', gate['accepted'], 'gate accepted K_2^+')
    require(Q(int(m2.group(1)), int(m2.group(2))) == K, 'gate decision and accepted texts bind different K_2^+')
    require(K > 0 and ceiling >= K, 'outward ceiling must dominate K_2^+')
    m3 = _match(r'\(3\) omega_tau\(W\)=\+tau/(\d+)\+r\(tau\) under I1\.5', gate['accepted'], 'gate first-order coefficient')
    c1 = Q(1, int(m3.group(1)))
    m4 = _match(r'at both signs of tau with \|tau\|<=10\^-(\d+):', gate['accepted'], 'gate cap')
    cap = Q(1, 10 ** int(m4.group(1)))
    _match(r'\(4\) \|r\(tau\)\|<=K_2\^\+ tau\^2 uniformly in N, cutoff and every AQ1 subsequential limit at the exact tier',
           gate['accepted'], 'gate uniform remainder statement')
    craw = _snapshot(AW1_CONTRACT_REL)
    require(hashlib.sha256(craw).hexdigest() == gate['bindings'][AW1_CONTRACT_REL], 'AW1 contract snapshot differs from the gate binding')
    rule_text = json.loads(craw.decode('utf-8'))['parameters']['aw2_coupling_rule']
    m5 = _match(r'^tau_AW2 = the largest element of the decade grid \{10\^-(\d+), 10\^-(\d+), \.\.\.\} with K_2\^\+ \* tau <= '
                r'(\d+)/(\d+) \(half the first-order coefficient\), K_2\^\+ the admitted exact-tier remainder constant; '
                r'frozen here, never chosen after K_2 is seen$', rule_text, 'AW1 frozen rule')
    start = int(m5.group(1))
    require(int(m5.group(2)) == start + 1, 'decade grid step')
    bound = Q(int(m5.group(3)), int(m5.group(4)))
    require(bound == c1 / 2, 'rule bound is not half the first-order coefficient')
    require(Q(1, 10 ** start) == cap, 'rule grid must start at the cap')
    return {'K': K, 'ceiling': ceiling, 'c1': c1, 'cap': cap, 'grid_start': start, 'rule_bound': bound,
            'rule_text': rule_text, 'gate_sha256': AW1_GATE_SHA256}


def coupling_rule(G):
    """The frozen AW1 decade-grid rule, evaluated from the gate constant (never a literal)."""
    k = G['grid_start']
    steps = []
    while True:
        tau = Q(1, 10 ** k)
        lhs = G['K'] * tau
        steps.append({'tau': textq(tau), 'K_2_plus_tau': textq(lhs), 'bound': textq(G['rule_bound']),
                      'satisfied': lhs <= G['rule_bound']})
        if lhs <= G['rule_bound']:
            return tau, steps
        k += 1
        require(k <= G['grid_start'] + 60, 'decade grid exhausted')


# ---------------------------------------------------------------------------
# The enclosure.
# ---------------------------------------------------------------------------
def enclose(*, tau, selected=('0', '0', '0'), fixed_design=False, tier=TIER,
            alpha='1', hbar='1', E_star='1', lattice_spacing='1'):
    """Enclose omega_tau(W) for every AQ1 subsequential limit at the zero selected triple.

    K_2^+ is not an argument (it is read from the AW1 gate); there is no
    centering argument (the omega(W) path is uncentered). Raises ValueError
    outside the proved domain and TypeError for unknown keywords.
    """
    if type(fixed_design) is not bool:
        raise ValueError('fixed_design must be a Boolean')
    if tier != TIER:
        raise ValueError('only the exact tier bound by the AW1 gate certifies; the crude tier fails at the cap '
                         'and is a limited-tier control')
    data = {name: exact(value, name) for name, value in {
        'tau': tau, 'alpha': alpha, 'hbar': hbar, 'E_star': E_star, 'lattice_spacing': lattice_spacing}.items()}
    if not isinstance(selected, (tuple, list)) or len(selected) != 3:
        raise ValueError('selected must contain exactly three coefficients')
    triple = tuple(exact(x, 'selected') for x in selected)
    if any(triple):
        raise ValueError('proved domain requires the zero selected triple (Haar reference; flip lemma at kappa=0)')
    if any(data[n] <= 0 for n in ('alpha', 'hbar', 'E_star', 'lattice_spacing')):
        raise ValueError('physical scales must be positive')
    G = gate_constants()
    t = data['tau']
    if t == 0:
        raise ValueError('tau=0 is the free reference (omega_0(W)=0 exactly); the enclosure is posed for 0<|tau|<=10^-8')
    if abs(t) > G['cap']:
        raise ValueError('coupling exceeds the admitted cap |tau|<=10^-8')
    tau_aw2, steps = coupling_rule(G)
    if fixed_design and abs(t) != tau_aw2:
        raise ValueError('fixed design requires |tau| = tau_AW2 from the frozen AW1 rule')
    K, c1 = G['K'], G['c1']
    first = c1 * t
    radius = K * t * t
    lo, hi = first - radius, first + radius
    require(lo < first < hi and hi - lo == 2 * radius, 'enclosure geometry')
    excludes = lo > 0 or hi < 0
    sign_margin = (c1 * abs(t)) / radius
    exclusion_margin = (c1 * abs(t) - radius) / radius
    require(exclusion_margin == sign_margin - 1, 'margin identity m = S - 1')
    at_cap = abs(t) == G['cap']
    below_cap_certified = excludes and abs(t) < G['cap']
    labels = ['static_not_dynamic'] + (['sign_certified_below_cap'] if below_cap_certified else [])
    return {
        'model': 'AQ_patterned_zero_selected: omega_tau(W) for every state in the whole set of AQ1 subsequential limits '
                 '(and every centered whole-star box N>=2, every on-site cutoff), cover R={0,e_z}',
        'tau': textq(t), 'sign': '+' if t > 0 else '-', 'fixed_design': fixed_design,
        'mirrored_coupling_replay': t < 0,
        'selected_coefficients_over_alpha': [textq(x) for x in triple],
        'physical_scales': {n: textq(data[n]) for n in ('alpha', 'hbar', 'E_star', 'lattice_spacing')},
        'physical_scale_note': 'omega(W) is a dimensionless static equal-time mean; no clock and no scale enters the enclosure',
        'tier': TIER, 'K_2_plus': textq(K), 'K_2_plus_source': 'AW1 gate decision text (sha256 %s)' % G['gate_sha256'],
        'K_2_plus_outward_ceiling': textq(G['ceiling']),
        'first_order_coefficient': textq(c1), 'first_order_value': textq(first),
        'second_order_radius': textq(radius),
        'enclosure': {'lower': textq(lo), 'upper': textq(hi)},
        'enclosure_decimal_outward': {'lower': dec_down(lo), 'upper': dec_up(hi)},
        'excludes_zero': excludes,
        'sign_of_omega_W': ('+' if lo > 0 else '-') if excludes else 'undetermined',
        'sign_margin': textq(sign_margin), 'sign_margin_decimal_down': dec_down(sign_margin),
        'exclusion_margin': textq(exclusion_margin), 'exclusion_margin_decimal_down': dec_down(exclusion_margin),
        'coupling_rule': {'tau_AW2': textq(tau_aw2), 'steps': steps, 'rule': G['rule_text']},
        'at_cap': at_cap,
        'sub_labels': labels,
        'static_not_dynamic': True,
        'sign_certified_below_cap': below_cap_certified,
        'resolved_interaction_shift_at_cap': excludes and at_cap,
        'centered_correlation_shift': 'unresolved (AV2 reference_unresolved)',
        'dynamical_correction_claim': False, 'mass_shift_claim': False, 'susceptibility_claim': False,
        'continuum_claim': False, 'uniform_wilson_claim': False, 'scientific_priority_verified': False,
        'uniqueness_claim': False,
    }
