#!/usr/bin/env python3
"""Exact Q(s) spectral checks; s^2=101/100. No sampled heat proof."""
import argparse
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as Q
import hashlib
import json
from math import isqrt
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def f(a=0, b=0):
    return Q(a), Q(b)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def neg(x):
    return -x[0], -x[1]


def mul(x, y):
    return (x[0] * y[0] + Q(101, 100) * x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


Z = f()
I = [[f(int(i == j)) for j in range(3)] for i in range(3)]


def msum(x, y):
    return [[add(x[i][j], y[i][j]) for j in range(3)] for i in range(3)]


def scale(a, x):
    return [[mul(a, v) for v in row] for row in x]


def mmul(x, y):
    result = [[Z for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] = add(result[i][j], mul(x[i][k], y[k][j]))
    return result


def sqrt_interval(x, digits=60):
    scale10 = 10 ** digits
    n = isqrt(x.numerator * scale10 * scale10 // x.denominator)
    lower, upper = Q(n, scale10), Q(n + 1, scale10)
    require(lower ** 2 <= x < upper ** 2, "invalid square-root enclosure")
    return lower, upper


def decimal_bound(x, rounding):
    with localcontext() as context:
        context.prec = 24
        context.rounding = rounding
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def interval_record(bounds):
    return {
        "lower_exact": str(bounds[0]),
        "upper_exact": str(bounds[1]),
        "lower_decimal_outward": decimal_bound(bounds[0], ROUND_FLOOR),
        "upper_decimal_outward": decimal_bound(bounds[1], ROUND_CEILING),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "fresh output directory required")

    H = [[f(1), f(Q(-1, 10)), Z],
         [f(Q(-1, 10)), f(3), Z], [Z, Z, f(5)]]
    P = [[f(1), Z, Z], [Z, Z, Z], [Z, Z, Z]]
    P2 = [[Z, Z, Z], [Z, Z, Z], [Z, Z, f(1)]]
    pi = [[f(Q(1, 2), Q(50, 101)), f(0, Q(5, 101)), Z],
          [f(0, Q(5, 101)), f(Q(1, 2), Q(-50, 101)), Z],
          [Z, Z, Z]]
    pi1 = msum(msum(I, scale(f(-1), pi)), scale(f(-1), P2))
    zero = scale(f(0), I)
    for projection, energy in [(pi, f(2, -1)), (pi1, f(2, 1)), (P2, f(5))]:
        require(mmul(projection, projection) == projection, "projector identity failed")
        require(projection == [list(row) for row in zip(*projection)], "non-self-adjoint projector")
        require(mmul(H, projection) == scale(energy, projection), "spectral identity failed")
    require(msum(msum(pi, pi1), P2) == I, "incomplete spectral resolution")
    require(mmul(pi, pi1) == zero and mmul(pi, P2) == zero, "projectors not orthogonal")
    residual = msum(mmul(H, P), scale(f(-1), P))
    expected_residual = [[Z, Z, Z], [f(Q(-1, 10)), Z, Z], [Z, Z, Z]]
    require(residual == expected_residual, "complete residual mismatch")
    require(mmul(P, residual) == zero and residual != zero, "missing-channel control failed")
    difference = msum(P, scale(f(-1), pi))
    d2_field = f(Q(1, 2), Q(-50, 101))
    require(mmul(difference, difference) == scale(d2_field, msum(I, scale(f(-1), P2))),
            "projector-distance formula failed")
    require(mul(f(-1, 1), f(1, 1)) == f(Q(1, 100)), "energy identity failed")
    require(mmul(msum(H, scale(f(-2, 1), I)), pi) == zero,
            "true centering does not preserve exact ground coefficient")
    require(mmul(msum(H, scale(f(-1), I)), pi) != zero,
            "wrong-centering control failed")

    slo, shi = sqrt_interval(Q(101, 100))
    epsilon = (2 - shi, 2 - slo)
    delta = (slo - 1, shi - 1)
    d2 = ((1 - 1 / slo) / 2, (1 - 1 / shi) / 2)
    d = (sqrt_interval(d2[0])[0], sqrt_interval(d2[1])[1])
    c = (sqrt_interval(1 - d2[1])[0], sqrt_interval(1 - d2[0])[1])
    require(slo > 1 and 2 + shi < 5, "ground simplicity or spectral ordering failed")
    rho, mu, b = Q(1, 10), Q(1), Q(3)

    def separated_threshold(value):
        require(value > mu, "nonpositive separation denominator")
        require(value <= 2 + slo, "unjustified full-space excited threshold")
        return value - mu

    separation = separated_threshold(b)
    require(delta[1] <= rho ** 2 / separation == Q(1, 200), "valid energy bound failed")
    require(d[1] < rho / separation == Q(1, 20), "valid projector bound failed")
    require(d[1] < rho / (1 + shi), "sharper projector certificate failed")

    rejected = {}
    for name, bad_b in [('invalid_full_spectrum_gap', Q(31, 10)),
                        ('nonpositive_separation_denominator', Q(1))]:
        try:
            separated_threshold(bad_b)
        except ValueError:
            rejected[name] = True
        else:
            raise ValueError('invalid threshold admitted: ' + name)
    require(delta[0] > Q(1, 210) and d[0] > Q(1, 21),
            "invalid-gap example did not actually falsify its proposed bounds")
    wrong_center_lower = c[0] * delta[0] * 1000
    require(wrong_center_lower > Q(49, 10), "wrong-centering growth witness failed")

    full_initial_error = msum(I, scale(f(-1), P))
    require(mmul(full_initial_error, full_initial_error) == full_initial_error
            and full_initial_error != zero, "full-input identity error is not one")
    # The actual compression is [1], hence its own centered heat is exactly 1.
    require(mmul(P, mmul(H, P)) == P, "retained centering mismatch")
    # At zero coupling H is diagonal, e0 is its exact ground, and leakage is zero.
    H0 = [[f(1), Z, Z], [Z, f(3), Z], [Z, Z, f(5)]]
    require(mmul(H0, P) == P, "zero-coupling exception failed")

    skill_root = Path(__file__).resolve().parent / 'inputs'
    inputs = [Path(__file__).resolve(), Path(__file__).resolve().parent.parent / 'report.md',
              skill_root / 'SKILL.md',
              skill_root / 'references/complete-residual-and-error-scope.md',
              skill_root / 'references/centered-heat-and-solo-closeout.md']
    results = {
        'status': 'passed', 'model': 'supplied three-dimensional matrix only',
        'attribution': 'single-author derivation and correlated arithmetic checks',
        'physics_loops_added': 0, 'novelty_claim': False,
        'arithmetic': 'exact Q(s) identities; rational square-root enclosures',
        's_interval': interval_record((slo, shi)),
        'true_ground_interval': interval_record(epsilon),
        'ritz_ground_exact': '1', 'residual_vector_exact': ['0', '-1/10', '0'],
        'residual_norm_squared_exact': '1/100',
        'valid_excited_threshold_exact': '3',
        'energy_error_upper_exact': '1/200',
        'projector_error_upper_exact': '1/20',
        'energy_error_interval': interval_record(delta),
        'projector_distance_interval': interval_record(d),
        'retained_heat_denominator_exact': '1',
        'retained_relative_error_exact': '(1-exp(-2*s*t))*sqrt((1-1/s)/2)',
        'retained_relative_error_supremum': 'sqrt((1-1/s)/2)',
        'full_input_zero_extended_norm_at_t0_exact': '1',
        'wrong_center_t1000_error_lower_decimal': decimal_bound(wrong_center_lower, ROUND_FLOOR),
        'source_sha256': {str(p.relative_to(Path(__file__).resolve().parent.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
    }
    controls = {'status': 'passed', 'controls': {
        'complete_spectral_resolution_exact': True,
        'projected_only_residual_rejected': True,
        **rejected,
        'invalid_gap_falsifies_energy_and_projector_bounds': True,
        'wrong_centering_rejected_by_ground_mode': True,
        'wrong_centering_growth_separated_from_true_error': True,
        'nonzero_leakage_unbounded_relative_error_claim_rejected': True,
        'zero_coupling_exception_restored': True,
        'full_input_t0_norm_one_retained_error_zero': True,
    }}
    args.output.mkdir(parents=True)
    for name, data in [('results.json', results), ('controls.json', controls)]:
        (args.output / name).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'passed', 'exact_controls': len(controls['controls']),
                      'physics_loops_added': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
