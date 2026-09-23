#!/usr/bin/env python3
"""Shared helpers for the Jung/Pauli lens, Round32 sub-round 1, assistant scripts.

Standing (loop3-signoff.md section 4 / the calling task): these are pre-registration
audits and tests for the lens. They count zero research loops. Nothing here is a
producer, a contract, a gate or a skeptical review, and nothing computed here is read
back into any contract, gate or skeptical review. Human project author: Hruday N M
(BUNZEEY); AI-assisted.

Every admission-relevant Boolean below is decided in exact ``fractions.Fraction``
arithmetic; decimal strings are truncated, labelled previews only and never decide
anything. The AV1/AV2 state-bound and window-radius formulas are re-implemented here
from the frozen contracts (``research/round32/contracts/av1.json``,
``research/round32/contracts/av2.json``) and the AV1 skeptical review
(``research/round32/skeptic/av1.md``); this module does not import
``forward/av1/check.py``, ``reverse/av1/check.py`` or any other producer/skeptic
module, per the task instruction.

Usage: each sibling script imports this module (``import common``) after adding this
directory to ``sys.path``; run every script with ``python3 -B``.
"""
import json
import re
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]  # assistant-1 -> jung -> experts -> round32 -> research -> ROOT
RESEARCH = ROOT / 'research' / 'round32'
CONTRACT_AV1 = RESEARCH / 'contracts' / 'av1.json'
CONTRACT_AV2 = RESEARCH / 'contracts' / 'av2.json'
GATE_AV1 = RESEARCH / 'advisor' / 'av1-gate.json'
SKEPTIC_AV1_JSON = RESEARCH / 'skeptic' / 'av1.json'
FORWARD_AV1_CHECK = RESEARCH / 'forward' / 'av1' / 'check.py'
REVERSE_AV1_CHECK = RESEARCH / 'reverse' / 'av1' / 'check.py'
FORWARD_AV1_RESULTS = RESEARCH / 'forward' / 'av1' / 'output' / 'results.json'
REVERSE_AV1_RESULTS = RESEARCH / 'reverse' / 'av1' / 'output' / 'results.json'


class AuditError(Exception):
    """An audit or a test condition failed, or a damaging mutation was accepted."""


def require(condition, message):
    if not condition:
        raise AuditError(message)


def expect_rejected(fn, *args, **kwargs):
    """Run a damaging mutation / a mislabelled admission attempt; it must raise
    AuditError. Returns the caught message; raises AuditError itself if the
    mutation was wrongly accepted (mirrors the producers' rejected()/control()
    idiom, independently written)."""
    try:
        fn(*args, **kwargs)
    except AuditError as exc:
        return str(exc)
    raise AuditError('damaging mutation or mislabelled admission was accepted')


def load_json(path):
    return json.loads(Path(path).read_bytes().decode('utf-8'))


def rat(value):
    """Exact rational parser: int, Fraction, or an integer/ratio string. No floats."""
    if isinstance(value, bool) or isinstance(value, float):
        raise AuditError('non-exact input rejected: ' + repr(value))
    if isinstance(value, (int, Q)):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value):
        return Q(value)
    raise AuditError('malformed rational rejected: ' + repr(value))


def dec(q, digits=10):
    """Truncated scientific-decimal preview of an exact rational. Never decides anything."""
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


def s(q):
    return str(Q(q))


def merge_results(path, key, payload):
    """Read-modify-write results.json, keeping the other scripts' sections."""
    data = {}
    if Path(path).exists():
        try:
            data = load_json(path)
        except Exception:
            data = {}
    data[key] = payload
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return data


# ---------------------------------------------------------------------------
# Contracts.
# ---------------------------------------------------------------------------
def av1_contract():
    c = load_json(CONTRACT_AV1)
    require(c.get('id') == 'AV1' and c.get('status') == 'frozen_before_production', 'AV1 contract identity')
    return c


def av2_contract():
    c = load_json(CONTRACT_AV2)
    require(c.get('id') == 'AV2' and c.get('status') == 'frozen_before_production', 'AV2 contract identity')
    return c


def av1_constants(c=None):
    """Re-derive the AV1 tier (i)/(ii) formula constants from the frozen contract text,
    independently of forward/av1/check.py and reverse/av1/check.py."""
    c = c or av1_contract()
    p = c['parameters']
    am2 = p['am2_constants']
    tau_cap = rat(p['tau_cap'])
    G_R = rat(am2['G_at_R_upper'])
    Gp_R = rat(am2['G_prime_at_R_upper'])
    mJ = re.fullmatch(r'<=(\d+)\|tau\|', am2['per_site_sum_J'])
    require(mJ is not None, 'per_site_sum_J not parsed from the contract')
    J_per_tau = int(mJ.group(1))
    req5 = c['required'][4]
    m1 = re.search(r'candidate (\d+)\|tau\|/(\d+)\)', req5)
    require(m1 is not None, 'tier (ii) candidate coefficient not parsed from contract item 5')
    t1_coeff = Q(int(m1.group(1)), int(m1.group(2)))
    m2 = re.search(r't<=t_1/\(1-(\d+)J\)', req5)
    require(m2 is not None, 'self-consistent remainder coefficient not parsed from contract item 5')
    require(int(m2.group(1)) == Gp_R, "self-consistent coefficient must equal the AM2 G'(R) bound")
    target = rat(c['preregistration']['target']['value'])
    return {'tau_cap': tau_cap, 'G_R': G_R, 'Gp_R': Gp_R, 'J_per_tau': J_per_tau,
            't1_coeff': t1_coeff, 'target': target}


def av2_constants(c=None):
    c = c or av2_contract()
    p = c['parameters']
    return {'s': rat(p['s']), 'tau_cap': rat(p['tau']),
            'absolute_target': rat(p['absolute_target']),
            'duhamel_k_coefficient': Q(49, 4)}  # k = 49|tau|/4, contract "duhamel_slope"


# ---------------------------------------------------------------------------
# AV1 state-bound formulas (forward-route form: eps=2t+t^2, D=2eps(1+eps)/(1+eps^2)),
# reproduced exactly against the admitted forward D_i/D_ii in skeptic/av1.md.
# ---------------------------------------------------------------------------
def D_of_eps(eps):
    eps = Q(eps)
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def D_tier_i(tau_abs, C=None):
    C = C or av1_constants()
    tau_abs = Q(tau_abs)
    require(tau_abs >= 0, 'tau must be nonnegative in D_tier_i')
    J = C['J_per_tau'] * tau_abs
    t = J * C['G_R']
    eps = 2 * t + t * t
    return {'tier': 'i', 'tau_abs': tau_abs, 'J': J, 't': t, 'eps': eps, 'D': D_of_eps(eps)}


def D_tier_ii(tau_abs, C=None):
    C = C or av1_constants()
    tau_abs = Q(tau_abs)
    require(tau_abs >= 0, 'tau must be nonnegative in D_tier_ii')
    J = C['J_per_tau'] * tau_abs
    t1 = C['t1_coeff'] * tau_abs
    K = C['Gp_R'] * J
    if tau_abs > 0:
        require(K < 1, 'self-consistent factor 352J must stay below one')
        T = t1 / (1 - K)
    else:
        T = Q(0)
    eps = 2 * T + T * T
    return {'tier': 'ii', 'tau_abs': tau_abs, 'J': J, 't1': t1, 'K': K, 'T': T, 'eps': eps, 'D': D_of_eps(eps)}


# ---------------------------------------------------------------------------
# AT4 square-root state bound, D_sqrt(tau) = 2*sqrt(49|tau|/3). D_sqrt^2 is exact
# and *linear* in |tau|; a directed rational bracket for D_sqrt itself is built by
# Newton's method (independently written, no import of any producer's sqrt helper).
# ---------------------------------------------------------------------------
def D_sqrt_squared(tau_abs):
    """Exact rational: D_sqrt(tau)^2 = 4*49*|tau|/3."""
    tau_abs = Q(tau_abs)
    require(tau_abs >= 0, 'tau must be nonnegative in D_sqrt_squared')
    return 4 * Q(49, 3) * tau_abs


def sqrt_bracket(y, denominator=10 ** 30):
    """Directed rational bracket [lo,hi] of sqrt(y) for y>=0, lo*lo<=y<=hi*hi, by
    integer Newton iteration on a fixed-denominator numerator (independent
    reimplementation of the standard isqrt-scaling technique)."""
    y = Q(y)
    require(y >= 0, 'negative argument to sqrt_bracket')
    if y == 0:
        return Q(0), Q(0)
    from math import isqrt
    scaled = y.numerator * denominator * denominator // y.denominator
    k = isqrt(scaled)
    while (k + 1) ** 2 <= scaled:
        k += 1
    while k * k > scaled:
        k -= 1
    lo = Q(k, denominator)
    hi = Q(k + 1, denominator)
    require(lo * lo <= y, 'sqrt_bracket lower bound too high')
    require(y <= hi * hi, 'sqrt_bracket upper bound too low')
    return lo, hi


def D_sqrt_bracket(tau_abs, denominator=10 ** 30):
    y = D_sqrt_squared(tau_abs)
    return sqrt_bracket(y, denominator)


# ---------------------------------------------------------------------------
# pi and exp(-3) directed rational brackets (independently written Machin/Taylor
# enclosures; same standard techniques the AV1 producers use, not their code).
# ---------------------------------------------------------------------------
def atan_inverse_bracket(k, terms=48):
    """Consecutive partial sums of the alternating series for arctan(1/k) bracket it."""
    total = Q(0)
    previous = Q(0)
    for j in range(terms):
        previous = total
        term = Q(1, (2 * j + 1) * k ** (2 * j + 1))
        total = total + term if j % 2 == 0 else total - term
    return (previous, total) if previous <= total else (total, previous)


def pi_bracket():
    """Machin's formula pi = 16*atan(1/5) - 4*atan(1/239), as a tight rational bracket."""
    lo5, hi5 = atan_inverse_bracket(5)
    lo239, hi239 = atan_inverse_bracket(239)
    lo = 16 * lo5 - 4 * hi239
    hi = 16 * hi5 - 4 * lo239
    require(lo < hi, 'pi bracket must be nondegenerate')
    require(Q(314159, 100000) < lo and hi < Q(314160, 100000), 'pi bracket outside the known digits')
    return lo, hi


def exp_upper_bracket(x, terms=40):
    """Upper bound of exp(x) for x>=0 by a truncated positive Taylor series plus a
    geometric tail (valid once x/(terms+2) < 1)."""
    x = Q(x)
    require(x >= 0, 'exp_upper_bracket requires x>=0')
    from math import factorial
    partial = sum((x ** k / factorial(k) for k in range(terms + 1)), Q(0))
    ratio = x / (terms + 2)
    require(ratio < 1, 'exp_upper_bracket needs more terms for this x')
    tail = x ** (terms + 1) / factorial(terms + 1) / (1 - ratio)
    return partial + tail


def exp_lower_bracket(x, terms=40):
    x = Q(x)
    require(x >= 0, 'exp_lower_bracket requires x>=0')
    from math import factorial
    return sum((x ** k / factorial(k) for k in range(terms + 1)), Q(0))


def exp_minus3_over4_bracket():
    """Directed rational bracket [lo,hi] of exp(-3)/4, via e^{-3}=1/e^3 and a
    positive-term Taylor bracket of e^3 (independent reimplementation)."""
    e3_lo = exp_lower_bracket(3)
    e3_hi = exp_upper_bracket(3)
    require(0 < e3_lo <= e3_hi, 'e^3 bracket malformed')
    lo = Q(1) / (4 * e3_hi)
    hi = Q(1) / (4 * e3_lo)
    require(lo <= hi, 'exp(-3)/4 bracket malformed')
    return lo, hi


# ---------------------------------------------------------------------------
# AV2 window radius, E = M0(D+D^2) + k*M1 = 2(D+D^2) + 49|tau|s/pi, itemized into
# state + mean_square + kernel_dynamics + arithmetic (contract item 4), with the
# arithmetic term taken as the width of the exp(-3)/4 Taylor bracket above.
# ---------------------------------------------------------------------------
def av2_window_radius(tau_abs, s_value, D):
    """Returns a dict with the four itemized terms and their exact-rational sum E."""
    tau_abs = Q(tau_abs)
    s_value = Q(s_value)
    D = Q(D)
    pi_lo, pi_hi = pi_bracket()
    e3_lo, e3_hi = exp_minus3_over4_bracket()
    state_term = 2 * D
    mean_square_term = 2 * D * D
    # 1/pi <= 1/pi_lo: dividing by the *lower* pi bound gives a valid upper bound.
    kernel_dynamics_term = 49 * tau_abs * s_value / pi_lo
    arithmetic_term = e3_hi - e3_lo
    E = state_term + mean_square_term + kernel_dynamics_term + arithmetic_term
    return {'tau_abs': tau_abs, 's': s_value, 'state_term': state_term,
            'mean_square_term': mean_square_term, 'kernel_dynamics_term': kernel_dynamics_term,
            'arithmetic_term': arithmetic_term, 'E': E, 'pi_lo': pi_lo, 'pi_hi': pi_hi,
            'exp_minus3_over4_lo': e3_lo, 'exp_minus3_over4_hi': e3_hi}
