# Advisor decision: close the causal electromagnetic loop before extending gravity

This third round changes the computational target. The previous work verified several external-background mode calculations but did not evolve the electric field using the resulting quantum current. That is the principal incomplete dependency. Another accurate calculation with a prescribed electric field would not close it. The immediate target is therefore a causal, homogeneous spinor Maxwell–Dirac initial-value problem at fixed parallel magnetic field, with a shared current/energy subtraction and explicit cutoff tests. This is a meaningful step toward the original coupled problem; it is not the complete Einstein–QED system.

The panel roles below are functional reviews performed by agents. They do not imply that named human specialists reviewed the project.

| Panel role | Question that can falsify the work | Required artifact |
|---|---|---|
| Current and renormalization theorist | Does the current preserve both quantum coherence and the physical finite magnetic susceptibility? | Independently derived mode current, shared energy subtraction and charge-matching limit |
| Numerical Hamiltonian implementer | Does the induced current actually change the field, with the correct energy/work sign? | Runnable coupled solver, raw invariants and source-off evolution |
| Independent verifier | Are regulator, quadrature, time-step and initial-state errors separated? | Alternative formulation and numerical limits that do not reuse the implementation |
| Gravity and effective-field-theory critic | Is the chosen geometry compatible with the stress, and does its constraint propagate? | Bianchi-I equations, pressure requirements, symbolic constraint test and counterexamples |
| Source and empirical critic | Which claims are primary results, models, criticisms, project plans or unsupported extrapolations? | Targeted primary-source ledger and testable hypotheses |

The root agent reviews the interfaces and maintains the research record. Increasing agent count is not a substitute for agreement on physical conventions.

## The previous numerical precision claim needs a narrower interpretation

The previous maximum intersolver difference of approximately $2.14\times10^{-16}$ was a measured difference between four-component and reduced-sector occupations in four cases. It was not a certified error bound for either solver. The runs shared DOP853, double precision and closely related finite endpoint states. Their maximum subspace/norm residuals were of order $10^{-12}$. A norm residual is not itself a lower bound on occupation error: nearly radial state error can have a much smaller effect on a small transition probability. Nevertheless, small intersolver disagreement alone does not constrain shared state, discretization or model errors.

A stronger check was missed. In the expansion-only case the fixed sector Hamiltonian is

$$h_s=a_g(t)\sigma_1-s c\sigma_2+K\sigma_3,\qquad c=\sqrt{2bn}.$$

The last two coefficients are constant. A time-independent unitary transformation therefore turns this into a Sauter two-level problem with longitudinal momentum $a_g(t)$ and constant transverse mass $\sqrt{c^2+K^2}$. For $a_g=1+\eta[1+\tanh(t/T_g)]/2$, the equivalent parameters are

$$K_{\rm eff}=1+\eta/2,\quad a_{\rm eff}=\eta/(2T_g),\quad T=T_g,\quad M_{\rm eff}=\sqrt{2bn+K^2}.$$

Consequently the expansion-only benchmark has an analytic asymptotic occupation. It was a useful counterexample to the naive changing-mass reduction, but should not be presented as a new analytically unsolved transition problem. At $\eta=1,T_g=0.5,b=10,n=1,K=0$, independent 70-digit evaluation gives

$$N=0.0000018823980738606970962996337658613292144640557795350464471236323376.$$

The prior four-component result differs by approximately $2.2492\times10^{-16}$, or $1.19\times10^{-10}$ relative. Its norm residual was approximately $4.20\times10^{-12}$. The recorded value is consistent with the exact result at the stated absolute scale; the interpretation of the tiny intersolver difference was too strong if read as a global accuracy guarantee. `advisor_checks.py` reruns finite-time and tolerance scans and records the exact comparison without importing either previous solver.

The new audit initially set an ambitious absolute-error target of $10^{-18}$ for its tightest double-precision run. That target failed: the measured error was $1.8243\times10^{-18}$, with a sampled norm residual around $5.37\times10^{-14}$. The saved JSON preserves the failed gate. This does not invalidate the resolved transition probability, but it does forbid claiming the stricter requested accuracy. The exact analytic comparator is a stronger validation than agreement between two related discretizations.

## Primary literature changes the renormalization contract

Three source checks materially affect the implementation. The initial-value review by Kluger, Eisenberg and Svetitsky explains why ultraviolet-compatible initial states are required and why a particle-only kinetic source loses phase information. We inspected its initial-state and spinor-renormalization sections, not just the abstract. [Pair production as an initial-value problem](https://arxiv.org/pdf/hep-ph/0311293).

Beltrán-Palau, Navarro-Salas and Pla distinguish adiabatic order assignments for the gauge potential and test them against covariance, the anomaly and the Schwinger–DeWitt expansion. Their four-dimensional electric-background prescription must not be assumed identical to a magnetic-field-resummed flat-space subtraction. We inspected the prescription, comparison and charge-scale sections. [Adiabatic regularization for Dirac fields](https://arxiv.org/pdf/2001.08710).

Domcke, Ema and Mukaida explicitly separate pair production, charge running and nonlinear vacuum response in parallel electric/magnetic fields. Their Landau sum and charge-matching derivation provide a direct check on the subtraction below. In particular, a finite current is not automatically a pure conduction current. We inspected the vacuum-current derivation and its matching equations. [Chiral anomaly, Schwinger effect and Euler–Heisenberg response](https://arxiv.org/pdf/1910.01205).

These sources motivate the distinctions; the finite-system energy identities and matching algebra below are independently derived in this project. The full covariant strong-field stress tensor is not supplied by those identities.

## Frozen equation contract

Use Heaviside–Lorentz units, $\hbar=c=1$, positive charge magnitude $e$, and electron mass $m$. Define

$$s=mt,\quad a=eA_z/m,\quad \mathcal E=eE_z/m^2,\quad b=|eB|/m^2,\quad P=K-a,\quad M_n^2=1+2bn.$$

The charge convention uses the positive-charge member of the pair; $a'=-\mathcal E$ and $P'=\mathcal E$. For each Landau/momentum mode,

$$h_n=(M_n,0,P),\qquad \omega_n=\sqrt{M_n^2+P^2},\qquad \mathbf r_n'=2h_n\times\mathbf r_n.$$

The pure-state Bloch vector has $|\mathbf r_n|=1$. With nonuniform momentum quadrature weights $\Delta K_i$, the positive mode weights are

$$w_{ni}=\frac{b(2-\delta_{n0})\Delta K_i}{4\pi^2}.$$

The lowest Landau level has one spin sector and higher levels have two. This degeneracy is already in $w$ and must not be added again to the occupation, current or energy. A finite fixed canonical momentum grid is part of the finite model. A constant gauge shift must translate the grid and $a$ together, preserving $P$; shifting $a$ alone compares different truncated states.

Define the instantaneous-vacuum-subtracted finite sums

$$J_0=\sum w\left(r_z+\frac P\omega\right),\qquad U_0=\sum w(h\cdot\mathbf r+\omega).$$

Their exact finite-system identity is

$$U_0'=\mathcal E J_0.$$

It follows from $h'=\mathcal E\hat z$ and $h\cdot(h\times\mathbf r)=0$. It does not require slow electric variation. The terms involving $r_z$ contain coherence; replacing them by an occupation-only ansatz changes the identity.

### Shared ultraviolet subtraction and finite magnetic matching

The second derivative-order terms from the Bloch expansion are

$$u_2=\frac{M^2\mathcal E^2}{8\omega^5},\qquad j_2=\frac{M^2\mathcal E'}{4\omega^5}-\frac{5M^2P\mathcal E^2}{8\omega^7}.$$

They obey $u_2'=\mathcal E j_2$ mode by mode. A subtraction that changes only one of these two observables breaks the shared work identity. Conversely, subtracting all of $j_2$ without matching back the finite magnetic response erases the physical low-frequency susceptibility. The required spinor one-loop susceptibility is

$$\chi_b=\frac{e^2}{12\pi^2}\left[b-\ln(2b)-\psi\left(1+\frac1{2b}\right)\right].$$

Here $\psi$ is the digamma function. This coefficient is exact in $b$ at the stated one-loop, weak-probe, zero-frequency order; it is not an arbitrary-frequency constitutive law. In the mode calculation, frequency dependence and nonlinear electric response remain in the evolved states.

Set

$$C=\sum w\frac{M^2}{4\omega^5},\qquad S=\sum w\frac{5M^2P}{8\omega^7},\qquad C'=-2S\mathcal E.$$

The matched finite current, matter-energy bookkeeping and Maxwell equation are

$$J=J_0-C\mathcal E'+S\mathcal E^2+\frac{\chi_b}{e^2}\mathcal E',$$

$$U_{\rm matter}=U_0-\frac C2\mathcal E^2+\frac{\chi_b}{2e^2}\mathcal E^2,$$

$$D\mathcal E'=-e^2(J_0+S\mathcal E^2)-I_{\rm ext},\qquad D=1+\chi_b-e^2C.$$

The external source is normalized by $I_{\rm ext}=e j_{\rm ext}/m^3$. The Maxwell sign is fixed by the bare-vacuum control: with matter absent, $\mathcal E'=-I_{\rm ext}$. A compact smooth source $I_{\rm ext}=-\mathcal E_{\rm drive}'$ would reproduce the target pulse in that control. It generally does not reproduce it after quantum feedback is enabled.

The total field-plus-matter energy satisfies

$$U=U_0+\frac{D\mathcal E^2}{2e^2},\qquad U'=-\frac{\mathcal E I_{\rm ext}}{e^2}.$$

This is an exact identity of the stated finite-regulator equations. The constant magnetic field energy does not change in this homogeneous flat-background problem. It would contribute to a gravitational stress tensor and cannot then simply be discarded. A small numerical energy residual verifies one identity of the model; it does not establish regulator independence or covariance.

### Why adding back the susceptibility is not double counting

For an infinite longitudinal integration,

$$\int_{-\infty}^{\infty}\frac{M^2\,dP}{4(P^2+M^2)^{5/2}}=\frac1{3M^2},\qquad \int_{-\infty}^{\infty}\frac{5M^2P\,dP}{8(P^2+M^2)^{7/2}}=0.$$

For Landau levels through $N$, writing $q=1/(2b)$ gives

$$C_B(N)=\frac{b+\psi(N+1+q)-\psi(1+q)}{12\pi^2}.$$

Subtract the corresponding zero-magnetic-field transverse cutoff term

$$C_0(N)=\frac{\ln(1+2bN)}{12\pi^2}.$$

Then $e^2[C_B(N)-C_0(N)]\to\chi_b$. Thus the finite-$b$ restoration is tied to ordinary zero-field charge matching in the completed integrals. It does not add a second copy of an unsubtracted polarization. At finite canonical momentum and Landau cutoffs, the two prescriptions differ by cutoff terms. Those differences are a numerical research question and must be measured, not omitted from the uncertainty budget. `advisor_checks.py` checks this matching limit at three field values and five Landau cutoffs.

## Initial data and admissible interpretation

Initialize at a time before the source turns on with $\mathcal E=0$, constant $a$ and $\mathbf r=-h/\omega$. Choose a compact smooth drive whose derivatives vanish at its support endpoints. This makes the initial vacuum stationary for every retained mode and avoids falsely attributing a sudden initial-state ultraviolet disturbance to pair production. An instantaneous vacuum initialized at nonzero electric field is a different finite problem and needs its own ultraviolet analysis.

The finite system is a well-defined causal semiclassical electromagnetic model. Calling its results a numerical approximation to the on-shell-renormalized continuum requires joint convergence in longitudinal range, Landau range and quadrature, with the drive and state fixed in physical units. Strong magnetic field alone does not justify omitting higher Landau modes during a short source pulse. A clean particle density after an external pulse is also different from instantaneous adiabatic occupation during an autonomous plasma oscillation.

Monitor $D$ throughout. Require a positive lower bound well separated from zero for the tested regulator and coupling. A near-zero denominator is a charge-counterterm/regulator failure or a Landau-pole warning, not evidence of a new physical instability. Taking a formal QED ultraviolet cutoff beyond its perturbative domain is not required to demonstrate useful low-energy numerical convergence.

## Regulator comparison and advisor down-selection

| Scheme | What it can establish this round | Failure mode or missing gate | Decision |
|---|---|---|---|
| Finite instantaneous-vacuum subtraction | Exact finite current/work identity and actual induced-field dynamics | Logarithmic continuum sensitivity; no physical charge matching | Retain as a deliberately unmatched control |
| Shared derivative subtraction plus $\chi_b$ restoration | Finite closed ODEs, matched low-frequency magnetic response, meaningful cutoff tests | Finite-cutoff completion and initial-state sensitivity; no covariant stress yet | Main executable target |
| Constant zero-field charge counterterm | Direct regulator-matched charge interpretation | Canonical-window artifacts and large cancelling terms | Independent limit/comparison where feasible |
| Pauli–Villars fields | Gauge-compatible continuum regulator can compare a different representation | Signed heavy-field cancellations, stiffness, regulator-state matching and finite charge condition | Derive and plan; do not label unexecuted regulator removal validated |
| Full covariant adiabatic/Hadamard stress in anisotropic curved space | Potential shared current/stress closure for gravity | Higher-order stress subtraction, finite gravitational couplings and constraints | Next required gravitational dependency |
| PINN fitted to field/current traces | Surrogate after a trusted solution exists | Can fit the wrong closure or hide residual imbalance | Not the primary verifier |

For Pauli–Villars, regulator moments must match the observable. A signed mass family that cancels the current's divergences need not cancel every stress divergence. One illustrative four-mass family $M_j^2=m^2+j\Lambda^2$, $c_j=(1,-3,3,-1)$ satisfies $\sum c_jM_j^{2q}=0$ for $q=0,1,2$. This algebraic condition is not a complete renormalization prescription: states, finite charge/gravity conditions and regulator limits remain necessary. The negative regulator weights are subtractions and must never be interpreted as negative probabilities of physical particles.

## Falsifiers and release gates

1. **The source actually closes the loop.** Compare the induced-field solution with the prescribed bare-vacuum pulse; report a physical observable that changes by more than numerical and cutoff uncertainty. Continue after the source has ended, so the field is driven by the computed quantum current.
2. **The energy sign is correct.** Integrate source work independently and compare it with $U(s)-U(s_0)$. Report signed residuals and scale them by the supplied energy. Repeat a source-free interval separately.
3. **State geometry is preserved.** Record raw maximum $||\mathbf r||-1$ or Gram residual and occupation violations before any clipping. Norm preservation alone does not prove trajectory accuracy.
4. **Finite magnetic response is retained once.** A small, slowly varying drive must recover $1+\chi_b$. The unmatched and fully subtracted-without-restoration controls should expose the corresponding discrepancy.
5. **Momentum integration is gauge covariant.** Translate the canonical window with a constant gauge shift and compare invariant fields and energies. Recentring the window during time evolution changes the system unless the associated flux terms are included.
6. **The physical cutoff error is measured separately.** Refine momentum quadrature at fixed bounds, then longitudinal bounds, then Landau levels. Record all changes in field, current and energy. Do not interpret a single plateau in one observable as convergence of the whole history.
7. **The initial state is not a numerical switch artifact.** Compare earlier start times or a drive with exactly vanishing endpoint derivatives while preserving the physical pulse. A different ramp is a different experiment and cannot be called an error estimate unless that change is quantified.
8. **Independent derivation reaches the same observable.** Use Bloch versus spinor, or a unitary stepping scheme versus adaptive ODE, and compare both with an analytic or linear-response limit where available. The allowed error is set before examining the comparison.

## Gravity remains a coupled dependency, not an optional label

A uniform $E\parallel B$ stress has unequal longitudinal and transverse pressures. A self-consistent homogeneous geometry is therefore generically axisymmetric Bianchi-I, not isotropic FLRW unless additional stress cancels the anisotropy. Matter energy alone does not determine those pressures. The electromagnetic energy/work identity is necessary but insufficient for the four-dimensional stress Ward identity and Einstein-constraint propagation.

The gravity reviewer must independently supply the compatible metric, orthonormal stress convention, Maxwell dilution terms and Einstein constraint. The next numerical stage must obtain current, energy density and both pressures from a common covariant regulated state and action. A scalar Ricci diagnostic does not replace the curvature tensor, and a small gravitational loop scale does not guarantee small stress fluctuations. Those are separate validity tests.

## What can actually be completed and verified now

The advisor authorizes execution of the finite matched Maxwell–Dirac system, its energy/work identity, source-off field feedback, gauge-window test, cutoff scans and independent solver comparison. The previous expansion-only case can additionally be validated against its exact analytic Sauter reduction. These are genuinely new computational steps beyond prescribed-background occupation calculations.

The advisor does not authorize describing these results as a solved self-consistent curved Einstein–QED problem, an all-frequency/all-loop QED solution, a proof of weak gravity or Festina Lente, a resolved Cauchy-horizon endpoint, or a verified anomalous gravitational force. Those require different observables and additional equations. The purpose of the panel is to turn each missing dependency into a falsifiable next experiment, not to retire it or replace it with a convenient benchmark.

## Final review of the executed causal calculation

The first production run actually closes the electric-field loop. Its prescribed quantity is an external current supported on $0<s<4$, normalized to leave $x=1$ in the absence of quantum matter. The actual initial field is zero. The run uses $b=10$, Landau levels $0\ldots8$, 256 Gauss–Legendre momentum nodes per level on $[-40,40]$, and $0\le s\le50$. It is therefore a specific 2304-mode approximation, not an implicitly unregulated continuum.

On this grid the electric field reaches approximately $0.98949$, is approximately $0.98791$ when the external source ends, and subsequently falls through zero to approximately $-0.03743$ at $s=50$. The source is exactly zero throughout the recorded post-pump interval. The retained quantum current is consequently responsible for the later evolution. This is a new causal electromagnetic calculation beyond the earlier prescribed-field results.

The recorded work is $W_{\rm drive}\simeq0.49780688$ in the code's $e^2\rho/m^4$ normalization. The maximum absolute energy/work residual is approximately $8.79\times10^{-12}$, or $1.77\times10^{-11}$ relative to that supplied energy. The initial diagnostics incorrectly called an error divided by $\max(1,|W|)$ a relative energy error; the implementation reviewer identified this and required a truthful normalization. The sampled maximum squared-Bloch-norm residual is approximately $3.14\times10^{-8}$. The minimum $Z$ is approximately $0.99602$. A constant gauge/grid translation changes the sampled field by approximately $8.48\times10^{-13}$. These checks support correct finite-system evolution; they do not assign a continuum error bar to the quoted late-time field.

### A convergence failure that changes acceptance

The advisor rejected treating the initial scan as successful momentum convergence. Even at $s=20$, the final fields at 128, 256 and 512 nodes are approximately $0.72844247$, $0.72817454$ and $0.72847889$. The difference between 256 and 512 nodes is $3.04\times10^{-4}$ at the endpoint and $3.33\times10^{-4}$ over the sampled history. It is much larger than the integration-tolerance or energy residual. This is precisely the kind of logical mistake the new protocol must prevent: conservation of an accurately solved quadrature approximation does not establish accuracy of the quadrature itself.

The old window scan also held the node count fixed while changing the interval. It therefore changed momentum resolution and the ultraviolet cutoff simultaneously. It is a useful stress test, but cannot isolate the physical cutoff contribution. The advisor requested a targeted resolved-grid sequence through the actual $s=50$ production interval, followed by a larger window at maintained resolution and a Landau-level comparison. Those later results must determine the release precision. The original eleven displayed digits of $x(50)$ are finite-grid output, not eleven validated physical digits.

The requested long-interval follow-up was then executed and inspected. All rows below use the same $b=10$ and pump, evolve through $s=50$, and retain the common subtraction.

| Long-interval test | Observed result |
|---|---:|
| $K_{\max}=40$, $n_{\max}=8$, 1024 nodes: $x(50)$ | $-0.0375827954464$ |
| Same bounds, 2048 nodes: $x(50)$ | $-0.0375716457510$ |
| Same bounds, 4096 nodes: $x(50)$ | $-0.0375716424940$ |
| Maximum sampled field-history change, 2048 to 4096 nodes | $3.26\times10^{-9}$ |
| Maximum matched-current-history change, 2048 to 4096 nodes | $1.13\times10^{-6}$ |
| Endpoint change, $K_{\max}=40$ with 2048 nodes to $K_{\max}=60$ with 3072 nodes | $4.11\times10^{-11}$ |
| Endpoint change, $n_{\max}=8$ to 12 at $K_{\max}=40$ with 2048 nodes | $5.06\times10^{-8}$ |

The large 1024-to-2048 change required the 4096-point calculation: enlarging the interval while preserving essentially the same resolution could otherwise share the unresolved quadrature error. The final comparison resolves that particular risk for the field history. The largest recorded endpoint change among the last component tests is the Landau truncation change. These are measured finite sequences, not mathematical tail bounds or a proof that every renormalized observable has converged. They support reporting the late-time field approximately as $x(50)=-0.03757$ for this matched mean-field experiment, and support its post-source sign reversal.

The refined runs record 251 time samples, compared with 501 in the first run. Their reported maximum field around $0.98931$ is a **sampled** maximum and misses the earlier sample near the true peak around $0.98949$; it is not evidence that momentum refinement substantially changed the peak. Current convergence must use the matched physical current inferred from the complete Maxwell right-hand side. The raw quantity $J_0$ alone changes with the subtraction/window and is not that observable.

### Weak-response and non-mean-field comparators

At $b=100$, a slow weak drive with bare-vacuum target $0.01$ gives a recorded matched late-field average approximately $0.0093130106$, compared with the static linear prediction $0.01/(1+\chi_b)\simeq0.0093130200$. The difference is approximately $9.33\times10^{-9}$. This is useful evidence that the intended finite magnetic response survives once after subtraction. It remains a finite-duration, finite-grid test; the late-time averaging window and residual oscillations must be reported. The deliberate fully subtracted/no-restoration control is the test of erasing that response. A negative-restoration control is a further deliberately wrong model, not the definition of the ordinary no-restoration control.

The separate bosonized one-dimensional comparison is accepted as a check on the first-order effective equation derived from that quantum theory. Fifteen parameter cases compare the oscillation period from an ODE with an independent energy quadrature; their largest reported difference is approximately $1.21\times10^{-11}$. The first-order truncation remainders scale with orders approximately $1.985$, $2.007$ and $2.001$ in the three amplitude sequences. This provides a useful example of a quantum correction omitted by a mean-field treatment, while retaining the source's dimensional and perturbative limitations. Solving the truncated equation accurately does not turn its higher numerical powers into derived higher-order QED predictions. The comparison does not supply an error bar for the three-dimensional massive Landau calculation.

### Disposition of the four original research fronts

| Original front | Accepted contribution from this round | What is still required before a conclusion about the open problem |
|---|---|---|
| Festina Lente and weak gravity | Clear separation of matter-induced discharge, imposed support and spectrum conjectures; causal-current methods are available for a future geometry-matched test | Charged de Sitter horizons, the chosen quantum state, physical charge normalization, scalar forces and actual decay channels; flat homogeneous pumping does not test either conjecture |
| Magnetized curved Schwinger backreaction | A matched, causal electromagnetic mode/current system and a finite-regulator energy identity; exact audit of the earlier external curved benchmark | Anisotropic curved current, energy and both pressures with common covariant subtractions, then metric feedback at the target curvature |
| Mass inflation and quantum evaporation | Explicit rejection of energy-only stress closure and a separately tested Einstein-constraint methodology | Null fluxes, horizon state/boundary data, dilaton/backscatter structure and a renormalized stress on the charged black-hole geometry; a homogeneous plasma oscillator cannot determine the Cauchy-horizon endpoint |
| Photon–graviton mixing | A checked magnetic susceptibility and a retarded finite-frequency electromagnetic comparator | Momentum-dependent polarization, both polarizations, the matched mixed photon–graviton kernel and geometry-dependent propagation; the homogeneous scalar response alone is not a conversion probability |

The source review's source-free de Sitter vector model and this pumped Maxwell system use different support assumptions. A mass or source requirement proved in one ansatz is not universally necessary for a field maintained by an external current. This is an example of comparing the full equation and support conditions before promoting a criticism into a general no-go result.

### Next decision

The mathematical and implementation acceptance is **a causal matched finite-regulator mean-field calculation**, with independently checked limits and the targeted long-interval momentum, window and Landau comparisons above. The field reversal and approximate late-time field are accepted; unqualified continuum convergence, eleven-digit physical precision and convergence of the entire stress tensor are not. Full quantum electromagnetic fluctuations, collisions, anisotropic covariant stress and metric feedback remain unresolved dependencies. The next physical advance should compute the compatible anisotropic current and pressures from a common state and subtraction prescription and test the Einstein constraint, with a quantum linear-response or fluctuation comparator. It should not add the present energy curve to a prescribed metric and call the combination self-consistent.
