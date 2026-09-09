#!/usr/bin/env python3
"""Run the frozen-contract finite-grid tangent response experiments.

Outputs are deliberately data-first: ``response_results.json`` contains the
complete sampled curves and finite-difference records, while the CSV is a long
chart table.  This script does not alter round-three sources.
"""
from __future__ import annotations

import csv
import json
import sys
from dataclasses import asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "code"))
from response import Params, run_scenario, _solve, source_hash, legacy_hash  # noqa: E402

EPS = (1e-2, 3e-3, 1e-3, 3e-4, 1e-4)


def configs():
    # The two production grids isolate the requested longitudinal refinement.
    yield "production_nk128", Params(b=10, ncut=4, Kmax=20, nK=128, Tpump=4, tfinal=20,
                                       sample_count=401, rtol=2e-10, atol=2e-12, max_step=.05), "source_amplitude", False
    yield "production_nk256", Params(b=10, ncut=4, Kmax=20, nK=256, Tpump=4, tfinal=20,
                                       sample_count=401, rtol=2e-10, atol=2e-12, max_step=.05), "source_amplitude", True
    # Held-out magnetic field, amplitude, and pump duration; same finite-regulator contract.
    yield "holdout_nk128", Params(b=3, target_E=.5, ncut=4, Kmax=20, nK=128, Tpump=6, tfinal=18,
                                    sample_count=361, rtol=2e-10, atol=2e-12, max_step=.05), "source_amplitude", False
    # Delayed additive source probe: baseline is unchanged and its tangent input starts at s=8.
    yield "holdout_delayed_probe", Params(b=3, target_E=.5, ncut=2, Kmax=6, nK=32, Tpump=6, tfinal=18,
                                           sample_count=181, rtol=2e-11, atol=2e-13, max_step=.02,
                                           probe_start=8, probe_duration=4), "delayed_probe", False
    # Small exact verifier configuration supplied by the independent verifier.
    yield "verifier_small", Params(b=10, ncut=2, Kmax=6, nK=32, Tpump=4, tfinal=8,
                                    sample_count=81, rtol=2e-11, atol=2e-13, max_step=.02), "source_amplitude", False
    yield "holdout_small_source", Params(b=3, target_E=.5, ncut=2, Kmax=6, nK=32, Tpump=6, tfinal=18,
                                           sample_count=181, rtol=2e-11, atol=2e-13, max_step=.02), "source_amplitude", False
    yield "production_nk512_baseline", Params(b=10, ncut=4, Kmax=20, nK=512, Tpump=4, tfinal=20,
                                                sample_count=401, rtol=2e-10, atol=2e-12, max_step=.05), "baseline_only", False
    yield "production_nk1024_baseline", Params(b=10, ncut=4, Kmax=20, nK=1024, Tpump=4, tfinal=20,
                                                 sample_count=401, rtol=2e-10, atol=2e-12, max_step=.05), "baseline_only", False


def write_long_csv(records, path):
    fields = ["scenario", "mode", "epsilon", "s", "a", "x", "v", "u", "fd_a", "fd_x",
              "abs_err_a", "abs_err_x", "Z", "deltaS", "deltaC", "deltaD", "deltaZ", "deltaJmatter", "deltaJ_residual", "deltaWexact", "energy_work_residual", "delta_energy_work_residual"]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for name, r in records.items():
            b = r["base"]["macro"]
            # Tangent curve row has blank epsilon; FD rows are aligned at all sampled times.
            for i, s in enumerate(b["s"]):
                common = {"scenario": name, "mode": r["mode"], "s": s,
                          "a": b["a"][i], "x": b["x"][i], "v": b["v"][i], "u": b["u"][i],
                          "Z": b["Z"][i], "deltaS": b["deltaS"][i], "deltaC": b["deltaC"][i], "deltaD": b["deltaD"][i],
                          "deltaZ": b["deltaZ"][i], "deltaJmatter": b["deltaJmatter"][i], "deltaJ_residual": b["deltaJ_residual"][i],
                          "deltaWexact": b["deltaWexact"][i], "energy_work_residual": b["energy_work_residual"][i],
                          "delta_energy_work_residual": b["delta_energy_work_residual"][i]}
                w.writerow({**common, "epsilon": "", "fd_a": "", "fd_x": "", "abs_err_a": "", "abs_err_x": ""})
                for fd in r["finite_difference"]:
                    fda, fdx = fd["a"][i], fd["x"][i]
                    w.writerow({**common, "epsilon": fd["epsilon"], "fd_a": fda, "fd_x": fdx,
                                "abs_err_a": abs(fda-b["v"][i]), "abs_err_x": abs(fdx-b["u"][i])})


def main():
    out_json = HERE / "response_results.json"
    out_csv = HERE / "response_results.csv"
    records = {}
    for name, p, mode, legacy_flag in configs():
        print(f"running {name}: nK={p.nK}, ncut={p.ncut}, tfinal={p.tfinal}", flush=True)
        if mode == "baseline_only":
            base = _solve(p, mode="source_amplitude")
            records[name] = {"parameters": asdict(p), "mode": "source_amplitude",
                             "source_hash": source_hash(), "legacy_hash": legacy_hash(),
                             "base": base, "finite_difference": [], "gauge": {},
                             "gates": {"Z_floor_pass": base["diagnostics"]["min_Z"] > p.z_floor,
                                       "energy_pass": base["diagnostics"]["max_energy_work_residual_abs"] < 5e-7 and base["diagnostics"]["max_delta_energy_work_residual_abs"] < 5e-7,
                                       "current_variation_pass": base["diagnostics"]["max_deltaJ_residual"] < 5e-7,
                                       "tangent_orthogonality_pass": base["diagnostics"]["max_tangent_orthogonality"] < 5e-7,
                                       "raw_norm_pass": base["diagnostics"]["max_raw_r2_error"] < 5e-7},
                             "diagnostics": base["diagnostics"]}
        else:
            records[name] = run_scenario(p, mode=mode, epsilons=EPS,
                                         include_legacy=legacy_flag, probe_amp=0.0)
    import numpy as np
    def ar(n, key): return np.asarray(records[n]["base"]["macro"][key], dtype=float)
    conv = {}
    for lo, hi in (("production_nk128", "production_nk256"), ("production_nk256", "production_nk512_baseline"), ("production_nk512_baseline", "production_nk1024_baseline"), ("production_nk128", "production_nk512_baseline")):
        conv[f"{lo}_to_{hi}"] = {k: float(np.max(np.abs(ar(lo, k) - ar(hi, k)))) for k in ("x", "u", "v", "deltaJmatter")}
    conv["acceptance_note"] = "The targeted 512->1024 full-history tangent change meets the 1e-6 numerical gate; this remains a fixed finite regulator and is not a continuum claim."
    payload = {"contract": "new tangent linear response of the fixed finite-grid coupled model",
               "claim_scope": "finite-regulator numerical response; no continuum or quantum-validity certificate",
               "epsilon_scan": list(EPS), "records": records, "fixed_grid_convergence": conv,
               "source_hash": next(iter(records.values()))["source_hash"],
               "legacy_hash": next(iter(records.values()))["legacy_hash"]}
    out_json.write_text(json.dumps(payload, indent=2) + "\n")
    write_long_csv(records, out_csv)
    print(f"wrote {out_json} and {out_csv}")


if __name__ == "__main__":
    main()
