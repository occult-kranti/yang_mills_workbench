# BA1 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/ba1.json` (sha256 `2c761366…32b9`, frozen 2026-09-24T21:56:46Z) before reading either BA1 producer. I am a model-agent skeptic with correlated ancestry. This is not human review. My triage (a).2–(a).5 proposed both BA1 routes and the loop-1 numbers, and my loop-2 review wrote the blocking edits that the frozen text carries. So this review checks my own wording as much as the advisor's. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written, with the readings below. Nothing blocks production.** `ba1_check.py` (101 checks) confirms the following:
- the frozen targets are well-posed exact-rational statements;
- every constant the contract names can be computed from the declared premises;
- all 37 controls can be executed as damaging mutations (90 mutations, all rejected for the expected reason).

Three readings will matter at the post-comparison:
- **R3:** the floor bracket fits only the contract's own lemma form.
- **R4:** the reverse headline margin is thin.
- **R5:** under the headline target, the reverse must not route general volumes through the union.

## 1. Frozen bytes against the loop-2 edits
All 16 blocking edits of `loop2-review.json` are present verbatim, with these exceptions, each traceable to a recorded non-blocking or lens edit:
- `$.model` carries the N9 padding sentence.
- `rate_constant_pair.headline` gains the lens `basis` field. It names q=1/64 as a chosen weight, not the ball radius. A new control, `ball_radius_not_used_as_tree_decay_ratio`, is added with semantics.
- `preregistration.target.note` and the brackets drop the preview numerals (N5), and the headline bracket is [95,105] (N4).
- N1–N9 are applied, but N2 only in part. The two ids were added without their semantics (R7).

Other freeze records check out:
- `selected_after` is `advisor/deliberation-2.md`, which exists.
- The plan history records `plan_sha256_at_freeze = 5310d5af…`. That equals the sha256 of the current `plan.json` with its last history entry (the freeze record) removed, re-serialized with indent 2 and a trailing newline. I checked this once outside the program, because `plan.json` is mutable.

**Producer inputs.** I ran `find` on the `inputs/` folder of both BA1 producers (names only) and hashed each file against the repository.
- Each folder holds 27 files: `AGENTS.md`, the contract and the 25 shared premises.
- Every file is byte-identical to its source.
- Both inventories equal the contract-derived list.
- Neither contains a triage, deliberation, lens or Round33 skeptic file.

So `reverse_premise_isolation` holds at the inventory level. The program itself checks a synthetic inventory derived from the contract, as in AY1.

## 2. Readings and wording defects (numbered)
1. **R1. The source set B.** `parameters.weights` defines B as "the sites met by the interaction terms present in one box and not the other". The parenthetical then names the shell `Λ_{N+1}∖Λ_N` for nested comparisons. For nested comparisons these two sets differ:
   - The new stars (F1) and the new faces (F2) also contain outer-layer sites of `Λ_N`, for example (0,0,N) in the star anchored there.
   - So the literal set lies at l∞ distance **N−1** from e_z, while the shell lies at distance **N** (checks `source_set_literal_reading_N2/N3`).

   **Reading:** B is the parenthetical set (shell, or outer layer for F1 against F2), and control `boundary_distance_exact` encodes exactly those distances (N, N+1, N−1). With the shell, the source loss `e^{β d_X}` must be charged, because the new supports are not inside B. With the literal set, no loss is charged and the exponent drops by one. The two readings give **the same bound**. An off-by-one (shell distance N together with no source loss) is invalid.
2. **R2. The lemma form.** `required[1]` states the order-versus-distance lemma as "order at least ceil(d/diam)". That is valid but one order weak. A chain of n terms of l∞ diameter 1 that starts at u and ends at a new term has `n ≥ 1 + d_∞(u, new supports)`.
   - My enumeration on Λ_2..Λ_4 attains `1+d` at every distance.
   - The algebraic qubit-chain fixture has its first nonzero difference at order exactly `1+d`.

   Under the contract's form, every comparison has exponent N−1 at e_z. Under the sharp count it is N at e_z and N+1 at 0, for all three comparisons. Both are admissible. The frozen exponent N−1 and the frozen targets are consistent with the contract form.
3. **R3. The floor scaling bracket [99/100, 101/100] fits only the contract-lemma form.** In that form K_floor does not depend on τ:
   - forward `w_max·X`, exact ratio 1;
   - analytic `2T(τ_*)`, exact ratio 1;
   - coefficientwise `2R/(1−q)`, ratio 1.000375.

   A producer who proves the sharp count and writes the floor constant against `q^{N−1}` gets `K_floor ∝ |τ|`, with exact ratio **100**. The frozen bracket rejects that (check `floor_bracket_rejects_sharp_forms`), although the bound is valid and stronger.

   **Reading:** the admitted floor constant is the contract-form one. A sharp floor constant is a labelled refinement with its own exact ratio 100. That ratio is derived, not a bracket chosen after evaluation. The headline bracket is unaffected: both forms give 101.0304 (forward) and 100.6284 (reverse).
4. **R4. The headline margin was checked against the forward preview only.**
   - The reverse's natural constant under the frozen lemma form (sup `2T(64|τ|)`, Schwarz form, `n_0=N−1`) is `49/111790368 ≈ 4.3832e-7`. Its margin against 1/2000000 is **1.1407**.
   - With coefficientwise Cauchy it is `14/31441041 ≈ 4.4528e-7`, margin 1.1229.

   Acceptance is "at most the target", so this is not blocking. But it leaves no room: a looser majorant would miss the target, for example G'(R) in place of G'(T) outside the self-consistent step, a crude remainder, or the labelled 84-face count.

   Two refinements have ample room:
   - First-order cancellation: the first-order parts of the two boxes coincide on supports through u ∈ R when N ≥ 2. This gives `≈ 2.2622e-9`.
   - The sharp count gives `49/7154583552 ≈ 6.8488e-9`.

   Either must be labelled.
5. **R5. General volumes "compared through their union".** The union route costs a factor 2.
   - Forward: `2 × 2.2004e-7 = 4.4009e-7`, which passes with margin 1.136.
   - Reverse (contract form): `2 × 4.3832e-7 = 49/55895184 ≈ 8.7664e-7`, which **misses** 1/2000000.

   `required[3]` applies the headline target "for every comparison", and `parameters.comparisons` lists the general-volume item.

   **Reading:** "through their union" names the forward mechanism. A direct comparison of the two volumes is admissible and costs no factor 2:
   - the analytic route needs one sup bound and the order count;
   - the weighted route takes the symmetric difference of the two interactions as its source.

   The reverse must use the direct comparison, or a labelled refinement, for this item. Otherwise that item is `limited`.
6. **R6. "Any two centered boxes … by telescoping".** Telescoping costs `1/(1−q)` (forward `2.2354e-7`), plus a triangle across families. That is not needed. As face sets, the constructions are totally ordered: `F1_N ⊂ F2_N ⊂ F1_{N+1} ⊂ F2_{N+1}`. So every pair is one nested comparison whose new supports lie at `d_∞ = N−1` from e_z and N from 0, with N the smaller size. I enumerated all 15 pairs on Λ_2..Λ_4. The same K applies.
7. **R7. Control semantics coverage.** `gate_fields_topic_specific` has no frozen semantics. The plan rule requires `new_control_semantics` for every id not defined in an earlier frozen contract. My prospective semantics names fields that BA1 does not export: `uniqueness_all_ground_states_claimed` and `dynamics_level`.
   - **Reading:** a packet exports exactly the 12 fields of `preregistration.gate_fields_required` with their frozen values. A missing field is rejected. The template is quoted as one span.
   - `full_original_wilson_cover` is a Round32 universal id: 48 links, 36 endpoints, 7 incident anchors.
8. **R8. The floor weight.** The contract names `e^β = 64` for the headline only. **Reading:** at the floor, `e^β = w = 390625/148` (β=μ), because q = 148/390625 must be realized by the weight.
9. **R9. Equality at the cap.** At `w = 390625/148` and at `ρ = τ_*`, the rational self-map bound is an equality: `J_0 w (148/7) = 28 τ_* (148/7) = 1/64`. The true G(R) lies below 148/7, so the map is strictly contracting. The closed disc of radius τ_* lies inside the open analyticity disc of radius `R/(28 G(R)) ≥ 2.66197e-5 > τ_* = 2.63936e-5`. The floor is therefore executable, including analyticity on a neighbourhood of the closed disc.
10. **R10. The l1 fallback in `acceptance.limited`.** With l1 diameters (`d_X=2`), the self-map at w=64 fails: `J_0·64²·G(R) = 9472/390625 > 1/64`. The l1 floor per l1 step is `q_min^{1/2} ≈ 0.019465`. The fallback therefore cannot realize the frozen headline pair. It is moot, because the l∞ diameter-1 convention is confirmed by enumeration.
11. **R11. Loss where supports lie inside B.** Every extra F2 face has its owner set inside the outer layer: all of its sites share the saturated coordinate b_i=N. Charging the loss there is valid but unnecessary. The contract-form constant charges it, and the sharp constant is `1/64` of it (labelled).
12. **R12. Cosmetic.** `scaling_brackets_per_constant.K_floor_pair` contains a double space ("leading order:  the weighted"). It is the residue of removing the preview numeral under N5 and has no effect.
13. **R13. Cutoff.** For L below 24, some face vectors are annihilated and the counts only decrease, so `t_1 = 49|τ|/144` still bounds the first order. Every constant is uniform in L. No coefficient statement survives cutoff removal, and none is needed.

## 3. Control mirror
- `controls` equals `preregistration.controls_required.ids`: 37 = 37, same order, no duplicates.
- 35 ids carry frozen semantics. The two that do not are covered in R7.
- The program implements all 37 as damaging mutations against a packet validator, with a reference packet accepted.
- 8 controls also point to exact fixtures: global Lipschitz, loss per interaction, subadditivity, weight direction, cardinality, q_min, marginal and ball radius.
- Two controls carry positive cases that must be accepted: the inequality digraphs for the placeholder rule, and a negated mention for the phrase scan.

The deferred parts are scope notes only:
- the reverse inventory is synthetic in the program (the real inventories were hashed, see §1);
- the phrase scan and the R1 detector are mirrors of the tools, not imports;
- tampering is checked at packet level; producer freeze inventories come at post-comparison.

## 4. Are the frozen targets well-posed? Margins
Both targets are exact-rational upper bounds of the form `Σ_{I∋u}‖c¹_I−c²_I‖ ≤ K q^{N−1}`, for u ∈ R, every comparison, both signs, each cutoff L. The distances are exact at every N:

| quantity | value |
|---|---|
| `d_∞(e_z, new supports)` | N−1 |
| `d_∞(0, new supports)` | N |
| shell (from e_z / from 0) | N / N+1 |
| outer layer (from e_z / from 0) | N−1 / N |

Evidence: enumeration at N=2,3,4, plus the all-size argument in the derivation §4.

| constant (both signs) | value | target | margin |
|---|---|---|---|
| forward headline, exact first order, contract form | 7334358…2259/3333124…5768 ≈ 2.2004450e-7 | 1/2000000 | 2.2723 |
| forward headline, sharp (labelled) | ≈ 3.4382e-9 | 1/2000000 | 145.4 |
| reverse headline, 2T(64\|τ\|), Schwarz | 49/111790368 ≈ 4.3832e-7 | 1/2000000 | **1.1407** |
| reverse headline, coefficientwise | 14/31441041 ≈ 4.4528e-7 | 1/2000000 | 1.1229 |
| forward floor, exact / crude | ≈ 1.4693e-5 / ≈ 2.0877e-2 | 1/12 | 5672 / 3.99 |
| reverse floor, exact / crude 2R / crude 2R/(1−q) | 49/2018304 / 1/32 / 390625/12495264 | 1/12 | 3432 / 2.667 / 2.666 |
| crude headline, forward / reverse (reported, not targets) | ≈ 2.9018e-4 / 296/390625 ≈ 7.578e-4 | 1/2000000 | fail (retained) |

The margin-2 rule was met against the recorded forward previews: 2.27 (headline) and 2.67 (floor preview `(1/32)/(1−q)`). It was not checked against the reverse's own headline form (R4).

**Scaling.** The exact τ-ratios of the contract-form constants lie inside their brackets:
- headline: 101.0304 (forward) and `4340004/43129 ≈ 100.628` (reverse);
- floor: exactly 1 (forward, analytic Schwarz), or 1.000375 (coefficientwise);
- `q_min`: exactly 100.
