# Four restricted extensions and the objections they resolve

Advisor derivation, 9 September 2026. The first three results concern the coefficient of the already specified finite Maxwell–Dirac model. The fourth is an exact stationary-vacuum linear-response lemma. These are conventional proofs under stated hypotheses; they are not formal proof-assistant certificates, new discoveries about continuum QED, or a solution of Einstein–QED. Numerical acceptance remains a separate record.

## R6-L1. Exact finite-window coefficient and its sharp integral bound

### Claim and domain

Fix `b>0`, finite `K>0`, integer `N>=0`, and `M_n²=1+2bn`, `d_n=2−δ_n0`. Replace longitudinal quadrature by its defining ordinary integral on the fixed canonical window `[-K,K]`, while retaining the finite Landau sum:

\[
C_{N,K}(a)=\frac{b}{16\pi^2}\sum_{n=0}^N d_n
\int_{-K}^K\frac{M_n^2\,dk}{[M_n^2+(k-a)^2]^{5/2}}.
\tag{L1}
\]

This coefficient is positive, even, and strictly decreasing as `a` increases from zero. Therefore its unique global maximum is `C_N,K(0)`. Its exact global denominator margin is `1+χ_b−e² C_N,K(0)`.

### Forward derivation

Define

\[
u_M(y)=\frac{y}{\sqrt{M^2+y^2}},\qquad
P_M(y)=\frac{u_M(y)-u_M(y)^3/3}{M^2}.
\tag{L2}
\]

Substitution gives `du/dy=M²/(M²+y²)^(3/2)` and `1−u²=M²/(M²+y²)`. It follows directly that

\[
P_M'(y)=\frac{M^2}{(M^2+y^2)^{5/2}}.
\tag{L3}
\]

The function `P_M` is odd. Evaluate L1 at its two endpoints:

\[
C_{N,K}(a)=\frac{b}{16\pi^2}\sum_n d_n
[P_{M_n}(K-a)+P_{M_n}(K+a)].
\tag{L4}
\]

Evenness follows by swapping the two summands. Let `f_M=P_M'`; this is even and strictly decreasing with its positive argument. Differentiation yields

\[
C_{N,K}'(a)=\frac{b}{16\pi^2}\sum_n d_n
[f_{M_n}(K+a)-f_{M_n}(K-a)].
\tag{L5}
\]

For `K>0,a>0`, `|K+a|>|K−a|`, so every bracket in L5 is strictly negative. Positivity of the weights proves the claim. Also `C_N,K(a)→0` as `|a|→∞`, since a finite collection of translated integrable kernels leaves the bounded window.

### Backward proof obligations and meeting

The target sharp global margin requires the global maximum of C. That requires evenness and monotonicity on the positive half line. The forward endpoint calculation establishes exactly these two obligations. No scan over sampled potentials is needed to establish the mathematical maximum.

### What this changes

The previous universal estimate bounded each retained mode by its individual peak and then added the peaks, even though different momenta peak at different potentials. L4–L5 give a sharper answer for the **continuous integral**, useful as an independent quadrature reference. They do not automatically sharpen the theorem for a fixed finite quadrature list.

### Counterexample to the tempting discrete inference

For a two-node Gauss–Legendre rule on `[-K,K]`, the nodes are `±K/√3` and both weights equal K. At `a=K/√3`, one retained `n=0` mode sits exactly at zero kinetic momentum. Its single contribution gives

\[
e^2 C^{\rm disc}(K/\sqrt3)
\ge\frac{\alpha bK}{4\pi}.
\tag{L6}
\]

The exact-integral `n=0` coefficient is bounded by its full-window value `e²b/(12π²)=αb/(3π)`, independently of K. At `b=10,K=20`, the discrete peak already exceeds this integral maximum. At `K=200`, L6 exceeds one for the stated illustrative α, and numerical evaluation verifies a negative discrete denominator even though the integral denominator is positive. These examples disprove transfer of the integral certificate; they do not disprove positivity of the quadrature weights or their polynomial exactness. A non-polynomial narrow peak can be badly resolved.

Negative or zero K, nonpositive b, negative/nonintegral N and nonfinite arguments are outside the claim. An off-center window has its maximum at that window's center in the corresponding fixed canonical gauge, not necessarily at a coordinate value named zero. The physical transformation shifts canonical momenta and potential together; holding the window fixed while changing a is the regulator geometry being studied here.

For very large `|a|/K`, the analytic difference in L4 can lose digits when implemented in floating point. The exact formula remains correct; stable numerical evaluation and range checks are a separate obligation.

## R6-L2. A uniform Landau-cutoff certificate at fixed longitudinal window

### Claim and domain

At `b=10,K=20`, choose any **finite** Landau cutoff N. On each retained level use positive longitudinal quadrature weights whose sum is exactly `2K`; the nodes need not have any particular spacing. With the already specified matching and `α<1/137`, the exact coefficient obeys

\[
Z(a)>\frac34\qquad\text{for every real }a.
\tag{L7}
\]

The number of retained Landau levels is unrestricted but finite. This strengthens the previous certificate, which explicitly stopped at N=4. Each resulting finite-dimensional ODE separately inherits the round-5 continuation theorem. The statement does not turn an infinite list of modes into a finite-dimensional ODE.

### Proof

Because `ω_nj>=M_n`, the total weight per level gives

\[
C^{\rm disc}(a)\le\frac{bK}{8\pi^2}
\left[1+2\sum_{n=1}^N(1+2bn)^{-3/2}\right].
\tag{L8}
\]

For the positive decreasing function `f(t)=(1+20t)^(-3/2)`, each `f(n)` is bounded above by its integral over `[n−1,n]`. Thus

\[
\sum_{n=5}^{\infty}f(n)\le\int_4^\infty f(t)dt=\frac1{90}.
\tag{L9}
\]

Using the four earlier conservative lower bounds for the mass cubes and `π>157/50`,

\[
\begin{aligned}
e^2 C^{\rm disc}(a)
&<\frac{100}{137(157/50)}
\left[1+2\left(\frac1{84}+\frac1{246}+\frac1{427}+\frac1{729}+\frac1{90}\right)\right]\\
&=\frac{67743204500}{274510827927}<\frac14.
\end{aligned}
\tag{L10}
\]

The final inequality is checked by exact integer comparison, `270972818000 < 274510827927`. The matched susceptibility is strictly positive for b>0 by the Binet integral and digamma recurrence already used in round 5. Therefore `1+χ_b−e²C>3/4`, proving L7. The scalar integral also satisfies the same upper estimate.

The backward global-existence route required a global positive denominator. The forward tail estimate now supplies that hypothesis for every finite N at this fixed K. This is a successful extension of one part of the theorem, not a limit-exchange theorem.

### A coefficient-only convergence corollary

Fix any b,K>0. Suppose increasing N retains exactly the already selected per-level quadratures and adds new levels; each level has positive weights summing to 2K. The same integral comparison gives

\[
e^2\sup_{a\in\mathbb R}
|C_{\infty,K}^{\rm disc}(a)-C_{N,K}^{\rm disc}(a)|
\le\frac{\alpha K}{\pi\sqrt{1+2bN}}.
\tag{L10a}
\]

Indeed the positive tail is bounded by `αbK/π` times `Σ_(n>N)(1+2bn)^(-3/2)`, and the latter is at most `1/[b sqrt(1+2bN)]`. This proves uniform convergence in a of this **coefficient series alone**. The same bound holds for the exact momentum integral. If an implementation changes previously retained quadratures when N changes, its additional replacement error is not covered by this tail estimate. No current, state, energy or trajectory limit follows from L10a alone.

### What the skeptic still blocks

Even though the lower denominator bound is uniform in N, the theorem's state dimension increases with N. Bounds or convergence for the renormalized current, total initial energy, source response and physical state family are still required. Initial energies can grow with N for inadmissibly excited ultraviolet tails. A uniform denominator alone cannot establish a Cauchy sequence of solutions, justify differentiating a limit, or produce a Hadamard continuum state. Exact positive quadrature weights and rounded machine-generated coefficients must also be distinguished; the rational result is an exact-coefficient theorem.

## R6-L3. The fixed-matching joint-cutoff obstruction

### Claim and domain

Keep b, e² and the specified susceptibility χ_b fixed. In the continuous longitudinal integral model at `a=0`, let both the canonical window K and the Landau cutoff N tend to infinity. Then C tends to positive infinity, and `Z=1+χ_b−e²C` tends to negative infinity. In particular there is no positive lower bound uniform over this cofinal regulator family. This disproves an extension of the existing positive-energy continuation route to the joint cutoff limit **without a new derivation of the renormalized equations**.

### First direction: exact full-momentum sum

In L2, `u_M(K)→1` as `K→∞`, so

\[
C_{N,\infty}=\frac{b}{12\pi^2}
\left[1+2\sum_{n=1}^N\frac1{1+2bn}\right].
\tag{L11}
\]

Set `z=1/(2b)`. Iterating the exact recurrence `ψ(z+1)−ψ(z)=1/z` rewrites the sum as

\[
C_{N,\infty}=\frac{1}{12\pi^2}
[b+\psi(N+1+z)-\psi(1+z)].
\tag{L12}
\]

Subtracting it from the **same** matched susceptibility gives

\[
Z_{N,\infty}=1-\frac{e^2}{12\pi^2}
[\log(2b)+\psi(N+1+z)].
\tag{L13}
\]

The positive-argument digamma grows as log N; hence L13 tends to minus infinity. This divergence also follows directly from the harmonic series in L11, without any asymptotic approximation. The special-function references support the recurrence and the optional growth illustration, not a physical identification of the divergence. [DLMF recurrence](https://dlmf.nist.gov/5.5.E2), [DLMF asymptotics](https://dlmf.nist.gov/5.11.E2).

### Reverse challenge: does an iterated limit prove every joint path?

An iterated limit alone would not generally be sufficient. Here positivity and monotonicity in both cutoffs resolve the objection. For any threshold A, select a finite N0 with `C_N0,∞>A`. Since the fixed finite sum converges as K grows, choose a finite K0 with `C_N0,K0>A`. Every pair with `N>=N0,K>=K0` then obeys `C_N,K>=C_N0,K0>A`. Every cofinal sequence eventually has both inequalities, even if its individual steps are not monotone. This is the joint divergence theorem.

An explicit comparison path is `K>=sqrt(1+2bN)`. Then each `u_n>=1/√2`, and the defining one-level integral including its factor 1/4 satisfies

\[
\int_{-K}^K\frac{M_n^2\,dk}{4(M_n^2+k^2)^{5/2}}
\ge\frac5{12\sqrt2 M_n^2}.
\tag{L14}
\]

Its positive Landau sum diverges harmonically. A finite numerical series illustrates this inequality; it is not needed to prove the infinite limit.

### A further finite-parameter corollary

The joint result ensures some finite N,K have `Z_N,K(0)<0`. For every fixed such finite pair, continuity and `C_N,K(a)→0` imply `Z_N,K(a)→1+χ_b>0` as `|a|→∞`. The intermediate value theorem therefore gives at least one zero at positive a and its even partner at negative a. This proves the coefficient develops singular surfaces for some finite members of the formal family. It does not prove that any selected physical trajectory reaches a zero, that the numerator fails to vanish there, or that an appropriately implicit or newly renormalized system has no solution.

### What is rejected, rather than solved

The current is a **combination** of state-dependent modal terms and subtraction terms. Divergence of C in the explicitly divided finite formula is not by itself a proof that a consistently renormalized current diverges. Cancellations with the regulated S and a differently organized common subtraction may matter. Consequently the accepted negative result is about uniform coefficient positivity and this particular coercive proof route. It is not a theorem of nonexistence of continuum QED, a physical Landau-pole measurement, an instability at N=4, or permission to tune χ independently of the current and energy. A changed matching requires a new common derivation and a new conservation audit.

The approximate zero of L13 is at `log N≈12π²/e²−log(2b)`. The logarithm is an illustrative asymptotic estimate at an enormous formal scale. There is no reason to construct arrays of that size, and treating a rounded asymptotic value as an exact critical integer would be a numerical error.

## R6-L4. Stationary-vacuum second variation: a positive response energy

### Precise target

The prior signed first variation of energy, δW, is not a positive norm and cannot establish stability of a pumped trajectory. A smaller claim is provable at an exact stationary vacuum. Fix any finite mode list and any real a0 with `Z0=Z(a0)>0`. Let

\[
F=0,\quad x=0,\quad p_i=k_i-a_0,\quad
\mathbf r_i=-\mathbf h_i/\omega_i.
\tag{L15}
\]

All base variables are stationary. Consider the **fixed-grid** linear response with variables `v=δa`, `u=δx`, `q_i=−v`, and pure-state tangent data `h_i·η_i=0`. Allow an additive perturbing drive f. Every coefficient below is evaluated at this stationary base.

Define

\[
\mathbf t_i=\partial_{p_i}(\mathbf h_i/\omega_i)
=\frac{\hat z}{\omega_i}-\frac{p_i\mathbf h_i}{\omega_i^3},
\quad \boldsymbol\xi_i=\boldsymbol\eta_i+q_i\mathbf t_i.
\tag{L16}
\]

The notation ξ in this section is a transformed first variation, not a second derivative of a Bloch vector. Since `h·t=0`, ξ remains transverse to h.

### Complete reduced linear system

At the stationary vacuum, the full tangent equations reduce without discarding terms to

\[
v'=-u,\qquad
Z_0u'=f-e^2\sum_iw_i\xi_{iz},\qquad
\boldsymbol\xi_i'=2\mathbf h_i\times\boldsymbol\xi_i+u\mathbf t_i.
\tag{L17}
\]

To check the reduction: `q'=u`; the base has `x=x'=0`, so the quadratic and quotient-variation terms vanish for a stated reason. Its spin equation is `η'=2h×η+2q ez×r=2h×(η+q t)`. Its current variation is `Σw(η_z+M²q/ω³)=Σw ξ_z`. These identities are exact only at this vacuum base. A pumped trajectory has additional terms.

Define the quadratic form

\[
\mathcal E_2=Z_0u^2+e^2\sum_iw_i\omega_i|\boldsymbol\xi_i|^2.
\tag{L18}
\]

All its coefficients are positive. Because h·ξ=0, `ω ξ·t=ξ_z`; precession is orthogonal to ξ. Differentiation gives

\[
\begin{aligned}
\mathcal E_2'
&=2u\left[f-e^2\sum_iw_i\xi_{iz}\right]
+2e^2u\sum_iw_i\omega_i\boldsymbol\xi_i\cdot\mathbf t_i\\
&=2uf.
\end{aligned}
\tag{L19}
\]

Therefore source-free tangent evolution preserves this positive quadratic form. In particular

\[
|u(t)|\le\sqrt{\mathcal E_2(0)/Z_0}\quad(f=0),
\tag{L20}
\]

and with a continuous or locally integrable perturbing source, the same epsilon-regularized argument as round 5 yields

\[
\sqrt{\mathcal E_2(t)}\le\sqrt{\mathcal E_2(0)}
+\frac1{\sqrt{Z_0}}\int_0^t|f(s)|ds.
\tag{L21}
\]

This is a finite-dimensional constant-coefficient linear system, so it exists at all finite times directly. Its positivity only requires the base value Z0>0, not a claim about every a in nonlinear neighboring trajectories.

### Why this is a second variation and what it does not bound

For a twice differentiable pure-state family, differentiate `|r|²=1` twice. At the vacuum, `h=−ωr`, so the term from the second Bloch derivative equals `ω|η|²`. The remaining second-order terms in U are `2qη_z+M²q²/ω³`; completing the square gives exactly `ω|η+q t|²`. The x=0 base contributes `Z0u²` to δ²W. Thus L18 is δ²W on the admissible pure-state tangent manifold, rather than the signed first variation δW.

There is a zero direction in the original variables: `u=0`, `v=c`, `η_i=c t_i`, so ξ=0. It is the tangent to the family of stationary vacua obtained by changing a0 and re-preparing the corresponding vacuum while holding the finite canonical list fixed. This must not be mislabeled as the simultaneous-grid gauge null used in round 4. L18 is positive definite in `(u,ξ)` but semidefinite in `(v,u,η)`.

Consequently the accepted conclusion is bounded electric tangent and bounded transformed mode perturbations. It is not a proof of bounded potential tangent, bounded original η for all time, stability of a pumped solution, nonlinear orbital stability, or quantum-noise control. General norm-changing variations have `h·η!=0` and need a different analysis; deleting this premise breaks the cancellation used in L19. The proof is a response-energy result on a specified tangent subspace.

The independent skeptic supplied an exact secular counterexample within this very model. Set one mode `M=w=e²=1,p=0,Z0=3/4`, take `u=1`, `q=t`, `ξ=(0,−1/2,0)`, `v=−t`, and `η=(0,−1/2,−t)`. L17 holds exactly, tangency to `h=(1,0,0)` holds, and `E2=1` is constant, while `|η|` grows without bound. This is why the word stability must carry its observable and subspace; a positive transformed energy does not bound every original coordinate.

### Executed independent checks and further falsifiers

Independently check L19 symbolically using `h·ξ=0`; build a one-mode real matrix for `(u,ξ)` in an orthonormal basis perpendicular to h and check the weighted skew-adjoint relation `AᵀG+GA=0`. Evolve with a matrix exponential or a separate ODE solver, compare the energy, and test a forced pulse against L21. Include deliberate defects: reverse the feedback sign, drop the contact term before transformation, and supply a longitudinal η outside the admissible tangent space. These tests can disprove an implementation; they do not replace the algebraic proof. No new production or pumped-run claim should be made without its own experiment contract.

The skeptic executed the general symbolic identity, an incorrect transformed-shift control and the exact secular solution above. For one mode `M=w=e²=1,p=0,Z0=3/4`, in coordinates `(u,ξ_y,ξ_z)`, they also checked

\[
A=\begin{pmatrix}0&0&-4/3\\0&0&-2\\1&2&0\end{pmatrix},\quad
G=\operatorname{diag}(3/4,1,1),\quad A^TG+GA=0.
\tag{L22}
\]

A matrix-exponential calculation starting from `(0.3,−0.2,0.4)` retained its exact initial quadratic energy `107/400` to a maximum relative discrepancy `2.054431391362439e-14` over the four requested times through t=10. This is a numerical cross-check, not a floating-point interval enclosure. The forced-pulse illustration remains a proposed experiment; the forced identity L19 is established symbolically.

## Decisions shared across all four results

The skeptic's job is to identify a failing implication, not to be defeated by extra parameter scans. In this round, the skeptical objections produce both a stronger fixed-window theorem and a genuine obstruction to a broader limit. A new theorem enters the dependency map only with its hypotheses, exact derivation, independent review status and source/code version. A numerical curve cannot silently supply an exact Horn-rule premise.

The next physical obligation is unchanged: common renormalized current and directional stress in a declared state, followed by the force Ward identity and the compatible gravitational initial-value system. The new obstruction makes that obligation more specific. The stationary-vacuum lemma provides a useful restricted response baseline, while the integral coefficient supplies an independent numerical reference for future finite-regulator experiments.
