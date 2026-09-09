# Round 6 advisor plan: use skepticism to choose the next theorem

9 September 2026. This plan is attached to `extensions.md` and the frozen `advisor_experiment_contract.md`. The selected work is a finite, auditable extension of the existing model. An objection is resolved by a proof, a corrected statement or a retained failure, never by treating agent agreement as scientific evidence.

## Executive decision and homepage copy

**Plain-language summary.** We have a carefully defined small model of an electric field interacting with finitely many quantum modes. Previous work established a work-conservation law, a bounded electric field and finite-time causal response under explicit assumptions. This round asks whether the same mathematical safety margin survives when the model includes more modes. It does when more Landau levels are added at a fixed momentum window, and it fails as a uniform argument when both cutoffs are removed under the unchanged matching. We also derived a positive response energy at an exact stationary vacuum; it controls the electric response but leaves a clear secular counterexample for other tangent coordinates.

**What is newly established in the mathematical model.** An exact reference integral and its maximizer; a stronger fixed-window coefficient certificate; a coefficient-only convergence estimate; a conditional obstruction to joint cutoff removal; and a stationary-vacuum response-energy identity. These results strengthen some branches and close off an invalid broader claim. They are not a derivation of physical continuum QED or gravity.

**What is still being worked on.** A common curved-space current/stress construction, admissible state family, compatible counterterms, fluctuation observables and a constrained gravitational evolution. The new obstruction increases the priority of this shared renormalization work. The existing Bianchi Ward-defect identity tells us how a conservation failure would spoil the gravitational constraint, but does not calculate the missing quantum stress.

**What “verified” means.** Each result has separate labels: hand-derived mathematics, independent skeptical review, exact symbolic/rational checks, finite numerical reference tests, or open physical applicability. A checked small calculation does not certify every line of the project, every theorem in the literature or a continuum limit.

## Stable claim registry

| ID | Claim | Exact scope | Current decision | Objection that remains visible |
|---|---|---|---|---|
| R6-L1 | Exact coefficient integral; unique maximum at a=0 | Continuous momentum integral on a centered finite window; finite Landau sum | Analytically accepted; numerical reference gates tracked separately | Finite Gauss nodes can have their largest coefficient away from zero |
| R6-L2 | Z>3/4 for every finite Landau N at b10,K20 | Positive constant-exact quadrature, unchanged matching | Analytically accepted by advisor and skeptic | Uniform denominator does not prove trajectory or current convergence |
| R6-L2-tail | Uniform convergence of the coefficient series at fixed K | Nested fixed per-level coefficients; tail bound in L10a | Analytically accepted | Does not cover replacement of earlier quadratures or any dynamical limit |
| R6-L3 | No uniform positive denominator for cofinal K,N removal | Exact momentum integral; fixed b,e²,χ_b; unmodified explicit finite closure | Analytically accepted as a negative result | A differently organized consistently renormalized current can contain cancellations absent from this coefficient argument |
| R6-L4 | Positive stationary-vacuum response energy | Finite fixed coefficients, Z0>0, pure-state tangent plane; exact vacuum base | Analytically accepted; independent symbolic, matrix and numerical checks executed | The original mode tangent can grow linearly even when this energy stays constant |

The table does not label a selected formula as a discovery in the research literature. It records new results **within this project** relative to round 5. Source review is not a novelty search.

Cross-reference to the skeptic's full project registry: R6-L1 is R6-C08 (`continuum-coefficient`), R6-L2 and its tail corollary are R6-C09 (`fixed-window-extension`), R6-L3 is R6-C10 (`joint-cutoff-obstruction`), and R6-L4 is R6-C11 (`stationary-vacuum-response`). The L identifiers name these derivations; the C identifiers are the site's project-wide claim records.

## Decomposition and bidirectional proof meetings

### R6-L1: replace a sampled extremum with a proof

Forward: positive massive kernel → explicit antiderivative → even coefficient → negative derivative for a>0. Backward: sharp denominator bound → global maximum of C → evenness plus monotonicity. The two directions meet at exact endpoint formulas, rather than at a visually convincing plot. The skeptic's discrete counterexample is admitted as a separate result; no rule transfers the integral maximum to finite quadrature.

### R6-L2: add infinitely many levels to a bound, not to an ODE

Forward: positive weights exact on constants → per-level M^-3 bound → integral-test tail → rational comparison. Backward: finite-model global existence → positive global denominator → uniform upper coefficient bound. The meeting is the explicit rational margin. Each finite-N ODE is covered separately. The coefficient-only series can also be shown uniformly convergent, but a new infinite-dimensional continuation theorem would need its own norm, state domain and bounds.

### R6-L3: test the proposed route by negating its key premise

Forward: exact full-momentum primitive → harmonic Landau sum → divergent coefficient. Backward: extend the positive-energy proof uniformly to both cutoffs → require a positive uniform coefficient margin. The two directions do **not** meet in a proof of that desired extension: they meet in a contradiction to its necessary premise **for this chosen proof route**. The correct outcome is a rejected route and a better problem statement. A path with one cutoff fixed is not a counterexample to the cofinal theorem, because its hypotheses differ.

### R6-L4: find a genuine norm where the first variation failed

Forward: stationary vacuum → transverse tangent plane → completed-square second variation → exact quadratic work identity. Backward: bound electric response → positive conserved quadratic form controlling u → stationary coefficients and tangency. The meeting is `E2'=2uf`. The earlier criticism that signed δW is not a norm remains correct. This new result succeeds because it uses a different quantity under much narrower assumptions, and the secular η example prevents inflation of its conclusion.

These are typed proof decompositions. The project’s Horn planner may record the corresponding implications only after the mathematical review certificates are attached. Backward regression still creates sufficient obligations; it does not reverse implication or turn failure of this route into impossibility of every alternative.

## Role assignments and execution boundary

The advisor owns the mathematical statements, experiment contract and derivations in round 6. The independent skeptic attacks hypotheses, finds counterexamples and runs separate exact checks. The assigned implementation worker writes only new experiment code and output. The parent owns integration, full-code review adjudication, homepage/detail pages and final release. Historical rounds remain immutable evidence.

Each code acceptance must compare independent expressions. L4's primitive is checked against direct quadrature of L1; L13 is checked against a direct finite harmonic sum; L10 uses rational arithmetic; the stationary-vacuum identity uses a weighted-skew matrix check independent of the production tangent RHS. The coarse-grid counterexample must remain in the result ledger even though it fails an overly broad desired conclusion. It is a successful falsification test, not a failed software build to be hidden.

The bounded numerical matrix, input validation, range limits, deliberate wrong-model controls and stopping criteria are in `advisor_experiment_contract.md`. Do not declare a plot verified merely because its generation command returned successfully. Every curve must have raw values, parameters, a source hash and its actual calculation method.

## Next experiments: ordered by proof value, not model size

| Priority | Hypothesis or obligation | Bounded first experiment | Acceptance evidence | Stop or revision trigger |
|---|---|---|---|---|
| 1 | The independent coefficient formulas match the implementation | Frozen E1–E9 matrix and coarse-grid adversaries | Symbolic zero; adaptive-integral agreement; exact rational certificate; discriminating counterexample | Any normalization, level degeneracy, sign or input-domain mismatch |
| 2 | The stationary vacuum provides a trustworthy restricted linear baseline | One-mode matrix, exact weighted-skew identity and matrix-exponential energy comparison | Symbolic identity and numerical conservation, with secular original-coordinate counterexample retained | A bound labeled as pumped or full-state stability |
| 3 | A finite quadrature can receive a rigorous sharper global certificate | Subdivide a bounded a interval and apply derivative/interval bounds; outside it use analytic tail envelopes | Validated upper enclosure for C across all real a, with quadrature coefficients fixed | Sampled maxima treated as rigorous interval enclosures |
| 4 | A common subtraction resolves the apparent cutoff obstruction consistently | First derive finite regulator-dependent current and energy from one common prescription; test exact work/Ward identities before evolution | Same local finite terms in current and stress, independent identity checks and stated physical matching | Adjust χ alone or subtract a divergent plot without rederiving the equations |
| 5 | Quantum directional stress closes the Bianchi interface | Specify a state and a short regular Bianchi interval; calculate J,ρ,p_perp,p_parallel independently | Force Ward identity with apparatus support and the existing constraint-defect response | Define a missing pressure solely to force a residual to zero |

No massive cutoff scan is needed to prove a logarithmic divergence. The next expensive computation should follow a new derivation, not precede it.

## Page and visualization contract for the parent

The homepage should show a detailed status summary with direct links to each solution and its strongest limitation. A visitor should be able to distinguish the selected finite model, the exact continuum-momentum reference, the prospective regulator limit and the missing gravity closure before viewing any plot.

Each detail page should include: plain-language question; exact statement with quantifiers; assumptions; equations and proof meeting; skeptical objection and resolution; executed evidence; remaining counterexamples; and the next research obligation. Keep proposed experiments separate from executed ones. The equation renderer must use actual mathematical notation rather than an image of pseudocode.

Recommended panels are the coefficient reference and coarse-grid counterexample, quadrature error by node count, fixed-window tail bound, and formal logarithmic full-window coefficient. A stationary-vacuum panel may show constant transformed energy alongside a linearly growing original η to explain precisely why “bounded response” needs a named observable. Avoid a green global “QED solved” badge. A counterexample is intellectually useful and deserves the same easy navigation as a positive result.

## Source-reading scope and protocol update

This cycle reuses the exact project equations and prior theorem rather than claiming to reread all physics literature. Fresh primary-source checks target the specific imported identities: NIST DLMF digamma recurrence, positive-axis asymptotic growth, Binet integral and Gaussian quadrature conditions. The new coefficient and response derivations are project algebra, not quotations from those sources. `advisor_sources.json` records reading scope and local source hashes.

The dedicated advisor skill should gain three general rules: separate quadrature refinement from removing physical cutoffs; require proof that a bound survives every claimed regulator limit; and distinguish positivity of a first variation, second variation and transformed norm. The numerical-validation skill should require at least one quadrature aliasing counterexample when a continuous extremum is used to justify a discrete global bound. The parent should own any skill edit and git synchronization; this advisor does not modify shared skills or the Site checkout.

Final promotion requires the independent reviewer and parent to inspect the executed artifacts. Failed or unexecuted gates remain visible. The outcome can legitimately be a stronger local theorem together with a blocked broad claim; this is better evidence, not a reason to force a predetermined conclusion.

## Executed skeptical update

The independent skeptic completed the stationary-vacuum weighted-skew matrix identity and a matrix-exponential comparison at times 0,0.3,1,10. The maximum relative quadratic-energy defect was `2.054431391362439e-14`, below the frozen `5e-13` gate. Their complete suite recorded 46/46 checks, including the exact secular tangent counterexample. These executed checks support promotion of the restricted L4 statement, alongside its mathematical proof.

The advisor's separate review of the first coefficient implementation found seven actionable issues despite its original all-green result: a cofinal-bound factor mismatch, an off-by-one special-function argument, a logarithm label error, catastrophic endpoint cancellation, unstated reference precision, inconsistent potential validation and a symbolic-domain mismatch. `advisor_experiment_review.json` preserves the concrete evidence and the initially observed source hash. The mathematical lemmas are unchanged; revised numerical artifacts must pass the additional checks before release.

**Final numerical decision:** all seven findings are repaired and reviewed; the independent advisor runner passes 29/29 checks against separately constructed high-precision references. The exact coefficient source accepted is `30396dbff23ade9aa7f5bf7e912571ff0e2e2a8029e5e663b65862915ddfc013`. The final implementation results and CSV hashes match that revision. The intermediate fixed-100-digit cancellation failure is retained in the audit, and the final adaptive precision passes its additional `a=10^30` regression. `advisor_experiment_review.md` and its JSON companion record the final bounded acceptance.
