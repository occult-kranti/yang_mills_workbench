# Hruday boundary comparison of the Heisenberg dynamics of the named constructions on compact windows — BA2 reverse (inner-F2 Duhamel and own-family limits)

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted reverse production: the derivations, `check.py` and this report were written by Claude (an AI model) as the BA2 reverse producer, under reverse premise isolation (`reverse_premise_isolation: true`). This is correlated model-agent work, not human review and not formal verification. HNM labels are project aliases; the contribution alias is **HNM-BA2-R** (reverse inner-F2 Duhamel comparison, own-family Cauchy limits and F2 limit dynamics).

I read the frozen contract snapshot `inputs/research/round33/contracts/ba2.json` first (sha256 `275ba3b002529b7295d0f8b91dc1cc7a96451e3c7f936ee698a932fdca54fcff`, verified by `check.py` before any evaluation), then `inputs/AGENTS.md`, `inputs/research/round33/advisor/selection-ba2.md`, the committed Nachtergaele–Sims excerpt and the premises. I did not open, list or read anything under `research/round33/forward/`, `research/round33/skeptic/`, `research/round33/experts/`, `research/round33/reverse/ba1/`, or any advisor file other than the snapshots in `inputs/`. Section 12 gives reading depths, the non-scientific style files and the scratch folder.

**Attribution.** The Lieb–Robinson bound (Theorem 3.1) and the limit dynamics (Theorem 4.1) are Nachtergaele–Sims, arXiv:1410.8174v1, quoted verbatim from the committed excerpt. The Duhamel (cocycle) identity for a bounded perturbation of a self-adjoint generator is standard. The compactness/stationarity/GNS/Fourier strategy rerun in O6 is AQ1 §§4–5, which credits Gauvin arXiv:2503.15539v3 Supplement A.10. The families, the face dictionary and the owner-set constant come from I1, AQ1 and AY1. Scientific priority is unverified.

## Verdict (reverse half)

Model (contract `model`, `parameters`, `preregistration`): the zero-selected patterned family `AQ_patterned_zero_selected` (SU(2) in Kogut–Susskind form on Z³ at fixed spacing, coarse 24-link factors, selected triple exactly (0,0,0), 21 omitted faces per anchor entering as `-(tau/3)W_f` in normalized units `delta=alpha/8`), both signs of `|tau|<=10^-8` evaluated at the cap `tau=±1/100000000`; the two named construction families **F1** (AQ1 centered whole-star boxes) and **F2** (I1 section 6 all-contained-face boxes with padding) on the same `Lambda_N=[-N,N]^3`, `N>=2`; observables `A in B(H_R)`, `||A||<=1`, on the cover `R={0,e_z}` (48 links, 36 endpoints); the common clock `theta=alpha t/hbar` with window `|theta|<=8`, i.e. `U=Theta/8=1` in the normalized time `u=theta/8`; the AQ1 decay function `F(r)=(1+r)^-4` on the coarse l1 metric (tier `polynomial_lieb_robinson`).

1. **Item 1 (§1).** Theorem 3.1 (51)–(52) and Theorem 4.1 (77), with (40), (41), (44)–(47), (48)–(50), are quoted verbatim. The unbounded Casimirs `h_b` sit in the `H_x` slot of (44) and enter no constant; Theorem 3.1 handles them through its interaction picture (54), (57). `||F||<=7`, `C<=224` are re-derived; the whole-star interaction `Phi` has `||Phi||_F<=81J=2268|tau|` and the owner-set interaction `Phi'` has `||Phi'||_F<=81·49|tau|/3=1323|tau|`, both re-derived; F1 on `Lambda_N` is the native restriction of `Phi` and F2 on `Lambda_N` without padding is the native restriction of `Phi'`.
2. **Item 2 (§2).** `H^{F2,pad}_N - H^{F1}_N` = the **28N(5N+1)** extra faces + the padding on-site terms. The padding **factors out exactly** (`T^{F2,pad}_theta(A(x)1)=T^{(2),N}_theta(A)(x)1`), so the Duhamel source is the bounded sum over the extra faces alone, each charged once. Every extra face has at most 3 owners, all on the outer layer, at coarse l1 distance at least `N` from `0` and at least `N-1` from `e_z` (both attained). Enumerated on `Lambda_2` (616) and `Lambda_3` (1344), counts checked to `N=6`, all-size anchor decomposition `140N^2+28N`.
3. **Item 3 (§3), inner F2 with `Phi'`:** `||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| <= b(N)||A|| = K_cmp (5N+1) N^-3 ||A||` for `|theta|<=8`, `N>=2`, both signs, with `K_cmp = 148176 tau^2 U^2 E_up(592704|tau|U) = 452554889222515527/30481402343750000000000000000` (preview `1.48469182657e-11`), meeting the frozen `6x10^-11` with margin `4.0412`. It is quadratic in `tau`; the first order vanishes because the zero-coupling dynamics keeps `A` in `B(H_R)` and no extra face meets `R`.
4. **Item 4 (§4), each family against its own Nachtergaele–Sims limit:** F1 (inner F1, `Phi`, 2268|tau|): `sup_{M>N} ||T^{F1,M}_theta(A)-T^{F1,N}_theta(A)|| <= c1/(N-1)`, `c1 = 12128856933354903/118967041015625000000000000` (preview `1.01951404605e-10`, margin `2.4521`); F2 (inner F2, `Phi'`, 1323|tau|, face by face): `c2 = 1055961408185869563/30481402343750000000000000000` (preview `3.46428092867e-11`, margin `7.2165`); both against `2.5x10^-10/(N-1)`, at the honest O(1/N) rate of the polynomial F. Both families converge as whole sequences in norm on the window; the F2 limit equals the AQ1 limit `T_theta` (identified through `b(N)->0` on every local observable); AQ1 §§4–5 (stationarity under `T_theta`, strong GNS continuity, nonnegative generator, gauge restriction) are rerun for every F2 subsequential limit state with F2's own subsequences.
5. **Item 5 (§5).** Algebraic Heisenberg dynamics of the named constructions on a compact window; not equality of GNS dynamics or of correlation functions of different states (that needs a common state, BB2). Template quoted once; gate fields exported.
6. **Item 6 (§6).** Scaling `tau->tau/100`: comparison about `10019.588`, `c1` about `10033.615`, `c2` about `10019.588`, all inside `[9500,10500]`, the comparison also inside `[9900,10100]`. Five exact trap fixtures. All 35 contract controls are damaging mutations (149 mutations, every one rejected for its stated reason).

**Proposed reverse verdict: `accepted_within_scope`**, sub-label `dynamics_on_compact_windows` (reverse half only; the contract's acceptance needs both routes and the skeptical review).

## 0. Model, families, clock and notation

**Families** (contract `parameters.boundary_source`; I1 §6; AQ1 §1; AY1 reverse §1.1). With `h_b>=0` the normalized on-site operator (here `8 sum_{e in b} C_e`, unbounded, self-adjoint, compact resolvent), `phi_b=-(tau/3) sum_{f in O_b} W_f` the whole-star group (`||phi_b||<=7|tau|`) and `M_f` the owner set of face `f` (I1.4):

- F1: `H^{F1}_N = sum_{b in Lambda_N} h_b + sum_{b+S inside Lambda_N} phi_b`, `S={0,e_x,e_y,e_z}`.
- F2: `H^{(2)}_N = sum_{b in Lambda_N} h_b + sum_{f: M_f inside Lambda_N} v_f`, `v_f=-(tau/3)W_f`; padded: `H^{F2,pad}_N = H^{(2)}_N (x) 1 + 1 (x) sum_{x in B_+ minus Lambda_N} h_x` on `H_{B_+}`, `B_+=Lambda_N+S`.

**Interactions** (Nachtergaele–Sims (44)). Whole-star `Phi(b+S)=phi_b`; owner-set `Phi'(M) = -(tau/3) sum_{f: M_f=M} W_f`. Both are bounded and self-adjoint (`W_f=(1/2)Tr U_f` is a real multiplication operator, `|W_f|<=1`). Then `H^{F1}_N = sum_{x in Lambda_N} h_x + sum_{X inside Lambda_N} Phi(X)` and `H^{(2)}_N = sum_{x in Lambda_N} h_x + sum_{M inside Lambda_N} Phi'(M)` are exactly the native restrictions; `check.py` verifies both identities face by face on `Lambda_2`, `Lambda_3`. The padded operator is not a native restriction of `Phi'` on `B_+`; it is reduced to `H^{(2)}_N` by the exact factorization of §2.1.

**Clock.** The physical evolution is `T^{F,N}_theta(A) = e^{itK_N/hbar} A e^{-itK_N/hbar}` with `K_N = delta(Hhat_N - E_N)`, `delta=alpha/8`; hence `T^{F,N}_theta = tau^{F,N}_u`, the Nachtergaele–Sims dynamics (46) of the normalized operator at `u=delta t/hbar=theta/8`; ground scalars cancel in the conjugation. `|theta|<=8` is `|u|<=1`, so `U=Theta/8=1`. The normalized `u` is used only internally with this conversion.

**Notation.** `J=28|tau|` (whole-star per-site sum, four incident stars, incoming anchors included); `J'=49|tau|/3` (owner-set per-site sum, 49 faces through a site); `C<=224`, `||F||<=7`; `E(y)=2(e^y-1-y)/y^2` and its rational upper bound `E_up(y)=1+y/3+y^2/(12(1-y/5))`; `A in B(H_R)`, `||A||<=1`. Uniformity is always **in N at fixed spacing**, never in the lattice spacing.

## 1. Item 1 — the Lieb–Robinson inequality, verbatim, and the placement of the on-site terms

### 1.1 Verbatim quotation (committed excerpt `research/round33/sources/nachtergaele-sims-1410.8174v1.md`, Part A; PDF sha256 `501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba`)

Setting and definitions:

> Setting (Section 3). Γ is a countable set with a metric d. If Γ is infinite, F : [0, ∞) → (0, ∞) is non-increasing and
>
> To each x ∈ Γ a separable complex Hilbert space H_x is associated; for finite Λ ⊂ Γ, H_Λ = ⊗_{x∈Λ} H_x and A_Λ = B(H_Λ). For each x there is a self-adjoint operator H_x with dense domain D_x ⊂ H_x; the bounded interaction Φ maps finite X ⊂ Γ to Φ(X)* = Φ(X) ∈ A_X, and
>
> (44) H_Λ = Σ_{x∈Λ} H_x + Σ_{X⊂Λ} Φ(X),
>
> essentially self-adjoint on the dense domain (45) D_Λ = span{⊗_{x∈Λ} ψ_x | ψ_x ∈ D_x}; (46) τ_t^Λ(A) = e^{itH_Λ} A e^{−itH_Λ} for A ∈ A_Λ.
>
> (40) ‖F‖ = sup_{x∈Γ} Σ_{y∈Γ} F(d(x, y)) < ∞ (uniform integrability);
>
> (41) C = sup_{x,y∈Γ} Σ_{z∈Γ} F(d(x, z)) F(d(z, y)) / F(d(x, y)) < ∞ (convolution condition).
>
> (48) ‖Φ‖ = sup_{x,y∈Γ} (1/F(d(x, y))) Σ_{X⊂Γ: x,y∈X} ‖Φ(X)‖ < ∞ defines the space B_F(Γ).
>
> (49) S_Λ(X) = {Z ⊂ Λ : Z ∩ X ≠ ∅ and Z ∩ (Λ \ X) ≠ ∅}, the surface of X in Λ, and S(X) = S_Γ(X).
>
> (50) ∂_Φ X = {x ∈ X : ∃Z ∈ S(X) with x ∈ Z and Φ(Z) ≠ 0}, the Φ-boundary of X.

Equation (47), present only in Part B (verbatim machine text):

```text
(47)                    U ψ = −iHΛ UtΛ ψ = −iUtΛ HΛ ψ for all ψ ∈ DΛ .
```

Theorem 3.1:

> **Theorem 3.1.** Let Γ and F be as indicated above. Fix a collection of local Hamiltonians {H_x}_{x∈Γ} and an interaction Φ ∈ B_F(Γ). Let X, Y ⊂ Γ be finite disjoint sets. For any finite Λ ⊂ Γ with X ∪ Y ⊂ Λ and any A ∈ A_X and B ∈ A_Y, the bound
>
> (51) ‖[τ_t^Λ(A), B]‖ ≤ (2‖A‖‖B‖ / C) (e^{2‖Φ‖C|t|} − 1) D(X, Y)
>
> holds for all t ∈ ℝ, where the quantity D(X, Y) is given by
>
> (52) D(X, Y) = min{ Σ_{x∈X} Σ_{y∈∂_Φ Y} F(d(x, y)), Σ_{x∈∂_Φ X} Σ_{y∈Y} F(d(x, y)) }.
>
> The proof (steps 1–4) uses an interaction-picture dynamics (57) generated from H_0 = Σ_{x∈Λ} H_x + Σ_{Z⊂X} Φ(Z) (54), which is how the unbounded on-site terms are handled.

Theorem 4.1 (statement; the excerpt's parenthetical section title is not reproduced here):

> Let Γ and F be as described in Section 3. Fix a collection of on-site Hamiltonians {H_x}_{x∈Γ} and an interaction Φ ∈ B_F(Γ). For each t ∈ ℝ and A ∈ A_Γ^loc, the norm limit
>
> (77) τ_t(A) = lim_{Λ→Γ} τ_t^Λ(A)
>
> exists and the convergence is uniform for t in compact sets. The limit may be taken along any increasing sequence of finite sets Λ which tend to Γ, and the result is independent of the particular sequence. This limiting dynamics τ_t(·) can be uniquely extended to a one-parameter group of *-automorphisms on A_Γ.
>
> In its proof: (78) U_Λ(t, s) = e^{itH_Λ^loc} e^{−i(t−s)H_Λ} e^{−isH_Λ^loc}, with (79) H_Λ^loc = Σ_{x∈Λ} H_x.

The last line of the Theorem 3.1 block is the excerpt's own note on the proof (the committed transcription), not the paper's wording; everything else is the paper's statement. The AQ1 report is the placement record for the model; the quotations above are the source, and `check.py` requires each passage verbatim in this report (`item1_ns_quotation_verbatim`).

### 1.2 The named decay function, `||F||` and `C`

`Gamma = Z^3` (coarse factor sites) with the l1 metric `d`; `F(r)=(1+r)^-4`, positive and non-increasing. Shells: the number of points at l1 distance `r>=1` is `4r^2+2` (enumerated for `r<=30`; derivation: `4r` points with `c=0` plus `sum_{k=1}^{r-1} 2·4(r-k)+2` with `c≠0`).

- (40): `||F|| = 1+sum_{r>=1}(4r^2+2)(1+r)^-4 <= 1+6 sum_{k>=2}k^-2 <= 7`, using `4r^2+2<=6(r+1)^2`; the checker also encloses the partial sum to `r=40` plus the tail `6/41` below 7.
- (41): for any `z`, either `d(x,z)>=d(x,y)/2` or `d(z,y)>=d(x,y)/2`; on the first half `F(d(x,z))<=F(d/2)<=16F(d)` (since `(1+d)/(1+d/2)<=2`), so that half contributes at most `16||F||`, and likewise the other: `C<=32||F||<=224`. Finite-window partial sums (previews only) lie between 1.03 and 4.22.

### 1.3 Placement of the unbounded on-site terms

The site Hilbert spaces `H_b = L^2(SU(2)^24)` are separable; `H_x := h_x` is self-adjoint on a dense domain with compact resolvent (I1 §2; AQ1 §2). It sits in the on-site slot of (44) and never in `Phi` or `Phi'`. Theorem 3.1 then gives (51) with only the bounded interaction norm `||Phi||` of (48) and the convolution constant `C` of (41); the unbounded `h_x` are handled inside its proof by the interaction picture (54), (57) and enter no constant. Placing a cutoff on-site ladder `h_L=diag(0,...,L)` inside the interaction as a one-site term would give `||Phi||_F>=L/F(0)=L`, so the velocity `2||Phi||C` would grow without bound with the cutoff (fixture §6.2); that placement is rejected. In the Duhamel identity of §3.1 only a bounded operator is subtracted between the two generators, so no unbounded term is ever differentiated or charged. Norm continuity in `theta` on all of `B(H_R)` is not claimed (the l²(ℕ) shift witness of AQ1 §6 is reproduced exactly: `||U(pi/n)AU(pi/n)^*-A||=2`).

### 1.4 The two interaction norms, re-derived

- **Whole stars `Phi`.** Every star `b+S` has l1 diameter 2; every site lies in exactly four stars (anchors `u-S`, incoming included), so `J=sup_u sum_{X∋u}||Phi(X)||<=4·7|tau|=28|tau|`. Only pairs with `d(x,y)<=2` share a star and `F(d)>=F(2)=1/81`, hence `||Phi||_F <= 81J = 2268|tau|`.
- **Owner sets `Phi'` (F2 on `Lambda_N`).** The I1 table gives 14 two-site and 7 three-site omitted classes; every owner set has l1 diameter at most 2. By translation covariance a site lies in 49 omitted faces grouped in 15 owner sets, so `J'=sup_u sum_{M∋u}||Phi'(M)|| <= 49|tau|/3` and `||Phi'||_F <= 81·49|tau|/3 = 1323|tau|`. The enumerated maximum on `Lambda_2`, `Lambda_3` is exactly 49 faces through a bulk site; the F2 padding sites carry no face.
- Pins from the table: 49 faces per factor, 15 owner sets, 82 faces meeting `R` (16 contain both sites), 10 with owner set exactly `R` — derived from the parsed I1 table, itself re-derived from `pi` and the link tails.
- Labelled remark (not used anywhere): the exact (48)-norms by pair enumeration are `108|tau|` for `Phi'` and `567|tau|` for `Phi` (maxima at pairs at distance 2 lying in one owner set or one star). Every constant below uses the contract constants `1323|tau|` and `2268|tau|`.

### 1.5 Substituting upper bounds

`(2/C)(e^{2nC|t|}-1) = 4n|t|·phi(2nC|t|)` with `phi(y)=(e^y-1)/y` increasing, `n=||Phi||_F`. So the right side of (51) is increasing in `C` and in `n`, and the theorem's actual `C` and `||Phi'||` may be replaced by `224` and `1323|tau|` (or `2268|tau|` for F1).

## 2. Item 2 — the F2-minus-F1 boundary source on `Lambda_N`

### 2.1 The padding factors out exactly

`B_+ minus Lambda_N` consists of `3(2N+1)^2` sites (75 at `N=2`, 147 at `N=3`; `|B_+|=200`, `490`, enumerated), carrying only `P_N = sum_{x in B_+ minus Lambda_N} h_x` on the tensor factor `H_pad`. For a tensor sum of self-adjoint operators on separate factors, `e^{iu(H(x)1+1(x)P)} = e^{iuH}(x)e^{iuP}`. Hence, for `A in B(H_R)` inside `B(H_{Lambda_N})`,

`T^{F2,pad}_theta(A(x)1) = e^{iuH^(2)_N} A e^{-iuH^(2)_N} (x) e^{iuP}e^{-iuP} = T^{(2),N}_theta(A)(x)1`.

The padding terms commute with `H^(2)_N`, with every face and with `B(H_R)`. The comparison is therefore between `T^{(2),N}` and `T^{F1,N}` on `H_{Lambda_N}`, whose generators differ by the bounded `V_N := H^{(2)}_N - H^{F1}_N = sum_{f in E_N} v_f`. The padding terms are never charged as boundary terms: charging them makes the source norm at least the cutoff `L`, while their exact contribution is zero. Exact fixture (sites `a` in `R`, `b`, and a padding qutrit `p` with `h_p=diag(0,1,2)`, `H=X_aX_b`; `e^{i(pi/2)H}` and `e^{i(pi/2)Hpad}` computed from Lagrange spectral projectors as Gaussian-rational matrices): `e^{iuHpad}(A(x)1)e^{-iuHpad} = (e^{iuH}Ae^{-iuH})(x)1`, `e^{iuHpad}=e^{iuH}(x)e^{iuh_p}`, `[H(x)1,1(x)h_p]=0`, with a nontrivial evolution `A=Z_a -> -Z_a`.

### 2.2 The extra faces and their count 28N(5N+1)

`E_N` = faces in F2 not in F1 = faces with `M_f` inside `Lambda_N` whose anchor `b` has `b+S` not inside `Lambda_N`. Since `b in M_f` lies in `Lambda_N`, "`b+S` not inside `Lambda_N`" means `b_i=N` for some `i`; since `M_f=b+K_f` lies in `Lambda_N`, the support `K_f` avoids `e_i` for every such `i`.

All-size count. The classes whose support avoids `e_x`, `e_y`, `e_z` number `17`, `13`, `5` (enumerated from the table). Anchors with exactly one coordinate equal to `N`: three planes with `(2N)^2` anchors each, giving `4N^2(17+13+5)=140N^2` faces. Anchors with exactly two: three edges with `2N` anchors each; the support must lie in `{0,e_k}`: 10 classes (`k=z`), 3 (`k=y`), 1 (`k=x`), giving `2N·14=28N`. The corner `(N,N,N)` admits no omitted face (every class has a nonzero offset). Total `140N^2+28N = 28N(5N+1)`. Equivalently `|F2| = 28N(2N+1)(3N+1)` and `|F1| = 21(2N)^3 = 168N^3` (verified for `N=2,...,6`).

Enumeration (`check.py`, from the parsed I1 table):

| `N` | F1 faces | F2 faces | extra `28N(5N+1)` | one-plane / two-plane | partial groups | padding sites |
|---|---:|---:|---:|---|---:|---:|
| 2 | 1344 | 1960 | 616 | 560 / 56 | 60 | 75 |
| 3 | 4536 | 5880 | 1344 | 1260 / 84 | 126 | 147 |

Both families retain the same 82 faces meeting `R` (for `N=2,3` and, by the geometry, every `N>=2`); `E_N` never meets `R`.

### 2.3 Owners, outer layer and distance

If `b_i=N`, every owner `o=b+k` (`k in K_f`, with no `e_i` component) has `o_i=N`: every owner lies on the plane `{y_i=N}` of the outer layer `max_i|y_i|=N`. Hence `|o|_1 >= |o_i| = N` and `|o-e_z|_1 >= |o_i-(e_z)_i|`, which is at least `N-1` (for `i=z`) and at least `N` otherwise. Both minima are attained (owners at `(0,0,N)`): enumerated minima `2, 1` at `N=2` and `3, 2` at `N=3`. Fine units (informational only; no constant uses them): a coarse step is `(4a,2a,a)`; the fine tail blocks of an owner on the `z`-plane are `N-1` fine lattice steps from those of `e_z` along `z` (`4N-3` for the `x`-plane, `2N-1` for the `y`-plane). No physical length is read from these numbers.

### 2.4 Each face charged once

A face is one pair (anchor, class); it is charged exactly once, as `v_f=-(tau/3)W_f` with `||v_f||<=|tau|/3`, never per owner, per anchor group or together with an F1 (old) term. The source is exactly `E_N` (`check.py` rejects a source with one F1 face added or one extra face missing).

## 3. Item 3 — the Duhamel comparison with the inner F2 evolution

### 3.1 The Duhamel identity for unbounded generators with a bounded difference

Let `H_1=H^{F1}_N`, `H_2=H^{(2)}_N=H_1+V_N` on `H_{Lambda_N}`; both are self-adjoint with `D(H_1)=D(H_2)` (`V_N` bounded). Write `tau^j_u(A)=e^{iuH_j}Ae^{-iuH_j}`. The cocycle `W(s)=e^{isH_1}e^{-isH_2}` satisfies, for `psi in D(H_1)`, `d/ds W(s)psi = -i e^{isH_1}V_N e^{-isH_2}psi`; hence `W(s)=1-i int_0^s e^{irH_1}V_N e^{-irH_2}dr` strongly (first on `D(H_1)`, then on every vector by boundedness), so `s -> W(s)psi` and `s -> W(s)^*psi` are C¹ for every `psi`. With `g(s)=tau^1_s(tau^2_{u-s}(A)) = W(s) tau^2_u(A) W(s)^*`, the product rule on vectors gives `d/ds <phi,g(s)psi> = -i<phi, tau^1_s([V_N, tau^2_{u-s}(A)])psi>`. Therefore

`tau^1_u(A) - tau^2_u(A) = -i int_0^u tau^1_s([V_N, tau^2_{u-s}(A)]) ds` (weakly), and `||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| <= sum_{f in E_N} int_0^{|u|} ||[v_f, tau^2_r(A)]|| dr`.

The outer evolution `tau^1` is isometric and drops out; **the evolution inside the commutator is F2's** (reverse route). No norm derivative of `tau(A)` in time is used, only vector derivatives of bounded C¹ families, consistent with the AQ1 distinction between norm volume convergence and norm time continuity.

### 3.2 The Lieb–Robinson bound per extra face, with F2's own constants

`tau^2_r` is the Nachtergaele–Sims dynamics (46) of the native restriction of `Phi'` to `Lambda=Lambda_N` with `H_x=h_x`. Take `X=R`, `Y=M_f` (both inside `Lambda_N`, disjoint since `d(R,M_f)>=N-1>=1`), `A in A_R`, `B=v_f in A_{M_f}`. (51)–(52) and §1.5 give

`||[tau^2_r(A), v_f]|| <= (2||A|| ||v_f||/C)(e^{2||Phi'||_F C|r|}-1) D(R,M_f)`, `C<=224`, `||Phi'||_F<=1323|tau|`,

with `D(R,M_f) <= sum_{x in R} sum_{y in M_f} F(d(x,y)) <= 3(F(N)+F(N-1))` (first entry of the min in (52), `∂_{Phi'}M_f` inside `M_f`, at most three owners).

### 3.3 The time integral

With `v=2||Phi'||_F C`, `int_0^U (2/C)(e^{vr}-1)dr = (2/C)(e^{vU}-1-vU)/v = 2||Phi'||_F U^2 E(vU)`, where `E(y)=2 sum_{j>=0} y^j/(j+2)!`. Since `(j+2)!>=24·5^{j-2}` for `j>=2`, `E(y) <= E_up(y) = 1+y/3+y^2/(12(1-y/5))`, a rational function. At the cap `y=592704·10^-8=9261/1562500`: `E_up = 48866741088707/48770243750000` (preview `1.00197861095797`); the directed exact-exponential enclosure of `E` (`1.00197861095729...`) lies below `E_up`, by about `7e-13`.

### 3.4 Sum over the extra faces: `b(N)` and the constant

`sum_{f in E_N} ||v_f|| D(R,M_f) <= (|tau|/3)·28N(5N+1)·3·(N^-4+(N+1)^-4) <= 56|tau|(5N+1)N^-3` (using `N(N+1)^-4<=N^-3`; linear addition, no root-N). Hence, for `|theta|<=8`, `N>=2` and both signs,

`||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| <= b(N)||A||`, `b(N) = 2·1323|tau|·U^2·E_up(592704|tau|U)·56|tau|·(5N+1)N^-3 = K_cmp(5N+1)N^-3`,

**`K_cmp = 148176 tau^2 U^2 E_up(592704|tau|U) = 452554889222515527/30481402343750000000000000000`** (preview `1.48469182657e-11` at `|tau|=10^-8`, `U=1`).

Frozen target `6x10^-11 (5N+1)N^-3`: since both sides carry the same `(5N+1)N^-3`, one inequality covers every `N>=2`; margin `4.04124269603`. The `-tau` evaluation replays the same `|tau|` formula (not a second confirmation). Values:

| `N` | `b(N)` | target `6x10^-11(5N+1)N^-3` |
|---|---|---|
| 2 | `2.04145126153e-11` | `8.25e-11` |
| 3 | `8.79817378709e-12` | `3.55555555555e-11` |
| 10 | `7.57192831552e-13` | `3.06e-12` |
| 100 | `7.43830605113e-15` | `3.006e-14` |

The bound decays like `N^-2` (the extra faces sit on the surface, about `N^2` faces at distance about `N`, `F~N^-4`). It grows like `U^2 e^{vU}` with the window and is **not uniform in time** (the ratio of the constant at `U=2` and `U=10` to the one at `U=1` is recorded in the controls; it grows faster than `U^2`).

### 3.5 Why the first order vanishes, and the tau order

To first order in the coupling, the Dyson term of `tau^1_u-tau^2_u` is `i int_0^u tau^0_s([V_N, tau^0_{u-s}(A)])ds` with `tau^0` the zero-coupling dynamics generated by the on-site sum alone. `tau^0` is a product of on-site unitaries and maps `B(H_R)` into itself, and no extra face meets `R` (§2.3), so `[V_N, tau^0_{u-s}(A)]=0` identically: the first order vanishes. In the bound, `e^{vr}-1=O(|tau|r)` multiplies `||v_f||=|tau|/3`, giving `O(tau^2U^2)`. The checker shows `K_cmp/tau^2` decreasing to 148176 (`148469.1826`, `148178.9275` at `tau/100`, `148176.0292` at `tau/10^4`) and `K_cmp/tau -> 0`; the exact ratio `K_cmp(tau)/K_cmp(tau/100) = 38176688920663121234473000000/3810205403940325763421973` (about `10019.588`) lies in `[9500,10500]` and in `[9900,10100]`. A linear-in-tau label (the naive `2U sum||v_f||` bound, ratio 100) is rejected.

### 3.6 Labelled values (not headline)

- Enumerated boundary sums: summing `F` exactly over the enumerated owners, `sum_f sum_{x in R, y in M_f}F(d(x,y)) = 616396498531/82978560000` (about 7.428) at `N=2` against the all-size `84N(5N+1)(N^-4+(N+1)^-4)` (about 138.3), and about 3.938 at `N=3` (against about 65.5). The labelled comparison values are `6.56479705992e-13` (`N=2`) and `3.48032930565e-13` (`N=3`); they are valid sharper numbers at `N=2,3` only; the headline is the all-size bound.
- Inner-family swap: the same computation with F1 inside the integral uses `Phi`, 2268|tau|, and gives `254016 tau^2U^2E_up(1016064|tau|U)` (about `2.5488e-11`), which is the forward's route. Using `2268` with F2 inside, or `1323` with F1 inside, without naming a re-indexed interaction, is rejected: the F1 box is not the native restriction of `Phi'` (616 faces missing at `N=2`) and the F2 box is not the native restriction of `Phi` (60 partial star groups at `N=2`).

## 4. Item 4 — within-family Cauchy estimates, limits, identification and O6

### 4.1 Own-family Duhamel between `Lambda_N` and `Lambda_M`

Fix a family `F`, `N>=2` and `M>N`. On `H_{Lambda_M}` put `Htilde_N := H^F_N (x) 1 + sum_{x in Lambda_M minus Lambda_N} h_x`, whose evolution on `B(H_R)` is `tau^{F,N}(A)(x)1` (exact factorization, §2.1), and `H^F_M = Htilde_N + V_{N,M}`. The source `V_{N,M}` is exactly the new terms: for F1 the whole stars `X` inside `Lambda_M` but not inside `Lambda_N`; for F2 the faces with `M_f` inside `Lambda_M` but not inside `Lambda_N`. Every new term meets `Lambda_M minus Lambda_N`; no old term is charged. §3.1 with the **larger box `Lambda_M` inside the commutator** gives

`||T^{F,M}_theta(A)-T^{F,N}_theta(A)|| <= sum_{X new} int_0^{|u|} ||[Phi^F(X), tau^{F,M}_r(A)]|| dr`,

and `tau^{F,M}` is the native restriction of the family's own interaction (`Phi` for F1, `Phi'` for F2) to `Lambda_M`, so Theorem 3.1 applies with the family's own constants, independent of `Lambda_M`. F2 regrouping: from `Lambda_2` to `Lambda_3`, 61 old anchors have groups that grow and already hold 616 faces; charging whole anchor groups would re-charge those 616. The owner-set indexing charges only the 3920 new faces, each once.

### 4.2 Source geometry and the polynomial tail

A new term is not inside `Lambda_N`, so it has a point with sup-norm at least `N+1`; its points differ by at most 1 in each coordinate, so **every point has sup-norm at least N**. In particular no new term meets `R` for `N>=2` (stars through `0` or `e_z` lie in `Lambda_2`), and Theorem 3.1's disjointness holds. Exchanging sums,

`sum_{X new} ||Phi(X)|| D(R,X) <= sum_{x in R} sum_{y: |y|_inf>=N} F(d(x,y)) sum_{X∋y} ||Phi(X)|| <= J_F (T(N)+T(N-1))`,

where `T(m)=sum_{r>=m}(4r^2+2)(1+r)^-4 <= 4 sum_{k>=m+1}k^-2 <= 4/m`, because `{|y|_inf>=N}` lies inside `{|y|_1>=N}` (around `0`) and inside `{|y-e_z|_1>=N-1}` (around `e_z`). Hence the source is at most `J_F(4/N+4/(N-1)) <= 8J_F/(N-1)` with `J_{F1}=J=28|tau|` and `J_{F2}=J'=49|tau|/3` (incoming anchors included), uniformly in `M`, hence for the supremum over all `M>N`. The enumerated `Lambda_2 -> Lambda_3` sources (F1: 152 new stars, source sum about `13.005|tau|`; F2: 3920 new faces, about `6.317|tau|`) lie far below `8J=224|tau|` and `8J'`.

### 4.3 The Cauchy constants

**F1** (inner F1, `Phi`, `||Phi||_F<=2268|tau|`, `x=2·2268·224|tau|U`):

`sup_{M>N} ||T^{F1,M}_theta(A)-T^{F1,N}_theta(A)|| <= 2||Phi||_F U^2 E_up(x)·8J/(N-1) = c1/(N-1)`,

**`c1 = 1016064 tau^2U^2E_up(1016064|tau|U) = 12128856933354903/118967041015625000000000000`** (preview `1.01951404605e-10`), at most `2.5x10^-10`, margin `2.45214865814`.

**F2** (inner F2, `Phi'`, `||Phi'||_F<=1323|tau|`, face by face):

`sup_{M>N} ||T^{F2,M}_theta(A)-T^{F2,N}_theta(A)|| <= 2||Phi'||_F U^2 E_up(x')·8J'/(N-1) = c2/(N-1)`,

**`c2 = 345744 tau^2U^2E_up(592704|tau|U) = 1055961408185869563/30481402343750000000000000000`** (preview `3.46428092867e-11`), margin `7.21650481434`.

Both are quadratic in `tau` (the Duhamel integrand vanishes at zero time because no new term meets `R`); exact `tau/100` ratios `13564609990853609831750000/1351916508459800973113` (about `10033.615`) and `38176688920663121234473000000/3810205403940325763421973` (about `10019.588`), both in `[9500,10500]`.

### 4.4 Whole-sequence convergence and each family's own limit

The Cauchy bounds hold for every `M>N` (not only `M=N+1`), so both **whole sequences** `(T^{F,N}_theta(A))_{N>=2}` converge in norm, uniformly for `|theta|<=8`. Theorem 4.1 applied to `Phi` (F1) and to `Phi'` (F2) gives for every local `A` the norm limit, uniformly on compact time sets and independent of the exhausting sequence, each extending to a one-parameter group of `*`-automorphisms of the quasi-local algebra; for F1 this limit is the AQ1 `T_theta` (AQ1 §3). Letting `M->∞` in the Cauchy bounds:

`||T_theta(A)-T^{F1,N}_theta(A)|| <= c1/(N-1)||A||` and `||T^{F2}_theta(A)-T^{F2,N}_theta(A)|| <= c2/(N-1)||A||`, both at most `2.5x10^-10/(N-1)||A||`.

### 4.5 Identification of the F2 limit with the AQ1 limit

For `A in B(H_R)`, `||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| <= b(N) -> 0` along the whole sequence, so `T^{F2}_theta(A)=T_theta(A)`. For a general local `A in A_X` with `X` inside `Lambda_{N0}`, the same §3 argument applies for `N>=N0+2`: the extra-face owners are at l1 distance at least `N-N0` from `X`, so `b_X(N) <= 2·1323|tau|U^2E_up·(|tau|/3)·28N(5N+1)·3·|X|·(1+N-N0)^-4 -> 0` (example `X=Lambda_1`, 27 sites: about `1.022e-11`, `1.004e-13`, `1.002e-15` at `N=10, 100, 1000`). Hence the two automorphism groups agree on the local algebra and, being isometric, on its norm closure: **the F2 limit dynamics is the AQ1 limit dynamics `T_theta`**, identified through the comparison bound (not through the static AY1 closeness).

### 4.6 A labelled weaker bound

The triangle inequality through the two limits gives only `||T^{F2,N}-T^{F1,N}|| <= (c1+c2)/(N-1)`, an `O(1/N)` bound that fails the comparison target: at `N=2` it is `1.36594213892e-10` against `8.25e-11`, and at `N=1000` it is `1.36730944837e-13` against `3.0006e-16`. It is reported only as a labelled weaker bound; the headline comparison is §3.

### 4.7 O6: AQ1 §§4–5 rerun for every F2 subsequential limit state

AY1 (§1.5, gate) admits F2 local trace-norm compactness and a diagonal extraction of its own. Let `omega` be an F2 subsequential limit: the local trace-norm limit of the simple F2 ground states `omega_{N_k}` (of `H^{(2)}_{N_k}`, equivalently of the padded operator) along **F2's own subsequence** `N_k`. Every statement below holds for a chosen subsequential limit of F2, each one separately; states converge only along subsequences, and no state convergence, common limit state or equality of states is claimed.

(a) **Stationarity under `T_theta`.** Fix `A in B(H_R)`, `|theta|<=8` and `L>=2`. For `N_k>L`, `omega_{N_k}(T^{F2,N_k}_theta(A))=omega_{N_k}(A)` (the ground state is an eigenvector), and the Cauchy bound gives `||T^{F2,N_k}_theta(A)-T^{F2,L}_theta(A)||<=c2/(L-1)`. `T^{F2,L}_theta(A)` lies in the fixed region `Lambda_L`, so local trace-norm convergence passes `k->∞`: `|omega(T^{F2,L}_theta(A))-omega(A)|<=c2/(L-1)`. With §4.4, `|omega(T_theta(A))-omega(A)| <= 2c2/(L-1)` for every `L` (about `7.70e-12`, `7.00e-13`, `6.94e-14` at `L=10, 100, 1000`), hence `omega∘T_theta=omega`. For general local `A in A_X` the same holds with the general-`X` Cauchy bound `2||Phi'||_F U^2E·J'|X|·4/(L-N0)` (or Theorem 4.1 for `Phi'`), then by density on the quasi-local algebra; the window extends to all `theta` by the group property.

(b) **Strong continuity of the GNS evolution.** Stationarity makes `U_theta pi(A)Omega = pi(T_theta(A))Omega` a well-defined unitary group. For the fixed region `Lambda_L`, `theta -> omega(A^* T^{F2,L}_theta(A)) = Tr(rho_L A^* T^{F2,L}_theta(A))` is continuous (strongly continuous finite unitary group; normal density `rho_L`, trace-class sum with dominated convergence). The uniform approximation of `T_theta(A)` on the window passes continuity to `omega(A^*T_theta(A))`, and `||(U_theta-1)pi(A)Omega||^2 = 2omega(A^*A)-2Re omega(A^*T_theta(A)) -> 0`; density of local cyclic vectors, unitarity and the group law extend this to all vectors and all `theta`. Stone's theorem gives `U_theta=exp(i theta G)`, `G=H_phys/alpha` self-adjoint, `G Omega=0`, with no reset of the physical clock.

(c) **Nonnegative generator.** With `G_N=(Hhat_N-E_N)/8>=0`, the finite correlation `c_N(theta)=omega_N(A^* T^{F2,N}_theta(A)) = <A Omega_N, e^{i theta G_N} A Omega_N>` is the Fourier transform of a positive measure supported on `[0,∞)`. `c_{N_k}(theta) -> c(theta)=<pi(A)Omega, U_theta pi(A)Omega>` for every `theta` (error at most `2||A||^2 c2(Theta)/(L-1)+o_k(1)` on any window `|theta|<=Theta`, since the same formulas hold at `U=Theta/8` with a constant that grows with `Theta`), and all `|c_N|<=||A||^2`. For nonnegative `f in C_c^∞((-∞,0))`, `int f dnu_{N,A}=0` passes to the limit by Fourier inversion and dominated convergence; the negative spectral projection of `G` annihilates every local cyclic vector and, by density, vanishes: `G>=0`.

(d) **Gauge restriction.** Every retained F2 term is an on-site Casimir or a Wilson loop and the F2 ground state is simple, so `omega_{N_k}` and hence `omega` are invariant under every original endpoint gauge action; `T_theta` preserves the gauge-invariant algebra (norm limit of gauge-invariant finite evolutions), so the physical cyclic space reduces `U_theta` and `G`.

The exact fixture `H=diag(0,1)`, `A=sigma_x`, `u=pi/2` keeps (a)–(d) separate from any claim about correlations: `omega_0(A tau(A))=i` but `omega_1(A tau(A))=-i` under one algebraic dynamics, so equal dynamics does not make correlation functions of different states equal.

### 4.8 The rate is O(1/N) and is honest

The Cauchy rate comes from the full exterior tail `T(N)`, which for `F(r)=(1+r)^-4` is of order `4/N`. The exact lower witnesses `m·S(m) >= 1/2` for `m=2,...,256` (with `S(m)=sum_{r=m}^{2m-1}(4r^2+2)(1+r)^-4`) show that no faster (in particular no exponential) rate in `N` follows from these constants. The comparison rate `N^-2` is faster only because its source lives on one surface layer. An `N` to `N+1` bound alone is not a Cauchy estimate: increments `c/(N-1)` sum like the harmonic series, which diverges. Every rate is in `N` at fixed spacing, per coarse step (a coarse step is `(4a,2a,a)`); nothing is uniform in the lattice spacing and no physical length is read.

## 5. Item 5 — honest meaning, mandatory template and gate fields

**Meaning.** This is an algebraic comparison of the Heisenberg dynamics of the two named constructions F1 and F2 on the compact window `|theta|<=8`, at the same coupling and at a rate in `N`. It does not state that the GNS dynamics or the correlation functions of different states agree (that would need a proved common state, BB2); it is not uniform in time; it is not uniform in the lattice spacing `a`; it does not concern weak coupling or the continuum. The mandatory sentence template, quoted verbatim once:

> For the zero-selected patterned family at the same coupling |tau|<=10^-8 and every A in B(H_R) with ||A||<=1 on the fixed cover R, the finite-box Heisenberg evolutions T^{F1,N}_theta and T^{F2,N}_theta of the named construction families F1 and F2 on the same centered coarse cube Lambda_N satisfy ||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| <= b(N) for |theta|<=8 in the common clock theta=alpha t/hbar; this is an algebraic comparison of the dynamics of the named constructions on a compact time window at a rate in N, not equality of GNS dynamics or of correlation functions of different states, not a uniform-in-time statement, and not a statement uniform in the lattice spacing a.

Here `b(N) = K_cmp(5N+1)N^-3` with `K_cmp` as in §3.4.

**Gate fields** (exported from `preregistration.gate_fields_required`; a field shown true is exported true only because its targets are admitted): `rate_in_N_claimed`, `whole_sequence_claimed` and `dynamics_limit_identified_claimed` are true; `uniqueness_of_ground_state_claimed`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `rate_in_a_claimed`, `continuum_claim`, `scientific_priority_verified`, `common_limit_claimed` (no common limit of states), `state_convergence_claimed`, `translation_invariance_claimed` and `weak_coupling_claim` are false; `whole_sequence_scope` (the contract text: dynamics only, no state) and `dynamics_level` (`algebraic_heisenberg_compact_window`) are unchanged.

## 6. Item 6 — scaling, trap fixtures and controls

### 6.1 `tau -> tau/100`

Each headline constant is evaluated twice from the same exact rational formula without intermediate rounding; brackets are read from the contract.

| constant | exact ratio | preview | bracket |
|---|---|---|---|
| comparison `K_cmp` | `38176688920663121234473000000/3810205403940325763421973` | `10019.5881516` | `[9500,10500]` and `[9900,10100]` |
| Cauchy `c1` | `13564609990853609831750000/1351916508459800973113` | `10033.6151722` | `[9500,10500]` |
| Cauchy `c2` | `38176688920663121234473000000/3810205403940325763421973` | `10019.5881516` | `[9500,10500]` |

### 6.2 Exact finite fixtures for the traps

1. **Polynomial versus exponential tail:** exact rationals `m·S(m) >= 1/2` at `m=2,...,256` (the half-shell sum is about `2/m`); a claimed `C0 q^m` decay is rejected (for `C0=1`, `q=1/2` it already fails at `m=2`).
2. **An unbounded on-site term placed wrongly:** the cutoff ladder `h_L=diag(0,...,L)` placed as a one-site interaction gives `||Phi||_F>=L` and a velocity of at least `448L` for `L=1,10,100,1000`; no cutoff-uniform constant exists, while the correct placement has constants independent of `L`.
3. **Padding on-site terms left in the Duhamel difference:** §2.1's exact Gaussian-rational fixture shows the factorization is exact, while a source charged with `h_p` has norm equal to the cutoff.
4. **An inner-family constant swapped:** on `Lambda_2`, F1 is not the native restriction of `Phi'` (616 faces missing) and F2 is not the native restriction of `Phi` (60 partial groups); a bound record naming F2 inside with `Phi`/2268 or F1 inside with `Phi'`/1323 is rejected.
5. **An N to N+1 bound summed as a Cauchy estimate:** increments `1/(n+1)` tend to 0 while their partial sums diverge; only a supremum over `M>N` from one Duhamel formula is accepted.

### 6.3 Controls

All 35 contract controls (`controls`, equal to `preregistration.controls_required.ids`) are damaging-mutation controls in `check.py`: 149 mutations, each rejected with an explicit reason; none is unimplementable. The 31 controls with new semantics follow `new_control_semantics`; the 4 without an entry (`full_original_wilson_cover`, `topology_named`, `cross_coupling_comparison_rejected`, `gate_fields_topic_specific`) are implemented from their earlier-round meaning. The map is in §11.

## 7. Constants at the cap (both signs; exact rationals and truncated previews)

| symbol | exact | preview | tier / route / inner family / interaction |
|---|---|---|---|
| `K_cmp` | `452554889222515527/30481402343750000000000000000` | `1.48469182657e-11` | polynomial_lieb_robinson; reverse Duhamel over `E_N`; F2 inside; `Phi'` 1323|tau|, C<=224 |
| `c1` | `12128856933354903/118967041015625000000000000` | `1.01951404605e-10` | polynomial_lieb_robinson; own-family Duhamel `Lambda_N->Lambda_M`; F1 (`Lambda_M`) inside; `Phi` 2268|tau| |
| `c2` | `1055961408185869563/30481402343750000000000000000` | `3.46428092867e-11` | polynomial_lieb_robinson; own-family Duhamel, face by face; F2 (`Lambda_M`) inside; `Phi'` 1323|tau| |
| `E_up(592704·10^-8)` | `48866741088707/48770243750000` | `1.00197861096` | directed rational upper bound of `E` |
| `E_up(1016064·10^-8)` | (in `results.json`) | `1.00339550074` | directed rational upper bound of `E` |
| targets | `3/50000000000` and `1/4000000000` | `6e-11`, `2.5e-10` | read from the contract (sha256 pinned) |

Every constant is monotone in `|tau|` and `U`, so the cap values bound every `|tau|<=10^-8` and every `|theta|<=8`.

## 8. Error ledger (preregistered names)

| term | entry |
|---|---|
| `lieb_robinson_tail` | comparison: `F(N)+F(N-1)<=2N^-4` per owner; Cauchy: `T(N)+T(N-1)<=8/(N-1)` (polynomial tier) |
| `duhamel_boundary_sum` | comparison: `(|tau|/3)·28N(5N+1)·3·(N^-4+(N+1)^-4) <= 56|tau|(5N+1)N^-3`; Cauchy: `8J_F/(N-1)`, `J_F=28|tau|` (F1) or `49|tau|/3` (F2); linear addition |
| `interaction_picture_onsite` | `0`: `h_b` enters no constant (the `H_x` slot of (44), interaction picture inside Theorem 3.1); the padding factors out exactly |
| `inner_family_constants` | comparison and F2 Cauchy: `Phi'`, `1323|tau|`, `C<=224`; F1 Cauchy: `Phi`, `2268|tau|`, `C<=224`; time integral `2||Phi||_F U^2 E` |
| `arithmetic` | `0`: exact Fractions; `E` replaced by the directed rational `E_up`; decimals are truncated previews that no admission reads |

## 9. Exclusions and claim flags

Contract `claim_exclusions` (verbatim), none claimed:
- not claimed: equality of GNS dynamics or of correlation functions of different states;
- not claimed: uniform-in-time statements;
- not claimed: exponential decay in N with the polynomial Lieb-Robinson function;
- not claimed: uniqueness of every infinite-volume ground state;
- not claimed: any estimate uniform in the lattice spacing a;
- not claimed: continuum or weak coupling;
- not claimed: scientific priority.

Claim flags, all false: `continuum_claim`, `uniqueness_of_ground_state_claimed`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `rate_in_a_claimed`, `scientific_priority_verified`, `weak_coupling_claim`, `uniform_wilson_claim`, `resolved_interaction_shift`. Scope: only the zero-selected patterned family, `|tau|<=10^-8`, the two named families on centered cubes, fixed spacing and strong bare coupling, the window `|theta|<=8`; nothing transfers to other boundary prescriptions (literal vertex boxes, periodic or orthant boxes), to nonzero selected triples, to the uniform model, to weak coupling or to the continuum. States are compared nowhere; O6 concerns each F2 subsequential limit separately. Historical, occult or governmental material supplies no premise.

## 10. Proposed reverse verdict, independence and contract wording notes

**Proposed reverse verdict: `accepted_within_scope`** (sub-label `dynamics_on_compact_windows`): the comparison and both Cauchy estimates are proved with each constant below its frozen target, the F2 limit dynamics is identified with the AQ1 `T_theta`, and O6 is rerun for F2 limit states. The checker's rule gives `insufficient` if the Lieb–Robinson placement fails or the source is miscounted, and `limited` if any target is missed or O6 is open, retained with its dominating term at unchanged `tau` (for example a hypothetical `tau=10^-7` gives `K_cmp` about `1.5e-9`, which fails; the dominating term is the Duhamel boundary sum).

**What is inherited, not re-proved:** Theorems 3.1 and 4.1 (as stated in the committed excerpt); the I1 face dictionary; AQ1's model placement, compactness and GNS strategy; AY1's F2 simple ground state, local trace-norm compactness and diagonal extraction; the tensor-sum exponential for self-adjoint operators on separate factors; the spectral and Stone theorems.

**Independence.** The contract, the selection note and AY2 name the route and the constants (`28N(5N+1)`, `N-1`, `1323|tau|`, `2268|tau|`, `C<=224`). Independence is limited to the inner family (F2), the interaction indexing (owner sets, face-by-face charging), the own-family Cauchy route with the larger box inside, the enumeration and the all-size anchor decomposition, the cocycle derivation of the Duhamel identity, `E_up`, the constants and the code. All agents are correlated model agents.

**Contract wording notes** (non-blocking):
1. `new_control_semantics` covers 31 of the 35 controls; `full_original_wilson_cover`, `topology_named`, `cross_coupling_comparison_rejected` and `gate_fields_topic_specific` have no entry and were implemented from their earlier-round meaning.
2. `parameters` declares the metric, weights and window as fields, but `N_0` appears only in the target text ("N at least 2") and `d_X` is absent (there is no exponential target), although the round-wide control names both.
3. `preregistration.observable` names an `N` to `N+1` quantity, while the Cauchy target (rightly) is the supremum over `M>N`; the supremum is proved.
4. Item 3 writes `B(N)` and `b(N)` for the same bound; item 4 writes `tau^{F,M}_theta` for `T^{F,M}_theta`, while `tau` is also the coupling.
5. The comparison ratio has two brackets (`[9500,10500]` in the scaling brackets, `[9900,10100]` in `duhamel_tau_order_quadratic`); both are met.
6. `state_provenance` says no state enters, but the O6 requirement needs AY1's F2 subsequential limit states; they are used as AY1 admits them.
7. The template's "the same centered coarse cube Lambda_N" holds through the canonical embedding of `B(H_{Lambda_N})` into `B(H_{B_+})`: the padded Hilbert space is larger, and the factorization of §2.1 makes the comparison exact.
8. The (48)-norm of `Phi'` is exactly `108|tau|` by pair enumeration, so `1323|tau|` is a per-site upper bound, not the norm (recorded, not used).

## 11. Map of contract items and controls

| item / control | where proved | `results.json` check id |
|---|---|---|
| 1 quotation, F, C, placement, norms | §1 | `item1_ns_quotation_verbatim`, `item1_F_convolution_constants`, `item1_onsite_placement_interaction_picture`, `item1_interaction_norms_Phi_and_Phi_prime`, `i1_table_parsed_and_rederived` |
| 2 extra faces, count, distance, padding | §2 | `item2_extra_faces_enumerated_and_all_size`, `item2_padding_factorization` |
| 3 comparison, first order | §3 | `item3_duhamel_comparison_inner_F2`, `item3_first_order_vanishes_quadratic_in_tau` |
| 4 Cauchy, limits, identification, O6 | §4 | `item4_cauchy_sources_and_tails`, `item4_cauchy_F1_own_limit`, `item4_cauchy_F2_own_limit`, `item4_limit_identification`, `item4_O6_rerun_for_F2_limit_states` |
| 5 meaning, template, gate fields | §5 | `item5_honest_meaning_and_claims`, `item5_mandatory_template_once`, `report_phrase_scan_negation_aware` |
| 6 scaling, fixtures | §6 | `item6_tau_scaling_per_constant` and the trap fixtures in the controls below |
| `coherent_evidence_tampering` | §§0, 12 | same id (9 mutations incl. rebound hashes, snapshot removal, gate and excerpt edits) |
| `exact_arithmetic_admission` | §8 | same id |
| `no_priority_or_continuum_claim` | §9 | same id |
| `changed_model_relabelled` | §0 | same id |
| `insufficient_verdict_retained` | §10 | same id |
| `tau_scaling_exponent` | §6.1 | same id |
| `wrong_delta_alpha_hbar_clock` | §0 | same id |
| `missing_incoming_stars` | §§1.4, 4.2 | same id |
| `root_n_misuse` | §§3.4, 4.2 | same id |
| `tier_mixing_rejected` | §7 | same id |
| `reverse_premise_isolation` | §12 | same id (and `freeze.py`) |
| `face_count_all_sites` | §1.4 | same id |
| `uniform_in_N_not_in_a` | §§0, 4.8 | same id |
| `placeholder_span_rejected` | contract strings | same id |
| `negation_aware_phrase_scan` | whole report | same id |
| `parameters_declare_metric_weights_window` | §10 note 2 | same id |
| `lieb_robinson_polynomial_tail` | §4.8 | same id |
| `lieb_robinson_F_declared` | §1.2 | same id (no exponential instance produced) |
| `lieb_robinson_form_quoted` | §1.1 | same id |
| `unbounded_onsite_interaction_picture` | §1.3 | same id |
| `duhamel_inner_family_constants` | §§3.2, 3.6, 4.1 | same id |
| `extra_face_count_and_distance` | §§2.2–2.3 | same id |
| `duhamel_tau_order_quadratic` | §3.5 | same id |
| `time_window_named_common_clock` | §§0, 3.4 | same id |
| `algebraic_not_gns_dynamics` | §§4.7, 5 | same id |
| `f2_limit_dynamics_equals_f1` | §§4.5, 4.7 | same id |
| `two_families_named` | §0 | same id |
| `subsequence_versus_whole_sequence` | §§4.4, 4.7 | same id |
| `decay_rate_in_N_not_a` | §4.8 | same id |
| `boundary_source_new_terms_only` | §§2.4, 4.1 | same id |
| `f2_regrouping_charged_once` | §4.1 | same id |
| `full_original_wilson_cover` | §0 | same id |
| `topology_named` | §1.3 | same id |
| `cross_coupling_comparison_rejected` | §5 | same id |
| `gate_fields_topic_specific` | §5 | same id |

## 12. Files read, scratch disclosure and reproduction

**Snapshots read in full:** the contract, `AGENTS.md`, `selection-ba2.md`, the Nachtergaele–Sims excerpt; the AQ1 forward report, gate and skeptic review; the I1 forward report; the AY1 reverse report; the AM2 skeptic review; the Round32 state-lemma reference and the complete-residual reference; the paired-physics, Newton, Tesla and historical-panel SKILL files; the AQ source dictionary and primary bindings. **Read in part:** the AY1 forward report (its first half and a keyword search), the AY2 forward report (statement and obligations table, O5/O6), the AY1, AY2, AV1 and AM2 gates (every field except the bindings lists), the AM2 forward report (opening section). **Not opened:** the AQ2 forward report, the AM2 reverse report, the AV1 forward and reverse reports. The Newton, Tesla and historical-panel skills were used only as modern methodological lenses (analysis backward from the desired comparison, i.e. the reverse route, before synthesis forward; the whole-device check that the padding load is accounted for; a derivative is not a finite-time estimate, so no norm derivative in time). No historical figure endorses anything here.

**Non-scientific style files outside `inputs/`:** `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py`, and `research/round32/reverse/ay1/check.py` and `report.md` (conventions only; I also listed the files of `research/round32/reverse/ay1/` and viewed the head of its `output/source-manifest.json`). None carries premise weight.

**Scratch disclosure.** My private scratch folder is `/tmp/claude-0/ba2-reverse-private/` (created with `mkdir -p` without listing its parent). It holds exploratory Fraction/float prototypes (`proto.py`, `consts.py`), a development harness that runs this checker against a stub report (`dev_run.py`, `dev_values.py`, `report_stub.md`, `dev_results.json`), the quote extraction (`quotes.txt`), the report draft and renderer, and the production runs. **Nothing in it is evidence.** I opened no other agent's folder and no file in the shared session scratchpad.

**Reproduce** (fresh absolute output directories outside the checkout):

```bash
python3 -B research/round33/reverse/ba2/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/reverse/ba2/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/freeze.py verify research/round33/reverse/ba2
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/ba2.json research/round33/reverse/ba2/report.md
```
