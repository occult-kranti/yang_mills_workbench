# AX1 skeptical review (post-comparison)

**Verdict: accepted_within_scope, sub-label `uniform_local_closeness_not_uniqueness`.** Both routes carry out all ten contract items for the uniform Kogut–Susskind SU(2) Hamiltonian at fixed spacing and strong bare coupling (`g^4=96/tau`, so `g^4=9.6×10^9` at the cap). Both use route B with the Haar reference, and both prove the same constants:

- `J'=29|tau|`;
- the re-frozen `J_0'=29/10^8`, with `1073/175000000<1/64` and `319/1562500<1`;
- the reset `102|tau|`, with `epsilon_R<=17|tau|` from the Haar gap six;
- 7 stars and 2 single-factor groups meeting `R`, holding 6 selected faces;
- 52 faces per factor, with 96 and 168 as labelled bounds only.

Both producers transfer the flip identity and `+tau/144` to the uniform model with proofs, and neither transfers `K_2`. The two tier-(ii) values differ, and each is a valid upper bound:

| Source | `D'_ii` at `tau=±10^-8` | Form |
|---|---|---|
| forward | `2425369125199104794263242601250/167893028420061547330293754713793182097` ≈ **1.44459e-8** | `2eps(1+eps)/(1+eps^2)`, `eps=2T'+T'^2` |
| reverse | `30934916107401289/2530733246376451200000000` ≈ 1.22237e-8 | `2eps`, `eps=88\|tau\|/144+2rho'+T'^2` |
| skeptic (pre-comparison) | identical to the forward value, rational for rational | forward form |

**The gate should bind the forward value.** It is the larger bound, and both inequalities certify it. It uses no R-refinement, and it is also what the AV1 gate bound for the zero-selected family. Both values meet `4/10^7` at both signs, so `target_met` is true. Tier (i) (`D'_i≈2.4526e-5`) fails the target and is retained. There are **no blocking issues**. No Euclidean node, `K_2`, uniform Wilson-mean sign, weak-coupling or continuum statement is admitted.

**Standing.** I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and both producers. My own triage (c)4 seeded route B and its constants. This is not human peer review or formal verification. Human project author: Hruday N M (BUNZEEY).

**My pre-comparison package is unchanged.** It contains:
- `ax1-independent-derivation.md`;
- `ax1_check.py` (80 checks, 26 of the 28 controls);
- `ax1-contract-review.md`;
- `ax1-independent/results.json`.

Its hashes match `ax1-independent-freeze.json`, and a replay under normal and `-O` Python is byte-identical. It was committed (`489e20e`, 00:58:34Z) before the reverse commit (`4eb7d8e`, 01:08:09Z) and the forward commit (`b2a1d86`, 01:09:17Z). It already contains every producer headline exactly:
- the forward `D'_ii` (my `D_ii_exact52`);
- the reverse `D'_ii` and its density form (my labelled `D_ii_R88`);
- both `D'_i`.

**This review adds:**
- `ax1_postreview_check.py`: 57 exact checks, including 29 source-edit mutation receipts;
- `ax1-postreview/results.json`: byte-identical under normal and `-O` Python, sha256 `def60c55…fe3`;
- `ax1-replays.json`.

## What is proved, with quantifiers

**Model.** The model is the uniform Kogut–Susskind SU(2) Hamiltonian on Z³ at fixed spacing:
- every elementary face has `nu=alpha*tau/24` (AL1: `alpha=g^2/(2a)`, `lambda=2/(g^2a)`, `tau=96/g^4`);
- both signs, `|tau|<=10^-8`;
- centred whole-star boxes `Lambda_N`, `N>=2`;
- the original xz Wilson loop `W` with cover `R={0,e_z}`;
- clock `theta=alpha t/hbar`, `G=H/alpha`.

The uniform triple `tau/24` lies in the admitted box for every `|tau|<=3`. `tau<0` has no real-`g` preimage: it is the `U_E` image of `+|tau|`, not a second coupling.

1. **Route B.** The on-site operator `h_b=8 sum C_e>=6Q_b>=Q_b` does not depend on tau and has the Haar vacuum.
   - The whole star `phi_b` holds the 21 omitted faces, with norm `7|tau|`.
   - The single-factor group `psi_b=-(tau/3)(W_g1+W_g2+W_g3)` has support `{b}` and `||psi_b||<=|tau|`.
   - Every face is charged exactly once: 5565 faces in `Lambda_3`.
   - `J'=4·7|tau|+|tau|=29|tau|`. The maximal support is 4 and the termination order is 8.
2. **Contraction.** At the cap, `J'=29/10^8>J_0=7/25000000`, so AM2 is re-instantiated with `J_0'=29/10^8` (R1). Using `e^{1/8}<8/7`, `G(R)<148/7`, `G'(R)<352`:
   - `J_0'G(R)<1073/175000000<1/64`;
   - `2J_0'G'(R)<319/1562500<1`.

   Every finite complete-factor route-B volume, at both signs, therefore has a unique gauge-invariant ground and a full-space gap of at least 1/2 normalized (`alpha/16` physical). The physical excited sector is nonzero.
3. **Reset and the AQ checklist.**
   - `omega(h_R)<=2(7·7+2·1)|tau|=102|tau|`.
   - `h_R>=6(I-P_R)` gives `epsilon_R<=17|tau|` and `2sqrt(17|tau|)≈8.246e-4<=1/500`, which is a square-root control only. The variance floor `61999/250000` follows.
   - AQ1's constants become `C_F=58|tau||F|` and `||Phi'||_F<=81J'=2349|tau|`.
   - The remaining AQ1, AQ2 and AV1 steps re-apply verbatim.
4. **Incidence.** Exactly 7 stars (anchors `R-S`) and 2 single-factor groups meet `R`. They hold:
   - 153 faces charged;
   - 88 faces meeting `R` (82 omitted, 6 selected);
   - 16 faces inside `R`;
   - 6 selected faces.

   No face is charged twice. `||B_N||<=51|tau|/8` and `k'=51|tau|/4` in `G` units.
5. **Counts.** The exact count is 52 faces per factor (49 omitted plus 3 selected; offsets 24+4+8+16) and 88 for `R`. The contract's 96 (4×24) and 168 (7×24) are valid bounds, not counts.
6. **State lemma, tier (ii).**
   - The value to bind is `D'_ii=2425369125199104794263242601250/167893028420061547330293754713793182097`. It meets `4/10^7` (margin 27.69) and `10^-6`.
   - The reverse's labelled R-refinement, ≈1.22237e-8, is also valid.
   - Tier (i) is `D'_i=23002790096235779074916932482/937890625141038667264537458466241` (≈2.4526e-5). It fails the target and is retained.
   - Consequences: `|omega(W)|<=D'`, `|omega(W^2)-1/4|<=D'/2`, and `m^2<=D'^2`.
   - The bound passes to every AQ1 subsequential limit. This is uniform local closeness, not uniqueness, whole-sequence convergence or a rate in N.
7. **Transfer.** Every face coefficient is `-(tau/3)`, `h_b` is τ-independent, and `E` meets every plaquette oddly, selected faces included. Hence `U_E H_N(tau)U_E^*=H_N(-tau)` in every box and every cutoff. Consequences:
   - `omega_{N,-tau}(W)=-omega_{N,tau}(W)`, and `omega_N(W^2)`, `C_N` and `c_N` are even;
   - `S(-tau)=S(tau)∘alpha_E` as whole sets;
   - the AW1 link grading applies verbatim to the selected faces;
   - only `f=W` contributes at first order, so `omega(W)^(1)=+tau/144` (`±1/14400000000`) is unchanged.

## Exact numbers re-derived (my own Fraction code)

**Constants** (every exported value of both producers equals mine; check `producer_constants_agree`):

| Quantity | Value | Forward | Reverse |
|---|---|---|---|
| `g^4` at the cap | 9600000000 | = | = |
| `J'` per `\|tau\|` | 29 (28 stars + 1 single) | = | = |
| `J_0'`, self-map, contraction | `29/10^8`, `1073/175000000`, `319/1562500` | = | = |
| reset, `epsilon_R`, gap | `102\|tau\|`, `17\|tau\|`, 6 | = | = |
| `C_F`, `\|\|Phi'\|\|_F` | `58\|tau\|\|F\|`, `2349\|tau\|` | = | = |
| `\|\|B_N\|\|`, `k'` | `51\|tau\|/8`, `51\|tau\|/4` | = | = |
| counts | 52 per factor, 88 meeting R, 16 inside R | = | = |
| `t_1'`, `T'`, `rho'` | `13/3600000000`, `13/3599632512`, `4147/11248851600000000` | = | = |

The three itemized incidence tables (forward, reverse, mine) agree row by row. For each group anchor they give the faces meeting `R` and the faces inside `R`:

| Anchor | Group | Faces meeting `R` | Inside `R` |
|---|---|---:|---:|
| 0 | star | 21 | 10 |
| `e_z` | star | 21 | 0 |
| `−e_z` | star | 16 | 0 |
| `−e_x` | star | 4 | 0 |
| `−e_y` | star | 8 | 0 |
| `e_z−e_x` | star | 4 | 0 |
| `e_z−e_y` | star | 8 | 0 |
| 0 | single | 3 | 3 |
| `e_z` | single | 3 | 3 |

**Why the two `D'_ii` values differ.** Both producers use the same three ingredients:
- `t_1'=52|tau|/144` (the reverse's `t_1'=13/3600000000` equals the forward's);
- the self-consistent `T'=t_1'/(1-352J')` and `rho'=352J'T'`;
- the pair term `T'^2`.

They differ at one inequality: the first-order collection over creations meeting `R`.
- **The forward** uses AV1's `eps=2t+t^2`, which bounds `sum_{I∩R≠∅}||c_I||` by `2||c||_a<=2T'=2t_1'+2rho'`. That charges `2×52=104` first-order faces, so the 16 faces whose owner sets contain both 0 and `e_z` are counted twice.
- **The reverse** bounds the same sum by `sum_{I∩R≠∅}||c^(1)_I||+2||c-c^(1)||_a<=88|tau|/144+2rho'`, which counts the 88 faces meeting `R` once.

Exactly, `eps_fwd-eps_rev=16|tau|/144=|tau|/9`.

The final inequalities also differ:
- the forward applies the explicit-density bound `2eps(1+eps)/(1+eps^2)`;
- the reverse applies `2eps`, which is at least the fidelity bound `2eps/sqrt(1+eps^2)`.

This second difference moves `D` by only about `1.04e-16`. So `D_fwd-D_rev=2|tau|/9+1.04e-16≈2.2222e-9`, and the ratio is ≈1.1818 (13/11).

**Validity.**
- **Forward.** Its value is valid under both inequalities. The density form at `eps=2T'+T'^2` dominates the fidelity form at the same `eps`. `sum_{I∩R≠∅}||c_I||<=sum_{I∋0}+sum_{I∋e_z}<=2||c||_a` holds, and the pair term is at most `T'^2`.
- **Reverse.** Its value is valid as the analogue of the AV1-reviewed labelled 82-face refinement. It uses `||c^(1)_I||=|tau|sqrt(n_I)/144<=|tau|n_I/144` with `sum_{I∩R≠∅}n_I=88` and `sum_{I∩R≠∅}||(c-c^(1))_I||<=2||c-c^(1)||_a<=2rho'`. Its headline rests on the fidelity inequality. Its density form, `313152084581405409248249989599356957723042/25618443057260367560228658195881478548484878861521` (≈1.22237e-8), is also below the target.
- **Ordering:** `fidelity(eps_rev)<=D_rev<=density(eps_rev)<2eps_fwd<=D_fwd<=4/10^7`.

**Which to bind.** The gate should bind the forward `D'_ii`, for five reasons:
- it is the larger bound, and both inequalities certify it;
- it uses no 88-face refinement, so it stays valid even if the refinement were disputed;
- it equals my pre-comparison headline;
- the reverse reproduces it exactly as its `tier_ii_global_two_site` density variant, so three agents agree rational for rational;
- it is the same construction the AV1 gate bound. My code reproduces AV1's `D_ii` exactly from 49 faces and `J=28|tau|`.

The reverse value should be admitted as a labelled R-refinement.

**Other re-derived values.**
- **AX2 feasibility.** `2(D+D^2)+51|tau|/pi<=10^-6` holds with the bound (radius ≈1.9123e-7, margin 5.23). The threshold lies in `[41883,41884]/10^11`, so the contract's "4.19×10^-7" is infeasible.
- **Scaling.** All forms scale linearly: the ratios `D(tau)/D(tau/100)` are 100.0101 (forward), 100.0119 (reverse) and 100.0015 (crude), against exactly 10 for the square-root control.
- **First order.** Among the 88 faces meeting `R`, only `f=W` has `E[W W_f]≠0` (it is 1/4). `E[W^2W_f]=0` for all 88. The 6 selected faces give zero, and 2 of them share a link with `W`.
- **Flip set.** `E` is odd on every plaquette of the fine box, including all 375 selected faces of `Lambda_2`. The 3×3 compression confirms `D H(tau,tau) D=H(-tau,-tau)`, and an untied selected coefficient breaks the identity.

## Review against the ten required items (both producers)

1. **Dictionary and box: complete in both.** Both give `tau=96/g^4` on three exact `(g^2,a)` fixtures, the box `|tau|/24<=1/8` iff `|tau|<=3`, the label, and the negative-sign note.
2. **Route B: complete in both.**
   - `||psi_b||<=|tau|` with equality at the identity configuration, and `J'=29|tau|`.
   - Support 4, and termination 8 with the qubit fixtures.
   - The AM2 majorant `2^p(2p)^k(1+k(p+1)/p)` uses `|X|<=p` only as an upper bound, so single-site groups are covered. This is the one new step; the rest of the majorant is inherited.
   - The reverse also compares four groupings. The per-face grouping (`52|tau|/3`) is smaller but changes the boundary prescription, and it is disclosed and not used.
3. **Contraction: complete in both.**
   - Both pin `J_0'`, `1073/175000000` and `319/1562500` with the contract sha256.
   - Both reject the old `J_0` and R2.
   - Both give the on-site theorem (`h_b>=6Q_b`), Haar gauge invariance and a nonzero excited sector. The forward argues from `{Omega_0, 2W_gOmega_0}`, with dim `H_phys>=2`; the reverse from the strictly positive ground and `(W_g-<W_g>)Omega_H≠0`. Both arguments are valid.
4. **AQ1/AQ2 checklist: complete in both.**
   - `||Phi'||_F` is recomputed as `81J'=2349|tau|`, not AQ1's 2268. A per-pair bound of `567|tau|` also holds; it is labelled and not needed.
   - `C_F` is `58|tau||F|`.
   - The reset is `102|tau|`.
   - **Haar gap six (the forward's note, assessed).** The forward's note is correct.
     - With gap one, `4·102/10^8>(1/500)^2`, so AQ2's `1/500`, and with it the variance floor, would fail.
     - AQ2's own `98|tau|` passed with gap one only barely: `2sqrt(98/10^8)≈1.980e-3`.
     - `h_R>=6(I-P_R)` follows from `Q_0⊗I+I⊗Q_{e_z}-(I-P_0⊗P_{e_z})=Q_0⊗Q_{e_z}>=0`, which the reverse writes out.
     - The reverse lists the floor as "verbatim" and puts the new constant in its overlap row. The forward lists the floor as "new constant (gap six required)". The substance is the same (N9).
   - The verbatim steps are the same in both: stationarity, GNS, nonnegativity, gauge averaging, reference moments, cutoff-vector removal and AQ passage.
5. **Incidence: complete in both.** Both give the all-size argument (`R-S` and `R`), the boxes for `N=2..4` (forward) and `N=2..11` (reverse, by coordinates), and `N=1` with 4 stars.
6. **State lemma: complete in both.**
   - Both apply the AV1 product ordering with the enlarged creation set. The single-site `c_{0}` and `c_{e_z}` are now first-order nonzero, both enter the pair term, and both are named.
   - Both give the crude and exact tiers at both signs, with 52 derived, and 96 and 168 labelled as bounds.
   - The two tier values differ as analysed above.
7. **Controls and claims: complete in both.**
   - All 28 control ids are damaging mutations in both producers. The forward has 93 in control checks, plus 1 in `flip_set_odd_all_classes`, for the 94 it reports. The reverse has 111.
   - Flags are the same in both: `continuum_claim`, `weak_coupling_claim`, `resolved_interaction_shift`, `scientific_priority_verified` and `euclidean_node_certified` are false; `uniform_wilson_claim` is true, scoped to the fixed-spacing model as labelled.
   - The forward also sets `uniqueness`, `rate`, `whole_sequence`, `k2_uniform` and `wilson_mean_sign` to false.
   - Replays are byte-identical, and both closures are frozen with `freeze.py`.
8. **Premises: as declared.**
   - The reverse inputs are exactly AGENTS.md, the contract and the 36 shared premises: 38 files. None of triage, loop-2, deliberation, experts, forward AX1 or skeptic AX1 is among them.
   - The forward inputs are the declared 41.
   - The contract text and `selection-ax1.md` state route B, `29|tau|` and the `J_0` issue, so the reverse could not "find them itself". Its independence is limited to proof route, enumeration and code. It says so; I recorded the same point before production (contract review item 8).
9. **Transfer: proved in both, not cited.** Both give the following:
   - the tie `kappa=tau` (selected coefficient `nu=alpha tau/24`) and τ-independent `h_b`, so the identity is `H(tau)->H(-tau)` with no `Q_L'` step;
   - the odd intersection enumerated with selected faces: the forward over 648 anchored faces and 3600 plaquettes, the reverse over 6591 plaquettes and the 1719 faces of `Lambda_2`;
   - the grading verbatim for single-face characters;
   - `+tau/144` with only `f=W`, and the selected faces orthogonal to `W Omega_0`.

   The two producers state the same transfer table:
   - **Transfers:** the finite-box parity theorem (with the τ² constant of `C_N` unbounded), antisymmetry and evenness, the whole-set AQ statement, and the coefficient.
   - **Needs route-B constants, not done in AX1:** `K_2`, the `omega(W^2)` uniform constant, the AW2 enclosure, and every uniform-in-N τ² constant.
   - AW1's step "first-order parts of `c_{0}`, `c_{e_z}` vanish" is false in route B, and both say so.
10. **Itemized incidence and bindings: complete in both.** Every face is exported with its class, base and owner set. Both prove no double counting and reject duplicate-charging mutations. Both pin the `J_0'` packet with the contract sha256.

**Contract binding.** Both checkers verify the snapshot sha256 before parsing. Both read the target `1/2500000`, `J_0'`, the rationals, the reset, the incidence and the bounds from it.
- **Byte edit without a rehash.** Aborts both.
- **Coherent rehash of the target to `1/3000000`** (feasible, still met):
  - the **reverse** records `1/3000000`, which shows it reads the value;
  - the **forward** aborts ("acceptance target differs from preregistration"), because it pins the target to the acceptance text.

  A rehash requires a `check.py` edit, which `freeze.json` binds.

## Replays, closures and isolation

`replay_declared.py ax1` produces the same output under normal and `-O` Python. For both producers it:
- verifies the closure file by file (45 and 42 files);
- compares every premise snapshot with its repository source;
- replays under normal and `-O` Python into fresh external directories.

All four runs reproduce `output/` byte for byte, and `freeze.py verify` returns `verified` for both:

| Output | sha256 |
|---|---|
| forward `results.json` | `1d2e8fd9…810b` |
| reverse `results.json` | `5f46c950…4816` |

**Reads and scratch.**
- Both producers disclose their reads. These include protocol and style files outside `inputs/`: tools README and `freeze.py`, plus `forward/av1/check.py` and `reverse/av1/check.py` respectively. None carries premise weight.
- The forward disclosed a listing of `/tmp/claude-0/` that showed other agents' folder names; it opened none of them.
- The reverse disclosed an incidental `git status` exposure of four untracked file names under `experts/modern/assistant-2/`; it opened none of them.
- I audited scratch at the level of names and times only:
  - the private folders exist as disclosed;
  - the shared scratchpad root holds **no AX1 file** after the AX1 freeze;
  - its post-freeze files are AW2 manuscript work (I opened `nums.py` to confirm).
- **Timing.** The two closures were frozen 74 s apart (reverse 01:07:16Z, forward 01:08:30Z). The forward `report.md` was last written at 01:08:06Z, after the reverse `freeze.json`. The forward `check.py` was last written at 01:02:16Z, before the reverse `check.py`. The forward shows no reverse-specific construct, so isolation rests on disclosure and content (N11).

## Mutation harness

- Unmutated copies of both closures reproduce the frozen `results.json` exactly.
- **25 source edits abort** at the intended check. Both producers:
  - selected row relabelled omitted;
  - coefficient `-1/4`;
  - single groups dropped (`J=28`);
  - AM2 remainder zeroed;
  - flip set re-keyed;
  - `weak_coupling_claim:true`;
  - contract byte edit.

  Forward only:
  - gap-one reset;
  - `8/7` dropped;
  - outgoing stars only;
  - 49-face `t_1`;
  - rehashed target;
  - undeclared reverse report in inputs.

  Reverse only:
  - on-site gap one;
  - `a_1` pinned to 52;
  - fidelity headline halved;
  - triage in inputs;
  - forward report in inputs.
- **Three silent value edits run to completion** in the producer checkers:
  - forward, density form replaced by `2eps`;
  - forward, pair term `T'^2` dropped;
  - reverse, pair term `T'^2` dropped.

  My value validator rejects all three, and so would the cross-producer comparison (N5).

## Blocking issues

None.

## Non-blocking findings

**N1. Two valid `D'_ii` values.** The difference is the double-counted 16 faces (`|tau|/9` in `eps`) plus `~1e-16` from the final inequality. The gate should bind the forward rational and admit the reverse value as a labelled R-refinement.

**N2. The contract's `d_prime_note` is rounded the wrong way.** "`D'<=4.19×10^-7`" is infeasible: the threshold lies in `[41883,41884]/10^11` (forward `[4188,4189]/10^10`; reverse ≈4.18831e-7). All three agents found this. It is non-blocking because the target `4/10^7` is below the threshold. The note's "candidate 2–3×10^-8" is the 96-bound variant (forward 2.667e-8), not the exact tier.

**N3. The contract's "candidates 96 per factor and 168 for R"** are bounds (4×24 and 7×24). The exact counts are 52 and 88. Both producers reject "96 as exact".

**N4. Reverse independence is limited**, because the contract and `selection-ax1.md` state route B, `J'` and `J_0'` (item 8; contract review item 8; both producers).

**N5. Producer checkers do not pin the pair term.** Dropping `T'^2` runs silently in both. The forward also does not pin its density form. AX2's checker should read `D'_ii` from the AX1 gate as an exact rational and reject any recomputed or smaller value.

**N6. The forward's `density_part_of_D` label.** The exported value `2eps^2/(1+eps^2)` is an upper bound on `D-2eps=2eps^2(1-eps)/(1+eps^2)`, not an identity; the excess is ≈7.5e-25. `D` itself is exact.

**N7. The forward's mutation count wording.** "All 28 controls reject … 94 in total": 93 of the rejections sit in control checks and 1 (`E_minus_one_link`) sits in `flip_set_odd_all_classes`.

**N8. The reverse rejects `100|tau|` as a miscount** (one single group). The same number is a valid labelled refinement: `2·7·7+2`, because the single groups lie inside `R` with Haar mean 0. The admitted budget stays `102|tau|`.

**N9. Checklist classification differs** for the variance floor ("verbatim" in the reverse, "new constant" in the forward), and the forward's "five steps" groups 58 with 102. The substance is identical: the gap six is load-bearing.

**N10. Pre-registration vocabulary.** The symbolic triple `['tau/24','tau/24','tau/24']` in the frozen preregistration is covered by the `plan.json` vocabulary extension. That extension was recorded at 00:45:54Z, after the AX1 freeze, and the contract is unamended. The gate should record it as an accepted extension. Both checkers parse the triple and verify it.

**N11. Isolation is shown by disclosure and content, not by mechanism.** The near-simultaneous freezes and the post-freeze write time of the forward report are recorded above.

**N12. Scope of `uniform_wilson_claim:true`.** It means only that the model is the uniform fixed-spacing Kogut–Susskind model as labelled. A uniform Wilson-mean sign certificate is a claim exclusion. The gate should carry the scope string.

**N13. The `-tau` values are a replay** of the same `|tau|` formula, justified by the flip identity. They are not a second observation.

## Limitations

- **Scope.** Only the uniform Kogut–Susskind SU(2) model at fixed spacing and strong bare coupling (`g^4>=9.6×10^9`, `|tau|<=10^-8`), the whole-star-plus-single-group boxes (`N>=2`) and the cover `R`. Nothing here is weak coupling or continuum. The boxes are not identified with AL1's all-contained-plaquette boundary.
- **Upper certificates only.** There is no lower bound on `||rho_R-P_R||_1`, and no value or sign of `omega(W)` beyond `|omega(W)|<=D'` and the finite-box first-order coefficient.
- **AQ limits.** Uniform local closeness only: not uniqueness, whole-sequence convergence or a rate in N.
- **Inherited without re-proof** (re-applied with the new constants):
  - AM2's fixed point, majorant, exclusion and cutoff removal;
  - AV1's product split, anchored-norm tier, cutoff-vector removal and AQ passage;
  - AQ1's compactness and Nachtergaele–Sims dynamics;
  - AQ2's gauge averaging and Fourier gap;
  - AT4's reset and relative-unitary arguments;
  - the I1 dictionary.

  Kato, Peter–Weyl and Nachtergaele–Sims are cited, not machine-checked.
- **Not transferred:** `K_2`, the `omega(W^2)` constant, the AW2 enclosure, and every uniform-in-N τ² constant.
- **Fixtures** (qubit termination, quaternion holonomies, 3×3 compressions, the route-A `kappa=30` compression, the one-plaquette mean) are finite algebras, with `transfers_to_aq:false`.
- **Priority.** Scientific priority is unverified.

## Advice for AX2 (planning only)

1. **Bind** `D'_ii=2425369125199104794263242601250/167893028420061547330293754713793182097` from the AX1 gate, read as an exact rational from the hash-checked gate. With it, the window radius is `2(D'+D'^2)+51|tau|/pi≈1.9123e-7<=10^-6` (margin 5.23).
2. **Use `k'=51|tau|/4`** (`G` units) and the Haar reference correlation `e^{-3s}/4`.
3. **Reject** a recomputed or smaller `D'` (N5), the 4.19e-7 threshold, and any weak-coupling or continuum label.
4. **Treat the `-tau` case as the `U_E` image**, not a second observation.
