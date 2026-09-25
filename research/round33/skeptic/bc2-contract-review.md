# BC2 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/bc2.json` (sha256 `28abe377…6b98a`, frozen 2026-09-25T04:21:44Z) before reading anything of the BC2 producer. I am a model-agent skeptic with correlated ancestry. This is not human review. My pre-freeze review wrote the 17 blocking and 13 non-blocking BC2 edits that the frozen text carries, so this review also checks my own wording. BC2 is single+skeptic, so my replay is an admission input. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written. Nothing blocks production.** `bc2_check.py` establishes the following:
- 110 checks pass, byte-identical under `-B`, `-B -O` and plain `python3`, with no cache written. The admitted AX2 calculator is executed from its hash-pinned source bytes, never imported.
- Every frozen target is a well-posed exact-rational upper bound, and every route-B constant is computable from route-B inputs and declared premises.
- All 52 controls execute as damaging mutations: 138 mutations, each rejected for the expected reason, plus 5 positive cases accepted.
- 11 source-edit mutations of the program all abort (§5). They include every silent route-A substitution: 49 faces, `28|tau|`, 4 groups, `G'(R)` rescaled to 9856.

Four readings will matter at the post-comparison:
- **R1:** the region-factor fixture holds with the per-box anchored bound `T'` only.
- **R3:** the untruncated passage for c5B is gated for route B, unlike BB1's F2 volumes.
- **R4:** the route-A extremes pass the route-B contraction test and fail only the self-map.
- **R7:** the calculator replay must not write a cache under `research/round32/`.

## 1. Frozen bytes against the pre-freeze edits; producer inputs

**Edits.** All 30 BC2 replacement texts of `bc-contract-review.json` are in the frozen bytes verbatim (17 blocking, 13 non-blocking; the appended premise and control id are present; check `prefreeze_edits_verbatim_in_frozen_bytes`). The plan-level edits are recorded in `plan.json` as committed with the freeze (sha256 `f69d4503…b264`); the program uses a recorded copy of the vocabulary.

**Producer inputs.** I ran `find` on `forward/bc2/inputs/` (names only) and hashed each file against the repository.
- The folder holds 42 files: `AGENTS.md`, the contract and its 40 shared premises, including `research/round32/forward/ax2/calculator.py` (sha256 `f368a3e7…1f5d`, the value the AX2 gate binds).
- Every file is byte-identical to its source, and the inventory equals the contract-derived list.
- No `experts/` file (in particular not `bc2-targets-proposal.md`), plan, panel update, deliberation or skeptic contract review is among them.

## 2. Executability, item by item

1. **Item 1 (incidence and admissibility).** Every count holds by enumeration: every plaquette lies in exactly one group; 7 stars and 2 single groups meet `R`; 153 faces charged, 88 meeting `R`, 16 inside `R`, 72 straddling (6 of them strictly containing `R`); 52 first-order faces and 5 groups per site; support-one groups. Both proof weights and the route-A rejections are exact rationals (derivation §2).
2. **Item 2 (coefficient input).** `T_B(rho) = (52 rho/144)/(1 − 29·352 rho)` reproduces the AX1 gate `T' = 13/3599632512` at `rho = |tau|`, and `K_B = 2T_B(64|tau|) = 13/27941256`. The route-B common core and the order-versus-distance count are enumerated (derivation §3).
3. **Item 3 (marginal locality, iterated split).** Executable with the BB1-reverse covering-chain route re-instantiated with route-B inputs. The same formula with route-A inputs reproduces both BB1 gate `iterated_split` rationals exactly, which anchors my implementation (check `route_a_gate_values_parsed`).
4. **Item 4 (whole sequence; 2a, 2b, 3, 4).** Executable. The exhaustion bound is explicit in the frozen text. The sign-mirror premise is present (AX1 F19–F20 and gate item 7). The identification needs only the region form at a proved constant.
5. **Item 5 (node).** The calculator, run from its pinned bytes at its fixed design, returns the AX2 gate `d` and `R'` exactly, and the interval is exactly `[d − R', d + R']`. My own re-evaluation (labelled) gives `r` about `2.7e-41` below `R'`.
6. **Item 6 (obligations)** and **item 7 (fixtures, template, gate fields, scaling, controls):** executable; 16 exact fixtures are exhibited in my checker.

## 3. Readings and residual defects (numbered)

1. **R1. The region-factor fixture.** "(1+t)^2 <= 1+10^-8 re-checked with the route-B anchored bound" holds only with the **per-box** bound `T' = 13/3599632512`: `(1+T')^2 − 1 ≈ 7.2230e-9`, margin about 1.38. With the comparison majorant `t_0 = 2T'` it fails (`≈ 1.4446e-8`). So `t` must be read as `T'`. The iterated split has `eta = 0` and needs no such factor. A route whose per-site factor carries `e^{2 t_0}` could not use the frozen `e^{|Y|/10^8}`.
2. **R2. The weighted first order.** Selected faces have owner set `{b}` of diameter 0, so the weighted first order is `(49W + 3)|tau|/144`. The contract-form `52W|tau|/144` is a valid upper bound; the smaller form is a labelled refinement (`t_W` about `7.78e-6` instead of `8.26e-6`), not the bound value.
3. **R3. The untruncated passage for c5B is gated.** AX1 gate item (2) gives a simple finite-volume ground and gap `1/2` in **every** finite complete-factor route-B volume. So AV1 F20–F23 apply to general route-B volumes directly. BB1 needed a reviewed local reading for non-centred F2 volumes (BB1 R10); route B does not.
4. **R4. The route-A extremes.** The disc radius `1/37888` and the split weight `1/(37888|tau|)` give the route-B self-map value `29/1792 > 1/64` but the contraction value `319/1184 < 1`. Only the self-map test rejects them, as the frozen semantics require. My validator tests admissibility before the frozen-value test, so both extremes are rejected as inadmissible under `J'`, not merely as "not frozen".
5. **R5. The order-versus-distance count** is attained (minimum slack 0 on `Lambda_2`, 509 pieces including 125 single-site pieces). Single-site pieces add order but no distance, so they never lower the vanishing order. The frozen exponent `(N − |u|_inf)_+` is the contract form. The sharp count would give one more order, but that is labelled only.
6. **R6. T3 and T4 are consequences.** `C'_B = C_B/(1−q)` nested, or `C_B` for one direct c4B comparison. T3's target equals T1's, so a telescoped T3 needs `C_B ≤ (63/64)/250000`. The margin is ample either way (4.17 nested). T4 at `1/400000` leaves room for `64/63` (margin 2.644).
7. **R7. Calculator replay hygiene.** Importing `research/round32/forward/ax2/calculator.py` without `-B` would write `research/round32/forward/ax2/__pycache__/`, a change inside a Round32 directory. The replay must run under `-B` or execute the source bytes. I checked that no such cache exists after my runs. The gate should check it after the producer's.
8. **D1 (residual, non-blocking). T1 has no `form` field.** `rate_constant_pair.R_form_T1` carries `q`, target, tier and route but no form. The R form is implied by required item 3 and the T0/T2 forms (`||rho^{box1}_R − rho^{box2}_R||_1 ≤ C_B q^(N−1)`, `N` the smaller size).
9. **D2 (residual, non-blocking). c1B is a special case of c4B.** The redundancy is harmless.
10. **D3 (residual, non-blocking). Inherited `parameters_declare_metric_weights_window`** (BA2 text) asks for `d_X` and `N_0`. BC2's `metric` names the diameters (star 1, single group 0) and `N_min` is 2. I read the control as satisfied.
11. **R8. The binding margins** are T0 (`K_B`, 2.1493) and T2 (`c_site,B`, 2.1491). They agree to three digits, because `c_site,B = K_B(2 + beta* S_lambda)` and the far term is about `1.04e-4` of the near term. The route-B input is about 6.1% above route A's `K`: `52/49` from the first order, times about 1.0002 from the larger contraction constant `29·352·64|tau|`.

## 4. Control mirror

- `controls` equals `preregistration.controls_required.ids`: 52 = 52, same order, no duplicates.
- 27 ids carry BC2 semantics; the other 25 are defined in the frozen BA1, BA2, BB1 or BB2 contracts, which are declared premises. For the route-specific inherited ids, BC2's own texts override (check `control_semantics_coverage`).
- The program implements all 52 as damaging mutations: 138 mutations, 5 positives.
  - `route_b_constants_not_route_a` is decided by a hard pin: every evaluation of `T_B(|tau|)` re-checks equality with the AX1 gate `T'`, so source edits to 49 faces, `28|tau|` or `G'(R)` abort.
  - The fixture controls are decided against exact finite fixtures.
  - `node_values_unchanged` is decided against the calculator's own output.
- Deferred parts are scope notes only: the inventory is recorded; the phrase scan mirrors the tool; tampering is packet level; the disc lemma's analytic steps (Weierstrass, maximum principle) are restated in the derivation, not machine-checked.

## 5. Targets, values and margins (exact rationals in `bc2-independent/results.json`)

| constant | value (both signs, c1B, c4B, c5B) | target | margin |
|---|---|---|---|
| `K_B` (T0; analytic_disc) | `13/27941256` ≈ 4.65261834e-7 | 1/1000000 | **2.1493** |
| `C_B` (T1; iterated_split) | ≈ 9.45161819e-7 | 1/250000 | 4.2321 |
| `c_site,B` (T2; iterated_split) | ≈ 9.30620868e-7 | 1/500000 | **2.1491** |
| `C'_B` nested / union (T3) | ≈ 9.60164388e-7 / 9.45161819e-7 | 1/250000 | 4.1660 / 4.2321 |
| `c'_site,B` nested / union (T4) | ≈ 9.45392628e-7 / 9.30620868e-7 | 1/400000 | 2.6444 / 2.6864 |
| exhaustion `c_site,B + c'_site,B` | ≈ 1.87601e-6 (nested), 1.86124e-6 (union) | none | — |
| crude tier `K_B` / `C_B` | ≈ 7.848e-4 / 1.876e-3 | reported only | fails, retained |

All `tau → tau/100` ratios lie in `[95,105]`: `K_B` is exactly `39059948/388073` ≈ 100.651, the density constants are ≈ 100.661, and the node-radius replay is ≈ 100.0015 (recorded). `q` and `rho/|tau|` are exactly 1 (frozen), and the node datum ratio is exactly 1.

**Source-edit mutations** (scratch copies; each aborts for its intended reason): faces 52 → 49; `J'` 29 → 28; groups 5 → 4; `W` = 64; the disc at the route-A extreme; `G'(R)` rescaled to `9856/29`; the lattice sum without its `24r^2` shell; the near-term constant 2 → 1; `C_B` without the `(1+q)` of `e_z`; the calculator hash changed; the selected predicate losing `r = 2`.
