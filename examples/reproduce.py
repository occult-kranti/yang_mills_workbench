#!/usr/bin/env python3
"""Small reproducible textbook benchmarks using SciPy numerical algorithms."""
from __future__ import annotations
import argparse, csv, json, math, platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.linalg import eigh_tridiagonal
from scipy.sparse import diags
from scipy.sparse.linalg import expm_multiply

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

H = 6.62607015e-34
HBAR = H / (2 * np.pi)
ME = 9.1093837139e-31
EV = 1.602176634e-19


def csv_write(path: Path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)


def oscillator(out: Path):
    omega0, gamma, x0, v0 = 4.0, 0.18, 1.0, 0.0
    wd = math.sqrt(omega0**2 - gamma**2)
    t = np.linspace(0.0, 20.0, 1001)

    def rhs(_, y):
        return [y[1], -2 * gamma * y[1] - omega0**2 * y[0]]

    sol = solve_ivp(rhs, (t[0], t[-1]), [x0, v0], t_eval=t, rtol=2e-10, atol=2e-12)
    if not sol.success:
        raise RuntimeError(sol.message)
    analytic = np.exp(-gamma * t) * (x0 * np.cos(wd * t) + (v0 + gamma * x0) / wd * np.sin(wd * t))
    err = np.abs(sol.y[0] - analytic)
    max_error = float(err.max())
    csv_write(out / "oscillator.csv", ["time_s", "numerical_x_m", "analytic_x_m", "absolute_error_m"],
              zip(t, sol.y[0], analytic, err))
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(t, sol.y[0], label="solve_ivp")
    ax.plot(t, analytic, "--", label="underdamped analytic")
    ax.set(xlabel="time (s)", ylabel="displacement (m)", title="Damped oscillator textbook benchmark")
    ax.legend(); fig.tight_layout(); fig.savefig(out / "oscillator.png", dpi=140); plt.close(fig)
    if max_error > 2e-6:
        raise RuntimeError(f"oscillator error {max_error:.3g} m exceeds threshold")
    return {"max_absolute_error_m": max_error, "omega0_rad_s": omega0, "gamma_s^-1": gamma, "solver": "scipy.integrate.solve_ivp"}


def infinite_well(out: Path):
    L, mass = 1e-9, ME
    analytic = np.array([(n * n * HBAR * HBAR * np.pi**2 / (2 * mass * L**2)) / EV for n in (1, 2, 3)])
    rows, errors = [], []
    for ngrid in (100, 200, 400):
        dx = L / (ngrid + 1)
        diag = np.full(ngrid, HBAR**2 / (mass * dx**2))
        off = np.full(ngrid - 1, -HBAR**2 / (2 * mass * dx**2))
        vals = eigh_tridiagonal(diag, off, select="i", select_range=(0, 2), check_finite=True)[0] / EV
        rel = np.abs((vals - analytic) / analytic)
        errors.append(rel)
        rows.extend((ngrid, i + 1, vals[i], analytic[i], rel[i]) for i in range(3))
    csv_write(out / "quantum_well.csv", ["interior_grid_points", "level", "numerical_energy_eV", "analytic_energy_eV", "relative_error"], rows)
    # Plot the finest-grid first three energies against the exact values.
    finest = np.array([r[2] for r in rows if r[0] == 400])
    fig, ax = plt.subplots(figsize=(6.4, 3.6)); levels = np.arange(1, 4)
    ax.plot(levels, analytic, "o--", label="infinite-well analytic")
    ax.plot(levels, finest, "s", label="tridiagonal eigensolver (N=400)")
    ax.set(xlabel="quantum level n", ylabel="energy (eV)", title="Infinite quantum well textbook benchmark")
    ax.legend(); fig.tight_layout(); fig.savefig(out / "quantum_well.png", dpi=140); plt.close(fig)
    # For a second-order stencil, halving dx should reduce error by about four.
    ratios = (errors[0][0] / errors[1][0], errors[1][0] / errors[2][0])
    finest_max = float(errors[-1].max())
    if not (all(3.2 < x < 4.8 for x in ratios) and finest_max < 1e-4):
        raise RuntimeError(f"well convergence check failed: ratios={ratios}, finest={finest_max:.3g}")
    return {"analytic_energies_eV": analytic.tolist(), "finest_relative_errors": errors[-1].tolist(),
            "grid_error_ratios_100_to_200_and_200_to_400": list(map(float, ratios)),
            "solver": "scipy.linalg.eigh_tridiagonal"}


def diffusion(out: Path):
    L, D, ngrid = 1.0, 0.08, 80
    x = np.linspace(0, L, ngrid + 2)
    dx = x[1] - x[0]
    interior = x[1:-1]
    u0 = np.sin(np.pi * interior / L)
    lap = diags([np.ones(ngrid - 1), -2 * np.ones(ngrid), np.ones(ngrid - 1)], [-1, 0, 1], format="csr") / dx**2
    operator = D * lap
    times = np.linspace(0, 1.0, 101)
    numerical = np.array([expm_multiply(operator * float(t), u0) for t in times])
    exact_amp = np.exp(-D * (np.pi / L) ** 2 * times)
    exact = exact_amp[:, None] * u0[None, :]
    err = np.max(np.abs(numerical - exact), axis=1)
    amp = (numerical @ u0) / np.dot(u0, u0)
    csv_write(out / "diffusion.csv", ["time_s", "numerical_mode_amplitude", "analytic_mode_amplitude", "max_absolute_error"],
              zip(times, amp, exact_amp, err))
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for idx in (0, 25, 50, 100): ax.plot(interior, numerical[idx], label=f"t={times[idx]:.2f} s")
    ax.set(xlabel="position (m)", ylabel="temperature-like field (arb.)", title="1D diffusion textbook benchmark")
    ax.legend(); fig.tight_layout(); fig.savefig(out / "diffusion.png", dpi=140); plt.close(fig)
    max_error = float(err.max())
    if max_error > 2e-4:
        raise RuntimeError(f"diffusion error {max_error:.3g} exceeds threshold")
    return {"max_absolute_error": max_error, "diffusion_coefficient_m2_s": D, "grid_points_interior": ngrid,
            "solver": "scipy.sparse.linalg.expm_multiply with sparse diffusion operator"}


def main():
    ap = argparse.ArgumentParser(description="Reproduce three small SciPy textbook benchmarks")
    ap.add_argument("--experiment", choices=("oscillator", "well", "diffusion", "all"), default="all")
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    if args.output.exists() and not args.output.is_dir():
        ap.error("--output must be a directory path")
    args.output.mkdir(parents=True, exist_ok=True)
    selected = {"oscillator": oscillator, "well": infinite_well, "diffusion": diffusion}
    if args.experiment != "all": selected = {args.experiment: selected[args.experiment]}
    metrics = {name: fn(args.output) for name, fn in selected.items()}
    metrics["metadata"] = {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "matplotlib": matplotlib.__version__}
    (args.output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
