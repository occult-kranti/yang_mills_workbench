#!/usr/bin/env python3
"""Finite-grid gauge--scalar bridge used for the round-7 audit.

This is an explicitly finite variational model.  The scalar is a new classical
degree of freedom; this file does not claim to derive a continuum QED stress
tensor or a gravitational closure.  The implementation keeps the old finite
mode sums and adds the gauge-kinetic function ``f(phi)=1+g**2*phi**2``.

Running the module writes the bounded JSON/CSV/readme artifacts in this
directory.  All acceptance gates are explicit exceptions rather than disabled
assertions, and every state used by an energy check is evolved as an ODE state
or reconstructed without clipping.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import platform
import numbers
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import digamma

HERE = Path(__file__).resolve().parent
E2 = 4.0 * math.pi / 137.035999084
ALPHA = 1.0 / 137.035999084


class FiniteScalarFailure(RuntimeError):
    """A numerical or contract failure that must be reported to the caller."""


@dataclass(frozen=True)
class Params:
    a0: float = 0.0
    target_E: float = 0.15
    b: float = 10.0
    Tpump: float = 4.0
    tfinal: float = 6.0
    ncut: int = 1
    Kmax: float = 20.0
    nK: int = 128
    g: float = 0.10
    nu: float = 0.50
    phi0: float = 0.40
    y0: float = 0.10
    chi_b: float | None = None
    rtol: float = 2.0e-10
    atol: float = 2.0e-12
    max_step: float = 0.05
    sample_count: int = 121
    z_floor: float = 1.0e-8
    probe_start: float = 4.5
    probe_duration: float = 1.0


def _finite(value: Any) -> bool:
    try:
        return isinstance(value, numbers.Real) and not isinstance(value, (bool, np.bool_)) and math.isfinite(float(value))
    except (TypeError, ValueError, OverflowError):
        return False


def validate_params(p: Params) -> None:
    if not isinstance(p, Params):
        raise FiniteScalarFailure("parameters must be a Params instance")
    for name in ("a0", "target_E", "b", "Tpump", "tfinal", "Kmax", "g", "nu",
                 "phi0", "y0", "rtol", "atol", "max_step", "z_floor",
                 "probe_start", "probe_duration"):
        if not _finite(getattr(p, name)):
            raise FiniteScalarFailure(f"{name} must be finite")
    if p.b <= 0 or p.Kmax <= 0 or p.nu < 0:
        raise FiniteScalarFailure("b and Kmax must be positive; nu must be nonnegative")
    if p.g < 0:
        raise FiniteScalarFailure("g must be nonnegative")
    if p.Tpump <= 0 or p.tfinal <= p.Tpump:
        raise FiniteScalarFailure("require tfinal > Tpump > 0")
    if p.probe_start < 0 or p.probe_duration <= 0 or p.probe_start + p.probe_duration > p.tfinal:
        raise FiniteScalarFailure("probe interval must lie inside [0,tfinal]")
    if p.rtol <= 0 or p.atol <= 0 or p.max_step <= 0 or p.z_floor <= 0:
        raise FiniteScalarFailure("integration tolerances and z_floor must be positive")
    if isinstance(p.ncut, bool) or not isinstance(p.ncut, int) or p.ncut < 0:
        raise FiniteScalarFailure("ncut must be an integer >= 0")
    if isinstance(p.nK, bool) or not isinstance(p.nK, int) or p.nK < 2:
        raise FiniteScalarFailure("nK must be an integer >= 2")
    if isinstance(p.sample_count, bool) or not isinstance(p.sample_count, int) or p.sample_count < 3:
        raise FiniteScalarFailure("sample_count must be an integer >= 3")
    if p.chi_b is not None and not _finite(p.chi_b):
        raise FiniteScalarFailure("chi_b must be finite when supplied")


def chi_match(b: float) -> float:
    if not _finite(b) or b <= 0:
        raise FiniteScalarFailure("invalid b for susceptibility")
    return float(E2 / (12.0 * math.pi**2) *
                 (b - math.log(2.0 * b) - float(digamma(1.0 + 1.0 / (2.0 * b)))))


class Grid:
    """Bounded inclusive Landau-level/longitudinal Gauss grid."""

    def __init__(self, p: Params, *, canonical_shift: float = 0.0):
        validate_params(p)
        if not _finite(canonical_shift):
            raise FiniteScalarFailure("canonical_shift must be finite")
        nodes, weights = np.polynomial.legendre.leggauss(p.nK)
        local = p.Kmax * nodes
        wk = p.Kmax * weights
        ns = np.arange(p.ncut + 1, dtype=int)
        degeneracy = np.where(ns == 0, 1.0, 2.0)
        self.K = np.tile(p.a0 + canonical_shift + local, ns.size)
        self.M = np.repeat(np.sqrt(1.0 + 2.0 * p.b * ns), p.nK)
        self.weights = np.repeat(p.b * degeneracy / (4.0 * math.pi**2), p.nK) * np.tile(wk, ns.size)
        self.n = np.repeat(ns, p.nK)
        self.size = int(self.K.size)
        if not (np.all(np.isfinite(self.K)) and np.all(np.isfinite(self.M)) and
                np.all(np.isfinite(self.weights)) and np.all(self.M > 0) and
                np.all(self.weights > 0)):
            raise FiniteScalarFailure("generated grid has invalid coefficients")


def bump_integral() -> float:
    # A fixed, positive normalizer; scipy's adaptive result is deterministic at
    # the precision used by the archived round-6 pump.
    from scipy.integrate import quad
    value, _ = quad(lambda u: math.exp(-1.0 / (u * (1.0 - u))), 0.0, 1.0,
                    epsabs=2e-14, epsrel=2e-14, points=(0.5,), limit=200)
    if not _finite(value) or value <= 0:
        raise FiniteScalarFailure("invalid pump normalizer")
    return float(value)


def pulse(s: float, width: float, norm: float) -> float:
    u = s / width
    if u <= 0.0 or u >= 1.0:
        return 0.0
    return math.exp(-1.0 / (u * (1.0 - u))) / (width * norm)


def _initial_state(grid: Grid, p: Params) -> np.ndarray:
    pz = grid.K - p.a0
    om = np.sqrt(grid.M * grid.M + pz * pz)
    r = np.empty((3, grid.size), dtype=float)
    r[0] = -grid.M / om
    r[1] = 0.0
    r[2] = -pz / om
    # [a, x, r(3*n), phi, y, pump work, omitted-exchange work]
    return np.concatenate(([p.a0, 0.0], r.reshape(-1), [p.phi0, p.y0, 0.0, 0.0]))


def _terms(a: float, state: np.ndarray, grid: Grid):
    pz = grid.K - a
    om = np.sqrt(grid.M * grid.M + pz * pz)
    r = state[2:2 + 3 * grid.size].reshape(3, grid.size)
    hdotr = grid.M * r[0] + pz * r[2]
    S = float(np.sum(grid.weights * (r[2] + pz / om)))
    C = float(np.sum(grid.weights * grid.M**2 / (4.0 * om**5)))
    D = float(np.sum(grid.weights * (5.0 * grid.M**2 * pz / (8.0 * om**7))))
    return pz, om, r, hdotr, S, C, D


def _solve(p: Params, *, wrong: bool = False, mode: str = "source_amplitude",
           probe_amp: float = 0.0) -> dict[str, Any]:
    validate_params(p)
    if not isinstance(wrong, bool):
        raise FiniteScalarFailure("wrong must be a bool")
    if not isinstance(mode, str) or mode not in {"source_amplitude", "delayed_probe"}:
        raise FiniteScalarFailure("mode must be source_amplitude or delayed_probe")
    if not _finite(probe_amp):
        raise FiniteScalarFailure("probe_amp must be finite")
    if mode == "source_amplitude" and probe_amp != 0:
        raise FiniteScalarFailure("probe_amp is only used in delayed_probe mode")
    grid = Grid(p)
    norm = bump_integral()
    chi_b = chi_match(p.b) if p.chi_b is None else float(p.chi_b)
    if not _finite(chi_b):
        raise FiniteScalarFailure("chi_b is nonfinite")
    y0 = _initial_state(grid, p)
    n = grid.size
    i_phi = 2 + 3 * n
    i_y = i_phi + 1
    i_wp = i_phi + 2
    i_wd = i_phi + 3
    ts = np.linspace(0.0, p.tfinal, p.sample_count)

    def drive(t: float) -> float:
        value = p.target_E * pulse(t, p.Tpump, norm)
        if mode == "delayed_probe":
            value += probe_amp * pulse(t - p.probe_start, p.probe_duration, norm)
        return value

    def rhs(t: float, state: np.ndarray) -> np.ndarray:
        a, x = float(state[0]), float(state[1])
        phi, y = float(state[i_phi]), float(state[i_y])
        pz, om, r, _, S, C, D = _terms(a, state, grid)
        f = 1.0 + p.g * p.g * phi * phi
        f_phi = 2.0 * p.g * p.g * phi
        Z = f + chi_b - E2 * C
        if not _finite(Z) or Z <= p.z_floor:
            raise FiniteScalarFailure(f"Z became nonpositive/tiny at t={t}: {Z}")
        F = drive(t)
        # Deliberately wrong control removes only Maxwell's scalar exchange;
        # it retains the scalar magnetic force in y'.
        exchange = 0.0 if wrong else f_phi * y * x
        xp = (F - E2 * (S + D * x * x) - exchange) / Z
        out = np.zeros_like(state)
        out[0], out[1] = -x, xp
        dr = out[2:2 + 3 * n].reshape(3, n)
        dr[0] = -2.0 * pz * r[1]
        dr[1] = 2.0 * (pz * r[0] - grid.M * r[2])
        dr[2] = 2.0 * grid.M * r[1]
        out[i_phi] = y
        out[i_y] = -p.nu * p.nu * phi + 0.5 * f_phi * (x * x - p.b * p.b)
        out[i_wp] = x * F
        out[i_wd] = f_phi * y * x * x if wrong else 0.0
        return out

    try:
        sol = solve_ivp(rhs, (0.0, p.tfinal), y0, method="DOP853", t_eval=ts,
                        rtol=p.rtol, atol=p.atol, max_step=p.max_step)
    except FiniteScalarFailure:
        raise
    except Exception as exc:
        raise FiniteScalarFailure(f"integrator failed: {type(exc).__name__}: {exc}") from exc
    if not sol.success or sol.y.shape != (y0.size, ts.size) or not np.all(np.isfinite(sol.y)):
        raise FiniteScalarFailure(f"integrator returned incomplete/nonfinite state: {sol.message}")

    m: dict[str, np.ndarray] = {k: np.empty(ts.size, dtype=float) for k in (
        "t", "a", "x", "F", "phi", "y", "f", "f_phi", "S", "C", "D", "Z",
        "Wtilde", "Wpump", "Wdefect", "energy_mismatch", "defect_residual", "max_r2_error")}
    omega0 = None
    for j, t in enumerate(ts):
        state = sol.y[:, j]
        a, x = float(state[0]), float(state[1])
        phi, y = float(state[i_phi]), float(state[i_y])
        pz, om, r, hdotr, S, C, D = _terms(a, state, grid)
        f = 1.0 + p.g * p.g * phi * phi
        f_phi = 2.0 * p.g * p.g * phi
        Z = f + chi_b - E2 * C
        w = 0.5 * Z * x * x + E2 * float(np.sum(grid.weights * (hdotr + om)))
        w += 0.5 * y * y + 0.5 * (p.nu * p.nu + p.g * p.g * p.b * p.b) * phi * phi
        m["t"][j], m["a"][j], m["x"][j], m["F"][j] = t, a, x, drive(float(t))
        m["phi"][j], m["y"][j], m["f"][j], m["f_phi"][j] = phi, y, f, f_phi
        m["S"][j], m["C"][j], m["D"][j], m["Z"][j] = S, C, D, Z
        m["Wtilde"][j], m["Wpump"][j], m["Wdefect"][j] = w, state[i_wp], state[i_wd]
        m["max_r2_error"][j] = float(np.max(np.abs(np.sum(r * r, axis=0) - 1.0)))
        if omega0 is None:
            omega0 = w
    m["energy_mismatch"] = m["Wtilde"] - m["Wtilde"][0] - m["Wpump"]
    m["defect_residual"] = m["energy_mismatch"] - m["Wdefect"]
    diag = {
        "wrong_model": wrong, "mode": mode, "probe_amp": probe_amp,
        "nmode": n, "min_Z": float(np.min(m["Z"])),
        "max_raw_r2_error": float(np.max(m["max_r2_error"])),
        "max_energy_mismatch": float(np.max(np.abs(m["energy_mismatch"]))),
        "max_defect_integral_residual": float(np.max(np.abs(m["defect_residual"]))),
        "final_a": float(m["a"][-1]), "final_x": float(m["x"][-1]),
        "final_phi": float(m["phi"][-1]), "final_y": float(m["y"][-1]),
        "nfev": int(sol.nfev), "samples": int(ts.size),
    }
    return {"parameters": asdict(p), "wrong_model": wrong, "mode": mode,
            "probe_amp": probe_amp, "constants": {"alpha": ALPHA, "e2": E2, "chi_b": chi_b,
                                                      "pump_normalizer": norm},
            "grid": {"nmode": n, "ncut": p.ncut, "nK": p.nK,
                     "Kmin": float(np.min(grid.K)), "Kmax": float(np.max(grid.K)),
                     "weight_sum": float(np.sum(grid.weights))},
            "macro": {k: v.tolist() for k, v in m.items()}, "diagnostics": diag}


def _max_difference(left: dict[str, Any], right: dict[str, Any], field: str) -> float:
    a = np.asarray(left["macro"][field], dtype=float)
    b = np.asarray(right["macro"][field], dtype=float)
    return float(np.max(np.abs(a - b)))


def _load_old_response():
    path = HERE.parent / "round6" / "code" / "response.py"
    if not path.exists():
        return None, path
    spec = importlib.util.spec_from_file_location("round6_response_for_round7", path)
    if spec is None or spec.loader is None:
        return None, path
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(spec.name, None)
        raise FiniteScalarFailure(f"baseline import failed: {exc}") from exc
    return module, path


def g0_baseline_compare(p: Params) -> dict[str, Any]:
    """Compare the actual old solver on exactly matched g=0 parameters."""
    old, path = _load_old_response()
    if old is None:
        return {"status": "unavailable", "reason": "round6 response could not be imported", "path": str(path)}
    scalar_p = Params(**{**asdict(p), "g": 0.0, "phi0": 0.4, "y0": 0.1})
    ours = _solve(scalar_p)
    old_fields = {k: v for k, v in asdict(scalar_p).items()
                  if k in {"a0", "target_E", "b", "Tpump", "tfinal", "ncut", "Kmax", "nK",
                           "rtol", "atol", "max_step", "sample_count", "z_floor"}}
    old_p = old.Params(**old_fields)
    old_run = old._solve(old_p, mode="source_amplitude")
    da = float(np.max(np.abs(np.asarray(ours["macro"]["a"]) - np.asarray(old_run["macro"]["a"]))))
    dx = float(np.max(np.abs(np.asarray(ours["macro"]["x"]) - np.asarray(old_run["macro"]["x"]))))
    passed = da < 3e-9 and dx < 3e-9
    return {"status": "compared", "passed": passed, "max_abs_a": da, "max_abs_x": dx,
            "threshold": 3e-9, "old_source": str(path)}


def zero_drive_gate(p: Params) -> dict[str, Any]:
    """Check the exact vacuum/mode solution with F=0 and x=0."""
    q = Params(**{**asdict(p), "target_E": 0.0, "probe_start": p.probe_start,
                  "probe_duration": p.probe_duration})
    run = _solve(q)
    t = np.asarray(run["macro"]["t"])
    om = math.sqrt(q.nu * q.nu + q.g * q.g * q.b * q.b)
    expected = (q.phi0 + q.y0*t if om == 0 else
                q.phi0 * np.cos(om * t) + q.y0 / om * np.sin(om * t))
    phi_err = float(np.max(np.abs(np.asarray(run["macro"]["phi"]) - expected)))
    x_max = float(np.max(np.abs(np.asarray(run["macro"]["x"]))))
    a_drift = float(np.max(np.abs(np.asarray(run["macro"]["a"]) - q.a0)))
    energy = float(np.max(np.abs(np.asarray(run["macro"]["Wtilde"]) - run["macro"]["Wtilde"][0])))
    passed = max(phi_err, x_max, a_drift, energy) < 2e-8
    return {"passed": passed, "threshold": 2e-8, "Omega": om, "max_phi_error": phi_err,
            "max_x": x_max, "max_a_drift": a_drift, "max_energy_drift": energy}


def finite_difference_gate(p: Params) -> dict[str, Any]:
    """Refine a centered finite-difference response and check pre-source causality.

    This checks resolution across perturbation sizes, not a tangent-equation or
    continuum response theorem. Values are evaluated at the same output times.
    """
    base_amp = 0.15
    derivatives = []
    for eps in (2e-4, 1e-4, 5e-5):
        plus = _solve(p, mode="delayed_probe", probe_amp=base_amp+eps)
        minus = _solve(p, mode="delayed_probe", probe_amp=base_amp-eps)
        derivatives.append((np.asarray(plus["macro"]["x"])-np.asarray(minus["macro"]["x"]))/ (2*eps))
    times = np.asarray(plus["macro"]["t"])
    pre = times <= p.probe_start
    causal = max(float(np.max(np.abs(d[pre]))) for d in derivatives)
    errors = [float(np.max(np.abs(derivatives[i]-derivatives[i+1]))) for i in range(2)]
    resolved = float(np.max(np.abs(derivatives[-1])))
    return {"mode":"delayed_probe", "epsilons":[2e-4,1e-4,5e-5],
            "probe_amp":base_amp, "max_fd_x":resolved,
            "successive_derivative_differences":errors,
            "pre_probe_max_abs_derivative":causal,
            "derivative_difference_threshold":2e-5, "causality_threshold":2e-6,
            "passed":_finite(resolved) and resolved>1e-6 and max(errors)<2e-5 and causal<2e-6}


def write_csv(result: dict[str, Any], path: str | Path, *, scenario: str) -> None:
    path = Path(path)
    macro = result["macro"]
    keys = ["scenario", "t", "a", "x", "F", "phi", "y", "f", "f_phi", "S", "C", "D", "Z",
            "Wtilde", "Wpump", "Wdefect", "energy_mismatch", "defect_residual", "max_r2_error"]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        for i in range(len(macro["t"])):
            writer.writerow({"scenario": scenario, **{k: macro[k][i] for k in keys if k != "scenario"}})


def _write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise FiniteScalarFailure(f"cannot write empty CSV: {path}")
    keys = sorted({k for row in rows for k in row})
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_hashes() -> dict[str, str | None]:
    paths = {"finite_scalar": Path(__file__),
             "round6_response": HERE.parent / "round6" / "code" / "response.py",
             "round4_response_contract": HERE.parent / "round4" / "response_contract.md",
             "round7_variable_contract": HERE / "variable_contract.md"}
    out: dict[str, str | None] = {}
    for name, path in paths.items():
        out[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    return out


def main() -> int:
    p = Params()
    validate_params(p)
    out_dir = HERE
    # Main correct run, wrong control, and one delayed-source holdout.
    correct = _solve(p)
    wrong = _solve(p, wrong=True)
    delayed = _solve(p, mode="delayed_probe", probe_amp=0.15)
    for name, run in (("correct", correct), ("wrong", wrong), ("delayed", delayed)):
        write_csv(run, out_dir / f"finite_{name}.csv", scenario=name)

    zero = zero_drive_gate(p)
    baseline = g0_baseline_compare(p)
    fd = finite_difference_gate(p)
    # Keep cutoff fixed while changing only node resolution.  This is separate
    # from the fixed-cutoff matrix and is intentionally small (64/128/256).
    refinement_rows: list[dict[str, Any]] = []
    refinement_runs: dict[int, dict[str, Any]] = {}
    for nk in (64, 128, 256):
        q = Params(**{**asdict(p), "nK": nk})
        run = _solve(q)
        refinement_runs[nk] = run
        refinement_rows.append({"nK": nk, "nmode": run["grid"]["nmode"],
                                "final_a": run["diagnostics"]["final_a"],
                                "final_x": run["diagnostics"]["final_x"],
                                "max_energy_mismatch": run["diagnostics"]["max_energy_mismatch"],
                                "max_r2_error": run["diagnostics"]["max_raw_r2_error"]})
    _write_rows(out_dir / "finite_refinement.csv", refinement_rows)
    refinement_diff = max(_max_difference(refinement_runs[128], refinement_runs[256], "a"),
                          _max_difference(refinement_runs[128], refinement_runs[256], "x"))

    matrix_rows: list[dict[str, Any]] = []
    for g in (0.05, 0.10):
        for nk in (64, 128):
            q = Params(**{**asdict(p), "g": g, "nK": nk})
            run = _solve(q)
            matrix_rows.append({"g": g, "nu": q.nu, "phi0": q.phi0, "y0": q.y0, "b": q.b,
                                "ncut": q.ncut, "Kmax": q.Kmax, "nK": nk,
                                "final_a": run["diagnostics"]["final_a"], "final_x": run["diagnostics"]["final_x"],
                                "final_phi": run["diagnostics"]["final_phi"],
                                "min_Z": run["diagnostics"]["min_Z"],
                                "max_energy_mismatch": run["diagnostics"]["max_energy_mismatch"],
                                "max_defect_integral_residual": run["diagnostics"]["max_defect_integral_residual"]})
    _write_rows(out_dir / "finite_matrix.csv", matrix_rows)

    thresholds = {"min_Z_margin": p.z_floor, "raw_norm_max": 5e-8,
                  "correct_energy_residual_max": 5e-7,
                  "wrong_defect_residual_max": 5e-7,
                  "node_refinement_max_abs_ax": 2e-5,
                  "g0_baseline_max_abs_ax": 3e-9}
    failures: list[str] = []
    if correct["diagnostics"]["min_Z"] <= thresholds["min_Z_margin"]:
        failures.append("correct Z floor")
    if correct["diagnostics"]["max_raw_r2_error"] > thresholds["raw_norm_max"]:
        failures.append("correct raw Bloch norm")
    if correct["diagnostics"]["max_energy_mismatch"] > thresholds["correct_energy_residual_max"]:
        failures.append("correct energy identity")
    if wrong["diagnostics"]["max_defect_integral_residual"] > thresholds["wrong_defect_residual_max"]:
        failures.append("wrong-control defect integral")
    observed_defect = float(np.max(np.abs(np.asarray(wrong["macro"]["energy_mismatch"]))))
    if observed_defect <= 1e-10:
        failures.append("wrong-control defect was not resolved")
    if refinement_diff > thresholds["node_refinement_max_abs_ax"]:
        failures.append("node refinement")
    if zero["passed"] is not True:
        failures.append("zero-drive harmonic gate")
    if baseline.get("status") != "compared" or baseline.get("passed") is not True:
        failures.append("g=0 round6 baseline")
    if fd.get("passed") is not True:
        failures.append("delayed-source finite difference")
    if source_hashes()["round6_response"] is None or source_hashes()["round4_response_contract"] is None:
        failures.append("frozen reference missing")

    result = {
        "status": "passed" if not failures else "failed",
        "scope": "Finite variational gauge-scalar bridge; no continuum QED or gravitational closure",
        "parameters": asdict(p),
        "constants": {"alpha": ALPHA, "e2": E2, "chi_b": correct["constants"]["chi_b"]},
        "thresholds": thresholds, "failures": failures,
        "source_hashes": source_hashes(),
        "versions": {"python": platform.python_version(), "numpy": np.__version__},
        "gates": {"correct": correct["diagnostics"], "wrong": wrong["diagnostics"],
                  "delayed": delayed["diagnostics"], "zero_drive": zero,
                  "g0_baseline": baseline, "delayed_finite_difference": fd,
                  "node_refinement_max_abs_ax": refinement_diff},
        "csv": ["finite_correct.csv", "finite_wrong.csv", "finite_delayed.csv",
                "finite_refinement.csv", "finite_matrix.csv"],
        "limitations": [
            "The scalar is a declared classical EFT hypothesis with finite mode sums.",
            "The result does not derive a continuum renormalized Einstein-QED current or stress.",
            "Node refinement is held at fixed b, ncut and Kmax and is not a regulator-removal proof.",
            "Wrong-control mismatch is a diagnostic for the omitted Maxwell exchange term.",
        ],
    }
    (out_dir / "finite_results.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    readme = f"""# Round-7 finite scalar bridge

This run evaluates the finite variational model with inclusive Landau levels,
an independent Gauss grid, and `f(phi)=1+g^2 phi^2`.  It uses
`p=k-a`, `h=(M,0,p)`, `S=sum(w*(rz+p/omega))`,
`C=sum(w*M^2/(4*omega^5))`, and `D=sum(w*5*M^2*p/(8*omega^7))`.
The scalar equations are `phi'=y` and
`y'=-nu^2 phi + f_phi*(x^2-b^2)/2`; the potential equation includes
`-f_phi*y*x` in `Z*x'`.  The shifted energy is
`Wtilde=Z*x^2/2+e2*sum(w*(h.r+omega))+y^2/2+
(nu^2+g^2*b^2)*phi^2/2`, and its expected work is `x*F`.

The wrong-control CSV removes only `-f_phi*y*x` from the potential equation.
Its expected defect is `f_phi*y*x^2`, integrated in an independent state and
compared with the observed energy mismatch.  Bloch norms are raw values; no
clipping or projection is applied.  The zero-drive gate checks the harmonic
solution with `Omega^2=nu^2+g^2*b^2`, and the g=0 gate compares the actual
archived round-6 solver with a required successful import and comparison.

Acceptance thresholds and failures are recorded in `finite_results.json`.
Current status: **{result['status']}**.  The scalar data are nondegenerate
(`phi0={p.phi0}`, `y0={p.y0}`); the model is not a derived continuum-QED or
gravitational closure.
"""
    (out_dir / "finite_readme.md").write_text(readme)
    if failures:
        raise FiniteScalarFailure("round-7 finite scalar gates failed: " + ", ".join(failures))
    print(json.dumps({"status": result["status"], "failures": failures,
                      "correct_energy": correct["diagnostics"]["max_energy_mismatch"],
                      "wrong_defect": wrong["diagnostics"]["max_defect_integral_residual"],
                      "node_refinement": refinement_diff}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FiniteScalarFailure as exc:
        print(f"finite_scalar failure: {exc}", file=sys.stderr)
        raise
