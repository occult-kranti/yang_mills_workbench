# BA2 skeptical review (post-comparison)

**Verdict: accepted_within_scope, sub-label `dynamics_on_compact_windows`.** There are **no blocking issues.**

Both routes carry out contract items 1–6 for the zero-selected patterned family at both signs of `|tau|<=10^-8`, with the two named construction families on the same `Lambda_N=[-N,N]^3`, `N` at least 2:
- F1, the AQ1 centered whole-star boxes;
- F2, the I1 §6 all-contained-face boxes with padding.

**What both routes prove:**
1. **The comparison** of the finite-box Heisenberg evolutions on the window `|theta|<=8`, with a rate in `N` at fixed spacing.
2. **The within-family Cauchy estimates** for F1 and F2 over all `M>N`.
3. **Whole-sequence convergence** of both families' dynamics.
4. **The identification** of the F2 limit dynamics with the AQ1 limit `T_theta`, on the whole quasi-local algebra.
5. **The AQ1 §§4–5 rerun** for every subsequential F2 limit state (AY2 row O6).

Every proved constant is at most its frozen target.

**Standing.** I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and both producers.
- My triage proposed this route and the loop-1 previews.
- My loop-2 review corrected the reverse route and wrote most of the frozen control semantics.

This is not human peer review or formal verification. Human project author: Hruday N M (BUNZEEY).

## Headline values

| quantity | forward (inner F1, `Phi`, 2268\|tau\|) | reverse (inner F2, `Phi'`, 1323\|tau\|) | skeptic pre-comparison | target, margin |
|---|---|---|---|---|
| comparison coefficient `K` in `b(N)=K(5N+1)N^-3` | **`3969/155720800000000`** ≈ 2.54879245e-11 | `452554889222515527/30481402343750000000000000000` ≈ 1.48469183e-11 | forward: = (closed form); reverse: closed form `9261/623765200000000`, sharp 1.484691826572e-11 | `6x10^-11`; 2.354 / 4.041 |
| F1 Cauchy `K_F1/(N-1)`, sup over `M>N` | **`9261/155720800000000`** ≈ 5.94718e-11 (faces charged once) | `12128856933354903/118967041015625000000000000` ≈ 1.01951e-10 (whole stars) | both predicted (face-charged closed = forward exactly; star-charged sharp 1.019514e-10) | `2.5x10^-10`; 4.204 / 2.452 |
| F2 Cauchy `K_F2/(N-1)`, sup over `M>N` | **`117747/1245766400000000`** ≈ 9.45177e-11 (F1-inner Duhamel plus the comparison) | `1055961408185869563/30481402343750000000000000000` ≈ 3.46428e-11 (own family, faces charged once) | reverse predicted (3.46428e-11); forward composed exactly of two predicted closed forms, `K_F1 + (11/8)K` | `2.5x10^-10`; 2.645 / 7.217 |
| `tau -> tau/100` ratios | `1953058850/194651` ≈ 10033.644 (all three) | 10019.588 (comparison, F2), 10033.615 (F1) | identical rationals | [9500,10500] |
| extra F2 faces | `28N(5N+1)`: 616, 1344, 2352 | 616, 1344 (counts to N=6) | 616, 1344, 2352, 3640 | enumeration plus all-size argument |

**Which constants the gate binds.**
- **Headline:** the forward route's three constants, with the reverse's as a labelled second route.
- **Sharpest proved value** for each quantity (both routes are valid): comparison `1.48469e-11` (reverse), F1 Cauchy `5.94718e-11` (forward), F2 Cauchy `3.46428e-11` (reverse).

The reasons are given in "Which value to bind".

## Pre-comparison package, replays and isolation

**My pre-comparison package is unchanged.** It was committed at `7daf273` (22:29:25Z), before the reverse (`9f207fe`, 22:34:30Z) and the forward (`302347b`, 22:34:46Z). It contains:
- `ba2-contract-review.md`;
- `ba2-independent-derivation.md`;
- `ba2_check.py` (95 checks, 38 controls, 101 rejected mutations);
- `ba2-independent/results.json`.

Its hashes match `ba2-independent-freeze.json`, and `ba2_check.py` replays byte for byte under normal and `-O` Python.

**Replays and closures** (`ba2-replays.json`):
- Four producer replays (forward and reverse, each under normal and `-O` Python) reproduce `output/` byte for byte:

  | output | sha256 |
  |---|---|
  | forward `results.json` | `4e85123b…5cf9` |
  | reverse `results.json` | `ac9b5cf7…625c` |
- `tools/freeze.py verify` reports `verified` for both producers.
- Both closures hold 33 files and verify file by file.
- Each producer's `check.py` sha256, recorded before evaluation, equals the frozen file.

**Inventories.** Both producers hold exactly the 29 declared inputs (AGENTS.md, the contract and the 27 shared premises), each byte-identical to the repository.
- The reverse inventory contains no skeptic, lens, deliberation, plan or forward file.
- `forward_additional_premises` is empty.

**Reads outside `inputs/`.** Both producers disclose protocol and style reads:
- `tools/README.md`, `freeze.py` and `phrase_scan.py`;
- a Round32 AY1 checker of the same direction.

None of these carries premise weight. The scratch folders `/tmp/claude-0/ba2-forward-private` and `/tmp/claude-0/ba2-reverse-private` match their disclosures by name and mtime; I opened no file in them.

**Timing.** Both producers wrote their final `check.py` and `report.md` between 22:30:52Z and 22:33:32Z. That is *after* my pre-comparison commit.
- Both disclose that they did not read `research/round33/skeptic/`.
- Neither contains a skeptic-only construct, with one exception: the labelled exact (48) suprema, `567|tau|` and `108|tau|`. These appear in my package and in both producers, but in no producer premise. Both producers compute them by pair enumeration in `check.py`.
- Isolation is therefore shown by disclosure, content and computation, not by commit order (finding N6).

## What is proved, with quantifiers

**Model.** `AQ_patterned_zero_selected`:
- SU(2) Kogut–Susskind form on Z³ at fixed spacing, with coarse 24-link factors;
- selected triple exactly `(0,0,0)`, with `h_b=8ΣC_e` unbounded, self-adjoint and with compact resolvent;
- 21 omitted faces per anchor, each `-(tau/3)W_f` (`delta=alpha/8`);
- both signs of `|tau|<=10^-8`; the `-tau` value replays the same `|tau|` formula;
- cover `R={0,e_z}`, observables `A` in `B(H_R)`;
- clock `theta=alpha t/hbar`; `u=theta/8` is used internally only, so `|theta|<=8` means `U=1`.

**Item 1: the Lieb–Robinson bound, quoted and placed.**
- **Quotations.** Both reports quote Theorem 3.1 (51)–(52), with (40), (41), (44), (48)–(50), and Theorem 4.1 (77) from the committed excerpt. My check matches every quoted line against the excerpt:
  - reverse: 18 lines, all verbatim;
  - forward: 17 lines, 15 byte for byte. The other two are headings: the bold markers of "Theorem 3.1." are dropped, and the Theorem 4.1 parenthetical is replaced by "(section title omitted)" (finding N1).
  - Both quote (47) from Part B and label it as machine text.
  - Neither quotes the section title that carries the forbidden phrasing (my reading R9 and D8).
- **Placement.** `H_x=h_x` sits in (44), and `Phi` is bounded. F1 on `Lambda_N` is the native restriction of the whole-star `Phi`, and F2 on unpadded `Lambda_N` is the native restriction of the owner-set `Phi'`. The reverse verifies both identities face by face.
- **Constants.** Both producers state that upper bounds for `C` and `||Phi||_F` may be substituted because the bound is monotone in them (my R3). Neither uses a fine-site metric.

**Item 2: the boundary source.**
- `H^{F2,pad}_N - H^{F1}_N` is the sum of the `28N(5N+1)` extra faces plus the padding on-site terms. The padding terms factor out exactly: both producers give exact Gaussian-rational fixtures, and I give an exact commutator-series fixture.
- **All-size count.** There are two decompositions, and both are correct:
  - forward, per owner-set class: 14 one-direction classes contribute `2N(4N+1)` each, and 7 two-direction classes `4N^2` each;
  - reverse and skeptic, per anchor class: 17/13/5 faces per anchor on the planes, 10/3/1 on the edges, and none at the corner.
- **Owners and distances.** Every owner lies on the outer layer, at l1 distance at least `N-1` from `e_z` and at least `N` from `0`; both minima are attained, and 11 faces reach `N-1`.
- **Enumeration.** Enumerated counts, owner incidences `28N(11N+2)`, minima and the exact distance sums (`S_2=616396498531/82978560000`) are identical in all three computations.
- **Fine units.** Both give fine units descriptively only (my D4).

**Item 3: the Duhamel comparison.** Both producers derive the identity for unbounded generators with a bounded difference through the cocycle `W(s)`, with vector derivatives only. The first order vanishes because the on-site dynamics keeps `A` in `B(H_R)` and no extra face meets R.
- **Forward**, inner F1: `K = (|tau|/3)·Lambda(1)·168` with `Lambda(U) <= 2||Phi||U^2/(1-vU/3)`, so `K = 254016 tau^2/(1-338688|tau|)`. This is my closed form, rational for rational.
- **Reverse**, inner F2: `K' = 148176 tau^2 E_up(592704|tau|)` with `E_up(y)=1+y/3+y^2/(12(1-y/5))`. I re-derived `E_up` from `(j+2)! >= 24·5^(j-2)`.
- **Reconciliation** with my closed form `9261/623765200000000`: sharp enclosure ≤ reverse ≤ closed. The reverse exceeds my exact-exponential enclosure by a relative 6.86e-13, and my closed form exceeds the reverse by 9.78e-7. Both are directed upper bounds of the same integral. They differ only in how the remainder `e^x-1-x` is bounded beyond second order.

**Item 4: the Cauchy estimates, limits, identification and O6.**
- **Forward:**
  - F1 Cauchy with faces charged once (per-site sum `49|tau|/3`, tail `392/(N-1)`), inner F1;
  - F2 Cauchy as one F1-inner Duhamel `F2(M)` against `F1(N)` plus the comparison at `N`, using `max_N (5N+1)(N-1)N^-3 = 11/8`;
  - the F2 distance to the limit by a direct F1-inner Duhamel on `Lambda_M` (`F2(N) ⊂ F1(M)`).
- **Reverse:** each family against its own NS limit, with the larger box inside the integral: F1 with whole stars (`J=28|tau|`), F2 with owner sets and faces charged once.
- **Rates and sources.** All sources are the new terms only, each charged once, with every point at `|y|_inf >= N`. The rates are the honest `1/(N-1)`; both producers give exact polynomial lower witnesses and reject harmonic step sums.
- **Identification.** Both prove it on every local algebra, with `R` replaced by a finite `X` and the distance `N-n` (my R7), and then on the quasi-local algebra.
- **O6.** Both rerun AQ1 §§4–5 with F2's own extraction:
  - stationarity: `|omega(T A)-omega(A)| <= 2 eps_n` (forward) or `<= 2c2/(L-1)` (reverse);
  - GNS strong continuity from normal local densities and uniform approximation;
  - a nonnegative generator by Fourier tests, which uses the finite ground property and not stationarity alone (forward fixture);
  - the gauge and physical-sector restriction.

  States remain subsequential and are not identified.

**Items 5–6.**
- **Meaning.** Both give the same meaning: algebraic dynamics of the named constructions on a compact window, not GNS or correlation equality (BB2), not uniform in time, and not uniform in `a`.
- **Template and gate fields.** The template is quoted once, as one unbroken span on one line. The gate fields are exactly the contract's, with the three true fields true because their targets are admitted.
- **Round tool.** `tools/phrase_scan.py` finds no affirmative hit in either report.
- **Scaling.** Every ratio is inside [9500,10500], and happens also to lie inside the stale [9900,10100] (my D1 did not bite).
- **Controls.** All 35 contract controls are damaging mutations in both checkers: forward 44 checks with 116 rejections, reverse 59 checks with 149 rejections.

## Mutation harness (`ba2_postreview_check.py`, 113 checks)

Unmutated copies of both closures reproduce the frozen `results.json` byte for byte.

- **70 control weakenings (35 per producer).** Each run weakens the validator that one control relies on. Every run aborts with `damaging mutation accepted: <label>` for the intended mutation. So every contract control in both checkers is a live damaging mutation, not a positive-only check.
- **19 must-abort edits.** All of them abort at the intended check:
  - forward: face sum 168→84, Cauchy sum 392→196, time-integral factor 2 dropped, contract byte edit, rehashed target `9x10^-11`, the reverse report as an input, a forbidden sentence, (51) paraphrased in the report, and the template removed;
  - reverse: the `E_up` quadratic term dropped (caught by the reverse's own exponential enclosure), geometry coefficient 84, F2 per-site sum 7, tail coefficient 4, contract byte edit, rehashed target, the triage or the forward report as an input, a forbidden sentence, and (51) paraphrased.
- **5 silent edits.** Each passes its producer checker and is caught only by this review's exact value validator:
  - forward: the retained triangle coefficient `3K_c1`, and the `b(N)` preview shape `5N`;
  - reverse: the labelled sharper value halved, the general-X example at 26 sites, and the triangle over `N`.

## Blocking issues

None.

## Non-blocking findings

- **N1. Forward "byte for byte" wording.** The forward calls its quotation block byte for byte, but two headings differ from the excerpt bytes: markdown bold is dropped, and the Theorem 4.1 parenthetical is replaced to avoid the forbidden phrasing. Every statement sentence and equation is verbatim.
- **N2. Reverse placeholder regex.** The reverse uses the pre-fix pattern `<[^<>]*>`. It gives no false positive on this contract, which contains no `>`, but it would misread inequality text with `>`.
- **N3. Reverse root-N control.** The reverse's first `root_n_misuse` mutation targets a constant-false stub (`divide_by_root`). The other three mutations exercise live validators.
- **N4. Forward F2 Cauchy uses F1's constants.** The forward bounds the F2 Cauchy estimate through the inner F1 evolution (labelled inner F1, whole-star `Phi`). It is valid, and 2.73 times larger than the reverse's own-family value. The contract's "inner family named" rule is met.
- **N5. Stale bracket (D1).** The stale [9900,10100] rejected no producer ratio. The gate should still cite [9500,10500].
- **N6. Timing.** The producers' final files postdate the skeptic pre-comparison commit. Isolation rests on disclosure and content. The shared labelled `567|tau|` and `108|tau|` are computed by both producers in code, and task-prompt channels cannot be audited.
- **N7. Unpinned labelled values.** The producer checkers do not pin every labelled value (the five silent edits). The gate binds the exact rationals from this review.
- **N8. Two remainder bounds.** The reverse's `E_up` and my closed form are two directed remainder bounds. The gate should label the reverse constant as its own formula, not as "the skeptic closed form".
- **N9. The `-tau` evaluations** are replays of one `|tau|` formula.
- **N10. Two readings of `common_limit_claimed`.** Forward W3 and the reverse's §5 gate-field text both read `common_limit_claimed: false` as "no common limit state", with the dynamics identification carried by `dynamics_limit_identified_claimed`. This is my R10.
- **N11. Phrase-scan hits on my own frozen derivation.** Run over my frozen, committed pre-comparison file `ba2-independent-derivation.md`, `research/round33/tools/phrase_scan.py` reports mention-style hits. They come from a checklist item that quotes two forbidden phrases in order to name them as producer errors; that clause has no negation word. The file is not gate text: the recorder scans only the supported statement, the decision and the limitations. It is left unedited because it is frozen. `ba2.md`, `ba2-contract-review.md`, the supported statement and the limitations all scan clean.

## Contract wording defects reconciled

| skeptic | forward | reverse | outcome |
|---|---|---|---|
| D1 stale bracket [9900,10100] in `duhamel_tau_order_quadratic` | W5 | note 5 | all ratios inside both brackets; [9500,10500] governs |
| D2 semantics cover 31 of 35 ids | implemented all 35 from their names | note 1 | both read the four ids as in my BA2-N2 |
| D3 `observable.id` names N to N+1 | not raised | note 3 | both prove the sup over all `M>N` |
| D4 "converted to fine units" against the metric field | W1 | §2.3 (informational) | display only in both |
| D5 no `N_0` or clock field; semantics copied from BA1 | W2 | note 2 | fields that exist are checked |
| D6 notation `b(N)`/`B(N)`, `tau^{F,M}` | W7 | note 4 | read as `T^{F,M}` |
| D7 route vocabulary only in plan.json | not raised | not raised | both name the inner family and interaction; the gate adds routes `duhamel_inner_f1`/`duhamel_inner_f2` |
| D8 section title against the forbidden phrasing | title omitted in the heading | "parenthetical section title is not reproduced" | met |
| — | W4 margin rule; W6 567\|tau\|; W8 (47) only in Part B; W9 new stars' faces may lie inside `Lambda_N` | note 6 `state_provenance`; note 7 canonical embedding of `B(H_{Lambda_N})`; note 8 108\|tau\| | all correct readings |

## The exact (48) supremum (recorded, not used)

Pair enumeration gives these exact suprema in (48):
- whole-star `Phi`: `567|tau|` (pairs at l1 distance 2 in one star, `81·7`), against the admitted `81J=2268|tau|`, a factor of 4;
- owner-set `Phi'`: `108|tau|` (the pair `(b+e_y, b+e_z)`, whose owner set holds 4 faces), against the admitted `1323|tau|`, a factor of 12.25.

All three computations agree. No constant, target or gate value uses these numbers. At leading order the comparison coefficient scales with `||Phi||_F`, so a future contract could tighten every constant by these factors. That would be a new, labelled instance.

## Which value to bind, and why

**Headline: the forward route.**
- `b(N) = K(5N+1)N^-3` with `K=3969/155720800000000`.
- `K_F1 = 9261/155720800000000`.
- `K_F2 = 117747/1245766400000000`.

Reasons:
- It is the contract's designated forward route (inner F1, whole-star `Phi`, route `duhamel_inner_f1`).
- Each constant is a closed rational that equals my independent closed forms exactly (`K_F2` is an exact composition of two of them).
- Its margins are at least 2.35.

**Labelled second route: the reverse's constants** (inner F2, `Phi'`, route `duhamel_inner_f2` for the comparison and F2; inner F1 on `Lambda_M`, route `duhamel_inner_f1`, for F1). They are valid and sharper for the comparison and F2. The minimum of the two routes is a valid bound for each quantity, and the gate may state it as "sharpest proved", with its route named.

**Tier.** Every constant is tier `polynomial_lieb_robinson`. No exponential-tier constant exists.

## Limitations

- **Scope.**
  - Covered: the zero-selected patterned family, the cover R, fixed spacing and `|tau|<=10^-8`, with F1 and F2 on centered cubes, `N` at least 2.
  - Not covered: literal vertex boxes, periodic or orthant boxes, nonzero selected triples, the uniform route-B model, weak coupling and the continuum.
- **Algebraic dynamics only.** It is not equality of GNS dynamics or of correlation functions of different states. There is no common limit state and no state convergence; limit states remain subsequential (BB2).
- **Window.** The constants hold for `|theta|<=8`. The bounds grow like `U^2/(1-vU/3)`, and nothing is uniform in time.
- **Rates.** Every rate is in `N` at fixed spacing: order `N^-2` for the comparison and `1/N` for the Cauchy estimates. There is no exponential decay in `N` and no estimate uniform in the lattice spacing `a`.
- **Upper bounds.** All constants are upper bounds. The admitted norms exceed the exact (48) suprema by factors of 4 and 12.25, and the all-size face sum is 20 to 31 times the enumerated sum.
- **Inherited without re-proof:**
  - NS Theorems 3.1 and 4.1, as transcribed in the committed excerpt;
  - AQ1's `C` and `||Phi||_F` bounds (arithmetic re-verified);
  - AM2's ground state and gap for F2 boxes, and F2 compactness and extraction, via AY1;
  - the I1 dictionary;
  - the Stone, Fourier and tensor-exponential facts.
- **Independence is limited** by the shared contract, selection note and AY2 table, by the timing (N6), and by correlated model agents.
- **Scientific priority is unverified.** The dynamics results are credited to Nachtergaele–Sims, and the O6 strategy to AQ1 (Gauvin, Supplement A.10).

## Advice for BB2 (planning only)

1. Read `K`, `K_F1`, `K_F2` and the second-route constants from the BA2 gate as exact rationals, with their routes. Reject recomputed or smaller values.
2. Equality of GNS dynamics and of correlation functions needs BA2 together with a proved common state. The Lieb–Robinson approximation of `T_theta(W)` needs the state difference on the region it reaches, not only on R.
3. A sharper `||Phi||_F` (567|tau| or 108|tau|) would be a new labelled instance with its own frozen constants. It must not be used under BA2's gate.

**Files.**
- `ba2_postreview_check.py` and `ba2-postreview/results.json`: 113 checks, byte-identical under `-B` and `-B -O`.
- `ba2-replays.json`: assembled by the private helper `/tmp/claude-0/skeptic-ba2-private/make_replays.py`. Every Boolean in it comes from the post-review checker or from `freeze.py verify`.
- `ba2.json`.
