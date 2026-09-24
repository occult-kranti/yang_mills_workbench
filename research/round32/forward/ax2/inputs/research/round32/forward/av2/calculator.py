#!/usr/bin/env python3
"""Exact-rational AV2 window-kernel calculator (forward producer).

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

Encloses the actual centered Euclidean Wilson correlation C_tau(s) of the
chosen AQ subsequential state in the zero-selected patterned family, using the
frozen C^2 window g(x)=e^{-sx} (x>=0), g(x)=e^{sx}(1-2sx+2s^2x^2) (x<0):

    |C_tau(s)-e^{-3s}/4| <= M_0(D+D^2)+k M_1,  M_0=2, M_1=4s/pi, k=49|tau|/4.

Only the proved domain is accepted: selected triple exactly zero, rational
|tau|<=10^-8, s>0 and positive physical scales. The state bound D cannot be
supplied: it is computed from the admitted AV1 forward tier-(ii) formula. The
C^1 window is available only as a labelled preview and never certifies.

Arithmetic routines (alternating exponential bracket with halving/squaring,
Machin pi, integer square roots, atanh logarithm) follow the snapshotted
research/round31/forward/at5/calculator.py; the outward rounding denominator is
10^40 here. No binary floating value enters any returned number or Boolean.
"""
from fractions import Fraction as Q
from math import isqrt
import re

DEN = 10 ** 40
CAP = Q(1, 10 ** 8)
FIXED = {'abs_tau': Q(1, 10 ** 8), 's': Q(1), 'target': Q(1, 10 ** 6)}
STATE_TIER = 'av1_forward_tier_ii'
WINDOW = 'C2'


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


# ---------------------------------------------------------------------------
# Admitted premises and the frozen window.
# ---------------------------------------------------------------------------
def av1_tier_ii_D(abs_tau):
    """AV1 forward tier (ii), admitted in research/round32/advisor/av1-gate.json.

    J=28|tau| (four incident stars per site, 7|tau| each), t_1=49|tau|/144
    (triangle bound of the exact first-order anchored norm), self-consistent
    T=t_1/(1-352J), eps=2T+T^2 (two-creation term included), and the explicit
    reduced-density inequality D=2eps(1+eps)/(1+eps^2). Increasing in |tau|.
    """
    abs_tau = Q(abs_tau)
    require(0 <= abs_tau <= CAP, 'AV1 tier (ii) is admitted only for |tau|<=10^-8')
    J = 28 * abs_tau
    require(352 * J < 1, 'self-consistent remainder requires 352J<1')
    t1 = Q(49, 144) * abs_tau
    T = t1 / (1 - 352 * J)
    eps = 2 * T + T * T
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def window_multiplier(x, s, kind=WINDOW):
    """g(x)=P(x) exp(-s|x|). P=1 for x>=0 (the heat function on the support).

    C2 (frozen): P=1+2s|x|+2s^2x^2 for x<0.  C1 (preview only): P=1+2s|x|.
    """
    x, s = Q(x), Q(s)
    if x >= 0:
        return Q(1)
    y = -x
    if kind == 'C2':
        return 1 + 2 * s * y + 2 * s * s * y * y
    if kind == 'C1':
        return 1 + 2 * s * y
    raise ValueError('unknown window ' + repr(kind))


def window_constants(s, pi_lo, pi_hi):
    """M_0=||ghat||_1=2, M_1=int|theta||ghat|=4s/pi, M_2=int theta^2|ghat|=2s^2."""
    s = Q(s)
    return {'M0': Q(2), 'M1_lower': 4 * s / pi_hi, 'M1_upper': 4 * s / pi_lo, 'M2': 2 * s * s}


def certify(*, tau='1/100000000', s='1', target='1/1000000', selected=('0', '0', '0'),
            alpha='1', hbar='1', E_star='1', lattice_spacing='1',
            state_tier=STATE_TIER, window=WINDOW, fixed_design=False):
    """Enclose the actual centered AQ C_tau(s), not an arbitrary supplied observation.

    Domain: zero selected triple, |tau|<=1e-8, s, target and physical scales
    positive. D is computed from the admitted AV1 tier-(ii) formula; it is not
    an input. `fixed_design=True` enforces |tau|=10^-8, s=1, target=10^-6 (the
    negative sign is the mirrored-coupling replay). A valid domain may return
    target_met=False: an honest insufficient certificate, not a lower bound.
    """
    if type(fixed_design) is not bool:
        raise ValueError('fixed_design must be a Boolean')
    if state_tier != STATE_TIER:
        raise ValueError('unadmitted state tier ' + repr(state_tier) + '; only the AV1 forward tier (ii) is bound by the AV2 contract')
    if window != WINDOW:
        raise ValueError('kernel switch rejected: the frozen C^2 window certifies; the C^1 window is preview-only (c1_window_preview)')
    data = {name: exact(value, name) for name, value in {
        'tau': tau, 's': s, 'target': target, 'alpha': alpha, 'hbar': hbar,
        'E_star': E_star, 'lattice_spacing': lattice_spacing}.items()}
    if not isinstance(selected, (tuple, list)) or len(selected) != 3:
        raise ValueError('selected must contain exactly three coefficients')
    triple = tuple(exact(x, 'selected') for x in selected)
    if any(triple):
        raise ValueError('proved calculator domain requires selected triple zero (Haar reference)')
    if abs(data['tau']) > CAP:
        raise ValueError('coupling exceeds admitted AQ/AV1 cap |tau|<=10^-8')
    if any(data[name] <= 0 for name in ('s', 'target', 'alpha', 'hbar', 'E_star', 'lattice_spacing')):
        raise ValueError('time, target and physical scales must be positive')
    if fixed_design and (abs(data['tau']) != FIXED['abs_tau'] or data['s'] != FIXED['s'] or data['target'] != FIXED['target']):
        raise ValueError('changed AV2 fixed design; use reusable mode with explicit scope')
    abs_tau = abs(data['tau'])
    clock = data['s']
    D = av1_tier_ii_D(abs_tau)
    k = Q(49, 4) * abs_tau
    pi_lo, pi_hi = pi_interval()
    M = window_constants(clock, pi_lo, pi_hi)
    # No zero-coupling branch: at tau=0, D=k=0 and only the arithmetic term remains.
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
    return {
        'model': 'actual centered zero-selected patterned full-Z3 AQ Wilson; chosen subsequential state at the specified tau',
        'parameters': {name: textq(value) for name, value in data.items()},
        'selected_coefficients_over_alpha': [textq(x) for x in triple],
        'fixed_design': fixed_design,
        'mirrored_coupling_replay': data['tau'] < 0,
        'nonzero_interacting_coupling': bool(abs_tau),
        'zero_coupling_branch_used': False,
        'state_tier': STATE_TIER,
        'state_bound_D': textq(D), 'mean_square_bound_D2': textq(D * D),
        'duhamel_slope_k': textq(k),
        'window': {'id': 'C2_frozen', 'M0': textq(M['M0']), 'M1_lower': textq(M['M1_lower']),
                   'M1_upper': textq(M['M1_upper']), 'M2': textq(M['M2']),
                   'definition': 'g(x)=e^{-sx} (x>=0); g(x)=e^{sx}(1-2sx+2s^2x^2) (x<0)'},
        'pi_interval': interval(pi_lo, pi_hi),
        'costs': {**{name: textq(value) for name, value in costs.items()}, 'arithmetic': textq(arithmetic)},
        'analytic_radius': textq(analytic),
        'certified_datum': textq(datum), 'certified_absolute_error': textq(radius),
        'actual_C_interval': interval(lo, hi), 'interval_width': textq(hi - lo),
        'free_C_interval': interval(free_lo, free_hi), 'free_reference_included': free_included,
        'sub_label': 'reference_unresolved', 'resolved_interaction_shift': False,
        'target_met': target_met,
        'physical_Euclidean_time': textq(data['hbar'] * clock / data['alpha']),
        'alpha_over_E_star': textq(data['alpha'] / data['E_star']),
        'energy_clock': 's=alpha*t_E/hbar, theta=alpha*t/hbar; free Wilson energy 3 in G=H/alpha units (24 in delta=alpha/8 units)',
        'uniform_wilson_claim': False, 'continuum_claim': False, 'grid_claim': False,
        'state_uniqueness_claim': False, 'scientific_priority_verified': False,
        'scope': 'analytic window-kernel enclosure of the actual AQ scalar; not a finite-box solver observation, a grid, or a detected interaction shift',
    }


def c1_window_preview(*, tau='1/100000000', s='1'):
    """Labelled preview of the C^1 window g=e^{sx}(1-2sx) (x<0). Never certifies.

    ghat=2s^2/(pi(s-i theta)^2(s+i theta)), |ghat|=(2s^2/pi)(s^2+theta^2)^{-3/2},
    M_0=4/pi, M_1=4s/pi, M_2 infinite (so no second-order refinement is possible).
    """
    abs_tau = abs(exact(tau, 'tau'))
    clock = exact(s, 's')
    if abs_tau > CAP or clock <= 0:
        raise ValueError('preview domain: |tau|<=10^-8, s>0')
    D = av1_tier_ii_D(abs_tau)
    k = Q(49, 4) * abs_tau
    pi_lo, pi_hi = pi_interval()
    radius_upper = 4 * (D + D * D) / pi_lo + k * 4 * clock / pi_lo
    return {
        'preview_only': True, 'used_for_certificate': False,
        'window': 'C1: g(x)=e^{-sx} (x>=0); g(x)=e^{sx}(1-2sx) (x<0)',
        'M0': '4/pi', 'M0_interval': interval(4 / pi_hi, 4 / pi_lo),
        'M1': '4s/pi', 'M1_interval': interval(4 * clock / pi_hi, 4 * clock / pi_lo),
        'M2': 'infinite',
        'negative_atom_multiplier_at_minus_one': textq(window_multiplier(-1, clock, 'C1')),
        'sign_mutation_multiplier_at_minus_three': textq(window_multiplier(-3, clock, 'C1')),
        'preview_radius_upper': textq(radius_upper),
        'reason_not_used': 'registered before production as a preview control; switching kernels after D is known is rejected',
    }
