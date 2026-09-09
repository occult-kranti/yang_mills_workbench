# Research roadmap: gates toward the coupled electromagnetic–quantum–gravity problem

This is a completion plan for a research programme, with explicit conditions for retiring, revising or accepting each claim. It does not promise that the unrestricted open problem has an analytic solution, nor assign a completion percentage to fundamental physics. The next numerical deliverable is P3 in `response_contract.md`; the other branches remain planned unless an execution record explicitly says otherwise.

## The master question must have a state, scale and observable

The shared master system is a metric, an Abelian gauge connection, a charged quantum Dirac field and, where needed, specified scalar moduli. A local classical/EFT organization is

\[
S=\int d^4x\sqrt{-g}\left[\frac{M_{\rm Pl}^2}{2}R-V(\phi)-\frac12G_{ab}(\phi)\nabla\phi^a\nabla\phi^b
-\frac14Z_F(\phi)F^2+\frac14\theta(\phi)F\widetilde F
+\bar\psi(i\gamma^\mu D_\mu-m(\phi))\psi\right]+S_{\rm local,EFT}+S_{\rm support}.
\]

The EFT terms may include \(R^2,R_{\mu\nu}R^{\mu\nu},RF^2,R_{\mu\nu}F^{\mu\alpha}F^{\nu}{}_{\alpha},R_{\mu\nu\rho\sigma}F^{\mu\nu}F^{\rho\sigma},(F^2)^2,(F\widetilde F)^2\), with coefficients of the appropriate dimensions and a stated truncation scale. A constant \(\theta F\widetilde F\) is a total derivative in local Abelian bulk equations; a spacetime-dependent scalar coefficient need not be. Arbitrarily appending every operator without an EFT power counting changes the problem instead of completing it.

For causal mean fields, the state-dependent matter functional is an in-in/closed-time-path functional. The loop-driven feedback is represented by its current and stress derivatives, including mixed responses. It is not one missing elementary local coupling. A local Euler–Heisenberg approximation can summarize an appropriate low-frequency part of the matter loop; it must not be added a second time when that same loop is already dynamically evaluated. Curvature near \(m_e^2\), electric fields near criticality and magnetic fields above criticality do not jointly justify a weak-curvature or weak-field expansion.

The target observables should be selected before the corresponding solver: charge loss, renormalized flux/current, horizon regularity in a specified norm, or conversion probability. “Unify the four theories” is too broad to be a numerical boundary-value problem.

## Stage ladder and decision ownership

| Stage | Mathematical object | Minimum reproducible gate | Current disposition |
|---|---|---|---|
| P0 | Conventions, EFT hierarchy, source/state definition | Every dimension and sign independently checked; support stress identified | Maintained, with explicit source/report errata |
| P1 | Prescribed Dirac modes | Exact flat/expansion benchmarks, endpoint and tolerance checks | Round-3 evidence retained |
| P2 | Matched causal mean current and energy | Same-regulator work identity, independent spinor solver, separate cutoff axes | Round-3 finite model accepted in its tested scope |
| P3 | Homogeneous longitudinal retarded response | Tangent/finite-difference/spinor agreement, delayed causality, held-out fixture | New implementation and review this round |
| P3b | Response spectrum and state families | Multiple independent probes, compact-support state perturbations, direct kernel reconstruction | Planned |
| P3c | Connected quantum noise | Smeared current covariance and a controlled quantum comparator | Planned; P3 is insufficient |
| P4 | Covariant anisotropic current and full stress | One local scheme; force Ward identity, pressures, anomaly/limit checks | Derived interface only; no quantum Einstein run |
| P5 | Einstein–Maxwell–Dirac mean-field evolution | Initial constraints, propagated constraints, physical scale budget, joint regulator control | Blocked on P4 |
| P6 | Geometry-specific physical conclusion | Relevant asymptotics, state variations, independent method and error budget | Separate branches below |

The advisor approves the model and interpretation; the implementation agent owns code; the verifier owns independent representations and falsifiers. A successful build or a majority of agents agreeing is not evidence for a physical hypothesis. A failed scientific gate remains in the record. A corrected code artifact must be identified by the actual delivered source hash.

## Branch A: WGC, Festina Lente and charged de Sitter discharge

The electric WGC is an existence condition on a sufficiently charged state relative to an appropriate extremality relation, not a requirement that every species satisfy an unspecified \(q/m\geq1\). A magnetic version gives a parametric EFT cutoff under monopole assumptions. Scalar forces, moduli-dependent gauge couplings and higher-derivative terms change the extremality/force comparison; their distinct formulations cannot be silently interchanged.

The March 2026 revision of Abu-Ajamieh and collaborators states its use of the flat extremality relation as a local small-hole approximation in quasi-de Sitter and identifies an extra assumption when extending to massive mediators. Its constraints are conditional on the conjectures. The modern paper is therefore a useful assumption ledger, not an experimental proof of WGC or Festina Lente. [R08]

The branch should proceed in this order:

1. Fix reduced Planck mass and physical charge conventions and derive the RN-dS metric from the selected action. Locate roots and double-root loci with interval-bracketed root finding; distinguish inner/event degeneracy from event/cosmological Nariai degeneracy.
2. Add one EFT correction at a time and derive the perturbative extremality shift. Compare equations obtained before and after a permitted field redefinition; track transformed observables.
3. Choose the near-horizon state and calculate discharge through a controlled dyonic near-horizon approximation. Compare the exact mode result to local constant-field asymptotics only where its gradient scale is adequate.
4. Add energy and charge flux together. A charge-loss ODE with no accompanying mass/energy flux is not a closed black-hole decay model.
5. Examine the dimensionless path through the allowed horizon region under changes of light-particle masses, charges and scalar parameters. Test consistency of decay-channel assumptions before using the path to infer a conjectural bound.

**Hypothesis A1.** A specific higher-derivative coefficient changes the extremality/discharge competition within EFT uncertainty. **Null:** the inferred change is smaller than the omitted operator order or vanishes under a consistent field redefinition. **Reject a conclusion** if it depends on coefficients outside positivity/causality or matching assumptions actually imposed, or on a spurious higher-derivative branch.

**Required output:** a convention-checked horizon map, flux budget and sensitivity table. A flat homogeneous pair-current experiment is method development; it cannot directly decide de Sitter black-hole discharge.

## Branch B: strong electric/magnetic pair creation and backreaction

P3 is the immediate down-selection because its full initial-value system is already specified and its derivatives can be checked independently. The question is whether a physical change of preparation produces a reproducible causal change in the mean field, and how that response depends on the retained modes.

**Hypothesis B1.** The coupled tangent solution equals the derivative of the independently solved nonlinear family. **Null:** discrepancies do not vanish in the central-difference truncation regime and persist under tolerance refinement. This is an implementation hypothesis, not a discovery about fundamental QED.

**Hypothesis B2.** The response remains insensitive to admissible regulator refinements over a specified finite interval. **Null:** the response drifts despite stable background energy. Increase momentum nodes at fixed window, then longitudinal window at comparable resolution, then Landau cutoff. Repeat against at least two initial preparations before extending the interval.

**Hypothesis B3.** Strong response is caused by a physical collective mode rather than source normalization or field-zero division. **Null controls:** a fixed nonzero normalization, delayed probes, phase-aligned trajectories, and a direct retarded-kernel reconstruction remove the apparent growth. A finite-time sensitivity plot does not establish an asymptotic Lyapunov exponent.

**Hypothesis B4.** A controlled approximation can reproduce the appropriate fully quantum comparator. Use the existing 1+1 bosonized frequency correction as a separate exactly identified model. The approximation must match that model's degrees of freedom and expansion order before a discrepancy can diagnose physics. It is invalid to transfer its numeric error bar to 3+1 dimensions. [R05]

Next, evaluate a smeared current noise kernel and compare intrinsic/state-induced response families. Then derive the Bianchi-I current and two pressures from one scheme. An axisymmetric dipole background comes after homogeneous anisotropic validation because its field gradients mix modes and require support currents. A magnetic field that is spatially uniform in the benchmark cannot be labeled a solved magnetar.

The new finite-interval scalar screening paper [R07] provides a complementary boundary-sensitive electrostatic benchmark. Its stationary nonlinear eigenproblem is a useful future validation branch. It does not replace causal time evolution, and a stable iteration map is not physical dynamical stability.

## Branch C: Cauchy horizons, mass inflation and evaporation

The July 2026 compact-trapped-region paper distinguishes finite-lifetime inner trapping horizons from eternal Cauchy horizons. In its s-wave Polyakov models, finite-time stress can remain finite while growing rapidly; inner-extremal models soften the growth. Its conclusions explicitly require a future self-consistent backreaction calculation to establish a long-lived endpoint. [R09]

That distinction corrects two tempting inferences: “finite RSET at each finite time proves stability” and “a background with no singular center solves mass inflation.” Neither follows.

1. Reproduce a classical double-null charged-scalar collapse/mass-inflation fixture, with explicit charge normalization, null constraints and two independent characteristic grid resolutions.
2. Track invariant areal radius, Misner–Sharp mass, surface gravity where defined, and parallel-propagated tidal observables. A coordinate component alone is inadequate for regularity.
3. Add a clearly labeled two-dimensional Polyakov source in a specified in-state. Check its Ward identity and Schwarzian transformation terms before any four-dimensional interpretation.
4. Separate finite-lifetime, eternal and inner-extremal background families. Test whether changing the lifetime or near-horizon degeneracy changes the observed growth law before the model's curvature cutoff is reached.
5. Replace the toy source with the covariant charged-matter current/stress closure only after P4. Include charge transport and external/source energy consistently.
6. State the extension regularity being tested: metric continuity, differentiability, locally integrable connection, or finite tidal distortion. Different cosmic-censorship statements use different conditions.

**Hypothesis C1.** Backreaction modifies the inner-horizon growth before the EFT validity boundary. **Null:** the proposed change occurs only after curvature or noise invalidates the retained model. **Hypothesis C2.** Inner extremality is dynamically approached and stable. **Null:** small admissible perturbations destroy degeneracy or excite other instabilities. The current cited backgrounds do not establish this dynamical attraction.

**Required output:** a constraint-verified characteristic solution with a stopping surface at the stated physical validity bound. A finite-grid endpoint is not an answer to the unrestricted singularity question.

## Branch D: resonant photon–graviton conversion

The transverse photon dispersion relevant to a propagating wave is not determined by the longitudinal, zero-spatial-momentum P3 susceptibility. This is an important interface restriction: a tensor response must be calculated at the relevant momentum and polarization.

The August 2026 finite-field birefringence paper gives a useful low-frequency comparison. It warns that a maximum obtained by retaining an unexpanded one-loop algebraic expression is not controlled at higher loop order. We should compare strict-order and unexpanded prescriptions explicitly; a visually striking feature is not automatically a robust strong-field prediction. [R11]

The July 2026 photon–graviton Leggett–Garg analysis assumes quantized gravitational perturbations and a particular measurement protocol. Its proposed witness is distinct from conversion probability; loss, invasiveness and reconstruction assumptions require independent controls. It contains no completed ultrastrong-field Euler–Heisenberg dispersion transport. [R10]

For one transparent polarization sector, normalize amplitudes so that

\[
i\frac{d}{d\ell}\begin{pmatrix}A_\gamma\\A_g\end{pmatrix}
=\begin{pmatrix}\Delta_\gamma(\ell)-i\Gamma_\gamma(\ell)/2&\Delta_M(\ell)\\
\Delta_M(\ell)&\Delta_g(\ell)\end{pmatrix}
\begin{pmatrix}A_\gamma\\A_g\end{pmatrix}.
\]

Every coefficient must follow from the same normalized quadratic action. For constant lossless coefficients, an exact two-state matrix exponential is the first benchmark. For variable coefficients, independently compare norm-preserving integration and ordered matrix products. At \(\Delta_\gamma=\Delta_g\), resonance is possible; neither a large \(B\) nor a large birefringent phase alone establishes efficient conversion.

1. Reproduce the lossless constant-field conversion and its zero-coupling limit.
2. Add polarization-dependent QED dispersion within its actual frequency/field domain, plus plasma dispersion separately.
3. Include absorption and photon splitting if energetically relevant. Check probability accounting into all retained channels.
4. Use a specified supported dipole/plasma profile and identify coherence length and resonance width. A numerical step must resolve both.
5. Propagate profile and subtraction uncertainties. Distinguish changes of near-surface phase from changes of far-field observable polarization or conversion.
6. Only then add a nonclassicality-witness proposal with a complete measurement channel and noise model.

**Hypothesis D1.** A specified plasma profile compensates QED mismatch and produces a robust conversion feature. **Null:** the feature vanishes when absorption, profile uncertainty or consistent loop order is included. **Hypothesis D2.** A proposed witness distinguishes the quantized channel. **Null:** an allowed classical measurement disturbance, electromagnetic path or truncated state reproduces it.

## Practical solver choices and stop rules

| Subproblem | Preferred first tool | Why it is feasible | What makes it expensive |
|---|---|---|---|
| P3 finite response | NumPy/SciPy vectorized mode+tangent ODE | Exact derivatives and independent spinor representation | High-momentum phase resolution and time horizon |
| Covariant subtraction | SymPy plus independently documented tensor algebra; xAct if available | Local coefficients and Ward identities are symbolic | State dependence and anisotropic mode mixing remain numerical |
| Stationary screened electrostatics | Spectral collocation plus continuation | One spatial dimension and explicit boundaries | Eigenvalue collisions and noncontractive iteration |
| Double-null horizons | Characteristic finite differences with constraints | Natural causal coordinates | Blueshift, stiffness, state source and boundary control |
| Conversion transport | Matrix exponentials/ordered products and adaptive ODE | Small linear system with exact constant-coefficient limits | Accurate physical coefficients and very small probabilities |

PINNs may be compared after a trusted solver exists. A low training loss does not establish a renormalized Ward identity, a resolved horizon or a rare-event probability. Neural surrogates should carry a validity domain and held-out residual/error tests; they do not replace the reference data generator.

The programme advances only when the next missing physical or numerical dependency is identified. If a branch fails, preserve the failure, identify whether it arose from the theory, implementation, state, regulator or observation model, and revise the hypothesis. More agents or more citations should be allocated only when they can resolve that concrete uncertainty.
