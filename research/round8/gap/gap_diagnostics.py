#!/usr/bin/env python3
"""Reproducible free-scalar and positive-correlator counterexamples, not Yang--Mills.

Run: python3 gap_diagnostics.py --output .
Dependencies: Python >=3.10, NumPy, Matplotlib. No simulation output is a proof
of the Yang--Mills mass gap; see README.md for the exact conditional statements.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
from pathlib import Path
from typing import Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def finite_real(value: float, name: str, *, positive: bool = False) -> float:
    if isinstance(value, (bool, str, bytes)):
        raise ValueError(f"{name} must be a finite real number")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite real number") from exc
    if not math.isfinite(result) or (result <= 0 if positive else result < 0):
        bound = "positive" if positive else "nonnegative"
        raise ValueError(f"{name} must be finite and {bound}")
    return result


def lattice_frequency(mass: float, spacing: float, sites: int, mode: int = 1) -> float:
    """Periodic 1-D free-scalar normal-mode frequency, natural units.

    This function includes k=0 when explicitly requested. The volume study
    requests k=1 and excludes the massless zero mode by construction.
    """
    m = finite_real(mass, "mass")
    a = finite_real(spacing, "spacing", positive=True)
    if isinstance(sites, bool) or not isinstance(sites, (int, np.integer)) or sites < 2:
        raise ValueError("sites must be an integer >= 2")
    if isinstance(mode, bool) or not isinstance(mode, (int, np.integer)) or not 0 <= mode < sites:
        raise ValueError("mode must be an integer with 0 <= mode < sites")
    # k and N-k have exactly equal frequencies, avoiding a sin(pi-epsilon) loss.
    k = min(int(mode), int(sites - mode))
    momentum = 2.0 * (math.sin(math.pi * (k / sites)) / a)
    answer = math.hypot(m, momentum)
    if not math.isfinite(answer):
        raise ArithmeticError("frequency exceeds floating-point range")
    return answer


def _spectrum(masses: Iterable[float], amplitudes: Iterable[float]):
    ms, amps = list(masses), list(amplitudes)
    if not ms or len(ms) != len(amps):
        raise ValueError("masses and amplitudes must have equal nonzero length")
    pairs = [(finite_real(m, "mass"), finite_real(a, "amplitude")) for m, a in zip(ms, amps)]
    support = [(m, math.log(a)) for m, a in pairs if a > 0]
    if not support:
        raise ValueError("at least one amplitude must be positive")
    support.sort()
    return support


def _logsumexp(values: Iterable[float]) -> float:
    values = list(values)
    peak = max(values)
    if not math.isfinite(peak):
        raise ArithmeticError("empty or nonfinite log-sum support")
    return peak + math.log(math.fsum(math.exp(v - peak) for v in values))


def log_correlator(time: float, masses: Iterable[float], amplitudes: Iterable[float]) -> float:
    t = finite_real(time, "time")
    support = _spectrum(masses, amplitudes)
    m0 = support[0][0]
    value = -m0 * t + _logsumexp(loga - (m - m0) * t for m, loga in support)
    if not math.isfinite(value):
        raise ArithmeticError("log correlator exceeds floating-point range")
    return value


def effective_mass(time: float, interval: float, masses: Iterable[float], amplitudes: Iterable[float]) -> float:
    """Stable [log C(t)-log C(t+delta)]/delta.

    The mass-minimum factor cancels analytically. log1p/expm1 avoid small-delta
    cancellation; log-sum-exp handles large mass-time products and amplitudes.
    No subtraction of two enormous nearly equal log C values is performed.
    """
    t = finite_real(time, "time")
    delta = finite_real(interval, "interval", positive=True)
    support = _spectrum(masses, amplitudes)
    m0 = support[0][0]
    gaps = [m - m0 for m, _ in support]
    logs = [loga - gap * t for gap, (_, loga) in zip(gaps, support)]
    peak = max(logs)
    shifted = [v - peak for v in logs]
    weights = [math.exp(v) for v in shifted]
    weight_sum = math.fsum(weights)
    change = math.fsum(w * math.expm1(-gap * delta) for w, gap in zip(weights, gaps)) / weight_sum
    if change > -0.5:
        # Evaluate the divided difference before multiplying by delta. This
        # also handles subnormal delta for which gap*delta rounds to zero.
        quotients = []
        for gap in gaps:
            z = gap * delta
            if z == 0:
                quotients.append(gap)
            elif math.isinf(z):
                quotients.append(1.0 / delta)
            else:
                quotients.append(gap * (-math.expm1(-z) / z))
        divided_change = math.fsum((w / weight_sum) * q for w, q in zip(weights, quotients))
        factor = -math.log1p(change) / (-change) if change else 1.0
        gap_part = divided_change * factor
    else:
        numerator = _logsumexp(v - gap * delta for v, gap in zip(shifted, gaps))
        denominator = math.log(weight_sum)
        gap_part = (denominator - numerator) / delta
    value = m0 + gap_part
    if not math.isfinite(value):
        raise ArithmeticError("effective mass exceeds floating-point range")
    return value


def _write_csv(path: Path, rows: list[dict]):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def produce(output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": "#fafafa", "axes.facecolor": "#fafafa",
                         "savefig.facecolor": "#fafafa"})
    fixed_l = 10.0
    refinement = []
    for mass in [0.0, 0.7]:
        target = math.hypot(mass, 2 * math.pi / fixed_l)
        for n in [8, 16, 32, 64, 128, 256, 512, 1024]:
            freq = lattice_frequency(mass, fixed_l / n, n)
            refinement.append(dict(mass=mass, L=fixed_l, N=n, a=fixed_l/n, mode=1,
                                   massless_zero_mode_excluded=True, omega=freq,
                                   fixed_L_continuum_omega=target,
                                   absolute_error=abs(freq-target)))
    volume = []
    fixed_a = 0.125
    for mass in [0.0, 0.7]:
        for n in [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]:
            length = n * fixed_a
            volume.append(dict(mass=mass, L=length, N=n, a=fixed_a, mode=1,
                               massless_zero_mode_excluded=True,
                               omega=lattice_frequency(mass, fixed_a, n),
                               continuum_k1_omega=math.hypot(mass, 2*math.pi/length),
                               infinite_volume_limit=mass))
    _write_csv(output / "finite_volume.csv", volume)
    _write_csv(output / "fixed_volume_refinement.csv", refinement)

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.5), layout="constrained")
    colors = {0.0: "#20639b", 0.7: "#ab4e00"}
    for mass in [0.0, 0.7]:
        rows = [r for r in refinement if r["mass"] == mass]
        axes[0].plot([r["N"] for r in rows], [r["omega"] for r in rows], "o-", color=colors[mass], label=f"m = {mass:g}")
        axes[0].axhline(rows[-1]["fixed_L_continuum_omega"], color=colors[mass], linestyle=":", alpha=.8)
        rows = [r for r in volume if r["mass"] == mass]
        axes[1].loglog([r["L"] for r in rows], [r["omega"] for r in rows], "o-", color=colors[mass], label=f"m = {mass:g}")
    axes[0].set_xscale("log", base=2)
    axes[0].set(xlabel="Number of sites N (L = 10 fixed)", ylabel="Lowest nonzero-mode frequency", title="Refining a at fixed volume leaves an infrared scale")
    axes[1].set(xlabel="Physical length L (a = 0.125 fixed)", ylabel="Lowest nonzero-mode frequency", title="Increasing physical volume distinguishes m = 0")
    axes[0].legend(frameon=False)
    axes[1].legend(frameon=False)
    for ax in axes:
        ax.grid(alpha=.2)
    fig.suptitle("Free-scalar toy counterexample • massless k = 0 explicitly excluded", fontsize=14)
    fig.savefig(output / "finite_volume.png", dpi=170)
    fig.savefig(output / "finite_volume.svg")
    plt.close(fig)

    masses, amplitudes = [0.1, 1.0], [1e-12, 1.0]
    delta = .5
    crossover = math.log(amplitudes[1]/amplitudes[0])/(masses[1]-masses[0])
    correlator = []
    for t in np.linspace(0, 80, 321):
        t = float(t)
        logc = log_correlator(t, masses, amplitudes)
        light = math.log(amplitudes[0]) - masses[0]*t
        heavy = math.log(amplitudes[1]) - masses[1]*t
        correlator.append(dict(time=t, interval=delta, light_mass=masses[0], heavy_mass=masses[1],
                               light_amplitude=amplitudes[0], heavy_amplitude=amplitudes[1],
                               log_C=logc, effective_mass=effective_mass(t, delta, masses, amplitudes),
                               light_spectral_fraction=math.exp(light-logc),
                               heavy_spectral_fraction=math.exp(heavy-logc)))
    _write_csv(output / "hidden_light_state.csv", correlator)
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.5), layout="constrained")
    times = [r["time"] for r in correlator]
    axes[0].plot(times, [r["effective_mass"] for r in correlator], color="#20639b", lw=2.5)
    axes[0].axhline(.1, color="#ab4e00", linestyle="--", label="Lowest supported mass = 0.1")
    axes[0].axvline(crossover, color="#888888", linestyle=":", label=f"Equal contributions: t ≈ {crossover:.2f}")
    axes[0].set(xlabel="Euclidean time t", ylabel="Effective mass (δ = 0.5)", ylim=(.02, 1.08), title="An early plateau can conceal a much lighter state")
    axes[0].legend(frameon=False, fontsize=9)
    axes[1].plot(times, [r["log_C"]/math.log(10) for r in correlator], color="#20639b", lw=2.5, label="Full positive correlator")
    axes[1].plot(times, [(math.log(1e-12)-.1*t)/math.log(10) for t in times], color="#ab4e00", linestyle="--", label="Light contribution")
    axes[1].plot(times, [-t/math.log(10) for t in times], color="#555555", linestyle=":", label="Heavy contribution")
    axes[1].set(xlabel="Euclidean time t", ylabel="log₁₀ C", title="The small overlap delays visibility")
    axes[1].legend(frameon=False, fontsize=9)
    for ax in axes:
        ax.grid(alpha=.2)
    fig.suptitle("Two-exponential toy counterexample • positive spectral weights", fontsize=14)
    fig.savefig(output / "hidden_light_state.png", dpi=170)
    fig.savefig(output / "hidden_light_state.svg")
    plt.close(fig)

    summary = {"status": "computed toy diagnostics; no Yang--Mills simulation or proof",
               "units": "natural units; arbitrary common mass and length scale",
               "zero_mode": "massless k=0 excluded; full massless field has no positive infinite-volume gap",
               "fixed_volume": {"L": fixed_l, "massless_continuum_k1": 2*math.pi/fixed_l,
                                "N_1024_massless_frequency": lattice_frequency(0, fixed_l/1024, 1024)},
               "volume": {"a": fixed_a, "L_4_massless_frequency": lattice_frequency(0, fixed_a, 32),
                          "L_1024_massless_frequency": lattice_frequency(0, fixed_a, 8192)},
               "hidden_state": {"masses": masses, "amplitudes": amplitudes, "interval": delta,
                                "equal_contribution_time": crossover,
                                "selected_effective_masses": {str(t): effective_mass(t, delta, masses, amplitudes) for t in [0,5,10,20,30,40,60,80]}},
               "environment": {"python": platform.python_version(), "numpy": np.__version__, "matplotlib": matplotlib.__version__}}
    (output / "experiment_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n")
    return summary


def manifest(output: Path):
    records = []
    for path in sorted(output.iterdir()):
        if path.is_file() and path.name != "manifest.json" and path.suffix in {".py", ".md", ".csv", ".json", ".png", ".svg"}:
            records.append({"file": path.name, "bytes": path.stat().st_size,
                            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    (output / "manifest.json").write_text(json.dumps({"algorithm":"SHA-256", "files":records},indent=2)+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    result = produce(args.output)
    manifest(args.output)
    print(json.dumps(result, indent=2, allow_nan=False))
