#!/usr/bin/env python3
"""Exact, standard-library-only reproduction of the supplied SU(2) case.

Run from this directory: python -B check.py
All arithmetic is rational. Polynomial maps use exponent keys.
The generator extension is the explicitly assumed reversible divergence form.
No input data or source files are modified.
"""
from fractions import Fraction as Q
from math import comb, factorial, prod
import json
from pathlib import Path


def poly(terms):
    return {k: Q(v) for k, v in terms.items() if v}


def add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, Q(0)) + v
    return poly(out)


def scale(p, c):
    return poly({k: v * c for k, v in p.items()})


def mul(*ps):
    out = {0: Q(1)}
    for p in ps:
        nxt = {}
        for i, u in out.items():
            for j, v in p.items():
                nxt[i+j] = nxt.get(i+j, Q(0)) + u*v
        out = poly(nxt)
    return out


def diff(p):
    return poly({k-1: k*v for k, v in p.items() if k})


def moment(k):
    # Supplied Catalan moment formula.
    return Q(0) if k % 2 else Q(comb(k, k//2), (k//2+1) * 2**k)


def moment_beta(k):
    # Independent formulation from B(n+1/2,3/2)/B(1/2,3/2).
    if k % 2:
        return Q(0)
    return prod((Q(2*j+1, 2*j+4) for j in range(k//2)), start=Q(1))


def expect(p, moments=moment):
    return sum((v*moments(k) for k, v in p.items()), Q(0))


def gegenbauer(n, lam):
    # NIST DLMF 18.5.10, finite series, checked 2026-09-14.
    return poly({n-2*j: Q((-1)**j * prod(range(lam, lam+n-j)) * 2**(n-2*j),
                         factorial(j)*factorial(n-2*j))
                 for j in range(n//2+1)})


def chebyshev_u(n):
    # Independent recurrence, U_0=1, U_1=2x, U_{n+1}=2xU_n-U_{n-1}.
    prev, cur = {0: Q(1)}, {1: Q(2)}
    if n == 0:
        return prev
    for _ in range(1, n):
        prev, cur = cur, add(mul({1: Q(2)}, cur), scale(prev, -1))
    return cur


ONE = {0: Q(1)}
X = {1: Q(1)}
A = {0: Q(1, 4), 2: Q(-1, 4)}
B = {1: Q(-3, 4)}
P = {1: Q(1, 8), 3: Q(-5, 6), 5: Q(1)}
M = [ONE, add(ONE, scale(P, Q(1, 4)))]
F = [X, {1: Q(1), 2: Q(1, 4)}, {2: Q(1), 3: Q(1)}]
G = {3: Q(1), 4: Q(1)}


def delta(f):
    return add(mul(A, diff(diff(f))), mul(B, diff(f)))


def generator(m, f):
    # rho^-1 (rho * m * A * f')' = m*Delta(f) + A*m'*f'.
    return add(mul(m, delta(f)), mul(A, diff(m), diff(f)))


def rate(m, f):
    return expect(mul(m, A, diff(f), diff(f)))


def curvature(m, f):
    lf = generator(m, f)
    # Check two formulations: <Lf,Lf> and <f,L^2 f>.
    by_norm = expect(mul(lf, lf))
    by_iteration = expect(mul(f, generator(m, lf)))
    assert by_norm == by_iteration
    return by_norm


def rank(matrix):
    rows = [[Q(x) for x in row] for row in matrix]
    r = 0
    for c in range(len(rows[0])):
        pivot = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        divisor = rows[r][c]
        rows[r] = [v/divisor for v in rows[r]]
        for i in range(len(rows)):
            if i != r:
                multiple = rows[i][c]
                rows[i] = [u-multiple*v for u, v in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def serial(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def main():
    # Frozen expected results are checked against executed exact calculations.
    expected_rates = [Q(3, 16), Q(25, 128), Q(59, 256)]
    rates = [[rate(m, f) for f in F] for m in M]
    assert rates == [expected_rates, expected_rates]
    orth = [expect(mul(A, P, {k: Q(1)})) for k in range(5)]
    assert orth == [0]*5
    assert P == scale(gegenbauer(5, 2), Q(1, 192))
    norm = expect(mul(A, P, P))
    assert norm == Q(1, 12288)
    bound = sum(abs(v) for v in P.values())
    assert bound == Q(47, 24)
    assert 1-bound/4 == Q(49, 96) > 0

    lx = [generator(m, X) for m in M]
    u6 = chebyshev_u(6)
    assert lx[1] == add(B, scale(u6, Q(-1, 128)))
    assert expect(mul(u6, u6)) == 1
    assert expect(mul(X, u6)) == 0
    curvatures = [curvature(m, X) for m in M]
    assert curvatures == [Q(9, 64), Q(2305, 16384)]
    assert curvatures[1]-curvatures[0] == Q(1, 16384)
    new_rates = [rate(m, G) for m in M]
    assert new_rates == [Q(51, 256), Q(409, 2048)]
    assert new_rates[1]-new_rates[0] == Q(1, 2048)

    # Verify stationarity and the rate identity, not just one output equality.
    for m in M:
        for f in F+[G]:
            assert expect(generator(m, f)) == 0
            assert -expect(mul(f, generator(m, f))) == rate(m, f)
            integrand = mul(m, A, diff(f), diff(f))
            assert expect(integrand) == expect(integrand, moment_beta)
            curvature(m, f)
    for k in range(21):
        assert moment(k) == moment_beta(k)

    matrix = [[rate({k: Q(1)}, f) for k in range(6)] for f in F]
    assert rank(matrix) == 3
    assert all(sum((row[k]*P.get(k, Q(0)) for k in range(6)), Q(0)) == 0
               for row in matrix)

    # Discriminating wrong-model control: m*Delta omits the necessary drift.
    wrong_mean = expect(mul(M[1], delta(X)))
    assert wrong_mean == Q(-1, 1024) != 0
    wrong_rates = [rate(add(ONE, {1: Q(1, 4)}), f) for f in F]
    assert wrong_rates != expected_rates  # Not every odd deformation is invisible.

    result = {
        "arithmetic": "exact Python fractions; no quadrature or finite-time fit",
        "original_observables": ["x", "x+x^2/4", "x^2+x^3"],
        "original_slopes_m0_m1": rates,
        "E_A_p_xk_k0_to_4": orth,
        "E_A_p_squared": norm,
        "p_coefficient_l1": bound,
        "certified_m1_lower_bound": 1-bound/4,
        "L_m0_x": lx[0], "L_m1_x": lx[1],
        "C_x_second_derivative_m0_m1": curvatures,
        "second_derivative_difference": curvatures[1]-curvatures[0],
        "t_squared_coefficient_difference": (curvatures[1]-curvatures[0])/2,
        "additional_observable": "x^3+x^4",
        "additional_slopes_m0_m1": new_rates,
        "additional_slope_difference": new_rates[1]-new_rates[0],
        "monomial_mobility_basis_0_to_5_matrix": matrix,
        "monomial_matrix_rank": rank(matrix),
        "monomial_matrix_nullity": 6-rank(matrix),
        "wrong_generator_E_mDelta_x": wrong_mean,
        "control_mobility_1_plus_x_over_4_slopes": wrong_rates,
        "scope": "finite initial-slope nonidentification; follow-ups separate these candidates",
    }
    text = json.dumps(serial(result), indent=2, sort_keys=True)+"\n"
    Path(__file__).with_name("exact_results.json").write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
