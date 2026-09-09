# Which new variables are legitimate bridges?

Research and equation audit, 9 September 2026. This report distinguishes changes to a finite model from a derivation of renormalized Einstein–QED. The new scalar sector is a hypothesis with independently testable conservation laws. It is not an established missing constituent of QED. Existing round-6 coefficient theorems remain the starting point.

## 1. Four changes that must not share one label

| Change | What actually changes | Required determining equation | What a successful test establishes |
|---|---|---|---|
| Regulator-dependent matching | Bare coefficients across a family of regulated descriptions | A fixed physical normalization condition and a common subtraction prescription | Agreement of specified observables within the family |
| Renormalization-group running | Description at an energy or subtraction scale | Beta functions and boundary values in a declared scheme | Scale consistency to the retained approximation order |
| A spacetime scalar, φ(x) | The physical field content and energy budget | A scalar action, initial data and Euler–Lagrange equation | Properties of an extended gauge–scalar model |
| A reconstructed pressure or current | The constitutive closure of the matter sector | State evolution and compatible composite-operator renormalization | A physical closure only if calculated independently of the conservation test |

Setting a coefficient equal to whatever makes a residual vanish proves an algebraic identity about that definition. It does not explain the underlying current or stress. A useful implementation must record which of these four operations it performs.

The exact-RG study by Igarashi and Itoh checks flow and quantum-master equations together. Its momentum regulator modifies how gauge symmetry is represented at finite cutoff; this is a concrete warning against assuming that an arbitrary cutoff preserves ordinary Ward identities. [QED in the Exact Renormalization Group](https://arxiv.org/abs/2107.14012).

## 2. Typed variables and their obligations

The same table is supplied in `variable_dependencies.json` for the proof graph. “Measured/matched” means constrained by a declared experiment or matching prescription; it does not mean that this project performed that measurement.

| Symbol | Type | What determines it | Ward/conservation consequence | Status of freedom | Missing proof or input |
|---|---|---|---|---|---|
| N | Nonnegative integer regulator label | Choice of retained Landau levels; limit specification | Finite-mode sums can break symmetries of the continuum regulator | Numerical resolution choice | Uniform current, stress and state estimates as N grows |
| K | Positive momentum-window regulator label | Choice of canonical integration window | A fixed window must transform with a canonical gauge shift | Numerical resolution choice | Joint regulator limit and regulator-shape independence |
| n_k | Quadrature resolution integer | Error tolerance for a fixed N,K | Refinement does not remove either physical cutoff | Numerical choice | Certified quadrature error; integral bounds do not transfer automatically |
| ν | Optional real interpolation label | Analytic continuation of a coefficient formula, if explicitly defined | Has no new spacetime Ward identity | Mathematical diagnostic | Does not define fractional Landau levels or an underlying Hilbert space |
| μ_R | Positive renormalization scale | Scheme choice and RG equation | Physical predictions should be μ_R-independent to stated accuracy | Description choice | RG consistency of the full retained current/stress, not just one term |
| e_R(μ_R) | Renormalized parameter as a function of scale | Beta function plus reference normalization | Must be combined with wave-function/vertex conventions | Matched, not a tunable time function | Applicable threshold treatment and perturbative error |
| z_B(N,K;μ_R) | Regulator-dependent bare gauge coefficient | Common regularized action and matching | Its current and stress variations must both be retained | Fixed after matching | Covariant derivation for this Landau/window regulator |
| χ_b | Existing finite-model susceptibility | The declared magnetic matching calculation | Changing it changes both the field equation and energy identity | Already matched within the old model | Justification in a new regulator or evolving geometry |
| φ(x) | Genuine scalar spacetime field | Scalar equation and admissible initial data | Its stress and exchange with gauge/matter sectors are required | New physical sector | Evidence for its couplings; scalar-model validity and well-posedness |
| f(φ) | Gauge kinetic function | Specified effective action; f>0 on the domain | Derivatives enter Maxwell and scalar equations | Functional model choice, then constrained | Matching or measurements; absence of unacceptable instabilities |
| V(φ), m(φ) | Potential and mass functions | Model definition or matching | Their derivatives enter scalar force and matter exchange | Functional model choices | Physical motivation and a renormalization prescription including scalar operators |
| b=e_R B/m_ref² | Derived dimensionless field | Maxwell/flux evolution with fixed reference units | Cannot vary independently of B, charge normalization and geometry | Derived observable | Re-derivation of modal dynamics when B or the basis changes |
| g_μν(x) | Metric field | Gravitational equations plus constraints | Bianchi identity requires conserved total source | Initial data plus evolution | Common renormalized quantum stress and gravitational existence theorem |
| ω₀ | Initial quantum state | Specified admissible two-point data and field equations | Determines finite state-dependent current/stress and noise | Physical initial data | Hadamard/adiabatic regularity and uniform ultraviolet tail control |
| Γ_q,ren | State-dependent quantum functional | In-in construction or an equivalent causal operator prescription | Common variations determine J, T and scalar density | Calculated object | Explicit strong-field curved-state implementation |
| J_q, ρ_q, p_⊥q, p_∥q | Composite observables | Same state, subtraction and finite counterterms | Must satisfy the force Ward identity jointly | Calculated, not free closure knobs | Independent current and directional-pressure evaluation |
| J_ext, T_support | Apparatus data and stress | A support model or explicit open-system work budget | Omitting support creates a total Ward defect | Specified physical setup | Consistent energy and pressure of the source |
| c_i(μ_R) | Local effective-action coefficients | Matching and renormalization conditions | Their full metric/gauge variations are linked | Matched EFT data | Valid operator basis, approximation order and higher-derivative treatment |

An analytic digamma formula can be evaluated at real ν. That is useful for plotting and asymptotics. It does not make N a physical continuously evolving variable. Likewise, a(t), the old dimensionless potential, and a_⊥(t), a_∥(t), the cosmological scale factors, must remain different symbols in code.

## 3. Bare matching and physical running are different calculations

For one charged Dirac species in the high-energy perturbative regime, the familiar one-loop equation is

\[
\mu_R\frac{de_R}{d\mu_R}=\frac{e_R^3}{12\pi^2}+O(e_R^5),\qquad
\frac1{e_R^2(\mu_R)}=\frac1{e_R^2(\mu_0)}-\frac1{6\pi^2}\log\frac{\mu_R}{\mu_0}
\]

at the displayed order. This is scale evolution, not a law for \(de/dt\). The integrated expression is meaningful only within its approximation and threshold assumptions. The coefficient agrees with the one-loop calculation in [Igarashi and Itoh](https://arxiv.org/abs/2107.14012). Physical charge normalization also needs a stated prescription: the Thomson-limit condition is one standard choice. [Dittmaier, Electric charge renormalization to all orders](https://arxiv.org/abs/2101.05154).

The formal pole in this one-loop extrapolation and the round-6 loss of positivity of a divided finite-model coefficient are distinct statements. Relating them needs a derivation of normalization, momentum scale, operator content and common subtraction. A graph of either quantity cannot establish that identification.

Ferreiro and Navarro-Salas explicitly introduce a mass scale into adiabatic subtraction and derive running couplings, including gravitational ones. The scale is a renormalization freedom in that construction, not an independently chosen time-dependent matter field. Their model-specific subtractions must be translated before use in this project. [Running couplings from adiabatic regularization](https://arxiv.org/html/1812.05564v2).

The round-6 coefficient admits an intentionally restricted reference-matching construction. Define a regulator-dependent coefficient by the condition

\[
Z_{N,K}^{\rm ref}(a_*)=z_*>0,\qquad
\chi_{N,K}^{\rm ref}=z_*-1+e^2C_{N,K}(a_*).
\]

Then exactly

\[
Z_{N,K}^{\rm ref}(a)=z_*+e^2[C_{N,K}(a_*)-C_{N,K}(a)].
\]

For the continuous symmetric momentum window and \(a_*=0\), round-6 monotonicity gives \(Z^{\rm ref}\ge z_*\). This is an honest coefficient lemma. It is not yet a covariant charge-renormalization theorem: the finite-window reference, state-dependent current, energy, gauge transformations and magnetic dependence must all be treated consistently. A discrete quadrature requires its own maximum bound. The advisor's `variable_contract.md` contains the selected matching experiment and its exact scope.

With a separate scalar coefficient, the same viable algebraic candidate is more transparently written

\[
\chi_{N,K}=\chi_R+e^2C_{N,K}(0),\qquad
Z_{N,K}(\phi,a)=f(\phi)+\chi_R+e^2[C_{N,K}(0)-C_{N,K}(a)]
\ge f(\phi)+\chi_R.
\]

Here χ_R is a fixed reference parameter and χ_N,K is **constant in time within each run** at fixed b,N,K. This candidate evades the fixed-χ obstruction by changing that obstruction's premise. It is not ruled out by the bounded-scalar no-go below. If \(\inf_D f+\chi_R>0\), it supplies the stated positive coefficient bound on D for the continuous symmetric window. This is a promising reference-subtracted finite closure, requiring a physical finite normalization condition before its identification with QED matching.

The old combined modal current is

\[
\mathcal J_{\rm comb}=S-C\dot x+Dx^2,\qquad
(1+\chi)\dot x=F-e^2\mathcal J_{\rm comb}.
\]

It is this **combination**, with the common state and subtractions, that must converge and obey the force identity. Removing the divergence of the isolated coefficient does not by itself establish convergence of the combined current. The canonical window and reference potential must transform together under a gauge shift; keeping the window fixed while relabeling a changes the regulated problem. A scalar-field extension also requires the action-derived \(\dot f\,x\) and scalar exchange terms. A time-dependent b would make the proposed χ_N,K vary unless the entire prescription were rederived; that case is outside this constant-per-run construction.

There is a simple diagnostic against silently making this matched coefficient a time-dependent knob. In the old finite equations, retain the old right-hand side but replace χ by χ(t). The already established cancellation now yields

\[
\dot W=xF+\tfrac12\dot\chi\,x^2,
\]

not \(\dot W=xF\). The extra work does not vanish because a numerical solver has a small residual. A gauge-kinetic field derived from an action has additional terms and an exchange sector, as below.

## 4. A consistent action for a genuinely new scalar

Use natural Heaviside–Lorentz units, signature \((-+++)\), \(F=dA\), and curvature
\(R^\rho{}_{\sigma\mu\nu}=\partial_\mu\Gamma^\rho_{\nu\sigma}-\partial_\nu\Gamma^\rho_{\mu\sigma}+\Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma}-\Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}\),
\(R_{\sigma\nu}=R^\rho{}_{\sigma\rho\nu}\). The local organizing action is

\[
S_{\rm loc}=\int\!\sqrt{-g}\,d^4x\left[
\frac{M_{\rm Pl}^2}{2}(R-2\Lambda)
-\frac14f(\phi)F_{\mu\nu}F^{\mu\nu}
-\frac12\nabla_\mu\phi\nabla^\mu\phi-V(\phi)
\right]+S_{\rm EFT}+S_{\rm support}.
\]

Here \(M_{\rm Pl}^{-2}=8\pi G\), \([\phi]=[M_{\rm Pl}]={\rm mass}\), and f is dimensionless. For example \(f(\phi)=\exp(2\beta\phi/F_\phi)\) is positive for finite φ, with dimensionless β and a mass scale \(F_\phi\). It is a chosen hypothesis. Scalar-dependent electromagnetic couplings have established precedents; they are not newly inferred from the failed cutoff extension. [Bekenstein's original variable-coupling framework](https://link.aps.org/doi/10.1103/PhysRevD.25.1527), [Gibbons–Maeda dilaton-gravity construction](https://www.sciencedirect.com/science/article/pii/0550321388900065).

Watanabe–Kanno–Soda give a directly relevant homogeneous anisotropic gauge–scalar action. Their coefficient is written \(f_{\rm WKS}(\phi)^2\); our coefficient is \(f(\phi)=f_{\rm WKS}(\phi)^2\). Consequently \(\dot f/f=2\dot f_{\rm WKS}/f_{\rm WKS}\). Copying their Maxwell term while using our logarithmic derivative would introduce a factor-of-two error. [Their action and basic equations](https://arxiv.org/html/0902.2833v2).

Add quantum matter through a renormalized closed-time-path functional \(\Gamma_{q,\rm ren}[g^\pm,A^\pm,\phi^\pm;\omega_0]\). An underlying Dirac convention can be chosen as \(D_\mu=\nabla_\mu-ie_R A_\mu\), \(\mathcal L_D=\bar\psi(i\gamma^\mu D_\mu-m(\phi))\psi\), with \(\{\gamma^\mu,\gamma^\nu\}=-2g^{\mu\nu}\). The sign of charge is a convention; all formulas below instead fix it operationally through the same functional variation:

\[
\delta\Gamma_q\big|_{\rm phys}
=\int\!\sqrt{-g}\,d^4x
\left[-\frac12 T^q_{\mu\nu}\delta g^{\mu\nu}
+J_q^\mu\delta A_\mu+\mathcal O_\phi\delta\phi\right].
\]

The physical-branch derivative is taken with respect to the plus variables before setting plus and minus equal. One must not first set the branches equal and then vary the identically normalized diagonal functional. Causal equations from the in-in framework are the relevant target for particle-creation backreaction. [Hu, Quantum Statistical Field Theory in Gravitation and Cosmology](https://arxiv.org/abs/gr-qc/9403061).

Ignoring additional EFT terms **only for the explicitly two-derivative bridge**, variation gives

\[
\nabla_\mu(fF^{\mu\nu})=-(J_q^\nu+J_{\rm ext}^\nu),\qquad
\Box\phi-V'(\phi)-\frac14f'(\phi)F^2+\mathcal O_\phi=0,
\]

\[
M_{\rm Pl}^2(G_{\mu\nu}+\Lambda g_{\mu\nu})
=T^{\rm EM}_{\mu\nu}+T^{\phi}_{\mu\nu}+T^q_{\mu\nu}+T^{\rm support}_{\mu\nu},
\]

\[
T^{\rm EM}_{\mu\nu}=f\left(F_{\mu\alpha}F_\nu{}^\alpha-\tfrac14g_{\mu\nu}F^2\right),\quad
T^\phi_{\mu\nu}=\nabla_\mu\phi\nabla_\nu\phi-g_{\mu\nu}\left[\tfrac12(\nabla\phi)^2+V\right].
\]

If the quantum action depends on φ only through m(φ), the formal scalar operator is \(\mathcal O_\phi=-m'(\phi)\langle\bar\psi\psi\rangle_{\rm ren}\); the composite operator and its local counterterms still need a prescription. The equations specify the obligation, not a numerical closure.

Our definition \(J=+\delta\Gamma_q/\delta A\) differs in sign from conventions defining the current with a minus sign. With physical electric components \(E_{\hat i}=F_{\hat i\hat0}\), the homogeneous Maxwell equation has \(f\dot E+(2H_\perp f+\dot f)E=-J\). This reduces to the earlier \(\dot E+2H_\perp E=-J\) when f=1. Keeping this sign translation explicit prevents importing an inconsistent force identity from another convention.

## 5. The new field must pay its energy cost

Gauge and diffeomorphism invariance of the common, anomaly-free prescription give

\[
\nabla_\mu J_q^\mu=0,\qquad
\nabla^\mu T^q_{\mu\nu}=F_{\nu\mu}J_q^\mu+\mathcal O_\phi\nabla_\nu\phi.
\]

These follow by varying \(A_\mu\to A_\mu+\nabla_\mu\lambda\), then applying a compactly supported diffeomorphism with \(\delta A_\mu=\xi^\rho F_{\rho\mu}+\nabla_\mu(\xi\cdot A)\), integrating by parts, and using the same functional derivatives. A scalar inserted only into Maxwell's denominator does not satisfy this argument.

The local identities, with J_ext=0, are

\[
\nabla^\mu T^{\rm EM}_{\mu\nu}=-F_{\nu\mu}J_q^\mu-\tfrac14F^2\nabla_\nu f,
\quad
\nabla^\mu T^\phi_{\mu\nu}=(\tfrac14 f'F^2-\mathcal O_\phi)\nabla_\nu\phi.
\]

Their sum with the quantum force identity vanishes. These signs can also be checked through the homogeneous energy budget:

\[
Q_{\rm EM}=-EJ_q+\frac12\dot f(B^2-E^2),\quad
Q_\phi=\mathcal O_\phi\dot\phi-\frac12\dot f(B^2-E^2),\quad
Q_q=EJ_q-\mathcal O_\phi\dot\phi.
\]

Here \(Q_i=\dot\rho_i+2H_\perp(\rho_i+p_{\perp i})+H_\parallel(\rho_i+p_{\parallel i})\). Thus the established Bianchi-I constraint-propagation lemma becomes applicable **if** these actual calculated sources meet their premises. The round-7 selected gauge–scalar gravitational benchmark deliberately has no quantum matter: \(J_q=\mathcal O_\phi=T_q=0\). A successful benchmark tests the classical exchange and gravity implementation. The separate finite scalar–QED variational completion tests another specified finite model. Neither validates a covariant curved-space quantum stress that has not been computed.

Zahn proves covariant Dirac-current conservation with gauge backgrounds and characterizes its charge-renormalization ambiguity. His section 4.2 stress argument explicitly specializes to constant mass and vanishing gauge curvature, with a perturbative alternative discussed. It cannot be promoted to a completed nonperturbative strong-F stress closure. [Zahn, Proposition 4.1 and section 4.2](https://arxiv.org/pdf/1210.4031). Hollands–Wald establish conservation conditions for their perturbative scalar-field construction; this is a methodological foundation, not our charged Dirac Bianchi-I solution. [Hollands–Wald](https://arxiv.org/abs/gr-qc/0404074).

## 6. A bounded new scalar cannot repair the unchanged cutoff family

**Conditional no-go lemma.** Retain the same C and χ as round 6, keep e²>0 fixed, and replace only the constant 1 by a scalar coefficient f. Let D be any scalar domain with finite \(f_{\max}=\sup_{\phi\in D}f(\phi)\). Then

\[
\sup_{\phi\in D} Z_{N,K}(\phi,0)
\le f_{\max}+\chi_b-e^2C_{N,K}(0)\longrightarrow-\infty
\]

as N,K grow cofinally. The final limit is the already proved round-6 positive-kernel obstruction. Therefore no bounded scalar coefficient supplies a positive margin uniform across the unchanged joint-cutoff family.

This includes every compact scalar domain with continuous f. A finite constant offset also fails. If \(f=e^{2\beta\phi/F_\phi}\), permitting φ to grow with the regulator may make f large enough algebraically, but then the physical scalar data and locally normalized charge \(e_{\rm eff}\approx e_R/\sqrt f\) change with the regulator. That is not convergence of a fixed physical problem. The approximate effective-charge relation is local and assumes slow enough scalar variation to interpret canonical normalization; derivative interactions are otherwise relevant.

The lemma does not rule out a consistently rederived renormalized current in which separately divergent pieces cancel before division. It also does not rule out new physics. It rules out this particular bounded-coefficient patch of the old formula. The scalar dynamics, the matched coefficient construction and the original finite closure are separate proof branches.

## 7. Further holes exposed by the source comparison

1. **A local constant is not a memory kernel.** Vacuum polarization can be dispersive and nonlocal. Donoghue–El-Menoufi derive curvature-dependent nonlocal structures for massless QED; their result is not a massive strong-field solution, but it demonstrates why substituting a local running number into a general curved equation is insufficient. [Covariant non-local action](https://arxiv.org/abs/1507.06321).
2. **An expansion needs a regime.** Drummond–Hathrell compute curvature corrections to the photon action; Shore analyzes dispersion beyond the lowest derivative approximation. Neither permits blindly using a low-order local polynomial at electron-scale curvature or arbitrary field gradients. [Drummond–Hathrell](https://link.aps.org/doi/10.1103/PhysRevD.22.343), [Shore](https://arxiv.org/abs/gr-qc/0203034).
3. **A disputed current cannot settle a different geometry.** Banyeres–Domènech–Garriga analyze local vacuum-polarization contributions and negative-current interpretations in de Sitter. [Paper, revised June 2025](https://arxiv.org/abs/1809.08977). Bastero-Gil and collaborators instead study a supported dynamical constant-electric-field prescription with a different matching condition; their April 2026 revision explicitly leaves the metric and stress dynamics outside the calculation and uses a zero-magnetic-field analytic setup. Its own scope blocks treating it as our magnetized Einstein–QED closure. [Sections 2 and 2.3](https://arxiv.org/html/2508.14973v2). These papers define hypotheses to compare, not permission to delete inconvenient finite terms.
4. **An external background has a source.** Holding E or B fixed during expansion needs support or a modified field sector. Our scalar model computes its exchange. If J_ext is retained and its stress omitted, the old \(Q_{\rm total}=-EJ_{\rm ext}\) defect remains.
5. **A changing B changes more than χ.** Landau masses, degeneracies, reference units, state preparation and potentially the mode basis change. Replacing b by b(t) inside the old flat, fixed-B ODE is a new approximation requiring a derivation. It is not the scalar Bianchi-I model already tested this round.
6. **Effective terms must be counted once.** If a retained fermion's loop supplies Euler–Heisenberg terms, do not add that same loop again as a free local coefficient. If curvature-squared operators are retained, include their metric variations or a declared order-reduction prescription. Their omission cannot be hidden by naming the equation semiclassical Einstein.

## 8. Bidirectional proof obligations for the next physical bridge

Forward direction: specify a gauge-covariant regulator and initial state → derive one common subtraction and finite matching → calculate current, scalar density and directional stress → establish their force Ward identity and uniform bounds.

Backward direction: seek a constrained semiclassical gravitational evolution → require a well-defined, conserved source with suitable regularity → require independently computed quantum stress and current → require the same state and counterterms in all composite observables.

The two directions meet at the **common renormalized current-and-stress construction**, not at an adjustable scalar coefficient. Completed algebraic and classical results can support this bridge; they cannot supply its missing premise. The next useful falsifier is a common-state Ward residual computed from independent observables while varying N, K and quadrature separately, with normalization held fixed. Only after that passes should a proof planner admit a new physical-closure edge.

## Source-selection record

This is a targeted primary-source audit resolving the variable, matching, Ward-identity and action questions. It is not a claim to have read every relevant paper or every country's project. `renormalization_sources.json` records exact links, inspected scope and relevance; `variable_dependencies.json` distinguishes hypothesis, calculated observable and regulator metadata for downstream tooling.
