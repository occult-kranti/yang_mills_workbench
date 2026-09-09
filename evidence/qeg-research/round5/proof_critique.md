# Independent skeptical review of the finite-model theorem

Review date: 9 September 2026. Reviewed inputs: `round4/response_contract.md` and `round4/physics_acceptance.json`. This reviewer did not import the production response solver. Independent exact calculations are in `counterexamples.py`; their output is `counterexample_results.json`.

## Decision

The proposed global-existence and causal-response result is supportable as a **conditional theorem of the specified finite-dimensional model**. It is stronger than sampled numerical consistency but narrower than continuum quantum electrodynamics, a stability theorem, a quantum-noise calculation, or a theorem about the four original black-hole/gravity problems.

The important correction is to state every hypothesis before connecting the result to the next theory. In particular, the energy identity does not itself provide a coercive norm for the tangent, and a small sampled minimum of a denominator is not its global positive lower bound. For the selected exact mathematical regulator, a separate rational inequality does supply a positive denominator for every potential value.

## 1. Hypotheses that the proof needs

1. A finite, fixed list of modes, with real fixed canonical momenta, strictly positive masses, and positive weights. Zero weights can simply be discarded. The regulator is part of the theorem's model, not a quantity silently removed by the proof.
2. Fixed finite charge coupling and matching coefficient. The selected physical case has `e²>0`; `e=0` is a separate decoupled limit. No denominator involving `1/e²` may be used in that limit.
3. Initial `|r_i|<=1`. The equations conserve these norms. A pure state requires equality; the mixed-state extension requires the inequality. An arbitrary numerical vector outside the unit ball does not automatically satisfy the energy argument.
4. A lower bound `Z(a)>=z_*>0` for all reachable potential values, proved independently of a finite sample. The clean sufficient hypothesis is a bound for every real `a`. A bound valid only on a proposed region requires a separate proof that the trajectory cannot leave that region.
5. For a classical theorem on every finite time interval, a continuous prescribed drive on `[0,infinity)` is sufficient. A merely locally integrable drive gives an absolutely continuous Carathéodory solution and almost-everywhere identities; one must say that explicitly. A source with a finite-time nonintegrable pole is outside either statement across that pole.
6. For source differentiation, a differentiable initial-data family and a sufficiently regular source family. A convenient sufficient condition is a source continuously differentiable in `(t,lambda)` on compact sets. More generally, a `C¹` map into `L¹([0,T])` with appropriate uniform bounds supports an integral-equation proof. Pointwise parameter derivatives without domination are not enough to interchange differentiation and time integration.
7. For every finite comparison interval, the family must have a common parameter neighborhood and remain separated from `Z=0`. If the regulator is fixed and its all-`a` bound holds, the denominator requirement is uniform automatically. If masses, weights, coupling, or matching are varied, their derivatives and a uniform positive neighborhood must also be included.
8. A causal source-response claim needs the same initial state and source history before the perturbation begins. It does not apply to deliberately different initial states.

The standard local existence, compact-set continuation, and smooth parameter-dependence tools used here can be checked in Teschl's author-hosted text, Theorems 2.2 and 2.11 and Corollary 2.16; the discussion on printed page 42 treats measurable forcing. Only the relevant sections were consulted, not the entire book. [Teschl, *Ordinary Differential Equations and Dynamical Systems*](https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf)

## 2. Independent energy audit

Since `|h_i|=omega_i` and `|r_i|<=1`, Cauchy–Schwarz gives

\[
U=\sum_iw_i(h_i\cdot r_i+\omega_i)\ge0,
\qquad W=\tfrac12 Zx^2+e^2U\ge\tfrac12z_*x^2.
\]

The derivative signs are essential. From `p'=x`, direct differentiation gives

\[
U'=xS,\qquad C'=-2Dx,\qquad Z'=2e^2Dx.
\]

Therefore

\[
W'=Zxx'+e^2Dx^3+e^2xS=xF.
\]

All four identities, including Bloch-norm preservation, simplify to zero in the independent symbolic check. This is an exact algebra check for the stated equations; it is not an independent derivation of those equations from continuum QED.

At positive `W`, `d sqrt(W)/dt <= |F|/sqrt(2z_*)`. To cover an initial vacuum with `W=0`, apply the calculation to `sqrt(W+epsilon)` and then take `epsilon` down to zero. Consequently,

\[
\sqrt{W(t)}\le \sqrt{W(0)}+
 \frac{1}{\sqrt{2z_*}}\int_0^t|F(s)|\,ds,
\]

\[
|x(t)|\le \sqrt{\frac{2W(0)}{z_*}}+
 \frac{1}{z_*}\int_0^t|F(s)|\,ds.
\]

For every finite `T`, this bounds `x`; integrating `a'=-x` bounds `a` on `[0,T]`; the Bloch norms bound all mode coordinates. The trajectory therefore stays in a compact subset of the smooth state domain separated from `Z=0`, permitting continuation beyond every finite endpoint. This proves global forward existence and uniqueness under the hypotheses.

For an integrable drive on the entire half-line, `W`, `x`, `U` and the Bloch vectors are uniformly bounded. The energy argument only supplies a linear-in-time bound for `a`, not a uniform bound on `a`. These distinctions must remain visible in the theorem statement.

## 3. Exact certificate for the selected regulator

With the physical weights in P1, positive exact longitudinal quadrature weights summing to `2K`, and `e²=4 pi alpha`,

\[
e^2C(a)\le \frac{\alpha bK}{2\pi}
\sum_{n=0}^{N}\frac{2-\delta_{n0}}{M_n^3}.
\]

This bound is valid for every `a`; it does not depend on the chosen canonical nodes. For `b=10`, `K=20`, and `N=4` **inclusive**, use

\[
M_0^3=1,\quad M_1^3\ge84,\quad M_2^3\ge246,
\quad M_3^3\ge427,\quad M_4^3=729.
\]

The lower bounds follow from the integer comparisons `(1+20n)^3 >= L_n²` for the positive quantities involved. With `0<alpha<1/137`, `pi>157/50`, and the separately supplied `chi>=0` hypothesis,

\[
e^2C(a)<\frac{100}{137(157/50)}
 \left[1+2\left(\frac1{84}+\frac1{246}+\frac1{427}+\frac1{729}\right)\right]
=\frac{66325137500}{274510827927}<\frac14.
\]

The last comparison is an exact integer comparison, with positive margin

\[
\frac14-\frac{66325137500}{274510827927}
=\frac{9210277927}{1098043311708}>0.
\]

Thus `Z>3/4` for this exact model, independently of the numerical trajectory. The fraction for the strict margin above is copied from the executable rational certificate.

The conclusion applies to mathematical quadrature weights with the stated exact sum. Floating-point generated weights and rounded constants define nearby parameters. To make a machine-specific certificate, bound their weight sum, positivity and constant rounding with rational or interval arithmetic. Agreement of floating sums to a few ulps is a diagnostic, not that certificate. The large exact margin makes such an implementation certificate plausible, but this review does not substitute plausibility for execution.

## 4. Explicit failed inferences and counterexamples

### A. Pointwise positive `Z` is not a global separation theorem

Take one mode with `M=1`, `w=4`, `e²=1`, `chi=0`, `k=0`, and the admissible mixed state `r=0`. Prescribe

\[
p(t)=1-t,\quad a(t)=t-1,\quad x(t)=-1,\quad
\omega=\sqrt{1+p^2},\quad
F(t)=\frac{4p}{\omega}+\frac{5p}{2\omega^7}.
\]

Here `Z=1-omega^{-5}` is strictly positive on `[0,1)` and vanishes at `t=1`. The smooth source gives `F-S-Dx²=0`, so the trajectory solves the divided ODE before that time. All fields remain finite, but the divided equation reaches `0/0` at `t=1`. A possibly extendible undivided differential-algebraic equation is a different problem. This invalidates continuation based solely on a positive initial or sampled denominator.

### B. Energy positivity uses physical initial states and positive weights

For `M=1,p=0,w=1,r=(-2,0,0)`, `U=-1`. For `M=1,p=0,w=-1,r=(1,0,0)`, `U=-2`. These are outside the hypotheses. They demonstrate why dropping either Bloch admissibility or positive quadrature weights invalidates the coercivity step.

For `M=p=0`, the chosen vacuum normalization and several displayed fractions are undefined. A massless model might exist after a separate limiting or reformulation procedure, but it is not justified by substituting zero into this theorem.

### C. A conserved tangent work quantity does not bound the tangent

Use one mode with `M=w=e²=1`, `p=0`, `chi=0`, and the pure initial-state family

\[
r(0;\lambda)=(-\cos\lambda,0,\sin\lambda),\qquad a(0)=x(0)=0.
\]

At `lambda=0`, `eta(0)=(0,0,1)`, `delta W(0)=0`, while `u'(0)=-4/3` when `F=f=0`. The tangent-work identity stays zero, but the response is nonzero. The first variation of a positive energy is a signed linear functional, not a positive quadratic tangent norm.

Also, the theorem's mixed-state extension must not impose the pure-state constraint unconditionally: the admissible family `r(lambda)=(lambda,0,0)` at `lambda=1/2` has `r dot eta=1/2`. That inner product is conserved; it is zero only when the initial family preserves its Bloch radius.

### D. Bounded global trajectories need not have bounded all-time derivatives

The exact family `(cos(lambda t),sin(lambda t))` has unit norm for all time, whereas its parameter derivative has norm `t`. This example refutes the general logical implication from bounded solutions to bounded parameter sensitivities. It does not claim instability of the selected Maxwell–Dirac run.

Similarly, `x(t,lambda)=cos(t)+lambda sin(t)` has a finite absolute derivative at `t=pi/2`, but a ratio using the vanishing baseline field diverges. A relative-gain pole at an ordinary field crossing is not a singular physical response.

### E. Continuous parameter dependence is not differentiability

At fixed one-mode positive-gap parameters, set `r=0`, `x(t,lambda)=t|lambda|`, `a=-t²|lambda|/2`, and define `F=Zx'+e²(S+Dx²)`. Each trajectory is a valid smooth-in-time solution. The source family is continuous in the parameter, but the solution has opposite one-sided derivatives at zero. A differentiable source family cannot be omitted from a tangent theorem.

An additional general warning comes from a moving narrow source pulse: `F_lambda(t)=sgn(lambda) g(t/|lambda|)`, with `g` smooth and supported inside `(1,2)`. Its pointwise parameter derivative at zero is zero for every fixed time, while its integral is proportional to `lambda`. Thus differentiating only pointwise and then integrating loses the pulse. This is a warning about a missing domination hypothesis; it is not an executed Maxwell–Dirac experiment.

### F. Every finite cutoff can exist globally while the continuum data diverge

For modes `i=1,...,N`, take `M_i=1`, `k_i=i`, `w_i=1/i²`, initially `a=x=0` and `r_i=h_i/omega_i`, with `e²=1`, `chi=0`. For every potential `a`, `omega_i>=1`, so

\[
C(a)\le\frac14\sum_{i\ge1}i^{-2}\le\frac14(1+1)=1/2,
\qquad Z(a)\ge1/2.
\]

At the initial potential, `omega_i>=i`, hence `U(0)>=2 sum_{i=1}^N 1/i`, which diverges with `N`. Each finite truncation satisfies the existence assumptions, while its initial energy diverges in the infinite list. This is a mathematical counterexample to inferring a finite continuum energy from finite-model global existence, not an asserted physical ultraviolet state for QED.

## 5. Conditional next link to gravity

For aligned-field Bianchi I, write `H_perp=Hp`, `H_parallel=Hl` and

\[
\mathcal C=H_p^2+2H_pH_l-\kappa\rho-\Lambda,\qquad
Q=\dot\rho+2H_p(\rho+p_\perp)+H_l(\rho+p_\parallel).
\]

Using the two spatial Einstein equations supplied by the root advisor,

\[
\dot H_p=\frac{\Lambda-\kappa p_\parallel-3H_p^2}{2},
\]
\[
\dot H_l=\Lambda-\kappa p_\perp-\dot H_p-H_p^2-H_l^2-H_pH_l,
\]

the independent exact simplification is

\[
\dot{\mathcal C}=-(2H_p+H_l)\mathcal C-\kappa Q.
\]

Consequently, total Ward conservation and an initially satisfied constraint imply constraint propagation. The adjective **total** matters. Aligned electromagnetic fields have `rho_EM=(E²+B²)/2`, `p_perp_EM=rho_EM`, `p_parallel_EM=-rho_EM`. With the P27 Maxwell equations, their work balance is `-E(J_q+J_ext)`. Adding the quantum-matter work `+EJ_q` leaves `Q=-EJ_ext` if the external apparatus is omitted. Even at `C=0`, this gives `Cdot=+kappa E J_ext`.

This identifies a necessary support/source sector for any pumped gravitational experiment. It does not provide either directional quantum pressure, renormalized stress response, or a completed covariant quantum closure. Conversely, a correctly propagated constraint would not prove that an arbitrarily selected stress closure represents QED.

## 6. Review gates before promoting a claim

| Gate | Acceptance condition | What failure means |
|---|---|---|
| Model identity | The finite regulator, matching and positive weights are stated | Theorems and experiments refer to different systems |
| Exact algebra | Independently simplified norm, work and current identities | A sign or coefficient blocks the proof |
| Coercivity | Physical Bloch norms and a proved all-domain positive `Z` gap | The energy estimate cannot establish continuation |
| Zero-energy endpoint | Square-root regularization covers the prepared vacuum | A proof divided by zero at its own initial data |
| Continuation | All state components are bounded on each finite interval | Bounding the electric field alone is insufficient |
| Derivative regularity | A common parameter neighborhood and differentiable source/data family | Formal tangent equations need not be derivatives of solutions |
| Causal comparison | Identical initial states and pre-probe sources | Early response could simply be an initial-state perturbation |
| Claim scope | No asymptotic stability or continuum conclusion from this theorem | A logically unsupported theory connection |
| Gravity interface | Both pressures, total Ward conservation and initial constraint | Energy-only closure or unsupported pumping violates the bridge |
| Implementation proof | Exact or interval bounds for floating inputs if claimed | Numerical consistency is being mislabeled as certification |

The executable checks confirm identities and counterexamples. They are not Lean/Isabelle proof objects, an exhaustive proof search, or an automatic validation of the entire physical theory. The forward/backward proof frontier should stop at the missing continuum, covariant-stress, noise and initial-constraint lemmas rather than introducing an unjustified edge to a grand conclusion.
