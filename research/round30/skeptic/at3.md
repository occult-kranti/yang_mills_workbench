# AT3 independent skeptical review and three-loop closeout

**Verdict: accept the conditional finite-readout theorem, the reusable evaluators and the declared abstract benchmarks.** Both frozen reports and code packages have been reviewed. No blocking scientific issue remains. Human project author: **Hruday N M (BUNZEEY)**. This is model-agent review with correlated ancestry, not external human peer review. Scientific priority is unverified.

At the frozen `T=128`, `h=1/32`, `N=4096` design, 4097 certified centered Euclidean observations with deterministic absolute error at most `10^-6` give a conditional interval for `I=alpha R`. For exact rational reported data its uniform width is below `1/500`. Properly enclosed arithmetic adds its actual positive-weight interval width. Both executed A/B abstract benchmark outputs meet the width target and remain separated for every allowed sample-error vector. **No actual AQ Euclidean samples or actual AQ inverse-response value were computed.**

## Analytic obligations

The inherited positive support and finite first and second moments justify the nonnegative Laplace integral, its two derivatives and continuity at zero. Tonelli gives `integral_0^T C'' <= u_up`; no third moment is assumed. On every cell the exact Peano kernel is `r(h-r)/2`, whose completed-square form proves nonnegativity and maximum `h²/8` on the entire cell. Two integrations by parts establish the trapezoid excess, including its sign. Summing against the integrated curvature gives `0<=Trap(C)-integral_0^T C<=47/512000`. This is the required global estimate, not an observed-convergence claim or an N-fold pointwise-curvature budget.

The positive gap gives the separate tail `(504/125)exp(-8)`. Trapezoid weights are positive and sum to 128, so deterministic sample errors contribute exactly at most `128*10^-6` on either side. Constant-sign error vectors attain this worst case and reject a root-N shortcut. The accepted interval is `[P_minus-Q-J, P_plus+D_upper+J]`, with distinct quadrature, tail, sample and arithmetic terms. Its units are dimensionless I. Physical `R=I/alpha`, and physical Euclidean duration is `hbar*s/alpha`; an integral in physical time equals hbar R.

## Controlled arithmetic and input APIs

Both directions use exact alternating-series brackets with nonnegative directed rounding and scale reduction. Their degree choices differ. Squaring preserves the enclosure, and the positive interval recurrence encloses every atomic exponential node through index 4096. All 4097 nodes are generated and carry their actual trapezoid weight. The exported CSVs are abstract fixture data, not AQ measurements. My independent implementation uses a shorter alternating bracket, independently rounded fixed-point recurrence and all nodes; its uniform arithmetic-free width bound is approximately `0.001700382190703`, strictly below 0.002.

The two reusable APIs have intentionally different arithmetic contracts:

| Evaluator | Arithmetic input contract | Accepted guarantee |
|---|---|---|
| Forward | Exact rational values or ordered rational bins of arbitrary width | Always reports the conditional enclosure and its actual width verdict; sufficiently wide bins can fail the target. |
| Reverse | Ordered rational bins, each width at most 10^-12, plus stated value-envelope checks | Every accepted bin-width design has uniform width below 0.002, including at most 128 times 10^-12 of arithmetic width. |

I directly called both frozen APIs on the exported reverse CSV data for both fixtures, checked all 4097 indices and exact times, and checked the reverse CSV reader. Both cover the exact benchmark values. Both reject malformed counts, changed grid/cutoff/error contracts, reversed intervals, booleans and nonfinite inputs. The forward API correctly returns an insufficient-width verdict for broad intervals; the reverse API correctly rejects them. Their difference is not a mathematical disagreement. Validating file shape does not certify AQ state provenance, centering or the supplied absolute-error bound.

## Worst-case discrimination and damaging controls

Both directions correctly compare the largest A upper output under all-positive observation errors to the smallest B lower output under all-negative errors. The observed trapezoid can shift by J and its output interval already contains another allowance J. Thus the separation calculation must pay both layers. The reviewed difference exceeds `0.004293`, and my independent all-node implementation agrees. This is a discrimination result for the specified abstract A/B measures, whose exact inverse integrals are 3/32 and 1/10. It is not a determination of the AQ spectrum.

The wrong quadrature sign would exclude the exact benchmark. Tail omission is independently defeated by a slow-support diagnostic; the reverse implementation internally generates an additional abstract tail-control curve preserving mass and first moment. It is not an exported A/B benchmark, not AQ data and not a fourth investigation. The forward version instead bounds a slow-atom control analytically. This required countercontrol work is recorded distinctly from the frozen A/B benchmark production.

An uncentered zero atom produces a constant term with divergent full time integral, so the gap tail bound cannot be applied to it. Short-cutoff and coarse-grid controls fail the uniform width certificate; that does not prove that every actual reconstruction at those settings fails. My independent checker also demonstrates that a bare floating exponential is outside a much tighter exact enclosure and cannot be treated as a zero-error certificate. Floating calculations are used only for that rejecting diagnostic and readable displays, never for admitted bound endpoints.

## Evidence and provenance

The independent mathematical checker passes 64 exact controls and the separate direct-API audit passes 41 controls, each in normal and optimized Python. Producer counts are 95 forward and 48 reverse. Four fresh producer replays reproduce every frozen output byte: manifests, exact certificates and all exported CSVs. Complete file closures, contract/instruction snapshots, hashes, ownership and nonsymlink paths pass. An initial replay rejected an ignored forward interpreter cache. Its owner removed only that unbound cache, leaving the source freeze unchanged; the fresh full replay then passed. All reviewer imports use disabled bytecode generation. This was an environment cleanup, not a changed proof or extra loop.

The review binds both reports and all source/output packages, the contract, its preceding gate, independent controls and API audit, both-mode receipts and the unchanged replay helper. Established trapezoidal quadrature, spectral calculus and moment methods retain their attribution to the checked primary sources. Hruday/HNM labels identify this AQ application and its reusable finite protocol; no new generic quadrature or verified priority is asserted.

## Stop and prospective priorities

Exactly three investigations have now been reviewed: AT1's actual same-state moment/domain result, AT2's certified spectral functionals and information limitation, and AT3's conditional finite-readout tool with abstract benchmarks. No fourth scientific investigation is authorized in this cycle. Replays, repairs, integration, naming, publication and the following planning advice add no research loops.

The next bounded AT deliverable requires **certified actual AQ Euclidean samples**. A source must identify the exact chosen AQ state and centered Wilson observable, physical clock and complete factors; quantify finite-volume/boundary/state errors and representation-cutoff errors; and include solver, arithmetic and any observational errors in the per-node absolute budget. Mere numerical convergence or a successful A/B calculator is insufficient. One certified actual node or a clearly isolated missing estimate would be a reasonable prospective first target; no such computation is executed here.

Preserve AR's quantitative bulk/boundary and state-identification goal because it can support that sample-production obligation. Preserve AS as the major fundamental strategy question: the present small numerical tau regime still misses the declared weak-bare-coupling trajectory, and common clock/energy rescaling does not repair it. Do not rank the easy finite readout as equivalent progress toward the continuum construction. AU's 561-state evaluator and AP's prior-fixed inference remain useful separate-model tasks; their outputs cannot be substituted for AQ samples without a complete matching theorem.

The continuum theory, positive continuum mass gap, all-state uniqueness, AO/AQ identity, physical susceptibility and AQ particle-pole question remain open in this release. Counts of aliases, equations, checks, graph nodes or completed investigations provide no percentage of the Clay problem solved.
