# Independent nonzero-coupling calculation — Round16 Loop2

This audit retains the Loop1 graph, normalized independent SU(2) link Haar measure, and the same eleven-trace observable in both actions. The ten outer coefficients are 1/8. The target is the expectation at shared coefficient 1/8 minus the expectation at shared coefficient zero. A nonzero shared-face response is a finite Euclidean integration result, not a physical Hamiltonian spectral gap.

## Independent polynomial coefficients

Let t=Tr U and x=t/2. Ordinary characters obey χ₀=1, χ₁=t and χ_(n+1)=tχ_n−χ_(n−1). Normalized Haar integration gives zero for odd powers of t and Catalan(r) for t^(2r). Thus the projection

\[
P_{p,n}=\int x^p\chi_n(U)\,dU
=2^{-p}\sum_j [t^j]\chi_n(t)\int t^{p+j}\,dU
\]

is evaluated by explicitly constructing the character polynomial and summing these moments. This is independent of the producer's factorial coefficient formula and triangle-rule fusion implementation.

For numerator insertion s=1 and partition insertion s=0, each face contributes the formal ε series

\[
a_{f,n}(\varepsilon)
=\sum_{r=0}^{N}\frac{\kappa_f^r\varepsilon^r}{r!}P_{r+s,n}.
\]

There is no extra ε or κ factor from the insertion: the numerator is x_f exp(εκ_f x_f) on every face. ε counts total Taylor degree and is evaluated at one. It is not a dynamical variable.

The accepted Loop1 graph reduction gives a boundary character for each five-face disk. Its coefficient is the product of its five individual face series divided by (n+1)^4. Every multiplication is truncated by the sum of formal ε degrees. Face coefficients are kept individually, including a signed unequal fixture. A disk label greater than floor(N/5)+s cannot occur by total degree N, since every face would require at least n−s powers. This finite label bound does not discard a physical tail; it exactly enumerates the labels present in the finite Taylor polynomial.

For the final shared-boundary integration, the independent code does not use a fusion condition. It multiplies χ_n(t)χ_m(t), inserts x_shared^(r+s), and integrates each monomial using Catalan moments. The shared exponential coefficient κ_shared^r/r! is included explicitly. Convolution with the two disk series yields every partition and numerator coefficient through degree N.

This coefficient derivation depends on the reviewed five-face disk identity. Its new arithmetic is independently implemented; its graph factors are supported by the separate Loop1 raw shared-edge projector. It does not pretend that using a second algebraic representation supplies a different underlying physical theory.

## Complete remainder and normalized difference

For S=Σκ_f x_f, |S|≤M=Σ|κ_f|, and |O|≤1. The exponential tail beyond N is bounded, when M/(N+2)<1, by

\[
R_N=\frac{M^{N+1}}{(N+1)!}\frac1{1-M/(N+2)}.
\]

The same bound controls both the numerator and partition tail. Signed couplings enter M through their absolute values. Each distinct square has Haar mean zero, so Jensen's inequality gives Z≥exp(⟨S⟩₀)=1. Therefore

\[
Z\in[\max(1,Z_N-R_N),Z_N+R_N],\qquad
A\in[A_N-R_N,A_N+R_N].
\]

All four endpoint quotients are evaluated as exact fractions and their minimum and maximum are taken. This is valid for numerator intervals of either sign. The target interval is [E_full,low−E_omit,high, E_full,high−E_omit,low]. Both actions have their own M, remainder and normalization. Dropping a normalization tail or substituting a different insertion changes this contract.

Degrees 0,6,12,18,24 are retained. A narrow-width certificate and a positive-lower-bound certificate are different claims; the target requires both. A coarse failure remains insufficient even if the final degree succeeds.

## Why the comparator is not zero

At shared coefficient zero, the all-eleven Haar product is zero only before the outer exponential is inserted. Center parity forces the first nonzero outer-action numerator term to add one extra power on all five faces of either disk. The two possibilities each contribute 41/(81·2^19), giving

\[
A(t,t,0)=\frac{41}{81\,2^{18}}t^5+O(t^7).
\]

The independent polynomial coefficients recover this exact degree-five term. The partition begins at one, so normalization preserves the leading term. This local expansion is a diagnostic; the finite t=1/8 comparator is separately enclosed with its full tail.

## Audit scope and completed acceptance

The verifier compared every saved coefficient, value, tail, normalization, quotient, difference, required fixture, input parameter and source binding. It rejected plausible wrong-model certificates even when their status fields claimed success. The independent prediction was written before the producer collection existed and is preserved separately from final acceptance.

All 84 named independent gates passed under ordinary and optimized Python, with byte-identical reports and independently reconstructed collections. The degree-24 target lower endpoint is approximately 2.4303274915976136×10^−7 and its width is approximately 4.1729944948126505×10^−22. Exact rational endpoints are stored in `output/review.json`. The full expectation is approximately 2.430920616729664×10^−7; the separately bounded omitted-action comparator is approximately 5.931251320486862×10^−11.

Degrees zero and six fail both useful positivity and precision. Degree twelve has a positive lower bound but width approximately 2.8181392775852724×10^−8, so remains insufficient for the requested 10^−12 precision. Degrees eighteen and twenty-four meet the complete target. All seven required signed, zero and unequal fixtures were independently reconstructed; these isolated fixture signs imply no general monotonicity theorem.

Negative controls cover missing fixtures, an empty inventory, omitted coarse failures, Boolean parameters, changed source and graph bindings, a changed individual coefficient, replacement of the all-eleven insertion, substituted numerator coefficients, discarded normalization or numerator tails, a fabricated zero baseline, forged precision or pass status, cache mutation, and actual source changes after import. Cached producer coefficient tuples are immutable; mutating a returned certificate cannot change a later certificate. Every file in the producer manifest matches its recorded hash.

The producer's complete `series.py`, `run_loop2.py`, and derivation were read, including factorial coefficients, degree truncation, graph factors, insertion convention, remainder, normalized quotient, fixed-target comparison and fixture admission. The independent implementation uses explicit polynomial Haar moments. This is a scoped source and behavior audit, not a claim of exhaustive branch coverage or review of unrelated historical files. No unresolved Loop2 mathematical or implementation defect was found; the genuine earlier cache-alias failure remains preserved in Loop1.

The portable entry point is `python verify_loop2.py --producer PATH_TO_FORWARD_LOOP2 --output NEW_OUTPUT_DIRECTORY`. It infers the sibling `loop1` directory, cold-loads the producer, and reconstructs the complete fixed collection independently. Final input hashes use relative `producer/` and `loop1/` prefixes, allowing byte-identical replay after copying the archive. The accompanying manifest binds the accepted source, results and review files.
