#!/usr/bin/env python3
"""Exact arithmetic checks supporting report.md; not a truncation proof."""

from fractions import Fraction as Q
from math import factorial
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sinc_interval(x):
    """Alternating series: degree 16 upper bound, degree 18 lower bound."""
    require(Q(0) < x <= Q(3, 8), "Series range not justified")
    terms = [x ** (2 * j) / factorial(2 * j + 1) for j in range(10)]
    require(all(a > b for a, b in zip(terms, terms[1:])),
            "Alternating terms must decrease")
    upper = sum((-1) ** j * terms[j] for j in range(9))
    lower = upper - terms[9]
    require(lower < upper, "Invalid sinc interval")
    return lower, upper


def matrices(size, wrong_adjoint_sign=False, diagonal_source=False):
    a, k = {}, {}
    for n in range(size - 1):
        w = Q(1, n + 1)
        c = Q(1, (n + 1) * (2 * n + 1))
        a[n + 1, n] = a[n, n + 1] = w
        k[n + 1, n] = c
        k[n, n + 1] = c if wrong_adjoint_sign else -c
    if diagonal_source:
        a[0, 0] = Q(1)
    return a, k


def commutator_ok(a, k):
    indices = set(a) | set(k)
    return all((j * j - i * i) * k.get((i, j), Q(0))
               == -a.get((i, j), Q(0)) for i, j in indices)


def skew_ok(k):
    return all(value == -k.get((j, i), Q(0))
               for (i, j), value in k.items())


def interval_record(interval):
    lower, upper = interval
    return {
        "lower_exact": str(lower),
        "upper_exact": str(upper),
        "lower_float_display": float(lower),
        "upper_float_display": float(upper),
        "width_exact": str(upper - lower),
    }


def main():
    q = sinc_interval(Q(1, 8))
    q1 = sinc_interval(Q(3, 8))
    require(Q(0) < q1[0] < q1[1] < q[0] < q[1] < Q(1),
            "Failed strict contraction or separation")
    # pi > 3, so the envelope 1/pi < 1/3 lies below both sinc values.
    require(Q(1, 3) < q1[0], "Tail envelope comparison failed")
    simple_upper = Q(1) - Q(1, 384) + Q(1, 491520)
    require(q[1] < simple_upper < Q(1), "Simple upper certificate failed")

    a, k = matrices(65)
    require(skew_ok(k), "Candidate is not skew")
    require(commutator_ok(a, k), "Finite-core commutator identity failed")

    for n in range(1025):
        w = Q(1, n + 1)
        c = Q(1, (n + 1) * (2 * n + 1))
        require((2 * n + 1) * c == w, "Adjacent inverse mismatch")
        require((n + 1) ** 2 * c <= 1, "GC coefficient bound failed")
        require(n ** 2 * c <= Q(1, 2), "CG coefficient bound failed")
        if n:
            c_previous = Q(1, n * (2 * n - 1))
            require((n - 1) ** 2 * c_previous <= Q(1, 2),
                    "GC* coefficient bound failed")
            require(n ** 2 * c_previous <= 1,
                    "C*G coefficient bound failed")

    a_wrong, k_wrong = matrices(65, wrong_adjoint_sign=True)
    require(not skew_ok(k_wrong), "Wrong-sign control was not rejected")
    require(not commutator_ok(a_wrong, k_wrong),
            "Wrong-sign commutator control was not rejected")
    a_diag, k_diag = matrices(65, diagonal_source=True)
    require(not commutator_ok(a_diag, k_diag),
            "Diagonal obstruction control was not rejected")
    require((0 ** 2 - 0 ** 2) * Q(7) != -a_diag[0, 0],
            "Diagonal commutator obstruction failed")

    output = {
        "status": "passed",
        "scope": "Arithmetic controls; infinite-dimensional claims proved in report.md",
        "theta_exact": "1/8",
        "q_interval": interval_record(q),
        "q1_interval": interval_record(q1),
        "simple_q_upper_exact": str(simple_upper),
        "norm_upper_bounds_float_display": {
            str(exponent): float(2 * q[1] ** exponent)
            for exponent in (1, 100, 1000, 5000)
        },
        "finite_core_dimension": 65,
        "coefficient_checks_n_inclusive": [0, 1024],
        "controls": {
            "wrong_adjoint_sign_rejected": True,
            "diagonal_source_obstruction_detected": True,
        },
        "proof_obligations": {
            "uniform_sinc_bound": "analytic monotonicity plus tail envelope in report",
            "operator_norm_bound": "exact weighted-shift norm formula in report",
            "domain_invariance": "bounded GC and GC* plus closedness in report",
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
