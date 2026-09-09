#!/usr/bin/env python3
"""Exact symbolic consistency checks owned by the advisor, not an independent verifier.

Uses only Python's standard library. Arithmetic is rational throughout. No solver
implementation, numerical eigensolver, or third-party symbolic package is imported.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import json

ZERO = (0, 0, 0)
ONE = {ZERO: F(1)}


def add(*polys):
    out = {}
    for p in polys:
        for k, v in p.items():
            out[k] = out.get(k, F(0)) + v
    return {k: v for k, v in out.items() if v}


def scale(p, a):
    return {k: F(a) * v for k, v in p.items() if F(a) * v}


def mul(p, q):
    out = {}
    for k, v in p.items():
        for l, w in q.items():
            key = tuple(a+b for a, b in zip(k, l))
            out[key] = out.get(key, F(0)) + v*w
    return {k: v for k, v in out.items() if v}


def deriv(p, i):
    out = {}
    for k, v in p.items():
        if k[i]:
            l = list(k)
            l[i] -= 1
            out[tuple(l)] = v*k[i]
    return out


def eps(a, b, c, rho=F(1)):
    j, k, ell = F(a+c, 2), F(b+c, 2), F(a+b, 2)
    return 3*j*(j+1) + 3*k*(k+1) + rho*ell*(ell+1)


def scalar_moment(n):
    return F(0) if n % 2 else F(comb(n, n//2), (n//2+1)*2**n)


def J(n, h):
    return sum((-1)**r*comb(h, r)*scalar_moment(n+2*r)
               for r in range(h+1))


def moment(a, b, c):
    return sum(F(comb(c, 2*h), 2*h+1)*J(a+c-2*h, h)*J(b+c-2*h, h)
               for h in range(c//2+1))


def integ(p):
    return sum(v*moment(*k) for k, v in p.items())


def main():
    checks = []
    def check(name, condition, detail=None):
        checks.append({'name': name, 'passed': bool(condition), 'detail': detail})

    x, y, z = ({(1, 0, 0): F(1)}, {(0, 1, 0): F(1)}, {(0, 0, 1): F(1)})
    xx, yy, zz = mul(x, x), mul(y, y), mul(z, z)
    xy, xz, yz = mul(x, y), mul(x, z), mul(y, z)
    D = add(ONE, scale(xx, -1), scale(yy, -1), scale(zz, -1), scale(mul(xy, z), 2))
    A = [[add(ONE, scale(xx, -1)), scale(add(z, scale(xy, -1)), F(1, 4)), scale(add(y, scale(xz, -1)), F(3, 4))],
         [scale(add(z, scale(xy, -1)), F(1, 4)), add(ONE, scale(yy, -1)), scale(add(x, scale(yz, -1)), F(3, 4))],
         [scale(add(y, scale(xz, -1)), F(3, 4)), scale(add(x, scale(yz, -1)), F(3, 4)), scale(add(ONE, scale(zz, -1)), F(3, 2))]]

    def K(p):
        return scale(add(*(deriv(mul(A[i][j], deriv(p, j)), i)
                           for i in range(3) for j in range(3))), -1)

    for i, expected in enumerate([scale(x, -3), scale(y, -3), scale(z, F(-9, 2))]):
        check('metric_divergence_'+str(i), add(*(deriv(A[j][i], j) for j in range(3))) == expected)
    for i, (q, fac) in enumerate([(x, -2), (y, -2), (z, -3)]):
        check('boundary_conormal_'+str(i), add(*(mul(A[i][j], deriv(D, j)) for j in range(3))) == scale(mul(D, q), fac))
    for name, p, expected in [('constant', ONE, {}), ('x', x, scale(x, 3)), ('y', y, scale(y, 3)),
                              ('outer_trace', z, scale(z, F(9, 2))),
                              ('xy', xy, add(scale(xy, F(13, 2)), scale(z, F(-1, 2)))),
                              ('coupled_eigenstate', add(xy, scale(z, F(-1, 4))), scale(add(xy, scale(z, F(-1, 4))), F(13, 2)))]:
        check('K_'+name, K(p) == expected)

    # Exact integration of the differential expression is an algebraic consistency check.
    for d in range(7):
        for a in range(d+1):
            for b in range(d-a+1):
                c = d-a-b
                key = (a, b, c)
                result = K({key: F(1)})
                check('triangular_'+str(key), result.get(key, F(0)) == eps(a, b, c)
                      and all(k == key or sum(k) < d for k in result))
                check('haar_zero_integral_K_'+str(key), integ(result) == 0)

    shell_values = []
    for d in range(25):
        minimum = min(eps(a, b, d-a-b) for a in range(d+1) for b in range(d-a+1))
        formula = F(5*d*d, 8)+2*d+F(3*(d % 2), 8)
        check('shell_minimum_'+str(d), minimum == formula)
        shell_values.append({'degree': d, 'minimum': str(minimum)})

    for rho in [F(0), F(1, 3), F(1), F(3), F(4), F(7)]:
        mins = [min(eps(a, b, d-a-b, rho) for a in range(d+1) for b in range(d-a+1))
                for d in range(1, 11)]
        check('rho_first_gap_'+str(rho), min(mins) == min(F(3, 4)*(3+rho), F(9, 2)))
        check('rho_shell_monotonic_'+str(rho), all(a < b for a, b in zip(mins, mins[1:])))

    # Exact finite Taylor lower bounds make the heat-kernel estimate independent of floating point.
    e3_lower = sum(F(3**n, factorial(n)) for n in range(10))
    e4_lower = sum(F(4**n, factorial(n)) for n in range(9))
    check('exp3_gt20', e3_lower > 20, str(e3_lower))
    check('exp4_gt50', e4_lower > 50, str(e4_lower))
    r_upper = F(1, 5)+F(4, 575)
    check('heat_remainder_lt_quarter', r_upper < F(1, 4), str(r_upper))
    check('heat_prefactor', 3*F(9, 25)**2 == F(243, 625))
    check('outer_correlation_moment', moment(1, 1, 1) == F(1, 16))

    result = {
        'contract_version': 'ym11-two-square-v1',
        'scope': 'Advisor-owned rational symbolic consistency checks; no independent verification claim.',
        'checks_total': len(checks), 'checks_passed': sum(c['passed'] for c in checks),
        'checks_failed': [c for c in checks if not c['passed']],
        'checks': checks, 'shell_values': shell_values,
        'heat_remainder_rational_upper': str(r_upper),
        'limitations': ['Finite shell scans supplement the analytic all-degree proof.',
                       'No interacting eigenvalue brackets are certified by this script.',
                       'The independent unreduced seven-link calculation is owned by the skeptic.']
    }
    out = Path(__file__).with_name('advisor_checks.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['checks_total', 'checks_passed', 'checks_failed']}))
    if result['checks_failed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
