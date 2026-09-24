#!/usr/bin/env python3
"""Round32 AV2 skeptic pre-comparison checker (window-kernel certificate).

Written after the AV2 contract freeze from the frozen contract, the AV1 gate and
the premises named in the skeptic brief, before reading
research/round32/forward/av2/ or research/round32/reverse/av2/. Nothing is
imported from any producer. Standard library only. Every admission Boolean is
decided with fractions.Fraction and directed enclosures; floats appear only in
the labelled 'previews' block. Every check and control raises an explicit
exception, so python -O cannot disable it. Model-agent skeptic with correlated
ancestry; not human peer review.

Route (third route, used by neither producer contract): the window transform is
obtained from the annihilating differential operator P(D)=(D+s)(D-s)^(d+1) and
the jump of the first discontinuous derivative at x=0; the moments come from the
substitution theta=s*tan(phi) and exact Wallis integrals, cross-checked by a
directed rational Riemann enclosure.

Usage: python3 -B research/round32/skeptic/av2_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from math import comb, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / 'research/round32/contracts/av2.json'
GATE = ROOT / 'research/round32/advisor/av1-gate.json'
AT4_REPORT = ROOT / 'research/round31/forward/at4/report.md'
CONTRACT_SHA256 = '686458cab7a4e6e65b63f0c6418d51496f66f1aada4897115ff14e8bbfad5687'
DEN = 10 ** 60


class Rejected(Exception):
    """Raised by a validator that refuses a packet; controls require it."""


class CheckFailure(RuntimeError):
    """Raised when a required check or control fails."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise CheckFailure(cid)
    if any(row['id'] == cid for row in CHECKS):
        raise CheckFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def rejects(fn, reason):
    """True iff fn() raises Rejected whose message contains `reason`."""
    try:
        fn()
    except Rejected as exc:
        if reason not in str(exc):
            raise CheckFailure('rejected for the wrong reason: %s (expected %s)' % (exc, reason))
        return True
    return False


def control(cid, mutations, **detail):
    """mutations: list of (label, callable, reason); each must be rejected."""
    rows = []
    for label, fn, reason in mutations:
        if not rejects(fn, reason):
            raise CheckFailure('control %s: mutation %s accepted' % (cid, label))
        rows.append({'mutation': label, 'rejected_for': reason})
    need(True, cid, kind='control', mutations=rows, **detail)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(x):
    return str(x)


def preview(x):
    return format(float(x), '.12e')


def rdown(x, den=DEN):
    return F((x.numerator * den) // x.denominator, den)


def rup(x, den=DEN):
    return F(-((-x.numerator * den) // x.denominator), den)


def fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def dfact(n):
    out = 1
    while n > 1:
        out *= n
        n -= 2
    return out


# ---------------------------------------------------------------- directed enclosures
def arctan_bracket(x, n=64):
    """Alternating series; consecutive partial sums bracket arctan(x), 0<x<1."""
    s = F(0)
    parts = []
    for k in range(n):
        s += F((-1) ** k) * x ** (2 * k + 1) / (2 * k + 1)
        parts.append(s)
    lo, hi = sorted(parts[-2:])
    return lo, hi


def pi_bracket():
    """Hutton: pi = 8 arctan(1/3) + 4 arctan(1/7); Machin used only as a consistency check."""
    a_lo, a_hi = arctan_bracket(F(1, 3))
    b_lo, b_hi = arctan_bracket(F(1, 7))
    lo, hi = rdown(8 * a_lo + 4 * b_lo), rup(8 * a_hi + 4 * b_hi)
    m1_lo, m1_hi = arctan_bracket(F(1, 5))
    m2_lo, m2_hi = arctan_bracket(F(1, 239))
    mlo, mhi = 16 * m1_lo - 4 * m2_hi, 16 * m1_hi - 4 * m2_lo
    if not (lo < hi and max(lo, mlo) <= min(hi, mhi) and hi - lo < F(1, 10 ** 55)):
        raise CheckFailure('pi bracket')
    if not (F(314159265358979, 10 ** 14) < lo < hi < F(314159265358980, 10 ** 14)):
        raise CheckFailure('pi sanity')
    return lo, hi


def exp_pos(x):
    """Directed enclosure of e^x for rational x>=0: halve to x<=1, Taylor with
    geometric remainder, then square with outward rounding."""
    x = F(x)
    if x < 0:
        raise CheckFailure('exp_pos domain')
    r = 0
    while x > 1:
        x /= 2
        r += 1
    n = 52
    s = F(0)
    term = F(1)
    for k in range(n + 1):
        s += term
        term = term * x / (k + 1)
    lo, hi = rdown(s), rup(s + term / (1 - x / (n + 2)))
    for _ in range(r):
        lo, hi = rdown(lo * lo), rup(hi * hi)
    if not (1 <= lo <= hi):
        raise CheckFailure('exp bracket')
    return lo, hi


def exp_neg(x):
    lo, hi = exp_pos(x)
    return rdown(1 / hi), rup(1 / lo)


_LOG2 = []


def log2_bracket(K=200):
    """log 2 = sum_{k>=1} 1/(k 2^k); tail <= 1/((K+1) 2^K)."""
    if not _LOG2:
        s = sum((F(1, k * 2 ** k) for k in range(1, K + 1)), F(0))
        _LOG2.append((s, s + F(1, (K + 1) * 2 ** K)))
    return _LOG2[0]


def log_pos(y):
    """Directed enclosure of log y for rational y>=1 (mantissa by atanh series)."""
    y = F(y)
    if y < 1:
        raise CheckFailure('log domain')
    n = 0
    while y >= 2:
        y /= 2
        n += 1
    z = (y - 1) / (y + 1)
    K = 70
    a = sum((z ** (2 * k + 1) / (2 * k + 1) for k in range(K)), F(0))
    tail = z ** (2 * K + 1) / ((2 * K + 1) * (1 - z * z))
    l2lo, l2hi = log2_bracket()
    return rdown(n * l2lo + 2 * a), rup(n * l2hi + 2 * a + 2 * tail)


def sqrt_bracket(x, scale=10 ** 40):
    x = F(x)
    r = isqrt(x.numerator * scale * scale // x.denominator)
    lo, hi = F(r, scale), F(r + 1, scale)
    if not (lo * lo <= x <= hi * hi):
        raise CheckFailure('sqrt bracket')
    return lo, hi


# ---------------------------------------------------------------- Gaussian rationals
def c_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def c_mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def c_abs2(a):
    return a[0] * a[0] + a[1] * a[1]


def c_inv(a):
    n = c_abs2(a)
    return (a[0] / n, -a[1] / n)


def c_pow(a, n):
    out = (F(1), F(0))
    for _ in range(n):
        out = c_mul(out, a)
    return out


def c_scale(a, x):
    return (a[0] * x, a[1] * x)


def polymul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


# ---------------------------------------------------------------- windows (jump route)
def left_poly(name, s):
    """g(x)=e^{-sx} (x>=0); g(x)=e^{sx} p(x) (x<0).  p coefficients in x."""
    return {'poisson': [F(1)], 'C1': [F(1), -2 * s], 'C2': [F(1), -2 * s, 2 * s * s]}[name]


def p_deriv_at(cs, j, x):
    return sum((cs[i] * F(fact(i), fact(i - j)) * x ** (i - j) for i in range(j, len(cs))), F(0))


def jump_route(name, s):
    """Distributional identity P(D) g = sum_r kappa_r delta^(r), P(D)=(D+s)(D-s)^(d+1)."""
    cs = left_poly(name, s)
    d = len(cs) - 1
    left = [sum((comb(n, j) * s ** (n - j) * p_deriv_at(cs, j, F(0)) for j in range(0, min(n, d) + 1)), F(0))
            for n in range(d + 2)]
    right = [(-s) ** n for n in range(d + 2)]
    J = [right[n] - left[n] for n in range(d + 2)]
    a = polymul([F(1)], [s, F(1)])
    for _ in range(d + 1):
        a = polymul(a, [-s, F(1)])
    # the right branch e^{-sx} is annihilated: P(-s)=0
    if sum((a[n] * (-s) ** n for n in range(len(a))), F(0)) != 0:
        raise CheckFailure('right branch not annihilated')
    # the left branch e^{sx}p(x): e^{-sx}P(D)[e^{sx}p] is a polynomial of degree <=d; zero at d+2 points
    for x in [F(-k, 3) for k in range(1, d + 4)]:
        val = sum((a[n] * sum((comb(n, j) * s ** (n - j) * p_deriv_at(cs, j, x) for j in range(0, min(n, d) + 1)), F(0))
                   for n in range(len(a))), F(0))
        if val != 0:
            raise CheckFailure('left branch not annihilated')
    kappa = [sum((a[n] * J[n - 1 - r] for n in range(r + 1, len(a))), F(0)) for r in range(len(a) - 1)]
    return {'d': d, 'jumps': J, 'operator': a, 'delta_coefficients': kappa, 'poly': cs}


def pi_ghat(route, s, theta):
    """pi*ghat(theta) with ghat=(2pi)^{-1} int g e^{-i theta x}: P(i theta) ghat = kappa_0/(2pi)."""
    a = route['operator']
    it = (F(0), F(theta))
    P = (F(0), F(0))
    for n, an in enumerate(a):
        P = c_add(P, c_scale(c_pow(it, n), an))
    return c_scale(c_inv(P), route['delta_coefficients'][0] / 2)


def closed_form(name, s, theta):
    a = (F(s), -F(theta))  # s - i theta
    b = (F(s), F(theta))   # s + i theta
    if name == 'C2':
        return c_scale(c_inv(c_mul(c_pow(a, 3), b)), 4 * s ** 3)
    if name == 'C1':
        return c_scale(c_inv(c_mul(c_pow(a, 2), b)), 2 * s ** 2)
    return (s / (s * s + theta * theta), F(0))


def half_line_comparator(name, s, theta):
    """Comparator only (the forward contract's route, recomputed here):
    2 pi ghat = 1/(s+i theta) + sum_j c_j (-1)^j j!/(s-i theta)^(j+1)."""
    cs = left_poly(name, s)
    a = (F(s), -F(theta))
    tot = c_inv((F(s), F(theta)))
    for j, cj in enumerate(cs):
        tot = c_add(tot, c_scale(c_inv(c_pow(a, j + 1)), cj * (-1) ** j * fact(j)))
    return c_scale(tot, F(1, 2))


def wallis(a, b):
    """int_0^{pi/2} sin^a cos^b = coef * (pi if pi_pow else 1); None if divergent (b<0)."""
    if b < 0:
        return None
    coef = F(dfact(a - 1) * dfact(b - 1), dfact(a + b))
    if a % 2 == 0 and b % 2 == 0:
        return coef / 2, 1
    return coef, 0


def moments(name):
    """M_j = int |theta|^j |ghat| = (c/pi) s^j W(j, d-j), c = |kappa_0|/s^(d+1).
    Returned symbolically as (coefficient, power of pi, power of s) or None (infinite)."""
    cs_ = []
    for s in (F(1), F(2), F(3, 7)):
        r = jump_route(name, s)
        cs_.append(abs(r['delta_coefficients'][0]) / s ** (r['d'] + 1))
    if len(set(cs_)) != 1:
        raise CheckFailure('kappa_0 not homogeneous in s')
    c = cs_[0]
    d = jump_route(name, F(1))['d']
    out = {}
    for j in range(3):
        w = wallis(j, d - j)
        out[j] = None if w is None else (c * w[0], w[1] - 1, j)
    return out, c, d


def mtext(m):
    if m is None:
        return 'infinity'
    coef, pp, sp = m
    t = q(coef)
    if sp == 1:
        t += 's'
    elif sp > 1:
        t += 's^%d' % sp
    if pp == -1:
        t += '/pi'
    elif pp == 1:
        t += '*pi'
    return t


def riemann_moment(j, T=64):
    """Directed enclosure of int_0^inf u^j (1+u^2)^{-2} du, j=0,1,2 (s=1)."""
    lo = hi = F(0)
    for a0, b0, h in ((F(0), F(4), F(1, 1024)), (F(4), F(T), F(1, 128))):
        n = int((b0 - a0) / h)
        for i in range(n):
            a = a0 + i * h
            b = a + h
            lo += rdown(a ** j / (1 + b * b) ** 2 * h, 10 ** 30)
            hi += rup(b ** j / (1 + a * a) ** 2 * h, 10 ** 30)
    Tq = F(T)
    tail_hi = Tq ** (j - 3) / (3 - j)
    tail_lo = tail_hi / (1 + 1 / (Tq * Tq)) ** 2
    return lo + tail_lo, hi + tail_hi


# ---------------------------------------------------------------- model geometry
def coarse(v):
    return (v[0] // 4, v[1] // 2, v[2])


def factor_links(b):
    out = []
    for r in range(4):
        for qq in range(2):
            tail = (4 * b[0] + r, 2 * b[1] + qq, b[2])
            for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                out.append((tail, e))
    return out


# ---------------------------------------------------------------- AV1 formula (admitted tier ii)
def D_tier_ii(tau):
    """AV1 forward tier (ii): t1=49|tau|/144, J=28|tau|, T=t1/(1-352J), eps=2T+T^2, D=2eps(1+eps)/(1+eps^2)."""
    t = abs(F(tau))
    t1 = F(49, 144) * t
    T = t1 / (1 - 352 * 28 * t)
    eps = 2 * T + T * T
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def D_tier_i():
    t = F(37, 6250000)
    eps = 2 * t + t * t
    return 2 * eps * (1 + eps) / (1 + eps * eps)


# ---------------------------------------------------------------- validators
def exact(value, name):
    if isinstance(value, bool) or isinstance(value, float):
        raise Rejected('exact arithmetic: %s is not an exact rational' % name)
    if isinstance(value, F):
        return value
    if isinstance(value, int):
        return F(value)
    if isinstance(value, str) and re.fullmatch(r'[+-]?[0-9]+(/[0-9]+)?', value):
        return F(value)
    raise Rejected('exact arithmetic: %s must be an integer or numerator/denominator text' % name)


def validate_certificate(p, truth):
    """Recompute the AV2 window certificate packet from the frozen contract data."""
    for key in ('tau', 's', 'D', 'k', 'M0', 'M1_over_s', 'state', 'mean_square', 'kernel_dynamics', 'arithmetic', 'radius'):
        exact(p[key], key)
    if p['kernel'] != 'C2':
        raise Rejected('kernel switch: the certificate kernel is the frozen C2 window')
    if (F(p['tau']) != truth['tau'] and F(p['tau']) != -truth['tau']) or F(p['s']) != truth['s'] \
            or [F(x) for x in p['triple']] != [F(0)] * 3 or p['reference'] != 'haar' or p['model_id'] != truth['model_id']:
        raise Rejected('model changed or relabelled')
    if p['stars'] != truth['stars']:
        raise Rejected('incident stars: seven whole stars meet R')
    if p['cover'] != (48, 36):
        raise Rejected('cover: 48 links and 36 endpoints')
    if p['clock_exponent'] != 3:
        raise Rejected('clock: s=alpha*t_E/hbar gives exponent 3')
    if p['centering'] != 'vector':
        raise Rejected('centering: vector centering required')
    if p['spectral_support'] != 'nonnegative (AQ1)':
        raise Rejected('negative support: window identity needs AQ1 nonnegativity')
    if p['free_atom'] != 'g(3)/4':
        raise Rejected('sign convention: free atom must read g(3)/4')
    if F(p['D']) != truth['D']:
        raise Rejected('av1 tier: D differs from the contract-bound admitted tier-(ii) value')
    if F(p['k']) != truth['k']:
        raise Rejected('duhamel slope: k must be the local seven-star value 49|tau|/4')
    if F(p['M0']) != 2:
        raise Rejected('L1 norm: ||ghat||_1=2 (not |int ghat|=g(0)=1)')
    if F(p['M1_over_s']) != 4 or p['M1_pi_power'] != -1:
        raise Rejected('first moment: int|theta||ghat|=4s/pi')
    if F(p['state']) != 2 * truth['D'] * p['state_factor'] or p['state_factor'] != 1:
        raise Rejected('state term is not an effect: no D/2 refinement on W alpha0_theta(W)')
    if F(p['mean_square']) != 2 * truth['D'] ** 2:
        raise Rejected('mean square not charged as M0*D^2')
    if p['combination'] != 'linear':
        raise Rejected('root-N: deterministic terms add linearly')
    kd = F(p['kernel_dynamics'])
    if kd != truth['k'] * 4 * F(p['s']) / truth['pi_lo']:
        raise Rejected('kernel dynamics must be k*4s/pi with the lower pi endpoint')
    if F(p['radius']) != F(p['state']) + F(p['mean_square']) + kd + F(p['arithmetic']) or F(p['arithmetic']) != truth['arithmetic']:
        raise Rejected('radius mismatch')
    for key in ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified', 'grid_claim'):
        if p['claims'][key] is not False:
            raise Rejected('forbidden claim ' + key)
    return True


def validate_scaling(claim, lo, hi):
    band = {'linear': (F(99), F(101)), 'sqrt': (F(99, 10), F(101, 10))}[claim]
    if not (band[0] <= lo and hi <= band[1]):
        raise Rejected('tau scaling: ratio outside the %s band' % claim)
    return True


def validate_retained(block, target):
    for key in ('at4_L_1e4', 'optimized_floor_D0', 'poisson_with_admitted_D'):
        row = block.get(key)
        if row is None or row.get('verdict') != 'insufficient' or not F(row['lower']) > target:
            raise Rejected('insufficient verdict retained: ' + key)
    return True


def validate_tau_zero(window_radius, window_arith, poisson_radius, poisson_tail_lower):
    if window_radius != window_arith:
        raise Rejected('tau zero: window radius must equal the arithmetic term')
    if poisson_radius < poisson_tail_lower:
        raise Rejected('Poisson tail at tau=0 must be kept')
    return True


def validate_support_identity(poly_on_nonnegative):
    if poly_on_nonnegative != [F(1)]:
        raise Rejected('window not equal to e^{-sx} on the support')
    return True


def validate_measure_support(atoms):
    if any(x < 0 for x, _ in atoms):
        raise Rejected('negative support: identity C(s)=int ghat c fails off [0,inf)')
    return True


def validate_poisson_moment(m1):
    if m1 != 'infinity':
        raise Rejected('Poisson first moment diverges')
    return True


def validate_linear_in_s(m1_fn):
    vals = [m1_fn(s) / s for s in (F(1, 2), F(1), F(2))]
    if len(set(vals)) != 1:
        raise Rejected('window first moment must be linear in s')
    return True


def validate_local_slope(k_by_N):
    if len(set(k_by_N.values())) != 1:
        raise Rejected('extensive Duhamel: slope must not depend on the box')
    return True


def validate_kernel_role(name, role):
    if name != 'C2' and role != 'preview_only':
        raise Rejected('kernel switch: C1 window is preview-only')
    if name == 'C2' and role != 'certificate':
        raise Rejected('kernel role')
    return True


def validate_reverse_inventory(inv, contract):
    expected = {'AGENTS.md', 'research/round32/contracts/av2.json'} | set(contract['shared_premises'])
    forbidden = re.compile(r'(skeptic/triage\.md|skeptic/loop2-response\.md|skeptic/av2|deliberation-\d+\.md|'
                           r'experts/[^/]+/loop2-response\.md|forward/av2/|reverse/av2/)')
    bad = [x for x in inv if forbidden.search(x)]
    if bad:
        raise Rejected('reverse premise isolation: forbidden input ' + bad[0])
    if set(inv) != expected:
        raise Rejected('reverse premise isolation: inventory differs from AGENTS.md+contract+shared_premises')
    return True


def validate_claims(flags):
    for key, val in flags.items():
        if val is not False:
            raise Rejected('forbidden claim ' + key)
    return True


def validate_evidence(evidence, required):
    body = json.dumps(evidence['rows'], sort_keys=True)
    if hashlib.sha256(body.encode()).hexdigest() != evidence['digest']:
        raise Rejected('evidence digest mismatch')
    have = {r['id']: r for r in evidence['rows']}
    for cid in required:
        if cid not in have:
            raise Rejected('missing required control ' + cid)
        if have[cid]['passed'] is not True:
            raise Rejected('required control not passed ' + cid)
    return True


def validate_centering(kind, m, d, residue):
    truth = {'vector': d * d, 'scalar': -2 * m * d - d * d, 'uncentered': m * m}[kind]
    if residue != truth:
        raise Rejected('centering residue')
    if kind != 'vector':
        raise Rejected('centering: vector centering required')
    return True


def calculator(tau='1/100000000', s='1', selected=('0', '0', '0'), pi=None, D_fn=D_tier_ii):
    """Skeptic comparator for the producers' item-8 calculator (proved domain only)."""
    tau = exact(tau, 'tau')
    s = exact(s, 's')
    sel = [exact(x, 'selected') for x in selected]
    if any(sel):
        raise Rejected('domain: selected triple must be zero')
    if abs(tau) > F(1, 10 ** 8):
        raise Rejected('domain: |tau|<=10^-8')
    if s <= 0:
        raise Rejected('domain: s>0')
    pi_lo, _ = pi
    D = D_fn(tau)
    k = F(49, 4) * abs(tau)
    f_lo, f_hi = exp_neg(3 * s)
    f_lo, f_hi = f_lo / 4, f_hi / 4
    terms = {'state': 2 * D, 'mean_square': 2 * D * D, 'kernel_dynamics': k * 4 * s / pi_lo,
             'arithmetic': (f_hi - f_lo) / 2}
    return terms, sum(terms.values(), F(0)), (f_lo + f_hi) / 2, (f_lo, f_hi)


# ---------------------------------------------------------------- main computation
def execute():
    contract_bytes = CONTRACT.read_bytes()
    need(hashlib.sha256(contract_bytes).hexdigest() == CONTRACT_SHA256, 'contract_sha256_bound')
    contract = json.loads(contract_bytes)
    par = contract['parameters']
    need(contract['status'] == 'frozen_before_production' and contract['id'] == 'AV2', 'contract_frozen')
    tau = F(par['tau'])
    tau_c = F(par['control_tau'])
    s1 = F(par['s'])
    target = F(par['absolute_target'])
    triple = [F(x) for x in par['selected_coefficients_over_alpha']]
    need(tau == F(1, 10 ** 8) and tau_c == -tau and s1 == 1 and target == F(1, 10 ** 6) and triple == [0, 0, 0]
         and F(contract['preregistration']['target']['value']) == target, 'contract_parameters_read')
    mD = re.search(r'D = (\d+)/(\d+)', par['state_bound'])
    D = F(int(mD.group(1)), int(mD.group(2)))

    # ---------------- AV1 gate binding
    gate_bytes = GATE.read_bytes()
    gate = json.loads(gate_bytes)
    g_ii = re.search(r'D_ii=(\d+/\d+)', gate['accepted'])
    g_i = re.search(r'D_i=(\d+/\d+)', gate['accepted'])
    g_rev = re.search(r'D_ii<=(\d+)/10\^40', gate['accepted'])
    D_gate = F(g_ii.group(1))
    D_i = F(g_i.group(1))
    D_rev = F(int(g_rev.group(1)), 10 ** 40)
    need(gate['verdict'] == 'accepted_within_scope' and D_gate == D and g_ii.group(1) in gate['decision'],
         'av1_gate_binds_contract_D')
    need(D_tier_ii(tau) == D and D_tier_ii(tau_c) == D, 'av1_formula_reproduces_D_both_signs',
         note='AV1 forward tier (ii) formula recomputed here; -tau is the same |tau| formula')
    need(D_tier_i() == D_i and D_i > 1000 * D and D_rev < D, 'av1_other_values_identified',
         D_i=q(D_i), D_ii_reverse_labelled=q(D_rev))

    pi_lo, pi_hi = pi_bracket()
    e_lo, e_hi = exp_pos(1)
    need(F(2718281828459045, 10 ** 15) < e_lo < e_hi < F(2718281828459046, 10 ** 15), 'exp_bracket_sanity')

    # ---------------- kernel by the jump route
    kern = {}
    for name in ('C2', 'C1', 'poisson'):
        mom, c, d = moments(name)
        r1 = jump_route(name, F(1))
        kern[name] = {'moments': mom, 'c': c, 'd': d, 'jumps_s1': r1['jumps'], 'kappa_s1': r1['delta_coefficients']}
        for s in (F(1), F(1, 2), F(3)):
            r = jump_route(name, s)
            J = r['jumps']
            if any(J[n] != 0 for n in range(d + 1)) or J[d + 1] == 0:
                raise CheckFailure('smoothness class ' + name)
            if any(r['delta_coefficients'][k] != 0 for k in range(1, len(r['delta_coefficients']))):
                raise CheckFailure('higher delta terms ' + name)
            if r['delta_coefficients'][0] != J[d + 1]:
                raise CheckFailure('delta coefficient ' + name)
            for th in (F(0), F(1, 3), F(1), F(-2), F(7, 2), F(10), F(-25, 4)):
                g1 = pi_ghat(r, s, th)
                if g1 != closed_form(name, s, th) or g1 != half_line_comparator(name, s, th):
                    raise CheckFailure('transform mismatch ' + name)
                if c_abs2(g1) != (r['delta_coefficients'][0] / 2) ** 2 / (s * s + th * th) ** (d + 2):
                    raise CheckFailure('modulus ' + name)
            # pi*ghat(0) = (1/2) int g, with int g = 1/s + sum_j c_j (-1)^j j!/s^(j+1)
            intg = 1 / s + sum((cj * (-1) ** j * fact(j) / s ** (j + 1) for j, cj in enumerate(left_poly(name, s))), F(0))
            if pi_ghat(r, s, F(0)) != (intg / 2, F(0)):
                raise CheckFailure('ghat(0) ' + name)
    c2 = kern['C2']
    need(c2['d'] == 2 and c2['jumps_s1'] == [0, 0, 0, -8] and c2['kappa_s1'][0] == -8,
         'C2_jump_route_transform', jump_g3='-8s^3', smoothness='C^2, jump in g\'\'\' only',
         transform='pi*ghat = 4s^3/((s-i theta)^3 (s+i theta)) at 21 (s,theta) pairs; equals half-line comparator')
    need(kern['C1']['jumps_s1'] == [0, 0, 4] and kern['poisson']['jumps_s1'] == [0, -2],
         'C1_and_poisson_jump_route', C1_transform='2s^2/(pi(s-i theta)^2(s+i theta))', poisson_transform='s/(pi(s^2+theta^2))',
         poisson_kink_jump_g_prime='-2s')
    mom = {name: {str(j): mtext(kern[name]['moments'][j]) for j in range(3)} for name in kern}
    need(mom['C2'] == {'0': '2', '1': '4s/pi', '2': '2s^2'}, 'C2_moments_wallis', moments=mom['C2'])
    need(mom['C1'] == {'0': '4/pi', '1': '4s/pi', '2': 'infinity'}, 'C1_moments_wallis', moments=mom['C1'])
    need(mom['poisson'] == {'0': '1', '1': 'infinity', '2': 'infinity'}, 'poisson_moments_wallis', moments=mom['poisson'])
    wt = par['window_transform']
    parsed = {'0': re.search(r'\|\|ghat\|\|_1=([^,]+)', wt).group(1).strip(),
              '1': re.search(r'int\|theta\|\|ghat\|=([^,]+)', wt).group(1).strip(),
              '2': re.search(r'int theta\^2\|ghat\|=([^,]+)', wt).group(1).strip()}
    need(parsed == mom['C2'] and '4s^3/(pi(s-i theta)^3(s+i theta))' in wt and '(4s^3/pi)(s^2+theta^2)^-2' in wt,
         'contract_constants_match_derivation', contract_text=parsed)
    need('e^{-sx} for x>=0' in par['window'] and 'e^{sx}(1-2sx+2s^2x^2) for x<0' in par['window'], 'contract_window_text')

    # directed quadrature cross-check (s=1): M_j = (8/pi) I_j
    quad = {}
    wal = {0: (pi_lo / 4, pi_hi / 4), 1: (F(1, 2), F(1, 2)), 2: (pi_lo / 4, pi_hi / 4)}
    for j in range(3):
        lo, hi = riemann_moment(j)
        if not (lo <= wal[j][0] and wal[j][1] <= hi):
            raise CheckFailure('quadrature does not contain Wallis value')
        quad[str(j)] = {'I_lower': q(rdown(lo, 10 ** 12)), 'I_upper': q(rup(hi, 10 ** 12)),
                        'M_lower': q(rdown(8 * lo / pi_hi, 10 ** 12)), 'M_upper': q(rup(8 * hi / pi_lo, 10 ** 12))}
    need(F(quad['0']['M_lower']) > F(199, 100) and F(quad['0']['M_upper']) < F(201, 100)
         and F(quad['2']['M_lower']) > F(199, 100) and F(quad['2']['M_upper']) < F(201, 100)
         and F(quad['1']['M_lower']) > F(127, 100) and F(quad['1']['M_upper']) < F(1277, 1000), 'moments_directed_quadrature',
         enclosures=quad, method='cells [0,4] h=1/1024 and [4,64] h=1/128, monotone numerator/denominator bounds, tail in [T^(j-3)/((3-j)(1+T^-2)^2), T^(j-3)/(3-j)]')

    # ---------------- model geometry and Duhamel slope
    R = [(0, 0, 0), (0, 0, 1)]
    S = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    anchors = sorted({(r[0] - v[0], r[1] - v[1], r[2] - v[2]) for r in R for v in S})
    orthant = [b for b in anchors if min(b) >= 0]
    links = [l for b in R for l in factor_links(b)]
    ends = {l[0] for l in links} | {tuple(l[0][i] + l[1][i] for i in range(3)) for l in links}
    wilson = [((0, 0, 0), (1, 0, 0)), ((1, 0, 0), (0, 0, 1)), ((0, 0, 1), (1, 0, 0)), ((0, 0, 0), (0, 0, 1))]
    owners = [coarse(l[0]) for l in wilson]
    need(len(anchors) == 7 and len(orthant) == 2 and len(links) == 48 and len(ends) == 36
         and owners == [(0, 0, 0), (0, 0, 0), (0, 0, 1), (0, 0, 0)] and all(l in links for l in wilson), 'cover_and_stars',
         incident_anchors=[list(a) for a in anchors], orthant_count=2, cover_links=48, cover_endpoints=36)
    star_norm = 21 * abs(tau) / 3 / 8          # 21 faces, |tau|/3 each (delta units), /8 to G=H/alpha
    B = len(anchors) * star_norm
    k = 2 * B
    need(star_norm == F(7, 8) * abs(tau) and B == F(49, 8) * abs(tau) and k == F(49, 4) * abs(tau)
         and '49|tau|/4' in par['duhamel_slope'] and '49|tau|/8' in par['duhamel_slope'], 'duhamel_slope_k',
         k=q(k), B_norm=q(B), stars=7)
    k_ext = {N: 2 * (2 * N) ** 3 * star_norm for N in (2, 3, 4)}

    # ---------------- radius at the cap
    f_lo, f_hi = exp_neg(3 * s1)
    f_lo, f_hi = f_lo / 4, f_hi / 4
    datum = (f_lo + f_hi) / 2
    arith = (f_hi - f_lo) / 2
    truth = {'tau': tau, 's': s1, 'D': D, 'k': k, 'pi_lo': pi_lo, 'arithmetic': arith, 'stars': 7,
             'model_id': contract['preregistration']['model_id']}
    radii = {}
    for label, t in (('plus', tau), ('minus', tau_c)):
        Dt = D_tier_ii(t)
        kt = F(49, 4) * abs(t)
        terms = {'state': 2 * Dt, 'mean_square': 2 * Dt * Dt, 'kernel_dynamics': kt * 4 * s1 / pi_lo, 'arithmetic': arith}
        rad = sum(terms.values(), F(0))
        radii[label] = (terms, rad)
    terms, radius = radii['plus']
    need(radii['minus'][1] == radius and radii['minus'][0] == terms, 'minus_tau_is_replay',
         note='same |tau| formula: a replay of the certificate at the mirrored coupling, not a second confirmation')
    kd_lo = k * 4 * s1 / pi_hi
    lo_int, hi_int = datum - radius, datum + radius
    need(radius <= target and lo_int <= f_lo and f_hi <= hi_int, 'radius_meets_target_reference_inside',
         radius=q(radius), target=q(target), sub_label='reference_unresolved')
    packet = {'tau': tau, 's': s1, 'triple': ['0', '0', '0'], 'reference': 'haar', 'model_id': truth['model_id'],
              'kernel': 'C2', 'stars': 7, 'cover': (48, 36), 'clock_exponent': 3, 'centering': 'vector',
              'spectral_support': 'nonnegative (AQ1)', 'free_atom': 'g(3)/4', 'D': D, 'k': k, 'M0': F(2),
              'M1_over_s': F(4), 'M1_pi_power': -1, 'state_factor': 1, 'state': terms['state'],
              'mean_square': terms['mean_square'], 'kernel_dynamics': terms['kernel_dynamics'],
              'arithmetic': terms['arithmetic'], 'radius': radius, 'combination': 'linear',
              'claims': {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
                         'scientific_priority_verified': False, 'grid_claim': False}}
    need(validate_certificate(packet, truth), 'certificate_packet_validates')
    ctau, crad, cdat, _ = calculator(pi=(pi_lo, pi_hi))
    need(crad == radius and cdat == datum and calculator(tau='-1/100000000', pi=(pi_lo, pi_hi))[1] == radius,
         'calculator_comparator_reproduces')

    # ---------------- crossover s*
    X = (target - 2 * (D + D * D)) / (49 * abs(tau))
    s_lo = rdown(pi_lo * X, 10 ** 12) - F(1, 10 ** 12)
    s_hi = rup(pi_hi * X, 10 ** 12)
    _, rad_slo, _, _ = calculator(s=s_lo, pi=(pi_lo, pi_hi))
    E_lo_shi = 2 * (D + D * D) + 49 * abs(tau) * s_hi / pi_hi
    need(rad_slo <= target and E_lo_shi >= target and F(61, 10) < s_lo < s_hi < F(63, 10), 's_star_enclosure',
         s_star_lower=q(s_lo), s_star_upper=q(s_hi),
         note='crossover of E(s)=2(D+D^2)+49|tau|s/pi only; no node other than s=1 is certified')
    s0_lo, s0_hi = rdown(100 * pi_lo / 49, 10 ** 12), rup(100 * pi_hi / 49, 10 ** 12)
    fs_lo, fs_hi = exp_neg(3 * s_hi)
    need(fs_hi / 4 < target / 100, 'free_value_at_s_star_below_radius', free_upper_at_s_star=q(rup(fs_hi / 4, 10 ** 15)))

    # ---------------- retained Poisson controls
    Da_lo, Da_hi = sqrt_bracket(F(49, 3) * abs(tau))
    Da_lo, Da_hi = 2 * Da_lo, 2 * Da_hi
    L4 = F(10 ** 4)
    lg_lo, lg_hi = log_pos(1 + L4 * L4 / (s1 * s1))
    at4_hi = Da_hi + Da_hi ** 2 + k * s1 * lg_hi / pi_lo + (F(1, 2) + Da_hi / 2) * 2 * s1 / (pi_lo * L4)
    at4_lo = Da_lo + Da_lo ** 2 + k * s1 * lg_lo / pi_hi + (F(1, 2) + Da_lo / 2) * 2 * s1 / (pi_hi * L4)
    rep = re.search(r'mathcal E\^\+≈(0\.[0-9]+)', AT4_REPORT.read_text()).group(1)
    need(at4_lo - F(1, 10 ** 18) <= F(rep) <= at4_hi + F(1, 10 ** 18) and at4_lo > target, 'poisson_at4_L1e4_retained',
         lower=q(rdown(at4_lo, 10 ** 30)), upper=q(rup(at4_hi, 10 ** 30)), at4_report_decimal=rep, verdict='insufficient')
    # all-L lower bound: log(1+L^2/s^2) >= 2 log(L/s) gives F(L) >= phi(L), min at L=1/(2k)
    y = 1 / (2 * k * s1)
    ly_lo, _ = log_pos(y)
    floor_lo = 2 * k * s1 * (1 + ly_lo) / pi_hi
    Lr = F(4081633)
    lr_lo, lr_hi = log_pos(1 + Lr * Lr / (s1 * s1))
    floor_hi = k * s1 * lr_hi / pi_lo + s1 / (pi_lo * Lr)
    need(target < floor_lo <= floor_hi, 'poisson_optimized_floor_retained', lower_all_L=q(rdown(floor_lo, 10 ** 30)),
         upper_at_L_4081633=q(rup(floor_hi, 10 ** 30)), L_star='1/(2k)=' + q(y), verdict='insufficient',
         note='D->0, forward tail (1/2)(2s/(pi L)); lower bound holds for every L>0')
    withD_lo = D + D * D + floor_lo
    need(withD_lo > target, 'poisson_with_admitted_D_insufficient', lower_all_L=q(rdown(withD_lo, 10 ** 30)),
         verdict='insufficient', note='the admitted D alone does not rescue the Poisson kernel; the window is needed')
    retained = {'at4_L_1e4': {'verdict': 'insufficient', 'lower': q(rdown(at4_lo, 10 ** 30))},
                'optimized_floor_D0': {'verdict': 'insufficient', 'lower': q(rdown(floor_lo, 10 ** 30))},
                'poisson_with_admitted_D': {'verdict': 'insufficient', 'lower': q(rdown(withD_lo, 10 ** 30))}}
    need(validate_retained(retained, target), 'retained_block_validates')
    # divergent Poisson first moment: P1(L)=(s/pi)log(1+L^2/s^2) against the window's 4s/pi
    l65_lo, _ = log_pos(65)
    _, l50_hi = log_pos(50)
    p1 = {}
    for L in (8, 10 ** 4, 10 ** 8, 10 ** 16):
        a_, b_ = log_pos(1 + F(L) ** 2)
        p1[str(L)] = {'lower': q(rdown(a_ / pi_hi, 10 ** 12)), 'upper': q(rup(b_ / pi_lo, 10 ** 12))}
    need(l65_lo > 4 and l50_hi < 4 and F(p1[str(10 ** 16)]['lower']) > 23, 'poisson_first_moment_divergent',
         truncated_first_moment=p1, window_first_moment='4s/pi (finite, all L)',
         crossing='P1(8)>4/pi>P1(7) at s=1', divergence='P1(L)>=(2s/pi)log(L/s), unbounded')

    # ---------------- fixtures
    g3 = F(1)                                      # g(3)=e^{-3s}: x=3 lies on the support branch
    p_m3 = sum((cj * F(-3) ** j for j, cj in enumerate(left_poly('C2', s1))), F(0))
    p1_m3 = sum((cj * F(-3) ** j for j, cj in enumerate(left_poly('C1', s1))), F(0))
    p_m1 = sum((cj * F(-1) ** j for j, cj in enumerate(left_poly('C2', s1))), F(0))
    p1_m1 = sum((cj * F(-1) ** j for j, cj in enumerate(left_poly('C1', s1))), F(0))
    need(p_m3 == 25 and p1_m3 == 7 and p_m1 == 5 and p1_m1 == 3 and g3 == 1, 'window_values_off_support',
         C2_g_minus3='25e^{-3}', C1_g_minus3='7e^{-3}', C2_g_minus1='5/e', C1_g_minus1='3/e')
    sign_mut = (25 * f_lo, 25 * f_hi)
    need(sign_mut[0] > f_hi, 'sign_convention_fixture', mutated_free_atom_lower=q(rdown(sign_mut[0], 10 ** 30)),
         correct_free_atom_upper=q(rup(f_hi, 10 ** 30)),
         note='theta->-theta conjugates ghat: |ghat|, M0, M1, M2 and E are unchanged; only the datum exposes it')
    em1_lo, em1_hi = exp_neg(1)
    need(5 * em1_hi < e_lo and em1_hi < e_lo and 5 * em1_lo > em1_hi, 'negative_atom_fixture',
         window_reads='5/e', true_value='e', poisson_reads='1/e', atom='x=-1 weight 1, s=1')
    # effect refinement is not available for the complex operator W alpha0_theta(W): 2x2 toy (labelled)
    u = (F(3, 5), F(4, 5))                          # e^{3 i theta} on a rational point of the unit circle
    Dt = F(1)
    tr = c_add(c_scale(u, Dt / 2), c_scale((u[0], -u[1]), -Dt / 2))
    need(c_abs2(u) == 1 and c_abs2(tr) == F(16, 25) * Dt * Dt and c_abs2(tr) > (Dt / 2) ** 2, 'complex_state_term_toy',
         value='|Tr(Delta A)|=4||Delta||_1/5 > ||Delta||_1/2', toy='A=W e^{i theta G0} W e^{-i theta G0}=diag(u,conj u), W=X, G0=diag(0,3)')

    # ---------------- previews and C1 (preview-only)
    c1_rad = (4 / pi_lo) * (D + D * D) + k * 4 * s1 / pi_lo + arith
    c1_sstar = (pi_lo * target - 4 * (D + D * D)) / (49 * abs(tau))
    c1 = {'role': 'preview_only', 'M0': '4/pi', 'M1': '4s/pi', 'M2': 'infinity', 'negative_atom_value': '3/e',
          'sign_mutation_value': '7e^{-3}/4', 'radius_preview_upper': q(rup(c1_rad, 10 ** 30)),
          'crossover_preview_lower': q(rdown(c1_sstar, 10 ** 9)),
          'note': 'a kernel switch after D is known is rejected; C2 is the certificate kernel (finite M2)'}
    need(validate_kernel_role('C1', 'preview_only') and c1_rad < radius, 'c1_preview_computed_labelled',
         radius_preview_upper=c1['radius_preview_upper'])

    # ---------------- tau scaling
    def E_bounds(t, Dfun):
        Dv = Dfun(t)
        base = 2 * (Dv + Dv * Dv)
        return base + 49 * abs(t) / pi_hi, base + 49 * abs(t) / pi_lo
    a_lo, a_hi = E_bounds(tau, D_tier_ii)
    b_lo, b_hi = E_bounds(tau / 100, D_tier_ii)
    ratio = (a_lo / b_hi, a_hi / b_lo)

    def D_sqrt(t):
        return 2 * sqrt_bracket(F(49, 3) * abs(t))[1]
    sa_lo, sa_hi = E_bounds(tau, D_sqrt)
    sb_lo, sb_hi = E_bounds(tau / 100, D_sqrt)
    ratio_sqrt = (sa_lo / sb_hi, sa_hi / sb_lo)

    # ---------------- tau = 0 null replay
    t0_terms, t0_rad, _, _ = calculator(tau='0', pi=(pi_lo, pi_hi))
    L9 = F(10 ** 9)
    poisson0_tail_lo = s1 / (pi_hi * L9)
    poisson0 = F(0) + F(0) + 0 + s1 / (pi_lo * L9) + arith

    # ---------------- controls (all 24 contract ids)
    def mut(**changes):
        p = dict(packet)
        p['claims'] = dict(packet['claims'])
        for key, val in changes.items():
            if key in p['claims']:
                p['claims'][key] = val
            else:
                p[key] = val
        return lambda: validate_certificate(p, truth)

    control('missing_incoming_stars', [('orthant_two_stars', mut(stars=2, k=F(14, 4) * abs(tau)), 'incident stars')],
            derived_anchors=7, orthant=2)
    control('full_original_wilson_cover', [('four_displayed_links', mut(cover=(4, 4)), 'cover'),
                                           ('endpoints_44', mut(cover=(48, 44)), 'cover')], links=48, endpoints=36)
    control('wrong_delta_alpha_hbar_clock', [('normalized_exponent_24', mut(clock_exponent=24), 'clock'),
                                             ('u_equals_s_over_8', mut(s=F(1, 8)), 'model changed')],
            fixture='alpha=2, hbar=3, t_E=3/2 gives s=1; u=s/8 is the AQ normalized clock')
    need(F(2) * F(3, 2) / F(3) == 1, 'nonunit_clock_fixture')
    control('vector_versus_scalar_centering',
            [('scalar_subtraction', lambda: validate_centering('scalar', F(1, 4), F(1, 100), F(-51, 10000)), 'centering'),
             ('uncentered', lambda: validate_centering('uncentered', F(1, 4), F(1, 100), F(1, 16)), 'centering'),
             ('packet_scalar', mut(centering='scalar'), 'centering')],
            vector_residue='1/10000', scalar_residue='-51/10000', uncentered_residue='1/16')
    control('first_order_mean_charged', [('mean_square_zero', mut(mean_square=F(0), radius=radius - terms['mean_square']), 'mean square'),
                                         ('mean_square_without_M0', mut(mean_square=D * D, radius=radius - D * D), 'mean square')],
            note='AV1 gives only |m|<=D; a first-order mean is not excluded, so m^2<=D^2 is charged')
    control('tau_scaling_exponent', [('sqrt_bound_called_linear', lambda: validate_scaling('linear', *ratio_sqrt), 'tau scaling')],
            linear_ratio=[q(rdown(ratio[0], 10 ** 9)), q(rup(ratio[1], 10 ** 9))],
            sqrt_ratio=[q(rdown(ratio_sqrt[0], 10 ** 9)), q(rup(ratio_sqrt[1], 10 ** 9))])
    need(validate_scaling('linear', *ratio) and validate_scaling('sqrt', *ratio_sqrt), 'tau_scaling_bands')
    control('changed_model_relabelled', [('tau_1e-14', mut(tau=F(1, 10 ** 14)), 'model changed'),
                                         ('s_half', mut(s=F(1, 2)), 'model changed'),
                                         ('nonzero_triple', mut(triple=['0', '1/8', '0']), 'model changed'),
                                         ('selected_reference', mut(reference='selected'), 'model changed'),
                                         ('finite_graph_id', mut(model_id='FG(one_plaquette)'), 'model changed')])
    control('insufficient_verdict_retained',
            [('floor_relabelled_met', lambda: validate_retained(dict(retained, optimized_floor_D0={'verdict': 'met', 'lower': retained['optimized_floor_D0']['lower']}), target), 'insufficient verdict retained'),
             ('at4_dropped', lambda: validate_retained({k_: v for k_, v in retained.items() if k_ != 'at4_L_1e4'}, target), 'insufficient verdict retained')])
    control('exact_arithmetic_admission', [('float_D', mut(D=float(D)), 'exact arithmetic'),
                                           ('decimal_radius', mut(radius='1.832e-7'), 'exact arithmetic')])
    control('root_n_misuse', [('rss_combination', mut(combination='root_sum_square'), 'root-N'),
                              ('divide_by_64', mut(radius=radius / 64), 'radius mismatch')])
    control('no_priority_or_continuum_claim', [(key, mut(**{key: True}), 'forbidden claim ' + key)
                                               for key in ('continuum_claim', 'scientific_priority_verified',
                                                           'resolved_interaction_shift', 'uniform_wilson_claim', 'grid_claim')])
    control('kernel_identity_on_support', [('mirrored_branches', lambda: validate_support_identity([F(1), 2 * s1, 2 * s1 * s1]), 'support')],
            positive='g(x)=e^{-sx} on x>=0 by construction; jumps of g,g\',g\'\' vanish; g(3)=e^{-3s}; C0=g(3)/4')
    control('kernel_negative_atom_misread', [('atom_at_minus_one', lambda: validate_measure_support([(F(-1), F(1))]), 'negative support'),
                                             ('packet_signed_support', mut(spectral_support='real line'), 'negative support')],
            window_reads='5/e', true='e')
    control('kernel_l1_and_first_moment', [('M0_as_int_ghat', mut(M0=F(1)), 'L1 norm'),
                                           ('M1_without_pi', mut(M1_over_s=F(4), M1_pi_power=0), 'first moment')],
            M0='2', M1='4s/pi', M2='2s^2')
    control('poisson_kink_divergence', [('finite_poisson_M1', lambda: validate_poisson_moment(p1[str(10 ** 4)]['upper']), 'Poisson first moment')],
            jump_g_prime='-2s', wallis='W(1,-1) divergent')
    need(validate_poisson_moment(mom['poisson']['1']), 'poisson_moment_is_infinite')
    control('window_linear_in_s', [('s_independent_M1', lambda: validate_linear_in_s(lambda s: F(4)), 'linear in s')],
            kernel_term='49|tau|s/pi')
    need(validate_linear_in_s(lambda s: 4 * s), 'window_M1_linear')
    control('local_not_extensive_duhamel', [('extensive_norm', lambda: validate_local_slope(k_ext), 'extensive'),
                                            ('packet_extensive_k', mut(k=k_ext[2]), 'duhamel slope')],
            extensive_k={str(N): q(v) for N, v in k_ext.items()}, local_k=q(k))
    need(validate_local_slope({2: k, 3: k, 4: k}), 'local_slope_box_independent')
    control('tau_zero_null_replay', [('poisson_tail_dropped', lambda: validate_tau_zero(t0_rad, t0_terms['arithmetic'], arith, poisson0_tail_lo), 'Poisson tail'),
                                     ('window_nonzero_at_tau0', lambda: validate_tau_zero(t0_rad + F(1, 10 ** 30), t0_terms['arithmetic'], poisson0, poisson0_tail_lo), 'tau zero')],
            window_radius_tau0=q(t0_rad), poisson_tail_tau0_L1e9_lower=q(rdown(poisson0_tail_lo, 10 ** 30)))
    need(validate_tau_zero(t0_rad, t0_terms['arithmetic'], poisson0, poisson0_tail_lo) and t0_terms['state'] == 0
         and t0_terms['kernel_dynamics'] == 0, 'tau_zero_window_equals_arithmetic')
    control('window_fourier_sign_convention', [('theta_to_minus_theta', mut(free_atom='g(-3)/4'), 'sign convention')],
            mutated_value='25e^{-3}/4', correct='e^{-3}/4')
    control('state_term_not_effect', [('D_over_2', mut(state=D, state_factor=F(1, 2), radius=radius - D), 'state term is not an effect')],
            toy='|Tr(Delta A)|=4D/5>D/2 for A=diag(u,conj u), u=(3+4i)/5')
    control('av1_tier_bound', [('tier_i', mut(D=D_i), 'av1 tier'),
                               ('at4_sqrt', mut(D=Da_hi), 'av1 tier'),
                               ('reverse_82_face_value', mut(D=D_rev), 'av1 tier')],
            bound='forward tier (ii) as frozen in contract parameters.state_bound')
    inv = ['AGENTS.md', 'research/round32/contracts/av2.json'] + list(contract['shared_premises'])
    need(validate_reverse_inventory(inv, contract) and not (set(contract['forward_additional_premises']) & set(contract['shared_premises'])),
         'reverse_inventory_declared_clean', files=len(inv), note='declared list only; the reverse inputs/ were not read')
    control('reverse_premise_isolation', [('triage_added', lambda: validate_reverse_inventory(inv + ['research/round32/skeptic/triage.md'], contract), 'forbidden input'),
                                          ('skeptic_av2_added', lambda: validate_reverse_inventory(inv + ['research/round32/skeptic/av2-independent-derivation.md'], contract), 'forbidden input'),
                                          ('premise_dropped', lambda: validate_reverse_inventory(inv[:-1], contract), 'inventory differs')])
    control('c1_window_preview_only', [('c1_as_certificate', mut(kernel='C1'), 'kernel switch'),
                                       ('c1_role_certificate', lambda: validate_kernel_role('C1', 'certificate'), 'kernel switch')],
            c1=c1)
    rows = [dict(r) for r in CHECKS if r.get('kind') == 'control']
    ev = {'rows': rows, 'digest': hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()}
    required = [c_ for c_ in contract['controls'] if c_ != 'coherent_evidence_tampering']
    need(validate_evidence(ev, required), 'evidence_validates')
    bad = [dict(r) for r in rows]
    bad[3]['passed'] = False
    ev_bad = {'rows': bad, 'digest': hashlib.sha256(json.dumps(bad, sort_keys=True).encode()).hexdigest()}
    fewer = [dict(r) for r in rows if r['id'] != 'state_term_not_effect']
    ev_few = {'rows': fewer, 'digest': hashlib.sha256(json.dumps(fewer, sort_keys=True).encode()).hexdigest()}
    control('coherent_evidence_tampering', [('flip_boolean_rebind_hash', lambda: validate_evidence(ev_bad, required), 'required control not passed'),
                                            ('drop_control_rebind_hash', lambda: validate_evidence(ev_few, required), 'missing required control')])
    executed = [r['id'] for r in CHECKS if r.get('kind') == 'control']
    need(sorted(executed) == sorted(contract['controls']) and len(executed) == 24, 'all_contract_controls_executed',
         note='controls has 24 ids; preregistration.controls_required lists 23 (c1_window_preview_only absent)')
    need(set(contract['controls']) - set(contract['preregistration']['controls_required']['ids']) == {'c1_window_preview_only'},
         'contract_control_list_observation')
    for bad_call, reason in ((lambda: calculator(tau=1e-8, pi=(pi_lo, pi_hi)), 'exact arithmetic'),
                             (lambda: calculator(tau='2/100000000', pi=(pi_lo, pi_hi)), 'domain'),
                             (lambda: calculator(selected=('0', '1/8', '0'), pi=(pi_lo, pi_hi)), 'domain'),
                             (lambda: calculator(s='0', pi=(pi_lo, pi_hi)), 'domain')):
        if not rejects(bad_call, reason):
            raise CheckFailure('calculator domain')
    need(True, 'calculator_domain_rejections')

    flags = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
             'scientific_priority_verified': False, 'grid_claim': False, 'skeptic_package_is_certificate': False}
    need(validate_claims(flags), 'claim_flags_false')

    previews = {
        'D': preview(D), 'radius': preview(radius), 'margin_target_over_radius': preview(target / radius),
        'state': preview(terms['state']), 'mean_square': preview(terms['mean_square']),
        'kernel_dynamics': preview(terms['kernel_dynamics']), 'arithmetic': preview(arith),
        'free_value': preview(datum), 's_star': preview((s_lo + s_hi) / 2), 's_star_D0': preview((s0_lo + s0_hi) / 2),
        'at4_L1e4_radius': preview(at4_hi), 'poisson_floor_D0': preview(floor_lo), 'poisson_floor_with_D': preview(withD_lo),
        'tier_i_window_radius': preview(2 * (D_i + D_i ** 2) + k * 4 / pi_lo),
        'at4_sqrt_window_radius': preview(2 * (Da_hi + Da_hi ** 2) + k * 4 / pi_lo),
        'effect_misuse_radius': preview(radius - D), 'dropped_m2_radius': preview(radius - terms['mean_square']),
        'c1_window_radius': preview(c1_rad), 'c1_crossover': preview(c1_sstar),
        'sign_mutation_free_atom': preview(25 * datum), 'negative_atom_window_reading': preview(5 * (em1_lo + em1_hi) / 2),
        'label': 'floating previews only; no admission Boolean reads them',
    }
    result = {
        'loop': 'AV2', 'stage': 'pre_comparison', 'role': 'skeptic',
        'standing': 'model-agent skeptic with correlated ancestry; not human peer review, not formal verification',
        'human_author': 'Hruday N M (BUNZEEY)',
        'producer_files_read': [],
        'route': 'annihilator-jump transform: P(D)=(D+s)(D-s)^3 kills both branches, P(D)g=[g\'\'\'](0) delta=-8s^3 delta, '
                 'so ghat=-8s^3/(2pi P(i theta)); moments by theta=s tan(phi) and Wallis integrals; directed Riemann cross-check',
        'contract_sha256': CONTRACT_SHA256, 'av1_gate_sha256': hashlib.sha256(gate_bytes).hexdigest(),
        'at4_report_sha256': sha(AT4_REPORT),
        'model_id': truth['model_id'],
        'conventions': {'c': 'c(theta)=<chi,e^{i theta G}chi>', 'ghat': '(2pi)^-1 int g(x) e^{-i theta x} dx',
                        'clock': 's=alpha*t_E/hbar, theta=alpha*t/hbar', 'free': 'c0(theta)=e^{3 i theta}/4'},
        'kernel': {'C2': {'transform': '4s^3/(pi(s-i theta)^3(s+i theta))', 'modulus': '(4s^3/pi)(s^2+theta^2)^-2',
                          'moments': mom['C2'], 'jumps_at_0_s1': [q(x) for x in c2['jumps_s1']], 'L1_norm_of_g': '8/s',
                          'ghat_at_0': '4/(pi s)'},
                   'poisson': {'transform': 's/(pi(s^2+theta^2))', 'moments': mom['poisson'],
                               'jumps_at_0_s1': [q(x) for x in kern['poisson']['jumps_s1']]},
                   'C1': c1},
        'quadrature_crosscheck': quad,
        'comparison': {'bound': '|c(theta)-c0(theta)|<=k|theta|+D+m^2, m^2<=D^2, all real theta', 'k': q(k),
                       'B_norm': q(B), 'stars': 7, 'D': q(D), 'effect_refinement_applied': False},
        'pi_bracket': {'lower': q(pi_lo), 'upper': q(pi_hi), 'method': 'Hutton 8atan(1/3)+4atan(1/7), outward to 1e-60; Machin overlap'},
        'free_reference': {'value': 'e^{-3}/4', 'lower': q(f_lo), 'upper': q(f_hi), 'datum': q(datum)},
        'radius': {
            'formula': 'E=M0(D+D^2)+k M1 + arithmetic, M0=2, M1=4s/pi, k=49|tau|/4, s=1',
            'terms_exact': {key: q(v) for key, v in terms.items()},
            'kernel_dynamics_lower_pi_hi': q(kd_lo),
            'pi_rounding_slack_inside_kernel_dynamics': q(terms['kernel_dynamics'] - kd_lo),
            'radius_exact': q(radius), 'radius_upper_1e-40': q(rup(radius, 10 ** 40)),
            'interval': {'lower': q(lo_int), 'upper': q(hi_int)},
            'target': q(target), 'target_met': radius <= target, 'margin_lower': q(rdown(target / radius, 10 ** 9)),
            'reference_inside': True, 'sub_label': 'reference_unresolved',
            'minus_tau': {'radius_exact_equal': radii['minus'][1] == radius, 'role': 'replay at the mirrored coupling'},
        },
        'crossover': {'s_star_lower': q(s_lo), 's_star_upper': q(s_hi), 's_star_D0_lower': q(s0_lo), 's_star_D0_upper': q(s0_hi),
                      'scope': 'crossover of the formula only; s=1 is the only preregistered node; no grid or [0,128] claim'},
        'poisson_retained': retained,
        'previews': previews,
        'checks': CHECKS,
    }
    result.update(flags)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    result = execute()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'radius': result['previews']['radius'],
                      's_star': [result['crossover']['s_star_lower'], result['crossover']['s_star_upper']]}))


if __name__ == '__main__':
    main()
