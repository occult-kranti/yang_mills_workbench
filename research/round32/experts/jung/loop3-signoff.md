# Jung/Pauli lens, deliberation loop 3: sign-off

Advisory, 2026-09-23. Read: loop2-response.md (my position/pre-registration block), deliberation-2.md, deliberation-3.md, plan.json, contracts/av1.json, contracts/av2.json.

## 1. Sign-off

No veto: plan v2, contract AV1, contract AV2. AZ2's move to sub-round 5 (from deliberation-2's "after sub-round 2") is accepted: still labelled, still not a resolution of goal 2, now sequenced after AW2's in-model sign rather than before it.

## 2. Preregistration check

Both contracts' `preregistration` objects carry every field of my loop-2 block (schema, frozen_before_any_outcome, model_id, selected_triple_alpha_units, tau{...}, state_provenance, clock, observable{...}, nodes{...}, error_terms_itemized, target{...}, expected_outcome_types, sub_labels_allowed, claim_exclusions, hash_binding{...}, direction). No field is missing. The skeptic's four amendments are present as restructurings, not omissions: `controls_required` is a flat `ids` list (=`controls`) replacing my `{universal,goal_group,extra}` sketch; `hash_binding.check_py_sha256_recorded_before_full_size_evaluation` replaces my `producer_code_committed_before_first_full_size_evaluation`; `error_terms_itemized` is itemized per loop (AV1 differs from AV2); AV1's `target.value`="1/2500000" (=4/10^7).

## 3. Skill edit

Deliberation-3 item 3 only summarizes; it is not the frozen text. Freeze this 10-line block in `lenses-and-evidence.md`:

1. Pre-registration (Round32), freeze before any computed outcome.
2. Freeze-and-hash: model id, selected triple, coupling (both signs), state provenance, clock, observable (centering+exact reference), nodes, itemized error terms, target, outcome taxonomy, claim exclusions; `check.py` reads target/reference from the contract; its own hash recorded before the first full-size evaluation.
3. No post-hoc node selection; whole grids reported; declared pilot runs excluded from the count.
4. An enclosure containing the matched free reference is `reference_unresolved`; no interaction claim however narrow.
5. A sign certified only below the cap is `sign_certified_below_cap`; the coupling change is a model change, not a refinement.
6. A finite-graph result carries `model_is_finite_graph:true`, `transfers_to_aq:false`, and its graph name.
7. Uniform local closeness of subsequential states is never called uniqueness.
8. Cautionary case: Jung's 1952 astrology experiment (pilot folded into the count, post-hoc maxima, thrice-corrected probability).
9. Cautionary case: Besant-Leadbeater's occult-chemistry number-weights (reference built into the readout).
10. Same-author passes are never independent review.

## 4. Three assistant scripts after sub-round 1

1. `tau_zero_null_replay.py` — PASS iff tau=0 gives exact-zero D/k terms and the byte-level diff of tau=10^-14 vs null is attributable term-by-term to D, D^2, k, tail; FAIL if any interacting interval is narrower than null or unattributed.
2. `tau_scaling_exponent.py` — PASS iff exponent p in [0.99,1.01] for linear tiers, [0.49,0.51] for sqrt, [1.99,2.01] for the K_2 remainder at tau in {10^-8,10^-10,10^-12}; FAIL if a linear-labelled tier has p<0.9.
3. `sign_convention_fixture.py` — PASS iff sign(<W>)=sign(tau) under the frozen I1.5 convention for every j_max in {1/2,1,3/2}, antisymmetry to O(tau^2) holds, and convergence in j_max is monotone; FAIL if sign changes with j_max or antisymmetry fails at first order.

## 5. Remaining disagreements
None blocking. Note only: AZ2 is now a formal single+skeptic loop with its own contract/gate rather than an unlabelled assistants' task; accepted only if its gate is never cited as resolving goal 2 and it keeps `model_is_finite_graph:true`/`transfers_to_aq:false`.
