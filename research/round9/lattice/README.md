# Four-dimensional SU(2) Wilson experiment

This package audits an actual finite SU(2) lattice gauge sampler. It does not solve the Yang–Mills mass gap problem.

Requirements: Python 3.10+, NumPy, SciPy. The tested runtime versions are recorded in `results/experiment_manifest.json`.

To reproduce in a fresh copy with no recorded output directory:

```bash
python test_lattice.py
python check_evidence_gate.py
python run_experiments.py
```

The runner deliberately refuses to overwrite a previously recorded manifest. Preserve the supplied `results/` directory and execute a fresh copy containing the source files if a new run is desired. A few minutes of CPU time is expected. Fixed seeds, volume, beta values, warmup, sample counts and decision gates are in `PREDECLARED_CONTRACT.md`. The code also accepts general four-dimensional periodic integer lengths≥2, but only small deterministic oracle tests exercise odd/unequal lengths; the measured ensemble is exactly 2×2×2×2.

Files:

- `su2_lattice.py`: group algebra, full Wilson action, oriented staples, local Metropolis sweeps, gauge/center transforms, exact one-matrix control and strict statistical diagnostics.
- `test_lattice.py`: independent Pauli-matrix action oracle, deterministic checks and nonfinite arithmetic regressions.
- `run_experiments.py`: fixed workload, source hashes, raw outputs and diagnostic aggregation.
- `check_evidence_gate.py`: rejects empty/stale/failed prerequisite records before sampling.
- `MATHEMATICAL_CONTRACT.md`: equations, assumptions, exact identities and blocked continuum implications.
- `results/`: raw sweep and one-matrix CSVs, retained warmup traces, final link configurations, diagnostic JSON, runtime/source hashes.

Interpretation: `consistent` means an exact target lies within the predeclared five estimated standard errors and minimum batching criteria are met. It is a limited diagnostic, not a proof. `insufficient` means uncertainty criteria did not support the comparison; `flagged` means the predeclared comparison detected disagreement. Neither should be converted into a passed gate. Beta-zero Ward output is identically zero and does not validate the sampler by itself.

The delivered current runner includes an evidence-gate repair made after the recorded stochastic experiment. The exact sources used for that experiment remain in `results/executed_sources/`, matching its manifest hashes. The sampler itself is unchanged. Current deterministic validation is separately stored in `results/deterministic_checks_current.json`; the original run evidence remains intact. See `RESULTS.md` for both discovered defects and their chronology.
