#!/usr/bin/env python3
"""Command-line driver for the round-three backreaction experiments."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import asdict, replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "code"))
from backreaction import Params, SolverFailure, run, source_hash, write_csv


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"


def one(name: str, p: Params, *, modes: bool = False, gauge: bool = False):
    started = time.perf_counter()
    result = run(p, return_modes=modes, gauge_check=gauge)
    elapsed = time.perf_counter() - started
    result["experiment"] = name
    result["provenance"]["wall_seconds"] = elapsed
    result["provenance"]["solver_sha256"] = source_hash()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    write_csv(result, OUT / f"{name}.csv")
    print(json.dumps({"experiment": name, "seconds": elapsed,
                      **result["diagnostics"]}, sort_keys=True))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment", choices=("baseline", "quick", "convergence", "control", "all"), default="baseline")
    ap.add_argument("--ncut", type=int)
    ap.add_argument("--nk", type=int)
    ap.add_argument("--kmax", type=float)
    ap.add_argument("--tfinal", type=float)
    ap.add_argument("--sample-count", type=int)
    ap.add_argument("--rtol", type=float)
    ap.add_argument("--atol", type=float)
    ap.add_argument("--max-step", type=float)
    ap.add_argument("--b", type=float)
    ap.add_argument("--target-e", type=float)
    ap.add_argument("--tpump", type=float)
    ap.add_argument("--a0", type=float, default=0.0)
    ap.add_argument("--modes", action="store_true")
    ap.add_argument("--gauge-check", action="store_true")
    args = ap.parse_args()

    base = Params(a0=args.a0)
    for key, value in (("ncut", args.ncut), ("nK", args.nk), ("Kmax", args.kmax),
                       ("tfinal", args.tfinal), ("sample_count", args.sample_count),
                       ("rtol", args.rtol), ("atol", args.atol), ("max_step", args.max_step),
                       ("b", args.b), ("target_E", args.target_e), ("Tpump", args.tpump)):
        if value is not None:
            base = replace(base, **{key: value})

    if args.experiment in {"baseline", "quick"}:
        if args.experiment == "quick":
            base = replace(base, ncut=3, nK=64, Kmax=20.0, tfinal=12.0,
                           sample_count=241, max_step=.08)
        one(args.experiment, base, modes=args.modes, gauge=args.gauge_check)
    elif args.experiment == "control":
        # Explicitly labelled diagnostics, useful for assessing subtraction
        # sensitivity; no control is silently substituted for matched closure.
        for mode in ("matched", "unrenormalized", "omitted_matching", "sign_reversed"):
            one(f"control_{mode}", replace(base, chi_mode=mode), modes=args.modes)
    elif args.experiment == "convergence":
        # Vary one numerical axis at a time, keeping the others fixed.
        cases = [
            ("ncut6", replace(base, ncut=6)), ("ncut8", replace(base, ncut=8)),
            ("ncut10", replace(base, ncut=10)),
            ("nk128", replace(base, nK=128)), ("nk256", replace(base, nK=256)),
            ("nk512", replace(base, nK=512)),
            ("window20", replace(base, Kmax=20.0)), ("window40", replace(base, Kmax=40.0)),
            ("window60", replace(base, Kmax=60.0)),
            ("tol1e-7", replace(base, rtol=1e-7, atol=1e-9)),
            ("tol2e-8", replace(base, rtol=2e-8, atol=2e-10)),
            ("tol2e-9", replace(base, rtol=2e-9, atol=2e-11)),
        ]
        rows = []
        for name, params in cases:
            result = one(name, params)
            rows.append({"case": name, **asdict(params), **result["diagnostics"],
                         "seconds": result["provenance"]["wall_seconds"]})
        (OUT / "convergence.json").write_text(json.dumps(rows, indent=2) + "\n")
        fields = list(rows[0])
        with (OUT / "convergence.csv").open("w") as f:
            f.write(",".join(fields) + "\n")
            for row in rows:
                f.write(",".join(str(row[k]) for k in fields) + "\n")
    else:  # all: compact reproducible suite; callers can use explicit modes above.
        one("baseline", base, modes=args.modes, gauge=args.gauge_check)
        one("control_unrenormalized", replace(base, chi_mode="unrenormalized"))
        one("control_omitted_matching", replace(base, chi_mode="omitted_matching"))
        one("control_sign_reversed", replace(base, chi_mode="sign_reversed"))


if __name__ == "__main__":
    try:
        main()
    except SolverFailure as exc:
        raise SystemExit(f"ROUND3 SOLVER FAILURE: {exc}")
