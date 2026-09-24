#!/usr/bin/env python3
"""Round32 AX2 skeptic pre-comparison replay (uniform-model window certificate).

Written after the AX2 contract freeze from the frozen contract, the AX1 and AV2
gates, selection-ax2.md, the skeptic's own AX1/AV2 notes and the admitted AV2
calculator (research/round32/forward/av2/calculator.py, used only as a
hash-pinned comparator), before reading anything under
research/round32/forward/ax2/. Standard library only. Every admission Boolean is
decided with fractions.Fraction and directed enclosures; floats appear only in
the labelled 'previews' block. Every check and control raises an explicit
exception, so python -O cannot disable it. Model-agent skeptic with correlated
ancestry; not human peer review, not formal verification.

What is replayed: the AV2 window lemma (C^2 window, M_0=2, M_1=4s/pi, re-derived
by the annihilator-jump route) transferred to route B of the uniform
Kogut-Susskind SU(2) model (AX1). Only the Duhamel slope k'=51|tau|/4 (seven
whole stars plus two single-factor selected groups, re-enumerated here) and the
state bound D' (read from the hash-pinned AX1 gate decision and recomputed from
the AX1 tier-(ii) formula) change. The Haar reference and the free correlation
e^{3 i theta}/4 are unchanged.

Usage: python3 -B research/round32/skeptic/ax2_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from fractions import Fraction as F
from itertools import product
from math import comb, isqrt
from pathlib import Path

sys.dont_write_bytecode = True   # the admitted AV2 calculator is imported; never write a .pyc into its closure

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / 'research/round32/contracts/ax2.json'
CONTRACT_SHA256 = 'da72afe377d7601e6b6ec3835ab69d05813cb26c4b46f67485a4d8e0c055992b'
AX1_GATE = ROOT / 'research/round32/advisor/ax1-gate.json'
AX1_GATE_SHA256 = '1b8fb152696659439bb01fc7df429fc76fa3132d4936df450d8131256015d177'
AX1_CONTRACT = ROOT / 'research/round32/contracts/ax1.json'
AX1_CONTRACT_SHA256 = 'bc834eec4f5377041cea9db42a8674cf1f3de0a43b7fef3696a461a011da7d8d'
AV2_GATE = ROOT / 'research/round32/advisor/av2-gate.json'
AV2_GATE_SHA256 = '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33'
AV2_CALC = ROOT / 'research/round32/forward/av2/calculator.py'
AV2_CALC_SHA256 = '99a9fc81f156ab207d91cae55fa8c736f3dd5848619c11521f0bd8b4cd133ed9'
DEN = 10 ** 60

DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
R_COVER = ((0, 0, 0), (0, 0, 1))
LABEL = 'uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling (g^4=96/tau=9.6x10^9 at the cap)'
STATE_TIER = 'ax1_gate_forward_tier_ii'
RECIPE = {'t1_faces': 52, 'J_over_tau': 29, 'self_consistent': True, 'pair_term': True, 'form': 'density'}


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
    """mutations: list of (label, callable, reason); each must be rejected for that reason."""
    rows = []
    for label, fn, reason in mutations:
        if not rejects(fn, reason):
            raise CheckFailure('control %s: mutation %s accepted' % (cid, label))
        rows.append({'mutation': label, 'rejected_for': reason})
    need(True, cid, kind='control', mutations=rows, **detail)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


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


def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def sub(a, b):
    return tuple(i - j for i, j in zip(a, b))


# ---------------------------------------------------------------- directed enclosures (own)
def arctan_bracket(x, n=64):
    s = F(0)
    parts = []
    for k in range(n):
        s += F((-1) ** k) * x ** (2 * k + 1) / (2 * k + 1)
        parts.append(s)
    lo, hi = sorted(parts[-2:])
    return lo, hi


def pi_bracket():
    """Hutton pi=8atan(1/3)+4atan(1/7), outward to 1e-60; Machin overlap required."""
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
    """e^x, rational x>=0: halve to x<=1, Taylor with geometric remainder, square outward."""
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
    if not _LOG2:
        s = sum((F(1, k * 2 ** k) for k in range(1, K + 1)), F(0))
        _LOG2.append((s, s + F(1, (K + 1) * 2 ** K)))
    return _LOG2[0]


def log_pos(y):
    """log y, rational y>=1: mantissa by atanh series, geometric tail, log 2 by its series."""
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


# ---------------------------------------------------------------- Gaussian rationals and the window (jump route)
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


def left_poly(name, s):
    return {'poisson': [F(1)], 'C1': [F(1), -2 * s], 'C2': [F(1), -2 * s, 2 * s * s]}[name]


def p_deriv_at(cs, j, x):
    return sum((cs[i] * F(fact(i), fact(i - j)) * x ** (i - j) for i in range(j, len(cs))), F(0))


def jump_route(name, s):
    """P(D)=(D+s)(D-s)^(d+1) kills both branches; P(D)g = sum kappa_r delta^(r)."""
    cs = left_poly(name, s)
    d = len(cs) - 1
    left = [sum((comb(n, j) * s ** (n - j) * p_deriv_at(cs, j, F(0)) for j in range(0, min(n, d) + 1)), F(0))
            for n in range(d + 2)]
    right = [(-s) ** n for n in range(d + 2)]
    J = [right[n] - left[n] for n in range(d + 2)]
    a = polymul([F(1)], [s, F(1)])
    for _ in range(d + 1):
        a = polymul(a, [-s, F(1)])
    if sum((a[n] * (-s) ** n for n in range(len(a))), F(0)) != 0:
        raise CheckFailure('right branch not annihilated')
    for x in [F(-k, 3) for k in range(1, d + 4)]:
        val = sum((a[n] * sum((comb(n, j) * s ** (n - j) * p_deriv_at(cs, j, x) for j in range(0, min(n, d) + 1)), F(0))
                   for n in range(len(a))), F(0))
        if val != 0:
            raise CheckFailure('left branch not annihilated')
    kappa = [sum((a[n] * J[n - 1 - r] for n in range(r + 1, len(a))), F(0)) for r in range(len(a) - 1)]
    return {'d': d, 'jumps': J, 'operator': a, 'delta_coefficients': kappa}


def pi_ghat(route, theta):
    a = route['operator']
    it = (F(0), F(theta))
    P = (F(0), F(0))
    for n, an in enumerate(a):
        P = c_add(P, c_scale(c_pow(it, n), an))
    return c_scale(c_inv(P), route['delta_coefficients'][0] / 2)


def closed_form_C2(s, theta):
    a = (F(s), -F(theta))
    b = (F(s), F(theta))
    return c_scale(c_inv(c_mul(c_pow(a, 3), b)), 4 * s ** 3)


def wallis(a, b):
    if b < 0:
        return None
    coef = F(dfact(a - 1) * dfact(b - 1), dfact(a + b))
    if a % 2 == 0 and b % 2 == 0:
        return coef / 2, 1
    return coef, 0


def moments(name):
    """M_j=(c/pi) s^j W(j,d-j), c=|kappa_0|/s^(d+1); symbolic text or 'infinity'."""
    cs_ = set()
    for s in (F(1), F(2), F(3, 7)):
        r = jump_route(name, s)
        cs_.add(abs(r['delta_coefficients'][0]) / s ** (r['d'] + 1))
    if len(cs_) != 1:
        raise CheckFailure('kappa_0 not homogeneous')
    c = cs_.pop()
    d = jump_route(name, F(1))['d']
    out = {}
    for j in range(3):
        w = wallis(j, d - j)
        if w is None:
            out[str(j)] = 'infinity'
            continue
        coef, pp = c * w[0], w[1] - 1
        t = q(coef) + ('' if j == 0 else ('s' if j == 1 else 's^%d' % j))
        t += '/pi' if pp == -1 else ('*pi' if pp == 1 else '')
        out[str(j)] = t
    return out


# ---------------------------------------------------------------- uniform model geometry (route B)
def pi_map(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    ea, ec = DIRS[a], DIRS[c]
    return ((p, a), (p, c), (add(p, ea), c), (add(p, ec), a))


def owner_set(p, a, c):
    return frozenset(pi_map(tail) for tail, _ in face_links(p, a, c))


def is_selected(p, a, c):
    """The three xy faces of a 4x2x1 factor whose four links all have tails in that factor."""
    return (a, c) == ('x', 'y') and p[0] % 4 in (0, 1, 2) and p[1] % 2 == 0


def anchored_faces(b):
    out = []
    for r, s in product(range(4), range(2)):
        p = (4 * b[0] + r, 2 * b[1] + s, b[2])
        for a, c in ORIENT:
            out.append({'base': p, 'orient': a + c, 'owners': owner_set(p, a, c), 'selected': is_selected(p, a, c),
                        'links': face_links(p, a, c)})
    return out


def in_box(b, n):
    return all(-n <= v <= n for v in b)


def groups_in_box(n):
    """Route B groups: whole star (21 omitted faces; retained iff b+S in the box) and a
    single-factor group (3 selected faces, support {b}). Norms in G=H/alpha units:
    each face carries |tau|/3 in delta=alpha/8 units, so |tau|/24 in G units."""
    out = []
    for b in product(range(-n, n + 1), repeat=3):
        faces = anchored_faces(b)
        om = [f for f in faces if not f['selected']]
        se = [f for f in faces if f['selected']]
        if len(om) != 21 or len(se) != 3:
            raise CheckFailure('face split per factor')
        if all(in_box(add(b, s), n) for s in S_STAR):
            out.append({'kind': 'star', 'anchor': b, 'support': frozenset(add(b, s) for s in S_STAR), 'faces': om,
                        'norm_G_over_tau': F(len(om), 24)})
        out.append({'kind': 'single', 'anchor': b, 'support': frozenset([b]), 'faces': se,
                    'norm_G_over_tau': F(len(se), 24)})
    return out


def incidence(n):
    groups = groups_in_box(n)
    Rset = set(R_COVER)
    meet = [g for g in groups if g['support'] & Rset]
    for g in groups:
        for f in g['faces']:
            if not f['owners'] <= g['support']:
                raise CheckFailure('face outside its group support')
    table = []
    for g in sorted(meet, key=lambda g: (g['kind'], g['anchor'])):
        m = [f for f in g['faces'] if f['owners'] & Rset]
        table.append((g['kind'], g['anchor'], len(g['faces']), len(m), sum(1 for f in m if f['owners'] <= Rset)))
    return {'stars': sum(1 for g in meet if g['kind'] == 'star'), 'singles': sum(1 for g in meet if g['kind'] == 'single'),
            'B_over_tau': sum((g['norm_G_over_tau'] for g in meet), F(0)),
            'extensive_over_tau': sum((g['norm_G_over_tau'] for g in groups), F(0)), 'table': table}


# ---------------------------------------------------------------- AX1 tier formulas (route B)
def dens(eps):
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def T_prime(a, faces=52, self_consistent=True):
    t1 = F(faces, 144) * a
    return t1 / (1 - 352 * 29 * a) if self_consistent else t1


def D_from_recipe(a, recipe):
    T = T_prime(a, recipe['t1_faces'], recipe['self_consistent'])
    eps = 2 * T + (T * T if recipe['pair_term'] else 0)
    return dens(eps) if recipe['form'] == 'density' else 2 * eps


def D_forward_ii(a):
    return D_from_recipe(a, RECIPE)


def D_reverse_R88(a):
    T = T_prime(a)
    eps = F(88, 144) * a + 2 * 352 * 29 * a * T + T * T
    return 2 * eps


def D_tier_i(a):
    t = 29 * a * F(148, 7)
    return dens(2 * t + t * t)


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
    """Recompute the AX2 packet from the frozen contract and the AX1 gate."""
    for key in ('tau', 's', 'D', 'k', 'J0', 'M0', 'M1_over_s', 'state', 'mean_square', 'kernel_dynamics', 'arithmetic', 'radius'):
        exact(p[key], key)
    if p['kernel'] != 'C2':
        raise Rejected('kernel switch: the certificate kernel is the frozen C2 window')
    if (F(p['tau']) != truth['tau'] and F(p['tau']) != -truth['tau']) or F(p['s']) != truth['s'] \
            or p['triple'] != ['tau/24'] * 3 or p['reference'] != 'haar' or p['route'] != 'B' \
            or p['model_id'] != truth['model_id']:
        raise Rejected('model changed or relabelled')
    if p['label'] != LABEL or re.search(r'weak[- ]coupling|continuum', p['label'], re.I) \
            or F(p['g4']) != 96 / abs(truth['tau']) or p['claims'].get('uniform_wilson_claim') is not True:
        raise Rejected('uniform label: uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling')
    if p['riders']:
        raise Rejected('uniform label: no sign certificate or K_2 rider (loop-2 veto)')
    if F(p['J0']) != F(29, 10 ** 8) or 29 * abs(F(p['tau'])) > F(p['J0']) or p['J0_route'] != 'R1':
        raise Rejected('j0 resolution: route-B J_0\'=29/10^8 (R1) must be declared')
    if p['single_groups'] != 2 or p['selected_faces_R'] != 6:
        raise Rejected('selected incidence: exactly two single-factor groups (six selected faces) meet R')
    if p['stars'] != 7:
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
    if p['D_recipe'] != RECIPE or set(p['D_tiers'].values()) != {STATE_TIER}:
        raise Rejected('tier mixing: every state occurrence uses the AX1 forward tier (ii) with its named ingredients')
    if F(p['D']) != truth['D'] or p['D_source'] != STATE_TIER:
        raise Rejected('av1 tier bound: D differs from the AX1 gate forward tier-(ii) value')
    if F(p['k']) != truth['k'] or F(p['k']) != 2 * (7 * p['stars'] + p['single_groups']) * abs(F(p['tau'])) / 8:
        raise Rejected('duhamel slope: k\' must be the local nine-group value 51|tau|/4')
    if F(p['M0']) != 2:
        raise Rejected('L1 norm: ||ghat||_1=2 (not |int ghat|=g(0)=1)')
    if F(p['M1_over_s']) != 4 or p['M1_pi_power'] != -1:
        raise Rejected('first moment: int|theta||ghat|=4s/pi')
    if p['state_factor'] != 1 or F(p['state']) != 2 * truth['D']:
        raise Rejected('state term is not an effect: no D/2 refinement on W alpha0_theta(W)')
    if F(p['mean_square']) != 2 * truth['D'] ** 2:
        raise Rejected('mean square not charged as M0*D\'^2')
    if p['combination'] != 'linear':
        raise Rejected('root-N: deterministic terms add linearly')
    if F(p['kernel_dynamics']) != truth['k'] * 4 * F(p['s']) / truth['pi_lo']:
        raise Rejected('kernel dynamics must be k\'*4s/pi with the lower pi endpoint')
    if F(p['arithmetic']) != truth['arithmetic'] or F(p['radius']) != F(p['state']) + F(p['mean_square']) \
            + F(p['kernel_dynamics']) + F(p['arithmetic']):
        raise Rejected('radius mismatch')
    if p['producers'] != ['forward'] or p['skeptic_replay_required'] is not True \
            or p['independence'] != 'single producer; skeptic replay from the contract alone':
        raise Rejected('single producer: producers=[forward]; admission requires the skeptic replay')
    for key in ('continuum_claim', 'weak_coupling_claim', 'resolved_interaction_shift', 'scientific_priority_verified', 'grid_claim'):
        if p['claims'][key] is not False:
            raise Rejected('forbidden claim ' + key)
    if p['claims']['euclidean_node_certified'] is not (F(p['radius']) <= truth['target']):
        raise Rejected('node flag must equal the s=1 target Boolean')
    if p['sub_label'] != 'reference_unresolved':
        raise Rejected('reference: free value inside, sub-label reference_unresolved')
    return True


def validate_gate_bytes(b):
    if sha_bytes(b) != AX1_GATE_SHA256:
        raise Rejected('gate sha256: AX1 gate bytes differ from the pinned admitted gate')
    return True


def validate_scaling(claim, lo, hi):
    band = {'linear': (F(99), F(101)), 'sqrt': (F(99, 10), F(101, 10))}[claim]
    if not (band[0] <= lo and hi <= band[1]):
        raise Rejected('tau scaling: ratio outside the %s band' % claim)
    return True


def validate_retained(block, target):
    for key in ('poisson_floor_uniform_D0', 'poisson_with_Dprime', 'poisson_at4_form_L1e4'):
        row = block.get(key)
        if row is None or row.get('verdict') != 'insufficient' or not F(row['lower']) > target:
            raise Rejected('insufficient verdict retained: ' + key)
    return True


def validate_support_identity(poly_on_nonnegative):
    if poly_on_nonnegative != [F(1)]:
        raise Rejected('window not equal to e^{-sx} on the support')
    return True


def validate_measure_support(atoms):
    if any(x < 0 for x, _ in atoms):
        raise Rejected('negative support: identity C(s)=int ghat c fails off [0,inf)')
    return True


def validate_linear_in_s(m1_fn):
    if len({m1_fn(s) / s for s in (F(1, 2), F(1), F(2))}) != 1:
        raise Rejected('window first moment must be linear in s')
    return True


def validate_local_slope(k_by_N):
    if len(set(k_by_N.values())) != 1:
        raise Rejected('extensive Duhamel: slope must not depend on the box')
    return True


def validate_incidence(inc_by_N):
    for N, inc in inc_by_N.items():
        if inc['singles'] != 2:
            raise Rejected('selected incidence: two single-factor groups meet R')
        if inc['stars'] != 7:
            raise Rejected('incident stars: seven whole stars meet R')
    return True


def validate_centering(kind, m, d, residue):
    truth = {'vector': d * d, 'scalar': -2 * m * d - d * d, 'uncentered': m * m}[kind]
    if residue != truth:
        raise Rejected('centering residue')
    if kind != 'vector':
        raise Rejected('centering: vector centering required')
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


# ---------------------------------------------------------------- skeptic comparator calculator (proved uniform domain)
def calculator(D_gate, pi, tau='1/100000000', s='1', selected='uniform', state=STATE_TIER, window='C2'):
    """Uniform route-B window certificate. D' is the AX1 gate value (a valid bound for
    every |tau|<=10^-8 because the tier-(ii) formula increases in |tau|); never an input."""
    tau = exact(tau, 'tau')
    s = exact(s, 's')
    if selected != 'uniform':
        raise Rejected('domain: selected triple must be the uniform tau/24 (the zero triple is the AV2 family)')
    if state != STATE_TIER:
        raise Rejected('domain: state bound from the AX1 gate only')
    if window != 'C2':
        raise Rejected('kernel switch: C2 window only')
    if abs(tau) > F(1, 10 ** 8):
        raise Rejected('domain: |tau|<=10^-8')
    if s <= 0:
        raise Rejected('domain: s>0')
    pi_lo, _ = pi
    k = F(51, 4) * abs(tau)
    f_lo, f_hi = exp_neg(3 * s)
    f_lo, f_hi = f_lo / 4, f_hi / 4
    terms = {'state': 2 * D_gate, 'mean_square': 2 * D_gate * D_gate, 'kernel_dynamics': k * 4 * s / pi_lo,
             'arithmetic': (f_hi - f_lo) / 2}
    return terms, sum(terms.values(), F(0)), (f_lo + f_hi) / 2, (f_lo, f_hi)


def load_av2_calculator():
    b = AV2_CALC.read_bytes()
    if sha_bytes(b) != AV2_CALC_SHA256:
        raise CheckFailure('admitted AV2 calculator hash')
    spec = importlib.util.spec_from_file_location('admitted_av2_calculator', str(AV2_CALC))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- main computation
def execute():
    contract_bytes = CONTRACT.read_bytes()
    need(sha_bytes(contract_bytes) == CONTRACT_SHA256, 'contract_sha256_bound')
    contract = json.loads(contract_bytes)
    par = contract['parameters']
    pre = contract['preregistration']
    need(contract['status'] == 'frozen_before_production' and contract['id'] == 'AX2' and contract['producers'] == ['forward']
         and contract['direction'] == 'single+skeptic' and contract['single_direction_independent_replay'] is True,
         'contract_frozen_single_direction')
    tau = F(par['tau'])
    s1 = F(par['s'])
    target = F(par['target'])
    need(tau == F(1, 10 ** 8) and s1 == 1 and target == F(1, 10 ** 6) and F(pre['target']['value']) == target
         and pre['target']['comparator'] == '<=' and pre['nodes']['s_values'] == ['1'] and pre['tau']['signs_evaluated'] == ['+', '-']
         and par['k_prime'] == '51|tau|/4' and par['window'] == 'AV2 C^2 window', 'contract_parameters_read',
         tau=q(tau), s=q(s1), target=q(target))
    need(contract['controls'] == pre['controls_required']['ids'] and len(contract['controls']) == 25, 'control_mirror_25')
    mref = re.fullmatch(r'exp\(-(\d+)\)/(\d+) enclosed', pre['observable']['reference_value_exact'])
    ref_energy, ref_weight = F(int(mref.group(1))), F(1, int(mref.group(2)))
    need(pre['observable']['reference_route'] == 'haar' and pre['observable']['centering'] == 'vector'
         and ref_energy == 3 and ref_weight == F(1, 4), 'contract_reference_read', reference='exp(-3s)/4')
    mDp = re.match(r'(\d+)/(\d+) ', par['D_prime'])
    D_contract = F(int(mDp.group(1)), int(mDp.group(2)))

    # ---------------- AX1 gate binding (hash-pinned)
    gate_bytes = AX1_GATE.read_bytes()
    need(validate_gate_bytes(gate_bytes), 'ax1_gate_sha256_pinned', sha256=AX1_GATE_SHA256)
    gate = json.loads(gate_bytes)
    Dp = F(re.search(r"Bind the forward D'_ii = (\d+/\d+)", gate['decision']).group(1))
    D_rev_gate = F(re.search(r"R-refinement D'_ii=(\d+/\d+)", gate['accepted']).group(1))
    D_i_dec = F(re.search(r"tier \(i\) D'_i~([0-9.]+e-[0-9]+)", gate['accepted']).group(1))
    need(gate['verdict'] == 'accepted_within_scope' and Dp == D_contract, 'ax1_gate_binds_contract_Dprime',
         D_prime=q(Dp))
    for key in ("J_0'=29/10^8", "k'=51|tau|/4", 'exactly 7 whole stars', '2 single-factor groups', 'g^4=9.6x10^9',
                "||B_N||<=51|tau|/8"):
        if key not in gate['accepted']:
            raise CheckFailure('gate text ' + key)
    need(True, 'ax1_gate_constants_read')
    ax1c = AX1_CONTRACT.read_bytes()
    need(sha_bytes(ax1c) == AX1_CONTRACT_SHA256 and gate['bindings']['research/round32/contracts/ax1.json'] == AX1_CONTRACT_SHA256,
         'ax1_contract_hash_matches_gate_binding')
    ax1_target = F(json.loads(ax1c)['preregistration']['target']['value'])
    av2g = AV2_GATE.read_bytes()
    need(sha_bytes(av2g) == AV2_GATE_SHA256, 'av2_gate_sha256_pinned')
    av2 = json.loads(av2g)
    D_zero = F(re.search(r'tier-\(ii\) bound D=(\d+/\d+)', av2['accepted']).group(1))
    av2_datum = F(int(re.search(r'datum d=(\d+)/\(4\*10\^40\)', av2['accepted']).group(1)), 4 * 10 ** 40)
    av2_R = F(int(re.search(r'R=(\d+)/10\^40', av2['accepted']).group(1)), 10 ** 40)

    # ---------------- recompute D' from the AX1 tier-(ii) formula
    a = abs(tau)
    Tp = T_prime(a)
    rho = 352 * 29 * a * Tp
    need(T_prime(a, 52, False) == F(13, 3600000000) and Tp == F(13, 3599632512) and rho == F(4147, 11248851600000000),
         'ax1_tier_ii_ingredients', t1=q(F(13, 3600000000)), T=q(Tp), rho=q(rho))
    need(D_forward_ii(a) == Dp and D_forward_ii(abs(-tau)) == Dp, 'Dprime_recomputed_both_signs',
         note='t1=52|tau|/144, J=29|tau|, T=t1/(1-352J), eps=2T+T^2, D=2eps(1+eps)/(1+eps^2)')
    D_i = D_tier_i(a)
    need(D_reverse_R88(a) == D_rev_gate and abs(D_i - D_i_dec) < F(5, 10 ** 10) and D_rev_gate < Dp < ax1_target
         and D_zero < Dp and D_i > target, 'other_state_values_identified',
         reverse_refinement=q(D_rev_gate), tier_i=q(D_i), ax1_target=q(ax1_target), zero_selected_D=q(D_zero))
    # monotone in |tau| on [0,cap]: T increasing, eps increasing, dens'(eps)=2(1+2eps-eps^2)/(1+eps^2)^2>0 for 0<=eps<=1
    eps_cap = 2 * Tp + Tp * Tp
    samples = [D_forward_ii(a * F(j, 8)) for j in range(9)]
    need(eps_cap < 1 and all(x < y for x, y in zip(samples, samples[1:])) and samples[-1] == Dp,
         'Dprime_monotone_cap_value_bounds_domain', note='1+2eps-eps^2>=1 on [0,1]; the gate value bounds every |tau|<=10^-8')

    pi_lo, pi_hi = pi_bracket()
    e_lo, e_hi = exp_pos(1)
    need(F(2718281828459045, 10 ** 15) < e_lo < e_hi < F(2718281828459046, 10 ** 15), 'exp_bracket_sanity')

    # ---------------- window lemma constants (unchanged; annihilator-jump route)
    r1 = jump_route('C2', F(1))
    for s in (F(1), F(1, 2), F(3)):
        r = jump_route('C2', s)
        if r['jumps'][:3] != [0, 0, 0] or r['jumps'][3] != -8 * s ** 3 or any(r['delta_coefficients'][1:]):
            raise CheckFailure('C2 jumps')
        for th in (F(0), F(1, 3), F(1), F(-2), F(7, 2), F(10), F(-25, 4)):
            g1 = pi_ghat(r, th)
            if g1 != closed_form_C2(s, th) or c_abs2(g1) != 16 * s ** 6 / (s * s + th * th) ** 4:
                raise CheckFailure('C2 transform')
    mom = {name: moments(name) for name in ('C2', 'C1', 'poisson')}
    need(r1['jumps'] == [0, 0, 0, -8] and mom['C2'] == {'0': '2', '1': '4s/pi', '2': '2s^2'}, 'window_lemma_constants',
         transform='pi*ghat=4s^3/((s-i theta)^3(s+i theta))', moments=mom['C2'])
    need(mom['C1'] == {'0': '4/pi', '1': '4s/pi', '2': 'infinity'} and mom['poisson'] == {'0': '1', '1': 'infinity', '2': 'infinity'},
         'comparison_kernel_moments', C1=mom['C1'], poisson=mom['poisson'])

    # ---------------- free reference unchanged in route B
    casimir_half = F(1, 2) * F(3, 2)
    energy_G = 8 * 4 * casimir_half / 8                       # h_b=8 sum C_e (delta units), G=H/alpha=h/8
    sphere = [F(1)]
    for i in range(3):
        sphere.append(sphere[-1] * F(2 * i + 1, 4 + 2 * i))   # E[q_0^{2m}] for q uniform on S^3
    W_links = face_links((0, 0, 0), 'x', 'z')
    sel_links = {l for b in R_COVER for f in anchored_faces(b) if f['selected'] for l in f['links']}
    z_links_W = [l for l in W_links if l[1] == 'z']
    need(energy_G == ref_energy and sphere[1] == ref_weight and sphere[2] == F(1, 8) and not is_selected((0, 0, 0), 'x', 'z')
         and len(z_links_W) == 2 and not (set(z_links_W) & sel_links), 'free_reference_unchanged_route_B',
         energy_G_units=q(energy_G), E_W2=q(sphere[1]), E_W=0,
         note='Haar reference (h_b tau-independent); a free z link makes the face holonomy Haar; no selected xy face holds a z link')

    # ---------------- incidence and Duhamel slope (uniform route B)
    inc = {N: incidence(N) for N in (2, 3, 4)}
    t2 = inc[2]['table']
    need(all(inc[N]['stars'] == 7 and inc[N]['singles'] == 2 and inc[N]['B_over_tau'] == F(51, 8) and inc[N]['table'] == t2
             for N in inc) and sum(r[3] for r in t2) == 88 and sum(r[4] for r in t2) == 16
         and sum(r[2] for r in t2) == 153 and sum(r[3] for r in t2 if r[0] == 'single') == 6, 'incidence_seven_stars_two_groups',
         table=[{'group': r[0], 'anchor': list(r[1]), 'faces': r[2], 'meeting_R': r[3], 'inside_R': r[4]} for r in t2],
         B_over_tau='51/8', faces_charged=153, meeting_R=88, inside_R=16)
    anchors = sorted({sub(r, s) for r in R_COVER for s in S_STAR})
    kp = 2 * inc[2]['B_over_tau'] * a
    k_ext = {N: 2 * inc[N]['extensive_over_tau'] * a for N in inc}
    need(len(anchors) == 7 and kp == F(51, 4) * a and len(set(k_ext.values())) == 3, 'duhamel_slope_kprime',
         k_prime=q(kp), extensive={str(N): q(v) for N, v in k_ext.items()})
    links = [((4 * b[0] + r, 2 * b[1] + qq, b[2]), d) for b in R_COVER for r in range(4) for qq in range(2) for d in 'xyz']
    ends = {l[0] for l in links} | {add(l[0], DIRS[l[1]]) for l in links}
    need(len(links) == 48 and len(ends) == 36 and all(l in links for l in W_links), 'cover_48_links_36_endpoints')
    J0 = F(29, 10 ** 8)
    need(29 * a <= J0 and J0 * F(148, 7) == F(1073, 175000000) < F(1, 64) and 2 * J0 * 352 == F(319, 1562500) < 1
         and F(7, 25000000) < 29 * a, 'j0_prime_inherited', J0_prime=q(J0))

    # ---------------- radius at the cap
    f_lo, f_hi = exp_neg(3 * s1)
    f_lo, f_hi = f_lo / 4, f_hi / 4
    datum = (f_lo + f_hi) / 2
    arith = (f_hi - f_lo) / 2
    truth = {'tau': tau, 's': s1, 'D': Dp, 'k': kp, 'pi_lo': pi_lo, 'arithmetic': arith, 'target': target,
             'model_id': pre['model_id']}
    radii = {}
    for label, t in (('plus', tau), ('minus', -tau)):
        terms_t, rad_t, dat_t, _ = calculator(Dp, (pi_lo, pi_hi), tau=t)
        radii[label] = (terms_t, rad_t, dat_t)
    terms, radius, _ = radii['plus']
    need(terms['state'] == 2 * Dp and terms['mean_square'] == 2 * Dp * Dp and terms['kernel_dynamics'] == 51 * a / pi_lo
         and terms['arithmetic'] == arith, 'terms_itemized')
    need(radii['minus'][1] == radius and radii['minus'][0] == terms and radii['minus'][2] == datum, 'minus_tau_is_mirror_replay',
         note='U_E mirror: C is even; same |tau| formula; not a second confirmation')
    kd_lo = kp * 4 * s1 / pi_hi
    lo_int, hi_int = datum - radius, datum + radius
    target_met = radius <= target
    need(target_met is True and lo_int <= f_lo and f_hi <= hi_int, 'radius_meets_target_reference_inside',
         radius=q(radius), sub_label='reference_unresolved')
    claims = {'continuum_claim': False, 'uniform_wilson_claim': True, 'weak_coupling_claim': False,
              'resolved_interaction_shift': False, 'scientific_priority_verified': False, 'grid_claim': False,
              'euclidean_node_certified': target_met}
    packet = {'tau': tau, 's': s1, 'triple': ['tau/24'] * 3, 'reference': 'haar', 'route': 'B', 'model_id': truth['model_id'],
              'label': LABEL, 'g4': 96 / a, 'riders': [], 'J0': J0, 'J0_route': 'R1',
              'kernel': 'C2', 'stars': 7, 'single_groups': 2, 'selected_faces_R': 6, 'cover': (48, 36), 'clock_exponent': 3,
              'centering': 'vector', 'spectral_support': 'nonnegative (AQ1)', 'free_atom': 'g(3)/4',
              'D': Dp, 'D_source': STATE_TIER, 'D_recipe': dict(RECIPE),
              'D_tiers': {'state': STATE_TIER, 'mean_square': STATE_TIER, 'minus_tau': STATE_TIER},
              'k': kp, 'M0': F(2), 'M1_over_s': F(4), 'M1_pi_power': -1, 'state_factor': 1,
              'state': terms['state'], 'mean_square': terms['mean_square'], 'kernel_dynamics': terms['kernel_dynamics'],
              'arithmetic': arith, 'radius': radius, 'combination': 'linear',
              'producers': ['forward'], 'skeptic_replay_required': True,
              'independence': 'single producer; skeptic replay from the contract alone',
              'claims': dict(claims), 'sub_label': 'reference_unresolved'}
    need(validate_certificate(packet, truth), 'certificate_packet_validates')

    # ---------------- admitted AV2 calculator: comparator only (hash-pinned; no .pyc written)
    calc = load_av2_calculator()
    c_pi = calc.pi_interval()
    c_f = calc.exp_negative(3)
    c_f = (c_f[0] / 4, c_f[1] / 4)
    wc = calc.window_constants(1, pi_lo, pi_hi)
    need(max(c_pi[0], pi_lo) <= min(c_pi[1], pi_hi) and c_f[0] <= f_lo and f_hi <= c_f[1]
         and wc['M0'] == 2 and wc['M1_upper'] == 4 / pi_lo and wc['M2'] == 2, 'admitted_calculator_primitives_overlap')
    try:
        calc.certify(selected=('1/2400000000',) * 3)
        uniform_refused = False
    except ValueError as exc:
        uniform_refused = 'selected triple zero' in str(exc)
    av2_run = calc.certify()
    need(uniform_refused and F(av2_run['certified_datum']) == av2_datum and F(av2_run['certified_absolute_error']) <= av2_R < radius,
         'admitted_av2_calculator_is_zero_selected_only',
         note='the AV2 calculator refuses the uniform triple; its zero-selected radius is below E\' and cannot be reused')
    c_datum = (c_f[0] + c_f[1]) / 2
    c_radius = 2 * (Dp + Dp * Dp) + kp * 4 / c_pi[0] + (c_f[1] - c_f[0]) / 2
    R_common = rup(max(radius, c_radius), 10 ** 40)
    need(c_datum == av2_datum and c_radius <= target and R_common <= target, 'producer_comparable_radius',
         radius_with_calculator_primitives=q(c_radius), common_outward_bound_1e40=q(R_common))
    common_lo, common_hi = av2_datum - R_common, av2_datum + R_common
    need(common_lo <= c_f[0] and c_f[1] <= common_hi and R_common >= c_radius and R_common >= radius,
         'common_interval_valid',
         datum=q(av2_datum), radius=q(R_common), lower=q(common_lo), upper=q(common_hi),
         note='|C-d|<=E\'_analytic+half-width of the admitted 1e-40 enclosure<=R\'; the skeptic 1e-60 enclosure lies inside it')

    # ---------------- crossover s*
    X = (target - 2 * (Dp + Dp * Dp)) / (51 * a)
    s_lo = rdown(pi_lo * X, 10 ** 12) - F(1, 10 ** 12)
    s_hi = rup(pi_hi * X, 10 ** 12)
    _, rad_slo, _, _ = calculator(Dp, (pi_lo, pi_hi), s=s_lo)
    E_lo_shi = 2 * (Dp + Dp * Dp) + 51 * a * s_hi / pi_hi
    need(rad_slo <= target and E_lo_shi >= target and F(59, 10) < s_lo < s_hi < F(61, 10), 's_star_enclosure',
         s_star_lower=q(s_lo), s_star_upper=q(s_hi), note='crossover of the formula only; only s=1 is certified')
    s0_lo, s0_hi = rdown(100 * pi_lo / 51, 10 ** 12), rup(100 * pi_hi / 51, 10 ** 12)
    fs_lo, fs_hi = exp_neg(3 * s_hi)
    need(fs_hi / 4 < target / 100, 'free_value_at_s_star_below_radius', free_upper=q(rup(fs_hi / 4, 10 ** 15)))
    X7 = (target - 2 * (Dp + Dp * Dp)) / (49 * a)
    s7 = rdown(pi_lo * X7, 10 ** 12)

    # ---------------- retained Poisson failures at the uniform slope
    y = 1 / (2 * kp * s1)
    ly_lo, _ = log_pos(y)
    floor_lo = 2 * kp * s1 * (1 + ly_lo) / pi_hi
    Lr = F(3921569)
    lr_lo, lr_hi = log_pos(1 + Lr * Lr)
    floor_hi = kp * s1 * lr_hi / pi_lo + s1 / (pi_lo * Lr)
    withD_lo = Dp + Dp * Dp + floor_lo
    Dq_lo, Dq_hi = sqrt_bracket(17 * a)
    Dq_lo, Dq_hi = 2 * Dq_lo, 2 * Dq_hi
    L4 = F(10 ** 4)
    lg_lo, lg_hi = log_pos(1 + L4 * L4)
    at4_lo = Dq_lo + Dq_lo ** 2 + kp * s1 * lg_lo / pi_hi + (F(1, 2) + Dq_lo / 2) * 2 * s1 / (pi_hi * L4)
    at4_hi = Dq_hi + Dq_hi ** 2 + kp * s1 * lg_hi / pi_lo + (F(1, 2) + Dq_hi / 2) * 2 * s1 / (pi_lo * L4)
    need(target < floor_lo <= floor_hi and withD_lo > target and at4_lo > target, 'poisson_failures_retained_uniform',
         floor_D0_lower_all_L=q(rdown(floor_lo, 10 ** 30)), floor_upper_at_L_3921569=q(rup(floor_hi, 10 ** 30)),
         with_Dprime_lower_all_L=q(rdown(withD_lo, 10 ** 30)), at4_form_L1e4=[q(rdown(at4_lo, 10 ** 30)), q(rup(at4_hi, 10 ** 30))],
         note='floor: log(1+L^2/s^2)>=2log(L/s), minimum at L=1/(2k\'); AT4 form uses the AX1 square-root control 2sqrt(17|tau|), labelled')
    retained = {'poisson_floor_uniform_D0': {'verdict': 'insufficient', 'lower': q(rdown(floor_lo, 10 ** 30))},
                'poisson_with_Dprime': {'verdict': 'insufficient', 'lower': q(rdown(withD_lo, 10 ** 30))},
                'poisson_at4_form_L1e4': {'verdict': 'insufficient', 'lower': q(rdown(at4_lo, 10 ** 30))}}
    need(validate_retained(retained, target), 'retained_block_validates')
    l65_lo, _ = log_pos(65)
    _, l50_hi = log_pos(50)
    need(l65_lo > 4 and l50_hi < 4, 'poisson_first_moment_divergent', crossing='P1(8)>4/pi>P1(7) at s=1')

    # ---------------- fixtures
    p_m3 = sum((cj * F(-3) ** j for j, cj in enumerate(left_poly('C2', s1))), F(0))
    p_m1 = sum((cj * F(-1) ** j for j, cj in enumerate(left_poly('C2', s1))), F(0))
    em1_lo, em1_hi = exp_neg(1)
    need(p_m3 == 25 and 25 * f_lo > f_hi and p_m1 == 5 and 5 * em1_hi < e_lo, 'window_off_support_fixtures',
         sign_mutation='25e^{-3}/4', negative_atom='5/e versus e')
    u = (F(3, 5), F(4, 5))
    tr = c_add(c_scale(u, F(1, 2)), c_scale((u[0], -u[1]), F(-1, 2)))
    need(c_abs2(tr) == F(16, 25) > F(1, 4), 'complex_state_term_toy', value='|Tr(Delta A)|=4||Delta||_1/5>||Delta||_1/2')
    m1 = tau / 144
    need(m1 != 0 and abs(m1) <= Dp, 'first_order_mean_nonzero_uniform', omega_W_first_order=q(m1),
         note='AX1 transfer: omega(W)^(1)=+tau/144 in the uniform model, so m^2<=D\'^2 must be charged')

    # ---------------- tau scaling (AX1 formula evaluated at tau/100, labelled)
    def E_rng(t, Dfun):
        Dv = Dfun(t)
        base = 2 * (Dv + Dv * Dv)
        return base + 51 * abs(t) / pi_hi, base + 51 * abs(t) / pi_lo

    def D_sqrt(t):
        return 2 * sqrt_bracket(17 * abs(t))[1]
    A_lo, A_hi = E_rng(a, D_forward_ii)
    B_lo, B_hi = E_rng(a / 100, D_forward_ii)
    ratio = (A_lo / B_hi, A_hi / B_lo)
    Q_lo, Q_hi = E_rng(a, D_sqrt)
    P_lo, P_hi = E_rng(a / 100, D_sqrt)
    ratio_sqrt = (Q_lo / P_hi, Q_hi / P_lo)
    need(validate_scaling('linear', *ratio) and validate_scaling('sqrt', *ratio_sqrt), 'tau_scaling_bands',
         linear=[q(rdown(ratio[0], 10 ** 9)), q(rup(ratio[1], 10 ** 9))],
         sqrt=[q(rdown(ratio_sqrt[0], 10 ** 9)), q(rup(ratio_sqrt[1], 10 ** 9))])

    # ---------------- controls (all 25 contract ids)
    def mut(**changes):
        p = dict(packet)
        p['claims'] = dict(packet['claims'])
        for key, val in changes.items():
            if key in p['claims']:
                p['claims'][key] = val
            else:
                p[key] = val
        return lambda: validate_certificate(p, truth)

    control('missing_incoming_stars', [('orthant_two_stars', mut(stars=2, k=F(2 * (14 + 2), 8) * a), 'incident stars')],
            anchors=[list(x) for x in anchors])
    control('full_original_wilson_cover', [('four_displayed_links', mut(cover=(4, 4)), 'cover'),
                                           ('endpoints_44', mut(cover=(48, 44)), 'cover')])
    control('wrong_delta_alpha_hbar_clock', [('exponent_24', mut(clock_exponent=24), 'clock'),
                                             ('u_equals_s_over_8', mut(s=F(1, 8)), 'model changed')],
            fixture='alpha=2, hbar=3, t_E=3/2 gives s=1')
    control('vector_versus_scalar_centering',
            [('scalar_subtraction', lambda: validate_centering('scalar', F(1, 4), F(1, 100), F(-51, 10000)), 'centering'),
             ('uncentered', lambda: validate_centering('uncentered', F(1, 4), F(1, 100), F(1, 16)), 'centering'),
             ('packet_scalar', mut(centering='scalar'), 'centering')])
    control('first_order_mean_charged', [('mean_square_zero', mut(mean_square=F(0), radius=radius - terms['mean_square']), 'mean square'),
                                         ('mean_square_without_M0', mut(mean_square=Dp * Dp, radius=radius - Dp * Dp), 'mean square')],
            first_order_mean=q(m1))
    control('tau_scaling_exponent', [('sqrt_called_linear', lambda: validate_scaling('linear', *ratio_sqrt), 'tau scaling')])
    control('changed_model_relabelled', [('tau_1e-14', mut(tau=F(1, 10 ** 14)), 'model changed'),
                                         ('s_half', mut(s=F(1, 2)), 'model changed'),
                                         ('zero_triple_relabelled_uniform', mut(triple=['0', '0', '0']), 'model changed'),
                                         ('route_A_selected_reference', mut(reference='selected', route='A'), 'model changed'),
                                         ('zero_selected_model_id', mut(model_id='AQ_patterned_zero_selected'), 'model changed'),
                                         ('finite_graph_id', mut(model_id='FG(one_plaquette)'), 'model changed')])
    control('insufficient_verdict_retained',
            [('floor_relabelled_met', lambda: validate_retained(dict(retained, poisson_floor_uniform_D0={'verdict': 'met', 'lower': retained['poisson_floor_uniform_D0']['lower']}), target), 'insufficient verdict retained'),
             ('at4_form_dropped', lambda: validate_retained({k_: v for k_, v in retained.items() if k_ != 'poisson_at4_form_L1e4'}, target), 'insufficient verdict retained')])
    control('exact_arithmetic_admission', [('float_D', mut(D=float(Dp)), 'exact arithmetic'),
                                           ('decimal_radius', mut(radius='1.912e-7'), 'exact arithmetic')])
    control('root_n_misuse', [('rss', mut(combination='root_sum_square'), 'root-N'),
                              ('divide_by_64', mut(radius=radius / 64), 'radius mismatch')])
    control('no_priority_or_continuum_claim', [(k_, mut(**{k_: True}), 'forbidden claim ' + k_)
                                               for k_ in ('continuum_claim', 'scientific_priority_verified',
                                                          'resolved_interaction_shift', 'grid_claim')])
    control('kernel_identity_on_support', [('mirrored_branches', lambda: validate_support_identity([F(1), 2 * s1, 2 * s1 * s1]), 'support')])
    control('kernel_negative_atom_misread', [('atom_at_minus_one', lambda: validate_measure_support([(F(-1), F(1))]), 'negative support'),
                                             ('packet_real_line', mut(spectral_support='real line'), 'negative support')])
    control('kernel_l1_and_first_moment', [('M0_as_int_ghat', mut(M0=F(1)), 'L1 norm'),
                                           ('M1_without_pi', mut(M1_pi_power=0), 'first moment'),
                                           ('pi_upper_in_upper_bound', mut(kernel_dynamics=kd_lo, radius=radius - terms['kernel_dynamics'] + kd_lo), 'kernel dynamics')])
    control('window_linear_in_s', [('s_independent_M1', lambda: validate_linear_in_s(lambda s: F(4)), 'linear in s'),
                                   ('node_s_2', mut(s=F(2)), 'model changed')], kernel_term='51|tau|s/pi')
    need(validate_linear_in_s(lambda s: 4 * s), 'window_M1_linear')
    control('local_not_extensive_duhamel', [('extensive_norm', lambda: validate_local_slope(k_ext), 'extensive'),
                                            ('packet_extensive_k', mut(k=k_ext[2]), 'duhamel slope')],
            local_k=q(kp), extensive_k={str(N): q(v) for N, v in k_ext.items()})
    need(validate_local_slope({N: 2 * inc[N]['B_over_tau'] * a for N in inc}), 'local_slope_box_independent')
    control('uniform_label_strong_coupling', [('weak_coupling_wording', mut(label=LABEL.replace('strong', 'weak')), 'uniform label'),
                                              ('continuum_wording', mut(label='uniform SU(2) Yang-Mills continuum limit'), 'uniform label'),
                                              ('g4_wrong', mut(g4=F(96, 1) * 10 ** 10), 'uniform label'),
                                              ('uniform_flag_dropped', mut(uniform_wilson_claim=False), 'uniform label'),
                                              ('weak_coupling_flag', mut(weak_coupling_claim=True), 'forbidden claim weak_coupling_claim'),
                                              ('sign_rider', mut(riders=['uniform_wilson_mean_sign_certificate']), 'no sign certificate'),
                                              ('k2_rider', mut(riders=['K_2_uniform']), 'no sign certificate')])
    control('selected_incidence_count', [('seven_star_slope', mut(single_groups=0, selected_faces_R=0, k=F(49, 4) * a), 'selected incidence'),
                                         ('singles_as_stars', mut(stars=9, single_groups=0, k=F(63, 4) * a), 'selected incidence'),
                                         ('six_single_groups', mut(single_groups=6), 'selected incidence'),
                                         ('slope_49_with_groups_declared', mut(k=F(49, 4) * a), 'duhamel slope'),
                                         ('enumeration_without_singles', lambda: validate_incidence({2: dict(inc[2], singles=0)}), 'selected incidence')])
    need(validate_incidence(inc), 'incidence_validates')
    control('j0_resolution_declared', [('old_J0', mut(J0=F(7, 25000000)), 'j0 resolution'),
                                       ('R2_route', mut(J0_route='R2'), 'j0 resolution'),
                                       ('R2_cap_relabelled', mut(tau=F(7, 725000000)), 'model changed')])
    control('av1_tier_bound', [('reverse_refinement', mut(D=D_rev_gate), 'av1 tier bound'),
                               ('ax1_target_value', mut(D=ax1_target), 'av1 tier bound'),
                               ('zero_selected_D', mut(D=D_zero), 'av1 tier bound'),
                               ('tier_i', mut(D=D_i), 'av1 tier bound'),
                               ('sqrt_control', mut(D=Dq_hi), 'av1 tier bound'),
                               ('source_relabelled', mut(D_source='ax1_reverse_R88'), 'av1 tier bound'),
                               ('gate_bytes_edited', lambda: validate_gate_bytes(gate_bytes.replace(b'2425369125199104794263242601250', b'2425369125199104794263242601249')), 'gate sha256')],
            bound='AX1 gate decision value, hash-pinned')
    control('state_term_not_effect', [('D_over_2', mut(state=Dp, state_factor=F(1, 2), radius=radius - Dp), 'state term is not an effect')])
    control('window_fourier_sign_convention', [('theta_to_minus_theta', mut(free_atom='g(-3)/4'), 'sign convention')],
            mutated='25e^{-3}/4')
    control('tier_mixing_rejected', [('mean_square_tier_i', mut(D_tiers={'state': STATE_TIER, 'mean_square': 'tier_i', 'minus_tau': STATE_TIER}), 'tier mixing'),
                                     ('not_self_consistent', mut(D_recipe=dict(RECIPE, self_consistent=False), D=D_from_recipe(a, dict(RECIPE, self_consistent=False))), 'tier mixing'),
                                     ('pair_term_dropped', mut(D_recipe=dict(RECIPE, pair_term=False), D=D_from_recipe(a, dict(RECIPE, pair_term=False))), 'tier mixing'),
                                     ('R88_eps_density_form', mut(D_recipe=dict(RECIPE, t1_faces=88)), 'tier mixing'),
                                     ('minus_tau_reverse_tier', mut(D_tiers={'state': STATE_TIER, 'mean_square': STATE_TIER, 'minus_tau': 'ax1_reverse_R88'}), 'tier mixing')])
    control('single_producer_declared', [('two_producers_claimed', mut(producers=['forward', 'reverse']), 'single producer'),
                                         ('replay_not_required', mut(skeptic_replay_required=False), 'single producer'),
                                         ('self_review_as_independent', mut(independence='forward self-review counted as independent'), 'single producer')])
    rows = [dict(r) for r in CHECKS if r.get('kind') == 'control']
    ev = {'rows': rows, 'digest': hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()}
    required = [c_ for c_ in contract['controls'] if c_ != 'coherent_evidence_tampering']
    need(validate_evidence(ev, required), 'evidence_validates')
    bad = [dict(r) for r in rows]
    bad[3]['passed'] = False
    ev_bad = {'rows': bad, 'digest': hashlib.sha256(json.dumps(bad, sort_keys=True).encode()).hexdigest()}
    fewer = [dict(r) for r in rows if r['id'] != 'av1_tier_bound']
    ev_few = {'rows': fewer, 'digest': hashlib.sha256(json.dumps(fewer, sort_keys=True).encode()).hexdigest()}
    control('coherent_evidence_tampering', [('flip_boolean_rebind_hash', lambda: validate_evidence(ev_bad, required), 'required control not passed'),
                                            ('drop_control_rebind_hash', lambda: validate_evidence(ev_few, required), 'missing required control')])
    executed = [r['id'] for r in CHECKS if r.get('kind') == 'control']
    need(sorted(executed) == sorted(contract['controls']) and len(executed) == 25, 'all_contract_controls_executed')
    for bad_call, reason in ((lambda: calculator(Dp, (pi_lo, pi_hi), tau=1e-8), 'exact arithmetic'),
                             (lambda: calculator(Dp, (pi_lo, pi_hi), tau='2/100000000'), 'domain'),
                             (lambda: calculator(Dp, (pi_lo, pi_hi), selected='zero'), 'domain'),
                             (lambda: calculator(Dp, (pi_lo, pi_hi), state='ax1_reverse_R88'), 'domain'),
                             (lambda: calculator(Dp, (pi_lo, pi_hi), window='C1'), 'kernel switch'),
                             (lambda: calculator(Dp, (pi_lo, pi_hi), s='0'), 'domain')):
        if not rejects(bad_call, reason):
            raise CheckFailure('calculator domain')
    need(True, 'calculator_domain_rejections')

    # ---------------- producer-error previews (each still passes the Boolean: the formula must be read)
    def rad_with(D=Dp, k=kp, mean=True, state_factor=1):
        return state_factor * 2 * D + (2 * D * D if mean else 0) + k * 4 / pi_lo + arith
    errors = {
        'seven_star_slope_49': rad_with(k=F(49, 4) * a), 'reverse_refinement_D': rad_with(D=D_rev_gate),
        'ax1_target_as_D': rad_with(D=ax1_target), 'zero_selected_D': rad_with(D=D_zero),
        'zero_selected_D_and_49_slope': rad_with(D=D_zero, k=F(49, 4) * a), 'dropped_m2': rad_with(mean=False),
        'effect_D_over_2': rad_with(state_factor=F(1, 2)), 'tier_i_D': rad_with(D=D_i),
        'pair_term_dropped_D': rad_with(D=D_from_recipe(a, dict(RECIPE, pair_term=False))),
    }
    need(all(v <= target for kk, v in errors.items() if kk != 'tier_i_D') and errors['tier_i_D'] > target
         and errors['zero_selected_D_and_49_slope'] <= av2_R, 'producer_errors_invisible_to_boolean',
         previews={kk: preview(v) for kk, v in errors.items()})

    need(claims['euclidean_node_certified'] is True and all(claims[k_] is False for k_ in claims
                                                            if k_ not in ('uniform_wilson_claim', 'euclidean_node_certified')),
         'claim_flags')
    previews = {
        'D_prime': preview(Dp), 'radius': preview(radius), 'margin_target_over_radius': preview(target / radius),
        'state': preview(terms['state']), 'mean_square': preview(terms['mean_square']),
        'kernel_dynamics': preview(terms['kernel_dynamics']), 'arithmetic': preview(arith), 'free_value': preview(datum),
        's_star': preview((s_lo + s_hi) / 2), 's_star_D0': preview((s0_lo + s0_hi) / 2), 's_star_if_49': preview(s7),
        'poisson_floor_D0': preview(floor_lo), 'poisson_with_Dprime': preview(withD_lo), 'poisson_at4_form_L1e4': preview(at4_hi),
        'radius_with_calculator_primitives': preview(c_radius), 'av2_zero_selected_radius': preview(av2_R),
        'label': 'floating previews only; no admission Boolean reads them',
    }
    result = {
        'loop': 'AX2', 'stage': 'pre_comparison', 'role': 'skeptic independent replay (single-direction admission input)',
        'standing': 'model-agent skeptic with correlated ancestry; not human peer review, not formal verification',
        'human_author': 'Hruday N M (BUNZEEY)',
        'producer_files_read': [],
        'incidental_exposure': 'directory names only: research/round32/forward/ax2 exists (a listing printed only . and ..) '
                               'and /tmp/claude-0/ax2-private exists; no file name or content under either was read',
        'checker_sha256': sha_bytes(Path(__file__).read_bytes()),
        'contract_sha256': CONTRACT_SHA256, 'ax1_gate_sha256': AX1_GATE_SHA256, 'av2_gate_sha256': AV2_GATE_SHA256,
        'av2_calculator_sha256': AV2_CALC_SHA256, 'model_id': truth['model_id'], 'label': LABEL,
        'transfer': {'unchanged': ['C2 window', 'M0=2', 'M1=4s/pi', 'M2=2s^2', 'Haar reference', 'c0(theta)=e^{3i theta}/4',
                                   'datum e^{-3}/4', 'cover R={0,e_z}', 'clock s=alpha*t_E/hbar'],
                     'changed': {'k_prime': '51|tau|/4 (7 stars x 7|tau|/8 + 2 groups x |tau|/8, doubled)',
                                 'D_prime': q(Dp)}},
        'state_values': {'D_prime_bound': q(Dp), 'reverse_refinement_not_used': q(D_rev_gate), 'tier_i_not_used': q(D_i),
                         'ax1_target_not_used': q(ax1_target), 'zero_selected_D_not_used': q(D_zero)},
        'pi_bracket': {'lower': q(pi_lo), 'upper': q(pi_hi), 'method': 'Hutton 8atan(1/3)+4atan(1/7), outward to 1e-60; Machin and admitted-calculator overlap'},
        'free_reference': {'value': 'e^{-3}/4', 'lower': q(f_lo), 'upper': q(f_hi), 'datum': q(datum),
                           'method': 'Taylor with geometric remainder, halving and outward squaring, inversion'},
        'radius': {
            'formula': "E'=M0(D'+D'^2)+k' M1 + arithmetic = 2(D'+D'^2)+51|tau|s/pi + arithmetic, s=1",
            'terms_exact': {key: q(v) for key, v in terms.items()},
            'kernel_dynamics_with_pi_hi': q(kd_lo), 'pi_rounding_slack_inside_kernel_dynamics': q(terms['kernel_dynamics'] - kd_lo),
            'radius_exact': q(radius), 'radius_upper_1e-40': q(rup(radius, 10 ** 40)),
            'radius_with_admitted_calculator_primitives': q(c_radius), 'calculator_datum_equals_av2_gate_datum': c_datum == av2_datum,
            'common_outward_bound_1e-40': q(R_common),
            'common_interval': {'datum': q(av2_datum), 'radius': q(R_common), 'lower': q(common_lo), 'upper': q(common_hi),
                                'lower_1e-16': q(rdown(common_lo, 10 ** 16)), 'upper_1e-16': q(rup(common_hi, 10 ** 16))},
            'interval': {'lower': q(lo_int), 'upper': q(hi_int)},
            'target': q(target), 'target_met': target_met, 'margin_lower': q(rdown(target / radius, 10 ** 9)),
            'reference_inside': True, 'sub_label': 'reference_unresolved',
            'minus_tau': {'radius_exact_equal': radii['minus'][1] == radius, 'role': 'U_E mirror; replay of the same |tau| formula'},
        },
        'crossover': {'s_star_lower': q(s_lo), 's_star_upper': q(s_hi), 's_star_D0_lower': q(s0_lo), 's_star_D0_upper': q(s0_hi),
                      'scope': 'crossover of the formula only; s=1 is the only preregistered node; no grid claim'},
        'poisson_retained': retained,
        'previews': previews,
        'checks': CHECKS,
    }
    result.update(claims)
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
