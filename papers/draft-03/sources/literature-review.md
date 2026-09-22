# Selected literature and contribution audit

The workbench is best presented as a **research compendium draft**. It contains calculations and certificates for several explicitly different models, plus scope checks on proposed continuations. This review establishes relevant prior methods and comparison points. It does **not** establish scientific novelty, exhaust the literature, or certify a continuum Yang–Mills construction.

The strongest candidate contribution is the collection of fully specified graph calculations, Gram identities, complete residual budgets, endpoint estimates, and inspectable certificates. The usual machinery—Haar integration, representation theory, single-plaquette reduction, min–max/Temple estimates, perturbative product-phase stability, local block diagonalization, and Lieb–Robinson comparison—is established. “New to this workbench” should not be rewritten as “new to the literature.”

A useful eventual split could isolate (i) finite-graph SU(2) certificates, (ii) fixed-spacing endpoint dynamics and computed heat evaluation, and (iii) a reproducibility/method appendix. That is an editorial option, not a conclusion about publishability.

The focused set now contains **24 references**, including three QED sources added during early-section integration.

## Reading method and limits

Primary research papers, an official problem statement, author-hosted mathematical exposition, and an official special-function reference were inspected online on 22 September 2026. The two historical primary sources serve only a short method note. Exact locations below record what was actually read; they do not imply full proof verification. The Kogut–Susskind original body was not accessible in this tool. The original Osterwalder–Schrader II article was read through a PDF mirror. Bibliographic details use the published record when verified, while equation locations retain the inspected preprint version.

The historical ledger independently counts **111 stored runs: 35 studies and 76 physics loops, across rounds 3–25**. This agrees with its declared counts. Round 26 is not part of that ledger; no missing early round or extra run is inferred. Counting is a provenance check, not a fresh execution.

## Consequences for manuscript claims

| Manuscript topic | Prior method or result | Defensible workbench relationship |
|---|---|---|
| One square and finite graph | Wilson/Kogut–Susskind formulation; existing Mathieu reduction; classical special functions | Explicit normalization, basis/Gram calculations, rational bounds, and complete omitted-channel accounting on stated graphs |
| Gauge fixing | Established maximal-tree and electric parallel-transport construction | Verify the induced kinetic operator; a factorized Haar measure alone does not determine it |
| Product-phase stability | Qualitative rotor-compatible stability and unbounded-interaction block diagonalization already exist | Match every domain, interaction, and geometry hypothesis; deriving explicit model constants would be additional work |
| Spatial limits and tails | Lieb–Robinson frameworks include unbounded onsite terms; stronger volume-tail results have their own finite-qudit hypotheses | Keep time topology, spatial convergence, support cardinality, and admitted interaction norms separate |
| Truncation and heat evaluation | Existing quantum-number truncation and variational error machinery | A retained block needs a complete residual; a computed centered heat map also needs rounding, center, and normalization budgets |
| Static/stochastic and canonical dynamics | Wilson measures and auxiliary Markov generators are established but carry different clocks | State exactly which operator has the claimed gap; transfer to physical time requires a separate derivation |
| Continuum target | Full reconstruction axioms and the Clay problem | Fixed-spacing statements remain fixed-spacing; no continuum mass-gap claim follows |

## Inspected sources

### 1. `wilson1974confinement` — Confinement of quarks

**Source:** [primary record](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.10.2445); [inspected text](https://hep.physics.uoc.gr/Erasmus-IP-2013/files/lectures/Rabinovici/Wilson.pdf).

**Inspected:** Publisher metadata; original article, abstract and introduction, printed pp. 2445–2446 (PDF pp. 1–2).

**Established method and hypotheses:** Compact lattice links and strong-coupling reasoning are established. The introductory discussion treats the lattice as an ultraviolet cutoff.

**Relationship:** Finite Haar integrations and graph identities should be presented as explicit computations within established lattice theory.

**Limit:** The strong-coupling cutoff model is not by itself a Lorentz-invariant continuum construction; the full expansion was not re-audited.

### 2. `kogut1975hamiltonian` — Hamiltonian formulation of Wilson's lattice gauge theories

**Source:** [primary record](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.11.395).

**Inspected:** Publisher abstract and bibliographic record only; original PDF access redirected to the abstract. Open normalization details were checked in D’Andrea et al. below.

**Established method and hypotheses:** The canonical Hamiltonian formulation uses coupled rigid rotators and non-Abelian electric flux.

**Relationship:** This is the historical Hamiltonian provenance; the workbench must specify its own energy, link, and plaquette normalizations.

**Limit:** Do not imply that the original paper’s body or all domain statements were inspected in this audit.

### 3. `bauer2023basis` — New basis for Hamiltonian SU(2) simulations

**Source:** [primary record](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.109.074501); [inspected text](https://arxiv.org/pdf/2307.11829v1).

**Inspected:** ArXiv v1 §II.B, Eqs. (54)–(56), PDF p. 7; Appendix B, Eqs. (B4)–(B10), PDF p. 24; publisher metadata.

**Established method and hypotheses:** The source displays H_E=g²ΣE²/(2a), H_B=ΣTr(2I−P−P†)/(2g²a), and a physical single-plaquette radial problem reducible to Mathieu functions.

**Relationship:** Single-square reduction and representation methods are prior tools. Graph-specific certified enclosures and fully enumerated residual arithmetic are candidate workbench contributions.

**Limit:** Match normalization and boundary conditions. ArXiv v1 had a different author order and the title “A new basis…”; the agreed bibliography key is retained.

### 4. `burbano2024gauge` — Gauge Loop-String-Hadron Formulation on General Graphs and Applications to Fully Gauge Fixed Hamiltonian Lattice Gauge Theory

**Source:** [primary record](https://arxiv.org/abs/2409.13812); [inspected text](https://arxiv.org/html/2409.13812v2).

**Inspected:** Appendix C introduction, §C3.2, and §C4.1, especially Eqs. (275)–(291).

**Established method and hypotheses:** Maximal-tree reduction separates kinematics from dynamics. The electric generator transforms with parallel transport; intertwining the Hamiltonian is an additional requirement beyond identifying configurations.

**Relationship:** A Haar-factorized coordinate system does not alone establish a product kinetic operator. Workbench cross-derivative terms need their own graph calculation.

**Limit:** The inspected portions do not replace a closed-domain proof for every reduced unbounded generator.

### 5. `yarotsky2004quasiparticles` — Quasi-particles in weak perturbations of non-interacting quantum lattice systems

**Source:** [primary record](https://arxiv.org/abs/math-ph/0411042); [inspected text](https://arxiv.org/pdf/math-ph/0411042).

**Inspected:** Setup and Theorem 1, PDF pp. 2–3.

**Established method and hypotheses:** Possibly infinite-dimensional sites have nonnegative self-adjoint onsite operators, a unique zero-energy vacuum, and a gap at least one. Bounded perturbations have a fixed finite support shape and sufficiently small uniform norm.

**Relationship:** This supplies qualitative product-phase stability after an explicit model dictionary, including interaction blocking.

**Limit:** Smallness constants depend on the interaction geometry and are not numerically evaluated here. This citation cannot certify a particular workbench coupling.

### 6. `henheik2022local` — Local stability of ground states in locally gapped and weakly interacting quantum spin systems

**Source:** [primary record](https://arxiv.org/abs/2106.13780); [inspected text](https://arxiv.org/html/2106.13780v3).

**Inspected:** §2, Definitions 1–2 and Theorem 3; introduction on the relation to Yarotsky.

**Established method and hypotheses:** Unique gapped onsite ground states and sufficiently weak bounded finite-range interactions give exponentially small distant ground-state effects of a local perturbation with relative bound below one. Infinite onsite dimension is allowed.

**Relationship:** Supports a carefully matched local-stability comparison, not an unqualified import of a numerical threshold.

**Limit:** The local perturbation can close the perturbed global gap. Theorem 3 is a locality statement about ground states, not a gap-preservation theorem for arbitrary local perturbations.

### 7. `bravyi2008polynomial` — Polynomial-time algorithm for simulation of weakly interacting quantum spin systems

**Source:** [primary record](https://arxiv.org/abs/0707.1894); [inspected text](https://arxiv.org/pdf/0707.1894).

**Inspected:** §1, PDF pp. 3–5, Eqs. (1)–(6), Theorems 1–3.

**Established method and hypotheses:** Qubits on a bounded-degree graph have onsite gaps at least Δ and two-qubit interactions bounded by J. The stated explicit perturbative scale is ε₀=2⁻¹⁸Δ/(dJ).

**Relationship:** Shows that explicit weak-interaction algorithms and thresholds are established in their stated setting.

**Limit:** The qubit/two-site theorem does not automatically cover infinite-dimensional SU(2) factors or arbitrary block interactions. This is not the later Schrieffer–Wolff paper.

### 8. `delvecchio2022local` — Local iterative block-diagonalization of gapped Hamiltonians: a new tool in singular perturbation theory

**Source:** [primary record](https://arxiv.org/abs/2007.07667); [inspected text](https://arxiv.org/pdf/2007.07667).

**Inspected:** ArXiv v2 §§1.1–1.2, PDF pp. 2–4; Theorem 5.3, PDF p. 41.

**Established method and hypotheses:** Finite onsite dimension, unique onsite vacuum with gap at least one, and bounded finite-range rectangular interactions yield a volume-independent small-coupling gap.

**Relationship:** Local block diagonalization and support bookkeeping are existing methods; a fully explicit model-specific numerical closure would require additional work.

**Limit:** This particular formulation is finite dimensional, but it must be read together with the broader unbounded-interaction result below.

### 9. `delvecchio2021unbounded` — Block-diagonalization of infinite-volume lattice Hamiltonians with unbounded interactions

**Source:** [primary record](https://arxiv.org/abs/2108.13907); [inspected text](https://arxiv.org/pdf/2108.13907).

**Inspected:** §§1.1–1.2, PDF pp. 3–5, Eqs. (1.3), (1.6)–(1.11); statement of Theorem 2.10, PDF p. 12.

**Established method and hypotheses:** Separable onsite spaces and unique gapped vacua are allowed. Finite-range symmetric interactions obey uniform local relative-form bounds, with the stated domain conditions or quadratic-form variant. A volume-independent sufficiently small coupling gives a gap.

**Relationship:** This is a relevant existing route for rotor-type spaces. The workbench must match domains, geometry, weighted norms, and quantitative constants.

**Limit:** No blanket claim that block-diagonalization literature excludes unbounded onsite systems is justified. Full inductive estimates and a numerical translated threshold were not audited.

### 10. `nachtergaele2014dynamics` — On the dynamics of lattice systems with unbounded on-site terms in the Hamiltonian

**Source:** [primary record](https://arxiv.org/abs/1410.8174); [inspected text](https://arxiv.org/pdf/1410.8174).

**Inspected:** §2, PDF pp. 2–6, including Proposition 2.1; §3, Theorem 3.1; finite-volume comparison around Eqs. (83)–(88).

**Established method and hypotheses:** Self-adjoint onsite terms on separable spaces coexist with bounded intersite interactions having finite F-norm. F is uniformly summable and has a finite convolution constant. Interaction-picture calculus controls local dynamics.

**Relationship:** Provides a framework for the workbench’s spatial limits and locality bounds with unbounded onsite kinetic energy.

**Limit:** Spatial norm convergence on compact time intervals does not establish norm continuity in time on the full local bounded-operator algebra. Commutator limits need domain/topology control.

### 11. `mcdonough2025volume` — Lieb--Robinson bounds with exponential-in-volume tails

**Source:** [primary record](https://arxiv.org/abs/2502.02652); [inspected text](https://arxiv.org/html/2502.02652v2).

**Inspected:** Abstract; Definitions 3.1–3.4 and introductory presentation of Theorem 3.6.

**Established method and hypotheses:** The inspected setup uses finite-dimensional qudits, a finite factor graph, controlled few-body interactions, and specified volume/boundary growth of graph balls.

**Relationship:** A prospective lead for stronger support-cardinality tails than a filled collar with only radius decay.

**Limit:** An adaptation to infinite-dimensional SU(2) sites was not established, and the full proof was not audited. The workbench may not treat the source as an already admitted cardinality-norm theorem.

### 12. `tong2022simulation` — Provably accurate simulation of gauge theories and bosonic systems

**Source:** [primary record](https://arxiv.org/abs/2110.06942); [inspected text](https://arxiv.org/html/2110.06942v2).

**Inspected:** Appendix B, Eq. (24), and Appendix D, Theorem 6, Eqs. (62)–(67); the project’s earlier §2 reading is recorded separately.

**Established method and hypotheses:** A controlled local quantum number changes by at most one under H_W; its cutoff norm grows as (Λ+1)^r with r<1. H_R preserves that number, and the initial state has a specified cutoff.

**Relationship:** Existing truncation theory distinguishes state tails from truncated Hamiltonian dynamics. Workbench retained blocks need their own complete leakage/error dictionary.

**Limit:** This is a fixed-spacing real-time result for its stated truncations and initial states, not an arbitrary Ritz-subspace or uniform all-time computed-heat theorem.

### 13. `teschl2014methods` — Mathematical Methods in Quantum Mechanics: With Applications to Schr"odinger Operators

**Source:** [primary record](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe2.pdf).

**Inspected:** §4.4, Corollary 4.13 and Theorem 4.14, printed p. 141; §4.5, Theorem 4.16, p. 142; §6.1, Theorem 6.4 and Lemma 6.5, p. 159.

**Established method and hypotheses:** Min–max and Temple bounds require the stated spectral separation and full-operator residual for a normalized domain vector. Kato–Rellich requires relative bound below one; the resolvent identity requires common resolvent points.

**Relationship:** Standard variational and perturbation tools support graph-specific Gram matrices, leakage bounds, rational enclosures, and resolvent estimates.

**Limit:** A compressed residual alone is insufficient; the correct Hilbert-space Gram and omitted channels matter. This is an author-hosted mathematical reference, not a claim of priority for the classical theorems.

### 14. `shen2022strong` — A stochastic analysis approach to lattice Yang--Mills at strong coupling

**Source:** [primary record](https://arxiv.org/abs/2204.12737); [inspected text](https://arxiv.org/pdf/2204.12737).

**Inspected:** §§1.1–1.2, PDF pp. 3–7, Assumption 1.1, Theorems 1.2 and 1.4, Corollary 1.6.

**Established method and hypotheses:** For unit-spacing Wilson measures, the SU(N) condition K_S=(N+2)/2−1−8N|β|(d−1)>0 controls the strong-coupling stochastic analysis and spatial covariance decay.

**Relationship:** Useful context for reversible stochastic generators and static conditional measures; their clocks must be identified explicitly.

**Limit:** The source’s Euclidean spatial mass-gap statement and auxiliary Langevin gap are not automatically the physical-time Kogut–Susskind gap or a continuum mass gap.

### 15. `osterwalder1975axioms` — Axioms for Euclidean Green's functions. II

**Source:** [primary record](https://projecteuclid.org/journals/communications-in-mathematical-physics/volume-42/issue-3/Axioms-for-Euclidean-Greens-functions-II-with-an-Appendix-by/cmp/1103899050.pdf); [inspected text](https://scispace.com/pdf/axioms-for-euclidean-green-s-functions-ii-with-an-appendix-4g1guiqrrx.pdf).

**Inspected:** Introduction, printed pp. 281–282; §III, p. 285; §IV.1 and opening of §IV.2, pp. 287–288.

**Established method and hypotheses:** The corrected reconstruction statement needs suitable regularity/growth, Euclidean covariance, reflection positivity, symmetry, and clustering of the Schwinger-function hierarchy. The introduction corrects a gap in the 1973 argument.

**Relationship:** This supplies the target-level reconstruction checklist for any proposed continuum hierarchy.

**Limit:** Reflection positivity or a finite positive measure alone does not meet the full hypotheses. Original text was inspected via a mirror; the official PDF was not accessible through this tool.

### 16. `jaffe_witten` — Quantum Yang--Mills Theory

**Source:** [primary record](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).

**Inspected:** §§3–5, PDF pp. 5–6, and opening of §6, p. 7.

**Established method and hypotheses:** The target is a nontrivial quantum Yang–Mills theory on four-dimensional space for a compact simple group, satisfying suitable axioms and possessing a strictly positive physical mass gap.

**Relationship:** Provides the boundary between finite-graph, fixed-spacing, infinite-volume, and continuum statements.

**Limit:** No finite matrix, numerical level difference, auxiliary stochastic clock, or inhomogeneous fixed-spacing endpoint proves this target.

### 17. `chatterjee2026lattice` — Exact Lattice Identities and Continuum-Limit Dyson--Schwinger Equations for Yang--Mills Theory

**Source:** [primary record](https://arxiv.org/abs/2608.05415); [inspected text](https://arxiv.org/html/2608.05415v1).

**Inspected:** Selected portions of §§III–V, Eqs. (9)–(19), the formal continuum discussion, and the scalar-ansatz discussion.

**Established method and hypotheses:** Exact lattice Haar identities, formal continuum expansions, gauge-variant source choices, and closure ansätze have distinct evidentiary status.

**Relationship:** The historical round-12 workbench audit compares particular displayed formulas under frozen conventions. Cite those local certificates for the exact statement tested.

**Limit:** No new reproduction was run here. Match the historical source bytes/version before asserting a present-paper error; neither the ansatz nor its audit supplies a Yang–Mills existence theorem.

### 18. `nistDLMFGegenbauer` — DLMF, Chapter 18, §18.5(iii), Equation 18.5.10: Ultraspherical (Gegenbauer) polynomials

**Source:** [primary record](https://dlmf.nist.gov/18.5.E10).

**Inspected:** §18.5(iii), Eq. (18.5.10), explicit finite-sum representation.

**Established method and hypotheses:** The Gegenbauer finite-sum formula gives C₃²(x)=32x³−12x and C₅²(x)=192x⁵−160x³+24x.

**Relationship:** The workbench’s monic polynomials are rescalings of a classical family. Model-specific response coefficients and proof certificates remain separate computations.

**Limit:** Do not describe these polynomials or their orthogonality family as newly discovered. This is an official special-function reference, not an original historical paper.

### 19. `newton_opticks` — Opticks: or, A Treatise of the Reflexions, Refractions, Inflexions and Colours of Light

**Source:** [primary record](https://www.gutenberg.org/files/33504/33504-h/33504-h.htm).

**Inspected:** Title page; Book III, Query 31, printed pp. 404–405.

**Established method and hypotheses:** Newton describes analysis from experiments and observed effects, followed by synthesis from established principles.

**Relationship:** A short historical method analogy for forward derivation and reverse identifiability checks.

**Limit:** No authority claim: this passage proves no modern quantum theorem and fixes no workbench numerical coefficient.

### 20. `tesla1905patent` — Art of transmitting electrical energy through the natural mediums

**Source:** [primary record](https://patents.google.com/patent/US787412A/en).

**Inspected:** Bibliographic header and the specification’s three numbered operating conditions, paragraphs beginning “First,” “Second,” and “Third.”

**Established method and hypotheses:** The patent sets out geometric, excitation-frequency, and duration conditions for a proposed electrical-transmission mechanism.

**Relationship:** A short method analogy for specifying boundary conditions, a driver, and retained or omitted channels.

**Limit:** A patent specification is not modern experimental validation, an SU(2) result, or evidence for a numerical resonance law in this workbench.

### 21. `froland2025two` — Simulating Fully Gauge-Fixed SU(2) Hamiltonian Dynamics on Digital Quantum Computers

**Source:** [primary record](https://arxiv.org/abs/2512.22782); [inspected text](https://arxiv.org/html/2512.22782v1).

**Inspected:** §II.1, Eq. (1); §II.2, Eq. (22), §II.2.3; Appendix C, Table 4; metadata checked against the round-11 source record.

**Established method and hypotheses:** The seven-link open two-plaquette model and its strong-coupling electric spectrum are prior comparisons. Table 4 lists levels 0, 3g²/2, 9g²/4, 13g²/4, and 4g².

**Relationship:** The workbench reproduces these levels after matching its electric normalization. Its explicit trace-coordinate calculations and certificates must be distinguished from discovering the listed spectrum.

**Limit:** The electric-only levels do not certify the full finite-coupling gap. Different tree conventions preclude unchecked termwise generator identification. Hardware/FEM claims were not reproduced; the displayed manuscript date differs from the abstract’s v1 submission date.

### 22. `mages2010euler` — Euler--Heisenberg Lagrangian to all orders in the magnetic field and the Chiral Magnetic Effect

**Source:** [primary record](https://arxiv.org/abs/1009.1495); [inspected text](https://arxiv.org/html/1009.1495v1).

**Inspected:** Fresh reading of §2, Eqs. (11)–(18), especially (13)–(17), and constant-field limitation in the introduction; compared with historical FT02 in evidence/qeg-research/round3/references.json.

**Established method and hypotheses:** The one-loop proper-time calculation treats constant fields, all orders in magnetic strength, and second order in the electric probe. Its finite subtraction convention is explicitly chosen.

**Relationship:** Prior formula provenance for the magnetic-response comparison and susceptibility; the workbench must state its matched field and subtraction conventions.

**Limit:** This is not an arbitrary time-dependent strong-field, pair-production, or curved-spacetime closure. No complete recalculation of the source was performed.

### 23. `kluger1993pair` — Pair production in a strong electric field: an initial value problem in quantum field theory

**Source:** [primary record](https://arxiv.org/abs/hep-ph/0311293); [inspected text](https://arxiv.org/pdf/hep-ph/0311293).

**Inspected:** Fresh reading of initial-state/regularization discussion, PDF pp. 6–7 and 12–14; spinor §3.2, PDF pp. 38–41, Eqs. (3.23)–(3.42). Historical C03 already recorded pp. 6–14 and the spinor-section entry.

**Established method and hypotheses:** Self-consistent pair production is treated in a homogeneous time-dependent electric field within semiclassical mean-field QED. Adiabatic state conditions and current subtraction are part of the initial-value prescription; the spinor current is derived separately.

**Relationship:** Nearest prior formalism for the workbench’s coupled finite current/field closure and adiabatic bookkeeping. Its evaluated finite-mode identities remain local derivations.

**Limit:** A primary-author review, not a proof of exact interacting QED or general Bianchi-I backreaction. Scalar formulas are not automatically spinor formulas; numerical experiments were not reproduced.

### 24. `zahn2014dirac` — The renormalized locally covariant Dirac field

**Source:** [primary record](https://arxiv.org/abs/1210.4031); [inspected text](https://arxiv.org/html/1210.4031v3).

**Inspected:** Fresh reading of §§4.1–4.2, Proposition 4.1, Eqs. (35)–(38), and explicit background restrictions; compared with historical H04.

**Established method and hypotheses:** A locally covariant parametrix gives conserved Dirac current and constrains its finite ambiguity. The stress analysis separates free backgrounds from coupled backgrounds treated perturbatively and discusses allowed local counterterms.

**Relationship:** Supports the need for a consistent renormalization prescription and explicit current/stress balance; it does not substitute for the workbench’s evaluated mode sums.

**Limit:** The direct free stress-conservation discussion assumes vanishing gauge curvature and constant mass. Arbitrary electromagnetic backgrounds require force/coupling terms; no strong-field Bianchi-I closure or full source proof was audited.

## Historical method note

Newton’s analysis/synthesis and Tesla’s specification of excitation and boundary conditions may motivate questions. They supply no premise for a modern proof, no evidence of scientific priority, and no fitted physical number. Their theological, symbolic, or later esoteric interpretations are outside this mathematical audit.
