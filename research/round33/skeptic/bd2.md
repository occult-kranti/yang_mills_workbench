# BD2 skeptical review (post-comparison, single producer: two-plaquette graph, Z³ 1×2 loop, electric band, 2+1D recount)

**Standing.** I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producer. The frozen BD2 contract carries the pre-freeze review written by another session of this role. This is not human peer review and not formal verification. Human project author: Hruday N M (BUNZEEY).

**Producer.** Forward only (`HNM-BD2-F`), packet `research/round33/forward/bd2/`, commit 37fa623. BD2 is single+skeptic: admission rests on this packet and on my replay from the contract alone.

**Order, as it happened (UTC, from git).**
- The BD contracts froze at 9ae1160 (05:09:18Z). The producer's input snapshots were written at 05:09:10Z.
- My BD2 values: the prototype certificate was ready at 05:35:30Z (scratch `graph_cert.py`). The inventory of the producer's `inputs/` was recorded at 05:37:45Z, by `find` and sha256 of names only.
- My checker run at 05:55:31Z (scratch `run2O`) produced every block of the committed `bd2-independent/results.json` unchanged. `bd2_check.py` was last written at 05:58:22Z.
- **BD1 reverse** a1010a4 05:53:54Z, **BD1 forward** 5a792b0 05:54:17Z, **BD2 forward** 37fa623 06:00:06Z. The producer's checkout file times: `check.py` 05:48:29Z, `report.md` 05:52:50Z, `freeze.json` 05:54:56Z.
- **My pre-comparison packages were committed last**, at bf1f531 (06:10:08Z), 10 min 2 s after the BD2 forward commit.
- Exposure before bf1f531:
  - the names and hashes of the 35 input files;
  - possibly the one-line git subject of 37fa623, in any `git log` output after 06:00:06Z.

  Both came after my values were final. I opened `forward/bd2/` only after the coordinator's post-comparison message.

**Verdict: `accepted_within_scope`.**
- Sub-label: `sign_certified_finite_graph`. Secondary sub-labels: `transfer_to_named_model`, `obstruction_recorded` and `static_not_dynamic`.
- **No blocking issues.**
- Every exported value equals, or certifiably contains, my own value.
- I re-evaluated the producer's angle lemma with my own basis and Ritz vectors. It reproduces every exported angle and residual to 8 digits.

## What the packet proves, with quantifiers

1. **Graph tables (item 1).** On the Round11 two-square patch, `H_FG(l1,l2) = K − l1 W_1 − l2 W_2`: gauge-invariant sector, `K` the sum of the seven link Casimirs at rho=1, alpha units. The coefficients through total order 4 are identical at `D = 6` and `D = 8`, with truncation error 0:
   - `<W_1> = l1/6 − 5 l1³/864 + l1 l2²/4212 + …`;
   - `<z> = 7 l1 l2/216 − 349 (l1³ l2 + l1 l2³)/303264 + …`;
   - `<C_shared> = (l1² + l2²)/48 − 5(l1⁴ + l2⁴)/4608 − 49 l1² l2²/438048 + …`;
   - `E_0 = −(l1² + l2²)/12 + 5(l1⁴ + l2⁴)/3456 − l1² l2²/8424 + …`.

   At `l1 = l2` the second-order coefficients are `7/216` for `<z>` and `1/24` for `<C_shared>`.
2. **Enclosures (item 2).** At `l1 = l2 = ±1/10, ±1/100, ±1/1000`, every `<z>` enclosure is positive at both cutoffs.
   - The worst `D = 8` relative width is `1.79645e-17` (margin 5.57 against `1/10^16`).
   - Each record carries the five-part ledger.
3. **Z³ 1×2 loop (item 3).**
   - The loop is the rectangle of the omitted xz faces at 0 and `e_x`. Its six links are owned by `R = {0, e_z}`.
   - The first-order coefficient is 0 in every box.
   - `|omega(W_{1x2})| ≤ K_2' tau²` (≈ 1.34175e-12 at the cap) for every F1 and F2 box and for the limit, at both signs.
   - It is even in tau in every F1 box and for the limit.
   - The formal `7/124416` is labelled `formal_second_order_coefficient`.
4. **Electric band (item 4).** `(3/2)L² ≤ omega(h_R) ≤ 98|tau|`, i.e. `[2.87586637818e-19, 9.8e-7]`. This holds for every F1 and F2 box (untruncated, at fixed N) and for the limit, at both signs.
5. **2+1D recount (item 5).**
   - Counting: `p = 3`, `J = |tau|`, three faces per site, termination order 6.
   - Constants at `R = 1/64`: `G_3(R) = 9e^{3/32}` and `G_3'(R) = 118e^{3/32}`, with a directed enclosure. The directed cap is `1580747155173/10^15`.
   - No 2+1D theorem is claimed.
6. **Items 6–7.**
   - Five obligation rows and the Einstein–QED no-transfer row.
   - The template appears once.
   - The gate fields equal the frozen dict.
   - All 21 controls reject damaging mutations.

## Adjudication of the coordinator's points

**1. Graph tables and flip parities.** I compared every producer entry with `m + n ≤ 4` (`E_0` to 5), zeros included: 15 + 15 + 15 + 21 entries. Each equals my table exactly. Every nonzero entry has the right parity:
- `<W_1>` has (odd, even) exponents, from the flip of `h1` (face 1, non-shared) for `l1` and of `h2` (face 2, non-shared) for `l2`;
- `<z>` has (odd, odd) exponents;
- `<C_shared>` and `E_0` have (even, even) exponents.

The producer's `W_2` table and its `l1 = l2` second orders (7/216 and 1/24) equal mine. The vM flip alone would give only the `l1 = l2` statement, and the producer's validator rejects that reading.

**2. `<z>` enclosures and the Eckart/angle lemma.** The producer's lemma is the admitted AZ2 certificate code, copied verbatim. It is valid:
- Weyl: `E_1 ≥ 3 − 2|l|`, since `||W_1 + W_2|| ≤ 2`.
- Temple: `E_0 ≥ mu − rho²/(b − mu)`.
- The Round11 comparison `H ≥ B ⊕ R·Q_D` holds for `R < tau_t`, by the Schur-complement inequality. Here:
  - `B = A − CC*/(tau_t − R)` and `C = P V Q`;
  - `tau_t = 45` or `69`, minus `2|l|`;
  - `R = b`.

  Then Temple on `B` applies, with `lambda_1(B) ≥ b − 4l²/(tau_t − R)` by interlacing and `||C|| ≤ 2|l|`. Since `E_0 ≤ mu < R`, `E_0 ≥ lambda_0(B)`.
- Eckart: `sin²θ ≤ (mu − E0_low)/(b − mu)`.
- Davis–Kahan: `sin θ ≤ rho/(b − mu)`.
- Observable step: `2sσ + 2s²||z||` with `||z|| = 1`.

I evaluated this lemma with my own orthogonal spin-network basis and my own Ritz vectors. At every point it reproduces, to 8 digits:
- `sin θ` (Eckart): 1.4544249e-21 at `D = 8`, `|l| = 1/10`;
- `sin θ` (Davis–Kahan): 7.0590303e-21;
- `rho²` and `rho_Q²`: 3.9113163e-40;
- the relative widths (1.79645e-17 at `D = 8`, 7.02377e-12 at `D = 6`).

Other agreements:
- The Schur-complement bound beats Temple at every point.
- The per-link thresholds (96 and 69 at `D = 8`; 123/2 and 45 at `D = 6`), the product threshold 145/2 and the ledger items equal mine.
- The ledger items are the per-link classes, the product channel, the corners and the `2XY` interference.

My own tail-comparison certificate is a different, sharper lemma, with worst width 3.56e-18 (margin 28.09). Its enclosures lie inside the producer's at all twelve points. The certified intervals are therefore consistent. Davis–Kahan alone would give 8.72e-17, still below the target. So the target is met by any of the three certificates.

**3. The Z³ 1×2 loop.**
- **The rectangle is the frozen one.** Its links are `(0,x)`, `(e_x,x)`, `(2e_x,z)`, `(e_x+e_z,x)`, `(e_z,x)` and `(0,z)`, all owned by R. It meets E_3 six times, so it has area 2.
- **Face counts.** My enumeration gives 82 omitted faces meeting R, 10 inside R, 16 containing R and 49 per site. That leaves 33 at one site without the other, and 72 straddling. These equal the producer's pins.
- **First order.** `E[W_{1x2} W_f] = 0` for every face `f`, by single occurrence, so the first-order coefficient is 0.
- **`K_2'`.** Recomputed from the five AY1 items with these counts, it equals the AY1 gate rational, item by item.
- **The bound** `K_2' tau²` is stated for F1, F2 and the limit at both signs.
- **Evenness** (AW1 flip lemma, `kappa = 0`) is stated for F1 boxes and the limit only. `F2_boxes_claimed: false`, and "evenness gives no remainder bound".
- **The formal coefficient.** `7/124416 = (7/216)/24²` is labelled `formal_second_order_coefficient`. It carries no sign, no certified value and no remainder, and the bound is not read as its enclosure.

**4. The electric band.**
- **Lower end.** `h_R ≥ 6 Q_R`, from the free Casimir gap 6δ. The pure-reference Fuchs–van de Graaf inequality, proved inline with exact qubit fixtures, gives `omega(h_R) ≥ 6(L/2)² = (3/2)L²`. The same rational `L` serves both cases:
  - the limit uses the AY2 gate lower end, identified by BB2 items 2–3;
  - every box uses the per-box ball of AY1 forward F11–F14, passed to the untruncated vector by AV1 F22.

  I recomputed `L` as `sqrt10_lo |tau|/72 − K_2' tau²`.
- **Upper end.** `2·7·7|tau| = 98|tau| = 49/50000000`, from the AQ1 reset with the 7 incident anchors (F2: AY1 gate item 1). It passes to the limit by lower semicontinuity of the monotone cutoff limit, and only in that direction; the producer's fixture shows why. The lower end is proved at the limit directly.
- **Premises.** The frozen premises are pinned by hash.
- **Per-link counts.** My count of `n_e` on the 48 links of R is `{2: 4, 3: 16, 4: 28}`, total 168. It equals the producer's per-link rows, giving the formal `7/144 tau²`.

**5. The 2+1D recount.**
- Numerators `L_k(3) = 8·6^k(1 + 4k/3)`: 8, 112, 1056, 8640, 65664, 476928, 3359232.
- `G_3 = 8e^{6t}(1+8t)` and `G_3' = 8e^{6t}(14+48t)`.
- At `R = 1/64`: `9e^{3/32} ≈ 9.8846` and `118e^{3/32} ≈ 129.598`.
- The producer's directed `e^{3/32}` bracket (25 terms plus a geometric tail, outward to `10^-40`) contains my 40-term bracket.
- The self-map binds. The cap is `1/(576 e^{3/32}) ≈ 1.58074715517e-3`, and the directed lower `1580747155173/10^15` lies below it. The exclusion condition `2J G_3'(R) < 1` alone would allow `1/(236 e^{3/32}) ≈ 3.858e-3`.
- No finite-volume theorem, AQ chain, node or dictionary is claimed in 2+1D.

**6. The producer's wording defects W1–W7.** All seven are correct and non-blocking.
- **W1.** The single model id names the graph only; every value carries its own model label.
- **W2.** The zero triple belongs to the Z³ family.
- **W3 (new).** A uniform fourth-order remainder presupposes evenness, which is admitted for F1 and the limit only. F2 would need a third-order remainder.
- **W4.** "Three faces per site" means the faces whose owner set contains the site. This equals my count.
- **W5.** `J = |tau|` is linear. What is tau-independent is `J/|tau| = 1`, the G's, the counts and the cap.
- **W6.** Labelling only: AY1 tier (ii) is the BD2 tier name `exact_first_order` for `K_2'`.
- **W7.** The sign restriction of the Round11 API is irrelevant to the exact certificates.

My contract-review readings are met. R3 (the Eckart item) is met: the producer's ledger part (d) carries both an Eckart and a Davis–Kahan angle. D1 (two scopes for the 1×2 loop) and D2 (nesting observed, not targeted) are respected.

**7. Code provenance.**
- `check.py` imports only the standard library: argparse, decimal, fractions, functools, hashlib, json, math, pathlib, re.
- The AZ2 forward algebra is copied verbatim with attribution. It is compared block by block with the pinned snapshot (63 blocks, none differing). The copied code reproduces the AZ2 gate enclosure of `<W_1>` exactly; that guard also catches a dropped tail comparison (below).
- The Round11 solver `two_plaquette.py` is read as bytes from its snapshot, to bind 13 exact source strings (the list the AZ2 checker uses). It is never imported or executed. The producer agent reports that it did not open the file. I hashed it only, and this review does not open it.
- No `__pycache__` or `.pyc` exists under `research/round11/`, `research/round32/` or the producer closure after all runs.

## Replays and mutation harness

- `freeze.py verify` reports `verified`. The closure verifies file by file (39 files). The 35 inputs equal the contract-derived list and my names-only record, and are byte-identical to the repository.
- The producer reproduces `output/` byte for byte under `-B` and `-B -O`: `4e6aa253…fcacd`, 41 checks, 107 rejected mutations.
- My pre-comparison package is unchanged and replays byte for byte: 64 checks, 21 controls, 85 mutations, 4 positives.
- `bd2_postreview_check.py`: 22 checks, byte-identical under `-B` and `-B -O`, also in a `git archive` tree of HEAD d95db8c plus the new files.
  - It runs 38 source-edit runs:
    - 2 unmutated or without-`-B` runs;
    - 21 validator weakenings, each aborting with a labelled mutation of its control. For exact arithmetic, `rat` is also removed from the verbatim-copy list, which would otherwise expose the edit one check earlier;
    - 12 must-abort edits, each caught by the producer: the Weyl gap 4; the Temple-only Eckart angle, caught once by the copy binding and, with the binding removed, by `z_certificates_complete`; the 56|tau| budget; Fuchs–van de Graaf without 1/2; the 2+1D exponent with p=4; the `K_2'` item `rho` in place of `2 rho`; the AY1 gate, contract and undeclared-input edits; report edits;
    - 3 silent edits: 1 harmless, and 2 export-only edits caught only by my validator.
  - 19 damaged packets are rejected by my validator for the expected reasons.

## Blocking issues

None.

## Non-blocking findings

- **N1.** Two exported fields are not self-validated: the interacting tail threshold and the recorded exclusion condition. Silent edits to them are caught only by the skeptic validator.
- **N2.** "Not opened" for `two_plaquette.py` describes the producer agent. Its checker reads the snapshot bytes to bind 13 strings, as text only.
- **N3.** The producer's angle is about 5 times looser than my tail-comparison certificate. Both certify the sign, and both meet the frozen width.
- **N4.** The `−l` certificates are computed separately and equal the `+l` ones exactly. The `D = 8` enclosures lie inside the `D = 6` ones (observed; not a target).
- **N5.** The gate must keep the two scopes of the 1×2 loop separate. The bound covers F1, F2 and the limit; evenness covers F1 and the limit only.

## Contract defects (non-blocking)

- W1–W7 as adjudicated above.
- My contract-review D1 (the two scopes) and D2 (nesting not a target) stand.
- R3 is resolved: the itemized ledger does carry an Eckart angle.

## Binding, limitations and advice

`bd2.json` binds by sha256 the producer closure and `freeze.json`, the contract, the selection note, every declared premise, and my pre- and post-comparison files. The supported statement quotes the mandatory template once as one unbroken span. The phrase tool passes it and the limitations with the BD2 contract.

**Advice for the gate.**
- Keep `graph_sign_certified` scoped to the graph grid.
- Keep `z3_1x2_formal_only`. The bound gives no sign.
- Record the band as two-sided but loose (ratio ≈ 3.4e12).
- State the 2+1D constants as a recount, not a theorem.
- The obligations are the next steps, each with its own contract:
  - a certified 1×2 sign, which needs a uniform fourth-order remainder (and a third-order one for F2);
  - a tight band, which needs a second-order upper bound for the unbounded `h_R`;
  - an area law, which needs a zero-free region;
  - the 2+1D finite-volume theorem.
