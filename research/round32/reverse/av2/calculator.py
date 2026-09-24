#!/usr/bin/env python3
"""HNM-AV2 reverse calculator: exact C^2 window-kernel enclosure of the centered
original xz Wilson Euclidean correlation C_tau(s) in the zero-selected AQ subfamily.

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production.

Admitted formula (research/round32/reverse/av2/report.md, HNM-AV2-R17):

    |C_tau(s) - e^{-3s}/4| <= M_0 (D + D^2) + k M_1,
    M_0 = ||ghat||_1 = 2,  M_1 = int |theta| |ghat| = 4s/pi,  k = 49|tau|/4,

with D the AV1 tier-(ii) forward state bound evaluated from its admitted formula
(t_1 = 49|tau|/144, J = 28|tau|, T = t_1/(1-352 J), eps = 2T+T^2,
D = 2 eps (1+eps)/(1+eps^2)); at |tau| = 10^-8 it equals the gate-bound rational.
The constants M_0, M_1 are hard-coded here; check.py re-derives them by residues
and compares every emitted cost with the derived constants.

Domain: selected triple exactly zero, rational |tau| <= 10^-8, rational s > 0,
positive rational physical scales and target, state tier 'ii_forward' only,
kernel 'C2_window' only. Binary floats, Booleans and malformed text are rejected.
The C^1 window is available only through preview_c1_window(), which never
returns a certificate. Standard library only; exact Fraction arithmetic decides
every Boolean; decimal strings are truncated previews.
"""
from fractions import Fraction as Q
import re

DEN = 10 ** 40
TAU_CAP = Q(1, 10 ** 8)
ADMITTED_D_CAP = Q(585079838465912592144137406066050, 42981220507576537932303142777593983768257)
FIXED_DESIGN = {'tau': Q(1, 10 ** 8), 's': Q(1), 'target': Q(1, 10 ** 6)}
WINDOW_M0 = Q(2)                 # ||ghat||_1
WINDOW_M1_TIMES_PI_OVER_S = Q(4)  # int |theta||ghat| dtheta = 4 s / pi
STAR_NORM_PER_TAU = Q(7, 8)      # ||V_b|| <= 7|tau|/8 in G = H/alpha units
INCIDENT_STARS = 7               # |R - S| for R = {0, e_z}
FREE_ENERGY_ALPHA = 3            # four j=1/2 links, Casimir 3/4 each, alpha units
FREE_VARIANCE = Q(1, 4)          # Haar E[W^2]
ADMITTED_STATE_TIERS = ('ii_forward',)
CERTIFIED_KERNELS = ('C2_window',)


class DomainError(ValueError):
    """Input outside the proved calculator domain (or not exact)."""


def _require(condition, message):
    if condition is not True:
        raise DomainError(message)


def exact(value, name):
    """Exact rational input: int, Fraction, exact decimal text or p/q text."""
    if isinstance(value, bool) or isinstance(value, float):
        raise DomainError(name + ': exact rational input required; bool/float rejected')
    if isinstance(value, Q):
        return value
    if isinstance(value, int):
        return Q(value)
    if not isinstance(value, str) or not re.fullmatch(
            r'[+-]?(?:[0-9]+/[1-9][0-9]*|[0-9]+(?:\.[0-9]+)?|\.[0-9]+)', value):
        raise DomainError(name + ': expected integer, exact decimal or numerator/denominator text')
    return Q(value)


def textq(x):
    x = Q(x)
    return str(x.numerator) if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)


def down(x):
    x = Q(x)
    return Q((x.numerator * DEN) // x.denominator, DEN)


def up(x):
    x = Q(x)
    return Q(-((-x.numerator * DEN) // x.denominator), DEN)


def _factorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


def exp_positive_interval(z, terms=34):
    """Directed enclosure of e^z for rational z >= 0.

    Halve z into [0,1/2]; there the Taylor partial sum S_N is a lower bound and
    S_N + z^(N+1)/(N+1)! / (1 - z/(N+2)) an upper bound (geometric majorant of the
    positive tail). Round outward and square back with outward rounding.
    """
    z = Q(z)
    _require(z >= 0, 'exp_positive_interval needs z >= 0')
    halvings = 0
    while z > Q(1, 2):
        z /= 2
        halvings += 1
    partial, power = Q(0), Q(1)
    for k in range(terms + 1):
        partial += power / _factorial(k)
        power *= z
    tail = power / _factorial(terms + 1) / (1 - z / (terms + 2))
    lo, hi = down(partial), up(partial + tail)
    for _ in range(halvings):
        lo, hi = down(lo * lo), up(hi * hi)
    return lo, hi


def exp_negative_interval(z):
    """Directed enclosure of e^{-z} for rational z >= 0 (reciprocal of e^z)."""
    lo, hi = exp_positive_interval(z)
    return down(1 / hi), up(1 / lo)


def _atan_inverse(n, terms=60):
    """Alternating series of atan(1/n): consecutive partial sums bracket it."""
    s, prev = Q(0), Q(0)
    for k in range(terms + 1):
        prev = s
        s += Q((-1) ** k, (2 * k + 1) * n ** (2 * k + 1))
    return min(prev, s), max(prev, s)


def pi_interval():
    """Machin: pi = 16 atan(1/5) - 4 atan(1/239), directed."""
    a_lo, a_hi = _atan_inverse(5)
    b_lo, b_hi = _atan_inverse(239)
    return down(16 * a_lo - 4 * b_hi), up(16 * a_hi - 4 * b_lo)


def av1_tier_ii_forward(abs_tau):
    """AV1 forward tier-(ii) state bound D(|tau|) (exact rational)."""
    abs_tau = Q(abs_tau)
    _require(0 <= abs_tau <= TAU_CAP, 'AV1 tier-(ii) formula is admitted only for |tau| <= 10^-8')
    t1 = Q(49, 144) * abs_tau
    J = 28 * abs_tau
    _require(352 * J < 1, 'self-consistent remainder needs 352 J < 1')
    T = t1 / (1 - 352 * J)
    eps = 2 * T + T * T
    D = 2 * eps * (1 + eps) / (1 + eps * eps)
    return {'t1': t1, 'J': J, 'T': T, 'eps': eps, 'D': D}


def _check_admitted_constant():
    D = av1_tier_ii_forward(TAU_CAP)['D']
    _require(D == ADMITTED_D_CAP, 'AV1 tier-(ii) formula does not reproduce the gate-bound value')
    return D


def sci(x, digits=10):
    """Truncated decimal preview computed with integers (never used to decide)."""
    x = Q(x)
    if x == 0:
        return '0'
    sign = '-' if x < 0 else ''
    x = abs(x)
    e = len(str(x.numerator)) - len(str(x.denominator))
    while Q(10) ** e > x:
        e -= 1
    while Q(10) ** (e + 1) <= x:
        e += 1
    scaled = x / Q(10) ** e * 10 ** (digits - 1)
    mant = str(scaled.numerator // scaled.denominator)
    return sign + mant[0] + '.' + mant[1:] + 'e' + str(e)


def certify(*, tau='1/100000000', s='1', target='1/1000000', selected=('0', '0', '0'),
            alpha='1', hbar='1', E_star='1', lattice_spacing='1',
            state_tier='ii_forward', kernel='C2_window', fixed_design=False):
    """Enclose the actual centered AQ C_tau(s) with the frozen C^2 window.

    Returns exact rational strings: datum (midpoint of the directed e^{-3s}/4
    enclosure), itemized costs (state, mean_square, kernel_dynamics, arithmetic),
    radius and interval. A valid domain can return target_met False.
    """
    if type(fixed_design) is not bool:
        raise DomainError('fixed_design must be a Boolean')
    if state_tier not in ADMITTED_STATE_TIERS:
        raise DomainError('state tier %r is not the AV1-admitted tier (ii) forward bound' % (state_tier,))
    if kernel not in CERTIFIED_KERNELS:
        if kernel == 'C1_window':
            raise DomainError('C^1 window is preview-only; a kernel switch after D is known is rejected')
        raise DomainError('kernel %r is not the frozen C^2 window' % (kernel,))
    data = {name: exact(value, name) for name, value in (
        ('tau', tau), ('s', s), ('target', target), ('alpha', alpha), ('hbar', hbar),
        ('E_star', E_star), ('lattice_spacing', lattice_spacing))}
    if not isinstance(selected, (tuple, list)) or len(selected) != 3:
        raise DomainError('selected must contain exactly three coefficients')
    sel = tuple(exact(x, 'selected') for x in selected)
    if any(x != 0 for x in sel):
        raise DomainError('proved domain requires the selected triple to be exactly zero')
    if abs(data['tau']) > TAU_CAP:
        raise DomainError('coupling exceeds the admitted cap |tau| <= 10^-8')
    for name in ('s', 'target', 'alpha', 'hbar', 'E_star', 'lattice_spacing'):
        if data[name] <= 0:
            raise DomainError(name + ' must be strictly positive')
    if fixed_design and any(data[k] != v for k, v in FIXED_DESIGN.items()):
        raise DomainError('changed AV2 fixed design (tau=+10^-8, s=1, target=10^-6)')
    _check_admitted_constant()
    abs_tau, clock = abs(data['tau']), data['s']
    state = av1_tier_ii_forward(abs_tau)
    D = state['D']
    k = 2 * INCIDENT_STARS * STAR_NORM_PER_TAU * abs_tau
    pi_lo, pi_hi = pi_interval()
    costs = {
        'state': WINDOW_M0 * D,
        'mean_square': WINDOW_M0 * D * D,
        'kernel_dynamics': up(k * WINDOW_M1_TIMES_PI_OVER_S * clock / pi_lo),
    }
    e_lo, e_hi = exp_negative_interval(FREE_ENERGY_ALPHA * clock)
    free_lo, free_hi = FREE_VARIANCE * e_lo, FREE_VARIANCE * e_hi
    datum = (free_lo + free_hi) / 2
    costs['arithmetic'] = (free_hi - free_lo) / 2
    radius = sum(costs.values(), Q(0))
    lo, hi = datum - radius, datum + radius
    free_included = lo <= free_lo and free_hi <= hi
    _require(free_included, 'enclosure must retain the free reference (reference_unresolved)')
    _require(hi - lo == 2 * radius, 'width and radius mismatch')
    target_met = radius <= data['target']
    return {
        'model': 'actual centered zero-selected patterned full-Z3 AQ Wilson; every AQ1 subsequential state at the given tau',
        'kernel': 'C2_window g(x)=e^{-sx} (x>=0), e^{sx}(1-2sx+2s^2x^2) (x<0)',
        'parameters': {name: textq(value) for name, value in sorted(data.items())},
        'selected_coefficients_over_alpha': [textq(x) for x in sel],
        'fixed_design': fixed_design,
        'state_tier': state_tier,
        'state_bound_D': textq(D),
        'state_bound_preview': sci(D),
        'duhamel_slope_k': textq(k),
        'window_constants': {'M0': textq(WINDOW_M0), 'M1': '%s*s/pi' % textq(WINDOW_M1_TIMES_PI_OVER_S)},
        'pi_enclosure': [textq(pi_lo), textq(pi_hi)],
        'costs': {name: textq(value) for name, value in sorted(costs.items())},
        'certified_datum': textq(datum),
        'certified_radius': textq(radius),
        'radius_preview': sci(radius),
        'actual_C_interval': {'lower': textq(lo), 'upper': textq(hi)},
        'free_C_interval': {'lower': textq(free_lo), 'upper': textq(free_hi)},
        'interval_width': textq(hi - lo),
        'target_met': target_met,
        'euclidean_node_certified': target_met,
        'free_reference_included': free_included,
        'sub_label': 'reference_unresolved',
        'resolved_interaction_shift': False,
        'physical_Euclidean_time': textq(data['hbar'] * clock / data['alpha']),
        'alpha_over_E_star': textq(data['alpha'] / data['E_star']),
        'energy_clock': 's=alpha*t_E/hbar; free Wilson energy 3 alpha',
        'continuum_claim': False, 'uniform_wilson_claim': False, 'grid_claim': False,
        'scientific_priority_verified': False, 'state_uniqueness_claim': False,
        'scope': 'analytic model enclosure for the frozen C^2 window; not a finite-box solver observation or a detected interaction shift',
    }


def preview_c1_window(*, tau='1/100000000', s='1'):
    """Labelled preview of the C^1 window g=e^{sx}(1-2sx) (x<0); never a certificate.

    Its |ghat| = (2s^2/pi)(s^2+theta^2)^(-3/2) is not rational, so the residue route
    of this producer does not apply; the substitution values are M_0 = 4/pi,
    M_1 = 4s/pi and M_2 = infinity.
    """
    abs_tau, clock = abs(exact(tau, 'tau')), exact(s, 's')
    _require(abs_tau <= TAU_CAP and clock > 0, 'preview domain')
    D = av1_tier_ii_forward(abs_tau)['D']
    k = 2 * INCIDENT_STARS * STAR_NORM_PER_TAU * abs_tau
    pi_lo, _ = pi_interval()
    radius_upper = up(Q(4) * (D + D * D) / pi_lo + k * 4 * clock / pi_lo)
    return {
        'label': 'preview_only_not_a_certificate',
        'certified': False,
        'window': 'g(x)=e^{-sx} (x>=0), e^{sx}(1-2sx) (x<0)',
        'M0': '4/pi', 'M1': '4*s/pi', 'M2': 'infinity',
        'radius_preview_upper': textq(radius_upper),
        'radius_preview': sci(radius_upper),
        'rule': 'the frozen kernel is the C^2 window; a switch to the C^1 window after D is known is rejected',
    }
