---
name: qeg-numerical-validation
description: Verify the project's Maxwell–Dirac and tangent-response computations using exact identities, independent formulations and separate numerical limits. Use when writing or reviewing quantum-field solver code and result claims.
---

## Nonabelian finite-model gates

For driven error certificates, independently reconstruct the absolute integrated drive and factorial order D−d₀+1. Bind the actual protocol, duration, initial degree, norm, cap and coefficient domain. Test signed cancellation, zero terminal leakage with nonzero accumulated error, nonzero initial degree, zero drive/time, an insufficient cutoff and certificate-field mutations. Equal A(T) does not imply equal states. Rational action enclosures and exact truncation bounds do not certify floating state evolution or coefficient conditioning; require separate evidence before reporting total error. Do not infer unbounded-energy accuracy from an L² state bound.

For growing-volume claims, check graph assumptions and distinguish failure of the estimate from closing of the actual gap. Use a tensor counterbenchmark where the exact gap stays fixed. Never identify a Gibbs density with a Hamiltonian ground-state density without testing Hφ/φ. For source formula audits, independently calculate action derivatives and source phases from matrices; assertions about hand-entered fixture constants only verify transcription. Check color-Lorentz rank before contracting full-color identities. Preserve zero-coupling cases in which the first moment identity is blind to a false closure.

For coupled plaquettes, independently compute link derivatives before checking the quotient operator. Exact generalized eigenvalue counts use H-rG, including zero pivots and repeated levels. Reject Boolean substitutions in integer inertia counts or semantic status, nonpositive requested precision, and approximate-zero pivot rules. Verify that rational division remains rational. Bind the stationary collection's outer schema as well as individual certificates. Execute reviewed source bytes for a frozen replay; hashing a file after importing another version does not establish that the imported implementation was checked. Run proof mutations in an isolated copy. Compare finite dynamics against an independent raw-monomial implementation with the correct Haar norm, and report representation differences separately from time-integration errors.

For exact spectral certificates, reconstruct rational matrices from the declared Hamiltonian. Bind physical scope, representation dimension, precision and semantic status as well as eigenvalue endpoints. Test exact-eigenvalue endpoints, zero pivots, zero offdiagonal, rational scaling and insufficient absolute precision. Independently check Sturm counts with a different exact congruence/inertia algorithm. Floating Mathieu and radial-grid comparisons are independent numerical oracles, not exact certificates.

Continuous-range certificates must verify all point-parameter matches, exact interval endpoints, coverage without holes, the stated Lipschitz constant and the final minimum margin. A missing center or wrong alpha cannot pass. Hash both theorem source and arithmetic evidence before admitting a proof-planner seed.

The provenance verifier must require the complete expected set of input hashes. Looping over whichever hashes happen to be present lets an empty or incomplete manifest pass. Validate digest syntax and input paths, reject escaped or substituted symlink inputs, then hash the actual bytes.

For a time-dependent coupling, integrate its Hamiltonian work rate separately from endpoint energy. Every independent evolution method must enforce its own promised work and norm checks; recording a residual without including it in acceptance is a defect. Stationary representation-tail certificates do not imply a certified time-dependent truncation bound.

For the Yang–Mills branch, use the advisor's `references/yang-mills-contract.md`. Audit quaternion arithmetic against independent complex matrices, local increments against full plaquette sums, and Lie derivatives against global-action perturbations. Include extent-two periodic geometry, rectangular geometry, gauge transformations, center seams, omitted daggers and coupling-factor mutations. Reject extent-one geometry unless repeated-link derivatives are explicitly implemented.

Report stochastic consistency separately from deterministic correctness and equilibrium. Preserve seeds, starts, warmup, raw histories, block uncertainty, predeclared thresholds and insufficient outcomes. Check derived statistics for finiteness even when every input is finite. Acceptance gates must survive `python -O`; ordinary assert statements are not sufficient for production validation.

For SU(2) spectra, independently check Haar integration including its sine-squared measure and representation-dimension factor. Use scaled Bessel evaluation and stable logarithms, with explicit beta-zero projection and negative-beta domain controls. Physical energy requires a time scale. For transfer-stability experiments use independent diagonal saturation fixtures and prove the shared-vacuum premise before comparing spectral gaps.

# Numerical validation for this research project

Use the current advisor-approved equation contract. The [response contract](references/response-contract.md) supplies the tangent system, preparation and identities; do not infer its equations from a chart.

## High-value checks

- Freeze the source hash before the run and record it in the output. Check that the delivered file, data and report refer to the same source.
- Initialize unevaluated diagnostic arrays to NaN, or use an equivalent completeness check. Refuse a pass if a promised diagnostic was never populated.
- Compute the subtracted mode integrand before summation when cancellation warrants it. Preserve any historical legacy comparison as a distinct source.
- Distinguish the effective Maxwell numerator from full matter current. For fixed matching, the tangent physical current uses the derivative of the electric response, not the response amplitude itself.
- Integrate external work and its perturbation alongside the state. Test the exact discrete current/energy identities and raw norm/tangent orthogonality without clipping or forced normalization.
- Check the physical preparation: amplitude perturbations of a smooth source start with zero state perturbation; a pure gauge shift moves the canonical nodes and potential together.

## Convergence and falsification

Hold the physical problem fixed while varying each numerical axis. A larger momentum window with unchanged central spacing does not replace quadrature refinement. A response derivative may converge much more slowly than the base field. Centered finite differences need a truncation-dominated second-order interval before roundoff or solver error plateaus.

Use independent complex spinors or another nonshared formulation to challenge production Bloch dynamics. Match their regulator and preparation before interpreting disagreement. Test deliberately missing polarization/coherence terms against a declared nondegenerate case. A wrong-model test must actually produce a distinguishable defect.

Report field, current and energy discrepancies separately. A global physical norm remains meaningful through a zero crossing. A zero-amplitude experiment has an absolute response but no well-defined relative gain based on its zero background; numerical residue is not a physical denominator.

Passing these checks validates the specified finite model. Tangent sensitivity is not by itself a full quantum correlation or semiclassical-validity calculation. Common covariant directional pressures are still needed before coupling the metric.

## Required regressions after the source and coefficient audit

- Center finite differences at the actual base source, including every nonzero auxiliary probe. Gauge, translated and legacy comparators must use that same source history or explicitly report the comparison unavailable. Check causal sample counts; absent observations cannot pass. Post-drive work constancy begins only after all applied sources stop.
- Mathematical acceptance must survive optimized Python. Use explicit failed-gate exceptions and inspect semantic result fields, output freshness and before/after source hashes; `assert` or process exit alone is insufficient. Reject unknown model modes, empty or duplicate nonpositive finite-difference steps and nonfinite/incomplete outputs.
- Bind the bytes of external proof and contract references, not only their path strings. Keep declared model assumptions distinct from conjectural assumptions. A planner trace remains conditional even when it retains no conjecture.
- Derive prefactors independently of the production test; reusing the same wrong factor on both sides is not verification. Check inclusive cutoffs, special-function indices and natural versus base-ten logarithms against hand-derived identities.
- An exact primitive can be a poor floating-point algorithm. Test saturated endpoint subtraction with held-out large-potential and tiny-window inputs. Use documented adaptive precision or explicit domain rejection; a fixed precision fallback is not universally stable. State precision explicitly in the independent reference and distinguish high precision from interval bounds.
- Label asymptotic plot rows and omitted argument shifts. An enormous formal logarithmic cutoff is not an exact critical integer, a physical instability or an instruction to allocate that many modes.

Record reviewed line/function scope separately from executed branch coverage. Preserve initial failing evidence and final corrected hashes. After the concrete held-out defects and required gates are resolved, stop optional scans.

## Scalar and geometry regressions

A comparator marked unavailable must fail a gate that requires comparison. Register dynamically loaded dataclass modules in sys.modules before execution, and surface import errors. Confirm that every defined analytic fixture is actually executed and included in acceptance.

Do not reject a valid invariant subspace merely because it is nondiscriminating. Test zero scalar, zero mass and zero-frequency affine limits separately from a nonzero exchange fixture. Never clip a negative constraint radicand or an exponential diagnostic to manufacture a regular result.

A flux-reduced system sharing the gravitational RHS is a useful consistency check, not a wholly independent implementation. Add independent symbolic equations or another state representation. An omitted-force control must show both a resolved constraint/work defect and agreement with its independently integrated prediction.

A tiny difference across finite-difference steps may be a solver-error floor; do not claim a demonstrated convergence order without a truncation-dominated interval. Keep fixed-grid refinement distinct from physical regulator changes.

## Acceptance defects found in review 8

Match every supported physical coefficient in a reference comparator. If the archived solver cannot represent a custom matching coefficient, report unavailable with the reason; never compare different physical equations as though they shared a contract. An unavailable required comparator is not a passing gate.

Validate derived diagnostics as well as integrated states for finiteness. Finite state components can overflow when squared, and multiplication by zero after overflow can create NaN. Reject nonfinite energies, work defects and constraints explicitly. Reject empty case collections before reducing gates with all(); semantic status must follow evaluated gates and required analytic fixtures, not be initialized to passed.

Keep base-trajectory node refinement separate from tangent-response node refinement. Agreement as the perturbation amplitude changes does not establish response quadrature convergence. Describe normalization by max(1, reference) as a mixed absolute/relative scale, not a purely relative error.

For spectral diagnostics, test lower-energy tiny overlaps and exactly absent channels, excluded zero modes, fixed-volume mesh refinement versus increasing volume, and log-domain underflow. Compare against a genuinely independent high-precision or matrix reference. A finite positive spectral matrix is only a finite necessary test; it does not establish reflection positivity for a quantum field theory.
