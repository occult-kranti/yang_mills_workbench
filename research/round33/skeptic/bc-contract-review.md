# Round33 skeptic: pre-freeze review of the draft contracts BC1 and BC2

**Standing.** This is a prospective review by a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producers. It is not human peer review and not formal verification. Human project author: Hruday N M (BUNZEEY). It admits nothing, and it is not a research loop.

**Previews.** Every preview number (every computed constant, margin, ratio and the value of `N_sign`) sits only in the section marked **Advisor only** at the end, and in `previews_recomputed` of `bc-contract-review.json`. No replacement text contains one; `build_review.py` checks this. The exact rationals come from `fractions.Fraction` in my private scratch folder `/tmp/claude-0/skeptic-bc-private/`:
- `bc_values.py`: previews, margins, admissibility, `N_sign`;
- `edits.py`: the replacement texts;
- `scan.py`: field-level phrase scans;
- `controls.py`: where each control id is defined;
- `build_review.py`: the freezer and scan runs on edited copies;
- `write_json.py`: the JSON.

That folder is not evidence and not a premise. **No producer may receive it, this file or `bc-contract-review.json`.**

**Order of work, disclosed.** I wrote and ran `bc_values.py` (04:06:08Z) before I read §10 of `experts/modern/bc2-targets-proposal.md`, then compared. Every value I recomputed agrees exactly with §10. I did not recompute the `polymer_kp` column, because BC2 does not permit that route.

Having read §10, my later BC2 pre-comparison replay cannot claim ignorance of the proposal. Its independence rests on my own code, which was written first. The proposal's distribution note excluded the skeptic's replay; the advisor's instruction for this review overrides it, and I record the exposure here.

**Read.**
- The drafts `contracts/bc1.json` (commit d0adac9) and `contracts/bc2.json` (commit a717454), with sha256 in the JSON; `advisor/selection-bc1.md`, `advisor/selection-bc2.md`, `advisor/panel-update-2.md` and `advisor/plan.json`.
- The modern `bc2-targets-proposal.md` in full, including the advisor-only §10.
- My record: `triage.md` (BC lines), `prospective-controls.json`, `loop2-review.md` P8–P9, `bb-contract-review.md`/`.json`, `bb2.md`.
- Gates: AV1, AV2, AW1, AW2, AX1, AX2, AY2, BA1, BA2, BB1 and BB2.
- Reports, for the premise checks:
  - AV2 forward §§1–2, 4–5 and 11–13, and AV2 reverse §§1, 4, 6 and 12–13;
  - AX1 forward §7 (F19–F20), with the AX1 reverse flip section;
  - AX2 forward §§6 and 10, and its calculator (run once with `-B`; no cache written);
  - BB1 reverse §§0 and 3–5 (the split route and R13);
  - AY2 forward (the O1–O6 table);
  - the AV2 contract preregistration.
- Tools: `freeze_contract.py`, `phrase_scan.py` and `record_gate.py`.

No BC production exists yet.

## Decision

- **BC1: `freeze_after_blocking_edits`.** It has 2 blocking issues, 6 field edits, plus the shared plan issue.
- **BC2: `freeze_after_blocking_edits`.** It has 5 blocking issues, 17 field edits, plus the shared plan issue.
- **plan.json: 1 blocking issue** shared by both contracts: the gate-field vocabulary, 7 entries.
- **30 blocking field edits** in all. **`signoff: false`** until they are applied.

The drafts as committed pass `freeze_contract.py` on copies (34 and 35 premises). The copies with the blocking edits also freeze, BC1 first and then BC2 (34 and 36 premises), and so do the copies with every edit. The control mirrors are equal. Neither the templates nor any other field produces an affirmative forbidden-phrase hit.

None of the blocking issues is a tool failure; they are content defects. After the edits I need no further loop, and I will check the frozen bytes against the JSON before my pre-comparison work.

## The questions asked

### 1. Executability

Both drafts are executable in shape. Controls, mirrors, templates and gate fields are all present, and the freezer passes. Two items are not executable from the declared premises as written:
- **BC2 item 5** asks for a replay of the AX2 calculator, which is not a premise (issue BC2-4).
- **BC2 item 2a** asks for an "explicit bound" but states none (issue BC2-3).

### 2. BC1 item 3: `N_sign`

The item is provable from the declared premises. The chain:
1. The BB2 gate gives `sup_{M>N} ||rho^{F2,M}_R - rho^{F2,N}_R||_1 <= C' q^(N-1)` for the untruncated vectors at fixed `N`. Letting `M -> inf` gives `||rho^{F2,N}_R - rho^inf_R||_1 <= C' q^(N-1)`, and BB2 item 2 makes `rho^inf` the common limit.
2. The AW2 gate encloses `omega_inf(W)`, because the limit equals every AQ1 subsequential state (BB2 item 3), and AW2 covers the whole set.
3. `||W|| <= 1` and trace duality give the widening by `C' q^(N-1)` on both sides.

I checked exactly that the AW2 endpoints equal `tau/144 -/+ K_2^+ tau^2`. I then computed `N_sign` with the BB2 gate's **bound value** `C'` (the nested-telescoping value at the hypothesis values).
- The labelled union-comparison `C'` and the labelled re-evaluated `C'` give the same `N_sign`. The result is therefore robust to which BB2 value a producer reads, but the contract should pin the bound value (non-blocking edit to `finite_box_sign`).
- The value is in the advisor-only section.
- Nothing is claimed for `2 <= N < N_sign`. That range should be an obligation row, not a failure (non-blocking).

Two scope points (non-blocking):
- **The corollary is for the untruncated F2 ground vector.** The BB2 per-cutoff bounds compare cutoff-L densities, whose `M -> inf` limit is a cutoff-L state, not `omega_inf`. A cutoff-L F2 sign would need another chain: AW2's F1 boxes at cutoff `L`, plus closedness, plus the per-cutoff c3 comparison. The contract should say the cutoff-L F2 states are not claimed.
- **The F1 wording "at every cutoff" is the AW2 gate's.** The untruncated F1 vector follows by the AV1 gate's cutoff-vector removal and the closed interval. That is agreement, not re-derivation, and should be said.

### 3. BC1 item 4: what the AV2 record proves about finite boxes

**It does not prove a finite-box node.** The evidence:
- The AV2 gate quantifies over "every AQ1 subsequential state of the centered whole-star construction (each chosen state separately)". Its model is the AT4 chosen AQ state, and the contract's `state_provenance` is `AQ1_centered_whole_star_subsequence`.
- The window lemma and the real-time comparison are stated for the GNS vector of that state, with AQ1 §5 nonnegativity:
  - forward: HNM-AV2-F01, F02, F07 and F15;
  - reverse: R01, R02, R08 and R13.
- **The only box-by-box step is the seven-star slope.** It appears as F13–F14 in the forward and R12 in the reverse, and the record passes it to the AQ evolution by AQ1's norm convergence.
- The AV2 reverse executes a "finite-box provenance" as a damaging mutation of `changed_model_relabelled` (its §12 control table). The admitted record treats a finite-box certificate as a different model.
- The AW1 gate item (1) gives the finite-box `C_N(s)` only with an explicitly non-uniform `tau^2` constant.
- AV1 proves the state bound `D` per box, and AV2 proves the slope per box. The window lemma for the finite-box vector would be easy: the generator `G_N - E_N >= 0` and the same `M_0`, `M_1`. **But it is a new derivation, not a restatement.**

The drafted item leaves this determination to the producer. It also carries its own argument for the new derivation (window lemma, uniform slope, volume-uniform `D`), which invites exactly the mislabelled "restatement" that `finite_box_node_only_from_record` is meant to reject. No gate field or acceptance clause records the item's outcome.

**Blocking (BC1-1):**
- freeze the determination;
- restate no finite-box node for F1 or F2;
- keep two obligation rows, each with its missing premise;
- rewrite the control semantics;
- add `finite_box_node_claimed: false`;
- name the outcome in the acceptance text.

If the advisor wants the F1 finite-box node, it must be a new, labelled derivation item with its own premises: AW1's finite-box `C_N(s)`, AV1's per-box `D`, and AV2 F13–F14/R12. It then no longer fits a pure statement loop. I do not recommend adding it in BC1.

### 4. BC1 common GNS item (P8): scope

It is within scope, and P8 is met.
- One state (BB2 items 2–3) has one GNS triple, up to unitary equivalence.
- Its GNS dynamics is the unique unitary implementation of `T_theta` fixing `Omega`. It exists by AQ1 stationarity, which BB2 item 3 inherits.
- BA2 item 4 identifies the F2 limit dynamics with `T_theta`.
- The correlation functions on `|theta| <= 8` are BB2 item 5, with the rate in N only on `5<=N<=14000`.

Nothing here is equality of the GNS dynamics of different states, and `gns_dynamics_equality_claimed` stays false. The gate field `dynamics_limit_identified_claimed: true` is exported but not defined in BC1; it restates BA2 item 4 (non-blocking edit to `gate_fields_rule`).

### 5. BC1 `resolved_interaction_shift` (blocking, BC1-2)

In Round32 this flag named its observable:
- AV2's `results.json` exported `false`, for `C(s)`;
- AW2's `results.json` exported `true`, for the static `omega(W)` only, and its gate says so.

BC1 restates both certificates in one gate. `false` contradicts the restated AW2 content, and `true` would contradict AV2.

**Replacement:**
- export `correlation_shift_resolved: false` (the AW2 flag name for `C(s)`);
- drop `resolved_interaction_shift` from BC1;
- the static mean is already carried by `sign_certificate_restated_for_limit` and `finite_box_sign_claimed`.

BC2 keeps `resolved_interaction_shift: false`, which is consistent with AX1/AX2, where route B has neither a node shift nor a Wilson-mean sign.

### 6. BC2 disc admissibility, route-A extremes, circle bound

All verified exactly with the AM2 rational bounds `G(R) < 148/7` and `G'(R) < 352`. These are the `e^{1/8} < 8/7` bounds; I checked that they dominate a 40-term Taylor enclosure.
- **Disc `rho = 64|tau|` under `J' = 29|tau|`:** the self-map `29 rho G(R) <= R` holds with wide room. The Lipschitz constant `29 rho G'(R)` and the exclusion constant `2*29 rho G'(R)` are far below 1.
- **Route-A extremes.** The disc radius `1/37888` and the split weight `1/(37888|tau|)` **fail the route-B self-map**. With the true `G(R)` they fail too.
  - They **pass the contraction test.** So the rejection in `disc_admissible_under_J_prime` must test the self-map; testing the contraction alone would accept them. The drafted semantics names both conditions, so it is correct, and the checker must execute the self-map rejection.
  - I also checked the identity `28 * (1/37888) * 148/7 = 1/64` exactly: route A sits on its own self-map boundary.
- **Split weight `W = 1024`:** admissible under the route-B weighted self-map and contraction, with `lambda = 2/W < q`.
- **Circle bound:** `T_B(rho) = (52 rho/144)/(1 - 29*352 rho)`.
  - At `rho = |tau|` it reproduces the AX1 gate `T' = 13/3599632512` exactly.
  - The same formula with `(49, 28)` reproduces the BA1 gate `K` exactly, and my split code reproduces both BB1 `iterated_split` rationals exactly. The formula chain is anchored to admitted values.
- **Region factor.** `(1+t)^2 <= 1+10^-8` holds with the route-B anchored bound, with less room than route A. It is not a step of the iterated-split route, whose bound needs no `e^{|Y|/10^8}` factor (BB1 R13). Keep it as a fixture (non-blocking wording).

### 7. BC2 targets against my own previews

Every target clears the plan's freeze-time margin of 2.
- The binding margins are `c_site,B` and `K_B`, nearly equal: `c_site,B` is almost entirely its near term `2K_B`. For the frozen `iterated_split` route both lie a little above the required margin, and they confirm the proposal's binding figure. The proposal's own binding value is its `polymer_kp` preview, a route BC2 does not permit.
- `C_B`, `C'_B` and `c'_site,B` have wide margins.
- The doubling variants behave as the proposal feared:
  - a union-volume density comparison would make `c_site,B` miss T2, and the direct-comparison requirement prevents it;
  - a telescoped coefficient input keeps above 2, but thinly.
- Numbers are in the advisor-only section.

### 8. T4 at `1/400000`: well posed?

**Yes, once the region domain is stated.**
- The T2 and T4 forms, and items 3–4, omit "for every finite complete-factor region `Y` inside `Lambda_N`". For `Y` not inside `Lambda_N` the box density on `Y` is undefined and `d_Y < 0`. BB1 froze the domain; BC2 must as well (blocking, BC2-2).
- T3 and T4 are consequences of T1 and T2 up to the assembly factor: 1 for a direct c4B comparison, `1/(1-q)` for nested telescoping. They are not independent discriminating thresholds, and the target note should say so (non-blocking).
- T4's `1/400000` leaves room above the telescoping factor. T3 equals T1's target, so a telescoped T3 needs `C_B` below `(63/64)` of T1's target. With the actual margin this is harmless, but it is asymmetric.
- For fixed `Y` the region rate holds for every `N` with `Y` inside `Lambda_N`. There is no BB2-item-5-type vacuity (D12), because `|Y|` is fixed.

### 9. Does the node restatement need only identification on every finite region?

**Yes.** The chain:
1. Identification on every finite region is identification as states on the quasi-local algebra: local algebras are norm-dense and states are continuous. This gives the same GNS triple.
2. The dynamics is the state-independent route-B limit dynamics (AX1 item 3).
3. `G >= 0` and the state term `D'` pass by identification. `D'` also passes directly through the closed trace-norm ball.
4. The window lemma depends only on `g`.

No route-B dynamics comparison, rate, common limit or uniqueness is needed. Two conditions matter:
- The identification must be with the **untruncated** AX1 construction, with the cutoff removed at fixed `N`.
- It needs a region-form Cauchy bound **at some proved constant**, not at the T4 target. A region constant above T4 is a limited outcome for that constant; the node restatement still stands. The drafted `region_form_load_bearing_for_node` should say so (non-blocking).

### 10. The exhaustion item (2a)

The contract says "with the explicit bound" but gives none. The correct bound follows from one direct c5B comparison of `V_k` with `Lambda_{N_k}` and the item-1 Cauchy bound, with `M -> inf`:

`||rho^{V_k}_Y - rho^inf_Y||_1 <= (c_site,B + c'_site,B) |Y| e^{|Y|/10^8} q^(N_k - max_{y in Y}|y|_inf)`

Here `N_k` is the largest `N` with `Lambda_N` inside `V_k`, and `Y` is inside `Lambda_{N_k}`. Every exhausting sequence of finite complete-factor route-B volumes has `N_k -> inf`, so this covers all of them. It stays within one prescription.

**Blocking (BC2-3):** state it. The replacement for item 4 also names the item-2b premise.

### 11. The pointwise sign mirror: its premise in AX1

**Present.** The AX1 forward F19–F20 and AX1 gate item (7) give `U_E H_N(tau) U_E^* = H_N(-tau)` in every centered box and every cutoff compression. `U_E` is a product of one-link unitaries, which makes the restriction to any `Y` immediate. The finite grounds are unique.

AX1 has the mirror only as an equality of whole sets (pointwise along a common subsequence). Whole-sequence convergence at both signs makes it pointwise on every finite region. The `-tau` statement remains a mirror replay with no real `g`.

### 12. Premise completeness and external theorems

- **BC1.** All listed files exist, and the freezer checks this. Two non-blocking points:
  - "which Round32 limitations the Round33 gates lift" is unbounded, since the Round32 HANDOFF and roadmap are not premises. The replacement scopes it to the gates in `shared_premises`.
  - The AY2 falsifying scenario should be recorded as excluded only for F1/F2, per my prospective control `falsifier_excluded_only_for_named_families`.
- **BC2.**
  - **Missing:** `research/round32/forward/ax2/calculator.py`, which item 5 replays (blocking, BC2-4).
    - It imports only `fractions`, `math` and `re`.
    - Run with `-B` at its fixed design, it returns the AX2 gate `d` and `R'` exactly. I checked that no cache was written.
    - An own re-implementation need not reproduce the gate rationals exactly: `d` is an algorithm-dependent midpoint, and `R'` is an outward rounding at `10^-40` of a Machin-pi value, the AV2 lesson.
  - **No external theorem needs a committed excerpt.** The iterated split is self-contained (BB1 gate). The disc lemma uses the maximum principle and Banach, standard and accepted as such in BA1/BB1. Trace-class completeness is standard. Nachtergaele–Sims, Kato and Peter–Weyl enter only through inherited AX1/AQ1 statements; nothing new is quoted. There is no Kotecký–Preiss use.
  - Say explicitly that `polymer_kp` is not permitted (non-blocking edit to `parameters.weights`).
- **P7-type isolation.** No `experts/` file, plan, panel update, triage, prospective controls, contract review or deliberation is a premise of either contract.

### 13. Control mirror and semantics coverage

- The mirrors are equal, with no duplicates. Every control id has frozen semantics somewhere (`controls.py`).
- **BC2 (blocking, BC2-1).** For six inherited ids, the latest frozen semantics are route-A or BB-specific texts that either prescribe route-A inputs or contradict BC2's own new semantics:

  | id | frozen definition | conflict |
  |---|---|---|
  | `every_site_coefficient_input` | BB1: BA1 inputs | `route_b_constants_not_route_a` |
  | `tier_mixing_rejected` | BB2: hypothesis source `bb1_frozen_targets` | BC2 has no hypothesis layer |
  | `rate_constant_pair_prefrozen` | BB1: weights up to `1/(37888|tau|)` | inadmissible under `J'` (`disc_admissible_under_J_prime`) |
  | `global_lipschitz_not_decay` | BB1: hard-codes route-A constants | silent route-A constants |
  | `translation_invariance_separate_item` | BB2: "(union comparison)" | `direct_comparison_required` |
  | `normalization_couples_supports` | BB1: carries the D1 defect (a support strictly containing R moves `rho_R` at first order) | `route_b_first_order_marginal` |

  A producer implementing the inherited texts would embed exactly the silent route-A constants that the modern lens calls the main risk. The replacements give BC2-specific semantics.
- **Non-blocking.**
  - `changed_model_relabelled` (it tests the opposite direction), `limit_identified_with_aq1_limits` and `cutoff_uniform_then_removed` get route-B texts.
  - The other inherited ids are defined only in contracts that are not premises (`ba1`, `ba2`, `bb1`, `bb2`). Either add those four contracts as premises, with BC2's semantics overriding, or give every inherited id its own text. This is the BB2 limitation D6 recurring; it applies to BC1 as well.
- **BC1.** The inherited ids are generic or zero-selected and fit. The item-4 control is rewritten under BC1-1.

### 14. Wording

- **Placeholders:** none (R1 passes).
- **Forbidden phrases:** no affirmative hit in any field of either draft or of the edited copies. I used the tool's own `phrase_scan.scan` with round, contract and plan lists, excluding the forbidden lists themselves. Templates were also scanned without removal.
  - A raw-file run of `phrase_scan.py` on a contract JSON hits only its own `forbidden_phrasings` and exclusion lists, so it is not a meaningful test.
- **Rate-range lesson** (panel-update-2 lesson 1; D12):
  - **BC2's template** says "at a rate in N" with no range in its clause, and BC2 has no `rate_range_stated` control (blocking, BC2-5). The replacement template adds "that holds for every N at least 2 with the region inside the box". The content is unchanged, since the density rate holds for every such `N`. The replacement passes all scans.
  - **BC1** has 8 fields with "rate" not followed by "in N", which the plan vocabulary forbids: `selection_reason`, `parameters.obligations`, `required[2]`, `required[4]`, `acceptance` and three spans in the `rate_range_stated` semantics. Non-blocking replacements are given; one of them, the acceptance text, is inside BC1-1.
- **Templates:** both are one literal span with no slot a producer must fill ("the exactly computed N_sign" is a symbol). Each can be quoted verbatim.
  - Both templates assert every item, so a limited gate cannot quote them truthfully. `record_gate.py` R7 still requires the span. BC2 gets a limited-outcome frame in `gate_fields_rule` (non-blocking), and BC1 should add the same.

### 15. Gate fields against the plan vocabulary (blocking, PLAN-1)

`plan.json` `vocabulary.gate_fields` lacks the following fields that the drafts export:
- `node_certificate_restated_for_limit`;
- `sign_certificate_restated_for_limit`;
- `finite_box_sign_claimed`;
- `finite_box_sign_scope`;
- `resolved_interaction_shift`.

It also lacks the two fields the BC1 edits add: `finite_box_node_claimed` and `correlation_shift_resolved`.

Loop-2 item P3 requires closure. The freezer does not check it, because R10 covers tiers and sub-labels only. Add the 7 entries and record the extension with plan.json's sha256 at the freeze (P5).

BA1's `coefficient_cauchy_scope` was already outside the vocabulary. That is a historical gap; record it, and do not edit BA1.

Sub-labels and tier names pass R10. BC1's `sign_certified_below_cap` passes R10 but does not apply: AW2 says so at the cap, and BC1 works at the cap. Replace it with `static_not_dynamic` (non-blocking).

### 16. R4

- **BC2's** `state_provenance`, `clock` and `error_terms_itemized` are unique across all Round32 and Round33 contracts.
- **BC1's** `clock` equals the BA1, BA2, BB1 and BB2 clock text. These are the same family (`AQ_patterned_zero_selected`), which R4 allows.

### 17. Scaling brackets

- **BC2:** all ratios fall inside `[95,105]`. `q`, `rho/|tau|` and the datum are exactly 1. The node-radius replay is recorded, not a target.
- **BC1:** there is no bracket, correctly. The drafted "half-width at tau and tau/100 for information only" names no `N`. A value at `tau/100` would look like an admission below the cap, although AW2 admits only the cap. Also, `C'` at the hypothesis values does not depend on `tau`. Non-blocking replacement given.

### 18. Acceptance, limited and insufficient

- **BC1:** the acceptance text omits item 4's outcome. Fixed in BC1-1, which also names the untruncated F2 state and the `C'` bound value.
- **BC2:** the acceptance text requires T0 "for the untruncated vectors". T0 is a coefficient statement per cutoff space; BA1 excludes untruncated coefficients. It also requires T3 and T4 "for c1B, c4B and c5B", but they are whole-sequence targets. Non-blocking replacement given.
- The limited and insufficient branches are sound, and a failed route is never evidence that two states differ.

### 19. `selected_after` for parallel freezing

BC2's `selected_after` names `bc1-gate.json`, which does not exist yet, with a note. R8 passes.
- It states a selection order that does not exist. BC2 is selected after the BB1 and BB2 gates, its plan condition, and uses no BC1 result.
- The BB2 precedent named an existing earlier gate (`ba2-gate.json`).

**Recommended (non-blocking):** `selected_after: research/round33/advisor/bb2-gate.json`, with a note saying "frozen together with BC1; selected after the BB1 and BB2 gates; its gate recorded after the BC1 gate". Freeze BC1 first in any case. BC2 does not snapshot `bc1.json`, so the order is not load-bearing.

## Blocking issues (30 field edits; exact texts in the JSON)

**BC1 (2 issues, 6 edits):**
- **BC1-1. Finite-box node determined from the record.** Edits:
  - `required[3]`;
  - `new_control_semantics.finite_box_node_only_from_record`;
  - add `gate_fields_required.finite_box_node_claimed: false`;
  - `acceptance.accepted_within_scope`.
- **BC1-2. Ambiguous `resolved_interaction_shift`.** Edits:
  - remove it;
  - add `correlation_shift_resolved: false`.

**BC2 (5 issues, 17 edits):**
- **BC2-1. Inherited semantics conflict with route B.** Six added `new_control_semantics` entries: `every_site_coefficient_input`, `tier_mixing_rejected`, `rate_constant_pair_prefrozen`, `global_lipschitz_not_decay`, `translation_invariance_separate_item` and `normalization_couples_supports`.
- **BC2-2. Region-form domain.** The T2, T4 and T3 forms.
- **BC2-3. Explicit exhaustion bound.** `required[3]`, which also carries the domain, the rate range and the item-2b premise.
- **BC2-4. AX2 calculator as a premise.** Edits:
  - append it to `shared_premises`;
  - `required[4]`;
  - `node_values_unchanged`.
- **BC2-5. Rate-range lesson.** Edits:
  - the template;
  - add `rate_range_stated` to `controls` and to the mirror;
  - its semantics.

**Shared (PLAN-1, 7 entries):** `plan.json` `vocabulary.gate_fields` gains the seven fields listed in question 15.

## Non-blocking (28 entries in the JSON)

**BC1:**
- `finite_box_sign`: untruncated vectors; the `C'` bound value; nothing claimed below `N_sign`; F1 through the AV1 removal.
- The `finite_box_sign_scope` text.
- Sub-labels: `static_not_dynamic` in place of `sign_certified_below_cap`.
- `gate_fields_rule`: define `dynamics_limit_identified_claimed`.
- The rate wording in `selection_reason`, `required[2]`, `required[4]` and the `rate_range_stated` semantics.
- `parameters.obligations`: add rows for the F2 sign below `N_sign`, non-centred F2 volumes (AY1 local reading) and BC2 as a parallel loop.
- Align the preregistration `claim_exclusions` with the top-level list.
- The `N_sign` scaling note.
- The tier-label route rule.
- `required[5]`: the AY2 falsifier and the bounded Round32 limitations.

**BC2:**
- `selected_after` and its note.
- The acceptance text.
- The target note (T3/T4 are consequences).
- Pin `T_B(|tau|)` to the AX1 gate `T'` in `route_b_constants_not_route_a`.
- `parameters.weights`: `polymer_kp` not permitted.
- `required[2]`: the region domain, and the region-factor check as a fixture.
- `region_form_load_bearing_for_node`: any proved region constant suffices.
- Route-B texts for `changed_model_relabelled`, `limit_identified_with_aq1_limits` and `cutoff_uniform_then_removed`.
- `required[6]`: byte-identical under `-B` and `-B -O`.
- `gate_fields_rule`: the AX2 meaning of `resolved_interaction_shift`, and a limited-outcome frame for the template.

**Both:** the defining contracts of the inherited ids as premises, or self-contained semantics (D6).

**plan.json:** `subrounds[2].selection_note_paths` (P12). Record the plan sha256 at the freeze (P5).

## Against my own record

- **P8 is met.** BC1 is statement+skeptic, the common GNS item is named, and the Round32 gates are untouched.
- **P9 is met.** BC2 is single+skeptic, every route-B constant is re-derived, and the condition holds: BB1 and BB2 are both `accepted_within_scope`.
- My triage line for BC2 ("BA1, BB1 and BB2 re-instantiated with its own constants") is implemented, with one family, exhaustion and the mirror in place of a common limit. That is sound, because the admitted record has no second route-B family (AX1 limitation 1; AY1/AY2 scope).
- **D6 recurs in BC2 with teeth.** The inherited texts are route-specific, which is why BC2-1 is blocking here, although D6 was non-blocking at the BB2 gate.
- **The D12 lesson is applied (BC2-5).** I missed the absence of `rate_range_stated` in BC2 until this review; no earlier review of mine saw the BC2 draft.

---

## Advisor only: previews (not for producers or replay inputs)

These are exact Fractions from `bc_values.py`; the decimals are truncated, and the exact rationals are in `previews_recomputed`. All values are at `|tau| = 10^-8`, and both signs replay the same `|tau|` formula.

**BC1 item 3.**

| N | `C' q^(N-1)` | widened lower endpoint | sign certified |
|---|---|---|---|
| 2 | 6.349e-8 | −6.342e-8 | no |
| 3 | 9.921e-10 | −9.230e-10 | no |
| 4 | 1.550e-11 | **5.3608e-11** | **yes** |
| 5 | 2.422e-13 | 6.8867e-11 | yes |

- **`N_sign = 4`**, with `C' = 4/984375`, the BB2 bound value.
- It is the same with the labelled `C' = 1/250000` and with the labelled re-evaluated `C'`.
- At `tau/100`, for information only, it would be 5.
- At `N = 4` the ratio of the lower endpoint to the widening is about 4.46.

**BC2 admissibility.**
- **Route-B values at `rho = 64|tau|`:**
  - self-map `1073/2734375 <= 1/64`;
  - Lipschitz `2552/390625`;
  - exclusion `5104/390625`.
- **Route-B maxima:**
  - disc radius `7/274688`, about `2548|tau|`;
  - weight `W_max = 2734375/1073`, about 2548.35.
- **`W = 1024`:** self-map `17168/2734375`, Lipschitz `40832/390625`.
- **Route-A extremes under `J'`:** self-map `29/1792 > 1/64` (0.016183; 0.016046 with the true `G(R)`); Lipschitz 0.2694 < 1.
- **Region factor:** `(1+t_B)^2 - 1 = 93590445481/12957354221447430144`, about 7.223e-9. The room is 1.384, against route A's 1.469.

**BC2 constants and margins (iterated_split, the frozen route).**

| constant | exact | decimal | target | margin |
|---|---|---|---|---|
| `K_B = 2T_B(64|tau|)` | `13/27941256` | 4.652618e-7 | 1/1000000 | 2.14933 |
| `C_B` | `2326328761843649826272217312701707175/2461302090348550272620124432958434944821248` | 9.451618e-7 | 1/250000 | 4.23208 |
| `c_site,B` | `35789673259133074250341804810795495/38457845161696098009689444264975546012832` | 9.306209e-7 | 1/500000 | **2.14910 (binding)** |
| `C'_B` nested (`×64/63`) | exact in JSON | 9.601644e-7 | 1/250000 | 4.16595 |
| `C'_B` direct c4B | `= C_B` | 9.451618e-7 | 1/250000 | 4.23208 |
| `c'_site,B` nested | exact in JSON | 9.453926e-7 | 1/400000 | 2.64440 |
| `c'_site,B` direct c4B | `= c_site,B` | 9.306209e-7 | 1/400000 | 2.68638 |

- **Split intermediates:**
  - `t_0 = 13/1799816256`;
  - `t_W = 26/3148137`;
  - `beta* ≈ 3.30376e-5`;
  - `S_lambda = 2169/343`.
- The near term `2K_B` is 99.990% of `c_site,B`.
- **τ → τ/100 ratios:** `K_B` 100.6510 (`39059948/388073`); `C_B`, `c_site,B`, `C'_B` and `c'_site,B` 100.6615. All are inside `[95,105]`.
- **Variants:**
  - union-volume factor 2 on `c_site,B`: margin 1.0746 (fails);
  - on `C_B`: 2.116;
  - telescoped coefficient input on `c_site,B`: 2.1155.
- **Exhaustion constant** `c_site,B + c'_site,B`: about 1.861e-6 (direct), or 1.876e-6 (telescoped).
- **Agreement with §10:** every value above matches the proposal's §10 exactly. The proposal's binding 2.14888 is its `polymer_kp` preview, a route that is not permitted.

No result here is a Round33 finding, a loop or a fraction of the continuum problem. The four-dimensional Yang–Mills existence and mass-gap problem remains open.
