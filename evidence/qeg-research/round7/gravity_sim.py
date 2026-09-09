#!/usr/bin/env python3
"""Bounded classical scalar--Einstein--Maxwell Bianchi-I benchmark.

This is a finite, classical new-sector benchmark.  It is not a computation of
Einstein--QED stress tensors, a Dirac calculation, or a cutoff-removal claim.
The independent flux-form system is integrated separately from the full
E,B-form system and is compared pointwise.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import numbers
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import numpy as np
from scipy import __version__ as SCIPY_VERSION
from scipy.integrate import solve_ivp

try:
    import numpy as _np_for_version
except ImportError:  # pragma: no cover - numpy is a declared dependency
    _np_for_version = None

HERE = Path(__file__).resolve().parent
OUTPUT_JSON = HERE / "gravity_results.json"

STATE_NAMES = ("lA", "lC", "phi", "v", "hp", "hl", "E", "B")
REDUCED_NAMES = ("lA", "lC", "phi", "v", "hp", "hl")
WRONG_EXTRA = "I_wrong"


@dataclass(frozen=True)
class Case:
    name: str
    mhat: float
    c: float
    lam: float
    phi0: float
    v0: float
    E0: float
    B0: float
    t_end: float
    samples: int = 161
    branch: int = 1
    description: str = ""

    def parameters(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class InitialState:
    y0: np.ndarray
    rho0: float
    hp0: float
    hl0: float
    electric_flux0: float
    magnetic_flux0: float


class InputError(ValueError):
    """Raised for malformed, non-finite, or unsafe benchmark inputs."""


def _finite(name: str, value: float) -> float:
    if not isinstance(value, numbers.Real) or isinstance(value, (bool, np.bool_)):
        raise InputError(f"{name} must be a real number")
    x = float(value)
    if not math.isfinite(x):
        raise InputError(f"{name} must be finite, got {value!r}")
    return x


def _safe_exp(x: float, *, name: str = "exponent") -> float:
    x = _finite(name, x)
    # np.exp(709) is finite on common IEEE platforms, but leaving no margin
    # makes a parameter typo turn into an inf silently during an ODE call.
    if x > 700.0 or x < -745.0:
        raise FloatingPointError(f"{name}={x} is outside safe exponential range")
    value = math.exp(x)
    if not math.isfinite(value):
        raise FloatingPointError(f"non-finite exp({name})")
    return value


def validate_times(times: Sequence[float] | np.ndarray) -> np.ndarray:
    """Validate a strictly increasing finite output-time grid."""
    try:
        arr = np.asarray(times, dtype=float)
    except (TypeError, ValueError) as exc:
        raise InputError("times must be a one-dimensional numeric sequence") from exc
    if arr.ndim != 1 or arr.size < 2:
        raise InputError("times must be one-dimensional with at least two values")
    if not np.isfinite(arr).all():
        raise InputError("times must contain only finite values")
    if not np.all(np.diff(arr) > 0.0):
        raise InputError("times must be strictly increasing")
    if arr[0] < 0.0:
        raise InputError("times must start at non-negative dimensionless time")
    return arr


def validate_case(case: Case) -> None:
    for key, value in asdict(case).items():
        if key in {"name", "description"}:
            if not isinstance(value, str) or (key == "name" and not value):
                raise InputError(f"{key} must be a non-empty string")
        elif key == "samples":
            if isinstance(value, bool) or not isinstance(value, int) or value < 2 or value > 20001:
                raise InputError("samples must be an integer in [2, 20001]")
        elif key == "branch":
            if isinstance(value, bool) or not isinstance(value, int) or value not in (-1, 1):
                raise InputError("branch must be +1 or -1")
        else:
            _finite(key, value)
    if case.mhat < 0.0:
        raise InputError("mhat must be non-negative")
    if case.t_end <= 0.0:
        raise InputError("t_end must be positive")
    # Keep the benchmark intentionally bounded; this also catches accidental
    # production-sized runs that could hide a singularity in a review artifact.
    if case.t_end > 100.0:
        raise InputError("t_end exceeds bounded benchmark limit 100")


def make_initial_state(case: Case) -> InitialState:
    validate_case(case)
    f0 = _safe_exp(2.0 * case.c * case.phi0, name="2*c*phi0")
    potential0 = 0.5 * case.mhat**2 * case.phi0**2
    scalar_kinetic0 = 0.5 * case.v0**2
    rho_em0 = 0.5 * f0 * (case.E0**2 + case.B0**2)
    rho0 = scalar_kinetic0 + potential0 + rho_em0
    radicand = (rho0 + case.lam) / 3.0
    if not math.isfinite(radicand):
        raise InputError("nonfinite initial Friedmann radicand")
    if radicand < 0:
        raise InputError(
            f"initial Friedmann radicand is negative ({radicand:.17g}) for {case.name}"
        )
    h0 = case.branch * math.sqrt(radicand)
    # Initial isotropy is explicit.  Negative branch is admitted only as the
    # bounded early-contraction case; the default branch is the prescribed root.
    y0 = np.array([0.0, 0.0, case.phi0, case.v0, h0, h0, case.E0, case.B0], dtype=float)
    if not np.isfinite(y0).all():
        raise InputError(f"non-finite initial state for {case.name}")
    return InitialState(
        y0=y0,
        rho0=rho0,
        hp0=h0,
        hl0=h0,
        electric_flux0=f0 * case.E0,
        magnetic_flux0=case.B0,
    )


def _components(case: Case, y: np.ndarray) -> dict[str, float]:
    la, lc, phi, v, hp, hl, E, B = map(float, y[:8])
    f = _safe_exp(2.0 * case.c * phi, name="2*c*phi")
    rho_em = 0.5 * f * (E * E + B * B)
    kinetic = 0.5 * v * v
    potential = 0.5 * case.mhat**2 * phi * phi
    rho = kinetic + potential + rho_em
    pperp = kinetic - potential + rho_em
    ppar = kinetic - potential - rho_em
    return {
        "lA": la,
        "lC": lc,
        "phi": phi,
        "v": v,
        "hp": hp,
        "hl": hl,
        "E": E,
        "B": B,
        "f": f,
        "rhoEM": rho_em,
        "rho": rho,
        "pperp": pperp,
        "ppar": ppar,
        "theta": 2.0 * hp + hl,
        "U": potential,
    }


def full_rhs(case: Case, t: float, y: np.ndarray, *, wrong_force: bool = False) -> np.ndarray:
    del t
    if np.asarray(y).shape[0] < 8 or not np.isfinite(y[:8]).all():
        raise FloatingPointError("full RHS received non-finite or malformed state")
    z = _components(case, y)
    theta = z["theta"]
    scalar_force = case.c * z["f"] * (z["B"] ** 2 - z["E"] ** 2)
    vd = -theta * z["v"] - case.mhat**2 * z["phi"]
    if not wrong_force:
        vd -= scalar_force
    hpd = (case.lam - z["ppar"] - 3.0 * z["hp"] ** 2) / 2.0
    hld = (
        case.lam
        - z["pperp"]
        - hpd
        - z["hp"] ** 2
        - z["hl"] ** 2
        - z["hp"] * z["hl"]
    )
    out = np.array(
        [
            z["hp"],
            z["hl"],
            z["v"],
            vd,
            hpd,
            hld,
            -(2.0 * z["hp"] + 2.0 * case.c * z["v"]) * z["E"],
            -2.0 * z["hp"] * z["B"],
        ],
        dtype=float,
    )
    if not np.isfinite(out).all():
        raise FloatingPointError("full RHS generated non-finite derivative")
    return out


def reduced_to_full(case: Case, initial: InitialState, y: np.ndarray) -> np.ndarray:
    """Recover E,B from conserved electric displacement and magnetic flux."""
    if np.asarray(y).shape[0] < 6 or not np.isfinite(y[:6]).all():
        raise FloatingPointError("reduced state is malformed or non-finite")
    la, lc, phi, v, hp, hl = map(float, y[:6])
    f = _safe_exp(2.0 * case.c * phi, name="2*c*phi")
    area_inv = _safe_exp(-2.0 * la, name="-2*lA")
    E = initial.electric_flux0 * area_inv / f
    B = initial.magnetic_flux0 * area_inv
    full = np.array([la, lc, phi, v, hp, hl, E, B], dtype=float)
    if not np.isfinite(full).all():
        raise FloatingPointError("reduced flux recovery generated non-finite E/B")
    return full


def reduced_rhs(case: Case, initial: InitialState, t: float, y: np.ndarray) -> np.ndarray:
    full = reduced_to_full(case, initial, y)
    return full_rhs(case, t, full)[:6]


def analytic_q(case: Case, y: np.ndarray, dy: np.ndarray) -> float:
    """Compute the wrong-model Ward defect from all state derivatives.

    This differentiates rho using phi', v', E', and B' from the actual wrong
    trajectory, then adds the anisotropic expansion work.  It is not imposed
    as a conservation law.
    """
    z = _components(case, y)
    _, _, phi_d, v_d, hp_d, hl_d, E_d, B_d = map(float, dy[:8])
    fd = 2.0 * case.c * z["f"] * phi_d
    rho_d = (
        z["v"] * v_d
        + case.mhat**2 * z["phi"] * phi_d
        + 0.5 * fd * (z["E"] ** 2 + z["B"] ** 2)
        + z["f"] * (z["E"] * E_d + z["B"] * B_d)
    )
    work_d = 2.0 * z["hp"] * (z["rho"] + z["pperp"]) + z["hl"] * (
        z["rho"] + z["ppar"]
    )
    q = rho_d + work_d
    if not math.isfinite(q):
        raise FloatingPointError("analytic Ward defect is non-finite")
    return q


def wrong_rhs(case: Case, t: float, y: np.ndarray) -> np.ndarray:
    if np.asarray(y).shape[0] < 9 or not np.isfinite(y[:9]).all():
        raise FloatingPointError("wrong-model RHS received malformed state")
    base = np.asarray(y[:8], dtype=float)
    dy = full_rhs(case, t, base, wrong_force=True)
    q = analytic_q(case, base, dy)
    z = _components(case, base)
    dI = _safe_exp(2.0 * z["lA"] + z["lC"], name="2*lA+lC") * q
    out = np.concatenate([dy, np.array([dI])])
    if not np.isfinite(out).all():
        raise FloatingPointError("wrong-model RHS generated non-finite derivative")
    return out


def _solve(rhs, span: tuple[float, float], y0: np.ndarray, times: np.ndarray, method: str):
    if method not in {"DOP853", "Radau"}:
        raise InputError(f"unsupported integration method {method!r}")
    try:
        sol = solve_ivp(
            rhs,
            span,
            np.asarray(y0, dtype=float),
            method=method,
            t_eval=times,
            rtol=2e-10,
            atol=2e-12,
            max_step=max((span[1] - span[0]) / 12.0, 1e-4),
        )
    except (FloatingPointError, OverflowError, ValueError) as exc:
        raise RuntimeError(f"{method} integration failed with unsafe state: {exc}") from exc
    if not sol.success or sol.y.shape[1] != times.size:
        raise RuntimeError(f"{method} integration did not complete: {sol.message}")
    if not np.isfinite(sol.y).all():
        raise RuntimeError(f"{method} integration returned non-finite trajectory")
    return sol


def _relative_error(values: np.ndarray, initial: float) -> np.ndarray:
    scale = max(abs(float(initial)), 1.0)
    return np.abs(values / scale - initial / scale)


def _trajectory_rows(case: Case, method: str, kind: str, times: np.ndarray, states: np.ndarray):
    for j, t in enumerate(times):
        row: dict[str, object] = {"case": case.name, "method": method, "kind": kind, "tau": float(t)}
        vals = states[:, j]
        for name, value in zip(STATE_NAMES, vals[:8]):
            row[name] = float(value)
        if vals.size > 8:
            row[WRONG_EXTRA] = float(vals[8])
        yield row


def run_case(case: Case) -> dict[str, object]:
    """Run full, reduced flux, method-comparison, and wrong-model controls."""
    initial = make_initial_state(case)
    times = validate_times(np.linspace(0.0, case.t_end, case.samples, dtype=float))
    span = (float(times[0]), float(times[-1]))
    full_solutions = {}
    reduced_solutions = {}
    for method in ("DOP853", "Radau"):
        full_solutions[method] = _solve(
            lambda t, y, m=method: full_rhs(case, t, y),
            span,
            initial.y0,
            times,
            method,
        )
        reduced_y0 = initial.y0[:6].copy()
        reduced_solutions[method] = _solve(
            lambda t, y: reduced_rhs(case, initial, t, y),
            span,
            reduced_y0,
            times,
            method,
        )
    wrong_y0 = np.concatenate([initial.y0, np.array([0.0])])
    wrong_solutions = {
        method: _solve(lambda t, y: wrong_rhs(case, t, y), span, wrong_y0, times, method)
        for method in ("DOP853", "Radau")
    }

    full = full_solutions["DOP853"].y
    full_radau = full_solutions["Radau"].y
    reduced = reduced_solutions["DOP853"].y
    reduced_full = np.column_stack([reduced_to_full(case, initial, reduced[:, j]) for j in range(times.size)])
    wrong = wrong_solutions["DOP853"].y
    wrong_radau = wrong_solutions["Radau"].y

    def constraints(states: np.ndarray) -> np.ndarray:
        out = []
        for j in range(states.shape[1]):
            z = _components(case, states[:, j])
            out.append(z["hp"] ** 2 + 2.0 * z["hp"] * z["hl"] - z["rho"] - case.lam)
        return np.asarray(out)

    c_full = constraints(full)
    c_reduced = constraints(reduced_full)
    c_wrong = constraints(wrong)
    V = 2.0 * full[0] + full[1]
    V_wrong = 2.0 * wrong[0] + wrong[1]
    wrong_I = wrong[8]
    wrong_invariant = np.array([_safe_exp(float(v), name="wrong volume") for v in V_wrong]) * c_wrong + wrong_I
    c0 = float(c_full[0])
    eflux = np.empty(times.size)
    bflux = np.empty(times.size)
    q_wrong = np.empty(times.size)
    for j in range(times.size):
        z = _components(case, full[:, j])
        eflux[j] = math.exp(2.0 * z["lA"]) * z["f"] * z["E"]
        bflux[j] = math.exp(2.0 * z["lA"]) * z["B"]
        q_wrong[j] = analytic_q(case, wrong[:8, j], wrong_rhs(case, times[j], wrong[:, j]))
    method_err = float(np.max(np.abs(full - full_radau)))
    reduced_err = float(np.max(np.abs(full - reduced_full)))
    reduced_radau_full = np.column_stack([reduced_to_full(case, initial, reduced_solutions["Radau"].y[:, j]) for j in range(times.size)])
    rho_scale = max(abs(initial.rho0), abs(case.lam), 1.0)
    flux_scale_e = max(abs(initial.electric_flux0), 1.0)
    flux_scale_b = max(abs(initial.magnetic_flux0), 1.0)
    diagnostics = {
        "case": case.name,
        "samples": int(times.size),
        "nfev_full_DOP853": int(full_solutions["DOP853"].nfev),
        "nfev_full_Radau": int(full_solutions["Radau"].nfev),
        "nfev_reduced_DOP853": int(reduced_solutions["DOP853"].nfev),
        "nfev_reduced_Radau": int(reduced_solutions["Radau"].nfev),
        "nfev_wrong_DOP853": int(wrong_solutions["DOP853"].nfev),
        "max_full_vs_Radau_state_abs": method_err,
        "max_full_vs_reduced_state_abs": reduced_err,
        "max_reduced_DOP853_vs_Radau_state_abs": float(np.max(np.abs(reduced_full-reduced_radau_full))),
        "max_wrong_DOP853_vs_Radau_state_abs": float(np.max(np.abs(wrong-wrong_radau))),
        "max_constraint_abs_full": float(np.max(np.abs(c_full))),
        "max_constraint_abs_reduced": float(np.max(np.abs(c_reduced))),
        "max_constraint_scaled_full": float(np.max(np.abs(c_full)) / rho_scale),
        "max_constraint_scaled_reduced": float(np.max(np.abs(c_reduced)) / rho_scale),
        "max_electric_flux_abs_error": float(np.max(np.abs(eflux - initial.electric_flux0))),
        "max_magnetic_flux_abs_error": float(np.max(np.abs(bflux - initial.magnetic_flux0))),
        "max_electric_flux_scaled_error": float(np.max(np.abs(eflux - initial.electric_flux0)) / flux_scale_e),
        "max_magnetic_flux_scaled_error": float(np.max(np.abs(bflux - initial.magnetic_flux0)) / flux_scale_b),
        "wrong_model_max_constraint_abs": float(np.max(np.abs(c_wrong))),
        "wrong_model_max_ward_Q_abs": float(np.max(np.abs(q_wrong))),
        "wrong_model_max_invariant_residual": float(np.max(np.abs(wrong_invariant - c0))),
        "wrong_model_final_constraint": float(c_wrong[-1]),
        "wrong_model_final_I": float(wrong_I[-1]),
        "initial_rho": float(initial.rho0),
        "initial_constraint": c0,
        "initial_hp": float(initial.hp0),
        "initial_hl": float(initial.hl0),
        "final_state_full_DOP853": full[:, -1].tolist(),
        "final_state_reduced_DOP853": reduced_full[:, -1].tolist(),
        "final_state_wrong_DOP853": wrong[:, -1].tolist(),
    }
    return {
        "case": case,
        "initial": initial,
        "times": times,
        "full_solutions": full_solutions,
        "reduced_solutions": reduced_solutions,
        "wrong_solutions": wrong_solutions,
        "full": full,
        "full_radau": full_radau,
        "reduced_full": reduced_full,
        "wrong": wrong,
        "constraint_full": c_full,
        "constraint_reduced": c_reduced,
        "constraint_wrong": c_wrong,
        "eflux": eflux,
        "bflux": bflux,
        "q_wrong": q_wrong,
        "wrong_invariant": wrong_invariant,
        "diagnostics": diagnostics,
    }


def default_cases() -> tuple[Case, ...]:
    return (
        Case("coupled_mixed", 0.35, 0.45, 0.01, 0.15, 0.02, 0.08, 0.06, 4.0, description="coupled scalar with E and B"),
        Case("pure_electric", 0.35, 0.45, 0.01, 0.15, 0.02, 0.08, 0.0, 4.0, description="scalar with electric field only"),
        Case("pure_magnetic", 0.35, 0.45, 0.01, 0.15, 0.02, 0.0, 0.08, 4.0, description="scalar with magnetic field only"),
        Case("c0", 0.35, 0.0, 0.01, 0.15, 0.02, 0.07, 0.06, 4.0, description="constant gauge coupling"),
        Case("minkowski", 0.5, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, description="zero-data Minkowski solution"),
        Case("pure_de_sitter", 0.0, 0.4, 0.03, 0.0, 0.0, 0.0, 0.0, 2.0, description="positive cosmological constant only"),
        Case("nonzero_scalar", 0.6, 0.25, 0.005, 0.25, 0.04, 0.0, 0.0, 3.0, description="nonzero scalar with no Maxwell field"),
        Case("early_contraction", 0.2, 0.2, 0.02, 0.1, 0.0, 0.02, 0.03, 0.35, branch=-1, description="short bounded contracting branch"),
    )


def analytic_fixture_checks() -> dict[str, float | bool]:
    """Check the two contract fixtures independently of the case suite.

    The fixture formulas are evaluated from the initial data and compared with
    a fresh full-system integration.  They do not project the constraint.
    """
    de_sitter = Case("fixture_de_sitter", 0.0, 0.31, 0.027, 0.0, 0.0, 0.0, 0.0, 1.5, 121)
    init_ds = make_initial_state(de_sitter)
    times_ds = validate_times(np.linspace(0.0, de_sitter.t_end, de_sitter.samples))
    sol_ds = _solve(lambda t, y: full_rhs(de_sitter, t, y), (0.0, de_sitter.t_end), init_ds.y0, times_ds, "DOP853")
    h0 = math.sqrt(de_sitter.lam / 3.0)
    expected_ds = np.zeros_like(sol_ds.y)
    expected_ds[0] = h0 * times_ds
    expected_ds[1] = h0 * times_ds
    expected_ds[4] = h0
    expected_ds[5] = h0
    err_ds = float(np.max(np.abs(sol_ds.y - expected_ds)))

    scalar = Case("fixture_massless_scalar", 0.0, 0.37, 0.0, 0.2, 0.11, 0.0, 0.0, 1.2, 121)
    init_sc = make_initial_state(scalar)
    times_sc = validate_times(np.linspace(0.0, scalar.t_end, scalar.samples))
    sol_sc = _solve(lambda t, y: full_rhs(scalar, t, y), (0.0, scalar.t_end), init_sc.y0, times_sc, "Radau")
    h0_sc = abs(scalar.v0) / math.sqrt(6.0)
    d = 1.0 + 3.0 * h0_sc * times_sc
    expected_sc = np.zeros_like(sol_sc.y)
    expected_sc[0] = np.log(d) / 3.0
    expected_sc[1] = np.log(d) / 3.0
    expected_sc[2] = scalar.phi0 + scalar.v0 / (3.0 * h0_sc) * np.log(d)
    expected_sc[3] = scalar.v0 / d
    expected_sc[4] = h0_sc / d
    expected_sc[5] = h0_sc / d
    err_sc = float(np.max(np.abs(sol_sc.y - expected_sc)))
    return {
        "de_sitter_max_abs_error": err_ds,
        "massless_scalar_max_abs_error": err_sc,
        "passed": bool(err_ds < 2e-10 and err_sc < 2e-9),
    }


def _write_csv(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def emit_artifacts(results: dict[str, object], runs: Sequence[dict[str, object]]) -> None:
    trajectory_rows = []
    constraint_rows = []
    flux_rows = []
    wrong_rows = []
    for run in runs:
        case: Case = run["case"]
        times: np.ndarray = run["times"]
        full: np.ndarray = run["full"]
        reduced_full: np.ndarray = run["reduced_full"]
        wrong: np.ndarray = run["wrong"]
        trajectory_rows.extend(_trajectory_rows(case, "DOP853", "full", times, full))
        trajectory_rows.extend(_trajectory_rows(case, "DOP853", "reduced_flux_recovered", times, reduced_full))
        trajectory_rows.extend(_trajectory_rows(case, "DOP853", "wrong_model", times, wrong))
        for j, t in enumerate(times):
            constraint_rows.append({
                "case": case.name, "tau": float(t),
                "C_full": float(run["constraint_full"][j]),
                "C_reduced": float(run["constraint_reduced"][j]),
                "C_wrong": float(run["constraint_wrong"][j]),
                "wrong_invariant_residual": float(run["wrong_invariant"][j] - run["constraint_wrong"][0]),
            })
            flux_rows.append({
                "case": case.name, "tau": float(t),
                "electric_flux": float(run["eflux"][j]),
                "magnetic_flux": float(run["bflux"][j]),
                "electric_flux_error": float(run["eflux"][j] - run["initial"].electric_flux0),
                "magnetic_flux_error": float(run["bflux"][j] - run["initial"].magnetic_flux0),
            })
            wrong_rows.append({
                "case": case.name, "tau": float(t), "Q_ward": float(run["q_wrong"][j]),
                "I_wrong": float(wrong[8, j]), "C_wrong": float(run["constraint_wrong"][j]),
                "weighted_C_plus_I": float(run["wrong_invariant"][j]),
            })
    _write_csv(HERE / "gravity_trajectories.csv", ["case", "method", "kind", "tau", *STATE_NAMES, WRONG_EXTRA], trajectory_rows)
    _write_csv(HERE / "gravity_constraints.csv", ["case", "tau", "C_full", "C_reduced", "C_wrong", "wrong_invariant_residual"], constraint_rows)
    _write_csv(HERE / "gravity_fluxes.csv", ["case", "tau", "electric_flux", "magnetic_flux", "electric_flux_error", "magnetic_flux_error"], flux_rows)
    _write_csv(HERE / "gravity_wrong_model.csv", ["case", "tau", "Q_ward", "I_wrong", "C_wrong", "weighted_C_plus_I"], wrong_rows)
    _write_csv(HERE / "gravity_case_summary.csv", ["case", "max_full_vs_Radau_state_abs", "max_full_vs_reduced_state_abs", "max_constraint_scaled_full", "max_constraint_scaled_reduced", "max_electric_flux_scaled_error", "max_magnetic_flux_scaled_error", "wrong_model_max_constraint_abs", "wrong_model_max_ward_Q_abs", "wrong_model_max_invariant_residual"], [r["diagnostics"] for r in runs])


def build_results(runs: Sequence[dict[str, object]]) -> dict[str, object]:
    source_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return {
        "status": "passed",
        "scope": "bounded classical scalar-Einstein-Maxwell Bianchi I benchmark; no Dirac quantum stress or cutoff removal",
        "source_file": str(Path(__file__).name),
        "source_sha256": source_sha256,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "software": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": _np_for_version.__version__,
            "scipy": SCIPY_VERSION,
        },
        "variables": {
            "time": "tau=mu*t",
            "phi": "physical_phi/Mpl",
            "v": "phi'",
            "hp": "Hperp/mu",
            "hl": "Hparallel/mu",
            "lA": "log(aperp)",
            "lC": "log(aparallel)",
            "E": "physical_E/(mu*Mpl)",
            "B": "physical_B/(mu*Mpl)",
            "U": "0.5*mhat^2*phi^2",
            "f": "exp(2*c*phi)>0",
        },
        "equations": {
            "constraint": "hp^2+2*hp*hl-rho-lambda",
            "constraint_propagation": "C'=-theta*C for the true model",
            "electric_flux": "exp(2*lA)*f*E",
            "magnetic_flux": "exp(2*lA)*B",
            "wrong_model": "v' omits only c*f*(B^2-E^2); Q=c*f*v*(B^2-E^2)",
            "wrong_model_invariant": "exp(2*lA+lC)*C+I, I'=exp(2*lA+lC)*Q",
        },
        "solver": {
            "methods": ["DOP853", "Radau"],
            "rtol": 2e-10,
            "atol": 2e-12,
            "bounded_time_limit": 100.0,
            "reduced_system": "E and B eliminated using two initial flux constants",
        },
        "cases": [
            {"parameters": r["case"].parameters(), "diagnostics": r["diagnostics"]} for r in runs
        ],
        "analytic_fixtures": analytic_fixture_checks(),
        "gates": {
            "all_finite_trajectories": all(np.isfinite(r["full"]).all() and np.isfinite(r["reduced_full"]).all() for r in runs),
            "full_reduced_agree": all(r["diagnostics"]["max_full_vs_reduced_state_abs"] < 2e-7 for r in runs),
            "methods_agree": all(r["diagnostics"]["max_full_vs_Radau_state_abs"] < 2e-7 for r in runs),
            "true_constraint_small": all(r["diagnostics"]["max_constraint_scaled_full"] < 2e-8 for r in runs),
            "fluxes_preserved": all(max(r["diagnostics"]["max_electric_flux_scaled_error"], r["diagnostics"]["max_magnetic_flux_scaled_error"]) < 2e-8 for r in runs),
            "wrong_invariant_small": all(r["diagnostics"]["wrong_model_max_invariant_residual"] < 2e-7 for r in runs),
            "auxiliary_methods_agree": all(max(r["diagnostics"]["max_reduced_DOP853_vs_Radau_state_abs"], r["diagnostics"]["max_wrong_DOP853_vs_Radau_state_abs"]) < 2e-7 for r in runs),
        },
    }


def write_readme(results: dict[str, object]) -> None:
    gates = results["gates"]
    text = f"""# Round7 bounded scalar–Einstein–Maxwell Bianchi-I benchmark

This directory contains a finite classical benchmark for the natural-unit system specified in the round7 task. It is a new-sector ODE calculation; it does not compute Dirac quantum stress tensors and makes no cutoff-removal claim.

`gravity_sim.py` integrates the full eight-variable state `(lA,lC,phi,v,hp,hl,E,B)` with both DOP853 and Radau. It separately integrates a six-variable reduced system (sharing the gravitational RHS) in which E and B are reconstructed from the conserved fluxes `exp(2*lA) f E` and `exp(2*lA) B`. The trajectories, constraints, fluxes, and wrong-model Ward data are emitted as CSV files.

The true constraint is `C=hp^2+2*hp*hl-rho-lambda` and propagates as `C'=-theta*C`. The control removes only the scalar electromagnetic force from `v'`, computes `Q` analytically from all state derivatives, and integrates `I'=exp(2*lA+lC)Q`; therefore `exp(2*lA+lC)C+I` remains constant while C itself drifts.

Cases: coupled mixed fields, pure electric, pure magnetic, c=0, Minkowski, pure de Sitter, nonzero scalar, and a short early-contraction branch. Inputs and time grids reject malformed, non-finite, non-monotone, and unsafe bounded runs with explicit exceptions.

Generated `{results['generated_utc']}` with Python {results['software']['python']}, NumPy {results['software']['numpy']}, SciPy {results['software']['scipy']}. Source SHA-256: `{results['source_sha256']}`.

Gate results: {json.dumps(gates, sort_keys=True)}
"""
    (HERE / "gravity_readme.md").write_text(text, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", help="run only named case (repeatable)")
    args = parser.parse_args(argv)
    cases = default_cases()
    if args.case:
        wanted = set(args.case)
        cases = tuple(c for c in cases if c.name in wanted)
        if len(cases) != len(wanted):
            missing = sorted(wanted - {c.name for c in cases})
            raise InputError(f"unknown case(s): {missing}")
    runs = [run_case(case) for case in cases]
    results = build_results(runs)
    results["gates"]["analytic_fixtures"] = results["analytic_fixtures"]["passed"]
    mixed = [r for r in runs if r["case"].name == "coupled_mixed"]
    results["wrong_control_discrimination"] = {"status": "tested" if mixed else "not_in_selected_cases"}
    if mixed:
        results["gates"]["wrong_constraint_fails_for_coupled_mixed"] = mixed[0]["diagnostics"]["wrong_model_max_constraint_abs"] > 1e-7
    failed = [name for name, ok in results["gates"].items() if not ok]
    if failed:
        raise RuntimeError(f"benchmark gates failed: {failed}")
    emit_artifacts(results, runs)
    # Hash is taken before the JSON/readme are written, so it is a stable exact
    # source fingerprint for this executable artifact.
    OUTPUT_JSON.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    write_readme(results)
    print(json.dumps({"status": results["status"], "cases": len(cases), "source_sha256": results["source_sha256"]}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (InputError, RuntimeError, FloatingPointError, OverflowError) as exc:
        print(f"gravity_sim error: {exc}", file=sys.stderr)
        raise SystemExit(2)
