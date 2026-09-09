## Synthesis: a staged research programme with rejection rules

The useful combination of partial solutions is a dependency graph expressed as tests. The matched flat current is a reference for the zero-expansion limit of a curved solver. The gravity fixture supplies independent constraint identities. The fully quantum comparator and retarded-current literature test the mean-field approximation. None of these outputs can simply be added to obtain a solved spacetime.

| Stage and hypothesis | Required calculation | Observable and rejection condition | Status |
|---|---|---|---|
| P1: finite magnetic matching survives causal evolution | Shared mode current/energy and weak pumped-field experiment | Reject if the physical low-frequency response is erased despite conservation | Executed; matched model passes tested comparison |
| P2: late field reversal is quadrature-resolved | Fixed-window momentum refinement, separate window and Landau checks | Reject stated precision if any component shift exceeds it | Executed; approximate reversal accepted, rigorous continuum bound absent |
| P3: the selected mean-field trajectory is stable to quantum response | Retarded-current commutator and perturbed-state evolution | Track growth relative to the background; reject validity if small perturbations grow beyond the declared regime | Proposed; the separate one-dimensional quantum comparator is executed |
| P4: anisotropic stress closes with the same subtraction | Compute current, energy, transverse and longitudinal pressure from the same modes and counterterms | Ward residual and Einstein constraint must converge together | Finite identities derived; full covariant quantum subtraction unfinished |
| P5: weak curvature reproduces both independent limits | Small anisotropic expansion, zero-expansion matched limit and zero-field anomaly checks | Reject a shortcut if it loses a basis connection or a curvature counterterm | Classical gravity fixture and prior external-field tests executed; coupled quantum test proposed |
| P6: target curvature has a realizable support budget | Solve initial Einstein constraints including matter, pump and magnetic supports | Reject a nominal target if its curvature is imposed without the required stress | Electromagnetic scale obstruction quantified |
| P7: resonant conversion survives a matched dispersive treatment | Transverse polarization tensor, mixed vertex and flux-normalized transfer system | Compare phase mismatch, absorption and full flux; reject an index-only inference | Proposed; constant two-state identity retained |
| P8: charged-horizon claims survive causal flux evolution | Geometry-matched current/stress, horizon-regular state and evolving mass/charge | Monitor constraints and continuation regularity at the actual horizons | Open; homogeneous calculation cannot decide it |

### Why the numerical method was down-selected

| Candidate | Symmetry and boundaries | Numerical hazard | Best first method | Advisor decision |
|---|---|---|---|---|
| Matched homogeneous Maxwell–Dirac | Temporal initial-value ODEs; Landau and momentum modes | Fast phases, subtraction cancellation, UV and quadrature limits | Vectorized adaptive ODE plus independent spinors and analytic limits | Selected and executed |
| Bianchi-I quantum backreaction | Homogeneous anisotropic metric plus modes | Two pressures, common covariant subtraction, constraints | Symbolic derivation then constrained ODE/mode integration | Interface and classical fixture executed |
| Spherical charged quantum interior | Double-null $1+1$ geometry plus state-dependent flux | Inner-horizon blueshift, stiff null layers, stress regularity | Characteristic finite differences with constraint refinement | Full evolution deferred until closure is specified |
| Static or slowly varying conversion ray | Two/four polarization amplitudes along a ray | Resonance layers, rapid phase and damping | Adaptive transfer ODE; spectral methods for smooth boundary problems | Requires matched quantum kernel |
| Axial multipolar Einstein–QED | Nonlinear geometry plus nonlocal matter state | Gauge/gravity constraints, UV subtraction, support, memory | Established numerical-relativity infrastructure plus verified quantum module | Research-scale integration, not a reasoning-only solution |

A PINN is not a remedy for an unspecified current or stress. It can interpolate or approximate a well-defined solution only after loss scaling, initial-state constraints and independent residual/error checks are established. High-frequency mode phases and competing physical scales are concrete hazards. Chebyshev collocation is suitable for smooth finite-domain boundary problems with well-treated endpoints; it is not inherently preferable to a causal initial-value solver here. [@ROOT13]

### Open-source tool choices and what was actually used

NumPy, SciPy, SymPy and mpmath supply the executed array integration, symbolic identities and high-precision benchmarks. The package contains complete project-authored Python and saved outputs. It does not replace those libraries with a new numerical framework. Requirements record the versions used; small independent checks can be rerun separately from the costly production mode evolution.

WarpX, Smilei and Ptarmigan are valuable strong-field simulation comparators, but their documented QED modules or reference configurations must be matched to the mechanism. Photon-emission and photon-induced pair Monte Carlo models do not automatically implement vacuum Schwinger production with a four-dimensional renormalized in-in stress tensor. None was used here as a substitute for that missing calculation. [@ROOT03; @ROOT05; @R235; @R236]

Two author GitHub repositories were inspected in this pass. One demonstrates Qiskit Schwinger-model simulations; the other is an external-field Schwinger plotting project with work-in-progress extensions. Their READMEs were checked, not their complete code or runtime output. Neither was represented as a ready-made three-dimensional causal gravity-backreaction solver. The educational quantum simulation can inform a separate lattice benchmark only after Hamiltonian normalization, truncation and continuum extrapolation are specified. [@N04; @N05]

For study, use the earlier source ledger's accessible proper-time QFT chapter, the initial-value pair-production review and the Dirac renormalization papers as a sequence: derive mode normalization, reproduce the exact pulse, derive the shared subtraction, then reproduce the weak response and the coupled experiment. Reading an entire textbook is not a prerequisite to checking a specified identity, but reading a source's abstract is not enough to claim its derivation was reproduced. [@R238; @C03; @V04]

### What would count as a new result

A new converged solution of a previously specified initial-value problem can be a useful research result even if it is not a solution of quantum gravity. A publishable novelty claim additionally needs a prior-art comparison, matched limiting cases, a physical observable, uncertainty from model and numerical approximations, and reproducible evidence that does not depend on selecting only successful parameter points. This run offers a corrected research foundation and executed partial solutions. It makes no priority or publication claim.

Before expanding the project again, the next advisor milestone is P4: implement covariantly compatible directional stresses and verify the shared Ward identity in an anisotropic background. P3 should run alongside it, because a beautifully conserved coupled mean field can still lie outside its fluctuation-validity regime. The original dipole, charged horizons and curvature of order $m_e^2$ should then be introduced in separate controlled stages, each with its own supporting sources and rejection conditions.

