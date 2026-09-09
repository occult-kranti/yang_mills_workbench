## Independent verification: what the numerical checks establish

This review separates a wrong physical model, a wrong implementation and an overstated accuracy claim. They require different corrections. The previous report already stated that its 2.14e-16 agreement was not a sixteen-digit physical result, and already classified the smallest strong-field occupations as unresolved. Those qualifications were correct. This round adds an exact reference, more informative error measures and an independently implemented backreaction check. It does not manufacture an error merely because the previous answer was rejected.

### Occupation error is not norm error

Let $P$ be the exact orthogonal positive-energy projector, $Y$ the exact evolved occupied basis, and $\widehat Y=Y+\delta Y$. Writing $N=\|PY\|_F^2$ gives

$$
|\widehat N-N|\leq 2\sqrt N\,\|\delta Y\|_F+\|\delta Y\|_F^2.
$$

If the projector itself has error $\delta P$, there is an additional contribution bounded by $\|\delta P\|_2\|\widehat Y\|_F^2$. The Gram residual $\|\widehat Y^\dagger\widehat Y-I\|$ does not bound $\|\delta Y\|$: a perfectly normalized vector can point in the wrong direction. Conversely, a radial rescaling of a negative-energy state changes its norm while leaving its exact positive-energy projection zero. The executable counterexamples give a zero norm residual with an occupation error of approximately 1e-6, and a norm residual of approximately 2e-6 with zero occupation error. These are deliberately constructed counterexamples to an invalid inference, not evidence that the production calculation suffered those particular defects.

Computing $P_+=(I+H/\omega)/2$ can subtract quantities of order one to obtain a very small occupation. For three static Hamiltonians, where the true production is exactly zero, this formula gives signed values between approximately -2.73e-17 and 1.39e-17. Direct overlaps with the positive eigenvectors instead give nonnegative values below 1e-32. Neither formula alone supplies a rigorous floating-point error bound, but the overlap avoids this cancellation mechanism.

The flat $b=10,n=1,K=0$ test has an exact independent reference,

$$
N_{\rm flat}=2\left[\frac{\sinh\pi}{\sinh(\pi\sqrt{22})}\right]^2
=1.6950184976499554\times10^{-10}.
$$

The previous four-component projector result has an absolute error of 2.0988e-16, which is a relative error of 1.2382e-6. Its stable two-sector overlap result has an absolute error of 4.96e-20. The new independent overlap integration differs from the exact reference by 7.24e-20. Thus a small absolute inter-method discrepancy can coexist with substantially fewer reliable relative digits in a rare occupation. Renormalizing a vector removes radial drift only; it does not repair phase or mixing-angle errors.

The expansion-only counterexample also has an exact reference. A constant unitary maps

$$
h_s=a_g(s)\sigma_1-s\sqrt{2bn}\,\sigma_2+K\sigma_3,
\qquad a_g=1.5+0.5\tanh(2s)
$$

to a Sauter Hamiltonian with longitudinal offset 1.5, longitudinal amplitude 0.5, pulse duration 0.5, and transverse mass $\sqrt{2bn+K^2}$. For $b=10,n=1,K=0$, the exact two-sector occupation is approximately 1.8823980738606993e-6. An independently integrated spinor result differs by 6.89e-18. This confirms the earlier nonzero result and falsifies the zero-production shortcut, while removing the need to rely exclusively on two numerical implementations.

### Finite boundaries and initial states require their own test

The in/out conditions in these tests are temporal. There is no black-hole horizon in the prescribed homogeneous FLRW problem. An instantaneous eigenstate at a finite initial time equals the intended asymptotic in-vacuum only up to a separate boundary error. For a two-state Hamiltonian $h=\mathbf h\cdot\boldsymbol\sigma$, the local nonadiabatic scale is controlled by $|\mathbf h\times\dot{\mathbf h}|/|\mathbf h|^3$; small background amplitudes by themselves do not bound a tiny occupation's relative error.

For the expanding electric case, extending the dimensionless endpoint factor from $L=8$ to $L=16$ changes the computed occupation by approximately 2.58e-12. At relative tolerance 2e-13, extending $L=16$ to $L=20$ changes it by approximately 5.51e-18. At fixed $L=16$, tightening the tolerance from 2e-12 to 2e-13 changes the answer by approximately 2.86e-17. This provides an empirical plateau for the checked case. It does not establish a uniform error bound for every Landau level, momentum or background.

The new massive backreaction experiment starts in the exact magnetic vacuum with zero electric field, then applies a smooth compactly supported external current. All derivatives of the pump vanish at its start. This makes the selected initial state explicit and avoids silently identifying a finite-time instantaneous vacuum in an already nonzero electric field with an adiabatically dressed state. Different initial states remain different physical experiments, even if each numerical evolution conserves energy.

### Independent derivation of the matched finite-grid closure

The verifier uses two-component wavefunctions satisfying $i\psi'=h\psi$; the production solver evolves Bloch vectors. No production module is imported. With $p=k-a$, $a'=-x$, $h=M\sigma_1+p\sigma_3$ and $\omega=\sqrt{M^2+p^2}$, one has $p'=x$. Writing $\mathbf r=\psi^\dagger\boldsymbol\sigma\psi$ gives $\mathbf r'=2\mathbf h\times\mathbf r$.

The adiabatic expansion starts with $\mathbf r^{(0)}=-\mathbf h/\omega$ and

$$
\mathbf r^{(1)}=\frac{\mathbf h\times\mathbf h'}{2\omega^3},
\qquad
r_z^{(2)}=\frac{M^2x'}{4\omega^5}-\frac{5M^2p x^2}{8\omega^7}.
$$

The second term includes the longitudinal normalization correction from the first-order vector. Omitting it changes the coefficient. On a fixed shared quadrature, define

$$
S=\sum w\left(r_z+\frac p\omega\right),\quad
C=\sum w\frac{M^2}{4\omega^5},\quad
D=\sum w\frac{5M^2p}{8\omega^7},\quad
Z=1+\chi_B-e^2C.
$$

The proposed equation is

$$
Zx'=F_{\rm drive}-e^2(S+D x^2).
$$

Here $\chi_B$ is a specified on-shell finite magnetic susceptibility matching coefficient. The finite-grid construction is not a proof that every subtraction and cutoff limit reproduces the full four-dimensional renormalized effective action. Adiabatic subtraction and its compatibility with gravitational renormalization are substantive theoretical requirements, not merely ways to improve quadrature. [@V04]

For the chosen fixed grid, the exact common energy is

$$
W=\frac{Zx^2}{2}+e^2\sum w\left(\mathbf h\cdot\mathbf r+\omega\right).
$$

Since $C'=-2Dx$, differentiation gives $W'=xF_{\rm drive}$. This checks the signs and the common finite counterterms. It does not prove the uniqueness of the finite matching prescription: an incorrectly matched but consistently varied model can conserve its own energy too.

For $b=10,n_{\max}=2,K_{\max}=6,N_k=32$, pump duration 4 and final time 8, the independent spinor calculation has a maximum energy-minus-integrated-pump-work residual of 1.066e-11. Its maximum spinor norm error is 1.053e-11. The electric field at the final time is 0.9550507371994522 in critical units. This deliberately small grid is an implementation comparison, not a continuum result.

The subsequent production comparison uses the same finite grid and pump, while evolving real Bloch vectors instead of complex spinors. Across 81 output times, the two electric histories differ by at most 3.63e-12 and the vector potentials by at most 4.62e-12. The production energy-work residual is 1.17e-15; this smaller residual does not imply that its physical prediction is accurate to fifteen digits. The source hash was unchanged during the comparison. `implementation_comparison.json` records the exact parameters, source hashes and measured differences; `compare_implementations.py` reproduces this final comparison against the independently generated reference data.

### Two deliberate failures establish that the diagnostics have power

At finite momentum cutoff, the instantaneous-vacuum term is generally nonzero:

$$
\int_{-K}^{K}\frac{k-a}{\sqrt{(k-a)^2+M^2}}\,dk
=\sqrt{(K-a)^2+M^2}-\sqrt{(-K-a)^2+M^2}.
$$

For $K=2,a=M=1$, its value is -1.7480640977952844. Discarding this boundary term by appealing to oddness while the momentum window is not centered on the kinetic momentum changes the model. The independent defective evolution, which intentionally deletes this term, produces a maximum energy-work defect of 12.6099 and an electric-field difference of 4.0688 from the matched calculation. The actual production model retains the term.

For a constant gauge shift $a\mapsto a+C$, one must shift the canonical modes and the finite window by the same $C$. The independent translated-window test with $C=7.3$ changes the electric history by only 4.44e-16. Keeping the window fixed instead changes it by 0.0151097. This demonstrates regulator sensitivity. It does not test arbitrary local gauge transformations or the full Ward identities of an inhomogeneous four-dimensional theory.

### A separate exact anomaly benchmark

The massive subtraction formula must not be evaluated by simply setting its mass to zero. Use a distinct massless lowest-Landau-level model with an arbitrary fixed reference scale. Its Hamiltonian is diagonal, so an initially filled negative branch has $r_z(k,t)=-\operatorname{sgn}(k-a_0)$. The subtracted integral is

$$
\int_{-\infty}^{\infty}\left[-\operatorname{sgn}(k-a_0)+\operatorname{sgn}(k-a)\right]dk
=-2(a-a_0).
$$

Writing $\lambda=e^2b/(4\pi^2)$ yields $J=-2\lambda(a-a_0)$, $a'=-x$ and, without a drive,

$$
x''+2\lambda x=0,
\qquad \frac{x^2}{2}+\lambda(a-a_0)^2=\text{constant}.
$$

For $\lambda=0.1,x(0)=1,a(0)=a_0=0$, an independent oscillator integration agrees with the cosine electric field to 3.79e-12 over the tested interval, with an energy drift below 3.86e-12. Exact piecewise spectral-flow integration reproduces the coefficient and shows how a window that fails to enclose the spectral crossing clips the current. An oscillator solved correctly is a benchmark of this massless model, not a demonstration that the massive model inherits its exactness.

### Independent weak-frequency check

The proposed below-threshold response kernel can also be tested without the nonlinear implementation. Substituting $k=M\tan\theta$ into its longitudinal integral produces a smooth integrand. At $b=10$, 96 Gauss nodes in $\theta$, Landau levels through 8192, and frequencies 0.01, 0.02 and 0.04, extrapolation of $\Delta\chi/\nu^2$ to zero frequency gives 0.0015604099969639626. The finite-sum analytic value is 0.0015604099969628834, a difference of 1.08e-15. The infinite-Landau trigamma expression is 0.00156041094205709; the explicitly omitted coefficient tail is 9.45e-10.

The independent $B\to0$ longitudinal integral gives $e^2/(60\pi^2)=0.00015485463105144795$ for the coefficient of $\nu^2$. This checks a frequency-dependent term rather than only re-reading the static susceptibility supplied as input. It remains a response-kernel quadrature and limiting-formula check; a fitted response from a driven nonlinear evolution would be an additional test.

### Challenge the comparator literature as well

The 2025 linear-response study by Newsome, Anderson and Grotzke explicitly includes a retarded current commutator, which is nonzero even before pair production. Their selected near-critical-field cases show growing perturbations. Consequently, a converged mean-field trajectory and a conserved mean-field energy do not establish that neglected quantum fluctuations remain small. Their result is a model-specific warning and test design, not a theorem that every strong-field semiclassical calculation fails. [@V02] The earlier Pla et al. study used an approximate linear-response criterion; the later study supplies a direct comparison and a more informative baseline. [@V03]

Gralla and Mizuno derive a first-order-in-mass correction in bosonized 1+1-dimensional QED which is absent in the corresponding semiclassical prediction. Their controlled result motivates the separate period experiment supplied by the lead researcher. It must not be transferred quantitatively to a multi-Landau-level four-dimensional theory without matching its degrees of freedom and regime. The latest version, v2 of 9 April 2026, also distinguishes a conserved total energy from a naive split into quantum field and particle energies: Appendix B retains a nonfactorizing quadratic expectation value. [@V01]

There is a specific logical point to check in that comparison: a pointwise small-mass expansion containing $m/k$ is nonuniform near $k=0$. The absence of an order-$m$ term at each nonzero momentum does not by itself justify exchanging an expansion with an infinite integral. For a compact region this problem can be addressed directly. Let $u=r_x+i r_y$. Then

$$
u'=2ipu-2imr_z,\qquad r_z'=2m\operatorname{Im}u.
$$

For the exact massive initial vacuum, $|u(0)|=|m|/\sqrt{k^2+m^2}$, and unit Bloch norm implies

$$
|u(t)|\leq\frac{|m|}{\sqrt{k^2+m^2}}+2|m|T,\qquad 0\leq t\leq T.
$$

Therefore

$$
\int_{-K}^{K}|r_z(t)-r_z(0)|\,dk
\leq4m^2T\operatorname{arsinh}\left(\frac K{|m|}\right)+8Km^2T^2
=o(|m|)
$$

for fixed $K,T$. This excludes a hidden linear-mass contribution from the shrinking $k\sim m$ region in this fixed-time compact estimate. It is not a uniform ultraviolet or long-time proof: $K\to\infty$, times of order $1/m$, and the renormalized high-momentum tail still require separate control. The supplied script evaluates the bound across decreasing masses; it does not label a finite set of evaluations a proof of the asymptotic statement.

### Acceptance decision

Accept the corrected curved-mode counterexample, the finite-regulator backreaction implementation checks, the exact massless spectral-flow coefficient, and the response-coefficient quadratures within their stated scopes. Do not yet accept a continuum four-dimensional stress/current closure, a mean-field validity theorem, a coupled Einstein evolution or a solution of the original unrestricted problem. The immediate next gates are stable simultaneous momentum/Landau cutoff changes, independently prepared states, a retarded linear-response or fluctuation test, and stress-tensor matching compatible with the same current subtraction.
