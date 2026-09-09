# Round 6: regulator certificate and obstruction experiment contract

Frozen mathematical contract, 9 September 2026. Advisor and independent skeptic derived the formulas below before implementation. Numerical execution must report its actual gates separately. This extends the round-5 finite model; it does not change historical equations, remove a regulator, or assert a new result in continuum QED.

## Accepted targets

1. Derive and independently evaluate the exact continuous-longitudinal-momentum coefficient at a finite Landau cutoff and finite canonical-momentum window; prove its maximizer is at zero potential.
2. Extend the existing discrete coefficient certificate to **every finite Landau cutoff** at fixed window `b=10, K=20`, using positive quadrature weights exact on constants.
3. Prove the explicitly fixed-matching coefficient cannot retain a uniform positive lower bound when **both** physical cutoffs tend to infinity. This is an obstruction to this proof route/model limit, not evidence of a physical singularity.

## Definitions and exact formulas

Use the unchanged round-4 convention `e² = 4π α`, `α = 1/137.035999084` for floating illustrations. `b>0`, `K>0`, integer `N>=0`, `n=0,...,N`, `d_n=2−δ_n0`, `M_n²=1+2bn`. The continuous longitudinal weight is `b d_n dk/(4π²)`. It differs from any particular discrete Gauss-node sum.

Let

\[
u_M(y)=\frac{y}{\sqrt{M^2+y^2}},\qquad
P_M(y)=\frac{u_M(y)-u_M(y)^3/3}{M^2}.
\]

Then `P'_M(y)=M²/(M²+y²)^(5/2)` and

\[
C_{N,K}(a)=\frac{b}{16\pi^2}\sum_{n=0}^N d_n
\left[P_{M_n}(K-a)+P_{M_n}(K+a)\right].
\tag{E1}
\]

The function is even. With `f_M(y)=M²/(M²+y²)^(5/2)`,

\[
\partial_a C_{N,K}(a)=\frac{b}{16\pi^2}\sum_n d_n
\left[f_{M_n}(K+a)-f_{M_n}(K-a)\right]<0\quad(a>0).
\tag{E2}
\]

Thus `sup_a C_N,K(a)=C_N,K(0)` exactly for the integral model. Its sharp global coefficient margin is

\[
\mu_{N,K}=1+\chi_b-e^2 C_{N,K}(0),\qquad
\chi_b=\frac{e^2}{12\pi^2}\left[b-\log(2b)-\psi\left(1+\frac1{2b}\right)\right].
\tag{E3}
\]

**Do not transfer E2 to finite quadrature by assertion.** A two-node Gauss rule on a wide window supplies a concrete counterexample to the proposed discrete maximum at `a=0`. The coarse grid is admissible and positive but its moving narrow integrand peak can align with a node away from zero.

For a positive discrete rule integrating constants exactly (`Σ_j w_kj=2K`), the separate pointwise estimate remains

\[
C^{\rm disc}(a)\le C_*^{(N)}=
\frac{bK}{8\pi^2}\left[1+2\sum_{n=1}^N(1+2bn)^{-3/2}\right].
\tag{E4}
\]

At `b=10,K=20`, retain the round-5 rational inequalities `α<1/137`, `π>157/50`, and lower mass-cube bounds `84,246,427,729` for levels 1 through 4. Monotonicity of `f(t)=(1+20t)^(-3/2)` gives

\[
\sum_{n=5}^{\infty}(1+20n)^{-3/2}
\le\int_4^{\infty}(1+20t)^{-3/2}dt=\frac1{90}.
\tag{E5}
\]

Consequently, for every finite `N` and all real `a`,

\[
e^2C^{\rm disc}(a)<
\frac{100}{137(157/50)}
\left[1+2\left(\frac1{84}+\frac1{246}+\frac1{427}+\frac1{729}+\frac1{90}\right)\right]
=\frac{67743204500}{274510827927}<\frac14.
\tag{E6}
\]

With the already proved `χ_b>0`, `Z(a)>3/4`. This extends the denominator certificate, and hence the finite-dimensional theorem individually, to all finite `N` at fixed window. It does **not** establish convergence of states, energy, current or derivatives as `N→∞`.

At fixed finite `N`, taking `K→∞` in E1 yields

\[
C_{N,\infty}=\frac{b}{12\pi^2}
\left[1+2\sum_{n=1}^N\frac1{1+2bn}\right].
\tag{E7}
\]

Writing `z=1/(2b)` and using the digamma recurrence gives

\[
Z_{N,\infty}=1-\frac{e^2}{12\pi^2}
\left[\log(2b)+\psi(N+1+z)\right].
\tag{E8}
\]

At fixed nonzero `e²` and `b`, E8 tends to minus infinity as `N→∞`. Positivity of the defining integrands proves the stronger cofinal statement: at `a=0`, every path with `N→∞` and `K→∞` eventually exceeds every specified value of `C`, whether or not the path itself is monotone. To prove it, choose a finite partial sum `N0` above the requested threshold after the full momentum integral, then choose a finite `K0` giving that threshold for `N0`. Every `N>=N0,K>=K0` exceeds it.

Optional explicit path check: for `K>=sqrt(1+2bN)`, each `u_n>=1/sqrt(2)` and

\[
\int_{-K}^K\frac{M_n^2\,dk}{4(M_n^2+k^2)^{5/2}}
\ge\frac5{12\sqrt2 M_n^2}.
\tag{E9}
\]

The harmonic lower bound diverges. An operational warning: E8's zero for the physical illustrative coupling lies at an astronomically large formal cutoff. Compute the asymptotic **logarithm**, `log(N_crit)≈12π²/e²−log(2b)`; never allocate modes up to that value, treat the asymptotic estimate as an exact integer threshold, or call this a demonstrated physical Landau pole.

## Implementation and edge-case gates

Use a new `round6` implementation only. Suggested owned outputs: `regulator_experiments.py`, `regulator_results.json`, `regulator_plot_data.csv`, plots, and a short execution README. If the root assigns different filenames, preserve the same content.

| Gate | Independent computation | Acceptance condition |
|---|---|---|
| Primitive | SymPy differentiates P; subtract defining integrand | Exact zero after simplification for positive M |
| Integral reference | SciPy adaptive quadrature of the original integrand, not P | Maximum scaled difference `<2e-11` across the bounded matrix below, with quadrature error estimates reported |
| Continuous geometry | Compare `a` and `−a`; analytic derivative and sampled positive-a monotonicity | Symmetry within roundoff; derivative nonpositive within a documented floating tolerance; proof remains the analytic inequality |
| Quadrature refinement | Gauss-node sums versus independent integral | Report errors at 32/64/128/256/512 nodes; highest-resolution max absolute error `<2e-10` on selected b10,N4,K20,a grid; do not require monotonic error at every doubling |
| Discrete adversary | N0,K20,two Gauss nodes; compare a0 and a at a node | Expose a nonzero-potential coefficient larger than a0 and larger than the continuous maximum; the invalid transfer is rejected |
| Uniform tail certificate | Python Fraction reconstructs E6 and cross-multiplies against 1/4 | Exact equality to given rational and strict inequality; no rounded printout used as proof |
| Full-window sum | Direct finite harmonic sum versus digamma E8 | Absolute difference `<2e-13` at N0,1,4,20,1000; both formulas independently formed |
| Tail behavior | E8 as function of log10(N+1) | Safe log-domain asymptotic illustration beyond representable N; label asymptotic rows, no exact numerical claim at unallocated N |
| Cofinal example | E9 reference path at N1,4,16,64,256,1024 | Formula bounds validated; this finite list illustrates, but does not prove, divergence |
| Input validation | b<=0, K<=0, N nonintegral/negative; NaN/inf a, b, K, coupling | Explicit rejection rather than silent conversion, empty sums or NaN success |
| Historical integrity | Hash any imported round4/5 equations/code and compare after | No historical file modified |

Bounded independent integral matrix: `b ∈ {0.3,3,10}`, `N ∈ {0,4,20}`, `K ∈ {0.1,2,20}`, and `a ∈ {0,0.3,K,2K,−K}`. This is 135 small evaluations, with each reference integrating the original per-level function. For very large `|a|/K`, direct differences of saturated P values can cancel; either reject an unsupported range or evaluate with a stable fallback and demonstrate it against arbitrary precision. Do not expand to huge parameter scans without an actual unresolved gate.

Suggested plots: (1) exact `Z(a)` for the selected finite window, loose pointwise bound and discrete examples; (2) finite-quadrature error versus node count; (3) formal full-window Z versus logarithmic cutoff, with exact/asymptotic methods visibly separated; (4) one fixed-window finite-N certificate versus the cofinal obstruction. Every plot must link raw values and calculation settings, and every status must separate conventional mathematical proof, symbolic identity, numerical cross-check and unsupported physical extension.

## Stop rule and next obligation

Once the formulas, counterexample and declared gates are resolved, stop optional scans. The obstruction means the next continuum task is to derive a consistent regulator-dependent subtraction and common current/stress matching, not to search for a plot that hides the divergence. Any changed matching is a new model contract and requires rederiving the work identity, denominator, Ward identity and physical renormalization conditions together.
