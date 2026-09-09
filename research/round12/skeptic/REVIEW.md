# Round 12 independent review

The bounded review passes for the current source hashes in `acceptance.json`. The exact fixed two-segment computation has an independently replayed total Hilbert-state error below **0.000337501**. This is a finite seven-link graph result.

The physical fixture has alpha=rho=1, degree D=3 and the normalized constant Haar initial state. It applies (lambda1,lambda2)=(1/20,1/10) for one time unit, then (1/10,1/20) for one time unit. Each segment uses the exact order-100 Taylor polynomial. The stored complex coefficients are rational pairs and remain unrenormalized. With e=(114/5)^101/101!, the full error bound is exactly

    27/80000 + 2e + e^2 < 0.000337501.

The representation part is 27/80000, from action A=3/10. The product-of-approximate-steps contribution is 2e+e^2. Both the state and its Haar norm were reconstructed using independent spherical moments, a divergence-form kinetic matrix, an independently inverted Gram matrix, and backward Horner polynomial evaluation. The production solver uses forward term accumulation. Substituting the form matrix for its Gram-correct coordinate operator was independently falsified.

## Executed evidence and attribution

| Audit | Distinct gates | Execution provenance |
|---|---:|---|
| Banded finite models and broken hypotheses | 35 | Previous independent reviewer; retained optimized record |
| Compact identities and defined scalar closure | 76 | Previous independent reviewer; retained optimized record |
| Exact action and certificate input paths | 210 | Previous independent reviewer; normal and optimized records |
| Numerical diagnostic/input comparisons | 23 | Previous independent reviewer; normal and optimized records |
| Exact stored polynomial state | 28 | Final verifier; post-fix normal and optimized runs |
| Frozen proof-wrapper admission | 34 | Final verifier; current normal and optimized runs |

There are **406 distinct recorded gates**. Repeating an audit under optimized Python does not increase this number. The previous reviewer performed the first four audits; the final verifier reviewed their scripts/records and checked their source bindings rather than claiming those executions as new work. `handoff_provenance.json` preserves original hashes and modification timestamps. `source_review.json` records the ten current reviewed files, their hashes, timestamps and review methods.

The final proof-wrapper runs reconstruct arithmetic from checked immutable bytes. Their mutations reject stale/self source, missing inputs, same-byte symlinks, altered dependency roles, wrong stored vectors, normalization metadata changes, changed error claims and a valid certificate attached to the wrong named protocol. Source inspection also checks all eight declared analytic fixtures: protocol kind/duration/both magnetic scales, evaluation time, alpha, rho, initial degree, unique case labels and the degree-3/4 pair set. A frozen-byte replay remains successful after isolated on-disk source corruption, which tests the actual execution path. No production source was mutated by this reviewer.

The positive routes have costs 6 (cosine representation), 12 (fixed exact computed state), 3 (finite-volume comparison), 2 (decaying bound does not imply gap closure), and 3 (defined point-closure rejection). Missing bandwidth, support, absolute action and exact-vector replay block their dependent conclusions. Floating-cosine total error and the four-dimensional target remain not derivable; seeding the unproved final target is rejected.

## Preserved findings and corrections

The initial dependency-manifest symlink acceptance is retained in `initial_drive_audit_results.json`; the corrected source passes 210 independent gates in both Python modes. Initial proof-manifest symlink acceptance is retained in `initial_proof_mutations.json`; the current wrapper rejects that mutation.

The initial volume implementation used assertions that disappeared under optimized Python. `volume_initial_hashes.json` preserves an incorrect-count mutation reported as passed under optimization, together with the historical source and mutant scripts. The final source uses explicit exception guards and matches `volume_final_hash.json`; its production result binds to that corrected source. No additional full volume sweep is claimed by the final verifier.

`initial_exact_step_audit_results.json` preserves the earlier 27-gate exact replay and public API defect: passing a floating state to `norm_squared` returned a float. The certificate constructor itself was unaffected. The corrected helper converts Gram entries and state components with the rational-input parser, validates complex-pair shape, and now returns the exact expected 1/100 for the regression input. Both post-fix independent runs pass 28 gates without defects.

`initial_time_grid_failure.json` retains the caught mismatched-grid diagnostic rather than hiding an unsuccessful comparison. The final numerical audit checks matching times, phases, protocol and shapes and rejects nonfinite transient entries. The previous proof normal report is also retained unchanged; fresh verifier labels bind the new exact-stepper source and certificate.

During source inspection, the final verifier notified the integrator that one production optimized edge-test report still referenced the old exact-stepper source. The integrator regenerated it, and final assembly checked both production edge reports against the current source bytes. Those production checks are not added to independent gate counts. This review's acceptance covers the named independent artifacts and reviewed sources, not deployment or archive contents.

## Mathematical scope

The advisor's bandwidth-one, one-sided Duhamel argument compares full and exact Galerkin evolution in the physical Haar norm with matched phases and initial state. The exact polynomial calculation adds a separately bounded finite-step error. It supplies neither an operator norm for the unbounded full kinetic energy nor a retrospective temporal certificate for floating cosine histories.

The finite-volume comparison retains its explicit link/plaquette dependence. The disconnected tensor counterbenchmark shows that decay of this lower bound does not imply decay of the true gap. It is not a theorem for growing connected lattices. The actual quantum ground-state density is distinct from the tilted Euclidean Gibbs measure; the conditional local curvature, limiting-semigroup, vacuum and observable-density premises remain unproved where stated.

The closure audit rejects the explicitly defined point-concentration replacement on a finite tilted-Haar measure using positive variance and the next identity at zero coupling. The inherited source-formula review has a stated version and convention boundary. The final verifier reviewed its local artifacts and did not conduct a new external literature audit. This does not rule out every scalar ansatz.

These are conventional mathematical reviews with exact arithmetic checks, not proof-assistant formalizations. Continuum construction, reconstruction, nontriviality and a positive four-dimensional Yang-Mills physical mass gap remain unresolved.
