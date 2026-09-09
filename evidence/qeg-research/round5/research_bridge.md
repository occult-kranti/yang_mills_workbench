# The next bridge: conserved stress before dynamical gravity

## What must be connected, and what is only a common framework

The intended large problem couples a classical metric and gauge field to quantum matter. A useful organizing action, in natural Heaviside–Lorentz units and signature \((-+++)\), is

\[
\begin{aligned}
S_{\rm loc}={}&\int d^4x\sqrt{-g}\bigg[
\frac{M_{\rm Pl}^2}{2}(R-2\Lambda)
-\frac14 f(\phi)F_{\mu\nu}F^{\mu\nu}
-\frac12(\nabla\phi)^2-V(\phi)\\
&+\bar\psi(i\gamma^\mu D_\mu-m(\phi))\psi
+c_1R^2+c_2R_{\mu\nu}R^{\mu\nu}
+\frac{c_3}{\mathcal M^4}(F_{\mu\nu}F^{\mu\nu})^2\\
&+\frac{c_4}{\mathcal M^4}(F_{\mu\nu}\widetilde F^{\mu\nu})^2
+\frac{c_5}{\mathcal M^2}RF_{\mu\nu}F^{\mu\nu}
+\frac{c_6}{\mathcal M^2}R_{\mu\nu}F^{\mu\alpha}F^\nu{}_{\alpha}
+\frac{c_7}{\mathcal M^2}R_{\mu\nu\alpha\beta}F^{\mu\nu}F^{\alpha\beta}
+\frac{\vartheta(\phi)}4F_{\mu\nu}\widetilde F^{\mu\nu}\bigg].
\end{aligned}
\tag{G1}
\]

Here \(M_{\rm Pl}^{-2}=8\pi G\), \(D_\mu=\nabla_\mu+ieA_\mu\), \(F=dA\), \(\widetilde F^{\mu\nu}=\epsilon^{\mu\nu\alpha\beta}F_{\alpha\beta}/2\), and \(\mathcal M\) denotes a stated effective-theory matching scale. This is a list of representative operators, not a complete independent operator basis or a prediction of their coefficients. Field redefinitions, boundary terms and four-dimensional curvature identities affect the basis. A constant \(\vartheta F\widetilde F\) is locally topological for an abelian field without monopole or boundary complications; a varying \(\vartheta\) changes the equations. Calling this term a new bulk force without specifying those conditions would be a mistake.

The coefficients must refer to a declared matching scheme and to degrees of freedom already integrated out. If the retained fermion's loop generates an Euler–Heisenberg contribution, count it once in the quantum effective action; do not add the identical loop again as an independent local term. A healthy two-derivative photon sector requires positive \(f(\phi)\) on the stated domain. Neither that condition nor an operator list guarantees a controlled ultraviolet completion.

The action connects subjects by shared variables. It does not prove that the Weak Gravity Conjecture, Festina Lente, cosmic censorship or singularity resolution follows from these operators. A charge-to-mass statement needs charge normalization, Planck convention, scalar forces and spacetime assumptions before it becomes a proposition. \(q/m\ge1\) alone is not a dimensionally universal axiom. The repulsive-force and black-hole-extremality versions require separate hypotheses. [Repulsive Forces and the Weak Gravity Conjecture](https://arxiv.org/abs/1906.02206), [Festina Lente](https://arxiv.org/abs/2106.07650).

Strong fields and curvature require another distinction. A local low-order Euler–Heisenberg polynomial is not uniformly justified when \(eE/m^2\sim1\), \(eB/m^2\gg1\), or curvature and derivative scales approach \(m^2\). A static real susceptibility is not the nonlocal retarded current of a pair-producing state. In a region of a source-free classical Einstein–Maxwell solution with zero cosmological constant, \(R=0\) even though the Riemann tensor can be large; Ricci scalar alone is therefore a poor curvature-validity test. A magnetar's strong magnetic field does not by itself imply electron-Compton-scale curvature. The appropriate checks involve field invariants, independent curvature components/invariants, frequencies, gradients, quantum state and approximation order.

For causal quantum feedback, the target object is a renormalized closed-time-path effective action \(\Gamma_{\rm CTP}[g^+,A^+;g^-,A^-;\omega_0]\), or an equivalent in-in construction. Its physical-branch variations must define a compatible current and stress tensor. A formal symbol \(\langle T_{\mu\nu}\rangle_{\rm ren}\) is not a closure until the state, subtraction, finite counterterms and evolution are supplied. If higher-curvature terms are retained, their metric variations must also enter the gravitational equations, or an explicit order-reduction prescription must replace them. G2–G9 below apply to the ordinary Einstein equations, or to a formulation where all additional contributions have consistently been moved into the conserved total source.

## A completed conditional interface lemma

Choose the axisymmetric homogeneous metric

\[
ds^2=-dt^2+a_\perp(t)^2(dx^2+dy^2)+a_\parallel(t)^2dz^2,
\quad H_\perp=\frac{\dot a_\perp}{a_\perp},\quad
H_\parallel=\frac{\dot a_\parallel}{a_\parallel},\quad
\theta=2H_\perp+H_\parallel.
\tag{G2}
\]

Assume positive scale factors, differentiable Hubble variables and total energy density, continuous directional pressures, constant \(\Lambda\), and \(\kappa=8\pi G\). The metric is dimensionful here; dots refer to physical proper time, whereas the selected finite theorem uses \(s=mt\). With diagonal comoving stress \(T^\mu{}_{\nu}=\operatorname{diag}(-\rho,p_\perp,p_\perp,p_\parallel)\), define

\[
\mathcal C=H_\perp^2+2H_\perp H_\parallel-\kappa\rho-\Lambda,
\quad Q=\dot\rho+2H_\perp(\rho+p_\perp)
+H_\parallel(\rho+p_\parallel).
\tag{G3}
\]

\(\mathcal C=0\) is the time-time Einstein constraint; \(Q=0\) is total energy conservation. Evolve the two spatial Einstein equations in the form

\[
\dot H_\perp=\frac{\Lambda-\kappa p_\parallel-3H_\perp^2}{2},
\tag{G4}
\]

\[
\dot H_\parallel=\Lambda-\kappa p_\perp-\dot H_\perp
-H_\perp^2-H_\parallel^2-H_\perp H_\parallel.
\tag{G5}
\]

Differentiate G3 without imposing the constraint:

\[
\dot{\mathcal C}=2(H_\perp+H_\parallel)\dot H_\perp
+2H_\perp\dot H_\parallel-\kappa\dot\rho.
\tag{G6}
\]

Substitute G4–G5 and replace \(\dot\rho\) by its definition through \(Q\). Collecting the cubic Hubble, cosmological and pressure terms gives the exact identity

\[
\boxed{\dot{\mathcal C}=-\theta\mathcal C-\kappa Q.}
\tag{G7}
\]

This algebra has two independent SymPy checks, including a deliberate wrong-coefficient mutation. With volume factor \(V=a_\perp^2a_\parallel>0\), \(\dot V/V=\theta\), integration gives

\[
\mathcal C(t)=\frac{V(0)}{V(t)}\mathcal C(0)
-\frac{\kappa}{V(t)}\int_0^t V(s)Q(s)\,ds.
\tag{G8}
\]

Therefore \(Q=0\) and \(\mathcal C(0)=0\) imply exact constraint propagation on every regular interval. Conversely, G8 quantifies how a Ward defect sources constraint error. Expansion damps the homogeneous constraint mode; contraction can amplify it. The coefficient is \(-\theta\) for G4–G5, not \(-2\theta\). Different off-constraint evolution systems can propagate constraint errors differently, so the evolution equations must accompany the coefficient.

For aligned physical electric and magnetic fields, the Maxwell and electromagnetic-stress equations are

\[
\begin{gathered}
\dot E+2H_\perp E=-(J_q+J_{\rm ext}),\qquad
\dot B=-2H_\perp B,\\
\rho_{\rm EM}=\frac{E^2+B^2}{2},\quad
p_{\perp,\rm EM}=\rho_{\rm EM},\quad
p_{\parallel,\rm EM}=-\rho_{\rm EM}.
\end{gathered}
\tag{G9}
\]

Direct differentiation yields \(Q_{\rm EM}=-E(J_q+J_{\rm ext})\). A compatible charged quantum sector must satisfy \(Q_q=EJ_q\). Omitting the driving apparatus then leaves \(Q_{q+\rm EM}=-EJ_{\rm ext}\), and even at \(\mathcal C=0\) one obtains \(\dot{\mathcal C}=\kappa EJ_{\rm ext}\). A support sector must account for the opposite work. Merely setting the electric drive to zero later does not repair a previously inconsistent constraint or supply the apparatus's pressures. Likewise, keeping \(B\) constant while \(H_\perp\ne0\) violates G9 unless an additional supporting mechanism is explicitly included.

This lemma connects conservation to constraints. It does not compute \(\rho_q,p_{\perp,q},p_{\parallel,q}\), prove a global gravitational solution, prevent a vanishing scale factor, or make an arbitrary pressure ansatz physically correct.

## Source audit: a theorem's domain travels with its citation

Zahn's locally covariant Dirac construction is relevant background, but section 4.2 explicitly treats constant mass and a gauge connection of vanishing curvature for its stated nonperturbative stress argument, with a perturbative background alternative discussed. It must not be cited as our already implemented strong-electromagnetic-field stress closure. For nonzero field strength the charged-matter force Ward identity must include electromagnetic work. The arXiv v3 is dated 18 October 2013; a recent HTML conversion timestamp does not create a new research revision. [Zahn, section 4.2](https://arxiv.org/html/1210.4031v3).

Meda, Pinamonti and Siemssen prove a local existence and uniqueness result for a specified scalar-field cosmology using a retarded inverse and a fixed-point construction. Their Theorem 5.9 requires compatible sufficiently regular state data; Remark 5.2 explains the mild-solution regularity and the additional requirements for a fourth derivative of the scale factor. This is a useful proof strategy to study, not a theorem for our charged Dirac Bianchi-I problem. [Theorem 5.9 and Remark 5.2](https://arxiv.org/html/2007.14665v1).

The earlier Pinamonti–Siemssen result extends a particular conformally coupled scalar cosmology until its specified singular boundary. The word “global” in its title does not establish singularity-free evolution for arbitrary semiclassical matter or geometry. Only the abstract and bibliographic scope were checked in this round. [Original record](https://arxiv.org/abs/1309.6303).

Stochastic-gravity validity also involves intrinsic and induced fluctuations. A bounded mean trajectory or a finite-time source derivative does not evaluate the symmetrized current/stress noise kernel. This remains a separate bridge. [Verdaguer](https://arxiv.org/html/gr-qc/0507073v1).

## Next obligations, with falsifiers and stopping rules

| Obligation | Constructive next step | Acceptance evidence | Failure that blocks promotion |
|---|---|---|---|
| Regulator limit | Specify a physical state family and a topology for renormalized current and energy; vary longitudinal window and Landau cutoff separately | Uniform bounds and a Cauchy/compactness argument, with counterterms tracked | Quadrature refinement alone or cutoff-dependent coercivity treated as a continuum theorem |
| Differentiate the limit | Establish uniform control of the variational kernel and justify limit–derivative interchange | A domination or operator-convergence theorem on fixed finite intervals | Pointwise convergence of trajectories without derivative control |
| Covariant stress | Construct current and both pressures in the same state and renormalization scheme | Flat matched limit, force Ward identity, finite-counterterm bookkeeping and independent residuals | Energy-only closure, mismatched subtraction, or conservation imposed by definition without testing the calculated observables |
| Gravity support | Include apparatus work/stress or formulate a closed system with admissible constrained initial data | G8 with independently computed total Q and initial constraint | An external current with its energy omitted |
| Noise and stability | Define smeared current/stress two-point observables and separate intrinsic from induced response | State-dependent finite observables and justified validity criterion | A pole in response divided by a zero field, or signed tangent work called a positive norm |
| Curved strong-field dynamics | Choose a regular short-time Bianchi interval and a controlled quantum closure before horizons | Local existence assumptions, constraint propagation and approximation error bounds | Inserting a flat fixed-B susceptibility into arbitrary curvature without a derivation |

The next selected scientific milestone is the covariant current/pressure Ward identity in a precisely specified charged-field state. G7 is now a completed conditional endpoint for that bridge: once the actual total source satisfies its premises, constraint propagation follows. Neither search directions nor agent agreement can replace the missing source construction.
