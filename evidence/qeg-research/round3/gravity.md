# Gravitational closure: equations, counterexamples and verified next steps

## What this audit changes

The previous curved-mode calculation was a valid calculation on a prescribed geometry. It was not an Einstein–Maxwell–Dirac solution, and its small occupation-number discrepancies could not certify the missing gravitational equations. The next meaningful extension must calculate **two directional pressures as well as energy and current**, and must propagate an initial gravitational constraint. A homogeneous magnetic field selects an axis; a single FLRW scale factor cannot in general respond to its stress. This is a restriction on the self-consistent extension, not a reason to discard the earlier prescribed-background benchmark. Magnetized Bianchi-I calculations explicitly retain this anisotropy. [@H01]

This module supplies a complete classical gravitational interface, a finite-regulated anisotropic Dirac interface, a common-counterterm Ward test, and an independently evolved classical test fixture. It does not supply the missing four-dimensional renormalized quantum state. Its executed checks appear in `gravity_checks.py` and `gravity_checks.json`. No quantum-gravity endpoint is inferred from them. The independent advisor reviewed and accepted (H11), (H14)–(H17) and (H19), including the spin and pressure factors, rotating-basis connection and counterterm signs, within the stated finite/classical scope.

## 1. Fix signs before coupling modules

Take signature $(-+++)$, $\hbar=c=1$, Heaviside–Lorentz electromagnetic units, $\kappa=8\pi G$, and

$$ds^2=-dt^2+a_\perp^2(t)(dx^2+dy^2)+a_\parallel^2(t)dz^2.$$

Let $h=\dot a_\perp/a_\perp$, $k=\dot a_\parallel/a_\parallel$, and $\theta=2h+k$. Choose $F=dA$, $F_{xy}=B_0$, $F_{0z}=\dot A_z=-a_\parallel E$, and $B=B_0/a_\perp^2$. Define the physical current $j=a_\parallel J^z$ by the matter-action variation $\delta W/\delta A_\mu=\sqrt{-g}J^\mu$. These definitions require

$$\nabla_\nu F^{\mu\nu}=J^\mu,\qquad
\dot E+2hE=-j,\qquad \dot B+2hB=0.\tag{H1}$$

Writing the antisymmetric tensor indices in the opposite order changes the sign of the Maxwell equation. The Lorentz-force Ward identities in these conventions are

$$\nabla_\mu J^\mu=0,\qquad
\nabla_\mu T_{\rm m}^{\mu\nu}=F^{\nu}{}_{\lambda}J^\lambda,\qquad
\nabla_\mu T_{\rm EM}^{\mu\nu}=-F^{\nu}{}_{\lambda}J^\lambda.\tag{H2}$$

The homogeneous Gauss constraint requires zero total charge density. Neutral pair creation is consistent with a nonzero longitudinal current. A charge density or transverse momentum introduced by a new state would require additional constraints and generally a larger ansatz. Parallel $E$ and $B$ carry no electromagnetic Poynting flux in this frame. A dipole or multipolar magnetic geometry is not represented by this homogeneous model.

**New source check.** Newsome–Anderson–Grotzke's 2025 PDF uses $E=-\dot A$ and $\ddot A=-\dot E=J_C+\langle J_Q\rangle$ in equation (3.1). Its displayed Sauter source (3.3a) has a minus sign, whereas differentiating its positive pulse (3.3b) requires $J_C=+2qE_0\operatorname{sech}^2(qt)\tanh(qt)$. Its perturbation (4.3) uses the latter sign. The introductory covariant equation also reverses the sign relative to its action and equation (2.2). These are displayed-equation inconsistencies; they do not establish what sign the authors' numerical implementation used. Our symbolic differentiation reproduces the discrepancy. The HTML numbers these formulas differently and displays a regenerated date; the PDF dates itself May 2, 2025. [@H02]

## 2. Full Einstein–Maxwell energy and stress system

Write the orthonormal matter tensor as $\operatorname{diag}(\rho_m,p_{m\perp},p_{m\perp},p_{m\parallel})$. With $u=(E^2+B^2)/2$,

$$\rho=\rho_m+u,\quad p_\perp=p_{m\perp}+u,\quad
p_\parallel=p_{m\parallel}-u.\tag{H3}$$

These field pressures, including the negative longitudinal pressure, follow from the Maxwell stress tensor; replacing all of them by $u/3$ changes the problem. The independent Einstein equations are

$$C\equiv h^2+2hk-\kappa\rho-\Lambda=0,\tag{H4}$$

$$\dot h=\frac{\Lambda-\kappa p_\parallel-3h^2}{2},\tag{H5}$$

$$\dot k=\Lambda-\kappa p_\perp-h^2-k^2-hk-\dot h,\tag{H6}$$

$$\dot a_\perp=ha_\perp,\quad \dot a_\parallel=ka_\parallel,\quad
\dot A_z=-a_\parallel E.\tag{H7}$$

The matter Ward identity and electromagnetic work identity reduce to

$$\dot\rho_m+2h(\rho_m+p_{m\perp})+k(\rho_m+p_{m\parallel})=Ej,\tag{H8}$$

$$\dot u+4hu=-Ej.\tag{H9}$$

Equations (H1), (H3)–(H9) become a closed initial-value problem only when the quantum state supplies $j,\rho_m,p_{m\perp},p_{m\parallel}$ consistently. One cannot determine all four functions from (H8). An external current requires the external apparatus' energy and stress, or a clearly prescribed-background approximation.

The curvature expressions useful for local screens are

$$R=4\dot h+2\dot k+6h^2+4hk+2k^2,$$

$$R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
=4\left[2(\dot h+h^2)^2+(\dot k+k^2)^2+h^4+2h^2k^2\right].\tag{H10}$$

The script independently constructs all Christoffel symbols, the Ricci tensor and Einstein tensor from the four-dimensional metric before comparing the reduced equations. This checks their signs and the relative factors rather than simply rearranging a copied ODE.

### 2.1 Constraint propagation and an actual review correction

Define the residual

$$\mathcal R_E=\dot\rho+2h(\rho+p_\perp)+k(\rho+p_\parallel).$$

Using precisely (H5)–(H6), direct differentiation gives

$$\boxed{\dot C=-\theta C-\kappa\mathcal R_E.}\tag{H11}$$

Thus constrained data stay constrained when total stress is conserved. The evolution equation also provides a diagnostic: compare the directly evaluated $C$ with the integrated source residual; they should agree to numerical error. Dividing by a tiny energy density alone is not a robust normalization near a field zero.

The reviewer initially suggested $-2\theta C$ by recalling a different constraint-added evolution system. The independent metric calculation rejected it: this spatial-Einstein evolution gives $-\theta C$. The equation above was corrected before acceptance and before any claimed result. Constraint propagation coefficients are formulation dependent off the constraint surface; memory of a standard formula is not a proof.

For running $\kappa(t)$ and $\Lambda(t)$ the same calculation yields

$$\dot C=-\theta C-\kappa\mathcal R_E-\dot\kappa\rho-\dot\Lambda.\tag{H12}$$

Simply replacing couplings by running functions while retaining separately conserved matter therefore fails unless $\dot\kappa\rho+\dot\Lambda=0$, or the additional terms follow from a consistently varied action or energy exchange. A 2026 asymptotic-safety Bianchi-I preprint, whose September 7 revision was checked, explicitly encounters an overdetermined magnetic system and introduces additional stress. Its equations (44)–(46) independently agree with the constraint-decay and running-coupling structure derived here. That is a model-dependent closure, not a four-dimensional QED current calculation. Its classical electric–magnetic duality also does not transfer unchanged to electrically charged pair production. [@H03]

### 2.2 Why mean-energy conservation is insufficient

Let $\Delta=k-h$. Subtracting the spatial Einstein equations gives

$$\dot\Delta+\theta\Delta=\kappa(p_\parallel-p_\perp).\tag{H13}$$

An initially isotropic geometry with isotropic matter and aligned electromagnetic fields has $\dot\Delta=-\kappa(E^2+B^2)$ immediately. A prescribed FLRW pulse cannot be turned into a self-consistent magnetic solution by evolving its single scale factor from $\rho$ alone.

There is an explicit nullspace in the energy constraint: changing $p_\perp$ by $k f(t)$ and $p_\parallel$ by $-2h f(t)$ leaves $2hp_\perp+kp_\parallel$ unchanged at every instant, while changing the shear source by $-\kappa\theta f(t)$. Here $f$ has units pressure divided by expansion rate. An energy-only fit cannot identify the missing anisotropic stress. The nullspace remains even with exact numerical energy conservation.

## 3. A concrete anisotropic Dirac bridge

Rescale the spinor by $\chi=(a_\perp^2a_\parallel)^{1/2}\psi$ to remove the homogeneous spin-connection volume term. For charge $q>0$ and a fixed comoving Landau basis define

$$P=\frac{k_z-qA_z}{a_\parallel},\quad
c_n=\frac{\sqrt{2n|qB_0|}}{a_\perp},\quad
H_n=m\beta+P\alpha_z+c_n\alpha_x,\qquad i\dot Y_n=H_nY_n.\tag{H14}$$

For $n\ge1$ one may use $\beta=\tau_z\otimes I$, $\alpha_z=\tau_x\otimes\sigma_z$, $\alpha_x=\tau_x\otimes\sigma_x$, and a $4\times2$ matrix of initially occupied negative-energy modes $Y_n$. The lowest Landau level has a single $2\times1$ occupied column and no transverse term. The longitudinal symbol $k_z$ is the canonical momentum, not the Hubble parameter $k$ used above. Transverse rotational symmetry and charge-neutral initial data are assumed.

Let

$$\mathcal D(t)=\frac{|qB_0|}{4\pi^2a_\perp^2a_\parallel},\qquad
\mathcal S[X]=\sum_n\int dk_z\operatorname{Tr}(Y_n^\dagger X_nY_n).$$

At a **fixed finite comoving mode regulator**, the common Hamiltonian variations give

$$\rho_{\rm bare}=\mathcal D\mathcal S[H],\quad
j_{\rm bare}=q\mathcal D\mathcal S[\alpha_z],\tag{H15}$$

$$p_{\parallel,\rm bare}=\mathcal D\mathcal S[P\alpha_z],\quad
p_{\perp,\rm bare}=\frac{\mathcal D}{2}\mathcal S[c_n\alpha_x].\tag{H16}$$

Both spin channels are already represented by the columns of $Y_n$ at $n\ge1$. Multiplying again by the usual twofold Landau degeneracy double counts them. The factor one-half in each transverse pressure is different: changing $a_\perp$ changes two spatial directions.

From $\dot{\mathcal D}=-\theta\mathcal D$, $\dot P=qE-kP$, $\dot c_n=-hc_n$, and $d\langle H\rangle/dt=\langle\dot H\rangle$, equations (H15)–(H16) satisfy (H8) exactly. The script checks this finite-mode identity symbolically. It is a useful interface test for a later mode solver, but fixed comoving cutoffs are not covariant renormalization and can violate gauge-shift comparisons through their boundaries. Divergent sea energies and anisotropic regulator stresses cannot be inserted into Einstein's equations as physical sources.

The previous curved-mode connection also generalizes. The conserved sector operator is $S=\tau_z\otimes\sigma_y$. In sector $s=\pm1$, write $h_s=P\sigma_3+m\sigma_1-sc_n\sigma_2$. A time-dependent rotation making the transverse mass real yields

$$h_{s,\rm rot}=\left[P+\frac{s(m\dot c_n-c_n\dot m)}{2(m^2+c_n^2)}\right]\sigma_3+
\sqrt{m^2+c_n^2}\sigma_1.\tag{H17}$$

Here $\dot m=0$ in cosmic time, so the connection is $-smhc_n/[2(m^2+c_n^2)]$. A naive replacement $m\to\sqrt{m^2+c_n^2}$ drops it. In conformal FLRW time the mass coefficient changes instead and reproduces the earlier connection with the corresponding sign. These are different time parametrizations of the same basis issue.

## 4. Renormalize current and stress together

A causal in-in effective action or a locally covariant point-splitting construction must define both observables from one state and one set of local counterterms. Formally, on coincident physical branches,

$$J^\mu=\frac1{\sqrt{-g}}\frac{\delta W_{\rm CTP}}{\delta A_\mu},\qquad
T_{\mu\nu}=-\frac2{\sqrt{-g}}\frac{\delta W_{\rm CTP}}{\delta g^{\mu\nu}}.\tag{H18}$$

Gauge and diffeomorphism invariance then give (H2). Variation of an in-out vacuum-persistence action is not automatically a causal expectation value in a chosen initial state. Zahn's construction demonstrates the current-renormalization freedom and the role of local covariance. Its stress-conservation discussion carefully restricts backgrounds or includes their dynamics; it must not be summarized as separate matter-stress conservation in an arbitrary external electromagnetic field. [@H04]

An explicit finite-counterterm test is useful. Add $W_{\rm ct}=-(c/4)\int\sqrt{-g}F^2$ to the matter effective action. In our convention it induces

$$\delta j=c(\dot E+2hE),\quad
\delta\rho_m=cu,\quad \delta p_{m\perp}=cu,\quad\delta p_{m\parallel}=-cu.\tag{H19}$$

These shifts satisfy (H8) using $\dot B=-2hB$, without imposing the sourced Maxwell equation. Changing only the current subtraction leaves a residual $-E\delta j$ if the old stress is kept. Changing both observables while compensating the electromagnetic coupling is a renormalization-scheme transformation; changing only one is a different, generally inconsistent dynamics. This is a concrete check rather than an appeal to a renormalization label.

The next initial state must also have appropriate short-distance structure. A finite-time instantaneous vacuum on an arbitrary rapidly changing geometry is not automatically a Hadamard state with a finite fourth-order-subtracted stress. Work on the semiclassical initial-value problem explicitly treats compatibility between initial geometry, quantum two-point functions and constraints, and labels important existence and uniqueness statements as conjectures. We therefore cannot choose all geometry derivatives and an arbitrary ultraviolet state independently. [@H05]

## 5. What the new numerical calculation verifies

Before putting a quantum source into this geometry, we solved a deliberately transparent classical fixture. Set $\Lambda=0$, $j=\sigma E$, and use an isotropic radiation reservoir with $p_m=\rho_m/3$ and

$$\dot\rho_m=-\frac43\theta\rho_m+\sigma E^2.$$

This Ohmic constitutive law is phenomenological. It is not a Schwinger current. The chosen dimensionless $\kappa=0.1$ makes gravitational effects visible for an algorithmic test and must not be interpreted as the physical electron coupling. Initial data are $a_\perp=a_\parallel=1$, $E=1$, $B=3$, $\rho_m=0.2$, $\sigma=0.2$, with $h=k=\sqrt{\kappa\rho/3}$. We evolve to $t=2$.

An independent formulation uses $H=(2h+k)/3$ and $\Delta=k-h$:

$$\dot H=-H^2-\frac{2\Delta^2}{9}-\frac\kappa6(\rho+3\bar p),\qquad
\dot\Delta=-3H\Delta+\kappa(p_\parallel-p_\perp),$$

where $\bar p=(2p_\perp+p_\parallel)/3$. The directional and Raychaudhuri–shear formulations were evolved independently; their equations agree on constrained solutions but differ off the constraint surface.

| Executed check | Result |
|---|---:|
| Symbolic zero-residual identities | 19 passed |
| Maximum Hamiltonian residual | $4.11\times10^{-14}$ |
| Maximum magnetic-flux error, $Ba_\perp^2-B_0$ | $7.86\times10^{-14}$ |
| Maximum damped-electric-flux error, $Ea_\perp^2e^{\sigma t}-E_0$ | $7.33\times10^{-14}$ |
| Independent Raychaudhuri–shear versus directional solver | $8.73\times10^{-14}$ |
| RK4 errors at 100, 200, 400, 800 steps | $5.62\times10^{-9}$, $3.47\times10^{-10}$, $2.15\times10^{-11}$, $1.34\times10^{-12}$ |
| Observed RK4 convergence orders | 4.018, 4.009, 4.009 |

At the endpoint $h=0.2373631$ and $k=-0.03305215$: the transverse directions expand while the longitudinal direction contracts. This demonstrates a behavior that an isotropic scale factor cannot represent. It validates the classical gravitational interface and numerical implementation only.

### 5.1 A quantitative scale obstruction

For the physical electron, the retained constants give $8\pi Gm_e^2\simeq4.40\times10^{-44}$. At $E/E_c=1$ and $B/B_c=100$, the field energy is about $5.45\times10^4m_e^4$, so $\kappa\rho_{\rm EM}/m_e^2\simeq2.40\times10^{-39}$. These fields by themselves do not generate electron-scale spacetime curvature. An order-one stress-curvature budget from a purely magnetic field would require $B/B_c$ of order $2.04\times10^{21}$ in this elementary estimate, far outside the previously tested $b\le1000$ range.

This is not a theorem forbidding $R\sim m_e^2$: other gravitating matter, a compact-object geometry or a cosmological sector can supply it. It is a missing-source test. The classical Maxwell trace is zero, so the scalar $R$ alone is especially misleading. The exact Kasner example $a_\perp\propto t^{2/3}$, $a_\parallel\propto t^{-1/3}$ has $R=0$ but $R_{\mu\nu\rho\sigma}^2=64/(27t^4)$. Both formulas were checked. The earlier report already printed a Kretschmann diagnostic; that stronger screen should be retained.

## 6. Stability and fluctuations are independent acceptance gates

Mean stress is not a complete measure of quantum fluctuations. Even a bounded energy observable can have the same conserved mean in an energy eigenstate and a mixture with probability $p$ at energy $\bar E/p$ and probability $1-p$ at zero. The variances are respectively zero and $\bar E^2(p^{-1}-1)$. At $p=0.01$ this is $99\bar E^2$. This elementary counterexample does not itself diagnose gravitational breakdown; it shows why equal conserved means cannot decide it.

The physically relevant object is a smeared stress noise kernel and its gravitational response, schematically $N=\langle\{T-\langle T\rangle,T'-\langle T'\rangle\}\rangle/2$ and an induced metric correlation $G_RNG_R^T$. Coincident unsmeared variances are singular, while ratios to a zero mean can spuriously label the Minkowski vacuum invalid. Stochastic-gravity analyses distinguish induced and intrinsic fluctuations. [@H06]

For the coupled problem one needs the retarded block response of current and stress to both $A$ and $g$, including $JJ$, $JT$, $TJ$, and $TT$ kernels with contact terms. The metric/current variations must respect the same Ward identities as the mean equations. A linear-response stability test is a necessary internal check, not a universal sufficient theorem that a semiclassical solution is exact. [@H07]

The 2025 Maxwell–Dirac study provides a concrete lower-dimensional benchmark for this next test. It evaluates the causal current commutator rather than only comparing two nonlinear trajectories. Consequently, a future finite-difference perturbation test must shrink its perturbation size and compare with a tangent or retarded-kernel calculation; agreement over an early interval must not be extrapolated indefinitely. [@H02]

### 6.1 Higher derivatives and order reduction

Retaining $R^2$ and $R_{\mu\nu}R^{\mu\nu}$ in an EFT introduces higher metric derivatives. Solving a truncated fourth-order equation with arbitrary extra initial data can excite modes outside the expansion's validity. A schematic equation $\ddot x+\omega^2x-\ell^2x^{(4)}=0$ has a rapidly growing branch with rate of order $1/\ell$ even though its low-frequency branch has a regular perturbative limit. A numerical integrator accurately resolving that branch does not establish a physical instability of the ultraviolet completion.

Order reduction uses the lower-order equation inside perturbative corrections and retains the requested order in the EFT expansion. It must be applied consistently to constraints and response equations, with the discarded order recorded. [@H08] An $R^2$ term is not automatically a ghost: it can represent an additional healthy scalar in a different theory; generic curvature-squared spin-two poles and EFT extra branches require separate analysis. [@H16] Conversely, deleting all matter-loop effects as “runaways” can discard meaningful large-$N$ physics. The choice between an EFT expansion and an enlarged dynamical theory must precede the initial-value problem. [@H06]

## 7. Cauchy horizons and quantum energy inequalities remain distinct tests

The earlier scalar diagnostic $\phi\sim |V|^\beta$ implies local squared-derivative behavior $|\partial_V\phi|^2\sim |V|^{2\beta-2}$. Its integral converges for $\beta>1/2$, diverges logarithmically at $\beta=1/2$, and diverges as a power below it. This is an energy-regularity statement about a specified asymptotic profile. It neither proves smooth extension of a metric nor supplies a backreacted quantum endpoint.

An extension claim must specify whether it means continuous metric extension, square-integrable connection, classical differentiability, or a distributional solution with a well-defined stress. Fixed-background divergent $\langle T_{VV}\rangle$ is not the same object as a solved singular backreacted geometry. Shahbazi-Moghaddam's analysis relates a mild singularity structure to robust, state-independent behavior in a near-horizon wedge construction; it explicitly does not prove that all states fit that construction or that every allowed divergence appears. [@H09]

Violating a pointwise classical energy condition also does not prove that a quantum bounce occurs. Fewster–Kontou establish a semiclassical singularity theorem for a specified minimally coupled scalar model with quantum-energy-inequality and initial contraction hypotheses. Its theorem and quantitative example were checked beyond the abstract. It cannot be imported unchanged into interacting spinor QED with strong electromagnetic fields. It is a counterexample to the generic inference “quantum negative energy removes all singularity arguments,” not a proof of censorship for our target. [@H10]

## 8. Reopened 2025–2026 entanglement dispute: test the channel

Aziz–Howl's 2025 Nature paper argues that classical gravity coupled to quantum matter can generate the relevant entanglement through a field-theoretic mechanism. This is a theoretical claim, not a reported observation of gravitationally mediated entanglement. [@H11] Marletto, Oppenheim, Vedral and Wilson contest the combination of an ultralocal nonrelativistic Hamiltonian with a propagator that reintroduces the discarded momentum term, and distinguish classical modulation of a quantum channel from classical mediation. [@H12]

Di Biagio emphasizes a separate qualification: subsystem mediation assumptions and relativistic no-signalling are different, and gauge-constrained field theories do not automatically admit the naive tensor-product decomposition. This is a criticism of overbroad interpretations of witness theorems, not a numerical renormalized-current closure. [@H13] Lin–Mondal's March 2026 paper calculates three quadrupole models and finds entanglement in its quantized tidal-parity model but not in its stated mean-field or stochastic alternatives. Its conclusion is model specific; it also illustrates how perturbative truncation can manufacture an apparent witness. [@H14]

We execute a small algebraic falsifier of that latter failure mode. Exact local evolution $U=e^{-i\eta\sigma_x}\otimes e^{-i\eta\sigma_x}$ maps $|00\rangle$ to a product state. Keeping only its first-order state, $|00\rangle-i\eta(|01\rangle+|10\rangle)$, and renormalizing yields apparent concurrence $2\eta^2/(1+2\eta^2)$, equal to $0.0196078$ at $\eta=0.1$. The apparent signal is at the omitted order and disappears in the exact channel. This does not replicate either gravity experiment; it tests the logic of taking a nonlinear witness after an uncontrolled truncation.

An actionable experiment must therefore compare complete channels under the same initial state, retain terms to the accuracy needed by the witness, bound electromagnetic and quantum-matter mediation, and identify which locality assumptions it tests. No gravity witness inferred from a source-field simulation should be presented as an observed quantum-gravity result.

## 9. Advisor decision: next experiments and rejection criteria

| Experiment | What is already available | Required advance | Decisive failure criterion |
|---|---|---|---|
| Bianchi-I finite-mode pressure test | Equations (H14)–(H16), symbolic work identity | Independent matrix-mode integration with evolving two scale factors | Energy Ward residual or unequal spin normalization beyond discretization error |
| Common four-dimensional subtraction | Local action identities and counterterm test | Hadamard/adiabatic expansion for current and all stresses in one convention | Gauge-shift or finite-scheme transformation changes a physical prediction |
| UV regulator comparison | Fixed-regulator identity only | Remove longitudinal and Landau cutoffs with a common covariant subtraction | Stable mean energy but drifting anisotropic pressure/shear |
| Causal fluctuation response | Lower-dimensional current-response primary benchmark | Tangent equations, then mixed current/stress kernels and smearing | Gauge-invariant growth not attributable to discretization or an EFT-discarded branch |
| Physical electron coupling | Scale-budget calculation | Perturbative gravitational correction or explicit external gravitating source | Visible order-one curvature from $b\sim100$ without an additional energy source |
| Cauchy-horizon bridge | Existing characteristic reduced model and regularity criteria | Specified state, charge evolution and extension norm | Endpoint changes under admissible state/subtraction variations without controlled error |

The down-selection is to complete the causal renormalized Maxwell–Dirac benchmark first, while using this anisotropic system as a verified gravitational interface. The full four-dimensional renormalized pressure calculation and noise response remain explicit research work. They have not been replaced by the classical fixture.

Public programmes are useful sources of methods and constraints, not evidence that a conjecture is true. For example, the European Commission-funded QuEST project ran in 2017–2019 and supported quantum-energy-condition and singularity research; the official university record establishes that historical funding, not a current machine or a solved quantum-gravity theory. [@H15]
