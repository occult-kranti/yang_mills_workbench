#!/usr/bin/env python3
"""Finite tilted-Haar susceptibility: exact launch bounds, numerical ODE tests.

The ODE solves a one-plaquette Euclidean expectation. It is not real-time
evolution and the floating integrations are not interval endpoint certificates.
All acceptance gates use explicit exceptions and survive Python -O.
"""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.special import ive, kv


class ContractError(ValueError):
    """Input or mathematical acceptance contract was not satisfied."""


def finite_real(value, name):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, Fraction, np.integer, np.floating)):
        raise ContractError(f"{name} must be a finite real scalar")
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise ContractError(f"{name} must be a finite real scalar") from exc
    if not math.isfinite(result):
        raise ContractError(f"{name} must be finite")
    return result


def rational(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise ContractError(f"{name} must be int or Fraction for exact arithmetic")
    return Fraction(value)


def series_coefficients(order=3, coefficient=3):
    """a[n] multiplies kappa**(2*n+1); derive by matching the Riccati equation."""
    if isinstance(order, bool) or not isinstance(order, int) or not 0 <= order <= 12:
        raise ContractError("series order must be an integer from 0 through 12")
    coefficient = rational(coefficient, "coefficient")
    if coefficient <= 0:
        raise ContractError("coefficient must be positive")
    values = [1 / (coefficient + 1)]
    for n in range(1, order + 1):
        values.append(-sum(values[i] * values[n - 1 - i] for i in range(n)) / (2 * n + coefficient + 1))
    return values


def series_value(kappa, coefficients):
    """Exact only when kappa and all coefficients are rational."""
    if not coefficients:
        raise ContractError("coefficient list must be nonempty")
    if any(isinstance(c, bool) or not isinstance(c, Fraction) for c in coefficients):
        raise ContractError("series coefficients must be Fractions")
    value = finite_real(kappa, "kappa")
    if abs(value) > 1:
        raise ContractError("local series helper is restricted to |kappa| <= 1")
    return sum(c * kappa ** (2 * n + 1) for n, c in enumerate(coefficients))


def residual_polynomial(coefficients, coefficient=3):
    """Exact sparse coefficients of R=k p'+c p-k(1-p²)."""
    coefficient = rational(coefficient, "coefficient")
    if not coefficients or any(not isinstance(c, Fraction) for c in coefficients):
        raise ContractError("a nonempty Fraction coefficient list is required")
    residual = {1: Fraction(-1)}
    for n, c in enumerate(coefficients):
        power = 2 * n + 1
        residual[power] = residual.get(power, Fraction()) + (power + coefficient) * c
    for i, a in enumerate(coefficients):
        for j, b in enumerate(coefficients):
            power = 2 * i + 2 * j + 3
            residual[power] = residual.get(power, Fraction()) + a * b
    return {power: value for power, value in sorted(residual.items()) if value}


def initial_bound(epsilon, order=3):
    """Rigorous rational bound on |u(epsilon)-p(epsilon)|, no ODE rounding.

    u is the already constructed regular tilted-Haar expectation. On [0,eps],
    u>=0 and p>=0 imply the integrating-factor attenuation <=(s/eps)^3.
    """
    epsilon = rational(epsilon, "epsilon")
    if not 0 < epsilon <= Fraction(1, 2):
        raise ContractError("exact initialization requires 0 < epsilon <= 1/2")
    coefficients = series_coefficients(order)
    positive_witness = coefficients[0] - sum(abs(c) * epsilon ** (2 * n) for n, c in enumerate(coefficients) if n)
    if positive_witness <= 0:
        raise ContractError("local polynomial positivity witness failed")
    residual = residual_polynomial(coefficients)
    bound = sum(abs(c) * epsilon ** power / (power + 3) for power, c in residual.items())
    return {
        "epsilon": str(epsilon), "order": order, "polynomial_degree": 2 * order + 1,
        "coefficients": [str(c) for c in coefficients],
        "polynomial_value": str(series_value(epsilon, coefficients)),
        "positive_witness": str(positive_witness),
        "residual_coefficients": {str(k): str(v) for k, v in residual.items()},
        "analytic_initial_error_bound": str(bound),
        "scope": "exact regular solution versus exact rational launch polynomial; excludes conversion and ODE roundoff",
    }


def bessel_mean(kappa):
    """Scaled I_2/I_1, with zero and odd reflection handled explicitly."""
    kappa = finite_real(kappa, "kappa")
    if abs(kappa) > 100:
        raise ContractError("diagnostic Bessel domain is |kappa| <= 100")
    if kappa == 0:
        return 0.0
    k = abs(kappa)
    # Series prevents the I_2 underflow / I_1 underflow corner for tiny input.
    if k < 1e-6:
        return float(series_value(kappa, series_coefficients(3)))
    result = float(ive(2, k) / ive(1, k))
    if not math.isfinite(result):
        raise ContractError("nonfinite scaled Bessel mean")
    return math.copysign(result, kappa)


def quadrature_moments(kappa):
    """Separate direct integral in theta; scaled weight avoids exp overflow."""
    kappa = finite_real(kappa, "kappa")
    if abs(kappa) > 20:
        raise ContractError("quadrature study is restricted to |kappa| <= 20")
    weights = []
    estimates = []
    for n in range(4):
        value, estimate = quad(
            lambda theta: math.cos(theta) ** n * math.exp(kappa * math.cos(theta) - abs(kappa)) * math.sin(theta) ** 2,
            0, math.pi, epsabs=2e-13, epsrel=2e-13, limit=200,
        )
        weights.append(value)
        estimates.append(estimate)
    if not all(math.isfinite(x) for x in weights + estimates) or weights[0] <= 0:
        raise ContractError("quadrature did not return finite normalized data")
    moments = [x / weights[0] for x in weights]
    return {"moments": moments, "variance": moments[2] - moments[1] ** 2,
            "quad_error_estimates": estimates, "scope": "floating quadrature, not interval bounds"}


def rhs(kappa, mean, coefficient=3):
    kappa = finite_real(kappa, "kappa")
    mean = finite_real(mean, "mean")
    coefficient = finite_real(coefficient, "coefficient")
    if kappa <= 0 or coefficient <= 0:
        raise ContractError("divided Riccati RHS requires kappa > 0 and coefficient > 0")
    result = 1.0 - mean * mean - coefficient * mean / kappa
    if not math.isfinite(result):
        raise ContractError("Riccati RHS overflowed")
    return result


def integrate_response(epsilon=Fraction(1, 100), stop=5, rtol=1e-11, order=3, coefficient=3, grid=None):
    epsilon = rational(epsilon, "epsilon")
    if not 0 < epsilon <= Fraction(1, 2):
        raise ContractError("launch epsilon must be in (0,1/2]")
    stop = finite_real(stop, "stop")
    rtol = finite_real(rtol, "rtol")
    coefficient = rational(coefficient, "coefficient")
    if not float(epsilon) < stop <= 20 or not 1e-13 <= rtol <= 1e-3:
        raise ContractError("require epsilon < stop <= 20 and 1e-13 <= rtol <= 1e-3")
    if coefficient <= 0:
        raise ContractError("coefficient must be positive")
    if grid is None:
        grid = np.linspace(float(epsilon), stop, 201)
    else:
        try:
            grid = np.asarray(grid, dtype=float)
        except (ValueError, TypeError) as exc:
            raise ContractError("grid must contain finite ascending samples") from exc
        if grid.ndim != 1 or grid.size == 0 or not np.isfinite(grid).all() or np.any(np.diff(grid) <= 0):
            raise ContractError("grid must contain finite strictly ascending samples")
        if grid[0] < float(epsilon) or grid[-1] > stop:
            raise ContractError("grid must stay in [epsilon,stop]")
    coefficients = series_coefficients(order, coefficient)
    initial = float(series_value(epsilon, coefficients))
    solution = solve_ivp(lambda k, y: [rhs(k, y[0], coefficient)], (float(epsilon), stop), [initial],
                         method="DOP853", t_eval=grid, rtol=rtol, atol=rtol / 100)
    if not solution.success or solution.y.shape != (1, len(grid)) or not np.isfinite(solution.y).all():
        raise ContractError(f"incomplete ODE integration: {solution.message}")
    return {"grid": solution.t, "mean": solution.y[0], "nfev": solution.nfev, "initial": initial,
            "epsilon": str(epsilon), "rtol": rtol, "atol": rtol / 100, "coefficient": str(coefficient), "order": order}


def zero_variance_root(kappa):
    kappa = finite_real(kappa, "kappa")
    if abs(kappa) > 100:
        raise ContractError("algebraic root diagnostic domain is |kappa| <= 100")
    return 2 * kappa / (3 + math.hypot(3, 2 * kappa))


def wrong_closure_fixture():
    k = Fraction(9, 8)
    u = Fraction(1, 3)
    moments = [u ** n for n in range(4)]
    n0 = -3 * moments[1] + k * (moments[0] - moments[2])
    n1 = moments[0] - 4 * moments[2] + k * (moments[1] - moments[3])
    return {"kappa": str(k), "mean": str(u), "moments": [str(x) for x in moments],
            "n0_residual": str(n0), "n1_residual": str(n1),
            "H1_leading_minor": "1", "H1_determinant": str(moments[2] - moments[1] ** 2),
            "L0": str(1 - moments[2]), "scope": "Dirac point measure is PSD and passes n=0 but fails n=1 tilted-Haar IBP"}


class Gates:
    def __init__(self):
        self.records = []

    def check(self, name, condition, detail=None):
        if not isinstance(condition, (bool, np.bool_)):
            raise ContractError(f"gate {name} condition must be Boolean")
        self.records.append({"name": name, "status": "passed" if condition else "failed", "detail": detail})
        if not condition:
            raise RuntimeError(f"failed gate: {name}: {detail}")

    def rejects(self, name, operation):
        try:
            operation()
        except ContractError as exc:
            self.check(name, True, str(exc))
            return
        self.check(name, False, "invalid input accepted")


def write_csv(path, rows):
    if not rows:
        raise ContractError("empty output collection")
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def study(output):
    output.mkdir(parents=True, exist_ok=True)
    before = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    gates = Gates()
    expected = [Fraction(1, 4), -Fraction(1, 96), Fraction(1, 1536), -Fraction(1, 23040), Fraction(13, 4423680)]
    gates.check("exact series coefficients through degree 9", series_coefficients(4) == expected)
    residual = residual_polynomial(expected)
    gates.check("coefficient matching cancels all powers through degree 9", min(residual) == 11)
    gates.check("regular origin susceptibility is 1/4", series_coefficients(0)[0] == Fraction(1, 4))
    gates.check("coefficient mutation changes origin susceptibility to 1/3", series_coefficients(0, 2)[0] == Fraction(1, 3))
    init = [initial_bound(eps, order) for order in (1, 3) for eps in (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16), Fraction(1, 100))]
    for row in init:
        eps = float(Fraction(row["epsilon"]))
        numerical_error = abs(float(Fraction(row["polynomial_value"])) - bessel_mean(eps))
        # Floating comparator receives an explicit absolute allowance; this is
        # not used to establish the analytic bound, which follows from the proof.
        gates.check(f"launch polynomial diagnostic order={row['order']} eps={row['epsilon']}",
                    numerical_error <= float(Fraction(row["analytic_initial_error_bound"])) + 5e-16,
                    {"floating_error": numerical_error, "comparison_allowance": 5e-16})

    fixture = wrong_closure_fixture()
    gates.check("wrong closure passes first recurrence", Fraction(fixture["n0_residual"]) == 0)
    gates.check("wrong closure H1 is PSD", Fraction(fixture["H1_leading_minor"]) > 0 and Fraction(fixture["H1_determinant"]) == 0)
    gates.check("wrong closure localizing L0 is PSD", Fraction(fixture["L0"]) == Fraction(8, 9))
    gates.check("next recurrence rejects wrong closure", Fraction(fixture["n1_residual"]) == Fraction(8, 9))

    reference_rows = []
    for k in (-20, -5, -2, -1, -0.01, 0, 0.01, 1, 2, 5, 20):
        quad_result = quadrature_moments(k)
        m = quad_result["moments"]
        bessel = bessel_mean(k)
        gates.check(f"Bessel versus independent integral k={k}", abs(m[1] - bessel) < 3e-13)
        gates.check(f"positive susceptibility k={k}", quad_result["variance"] > 0)
        n0 = -3 * m[1] + k * (1 - m[2])
        n1 = 1 - 4 * m[2] + k * (m[1] - m[3])
        gates.check(f"first two Haar identities k={k}", max(abs(n0), abs(n1)) < 4e-12)
        reference_rows.append({"kappa": k, "mean_quad": m[1], "mean_bessel": bessel,
                               "variance_quad": quad_result["variance"], "n0_residual": n0, "n1_residual": n1})
    for k in (Fraction(1, 100000000), Fraction(1, 100), 1, 5, 20):
        gates.check(f"odd mean reflection k={k}", bessel_mean(-k) == -bessel_mean(k))
        pos, neg = quadrature_moments(k), quadrature_moments(-k)
        gates.check(f"even variance independent integral k={k}", abs(pos["variance"] - neg["variance"]) < 5e-14)
    origin = quadrature_moments(0)
    gates.check("origin integral is Haar variance 1/4", abs(origin["variance"] - 0.25) < 1e-14)
    gates.check("false zero-variance root has wrong derivative", abs(zero_variance_root(1e-7) / 1e-7 - 1 / 3) < 1e-13)

    # Keep launch error and tolerance error on different experimental axes.
    common_grid = np.linspace(0.5, 5, 181)
    reference = np.asarray([bessel_mean(k) for k in common_grid])
    epsilon_rows = []
    for eps in (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)):
        run = integrate_response(epsilon=eps, order=1, rtol=2e-13, grid=common_grid)
        error = np.abs(run["mean"] - reference)
        certificate = initial_bound(eps, 1)
        epsilon_rows.append({"epsilon": float(eps), "epsilon_exact": str(eps), "polynomial_degree": 3,
                             "rtol": run["rtol"], "initial_analytic_bound": float(Fraction(certificate["analytic_initial_error_bound"])),
                             "max_mean_difference": float(error.max()), "at_kappa_half": float(error[0]),
                             "at_kappa_five": float(error[-1]), "nfev": run["nfev"]})
    gates.check("epsilon refinement resolves launch dependence", epsilon_rows[0]["max_mean_difference"] > 100 * epsilon_rows[1]["max_mean_difference"])
    gates.check("epsilon refinement next level improves", epsilon_rows[1]["max_mean_difference"] > 50 * epsilon_rows[2]["max_mean_difference"])
    gates.check("finest launch sweep agrees with Bessel", epsilon_rows[-1]["max_mean_difference"] < 2e-11)

    tolerance_grid = np.linspace(0.05, 5, 199)
    tolerance_reference = np.asarray([bessel_mean(k) for k in tolerance_grid])
    tolerance_rows = []
    for tol in (1e-5, 1e-8, 1e-11, 2e-13):
        run = integrate_response(rtol=tol, grid=tolerance_grid)
        error = np.abs(run["mean"] - tolerance_reference)
        tolerance_rows.append({"epsilon_exact": "1/100", "polynomial_degree": 7,
                               "rtol": tol, "atol": run["atol"], "max_mean_difference": float(error.max()),
                               "endpoint_mean_difference": float(error[-1]), "nfev": run["nfev"]})
    gates.check("tolerance refinement improves first decade group", tolerance_rows[0]["max_mean_difference"] > 20 * tolerance_rows[1]["max_mean_difference"])
    gates.check("tolerance refinement improves second decade group", tolerance_rows[1]["max_mean_difference"] > 20 * tolerance_rows[2]["max_mean_difference"])
    gates.check("tight integration agrees with Bessel", tolerance_rows[-1]["max_mean_difference"] < 2e-12)

    positive_grid = np.linspace(0.025, 5, 200)
    fine = integrate_response(rtol=2e-13, grid=positive_grid)
    wrong = integrate_response(rtol=2e-13, coefficient=2, grid=positive_grid)
    wrong_gap = max(abs(a - b) for a, b in zip(wrong["mean"], fine["mean"]))
    gates.check("coefficient 3 to 2 mutation is discriminated", wrong_gap > 0.05, wrong_gap)
    curves = []
    for sign in (-1, 1):
        for k, u_ode, bad in zip(positive_grid, fine["mean"], wrong["mean"]):
            kk = float(sign * k)
            q = quadrature_moments(kk)
            exact = bessel_mean(kk)
            curves.append({"kappa": kk, "mean_bessel": exact, "mean_quad": q["moments"][1],
                           "mean_ode_reflected": float(sign * u_ode), "susceptibility_quad": q["variance"],
                           "mean_zero_variance_root": zero_variance_root(kk), "mean_wrong_coefficient_reflected": float(sign * bad),
                           "ode_bessel_difference": abs(float(sign * u_ode) - exact)})
    curves.append({"kappa": 0.0, "mean_bessel": 0.0, "mean_quad": origin["moments"][1], "mean_ode_reflected": 0.0,
                   "susceptibility_quad": origin["variance"], "mean_zero_variance_root": 0.0,
                   "mean_wrong_coefficient_reflected": 0.0, "ode_bessel_difference": 0.0})
    curves.sort(key=lambda row: row["kappa"])
    gates.check("finite recorded plot diagnostics", all(math.isfinite(value) for row in curves for value in row.values()))
    gates.check("zero-variance omission is visibly wrong", max(abs(row["mean_zero_variance_root"] - row["mean_bessel"]) for row in curves) > 0.04)

    branch_rows = []
    for k in (0.001, 0.01, 0.1, 0.5, 1, 5):
        singular = float(-kv(2, k) / kv(1, k))
        branch_rows.append({"kappa": k, "regular_mean": bessel_mean(k), "pure_K_branch": singular, "kappa_times_K_branch": k * singular})
    gates.check("K branch violates compact mean range", all(row["pure_K_branch"] < -1 for row in branch_rows))
    gates.check("K branch approaches -2/kappa", abs(branch_rows[0]["kappa_times_K_branch"] + 2) < 1e-5)

    invalid_cases = [
        ("reject origin divided RHS", lambda: rhs(0, 0)),
        ("reject negative divided RHS", lambda: rhs(-1, 0)),
        ("reject float exact epsilon", lambda: initial_bound(0.1)),
        ("reject zero exact epsilon", lambda: initial_bound(Fraction(0))),
        ("reject large launch epsilon", lambda: initial_bound(Fraction(3, 4))),
        ("reject Boolean order", lambda: series_coefficients(True)),
        ("reject negative order", lambda: series_coefficients(-1)),
        ("reject invalid coefficient", lambda: series_coefficients(1, 0)),
        ("reject empty grid", lambda: integrate_response(grid=[])),
        ("reject repeated grid", lambda: integrate_response(grid=[1, 1])),
        ("reject reversed grid", lambda: integrate_response(grid=[2, 1])),
        ("reject nonfinite grid", lambda: integrate_response(grid=[1, float('nan')])),
        ("reject prelaunch grid", lambda: integrate_response(grid=[0, 1])),
        ("reject offdomain grid", lambda: integrate_response(grid=[1, 6])),
        ("reject nonfinite tolerance", lambda: integrate_response(rtol=float('nan'))),
        ("reject impossible tolerance", lambda: integrate_response(rtol=1e-20)),
        ("reject Boolean kappa", lambda: bessel_mean(True)),
        ("reject nonfinite kappa", lambda: bessel_mean(float('inf'))),
        ("reject unsupported quadrature domain", lambda: quadrature_moments(100)),
        ("reject RHS overflow", lambda: rhs(1, 1e308)),
    ]
    for name, operation in invalid_cases:
        gates.rejects(name, operation)

    write_csv(output / "response_curves.csv", curves)
    write_csv(output / "epsilon_sweep.csv", epsilon_rows)
    write_csv(output / "tolerance_sweep.csv", tolerance_rows)
    write_csv(output / "reference_checks.csv", reference_rows)
    write_csv(output / "singular_branches.csv", branch_rows)
    (output / "initialization_bounds.json").write_text(json.dumps(init, indent=2) + "\n")
    (output / "wrong_closure_fixture.json").write_text(json.dumps(fixture, indent=2) + "\n")

    plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3), constrained_layout=True)
    x = [r["kappa"] for r in curves]
    axes[0].plot(x, [r["mean_bessel"] for r in curves], color="#1f5588", label="Regular tilted-Haar mean")
    axes[0].plot(x, [r["mean_zero_variance_root"] for r in curves], "--", color="#bd573a", label="Variance omitted")
    axes[0].plot(x, [r["mean_wrong_coefficient_reflected"] for r in curves], ":", color="#84633a", label="Wrong coefficient 3 → 2")
    axes[0].set(xlabel="Euclidean coupling κ", ylabel="Mean u = E[x]", title="A scalar equation closes only with response")
    axes[0].legend(fontsize=9)
    axes[1].plot(x, [r["susceptibility_quad"] for r in curves], color="#26765a", label="u′ = Var(x), direct integral")
    axes[1].axhline(0, color="#bd573a", linestyle="--", label="False zero variance")
    axes[1].scatter([0], [0.25], color="#26765a", zorder=3)
    axes[1].set(xlabel="Euclidean coupling κ", ylabel="Susceptibility", title="The origin fixes u′(0) = 1/4")
    axes[1].legend(fontsize=9)
    for ax in axes:
        ax.grid(alpha=0.2)
    fig.savefig(output / "response_closure.png", dpi=180)
    fig.savefig(output / "response_closure.svg")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3), constrained_layout=True)
    axes[0].loglog([r["epsilon"] for r in epsilon_rows], [r["max_mean_difference"] for r in epsilon_rows], "o-", color="#1f5588")
    axes[0].set(xlabel="Launch ε (cubic polynomial)", ylabel="Maximum difference from Bessel ratio",
                title="Vary launch point; fix ODE tolerance")
    axes[1].loglog([r["rtol"] for r in tolerance_rows], [r["max_mean_difference"] for r in tolerance_rows], "o-", color="#26765a")
    axes[1].set(xlabel="ODE relative tolerance (ε = 0.01)", ylabel="Maximum difference from Bessel ratio",
                title="Vary tolerance; fix launch point")
    for ax in axes:
        ax.grid(alpha=0.2, which="both")
    fig.savefig(output / "response_refinement.png", dpi=180)
    fig.savefig(output / "response_refinement.svg")
    plt.close(fig)

    after = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    gates.check("source bytes unchanged during study", before == after)
    if not gates.records or any(row["status"] != "passed" for row in gates.records):
        raise RuntimeError("incomplete acceptance record")
    result = {"schema": "ym13-response-v1", "status": "passed", "scope": "finite one-plaquette Euclidean response; floating ODE comparisons are diagnostic",
              "source_sha256": before, "check_count": len(gates.records), "checks": gates.records,
              "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
              "tight_ode_max_difference": tolerance_rows[-1]["max_mean_difference"],
              "wrong_coefficient_max_difference": wrong_gap,
              "unproved": ["floating ODE endpoint interval certificate", "Hamiltonian spectral gap from this susceptibility", "4D continuum Yang-Mills construction"]}
    (output / "results.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir()) if p.is_file() and p.name != "SHA256SUMS.json"}
    (output / "SHA256SUMS.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "check_count": result["check_count"], "source_sha256": before,
                      "tight_ode_max_difference": result["tight_ode_max_difference"]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "output")
    study(parser.parse_args().output)
