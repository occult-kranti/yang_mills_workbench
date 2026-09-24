# AY1 skeptical review (post-comparison)

**Verdict: accepted_within_scope, sub-label `uniform_local_closeness_not_uniqueness`.** Both routes carry out contract items 1–6 for the zero-selected patterned family at both signs of `|tau|<=10^-8`, with the two named construction families:
- F1, the AQ1 centered whole-star boxes;
- F2, the I1 §6 all-contained-face boxes with padding, on the same `Lambda_N=[-N,N]^3`.

The shared results:
- **The premises hold for both families.** F2 is itemized: supports at most 4, termination order 8, per-site sum `28|tau| = J_0` at the cap, contraction `37/6250000 < 1/64` and `77/390625 < 1`, reset `98|tau|` (`56|tau||F|` in general), local trace-norm compactness and its own diagonal extraction.
- **The pair constant `2D`.** It holds for every pair of subsequential limits of either family at the same τ.
- **The common first-order density.** `rho^(1)_R` is an explicit 10-face operator.
- **An R-local trace-norm constant `K_2'`** for the second-order difference.

Every headline constant is the same exact rational in the forward, the reverse and my pre-comparison package:

| quantity | exact | preview | forward | reverse | skeptic (pre) |
|---|---|---|---|---|---|
| `D` (AV1 gate, forward tier ii) | `585079838465912592144137406066050/42981220507576537932303142777593983768257` | 1.36124528702e-8 | = | = | = |
| **`2D`** | `1170159676931825184288274812132100/42981220507576537932303142777593983768257` | **2.72249057405e-8** | = | = | = |
| target / margin | `1/1250000` | 29.3849 | met | met | met |
| `2D_i` (tier i, retained) | `72266694536315307496644/1525878906463907516326874161` | 4.73607e-5 (fails) | reported | = | = |
| faces meeting R / surviving the R-marginal | 82 / 10 | | = | = | = |
| `||rho^(1)_R||_1` | `sqrt(10)|tau|/72` (square `1/5184000000000000000` at the cap) | 4.39205230578e-10 | = | = | = |
| `Tr(rho^(1)_R W)` | `+tau/144` | | = | = | = |
| **`K_2'`** (trace norm, R-local, triangle) | `966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000` | **13417.5275439** | = | = | = |
| **`2K_2'tau^2`** | `966771578474926086618624139557778885954947547760216752246561/360264428489086053772729024659456000000000000000000000000000000000000000` | **2.68350550879e-12** | = | = | = |
| `K_2'/K_2^+` | `K_2^+` = AW1 gate `81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984` | 3.99949762 | = | = (exact ratio exported) | = |

**The gate should bind these values:**
- `2D` (the pair constant and the preregistered target quantity);
- the 10-face `rho^(1)_R`;
- the triangle headline `K_2'`;
- `2K_2'tau^2`.

The labelled variants are valid but should not be the headline (see "Which value to bind"). There are **no blocking issues**. Uniqueness, whole-sequence convergence, a rate in N, translation invariance, boundary independence of the dynamics, and any dynamical, continuum or weak-coupling statement are not admitted.

**Standing.** I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and both producers. My own triage (Goal-4 note and control 17) seeded the "2D closeness" observation and the fixed-vector and common-interval controls. My AV1 and AW1 reviews are shared premises of both producers. This is not human peer review or formal verification. Human project author: Hruday N M (BUNZEEY).

**My pre-comparison package is unchanged.** It contains:
- `ay1-contract-review.md`;
- `ay1-independent-derivation.md`;
- `ay1_check.py` (96 checks, 26 controls, 70 rejected mutations);
- `ay1-independent/results.json`.

Its hashes match `ay1-independent-freeze.json`. It was committed at `55be992` (02:39:42Z), before the reverse (`d1e6ac6`, 02:49:24Z) and the forward (`f7b9839`, 02:50:55Z). A fresh replay of `ay1_check.py` under normal and `-O` Python reproduces the frozen `results.json` byte for byte. My predictions matched every producer headline rational for rational (see "Predictions against producers").

**This review adds:**
- `ay1_postreview_check.py`: 55 exact checks, including 28 source-mutation runs (22 must-abort edits aborted, 4 silent edits caught, and 2 unmutated copies);
- `ay1-postreview/results.json`: byte-identical under normal and `-O` Python;
- `ay1-replays.json`.

## What is proved, with quantifiers

**Model.** `AQ_patterned_zero_selected`:
- SU(2) Kogut–Susskind form on Z³ at fixed spacing, with coarse 24-link factors;
- selected triple exactly `(0,0,0)`, so `h_b=8ΣC_e>=6Q_b` and the reference `P_R` is the Haar product;
- 21 omitted faces per anchor, each entering as `−(tau/3)W_f` (I1.5, `delta=alpha/8`);
- both signs of τ, `|tau|<=10^-8`;
- cover `R={0,e_z}` (48 links, 36 endpoints, 7 incident anchors);
- observable class `B(H_R)`;
- common clock `s=alpha t_E/hbar`, `theta=alpha t/hbar`.

**1. Both families satisfy the AV1 premises.**
- **F1** is covered by the admitted chain I1 → AM2 → AQ1/AQ2 → AV1 → AW1. Both producers cite it step by step.
- **F2** (retain an omitted face iff its actual owner set lies in `Lambda_N`, grouped at its anchor; I1 §6 padding to `B_+ = B+S` with decoupled Haar sites) is verified item by item:
  - supports: `(b+S)∩Lambda_N`, so `|X|<=4`;
  - termination: order `2|X| = 8`;
  - per-site sum: `J<=4·7|tau|=28|tau|=J_0` at the cap, with equality at bulk sites;
  - contraction at the **same** `J_0`: `J_0G(R) < 37/6250000 < 1/64` and `2J_0G'(R) < 77/390625 < 1`;
  - first-order faces: at most 49 per site, so `T`, `rho` and `eps` are unchanged and the same `D` bounds every F2 box;
  - cutoff removal: AM2 §6 and AV1 §7;
  - reset: `omega(h_R)<=98|tau|` (the same seven full groups as F1 for `N>=2`), and `C_F=56|tau||F|`;
  - compactness: trace-norm compactness and F2's own diagonal extraction.
- **Enumeration** (`N=2,3`), identical in both producers and in my code:
  - F1 retains `21(2N)^3` faces (1344 and 4536);
  - F2 retains `14(2N)(2N+1)^2+7(2N)^2(2N+1)` (1960 and 5880);
  - F2 minus F1 is `28N(5N+1)` (616 and 1344), with partial groups 60 and 126 and `B_+` of 200 and 490 sites;
  - both families retain the same 82 faces meeting R and the same 10 faces with owner set R.
- **Topologies**, named separately:
  - states: trace norm on `B(H_R)`;
  - dynamics: norm on compact time windows (Nachtergaele–Sims), named only. F1 inherits the star-indexed `Phi`; F2 has the owner-set-indexed `Phi'` with `||Phi'||_F<=1323|tau|` (reverse). Neither producer claims that the two families' dynamics coincide.

**2. Closeness.** For every pair of subsequential limits (same family or different families) at the same τ, `||rho_R-rho'_R||_1 <= 2D`. The statement holds for a chosen subsequential limit of either family, each one separately; it does not identify limits with one another. The proof is the triangle through `P_R` plus closed-ball passage (forward), or the fidelity identity passed to limits plus the same triangle (reverse).

The reverse adds a labelled pairwise Bures-angle route, `||rho_R-rho'_R||_1 <= 4eps/(1+eps^2) = 1170159668967453566242603438964736/42981220507576537932303142777593983768257` (≈2.72249055552e-8, below `2D`). I re-derived it:
- `A(rho,P_R) <= arctan eps`;
- `A(rho,rho') <= 2arctan eps <= pi/2`;
- Fuchs–van de Graaf gives `(1/2)||rho-rho'||_1 <= sin(2arctan eps) = 2eps/(1+eps^2)`.

It is correct.

**3. First-order density and second-order difference.**
- **The density.** `rho^(1)_R = (tau/72) Σ_{f∈F_R}(|W_fΩ_R⟩⟨Ω_R| + |Ω_R⟩⟨W_fΩ_R|)`, where F_R is the 10 faces with owner set exactly R: xz with `r<=2`, `s=0,1`, and yz with `s=0`, `r=0..3`, all anchored at 0.
- **Why only 10 faces.** Of the 82 faces meeting R (from the anchors 21+21+16+4+8+4+8), the 72 straddling faces have zero R-marginal: each has a link owned outside R that occurs once, so its Haar integral vanishes. The zero-selected family has no single-site creations.
- **Properties.** The density is rank two, self-adjoint and traceless, with only off-diagonal blocks. Its trace norm is `sqrt(10)|tau|/72`, and `Tr(rho^(1)W)=+tau/144` (AW1).
- **The forward derivation** is the R-marginal of `−(c^(1)Ω_0^*+h.c.)`.
- **The reverse derivation** uses the block decomposition:
  - the scalar fidelity identity kills the diagonal block;
  - positivity kills the excited block;
  - the vector overlap identity `rho_R Omega_R = (1⊗⟨phi_out|)psi/||psi||^2` gives the off-diagonal block.

  The reverse also proves that the first-order coefficient is independent of the family, subsequence and selection. If X and X′ both satisfy the uniform expansion, then `||X−X'||_1 <= (K+K')|tau_j| → 0`.
- **The second-order bound.** For every subsequential limit of either family, `||rho_R−P_R−rho^(1)_R||_1 <= K_2'tau^2`, uniformly in N, the cutoff and the family. Hence `||rho_R−rho'_R||_1 <= 2K_2'tau^2`, which is about 1.0145×10⁴ times below `2D`.
- **The five items** are identical in all three computations: `4rho`, `2T(72a+2rho)`, `2(33a+rho)^2`, `2eps_R^2` and `20a·eps_R^2`, with `a=|tau|/144`, `rho=352JT`, `eps_R=82a+2rho+(33a+rho)^2`.

**4–6.**
- **Sentence and fields.** Both producers state the contract template and the Jung loop-2 form, and export the five gate fields as false.
- **Definition.** Both define "quantitative boundary comparison" as the closeness bound plus the matching first-order term, and not as a variational statement about which boundary condition the infinite-volume theory selects.
- **Uniformity.** Both state "uniform in N at fixed spacing, never in a".
- **Controls.** All 21 contract controls are damaging mutations in both checkers.

## Predictions against producers

My pre-comparison predictions matched every headline to the rational:
- `D`, `2D` and `2D_i`;
- the counts 49, 82, 10, 72, 66, 33, 16, 6 and 27, and the 7 anchors;
- F2 J = 28, support 4, termination 8, reset 98 and `C_F` 56;
- the extra-face formula `28N(5N+1)` and the distance N−1;
- the 10-face `rho^(1)_R` with trace norm `sqrt(10)|tau|/72`;
- `K_2'` ≈13417.5275 with all five items, the √2 variant ≈9487.945, and the W-projected analogue ≈3354.4994;
- `2K_2'tau^2` and the `±tau` separation ≈8.757e-10;
- the "first-order-resolved" upper value ≈4.405e-10.

No producer number differs from a prediction. The producers' additional labelled values are:
- the reverse's 288-majorant variant (≈10978.18);
- the combined variant (≈7763.06);
- the admitted-`eps` variant (≈13417.81);
- the Bures constant;
- the lower end ≈4.37863e-10 of the supplementary observation.

I re-derived all of them exactly (post-review checks `reverse_labelled_variants_valid` and `supplementary_two_sided_observation_in_bracket`).

## The K_2' > K_2^+ finding and how "not the whole-box K_2^+" must be read

Contract item 3 asks for "an explicit R-local `K_2'` built from the AW1 remainder items restricted to faces meeting R (not the whole-box `K_2^+`)". The modern lens (update-3) expected `K_2'` to be "strictly smaller than AW1's `K_2^+`". It is not, and it cannot be with the admitted remainder:
- **`K_2^+` is already a constant on R.** It bounds the single observable W. W pairs only with the `{0,e_z}` sector, with multiplier `2||WΩ_R||=1`, and it annihilates the single-site remainders and the 66 one-site straddling faces.
- **The trace norm costs more.** A trace norm on `B(H_R)` pays multiplier 2, and it pays all three excited sectors (`{0}`, `{e_z}`, `{0,e_z}`) at both sites.
- **The dominant term is not R-local.** 99.979% of `K_2^+` and 99.99% of `K_2'` is the generic AM2 majorant `rho=352JT`, which is a per-site constant.
- **Hence a floor.** Every trace-norm constant assembled from the AW1 items is at least `2rho/tau^2 ≈ 6708.2`, and at least ≈5488.7 with the sharper `288t/(1-8t)` majorant. Both exceed `K_2^+`.

Measured values:
- triangle `K_2'` = 3.9995 `K_2^+`;
- √2 sector variant ≈ 2.828 `K_2^+`;
- 288 variant ≈ 3.272 `K_2^+`;
- both refinements ≈ 2.314 `K_2^+`.

Only the W-projected R-local analogue, `rho+T(6a+rho)+(33a+rho)^2+eps_R^2+a eps_R^2` ≈ 3354.4994, lies below `K_2^+`, by 0.3038. It is AW1's minimal form, not a density bound.

**The gate must read the parenthetical as follows:** `K_2'` is built from R-local face pins (82, 72, 33 and 10), unlike `K_2^+`'s unpinned `T·T`, `T^2` and `2T+T^2`. It is **not** a claim that `K_2'` is smaller. "Whole-box" should not be repeated: `K_2^+` is uniform in N, not volume-dependent.

All three agents report `K_2'>K_2^+` with its sign and its reason:
- forward W1 and §5.6;
- reverse §3.8 and wording note 2;
- my contract review item 1.

## The reverse route's "derivative of the fidelity identity" (vector form)

The scalar identity `Tr(rho_R P_R) = 1/(1+e^2) = 1−O(tau^2)` has zero τ-derivative. It fixes only the vanishing of the `P_R` block of `rho^(1)`. The contract's phrase must therefore be read as the derivative of the **vector** vacuum-overlap identity, `rho_R Ω_R = (1_R⊗⟨phi_out|)psi/||psi||^2`, whose `Ω_R` component is the scalar identity. Positivity (`Tr rho_⊥⊥ = 1−F <= eps^2`) removes the excited block.

The reverse states exactly this (wording note 1), as did my contract review (item 3). The derivative is taken in finite boxes, and passage to limits is only through the uniform remainder. Neither producer differentiates a subsequential limit. Both say explicitly that "the" first-order density is a statement about a coefficient, not about states.

## The supplementary two-sided observation (record as a labelled observation only)

The reverse triangle inequality applied to the uniform expansion gives, for every subsequential limit of either family at either sign,

`sqrt(10)|tau|/72 − K_2'tau^2 <= ||rho_R−P_R||_1 <= sqrt(10)|tau|/72 + K_2'tau^2`.

At the cap this lies in **[4.3786e-10, 4.4055e-10]**:

| end | exact value | preview |
|---|---|---|
| forward lower | `315493271189404336654387912683326986946293536292239783247753439/720528856978172107545458049318912000000000000000000000000000000000000000` | 4.37863477824e-10 |
| reverse lower | `616197795291805409919264392064860992079046237503264929983414263332219/1407282923785492397549722752576000000000000000000000000000000000000000000000000` | same preview |
| forward upper | `317426814346354288901077519041901926031821392347760216752246561/720528856978172107545458049318912000000000000000000000000000000000000000` | 4.40546983333e-10 |

I verified each end exactly as a directed bound: `(lower + K_2'tau^2)^2 <= 10tau^2/5184 <= (upper − K_2'tau^2)^2`.

**Two consequences:**
- The upper end is about 30.9 times below `D`. AV1's `eps` charges the 72 straddling faces at first order, but they reach the off-diagonal block only at second order.
- The lower end is the first lower bound on `||rho_R−P_R||_1` in Round32. The AV1 gate lists this quantity as "not provided".

**Recommendation: the gate may record it only as a labelled observation.**
- It is not a preregistered target or comparator.
- It is not an admitted tier, and it must not replace `D` anywhere, including in `2D`.
- It must not be called a resolved interaction shift. `resolved_interaction_shift` stays false: the flag concerns the Euclidean and dynamical shift, and the static Wilson mean is AW2's.
- Both producers already label it this way ("not a contract target", "not claimed").

If recorded, it should be recorded from the exact values above, which this review re-derived. The forward checker does not pin its lower end (finding N2).

## Review against the six required items (both producers)

1. **Complete in both.**
   - The forward verifies AM2's five hypotheses, H1–H5, literally for F2, with actual supports `X_b=∪M_f⊂(b+S)∩Lambda_N`. With that convention padding is inessential.
   - The reverse indexes each clipped group by its declared support `X_b=b+S` inside the AM2 volume `B_+`, following the AM2 reverse's scope statement. With that convention padding is required, and the reverse rejects its removal.
   - Both conventions are valid (finding N1).
   - Both producers state compactness and F2's own extraction, and name both topologies separately.
2. **Complete in both**, with the quantifier "every pair of subsequential limits, same or different family, same τ". Both producers reject:
   - equality from closeness;
   - whole-sequence convergence;
   - a rate.
3. **Complete in both.** The two derivations differ in route (explicit marginal versus block decomposition with the vector overlap identity) and agree to the rational. Family independence is proved face by face for `N=2,3` and by the general geometry. The `K_2'` comparison is reported with its sign.
4. **Complete in both.**
   - **Contract template.** The forward quotes it verbatim, with constants appended. The reverse fills it with the constants inserted in parentheses, and every clause of the template appears verbatim and in order (post-review check `mandatory_sentence_template_present`).
   - **Gate fields.** All five are false in both `results.json`.
   - **Jung fields.** The forward exports `rate_in_N_claimed`, `states_compared`, `region`, `topology` and `closeness_order: 2`. The reverse exports `closeness_order: [1,2]` and lacks `rate_in_N_claimed`, which the contract does not require (finding N4).
5. **Complete in both.** All 21 contract controls are damaging mutations in both checkers, and the reverse has no unimplementable control.
   - **Fixed-vector versus moving-vector.**
     - The forward shows strong versus norm continuity: fixed `e_1` gives `<=4/n` against moving `e_n` at 2.
     - The forward shows weak-* mass escape of `|e_n⟩⟨e_n|`.
     - The reverse gives an alternating moving sequence near a fixed vector, and a weak-* mass-escape example in §1.6.
   - **Common enclosing interval.**
     - The forward uses two limits in the AW2 enclosure.
     - The reverse uses `tau/144 ± K_2^+tau^2/2`.
     - Both certify that the `±tau` first-order densities differ by `sqrt(10)|tau|/36` at first order, so a comparison across couplings is rejected.
   - **Freeze and byte-identical replays** are protocol steps, verified below.
6. **Complete in both.** Both state "uniform in N at fixed spacing, not in a" with the `tau=96/g^4` illustration labelled as a different model (AX1). Both give the "quantitative boundary comparison" definition verbatim in substance.

**Checker counts.**
- **Forward:** 42 checks. The rejected mutations number 97 in total, 72 of them inside the 21 contract-control checks. The report's "All 21 contract controls … 97 in total" counts every rejection in the checker (finding N7).
- **Reverse:** 41 checks and 94 rejected mutations, 87 inside the control checks.

**Contract binding.** Both checkers verify the snapshot sha256 before parsing. A byte edit without rehash aborts both. A coherently rehashed target `1/125000` aborts both:
- the forward pins it to `1/1250000`;
- the reverse ties it to twice the AV1 target.

Each `check.py` sha256 recorded before evaluation equals the frozen file.

## Replays, closures and isolation

`replay_declared.py ay1` and `replay_loop.py ay1` each give identical output under normal and `-O` Python. Both verify:
- the closures file by file (forward 36 files, reverse 34);
- every premise snapshot against its repository source.

Both replay each producer under normal and `-O` Python into fresh external directories. All four runs reproduce `output/` byte for byte:

| Output | sha256 |
|---|---|
| forward `results.json` | `9a71a5f1…3df4` |
| reverse `results.json` | `569df79e…2e14` |

`tools/freeze.py verify` returns `verified` for both.

**Inventories.**
- **Reverse.** Its inputs equal AGENTS.md + the contract + the 28 `shared_premises` exactly: 30 files. The only skeptic files are `skeptic/av1.md` and `skeptic/aw1.md`, which are declared shared premises. It has no `triage.md`, Jung loop-2 response, deliberation, panel or `experts/` file, and no forward-AY1 or skeptic-AY1 file.
- **Forward.** Its inputs are those 30 plus the two forward-additional premises, `triage.md` and `experts/jung/loop2-response.md`: 32 files.

**Reads and scratch.**
- **Disclosed style reads.** Both disclose style and protocol reads outside `inputs/`:
  - forward: `tools/README.md` and `freeze.py`, parts of `forward/ax1/check.py`, and output conventions;
  - reverse: `tools/README.md` and `freeze.py`, portions of `reverse/av1/check.py` and `reverse/aw1/check.py`, and directory listings.

  None of these carries premise weight.
- **Incidental name exposure.** The reverse discloses that a final `git status` showed the *names* of `forward/ay1/check.py` and `report.md`, after its work was complete.
- **Non-repository channel.** The reverse's Jung-form sentence is "as relayed in my task": the forward-only Jung phrasing reached the reverse through its task prompt, not through a file (finding N3).
- **Scratch folders.** The names and mtimes (contents not opened) of `/tmp/claude-0/ay1-forward-private` and `/tmp/claude-0/ay1-reverse-private` match their disclosures.
- **Shared scratchpad root.** No file there was written after the AY1 freeze except the AX2 manuscript folder.
- **Timing.** The forward report was last written 02:49:43Z, after the reverse freeze at 02:48:44Z. It contains no reverse-specific construct (no Bures route, vector overlap identity or 288 variant). Isolation is shown by disclosure and content, not by mechanism.

## Mutation harness

Unmutated copies of both closures reproduce the frozen `results.json` byte for byte.

**22 must-abort source edits all abort at the intended check.**

Forward:
- `4rho`→`2rho`, straddling pin 72→66, and density item zeroed: all caught by `second_order_K2prime_itemized` through its second code path;
- the F2 rule replaced by F1, and straddling faces added to `F_R`: `family_F2_padded_interaction`;
- amplitude `tau/576`: `av1_tier_ii_bound_both_families`;
- `uniqueness_claimed` true;
- `continuum_claim` true;
- a contract byte edit;
- a rehashed target;
- the reverse report added as an input;
- the forbidden sentence `The AQ state is unique.` appended to the report (a mutation, not a claim).

Reverse:
- am2 item halved: `item3_K2_prime_versus_K2_plus`;
- the F2 rule replaced by F1;
- padding removed ("indexed support leaves the AM2 volume");
- the Bures bound doubled;
- `continuum_claim` true;
- a contract byte edit;
- a rehashed target (not twice the AV1 target);
- `triage.md` added as an input;
- the forward report added as an input;
- the forbidden phrase appended to the report.

**4 silent edits run to completion in the producer checkers and are caught only by this review's value validator:**
- forward: the supplementary lower end computed with `K_2'tau^2/2` ("not a lower bound");
- forward: the √2 of the orthogonal variant rounded down ("not an upper bound");
- reverse: `eps_R` pinned to 49 faces instead of 82;
- reverse: the straddling pin 72 replaced by 66.

The last two both give "`K_2'` differs from the skeptic's R-local itemization". The reverse has no second code path for its ledger, and the forward's second path does not cover its supplementary bounds or its variant.

## Blocking issues

None.

## Non-blocking findings

**N1. Two valid padding conventions.** The reverse says the padding "exists precisely so that each indexed support lies inside the AM2 volume". That is true for its declared-support indexing (`X_b=b+S`). With actual supports (forward, skeptic), F2 needs no padding for AM2; the padded sites then only fit I1's source empty-boundary form. The reduced density on R is unchanged either way.

**N2. Silent edits.** See the mutation harness. If the gate records the supplementary observation, it should use this review's exact values. AY2's checker should read `2D`, `K_2'` and `2K_2'tau^2` from the AY1 gate as exact rationals and reject any recomputed or smaller value.

**N3. Reverse isolation holds for repository inputs only.** The Jung sentence form reached the reverse through its task prompt, and it saw two forward file names. Both are disclosed; neither carries mechanism. Independence is further limited, as my contract review item 11 predicted, because the contract text and `selection-ay1.md` state `2D` and "first-order densities coincide", and the shared AV1/AW1 reports and reviews state the split and the pins.

**N4. Jung fields.** The reverse lacks `rate_in_N_claimed`; the forward exports it as false. `closeness_order` is `2` (forward) versus `[1,2]` (reverse). The gate should export `[1,2]`: order 1 for `2D`, order 2 after subtracting `rho^(1)_R`.

**N5. `2D` holds across couplings as well.** `P_R` does not depend on τ. Both producers show the `±tau` densities differ by at least 8.757e-10, yet both lie within `2D`. So `2D` alone is a common enclosing ball, and the boundary-comparison content is the first-order match with `2K_2'tau^2` (my contract review item 7). The gate sentence keeps "at the same coupling".

**N6. The contract exclusions use the phrase `the AQ state`.** Both producers quote them only verbatim and do not assert them: the forward in code spans, the reverse as "not claimed: …". My phrase scan (code spans removed; that phrase allowed only inside the negated verbatim exclusion) passes both reports.

**N7. Forward mutation-count wording.** "All 21 contract controls reject … 97 in total" counts every rejection in the checker; 72 sit inside the 21 control checks.

**N8. The `-tau` values are a replay** of the same `|tau|` formula, justified by the flip lemma (`rho^(1)_R` is odd). They are not a second observation.

**N9. Undeclared style reads** by both producers are disclosed and carry no premise weight.

## Contract wording defects (W1–W7, forward numbering) and my readings (R1–R6)

**Wording defects** (all non-blocking):

| id | defect |
|---|---|
| W1 | "(not the whole-box `K_2^+`)": `K_2^+` is uniform in N and observable-specific; the R-local trace-norm `K_2'` is about 4 times larger. Read it as "built from R-local pins", not "smaller" (reverse wording note 2; my R1) |
| W2 | The contract and preregistration exclusions contain `uniqueness of the AQ state`, which the Jung phrasing rule forbids. It is quoted only verbatim and is not asserted |
| W3 | `rate_claimed` (contract) versus `rate_in_N_claimed` (Jung). Export both as false |
| W4 | `state_provenance` names only F1's construction. F2 has its own diagonal extraction (reverse wording note 4) |
| W5 | F2's box geometry is not fixed. Both producers and I use the same centered `Lambda_N`, and the bounds hold for any finite region containing R |
| W6 | Item 5 lists "freeze; byte-identical replays" as controls, but they are not among the 21 ids. They are protocol steps, verified here |
| W7 | Verified, no defect: item 3's `−(c^(1)Ω_0^*+h.c.)` gives `+tau/144` with the AV1 convention, unlike AW1's item-3 display |

**My readings:**

| id | reading | outcome |
|---|---|---|
| R1 | `K_2'` versus `K_2^+` | Confirmed by both producers (`K_2'` ≈3.9995 `K_2^+`; floor `2rho` > `K_2^+`) |
| R2 | "Creations meeting R" leave 10 of 82 faces. The modern update-3 display `−(tau/72)Σ…` has the wrong sign | Both producers have 10 faces and `+tau/72` |
| R3 | The reverse route needs the **vector** overlap identity, and derivatives are taken in boxes only | The reverse states this as wording note 1 |
| R4 | `2D` alone is not a boundary comparison (N5) | Both producers exhibit the `±tau` separation |
| R5 | The template differs from Jung's loop-2 §4 text | Both producers fill both forms |
| R6 | `state_provenance` (W4), the box sequence (W5), and the limited reverse isolation (N3) | As recorded |

## Which value to bind, and why

**Bind:**
- **`2D`**: the pair constant and the preregistered target quantity, with D the AV1 gate forward tier (ii);
- **the 10-face `rho^(1)_R`**, with trace norm `sqrt(10)|tau|/72`;
- **the triangle `K_2'`** and **`2K_2'tau^2`**, as given above.

**Why.**
- **They agree.** The triangle `K_2'` is the same exact rational in all three computations.
- **They are purely rational.** They use only the admitted `rho=352JT`, `T` and the enumerated pins, with no irrational bracket.
- **The variants need more.** Each labelled variant rests on an extra step:
  - the √2 sector variant (forward ≈9487.94517; reverse ≈9487.94517, which differ only in the √2 bracket) needs sector orthogonality and a directed √2;
  - the 288 variant (≈10978.18) and the combined variant (≈7763.06) need the sharper majorant `G(t)−16<=288t/(1−8t)`.

  All are valid upper bounds, and all exceed `K_2^+`. The admitted-`eps` variant (≈13417.81) is larger than the headline and also valid.
- **The Bures constant** `4eps/(1+eps^2)` (≈2.72249055552e-8) is a valid labelled pairwise refinement. The contract names `2D`, so `2D` stays the headline.

## Limitations

- **Scope.**
  - Covered: the zero-selected patterned family, the cover R, fixed spacing and `|tau|<=10^-8`, with the two named families on centered cubes `N>=2`.
  - Not covered: literal vertex boxes (I1 §7), periodic or orthant boxes, nonzero selected triples, the uniform route-B model (its `K_2` was not transferred in AX1), weak coupling and the continuum.
- **Uniform local closeness on R only.** It is not uniqueness, whole-sequence convergence, a rate in N, translation invariance, or boundary independence of the dynamics or beyond R. Two limits may differ by up to `2K_2'tau^2` on R and without bound elsewhere.
- **The first-order density is a statement about a coefficient,** through the uniform remainder. It is not a τ-derivative of a subsequential limit.
- **`K_2'` is an upper bound,** 99.99% of it the generic AM2 majorant `4rho`, and larger than `K_2^+`. The labelled variants are valid, not headlines.
- **The supplementary two-sided observation** on `||rho_R−P_R||_1` ([4.3786e-10, 4.4055e-10]) is a labelled observation only. It is not a target, not a tier, and not a resolved interaction shift.
- **Inherited without re-proof:**
  - AM2's majorant, fixed point, exclusion and cutoff passage (applied to F2 through their hypotheses);
  - AV1's split and cutoff-vector removal;
  - AQ1's compactness and dynamics (named only);
  - AW1's `c^(1)` and amplitude lemma;
  - the I1 dictionary.

  Peter–Weyl/Haar orthogonality, Uhlmann/Fuchs–van de Graaf and Nachtergaele–Sims are cited, not machine-checked.
- **Independence is limited** by the shared premises and the task-prompt channel (N3). All agents are correlated model agents.
- **Producer checkers do not pin every exported value** (N2).
- **Priority.** Scientific priority is unverified.

## Advice for AY2 (planning only)

1. **Bind from the gate.** Read `2D`, `K_2'` and `2K_2'tau^2` from the AY1 gate as exact rationals, and reject recomputed or smaller values.
2. **State what remains unproved.** The obligations table should cover each of these, with the candidate route named:
   - uniqueness, which is not proved here (a candidate is Yarotsky-type uniqueness for weak perturbations, with its constants unevaluated);
   - whole-sequence convergence;
   - a rate in N;
   - translation invariance;
   - boundary independence of the dynamics (a Lieb–Robinson boundary argument for `Phi` versus `Phi'`);
   - a third-order or order-by-order locality statement. The second-order densities are also box-local for `N>=3`, but proving it needs a uniform third-order remainder.
3. **The supplementary lower bound** may be discussed as a labelled observation. It needs its own contract before any admission.
