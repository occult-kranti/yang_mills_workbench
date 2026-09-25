# BB1 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/bb1.json` (sha256 `30400d2e…8018`, frozen 2026-09-24T23:36:46Z) before reading either BB1 producer. I am a model-agent skeptic with correlated ancestry. This is not human review. My pre-freeze review (`bb-contract-review.md` / `.json`) wrote 7 blocking and 10 non-blocking edits that the frozen text carries. So this review checks my own wording as much as the advisor's. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written, with the readings below. Nothing blocks production.** `bb1_check.py` establishes the following:
- 88 checks pass, byte-identical under `-B` and `-B -O`;
- the frozen targets are well-posed exact-rational upper bounds, and every constant the contract names can be computed from the declared premises;
- all 37 controls execute as damaging mutations: 106 mutations, each rejected for the expected reason, plus 39 positive cases accepted.

Four readings will matter at the post-comparison:
- **R6:** the normalization of intermediate regions in the split route.
- **D1:** a false clause in `normalization_couples_supports`, which I wrote.
- **R3:** the every-site exponent at u=0 changes C by a factor of about 1.97.
- **R10:** the fifth comparison and the untruncated passage for general F2 volumes.

## 1. Frozen bytes against the pre-freeze edits; producer inputs

**Edits.** All 17 replacement texts of `bb-contract-review.json` are in the frozen bytes verbatim (7 blocking, 10 non-blocking; check `prefreeze_edits_verbatim_in_frozen_bytes`). A field-by-field diff of the reviewed draft (commit e4857b4, sha256 `d2b82488…6d6b`) against the frozen file shows exactly those 17 fields changed, plus `status` and `frozen_at`. Nothing else changed.

**Plan records (outside the contract).**
- The BB1/BB2 freeze event was missing when I started. It was added during this review by commit 43eb922, after the BB2 skeptic's defect D8. It records `plan_sha256_at_freeze = fb018ac5…4713` and the BB1 contract hash `30400d2e…8018`. I checked both against commit 45a87be, the freeze commit: they match. P5 is now met after the fact.
- **Residual, non-blocking.** The "pre-freeze review applied" entry still says "secondary BB1 pair corrected with the admitted floor constant". The edit did the opposite: it names a re-instantiated disc input and records that the admitted floor constant does *not* reach the secondary targets.

**Producer inputs.** I ran `find` on `forward/bb1/inputs/` and `reverse/bb1/inputs/` (names only) and hashed each file against the repository.
- Each folder holds 35 files: `AGENTS.md`, the contract and the 33 shared premises.
- Every file is byte-identical to its source.
- Both inventories equal the contract-derived list.
- The only Round33 skeptic files are my BA1 and BA2 reviews (`ba1.md`, `ba2.md`). There is no triage, BB contract review, deliberation, plan, lens file, BB-targets proposal, forward BB1 file or BB2 producer file.

So `reverse_premise_isolation` holds at the inventory level. The program checks a synthetic inventory derived from the contract, as in BA1.

## 2. Readings and wording defects (numbered)

1. **D1 (wording defect, mine). `normalization_couples_supports` says "a one-site straddling first-order face has zero R-marginal while a support strictly containing R does not".** The second clause is false.
   - At first order only supports **contained in** R move ρ_R. These are the 10 faces with owner set exactly R: the AY2 gate's ρ^(1)_R is a sum over those 10 faces.
   - Every support that meets the complement of R has zero first-order R-marginal, because the Haar mean over its outside link vanishes. That includes supports strictly containing R, such as `{0,e_x,e_z}`.
   - The qubit fixture shows it exactly (check `fixture_straddling_supports`):
     - `{r0}`, `{r1}` and `{r0,r1}` move ρ_R at first order;
     - `{r0,o}`, `{r1,o}` and `{r0,r1,o}` (strictly containing R) have zero first-order marginal and a nonzero second-order block.

   **Reading:** "strictly containing R" is read as "contained in R". The damaging mutations of the control are unaffected: dropping straddling supports, charging them only at first order, or normalizing by 1+O(t²). A producer who reports the literal clause as true has an error.
2. **R1. The frozen lemma form and η.** With the real-parameter derivative, ∂ψ = −δ̂ψ, the near term has constant exactly 2 (η=0). The reason is the variance bound `|ω(A;δ̂_I)| ≤ ||δ_I||·||⟨Ω_I|ψ||/||ψ||·√Var A`, with −1≤A≤1 (fixture `fixture_near_support_variance_bound`). The split route's sine bound gives `2(1+t̄+K)` on R. Both fit the frozen form `2(1+η)`.
3. **R2. The far term has no polynomial p(|I|) if it is charged per site along chains.** The truncated-correlation recursion gives `κ(I) ≤ 2A|Y|e^{β|Y|}·64^{−d_∞(I,Y)}`, with p ≡ 1 and w' = 64 (derivation §4). But with w' = 1/q exactly, a per-support κ summed over a lattice diverges.
   - The region constant must therefore be assembled in the chain form, where the data profile `D(x) ≤ Kq^{d_Y}64^{d(x,Y)}` is carried along the recursion. Alternatively, κ is stated with w' > 64 and a shell sum per starting site.
   - A κ-form assembly with a lattice sum around all of Y gives |Y|², not the frozen |Y|.

   **Reading:** κ_0 may depend on Y as stated (`2A|Y|e^{β|Y|}`). The assembly must stay linear in |Y|.
4. **R3. The every-site exponent at u=0.** Form (b) gives `Σ_{I∋u}||δ_I|| ≤ K q^{N−|u|_∞}`, so the site 0 of R carries q^N.
   - Using it, `C = 2K(1+q+2Ae^{2β}) ≈ 8.9035e-7`.
   - Using the BA1 gate statement (u∈R, exponent N−1 at both sites) gives `C ≈ 1.7533e-6`.

   Both are valid and both meet 1/250000, with margins 4.49 and 2.28. A producer's C should be one of these, possibly with a larger η. The region constant is `c_site = 2K(1+A) ≈ 8.7664e-7` either way, because every site of Y is charged at `q^{d_Y}`. **c_site is the binding margin: 2.2814.**
5. **R4. Form (a) needs its source set named per comparison.** `K_own = T_w/(1−Γ) = 19140625/86785322066496 ≈ 2.2055e-7` is the every-u constant of the BA1 forward norm; its proof takes a maximum over u. The exponent is `d_∞(u,B)`:
   - the shell for nested comparisons (N+1−|u|);
   - the positive outer layer for F1 against F2 (N−max_i u_i);
   - sites outside Λ_N for the direct general-volume comparison, which the BA1 forward did not tabulate: it telescoped or went through the union.

   All of these are at least N−|u|_∞. These are labelled weighted_norm values, never the gate's bound value. The BA1 gate records the telescoped `K_gen = 2734375/12204185915601` as the forward's general value. A producer must say whether it uses K_own directly or K_gen.
6. **R5. Sites outside the smaller box.** Form (b) and form (a) are stated for u ∈ Λ_N.
   - Outside Λ_N the only input is the anchored norm: `D(x) ≤ 2t̄ = 2·49/14398580736`.
   - With `d(x,Y) ≥ d_Y+1`, this enters the data profile as `2t̄q·q^{d_Y}64^{d(x,Y)}`, which is far below `Kq^{d_Y}`.

   A packet that sets `D(x)=0` there is wrong for the fifth comparison, and for any comparison once x lies in the bigger box.
7. **R6. The normalization of intermediate regions (main reading; to be checked in the reverse).** The contract's reverse weights read "the diameter weight with support sizes charged per site through |I| ≤ 8·2^{diam I}". That controls the **count** of next-level straddlers. It does not control the **normalization** of an intermediate region S, the straddle part of a straddler.
   - Re-splitting the outside state with respect to S expands `X^{(S)}` over every family of supports meeting S. That produces `∏_{s∈S}(1+Σ_{J∋s}||c_J||)² ≈ e^{2t̄|S|}`, and for multi-straddler families another `e^{2σ|S|}`.
   - With |S| ≤ |J| ≤ 8·2^{diam J}, the factor `e^{16t̄·2^d}` overwhelms any diameter weight W^d ≤ w_max^d once d ≥ 33.
   - With |J| ≤ (1+d)³ it does so once d ≥ 34021.

   So a diameter-only recursion gives a constant that is not uniform in N; supports of diameter up to 2N+1 are allowed in Λ_N. Neither the contract nor the recorded preview structure (`η_str = 32T_*/(1−32T_*)`) charges this factor.

   The fix is cheap, and either route may use it:
   - a cardinality factor `e^{b|J|}` with b ≥ 2t̄ (the mixed-weight lemma, which the contract requires of the forward); or
   - a face-order count: owner sets have at most 3 sites, so `c_M` has Taylor order at least `⌈(|M|−1)/2⌉`. That gives `Σ_{J∋x,|J|=m}||c_J|| ≤ T(ρ)(|τ|/ρ)^{⌈(m−1)/2⌉}`, a BB1 lemma provable from the BA1 disc.

   I will require each packet to show where the intermediate normalization is charged. This is not blocking: nothing in the contract forbids the reverse from proving a cardinality control.
8. **R7. The split route's near term against the frozen `e^{|Y|/10^8}`.** Expanding `X¹−X²` over every family meeting Y gives `Σ_y D(y)·∏_y(1+t̄+D(y))`, which carries `e^{(t̄+Kq^{d_Y})|Y|}`.
   - At d_Y=0 the exponent is 4.417e-7. At d_Y=1 it is `t̄+Kq = 1.0252e-8`, just above 10^-8.
   - The frozen bound is trivially true once `c_site|Y|e^{|Y|/10^8}q^{d_Y} ≥ 2`. In the nontrivial range the excess factor is at most `e^{0.43} ≈ 1.54` at d_Y=0, and `e^{0.016}` at d_Y=1.
   - Both are absorbed by the margin 2.28: `2K·1.54 ≈ 1.35e-6 ≤ 2e-6`.

   A split packet must state this range argument or interpolate the coefficient change linearly. The derivative identity has no such factor.
9. **R8. The crude region constant cannot be written in the frozen form.** The crude anchored norm gives `β_crude = 2J e^{4b}G(R) ≈ 1.9e-5`, which exceeds 10^-8. Crude region constants are reported with their own exponent and labelled. `crude_majorant_tier_reported` never makes them targets.
10. **R9. The secondary input is a labelled re-instantiation.** At `ρ_2 = |τ|/q_2 = 1/151552` (not a gate radius), `K_2 = 2T(ρ_2) = 49/10202112`, which is exactly τ-invariant. `tier_mixing_rejected` admits it as "a labelled exact_first_order value" only if the packet proves Theorem 4.1 at that radius. Every step is the same, and `28ρ_2G(R) = 1/256 ≤ R`.
11. **R10. The fifth comparison and the untruncated passage.** For F1 general volumes, AM2 §6 covers every finite complete-factor volume, so AV1 F20–F23 applies. For F2 general volumes, the AY1 item-by-item list (|X|≤4, J≤28|τ|, termination, cutoff-vector removal) is gated for the centered Λ_N only.
    - The items are volume-independent, but the gate does not say so.
    - **Reading:** each packet re-verifies the items for the non-centered F2 volumes, or states the fixed-N untruncated form for those volumes as `limited`. The in-cutoff statement is unaffected.
12. **R11. "Exhibit exactly the finite fixtures named by the fixture controls" (required item 5)** applies to both packets whatever their route. The forward exhibits the split fixtures and the reverse exhibits the polymer identity, because each packet executes all 37 controls.
13. **R12. The mixed-weight loss.** `|M| ≤ |X|+Σ|I_j|` gives the frozen loss `w e^{4b}`.
    - It is attained only by the generic k=0 count (the 16 output sets of AM2's majorant).
    - For k≥1 the excess is at most 3. I enumerated 13 881 words of order at most 2 around the star.

    A packet may use `e^{4b}` throughout. `e^{3b}` for the k≥1 remainder is a valid refinement if it is labelled.
14. **R13. Cosmetic.** `selection-bb1.md` still says "the rate q=1/64" without "in N". It is a premise, left unchanged, with no effect.

## 3. Control mirror
- `controls` equals `preregistration.controls_required.ids`: 37 = 37, same order, no duplicates.
- 21 ids carry BB1 semantics.
- The other 16 are defined in the frozen BA1 contract, 15 of them also in BA2. So the plan rule "semantics for every id not defined in an earlier frozen contract" is met.
- The inherited BA1 texts fit BB1 as read here:
  - `parameters_declare_metric_weights_window` asks for metric, weights, window, clock and N_min, all present;
  - `tau_scaling_exponent` points to BB1's own brackets.
- The program implements all 37 as damaging mutations against a packet validator (106 mutations, 39 positives):
  - 14 required fixtures are exhibited, each labelled finite-graph and not transferring;
  - the second-order, split-charging, polymer-cardinality, global-fidelity and zero-free-region controls are decided against those exact fixtures, not flags;
  - positive cases (inequality digraphs, a negated forbidden phrase) must be accepted.
- Deferred parts are scope notes only:
  - the reverse inventory is synthetic in the program (the real inventories were hashed, §1);
  - the phrase scan and placeholder detector are mirrors of the tools;
  - tampering is checked at packet level;
  - the forward's far constant is not re-derived: its KP parameters are the producer's choice. Only KP feasibility, the mixed-weight loss and the recorded-preview structure are recomputed.

## 4. Are the frozen targets well-posed? Margins
Each target is an exact-rational upper bound on a trace norm, for every comparison, both signs, each Q_L and, at fixed N, the untruncated vectors. The exponents are exact: `d_R = N−1`, and `d_Y = N − max_{y∈Y}|y|_∞`. Every source site of every comparison satisfies |p|_∞ ≥ N, with equality attained (27 centered pairs on Λ_2..Λ_4 into Λ_5, plus general cuboids).

| constant (both signs; derivative near term, far factor A) | value | target | margin |
|---|---|---|---|
| C, every-site form (b), u=0 at q^N | ≈ 8.9035e-7 | 1/250000 | 4.4926 |
| C, BA1 gate statement at both sites of R | ≈ 1.7533e-6 | 1/250000 | **2.2814** |
| C, form (a) K_own (labelled) / K_gen (labelled) | ≈ 4.4800e-7 / 4.5511e-7 | 1/250000 | 8.93 / 8.79 |
| C, split (sine bound), every-site / R-only | ≈ 8.9034e-7 / 1.7533e-6 | 1/250000 | 4.4927 / 2.2814 |
| recorded preview structure, split / polymer (R-only) | 352765230433/201124673670833280 ≈ 1.7540e-6 / ≈ 1.7536e-6 | 1/250000 | 2.2805 / 2.2810 |
| c_site, form (b) | ≈ 8.7664e-7 | 1/500000 | **2.2814** |
| c_site, form (a) | ≈ 4.4110e-7 | 1/500000 | 4.534 |
| secondary C_2, every-site / R-only | ≈ 9.6213e-6 / 1.9213e-5 | 1/20000 | 5.197 / 2.6025 |
| secondary c_site,2 | ≈ 9.6063e-6 | 1/40000 | 2.6025 |
| density union (factor 2), C every-site / R-only / c_site | ≈ 1.7807e-6 / 3.5066e-6 / 1.7533e-6 | — | labelled only (2.25 / 1.14 / 1.14) |
| crude tier, C every-site / R-only | ≈ 1.5624e-3 / 3.0542e-3 | 1/250000 | fails, retained |

- The margin-2 rule holds for every frozen pair at the worst admitted input.
- The union comparison shows why the contract made the fifth comparison direct: through the union, the R-only C has margin 1.14.
- Proof weights: θ = 1/q = 64 and e^b = 9/8 give a loss of 6561/64 = 102.5 ≤ w_max = 390625/148. The secondary uses θ_2 = 390625/592, giving a loss of 1056.9. Both lie inside the weighted self-map, as `rate_constant_pair_prefrozen` requires.

**Scaling (exact ratios, same formula).**
- C and c_site: about 100.63 (form (a) 101.26), inside [95,105].
- The input ratio is `4340004/43129` exactly.
- Secondary constants: 1.0015 and 1.0000, inside [99/100, 101/100]; the secondary input is exactly τ-invariant.
- q_2: exactly 100.
- A first-order-cancellation refinement is quadratic in τ (ratio about 10^4). It must be labelled and not tested against the linear bracket.

## 5. What the every-site coefficient input requires
**Form (b), the reverse theorem restated at every u.** It is a BB1 lemma and must be proved in full. The BA1 gate admits u ∈ R only.
1. **Lemma 2.2 with M ∋ u.** A nonzero order-n term on M ∋ u whose family contains a source piece Y has `n ≥ 1 + ⌈d_∞(u,Y)/diam⌉`. The contract form drops the 1.
2. **The source-site lemma.** Every face present in one volume and not the other has all its sites at |p|_∞ ≥ N. The cases:
   - new F1 stars have some b_i ∈ {N, −N−1};
   - new F2 owner sets meet |p_i| = N+1 and have diameter 1;
   - the extra F2 faces of F1 against F2 share p_i = N;
   - symmetric differences of volumes containing Λ_N contain a site outside Λ_N.

   Hence `d_∞(u, sources) ≥ N−|u|_∞`. It is attained, for example along the z-axis.
3. **The circle bound.** 2T(ρ) is uniform in u, because the anchored norm is a maximum over u.
4. **Schwarz.** `Σ_{I∋u}||δ_I|| ≤ 2T(64|τ|) q^{N−|u|_∞} = K q^{N−|u|_∞}`, with K = 49/111790368, in each Q_L, both signs, every comparison.

**Form (a).** Cite the BA1 forward's max-over-u norm bound, whose proof is every-site. Name B and `d_∞(u,B)` per comparison (R4). Label K_own or K_gen as weighted_norm values.

**Both forms.** Outside Λ_N, charge the anchored norm 2t̄ (R5). Never use the R-only gate statement at far sites.
