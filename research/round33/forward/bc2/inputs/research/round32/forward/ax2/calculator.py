#!/usr/bin/env python3
"""Exact-rational AX2 uniform-model window calculator (forward, single producer).

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

Encloses the actual centered Euclidean Wilson correlation C_tau(s) of a chosen
AQ1 subsequential state of the UNIFORM Kogut-Susskind SU(2) Hamiltonian at fixed
spacing and strong bare coupling (route B of AX1: Haar reference, whole stars
plus one single-factor group per factor for its three selected xy faces), with
the frozen AV2 C^2 window g(x)=e^{-sx} (x>=0), e^{sx}(1-2sx+2s^2x^2) (x<0):

    |C_tau(s)-e^{-3s}/4| <= E'(s) = M_0(D'+D'^2)+k' M_1,
    M_0=2, M_1=4s/pi, k'=51|tau|/4 (seven stars and two single-factor groups).

Only the proved uniform domain is accepted: the uniform selected triple
(tau/24,tau/24,tau/24), rational |tau|<=10^-8, s>0 and positive physical
scales. D' is not an input: at the cap it is the exact rational bound by the
AX1 gate (pinned below and re-read from the hash-checked gate by check.py);
below the cap it is the same admitted tier-(ii) |tau|-form (increasing in
|tau|, so never above the gate value). The AV1 zero-selected D, the AX1
reverse R-refinement, the AX1 target 4/10^7 and tier (i) are never used.

Arithmetic routines (alternating exponential bracket with halving/squaring,
Machin pi, integer square roots, atanh logarithm) follow the snapshotted
research/round32/forward/av2/calculator.py with the same outward-rounding
denominator 10^40. No binary floating value enters any returned number or
Boolean. Every returned number is an exact rational string.
"""
from fractions import Fraction as Q
from math import isqrt
import re

DEN = 10 ** 40
CAP = Q(1, 10 ** 8)
FIXED = {'abs_tau': Q(1, 10 ** 8), 's': Q(1), 'target': Q(1, 10 ** 6)}
STATE_TIER = 'ax1_forward_tier_ii'
WINDOW = 'C2'
MODEL = 'uniform_KS_routeB'
UNIFORM_SELECTED = 'tau/24'
# Admitted uniform state bound (AX1 gate decision, forward tier ii, tau=+-10^-8).
AX1_GATE_D_PRIME = Q(2425369125199104794263242601250, 167893028420061547330293754713793182097)
# Route-B incidence on the cover R={0,e_z} (AX1 gate item 4), normalized delta=alpha/8 norms per |tau|.
STARS_MEETING_R, STAR_NORM = 7, 7
SINGLE_GROUPS_MEETING_R, SINGLE_NORM = 2, 1
B_N_OVER_TAU_G_UNITS = Q(STARS_MEETING_R * STAR_NORM + SINGLE_GROUPS_MEETING_R * SINGLE_NORM, 8)   # 51/8
K_PRIME_OVER_TAU = 2 * B_N_OVER_TAU_G_UNITS                                                          # 51/4
LABEL_STEM = 'uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling'
UNIFORM_WILSON_SCOPE = ('uniform_wilson_claim:true means only that the model is the uniform fixed-spacing '
                        'Kogut-Susskind SU(2) model at strong bare coupling as labelled; no uniform Wilson-mean sign certificate')


class CalculatorError(RuntimeError):
    """An internal invariant of the calculator failed."""


def require(condition, message):
    if not condition:
        raise CalculatorError(message)


def down(x):
    x = Q(x)
    return Q((x.numerator * DEN) // x.denominator, DEN)


def up(x):
    x = Q(x)
    return Q(-((-x.numerator * DEN) // x.denominator), DEN)


def textq(x):
    x = Q(x)
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def interval(lo, hi):
    require(lo <= hi, 'inverted rigorous interval')
    return {'lower': textq(lo), 'upper': textq(hi)}


# ---------------------------------------------------------------------------
# Directed transcendental enclosures (all endpoints exact rationals).
# ---------------------------------------------------------------------------
def exp_negative(x):
    """P_41(z) <= exp(-z) <= P_40(z) on [0,1/2]; halve, then square outward."""
    x = Q(x)
    require(x >= 0, 'negative decay argument')
    halvings = 0
    while x > Q(1, 2):
        x /= 2
        halvings += 1
    total = Q(1)
    term = Q(1)
    even = None
    for k in range(1, 42):
        term *= (-x) / k
        total += term
        if k == 40:
            even = total
    lo, hi = down(total), up(even)
    require(0 <= lo <= hi <= 1, 'invalid alternating exponential bracket')
    for _ in range(halvings):
        lo, hi = down(lo * lo), up(hi * hi)
    return lo, hi


def exp_positive(x):
    """exp(+x) for x>=0 as the reciprocal of the exp(-x) bracket."""
    lo, hi = exp_negative(x)
    require(lo > 0, 'exponential underflow in bracket')
    return down(1 / hi), up(1 / lo)


def log_small(y):
    """For 1<=y<=2: log y = 2 sum z^(2k+1)/(2k+1), z=(y-1)/(y+1); geometric tail."""
    y = Q(y)
    require(1 <= y <= 2, 'log_small domain')
    z = (y - 1) / (y + 1)
    terms = 64
    partial = 2 * sum((z ** (2 * k + 1) / Q(2 * k + 1) for k in range(terms)), Q(0))
    tail = 2 * z ** (2 * terms + 1) / (Q(2 * terms + 1) * (1 - z * z))
    return down(partial), up(partial + tail)


def log_positive(y):
    y = Q(y)
    require(y >= 1, 'log domain')
    shifts = 0
    while y > 2:
        y /= 2
        shifts += 1
    lo, hi = log_small(y)
    l2, u2 = log_small(Q(2))
    return down(lo + shifts * l2), up(hi + shifts * u2)


def atan_interval(z):
    """Consecutive alternating partial sums of arctan on [0,1/5]."""
    z = Q(z)
    require(0 <= z <= Q(1, 5), 'atan domain')
    total = Q(0)
    lower = upper = None
    for k in range(80):
        total += (-1 if k % 2 else 1) * z ** (2 * k + 1) / Q(2 * k + 1)
        if k == 78:
            upper = total
        if k == 79:
            lower = total
    return down(lower), up(upper)


def pi_interval():
    """Machin: pi = 16 atan(1/5) - 4 atan(1/239), directed outward."""
    a, b = atan_interval(Q(1, 5))
    c, d = atan_interval(Q(1, 239))
    lo, hi = down(16 * a - 4 * d), up(16 * b - 4 * c)
    require(Q(333, 106) < lo <= hi < Q(355, 113), 'Machin pi bracket out of range')
    return lo, hi


def sqrt_interval(x):
    x = Q(x)
    require(x >= 0, 'sqrt domain')
    k = isqrt((x.numerator * DEN * DEN) // x.denominator)
    lo = Q(k, DEN)
    hi = lo if lo * lo == x else Q(k + 1, DEN)
    require(lo * lo <= x <= hi * hi, 'sqrt bracket failed')
    return lo, hi


# ---------------------------------------------------------------------------
# Exact input contract.
# ---------------------------------------------------------------------------
def exact(value, name):
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError(name + ': exact rational input required; bool/float rejected')
    if isinstance(value, Q):
        return value
    if isinstance(value, int):
        return Q(value)
    if not isinstance(value, str) or not re.fullmatch(r'[+-]?(?:[0-9]+/[0-9]+|[0-9]+(?:\.[0-9]*)?|\.[0-9]+)', value):
        raise ValueError(name + ': expected integer, exact decimal or numerator/denominator text')
    try:
        return Q(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(name + ': invalid rational') from error


def uniform_selected_triple(selected, tau):
    """The uniform model ties every selected face to nu=alpha*tau/24: entries 'tau/24' or the rational tau/24."""
    if not isinstance(selected, (tuple, list)) or len(selected) != 3:
        raise ValueError('selected must contain exactly three coefficients')
    out = []
    for x in selected:
        if isinstance(x, str) and x == UNIFORM_SELECTED:
            out.append(tau / 24)
            continue
        value = exact(x, 'selected')
        if value != tau / 24:
            raise ValueError('uniform model requires the selected triple (tau/24,tau/24,tau/24); '
                             'a zero or non-uniform triple is a different model (AV2 or patterned family)')
        out.append(value)
    return tuple(out)


# ---------------------------------------------------------------------------
# Admitted premises and the frozen window.
# ---------------------------------------------------------------------------
def ax1_tier_ii_D_prime(abs_tau):
    """AX1 forward tier (ii), admitted in research/round32/advisor/ax1-gate.json.

    J'=29|tau| (four stars of 7|tau| plus one single-factor group of |tau| per
    site), t_1'=52|tau|/144 (52 first-order faces per factor), self-consistent
    T'=t_1'/(1-352J'), eps=2T'+T'^2 (pair term included) and the explicit
    reduced-density inequality D'=2eps(1+eps)/(1+eps^2). Pinned: at |tau|=10^-8
    the value must equal the gate rational exactly (so a dropped pair term or a
    replaced density form cannot run silently); increasing in |tau|, so it
    never exceeds the gate value on the domain.
    """
    abs_tau = Q(abs_tau)
    require(0 <= abs_tau <= CAP, 'AX1 tier (ii) is admitted only for |tau|<=10^-8')
    J = 29 * abs_tau
    require(352 * J < 1, 'self-consistent remainder requires 352J\'<1')
    t1 = Q(52, 144) * abs_tau
    T = t1 / (1 - 352 * J)
    eps = 2 * T + T * T
    D = 2 * eps * (1 + eps) / (1 + eps * eps)
    if abs_tau == CAP:
        require(D == AX1_GATE_D_PRIME, 'tier-(ii) formula differs from the AX1 gate rational at the cap')
    require(D <= AX1_GATE_D_PRIME, 'state bound exceeds the gate value on the proved domain')
    return D


def window_multiplier(x, s, kind=WINDOW):
    """g(x)=P(x) exp(-s|x|). P=1 for x>=0 (the heat function on the support).

    C2 (frozen, AV2): P=1+2s|x|+2s^2x^2 for x<0. Any other kernel is rejected.
    """
    x, s = Q(x), Q(s)
    if kind != 'C2':
        raise ValueError('unknown or unadmitted window ' + repr(kind))
    if x >= 0:
        return Q(1)
    y = -x
    return 1 + 2 * s * y + 2 * s * s * y * y


def window_constants(s, pi_lo, pi_hi):
    """M_0=||ghat||_1=2, M_1=int|theta||ghat|=4s/pi, M_2=int theta^2|ghat|=2s^2 (AV2 gate)."""
    s = Q(s)
    return {'M0': Q(2), 'M1_lower': 4 * s / pi_hi, 'M1_upper': 4 * s / pi_lo, 'M2': 2 * s * s}


def coupling_label(tau):
    abs_tau = abs(tau)
    if abs_tau == 0:
        return LABEL_STEM + ' limit tau=0 (g^4 infinite; free Casimir model)', None
    g4 = 96 / abs_tau
    g4_text = textq(g4)
    if g4 == Q(96 * 10 ** 8):
        g4_text = '9.6x10^9'
    return LABEL_STEM + ' (g^4=' + g4_text + ')', g4


def certify(*, tau='1/100000000', s='1', target='1/1000000', selected=(UNIFORM_SELECTED,) * 3,
            alpha='1', hbar='1', E_star='1', lattice_spacing='1',
            state_tier=STATE_TIER, window=WINDOW, model=MODEL, fixed_design=False):
    """Enclose the actual centered AQ C_tau(s) of the uniform route-B model.

    Domain: uniform selected triple, |tau|<=1e-8, s, target and physical scales
    positive. D' is not an input. `fixed_design=True` enforces |tau|=10^-8,
    s=1, target=10^-6 (the negative sign is the U_E mirror replay). A valid
    domain may return target_met=False: an honest certificate that misses the
    target, not a lower bound.
    """
    if type(fixed_design) is not bool:
        raise ValueError('fixed_design must be a Boolean')
    if model != MODEL:
        raise ValueError('model ' + repr(model) + ' is outside this calculator; only the uniform route-B model (AX1) is proved here')
    if state_tier != STATE_TIER:
        raise ValueError('unadmitted state tier ' + repr(state_tier) + '; only the AX1 forward tier (ii) bound by the AX1 gate is used')
    if window != WINDOW:
        raise ValueError('kernel switch rejected: only the frozen AV2 C^2 window certifies')
    data = {name: exact(value, name) for name, value in {
        'tau': tau, 's': s, 'target': target, 'alpha': alpha, 'hbar': hbar,
        'E_star': E_star, 'lattice_spacing': lattice_spacing}.items()}
    if abs(data['tau']) > CAP:
        raise ValueError('coupling exceeds admitted uniform cap |tau|<=10^-8 (g^4>=9.6x10^9)')
    triple = uniform_selected_triple(selected, data['tau'])
    if any(data[name] <= 0 for name in ('s', 'target', 'alpha', 'hbar', 'E_star', 'lattice_spacing')):
        raise ValueError('time, target and physical scales must be positive')
    if fixed_design and (abs(data['tau']) != FIXED['abs_tau'] or data['s'] != FIXED['s'] or data['target'] != FIXED['target']):
        raise ValueError('changed AX2 fixed design; use reusable mode with explicit scope')
    abs_tau = abs(data['tau'])
    clock = data['s']
    D = ax1_tier_ii_D_prime(abs_tau)
    k = K_PRIME_OVER_TAU * abs_tau
    pi_lo, pi_hi = pi_interval()
    M = window_constants(clock, pi_lo, pi_hi)
    costs = {'state': M['M0'] * D,
             'mean_square': M['M0'] * D * D,
             'kernel_dynamics': k * M['M1_upper']}
    free_lo, free_hi = exp_negative(3 * clock)
    free_lo, free_hi = free_lo / 4, free_hi / 4
    datum = (free_lo + free_hi) / 2
    arithmetic = (free_hi - free_lo) / 2
    analytic = costs['state'] + costs['mean_square'] + costs['kernel_dynamics']
    radius = analytic + arithmetic
    lo, hi = datum - radius, datum + radius
    free_included = lo <= free_lo and free_hi <= hi
    require(free_included, 'the certified interval must retain the exact free reference')
    require(hi - lo == 2 * radius, 'width and radius mismatch')
    target_met = radius <= data['target']
    label, g4 = coupling_label(data['tau'])
    return {
        'model': MODEL,
        'label': label,
        'g4_real_image': textq(g4) if g4 is not None else 'infinite',
        'parameters': {name: textq(value) for name, value in data.items()},
        'selected_coefficients_over_alpha': [textq(x) for x in triple],
        'selected_rule': 'uniform: every selected face nu=alpha*tau/24 (tied to tau)',
        'fixed_design': fixed_design,
        'mirrored_coupling_replay': data['tau'] < 0,
        'mirror_note': ('tau<0 has no real g; it is the U_E image of +|tau| (AX1 flip identity); '
                        'a replay of the same |tau| formula, not a second confirmation') if data['tau'] < 0 else '',
        'nonzero_interacting_coupling': bool(abs_tau),
        'state_tier': STATE_TIER,
        'state_bound_D_prime': textq(D), 'mean_square_bound_D_prime_squared': textq(D * D),
        'state_bound_equals_ax1_gate_value': D == AX1_GATE_D_PRIME,
        'duhamel_slope_k_prime': textq(k),
        'incidence': {'stars_meeting_R': str(STARS_MEETING_R), 'single_factor_groups_meeting_R': str(SINGLE_GROUPS_MEETING_R),
                      'B_N_over_abs_tau_G_units': textq(B_N_OVER_TAU_G_UNITS), 'k_prime_over_abs_tau': textq(K_PRIME_OVER_TAU)},
        'window': {'id': 'C2_frozen_AV2', 'M0': textq(M['M0']), 'M1_lower': textq(M['M1_lower']),
                   'M1_upper': textq(M['M1_upper']), 'M2': textq(M['M2']),
                   'definition': 'g(x)=e^{-sx} (x>=0); g(x)=e^{sx}(1-2sx+2s^2x^2) (x<0)'},
        'pi_interval': interval(pi_lo, pi_hi),
        'costs': {**{name: textq(value) for name, value in costs.items()}, 'arithmetic': textq(arithmetic)},
        'analytic_radius': textq(analytic),
        'certified_datum': textq(datum), 'certified_absolute_error': textq(radius),
        'certified_absolute_error_outward_1e-40': textq(up(radius)),
        'actual_C_interval': interval(lo, hi), 'interval_width': textq(hi - lo),
        'free_C_interval': interval(free_lo, free_hi), 'free_reference_included': free_included,
        'reference': 'Haar P_R with the free Casimir generator on R (route B): C_0(s)=e^{-3s}/4, unchanged from AV2',
        'sub_label': 'reference_unresolved', 'resolved_interaction_shift': False,
        'target_met': target_met,
        'physical_Euclidean_time': textq(data['hbar'] * clock / data['alpha']),
        'alpha_over_E_star': textq(data['alpha'] / data['E_star']),
        'energy_clock': 's=alpha*t_E/hbar, theta=alpha*t/hbar; free Wilson energy 3 in G=H/alpha units (24 in delta=alpha/8 units)',
        'uniform_wilson_claim': True, 'uniform_wilson_claim_scope': UNIFORM_WILSON_SCOPE,
        'continuum_claim': False, 'weak_coupling_claim': False, 'grid_claim': False,
        'state_uniqueness_claim': False, 'wilson_mean_sign_certified': False, 'k2_uniform_claimed': False,
        'scientific_priority_verified': False,
        'scope': ('analytic window-kernel enclosure of the actual AQ scalar of the uniform route-B model at fixed spacing; '
                  'not a finite-box solver observation, a grid, or a detected interaction shift'),
    }
