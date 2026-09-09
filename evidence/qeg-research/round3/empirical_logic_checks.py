"""Executable counterexamples to four source-level inferences.

These are mathematical and simulated measurement checks, not hardware tests.
Run from the repository workspace with:
  PYTHONPATH=qeg-research/vendor-python python3 qeg-research/round3/empirical_logic_checks.py
An ordinary installation of numpy, scipy and sympy also works without PYTHONPATH.
"""

from __future__ import annotations

import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as sp


def action_counterexample():
    t, duration, mass = sp.symbols("t duration mass", positive=True)
    eps, velocity, offset = sp.symbols("eps velocity offset", real=True)
    variation = t * (duration - t)
    trajectory = velocity * t + eps * variation
    lagrangian = mass * sp.diff(trajectory, t) ** 2 / 2 - offset
    first_variation = sp.simplify(
        sp.integrate(sp.diff(lagrangian, eps).subs(eps, 0), (t, 0, duration))
    )
    ordinary_derivative = sp.diff(offset * t, t)
    euler_lagrange = sp.diff(mass * sp.diff(trajectory, t), t).subs(eps, 0)
    residuals = {
        "variation_at_initial_endpoint": variation.subs(t, 0),
        "variation_at_final_endpoint": variation.subs(t, duration),
        "first_variation_of_action": first_variation,
        "euler_lagrange_residual": euler_lagrange,
    }
    assert all(sp.simplify(value) == 0 for value in residuals.values())
    assert ordinary_derivative == offset
    assert (mass * velocity ** 2 / 2 + offset).subs({mass: 2, velocity: 3, offset: -9}) == 0
    return {
        "source": "E15, US11511891B2, Theory of Operation Eqs.1-5",
        "model": "Free particle in a constant potential, fixed-endpoint variations",
        "trajectory_family": str(trajectory),
        "lagrangian": str(lagrangian),
        "symbolic_residuals": {key: str(value) for key, value in residuals.items()},
        "d_Ut_dt": str(ordinary_derivative),
        "example_parameters": {"mass": 2.0, "velocity": 3.0, "duration": 5.0, "offset": -9.0},
        "example_stationary_action_first_variation": 0.0,
        "example_d_Ut_dt": -9.0,
        "example_total_energy": 0.0,
        "conclusion": "Stationary action does not imply d(Ut)=0.",
        "scope": "Invalidates the stated inference, not every claimed instrument observation.",
        "passed": True,
    }


def isolated_coulomb_check():
    # Scaled units: Coulomb constant is one. All three charges are included.
    coordinates = sp.symbols("x0 x1 x2", real=True)
    shift = sp.symbols("shift", real=True)
    charges = (sp.Integer(1), sp.Integer(2), sp.Integer(-3))
    # Domain x0<x1<x2, so distances have an unambiguous exact algebraic form.
    energy = sum(
        charges[i] * charges[j] / (coordinates[j] - coordinates[i])
        for i in range(3) for j in range(i + 1, 3)
    )
    force_from_energy = [-sp.diff(energy, x) for x in coordinates]
    translated = energy.subs({x: x + shift for x in coordinates}, simultaneous=True)
    translation_residual = sp.simplify(translated - energy)
    points = (sp.Integer(0), sp.Integer(1), sp.Integer(3))
    evaluated = [sp.simplify(f.subs(dict(zip(coordinates, points)))) for f in force_from_energy]
    # Independent direct Coulomb expression, rather than differentiated energy.
    direct = [
        sp.simplify(sum(charges[i] * charges[j] * (points[i] - points[j]) /
                        abs(points[i] - points[j]) ** 3
                        for j in range(3) if j != i))
        for i in range(3)
    ]
    assert translation_residual == 0
    assert sp.simplify(sum(force_from_energy)) == 0
    assert evaluated == direct
    assert sum(evaluated) == 0 and evaluated[0] != 0
    return {
        "source": "E15; independent whole-system conservation comparator",
        "units": "Scaled electrostatic units with Coulomb constant=1",
        "charges": [int(q) for q in charges],
        "positions": [int(x) for x in points],
        "boundary": "Isolated finite charge collection; no external field",
        "potential_energy": str(energy),
        "force_from_energy": [str(f) for f in evaluated],
        "direct_pairwise_force": [str(f) for f in direct],
        "translation_energy_residual": str(translation_residual),
        "total_force": str(sum(evaluated)),
        "force_if_only_first_member_counted": str(evaluated[0]),
        "conclusion": "A nonzero force on a selected member is compatible with zero total force.",
        "scope": "Static isolated Coulomb system; not a finite-element reconstruction of the patent apparatus.",
        "passed": True,
    }


def cavity_energy_check():
    time, power, decay = sp.symbols("time power decay", positive=True)
    energy = power / decay * (1 - sp.exp(-decay * time))
    symbolic_residual = sp.simplify(sp.diff(energy, time) - power + decay * energy)
    assert symbolic_residual == 0
    sample_times = np.array([0.0, 0.1, 1.0, 3.0, 10.0, 30.0])
    # Nondimensional u=decay*time, y=decay*U/power avoids physical stiffness.
    solution = solve_ivp(lambda u, y: 1.0 - y, (0.0, 30.0), [0.0],
                         method="DOP853", rtol=1e-12, atol=1e-14,
                         t_eval=sample_times)
    assert solution.success
    reference = -np.expm1(-sample_times)
    max_error = float(np.max(np.abs(solution.y[0] - reference)))
    assert max_error < 2e-11
    p_watt, frequency_hz, q_cavity, observation_s = 1000.0, 1e10, 2 * np.pi * 1e5, 1000.0
    omega = 2 * np.pi * frequency_hz
    loss_rate = omega / q_cavity
    stored_energy = p_watt / loss_rate
    report_effective_energy = p_watt * observation_s * q_cavity / (2 * np.pi)
    return {
        "source": "E09, DIA report Section2.2.3 Eq.7, compared with mode energy balance",
        "model": "Constant power deposited in one lossy mode; initially empty",
        "power_convention": "Deposited power; coupling/reflection factors required for a generator rating",
        "equation": "dU/dt=P_deposited-(omega/Q_cavity)*U",
        "symbolic_solution_residual": str(symbolic_residual),
        "parameters": {"deposited_power_watt": p_watt, "frequency_hz": frequency_hz,
                       "cavity_Q": float(q_cavity), "observation_s": observation_s},
        "ring_up_time_s": float(1 / loss_rate),
        "steady_stored_energy_joule": float(stored_energy),
        "report_effective_energy_expression_joule": float(report_effective_energy),
        "ratio_if_effective_energy_is_interpreted_as_stored_energy": float(report_effective_energy / stored_energy),
        "dimensionless_time_samples": sample_times.tolist(),
        "numerical_normalized_energy": solution.y[0].tolist(),
        "analytic_normalized_energy": reference.tolist(),
        "maximum_normalized_ode_error": max_error,
        "conclusion": "Physical stored energy saturates; observation duration cannot be repeatedly counted as stored energy.",
        "scope": "Rejects a stored-energy interpretation. Does not derive the full proposed detector sensitivity or rule out every effective estimator definition.",
        "passed": True,
    }


def balanced_detection_check():
    rng = np.random.default_rng(831704)
    trials = 200_000
    signal_photons = 2.0
    phase = 0.0
    rows = []
    for oscillator_photons in [0.02, 0.2, 2.0, 20.0, 200.0, 2000.0, 20000.0]:
        total = oscillator_photons + signal_photons
        amplitude = np.sqrt(oscillator_photons * signal_photons) * np.cos(phase)
        means = [0.5 * total + amplitude, 0.5 * total - amplitude]
        assert min(means) >= 0
        counts_plus = rng.poisson(means[0], trials)
        counts_minus = rng.poisson(means[1], trials)
        difference = counts_plus - counts_minus
        observed_mean = float(np.mean(difference))
        observed_variance = float(np.var(difference, ddof=1))
        exact_mean, exact_variance = float(2 * amplitude), float(total)
        mean_se = np.sqrt(exact_variance / trials)
        # Independent Poisson difference is Skellam; kappa4=variance.
        fourth_central_moment = exact_variance + 3 * exact_variance ** 2
        variance_se = np.sqrt((fourth_central_moment - (trials - 3) / (trials - 1) *
                               exact_variance ** 2) / trials)
        mean_z = (observed_mean - exact_mean) / mean_se
        variance_z = (observed_variance - exact_variance) / variance_se
        assert abs(mean_z) < 6 and abs(variance_z) < 6
        rows.append({
            "local_oscillator_photons": oscillator_photons,
            "output_poisson_means": [float(x) for x in means],
            "mean_difference_exact": exact_mean,
            "mean_difference_simulated": observed_mean,
            "variance_difference_exact": exact_variance,
            "variance_difference_simulated": observed_variance,
            "mean_error_in_standard_errors": float(mean_z),
            "variance_error_in_standard_errors": float(variance_z),
            "snr_exact": float(exact_mean / np.sqrt(exact_variance)),
            "snr_simulated": float(observed_mean / np.sqrt(observed_variance)),
        })
    assert all(a["snr_exact"] < b["snr_exact"] for a, b in zip(rows, rows[1:]))
    limit = float(2 * np.sqrt(signal_photons))
    assert rows[-1]["snr_exact"] < limit
    return {
        "source": "E09/E11 motivate the question; this is an independently defined detector model",
        "model": "Ideal balanced detection of two coherent modes; independent Poisson outputs",
        "seed": 831704, "trials_per_setting": trials,
        "signal_photons": signal_photons, "phase_radian": phase,
        "statistical_check": "Mean and unbiased variance agree within6analytic standard errors at each fixed setting",
        "snr_large_local_oscillator_limit": limit,
        "rows": rows,
        "conclusion": "At fixed signal, increasing coherent local-oscillator power yields finite SNR rather than noiseless unbounded gain.",
        "scope": "Simulated ideal coherent detector, not a complete Li-Baker geometry, squeezed-state calculation, or hardware experiment.",
        "passed": True,
    }


def main():
    checks = {
        "action_variation_counterexample": action_counterexample(),
        "isolated_electrostatic_force": isolated_coulomb_check(),
        "cavity_energy_accounting": cavity_energy_check(),
        "coherent_balanced_detection": balanced_detection_check(),
    }
    result = {
        "kind": "Executed mathematical and simulated measurement checks",
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "sympy": sp.__version__},
        "number_of_check_groups": len(checks),
        "all_passed": all(c["passed"] for c in checks.values()),
        "checks": checks,
    }
    destination = Path(__file__).with_name("empirical_logic_results.json")
    destination.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"all_passed": result["all_passed"],
                      "groups": len(checks),
                      "cavity_ode_error": checks["cavity_energy_accounting"]["maximum_normalized_ode_error"],
                      "output": str(destination)}, indent=2))


if __name__ == "__main__":
    main()
