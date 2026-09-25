# BA1 skeptical review (post-comparison)

**Verdict: `accepted_within_scope`, sub-label `boundary_decay_rate_only`, secondary `static_not_dynamic`.** There are no blocking issues.

Both routes prove the frozen coefficient-difference bound for every comparison of the contract, at both signs, at both frozen pairs, and in the `exact_first_order` tier. The setting is the zero-selected patterned family at `|tau|<=10^-8`, with the two named construction families:
- F1, the AQ1 centered whole-star boxes;
- F2, the I1 §6 all-contained-face boxes with padding, on the same `Lambda_N=[-N,N]^3`.

- **Forward route (`weighted_norm`):** a diameter-weighted anchored norm with loss `w^{d_X}=w` charged once per interaction term, plus a boundary-distance weight `e^{beta rho_B}`.
- **Reverse route (`analytic_disc`):** analyticity of the fixed point on the complex disc `|z|<=rho`, the order-versus-distance count as a Taylor-coefficient lemma, and a Schwarz estimate.

The acceptance rule (contract `acceptance.accepted_within_scope`) asks that each proved constant be at most its frozen target. It says the margin of at least 2 is a freeze-time property of the target against the loop-1 previews, not an acceptance condition.

**What the gate should bind.** For each frozen pair, bind the larger valid constant, which both routes certify. The other route's value is labelled. This follows the Round32 AX1 precedent.

| pair | bound K (exact) | preview | route, tier | margin | also certified (labelled) |
|---|---|---|---|---|---|
| headline `q=1/64`, target `1/2000000` | **`49/111790368`** | **4.383204e-7** | analytic_disc on the disc of radius `64|tau|`, exact_first_order | **1.1407** | weighted_norm `2734375/12204185915601` ≈ 2.240522e-7 (any two centered boxes, telescoped; margin 2.2316) |
| floor `q=148/390625=37888|tau|`, target `1/12` | **`49/2018304`** | **2.427781e-5** | analytic_disc on the disc of radius `tau_*=1/37888`, exact_first_order | 3432.49 | weighted_norm `708203125/43148545682688` ≈ 1.641314e-5 (margin 5077.2) |

Every bound comparison has exponent `N-1`: the contract form `ceil(d/diam)` with coarse l∞ star diameter `d_X=1`. The rate is per coarse step in N at fixed spacing, uniform in the on-site cutoff L, and never uniform in a.

The review program is `ba1_postreview_check.py`, whose output is `ba1-postreview/results.json` (sha256 `85989015…6ba48146`). Normal and `-O` runs are byte-identical. It runs:
- **20 exact checks.**
- **81 source-edit runs on temporary copies:**
  - 2 unmutated copies, each reproducing its frozen output byte for byte;
  - 74 validator weakenings, one per contract control per producer, each aborting with that control's own `damaging mutation accepted: <label>`;
  - 5 input edits, each aborting without output.
- **10 damaged packets**, each rejected by the review's own value validator for the expected reason.

Both producers replay byte for byte under normal and `-O` Python (`ba1-replays.json`).

## What is proved, with quantifiers

**Model.** AQ_patterned_zero_selected:
- SU(2) Kogut–Susskind form on Z^3 at fixed spacing, with coarse 24-link factors;
- selected triple exactly (0,0,0), with Haar product reference;
- 21 omitted faces per anchor, entering as `-(tau/3)W_f` in normalized units `delta=alpha/8`;
- both signs, `|tau|<=10^-8`;
- the AM2 creation expansion with `J<=28|tau|`, `R=1/64`, `G(t)=16e^{8t}(1+10t)`, `G(R)<148/7`, `G'(R)<352` and `t_1=49|tau|/144`;
- cover `R={0,e_z}` and the coarse l∞ metric.

**Statement.** For the families F1 and F2 on centered cubes, `N>=2`, the AM2 creation coefficients meet the following bound. It holds in each on-site cutoff space `Q_L`, with constants independent of L, on supports meeting R. For any two boxes of the named constructions, with N the smaller box size, the coefficients differ in the anchored norm by at most `K q^(N-1)`.

The comparisons are those in `parameters.comparisons`:
- F1 on `Lambda_N` versus `Lambda_(N+1)`;
- F2 on `Lambda_N` versus `Lambda_(N+1)`;
- F1 versus F2 on the same `Lambda_N`;
- any two centered boxes of size at least N, of either family;
- any two complete-factor volumes of one prescription that both contain `Lambda_N`.

**Consequence.** For each family, the whole sequence of coefficients on supports meeting R is Cauchy in each `Q_L`. This is `coefficient_cauchy_claimed=true` with the frozen scope.

**Scope.** This is decay of the coefficients of the named constructions at a rate in N. It is not decay of the reduced density or of any state. It says nothing about untruncated creation coefficients or about a common limit of states. It is not uniqueness of any ground state and not a statement uniform in the lattice spacing a.

The 12 frozen gate fields hold exactly as prefrozen. `rate_in_N_claimed` and `coefficient_cauchy_claimed` are true. Every other Boolean is false.

## Predictions against producers

My pre-comparison package (`09ae71e`, committed at 22:36:35Z, before either producer commit) predicted the following:

| quantity | skeptic (pre) | forward | reverse | status |
|---|---|---|---|---|
| `w_max`, `q_min`, `tau_*` | 390625/148, 148/390625, 1/37888 | = | = | identical |
| `T_w(64)=T(64|tau|)` | 49/223580736 | = | = | identical |
| `T_w(w_max)=T(tau_*)` | 49/4036608 | = | = | identical |
| `Gamma` at w=64 / w_max | 2464/390625 / 77/296 (G'(R) form) | = | (disc: `28 rho G'(R)`, same numbers) | identical |
| reverse headline K (Schwarz, contract form) | 49/111790368 | — | = | **identical** |
| reverse floor K | 49/2018304 | — | = | **identical** |
| reverse crude headline / floor | 296/390625 / 1/32 | — | = | identical; the headline fails and is retained |
| reverse coefficientwise (Cauchy) | 14/31441041 | — | = (labelled) | identical |
| reverse sharp count, headline | 49/7154583552 | — | = (labelled) | identical |
| reverse general volumes | direct K; union 49/55895184 misses | — | direct K; telescoped 889/1006113312 misses (recorded) | agrees (see below) |
| forward headline K | 2.20045e-7 (contract form, G'(T_w), direct comparison) | 2734375/12204185915601 ≈ 2.24052e-7 (telescoped) | — | **differs; reconciled, both valid** |
| forward F1-vs-F2 K | listed exact variant 19140625/86785322066496 ≈ 2.20551e-7 | = | — | identical to the listed variant |
| forward floor K | 1.4693e-5 | 708203125/43148545682688 ≈ 1.64131e-5 | — | differs; reconciled, both valid |
| forward crude headline | ≈ 2.90e-4 (2.897e-4 with an iterated t_w) | 9472/24454143 ≈ 3.8734e-4 | — | differs (majorant choice); both fail and are retained |
| τ ratio, headline | 101.030 (forward contract form), 100.628 (reverse) | 4708908680004/46502766025 ≈ 101.2608 | 4340004/43129 ≈ 100.6284 | reverse identical; forward is the G'(R) variant from my loop-2 list |
| τ ratio, floor / q_min | 1 / 100 | 3255196/3253975 ≈ 1.000375 / 100 | 1 / 100 | within the frozen bracket `[99/100,101/100]` |
| distances (e_z, 0) | nested new supports N−1, N; shell N, N+1; outer layer N−1, N | = | = | identical |
| F1-vs-F2 extra faces | `28N(5N+1)` = 616/1344/2352, classes 17/13/5/10/3/1/0 | = | = | identical |

**Reconciling the forward headline (2.2405e-7 against my 2.2004e-7).** Two choices account for the whole difference, and both are valid upper bounds:
1. **Derivative evaluated at R.** The forward evaluates the derivative at R in the contraction factor and in the first-order remainder: `Gamma = J w G'(R)` with `G'(R)<=352`, and `S = w t_1 + Gamma T_w`. I evaluated `G'` at `T_w` and used `G(T_w)-16` in the source. Since `G'` is increasing and `T_w < R`, the forward's majorant is the larger one. This moves `2.20045e-7` to the exact variant `19140625/86785322066496 ≈ 2.20551e-7`, which I listed in my derivation §10. The review re-derives it from the forward's declared formula: check `forward_values_reproduced_exactly`.
2. **Telescoped general comparison.** The forward binds the general comparison by telescoping, `K_gen = K_12 + K_nest/(1-q)`. With `K_nest = K_12/w`, this is `K_12 * w/(w-1) = (64/63) K_12`, giving `2734375/12204185915601`. My R6 reading was that the constructions are totally ordered as face sets, `F1_N ⊂ F2_N ⊂ F1_(N+1)`, so any pair is one nested comparison and the factor 64/63 is unnecessary. Telescoping is still valid.

The headline margin moves from 2.2723 (mine) to 2.2316 (forward). The forward floor (`1.64131e-5` against my `1.4693e-5`) differs for the same two reasons. At `w_max`, the telescoping factor is `w_max/(w_max-1) ≈ 1.00038`, which is why the forward floor τ-ratio is `3255196/3253975` instead of exactly 1.

**Reverse headline and floor.** They equal my predictions exactly: `K=2T(rho)`, `T(rho)=(49 rho/144)/(1-9856 rho)`, at `rho=64|tau|` and at `rho=tau_*`.

## Items adjudicated

1. **Diameter convention and the sharper lemma.**
   - **Metric and lemma form.** Both producers use the coarse l∞ metric with `d_X=1`, verified by enumeration. Both use the contract form `ceil(d/diam)` for every bound constant.
   - **Sharp count.** Both prove the sharp count `1+ceil(d/diam)`: forward F08 with W4, and the reverse's Taylor-coefficient lemma.
     - The reverse records sharp-count constants as labelled refinements: `49/7154583552` at the headline and `1813/197100000000` at the floor.
     - The forward's nested constant `K_nest = K_12/w` is labelled. It is taken at shell distance N with the loss charged. Its floor variant (`floor_K_nested_contract_form`) is linear in τ, with ratio exactly 100.
   - **Floor bracket.** A floor constant that improves on the contract-form exponent, written against `q^(N-1)`, is linear in τ, with exact ratio 100. It therefore lies outside the frozen floor bracket (my R3). Both producers keep such constants labelled, and neither tests them against the bracket as a failure.
   - **l1 alternative.** The l1 alternative is tabulated by the forward (l1 gives the same distances). It is moot for the verdict.
2. **Source-set readings.**
   - **Nested comparisons (my R1).** The literal set of sites met by the new terms adds the outer layer of `Lambda_N`, at distance `N-1` from `e_z`. The parenthetical shell lies at N. The two readings give the same bound once the source loss is charged:
     - The forward takes the shell and charges `w` in the source, `S = w t_1 + …`.
     - The reverse takes the distance `N-1` to the new terms directly.
   - **Wording in the reverse (non-blocking N4).** The reverse report says the sites met by the F1 nested source are the shell together with the *positive* outer layer. Stars anchored at `b_i=-N-1` also contain sites with coordinate `-N`. So the literal set is the full outer layer: 98, 218 and 386 sites at N=2,3,4, confirmed in my pre-comparison checks `source_set_literal_reading_N2/N3`. The distance to `e_z` is `N-1` either way, so no value changes.
   - **F1 versus F2.** The source is the faces with `max_i b_i = N`. The `28N(5N+1)` new F1 faces lying inside `Lambda_N` are exactly the extra F2 faces `F2(Lambda_N)\F1(Lambda_N)`; the reverse `check.py` proves this, and the forward's class table agrees. The contract's set `max_i |b_i| = N` is a harmless superset (reverse wording defect 2).
3. **General comparisons.**
   - **Reverse.** The reverse compares any two volumes directly, as my R5 reading asked, and gets `K`. It records that telescoping at exponent `N-1` would give `889/1006113312 ≈ 8.836e-7`, above `1/2000000` (with the sharp exponent, `889/64391251968` meets the target). A two-step union would give `49/55895184 ≈ 8.766e-7`, also above.
   - **Forward.** The forward's telescoped constant meets the target with margin 2.23. Its labelled one-prescription union constant `2K_nest = 19140625/2777130306127872` is valid.
   - **Forward wording (non-blocking N3).** The forward says the union's new terms "lie outside `Lambda_N`, at l-infinity distance at least N from `e_z`". Each new term meets the complement of `Lambda_N`, but a star or face straddling the boundary can contain outer-layer sites at distance `N-1`. The constant `2K_nest` remains valid because the source loss `w` is charged, exactly as in the nested case. The value is labelled and not bound.
4. **Crude tiers.**
   - Forward: `9472/24454143 ≈ 3.873e-4` at `q=1/64`.
   - Reverse: `296/390625 ≈ 7.578e-4`.

   Both fail `1/2000000`, and both are reported and retained, not relabelled. At the floor, the crude tiers `14453125/684115704` (forward) and `1/32` (reverse) meet `1/12`. They are reported only; the bound floor is the exact_first_order value.
5. **Scaling ratios.** Each ratio comes from the same exact formula at `tau/100`, with no intermediate rounding:

   | ratio | forward | reverse | frozen bracket |
   |---|---|---|---|
   | headline, `tau -> tau/100` | 101.2608 | `4340004/43129 ≈ 100.6284` | `[95,105]` |
   | floor | 1.000375 | exactly 1 | `[99/100, 101/100]` |
   | `q_min` | exactly 100 | exactly 100 | — |

   **Bound ratios.** For the bound constants (both reverse), the ratios are `4340004/43129` and `1`.
6. **Lipschitz wording.**
   - **The contract wording.** The semantics of `global_lipschitz_not_decay` call `2J_0G'(R)` the sup-norm Lipschitz constant. That wording originated in my own loop-1/2 triage.
   - **The correct reading.** The fixed-point map has Lipschitz constant `J_0G'(R) < 77/781250`, and `2J_0G'(R) < 77/390625` is AM2's shifted-inverse exclusion constant. The no-decay number `37/6249384 = J_0G(R)/(1-J_0G'(R))` uses the former; with `2J_0G'(R)` it would be `37/6248768`.
   - **Both producers found this independently.** Forward W3, reverse defect 4.
   - **Neither uses a global Lipschitz constant as a decay factor.** Both reject that in their controls.
7. **Refinements recorded but not bound.**
   - **Reverse first-order cancellation, `3773/1364628515625 ≈ 2.765e-9`.** The circle bound is `2·28 rho G'(R) T(rho)`, because the exact first-order parts coincide on supports through `u in R` when `N>=2`. The reverse correctly notes that it is **quadratic in τ**: ratio ≈ 10062.8, outside the linear headline bracket.
     - **Self-correction.** My pre-comparison listed a cancellation value (≈ 2.2622e-9, a different majorant) without noting that it is quadratic. It is a labelled refinement only.
   - **Forward loss-one F1-versus-F2 value `57270955/16662781836767232 ≈ 3.437e-9`.** The extra F2 faces lie inside the outer layer, so no loss is needed (my R11), and the face-level source uses `J_new = 49|tau|/3`. It is reproduced exactly and labelled.
   - **Reverse coefficientwise Cauchy form `14/31441041`.** Recorded, labelled.
   - **The skeptic's contract-form forward constant.** Recorded, labelled.
   - **None of these is bound.**

## Review against the contract items (both producers)

- **Item 1.**
  - **Forward.** The weighted multilinear estimate: the self-map `J_0 w G(R) <= R` and `Gamma = J_0 w G'(R) <= 77/296` hold for every `w in [1, 390625/148]`. At the cap the rational self-map is an equality, and the true `G(R)<148/7` gives strict contraction (my R9).
  - **Reverse.** Disc contraction and analyticity hold on the closed disc of radius `tau_*`, inside the open analyticity radius `R/(28G(R))`.
  - **Both.** The loss is charged per interaction term, never per creation.
- **Item 2.** The order-versus-distance lemma holds with the tree-chain proof. Forward: Lemma W, including the disconnected-output case. Reverse: the Taylor-coefficient form. Enumerations on `Lambda_2..Lambda_4` match mine.
- **Item 3.** Every comparison at both pairs and both signs is covered. The `-tau` rows replay the same `|tau|` formula: this is a replay, not a second confirmation.
- **Item 4.** The crude tier is reported separately and retained, and no global-Lipschitz decay is used.
- **Item 5.**
  - The mandatory template appears once, as one unbroken span, in each report.
  - The phrase scans of both reports are clean: `phrase_scan.py` with the BA1 contract, and my negation-aware scan with the template removed as one literal.
  - The 12 gate fields are exported exactly as frozen.
- **Item 6.** All 37 contract controls are implemented as damaging mutations in each producer:
  - forward: 51 checks and 96 rejected mutations;
  - reverse: 61 checks and 132 rejected mutations.

  Each `check.py` records its own sha256 before the full evaluation, reads the targets from the contract, and pins the contract sha256 `2c761366…8532b9`.

## Replays, closures and isolation

The full record is `ba1-replays.json`.
- **Replays.** All four producer replays (forward/reverse × normal/`-O`, fresh external directories) reproduce the frozen `output/` byte for byte:
  - forward: `results.json` `644df274…ceda01`, `source-manifest.json` `57cb62db…98369f1`;
  - reverse: `results.json` `ab495dc1…d10934`, `source-manifest.json` `e61c8946…cdac03ab`.
- **Closures.** `tools/freeze.py verify` reports `verified` for both closures. Each closure has 31 files: `check.py`, `report.md`, 27 inputs and 2 outputs. The freeze records have sha256:
  - forward `cffc6fdf…82d0`;
  - reverse `7749f2f9…c4`.
- **Inventories.** Both input inventories are identical and equal `AGENTS.md` + `contracts/ba1.json` + the 25 shared premises; `forward_additional_premises` is empty. Every snapshot is byte-identical to its repository source.
- **Reverse isolation.** No Round33 skeptic, experts, forward, deliberation, plan, brief or panel file is present. The only skeptic file is the declared Round29 review `research/round29/skeptic/am2.md`.
- **Pre-comparison package.** My package is unchanged since its freeze (record `cb1e1f9b…1f21`, results `2c3afdb2…0fb1`) and replays byte for byte under normal and `-O`.
- **Timeline** (UTC; working-tree mtimes and commit times):

  | time | event |
  |---|---|
  | 21:56:57 | contract frozen (`a4ff218`) |
  | 22:30:49 | my `ba1_check.py` last written |
  | 22:36:35 | my pre-comparison commit (`09ae71e`) |
  | 22:36:44 | forward `check.py` and `report.md` last written |
  | 22:38:15 | forward commit (`721ffe5`) |
  | 22:39:25 | reverse `check.py` last written |
  | 22:40:08 | reverse `report.md` last written |
  | 22:41:21 | reverse commit (`e87511b`) |

  I read neither producer before the reverse commit.

## Mutation harness

The review's own source edits run on temporary copies (`<tmp>/repo/<producer path>` with `check.py`, `report.md` and `inputs/`). Each run uses `-B`, and also `-O` in the optimized run. The harness asserts that no interpreter cache is written into a copy.
- **Unmutated copies (2).** Each reproduces its frozen output byte for byte.
- **Validator weakenings (74 = 37 × 2).** For each contract control and each producer, one `require(...)` of that control is replaced by an always-true or subset form. The run must abort with `damaging mutation accepted: <label>`, where the label is that control's own damaging mutation. All 74 abort as expected.

  Two anchors needed care in the reverse:
  - `reverse_premise_isolation`: the forbidden-prefix test is neutralized and the inventory equality is relaxed to a subset, so the harness reaches `forward_ba1_added`;
  - `uniform_in_N_not_in_a`: the second, qualifier `require` is neutralized, giving `unqualified_uniform_rate`.
- **Input edits (5).** Each aborts without output:
  - a contract byte edit without rehash (forward and reverse);
  - an undeclared skeptic file in `inputs/` (forward and reverse);
  - the forward BA1 report placed in the reverse inputs.
- **Damaged packets (10).** The review's own validator rejects each one for the expected reason:
  - forward:
    - headline K halved;
    - skeptic value substituted;
    - crude marked met;
    - `-tau` row differing;
    - F1-vs-F2 distance set to N;
  - reverse:
    - sharp constant presented as the contract form;
    - floor ratio 100;
    - telescoping marked met;
    - crude marked met;
    - template trimmed.

## Blocking issues

None.

## Non-blocking findings

- **N1. Concurrent development and isolation.** My package was on disk, uncommitted, from 22:30:49Z and committed at 22:36:35Z. The forward last wrote `check.py` and `report.md` 9 s after that commit, and the reverse about 3–4 min after. Both reports disclose that nothing under `research/round33/skeptic/` was opened. The content agrees with that:
  - The forward binds a telescoped general comparison and evaluates G' at R, contrary to my R6 reading and my G'(T_w) choice.
  - The reverse records that the cancellation refinement is quadratic, which my package missed.

  Isolation therefore rests on disclosure and content, not on timing. Independence is limited to routes, enumerations and code.
- **N2. Forward headline and floor differ from my pre-comparison values.** The cause is the `G'(R)` evaluation and telescoping (factor 64/63 at the headline). Every value is a valid upper bound, and the F1-vs-F2 value equals the exact variant I listed.
- **N3. Forward union wording.** "New terms lie outside `Lambda_N`" is inaccurate: each new term meets the complement, but it may contain outer-layer sites. The labelled `2K_nest` stays valid with the loss charged.
- **N4. Reverse "positive outer layer" wording.** The literal F1 nested source set is the full outer layer (98/218/386 at N=2,3,4). The same distance `N-1` applies, so no value changes.
- **N5. Lipschitz wording.** Both producers corrected the contract's `2J_0G'(R)` wording (my triage's error): `J_0G'(R)` is the map constant. `37/6249384` is correct; `37/6248768` would follow from the wrong wording. No decay uses either.
- **N6. Self-correction (the review's own).** My pre-comparison listed the first-order cancellation refinement without flagging that it is quadratic in τ, so outside the prefrozen linear headline bracket. My value differs from the reverse's (different majorants). Neither is bound.
- **N7. Convention reads outside `inputs/`.** Both reports disclose reading `research/round33/tools/{README.md,freeze.py,phrase_scan.py}` for conventions. The forward also read `research/round32/forward/ay1/check.py` and its report, and the reverse the header and validators of `research/round32/reverse/ay1/check.py`. None carries premise weight; this matches the Round32 practice.
- **N8. Scratch audit** (names and mtimes only; no file opened). The producers' private folders `/tmp/claude-0/ba1-forward-private` and `/tmp/claude-0/ba1-reverse-private` match their disclosures. The only shared-scratchpad entry after the contract freeze is `bb_previews.py` (22:55:26Z, the modern-lens BB previews), written after both BA1 commits.
- **N9. Thin headline margin.** The bound headline margin is 1.1407. The freeze-time "margin at least 2" rule was checked against the forward preview only (my R4). Acceptance is "at most", so this is recorded, not blocking. Two things would have missed the target at exponent `N-1`: a looser reverse majorant, or telescoping on the analytic route. The labelled refinements have wide room.

## Contract wording defects and readings (reconciled)

| reading (skeptic pre-comparison) | forward | reverse | outcome |
|---|---|---|---|
| R1 nested source set (shell versus literal set) | shell with loss charged | literal distance N−1 ("positive outer layer" understated, N4) | same bound; read as recorded in the limitations |
| R2 lemma form one order weak | contract form bound; sharp labelled | contract form bound; sharp labelled | agree |
| R3 floor bracket fits only the contract form | floor ratio 1.000375; nested contract-form ratio 100 labelled | floor ratio 1; sharp floor labelled | agree |
| R4 thin reverse margin | — | margin 1.1407 recorded | bound value; recorded (N9) |
| R5 general volumes: direct, not union, on the analytic route | union labelled (2K_nest) | direct K; union and telescoping recorded as missing | agree |
| R6 total order makes telescoping unnecessary | telescoping used (valid, 64/63) | direct | both valid |
| R7 `gate_fields_topic_specific` semantics | 12 frozen fields | 12 frozen fields | read as the 12 frozen gate fields |
| R8 floor weight `e^beta = w_max` | w_max | disc radius `tau_*` | agree |
| R9 equality at the cap | strict contraction noted | closed disc inside the analyticity disc | agree |
| R10 l1 fallback moot | tabulated, same distances | not needed | agree |
| R11 loss inside B unnecessary for F1 vs F2 | loss-one refinement labelled | no loss on the disc route | agree |
| R12 cosmetic double space | — | — | no effect |
| R13 cutoff uniformity | every constant uniform in L | every constant uniform in L | agree |
| New: Lipschitz wording `2J_0G'(R)` | W3 | defect 4 | corrected by both (N5) |
| New: F1-vs-F2 source set `max_i |b_i|=N` | — | defect 2 (superset, harmless) | agree |

## Which value to bind, and why

- **Both routes are valid and meet both frozen pairs.** For every comparison, the forward's constants are below the reverse's.
- **The gate should bind the larger valid K per pair:**
  - headline: `K=49/111790368` at `q=1/64`;
  - floor: `K=49/2018304` at `q=148/390625`.

  Both are the reverse's `analytic_disc`, `exact_first_order` constants. Each is certified by both routes, because the forward proves a smaller constant for the same statement.
- **Labelled forward values.** `2734375/12204185915601` (headline) and `708203125/43148545682688` (floor).
- **Also recorded:**
  - the τ ratios `4340004/43129` (headline) and exactly 1 (floor), with `q_min` ratio exactly 100;
  - the crude tiers, which fail at the headline and are retained;
  - every refinement, labelled and not bound.

## Limitations

1. **Model scope.** Only the zero-selected patterned family (selected triple (0,0,0), Haar reference) is covered, with:
   - the cover `R={0,e_z}`, fixed spacing and `|tau|<=10^-8`;
   - F1 and F2 on centered cubes `Lambda_N`, `N>=2`, and complete-factor volumes of one prescription containing `Lambda_N`.

   Nothing transfers to:
   - nonzero selected triples;
   - the uniform route-B model;
   - literal vertex boxes;
   - weak coupling;
   - the continuum.

   Every constant is uniform in N at fixed spacing and in the cutoff, never in a.
2. **Coefficients only.** The statements concern AM2 creation coefficients in each `Q_L`. They are not decay of the reduced density or of any state (BB1/BB2) and not a statement about untruncated creation coefficients. Analyticity in the coupling is not extended to the reduced density: no zero-free region of the complexified normalization is proved.
3. **Cauchy property.** The coefficient Cauchy property gives whole-sequence convergence of coefficients per cutoff space only. `whole_sequence_claimed` and `common_limit_claimed` concern states and stay false. No uniqueness of any ground state is asserted.
4. **Thin headline margin (1.1407).** The labelled refinements are recorded and not bound.
5. **Contract form of the count.** The exponent convention is the contract form; sharp forms are labelled.
6. **Inherited without re-proof:**
   - AM2 majorant, fixed point, uniqueness in the ball and cutoff facts;
   - AV1 first-order coefficient and remainder;
   - AY1 F2 premises;
   - the I1 dictionary.

   Banach, Weierstrass and the maximum principle are standard and not machine-checked.
7. **Limited independence.** Independence is limited to routes, enumerations and code:
   - The contract and selection note name both mechanisms.
   - My triage proposed both routes and the frozen parameters.
   - All agents are correlated model agents.
   - Isolation is verified for repository inputs only.
8. **Upper bounds only.** Scientific priority is unverified.

## Advice for the next loops (planning only)

- **BB1/BB2 (reduced density decay).** Coefficient decay does not transfer to the reduced density without a separate argument: a zero-free region for the normalization, or a polymer or iterated-split estimate. The BA1 constants may enter as premises only through the bound values above, with the exponent convention stated.
- **The sharp count.** A future contract that wants the sharp count should freeze its exponent (`q^N` at `e_z`) and a τ-linear floor bracket before production. The present floor bracket admits only the contract form.
- **The headline margin.** If a later loop needs the headline with more room, the natural candidates are:
  - the direct weighted-norm constant `K_12 + K_nest`, or the F1-vs-F2 value `19140625/86785322066496`;
  - the sharp analytic count.

  Either would have to be prefrozen as its own pair.
