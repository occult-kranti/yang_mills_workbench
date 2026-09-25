# BD1 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/bd1.json` (sha256 `a5c84166…75c1fc`, frozen 2026-09-25T05:09:10Z) before reading anything of either BD1 producer. I am a model-agent skeptic with correlated ancestry. This is not human review. The pre-freeze review of this contract (`bd-contract-review.md`/`.json`) was written by another session of this role; I read its blocking edits and determinations, not its advisor-only previews. BD1 is paired, so my replay is the skeptic's input to the post-comparison of two producer routes. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written. Nothing blocks production.** `bd1_check.py` establishes the following:
- 57 checks pass, byte-identical under `-B`, `-B -O` and plain `python3`, with no cache written.
- All seven group cells are computed exactly by characters, by Weyl integration and by a labelled third route (Frobenius counts), and the three agree. SU(2) reproduces AW1 (`1/144`, the moments and the one-plaquette coefficient `−5/11943936`).
- All 22 controls execute as damaging mutations: 88 mutations, each rejected for the expected reason, plus 4 positive cases accepted.
- 12 source-edit mutations of the program all abort (§5).

Four readings will matter at the post-comparison:
- **R1:** under the frozen `tier_mixing_rejected`, the second- and fourth-order coefficients carry a `route_of_computation` in {characters, weyl_integration} and no tier. The first-order `tau`-derivative of `omega(W²)` carries `exact_first_order`.
- **R2:** `flip_transfer_scope` in `gate_fields_required` is a description. The exported scope must name the groups (SU(2), SU(4), U(1), Z2).
- **R3:** the reverse's Weyl integration must run on the SU(N) torus. The U(N) torus erases the SU(3) obstruction.
- **R4:** the SU(5) fourth-order coefficient has an exact closed form from the single Z₅ column path; it is small (≈1.58e-14) but not delicate.

## 1. Frozen bytes against the pre-freeze edits; producer inputs

**Edits.** All 24 BD1 replacement texts of `bd-contract-review.json` are in the frozen bytes verbatim: 15 blocking and 9 non-blocking (check `prefreeze_edits_verbatim_in_frozen_bytes`). The review's previews block is not read by the program. The plan vocabulary is recorded from `plan.json` as committed with the freeze (sha256 `7d71bfcb…75c9`). The 12 gate fields, the single tier and the two sub-labels are all in it.

**Producer inputs.** I ran `find` on `forward/bd1/inputs/` and `reverse/bd1/inputs/` (names only) and hashed each file against the repository.
- Both folders hold the same 23 files: `AGENTS.md`, the contract and its 21 shared premises.
- Every file is byte-identical to its source, and the inventory equals the contract-derived list.
- No plan, panel, deliberation, expert, skeptic review or other producer file is among them. The reverse isolation flag is `true`, and the reverse folder holds no forward file.

## 2. Executability, item by item

1. **Item 1 (criterion A).** Provable as written. A central `z` with `ρ_fund(z) = −I` commutes with all translations, so it commutes with Casimirs, cutoff projections and gauge actions, and fixes `Omega_0`. It maps `W_f → (−1)^{|f∩E|} W_f`. The group cases:
   - It exists for SU(2), SU(4) (`−I`, since `det = 1`), U(1) and Z2.
   - It does not exist for SU(3) and SU(5) (the centre consists of `N`-th roots of unity) or for SO(3) (trivial centre).
   - The one-plaquette grading `(−1)^{N-ality}` is checked exactly.
2. **Item 2 (criterion B).** Provable as written, including the complex level. The level at `32 C_F` in a box is `span{chi_□(U_g)Ω, chi_□*(U_g)Ω}`: four links at the minimal Casimir must form a 4-cycle. Its `V`-compression reduces to the cubic moments, which are nonnegative integers. The nonzero derivative for `E[W³] ≠ 0` is `(2/3)E[W³]/(32C_F)`.
3. **Item 3 (moments and first order).** Executable by both routes. Weyl integration for SU(5) at `k ≤ 5` needs only the one-sided Weyl factor (120 terms) and takes well under a second.
4. **Item 4 (obstruction cells).**
   - SU(3) and SO(3) are exhibited with nonzero exact coefficients.
   - For SU(5), both SU(3)-type coefficients vanish, and the fourth order equals `1/63403380965376` by the series and by the column-path closed form.
   - The flip non-existence follows from Hellmann–Feynman: a flip unitary would make `E(τ)` even and `ω(W)` odd.
5. **Item 5 (flip sets).** Enumerated on `N = 2, 3, 4`, on seven coarse factors (52 faces each) and on E₂ for `N = 2, 3, 4`. The odd tori are recorded with 16 (E₃) and 4 (E₂) even plaquettes.
6. **Item 6 (area parity).** Provable from AW1 F09–F10 and BB2 item 1 at each sign.
   - Surface independence follows from `|C∩E₃|` alone; no homology is needed.
   - The Casimir step goes through bounded spectral cutoffs.
7. **Items 7–8.** The ledger has 28 rows and there are 11 obligations. The template scans clean and has no placeholder. The gate fields are as frozen (with R2).

## 3. Readings and residual defects (numbered)

1. **R1. Route labels on higher-order coefficients.** The frozen BD1 `tier_mixing_rejected` rejects "a route_of_computation other than characters or weyl_integration", and it also governs "the second- and fourth-order one-plaquette coefficients".
   - A producer that labels a Rayleigh–Schrödinger value `rayleigh_schroedinger`, or labels its closed form `closed_form`, is rejected by the frozen text. The route label must name where its matrix elements come from.
   - "Every first-order tau-derivative carries the tier exact_first_order" includes `dω(W²)/dτ` in the obstruction cells.
   - My validator implements exactly this: 3 mutations and 1 positive.
2. **R2. `flip_transfer_scope`.** The frozen value describes the scope ("the listed groups … named in the gate group by group"), and `gate_fields_rule` says the exported scope "names the groups found".
   - A recorder that compares exported gate fields literally with `gate_fields_required` would reject a correct packet.
   - I read the field as "names exactly SU(2), SU(4), U(1), Z2, the two named models and the AM2 exclusion". Both the literal frozen text and a scope adding SU(5) are rejected.
   - Non-blocking. The gate should apply the rule, not string equality.
3. **R3. The torus trap.** Constant-term extraction that keeps only the exponent 0 integrates over U(N). It gives `E[W³]=0` for SU(3), `E[W⁴]=3/1024` (not `7/2048`) for SU(4) and `E[W⁵]=0` for SU(5).
   - The contract says "Weyl integration over the maximal torus by constant-term extraction" without naming the SU(N) constraint.
   - A reverse on the U(N) torus would turn SU(3) into a parity transfer and could not exhibit the SU(5) cell. The two-route agreement would then fail loudly on SU(3), SU(4) and SU(5).
   - Recorded as a producer trap (check `weyl_route_torus_trap`), not a contract defect.
4. **R4. The SU(5) fourth order is exact and unique-path.** `ω₄ = 30/(243·10⁵·Π_k 32C_2(Λ^k))`.
   - A basis truncated below four steps from the trivial class changes it. At six and seven steps (80 irreps and more) it is stable.
   - The same argument gives SU(3)'s `ω₂` from the three-step path.
5. **R5. Kato per box.** Criteria A and B for `G ≠ SU(2)` use simple ground states near `τ = 0` in each box, with a box-dependent radius. This is a plain Kato statement: `H^G_N(0)` has the simple vacuum `Omega_0` and a gap of at least `8 C_F` (one link at the minimal nontrivial Casimir, which is `C_F` for all seven groups), and the interaction is bounded in each box. It is not the AM2 uniqueness that `claim_exclusions` names, so `uniqueness_of_ground_state_claimed: false` remains correct. The per-box radius must never be read as uniform in `N`.
6. **R6. E₃ on the coarse factors** has two patterns (16 and 8 links) by the parity of `b_z`. The frozen `flip_sets` text says so. The lemma needs only the odd intersection with every face.
7. **D1 (residual, non-blocking). `moment_tables_two_routes`.** The text says every moment "is computed exactly by both routes". In a paired loop each producer computes one route, so the two-route agreement is a gate-level comparison. I read the control as satisfied by the pair.
8. **D2 (residual, non-blocking). Box-model first-order coefficient.** The template says each group has "its own first-order Wilson coefficient … on one-plaquette models and on group box models". The box value equals the one-plaquette value for a retained face: single occurrence, and `W_fΩ` has energy `32C_F`. The contract does not say so explicitly, so producers should state it.

## 4. Control mirror

- `controls` equals `preregistration.controls_required.ids`: 22 = 22, same order, no duplicates.
- 16 ids carry BD1 semantics. The other 6 (`coherent_evidence_tampering`, `exact_arithmetic_admission`, `no_priority_or_continuum_claim`, `insufficient_verdict_retained`, `placeholder_span_rejected`, `negation_aware_phrase_scan`) are defined in the frozen BA1 contract, a declared premise (check `control_semantics_coverage`).
- The program implements all 22 as damaging mutations: 88 mutations and 4 positives.
  - Exact cell values are decided against my own three-route table.
  - The flip and parity columns are decided against the centre analysis and `E[W³]`.
  - The flip sets are decided against the enumeration.
- **Deferred parts (scope notes):**
  - the inventory is recorded;
  - the phrase scan mirrors the round tool;
  - tampering is tested at packet level;
  - criteria A and B on `H^G_N` and the BB2 passage are restated in the derivation, not machine-checked beyond the one-plaquette models and the flip sets.

## 5. Values and source-edit mutations (exact rationals in `bd1-independent/results.json`)

| cell | value |
|---|---|
| first-order coefficients | SU(2) 1/144, SU(3) 1/1152, SU(4) 1/2880, SU(5) 1/5760, U(1) 1/96, Z2 1/48, SO(3) 1/864 |
| SU(3) obstruction | E[W³]=1/108; dω(W²)/dτ=1/6912; ω₂=1/589824 |
| SO(3) obstruction | E[W³]=1/27; dω(W²)/dτ=1/2592; ω₂=1/331776 |
| SU(5) flip obstruction | ω₄=1/63403380965376 ≈ 1.5772e-14 (parity transfer: E[W³]=0) |
| flip / parity transfers | SU(2), SU(4), U(1), Z2 / SU(2), SU(4), SU(5), U(1), Z2 |
| scaling | first order exactly 100, second order 10⁴, SU(5) quartic 10⁸, moments 1 |

**Source-edit mutations** (scratch copies, each aborting for its intended reason):
- Z2 odd Casimir `1/8`;
- the SO(3) `W` coefficient changed in the character route only;
- `C_F = (N²−1)/N`;
- the Pieri rule without the antifundamental moves;
- the Weyl factor without signs;
- the E₃ x-links keyed to `p_x`;
- the SU(5) closed form without the conjugate path;
- the obstruction closed form without `1/3`;
- the selected predicate with `r=3`;
- a hook length off by one;
- the face energy `8C_F`;
- SO(3) given a central `−1`.

The SO(3)-centre edit first stopped with a `TypeError`. It now aborts through an explicit check (`central -1 claimed for a group without a centre grading`), added before these files were frozen.
