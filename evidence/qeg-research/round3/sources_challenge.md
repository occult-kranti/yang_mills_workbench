# Empirical and source challenge: third research cycle

## What this pass actually adds

This pass reopens omitted mechanisms and tests the sources themselves. It does not infer that a government programme, patent, impressive sensitivity number, or agreement among simulated models establishes the proposed physics. Six concrete additions change the research plan: a 2026 disagreement over the support and renormalization of constant electric fields in de Sitter; an invalid action argument inside an electrostatic-force patent; an incorrect graviton–fermion selection rule in another patent; a detector-noise bookkeeping problem in a released government report; a recent multi-detector rejection of apparently interesting transients; and a spin-polarization experiment whose apparent displacement arose from its optical readout environment.

The international search adds Canada, South Korea and Brazil and deepens Australia, Italy, Germany and the United States. These are targeted searches, recorded in `search_coverage.json`. They are not an inventory of every country's projects. Historical source documents, current research activity, simulations and measurements have separate statuses. No inaccessible or classified record is treated as read.

## A new challenge to the negative-current narrative

Bastero-Gil and colleagues' April 2026 revision studies a dynamical, homogeneous vector field in de Sitter and chooses a tachyonic mass, $m_A^2=-2H^2$, to sustain its constant electric background. Their finite subtraction uses flat-space vacuum polarization evaluated at $p^2=2H^2$ and yields a positive, finite current in regimes previously associated with negative infrared divergence. They explicitly leave stress evolution and realistic electromagnetic generation outside their calculation. Sections 2.1–2.4, rather than the headline, define the comparison. [@E01]

The following is our independent consistency check. With physical electric field and physical current defined in the usual cosmological Ampere convention, homogeneous Maxwell evolution is

$$\dot E+2HE=-j_{\rm matter}-j_{\rm pump}.$$

Multiplication by $E$ yields the energy budget

$$\dot\rho_E+4H\rho_E=-E(j_{\rm matter}+j_{\rm pump}),\qquad \rho_E=E^2/2.$$

An externally maintained constant field is therefore possible in ordinary Maxwell theory when the pump supplies the dilution and matter-work losses. A source-free Maxwell field instead redshifts as $a^{-2}$. The statement that constant physical $E$ universally demands a tachyonic photon mass is too broad: it demands support, and the support model must be specified. Comparing a pumped massless theory with a source-free modified vector theory is not a clean renormalization-only comparison. Neither calculation supplies the current of our finite pulse merely by substituting its instantaneous field.

Hayashinaka and Xue's original maximal-subtraction proposal makes a different choice: remove the inverse-mass terms so the heavy-particle current decays exponentially. Its Eqs. 12–15 show how the finite subtraction changes the conductivity, and Eq. 7 keeps the product of renormalized charge and gauge potential invariant. This is a physical prescription that must be examined, not a theorem that any term without a Schwinger exponential is erroneous. [@E02]

Our falsifiable test is to compare the **same** pumped background, quantum state, measured charge and stress/current counterterms under two admissible descriptions. Move a local polarization contribution between the field equation and the source consistently. A claimed physical amplification must persist in the total field evolution and work balance. A sign change in one named piece is insufficient. Re-entry requirements are a finite renormalization map, Ward identity, matched pump stress and an evolved field; this source review does not claim to have run that continuum calculation.

## Government and international comparators with explicit status

| Jurisdiction and record | Established status and measurement | Exact use in this project |
|---|---|---|
| Canada: TRIUMF, ALPHA/HAICU | The May 2026 laboratory article reports antimatter spectroscopy and describes HAICU as infrastructure being developed. The existing ALPHA gravitational result is distinct from the future hydrogen quantum-sensing programme. [@E04] | Magnetic-trap force gradients and state preparation must enter the gravitational observable. A new initiative is not a completed interference test. |
| South Korea: IBS CoReLS | The laboratory's May 2021 report documents the demonstrated laser-intensity milestone and describes focusing and beam diagnostics. It is a historical performance result, not a current world-record assertion. [@E05] | Use measured pulse geometry and fluctuations when predicting strong-field processes; peak intensity alone does not specify electric-like invariants. |
| Australia: MAGE at UWA | A 2025 report analyzes 61 days of data with two quartz detectors and uses coincidence selection to reject predecessor-like rare transients as gravitational candidates. [@E03] | Test a proposed signal in an independent sensor and calibrate coincidence efficiency. Narrowband strain sensitivity is not an unexplained-event detection. |
| Brazil and international partners: BINGO | The 2026 collaboration analysis is a forecast using simulated HI maps and Planck likelihoods. Its acknowledgements identify Brazilian public funding and national supercomputing resources. It omits some correlated noise and beam/leakage complexities. [@E06] | A cosmological inference comparator, not a strong-field laboratory. Repeat forecasts under omitted nuisance models before translating precision into evidence for new gravity. |
| Italy: INFN/CNR Archimedes | The 2024 prototype paper reports torque noise near $7\times10^{-13}\,\mathrm{N\,m}/\sqrt{\mathrm{Hz}}$ around 60 mHz. The final vacuum-weight target is a future sensitivity requirement, not the reported signal. [@E07] | Model the weight of the complete energy-changing apparatus, thermal and seismic transfer functions, and superconducting-state changes. |
| Germany: IFW Dresden/TU Dresden NMR test | The original 2024 experiment compares spin-polarized samples and control configurations. Its sensitivity differs by material and polarized mass fraction. [@E13] | Do not convert a best resolution from one sample into a universal exclusion for every material or DNP mechanism. |
| United States: NASA BPP | Official indexed records identify the historical programme and memoranda. Direct full retrieval failed again in this pass. [@E16] | Retain as an access gap and historical lead; do not claim detailed source adjudication from the unread memorandum. |
| United States: DIA released HFGW reference document | A dated 2010 report is directly available in DIA's public reading room, with author identity redacted in this copy. It discusses projected concepts and calculations. [@E09] | Its equations and assumptions can be tested. Release by an agency does not transform forecasts into measured performance. |

The source map deliberately excludes generic quantum-computing announcements that would inflate geographic coverage without changing a QED–gravity test. It also avoids claiming that conventional laboratory fields realize $R/m_e^2\sim1$. No newly inspected facility demonstrates the complete strongly curved Einstein–QED feedback problem.

## Two patents whose equations can be challenged directly

### Electrostatic propulsion: the invalid inference appears before the force calculation

The Aurigema–Buhler patent US11511891B2, in “Theory of Operation,” Eqs. 1–5, replaces stationarity of the action with an ordinary differential condition on an energy–time product, obtaining $d(Ut)=0$ and $Udt=-t\,dU$. Later paragraphs treat Coulomb attraction and electrostatic pressure as separate contributions. These are substantive claims to test, not merely unusual terminology. [@E15]

Our counterexample requires no disputed new physics. Take

$$L=\tfrac12 m\dot x^2-U_0,\qquad x(t)=vt+x_0,$$

with a nonzero constant potential offset $U_0$ and fixed endpoint variations. Euler–Lagrange gives $m\ddot x=0$, so the trajectory has stationary action. Nevertheless,

$$\frac{d(U_0t)}{dt}=U_0\ne0.$$

Thus $\delta\int Ldt=0$ does not imply $d(Ut)=0$. Adding an arbitrary constant to a potential cannot change forces, whereas the disputed inference is sensitive to that constant. The proposed derivation therefore fails before its geometry optimization. This does not by itself diagnose every reported instrument signal; that requires data and a complete apparatus model.

An independent whole-system identity is

$$\mathbf F_{\rm matter}=\oint_{\partial V}\mathbf T_{\rm EM}\cdot\mathbf n\,dS-\frac{d}{dt}\int_V\epsilon_0\mathbf E\times\mathbf B\,dV,$$

$$T_{ij}=\epsilon_0(E_iE_j-\tfrac12\delta_{ij}E^2)+\mu_0^{-1}(B_iB_j-\tfrac12\delta_{ij}B^2).$$

For an isolated, localized, electrostatic charge distribution and a boundary taken to infinity, field momentum is static and the surface integral vanishes. The result includes the total matter, bound charges and supports. Integrating selected electrode faces can produce a force on those faces while missing its reaction elsewhere. In matter, use a vacuum bounding surface around the apparatus to avoid confusing alternative macroscopic stress conventions.

The corresponding discrete counterexample is exact: for any finite collection of separated charges, the internal Coulomb force obeys $\sum_i\sum_{j\ne i}\mathbf F_{ij}=0$ because $\mathbf F_{ij}=-\mathbf F_{ji}$. Asymmetric charge geometry does not change the pair cancellation. A finite-element extension should integrate the same closed surface at multiple radii, include the supply and shield, and compare against all volume forces. A nonzero residual that moves with the integration boundary is a diagnostic of missing terms or discretization, not thrust.

### Graviton spin does not prohibit coupling to an electron

The Pais patent US10322827B2 claims, in its discussion following Eq. 4, that spin-two gravitons do not couple to spin-one-half electrons. It also assumes extraordinary source fields in its conversion estimates; those values are premises rather than reported measurements. [@E08]

Our direct field-theory test starts with the generally covariant Dirac action. Variation with respect to the metric gives the symmetric matter stress, with on-shell form

$$T_D^{\mu\nu}=\frac{i}{4}\bar\psi\left(\gamma^\mu\overleftrightarrow{D}^{\nu}+\gamma^\nu\overleftrightarrow{D}^{\mu}\right)\psi.$$

The linear metric perturbation couples to this tensor through $\delta S_D=\tfrac12\int\sqrt{-g}\,T_D^{\mu\nu}\delta g_{\mu\nu}\,d^4x$ under that stress convention. It is nonzero for an electron state carrying energy and momentum. Different particle spins do not remove this interaction. Weak coupling or kinematic restrictions for a particular process must not be replaced by a universal spin prohibition. This counterexample invalidates that inference, without adjudicating every patent claim.

## A government report can double-count measurement resources

The DIA HFGW document's Section 2.2.3 first estimates an “effective stored” RF energy from power times a 1000-second observation times a cavity factor. It then incorporates temporal and spatial selectivity factors in another effective quality factor. Its later communication example explicitly chooses a hypothetical bandwidth and noise floor. These numbers require a detector transfer-function derivation before they can be used as sensitivity. [@E09]

Our dimensional and dynamical comparator is the actual cavity balance,

$$\dot U=P_{\rm in}-\kappa U,\qquad \kappa=\omega/Q_{\rm cav},\qquad U_{\rm ss}=P_{\rm in}Q_{\rm cav}/\omega.$$

Here $P_{\rm in}$ is the power deposited in the mode; coupling and reflection must be included when converting a generator rating into that quantity. For fixed deposited power, observing longer does not cause the steady stored energy to grow indefinitely. Integration time improves an estimator through its noise bandwidth and number of independent data, not by repeatedly counting the same intracavity energy. For a given physical apparatus, replace verbal “quality factors” by an input–output transfer matrix, loss channels and noise covariance. Separate loaded cavity $Q$, observation duration, angular response and collection efficiency.

The actual opposing view was read. GravWave's author-side response argues that the Li–Baker synchro-resonant Gaussian-beam geometry differs from bare Gertsenshtein conversion and that transverse detection rejects background. This geometry objection deserves a matched calculation; it is not answered by citing a critic's status. [@E11] The JASON archive records a contrary assessment, but the complete linked report could not be retrieved here. We therefore do not claim to have independently checked its detailed equations. [@E10]

Here is our small independent detector benchmark. For an ideal lossless balanced mixer with coherent signal and local oscillator, measured photon counts are Poisson with

$$\bar N_\pm=\tfrac12(N_{\rm LO}+N_s)\pm\sqrt{N_{\rm LO}N_s}\cos\phi.$$

For difference $D=N_+-N_-$,

$$\langle D\rangle=2\sqrt{N_{\rm LO}N_s}\cos\phi,\qquad \operatorname{Var}D=N_{\rm LO}+N_s.$$

At fixed signal and optimal phase, increasing $N_{\rm LO}$ gives $\mathrm{SNR}\to2\sqrt{N_s}$, rather than unbounded noiseless gain. This is an explicitly defined benchmark, not a full proof about an arbitrary Li–Baker geometry. A proposed background-free output requires its own mode-overlap, loss and detector covariance calculation. Squeezing or active media changes the quantum state and resource accounting; it cannot be silently inserted into the coherent benchmark.

## A critic's negative control and an actual replication are different evidence

Prutchi's 2019 author-hosted critique identifies a reported magnet-off control that undermines attribution of an apparent weight change to resonance-dependent spin ordering. He also identifies missing simultaneous recording of microwave timing. His diagrams partly reconstruct the apparatus from a book; this is a documentary critique, not his own complete replication. [@E12]

Stark, Grafe and Tajmar then supplied an actual NMR investigation. Its material-dependent sensitivity table matters: some metallic samples have too little polarized mass relative to noise to support exclusion. Apparent shifts at higher pulse loading also occur without a specimen and track heating-induced refractive-index changes in the interferometer path. This is a specific instrumental account, not an argument that every conceivable spin-dependent force is impossible. [@E13]

The alternative-propulsion community's 2026 event page still presents spin ordering as a test target and explicitly distinguishes DNP's established spectroscopic role from gravitational control. It is a current participant-community lead, not an independently validated force law. [@E14]

The improved experiment must measure spin polarization and force simultaneously. Use independent sensing principles, randomized resonant/off-resonant settings with matched deposited heat, blank specimens and optical-path monitoring. A resonance in the force channel alone is ambiguous: resonant absorption itself changes thermal power. Fit the alternative amplitude to a separately measured spin observable rather than to the microwave command.

## Executed source-criticism checks

`empirical_logic_checks.py` was executed and wrote `empirical_logic_results.json`. Four check groups passed: the fixed-endpoint action variation vanishes while $d(U_0t)/dt=-9$ for a constant-potential example that also satisfies the patent’s assumed zero total energy; energy differentiation and direct Coulomb summation independently give forces $(-5/3,7/2,-11/6)$ with zero total; a dimensionless lossy-cavity integration agrees with its analytic energy law to $5.20\times10^{-13}$; and 200,000 simulated coherent-detector trials at each of seven local-oscillator settings reproduce the predicted count mean and variance within the declared six-standard-error threshold. At fixed two signal photons, the analytic SNR approaches $2\sqrt2$ rather than increasing without bound. These are mathematical and simulated measurement checks. The full apparatus reconstructions, continuum-current comparison and hardware experiments below remain proposed.

## New hypothesis and experiment ledger

These are proposed discriminating experiments and calculations. None is presented as hardware work executed by this source-review agent.

| ID | Hypothesis | Distinguishing observation or calculation | Nuisance model and failure criterion |
|---|---|---|---|
| E-X01 | Negative current represents observable field amplification. | Compare two matched finite-renormalization descriptions of one pumped background and the total evolved $E(t)$. | Unmatched charge, local polarization and pump work. Fail if amplification changes only when bookkeeping changes. |
| E-X02 | Constant de Sitter $E$ universally forces a photon mass change. | Integrate ordinary Maxwell with a prescribed compensating current and its power budget. | External support is explicitly included. Counterexample succeeds if constant $E$ and energy balance coexist with massless Maxwell. |
| E-X03 | Stationary action requires $d(Ut)=0$. | Free-particle/constant-potential analytic counterexample; repeat after changing the potential zero. | No statistical uncertainty needed. Failure is mathematical and occurs before numerical optimization. |
| E-X04 | Electrode asymmetry produces isolated steady thrust. | Closed-surface stress, pair-force cancellation and a source-inclusive finite-element model. | Bound charges, supports, grounded enclosure, lead forces and radiation. Fail if a force disappears when the whole system is counted. |
| E-X05 | Graviton–electron coupling vanishes because spins differ. | Vary Dirac action and evaluate its stress between nonzero-energy electron states. | Distinguish nonzero coupling from a kinematically forbidden special process. The universal claim fails if the stress vertex is nonzero. |
| E-X06 | A local oscillator amplifies conversion without added quantum noise. | Poisson balanced-detector benchmark, then a full proposed-mode transfer model. | LO fluctuations, vacuum ports, losses and detector dark counts. Fail if signal growth is accompanied by the omitted variance. |
| E-X07 | Longer observation increases stored cavity energy. | Solve the driven lossy cavity and compare energy with estimator SNR as duration changes. | Ring-up time and finite bandwidth. Fail if stored energy saturates while the proposed formula grows with observation time. |
| E-X08 | Spin ordering changes weight beyond ordinary forces. | Simultaneous polarization, interferometric and independent force measurements under blinded settings. | Heat-matched detuning, magnetic gradients, sample-free optical paths. Reject a claimed mechanism if its spin dependence is absent under adequate sensitivity. |
| E-X09 | Rare narrowband transients are gravitational. | Two-detector coherent injection and coincidence analysis with declared timing/antenna response. | Local crystal events, RF pickup and correlated environmental disturbances. Lack of coincidence is informative only above both instruments' detection efficiency. |
| E-X10 | A vacuum-weight signal identifies the absolute cosmological vacuum energy. | Model and modulate a specified finite apparatus energy difference including supports. | Condensation energy, heat flow, thermal expansion, magnetic force and seismic tilt. A measured energy difference does not identify the absolute cosmological constant. |
| E-X11 | A facility's peak intensity fixes the pair-production signal. | Sample measured vector pulse shapes and compute field invariants and spectra. | Spatiotemporal coupling, incoming particles, focal averaging. Fail if indistinguishable peak intensity produces different process predictions. |
| E-X12 | Simulated cosmological precision is insensitive to omitted systematics. | Add correlated noise, frequency-dependent beams and polarization leakage to held-out forecasts. | Foreground complexity and fitting flexibility. Fail if nominal intervals lose their injection-calibrated coverage. |

The new priority is not a wider unstructured bibliography. It is a source-to-equation challenge record: state the premise, build an admissible counterexample, identify what the measured observable is, and prevent the counterexample from silently becoming another substitute for the full coupled problem.
