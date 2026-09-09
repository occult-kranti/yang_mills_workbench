# A typed map of the research problem

This is a targeted map of 44 nodes, not an exhaustive inventory of physics. It separates physical framework choices, measured premises, mathematical theorems, numerical evidence and unresolved problems. The selected target is **M09: global-forward existence of the frozen finite Maxwell–Dirac system**. Its useful observable consequence is **M08: an all-time field envelope for an integrable drive**. Neither result proves the surrounding conjectures.

A backward search asks which jointly sufficient premises would prove a target. A forward search derives consequences from accepted premises. Their meeting is meaningful only when the entire premise set is satisfied. Adjacency, citation, similarity and agent agreement are insufficient.

## Foundations

| ID | Node and evidence type | Statement | Sources |
|---|---|---|---|
| F01 | **Classical implication and proof search** — method framework; adopted | Backward theorem application opens all missing premises; it never reverses an implication. | [S01], [S02], [S04], [S05] |
| F02 | **Real calculus and inner-product identities** — mathematical foundation; established | Chain rules, Cauchy–Schwarz and antisymmetry of the cross product support the finite energy argument. | [TA01], [P:T] |
| F03 | **Local ODE theory and continuation** — mathematical theorem; established | A locally Lipschitz finite ODE has a unique local solution; compact confinement permits continuation. | [TA01] |
| F04 | **Quantum state and unitary-evolution postulates** — framework postulate; assumed framework | Positive density operators and unitary dynamics specify the quantum blocks used in the model. | [P:P3] |
| F05 | **Maxwell–Dirac gauge framework** — framework postulate; assumed framework | An abelian gauge connection coupled to a Dirac field supplies the electromagnetic matter framework. | [P:P3], [R3:FT01] |
| F06 | **Einstein gravitational framework** — framework postulate; assumed framework | The metric obeys Einstein equations with a declared total stress tensor and any specified higher-curvature terms. | [P:P3], [R3:H08] |
| F07 | **Measured constants and frozen parameter choice** — empirical premise; measured and frozen | The solver freezes alpha=1/137.035999084; the proof needs only alpha<1/137. | [TA05], [TA06] |
| F08 | **Bloch-ball positivity** — mathematical theorem; established | The matrix (I+r·sigma)/2 is positive exactly when &#124;r&#124;<=1. | [P:T] |
| F09 | **Positive Gauss–Legendre quadrature** — mathematical theorem; established | Exact Gauss weights are positive and integrate constants exactly. | [TA04] |
| F10 | **Digamma recurrence and Binet positivity** — mathematical theorem; established | For b>0 the matched susceptibility bracket has a positive Binet-integral representation. | [TA02], [TA03], [P:T] |
| F11 | **Newtonian gravitational limit** — framework limit; restricted context | Newtonian gravitational interactions form a separate weak-field context, including current entanglement arguments. | [R3:H14] |

## Finite model and selected theorem

| ID | Node and evidence type | Statement | Sources |
|---|---|---|---|
| M01 | **Finite homogeneous regulator and state** — model assumption; frozen | Use fixed finite positive weights, positive masses and canonical momenta; production has b=10,K=20,n=0..4. | [P:P3], [TA06] |
| M02 | **Matched finite Maxwell–Dirac closure** — model assumption; frozen | The mode equations and shared S,C,D,Z and energy definitions are fixed by T1–T5. | [P:T], [P:P3] |
| M03 | **Admissible drive and parameter families** — model assumption; frozen | Use continuous drives; smooth compact pumps and differentiable source families support the production response. | [P:T], [P:P3] |
| M04 | **All-potential coefficient margin** — mathematical theorem; proved conditionally | For the selected regulator, Z(a)>3/4 for every real a. | [P:T], [TA02], [TA03], [TA04] |
| M05 | **Invariant Bloch norms** — mathematical theorem; proved conditionally | Precession preserves each &#124;r_i&#124;, hence the initial Bloch balls. | [P:T] |
| M06 | **Positive finite excitation energy** — mathematical theorem; proved conditionally | Positive weights and &#124;r_i&#124;<=1 imply U=sum w_i(h_i·r_i+omega_i)>=0. | [P:T] |
| M07 | **Exact shared work balance** — mathematical theorem; proved conditionally | With W=Zx²/2+e²U, the frozen equations give Wdot=xF. | [P:T] |
| M08 | **Electric-field envelope** — mathematical theorem; proved conditionally | &#124;x(t)&#124;<=sqrt(2W0/z*)+&#124;&#124;F&#124;&#124;L1(0,t)/z*; vacuum unit impulse gives &#124;x&#124;<=4/3. | [P:T] |
| M09 | **Selected global-forward theorem** — mathematical theorem; proved conditionally | The selected finite system has a unique classical solution on every finite future interval. | [P:T] |
| M10 | **Finite-time tangent and retarded support** — mathematical theorem; proved conditionally | Differentiable source/state families satisfy the tangent system; unchanged preparation gives zero response before a delayed probe. | [P:T], [P:P3], [R4:R01] |
| M11 | **Independent finite-model numerical checks** — numerical evidence; accepted limited | Round4 independent spinor/finite-difference checks and 512-to1024 momentum refinement support the recorded response implementation. | [TA06], [P:ACCEPT] |
| M12 | **All-time response stability** — open problem; unresolved | Determine whether a declared physical perturbation norm remains uniformly controlled for admissible states. | [P:T], [R4:R01], [R4:R02] |

## Quantum and continuum obligations

| ID | Node and evidence type | Statement | Sources |
|---|---|---|---|
| Q01 | **Hadamard and local-covariance framework** — mathematical framework; established with scope | Local covariant renormalization organizes admissible states and finite current/stress ambiguities. | [R4:R06] |
| Q02 | **Common quantum current and directional stress** — open obligation; unresolved | Derive J,rho,p_perp,p_parallel from one state and common renormalization prescription. | [P:P3], [R4:R06] |
| Q03 | **Full causal current/stress response blocks** — open obligation; partially mapped | Construct retarded JJ,JT,TJ,TT variations with all contact terms from a causal state prescription. | [P:P3], [R4:R01], [R4:R02] |
| Q04 | **Physically smeared quantum noise** — open obligation; unresolved | Compute symmetrized connected current and stress fluctuations with physical smearing. | [R4:R04], [P:P3] |
| Q05 | **Controlled continuum limit** — open obligation; unresolved | Prove regulator-uniform bounds and convergence to a defined renormalized continuum model. | [P:T], [P:CRIT], [R4:R03] |
| Q06 | **Semiclassical validity criterion** — open problem; unresolved for target | Determine where mean-field evolution approximates the intended quantum observables. | [R4:R02], [R4:R04], [R4:R05] |

## Gravitational interface

| ID | Node and evidence type | Statement | Sources |
|---|---|---|---|
| G01 | **Axisymmetric Bianchi-I reduction** — model assumption; candidate reduction | Use ds²=-dt²+a_perp²(dx²+dy²)+a_parallel²dz² with aligned fields and diagonal total stress. | [P:P3], [R3:H01] |
| G02 | **Total Ward defect** — defined observable; defined | Q=rhodot+2H_perp(rho+p_perp)+H_parallel(rho+p_parallel) measures total energy-conservation failure. | [P:BIANCHI], [P:P3] |
| G03 | **Bianchi-I constraint propagation** — conditional lemma; derived conditionally | Spatial Einstein evolution gives Cdot=-theta C-kappa Q; thus Q=0 and C(0)=0 preserve C=0. | [P:BIANCHI] |
| G04 | **Self-consistent quantum Bianchi-I evolution** — open problem; unresolved | Solve the coupled geometry, fields and quantum state with constraint propagation and controlled validity. | [P:P3], [R3:H05], [R3:H08] |

## Four surrounding research fronts

| ID | Node and evidence type | Statement | Sources |
|---|---|---|---|
| O01 | **Electric Weak Gravity Conjecture** — conjecture; open general statement | Conjecture an appropriately superextremal charged state relative to the relevant gravitational extremality relation. | [R3:G01], [R4:R08] |
| O02 | **Magnetic Weak Gravity Conjecture** — conjecture; open general statement | A magnetic/UV-scale version constrains the gauge-theory cutoff relative to gravity. | [R3:G01], [R4:R08] |
| O03 | **Festina Lente criterion** — conjecture; open general statement | Quasi-de Sitter discharge arguments motivate a lower charged-mass bound of schematic form m⁴≳g²q²H²M_Pl². | [R3:G02], [R3:G04], [R4:R08] |
| O04 | **Charged de-Sitter decay compatibility** — open problem; partially mapped | Reconcile discharge, Hawking evaporation, extremality and possible WGC/FL constraints in one causal model. | [R3:G04], [R3:G14], [R4:R08] |
| O05 | **Schwinger pair creation in prescribed fields** — established calculation; known with regime | Vacuum pair production is nonperturbative in an electric field; magnetic fields alter the charged spectrum. | [R3:FT01], [R3:RT06] |
| O06 | **Euler–Heisenberg and curvature expansion** — effective framework; known with regime | One-loop local effective actions encode vacuum polarization only within their field, derivative and curvature assumptions. | [R3:FT02], [R3:FT06], [R3:FT07] |
| O07 | **Magnetized curved Schwinger backreaction** — open problem; unresolved target | Compute causal pair current and stress in a chosen strongly magnetized curved geometry, then evolve backreaction. | [P:P3], [R3:FT06], [R4:R03] |
| O08 | **Classical mass inflation** — conditional result; known with hypotheses | Coupled fluxes can destabilize charged inner horizons and produce mass inflation under specified data and decay assumptions. | [R3:G03] |
| O09 | **Quantum Cauchy-horizon endpoint** — open problem; unresolved target | Determine the backreacted endpoint when quantum stress, evaporation and inner-horizon dynamics interact. | [R3:R227], [R3:H09], [R4:R09] |
| O10 | **Perturbative photon–graviton conversion** — established calculation; known with regime | An external magnetic field couples photon and graviton perturbations; conversion depends on phase matching and polarization. | [R3:G13], [R4:R10] |
| O11 | **Quantum-dispersive conversion in strong fields** — open problem; unresolved target | Determine when QED birefringence, plasma and geometry suppress or permit coherent conversion. | [R3:G13], [R4:R11] |

## The accepted meeting of forward and backward reasoning

Forward: finite admissible blocks imply invariant Bloch balls; positive weights imply nonnegative finite excitation energy; the shared current/energy definitions give exact work balance. The analytic coefficient bound then yields a field envelope. Backward: global existence requires continuation; continuation requires finite-time confinement and an open, nonsingular equation domain. The envelope bounds the field, its integral bounds the potential on each finite interval, the Bloch norms bound the remaining coordinates, and the global denominator estimate prevents degeneracy.

\[ Z(a)>\frac34,\qquad W=\frac12Zx^2+e^2U,\qquad \dot W=xF,\qquad |x(t)|\le\sqrt{\frac{2W_0}{z_*}}+\frac{\|F\|_{L^1(0,t)}}{z_*}. \]

This is a conditional theorem about an exact finite ODE. The proof treats the zero-energy vacuum start without dividing by zero. Pure-state data need not make the potential uniformly bounded for all time by this argument; one strictly mixed block supplies an additional coercive estimate. Source response is retarded and finite on compact intervals, but its signed first-variation work is not a positive stability norm. See [P:T] and [P:CRIT].

## A next conditional lemma, with its missing physical input

For the axisymmetric Bianchi-I metric define \(\theta=2H_\perp+H_\parallel\), \(C=H_\perp^2+2H_\perp H_\parallel-\kappa\rho\), and \(Q=\dot\rho+2H_\perp(\rho+p_\perp)+H_\parallel(\rho+p_\parallel)\). Absorb any constant cosmological term into the total density and pressures, or set it to zero. With the spatial Einstein equations imposed, the root derivation obtains

\[ \dot C=-\theta C-\kappa Q. \]

Thus \(Q=0\) and \(C(0)=0\) preserve the Hamiltonian constraint. The equation does not manufacture \(Q=0\). The total stress must include field, matter and any external/support sector consistently. The quantum current and both directional pressures remain unclosed. Zahn v3 section4.2 imposes a restriction on background gauge curvature in its stress argument; that result cannot simply be cited as the required nonzero-field Ward identity. [P:BIANCHI], [R4:R06].

## How to interpret the connections

| Edge type | Meaning |
|---|---|
| assumption | A target adopts a premise or physical framework. |
| proved hyperedge | Every source node in the conjunction is required, together with stated target assumptions. |
| context | A relation worth studying; no logical implication. |
| restricted analogue | A shared mechanism in a different geometry, state or approximation. |
| unresolved bridge | A derivation, estimate, observable or physical closure is missing. |

The JSON records each node’s assumptions, dependencies, source reading provenance, scope and next obligation, plus explicit typed edges. Only the proved hyperedges may be used as accepted inference rules, and even those must retain all assumptions. The four original fronts require different geometries and observables: no single homogeneous calculation closes them.

## Next obligations in dependency order

1. Preserve the finite theorem and its counterexamples; formalize its statement if kernel checking is desired.
2. Prove regulator-uniform estimates or exhibit a failure; independently control momentum-window and Landau limits.
3. Derive current, energy and directional pressures from one state and subtraction prescription.
4. Establish the nonzero-field force Ward identity and account for supports; use the Bianchi lemma as a discriminating constraint test.
5. Construct causal response and physically smeared fluctuation observables; test semiclassical validity.
6. Return to one original front with its own geometry, quantum state, boundary conditions and approximation regime.

## Source keys

External sources retain the earlier audits’ reading limits; this map is not a claim that every cited paper was newly read in full. Project artifacts document derivations rather than functioning as external authority.

**P:ACCEPT**: Round4 acceptance and sampled numerical scope; `qeg-research/round4/physics_acceptance.json`.

**P:BIANCHI**: Root-derived Bianchi-I constraint propagation lemma; `qeg-research/round5/symbolic_checks.py` and `qeg-research/round5/symbolic_results.json`.

**P:CRIT**: Independent proof critique and falsifiers; `qeg-research/round5/proof_critique.md`.

**P:P3**: Frozen P3 response contract; `qeg-research/round4/response_contract.md`.

**P:T**: Finite-model theorem and advisor review; `qeg-research/round5/theorem_advisor.md`.
[R3:FT01]: https://doi.org/10.1103/PhysRev.82.664 "On Gauge Invariance and Vacuum Polarization"
[R3:FT02]: https://arxiv.org/pdf/1009.1495 "Euler-Heisenberg Lagrangian to all orders in the magnetic field and the Chiral Magnetic Effect"
[R3:FT06]: https://arxiv.org/html/0906.2430v1 "Non-Perturbative One-Loop Effective Action for Electrodynamics in Curved Spacetime"
[R3:FT07]: https://arxiv.org/html/2511.03315v1 "Heat Kernels and Resummations: the Spinor Case"
[R3:G01]: https://arxiv.org/abs/1906.02206 "Repulsive Forces and the Weak Gravity Conjecture"
[R3:G02]: https://arxiv.org/abs/2106.07650 "The FL bound and its phenomenological implications"
[R3:G03]: https://arxiv.org/abs/2506.08075 "Mass inflation from rough initial data"
[R3:G04]: https://arxiv.org/html/2311.13742v2 "Extremal Black Hole Decay in de Sitter Space"
[R3:G13]: https://arxiv.org/abs/2601.23279 "One loop photon-graviton mixing in an electromagnetic field: Part 3"
[R3:G14]: https://arxiv.org/html/2605.20349v1 "The fate of Reissner–Nordström–de Sitter black holes: nonequilibrium discharge and evaporation"
[R3:H01]: https://arxiv.org/abs/1807.00434v4 "Linear perturbations of an anisotropic Bianchi I model with a uniform magnetic field"
[R3:H05]: https://arxiv.org/html/2205.11671v5 "On the initial value problem for semiclassical gravity without and with quantum state collapses"
[R3:H08]: https://arxiv.org/pdf/gr-qc/9211002 "Einstein Equation with Quantum Corrections Reduced to Second Order"
[R3:H09]: https://arxiv.org/html/2411.11948v1 "The Structure of Quantum Singularities on a Cauchy Horizon"
[R3:H14]: https://link.aps.org/pdf/10.1103/fv38-kgkb "Can Newtonian gravity produce quantum entanglement?"
[R3:R227]: https://arxiv.org/abs/1912.06047 "Quantum Instability of the Cauchy Horizon in Reissner-Nordström-deSitter Spacetime"
[R3:RT06]: https://arxiv.org/abs/hep-th/0301132 "Schwinger Pair Production in Electric and Magnetic Fields"
[R4:R01]: https://arxiv.org/html/2410.22633v2 "Linear Response Analysis of the Semiclassical Approximation to Spin 1/2 Quantum Electrodynamics in 1+1 Dimensions"
[R4:R02]: https://arxiv.org/abs/gr-qc/0209075 "Linear Response, Validity of Semi-Classical Gravity, and the Stability of Flat Space"
[R4:R03]: https://arxiv.org/html/2001.08710v2 "Adiabatic regularization for Dirac fields in time-varying electric backgrounds"
[R4:R04]: https://arxiv.org/html/gr-qc/0507073v1 "Validity of semiclassical gravity in the stochastic gravity approach"
[R4:R05]: https://arxiv.org/html/2511.23464v2 "Schwinger effect with backreaction in 1+1D massive QED with a strong external field"
[R4:R06]: https://arxiv.org/html/1210.4031v3 "The renormalized locally covariant Dirac field"
[R4:R08]: https://arxiv.org/html/2509.16762v2 "Novel Bounds From The Weak Gravity and Festina Lente Conjectures"
[R4:R09]: https://arxiv.org/html/2607.03916v1 "Semiclassical regularity of compact trapped regions: From dynamical horizons to inner extremality"
[R4:R10]: https://arxiv.org/html/2601.20436v2 "Violation of the Leggett-Garg inequality in photon-graviton conversion"
[R4:R11]: https://link.springer.com/article/10.1140/epjc/s10052-026-16246-2 "Finite-field QED corrections to vacuum birefringence and magnetar polarization transport"
[S01]: https://ai.stanford.edu/~nilsson/OnlinePubs-Nils/PublishedPapers/astar.pdf "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
[S02]: https://www.cs.du.edu/~sturtevant/papers/MMaaai.pdf "Bidirectional Search That Is Guaranteed to Meet in the Middle"
[S04]: https://lean-lang.org/theorem_proving_in_lean4/Tactics/ "Theorem Proving in Lean 4 — Tactics"
[S05]: https://lean-lang.org/faq/ "Lean Frequently Asked Questions"
[TA01]: https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf "Ordinary Differential Equations and Dynamical Systems"
[TA02]: https://dlmf.nist.gov/5.9.E15 "DLMF 5.9.15: Binet integral for the digamma function"
[TA03]: https://dlmf.nist.gov/5.5.E2 "DLMF 5.5.2: Digamma recurrence"
[TA04]: https://dlmf.nist.gov/3.5#v "DLMF 3.5(v): Gauss quadrature"
[TA05]: https://physics.nist.gov/cuu/pdf/wallet_2022.pdf "2022 CODATA recommended values of the fundamental physical constants"

**TA06**: Frozen round-4 P3 contract, implementation and acceptance; `project artifact`.

[P:ACCEPT]: sandbox:/workspace/scratch/d757324dc341/qeg-research/round4/physics_acceptance.json

[P:BIANCHI]: sandbox:/workspace/scratch/d757324dc341/qeg-research/round5/symbolic_checks.py

[P:CRIT]: sandbox:/workspace/scratch/d757324dc341/qeg-research/round5/proof_critique.md

[P:P3]: sandbox:/workspace/scratch/d757324dc341/qeg-research/round4/response_contract.md

[P:T]: sandbox:/workspace/scratch/d757324dc341/qeg-research/round5/theorem_advisor.md
