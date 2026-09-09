# Independent skeptical review — Yang–Mills round 10

**Verdict:** accept the conventional proof and exact-rational certificates for the stated single-square SU(2) Hamiltonian, including removal of its character truncation and a lower gap bound for every real coupling ratio in a closed interval. Accept the time-dependent calculation as a tested finite-Galerkin numerical result. None of these results constructs four-dimensional continuum Yang–Mills or proves its physical mass gap.

The current independent review has **119 grouped gates**: 44 independent algebra/radial/edge checks, 43 delivered-artifact checks, 16 acceptance controls, and 16 proof-wrapper controls. The first group includes **1,800 exact Sturm-count comparisons** against a separately implemented dense rational congruence algorithm. Acceptance controls also pass under `python -O`. These are executed diagnostics, not 119 new theorems or a claim of full branch coverage. The mathematical arguments were independently reviewed by an agent; they have not been checked by a formal proof assistant or credentialed human peer reviewer.

## Accepted mathematical result

On a single cycle of four independent SU(2) links, imposing every vertex Gauss constraint leaves class functions of the loop holonomy. With link Casimirs normalized to j(j+1), the Hamiltonian is

    H = alpha sum_e C_e + lambda [1 - Re Tr(U_loop)/2],
    alpha > 0, lambda >= 0.

In the orthonormal character basis chi_(n/2), n>=0, the diagonal is alpha n(n+2)+lambda and adjacent off-diagonal entries are -lambda/2. The factor n(n+2) already includes all four links. The radial Haar transformation gives the equivalent Dirichlet operator

    -alpha d²/dtheta² + lambda(1-cos theta) - alpha, 0<theta<pi.

This regular radial problem has a selfadjoint compact-resolvent realization and simple eigenvalues. Its fixed-parameter gap is positive. This is an infinite-dimensional quantum operator on a finite spatial graph; the one-plaquette solution is already known in the literature.

The cutoff certificate retains n=0,...,N-1 and bounds the omitted tail below by tau=alpha N(N+2). A rational level U strictly between the first excited retained eigenvalue and tau gives delta=(lambda/2)²/(tau-U). Completing a square proves

    H >= [A_N - delta P_boundary] direct_sum U I.

The first two min–max levels therefore lie between the corresponding finite lower and upper matrices. Exact rational brackets, with independently checked eigenvalue indices, bound the full infinite-character gap. The gap subtraction uses the lower excited endpoint minus the upper ground endpoint for its lower bound. Using opposite directions would not be a valid lower certificate.

After H=alpha h(kappa), kappa=lambda/alpha, the gap delta(kappa) is 2-Lipschitz. The scalar kappa I cancels from a gap and the remaining bounded operator is multiplication by cos(theta), of norm one. Certified centers at 0,2,4,6,8,10 cover [0,10] within distance one. Exact subtraction gives

    delta(kappa) >= 70368744177647 / 70368744177664
                 >= 999999 / 1000000, for every real 0<=kappa<=10.

Consequently Delta(alpha,lambda)>=alpha*999999/1000000 whenever alpha>0 and lambda/alpha lies in that interval. The six rational point certificates and analytic continuity theorem cover irrational coupling ratios too. A global physical lower bound over changing alpha additionally requires alpha to be bounded away from zero in specified units.

The independent dense rational inertia checker verifies all 16 delivered stationary certificates, including lambda=100 with N=8,16,24. A separate radial quadratic-form integration verifies the Haar and four-link normalization. A second-order radial finite-difference calculation approaches the same first gap with the expected convergence order. Floating Mathieu values are corroborating evaluations, not the source of the exact certificate.

## Retained failures and repairs

1. **Unbound certificate meaning and precision.** The initial replay accepted `scope="complete four-dimensional Yang-Mills"`, a 128-bit label on brackets produced at 20 bits, and numeric `1` in place of a boolean positivity status. The endpoints still enclosed the finite-graph eigenvalues, but their meaning and stated precision were not protected. The corrected replay requires the exact finite-graph scope, valid precision, every bracket width <=2^(-bits), and a real boolean. The original source and mutation results are retained in `initial_certificate_metadata_failures.json` and its source snapshot.
2. **A recorded independent work error was not an acceptance gate.** Replacing the unitary-midpoint method's returned work by zero left all 11 original dynamics gates passing while its work defects were about 6.0723. This was reproduced against the preserved source, not inferred solely by inspection. The repaired code explicitly gates midpoint norm and work and checks the work-refinement order. The same mutation now fails the required work gate. The corrected full work calculation is unchanged; only the missing acceptance requirement was added. The new 10^-4 work criterion is a review-added criterion, not retrospectively described as predeclared before the first run.
3. **Incomplete provenance manifests passed.** The first proof wrapper accepted an empty SHA-256 manifest and one omitting the mathematical advisor document. Both still produced the 13-rule route. The corrected wrapper requires the exact six reviewed inputs, well-formed digests and paths confined to its package; symlinks and extra escaped paths are rejected. Semantic arithmetic mutations are also rejected after deliberately refreshing their JSON hashes, so rejection does not depend only on stale bytes.
4. **Acceptance state could become stale across reruns.** The initial main routine recorded producer hashes only after execution and could leave an old successful validation artifact after a later failure. The repaired routine freezes hashes before and after, clears prior gates, records `running`, and writes `failed` on an exception. An injected failed rerun now replaces the previous passed status.
5. **Review during active repairs correctly failed source binding.** The first delivered-artifact audit observed source hashes that no longer matched while the implementer was changing the files. It did not certify those bytes. That failure is retained separately; the final 43-gate artifact audit binds the refreshed output and final producer sources.

No arithmetic discrepancy was found between the producer Sturm recurrence and the independent dense rational congruence algorithm on the declared fixtures. No assumption or acceptance threshold was relaxed to convert a mathematical counterexample into a passing result.

## Edge cases and unresolved limits

- At lambda=0, the exact spectrum is alpha n(n+2) and the first gap is 3 alpha. Zero off-diagonal coupling needs a diagonal counting rule; exact eigenvalue endpoints and zero internal principal determinants were tested explicitly.
- A coarse valid enclosure may have a negative lower gap endpoint. The alpha=10^-100, 128-bit absolute-tolerance fixture correctly returns an inconclusive positivity flag while still enclosing the true 3*10^-100 gap. Mathematical positivity and numerical certification at fixed absolute precision are distinct claims.
- Alpha=0 is outside the theorem. For lambda>0 the operator becomes multiplication with spectrum [0,2 lambda] and has no normalizable isolated vacuum at zero. The advisor's two-trial-state bound proves Delta <= 2 sqrt(2) pi sqrt(alpha lambda)-alpha along fixed lambda and sufficiently small positive alpha, hence the gap tends to zero. This is a specific parameter path, not the matched Yang–Mills continuum trajectory.
- Negative lambda is excluded by the computational physical contract. An analytic reflection relates its spectrum to positive lambda with a constant energy shift, so its gap is unchanged; that observation does not justify silently admitting it to an implementation whose tail proof assumes nonnegative potential.
- A missing coverage cell, wrong center, understated radius, changed Lipschitz factor, omitted endpoint or rounded-up uniform lower constant is rejected. Finite samples alone do not prove a range-wide result.
- Small Hilbert-space or time-step differences in the dynamics are numerical evidence. They do not certify the full infinite-character time evolution, an adiabatic theorem, or the state following its instantaneous vacuum.

## Time-dependent coefficient result

The executed driver is alpha=1 and lambda(t)=5[1-cos(pi t/2)] for 0<=t<=2, starting in chi_0. Because lambda is prescribed externally, the required identity is d<H>/dt=lambda'(t)<V>, not conservation of quantum energy alone.

The reference run's energy change is approximately 6.07229637262671 and its independently integrated work is 6.07229637262666. The N=16 to N=24 state discrepancy is 4.35e-10; the tolerance refinement discrepancy is 1.23e-8. A separately propagated unitary-midpoint solution reaches a final state discrepancy of 7.74e-7 with observed order approximately 2.000002. These are separate diagnostics with separate meanings. The finite-Galerkin Schrödinger equation and its work accounting pass; an externally adjusted coefficient has not become a dynamical field with its own energy or stress.

## Proof search and the next obligation

The two-front search returns a replayed 13-rule route to the scaled compact-parameter gap bound. Withdrawing gauge projection, tail positivity, exact brackets or complete coverage blocks the route. The four-dimensional Yang–Mills target remains underivable. The wrapper now binds the mathematical document, both source programs and both arithmetic artifacts; its Horn implications remain conventional mathematical premises, not machine-checked proofs of the source document.

The next substantive target is two adjacent squares with seven independent links and all six vertex gauge constraints. A product of two independent class-function rotor spaces loses relative-orientation information and shared-link electric terms. After tree reduction the two loop matrices transform by simultaneous conjugation. In particular, their individual traces do not determine Tr(UV): U=i sigma_3 with V=i sigma_3 or V=i sigma_1 gives the same two individual traces but product traces -2 and 0. A continuous relative orientation z=n_1 dot n_2 is therefore a meaningful next coordinate, with endpoint degeneracies treated explicitly; it is not an arbitrary added mass term. Its coupled kinetic operator and cutoff theorem still need derivation and independent comparison to the full Gauss-constrained graph.

Growing-graph uniformity, physical scale matching, nontrivial continuum correlations and reconstruction axioms remain absent. The finite U(1)/Einstein–QED work contributes verification methods, but no mathematical implication identifies its state, stress or gauge group with pure SU(2) Yang–Mills.

## Audit scope and reproduction

Run `audit_independent.py`, `audit_artifacts.py`, `audit_acceptance.py`, and `audit_proof.py` from this directory; use `python -O audit_acceptance.py` for the independently replayed optimization check. The scripts locate the sibling solver and parent proof package in the portable archive. Source hashes, line counts and function ranges are recorded with the reports. The core certificate and study sources were reviewed line by line; the newly added range verifier and proof wrapper received targeted mutation checks. The inherited search engine was inspected at relevant guards and replay boundaries, not re-audited in full. This review supplies no claim of complete executed branch coverage, browser validation or independent full-paper literature reading.
