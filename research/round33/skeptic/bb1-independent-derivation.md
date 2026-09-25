# BB1 independent derivation before producer comparison

**Standing.** I wrote this after the BB1 contract froze (`frozen_at` 2026-09-24T23:36:46Z, sha256 `30400d2e…8018`). I have not opened, listed or read `research/round33/forward/bb1/`, `research/round33/reverse/bb1/`, `research/round33/forward/bb2/` or `research/round33/reverse/bb2/`. The one exception, which the task permits: I ran `find` on the two BB1 `inputs/` folders and hashed each file against the repository (35 files each, all byte-identical, equal to the contract-derived list).

**Sources:**
- the frozen contract, `advisor/selection-bb1.md`, `advisor/plan.json`, `advisor/deliberation-2.md`, and `experts/modern/bb-targets-proposal.md` including its advisor-only §7 (the recorded previews);
- my Round33 record: `triage.md` §(a), `prospective-controls.json`, `loop2-review.md`, `bb-contract-review.md`/`.json`, and the BA1 package (format);
- the premises: BA1 gate, forward and reverse reports and my BA1 review; AV1 forward and reverse reports and gate; AM2 forward report and gate; AQ1 gate; I1 forward report; AW1, AY1 and AY2 gates; `AGENTS.md`.

**Scratch.** All scratch work stayed in the private folder `/tmp/claude-0/skeptic-bb1-private/`. For about one command, the two inventory name lists sat in `/tmp/claude-0/` before I moved them there; they were my own files. I read nothing in any other agent's scratch folder, including my earlier Round33 scratch folders. Every number here was recomputed.

**Name-only exposures, disclosed:**
- `git status` printed nothing.
- `git log` printed commit subjects up to dd4d44c "Round33 README: BB1/BB2 in production". None of them carries BB1 producer content.
- `git show --stat 45a87be` printed abbreviated paths of the committed `inputs/` snapshots of the BB1/BB2 producers (names only).
- A later `git log` showed commits made during this review: the BB2 forward and reverse producers (d05efda, 17c0ecf), the BB2 skeptic package (8921539) and the plan freeze entry (43eb922). I read only the plan entry. The BB2 files were seen as commit subjects only, and `programs.json` already carried the BB2 skeptic's key when I added mine.

**Correlated ancestry.** I am a model-agent skeptic with correlated ancestry. My triage §(a).4 proposed both BB1 routes and the marginal-locality lemma form. My pre-freeze review wrote 17 of the frozen texts. What follows is a re-derivation, not independent discovery or human review.

**Exactness.** Exact values come from `bb1_check.py`:
- 88 checks, byte-identical under `-B` and `-B -O`;
- all 37 contract controls as 106 damaging mutations;
- rationals with directed enclosures (exp from above and below, `log x ≥ 2(x−1)/(x+1)`, square-root brackets).

Every decimal below is a preview. Human project author: Hruday N M (BUNZEEY).

## 1. Model and the admitted objects used
**Model.** The model is `AQ_patterned_zero_selected`:
- SU(2) Kogut–Susskind form on Z³ at fixed spacing, with coarse 24-link factors;
- selected triple (0,0,0) with the Haar product reference;
- 21 omitted faces per anchor entering as `−(τ/3)W_f`;
- both signs, |τ| ≤ 10⁻⁸.

**Families.** F1 (AQ1 whole stars) and F2 (I1 §6 faces with padding), on Λ_N = [−N,N]³ with N ≥ 2, together with general complete-factor volumes of one prescription containing Λ_N. The observable is the reduced density ρ_Y of the normalized finite-box ground vector, on R = {0,e_z} and on finite complete-factor regions Y ⊂ Λ_N, in the trace norm on B(H_Y).

**Admitted.** In each on-site cutoff space Q_L:
- the AM2 creation fixed point `ψ = ∏_I(1−ĉ_I)Ω`, with `c_I ∈ ⊗_{x∈I}Q_xH_x`;
- `J ≤ 28|τ|`, `G(R) < 148/7`, `G'(R) < 352`, R = 1/64;
- the exact first order `c^(1) = −(τ/72)ΣW_fΩ_0` on owner sets M_f with `|M_f| ∈ {2,3}` and diameter 1;
- `t_1 = 49|τ|/144`, and the AV1 anchored bound `t ≤ t̄ = t_1/(1−352J) = 49/14398580736 ≈ 3.4031e-9`.

**BA1.** The disc bound is `T(ρ) = (49ρ/144)/(1−28ρG'(R))`. The gate bound value is `K = 2T(64|τ|) = 49/111790368 ≈ 4.3832e-7`, admitted **for u ∈ R** at q = 1/64. The forward norm constant is `K_own = T_w/(1−Γ) = 19140625/86785322066496 ≈ 2.2055e-7` (w = 64, labelled). The forward's telescoped general value is `K_gen = 2734375/12204185915601 ≈ 2.2405e-7` (labelled). `w_max = 390625/148` and `τ_* = 1/37888`.

**Cutoff.** AV1 F20–F23 (Eckart, untruncated gap 1/2) for F1 boxes. AY1's item-by-item list, including cutoff-vector removal, for F2 boxes with padding.

## 2. The AV1-type decomposition for a region Y
**Setup.** Put `A_Y = {I : I∩Y ≠ ∅}` and `X_c = ∏_{I∈A_Y}(1−ĉ_I)`. Let φ be the outside vector `∏_{I∩Y=∅}(1−ĉ_I)Ω_{Y^c}` and let `O = ∪_{I∈A_Y}(I∖Y)` be the straddle region. Creations commute, so `ψ = X_c(Ω_Y⊗φ)`, and exactly

`ρ_Y = N_c(ω_O)/Tr N_c(ω_O)`, with `N_c(ω) := Tr_O[X_c(P_Y⊗ω)X_c^*]` linear in ω, and `ω_O = Tr_{Y^c∖O}|φ⟩⟨φ|/||φ||²`.

**Tr N_c ≥ 1 (AV1 orthogonality, F09).** Every nonempty family in X_c contains a creation excited at some y ∈ Y. So `(P_Y⊗1)X_c(Ω_Y⊗v) = Ω_Y⊗v`, and for every density ω on O, `Tr N_c(ω) = Σ_k p_k||X_c(Ω_Y⊗v_k)||² ≥ 1`. As an operator on O, `G_1 := ⟨Ω_Y|X_c^*X_c|Ω_Y⟩ ≥ 1`. The fixture checks `G_1 − 1 ⪰ 0` by an exact LDLᵀ decomposition.

**Lipschitz bound in the outside state.** For positive A, B with Tr ≥ 1,

`||A/TrA − B/TrB||_1 ≤ 2||A−B||_1/max(TrA,TrB)`.

Hence `||ρ_c(ω)−ρ_c(ω')||_1 ≤ 2||N_c(ω−ω')||_1 ≤ 2||X_c||²||ω−ω'||_1`.

Refinement: write `X_c = X_in + X_s`, where X_s collects the terms with at least one straddler. The `X_in⊗X_in` part vanishes on the traceless ω−ω', so

`||ρ_c(ω)−ρ_c(ω')||_1 ≤ 2(2||X_in||·||X_s|| + ||X_s||²)·||ω−ω'||_1`.

On R: `L_ω ≤ 2[2(1+t̄)²(2t̄+t̄²) + (2t̄+t̄²)²] ≈ 2.7225e-8` (exact rational in `results.json`). Tier exact_first_order, route iterated_split. **This is a Lipschitz constant, not a rate.** Used as a per-shell factor it would give a rate of 2.7e-8 per step, below the BA1 floor `q_min = 148/390625` (check `density_lipschitz_not_decay`).

**Lipschitz bound in the coefficients.** At a fixed pure outside vector φ̂, take `u = X_c(Ω_Y⊗φ̂)` and `v = X_{c'}(Ω_Y⊗φ̂)`, with norms at least 1. The sine bound gives

`||ρ_c−ρ_{c'}||_1 ≤ 2||u−v||/max(||u||,||v||) ≤ 2||X_c−X_{c'}||`.

A mixed outside state is handled by purifying it. Charging each family to distinct representative sites of Y gives

`||X_c−X_{c'}|| ≤ ∏_{y∈Y}(1+t̄+D_y) − ∏_{y∈Y}(1+t̄)`, where `D_y = Σ_{I∋y}||c_I−c'_I||`.

On R this is `(D_0+D_{e_z})(1+t̄+K)`. For a large Y it carries `e^{(t̄+Kq^{d_Y})|Y|}`: see contract review R7, where it is absorbed in the nontrivial range.

**The fixtures:**
- **Split check.** With R = {r}, O = {o}, a mixed ω = [[2/3,1/6],[1/6,1/3]] and a second ω' = [[1/2,−1/5],[−1/5,1/2]], the fixture gives Tr N = 659/600 and 841/800. It also gives `||ρ(ω)−ρ(ω')||_1 ≤ 0.17487 ≤ 0.37857 ≤ 2||N(ω−ω')||_1`, as directed brackets.
- **Product charging.** Charging the product of region sizes s_k = k+1 at amplitude 1/10 gives `(k+1)!/10^k`, which increases from k = 9. Per-site charging gives a geometric series.

## 3. The derivative identity and the near term (constant 2, η = 0)
**Derivative identity.** Take `c(λ) = c + λδ`, with δ = c' − c on the common volume. The coefficients are zero-extended; padding sites carry vacuum. Since `δ̂_Iĉ_I = 0`,

`∂_λψ(λ) = −δ̂ψ(λ)`, where `δ̂ = Σ_I δ̂_I`.

This is checked as an exact polynomial identity in λ.

**Derivative of the state.** For self-adjoint A on Y,

`dω_λ(A)/dλ = −ω(A;δ̂) − ω(δ̂^*;A) = −2Re ω_λ(A;δ̂)`.

Hence `||ρ_Y(c')−ρ_Y(c)||_1 = sup_{−1≤A≤1}|ω_1(A)−ω_0(A)| ≤ 2 sup_λ Σ_I |ω_λ(A;δ̂_I)|`.

**Near supports (I∩Y≠∅).** By Cauchy–Schwarz,

`|ω(A;δ̂_I)| ≤ √Var_ω(A) · ||δ̂_Iψ||/||ψ|| = √Var(A) · ||δ_I|| · ||⟨Ω_I|ψ||/||ψ|| ≤ ||δ_I||`,

and this is checked exactly on a fixture. The near part is therefore `2Σ_{I∩Y≠∅}||δ_I|| ≤ 2Σ_{y∈Y}D(y)`: η = 0 in the frozen lemma form, with no |Y|-exponential. The interpolated collections are convex combinations, so every per-site norm bound holds uniformly in λ.

## 4. The far term: the truncated-correlation split recursion
**Reduction (exact identity).** Let Z be a region, E an operator on Z, and B = δ̂_I with I∩Z = ∅. B commutes with every creation and acts outside Z. Split ψ = X(Ω_Z⊗φ) with respect to Z, and put `G_E := ⟨Ω_Z|X^*EX|Ω_Z⟩`. This is an operator on the straddle region; its part with no straddler is the scalar `g_E·1`. Write `H_E := G_E − g_E·1` and `E' = E − ω(E)`. Then

`ω(E;B) = ω_φ(H_{E'};B)/ω_φ(G_1)`, with `ω_φ(G_1) ≥ 1`.

The identity is verified exactly on a three-qubit fixture: both sides equal `171988775/79003421523`. Its algebra is the product-ordering split of AV1 applied to a truncated correlation. H_{E'} is a sum over pairs (F,F') of families of disjoint supports meeting Z with at least one straddler. Each term `H_α` acts on `S_α = ∪(J∖Z)` over the straddlers J of α, and has norm at most `||E'||∏_{J∈α}||c_J|| ≤ 2∏||c_J||`.

**Recursion.** If S_α meets I, then `|ω_φ(H_α;B)| ≤ ||H_α||·||δ_I||`: this is the variance bound, with no normalization. Otherwise re-split φ with respect to S_α. That re-split is the source of the issue below.

**The intermediate normalization (contract review R6).** Re-splitting with respect to S_α expands every family of supports meeting S_α. The family sum is `∏_{s∈S_α}(1+Σ_{J∋s}||c_J||)`, about `e^{t̄|S_α|}` on each side. With |S_α| up to |J|, this factor is not controlled by any diameter weight uniformly in N:
- with `|J| ≤ 8·2^{diam J}`, `e^{16t̄·2^d}` exceeds `w_max^d` from d = 33;
- with `|J| ≤ (1+d)³`, from d = 34021.

**Per-site charging of sizes controls the count of the next straddlers, not this factor.** I close the recursion with a cardinality weight.

**Lemma MW (mixed-weight contraction, proved).** Put `wt(J) = w^{diam J}e^{b|J|}` with w ≥ 1 and b ≥ 0, and `||c||_{w,b} = max_u Σ_{J∋u}wt(J)||c_J||`.
- In a nonzero AM2 word (X; I_1,…,I_k), every I_j meets X and M ⊂ X∪⋃I_j.
- So `diam M ≤ d_X + Σdiam I_j`, with d_X = 1 (BA1 Lemma W), and `|M| ≤ |X| + Σ|I_j|` with |X| ≤ 4.
- Hence `wt(M) ≤ w e^{4b}∏wt(I_j)`. AM2's counting uses only the norms attached to the creation slots: the 16 output sets, `|I_j| ≤ |M|+4`, the 1/|M| cancellation and the 2^k products. It therefore passes through unchanged:

  `||L_k(c_1,…,c_k)||_{w,b} ≤ w e^{4b}·J·16·8^k(1+5k/4)·∏||c_j||_{w,b}`.

  **The loss is paid once per interaction, never per creation.**
- **Self-map.** `J w e^{4b} G(R) ≤ R` exactly when `w e^{4b} ≤ w_max = 390625/148`. Weights are at least 1, so the ball lies inside the AM2 ball, and the unique fixed point lies in it.
- **Exact first order.** `||L_0||_{w,b} ≤ w e^{3b} t_1`, since owner sets have diameter 1 and at most 3 sites. So

  `T_{w,b} = w e^{3b} t_1/(1 − J w e^{4b} G'(R))`.

**Attainment.** Over 13 881 words of order at most 2 built from actual owner sets around the star, `|M| − Σ|I_j|` reaches 4 only for the generic k = 0 count; it is at most 3 for k ≥ 1 (check `cardinality_loss_and_face_order_count`). **Alternative for the reverse (labelled):** owner sets have at most 3 sites, so c_M has Taylor order at least `⌈(|M|−1)/2⌉`. On the BA1 disc this gives `Σ_{J∋x,|J|=m}||c_J|| ≤ T(ρ)(|τ|/ρ)^{⌈(m−1)/2⌉}`.

**Claim (induction on the number of supports).** Assume, for every subcollection and every λ:
- `t' ≥ sup_x Σ_{J∋x}e^{b|J|}||c_J||`;
- `M ≥ sup_x Σ_{J∋x}θ^{diam J}e^{b|J|}||c_J||`, with θ ≥ 1.

Put β = 2t' and 0 < ε ≤ b − β. Let the data satisfy `D(x) ≤ Δ_Z θ^{d(x,Z)}`. Then, for every E on Z with ||E|| ≤ 1,

`Ψ(Z) := Σ_{I∩Z=∅}|ω(E;δ̂_I)| ≤ A |Z| e^{β|Z|} Δ_Z`, with `A = 4M/(εe − 4M)`.

*Proof of the step.* Take `Δ_{S_α} ≤ Δ_Zθ^{maxdiam(α)}` and `Σ_{x∈S_α}D(x) ≤ |S_α|Δ_Zθ^{maxdiam(α)}`, and use:
- `|S|e^{β|S|} ≤ e^{(β+ε)|S|}/(εe) ≤ ∏_{straddlers}e^{b|J|}/(εe)`;
- `θ^{maxdiam} ≤ Σ_{J_0}θ^{diam J_0}`;
- the families other than J_0 contribute at most `∏_{z∈Z}(1+t')² ≤ e^{2t'|Z|}`, each member charged to a distinct representative site;
- the straddlers J_0 contribute at most `|Z|M`, times 2 for the side.

This gives `Ψ(Z) ≤ (1+A)(4M/(εe))|Z|e^{2t'|Z|}Δ_Z`, which is at most `A|Z|e^{β|Z|}Δ_Z` when β = 2t' and `A = 4M/(εe−4M)`. If Z has no straddler, the state is a product across Z and Ψ = 0. ∎

**Proof weights (declared before any constant).**
- θ = 1/q = 64 and e^b = 9/8, so b ≥ 2/17 by the log bound.
- The loss is θe^{4b} = 6561/64 ≈ 102.5 ≤ w_max.
- `t' = T_{1,9/8} = 3969/819070669568 ≈ 4.8457e-9`, so β = 2t' ≈ 9.6915e-9 ≤ 10⁻⁸. That makes `e^{β|Y|} ≤ e^{|Y|/10^8}`, the frozen factor.
- `M = T_{64,9/8} = 3969/12670669568 ≈ 3.1324e-7`.
- `ε ≥ 2/17 − β`.
- **A ≈ 3.9180e-6** (exact rational in `results.json`).

**Lemma form (frozen control).**
- η = 0.
- `κ(I) ≤ 2A|Y|e^{β|Y|}·64^{−d_∞(I,Y)}` for I∩Y = ∅, with w' = 64 and p ≡ 1. On R, `κ_0 = 4Ae^{2β} ≈ 1.567e-5`.
- The assembly uses the chain (Δ-profile) form, not a lattice sum of κ (review R2).

**For comparison: diameter-only per-site charging (the contract's reverse wording).**
- With |I| ≤ 8·2^{diam I} at creation weight 2θ = 128, the per-level factor is `32T(128|τ|) ≈ 1.4116e-5`, so `η = 32T_128/(1−32T_128) ≈ 1.4116e-5`.
- The recorded preview bounds T_128 by `T_* = 49/4036608`, which gives `η_str = 49/126095 ≈ 3.886e-4`.

Both leave the intermediate normalization uncharged. The constants are admissible only if a packet charges it separately.

## 5. The every-site coefficient input
**Form (b): BA1 reverse Theorem 4.1 with R replaced by {u}. This is a BB1 lemma; the gate admits u ∈ R only.**
1. **Lemma 2.2 at u.** A nonzero order-n term on M ∋ u whose family contains a source piece Y has `n ≥ 1+⌈d_∞(u,Y)⌉`. The contract form is ⌈d⌉.
2. **The source-site lemma, all sizes.** Every face present in one volume and not the other has all its sites at |p|_∞ ≥ N:
   - a new F1 star has some b_i ∈ {N, −N−1};
   - a new F2 owner set meets |p_i| = N+1 and has diameter 1;
   - an extra F2 face of F1 against F2 is anchored at b_i = N, and all its sites share p_i = N;
   - in a comparison of volumes containing Λ_N, a symmetric-difference term contains a site outside Λ_N and has diameter 1.

   Hence `d_∞(u, sources) ≥ N − |u|_∞`.
3. **The circle bound** `2T(ρ)` is uniform in u.
4. **Schwarz.** For every u ∈ Λ_N, every comparison, both signs and each Q_L,

   `Σ_{I∋u}||c¹_I − c²_I|| ≤ K q^{N−|u|_∞}`, with `K = 2T(64|τ|) = 49/111790368`.

**Enumeration (check `every_site_sources_all_centered_pairs`).** All 27 pairs of centered boxes of F1 or F2 with smaller size 2, 3 or 4 were enumerated, with larger boxes up to Λ_5. The minimum `|p|_∞` over source sites equals N exactly. Site by site on Λ_2 and Λ_3, `d_∞(u, sources) ≥ N−|u|_∞` everywhere. The bound is attained at 81 of 125 sites for F1 against F2 on Λ_2, and at every site for the nested pairs. Non-centered cuboids at N = 2, 3 behave the same way for both prescriptions.

**Form (a), labelled.**
- `K_own = T_w/(1−Γ)` with `Σ_{I∋u}||δ_I|| ≤ K_own q^{d_∞(u,B)}`.
- B is the shell for nested comparisons (exponent N+1−|u|), the positive outer layer for F1 against F2 (N−max_i u_i), and the sites outside Λ_N for a direct general comparison.
- All of these are at least N − |u|_∞.

**Outside the smaller box.** `D(x) ≤ 2t̄ = 2·49/14398580736`. The data profile is `D(x) ≤ Δ_Y·64^{d(x,Y)}`, with `Δ_Y = max(K, 2t̄q)·q^{d_Y} = Kq^{d_Y}`, because `|x|_∞ ≤ max_Y|y|_∞ + d(x,Y)`.

## 6. Assembly at q = 1/64 (both signs identical; every comparison)
The per-site data are the same for all five comparisons of `parameters.comparisons`: F1 N→N+1, F2 N→N+1, F1 against F2 at fixed N, any two centered boxes compared directly (the face sets are totally ordered), and two volumes of one prescription containing Λ_N compared directly. So one pair of constants covers them all:

- **R form:** `||ρ¹_R−ρ²_R||_1 ≤ 2[Kq^N + Kq^{N−1} + 2Ae^{2β}Kq^{N−1}] = C q^{N−1}`, with `C = 2K(1+q+2Ae^{2β})`.
- **Region form:** `||ρ¹_Y−ρ²_Y||_1 ≤ 2K(1+A)·|Y|e^{β|Y|}q^{d_Y} ≤ c_site|Y|e^{|Y|/10^8}q^{d_Y}`, with `c_site = 2K(1+A)`.

| constant | value | target | margin |
|---|---|---|---|
| **C**, form (b) every-site (u=0 at q^N) | ≈ **8.9035e-7** (exact rational in `results.json`) | 1/250000 | 4.4926 |
| C, BA1 gate statement at both sites of R | ≈ 1.7533e-6 | 1/250000 | 2.2814 |
| **c_site**, form (b) | ≈ **8.7664e-7** | 1/500000 | **2.2814** |
| C / c_site, form (a) K_own (labelled) | ≈ 4.4800e-7 / 4.4110e-7 | — | 8.93 / 4.53 |
| C, form (a) with the forward's K_gen (labelled) | ≈ 4.5511e-7 | — | 8.79 |
| C, split (sine-bound near term, far `A' = 2M/(εe−2M)`), every-site / R-only | ≈ 8.9034e-7 / 1.7533e-6 | — | 4.4927 / 2.2814 |
| density union (factor 2): C every-site / R-only / c_site | ≈ 1.7807e-6 / 3.5066e-6 / 1.7533e-6 | labelled only | 2.25 / 1.14 / 1.14 |

**Refinements, labelled only:**
- The sharp count multiplies every constant by q.
- First-order cancellation makes the near data quadratic in τ, because every face through a site u with |u|_∞ ≤ N−1 is common. Its τ-ratio is about 10⁴, outside the linear bracket.

## 7. The secondary pair (labelled) at q_2 = 151552|τ| = 592/390625
- **Input (labelled re-instantiation of Theorem 4.1).** At `ρ_2 = |τ|/q_2 = 1/151552`, the disc satisfies `28ρ_2G(R) = 1/256 ≤ R`, and `K_2 = 2T(ρ_2) = 49/10202112 ≈ 4.8029e-6`. K_2 is exactly τ-invariant.
- **Far term.** θ_2 = 1/q_2 = 390625/592 and e^b = 9/8, so the loss is 1056.9 ≤ w_max. `M_2 = 3969/1112183552` and A_2 ≈ 4.4638e-5.
- **Results:**
  - C_2 ≈ 9.6213e-6 every-site (margin 5.20), or 1.9213e-5 with both sites of R at q_2^{N−1} (margin 2.60);
  - c_site,2 ≈ 9.6063e-6 (margin 2.60 against 1/40000).
- **Scaling.** The ratios are 1.0015 and 1.0000, inside [99/100, 101/100]. The ratio for q_2 is exactly 100.

## 8. Crude tier (reported, never a target)
- **Input.** `K_c = 2·28(64|τ|)G(R) = 296/390625`. The crude mixed norms are `J·θe^{4b}·G(R)` and `J·e^{4b}G(R)`, giving `A_c ≈ 7.65e-3` and `β_c = 242757/12800000000 ≈ 1.8965e-5`.
- **Results.** C_crude ≈ 1.5624e-3 every-site, or 3.0542e-3 R-only. Both miss 1/250000 and are retained.
- **Region form.** β_c exceeds 10⁻⁸, so the crude region constant (≈ 1.527e-3) cannot be written in the frozen form. It carries its own exponent and is labelled.

## 9. Cutoff order
1. Everything above holds in each Q_L with constants independent of L. Compression keeps supports and J. First-order face vectors are exact for L ≥ 24, and for smaller L the counts only decrease. K, t̄, T and T_{w,b} are therefore uniform in L.
2. At fixed N, for each box separately, the AV1 cutoff-vector removal applies: F20–F23, with `1−|⟨ψ,ψ_L⟩|² ≤ 2(E_{0,L}−E_0) → 0` from the untruncated gap 1/2. F1 boxes use AM2 §6 directly. F2 boxes with padding use the AY1 item list, and non-centered F2 volumes need that list re-verified (review R10). So ρ^{box,L}_Y → ρ^{box}_Y in trace norm, and the bound survives in the closed ball.
3. The N and L limits are never exchanged. No statement is made inside a fixed Q_L as N→∞.

Fixtures:
- **Eckart**, with gap 1/2: the pairs are (8/9, 20/9), (4/9, 32/45) and (0, 0). Without a gap (diag(0,0,1)), a vector with the ground energy is orthogonal to the ground vector.
- **Limit order.** For `x(N,L) = min(1, L/N)`, `lim_N lim_L = 1` but `lim_L lim_N = 0`.

## 10. The polymer route: KP feasibility and the mixed-weight loss
**Polymer representation.** Polymers are overlap-connected pairs (F,F') of families of disjoint supports with ∪F = ∪F' = X_γ. The activity satisfies `|w(γ)| ≤ ∏_{J∈F⊔F'}||c_J||`, `e^{a|X_γ|} = ∏e^{(a/2)|J|}` and `diam X_γ ≤ Σ diam J`.

**KP bound.** A spanning-tree branching bound with side labels, and at least one child because both F and F' are nonempty, gives

`sup_x Σ_{γ∋x}|w(γ)|e^{a|X_γ|}W^{diam X_γ} ≤ 2Z̄·Σ_{J∋x}ν(J)|J|e^{|J|Z̄} ≤ 4T²/(eζ)`,

where Z̄ = 2T, `b ≥ a/2 + Z̄ + ζ` and `T = T_{W,b}`.

**At (a, W, e^b) = (1/1000, 1024, 9/8).**
- The loss is W e^{4b} = 6561/4 ≈ 1640 ≤ w_max.
- T ≈ 5.918e-6 and ζ ≈ 0.11714.
- The KP sum is at most ≈ 4.40e-10 ≪ a = 10⁻³.

KP is feasible by about six orders of magnitude. **The cardinality factor is essential** (fixture below). The far factor via ℓ∞ shells around R is `S(qW) = Σ_{d≥1}(24d²+8d+2)(qW)^{−d}`, with S(16) ≈ 2.636. At the recorded preview's W_c = 390625/296, `S = 99977074261152768/51346528044814241 ≈ 1.9471` (reproduced exactly), and the recorded structure gives η_far ≈ 1.8948e-4. The recorded polymer preview (R-only input) is C ≈ 1.75361e-6.

## 11. Scaling τ → τ/100 (exact ratios, same formula)
| constant | ratio | bracket |
|---|---|---|
| C (every-site / R-only) | 100.6292 / 100.6288 | [95,105] ✓ |
| c_site | 100.6288 | [95,105] ✓ |
| C, form (a) | 101.2616 | [95,105] ✓ |
| recorded split, R-only | 100.6284 | [95,105] ✓ |
| input K | 4340004/43129 exactly | — |
| C_2 / c_site,2 | 1.00150 / 1.00000 | [99/100,101/100] ✓ |
| q_2 | exactly 100 | exactly 100 ✓ |

## 12. Exact finite fixtures for the traps
Every fixture is labelled `model_is_finite_graph: true` and `transfers_to_aq: false`.
- **Coefficient decay is not marginal decay** (AV1 F13). On r, o, o', take c_{r,o} = 1/3 and change c_o from 1/2 to 0. The coefficients meeting R do not change, yet ρ_r moves from `[[45/49,6/49],[6/49,4/49]]` to `[[9/10,0],[0,1/10]]`.
- **Second-order propagation.** On the chain r–o–o'' with straddlers a = c_{r,o} and b = c_{o,o''}, change only e = c_{o''}.
  - As exact polynomials: numerator of ρ_01 = −abe, and Z = (1+a²)(1+e²)+b².
  - At a = 1/3, b = 1/4: ∂_eρ_01(0) = −12/169, and at e = 1/5, ρ_01 = −12/877.
  - "First-order propagation" (a zero derivative) and a per-link factor a² both fail.
- **Normalization.**
  - With 0 to 3 decoupled spectators (coefficient 1/6), ρ_R is identical, while `⟨ψ,P_Rψ⟩` runs through 145/144, 5365/5184, 198505/186624 and 7344685/6718464 (AV1's values).
  - **Global fidelity:** flipping the spectator coefficient to −1/6 multiplies the squared overlap by (35/37)² per spectator. The infidelity grows 7.3e-8 → 0.105 → 0.199 → 0.284, while the R-marginal difference is fixed.
- **Straddling supports.**
  - e² = a²/(1+b²) = 4/45 (first order in a), while the off-diagonal is of order ab.
  - Only supports contained in R move ρ_R at first order. `{r0,o}`, `{r1,o}` and `{r0,r1,o}` (strictly containing R) have zero first-order marginal and a nonzero second-order block (contract defect D1).
- **Split.** Tr N ≥ 1 and the ω-Lipschitz inequality on a mixed outside state; product charging increases with depth, per-site charging is geometric (§2).
- **Polymer identity.** On four sites with eight supports, (ψ,ψ) = 44112048886673/31361328698700 equals the hard-core sum over 28 polymers. 474 family pairs with different excitation sets contribute zero.
- **Cardinality factor.** Take J_0 = {0,1,2,3} (u = 1/20) and four P_k = {k,k+4} (v = 1/20); the enumeration finds exactly the 5 diagonal polymers.
  - KP with `a(γ) = a|X_γ|` (a = 1/100) holds.
  - The single-polymer part of the cluster sum incompatible with ({J_0},{J_0}) is 1/80, which exceeds the no-cardinality bound a = 1/100.
- **Cutoff:** Eckart and limit order (§9). **Topology:** a moving vector e_n has trace distance 2 from e_1 while ⟨e_1, ρ_n e_1⟩ = 0.
- **Zero-free region.** The bilinear normalization 1 + 4z² of ψ(z) = Ω − 2z|11⟩ vanishes at z = i/2.
- **Outside vector.** φ_out = (1 − ½ĉ_o)Ω has number energy 1/5 > 0, so it is not an outside ground state and no gap argument applies to it.

## 13. What I will require of each producer
**Both producers:**
1. **Model and weights.** State the model, the metric (coarse ℓ∞, d_X = 1) and the proof weights as exact values before any constant. Show that each weight passes the weighted self-map after the cardinality loss.
2. **The decomposition.** Give `ρ_Y = N_c(ω_O)/Tr N_c(ω_O)` with Tr N_c ≥ 1, and both Lipschitz bounds with constants, tier and route. The ω-Lipschitz constant must never be used as a rate.
3. **Every-site input.**
   - Form (b) is proved in full: Lemma 2.2 at u, the source-site lemma for all five comparisons, the uniform circle bound and Schwarz.
   - Form (a) names B and the exponent per comparison, and labels K_own or K_gen.
   - Outside Λ_N the input is 2t̄, never zero and never the R-only gate statement.
4. **The marginal-locality lemma** in the frozen form, with η, κ_0 (|Y|-dependence stated), w' > 1 and p exact. The assembly stays linear in |Y|.
5. **Intermediate normalization (review R6).** Show where the family sums of every re-split or polymer region are charged: a cardinality factor, the mixed-weight lemma or the face-order count. Diameter weights alone are not uniform in N.
6. **Every comparison.** All five comparisons, directly; a union factor of 2 is labelled only. Both signs, each Q_L, then fixed N untruncated via F20–F23 (F2 via AY1, re-verified for non-centered volumes).
7. **Constants.** R form and region form at q = 1/64, and the secondary pair (labelled) with its re-instantiated input proved. The crude tier is reported separately, with its own region exponent. The τ/100 ratios are computed from the same formula.
8. **Wording and controls.**
   - All the fixtures of required item 5 are exhibited, whatever the route; the straddling fixture follows the reading of D1.
   - The template is quoted once. The 11 gate fields are exported as frozen.
   - All 37 controls run as damaging mutations. Replays are byte-identical.

**Forward (polymer_kp):**
- The polymer identity is derived, with the activity bound and the KP condition at an explicit a, weights and tree majorant, including the cardinality factor.
- Lemma MW is proved in full, loss w e^{4b} per interaction.
- The real-parameter derivative is used, and nothing is said about analyticity of ρ_Y.
- The far sum is given with its shell counts. Its η_far may be as large as about 1.9e-4 (recorded structure) and still meet the targets.

**Reverse (iterated_split):**
- The AV1 split is applied recursively to the outside state, with multi-straddler families written out.
- Sizes are charged per site, never as a product of growing regions.
- The near-term region factor of review R7 is stated.
- The intermediate normalization is charged (R6).
- The inventory equals the 35 contract-derived files; I hashed them.

## 14. Predictions (the post-comparison flags any difference)
| quantity | prediction |
|---|---|
| near-term constant | 2 (derivative) or 2(1+t̄+K) on R (split); η ≤ 4e-4 |
| far relative factor | 3.9e-6 (mixed weight θ = 64, e^b = 9/8) up to 1.4e-5 (per-site, T_128), 3.9e-4 (recorded η_str with T_*), 1.9e-4 (recorded polymer η_far) |
| C, form (b), u = 0 at q^N | ≈ 8.90e-7 (8.9035e-7 here; up to ≈ 8.907e-7 with η_str) |
| C, R-only gate input | ≈ 1.7533e-6 to 1.7540e-6 (recorded split `352765230433/201124673670833280`) |
| C, form (a) | ≈ 4.48e-7 (K_own) to 4.553e-7 (K_gen with η_str) |
| c_site | 8.766e-7 (form b) to 8.770e-7 with η_str; 4.411e-7 (form a) |
| secondary | C_2 ≈ 9.62e-6 to 1.95e-5; c_site,2 ≈ 9.61e-6 to 9.77e-6 |
| crude | C ≈ 1.54e-3 to 3.05e-3; fails, retained |
| τ ratios | ≈ 100.63 (form b), ≈ 101.26 to 101.28 (form a); secondary ≈ 1.0000 to 1.0030; q_2 exactly 100 |
| KP | feasible with a cardinality factor; KP sum ≪ a |

**Flagged as errors:**
- A C below 4.48e-7, or a c_site below 4.41e-7, with an exact_first_order label and no labelled refinement.
- A constant meeting 1/250000 with a crude input.
- A density-union constant reported as the fifth comparison's C.

## 15. Producer-error checklist
1. **Coefficient decay stated as density decay.** Straddling supports dropped or charged at first order only. Normalization by 1+O(t²) or by the global overlap.
2. **R-only gate input at far sites.** Form (b) cited as admitted. An exponent above N−|u|_∞. Zero data outside Λ_N.
3. **An intermediate region renormalized without a cardinality control (R6).** A mixed-weight lemma cited from BA1. A loss charged per creation, or above w_max.
4. **Lipschitz constants of the fixed-point map or the density map used as a rate.** For reference: 77/390625, 37/6249384 and L_ω ≈ 2.7e-8.
5. **A κ-form lattice sum that makes the region constant grow like |Y|².** An R constant reused on Y. A crude region constant written with the frozen e^{|Y|/10^8}.
6. **Cutoff.** Limits swapped, eigenvalue convergence only, or F2 general volumes passed to L → ∞ without the AY1 items.
7. **The fifth comparison through the union reported as C.** Telescoping at the density level.
8. **Analyticity of ρ_Y claimed.** A bracket changed after evaluation. A rate other than the frozen pairs reported as the result. A rate in a. Any uniqueness claim, any whole-sequence claim (BB2), or any phrase on the forbidden list.
9. **Arithmetic.** Floats in admission, or exp and log without directed enclosures.
