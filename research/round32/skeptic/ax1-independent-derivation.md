# AX1 independent derivation before producer comparison

**Standing.** I wrote this after the AX1 contract froze (`frozen_at` 2026-09-24T00:40:52Z, sha256 `bc834eec…da7d8d`). I had not opened, listed or read `research/round32/forward/ax1/` or `research/round32/reverse/ax1/`. I worked from the frozen contract, `selection-ax1.md`, the AV1, AV2, AW1 and AW2 gates, my own triage, loop-2, AV1 and AW1 notes, the modern `update-2.md` and `loop2-response.md`, the AM2, AL1 and AQ1 forward reports, AQ2 forward §3–5 (a declared shared premise) and I1 forward. Scratch work stayed in a private folder, and I read nothing from the shared scratchpad. I am a model-agent skeptic with correlated ancestry: the route-B mechanism and its constants (29|τ|, 102|τ|, 51|τ|/8, the 96/168 bounds) came from my own triage (c)4, so this note re-derives them and is not an independent discovery or human review. Exact values come from `ax1_check.py`, which runs 80 checks and implements 26 of the 28 contract controls as damaging mutations. Every decimal is a preview. Human project author: Hruday N M (BUNZEEY).

## 1. Dictionary and coefficient box
- **Dictionary (AL1).** α = g²/(2a), λ = 2/(g²a), λ/α = 4/g⁴; every face has ν = λ = ατ/24, so **τ = 24λ/α = 96/g⁴**, and |τ| = 10⁻⁸ gives **g⁴ = 9.6×10⁹** (g² ≈ 9.8×10⁴): strong bare coupling at fixed spacing. Label: *uniform Kogut–Susskind SU(2) at fixed spacing, g⁴ = 96/τ*, never weak coupling or continuum.
- **Box.** The selected triple is r = τ/24 per face; ends need |r| ≤ 1/2, the bridge |r| ≤ 1/8, i.e. |τ| ≤ 3; at the cap r = 1/(2.4×10⁹). **Normalized:** ν/δ = τ/3, so **every** face, omitted or selected, enters as −(τ/3)W_f (I1.5).
- **Negative τ** has no real-g preimage (96/g⁴ > 0): it is the mirrored coupling, unitarily equivalent to +|τ| through U_E in open boxes (§8).

## 2. Route-B groups, J′, supports, termination
**On-site operator.** h_b = 8Σ_{24 links}C_e is τ-independent with Haar vacuum Ω_b (constants). C_e ≥ (3/4)(1−P_e) and 1−⊗P_e ≤ Σ(1−P_e) give **h_b ≥ 6Q_b ≥ Q_b**; C_e is bi-invariant and Ω_b, W_f are gauge invariant, so AM2 §5 gauge invariance holds.

**Groups.** φ_b = −(τ/3)Σ W_f over the 21 omitted faces anchored at b (support b+S, retained iff b+S ⊂ Λ_N, ‖φ_b‖ = 7|τ|); ψ_b = −(τ/3)Σ W_f over the 3 selected xy faces (r ≤ 2, s = 0; by I1.4 all four tails lie in T_b, so support {b}; always retained; ‖ψ_b‖ ≤ |τ|).

**No double count.** A face has one base and orientation, hence one anchor π(p) and one role; the checker verifies selected ⇔ single-factor support, so faces are partitioned among groups (N = 3: 5565 retained faces, no repeats). Charging selected faces to stars too gives 8|τ| stars and J = 33|τ| (rejected).

**Per-site sum.** J′ = max_u Σ_{X∋u}‖V_X‖ = 4·7|τ| + |τ| = **29|τ|** (stars at u, u−e_x, u−e_y, u−e_z plus ψ_u); brute force on N = 1, 2, 3 never exceeds 29.

**Supports and termination.** Every group has |X| ≤ 4. AM2's majorant (HNM-AM2.5) uses only |X| ≤ p = 4: 2^{|X|} ≤ 16 output sets, |I_j| ≤ |M|+p and 1/|M| ≤ (p+1)/|I_l|. So L_k^num = 16·8^k(1+5k/4) is unchanged, and the nested commutator vanishes for k > 2|X|, so **termination at order 8** is unchanged.

## 3. Re-frozen contraction (R1)
- **Majorant.** e^{1/8} < 8/7 (order-12 Taylor sum plus geometric tail), so G(R) = 16e^{1/8}·74/64 < 148/7 and G′(R) = 308e^{1/8} < 352.
- **Contraction with J ≤ J_0′ = 29/10⁸:** J_0′G(R) < **1073/175000000** < 1/64 (1073·64 = 68672 < 1.75×10⁸) and 2J_0′G′(R) < **319/1562500** < 1.
- **Old constant fails:** J_0 = 7/25000000 = 28/10⁸ < J′ at the cap, so the frozen AM2 gate is out of hypothesis; R2 (|τ| ≤ 7/725000000) is a changed coupling. **Slack:** the self-map needs |τ| ≤ 7/274688 ≈ 2.55×10⁻⁵ (≈2548× the cap); Lipschitz (|τ| < 1/20416) is weaker.

**Consequence.** AM2 §3–6 applies verbatim with these constants: unique ground in every centered box and cutoff, full-space gap ≥ 1/2 normalized (**α/16** physical), cutoff removal. **Excited physical sector:** for any face f, (W_f − ⟨W_f⟩)Ω_H ≠ 0, since multiplication by a nonconstant real-analytic function is injective on L² (null level sets); no selected square is needed. **Route A** (strip reference, triple in the box, J = 28|τ| ≤ J_0) is the same operator up to a scalar and cross-checks the gap, but does not supply the Haar vector ψ = e^{−C}Ω_0, which needs R1.

## 4. Reset budget and the AQ1/AQ2 re-instantiation checklist

| AQ step | Status | Route-B constant |
|---|---|---|
| Reset on R (AQ2 §4) | new constant | ω(h_R) ≤ 2(7·7+2·1)\|τ\| = **102\|τ\|**. Labelled refinement: 100\|τ\|, because the two singles lie inside R with Haar mean 0 |
| ε_R | needs Haar gap six | h_R ≥ 6Q_R gives ε_R ≤ **17\|τ\|** and the square-root control 2√(17\|τ\|) ≤ 8.2463×10⁻⁴ ≤ 1/500. **Without gap six** it fails: 102/10⁸ > 10⁻⁶ |
| Wilson variance floor (AQ2 §5) | verbatim once the ≤ 1/500 bound holds | Tr(P_RW) = 0 and Tr(P_RW²) = 1/4 are immediate for the Haar product; floor 61999/250000 |
| Trace-norm compactness (AQ1.1–2) | verbatim argument, new constant | C_F ≤ 2(4·7+1)\|τ\|\|F\| = **58\|τ\|\|F\|** |
| Nachtergaele–Sims placement (AQ1.3) | new constant | F(r) = (1+r)⁻⁴, ‖F‖ ≤ 7 and C ≤ 224 are unchanged. The crude bound is ‖Φ‖_F ≤ 81J′ = **2349\|τ\|**. Per pair: two distinct sites lie in at most one star (the differences in S are distinct) and in no single group, so ‖Φ‖_F = max(29, 16·7, 81·7)\|τ\| = 567\|τ\|. AQ1's 2268\|τ\| is not a route-B bound by its own formula (81·28) |
| Stationarity, GNS, Stone, H ≥ 0 (AQ1 §4–5) | verbatim | none |
| Gauge averaging, physical gap α/16 (AQ2 §1–3) | verbatim, with the R1 full-Hilbert gap | none |
| AV1 cutoff-vector removal and AQ passage | verbatim, using the uniform gap 1/2 | none |

## 5. Itemized incidence on R = {0, e_z}
**All sizes.** A group meets R iff its anchor lies in R minus its offsets.
- **Stars:** R−S = {0, −e_x, −e_y, −e_z, e_z, e_z−e_x, e_z−e_y}. That is **7** anchors (0 arises twice). All are retained for N ≥ 2 (anchor e_z needs 2e_z ∈ Λ_N). At N = 1 only 4 are retained, with 55 faces meeting R.
- **Single groups:** the anchors are R itself, **2** groups.

**Per-face table.** The owner set of class k at anchor b is b+S_k. The checker exports every face, with its base, orientation, owners and meets-R flag.

| Group | Anchor | Faces | Owner set meets R | Owner set inside R | Classes meeting R |
|---|---|---:|---:|---:|---|
| star | 0 | 21 | 21 | 10 | all (every S_k ∋ 0) |
| star | e_z | 21 | 21 | 0 | all (e_z+S_k ∋ e_z) |
| star | −e_z | 21 | 16 | 0 | S_k ∋ e_z: xz 6+2, yz 4+4 |
| star | −e_x | 21 | 4 | 0 | S_k ∋ e_x: xy r=3 (1+1), xz r=3 (2) |
| star | −e_y | 21 | 8 | 0 | S_k ∋ e_y: xy s=1 (3+1), yz s=1 (4) |
| star | e_z−e_x | 21 | 4 | 0 | as −e_x |
| star | e_z−e_y | 21 | 8 | 0 | as −e_y |
| single | 0 | 3 | 3 | 3 | selected xy |
| single | e_z | 3 | 3 | 3 | selected xy |

**Totals.** B_N's groups hold 153 faces (7·21 + 2·3), norm 51|τ| normalized, so **‖B_N‖ ≤ 51|τ|/8** in G = H/α units and **k′ = 51|τ|/4**. Owner sets meeting R: 82 + 6 = 88; inside R 10 + 6 = 16; straddling 72 (selected faces never straddle). The **six selected faces** are exactly the two single groups; no face appears in two rows.

## 6. Uniform per-factor owner-set count
Among the 24 anchored classes, the number containing each offset of S is 0: 24, e_x: 4, e_y: 8, e_z: 16; for f anchored at b, u ∈ M(f) iff u−b ∈ S_k.
- **Per factor:** exact 24+4+8+16 = **52** = 49 omitted + 3 selected (singletons {u}); bound **96** = 4 anchors × 24, which also counts the 44 faces of those groups whose owner sets miss u.
- **For R:** exact 52+52−16 = **88** (the 16 faces containing both sites sit at anchor 0 with S_k ∋ e_z); bound **168** = 7 × 24.
- **Boundary:** in every Λ_N each site's counts are at most the bulk counts (brute force N = 1, 2, 3: maxima 52 and J′ = 29, never exceeded).
- **Owner sets through a site:** 16 (15 omitted plus {u}), multiplicities {1⁵, 2³, 3³, 4³, 10²}, Σ√n_I = 11+3√2+3√3+2√10 ≈ 26.763. So 96/168 are valid triangle bounds and 52/88 the exact counts.

## 7. State-lemma tiers D′_i and D′_ii (both signs)
**First order.** c′^(1)_I = H_I⁻¹P_IVΩ_0 = −(τ/72)Σ_{M(f)=I}W_fΩ_0; each W_fΩ_0 is an H_0 eigenvector at 24 = 8·4·(3/4) with norm 1/2, distinct faces orthogonal. New in route B: c′^(1)_{u} ≠ 0 (norm √3|τ|/144). ‖c′^(1)‖_a ≤ 52|τ|/144 (triangle); exact (11+3√2+3√3+2√10)|τ|/144. **Remainder:** t ≤ t_1 + J′(G(t)−16) ≤ t_1 + 352J′t (t ≤ R from tier (i), G convex), so **t ≤ t_1/(1−352J′)**, 352J′ = 319/3125000. **Split (AV1):** ε = 2t+t², D_fwd = 2ε(1+ε)/(1+ε²); purification 2ε/√(1+ε²) ∈ [2ε−ε³, 2ε].

| Tier | t at the cap | D′ (exact, `D_fwd`) | Preview | Against 4/10⁷ |
|---|---|---|---|---|
| (i) crude, t = J_0′·148/7 | 1073/175000000 | 23002790096235779074916932482/937890625141038667264537458466241 | 2.45261e-5 | fails by 61×, retained as limited |
| **(ii) exact, 52 faces** | 13/3599632512 | **2425369125199104794263242601250/167893028420061547330293754713793182097** | **1.444592e-8** | passes, margin 27.7 |
| (ii) bound, 96 faces (contract candidate) | 1/149984688 | 13495866406962926701045634/506043319649587578441076493302465 | 2.666939e-8 | passes, margin 15.0 |
| (ii) grouped √ (labelled, directed √) | exact in results | exact in results | 7.4350e-9 | passes |
| (ii) R-refined, 88 faces (labelled) | same t | exact in results | 1.2224e-8 | passes |

The same code reproduces AV1's admitted D_ii exactly from 49 faces and J = 28|τ|; tiers (i), (ii)-52 and (ii)-96 scale linearly (exact D(τ)/D(τ/100) ∈ [99, 101]); consequences |ω(W)| ≤ D′, |ω(W²)−1/4| ≤ D′/2, m² ≤ D′². **Ledger:** am2_remainder 352J′t; two_creation t² in ε (both factors are first order in route B, so the term is O(τ²)); straddling inside 2t; density inside D_fwd; onsite_cutoff_vector not additive (uniform gap moves the vector); arithmetic exact.

**AX2 feasibility.** The condition 2(D′+D′²) + 51|τ|/π ≤ 10⁻⁶ holds iff D′ ≲ 4.1883×10⁻⁷, bracketed by [41883, 41884]/10¹¹ with a directed π. The contract's "4.19×10⁻⁷" is itself infeasible. With D′_ii(52), the radius preview is 1.912×10⁻⁷, a margin of 5.23.

## 8. Transfer of the flip identity and parity to the uniform model
**(a) Every coefficient is tied to τ.** H_N(τ) = Σh_b + Σ_{b+S⊂Λ_N}φ_b(τ) + Σ_{b∈Λ_N}ψ_b(τ): every face term is −(τ/3)W_f and h_b is τ-independent. In AW1's notation this is H(τ, κ(τ)), κ(τ) = (τ/24)(1,1,1), up to the scalar E_strip.

**(b) Flip.** U_E = Π_{e∈E}Γ_e. E meets every plaquette in 1 or 3 links (per orientation one parallel pair splits, the other agrees; checker: 3000 faces on Λ_2, 1400 one-link and 1600 three-link, selected included; W meets E in 3). Γ_e commutes with every C_e and gauge action and fixes Ω_0, so U_EW_fU_E* = −W_f, U_Eh_bU_E* = h_b, U_EQ_nU_E* = Q_n (no Q_L → Q_L′ step, unlike AW1 at κ ≠ 0). **Hence U_E H_{N,n}(τ) U_E* = H_{N,n}(−τ)** in every open centered box and cutoff.

**(c) Antisymmetry.** R1 uniqueness gives ψ_{N,−τ} ∝ U_Eψ_{N,τ}: ω_{N,−τ}(W) = −ω_{N,τ}(W); ω_N(W²), C_N, c_N even; ρ_{N,R}(−τ) = U_{E∩R}ρ_{N,R}(τ)U_{E∩R}* with P_R fixed, so ‖ρ_R−P_R‖_1 is exactly even (the −τ bound is a theorem, not only a replay); AQ limits: S(−τ) = S(τ)∘α_E as whole sets. Fixture: an untied selected coefficient (−1/15 fixed) breaks the identity.

**(d) Parity.** ∂_τH|_0 = −(1/3)Σ_{all faces}W_f, and every AW1 ingredient is per plaquette: E[W²W_f] = 0 and E[WW_f] = δ_{fW}/4 for any plaquette (a link of f outside W carries a lone j = 1/2; f = W gives E[W³] = 0); P_24W_gWΩ_0 = 0 for g ≠ W (at most one shared link leaves ≥ 6 spin-½ links, energy ≥ 36); the invariant energy-24 multiplet now includes selected g, and its splitting needs three plaquettes covering every link evenly (6 shared links; three plaquettes share at most 3). Parity transfers verbatim with selected faces included.

**(e) First order.** ω(W)^(1) = −2Re⟨WΩ_0, c′^(1)⟩ = (τ/36)Σ_fE[WW_f] = **+τ/144**: W is the omitted xz face of class {0,e_z}, not among the xy selected faces, so only f = W contributes; ±1/14400000000 at the cap.

**(f) Quantifiers.** Verbatim: flip combinatorics, U_E properties, parity (finite boxes; C_N's τ² constant unbounded), +τ/144, whole-set AQ statement. Strengthened: antisymmetry without κ = 0. Needs route-B constants: K_2^+ (J′, t from 52 faces, 352J′, ε; its two-creation term is O(τ²) here, not O(τ⁴)). Not transferred: the AW2 enclosure and sign (claim exclusion).

## 9. Producer-error checklist
1. **Mixing routes A and B.** Examples: the strip reference, or AQ2's 98|τ|, with the Haar expansion; 102|τ| with the strip reference; e^{−3s}/4 claimed under route A, where both x links of W are strip links.
2. **Double-charging selected faces.** Examples: 24-face stars, J = 33|τ|; also leaving ψ_b out of J′, the reset or B_N.
3. **Keeping J_0 = 7/25000000**, or silently using the R2 cap.
4. **Asserting counts without the table.** Examples: 7/2/6/52/88 without the itemized table; calling 96 or 168 exact; reusing 49; counting only at 0 and e_z.
5. **Coupling wording.** "Weak coupling" or "continuum"; negative τ called a Kogut–Susskind coupling with real g.
6. **Citing AW1's flip or parity instead of proving the transfer.** AW1's antisymmetry needed κ = 0; here it needs κ tied to τ and h_b independent of τ.
7. **A selected-reference correlation or projection used with the Haar reference.**
8. **Tier mixing.** Examples: the exact c^(1) with the crude t; 352·28|τ| where 352·29|τ| is needed; unlabelled grouped or refined forms.
9. **Two-creation term.** Calling it O(τ⁴) (true only at the zero triple), or dropping it from ε.
10. **Stale AQ1 constants.** ‖Φ‖_F = 2268|τ| or C_F = 56|τ||F| cited as "unchanged".
11. **Reset without gap six.** Using 102|τ| in 2√ε ≤ 1/500 without the gap six fails.
12. **Threshold and target confusion.** Using 4.19×10⁻⁷ as the threshold, or reporting the D′ target as the admitted value.
13. **Sign cases.** Presenting −τ as an independent confirmation, or claiming pointwise AQ antisymmetry.
14. **Arithmetic.** Floats in an admission Boolean, float-log ratios, or a root-sum-square ε.
