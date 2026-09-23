# Round32 skeptic, deliberation loop 2: critique of plan v1 and the three lens memos

**Standing.** Model-agent skeptic with correlated ancestry (same model family as the advisor, lenses and producers). This is not human peer review and not formal verification. The note extends `triage.md` and `prospective-controls.json` and corrects them where they were wrong. Read: `AGENTS.md`; `advisor/brief.md`, `deliberation-1.md`, and the draft `plan.json`, `selection-av1.md`, `contracts/av1.json` and `av2.json` (these appeared during this loop); the historical, Jung and modern memos with their recommendations and loop-2 responses, plus `sota-table.md`; AM2 forward; AT4 forward §1–6; I1 forward §3–4 (the face table and I1.5); Round29 `experts/sources.json`. The scratch previews (`loop2_checks.py`, `inv.py` in the session scratchpad; mpmath at 25–30 digits plus `Fraction`) are not evidence. Human project author: Hruday N M (BUNZEEY).

## 0. Two new facts that change numbers in every memo (mine included)

- **Per-site face count is 49, not 84.** I1's 21 omitted classes have relative supports {0,e_y}×3, {0,e_x}, {0,e_x,e_y}, {0,e_z}×6, {0,e_x,e_z}×2, {0,e_z}×4, {0,e_y,e_z}×4. The number of classes containing each offset is: 0 in 21, e_x in 4, e_y in 8 and e_z in 16. So a bulk factor u lies in the owner set of 21+4+8+16 = **49** faces, which fall into 15 owner sets with multiplicities {1,1,1,1,1,2,2,2,3,3,4,4,4,10,10}. There are 82 faces meeting R, 10 with owner set exactly R and 16 containing R; these match the modern enumeration. My 84 = 4×21 is only an upper bound. Faces with the same owner set give mutually orthogonal vectors W_fΩ_0 of norm 1/2, so exactly ||c^(1)||_a = (|τ|/144)·Σ_M √n_M ≈ 0.17384|τ|. The rational triangle bound is ≤ 49|τ|/144.
- **Wilson-mean multiplier is 1, not 4.** In ψ = ψ_out + δ, the only term of ξ that overlaps WΩ_R at first and second order is −c_R, whose support is exactly R. The single-site terms c_{0}⊗Ω and Ω⊗c_{e_z} are exactly orthogonal to WΩ_R at all orders, because W puts j=1/2 on the e_z-owned link (e_z,x). Also ||WΩ_R|| = 1/2. Hence |2Re⟨(c−c^(1))_R, WΩ_R⟩| ≤ ||c−c^(1)||_a. My triage's "4·2·4704 ≈ 1.9e4" was both an arithmetic slip (the product is 3.76e4) and an unnecessary factor 4. The historical loop-2 table inherited that factor as "2 Re × 2 sites".

## 1. Errors or overclaims in each memo

**Historical (Newton/Tesla).**
- (a) "If the weighted AM2 fixed point does not close ..., the O(tau) claim is withdrawn" (memo §2 and §3 table). This falsifier is misdirected. The product split needs no star-connectivity and no Kotecký–Preiss step. Loop 2 retires the polymer reading for AV1, and I agree.
- (b) "K_2 ≈ 1.6e8". The (20·592)² term over R⁺ is an over-count, and the Lipschitz constant G'(R) is taken at the ball edge. Loop 2 concedes both.
- (c) Loop 2's S2 says "enumerate 84 faces per site … ||c^(1)||_a = 7|tau|/12". The count is 49 (§0), and the "multiplier 4" row is wrong (§0).
- (d) Memo §0.5/§5.5 mixes the two uniform-model routes. "Haar reset budget … 102|tau|" is route B. "AM2's h_x already contains the selected potential, so its gap proof covers the uniform triple … reference no longer Haar" is route A. The 102|τ| budget is valid only with the Haar reference and a J'=29|τ| re-proof. Control `reference_route_declared` exists for exactly this mix.

**Jung/Pauli.**
- (a) "an O(tau)-error method cannot resolve an O(tau) shift, so AT4-type budgets are structurally reference-inside at every tau." This is false as a general rule: an O(τ) method resolves an O(τ) shift whenever its constant is below the coefficient (here c_1 < 1/144). The true statements are narrower. AT4's √τ budget cannot resolve any O(τ) effect at small τ. The crude O(τ) constants (1792–2368) exceed 1/144 by (2.6–3.4)×10^5. And the centered C(s) shift is O(τ²) anyway.
- (b) T2's finite graph, "the 48-link cover R={0,e_z} with the seven incident whole-star terms … j<=j_max", is not closed: the stars reach 20 factors. It is also not executable: already at j ≤ 1/2 there are 5^48 ≈ 3.6×10^33 link states before gauge reduction. The executable finite model is the Round11 two-plaquette graph.
- (c) T1 proposes C_τ(s*)−e^{−3s*}/4 as a shift observable. It is second order (about 10^-16 at the cap), so it cannot serve as a Round32 shift target.
- (d) Loop-2 script 1 passes when "at tau=0 … every node interval is e^{-3s}/4 ± 3/(2·10^30)". That criterion is wrong for the AT6 Poisson pipeline, because the tail (1/2)(2s/(πL)) survives at τ=0: 3.2e-10 at s=1 and 4.1e-8 at s=128 for L=10^9. It is correct for the AV2 window pipeline, which has no tail.
- (e) Script 2 decides PASS through floating logarithms. An admission-grade check must compare the exact ratio D(τ)/D(τ/100) with rational brackets: [99,101] for linear, [9.9,10.1] for square root, [9900,10100] for quadratic.
- (f) Loop-2 §3 says "E_+ + E_- enclosed in [-2K_2 tau^2, 2K_2 tau^2]" (mirror images). This holds by construction for any enclosure of the form ±τ/144 ± K_2τ², so it discriminates nothing. The discriminating controls are the φ_b-sign mutation and an independent small-model fixture.

**Modern (Penrose/Feynman).**
- (a) (M1): "No <psi,psi> and no e^{-C^dagger} appear." The left vector is l = e^{−C†}ψ/⟨ψ,ψ⟩, so both are hidden inside l. The unproved anchored bound on l is the normalization problem itself, moved rather than removed.
- (b) "c_1' of order 1.5e7" and "remainder ~1.4e7 tau^2" mix tiers. The first-order c^(1) is exact, but the remainder uses the crude t = 448|τ| and the factor 4. Self-consistently t ≈ 0.17–0.58|τ| and K_2 ≈ 1.4e3–5.8e3 (§2b).
- (c) (M3) "~1.5e-9 at the cap" and the expected "accepted_within_scope (radius <= 1e-8)". (M3) omits the second relative-unitary step. The first-order Duhamel integrand contains B evolved by A = G_{0,R}+G_outside, which is interacting outside R. Haar vanishing of T_1 applies only after replacing A by free dynamics on R⁺ (40 stars; historical H3) and after an O(τ) state lemma on the 20-site R⁺. The memo also silently redefines the target: the roadmap target is 10^-6.
- (d) The failure mode "insufficient (anchored bound for the left eigenvector not proved; fallback to sqrt reset)" is a false dichotomy. The product split needs no l-bound.
- (e) "|omega(W^2)-1/4| <= c_2 tau^2 … beaten by one order." The vanishing of the first-order term is an AW1 target, not a premise, and c_2 must also carry the density and pair terms.
- (f) Skeptic question 4 assumes "faces sharing two links with W (same-plane neighbours)". Two distinct plaquettes share at most one link; same-plane neighbours share exactly one.
- (g) The Gauvin framing "priority/independence … must be diffed" is misframed (§3).
- (h) The C² taper is said to be "evaluated in closed form". M_j = ∫|θ|^j|f̂| is the integral of the modulus of an oscillatory function and has no closed form, so it needs a certified quadrature with tails.

**Deliberation-1.**
- Agreement 3 says "Both the skeptic and the historical lens derived this independently." We are correlated model agents, so the word should be "separately". The parity vanishing is also an AW1 derivation target, not an agreed premise; AV2 as drafted correctly does not use it.
- Agreement 1's figure "D<=2.34e-8" rests on the 84 bound. With 49 faces it becomes 6.95e-9 (grouped) to 1.36e-8 (triangle bound).

## 2. Positions on the disagreements

**(a) Window versus second-order Duhamel for AV2: freeze the window.** Checked independently. The transform ĝ(θ) = (2π)^{-1}∫g e^{−iθx}dx = 4s³/(π(s−iθ)³(s+iθ)) matches direct quadrature to 1e-20. The window is C² at 0. The constants are ||ĝ||_1 = 2, ∫|θ||ĝ| = 4s/π and ∫θ²|ĝ| = 2s², analytically: ∫(s²+θ²)^{-2} = π/(2s³) and ∫|θ|(s²+θ²)^{-2} = 1/s². Oscillatory-quadrature inversion reproduces e^{−3}, e^{−1/2} and g(−1) to 15 digits. Keep the second-order Duhamel as a named, unexecuted refinement, whose hypotheses include the 40-star second step. Newly observed: the C¹ window g(x) = e^{sx}(1−2sx) for x<0 has ĝ = 2s²/(π(s−iθ)²(s+iθ)), with M_0 = **4/π** and M_1 = 4s/π; M_2 is infinite. It dominates the C² window for AV2's first-order budget, but the gain is 5% at tier (ii) (1.73e-7 versus 1.83e-7). No re-plan: the C² window keeps M_2 finite for the refinement.

**(b) K_2 for ω_τ(W) = τ/144 + r.** Terms that are real:
(i) the AM2 degree-≥1 remainder on c_R, ≤ J(G(t)−16) ≤ 352·J·t (all-rational; 288.02·J·t with a directed exp); (ii) the two-creation term c_{0}⊗c_{e_z}, ≤ t² (in the zero-selected corner c^(1)_{0} = c^(1)_{e_z} = 0 because no omitted face has single-factor support, so it is really O(τ⁴)); (iii) straddling I ⊋ R, ≤ t², while straddling I with |I∩R| = 1 contributes exactly 0; (iv) density Tr_out|δ⟩⟨δ|, ≤ ε²; (v) normalization, τ/144 × ε², third order; (vi) pairs involving a straddling creation, O(t³).

Terms that are not real: the R⁺ square and the ×4 multiplier. Here t is the self-consistent bound t ≤ t_1/(1−352J), with t_1 the exact first-order anchored norm.

My honest range at the exact tier is **K_2 ∈ [1.4×10^3, 5.8×10^3]** with multiplier 1 (grouped count through the 84 bound). It widens to at most 2.3×10^4 if AW1 proves only the conservative ×4. The sign margin (1/144)/(K_2·10^-8) is therefore 30–500 at the cap. At the crude tier (t = 448–592|τ|), K_2 ∈ [4.8×10^6, 2.1×10^7] and the sign fails at the cap by a factor of 7–30. The figure 1.6×10^8 is retired.

AW1 must enumerate, with each term's tier named: (1) the 21 classes, the 15 owner sets and 49 faces per site, with boundary ≤ bulk; (2) the 10 faces with owner set exactly R, showing ⟨W_fΩ_0, WΩ_0⟩ ≠ 0 only for f = W; (3) the self-consistent t; (4) terms (i)–(vi) separately, none set to zero; (5) τ → τ/100 scaling of each term; (6) the sign under I1.5 (V = −(τ/24)ΣW_f in G units, giving +τ/144).

**Riesz/left-eigenvector formulation versus ψ_out+δ.** They are algebraically equivalent: P = |ψ⟩⟨ψ|/⟨ψ,ψ⟩ = e^{−C}|Ω_0⟩⟨l|e^C. They are not proof-equivalent, because the l-route puts an unproved nonlocal bound on the critical path. Freeze the forward route as the product split with the explicit reduced density, giving 2ε(1+ε)/(1+ε²). Freeze the reverse route as fidelity: (P_R⊗1)ψ = ψ_out, then 1−Tr(ρP_R) = e²/(1+e²), then AT4 F08, giving 2ε/√(1+ε²). This bound is sharper and shows why the square root disappears: the infidelity is O(τ²) from the vector, versus O(τ) from the energy. The Riesz form becomes an assistant fixture only (a 3–4 site comparison of ⟨l, e^C A e^{−C}Ω_0⟩ with Tr(ρA)), not a producer route.

**(c) Finite-graph placement: accept** assistants after sub-round 2 and candidate AZ2, with Jung's three conditions. I add three more:
- The graph is the Round11 two-plaquette graph, or smaller.
- Coefficients are computed algebraically (exact Rayleigh–Schrödinger on the graph plus a certified tail) or as certified values on a τ_FG grid frozen in advance; coefficients fitted to enclosures are previews only.
- A finite-graph δ never resolves roadmap goal 2. τ_FG ∈ [24,48] lies about 2.4–4.8×10^9 times beyond the AQ cap, so "moderate" is a misnomer.

**(d) Uniform model: J' = 29|τ| versus the frozen J_0 = 7/25000000.**
- Resolution A (preferred): a new AX1 instance with J_0^unif = 29/10^8. The conditions are J_0^unif·148/7 = 1073/175000000 < 1/64 and 2·J_0^unif·352 = 319/1562500 < 1, and the excited-sector exclusion uses the same inequality. The majorant (HNM-AM2.5) accepts |X| = 1 groups because p = 4 bounds the support.
- Resolution B: keep J_0 and restrict the model to |τ| ≤ 7/725000000 ≈ 9.655×10^-9. This is a changed coupling and would need `changed_model_relabelled`.

I prefer A because it keeps the cap at a slack of about 2500. A is a new paired theorem instance, not an edit of the frozen AM2 gate, and AQ1/AQ2 constants that depend on the interaction family (for example ||Φ||_F ≤ 2268|τ|) must be re-derived too. Add a control fixing the selected-face sign convention: all 24 faces per factor enter as −(τ/3)W_f in δ units.

**(e) Modern C² taper versus the rational window: the rational window.** |ĝ| is an explicit rational function, so the constants are exact rationals times π^{-1}. The taper's M_1 of 2.4–3.0 (preview) is 1.9–2.4 times worse on the term that dominates at tier (ii), totalling 3.2–4.0e-7 against 1.7–2.0e-7. Its smaller M_0 helps only at tier (i), where every kernel fails anyway (3.1e-5 against 4.7e-5). Keep the taper as an assistant preview.

## 3. Gauvin arXiv:2503.15539

The project's own Round29 ledger (`research/round29/experts/sources.json`, accessed 2026-09-22) already records v3's supplement A.6–A.8 ("creation estimates, spectral exclusion, cutoff removal") as the **AM template**. Independence of AM2 is therefore excluded whatever v1 contains, and the diff decides only whom and which date to credit.

Diff v1 (2025-03-06) against v3 (2026-09-14), and v2, from downloaded PDFs and sources with SHA256 recorded. Extracted text only; no tool summaries.
- (i) Submission history: dates, sizes, title, abstract, comments, category and cross-lists, and the ancillary files (whether a supplement exists in v1).
- (ii) For each v3 item, mark it present in v1 verbatim or equivalent, present as statement only, or absent, with its v1 location: Thm 2.3 (fixed-cutoff SU(3) gap ≥ 8a/3, b/a ≤ 1/648, uniform in volume); Lemmas 2.14–2.15 (creation adaptation to rotors); the constants radius 1/24, J/δ ≤ 1/128, Lipschitz < 47/48; Thm 2.5 and Cor 2.6 (thermodynamic ground state, nonnegative generator); supplement A.6–A.11; §VI.D Thm 6.13 and §VI.F.
- (iii) Whether v2/v3 cite earlier creation or Kirkwood–Thomas-type expansions (Yarotsky, Datta–Kennedy), and whether they mention this workbench (its first publication commit is dated 2026-09-09) or AI assistance. Record only; no inference about direction of influence.

Sentence the project may use meanwhile: *"AM2 applies, with separately derived constants for the SU(2) I1 selected-strip family, the fixed-cutoff creation-operator strategy that this project's Round29 source ledger records as its template, Gauvin arXiv:2503.15539v3 (2026-09-14; main text §II.3 and supplement A.6–A.8); whether that strategy already appears in v1 (2025-03-06) has not been checked, and no priority or independence is claimed."*

## 4. Freezable wording for AV1 and AV2

**New control ids.**
- `tier_mixing_rejected`: the exact c^(1) combined with the crude t, or a refined t used without the self-consistent inequality t ≤ t_1/(1−352J), is rejected; every term names its tier.
- `face_count_all_sites`: 49 faces per factor and 15 owner sets, from the I1 table by translation covariance, with boundary counts ≤ bulk; a count restricted to sites 0 and e_z is rejected; 84 is accepted only as a labelled bound.
- `reverse_premise_isolation`: the reverse `inputs/` inventory equals the contract's reverse list; it contains no `skeptic/triage.md`, `deliberation-*.md`, `experts/*/loop2-response.md` or forward AV files.
- `av2_feasibility_threshold`: D is also tested against 4/10^7, the value AV2 needs, because 2(D+D²)+49·10^-8/π ≤ 10^-6 requires D ≤ 4.22·10^-7.
- `window_fourier_sign_convention`: the frozen convention is c(θ) = ⟨χ,e^{iθG}χ⟩ with ĝ = (2π)^{-1}∫g e^{−iθx}; the mutation θ → −θ returns g(−3)/4 = 25e^{−3}/4 on the free atom and must be rejected.
- `state_term_not_effect`: the D/2 effect refinement applied to Wα^0_θ(W) is rejected (AT4 F12).
- `av1_tier_bound`: the D used in AV2 equals the AV1 gate's admitted tier; an unadmitted tier is rejected.
- `tau_zero_null_replay` (Jung, amended): at τ=0 the window radius equals the arithmetic term alone. The Poisson comparison at τ=0 keeps the itemized tail s/(πL), so a ±3/(2·10^30) criterion there is rejected.

For AW1 and AX1 later: `wilson_overlap_single_component` (only c_R overlaps WΩ_R; ×4 is accepted only if labelled conservative); `sign_convention_fixture` (Jung's one-plaquette fixture under I1.5, labelled a finite graph); `aw2_coupling_rule_prefrozen` (τ_AW2 is the largest element of a decade grid with K_2^+|τ| ≤ 1/288, frozen in AW1's contract); `j0_resolution_declared` and `uniform_sign_convention` (as in §2d); `fg_coefficients_not_fitted`.

**AV1 required** (replaces the draft list):
1. **AM2 objects.** State the AM2 objects: creators, the fixed point, ψ = e^{−C}Ω_0 in each cutoff space and each centered whole-star box Λ_N (N ≥ 2). Give J ≤ 28|τ|, R = 1/64, G, G(R) < 148/7 and G'(R) < 352 as exact rationals. Prove that AQ1's boxes are AM2's family: the same stars b+S ⊂ Λ_N and the same onsite Haar reference. No Yarotsky, HTW or Gauvin constant is used.
2. **Forward route.** Place the factors meeting R last to get ψ = ψ_out+δ with δ ⊥ ψ_out and ||δ|| ≤ ε||ψ_out||, where ε ≤ 2t+t² includes the two-creation term. Write ρ_{N,R} explicitly, including |Ω_R⟩⟨ξ|, its adjoint and Tr_out|δ⟩⟨δ|, and prove ||ρ_{N,R}−P_R||_1 ≤ 2ε(1+ε)/(1+ε²) uniformly in N.
3. **Reverse route.** Prove (P_R⊗1)ψ = ψ_out and Tr(ρ_{N,R}P_R) = 1/(1+e²) with e ≤ ε, then apply AT4 F08 to get ≤ 2ε/√(1+ε²). The shared product-ordering premise is declared. Independence is claimed only for the inequality, the constants, the enumeration, the cutoff step and the passage step. Each producer derives the normalization trap and a model-class counterexample (a three-site fixture) before exchange (AGENTS.md).
4. **Tier (i).** Use t ≤ J_0G(R) < 148/25000000, optionally iterated with a directed exp. Report D_i at τ = ±10^-8 as exact rationals.
5. **Tier (ii).** Enumerate as in `face_count_all_sites`. Show that each W_fΩ_0 is an H_0 eigenvector at normalized energy 24 and that the vectors are orthogonal with norm 1/2. Then ||c^(1)||_a ≤ 49|τ|/144, and the grouped √-form is allowed with rational upper bounds. Use t ≤ t_1/(1−352J) and ||c−c^(1)||_a ≤ 352Jt, or the sharper directed form. Report D_ii at τ = ±10^-8 (preview 7.0e-9 to 1.4e-8).
6. **Cutoff-vector removal.** Prove the ground vector converges, via Q_nφ, the uniform gap 1/2 and |⟨ψ_n, Q_nφ⟩| → 1, so the reduced densities converge in trace norm.
7. **AQ passage.** The bound holds for every subsequential limit of AQ1's construction; no uniqueness.
8. **Consequences and scaling.** Show |ω(W)| ≤ D and |ω(W²)−1/4| ≤ D/2 for both tiers. Show the exact ratio D(τ)/D(τ/100) ∈ [99,101] for both tiers, against [9.9,10.1] for AT4.
9. **Targets and checker.** Test D_ii ≤ 4/10^7 and also report against 10^-6. `check.py` records exact rationals, the fixtures and the claim flags (the draft's five plus `first_order_parity_claim:false`). Replays are byte-identical under normal and -O Python.
10. **Premise lists.** The forward list may include `triage.md` (disclosed). The reverse list is AGENTS.md, the contract, the AM2 forward, reverse and gate, the AQ1/AQ2 forward reports, AT4 forward §3, I1 and `methods/`.

**AV1 controls.** The draft list, minus `sign_convention_fixture` (moved to AW1), plus `tier_mixing_rejected`, `face_count_all_sites`, `reverse_premise_isolation` and `av2_feasibility_threshold`. `first_order_face_enumeration` is re-read as 49 per site.

**AV1 exclusions.** The draft list, plus: the value or sign of ω(W) beyond |ω(W)| ≤ D; the first-order coefficient 1/144; any vanishing of first-order C(s) or ω(W²) (all AW1).

**AV1 verdicts.**
- accepted_within_scope: both routes are proved and D_ii ≤ 4/10^7 at both signs in both producers; the cutoff and passage steps are complete; every control rejects its mutation.
- limited: tier (i) only, or D_ii > 4/10^7, or only one route survives review, or the cutoff step is conditional. Name the dominating term.
- insufficient: the split, the orthogonality or the uniformity fails. AT4's √ bound then stays the admitted state term.

**AV2 required** (replaces the draft list):
1. **Window lemma.** Freeze the conventions of `window_fourier_sign_convention`. Prove the window lemma: g ∈ L¹ ∩ C_0; ĝ ∈ L¹; inversion on supp η ⊂ [0,∞) using AQ1 nonnegativity only, not the AQ2 gap; Fubini with finite η. Conclude C(s) = ∫ĝc and C_0(s) = g(3)/4.
2. **Constants.** Prove ĝ, |ĝ| = (4s³/π)(s²+θ²)^{-2}, M_0 = 2, M_1 = 4s/π and M_2 = 2s². The forward producer uses half-line transforms. The reverse producer uses residues (the simple pole at θ = is, the triple pole at θ = −is). The reverse checker computes these values from its own derivation and compares them with the contract; π is enclosed with directed rounding.
3. **Real-time comparison.** Prove |c(θ)−c_0(θ)| ≤ k|θ| + D + m² for all θ (AT4 F10–F12), with k = 49|τ|/4, D the AV1-admitted value and m² ≤ D².
4. **Radius.** E = M_0(D+D²) + kM_1 at τ = ±10^-8, s = 1, itemized, with a directed enclosure of e^{−3}/4 and a Boolean against 10^-6.
5. **Retained failures.** Keep the AT4 L=10^4 radius and the optimized Poisson floor 1.2651e-6 at unchanged τ and s, and show the divergent Poisson first moment.
6. **Crossover.** Report the s* where E = 10^-6 (about 6.1–6.3); no grid claim beyond it.
7. **No resolved shift.** The result carries the sub-label reference_unresolved.
8. **Calculator.** The AT5-style calculator is restricted to the proved domain.

**AV2 controls.** The draft list, plus `window_fourier_sign_convention`, `state_term_not_effect`, `av1_tier_bound` and the amended `tau_zero_null_replay`.

**AV2 exclusions.** The draft list, plus: the second-order Dyson refinement; any shift of C(s).

**AV2 verdicts.**
- accepted_within_scope: the lemma and constants are proved by both routes; E ≤ 10^-6 with the admitted tier-(ii) D (preview 1.7–2.0e-7).
- limited: only tier (i) is admitted (preview 3.6–4.7e-5), or only one route's constants survive.
- insufficient: the lemma or the constants fail, and the Poisson floor stands.

**Pre-registration.** I agree with Jung's block, with four amendments:
- `error_terms_itemized` is written per loop, and an entry may be "not_applicable" only with a reason. For AV1 the entries are am2_remainder, two_creation, straddling, density, onsite_cutoff_vector and arithmetic. For AV2 they are state, mean_square, kernel_dynamics and arithmetic.
- `controls_required` lists explicit ids, not descriptions such as "all 12 ids".
- `hash_binding` adds `check_py_sha256_recorded_before_full_size_evaluation` in place of "committed".
- The AV1 target is `{"quantity":"D_ii","value":"1/2500000","comparator":"<="}`.

## 5. Vetoes

1. **Draft av1.json item 2 conflicts with its premises.** The item requires each producer to find the normalization trap "on its own", yet both producers receive `triage.md`, `deliberation-1.md` and the loop-2 responses, which spell the trap out. Fix it with the premise isolation of AV1 item 10 and the reworded item 3.
2. **Draft AV1 target 10^-6.** Even a D ≤ 10^-6 at that target would leave AV2 infeasible. The target is 4/10^7.
3. **Draft AV1 item 4.** It enumerates faces only for factors 0 and e_z, but the anchored norm is a maximum over all sites.
4. **Plan AW2 "K_2|tau|<1/144, else the largest admissible tau".** A margin of 1 is too small and the coupling rule is chosen after K_2 is known. Require a margin ≥ 2 and a rule frozen in AW1's contract; the cap outcome is retained as limited.
5. **The AX2 rider** "plus the uniform Wilson-mean sign if AW transfers". An observable added after freeze needs its own contract.
6. **AZ2 fitted coefficients, and Jung's 48-link finite graph.**
7. **Any AM2 priority or independence sentence** other than the one in §3.
8. **Any AV target of "radius <= 1e-8"** imported from the modern memo. The roadmap target of 10^-6 stays, and the radius is reported.
