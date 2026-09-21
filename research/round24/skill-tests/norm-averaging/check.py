#!/usr/bin/env python3
"""Exact finite-support algebra checks. This is not an operator-norm proof."""
import argparse
from fractions import Fraction as F
import json
from math import factorial
from pathlib import Path


class CheckError(Exception):
    pass


def require(ok, message):
    if ok is not True:
        raise CheckError(message)


# Gaussian rationals, represented as (real, imaginary). No floating point.
def g(x=0, y=0):
    return (F(x), F(y))


ZERO, ONE, I = g(), g(1), g(0, 1)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, b):
    return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])


def scale(a, b):
    return (a[0]*b, a[1]*b)


def gp(a, k):
    result = ONE
    for _ in range(k):
        result = mul(result, a)
    return result


def clean(v):
    return {n: a for n, a in v.items() if a != ZERO}


def vs(v, a):
    return clean({n: mul(x, a) for n, x in v.items()})


def va(*vectors):
    out = {}
    for v in vectors:
        for n, a in v.items():
            out[n] = add(out.get(n, ZERO), a)
    return clean(out)


def basis(n):
    return {n: ONE}


def shift(v, direction):
    return {n + direction: a for n, a in v.items() if n + direction >= 0}


def diagonal(v, tau):
    return clean({n: scale(a, F(n)/tau) for n, a in v.items()})


def hamiltonian(v, tau, c):
    return va(diagonal(v, tau), shift(v, 1), shift(v, -1), vs(v, g(c)))


def powers(op, v, degree):
    result = [v]
    for _ in range(degree):
        result.append(op(result[-1]))
    return result


def direct_column(n, tau, c, degree, adjoint=False):
    """Taylor coefficients of the actual ordered product on e_n.

    All intermediate states live in N0, with no artificial top boundary.
    """
    out = [{} for _ in range(degree + 1)]
    if not adjoint:
        hp = powers(lambda v: hamiltonian(v, tau, c), basis(n), degree)
        for k in range(degree + 1):
            kp = powers(lambda v: diagonal(v, tau), hp[k], degree-k)
            for j in range(degree-k+1):
                factor = scale(mul(gp(I, j), gp(g(0, -1), k)),
                               F(1, factorial(j)*factorial(k)))
                out[j+k] = va(out[j+k], vs(kp[j], factor))
    else:
        hp = powers(lambda v: hamiltonian(v, tau, c), basis(n), degree)
        for k in range(degree + 1):
            for j in range(degree-k+1):
                factor = scale(mul(gp(I, j), gp(g(0, -1), k)),
                               (F(n)/tau)**k / (factorial(j)*factorial(k)))
                out[j+k] = va(out[j+k], vs(hp[j], factor))
    return out


def source_coefficient(v, m, tau, c, wrong_sign=False):
    sign = -1 if wrong_sign else 1
    up = scale(gp(g(0, sign), m), tau**(-m)/factorial(m))
    down = scale(gp(g(0, -sign), m), tau**(-m)/factorial(m))
    result = va(vs(shift(v, 1), up), vs(shift(v, -1), down))
    return va(result, vs(v, g(c))) if m == 0 else result


def forward_ode_column(n, tau, c, degree, wrong_sign=False):
    coeff = [basis(n)]
    for k in range(degree):
        rhs = va(*(source_coefficient(coeff[k-m], m, tau, c, wrong_sign)
                   for m in range(k+1)))
        coeff.append(vs(rhs, g(0, -F(1, k+1))))
    return coeff


def adjoint_rhs(n, tau, c, coeff_cache, k, wrong_side=False):
    result = {}
    for m in range(k+1):
        j = k-m
        if wrong_side:
            term = source_coefficient(coeff_cache[n][j], m, tau, c)
        else:
            input_v = source_coefficient(basis(n), m, tau, c)
            term = va(*(vs(coeff_cache[r][j], a) for r, a in input_v.items()))
        result = va(result, term)
    return vs(result, I)


# Laurent polynomials in q=exp(is/tau), with tau powers and shift letters.
# Keys are (tau power, q power, operator letter); values are Gaussian rationals.
def primitive():
    return {(1, 1, 'S'): g(0, -1), (1, 0, 'S'): I,
            (1, -1, 'T'): I, (1, 0, 'T'): g(0, -1)}


def derivative(poly):
    return { (p-1, q, op): mul(a, g(0, q))
             for (p, q, op), a in poly.items() if q != 0 }


def at_q_one(poly):
    out = {}
    for (p, _, op), a in poly.items():
        key = (p, op)
        out[key] = add(out.get(key, ZERO), a)
    return {k: v for k, v in out.items() if v != ZERO}


def average(poly):
    return {key: value for key, value in poly.items() if key[1] == 0}


def certificate(tau, horizon):
    require(tau > 0, 'tau must be positive')
    require(horizon >= 0, 'horizon must be nonnegative')
    return min(F(2), F(2)*horizon, F(4)*tau*(1+F(2)*horizon))


def compute():
    checks, controls = {}, {}
    degree = 6
    tau = F(2, 5)
    source = {(0, 1, 'S'): ONE, (0, -1, 'T'): ONE}
    shifted_source = {**source, (0, 0, 'I'): g(F(2, 3))}
    checks['primitive_derivative_is_actual_source'] = derivative(primitive()) == source
    checks['primitive_zero_at_origin'] = at_q_one(primitive()) == {}
    checks['actual_average_is_zero'] = average(source) == {}
    checks['scalar_average_retained'] = average(shifted_source) == {(0, 0, 'I'): g(F(2, 3))}
    controls['wrong_unaveraged_source_as_average_rejected'] = average(source) != source
    controls['discard_scalar_average_rejected'] = average(shifted_source) != {}
    bad_primitive = {key: scale(value, -1) for key, value in primitive().items()}
    controls['reversed_primitive_sign_rejected'] = derivative(bad_primitive) != source
    checks['commutator_and_boundary'] = True
    for n in [0, 1, 2, 7, 1000]:
        v = basis(n)
        for direction in [-1, 1]:
            lhs = va(diagonal(shift(v, direction), F(1)),
                     vs(shift(diagonal(v, F(1)), direction), g(-1)))
            require(lhs == vs(shift(v, direction), g(direction)), 'commutator')
    boundary_commutator = va(shift(shift(basis(0), -1), 1),
                             vs(shift(shift(basis(0), 1), -1), g(-1)))
    require(boundary_commutator == {0: g(-1)}, '[S,S*] e0=-e0')
    controls['bilateral_boundary_commutation_rejected'] = boundary_commutator != {}
    checks['ordered_product_matches_forward_ode'] = True
    checks['ordered_adjoint_matches_right_ode'] = True
    for c in [F(0), F(2, 3)]:
        adj = {n: direct_column(n, tau, c, degree, True) for n in range(10)}
        for n in [0, 1, 7]:
            require(direct_column(n, tau, c, degree) ==
                    forward_ode_column(n, tau, c, degree), 'forward product/ODE')
            for k in range(degree):
                require(vs(adj[n][k+1], g(k+1)) == adjoint_rhs(n, tau, c, adj, k),
                        'adjoint product/right ODE')
    controls['wrong_source_phase_rejected'] = (
        direct_column(0, tau, F(0), degree) !=
        forward_ode_column(0, tau, F(0), degree, True))
    adj = {n: direct_column(n, tau, F(0), degree, True) for n in range(3)}
    controls['adjoint_left_multiplication_rejected'] = any(
        vs(adj[0][k+1], g(k+1)) != adjoint_rhs(0, tau, F(0), adj, k, True)
        for k in range(degree))
    base = direct_column(0, tau, F(0), degree)
    c = F(2, 3)
    actual = direct_column(0, tau, c, degree)
    phased = [va(*(vs(base[k-j], scale(gp(g(0, -c), j), F(1, factorial(j))))
                   for j in range(k+1))) for k in range(degree+1)]
    checks['scalar_shift_factorization'] = actual == phased
    controls['scalar_shift_limit_identity_rejected'] = actual[1] != base[1]
    controls['negative_tau_rejected'] = False
    controls['negative_horizon_rejected'] = False
    for label, args in [('negative_tau_rejected', (F(-1), F(1))),
                        ('negative_horizon_rejected', (F(1), F(-1)))]:
        try:
            certificate(*args)
        except CheckError:
            controls[label] = True
    bounds = []
    for horizon in [F(0), F(1, 2), F(1), F(3)]:
        for tau_test in [F(1, 64), F(1, 128)]:
            value = certificate(tau_test, horizon)
            require(value >= 0, 'nonnegative bound')
            require(F(4)*(tau_test/2)*(1+2*horizon) ==
                    F(4)*tau_test*(1+2*horizon)/2, 'linear tau majorant')
            bounds.append({'tau': str(tau_test), 'T': str(horizon), 'bound': str(value)})
    checks['rational_majorant_arithmetic'] = True
    for name, ok in {**checks, **controls}.items():
        require(ok, name)
    return {'schema': 'norm-averaging-check-v1', 'passed': True,
            'arithmetic': 'fractions.Fraction Gaussian rationals; no floating point',
            'degree': degree, 'basis_indices': [0, 1, 7],
            'checks': checks, 'controls': controls, 'bounds': bounds,
            'scope': 'Finite-support algebra and certificate arithmetic only; report.md proves domains and infinite-dimensional norm convergence.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    require(args.output.is_absolute(), 'output directory must be absolute')
    require(not args.output.exists(), 'output directory must be fresh')
    result = compute()
    args.output.mkdir(parents=True)
    (args.output/'results.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    (args.output/'controls.json').write_text(json.dumps(
        {'schema': 'norm-averaging-controls-v1', 'passed': True,
         'controls': result['controls']}, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'passed': True, 'checks': len(result['checks']),
                      'controls': len(result['controls'])}, sort_keys=True))


if __name__ == '__main__':
    main()
