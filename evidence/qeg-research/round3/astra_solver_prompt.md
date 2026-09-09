## Targeted solver specification for GPT Astra

### Role, target and output contract

Act as a computational QED researcher with a separate adversarial verification role. Reproduce and extend the following *specified* homogeneous semiclassical Maxwell–Dirac experiment. Quantize the charged fermion; evolve the classical electric expectation field causally from its current. Use a static uniform parallel magnetic field and initially the exact magnetic vacuum. Do not claim to solve the full multipolar Einstein–QED system. Provide derivations that a reviewer can check, complete runnable code, environment versions, convergence tables, raw invariants and a precise account of failed gates. Use NumPy/SciPy and SymPy; use mpmath for independent analytic references. Do not substitute a PINN before a conventional reference exists.

### Geometry, scales and state

Use natural Heaviside–Lorentz units, signature $(-+++)$, physical mass $m>0$, physical charge magnitude $e>0$, $e^2=4\pi\alpha$, and $\alpha=1/137.035999084$. The spacetime is Minkowski:

$$ds^2=-dt^2+dX^2+dY^2+dZ^2.$$

With dimensionless coordinates $(s,\xi,\eta,\zeta)=m(t,X,Y,Z)$, the metric is $m^{-2}\operatorname{diag}(-1,1,1,1)$ and its connection and curvature vanish. Landau gauge may be chosen for the constant $B$; the electric connection is homogeneous $A_z(t)$. No cosmological scale factor is hidden in the notation.

Define $a=eA_z/m$, $x=eE_z/m^2$, $b=|eB|/m^2$, canonical longitudinal momentum $k$, kinetic momentum $p=k-a$, $M_n^2=1+2bn$, and $\omega_{nk}=(M_n^2+p^2)^{1/2}$. The positive-charge member is used to define the reduced one-particle Hamiltonian. With the negative branch initially occupied, no extra particle/antiparticle degeneracy factor is added.

### Complete differential system

For each mode evolve the real Bloch vector $\mathbf r=(r_1,r_2,r_3)$:

$$a'=-x,\quad r_1'=-2pr_2,\quad
r_2'=2(pr_1-M_nr_3),\quad r_3'=2M_nr_2.$$

On a fixed canonical Gauss–Legendre grid, with $n=0,\ldots,N$ and positive longitudinal weights $w_i^{(k)}$, use

$$w_{ni}=\frac{b(2-\delta_{n0})}{4\pi^2}w_i^{(k)},$$
$$S=\sum_{ni}w_{ni}(r_3+p/\omega),\quad
U=\sum_{ni}w_{ni}(M_nr_1+pr_3+\omega),$$
$$C=\sum_{ni}w_{ni}\frac{M_n^2}{4\omega^5},\qquad
D=\sum_{ni}w_{ni}\frac{5M_n^2p}{8\omega^7}.$$

Use the physical finite magnetic matching term

$$\chi_b=\frac{e^2}{12\pi^2}
\left[b-\ln(2b)-\psi\!\left(1+\frac1{2b}\right)\right],
\qquad Z=1+\chi_b-e^2C,$$

where $\psi$ is digamma. For very small positive $b$, use a cancellation-safe proper-time or asymptotic evaluation with a checked overlap region; the production experiment uses $b=10$ and the formula is well conditioned. The exact $b=0$ transverse continuum is a separate limit, not a zero-weight Landau grid.

Close Maxwell's equation and integrate accumulated pump work $I_W$:

$$x'=\frac{F(s)-e^2(S+Dx^2)}{Z},\qquad I_W'=xF(s).$$

All right-hand sides now depend only on the current state, fixed grid and specified pump. The full matter current is

$$\mathcal J=S+Dx^2-Cx'+\chi_b x'/e^2=(F-x')/e^2.$$

Do not label $S+Dx^2$ the full physical current; it is the effective numerator after moving local polarization to the left side. Compute the subtracted integrands before summing to reduce avoidable cancellation. Never clip occupations or renormalize Bloch vectors inside the evolution to make an invariant look exact.

### Initial and asymptotic conditions

At $s=0$, set $x=0$, $a=a_0$, $I_W=0$, and

$$\mathbf r_{ni}=-\frac{(M_n,0,k_i-a_0)}{\sqrt{M_n^2+(k_i-a_0)^2}}.$$

For $s\leq0$, this static magnetic vacuum is the preparation. On $0<s<T_p$, set $u=s/T_p$ and

$$F(s)=\frac{x_{\rm target}}{T_pI}
\exp[-1/(u(1-u))],\qquad
I=\int_0^1\exp[-1/(v(1-v))]dv.$$

Set $F=0$ elsewhere. For $s>T_p$, impose no final electric value: solve the source-free evolution. There is no spatial horizon or distinguished radial origin in this homogeneous model, so horizon boundary data would be spurious. The ultraviolet mode boundary is an integration limit, not a spacetime infinity condition. Begin with finite $k\in[a_0-K,a_0+K]$ and increase $K$, node count and Landau cutoff separately. Do not impose a vacuum final state while pairs or coherent polarization remain present. A late field oscillation need not have a static $s\to\infty$ limit.

A residual gauge test changes $a_0$ and every canonical node by the same constant. Holding the window fixed changes the regulator and is a deliberately inequivalent comparison.

### Required derivation and analytic gates

Before coding, verify symbolically:

1. $p'=x$, $|\mathbf r|^2{}'=0$, and $U'=xS$ at any fixed quadrature.
2. The second-order current subtraction is $c=M_n^2x'/(4\omega^5)-5M_n^2p x^2/(8\omega^7)$ and its common energy term is $u_2=M_n^2x^2/(8\omega^5)$; verify $u_2'=xc$.
3. $C'=-2Dx$ and the exact finite-grid identity $W'=xF$ for $W=Zx^2/2+e^2U$.
4. The full-longitudinal integral of $M_n^2/(4\omega^5)$ is $1/(3M_n^2)$; subtract a matched zero-field transverse continuum and recover $\chi_b$.
5. Independently recover $\chi_b$ from the proper-time integral, its weak-field limit $\alpha b^2/(9\pi)$ and the below-threshold frequency coefficient. Keep physical finite matching distinct from regulator convergence.

### Discretization and execution

Use vectorized mode arrays and DOP853 or a demonstrably equivalent adaptive high-order integrator. Integrate source work as a state variable. Avoid estimating it with a coarse trapezoid over saved plots. Stop with an explicit failure if the integration fails, a nonfinite value occurs or $Z$ approaches the declared positive floor. A negative denominator is not automatically a physical instability.

First run a small shared-regulator comparison: $b=10$, $N=2$, $K=6$, 32 nodes, $T_p=4$, $s_f=8$, 81 output times. Implement independent complex-spinor equations $iy'=(M_n\sigma_1+p\sigma_3)y$ without importing production dynamics. Compare histories and energy/work residuals, not only a final number.

Then reproduce the final experiment: $b=10$, $N=8$, $K=40$, 4096 nodes, $T_p=4$, $x_{\rm target}=1$, $s_f=50$, 251 output times, relative tolerance $2\times10^{-10}$, absolute tolerance $2\times10^{-12}$ and maximum step 0.05. Expect approximately $x(50)=-0.03757$ within the explicitly reported finite-model tests, not eleven-digit certified accuracy. Keep exact machine outputs in data files.

Vary ODE tolerance independently of quadrature. Compare 1024, 2048 and 4096 nodes at fixed $K=40$; compare $K=40$/2048 with $K=60$/3072; compare $N=8$ with $N=12$. Report field and full-current histories separately. Distinguish sampled maxima from event-located extrema. A window enlargement at nearly fixed central spacing does not replace node refinement.

For the physical-response check use $b=100$, target 0.01, pump duration 20 and final time 40. Compare the measured late-field mean with $0.01/(1+\chi_b)$ and repeat with omitted/sign-reversed matching as explicitly wrong controls. A consistently wrong model may conserve its own energy: acceptance needs both conservation and physical matching.

### Deliverables and extension gate

Return runnable Python files, requirements, commands, source hashes, JSON/CSV histories and a gate ledger containing failures. Report absolute energy error, the actual physical normalization scale, relative error, raw mode norm defects, raw occupation extrema, minimum $Z$, gauge test, independent implementation discrepancy and each numerical limit. Provide no blanket “all tests passed” if a stricter requested target failed.

Keep the full quantum one-dimensional bosonized comparator separate; it tests a known missing mean-field correction in another theory. For gravitational extension, start from the supplied Bianchi-I equations and compute both directional pressures with common covariant current/stress counterterms. Require the Einstein constraint and Ward identity before evolving the metric. Do not substitute $m\to ma(t)$ into the flat subtraction or identify the current calculation as a proof of semiclassical validity. The original charged horizons, strong curvature and multipolar fields remain future geometry-matched problems.

