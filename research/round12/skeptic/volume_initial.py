#!/usr/bin/env python3
"""Reproduce finite-graph volume scaling and the tensor-product counterbenchmark.

Run: python volume_checks.py [--out OUTPUT_DIRECTORY]
Python >=3.10; numpy, scipy, matplotlib. No network, no input files.
Numerical eigenvalues are diagnostics; analytic inequalities are proved in volume-bridge.md.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import eigh_tridiagonal


def write_csv(path, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def counts(d, n):
    return d*n*(n+1)**(d-1), math.comb(d, 2)*n*n*(n+1)**(d-2)


def enumerate_box(d, n):
    vertices = list(itertools.product(range(n+1), repeat=d))
    edges = []
    for v in vertices:
        for direction in range(d):
            if v[direction] < n:
                w = list(v)
                w[direction] += 1
                edges.append((v, tuple(w)))
    plaquettes = []
    for v in vertices:
        for i, j in itertools.combinations(range(d), 2):
            if v[i] < n and v[j] < n:
                plaquettes.append((v, i, j))
    return vertices, edges, plaquettes


def one_square(kappa, cutoff):
    n = np.arange(cutoff+1, dtype=float)
    diag = n*(n+2)+kappa
    off = np.full(cutoff, -kappa/2)
    vals, vecs = eigh_tridiagonal(diag, off, select="i", select_range=(0, 1))
    # Exact residual norm of the embedded finite eigenvector in the infinite
    # Jacobi matrix, up to eigensolver floating-point error.
    residuals = abs(kappa/2*vecs[-1, :])
    return vals, residuals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent/"output")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    checks = []
    for d in (2, 3):
        for n in range(1, 5):
            _, edges, plaquettes = enumerate_box(d, n)
            expected = counts(d, n)
            assert (len(edges), len(plaquettes)) == expected
            checks.append({"check": "box_enumeration", "d": d, "n_cells": n,
                           "edges": len(edges), "plaquettes": len(plaquettes), "passed": True})
    # Exhaustively check the combinatorial lower-bound premise on the 1x1,
    # 2x2 planar and single-cube boxes. This is not a spin-network enumeration.
    for d, n in ((2, 1), (2, 2), (3, 1)):
        vertices, edges, _ = enumerate_box(d, n)
        minimum = len(edges)+1
        for mask in range(1, 1 << len(edges)):
            degrees = dict.fromkeys(vertices, 0)
            size = 0
            for k, (v, w) in enumerate(edges):
                if (mask >> k) & 1:
                    degrees[v] += 1
                    degrees[w] += 1
                    size += 1
            if all(degree != 1 for degree in degrees.values()):
                minimum = min(minimum, size)
        assert minimum == 4
        checks.append({"check": "nonempty_support_without_degree_one", "d": d,
                       "n_cells": n, "minimum_edges": minimum, "passed": True})

    volume_rows = []
    for d in (2, 3):
        for kappa in (0., .05, .5):
            for n in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32):
                e, p = counts(d, n)
                log_b = math.log(3)+2*e*math.log(3/5)-16*kappa*p
                volume_rows.append({"spatial_dimension": d, "n_cells_per_side": n,
                                    "n_vertices_per_side": n+1, "E_links": e, "P_plaquettes": p,
                                    "kappa_lambda_over_alpha": kappa,
                                    "log_bound_Delta_over_alpha": log_b,
                                    "log10_bound_Delta_over_alpha": log_b/math.log(10),
                                    "bound_Delta_over_alpha": math.exp(log_b) if log_b > -740 else 0.,
                                    "bound_underflow": log_b <= -740})
    write_csv(args.out/"volume_scaling.csv", volume_rows)

    convergence = []
    for kappa in (.5, 1., 4.):
        for cutoff in (8, 16, 32, 64):
            vals, residuals = one_square(kappa, cutoff)
            gap = float(vals[1]-vals[0])
            assert gap >= 3-kappa-1e-10
            convergence.append({"kappa": kappa, "cutoff_n": cutoff,
                                "matrix_dimension": cutoff+1,
                                "E0_over_alpha": float(vals[0]), "E1_over_alpha": float(vals[1]),
                                "gap_over_alpha": gap,
                                "omitted_component_residual0": float(residuals[0]),
                                "omitted_component_residual1": float(residuals[1])})
    write_csv(args.out/"one_square_convergence.csv", convergence)
    benchmark_gap = next(row["gap_over_alpha"] for row in convergence
                         if row["kappa"] == .5 and row["cutoff_n"] == 64)
    tensor_rows = []
    for q in (1, 2, 3, 4, 8, 16, 32, 64, 128):
        kappa = .5
        # Reduced one-square heat time t=1: exp(-K) = exp(-4C).
        log_b = math.log(3)+2*q*math.log(3/5)-4*kappa*q
        # Independent round-11 two-square blocks at kappa1=kappa2=.25.
        log_b_two = math.log(3)+2*q*math.log(9/25)-16*q*.5/3
        tensor_rows.append({"q_independent_copies": q, "one_square_kappa": kappa,
                            "numerical_one_square_gap_over_alpha": benchmark_gap,
                            "analytic_tensor_gap_lower_bound_over_alpha": 2.5,
                            "global_one_square_comparison_over_alpha": math.exp(log_b),
                            "global_one_square_log10_comparison": log_b/math.log(10),
                            "two_square_kappa1": .25, "two_square_kappa2": .25,
                            "global_two_square_comparison_over_alpha": math.exp(log_b_two),
                            "global_two_square_log10_comparison": log_b_two/math.log(10)})
    write_csv(args.out/"tensor_counterbenchmark.csv", tensor_rows)
    # Independent Kronecker-sum spectral check in small finite spaces.
    diag = np.arange(6, dtype=float)*(np.arange(6, dtype=float)+2)+.5
    h = np.diag(diag)+np.diag(np.full(5, -.25), 1)+np.diag(np.full(5, -.25), -1)
    gap_small = np.diff(np.linalg.eigvalsh(h)[:2])[0]
    for q in (2, 3):
        hsum = np.zeros((6**q, 6**q))
        for location in range(q):
            term = np.array([[1.]])
            for factor in range(q):
                term = np.kron(term, h if factor == location else np.eye(6))
            hsum += term
        vals = np.linalg.eigvalsh(hsum)
        err = abs((vals[1]-vals[0])-gap_small)
        assert err < 1e-10
        checks.append({"check": "kronecker_sum_gap", "q": q,
                       "absolute_error": float(err), "passed": True})

    # Probe exact polynomial obstruction to an exponential Wilson ground state.
    obstruction_rows = []
    for kappa in (.5, 1., 4.):
        theta = kappa/3  # cancels x term, but leaves theta^2 x^2.
        assert theta*theta > 0
        obstruction_rows.append({"kappa": kappa, "theta": theta,
                                 "constant_coefficient": kappa-theta*theta,
                                 "x_coefficient": 3*theta-kappa,
                                 "x_squared_coefficient": theta*theta})
    write_csv(args.out/"gibbs_groundstate_obstruction.csv", obstruction_rows)

    scale_rows = []
    # A declared dimensionless diagnostic trajectory, not a computed YM running coupling.
    for a in (1., .5, .25, .125, .0625):
        g2 = 1/(1+math.log(1/a))
        n = round(1/a)
        e, p = counts(3, n)
        kappa = 4/(g2*g2)
        alpha = g2/(2*a)
        lam = 2/(g2*a)
        log_a_b = math.log(a*3*alpha)+2*e*math.log(3/5)-16*kappa*p
        assert abs(lam/alpha-kappa) < 1e-10
        scale_rows.append({"a_in_reference_length_units": a, "L_reference": 1.,
                           "n_cells": n, "gH_squared_diagnostic": g2,
                           "alpha_reference_energy": alpha, "lambda_reference_energy": lam,
                           "kappa": kappa, "E_links": e, "P_plaquettes": p,
                           "log10_a_times_gap_bound": log_a_b/math.log(10),
                           "illustrative_target_a_m_for_m1": a})
    write_csv(args.out/"spacing_dictionary_diagnostic.csv", scale_rows)

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "savefig.dpi": 180})
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3), constrained_layout=True)
    for d, style in ((2, "-"), (3, "--")):
        rows = [r for r in volume_rows if r["spatial_dimension"] == d and r["kappa_lambda_over_alpha"] == .05
                and r["n_cells_per_side"] <= 8]
        axes[0].plot([r["n_cells_per_side"] for r in rows],
                     [r["log10_bound_Delta_over_alpha"] for r in rows], style,
                     marker="o", label=f"Spatial dimension {d}, κ = 0.05")
    axes[0].set(xlabel="Cells per side n", ylabel="log₁₀(lower bound / α)",
                title="Global comparison on connected boxes")
    axes[0].legend(frameon=False)
    qs = [r["q_independent_copies"] for r in tensor_rows if r["q_independent_copies"] <= 32]
    axes[1].plot(qs, [math.log10(benchmark_gap)]*len(qs), "-", lw=2,
                 label="Exact tensor identity; numerical one-copy gap")
    axes[1].plot(qs, [math.log10(2.5)]*len(qs), ":", color="black",
                 label="Analytic uniform lower bound = 2.5 α")
    axes[1].plot(qs, [r["global_one_square_log10_comparison"] for r in tensor_rows
                     if r["q_independent_copies"] <= 32], "--", marker="o",
                 label="Global comparison lower bound")
    axes[1].set(xlabel="Independent one-square copies q (κ = 0.5)",
                ylabel="log₁₀(gap or lower bound / α)", title="Counterbenchmark: gap stays positive")
    axes[1].legend(frameon=False, fontsize=8, loc="lower left")
    for ax in axes:
        ax.grid(axis="y", alpha=.2)
    fig.savefig(args.out/"volume_counterbenchmark.png")
    fig.savefig(args.out/"volume_counterbenchmark.svg")
    plt.close(fig)

    summary = {"all_checks_passed": True, "checks": checks,
               "one_square_kappa_half_numerical_gap": benchmark_gap,
               "one_square_kappa_half_analytic_gap_lower_bound": 2.5,
               "numerical_eigenvalues_are_certified": False,
               "tensor_gap_identity_is_exact_mathematics": True,
               "underflow_policy": "Store log bounds and mark displayed zeros as numerical underflow.",
               "scope": "Pure gauge finite graphs and disconnected tensor counterbenchmark; no continuum result."}
    (args.out/"checks.json").write_text(json.dumps(summary, indent=2)+"\n")
    files = sorted(p for p in args.out.iterdir() if p.is_file() and p.name != "SHA256SUMS.json")
    (args.out/"SHA256SUMS.json").write_text(json.dumps({p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                                        for p in files}, indent=2)+"\n")
    print(json.dumps({"all_checks_passed": True,
                      "one_square_kappa_half_gap": benchmark_gap,
                      "output": str(args.out.resolve()), "n_checks": len(checks)}, indent=2))


if __name__ == "__main__":
    main()
