# BB2 independent derivation before producer comparison

**Standing.** I wrote this after the BB2 contract froze (`frozen_at` 2026-09-24T23:36:46.617Z, sha256 `ed5c0b24…ad35`), together with BB1 (sha256 `30400d2e…5018`, which supplies the hypotheses), and before reading any BB1 or BB2 producer.

**Isolation.**
- I did not open, list or read `research/round33/{forward,reverse}/{bb1,bb2}/`.
- The one exception: I ran `find` on the two BB2 `inputs/` folders and hashed the snapshots against the repository. Each holds 38 files, all identical to the repository, and both hold the frozen BB1 bytes.
- Git commands:
  - one early unrestricted `git status --short` printed nothing, because the tree was clean at that moment;
  - `git log --oneline` printed commit messages only;
  - `git show --stat` and `git show` were restricted to `advisor/` and `contracts/`.

  No producer file name was displayed.
- I read nothing in any other agent's folder.

**Sources.**
- The frozen BB2 and BB1 contracts, `advisor/selection-bb2.md` and `advisor/plan.json`.
- `experts/modern/bb-targets-proposal.md` and `advisor/deliberation-2.md` (advisor-only previews).
- My `bb-contract-review.md`/`.json`, triage, loop-2 review and BA2 package (for format).
- The premises:
  - BA1 and BA2 gates and reports, and my `ba1.md` and `ba2.md`;
  - AQ1 report and gate; AQ2 report and gate;
  - AV1 §§7–8 (F20–F24); the AY1, AY2 and AW1 gates;
  - the committed Nachtergaele–Sims excerpt (through BA2).

**Scratch.** `/tmp/claude-0/skeptic-bb2-private/`. It is not evidence and not a premise.

**Correlated ancestry.**
- My triage proposed the Cauchy route and the translation item.
- My BB pre-freeze review wrote the frozen targets, brackets and conditional semantics.
- What follows is a re-derivation in fresh code, not independent discovery or human review.

**Exactness.** Exact values come from `bb2_check.py`:
- 81 checks, of which 38 are controls (the 34 contract ids plus 4 extras) with 142 damaging mutations;
- byte-identical results under `python3 -B` and `-B -O`, and under two hash seeds;
- 18 source edits to a private copy each make the run fail.

Every decimal below is a preview of an exact rational or a directed enclosure. Human project author: Hruday N M (BUNZEEY).

## 1. Model and what BB2 proves

**Model.**
- Zero-selected patterned family (`AQ_patterned_zero_selected`), both signs |τ| ≤ 10⁻⁸.
- F1 = AQ1 centered whole-star boxes, and F2 = I1 §6 all-contained-face boxes with padding, both on Λ_N = [−N,N]³ with N ≥ 2.
- ρ^{F,N}_Y is the reduced density on a finite complete-factor region Y ⊂ Λ_N of the normalized untruncated finite-box ground vector (for F2, ψ^(2)_N ⊗ Ω_pad). The norm is the trace norm on B(H_Y), and R = {0, e_z}.
- Metrics: coarse ℓ∞ for states; ℓ1 with F(r) = (1+r)⁻⁴ for dynamics.

**Hypotheses H(C_h, c_h)** (the BB1 frozen targets). For every BB1 comparison, both signs, each Q_L and at fixed N for the untruncated vectors, with N the smaller box size:

  ‖ρ^{b1}_R − ρ^{b2}_R‖₁ ≤ C_h q^(N−1),  ‖ρ^{b1}_Y − ρ^{b2}_Y‖₁ ≤ c_h |Y| e^{|Y|/10⁸} q^{d_Y},  d_Y = N − max_{y∈Y}|y|_∞,

with q = 1/64, C_h = 1/250000 and c_h = 1/500000. The secondary pair is q₂ = 151552|τ| = 592/390625, C_2h = 1/20000 and c_2h = 1/40000.

The comparisons are:
- c1: F1 on Λ_N against Λ_{N+1};
- c2: F2 on Λ_N against Λ_{N+1};
- c3: F1 against F2 on the same Λ_N;
- c4: any two centered boxes Λ_M, Λ_{M′} with M, M′ ≥ N, compared directly;
- c5: two complete-factor volumes of one prescription, both containing Λ_N, compared directly.

**BB2 proves an implication**, H ⇒ items 1–5, with each constant an explicit nondecreasing function of (C_h, c_h) and of the BA2 gate constants. It becomes unconditional only through the discharge protocol (§11).

## 2. Item 1: whole-sequence Cauchy estimates and the limit

**Forward, nested telescoping (c1 for F1, c2 for F2).** For M > N:

  ‖ρ^{F,M}_R − ρ^{F,N}_R‖₁ ≤ Σ_{k=N}^{M−1} ‖ρ^{F,k+1}_R − ρ^{F,k}_R‖₁ ≤ C_h Σ_{k=N}^{M−1} q^(k−1) = C_h q^(N−1)(1−q^(M−N))/(1−q) ≤ C_h q^(N−1)/(1−q).

The bound is uniform in M, so it bounds the sup over M > N.

On a region Y ⊂ Λ_N, step k compares Λ_k and Λ_{k+1}. Since Y ⊂ Λ_k, the exponent is d_Y(k) = k − max|y| = d_Y(N) + (k−N), and the same factor appears:

  sup_{M>N}‖ρ^{F,M}_Y − ρ^{F,N}_Y‖₁ ≤ [c_h/(1−q)] |Y| e^{|Y|/10⁸} q^{d_Y}.

**Reverse, direct comparison (c4, same family, M > N).** The same two bounds hold with factor 1.

**The constants, as functions of the hypotheses.**

| | nested telescoping | union / direct |
|---|---|---|
| C′(C_h) | C_h/(1−q) = (64/63)C_h | C_h |
| c′_site(c_h) | (64/63)c_h | c_h |
| at the hypothesis values | C′ = 4/984375 ≈ 4.0635e-6; c′_site = 2/984375 ≈ 2.0317e-6 | 1/250000; 1/500000 |
| margins (targets 1/100000, 1/200000) | 315/128 = 2.4609 each | 5/2 each |
| secondary C′₂ = C_2h/(1−q₂) | 625/12481056 ≈ 5.0076e-5; margin 390033/156250 = 2.4962 against 1/8000 | 1/20000; margin 5/2 |
| secondary c′_site,2 (no target) | 625/24962112 ≈ 2.5038e-5 | 1/40000 |

- Each map is linear with a positive coefficient, and neither constant depends on the other hypothesis constant. So each is nondecreasing in (C_h, c_h). This is checked exactly on a grid and holds symbolically.
- A packet whose C′ decreases in a hypothesis constant is rejected, even when it agrees at the hypothesis values. The fixture is [128/63, −128/63]·(C_h, c_h).
- The region form at Y = R, c_h·2·e^{2/10⁸} = C_h e^{2·10⁻⁸}, exceeds the R form by less than 10⁻¹³. The R form is the sharper statement on R.
- Interleaved telescoping F1_N ⊂ F2_N ⊂ F1_{N+1} (c3 plus cross-family c4) gives 2C_h/(1−q) ≈ 8.13e-6, margin 1.23. It is valid only as labelled.

**The limit without compactness.**
- T₁(H_Y) is a Banach space. The sup bound gives ‖ρ^{F,M}_Y − ρ^{F,M′}_Y‖₁ ≤ 2c′_site|Y|e^{|Y|/10⁸}q^{d_Y(N)} for M, M′ > N, which is a Cauchy sequence, so ρ^{F,∞}_Y exists.
- Positivity and unit trace are closed in the trace norm.
- Partial trace is trace-norm contractive, so Tr_{Y′∖Y} ρ^{F,∞}_{Y′} = ρ^{F,∞}_Y.
- ω^F_∞(A) = Tr ρ^{F,∞}_Y A for A ∈ B(H_Y) defines a locally normal state on the quasi-local algebra, by norm extension.
- ‖ρ^{F,N}_Y − ρ^{F,∞}_Y‖₁ = lim_M ‖ρ^{F,N}_Y − ρ^{F,M}_Y‖₁ ≤ c′_site|Y|e^{|Y|/10⁸}q^{d_Y}. The same holds on R with C′q^(N−1).

**Fixtures (exact).**
1. ρ_N = diag(½ + (−1)^N ε, ½ − (−1)^N ε) stays in the trace-norm ball of radius 2ε about P for every N, yet has two subsequential limits. A one-state ball is not convergence.
2. Steps of 1/(2(N+1)) tend to 0, while p_N turns between ¼ and ¾ at N = 6, 21, 60 and 166. A per-step bound is not a Cauchy estimate.
3. Geometric steps C_h q^(k−1), with any signs, give a sup over M > N of at most C_h q^(N−1)/(1−q), checked for N ≤ 7.

## 3. Cutoff order

- The hypotheses include the untruncated regime at fixed N, so the Cauchy bounds hold for the untruncated densities directly.
- If BB1 admits only the Q_L regime, a packet can pass each bound from Q_L to the untruncated vectors at fixed N and M:
  - the vectors converge by Eckart, 1 − |⟨ψ, ψ_L⟩|² ≤ 2(E_L − E_0) with the untruncated gap ½ (AV1 F22), for F1 boxes;
  - for F2 boxes the AY1 itemization does the same;
  - partial trace is contractive, and a closed trace-norm ball contains the limit.
- Then N → ∞.
- The fixture pairs (8/9, 20/9), (5/9, 8/9) and (0, 0) satisfy the Eckart form. Without the gap, a ground-energy vector can be orthogonal to the ground state.
- a_{N,L} = [L ≥ N] has lim_N lim_L = 1 and lim_L lim_N = 0.
- The order is part of the statement. Under uniform-in-L bounds the exchange would be valid (Moore–Osgood), but it is neither used nor claimed.

## 4. Item 2: common limit

By c3 at the same N and item 1 for both families:

  ‖ρ^{F1,∞}_Y − ρ^{F2,∞}_Y‖₁ ≤ (2c′_site + c_h)|Y| e^{|Y|/10⁸} q^{d_Y(N)} for every N ≥ max|y|_∞, hence 0.

On R the bound is (2C′ + C_h)q^(N−1): 1.8948e-7 at N = 2, 2.9607e-9 at N = 3 and 4.6261e-11 at N = 4.

Write ω_∞ for the common state. It is **the limit of the named constructions**: not uniqueness of any ground state, not a statement about other boundary conditions, and not uniform in a.

## 5. Item 3: identification and inheritance

**Identification comes first.**
- AQ1 (report §2): a diagonal subsequence N_k has ρ^{F1,N_k}_F → ρ^{AQ}_F in trace norm on every finite complete-factor F. The gate describes it as locally normal, gauge invariant and stationary.
- A whole-sequence trace-norm limit equals the limit along every subsequence, so ρ^{AQ}_F = ρ^{F1,∞}_F = ρ^∞_F for every F. By norm continuity the states agree on the quasi-local algebra.
- The same argument applies to every F2 subsequential limit: AY1's own extraction, and the subsequences used in BA2's rerun of AQ1 §§4–5.
- All AQ1 and F2 subsequential limits are therefore one state, ω_∞. Their GNS triples coincide up to unitary equivalence.

**Inherited, each with its admitted scope:**
- **AQ1:** stationarity under T_θ; strong continuity of the GNS evolution; a nonnegative self-adjoint generator (and the reducing physical cyclic restriction).
- **F2 (BA2 rerun of AQ1 §§4–5):** the same three properties. These are now properties of the same state.
- **AQ2**, admitted "for the actual AQ1 centered full-Z³ subsequential state", which is now ω_∞:
  - H_phys ≥ (α/16)(I − P_Ω) with a simple vacuum on the invariant-local cyclic completion;
  - the full-GNS strengthening only as qualified in the AQ2 gate, which uses AM2's separately reviewed full-Hilbert finite gap.
  - Because of item 2, this is now also a statement about every F2 subsequential limit. That is new.
- **By identity, labelled:**
  - AV1's ‖ρ_R − P_R‖₁ ≤ D;
  - AY1/AY2: the pairwise bounds 2D and 2K₂′τ² are now 0 for the named constructions, and the two-sided first-order bracket applies to ω_∞;
  - AQ2's Wilson variance, at least 61999/250000.
- **Not inherited:** uniqueness of any ground state; statements about other boundary conditions; equality of GNS dynamics of different states (there is now one state, but no other states are addressed).
- The AY2 falsifying pair is excluded for the named constructions only.

## 6. Item 4: coarse translations

**Covariance.**
- A coarse translation v acts as the fine translation (4v_x, 2v_y, v_z). It maps factor blocks to blocks and keeps the owner type of every face. This is checked face by face for five coarse shifts.
- So the prescription-F Hamiltonian on Λ_N + v is U_v H_{Λ_N} U_v*.
- The finite ground state is simple (AM2; AY1 for F2), so ρ^{Λ_N+v}_{Y+v} = U_v ρ^{Λ_N}_Y U_v*.

**The quantitative bound.**
- Λ_{N−|v|} is the largest centered cube inside Λ_N ∩ (Λ_N + v). This is enumerated for N ≤ 5 and |v|_∞ ≤ 2, and it is not contained one size larger.
- The direct c5 comparison of the two one-prescription volumes Λ_N + v and Λ_N gives

  ‖ρ^{Λ_N+v}_R − ρ^{Λ_N}_R‖₁ ≤ C_h q^(N−|v|_∞−1),  N ≥ |v|_∞ + 2.

- Values: 1/16000000 at (|v|,N) = (1,3); 1/65536000000 at (1,5); 1/16000000 at (2,4); 1/17179869184000000 at (3,10).
- Through the union U = Λ_N ∪ (Λ_N+v), in two steps, the bound is C_h q^(N−|v|−1)(1 + q^{|v|}), with factor 65/64, 4097/4096 or 262145/262144 for |v| = 1, 2, 3. That is above the frozen constant, so it is labelled only.

**Invariance of ω_∞.** For A ∈ B(H_Y):
- ω_∞(α_v A) = lim_N ω^{Λ_N}(α_v A) = lim_N ω^{Λ_N−v}(A), using item 1 on Y+v and covariance.
- |ω^{Λ_N−v}(A) − ω^{Λ_N}(A)| ≤ c_h|Y|e^{|Y|/10⁸}q^{d_Y(N−|v|)}‖A‖ → 0, by the c5 region form with Λ_{N−|v|} inside both volumes.
- Hence ω_∞ ∘ α_v = ω_∞. This needs the region forms of c5 and of item 1.
- With the R forms only, one gets covariance on translates of R (ρ^{Λ_N}_{R+v} → U_v ρ^∞_R U_v*), not invariance of a state.
- Nested centered cubes alone never compare Λ_N + v with Λ_N.

**Non-coarse counter-fixture.**
- The fine shifts (1,0,0), (2,0,0), (3,0,0), (0,1,0) and (1,1,0) map no factor block onto a block and change face classes. For example, the selected xy face at r = 2 becomes the omitted type {0, e_x} at r = 3.
- **Pitfall found:** the per-anchor histogram of the 24 owner types (3, 10, 4, 3, 2, 1, 1) is unchanged by every fine shift, because the translated faces of one anchor reassemble the same multiset. A histogram-level residue check therefore accepts non-coarse translations. The face-by-face map is required.

## 7. Scaling (τ → τ/100)

| Constant | Exact ratio | Bracket |
|---|---|---|
| C′, c′_site (both assemblies) | exactly 1 | exactly 1 |
| secondary C′₂, telescoped | 1085053/1083425 ≈ 1.0015026 | [99/100, 101/100] |
| secondary, union | exactly 1 | [99/100, 101/100] |
| q₂ | exactly 100 | exactly 100 |
| C_dyn, inner F1 (forward closed form) | 1953058850/194651 ≈ 10033.644 | [9500, 10500] |
| C_dyn, inner F2 (reverse E_up form) | 38176688920663121234473000000/3810205403940325763421973 ≈ 10019.588 | [9500, 10500] |
| C_dyn, with the whole-star K_c1′ | ≈ 10033.619 | [9500, 10500] |

A C′ ratio near 100 (for example 4340004/43129, BA1's) would mean that BB1 formulas were used, which is forbidden. The linear scaling of the underlying BB1 constants is recorded at the discharge.

## 8. Item 5: correlation functions on |θ| ≤ 8

**Decomposition.** Fix F, N ≥ 5, r = r_N = ⌊(N−1)/2⌋ ≥ 2, and A ∈ B(H_R). Write:
- B_N = T^{F,N}_θ(A) (for F2, padded: T^{F2,N}(A) ⊗ 1);
- B_∞ = T_θ(A);
- B_r, a Λ_r box evolution (T^{F1,r}_θ(A) or T^{F2,r}_θ(A)), so that A*B_r ∈ B(H_{Λ_r}).

Then:

  ω^{F,N}(A*B_N) − ω_∞(A*B_∞) = ω^{F,N}(A*(B_N−B_r)) + (ω^{F,N}−ω_∞)(A*B_r) + ω_∞(A*(B_r−B_∞)),

  | |ω^{F,N}(A)|² − |ω_∞(A)|² | ≤ (|a|+|b|)|a−b| ≤ 2‖A‖²‖ρ^{F,N}_R − ρ^∞_R‖₁ ≤ 2C′q^(N−1)‖A‖².

The middle term is at most ‖ρ^{F,N}_{Λ_r} − ρ^∞_{Λ_r}‖₁‖A‖², which is at most c′_site|Λ_r|e^{|Λ_r|/10⁸}q^{N−r}‖A‖² (item 1 with Y = Λ_r, d = N−r, and item 2). The outer terms are at most ‖A‖(‖B_N−B_r‖ + ‖B_r−B_∞‖).

**The BA2 gate constants**, parsed from the pinned gate and reproduced exactly:

| | Formula | Route | Value | τ/100 |
|---|---|---|---|---|
| K_cmp (forward) | 254016τ²/(1−338688\|τ\|) | inner F1 | 3969/155720800000000 ≈ 2.5488e-11 | 10033.644 |
| K′_cmp (reverse) | 148176τ²E_up(592704\|τ\|) | inner F2 | 452554889222515527/3048140234375·10¹⁶ ≈ 1.4847e-11 | 10019.588 |
| K_c1 (forward, face) | 592704τ²/(1−338688\|τ\|) | inner F1 | 9261/155720800000000 ≈ 5.9472e-11 | 10033.644 |
| K_c1′ (reverse, whole star) | 1016064τ²E_up(1016064\|τ\|) | inner F1 | 12128856933354903/118967041015625·10¹² ≈ 1.01951e-10 | 10033.615 |
| K_c2 (forward, through F1) | 941976τ²/(1−338688\|τ\|) = K_c1 + (11/8)K_cmp | inner F1 | 117747/1245766400000000 ≈ 9.4518e-11 | 10033.644 |
| K_c2′ (reverse, own family) | 345744τ²E_up(592704\|τ\|) | inner F2 | 1055961408185869563/3048140234375·10¹⁶ ≈ 3.4643e-11 | 10019.588 |

Here E_up(y) = 1 + y/3 + y²/(12(1−y/5)). Gate item (4) gives ‖T^{F2,N}−T‖ ≤ K_c2′/(N−1) (reading R9).

**Assemblies.** Each uses (5N+1)N⁻³ ≤ (5r+1)r⁻³ ≤ (11/8)/(r−1). That holds for r ≥ 2 with equality at r = 2, and (5N+1)N⁻³ is decreasing.

| Assembly (B_r) | C_dyn | Route | Margin |
|---|---|---|---|
| inner F2: F2 2K_c2′; F1 2K_c2′ + (11/8)K′_cmp (B_r = T^{F2,r}) | 4374697262484316761/48770243750000000000000000000 ≈ 8.9700e-11 | duhamel_inner_f2 | 5.574 |
| same-family intermediate: F1 2K_c1, F2 2K_c2′ | 9261/77860400000000 ≈ 1.1894e-10 | composite (f1 and f2) | 4.204 |
| inner F1: F1 2K_c1; F2 2K_c1 + (11/8)K_cmp (B_r = T^{F1,r}) | 38367/249153280000000 ≈ 1.5399e-10 | duhamel_inner_f1 | 3.247 |
| advisor form: F2 K_c1′ + K_c2 + (11/8)K_cmp | 175777236988465912821/759247655761718750000000000000 ≈ 2.3152e-10 | duhamel_inner_f1 | 2.160 |
| inner F1 with K_c1′: 2K_c1′ + (11/8)K_cmp (worst natural) | ≈ 2.3895e-10 | duhamel_inner_f1 | 2.092 |
| labelled refinement: (11/8) replaced by 72/343, from (5N+1)N⁻³ ≤ (10r+6)(2r+1)⁻³ and (r−1)(10r+6)(2r+1)⁻³ ≤ 72/343 | inner F1 1.2429e-10; inner F2 7.2402e-11 | as above | 4.02; 6.91 |

- Every assembly meets 1/2000000000 with a margin of at least 2.09. The C_dyn target is therefore well posed for any honest assembly.
- Floor: every assembly bounds two Cauchy-or-limit terms by admitted constants, each at least K_c2′, over (r−1). A C_dyn below 2K_c2′ = 1055961408185869563/15240701171875000000000000000 ≈ 6.9286e-11 without a labelled refinement is an error.

**The three terms (‖A‖ = 1; e^{|Λ_r|/10⁸} enclosed from above).**

| Constants | N = 5 (r = 2, 125 sites): dynamics / state / mean / sum | N = 10 (r = 4, 729 sites): sum | N = 20 (r = 9, 6859 sites): sum |
|---|---|---|---|
| telescoped C′, c′_site; C_dyn inner F1 (1.5399e-10) | 1.5399e-10 / 9.6881e-10 / 4.844e-13 / 1.1233e-9 | 5.1351e-11 (dynamics 5.1330e-11, state 2.155e-14) | 1.9249e-11 |
| union C′, c′_site; C_dyn inner F2 (8.9700e-11) | 8.9700e-11 / 9.5368e-10 / 4.768e-13 / 1.0439e-9 | 2.9921e-11 | 1.1213e-11 |
| telescoped; worst natural C_dyn (2.3895e-10) | 2.3895e-10 / 9.6881e-10 / 4.844e-13 / 1.2082e-9 | 7.9671e-11 | 2.9869e-11 |
| at the targets (1/100000, 1/200000, 1/2000000000) | 5.0e-10 / 2.3842e-9 / 1.192e-12 / 2.8854e-9 | 1.6672e-10 | 6.2500e-11 |

- At N = 5 the state term (125 sites, q³) exceeds the dynamics term. From N = 10 on, the O(1/N) dynamics term dominates, and the state and mean terms are 10⁻¹⁴ or smaller.
- The three constants are kept separate. No single bracket covers the sum.
- The rate is O(1/N), because r_N − 1 ≥ (N−4)/2 with the polynomial F. There is no exponential claim, no uniform-in-time claim, and no equality of GNS dynamics of different states.

**Centering fixture (exact Gaussian rationals).**
- Take ρ = [[½, (1+i)/4], [(1−i)/4, ½]] (det ⅛ > 0) and A = σ₊.
- ω(A) = (1−i)/4 and |ω(A)|² = ⅛, so c_A(0) = ω(A*A) − |ω(A)|² = ⅜, a variance.
- Centering with ω(A)² gives ½ + i/8, which is complex. Centering with (Re ω(A))² gives 7/16.
- The mean term obeys (|a|² − |b|²)² ≤ 4‖A‖²|a−b|².

## 9. Other fixtures in the checker

- **Cross-coupling.** The +τ and −τ limits differ on R by at least 8.757e-10 (AY2 gate). Used as a BB1 comparison, the pair would need (2C′+C_h)q^(N−1) ≥ 8.757e-10, which fails from N = 4.
- **Polynomial tail.** The shell tail of F from distance k is at least 1/(4k), so no exponential rate follows from these constants.
- **Fixed against moving vector.** ‖U(π/n)AU(π/n)* − A‖ = 2 for every n, while U(t)e₁ → e₁. The topologies are trace norm for states, norm on compact windows per fixed A for dynamics, and GNS strong for representations.

## 10. Readings and defects

These are listed in `bb2-contract-review.md`: readings R1–R13 and defects D1–D11, none blocking. The two with consequences for the numbers:
- **R1/D2.** A literal union route misses the item-4 constant by the factor 1+q^{|v|}.
- **R2/D3.** C_dyn is assembly-dependent (8.970e-11 to 2.389e-10), and "exactly one route" is ill-posed for a composite.

## 11. Discharge protocol (summary; the full table is in the contract review)

- An item becomes unconditional when, at both signs, at least one route proves it from BB1 instances (comparison, form, regime) that the BB1 gate admits at q = 1/64 with:
  - a bound dominated pointwise by the hypothesis form: same q, exponent shift ≥ 0, |Y| power ≤ 1, e-rate ≤ 10⁻⁸;
  - a constant at most C_h or c_h.
- Validity follows from dominance (the admitted statement implies the hypothesis instance) together with monotonicity (the constants re-evaluated at the admitted values are no larger).
- A constant above the hypothesis value leaves the item conditional; any re-evaluation is labelled only.

The engine in `bb2_check.py` runs twelve labelled synthetic BB1 outcomes (none of them BB1 results):

| Synthetic outcome | Items 1 / 2 / 3 / 4 / 5 | Verdict |
|---|---|---|
| S1 accepted, at the advisor split preview (C = 1.75396e-6, C/2 per site) | full ×5; re-evaluated C′ = 1.78180e-6 (telescoped) or 1.75396e-6 (union); c′_site = 8.9090e-7 or 8.7698e-7 | accepted_within_scope |
| S2 region form missing | R only / R only / R-marginals / R-translate covariance / dropped | limited |
| S3 c5 missing | full / full / full / dropped / full | limited |
| S4 BB1 insufficient | conditional ×5 | insufficient |
| S5 c3 above the hypothesis (1/200000) | full / conditional / per family / full / per family | limited |
| S6 Q_L only | full ×5 through the forward (own cutoff removal) | accepted_within_scope |
| S7 +τ only | full at +τ; conditional at −τ | limited |
| S8 c4 missing | full ×5 through the forward | accepted_within_scope (pairing limitation recorded) |
| S9 admitted = hypothesis | full ×5 | accepted_within_scope |
| S10 sharper exponent q^N | full ×5 | accepted_within_scope |
| S11 region factor \|Y\|² | as S2 | limited |
| S12 region form at q = 1/32 | as S2 | limited |

## 12. Predicted values for the post-comparison

All values are at |τ| = 10⁻⁸, both signs, |θ| ≤ 8, and at the hypothesis values. The exact rationals are in `bb2-independent/results.json`.

| Quantity | Forward (nested telescoping) | Reverse (union comparison) |
|---|---|---|
| C′ | 4/984375 ≈ 4.0635e-6 (margin 2.4609) | 1/250000 (margin 2.5) |
| c′_site | 2/984375 ≈ 2.0317e-6 (margin 2.4609) | 1/500000 (margin 2.5) |
| C′₂ (secondary) | 625/12481056 ≈ 5.0076e-5 (margin 2.4962) | 1/20000 (margin 2.5) |
| τ/100 | exactly 1; secondary 1085053/1083425 | exactly 1; secondary 1 |
| labels | exact_first_order, nested_telescoping, bb1_frozen_targets | exact_first_order, union_comparison, bb1_frozen_targets |
| item 4 | C_h q^(N−\|v\|−1), direct c5 through Λ_{N−\|v\|} | the same; the literal union two-step is labelled (65/64 at \|v\| = 1) |
| C_dyn (likely) | inner F1, 1.5399e-10 (margin 3.25); or 2.3152e-10 or 2.3895e-10 with whole-star constants | inner F2, 8.9700e-11 (margin 5.57) |
| item-5 sums at N = 5, 10, 20 | 1.1233e-9, 5.1351e-11, 1.9249e-11 | 1.0439e-9, 2.9921e-11, 1.1213e-11 |

The following are errors unless labelled as refinements:
- a C′ below 4/984375 (telescoping) or below 1/250000 (union);
- a C_dyn below 6.9286e-11;
- any τ ratio other than 1 for C′ or c′_site.

## 13. What I will require

**Both producers.**
1. Each state constant as an explicit function of (C_h, c_h), nondecreasing, checked exactly, and evaluated only at the frozen hypothesis values. No BB1 file may be read.
2. The Cauchy estimate over all M > N, on R and on every Y ⊂ Λ_N, with |Y|, e^{|Y|/10⁸} and d_Y explicit. The limit from completeness of T₁(H_Y), not from compactness. The words "whole sequence".
3. Cutoff: the bounds in each Q_L uniformly in L, then the untruncated vectors at fixed N (hypothesis, or AV1 F20–F23 and AY1), then N → ∞.
4. Item 2 through c3, named "the limit of the named constructions".
5. Item 3: identification with every AQ1 and every F2 subsequential limit before any inheritance, with the AQ2 scope as in §5.
6. Item 4 as its own item: the c5 input stated as BB1's density comparison (not BA1's coefficient comparison), Λ_{N−|v|}, N ≥ |v|+2, and a face-by-face non-coarse rejection.
7. Item 5:
   - r_N = ⌊(N−1)/2⌋ and N ≥ 5;
   - complex-mean centering;
   - the three constants separate;
   - C_dyn with its assembly, each component's exact BA2 gate value and route;
   - the rate O(1/N);
   - |θ| ≤ 8 with U = 1.
8. The template once, inside the frame at a limited verdict. The gate fields exported as conditional on the BB1 discharge. The error terms itemized. The fixtures of required item 6. Private scratch folders and any name-only exposures disclosed.

**Forward.** Nested telescoping through c1 and c2, with the factor 64/63 and cutoff removal at fixed N named.

**Reverse.**
- A direct comparison through c4 and c5 with factor 1. If it passes through a union in two steps, it must say so and label the factor.
- Inputs exactly the 38 recorded files.

## 14. Producer-error checklist

1. A BB1 value other than the frozen targets (a preview, or a value "expected" from BB1); the condition dropped; "unconditional", or gate fields exported as unconditional before the discharge.
2. A C′ τ-ratio near 100; a lumped item-5 bracket; a Lieb–Robinson tier on a state constant; a BB1 route claimed.
3. An N → N+1 bound presented as Cauchy; compactness plus closeness; "subsequence" limits called whole-sequence.
4. C′ reused on Λ_{r_N}; d_Y = N−1 for every Y; the |Y| factor dropped.
5. Inheritance before identification; the AQ2 gap claimed in the full GNS space without the qualification; uniqueness inherited.
6. Item 4 from nested cubes, or from BA1's coefficient comparison; a non-coarse translation accepted; the histogram-only residue check; the union two-step used as the frozen bound.
7. ω(A)² or (Re ω(A))² centering; r_N chosen after evaluation; an exponential rate in N; a window in u labelled θ; uniform-in-time or GNS-dynamics-equality claims.
8. A +τ/−τ pair used as a comparison; floats in admission; a √N combination; "the thermodynamic limit", "the infinite-volume ground state" or "a unique limit" used affirmatively.

No result here is a Round33 finding, a loop, or a fraction of the continuum problem. The four-dimensional Yang–Mills existence and mass-gap problem remains open.
