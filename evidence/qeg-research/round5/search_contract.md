# Bidirectional proof planning: a finite, auditable search contract

Version 1.0, 9 September 2026. This is an implementation contract and a mathematical proof-planning proposal. It does not claim that a graph search proves continuum quantum electrodynamics or gravitation. The numerical results in round 4 remain numerical evidence for their stated finite model.

## 1. What the search must accomplish

Start at two precisely different objects: an explicitly declared set of available assumptions and established lemmas, and an explicitly stated target theorem. Forward search asks what follows from what is available. Backward search asks which sufficient premises would let an already checked theorem establish the target. When every remaining backward premise is already available forward, reconstruct the entire derivation and independently check every application.

The selected mathematical target is **global forward well-posedness, together with smooth finite-time source-amplitude dependence, of the finite-regulator homogeneous Maxwell–Dirac ODE under a uniform positive kinetic-coefficient hypothesis**. This is a bounded advance over observing converged trajectories. It does not assert uniform bounds as the regulator is removed, stability as time tends to infinity, or agreement with fully quantized electromagnetism.

The algorithm is inspired by A* and bidirectional heuristic search. A* combines accumulated cost with an estimated remaining cost; this project starts with the admissible baseline heuristic zero. The original historical source is [Hart, Nilsson and Raphael, 1968](https://ai.stanford.edu/~nilsson/OnlinePubs-Nils/PublishedPapers/astar.pdf). We make no claim here about optimal efficiency among all possible heuristic algorithms.

The MM algorithm gives a rigorously specified midpoint property and stopping rule for its own graph-search setting. Our forward fact sets and backward sufficient-goal sets are different representations. Its theorem cannot be imported by merely giving our program a bidirectional name. [Holte et al., 2016](https://www.cs.du.edu/~sturtevant/papers/MMaaai.pdf) The independently checked forward uniform-cost certificate below supplies the optimization guarantee actually used here.

## 2. Separate the theory map from the proof graph

The broad research map may contain definitions, mathematical theorems, physical postulates, effective descriptions, empirically supported claims, conjectures, contradictions and proposed experiments. Its arrows must be typed: implication, sufficient condition, limiting case, approximation, motivation, analogy or unresolved dependency. Only a checked implication, with all its hypotheses, may become an inference rule.

An analogy is never a proof edge. A numerical experiment is not an exact existence theorem. An implication valid for fixed positive masses cannot be instantiated at a zero-mass point. A statement proved with a finite mode set cannot lose its finite-regulator type when passed to another node. Dependency extraction and premise retrieval are useful precisely because mathematical statements depend on specific earlier results; LeanDojo exposes such dependencies and tactic feedback for Lean repositories. [LeanDojo](https://leandojo.org/leandojo.html)

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

## 3. AND/OR semantics and the direction that must not be reversed

One rule with three premises is an AND requirement: all three are needed. Two different applicable rules for the same conclusion are OR alternatives. Represent each conjunctive rule as a hyperedge, or as a visibly labeled rule node receiving all prerequisite arrows. Ordinary paths that touch only one prerequisite do not represent proofs.

For example, from `energy_identity ∧ coercivity ∧ source_integrable ⇒ bounded_field`, backward reasoning replaces the goal `bounded_field` by those three goals. It does **not** infer the three premises from the truth of `bounded_field`. The same distinction appears in Lean's `apply`: applying a theorem matching the conclusion creates the remaining premise goals. [Theorem Proving in Lean: Tactics](https://lean-lang.org/theorem_proving_in_lean4/Tactics/)

Backward regression preserves **sufficiency**, not equivalence and not necessity. If a selected route requires coercivity and coercivity has not been established, that route is blocked. Another theorem might establish the target by different means. Failure of a sufficient condition does not disprove the desired conclusion.

## 4. Executable forward and backward searches

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

Checking this sequence verifies Horn-rule application. It does not verify that a manually entered differential inequality is a valid theorem. Such claims need their mathematical derivation and independent review. A future Lean formalization must generate proof objects accepted by Lean's kernel; a JSON `passed` field is not equivalent. [Lean FAQ: proof objects](https://lean-lang.org/faq/)

## 5. Safe stopping and the exact scope of an optimality claim

The first meeting produces an **incumbent derivation**, not a least-cost certificate. For example, with initial `A`, rules `A⇒T` of cost 9, `A⇒B` of cost 1 and `B⇒T` of cost 1, a generated direct goal can be noticed before the cheaper two-step route. Queue order and a visual meeting are insufficient.

Use this baseline certification strategy:

1. Obtain any fully replayed bidirectional candidate of actual cost `U`.
2. Independently run forward uniform-cost search over exact fact sets using S2, seeded at `F0`.
3. Ignore stale heap records. When a goal state is popped, its cost is minimal among all admissible rule-application sequences in this finite library.
4. Alternatively, if every remaining heap key is at least the already checked incumbent cost `U`, terminate and certify `U` minimal. Nonnegative extensions cannot produce a cheaper goal.
5. If a cheaper goal is found, replace the incumbent and retain the earlier meeting as a useful nonoptimal trace.
6. If the heap exhausts without reaching the target, report **not derivable in this finite rule library**. This is not a proof that the physical target is false or impossible.

There are at most `2^|A|` exact sets in either state representation. Positive integer costs and finite state/rule sets ensure baseline termination with exact duplicate detection. This worst-case bound is large: use a deliberately small reviewed library first. Shared lemmas make proof costs different from adding independent single-goal costs; a heuristic that sums overlapping subgoal estimates can overestimate. Keep `h=0` until any nonzero heuristic has an actual admissibility argument for these states.

Do not use an unproved `min(frontier_F)+min(frontier_B) ≥ U` stopping condition for this mixed representation. Do not claim MM midpoint guarantees, NBS expansion bounds or optimality over every possible mathematical proof. NBS's near-optimal node-expansion result is a carefully defined result for its specified search model, not a license to transfer the label to a new planner. [Chen et al., 2017](https://arxiv.org/abs/1703.03868)

## 6. Minimal Maxwell–Dirac theorem library

All physics atoms below are scoped to one fixed finite mode set. They refer to the exact equations in `round4/response_contract.md` P1–P6, not to floating-point solver output. Standard ODE lemmas are imported only after their hypotheses have been checked by the mathematical advisor.

| Seed | Exact hypothesis or adopted mathematical result |
|---|---|
| `A_model` | Finite `i=1,...,N`; `M_i>0`, `w_i>0`, `k_i∈R`; fixed real `χ`, `e²>0`; the stated matched ODE and energy definitions |
| `A_state` | Finite real `a(0),x(0)` and `|r_i(0)|≤1` |
| `A_margin` | `μ = 1+χ−e² Σ_i w_i/(4M_i³) > 0` |
| `A_drive` | `F:[0,∞)→R` is continuous, hence integrable on every compact interval |
| `A_ode` | Local existence/uniqueness and the compact-containment continuation theorem for finite-dimensional ODEs with continuous time dependence and locally Lipschitz state dependence |
| `A_parameter` | At fixed modes/weights/couplings, `F(s,λ)` and initial data are `C^k` in `λ`, `k≥1`, with the required derivatives continuous jointly on compact sets; nearby initial Bloch states remain in the unit ball |
| `A_dependence` | Standard finite-time `C^k` parameter-dependence theorem for such an ODE flow, on a common existence interval |

The `A_ode` and `A_dependence` nodes represent stated mathematical theorem imports, not unproved physical conjectures. `A_margin` is a deliberately explicit sufficient parameter restriction. A theorem written under that assumption does not imply that the restriction holds for every regulator or physical theory.

| Rule | Conjunctive premises ⇒ conclusion | Mathematical reason |
|---|---|---|
| R01 | `A_model, A_margin ⇒ Z_positive` | `ω_i≥M_i`, so `0≤C(a)≤Σ_i w_i/(4M_i³)` and `Z(a)≥μ` for every real `a` |
| R02 | `A_model, A_state ⇒ bloch_bounded` | `d|r_i|²/ds=4r_i·(h_i×r_i)=0` on any local solution |
| R03 | `A_model, Z_positive, A_drive ⇒ regular_rhs` | Positive masses and denominator margin remove the finite-system singularities; RHS is smooth in state and continuous in time |
| R04 | `regular_rhs, A_state, A_ode ⇒ local_unique` | Apply the local ODE theorem at the initial point |
| R05 | `A_model, local_unique ⇒ energy_identity` | Direct differentiation gives `U'=xS`, `C'=-2Dx`, hence `W'=xF` |
| R06 | `A_model, bloch_bounded, Z_positive ⇒ energy_coercive` | `h_i·r_i+ω_i≥0`, hence `W≥μx²/2≥0` |
| R07 | `energy_identity, energy_coercive, A_drive ⇒ field_bounded_on_compacts` | Apply the square-root energy estimate below, including its `W=0` case |
| R08 | `A_model, field_bounded_on_compacts, bloch_bounded ⇒ state_bounded_on_compacts` | Integrate `a'=-x`; the finitely many Bloch coordinates are bounded |
| R09 | `local_unique, regular_rhs, Z_positive, state_bounded_on_compacts, A_ode ⇒ global_unique` | If a finite maximal time existed, the state would remain in a compact regular region, contradicting the continuation alternative |
| R10 | `global_unique, regular_rhs, A_parameter, A_dependence ⇒ smooth_finite_time_response` | Apply parameter dependence on each fixed compact time interval with a common positive margin |
| R11 | `global_unique, smooth_finite_time_response ⇒ selected_target` | Package the two conclusions without extending their scope |

The first useful meeting is often near `{local_unique, energy_coercive, energy_identity}`: these are concrete forward facts, while the backward global-existence route needs an a priori bound followed by continuation. The actual implementation must report the meeting it computes, not invent a trace matching this illustrative sentence.

## 7. The energy estimate that connects the two directions

Let `W=Zx²/2+e²U`. Positivity and the exact energy identity give

\[
W' = xF,\qquad |x|\leq\sqrt{2W/\mu}.
\tag{S5}
\]

Direct division by `sqrt(W)` fails at the instantaneous vacuum initial state, where `W(0)` may be zero. For `ε>0`, differentiate `sqrt(W+ε)` instead:

\[
\frac{d}{ds}\sqrt{W+\epsilon}
=\frac{xF}{2\sqrt{W+\epsilon}}
\leq\frac{|F|}{\sqrt{2\mu}}.
\tag{S6}
\]

Integrating and sending `ε↓0` yields, for every finite `t` within the maximal solution interval,

\[
\sqrt{W(t)}\leq\sqrt{W(0)}
+\frac{1}{\sqrt{2\mu}}\int_0^t|F(s)|\,ds,
\tag{S7}
\]

\[
|x(t)|\leq\sqrt{\frac{2W(0)}{\mu}}
+\frac{1}{\mu}\int_0^t|F(s)|\,ds,
\qquad
|a(t)|\leq|a(0)|+\int_0^t|x(s)|\,ds.
\tag{S8}
\]

Thus no state coordinate can blow up at a finite time while `Z≥μ>0`. The ODE continuation argument establishes existence for every finite future time. It does not give a time-independent bound on `a`, and a smooth solution can still exhibit substantial sensitivity or oscillation. A finite-time tangent estimate is not a proof of asymptotic stability.

## 8. The full-theory target must remain blocked

Use an explicit unresolved target such as `controlled_semiclassical_Einstein_QED_prediction`. Its backward work-plan obligations include a common covariant current/stress renormalization, defined quantum state and causal response, a gauge-fixed gravitational initial-value formulation with controlled higher-derivative treatment, appropriate stress/current noise or a stated validity criterion, constraint-compatible initial data, and controlled regulator removal in observables and evolution.

Do not register a rule saying that this list automatically implies a complete theory of nature. It is a **research decomposition**, not yet a proved sufficient theorem. The finite model has no admission rule from `selected_target` to any of those continuum or curved-space obligations. Return the blocked subgoals and the missing inference certificates. “No path in this library” accurately exposes the next research work.

For later candidates, distinction among proof, conditional prediction and conjecture stays mandatory. Festina Lente and the Weak Gravity Conjecture are not axioms of established QED. A proposed inner-horizon mechanism must specify the state and renormalized stress tensor before classical mass-inflation theorems can be compared with it. Photon–graviton mixing in a prescribed background does not itself supply semiclassical gravitational backreaction. These distinctions constrain which edges the larger map can admit.

## 9. Acceptance tests that attack logical failures

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

## 10. Advisor execution protocol

Freeze the target and its quantifiers. Confirm the equations and signs independently. Build the smallest admitted-rule library needed for one theorem. Run reachability saturation, bidirectional candidate search, independent replay and forward optimality certification. Have a separate mathematical reviewer attack each inference and the coercivity edge cases. Only then add the accepted theorem node and its exact assumptions to the broader research map.

For an unresolved bridge, output a proposed lemma with its precise hypotheses, a potential counterexample and an experiment or proof obligation that could decide it. The advisor may generate candidate rules but may not mark their proofs checked. Feedback-guided theorem agents such as COPRA similarly execute proposed tactics in a proof environment rather than accepting text alone. [Thakur et al., 2023](https://arxiv.org/abs/2310.04353) Our implementation currently certifies the finite planning trace; formal verification of the analytical theorem would require a separate Lean/Isabelle/Rocq development.
