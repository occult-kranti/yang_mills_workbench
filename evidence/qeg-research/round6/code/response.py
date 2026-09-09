"""Round-six audited tangent response of the frozen finite-grid model.

Updates scenario preparation, input validation and provenance; equations unchanged.

This module keeps the regulator fixed while differentiating the coupled ODE with
respect to an external source amplitude.  It intentionally evaluates
``S = sum(w*(rz + p/omega))`` in one expression; round-three's separate
``Jrz + Jkin`` sums are retained only as a legacy comparison diagnostic.
"""
from __future__ import annotations

import csv
import hashlib
import math
import platform
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.special import digamma

# Import only constants and the legacy implementation for provenance/comparison.
R3 = Path(__file__).resolve().parents[2] / "round3" / "code"
if str(R3) not in sys.path:
    sys.path.insert(0, str(R3))
import backreaction as legacy  # type: ignore  # noqa: E402

ALPHA = legacy.ALPHA
E2 = legacy.E2


class ResponseFailure(RuntimeError):
    pass


@dataclass(frozen=True)
class Params:
    a0: float = 0.0
    target_E: float = 1.0
    b: float = 10.0
    Tpump: float = 4.0
    tfinal: float = 20.0
    ncut: int = 4
    Kmax: float = 20.0
    nK: int = 256
    rtol: float = 2.0e-10
    atol: float = 2.0e-12
    max_step: float = 0.05
    sample_count: int = 401
    z_floor: float = 1.0e-8
    chi_mode: str = "matched"
    # Additive delayed probe used only for the holdout tangent.
    probe_start: float = 8.0
    probe_duration: float = 4.0


class Grid:
    def __init__(self, p: Params, *, canonical_shift: float = 0.0):
        _validate(p)
        if not np.isfinite(canonical_shift):
            raise ResponseFailure("canonical_shift must be finite")
        nodes, weights = np.polynomial.legendre.leggauss(int(p.nK))
        local = p.Kmax * nodes
        wk = p.Kmax * weights
        ns = np.arange(int(p.ncut) + 1, dtype=int)
        degeneracy = np.where(ns == 0, 1.0, 2.0)
        self.K = np.tile(p.a0 + canonical_shift + local, ns.size)
        self.M = np.repeat(np.sqrt(1.0 + 2.0 * p.b * ns), int(p.nK))
        self.weights = np.repeat(p.b * degeneracy / (4.0 * math.pi**2), int(p.nK)) * np.tile(wk, ns.size)
        self.n = np.repeat(ns, int(p.nK))
        self.size = self.K.size
        if not (np.all(np.isfinite(self.K)) and np.all(np.isfinite(self.M))
                and np.all(np.isfinite(self.weights)) and np.all(self.M > 0) and np.all(self.weights > 0)):
            raise ResponseFailure("generated regulator coefficients must be finite with positive masses and weights")


def _validate(p: Params) -> None:
    if not np.isfinite(p.a0) or not np.isfinite(p.target_E) or not np.isfinite(p.b) or p.b <= 0:
        raise ResponseFailure("a0 and target_E must be finite and b must be positive")
    if not np.isfinite(p.Tpump) or not np.isfinite(p.tfinal) or p.Tpump <= 0 or p.tfinal <= p.Tpump:
        raise ResponseFailure("require finite tfinal > Tpump > 0")
    if not np.isfinite(p.Kmax) or p.Kmax <= 0:
        raise ResponseFailure("Kmax must be finite and positive")
    if not np.isfinite(p.probe_start) or not np.isfinite(p.probe_duration) or p.probe_start < 0 or p.probe_duration <= 0:
        raise ResponseFailure("probe_start must be finite/nonnegative and probe_duration positive")
    if (isinstance(p.ncut, bool) or not np.isfinite(p.ncut) or p.ncut < 0 or int(p.ncut) != p.ncut
            or isinstance(p.nK, bool) or not np.isfinite(p.nK) or p.nK < 2 or int(p.nK) != p.nK):
        raise ResponseFailure("ncut and nK must be finite integers (ncut >= 0, nK >= 2)")
    if (not np.isfinite(p.rtol) or not np.isfinite(p.atol) or not np.isfinite(p.max_step) or not np.isfinite(p.z_floor)
            or p.rtol <= 0 or p.atol <= 0 or p.max_step <= 0 or p.z_floor <= 0):
        raise ResponseFailure("rtol, atol, max_step, and z_floor must be finite and positive")
    if (isinstance(p.sample_count, bool) or not np.isfinite(p.sample_count)
            or p.sample_count < 3 or int(p.sample_count) != p.sample_count):
        raise ResponseFailure("sample_count must be a finite integer >= 3")
    if p.chi_mode not in {"matched", "omitted_matching", "sign_reversed"}:
        raise ResponseFailure(f"response tangent supports matched, omitted_matching, or sign_reversed chi_mode; got {p.chi_mode}")


def _validate_request(mode: str, probe_amp: float, canonical_shift: float = 0.0, gauge: bool = False) -> None:
    if mode not in {"source_amplitude", "delayed_probe"}:
        raise ResponseFailure("mode must be source_amplitude or delayed_probe")
    if not np.isfinite(probe_amp) or not np.isfinite(canonical_shift):
        raise ResponseFailure("probe_amp and canonical_shift must be finite")
    if mode == "source_amplitude" and probe_amp != 0:
        raise ResponseFailure("probe_amp is only defined for delayed_probe mode")
    if not isinstance(gauge, bool):
        raise ResponseFailure("gauge must be a boolean")


def _validated_epsilons(values: Iterable[float]) -> tuple[float, ...]:
    try:
        result = tuple(float(value) for value in values)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ResponseFailure("epsilons must be a nonempty iterable of finite positive numbers") from exc
    if not result or any(not math.isfinite(value) or value <= 0 for value in result):
        raise ResponseFailure("epsilons must be nonempty, finite and positive")
    if len(set(result)) != len(result):
        raise ResponseFailure("duplicate epsilons would overwrite CSV columns")
    return result


def bump_integral() -> float:
    value, err = quad(lambda u: math.exp(-1.0 / (u * (1.0 - u))), 0.0, 1.0,
                      epsabs=2e-14, epsrel=2e-14, points=(0.5,), limit=200)
    if not np.isfinite(value) or value <= 0:
        raise ResponseFailure(f"invalid bump normalization: {value}, {err}")
    return float(value)


def _chi(b: float) -> float:
    return float(E2 / (12.0 * math.pi**2) *
                 (b - math.log(2.0 * b) - digamma(1.0 + 1.0 / (2.0 * b))))


def _pulse(s: float, width: float, norm: float) -> float:
    u = s / width
    if u <= 0.0 or u >= 1.0:
        return 0.0
    return math.exp(-1.0 / (u * (1.0 - u))) / (width * norm)


def _initial_state(grid: Grid, a0: float, *, gauge_v: float = 0.0) -> np.ndarray:
    pz = grid.K - a0
    om = np.sqrt(grid.M * grid.M + pz * pz)
    r = np.empty((3, grid.size), dtype=float)
    r[0] = -grid.M / om
    r[1] = 0.0
    r[2] = -pz / om
    # Baseline: a,x,modes,Wdrive. Tangent: v,u,eta,dWdrive.
    z = np.concatenate(([a0, 0.0], r.reshape(-1), [0.0]))
    dz = np.zeros_like(z)
    dz[0] = gauge_v
    return np.concatenate((z, dz))


def _terms(a: float, y: np.ndarray, grid: Grid):
    pz = grid.K - a
    om = np.sqrt(grid.M * grid.M + pz * pz)
    r = y[2:2 + 3 * grid.size].reshape(3, grid.size)
    # This single weighted sum is the response implementation's source of truth.
    S = float(np.sum(grid.weights * (r[2] + pz / om)))
    S_legacy = float(np.sum(grid.weights * r[2]) + np.sum(grid.weights * (pz / om)))
    C = float(np.sum(grid.weights * grid.M**2 / (4.0 * om**5)))
    D = float(np.sum(grid.weights * (5.0 * grid.M**2 * pz / (8.0 * om**7))))
    return pz, om, r, S, S_legacy, C, D


def _tangent_terms(a: float, v: float, y: np.ndarray, dy: np.ndarray, grid: Grid):
    pz, om, r, S, S_legacy, C, D = _terms(a, y, grid)
    eta = dy[2:2 + 3 * grid.size].reshape(3, grid.size)
    q = -v  # delta canonical momentum is zero for source-amplitude response
    deltaS = float(np.sum(grid.weights * (eta[2] + grid.M**2 * q / om**3)))
    deltaC = float(np.sum(grid.weights * (-5.0 * grid.M**2 * pz * q / (4.0 * om**7))))
    deltaD = float(np.sum(grid.weights * (5.0 * grid.M**2 * (grid.M**2 - 6.0 * pz**2) * q / (8.0 * om**9))))
    return pz, om, r, eta, S, S_legacy, C, D, deltaS, deltaC, deltaD


def _closures(p: Params, *, mode: str, canonical_shift: float = 0.0):
    grid = Grid(p, canonical_shift=canonical_shift)
    norm = bump_integral()
    chi0 = _chi(p.b)
    if not np.isfinite(chi0):
        raise ResponseFailure("computed susceptibility is nonfinite")
    chi = {"matched": chi0, "omitted_matching": 0.0,
           "sign_reversed": -chi0, "unrenormalized": 0.0}[p.chi_mode]
    primary = lambda s: _pulse(s, p.Tpump, norm)
    probe = lambda s: _pulse(s - p.probe_start, p.probe_duration, norm)

    def drive(s: float, amp: float = 0.0) -> float:
        return p.target_E * primary(s) + (amp * probe(s) if mode == "delayed_probe" else 0.0)

    def delta_drive(s: float) -> float:
        return probe(s) if mode == "delayed_probe" else primary(s)

    return grid, norm, chi, drive, delta_drive


def _solve(p: Params, *, mode: str = "source_amplitude", probe_amp: float = 0.0,
           canonical_shift: float = 0.0, gauge: bool = False) -> Dict[str, Any]:
    _validate(p)
    _validate_request(mode, probe_amp, canonical_shift, gauge)
    grid, norm, chi, drive, delta_drive = _closures(p, mode=mode, canonical_shift=canonical_shift)
    n = grid.size
    y0 = _initial_state(grid, p.a0, gauge_v=1.0 if gauge else 0.0)
    base_len = 2 + 3 * n + 1
    dK = 1.0 if gauge else 0.0

    def rhs(s: float, yy: np.ndarray) -> np.ndarray:
        y = yy[:base_len]
        dy = yy[base_len:]
        a, x = float(y[0]), float(y[1])
        v, u = float(dy[0]), float(dy[1])
        pz, om, r, S, Slegacy, C, D = _terms(a, y, grid)
        Z = 1.0 if p.chi_mode == "unrenormalized" else 1.0 + chi - E2 * C
        if not np.isfinite(Z) or Z <= p.z_floor:
            raise ResponseFailure(f"Z became nonpositive/tiny at s={s}: {Z}")
        F = drive(s, probe_amp)
        deltaF = 0.0 if gauge else delta_drive(s)
        xp = (F - E2 * (S + D * x*x)) / Z
        # q = delta k - v. Source response has delta k=0; gauge has delta k=1.
        q = dK - v
        eta = dy[2:2 + 3*n].reshape(3, n)
        deltaS = float(np.sum(grid.weights * (eta[2] + grid.M**2 * q / om**3)))
        deltaC = float(np.sum(grid.weights * (-5.0 * grid.M**2 * pz * q / (4.0 * om**7))))
        deltaD = float(np.sum(grid.weights * (5.0 * grid.M**2 * (grid.M**2 - 6.0*pz**2) * q / (8.0 * om**9))))
        up = (deltaF - E2 * (deltaS + deltaD*x*x + 2.0*D*x*u) + E2*deltaC*xp) / Z
        out = np.empty_like(yy)
        out[:base_len] = 0.0
        out[0], out[1] = -x, xp
        dr = out[2:2 + 3*n].reshape(3, n)
        dr[0] = -2.0 * pz * r[1]
        dr[1] = 2.0 * (pz * r[0] - grid.M * r[2])
        dr[2] = 2.0 * grid.M * r[1]
        out[base_len - 1] = x * F
        out[base_len:] = 0.0
        out[base_len + 0], out[base_len + 1] = -u, up
        deta = out[base_len + 2:base_len + 2 + 3*n].reshape(3, n)
        deta[0] = 2.0 * (-pz * eta[1] - q * r[1])
        deta[1] = 2.0 * (pz * eta[0] - grid.M * eta[2] + q * r[0])
        deta[2] = 2.0 * (grid.M * eta[1])
        # Linearized drive-work accumulator and no numerical clipping.
        out[-1] = u * F + x * deltaF
        return out

    ts = np.linspace(0.0, p.tfinal, int(p.sample_count))
    try:
        sol = solve_ivp(rhs, (0.0, p.tfinal), y0, method="DOP853", t_eval=ts,
                        rtol=p.rtol, atol=p.atol, max_step=p.max_step)
    except ResponseFailure:
        raise
    except Exception as exc:
        raise ResponseFailure(f"integrator failed: {type(exc).__name__}: {exc}") from exc
    if not sol.success:
        raise ResponseFailure(sol.message)
    if sol.y.shape != (y0.size, ts.size) or not np.all(np.isfinite(sol.y)):
        raise ResponseFailure("integrator returned incomplete or nonfinite state samples")

    keys = ("s", "a", "x", "Fdrive", "Jrz", "Jkin", "S", "S_legacy", "legacy_S_effect",
            "Sx2", "C", "D", "Z", "Wdrive", "Wexact", "energy_work_residual",
            "energy_work_relative", "max_r2_error", "raw_f_min", "raw_f_max", "raw_f_mean",
            "v", "u", "deltaF", "deltaS", "deltaC", "deltaD", "deltaZ", "delta_xprime",
            "deltaJmatter", "deltaJmatter_direct", "deltaJ_residual", "deltaU", "max_tangent_orthogonality", "deltaWdrive", "deltaWexact", "delta_energy_work_residual",
            "delta_energy_work_relative")
    m = {k: np.full(ts.size, np.nan, dtype=float) for k in keys}
    for i, s in enumerate(ts):
        yy = sol.y[:, i]; y = yy[:base_len]; dy = yy[base_len:]
        a, x = float(y[0]), float(y[1]); v, u = float(dy[0]), float(dy[1])
        pz, om, r, S, Slegacy, C, D = _terms(a, y, grid)
        eta = dy[2:2 + 3*n].reshape(3, n)
        q = dK - v
        Z = 1.0 if p.chi_mode == "unrenormalized" else 1.0 + chi - E2*C
        F = drive(float(s), probe_amp); dF = 0.0 if gauge else delta_drive(float(s))
        xp = (F - E2*(S + D*x*x))/Z
        dS = float(np.sum(grid.weights*(eta[2] + grid.M**2*q/om**3)))
        dC = float(np.sum(grid.weights*(-5.0*grid.M**2*pz*q/(4.0*om**7))))
        dD = float(np.sum(grid.weights*(5.0*grid.M**2*(grid.M**2-6.0*pz**2)*q/(8.0*om**9))))
        du = (dF - E2*(dS + dD*x*x + 2.0*D*x*u) + E2*dC*xp)/Z
        hdotr = grid.M*r[0] + pz*r[2]
        W = Z*x*x/2 + E2*float(np.sum(grid.weights*(hdotr + om)))
        dU = float(np.sum(grid.weights*(grid.M*eta[0] + pz*eta[2] + (r[2] + pz/om)*q)))
        dW = -E2*dC*x*x/2 + Z*x*u + E2*dU
        dJdirect = dS - dC*xp - C*du + dD*x*x + 2.0*D*x*u + (chi/E2)*du
        dJresid = du - (dF - E2*dJdirect)
        fraw = 0.5*(1.0 + hdotr/om)
        m["s"][i], m["a"][i], m["x"][i], m["Fdrive"][i] = s, a, x, F
        m["Jrz"][i] = float(np.sum(grid.weights*r[2])); m["Jkin"][i] = float(np.sum(grid.weights*pz/om))
        m["S"][i], m["S_legacy"][i], m["legacy_S_effect"][i] = S, Slegacy, S-Slegacy
        m["Sx2"][i], m["C"][i], m["D"][i], m["Z"][i] = D*x*x, C, D, Z
        m["Wdrive"][i], m["Wexact"][i] = y[-1], W
        m["max_r2_error"][i] = float(np.max(np.abs(np.sum(r*r, axis=0)-1.0)))
        m["raw_f_min"][i], m["raw_f_max"][i], m["raw_f_mean"][i] = np.min(fraw), np.max(fraw), np.sum(grid.weights*fraw)/np.sum(grid.weights)
        m["v"][i], m["u"][i], m["deltaF"][i] = v, u, dF
        m["deltaS"][i], m["deltaC"][i], m["deltaD"][i], m["deltaZ"][i] = dS, dC, dD, -E2*dC
        m["delta_xprime"][i] = du
        m["deltaJmatter"][i] = dJdirect; m["deltaJmatter_direct"][i] = dJdirect
        m["deltaJ_residual"][i] = dJresid; m["deltaU"][i] = dU
        m["max_tangent_orthogonality"][i] = float(np.max(np.abs(np.sum(r*eta, axis=0))))
        m["deltaWdrive"][i], m["deltaWexact"][i] = dy[-1], dW
    m["energy_work_residual"] = m["Wexact"] - m["Wexact"][0] - m["Wdrive"]
    escale = max(float(np.max(np.abs(m["Wexact"]-m["Wexact"][0]))), float(np.max(np.abs(m["Wdrive"]))))
    m["energy_work_relative"] = np.abs(m["energy_work_residual"])/(escale if escale > 0 else 1.0)
    m["delta_energy_work_residual"] = m["deltaWexact"] - m["deltaWexact"][0] - m["deltaWdrive"]
    descale = max(float(np.max(np.abs(m["deltaWexact"]-m["deltaWexact"][0]))), float(np.max(np.abs(m["deltaWdrive"]))))
    m["delta_energy_work_relative"] = np.abs(m["delta_energy_work_residual"])/(descale if descale > 0 else 1.0)
    if not all(np.all(np.isfinite(v)) for v in m.values()):
        missing = [k for k, v in m.items() if not np.all(np.isfinite(v))]
        raise ResponseFailure(f"nonfinite or unassigned sampled diagnostics: {missing}")
    return {"parameters": asdict(p), "mode": mode, "probe_amp": probe_amp, "canonical_shift": canonical_shift,
            "gauge": gauge, "constants": {"alpha": ALPHA, "e2": E2, "chi": chi, "bump_integral": norm},
            "grid": {"nmode": n, "ncut": p.ncut, "nK": p.nK, "Kmin": p.a0-p.Kmax+canonical_shift, "Kmax": p.a0+p.Kmax+canonical_shift,
                     "weight_sum": float(np.sum(grid.weights))},
            "macro": {k: v.tolist() for k,v in m.items()},
            "diagnostics": {"min_Z": float(np.min(m["Z"])), "max_raw_r2_error": float(np.max(m["max_r2_error"])),
                            "max_energy_work_residual_abs": float(np.max(np.abs(m["energy_work_residual"]))),
                            "max_delta_energy_work_residual_abs": float(np.max(np.abs(m["delta_energy_work_residual"]))),
                            "max_deltaJ_residual": float(np.max(np.abs(m["deltaJ_residual"]))),
                            "max_tangent_orthogonality": float(np.max(m["max_tangent_orthogonality"])),
                            "max_legacy_S_effect": float(np.max(np.abs(m["legacy_S_effect"]))),
                            "final_a": float(m["a"][-1]), "final_x": float(m["x"][-1]),
                            "final_v": float(m["v"][-1]), "final_u": float(m["u"][-1])}}


def source_hash() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def legacy_hash() -> str:
    return hashlib.sha256(Path(legacy.__file__).read_bytes()).hexdigest()


def run_scenario(p: Params, *, mode: str = "source_amplitude", epsilons: Iterable[float] = (1e-2, 3e-3, 1e-3),
                 include_legacy: bool = True, probe_amp: float = 0.0) -> Dict[str, Any]:
    """Run tangent, central finite differences, and gauge checks for one fixed grid."""
    _validate(p)
    _validate_request(mode, probe_amp)
    epsilons = _validated_epsilons(epsilons)
    frozen_source, frozen_legacy = source_hash(), legacy_hash()
    base = _solve(p, mode=mode, probe_amp=probe_amp)
    base_m = {k: np.asarray(v) for k,v in base["macro"].items()}
    fd = []
    for eps in epsilons:
        if mode == "source_amplitude":
            pp = Params(**{**asdict(p), "target_E": p.target_E + eps})
            pm = Params(**{**asdict(p), "target_E": p.target_E - eps})
            plus = _solve(pp, mode=mode); minus = _solve(pm, mode=mode)
        else:
            plus = _solve(p, mode=mode, probe_amp=probe_amp+eps); minus = _solve(p, mode=mode, probe_amp=probe_amp-eps)
        ap = np.asarray(plus["macro"]["a"]); am = np.asarray(minus["macro"]["a"])
        xp = np.asarray(plus["macro"]["x"]); xm = np.asarray(minus["macro"]["x"])
        fda, fdx = (ap-am)/(2*eps), (xp-xm)/(2*eps)
        ta, tx = base_m["v"], base_m["u"]
        err_a, err_x = np.abs(fda-ta), np.abs(fdx-tx)
        scale = max(1.0, float(np.max(np.abs(ta))), float(np.max(np.abs(tx))))
        fd.append({"epsilon": eps, "a": fda.tolist(), "x": fdx.tolist(),
                   "max_abs_error_a": float(np.max(err_a)), "max_abs_error_x": float(np.max(err_x)),
                   "max_abs_error": float(max(np.max(err_a), np.max(err_x))),
                   "scaled_max_abs_error": float(max(np.max(err_a), np.max(err_x))/scale)})
    # Gauge tangent and translated baseline verify q=delta k-v=0 invariance.
    gau = _solve(p, mode=mode, probe_amp=probe_amp, gauge=True)
    gm = {k: np.asarray(v) for k,v in gau["macro"].items()}
    tr = _solve(Params(**{**asdict(p), "a0": p.a0+3.271}), mode=mode, probe_amp=probe_amp, canonical_shift=0.0)
    trm = {k: np.asarray(v) for k,v in tr["macro"].items()}
    gauge = {"max_v_minus_one": float(np.max(np.abs(gm["v"]-1.0)),),
             "max_u": float(np.max(np.abs(gm["u"]))),
             "max_translated_x": float(np.max(np.abs(base_m["x"]-trm["x"]))),
             "max_translated_a": float(np.max(np.abs((base_m["a"]+3.271)-trm["a"]))),
             "passed": bool(np.max(np.abs(gm["v"]-1.0)) < 2e-8 and np.max(np.abs(gm["u"])) < 2e-8 and
                             np.max(np.abs(base_m["x"]-trm["x"])) < 2e-8 and np.max(np.abs(base_m["a"]+3.271-trm["a"])) < 2e-8)}
    fd_min = min(x["scaled_max_abs_error"] for x in fd)
    extra_gates = {}
    if mode == "delayed_probe":
        pre = base_m["s"] < p.probe_start
        post = base_m["s"] > max(p.Tpump, p.probe_start + p.probe_duration)
        pre_max = float(max(np.max(np.abs(base_m["v"][pre])), np.max(np.abs(base_m["u"][pre])))) if np.any(pre) else None
        post_var = float(np.max(np.abs(base_m["deltaWexact"][post] - base_m["deltaWexact"][post][-1]))) if np.any(post) else None
        extra_gates = {"delayed_pre_tangent_pass": pre_max is not None and pre_max < 2e-8,
                       "delayed_post_work_constant_pass": post_var is not None and post_var < 2e-8,
                       "delayed_pre_tangent_samples": int(np.count_nonzero(pre)),
                       "delayed_post_work_samples": int(np.count_nonzero(post)),
                       "delayed_pre_tangent_max": pre_max, "delayed_post_work_variation": post_var}
    out = {"parameters": asdict(p), "mode": mode, "source_hash": frozen_source, "legacy_hash": frozen_legacy,
           "base": base, "finite_difference": fd, "gauge": gauge,
           "gates": {"tangent_fd_pass": bool(fd_min < 2e-5),
                     "gauge_pass": gauge["passed"], "Z_floor_pass": bool(base["diagnostics"]["min_Z"] > p.z_floor),
                     "energy_pass": bool(base["diagnostics"]["max_energy_work_residual_abs"] < 5e-7 and base["diagnostics"]["max_delta_energy_work_residual_abs"] < 5e-7),
                     "current_variation_pass": bool(base["diagnostics"]["max_deltaJ_residual"] < 5e-7),
                     "tangent_orthogonality_pass": bool(base["diagnostics"]["max_tangent_orthogonality"] < 5e-7),
                     "raw_norm_pass": bool(base["diagnostics"]["max_raw_r2_error"] < 5e-7),
                     **{k: v for k, v in extra_gates.items() if k.endswith("_pass")}},
           "diagnostics": {**base["diagnostics"], **{k: v for k, v in extra_gates.items() if not k.endswith("_pass")}}}
    if include_legacy and mode == "delayed_probe" and probe_amp != 0:
        out["legacy_effect"] = {"status": "not_comparable", "reason": "legacy solver has no delayed baseline probe"}
    elif include_legacy:
        legacy_fields = {"a0", "target_E", "b", "Tpump", "tfinal", "ncut", "Kmax", "nK", "rtol", "atol", "max_step", "sample_count", "z_floor", "chi_mode"}
        lp = legacy.Params(**{k: v for k, v in asdict(p).items() if k in legacy_fields})
        old = legacy.run(lp)
        om = old["macro"]
        out["legacy_effect"] = {"max_abs_a": float(np.max(np.abs(base_m["a"]-np.asarray(om["a"]))),),
                                 "max_abs_x": float(np.max(np.abs(base_m["x"]-np.asarray(om["x"]))),),
                                 "legacy_final_a": float(om["a"][-1]), "legacy_final_x": float(om["x"][-1])}
    if source_hash() != frozen_source or legacy_hash() != frozen_legacy:
        raise ResponseFailure("source changed during scenario; discard mixed-source result")
    return out


def write_csv(result: Dict[str, Any], path: str | Path) -> None:
    """Write a chart-friendly long table for baseline/tangent and all FD epsilons."""
    path = Path(path)
    b = result["base"]["macro"]
    eps_map = {float(fd["epsilon"]): fd for fd in result["finite_difference"]}
    keys = ["scenario", "epsilon", "s", "a", "x", "v", "u", "fd_a", "fd_x", "abs_err_a", "abs_err_x", "Z", "W_residual", "delta_W_residual"]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for i, s in enumerate(b["s"]):
            common = {"scenario": result["mode"], "s": s, "a": b["a"][i], "x": b["x"][i],
                      "v": b["v"][i], "u": b["u"][i], "Z": b["Z"][i],
                      "W_residual": b["energy_work_residual"][i], "delta_W_residual": b["delta_energy_work_residual"][i]}
            w.writerow({**common, "epsilon": "", "fd_a": "", "fd_x": "", "abs_err_a": "", "abs_err_x": ""})
            for eps, fd in eps_map.items():
                fda, fdx = fd["a"][i], fd["x"][i]
                w.writerow({**common, "epsilon": eps, "fd_a": fda, "fd_x": fdx,
                            "abs_err_a": abs(fda-b["v"][i]), "abs_err_x": abs(fdx-b["u"][i])})
