# AW1 independent derivation before producer comparison

**Standing.** I wrote this after the AW1 contract froze (`frozen_at` 2026-09-23T22:59:30Z, sha256 `c24bf7eb…14ef`). I had not opened, listed or read `research/round32/forward/aw1/` or `research/round32/reverse/aw1/`. I worked from the frozen contract, `selection-aw1.md`, the AV1 and AV2 gates, my own triage, loop-2, loop-3, AV1 and AV2 notes, the modern loop-3 sign-off, AM2 forward, AT4 forward and I1 forward. I did not run the assistant scripts, so nothing here depends on them. I am a model-agent skeptic with correlated ancestry: same model family as the advisor, the lenses and the producers, and my triage seeded the parity and K_2 mechanism. This is not human peer review and not an independent discovery. Exact values come from `aw1_check.py` (79 checks, 31 controls). Every decimal here is a preview.

**Scratchpad disclosure.** For about ten minutes I left scratch copies of the K_2 and Haar arithmetic in the shared session scratchpad root. Another agent later overwrote one of them (`k2.py`). My copies now sit in a private subfolder. The producers should say whether they read scratchpad files.

Human project author: Hruday N M (BUNZEEY).

## 0. Notation
Each link space is L^2(SU(2)) = ⊕_j V_j⊗V_j^*, with C_e = j(j+1) on block j. G_0 = Σ C_e (alpha units; WΩ_0 at energy 3) and H_0 = 8G_0 (normalized; WΩ_0 at 24). By I1.5, V = -(τ/3)Σ_f W_f in δ units, that is V_G = -(τ/24)Σ_f W_f. The AM2 state is ψ = e^{-C}Ω_0 with c^(1) = L_0 = H_0^{-1}P_⊥VΩ_0 = -(τ/72)Σ_f W_fΩ_0 (the AV1 convention), so ψ = Ω_0 + (τ/72)Σ_f W_fΩ_0 + O(τ^2).

The Wilson face W is the omitted class (xz, r=0, s=0) anchored at factor 0. It is one of the 21 omitted faces at that anchor (the other 20 are separate), and one of the 10 faces whose owner set is exactly R = {0,e_z} (the other 9 are separate).

## 1. (a) The parity theorem
**Grading.** Put (Γ_eψ)(U) = ψ(…,-U_e,…). On block j of link e, Γ_e = (-1)^{2j}, because D^j(-1) = (-1)^{2j}. Its properties:
- Γ_e is diagonal in Peter–Weyl, so it commutes with every C_e', with H_0, with every onsite spectral projection, and with every endpoint gauge action (-1 is central).
- Γ_eΩ_0 = Ω_0.
- Γ_eW_fΓ_e = -W_f if e ∈ f, and +W_f otherwise.

For σ ∈ Z_2^{links}, the joint eigenspaces H_σ are invariant under H_0, and W_f maps H_σ to H_{σ+∂f}. Hence <Ω_0, XΩ_0> = 0 for any word X in the W's and functions of H_0 whose ∂-sum is nonzero, that is, whenever **some link carries an odd number of spin-1/2 factors**. In Peter–Weyl language, an odd power of spin 1/2 on a link contains only half-integer spins. H_0 evolution acts on each link diagonally in j, so it cannot change that content.

**Haar moments.** E[W^n] = 2^{-n}·mult(0 in (1/2)^{⊗n}), a Catalan number over 2^n. So E[W] = 0, E[W^2] = 1/4, E[W^3] = 0 and E[W^4] = 1/8 (then 5/64 and 7/128). The checker computes them two ways: from the character recursion χ_{1/2}χ_j = χ_{j-1/2}+χ_{j+1/2}, and by integrating the actual plaquette polynomials in U = [[a,-b̄],[b,ā]] with E|a|^{2p}|b|^{2r} = p!r!/(p+r+1)!. The two agree. Over all 82 omitted faces f meeting R, including f = W, the second route gives E[W W_f] = (1/4)δ_{fW}, E[W^2 W_f] = 0 and E[W_f] = 0.

**The first-order terms and their odd links.** Distinct plaquettes share at most one link. For f ≠ W, the odd links are the at least three links of f outside W, with multiplicity 1, plus the shared link if there is one, with multiplicity 3. For f = W, all four links of W have multiplicity 3 (this is E[W^3] = 0).

| Term | First-order expression (per unit τ) | Odd link |
|---|---|---|
| State, ω(W^2) | (1/36)Σ_f E[W_f W^2] | as above |
| State, C(s) | (1/36)e^{-3s}Σ_f E[W_f W^2] (W Ω_0 is G_0-eigen at 3) | as above |
| State, real time | (1/36)Σ_f Re<W_fΩ_0, W α^0_θ(W)Ω_0>, grade ∂f | as above |
| Duhamel, C(s) | +(s/24)e^{-3s}Σ_f E[W W_f W] | as above |
| Duhamel, real time | i∫_0^θ<Ω_0, W α^0_{θ'}([V_G, α^0_{θ-θ'}W])Ω_0>, grade ∂f | as above |
| Energy | E^(1) = -(1/24)Σ_f E[W_f] | all four links of f (multiplicity 1) |
| Mean square | m^2 = (τ/144)^2+…, second order (m itself is first order) | not applicable |

So in every box N ≥ 2 and every cutoff, ∂_τ C_N(s), ∂_τ ω_N(W^2) and ∂_τ ω_N(Wα_θW) all vanish at τ = 0. Their zeroth-order values are e^{-3s}/4, 1/4 and e^{3iθ}/4.

**The energy-3 multiplet.** Σ_e j_e(j_e+1) = 3 forces exactly four spin-1/2 links. Gauge invariance needs an even number of half-integer links at each vertex, so the four links form an even-degree 4-edge subgraph. Such a subgraph is a single 4-cycle (Z^3 has girth 4), that is, a plaquette, and the vertex singlet is unique there. So the invariant multiplet is span{W_gΩ_0}. The checker enumerates the 4-cycles of a 3×3×3 vertex cube and finds exactly its 36 plaquettes.

A splitting matrix element <W_gΩ_0, V W_hΩ_0> would need ∂f = ∂g+∂h. That set has size 0, 6 or 8, never 4, so the first-order splitting is zero. The checker also integrates the 984 elements <WΩ, W_f W_hΩ>: 183 directly and 801 by factorization.

The face f = W sends WΩ_0 to W^2Ω_0 = (1/4)Ω_0 + (1/4)χ_1(U_W)Ω_0. That is the identity component plus spin-1 content at energy 8; there is no energy-3 part.

Caution: on the *full*, non-invariant energy-24 eigenspace, PVP ≠ 0. The normalized element 1/8 between U1_00U2_00U5_00U6_00 and U3_00U4_00U5_00U6_00 is an example. Gauge invariance is essential.

**Scope.** The vanishing is a finite-volume Taylor statement. For ω(W^2), the split of §4 gives a volume-uniform bound (a labelled extra): |ω(W^2)-1/4| ≤ 1677.52 τ^2, using ||(W^2-1/4)Ω_R|| = 1/4 and ||W^2-1/4|| = 3/4. For C(s), no uniform O(τ^2) constant is proved here: the second-order Duhamel needs the second relative-unitary step, so the constant is **explicitly unbounded**.

**Named cross-check.** The link (0,z) is free, so U_W is Haar distributed and the single-loop moments equal the character moments (verified). This does not give the mixed moments E[W^2W_f].

## 2. (b) The flip lemma, with the skeptic's conditions
**Combinatorics.** In each orientation, one parallel pair of links differs in the parity that decides membership in E, so exactly one of the two is in E. The other pair shares its parity, so both are in E or neither is:
- xy: the x links differ in p_y, and the y links share p_z;
- yz: the y links differ in p_z, and the z links share p_x;
- xz: the z links differ in p_x, and the x links share p_y.

So |f∩E| ∈ {1,3}. The full enumeration (counts are 1-link/3-link) finds no even plaquette: the 8×3 parity cell 12/12; all 24 anchored classes on Λ_2 (3000 faces) 1400/1600; the 49 faces through a factor at both z-parities (coarse e_z moves fine z by one) 19/30 or 30/19; the 82 faces meeting R 41/41; the selected faces are odd as well.

Removing one link from E makes plaquettes even. Every periodic Z_2 coboundary meets every plaquette evenly, and E is none of the 256, so U_E is not a gauge transformation.

**Operator identity.** U_E = Π_{e∈E}Γ_e is unitary, self-inverse and diagonal in Peter–Weyl. So:
- it commutes with every C_e, with H_0, with every Q_n and every compression Q_nHQ_n, and with every endpoint gauge action;
- it fixes Ω_0, and P_R when κ = 0;
- U_EW_fU_E^* = -W_f for every plaquette (checked on the entry polynomials).

Hence **U_E H_{N,n}(τ,κ) U_E^* = H_{N,n}(-τ,-κ)**. The selected xy faces flip too. For κ ≠ 0, h_b(κ) → h_b(-κ): E_strip is even by unitary equivalence, and the reference Ω_b(κ) → Ω_b(-κ). Antisymmetry in τ therefore fails at κ ≠ 0:
- the coefficient map with κ = (1/5,-1/10,1/7) gives (-τ,-κ), not (-τ,κ);
- in a two-plaquette fixture, ω(W_sel) = κ/144 is unchanged by τ → -τ.

The identity needs open boxes. It fails for odd periodic sides and for frozen or gauge-fixed links.

**Finite ground states.** At κ = 0, AM2 gives a unique ground state at both signs, so U_Eψ_N(τ) ∝ ψ_N(-τ) and ω_{N,-τ} = ω_{N,τ}∘α_E. Hence ω_{N,-τ}(W) = -ω_{N,τ}(W); ω_N(W^2) and E_N are even; χ_{-τ} = -U_Eχ_τ makes C_N(s) even; and α_E intertwines the finite dynamics, so the real-time correlation is even too.

**AQ limits.** AQ1's diagonal subsequence depends on τ. If ω_{N_k,τ} → ω locally, then ω_{N_k,-τ} = ω_{N_k,τ}∘α_E → ω∘α_E, because α_E preserves each B(H_X). So **S(-τ) = S(τ)∘α_E as sets of subsequential limits**. Pointwise antisymmetry holds only for states taken along a common subsequence; AQ1's chosen -τ state need not be the image of its chosen +τ state. The limit of the dynamics is inherited from AQ1's local norm convergence.

**No O(τ^3) from oddness.** In finite volume, oddness kills the τ^2 Taylor coefficient of ω_N(W). It does not improve a uniform bound |r| ≤ K_2τ^2: r(τ) = Kτ|τ| is odd, and r/τ^2 = ±K. Any uniform third-order bound is a separate obligation, for example uniform complex-τ analyticity of the bilinear form. Nothing here assumes one. The K_2 value at -τ is a replay of the same |τ| formula, not evidence for the lemma.

## 3. (c) The first-order coefficient +τ/144 and its sign chain
The sign chain under I1.5:
1. I1: every omitted face enters as +ν(1-W_f), with ν = ατ/24.
2. I1.5: V = -(τ/3)ΣW_f in δ units.
3. c^(1) = H_0^{-1}P_⊥VΩ_0 = -(τ/72)ΣW_fΩ_0, since (τ/3)/24 = (τ/24)/3 = τ/72. The mixed-unit values τ/9 and τ/576 are rejected.
4. ψ = e^{-C}Ω_0 = Ω_0 - c^(1) + O(τ^2).
5. **ω(W) = -2Re<WΩ_0,c^(1)> + O(τ^2) = (τ/36)Σ_fE[W W_f] = (τ/36)E[W^2] = +τ/144.**
6. For τ > 0 the magnetic term favours W = +1, so the sign is right.

Only f = W contributes. The wrong-face control gives E[W W_f] = 0 for the other 81 faces meeting R, including the 9 others with owner set R. W is real, since tr U^{-1} = tr U, and invariant under a cyclic change of base point, so the coefficient does not depend on orientation.

The contract's literal formula "2<WΩ_0,c^(1)>" with the AV1-admitted c^(1) gives **-τ/144** (see the contract review, item 1).

Evaluations:
- At ±10^-8: ±1/14400000000.
- One-plaquette fixture (finite graph, labelled): <W> = τ/144 - 5τ^3/11943936 + O(τ^5), with E_1 = 0 and E_2 = -τ^2/6912.
- AV1 compatibility: D_ii/(τ/144) = 196.0.

## 4. (d) K_2, itemized and uniform in volume
**Exact identity.** From ψ = ψ_out+δ, ψ_out = Ω_R⊗φ_out and ξ̃ = (1⊗<φ_out|)δ/||φ_out||^2, with E[W] = 0:

  ω(W) = [2Re<WΩ_R,ξ̃> + <δ,Wδ>/||φ_out||^2]/(1+e^2).

Write ξ̃ = -c_R - Σ_{I⊋R}ξ̃_I - (terms touching one site of R) + Σ_{pairs}ξ̃_{IJ}. WΩ_R is excited at e_z through the link (e_z,x), and ||WΩ_R|| = 1/2. So every one-site term is exactly orthogonal to WΩ_R. That covers c_{0}⊗Ω, Ω⊗c_{e_z} and 66 of the 72 straddling faces. The 6 faces with owner sets {0,e_x,e_z} and {0,e_y,e_z} strictly contain R.

**Outside-excitation lemma.** Split φ_out at a single site y. Then ||Q_yφ_out|| ≤ (Σ_{J∋y}||c_J||)||φ_out|| ≤ t||φ_out||. For I⊋R this gives ||ξ̃_I|| ≤ ||c_I||·t.

**Result.** r = ω(W) - τ/144 obeys

  |r| ≤ 1·(am2 + straddling + two_creation) + density + normalization,

with every t equal to the tier's anchored-norm bound. The leading factor 1 is the multiplier 2·||WΩ_R||.

| Term (the tier names t) | Form | Exact tier, t = T = (49|τ|/144)/(1-352J) | Crude tier, t = J_0G(R) = 592|τ| |
|---|---|---|---|
| am2_remainder | ||(c-c^(1))_R|| ≤ J(G(t)-16) ≤ 352Jt, J = 28|τ| | 3354.108 τ^2 | 5,834,752 τ^2 |
| two_creation | all disjoint pairs I∋0, J∋e_z: ≤ t^2 (refined (352Jt)^2+t^3, since c^(1)_{0} = 0) | 0.1158 τ^2 | 350,464 τ^2 |
| straddling | I⊋R paired with an outside excitation: ≤ t·t (refined t(6|τ|/144+352Jt)) | 0.1158 τ^2 | 350,464 τ^2 |
| density | |<δ,Wδ>|/||φ_out||^2 ≤ ε^2, ε = 2t+t^2 | 0.4632 τ^2 | 1,401,864.3 τ^2 |
| normalization_order | (|τ|/144)e^2/(1+e^2): **third order** | 3.2e-11 at the cap | 9.7e-5 at the cap |
| overlap_multiplier | 2·||WΩ_R|| = 1 (×4 only as a labelled conservative choice) | 1 | 1 |
| arithmetic | not applicable: exact rationals throughout | 0 | 0 |

**K_2^+ at the exact tier** is 3354.803229461691 (≤ 3354803229461691/10^12). **K_2^+ at the crude tier** is 7937544.299097154189 (≤ 7937544299097154189/10^12). The exact rationals are in `results.json`.

Every quadratic term scales by a ratio in [9900, 10100] when τ → τ/100. Each τ^2 coefficient increases with |τ|, so the cap values bound every |τ| ≤ 10^-8. Every term uses only the anchored norm (a maximum over sites, with boundary counts at most the bulk counts) and the two-site R. So the bound is uniform in N and in the cutoff. It passes to the untruncated ground vector (AV1 §7) and to every AQ1 subsequential limit.

**Labelled variants (not the headline).** The 288t/(1-8t) remainder with the enumerated straddling and ε_82 gives 2744.61. The grouped √-anchored norm gives 1713.60 (352 form) or 1402.07 (288 form). The conservative ×4 multiplier gives 13417.82, and the 84-face bound with ×4 gives 23003.68.

My loop-2 range at the exact tier, 1.4e3–5.8e3, contains the headline. My loop-3 figure, 1.1–1.9e4 with margins 36–63, was the conservative ×4 reading, and this computation supersedes it.

## 5. (e) The AW2 decade-grid rule
K_2^+·10^-8 = 3.3548e-5, which is at most 1/288 ≈ 3.472e-3. So **τ_AW2 = 10^-8**, the cap and the largest grid element. The **margin at the cap** is 1/(144K_2^+·10^-8) = **207.00005**; the directed lower bound is 41400010489/200000000.

The outcome is robust: every exact-tier K_2^+ ≤ 10^8/288 ≈ 347,222 gives 10^-8, including the ×4 and 84×4 variants (margins 51.8 and 30.2).

At the crude tier the margin at the cap is 0.0875, so it fails and is retained as limited. The rule applied to that tier would give 10^-10. That is a comparison only: the frozen rule names the exact tier. AW1 admits no enclosure; the sign stays with AW2.

## 6. (f) Likely producer errors (review checklist)
1. **Tier mixing.** Examples: the exact T in the remainder combined with a crude ε, or the crude t labelled exact. Also: a K_2 whose terms carry different tier labels, or a grouped or 288 form presented without a label.
2. **Missing the two-creation (pair) term**, in ξ or in ε. It is also wrong to claim it vanishes without c^(1)_{0} = c^(1)_{e_z} = 0 and a remainder bound.
3. **Excluding f = W from the omitted set**, which gives coefficient 0 and makes "parity kills everything" look true. Also wrong: merging W with the 20 other anchored faces, or with the 9 other faces of R (10/144 or 21/144).
4. **Claiming O(τ^3), or an "effective K_2", from oddness.** Also wrong: dropping d or T_strad because their τ^2 Taylor coefficients vanish, without paying them as absolute bounds.
5. **Wrong sign.** Using 2<WΩ_0,c^(1)> with AM2's c^(1) gives -τ/144. Other ways to go wrong: mixed units (τ/9, τ/576), or signs that are never evaluated (sign-blind |τ| code).
6. **Double-counting the overlap.** Examples: a factor 4 from "2Re × 2 sites" without the label "conservative", c_R counted at both anchors, or the 66 one-site straddling faces charged to the overlap. Harmless but unlabelled: the 16 faces containing R double-counted in ε.
7. **Using the -τ replay as evidence for the flip lemma**, or the AV2 interval as evidence for the parity theorem.
8. **Declaring zero first-order splitting on the full energy-24 eigenspace** instead of the gauge-invariant multiplet. Omitting the f = W case (E[W^3] = 0) or the energy term.
9. **An unconditional flip statement:** H(τ) → H(-τ) without κ, for periodic or gauge-fixed boxes, with the compressions Q_nHQ_n omitted, or pointwise AQ antisymmetry for independently chosen states.
10. **Counting at sites 0 and e_z only, or hard-coding 49/82/72**; presenting 84 as exact. A flip enumeration at only one z-parity, or on a sample.
11. **Treating the normalization term as second order**, or normalizing by 1+O(τ^2) with the outside creations left in the numerator.
12. **Stating C(s) = e^{-3s}/4+O(τ^2) as a uniform AQ theorem**, or relabelling the static mean as a dynamical or mass-gap effect.
13. **Arithmetic slips:** floats in an admission Boolean, a root-sum-square combination of the terms, or a τ_AW2 chosen off the grid or from the crude tier.
