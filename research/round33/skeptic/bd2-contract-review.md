# BD2 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/bd2.json` (sha256 `783cad80…46f41e`, frozen 2026-09-25T05:09:10Z) before reading anything of the BD2 producer. I am a model-agent skeptic with correlated ancestry. This is not human review. The pre-freeze review (`bd-contract-review.md`/`.json`) was written by another session of this role, whose `<z>` preview reused a scratch copy of the AZ2 checker. I read its blocking edits and determinations, not its advisor-only previews, and I reused none of its code. BD2 is single+skeptic, so my replay is an admission input. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written. Nothing blocks production.** `bd2_check.py` establishes the following:
- 64 checks pass, byte-identical under `-B`, `-B -O` and plain `python3`, with no cache written. The AZ2 checker and the Round11 solver are hashed, never opened or run.
- The two-plaquette algebra is rebuilt in a monic spin-network basis. It reproduces every AZ2 anchor at `l1 = l2`.
- The frozen D=8 width target is met at every grid point with margin **28.09**. The maximal relative width is 3.5602e-18.
- All 21 controls execute as damaging mutations: 85 mutations, each rejected for the expected reason, plus 4 positive cases accepted.
- 14 source-edit mutations of the program all abort (§5).

Four readings will matter at the post-comparison:
- **R1:** the frozen `1/10^16` discriminates between certificate types.
  - a tail-comparison angle gives 3.56e-18 (margin 28);
  - an AZ2-type Eckart angle is expected near 1.8e-17 (margin ≈ 5.6);
  - a bare Davis–Kahan angle with the full residual gives 8.72e-17 (margin 1.15).
- **R2:** two different one-link flips are needed: h1 for `l1`, h2 for `l2`. The vM flip only gives the `l1 = l2` statement.
- **R3:** the formal Z³ 1×2 coefficient is `7/124416` by two routes: Z³ Rayleigh–Schrödinger, and the graph `7/216` under `τ_FG = τ/24`.
- **R4:** the band's lower end is the same rational `(3/2)L²` for every box and for the limit, but its premise differs. Boxes rest on AY1 forward F11–F14, a reviewed step. The limit rests on AY2 gate item (2) with BB2.

## 1. Frozen bytes against the pre-freeze edits; producer inputs

**Edits.** 28 of the 29 BD2 replacement texts of `bd-contract-review.json` are in the frozen bytes verbatim: 19 blocking and 9 non-blocking.
- The non-blocking `target.note` edit was **superseded**: the advisor tightened the target from `1/10^10` to `1/10^16` instead of relabelling it. The review offered both.
- The frozen note keeps the edit's two definitions: relative width `(upper − lower)/min(|lower|, |upper|)`, and nesting as an observed consistency check (check `prefreeze_edits_in_frozen_bytes`).
- The plan vocabulary is recorded from `plan.json` as committed with the freeze (sha256 `7d71bfcb…75c9`). All 12 gate fields, the three tiers and the four sub-labels are in it.

**Producer inputs.** I ran `find` on `forward/bd2/inputs/` (names only) and hashed each file against the repository.
- The folder holds 35 files: `AGENTS.md`, the contract and its 33 shared premises, including the four Round11 files (with `two_plaquette.py`), the AZ2 `check.py` and the AY1 forward report.
- Every file is byte-identical to its source, and the inventory equals the contract-derived list.
- No plan, panel, deliberation, expert, skeptic review or BD1 file is among them.

## 2. Executability, item by item

1. **Item 1 (graph tables).** Executable with zero truncation error.
   - `ψ_ij ∈ P_{i+j}`, and in the orthogonal basis `K` is diagonal. The D=6 and D=8 tables agree through total order 9. The `<z>` series along `l1 = l2` first differs at order 14.
   - The parities (odd/even, odd/odd, even/even) hold on the full two-variable table.
   - The second-order values at `l1 = l2` are `<z>` 7/216 and `<C_shared>` 1/24.
2. **Item 2 (enclosures).** Executable with an AZ2-type five-part ledger.
   - Every enclosure is positive, so its sign is certified. The D=8 enclosures nest inside D=6, and the `−l` enclosures equal the `+l` ones.
   - D=8 relative widths: 3.54e-32 (`l = ±1/1000`), 3.54e-25 (`±1/100`) and 3.56e-18 (`±1/10`).
   - D=6 widths (reported): 1.69e-22, 1.69e-17 and 1.71e-12.
3. **Item 3 (Z³ 1×2).** Executable.
   - The rectangle's six links are owned by `R`, and the first order is 0.
   - `|ω| ≤ K_2′τ²` ≈ 1.34175e-12, with `K_2′` recomputed from the AY1 items.
   - `|C∩E₃| = 6`, so evenness holds in F1 and in the limit.
4. **Item 4 (band).** Executable from the frozen premises.
   - At `τ = ±10⁻⁸`: lower `(3/2)L²` ≈ 2.875866e-19, with `L` the AY2 lower end exactly; upper `98|τ| = 49/50000000`.
   - The formal per-link values give `Σn_e = 168`, so the total is `7τ²/144`.
5. **Item 5 (2+1D).** Executable from the AM2 counting alone.
   - `L_k(3) = 8·6^k(1+4k/3)`, termination order 6, `G_3(R) = 9e^{3/32}` and `G_3′(R) = 118e^{3/32}`.
   - The self-map binds: the cap is ≈ 1.580747e-3.
6. **Items 6–7.** Executable: six obligations, the Einstein–QED no-transfer row, the template (clean, no placeholder) and the frozen gate fields.

## 3. Readings and residual defects (numbered)

1. **R1. The target discriminates the certificate.** With the same Ritz vector, the certificate choice decides the D=8 relative width at `l = ±1/10`:

   | certificate | D=8 width at `l = ±1/10` | margin against `1/10^16` |
   |---|---|---|
   | angle from the projected eigen-equations with the tail threshold `m_{D+1}` (mine) | 3.56e-18 | 28 |
   | AZ2 Eckart angle with the tail-comparison energy bound | ≈ 1.8e-17 (expected from the AZ2 report's own angle) | ≈ 5.6 |
   | Davis–Kahan with the full residual and the Weyl separation `3 − 2|l|` alone | 8.72e-17 | 1.147 |

   Any further loss would miss the target, for example rounding at `10⁻¹⁶` or `2s + 2s²` with a looser `s`. The frozen `limited` branch then applies. This makes the threshold a genuine test, as the advisor intended.
2. **R2. Two flips.** Already frozen after BD2-5. The flip of `vM` reverses both faces and fixes `z`, so it cannot separate the couplings. My validator rejects a single flip used for both couplings, and a parity check made at `l1 = l2` only.
3. **R3. The Eckart item of the ledger.** `enclosure_itemized_residual` lists a "Ritz/Davis-Kahan/Eckart part". My ledger's part (d) gives the retained Davis–Kahan angle, the tail angle from the projected eigen-equations, and a labelled full-residual Davis–Kahan comparison, but no Eckart angle. I read the item as "the Ritz-residual angle by a valid lemma, itemized". Non-blocking. If the gate requires the Eckart bound literally, it can be added; it would not tighten the result.
4. **R4. The band premises.** One rational bounds `‖ρ_R − P_R‖₁` from below for every box and for the limit: `L = sqrt10_lo|τ|/72 − K_2′τ²`, equal to the AY2 gate lower end. The finite-box use rests on AY1 forward F11–F14 (a premise of BD2), passed to the untruncated vector by AV1 F22, not on an AY1 or AY2 gate sentence. The frozen text says exactly this.
5. **R5. The formal per-link count.** `n_e ∈ {2, 3, 4}` on the 48 links of `R` (4, 16 and 28 links), `Σ = 168`. The triage's four faces per link would give 192 (`τ²/18`), which the frozen text now excludes.
6. **R6. "stars" in the 2+1D recount.** The frozen text lists "stars" without a definition. I read it as the union of the owner sets through a site (7 sites). The owner set itself (3 sites) is a separate entry. Non-blocking: a producer should define its reading.
7. **R7. The AZ2 checker as a premise.** The producer may re-instantiate it (the contract says so). My replay is my own code: the checker was hashed only. The pre-freeze preview that reused it is not part of this replay.
8. **D1 (residual, non-blocking). Two scopes for the 1×2 loop.** The bound holds for F2 boxes; evenness is not claimed for F2. The frozen texts agree on this, but a gate should keep the two scopes separate.
9. **D2 (residual, non-blocking). Nesting.** Nesting is observed at all six points and both cutoffs. It is not a target (frozen note).

## 4. Control mirror

- `controls` equals `preregistration.controls_required.ids`: 21 = 21, same order, no duplicates.
- 15 ids carry BD2 semantics. The other 6 are defined in the frozen BA1 contract, a declared premise (check `control_semantics_coverage`).
- The program implements all 21 as damaging mutations: 85 mutations and 4 positives.
  - The graph tables are decided against my own tables.
  - Each enclosure must intersect my certified one and exclude 0, and the D=8 `meets_target` flag is recomputed from the exported ends.
  - The band endpoints are decided against the AY1/AY2/AQ1 rationals.
  - The 2+1D constants are decided against my recount.
- **Deferred parts (scope notes):**
  - the inventory is recorded;
  - the phrase scan mirrors the round tool;
  - tampering is tested at packet level;
  - the angle lemmas, the BB2 identification and lower semicontinuity are restated in the derivation, not machine-checked; their inputs are exact.

## 5. Values, margins and source-edit mutations (exact rationals in `bd2-independent/results.json`)

| quantity | value | target / bracket | margin |
|---|---|---|---|
| max D=8 relative width of `<z>` | 3.5602e-18 (at `l = ±1/10`) | ≤ 1/10^16 | **28.09** |
| D=8 widths at ±1/1000, ±1/100 | 3.541e-32, 3.542e-25 | ≤ 1/10^16 | — |
| `<z>` second order at `l1 = l2` | 7/216 | exact | — |
| Z³ formal 1×2 coefficient | 7/124416 ≈ 5.6263e-5 | labelled formal | — |
| 1×2 bound at the cap | K_2′τ² ≈ 1.34175e-12 | exact_first_order | — |
| band at ±10⁻⁸ | [≈2.875866e-19, 49/50000000] | ratios 9939.60 and 100 | [9500,10500] ✓, 100 ✓ |
| 2+1D cap | ≥ 1/(576e^{3/32}) ≈ 1.580747e-3 | directed lower bound | — |

**Source-edit mutations** (scratch copies, each aborting for its intended reason):
- the shared-link weight `rho = 2`;
- Q4 with `E[t^{2h}] = 1/(2h)`;
- the edge cross term halved;
- the tail threshold taken one shell too far;
- the Ritz iteration stopped at `10⁻²⁰`;
- the face channels added in quadrature;
- the 1×2 state energy 24;
- selected faces counted in `n_e`;
- the upper budget `112|τ|`;
- the AM2 numerator `(1 + kp/(p+1))`;
- the 3+1D exponent in the 2+1D bracket;
- the lower endpoint with `K_2′τ²/2`;
- an h1 flip that fixes `z`;
- the Rayleigh–Schrödinger energy sign flipped.

The tail-threshold and lower-endpoint edits first ran to completion. They now abort because `tail_lower` is pinned to the AZ2 gate and `(3/2)L²` to the AY2 lower end. Both pins were added before these files were frozen.
