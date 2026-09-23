# P3: causal tangent response of the matched Maxwell–Dirac model

Contract version 1, frozen 9 September 2026. This document supplies the equations and acceptance conditions for the new response implementation. Numerical results and acceptance decisions belong in `response_advisor_review.md`; derivation is not execution evidence.

## Decision and physical scope

The next executable advance is the first variation of the coupled quantum-mode/electric-field evolution. A small change in the external preparation current changes the electric field, which changes every occupied Dirac mode and hence changes the subsequent current. Evolving those variations together tests this feedback without subtracting two almost equal solutions at every integration step.

The background remains spatially homogeneous, flat, collisionless and at fixed magnetic field. The charged field is quantized in a pure quasifree initial state; the electromagnetic background follows its mean current. Only the homogeneous longitudinal response sector is included. The mathematical model has an explicitly finite Landau/momentum regulator with the same on-shell magnetic susceptibility matching as round 3. The implemented result cannot certify continuum QED, all perturbation channels, electromagnetic quantum fluctuations, or gravitational backreaction.

Newsome, Anderson and Grotzke directly studied a retarded-current response in a different, 1+1-dimensional spinor model. Their necessary validity criterion and comparison to nearby nonlinear trajectories motivate our separate tangent and finite-difference checks. Their numerical conclusions cannot be transferred to our 3+1-dimensional Landau sum. [R01]

## 1. Fixed background equations and conventions

Use natural Heaviside–Lorentz units and signature \((-+++ )\), with physical fermion mass \(m>0\) and charge magnitude \(e>0\). The dimensionless variables are

\[
s=mt,\qquad a=eA_z/m,\qquad x=eE_z/m^2,\qquad b=|eB|/m^2>0.
\]

For each fixed canonical momentum \(k_i\) and Landau index \(n\), define

\[
p_i=k_i-a,\quad M_i=\sqrt{1+2bn},\quad
\omega_i=\sqrt{M_i^2+p_i^2},\quad
\mathbf h_i=(M_i,0,p_i),\quad
w_i=\frac{b(2-\delta_{n0})w_{k_i}}{4\pi^2}.
\tag{P1}
\]

All sums below run over the same positive fixed weights. There is no additional particle/antiparticle factor of two. A Bloch vector represents one occupied negative-energy state per block, \(\mathbf r_i=y_i^\dagger\boldsymbol\sigma y_i\), with \(y_i^\dagger y_i=1\).

\[
S=\sum_iw_i(r_{iz}+p_i/\omega_i),\quad
C=\sum_iw_i\frac{M_i^2}{4\omega_i^5},\quad
D=\sum_iw_i\frac{5M_i^2p_i}{8\omega_i^7},
\tag{P2}
\]

\[
\chi_b=\frac{e^2}{12\pi^2}\left[b-\log(2b)-\psi\!\left(1+\frac1{2b}\right)\right],\qquad
Z=1+\chi_b-e^2C.
\tag{P3}
\]

The round-3 theory independently matches this static magnetic susceptibility to its proper-time expression. It is retained exactly once. This calculation is a first derivative of that specified matched model; it does not rederive the four-dimensional continuum subtraction from a new covariant regulator.

\[
a'=-x,\qquad
x'=\frac{F-e^2(S+Dx^2)}{Z},\qquad
\mathbf r_i'=2\mathbf h_i\times\mathbf r_i.
\tag{P4}
\]

Here \(F=-eJ_{\rm ext}/m^3\) specifies an external-current drive. Stop on nonfinite quantities or \(Z\leq Z_{\rm floor}\), report the minimum \(Z\), and distinguish a regulator-conditioning failure from a physical instability. The support and time-independent energy of the magnetic background are external to this flat-space experiment.

The matter-current and energy definitions are

\[
J=S-Cx'+Dx^2+\frac{\chi_b}{e^2}x',\qquad
U=\sum_iw_i(\mathbf h_i\cdot\mathbf r_i+\omega_i),
\tag{P5}
\]

\[
\rho_q/m^4=U-Cx^2/2+\chi_bx^2/(2e^2),\qquad
W=Zx^2/2+e^2U.
\tag{P6}
\]

Thus \(x'=F-e^2J\), \(U'=xS\), \(C'=-2Dx\), and \(W'=xF\) exactly at the fixed regulator. Current evaluation should perform the subtraction inside the weighted sum, `sum(weights*(rz+p/omega))`, to avoid unnecessary cancellation between two large completed sums.

## 2. What is varied

Consider a differentiable family parameter \(\lambda\) at fixed \(e,b,M_i,w_i\) and physical reference mass. Set

\[
v=\partial_\lambda a,\quad u=\partial_\lambda x,\quad
\boldsymbol\eta_i=\partial_\lambda\mathbf r_i,\quad
q_i=\partial_\lambda p_i=\kappa_i-v,\quad
\kappa_i=\partial_\lambda k_i,\quad f=\partial_\lambda F.
\tag{P7}
\]

The symbol \(q_i\) here denotes a momentum variation, not electric charge. In a physical source-amplitude experiment, the canonical grid is fixed and \(\kappa_i=0\), so \(q_i=-v\). A residual constant gauge transformation instead has \(\kappa_i=v=c\), \(q_i=0\), \(u=0\). This distinction must be explicit in tests.

No derivative with respect to \(b\), the cutoffs or the quadrature nodes is included in a physical tangent. Changing \(b\) would change the weights, masses and finite matching; differentiating only the mode Hamiltonian would then be incomplete. Varying cutoffs is a numerical sensitivity experiment, not this physical response.

## 3. Complete first-variation system

At fixed weights and masses,

\[
\delta\omega_i=\frac{p_iq_i}{\omega_i},\qquad
\delta S=\sum_iw_i\left(\eta_{iz}+\frac{M_i^2q_i}{\omega_i^3}\right),
\tag{P8}
\]

\[
\delta C=-\sum_iw_i\frac{5M_i^2p_iq_i}{4\omega_i^7},\qquad
\delta D=\sum_iw_i\frac{5M_i^2(M_i^2-6p_i^2)q_i}{8\omega_i^9},\qquad
\delta Z=-e^2\delta C.
\tag{P9}
\]

The complete coupled tangent equations are

\[
\boxed{
v'=-u,\qquad
u'=\frac{f-e^2(\delta S+\delta D\,x^2+2Dxu)+e^2\delta C\,x'}{Z},\qquad
\boldsymbol\eta_i'=2\mathbf h_i\times\boldsymbol\eta_i
+2(0,0,q_i)\times\mathbf r_i.
}
\tag{P10}
\]

The positive sign of \(e^2\delta C\,x'\) follows by differentiating \(Zx'=F-e^2(S+Dx^2)\). Omitting this quotient term gives a different linearization, even if the background trajectory itself is correct.

For an implementation that uses real arrays,

\[
\eta_{ix}'=-2(p_i\eta_{iy}+q_i r_{iy}),\quad
\eta_{iy}'=2(p_i\eta_{ix}+q_i r_{ix}-M_i\eta_{iz}),\quad
\eta_{iz}'=2M_i\eta_{iy}.
\tag{P11}
\]

The differentiated physical matter current is

\[
\delta J=\delta S-\delta C\,x'-C u'+\delta D\,x^2+2Dxu
+\frac{\chi_b}{e^2}u'.
\tag{P12}
\]

It must obey \(u'=f-e^2\delta J\). This is a useful independent algebraic residual if all terms are evaluated directly rather than defining \(\delta J\) by rearranging Maxwell's equation.

## 4. Preparation and temporal boundary conditions

This is a homogeneous temporal initial-value problem. There is no black-hole horizon, radial origin or spatial asymptotic boundary in the implemented calculation. The momentum cutoff is a regulator; it is not a reflecting spatial wall.

Prepare the common initial state in an exactly static magnetic background:

\[
a(0)=a_0,\quad x(0)=0,\quad
\mathbf r_i(0)=-\mathbf h_i(0)/\omega_i(0).
\tag{P13}
\]

Define a normalized compact pulse

\[
I=\int_0^1e^{-1/[z(1-z)]}\,dz,\qquad
g_T(s)=\begin{cases}
e^{-1/[z(1-z)]}/(TI),&z=s/T\in(0,1),\\
0,&\text{otherwise}.
\end{cases}
\tag{P14}
\]

All derivatives vanish at the two endpoints and \(\int g_Tds=1\). The target parameter is an integrated external-current impulse, not a promise that the interacting field reaches that value.

**Amplitude preparation.** Set \(F(s;\lambda)=\lambda g_T(s)\). At the selected background amplitude \(\lambda_0\), use \(f=g_T\) and \(v(0)=u(0)=\boldsymbol\eta_i(0)=0\). These are derivatives with respect to an absolute dimensionless amplitude. Multiplying by \(\lambda_0\) gives the derivative with respect to logarithmic amplitude when \(\lambda_0\ne0\); never silently confuse the two.

**Delayed probe.** Set \(F(s;\epsilon)=F_0(s)+\epsilon g_{T_p}(s-s_p)\), with \(s_p>0\). The base and perturbed preparations agree until \(s_p\); all tangent variables must remain zero before that time. This supplies a causal support test independent of the shape of the initial pump.

**Gauge null.** Translate every retained canonical momentum by the same constant as \(a_0\). Then \(q_i=0\), \(\boldsymbol\eta_i=u=0\), and the physical response vanishes. Holding a finite grid fixed while changing \(a_0\) changes the selected physical modes and is a deliberately different regulator test.

**Future state perturbation.** A distinct admissible family can rotate each initially occupied Bloch vector by \(\mathbf r_i(\epsilon)=\mathrm{Rot}_{\hat y}[\epsilon h_i]\mathbf r_i(0)\), where \(h_i\) is smooth and compactly supported in momentum and limited to finitely many Landau levels. Then \(\boldsymbol\eta_i(0)=h_i\hat y\times\mathbf r_i(0)\). This preserves pure-state normalization and changes the quasifree state without modifying its ultraviolet tail. It is an explicit additional experiment, not part of a source-amplitude derivative. Initializing an arbitrary nonzero electric field while keeping the modes in an undressed instantaneous vacuum is not a substitute for any of these preparations.

For a general change of the initial Hamiltonian, a differentiated instantaneous vacuum has

\[
\boldsymbol\eta_i(0)=\left(\frac{M_ip_iq_i}{\omega_i^3},\ 0,\ -\frac{M_i^2q_i}{\omega_i^3}\right)_{s=0}.
\tag{P15}
\]

This algebraic formula does not make such a state the correct ultraviolet preparation in an initially time-dependent background. The electric and gravitational adiabatic prescriptions require their own consistent order assignments. [R03]

## 5. Exact tangent constraints and energy identities

Differentiating \(|\mathbf r_i|^2=1\) gives

\[
\mathbf r_i\cdot\boldsymbol\eta_i=0,\qquad
(\mathbf r_i\cdot\boldsymbol\eta_i)'=0.
\tag{P16}
\]

This tangency constraint is conserved. The tangent magnitude itself need not be constant:

\[
(|\boldsymbol\eta_i|^2)'=4\boldsymbol\eta_i\cdot[(0,0,q_i)\times\mathbf r_i].
\tag{P17}
\]

Do not normalize the tangent vector, project away its growth, or impose \(|\boldsymbol\eta_i|=1\). Doing so changes the physical derivative being measured.

\[
\delta U=\sum_iw_i\left[\mathbf h_i\cdot\boldsymbol\eta_i
+(r_{iz}+p_i/\omega_i)q_i\right],
\qquad
(\delta U)'=uS+x\delta S.
\tag{P18}
\]

\[
\delta\rho_q/m^4=\delta U-\frac{\delta C\,x^2}{2}-Cxu
+\frac{\chi_b}{e^2}xu,
\qquad
(\delta\rho_q/m^4)'=uJ+x\delta J.
\tag{P19}
\]

\[
\boxed{
\delta W=Zxu-\frac{e^2\delta C\,x^2}{2}+e^2\delta U,
\qquad
(\delta W)'=uF+xf.
}
\tag{P20}
\]

Integrate both work variables as part of the adaptive ODE state, \(w'=xF\) and \(z_w'=uF+xf\), rather than attributing errors from coarse sampled quadrature to the evolution. For the two source preparations, \(\delta W(0)=0\). After both the base and probe sources cease, \(\delta W\) is constant. A small residual checks the differentiated specified model; it neither bounds every observable error nor proves that the matching model is physically unique.

For diagnostic occupations \(f_i^{\rm pair}=[1+\mathbf h_i\cdot\mathbf r_i/\omega_i]/2\),

\[
\delta f_i^{\rm pair}=\frac12\left[
\frac{\mathbf h_i\cdot\boldsymbol\eta_i+q_i r_{iz}}{\omega_i}
-\frac{(\mathbf h_i\cdot\mathbf r_i)p_iq_i}{\omega_i^3}\right].
\tag{P21}
\]

Do not replace the current by this instantaneous-basis occupation or clip signed roundoff before auditing it.

## 6. Independent spinor and retarded formulations

An implementation with different state variables should solve

\[
iy_i'=H_i y_i,\qquad i\zeta_i'=H_i\zeta_i+q_i\sigma_3y_i,
\qquad H_i=M_i\sigma_1+p_i\sigma_3,
\tag{P22}
\]

where \(\zeta_i=\delta y_i\) and

\[
\eta_{ij}=2\operatorname{Re}(y_i^\dagger\sigma_j\zeta_i),\quad
\operatorname{Re}(y_i^\dagger\zeta_i)=0.
\tag{P23}
\]

The phase of \(\zeta_i\) is representation dependent; compare gauge-invariant \(u\), the current variation and \(\boldsymbol\eta\), not a spinor phase chosen differently by two codes. A spinor reimplementation must not import the production tangent RHS.

There is also an exact causal representation at the finite regulator. Let \(R_i(s,t)\) be the three-dimensional rotation propagator generated by \(2\mathbf h_i\times\), with \(R_i(t,t)=I\). For an unchanged initial state and a fixed canonical grid,

\[
\boldsymbol\eta_i(s)=-2\int_0^sR_i(s,t)[\hat z\times\mathbf r_i(t)]v(t)\,dt,
\tag{P24}
\]

\[
\delta S(s)=\int_0^sK(s,t)v(t)\,dt-T(s)v(s),\quad
T(s)=\sum_iw_iM_i^2/\omega_i(s)^3,
\tag{P25}
\]

\[
K(s,t)=-2\sum_iw_i\hat z\cdot R_i(s,t)[\hat z\times\mathbf r_i(t)].
\tag{P26}
\]

The first term is a retarded response of the occupied quantum modes; the second is the differentiated instantaneous-vacuum contact term. The remaining local terms in P12 are required by the common matching prescription. At constant vacuum background, one mode supplies \(2M_i^2\sin[2\omega_i(s-t)]/\omega_i^2\) to the response kernel before its weight. The equivalent Heisenberg expression is \(i\langle[\sigma_3(s),\sigma_3(t)]\rangle\) with the perturbation Hamiltonian \(-v\sigma_3\). This establishes the sign and causal interpretation without substituting a time-ordered in/out polarization tensor.

P24–P26 are an independent derivation of the response of our finite model. The numerical kernel integral need not be stored as a dense two-time array to evolve it: P10 propagates its action through the mode tangents. An explicit propagator/kernel quadrature would be an additional representation check.

## 7. Acceptance gates fixed before examining results

| Gate | Required measurement | Interpretation and failure action |
|---|---|---|
| Algebra | Independent derivatives of P8–P12; exact P16 and P20 | A sign disagreement blocks implementation acceptance |
| Baseline compatibility | New per-mode current versus unchanged legacy at identical grid, source and tolerance | Record numerical effect and code hashes; a code/report mismatch is not automatically a false physical result |
| Finite differences | Central derivative \([x(\lambda+\epsilon)-x(\lambda-\epsilon)]/(2\epsilon)\) over at least three amplitudes | Expect second-order truncation until numerical error divided by \(\epsilon\) dominates; do not demand indefinite improvement |
| Independent representation | Complex-spinor tangent and Bloch tangent over full sampled history | Set tolerance from each solver's refinement; no claim of continuum accuracy |
| Held-out configuration | Change \(b\), pump amplitude and duration after equation freeze | The same implementation must satisfy identities and FD behavior |
| Retarded support | Delayed probe with exactly identical pre-probe history | Any resolvable pre-probe response is an implementation/preparation failure |
| Gauge null | Shift both the potential and canonical grid | Physical field response must vanish; a fixed-grid shift is a separate regulator change |
| Constraint/work | Raw \(\mathbf r\cdot\boldsymbol\eta\), P20 and current residual | No clipping or renormalizing tangent vectors to manufacture success |
| Momentum refinement | Same longitudinal window with increased node count | Excellent work conservation cannot replace observable quadrature convergence |
| Cutoff sensitivity | Independent longitudinal-window and Landau-cutoff changes | Label finite-regulator results if not jointly controlled |
| Deliberate defect | Delete quotient variation or a contact term in a test-only path | A meaningful discrepancy establishes diagnostic power; do not alter production equations |

Suggested finite-regulator research cases are \(b=10,\lambda_0=1,T=4,s_f=20,N=4,K=20\), with longitudinal node refinement, and a held-out \(b=3,\lambda_0=0.5,T=6,s_f=18\). An independently affordable representation case is \(b=10,N=2,K=6,N_k=32,T=4,s_f=8\). Report actual run settings, including output times; these suggestions are not claims that calculations have occurred.

The primary response observable is \(u(s)=\partial x/\partial\lambda\). Use maximum absolute full-history differences for verification. Ratios with \(|x(s)|\) in the denominator are singular at ordinary field reversals and can fake instability. Optional amplification should use a fixed source-impulse scale or a nonzero reference norm stated once. A finite-time large derivative can also reflect accumulated phase shifts; it is not by itself a positive asymptotic Lyapunov exponent.

## 8. What this response does and does not decide

The tangent calculation contains the restricted retarded commutator response through the variation of quantum modes. It is therefore more specific than treating the induced current as an arbitrary fitted fluid law. Nevertheless, one driven homogeneous perturbation is not the supremum over admissible nonsingular initial states or inhomogeneous perturbations. Bounded response on a finite time interval cannot establish asymptotic stability. The semiclassical-gravity linear-response criterion was originally formulated and demonstrated under different matter/background assumptions. [R02]

The symmetrized connected noise \(N_{JJ}(s,t)=\tfrac12\langle\{\delta\hat J(s),\delta\hat J(t)\}\rangle\) is not supplied by measuring a parameter derivative alone. In a nonequilibrium pumped state there is no automatic equilibrium fluctuation-dissipation substitution that reconstructs it from our one response history. For gravity, the current/stress response blocks and the noise blocks must be defined in the same state, with physical smearing and local renormalization. Distributional coincident-point stress fluctuations are not finite scalar error bars. [R04]

A 2026 fully quantum 1+1-dimensional calculation obtains a mass-dependent oscillation-frequency correction missed by its semiclassical comparator. That remains an independent warning: passing finite-model response tests cannot establish agreement with the fully quantized four-dimensional theory. [R05]

## 9. P4: exact dependency before connecting gravity

The next gravitational interface uses

\[
ds^2=-dt^2+a_\perp^2(dx^2+dy^2)+a_\parallel^2dz^2,\qquad
H_\perp=\dot a_\perp/a_\perp,\quad H_\parallel=\dot a_\parallel/a_\parallel.
\]

With physical aligned fields, \(\dot B=-2H_\perp B\) and \(\dot E+2H_\perp E=-(J_q+J_{\rm ext})\). A usable quantum closure must return \(J_q,\rho_q,p_{\perp q},p_{\parallel q}\), and obey

\[
\dot\rho_q+2H_\perp(\rho_q+p_{\perp q})+H_\parallel(\rho_q+p_{\parallel q})=EJ_q.
\tag{P27}
\]

The energy density alone is insufficient. One common local counterterm action must generate the current, both pressures and energy with the same finite coefficients, including charge, cosmological, Einstein and curvature-squared terms. If the quantum Dirac field has already been integrated dynamically, its loop contribution cannot also be added as an independent Euler–Heisenberg matter source. A curved-space adiabatic expansion and a locally covariant point-splitting construction must agree up to their explicitly fixed allowed local terms. Zahn's locally covariant treatment provides the conservation and ambiguity framework; it is not an evaluated strong-field Bianchi-I solver. [R06]

Let \(X_A=(A_\mu,g_{\mu\nu})\). The next causal closure requires variations \(\delta\langle J\rangle/\delta A\), \(\delta\langle J\rangle/\delta g\), \(\delta\langle T\rangle/\delta A\), and \(\delta\langle T\rangle/\delta g\), with retarded support and all local contact terms. A closed-time-path effective action is the natural organization; replacing its derivatives by an in/out action can impose the wrong state and boundary prescription. P3 computes only a symmetry projection of the first block at fixed metric.

Before an Einstein run: reproduce the electromagnetic force Ward identity P27; check the same result in a second subtraction scheme; enforce the Hamiltonian constraint on initial geometry and quantum state; preserve its propagation with the same source; test transverse versus longitudinal pressure cutoffs; compare the physical electron scale to the requested curvature. Round 3 found that \(E/E_c=1,B/B_c=100\) alone yields \(\kappa\rho/m_e^2\sim2.4\times10^{-39}\), so curvature of order \(m_e^2\) requires an additional source or a distinct scaling assumption. No amount of tighter numerical tolerance changes this scale budget.

## 10. A new primary-source challenge and a useful alternative branch

Sanz-Wuhl and Zahn's May 2026 finite-interval scalar calculation revisits stationary vacuum screening with a gauge-compatible subtraction, explicit spatial boundary conditions and damped continuation. Its reported over-screening is a candidate electrostatic benchmark, not the homogeneous dynamical spinor problem. The authors explicitly leave quantum-fluctuation validity for future work. Their acknowledgment identifies Basque Government and Spanish AEI support; funding is provenance, not validation. [R07]

There is a checkable displayed-sign inconsistency. Their PDF equation 6 has a positive temporal covariant derivative squared followed by \(+\partial_x^2-m^2\), whereas their equation 7 after \(e^{-i\Omega t}\) has \(+(\Omega-eA_0)^2+\partial_x^2-m^2\). At zero potential, a mode with \(\Omega^2=k^2+m^2\) obeys equation 7 but gives \(-2(k^2+m^2)\phi\) in printed equation 6. A negative sign on the temporal squared derivative repairs that displayed form. This is not evidence that their calculations based on equation 7 are wrong. It is a concrete example of independently checking a source's reduction rather than treating peer review or a recent date as an equation test.

The proposed followup should reproduce both spatial boundary-condition cases and compare the correct local subtraction with the intentionally incorrect older truncation. A converged damped fixed-point iteration establishes a stationary solution of the discretized equation; it does not establish real-time dynamical stability. That distinction is precisely why the causal P3 experiment remains the immediate priority.
