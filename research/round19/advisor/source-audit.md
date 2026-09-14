# Round19 prospective A2 source audit: limiting-state passage and dense stability

Status: planning source audit only. This file does not freeze A2 and does not accept any A1 evidence. A2 remains gated on an accepted or terminal A1 boundary-consistency result.

Repository head inspected: `e62886d4cf724557c1884d11e5579bae94e28fcb`. The published A1 planning files are preserved as written at this head. The external skill snapshot mapping expected by the handoff is present at `research/round19/methods/external-dependencies.json`; I did not find a top-level `methods/` directory in this checkout. The snapshot hashes match the local validation skill copies recorded in `contract-a1.json`, so this audit treats `research/round19/methods/paired-physics-research.md` and `research/round19/methods/scale-and-exceptions.md` as the installed source snapshots for Round19 planning.

## Question being audited

Prospective A2 should only be selected after A1 decides whether literal finite-volume restrictions of one infinite coefficient assignment have a complete local component bound. If A1 passes, the next possible question is whether those local bounds can be connected to limiting states, limiting dynamics and a spectral lower bound, or whether a conventional dense weak-perturbation theorem supplies a separate dense-stability route. These are not the same question:

- a finite-volume component lower bound controls a declared family of finite Hamiltonians;
- a limiting state/dynamics statement needs a specified net of finite restrictions and a theorem or construction that survives the limit;
- a dense homogeneous stability statement needs a smallness condition for all local plaquette interactions in one physical energy convention;
- a continuum Yang-Mills mass-gap claim remains outside all of these finite-spacing statements.

A2 must therefore record `E_star > 0`, `alpha/E_star`, local coupling ratios, finite volume and any lattice-spacing label as separate variables. Static Euclidean `kappa`, a numerical tolerance, or a Fibonacci index cannot supply a Hamiltonian energy scale.

## Primary source: Yarotsky weak perturbation theorem

Source: D. A. Yarotsky, *Quasi-particles in weak perturbations of non-interacting quantum lattice systems*, arXiv:math-ph/0411042v1, 11 Nov 2004, https://arxiv.org/pdf/math-ph/0411042.

Reading depth this round: abstract; definitions and finite-volume setup in Section 1; Theorems 1-3; boundary convention; selected proof-review material in Section 2 around the ground-state ansatz, Lemma 1, estimate (14) and resolvent expansion (15). I did not rebuild the full contraction proof from the cited earlier papers.

What the source states and why it matters:

- The source permits a Hilbert space `H_x` at each lattice site that is possibly infinite-dimensional, and a nonnegative self-adjoint possibly unbounded local `h_x` with a nondegenerate vacuum and gap at least one. This is the key reason the theorem is not automatically disqualified for SU(2) link rotors.
- The perturbation is a sum of bounded finite-range self-adjoint terms `phi_x` with `sup_x ||phi_x||` sufficiently small. Empty-boundary finite-volume Hamiltonians keep terms whose full range lies inside the finite volume.
- Theorem 1 gives constants `c1(Lambda_0)` and `c2(Lambda_0)`: if `sup_x ||phi_x|| < c1`, every finite-volume Hamiltonian has a nondegenerate ground state, and the renormalized spectrum lies within `c2 sup_x ||phi_x||` neighborhoods of the free spectrum. The displayed gap lower bound is `1 - c2 sup_x ||phi_x||` after normalizing the free gap to one.
- Theorems 2 and 3 provide the weak-* thermodynamic ground-state limit and a self-adjoint GNS generator with the same spectral estimates. Translation invariance is introduced later for quasiparticle claims and is not needed for the basic ground/gap route.
- Section 2 confirms that the source's constants are not presented as evaluated numerical values: it uses generic constants `c` and small `epsilon` depending on range but not volume, then sketches Lemma 1 and estimate (14) before the resolvent expansion.

Project applicability if A1 passes:

A Yarotsky-style route can be prospective A2 only after A1 provides a fixed local block/reference decomposition with a unique ground and a full-link gap in one physical unit. Then one must choose the actual site blocking. Two candidates are possible and should not be mixed:

1. **Free-link dense route.** Use outgoing-link cells as sites, local free electric Hamiltonian as `h_x`, and every plaquette as a bounded perturbation. This is the cleanest route to a homogeneous dense finite-spacing theorem. It supports only sufficiently small `lambda_max/alpha`; it does not use the Round18/Round19 dressed bridge ratios as an accepted dense threshold.
2. **Dressed-component route.** Use A1 components or periodic blocks as local gapped units, and treat only the remaining interactions or boundary couplings as perturbations. This may help with a boundary-consistent exceptional family, but it requires a new exact blocking map, a proof that each block has a unique ground in the full-link space, a uniform block gap in `E_star` units, and a bounded finite-range residual interaction assigned consistently across the infinite lattice.

The source does not by itself provide the numerical smallness threshold for either route. A2 can use it qualitatively only after the model's `epsilon_A2 = sup_x ||phi_x||` is computed in the same normalization as the local block gap and then kept symbolic under the condition `epsilon_A2 < min(c1, 1/(2c2))` or an equivalent explicit condition. A numerical dense threshold requires extracting concrete `c1,c2` from the proof or from another theorem whose hypotheses match the SU(2) rotor blocking.

Exact missing estimates before an A2 contract can be frozen:

| Missing item | Why it is required | Current status |
|---|---|---|
| A1 local block result | A2 cannot choose free-link, clipped-component or dressed-block route until A1 proves or rejects every boundary component. | Pending A1 evidence. |
| Site/block map `B_x` and range `Lambda_0` | Yarotsky constants depend on the perturbation range; the source theorem cannot be applied to an unnamed graph decomposition. | Not frozen. |
| Normalized block gap `g_block/E_star` | The theorem assumes local gap at least one after rescaling. For free-link cells this is algebraic; for dressed A1 blocks it depends on the A1 proof. | Free route known qualitatively; dressed route pending. |
| Perturbation norm `epsilon_A2 = sup_x ||phi_x||` | The theorem's smallness condition is on the operator norm per translated finite-range term, not on total finite-volume norm. | Needs exact grouping; no accepted A2 value. |
| Numerical or symbolic constants `c1(Lambda_0), c2(Lambda_0)` | A positive qualitative result can retain existential constants; an explicit dense threshold needs evaluated constants. | Missing; Section 2 uses generic constants. |
| Boundary convention transfer | Empty-boundary restrictions and all-contained plaquette boxes differ near boundaries; any padding or literal-restriction argument must be written for the chosen blocking. | Previous padding argument exists for free-link route; not audited for A1 clipped blocks. |
| Gauge-sector passage | The source theorem is on the full product Hilbert space; the physical Gauss sector needs a reducing-subspace and unique-ground invariance argument. | Previously argued in Round13/Round18 style; must be rebound to A2 source bytes and block choice. |
| Limiting observable nontriviality | A GNS generator gap does not by itself exhibit a nonzero physical local excitation or continuum mass. | Missing; not needed for finite-spacing gap, required for stronger physical claims. |

Decision for A2 planning: Yarotsky is the correct primary source to audit for a qualitative finite-spacing limiting-state and spectral-passage route. It is not yet a frozen A2 contract because the exact block/range/norm constants depend on A1 and because no explicit `c1,c2` have been reconstructed.

## Comparator source: Bravyi, DiVincenzo and Loss

Source: S. Bravyi, D. P. DiVincenzo and D. Loss, *Polynomial-time algorithm for simulation of weakly interacting quantum spin systems*, arXiv:0707.1894v1, 12 Jul 2007, https://arxiv.org/pdf/0707.1894.

Reading depth this round after title correction: title/abstract lines, model definition, Theorem 1, Theorem 2 statement, and convergence-constant derivation around Lemma 5/Corollary 4. I did not review all algorithmic sections or treat the separate Schrieffer-Wolff paper as a source for this audit.

What the source states and why it is not transferable as an SU(2) threshold:

- The model has spin-1/2 qubits at graph vertices and two-qubit interactions on graph edges.
- Theorem 1 gives an explicit condition `|epsilon| <= 2 epsilon_0`, where `epsilon_0 = 2^-18 Delta/(d J)`, and then a nondegenerate smallest eigenvalue with gap at least `Delta/2`.
- The derivation of the explicit constant uses qubit creation operators, graph degree `d` for two-site interactions, and finite-dimensional combinatorics. Those hypotheses do not match unbounded SU(2) link rotor Hilbert spaces or four-link plaquette multiplication operators.

Decision for A2 planning: this source is useful as a rejecting control for bad source transfer. Any A2 draft that copies `2^-18 Delta/(dJ)` into the rotor problem, or treats a two-site qubit degree as the plaquette support/range constant, must fail source admission.


Correction before publication: an earlier advisor draft mislabeled arXiv:0707.1894 as a Schrieffer-Wolff paper. Reopening the linked PDF confirmed the actual title above and confirmed that the theorem statements used here belong to the weakly interacting qubit spin-system paper: the model is `H(epsilon)=H0+epsilon V` with qubits on graph vertices and two-qubit interactions, and Theorem 1 uses `epsilon_0 = 2^-18 Delta/(dJ)`. The decision remains unchanged: this is a wrong-hypothesis comparator for SU(2) rotors, not an imported threshold.

## Prize-problem boundary

Source: Clay Mathematics Institute, *Yang-Mills & the Mass Gap*, https://www.claymath.org/millennium/yang-mills-the-maths-gap/.

Reading depth this round: official problem page status and overview only.

The Clay page identifies Yang-Mills and the mass gap as unsolved and describes the missing mathematical foundation of four-dimensional quantum Yang-Mills theory. A finite-spacing lattice stability theorem, a GNS generator for a small-coupling lattice model, or a boundary-consistent exceptional family does not construct the required continuum quantum field theory. A2 should state this boundary in its contract if it is later frozen.

## Source-bound decision ledger for prospective A2

| Prospective claim | Source support | Current decision |
|---|---|---|
| Qualitative thermodynamic ground state and GNS spectral gap for small bounded finite-range perturbations of a gapped product model | Supported by Yarotsky Theorems 1-3 under `sup_x ||phi_x|| < c1(Lambda_0)` and the normalized gap hypothesis. | Admissible as a candidate route only after exact A2 blocking/norm definitions are frozen. |
| Explicit numerical dense rotor threshold | Not supplied by the inspected Yarotsky statements; Bravyi's explicit number has wrong hypotheses. | Missing estimate; do not freeze a numerical threshold. |
| Boundary-consistent finite restrictions imply limiting spectral passage | Not automatic; needs source boundary or a padding/literal-restriction proof for the chosen block family. | Open pending A1 and a written boundary theorem. |
| A1 local `alpha/8` bound, if accepted, proves dense homogeneous stability | Not supported by any inspected theorem without an additional smallness/range/contraction argument. | Reject as overclaim. |
| Positive finite-spacing lattice gap implies Clay mass gap | Contradicted by the problem boundary; continuum construction and scale limit are separate. | Reject as overclaim. |

## Recommended A2 acceptance tests after A1, if selected

1. Freeze a new A2 contract version after A1 evidence, naming one route: free-link dense Yarotsky route, dressed-component limiting route, or a narrower exception route. Do not combine premises from different routes without a conversion lemma.
2. Declare `E_star > 0`, `alpha/E_star`, all coupling ratios, finite volume, lattice spacing and boundary convention as separate fields.
3. Provide an exact site/block map, perturbation range `Lambda_0`, local normalized gap and `sup_x ||phi_x||` bound in the theorem's units.
4. State the theorem condition symbolically if constants remain existential: for example `epsilon_A2 < c1(Lambda_0)` and `c2(Lambda_0) epsilon_A2 < 1`, with no numerical threshold claimed.
5. Include rejecting controls: copied Bravyi constant, total-volume norm instead of per-range norm, `E_star=0`, static `kappa` as an energy, changed local coefficients across finite boxes, missing Gauss-sector invariance, and direct promotion to continuum mass gap.
6. Require independent reconstruction of the block/range/norm dictionary before any source theorem is admitted.

## URLs and local source records inspected

- Yarotsky primary PDF: https://arxiv.org/pdf/math-ph/0411042. Reading depth: Section 1 definitions and Theorems 1-3; selected Section 2 proof review around Lemma 1, estimate (14), and resolvent expansion (15).
- Bravyi-DiVincenzo-Loss primary PDF: https://arxiv.org/pdf/0707.1894, *Polynomial-time algorithm for simulation of weakly interacting quantum spin systems*. Reading depth: title/abstract, model definition, Theorem 1, Theorem 2 statement and explicit convergence-bound derivation; not imported as a rotor theorem.
- Clay official problem page: https://www.claymath.org/millennium/yang-mills-the-maths-gap/. Reading depth: official status and overview.
- Local prior audit: `research/round13/advisor/weak-coupling-stability.md`, SHA-256 `f21c9c84713fb39b4c91d5570f0248b44e7b51785f58b07d95f09e0d6c6d2045`.
- Local Round17 audit: `research/round17/advisor/source-audit.md`, SHA-256 `c6dc0c3cfd991975092c7fab20735655696e8dc432dccb67b5775dc3cab228e7`.
- Local Round18 audit: `research/round18/advisor/source-audit.md`, SHA-256 `e1307e50e4756e89e35759b85a7202c7c35906bb7c0a02062bef108dc5edaa2d`.
- Round19 external dependency mapping: `research/round19/methods/external-dependencies.json`, SHA-256 `06915ffeed40753312fdeb50da23a9059299a422a3ce5916f093dba8030b26a0`.
- Round19 A1 contract: `research/round19/advisor/contract-a1.json`, SHA-256 `dc2d5b1e41f75d7f1d27fb6c9fde20194611a35eef9d184a39bf7d3a5a096b87`.

## Decision-relevant ambiguity

The handoff referred to `methods/external-dependencies.json`, while the repository path at this head is `research/round19/methods/external-dependencies.json`. I used the actual repository path. If a later packaging step expects a top-level `methods/` path, it should either update the handoff wording or add an explicit path adapter; this source audit should not silently create that directory.


## Addendum: constructive product-representation route proposed during A1 execution

A second prospective A2 route is now on the table. It should be adjudicated after A1, not frozen now.

Candidate statement, if A1 supplies the needed local facts: construct an infinite tensor product reference state from complete strip ground states and free Haar factors. Let `H_ref` be the sum of nonnegative cluster Hamiltonians after subtracting each local ground energy. On the finite-excitation core, require a vacuum gap `delta = alpha/8` in the same `E_star` scale register as A1. Add a spatially summable perturbation `V` with operator-norm budget `beta <= alpha |tau|`, and require the reference trial mean `Omega_ref V Omega_ref = 0` termwise by actual unused-link Haar factors or another proved zero-mean mechanism. A codimension-one form/min-max argument may then isolate a unique ground and a gap lower estimate of order `delta - beta`, provided the infinite-domain and essential-spectrum premises are actually proved.

This is not the same as the Yarotsky free-link dense route. It uses a dressed product reference rather than the electric product vacuum, and its smallness condition is a global summable norm budget relative to the reference gap rather than a per-translate dense perturbation constant. It is also not the same as convergence of finite clipped restrictions: a direct infinite product representation can define a candidate GNS sector without proving that every finite boundary sequence converges to it. If A2 wants convergence from literal finite restrictions, it must add local-state convergence, boundary stabilization and spectral convergence statements separately. The construction also does not address a homogeneous nondecaying dense remainder, because `sum ||V_f||` would not be finite.

Feasibility judgment before A1 evidence: plausible but conditional. It is feasible as a narrow summable-exception route if A1 proves the complete/clipped local gap and zero-mean mechanisms strongly enough to build a reference product with fixed `E_star`, and if A2 proves the operator-theoretic infinite sum instead of treating finite ledgers as the limit. It is not feasible as a dense homogeneous or continuum route without an additional theorem.

Additional exact proof obligations for this route:

| Obligation | Required content | Falsifier |
|---|---|---|
| Infinite product reference | Specify the complete strip/free-factor partition, the reference vector, the incomplete boundary convention if any, and the local algebra/core. | A finite clipped boundary product is silently substituted for the complete infinite product. |
| Nonnegative `H_ref` and core gap | Define each shifted local Hamiltonian, prove essential self-adjointness or closed form construction, and show `H_ref >= delta Q` on the finite-excitation core with `delta/E_star = (alpha/E_star)/8`. | The proof only bounds sampled finite matrices or changes `alpha/E_star` by volume. |
| Summable perturbation | Prove `V` is a bounded self-adjoint operator with `||V|| <= beta <= alpha |tau|` in the same representation, including signed coefficients and no cancellation in the norm budget. | Replace the summable schedule by a homogeneous nondecaying remainder while retaining the same beta. |
| Zero trial mean | Prove `Omega_ref V Omega_ref = 0` termwise from an actual free Haar factor, or retain the generic two-norm loss. | Use bare-vacuum parity where the dressed reference has no untouched link. |
| Ground and gap isolation | Give a valid codimension-one min-max or form theorem for `H_ref + V`, including offdiagonal coupling from the reference vector and essential-spectrum stability. | Claim `delta - beta` from a finite-volume eigenvalue gap without a domain/essential-spectrum argument. |
| Relationship to finite restrictions | State whether the result is a direct product-representation theorem or a limit of finite clipped restrictions. If the latter, prove convergence of states, forms/resolvents and local observables. | Present the direct product result as convergence of all boundary restrictions. |

Recommended post-A1 adjudication: if A1 passes only finite clipped component bounds, select between two A2 contracts. The constructive product-representation route is the narrower, likely cheaper route for a summable exception. The Yarotsky route is the broader source-backed route for small dense perturbations, but still lacks explicit constants. They should not be merged unless A2 proves an exact dictionary between the reference product construction and the source theorem hypotheses.
