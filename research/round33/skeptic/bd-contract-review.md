# Round33 skeptic: pre-freeze review of the draft contracts BD1 and BD2

**Standing.** This is a prospective review by a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producers. It is not human peer review and not formal verification. Human project author: Hruday N M (BUNZEEY). It admits nothing, and it is not a research loop.

**Previews.** Every preview number (every computed moment, coefficient, endpoint, margin and constant) sits only in the section marked **Advisor only** at the end, and in `previews_recomputed` of `bd-contract-review.json`. No replacement text contains one; `build_review.py` checks this against a pattern list. Admitted gate values (1/144, `K_2'`, `98|tau|`, `56|tau||F|`, the AW1 face counts, the AZ2 series, `R=1/64`) appear where a replacement pins them. The exact rationals come from `fractions.Fraction` in my private scratch folder `/tmp/claude-0/skeptic-bd-private/`:
- `groups.py`: Haar moments by two routes (characters; Weyl integration by constant-term extraction, Z2 by summation) and the one-plaquette Rayleigh–Schrödinger series for all seven groups;
- `su5_check.py`: a floating diagonalization of the one-plaquette models, a labelled cross-check of the even parts only;
- `graph_rs.py`: the two-variable Rayleigh–Schrödinger table on the Round11 graph;
- `z_preview.py`: enclosures of `<z>` at `l1=l2` on the AZ2 grid;
- `geometry.py`: flip sets, the I1 incidences on `R`, the electric band endpoints and the 2+1D AM2 constants;
- `edits.py`, `scan.py`, `build_review.py`, `write_json.py`: replacement texts, scans, freezer runs on edited copies, and the JSON.

That folder is not evidence and not a premise. **No producer may receive it, this file or `bd-contract-review.json`.**

**Order of work, disclosed.**
- `z_preview.py` ran at 04:36Z, before I read §4 of `experts/modern/memo.md`. It imports a scratch copy of the AZ2 checker's primitives and its `certify` path, so it is a replay of AZ2 code with a new observable, not an independent route. My BD2 pre-comparison replay must use my own code for the certificate; I record this exposure now.
- `groups.py`, `graph_rs.py` and `geometry.py` ran at 04:44–04:48Z, after I had read the modern memo §4 and my own triage §(d). Both state several of the same values. Every overlapping value agrees, with one exception: the triage's formal electric second-order value counted four coupled faces per link, which is wrong for the zero-selected family (selected faces carry coefficient 0). My independence from the memo is limited to code.
- `groups.py` reproduces the AW1 one-plaquette fixture exactly (the SU(2) third-order coefficient `-5/11943936`), and `graph_rs.py` reproduces the AZ2 gate series exactly at `l1=l2`. These anchor both code paths to admitted values.

**Read.**
- The drafts `contracts/bd1.json` and `contracts/bd2.json` (commit 1833023; sha256 in the JSON), `advisor/selection-bd1.md`, `advisor/selection-bd2.md` and `advisor/plan.json`.
- My record: `triage.md` §(d) and the BD lines of the recommended plan; `loop2-review.md` P10–P11; `bc-contract-review.md`/`.json` as the format.
- The modern memo §4 and the historical memo §4.
- Gates: AW1, AW2, AZ2, AV1, AV2, AY1, AY2, BB2, AM2, AQ1.
- Reports, for the premise checks:
  - AW1 forward §§1, 3 and 4.2;
  - AZ2 forward §§1–2 and 9, and the AZ2 checker (its basis, kinetic, certify and Rayleigh–Schrödinger code, and its Round11 bindings);
  - AY1 forward §§5.3–5.5 (F11–F14);
  - AM2 forward (all), AQ1 forward (all), I1 forward (all);
  - the Round11 README (its coupling scope).
- The inherited control texts in `ba1.json`, `bb2.json` and `bc2.json`.
- Tools: `freeze_contract.py` and `phrase_scan.py`.

No BD production exists yet. I did not open `forward/bc1/` or `forward/bc2/`.

## Decision

- **BD1: `freeze_after_blocking_edits`.** It has 5 blocking issues and 15 field edits.
- **BD2: `freeze_after_blocking_edits`.** It has 6 blocking issues and 19 field edits.
- **plan.json: no blocking issue.** Every gate field of both drafts is already in `vocabulary.gate_fields`. Two non-blocking plan entries remain (P10, P12).
- **34 blocking field edits** in all. **`signoff: false`** until they are applied.

The drafts as committed pass `freeze_contract.py` on copies (20 and 28 premises). So do the copies with the blocking edits (20 and 33) and those with every edit (21 and 33). The control mirrors are equal, and every new control id has semantics. With every edit applied, no field and neither template produces a forbidden-phrase hit.

None of the blocking issues is a tool failure. The freezer's R3 check only asks for a non-empty `hamiltonian_terms` list, so it cannot see the two unnamed models (BD1-3, BD2-3). After the edits I need no further loop. I will check the frozen bytes against the JSON before my BD2 pre-comparison replay.

## The questions asked

### 1. Haar moments, all seven groups

I computed `E[W^k]`, k=1..5, by characters and by Weyl integration. The two routes agree exactly for every group, and SU(2) returns AW1's `0, 1/4, 0, 1/8`.
- **`E[W^3]=0`** for SU(2), SU(4), SU(5), U(1) and Z2.
- **`E[W^3]≠0`** for SU(3) and SO(3).
- Values are in the advisor-only section.

Contract item 3 is executable by both routes as written. Weyl integration for SU(5) at k=4 is a constant term in four variables with a 20-factor Vandermonde; it runs in under a second.

### 2. First-order coefficients under the frozen convention; is the convention unambiguous?

The formula `2(1/3)E[W^2]/(32 C_F)` equals the first-order Rayleigh–Schrödinger coefficient on `H_FG(G)` for every group. This is exact, because `W Omega_0` is an eigenvector of `32 C_2` at `32 C_F`. It reproduces **1/144 for SU(2)**.

The convention is unambiguous for SU(N), U(1) and SO(3):
- SU(N): `C_F=(N^2-1)/(2N)`, with the standard Casimir on every irrep.
- U(1): `C_2(n)=n^2`, with charge 1 as the Wilson representation, so `C_F=1`.
- SO(3): `C_2(l)=l(l+1)`, vector `C_F=2` and `W=Tr/3`. The trace of the vector representation is real, so `Re` is redundant but harmless.

**It is ambiguous for Z2 (blocking, BD1-1).**
- The text defines the electric term both as `8 C_2` and as "eigenvalue 0 on the even and 1 on the odd link state".
- The two readings differ by a factor 8 in the face energy, and so in the Z2 coefficient.
- The modern memo uses a third normalization, `1 - sigma^x`.
- Two correct routes could therefore disagree on the Z2 cell, and `frozen_convention_used` cannot say which of them used "another normalization".
- My triage's own parenthetical ("with the electric term normalized to 1 on the odd state") is the likely origin of the ambiguous wording.
- The replacement freezes `C_2=1` on the odd state, the reading that keeps `8 C_2` per link for every group.

**The creation sign is not stated.** `c^(1)=-(tau/3)/(32 C_F) sum W_f Omega_0` together with `omega(W)=+2(tau/3)E[W^2]/(32C_F)` holds only under the AM2/AV1 sign `psi=e^{-C}Omega_0`, where `omega(W)=-2Re(W Omega_0, c^(1))`. AW1 recorded exactly this wording defect, so the replacement states the sign.

### 3. The SU(3) and SO(3) obstruction coefficients

**Both are nonzero under `H_FG(G)=32C_2-(tau/3)W`.** Because `R W Omega_0 = W/(32C_F)` exactly, they have closed forms:
- the first-order derivative of `omega(W^2)` is `(2/3)E[W^3]/(32C_F)`;
- the second-order coefficient of `omega(W)` is `E[W^3]/(3(32C_F)^2)`.

My Rayleigh–Schrödinger series agree with both closed forms. The even part of `omega(W)` from a floating diagonalization agrees with the exact even terms to about 1e-13 relative, which is a labelled cross-check.

**The model is well defined for all seven groups:**
- **U(1):** `32n^2-(tau/3)cos theta` on `L^2(U(1))`, with compact resolvent and a simple ground state at `tau=0` with gap 32.
- **Z2:** a two-level model.
- **SO(3):** `W` has a diagonal part (`W chi_l=(chi_{l-1}+chi_l+chi_{l+1})/3`), which changes nothing in the argument.

### 4. SU(5): parity without flip, and an undefined cell (blocking, BD1-2)

SU(5) has no central `-1`, because its centre acts by fifth roots of unity. It does have `E[W^3]=0`, so the first-order parity transfers. By the Z_5 grading, the two SU(3)/SO(3) obstruction coefficients vanish identically for SU(5).

The draft still makes an SU(5) obstruction cell mandatory: `flip_criterion_central_minus_one` says "a group without such z receives no flip claim and its obstruction cell is mandatory". It does not define that cell. The template's "transfers exactly" also asserts that the flip lemma fails for SU(5), and the missing central element does not prove that, since another unitary could reverse `W`.

The exact counterexample is the **fourth-order coefficient of `omega(W)` on `H_FG(SU(5))`**, the first possible nonzero even-order coefficient under the Z_5 grading. My exact value is nonzero, and the floating even part agrees.

**Fix:**
- define the cell in `required[3]`;
- add the control `su5_flip_obstruction_fourth_order`;
- rewrite the flip semantics so that an obstruction is always an exhibited counterexample;
- name the cell in the acceptance text and the template.

SU(4) shows the other direction: the floating even part of `omega(W)` is exactly zero.

### 5. The area-parity corollary for the limit: does it follow from AW1 plus BB2 at each sign?

**Yes, with the stated conditions.** The chain:
1. AW1 F09–F10: `U_E H_N(tau) U_E^* = H_N(-tau)` in every open centered whole-star box and every cutoff at `kappa=0`, with pointwise covariance of the untruncated and cutoff F1 ground vectors (AM2 uniqueness).
2. `U_E W_C U_E^* = (-1)^{|C∩E|} W_C`.
3. `|C∩E|` is congruent mod 2 to the plaquette count of any spanning surface. The count is well defined because every closed plaquette surface in a box is a sum of cube boundaries, and so has an even number of plaquettes.
4. BB2 item 1 gives whole-sequence trace-norm convergence on a finite complete-factor region containing the links of C, at each sign. The box identity therefore passes to the limit pointwise.

AW1's set-level AQ statement is superseded by BB2's whole-sequence limit; no common subsequence is needed.

Two refinements (non-blocking edit to `required[5]`):
- Evenness of the Casimirs in the limit needs their bounded spectral cutoffs, which commute with `U_E`, and then the monotone limit, because trace-norm convergence does not pass an unbounded expectation.
- The surface-independence of `A(C)` mod 2 should be proved, not assumed.

My enumeration checks the parity rule on rectangles up to 3×3 in all planes and offsets, on an L-shaped loop and on a bent two-plane loop.

**The template overclaims (blocking, BD1-4).** "In every box" includes:
- periodic boxes with an odd side, which item 5 itself records as an obstruction;
- boxes at `kappa≠0`, where AW1 gives no antisymmetry;
- F2 and literal vertex boxes, which are outside AW1's admitted flip lemma.

"Enclosed area" is undefined for a non-planar loop. The replacement template names the zero-selected family at `kappa=0` and the whole-star boxes, speaks of "any spanning surface", excludes odd periodic boxes and adds the SU(5) cell.

### 6. Where do the flip and parity transfers live? (blocking, BD1-3)

Criteria A and B transfer statements that AW1 proves on SU(2) whole-star boxes. For the other groups, however:
- the draft names only one-plaquette models;
- the gate scope says "flip-set boxes" with no Hamiltonian;
- R3's intent is that every coupling of every finite model is named.

Without AM2 for G, each box needs a unique ground state from Kato perturbation theory, with a box-dependent radius, and the contract must say so.

The complex Wilson representations (U(1), SU(N≥3)) raise a further point. The gauge-invariant level at `32C_F` also contains `Im chi(U_g) Omega_0`, which the SU(2) argument never met. Zero first-order splitting must be shown on the whole level. It holds because `E[W^3]=0` forces every cubic moment `E[chi^a conj(chi)^b]` with a+b=3 to vanish: these moments are nonnegative integers.

The replacements do the following:
- name the group-G whole-star box models `H^G_N` in `model` and `hamiltonian_terms`;
- restate criteria A and B on those models;
- make the gate scope name the groups.

### 7. BD2: are total orders through 4 at D∈{6,8} reachable with zero truncation error?

**Yes.** `psi_{ij}` lies in `P_{i+j}`, so every coefficient through total order 4 (I ran order 5) is exact at `D=6`, and the D=6 and D=8 tables are identical. The `l1=l2` restriction reproduces the AZ2 gate series of `<W_1>` and the second-order `<z>`. The table shows:
- `<W_1>` odd in `l1` and even in `l2`;
- `<z>` odd in each coupling;
- `<C_shared>` even in each.

The AZ2 one-face/two-face difference is the `l1 l2^2` coefficient. The Round11 solver API requires `lambda>=0`. That is irrelevant for the coefficients, and the negative grid points are handled by the flips as in AZ2.

**One flip cannot give both parities (blocking, BD2-5).** The flip of a non-shared link of face 1 reverses `W_1` and `z` and fixes `W_2`, so it proves oddness in `l1` only. Evenness in `l2` needs the flip of a non-shared link of face 2. The drafted control prescribes the face-1 flip for both.

### 8. The width target 1/10^10 for `<z>`

**The target is met with an enormous margin.** I replayed the AZ2 certificate with `z` as the observable; the Ritz vector is the same, `||z||<=1`, and so the absolute half-width is AZ2's own. Results:
- every enclosure excludes 0 and is positive at both signs, since `<z>` is even;
- the D=8 enclosure lies inside the D=6 one at all twelve points;
- the relative width at D=8 lies below the target by a factor of several million, and even D=6 meets it.

The margin of at least 2 holds, but the threshold discriminates nothing. Either relabel it as a format threshold (non-blocking edit to the target note, which also defines "relative width" and makes nesting an observed check) or tighten it. The choice of target is the advisor's; a candidate is in the advisor-only section.

### 9. The electric band: both endpoints from admitted premises (blocking, BD2-2)

**Lower endpoint.** Three steps:
1. `h_R >= 6 Q_R`, from I1 (free Casimir gap 6δ) and the zero-selected Haar reference (AY1/AY2 model).
2. The pure-reference Fuchs–van de Graaf inequality, `Tr(Q_R rho) >= ((1/2)||rho-P_R||_1)^2`. In the record it is only cited (AY1 limitations), but the pure case is three lines: the rank-one formula plus convexity. It should be proved inline.
3. A lower bound on `||rho_R-P_R||_1`.
   - For the limit, it comes from AY2 item (2) for every subsequential limit, identified with the limit by BB2 items 2–3.
   - **For finite F1 and F2 boxes no gate states it.** AY1 and AY2 state the ball and the two-sided distance only for subsequential limits.
   - The per-box statement is AY1 forward F11–F14: uniform in N, in the cutoff and in both families, and passed to the untruncated ground by AV1 F22. It is a reviewed step of the admitted proof, but the AY1 forward report is not a BD2 premise.

**Upper endpoint.**
- AQ1 HNM-AQ1.1 with the 7 incident anchors of R gives `98|tau|`, which the AY1 gate states for F2.
- The AQ1 gate itself states the generic `56|tau||F|`, which is `112|tau|` on R. That is a different valid value, and with exact endpoints required the contract must pin one.
- The budget holds for untruncated F1 and F2 boxes.
- It passes to the limit only by lower semicontinuity of the monotone cutoff limit under trace-norm convergence on R. No gate states this step; it is elementary, and the contract must name it.

The scaling brackets hold: `band_lower` falls inside `[9500,10500]` and `band_upper` is exactly 100. The formal second-order value must count each link's omitted-face incidence, which is 2, 3 or 4 because selected faces carry coefficient 0. My triage used 4 for every link.

### 10. The 1×2 loop (blocking, BD2-4)

"Two adjacent faces of the original loop's plane" does not fix the rectangle. The template also says the 1×2 mean "vanishes at first order" in the family. For the limit that claim needs a uniform remainder, and the draft names none.

Take the rectangle made of W and the xz face at the fine point `e_x`. All six of its links are owned by R, so `W_{1x2}` lies in `B(H_R)`. Then:
- `Tr(P_R W_{1x2}) = Tr(rho^(1)_R W_{1x2}) = 0` by single occurrence;
- the AY1 ball per box and the AY1/AY2 gate ball for every limit give **`|omega(W_{1x2})| <= K_2' tau^2` for every box and the limit**;
- my triage's "recounted cover R'" is unnecessary.

This is an admitted-premise consequence that the draft omits. It carries no sign, and the formal coefficient stays formal. My formal coefficient agrees with the graph `<z>` coefficient under the AZ2 dictionary `tau_FG=tau/24`. Evenness follows as in question 5; the F2 boxes should not be claimed (non-blocking).

### 11. 2+1D: is the AM2 derivation for p=3 feasible from the AM2 report alone, and is the factorization well posed? (blocking, BD2-3)

**Feasible.** AM2 §2 states its counting for general p:
- `2^p` output supports;
- `p||c||_a` per collection;
- `(p+1)/|I_l|`;
- termination for `k>2p`.

Hence `L_k(3)=8·6^k(1+4k/3)`, `G_3(t)=8e^{6t}(1+8t)`, `G_3'(t)=8e^{6t}(14+48t)` and termination at order 6. I checked that the general-p formula reproduces AM2's `16·8^k(1+5k/4)` at p=4, and `148/7` and `352` with `e^{1/8}<8/7`. The report has no rational bound for `e^{3/32}`, so the producer needs its own directed enclosure.

**Well posed for the constants, but not frozen.** The declared factorization is complete: each link has its tail as owner, and each face has owner set `{p,p+e_x,p+e_y}`. Four things are open:
- **The Hamiltonian terms are not named.**
- **The radius** is "declared" in `required[4]` but appears nowhere.
- **The on-site normalization** is open. AM2 uses `h_x>=Q_x`; with the free gap 6 instead, the cap scales by 6.
- **The cap depends on the radius.** At the radius that is optimal for the self-map alone, the exclusion condition `2JG_3'(R)<1` fails, by an exact identity. The cap must therefore be defined by both conditions at a frozen radius.

The draft also leaves open whether a finite-volume 2+1D gap theorem is claimed. It should not be: that theorem needs a 2D finite-volume prescription and AM2 §§4–6 re-verified. The replacement makes it an obligation row. The AV2 window-kernel constants are dimension-free, as drafted.

### 12. Premise completeness

- **BD2 (blocking, BD2-1).** The graph and everything AZ2 inherits without re-proof are Round11 results:
  - the Gauss reduction (Q1–Q3);
  - the kinetic operator (K1–K5);
  - the spectrum and tail threshold (E1–E4);
  - Theorem F.

  The AZ2 checker, a declared BD2 premise, binds these to four Round11 files and refuses to run without them: `research/round11/README.md`, `advisor/advisor.md`, `solver/README.md` and `solver/two_plaquette.py`. None of the four is a BD2 premise.
- **BD2 (inside BD2-2).** `research/round32/forward/ay1/report.md` is needed for the finite-box lower endpoint.
- **BD1 (non-blocking).** The ledger's dictionary column cites `tau=96/g^4` and `alpha=g^2/(2a)`, which are AZ1 (and AX1/AX2) gate statements. Add `research/round32/advisor/az1-gate.json`.
- **External theorems.** None needs a committed excerpt:
  - Fuchs–van de Graaf is proved inline in its pure case;
  - Kato, Peter–Weyl, Weyl integration and the maximum-principle/Banach steps are standard and already accepted in the record.

### 13. Controls: mirror and semantics coverage

- The mirrors are equal, with no duplicates, and every new id has semantics.
- The nine inherited ids are defined in `ba1.json` (eight also in `ba2.json`), which is a declared premise of both drafts.
- **`tier_mixing_rejected` (blocking, BD1-5 and BD2-6).**
  - BA1 defines it with the routes `{weighted_norm, analytic_disc}` and the tiers `{crude_majorant, exact_first_order}`; BB2 defines it with the hypothesis source `bb1_frozen_targets`.
  - Both conflict with BD1's `route_of_computation` rule and with BD2's `first_order_distance_from_product`.
  - BD2's `tier_label_rule` also calls graph coefficients of orders two to four `exact_first_order`.
  - Each draft gets its own text.
- **Non-blocking.**
  - `changed_model_relabelled`: the BA1 text rejects "other-group, 2D or finite-graph" results, which are these loops' subjects, so it needs a BD text.
  - `parameters_declare_metric_weights_window`: the BA1 text requires `d_X` and `N_0`, which neither draft has.

### 14. R3, R4 and gate fields

- **R3.** BD1's box models and BD2's 2+1D model are unnamed (blocking, inside BD1-3 and BD2-3). BD2's admitted Z^3 family gets a named entry (non-blocking).
- **R4.** `state_provenance`, `clock` and `error_terms_itemized` of both drafts are unique across all Round32 and Round33 contracts. None is copied across families.
- **Gate fields** are all in the plan vocabulary. Tiers and sub-labels pass R10.
- BD1's `sign_certified_finite_graph` does not apply, because BD1 certifies no sign (non-blocking).

### 15. Wording, templates and the rate-range lesson

- **Placeholders:** none in the drafts. My first convention text contained `<W Omega_0, c^(1)>`, which R1 rejects; the replacement uses `(u, v)`.
- **Forbidden phrases:**
  - Neither template hits, with or without removal.
  - BD1 hits only in the negated `no_transfer_called_prediction`.
  - BD2's `claim_exclusions[1]`, which names the excluded area-law and string-tension statements without a negation word, scans as affirmative. A gate copying it into its limitations would fail `record_gate.py`, so it is reworded (non-blocking).
- **Rate-range lesson:** neither template has a rate. BD2's `rate_range_stated` text says "rate claim" twice, which is the unqualified form the plan forbids (non-blocking replacement).
- **Templates:** each is one literal span a producer can quote, with no slot.
  - Both assert every item, so each gets a limited-outcome frame in `gate_fields_rule` (non-blocking).
  - BD1's template needed the substantive fix of BD1-4.

### 16. Scaling brackets

- **BD1:** the brackets describe the terms, not the coefficients. A coefficient is independent of tau; the first-order term is linear and the second-order term quadratic. The SU(5) quartic term needs its own bracket (non-blocking).
- **BD2:** `band_lower`, `band_upper` and `z3_formal` pass (question 9).

### 17. Acceptance

- **BD1:** the acceptance text now names the SU(5) cell, the named models, the whole-star boxes and `kappa=0` (inside BD1-2).
- **BD2:** the non-blocking replacement:
  - ties acceptance to the frozen band premises and the `W_{1x2}` bound;
  - adds the 2+1D obligation;
  - removes the dependence on observed nesting.
- The limited and insufficient branches of both drafts are sound.

## Blocking issues (34 field edits; exact texts in the JSON)

**BD1 (5 issues, 15 edits):**
- **BD1-1. Z2 normalization and the creation sign.** `parameters.convention`.
- **BD1-2. The SU(5) cell.** Edits:
  - `required[3]`;
  - `flip_criterion_central_minus_one`;
  - the new control `su5_flip_obstruction_fourth_order` in `controls`, in the mirror and in the semantics;
  - `acceptance.accepted_within_scope`.
- **BD1-3. Group box models.** Edits:
  - `model`;
  - two `hamiltonian_terms` entries;
  - `required[0]` and `required[1]`, the latter covering the complex level;
  - `flip_transfer_scope`.
- **BD1-4. The template.** `mandatory_sentence_template`.
- **BD1-5. Tier semantics.** `tier_mixing_rejected`.

**BD2 (6 issues, 19 edits):**
- **BD2-1. Round11 premises.** Four `shared_premises` appends.
- **BD2-2. Electric band.** Edits:
  - `parameters.electric_band`;
  - `required[3]`;
  - the AY1 forward report as a premise;
  - `unbounded_observable_handled`.
- **BD2-3. The 2+1D model.** Edits:
  - `parameters.dimension_2p1`;
  - two `hamiltonian_terms` entries;
  - `required[4]`.
- **BD2-4. The 1×2 rectangle and its limit bound.** Edits:
  - `parameters.z3_1x2`;
  - `required[2]`;
  - `formal_coefficient_labelled`.
- **BD2-5. Two flips.** `required[0]` and `independent_coupling_flip`.
- **BD2-6. Tier semantics.** `tier_mixing_rejected` and `tier_label_rule`.

## Non-blocking (21 entries in the JSON)

**BD1:**
- `parameters.flip_sets`: what the 24-link factor check verifies.
- `required[5]`: the surface independence, the untruncated vectors and Casimirs in the limit.
- `sub_labels_allowed`.
- The scaling brackets.
- The AZ1 gate as a premise.
- `claim_exclusions`: nonzero `kappa`, odd periodic boxes, F2 and literal boxes.
- BD texts for `changed_model_relabelled` and `parameters_declare_metric_weights_window`.
- `gate_fields_rule`: a limited-outcome frame, and the scope names the groups found.

**BD2:**
- `graph_grid`: the 7×7 grid is used by no item.
- `target.note`: the relative-width definition, a format threshold, nesting observed.
- `rate_range_stated` wording.
- `claim_exclusions[1]` wording.
- `evenness_from_flip`: whole-star F1 boxes.
- A Z^3 `hamiltonian_terms` entry.
- BD texts for `changed_model_relabelled` and `parameters_declare_metric_weights_window`.
- `gate_fields_rule`: a limited-outcome frame.
- The acceptance text.

**plan.json:**
- `subrounds[3].selection_note_paths` (P12).
- `subrounds[3].loop_ownership` (P10): BD1 owns `E_2`, BD2 the 2+1D recount.
- Record the plan sha256 at the freeze (P5).

## Against my own record

- **P10 is met in part.** BD1 is paired with genuinely different routes, the SU(3) and SO(3) cells are mandatory, the convention is frozen (after BD1-1), and 1/144 and `96/g^4` are never transferred. The plan does not yet say which loop owns the 2D flip set (non-blocking plan entry).
- **P11 is met.** BD2 is single+skeptic, the Z^3 1×2 coefficient is labelled formal, the electric energy keeps its unbounded-observable obstruction, and the graph carries an FG model id and `hamiltonian_terms`. The calculators are a presentation deliverable outside BD2.
- **Triage §(d) errors, corrected here:**
  - It listed no SU(5) row, and neither did P10. SU(5) is the one group where flip and parity separate, and the draft inherited the gap (BD1-2).
  - Its Z2 parenthetical is the likely source of BD1-1.
  - Its formal electric value counted four coupled faces per link.
  - Its 1×2 bound asked for a recounted cover that is unnecessary for the rectangle inside R.
  - Its band lower endpoint subtracted `K_2' tau^2` from the half-distance, not the valid `K_2' tau^2/2`. The triage form is valid but looser.
- **BD2 replay exposure.** My BD2 preview reuses AZ2 code (see Order of work). The pre-comparison replay the contract requires must be my own code; this file does not count as it.

---

## Advisor only: previews (not for producers or replay inputs)

Exact Fractions from the scripts above; decimals are truncated. `tau` coefficients are for `H_FG(G)=32C_2-(tau/3)W` in delta units under the convention with Z2 `C_2(odd)=1`.

**Group cells.**

| group | `E[W]..E[W^4]` | `E[W^5]` | first-order coeff. | `d omega(W^2)/dtau` | 2nd-order `omega(W)` | 4th-order `omega(W)` |
|---|---|---|---|---|---|---|
| SU(2) | 0, 1/4, 0, 1/8 | 0 | 1/144 | 0 | 0 | 0 |
| SU(3) | 0, 1/18, 1/108, 1/108 | 5/1296 | 1/1152 | 1/6912 | 1/589824 | −77/9393093476352 |
| SU(4) | 0, 1/32, 0, 7/2048 | 0 | 1/2880 | 0 | 0 | 0 |
| SU(5) | 0, 1/50, 0, 3/2500 | 1/50000 | 1/5760 | 0 | 0 | **1/63403380965376** (≈1.577e-14) |
| U(1) | 0, 1/2, 0, 3/8 | 0 | 1/96 | 0 | 0 | 0 |
| Z2 | 0, 1, 0, 1 | 0 | 1/48 | 0 | 0 | 0 |
| SO(3) | 0, 1/9, 1/27, 1/27 | 2/81 | 1/864 | 1/2592 | 1/331776 | −55/2972033482752 |

- **Z2 under the other reading** ("electric term 1 on the odd state"): first-order 1/6.
- **SU(2) third-order coefficient:** −5/11943936, equal to the AW1 fixture.
- **Floating cross-check of the even part `(omega(tau)+omega(-tau))/2` against the exact even terms:**
  - SU(5) at `tau=1`: 1.57721e-14 against 1.57720e-14;
  - SU(5) at `tau=2`: 2.52352e-13 against 2.52352e-13;
  - SU(3) and SO(3): agreement to about 13 digits;
  - SU(4): exactly 0.

**Graph (Round11, `H=K-l1 W_1-l2 W_2`, alpha units).**
- **Tables identical at D=6 and D=8.**
- **`<W_1>`:** `l1/6 - (5/864)l1^3 + (1/4212)l1 l2^2 + (289/829440)l1^5 - (22285/756946944)l1^3 l2^2 - (22285/1513893888)l1 l2^4`.
- **`<z>`:** `(7/216)l1 l2 - (349/303264)(l1^3 l2 + l1 l2^3)`.
- **`<C_shared>`:** `(l1^2+l2^2)/48 - (5/4608)(l1^4+l2^4) - (49/438048)l1^2 l2^2`.
- **At `l1=l2`:**
  - `<W_1>`: 1/6, −187/33696, 767713/2523156480 (the AZ2 gate);
  - `<z>`: 7/216, then −349/151632;
  - `<C_shared>`: 1/24, then −7997/3504384.

**`<z>` enclosures at `l1=l2`** (the AZ2 certificate with observable z; every one excludes 0 and is positive at both signs; D=8 inside D=6 everywhere):

| `|l|` | D=6 relative width | D=8 relative width | D=8 margin against 1/10^10 |
|---|---|---|---|
| 1/1000 | 6.79e-22 | 1.74e-31 | 5.8e20 |
| 1/100 | 6.81e-17 | 1.74e-24 | 5.7e13 |
| 1/10 | 7.02e-12 | 1.80e-17 | **5.57e6** (binding) |

- D=6 would meet the target with margin 14.2.
- A target of 1/10^15 at D=8 would keep a margin of about 55.7 at the binding point; 1/10^16 would keep about 5.6.

**Z^3 1×2 loop.**
- **Formal second-order coefficient:** 7/124416. It is `2·2(1/3)(1/72)(1/16)/36 + 2(1/72)^2(1/16)`, with rectangle energy 36δ, and it equals `(7/216)/24^2`.
- **Certified bound at the cap:** `|omega(W_{1x2})| <= K_2'·10^-16 ≈ 1.3418e-12`. That is about 2.4e8 times the formal value at the cap, so it carries no sign.

**Electric band on R at `|tau|=10^-8`** (δ units):
- **Lower endpoint:** `(3/2)L^2`, with L the AY2 exact lower end (reproduced from `sqrt10_lo|tau|/72 - K_2' tau^2`), about **2.8759e-19**. The exact rational is in the JSON.
- **Upper endpoint:** `98|tau| = 49/50000000` (9.8e-7). The AQ1-gate alternative is `7/6250000`.
- **`tau -> tau/100` ratios:** lower about 9939.60 (inside `[9500,10500]`); upper exactly 100.
- **Formal second order:**
  - `sum_e n_e = 168`, since per-link incidences are 2 (4 links), 3 (16) and 4 (28);
  - `omega(h_R) ≈ (7/144)tau^2 ≈ 4.86e-18`;
  - the triage's four faces per link would give `tau^2/18`.
- **AY1 pins reproduced:** 82 omitted faces meet R, 10 have owner set exactly R.

**Flip sets.**
- **N=2 box:** 3000 links; 2335 plaquettes, of which 1082 are met once and 1253 three times; 1344 retained whole-star faces. All four counts equal AW1's.
- **N=3 box:** 6909 plaquettes, all met oddly.
- **Per factor:** 16 E-links if `b_z` is even, 8 if odd. E_3 is not invariant under an odd coarse z shift.
- **E_2:** exactly one link per plaquette at N=2,3,4.
- **Tori:** a 4×3 torus has 4 even seam plaquettes; 4×4 has none.

**2+1D AM2 (p=3, R=1/64, unit on-site gap).**
- **Constants:** `G_3(R) ≈ 9.88457`, `G_3'(R) ≈ 129.598`, per-site sum `J=|tau|` (three faces per site at `|tau|/3`).
- **Cap:** self-map about 1.5807e-3 (directed), exclusion about 3.858e-3, so the cap is about **1.5807e-3**.
- **With the crude bound `e^{3/32}<32/29`:** 29/18432 (≈1.5734e-3).
- **Alternatives:**
  - with the free gap 6, about 9.48e-3;
  - at the self-map-optimal radius (≈0.0948) the self-map cap is about 3.816e-3, but `2JG_3'` equals exactly 2 there. It is `(2+16R)/(1+8R)` with `48R^2=1-6R`, so the exclusion fails.
- **3+1D check:** `G(1/64) < 148/7` and `G'(1/64) < 352` are reproduced from the general-p formula.

No result here is a Round33 finding, a loop or a fraction of the continuum problem. The four-dimensional Yang–Mills existence and mass-gap problem remains open.
