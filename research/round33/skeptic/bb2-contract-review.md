# BB2 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/bb2.json` (sha256 `ed5c0b24…ad35`, frozen 2026-09-24T23:36:46.617Z) and the frozen `contracts/bb1.json` (sha256 `30400d2e…5018`, frozen 23:36:46.587Z, which supplies the hypotheses). I wrote it before reading any BB1 or BB2 producer. I am a model-agent skeptic with correlated ancestry, not human review. Human author: Hruday N M (BUNZEEY).

My own record seeded this loop:
- my triage proposed whole-sequence convergence by a Cauchy estimate and the pre-registered translation item;
- my loop-2 review fixed P6 (forward telescoping, reverse unions);
- my BB pre-freeze review (`bb-contract-review.md`/`.json`) wrote all 15 blocking BB2 field edits, including the targets, the brackets, the conditional semantics and the acceptance text.

This review therefore checks the frozen contract against the premises and against my own edits. It is not an independent assessment of the design.

**What I did and did not open.**
- I did not open, list or read `research/round33/{forward,reverse}/{bb1,bb2}/`.
- The one exception: I ran `find` on the two BB2 `inputs/` folders (file names only) and hashed each snapshot against the repository.
  - Both producers hold the same 38 files: `AGENTS.md`, the contract and the 36 shared premises.
  - Every snapshot is byte-identical to the repository.
  - Both hold the frozen BB1 bytes (`30400d2e…`).
  - The reverse inventory contains no triage, recommendation, prospective-controls, loop-2 review, BB contract review, deliberation, plan, panel, lens file, modern BB-targets proposal, forward file or BB1 producer, skeptic or gate file. The only skeptic files are `ba1.md` and `ba2.md`.
- I read nothing in any other agent's folder.
- Git commands:
  - one early unrestricted `git status --short` printed nothing (the tree was clean then);
  - the other `git` commands were path-restricted to `advisor/` and `contracts/`, or printed commit messages only.
- Private scratch: `/tmp/claude-0/skeptic-bb2-private/` (value scripts, input hash list, replay directories, mutated copies of the checker). It is not evidence and not a premise.

**Verdict: executable as written, with the readings below.** Nothing blocks production.

`bb2_check.py` confirms the frozen facts:

| Item | Value |
|---|---|
| Checks | 81, of which 38 are controls: the 34 contract ids plus 4 extras, with 142 damaging mutations |
| Control mirror | `controls` = `preregistration.controls_required.ids`, 34 = 34, no duplicates |
| Semantics | 15 in this contract, 19 inherited from earlier frozen contracts (BA2, BB1); none undefined |
| Premises | all 36 exist, including `contracts/bb1.json` and the AQ2 gate |
| Gates pinned | BA1, BA2, AQ1, AQ2, AM2, AV1, AY1, AY2 |
| Replays | byte-identical under `python3 -B` and `-B -O`, and under two hash seeds |
| Source edits | 18 edits to a private copy of the validator, discharge engine or fixtures each make the run fail |

## Pre-freeze edits against the frozen bytes

All pre-freeze edits are in the frozen bytes verbatim. `bb2_check.py` compares every replacement text in `bb-contract-review.json` with the frozen field:
- BB2: 15 of 15 blocking field edits and 3 of 3 non-blocking field edits (`reverse_premise_isolation`, `gate_fields_rule`, `forbidden_phrasings`);
- BB1: 7 of 7 blocking and 10 of 10 non-blocking field edits.

The draft-to-frozen diff of `bb2.json` contains nothing else, apart from `status` and `frozen_at`.

My two recommendations that had no field:
- **Freeze order: applied.** BB1 froze 30 ms before BB2.
- **A frame for limited outcomes: not applied.** Reading R8 covers it.

## Target well-posedness and margins

Every target is a "proved constant at most the target" comparison. Every constant is independent of N.
- The state constants are functions of the hypothesis values only, so they do not depend on τ.
- C_dyn is evaluated at |θ| ≤ 8 (U = 1) and |τ| = 10⁻⁸, at both signs.

| Target | Assembly or route | Constant | Margin |
|---|---|---|---|
| C′ ≤ 1/100000 | nested telescoping, C_h/(1−q) | 4/984375 ≈ 4.0635e-6 | 315/128 = 2.4609 |
| | direct union comparison, C_h | 1/250000 | 5/2 |
| c′_site ≤ 1/200000 | telescoping, c_h/(1−q) | 2/984375 ≈ 2.0317e-6 | 315/128 |
| | union, c_h | 1/500000 | 5/2 |
| C_dyn ≤ 1/2000000000 | inner F2 (reverse BA2 values), 2K_c2′ + (11/8)K′_cmp | 8.9700e-11 | 5.574 |
| | same-family intermediate (2K_c1 forward; F2 2K_c2′) | 1.1894e-10 | 4.204 |
| | inner F1 (forward BA2 values), 2K_c1 + (11/8)K_cmp | 38367/249153280000000 ≈ 1.5399e-10 | 3.247 |
| | advisor form, K_c1′ + K_c2 + (11/8)K_cmp | 2.3152e-10 | 2.160 |
| | inner F1 with the whole-star K_c1′ (worst natural assembly) | 2.3895e-10 | 2.092 |
| C′₂ ≤ 1/8000 (secondary) | telescoping, C_2h/(1−q₂) | 625/12481056 ≈ 5.0076e-5 | 390033/156250 = 2.4962 |
| | union | 1/20000 | 5/2 |

- The telescoped and union constants depend on (C_h, c_h) only through linear maps with positive coefficients (64/63 or 1). The monotonicity that the contract requires is therefore exact.
- Every natural assembly of admitted BA2 statements meets the C_dyn target with a margin of at least 2.09 (derivation §8).
- The six BA2 gate constants are parsed from the pinned gate and reproduced exactly from their formulas.
- τ → τ/100:
  - C′ and c′_site: exactly 1.
  - C_dyn: 10019.588 (inner F2) to 10033.644 (inner F1), inside [9500, 10500].
  - Secondary: 1085053/1083425 ≈ 1.0015 (telescoped) or exactly 1 (union), inside [99/100, 101/100].
  - q₂: exactly 100.

## The discharge protocol I will apply at the BB2 post-review

**What is discharged.** Each BB2 packet proves an implication: H(C_h, c_h) ⇒ items 1–5 with constants C′, c′_site and C_dyn. Here H is the family of BB1 inequalities, indexed by:
- comparison: c1 F1 N vs N+1; c2 F2 N vs N+1; c3 F1 vs F2 at the same N; c4 any two centered boxes; c5 two one-prescription volumes containing Λ_N;
- form: R (C_h q^(N−1)) or region (c_h|Y|e^{|Y|/10⁸}q^{d_Y});
- cutoff regime: each Q_L, or untruncated at fixed N;
- sign.

**Why the discharge is valid when BB1 admits constants at or below the targets.**
1. **Pointwise dominance.** Suppose the BB1 gate admits, for an instance, a bound B_adm(N,Y) with:
   - the same q = 1/64;
   - an exponent at least that of the hypothesis (a sharper q^N is allowed);
   - a power of |Y| at most 1 and an e-rate at most 10⁻⁸;
   - a constant at most C_h (R form) or c_h (region form).

   Then B_adm ≤ B_hyp for every N ≥ 2 and every Y ⊂ Λ_N. The admitted statement implies that hypothesis instance, and the BB2 implication fires.
2. **Monotone re-evaluation.** Every BB2 constant is a nondecreasing function of the hypothesis constants:
   - C′ = C_h/(1−q) or C_h;
   - c′_site = c_h/(1−q) or c_h;
   - the item-4 bound is C_h q^(N−|v|−1);
   - the item-5 sum has positive coefficients in C_dyn, c′_site and C′.

   The proofs use the hypothesis constants only through upward-closed inequalities: triangle inequalities, geometric sums and limits. The proof schema is therefore valid at the admitted values, and C′(C_adm) ≤ C′(C_h) ≤ target. The gate records both.
3. **Nothing else discharges.** Suppose an admitted constant exceeds the hypothesis value for any instance an item uses. That item stays conditional, even if the re-evaluated schema would still meet the BB2 target. The re-evaluated value is then recorded as labelled only, because the contract makes a conclusion unconditional "only when … at most the hypothesis values".

**What each item uses.** An item is unconditional when, at both signs, at least one BB2 route proves it from instances that the BB1 gate discharges.

| Item | BB1 instances used |
|---|---|
| 1, R part (C′) | forward: c1 (F1), c2 (F2), R form; reverse: c4, R form (same family, M > N) |
| 1, region part (c′_site) | the same comparisons in region form (d_Y as in BB1) |
| 2 (common limit) | item 1 for both families, plus c3 in R form (on R) and region form (every finite region) |
| 3 (identification, inheritance) | full states: item 1 in region form (F1 for AQ1 limits, F2 for F2 limits), plus item 2 in region form (inheritance across families, including AQ2 for F2 limits) |
| 4 (translations) | quantitative R bound: c5 in R form, direct, via Λ_{N−\|v\|}; invariance of the limit state on every finite region: c5 in region form plus item 1 in region form |
| 5 (correlations) | items 1–2 in region form on Λ_{r_N}; item 1 in R form (mean term); BA2 gate constants (already admitted, no discharge) |
| secondary pair | the BB1 secondary pair; labelled in every outcome (its BA1 input is a labelled re-instantiation) |

**Regime and sign.**
- The untruncated regime at fixed N is needed.
- A Q_L-only admission discharges only through a route that removes the cutoff itself at fixed N: AV1 F20–F23 for F1, and the AY1 itemization for F2. The forward assembly names this step.
- Signs are discharged separately. A +τ/−τ pair is never a comparison.

**Outcome map.** The discharge engine in `bb2_check.py` runs each row on a labelled synthetic BB1 outcome. None of these is a BB1 result.

| BB1 gate outcome | BB2 items | BB2 verdict | Gate fields |
|---|---|---|---|
| accepted_within_scope, every used instance at most the hypothesis | 1–5 full | accepted_within_scope | all true, as frozen |
| limited: region form missing (or dominated only in R form, e.g. an \|Y\|² factor or another q) | 1 R only; 2 on R; 3 R-marginals only (every AQ1 and F2 limit has R-marginal ρ^∞_R; nothing inherited, since stationarity, GNS continuity and the gap are properties of full states); 4 R bound and R-translate covariance only; 5 dropped | limited | only rate_in_N_claimed true; the frozen scope "every finite region" cannot be exported |
| limited: c5 missing | 4 dropped; 1, 2, 3 and 5 full | limited | translation_invariance_claimed false |
| c3 missing, or above the hypothesis | 2 conditional; 3 per family (each family's limit equals its own subsequential limits; AQ2 not transferred to F2 limits); 5 per family only (the frozen item 5 needs the common limit) | limited | common_limit_claimed false; dynamics_level not set |
| c4 missing (c1, c2 present) | 1–5 full through the forward route; the reverse route's item 1 is retained as conditional | accepted_within_scope, with the reduced pairing recorded as a limitation | as frozen |
| Q_L only | discharged through the forward route (own cutoff removal); the reverse is conditional | accepted_within_scope only if a packet proves the passage at fixed N | as frozen, or all false |
| one sign only | full at that sign; conditional at the other | limited | both-sign fields false |
| only one BB1 route admitted | unaffected (the bound value of the admitted route is used) | as in the first row | as frozen |
| near-support part only | no bound on reduced densities; nothing discharged | insufficient | all false |
| BB1 insufficient | every implication retained as conditional_on_bb1_targets | insufficient | all false |

**Post-review record.** At the post-review, my record (`bb2*` files, bound by `record_gate.py`) will contain:
- the BB1 gate sha256 and its verdict;
- for every item and route: the instances used, their admitted constants and bound shapes, the dominance result and the BB1 route of the bound value (`polymer_kp` or `iterated_split`);
- the BB2 constants re-evaluated at the admitted values, for example C′ = C_adm/(1−q), and at both signs;
- the gate fields under `gate_fields_rule`;
- the retained conditional statements.

Two illustrations, both labelled and neither a BB1 result:
- With the advisor-recorded split preview C = 352765230433/201124673670833280 (1.75396e-6) and C/2 per site, the re-evaluation gives C′ = 1.78180e-6 (telescoped) or 1.75396e-6 (union), and c′_site = 8.9090e-7 or 8.7698e-7.
- BB1's own τ/100 ratio (bracket [95,105]) is recorded at this step. BB2's brackets stay "exactly 1".

## Numbered readings

1. **R1, union comparison.**
   - `union_comparison` means one direct application of a BB1 general-volume hypothesis: c4 for item 1, c5 for item 4.
   - A literal two-step comparison through U = Λ_N ∪ (Λ_N+v) costs C_h q^(N−|v|−1)(1+q^{|v|}), a factor of 65/64 at |v| = 1. That exceeds the frozen item-4 constant, so it is labelled only (D2).
2. **R2, C_dyn.**
   - Any assembly of admitted BA2 statements is valid if each step cites one:
     - comparison (5N+1)N⁻³;
     - Cauchy over all M > N;
     - limit (N−1)⁻¹, including gate item (4) for F2.
   - A C_dyn whose components share a route carries that route. A composite of both routes must list each component with its route and be labelled `composite` (D3).
   - Values range from 8.970e-11 to 2.389e-10. Every value is at least the floor 2K_c2′ = 6.9286e-11.
3. **R3, item-level discharge.** An item is discharged through at least one route. A route whose instances are undischarged is retained as conditional and recorded as a pairing limitation.
4. **R4, item 4 without the region form.** Item 4 keeps its quantitative R bound and the covariance on translates of R: the marginals on R+v converge to the translate of ρ^∞_R. Invariance of a state is not established, and `translation_invariance_claimed` stays false (D1).
5. **R5, "own GNS representation".** Required item 3's "in its own GNS representation" is read through `items.3`:
   - the gap α/16 and vacuum simplicity hold on the invariant-local cyclic completion;
   - the full-GNS strengthening holds only as qualified in the AQ2 gate, because it uses AM2's full-Hilbert finite gap (D4).
6. **R6, d_Y and c4.**
   - d_Y = N − max_{y∈Y}|y|_∞ as in BB1 `region_form` (D7).
   - c4 "of F1 or F2" includes cross-family pairs of different sizes. A telescoping that interleaves F1_N ⊂ F2_N ⊂ F1_{N+1} is valid but costs two comparisons per step (2C_h/(1−q) ≈ 8.13e-6), and it is labelled.
7. **R7, inherited semantics.** Inherited control texts are read by name. For example, `rate_constant_pair_prefrozen` names BB1 proof weights, and BB2 has none: its "weights" are the hypotheses (D6).
8. **R8, template under a limited verdict.** The template asserts every item. At a limited verdict the gate quotes it inside the frame "the preregistered sentence … is established except for item k" (D9).
9. **R9, BA2 gate item (4).** It reads ‖T^{F2,N}−T‖ ≤ min(K_F1, second-route K_F2)/(N−1).
   - The K_F1 there is the forward Duhamel pair with inner F1(Λ_M) and source F1(M) minus F2(N) (BA2 forward report).
   - The min equals K_c2′ = 3.4643e-11.
   - K_F1 alone may not be used for the F2 sequence without that pair.
10. **R10, general volumes.**
    - The hypothesis "at fixed N for the untruncated ground vectors" needs, for c5, the AM2 §6 facts in each volume.
    - Item 4 uses only translated cubes, and there those facts follow from coarse covariance.
11. **R11, signs.** +τ and −τ are separate models. The AY2 gate separates their limits by at least 8.757e-10 on R. A cross-coupling pair used as a comparison contradicts the hypothesis bound from N = 4.
12. **R12, extra inheritances.** Identity of states transfers every admitted statement about the AQ1 state, each with its gate scope: local normality, gauge invariance, AV1's D, AY1/AY2 bounds, and AQ2's Wilson variance of at least 61999/250000. The frozen list is the required minimum, and "exactly" is read as "with exactly the admitted scope" (D11).
13. **R13, limit order.** The cutoff is removed at fixed N, then N → ∞. Under the uniform-in-L bounds the exchange would be valid (Moore–Osgood), but it is neither used nor claimed.

## Residual defects (none blocks production)

- **D1.** `acceptance.limited` does not say what happens to item 4 when the region form is missing (R4).
- **D2.** A literal union route cannot meet the frozen item-4 constant C_h q^(N−|v|−1) (R1).
- **D3.** "Exactly one route" per dynamics constant is ill-posed for a composite C_dyn. Pure-route assemblies exist for both routes (R2).
- **D4.** Required item 3 ("in its own GNS representation") is broader than `items.3` (R5).
- **D5.** The secondary pair has no target for c′_site,2. It is labelled only: 625/24962112 ≈ 2.5038e-5 (telescoped) or 1/40000 (union).
- **D6.** Several inherited control texts are written for BA2 or BB1 (R7).
- **D7.** d_Y is defined only in BB1 (R6).
- **D8.** P5: `plan.json` history has no BB-freeze entry with `plan_sha256_at_freeze`. The BA freeze has one.
- **D9.** There is no frame and no second template for limited outcomes (R8). My non-blocking recommendation was not applied.
- **D10.** Item 5 fixes neither the intermediate evolution nor the assembly of C_dyn. Every natural assembly meets the target (R2).
- **D11.** "Inherits exactly the admitted properties" lists a subset of what identity transfers (R12).

## Control mirror

- All 34 contract ids are executed as damaging mutations in `bb2_check.py`. Each mutation must be rejected with its stated reason. Positives are accepted:
  - a limited packet with a dominating term;
  - a labelled mixed-route composite;
  - a labelled union two-step;
  - a negated forbidden phrase;
  - inequality text such as `N>=2`.
- Four extra controls:
  - `discharge_protocol_executable`: 11 mis-discharge mutations and 12 correct synthetic records;
  - `union_two_step_labelled`;
  - `mandatory_sentence_once`;
  - `error_terms_itemized`.
- `reverse_premise_isolation` runs on the contract-derived inventory. The actual inventories are recorded by name and hash as above. Report contents, and the discharge itself (which needs the BB1 gate), are checked at post-comparison.

No result here is a Round33 finding, a loop, or a fraction of the continuum problem. The four-dimensional Yang–Mills existence and mass-gap problem remains open.
