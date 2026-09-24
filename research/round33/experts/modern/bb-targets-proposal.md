# BB1/BB2 frozen-target proposal (modern lens, Round33)

**Status.** This file is advisory. It admits nothing and counts zero research loops. It is not a contract, a premise or a gate.

**Author.** Human project author: Hruday N M (BUNZEEY). This lens is a model agent with ancestry shared with every other agent in the round, so this is not external review.

**Distribution.**
- Sections 1–6 are written so that the advisor can copy them into the BB1/BB2 contracts. They carry target values but no previews or margins.
- Section 7, **previews (advisor only)**, holds every preview number and margin. It must stay out of producer inputs.
- Under plan rule P7, the **BB1 reverse producer must not receive this file**, just as it receives neither the modern memo nor the skeptic triage.

**Read for this proposal:**
- the frozen BA1 outputs (forward and reverse `output/results.json` and `report.md`);
- the frozen BA2 outputs (forward and reverse `output/results.json`);
- the BA1 and BA2 contracts;
- `advisor/plan.json` (vocabulary, contract rules, history);
- `advisor/deliberation-2.md` (P1–P13, especially P6 and P7);
- the skeptic's triage, §(a).4–(a).8 and the fixture list.

The BA1 and BA2 gates are still pending the skeptic's post-comparison review. Every target below assumes those gates will admit what the producers proposed. §6 covers what changes if they do not.

---

## 1. Parametrization (item a)

**Headline rate for both loops: `q = 1/64`, the BA1 headline rate.**
- Both BB1 routes reach this rate using only BA1 constants plus one weighted-norm bound taken at a larger weight. That bound is BA1's own weighted-norm lemma at `w ≤ 1/(37888|tau|)`, which is monotone in `w`.
- Every constant carries the tier `exact_first_order`. A `crude_majorant` value is reported, never a target.
- Routes, from the closed vocabulary:
  - **BB1 forward:** `polymer_kp`. Polymer representation of the normalized creation-product state, with a Kotecký–Preiss condition checked with explicit constants.
  - **BB1 reverse:** `iterated_split`. The AV1 product-ordering split, applied recursively to the outside state.
  - **BB2:** each constant carries the tier and route of the input it assembles.
    - The state constants carry `exact_first_order` with `polymer_kp` or `iterated_split`, whichever BB1 input the producer uses.
    - The dynamics constant carries `polynomial_lieb_robinson` with `duhamel_inner_f1` or `duhamel_inner_f2` (BA2).
    - The assembly method is recorded in a separate `assembly` field: `nested_telescoping` (forward) or `union_comparison` (reverse). If the advisor wants these as route labels, the vocabulary must be closed first (Round32 rule R10); they are not in plan.json today.

**Why not the floor rate `q_min = 148/390625` (= `37888|tau|`).** Neither route reaches the floor for reduced densities. Both routes have to spend some of the weight range that BA1 used up entirely at `q_min`:
- **Iterated split.** The straddling recursion charges the size of each straddling support. The only admitted size control is the diameter, with `|I| ≤ (1+diam I)^3 ≤ 8·2^{diam I}`. So the creations must be measured at weight `2/q`, which must be at most `1/(37888|tau|)`. That forces `q ≥ 2 q_min`.
- **Polymer / KP.** The far-support sum over sites at distance `d` from `R`, with `24d²+8d+2` sites per ℓ∞ shell, converges only if the cluster weight `W_c` satisfies `q W_c > 1`. The KP tree bound also needs a cardinality factor `e^{b|I|}` on top of the diameter weight. So `q > q_min e^{4b}`, and at `q = q_min` the sum diverges.

A floor pair frozen at `q_min` would therefore be an expected failure, so it should not be frozen.

**Why not my loop-1 polymer rate `56832|tau|` (= `1.5 q_min`).** That rate used the star-count weight, where `|I| ≤ 4 n(I)` is linear. BA1 admitted the **diameter** weight, for which `|I|` is cubic in the diameter. At `1.5 q_min` the split route would need weight `2/q > 1/(37888|tau|)`, which is not admissible. I withdraw that rate as a target.

**Optional secondary pair, if the advisor wants a member that scales with `tau`: `q_2 = 4 q_min = 151552|tau|` (= `592/390625` at the cap).**
- Both routes have room there.
- The split needs weight `2/q_2 = (1/2)·1/(37888|tau|)`.
- The polymer route needs `q_2 W_c = 2` with `W_c = (1/2)·1/(37888|tau|)`.
- The constants are `tau`-invariant at leading order, like BA1's floor constant.
- Freeze it only as a labelled secondary pair. The headline pair decides the loop.

---

## 2. BB1 — marginal locality (frozen targets, item c)

**Objects.** Fix a sign of `tau` with `|tau| ≤ 10^-8`, and fix a BA1 comparison with smaller box size `N ≥ 2`. The comparisons are:
- F1 `Lambda_N` against `Lambda_{N+1}`;
- F2 `Lambda_N` against `Lambda_{N+1}`;
- F1 against F2 on the same `Lambda_N`;
- any two centered boxes `Lambda_M`, `Lambda_{M'}` with `M, M' ≥ N`, of F1 or F2;
- labelled: two finite complete-factor volumes of one prescription, both containing `Lambda_N`, compared through their union.

`rho^{box}_Y` is the reduced density on a finite complete-factor region `Y` of the normalized finite-box ground vector. It is evaluated in each on-site cutoff space `Q_L` and, at fixed `N`, for the untruncated ground vector after the AV1 cutoff-vector removal (F20–F23).

**Target BB1-T1 (headline, `q = 1/64`).** For every comparison above, both signs, every `L`, and at fixed `N` for the untruncated vectors:

`||rho^{box1}_R − rho^{box2}_R||_1 ≤ C q^(N−1)`, with `q = 1/64` and `C ≤ 4·10^-6` (= `1/250000`).

The norm is the trace norm on `B(H_R)`, with `R = {0, e_z}`. The tier is `exact_first_order`. The route is `polymer_kp` (forward) or `iterated_split` (reverse). One `C` must cover every comparison.

**Target BB1-T2 (region form; needed by BB2 items 3–5).**
- Let `Y ⊂ Lambda_N` be a finite complete-factor region, and put `d_Y = N − max_{y∈Y} |y|_∞`. This is the ℓ∞ distance from `Y` to the outer layer `max_i |b_i| = N`; it gives `d_R = N−1`.
- For every comparison above: `||rho^{box1}_Y − rho^{box2}_Y||_1 ≤ c_site |Y| e^{|Y|/10^8} q^{d_Y}`, with `c_site ≤ 2·10^-6`.
- The same tier and route vocabulary applies.
- The factor `e^{|Y|/10^8}` is frozen as written. It absorbs the growth of the region normalization in the split route, where the unweighted anchored norm is at most `10^-8` per site.

**Target BB1-T3 (optional secondary pair, labelled).** Items T1 and T2 with `q_2 = 151552|tau|`, `C_2 ≤ 5·10^-5` and `c_site,2 ≤ 2.5·10^-5`.

**Required derivations.**
1. The exact AV1 decomposition `rho_Y = N_c(omega_O)/Tr N_c(omega_O)`, where `omega_O` is the outside marginal on the straddle region. Prove `Tr N_c ≥ 1` by the AV1 orthogonality (F09), and prove the two Lipschitz bounds, one in the coefficients and one in `omega_O`.
2. **Reverse (split).** The straddling recursion must charge **per site**, with each support's size charged to the weight through `|I| ≤ 8·2^{diam I}`. It must never charge the product of growing shell sizes. Multi-support families (two or more straddling supports) must be bounded explicitly.
3. **Forward (polymer).** Derive the hard-core polymer representation of `⟨psi,psi⟩` and `⟨psi,A psi⟩`: polymers are overlap-connected pairs `(F,F')` of families of disjoint supports with the same excitation set. Give the activity bound `|w(gamma)| ≤ prod_{I∈F⊔F'} ||c_I||`, and state the KP condition with an explicit `a`, weights, and the tree majorant.
   - The needed cardinality control is a **new lemma**: the BA1 contraction with the mixed weight `w^{diam I} e^{b|I|}`, with loss `w e^{4b}` per interaction. Prove it in full, not by analogy.
   - Use the real-parameter derivative along `c + lambda(c' − c)`: `∂psi = −δ̂ psi`, because `δ̂_I ĉ_I = 0`.
   - No analyticity of `rho_R` in the coupling may be claimed without a proved zero-free region (P7).
4. Both routes must use the BA1 coefficient differences at **every** site, not only on `R`. They may use the forward boundary-weighted norm, or the reverse disc theorem re-stated for every `u` with vanishing order at least `1 + d(u,B)`. State which, and re-derive it if it is not in the admitted report.
5. Pass the bound from `Q_L` to `L → ∞` at fixed `N` (AV1 F20–F23, untruncated gap 1/2 in each box). Never take `N → ∞` inside a fixed `Q_L`.
6. Report the crude tier separately, and never use the global Lipschitz constant as a decay factor.

**Gate fields.**
- `state_decay_claimed: true`, with the scope "reduced densities of F1/F2 finite-box ground vectors on R and on regions Y, per comparison".
- `rate_in_N_claimed: true`.
- False: `whole_sequence_claimed` (BB2), `common_limit_claimed` (BB2), `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `continuum_claim`, `translation_invariance_claimed` and `weak_coupling_claim`.

**Suggested mandatory sentence template** (checked against the forbidden list):

> For the zero-selected patterned family at the same coupling |tau|<=10^-8, and for every comparison of the named construction families F1 and F2 on centered coarse cubes, the reduced densities of the finite-box ground vectors on the cover R differ by at most C q^(N-1) in trace norm, in each on-site cutoff space and, at fixed N, for the untruncated ground vectors, where N is the smaller box size; this is locality of the reduced densities of the named constructions at a rate in N, not uniqueness of any ground state, not a statement about other boundary conditions, and not a statement uniform in the lattice spacing a.

---

## 3. BB2 — whole-sequence convergence, common limit, identification, translations, correlations (frozen targets, item c)

**Item 1 — whole-sequence Cauchy estimate** (the quantifier is over all `M` above `N`, per plan). For `F ∈ {F1, F2}` and `N ≥ 2`:

`sup_{M>N} ||rho^{F,M}_R − rho^{F,N}_R||_1 ≤ C' q^(N−1)`, with `q = 1/64` and `C' ≤ 4·10^-6`.

The same holds on regions `Y`, with `c_site |Y| e^{|Y|/10^8} q^{d_Y}` and `c_site ≤ 2·10^-6`. Hence the limit `rho^∞_Y` exists without compactness, and `||rho^{F,N}_Y − rho^∞_Y||_1` obeys the same bound.

**Item 2 — common limit.** The F1 and F2 limits coincide on every finite region `Y` (from BB1 same-`N` comparison and item 1). The limit is written `omega_inf`, with the wording "the limit of the named constructions" (P1).

**Item 3 — identification.**
- `omega_inf` equals every AQ1 subsequential limit (F1) and every F2 subsequential limit (AY1), on every finite region.
- It therefore inherits AQ1's stationarity, GNS continuity and `H_num ≥ 0`, and AQ2's gap `alpha/16` and vacuum simplicity, in its own GNS representation.

**Item 4 — coarse translation invariance** (pre-registered; dropped and recorded as a limitation if BA1's general-volume comparison is not admitted, P6).
- For every coarse translation `v`, meaning a fine translation `(4v_x, 2v_y, v_z)` that preserves residues and face classes, `omega_inf ∘ T_v = omega_inf`.
- Quantitatively, for `N ≥ |v|_∞ + 2`: `||rho^{Lambda_N+v}_R − rho^{Lambda_N}_R||_1 ≤ C q^(N−|v|_∞−1)`. This is the BB1 general-volume comparison applied with `Lambda_{N−|v|_∞}`.
- A translation that breaks the residues is a rejected control.

**Item 5 — correlation functions on compact windows** (uses BA2).
- Definitions:
  - `c^{F,N}_A(theta) = omega^{F,N}(A* T^{F,N}_theta(A)) − |omega^{F,N}(A)|^2`;
  - `c^inf_A(theta) = omega_inf(A* T_theta(A)) − |omega_inf(A)|^2`, where `T_theta` is the AQ1 limit dynamics, which BA2 identifies with the F2 limit;
  - `theta = alpha t/hbar`.
- For `F ∈ {F1, F2}`, `N ≥ 5`, `r_N = floor((N−1)/2)`, `|theta| ≤ 8` and `A ∈ B(H_R)`:

  `|c^{F,N}_A(theta) − c^inf_A(theta)| ≤ ||A||^2 [ C_dyn/(r_N − 1) + c_site |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N − r_N) + 2 C' q^(N−1) ]`

  with `C_dyn ≤ 5·10^-10` (tier `polynomial_lieb_robinson`, route `duhamel_inner_f1` or `duhamel_inner_f2`, inherited from BA2) and `c_site`, `C'` as above.
- `r_N` is frozen as written; no post-hoc choice.
- The derivation route is:
  - Approximate `T_theta(A)` and `T^{F,N}_theta(A)` by the `Lambda_{r_N}` box evolution `T^{F1,r_N}_theta(A)`, using the BA2 within-family Cauchy and comparison bounds together with `(5r+1)/r^3 ≤ (11/8)/(r−1)` for `r ≥ 2`.
  - Use the region form on `Lambda_{r_N}`.
  - Use the complex-mean centering `|omega(A)|^2`.
- The rate is O(1/N), the honest rate for a polynomial `F`. There is no uniform-in-time claim, and no equality of GNS dynamics of different states.

**Optional secondary pair.** Items 1 and 4 with `q_2 = 151552|tau|`, `C'_2 ≤ 5·10^-5` and `c_site,2 ≤ 2.5·10^-5`.

**Gate fields.**
- `whole_sequence_claimed: true`, with `whole_sequence_scope` = "reduced densities of the named constructions F1 and F2 on every finite region".
- `common_limit_claimed: true`.
- `state_convergence_claimed: true`.
- `translation_invariance_claimed: true` only with the scope "coarse translations; the limit of the named constructions".
- `rate_in_N_claimed: true`.
- `dynamics_level: correlation_functions_compact_window`. This is a new value; add it to plan.json before freeze.
- False: `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `continuum_claim`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed` and `weak_coupling_claim`.

**Suggested mandatory sentence template:**

> For the zero-selected patterned family at the same coupling |tau|<=10^-8, the reduced densities of the named construction families F1 and F2 on centered coarse cubes converge as whole sequences, at a rate in N, to one common limit on every finite region; this limit coincides with every AQ1 subsequential limit and every F2 subsequential limit, is invariant under coarse translations, and has as correlation functions on |theta|<=8 the limits of the finite-box correlation functions; this is convergence of the named constructions, not uniqueness of any ground state, not a statement about states outside the named constructions, and not a statement uniform in the lattice spacing a.

---

## 4. Scaling brackets per constant (item d)

The check is `tau → tau/100`, declared before production.

| constant | tau order | bracket | reason |
|---|---|---|---|
| `C` (BB1-T1), `C'` (BB2 item 1), `c_site` (T2 and item 1) at `q = 1/64` | linear | `[95,105]` | `q` is fixed. The constants are BA1's exact-first-order constants (linear in `tau`, with a positive nonlinear correction from `1/(1−Γ)^k`) times factors `1 + O(tau)`. |
| `q = 1/64` | fixed | exactly 1 | the frozen headline rate |
| `C_dyn` (BB2 item 5) | quadratic | `[9500,10500]` | inherited from BA2 (quadratic in `tau`) |
| `C_2`, `C'_2`, `c_site,2` at `q_2 = 151552|tau|` | q-dominated | `[99/100, 101/100]` | `w t_1` and `J w` are invariant at `w = 1/q_2`, so the constants are `tau`-invariant at leading order, like BA1's floor constant |
| `q_2` | linear | exactly 100 | `151552|tau|` |

The item-5 bound is a sum of a quadratic part (`C_dyn`) and linear parts (`c_site`, `C'`). **No single bracket may be declared for the sum.** Each constant is checked separately, which is why item 5 keeps three named constants instead of one lumped constant.

---

## 5. Exact finite fixtures that must be required (item e)

Every fixture is labelled `model_is_finite_graph: true` and `transfers_to_aq: false`. Each one carries a damaging mutation that `check.py` must reject.

1. **Coefficient decay is not marginal decay (mandatory, P7).** Use the AV1-F13-type qubit fixture: sites `r, o, o'` with `R = {r}`, straddling `c_{r,o} = 1/3`, and `c_o` changed from `1/2` to `0`.
   - Every coefficient on a support meeting `R` is unchanged.
   - `rho_r` moves from `[[45/49,6/49],[6/49,4/49]]` to `[[9/10,0],[0,1/10]]`.
   - Rejected: the inference "coefficients meeting R unchanged, so the marginal is unchanged".
2. **Second-order propagation (order counting).** Use a chain `r – o – o''` with straddling creations `c_{r,o}` and `c_{o,o''}`, and change only `c_{o''}`.
   - The `R`-marginal moves exactly at the order of the product of the two straddling amplitudes. Verify it exactly as a polynomial.
   - Rejected: first-order propagation claims, and a bound whose per-link factor is below the exact one.
3. **Normalization coupling.**
   - Spectator independence: `rho_R` is fixed, while the unnormalized weights run through AV1's four values `145/144, 5365/5184, 198505/186624, 7344685/6718464`.
   - A **global-fidelity** fixture: the overlap of the two normalized vectors decays geometrically in the number of spectators whose coefficient changes, while the `R`-marginal difference stays fixed. This rejects every route through the global overlap and every numerator-only route.
4. **Straddling supports.**
   - A straddling creation enters `e^2` at first order but the off-diagonal marginal element only at second order (AV1 F13 (iii)).
   - One-site straddling first-order faces have zero `R`-marginal (Haar), while supports strictly containing `R` do not.
   - Rejected: dropping straddling supports from the split, and charging them only at first order.
5. **Split route.**
   - `Tr N_c(omega) ≥ 1` and the Lipschitz inequality `||rho(omega) − rho(omega')||_1 ≤ 2||N(omega − omega')||_1`, checked exactly on a mixed outside state.
   - A fixture where charging the product of growing region sizes gives a bound that increases with depth, while per-site charging gives a convergent geometric bound. The first is rejected.
6. **Polymer route.**
   - Brute-force `⟨psi,psi⟩` on a four-site collection equals the polymer sum.
   - Pairing families with different excitation sets gives zero.
   - A tree-majorant fixture shows that dropping the cardinality factor `e^{|I|F}` underestimates the cluster sum. That mutation is rejected.
   - A zero-free-region control: an "analytic `rho_R`" claim without a proved zero-free region is rejected (P7).
7. **Cutoff order.**
   - Reuse the AV1 Eckart fixture (the `3×3` rational fixture with gap `1/2`).
   - A mutation that swaps the order of the `N` and `L` limits is rejected.
8. **Whole sequence against subsequence.**
   - A sequence satisfying a one-state ball in every box with two distinct subsequential limits is rejected as "convergence".
   - An `N → N+1` bound alone is rejected as a Cauchy estimate.
9. **Translations.**
   - A non-coarse fine translation breaks residues and must be rejected.
   - A translated box sequence is compared only through the general-volume comparison.
10. **Correlation functions.**
    - Polynomial against exponential Lieb–Robinson tail.
    - A moving-mean fixture with complex means (`|omega(A)|^2`, not `omega(A)^2`).
    - A post-hoc choice of `r_N` is rejected.

---

## 6. Risks and retained-failure outcomes (item f)

**Risks:**
1. **The BA1 and BA2 gates are pending.** The targets assume both BA1 routes' constants and both BA2 routes' constants are admitted. If only one route is admitted per loop, the relevant input constant can only get smaller, so the targets remain valid. If BA1's general-volume comparison is not admitted, BB2 item 4 is dropped (P6).
2. **The polymer route needs cardinality control that BA1 did not admit.** The diameter weight alone does not dominate `e^{|I|F}` once supports have diameter in the thousands. The mixed-weight contraction is a new lemma. It is short, since `|M| ≤ |X| + sum_j |I_j|`, but it must be proved in full.
3. **The split route can hide region dependence.** Charging whole regions level by level gives factorial growth. Only per-site charging with the diameter weight closes. Multi-support straddling families must be written out.
4. **Reverse BA1 states its bound only for `u ∈ R`.** Far-site differences need either the forward boundary-weighted norm (all `u`) or a restatement of the disc theorem at every `u`. If neither is available, BB1 is `limited`.
5. **Normalization traps:** global-overlap and numerator-only arguments (fixture 3).
6. **Unproved analyticity of the reduced density** (P7).
7. **Correlation functions.** The BA2 rate is polynomial, so the convergence rate is O(1/N). At small `N` the state term of item 5 is comparable to the dynamics term, which is why the constants are kept separate.
8. **The secondary pair sits closer to the routes' limits.** The polymer far-support factor is about 100 times larger there than at `q = 1/64`. It may end `limited` while the headline stands.
9. **Label drift.** Every phrase on the `vocabulary.forbidden` list of `advisor/plan.json` is excluded, and "rate" is always qualified "in N". The limit is always "the limit of the named constructions".

**Retained outcomes:**
- **BB1**
  - `accepted_within_scope`: T1 and T2 are proved by both routes at or below the frozen values.
  - `limited`:
    - only the `R` form (T1) is proved, without T2 (then BB2 items 3–5 are restricted to `R` and item 5 is dropped); or
    - only the near-support part is proved (supports meeting `Y`), with no control of the far supports.
  - `insufficient`: neither route controls the outside-state dependence. Coefficient decay (BA1) still stands, labelled as such.
- **BB2**
  - `accepted_within_scope`: items 1–5 are proved.
  - `limited`: item 4 is dropped under P6, or item 5 is dropped because T2 is missing. Each drop is recorded.
  - `insufficient`: BB1 is insufficient.
- **Either loop:** a failed route is never evidence that two limits differ. Nothing is retuned: not `q`, not `r_N`, not `a`, not the weights, not `tau`.

---

## 7. Previews (advisor only; item b) — not for producer inputs

All values are at `|tau| = 10^-8`. Both signs replay the same `|tau|` formula. The admitted-candidate inputs are:

| symbol | meaning | value |
|---|---|---|
| `t̄` | unweighted exact-first-order anchored norm | `49/14398580736 ≈ 3.4031e-9` |
| `T_*` | weighted norm at the maximal weight (BA1 exact_first_order, `w = 390625/148`) | `49/4036608 ≈ 1.21389e-5`; bounds every weighted norm with `w ≤ 390625/148` |
| `K_gen^fwd` | BA1 forward, general comparison, at `e_z` | `2734375/12204185915601 ≈ 2.24052e-7`; at site `0` one extra factor `q` |
| `K_rev` | BA1 reverse, contract form, same at both sites of `R` | `49/111790368 ≈ 4.38320e-7` |

Write `δ̄_u` for the BA1 bound on `sum_{I∋u} ||c^1_I − c^2_I||` divided by `q^(N−1)`.

**Iterated-split route: normalization and straddling constants.**
- **Normalization / coefficient term.**
  - The pure-state sine bound, together with `||X φ̂|| ≥ 1`, gives `||rho_{c^1}(omega) − rho_{c^2}(omega)||_1 ≤ 2||X^1 − X^2||`.
  - For `R`, `||X^1 − X^2|| ≤ (δ_0 + δ_{e_z})(1 + 2t̄)`.
- **Straddling term.**
  - `||rho(omega) − rho(omega')||_1 ≤ 2(2(1+2t̄) + s) s · D`.
  - Charge per site with `|I| ≤ 8·2^{diam I}`, at creation weight `2/q ≤ 390625/148`, bounded by `T_*`.
  - The relative factor per recursion level is at most `32 T_*`, so the straddle series gives `eta_str = 32T_*/(1 − 32T_*) = 49/126095 ≈ 3.886e-4`.
- **Assembly:** `C_split = 2(δ̄_0 + δ̄_{e_z})(1 + 2t̄)(1 + eta_str)`.
  - With forward inputs (`δ̄_{e_z} = K_gen^fwd`, `δ̄_0 = q K_gen^fwd`): `255912276541796875/562095032088559080946176 ≈ 4.55283e-7`.
  - With reverse inputs (`δ̄_0 = δ̄_{e_z} = K_rev`): `352765230433/201124673670833280 ≈ 1.753963e-6`.

**Polymer route: KP condition, activity bound and resulting C.**
- **Activity:** `|w(gamma)| ≤ prod_{I∈F⊔F'} ||c_I||`.
- **KP weight and parameters:**
  - weight `e^{a|X_gamma| + mu diam X_gamma}`, with `a = 1/1000` and `e^mu = W_c = (1/2)·390625/148 = 390625/296`;
  - cardinality factor `e^{b|I|}` with `e^{4b} ≤ 2` and `b ≥ a/2 + F`;
  - mixed-norm stand-in `T_KP = 2T_*`.
- **KP sum:** at most `4T_KP = 49/504576 ≈ 9.71e-5 ≤ a`, about 10 times below `a`.
- **Near supports:** from `∂psi = −δ̂ psi`, the bound is `2||A|| ||δ_I|| (1 + t̄)`, using the AW1 amplitude lemma for `|omega(δ̂_I)|`.
- **Far supports:**
  - `eta_far = e^{2a} · 4T_KP · S(q W_c)/(1 − 4T_KP)`, where `S(x) = sum_{d≥1} (24d²+8d+2) x^{−d}` counts the ℓ∞ shells around `R`.
  - At `x = q W_c = 390625/18944 ≈ 20.62`, `S = 99977074261152768/51346528044814241 ≈ 1.9471`, so `eta_far ≈ 1.895e-4`.
- **Result:** `C_poly = 2(δ̄_0 + δ̄_{e_z})(1 + t̄)(1 + eta_far)`. With forward inputs this is about `4.55192e-7`; with reverse inputs, about `1.753614e-6`.

**Margins at `q = 1/64`** (margin = target over the larger preview):

| constant | worst preview | target | margin |
|---|---|---|---|
| `C` (BB1-T1) | `1.753963e-6` (split, reverse BA1 input) | `4·10^-6` | 2.2806 |
| `C'` (BB2 item 1, nested telescoping, `C/(1−q)`) | `50395032919/28283157234960930 ≈ 1.781804e-6` | `4·10^-6` | 2.2449 |
| `c_site` (per site, with the `1/(1−q)` Cauchy factor) | `8.909018e-7` | `2·10^-6` | 2.2449 |
| `C_dyn` (BB2 item 5): `K_c2 + K_c1 + (11/8)K_cmp` with the larger BA2 value of each | `2.315150e-10` | `5·10^-10` | 2.1597 |

The `C_dyn` inputs are `K_c2 = 117747/1245766400000000` (forward), `K_c1 = 1.01951e-10` (reverse) and `K_cmp = 3969/155720800000000` (forward); the exact sum is `175777236988465912821/759247655761718750000000000000`. The F1-only value is `2K_c1 ≈ 2.03903e-10`.

**Item-5 term sizes by `N`** (at the worst constants):

| `N` | `r_N` | dynamics term | state term | mean term |
|---|---|---|---|---|
| 5 | 2 | `2.32e-10` | `4.25e-10` | `2.1e-13` |
| 6 | 2 | `2.32e-10` | `6.6e-12` | — |
| 7 | 3 | `1.16e-10` | `1.8e-11` | — |
| 9 | 4 | `7.7e-11` | `6.0e-13` | — |

At `N = 5` the state term exceeds the dynamics term, so the constants must stay separate.

**Previous panel figures.** The skeptic's triage had `C_rho = 4K ≈ 8.80e-7`, `C_inf ≈ 8.94e-7` and the BB2 candidate `2·10^-6`. Those were built on the loop-1 BA1 preview `K ≈ 2.2e-7`. The admitted reverse BA1 constant is about twice that (`4.38e-7`), and producers may use it in contract form at both sites. **A `2·10^-6` target would then have margin of only about 1.14. Do not freeze it.**

**Secondary pair `q_2 = 592/390625`:**

| constant | worst preview | target | margin |
|---|---|---|---|
| `C_2` | `1.951458e-5` (polymer, reverse input; `eta_far ≈ 1.58e-2` since `S(2) = 162`) | `5·10^-5` | 2.562 |
| `C'_2` | `1.954420e-5` | `5·10^-5` | 2.558 |
| `c_site,2` | `9.772e-6` | `2.5·10^-5` | 2.558 |

**Crude tier (report only, not a target), at `q = 1/64`:**
- reverse crude input `296/390625` gives `C ≈ 3.03e-3`;
- forward crude general input gives `C ≈ 7.87e-4`.

**Scaling previews (`tau → tau/100`):**
- headline `C`, `C'`, `c_site`: 100.63 (reverse input) to 101.28 (forward input), inside `[95,105]`;
- secondary constants: 1.0000 to 1.0030, inside `[99/100, 101/100]`;
- `C_dyn`: the BA2 ratios, about 10020–10034, inside `[9500,10500]`.

**Recommendation.** Freeze the headline pair `q = 1/64` with:
- BB1: `C ≤ 4·10^-6` and `c_site ≤ 2·10^-6`;
- BB2: `C' ≤ 4·10^-6`, `c_site ≤ 2·10^-6` and `C_dyn ≤ 5·10^-10`.

Freeze the secondary pair `q_2 = 151552|tau|` (`C_2`, `C'_2 ≤ 5·10^-5`; `c_site,2 ≤ 2.5·10^-5`) only as a labelled extra.

This lens admits nothing and counts zero research loops.
