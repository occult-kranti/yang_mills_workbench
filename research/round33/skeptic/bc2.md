# BC2 skeptical review (post-comparison, single producer, route-B uniform model)

**Standing.** I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producer. The frozen BC2 texts carry my 30 pre-freeze edits. This is not human peer review and not formal verification. Human project author: Hruday N M (BUNZEEY).

**Order, as it happened.**
- The contracts froze at e4ffdf5 (04:22:10Z). The producer's input snapshots were written at 04:22:09Z.
- My pre-comparison values were final by 04:58:27Z (`bc2_check.py` last written 04:53:13Z, results sha256 `f6992cae…3c5c`).
- **My pre-comparison package was committed first**, at 5ec599f (05:00:47Z).
- The forward `check.py` was last written at 05:02:17Z, and the **forward commit ee45eed came after**, at 05:04:31Z (3 min 44 s later).
- My exposure was to names only:
  - a `git status` printed the untracked `forward/bc2/check.py` and `report.md`, which I disclosed in the derivation;
  - during the BC1 post-review, after my BC2 package was committed, `git log` printed the ee45eed subject, which states `K_B=13/27941256`.
- I opened `forward/bc2/` only after the coordinator's BC2 post-comparison message.

**Verdict: `accepted_within_scope`.** Sub-label `convergence_of_named_constructions`, secondary `certificate_restated_for_limit`, `reference_unresolved` and `static_not_dynamic`. There are **no blocking issues**.

Every route-B constant equals my frozen pre-comparison rational **exactly**, not only to the printed digits:
- `K_B = 13/27941256`;
- `C_B = 2326328761843649826272217312701707175/2461302090348550272620124432958434944821248`;
- `c_site,B = 35789673259133074250341804810795495/38457845161696098009689444264975546012832`;
- the split closure: `t_0`, `t_W`, `c_1`, `c_2`, `beta*` and `S_lambda`.

Each is recomputed from route-B inputs only. Twenty-two source edits that substitute route-A inputs or gate constants into the producer's `check.py` all abort.

## What the packet proves, with quantifiers

Model `AQ_uniform_routeB`: uniform Kogut–Susskind SU(2) at fixed spacing and strong bare coupling (`g^4=9.6x10^9`). Every face has `nu = alpha tau/24`. Route B groups the interaction into whole stars (21 omitted faces, norm `7|tau|`) and single-factor groups (3 selected faces, support `{b}`), with `J' = 29|tau|`. Both signs `|tau| ≤ 10^-8`; `tau < 0` is the `U_E` mirror, with no real `g`.

The named construction FB is the centred whole-star-plus-single-group boxes `Lambda_N`, `N ≥ 2`, together with the finite complete-factor route-B volumes containing `Lambda_N`. Every bound holds in each `Q_L` uniformly in `L`, then at fixed `N` for the untruncated ground vectors (AV1 F20–F23 with the AX1 route-B gap 1/2); the `N` and `L` limits are never exchanged.

1. **Item 1.** The partition (3000 plaquettes), the per-site inputs (52 faces, 5 groups, `29|tau|`) and the incidence on `R` (7 + 2 groups; 153 / 88 / 16 / 72 faces, 6 of them strictly containing `R`) are all derived from the fine geometry.
   - Admissibility is exact: disc `1073/2734375 ≤ 1/64` and `2552/390625 < 1`; weight `W=1024`: `17168/2734375` and `40832/390625`; `lambda = 1/512 < q`.
   - The route-A extremes give `29/1792 > 1/64` and are rejected by the self-map.
2. **T0** (`analytic_disc`, proved in the packet). At every site `u` of the union volume, `sum_{I∋u} ||c^A_I − c^B_I|| ≤ K_B q^((N−|u|_inf)_+)`, with `K_B = 2T_B(64|tau|) = 13/27941256` (margin 2.1493).
   - The route-B circle bound `T_B(|tau|) = 13/3599632512` is pinned to the AX1 gate `T'`.
   - The piece graph gives order `≥ 1 + d`. It is attained, and single sites cost one order and no distance.
   - The every-site common core holds for c1B, c4B and c5B.
3. **T1/T2** (`iterated_split`, direct comparisons): `C_B q^(N−1)` on `R` (margin 4.2321) and `c_site,B |Y| e^{|Y|/10^8} q^{d_Y}` on every finite complete-factor region `Y ⊂ Lambda_N` (margin 2.1491), at both signs.
4. **T3/T4** (`union_comparison`: one direct c4B comparison of `Lambda_N` with `Lambda_M`, factor 1). `C'_B = C_B` and `c'_site,B = c_site,B` (margins 4.2321 and 2.6864). The limit exists on every finite region, without compactness.
   - **2a.** Exhaustion within the prescription, constant `2c_site,B`.
   - **2b.** The pointwise `U_E` mirror.
   - **3.** Identification with every AQ1-type subsequential state before inheritance of the AX1 route-B list.
   - **4.** Coarse translations with `C_B q^(N−|v|_inf−1)`, and no claim for non-coarse translations.
5. **Node.** The AX2 gate `d` and `R'` are restated for the limit. The admitted calculator returns them exactly, and `e^{-3}/4` lies inside the interval.
6. **Obligations.** Five, equal to the contract's item 6 and to my list.

## Values against the pre-comparison predictions (exact)

| quantity | producer | my frozen pre-comparison | relation |
|---|---|---|---|
| `K_B` | `13/27941256` | `13/27941256` | equal |
| `C_B` | `2326…7175/2461…1248` ≈ 9.45161819414e-7 | same rational | equal |
| `c_site,B` | `3578…5495/3845…2832` ≈ 9.30620868347e-7 | same rational | equal |
| `t_0`, `t_W`, `c_1`, `c_2`, `beta*`, `S_lambda` | `13/1799816256`, `26/3148137`, …, `2169/343` | same | equal |
| `C'_B`, `c'_site,B` (union) | `= C_B`, `= c_site,B` | union values | equal |
| nested `C'_B`, `c'_site,B` (labelled) | `C_B/(1−q)`, `c_site,B/(1−q)` | nested values | equal |
| margins | 2.1493, 4.2321, 2.1491, 4.2321, 2.6864 | same | equal |
| crude tier | `2146/2734375`; ≈ 1.8756e-3, 1.8468e-3 | ≈ 7.848e-4, 1.876e-3 | equal (recomputed exactly) |
| `tau/100` ratios | `39059948/388073` ≈ 100.651; ≈ 100.66145 | same | equal |
| node `d`, `R'` | AX2 gate rationals | same (own calculator run) | equal |
| own labelled radius | ≈ 2.7e-41 below `R'` | ≈ 2.7e-41 below `R'` | consistent (different half-width term, both labelled) |

**Against myself.** My derivation §10 prints the density-constant `tau/100` ratio as "≈ 100.662". The exact ratio is 100.6614518, which is 100.661 to three decimals, as my contract review and results record. This is a rounding slip in my prediction table, and nothing depends on it.

**Why the agreement is exact.** Both codes follow the same frozen formula chain: the contract's route-B inputs, the BB1 reverse covering-chain closure and `T_B`. The agreement therefore checks arithmetic and code. It is not a second method.

## The coordinator's readings

- **R1** (the `(1+t)^2 ≤ 1+10^-8` fixture). The producer uses **`t = T'`**, the per-box anchored bound `T_B(|tau|) = 13/3599632512`: `(1+T')^2 − 1 = 93590445481/12957354221447430144` ≈ 7.223e-9 ≤ 10^-8. With `2T'` it would be ≈ 1.4446e-8, which fails. This is my reading, and the split bound needs no such factor.
- **R2** (the weighted first order). `(49W+3)|tau|/144` is labelled ("`refined_weighted_first_order_(49W+3)/144`" = `50179/6447384576` ≈ 7.7828e-6) and not used. The bound `t_W = 26/3148137` uses `52W|tau|/144`.
- **R7** (interpreter cache).
  - After the producer's replays (normal and `-O`), my own calculator runs (executed from source bytes) and all 94 source-edit runs, no `__pycache__` or `.pyc` exists under `research/round32/forward/ax2/`, under `research/round32/forward/` or in the producer closure.
  - The producer loads the calculator from its `inputs/` snapshot with `sys.dont_write_bytecode = True`.
  - A run **without `-B`** and without `PYTHONDONTWRITEBYTECODE`, on a copy outside the checkout, reproduces the frozen output and writes no cache anywhere in the copy.

## Route-A substitutions into the producer's `check.py` (22 runs, each aborts without output)

| substitution | aborts at |
|---|---|
| per-site sum `28|tau|`; 49 faces; 4 groups | `route-B per-site inputs` |
| every constant evaluated with `(28, 49)`; `K_B` replaced by the BA1 `K=49/111790368` | `K_B formula` |
| contraction coefficient `9856 = 28·352` in `T_B` | `T_B(|tau|) equals the AX1 gate T prime` |
| `G'(R)` rescaled so that `29G'(R) = 9856` | `G(R)<148/7 and G'(R)<352` |
| `C_B` ← a BB1 gate `C` | `ledger sums to C_B` |
| `c_site,B` ← a BB1 gate `c_site`; `c'_site,B` ← BB2 `2/984375` | `tau/100 ratio outside the prefrozen bracket` |
| `C'_B` ← BB2 `4/984375` | `bound exceeds its target` |
| disc radius `1/37888`; split weight `1/(37888|tau|)`; `W = 2600` | the route-B self-map (disc, split weight) |
| single groups dropped from the `R` incidence (the route-A ten faces) | `route-B incidence on R at N=2` |
| `D'` with `28|tau|` or with 49 faces | `route-B D prime recomputed` |
| node slope `49|tau|/4` | `a slope other than 51|tau|/4` |
| selected predicate without `r = 2` | `I1 table row disagrees with the derived class` |
| single groups not kept by route-B volumes | `single-factor group clipped by a route-B volume` |
| route-A rejection list emptied | `damaging mutation accepted: BA1_K_under_route_B` |
| `T'` pin and per-site must removed, 49 faces | `check failed: boundary_counts_at_most_bulk` |

The last row is defence in depth: with both guards removed, the derived per-site face counts of the boxes still expose 49.

## Producer notes W1–W7 against my readings

- **W1.** Clause 2a's "item 1" is the whole-sequence bound (T4), not BC2 item 1. Correct and new; my derivation read it the same way without flagging it.
- **W2** equals my **R5**: the sharp order `N−|u|_inf+1` is not substituted.
- **W3.** T0 holds only in each `Q_L`, and no untruncated coefficients are asserted. Correct, and consistent with my derivation §3.
- **W4** equals my **R4**: the route-A extremes fail only the self-map, by `29/28`.
- **W5** equals my **R6**: with `union_comparison`, T3 carries nothing beyond T1.
- **W6.** The inherited AX1 stationarity under `T_theta` is not a route-B dynamics claim. Correct and new; I adopt it (Limitations).
- **W7.** The factor 2 of `8·2^{diam I}` is absorbed into `lambda = 2/W`. This is the BB1 convention, and my derivation uses it.
- My **D1** (T1 has no form field), **D2** (c1B is a special case of c4B) and **D3** (the inherited parameter control asks for `d_X` and `N_0`) stand, and all are non-blocking.
- My **R3** (the untruncated passage for c5B volumes is gated by AX1 item 2) matches the producer's Theorem S5 (vi).
- My **R8** (the binding margins T0/T2 agree to three digits) matches the producer's limitation 4.

## Producer disclosures, adjudicated

1. **Heredoc report.** The file tool refused the report, so it was written with a shell heredoc. The content is bound by `freeze.json` and verified. Accepted as disclosed, as in BB1 and BC1.
2. **A briefly written stub report.** This was disclosed to the coordinator, not in the frozen packet. It is harmless: the frozen `check.py` validates the frozen report (the template once, the phrase scan, 19 pinned values), and `freeze.json` binds it. I record the disclosure here because the packet does not carry it.
3. **The `tools/` listing** (names only, including the ignored `tools/__pycache__` from 2026-09-24). Harmless.
4. **Parts of the gated BB1 reverse `check.py` read outside `inputs/`** "for conventions". This file is not a declared premise. The method is in the declared BB1 reverse report, and my independently coded constants from the declared premises equal the producer's exactly. Accepted as disclosed; recorded as a provenance note.

## Review against the contract items and acceptance

- **Item 1:** met, by enumeration, and my own enumeration agrees:
  - per-site faces 52;
  - incidence `(7, 2, 153, 88, 16, 72, 6)`;
  - piece graph of `Lambda_3`: 1639 pieces, 343 single sites, minimum slack 0 from the five sites. 324 singles are reached from each site; the 19 unreachable ones have two or more coordinates equal to +3 and meet no star inside the box;
  - selected source faces 654 / 1158 / 1806;
  - flip set 864 / 108 with intersections {1, 3};
  - 8 of 64 translations.
- **Item 2:** met. The complexified map with `29|z|`, termination order 8, the circle bound pinned to `T'`, the piece graph and the common core are all proved in the packet, and no BA1 or BB1 form is cited as admitted.
- **Item 3:** met. The split closure, per-site charging and the normalization channel (ledger parts exact, summing to `C_B`) are shown; direct comparisons only; both signs, each `Q_L`, and the untruncated vectors. The `(1+t)^2` fixture holds with `T'`, and the crude tier is reported and fails.
- **Item 4:** met, with 2a (`2c_site,B`), 2b, identification before inheritance, and item 4 by one direct c5B comparison.
- **Item 5:** met. The calculator replay is exact at `+tau` and at the mirror, `D'` is recomputed, and the own radius is labelled.
- **Item 6:** met, with five rows.
- **Item 7:** met.
  - The fixtures carry their labels.
  - The template appears once as one line.
  - The 18 gate fields are exported exactly, with no `dynamics_level`.
  - The `tau/100` ratios lie in their brackets.
  - All 52 controls run as damaging mutations: 219 rejections.
  - The output is byte-identical under `-B` and `-B -O`.

Every clause of `acceptance.accepted_within_scope` holds.

**Uniqueness wording.** Every clause of the report that mentions uniqueness falls into one of these kinds:
- negated or excluded;
- a field or control identifier;
- the open obligation row;
- the claim-exclusion list;
- the AM2 fixed point, unique in its ball;
- a covering member unique through a site;
- the AX1 finite-volume statement (a simple ground in every finite route-B volume).

No infinite-volume uniqueness is asserted. The round phrase tool finds no hit.

## Replays, closure and isolation (`bc2-replays.json`)

- **Replays.** The forward replays reproduce `output/` byte for byte, normal and `-O` (111 checks, 52 controls, 219 rejections), and `freeze.py verify` reports verified.
- **Closure.** 46 files, verified one by one.
- **Inputs.** 42, equal to the contract-derived list and to the inventory I recorded before production, and byte-identical to the repository.
- **My pre-comparison package** is unchanged and replays byte for byte.
- **Release layout.** `bc2_postreview_check.py` reproduces `bc2-postreview/results.json` byte for byte, normal and `-O`, in a git-archive tree of HEAD plus the new skeptic files.
- **Isolation** rests on disclosure and content.
  - My untracked files were in the shared checkout while the forward produced.
  - The forward discloses no read of `research/round33/skeptic/`, and its inventory check forbids `skeptic/bc`.
  - Its enumerations (the 3000-plaquette partition, `Lambda_3` with 1639 pieces), its own-radius term and its choice of assembly differ from mine.

## Mutation harness (`bc2_postreview_check.py`: 21 checks, 94 source-edit runs, byte-identical under `-B` and `-B -O`)

- **52 validator weakenings**, one per control, on temporary copies. Each aborts naming a mutation of that control, except the disc self-map, which is double-guarded and is exposed one check earlier, at `weights_declared_and_admissible`.
- **22 route-A substitutions**, as in the table above.
- **12 other must-abort edits:**
  - the lattice-sum shell, the `(1+q)` factor, the near term 2 and a union factor 2;
  - the AX2 datum perturbed;
  - edited calculator, AX1 gate and contract snapshots, and an undeclared skeptic file;
  - a forbidden phrase, an altered template and an altered pinned ledger value in the report.
- **6 silent edits.**
  - One harmless: a 30-term `e^{1/8}` enclosure, accepted by my validator.
  - Five damaging, run silently by the producer and rejected by my validator: the example exponent `N`, a translation row with exponent 3, the labelled own radius with slope `49|tau|/4`, a changed `K_B` margin in the verdict table, and a changed `C_B` digit at one of its two report sites.
- **16 damaged results packets** are rejected by my validator.
- **Unmutated copies.** One reproduces the frozen output; one run without `-B` reproduces it and writes no cache.

## Blocking issues

None.

## Non-blocking findings

1. The producer checker does not pin the report's margins or example rows, pins each exact value only somewhere in the report, and does not validate the exported example and translation rows or the lower side of its labelled own radius. The five silent edits above are caught only by my validator.
2. The disc self-map guard is shared by the pre-constant check and the control, so a weakened self-map is exposed one check early. Not a defect.
3. `uniform_wilson_claim: true` is a results field outside the contract's gate fields. It carries the AX1/AX2 scope string ("no uniform Wilson-mean sign certificate") and is not a gate field.
4. The node record's `interval` is the calculator's actual interval `[d−r, d+r]` with `r ≤ R'`. The restated statement uses `R'`.
5. `static_not_dynamic` is read as covering state statements and the inherited Euclidean node, with no route-B real-time dynamics or correlation-function statement.
6. The stub-report disclosure is not in the frozen packet; this review records it.
7. The producer read parts of the gated BB1 reverse `check.py` outside its inputs for conventions (disclosed; nothing depends on it).
8. My own rounding slip (100.662 for 100.6615) in the derivation's prediction table.

## Contract defects

- W1 (clause 2a "item 1").
- W3 (T0 per cutoff space).
- W6 (the inherited stationarity).
- W7 (the factor 2 in `lambda`).
- W2 = R5, W4 = R4, W5 = R6.
- D1 (T1 has no form field).
- D2 (c1B ⊂ c4B).
- D3 (the inherited parameter control).

None is blocking.

## Which values the gate binds

- **T0:** `K_B = 13/27941256` (`analytic_disc`, `rho = 64|tau|`).
- **T1/T2:** `C_B` and `c_site,B` as above (`iterated_split`, `W = 1024`), at `q = 1/64`.
- **T3/T4:** `C'_B = C_B` and `c'_site,B = c_site,B` (`union_comparison`, factor 1).
- **Items:** exhaustion `2c_site,B`; translations `C_B q^(N−|v|_inf−1)` for `N ≥ |v|_inf + 2`.
- **Node:** the AX2 `d` and `R'`.
- **Labelled only:**
  - the nested values;
  - the union-volume `2C_B`;
  - the telescoped `K`;
  - the weighted first order;
  - the crude tier;
  - the own radii.

## Limitations

- **Scope.** The uniform route-B model at fixed spacing and strong bare coupling, the named construction and route-B volumes containing `Lambda_N`, finite complete-factor regions, coarse translations and the node `s = 1`. It is one family: there is no common limit, no transfer to the zero-selected family, no other boundary prescription, no weak coupling or continuum, and nothing uniform in the lattice spacing `a`.
- **No uniqueness of any ground state.** No route-B dynamics or correlation-function statement. No finite-box node convergence and no interaction shift of `C(s)`.
- **Upper bounds only.** The thin margins are T0 and T2.
- **Admission basis.** Admission rests on the single forward producer plus my pre-comparison replay, all correlated agents. Scientific priority is unverified.

## Advice (planning only)

- For a single+skeptic loop, freeze an exact-value pin list for every exported number, including the examples, the translation rows and labelled cross-checks with a lower bracket, so that the silent edits above abort in the producer's own checker.
- A route-B BA2 (`||Phi'||_F ≤ 2349|tau|`) and a route-B boundary-prescription comparison are the natural next rows, as recorded.
