# AY1 independent derivation before producer comparison

**Standing.** I wrote this after the AY1 contract froze (`frozen_at` 2026-09-24T02:11:14Z, sha256 `be9b3544…79ae0`). I have not opened, listed or read `research/round32/forward/ay1/` or `research/round32/reverse/ay1/`.

**Sources.** I worked from:
- the frozen contract, `selection-ay1.md`, `panel-update-3.md` and `plan.json`;
- the six Round32 gates;
- the AV1 and AW1 forward and reverse reports, and my own `av1.md`, `aw1.md`, triage, prospective controls, loop-2 and loop-3 notes, and AX1 package (for format);
- the Jung loop-2 response and the three lens `update-3.md` notes;
- AM2 forward, AM2 skeptic and the AM2 gate; AQ1 and AQ2 forward; I1 forward (§3–6); AGENTS.md.

I did not use the AM2 reverse report or AT4 forward, although both are declared premises.

**Scratch.** All scratch work stayed in the private folder `/tmp/claude-0/skeptic-ay1-private/`. I read nothing in other agents' scratch folders or in the shared scratchpad root.

**Disclosure.** Early on, one recursive `grep` over `research/round32` (for "moving vector", "fixed vector" and "enclosing interval") did not exclude the two AY1 producer folders. The command piped its output through `grep -v "forward/ay1\|reverse/ay1"`, so no line from those paths was displayed to me, and I do not know whether they existed at that time. Every later search excluded them.

**Correlated ancestry.** I am a model-agent skeptic with correlated ancestry. My triage seeded the 2D observation and controls 13–17, and my AV1 and AW1 reviews are shared premises, so this is re-derivation, not independent discovery or human review.

**Exactness.** Exact values come from `ay1_check.py`: 96 checks, of which 26 are controls (the 21 contract ids plus 5 extra) with 70 rejected mutations. Every decimal below is a preview. Human project author: Hruday N M (BUNZEEY).

## 1. Model and the AV1 premises being verified
**Model.** Zero-selected patterned family:
- SU(2) Kogut–Susskind form on Z³ at fixed spacing, with 24-link coarse factors;
- selected triple `(0,0,0)`, so `h_b = 8ΣC_e ≥ 6Q_b` with the Haar vacuum;
- 21 omitted faces per anchor, each entering as `−(τ/3)W_f` (I1.5), with `a := |τ|/144` the per-face first-order norm;
- both signs, `|τ| ≤ 10⁻⁸`;
- cover `R = {0,e_z}` (48 links, 36 endpoints: 22 per factor, 8 shared).

**The premises the AV1 lemma uses**, which each family must meet:

| Premise | Content |
|---|---|
| P1 | Interaction groups with support `|X| ≤ 4` and per-site sum `J ≤ J_0 = 7/25000000`; AM2 fixed point, uniqueness and gap `1/2` |
| P2 | The untruncated gap, for cutoff-vector removal (AV1 §7) |
| P3 | At most 49 faces with owner set containing any site, so `||c^(1)||_a ≤ t_1 = 49a` |
| P4 | Reset budget on every finite F, giving local trace-norm compactness and diagonal extraction |
| P5 | Haar reference `P_R` |
| P6 | Every creation meeting R is counted, straddling ones included |

Given P1–P6, tier (ii) gives `||ρ_{N,R} − P_R||_1 ≤ D` with the gate rational `D = 585079838465912592144137406066050/42981220507576537932303142777593983768257` (≈ 1.361245e-8). The checker reproduces `D` exactly from `T = 49/14398580736`, `ρ = 352JT = 3773/11248891200000000` and `ε = 2T+T²`.

## 2. Family F1: AQ1 centered whole-star boxes
The admitted chain applies unchanged: the AM2 gate, AQ1 and AQ2, and the AV1 and AW1 gates. The checker confirms the following for N = 1, 2, 3:
- each site has at most 4 groups, per-site sum at most 28|τ|, at most 49 faces and support at most 4;
- `21(2N)³` retained faces;
- for N ≥ 2, the seven full stars meet R and carry 82 faces meeting R. At N = 1 only four stars meet R, with 49 faces.

## 3. Family F2: I1 §6 all-contained-face boxes with padding, itemized
**Definition.** On `B = Λ_N = [−N,N]³`, for each `b ∈ B` let `φ_b^{(B)} = −(τ/3) Σ W_f` over the omitted faces anchored at b whose actual owner set (I1.4) lies in B. A face anchored outside B always has its anchor in its owner set, so it is never retained. Pad to `B_+ = ∪_b(b+S)`; each padded site carries `h_b` only. The ground state on `B_+` is `ψ_B ⊗ Ω_pad`, so `ρ_R` is the same with or without padding. Padding places the operator in the source empty-boundary form. AM2 does not need it.

**The checks, one by one:**
- **Support.** `supp φ_b^{(B)} ⊂ b+S`, so `|X| ≤ 4`. The nested commutator terminates at order `2p = 8`, and AM2's majorant `L_k^num = 16·8^k(1+5k/4)` uses only `|X| ≤ 4`.
- **Per-site sum.** `J(u) = Σ_{b∈u−S} ||φ_b^{(B)}|| ≤ 4·7|τ| = 28|τ|`, with equality at bulk sites. Brute force on N = 1, 2, 3 never exceeds 28, and incoming groups are always counted. The contraction at the **same** `J_0` is therefore `J_0G(R) < 37/6250000 < 1/64` and `2J_0G'(R) < 77/390625 < 1`, with `e^{1/8} < 8/7`, `G(R) < 148/7` and `G'(R) < 352`. At the cap this holds with equality `J = J_0`, which AM2 allows.
  - **Labelled alternative.** Group by owner set instead: `J = 49|τ|/3`, support ≤ 3. This is F2's native Nachtergaele–Sims restriction `Σ_{X⊂Λ}Φ'(X)`, with crude `||Φ'||_F ≤ 81·49|τ|/3 = 1323|τ|`.
- **Grouping.** Each retained face lies in exactly one anchor group, and incoming groups are counted. This meets the AM2 gate's limitation "complete interaction grouping essential" and the AGENTS.md rule that a changed support decomposition changes the budget: the budget was recomputed and did not change.
- **Ground, gap, cutoff.** Unique gauge-invariant ground, full-space gap `≥ 1/2` normalized (`α/16` physical), and AM2 §6 cutoff removal all hold: compressions keep supports and do not raise J. AV1 §7 (Eckart plus Rayleigh) then removes the cutoff from the ground **vector**.
- **Reset.** Resetting F to `P_F` with the exterior marginal kept changes every incident group by at most `2·7|τ|`. At most `4|F|` groups meet F, so `C_F = 56|τ||F|`. On R the seven full groups give **`98|τ|`**, the same as F1; the labelled face-level refinement is `2·82/3 = 164|τ|/3`. With the Haar gap six, `ε_R ≤ 49|τ|/3`, and AQ2's `2√(98|τ|) ≤ 1/500` holds.
- **Compactness.** `Tr ρ_{N,F}(1−Q_{F,L}) ≤ C_F/L` and `||ρ − QρQ||_1 ≤ 2√(C_F/L)`, followed by diagonal extraction, exactly as in AQ1 §2. F2 needs its **own** extraction: the F2 limits are not AQ1's chosen state.
- **AV1 premises.** Per-site face counts are at most 49 and `J ≤ 28|τ|`, so `T` and `ε` are unchanged and **the same D bounds every F2 box** and every F2 subsequential limit.

**Counts.** Let `m = 2N`. F2 retains `14m(m+1)² + 7m²(m+1)` faces, so F2 minus F1 is `28N(5N+1)` faces (168, 616 and 1344 for N = 1, 2, 3). The nearest extra face has owner set at ℓ∞ distance **N−1** from R.

| N | F1 faces meeting R | F2 faces meeting R | faces inside R (both) |
|---|---|---|---|
| 1 | 49 | 60 | 10 |
| 2, 3 | 82, identical sets and the same 7 full groups | 82 | 10 |

## 4. Topologies and clock
- **States:** trace norm on `B(H_R)`, `||ρ−ρ'||_1 = sup_{||A||≤1, A∈B(H_R)} |ω(A)−ω'(A)|`.
- **Dynamics:** for each fixed bounded local A, norm convergence of `τ_θ^N(A)` uniformly on compact windows of `θ = αt/ħ` (Nachtergaele–Sims). This is **not** uniform over the unit ball of the full local `B(H)`.
- **Clock:** `s = αt_E/ħ`, `θ = αt/ħ`, `G = H/α`. AQ1's `u = δt/ħ = θ/8` must be converted before it enters any packet.
- **Dynamics per family:** F1 has star-indexed Φ and F2 has owner-set-indexed Φ′. AY1 does not claim that the two limits coincide (`boundary_independence_of_dynamics_claimed:false`), and the closeness bound does not use dynamics.

## 5. The pair constant 2D
For subsequential limits ω, ω′ of F1 or F2 (same or different family) at the same τ, the triangle inequality through `P_R` gives `||ρ_R−ρ'_R||_1 ≤ 2D`.

**Value.** `2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257` ≈ 2.722491e-8. This meets `1/1250000` with margin **29.3849**. Tier (i) gives `2D_i` ≈ 4.7361e-5, which fails and is retained. The scaling ratio `D(τ)/D(τ/100)` is 100.0098, so the bound is linear.

**Caveat.** `P_R` does not depend on τ, so the same bound holds between couplings τ and τ′ (checked at τ/7). 2D is a common enclosing ball, not a boundary comparison. The √2 root-sum-square combination and "D" alone are both wrong constants.

## 6. First-order reduced density ρ^(1)_R
**Forward route (explicit marginal).**
- The AV1 convention is `ψ = e^{−C}Ω_0` with `c^(1) = L_0 = −(τ/72)Σ_f W_fΩ_0`. So `ψ = Ω_0 − c^(1) + O(τ²)` and `ρ^(1) = −(c^(1)Ω_0* + h.c.)`.
- Take `Tr_{R^c}`. A face whose link set contains a link owned outside R leaves that link's Haar integral `∫U dU = 0` (it occurs once), so its term vanishes.
- Recount the whole-star creations meeting R from the seven incident anchors R−S:

| Anchor | 0 | e_z | −e_z | −e_x | −e_y | e_z−e_x | e_z−e_y | total |
|---|---|---|---|---|---|---|---|---|
| Faces meeting R | 21 | 21 | 16 | 4 | 8 | 4 | 8 | **82** (27 owner sets) |
| Survive `Tr_{R^c}` | 10 | 0 | 0 | 0 | 0 | 0 | 0 | **10** |

- The 72 straddling faces split 66 + 6 by `|I∩R|` (33 single-contact faces per site), and all of them vanish. There are no single-site creations: selected faces carry coefficient 0, unlike AX1's 16/88.
- The 10 survivors are the faces anchored at 0 with owner set `{0,e_z}`: the xz faces with `r ≤ 2` and `s = 0,1` (6), and the yz faces with `s = 0` and `r = 0..3` (4).

Hence

`ρ^(1)_R = (τ/72) Σ_{f∈F_R} ( |W_fΩ_R⟩⟨Ω_R| + |Ω_R⟩⟨W_fΩ_R| )`, `|F_R| = 10`.

**Properties.**
- The face vectors are orthogonal with norm 1/2. The checker verifies this for all 82·81 ordered pairs.
- `x = (τ/72)ΣW_fΩ_R` has `||x|| = √10|τ|/144`. The operator is rank two, with eigenvalues ±||x||, so `||ρ^(1)_R||_1 = √10|τ|/72`. At the cap this is ≈ 4.3920523058e-10, with directed bracket [395284707521/(9·10²⁰), 3162277660169/(7.2·10²¹)]. The triangle bound is `5|τ|/36`.
- `Tr ρ^(1) = P_Rρ^(1)P_R = Q_Rρ^(1)Q_R = 0`, since `E[W_f] = 0` for all 82 faces.
- `Tr(ρ^(1)W) = 2(τ/72)E[W²] = +τ/144`, which is AW1's coefficient: only f = W contributes. `Tr(ρ^(1)W²) = 0`, the AW1 parity result.
- Every face is odd under the AW1 flip set, so `U_{E∩R}ρ^(1)(τ)U* = −ρ^(1)(τ) = ρ^(1)(−τ)`.
- The wrong sign `−(τ/72)`, as displayed in the modern lens's update-3, gives −τ/144.

**Reverse route (overlap derivative, finite boxes).** Use AV1 (R06–R09) with `n = ||φ_out||`:
- The `P_R` block, `Tr(ρ_R P_R) = 1/(1+e²) = 1−O(τ²)`, has zero derivative.
- The `Q_R` block `σ/n²` is positive with trace `e²/(1+e²) = O(τ²)`, so it vanishes at first order.
- For `v ⊥ Ω_R`, the off-diagonal block `⟨v|ρ_R|Ω_R⟩ = ⟨v⊗φ_out, δ⟩/(n²(1+e²))` has derivative `−⟨v, c^(1)_R⟩`. Straddling creations enter it only at second order, because `(Q_uφ_out)` has relative size ≤ T (AW1 F14).

The result is the same operator.

**Family independence.** The 10 faces are retained by F1 and F2 for every N ≥ 1 (checked for N = 1, 2, 3). With the uniform remainder of §7, every subsequential limit of either family has the same first-order term. A τ-derivative of a subsequential limit is never taken.

## 7. Second-order difference: R-local trace-norm K_2′
**Setup.** In AV1 notation, `ρ_R = [P_R + (|ξ̂⟩⟨Ω_R| + h.c.) + σ̂]/(1+e²)`, with:
- `ξ̂ = (1⊗⟨φ_out|)δ/n²`;
- `σ̂ = Tr_out|δ⟩⟨δ|/n²`, with `Tr σ̂ = e²`.

Write `ξ̂ = −c + y`, where `c = c^(1)_{{0,e_z}}`, `||c|| = √10 a`, and y has three parts:
- `y_1 = −Σ_{I⊂R}(c−c^(1))_I`, the inside-R remainder;
- `y_2 = −Σ_{I straddling}(1⊗⟨φ_out|)ĉ_Iψ_out/n²`;
- `y_3 = +Σ_{pairs}(1⊗⟨φ_out|)ĉ_Iĉ_Jψ_out/n²`.

**Identity.** Then, exactly,

`ρ_R − P_R − ρ^(1)_R = [ (|y⟩⟨Ω_R| + h.c.) + e²(|c⟩⟨Ω_R| + h.c.) + σ̂ − e²P_R ] / (1+e²)`,

so `||ρ_R−P_R−ρ^(1)_R||_1 ≤ 2||y|| + 2e²||c|| + 2e²`. Here `σ̂` and `P_R` have orthogonal supports, which gives the `2e²`.

**Bounds on the pieces:**
- `||y_1|| ≤ 2ρ`: the anchored norm at 0 and at e_z, covering the `{0}`, `{e_z}` and `{0,e_z}` sectors.
- `||y_2|| ≤ T(72a+2ρ)`: AW1 F14, with all 72 straddling faces because the full density sees every sector.
- `||y_3|| ≤ (33a+ρ)²`.
- `e ≤ ε_R = 82a+2ρ+(33a+ρ)²`, the AW1 reverse's R-local ε.

**Items at the cap (exact in results; /τ²):**

| Item | Formula | Value |
|---|---|---|
| am2_remainder | `4ρ` | 94325000000/7030557 ≈ 13416.4334 |
| straddling | `2T(72a+2ρ)` | ≈ 0.340357 |
| two_creation | `2(33a+ρ)²` | ≈ 0.105065 |
| density | `2ε_R²` | ≈ 0.648687 |
| normalization | `2ε_R²·10a` | ≈ 4.5e-10 |
| **K_2′** | sum | **≈ 13417.5275** (exact 60-digit rational in results) |

**Comparison with K_2^+** (gate, ≈ 3354.80323, reproduced exactly as `ρ+T²+T²+ε_F²+aε_F²`):
- `K_2′/K_2^+ ≈ 3.99950`. The factor 4 has two sources. First, trace norm pays `2||y||`, where W pays only `2||WΩ_R||·||y|| = ||y||`. Second, the remainder is charged at both sites (three sectors) instead of the single `{0,e_z}` sector. The ratio falls short of 4 because the non-AM2 items are pinned R-locally.
- Every trace-norm constant from these items is at least `2ρ/τ²` ≈ 6708.217. With the sharper majorant `288t/(1−8t)` it is still at least 5488.70. Both exceed K_2^+.
- The labelled sector-orthogonal variant is `2√2ρ+…` ≈ 9487.95, which also exceeds K_2^+.
- Only the W-projected R-local analogue `ρ+T(6a+ρ)+(33a+ρ)²+ε_R²+aε_R²` ≈ 3354.49943 lies below K_2^+ (by 0.30380). That is AW1's minimal form, not a density bound.
- The AM2 majorant is 99.979% of K_2^+ and is per-site, so "R-local" cannot remove it.

**Difference and consequences:**
- The difference constant is `2K_2′τ²` ≈ 2.68351e-12, about 1.0145×10⁴ below 2D. The scaling ratio at τ/100 is 10000.98, so it is quadratic, and it is monotone in |τ|.
- **Labelled observation (not the admitted tier, not a target).** `||ρ_R−P_R||_1 ≤ √10|τ|/72 + K_2′τ²` ≈ 4.40547e-10, about 30.9 times below D. AV1's ε charges the 72 straddling faces at first order, but they enter ξ̂ only at second order.
- **±τ states.** `||ρ_R(τ)−ρ_R(−τ)||_1 ≥ 2√10|τ|/72 − 2K_2′τ²` ≈ 8.7573e-10 > 0, yet both lie within 2D. The Wilson means `ω_{±τ}(W)` are separated by at least `2(τ/144−K_2^+τ²) > 0` and both lie in [−D, D].

## 8. Fixtures
- **Fixed versus moving vector.** Let `U(t)e_j = e^{ijt}e_j` on ℓ²(N) with `t = π/n`. The moving vector gives `||U e_n − e_n||² = 4`. The fixed vector gives `||U e_1 − e_1||² ≤ (16/(5n))² → 0`. So the evolution is strongly continuous but not norm continuous: the dynamics topology is per fixed local A.
- **States analogue.** `ρ_n = (1−D/2)|e_0⟩⟨e_0| + (D/2)|e_n⟩⟨e_n|` converges on fixed observables, yet `||ρ_n−ρ_m||_1 = D` and the weak limit has mass `1−D/2`. Trace norm needs the reset tightness.
- **Common interval versus equality.** `±τ/144` both lie in [−D, D] and differ, and the in-model certified pair is the one in §7.
- **Uniform in N versus uniform in a.** D, ρ^(1) and K_2′ contain no N, but everything is at fixed spacing. Under `τ = 96/g⁴`, the cap requires `g⁴ ≥ 9.6×10⁹` and the box requires `g⁴ ≥ 32`, so every a→0, g→0 path leaves both.

## 9. What I will require of each producer
**Both producers:**
1. **F2 itemized, not by analogy.** State the definition, the padding, the per-site sum (4 incoming groups, `28|τ|`), support ≤ 4, termination 8, the two exact contraction inequalities at `J_0 = 7/25000000`, the gap, cutoff-vector removal, reset (`98|τ|` on R and `56|τ||F|`), compactness, and F2's own diagonal extraction. Show enumeration on at least two N together with an all-size argument.
2. **D.** Use D = the AV1 gate forward rational, with 2D exact and the margin reported. Retain tier (i). No AX1 D′, and no unlabelled reverse 82-face value.
3. **Two topologies and one clock,** named separately.
4. **ρ^(1)_R.** Give it with the 82→10 recount, the sign (`+τ/72` on `|W_fΩ_R⟩⟨Ω_R|`), trace norm `√10|τ|/72` as a directed bracket (a triangle bound must be labelled), and the cross-checks `Tr(ρ^(1)W) = τ/144` and `Tr(ρ^(1)W²) = 0`.
5. **K_2′.** Name its topology, sectors and multiplier; itemize it with the pins 72/33/82/10; state the sign of its comparison with K_2^+. Label a W-projected constant as such.
6. **Wording, fields and exports.**
   - The template sentence verbatim, and the five gate fields false in `results.json`.
   - The contract's definition of "quantitative boundary comparison".
   - The statement "uniform in N at fixed spacing, never in a".
   - The fixed-versus-moving-vector and common-interval fixtures.
   - The scratch-read disclosure line.

**Reverse, in addition:**
- the overlap-derivative route with the block argument, and derivatives in boxes only;
- its own enumeration;
- inputs = AGENTS.md + contract + the 28 shared premises (30 files), with no `triage.md`, Jung loop-2 or forward AY1 file.

## 10. Predicted values (the post-comparison flags any difference)

| Quantity | Prediction |
|---|---|
| D | 585079838465912592144137406066050/42981220507576537932303142777593983768257 ≈ 1.361245287e-8 |
| 2D; margin to 1/1250000 | 1170159676931825184288274812132100/42981220507576537932303142777593983768257 ≈ 2.722490574e-8; 29.3849 |
| 2D_i | 72266694536315307496644/1525878906463907516326874161 ≈ 4.7361e-5 (fails) |
| F2 J; support; termination | 28\|τ\| (= J_0 at cap); 4; 8; owner-set alternative 49\|τ\|/3 |
| F2 − F1 faces; distance | 28N(5N+1); N−1 |
| Reset on R; C_F | 98\|τ\| (both families); 56\|τ\|\|F\| |
| Creations meeting R | 82 faces / 27 owner sets from 7 anchors; 10 survive; 72 vanish; 0 single-site |
| ‖ρ^(1)_R‖_1 | √10\|τ\|/72 ≈ 4.39205e-10 (triangle 5\|τ\|/36) |
| Tr(ρ^(1)W), Tr(ρ^(1)W²) | +τ/144, 0 |
| K_2′ (trace norm, triangle) | ≈ 13417.5275 (≈ 3.9995 K_2^+) |
| K_2′ (√2 sectors, labelled) | ≈ 9487.95 |
| W-projected R-local | ≈ 3354.49943 (K_2^+ − 0.30380) |
| 2K_2′τ² | ≈ 2.68351e-12 |
| ±τ separation | ≥ 8.7573e-10 |

A producer `K_2′` for the density below K_2^+, or below 6708 without a new second-order computation, is an error.

## 11. Producer-error checklist
1. **82-face density.** ρ^(1)_R written over the 82 faces or 27 owner sets meeting R, or a trace norm of `2√82 a` or `164a`.
2. **Sign and units.** The sign `−τ/72`, or the mixed-unit amplitudes τ/9 or τ/576.
3. **Derivative misuse.** Differentiating only the fidelity (which gives 0), or differentiating a subsequential limit.
4. **K_2′ errors.**
   - K_2′ smaller than K_2^+ for trace norm.
   - K_2^+ reused as K_2′.
   - A W-projected constant presented as a density bound.
   - Straddling pinned to 6 in trace norm.
   - A missing sector or a missing factor 2.
   - Crude T mixed with the exact tier.
5. **F2 errors.**
   - AM2 cited for F2 without recomputing J.
   - Outgoing-only J (7|τ|).
   - AX1's `J_0′ = 29/10⁸`.
   - The claim that padding changes ρ_R.
   - AQ1's chosen subsequence reused for F2.
6. **Pair-constant errors.** D instead of 2D, √2D, D_i mixed with D_ii, or AX1's D′.
7. **Forbidden claims.** Uniqueness, whole-sequence convergence, rate, translation invariance, boundary independence of dynamics, "the AQ state", "the limit state", or "uniform in a".
8. **Topology errors.** Weak-* passed off as trace norm, or dynamics claimed uniform over the full local B(H).
9. **Clock and coupling.** `u = s/8` in a packet, or a comparison across couplings labelled "same τ".
10. **Boundary comparison.** "Quantitative boundary comparison" stated as 2D alone, or as a selection of the boundary condition.
11. **Uniform-in-N constants.** A Kato per-box τ² constant used as uniform in N (AW1: C(s)'s constant is unbounded). The uniform K_2′ comes from the anchored norm.
12. **Arithmetic.** Floats in admission, or √10 and √2 without directed brackets.
