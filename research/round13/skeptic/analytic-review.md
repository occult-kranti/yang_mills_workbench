# Independent analytic review, round 13

## The finite and infinite moment statements are different

For finite real κ let μκ have normalized density exp(κx) sqrt(1−x²) on [−1,1]. Its moment recurrence follows from a vanishing-endpoint integration by parts. Normalization m0=1 is independent of the recurrence. At nonzero κ, every moment through the chosen even order is affine in u=m1. At κ=0 one must use the Haar branch; division by κ is invalid.

For every r>=1 the Hankel matrix H_r and localizer L_(r−1) are positive semidefinite for the true measure. Therefore their affine-in-u PSD feasible set is a nonempty closed convex interval. These intervals are nested. A numerical search point, optimizer status, approximate eigenvalue, or successful Cholesky computation does not prove either endpoint.

An exact negative witness v for M(u)=A+uB gives c+du=v^T M(u)v>=0 at the true mean. It therefore supplies a rational half-line. The intersection of such verified half-lines with [−1,1] is a valid outer enclosure. A rejection at one point, without the witness slope, does not determine which entire side can be removed. Zero pivots with nonzero off-diagonal rows are indefinite; positive-definite Cholesky alone does not implement PSD testing.

All-order positivity does establish more. On polynomials define <p,q>=L(pq). The Hankel condition makes this positive semidefinite. The localizer gives ||xp||²<=||p||², so multiplication by x descends through null vectors and extends to a bounded selfadjoint contraction. The spectral measure of its cyclic vector 1 represents the moments and has support in [−1,1]. Thus all-order support is proved, not inserted as an unverified assertion.

The recurrence establishes the integration-by-parts identity for polynomial tests. Given f in C1[−1,1], approximate f′ uniformly by polynomials and integrate them, matching f(0). This yields simultaneous uniform convergence of f and f′, so the identity extends to C1. Put ν=(1−x²)μ. On the open interval its distributional equation is Dν=[κ−3x/(1−x²)]ν. An integrating factor shows that ν=C exp(κx)(1−x²)^(3/2) dx there. Thus μ has the desired density in the interior. Possible endpoint atoms require a separate check: multiplication by (1−x²) kills them on the left, whereas the right side contributes −3a_+δ_1+3a_-δ_-1. The interior ν vanishes at the endpoints and supplies no compensating delta, so both atoms vanish. Normalization fixes C.

Consequently the complete hierarchy has a unique normalized solution. The full finite PSD feasible intervals are nested compact subsets of [−1,1] whose intersection is this single mean; their diameters tend to zero. This is a qualitative mathematical statement without a convergence rate. It does not by itself prove convergence of a particular heuristic sequence of witness cuts, and does not identify the Euclidean tilted measure with a Hamiltonian ground-state or real-time measure.

## Locality cannot be substituted for a spectral gap

For a finite-volume comparison, tensor-product free evolution preserves the support of bounded observables even when the onsite Casimirs are unbounded. Bounded interaction-picture plaquette terms can then be controlled by an integrable absolute-coupling envelope. Signed interactions must use absolute values; differences between the shared onsite evolutions must be included as additional defects rather than ignored.

A naïve Dyson expansion produces nested commutators whose next support need only overlap the entire accumulated union. Such terms are not all consecutive-overlap paths. A degree-based path count must instead be justified through the commutator differential inequality and a Duhamel volume comparison, where internal unitary terms are removed before iteration.

Even exact finite-time locality supplies no lower bound on the ground-state gap. As a counterexample, take a spin chain with H_n=2 sum_i n_i − sum_(i=1)^(n−1)(σ_i^+σ_(i+1)^−+σ_i^−σ_(i+1)^+). Jordan–Wigner gives a number-conserving free-fermion Hamiltonian whose one-particle matrix is the Dirichlet tridiagonal Laplacian. The vacuum is unique, and its gap is 2−2cos(π/(n+1)), which tends to zero. The onsite norms and nearest-neighbor interaction norms remain bounded independently of n; the usual locality estimate remains uniform. This is a logical counterexample to locality implies gap, not a counterexample to the Yang–Mills conjecture.

A global-state boundary error proportional to total affected volume is also distinct from a local-observable error. Uniformity in finite time and fixed support is not uniformity in arbitrarily long imaginary time, all supports, lattice spacing, and physical energy calibration. None of those limit exchanges can be filled by giving two different quantities the same symbol.

## Exact false-closure control

At κ=9/8, the point mass at u=1/3 has H1 positive semidefinite, L0=8/9, and exactly satisfies the n=0 identity 3u=κ(1−u²)=1. Its n=1 identity has residual 8/9. Thus even perfect low-order arithmetic and positivity can accept a false closure. The recurrence-generated order-four hierarchy rejects the same u. This fixture supplies a rational, reproducible reason to require the next equation.
