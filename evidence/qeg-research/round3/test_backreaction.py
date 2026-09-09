"""Small executable checks for the round-three production solver."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent / "code"))
from backreaction import Grid, Params, SolverFailure, _initial_state, bump_integral, run


def test_bump_is_normalized():
    assert abs(bump_integral() - 0.007029858406607256) < 2e-14


def test_initial_bloch_vectors_are_unit_and_vacuum_current_zero():
    p = Params(ncut=2, nK=16, Kmax=8.0)
    g = Grid(p)
    y = _initial_state(g, p.a0)
    r = y[2:-1].reshape(3, -1)
    assert np.max(np.abs(np.sum(r*r, axis=0)-1.0)) < 3e-15


def test_small_run_gauge_and_energy_diagnostics():
    p = Params(ncut=2, nK=32, Kmax=6.0, tfinal=8.0, sample_count=81,
               rtol=2e-10, atol=2e-12, max_step=.02)
    out = run(p, gauge_check=True)
    assert out["gauge_check"]["passed"]
    assert out["diagnostics"]["min_Z"] > 0
    assert out["diagnostics"]["max_raw_r2_error"] < 5e-8
    assert out["diagnostics"]["max_energy_work_residual_relative"] < 5e-3


def test_invalid_z_floor_is_rejected_descriptively():
    try:
        run(Params(ncut=1, nK=8, Kmax=2.0, tfinal=5.0, z_floor=2.0))
    except SolverFailure as exc:
        assert "Z" in str(exc)
    else:
        raise AssertionError("expected positive-z-floor validation failure")


if __name__ == "__main__":
    for name in sorted(k for k in globals() if k.startswith("test_")):
        globals()[name]()
        print(name, "ok")
