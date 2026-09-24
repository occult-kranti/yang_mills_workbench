# Jung/Pauli lens, Round32 sub-round 1 -> sub-round 2 update

Advisory only; model-agent lens with correlated ancestry to the advisor, producers and skeptic. No historical-person participation or endorsement. Human project author: Hruday N M (BUNZEEY); AI-assisted.

## 1. Observation-map assessment of sub-round 1

Pre-registration was honoured. AV1: `controls_required.ids` equals `controls` byte-for-byte (25=25); both checkers read the target `1/2500000` from the frozen contract rather than hard-coding it (assistant-1 `results.json` items 3, 5-8); no post-hoc nodes (only `|tau|<=10^-8`, with the `-tau` evaluation correctly labelled a replay, not a second confirmation); tier (i) fails both targets and is explicitly retained as a limited-tier value in `av1-gate.json` rather than dropped. AV2 (forward and reverse, both `report.md`) independently agree on radius `~1.8319675034e-7`, correctly self-label `reference_unresolved` (the free value `e^{-3}/4` lies inside the enclosure) with `resolved_interaction_shift:false`, and both the AT4 Poisson certificate and the tier-(i) window are retained as `insufficient` rather than discarded.

**AV2 mirror gap.** `contracts/av2.json`'s `controls` list has 24 entries; its `preregistration.controls_required.ids` has only 23, missing `c1_window_preview_only` (assistant-1 finding, `results.json` item 4). Both producers nonetheless executed `c1_window_preview_only` correctly (`forward/av2/check.py:916`, `reverse/av2/check.py:1404`, both present in `output/results.json`), reading it from `controls`/`new_control_semantics` rather than from the incomplete `ids` list, so the science already produced is unaffected. But the contract's own internal cross-check fails, and this is a genuine authoring gap, not a false positive. **Recommend:** the pending `av2-gate.json` record this as a non-blocking finding parallel to AV1's N1-N6, state plainly that both producers executed the control despite the omission, and note that `controls_required.ids` should read 24 entries; do not silently edit the already-frozen `av2.json` itself.

## 2. Sub-rounds 2-5: goal recommendations

- **Sub-round 2 (AW1/AW2, interaction shift).** No change to the goal. It is well posed given AV2's `reference_unresolved` outcome: AW1 targets the only remaining first-order effect (the uncentered `tau/144`), not the centered shift AV2 could not resolve. Process note: `contracts/aw1.json.selected_after` points at `research/round32/advisor/av2-gate.json`, which does not yet exist. Do not move AW1/AW2 from `status: draft` to production until AV2's own skeptical review and gate are written.
- **Sub-round 3 (AX1/AX2, uniform Hamiltonian).** No change recommended; independent of the AV1/AV2 outcome.
- **Sub-round 4 (AY1/AY2, state identification).** No change recommended; keep `uniform_local_closeness_not_uniqueness` and the forbidden-phrasing list (loop2-response.md sec. 4) in force.
- **Sub-round 5 (AZ1/AZ2, continuum + finite graph).** No change recommended; AZ2 keeps `model_is_finite_graph:true`/`transfers_to_aq:false` and is never cited as resolving goal 2 (loop3-signoff.md sec. 5).

## 3. AW1/AW2 pre-registration specifics

`contracts/aw1.json.parameters.aw2_coupling_rule`: "tau_AW2 = the largest element of the decade grid {10^-8, 10^-9, ...} with K_2^+ * tau <= 1/288 ..., frozen here, never chosen after K_2 is seen." AW2's `preregistration.tau.rule_if_chosen_later` already correctly carries "AW1 decade-grid rule" (a formula reference, not `null`); `check.py` must compute `tau_AW2` at run time from the AW1 gate's admitted `K_2^+` (read by path and hash), never copy a literal. Both `aw1.json` and `aw2.json` now have `controls`==`controls_required.ids` byte-for-byte (28/28 and 22/22) -- the AV2 mirror gap was not repeated.

Sub-labels: `static_not_dynamic` (AW1 item 3, AW2 item 3 -- an equal-time effect, not a dynamical correction) and `sign_certified_below_cap` (if `tau_AW2<10^-8`), drawn from the same closed five-label vocabulary as AV1/AV2.

Sign-convention fixture: control `sign_convention_fixture`, "a one-plaquette exact fixture under I1.5 (labelled a finite graph) shows sign(<W>)=sign(tau) at first order" (`aw1.json.new_control_semantics`), matching the assistant script specified in `loop3-signoff.md` sec. 4 item 3: PASS iff `sign(<W>)=sign(tau)` for every `j_max` in {1/2,1,3/2}, antisymmetry to O(tau^2), monotone convergence in `j_max`.

Controls separating a real first-order effect from an artifact: **centering** -- `vector_versus_scalar_centering` (AW1), "no m_hat in the omega(W) path" (AW2 item 4); **convention** -- `sign_convention_fixture`, `haar_parity_exact`, the orientation-invariance control (AW1 item 3); **boundary** -- K_2 "itemized and uniform in volume" (AW1 item 4), "two box sizes give the same formula" (AW2 item 4); **arithmetic** -- `exact_arithmetic_admission`, `tier_mixing_rejected`, Fraction-only with labelled Arb previews. `flip_no_third_order_claim` further blocks over-reading the flip lemma's oddness into an unproved O(tau^3) remainder.

## 4. Occult/mystical sources

None. `sources.json.not_admitted` is explicit: synchronicity/archetypes, Besant-Leadbeater's clairvoyant "number-weights," Dee/Agrippa/Fludd symbolism and the CIA remote-viewing report supplied no force, medium, observer variable or Hamiltonian term anywhere in sub-round 1; they served only as cautionary templates for the pre-registration rules (post-hoc node/batch discipline, reference-built-into-readout, shared-judge confounds) applied to the AV2 finding above.

## 5. Assistant tests wanted after sub-round 2

1. Replay the chain AW1 gate -> AW2 contract rule -> AW2 `check.py` `tau_AW2`, rejecting any mutation that hard-codes `tau_AW2` instead of deriving it from the AW1 gate's `K_2^+` (loop2-response.md sec. 2-3; assistant-1 README planning note 1).
2. `sign_convention_fixture.py` per `loop3-signoff.md` sec. 4 item 3: PASS iff `sign(<W>)=sign(tau)` under I1.5 for every `j_max` in {1/2,1,3/2}, antisymmetry to O(tau^2), and monotone convergence in `j_max`.
3. Re-run `preregistration_audit.py`'s structural checks (`controls`==`controls_required.ids`, byte-identical) against every AX/AY/AZ contract the moment it freezes, before production, to catch a second instance of the AV2-style mirror gap early.
