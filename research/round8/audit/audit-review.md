# Independent round-7 scientific code audit

Audit date: 9 September 2026. Historical evidence was read without changing it. Proposed corrections and fresh reruns are separate revisions. This audit confirms the published default finite-model trajectories within the executed tolerances, and identifies three additional implementation/validation defects. None of these defects changes the reproduced default equations or establishes a continuum Einstein–QED result.

## Exact reviewed scope

Read in full, line by line at the function/file level:

- `round7/finite_scalar.py`, original lines 1–530.
- `round7/gravity_sim.py`, original lines 1–661.
- `round7/proof_obligations.py`, original lines 1–153.
- `round7/validate_simulations.py`, original lines 1–157.
- `round7/independent_checks.py`, original lines 1–238.
- `round7/validate_proof_plan.py`, original lines 1–40.
- `round6/code/evidence_guard.py`, original lines 1–63.
- `round6/code/coefficient_certificate.py`, original lines 1–68.

Also read the variable contract, search contract, prior implementation audit, round-6 advisor derivation scope, and both requested project skills. Reviewed the historical response comparator's parameter and matching interface and executed it through the g=0 comparison. **Not** a fresh line-by-line review of the entire 425-line response solver, 600-line Horn planner, SciPy/NumPy, every historical round, or the website. Their executed uses are narrower than full source/branch coverage. No claim of formal floating-point verification is made.

## Demonstrated defects and proposed corrections

### S8-C1 — Comparator changes a custom matching coefficient

Location: `finite_scalar.py`, original lines 301–317. The new solver accepts `chi_b`, but `g0_baseline_compare` drops it when constructing historical parameters. With `nK=16`, `ncut=0`, and `chi_b=0.2`, the function says the models were compared and failed, with maximum potential discrepancy **0.09653632660722022** and field discrepancy **0.024135938266560047**. This is a comparison of different models, not evidence that decoupling fails.

The historical solver supports discrete `chi_mode` prescriptions only. The proposed correction maps matched, zero, and sign-reversed matching exactly to supported modes; an arbitrary unavailable coefficient returns `status=unavailable` and the explicit reason. It never silently substitutes a coefficient. A caller requiring this baseline must treat unavailable as blocked. The separate complex-spinor reference remains a suitable comparison route for arbitrary coefficients.

Impact: supported parameter investigations and interpretation of decoupling. The default `chi_b=None` replay was already correct. Regression checks verify all three supported prescriptions and the unavailable arbitrary case.

### S8-C2 — Finite state does not imply finite energy diagnostics

Location: `finite_scalar.py`, original lines 236–273. Integration checks the ODE state for finiteness, but not the subsequently reconstructed quadratic energy and residuals. A legitimate finite affine scalar input, `g=nu=0`, `phi0=y0=1e155`, `target_E=0`, `ncut=0`, `nK=16`, completes with finite state and returns **NaN** for `max_energy_mismatch` and `max_defect_integral_residual`. The floating-point energy overflows although the real-valued affine solution exists.

The proposed correction initializes diagnostics to NaN, requires every populated observable to be finite before energy subtraction, and rechecks the final residual arrays. It raises an explicit `FiniteScalarFailure` for the demonstrated overflow case. This is rejection of an unsupported floating-point scale, not a disproof of the mathematical finite-model theorem.

Impact: callers of `_solve` could otherwise receive unusable diagnostics; tests relying only on `residual > threshold` can also mishandle NaN. The delivered CLI uses strict JSON serialization, which would reject NaN before publishing such a result; this audit does **not** claim an observed false CLI publication. Ordinary macro histories remain exactly unchanged.

### S8-C3 — Gravity result builder claims success before acceptance

Location: `gravity_sim.py`, original lines 549–605. `build_results([])` reports `status=passed` and all seven trajectory gates true because `all([])` is true. With an executed run whose recorded constraint diagnostic is deliberately changed to 1, the same API returns `status=passed` beside a false constraint gate.

The proposed correction rejects empty case collections, evaluates the analytic-fixture and applicable discrimination gates inside the builder, and derives its semantic status from the complete evaluated gate dictionary. The existing CLI independently checks failed gates, so the reproduced full CLI suite was unaffected; the defect is observable at the reusable result-building boundary.

Impact: API integration, future case selectors, and consumers that inspect semantic status. The wrong-model discrimination remains explicitly absent when its fixture is not selected; a nondiscriminating Minkowski-only test is not relabeled a complete physical challenge.

## Reproduced acceptance evidence

| Check | New execution | Scope |
|---|---:|---|
| Original complete finite solver suite | Passed | Declared finite modes, source, scalar, controls, and base quadrature |
| Original complete classical gravity suite | Passed, 8 cases | Regular bounded Bianchi I examples |
| Original independent spinor/root validator | Passed, 47 gates | Includes custom input rejections and selected gauge/physics fixtures |
| Frozen Horn proof planning | Reproduced 17-rule finite and 11-rule gravity routes | Reviewed rule-library inference only |
| Frozen proof rejection/manifest checks | Passed, 6 gates | Changed bound bytes rejected; missing Maxwell and common closure underivable |
| Archived independent checker's numerical branches | Passed, 21 gates | Executed `cutoff_checks` and `numerical_scalar` only |
| Archived independent checker's symbolic branches | **Blocked** | SymPy absent from both advertised Python runtimes |
| Proposed corrected full finite suite | Passed | Same default physical experiment |
| Proposed corrected full gravity suite | Passed, 8 cases | Same default physical experiments |
| Proposed corrected root validator under `python -O` | Passed, 47 gates | Acceptance survives optimized Python |
| New defect/fix regression script | Passed, 13 gates, normal and optimized Python | Deliberate original defects and revised behavior |
| Original versus corrected scientific CSV files | 10 of 10 byte-identical | Confirms unchanged default sampled trajectories and diagnostics |
| New fixed-domain delayed-response node study | 64-node discrepancy fails; 128→256 meets working threshold | Finite-regulator adjacent-grid evidence; full potential/field/scalar responses recorded |

Heterogeneous gate counts are not confidence percentages. The 21 numerical independent checks were executed by removing only the unavailable SymPy import from an in-memory AST and calling its unchanged numerical functions. The archived source bytes remain intact. Neither symbolic branch is counted as newly executed. Conventional algebra was inspected by reading the equations, but that is distinct from a machine symbolic rerun.

Representative fresh numerical results:

- Finite-model correct maximum work residual: **1.528291382335567e-15**.
- Finite omitted-exchange control work discrepancy: **1.9071505293148314e-5**, explained by its integrated defect with residual **8.7809533949601e-16**.
- Base momentum-node refinement, 128 to 256: maximum sampled potential/field difference **4.135270931238111e-7**.
- Maximum correct gravitational constraint residual over eight cases: **7.680488189887313e-15**.
- Coupled wrong-gravity control constraint discrepancy: **3.0216003773448144e-5**.
- Analytic de Sitter and massless-scalar maximum state errors: **5.55e-17** and **3.60e-12**.

## Mathematical and physical verdict

Within the declared finite model, the reviewed work identity, scalar exchange sign, preserved mode norms, and conditional continuation argument remain compatible with the tested code. The original cutoff conditions still matter: positivity for exact positive quadrature coefficients is not automatically a certificate for arbitrary rounded coefficients or a joint regulator limit.

The gravity branch has a complete classical scalar–Maxwell stress and propagates the constraint on an existing regular interval. It does not calculate a Dirac current or quantum directional pressures, and its flux-reduced comparator shares the gravitational RHS. The separately written numerical benchmark and inspected symbolic identities provide additional evidence, rather than erasing that shared-code limitation.

The Horn planner's `proved` string means derivability in the frozen reviewed inference library. Its graph replay does not machine-check the mathematics in cited prose. Withdrawing one certificate blocks that graph route; it is not a theorem that every conceivable physical proof is impossible.

The project remains missing a common causal renormalized current, energy density, directional pressures, admissible state evolution, controlled limit, and fluctuation validity before its finite QED and classical gravity branches can be combined. A regulator-dependent positive coefficient is not a demonstrated elimination of the QED Landau pole, and neither reduced model solves the Yang–Mills mass-gap problem.

## Remaining numerical obligations

The original delayed-response gate varies perturbation size, while its node-refinement gate tests only base potential/field histories. These are different accuracy questions. Its tiny adjacent epsilon differences are not a demonstrated second-order interval and do not by themselves establish response quadrature accuracy. A fresh bounded same-domain response study has now run through `response_grid_audit.py`, with its own result/CSV files; its result is not retroactively attributed to the historical run. It fixes `b=10`, inclusive `ncut=1`, `Kmax=20`, pulse history, probe amplitude 0.15, centered perturbation 5e-5, solver tolerances, and output times. The predeclared working absolute discrepancy scale was 2e-5. Only the longitudinal Gauss-node count changes.

| Response observable | Max difference 64→128 nodes | Max difference 128→256 nodes |
|---|---:|---:|
| Potential a | 1.3856872094208939e-4 | 3.54516416223305e-7 |
| Electric field x | 2.8715392452749455e-4 | 1.389027781684149e-6 |
| Scalar phi | 1.0451861598426149e-7 | 1.1457501614131615e-9 |
| Scalar velocity y | 1.7507717497977637e-7 | 1.7907897387203775e-9 |

The coarse 64-node field/potential responses miss that scale. The 128→256 comparison meets it for all four observables. The predeclared rule would add 512 nodes only if that comparison failed, so no additional extension was needed. This supplies useful new response-grid evidence. It is not a proven quadrature error upper bound, a continuum limit, or a determination of quantum fluctuations.

The gravity quantities named `scaled` use denominators `max(abs(reference),1)`. For sub-unit references these are absolute errors in the chosen unit, **not** relative errors. The independent numerical gravity benchmark includes actual initial-density and nonzero-flux relative diagnostics. Any broad weak-field accuracy claim needs a declared physical scale and suitable tolerances.

Future physics changes need new equations and independent verification. The corrections here only make the implementation's acceptance boundary more reliable.

## Deliverables

`fixed/finite_scalar.py` and `fixed/gravity_sim.py` contain the proposed new source revision. `proposed_corrections.diff` isolates the changes. `regression_audit.py` and `regression_results.json` reproduce the three defect classes and their fixes. `history_comparison.json` records all ten unchanged CSV fingerprints. `replay/` preserves fresh unmodified-source executions; `fixed-replay/` holds the corrected executions. `independent_numerical_subset.json` explicitly records the unexecuted symbolic branches. No historical evidence was overwritten.
