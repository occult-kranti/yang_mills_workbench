# BA2 independent derivation before producer comparison

**Standing.** I wrote this after the BA2 contract froze (`frozen_at` 2026-09-24T21:56:46Z, sha256 `275ba3b0…fcff`), and before reading either producer.

**Isolation.**
- I did not open, list or read `research/round33/forward/ba2/`, `research/round33/reverse/ba2/`, `research/round33/forward/ba1/` or `research/round33/reverse/ba1/`.
- The one exception: I ran `find` on the two BA2 `inputs/` folders and compared the snapshots with the repository by sha256 (29 files each, all identical).
- I did not touch the concurrent skeptic's BA1 files.

**Sources.**
- The frozen contract, `advisor/selection-ba2.md`, `advisor/deliberation-2.md` (recorded previews), `advisor/plan.json`, and the committed excerpt `sources/nachtergaele-sims-1410.8174v1.md`.
- AQ1 forward and gate; the AQ1 review and the Round29 source dictionary and bindings.
- AY1 forward and reverse and their gate; the AY2 gate; the I1 report (§§1–6).
- My Round33 triage, loop-2 review, recommendation and prospective controls, and my Round32 AY1 package (for format).

**Scratch and exposure.**
- Scratch work stayed in the private folder `/tmp/claude-0/skeptic-ba2-private/`: preview scripts, enumeration prototypes, replay directories, and mutated copies of the checker used to test that controls bite.
- One `ls /tmp/claude-0/` early in the session showed other folder names, including my older skeptic folders and Round32 producer folders. I opened none of them.
- After `results.json` and every value here were final, one `git status --short` displayed untracked file names:
  - `forward/ba1/{check.py,report.md}`, `forward/ba2/{check.py,report.md}`, `reverse/ba1/{check.py,report.md}` and `reverse/ba2/check.py`;
  - the concurrent skeptic's `ba1_check.py`.

  This was a name-only exposure. I opened none of these files.

**Correlated ancestry.**
- My triage proposed this loop's route and previews.
- My loop-2 review corrected the reverse route and wrote most of the frozen control semantics.
- What follows is a re-derivation in fresh code, not independent discovery or human review.

**Exactness.** Exact values come from `ba2_check.py`:
- 95 checks, of which 38 are controls (the 35 contract ids plus 3 extras) with 101 damaging mutations;
- byte-identical results under `python3 -B` and `python3 -B -O`, and under two hash seeds.

Every decimal below is a preview of an exact rational or a directed enclosure. Human project author: Hruday N M (BUNZEEY).

## 1. Model, clock and placement

**Model.**
- Zero-selected patterned family: SU(2) Kogut–Susskind form on Z³ at fixed spacing, with coarse 24-link factors.
- Selected triple (0,0,0); normalized units δ = α/8.
- On-site term h_b = 8Σ_{e∈b} C_e ≥ 6Q_b: unbounded, self-adjoint, with compact resolvent.
- 21 omitted faces per anchor, each entering as V_f = −(τ/3)W_f with ‖W_f‖ ≤ 1.
- Both signs of |τ| ≤ 10⁻⁸; cover R = {0, e_z}.

**Families on Λ_N = [−N,N]³ (coarse), N ≥ 2.**
- F1 (AQ1): H^(1)_N = Σ_{x∈Λ_N} h_x + Σ_{b+S⊂Λ_N} φ_b, where φ_b = Φ(b+S) is the whole star, S = {0, e_x, e_y, e_z}. This is the Nachtergaele–Sims (NS) native restriction of the whole-star interaction Φ.
- F2 (I1 §6, AY1 F02):
  - Unpadded: H^(2)_N = Σ_{x∈Λ_N} h_x + Σ_{O⊂Λ_N} Φ′(O), where Φ′(O) = −(τ/3)Σ_{f: O(f)=O} W_f is the owner-set interaction. This is the native restriction of Φ′.
  - Padded: H^{F2,pad}_N = H^(2)_N ⊗ 1 + 1 ⊗ Σ_{x∈B_+∖Λ_N} h_x on B_+ = Λ_N + S. It is not the native restriction of Φ′ on B_+.

**Clock.**
- θ = αt/ħ (real time) and s = α t_E/ħ (Euclidean).
- The normalized time is u = δt/ħ = θ/8, used internally only. The contract window |θ| ≤ 8 is U := max|u| = 1.
- NS's t is u, and NS's τ_t^Λ(A) = e^{itH_Λ}Ae^{−itH_Λ} is our T^{F,N}_θ(A) with t = θ/8. The NS τ is never the coupling.
- The Round29 source dictionary calls u "s = δt/ħ". That label is forbidden here.

**Placement of the unbounded terms (NS (44)–(47), proof steps (54), (57)).**
- NS assumes self-adjoint on-site operators H_x on H_x, and bounded Φ(X) = Φ(X)* ∈ A_X.
- Here H_x := h_x and Φ := the faces. No on-site operator ever enters Φ.
- The NS proof puts the on-site terms (and Φ on the subsets of X) into the interaction-picture generator H_0 of (54). e^{itH_x} is an automorphism of A_x, so it preserves supports. The velocity 2‖Φ‖C therefore does not depend on h_x.
- If h_x were placed in Φ, ‖Φ‖_F would be at least ‖h_x 1[spin ≤ j]‖ = 8·24·j(j+1), which is unbounded in the cutoff. The checker's fixture gives velocity ratios of 5.1×10⁸ to 1.7×10¹² for j = 1/2 to 50.

## 2. The Lieb–Robinson inequality, quoted, and its instance

Quoted from the committed excerpt, Part A (checked against Part B by the checker):

> **Theorem 3.1.** Let Γ and F be as indicated above. Fix a collection of local Hamiltonians {H_x}_{x∈Γ} and an interaction Φ ∈ B_F(Γ). Let X, Y ⊂ Γ be finite disjoint sets. For any finite Λ ⊂ Γ with X ∪ Y ⊂ Λ and any A ∈ A_X and B ∈ A_Y, the bound
> (51) ‖[τ_t^Λ(A), B]‖ ≤ (2‖A‖‖B‖ / C) (e^{2‖Φ‖C|t|} − 1) D(X, Y)
> holds for all t ∈ ℝ, where the quantity D(X, Y) is given by
> (52) D(X, Y) = min{ Σ_{x∈X} Σ_{y∈∂_Φ Y} F(d(x, y)), Σ_{x∈∂_Φ X} Σ_{y∈Y} F(d(x, y)) }.

The definitions are (40) ‖F‖, (41) C, (48) ‖Φ‖ = sup_{x,y} F(d(x,y))⁻¹ Σ_{X∋x,y}‖Φ(X)‖ and (49)–(50) ∂_Φ. The limit dynamics is Theorem 4.1, (77) τ_t(A) = lim_{Λ→Γ} τ_t^Λ(A), uniform for t in compact sets and independent of the increasing sequence. Cite it as "Section 4": its title carries a forbidden phrasing.

**Instance.**
- Γ = Z³ (coarse), d = ℓ1, F(r) = (1+r)⁻⁴.
- The shell at ℓ1 radius r has 4r²+2 sites (checked for r ≤ 12).
- ‖F‖ = 4ζ(2) − 8ζ(3) + 6ζ(4) − 1 ≈ 2.4572. The exact enclosure is [2.3932, 2.4588], below AQ1's bound 7.
- C ≤ 32‖F‖ ≤ 224 (AQ1 §3, parsed from the bound report; the half-split inequality F(r/2) ≤ 16F(r) is checked).
- **Φ (whole stars).** A star has ℓ1 diameter 2, and each site lies in 4 stars (incoming anchors included), each of norm ≤ 7|τ|. So J = 28|τ| and ‖Φ‖_F ≤ 81J = 2268|τ|.
- **Φ′ (owner sets).** An owner set has ℓ1 diameter ≤ 2, and each site lies in the owner sets of 49 faces. So the per-site sum is 49|τ|/3 and ‖Φ′‖_F ≤ 81·49|τ|/3 = 1323|τ| (AY1 reverse).
- Labelled observation, not used: the enumerated sup in (48) is 567|τ| for Φ (a distance-2 pair lies in one star) and 108|τ| for Φ′ (attained at (b+e_y, b+e_z)).
- Velocities: v = 2C‖Φ‖ ≤ 1016064|τ| and v′ = 592704|τ| per unit u; at the cap, v = 3969/390625 and v′ = 9261/1562500.

**Monotonicity (needed because C sits in a denominator).**
- Write E(x) := e^x − 1 − x. Then (e^{2‖Φ‖Cs} − 1)/C and ∫_0^U(e^{2‖Φ‖Cs} − 1)ds/C = 2‖Φ‖U²·E(x)/x², with x = 2‖Φ‖CU, are nondecreasing in C and in ‖Φ‖, because E(x)/x² = Σ_{k≥2} x^{k−2}/k!.
- So the upper bounds C ≤ 224 and ‖Φ‖_F ≤ 2268|τ| (or 1323|τ|) may be substituted.
- At leading order C cancels. It enters only through the factor E(x)/(x²/2) = 1 + x/3 + ….

**Directed arithmetic.**
- e^x ∈ [Σ_{k≤30} x^k/k!, Σ_{k≤30} x^k/k! + x³¹/31!·32/(32−x)] for 0 ≤ x ≤ 1.
- The closed skeptic form uses E(x) ≤ (x²/2)/(1 − x/3), valid because k! ≥ 2·3^{k−2}.
- The modern form uses E(x) ≤ (x²/2)e^x.

## 3. The boundary source: the extra F2 faces

**Faces from fine coordinates.**
- π(x,y,z) = (⌊x/4⌋, ⌊y/2⌋, z), with Euclidean division, so negative coordinates are handled.
- The face at p in directions (a,c) has owner set O(f) = {π(p), π(p+e_a), π(p+e_c)} (I1.4). Its anchor is π(p) ∈ O(f).
- Each anchor has 24 faces: 3 selected, with owner set {b}, and 21 omitted.
- The omitted owner types relative to b are: {0,e_z} 10, {0,e_y,e_z} 4, {0,e_y} 3, {0,e_x,e_z} 2, {0,e_x} 1, {0,e_x,e_y} 1. This matches the parsed I1 table row by row, and translation covariance holds for all 343 anchors in [−3,3]³.
- Per site: 49 faces, 15 owner sets, 4 incoming stars.
- On R: 82 faces meet R, 10 lie inside R, from 7 incident anchors and 27 owner sets.

**The difference of the two Hamiltonians.**
- F1 retains the faces of anchors with b+S ⊂ Λ_N. F2 retains every face with O(f) ⊂ Λ_N. So F1 ⊂ F2.
- Since b ∈ O(f), F2 has no anchor outside Λ_N. The extra faces are those with O(f) ⊂ Λ_N and b ∈ Λ_N but b+S ⊄ Λ_N.
- The last condition means b_i = +N for some i. The anchors on the lower faces (b_i = −N only) contribute nothing, because S has only nonnegative offsets.
- Hence H^(2)_N − H^(1)_N = Σ_{f∈E_N} V_f, with every extra face charged exactly once (at its unique anchor, or at its owner set; the charge is the same).

**All-size count.**
- Let Out(b) = {i : b_i = N}. At an anchor with Out(b) ≠ ∅, F2 keeps exactly the face types that avoid every e_i with i ∈ Out(b).
- The number of such types per anchor is: x 17, y 13, z 5, xy 10, xz 3, yz 1, xyz 0.
- The anchor counts are (2N)² for each single class, 2N for each pair, and 1 for xyz.
- Hence |E_N| = 4N²(17+13+5) + 2N(10+3+1) = 140N² + 28N = **28N(5N+1)**.
- The enumeration agrees for N = 2, 3, 4, 5: 616, 1344, 2352, 3640.
- The family sizes are 21(2N)³ for F1 and 14m(m+1)² + 7m²(m+1) for F2 (m = 2N); for N = 2 these are 1344 and 1960.
- Summing owner sizes over the extra faces gives 308N² + 56N = 28N(11N+2) owner incidences (enumerated: 1344, 2940, 5152, 7980).

**Distances.**
- Every owner of an extra face keeps the coordinate y_i = N for i ∈ Out(b), because it is b or b + e_j with j ∉ Out(b). So max_i |y_i| = N.
- Hence d_1(y, e_z) ≥ N−1, with equality only at y = (0,0,N), and d_1(y, 0) ≥ N.
- Exactly 11 extra faces reach distance N−1, for every N:
  - 5 anchored at (0,0,N);
  - 2 at (−1,0,N) through their e_x owner;
  - 4 at (0,−1,N) through their e_y owner.

  The enumeration confirms this for N = 2..5.
- The owner sets have at most 3 sites, and they are disjoint from R for N ≥ 2.
- In fine units (display only), the nearest owner is N−1 coarse z-steps, that is (N−1)a, from e_z. No constant uses fine units.

**Padding factors out exactly.**
- The padding operator 1 ⊗ Σ_pad h_x commutes with H^(2)_N ⊗ 1, with every face and with B(H_R), since no retained face has an owner among the padding sites (checked).
- Hence e^{iuH^{F2,pad}} = e^{iuH^(2)_N} ⊗ e^{iuH_pad}, and T^{F2,pad,N}(A ⊗ 1) = T^{F2,N}(A) ⊗ 1 for A ∈ A_{Λ_N}.
- The exact fixture checks ad^k_{H_in⊗1+1⊗h_pad}(A⊗1) = (ad^k_{H_in}A)⊗1 for k ≤ 7.
- The padding therefore contributes 0. Charging it instead puts ‖h_pad 1[≤L]‖ = L into the source, which is unbounded in the cutoff.
- There are 3(2N+1)² padding sites: 75, 147, 243, 363.

## 4. The Duhamel comparison

**Duhamel identity with unbounded on-site terms.**
- H^(1)_N and H^(2)_N have the same on-site sum, and ΔH := H^(2)_N − H^(1)_N is bounded. So D(H^(2)) = D(H^(1)).
- W(s) := e^{isH²}e^{−isH¹} satisfies W(s) = 1 + i∫_0^s W(r)T¹_r(ΔH)dr strongly, and W(s)* is strongly C¹ with derivative −iT¹_s(ΔH)W(s)*.
- Since T²_s(T¹_{u−s}(A)) = W(s)T¹_u(A)W(s)*, the product rule gives d/ds = iT²_s([ΔH, T¹_{u−s}(A)]). Hence

  T^{F2,N}_u(A) − T^{F1,N}_u(A) = i∫_0^u T²_s([ΔH, T¹_{u−s}(A)]) ds (strong integral) — inner F1;

  and, with the roles exchanged, the same identity with T¹ outside and T² inside — inner F2.
- The exact fixture checks the Taylor coefficients to order 6 on a two-site toy (ad_{H2}^n − ad_{H1}^n = Σ_{j+k=n−1} ad_{H2}^j ad_V ad_{H1}^k). It also checks that [V,A] = 0 for disjoint supports while [V,[H1,A]] ≠ 0.

**Bound with inner F1 (forward).** The outer evolution is isometric. Apply (51) with X = R, Y = O(f), Λ = Λ_N and the interaction Φ:

‖T^{F2,N}_u(A) − T^{F1,N}_u(A)‖ ≤ Σ_{f∈E_N} (|τ|/3) ∫_0^{U} (2‖A‖/C)(e^{vs} − 1) D(R, O(f)) ds = (2|τ|‖A‖/(3C v)) E(vU) Σ_{f∈E_N} D(R, O(f)).

Using D(R, O(f)) ≤ Σ_{x∈R}Σ_{y∈O(f)} F(d(x,y)) ≤ 2·3·N⁻⁴:

**b(N) = K (5N+1) N⁻³ ‖A‖, with K = 112|τ| E(vU)/(vC) = 508032 τ²U² · E(x)/x², x = vU.**

In θ this reads 3969 τ²Θ² · 2E(x)/x² with x = 127008|τ|Θ.

**The τ-order.**
- Every O(f) is disjoint from R for N ≥ 2, so [V_f, A] = 0. The integrand e^{vs} − 1 vanishes at s = 0, and there is no first-order term.
- K = 254016τ²U²(1 + vU/3 + …) is quadratic in τ: K/τ² → 254016 as τ → 0.

**Values at |θ| ≤ 8 (U = 1), |τ| = 10⁻⁸, both signs.**

| Form | K (coefficient of (5N+1)N⁻³) | Margin to 6×10⁻¹¹ |
|---|---|---|
| sharp (enclosure of E) | 2.548785115133e-11 (width below 10⁻³⁰) | 2.35406 |
| closed, (x²/2)/(1−x/3) | 3969/155720800000000 ≈ 2.548792e-11 | 2.35406 |
| modern, (x²/2)e^x | 2.566101217813e-11 | 2.33817 |
| modern with e^x ≤ 1/(1−x) | 3969/154662400000000 ≈ 2.566233e-11 | 2.33804 |
| leading term only (**not a bound**) | 3969/156250000000000 = 2.54016e-11 | — |

b(2) = 3.5046e-11, b(3) = 1.5104e-11, b(4) = 8.3632e-12, b(5) = 5.3015e-12.

The labelled refinement with the enumerated exact sums, b_exact(N) = K·S_N/168, gives 1.127e-12, 5.97e-13, 3.76e-13 and 2.59e-13 (S_N/crude = 3.2%, 4.0%, 4.5%, 4.9%). The all-size refinement (308N²+56N)(N⁻⁴ + (N+1)⁻⁴) lies between the exact and the crude sums.

**Bound with inner F2 (reverse).** Apply (51) with Φ′ on Λ_N: the unpadded F2 is the native restriction, and the padding factors out. With the same source and distances:

**K′ = 112|τ| E(v′U)/(v′C) = 296352 τ²U² · E(x′)/x′², x′ = v′U.**

| Form | K′ | Margin |
|---|---|---|
| sharp | 1.484691826572e-11 | 4.04124 |
| closed | 9261/623765200000000 ≈ 1.484693e-11 | 4.04124 |
| modern (x²/2)e^x | 1.490568529256e-11 | 4.0253 |

- A reverse that bounds the inner F2 evolution with the padded anchor-grouped interaction Ψ_N (2268|τ|) gets the forward's K. That is valid only if stated, and it removes the constant difference between the routes.
- An inner F1 evolution bounded with Φ′'s 1323|τ| is **wrong**, because F1 is not a restriction of Φ′. It would understate K by the factor 0.58.

## 5. Within-family Cauchy estimates, for all M > N

**The difference.** For M > N, compare on Λ_M. Extend T^{F,N} by the on-site terms of Λ_M∖Λ_N (these commute with A_{Λ_N}, so T^{F,N}(A) ⊗ 1 is unchanged). The difference of the generators is then bounded:
- for F1: the stars with b+S ⊂ Λ_M and b+S ⊄ Λ_N;
- for F2: the faces with O(f) ⊂ Λ_M and O(f) ⊄ Λ_N.

**Geometry.** Every site of a new star, and every owner of a new face, has |y|_∞ ≥ N. This follows because b_i = N when b ∈ Λ_N, and because |b_j| > N otherwise. It is checked for (N,M) = (2,3), (2,4) and (3,4). Per-site incidences are at most 4 stars or 49 faces, and nothing meets R.

**Tail sum.**
- (4r²+2)(1+r)⁻⁴ ≤ 4(1+r)⁻² and Σ_{m≥k+1} m⁻² ≤ 1/k.
- So Σ_{y: |y|_∞≥N} [F(d(0,y)) + F(d(e_z,y))] ≤ 4/N + 4/(N−1) ≤ 8/(N−1).
- This bound is uniform in M, so it bounds the sup over M > N, not a single step.

**Coefficients.** Each estimate has the form sup_{M>N}‖T^{F,M}_θ(A) − T^{F,N}_θ(A)‖ ≤ K_C/(N−1)·‖A‖, and hence ‖T_θ(A) − T^{F,N}_θ(A)‖ ≤ K_C/(N−1)·‖A‖.

| Family, charging, inner interaction | Leading K_C/τ² | K_C at the cap | Margin to 2.5×10⁻¹⁰ |
|---|---|---|---|
| F1, star (28\|τ\| per site), Φ | 1016064 | 1.019514046e-10 (closed 3969/38930200000000) | 2.452 |
| F1, face (49\|τ\|/3), Φ | 592704 | 5.947165269e-11 | 4.204 |
| F2, face (49\|τ\|/3), Φ′ | 345744 | 3.464280929e-11 (closed 21609/623765200000000) | 7.217 |
| F2, clipped group (28\|τ\|), Φ′ | 592704 | 5.938767306e-11 | 4.210 |
| F2 through F1 (triangle, labelled) | — | 1.720429953e-10 | 1.453 |

The triangle row uses K_C1 + 2K·max_N (5N+1)(N−1)N⁻³, and that maximum is 11/8, at N = 2: 5/N − 4/N² − 1/N³ is decreasing for N ≥ 2 because 5N² > 8N + 3.

- The rate is the honest polynomial 1/N. The fixture shows that the shell tail from distance k is at least 1/(4k) for every k, so it can never be restated as Kq^N.
- An N-to-N+1 bound c/(N−1) summed over N diverges (H_{2^k} ≥ 1 + k/2).
- The F2 row with anchor regrouping reproduces the loop-2 preview of 5.94e-11. Face-by-face charging (control `f2_regrouping_charged_once`) gives 3.46e-11.

## 6. Identification of the F2 limit dynamics with AQ1's

1. **Rate on the fixed cover.** For A ∈ B(H_R), ‖T^{F2,N}_θ(A) − T_θ(A)‖ ≤ K(5N+1)N⁻³ + K_C1/(N−1). This is 1.370e-10 at N = 2, 1.26e-11 at N = 10 and 1.02e-13 at N = 1000. F2's own Cauchy rate is K_C2/(N−1) with K_C2 = 3.464e-11.
2. **Every local A.** For A ∈ A_Y with Y finite, the same Duhamel sum with R replaced by Y is at most 3|Y|·28N(5N+1)·(1+N−r_Y)⁻⁴ times the same factor, once N > r_Y := max_{x∈Y}|x|_∞. It tends to 0.
3. **Whole sequence.** The F2 evolutions converge as a whole sequence. This follows from the Cauchy bound, and also from NS Theorem 4.1 for Φ′, whose native restrictions are the unpadded F2 boxes.
4. **Equality of the automorphisms.** The limit automorphism group of F2 agrees with T_θ on the local algebra. Both extend uniquely to automorphism groups of A_Γ, so they are equal.

This is algebraic Heisenberg dynamics on compact windows. It does not identify states, GNS dynamics or correlation functions (fixture: one dynamics, two states, ω(Z) = ±1).

## 7. AQ1 §§4–5 rerun for F2 limit states (AY2 row O6)

**Inputs for F2, all from the AY1 gate.**
- AM2 at the same J_0, for the padded family.
- A simple ground state ψ^(2)_N ⊗ Ω_pad with gap ≥ 1/2.
- Reset bounds 98|τ| on R and C_F = 56|τ||F|.
- Local trace-norm compactness, and F2's **own** diagonal extraction N_k.

The F2 limit states need not equal the AQ1 state.

**§4, stationarity.** For local A, ω_{N_k}(T^{F2,N_k}_θ(A)) = ω_{N_k}(A), because the finite ground state is invariant. Then

|ω(T_θ A) − ω(A)| ≤ |(ω − ω_{N_k})(T_θ A)| + ‖T_θ A − T^{F2,N_k}_θ A‖ + |(ω_{N_k} − ω)(A)| → 0.

The first term vanishes by norm approximation of the quasi-local T_θ(A) through local observables. The second vanishes by §6, including for local A outside B(H_R).

**§4, strong continuity.**
- θ ↦ ω(A*T^{F2,N}_θ(A)) = Tr(ρ_{Λ_N} A*e^{iuH}Ae^{−iuH}) is continuous, by strong continuity and a trace-class ρ.
- The uniform approximation on every compact window then makes ω(A*T_θ(A)) continuous. Here K(Θ) is finite for every Θ, and the bound tends to 0 in N.
- ‖(U_θ − 1)π(A)Ω‖² = 2ω(A*A) − 2Re ω(A*T_θ A) → 0, and Stone's theorem gives the generator.

**§5, nonnegative generator.**
- c_N(θ) = ⟨Aψ_N, e^{iu(H−E_N)}Aψ_N⟩ has spectral measure on [0,∞) for the F2 finite ground state.
- c_{N_k} → c pointwise and boundedly, along F2's subsequence.
- Fourier tests supported in (−∞,0) pass to the limit, so H_ω ≥ 0.
- Gauge invariance is inherited, because faces and h_b are gauge invariant and the finite ground state is simple.

Topology: the operator norm on compact θ windows, for each fixed local A. This is not norm continuity in time on all of B(H) (fixture: ‖U(π/n)AU(π/n)* − A‖ = 2 for every n).

## 8. τ → τ/100 scaling (brackets [9500, 10500])

| Constant | Exact ratio |
|---|---|
| forward comparison, closed | 1953058850/194651 ≈ 10033.644 |
| forward comparison, sharp | 10033.615 |
| forward comparison, modern with 1/(1−x) | 976463275/96664 ≈ 10101.623 |
| forward comparison, modern with exact e | ≈ 10101.10 |
| reverse comparison and F2 Cauchy, closed | 15624691300/1559413 ≈ 10019.598 |
| reverse comparison and F2 Cauchy, sharp | 10019.588 |
| F1 Cauchy | same as the forward comparison, 10033.644 |
| a linear-in-τ bound (rejected) | 100 |

- Every valid form lies inside [9500, 10500].
- The modern form lies outside the stale [9900, 10100] of the `duhamel_tau_order_quadratic` semantics (contract review, D1).

## 9. Reconciliation of the recorded 0.67% difference

The two loop-1 previews were 2.549e-11 (skeptic) and 2.566e-11 (modern: 3969τ²θ²e^{127008|τ||θ|}). Both use the same face-distance sum, 168(5N+1)N⁻³ = 28N(5N+1)·|R|·3·N⁻⁴, with the same Φ, C and velocity. The ratio is exactly

modern/skeptic = e^x·(x²/2)/E(x) at x = vU = 3969/390625 ≈ 1.0067939,

which is +0.679% relative to the skeptic value and 0.675% relative to the modern one. The rounded previews give 2.566/2.549 = 1.00667, and the rounding intervals of both previews contain the exact values.

**The whole gap is the bound on the exponential remainder:**
- the modern form uses e^x − 1 − x ≤ (x²/2)e^x;
- the skeptic form uses (x²/2)/(1−x/3).

deliberation-2's attribution of part of the gap to "the face-distance sum" is not needed: the face-distance sums coincide.

The recorded reverse preview (1.485e-11) and Cauchy preview (1.0195e-10) are reproduced to their printed digits.

## 10. Fixtures in the checker (exact; `model_is_finite_graph` where relevant)

- polynomial versus exponential tail;
- on-site term misplaced into Φ;
- padding left in the Duhamel difference;
- Duhamel identity and sign, with first-order vanishing;
- an inner-family constant swapped (a validator mutation);
- an N-to-N+1 bound summed (harmonic);
- fixed versus moving vector;
- ±τ separation ≥ 8.757e-10 (AY2 gate), so a cross-coupling pair is not a boundary comparison;
- one dynamics with two states;
- the placeholder rule (the fixed freezer regex keeps `J<=28|tau| … N>=2`, which the old regex misread);
- the negation-aware phrase scan, including the NS section title.

## 11. Predicted values for the post-comparison

All values at |θ| ≤ 8, |τ| = 10⁻⁸ and both signs; exact rationals in `ba2-independent/results.json`.

| Quantity | Prediction |
|---|---|
| extra faces; owners; distances | 28N(5N+1) (616, 1344, 2352); at most 3 owners, all with max_i\|y_i\| = N; ℓ1 ≥ N−1 from e_z (11 faces attain it), ≥ N from 0 |
| per-anchor extra classes | x 17, y 13, z 5, xy 10, xz 3, yz 1, xyz 0 |
| velocities | v = 1016064\|τ\|, v′ = 592704\|τ\| per unit u (127008\|τ\| and 74088\|τ\| per unit θ) |
| forward K (inner F1, Φ) | 2.548785e-11 (any valid remainder form ≤ 2.56623e-11); margin 2.354 |
| reverse K′ (inner F2, Φ′) | 1.484692e-11 (≤ 1.49057e-11 in the modern form); margin 4.041 |
| F1 Cauchy (all M > N) | 1.019514e-10 star-charged (5.947e-11 face-charged); margin 2.452 |
| F2 Cauchy (all M > N) | 3.464281e-11 face-charged; 5.938767e-11 group-charged; 1.72043e-10 through F1 |
| τ/100 ratios | 10033.6 (forward, F1 Cauchy), 10019.6 (reverse, F2 Cauchy), 10101.1–10101.6 (modern) |
| leading coefficients | 254016τ² (forward), 148176τ² (reverse), 1016064τ² (F1 Cauchy, star), 345744τ² (F2 Cauchy, face) |

A producer constant below the sharp value for its stated inner family, charging and form, without a labelled refinement, is an error. So is one of the wrong τ order.

## 12. What I will require

**Both producers.**
1. Quote (51)–(52) with (40), (41), (44), (48)–(50) and (77) verbatim from the committed excerpt. Name F, C and ‖Φ‖. Map NS t to u = θ/8 and NS τ_t^Λ to T. Cite Theorem 4.1 as Section 4, never by its title.
2. The placement of §1: H_x = h_x in (44), and Φ bounded. State which interaction the inner evolution natively restricts (F1: Φ on Λ_N; F2: Φ′ on unpadded Λ_N). Derive the exact padding factorization.
3. State the monotonicity in C and ‖Φ‖ wherever an upper bound is substituted.
4. Derive the Duhamel identity with bounded ΔH, strongly, and with its sign. Give the reason the first order vanishes.
5. The source: enumeration on Λ₂ and Λ₃ (Λ₄ welcome) plus the all-size class argument (17/13/5/10/3/1/0), each face once, and distances N−1 and N.
6. The explicit coefficient with its tier (`polynomial_lieb_robinson`), its route (`duhamel_inner_f1` or `duhamel_inner_f2`) and its inner family. Evaluate it at both signs and state the margin.
7. Cauchy estimates over all M > N, for F1 and F2, at rate 1/(N−1), with the charging named (star, face or group, never twice).
8. Identification of the F2 limit with T_θ on every local A, not only on B(H_R). Rerun AQ1 §§4–5 with F2's own extraction and the F2 reset bounds.
9. τ/100 ratios against [9500, 10500].
10. The fixtures of required item 6. The template quoted once. The gate fields with `dynamics_level` and a non-empty `whole_sequence_scope`. `gns_dynamics_equality_claimed`, `common_limit_claimed`, `state_convergence_claimed`, `uniform_in_time_claimed` and `rate_in_a_claimed` all false. Sub-label `dynamics_on_compact_windows`. Uniformity stated "in N at fixed spacing".
11. Disclosure of private scratch folders and name-only exposures.

**Forward.** Inner F1 with Φ (2268|τ|). The F2 Cauchy estimate may use Φ′ or the triangle through F1 (labelled; margin 1.45).

**Reverse.**
- Inner F2 with Φ′ (1323|τ|), re-derived for the unpadded Λ_N.
- Each family against its own NS limit for the Cauchy estimates.
- If it uses the padded anchor-grouped Ψ_N (2268|τ|) instead, it must say so.
- Inputs exactly the 29 recorded files.

## 13. Producer-error checklist

1. (51) paraphrased, or quoted from AQ1 or another report; a constant re-derived instead of quoted; (53) used with the polynomial F.
2. h_x inside Φ; a bounded LR bound applied to the full Hamiltonian; the padding terms in ΔH or in the source.
3. C ≤ 224 substituted without monotonicity; the leading term 254016τ² reported as a bound.
4. Φ′ constants for an inner F1 evolution, or Φ constants for an inner F2 evolution, without the Ψ_N statement.
5. 7|τ| outgoing-only; 21 faces per site or the literal 84; distance N instead of N−1, or N−1 used for 0.
6. An N-to-N+1 bound presented as Cauchy; an exponential rate in N; a rate or uniformity in a; a conversion to fm.
7. A window in u labelled θ (the eightfold error: U = 8 gives K ≈ 1.6707e-9, U = 1/8 gives 3.97e-13); a uniform-in-time claim; norm continuity in time on all of B(H).
8. F2 identification on B(H_R) only; §§4–5 assumed; AQ1's subsequence reused for F2; equality of GNS dynamics, correlation functions or states claimed; "the AQ state" or "the thermodynamic limit" used affirmatively.
9. A +τ/−τ pair presented as a boundary comparison.
10. Floats in admission; √N combination; a bracket chosen after evaluation.

No result here is a Round33 finding, a loop, or a fraction of the continuum problem. The four-dimensional Yang–Mills existence and mass-gap problem remains open.
