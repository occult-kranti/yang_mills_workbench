# AZ2 skeptical review (post-comparison, single+skeptic, finite graph)

**Verdict: accepted_within_scope.** Sub-label `sign_certified_finite_graph`; secondary sub-label `static_not_dynamic`. There are **no blocking issues**.

The single forward producer carries out contract items 1–6 on a finite model that it names exactly. That model is **`H_FG = K - tau_FG (W_1 + W_2)`**, with both faces coupled equally. My pre-comparison package read the other admissible model, with the second face uncoupled. The contract text fixes neither, and the producer disclosed its choice, so the difference is a contract wording defect, not a blocking issue. The gate must name the two-face model.

In the computed model, every exact value the producer exports agrees with my own recomputation. These include:
- the derivative `[1/6, 1/6]` at both cutoffs;
- the free reference `[0, 0]`;
- the zero second-order Wilson coefficient;
- `E_2 = -1/6` and the third-order `-187/33696`, which my pre-comparison package had recorded as the "both faces" side value;
- the tails 45/69 and the per-channel thresholds;
- the leading-order omitted residual;
- all twelve enclosures, each of which contains my independent tighter enclosure.

**Admission basis.** AZ2 has one producer (`producers=["forward"]`, `direction: single+skeptic`, `single_direction_independent_replay: true`). Admission rests on:
- that producer;
- my pre-comparison derivation and replay, written from the contract and frozen without opening any producer file;
- this review.

**Standing.** I am a model-agent skeptic with correlated ancestry: I share a model family with the advisor, the lenses and the producer. My loop-2 response set two conditions for this loop: "the Round11 two-plaquette graph or smaller" and "coefficients computed algebraically, never fitted". My triage wrote the finite-graph labelling. The contract, `selection-az2.md` and `update-4.md` already print `1/6`, the dimensions and the tails. The agreement below is replay and re-derivation, not independent discovery, human peer review or formal verification. Human project author: Hruday N M (BUNZEEY).

**My pre-comparison package is unchanged.** It consists of:
- `az2-contract-review.md`;
- `az2-independent-derivation.md`;
- `az2_check.py`: 81 checks, 23 controls, 75 rejected mutations;
- `az2-independent/results.json` (sha256 `30917f54…ea0f`).

Its hashes match `az2-independent-freeze.json` (sha256 `33f6077a…7251`). The committed bytes equal the working tree, and a fresh replay reproduces the results byte for byte.

**Commit order.** The skeptic commit comes first:

| Event | Time (UTC) |
|---|---|
| Contract frozen, with the 28 input snapshots (`32de53b`) | 04:29:40 |
| My scratch, first file | 04:41:37 |
| Producer scratch, first file | 04:46:16 |
| Producer Arb preview script / output | 05:14:02 / 05:18:08 |
| My checker last written (final replays followed) | 05:17:07 |
| Producer `check.py` / report last written | 05:27:23 / 05:27:39 |
| Producer output | 05:28:27 |
| My freeze (disclosure re-freeze) | 05:29:35 |
| Producer freeze | 05:29:49 |
| **My pre-comparison commit (`4bae265`)** | **05:30:10** |
| **Producer commit (`dc817d8`)** | **05:33:11** |

The two packages were developed at the same time.
- **The producer's side.** It declares no read under `research/round32/skeptic/`, and its 28 inputs hold no `skeptic/az2*` file.
- **My side.** Before my freeze I saw only producer file names, and I disclosed them. Isolation rests on disclosure, name-only exposure, content and commit order.
- **The model split supports isolation.** The two packages chose different face couplings, which is itself evidence that neither read the other.

**This review adds:**
- `az2_postreview_check.py`, with 28 exact checks and 27 source-edit runs on copies of the producer closure. The copies sit outside the checkout and always run under `python -B`:
  - 1 unmutated copy reproduces `output/` byte for byte;
  - 20 weakenings, one per contract control, each abort at that control;
  - 6 semantic edits: 5 abort, and 1 completes by design.

  Its own validator also refuses 18 damaged packets.
- `az2-postreview/results.json` (sha256 `26c55d5d…4ccd`), byte-identical under `-B` and `-B -O`. Each run takes about 4.5 minutes.
- `az2-replays.json`. It uses the unchanged `replay_declared.py`: two byte-identical producer replays of about 41 s each, and `freeze.py verify` run twice.

## The model question, resolved

**What each package computed.**
- **The producer:** `H_FG = K - tau_FG (W_1 + W_2) = H_R11(alpha=1, lambda1=lambda2=tau_FG, rho=1) - 2 tau_FG`. Both faces carry the same coupling. The observable is `<W_1>`, the square containing `h1, vL, h3, vM`.
- **My pre-comparison:** `H_FG = K - tau_FG W_1`, with the second face uncoupled. I read this from the dictionary parenthetical.

**What the contract fixes: neither model.**
- The model string names one coupling, "coupling tau_FG in a declared grid", but not which faces carry it. `lambda2` appears nowhere.
- `parameters.observable` names the observable ("`<W>` of one square"), not the coupling.
- The only face wording sits in the dictionary: "(every face coefficient nu=alpha*tau/24 in the Z^3 model; the two-plaquette graph's own coupling multiplies one face)". That sentence explains the normalization, `tau_FG` ↔ one face coefficient `alpha tau/24`. It reads equally well as "multiplies one face each".
- The Round11 defaults (`lambda1 = lambda2 = 0`) decide nothing.
- The shared premise `experts/modern/loop2-response.md` specifies `H/alpha = K + kappa_1(1-x) + kappa_2(1-y)`, with both faces coupled.
- The Z^3 uniform model that the dictionary quotes couples every face.

So the producer's two-face reading is at least as well supported as mine. My one-face reading remains admissible.

**Disclosure.** The producer names its Hamiltonian in:
- the verdict, and §1 of its report;
- `results.model.hamiltonian`, `results.headline.hamiltonian` and `round11_equivalence`;
- its `validate_model` control.

It also computes the one-face `E_2 = -1/12` as a labelled control value. There is no undisclosed model change. By the coordinator's rule this is **not blocking**. It is a contract wording defect (below, W-A), and the gate records the model exactly.

**The exact coefficients identify the model.** This review recomputes the untruncated Rayleigh–Schrödinger series in Round11 monomials:

| | `a_1` | `a_2` | `a_3` | `a_5` | `E_2` | `E_4` |
|---|---|---|---|---|---|---|
| two faces (producer, recomputed here) | 1/6 | 0 | **-187/33696** | 767713/2523156480 | **-1/6** | 187/67392 |
| one face (my pre-comparison) | 1/6 | 0 | -5/864 | 289/829440 | -1/12 | 5/3456 |

The producer's second-order values `<W_1^2>: 7/576`, `<W_1 W_2>: 79/2808` and `<z>: 7/216` are recomputed exactly as well.

**What holds in both models:**
- the derivative `1/6`;
- the zero second-order coefficient of `<W>` (the centre flip on a U link in one model, on `vM` in the other);
- the dictionary `1/6 <-> 1/144`;
- the own free reference `0`;
- the dimensions, tails and thresholds.

**What holds only in the one-face model.** My pre-comparison spectator identity: the second square as spectator, making the model AW1's one-plaquette fixture. In the admitted two-face model the second square is active. The model differs from the AW1 fixture at third order:
- `-187/33696` instead of `-5/864`;
- through the dictionary, `-187/(33696·24^3)` against AW1's `-5/11943936`.

It is therefore a genuinely different finite model beyond first order.

**The second-square shift is certified.**
- The difference `<W_1>_two-face - <W_1>_one-face` is `tau_FG^3/4212 + O(tau_FG^5)` exactly, since `-187/33696 + 5/864 = 1/4212`.
- It is certified from my two-face enclosures together with my frozen one-face enclosures. At D=8 the midpoints are 2.3697588999e-7, 2.3741248805e-10 and 2.3741685992e-13 at `+1/10`, `+1/100` and `+1/1000`. At every point the sign is `sign(tau_FG)`.
- The producer's twelve enclosures and my twelve pre-comparison enclosures are **disjoint** at every point. That is why "the twelve enclosures intersecting yours" holds only against my post-review two-face enclosures.

## What is admitted, with quantifiers

**Model.** `FG(two-plaquette, D in {6,8}, tau_FG grid, I1.5, gauge-invariant)`:
- the Round11 open two-square patch: 6 vertices, 7 links, 6 Gauss constraints;
- the gauge-invariant sector;
- `H_FG = K - tau_FG (W_1 + W_2)` in alpha units, with `K` the sum of the seven link Casimirs (`rho = 1`);
- the I1.5 sign: the first-order mean is positive for positive `tau_FG`;
- the basis: trace monomials of total degree `D`, with dimensions 84 and 165;
- the grid `tau_FG` in `{±1/1000, ±1/100, ±1/10}`.

Flags: `model_is_finite_graph: true`, `transfers_to_aq: false`, `fg_coefficients_fitted: false`.

**1. Derivative and free reference.**
- `d<W_1>/dtau_FG` at 0 is exactly `1/6` at D=6 and at D=8, with enclosure `[1/6, 1/6]`. The same value holds on the untruncated graph, because `psi_1 = (W_1+W_2)/3` is an exact `K`-eigenvector combination; the omitted tail is 0.
- The free reference `<W_1>(0)` is `[0, 0]` at both cutoffs, computed in the same routine.
- The producer's Cauchy route 2 gives `[0.16662873, 0.16670459]` (labelled, wider).

**2. Enclosures of `<W_1>`.** All are full-graph certified. Decimals are rounded outward at 32 places; the exact rationals are in the producer's `output/results.json` and in `az2.json`. The negative points are the exact negations.

| D | `tau_FG` | lower | upper | half-width |
|---|---|---|---|---|
| 6 | +1/1000 | 0.00016666666111704683798008229862 | 0.00016666666111704683798008232063 | 1.10e-29 |
| 6 | +1/100 | 0.00166666111707696022389733087208 | 0.00166666111707696022411805253250 | 1.10e-22 |
| 6 | +1/10 | 0.01666112008741082417265341370420 | 0.01666112008741309878195670288161 | 1.14e-15 |
| 8 | +1/1000 | 0.00016666666111704683798008230962 | 0.00016666666111704683798008230963 | 2.81e-39 |
| 8 | +1/100 | 0.00166666111707696022400769169946 | 0.00166666111707696022400769170512 | 2.82e-30 |
| 8 | +1/10 | 0.01666112008741196147439620849567 | 0.01666112008741196148021390820658 | 2.91e-21 |

**3. Coefficients (finite-model values, exact, D-independent).**
- `<W_1> = tau_FG/6 + 0·tau_FG^2 - (187/33696) tau_FG^3 + (767713/2523156480) tau_FG^5 + …`
- `E_0 = -tau_FG^2/6 + (187/67392) tau_FG^4 + …`
- Second-order values: `<W_1^2>: 7/576`, `<W_1 W_2>: 79/2808`, `<z>: 7/216`.
- The truncation error of every coefficient is exactly 0: `psi_n` lies in `P_n` inside `P_D`.

**4. Ledger.** The complete residual lies exactly in shell `D+1`, which splits into 36 sectors at D=6 and 55 at D=8, all orthogonal. The five parts at every one of the 14 points:
- **(a)** seven per-link rows: link classes `j` (h1, vL, h3), `k` (h2, vR, h4) and `ell` (vM);
- **(b)** the joint product channel: the complete omitted sum, the product-channel weight, corner overlaps, and the `2XY` interference, which is positive, so the face channels are not orthogonal;
- **(c)** gauge projection exactly 0, with its reason;
- **(d)** the Ritz residual, with Davis–Kahan and Eckart angles and the Weyl separation `3-2|tau_FG|`;
- **(e)** directed arithmetic.

The thresholds:

| Threshold | D=6 | D=8 |
|---|---|---|
| `tail_lower` | 45 | 69 |
| `j`/`k` links | 123/2 | 96 |
| `vM` | 45 | 69 |
| product channel | 48 | 145/2 |

**5. Dictionary.** `tau_FG = tau/24`, and `1/6` corresponds to `1/144`. It is **consistent with** the matched Z^3 first-order coefficient; the mandatory sentence appears verbatim. The agreement is expected: both models give `2·coefficient·E[W^2]/3` with energy 3.

## Exact comparison (own code; nothing imported from the producer)

| Quantity | Producer | This review | Pre-comparison prediction |
|---|---|---|---|
| dimension, `tail_lower` | 84/45, 165/69 | same | same |
| derivative at 0 | `[1/6,1/6]` at D=6, 8 | `1/6` | `1/6` (both models) |
| free reference | `[0,0]` | `0` | `0` |
| second-order `<W>` | 0 | 0 | 0 |
| `E_2` | -1/6 | -1/6 (two-face) | -1/12 (one-face); -1/6 recorded as the both-faces side value |
| third-order `<W>` | -187/33696 | -187/33696 | -5/864 (one-face); -187/33696 recorded as the side value |
| thresholds j/vM/product | 123/2, 45, 48; 96, 69, 145/2 | same | same (my A/B, S, joint) |
| enclosures (12) | half-widths 1.1e-29 … 2.9e-21 | contain my two-face degree-12 enclosures (half-widths 7.3e-48, 7.3e-35, 7.8e-22) | disjoint from my one-face enclosures by the certified shift |
| omitted residual `rho_Q^2` at `tau=1/1000` | 3.81105e-57 (D=6), 3.91821e-76 (D=8) | `tau^(2D+2)·‖Q_D(x+y)psi_D‖^2` agrees to relative 1.6e-7 and 1.8e-7 | — |
| product channel | nonzero, ≈5.0e-18·`tau^16` (D=6) | 0 at leading order; enters at `tau^(2D+4)` (producer ratios 9.9998e15 and 9.9998e19 per decade) | — |
| Arb preview | 14 balls inside the enclosures | inside the producer enclosures; they also meet my two-face enclosures | — |

**How the independent routes work.**
- **The enclosures.** They use a degree-12 Rayleigh–Schrödinger vector with the exact complete residual and the Weyl separation `3-2|tau_FG|`, bounded by Davis–Kahan. The negative points follow from the exact `(-1)^n` flip parity of `psi_n`. This is not a cutoff-D certificate; it certifies the full-graph value that both producer cutoffs enclose.
- **The leading-order leak.** It is computed by exact Gram projection with my own LDL on the parity blocks, and the 36/55 sectors are verified orthogonal. The producer's `vM` class carries the whole leading leak, and its `j`-class weight agrees with mine to relative 9e-8.

## Widths: which is tighter, and why

| Half-width | `+1/1000` | `+1/100` | `+1/10` |
|---|---|---|---|
| producer, D=6 (two-face, Eckart with tail comparison) | 1.10e-29 | 1.10e-22 | 1.14e-15 |
| producer, D=8 | 2.81e-39 | 2.82e-30 | 2.91e-21 |
| my pre-comparison, D=6 (one-face, Davis–Kahan) | 3.59e-31 | 3.60e-24 | 3.71e-17 |
| my pre-comparison, D=8 | 1.78e-41 | 1.79e-32 | 1.84e-23 |
| my post-review two-face, degree-12 vector (not a cutoff certificate) | 7.27e-48 | 7.31e-35 | 7.77e-22 |

**The one-face numbers are narrower, by about 30 times at D=6 and about 160 times at D=8.** They are also a different model.
- In the one-face model the omitted residual of the ground vector is a single spin-network component: `|(D+1)/2, 0, (D+1)/2>` with amplitude `tau_FG v_D/2`.
- In the two-face model, `(x+y)` applied to the top shell leaks into the whole `vM` channel `x^a y^b` with `a+b = D+1`, with binomially grown amplitudes. At D=6 the two-face leak is about 115 times the one-face leak (6.2e-15 against 5.4e-17 at `1/10`).
- Part of that gap is recovered by the producer's sharper angle bound. Its Eckart angle, which uses the Round11 tail-comparison energy, is 3.74–4.85 times smaller than the Davis–Kahan angle I used. The ratio is recorded exactly at every point.

**Within one model** the producer's cutoff-D certificates are the tightest of their kind. My degree-12 vector is tighter only because it leaves `P_8`.

**All intervals are valid.**
- Every producer interval contains my independent two-face interval.
- D=8 lies inside D=6 at every point.
- The Arb balls lie inside the producer intervals.

## How the producer handled my pre-comparison findings

The producer did not read my package, so the correspondences below are independent convergences, not uptake.

1. **Spectator second square.** This is moot for the producer's model: coupling both faces makes the second square active. Its §5 calls the `1/144` agreement "expected rather than informative", which matches my "identity" reading.
2. **Unpinned `alpha`, `rho` and `lambda2`.** The producer states `alpha = 1`, `rho = 1` and `lambda1 = lambda2 = tau_FG`. It handles negative `tau_FG` outside the Round11 API with a sign-free argument, and it checks the `-tau` certificate against the `vM`-flip image.
3. **Reading the five ledger parts for a degree basis.** The producer's reading equals mine: link classes by the Gauss law, per-link means spin `> D/2`, and the product channel means all spins `<= D/2` at joint degree `D+1`. It goes further than my one-vector argument:
   - an exact sector decomposition;
   - corner overlaps;
   - the positive `2XY` interference;
   - certified per-link and joint tails of the true ground state.

   Item (c) is exactly 0 with its reason. Item (d) uses the Weyl separation, not a finite-matrix gap.
4. **The update-4 correction.** The producer uses neither update-4's truncated brackets nor its `tau^2/(tail-3)` heuristic. It certifies full-graph enclosures with the complete residual and the Round11 tail comparison. My correction remains on record: update-4 is a premise, and its "each bracket is already a certified two-sided enclosure" claim is false for `exact_bracket`.
5. **Second-order coefficients.** Zero by a centre flip, with zero truncation error. Coefficients come from exact Rayleigh–Schrödinger algebra and are never fitted. This agrees with my reading 5 and with producer D4.
6. **Target indicator** and **7. legacy error terms.** These agree (producer D5 and D1).
8. **`selected_after`.** The producer's D6 records it, with a different emphasis.
9. **`state_provenance` and `clock`.** Producer D2 and D8.
10. **Legacy control ids.** The producer's finite-graph analogues differ from mine in two places, both legitimate once the model is fixed:
    - `missing_incoming_stars` requires both faces: `W_2` is "incoming" on `vM`. This encodes the producer's model choice. The rejected mutation "W_2 omitted" is the one-face model, which the contract text admits; so this control should not be cited as showing the one-face reading wrong (N2).
    - `root_n_misuse` is the `2XY` interference. That is a genuine two-face refinement.
11. **Forbidden phrases.** The producer's scan is a substring scan on lowercase text with code spans removed. My whole-word scan of the prose finds nothing. The two occurrences sit in code spans in §9, where the claim-exclusion list is quoted.

## Producer defects D1–D8, reconciled

| Producer | Content | My pre-comparison reading |
|---|---|---|
| D1 | `truncation_jmax` preregistered though no `j_max` is well-posed; mapped to items a+b+c | reading 7 (same; I added that in the one-face ground sector the cutoff *is* per-link) |
| D2 | `state_provenance` is an AQ string | reading 9 |
| D3 | control ids name AQ/Z^3 objects | reading 10 |
| D4 | item 4's tail residual: the coefficient truncation error is exactly 0 and `a_2 = 0` | reading 5 |
| D5 | the target `1 >=` is an indicator | reading 6 |
| D6 | `selected_after` names the AZ1 gate, not a premise | reading 8 (the gate did not exist at freeze) |
| D7 | "must reproduce" in `parameters.observable` read as the item-3 comparison only | not raised; agreed |
| D8 | "exponent 24 forbidden" versus the dictionary's 24 | noted in my checker (a divisor, not an exponent); agreed |

**Added by this review:**
- **W-A.** The contract does not fix which faces carry `tau_FG`. The producer's two-face reading and my one-face reading are both admissible, and they differ at third order. Record the model exactly.
- **W-B.** `alpha_FG`, `rho` and `lambda2` are pinned only implicitly (my reading 2). The producer pins `alpha = rho = 1` and `lambda1 = lambda2`.

## Review against the contract items

1. **Graph, basis, cutoff and a complete five-part ledger.** Present at all 14 points, with (a) through (e) itemized as listed in §4 above.

   The ledger values were checked independently at leading order. The omitted residual equals `tau^(2D+2) ‖Q_D(x+y)psi_D‖^2` to relative 1.6e-7 (D=6) and 1.8e-7 (D=8). The `j` and `vM` class weights match. The product channel vanishes at leading order and scales as `tau^(2D+4)`.
2. **Enclosures at the grid, the derivative and the own free reference.** All 12 enclosures are sign-certified. Each contains my independent enclosure, and D=8 lies inside D=6. The derivative is `[1/6, 1/6]` at both cutoffs and the free reference is `[0, 0]`.
3. **Comparison with `1/144`.** The dictionary gives `1/6 -> 1/144`. It is "consistent with" the matched coefficient, the mandatory sentence appears verbatim, and the scan finds no forbidden phrase.
4. **Second-order coefficients.** They are exact finite-model values: `<W_1>: 0`, `E_0: -1/6`, `<W_1^2>: 7/576`, `<W_1 W_2>: 79/2808` and `<z>: 7/216`. Their truncation error is 0.
5. **Labels and controls.**
   - Labels: all eight present.
   - Gate fields: `transfers_to_aq: false`, `model_is_finite_graph: true`, `fg_coefficients_fitted: false`.
   - Arb: python-flint 0.9.0, labelled PREVIEW ONLY, never imported (AST of `check.py`). Deleting its output changes no admission value.
   - Controls: all 20 carry damaging mutations (80 in the control checks, 90 in total), and each is live under source edit.
   - Freeze: verified.
   - Skeptic: the pre-comparison replay and this post-comparison review are done.
6. **Forbidden phrasings.** None in the prose. The flags `continuum_claim`, `scientific_priority_verified`, `weak_coupling_claim`, `roadmap_goal_2_resolved` and `resolved_interaction_shift` are all false.

**Acceptance clause.** "Enclosures with certified tails at every grid point; first-order coefficient consistent with the dictionary; labels present." All three hold at both cutoffs, and the joint product channel is itemized. So the result is `accepted_within_scope`, not `limited`.

## Replays, closure and isolation

**The tool.** `replay_declared.py` (unchanged, `9707c779…`) accepts this loop, because the contract declares `single+skeptic`. It reuses `replay_loop.py` unchanged (`e627df04…`).

**Results:**
- The closure has 34 listed files plus `freeze.json`, and it verifies file by file.
- The inputs are exactly AGENTS.md, the contract and the 26 shared premises (28 files), each byte-identical to its repository source.
- The normal and `-O` replays reproduce `results.json` (`96d7b88d…`) and `source-manifest.json` (`56e24535…`) byte for byte.
- `freeze.py verify` reports verified, both inside the tool and in a separate run.
- No `reverse/az2` package exists.

**Scratch audit** (names and mtimes only). `/tmp/claude-0/az2-forward-private/` matches the producer's disclosure: `proto/` from 04:46, `cont*.py` 05:03–05:07, `run1`/`run2`, `mutaudit/` (nine edit folders, 05:25–05:27) and `run-final` at 05:28:20.

**Name exposures.** Disclosed in `az2-replays.json`.

## Source-edit receipts

**Unmutated copy.** It reproduces `output/` byte for byte.

**One weakening per contract control (20 of 20 abort at that control).** Each validator was made to return `True`; for `exact_arithmetic_admission`, `rat` was made to accept non-exact input instead. The producer's own damaging mutation is then accepted, and the copy aborts with "damaging mutation accepted: `<first label>`":

| Control | First label accepted |
|---|---|
| `missing_incoming_stars` | `incoming_face_W2_coupling_omitted` |
| `full_original_wilson_cover` | `three_drawn_links_open_path` |
| `wrong_delta_alpha_hbar_clock` | `tau_over_18_…` |
| `vector_versus_scalar_centering` | `scalar_subtraction_as_centring_bound` |
| `first_order_mean_charged` | `first_order_mean_set_to_zero_by_parity` |
| `tau_scaling_exponent` | `remainder_labelled_second_order` |
| `changed_model_relabelled` | `anisotropic_shared_link_rho2` |
| `coherent_evidence_tampering` | `control_boolean_flipped_hash_rebound` |
| `insufficient_verdict_retained` | `tail_only_at_D6_relabelled_accepted` |
| `exact_arithmetic_admission` | `float_input` |
| `root_n_misuse` | `rss_of_face_channels_without_interference` |
| `no_priority_or_continuum_claim` | `continuum_true` |
| `finite_graph_model_id` | `model_is_finite_graph_false` |
| `complete_residual_all_channels` | `y_channel_dropped` |
| `certified_representation_tail` | `last_retained_shell_m_D_as_tail` |
| `own_free_reference` | `Z3_first_order_imported_as_reference` |
| `no_transfer_to_aq` | `transfers_to_aq_true` |
| `fg_coefficients_not_fitted` | `least_squares_slope_through_grid` |
| `sign_convention_fixture` | `flipped_sign_gives_minus_one_sixth` |
| `complete_residual_ledger_itemized` | `joint_product_channel_not_itemized` |

**Semantic edits (6):**

| Edit | Outcome |
|---|---|
| One-face default in `rs_series` | aborts at `rs_exact_full_space` |
| One-face certificate Hamiltonian (`t = x v`) | aborts: "square root of a negative number", an internal guard (N5) |
| Free gap 4 | aborts at `round11_conventions_bound` |
| Omitted residual dropped | aborts at `ritz_certificates_complete` |
| the forbidden phrase `predicts` appended to the report | aborts: `forbidden phrasing in the report: predicts` |
| `preview/arb_preview.json` removed | completes; the headline and every point are unchanged, and only the preview comparison record differs (by design) |

**Own validator.** It accepts the frozen packet and refuses 18 damaged packets. The model-specific ones:
- the Hamiltonian relabelled one-face while the numbers stay two-face;
- the one-face `E_2` inserted with the two-face series;
- an unnamed model;
- an enclosure replaced by the one-face interval.

The rest:
- the derivative `1/144`;
- the free reference `1/4`;
- a nonzero `a_2`;
- `fitted: true`;
- `transfers: true`;
- tail 56;
- a lost sign;
- the joint ledger dropped;
- the gauge reason dropped;
- the `vM` row dropped;
- product threshold 45;
- the altered sentence;
- the dictionary relation relabelled as the forbidden verb (`predicts`);
- a dropped sub-label.

## Which values the gate should bind

- **Model.** `H_FG = K - tau_FG (W_1 + W_2)`, alpha units, `rho = 1`, both faces coupled equally, I1.5 sign, gauge-invariant sector of the Round11 two-plaquette graph. `D` in {6, 8} (dimensions 84, 165). Grid `{±1/1000, ±1/100, ±1/10}`.
- **The derivative** `[1/6, 1/6]` at both cutoffs, and the free reference `[0, 0]`.
- **The twelve exact enclosures** from `output/results.json`, as listed in `az2.json`.
- **Coefficients.** `a_2 = 0`, `E_2 = -1/6`, `a_3 = -187/33696`, `a_5 = 767713/2523156480`, `E_4 = 187/67392`, `<W_1^2>_2 = 7/576`, `<W_1 W_2>_2 = 79/2808` and `<z>_2 = 7/216`. Truncation error 0.
- **Thresholds.** `tail_lower` 45/69; per-link 123/2 and 96 for the `j`/`k` links, 45 and 69 for `vM`; product channel 48 and 145/2.
- **The dictionary.** `1/6 <-> 1/144`, consistency only.
- **Skeptic findings to record, not as producer values:**
  - the second-square shift `tau^3/4212 + O(tau^5)`, certified at every point;
  - the one-face reading's values as the alternative model: `-5/864`, `-1/12`, and my pre-comparison enclosures;
  - the spectator identity with the AW1 fixture, which holds only for the one-face model.

## Blocking issues

None. The model question is not blocking because the contract does not fix one face and the producer disclosed its model.

## Non-blocking findings

- **N1 (W-A).** The face coupling is not fixed by the contract. The gate names the two-face model. Later contracts that reuse a finite graph should name every coupled face and its coefficient.
- **N2.** The producer's `missing_incoming_stars` control rejects "W_2 omitted" as a damaging mutation. Relative to the frozen text that is the alternative admissible model, not an error. The control encodes the producer's model choice and should not be cited as refuting the one-face reading.
- **N3.** In the same model, the producer's Eckart/tail-comparison angle is 3.74–4.85 times sharper than Davis–Kahan. The two-face leak is about 115 times the one-face leak at D=6. The one-face pre-comparison widths are narrower only because they belong to that model.
- **N4.** The producer's Cauchy route 2 is valid but wide (about 1e-4). It is correctly retained as a weaker tier.
- **N5.** The one-face certificate-Hamiltonian edit is caught by an internal square-root guard, not by a named check. It still aborts. A named model-consistency check between the proposal Hamiltonian and the certificate Hamiltonian would be clearer.
- **N6.** The Arb preview is not an admission input. Deleting its output leaves every admission value unchanged; only the recorded comparison count changes.
- **N7.** Outside its inputs, the producer read `tools/freeze.py`, most of `forward/ay2/check.py` and the header of the AX2 report, for protocol and style. This is disclosed and carries no premise weight.
- **N8.** My pre-comparison predictions for the one-face model (the enclosures, `-5/864`, `-1/12`) do not apply to the admitted model. The model-independent predictions all held: `1/6`, `0`, `0`, 84/165, 45/69 and the channel thresholds. My recorded both-faces side values (`-187/33696`, `-1/6`) match the producer exactly.

## Limitations

- **Scope.** This is one finite graph, the Round11 two-square patch, and one named model (both faces coupled equally, `alpha = rho = 1`), at `D` in {6, 8} and the declared grid only. It is a static ground-state mean: no dynamics, correlator, clock or mass-gap reading.
- **No transfer.** Nothing transfers to the AQ construction, its subsequential limits, `K_2`, the Z^3 shift, roadmap goal 2, weak coupling or the continuum. The zero second-order coefficient is a finite-graph fact from a centre flip; it says nothing about the AQ remainder.
- **The dictionary.** `1/6 <-> 1/144` is a consistency check, expected from the shared normalization. It is not a prediction or a confirmation.
- **The one-face model is not admitted.** Its values are recorded as the skeptic's alternative reading, together with the certified shift between the two.
- **Inherited without re-proof.** The Round11 reduction, kinetic operator, spectrum, tail and Theorem F, as well as Kato perturbation theory, Weyl, Temple, Eckart and Davis–Kahan, are cited. The checkers re-verify the fixtures, not the reduction.
- **Standing.** This is model-agent review with correlated ancestry, not human peer review or formal verification. Scientific priority is unverified.
