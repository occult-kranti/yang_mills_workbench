#!/usr/bin/env python3
"""PREVIEW ONLY - AZ2 forward: an independent python-flint (FLINT fmpq / Arb ball) rebuild of the finite-graph
Ritz data on the Round11 two-plaquette graph, used only as a labelled comparison with check.py's exact enclosures.

Human project author: Hruday N M (BUNZEEY). AI-assisted (a Claude model agent).
This script is never imported by check.py and produces no admission value.  It rebuilds the Haar moments (Round11
advisor Q4), the kinetic operator directly from the Round11 K4 differential formula (rho=1, not from check.py's
Casimir decomposition), the Gram/kinetic/multiplication matrices as FLINT fmpq matrices, runs Arb-ball inverse
iteration at 400 bits, and records balls for the Ritz Wilson mean <W_1> and the Ritz energy.  A finite-matrix
eigenvalue is not a full-space certificate; the preview only checks that an independent rebuild lands inside
check.py's exact enclosures.

Usage: python3 -B arb_preview.py   (writes preview/arb_preview.json next to this script)
"""
import json
from fractions import Fraction
from math import comb
from pathlib import Path

import flint

LABEL = 'PREVIEW ONLY - python-flint Arb/fmpq cross-check; never an admission value'
BASE = Path(__file__).resolve().parent
PREC = 400
ITER = 60


def basis(d):
    return [(a, b, n - a - b) for n in range(d + 1) for a in range(n + 1) for b in range(n - a + 1)]


_cache = {}


def mu_x(n):
    if n % 2:
        return flint.fmpq(0)
    m = n // 2
    return flint.fmpq(comb(2 * m, m), 4 ** m * (m + 1))


def jfun(n, h):
    return sum((flint.fmpq((-1) ** r * comb(h, r)) * mu_x(n + 2 * r) for r in range(h + 1)), flint.fmpq(0))


def moment(a, b, c):
    key = (a, b, c)
    if key not in _cache:
        _cache[key] = sum((flint.fmpq(comb(c, 2 * h), 2 * h + 1) * jfun(a + c - 2 * h, h) * jfun(b + c - 2 * h, h)
                           for h in range(c // 2 + 1)), flint.fmpq(0))
    return _cache[key]


def kinetic_k4(mono):
    """Round11 advisor K4 at rho=1: -[(1-x^2)f_xx + (1-y^2)f_yy + 3/2(1-z^2)f_zz + 1/2(z-xy)f_xy + 3/2(y-xz)f_xz
    + 3/2(x-yz)f_yz - 3x f_x - 3y f_y - 9/2 z f_z]."""
    a, b, c = mono
    out = {}

    def add(k, v):
        out[k] = out.get(k, flint.fmpq(0)) + v
    add(mono, flint.fmpq(3 * a + 3 * b) + flint.fmpq(9, 2) * c)
    if a >= 2:
        add((a - 2, b, c), flint.fmpq(-a * (a - 1))); add(mono, flint.fmpq(a * (a - 1)))
    if b >= 2:
        add((a, b - 2, c), flint.fmpq(-b * (b - 1))); add(mono, flint.fmpq(b * (b - 1)))
    if c >= 2:
        add((a, b, c - 2), flint.fmpq(-3 * c * (c - 1), 2)); add(mono, flint.fmpq(3 * c * (c - 1), 2))
    if a >= 1 and b >= 1:
        add((a - 1, b - 1, c + 1), flint.fmpq(-a * b, 2)); add(mono, flint.fmpq(a * b, 2))
    if a >= 1 and c >= 1:
        add((a - 1, b + 1, c - 1), flint.fmpq(-3 * a * c, 2)); add(mono, flint.fmpq(3 * a * c, 2))
    if b >= 1 and c >= 1:
        add((a + 1, b - 1, c - 1), flint.fmpq(-3 * b * c, 2)); add(mono, flint.fmpq(3 * b * c, 2))
    return {k: v for k, v in out.items() if v != 0}


def build(D):
    bs = basis(D)
    n = len(bs)
    kp = [kinetic_k4(q) for q in bs]
    G = flint.fmpq_mat(n, n, [moment(p[0] + q[0], p[1] + q[1], p[2] + q[2]) for p in bs for q in bs])
    AK = flint.fmpq_mat(n, n, [sum((v * moment(p[0] + k[0], p[1] + k[1], p[2] + k[2]) for k, v in kp[j].items()), flint.fmpq(0))
                               for p in bs for j in range(n)])
    MX = flint.fmpq_mat(n, n, [moment(p[0] + q[0] + 1, p[1] + q[1], p[2] + q[2]) for p in bs for q in bs])
    MY = flint.fmpq_mat(n, n, [moment(p[0] + q[0], p[1] + q[1] + 1, p[2] + q[2]) for p in bs for q in bs])
    return bs, G, AK, MX, MY


def exact_endpoints(ball):
    def frac(x):
        man, exp = x.man_exp()
        man, exp = int(man), int(exp)
        return Fraction(man) * (Fraction(2) ** exp)
    mid, rad = frac(ball.mid()), frac(ball.rad())
    lo, hi = mid - rad, mid + rad
    return [str(lo), str(hi)]


def quad(u, M, w):
    return (u.transpose() * M * w)[0, 0]


def main():
    flint.ctx.prec = PREC
    out = {'label': LABEL, 'flint_version': flint.__version__, 'precision_bits': PREC, 'iterations': ITER,
           'wilson_balls': {}, 'energy_balls': {},
           'method': 'fmpq matrices from Q4 moments and the K4 differential formula; Arb inverse iteration (A - sigma G) w = G v, sigma = -tau^2/6 - 1/1000'}
    for D in (6, 8):
        bs, G, AK, MX, MY = build(D)
        n = len(bs)
        for tnum, tden in ((0, 1), (1, 1000), (-1, 1000), (1, 100), (-1, 100), (1, 10), (-1, 10)):
            tau = flint.fmpq(tnum, tden)
            A = AK - (MX + MY) * tau
            sigma = -tau * tau / 6 - flint.fmpq(1, 1000)
            Ma, Ga = flint.arb_mat(A - G * sigma), flint.arb_mat(G)
            v = flint.arb_mat(n, 1, [1] + [0] * (n - 1))
            for _ in range(ITER):
                w = Ma.solve(Ga * v)
                v = w * (1 / w[0, 0])
            nrm = quad(v, Ga, v)
            wR = quad(v, flint.arb_mat(MX), v) / nrm
            E0 = quad(v, flint.arb_mat(A), v) / nrm
            sign = '+' if tnum > 0 else ('-' if tnum < 0 else '')
            key = 'D%d_tau%s%s' % (D, sign, str(Fraction(abs(tnum), tden)))
            out['wilson_balls'][key] = exact_endpoints(wR)
            out['energy_balls'][key] = exact_endpoints(E0)
    (BASE / 'preview').mkdir(exist_ok=True)
    (BASE / 'preview' / 'arb_preview.json').write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'label': LABEL, 'points': len(out['wilson_balls'])}))


if __name__ == '__main__':
    main()
