# Independent reviewer artifacts

`acceptance.json` is the bounded verdict and lists the ten current reviewed source hashes plus six independent reports. `REVIEW.md` explains the result, provenance, corrections and limits. `source_review.json` records source timestamps and review methods. `handoff_provenance.json` identifies files copied unchanged from the earlier reviewer.

The exact finite-graph result uses two duration-one nonnegative segments, (1/20,1/10) then (1/10,1/20), alpha=rho=1, D=3, the constant initial state and exact order-100 polynomials. Its unrenormalized stored vector has total error 27/80000+2e+e^2 < 0.000337501, where e=(114/5)^101/101!.

The previous reviewer supplied `banded_results.json` (35), `closure_results.json` (76), `final_drive_*_results.json` (210) and `final_numerical_*_results.json` (23). The final verifier supplied `verifier_exact_*_results.json` (28) and `verifier_proof_*_results.json` (34). Counts are per distinct gate, not per interpreter run. The older `final_proof_normal_results.json` is preserved handoff evidence and is superseded by fresh verifier proof records for final source binding.

From an extracted round-12 directory with this folder named `skeptic`, reproduce the final independent checks with:

```bash
python -B skeptic/audit_exact_stepper.py solver/exact_stepper.py --label verifier_exact_normal
python -B -O skeptic/audit_exact_stepper.py solver/exact_stepper.py --label verifier_exact_optimized
python -B skeptic/audit_proof_routes.py . --label verifier_proof_normal
python -B -O skeptic/audit_proof_routes.py . --label verifier_proof_optimized
python -B skeptic/finalize_review.py .
```

The exact-state and proof-wrapper auditors use Python standard-library arithmetic and copied independent algebra helpers. The wrapper creates isolated probe directories beside its audit script, copies the declared manifest inputs, and restores its mutation fixtures. It never mutates the supplied round-12 sources. Earlier numerical audits additionally require NumPy/SciPy; volume plotting requires Matplotlib. `-B` avoids writing bytecode into reviewed source directories.

Historical findings remain in the `initial_*` JSON files and volume historical sources/mutants. The integrator also retains earlier failure probe folders in the portable package. Do not replace historical files with passing outputs: use fresh labels when changing an audit or source. Source hashes show identity, not mathematical truth.

Acceptance covers the declared finite claims and exact computation. It does not certify floating cosine total error, all scalar reductions, a growing connected-lattice gap, a four-dimensional continuum result, UI behavior or published package contents.
