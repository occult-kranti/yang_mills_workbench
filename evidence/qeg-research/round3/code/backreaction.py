"""Round-three homogeneous spinor-QED backreaction solver.

The evolution variables are dimensionless, ``s = m_e t``, ``a = e A_z/m_e``
and ``x = e E_z/m_e**2``.  This module deliberately keeps the finite
Landau/momentum grid explicit: the current is the mode sum requested by the
round-three closure and the two adiabatic counterterms are evaluated on that
same grid at every right-hand-side call.

This is a numerical experiment, not a continuum renormalization proof.  In
particular, ``raw_occupation`` is diagnostic only and is never clipped.
"""

from __future__ import annotations

import hashlib
import math
import platform
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.special import digamma


ALPHA = 1.0 / 137.035999084
E2 = 4.0 * math.pi * ALPHA


class SolverFailure(RuntimeError):
    """A descriptive failure of parameter validation or the causal closure."""


@dataclass(frozen=True)
class Params:
    a0: float = 0.0
    target_E: float = 1.0
    b: float = 10.0
    Tpump: float = 4.0
    tfinal: float = 50.0
    ncut: int = 8
    Kmax: float = 40.0
    nK: int = 256
    rtol: float = 2.0e-10
    atol: float = 2.0e-12
    max_step: float = 0.05
    sample_count: int = 501
    z_floor: float = 1.0e-8
    chi_mode: str = "matched"  # matched, omitted_matching, sign_reversed, unrenormalized


def bump_integral() -> float:
    value, error = quad(lambda u: math.exp(-1.0 / (u * (1.0 - u))),
                        0.0, 1.0, epsabs=2e-14, epsrel=2e-14,
                        points=(0.5,), limit=200)
    if not np.isfinite(value) or value <= 0.0:
        raise SolverFailure(f"bump normalization failed: I={value!r}, error={error!r}")
    return float(value)


def _validate(p: Params) -> None:
    if not np.isfinite(p.a0) or not np.isfinite(p.target_E):
        raise SolverFailure(f"a0 and target_E must be finite, got a0={p.a0!r}, target_E={p.target_E!r}")
    if p.b <= 0 or not np.isfinite(p.b):
        raise SolverFailure(f"b must be positive and finite, got {p.b!r}")
    if not np.isfinite(p.Tpump) or not np.isfinite(p.tfinal) or p.Tpump <= 0 or p.tfinal <= p.Tpump:
        raise SolverFailure(f"require tfinal > Tpump > 0, got Tpump={p.Tpump}, tfinal={p.tfinal}")
    if (isinstance(p.ncut, bool) or not np.isfinite(p.ncut)
            or p.ncut < 0 or int(p.ncut) != p.ncut):
        raise SolverFailure(f"ncut must be a nonnegative integer, got {p.ncut!r}")
    if (isinstance(p.nK, bool) or not np.isfinite(p.nK)
            or p.nK < 2 or int(p.nK) != p.nK):
        raise SolverFailure(f"nK must be an integer >= 2, got {p.nK!r}")
    if p.Kmax <= 0 or not np.isfinite(p.Kmax):
        raise SolverFailure(f"Kmax must be positive and finite, got {p.Kmax!r}")
    if (not np.isfinite(p.rtol) or not np.isfinite(p.atol) or not np.isfinite(p.max_step)
            or p.rtol <= 0 or p.atol <= 0 or p.max_step <= 0):
        raise SolverFailure("rtol, atol, and max_step must be positive")
    if (isinstance(p.sample_count, bool) or not np.isfinite(p.sample_count)
            or int(p.sample_count) != p.sample_count or p.sample_count < 3):
        raise SolverFailure("sample_count must be a finite integer >= 3")
    if not np.isfinite(p.z_floor) or p.z_floor <= 0:
        raise SolverFailure("z_floor must be positive and finite")
    if p.chi_mode not in {"matched", "omitted_matching", "sign_reversed",
                          "unrenormalized", "zero", "over_subtracted"}:
        raise SolverFailure("chi_mode must be matched, omitted_matching, sign_reversed, or unrenormalized")


class Grid:
    def __init__(self, p: Params):
        nodes, weights = np.polynomial.legendre.leggauss(int(p.nK))
        k_local = p.Kmax * nodes
        wk = p.Kmax * weights
        ns = np.arange(int(p.ncut) + 1, dtype=int)
        degeneracy = np.where(ns == 0, 1.0, 2.0)
        # n-major ordering: each block has the same K grid.
        self.K = np.tile(p.a0 + k_local, ns.size)
        self.M = np.repeat(np.sqrt(1.0 + 2.0 * p.b * ns), int(p.nK))
        self.weights = np.repeat(p.b * degeneracy / (4.0 * math.pi**2), int(p.nK)) * np.tile(wk, ns.size)
        self.n = np.repeat(ns, int(p.nK))
        self.size = self.K.size


def _chi(b: float) -> float:
    return float(E2 / (12.0 * math.pi**2) *
                 (b - math.log(2.0 * b) - digamma(1.0 + 1.0 / (2.0 * b))))


def _make_pump(target_E: float, Tpump: float):
    norm = bump_integral()
    amplitude = target_E / (Tpump * norm)

    def drive(s: float) -> float:
        u = s / Tpump
        if u <= 0.0 or u >= 1.0:
            return 0.0
        return amplitude * math.exp(-1.0 / (u * (1.0 - u)))

    return drive, norm, amplitude


def _initial_state(grid: Grid, a0: float) -> np.ndarray:
    pz = grid.K - a0
    om = np.sqrt(grid.M * grid.M + pz * pz)
    r = np.empty((3, grid.size), dtype=float)
    r[0] = -grid.M / om
    r[1] = 0.0
    r[2] = -pz / om
    # The final component integrates W_drive' = x F_drive.  Keeping it in the
    # adaptive state avoids contaminating the energy audit with macro-grid
    # quadrature error.
    return np.concatenate(([a0, 0.0], r.reshape(-1), [0.0]))


def _grid_terms(a: float, y: np.ndarray, grid: Grid):
    pz = grid.K - a
    om = np.sqrt(grid.M * grid.M + pz * pz)
    r = y[2:2 + 3 * grid.size].reshape(3, grid.size)
    rz = r[2]
    jrz = float(np.sum(grid.weights * rz))
    jkin = float(np.sum(grid.weights * (pz / om)))
    j0 = jrz + jkin
    c = float(np.sum(grid.weights * grid.M**2 / (4.0 * om**5)))
    s = float(np.sum(grid.weights * (5.0 * grid.M**2 * pz / (8.0 * om**7))))
    return pz, om, r, jrz, jkin, j0, c, s


def run(p: Params, *, return_modes: bool = False, gauge_check: bool = False) -> Dict[str, Any]:
    """Run one finite-grid causal closure and return JSON-serializable data."""
    _validate(p)
    grid = Grid(p)
    drive, bump_I, drive_amplitude = _make_pump(p.target_E, p.Tpump)
    chi_matched = _chi(p.b)
    # ``zero`` and ``over_subtracted`` remain accepted as input aliases for
    # old scripts.  Reported control runs use the precise canonical names.
    mode = {"zero": "omitted_matching", "over_subtracted": "sign_reversed"}.get(
        p.chi_mode, p.chi_mode)
    chi = {"matched": chi_matched, "omitted_matching": 0.0,
           "sign_reversed": -chi_matched, "unrenormalized": 0.0}[mode]
    y0 = _initial_state(grid, p.a0)
    nmode = grid.size

    def rhs(s: float, y: np.ndarray) -> np.ndarray:
        a, x = float(y[0]), float(y[1])
        pz, om, r, _, _, j0, c, ss = _grid_terms(a, y, grid)
        z = 1.0 if mode == "unrenormalized" else 1.0 + chi - E2 * c
        if not np.isfinite(z) or z <= p.z_floor:
            raise SolverFailure(
                f"causal Maxwell closure Z became nonpositive/tiny at s={s:.9g}: "
                f"Z={z:.9g}, chi={chi:.9g}, C={c:.9g}")
        out = np.empty_like(y)
        out[0] = -x
        quantum_current = j0 if mode == "unrenormalized" else j0 + ss * x * x
        out[1] = (drive(s) - E2 * quantum_current) / z
        rx, ry, rz = r
        dr = out[2:2 + 3 * nmode].reshape(3, nmode)
        dr[0] = -2.0 * pz * ry
        dr[1] = 2.0 * (pz * rx - grid.M * rz)
        dr[2] = 2.0 * grid.M * ry
        out[-1] = x * drive(s)
        return out

    t_sample = np.linspace(0.0, p.tfinal, int(p.sample_count))
    try:
        sol = solve_ivp(rhs, (0.0, p.tfinal), y0, method="DOP853", t_eval=t_sample,
                        rtol=p.rtol, atol=p.atol, max_step=p.max_step)
    except SolverFailure:
        raise
    except Exception as exc:
        raise SolverFailure(f"integrator failed: {type(exc).__name__}: {exc}") from exc
    if not sol.success:
        raise SolverFailure(f"integrator failed: {sol.message}")
    if sol.y.shape[1] != t_sample.size:
        raise SolverFailure(f"integrator returned {sol.y.shape[1]} samples, expected {t_sample.size}")

    # Macrodiagnostics are computed after integration. solve_ivp retains the
    # requested macro samples (not every internal RHS step), plus the mode
    # state needed for each sample; this is bounded by sample_count*nmode.
    nsamp = t_sample.size
    macro = {k: np.empty(nsamp, dtype=float) for k in (
        "s", "a", "x", "Fdrive", "Jrz", "Jkin", "J0", "Sx2", "C", "Z",
        "Wdrive", "Wexact", "energy_work_residual", "energy_work_relative",
        "max_r2_error", "raw_f_min", "raw_f_max", "raw_f_mean")}
    macro["s"][:] = t_sample
    for i, s_now in enumerate(t_sample):
        yi = sol.y[:, i]
        a, x = float(yi[0]), float(yi[1])
        pz, om, r, jrz, jkin, j0, c, ss = _grid_terms(a, yi, grid)
        z = 1.0 if mode == "unrenormalized" else 1.0 + chi - E2 * c
        hdotr = grid.M * r[0] + pz * r[2]
        wexact = z * x*x / 2.0 + E2 * float(np.sum(grid.weights * (hdotr + om)))
        fraw = 0.5 * (1.0 + hdotr / om)
        macro["a"][i], macro["x"][i] = a, x
        macro["Fdrive"][i] = drive(float(s_now))
        macro["Jrz"][i], macro["Jkin"][i], macro["J0"][i] = jrz, jkin, j0
        macro["Sx2"][i], macro["C"][i], macro["Z"][i] = ss*x*x, c, z
        macro["Wexact"][i] = wexact
        macro["max_r2_error"][i] = float(np.max(np.abs(np.sum(r*r, axis=0) - 1.0)))
        macro["raw_f_min"][i] = float(np.min(fraw))
        macro["raw_f_max"][i] = float(np.max(fraw))
        macro["raw_f_mean"][i] = float(np.sum(grid.weights * fraw) / np.sum(grid.weights))
    macro["Wdrive"][:] = sol.y[-1]
    resid = macro["Wexact"] - macro["Wexact"][0] - macro["Wdrive"]
    macro["energy_work_residual"][:] = resid
    energy_scale = float(max(np.max(np.abs(macro["Wexact"] - macro["Wexact"][0])),
                             np.max(np.abs(macro["Wdrive"]))))
    if energy_scale > 0.0:
        macro["energy_work_relative"][:] = np.abs(resid) / energy_scale
        relative_max: Optional[float] = float(np.max(macro["energy_work_relative"]))
    else:
        macro["energy_work_relative"][:] = 0.0
        relative_max = None

    # Exact finite-grid identity is a stringent implementation check; the
    # sampled trapezoid estimate is kept separate from the exact derivative.
    max_z = float(np.min(macro["Z"]))
    if max_z <= p.z_floor:
        raise SolverFailure(f"minimum sampled Z={max_z:.9g} <= z_floor={p.z_floor}")
    result: Dict[str, Any] = {
        "parameters": asdict(p),
        "constants": {"alpha": ALPHA, "e2": E2, "chi_matched": chi_matched,
                       "bump_integral": bump_I, "drive_amplitude": drive_amplitude},
        "grid": {"nmode": nmode, "ncut": p.ncut, "nK": p.nK, "Kmin": p.a0-p.Kmax,
                 "Kmax": p.a0+p.Kmax, "weight_sum": float(np.sum(grid.weights))},
        "diagnostics": {
            "final_a": float(macro["a"][-1]), "final_x": float(macro["x"][-1]),
            "final_field_change": float(macro["x"][-1]),
            "max_abs_x": float(np.max(np.abs(macro["x"]))),
            "min_Z": max_z, "max_raw_r2_error": float(np.max(macro["max_r2_error"])),
            "max_energy_work_residual_abs": float(np.max(np.abs(resid))),
            "energy_work_scale": energy_scale,
            "max_energy_work_residual_relative": relative_max,
            "final_raw_occupation_min": float(macro["raw_f_min"][-1]),
            "final_raw_occupation_max": float(macro["raw_f_max"][-1]),
            "final_raw_occupation_mean": float(macro["raw_f_mean"][-1]),
        },
        "macro": {k: v.tolist() for k, v in macro.items()},
        "curves": {
            "early": {k: v[:min(nsamp, 101)].tolist() for k,v in macro.items()},
            "late": {k: v[max(0, nsamp-101):].tolist() for k,v in macro.items()},
        },
        "provenance": {
            "python": sys.version, "platform": platform.platform(),
            "numpy": np.__version__, "scipy": __import__("scipy").__version__,
        },
    }
    if return_modes and nmode <= 100000:
        yf = sol.y[:, -1]
        pz = grid.K - yf[0]
        om = np.sqrt(grid.M*grid.M + pz*pz)
        rr = yf[2:2 + 3 * nmode].reshape(3, nmode)
        result["final_modes"] = {"K": grid.K.tolist(), "n": grid.n.tolist(), "M": grid.M.tolist(),
                                  "weight": grid.weights.tolist(), "rx": rr[0].tolist(),
                                  "ry": rr[1].tolist(), "rz": rr[2].tolist(),
                                  "r2": np.sum(rr*rr, axis=0).tolist(),
                                  "raw_occupation": (0.5*(1.0 + (grid.M*rr[0]+pz*rr[2])/om)).tolist()}
    if gauge_check:
        shift = 3.271
        gp = Params(**{**asdict(p), "a0": p.a0 + shift})
        # The translated run is a recursion-free check of P=K-a invariance.
        translated = run(gp, return_modes=False, gauge_check=False)
        dx = np.max(np.abs(np.asarray(result["macro"]["x"]) - np.asarray(translated["macro"]["x"])))
        da = np.max(np.abs((np.asarray(result["macro"]["a"]) + shift) - np.asarray(translated["macro"]["a"])))
        result["gauge_check"] = {"shift": shift, "max_x_difference": float(dx),
                                  "max_translated_a_difference": float(da),
                                  "passed": bool(dx < 2e-8 and da < 2e-8)}
    return result


def write_csv(result: Dict[str, Any], path: str | Path) -> None:
    import csv
    path = Path(path)
    macro = result["macro"]
    keys = list(macro)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        writer.writerows(zip(*(macro[k] for k in keys)))


def source_hash() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
