# Jung/Pauli lens, Round32 sub-round 1, assistant-1

Pre-registration audits and tests for the lens (loop3-signoff.md section 4 /
loop2-response.md section 5). **These outputs count zero research loops.** Nothing
here is a producer, a contract, a gate or a skeptical review; nothing computed here
is read back into any contract, gate or skeptical review. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Standard library only (`fractions`, `json`, `re`,
`math`). Run every script with `python3 -B`.

Read before this work: `research/round32/experts/jung/loop3-signoff.md`,
`research/round32/experts/jung/loop2-response.md`,
`research/round32/contracts/av1.json`, `research/round32/contracts/av2.json`,
`research/round32/advisor/av1-gate.json`,
`research/round32/forward/av1/output/results.json` and `check.py`,
`research/round32/reverse/av1/output/results.json` and `check.py`,
`research/round32/skeptic/av1.md` and `av1.json`.

## Files

- `common.py` — shared helpers: contract loaders, exact-`Fraction` re-implementations
  of the AV1 tier (i)/(ii) state-bound formulas and the planned AV2 window-radius
  formula, and independent Machin/Taylor rational brackets for `pi` and
  `exp(-3)/4`. Does **not** import `forward/av1/check.py`, `reverse/av1/check.py` or
  any other producer/skeptic module, per the task instruction; every formula is
  re-derived from the frozen contracts and cross-checked against the admitted
  numbers in `skeptic/av1.md`.
- `tau_zero_null_replay.py` — script 1/3.
- `tau_scaling_exponent.py` — script 2/3.
- `preregistration_audit.py` — script 3/3.
- `results.json` — merged output of all three scripts, plus a `meta` summary.
  Produced by `rm -f results.json && python3 -B tau_zero_null_replay.py &&
  python3 -B tau_scaling_exponent.py && python3 -B preregistration_audit.py`.

## Results

### 1. `tau_zero_null_replay.py` — PASS

The AV1 state bound (both tiers, re-implemented from the frozen contract's `am2_constants`
and item-5 candidate coefficient) is exactly `Fraction(0)` at `tau=0`:
`D_i(0)=0`, `D_ii(0)=0`, with every intermediate term (`t`, `eps`, `T`) also exactly
zero. At the AV1 cap `tau=10^-8`, `D_ii(10^-8)` reproduces the admitted forward AV1
value bit for bit,
`585079838465912592144137406066050/42981220507576537932303142777593983768257`
(~1.3612e-8), confirming the re-implementation matches the frozen record.

The planned AV2 window radius `E = 2(D+D^2) + 49|tau|s/pi`, itemized into
`state + mean_square + kernel_dynamics + arithmetic` (AV2 contract item 4), has its
`state`, `mean_square` and `kernel_dynamics` terms exactly zero at `tau=0` — leaving
`E(0)` equal to the `arithmetic` term alone, taken here as the width of an
independently computed Taylor bracket of `exp(-3)/4` (~7.28e-34 at this script's
precision). This reproduces, from first principles, the behavior AV2's own control
`tau_zero_null_replay` (`new_control_semantics`) requires. At `tau=10^-8`,
`E(10^-8) ~ 1.8320e-7`, matching the skeptic's independent preview in `av1.md`
("about 1.83e-7") to four significant figures.

The resolving-power ratio `rho = E(10^-8) / (|tau|/144) ~ 2638`. Since `rho > 1`, the
certificate is labelled `reference_unresolved`: the window's own radius is ~2600
times wider than the first-order free-reference distance `tau/144` it would need to
exclude to certify a sign, so **no interaction claim follows from AV2 at this cap** —
consistent with AV2's own `claim_exclusions` and required item 7. A damaging mutation
that mislabels the certificate `reference_unresolved: False` while `rho>1` is
rejected.

### 2. `tau_scaling_exponent.py` — PASS

Fitted exponent `p` of `D(tau) ~ tau^p` at consecutive nodes in
`{10^-8, 10^-9, 10^-10}` (exact-`Fraction` ratios; only the reported `p` itself is a
float):

| series | p (10^-8 -> 10^-9) | p (10^-9 -> 10^-10) | band | in band |
|---|---|---|---|---|
| tier (i) | 1.0000058 | 1.0000006 | [0.99, 1.01] | yes |
| tier (ii) | 1.0000385 | 1.0000039 | [0.99, 1.01] | yes |
| AT4 sqrt `2*sqrt(49\|tau\|/3)` | 0.5 (exact bracket) | 0.5 (exact bracket) | [0.49, 0.51] | yes |

For the sqrt formula, `D_sqrt(tau)^2 = 4*49*|tau|/3` is *exactly* linear in `|tau|`,
so the exact-`Fraction` ratio of squares between nodes equals the exact tau ratio
(10); the reported exponent is therefore exactly `0.5` at both node pairs, not merely
close to it. The label-swap mutation — certifying the sqrt bound under the tiers'
linear `[0.99,1.01]` band, i.e. calling it "linear" — is detected and rejected (its
exponent, 0.5, falls outside that band).

### 3. `preregistration_audit.py` — FAIL (one item; a genuine finding, not a bug in the audit)

| # | item | result |
|---|---|---|
| 1 | AV1 pre-registration block: every field present with an allowed value | PASS |
| 2 | AV2 pre-registration block: every field present with an allowed value | PASS |
| 3 | AV1 `controls_required.ids` equals AV1 `controls` | PASS (25 = 25, identical list) |
| 4 | AV2 `controls_required.ids` equals AV2 `controls` | **FAIL** |
| 5 | AV1 forward `results.json` `checks` contains every AV1 control id | PASS (25/25) |
| 6 | AV1 reverse `results.json` `checks` contains every AV1 control id | PASS (25/25) |
| 7 | AV1 target `1/2500000` read from contract, not hard-coded, in forward `check.py` | PASS |
| 8 | AV1 target `1/2500000` read from contract, not hard-coded, in reverse `check.py` | PASS |
| 9 | gate `accepted` equals skeptic `av1.json` field | PASS (`gate.accepted == skeptic.supported_statement`, byte-identical, 2326 chars) |
| 10 | gate `limitations` equals skeptic `av1.json.limitations` | PASS (list-identical) |

**Finding (item 4).** AV2's `preregistration.controls_required.ids` has 23 entries;
AV2's top-level `controls` list has 24. The one missing id is
`c1_window_preview_only` — itself a required AV2 control (required item 10: "the
C^1 window is registered as a preview-only control"; `new_control_semantics`
defines its exact rejection condition). AV1's two lists are byte-identical (25
entries each). This is not a false positive: it is a real gap between AV2's
`controls` list (what the contract enumerates as required controls) and its
`preregistration.controls_required.ids` (what a producer's `check.py` would read to
know which controls it must execute), discovered by exact-list comparison before
AV2 goes to production. Items 7-8's absence check for `1/2500000` is AV1-specific,
per the task; the same discipline (grep for the contract path, and for the absence
of the target literal outside a contract-comparison) should be re-run against AV2's
`check.py` once AV2 is produced, checking for `1/1000000` instead.

Full per-field and per-item detail, including the exact rational values, is in
`results.json`.

## Three planning notes for the lens about sub-round 2

**1. The AW2 coupling rule must be evaluated inside `check.py` from the AW1 gate, not
chosen after `K_2` is seen.** Per loop2-response.md section 2 (`tau.rule_if_chosen_later`)
and section 3 (the below-cap gate template): AW1 must freeze, in its own contract,
before any `K_2` value is computed, an explicit *formula* for the largest admissible
`|tau_AW2|` — the template's proposed rule is "the largest admissible value with
`K_2|tau| <= 1/288`". AW2's contract must then set
`preregistration.tau.rule_if_chosen_later` to that frozen formula (not `null`, and
not a numeric literal), and AW2's `check.py` must *compute* `tau_AW2` at run time from
the AW1 gate's admitted `K_2` (read from `research/round32/advisor/aw1-gate.json` by
path and hash, the same pattern AV1's `check.py` uses for its own contract), the same
way `av1_tier_bound` forces AV2's `check.py` to read `D` from the AV1 gate rather than
copy a number. A follow-up assistant script for sub-round 2 should replay this
specific chain (`AW1 gate -> AW2 contract rule -> AW2 check.py tau_AW2`) the same way
`tau_zero_null_replay.py` replays AV1/AV2 here, and should reject a mutation that
hard-codes `tau_AW2` instead of deriving it.

**2. Sub-label rules: keep the five-label vocabulary closed, and match the label to
the mechanism, not the outcome.** Both AV1 and AV2 freeze the identical
`sub_labels_allowed` list (`reference_unresolved`, `sign_certified_finite_graph`,
`sign_certified_below_cap`, `static_not_dynamic`,
`uniform_local_closeness_not_uniqueness`); this audit confirms both contracts carry
it verbatim. For sub-round 2: AW2's below-cap outcome (if any) must carry
`sign_certified_below_cap`, never a bare `limited` with no sub-label, and the gate
statement template in loop2-response.md section 3 must be used verbatim. AZ2 (the
finite-graph task) must carry `sign_certified_finite_graph` together with the two
mandatory flags `model_is_finite_graph:true` and `transfers_to_aq:false` and the
graph's name in every sentence that states a sign (loop3-signoff.md section 1,
condition ii) — never presented as resolving roadmap goal 2. AY's state-identification
sentences use `uniform_local_closeness_not_uniqueness` and must follow the mandatory
template and forbidden-phrasing list in loop2-response.md section 4 exactly (no "the
AQ state", no bare "unique"). No sub-round-2 contract should introduce a sixth label
without a Jung-lens sign-off note amending this list, mirroring how this audit caught
AV2's `controls_required.ids` drifting from its own `controls` list — the same
drift-by-omission risk applies to `sub_labels_allowed` and should be checked by a
follow-up assistant script once AW1/AW2/AZ2 contracts are frozen.

**3. What to freeze, and the freeze-check that should run before production, not
after.** This sub-round's finding (item 4 above) shows that a frozen contract's own
internal lists can silently drift apart (`controls` vs.
`controls_required.ids`) even though both are frozen at the same instant. Before any
AW1/AW2/AZ2 contract moves from `status: frozen_before_production` to producers
reading it, the pre-registration audit performed here — (a) every
`preregistration` field present with an allowed value, (b) `controls_required.ids`
byte-identical to `controls`, (c) the coupling-selection rule is a formula, not a
number, whenever `tau.is_model_change_vs_previous_loop` could apply, (d)
`reverse_premise_isolation`'s forbidden-prefix list actually matches the sibling
loop's file layout — should be run and be clean *before* `check.py` is written, the
same way `freeze.py` is run after. Concretely for sub-round 2: freeze AW1's coupling
formula and AW2's `av1_tier_bound`-style pointer to AW1's own admitted `K_2` (never a
copied literal); freeze AZ2's graph name and `tau_FG` inside its own contract's
`model_id` (`FG(<graph>,<j_max>,<tau_FG>,<convention>,<sector>)`, per the template);
and re-run `preregistration_audit.py`'s two structural checks (items 3-4 and 9-10's
pattern) against every new contract and gate the moment each is frozen, not only
after its skeptical review.

## Reproducing

```bash
cd research/round32/experts/jung/assistant-1
rm -f results.json
python3 -B tau_zero_null_replay.py
python3 -B tau_scaling_exponent.py
python3 -B preregistration_audit.py   # exits 1: the AV2 finding above is a real fail, not a script bug
```
