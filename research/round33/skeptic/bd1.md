# BD1 skeptical review (post-comparison, paired: forward characters route, reverse Weyl-integration route)

**Standing.** I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and both producers. The frozen BD1 contract carries the pre-freeze review written by another session of this role. This is not human peer review and not formal verification. Human project author: Hruday N M (BUNZEEY).

**Producers reviewed (paired loop).**
- **Forward** (`HNM-BD1-F`, route `characters`): Peter–Weyl, Pieri, Clebsch–Gordan and charge counting. Packet `research/round33/forward/bd1/`, commit 5a792b0.
- **Reverse** (`HNM-BD1-R`, route `weyl_integration`): constant terms on the SU(N) maximal torus, the SO(3) torus density, the binomial constant term for U(1), and summation for Z2. Packet `research/round33/reverse/bd1/`, commit a1010a4.

**Order, as it happened (UTC, from git).**
- The BD contracts froze at 9ae1160 (05:09:18Z; `frozen_at` 05:09:10Z).
- My BD1 values were final in scratch at 05:30:43Z (groups prototype). My pre-comparison checker produced every value of the committed package at 05:45:05Z: the prediction, obstruction, flip-set, group-table and SU(5) blocks of that run equal the committed `bd1-independent/results.json`.
- I recorded the producers' `inputs/` inventories at 05:37:45Z. I listed file names with `find` and hashed them; I did not read the files.
- **BD1 reverse** a1010a4, 05:53:54Z. **BD1 forward** 5a792b0, 05:54:17Z. **BD2 forward** 37fa623, 06:00:06Z.
- `bd1_check.py` was last written at 06:02:31Z. The edits after 05:45:05Z added the labelled `weyl_route_torus_trap` check and three tier-alignment mutations (85 → 88). No value changed.
- **My pre-comparison packages were committed last**, at bf1f531 (06:10:08Z). The producers committed first.
- Exposure before bf1f531:
  - the names and hashes of the producers' `inputs/` files;
  - possibly the one-line git subjects of a1010a4 and 5a792b0, in any `git log` output after 05:53:54Z.

  Both came after my values were final at 05:45:05Z. I opened `forward/bd1/` and `reverse/bd1/` only after the coordinator's post-comparison message.

**Verdict: `accepted_within_scope`.**
- Sub-label: `transfer_to_named_model`. Secondary sub-label: `obstruction_recorded`.
- **No blocking issues.**
- Every moment, coefficient and obstruction value is equal **exactly** across three sources: forward, reverse, and my three own routes (characters, Weyl constant terms on the SU(N) torus, and Frobenius/hook with closed-form counts). 141 cells are compared.
- The gate must export `flip_transfer_scope` naming SU(2), SU(4), U(1) and Z2; recommended text below. This is a gate requirement, not a defect of either packet.

## What the two packets prove, with quantifiers

**Convention and models.** The frozen convention:
- per-link electric term `8 C_2`, with `C_F = (N²−1)/(2N)` for SU(N), `n²` for U(1), `l(l+1)` for SO(3), and `C_2 = 1` on the odd Z2 state;
- face energy `32 C_F` and magnetic term `−(tau/3) W`, with `W = Re chi_fund/dim fund`;
- creation sign `psi = e^{−C} Omega_0` and `omega(W) = −2 Re (W Omega_0, c^(1))`.

The statements hold on the following models, and on nothing else for groups other than SU(2):
- the one-plaquette finite graphs `H_FG(G)`;
- the group-G whole-star box models `H^G_N`, box by box, for `|tau|` below the box's Kato radius;
- for SU(2) only, the admitted zero-selected family.

1. **Moments and first-order coefficients** for all seven groups, `k = 1..5` in the forward and `k = 1..4` in the reverse (SU(5) to `k = 6`):

   | group | `E[W^k]`, k=1..5 | `C_F` | first-order coefficient of `omega(W)/tau` |
   |---|---|---|---|
   | SU(2) | 0, 1/4, 0, 1/8, 0 | 3/4 | 1/144 |
   | SU(3) | 0, 1/18, 1/108, 1/108, 5/1296 | 4/3 | 1/1152 |
   | SU(4) | 0, 1/32, 0, 7/2048, 0 | 15/8 | 1/2880 |
   | SU(5) | 0, 1/50, 0, 3/2500, 1/50000 | 12/5 | 1/5760 |
   | U(1) | 0, 1/2, 0, 3/8, 0 | 1 | 1/96 |
   | Z2 | 0, 1, 0, 1, 0 | 1 | 1/48 |
   | SO(3) | 0, 1/9, 1/27, 1/27, 2/81 | 2 | 1/864 |

2. **Criterion A (flip).** A central `z` with `rho_fund(z) = −I` exists for SU(2), SU(4), U(1) and Z2, and for no other listed group:
   - `U_E` built from `z` commutes with every link Casimir, every endpoint gauge action and every on-site cutoff projection;
   - it fixes the vacuum and reverses every `W_f`;
   - hence `U_E H^G_N(tau) U_E^* = H^G_N(−tau)` in every box and cutoff.

   `omega(W)` is odd wherever the ground eigenvalue is simple.
3. **Criterion B (parity).** `E[W^3] = 0` exactly for SU(2), SU(4), SU(5), U(1) and Z2. Every cubic moment `E[chi^a conj(chi)^b]` with `a+b = 3` is a nonnegative integer and vanishes. With single-occurrence orthogonality, the first-order derivatives of `omega(W²)` and of the centred Euclidean and real-time correlations vanish.
4. **Obstruction cells.** All values are exact and nonzero:
   - **SU(3):** `E[W^3] = 1/108`, `d omega(W²)/dtau = 1/6912`, `omega_2 = 1/589824`.
   - **SO(3):** `1/27`, `1/2592`, `1/331776`.
   - **SU(5):** `E[W^3] = 0`, so the parity column is a transfer. `d omega(W²)/dtau = omega_2 = 0` by the Z_5 grading, and `omega_4 = 1/63403380965376 = 1/(2^30 3^10)` (≈ 1.57720295790e-14). SU(5) is therefore a flip obstruction on `H_FG(SU(5))`.
5. **Flip sets.**
   - `E_3` meets every owned plaquette of `Lambda_2`, `Lambda_3` and `Lambda_4` an odd number of times: 2335 / 6909 / 15291 plaquettes, 1082 / 3630 / 7348 of them once and the rest three times. It meets 1344 / 4536 / 10752 retained faces.
   - Every face meeting a 24-link coarse factor meets `E_3` oddly: 52 faces, 49 omitted and 3 selected. `E_3` has 16 links in a factor with `b_z` even and 8 with `b_z` odd.
   - `E_2` meets every plaquette of `[−N,N]²` exactly once.
6. **SU(2) area parity.** In every open centered whole-star box and every on-site cutoff at `kappa = 0`, `|tau| ≤ 10^-8`, both signs: `omega(W_C)(−tau) = (−1)^{A(C)} omega(W_C)(tau)`. It holds pointwise for the limit of the named constructions through BB2 at each sign.

## Adjudication of the coordinator's points

**1. Exact cross-route agreement.** For each of the seven groups, the following cells are equal across forward, reverse and my three routes:
- the moments `k = 1..4`;
- the first-order coefficient and `d omega(W²)/dtau`;
- the one-plaquette series `omega_0..omega_4`, `E_0..E_5` and `omega(W²)_0..2`.

SU(5) `E[W^5] = 1/50000` is also equal. That makes 141 cells, with no single-route cell. The obstruction values (SU(3), SO(3), and SU(5) `omega_4`) and my frozen predictions agree digit for digit (check `cross_route_exact_agreement`).

**2. Tier and route labels (D1 of my pre-comparison reply, R1 of my contract review).** Both producers follow the frozen control `tier_mixing_rejected`:
- `exact_first_order` is on every first-order coefficient and every first-order derivative: `d omega(W²)/dtau`, and the state and Duhamel terms of `C(s)`;
- moments and the second- and fourth-order coefficients carry a route and no tier;
- the forward labels every value `characters` (91 entries); the reverse labels every value `weyl_integration`.

**Neither packet is rejected.** The conflict is in the contract. `preregistration.tier_label_rule` says "every group coefficient carries the tier exact_first_order", but the control rejects "a tier on a moment or on a higher-order coefficient". The more specific control governs. This is contract defect C1, and it does not block.

**3. Flip scope (D2 / R2).** The frozen `gate_fields_required.flip_transfer_scope` is a description and names no group. `gate_fields_rule` requires that the scope "names the groups found".
- The forward exports the literal description, because its validator requires the frozen dict at accepted. It names the four groups in `gate_field_groups.flip_transfer_scope_named` and in the report.
- The reverse names them in the field itself. It adds `obstructions` and `parity_transfer_scope`, which are outside the contract's 12 fields.

The gate must check the four names. Recommended exact text:

> SU(2), SU(4), U(1) and Z2 (central elements -I, -I, e^{i pi} and the nontrivial element, each acting as -1 on the Wilson representation), on their one-plaquette models H_FG(G) and group-G whole-star box models H^G_N (the operator identity in every box and cutoff; oddness of omega(W) in each box inside its Kato radius), with the flip sets E_3 and E_2 verified; no AM2, AV1 or AQ statement for any group other than SU(2)

The parity groups (SU(2), SU(4), SU(5), U(1), Z2) and the obstructions belong in the accepted text, not in new gate fields.

**4. Criterion proofs on `H^G_N`.**
- **Kato radius `12 C_F/(21(2N)^3)`: valid, and sufficient rather than sharp.**
  - On the full box space, `H_0` has the simple vacuum and gap `8 C_min`: one excited link. `C_min = C_F` for all seven groups (for SU(4), `C_2(Lambda²) = 5/2 > 15/8`).
  - `||V_1|| ≤ F_N/3`, with `F_N = 21(2N)³` retained faces. My enumeration gives 1344, 4536 and 10752.
  - On `|z| = 4 C_F` the Neumann series converges for `|tau| F_N/3 < 4 C_F`. The Riesz projection is therefore analytic and of rank one. The spectrum moves by at most `|tau| ||V_1||`, so the eigenvalue stays lowest.
  - The one-plaquette radius is `48 C_F`.
  - Both producers export the same radii: 3/448, 1/84, 15/896, 3/140, 1/112, 1/112, 1/56 at `N = 2`.
- **"Unique" read as simplicity: correct.** The contract says "wherever the ground state is unique" in item 1 and "by AM2 uniqueness" in item 6. In both places the word means a simple finite-box ground eigenvalue, used as a hypothesis. The claim exclusion concerns uniqueness of any ground state beyond that. The forward says so explicitly (wording note 3 and limitation 2). The reverse writes "wherever the ground eigenvalue is simple". Every clause mentioning uniqueness in either report is negated, an identifier, or the exclusion list quoted verbatim.
- **Box first-order coefficients from the `N = 2` sums: confirmed.** Take `W` to be the xz face at the origin, which is a retained face.
  - My enumeration of the 1344 retained faces finds that every other retained face shares at most one link with `W`; 10 faces share exactly one.
  - So `sum_f E[W W_f] = E[W²]` and `sum_f E[W² W_f] = sum_f E[W W_f W] = E[W³]`.
  - The box coefficient `2(1/3) E[W²]/(32 C_F)` and `d omega(W²)/dtau = 2a E[W³]` therefore equal the one-plaquette values for every group.
  - The forward's `box_terms` equal these sums. The reverse states the same reduction.

**5. Periodic tori.** My enumeration and my GF(2) elimination cover 13 tori:
- `E_2`: 0 even plaquettes on 3×4 and on 4×4; 4 on 4×3; 3 on 3×3; 5 on 5×5; 3 on 3×5.
- `E_3`: 0 on 4×4×4; 16 on 3×4×4, 4×3×4 and 4×4×3; 24 on 3×3×4 and on 3×4×3; 27 on 3×3×3.
- Some flip set exists exactly when every coordinate plane has an even plaquette count: in 2D when `L_x L_y` is even, in 3D when at most one side is odd.

The forward's `E_2` on 3×4 = 0 is correct: `E_2` is keyed to `p_y`, and the odd side there is x. The reverse's GF(2) finding is correct, and so is the forward's labelled remark.

The contract's "obstruction" wording concerns `E_3` and `E_2` at the seam of an odd keyed side, not every flip set. "Not statements for periodic boxes with an odd side" is a scope exclusion. It is not a proof that the flip lemma fails there. Both producers make no periodic statement.

**6. SU(2) area parity for the limit.**
- At each `N` and each sign, `rho^{F1,N}_Y(−tau) = U_{E cap Y} rho^{F1,N}_Y(tau) U_{E cap Y}^*`. This holds because the AW1 identity holds and `U_E` is a product over links.
- BB2 item 1 bounds `sup_{M>N} ||rho^{F,M}_Y − rho^{F,N}_Y||_1 ≤ c'_site |Y| e^{|Y|/10^8} q^{d_Y}` at both signs, along the whole sequence.
- Conjugation is trace-norm continuous, so the identity passes to the limit pointwise.

The forward read `c'_site = 2/984375` and `q = 1/64` from the gate, not the labelled union value 1/500000. Its bound values are exact:
- the W face has `|Y| = 2` and `max|y|_inf = 1`, which I recomputed independently;
- the bound at `N_0 = 2` is `200/3149999937`;
- `2·bound < 10^-40` from `N = 21`.

The directed `e^x ≤ 1/(1−x)` bound is valid. The identity `|C ∩ E_3| ≡ A(S) (mod 2)` is audited as follows:
- my pre-comparison check covers 216 planar loops with alternative surfaces, plus 4 others;
- the forward covers 9 loops and 5 closed surfaces, including genus one;
- the reverse covers 6480 rectangles and 400 random surfaces, and its quaternion fixture signs follow `(−1)^A`.

**7. The SU(3) U(N)-torus trap.** The reverse integrates on the SU(N) torus. Its `TorusSU.norm` subtracts the minimum exponent, "exponents taken modulo the diagonal", so `z^{c(1,…,1)}` counts as the trivial character. It returns SU(3) `E[W^3] = 1/108` and SU(4) `E[W^4] = 7/2048`. On the U(N) torus my labelled trap gives 0 and 3/1024. The forward's internal cross-check reduces modulo the diagonal in the same way. A U(N) substitution in either producer aborts:
- the reverse with `check failed: haar_moments_weyl_integration`;
- the forward with `routes disagree on SU(2):E[W^2]`.

## Producer notes, disclosures and wording findings

- **Reverse report preview typo (non-blocking).** Section 7.3 prints `omega_4 … preview 1.57720727258e-14`. The exact `1/63403380965376` truncates to `1.57720295790e-14`, which is what the reverse `results.json` carries. The other 11 previews in the reverse report and all 19 in the forward report are within one unit of their last digit.
- **Silent edits.** Some edits are caught only by my validator:
  - forward: `c'_site` read as 1/500000; the region bound without `e^{|Y|/10^8}`;
  - reverse: the box Kato radius doubled; the one-plaquette radius `96 C_min`.

  Each runs to completion in the producer. Neither producer cross-checks those exported values.
- **Paired reading of `moment_tables_two_routes`.** Each producer computes one route: the reverse makes two constant-term evaluations inside `weyl_integration`, and the forward adds a labelled internal Weyl cross-check. The cross-route equality is established here, cell by cell. This matches the reverse's wording finding 2 and my contract-review D1.
- **Box-model coefficient.** Both producers state and verify that it equals the one-plaquette value, which answers my contract-review D2.
- **Wording findings.** The reverse's five findings (tori, moment tables, AW1 display sign, corollary coupling, level span) and the forward's three wording notes (tori, "unique", Kato radius not fixed by the contract) are correct.
- **Forward scratch and style reads.** The forward declares scratch `/tmp/claude-0/bd1-forward-private/` and style-only reads outside `inputs/`: tools README, freeze, phrase_scan, and the Round32 AW1 `check.py` for conventions. No value depends on them. Both inventories hold exactly the 23 declared inputs.

## Replays and mutation harness

- `freeze.py verify` reports `verified` for both producers.
- Both closures verify file by file (27 files each). Both inventories equal the contract-derived list and my names-only record, and are byte-identical to the repository.
- Both producers reproduce `output/` byte for byte under `-B` and `-B -O`:
  - forward `adfa24fb…e4c3`, 37 checks, 111 damaging mutations;
  - reverse `8052d2e9…7629`, 64 checks, 110 mutations.
- My pre-comparison package is unchanged and replays byte for byte: 57 checks, 22 controls, 88 mutations, 4 positives.
- `bd1_postreview_check.py`: 29 checks, byte-identical under `-B` and `-B -O`, also in a `git archive` tree of HEAD d95db8c plus the new files.
  - It runs 71 source-edit runs:
    - 4 unmutated or without-`-B` runs;
    - 44 validator weakenings, one per control per producer. Each forward run aborts naming a mutation of that control. Each reverse run aborts naming the validator inside that control's `control(…)` call, read from the traceback;
    - 17 must-abort substitutions: the U(N) torus in both routes, a zeroed SU(3) cubic moment, Z2 Casimir 1/4, flip-set membership without x-links, face energy `24 C_F`, a perturbed SU(5) closed form, premise edits, an undeclared input, and report edits;
    - 6 silent edits: 2 harmless, and 4 damaging ones caught only by my validator.
  - 27 damaged packets are rejected by my validators for the expected reasons.
- No interpreter cache exists in either closure after all runs. The `research/round33/tools/__pycache__` present in the checkout predates this review (2026-09-24), is gitignored and lies outside every closure.

## Blocking issues

None.

## Non-blocking findings

- **N1.** Reverse report `omega_4` preview typo; results correct.
- **N2.** The forward exports the literal scope description in `gate_fields` and puts the group names beside it.
- **N3.** The reverse `gate_fields` carries two fields outside the contract list.
- **N4.** Four silent edits are caught only by the skeptic validator (see above).
- **N5.** The forward headline previews use 8-digit truncation and its report mixes 4–5-digit rounding. All are within one unit of the last digit.
- **N6.** The reverse exports moments only to `k = 4` (SU(5) to 6). This is sufficient: the contract asks `k = 1..4`.

## Contract defects (non-blocking)

- **C1.** The literal `tier_label_rule` conflicts with the control for higher-order coefficients. The control governs (R1).
- **C2.** `flip_transfer_scope` in `gate_fields_required` is a description, while `gate_fields_rule` asks that the groups be named (R2).
- **C3.** "Unique" in items 1 and 6 means a simple finite-box ground eigenvalue.
- **C4.** The periodic "obstruction" concerns `E_3`/`E_2` at the seam, not every flip set. The GF(2) criterion is at most one odd side.
- **C5.** In a paired loop, `moment_tables_two_routes` is a pair-level comparison.
- **C6.** The contract does not say that the box first-order coefficient equals the one-plaquette value; both producers prove it.
- **C7.** The inherited AW1 display sign `2 (W Omega_0, c^(1))`. The contract records it, and both producers reject it.

## Binding, limitations and advice

`bd1.json` binds every piece of evidence by sha256:
- both producer closures and their `freeze.json`;
- the contract, the selection note and every declared premise;
- my pre-comparison and post-comparison files.

The supported statement quotes the mandatory template once as one unbroken span. The phrase tool passes it and the limitations with the BD1 contract.

**Advice for the gate.**
- Export the 12 contract gate fields with `flip_transfer_scope` as recommended above.
- Put the parity columns and the obstruction values in the accepted text.
- Do not copy the reverse report's `omega_4` preview.
- Keep "not statements for periodic boxes with an odd side" as an exclusion.
- The next applications step would need its own contract: an AM2 re-instantiation for any group other than SU(2).
