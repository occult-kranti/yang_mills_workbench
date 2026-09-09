# Bidirectional proof dossier: a finite Maxwell–Dirac theorem and its gravity frontier

Research round 5 • 9 September 2026 • Equation audit, conventional proof, adversarial checks and executable dependency search.

## What this round establishes

We selected one sharply defined claim from the larger electromagnetic–quantum–gravitational project and proved it under explicit assumptions: the finite homogeneous Maxwell–Dirac initial-value problem used in the accepted response experiment has a unique solution for every finite future time. It has a quantitative electric-field bound; smooth changes in admissible initial data and drive have a finite-time differentiable response with retarded source support. For the selected regulator the proof establishes a global denominator bound, not just a sampled one:

\[
Z(a)>\frac34\quad(a\in\mathbb R),\qquad
|x(s)|\le\frac43|\lambda|\quad(s\ge0)
\]

for the exact vacuum start and a normalized nonnegative pulse of amplitude \(\lambda\). This is a conventional mathematical theorem obtained from the explicitly stated finite equations and standard ODE results. It is not a novel universal theorem of QED, a formal proof-assistant certificate, a continuum limit, or a solution of quantum gravity. The theorem's useful contribution is to remove a precise regularity gap in this project's finite model.

The wider theory remains open. The four original fronts share mechanisms, but their assumptions differ: de Sitter black-hole discharge bounds, curved-space particle creation, inner-horizon instability, and photon–graviton mixing cannot be chained as if each implies the next. The map below records those connections with separate edge types. A conjecture is never silently promoted to an axiom.

## How to read and reproduce this dossier

Start with the theory map to see what is assumed, established, derived here or unresolved. Read the theorem statement before its proof. Follow the forward estimates and the backward continuation requirements until they meet. Then inspect the explicit counterexamples: they determine which stronger statements this proof cannot support. Finally, use the gravity interface lemma to see what is needed next.

The companion package includes editable Markdown, the full machine-readable map, every proof-planning rule, symbolic checks, independent falsification tests, exact rational certificates, source reading-depth ledgers and the historical model contract. Run the instructions in README.md from the extracted package root. Reported test counts refer to executed checks, not votes by agents or a probability that a physical theory is true.

## Selection before search

| Candidate | Current proof-ready inputs | Missing decisive lemma | Decision |
|---|---|---|---|
| Global finite-model existence and causal response | Explicit smooth finite equations, positive modal state space, matched work identity | Global Z margin and compact continuation estimate | Select; both gaps are closed in this round |
| Uniform-in-time tangent stability | Exact first-variation equations | Positive perturbation norm or spectral/dynamical stability argument | Do not infer from signed tangent work |
| Regulator-independent continuum response | Finite trajectories and one fixed-window quadrature study | State, subtraction, uniform bounds, current and derivative convergence | Retain as a separate research target |
| Self-consistent Bianchi-I Einstein–QED | Classical constraints and a chosen symmetry | Renormalized directional stress, total force Ward identity, local closure | Derive constraint propagation now; quantum closure remains open |
| Unified WGC/FL, singularity and conversion theory | Several established model results and conjectural bounds | Shared hypotheses and genuine bridge theorems | No proof route currently supplied |

## What “bidirectional A*” means here

Mathematical proof is an AND/OR dependency problem. Applying a theorem often needs several premises simultaneously. A theory-name graph with ordinary reversible arrows would lose those conjunctions and permit invalid arguments. We therefore use finite ground Horn rules: a rule records every premise, one conclusion, its scope and a reference to an independently reviewed derivation.

Forward search accumulates conclusions only when every premise is present. Backward search replaces an unproved goal with a sufficient set of premises of an applicable theorem. For example, global continuation can be reduced to local uniqueness, a regular vector field and finite-time compact bounds. This is goal regression; it does not assert that global existence logically implies those particular sufficient conditions.

The two searches meet when all remaining backward obligations are already among the forward facts. The reconstructed route is replayed independently. We use the admissible zero heuristic, so costs are uniform-cost search costs. A first meeting is only a candidate. A separate forward uniform-cost goal pop certifies least cost within the frozen, finite supplied rule library. Neither minimal cost nor successful JSON replay validates the mathematics behind a rule: the attached derivations and critic review serve that separate purpose. Official Lean documentation makes the stronger distinction between proof generation and kernel verification. Lean tactics [@D010], Lean FAQ [@D011].

Costs currently count reviewed rule applications. They do not measure scientific truth, novelty, proof length in an unbounded mathematical language, or compute needed for quantum gravity. A failed search says that this finite library lacks a derivation, not that the target is false. Research conjectures can be explored only as retained explicit conditions.

## Corrections and methodological lessons

The energy estimate must cover zero initial energy, which is the actual vacuum preparation. We use \(\sqrt{W+\epsilon}\) and take a limit, avoiding division by zero. The global Z condition must hold for every potential reached by any allowed solution; a good trajectory minimum cannot supply it. A first variation of energy is signed and cannot become a positive tangent norm by naming it an energy. Fixed-time differentiability does not imply bounded response for all time. Finally, a covariant gravity source needs directional pressures and external-work accounting, not just an energy history.

During code review, the first planner draft ran forward certification to completion before its backward phase. Its positive fixture therefore met immediately at the original goal. That draft checked a proof route but did not demonstrate useful two-front search. The correction requires actual frontier expansion in both directions, an intermediate meeting, and a separate certification phase. The executable record states whether those gates pass; the algorithm's label is not acceptance evidence.

The theorem advisor and critic worked independently on the algebra and counterexamples. A separate search advisor specified the logical contract, and the coding agent implemented it. Completed prior agents remain inactive; they are not an unmonitored continuing swarm. Agent review is supporting process evidence, not a substitute for mathematical proof.

## Model coordinates and domain

Use \(\hbar=c=1\), physical fermion mass \(m>0\), charge magnitude \(e>0\), and

\[
s=mt,\qquad a=eA_z/m,\qquad x=eE_z/m^2,
\qquad b=|eB|/m^2.
\]

All theorem primes refer to dimensionless time s; its use of t as an abstract ODE variable is interchangeable with s, not with dimensionful proper time without the factor m. The selected values are b=10, longitudinal momentum window [-20,20] and Landau indices 0 through 4 inclusive. The theorem covers every positive exact Gauss–Legendre node count in that window. The historical response experiment used 1,024 longitudinal nodes per retained level. This is a temporal initial-value problem: it has no radial horizon condition, origin condition or spatial infinity boundary. Introducing one merely to resemble the original black-hole request would change the problem.


## A typed map of the research problem

This is a targeted map of 44 nodes, not an exhaustive inventory of physics. It separates physical framework choices, measured premises, mathematical theorems, numerical evidence and unresolved problems. The selected target is **M09: global-forward existence of the frozen finite Maxwell–Dirac system**. Its useful observable consequence is **M08: an all-time field envelope for an integrable drive**. Neither result proves the surrounding conjectures.

A backward search asks which jointly sufficient premises would prove a target. A forward search derives consequences from accepted premises. Their meeting is meaningful only when the entire premise set is satisfied. Adjacency, citation, similarity and agent agreement are insufficient.

### Foundations

| ID | Node and evidence type | Statement | Sources |
|---|---|---|---|
| F01 | **Classical implication and proof search** — method framework; adopted | Backward theorem application opens all missing premises; it never reverses an implication. | [@D007], [@D008], [@D010], [@D011] |
| F02 | **Real calculus and inner-product identities** — mathematical foundation; established | Chain rules, Cauchy–Schwarz and antisymmetry of the cross product support the finite energy argument. | [@D001], [@D027] |
| F03 | **Local ODE theory and continuation** — mathematical theorem; established | A locally Lipschitz finite ODE has a unique local solution; compact confinement permits continuation. | [@D001] |
| F04 | **Quantum state and unitary-evolution postulates** — framework postulate; assumed framework | Positive density operators and unitary dynamics specify the quantum blocks used in the model. | [@D026] |
| F05 | **Maxwell–Dirac gauge framework** — framework postulate; assumed framework | An abelian gauge connection coupled to a Dirac field supplies the electromagnetic matter framework. | [@D026], [@D028] |
| F06 | **Einstein gravitational framework** — framework postulate; assumed framework | The metric obeys Einstein equations with a declared total stress tensor and any specified higher-curvature terms. | [@D026], [@D037] |
| F07 | **Measured constants and frozen parameter choice** — empirical premise; measured and frozen | The solver freezes alpha=1/137.035999084; the proof needs only alpha<1/137. | [@D005], [@D006] |
| F08 | **Bloch-ball positivity** — mathematical theorem; established | The matrix (I+r·sigma)/2 is positive exactly when &#124;r&#124;<=1. | [@D027] |
| F09 | **Positive Gauss–Legendre quadrature** — mathematical theorem; established | Exact Gauss weights are positive and integrate constants exactly. | [@D004] |
| F10 | **Digamma recurrence and Binet positivity** — mathematical theorem; established | For b>0 the matched susceptibility bracket has a positive Binet-integral representation. | [@D002], [@D003], [@D027] |
| F11 | **Newtonian gravitational limit** — framework limit; restricted context | Newtonian gravitational interactions form a separate weak-field context, including current entanglement arguments. | [@D039] |

### Finite model and selected theorem

| ID | Node and evidence type | Statement | Sources |
|---|---|---|---|
| M01 | **Finite homogeneous regulator and state** — model assumption; frozen | Use fixed finite positive weights, positive masses and canonical momenta; production has b=10,K=20,n=0..4. | [@D026], [@D006] |
| M02 | **Matched finite Maxwell–Dirac closure** — model assumption; frozen | The mode equations and shared S,C,D,Z and energy definitions are fixed by T1–T5. | [@D027], [@D026] |
| M03 | **Admissible drive and parameter families** — model assumption; frozen | Use continuous drives; smooth compact pumps and differentiable source families support the production response. | [@D027], [@D026] |
| M04 | **All-potential coefficient margin** — mathematical theorem; proved conditionally | For the selected regulator, Z(a)>3/4 for every real a. | [@D027], [@D002], [@D003], [@D004] |
| M05 | **Invariant Bloch norms** — mathematical theorem; proved conditionally | Precession preserves each &#124;r_i&#124;, hence the initial Bloch balls. | [@D027] |
| M06 | **Positive finite excitation energy** — mathematical theorem; proved conditionally | Positive weights and &#124;r_i&#124;<=1 imply U=sum w_i(h_i·r_i+omega_i)>=0. | [@D027] |
| M07 | **Exact shared work balance** — mathematical theorem; proved conditionally | With W=Zx²/2+e²U, the frozen equations give Wdot=xF. | [@D027] |
| M08 | **Electric-field envelope** — mathematical theorem; proved conditionally | &#124;x(t)&#124;<=sqrt(2W0/z*)+&#124;&#124;F&#124;&#124;L1(0,t)/z*; vacuum unit impulse gives &#124;x&#124;<=4/3. | [@D027] |
| M09 | **Selected global-forward theorem** — mathematical theorem; proved conditionally | The selected finite system has a unique classical solution on every finite future interval. | [@D027] |
| M10 | **Finite-time tangent and retarded support** — mathematical theorem; proved conditionally | Differentiable source/state families satisfy the tangent system; unchanged preparation gives zero response before a delayed probe. | [@D027], [@D026], [@D042] |
| M11 | **Independent finite-model numerical checks** — numerical evidence; accepted limited | Round4 independent spinor/finite-difference checks and 512-to1024 momentum refinement support the recorded response implementation. | [@D006], [@D023] |
| M12 | **All-time response stability** — open problem; unresolved | Determine whether a declared physical perturbation norm remains uniformly controlled for admissible states. | [@D027], [@D042], [@D043] |

### Quantum and continuum obligations

| ID | Node and evidence type | Statement | Sources |
|---|---|---|---|
| Q01 | **Hadamard and local-covariance framework** — mathematical framework; established with scope | Local covariant renormalization organizes admissible states and finite current/stress ambiguities. | [@D014] |
| Q02 | **Common quantum current and directional stress** — open obligation; unresolved | Derive J,rho,p_perp,p_parallel from one state and common renormalization prescription. | [@D026], [@D014] |
| Q03 | **Full causal current/stress response blocks** — open obligation; partially mapped | Construct retarded JJ,JT,TJ,TT variations with all contact terms from a causal state prescription. | [@D026], [@D042], [@D043] |
| Q04 | **Physically smeared quantum noise** — open obligation; unresolved | Compute symmetrized connected current and stress fluctuations with physical smearing. | [@D017], [@D026] |
| Q05 | **Controlled continuum limit** — open obligation; unresolved | Prove regulator-uniform bounds and convergence to a defined renormalized continuum model. | [@D027], [@D025], [@D044] |
| Q06 | **Semiclassical validity criterion** — open problem; unresolved for target | Determine where mean-field evolution approximates the intended quantum observables. | [@D043], [@D017], [@D045] |

### Gravitational interface

| ID | Node and evidence type | Statement | Sources |
|---|---|---|---|
| G01 | **Axisymmetric Bianchi-I reduction** — model assumption; candidate reduction | Use ds²=-dt²+a_perp²(dx²+dy²)+a_parallel²dz² with aligned fields and diagonal total stress. | [@D026], [@D035] |
| G02 | **Total Ward defect** — defined observable; defined | Q=rhodot+2H_perp(rho+p_perp)+H_parallel(rho+p_parallel) measures total energy-conservation failure. | [@D024], [@D026] |
| G03 | **Bianchi-I constraint propagation** — conditional lemma; derived conditionally | Spatial Einstein evolution gives Cdot=-theta C-kappa Q; thus Q=0 and C(0)=0 preserve C=0. | [@D024] |
| G04 | **Self-consistent quantum Bianchi-I evolution** — open problem; unresolved | Solve the coupled geometry, fields and quantum state with constraint propagation and controlled validity. | [@D026], [@D036], [@D037] |

### Four surrounding research fronts

| ID | Node and evidence type | Statement | Sources |
|---|---|---|---|
| O01 | **Electric Weak Gravity Conjecture** — conjecture; open general statement | Conjecture an appropriately superextremal charged state relative to the relevant gravitational extremality relation. | [@D018], [@D046] |
| O02 | **Magnetic Weak Gravity Conjecture** — conjecture; open general statement | A magnetic/UV-scale version constrains the gauge-theory cutoff relative to gravity. | [@D018], [@D046] |
| O03 | **Festina Lente criterion** — conjecture; open general statement | Quasi-de Sitter discharge arguments motivate a lower charged-mass bound of schematic form m⁴≳g²q²H²M_Pl². | [@D019], [@D033], [@D046] |
| O04 | **Charged de-Sitter decay compatibility** — open problem; partially mapped | Reconcile discharge, Hawking evaporation, extremality and possible WGC/FL constraints in one causal model. | [@D033], [@D034], [@D046] |
| O05 | **Schwinger pair creation in prescribed fields** — established calculation; known with regime | Vacuum pair production is nonperturbative in an electric field; magnetic fields alter the charged spectrum. | [@D028], [@D041] |
| O06 | **Euler–Heisenberg and curvature expansion** — effective framework; known with regime | One-loop local effective actions encode vacuum polarization only within their field, derivative and curvature assumptions. | [@D029], [@D030], [@D031] |
| O07 | **Magnetized curved Schwinger backreaction** — open problem; unresolved target | Compute causal pair current and stress in a chosen strongly magnetized curved geometry, then evolve backreaction. | [@D026], [@D030], [@D044] |
| O08 | **Classical mass inflation** — conditional result; known with hypotheses | Coupled fluxes can destabilize charged inner horizons and produce mass inflation under specified data and decay assumptions. | [@D032] |
| O09 | **Quantum Cauchy-horizon endpoint** — open problem; unresolved target | Determine the backreacted endpoint when quantum stress, evaporation and inner-horizon dynamics interact. | [@D040], [@D038], [@D047] |
| O10 | **Perturbative photon–graviton conversion** — established calculation; known with regime | An external magnetic field couples photon and graviton perturbations; conversion depends on phase matching and polarization. | [@D021], [@D048] |
| O11 | **Quantum-dispersive conversion in strong fields** — open problem; unresolved target | Determine when QED birefringence, plasma and geometry suppress or permit coherent conversion. | [@D021], [@D049] |

### The accepted meeting of forward and backward reasoning

Forward: finite admissible blocks imply invariant Bloch balls; positive weights imply nonnegative finite excitation energy; the shared current/energy definitions give exact work balance. The analytic coefficient bound then yields a field envelope. Backward: global existence requires continuation; continuation requires finite-time confinement and an open, nonsingular equation domain. The envelope bounds the field, its integral bounds the potential on each finite interval, the Bloch norms bound the remaining coordinates, and the global denominator estimate prevents degeneracy.

\[ Z(a)>\frac34,\qquad W=\frac12Zx^2+e^2U,\qquad \dot W=xF. \]

\[ |x(t)|\le\sqrt{\frac{2W_0}{z_*}}+\frac{\|F\|_{L^1(0,t)}}{z_*}. \]

This is a conditional theorem about an exact finite ODE. The proof treats the zero-energy vacuum start without dividing by zero. Pure-state data need not make the potential uniformly bounded for all time by this argument; one strictly mixed block supplies an additional coercive estimate. Source response is retarded and finite on compact intervals, but its signed first-variation work is not a positive stability norm. See [@D027] and [@D025].

### A next conditional lemma, with its missing physical input

For the axisymmetric Bianchi-I metric define \(\theta=2H_\perp+H_\parallel\), \(C=H_\perp^2+2H_\perp H_\parallel-\kappa\rho\), and \(Q=\dot\rho+2H_\perp(\rho+p_\perp)+H_\parallel(\rho+p_\parallel)\). Absorb any constant cosmological term into the total density and pressures, or set it to zero. With the spatial Einstein equations imposed, the root derivation obtains

\[ \dot C=-\theta C-\kappa Q. \]

Thus \(Q=0\) and \(C(0)=0\) preserve the Hamiltonian constraint. The equation does not manufacture \(Q=0\). The total stress must include field, matter and any external/support sector consistently. The quantum current and both directional pressures remain unclosed. Zahn v3 section4.2 imposes a restriction on background gauge curvature in its stress argument; that result cannot simply be cited as the required nonzero-field Ward identity. [@D024], [@D014].

### How to interpret the connections

| Edge type | Meaning |
|---|---|
| assumption | A target adopts a premise or physical framework. |
| proved hyperedge | Every source node in the conjunction is required, together with stated target assumptions. |
| context | A relation worth studying; no logical implication. |
| restricted analogue | A shared mechanism in a different geometry, state or approximation. |
| unresolved bridge | A derivation, estimate, observable or physical closure is missing. |

The JSON records each node’s assumptions, dependencies, source reading provenance, scope and next obligation, plus explicit typed edges. Only the proved hyperedges may be used as accepted inference rules, and even those must retain all assumptions. The four original fronts require different geometries and observables: no single homogeneous calculation closes them.

### Next obligations in dependency order

1. Preserve the finite theorem and its counterexamples; formalize its statement if kernel checking is desired.
2. Prove regulator-uniform estimates or exhibit a failure; independently control momentum-window and Landau limits.
3. Derive current, energy and directional pressures from one state and subtraction prescription.
4. Establish the nonzero-field force Ward identity and account for supports; use the Bianchi lemma as a discriminating constraint test.
5. Construct causal response and physically smeared fluctuation observables; test semiclassical validity.
6. Return to one original front with its own geometry, quantum state, boundary conditions and approximation regime.


## Conditional theorem for the finite Maxwell–Dirac model

Advisor review, 9 September 2026. This is a conventional mathematical proof for the explicitly defined finite model from round 4. It is not a new theorem about continuum quantum electrodynamics or semiclassical Einstein equations, and it is not a machine-checked Lean proof. The exact identities below supply a useful forward chain from assumptions to consequences; the continuation criterion supplies the backward chain from the target to the estimates that must be proved.

**Decision:** accept global forward existence and uniqueness, an explicit electric-field energy bound, finite-time differentiability under the stated parameter regularity, and retarded support. Accept the analytic certificate \(Z(a)>3/4\) for every real potential \(a\) at the selected finite regulator. Reject the stronger inference that this proves all-time tangent stability, quantum fluctuation control, a continuum limit, or gravitational backreaction.

### 1. Model assumptions, rather than unqualified physical axioms

Let \(I=\{1,\ldots,L\}\) be a fixed finite nonempty mode list. For every mode fix \(w_i>0\), \(M_i>0\), and \(k_i\in\mathbb R\). Fix \(e^2>0\) and a finite real susceptibility \(\chi\). None of these quantities varies with time. Let the prescribed drive \(F\) be continuous on \([0,\infty)\). Set

\[
p_i=k_i-a,\qquad \omega_i=(M_i^2+p_i^2)^{1/2},\qquad
\mathbf h_i=(M_i,0,p_i),
\tag{T1}
\]

\[
S=\sum_iw_i\left(r_{iz}+\frac{p_i}{\omega_i}\right),\quad
C=\sum_iw_i\frac{M_i^2}{4\omega_i^5},\quad
D=\sum_iw_i\frac{5M_i^2p_i}{8\omega_i^7},\quad
Z(a)=1+\chi-e^2C(a).
\tag{T2}
\]

The exact real-arithmetic evolution under examination is

\[
a'=-x,\qquad
x'=\frac{F-e^2(S+Dx^2)}{Z},\qquad
\mathbf r_i'=2\mathbf h_i\times\mathbf r_i.
\tag{T3}
\]

Initial data are finite and obey \(|\mathbf r_i(0)|\le1\). Finally assume the **global coefficient bound**

\[
Z(a)\ge z_*>0\qquad\text{for every }a\in\mathbb R.
\tag{T4}
\]

These assumptions define a flat, homogeneous, fixed-magnetic-background mean-field model with a fixed finite regulator. The matching prescription in T2 is part of the assumed model. Proving consequences of that prescription does not independently derive its physical correctness. The proof is insensitive to the canonical momenta's spacing; it requires positivity and finiteness of the weights and masses.

The condition \(|\mathbf r|\le1\) is precisely positivity of the unit-trace two-dimensional density matrix \((I+\mathbf r\cdot\boldsymbol\sigma)/2\). Pure blocks have norm one; strictly mixed blocks have norm less than one. This mathematical extension does not assert that every such list is a continuum Hadamard state. The production preparation is the particular pure vacuum list \(\mathbf r_i(0)=-\mathbf h_i(0)/\omega_i(0)\), with \(x(0)=0\).

### 2. The target theorem

Under T1–T4, the initial-value problem has a unique classical solution for all \(t\ge0\). Define

\[
U=\sum_iw_i(\mathbf h_i\cdot\mathbf r_i+\omega_i),\qquad
W=\frac12Zx^2+e^2U,\qquad W_0=W(0).
\tag{T5}
\]

For every finite \(t\ge0\),

\[
U(t)\ge0,\quad W(t)\ge\frac{z_*}{2}x(t)^2,\quad
W'(t)=x(t)F(t),
\tag{T6}
\]

\[
\boxed{
|x(t)|\le \sqrt{\frac{2W_0}{z_*}}
+\frac1{z_*}\int_0^t|F(s)|\,ds.}
\tag{T7}
\]

If \(F\in L^1(0,\infty))\), T7 uniformly bounds the electric field, and T6 uniformly bounds \(W\) and \(U\). Every Bloch vector remains in its initial sphere. The proof gives a bound for \(a\) on every finite interval, and at most linear growth of \(|a|\) when \(F\in L^1\). It does **not**, for general pure-state data, establish a uniform bound on the entire state vector for all time.

### 3. Proof, with the zero-energy case retained

**Local existence and uniqueness.** Each \(\omega_i\ge M_i>0\), and T4 keeps the denominator away from zero. Consequently the right side of T3 is continuous in time and smooth in all state variables on an open finite-dimensional state space. It is locally Lipschitz in those variables uniformly on compact time intervals. The local theorem and the compact-set continuation criterion apply. Relevant reference locations are Teschl §2.2, Theorem 2.2; §2.6, Theorem 2.13, Lemma 2.14 and Corollary 2.15. Smooth dependence and first variations are treated in §2.4, Theorems 2.10–2.11. These are standard ODE inputs; the estimates that make them applicable here are derived next. [Teschl, author-hosted text [@D001].

**Invariant state positivity.** Antisymmetry of the cross product gives

\[
\frac{d}{dt}|\mathbf r_i|^2
=4\mathbf r_i\cdot(\mathbf h_i\times\mathbf r_i)=0.
\tag{T8}
\]

Thus the initial Bloch balls are invariant. Cauchy–Schwarz then yields, separately for every mode,

\[
\mathbf h_i\cdot\mathbf r_i+\omega_i
\ge\omega_i(1-|\mathbf r_i|)\ge0.
\tag{T9}
\]

The positive weights imply \(U\ge0\), and T4 gives the coercive field term in T6. There is no assumption that a signed, vacuum-subtracted continuum stress tensor is positive: T9 is a statement about this finite sum.

**Work identity.** Because \(p_i'=x\),

\[
\mathbf h_i'=(0,0,x),\qquad \omega_i'=p_ix/\omega_i,
\]

and the precession contribution to \((\mathbf h_i\cdot\mathbf r_i)'\) vanishes. Hence

\[
U'=xS,\qquad
C'=-\sum_iw_i\frac{5M_i^2p_ix}{4\omega_i^7}=-2Dx,
\qquad Z'=2e^2Dx.
\tag{T10}
\]

Direct differentiation, without an extra approximation, gives

\[
\begin{aligned}
W'&=\tfrac12Z'x^2+Zxx'+e^2U'\\
&=e^2Dx^3+x[F-e^2(S+Dx^2)]+e^2xS=xF.
\end{aligned}
\tag{T11}
\]

This cancellation would fail if the inertia correction, quadratic-current term and energy counterterm were chosen independently.

**Energy estimate at and away from \(W=0\).** A derivation that divides directly by \(\sqrt W\) is incomplete for the actual vacuum start, where \(W_0=0\). For \(\epsilon>0\), use T6 to obtain

\[
\frac{d}{dt}\sqrt{W+\epsilon}
=\frac{xF}{2\sqrt{W+\epsilon}}
\le\frac{|F|}{\sqrt{2z_*}}\sqrt{\frac{W}{W+\epsilon}}
\le\frac{|F|}{\sqrt{2z_*}}.
\tag{T12}
\]

Integrate and send \(\epsilon\downarrow0\):

\[
\sqrt{W(t)}\le\sqrt{W_0}
+\frac{1}{\sqrt{2z_*}}\int_0^t|F(s)|\,ds.
\tag{T13}
\]

Combining \(|x|\le\sqrt{2W/z_*}\) with T13 proves T7. Negative or sign-changing drive is allowed because its absolute integral appears. A drive that removes energy does not invalidate the estimate. A field reversal does not produce a singularity.

**Continuation.** Suppose a maximal forward interval ended at a finite \(T_+\). Continuity of the drive makes \(\int_0^{T_+}|F|\) finite. T7 gives a finite constant \(X_{T_+}\) bounding \(|x|\), and

\[
|a(t)|\le|a(0)|+\int_0^t|x(s)|\,ds
\le|a(0)|+T_+X_{T_+}.
\tag{T14}
\]

Together with T8, this confines every state coordinate to a compact set. On that set T4 excludes a denominator boundary and T1 excludes a zero mass gap. Compact continuation extends the solution beyond \(T_+\), a contradiction. Therefore no finite forward endpoint exists. This proves the theorem.

**An extra mixed-state consequence.** If at least one retained block \(j\) is strictly mixed, write \(\delta_j=1-|\mathbf r_j(0)|>0\). Then

\[
U\ge w_j\delta_j\omega_j
\ge w_j\delta_j|k_j-a|.
\tag{T15}
\]

An \(L^1\) drive therefore gives the additional uniform bound
\(|a|\le|k_j|+\sup W/(e^2w_j\delta_j)\). This strengthens the theorem for that subclass. The positive gap \(\delta_j\) is essential to this estimate; it vanishes for the production pure-state preparation.

### 4. Proving the global denominator condition before running a trajectory

For any finite positive-weight model,

\[
0<C(a)\le C_*:=\sum_i\frac{w_i}{4M_i^3},\qquad
Z(a)\ge1+\chi-e^2C_*.
\tag{T16}
\]

This follows from \(\omega_i\ge M_i\). It is a sufficient bound, not a claim that all modes simultaneously attain their individual maxima at one potential. If the right side is nonpositive, the test is inconclusive; it does not prove that the actual \(Z(a)\) crosses zero. In contrast, a positive minimum sampled along one trajectory does not prove T4.

For the matched magnetic susceptibility, set \(z=1/(2b)>0\). The exact recurrence and Binet integral imply

\[
\begin{aligned}
b-\log(2b)-\psi(1+1/(2b))
&=\log z-\frac1{2z}-\psi(z)\\
&=2\int_0^\infty
\frac{t}{(t^2+z^2)(e^{2\pi t}-1)}\,dt>0.
\end{aligned}
\tag{T17}
\]

The integrand has a finite positive limit at the origin and decays at infinity, so the positivity claim does not depend on subtracting nearly equal floating-point digamma terms. Thus \(\chi_b>0\) for every \(b>0\). The two primary identities are DLMF 5.5.2 [@D003] and DLMF 5.9.15 [@D002]. Only these identities, not a large-field asymptotic expansion, are used.

#### Selected finite regulator: exact analytic certificate

Take \(b=10\), \(K=20\), and Landau indices \(n=0,1,2,3,4\) inclusive. For any exact Gauss–Legendre rule with a positive number of nodes, its longitudinal weights are positive and sum to \(2K=40\). Positivity and polynomial exactness are stated in DLMF §3.5(v), equations 3.5.18–3.5.21 [@D004]. Only exactness on the constant function is required here. With \(d_0=1\), \(d_{n>0}=2\),

\[
\sum_{i:n_i=n}w_i=\frac{b\,d_n(2K)}{4\pi^2},\qquad
M_n^3=(1+20n)^{3/2}.
\tag{T18}
\]

For \(n=1,2,3,4\), use the deliberately conservative exact bounds

\[
21\sqrt{21}>84,\quad41\sqrt{41}>246,\quad
61\sqrt{61}>427,\quad81\sqrt{81}=729.
\tag{T19}
\]

Since \(e^2=4\pi\alpha\),

\[
\begin{aligned}
e^2C_*
&=\frac{100\alpha}{\pi}
\left[1+2\sum_{n=1}^4(1+20n)^{-3/2}\right]\\
&<\frac{100}{137(314/100)}
\left[1+2\left(\frac1{84}+\frac1{246}+\frac1{427}+\frac1{729}\right)\right]\\
&=\frac{66325137500}{274510827927}<\frac14.
\end{aligned}
\tag{T20}
\]

The final strict comparison is exactly equivalent to
\(265300550000<274510827927\); the positive rational margin below \(1/4\) is \(9210277927/1098043311708\). Together with T17,

\[
\boxed{Z(a)>3/4\quad\text{for every real }a.}
\tag{T21}
\]

This certificate is independent of time, source amplitude, canonical-grid translation, and longitudinal node count for the stated exact quadrature family. It is much more conservative than the recorded trajectory minimum \(0.9965117049606924\), because it bounds every mode by its separate worst case. No numerical trajectory is an input to T20.

The assumptions \(\alpha<1/137\) and \(\pi>3.14\) are ample. The frozen production source defines \(\alpha=1/137.035999084\); its defining decimal already implies the first inequality. The current NIST table inspected in this review lists a slightly different recommended central value, \(7.2973525643\times10^{-3}\), which also satisfies it. The historical solver constant has been preserved; the proof does not silently update the experiment. NIST 2022 CODATA table [@D005].

For a normalized nonnegative compact pump \(F=\lambda g_T\), \(\int g_T=1\), and the exact production vacuum preparation \(W_0=0\), T7 yields

\[
\boxed{|x(t)|\le4|\lambda|/3\qquad(t\ge0).}
\tag{T22}
\]

For \(\lambda=1\), this is an all-time electric-field amplitude bound \(4/3\). It neither predicts the detailed waveform nor bounds its amplitude derivative by \(4/3\). Differentiating an inequality between nonlinear solution families does not produce an inequality between their derivatives.

#### Exact quadrature, rounded coefficients, and a computed trajectory are different claims

The selected code creates weights and masses in IEEE double precision. At 1,024 nodes the observed weight totals differ from the usual double-precision expression for T18 by approximately \(-1.78\times10^{-15}\) in level zero and \(-3.55\times10^{-15}\) in each other level. This is harmless as a diagnostic, but an approximate equality is not the exact Gauss–Legendre identity.

A separate check performed in this review interpreted every generated weight, mass, \(e^2\), and \(\chi\) as its exact binary rational. Grouping weights by their five repeated masses and using rational arithmetic in T16 produced the **exact comparison**

\[
1+\widehat\chi-\widehat{e^2}\sum_i\frac{\widehat w_i}{4\widehat M_i^3}>3/4.
\tag{T23}
\]

Its decimal display is approximately \(0.7653173589206453\), with a margin approximately \(0.015317358920645334\). Every generated weight was positive and every mass positive. This certifies the real-arithmetic ODE using that rounded coefficient list, provided its initial vectors satisfy the exact norm condition. It does not certify accumulated floating-point time-stepping errors or an interval enclosure of the recorded trajectory. The saved trajectory has small nonzero norm defects, so it cannot itself be called an exact invariant-ball solution.

Reproduction recipe for T23: generate the frozen `response.Grid(response.Params(nK=1024))`; convert floats using `Fraction.from_float`; sum the weights in each Landau group exactly; divide by four times that group's exact rational mass cubed; multiply by the exact rational `response.E2`; compare `1 + Fraction.from_float(response._chi(10)) - E2*Cstar` with `Fraction(3,4)`. No floating transcendental function is being certified by that operation: the already evaluated coefficient is the rational model input. The original analytic susceptibility is certified separately by T17.

### 5. Tangent existence, causality, and the missing stability inference

Let \(Y=(a,x,\mathbf r_1,\ldots,\mathbf r_L)\). For a source family \(F(t;\lambda)\) with continuous first parameter derivative and an admissible continuously differentiable initial-data family, standard parameter dependence gives a first variation on each compact time interval. If the complete drive/data family is \(C^k\), the corresponding solution family is \(C^k\); a merely continuous drive does not imply unlimited differentiability with respect to time. The smooth compact production pulse meets the stronger hypothesis.

For the fixed canonical grid define \(v=\partial_\lambda a\), \(u=\partial_\lambda x\), \(\boldsymbol\eta_i=\partial_\lambda\mathbf r_i\), \(q_i=-v\) and \(f=\partial_\lambda F\). Direct differentiation gives

\[
\begin{gathered}
\delta S=\sum_iw_i(\eta_{iz}+M_i^2q_i/\omega_i^3),\\
\delta C=-\sum_iw_i\frac{5M_i^2p_iq_i}{4\omega_i^7},\quad
\delta D=\sum_iw_i\frac{5M_i^2(M_i^2-6p_i^2)q_i}{8\omega_i^9},\\
v'=-u,\qquad
u'=\frac{f-e^2(\delta S+\delta D x^2+2Dxu)+e^2\delta C x'}{Z},\\
\boldsymbol\eta_i'=2\mathbf h_i\times\boldsymbol\eta_i
+2(0,0,q_i)\times\mathbf r_i.
\end{gathered}
\tag{T24}
\]

Writing this as \(\delta Y'=A(t)\delta Y+B(t)f\), with \(B=\mathbf e_x/Z\), its continuous coefficients are bounded on each fixed finite interval. If \(\Phi(t,s)\) is the fundamental matrix,

\[
\delta Y(t)=\Phi(t,0)\delta Y(0)
+\int_0^t\Phi(t,s)B(s)f(s)\,ds.
\tag{T25}
\]

This proves retarded support: if initial variations vanish and the source variation vanishes before \(t_p\), every tangent is zero before \(t_p\). For a bound \(\|A(t)\|\le L_T\) on \([0,T]\),

\[
\|\delta Y(t)\|\le e^{L_Tt}
\left(\|\delta Y(0)\|+\frac1{z_*}\int_0^t|f(s)|\,ds\right).
\tag{T26}
\]

This finite-time estimate supplies existence and continuous dependence, not a useful uniform-in-time stability constant. Neither \(L_T\) nor its exponential has been bounded independently of \(T\).

Two exact tangent facts require especially careful wording:

* \((\mathbf r_i\cdot\boldsymbol\eta_i)'=0\), but this conserved value is zero only when the initial family has fixed norm to first order. A mixed family \(\mathbf r(\lambda)=(\lambda,0,0)\) at \(\lambda=1/2\) has \(\mathbf r\cdot\boldsymbol\eta=1/2\). The pure-state tangent constraint must not be imposed on every mixed-state variation.
* \(\delta W=Zxu-e^2\delta C\,x^2/2+e^2\delta U\) is signed and obeys \((\delta W)'=uF+xf\). It is not a positive quadratic norm of the tangent. Conservation of \(\delta W\) after source shutoff cannot prove tangent stability.

A concrete falsifier of the latter inference uses one mode, \(M=w=e^2=1\), \(k=a=x=0\), \(\chi=F=0\), and the admissible rotated initial family \(\mathbf r(\lambda)=(-\cos\lambda,0,\sin\lambda)\). At \(\lambda=0\), the baseline is stationary, \(Z=3/4\), \(\delta W=0\), but \(\eta_z=1\) and \(u'(0)=-4/3\). A nonzero response is compatible with zero first-variation energy. This example does not claim an instability; it invalidates that proposed stability diagnostic.

### 6. Assumptions that cannot be silently deleted

| Proposed shortcut | Why the proof fails or the interpretation changes |
|---|---|
| Only check \(Z>0\) at sampled times | There is no all-potential margin; denominator degeneracy can occur elsewhere or between samples. |
| Declare failure whenever T16 is nonpositive | T16 is sufficient, not necessary; its separate mode maxima may overestimate the actual maximum of \(C(a)\). |
| Allow \(M_i=0\) without a new analysis | \(p_i=0\) can make the square-root derivatives and counterterms undefined; smoothness and T16 no longer follow. |
| Allow negative weights | The sum of individually nonnegative modal energies need not be nonnegative. |
| Permit \(|\mathbf r_i|>1\) | State positivity and T9 fail. For \(M=1,p=0,\mathbf r=(-2,0,0)\), the modal energy is \(-1\). |
| Use arbitrary time-dependent weights, masses or matching | T10–T11 acquire extra work and parameter-derivative terms. |
| Replace the finite sum with an infinite limit | Uniform coercivity, renormalized-energy control, compactness and convergence have not been established. |
| Use a discontinuous or merely integrable drive but claim a classical smooth solution | One must instead state and prove an appropriate absolutely continuous/Carathéodory formulation. The present theorem uses a continuous drive. |
| Divide response by instantaneous \(x(t)\) | Ordinary field zeros make the ratio undefined; they are not evidence of an instability. |
| Differentiate the amplitude envelope T22 to bound \(u\) | Derivatives cannot be inferred from an inequality between function values. |
| Call the energy bound a quantum-noise estimate | No symmetrized current or stress fluctuation observable appears in the theorem. |
| Insert the energy alone into Einstein equations | A conserved covariant source also needs directional pressures, current/stress compatibility and gravitational constraints. |

### 7. Forward and backward proof connections

The forward chain is **finite admissible blocks → invariant Bloch balls → positive finite excitation energy → exact work balance → field envelope → compact finite-time state bounds**. The backward chain is **global solution target → continuation criterion → finite-time compactness and a nonsingular vector field → bounds on \(a,x,\mathbf r\) and a uniform \(Z\) margin**. They meet at T7, T8, T14 and T21. No edge is inverted simply because its forward implication is true.

The accepted theorem removes one concrete dependency: the selected finite dynamical model cannot develop a finite-time solution singularity from its own denominator or field amplitude under the stated continuous drive. It does not establish that its tangent stays uniformly small. The next proof obligations are distinct: a controlled infinite-regulator limit; a stronger stability norm or a discriminating instability result; fluctuation observables with physical smearing; and a common covariant current/stress closure. Those obligations must be added as open nodes rather than drawn as already proved consequences.

### 8. Review outcome and provenance

The round-4 acceptance file identifies the 1,024-node production run, source hash `0a197f5b46de8114d790c937059018d21df3f55a436c76067b91c09277035867`, fixed \(K=20\), and Landau indices zero through four. Its numerical response and finite-difference evidence remain numerical evidence. The theorem above is an additional analytic statement over the same declared model and a larger class of admissible initial data. It neither upgrades sampled errors into interval enclosures nor retrospectively erases underresolved runs.

The independent critic specifically challenged the zero-energy square-root step, all-time wording, mixed-state tangent normalization, and use of signed tangent work as a norm. Those challenges are addressed above. This advisor accepts T6–T7, T21–T22 and finite-time T24–T26 under their hypotheses. All-time tangent stability, continuum QED validity, quantum noise control and a gravitational solution remain **unproved**.


## Independent skeptical review of the finite-model theorem

Review date: 9 September 2026. Reviewed inputs: `round4/response_contract.md` and `round4/physics_acceptance.json`. This reviewer did not import the production response solver. Independent exact calculations are in `counterexamples.py`; their output is `counterexample_results.json`.

### Decision

The proposed global-existence and causal-response result is supportable as a **conditional theorem of the specified finite-dimensional model**. It is stronger than sampled numerical consistency but narrower than continuum quantum electrodynamics, a stability theorem, a quantum-noise calculation, or a theorem about the four original black-hole/gravity problems.

The important correction is to state every hypothesis before connecting the result to the next theory. In particular, the energy identity does not itself provide a coercive norm for the tangent, and a small sampled minimum of a denominator is not its global positive lower bound. For the selected exact mathematical regulator, a separate rational inequality does supply a positive denominator for every potential value.

### 1. Hypotheses that the proof needs

1. A finite, fixed list of modes, with real fixed canonical momenta, strictly positive masses, and positive weights. Zero weights can simply be discarded. The regulator is part of the theorem's model, not a quantity silently removed by the proof.
2. Fixed finite charge coupling and matching coefficient. The selected physical case has `e²>0`; `e=0` is a separate decoupled limit. No denominator involving `1/e²` may be used in that limit.
3. Initial `|r_i|<=1`. The equations conserve these norms. A pure state requires equality; the mixed-state extension requires the inequality. An arbitrary numerical vector outside the unit ball does not automatically satisfy the energy argument.
4. A lower bound `Z(a)>=z_*>0` for all reachable potential values, proved independently of a finite sample. The clean sufficient hypothesis is a bound for every real `a`. A bound valid only on a proposed region requires a separate proof that the trajectory cannot leave that region.
5. For a classical theorem on every finite time interval, a continuous prescribed drive on `[0,infinity)` is sufficient. A merely locally integrable drive gives an absolutely continuous Carathéodory solution and almost-everywhere identities; one must say that explicitly. A source with a finite-time nonintegrable pole is outside either statement across that pole.
6. For source differentiation, a differentiable initial-data family and a sufficiently regular source family. A convenient sufficient condition is a source continuously differentiable in `(t,lambda)` on compact sets. More generally, a `C¹` map into `L¹([0,T])` with appropriate uniform bounds supports an integral-equation proof. Pointwise parameter derivatives without domination are not enough to interchange differentiation and time integration.
7. For every finite comparison interval, the family must have a common parameter neighborhood and remain separated from `Z=0`. If the regulator is fixed and its all-`a` bound holds, the denominator requirement is uniform automatically. If masses, weights, coupling, or matching are varied, their derivatives and a uniform positive neighborhood must also be included.
8. A causal source-response claim needs the same initial state and source history before the perturbation begins. It does not apply to deliberately different initial states.

The standard local existence, compact-set continuation, and smooth parameter-dependence tools used here can be checked in Teschl's author-hosted text, Theorems 2.2 and 2.11 and Corollary 2.16; the discussion on printed page 42 treats measurable forcing. Only the relevant sections were consulted, not the entire book. Teschl, *Ordinary Differential Equations and Dynamical Systems* [@D001]

### 2. Independent energy audit

Since `|h_i|=omega_i` and `|r_i|<=1`, Cauchy–Schwarz gives

\[
U=\sum_iw_i(h_i\cdot r_i+\omega_i)\ge0,
\qquad W=\tfrac12 Zx^2+e^2U\ge\tfrac12z_*x^2.
\]

The derivative signs are essential. From `p'=x`, direct differentiation gives

\[
U'=xS,\qquad C'=-2Dx,\qquad Z'=2e^2Dx.
\]

Therefore

\[
W'=Zxx'+e^2Dx^3+e^2xS=xF.
\]

All four identities, including Bloch-norm preservation, simplify to zero in the independent symbolic check. This is an exact algebra check for the stated equations; it is not an independent derivation of those equations from continuum QED.

At positive `W`, `d sqrt(W)/dt <= |F|/sqrt(2z_*)`. To cover an initial vacuum with `W=0`, apply the calculation to `sqrt(W+epsilon)` and then take `epsilon` down to zero. Consequently,

\[
\sqrt{W(t)}\le \sqrt{W(0)}+
 \frac{1}{\sqrt{2z_*}}\int_0^t|F(s)|\,ds,
\]

\[
|x(t)|\le \sqrt{\frac{2W(0)}{z_*}}+
 \frac{1}{z_*}\int_0^t|F(s)|\,ds.
\]

For every finite `T`, this bounds `x`; integrating `a'=-x` bounds `a` on `[0,T]`; the Bloch norms bound all mode coordinates. The trajectory therefore stays in a compact subset of the smooth state domain separated from `Z=0`, permitting continuation beyond every finite endpoint. This proves global forward existence and uniqueness under the hypotheses.

For an integrable drive on the entire half-line, `W`, `x`, `U` and the Bloch vectors are uniformly bounded. The energy argument only supplies a linear-in-time bound for `a`, not a uniform bound on `a`. These distinctions must remain visible in the theorem statement.

### 3. Exact certificate for the selected regulator

With the physical weights in P1, positive exact longitudinal quadrature weights summing to `2K`, and `e²=4 pi alpha`,

\[
e^2C(a)\le \frac{\alpha bK}{2\pi}
\sum_{n=0}^{N}\frac{2-\delta_{n0}}{M_n^3}.
\]

This bound is valid for every `a`; it does not depend on the chosen canonical nodes. For `b=10`, `K=20`, and `N=4` **inclusive**, use

\[
M_0^3=1,\quad M_1^3\ge84,\quad M_2^3\ge246,
\quad M_3^3\ge427,\quad M_4^3=729.
\]

The lower bounds follow from the integer comparisons `(1+20n)^3 >= L_n²` for the positive quantities involved. With `0<alpha<1/137`, `pi>157/50`, and the separately supplied `chi>=0` hypothesis,

\[
e^2C(a)<\frac{100}{137(157/50)}
 \left[1+2\left(\frac1{84}+\frac1{246}+\frac1{427}+\frac1{729}\right)\right]
=\frac{66325137500}{274510827927}<\frac14.
\]

The last comparison is an exact integer comparison, with positive margin

\[
\frac14-\frac{66325137500}{274510827927}
=\frac{9210277927}{1098043311708}>0.
\]

Thus `Z>3/4` for this exact model, independently of the numerical trajectory. The fraction for the strict margin above is copied from the executable rational certificate.

The conclusion applies to mathematical quadrature weights with the stated exact sum. Floating-point generated weights and rounded constants define nearby parameters. To make a machine-specific certificate, bound their weight sum, positivity and constant rounding with rational or interval arithmetic. Agreement of floating sums to a few ulps is a diagnostic, not that certificate. The large exact margin makes such an implementation certificate plausible, but this review does not substitute plausibility for execution.

### 4. Explicit failed inferences and counterexamples

#### A. Pointwise positive `Z` is not a global separation theorem

Take one mode with `M=1`, `w=4`, `e²=1`, `chi=0`, `k=0`, and the admissible mixed state `r=0`. Prescribe

\[
p(t)=1-t,\quad a(t)=t-1,\quad x(t)=-1,\quad
\omega=\sqrt{1+p^2},\quad
F(t)=\frac{4p}{\omega}+\frac{5p}{2\omega^7}.
\]

Here `Z=1-omega^{-5}` is strictly positive on `[0,1)` and vanishes at `t=1`. The smooth source gives `F-S-Dx²=0`, so the trajectory solves the divided ODE before that time. All fields remain finite, but the divided equation reaches `0/0` at `t=1`. A possibly extendible undivided differential-algebraic equation is a different problem. This invalidates continuation based solely on a positive initial or sampled denominator.

#### B. Energy positivity uses physical initial states and positive weights

For `M=1,p=0,w=1,r=(-2,0,0)`, `U=-1`. For `M=1,p=0,w=-1,r=(1,0,0)`, `U=-2`. These are outside the hypotheses. They demonstrate why dropping either Bloch admissibility or positive quadrature weights invalidates the coercivity step.

For `M=p=0`, the chosen vacuum normalization and several displayed fractions are undefined. A massless model might exist after a separate limiting or reformulation procedure, but it is not justified by substituting zero into this theorem.

#### C. A conserved tangent work quantity does not bound the tangent

Use one mode with `M=w=e²=1`, `p=0`, `chi=0`, and the pure initial-state family

\[
r(0;\lambda)=(-\cos\lambda,0,\sin\lambda),\qquad a(0)=x(0)=0.
\]

At `lambda=0`, `eta(0)=(0,0,1)`, `delta W(0)=0`, while `u'(0)=-4/3` when `F=f=0`. The tangent-work identity stays zero, but the response is nonzero. The first variation of a positive energy is a signed linear functional, not a positive quadratic tangent norm.

Also, the theorem's mixed-state extension must not impose the pure-state constraint unconditionally: the admissible family `r(lambda)=(lambda,0,0)` at `lambda=1/2` has `r dot eta=1/2`. That inner product is conserved; it is zero only when the initial family preserves its Bloch radius.

#### D. Bounded global trajectories need not have bounded all-time derivatives

The exact family `(cos(lambda t),sin(lambda t))` has unit norm for all time, whereas its parameter derivative has norm `t`. This example refutes the general logical implication from bounded solutions to bounded parameter sensitivities. It does not claim instability of the selected Maxwell–Dirac run.

Similarly, `x(t,lambda)=cos(t)+lambda sin(t)` has a finite absolute derivative at `t=pi/2`, but a ratio using the vanishing baseline field diverges. A relative-gain pole at an ordinary field crossing is not a singular physical response.

#### E. Continuous parameter dependence is not differentiability

At fixed one-mode positive-gap parameters, set `r=0`, `x(t,lambda)=t|lambda|`, `a=-t²|lambda|/2`, and define `F=Zx'+e²(S+Dx²)`. Each trajectory is a valid smooth-in-time solution. The source family is continuous in the parameter, but the solution has opposite one-sided derivatives at zero. A differentiable source family cannot be omitted from a tangent theorem.

An additional general warning comes from a moving narrow source pulse: `F_lambda(t)=sgn(lambda) g(t/|lambda|)`, with `g` smooth and supported inside `(1,2)`. Its pointwise parameter derivative at zero is zero for every fixed time, while its integral is proportional to `lambda`. Thus differentiating only pointwise and then integrating loses the pulse. This is a warning about a missing domination hypothesis; it is not an executed Maxwell–Dirac experiment.

#### F. Every finite cutoff can exist globally while the continuum data diverge

For modes `i=1,...,N`, take `M_i=1`, `k_i=i`, `w_i=1/i²`, initially `a=x=0` and `r_i=h_i/omega_i`, with `e²=1`, `chi=0`. For every potential `a`, `omega_i>=1`, so

\[
C(a)\le\frac14\sum_{i\ge1}i^{-2}\le\frac14(1+1)=1/2,
\qquad Z(a)\ge1/2.
\]

At the initial potential, `omega_i>=i`, hence `U(0)>=2 sum_{i=1}^N 1/i`, which diverges with `N`. Each finite truncation satisfies the existence assumptions, while its initial energy diverges in the infinite list. This is a mathematical counterexample to inferring a finite continuum energy from finite-model global existence, not an asserted physical ultraviolet state for QED.

### 5. Conditional next link to gravity

For aligned-field Bianchi I, write `H_perp=Hp`, `H_parallel=Hl` and

\[
\mathcal C=H_p^2+2H_pH_l-\kappa\rho-\Lambda,\qquad
Q=\dot\rho+2H_p(\rho+p_\perp)+H_l(\rho+p_\parallel).
\]

Using the two spatial Einstein equations supplied by the root advisor,

\[
\dot H_p=\frac{\Lambda-\kappa p_\parallel-3H_p^2}{2},
\]
\[
\dot H_l=\Lambda-\kappa p_\perp-\dot H_p-H_p^2-H_l^2-H_pH_l,
\]

the independent exact simplification is

\[
\dot{\mathcal C}=-(2H_p+H_l)\mathcal C-\kappa Q.
\]

Consequently, total Ward conservation and an initially satisfied constraint imply constraint propagation. The adjective **total** matters. Aligned electromagnetic fields have `rho_EM=(E²+B²)/2`, `p_perp_EM=rho_EM`, `p_parallel_EM=-rho_EM`. With the P27 Maxwell equations, their work balance is `-E(J_q+J_ext)`. Adding the quantum-matter work `+EJ_q` leaves `Q=-EJ_ext` if the external apparatus is omitted. Even at `C=0`, this gives `Cdot=+kappa E J_ext`.

This identifies a necessary support/source sector for any pumped gravitational experiment. It does not provide either directional quantum pressure, renormalized stress response, or a completed covariant quantum closure. Conversely, a correctly propagated constraint would not prove that an arbitrarily selected stress closure represents QED.

### 6. Review gates before promoting a claim

| Gate | Acceptance condition | What failure means |
|---|---|---|
| Model identity | The finite regulator, matching and positive weights are stated | Theorems and experiments refer to different systems |
| Exact algebra | Independently simplified norm, work and current identities | A sign or coefficient blocks the proof |
| Coercivity | Physical Bloch norms and a proved all-domain positive `Z` gap | The energy estimate cannot establish continuation |
| Zero-energy endpoint | Square-root regularization covers the prepared vacuum | A proof divided by zero at its own initial data |
| Continuation | All state components are bounded on each finite interval | Bounding the electric field alone is insufficient |
| Derivative regularity | A common parameter neighborhood and differentiable source/data family | Formal tangent equations need not be derivatives of solutions |
| Causal comparison | Identical initial states and pre-probe sources | Early response could simply be an initial-state perturbation |
| Claim scope | No asymptotic stability or continuum conclusion from this theorem | A logically unsupported theory connection |
| Gravity interface | Both pressures, total Ward conservation and initial constraint | Energy-only closure or unsupported pumping violates the bridge |
| Implementation proof | Exact or interval bounds for floating inputs if claimed | Numerical consistency is being mislabeled as certification |

The executable checks confirm identities and counterexamples. They are not Lean/Isabelle proof objects, an exhaustive proof search, or an automatic validation of the entire physical theory. The forward/backward proof frontier should stop at the missing continuum, covariant-stress, noise and initial-constraint lemmas rather than introducing an unjustified edge to a grand conclusion.


## Bidirectional proof planning: a finite, auditable search contract

Version 1.0, 9 September 2026. This is an implementation contract and a mathematical proof-planning proposal. It does not claim that a graph search proves continuum quantum electrodynamics or gravitation. The numerical results in round 4 remain numerical evidence for their stated finite model.

### 1. What the search must accomplish

Start at two precisely different objects: an explicitly declared set of available assumptions and established lemmas, and an explicitly stated target theorem. Forward search asks what follows from what is available. Backward search asks which sufficient premises would let an already checked theorem establish the target. When every remaining backward premise is already available forward, reconstruct the entire derivation and independently check every application.

The selected mathematical target is **global forward well-posedness, together with smooth finite-time source-amplitude dependence, of the finite-regulator homogeneous Maxwell–Dirac ODE under a uniform positive kinetic-coefficient hypothesis**. This is a bounded advance over observing converged trajectories. It does not assert uniform bounds as the regulator is removed, stability as time tends to infinity, or agreement with fully quantized electromagnetism.

The algorithm is inspired by A* and bidirectional heuristic search. A* combines accumulated cost with an estimated remaining cost; this project starts with the admissible baseline heuristic zero. The original historical source is Hart, Nilsson and Raphael, 1968 [@D007]. We make no claim here about optimal efficiency among all possible heuristic algorithms.

The MM algorithm gives a rigorously specified midpoint property and stopping rule for its own graph-search setting. Our forward fact sets and backward sufficient-goal sets are different representations. Its theorem cannot be imported by merely giving our program a bidirectional name. Holte et al., 2016 [@D008] The independently checked forward uniform-cost certificate below supplies the optimization guarantee actually used here.

### 2. Separate the theory map from the proof graph

The broad research map may contain definitions, mathematical theorems, physical postulates, effective descriptions, empirically supported claims, conjectures, contradictions and proposed experiments. Its arrows must be typed: implication, sufficient condition, limiting case, approximation, motivation, analogy or unresolved dependency. Only a checked implication, with all its hypotheses, may become an inference rule.

An analogy is never a proof edge. A numerical experiment is not an exact existence theorem. An implication valid for fixed positive masses cannot be instantiated at a zero-mass point. A statement proved with a finite mode set cannot lose its finite-regulator type when passed to another node. Dependency extraction and premise retrieval are useful precisely because mathematical statements depend on specific earlier results; LeanDojo exposes such dependencies and tactic feedback for Lean repositories. LeanDojo [@D012]

A node record must include:

| Field | Requirement |
|---|---|
| `id` | Unique stable atom identifier |
| `statement` | Full sentence with quantifiers, domains and inequalities |
| `scope` | For example `finite_homogeneous_fixed_B`, never just `QED` |
| `kind` | Definition, theorem, declared hypothesis, numerical evidence, conjecture, target |
| `assumption_ids` | Explicit inherited hypotheses; the ledger never silently drops them |
| `verification` | Manual derivation/review, symbolic check, kernel-checked proof, numeric evidence, or unverified |
| `source` | Exact local theorem section or primary external source |
| `version` | Statement and proof revision, tied to the rule-library hash |

A rule is `id, premises, conclusion, cost, scope, proof_ref, review_status`. It represents only the grounded implication

\[
\left(\bigwedge_{p\in P_r}p\right)\Longrightarrow q_r.
\tag{S1}
\]

Use a finite atom universe and a finite library of ground rules. No free unification variables, quantified term generation, default negation, existential witness invention, destructive actions or rule creation during a certified search. A new candidate lemma is evaluated outside the frozen run and creates a new library version only after review. This restriction makes the search claims finite and testable.

The theorem remains conditional on declared mathematical/model hypotheses. Reporting `A1 ∧ ... ∧ A6 ⇒ T` accurately is different from asserting `T` for the physical universe. An experimental branch may explicitly assume a conjecture, but all its descendants retain that conjecture and cannot be presented as an unconditional result. Numerical evidence and conjecture atoms are excluded from exact-proof initial facts unless their role is explicitly a hypothesis of a conditional query.

### 3. AND/OR semantics and the direction that must not be reversed

One rule with three premises is an AND requirement: all three are needed. Two different applicable rules for the same conclusion are OR alternatives. Represent each conjunctive rule as a hyperedge, or as a visibly labeled rule node receiving all prerequisite arrows. Ordinary paths that touch only one prerequisite do not represent proofs.

For example, from `energy_identity ∧ coercivity ∧ source_integrable ⇒ bounded_field`, backward reasoning replaces the goal `bounded_field` by those three goals. It does **not** infer the three premises from the truth of `bounded_field`. The same distinction appears in Lean's `apply`: applying a theorem matching the conclusion creates the remaining premise goals. Theorem Proving in Lean: Tactics [@D010]

Backward regression preserves **sufficiency**, not equivalence and not necessity. If a selected route requires coercivity and coercivity has not been established, that route is blocked. Another theorem might establish the target by different means. Failure of a sufficient condition does not disprove the desired conclusion.

### 4. Executable forward and backward searches

Let `A` be the finite set of atoms, `F0 ⊆ A` the initial facts/declared hypotheses and `T ⊆ A` the conjunctive target. All rule costs are positive integers in the baseline. Unit costs measure the number of rule applications, not physical truth, confidence, proof difficulty or research priority.

**Forward state.** An immutable fact set `F`. A rule is applicable when `P_r ⊆ F` and `q_r ∉ F`; its successor is

\[
F'=F\cup\{q_r\},\qquad g_F(F')=g_F(F)+c_r.
\tag{S2}
\]

Store the least cost and a parent/rule pointer for each exact set. Do not replace a state by its free deductive closure while still charging per-rule costs: that would erase proof cost. A separate saturation pass may decide reachability and identify blocked atoms, but it is not the costed search.

**Backward state.** An immutable set `G` of jointly sufficient obligations. Start at `G=T`, cost zero. For any `q_r ∈ G`, regress along an admitted rule:

\[
G'=(G\setminus\{q_r\})\cup P_r,
\qquad g_B(G')=g_B(G)+c_r.
\tag{S3}
\]

The invariant is: establishing every atom in `G`, followed by the recorded suffix in reverse regression order, suffices to establish `T`. Store the least cost for each exact goal set, use visited/distances to suppress cycles, and keep a parent pointer to the previous goal set and chosen rule. Never remove an unsatisfied conjunct merely because it appears on another branch.

**Meeting.** A forward and a backward state meet if and only if

\[
G\subseteq F.
\tag{S4}
\]

They need not be equal. The forward set may contain additional valid lemmas. Scan stored reachable states or maintain an indexed subset query; for the small initial library a direct scan is easier to verify. Interleave two min-heaps with `priority=g` (`h=0`) using a documented deterministic tie-break. A tie-break or large-language-model preference may affect work performed but must not affect acceptance.

**Reconstruction.** Recover the forward prefix from `F0` to `F`. Recover the backward choices from `T` to `G`, reverse their order, and append them to the prefix. Replay the whole sequence from `F0` using a separate checker. A suffix conclusion may already be known; either retain the valid redundant application and its cost or remove it and recompute the actual cost. Never report the unverified sum `g_F+g_B` after silently dropping steps.

**Independent checker.** For every step, look up the frozen rule, check its status and scope, require all premises in the current facts, append the conclusion and accumulate the actual cost. At the end require `T ⊆ facts` and output the exact assumption set, library hash, rule sequence, cost and checker result. The checker should not call the search function or accept a claimed meeting as proof.

Checking this sequence verifies Horn-rule application. It does not verify that a manually entered differential inequality is a valid theorem. Such claims need their mathematical derivation and independent review. A future Lean formalization must generate proof objects accepted by Lean's kernel; a JSON `passed` field is not equivalent. Lean FAQ: proof objects [@D011]

### 5. Safe stopping and the exact scope of an optimality claim

The first meeting produces an **incumbent derivation**, not a least-cost certificate. For example, with initial `A`, rules `A⇒T` of cost 9, `A⇒B` of cost 1 and `B⇒T` of cost 1, a generated direct goal can be noticed before the cheaper two-step route. Queue order and a visual meeting are insufficient.

Use this baseline certification strategy:

1. Obtain any fully replayed bidirectional candidate of actual cost `U`.
2. Independently run forward uniform-cost search over exact fact sets using S2, seeded at `F0`.
3. Ignore stale heap records. When a goal state is popped, its cost is minimal among all admissible rule-application sequences in this finite library.
4. Alternatively, if every remaining heap key is at least the already checked incumbent cost `U`, terminate and certify `U` minimal. Nonnegative extensions cannot produce a cheaper goal.
5. If a cheaper goal is found, replace the incumbent and retain the earlier meeting as a useful nonoptimal trace.
6. If the heap exhausts without reaching the target, report **not derivable in this finite rule library**. This is not a proof that the physical target is false or impossible.

There are at most `2^|A|` exact sets in either state representation. Positive integer costs and finite state/rule sets ensure baseline termination with exact duplicate detection. This worst-case bound is large: use a deliberately small reviewed library first. Shared lemmas make proof costs different from adding independent single-goal costs; a heuristic that sums overlapping subgoal estimates can overestimate. Keep `h=0` until any nonzero heuristic has an actual admissibility argument for these states.

Do not use an unproved `min(frontier_F)+min(frontier_B) ≥ U` stopping condition for this mixed representation. Do not claim MM midpoint guarantees, NBS expansion bounds or optimality over every possible mathematical proof. NBS's near-optimal node-expansion result is a carefully defined result for its specified search model, not a license to transfer the label to a new planner. Chen et al., 2017 [@D009]

### 8. The full-theory target must remain blocked

Use an explicit unresolved target such as `controlled_semiclassical_Einstein_QED_prediction`. Its backward work-plan obligations include a common covariant current/stress renormalization, defined quantum state and causal response, a gauge-fixed gravitational initial-value formulation with controlled higher-derivative treatment, appropriate stress/current noise or a stated validity criterion, constraint-compatible initial data, and controlled regulator removal in observables and evolution.

Do not register a rule saying that this list automatically implies a complete theory of nature. It is a **research decomposition**, not yet a proved sufficient theorem. The finite model has no admission rule from `selected_target` to any of those continuum or curved-space obligations. Return the blocked subgoals and the missing inference certificates. “No path in this library” accurately exposes the next research work.

For later candidates, distinction among proof, conditional prediction and conjecture stays mandatory. Festina Lente and the Weak Gravity Conjecture are not axioms of established QED. A proposed inner-horizon mechanism must specify the state and renormalized stress tensor before classical mass-inflation theorems can be compared with it. Photon–graviton mixing in a prescribed background does not itself supply semiclassical gravitational backreaction. These distinctions constrain which edges the larger map can admit.

### 9. Acceptance tests that attack logical failures

| Test | Expected behavior |
|---|---|
| Missing conjunct | With `A∧B⇒T` and only `A`, no proof of `T` |
| Reverse implication trap | With `A⇒B` and seed `B`, no proof of `A` |
| First-meeting trap | Direct cost-9 route is replaced/certified against the cost-2 route |
| Shared premise | A derived lemma reused by two rules is not unnecessarily charged as two independent proofs |
| Cyclic support | `A⇒B`, `B⇒A` with neither seeded derives neither |
| Rule replay mutation | Deleting a required step or changing its conclusion makes the checker reject |
| Scope mutation | Replacing a finite-mode conclusion with a continuum conclusion fails validation |
| Conjecture laundering | A conjecture cannot become an exact-proof seed without an explicit retained conditional assumption |
| Zero-energy edge | S6 handles `W(0)=0` without division by zero |
| Nonpositive margin | `μ≤0` blocks this sufficient proof route; it is not labeled blow-up or physical instability |
| Unphysical norm/weights | `|r_i(0)|>1`, negative weights or zero masses invalidate the corresponding coercivity/regularity premises |
| Finite-time quantifier | A claim of global existence never silently becomes a uniform-in-time stability statement |
| Unknown atom/rule | Malformed references or missing review certificates are rejected before search |
| Resource limit | Interrupted search is `incomplete`, distinct from exhausted-library non-derivability |
| Library revision | An older rule sequence cannot be called verified against a new hash without replay |

The delivered trace is an auditable account of assumptions, applications, failed branches and checks. It is not hidden internal reasoning and is not a substitute for the mathematical proofs referenced by its rules.

### 10. Advisor execution protocol

Freeze the target and its quantifiers. Confirm the equations and signs independently. Build the smallest admitted-rule library needed for one theorem. Run reachability saturation, bidirectional candidate search, independent replay and forward optimality certification. Have a separate mathematical reviewer attack each inference and the coercivity edge cases. Only then add the accepted theorem node and its exact assumptions to the broader research map.

For an unresolved bridge, output a proposed lemma with its precise hypotheses, a potential counterexample and an experiment or proof obligation that could decide it. The advisor may generate candidate rules but may not mark their proofs checked. Feedback-guided theorem agents such as COPRA similarly execute proposed tactics in a proof environment rather than accepting text alone. Thakur et al., 2023 [@D013] Our implementation currently certifies the finite planning trace; formal verification of the analytical theorem would require a separate Lean/Isabelle/Rocq development.


## Executed proof route and validation record

These are results from the supplied code, not an illustrative invented search. The selected-regulator scenario starts from the parameter, state, drive and imported mathematical assumptions. It does not assume the positive margin that it seeks to derive. All outputs preserve the finite-model scope.

### Accepted search route

| Step | Reviewed rule | New conclusion |
|---|---|---|
| 1 | PM01 | `finite_parameter_certificate` |
| 2 | PM02 | `positive_margin` |
| 3 | R01 | `Zpositive` |
| 4 | R02 | `norm` |
| 5 | R03 | `regular_rhs` |
| 6 | R04 | `localwellposed` |
| 7 | R05 | `energyidentity` |
| 8 | R06 | `Upositive` |
| 9 | R07 | `energybound` |
| 10 | R08 | `compacttrajectory` |
| 11 | R09 | `globalwellposed` |
| 12 | R10 | `smoothflow` |
| 13 | R11 | `causal_tangent` |
| 14 | R12 | `selected_theorem` |

The genuine intermediate meeting has forward cost **8** and backward suffix cost **6**. At that meeting, the backward goals are a subset of the forward facts. The checked combined route costs **14**. Independent forward uniform-cost certification popped **24** states; the bidirectional phase popped **548** backward states. These are counts of algorithm states, not physical degrees of freedom.

At the meeting, the forward side has already established the parameter certificate, positive margin, regular vector field, local solution, invariant norms, work identity and positive/coercive energy. The backward side has reduced the target to those facts plus the retained model, drive and ODE assumptions. It then replays the field bound, finite-time compactness, continuation, smooth dependence and conditional causal support. Every required premise is retained.

The generic margin-assumed theorem has certified cost 12; the isolated margin calculation has cost 2. The full selected-regulator route joins those calculations in one actual scenario. Costs apply only to the supplied reviewed rule library. The search did not invent or symbolically prove the ODE theorems referenced by its rules.

### Executed checks

| Check family | Executed result | Meaning |
|---|---|---|
| Root symbolic algebra | 16/16 passed | Exact identities, including deliberately omitted quotient and wrong constraint coefficient |
| Independent mathematical critic | 24/24 passed | Algebra, rational bounds and explicit failed generalizations |
| Planner regression suite | 24/24 passed | Conjunction, scope, assumption retention, immutable certificates, costs and limits |
| Independent search review | 19/19 gates passed | Includes 64 independently enumerated small-library cost comparisons |
| Rounded coefficient certificate | Exact rational comparison passed | Display-only global lower bound 0.7653173589206453 exceeds 3/4 |
| Continuum or gravitational closure | Not established | Not converted into a passing gate or an assumed proof edge |

Some independent algebraic checks intentionally overlap. Adding their counts does not measure confidence or create a larger theorem. Source hashes in the raw logs tie each execution to its actual code and fixture. The rational-coefficient check certifies a nearby exact finite model defined by rounded inputs, not the numerical time trajectory.

### Defects found and corrected during this run

| Defect | Why it mattered | Accepted correction |
|---|---|---|
| Forward solve completed before backward search | The supposed two-front result immediately met at the original target | Alternate actual frontiers; retain an intermediate meet and separate optimality certificate |
| Parameter-margin fixture was isolated | The full theorem still used an unexplained margin seed | Add an integrated selected-constants-to-theorem scenario |
| Hidden assumption metadata and unverified seeds | A route could appear exact while depending on an undisclosed conjecture | Require retained seed dependencies, safe theorem verification and inherited assumptions |
| Mutable library after hash creation | Costs or rules could change while the old hash remained attached | Immutable mappings plus hash recomputation at planning and replay |
| Causal-support statement lacked its comparison condition | Varying initial data may produce pre-probe response | State identical preparation/source histories and zero initial tangent explicitly |

Initial findings are preserved separately. One early inline metadata probe did not retain its own source hash; its provenance is identified as a contemporaneous observation, not retroactively presented as a reproducible failing test. The later regression tests and final independent review are reproducible.

### Evidence limits and next proof frontier

The analytical proof is a reviewed conventional argument, supported by exact checks. It has not been translated into a proof-assistant kernel. The strongest accepted mathematical claim is the finite-model theorem under its displayed assumptions, together with the separate conditional Bianchi identity. No numerical horizon resolution, cosmological solution, quantum-noise calculation, continuum limit or proof of WGC/FL is hidden in the reported success status.

The next frontier consists of concrete obligations: a common renormalized quantum current and directional stress, their force Ward identity, regulator-uniform estimates where a continuum claim is intended, and consistent total constrained gravitational data. The supplied solver prompt keeps these obligations explicit.


## The next bridge: conserved stress before dynamical gravity

### What must be connected, and what is only a common framework

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

The action connects subjects by shared variables. It does not prove that the Weak Gravity Conjecture, Festina Lente, cosmic censorship or singularity resolution follows from these operators. A charge-to-mass statement needs charge normalization, Planck convention, scalar forces and spacetime assumptions before it becomes a proposition. \(q/m\ge1\) alone is not a dimensionally universal axiom. The repulsive-force and black-hole-extremality versions require separate hypotheses. Repulsive Forces and the Weak Gravity Conjecture [@D018], Festina Lente [@D019].

Strong fields and curvature require another distinction. A local low-order Euler–Heisenberg polynomial is not uniformly justified when \(eE/m^2\sim1\), \(eB/m^2\gg1\), or curvature and derivative scales approach \(m^2\). A static real susceptibility is not the nonlocal retarded current of a pair-producing state. In a region of a source-free classical Einstein–Maxwell solution with zero cosmological constant, \(R=0\) even though the Riemann tensor can be large; Ricci scalar alone is therefore a poor curvature-validity test. A magnetar's strong magnetic field does not by itself imply electron-Compton-scale curvature. The appropriate checks involve field invariants, independent curvature components/invariants, frequencies, gradients, quantum state and approximation order.

For causal quantum feedback, the target object is a renormalized closed-time-path effective action \(\Gamma_{\rm CTP}[g^+,A^+;g^-,A^-;\omega_0]\), or an equivalent in-in construction. Its physical-branch variations must define a compatible current and stress tensor. A formal symbol \(\langle T_{\mu\nu}\rangle_{\rm ren}\) is not a closure until the state, subtraction, finite counterterms and evolution are supplied. If higher-curvature terms are retained, their metric variations must also enter the gravitational equations, or an explicit order-reduction prescription must replace them. G2–G9 below apply to the ordinary Einstein equations, or to a formulation where all additional contributions have consistently been moved into the conserved total source.

### A completed conditional interface lemma

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

### Source audit: a theorem's domain travels with its citation

Zahn's locally covariant Dirac construction is relevant background, but section 4.2 explicitly treats constant mass and a gauge connection of vanishing curvature for its stated nonperturbative stress argument, with a perturbative background alternative discussed. It must not be cited as our already implemented strong-electromagnetic-field stress closure. For nonzero field strength the charged-matter force Ward identity must include electromagnetic work. The arXiv v3 is dated 18 October 2013; a recent HTML conversion timestamp does not create a new research revision. Zahn, section 4.2 [@D014].

Meda, Pinamonti and Siemssen prove a local existence and uniqueness result for a specified scalar-field cosmology using a retarded inverse and a fixed-point construction. Their Theorem 5.9 requires compatible sufficiently regular state data; Remark 5.2 explains the mild-solution regularity and the additional requirements for a fourth derivative of the scale factor. This is a useful proof strategy to study, not a theorem for our charged Dirac Bianchi-I problem. Theorem 5.9 and Remark 5.2 [@D015].

The earlier Pinamonti–Siemssen result extends a particular conformally coupled scalar cosmology until its specified singular boundary. The word “global” in its title does not establish singularity-free evolution for arbitrary semiclassical matter or geometry. Only the abstract and bibliographic scope were checked in this round. Original record [@D016].

Stochastic-gravity validity also involves intrinsic and induced fluctuations. A bounded mean trajectory or a finite-time source derivative does not evaluate the symmetrized current/stress noise kernel. This remains a separate bridge. Verdaguer [@D017].

### Next obligations, with falsifiers and stopping rules

| Obligation | Constructive next step | Acceptance evidence | Failure that blocks promotion |
|---|---|---|---|
| Regulator limit | Specify a physical state family and a topology for renormalized current and energy; vary longitudinal window and Landau cutoff separately | Uniform bounds and a Cauchy/compactness argument, with counterterms tracked | Quadrature refinement alone or cutoff-dependent coercivity treated as a continuum theorem |
| Differentiate the limit | Establish uniform control of the variational kernel and justify limit–derivative interchange | A domination or operator-convergence theorem on fixed finite intervals | Pointwise convergence of trajectories without derivative control |
| Covariant stress | Construct current and both pressures in the same state and renormalization scheme | Flat matched limit, force Ward identity, finite-counterterm bookkeeping and independent residuals | Energy-only closure, mismatched subtraction, or conservation imposed by definition without testing the calculated observables |
| Gravity support | Include apparatus work/stress or formulate a closed system with admissible constrained initial data | G8 with independently computed total Q and initial constraint | An external current with its energy omitted |
| Noise and stability | Define smeared current/stress two-point observables and separate intrinsic from induced response | State-dependent finite observables and justified validity criterion | A pole in response divided by a zero field, or signed tangent work called a positive norm |
| Curved strong-field dynamics | Choose a regular short-time Bianchi interval and a controlled quantum closure before horizons | Local existence assumptions, constraint propagation and approximation error bounds | Inserting a flat fixed-B susceptibility into arbitrary curvature without a derivation |

The next selected scientific milestone is the covariant current/pressure Ward identity in a precisely specified charged-field state. G7 is now a completed conditional endpoint for that bridge: once the actual total source satisfies its premises, constraint propagation follows. Neither search directions nor agent agreement can replace the missing source construction.


## Solver specification for the next audited research cycle

### Role and evidence contract

You are the mathematical research advisor for the attached finite Maxwell–Dirac theorem and its semiclassical-gravity frontier. Use the exact model and source hashes supplied in this package. Separate conventional proof, formal proof-assistant verification, symbolic identity checks, numerical experiments, physical assumptions and conjectures in every result. Give definitions, derivations, cited theorem hypotheses and falsifiers; private deliberation is not an evidence artifact. Do not claim a new physical theorem because a search graph reaches a target.

Read theorem_advisor.md, proof_critique.md, research_bridge.md, theory_map.json, search_contract.md and the recorded verification results before proposing a modification. Do not overwrite historical round-3/round-4 evidence. Freeze any new model version separately. Keep the proposal author, mathematical critic and implementation verifier in separate bounded roles. A critic may reject a bridge even when every existing test passes.

### A. Audit the completed finite theorem

1. Restate T1–T4, including fixed positive masses/weights, physical Bloch data, continuous drive and a uniform positive denominator. Specify dimensionless time s=mt, potential a=eA_z/m, electric field x=eE_z/m² and magnetic field b=|eB|/m². State that the regulator is fixed and spatially homogeneous. No artificial radial boundary conditions are permitted.
2. Re-derive T8–T11 from the vector equations. Check state positivity, U≥0, the sign of C′, and the cancellation in W′=xF. Locate exactly where every assumption is used.
3. Prove the field estimate using sqrt(W+epsilon), including W0=0 and sign-changing drives. Bound a on every finite interval, invoke the compact continuation theorem with its hypotheses, and distinguish all finite times from uniform all-time bounds on the complete state.
4. Derive T16–T21 from the digamma recurrence, Binet integral, positive exact quadrature, mass bounds and a stated alpha inequality. Verify the strict rational comparison without decimal approximation. Recheck the separate rounded-coefficient model if its source hash differs. Do not treat it as an interval enclosure of a floating trajectory.
5. Derive every tangent term in T24, especially the positive e² deltaC x′ quotient term. State joint parameter regularity, fixed regulator and admissible nearby initial data. Derive Duhamel's formula and its retarded support. Keep the initial variation term if it is nonzero. Do not infer all-time stability from T26 or from signed deltaW.
6. Attempt the supplied counterexamples before proposing a stronger theorem: Z degeneracy, unphysical Bloch norm, negative weights, zero mass, mixed-state norm-changing variation, divergent continuum energy and bounded solutions with unbounded parameter derivative.

### B. Use bidirectional search as an obligation organizer

Freeze a finite rule library with exact scope and version metadata. Forward application requires every premise. Backward application replaces a conclusion goal by the rule's sufficient premises, retaining every other pending goal. A meet is a subset check between backward obligations and forward facts. Replay the forward prefix and reversed backward suffix independently before accepting a candidate.

Use h=0 until an admissible heuristic for this exact AND/OR representation has been proved. Record actual expansions in both directions. A first meet is an incumbent, not an optimality proof. Certify least cost separately by forward uniform-cost search within the supplied library. Report the finite-library hash and limits. The full continuum/gravity goal has no reviewed bridge and must remain blocked. Do not turn a blocked target into a seed or turn an empirical fit into an exact theorem node.

Run the selected-parameter scenario in which the margin is derived, then the complete finite theorem, rather than demonstrating those routes in disconnected fixtures. Also run deliberately malformed libraries: missing conjunct, reversed implication, scope change, unretained conjecture, wrong time quantifier and changed certificate. Preserve honest incomplete/not-derivable distinctions under resource exhaustion.

### C. Select one next analytical target

Primary target: formulate and verify a compatible renormalized quantum current and both directional pressures in an explicitly specified homogeneous axisymmetric charged-field state. Begin on a prescribed regular metric interval; do not simultaneously add black-hole horizons, dipole geometry, dynamical moduli and higher-derivative gravity. State what simplification is made and which original mechanism it retains.

Required objects are Jq, rhoq, pperp,q and pparallel,q. Specify charge normalization, mode degeneracy, state construction, ultraviolet regulator, local subtractions and allowed finite counterterms. Show how flat constant-B observables reduce to the matched model or identify a concrete mismatch. The required energy-force Ward identity is

\[
\dot\rho_q+2H_\perp(\rho_q+p_{\perp,q})
+H_\parallel(\rho_q+p_{\parallel,q})=EJ_q.
\]

Independently calculate the left and right sides. Defining one pressure algebraically to force this identity is insufficient physical validation. Audit the hypotheses of every cited curved-QFT stress theorem; Zahn section 4.2 is not a blanket nonperturbative strong-F closure.

Use G2–G9 as the gravitational interface. Derive G7 and G8 again without imposing the constraint early. If a prescribed electric drive is retained, include its work and stress in a support sector. If fixed B is retained during expansion, supply the mechanism modifying the source-free magnetic evolution. Initial metric data must satisfy the time-time constraint. Positive scale factors and regularity are interval assumptions, not proved absence of a future singularity.

### D. Computation after closure, with explicit acceptance gates

Use open-source SymPy for exact identities and rational arithmetic for coefficient certificates. Use SciPy DOP853 or an independently implemented embedded Runge–Kutta method for a genuinely closed finite ODE. A symplectic or spin-rotation update may improve norm preservation, but it must be shown to integrate the coupled model at the claimed order. Do not propose a PINN as a proof substitute or discretize undefined renormalized observables.

For a new solver, deliver a single runnable command, pinned dependencies, dimensions/order of every state array, exact parameter file and machine-readable results. Separate time-step/tolerance convergence from momentum quadrature convergence, momentum-window changes and Landau-cutoff changes. Compute independent norm, Maxwell-current, work and total-constraint residuals. Report absolute response at field zeros. Track conservation error against the analytically predicted Ward-defect integral G8. Include zero-drive, zero-source-variation, pre-probe causality and deliberate wrong-sign tests.

If a cutoff limit is claimed, supply a mathematical state family and uniform estimates before extrapolating. If a quantum validity claim is made, define smeared noise observables and compute them; a mean-field tangent is not their replacement. If a theorem is formalized in Lean or Isabelle, provide the full proof file, exact dependency versions and executed kernel output. Otherwise retain the conventional-proof label.

### E. Required research handoff

Return: one precise accepted or rejected proposition; its complete assumptions and equations; forward lemmas and backward obligations; source locations and reading depth; executed code and raw results; failed alternatives with concrete counterexamples; a changed-assumption ledger; and the smallest remaining bridge. Separate newly derived results from reproductions of standard theory. A missing continuum/stress lemma is an unfinished scientific task, not permission to declare the large theory solved.
