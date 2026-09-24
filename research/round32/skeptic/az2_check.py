#!/usr/bin/env python3
"""Round32 AZ2 skeptic pre-comparison replay (finite two-plaquette graph).

Written after the AZ2 contract froze, from the frozen contract, selection-az2.md,
panel-update-4.md, the Round11 README/advisor/solver (conventions only; the
solver imports numpy and is NOT imported here), the AW1 gate and forward
report (the I1.5 sign and the one-plaquette fixture), the modern lens update-4
and its assistant rehearsals (read as previews), and AGENTS.md, before reading
anything of the AZ2 producer. From research/round32/forward/az2/ this program
touches only inputs/, whose files it hashes (bytes only, never parsed) against
the repository. Standard library only; every admission Boolean is decided with
fractions.Fraction and directed rational rounding. Floats appear only in the
labelled 'previews' block. Every check and control raises an explicit exception,
so python -O cannot disable it. Model-agent skeptic with correlated ancestry;
not human peer review, not formal verification.

Model FG(two-plaquette, D in {6,8}, tau_FG grid, I1.5, gauge-invariant):
H_FG = K - tau_FG*x on the gauge-invariant L^2 of the Round11 graph (alpha=1,
rho=1, second face uncoupled), K = sum of the seven link Casimirs, x=(1/2)Tr U
for the square U = vM h3^-1 vL^-1 h1. What is computed here:
  * own Haar moments (Beta-function route) cross-checked against the Round11
    semicircle/uniform-u route; own kinetic operator in Round11 coordinates,
    checked on the Round11 fixtures and the Casimir labels (E1)=(E2);
  * the x-only sector: Chebyshev U_k(x) are orthonormal characters with
    K U_k = k(k+2) U_k and x U_k = (U_{k+1}+U_{k-1})/2, and U_{D+1} is orthogonal
    to every monomial of degree <= D, so the Round11 Galerkin block on the
    x-only monomials is exactly the Jacobi matrix diag(k(k+2)) - (tau_FG/2)(shift);
  * route C (primary): certified full-graph enclosures of <W>(tau_FG) at
    tau_FG in {+-1/1000, +-1/100, +-1/10}, D in {6,8}, from the exact full-space
    residual of a rational Ritz vector (P-part plus the exact one-component leak
    into shell D+1) and the full-space separation 3-|tau_FG| (Weyl from the free
    gap 3), converted by the spectral-measure (Davis-Kahan) bound;
  * route F (cross-check): Hellmann-Feynman plus concavity of E_0(tau_FG), upper
    energies from the Ritz value, lower energies from the Round11 Feshbach bound
    with the certified tail floor m_{D+1}-|tau_FG| (45 and 69 before the shift);
  * the Round11 monomial pencils at D=6 (84) and D=8 (165): exact inertia at the
    Jacobi bracket endpoints, the first-order Galerkin identity K(x/3)=x.1 with
    kernel(K)=constants (derivative 1/6 on the finite basis), and the centre-flip
    congruence that makes -tau_FG an exact mirror;
  * exact Rayleigh-Schrodinger coefficients (Jacobi route and untruncated
    Round11-monomial route), the tail floors per channel, the dictionary, and the
    20 contract controls (plus 3 extra) as damaging mutations of a packet.

Usage: python3 -B research/round32/skeptic/az2_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction as F
from functools import lru_cache
from math import comb, factorial, isqrt
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / 'research/round32/contracts/az2.json'
CONTRACT_SHA256 = '2861d5c59841b5b8e688712aab4faf3edf9f9f8ee2079d8ebbda07fabb7461c3'
PINNED = {
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/forward/aw1/report.md': 'ea3a936244a31c7ea4d2c8de65798b2bb0fc65a60437122b71a30465e089d883',
    'research/round11/solver/two_plaquette.py': 'ae9084850538ebf523f8c34564352b48ce0b30d07955991d4b4d1980ab36ce43',
    'research/round11/solver/README.md': '9439177f8213c4c2b72ee7ac81236ee4b485d585591fbfde0a8fe1aceb5918c4',
    'research/round11/advisor/advisor.md': '5a4853e4bbec267c7320457632c7e9346f85e3e3aa781acefd3291f4a9d1bb32',
    'research/round32/advisor/selection-az2.md': '5e2fbae50c68ff1288286ca39f05d3910c9b287df4a4b23bacfc8dc750ba1661',
    'research/round32/experts/modern/update-4.md': '5a0aa5077fe3e044f5c601c99cc7c978e50e54b075b869dd6d5ad659fbd0aadd',
    'research/round32/methods/paired-physics-research/references/complete-residual-and-error-scope.md':
        '9e387df64ae05738e740d2ff65973cef0672530e64344ab9e730a139b81b435d',
}
INPUTS = ROOT / 'research/round32/forward/az2/inputs'
MODEL_ID = 'FG(two-plaquette, D in {6,8}, tau_FG grid, I1.5, gauge-invariant)'
LINKS_U = ('h1', 'vL', 'h3', 'vM')           # square U = vM h3^-1 vL^-1 h1 (Round11 G2)
LINKS_V = ('h2', 'vR', 'h4')                 # square V minus the shared link
ALL_LINKS = ('h1', 'h2', 'h3', 'h4', 'vL', 'vM', 'vR')
EXTRA_CONTROLS = ('ground_sector_spectator_disclosed', 'minus_tau_mirror_replay', 'truncated_bracket_not_full_graph')
OUT_DEN = 10 ** 60          # outward rounding of reported endpoints
SQRT_DEN = 10 ** 100        # directed square roots
BRACKET_W = F(1, 10 ** 90)  # Sturm bisection width for the Ritz eigenvalue


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
    try:
        fn()
    except Rejected as exc:
        if reason not in str(exc):
            raise CheckFailure('rejected for the wrong reason: %s (expected %s)' % (exc, reason))
        return True
    return False


def control(cid, mutations, **detail):
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
    return format(float(x), '.13e')


def rdown(x, den=OUT_DEN):
    return F((x.numerator * den) // x.denominator, den)


def rup(x, den=OUT_DEN):
    return F(-((-x.numerator * den) // x.denominator), den)


def dec(x, digits, up):
    """Exact decimal text of x rounded down (up=False) or up (up=True) at 10^-digits."""
    n = x * 10 ** digits
    k = -((-n.numerator) // n.denominator) if up else n.numerator // n.denominator
    sign, k = ('-', -k) if k < 0 else ('', k)
    ip, fp = divmod(k, 10 ** digits)
    return '%s%d.%0*d' % (sign, ip, digits, fp)


def sqrt_up(x, den=SQRT_DEN):
    """Smallest r/den with (r/den)^2 >= x (x >= 0 rational)."""
    if x < 0:
        raise CheckFailure('sqrt domain')
    r = isqrt((x.numerator * den * den) // x.denominator)
    while F(r * r, den * den) < x:
        r += 1
    return F(r, den)


def sqrt_down(x, den=SQRT_DEN):
    r = isqrt((x.numerator * den * den) // x.denominator)
    while F(r * r, den * den) > x:
        r -= 1
    return F(r, den)


# ---------------------------------------------------------------- Haar moments (two routes)
@lru_cache(None)
def ex(p, k):
    """E[x^p (1-x^2)^k], x=(1/2)Tr U with density (2/pi)sqrt(1-x^2): (2/pi)B((p+1)/2, k+3/2)."""
    if p % 2:
        return F(0)
    h = p // 2
    g1 = F(factorial(2 * h), 4 ** h * factorial(h))            # Gamma(h+1/2)/sqrt(pi)
    g2 = F(factorial(2 * k + 2), 4 ** (k + 1) * factorial(k + 1))  # Gamma(k+3/2)/sqrt(pi)
    return 2 * g1 * g2 / factorial(h + k + 1)


@lru_cache(None)
def mom(a, b, c):
    """E[x^a y^b z^c]; z=(1/2)Tr(UV)=xy - |u||v| cos, cos uniform on [-1,1] (independent isotropic axes)."""
    s = F(0)
    for m in range(0, c + 1, 2):
        s += F(comb(c, m), m + 1) * ex(a + c - m, m // 2) * ex(b + c - m, m // 2)
    return s


def mom_round11_route(a, b, c):
    """The Round11 route written separately: Catalan moments and binomial expansion of (1-x^2)^k."""
    def xp(n):
        if n % 2:
            return F(0)
        m = n // 2
        return F(comb(2 * m, m), 4 ** m * (m + 1))

    def rad(n, k):
        return sum((F((-1) ** j * comb(k, j)) * xp(n + 2 * j) for j in range(k + 1)), F(0))
    return sum((F(comb(c, 2 * k), 2 * k + 1) * rad(a + c - 2 * k, k) * rad(b + c - 2 * k, k) for k in range(c // 2 + 1)), F(0))


# ---------------------------------------------------------------- polynomials in (x, y, z)
ONE = {(0, 0, 0): F(1)}
PX = {(1, 0, 0): F(1)}
PY = {(0, 1, 0): F(1)}
PZ = {(0, 0, 1): F(1)}


def padd(p, r, s=F(1)):
    out = dict(p)
    for k, v in r.items():
        out[k] = out.get(k, F(0)) + s * v
    return {k: v for k, v in out.items() if v}


def pmul(p, r):
    out = {}
    for k1, v1 in p.items():
        for k2, v2 in r.items():
            k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            out[k] = out.get(k, F(0)) + v1 * v2
    return {k: v for k, v in out.items() if v}


def pscale(p, s):
    return {k: s * v for k, v in p.items() if s * v}


def pder(p, i):
    out = {}
    for k, v in p.items():
        if k[i]:
            j = list(k)
            j[i] -= 1
            out[tuple(j)] = out.get(tuple(j), F(0)) + v * k[i]
    return out


def kinetic(p, rho=F(1)):
    """Round11 K_rho in (x,y,z) coordinates (solver README): 3C_A+3C_B+rho C_shared."""
    out = {}
    for i, co in enumerate((PX, PY, PZ)):
        out = padd(out, pmul(co, pder(p, i)), 3 * (3 + rho) / 4 if i < 2 else F(9, 2))
        out = padd(out, pmul(padd(ONE, pmul(co, co), F(-1)), pder(pder(p, i), i)), -(3 + rho) / 4 if i < 2 else F(-3, 2))
    out = padd(out, pmul(padd(PZ, pmul(PX, PY), F(-1)), pder(pder(p, 0), 1)), -rho / 2)
    out = padd(out, pmul(padd(PY, pmul(PX, PZ), F(-1)), pder(pder(p, 0), 2)), F(-3, 2))
    out = padd(out, pmul(padd(PX, pmul(PY, PZ), F(-1)), pder(pder(p, 1), 2)), F(-3, 2))
    return out


def mean(p):
    return sum((v * mom(*k) for k, v in p.items()), F(0))


def inner(p, r):
    return mean(pmul(p, r))


def deg(p):
    return max((sum(k) for k in p), default=-1)


def basis(D):
    return [(a, b, n - a - b) for n in range(D + 1) for a in range(n + 1) for b in range(n - a + 1)]


def eps(a, b, c, rho=F(1)):
    """Casimir label energy: 3j(j+1)+3s(s+1)+rho*l(l+1), j=(a+c)/2, s=(b+c)/2, l=(a+b)/2."""
    j, s, l = F(a + c, 2), F(b + c, 2), F(a + b, 2)
    return 3 * j * (j + 1) + 3 * s * (s + 1) + rho * l * (l + 1)


def m_shell(d):
    return min(eps(a, b, d - a - b) for a in range(d + 1) for b in range(d - a + 1))


def chebyshev_u(n):
    """U_k(x) with x=cos(theta): the SU(2) character chi_{k/2}(U) as a polynomial in x=(1/2)Tr U."""
    us = [ONE, {(1, 0, 0): F(2)}]
    while len(us) <= n:
        us.append(padd(pmul({(1, 0, 0): F(2)}, us[-1]), us[-2], F(-1)))
    return us[:n + 1]


# ---------------------------------------------------------------- exact symmetric inertia
def inertia(A):
    A = [row[:] for row in A]
    neg = zero = pos = 0
    while A:
        n = len(A)
        piv = next((i for i in range(n) if A[i][i]), None)
        if piv is None:
            if any(any(r) for r in A):
                raise CheckFailure('inertia: zero diagonal with nonzero off-diagonal (not expected here)')
            zero += n
            break
        if piv:
            A[0], A[piv] = A[piv], A[0]
            for row in A:
                row[0], row[piv] = row[piv], row[0]
        p = A[0][0]
        if p < 0:
            neg += 1
        else:
            pos += 1
        r0 = A[0]
        A = [[A[i][j] - A[i][0] * r0[j] / p for j in range(1, n)] for i in range(1, n) ]
    return neg, zero, pos


# ---------------------------------------------------------------- the x-only (s=0) sector: Jacobi matrix
def kk(k):
    return F(k * (k + 2))


def sturm_below(D, t, lam, top_shift=F(0)):
    """Number of eigenvalues < lam of J_D(t) - top_shift*e_D e_D^T; None if lam hits a pivot zero."""
    b2 = (t / 2) ** 2
    cnt, prev = 0, None
    for k in range(D + 1):
        d = kk(k) - lam - (top_shift if k == D else 0) - (b2 / prev if k else 0)
        if d == 0:
            return None
        cnt += d < 0
        prev = d
    return cnt


def ground_bracket(D, t, width=BRACKET_W, top_shift=F(0)):
    lo, hi = F(-4), F(2)
    if sturm_below(D, t, lo, top_shift) != 0 or sturm_below(D, t, hi, top_shift) != 1:
        raise CheckFailure('ground bracket start')
    while hi - lo > width:
        for div in (2, 3, 5, 7, 11):
            mid = lo + (hi - lo) / div
            c = sturm_below(D, t, mid, top_shift)
            if c is not None:
                break
        else:
            raise CheckFailure('no admissible bisection point')
        if c == 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


def back_vector(D, t, lam):
    """Three-term recurrence from the top: (Hv)_k = lam v_k exactly for k=1..D; residual in row 0 and row D+1."""
    v = [F(0)] * (D + 2)
    v[D] = F(1)
    for k in range(D, 0, -1):
        v[k - 1] = 2 * (kk(k) - lam) * v[k] / t - v[k + 1]
    return v[:D + 1]


def apply_H(v, t):
    """Full-space action of H=K-t x on sum_k v_k U_k (k<=D): components 0..D+1."""
    D = len(v) - 1
    out = [F(0)] * (D + 2)
    for k in range(D + 1):
        out[k] += kk(k) * v[k]
        out[k + 1] -= t * v[k] / 2
        if k:
            out[k - 1] -= t * v[k] / 2
    return out


def route_c(D, t):
    """Certified full-graph enclosure of <W>(t) by the exact full-space residual and the separation 3-|t|."""
    if t == 0:                                    # own free reference in the same routine
        v, lo, hi = [F(1)] + [F(0)] * D, F(0), F(0)
    else:
        lo, hi = ground_bracket(D, t)
        v = back_vector(D, t, (lo + hi) / 2)
    nv = sum(a * a for a in v)
    Hv = apply_H(v, t)
    rho = sum(Hv[k] * v[k] for k in range(D + 1)) / nv
    r = [Hv[k] - (rho * v[k] if k <= D else 0) for k in range(D + 2)]
    p2 = sum(a * a for a in r[:D + 1]) / nv            # (d) Galerkin part of the residual (rational Ritz vector)
    leak2 = r[D + 1] ** 2 / nv                          # (a)+(b): the exact omitted-shell component
    xv = sum(v[k] * v[k + 1] for k in range(D)) / nv
    sep = 3 - abs(t)
    if not rho < sep:
        raise CheckFailure('separation')
    leak_up, p_up = sqrt_up(leak2), sqrt_up(p2)
    items = {'a_per_link_leak': 2 * leak_up / (sep - rho), 'b_joint': F(0), 'c_gauge': F(0),
             'd_ritz': 2 * p_up / (sep - rho)}
    # (e) arithmetic: square-root rounding slack plus outward rounding of both endpoints
    exact_rad = items['a_per_link_leak'] + items['d_ritz']
    lo_x, hi_x = rdown(xv - exact_rad), rup(xv + exact_rad)
    items['e_arithmetic'] = max((xv - exact_rad) - lo_x, hi_x - (xv + exact_rad)) \
        + 2 * ((leak_up - sqrt_down(leak2)) + (p_up - sqrt_down(p2))) / (sep - rho)
    return {'E_ritz': (lo, hi), 'rho': rho, 'xv': xv, 'p2': p2, 'leak2': leak2, 'sep': sep, 'items': items,
            'radius': exact_rad, 'lower': lo_x, 'upper': hi_x, 'vD': v[D], 'nv': nv, 'v': v}


def route_f(D, t, h, floor):
    """HF + concavity: <W>(t) in [(Elo(t-h)-Ehi(t))/h, (Ehi(t)-Elo(t+h))/h]; Feshbach lower energies with the tail floor."""
    def upper(tt):
        return ground_bracket(D, tt, F(1, 10 ** 80))[1]

    def lower(tt):
        R = upper(tt)
        fl = floor - abs(tt)
        if not R < fl:
            raise CheckFailure('Feshbach: R must lie below the tail floor')
        shift = (tt / 2) ** 2 / (fl - R)                  # C C^* = (t/2)^2 e_D e_D^T in the x-only sector
        lo_b = ground_bracket(D, tt, F(1, 10 ** 80), top_shift=shift)[0]
        if not lo_b <= R:
            raise CheckFailure('Feshbach: lambda_min(B) above R')
        return lo_b, shift
    e0 = upper(t)
    lm, _ = lower(t - h)
    lp, shift = lower(t + h)
    return {'lower': (lm - e0) / h, 'upper': (e0 - lp) / h, 'h': h, 'feshbach_shift_at_t_plus_h': shift}


def ritz_only(D, t, h):
    """Retained insufficient row: truncated-matrix brackets only (encloses the D-truncated <W>_D, no tail)."""
    b = {tt: ground_bracket(D, tt, F(1, 10 ** 80)) for tt in (t - h, t, t + h)}
    return (b[t - h][0] - b[t][1]) / h, (b[t][1] - b[t + h][0]) / h


def jacobi_rs(D, order):
    """Exact Rayleigh-Schrodinger for J_D(t), intermediate normalisation; returns E_n (n=0..order)."""
    n = D + 1
    psi = [[F(1)] + [F(0)] * (n - 1)]
    E = [F(0)]
    for m in range(1, order + 1):
        prev = psi[m - 1]
        xp = [F(0)] * n
        for k in range(n):
            if prev[k]:
                if k + 1 < n:
                    xp[k + 1] += prev[k] / 2
                if k:
                    xp[k - 1] += prev[k] / 2
        Vp = [-a for a in xp]
        E.append(Vp[0])
        rhs = [-Vp[k] + sum(E[i] * psi[m - i][k] for i in range(1, m + 1)) for k in range(n)]
        psi.append([F(0)] + [rhs[k] / kk(k) for k in range(1, n)])
    return E


def poly_rs(V, order):
    """Untruncated exact RS in Round11 monomial coordinates: psi^(n) solved shell by shell (K triangular in degree)."""
    def solve_k(f):
        f, psi = dict(f), {}
        while f:
            top = deg(f)
            if top == 0:
                if any(f.values()):
                    raise CheckFailure('poly RS: nonzero mean in the source')
                break
            part = {k: v / eps(*k) for k, v in f.items() if sum(k) == top}
            psi = padd(psi, part)
            f = padd(f, kinetic(part), F(-1))
        m = mean(psi)
        return padd(psi, {(0, 0, 0): -m}) if m else psi
    psi, E = [ONE], [F(0)]
    for n in range(1, order + 1):
        E.append(mean(pmul(V, psi[n - 1])))
        rhs = pscale(pmul(V, psi[n - 1]), F(-1))
        for k in range(1, n + 1):
            rhs = padd(rhs, psi[n - k], E[k])
        psi.append(solve_k(rhs))
    N = [sum(inner(psi[i], psi[n - i]) for i in range(n + 1)) for n in range(order)]
    Xn = [sum(inner(psi[i], pmul(PX, psi[n - i])) for i in range(n + 1)) for n in range(order)]
    w = []
    for n in range(order):
        w.append(Xn[n] - sum(w[k] * N[n - k] for k in range(n)))
    return E, w


# ---------------------------------------------------------------- monomial (Round11-basis) pencils
def monomial_forms(D):
    bs = basis(D)
    n = len(bs)
    G = [[mom(bs[i][0] + bs[j][0], bs[i][1] + bs[j][1], bs[i][2] + bs[j][2]) for j in range(n)] for i in range(n)]
    MX = [[mom(bs[i][0] + bs[j][0] + 1, bs[i][1] + bs[j][1], bs[i][2] + bs[j][2]) for j in range(n)] for i in range(n)]
    kp = [kinetic({m: F(1)}) for m in bs]
    Kf = [[inner({bs[i]: F(1)}, kp[j]) for j in range(n)] for i in range(n)]
    return bs, G, Kf, MX


def pencil(Kf, MX, G, t, lam):
    n = len(G)
    return [[Kf[i][j] - t * MX[i][j] - lam * G[i][j] for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------- packet validator (the AZ2 semantics as read here)
TEMPLATE_KEY = 'mandatory_sentence_template'


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


TEXT_KEYS = frozenset(('reason', 'channel', 'membership', 'note', 'bound_from', 'verdict', 'role', 'floor_source',
                       'combination', 'method', 'imported'))


def walk_exact(obj, name):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in TEXT_KEYS or v == 'not_applicable':
                continue
            walk_exact(v, name + '.' + str(k))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            walk_exact(v, '%s[%d]' % (name, i))
    elif isinstance(obj, bool) or obj is None:
        return
    else:
        exact(obj, name)


def forbidden_hits(text, phrases):
    hits = []
    for ph in phrases:
        if re.search(r'(?<![A-Za-z])' + re.escape(ph) + r'(?![A-Za-z])', text, re.I):
            hits.append(ph)
    return hits


def validate_packet(p, truth):
    # 10 exact arithmetic
    for key in ('enclosures', 'ledger', 'coefficients', 'own_free_reference', 'tail', 'scaling'):
        walk_exact(p[key], key)
    exact(p['derivative_at_zero'], 'derivative_at_zero')
    # 13 finite-graph model id
    if p['model_id'] != MODEL_ID or p['model_is_finite_graph'] is not True or p['coupling_name'] != 'tau_FG':
        raise Rejected('finite-graph model id: FG(...) label, model_is_finite_graph:true and the coupling named tau_FG')
    # 7 changed model relabelled
    g = p['graph']
    h = p['hamiltonian']
    if g != truth['graph'] or p['cutoffs'] != [6, 8] or p['dimensions'] != {'6': 84, '8': 165} \
            or p['tau_grid'] != truth['tau_grid'] or p['signs'] != ['+', '-'] \
            or h['alpha'] != '1' or h['rho'] != '1' or h['faces_coupled'] != ['U'] or h['lambda2'] != '0' \
            or sorted(p['enclosures']) != ['6', '8'] \
            or any(sorted(p['enclosures'][d]) != sorted(truth['points']) for d in p['enclosures']):
        raise Rejected('model changed or relabelled: graph, cutoffs, dimensions, grid, alpha=rho=1 and one coupled face are frozen')
    # 3 units (the legacy clock control, read for a static finite graph)
    u = p['units']
    if u != {'energy': 'alpha_FG=1 (Round11 alpha)', 'dictionary': 'tau_FG=tau/24',
             'z3_face_term': '-(tau/3)W_f in delta=alpha/8 units = -(tau/24)W_f in alpha units'} or 'clock' in p:
        raise Rejected('units: alpha_FG=1, tau_FG=tau/24 from delta=alpha/8; a static ground-state observable has no clock')
    # 2 full Wilson cover
    ob = p['observable']
    if ob['name'] != 'W=x=(1/2)Tr U' or tuple(ob['links']) != LINKS_U:
        raise Rejected('wilson cover: W is the full four-link square U (h1, vL, h3 and the shared vM)')
    # 4 centering
    if ob['centering'] != 'none' or ob.get('reference_subtracted') not in (None, '0'):
        raise Rejected('centering: the preregistered observable is uncentered (<W>, own free value 0)')
    # 19 sign convention fixture
    sc = p['sign_convention']
    if sc['rule'] != 'I1.5: V=-tau_FG*W' or sc['fixture_first_order'] != '+1/6':
        raise Rejected('sign convention: I1.5 gives V=-tau_FG*W and a fixture slope +1/6')
    # 5 first-order mean charged
    if exact(p['derivative_at_zero'], 'derivative') != F(1, 6):
        raise Rejected('first-order mean: d<W>/dtau_FG at 0 is exactly 1/6 (nonzero; parity does not kill it)')
    for d, rows in p['enclosures'].items():
        for key, (lo, hi) in rows.items():
            t = F(key)
            lo, hi = exact(lo, 'lo'), exact(hi, 'hi')
            if not ((t > 0 and lo > 0) or (t < 0 and hi < 0)):
                raise Rejected('first-order mean: every enclosure excludes the free value 0 with the sign of tau_FG')
    # 16 own free reference
    fr = p['own_free_reference']
    if fr != {'W': '0', 'E0': '0', 'free_gap': '3', 'E_W2': '1/4', 'same_code_path': True, 'imported': None}:
        raise Rejected('own free reference: computed on the graph in the same routine; nothing imported from Z^3')
    # enclosure containment against the certified truth
    for d, rows in p['enclosures'].items():
        for key, (lo, hi) in rows.items():
            tl, th = truth['enclosures'][d][key]
            if not (F(lo) <= F(hi) and F(lo) <= th and F(hi) >= tl):
                raise Rejected('enclosure: disjoint from the certified enclosure at D=%s tau_FG=%s' % (d, key))
    # 18 coefficients not fitted
    co = p['coefficients']
    if p['fg_coefficients_fitted'] is not False or co['method'] != truth['coefficients']['method'] \
            or co['W'] != truth['coefficients']['W'] or co['E'] != truth['coefficients']['E']:
        raise Rejected('fitted coefficients: coefficients come from exact Rayleigh-Schrodinger algebra, never from enclosures')
    # 6 tau scaling exponent
    sca = p['scaling']
    if sca['first_order_exponent'] != 1 or sca['remainder_exponent'] != 3 \
            or not (F(990) <= F(sca['remainder_ratio_bracket'][0]) and F(sca['remainder_ratio_bracket'][1]) <= F(1000)):
        raise Rejected('tau scaling: first order exponent 1 and remainder exponent 3 (ratio near 1000 per decade)')
    # 20, 14, 15, 1, 11 residual ledger
    for d, rows in p['ledger'].items():
        for key, led in rows.items():
            tr = truth['ledger'][d][key]
            for part in ('a_per_link', 'b_joint', 'c_gauge', 'd_ritz', 'e_arithmetic'):
                item = led.get(part)
                if item is None:
                    raise Rejected('ledger itemization: part %s missing' % part)
                if item.get('value') == 'not_applicable' and not item.get('reason'):
                    raise Rejected('ledger itemization: not_applicable needs a stated reason (%s)' % part)
            if 'a_plus_b' in led:
                raise Rejected('ledger itemization: per-link and joint parts are separate items')
            links = led['a_per_link']['links']
            if tuple(sorted(links)) != tuple(sorted(ALL_LINKS)) \
                    or led['b_joint']['channel'] != 'all seven link spins <= D/2 and j+s+l >= D+1' \
                    or led['bound_from'] != 'exact full-space residual' \
                    or any(links[e] != tr['a_per_link']['links'][e] for e in ALL_LINKS):
                raise Rejected('all channels: seven per-link tails plus the joint channel, from the exact residual')
            if F(led['floor']) != tr['floor'] or led['floor_source'] != tr['floor_source']:
                raise Rejected('representation tail: floor m_{D+1}-|tau_FG| over the entire omitted space')
            if led['leak_included'] is not True or F(led['leak_norm2']) != tr['leak_norm2'] \
                    or F(led['feshbach_coupling_square']) != tr['feshbach_coupling_square']:
                raise Rejected('incoming coupling: the omitted-shell coupling (the leak) enters the residual and the lower bound')
            parts = sum((F(led[k]['value']) for k in ('d_ritz', 'e_arithmetic')), F(led['a_per_link']['value']) + F(led['b_joint']['value']))
            if led['combination'] != 'linear' or F(led['radius']) < parts:
                raise Rejected('root-N: ledger items add linearly into the radius')
    if {k: F(v) for k, v in p['tail'].items()} != {'6': F(45), '8': F(69)}:
        raise Rejected('representation tail: tail_lower(6)=45 and tail_lower(8)=69')
    # 9 insufficient verdict retained
    ret = p['retained']
    for key in ('ritz_only_truncated_bracket', 'heuristic_tau2_over_tail', 'single_omitted_element'):
        if key not in ret or ret[key].get('verdict') != 'insufficient':
            raise Rejected('insufficient verdict retained: ' + key)
    # extras
    if p['enclosure_route'] != truth['enclosure_route']:
        raise Rejected('truncated: a Ritz bracket of the truncated matrix is not a full-graph enclosure')
    if p['ground_sector'] != truth['ground_sector']:
        raise Rejected('spectator: the second square is a spectator in the ground sector (AW1 fixture identity) and must be disclosed')
    if p['minus_tau_role'] != 'exact mirror replay (centre flip on one U link), not a second confirmation':
        raise Rejected('mirror: -tau_FG is an exact centre-flip replay')
    # 12 no priority or continuum claim
    for key in ('continuum_claim', 'scientific_priority_verified', 'weak_coupling_claim', 'resolves_roadmap_goal_2'):
        if p['claims'][key] is not False:
            raise Rejected('forbidden claim ' + key)
    hits = forbidden_hits(p['report_text'], truth['forbidden_phrasings'])
    if hits:
        raise Rejected('forbidden claim phrasing: ' + ', '.join(hits))
    # 17 no transfer to AQ
    if p['claims']['transfers_to_aq'] is not False or truth[TEMPLATE_KEY] not in p['report_text'] \
            or re.search(r'K_2|AQ (model|limit|state)', p['report_text'].replace(truth[TEMPLATE_KEY], '')) \
            or p['dictionary'] != {'tau_FG': 'tau/24', 'fg_first_order': '1/6', 'z3_first_order': '1/144', 'role': 'consistency_only'}:
        raise Rejected('transfer to AQ: transfers_to_aq false, the template verbatim, no AQ or K_2 sentence, dictionary as consistency only')
    if p['sub_label'] != 'sign_certified_finite_graph':
        raise Rejected('sub-label')
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


# ---------------------------------------------------------------- main computation
def execute():
    contract_bytes = CONTRACT.read_bytes()
    need(sha_bytes(contract_bytes) == CONTRACT_SHA256, 'contract_sha256_bound')
    contract = json.loads(contract_bytes)
    pre = contract['preregistration']
    pinned_text = {}
    for rel, sha in PINNED.items():
        b = (ROOT / rel).read_bytes()
        if sha_bytes(b) != sha:
            raise CheckFailure('pinned source changed: ' + rel)
        pinned_text[rel] = b.decode()
    need(True, 'pinned_sources_sha256', files=sorted(PINNED))

    # ---------------- contract reading
    ctrl = contract['controls']
    need(ctrl == pre['controls_required']['ids'] and len(ctrl) == 20 and len(set(ctrl)) == 20, 'control_mirror_20_equals_20')
    need(pre['gate_fields_required'] == {'transfers_to_aq': False, 'model_is_finite_graph': True, 'fg_coefficients_fitted': False}
         and pre['forbidden_phrasings'] == ['predicts', 'confirms the Z^3 value'] and pre['model_id'] == MODEL_ID
         and contract['producers'] == ['forward'] and contract['direction'] == 'single+skeptic'
         and contract['single_direction_independent_replay'] is True, 'preregistration_fields')
    grid = [F(s) for s in contract['parameters']['tau_FG_grid']]
    need(grid == [F(1, 1000), F(1, 100), F(1, 10)] and pre['tau']['signs_evaluated'] == ['+', '-'], 'tau_grid_read_from_contract',
         grid=[q(x) for x in grid])
    cut = contract['parameters']['cutoff']
    need(all(s in cut for s in ('84 at D=6', '165 at D=8', '45 at D=6', '69 at D=8', 'C(D+3,3)'))
         and comb(6 + 3, 3) == 84 and comb(8 + 3, 3) == 165 and len(basis(6)) == 84 and len(basis(8)) == 165,
         'cutoff_dimensions_read_from_contract')
    nd = contract['parameters']['normalization_dictionary']
    need('tau_FG=tau/24' in nd and '1/6 <-> 1/144' in nd and 'consistency only' in nd, 'dictionary_read_from_contract')
    template = pre[TEMPLATE_KEY]
    need(forbidden_hits(template, pre['forbidden_phrasings']) == [] and '1/144' in template, 'template_passes_forbidden_scan')
    need(contract['selected_after'] == 'research/round32/advisor/az1-gate.json', 'selected_after_names_az1_gate',
         note='wording defect: AZ1 and AZ2 were frozen together; the named gate did not exist at freeze (checked by listing, 2026-09-24)')
    need(pre['error_terms_itemized'] == ['truncation_jmax', 'eigenvector_residual', 'arithmetic'], 'prereg_error_terms_three_legacy_items',
         note='wording defect: three legacy items versus the five ledger parts of required item 1')

    # ---------------- pinned-source strings (conventions and admitted values)
    solver = pinned_text['research/round11/solver/two_plaquette.py']
    need(all(s in solver for s in ('return [(a,b,n-a-b) for n in range(d+1) for a in range(n+1) for b in range(n-a+1)]',
                                   'if r==1: return a*(F(5,8)*d*d+2*d+F(3,8)*(d%2))',
                                   'out=add(out,mul(add(Z,mul(X,Y),-1),deriv(deriv(p,0),1)),-r/2)',
                                   'def parameters(alpha=1,lambda1=0,lambda2=0,rho=1):',
                                   "if a<=0 or r<=0 or l1<0 or l2<0: raise ValueError")),
         'round11_solver_conventions_pinned', note='basis(d), tail_lower, kinetic cross term, default alpha=rho=1; negative lambda rejected by the API')
    aw1_gate = json.loads(pinned_text['research/round32/advisor/aw1-gate.json'])
    need('the exact first-order Wilson mean +tau/144 under I1.5' in aw1_gate['decision'], 'aw1_gate_first_order_plus_tau_over_144')
    aw1_rep = pinned_text['research/round32/forward/aw1/report.md']
    need('`H_0=32j(j+1)`, `V=-(tau/3)W`' in aw1_rep and '`<W>=tau/144+0·tau^2-(5/11943936)tau^3+...`' in aw1_rep,
         'aw1_one_plaquette_fixture_line')
    need('ground projection distance <=rho/(b-mu)' in pinned_text[
        'research/round32/methods/paired-physics-research/references/complete-residual-and-error-scope.md'], 'residual_method_reference')

    # ---------------- producer input snapshot inventory (bytes hashed only)
    declared = sorted(['AGENTS.md', 'research/round32/contracts/az2.json'] + contract['shared_premises'])
    have = sorted(str(p.relative_to(INPUTS)) for p in INPUTS.rglob('*') if p.is_file())
    mism = [r for r in declared if sha_bytes((INPUTS / r).read_bytes()) != sha_bytes((ROOT / r).read_bytes())] if have == declared else ['inventory']
    need(have == declared and len(have) == 28 and mism == [], 'producer_inputs_28_byte_identical_to_repository',
         note='inputs/ only; hashed, not parsed; nothing else under forward/az2 touched')

    # ---------------- Haar moments: two routes
    trip = [(a, b, n - a - b) for n in range(19) for a in range(n + 1) for b in range(n - a + 1)]
    need(all(mom(*k) == mom_round11_route(*k) for k in trip), 'haar_moments_two_routes_agree_to_degree_18', triples=len(trip))
    need(mom(2, 0, 0) == F(1, 4) and mom(0, 2, 0) == F(1, 4) and mom(0, 0, 2) == F(1, 4) and mom(1, 1, 1) == F(1, 16)
         and mom(1, 0, 0) == 0 and mom(4, 0, 0) == F(1, 8) and mom(2, 1, 0) == 0, 'round11_moment_fixtures')

    # ---------------- kinetic operator: Round11 fixtures and Casimir labels
    lower_ok = True
    for (a, b, c) in basis(9):
        kp = kinetic({(a, b, c): F(1)})
        top = {k: v for k, v in kp.items() if sum(k) == a + b + c}
        if top != ({(a, b, c): eps(a, b, c)} if eps(a, b, c) else {}) or deg(kp) > a + b + c:
            lower_ok = False
    e1 = all(eps(a, b, c) == a * a + b * b + F(3, 2) * c * c + F(1, 2) * a * b + F(3, 2) * c * (a + b) + 2 * a + 2 * b + 3 * c
             for (a, b, c) in basis(12))
    need(lower_ok and e1, 'kinetic_triangular_with_casimir_diagonal_E1_equals_E2', degree=9)
    fixtures = {'1': (ONE, 0), 'x': (PX, 3), 'y': (PY, 3), 'z': (PZ, F(9, 2)),
                'xy-z/4': (padd(pmul(PX, PY), PZ, F(-1, 4)), F(13, 2)), 'x^2-1/4': (padd(pmul(PX, PX), ONE, F(-1, 4)), 8)}
    need(all(kinetic(p) == pscale(p, F(e)) for p, e in fixtures.values()), 'round11_low_level_table',
         levels={k: q(F(e)) for k, (_, e) in fixtures.items()})

    # ---------------- tail floors (all channels) and per-channel floors
    need(all(m_shell(d) == F(5, 8) * d * d + 2 * d + F(3, 8) * (d % 2) for d in range(0, 61))
         and all(m_shell(d) < m_shell(d + 1) for d in range(0, 60)), 'shell_minimum_closed_form_E3_and_increasing')
    need(all(eps(a + 1, b, c) > eps(a, b, c) and eps(a, b + 1, c) > eps(a, b, c) and eps(a, b, c + 1) > eps(a, b, c)
             for (a, b, c) in basis(30)), 'eps_strictly_increasing_in_each_exponent',
         note='lowering any positive exponent of an omitted monomial lowers eps, so later shells never undercut shell D+1')
    tails = {6: m_shell(7), 8: m_shell(9)}
    need(tails == {6: F(45), 8: F(69)}, 'tail_lower_6_is_45_and_8_is_69')
    channel = {}
    for D in (6, 8):
        half, mins = F(D, 2), {}
        for d in range(D + 1, D + 41):
            for a in range(d + 1):
                for b in range(d - a + 1):
                    c = d - a - b
                    j, s, l = F(a + c, 2), F(b + c, 2), F(a + b, 2)
                    cls = [n for n, lab in (('A', j), ('B', s), ('S', l)) if lab > half] or ['joint']
                    for n in cls:
                        if n not in mins or eps(a, b, c) < mins[n][0]:
                            mins[n] = (eps(a, b, c), (a, b, c), d)
        channel[D] = mins
    need({k: v[0] for k, v in channel[6].items()} == {'A': F(123, 2), 'B': F(123, 2), 'S': F(45), 'joint': F(48)}
         and {k: v[0] for k, v in channel[8].items()} == {'A': F(96), 'B': F(96), 'S': F(69), 'joint': F(145, 2)}
         and all(v[2] == D + 1 for D in (6, 8) for v in channel[D].values()),
         'per_channel_floors', D6={k: q(v[0]) for k, v in channel[6].items()}, D8={k: q(v[0]) for k, v in channel[8].items()},
         note='A = h1,vL,h3 (spin j); B = h2,vR,h4 (spin s); S = vM (spin l); joint = all <= D/2 with j+s+l >= D+1')

    # ---------------- x-only sector: characters, exact shell structure
    for D in (6, 8):
        us = chebyshev_u(D + 2)
        orth = all(inner(us[i], us[j]) == (1 if i == j else 0) for i in range(D + 2) for j in range(i + 1))
        eig = all(kinetic(us[k]) == pscale(us[k], kk(k)) for k in range(D + 2))
        xmul = all(pmul(PX, us[k]) == padd(pscale(us[k + 1], F(1, 2)), pscale(us[k - 1], F(1, 2)) if k else {}) for k in range(D + 1))
        leak_perp = all(inner({m: F(1)}, us[D + 1]) == 0 for m in basis(D))
        need(orth and eig and xmul and leak_perp, 'x_sector_exact_D%d' % D,
             note='U_k orthonormal, K U_k=k(k+2)U_k, x U_k=(U_{k+1}+U_{k-1})/2, U_{D+1} orthogonal to all of P_D')

    # ---------------- exact coefficients
    Ej = {D: jacobi_rs(D, 19) for D in (6, 8, 20)}
    Wj = {D: [-(m + 1) * Ej[D][m + 1] for m in range(19)] for D in Ej}
    need(Ej[6][:5] == [0, 0, F(-1, 12), 0, F(5, 3456)] and Wj[6][:6] == [0, F(1, 6), 0, F(-5, 864), 0, F(289, 829440)],
         'rs_coefficients_jacobi', E=[q(x) for x in Ej[20][:9]], W=[q(x) for x in Wj[20][:8]])
    need(Wj[6][:13] == Wj[20][:13] and Wj[6][13] != Wj[20][13] and Wj[8][:17] == Wj[20][:17] and Wj[8][17] != Wj[20][17],
         'rs_coefficients_D_independent_through_order_2D',
         note='<W>_D equals the untruncated series through tau_FG^(2D) and first differs at tau_FG^(2D+1) (D=6: 13, D=8: 17)')
    Ep, Wp = poly_rs({(1, 0, 0): F(-1)}, 6)
    need(Ep == Ej[20][:7] and Wp == Wj[20][:6], 'rs_coefficients_round11_monomial_route_untruncated')
    Eb, Wb = poly_rs({(1, 0, 0): F(-1), (0, 1, 0): F(-1)}, 6)
    need(Wb[:4] == [0, F(1, 6), 0, F(-187, 33696)] and Eb[2] == F(-1, 6), 'both_faces_variant_labelled_side_value',
         note='NOT the contract model (lambda2=0); shows the second square enters only if its face is coupled')

    # ---------------- first-order derivative on the finite bases (Round11 monomials)
    mono = {}
    first_order = {}
    for D in (6, 8):
        bs, G, Kf, MX = monomial_forms(D)
        mono[D] = (bs, G, Kf, MX)
        n, ix = len(bs), bs.index((1, 0, 0))
        sym = all(Kf[i][j] == Kf[j][i] and G[i][j] == G[j][i] and MX[i][j] == MX[j][i] for i in range(n) for j in range(i))
        galerkin = all(Kf[i][ix] == 3 * G[i][ix] and MX[i][0] == G[i][ix] for i in range(n))
        kern = inertia(Kf)
        deriv = 2 * MX[0][ix] / 3
        first_order[D] = deriv
        need(sym and galerkin and kern == (0, 1, n - 1) and deriv == F(1, 6), 'first_order_derivative_finite_basis_D%d' % D,
             inertia_K=list(kern), derivative=q(deriv),
             note='K(x/3)=x.1 exactly in the Galerkin form; ker K = constants; d<W>/dtau_FG(0)=2<1,x x/3>=1/6')
        par = [(-1) ** (m[0] + m[2]) for m in bs]
        mirror = all((Kf[i][j] == 0 or par[i] * par[j] == 1) and (G[i][j] == 0 or par[i] * par[j] == 1)
                     and (MX[i][j] == 0 or par[i] * par[j] == -1) for i in range(n) for j in range(n))
        need(mirror, 'centre_flip_congruence_D%d' % D, note='S=(-1)^(a+c): S K S=K, S G S=G, S MX S=-MX, so tau_FG -> -tau_FG is exact')

    # ---------------- route C enclosures at the grid
    points = [s * t for t in grid for s in (1, -1)]
    encl, ledger_truth, rc = {}, {}, {}
    for D in (6, 8):
        encl[str(D)], ledger_truth[str(D)] = {}, {}
        for t in points:
            r = route_c(D, t)
            rc[(D, t)] = r
            it = {k: rup(v, 10 ** 100) for k, v in r['items'].items()}   # outward: each item an upper bound
            encl[str(D)][q(t)] = (r['lower'], r['upper'])
            leak_share = q(it['a_per_link_leak'])
            ledger_truth[str(D)][q(t)] = {
                'a_per_link': {'value': q(it['a_per_link_leak']),
                               'links': {e: (leak_share if e in LINKS_U else '0') for e in ALL_LINKS},
                               'membership': 'one leaked vector U_{D+1}(x) = spin network (j,s,l)=((D+1)/2,0,(D+1)/2): '
                                             'the same vector lies in the tails of h1,vL,h3 and vM; B links carry s=0'},
                'b_joint': {'value': '0', 'channel': 'all seven link spins <= D/2 and j+s+l >= D+1',
                            'reason': 'the leak of an x-only vector has j=l=(D+1)/2 > D/2'},
                'c_gauge': {'value': 'not_applicable', 'reason': 'gauge-invariant trace-monomial basis; H commutes with all six Gauss generators; no projection'},
                'd_ritz': {'value': q(it['d_ritz'])},
                'e_arithmetic': {'value': q(it['e_arithmetic'])},
                'floor': tails[D] - abs(t), 'floor_source': 'm_{D+1} over the entire first omitted shell (all channels), minus |tau_FG|',
                'separation': 3 - abs(t), 'leak_norm2': rup(r['leak2'], 10 ** 200),
                'feshbach_coupling_square': rup((t / 2) ** 2 * r['vD'] ** 2 / r['nv'], 10 ** 200),
                'bound_from': 'exact full-space residual', 'leak_included': True, 'combination': 'linear',
                'radius': it['a_per_link_leak'] + it['d_ritz'] + it['e_arithmetic']}
    free = {D: route_c(D, F(0)) for D in (6, 8)}
    need(all(free[D]['xv'] == 0 and free[D]['rho'] == 0 and free[D]['radius'] == 0 and free[D]['lower'] == 0 == free[D]['upper']
             for D in (6, 8)), 'own_free_reference_same_routine', note='<W>(0)=0, E_0(0)=0 exactly in route_c')
    need(all((t > 0 and encl[str(D)][q(t)][0] > 0) or (t < 0 and encl[str(D)][q(t)][1] < 0) for D in (6, 8) for t in points),
         'sign_certified_every_point', sub_label='sign_certified_finite_graph')
    need(all(encl[str(D)][q(-t)] == (-encl[str(D)][q(t)][1], -encl[str(D)][q(t)][0]) for D in (6, 8) for t in grid),
         'minus_tau_exact_mirror_of_route_c')
    need(all(rc[(D, t)]['p2'] < rc[(D, t)]['leak2'] and rc[(D, t)]['leak2'] > 0 for D in (6, 8) for t in points),
         'leak_dominates_galerkin_part', note='the certified width is set by the exact tail leak, not by the rational Ritz vector')
    need(all(max(encl['6'][k][0], encl['8'][k][0]) <= min(encl['6'][k][1], encl['8'][k][1]) for k in encl['6']),
         'D6_and_D8_enclosures_intersect')
    gap1 = m_shell(1)
    need(gap1 == 3 and all(rc[(D, t)]['sep'] == gap1 - abs(t) for D in (6, 8) for t in points), 'separation_is_free_gap_minus_tau',
         note='recomputed outside route_c: Weyl bound lambda_1(K - tau_FG x) >= m_1 - |tau_FG| with m_1 = 3 (never a finite-matrix level)')
    need(all(rc[(D, t)]['radius'] >= 2 * sqrt_down(rc[(D, t)]['leak2'] + rc[(D, t)]['p2']) / (gap1 - abs(t) - rc[(D, t)]['rho'])
             for D in (6, 8) for t in points), 'davis_kahan_factor_recomputed',
         note='radius >= 2||r||/(b-rho): sin(theta) <= ||r||/(b-rho) and |Tr((P_psi-P_v)x)| <= 2 sin(theta)||x||')

    # ---------------- route F (HF + concavity + Feshbach tail) and the retained Ritz-only bracket
    rf, contain, ritz_rows = {}, True, {}
    for D in (6, 8):
        for t in points:
            h = abs(t) / 10 ** 12
            f = route_f(D, t, h, tails[D])
            R_ext = ground_bracket(D, t + h, F(1, 10 ** 80))[1]
            if not (f['feshbach_shift_at_t_plus_h'] > 0 and f['feshbach_shift_at_t_plus_h'] == ((t + h) / 2) ** 2 / (m_shell(D + 1) - abs(t + h) - R_ext)):
                raise CheckFailure('feshbach term recomputed')
            rf[(D, t)] = f
            lo, hi = encl[str(D)][q(t)]
            contain = contain and f['lower'] <= lo and hi <= f['upper']
            ritz_rows[(D, t)] = ritz_only(D, t, h)
    need(contain, 'route_c_inside_route_f_every_point', note='independent certified route using the tail floor 45/69 minus |tau_FG|')
    need(True, 'feshbach_term_recomputed_every_point', note='(tau_FG/2)^2/(m_{D+1}-|tau_FG|-R) > 0 recomputed outside route_f at all 12 points')

    # ---------------- monomial pencils: Ritz ground energy of the producer's basis inside the Jacobi bracket
    mono_rows = {}
    for D in (6, 8):
        bs, G, Kf, MX = mono[D]
        n = len(bs)
        for t in list(grid) + [F(-1, 10)]:
            lo, hi = rc[(D, t)]['E_ritz']
            lo25, hi25 = rdown(lo, 10 ** 25), rup(hi, 10 ** 25)
            a = inertia(pencil(Kf, MX, G, t, lo25))
            b = inertia(pencil(Kf, MX, G, t, hi25))
            mono_rows[(D, t)] = (a, b)
            need(a == (0, 0, n) and b == (1, 0, n - 1), 'monomial_pencil_ground_in_jacobi_bracket_D%d_tau_%s' % (D, q(t)),
                 bracket_1e25=[q(lo25), q(hi25)], inertia_lower=list(a), inertia_upper=list(b))
    bs, G, Kf, MX = mono[6]
    a0 = inertia(pencil(Kf, MX, G, F(0), F(-1, 10 ** 25)))
    b0 = inertia(pencil(Kf, MX, G, F(0), F(1, 10 ** 25)))
    need(a0 == (0, 0, 84) and b0 == (1, 0, 83), 'monomial_free_reference_D6', note='E_0(0) in (-1e-25, 1e-25) in the Round11 basis')

    # ---------------- scaling, retained rows, dictionary, AW1 fixture identity
    def rem_bounds(D, t):
        lo, hi = encl[str(D)][q(t)]
        return lo - t / 6, hi - t / 6
    r1, r2 = rem_bounds(8, F(1, 10)), rem_bounds(8, F(1, 100))
    ratio = (r1[1] / r2[0], r1[0] / r2[1])  # both remainders negative
    ratio_lo, ratio_hi = min(ratio), max(ratio)
    need(F(990) <= ratio_lo <= ratio_hi <= F(1000), 'remainder_scaling_exponent_three',
         ratio=[q(rdown(ratio_lo, 10 ** 12)), q(rup(ratio_hi, 10 ** 12))], note='a tau^2 remainder would give a ratio near 100')
    heur = {D: {q(t): (t * t) / (tails[D] - 3) for t in grid} for D in (6, 8)}
    need(all(heur[D][q(t)] > 10 ** 10 * ledger_truth[str(D)][q(t)]['radius'] for D in (6, 8) for t in grid),
         'heuristic_tau2_estimate_retained_as_insufficient', note='assistant-4 tau^2/(tail-3) is uncertified and exponent 2, the true leak is order 2D+1')
    need(F(1, 6) / 24 == F(1, 144) and F(-5, 864) / 24 ** 3 == F(-5, 11943936) and 8 * F(1, 24) == F(1, 3)
         and all(8 * kk(k) == 32 * F(k, 2) * (F(k, 2) + 1) for k in range(20)), 'dictionary_and_aw1_fixture_identity',
         note='8*(4C - tau_FG x) = 32C - (tau/3)x under tau_FG=tau/24: the ground sector IS the AW1 one-plaquette fixture')
    target_indicator = 1 if (all(k in encl[d] for d in ('6', '8') for k in map(q, points)) and first_order[6] == F(1, 6) == first_order[8]) else 0
    need(target_indicator >= 1, 'preregistered_target_indicator_ge_1', note='feasibility/format target; the enclosures are the deliverable')

    # ---------------- packet semantics and controls
    truth = {
        'graph': {'vertices': 6, 'links': 7, 'gauss_constraints': 6, 'squares': 2, 'shared_links': ['vM']},
        'tau_grid': ['1/1000', '1/100', '1/10'], 'points': [q(t) for t in points],
        'enclosures': encl, 'ledger': ledger_truth,
        'coefficients': {'W': {'1': '1/6', '2': '0', '3': '-5/864'}, 'E': {'2': '-1/12', '4': '5/3456'},
                         'method': 'exact Rayleigh-Schrodinger (x-only characters and untruncated Round11 monomials)'},
        'enclosure_route': 'exact full-space residual with separation 3-|tau_FG| (Davis-Kahan); HF-concavity with Feshbach tail as cross-check',
        'ground_sector': {'conserved_label': 's (spin of h2,vR,h4)', 'ground_label': 's=0',
                          'equivalent_to': 'one-plaquette four-link graph 4C - tau_FG x = (1/8)(AW1 fixture 32j(j+1) - (tau/3)W) at tau_FG=tau/24',
                          'second_square': 'spectator'},
        'forbidden_phrasings': pre['forbidden_phrasings'], TEMPLATE_KEY: template,
    }

    def good():
        return {
            'model_id': MODEL_ID, 'model_is_finite_graph': True, 'coupling_name': 'tau_FG',
            'graph': dict(truth['graph'], shared_links=['vM']), 'cutoffs': [6, 8], 'dimensions': {'6': 84, '8': 165},
            'tau_grid': list(truth['tau_grid']), 'signs': ['+', '-'],
            'hamiltonian': {'alpha': '1', 'rho': '1', 'faces_coupled': ['U'], 'lambda2': '0', 'form': 'H=K-tau_FG*x'},
            'units': {'energy': 'alpha_FG=1 (Round11 alpha)', 'dictionary': 'tau_FG=tau/24',
                      'z3_face_term': '-(tau/3)W_f in delta=alpha/8 units = -(tau/24)W_f in alpha units'},
            'observable': {'name': 'W=x=(1/2)Tr U', 'links': list(LINKS_U), 'centering': 'none'},
            'sign_convention': {'rule': 'I1.5: V=-tau_FG*W', 'fixture_first_order': '+1/6'},
            'derivative_at_zero': '1/6',
            'own_free_reference': {'W': '0', 'E0': '0', 'free_gap': '3', 'E_W2': '1/4', 'same_code_path': True, 'imported': None},
            'enclosures': {d: {k: [q(v[0]), q(v[1])] for k, v in rows.items()} for d, rows in encl.items()},
            'coefficients': json.loads(json.dumps(truth['coefficients'])), 'fg_coefficients_fitted': False,
            'scaling': {'first_order_exponent': 1, 'remainder_exponent': 3,
                        'remainder_ratio_bracket': [q(rdown(ratio_lo, 10 ** 12)), q(rup(ratio_hi, 10 ** 12))]},
            'ledger': {d: {k: {kk_: (q(vv) if isinstance(vv, F) else json.loads(json.dumps(vv))) for kk_, vv in led.items()}
                           for k, led in rows.items()} for d, rows in ledger_truth.items()},
            'tail': {'6': '45', '8': '69'},
            'retained': {'ritz_only_truncated_bracket': {'verdict': 'insufficient'},
                         'heuristic_tau2_over_tail': {'verdict': 'insufficient'},
                         'single_omitted_element': {'verdict': 'insufficient'}},
            'enclosure_route': truth['enclosure_route'], 'ground_sector': json.loads(json.dumps(truth['ground_sector'])),
            'minus_tau_role': 'exact mirror replay (centre flip on one U link), not a second confirmation',
            'claims': {'continuum_claim': False, 'scientific_priority_verified': False, 'weak_coupling_claim': False,
                       'resolves_roadmap_goal_2': False, 'transfers_to_aq': False},
            'dictionary': {'tau_FG': 'tau/24', 'fg_first_order': '1/6', 'z3_first_order': '1/144', 'role': 'consistency_only'},
            'report_text': template + ' The finite-graph enclosures are consistent with the matched coefficient and nothing more.',
            'sub_label': 'sign_certified_finite_graph',
        }

    need(validate_packet(good(), truth), 'reference_packet_validates')

    def mut(path, value, *more):
        def fn():
            p = good()
            for pth, val in ((path, value),) + tuple(zip(more[::2], more[1::2])):
                node = p
                for key in pth[:-1]:
                    node = node[key]
                if val is DELETE:
                    del node[pth[-1]]
                else:
                    node[pth[-1]] = val
            return validate_packet(p, truth)
        return fn

    def flip_signs():
        def fn():
            p = good()
            p['sign_convention'] = {'rule': 'I1.5: V=+tau_FG*W', 'fixture_first_order': '-1/6'}
            p['derivative_at_zero'] = '-1/6'
            p['enclosures'] = {d: {k: [q(-F(v[1])), q(-F(v[0]))] for k, v in rows.items()} for d, rows in p['enclosures'].items()}
            return validate_packet(p, truth)
        return fn

    L6 = ('ledger', '6', '1/10')
    fit_c3 = (F(encl['6']['1/10'][0]) - F(1, 60)) * 1000       # a divided-difference 'coefficient' from one enclosure
    lo_e, hi_e = encl['6']['1/1000']
    control('missing_incoming_stars', [
        ('leak_dropped_from_residual', mut(L6 + ('leak_included',), False, L6 + ('leak_norm2',), '0'), 'incoming coupling'),
        ('feshbach_square_zero_ritz_as_lower', mut(L6 + ('feshbach_coupling_square',), '0'), 'incoming coupling')],
        reading='finite-graph reading: every coupling from P_D into the omitted space (the x-raising leak of the top shell) is counted')
    control('full_original_wilson_cover', [
        ('three_links_without_shared_vM', mut(('observable', 'links'), ['h1', 'vL', 'h3']), 'wilson cover'),
        ('outer_loop_z', mut(('observable', 'name'), 'W=z=(1/2)Tr UV'), 'wilson cover'),
        ('other_square_y', mut(('observable', 'name'), 'W=y=(1/2)Tr V', ('observable', 'links'), ['h2', 'vR', 'h4', 'vM']), 'wilson cover')])
    control('wrong_delta_alpha_hbar_clock', [
        ('delta_units_tau_over_3', mut(('units', 'dictionary'), 'tau_FG=tau/3'), 'units'),
        ('tau_over_8', mut(('units', 'dictionary'), 'tau_FG=tau/8'), 'units'),
        ('energy_alpha_8', mut(('units', 'energy'), 'alpha_FG=8'), 'units'),
        ('clock_field_added', mut(('clock',), 's=alpha*t_E/hbar'), 'units')])
    control('vector_versus_scalar_centering', [
        ('scalar_centering', mut(('observable', 'centering'), 'scalar'), 'centering'),
        ('vector_centering', mut(('observable', 'centering'), 'vector'), 'centering'),
        ('E_W2_subtracted', mut(('observable', 'reference_subtracted'), '1/4'), 'centering')])
    control('first_order_mean_charged', [
        ('parity_zero', mut(('derivative_at_zero',), '0'), 'first-order mean'),
        ('missing_factor_two', mut(('derivative_at_zero',), '1/12'), 'first-order mean'),
        ('E_W2_as_one_half', mut(('derivative_at_zero',), '1/3'), 'first-order mean'),
        ('free_value_inside', mut(('enclosures', '6', '1/1000'), [q(-F(1, 10 ** 12)), q(hi_e)]), 'first-order mean')])
    control('tau_scaling_exponent', [
        ('remainder_exponent_two', mut(('scaling', 'remainder_exponent'), 2, ('scaling', 'remainder_ratio_bracket'), ['99', '101']), 'tau scaling'),
        ('linear_called_sqrt', mut(('scaling', 'first_order_exponent'), F(1, 2)), 'tau scaling')])
    control('changed_model_relabelled', [
        ('D4_labelled_D6', mut(('dimensions',), {'6': 35, '8': 165}), 'model changed'),
        ('one_plaquette_graph', mut(('graph', 'links'), 4, ('graph', 'gauss_constraints'), 4, ('graph', 'squares'), 1), 'model changed'),
        ('both_faces_coupled', mut(('hamiltonian', 'faces_coupled'), ['U', 'V'], ('hamiltonian', 'lambda2'), 'tau_FG'), 'model changed'),
        ('rho_one_half', mut(('hamiltonian', 'rho'), '1/2'), 'model changed'),
        ('grid_point_1_20', mut(('tau_grid',), ['1/1000', '1/100', '1/20']), 'model changed'),
        ('cutoff_D10', mut(('cutoffs',), [6, 10]), 'model changed')])
    control('insufficient_verdict_retained', [
        ('ritz_only_row_dropped', mut(('retained', 'ritz_only_truncated_bracket'), DELETE), 'insufficient verdict retained'),
        ('heuristic_promoted', mut(('retained', 'heuristic_tau2_over_tail', 'verdict'), 'accepted'), 'insufficient verdict retained'),
        ('single_element_row_dropped', mut(('retained', 'single_omitted_element'), DELETE), 'insufficient verdict retained')])
    control('exact_arithmetic_admission', [
        ('float_endpoint', mut(('enclosures', '8', '1/10'), [float(encl['8']['1/10'][0]), q(encl['8']['1/10'][1])]), 'exact arithmetic'),
        ('float_derivative', mut(('derivative_at_zero',), 1 / 6), 'exact arithmetic'),
        ('float_floor', mut(L6 + ('floor',), 44.9), 'exact arithmetic')])
    control('root_n_misuse', [
        ('root_sum_square_of_items', mut(L6 + ('combination',), 'root_sum_square'), 'root-N'),
        ('radius_below_linear_sum', mut(L6 + ('radius',), q(F(ledger_truth['6']['1/10']['radius']) / 2)), 'root-N')])
    control('no_priority_or_continuum_claim', [
        ('continuum', mut(('claims', 'continuum_claim'), True), 'forbidden claim'),
        ('priority', mut(('claims', 'scientific_priority_verified'), True), 'forbidden claim'),
        ('weak_coupling', mut(('claims', 'weak_coupling_claim'), True), 'forbidden claim'),
        ('goal_2', mut(('claims', 'resolves_roadmap_goal_2'), True), 'forbidden claim'),
        ('phrase_predicts', mut(('report_text',), template + ' The graph predicts the Z^3 slope.'), 'forbidden claim'),
        ('phrase_confirms', mut(('report_text',), template + ' This confirms the Z^3 value.'), 'forbidden claim')])
    control('finite_graph_model_id', [
        ('not_finite_graph', mut(('model_is_finite_graph',), False), 'finite-graph model id'),
        ('coupling_named_tau', mut(('coupling_name',), 'tau'), 'finite-graph model id'),
        ('z3_label', mut(('model_id',), 'AQ_uniform(tau=1e-8)'), 'finite-graph model id')])
    control('complete_residual_all_channels', [
        ('B_links_omitted', mut(L6 + ('a_per_link', 'links'), {e: v for e, v in good()['ledger']['6']['1/10']['a_per_link']['links'].items()
                                                                 if e in LINKS_U}), 'all channels'),
        ('shared_link_omitted', mut(L6 + ('a_per_link', 'links'), {e: v for e, v in good()['ledger']['6']['1/10']['a_per_link']['links'].items()
                                                                     if e != 'vM'}), 'all channels'),
        ('joint_channel_assumed_empty', mut(L6 + ('b_joint', 'channel'), 'none: per-link tails assumed complete'), 'all channels'),
        ('single_omitted_element_as_bound', mut(L6 + ('bound_from',), 'one omitted matrix element <D+1|x|D>=1/2'), 'all channels'),
        ('shared_link_leak_zeroed', mut(L6 + ('a_per_link', 'links', 'vM'), '0'), 'all channels')])
    control('certified_representation_tail', [
        ('finite_matrix_gap_as_floor', mut(L6 + ('floor',), '3'), 'representation tail'),
        ('floor_without_minus_tau', mut(L6 + ('floor',), '45'), 'representation tail'),
        ('sector_floor_63_unproved', mut(L6 + ('floor',), q(63 - F(1, 10)), L6 + ('floor_source',), 'x-only sector floor (D+1)(D+3)'), 'representation tail'),
        ('last_retained_shell_m6', mut(L6 + ('floor',), q(m_shell(6) - F(1, 10))), 'representation tail'),
        ('D8_tail_left_at_45', mut(('tail', '8'), '45'), 'representation tail')])
    control('own_free_reference', [
        ('imported_z3_free_atom', mut(('own_free_reference', 'imported'), 'e^{-3}/4'), 'own free reference'),
        ('not_same_code_path', mut(('own_free_reference', 'same_code_path'), False), 'own free reference'),
        ('W2_as_reference', mut(('own_free_reference', 'W'), '1/4'), 'own free reference')])
    control('no_transfer_to_aq', [
        ('transfers_true', mut(('claims', 'transfers_to_aq'), True), 'transfer to AQ'),
        ('template_missing', mut(('report_text',), 'The finite graph is consistent with 1/144.'), 'transfer to AQ'),
        ('k2_sentence', mut(('report_text',), template + ' Hence K_2 overestimates the AQ model remainder.'), 'transfer to AQ'),
        ('dictionary_as_prediction', mut(('dictionary', 'role'), 'prediction'), 'transfer to AQ')])
    control('fg_coefficients_not_fitted', [
        ('fitted_flag', mut(('fg_coefficients_fitted',), True), 'fitted coefficients'),
        ('c3_from_one_enclosure', mut(('coefficients', 'W', '3'), q(rdown(fit_c3, 10 ** 12))), 'fitted coefficients'),
        ('c2_nonzero_from_fit', mut(('coefficients', 'W', '2'), '1/1000000000000'), 'fitted coefficients'),
        ('method_fit', mut(('coefficients', 'method'), 'least-squares fit to the grid enclosures'), 'fitted coefficients')])
    control('sign_convention_fixture', [
        ('plus_tau_W', flip_signs(), 'sign convention'),
        ('fixture_minus', mut(('sign_convention', 'fixture_first_order'), '-1/6'), 'sign convention')])
    control('complete_residual_ledger_itemized', [
        ('a_and_b_merged', mut(L6 + ('a_plus_b',), {'value': ledger_truth['6']['1/10']['a_per_link']['value']}), 'ledger itemization'),
        ('gauge_na_without_reason', mut(L6 + ('c_gauge',), {'value': 'not_applicable', 'reason': ''}), 'ledger itemization'),
        ('arithmetic_missing', mut(L6 + ('e_arithmetic',), DELETE), 'ledger itemization'),
        ('ritz_missing', mut(L6 + ('d_ritz',), DELETE), 'ledger itemization')])
    control('ground_sector_spectator_disclosed', [
        ('spectator_hidden', mut(('ground_sector', 'second_square'), 'active'), 'spectator'),
        ('fixture_identity_hidden', mut(('ground_sector', 'equivalent_to'), 'an independent finite model'), 'spectator')], extra=True)
    control('minus_tau_mirror_replay', [
        ('second_confirmation', mut(('minus_tau_role',), 'independent confirmation at negative coupling'), 'mirror')], extra=True)
    control('truncated_bracket_not_full_graph', [
        ('update4_reading', mut(('enclosure_route',), 'exact_bracket of the truncated matrix (tail used as energy floor)'), 'truncated')], extra=True)

    rows = [dict(r) for r in CHECKS if r.get('kind') == 'control']
    ev = {'rows': rows, 'digest': hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()}
    required = [c_ for c_ in ctrl if c_ != 'coherent_evidence_tampering']
    need(validate_evidence(ev, required), 'evidence_validates')
    bad = [dict(r) for r in rows]
    bad[4]['passed'] = False
    ev_bad = {'rows': bad, 'digest': hashlib.sha256(json.dumps(bad, sort_keys=True).encode()).hexdigest()}
    fewer = [dict(r) for r in rows if r['id'] != 'certified_representation_tail']
    ev_few = {'rows': fewer, 'digest': hashlib.sha256(json.dumps(fewer, sort_keys=True).encode()).hexdigest()}
    stale = dict(ev, rows=bad)
    control('coherent_evidence_tampering', [
        ('flip_boolean_rebind_hash', lambda: validate_evidence(ev_bad, required), 'required control not passed'),
        ('drop_control_rebind_hash', lambda: validate_evidence(ev_few, required), 'missing required control'),
        ('flip_boolean_stale_hash', lambda: validate_evidence(stale, required), 'evidence digest mismatch')])
    executed = [r['id'] for r in CHECKS if r.get('kind') == 'control']
    contract_exec = [c_ for c_ in executed if c_ not in EXTRA_CONTROLS]
    need(sorted(contract_exec) == sorted(ctrl) and len(contract_exec) == 20 and len(executed) == 23, 'all_contract_controls_executed',
         contract=20, extra=list(EXTRA_CONTROLS))
    n_mut = sum(len(r['mutations']) for r in CHECKS if r.get('kind') == 'control')
    n_mut_contract = sum(len(r['mutations']) for r in CHECKS if r.get('kind') == 'control' and r['id'] not in EXTRA_CONTROLS)

    # ---------------- result assembly
    point_rows = {}
    for D in (6, 8):
        for t in points:
            r, f = rc[(D, t)], rf[(D, t)]
            led = ledger_truth[str(D)][q(t)]
            point_rows['D%d_tau_%s' % (D, q(t))] = {
                'enclosure_lower_1e-60': q(r['lower']), 'enclosure_upper_1e-60': q(r['upper']),
                'ritz_expectation_exact': q(r['xv']) if len(q(r['xv'])) < 400 else 'exact rational, %d characters' % len(q(r['xv'])),
                'ritz_energy_bracket_1e-40': [q(rdown(r['E_ritz'][0], 10 ** 40)), q(rup(r['E_ritz'][1], 10 ** 40))],
                'separation': q(led['separation']), 'tail_floor': q(led['floor']),
                'enclosure_decimal_45': [dec(r['lower'], 45, False), dec(r['upper'], 45, True)],
                'items_upper_1e-100': {k: q(rup(v, 10 ** 100)) for k, v in r['items'].items()},
                'radius_upper_1e-100': q(rup(led['radius'], 10 ** 100)),
                'route_f_hf_concavity': {'h': q(f['h']), 'lower_1e-40': q(rdown(f['lower'], 10 ** 40)), 'upper_1e-40': q(rup(f['upper'], 10 ** 40))},
                'retained_ritz_only_truncated': {'lower_1e-40': q(rdown(ritz_rows[(D, t)][0], 10 ** 40)),
                                                 'upper_1e-40': q(rup(ritz_rows[(D, t)][1], 10 ** 40)), 'verdict': 'insufficient',
                                                 'reason': 'encloses the truncated <W>_D; no tail, so not a full-graph enclosure'},
            }
    previews = {'label': 'floating previews only; no admission Boolean reads them'}
    for D in (6, 8):
        for t in points:
            r = rc[(D, t)]
            previews['D%d_tau_%s' % (D, q(t))] = {'W': preview(r['xv']), 'half_width': preview(r['radius'] + r['items']['e_arithmetic']),
                                                  'leak': preview(sqrt_up(r['leak2'], 10 ** 80)), 'E_ritz': preview(r['E_ritz'][1]),
                                                  'route_f_width': preview(rf[(D, t)]['upper'] - rf[(D, t)]['lower'])}
    previews['heuristic_tau2_over_tail_minus_3'] = {'D%d_tau_%s' % (D, k): preview(v) for D in heur for k, v in heur[D].items()}
    previews['remainder_ratio_tau_1_10_over_1_100'] = [preview(ratio_lo), preview(ratio_hi)]
    previews['both_faces_c3'] = preview(F(-187, 33696))
    result = {
        'loop': 'AZ2', 'stage': 'pre_comparison', 'role': 'skeptic independent replay (single-direction admission input)',
        'standing': 'model-agent skeptic with correlated ancestry; not human peer review, not formal verification',
        'human_author': 'Hruday N M (BUNZEEY)',
        'producer_files_read': [],
        'producer_paths_touched': 'research/round32/forward/az2/inputs/ only: 28 file names listed and their bytes hashed against the repository',
        'scratch': '/tmp/claude-0/skeptic-az2-private/ (disclosed; not evidence)',
        'checker_sha256': sha_bytes(Path(__file__).read_bytes()),
        'contract_sha256': CONTRACT_SHA256, 'pinned_sha256': PINNED, 'model_id': MODEL_ID,
        'model': {'hamiltonian': 'H_FG = K - tau_FG*x, K = sum of the 7 link Casimirs (alpha=1, rho=1), second face uncoupled',
                  'observable': '<W> = <x>, x=(1/2)Tr U, U = vM h3^-1 vL^-1 h1', 'sector': 'gauge-invariant',
                  'model_is_finite_graph': True, 'transfers_to_aq': False, 'fg_coefficients_fitted': False},
        'ground_sector': truth['ground_sector'],
        'dimensions': {'6': 84, '8': 165}, 'tail_lower': {'6': '45', '8': '69'},
        'per_channel_floors': {str(D): {k: q(v[0]) for k, v in channel[D].items()} for D in (6, 8)},
        'sector_floor_x_only': {'6': '63', '8': '99'},
        'first_order': {'derivative_at_zero': '1/6', 'D6': q(first_order[6]), 'D8': q(first_order[8]),
                        'reason': 'x=(1/2)Tr U is an exact K-eigenvector with eigenvalue 3 in P_1, and x.1=x; the first-order vector (tau_FG/3)x lies in every P_D, D>=1'},
        'coefficients': {'W_series': [q(x) for x in Wj[20][:8]], 'E_series': [q(x) for x in Ej[20][:9]],
                         'second_order_W': '0', 'third_order_W': '-5/864', 'second_order_E': '-1/12', 'fourth_order_E': '5/3456',
                         'D_independent_through_order_W': '2D', 'both_faces_variant_third_order_W': '-187/33696 (not the contract model)'},
        'dictionary': {'tau_FG': 'tau/24', 'first_order': '1/6 -> 1/144', 'third_order': '-5/864 -> -5/11943936 (AW1 one-plaquette fixture)',
                       'role': 'consistency_only; an identity of the two first-order formulas, not an independent observation'},
        'points': point_rows,
        'ledger': {d: {k: {kk_: (q(vv) if isinstance(vv, F) else vv) for kk_, vv in led.items()} for k, led in rows.items()}
                   for d, rows in ledger_truth.items()},
        'monomial_crosscheck_inertia': {'D%d_tau_%s' % (D, q(t)): [list(a), list(b)] for (D, t), (a, b) in mono_rows.items()},
        'remainder_ratio_bracket': [q(rdown(ratio_lo, 10 ** 12)), q(rup(ratio_hi, 10 ** 12))],
        'retained_insufficient': {
            'ritz_only_truncated_bracket': 'truncated-matrix brackets (assistant-4/update-4 reading) enclose <W>_D, not the full graph',
            'heuristic_tau2_over_tail': 'tau^2/(m_{D+1}-3) is uncertified and has exponent 2; the certified leak has order 2D+1',
            'single_omitted_element': '<D+1|x|D>=1/2 proves leakage; the bound needs the whole omitted component (here one, by the three-term structure)'},
        'post_comparison_predictions': {
            'derivative_at_zero': '1/6 exactly at D=6 and D=8 (and for the untruncated graph)',
            'coefficients': {'W_1': '1/6', 'W_2': '0', 'W_3': '-5/864', 'E_2': '-1/12', 'E_4': '5/3456'},
            'dictionary': '1/6 -> 1/144; -5/864 -> -5/11943936 (the AW1 one-plaquette fixture)',
            'dimensions_tails': {'6': [84, '45'], '8': [165, '69']},
            'enclosures': 'every producer enclosure intersects the certified one at the same (D, tau_FG); D=6 and D=8 agree to '
                          'below 1e-16; sign(<W>)=sign(tau_FG) at all 12 points; -tau_FG is the exact negation',
            'ledger': 'B-link tails and the joint channel receive 0 from the ground vector; the leak sits in the tails of h1,vL,h3,vM '
                      'together; gauge projection 0 (not applicable); the width is set by the leak ~ tau_FG^(D+1)',
            'verdict_if_route_is_truncated_only': 'not a full-graph enclosure: limited at best until the tail or residual is added'},
        'sub_label': 'sign_certified_finite_graph',
        'claims': {'continuum_claim': False, 'scientific_priority_verified': False, 'weak_coupling_claim': False,
                   'resolves_roadmap_goal_2': False, 'transfers_to_aq': False, 'model_is_finite_graph': True,
                   'fg_coefficients_fitted': False},
        'counts': {'checks': None, 'controls': 23, 'contract_controls': 20, 'extra_controls': 3,
                   'mutations': n_mut, 'mutations_in_contract_controls': n_mut_contract},
        'previews': previews,
        'checks': CHECKS,
    }
    result['counts']['checks'] = len(CHECKS)
    return result


DELETE = object()


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
    print(json.dumps({'checks': len(result['checks']), 'controls': result['counts']['controls'],
                      'mutations': result['counts']['mutations'],
                      'W_D8_tau_1_10': [result['points']['D8_tau_1/10']['enclosure_lower_1e-60'][:40],
                                        result['points']['D8_tau_1/10']['enclosure_upper_1e-60'][:40]]}))


if __name__ == '__main__':
    main()
