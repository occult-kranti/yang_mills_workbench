# Jung/Pauli lens, Round32 sub-round 3 -> sub-round 4 update

Advisory only; model-agent lens with correlated ancestry to the advisor, producers and skeptic. No historical-person participation or endorsement. Human project author: Hruday N M (BUNZEEY); AI-assisted.

## 1. Observation-map assessment of sub-round 3

**Vocabulary extension: acceptable, correctly recorded.** `plan.json.preregistration_vocabulary_extensions` (dated 2026-09-24, reason "Jung assistant-2 audit found three schema gaps") is a dated, reasoned history entry, not a silent contract edit. The AX1 contract itself is unamended; `ax1-gate.json.limitations` records the symbolic triple as "an accepted pre-registration vocabulary extension (plan.json)" timestamped after the AX1 freeze, and the skeptic (N10) confirms both checkers parse and verify the triple. **Rule preventing recurrence:** repair-by-record (AGENTS.md) plus prospective use — the extended vocabulary (symbolic tau expressions, `statement+skeptic`/`statement-only` direction, `n/a`/`grid` fields) is written directly into the AX2/AY1/AY2/AZ1/AZ2 preregistrations from the start, so no later contract needs a retroactive fix; only AX1 is grandfathered, and only by an explicit gate note, never by editing `contracts/ax1.json`.

**Mis-rounded threshold: handled correctly, non-blocking.** The frozen contract's "D'<=4.19e-7" is infeasible; the exact threshold is `[41883,41884]/10^11`. Both producers and the skeptic (N2) found this independently and did not amend the contract; the gate binds the exact rational `D'` and the actual target `4/10^7`, which lies safely below the threshold either way, so the wrong-way-rounded prose note never entered the admission path. Good discipline: text notes are advisory, only exact-rational comparison is decisive.

**"Bounds versus counts": correctly separated.** The contract's "candidates 96 (4x24) and 168 (7x24)" are upper bounds only; both producers derive and the gate binds the exact counts 52 per factor and 88 meeting R (N3). No certificate substitutes a bound for a count.

**Uniform label discipline: maintained.** "Uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling" is the fixed model string in `ax1-gate.json`, `ax2.json`, and carried into `az1.json`/`az2.json` (`uniform_label_strong_coupling` control). "Weak coupling" and "continuum" remain listed `claim_exclusions` in every one of ax1/ax2/ay1/ay2/az1/az2 and are asserted false in every results.json seen so far.

## 2. Goals for sub-rounds 4-5

- **Sub-round 4 (AY1/AY2).** No change: `ay1.json` already implements the loop-2 mandatory sentence template and family/topology freezing verbatim.
- **Sub-round 5 (AZ1/AZ2).** No change: AZ2 keeps `transfers_to_aq:false`/`model_is_finite_graph:true` and the roadmap-goal-2 exclusion I required in loop 2 sec.1; AZ1 keeps the bridge obstruction and `loop_count_not_fraction`.

## 3. AY1/AY2 and AZ1/AZ2 pre-registration specifics

**Mandatory sentence template (AY1 required item 4, text from my loop-2 response sec.4):** for every pair of subsequential limits omega', omega'' of families F1, F2 at the same tau, and every A in B(H_R) with ||A||<=1: |omega'(A)-omega''(A)| <= constant(tau); this is uniform local closeness on a fixed region at fixed coupling, not equality, whole-sequence convergence, translation invariance or a rate in N.

**Gate fields — one gap to flag.** `ay1.json` required item 4 pins `uniqueness_claimed:false`, `whole_sequence_claimed:false`, `rate_claimed:false`. `translation_invariance_claimed:false` is **not** separately listed there, although "translation invariance" is a `claim_exclusions` entry and no control id names it explicitly either (only `local_closeness_not_uniqueness`, `subsequence_versus_whole_sequence`). The AY1 skeptic should add `translation_invariance_claimed:false` as an explicit exported field, not leave it implicit in the exclusions list.

**Two families frozen before comparison:** centered whole-star boxes Lambda_N (AQ1) and all-contained-face boxes with I1 sec.6 padding — both named in `ay1.json.parameters.families` before any AY1 outcome.

**Observable class frozen:** `||rho_R-rho'_R||_1` and the first-order density `rho^(1)_R` on B(H_R), trace norm, Haar reference, centering "none" — fixed in `ay1.json.preregistration.observable` before production; matches my "frozen before the comparison and never enlarged after inspection" rule.

**AZ1/AZ2 finite-graph labels and forbidden transfer sentence.** AZ2's model line states `model_is_finite_graph:true; transfers_to_aq:false` directly, with controls `finite_graph_model_id`, `own_free_reference`, `no_transfer_to_aq`, `fg_coefficients_not_fitted`. Its `claim_exclusions` explicitly forbid "any statement about the AQ model's shift or K_2 from the graph" and "resolution of roadmap goal 2" — the exact forbidden transfer sentence my loop-2 condition (iii) required. AZ1 stays a trajectory statement (no finite-graph mixing) with `bridge_obstruction_retained` and `e_star_fixed_no_plateau`.

## 4. Occult/mystical sources

None: no occult, mystical or synchronicity source appears among the AX1/AX2 shared premises, inputs or bindings; nothing changed a premise, force, Hamiltonian term or coupling value in sub-round 3.

## 5. Assistant tests wanted after sub-round 4

1. Grep `ay1`/`ay2` reports and results.json for "unique", "whole sequence", "the AQ state" appearing without an adjacent "not"/"never"/"a chosen subsequential" (forbidden-phrasing check).
2. Confirm the AY1 gate exports `translation_invariance_claimed:false` explicitly (flagging sec.3's gap if it does not), alongside `uniqueness_claimed`, `whole_sequence_claimed`, `rate_claimed`.
3. Recompute `2*D` from the admitted AV1 gate rational (not a recomputed or smaller value) and confirm it is `<=1/1250000`; reject any substitution of AX1's D' in its place, since AY1 binds AV1's tier, not AX1's.
4. Confirm reverse-premise isolation for AY1: the reverse's declared inputs exclude `forward_additional_premises` (triage.md, jung/loop2-response.md).
