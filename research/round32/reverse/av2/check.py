#!/usr/bin/env python3
"""HNM-AV2 reverse producer: residue reconstruction of the C^2 window-kernel
certificate for the centered original xz Wilson Euclidean correlation at the
original cap tau=10^-8, s=1, in the zero-selected AQ subfamily.

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production under
premise isolation; HNM labels are project aliases. Fourier inversion, residue
calculus, Duhamel's formula and trace duality are established mathematics;
scientific priority is unverified.

Standard library only. Exact Fraction and Gaussian-rational arithmetic decides
every Boolean; decimal strings are truncated previews. Every contract control is a
damaging mutation whose rejection is required; rejections and failures are
explicit exceptions (never assert), so the run and its output bytes are identical
under python -O.

Usage: python3 -B research/round32/reverse/av2/check.py --output /absolute/fresh/dir
"""
import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from fractions import Fraction as Q  # noqa: E402
from math import comb, factorial, isqrt  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUTS = HERE / 'inputs'
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import calculator as calc  # noqa: E402

CONTRACT_REL = 'research/round32/contracts/av2.json'
GATE_REL = 'research/round32/advisor/av1-gate.json'
SELECTION_REL = 'research/round32/advisor/selection-av2.md'
CONTRACT_SHA256 = '686458cab7a4e6e65b63f0c6418d51496f66f1aada4897115ff14e8bbfad5687'
DEN = 10 ** 40
FORBIDDEN_PREFIXES = (
    'research/round32/forward/av2/',
    'research/round32/skeptic/av2',
    'research/round32/experts/',
    'research/round32/advisor/deliberation-',
)
UNIVERSAL_FLAGS = ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift',
                   'scientific_priority_verified', 'grid_claim')


# ----------------------------------------------------------------- exceptions
class Rejected(Exception):
    """A validator refused its input: the required fate of a damaging mutation."""


class ProducerError(Exception):
    """An identity required by the proof failed; the run aborts without output."""


def require(condition, reason):
    if condition is not True:
        raise Rejected(reason)


def must(condition, reason):
    if condition is not True:
        raise ProducerError(reason)


CHECKS = []


def record(check_id, condition, **details):
    must(condition, 'check failed: ' + check_id)
    must(all(c['id'] != check_id for c in CHECKS), 'duplicate check id: ' + check_id)
    entry = {'id': check_id, 'passed': True}
    entry.update(details)
    CHECKS.append(entry)


def rejection(function, *args):
    """Run one damaging mutation; return its rejection reason, abort if accepted."""
    try:
        function(*args)
    except (Rejected, calc.DomainError) as exc:
        return str(exc)
    raise ProducerError('damaging mutation accepted by ' + getattr(function, '__name__', 'mutation'))


def control(check_id, mutations, **details):
    """A contract control passes only if every listed damaging mutation is rejected."""
    rejected = {}
    for label, function, args in mutations:
        rejected[label] = rejection(function, *args)
    record(check_id, len(rejected) == len(mutations) and len(mutations) > 0,
           kind='damaging_mutation_control', rejected_mutations=rejected, **details)


# ----------------------------------------------------------- exact arithmetic
def parse_q(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise Rejected('non-exact numeric input rejected: ' + repr(value))
    if isinstance(value, Q):
        return value
    if isinstance(value, int):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'[+-]?[0-9]+(/[1-9][0-9]*)?', value):
        return Q(value)
    raise Rejected('malformed rational input rejected: ' + repr(value))


def admit_bound(value, target):
    require(isinstance(value, Q) and isinstance(target, Q), 'admission requires exact rationals, not floating values')
    return value <= target


def qs(x):
    return str(Q(x))


def floor_to(x, den=DEN):
    x = Q(x)
    return Q((x.numerator * den) // x.denominator, den)


def ceil_to(x, den=DEN):
    x = Q(x)
    return Q(-((-x.numerator * den) // x.denominator), den)


def exp_minus_alternating(z):
    """Directed enclosure of e^{-z}, z >= 0 (independent of the calculator's method).

    Halve z into [0,1/2]; there the alternating Taylor terms decrease, so the
    partial sums ending at degree 43 (negative last term) and 42 bracket e^{-y}.
    Round outward and square back with outward rounding.
    """
    z = Q(z)
    must(z >= 0, 'negative decay argument')
    halvings = 0
    while z > Q(1, 2):
        z /= 2
        halvings += 1
    total, term, even, odd = Q(1), Q(1), None, None
    for k in range(1, 44):
        term = term * (-z) / k
        total += term
        if k == 42:
            even = total
        if k == 43:
            odd = total
    lo, hi = floor_to(odd), ceil_to(even)
    must(Q(0) < lo and lo <= hi and hi <= 1, 'alternating exponential bracket')
    for _ in range(halvings):
        lo, hi = floor_to(lo * lo), ceil_to(hi * hi)
    return lo, hi


def atan_recip_bounds(n, terms=70):
    s, partials = Q(0), []
    for k in range(terms):
        s += Q((-1) ** k, (2 * k + 1) * n ** (2 * k + 1))
        partials.append(s)
    return min(partials[-1], partials[-2]), max(partials[-1], partials[-2])


def pi_bounds():
    a_lo, a_hi = atan_recip_bounds(5)
    b_lo, b_hi = atan_recip_bounds(239)
    return floor_to(16 * a_lo - 4 * b_hi), ceil_to(16 * a_hi - 4 * b_lo)


def log_small(y, terms=60):
    """log y for 1 <= y <= 2: 2 sum z^(2j+1)/(2j+1), z=(y-1)/(y+1) <= 1/3, geometric tail."""
    y = Q(y)
    must(Q(1) <= y and y <= 2, 'log_small domain')
    z = (y - 1) / (y + 1)
    partial = 2 * sum((z ** (2 * j + 1) / (2 * j + 1) for j in range(terms)), Q(0))
    tail = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    return floor_to(partial), ceil_to(partial + tail)


def log_bounds(y):
    y = Q(y)
    must(y >= 1, 'log domain')
    k = max(0, (y.numerator // y.denominator).bit_length() - 1)
    r = y / 2 ** k
    while r >= 2:
        r /= 2
        k += 1
    must(Q(1) <= r and r < 2, 'log range reduction')
    lo, hi = log_small(r)
    l2_lo, l2_hi = log_small(Q(2))
    return floor_to(lo + k * l2_lo), ceil_to(hi + k * l2_hi)


def sqrt_bounds(y):
    y = Q(y)
    must(y >= 0, 'negative square-root argument')
    scaled = y.numerator * DEN * DEN
    r = isqrt(scaled // y.denominator)
    lo = Q(r, DEN)
    hi = lo if r * r * y.denominator == scaled else Q(r + 1, DEN)
    must(lo * lo <= y and y <= hi * hi, 'square-root enclosure')
    return lo, hi


def sci(x, digits=10):
    return calc.sci(x, digits)


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ------------------------------------------------ Gaussian rationals, series
class CQ:
    """Exact Gaussian rational re + i im."""
    __slots__ = ('re', 'im')

    def __init__(self, re=0, im=0):
        if isinstance(re, (bool, float)) or isinstance(im, (bool, float)):
            raise ProducerError('non-exact scalar in complex arithmetic')
        self.re = Q(re)
        self.im = Q(im)

    def __add__(self, o):
        o = cq(o)
        return CQ(self.re + o.re, self.im + o.im)

    __radd__ = __add__

    def __sub__(self, o):
        o = cq(o)
        return CQ(self.re - o.re, self.im - o.im)

    def __rsub__(self, o):
        return cq(o) - self

    def __neg__(self):
        return CQ(-self.re, -self.im)

    def __mul__(self, o):
        o = cq(o)
        return CQ(self.re * o.re - self.im * o.im, self.re * o.im + self.im * o.re)

    __rmul__ = __mul__

    def inv(self):
        n = self.re * self.re + self.im * self.im
        must(n != 0, 'division by zero in exact complex arithmetic')
        return CQ(self.re / n, -self.im / n)

    def __truediv__(self, o):
        return self * cq(o).inv()

    def __rtruediv__(self, o):
        return cq(o) * self.inv()

    def __pow__(self, n):
        must(isinstance(n, int) and n >= 0, 'nonnegative integer power')
        r = CQ(1)
        for _ in range(n):
            r = r * self
        return r

    def __eq__(self, o):
        o = cq(o)
        return self.re == o.re and self.im == o.im

    def __hash__(self):
        return hash((self.re, self.im))

    def is_zero(self):
        return self.re == 0 and self.im == 0

    def abs2(self):
        return self.re * self.re + self.im * self.im

    def text(self):
        if self.im == 0:
            return qs(self.re)
        if self.re == 0:
            return '(%s)*i' % qs(self.im)
        return '%s%s(%s)*i' % (qs(self.re), '+' if self.im > 0 else '-', qs(abs(self.im)))


def cq(v):
    if isinstance(v, CQ):
        return v
    if isinstance(v, (int, Q)) and not isinstance(v, bool):
        return CQ(v, 0)
    raise ProducerError('non-exact scalar in complex arithmetic: ' + repr(v))


IU = CQ(0, 1)


def p_trim(p):
    p = list(p)
    while p and p[-1].is_zero():
        p.pop()
    return p


def p_add(a, b):
    n = max(len(a), len(b))
    return p_trim([(a[i] if i < len(a) else CQ()) + (b[i] if i < len(b) else CQ()) for i in range(n)])


def p_mul(a, b):
    if not a or not b:
        return []
    out = [CQ() for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = out[i + j] + x * y
    return p_trim(out)


def p_scale(a, c):
    return p_trim([x * c for x in a])


def p_real(a):
    must(all(x.im == 0 for x in a), 'imaginary part survived in a real inverse transform')
    return [x.re for x in a]


def p_eval_real(coeffs, x):
    total = Q(0)
    for c in reversed(coeffs):
        total = total * x + c
    return total


def s_mul(A, B, n):
    out = [[] for _ in range(n)]
    for i in range(n):
        if not A[i]:
            continue
        for j in range(n - i):
            if B[j]:
                out[i + j] = p_add(out[i + j], p_mul(A[i], B[j]))
    return out


def inv_linear_series(A, B, m, n):
    """(A + B w)^(-m) = A^(-m) sum_k C(m+k-1,k) (-B/A)^k w^k, as series of constants."""
    require(not A.is_zero(), 'coincident poles must be merged into one factor')
    base = A.inv() ** m
    ratio = -(B / A)
    out, power = [], CQ(1)
    for k in range(n):
        out.append(p_trim([base * comb(m + k - 1, k) * power]))
        power = power * ratio
    return out


def numerator_series(num, z0, n):
    out = []
    for k in range(n):
        c = CQ(0)
        for p, coeff in enumerate(num):
            if p >= k:
                c = c + coeff * comb(p, k) * z0 ** (p - k)
        out.append(p_trim([c]))
    return out


def exp_series(z0, n):
    """e^{i theta x} at theta=z0+w, without the factor e^{i z0 x}: sum (i x)^k w^k/k! (polys in x)."""
    return [p_trim([CQ() for _ in range(k)] + [IU ** k * Q(1, factorial(k))]) for k in range(n)]


def log_series(z0, n):
    """log(z0+w) = L + sum_{k>=1} (-1)^(k+1) w^k/(k z0^k), L = log z0 a formal symbol."""
    out = [[CQ(0), CQ(1)]]
    for k in range(1, n):
        out.append(p_trim([CQ(Q((-1) ** (k + 1), k)) / (z0 ** k)]))
    return out


def mirror(kernel):
    """K(-theta): each linear factor a + b theta becomes a - b theta."""
    return {'coef': kernel['coef'], 'factors': [(a, -b, m) for a, b, m in kernel['factors']],
            'num': [c * (-1) ** p for p, c in enumerate(kernel['num'])]}


def pole_data(kernel):
    poles = []
    for j, (a, b, m) in enumerate(kernel['factors']):
        must(not b.is_zero(), 'degenerate linear factor')
        poles.append((j, -(a / b), m))
    roots = [z for _, z, _ in poles]
    must(len(set(roots)) == len(roots), 'repeated roots must be merged')
    return poles


def decay_order(kernel, extra_power=0):
    return sum(m for _, _, m in kernel['factors']) - (len(kernel['num']) - 1) - extra_power


def residue_poly(kernel, j, extra=None, numerator=None):
    """Residue at the root of factor j of num(theta)/prod(a+b theta)^m times an extra series."""
    a, b, m = kernel['factors'][j]
    z0 = -(a / b)
    n = m
    h = [p_trim([b.inv() ** m])] + [[] for _ in range(n - 1)]
    for l_idx, (al, bl, ml) in enumerate(kernel['factors']):
        if l_idx != j:
            h = s_mul(h, inv_linear_series(al + bl * z0, bl, ml, n), n)
    h = s_mul(h, numerator_series(kernel['num'] if numerator is None else numerator, z0, n), n)
    if extra is not None:
        h = s_mul(h, extra(z0, n), n)
    return z0, h[n - 1]


def poly_text(coeffs, var='x'):
    parts = []
    for p, c in enumerate(coeffs):
        c = cq(c)
        if c.is_zero():
            continue
        parts.append('(%s)%s' % (c.text(), '' if p == 0 else (var if p == 1 else '%s^%d' % (var, p))))
    return '+'.join(parts) if parts else '0'


def inverse_transform(kernel):
    """int K(theta) e^{i theta x} dtheta for K = (coef/pi) num/prod(a+b theta)^m, by residues.

    x >= 0: close in the upper half-plane (+2 pi i sum Res); x <= 0: close in the lower
    half-plane (-2 pi i sum Res). Arcs vanish because K decays like |theta|^-2 or faster.
    Returns, for each half-line, terms (rate, real polynomial) meaning e^{rate x} poly(x).
    """
    require(decay_order(kernel) >= 2, 'kernel decays slower than |theta|^-2: arcs do not vanish and K is not L^1')
    halves = {'nonneg': {}, 'neg': {}}
    residues = []
    for j, z0, m in pole_data(kernel):
        require(z0.im != 0, 'pole on the real axis: kernel not integrable')
        require(z0.re == 0, 'pole off the imaginary axis (outside this engine)')
        _, res = residue_poly(kernel, j, exp_series)
        rate = -z0.im
        if z0.im > 0:
            key, factor = 'nonneg', 2 * IU * kernel['coef']
        else:
            key, factor = 'neg', -2 * IU * kernel['coef']
        residues.append({'pole': z0.text(), 'order': m,
                         'half_plane': 'upper' if z0.im > 0 else 'lower',
                         'residue_without_coef_over_pi': 'e^{%s x}[%s]' % (qs(rate), poly_text(res))})
        halves[key][rate] = p_add(halves[key].get(rate, []), p_scale(res, factor))
    out = {'residues': residues}
    for key, terms in halves.items():
        out[key] = sorted((rate, p_real(poly)) for rate, poly in terms.items() if poly)
    return out


def describe_half(terms):
    return ' + '.join('e^{%sx}[%s]' % (qs(rate), poly_text(poly)) for rate, poly in terms) or '0'


def readout(kernel, atom, weight=Q(1)):
    """int K(theta) w e^{i theta atom} dtheta: the kernel applied to a spectral atom."""
    inv = inverse_transform(kernel)
    terms = inv['nonneg'] if atom >= 0 else inv['neg']
    value = {}
    for rate, poly in terms:
        e = rate * atom
        value[e] = value.get(e, Q(0)) + weight * p_eval_real(poly, atom)
    return sorted((e, c) for e, c in value.items() if c != 0)


def value_text(value):
    return ' + '.join('%s*e^{%s}' % (qs(c), qs(e)) for e, c in value) or '0'


def kernel_eval(kernel, theta):
    """coef * num(theta) / prod (a + b theta)^m at real rational theta (the 1/pi omitted)."""
    t = cq(theta)
    num = CQ(0)
    for p, c in enumerate(kernel['num']):
        num = num + c * t ** p
    den = CQ(1)
    for a, b, m in kernel['factors']:
        den = den * (a + b * t) ** m
    return cq(kernel['coef']) * num / den


def modulus_kernel(kernel, s):
    """|K(theta)| for real theta when every factor is s +- i theta: coef (s^2+theta^2)^(-M/2)."""
    for a, b, m in kernel['factors']:
        require(a == CQ(s) and (b == IU or b == -IU), '|K| is rational only for factors (s +- i theta)')
    require(kernel['num'] == [CQ(1)], 'numerator must be 1 for the modulus form')
    total = sum(m for _, _, m in kernel['factors'])
    require(total % 2 == 0, 'odd total order %d: |K| = coef (s^2+theta^2)^(-%d/2) is not rational; residues do not apply' % (total, total))
    half = total // 2
    return {'coef': abs(kernel['coef']), 'factors': [(-IU * s, CQ(1), half), (IU * s, CQ(1), half)], 'num': [CQ(1)]}


def full_line_even_moment(kmod, k):
    """int theta^k |K| dtheta (k even) = 2 i coef sum_{upper} Res[theta^k R]; value times pi^0."""
    require(k % 2 == 0, 'full-line residue moment needs an even power')
    require(decay_order(kmod, k) >= 2, 'moment %d diverges: |theta|^%d |K| decays like |theta|^-%d' % (k, k, decay_order(kmod, k)))
    num = [CQ(0)] * k + [CQ(1)]
    total = CQ(0)
    for j, z0, m in pole_data(kmod):
        if z0.im > 0:
            _, res = residue_poly(kmod, j, None, numerator=num)
            total = total + (res[0] if res else CQ(0))
    value = 2 * IU * kmod['coef'] * total
    must(value.im == 0, 'even moment must be real')
    return value.re


def half_line_moment_keyhole(kmod, k):
    """int_0^inf theta^k R(theta) dtheta = -sum_all Res[theta^k R log theta] (keyhole, arg in (0,2pi)).

    Requires decay |theta|^-2 or faster and no pole on [0,inf); the formal log symbol
    must cancel pole by pole (true when theta^k R is an exact derivative).
    """
    require(decay_order(kmod, k) >= 2, 'moment %d diverges: |theta|^%d |K| decays like |theta|^-%d' % (k, k, decay_order(kmod, k)))
    num = [CQ(0)] * k + [CQ(1)]
    total = CQ(0)
    per_pole = []
    for j, z0, m in pole_data(kmod):
        require(not (z0.im == 0 and z0.re >= 0), 'pole on the keyhole cut [0,inf)')
        _, res = residue_poly(kmod, j, log_series, numerator=num)
        require(len(res) <= 1, 'log terms do not cancel at pole %s' % z0.text())
        r0 = res[0] if res else CQ(0)
        per_pole.append({'pole': z0.text(), 'residue_log_free': r0.text()})
        total = total + r0
    value = -total
    must(value.im == 0, 'half-line moment must be real')
    return value.re, per_pole


# --------------------------------------------------------------- geometry
EX, EY, EZ, ORIGIN = (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)
UNIT = {'x': EX, 'y': EY, 'z': EZ}
STAR = (ORIGIN, EX, EY, EZ)
WILSON_LINKS = (((0, 0, 0), 'x'), ((1, 0, 0), 'z'), ((0, 0, 1), 'x'), ((0, 0, 0), 'z'))


def vadd(a, b):
    return tuple(p + q for p, q in zip(a, b))


def vsub(a, b):
    return tuple(p - q for p, q in zip(a, b))


def coarse(p):
    return (p[0] // 4, p[1] // 2, p[2])


def factor_links(b):
    return [((4 * b[0] + r, 2 * b[1] + q, b[2]), d) for r in range(4) for q in range(2) for d in 'xyz']


def wilson_geometry():
    owners = [coarse(t) for t, _ in WILSON_LINKS]
    cover = tuple(sorted(set(owners)))
    links = sorted({lk for b in cover for lk in factor_links(b)})
    ends = {t for t, _ in links} | {vadd(t, UNIT[d]) for t, d in links}
    incident = tuple(sorted({vsub(u, v) for u in cover for v in STAR}))
    return {'owners': owners, 'cover': cover, 'links': links, 'endpoints': ends, 'incident': incident}


GEOM = wilson_geometry()


def box_star_anchors(N):
    box = {(x, y, z) for x in range(-N, N + 1) for y in range(-N, N + 1) for z in range(-N, N + 1)}
    return sorted(b for b in box if all(vadd(b, v) in box for v in STAR))


# ------------------------------------------------------------ validators
def certify_cover(cover, link_count):
    require(tuple(cover) == GEOM['cover'], 'cover %s is not the complete cover R={0,e_z} of the original xz Wilson' % (list(cover),))
    require(link_count == len(GEOM['links']) == 48, 'the complete cover has 48 links, not %d' % link_count)
    return True


def certify_slope(k, abs_tau, anchors, combination='triangle', box_N=None):
    require(tuple(sorted(anchors)) == GEOM['incident'], 'star set %s is not the seven incident anchors R-S' % (list(anchors),))
    require(combination == 'triangle', 'incident star norms add by the triangle inequality, not in quadrature')
    require(box_N is None, 'the Duhamel slope must be local (seven incident stars), not the extensive total norm of box N=%s' % box_N)
    expected = 2 * len(anchors) * calc.STAR_NORM_PER_TAU * abs_tau
    require(k == expected, 'slope %s differs from 2*7*(7|tau|/8)=%s' % (qs(k), qs(expected)))
    return True


def certify_generator_units(free_energy, units, star_norm_per_tau):
    require(units == 'alpha', 'the clock s=alpha t_E/hbar pairs with G=H/alpha energies, not %s units' % units)
    require(free_energy == calc.FREE_ENERGY_ALPHA, 'free Wilson energy %s is not 3 in alpha units' % qs(free_energy))
    require(star_norm_per_tau == calc.STAR_NORM_PER_TAU, 'star norm %s|tau| is not 7|tau|/8 in G=H/alpha units' % qs(star_norm_per_tau))
    return True


def centering_shift(method, m, d):
    if method == 'vector':
        return d * d
    if method == 'scalar':
        return -2 * m * d - d * d
    if method == 'uncentered':
        return m * m
    raise ProducerError('unknown centering method')


def certify_centering(method):
    require(method == 'vector', 'the certified readout uses the vector-centered chi=(W-m)Omega, not %s centering' % method)
    return True


def certify_state_term(operator_kind, factor):
    if factor == Q(1, 2):
        require(operator_kind == 'effect', 'the D/2 effect refinement needs 0<=A<=I; W alpha^0_theta(W) is a complex non-effect')
    require(factor in (Q(1), Q(1, 2)), 'state factor')
    return True


def certify_radius(costs, radius, D, k, s, M0, M1_times_pi_over_s, pi_lo, arithmetic, combination='linear'):
    require(sorted(costs) == ['arithmetic', 'kernel_dynamics', 'mean_square', 'state'],
            'itemized terms must be state, mean_square, kernel_dynamics and arithmetic; got %s' % sorted(costs))
    require(M0 == 2, 'window L1 norm M_0=%s is not the residue-derived 2' % qs(M0))
    require(costs['state'] == M0 * D, 'state term %s is not M_0*D' % sci(costs['state']))
    require(costs['mean_square'] == M0 * D * D, 'mean-square term is not M_0*D^2 (m^2<=D^2 charged)')
    exact_dyn_upper = k * M1_times_pi_over_s * s / pi_lo
    require(costs['kernel_dynamics'] >= exact_dyn_upper, 'kernel-dynamics term below k*M_1 with directed pi')
    require(costs['arithmetic'] >= arithmetic, 'arithmetic term below the exponential enclosure half-width')
    require(combination == 'linear', 'worst-case bounds of one integral add linearly; root-sum-square is rejected')
    require(radius == sum(costs.values(), Q(0)), 'radius is not the sum of the itemized terms')
    return True


def certify_kernel_identity(kernel, s):
    inv = inverse_transform(kernel)
    require(inv['nonneg'] == [(-s, [Q(1)])],
            'kernel does not reproduce e^{-sx} on the nonnegative support: gives %s' % describe_half(inv['nonneg']))
    return inv


def certify_heat_readout(kernel, atom, claimed):
    require(atom >= 0, 'spectral atom at %s<0: the window identity holds only on the nonnegative support (AQ1 H>=0)' % qs(atom))
    return compare_readout(kernel, atom, claimed)


def compare_readout(kernel, atom, claimed):
    value = readout(kernel, atom)
    require(value == claimed, 'window readout at x=%s is %s, not the claimed %s' % (qs(atom), value_text(value), value_text(claimed)))
    return True


def certify_constant(name, claimed, derived):
    require(claimed == derived, '%s claimed %s*pi^%d differs from the residue-derived %s*pi^%d'
            % (name, qs(claimed[0]), claimed[1], qs(derived[0]), derived[1]))
    return True


def certify_first_moment_finite(kernel, s):
    kmod = modulus_kernel(kernel, s)
    half_line_moment_keyhole(kmod, 1)
    return True


def certify_kernel_choice(kernel_name, frozen_name, after_D_known):
    require(kernel_name == frozen_name, 'kernel %s is not the frozen %s; a kernel switch %s is rejected'
            % (kernel_name, frozen_name, 'after D is known' if after_D_known else 'without a new contract'))
    return True


def certify_state_bound(D, gate_D, provenance):
    require(provenance == 'av1_gate_tier_ii_forward', 'state bound provenance %s is not the AV1-admitted tier (ii) forward value' % provenance)
    require(D == gate_D, 'D=%s is not the AV1 gate-bound tier (ii) forward value' % sci(D))
    return True


def certify_null_replay(window_costs, window_radius, window_route, poisson_costs, poisson_radius, s, L, pi_hi):
    require(window_route == 'same_formula', 'the window null replay must use the unchanged formula, not a bypass branch')
    require(all(window_costs[n] == 0 for n in ('state', 'mean_square', 'kernel_dynamics')),
            'window radius at tau=0 must equal the arithmetic term alone')
    require(window_radius == window_costs['arithmetic'], 'window radius at tau=0 differs from its arithmetic term')
    require(poisson_costs.get('tail', Q(0)) >= s / (pi_hi * L) and poisson_costs.get('tail', Q(0)) > 0,
            'the Poisson comparison at tau=0 keeps its itemized tail s/(pi L)')
    require(poisson_radius == sum(poisson_costs.values(), Q(0)), 'Poisson radius is not its itemized sum')
    return True


def certify_linear_scaling(bracket):
    require(Q(99) <= bracket[0] and bracket[1] <= Q(101),
            'E(tau)/E(tau/100) in [%s,%s] is not linear scaling [99,101]' % (sci(bracket[0], 6), sci(bracket[1], 6)))
    return True


def producer_outcome(kernel, lemma, constants, tier, radius, target):
    if kernel != 'C2_window' or not lemma or not constants:
        return 'insufficient'
    if tier == 'i':
        return 'limited'
    require(tier == 'ii_forward', 'unadmitted state tier %s' % tier)
    if radius > target:
        return 'limited'
    return 'accepted_within_scope'


def certify_outcome(recorded, inputs):
    computed = producer_outcome(**inputs)
    require(recorded == computed, 'recorded outcome %s differs from the evidence-derived %s' % (recorded, computed))
    return computed


def validate_claim_flags(flags, node_met):
    require(sorted(flags) == sorted(UNIVERSAL_FLAGS + ('euclidean_node_certified',)), 'claim flag set changed')
    for name in UNIVERSAL_FLAGS:
        require(flags[name] is False, 'claim flag %s must be false in AV2' % name)
    require(flags['euclidean_node_certified'] is node_met, 'euclidean_node_certified must equal (radius<=10^-6)')
    return True


def certify_model(tau, selected, s, model_id, provenance, frozen):
    require(model_id == frozen['model_id'], 'model id %s is not %s' % (model_id, frozen['model_id']))
    require(len(selected) == 3 and all(parse_q(x) == 0 for x in selected), 'nonzero selected triple is a different model (P_R not Haar)')
    require(abs(parse_q(tau)) == frozen['abs_tau'], 'coupling %s is a model change, not the frozen cap' % tau)
    require(parse_q(s) == frozen['s'], 'Euclidean node s=%s is not the frozen s=1' % s)
    require(provenance == frozen['provenance'], 'state provenance %s is not the AQ1 centered whole-star subsequence' % provenance)
    return True


def certify_poisson_moment_bound(B, s, pi_hi, log10_lo):
    """Claim: sup_L int_{-L}^{L} |theta| P_s <= B. Exhibit L=10^j with a larger lower bound."""
    must(s == 1, 'divergence witness written for s=1')
    j = int(ceil_to(Q(B) * pi_hi / (2 * log10_lo), 1)) + 1
    lower = 2 * j * log10_lo / pi_hi
    require(lower <= Q(B), 'Poisson truncated first moment at L=10^%d is >= %s > claimed bound %s' % (j, sci(lower, 6), sci(B, 6)))
    return True


# --------------------------------------------------------------- contract
def parse_window_poly(body):
    terms = re.findall(r'[+-]?[^+-]+', body)
    out = {}
    for t in terms:
        m = re.fullmatch(r'([+-]?)(\d*)(s(?:\^(\d+))?)?(x(?:\^(\d+))?)?', t)
        require(m is not None, 'malformed window term ' + t)
        coeff = int(m.group(2) or '1') * (-1 if m.group(1) == '-' else 1)
        sp = 0 if not m.group(3) else int(m.group(4) or 1)
        xp = 0 if not m.group(5) else int(m.group(6) or 1)
        require(sp == xp, 'window term %s is not a function of s*x' % t)
        out[xp] = coeff
    return out


def contract_window(text):
    m = re.fullmatch(r'g\(x\)=e\^\{-sx\} for x>=0; g\(x\)=e\^\{sx\}\(([^)]*)\) for x<0', text)
    require(m is not None, 'window text not in the frozen form')
    return parse_window_poly(m.group(1))


def contract_transform(text):
    m1 = re.search(r'ghat\(theta\)=(\d+)s\^(\d+)/\(pi\(s-i theta\)\^(\d+)\(s\+i theta\)\)', text)
    m2 = re.search(r'\|ghat\|=\((\d+)s\^(\d+)/pi\)\(s\^2\+theta\^2\)\^-(\d+)', text)
    m3 = re.search(r'\|\|ghat\|\|_1=(\d+)', text)
    m4 = re.search(r'int\|theta\|\|ghat\|=(\d+)s/pi', text)
    m5 = re.search(r'int theta\^2\|ghat\|=(\d+)s\^2', text)
    require(None not in (m1, m2, m3, m4, m5), 'window transform text not in the frozen form')
    return {'coef': int(m1.group(1)), 'coef_power': int(m1.group(2)), 'lower_order': int(m1.group(3)),
            'mod_coef': int(m2.group(1)), 'mod_power': int(m2.group(2)), 'mod_exponent': int(m2.group(3)),
            'M0': int(m3.group(1)), 'M1_coef': int(m4.group(1)), 'M2_coef': int(m5.group(1))}


def contract_slope(text):
    m = re.fullmatch(r'k=(\d+)\|tau\|/(\d+) in G=H/alpha units from \|\|B_N\|\|<=(\d+)\|tau\|/(\d+) \((\w+) stars\)', text)
    require(m is not None, 'Duhamel slope text not in the frozen form')
    words = {'two': 2, 'seven': 7}
    require(m.group(5) in words, 'star count word')
    return Q(int(m.group(1)), int(m.group(2))), Q(int(m.group(3)), int(m.group(4))), words[m.group(5)]


def contract_state_bound(text):
    m = re.match(r'D = (\d+)/(\d+) \(forward AV1 tier ii, admitted in research/round32/advisor/av1-gate\.json\)', text)
    require(m is not None, 'state bound text not in the frozen form')
    require('tier (i) and the AT4 square-root bound must not be used' in text, 'state bound exclusion text')
    return Q(int(m.group(1)), int(m.group(2)))


def gate_values(gate):
    must(gate.get('loop') == 'AV1' and gate.get('verdict') == 'accepted_within_scope', 'AV1 gate verdict')
    md = re.search(r'Bind the forward tier-\(ii\) value D_ii=(\d+)/(\d+) \(certified by both inequalities\) as the admitted state bound for AV2', gate['decision'])
    mi = re.search(r'D_i=(\d+)/(\d+) \(~2\.3680e-5; exact, forward\)', gate['accepted'])
    mr = re.search(r'D_ii<=(\d+)/10\^40 \(~1\.1390e-8', gate['accepted'])
    mc = re.search(r'either sign of tau with \|tau\|<=10\^-(\d+)', gate['accepted'])
    must(None not in (md, mi, mr, mc), 'AV1 gate values not found')
    return {'D': Q(int(md.group(1)), int(md.group(2))), 'D_i': Q(int(mi.group(1)), int(mi.group(2))),
            'D_rev': Q(int(mr.group(1)), 10 ** 40), 'cap': Q(1, 10 ** int(mc.group(1)))}


def validate_contract(data, ctx):
    require(data.get('id') == 'AV2' and data.get('status') == 'frozen_before_production', 'contract identity or status')
    p = data['parameters']
    require(parse_q(p['tau']) == ctx['gate']['cap'], 'contract tau differs from the AV1-admitted cap')
    require(parse_q(p['control_tau']) == -ctx['gate']['cap'], 'contract control tau is not the mirrored cap')
    require(parse_q(p['s']) == 1, 'contract node is not s=1')
    require(len(p['selected_coefficients_over_alpha']) == 3 and all(parse_q(x) == 0 for x in p['selected_coefficients_over_alpha']),
            'contract selected triple is not zero')
    target = data['preregistration']['target']
    require(target['quantity'] == 'radius' and target['comparator'] == '<=', 'target quantity/comparator')
    require(parse_q(target['value']) == ctx['selection_target'], 'contract target differs from the unchanged 10^-6 of the selection record')
    D = contract_state_bound(p['state_bound'])
    require(D == ctx['gate']['D'], 'contract state bound differs from the AV1 gate-bound tier (ii) value')
    require(contract_window(p['window']) == ctx['window_poly_int'], 'contract window differs from the residue-reconstructed C^2 window')
    tr = contract_transform(p['window_transform'])
    require(tr == ctx['transform'], 'contract transform or constants differ from the residue derivation: %s' % tr)
    require(contract_slope(p['duhamel_slope']) == ctx['slope'], 'contract Duhamel slope differs from the seven-star derivation')
    mm = re.search(r'Haar product reference C_0\(s\)=e\^\{-(\d+)s\}/(\d+)', data['model'])
    require(mm is not None and int(mm.group(1)) == calc.FREE_ENERGY_ALPHA and Q(1, int(mm.group(2))) == calc.FREE_VARIANCE,
            'contract free reference is not e^{-3s}/4')
    ids = data['controls']
    prereg = data['preregistration']['controls_required']['ids']
    require(len(set(ids)) == len(ids) and set(prereg) <= set(ids), 'controls list lost a preregistered id')
    require(set(data['new_control_semantics']) <= set(ids), 'controls list lost a new-control id')
    require(data.get('reverse_premise_isolation') is True, 'reverse premise isolation flag')
    return True


def validate_contract_bytes(raw, expected_sha, ctx):
    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'contract bytes do not match the bound hash')
    data = json.loads(raw)
    validate_contract(data, ctx)
    return data


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    for f in files:
        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)
        require(f not in contract.get('forward_additional_premises', []), 'forward-only premise in reverse inputs: ' + f)
    require(set(files) == expected and len(files) == len(expected),
            'reverse inputs inventory differs from AGENTS.md + contract + shared_premises')
    return True


# ------------------------------------------------------------ Poisson side
def poisson_costs(D, k, s, L, pi_lo):
    """AT4 F16 with directed enclosures: state, mean square, bulk dynamics, whole tail."""
    _, log_hi = log_bounds(1 + (Q(L) / s) ** 2)
    return {'state': D, 'mean_square': D * D,
            'bulk_dynamics': ceil_to(k * s * log_hi / pi_lo),
            'tail': ceil_to((Q(1, 2) + D / 2) * 2 * s / (pi_lo * L))}


def poisson_floor(k, s, pi_lo, pi_hi):
    """min_L (k s/pi) log(1+L^2/s^2) + s/(pi L) at s=1: unique critical point 2kL^3 = 1+L^2."""
    must(s == 1, 'floor written for s=1')

    def u(L):
        return 2 * k * L ** 3 - L * L - 1

    lo = int(1 / (3 * k))
    hi = int(1 / k) + 1
    must(u(Q(lo)) < 0 and u(Q(hi)) > 0, 'floor bracket')
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if u(Q(mid)) < 0:
            lo = mid
        else:
            hi = mid
    log_lo_a, _ = log_bounds(1 + Q(lo) ** 2)
    _, log_hi_a = log_bounds(1 + Q(lo) ** 2)
    lower = floor_to(k * log_lo_a / pi_hi + Q(1) / (pi_hi * hi))
    upper = ceil_to(k * log_hi_a / pi_lo + Q(1) / (pi_lo * lo))
    return {'L_star_bracket': [lo, hi], 'floor_lower': lower, 'floor_upper': upper}


# ==================================================================== compute
def compute():
    check_py_sha = sha256_file(HERE / 'check.py')          # recorded before any evaluation
    calculator_sha = sha256_file(HERE / 'calculator.py')
    raw = (INPUTS / CONTRACT_REL).read_bytes()
    contract_sha = hashlib.sha256(raw).hexdigest()
    must(contract_sha == CONTRACT_SHA256, 'contract snapshot hash mismatch')
    contract_json = json.loads(raw)
    gate = json.loads((INPUTS / GATE_REL).read_text())
    selection = (INPUTS / SELECTION_REL).read_text()
    record('contract_snapshot_bound', contract_sha == CONTRACT_SHA256, contract_sha256=contract_sha,
           source='inputs/' + CONTRACT_REL)
    record('check_py_hash_recorded_before_evaluation', len(check_py_sha) == 64 and len(calculator_sha) == 64,
           check_py_sha256=check_py_sha, calculator_py_sha256=calculator_sha)
    cache = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if '__pycache__' in p.parts or p.suffix == '.pyc')
    record('no_interpreter_cache_in_closure', cache == [])

    PI_LO, PI_HI = pi_bounds()
    cpi_lo, cpi_hi = calc.pi_interval()
    must(Q(314159, 100000) < PI_LO and PI_HI < Q(314160, 100000) and PI_HI - PI_LO < Q(1, 10 ** 38), 'pi enclosure')
    must(cpi_lo <= PI_HI and PI_LO <= cpi_hi, 'calculator and checker pi enclosures intersect')

    gv = gate_values(gate)
    ms = re.search(r'against the unchanged 10\^-(\d+) target', selection)
    must(ms is not None, 'selection record target not found')
    selection_target = Q(1, 10 ** int(ms.group(1)))
    params = contract_json['parameters']
    TAU = parse_q(params['tau'])
    ABS_TAU = abs(TAU)
    S0 = parse_q(params['s'])
    TARGET = parse_q(contract_json['preregistration']['target']['value'])

    # ---- reverse analysis: the kernel family K_n by the residue ansatz
    family = {}
    for n in (1, 2, 3):
        raw_kernel = {'coef': Q(1), 'factors': [(CQ(S0), IU, 1), (CQ(S0), -IU, n)], 'num': [CQ(1)]}
        inv0 = inverse_transform(raw_kernel)
        must(len(inv0['nonneg']) == 1 and inv0['nonneg'][0][0] == -S0 and len(inv0['nonneg'][0][1]) == 1,
             'upper half-plane holds exactly one simple pole at theta=is')
        c0 = inv0['nonneg'][0][1][0]
        K = dict(raw_kernel, coef=raw_kernel['coef'] / c0)
        inv = certify_kernel_identity(K, S0)
        kmod_ok, moments = True, {}
        try:
            kmod = modulus_kernel(K, S0)
        except Rejected as exc:
            kmod_ok, kmod, moments = False, None, {'modulus': str(exc)}
        if kmod_ok:
            for kk in (0, 1, 2, 3):
                moments['M%d_finite' % kk] = decay_order(kmod, kk) >= 2
        family[n] = {'kernel': K, 'inv': inv, 'kmod': kmod, 'moments': moments}
    must(family[1]['kernel']['coef'] == S0 and family[1]['inv']['neg'] == [(S0, [Q(1)])],
         'n=1 is the Poisson kernel s/(pi(s^2+theta^2)) with inverse e^{-s|x|}')
    for n in (1, 2, 3):
        must(family[n]['kernel']['coef'] == Q((2 * S0) ** n) / 2, 'normalization (2s)^n/2 from the upper residue')
    n_min = min(n for n in (1, 2, 3) if family[n]['kmod'] is not None and decay_order(family[n]['kmod'], 2) >= 2)
    must(n_min == 3, 'minimal lower-pole order with finite M_0, M_1, M_2')
    K3 = family[3]['kernel']
    inv3 = family[3]['inv']
    must(len(inv3['neg']) == 1 and inv3['neg'][0][0] == S0, 'x<0 branch is e^{sx} times a polynomial')
    window_poly = inv3['neg'][0][1]
    window_poly_int = {}
    for p, c in enumerate(window_poly):
        must((c / S0 ** p).denominator == 1, 'window coefficient per s-power is an integer')
        window_poly_int[p] = int(c / S0 ** p)
    record('residue_kernel_family_reconstructed', True,
           ansatz='K_n(theta)=N_n/((s+i theta)(s-i theta)^n): one simple upper pole at theta=is (exactness on x>=0), one lower pole of order n at theta=-is',
           family={str(n): {'coef_times_pi': qs(family[n]['kernel']['coef']),
                            'x_nonneg': describe_half(family[n]['inv']['nonneg']),
                            'x_neg': describe_half(family[n]['inv']['neg']),
                            'residues': family[n]['inv']['residues'],
                            'moments': family[n]['moments']} for n in (1, 2, 3)},
           n1='Poisson kernel s/(pi(s^2+theta^2)), g=e^{-s|x|}', n2='C^1 window', n3='C^2 window (frozen)',
           minimal_order_for_finite_M0_M1_M2=n_min)

    # ---- regularity of the reconstructed window
    derivs_neg, derivs_pos = [], []
    for kder in range(4):
        pos = (-S0) ** kder
        neg = sum((comb(kder, j) * S0 ** (kder - j) * factorial(j) * (window_poly[j] if j < len(window_poly) else 0)
                   for j in range(kder + 1)), Q(0))
        derivs_pos.append(pos)
        derivs_neg.append(neg)
    l1_neg = sum((abs(window_poly[j]) * factorial(j) / S0 ** (j + 1) for j in range(len(window_poly))), Q(0))
    signs_alternate = all((window_poly[j] * (-1) ** j) > 0 for j in range(len(window_poly)))
    g_l1 = 1 / S0 + l1_neg
    record('window_regularity_C2_and_L1', derivs_pos[:3] == derivs_neg[:3] and derivs_pos[3] != derivs_neg[3]
           and signs_alternate and g_l1 == 8 / S0
           and kernel_eval(K3, 0) == cq(g_l1 / 2) and window_poly[1] ** 2 - 4 * window_poly[0] * window_poly[2] < 0,
           derivatives_at_0_plus=[qs(v) for v in derivs_pos], derivatives_at_0_minus=[qs(v) for v in derivs_neg],
           third_derivative_jump=qs(derivs_pos[3] - derivs_neg[3]), g_L1_norm=qs(g_l1),
           ghat_at_0_times_pi=qs(kernel_eval(K3, 0).re), statement="g in C^2 (the first jump is in g'''), g>0, ||g||_1=8/s, g->0 at +-infinity; ghat(0)=||g||_1/(2pi)=4/(pi s)")

    # ---- contract comparison of window and constants (after derivation)
    mod3 = family[3]['kmod']
    M0 = full_line_even_moment(mod3, 0)
    M1_half, keyhole_poles = half_line_moment_keyhole(mod3, 1)
    M1_coef = 2 * mod3['coef'] * M1_half          # M_1 = M1_coef / pi
    M2 = full_line_even_moment(mod3, 2)
    subst_M1_half = Q(1, 2) / S0 ** 2               # u=theta^2: (1/2) int_0^inf (s^2+u)^-2 du
    must(K3['factors'][1][2] == n_min and (K3['coef'] / S0 ** n_min).denominator == 1, 'lower-pole order and coefficient')
    transform_derived = {'coef': int(K3['coef'] / S0 ** n_min), 'coef_power': n_min, 'lower_order': K3['factors'][1][2],
                         'mod_coef': int(mod3['coef'] / S0 ** n_min), 'mod_power': n_min, 'mod_exponent': mod3['factors'][0][2],
                         'M0': int(M0), 'M1_coef': int(M1_coef / S0), 'M2_coef': int(M2 / S0 ** 2)}
    must(M0 == 2 and M1_coef == 4 * S0 and M2 == 2 * S0 ** 2 and M1_half == subst_M1_half, 'residue constants')
    n_star = len(GEOM['incident'])
    slope_derived = (2 * n_star * calc.STAR_NORM_PER_TAU, n_star * calc.STAR_NORM_PER_TAU, n_star)
    must(n_star == calc.INCIDENT_STARS, 'calculator star count equals the derived |R-S|')
    ctx = {'gate': gv, 'selection_target': selection_target, 'window_poly_int': window_poly_int,
           'transform': transform_derived, 'slope': slope_derived}
    contract = validate_contract_bytes(raw, CONTRACT_SHA256, ctx)
    record('contract_semantics_match_derivation', True, window_from_contract=contract_window(params['window']),
           window_from_residues={str(k): v for k, v in sorted(window_poly_int.items())},
           transform_from_contract=contract_transform(params['window_transform']), transform_from_residues=transform_derived,
           note='the contract window, transform and constants are compared only after the residue derivation')
    for theta in (Q(0), Q(1), Q(-3, 7), Q(5), Q(-11, 2)):
        v = kernel_eval(K3, theta)
        must(v.abs2() == (mod3['coef'] / (S0 ** 2 + theta ** 2) ** 2) ** 2, '|ghat|^2 identity at rational theta')
    record('ghat_residue_form_and_modulus', True,
           ghat='4s^3/(pi(s-i theta)^3(s+i theta))', modulus='(4s^3/pi)(s^2+theta^2)^-2',
           residues=inv3['residues'], x_nonneg=describe_half(inv3['nonneg']), x_neg=describe_half(inv3['neg']),
           modulus_identity_rational_points=['0', '1', '-3/7', '5', '-11/2'],
           uniqueness='K_3 is L^1 and its inverse transform is g in L^1; the L^1 inversion theorem gives K_3 = (2pi)^-1 int g e^{-i theta x}dx (both continuous)')
    record('constants_by_residues', M0 == 2 and M1_coef == 4 * S0 and M2 == 2 * S0 ** 2,
           M0=qs(M0), M1='%s/pi' % qs(M1_coef), M2=qs(M2),
           M0_route='2 i (4s^3) Res_{theta=is}(theta-is)^-2(theta+is)^-2 = 2',
           M1_route='keyhole: int_0^inf theta R = -sum Res[theta R log theta] (log symbol cancels pole by pole) = 1/(2s^2)',
           M1_keyhole_poles=keyhole_poles, M1_substitution_crosscheck=qs(subst_M1_half),
           M2_route='2 i (4s^3) Res_{theta=is} theta^2 (theta-is)^-2(theta+is)^-2 = 2s^2',
           signed_integral_of_ghat=qs(readout(K3, Q(0))[0][1]), contract_values=contract_transform(params['window_transform']))
    lin = {}
    for s_val in (Q(1, 3), Q(1), Q(2), Q(7)):
        Ks = {'coef': Q((2 * s_val) ** 3) / 2, 'factors': [(CQ(s_val), IU, 1), (CQ(s_val), -IU, 3)], 'num': [CQ(1)]}
        certify_kernel_identity(Ks, s_val)
        ms_ = modulus_kernel(Ks, s_val)
        m1h, _ = half_line_moment_keyhole(ms_, 1)
        lin[qs(s_val)] = {'M0': qs(full_line_even_moment(ms_, 0)), 'M1_times_pi': qs(2 * ms_['coef'] * m1h),
                          'M2': qs(full_line_even_moment(ms_, 2))}
    record('constants_scaling_in_s', all(Q(v['M0']) == 2 and Q(v['M1_times_pi']) == 4 * Q(sv) and Q(v['M2']) == 2 * Q(sv) ** 2
                                         for sv, v in lin.items()), values=lin)
    free_value = readout(K3, Q(3), calc.FREE_VARIANCE)
    record('window_lemma_free_atom', free_value == [(-3 * S0, Q(1, 4))],
           readout=value_text(free_value), statement='int ghat c_0 = g(3)/4 = e^{-3s}/4 = C_0(s); c_0(theta)=e^{3i theta}/4')
    record('fubini_and_support_premises', M0 == 2 and decay_order(mod3) == 4,
           statement='|ghat(theta) e^{i theta x}| integrates to M_0 * eta(R) = 2||chi||^2 < inf; eta supported in [0,inf) by AQ1 H_num>=0 only (no AQ2 gap)')

    # ---- geometry, clock and Duhamel slope
    record('wilson_cover_and_incident_stars', GEOM['cover'] == (ORIGIN, EZ) and len(GEOM['links']) == 48
           and len(GEOM['endpoints']) == 36 and len(GEOM['incident']) == 7
           and all(lk in GEOM['links'] for lk in WILSON_LINKS),
           owners=[list(o) for o in GEOM['owners']], cover=[list(c) for c in GEOM['cover']], links=len(GEOM['links']),
           endpoints=len(GEOM['endpoints']), incident_anchors=[list(a) for a in GEOM['incident']])
    boxes = {}
    for N in (1, 2, 3):
        anchors = box_star_anchors(N)
        boxes[str(N)] = {'retained_stars': len(anchors), 'incident_retained': sum(1 for a in GEOM['incident'] if a in set(anchors))}
    k_value = 2 * calc.INCIDENT_STARS * calc.STAR_NORM_PER_TAU * ABS_TAU
    slope_text = contract_slope(params['duhamel_slope'])
    record('seven_star_duhamel_slope', certify_slope(k_value, ABS_TAU, GEOM['incident']) and k_value == Q(49, 4) * ABS_TAU
           and slope_text == slope_derived and boxes['2']['incident_retained'] == 7 and boxes['2']['retained_stars'] == 64,
           k=qs(k_value), B_N_norm=qs(Q(49, 8) * ABS_TAU), boxes=boxes,
           statement='relative unitary K=e^{i theta G_N}e^{-i theta A_N}: ||K-I||<=|theta| ||B_N||; ||K X K*-X||<=2||K-I|| ||X||')
    certify_generator_units(calc.FREE_ENERGY_ALPHA, 'alpha', calc.STAR_NORM_PER_TAU)

    # ---- the state bound D from the contract, bound by the AV1 gate
    D = contract_state_bound(params['state_bound'])
    av1 = calc.av1_tier_ii_forward(ABS_TAU)
    certify_state_bound(D, gv['D'], 'av1_gate_tier_ii_forward')
    record('av1_state_bound_bound_and_reproduced', D == gv['D'] and av1['D'] == D and calc.ADMITTED_D_CAP == D,
           D=qs(D), preview=sci(D), formula={k2: qs(v) for k2, v in av1.items()},
           gate_decision='Bind the forward tier-(ii) value as the admitted state bound for AV2',
           consequences='|m|=|omega(W)|<=D, m^2<=D^2')

    # ---- certificate at +tau (calculator, fixed design) and independent verification
    cert = calc.certify(fixed_design=True)
    minus = calc.certify(tau=params['control_tau'])
    c = {k2: Q(v) for k2, v in cert['costs'].items()}
    radius = Q(cert['certified_radius'])
    datum = Q(cert['certified_datum'])
    e_lo, e_hi = exp_minus_alternating(3 * S0)
    own_free = (calc.FREE_VARIANCE * e_lo, calc.FREE_VARIANCE * e_hi)
    calc_free = (Q(cert['free_C_interval']['lower']), Q(cert['free_C_interval']['upper']))
    certify_radius(c, radius, D, k_value, S0, M0, M1_coef / S0, PI_LO if PI_LO >= cpi_lo else cpi_lo, (calc_free[1] - calc_free[0]) / 2)
    must(abs(c['kernel_dynamics'] - ceil_to(k_value * M1_coef / PI_LO)) <= Q(2, 10 ** 38), 'kernel-dynamics term cross-check')
    must(own_free[0] <= calc_free[1] and calc_free[0] <= own_free[1] and own_free[1] - own_free[0] < Q(1, 10 ** 35),
         'independent e^{-3}/4 enclosures intersect')
    e1_lo, e1_hi = exp_minus_alternating(S0)
    must(e1_lo ** 3 <= e_hi and e_lo <= e1_hi ** 3, 'e^{-3} consistent with (e^{-1})^3')
    node_met = admit_bound(radius, TARGET)
    record('radius_plus_tau_itemized', node_met is True and cert['target_met'] is True
           and Q(17, 10 ** 8) <= radius <= Q(2, 10 ** 7),
           tau=qs(TAU), s=qs(S0), costs={k2: qs(v) for k2, v in sorted(c.items())},
           costs_preview={k2: sci(v) for k2, v in sorted(c.items())}, radius=qs(radius), radius_preview=sci(radius),
           datum=qs(datum), interval=cert['actual_C_interval'], target=qs(TARGET), target_met=node_met,
           contract_preview='about 1.83e-7; acceptance preview 1.7-2.0e-7')
    record('radius_minus_tau_replay', minus['certified_radius'] == cert['certified_radius']
           and minus['certified_datum'] == cert['certified_datum'] and minus['target_met'] is True,
           tau=params['control_tau'], radius=minus['certified_radius'],
           statement='same |tau| formula: a replay at the mirrored coupling, not a second confirmation')
    free_inside = Q(cert['actual_C_interval']['lower']) <= calc_free[0] and calc_free[1] <= Q(cert['actual_C_interval']['upper'])
    record('free_reference_inside_reference_unresolved', free_inside and cert['resolved_interaction_shift'] is False
           and cert['sub_label'] == 'reference_unresolved', free_interval=cert['free_C_interval'],
           statement='e^{-3}/4 lies inside the enclosure: no interaction shift, sign or coefficient is claimed')
    record('arithmetic_enclosure_e_minus_3', c['arithmetic'] > 0 and c['arithmetic'] < Q(1, 10 ** 38),
           calculator_enclosure=cert['free_C_interval'], checker_enclosure={'lower': qs(own_free[0]), 'upper': qs(own_free[1])},
           exact_datum=cert['certified_datum'], method='calculator: reciprocal of the positive Taylor series with geometric tail; checker: alternating series; both halve and square outward')

    # ---- retained failures: AT4 Poisson L=10^4, optimized floor, divergent first moment
    retained = contract_json['parameters']['retained_insufficient_controls']
    mr1 = re.search(r'L=10\^(\d+) \(radius ~([0-9.]+)\)', retained[0])
    mr2 = re.search(r'floor ~([0-9.]+)e-(\d+) at L~([0-9.]+)e(\d+)', retained[1])
    must(mr1 is not None and mr2 is not None, 'retained controls text')
    L4 = Q(10) ** int(mr1.group(1))
    D_at4 = 2 * sqrt_bounds(Q(49, 3) * ABS_TAU)[1]
    pc = poisson_costs(D_at4, k_value, S0, L4, PI_LO)
    p_rad = sum(pc.values(), Q(0))
    stated_at4 = Q(mr1.group(2))
    record('retained_at4_poisson_L1e4', p_rad > TARGET and abs(p_rad - stated_at4) < Q(1, 10 ** 9),
           D_at4_upper=qs(D_at4), costs={k2: sci(v) for k2, v in sorted(pc.items())}, radius=qs(p_rad), radius_preview=sci(p_rad),
           contract_stated=mr1.group(2), outcome='insufficient (retained)')
    pc_adm = poisson_costs(D, k_value, S0, L4, PI_LO)
    record('retained_poisson_with_admitted_D_L1e4', sum(pc_adm.values(), Q(0)) > TARGET and pc_adm['tail'] > TARGET,
           costs={k2: sci(v) for k2, v in sorted(pc_adm.items())}, radius_preview=sci(sum(pc_adm.values(), Q(0))),
           statement='even with the AV1 tier-(ii) D the Poisson tail alone exceeds 10^-6 at L=10^4')
    fl = poisson_floor(k_value, S0, PI_LO, PI_HI)
    stated_floor = Q(mr2.group(1)) / 10 ** int(mr2.group(2))
    stated_L = Q(mr2.group(3)) * 10 ** int(mr2.group(4))
    record('retained_poisson_floor_optimized', fl['floor_lower'] > TARGET and abs(fl['floor_lower'] - stated_floor) < Q(1, 10 ** 10)
           and abs(Q(fl['L_star_bracket'][0]) - stated_L) < Q(10 ** 4),
           L_star_bracket=fl['L_star_bracket'], floor_lower=qs(fl['floor_lower']), floor_upper=qs(fl['floor_upper']),
           floor_preview=[sci(fl['floor_lower']), sci(fl['floor_upper'])], with_admitted_D_lower=sci(fl['floor_lower'] + D + D * D),
           contract_stated=[mr2.group(1) + 'e-' + mr2.group(2), 'L~' + mr2.group(3) + 'e' + mr2.group(4)],
           statement='u(L)=2kL^3-L^2-1 has one positive root; F decreases before and increases after it; the lower bound holds for every L>0 with D->0')
    log10_lo, _ = log_bounds(Q(10))
    trunc_window = {str(j): qs(Q(4) * S0 * Q(10) ** (2 * j) / (S0 ** 2 + Q(10) ** (2 * j))) for j in (1, 2, 4, 8)}
    record('poisson_first_moment_divergent_window_finite',
           all(Q(v) < M1_coef for v in trunc_window.values()) and family[1]['moments'].get('M1_finite') is False
           and family[3]['moments'].get('M1_finite') is True,
           poisson_truncated_first_moment='(s/pi) log(1+L^2/s^2) -> infinity',
           window_truncated_first_moment_times_pi=trunc_window, window_M1_times_pi=qs(M1_coef),
           poisson_kink='g=e^{-s|x|}: g\'(0+)-g\'(0-)=-2s, so |ghat|~theta^-2',
           window_decay='|ghat|~theta^-4 (g\'\'\' jumps by -8s^3)')

    # ---- crossover s*
    cross_text = re.search(r'about ([0-9.]+)-([0-9.]+)', contract_json['required'][5])
    must(cross_text is not None, 'crossover range text')
    A = 2 * (D + D * D)
    s_lo = floor_to((TARGET - A) * PI_LO / (49 * ABS_TAU), 10 ** 9)
    s_hi = ceil_to((TARGET - A) * PI_HI / (49 * ABS_TAU), 10 ** 9)
    s_below = s_lo - Q(1, 10 ** 9)
    s_above = s_hi + Q(1, 10 ** 9)
    below = calc.certify(s=s_below)
    above_lower = A + 49 * ABS_TAU * s_above / PI_HI
    record('crossover_s_star_enclosed', below['target_met'] is True and above_lower > TARGET
           and Q(cross_text.group(1)) <= s_lo and s_hi <= Q(cross_text.group(2)),
           s_star_bracket=[qs(s_lo), qs(s_hi)], s_star_preview=sci(s_lo, 8),
           witness_below={'s': qs(s_below), 'radius': below['radius_preview']},
           witness_above={'s': qs(s_above), 'analytic_radius_lower': sci(above_lower)},
           contract_range=[cross_text.group(1), cross_text.group(2)],
           rule='E(s)=2(D+D^2)+49|tau|s/pi is linear in s; no grid claim beyond s*, no [0,128] claim at the cap')

    # ---- tier (i) and the C^1 preview (retained / preview only)
    D_i = gv['D_i']
    E_i = 2 * (D_i + D_i * D_i) + ceil_to(k_value * 4 * S0 / PI_LO)
    record('tier_i_preview_retained_limited', E_i > TARGET and certify_outcome('limited', dict(
        kernel='C2_window', lemma=True, constants=True, tier='i', radius=E_i, target=TARGET)) == 'limited',
           D_i=qs(D_i), radius_preview=sci(E_i), outcome='limited (retained)',
           note='contract preview 3.6-4.7e-5; the exact tier-(i) value here is ~4.752e-5 (rounded preview)')
    K2 = family[2]['kernel']
    c1_poly = family[2]['inv']['neg'][0][1]
    c1_text = re.search(r'the C\^1 window g=e\^\{sx\}\(([^)]*)\) \(x<0\) with M_0=(\d+)/pi, M_1=(\d+)s/pi, M_2=(\w+), negative-atom value (\d+)/e and sign-mutation value (\d+)e\^\{-(\d+)\}/(\d+)',
                        contract_json['new_control_semantics']['c1_window_preview_only'])
    must(c1_text is not None, 'C^1 semantics text')
    c1_neg_atom = readout(K2, Q(-1))
    c1_sign = readout(mirror(K2), Q(3), calc.FREE_VARIANCE)
    c1_mod = rejection(modulus_kernel, K2, S0)
    preview = calc.preview_c1_window()
    c1_ok = (parse_window_poly(c1_text.group(1)) == {p: int(v / S0 ** p) for p, v in enumerate(c1_poly)}
             and int(c1_text.group(2)) == 4 and int(c1_text.group(3)) == 4 and c1_text.group(4) == 'infinity'
             and c1_neg_atom == [(-S0, Q(int(c1_text.group(5))))]
             and c1_sign == [(-3 * S0, Q(int(c1_text.group(6)), int(c1_text.group(8))))]
             and preview['certified'] is False)
    record('c1_window_preview_values', c1_ok, window_neg='e^{sx}(%s)' % poly_text(c1_poly),
           M0='4/pi (substitution: (2s^2/pi) int (s^2+theta^2)^-3/2 = 4/pi)', M1='4s/pi (substitution)',
           M2='infinity (theta^2|ghat_1| ~ 1/|theta|)', residue_route_refused=c1_mod,
           negative_atom=value_text(c1_neg_atom), sign_mutation=value_text(c1_sign),
           radius_preview=preview['radius_preview'], label=preview['label'])

    # ---- calculator domain
    cases = [
        ('nonzero_selected', {'selected': ('0', '1/100', '0')}), ('selected_wrong_length', {'selected': ('0', '0')}),
        ('selected_float', {'selected': ('0', 0.0, '0')}), ('selected_malformed', {'selected': ('0', 'NaN', '0')}),
        ('positive_cap_exceeded', {'tau': '1/10000000'}), ('negative_cap_exceeded', {'tau': '-1/10000000'}),
        ('tau_float', {'tau': 1e-8}), ('tau_bool', {'tau': True}), ('tau_nan', {'tau': 'NaN'}),
        ('tau_infinity', {'tau': 'Infinity'}), ('tau_empty', {'tau': ''}), ('tau_zero_denominator', {'tau': '1/0'}),
        ('tau_bad_separator', {'tau': '1//2'}), ('tau_object', {'tau': None}),
        ('s_zero', {'s': '0'}), ('s_negative', {'s': '-1'}), ('alpha_zero', {'alpha': '0'}),
        ('hbar_negative', {'hbar': '-1'}), ('E_star_zero', {'E_star': '0'}), ('lattice_spacing_zero', {'lattice_spacing': '0'}),
        ('target_zero', {'target': '0'}), ('target_float', {'target': 1e-6}),
        ('fixed_design_changed_tau', {'fixed_design': True, 'tau': '-1/100000000'}),
        ('fixed_design_changed_s', {'fixed_design': True, 's': '2'}),
        ('fixed_design_changed_target', {'fixed_design': True, 'target': '1/100000'}),
        ('fixed_design_not_boolean', {'fixed_design': 'true'}),
        ('state_tier_i', {'state_tier': 'i'}), ('state_tier_ii_reverse', {'state_tier': 'ii_reverse'}),
        ('state_tier_at4_sqrt', {'state_tier': 'at4_sqrt'}), ('kernel_c1', {'kernel': 'C1_window'}),
        ('kernel_poisson', {'kernel': 'poisson'}),
    ]
    rejected_cases = {}
    for name, kwargs in cases:
        try:
            calc.certify(**kwargs)
        except calc.DomainError as exc:
            rejected_cases[name] = str(exc)
        else:
            raise ProducerError('invalid calculator case accepted: ' + name)
    scaled = calc.certify(alpha='5', hbar='7', E_star='3', lattice_spacing='2')
    exact_forms = calc.exact(Q(1, 10), 'q') == calc.exact('0.1', 'd') == calc.exact('1/10', 'r') and calc.exact(1, 'i') == 1
    record('calculator_domain_and_exact_inputs', len(rejected_cases) == len(cases) and exact_forms
           and scaled['physical_Euclidean_time'] == '7/5' and scaled['certified_radius'] == cert['certified_radius'],
           rejected_cases=rejected_cases, physical_time_alpha5_hbar7=scaled['physical_Euclidean_time'],
           domain='zero selected triple; |tau|<=10^-8; s>0; positive physical scales and target; tier ii forward; C2 window')

    # =================================================== the contract controls
    control('missing_incoming_stars', [
        ('outgoing_anchors_only', certify_slope, (2 * 2 * calc.STAR_NORM_PER_TAU * ABS_TAU, ABS_TAU, [ORIGIN, EZ])),
        ('origin_star_only', certify_slope, (2 * calc.STAR_NORM_PER_TAU * ABS_TAU, ABS_TAU, [ORIGIN])),
    ], complete_anchors=[list(a) for a in GEOM['incident']], outgoing_only_slope=qs(Q(7, 2) * ABS_TAU))
    control('full_original_wilson_cover', [
        ('origin_factor_only', certify_cover, (((0, 0, 0),), 24)),
        ('four_displayed_links', certify_cover, (GEOM['cover'], 4)),
        ('extra_factor', certify_cover, (((0, 0, -1), (0, 0, 0), (0, 0, 1)), 72)),
    ], links=len(GEOM['links']), endpoints=len(GEOM['endpoints']))
    phys = []
    for alpha, hbar in ((Q(1), Q(1)), (Q(5), Q(7)), (Q(2, 3), Q(11))):
        t_e = hbar * S0 / alpha
        phys.append(qs(calc.FREE_ENERGY_ALPHA * alpha * t_e / hbar))
    must(len(set(phys)) == 1 and phys[0] == '3', 'physical-scale invariance of the free exponent')
    control('wrong_delta_alpha_hbar_clock', [
        ('exponent_24_with_alpha_clock', certify_generator_units, (24, 'alpha', calc.STAR_NORM_PER_TAU)),
        ('energy_3_with_normalized_clock', certify_generator_units, (3, 'delta', calc.STAR_NORM_PER_TAU)),
        ('normalized_star_norm_in_alpha_clock', certify_generator_units, (3, 'alpha', Q(7))),
        ('slope_98_tau_eightfold', certify_slope, (98 * ABS_TAU, ABS_TAU, GEOM['incident'])),
    ], free_exponent_for_scales=phys, statement='s=alpha t_E/hbar; free energy 3 alpha; u=s/8 with exponent 24 forbidden')
    m_c, d_c = Q(1, 4), Q(1, 100)
    vacuum_atom = readout(K3, Q(0), m_c ** 2)
    control('vector_versus_scalar_centering', [
        ('scalar_subtraction', certify_centering, ('scalar',)),
        ('uncentered', certify_centering, ('uncentered',)),
    ], exact_control={'vector': qs(centering_shift('vector', m_c, d_c)), 'scalar': qs(centering_shift('scalar', m_c, d_c)),
                      'uncentered_residue': qs(centering_shift('uncentered', m_c, d_c))},
        window_readout_of_vacuum_atom=value_text(vacuum_atom), note='g(0)=1: an uncentered readout keeps m^2')
    arith_c = c['arithmetic']
    no_ms = {k2: v for k2, v in c.items() if k2 != 'mean_square'}
    zero_ms = dict(c, mean_square=Q(0))
    control('first_order_mean_charged', [
        ('mean_square_dropped', certify_radius, (no_ms, radius - c['mean_square'], D, k_value, S0, M0, M1_coef / S0, cpi_lo, arith_c)),
        ('zero_mean_assumed', certify_radius, (zero_ms, radius - c['mean_square'], D, k_value, S0, M0, M1_coef / S0, cpi_lo, arith_c)),
    ], mean_square_term=qs(c['mean_square']), statement='|m|<=D by trace duality; m^2<=D^2 is charged at M_0')

    def window_E(abs_tau, D_value, pi_val):
        return 2 * (D_value + D_value * D_value) + 49 * abs_tau * S0 / pi_val

    D_small = calc.av1_tier_ii_forward(ABS_TAU / 100)['D']
    ratio = (window_E(ABS_TAU, D, PI_HI) / window_E(ABS_TAU / 100, D_small, PI_LO),
             window_E(ABS_TAU, D, PI_LO) / window_E(ABS_TAU / 100, D_small, PI_HI))
    certify_linear_scaling(ratio)
    D_at4_small = 2 * sqrt_bounds(Q(49, 3) * ABS_TAU / 100)[1]
    at4_ratio = (window_E(ABS_TAU, D_at4, PI_HI) / window_E(ABS_TAU / 100, D_at4_small, PI_LO),
                 window_E(ABS_TAU, D_at4, PI_LO) / window_E(ABS_TAU / 100, D_at4_small, PI_HI))
    control('tau_scaling_exponent', [
        ('at4_square_root_state_bound_labelled_linear', certify_linear_scaling, (at4_ratio,)),
    ], window_ratio=[sci(ratio[0], 8), sci(ratio[1], 8)], at4_sqrt_ratio=[sci(at4_ratio[0], 6), sci(at4_ratio[1], 6)])
    frozen = {'model_id': contract_json['preregistration']['model_id'], 'abs_tau': ABS_TAU, 's': S0,
              'provenance': contract_json['preregistration']['state_provenance']}
    must(certify_model(params['tau'], ('0', '0', '0'), params['s'], frozen['model_id'], frozen['provenance'], frozen), 'frozen model')
    control('changed_model_relabelled', [
        ('nonzero_selected_triple', certify_model, (params['tau'], ('0', '1/100', '0'), '1', frozen['model_id'], frozen['provenance'], frozen)),
        ('at5_coupling_as_cap_node', certify_model, ('1/100000000000000', ('0', '0', '0'), '1', frozen['model_id'], frozen['provenance'], frozen)),
        ('crossover_node_as_frozen_node', certify_model, (params['tau'], ('0', '0', '0'), '6', frozen['model_id'], frozen['provenance'], frozen)),
        ('finite_graph_model', certify_model, (params['tau'], ('0', '0', '0'), '1', 'finite_graph', frozen['provenance'], frozen)),
        ('finite_box_provenance', certify_model, (params['tau'], ('0', '0', '0'), '1', frozen['model_id'], 'finite_volume_box', frozen)),
    ])
    base = json.loads(raw)

    def coherent(mutate):
        doc = json.loads(json.dumps(base))
        mutate(doc)
        blob = json.dumps(doc, indent=2).encode()
        return blob, hashlib.sha256(blob).hexdigest()

    tampers = {}
    for label, mutate in (
            ('target_relaxed_1e-3', lambda d: d['preregistration']['target'].__setitem__('value', '1/1000')),
            ('state_bound_tier_i', lambda d: d['parameters'].__setitem__('state_bound', d['parameters']['state_bound'].replace(
                qs(gv['D']), qs(gv['D_i'])))),
            ('window_c1', lambda d: d['parameters'].__setitem__('window', 'g(x)=e^{-sx} for x>=0; g(x)=e^{sx}(1-2sx) for x<0')),
            ('l1_norm_one', lambda d: d['parameters'].__setitem__('window_transform', d['parameters']['window_transform'].replace(
                '||ghat||_1=2', '||ghat||_1=1'))),
            ('slope_two_stars', lambda d: d['parameters'].__setitem__('duhamel_slope',
                                                                         'k=7|tau|/2 in G=H/alpha units from ||B_N||<=7|tau|/4 (two stars)')),
            ('tau_1e-14', lambda d: d['parameters'].__setitem__('tau', '1/100000000000000')),
            ('control_removed', lambda d: d['controls'].pop())):
        tampers[label] = coherent(mutate)
    control('coherent_evidence_tampering', [
        (label, validate_contract_bytes, (blob, digest, ctx)) for label, (blob, digest) in sorted(tampers.items())
    ] + [('byte_change_without_rehash', validate_contract_bytes, (raw + b' ', CONTRACT_SHA256, ctx))],
        note='each tampered copy is rehashed coherently; semantic comparison with the gate, the selection record and the residue derivation still rejects it')
    good = dict(kernel='C2_window', lemma=True, constants=True, tier='ii_forward', radius=radius, target=TARGET)
    outcome = certify_outcome(producer_outcome(**good), good)
    at4_inputs = dict(kernel='poisson', lemma=True, constants=True, tier='ii_forward', radius=p_rad, target=TARGET)
    floor_inputs = dict(kernel='poisson', lemma=True, constants=True, tier='ii_forward', radius=fl['floor_lower'], target=TARGET)
    tier_i_inputs = dict(good, tier='i', radius=E_i)
    lemma_fail = dict(good, lemma=False)
    control('insufficient_verdict_retained', [
        ('at4_poisson_relabelled_accepted', certify_outcome, ('accepted_within_scope', at4_inputs)),
        ('poisson_floor_relabelled_limited', certify_outcome, ('limited', floor_inputs)),
        ('tier_i_relabelled_accepted', certify_outcome, ('accepted_within_scope', tier_i_inputs)),
        ('lemma_failure_relabelled_limited', certify_outcome, ('limited', lemma_fail)),
    ], retained={'at4_poisson_L1e4': producer_outcome(**at4_inputs), 'poisson_floor': producer_outcome(**floor_inputs),
                 'tier_i_window': producer_outcome(**tier_i_inputs)})
    control('exact_arithmetic_admission', [
        ('float_tau_to_calculator', lambda: calc.certify(tau=1e-08), ()),
        ('bool_parse', parse_q, (True,)),
        ('nan_string', parse_q, ('NaN',)),
        ('float_radius_admission', admit_bound, (float(radius), TARGET)),
        ('zero_denominator', parse_q, ('1/0',)),
    ], note='every Boolean is decided on Fraction or Gaussian-rational values; decimal strings are previews')
    rss_rad = sqrt_bounds(sum((v * v for v in c.values()), Q(0)))[1]
    control('root_n_misuse', [
        ('root_sum_square_of_terms', certify_radius, (c, rss_rad, D, k_value, S0, M0, M1_coef / S0, cpi_lo, arith_c, 'root_sum_square')),
        ('seven_stars_in_quadrature', certify_slope, (2 * sqrt_bounds(Q(7))[1] * calc.STAR_NORM_PER_TAU * ABS_TAU, ABS_TAU,
                                                      GEOM['incident'], 'quadrature')),
    ], rss_radius_preview=sci(rss_rad), linear_radius_preview=sci(radius))
    flags = {name: False for name in UNIVERSAL_FLAGS}
    flags['euclidean_node_certified'] = node_met
    must(validate_claim_flags(flags, node_met), 'claim flags')
    control('no_priority_or_continuum_claim', [
        ('continuum_claim_true', validate_claim_flags, (dict(flags, continuum_claim=True), node_met)),
        ('priority_claim_true', validate_claim_flags, (dict(flags, scientific_priority_verified=True), node_met)),
        ('uniform_wilson_true', validate_claim_flags, (dict(flags, uniform_wilson_claim=True), node_met)),
        ('resolved_shift_true', validate_claim_flags, (dict(flags, resolved_interaction_shift=True), node_met)),
        ('grid_claim_true', validate_claim_flags, (dict(flags, grid_claim=True), node_met)),
        ('node_flag_flipped', validate_claim_flags, (dict(flags, euclidean_node_certified=not node_met), node_met)),
    ])
    K3_double = dict(K3, coef=2 * K3['coef'])
    K3_shifted = {'coef': Q((4 * S0) ** 3) / 2, 'factors': [(CQ(2 * S0), IU, 1), (CQ(2 * S0), -IU, 3)], 'num': [CQ(1)]}
    K_real_pole = {'coef': K3['coef'], 'factors': [(CQ(S0), IU, 1), (CQ(0), CQ(1), 1), (CQ(S0), -IU, 2)], 'num': [CQ(1)]}
    control('kernel_identity_on_support', [
        ('normalization_doubled', certify_kernel_identity, (K3_double, S0)),
        ('poles_swapped_theta_to_minus_theta', certify_kernel_identity, (mirror(K3), S0)),
        ('poles_at_plus_minus_2is', certify_kernel_identity, (K3_shifted, S0)),
        ('real_axis_pole', certify_kernel_identity, (K_real_pole, S0)),
    ], identity='int ghat(theta) e^{i theta x} dtheta = e^{-sx} for every x>=0 (upper residue at theta=is)')
    neg_atom = readout(K3, Q(-1))
    heat_claim = [(S0, Q(1))]
    control('kernel_negative_atom_misread', [
        ('negative_atom_as_heat_value', compare_readout, (K3, Q(-1), heat_claim)),
        ('negative_support_admitted', certify_heat_readout, (K3, Q(-1), heat_claim)),
    ], window_value_at_minus_1=value_text(neg_atom), heat_value_claimed='e^{s}',
        statement='an atom at x=-1 returns g(-1)=e^{-s}(1+2s+2s^2), not e^{s}; nonnegativity (AQ1) is essential')
    control('kernel_l1_and_first_moment', [
        ('signed_integral_as_l1_norm', certify_constant, ('M0', (readout(K3, Q(0))[0][1], 0), (M0, 0))),
        ('probability_kernel_mass_one', certify_constant, ('M0', (Q(1), 0), (M0, 0))),
        ('one_sided_first_moment', certify_constant, ('M1', (M1_coef / 2, -1), (M1_coef, -1))),
        ('first_moment_without_pi', certify_constant, ('M1', (M1_coef, 0), (M1_coef, -1))),
    ], M0=qs(M0), M1='%s/pi' % qs(M1_coef), signed_integral=qs(readout(K3, Q(0))[0][1]))
    control('poisson_kink_divergence', [
        ('poisson_first_moment_finite', certify_first_moment_finite, (family[1]['kernel'], S0)),
        ('poisson_moment_bounded_by_window_M1', certify_poisson_moment_bound, (M1_coef / PI_LO, S0, PI_HI, log10_lo)),
        ('poisson_moment_bounded_by_1e6', certify_poisson_moment_bound, (Q(10 ** 6), S0, PI_HI, log10_lo)),
    ], window_first_moment_finite=family[3]['moments'].get('M1_finite'))
    control('window_linear_in_s', [
        ('M1_independent_of_s', certify_constant, ('M1 at s=2', (Q(4), -1), (Q(lin['2']['M1_times_pi']), -1))),
        ('M1_quadratic_in_s', certify_constant, ('M1 at s=7', (Q(2) * 49, -1), (Q(lin['7']['M1_times_pi']), -1))),
    ], M1_times_pi_over_s={sv: qs(Q(v['M1_times_pi']) / Q(sv)) for sv, v in lin.items()},
        free_exponent='-3s (linear in s)')
    control('local_not_extensive_duhamel', [
        ('extensive_box_2', certify_slope, (2 * boxes['2']['retained_stars'] * calc.STAR_NORM_PER_TAU * ABS_TAU, ABS_TAU, GEOM['incident'], 'triangle', 2)),
        ('extensive_box_3', certify_slope, (2 * boxes['3']['retained_stars'] * calc.STAR_NORM_PER_TAU * ABS_TAU, ABS_TAU, GEOM['incident'], 'triangle', 3)),
    ], retained_stars_by_box={N: v['retained_stars'] for N, v in boxes.items()}, local_slope=qs(k_value))
    zero = calc.certify(tau='0')
    z_costs = {k2: Q(v) for k2, v in zero['costs'].items()}
    pz = poisson_costs(Q(0), Q(0), S0, L4, PI_LO)
    pz_rad = sum(pz.values(), Q(0))
    must(certify_null_replay(z_costs, Q(zero['certified_radius']), 'same_formula', pz, pz_rad, S0, L4, PI_HI), 'null replay')
    pz_dropped = dict(pz, tail=Q(0))
    z_floor = dict(z_costs, kernel_dynamics=pz['tail'])
    control('tau_zero_null_replay', [
        ('window_with_poisson_tail_floor', certify_null_replay, (z_floor, sum(z_floor.values(), Q(0)), 'same_formula', pz, pz_rad, S0, L4, PI_HI)),
        ('poisson_tail_dropped', certify_null_replay, (z_costs, Q(zero['certified_radius']), 'same_formula', pz_dropped, Q(0), S0, L4, PI_HI)),
        ('window_bypass_branch', certify_null_replay, (z_costs, Q(zero['certified_radius']), 'exact_zero_bypass', pz, pz_rad, S0, L4, PI_HI)),
    ], window_radius_tau0=zero['certified_radius'], window_arithmetic_tau0=zero['costs']['arithmetic'],
        poisson_tail_tau0=qs(pz['tail']), poisson_tail_preview=sci(pz['tail']))
    sign_value = readout(mirror(K3), Q(3), calc.FREE_VARIANCE)
    sign_text = re.search(r'returns g\(-3\)/4=(\d+)e\^\{-3\}/4', contract_json['new_control_semantics']['window_fourier_sign_convention'])
    must(sign_text is not None and sign_value == [(-3 * S0, Q(int(sign_text.group(1)), 4))], 'sign-mutation value 25e^{-3}/4')
    control('window_fourier_sign_convention', [
        ('theta_to_minus_theta_free_atom', compare_readout, (mirror(K3), Q(3), free_value)),
        ('theta_to_minus_theta_kernel', certify_kernel_identity, (mirror(K3), S0)),
    ], mutated_readout=value_text(sign_value), correct_readout=value_text(free_value))
    p_fx = Q(1, 10)
    u_fx = CQ(Q(-7, 25), Q(24, 25))
    must(u_fx.abs2() == 1, 'unit-modulus fixture phase')
    tr_dx = p_fx * (u_fx - 1)                        # Tr[(rho-P) diag(1,u)] with rho-P = diag(-p,p)
    trace_norm = 2 * p_fx
    must(tr_dx.abs2() > (trace_norm / 2) ** 2 and tr_dx.abs2() <= trace_norm ** 2, 'non-effect fixture')
    halved = dict(c, state=c['state'] / 2)
    control('state_term_not_effect', [
        ('half_D_on_complex_operator', certify_state_term, ('complex_non_effect', Q(1, 2))),
        ('half_D_in_radius', certify_radius, (halved, sum(halved.values(), Q(0)), D, k_value, S0, M0, M1_coef / S0, cpi_lo, arith_c)),
    ], fixture={'rho_minus_P': 'diag(-1/10,1/10)', 'X': 'diag(1,(-7+24i)/25)', 'abs_trace_squared': qs(tr_dx.abs2()),
                'half_trace_norm_squared': qs((trace_norm / 2) ** 2)}, statement='AT4 F12: W alpha^0_theta(W) is not an effect')
    D_at4_cap = 2 * sqrt_bounds(Q(49, 3) * ABS_TAU)[1]
    control('av1_tier_bound', [
        ('tier_i_value', certify_state_bound, (gv['D_i'], gv['D'], 'av1_gate_tier_ii_forward')),
        ('at4_square_root_bound', certify_state_bound, (D_at4_cap, gv['D'], 'av1_gate_tier_ii_forward')),
        ('reverse_82_face_refinement_switch', certify_state_bound, (gv['D_rev'], gv['D'], 'av1_gate_tier_ii_forward')),
        ('halved_D', certify_state_bound, (D / 2, gv['D'], 'av1_gate_tier_ii_forward')),
        ('unadmitted_provenance', certify_state_bound, (D, gv['D'], 'av1_tier_i')),
    ], bound_D=qs(D), gate_decision_value=qs(gv['D']))
    inventory = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    must(validate_inventory(inventory, contract), 'reverse inputs inventory')
    control('reverse_premise_isolation', [
        ('skeptic_triage_added', validate_inventory, (inventory + ['research/round32/skeptic/triage.md'], contract)),
        ('deliberation_added', validate_inventory, (inventory + ['research/round32/advisor/deliberation-1.md'], contract)),
        ('forward_av2_added', validate_inventory, (inventory + ['research/round32/forward/av2/report.md'], contract)),
        ('premise_missing', validate_inventory, (inventory[1:], contract)),
    ], inventory_size=len(inventory))
    control('c1_window_preview_only', [
        ('kernel_switch_after_D_known', certify_kernel_choice, ('C1_window', 'C2_window', True)),
        ('calculator_c1_certificate', lambda: calc.certify(kernel='C1_window'), ()),
        ('c1_residue_modulus', modulus_kernel, (K2, S0)),
    ], preview_radius=preview['radius_preview'], preview_label=preview['label'])

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in contract['controls'] if cid not in ids]
    must(missing == [], 'contract controls without a check: ' + ','.join(missing))

    result = {
        'loop': 'AV2', 'direction': 'reverse', 'route': 'residues: simple pole at theta=is, triple pole at theta=-is',
        'human_author': 'Hruday N M (BUNZEEY)',
        'contribution_alias': 'HNM-AV2-R reverse residue window-kernel certificate',
        'attribution': {'fourier_residues': 'standard L^1 Fourier inversion and residue calculus (Jordan-type arc bounds, keyhole contour)',
                        'duhamel_and_trace_duality': 'established; AT4 F10-F12 project aliases',
                        'scientific_priority': 'unverified'},
        'contract_snapshot_sha256': contract_sha, 'check_py_sha256': check_py_sha, 'calculator_py_sha256': calculator_sha,
        'model': contract['model'],
        'target': {'quantity': 'radius', 'value': qs(TARGET), 'comparator': '<=', 'read_from': 'contract preregistration.target'},
        'window': {'g': params['window'], 'ghat': 'ghat(theta)=4s^3/(pi(s-i theta)^3(s+i theta))',
                   'modulus': '(4s^3/pi)(s^2+theta^2)^-2', 'g_L1_norm': '8/s', 'regularity': 'C^2, g\'\'\' jumps by -8s^3'},
        'constants': {'M0': qs(M0), 'M1': '4s/pi', 'M2': '2s^2', 'at_s_1': {'M0': qs(M0), 'M1_times_pi': qs(M1_coef), 'M2': qs(M2)}},
        'state_bound': {'D': qs(D), 'preview': sci(D), 'source': GATE_REL + ' decision (tier ii forward)'},
        'duhamel_slope': {'k': qs(k_value), 'preview': sci(k_value), 'stars': 7},
        'certificate': {'+': {'tau': qs(TAU), 'costs': cert['costs'], 'radius': cert['certified_radius'],
                              'radius_preview': cert['radius_preview'], 'datum': cert['certified_datum'],
                              'interval': cert['actual_C_interval'], 'target_met': cert['target_met']},
                        '-': {'tau': params['control_tau'], 'radius': minus['certified_radius'], 'datum': minus['certified_datum'],
                              'role': 'replay at the mirrored coupling'}},
        'retained_failures': {'at4_poisson_L1e4_radius': qs(p_rad), 'at4_poisson_L1e4_preview': sci(p_rad),
                              'poisson_floor_lower': qs(fl['floor_lower']), 'poisson_floor_preview': sci(fl['floor_lower']),
                              'poisson_floor_L_star_bracket': fl['L_star_bracket'],
                              'tier_i_window_radius_preview': sci(E_i)},
        'crossover': {'s_star_bracket': [qs(s_lo), qs(s_hi)], 'preview': sci(s_lo, 8)},
        'c1_window_preview': preview,
        'producer_outcome': outcome,
        'sub_label': 'reference_unresolved',
        'outcome_note': 'proposed for the reverse half only; admission requires the forward route, exchange and the skeptical review',
        'claim_exclusions': contract['claim_exclusions'],
        'checks': CHECKS,
    }
    result.update(flags)
    return result


def main():
    ap = argparse.ArgumentParser(description='HNM-AV2 reverse producer checker (exact arithmetic)')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('check.py: --output must be an absolute path')
    if out.exists():
        raise SystemExit('check.py: --output must be a fresh directory')
    resolved = out.resolve()
    if resolved == ROOT or ROOT in resolved.parents:
        raise SystemExit('check.py: --output must lie outside the checkout')
    result = compute()
    out.mkdir(parents=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    sources = {p.relative_to(HERE).as_posix(): sha256_file(p) for p in sorted(HERE.rglob('*'))
               if p.is_file() and (p.relative_to(HERE).parts[0] == 'inputs' or p.name in ('check.py', 'calculator.py', 'report.md'))
               and p.relative_to(HERE).parts[0] != 'output'}
    manifest = {'loop': 'AV2', 'direction': 'reverse', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AV2', 'direction': 'reverse', 'checks': len(result['checks']),
                      'radius_plus_tau': result['certificate']['+']['radius_preview'],
                      'target_met': result['certificate']['+']['target_met'],
                      'outcome': result['producer_outcome']}, sort_keys=True))


if __name__ == '__main__':
    main()
