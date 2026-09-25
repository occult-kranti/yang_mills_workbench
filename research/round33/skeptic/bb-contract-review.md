# Round33 skeptic: pre-freeze review of the draft contracts BB1 and BB2

**Standing.** This is a prospective review by a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producers. It is not human peer review and not formal verification. Human project author: Hruday N M (BUNZEEY). It admits nothing, and it is not a research loop.

Every decimal below is a preview. The exact rationals were computed with `fractions.Fraction` in my private scratch folder `/tmp/claude-0/skeptic-bb-review-private/`:
- `bb_values.py`: previews and margins;
- `scan.py`: phrase scans;
- `controls.py`: control-semantics coverage;
- `build_review.py`: the JSON, and the freezer and scan runs on edited copies.

That folder is not evidence and not a premise. **No producer may receive it, this file or `bb-contract-review.json`.** All three hold previews and route advice.

**Read.**
- The drafts `contracts/bb1.json` and `contracts/bb2.json` (commits bad14fc and 4c8acd3; sha256 recorded in the JSON), with `advisor/selection-bb1.md` and `advisor/selection-bb2.md`.
- `experts/modern/bb-targets-proposal.md` in full, including the advisor-only §7.
- `advisor/plan.json`: vocabulary, contract rules and history.
- The BA1 and BA2 gates.
- My own `triage.md` (marginal-locality section), `loop2-review.md` (P6 and P7), `ba1.md` and the `ba2.md` advice section.
- The tools `freeze_contract.py` and `phrase_scan.py`.
- For the premise checks:
  - BA1 reverse report §§2–4 (Lemmas 2.2 and 3.1, Theorem 4.1);
  - BA1 forward §§1–2 (the weighted norms);
  - AV1 forward §7 (F20–F23);
  - the AY1 and AQ2 gates.

No BB production exists yet: `forward/` and `reverse/` hold only `ba1` and `ba2`.

## Decision

- **BB1: freeze vetoed** until its 7 blocking edits (4 issues) are applied.
- **BB2: freeze vetoed** until its 15 blocking edits (7 issues) are applied.
- **`signoff: false`.**

Once the edits are applied I need no further loop. The edited copies pass `freeze_contract.py`: BB1 first, then BB2, on a scratch extraction of HEAD. Their templates and all other fields scan clean with `phrase_scan.py`, and also against the plan list without template removal.

The exact replacement texts are in `bb-contract-review.json`, which also holds the verification records. I will check the frozen bytes against it at pre-comparison time.

The drafts as committed also pass the freezer (on copies). None of the blocking issues is a tool failure; they are content defects.

## The questions asked

### 1. BB2 conditional on BB1's frozen targets: sound, and correctly worded?

**Sound in principle.** BB2 proves an implication: if the BB1 bounds hold with the frozen constants, then items 1–5 hold. It becomes unconditional once the BB1 gate admits constants at most those values. Every BB2 step is a triangle inequality, a geometric sum with nonnegative terms, a completeness argument or a trace-norm duality. So every BB2 constant is a nondecreasing function of the hypothesis constants, and an admitted BB1 constant at most the target gives the BB2 bound. This is a legitimate design, and it keeps BB1 and BB2 in one sub-round.

**Not correctly worded yet.** Seven points must be fixed; all are blocking.
1. **Targets equal the hypotheses** (`parameters.rate_constant_pair`).
   - BB2's `C'` target is 1/250000 and its `c_site` target is 1/500000. These are exactly BB1's hypothesis values.
   - From the hypotheses alone, the forward assembly fixed by P6 (nested telescoping) gives `C_h/(1-q) = 4/984375 ≈ 4.0635e-6 > 1/250000`, and `c_h/(1-q) = 2/984375`. The forward cannot meet its own target.
   - The union assembly gives exactly `C_h`, which is margin 1.
   - The advisor's margin of 2.24 was computed with BB1's preview constants. The conditional design forbids BB2 producers to use those.
   - **Replacement:** `C' ≤ 1/100000` and `c'_site ≤ 1/200000`. Both have margin `315/128 ≈ 2.4609` against the hypothesis-derived telescoped values.
   - **Secondary:** `C_2h/(1-q_2) = 625/12481056 ≈ 5.0076e-5` already exceeds 1/20000. Replace it with 1/8000 (margin 2.496).
   - Item 1's region symbol and item 5's constants are renamed accordingly (`c'_site`, the item-1 Cauchy constant, not BB1's `c_site`).
2. **The τ-scaling brackets cannot be met.**
   - Under the hypotheses, `C'` and `c'_site` are functions of fixed numbers at fixed `q`, so their τ → τ/100 ratio is **exactly 1**.
   - The drafted `[95,105]` would reject every valid BB2 packet.
   - A ratio near 100 would need BB1's formulas, and `conditional_on_bb1_targets` forbids those.
   - **Replacement:** "exactly 1 at the hypothesis values". The linear scaling is checked in BB1 and recorded at the BB2 gate with the discharge.
   - `C_dyn` keeps `[9500,10500]`, from the BA2 formulas. The secondary keeps `[99/100,101/100]`: its ratio is `(1-q_2(τ/100))/(1-q_2(τ)) ≈ 1.0015`.
3. **The discharge must cover scope, not only constants** (`conditional_on_bb1_targets`, `acceptance`).
   - The hypotheses are BB1's frozen *statements*: every comparison, the R form and the region form, each cutoff space and the untruncated vectors at fixed N, and both signs.
   - A BB1 gate that admits small constants for a narrower scope does not discharge the items that use the missing part.
   - Monotonicity must be checked exactly, not assumed.
   - The discharge must be hash-bound:
     - `record_gate.py` binds only skeptic files that start with `bb2`;
     - the BB1 gate is not a BB2 premise;
     - so the BB2 skeptic review must record the BB1 gate sha256, the item-by-item discharge, and the BB2 constants re-evaluated at the admitted BB1 values.
   - BB2 producers must read no BB1 producer, skeptic or gate file.
   - The acceptance text is rewritten item by item. A proved implication whose hypothesis is not discharged is retained as a labelled conditional statement, never lost and never promoted.
4. **The template must carry the hypothesis.**
   - BB2 producers prove only the implication, so they cannot quote the drafted unconditional sentence truthfully.
   - The replacement adds one clause: "under the BB1 locality bounds at their frozen targets as hypotheses (discharged only when the BB1 gate admits constants at most those targets)".
   - The sentence stays true after the discharge. It passes `phrase_scan.py` and the plan list without removal.
5. **Translation input** (`items.4_translations`, `required[3]`).
   - The draft names "BA1's general-volume comparison". That is a coefficient statement, and using it for densities is exactly the `coefficient_decay_not_marginal_decay` trap.
   - The input is BB1's general-volume comparison of the reduced densities, which is a hypothesis.
   - Its coefficient input is BA1's accepted comparison of any two complete-factor volumes of one prescription containing `Lambda_N`.
   - P6's condition is met: the BA1 gate's accepted statement lists that comparison, although the gate's decision text omits it (non-blocking; cite the accepted field).
6. **AQ2 gate** (`shared_premises`, `items.3_identification`).
   - Item 3 inherits AQ2's gap `alpha/16` and vacuum simplicity, but only the AQ2 forward report is a premise. Add `research/round29/advisor/aq2-gate.json`, which exists.
   - The wording "in its own GNS representation" overstates the gate. AQ2 admits `H_phys ≥ (alpha/16)(I-P_Omega)` with a simple vacuum on the invariant-local cyclic completion, and a full-GNS strengthening only as explicitly qualified there.
7. **Tier and route labels** (`tier_label_rule`, `tier_mixing_rejected`).
   - A state constant built on hypotheses has no BB1 route when the producer builds it, so the draft rule (one of four routes) cannot label it.
   - The replacement records the assembly (`nested_telescoping` or `union_comparison`, both in `plan.json` `assembly_values`) and the hypothesis source. The BB1 route is attached at the gate.
   - `tier_mixing_rejected` has no BB2 semantics (see BB1, issue 3 below).

**An alternative, not required.** BB2 could be frozen after the BB1 gate, with BB1's admitted constants as premises. That removes the conditional machinery at the cost of sequencing. With the seven fixes above, the concurrent design is sound, and I accept it.

### 2. Is the thin BA1 margin (1.14) a problem for BB1's targets?

**No, for the targets as frozen.**
- BB1's input is the admitted BA1 bound value `K = 49/111790368`, not BA1's target. BA1's margin measures that value against 1/2000000 and does not propagate.
- The proposal already uses `K` at both sites of R. That is conservative: the every-site form gives `qK` at site 0.
- I recomputed the split preview exactly: `C = 2(2K)(1+2t̄)(1+η_str) = 352765230433/201124673670833280 ≈ 1.75396e-6`. That is the proposal's rational, with margin **2.2805** against 1/250000.
  - `t̄ = 49/14398580736`;
  - `η_str = 32T_*/(1-32T_*) = 49/126095`, with `T_* = 49/4036608`.
- With the every-site input, 0 gets `qK`, which gives about 8.91e-7.
- Per site, `c_site ≈ 8.770e-7`, margin 2.2805 against 1/500000.
- τ → τ/100 ratio: 100.628, inside `[95,105]`.
- I did not re-derive the polymer Kotecký–Preiss preview. It is smaller than the split preview (about 1.7536e-6 per the proposal), so it does not set the margin.

**Where the thin margin would bite, and how the drafts handle it:**
- **Density-level union.** A comparison of the reduced densities *through the union* costs a factor 2: 3.5079e-6, margin **1.140**. The draft item says "compared through their union" and "labelled", yet BB2 item 4 needs it with the constant C. This is blocking (BB1, issue 4): compare directly, since BA1 admits any two such volumes directly, and make the item required.
- **Density-level telescoping plus a cross-family triangle.** This gives `C(1+1/(1-q)) ≈ 3.536e-6`, margin 1.131. The draft's "compared directly, not by telescoping" for centered boxes prevents it, so **keep that wording**. The face sets are totally ordered, so a direct comparison is always available.

### 3. Does the reverse BA1 theorem, as admitted, give the every-site input? (proposal risk 4)

**No.**
- The BA1 gate's decision reads "for u in R". The accepted statement concerns supports meeting R.
- The reverse Theorem 4.1 is stated "for `u` in `R`", and its Lemma 2.2 assumes that the support `M` meets R.
- The forward boundary-weighted norm `max_u sum_{I∋u} e^{βρ_B(I)}||δ_I|| ≤ K_own` *is* every-site, and it was reviewed in BA1. But its constants are labelled values, not the gate's bound value.

The reverse restatement is short:
- Replace R by `{u}` in Lemmas 2.2 and 3.1. Every source term of every comparison lies at ℓ∞ distance at least `N-|u|_∞` from `u`. The reasons: the new F1 stars and the new F2 faces all meet `{|p|_∞ ≥ N}`, and the faces inside `Lambda_{N-1}` are common to both prescriptions.
- The circle bound `2T(ρ)` is uniform in `u`, because the anchored norm is a maximum over `u`.
- This gives `sum_{I∋u}||δ_I|| ≤ K q^(N-|u|_∞)` with the same `K`. It matches the region exponent `d_Y`.

**But this is a new BB1 lemma, not an admitted BA1 statement.** The draft phrase "through a stated admitted form" names a premise that does not exist. This is blocking (BB1, issue 1). The replacement requires each producer to state one of the two forms and to prove the reverse form in full.

**The same kind of gap affects the secondary pair (non-blocking).**
- The proposal's `C_2 ≈ 1.95e-5` uses `2T(ρ)` at `ρ = |τ|/q_2 = 1/151552`, which is `49/10202112 ≈ 4.80e-6`. That is not a gate value.
- With the admitted floor constant `49/2018304`, `C_2 ≈ 9.71e-5` misses 1/20000.
- The input must be named as a labelled re-instantiation of Theorem 4.1, which is stated for every `ρ ≤ τ_*`.

### 4. Premise lists

- **P7 is met.** Neither BB1 nor BB2 lists anything under `experts/`: not the modern memo, not the BB proposal. Neither lists `skeptic/triage.md`, `recommendation.json`, `prospective-controls.json`, the loop-2 review, any deliberation, `plan.json` or `panel.json`.
  - The only Round33 skeptic premises are my BA1 and BA2 reviews (`ba1.md`, `ba2.md`). Their "advice" sections name only the routes the contracts already name, and they contain no BB preview.
  - Non-blocking: name the proposal and this review in the `reverse_premise_isolation` semantics, and name the concurrent BB1 or BB2 producer directories.
- **Missing (blocking):** the AQ2 gate in BB2.
- **AV1 F20–F23 are present** (AV1 forward §7, which is in both lists).
  - They were derived for F1 boxes. F2 boxes rely on the AY1 itemization, whose gate lists "cutoff-vector removal".
  - Non-blocking: say so in `parameters.cutoff`.
- **AQ2 for the gap:** the AQ2 forward report is in both lists, but the admitted statement is the gate's (above).
- **BB2 lists `contracts/bb1.json`.** Freeze BB1 first, so that BB2 snapshots the frozen bytes (non-blocking).
- **The marginal-locality lemma is undefined for producers (blocking, BB1 issue 2).** `marginal_locality_constants_explicit` refers to "eta, kappa_0 and w' of the marginal-locality lemma". That lemma exists only in my triage, which the reverse must not receive. The replacement states the lemma form in the semantics.

### 5. Freezer

The committed drafts freeze on copies (BB1: 33 premises; BB2: 35). The copies with every edit applied also freeze: BB1 first, then BB2 with 36 premises. Every applicable freezer rule passes (R1, R2, R4, R8, R10; R3 and R5 do not apply), and the preregistration control mirror equals `controls`. The advisor's commit 4c8acd3 already removed the bra-ket span that R1 would read as a placeholder.

### 6. Templates

- Both drafted templates are clean. So is the replacement BB2 template. Each was scanned with `phrase_scan.py` and also without template removal against the round list, the contract list and the plan's forbidden list.
- "rate" is always "rate in N".
- The contracts' `forbidden_phrasings` do not yet list the plan-forbidden entries "boundary independent", "uniform in a" and "confirms". Adding them (non-blocking) leaves every template and field clean.
- The BB1 selection note says "the rate q=1/64", which is a named value; "rate in N" would be tidier.

### 7. Gate fields

- Closed over `plan.json`: all 11 BB1 fields and all 15 BB2 fields are in `vocabulary.gate_fields`.
- `dynamics_level: correlation_functions_compact_window` is a listed value.
- `whole_sequence_scope` and `translation_invariance_scope` are non-empty, and each names the construction (and coarse translations).
- Sub-labels and tier names pass R10.
- BB2 needs a true-values rule (non-blocking), as the BA2 gate had. The fields are true only after the discharge, and a dropped item exports its field false.

### 8. Brackets

- **BB1:** `C` and `c_site` `[95,105]` (preview 100.63 to 101.28); secondary `[99/100,101/100]` (preview 1.000–1.003); `q_2` exactly 100. All correct.
- **BB2:** `C'` and `c'_site` must be "exactly 1 at the hypothesis values" (blocking, above). `C_dyn` `[9500,10500]` is correct: the BA2 ratios are 10019.6 to 10033.6. The secondary and `q_2` are correct. No single bracket applies to the item-5 sum (as drafted).

## Blocking issues

### BB1 (4 issues, 7 field edits)

1. **Every-site coefficient input** (`parameters.coefficient_input`, `required[3]`, `every_site_coefficient_input`). The BA1 gate is for `u` in `R` only. Either use the forward boundary-weighted bound (every u; labelled constants), or prove the reverse Theorem 4.1 restated for every `u` in full within BB1. Neither may be cited as an admitted BA1 statement.
2. **Marginal-locality lemma undefined** (`marginal_locality_constants_explicit`). The symbols come from the triage (P7). Replace with a self-contained lemma form, `2(1+η)` near plus `κ(I) ≤ κ_0 w'^{-d} p(|I|)` far, with exact constants per route.
3. **`tier_mixing_rejected` has no BB1 meaning** (`tier_label_rule`, the new semantics).
   - The frozen definitions are BA1's (routes `weighted_norm`/`analytic_disc`) and BA2's (Lieb–Robinson tiers only). Either would reject every BB1 constant.
   - The replacement adds the BA1 input as a separate field.
4. **The one-prescription union comparison** (`comparisons[4]`). As drafted it is labelled and compared through the union, which costs a factor 2 (margin 1.14). It is BB2 item 4's input. Make it a direct, required comparison, with the union form labelled only.

### BB2 (7 issues, 15 field edits)

1. Targets equal the hypotheses (`rate_constant_pair`, `preregistration.target`, `items.1`, `items.5`, `required[4]`). The replacements are `C' ≤ 1/100000`, `c'_site ≤ 1/200000` and secondary `C'_2 ≤ 1/8000`.
2. Scaling brackets (`scaling_brackets_per_constant`): exactly 1 at the hypothesis values.
3. Conditional semantics and acceptance (`conditional_on_bb1_targets`, `acceptance`): scope, monotonicity, a hash-bound discharge, isolation from BB1 production, and retained conditional statements.
4. Translation input (`items.4_translations`, `required[3]`): BB1's density comparison, not BA1's coefficient comparison.
5. The template carries the hypothesis clause.
6. The AQ2 gate is added to `shared_premises`, and the `items.3` inheritance is worded as admitted.
7. `tier_label_rule` and `tier_mixing_rejected` for hypothesis-built state constants and BA2 dynamics constants.

## Non-blocking findings (replacement texts in the JSON where a field applies)

**BB1:**
- The secondary pair's BA1 input is not a gate value (above).
- `global_lipschitz_not_decay` inherits BA1's `2J_0G'(R)` wording, which both BA1 producers corrected. The corrected text also names the density-level Lipschitz constants.
- The straddling-supports fixture has no control. It is folded into `normalization_couples_supports`.
- The region form should state `Y ⊂ Lambda_N` and what `|Y|` counts.
- `rate_constant_pair_prefrozen` inherits "weights frozen in the contract" and a labelled family down to `q_min`. BB1 freezes only ranges, and `q_min` is unreachable for densities. The replacement says producers declare exact proof weights before their constants.
- `reverse_premise_isolation` should name the proposal, this review and the BB2 producer files.
- `parameters.cutoff`: F2 relies on the AY1 itemization.
- The acceptance text should mirror the template's cutoff regimes and say what one route alone gives.
- Add the three plan-forbidden phrases.
- Add `analytic_disc` and `weighted_norm` to `tier_names_allowed` for the input field (R10 passes).

**BB2:**
- `reverse_premise_isolation` (as for BB1, plus the BB1 files).
- A `gate_fields_rule` for limited outcomes.
- The three plan-forbidden phrases.
- Freeze order (BB1 first).
- A frame, or a second template, for limited outcomes, since the template asserts every item.

**Both:**
- The BA1 gate's decision text omits the one-prescription volumes, while its accepted statement lists them. Cite the accepted field.
- P5: record plan.json's sha256 in `history` at this freeze.

**P7 relaxation (my own).** In loop 2, P7 asked that η, κ_0 and w' be frozen with margin 2. The two routes define different intermediate constants (η_str against η_far). The decisive pairs `(q, C)` and `(q, c_site)` are frozen with margins 2.28 and 2.28 at the worst admitted input. So I accept exact, declared intermediate constants, under the self-contained semantics of BB1 issue 2, in place of frozen ones.

## Numbers at a glance (previews; exact rationals in the scratch script)

| quantity | value | against |
|---|---|---|
| BB1 `C` (split, reverse BA1 input at both sites of R) | `352765230433/201124673670833280 ≈ 1.75396e-6` | 1/250000: margin 2.2805 (matches the proposal exactly) |
| same, every-site input (`qK` at 0) | ≈ 8.907e-7 | margin 4.49 |
| BB1 `c_site` (per site of R) | ≈ 8.770e-7 | 1/500000: margin 2.2805 |
| density comparison through the union (factor 2) | ≈ 3.5079e-6 | margin **1.140** (hence BB1 issue 4) |
| density telescoping plus a cross-family triangle | ≈ 3.5358e-6 | margin 1.131 (the "directly" wording prevents it) |
| BB1 `C` τ-ratio | 100.628 | `[95,105]` |
| secondary input `2T(1/151552)` | `49/10202112 ≈ 4.80e-6` | not a gate value; with the gate floor constant `C_2 ≈ 9.71e-5` misses 1/20000 |
| BB2 `C'` from the hypotheses, telescoped | `4/984375 ≈ 4.0635e-6` | draft target 1/250000 **missed**; replacement 1/100000: margin 315/128 = 2.4609 |
| BB2 `c'_site` from the hypotheses, telescoped | `2/984375 ≈ 2.0317e-6` | replacement 1/200000: margin 2.4609 |
| BB2 `C'_2` from the hypotheses | `625/12481056 ≈ 5.0076e-5` | draft 1/20000 missed; 1/8000: margin 2.496 |
| `C_dyn = K_c1 + K_c2 + (11/8)K_cmp` (BA2 gate values, larger per constant) | `175777236988465912821/759247655761718750000000000000 ≈ 2.3152e-10` | 1/2000000000: margin 2.1597 (matches the proposal exactly); F1 alone `2K_c1 ≈ 2.039e-10` |
| `(5r+1)/r^3 ≤ (11/8)/(r-1)` | holds for r ≥ 2, equality at r = 2 | the item-5 derivation |
| item-5 terms at the replacement targets | N=5: dynamics 2.3e-10, state 2.4e-9; N=7: 1.2e-10, 1.0e-10; N=9: 7.7e-11, 3.4e-12 | no single target (as drafted) |
| ℓ∞ shells around R | `24d²+8d+2` sites at distance d | the proposal's `S(x)` |

No result here is a Round33 finding, a loop or a fraction of the continuum problem. The four-dimensional Yang–Mills existence and mass-gap problem remains open.
