# Certified representation error for a driven two-plaquette graph

Round 12 adds an analytic bound on the error caused by truncating the invariant-polynomial degree during time evolution. A separate exact rational two-step calculation also certifies its **total endpoint error below 0.000337501**, including representation truncation and the finite evolution algorithm. The four smooth-drive comparisons continue to report floating integration and conditioning errors separately.

For a normalized initial state of degree at most d₀ and cutoff D≥d₀, define

\[
 A(t)=\int_0^t (|\lambda_1(s)|+|\lambda_2(s)|)\,ds,
 \qquad m=D-d_0+1.
\]

The new bound is

\[
 \boxed{\|\psi(t)-\psi_D(t)\|_{L^2(\mathrm{Haar})}
 \le \min\left\{2,\frac{A(t)^m}{m!}\right\}.}
\]

For three different protocols with A(T)=1/2 and d₀=0, this gives **1/384 at D=3 and 1/3840 at D=4**, with exact rational arithmetic. For the original full-strength round-11 protocol A(T)=5, both selected cutoffs give only the trivial bound 2. We do not describe that original case as having a small certified error.

## Reproduce

Dependencies are Python, NumPy, SciPy and Matplotlib. No network or computer-algebra package is used. All inputs and outputs are resolved relative to this directory, so it can be copied intact into another checkout:

```bash
python drive_bound.py --degree 4 --duration 2 --lambda1-scale 1/10 --lambda2-scale 3/20
python exact_stepper.py
python test_solver.py
python -O test_solver.py
python run_study.py
python -O run_study.py
```

The first command produces and verifies an exact analytic representation certificate. `exact_stepper.py` creates and replays the stronger total-state certificate for the single nonnegative two-step fixture. The full numerical study uses only four declared protocols, degrees 3 and 4 for the primary comparison, and degrees 5 and 6 as numerical references. It takes approximately six seconds in the recorded environment. No high-degree scan is needed to obtain the theorem.

`vendor/two_plaquette.py` is the unchanged round-11 exact kinetic/Haar implementation. `vendor/round11_run_study.py` preserves the unchanged original drive protocol as provenance; it is not executed. `dependencies.json` records their original project paths, roles and SHA-256 digests. The expected paths and hashes are pinned in the analytic verifier, which rejects missing, replaced or symlink-substituted dependencies. The scripts do not depend on a neighboring repository or an absolute workspace path.

## One total-error certificate with exact time evolution arithmetic

A separate bounded fixture uses α=ρ=1 and D=3 (20 monomials). The magnetic coefficients are constant for each of two duration-one segments:

| Segment | λ₁ | λ₂ |
|---|---:|---:|
| First | 1/20 | 1/10 |
| Second | 1/10 | 1/20 |

The initial state is the constant Haar wavefunction: the **electric vacuum**, not the interacting ground state at these nonzero coefficients. The coefficients are nonnegative. Their swap gives two distinct Hamiltonians, and A(T)=3/10.

`exact_stepper.py` reconstructs each rational form matrix and its monomial-coordinate operator `Hcoord=G⁻¹Hform`. It applies a degree-100 Taylor polynomial for each exponential using exact pairs of real and imaginary Fractions. The stored 20-component coefficient vector is never renormalized. Its exact Haar norm squared is recorded; it differs slightly from one, as permitted for a polynomial approximation.

The largest kinetic eigenvalue retained at D=3 is exactly 45/2. Boundedness of the two plaquette potentials gives the physical operator norm bound `M=45/2+2(3/20)=114/5` on each finite Hamiltonian. This bound is in the Haar/Gram norm; the raw coordinate matrix need not be symmetric in the Euclidean norm.

For a selfadjoint Hamiltonian, the integral remainder and unitarity give

`||exp(−ihH)−Σ(k=0..p)(−ihH)^k/k!|| ≤ (hM)^(p+1)/(p+1)!`.

There is no exponential factor. If the two step remainders are ε₁ and ε₂, telescoping their products gives an algorithm error at most `(1+ε₁)(1+ε₂)−1`. The factors account for the polynomial propagators being only approximately unitary. Here that exact rational bound is about **3.01e−23**. Exact Fraction arithmetic contributes zero rounding error to the stored rational result.

The representation contribution is exactly `27/80000 = 0.0003375`. Adding the algorithm contribution proves the total Haar state-distance bound **strictly below 0.000337501** between the exact infinite-representation state and the stored coefficient vector. The total bound is not capped at 2, because the stored polynomial state is not assumed normalized.

`output/exact_step_certificate.json` retains the exact vector, exact Gram norm squared, both operator bounds and Taylor remainders, the product and representation errors, the total bound, physical protocol and source hashes. Its verifier reconstructs and replays the complete fixed fixture. Changing a coefficient, protocol, cutoff, norm, normalization flag or semantic target is rejected. This is an end-to-end arithmetic certificate conditional on the same finite-graph Hamiltonian and analytic operator theorems. It does not apply to the separate floating smooth-drive runs or a continuum theory.

## Mathematical setting and proof

The spatial graph, local gauge constraints and Casimir normalization are unchanged from round 11. The physical Hilbert space is the simultaneous-conjugation quotient of two SU(2) loops. Coordinates are x=Tr(A)/2, y=Tr(B)/2 and z=Tr(AB)/2, with

`|x|≤1, |y|≤1, (z−xy)²≤(1−x²)(1−y²)`

and measure `2/π² dx dy dz`. P_D denotes the orthogonal projection onto invariant polynomials of **total degree at most D**, not an eigenvalue-index cutoff. The Hamiltonian is

\[
 H(t)=\alpha K_\rho+\lambda_1(t)(1-x)+\lambda_2(t)(1-y),
 \quad \alpha>0,\quad\rho>0.
\]

The API holds α and ρ fixed. Real signed, integrable magnetic coefficients are allowed for this evolution theorem. They need not be nonnegative as required by the previous spectral-tail argument. The original model has α=ρ=1. This remains a finite open graph with an infinite representation space; no spatial-volume or continuum limit is taken.

Write the Hamiltonian, after removal of a common scalar phase, as

`Hc(t)=αKρ+W(t)`, `W(t)=−λ1(t)x−λ2(t)y`.

The removed phase is identical at every degree and therefore leaves the state-distance comparison unchanged. Kρ preserves every P_D. Multiplication by x or y raises degree by at most one; selfadjointness makes its matrix in orthogonal degree layers tridiagonal in those layers. Also `||W(t)||≤w(t)=|λ1(t)|+|λ2(t)|`.

Let the exact normalized Galerkin state be ψ_D. For n>d₀, let Qₙᴰ project onto degree layers n through D, and let Πₙ₋₁ project onto layer n−1. The state Qₙᴰψ_D evolves under its own selfadjoint compressed block, forced only by `Qₙᴰ W Πₙ₋₁ ψ_D`. The compressed propagator is unitary, so

\[
 \|Q_n^D\psi_D(t)\|
 \le\int_0^t w(s)\|Q_{n-1}^D\psi_D(s)\|\,ds.
\]

The initial higher tail is zero and the base norm is at most one. Induction gives

\[
 \|Q_n^D\psi_D(t)\|
 \le \frac{A(t)^{n-d_0}}{(n-d_0)!}.
\]

Embed ψ_D in the full Hilbert space. Its omitted forcing is `(I−P_D)Wψ_D`, which depends only on the last retained degree layer. A single Duhamel comparison with the unitary full propagator therefore gives

\[
 \|\psi(t)-\psi_D(t)\|
 \le\int_0^t w(s)\frac{A(s)^{D-d_0}}{(D-d_0)!}\,ds
 =\frac{A(t)^{D-d_0+1}}{(D-d_0+1)!}.
\]

The final cap 2 follows because both exact states have norm one. There is **no factor 2 or exponential in the factorial term**. This argument needs bounded perturbation evolution and degree locality; it does not use a sampled residual, an empirical tail probability or numerical convergence. Piecewise constant discontinuities are permitted: the integral is defined across the jumps, and Duhamel and the induction hold almost everywhere. No derivative of λ is required for this state-error theorem.

For any bounded observable O, the same normalized-state comparison implies an expectation difference at most `2||O||` times the state bound. An energy error cannot be inferred by inserting the unbounded Hamiltonian into that bounded-observable inequality.

## Exact action evaluation and certificate scope

The executable protocols are:

- `cosine_ramp`: λᵢ(t)=sᵢ[1−cos(πt/T)], with rational duration and signed scales.
- `constant`: rational signed coefficients over a rational interval.
- `piecewise_constant`: a nonempty list of positive rational durations and rational signed coefficients.

The zero-time case is supported by the cosine and constant protocols. The certificate is for any normalized initial vector in P_d₀. It does not claim to certify the preparation of an arbitrary floating initial vector.

For a cosine ramp,

\[
 A(t)=(|s_1|+|s_2|)\left[t-\frac{T}{\pi}\sin(\pi t/T)\right].
\]

At t=0 and t=T this is exact rational arithmetic. At intermediate times, `action_interval` derives a rational π enclosure from the Machin identity `π=16 arctan(1/5)−4 arctan(1/239)` and alternating arctangent series. It then bounds `s−sin(πs)/π` by fourteen-term lower and thirteen-term upper alternating partial sums. The term ratio is at most `π²/20<1` for 0≤s≤1. Interval arithmetic handles π, and final decimal-denominator endpoints are rounded outward. The factorial is applied to the **upper** action endpoint. Numerical sine values never supply a certificate premise.

`verify_certificate` reconstructs the exact result and checks the complete field set, physical scope, target state pair, normalization and initial subspace, protocol, time, α and ρ, factorial order, action endpoints, cap, source hashes and semantic status. The Boolean and integer metadata are checked by type. A certificate cannot relabel the time-step or coefficient-conditioning error as certified.

This is an exact arithmetic verifier conditional on the mathematical degree-locality and Duhamel proof. It is not a formal proof kernel. The accompanying advisor and skeptic materials provide the independent derivation and audit.

## Declared numerical comparisons

All four cases begin in the normalized constant Haar wavefunction at α=ρ=1:

| Case | Duration T | s₁ | s₂ | A(T) |
|---|---:|---:|---:|---:|
| Original | 2 | 1 | 3/2 | 5 |
| Reduced amplitude | 2 | 1/10 | 3/20 | 1/2 |
| Short strong drive | 1/5 | 1 | 3/2 | 1/2 |
| Slow weak drive | 4 | 1/20 | 3/40 | 1/2 |

The last three have the same analytic upper bound despite different electric evolution over the drive duration. Their numerical differences show how conservative an action-only bound can be:

| Case | D=3 difference from numerical D=6 | D=4 difference from numerical D=6 |
|---|---:|---:|
| Reduced amplitude | 7.34e−7 | 6.64e−9 |
| Short strong drive | 6.28e−5 | 2.68e−6 |
| Slow weak drive | 2.41e−8 | 1.02e−10 |

These are computed endpoint differences, not rigorous errors relative to the infinite-dimensional state. The D=5 to D=6 endpoint differences are respectively about 7.22e−11, 9.57e−8 and 3.24e−11. The smallest slow-drive differences are near the numerical/reference floor; they are not evidence of a certified 1e−10 solution.

At early times the analytic representation bound can be much smaller than floating integration or rounding effects. Consequently a **computed** D-to-D6 difference can exceed the analytic representation bound. This is expected when comparing different error categories. The plot states this explicitly, and no numerical time-step or rounding error is silently added to the exact certificate.

DOP853 evolves the finite state and integrates external work separately. Each trajectory passes finite-history, norm and work checks. For the reduced ramp at D=4, changing the solver tolerance gives an endpoint difference about 5.13e−10. An independent frozen-midpoint exponential method separately integrates Hamiltonian work and enforces its own norm/work gates. It gives state errors approximately 5.27e−6, 1.32e−6 and 3.29e−7 at 80, 160 and 320 steps, with observed orders 1.9995 and 1.9999. These are numerical diagnostics. The solver tolerance is not a rigorous global error bound, and this midpoint matrix exponential is evaluated in floating arithmetic. These smooth-run states use an explicitly recorded common scalar-potential phase removal; they cannot be directly mixed with the physical-phase exact Taylor vector.

The numerical acceptance gates require norm and work defects below 1e−8, fixed-D tolerance difference below 1e−7, and midpoint orders in (1.7,2.3) with the finest difference below 1e−5. A finite-D pairwise comparison is checked against the sum of the two analytic bounds with an explicitly numerical 1e−8 slack; this is a consistency check, not a certificate of the computed states. Gram condition numbers and metric-transform defects are reported separately and are not converted into invented rounding bounds.

## Outputs and falsifiers

- `analytic_certificates.json`: eight exact endpoint certificates, including correctly inconclusive small-error results for the original full-strength drive.
- `comparison_summary.csv`: exact bound strings, all physical coefficients through the named protocol, numerical reference differences and conditioning diagnostics.
- `bound_curves.csv`: rational times, exact action intervals and analytic error bounds, alongside separately labeled computed differences.
- `numerical_histories.csv`: raw energy, independently integrated work, work defect and norm defect for all sixteen trajectories.
- `midpoint_histories.csv`: independent midpoint raw work and norm histories.
- `exact_step_certificate.json`: the exact two-step vector, exact Gram norm and total-error certificate.
- `numerical_comparisons.json`: D5/D6 reference refinement, fixed-D tolerance and independent midpoint comparisons.
- `driven_truncation_bounds.png` and `.svg`: bound curves and the matched-action comparison.
- `edge_tests.json`, `edge_tests_optimized.json`: exact fixtures, invalid-input rejection and independent finite-chain checks.
- `validation.json`: complete source hashes, environment versions and executed study gates. Failed reruns are marked failed.

All listed output files are under `output/`. Tests cover D=0, nonzero initial degree, zero time and drive, negative coefficients, discontinuous signed protocols, invalid Boolean/nonfinite inputs, missing certificate provenance and semantic mutations. Independent finite-chain matrix calculations challenge the factorial order. A signed pulse example has zero integrated signed coefficient but nonzero evolution error, proving why absolute values belong inside the action integral. A two-level example has zero terminal leakage and state distance 2, rejecting the claim that final leakage alone bounds the accumulated evolution error.

The new result closes a representation-truncation obligation for this driven finite graph. The single rational two-step fixture supplies a validated algorithm budget, exact arithmetic and exact initial preparation. A certified floating implementation of the four smooth protocols would still need its own validated integration and rounding budget. No claim here supplies a four-dimensional Yang–Mills construction.
