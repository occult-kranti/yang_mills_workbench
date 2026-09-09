# Independent round-11 review

Read `REVIEW.md` for the verdict, mathematical scope, reviewed hashes, failures, and execution counts. `SHA256SUMS.json` binds the delivered reviewer files. The review is for the finite two-square graph and does not certify a continuum theory.

## Portable replay

Run from this directory. The delivered project is expected to place its production code in `../solver`; replace that path with the actual solver directory when necessary. Python requires NumPy, SciPy and Matplotlib for production imports and dynamics. The standalone identity probe uses only the standard library.

```bash
python -O independent_checks.py
python audit_solver.py ../solver/two_plaquette.py --label replay_normal
python -O audit_solver.py ../solver/two_plaquette.py --label replay_optimized
python -O source_mutations.py ../solver/two_plaquette.py
python -O reproduce_initial_failures.py
python -O audit_dynamics.py ../solver
```

`audit_solver.py` reads the supplied solver. It writes its result in this reviewer directory. The source-mutation runner creates deliberately wrong copies under `source_mutants/` and leaves the supplied source unchanged. The initial-failure reproducer must report `expected-initial-defects-reproduced`; it is testing historical defects, not the final solver.

**Run the proof audit only in an isolated copied fixture.** It temporarily modifies manifests and scientific inputs to test rejection, then restores them. Do not pass the production project's proof directory. The supplied `proof_probe/` is already a self-contained review fixture; make a fresh disposable copy for each replay:

```bash
python -c "import shutil; shutil.copytree('proof_probe', 'replay_proof_probe')"
python -O audit_proof_routes.py replay_proof_probe
```

Use a new destination name if `replay_proof_probe` already exists. The copied fixture uses exact relative paths and needs no network, credentials or original workspace location.

## Evidence

| File | Purpose |
|---|---|
| `independent_results.json` | 248 exact unreduced-link, quotient-moment and wrong-model gates |
| `final_normal_results.json`, `final_optimized_results.json` | 495 final exact-solver audit gates in each Python mode |
| `source_mutation_results.json` | Three wrong production-source clones rejected |
| `dynamic_audit_results.json` | 16 checks including independent monomial RK45 evolution |
| `proof_audit_results.json` | 30 provenance, arithmetic, coverage and typed-route checks |
| `initial_failures.json` | Reproduced exactness, precision and metadata defects |
| `initial_audit_results.json` | Historical earlier audit before the additional held-out challenges |
| `review_scope.json` | Reviewed source hashes and per-function line ranges |

`initial_precision_solver.py`, `source_mutants/`, and the schema mutation inside the proof fixture are intentionally incorrect historical or adversarial controls. They are not production alternatives. Gate counts overlap in coverage and should not be summed as independent scientific facts.
