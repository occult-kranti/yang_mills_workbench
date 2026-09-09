"""Round-6 finite-regulator coefficient and obstruction experiments.

This module evaluates the frozen round-6 contract.  It deliberately keeps
the continuous integral, finite quadrature, exact rational certificate and
formal full-window tail as separate diagnostics; none is an ODE run or a
claim about physical QED.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from scipy.integrate import quad
from scipy.special import digamma

ROOT = Path(__file__).resolve().parent
DEPS = ROOT / "../round5/deps"
if str(DEPS) not in sys.path:
    sys.path.insert(0, str(DEPS))
import mpmath as mp  # type: ignore  # bundled dependency

ALPHA = 1.0 / 137.035999084
E2 = 4.0 * math.pi * ALPHA
PI = math.pi
TOL = 2e-11


def _finite(x: Any) -> bool:
    try:
        return math.isfinite(float(x))
    except (TypeError, ValueError, OverflowError):
        return False


def validate_params(b: Any, N: Any, K: Any, a: Any) -> None:
    if isinstance(b, bool) or not isinstance(b, (int, float)) or not _finite(b) or b <= 0:
        raise ValueError("b must be finite and strictly positive")
    if isinstance(N, bool) or not isinstance(N, int) or N < 0:
        raise ValueError("N must be an integer >= 0")
    if isinstance(K, bool) or not isinstance(K, (int, float)) or not _finite(K) or K <= 0:
        raise ValueError("K must be finite and strictly positive")
    if not _finite(a):
        raise ValueError("a must be finite")


def mass(b: float, n: int) -> float:
    return math.sqrt(1.0 + 2.0 * b * n)


def degeneracy(n: int) -> int:
    return 1 if n == 0 else 2


def primitive(M: float, y: float) -> float:
    u = y / math.sqrt(M * M + y * y)
    return (u - u**3 / 3.0) / (M * M)


def density(M: float, y: float) -> float:
    return M * M / (M * M + y * y) ** 2.5


def chi(b: float) -> float:
    return E2 / (12.0 * PI**2) * (b - math.log(2.0 * b) - float(digamma(1.0 + 1.0 / (2.0 * b))))


def exact_C(b: float, N: int, K: float, a: float) -> float:
    validate_params(b, N, K, a)
    # Saturated primitives can lose digits when K is tiny compared with |a|.
    # mpmath is a stable fallback for that explicitly tested edge regime.
    if K < 1e-6 * max(1.0, abs(a)) or abs(a) > 1e8:
        with mp.workdps(100):
            bb, kk, aa = mp.mpf(str(b)), mp.mpf(str(K)), mp.mpf(str(a))
            total = mp.mpf("0")
            for n in range(N + 1):
                MM = mp.sqrt(1 + 2 * bb * n)
                def pp(y: mp.mpf) -> mp.mpf:
                    u = y / mp.sqrt(MM * MM + y * y)
                    return (u - u**3 / 3) / (MM * MM)
                total += degeneracy(n) * (pp(kk - aa) + pp(kk + aa))
            return float(bb / (16 * mp.pi**2) * total)
    return b / (16.0 * PI**2) * math.fsum(
        degeneracy(n) * (primitive(mass(b, n), K - a) + primitive(mass(b, n), K + a))
        for n in range(N + 1)
    )


def reference_C(b: float, N: int, K: float, a: float) -> tuple[float, float]:
    validate_params(b, N, K, a)
    value = 0.0
    error = 0.0
    for n in range(N + 1):
        M = mass(b, n)
        q, e = quad(lambda k: density(M, k - a), -K, K, epsabs=2e-13, epsrel=2e-13, limit=200)
        value += degeneracy(n) * q
        error += degeneracy(n) * e
    factor = b / (16.0 * PI**2)
    return factor * value, factor * error


def discrete_C(b: float, N: int, K: float, a: float, nk: int) -> float:
    validate_params(b, N, K, a)
    if isinstance(nk, bool) or not isinstance(nk, int) or nk <= 0:
        raise ValueError("nk must be a positive integer")
    x, w = np.polynomial.legendre.leggauss(nk)
    k = K * x
    wk = K * w
    total = 0.0
    for n in range(N + 1):
        M = mass(b, n)
        total += degeneracy(n) * float(np.dot(wk, M * M / (M * M + (k - a) ** 2) ** 2.5))
    return b / (16.0 * PI**2) * total


def z_from_C(b: float, C: float) -> float:
    return 1.0 + chi(b) - E2 * C


def symbolic_gate() -> dict[str, Any]:
    import sympy as sp  # resolved from bundled round5/deps
    y, M = sp.symbols("y M", positive=True)
    u = y / sp.sqrt(M**2 + y**2)
    P = (u - u**3 / 3) / M**2
    residual = sp.simplify(sp.diff(P, y) - M**2 / (M**2 + y**2) ** sp.Rational(5, 2))
    return {"passed": residual == 0, "residual": str(residual), "scope": "symbolic primitive for M>0"}


def matrix_gate() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    max_scaled = 0.0
    failures = 0
    for b in (0.3, 3.0, 10.0):
        for N in (0, 4, 20):
            for K in (0.1, 2.0, 20.0):
                for a in (0.0, 0.3, K, 2.0 * K, -K):
                    exact = exact_C(b, N, K, a)
                    ref, err = reference_C(b, N, K, a)
                    abs_diff = abs(exact - ref)
                    scale = abs_diff / max(1.0, abs(ref))
                    passed = scale < TOL
                    failures += not passed
                    max_scaled = max(max_scaled, scale)
                    rows.append({"b": b, "N": N, "K": K, "a": a, "exact": exact, "reference": ref, "quad_error": err, "abs_diff": abs_diff, "scaled_diff": scale, "passed": passed})
    return {"count": len(rows), "max_scaled_difference": max_scaled, "failures": failures, "passed": failures == 0, "rows": rows, "tolerance": TOL}


def geometry_gate() -> dict[str, Any]:
    rows = []
    symmetry_max = 0.0
    derivative_max_positive = 0.0
    for b, N, K in ((0.3, 0, 0.1), (3.0, 4, 2.0), (10.0, 4, 20.0)):
        for a in (0.001, 0.3, K, 2 * K, 100 * K):
            cp, cm = exact_C(b, N, K, a), exact_C(b, N, K, -a)
            symmetry_max = max(symmetry_max, abs(cp - cm))
            derivative = b / (16 * PI**2) * math.fsum(
                degeneracy(n) * (density(mass(b, n), K + a) - density(mass(b, n), K - a)) for n in range(N + 1)
            )
            derivative_max_positive = max(derivative_max_positive, derivative)
            rows.append({"b": b, "N": N, "K": K, "a": a, "C": cp, "dC_da": derivative})
    return {"rows": rows, "symmetry_max": symmetry_max, "derivative_max_positive": derivative_max_positive, "passed": symmetry_max < 5e-15 and derivative_max_positive <= 5e-15, "proof_scope": "analytic E2 supplies strict decrease for a>0; samples are a numerical cross-check"}


def refinement_gate() -> dict[str, Any]:
    b, N, K = 10.0, 4, 20.0
    a_values = (0.0, 0.3, 5.0, 20.0, 40.0, -20.0)
    rows = []
    maximum = 0.0
    maximum_highest = 0.0
    for nk in (32, 64, 128, 256, 512):
        for a in a_values:
            exact = exact_C(b, N, K, a)
            value = discrete_C(b, N, K, a, nk)
            error = abs(value - exact)
            maximum = max(maximum, error)
            if nk == 512:
                maximum_highest = max(maximum_highest, error)
            rows.append({"b": b, "N": N, "K": K, "a": a, "nk": nk, "exact": exact, "discrete": value, "abs_error": error})
    return {"rows": rows, "max_abs_error_all_nodes": maximum, "max_abs_error_nk512": maximum_highest, "passed": maximum_highest < 2e-10, "tolerance": 2e-10, "note": "coarse Gauss rules are retained as diagnostics; only the highest-resolution gate is bounded"}


def adversary_gate() -> dict[str, Any]:
    rows = []
    for K in (20.0, 200.0):
        b, N, nk = 10.0, 0, 2
        nodes, _ = np.polynomial.legendre.leggauss(nk)
        a_node = K / math.sqrt(3.0)
        c0, cnode, cmax = discrete_C(b, N, K, 0.0, nk), discrete_C(b, N, K, a_node, nk), exact_C(b, N, K, 0.0)
        rows.append({"b": b, "N": N, "K": K, "nk": nk, "a_node": a_node, "C_disc_a0": c0, "C_disc_at_node": cnode, "C_continuous_max": cmax, "Z_disc_at_node": z_from_C(b, cnode), "Z_continuous_max_point": z_from_C(b, cmax), "nonzero_exceeds_zero": cnode > c0, "exceeds_continuous_max": cnode > cmax, "negative_discrete_Z": z_from_C(b, cnode) < 0})
    return {"rows": rows, "passed": rows[0]["nonzero_exceeds_zero"] and rows[0]["exceeds_continuous_max"] and rows[1]["negative_discrete_Z"], "interpretation": "permitted positive quadrature-grid failure; not a physical instability or QED Landau pole"}


def uniform_tail_gate() -> dict[str, Any]:
    frac = Fraction(100, 137) / Fraction(157, 50) * (1 + 2 * (Fraction(1, 84) + Fraction(1, 246) + Fraction(1, 427) + Fraction(1, 729) + Fraction(1, 90)))
    target = Fraction(67743204500, 274510827927)
    return {"fraction": str(frac), "target": str(target), "exact_equal": frac == target, "less_than_quarter": frac < Fraction(1, 4), "passed": frac == target and frac < Fraction(1, 4), "scope": "all finite N, b=10,K=20, positive constant-exact quadrature"}


def full_window_gate() -> dict[str, Any]:
    rows = []
    maximum = 0.0
    b = 10.0
    for N in (0, 1, 4, 20, 1000):
        direct = b / (12 * PI**2) * math.fsum(degeneracy(n) / (1 + 2 * b * n) for n in range(N + 1))
        z_direct = 1 + chi(b) - E2 * direct
        z_digamma = 1 - E2 / (12 * PI**2) * (math.log(2 * b) + float(digamma(N + 1 + 1 / (2 * b))))
        diff = abs(z_direct - z_digamma)
        maximum = max(maximum, diff)
        rows.append({"b": b, "N": N, "C_direct": direct, "Z_direct": z_direct, "Z_digamma": z_digamma, "abs_diff": diff})
    return {"rows": rows, "max_abs_difference": maximum, "passed": maximum < 2e-13, "tolerance": 2e-13}


def cofinal_gate() -> dict[str, Any]:
    rows = []
    b = 10.0
    for N in (1, 4, 16, 64, 256, 1024):
        K = math.sqrt(1 + 2 * b * N)
        lower = b / (16 * PI**2) * math.fsum(degeneracy(n) * (5 / (12 * math.sqrt(2) * mass(b, n) ** 2)) for n in range(N + 1))
        actual = exact_C(b, N, K, 0.0)
        rows.append({"b": b, "N": N, "K": K, "lower_bound": lower, "C_at_zero": actual, "bound_valid": actual >= lower})
    return {"rows": rows, "passed": all(row["bound_valid"] for row in rows), "scope": "finite examples illustrating the E9 lower bound; not by themselves a divergence proof"}


def tail_rows() -> list[dict[str, Any]]:
    b = 10.0
    out = []
    for log10_n1 in (0.0, 1.0, 4.0, 8.0, 12.0, 20.0, 100.0, 1000.0):
        x = log10_n1 * math.log(10.0)
        if log10_n1 <= 15:
            n1 = 10.0**log10_n1
            psi_value = float(digamma(n1 + 1 + 1 / (2 * b)))
            method, error_note = "scipy.digamma", "direct floating evaluation"
        else:
            n1 = math.inf
            # For x beyond the float exponent range, exp(-x) underflows to
            # zero; keep the logarithm and label the omitted O(N^-1) terms.
            inv = math.exp(-x) if x < 700 else 0.0
            psi_value = x - (0.5 * inv if inv else 0.0) - (inv * inv / 12.0 if inv else 0.0)
            method, error_note = "asymptotic_log_guard", "no integer N allocated; omitted O(N^-4) below float range"
        z = 1 - E2 / (12 * PI**2) * (math.log(2 * b) + psi_value)
        out.append({"log10_N_plus_1": log10_n1, "Z_N_infinity": z, "method": method, "error_note": error_note})
    log_ncrit = 12 * PI**2 / E2 - math.log(2 * b)
    return out + [{"log10_N_critical_asymptotic": log_ncrit, "method": "asymptotic_log_guard", "error_note": "formal logarithm only; no allocation or exact threshold claim"}]


def input_gate() -> dict[str, Any]:
    bad = [(0, 0, 1, 0), (-1, 0, 1, 0), (1, -1, 1, 0), (1, 0.2, 1, 0), (1, 0, 0, 0), (math.nan, 0, 1, 0), (1, 0, math.inf, 0), (1, 0, 1, math.inf)]
    failures = []
    for args in bad:
        try:
            validate_params(*args)
            failures.append({"args": list(args), "accepted": True})
        except ValueError as exc:
            failures.append({"args": [str(x) for x in args], "accepted": False, "error": str(exc)})
    return {"rows": failures, "passed": all(not row["accepted"] for row in failures)}


def cancellation_gate() -> dict[str, Any]:
    """Check the high-|a|/tiny-K fallback against arbitrary precision."""
    rows = []
    for b, N, K, a in ((3.0, 4, 1e-12, 1e8), (10.0, 0, 1e-10, 1e6)):
        bb, kk, aa = mp.mpf(str(b)), mp.mpf(str(K)), mp.mpf(str(a))
        total = mp.mpf("0")
        for n in range(N + 1):
            MM = mp.sqrt(1 + 2 * bb * n)
            q = mp.quad(lambda k: MM**2 / (MM**2 + (k - aa) ** 2) ** mp.mpf("2.5"), [-kk, kk])
            total += degeneracy(n) * q
        reference = float(bb / (16 * mp.pi**2) * total)
        value = exact_C(b, N, K, a)
        error = abs(value - reference)
        relative = error / max(abs(reference), 1e-300)
        rows.append({"b": b, "N": N, "K": K, "a": a, "stable_value": value, "mp_reference": reference, "abs_error": error, "relative_error": relative})
    return {"rows": rows, "passed": all(row["relative_error"] < 1e-12 for row in rows), "tolerance": 1e-12, "method": "mpmath arbitrary-precision direct integral"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_csv(path: Path, rows: Iterable[dict[str, Any]], *, dataset: str, scope: str) -> None:
    rows = list(rows)
    keys = sorted({k for row in rows for k in row})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["dataset", "scope", *keys])
        writer.writeheader()
        for row in rows:
            writer.writerow({"dataset": dataset, "scope": scope, **row})


def run() -> dict[str, Any]:
    plot_dir = ROOT / "plot_data"
    plot_dir.mkdir(exist_ok=True)
    symbolic = symbolic_gate()
    matrix = matrix_gate()
    geometry = geometry_gate()
    refinement = refinement_gate()
    adversary = adversary_gate()
    uniform_tail = uniform_tail_gate()
    full_window = full_window_gate()
    cofinal = cofinal_gate()
    inputs = input_gate()
    cancellation = cancellation_gate()
    tails = tail_rows()
    write_csv(plot_dir / "finite_geometry.csv", geometry["rows"], dataset="exact_continuous_geometry", scope="finite b,N,K; a in displayed sample")
    write_csv(plot_dir / "quadrature_refinement.csv", refinement["rows"], dataset="finite_gauss_vs_exact", scope="b=10,N=4,K=20; finite Gauss rules")
    write_csv(plot_dir / "tail_behavior.csv", tails, dataset="full_window_tail", scope="fixed b=10; exact small N and labeled asymptotic log guard")
    files = [ROOT / "advisor_experiment_contract.md", ROOT / "../round4/response_contract.md", ROOT / "../round5/search_contract.md", ROOT / "../round5/theorem_advisor.md"]
    repo_root = ROOT.parent.parent.resolve()
    hashes = {str(path.resolve().relative_to(repo_root)): sha256(path) for path in files if path.exists()}
    hashes["qeg-research/round6/experiments.py"] = sha256(ROOT / "experiments.py")
    for csv_path in sorted(plot_dir.glob("*.csv")):
        hashes[str(csv_path.resolve().relative_to(repo_root))] = sha256(csv_path)
    out = {
        "contract": "round6/advisor_experiment_contract.md",
        "scope": "finite continuous momentum window, finite Landau cutoff, fixed matching; no ODE trajectory",
        "constants": {"alpha": ALPHA, "e2": E2},
        "gates": {"symbolic_primitive": symbolic, "integral_reference": matrix, "continuous_geometry": geometry, "quadrature_refinement": refinement, "discrete_adversary": adversary, "uniform_tail_certificate": uniform_tail, "full_window_sum": full_window, "cofinal_example": cofinal, "input_validation": inputs, "cancellation_stability": cancellation},
        "tail_behavior": tails,
        "failed_hypotheses_retained": {"discrete_maximum_at_zero": {"passed": False, "evidence": adversary["rows"]}, "continuum_uniform_positive_bound": {"passed": False, "interpretation": "formal fixed-matching obstruction; not a physical instability or QED Landau pole"}},
        "hashes": hashes,
        "all_conventional_gates_pass": all(g.get("passed", False) for g in (symbolic, matrix, geometry, refinement, adversary, uniform_tail, full_window, cofinal, inputs, cancellation)),
    }
    (ROOT / "experiment_results.json").write_text(json.dumps(out, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    result = run()
    print(json.dumps({"all_conventional_gates_pass": result["all_conventional_gates_pass"], "adversary": result["gates"]["discrete_adversary"], "hashes": result["hashes"]}, indent=2))
