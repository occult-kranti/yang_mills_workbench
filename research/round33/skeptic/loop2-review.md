# Round33 skeptic, deliberation loop 2: review of plan v1 and the draft contracts BA1 and BA2 before freeze

**Standing.** This is a prospective review by a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producers. It is not human peer review and not formal verification. Human project author: Hruday N M (BUNZEEY). The review was written on 2026-09-24, before any Round33 contract was frozen and before any production. It admits nothing, and it is not a research loop. Every decimal below is a preview. The exact rationals were computed with `fractions.Fraction` in my private scratch folder `/tmp/claude-0/skeptic-r33-loop2/` (`loop2_numbers.py`, `ba2_reverse.py`, `build_proposed.py`, `assemble.py`). That folder is not evidence and not a premise, and no reverse producer may receive it.

**Read.**
- `advisor/plan.json`, `advisor/deliberation-1.md`, `advisor/panel.json`, `advisor/selection-ba1.md`, `advisor/selection-ba2.md`;
- the draft contracts `contracts/ba1.json` and `contracts/ba2.json` (commit 23e8922);
- my `skeptic/triage.md`, `recommendation.json` and `prospective-controls.json`;
- the tools `freeze_contract.py` (re-read after commit 7c4c344 added rule R10), `phrase_scan.py` (re-read after the same commit extended its list), `record_gate.py`, `freeze.py` and `reproduce.py`;
- the premise sources that the checks below depend on: AQ1 forward (all of it), AY1 forward §§1–3, the AY2 gate and AY2 forward rows O5–O6, AM2 forward §6, AV1 forward §7, the Round29 source records (`experts/aq-source-dictionary.md`, `aq-primary-bindings.json`, `sources.json`), and the Round32 AV1 and AY1 contracts (for precedent).

**Primary source checked.** I downloaded arXiv:1410.8174v1 into my scratch folder. Its sha256, `501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba`, equals the hash recorded in `research/round29/experts/aq-primary-bindings.json`. I read the statements of Theorem 3.1 (PDF p. 8, eqs. (40)–(52)) and Theorem 4.1 (p. 11, eqs. (77)–(80)).

**Exposure, disclosed.**
- The lens loop-2 responses were committed (ea3242c) while I was reviewing. I did not open them. I saw only the commit subject line: "padding on-site terms in the BA2 source, scoped 'unique' phrasings, headline pair basis". I had already identified the padding issue (item BA2-B3) from AY1 forward §1 line 77 before I saw that line. The agreement is therefore convergent, not independent confirmation.
- A `grep` for `28N` printed lines 148, 172–180, 219 and 315 of `experts/modern/memo.md`. I used its Duhamel form, which `deliberation-1.md` also summarizes, only for the scaling-bracket check.
- **Self-correction.** In loop 1 my triage proposed, as the BA2 reverse route, "each family against its own Nachtergaele–Sims limit". I did not check that route against the comparison target. It cannot meet that target (BA2-B8 below). This corrects my own triage.

**What I ran.**
1. The current freezer, on copies of both drafts in my scratch folder, with `ROOT` patched to the repository for read-only premise checks and the contract path pointed at the copy. **Both drafts fail rule R1.** The pattern `<([^<>]*)>` reads the inequality text between `J<=28|tau|` (or `|tau|<=10^-8`) and `N>=2` as a placeholder. The failures are in BA1 `$.model`, BA2 `$.model`, BA2 `$.parameters.targets.comparison` and BA2 `$.parameters.targets.within_family_cauchy`. With only `N>=2` changed to "N at least 2" (and `|theta|<=8, N>=2` changed to "|theta| at most 8 and N at least 2"), both copies pass every rule, including R10, R8, R4 and the control mirror. Every declared premise exists.
2. The same freezer on proposed copies that carry **all** the blocking edits below. These ran on a scratch overlay ROOT: symlinks to the real repository, plus stand-ins for the two files that the edits require the advisor to create (`advisor/deliberation-2.md` and `sources/nachtergaele-sims-1410.8174v1.md`). Both copies freeze. No replacement text contains an R1 span.
3. `phrase_scan.py` on each mandatory template, both as drafted and as proposed. The tool itself strips the template, so that run is vacuous. I therefore also scanned each template with the template field emptied, against the round list plus the contract list, and against a stricter list: 'unique ground state', 'uniqueness of the ground state', 'correlation length', 'uniform in a', 'fraction of the', 'boundary independent', 'boundary independence', 'confirms', 'the continuum limit' and 'the thermodynamic limit'. **All four templates are clean.** All other contract strings are clean too. The proposed control semantics are clean after rewording three lines that quoted forbidden phrases as mentions.
4. The repository is unchanged except for the two files of this review. `git status` was clean after every scratch run.

---

## (1) Veto conditions: does each draft satisfy them?

### BA1 (conditions from `recommendation.json`, BA1)

| # | veto condition | draft field | satisfied? |
|---|---|---|---|
| 1 | metric, `d_X`, weights (`w=e^mu`, `e^beta`) or `N_0` missing from parameters, or ℓ1 and ℓ∞ mixed | `parameters.metric` names the coarse ℓ∞ metric with `d_X=1`, and ℓ1 (diameter 2) as a labelled alternative, "never mixed". `parameters.weights` gives no numeric `w`, `e^beta` or maximum weight, and it calls the star-count weight `w^{n(I)}` "equivalently the coarse l-infinity diameter weight". That is false: `n(I) >= diam(I)`, and eight sites of diameter 1 need two stars. `N_0` appears only in the model prose. | **No** → B2, B4, B5 |
| 2 | global Lipschitz constant `2J_0G'(R)` used as a decay factor | `required[3]` ("never use the global Lipschitz constant ... as a decay factor"); control `global_lipschitz_not_decay`; `acceptance.insufficient` | yes |
| 3 | loss factor omitted or charged per creation | `parameters.weights` ("loss paid once per interaction"); `required[0]`; control `loss_per_interaction_not_per_creation` | yes |
| 4 | difference weight in the wrong direction or not submultiplicative | `parameters.weights`: "measured by distance from the boundary source" is correct, but "growing towards R's complement" states the reversed direction. The field contradicts itself. | **No** → B2 |
| 5 | any statement about `rho_R` or states | `claim_exclusions[0]` and `required[4]` are right, but `preregistration.sub_labels_allowed` admits `convergence_of_named_constructions`, `common_limit_of_named_constructions` and `dynamics_on_compact_windows` | **No** → B9 |
| 6 | any statement about untruncated creation coefficients | `parameters.cutoff`: "L>=24 uniform, **then removed as in AV1**". AV1 §7 removes the cutoff for the ground *vector*, and AM2 §6 removes it for eigenvalues. No untruncated coefficient exists. `claim_exclusions[4]` ("beyond the AM2 cutoff-removal chain") implies one does. The template has no cutoff qualifier. | **No** → B3, B10, B12, B13 |
| 7 | F2 regrouping not charged face by face, or charged twice | `required[2]` ("charged face by face exactly once"); control `f2_regrouping_charged_once` | yes |
| 8 | headline (q,K) not frozen, margin below 2, or q below `q_min` | The headline `(1/64, 1/2000000)` has margin 2.2723 against my `K_ii = 2.20045e-7` (variants: 2.2670, 2.2527). The **floor `(148/390625, 1/16)` has margin 1.99924** against the analytic preview `(1/32)/(1-q) = 0.0312618`, exactly `2(1-148/390625)`, **below 2**. `q` is never below `q_min`. | **No** → B6, B7, B11 |
| 9 | τ-scaling bracket not declared per constant (AV1's [99,101] rejects the valid `K_ii` ratio ≈ 101.03) | `K_ii`: [100,102.5] contains 101.030. So do my variants 101.261 and 101.897. **`K_floor`: [99,101] is wrong.** The floor rate scales as `q_min(tau)=37888|tau|` (ratio exactly 100), and `K_floor` is τ-independent at leading order (analytic ratio 1.000375; weighted form invariant). Every valid floor constant would be rejected. | **No** → B8 |
| 10 | reverse inventory containing the triage, deliberations, loop-2 responses, a lens memo proposing the forward route, or forward files | `shared_premises` contains none of these, and `reverse_premise_isolation` is true. The selection note and the contract name both routes, as Round32 contracts did; that is acceptable. | yes |
| 11 | analyticity route extended to `rho_R` without a zero-free region | `claim_exclusions[0]`; control `analytic_route_disc_radius` (but see B16: no control carries semantics) | yes (after B16) |
| general | "the thermodynamic limit", "uniqueness of the ground state" or "correlation length" used affirmatively | They appear only in `forbidden_phrasings`, and the scan is clean. | yes |

### BA2 (conditions from `recommendation.json`, BA2)

| # | veto condition | draft field | satisfied? |
|---|---|---|---|
| 1 | exponential decay in N claimed with AQ1's polynomial F | `claim_exclusions[2]`, `required[3]`; control `lieb_robinson_polynomial_tail` | yes |
| 2 | exponential `F_mu` not declared as a new labelled instance | `parameters.weights` ("separately labelled instance with its own constants and is optional") | yes (N5: no target frozen for it) |
| 3 | Lieb–Robinson inequality paraphrased rather than quoted verbatim from Nachtergaele–Sims | `required[0]` asks for a verbatim quote "as the AQ1 report states it". **AQ1 states no inequality.** It says only that the model satisfies "Nachtergaele–Sims Section3 and Theorem4.1". The repository holds no verbatim text: Round29 kept its reading copy in `/tmp` and recorded hashes only. Moreover the inequality is **Theorem 3.1, eq. (51)–(52)**; Theorem 4.1, eq. (77), is the limit dynamics. As drafted, a verbatim quote cannot be produced from any premise. | **No** → B5, B6 |
| 4 | Lieb–Robinson bound applied to unbounded on-site terms without the interaction-picture placement | `required[0]` asks for the placement. But `parameters.boundary_source` omits the **padding on-site terms** of F2 (I1 §6; AY1 forward §1: "pads to `B_+` with the onsite `h_x` alone"). These terms are unbounded. A Duhamel difference that keeps them is not bounded, and one that drops them silently is unjustified. They commute with `H^(2)_N`, with the faces and with `B(H_R)`, so they factor out exactly, but this must be derived. On `B_+`, F2 is **not** the Nachtergaele–Sims native restriction of `Phi'`; on `Lambda_N` it is. | **No** → B3 |
| 5 | window in u without conversion, or a uniform-in-time claim | `parameters.window`; `preregistration.clock`; `claim_exclusions[1]`; gate field `uniform_in_time_claimed:false` | yes |
| 6 | bound mislabelled in τ order | `required[2]` ("quadratic in tau"); control `duhamel_tau_order_quadratic`. But the comparison bracket [9900,10100] **rejects a valid quadratic form**: the modern lens's `3969 tau^2 theta^2 e^{127008|tau||theta|}` has exact ratio 10101.62 with `e^x <= 1/(1-x)`, and 10101.10 with the true exponential. The Cauchy bracket is left for the producer to declare after derivation, which is the trap itself. | **No** → B9, B5 |
| 7 | equality of GNS dynamics or of correlation functions claimed | `claim_exclusions[0]`; the template; gate field. But `sub_labels_allowed` admits `common_limit_of_named_constructions`, `convergence_of_named_constructions` and `static_not_dynamic`. | **No** → B10 |
| 8 | "boundary independence of the dynamics" without "algebraic, compact windows, named families" | title and template qualify it | yes |
| 9 | extra-face count 28N(5N+1) or distance N−1 not derived by enumeration plus an all-size argument | `required[1]`, `parameters.boundary_source` ("to be derived"). The count agrees with the Round32 enumeration (616 at N=2, 1344 at N=3). Every owner of an extra face lies on the outer layer `max_i|b_i|=N`: at ℓ1 ≥ N−1 from `e_z` and ≥ N from 0. **But `parameters.metric` says "l1 metric on Z^3 fine sites as in AQ1".** AQ1 §3 uses ℓ1 on the **coarse** factor lattice (stars `{0,e_x,e_y,e_z}` of ℓ1 diameter 2, shell count `4r^2+2`). The constants `C<=224` and `||Phi||_F<=2268|tau|` hold only there. | **No** → B2 |
| 10 | inner-evolution constants of one family used for the other without statement | `required[2]` names the inner family; control `duhamel_inner_family_constants` | yes |
| design | not a veto condition, but decisive | **The drafted reverse route cannot meet the comparison target.** The triangle inequality through the two limits gives `(1.0195e-10 + 5.94e-11)/(N-1) = 1.613e-10/(N-1)`. Against the target `6e-11 (5N+1)N^-3` that is 1.61e-10 vs 8.25e-11 at N=2, 4.03e-11 vs 1.25e-11 at N=5, and 1.63e-12 vs 3.0e-14 at N=100. It misses at every N, so the loop would be `limited` by construction. The within-family target is also quantified from N to N+1 only; a per-step bound `c/(N-1)` sums to a divergent harmonic series and does not make the sequence Cauchy. | **No** → B4, B7, B8, B12 |

---

## (2) Edits required before freeze

### Summary of the checks the advisor asked for

- **Metric and diameter.**
  - BA1: coarse ℓ∞ with `d_X=1` is right, and matches my `q_min = 148/390625`. The weight must be unique (B2); the ℓ1 diameter-2 reading remains a labelled alternative.
  - BA2: it must be ℓ1 on the **coarse** lattice, not fine sites (BA2-B2).
  - The two loops use different metrics correctly. A later combination must convert explicitly (`d_inf <= d_1 <= 3 d_inf`, BA1-N7).
- **Weight direction.** Reversed in the draft wording (BA1-B2). The replacement defines `rho_B(I) = max_{p in I} d_inf(p,B)`, with `B` the source set of each comparison, and `e^beta = 64`.
- **(q,K) pairs and margins.**
  - BA1 headline: margin 2.272. Fine.
  - BA1 floor: 1.99924, **fails**. Replace the target with 1/12 (margin 2.666).
  - BA2 comparison: 2.354 (skeptic) and 2.338 (modern). Fine.
  - BA2 Cauchy: 2.452. Fine, once quantified over all M > N; the preview already sums every shell from N−1 to infinity.
  - The drafts' acceptance wording "met (margin at least 2)" would halve every target. The margin is a freeze-time property (BA1-B14, BA2-B8).
- **Tier names.**
  - Rule R10 passes: `tier_names_allowed` is a subset of the plan vocabulary for both loops.
  - But the BA1 headline `tier` field is a token followed by prose.
  - The closed vocabulary also mixes routes (`weighted_norm`, `analytic_disc`) with tiers (`crude_majorant`, `exact_first_order`), so `tier_mixing_rejected` has no deterministic meaning. Fix: a `tier_label_rule` with a tier and a route for every constant, plus a mapping from my prospective ids (BA1-B6, plan P2).
- **Scaling brackets.**
  - `K_ii` [100,102.5]: acceptable (101.03 inside). Widening to [95,105] is non-blocking (N4).
  - `K_floor` [99,101]: **wrong**. Use [99/100,101/100].
  - BA2 comparison [9900,10100]: **too narrow**. Use [9500,10500].
  - BA2 Cauchy: **undeclared**. Use [9500,10500]; it is quadratic because the new stars do not meet R for N ≥ 2.
- **Extra faces and distance.** The count and the distances are correct. The metric wording and the padding must be fixed (BA2-B2, B3).
- **Lieb–Robinson source.**
  - The AQ1 report is **not adequate** as the quotation premise. It cites the theorem but quotes no inequality.
  - The advisor must commit a source excerpt: the verbatim Theorem 3.1 (eqs. (40), (41), (44)–(52)) and Theorem 4.1 (eqs. (77)–(80)), the URL, the PDF sha256 above, pages 7–8 and 11–12, the extraction method and the date. It becomes a shared premise of both BA2 producers (BA2-B5, B6).
  - I confirmed that the form I used in triage matches eq. (51): `||[tau_t(A),B]|| <= (2||A|| ||B||/C)(e^{2||Phi|| C|t|}-1) D(X,Y)`, where `D` sums `F` over `X x dPhi(Y)`, or over `dPhi(X) x Y`, whichever is smaller. The time `t` is the normalized time u of `e^{itH_Lambda}`.
- **F2 dynamics identification.**
  - The padding factorization must be derived (BA2-B3).
  - The F2 limit equals `T_theta`, which follows from the comparison. Theorem 4.1 already gives whole-sequence convergence of each family to its own limit.
  - AY2 row O6 includes AQ1 §§4–5 for F2 limit states (the AY2 gate text). The draft addresses O6 only at the dynamics level, so the rerun is added (BA2-B3, B4, B5, B8).
- **Gate fields.**
  - BA2 lacks `whole_sequence_claimed` with its scope, although whole-sequence convergence of the dynamics is its main claim. It also lacks `dynamics_level` and the identification field (BA2-B11).
  - BA1 lacks the plan field `translation_invariance_claimed` and a scoped coefficient-Cauchy field (N3).
- **Templates.** Both pass the phrase scan, as drafted and as proposed.
  - BA1: the template must carry the cutoff qualifier (BA1-B10).
  - BA2: the template uses "tau" for both the coupling and the evolution, and "B(N)" next to "B(H_R)". Non-blocking (BA2-N1, replacement checked clean).
- **Premise lists.**
  - Nothing that the reverse must not see (no triage, deliberation, lens memo, recommendation or loop-2 file).
  - Missing, blocking: the Nachtergaele–Sims excerpt (BA2).
  - Missing, non-blocking: AW1 gate and report for BA1; the Round29 source dictionary, bindings and AQ1 review for BA2.
  - Weak leak, non-blocking: preview numerals in producer-visible contract fields and selection notes (BA1-N5, BA2-N4).
  - `forward_additional_premises`: none recommended (BA1-N8).
- **Control semantics.** 19 of BA1's 34 ids and 16 of BA2's 31 ids are new in Round33, and 4 more in each are amended or renamed Round32 controls: 23 and 20 ids whose Round33 meaning exists only in my `prospective-controls.json`, which no producer receives and the reverse must not. Round32 contracts carried `new_control_semantics`. Without it the controls cannot be executed as damaging mutations. **Blocking** for both loops (BA1-B16, BA2-B14). The full objects are in `loop2-review.json`.
- **`selected_after`: plan.json is not acceptable.**
  - Its status is `plan_v1_pending_loop2_signoff`, and it is mutable: the history is appended after each sub-round under `goal_change_rule`. No hash binds it, since `record_gate.py` does not bind `selected_after`.
  - Freezer R10 also reads its vocabulary unhashed at freeze time.
  - The selection must follow the loop-2 sign-offs. Round32 precedent: AV1 used `deliberation-3.md`. Replace it with `research/round33/advisor/deliberation-2.md`, which must exist before freeze (R8), and record plan.json's sha256 at each freeze (P5).

The exact replacement texts follow. They are generated from `loop2-review.json`, and each one was checked with the freezer and the phrase scan as described above.

### BA1: blocking edits (exact replacement texts)

**BA1-B1. `$.model`**

Reason: R1: the freezer reads the span from "J<=28|tau|" to "N>" as a placeholder; the draft does not freeze (verified with the current freeze_contract.py on a copy).

Replacement:

```
Zero-selected patterned family (AM2/AQ1): SU(2) Kogut-Susskind form on Z^3 at fixed spacing, coarse 24-link factors, selected triple exactly (0,0,0), Haar product reference, 21 omitted faces per anchor with normalized coefficient -(tau/3) per face (delta=alpha/8), both signs |tau|<=10^-8; the AM2 creation expansion with J<=28|tau|, R=1/64, G(t)=16e^{8t}(1+10t); construction families F1 (AQ1 centered whole-star boxes Lambda_N=[-N,N]^3 in coarse coordinates) and F2 (I1 section 6 all-contained-face boxes with padding on the same Lambda_N), N at least 2; cover R={0,e_z}.
```

**BA1-B2. `$.parameters.weights`**

Reason: Veto conditions 1 and 4 (recommendation.json BA1): the draft names two inequivalent weights as "equivalent" (n(I) is at least the l-infinity diameter, not equal to it), gives no numeric w, e^beta or maximum weight, and its phrase "growing towards R's complement" states the reversed direction while "measured by distance from the boundary source" states the correct one. The reverse radius for the headline pair was not declared.

Replacement:

```
forward: diameter-weighted anchored norm ||c||_w = max_u sum_{I containing u} w^{diam(I)} ||c_I||, diam the coarse l-infinity diameter on factor sites; headline w = e^mu = 64 (q = 1/w = 1/64); admissible w from 1 to 390625/148 (self-map J_0 w G(R) at most R); loss factor w^{d_X} = w charged once per interaction term, never per creation; the star-count weight w^{n(I)} (n(I) the least number of stars in a connected cover of I, n(I) at least diam(I)) is a labelled alternative, never mixed with the diameter weight. Difference weight: ||delta||_{B,beta} = max_u sum_{I containing u} e^{beta rho_B(I)} ||delta_I|| with rho_B(I) = max over p in I of d_inf(p,B), where B is the source set of the comparison (the sites met by the interaction terms present in one box and not the other: the shell Lambda_{N+1} minus Lambda_N for nested comparisons, the outer layer max_i |b_i| = N of Lambda_N for F1 versus F2); e^beta = 64 with beta at most mu; the weight grows with distance from B, that is towards R; a weight growing with distance from R, or a non-submultiplicative pure distance weight, is the rejected reversed direction. Reverse: complex coupling z on a disc of declared radius rho at most tau_star = 1/37888 in the J = 28|z| parametrization (self-map 28 rho G(R) at most R with G(R) below 148/7), q = |tau|/rho: rho = tau_star for the floor pair, rho = 64|tau| for the headline pair.
```

**BA1-B3. `$.parameters.cutoff`**

Reason: Veto condition 6 (untruncated coefficients): "then removed as in AV1" applies AV1's ground-vector cutoff removal to coefficients, which AM2 never defines untruncated; it contradicts control untruncated_coefficients_not_asserted.

Replacement:

```
each on-site cutoff space Q_L (product of 1_[0,L](h_x)), every L (for L at least 24 the first-order coefficients are exact, AV1 section 7); every coefficient statement holds in each Q_L with constants uniform in L; no cutoff removal is applied to coefficients and no untruncated creation expansion is asserted (AM2 section 6 removes the cutoff for eigenvalues and AV1 F20-F23 for the ground vector; reduced densities are BB1/BB2)
```

**BA1-B4. `$.parameters.N_min`**

Reason: Veto condition 1 lists N_0 as a parameters field; the draft has N at least 2 only in the model prose.

Replacement:

```
2 (every comparison is for N at least 2; the exponent N-1 is then at least 1)
```

**BA1-B5. `$.parameters.clock`**

Reason: Plan contract rule: metric, weights, window and clock are named in parameters.

Replacement:

```
not applicable to static coefficients; the round clock s=alpha*t_E/hbar, theta=alpha*t/hbar is named in preregistration.clock
```

**BA1-B6. `$.parameters.rate_constant_pair`**

Reason: Veto condition 8 (margin below 2): the floor target 1/16 against the analytic preview (1/32)/(1-q) = 0.0312618 has margin 1.99924 (exact 2(1-148/390625)), below the frozen-margin rule; 1/12 gives 2.666. The headline tier string mixed a vocabulary token with prose and the closed vocabulary conflates routes (weighted_norm, analytic_disc) with tiers (crude_majorant, exact_first_order), so tier_mixing_rejected had no deterministic meaning.

Replacement:

```
{
 "headline": {
  "q": "1/64",
  "K_target": "1/2000000",
  "tier": "exact_first_order",
  "route": "weighted_norm (forward); analytic_disc with rho = 64|tau| (reverse)"
 },
 "rate_floor": {
  "q": "148/390625",
  "K_target": "1/12",
  "tier": "named by the producer from the closed vocabulary (crude_majorant or exact_first_order)",
  "route": "weighted_norm with w = 390625/148 (forward); analytic_disc with rho = tau_star (reverse)",
  "note": "q_min = 37888|tau| = |tau|/tau_star at the cap; the floor rate scales with |tau|"
 },
 "crude_tier_reported": "crude_majorant at q = 1/64 reported, not a target",
 "tier_label_rule": "every constant carries a tier in {crude_majorant, exact_first_order} and a route in {weighted_norm, analytic_disc}; exact_first_order requires the exact first-order coefficients (AV1) and the self-consistent inequality t at most w t_1/(1 - J w G'(R)) re-derived in the stated norm; mapping from the skeptic prospective ids: crude_i = crude_majorant, exact_first_order_ii = exact_first_order, weighted_i = weighted_norm with crude_majorant, weighted_ii = weighted_norm with exact_first_order"
}
```

**BA1-B7. `$.preregistration.target`**

Reason: Follows the floor-target change; the old note claimed a margin "about 2" that is 1.99924.

Replacement:

```
{
 "quantity": "K at q=1/64 (exact first-order tier) and K at q=148/390625",
 "value": "1/2000000 and 1/12",
 "comparator": "<=",
 "note": "blind discriminating threshold for a new estimate; margins at least 2 against the loop-1 panel previews (about 2.27 for the headline pair and about 2.67 for the floor pair)"
}
```

**BA1-B8. `$.preregistration.scaling_brackets_per_constant`**

Reason: Veto condition 9 (bracket per constant): with the rate at q_min the tau-dependence sits in q (ratio exactly 100), not in K; the draft bracket [99,101] for K_floor would reject every valid floor constant (ratio near 1).

Replacement:

```
{
 "K_exact_first_order_at_q_1_64": "[100,102.5] (deliberation preview 101.03)",
 "K_floor_pair": "[99/100, 101/100] (the floor rate q_min(tau) = 37888|tau| scales with |tau| and K_floor is tau-independent at leading order: analytic 2R/(1-q) has ratio about 1.00038, the weighted form at w = 1/q_min is invariant because J w and w t_1 are)",
 "q_min": "exactly 100 (linear in |tau|)"
}
```

**BA1-B9. `$.preregistration.sub_labels_allowed`**

Reason: Veto condition 5 (no state statement in BA1): convergence_of_named_constructions, common_limit_of_named_constructions and dynamics_on_compact_windows would let a coefficient result carry a state or dynamics label.

Replacement:

```
[
 "boundary_decay_rate_only",
 "static_not_dynamic"
]
```

**BA1-B10. `$.preregistration.mandatory_sentence_template`**

Reason: Veto condition 6: the public sentence must carry the cutoff qualifier, since AM2 coefficients exist only in each cutoff space.

Replacement:

```
For the zero-selected patterned family at the same coupling |tau|<=10^-8, and for the named construction families F1 (centered whole-star boxes) and F2 (all-contained-face boxes with padding) on centered coarse cubes, the AM2 creation coefficients in each on-site cutoff space, on supports meeting the cover R, differ between two boxes of the named constructions by at most K q^(N-1) in the anchored norm, uniformly in the cutoff, where N is the smaller box size; this is decay of the coefficients of the named constructions at a rate in N, not decay of the reduced density, not a statement about untruncated creation coefficients, not uniqueness of any ground state, and not a statement uniform in the lattice spacing a.
```

**BA1-B11. `$.required[3]`**

Reason: Follows the floor-target change (the draft item still carried 1/16).

Replacement:

```
4. Prove the coefficient-difference bound sum_{I containing u, I meeting R} ||c_I^{box1}-c_I^{box2}|| <= K q^(N-1) for u in R with the frozen headline pair (q=1/64, K<=1/2000000 at the exact first-order tier) and the floor pair (q=148/390625, K at most 1/12), both signs of tau, for every comparison; report the crude-majorant tier separately; never use the global Lipschitz constant 2J_0G'(R) as a decay factor.
```

**BA1-B12. `$.claim_exclusions[4]`**

Reason: Veto condition 6: "beyond the AM2 cutoff-removal chain" implies such a chain exists for coefficients; it does not.

Replacement:

```
any statement about untruncated creation coefficients (AM2 section 6 removes the cutoff for eigenvalues and AV1 F20-F23 for the ground vector; neither defines untruncated coefficients)
```

**BA1-B13. `$.preregistration.error_terms_itemized`**

Reason: Follows the cutoff edit.

Replacement:

```
[
 "weighted_contraction_loss",
 "boundary_source_terms",
 "order_versus_distance_count",
 "exact_first_order_remainder",
 "cutoff_uniformity",
 "arithmetic"
]
```

**BA1-B14. `$.acceptance`**

Reason: The draft phrase "frozen pairs met (margin at least 2)" can be read as requiring K at most target/2, which silently halves every target and flips verdicts; the margin rule is a freeze-time rule.

Replacement:

```
{
 "accepted_within_scope": "Both routes prove the coefficient-difference bound for every comparison, at both signs, with each proved constant at most its frozen target (the margin of at least 2 is a freeze-time property of the target against the loop-1 previews, not an acceptance condition).",
 "limited": "Only the floor pair, only one comparison, or only the crude tier is proved; or the diameter convention fails and only the l1 alternative closes.",
 "insufficient": "The weighted contraction fails at the cap, or the bound is derived from the global Lipschitz constant."
}
```

**BA1-B15. `$.selected_after`**

Reason: plan.json is a mutable file (status plan_v1_pending_loop2_signoff; history appended after each sub-round) and is bound by no hash; the selection must follow the loop-2 sign-offs (Round32 precedent: AV1 selected_after deliberation-3.md). The file must exist before freeze (freezer R8).

Replacement:

```
research/round33/advisor/deliberation-2.md
```

**BA1-B16. `$.new_control_semantics`**

Reason: Nineteen of the thirty-four control ids are new in Round33 and four more are amended or renamed Round32 controls; their Round33 meaning exists only in skeptic/prospective-controls.json, which no producer receives (and the reverse must not). Round32 contracts carried new_control_semantics; without it the controls are not executable as damaging mutations and the tier and bracket semantics would silently follow the stale prospective wording. Text sanitized of angle brackets for R1.

Replacement: a new object with one line per control id; the full text is in `loop2-review.json` at `ba1.blocking[15].replacement`. Amended lines (the rest are the prospective semantics with angle brackets written in words):

- `tier_mixing_rejected`: Every constant names its tier in {crude_majorant, exact_first_order} and its route in {weighted_norm, analytic_disc}; an exact_first_order constant uses the exact first-order coefficients (AV1) with the self-consistent inequality t at most w t_1/(1 - J w G'(R)) re-derived in the norm in which it is stated; an exact first-order source combined with a crude_majorant t is labelled crude_majorant; any other mixing is rejected.
- `tau_scaling_exponent`: Each headline constant's exact ratio C(tau)/C(tau/100), computed from the same exact formula without intermediate rounding, lies in its bracket in preregistration.scaling_brackets_per_constant; a bound of the wrong tau order, or a bracket chosen after evaluation, is rejected.
- `reverse_premise_isolation`: The reverse inputs/ inventory equals AGENTS.md, this contract and shared_premises exactly; it contains no skeptic triage, recommendation, prospective-controls or loop-2 review, no deliberation, no lens memo, recommendation or loop-2 response, and no forward file of this loop.
- `q_min_not_crossed`: A rate below the proved minimum q_min = J G(r)/r at the declared radius (148/390625 at r = R = 1/64) is rejected; a rate proved at another radius is reported only with that radius named.
- `analytic_route_disc_radius`: The analyticity route uses a declared disc radius rho at most tau_star = 1/37888 (self-map 28 rho G(R) at most R) with q = |tau|/rho (rho = tau_star for the floor pair, rho = 64|tau| for the headline pair) and the order-versus-distance count; extending it to rho_R without a proved zero-free region for the complexified normalization is rejected.
- `untruncated_coefficients_not_asserted`: Every coefficient statement holds in each on-site cutoff space Q_L with constants uniform in L; no cutoff removal is applied to coefficients and no untruncated creation expansion is asserted (AM2 section 6 removes the cutoff for eigenvalues, AV1 F20-F23 for the ground vector).
- `weight_direction_toward_source`: The difference weight e^{beta rho_B(I)}, rho_B(I) = max over p in I of d_inf(p,B), grows with distance from the source set B of the comparison (towards R); a weight growing with distance from R, or a non-submultiplicative pure distance weight, is rejected by a fixture.

### BA1: non-blocking edits

**BA1-N1. `$.parameters.comparisons[3]`**. The named constructions are centered cubes, so "general volumes via the union" is either redundant or a scope extension; state which, and label the general-volume item as the BB2 input.

Replacement:

```
any two centered boxes Lambda_M and Lambda_M' (M, M' at least N) of F1 or F2, by telescoping and the same-N F1/F2 comparison; separately labelled: any two finite complete-factor volumes of one prescription both containing Lambda_N, compared through their union (input to the BB2 pre-registered translation item)
```

**BA1-N2. `$.controls and $.preregistration.controls_required.ids`**. full_original_wilson_cover is a universal control (the exponents N-1, N, N+1 depend on R={0,e_z}); gate_fields_topic_specific makes the exported fields executable. Add their semantics: {"full_original_wilson_cover": "The cover R={0,e_z} (48 links, 36 endpoints, 7 incident anchors) is used; a one-factor cover is rejected.", "gate_fields_topic_specific": "Convergence contracts export whole_sequence_claimed, rate_in_N_claimed, common_limit_claimed, uniqueness_all_ground_states_claimed and dynamics_level; a missing field is rejected."}

Replacement:

```
[
 "coherent_evidence_tampering",
 "exact_arithmetic_admission",
 "no_priority_or_continuum_claim",
 "changed_model_relabelled",
 "insufficient_verdict_retained",
 "tau_scaling_exponent",
 "wrong_delta_alpha_hbar_clock",
 "missing_incoming_stars",
 "root_n_misuse",
 "tier_mixing_rejected",
 "reverse_premise_isolation",
 "face_count_all_sites",
 "uniform_in_N_not_in_a",
 "placeholder_span_rejected",
 "negation_aware_phrase_scan",
 "parameters_declare_metric_weights_window",
 "global_lipschitz_not_decay",
 "weighted_norm_contraction_rechecked",
 "loss_per_interaction_not_per_creation",
 "diameter_subadditivity_through_interaction",
 "coarse_metric_named",
 "weight_direction_toward_source",
 "c ... (full text in loop2-review.json)
```

**BA1-N3. `$.preregistration.gate_fields_required`**. translation_invariance_claimed is a plan gate field; the coefficient Cauchy property that BA1 does prove needs its own scoped field so that whole_sequence_claimed=false (states) stays unambiguous.

Replacement:

```
{
 "uniqueness_of_ground_state_claimed": false,
 "whole_sequence_claimed": false,
 "state_decay_claimed": false,
 "rate_in_N_claimed": true,
 "rate_in_a_claimed": false,
 "continuum_claim": false,
 "scientific_priority_verified": false,
 "translation_invariance_claimed": false,
 "common_limit_claimed": false,
 "weak_coupling_claim": false,
 "coefficient_cauchy_claimed": true,
 "coefficient_cauchy_scope": "AM2 creation coefficients of F1 and F2 on supports meeting R, in each on-site cutoff space"
}
```

**BA1-N4. `$.preregistration.scaling_brackets_per_constant.K_exact_first_order_at_q_1_64`**. [100,102.5] contains my three exact variants (101.030, 101.261, 101.897) but has no slack at the lower edge for a rounded K(tau/100); [95,105] still separates linear from square-root (10) and quadratic (10^4).

Replacement:

```
[95,105] (linear in tau with a positive nonlinear correction; computed from the same exact formula at tau and tau/100 without intermediate rounding)
```

**BA1-N5. `$.preregistration.target.note, $.preregistration.scaling_brackets_per_constant, $.parameters.rate_constant_pair.crude_tier_reported`**. The reverse should derive its constants blind; the freeze-time margin can be documented outside the premise closure.

Replacement:

```
remove the preview numerals (2.2004e-7, 0.0313, 101.03, 2.9e-4) from producer-visible contract fields; record them in the loop-2 synthesis, which no producer receives
```

**BA1-N6. `$.shared_premises`**. The exact_first_order tier rests on c^(1) = L_0 = -(tau/72) sum_f W_f Omega_0 and the amplitude lemma (AW1 F02, F11-F15); AV1 carries t_1 but AW1 carries the formula. Route-neutral, both producers.

Replacement:

```
append research/round32/advisor/aw1-gate.json and research/round32/forward/aw1/report.md
```

**BA1-N7. `$.parameters.metric`**. BA1 (l-infinity) and BA2 (l1) are correct separately; BB1/BB2 will combine them.

Replacement:

```
coarse l-infinity metric on factor sites; every whole star phi_b has support b+S with l-infinity diameter d_X=1 (to be verified by enumeration; an l1 reading with diameter 2 is a labelled alternative, never mixed); any later combination with the coarse l1 Lieb-Robinson constants of BA2 converts explicitly (d_inf at most d_1 at most 3 d_inf)
```

**BA1-N8. `$.forward_additional_premises`**. Round32 gave forward producers the skeptic triage; here triage (a).2 is the forward route in full, so giving it would make my previews a copy rather than a separate check. If the advisor adds any, list them and record that the triage numbers no longer count as a separate derivation.

Replacement:

```
none
```

**BA1-N9. `$.model`**. Makes the padding explicit for coefficients too (AY1 forward section 1).

Replacement:

```
append: "the F2 padding sites carry no interaction, so coefficients on supports meeting the padding vanish"
```

### BA2: blocking edits (exact replacement texts)

**BA2-B1. `$.model`**

Reason: R1: the span from "|tau|<=10^-8" to "N>" is read as a placeholder; the draft does not freeze.

Replacement:

```
Zero-selected patterned family (AM2/AQ1) as in BA1, both signs |tau|<=10^-8; construction families F1 (AQ1 centered whole-star boxes) and F2 (I1 section 6 all-contained-face boxes with padding) on the same Lambda_N, N at least 2; Heisenberg dynamics generated by the finite-box Hamiltonians with the unbounded on-site Casimir terms h_b and bounded finite-range interactions; observables A in B(H_R), cover R={0,e_z}.
```

**BA2-B2. `$.parameters.metric`**

Reason: AQ1 section 3 uses the l1 metric on the coarse factor lattice (stars S={0,e_x,e_y,e_z} of l1 diameter 2, shell count 4r^2+2); "fine sites" would invalidate C at most 224 and ||Phi||_F at most 2268|tau|. Metric veto (recommendation.json, parameters rule).

Replacement:

```
l1 metric on the coarse Z^3 factor lattice, as in AQ1 section 3 (F(r)=(1+r)^-4 with 4r^2+2 sites at l1 distance r, convolution constant C at most 224, ||Phi||_F at most 81J = 2268|tau| for whole stars of l1 diameter 2); the F2 owner-set interaction ||Phi'||_F at most 1323|tau| (AY1 reverse) in the same metric; no fine-site metric and no coarse-to-fine conversion enters any constant
```

**BA2-B3. `$.parameters.boundary_source`**

Reason: Veto conditions (unbounded on-site terms; extra-face derivation): the draft source omits the padding on-site terms of the F2 prescription; they are unbounded, so a Duhamel difference that silently keeps them is not bounded and one that silently drops them is unjustified. I identified this from AY1 forward section 1 ("I1 section 6 pads to B_+ with the onsite h_x alone").

Replacement:

```
H^{F2,pad}_N minus H^{F1}_N equals the sum of the 28N(5N+1) faces with owner set inside Lambda_N and anchor b with b+S not inside Lambda_N, plus the on-site terms h_x on the padding B_+ minus Lambda_N (I1 section 6, AY1 forward section 1); the padding terms commute with H^(2)_N, with every face and with B(H_R), so they factor out of the evolution exactly and the Duhamel difference is the bounded sum over the extra faces (derived, not assumed; F2 on Lambda_N without padding is the Nachtergaele-Sims native restriction of Phi'); every owner of every extra face lies on the outer layer max_i |b_i| = N, hence at coarse l1 distance at least N-1 from e_z and at least N from 0; count and distance derived by enumeration on Lambda_2 and Lambda_3 plus an all-size argument; each face charged exactly once
```

**BA2-B4. `$.parameters.targets`**

Reason: R1 on two strings; and the within-family target quantified N to N+1 only: a bound c/(N-1) per step is harmonic and does not make the sequence Cauchy. The preview 1.0195e-10 already bounds all M above N (shell sum from N-1 to infinity), so the fix keeps the margin 2.45. O6 per the AY2 gate includes AQ1 sections 4-5 for F2.

Replacement:

```
{
 "comparison": "||tau^{F2,N}_theta(A)-tau^{F1,N}_theta(A)|| <= 6x10^-11 (5N+1) N^-3 ||A|| for |theta| at most 8 and N at least 2 (polynomial_lieb_robinson tier; previews 2.549e-11 and 2.566e-11)",
 "within_family_cauchy": "sup over M greater than N of ||tau^{F1,M}_theta(A)-tau^{F1,N}_theta(A)|| at most 2.5x10^-10/(N-1) ||A|| for |theta| at most 8 and N at least 2, and the same for F2 (preview 1.0195e-10 for F1); hence ||T_theta(A)-tau^{F1,N}_theta(A)|| at most 2.5x10^-10/(N-1) ||A||; the O(1/N) rate is the honest polynomial-F rate; an N to N+1 bound alone is not a Cauchy estimate",
 "f2_dynamics": "the F2 finite-box evolutions converge as a whole sequence in norm on compact windows and their limit equals the AQ1 limit dynamics T_theta (identified through the comparison bound); AQ1 sections 4-5 rerun for every subsequential F2 limit state (AY2 row O6)"
}
```

**BA2-B5. `$.required`**

Reason: Item 1: AQ1 does not state the inequality at all (it cites "Section3 and Theorem4.1" and says the hypotheses are met); the inequality is Theorem 3.1 eq. (51), the limit Theorem 4.1 eq. (77) (checked on the arXiv v1 PDF whose sha256 matches research/round29/experts/aq-primary-bindings.json). Item 4: quantifier and O6. Item 6: the bracket may not be chosen by the producer after the tau order is derived.

Replacement:

```
[
 "1. Quote the Lieb-Robinson inequality verbatim from the committed source excerpt research/round33/sources/nachtergaele-sims-1410.8174v1.md (Nachtergaele-Sims arXiv:1410.8174v1, Theorem 3.1, eqs. (51)-(52), with the definitions (40), (41), (44), (48)-(50); limit dynamics Theorem 4.1, eq. (77)), with F, C and ||Phi||_F named, and place the unbounded on-site terms h_b exactly as that theorem's setting (44)-(47) and its interaction-picture proof require; the AQ1 report is the placement record, not the quotation source; never paraphrase.",
 "2. Derive the F2-minus-F1 boundary source on Lambda_N: the extra faces, their count 28N(5N+1), their anchors and their exact l1 distance (at least N-1 in coarse units, converted to fine units) from R, by enumeration on Lambda_2 and Lambda_3 plus an all-size argument; charge each face exactly once.",
 "3. Prove the Duhamel comparison ||tau^{F2,N}_theta(A)-tau^{F1,N}_theta(A)|| <= B(N)||A|| for |theta|<=8 with B(N) explicit, quadratic in tau (state why the first order vanishes or is bounded), with the inner-family constants of the family whose evolution is inside the integral named; evaluate at the cap, both signs, and meet the frozen target 6x10^-11 (5N+1) N^-3 (margin at least 2).",
 "4. Prove the within-family Cauchy estimate sup over M greater than N of ||tau^{F,M}_theta(A)-tau^{F,N}_theta(A)|| for F = F1 and F = F2 at the honest polynomial rate and meet 2.5x10^-10/(N-1); prove that the F2 evolutions converge as a whole sequence on compact windows and that the limit equals the AQ1 limit dynamics T_theta; rerun AQ1 sections 4-5 for every subsequential F2 limit state (stationarity under T_theta, strong continuity of the GNS evolution, nonnegative generator) with F2's own subsequences; never claim exponential decay in N with the polynomial F.",
 "5. State the honest meaning: algebraic Heisenberg dynamics of the named constructions on a compact window; not equality of GNS dynamics or of correlation functions of different states (those need BB2); export the gate fields; quote the mandatory sentence template once as one unbroken span.",
 "6. Declare and check the tau to tau/100 scaling of each headline constant against preregistration.scaling_brackets_per_constant (comparison and Cauchy coefficients are quadratic in tau: [9500,10500]); exact finite fixtures for the traps (polynomial versus exponential tail; an unbounded on-site term placed wrongly; the padding on-site terms left in the Duhamel difference; an inner-family constant swapped; an N to N+1 bound summed as a Cauchy estimate); every control executed as a damaging mutation."
]
```

**BA2-B6. `$.shared_premises`**

Reason: The repository holds no verbatim statement of the theorem; Round29 kept its reading copy in /tmp and recorded only hashes. The advisor must commit, before freeze, an excerpt with the verbatim statements of Theorem 3.1 (eqs. (40), (41), (44)-(52)) and Theorem 4.1 (eqs. (77)-(80)), the URL https://arxiv.org/pdf/1410.8174v1, PDF sha256 501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba, PDF pages 7-8 and 11-12, extraction method and date. It is route-neutral and goes to both producers.

Replacement:

```
[
 "research/round29/forward/am2/report.md",
 "research/round29/reverse/am2/report.md",
 "research/round29/skeptic/am2.md",
 "research/round29/advisor/am2-gate.json",
 "research/round29/forward/aq1/report.md",
 "research/round29/advisor/aq1-gate.json",
 "research/round29/forward/aq2/report.md",
 "research/round21/forward/i1/report.md",
 "research/round32/advisor/av1-gate.json",
 "research/round32/forward/av1/report.md",
 "research/round32/reverse/av1/report.md",
 "research/round32/advisor/ay1-gate.json",
 "research/round32/forward/ay1/report.md",
 "research/round32/reverse/ay1/report.md",
 "research/round32/advisor/ay2-gate.json",
 "research/round32/forward/ay2/report.md",
 "research/round33/methods/paired-physics-research/SKILL.md",
 "research/round33/methods/paired-physics-research/references/complete-residual-and-error-scope.md",
 "research/round33/methods/newton-analysis-synthesis/SKILL.md",
 "research/round33/methods/tesla-mechanism-resonance/SKILL.md",
 "research/round33/methods/historical-physics-panel/SKILL.md",
 "research/round33/methods/qeg-research-advisor/references/round32-state-lemma-and-window.md",
 "research/round33/advisor/selection-ba2.md",
 "research/round33/sources/nachtergaele-sims-1410.8174v1.md"
]
```

**BA2-B7. `$.direction_note`**

Reason: The drafted reverse ("comparison bound by the triangle inequality with its own constants") yields (1.0195e-10 + 5.94e-11)/(N-1) = 1.61e-10/(N-1), which misses the frozen comparison target at every N (N=2: 1.61e-10 against 8.25e-11; N=100: 1.63e-12 against 3.0e-14), so the loop would be limited by construction. The F2-inner Duhamel preview is 1.485e-11 (5N+1)N^-3, margin 4.04. This corrects my own triage, which proposed the limit route for the reverse without checking it against the comparison target. selection-ba2.md must be updated to match.

Replacement:

```
Forward: Duhamel over the extra F2 faces with the inner F1 evolution bounded by the whole-star Nachtergaele-Sims constants (Phi, 2268|tau|). Reverse: Duhamel with the inner F2 evolution bounded by the owner-set constants (Phi', 1323|tau|, re-derived for F2 on Lambda_N) for the comparison; each family against its own Nachtergaele-Sims limit (Theorem 4.1) for the within-family Cauchy estimates; identification of the two limits from the comparison. The triangle inequality through the two limits gives only O(1/N) and cannot meet the comparison target; it may be reported only as a labelled weaker bound. Independence is limited to the inner family, the interaction indexing, the constants, the enumeration and the code.
```

**BA2-B8. `$.acceptance`**

Reason: Removes the ambiguous "margin at least 2" acceptance reading (it would halve the targets) and aligns acceptance with the O6 item.

Replacement:

```
{
 "accepted_within_scope": "Both routes prove the comparison and the within-family Cauchy estimates with each proved constant at most its frozen target, the F2 limit dynamics identified with AQ1's, and AQ1 sections 4-5 rerun for F2 limit states (the margin of at least 2 is a freeze-time property of the targets, not an acceptance condition).",
 "limited": "Only the comparison or only the Cauchy estimates are proved, a target is missed at some N, or the F2 limit-state properties (O6) are not closed.",
 "insufficient": "The Lieb-Robinson inequality does not apply to the unbounded on-site terms as placed, or the boundary source is miscounted."
}
```

**BA2-B9. `$.preregistration.scaling_brackets_per_constant`**

Reason: Veto condition (bracket per constant): the Cauchy bracket was left to the producer after derivation, and [9900,10100] rejects the modern lens's valid directed-exp form (exact ratio 10101.6 with e^x at most 1/(1-x); 10101.1 with the exact exponential) - the same trap as K_ii at 101.03 in AV1's bracket.

Replacement:

```
{
 "comparison_coefficient": "[9500,10500] (quadratic in tau; the loop-1 modern form 3969 tau^2 theta^2 e^{127008|tau||theta|} has ratio about 10101.6 and the skeptic form about 10033.6, so [9900,10100] would reject a valid bound)",
 "cauchy_coefficient": "[9500,10500] (quadratic in tau: the stars outside Lambda_N do not meet R for N at least 2, so the Duhamel integrand vanishes at zero time; preview ratio about 10033.6); the same bracket for F2 and for the F2-inner comparison"
}
```

**BA2-B10. `$.preregistration.sub_labels_allowed`**

Reason: Veto conditions (GNS/correlation equality; "boundary independence" without qualifiers): common_limit_of_named_constructions and convergence_of_named_constructions read as state statements; static_not_dynamic and boundary_decay_rate_only do not describe this loop.

Replacement:

```
[
 "dynamics_on_compact_windows"
]
```

**BA2-B11. `$.preregistration.gate_fields_required`**

Reason: Plan vocabulary: whole_sequence_claimed needs a scope and translation_invariance_claimed is a plan field; the loop's main claims (whole-sequence convergence of the dynamics, identification of the F2 limit) had no field, and the state fields that must stay false were absent.

Replacement:

```
{
 "uniqueness_of_ground_state_claimed": false,
 "gns_dynamics_equality_claimed": false,
 "uniform_in_time_claimed": false,
 "rate_in_N_claimed": true,
 "rate_in_a_claimed": false,
 "continuum_claim": false,
 "scientific_priority_verified": false,
 "whole_sequence_claimed": true,
 "whole_sequence_scope": "finite-box Heisenberg evolutions of F1 and F2 of A in B(H_R), in norm, uniformly for |theta| at most 8; dynamics only, no state",
 "dynamics_level": "algebraic_heisenberg_compact_window",
 "dynamics_limit_identified_claimed": true,
 "common_limit_claimed": false,
 "state_convergence_claimed": false,
 "translation_invariance_claimed": false,
 "weak_coupling_claim": false,
 "true_values_rule": "a field shown true is exported true only if its target is admitted; otherwise false with the reason"
}
```

**BA2-B12. `file:research/round33/advisor/selection-ba2.md (a shared premise of both producers)`**

Reason: The selection note is snapshotted by both producers; left unchanged it would contradict the corrected direction_note and the corrected Cauchy quantifier.

Replacement:

```
replace the phrase "reverse: each family against its own Nachtergaele-Sims limit and identification of the limits" by "reverse: Duhamel with the inner F2 evolution and the owner-set constants, each family against its own Nachtergaele-Sims limit for the Cauchy estimates, and identification of the limits", and "2.5x10^-10/(N-1)" by "2.5x10^-10/(N-1) for all M above N"
```

**BA2-B13. `$.selected_after`**

Reason: As for BA1.

Replacement:

```
research/round33/advisor/deliberation-2.md
```

**BA2-B14. `$.new_control_semantics`**

Reason: As for BA1: sixteen of the thirty-one ids are new in Round33 and four more are amended or renamed; their Round33 meaning is defined only in the skeptic file no producer receives; four are amended here (form quoted from the committed excerpt, inner-family constants both ways, padding, O6 rerun, all-M Cauchy).

Replacement: a new object with one line per control id; the full text is in `loop2-review.json` at `ba2.blocking[13].replacement`. Amended lines (the rest are the prospective semantics with angle brackets written in words):

- `tier_mixing_rejected`: Every constant names its tier in {polynomial_lieb_robinson, exponential_lieb_robinson} and the interaction (whole-star Phi or owner-set Phi') whose Nachtergaele-Sims constants it uses; mixing is rejected.
- `tau_scaling_exponent`: Each headline constant's exact ratio C(tau)/C(tau/100), computed from the same exact formula without intermediate rounding, lies in its bracket in preregistration.scaling_brackets_per_constant; a bound of the wrong tau order, or a bracket chosen after evaluation, is rejected.
- `reverse_premise_isolation`: The reverse inputs/ inventory equals AGENTS.md, this contract and shared_premises exactly; it contains no skeptic triage, recommendation, prospective-controls or loop-2 review, no deliberation, no lens memo, recommendation or loop-2 response, and no forward file of this loop.
- `lieb_robinson_form_quoted`: The Lieb-Robinson inequality and its constants are quoted verbatim from the committed excerpt of Nachtergaele-Sims arXiv:1410.8174v1 (Theorem 3.1, eqs. (51)-(52), with (40), (41), (44), (48)-(50); limit dynamics Theorem 4.1, eq. (77); PDF sha256 501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba); a paraphrased, second-hand or re-derived constant form is rejected.
- `duhamel_inner_family_constants`: In a Duhamel formula only the inner family's constants enter (F1 inner: Phi, 2268|tau|; F2 inner: Phi', 1323|tau|); the inner family is named for every bound; using the other family's constants unstated is rejected.
- `extra_face_count_and_distance`: 28N(5N+1) extra F2 faces, at most 3 owners each, every owner on the outer layer max_i |b_i| = N and hence at coarse l1 distance at least N-1 from e_z and at least N from 0, derived by enumeration (N = 2, 3) and an all-size argument; the padding on-site terms are shown to factor out exactly and are never charged as boundary terms.
- `f2_limit_dynamics_equals_f1`: F2 finite dynamics converge as a whole sequence in norm on compact windows to the AQ1 automorphism group T_theta, identified through the comparison bound; stationarity, strong GNS continuity and a nonnegative generator for every subsequential F2 limit state are rerun (AQ1 sections 4-5) with F2's own subsequences, not assumed.
- `lieb_robinson_polynomial_tail`: With AQ1's F(r)=(1+r)^-4 the F1-versus-F2 bound decays like N^-2 and each family's Cauchy estimate like 1/N, stated for all M above N (an N to N+1 bound summed as a Cauchy estimate is rejected: the harmonic sum diverges); an exponential rate claimed with AQ1 constants is rejected.

### BA2: non-blocking edits

**BA2-N1. `$.preregistration.mandatory_sentence_template (and the same symbol change in observable.id, parameters.targets, required)`**. tau is both the coupling and the evolution, and B(N) collides with B(H_R); AQ1 writes T_t. The replacement passes phrase_scan and has no R1 span.

Replacement:

```
For the zero-selected patterned family at the same coupling |tau|<=10^-8 and every A in B(H_R) with ||A||<=1 on the fixed cover R, the finite-box Heisenberg evolutions T^{F1,N}_theta and T^{F2,N}_theta of the named construction families F1 and F2 on the same centered coarse cube Lambda_N satisfy ||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| <= b(N) for |theta|<=8 in the common clock theta=alpha t/hbar; this is an algebraic comparison of the dynamics of the named constructions on a compact time window at a rate in N, not equality of GNS dynamics or of correlation functions of different states, not a uniform-in-time statement, and not a statement uniform in the lattice spacing a.
```

**BA2-N2. `$.controls and $.preregistration.controls_required.ids`**. Universal cover control; norm-on-compact-windows topology; one coupling per comparison; executable gate fields. Add their semantics: {"full_original_wilson_cover": "The cover R={0,e_z} (48 links, 36 endpoints, 7 incident anchors) is used; a one-factor cover is rejected.", "topology_named": "Trace norm on B(H_Y) for states, norm on compact theta windows for dynamics, GNS strong for representations; a fixed-vector versus moving-vector fixture is included.", "cross_coupling_comparison_rejected": "Every convergence or comparison is at one coupling; a +tau/-tau comparison (difference at least 8.76e-10) presented as boundary comparison is rejected.", "gate_fields_topic_specific": "Convergence contracts export whole_sequence_claimed, rate_in_N_claimed, common_limit_claimed, uniqueness_all_ground_states_claimed and dynamics_level; a missing field is rejected."}

Replacement:

```
[
 "coherent_evidence_tampering",
 "exact_arithmetic_admission",
 "no_priority_or_continuum_claim",
 "changed_model_relabelled",
 "insufficient_verdict_retained",
 "tau_scaling_exponent",
 "wrong_delta_alpha_hbar_clock",
 "missing_incoming_stars",
 "root_n_misuse",
 "tier_mixing_rejected",
 "reverse_premise_isolation",
 "face_count_all_sites",
 "uniform_in_N_not_in_a",
 "placeholder_span_rejected",
 "negation_aware_phrase_scan",
 "parameters_declare_metric_weights_window",
 "lieb_robinson_polynomial_tail",
 "lieb_robinson_F_declared",
 "lieb_robinson_form_quoted",
 "unbounded_onsite_interaction_picture",
 "duhamel_inner_family_constants",
 "extra_face_count_and_distance",
 "duhamel_tau_order ... (full text in loop2-review.json)
```

**BA2-N3. `$.shared_premises`**. The Round29 placement dictionary (l1 on the coarse lattice, interaction-picture placement, clock conversion), the PDF hash the new excerpt must match, and the AQ1 review of the placement. Route-neutral.

Replacement:

```
append research/round29/experts/aq-source-dictionary.md, research/round29/experts/aq-primary-bindings.json and research/round29/skeptic/aq1.md
```

**BA2-N4. `$.parameters.targets, $.preregistration.target.note, research/round33/advisor/selection-ba2.md`**. They are the modern lens's and my values; the reverse should derive blind.

Replacement:

```
remove the preview numerals (2.549e-11, 2.566e-11, 1.0195e-10) from producer-visible text; record them in the loop-2 synthesis
```

**BA2-N5. `$.parameters.weights`**. Prevents a post-hoc exponential-in-N headline.

Replacement:

```
Lieb-Robinson decay function F(r)=(1+r)^-4 (polynomial, AQ1); an exponential F_mu(r)=e^{-mu r}F(r) is a separately labelled instance with its own constants and is optional; no target is frozen for the exponential instance, so any such result is a labelled extra without admission weight in this loop
```

**BA2-N6. `$.direction_note (optional extra)`**. For this finite-range bounded interaction at a fixed window it decays faster than any power of N; a genuinely different mechanism, useful as a cross-check, but it must not replace the frozen polynomial-tier targets.

Replacement:

```
an interaction-picture Dyson bound with an order-versus-distance count (a nonzero nested commutator must chain from R to an extra face) may be reported as a labelled extra; it is not a target
```

---

## (3) Plan v1: sign-off, with required changes

**Decision.**
- **BA1 and BA2: freeze vetoed** until their blocking edits (16 and 14) are applied. After that I do not need another loop: the edited copies already pass the freezer and the scan. The advisor should apply the edits, create `advisor/deliberation-2.md` and `sources/nachtergaele-sims-1410.8174v1.md`, and freeze. I will check the frozen bytes against `loop2-review.json` at review time.
- **Plan v1: signed off.** This covers the architecture (four sub-rounds, locality → convergence → consequences → applications), the direction rules, the zero-count assistant rule, the decision not to schedule a Dobrushin/HTW loop (with the Jung dissent recorded), and the sub-round-1 selection.
- The sign-off carries required changes:
  - **P1–P5** must be recorded in plan.json history before any sub-round-2 contract is drafted;
  - **P6–P11** bind the corresponding contracts.

**Required changes.**

- **P1. Vocabulary.**
  - Delete the exception "the thermodynamic limit (except as the limit of the named construction after admission)". The phrase is never used; the admitted object is "the limit of the named constructions".
  - Add "correlation length" and an unqualified "uniform in a" to the forbidden list.
- **P2. Tiers.** Add a `tier_label_rule`.
  - Tiers: `crude_majorant`, `exact_first_order`, `polynomial_lieb_robinson`, `exponential_lieb_robinson`, `first_order_distance_from_product`.
  - Routes: `weighted_norm`, `analytic_disc`, `polymer_kp`, `iterated_split`.
  - Every constant carries both. R10 checks only the list, so the rule must be stated in the plan and in each contract.
- **P3. Gate fields.** Close the gate-field vocabulary over every field the contracts use (listed in the JSON).
- **P4. Contract rules.**
  - (a) Brackets admit every valid form of the declared τ order: linear [95,105], quadratic [9500,10500], unless exact variants justify a narrower one. They are declared before production.
  - (b) The margin of 2 is a freeze-time property. Acceptance means "proved constant at most the frozen target".
  - (c) Every contract carries `new_control_semantics`.
  - (d) An external theorem is quoted from a committed, hash-bound excerpt, never from a report that cites it.
  - (e) A within-family Cauchy target is quantified over all M > N.
- **P5. `selected_after`.** It never names plan.json. Record plan.json's sha256 in `history` at each freeze.
- **P6. BB2 direction: paired, fixed now.** The plan defers it to selection; I do not accept that deferral.
  - Forward: nested telescoping with BA1 and BB1, and cutoff removal at fixed N via AV1 F20–F23.
  - Reverse: general-volume comparison through unions, which also gives coarse translation covariance.
  - Coarse translation invariance is a pre-registered item. Its input is BA1's separately labelled general-volume comparison (BA1-N1). If that item is not admitted, translation invariance is dropped from BB2 and recorded as a limitation.
- **P7. BB1.**
  - The reverse receives neither the modern memo (polymer constants) nor my triage.
  - `eta`, `kappa_0`, `w'` and the (q,K) pair are frozen with margin 2.
  - No analyticity claim for `rho_R` without a zero-free region.
  - The fixture showing that coefficient decay is not marginal decay is mandatory.
- **P8. BC1.**
  - Direction: **statement+skeptic**, not single+skeptic. It restates certificates with unchanged radii.
  - Either name "common correlation functions and GNS dynamics of F1 and F2 once BA2 and BB2 are admitted" as an item, or exclude it.
  - Round32 gates stay untouched.
- **P9. BC2.**
  - Single+skeptic, with every route-B constant re-derived.
  - It runs only if BB1 and BB2 are `accepted_within_scope`. Otherwise use the pre-frozen boundary-class alternative, or record the obligation.
- **P10. BD1.** Paired is acceptable (characters against exact Weyl integration), provided that:
  - every cell has an exact check;
  - the SU(3) and SO(3) obstruction cells are mandatory (SU(3): `E[(Re Tr U/3)^3]=1/108`);
  - the convention is frozen in the contract;
  - `1/144` and `tau=96/g^4` are never transferred;
  - the plan says which loop owns the 2D flip set and its recounts.
- **P11. BD2.**
  - Single+skeptic.
  - The Z^3 1×2 coefficient `7 tau^2/124416` is stated only as an exact second-order coefficient with a certified third-order remainder. Otherwise it is a labelled formal coefficient carrying the sign obstruction.
  - Electric energy keeps its unbounded-observable obstruction.
  - Graphs carry FG model ids and `hamiltonian_terms` (R3).
  - Calculators display gate-bound values only.
- **P12. Selection notes.** `subrounds[0]` lists both selection notes.
- **P13. History.** Plan v2 records the BA1 floor change, the BA2 reverse-route correction, the Cauchy quantifier and the new source excerpt.

**Tool notes (not required changes; for the advisor's infrastructure).**
- Freezer R1 produces false positives on the inequality digraphs `<=` and `>=`. Both drafts hit it.
- `phrase_scan.py` has two weaknesses in its negation handling:
  - The negation frame is clause-wide. A clause such as "this is X and not Y" passes even when X is forbidden; that is a false negative.
  - The negation list lacks "rejected". A quoted forbidden phrase inside "... is rejected" is flagged; that is a false positive, in the safe direction.
- R10 reads plan.json without binding its hash.

---

## Numbers at a glance (previews; exact rationals in scratch)

| quantity | value | against |
|---|---|---|
| BA1 headline `K_ii` at q=1/64 (three valid arrangements) | 2.20045e-7 / 2.20551e-7 / 2.21951e-7 | 1/2000000: margins 2.272 / 2.267 / 2.253 |
| `K_ii` ratio τ : τ/100 | 101.030 / 101.261 / 101.897 | draft [100,102.5]: inside; AV1 [99,101]: outside |
| BA1 floor, analytic `(1/32)/(1-q_min)` | 0.0312618 | 1/16: margin **1.99924**; 1/12: 2.666 |
| floor ratio τ : τ/100 with `q_min(tau)` | K: 1.000375; q: exactly 100 | draft [99,101] rejects it |
| disc radius | `28 tau_* (148/7) = 1/64` exactly at `tau_*=1/37888`; `2J G'(R)` = 0.520 there | contraction holds on the closed disc |
| BA2 comparison coefficient of `(5N+1)N^-3`, \|θ\|≤8 | 2.5488e-11 (skeptic), 2.5662e-11 (modern) | 6e-11: margins 2.354 / 2.338 |
| comparison ratio τ : τ/100 | 10033.6 (skeptic), **10101.6** (modern, directed exp) | draft [9900,10100] rejects the modern form |
| BA2 F1 Cauchy, all M > N, coefficient of 1/(N−1) | 1.0195e-10 (F2 with `Phi'`: 5.94e-11) | 2.5e-10: margins 2.452 / 4.21 |
| drafted reverse (triangle) | 1.613e-10/(N−1) | misses the comparison target at every N |
| F2-inner Duhamel (proposed reverse) | 1.4847e-11 `(5N+1)N^-3` | margin 4.04 |
| extra F2 faces `28N(5N+1)` | 616, 1344, 2352 (N=2,3,4) | agrees with the Round32 enumeration |

No result here is a Round33 finding, a loop or a fraction of the continuum problem. The four-dimensional Yang–Mills existence and mass-gap problem remains open.
