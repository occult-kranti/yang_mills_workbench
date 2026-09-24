# AY1 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/ay1.json` (sha256 `be9b3544…79ae0`, frozen 2026-09-24T02:11:14Z) before reading either AY1 producer. I am a model-agent skeptic with correlated ancestry. My triage (Goal 4 note and control 17) seeded the "2D closeness" idea and the fixed-vector and common-interval controls, and my AV1 and AW1 reviews are shared premises. This is not human review. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written, with the readings below.** `ay1_check.py` (96 checks) confirms the following:

| Item | Value |
|---|---|
| AV1 tier `D` | the gate's forward `D_ii ≈ 1.36125e-8` |
| `2D` | `≈ 2.72249e-8 ≤ 1/1250000`, margin 29.385 |
| Tier (i) | `2D_i ≈ 4.736e-5`, fails and is retained |
| Padded family (F2) | per-site sum `J = 28|τ|` (equal to `J_0` at the cap), support ≤ 4, termination order 8 |
| Contraction | `37/6250000 < 1/64` and `77/390625 < 1` |
| Reset | `98|τ|` on R, `C_F = 56|τ||F|` |
| First-order density | 10 of the 82 faces meeting R survive the R-marginal |
| Trace-norm `K_2'` | `≈ 13417.53` |

All 21 contract controls are implemented as damaging mutations. `reverse_premise_isolation` runs on an inventory derived from the contract; the actual producer inventories can only be checked after comparison. The control mirror matches (`controls` = `preregistration.controls_required.ids`, 21 = 21). Nothing blocks production.

1. **Item 3: "R-local K_2' … (not the whole-box K_2^+)", and "compare K_2' with K_2^+".** This is the main reading. The phrase assumes that restricting to faces meeting R shrinks `K_2^+`. It does not, for three reasons:
   - `K_2^+` is already a constant on the cover R, for the single observable W.
   - 99.979% of `K_2^+` is the per-site AM2 majorant `ρ = 352JT ≈ 3354.108τ²`. No restriction to faces meeting R reduces it.
   - A **trace-norm** constant on `B(H_R)` is the topology that item 1 names and the sentence template uses. It pays multiplier 2, not `2||WΩ_R|| = 1`. It also pays three excited sectors of `H_R` (`{0}`, `{e_z}`, `{0,e_z}`) instead of one.

   Hence every trace-norm `K_2'` assembled from the AW1 items satisfies `K_2' ≥ 2ρ/τ² ≈ 6708.2 > K_2^+`. The sharper `288t/(1-8t)` majorant still gives ≈ 5488.7. The values are:

   | Variant | `K_2'` | Relation to `K_2^+` |
   |---|---|---|
   | triangle | ≈ 13417.53 | ≈ 3.9995 `K_2^+` |
   | labelled sector-orthogonal (√2) | ≈ 9487.95 | larger |
   | W-projected R-local analogue | 3354.4994 | below `K_2^+` by 0.3038 |

   The W-projected analogue is the only one below `K_2^+`, and it is not a density bound. The modern lens's update-3 expectation that `K_2'` is "strictly smaller than AW1's K_2^+" is false for a trace-norm constant. Each packet must name the topology of its `K_2'` and state the sign of the comparison.
2. **Item 3: "restricted to the creations meeting R".**
   - The seven incident anchors carry 21+21+16+4+8+4+8 = **82** faces meeting R (27 owner sets). There are no single-site creations in the zero-selected family.
   - The R-marginal removes the **72** straddling faces exactly. Each has a link owned outside R that occurs once, so its Haar integral is zero.
   - So `ρ^(1)_R = +(τ/72) Σ_{10 faces with owner set {0,e_z}} (|W_fΩ_R⟩⟨Ω_R| + h.c.)`. It is rank two, has trace norm `√10|τ|/72` and `Tr(ρ^(1)W) = +τ/144`.
   - The modern update-3 display "−(τ/72) Σ Tr_{R^c}[…]" has the opposite sign and gives −τ/144. That note is not an AY1 premise, but it is a trap.
3. **Reverse route, "derivative of the vacuum-overlap/fidelity identity".** `Tr(ρ_R P_R) = 1/(1+e²)` has zero τ-derivative. It fixes only the `P_R` block. The `Q_R` block has trace `e²/(1+e²) = O(τ²)`. The off-diagonal block needs the partial overlap `⟨v⊗φ_out, ψ⟩/||ψ_out||²` with `v ⊥ Ω_R`.

   Derivatives exist only in finite boxes. A subsequential limit is chosen separately at each τ, so it has no τ-derivative. "The same for every subsequential limit" must therefore be the uniform-remainder statement `||ρ_R − P_R − ρ^(1)_R||_1 ≤ K_2'τ²`.
4. **Template "agree to first order in tau".** I read this as `||ρ_R − ρ'_R||_1 ≤ 2K_2'τ²` at the same τ, for every `|τ| ≤ 10^-8`, with `K_2'` explicit and uniform in N.
5. **Which boxes carry family F2.** I read F2 on the same centered cubes `Λ_N = [−N,N]³`, padded to `B_+ = ∪(b+S)` with decoupled Haar sites. The padding leaves `ρ_R` unchanged.
   - F2 retains `28N(5N+1)` more faces than F1, and the nearest of them lies at ℓ∞ distance N−1 from R.
   - For N ≥ 2 both families have the same 82 faces meeting R and the same seven full groups. At N = 1 the counts are 49 and 60.
   - A producer using other exhaustions must name them.
6. **AM2 "at the same J_0" for F2.** This holds with equality at the cap: bulk sites have `J = 28|τ| = 7/25000000`.
   - The AM2 gate's limitation "complete interaction grouping essential" is met, because each retained face sits in exactly one anchor group and all incoming groups are counted.
   - AGENTS.md requires recomputing the budget after a changed support decomposition. I recomputed it, and it happens not to change.
   - Owner-set grouping (`J = 49|τ|/3`, support 3) is an admissible labelled alternative. It is also the native Nachtergaele–Sims restriction for F2.
7. **"At the same tau" and the meaning of 2D.** `P_R` does not depend on τ, so `2D` also bounds two states at different couplings.
   - The `±τ` densities are certifiably different, at least 8.757e-10 apart, yet both lie within `2D`.
   - So 2D alone is not a boundary comparison. The comparison content is the matching first-order term, with difference `2K_2'τ² ≈ 2.684e-12`.
   - Item 6's definition says exactly this. A packet that offers 2D alone as "the comparison" is incomplete.
8. **Template and gate fields.** The frozen preregistration string governs.
   - It differs from the Jung loop-2 §4 text that item 4 names. Jung's version adds:
     - "every A in B(H_R), ||A|| ≤ 1", which is equivalent by trace duality;
     - "boundary independence beyond R";
     - "may differ … without bound elsewhere";
     - the fields `states_compared`, `region`, `topology`, `closeness_order` and `rate_in_N_claimed`.
   - Jung update-3 flags a missing `translation_invariance_claimed`. That flag refers to a draft: the frozen item 4 and `gate_fields_required` both list it.
   - Export the contract's five fields (mandatory) and, where they do not conflict, Jung's fields as well.
9. **`state_provenance`** names only the AQ1 subsequence, but F2 is not AQ1's construction. This is non-blocking wording: each family needs its own diagonal extraction.
10. **Dynamics.** Each family carries its own Nachtergaele–Sims dynamics: F1 with star-indexed Φ, F2 with owner-set-indexed Φ′. AY1 does not claim that the two infinite-volume dynamics coincide (`boundary_independence_of_dynamics_claimed:false`). A Lieb–Robinson boundary argument may give this, but it would need its own contract.
11. **Reverse isolation.** The shared premises already state much of the mechanism:
    - the AV1 and AW1 reports and my `av1.md` and `aw1.md` state the product split, the 82/10/72/33/6 pins and the ×4 conservative variant;
    - `selection-ay1.md` states 2D and "first-order densities coincide".

    The reverse's independence is therefore limited to its proof route, enumeration and code. This is non-blocking, and the gate should say so.
12. **Tier.** The target `1/1250000` is twice AV1's `4/10⁷`.
    - `D` must be the gate's forward `D_ii`.
    - The reverse's 82-face value (≈ 1.139e-8) may be used only as a labelled refinement.
    - AX1's `D'` (uniform model, ≈ 1.4446e-8) belongs to a different model and is rejected.
13. **Not uniform in a.** The zero-selected patterned family is defined at fixed spacing and has no τ(a) dictionary. Under the uniform-model dictionary `τ = 96/g⁴`, every path with `a → 0` and `g → 0` leaves `|τ| ≤ 10^-8` once `g⁴ < 9.6×10⁹`, and leaves the coefficient box once `g⁴ < 32`. "Uniform in N" means uniform in the volume at fixed spacing only.
