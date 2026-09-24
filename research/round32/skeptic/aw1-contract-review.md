# AW1 contract review (skeptic, pre-comparison)

**Standing.** Written from the frozen `contracts/aw1.json` (sha256 `c24bf7eb…14ef`) before either AW1 producer was read. I am a model-agent skeptic with correlated ancestry, not a human reviewer. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written, under the readings below.** `aw1_check.py` executes all 30 control ids as damaging mutations, adding positive demonstrations where the semantics ask for them. It gives exact-tier K_2^+ ≈ 3354.80 and τ_AW2 = 10^-8, with a margin of 207.0 at the cap. Item 1 is the only substantive defect. Nothing blocks production, and I will hold the producers to these readings.

1. **Sign of item 3's formula.** "omega_tau(W)=2<W Omega_0, c^(1)>" with the AV1-admitted c^(1)=H_0^{-1}P V Omega_0=-(tau/72)ΣW_fΩ_0 gives **-τ/144**. Since ψ=e^{-C}Ω_0=Ω_0-c^(1)+…, the correct formula is ω(W)=-2Re<WΩ_0,c^(1)>+O(τ^2)=+τ/144. Each report must name its c^(1) convention and show the full sign chain from I1.5. A +τ/144 obtained from the literal formula hides a compensating sign error.
2. **What a tier is for K_2.** The coefficient 1/144 is exact algebra and belongs to no tier. The tier is the source of t in every remainder term. Exact tier: t≤t_1/(1-352J), with t_1=49|τ|/144 (grouped √ only if labelled). Crude tier: t≤J_0G(R) in every term. The 288t/(1-8t) form appears in the AV1 forward report but not in the AV1 gate text, so I accept it only as a labelled refinement.
3. **"49 omitted faces of a factor"** (item 2) means the faces whose owner set contains the factor; 21 are anchored there. Coarse e_z moves the fine z coordinate by one, and E is not invariant under that shift, so the enumeration must cover both z-parities of the factor. My enumeration does.
4. **"The multiplet"** (item 1) must be the gauge-invariant energy-3 eigenspace, which is the span of the plaquette vectors. On the full energy-24 eigenspace, PVP≠0: I exhibit a normalized element 1/8.
5. **"C(s)=e^{-3s}/4+O(τ^2)"** is a finite-volume Taylor statement. AW1 has no uniform constant for it, so it must be marked explicitly unbounded. For ω(W^2), the same split gives a uniform constant (≈1677.5, a labelled extra).
6. **Two-creation term** (item 4). I read this as all disjoint pairs I∋0, J∋e_z. The internal pair {0},{e_z} is O(τ^4) because c^(1)_{0}=c^(1)_{e_z}=0. The pairs that involve straddling are O(t^3). The conservative t^2 is acceptable.
7. **Reverse isolation.** Item 8's "without the panel notes" cannot hold for the flip lemma:
   - `shared_premises` includes both loop-3 sign-offs (`skeptic/loop3-signoff.md` §3 and `experts/modern/loop3-signoff.md` §2), which state the lemma, its combinatorics and a K_2 range;
   - `skeptic/av2.md` gives AW1 advice;
   - `selection-aw1.md` states the mechanism.

   The reverse's independence is therefore limited to its proof route, enumeration and code, and the gate should say so. This is non-blocking and the same pattern as my AV1 veto 1.
8. **AW2 rule.** Rounding is not preregistered, so the producers' K_2^+ will differ (352 or 288 form, triangle or grouped, multiplier). The rule's output is τ_AW2=10^-8 for every exact-tier K_2^+≤10^8/288≈347,222, so it is robust to those choices. The gate should still quote one directed value together with its form. A crude-tier K_2 (≈7.94e6) would give 10^-10, and that result is rejected.
9. **Sign and scope.** "Margin ≥ 2 for accepted" is a feasibility statement: item 5 admits no enclosure of ω(W), so no sign is certified in AW1. My loop-3 figure "K_2 1.1–1.9e4, margin 36–63" was the ×4 reading and is superseded.
10. **Flags.** Item 7 does not list `third_order_remainder_claim`. My checker adds it as false. The mirror equals the control list (30=30).
11. **Flip statement.** Item 2's flip must be stated for open whole-star boxes and their compressions Q_nHQ_n. Odd periodic sides and frozen or gauge-fixed links are excluded. The AQ statement is S(-τ)=S(τ)∘α_E, with pointwise antisymmetry only along a common subsequence.
