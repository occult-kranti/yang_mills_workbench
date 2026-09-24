# AY2 independent derivation (skeptic, before comparison)

**Standing.** I wrote this after the AY2 contract froze (`frozen_at` 2026-09-24T03:09:12Z, sha256 `8e55e8e9…6b38`). AY2 has a single forward producer, so this package is a required admission input (`single_direction_independent_replay`).

**Sources.** I worked from:
- the frozen contract and `selection-ay2.md`;
- `advisor/ay1-gate.json` (sha256 `d1d3f921…78e5`, pinned) and the other Round32 gates;
- the AY1 forward and reverse reports, `check.py` and `output/results.json`;
- my `ay1.md`, `ay1.json`, AY1 pre-comparison package, `triage.md`, `prospective-controls.json` and `loop2-response.md`;
- the Jung loop-2 response;
- the AM2 forward report and gate, AQ1 §2–5, AQ2 §6 and I1 §5–6;
- for background only, the Round29 AN1/AN2 gates and `experts/an-source-dictionary.md`, which are not AY2 premises;
- AGENTS.md.

**Isolation.**
- I did not open, list or read anything under `research/round32/forward/ay2/` except `inputs/`. There I listed the file names with `find`: 23 files, equal to AGENTS.md, the contract and the 21 shared premises.
- I hashed those 23 files against their repository sources, and all are byte-identical. I opened none of them. The same 23 files are ones I read at their repository paths.
- **Incidental exposure.** After this package was written, two `git status` runs showed the names, and only the names, of untracked producer paths: `research/round32/forward/ay2/check.py` and `report.md`, and in the second run also `freeze.json` and `output/`. The producer was therefore working in parallel. I opened none of them, and nothing in this package was changed in response, apart from this disclosure line and the matching `incidental_exposure` string in the checker output.

**Scratch.** All scratch work (the integrator tests, the source-edit harness and the replays) stayed in `/tmp/claude-0/skeptic-ay2-private/`. I read nothing in other agents' scratch folders or in the shared scratchpad root.

**Correlated ancestry.** I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producer. My triage seeded the 2D observation. My AY1 review, a shared premise, lists the obligations. My AY1 pre-comparison first printed the two-sided tier. This is re-derivation, not independent discovery or human review.

**Exactness.** Exact values come from `ay2_check.py`: 82 checks and 29 controls (the 21 contract ids plus 8 extra), with 88 rejected mutations, 73 of them inside the contract controls. Every decimal below is a preview. Human project author: Hruday N M (BUNZEEY).

## 1. What AY1 admitted (the statement AY2 must make)

**Model.** `AQ_patterned_zero_selected`:
- SU(2) Kogut–Susskind form on Z³ at fixed spacing, with 24-link factors;
- selected triple exactly `(0,0,0)`, with Haar reference `P_R`;
- 21 omitted faces per anchor, each entering as `−(tau/3)W_f`;
- both signs of τ, `|tau|<=10^-8`;
- cover `R={0,e_z}`: 48 links, 36 endpoints, 7 incident anchors;
- families F1 (AQ1 centered whole-star boxes) and F2 (I1 §6 all-contained-face boxes with padding), on the same `Lambda_N=[-N,N]^3` with `N>=2`.

**Template.** The mandatory template, quoted from the AY1 gate (it is not in the AY2 preregistration; contract review item 5), with its constants filled in:

> For every pair of subsequential limits of the named construction families F1 and F2 at the same coupling, on the fixed cover R and for the frozen observable class, the reduced densities satisfy `||rho_R - rho'_R||_1 <= 2D` and agree to first order in tau; this does not assert equality of the states, whole-sequence convergence, translation invariance, boundary independence of the dynamics, or a rate in N.

**Constants.**
- `2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257` ≈ 2.72249057405e-8.
- The common first-order density is `rho^(1)_R=(tau/72)Σ_{f∈F_R}(|W_fΩ_R⟩⟨Ω_R|+h.c.)` over the 10 faces with owner set exactly R.
- For every chosen subsequential limit of either family, `||rho_R-P_R-rho^(1)_R||_1 <= K_2'tau^2`, with `K_2' = 966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000` ≈ 13417.5275440.
- Hence any two limits at the same τ satisfy `||rho_R-rho'_R||_1 <= 2K_2'tau^2` ≈ 2.68350550880e-12.

**Recomputation.** The checker reads these constants as exact rationals from the pinned gate. It then recomputes:
- `K_2'` from the gate's own item formula (`4rho+2T(72a+2rho)+2(33a+rho)^2+2eps_R^2+20a·eps_R^2`, `a=|tau|/144`, `T=49a/(1-352J)`, `rho=352JT`, `J=28|tau|`);
- `D` from `eps_F=2T+T^2`;
- `K_2^+`.

All three agree to the rational.

## 2. The trace norm of rho^(1)_R, re-verified by explicit Haar integration

This verification uses no parity rule.

**Integrator.** I parametrize each link as `U=[[a,−b̄],[b,ā]]` with Haar measure uniform on S³, so that `E[a^p ā^q b^r b̄^s] = δ_{pq}δ_{rs} p! r!/(p+r+1)!`.

**Tests of the integrator.** It reproduces the following:
- `E[(|a|²+|b|²)^k]=1` for k = 1–4;
- the moments `E[W^n] = 1, 0, 1/4, 0, 1/8, 0, 5/64, 0, 7/128`;
- in scratch, the character identities `E[Tr(UV)TrU TrV]=1/2`, `E[Tr(UVX†)TrU TrV TrX]=1/4` and `Tr(U)²−Tr(U²)=2det U`.

**The ten faces.** They form the set F_R: the xz faces with `r=0,1,2`, `s=0,1`, and the yz faces with `r=0..3`, `s=0`, all anchored at 0, and all of their links lie among the 48 cover links. Each face function is expanded as the full trace polynomial of `U_{p,a}U_{p+a,c}U†_{p+c,a}U†_{p,c}`.

**The Gram matrix.** With `e_f=2W_fΩ_R=Tr(U_f)`, the 11×11 Gram matrix of `{Ω_R, e_f}` is **exactly the identity**. All 66 pairs were integrated over every link. So:
- `⟨Ω_R, W_fΩ_R⟩=E[W_f]=0`;
- `||W_fΩ_R||=1/2`;
- distinct faces are orthogonal.

Orthogonality needs only that the two faces are distinct: then some link occurs once in the product.

**The operator.** Write `rho^(1)_R = |x⟩⟨Ω_R| + |Ω_R⟩⟨x|` with `x=(tau/72)ΣW_fΩ_R=(tau/144)Σe_f ⊥ Ω_R`, so `||x||² = 10tau²/20736`. On `span{Ω_R, e_f}`, per unit τ, the operator:
- is symmetric and traceless;
- has `Tr M²=20/20736`, `M³=(10/20736)M` and rank 2;
- has characteristic polynomial `λ⁹(λ²−10/20736)`, computed by Faddeev–LeVerrier.

Its eigenvalues are therefore `±sqrt(10)|tau|/144`, with 0 nine-fold, so **`||rho^(1)_R||_1 = 2||x|| = sqrt(10)|tau|/72`**. At the cap it is about 4.392052305789e-10, and its square is exactly `1/5184000000000000000`.

**The triangle alternative.** Each of the ten rank-one pieces `(tau/72)(|W_fΩ⟩⟨Ω|+h.c.)` has trace norm `|tau|/72`, so the triangle sum is `10|tau|/72=5|tau|/36`. Orthogonality turns that sum into `sqrt(10)|tau|/72`. The triangle value is a valid **upper** bound only. Used at the lower end it would give an invalid tier (`5|tau|/36−K_2'tau^2` ≈ 1.3875e-9, which exceeds the true distance).

**The R-marginal.** For each of the 72 straddling faces, integrating its outside-owned links against the Haar vacuum gives the **zero polynomial**. So only the 10 faces survive `Tr_{R^c}`, and none of the straddling faces reaches `rho^(1)_R`.

**Readouts.** `Tr(rho^(1)_R W)=+tau/144` and `Tr(rho^(1)_R W²)=0`, both by the same integrator. `Tr(rho^(1)_R W_g)=+tau/144` for **every** `g∈F_R`, so this readout cannot tell W apart from the other nine faces. A source edit that moves W inside F_R is silent.

## 3. The single-state remainder and the tier

**The admitted item.** The bound `||rho_R−P_R−rho^(1)_R||_1 <= K_2'tau^2`, for every subsequential limit of either family, is the AY1 gate `accepted` statement in items (2)–(3). It is proved in AY1 forward (HNM-AY1-F11 with the exact decomposition F13 and the itemization F14) and in AY1 reverse (§3.5 exact identity, §3.6 ledger, §3.7 passage to every limit through closed trace-norm balls). The gate's `decision` item (4) binds only the pair form.

**Derivation of the tier.** Apply the reverse triangle inequality to `rho_R−P_R = rho^(1)_R + r_R` with `||r_R||_1<=K_2'tau^2`:

`sqrt(10)|tau|/72 − K_2'tau^2  <=  ||rho_R−P_R||_1  <=  sqrt(10)|tau|/72 + K_2'tau^2`.

**Directed bracket.** `sqrt(10)` lies in `[s_lo, s_hi]`, with:
- `s_lo = 6324555320336758663997787088865437067439/2·10^39`;
- `s_hi = 7905694150420948329997233861081796334299/2.5·10^39`;
- `s_lo² <= 10 <= s_hi²` and `s_hi−s_lo = 10^-40`.

The lower end uses `s_lo` and the upper end uses `s_hi`.

**Endpoints at `|tau|=10^-8`, either sign:**

| End | Exact | Preview |
|---|---|---|
| lower `s_lo|tau|/72 − K_2'tau^2` | `123239559058361081983852878412972198415914793719936897926499081872887/281456584757098479509944550515200000000000000000000000000000000000000000000000` | **4.378634778245e-10** |
| upper `s_hi|tau|/72 + K_2'tau^2` | `619974246770223089945118392610008565852855028054286523715368951086693/1407282923785492397549722752576000000000000000000000000000000000000000000000000` | **4.405469833333e-10** |
| half-width `K_2'tau^2` | `966771578474926086618624139557778885954947547760216752246561/720528856978172107545458049318912000000000000000000000000000000000000000` | 1.341752754400e-12 |

**Checks on the endpoints.** Each is directed: `(lower+K_2'tau^2)^2 <= 10tau^2/5184 <= (upper−K_2'tau^2)^2`, checked exactly, and the bracket slack is at most `1.4×10^-50`. The tier lies inside the AY1 gate's recorded observation [4.3786e-10, 4.4055e-10]. The upper end is 0.0324 D.

**Consequences, with their limits:**
- The lower end is positive, since `(72K_2'|tau|)^2 < 10` with a ratio of 327.34. So **no chosen subsequential limit of either family has the Haar product as its R-marginal**.
- The tier does **not** identify the limit: it holds for every limit alike.
- It is a static property of the state on R. It is not a resolved interaction shift, a Euclidean node or a dynamical statement.
- `K_2'(|tau|)` is nondecreasing, so the cap formula holds at every `|tau|<=10^-8`. The first-order term scales with exponent 1 and the remainder with exponent 2 (checked at τ/100).

**Label:** `first_order_distance_from_product`.

## 4. Relative width and the preregistered target

**Value.** The tier's width relative to its centre is `2K_2'tau^2/(sqrt(10)|tau|/72) = 144K_2'|tau|/sqrt(10)`. Its directed bracket is ≈ [6.1099124554e-3, 6.1099124554e-3] (exact in the results).

**Decision.** The target `<= 1/100` is decided without a bracket, as `(14400K_2'|tau|)^2 = 3.7331… <= 10`. The margin is 1.63668. The endpoint form `(U−L)/((U+L)/2)` also passes.

**What the target can and cannot catch:**
- It fails only for `K_2' >= 21960.26`.
- It passes with `K_2^+` (1.53e-3) and with every labelled variant, so it cannot detect tier mixing.
- It catches the pair constant used as the half-width (1.2220e-2) and a double-counted τ.

## 5. The ±tau separation, and why 2D alone is not a boundary comparison

Write `rho_R(±tau) = P_R ± tau·rho_hat + r_±`. Then

`||rho_R(tau)−rho_R(−tau)||_1 >= 2·sqrt(10)|tau|/72 − 2K_2'tau^2 = sqrt(10)|tau|/36 − 2K_2'tau^2 >= 8.757269556e-10`.

Yet each limit lies within `upper <= D` of `P_R`, so the two are within 2D of each other. `P_R` does not depend on τ, so 2D is a common enclosing ball. The comparison content is the matching first-order term together with `2K_2'tau^2`. The `±tau` states are at different couplings, so they fall under the `common_clock` control, not under a same-coupling boundary comparison. The contract's "both lie within 2D of the product" should read "each within D" (contract review item 8).

## 6. The falsifying scenario and an exact fixture

The present bounds constrain a subsequential limit on R only through these statements:
- `||rho_R−P_R||_1<=D` (AV1);
- `|omega(W)−tau/144|<=K_2^+tau^2` (AW1);
- `||rho_R−P_R−rho^(1)_R||_1<=K_2'tau^2` (AY1);
- positivity, trace one and gauge invariance.

None of these puts a lower bound on the distance between two limits after the common first-order term is removed. So two limits, of the same family or of different families, may differ on R by up to `2K_2'tau^2` ≈ 2.6835e-12, and without bound off R.

**Exact 12-dimensional fixture.** It is not asserted to be realized by the AQ Hamiltonian.
- **Space and vectors.** Take `Ω_R`, the ten `e_f` and `v=χ_1(U_{f1})Ω_R=(Tr(U_{f1})²−1)Ω_R` for the yz face `f1=(1,0,0)`. The integrator shows these 12 vectors are orthonormal. All are gauge-invariant class functions of plaquettes.
- **States.** Let `psi_± = Ω_R + x ± κv` with `κ=(K_2'tau^2−21t²)/2`, where `t=tau/144`. Let `rho_±=|psi_±⟩⟨psi_±|/n²`.
- **Each state satisfies every bound listed above:**
  - `||rho_±−P_R−rho^(1)_R||_1 <= K_2'tau^2`, by a directed triangle bound;
  - `||rho_±−P_R||_1 <= D`;
  - `omega_±(W) = (tau/144)/n²`: all W matrix elements involving v vanish by exact integration, so the deviation is only about −3.3e-30.
- **The two states differ by almost the full bound.** With the norm-one test operator `|v⟩⟨Ω_R|+h.c.`, `||rho_+−rho_−||_1 >= 4κ/n²` ≈ 2.683505306e-12. That is `(1−7.5×10^-8)·2K_2'tau^2`.

**Why going to higher order would not help.** Carrying the AY1 argument to order k (with constants `K_k'`) would shrink the scenario to `2K_k'|tau|^k`. At fixed τ that never excludes a nonzero difference, unless one adds an analyticity argument that is uniform in N (§8, route U-b).

## 7. K_2' versus K_2^+

**The ratio.** `K_2'/K_2^+ = 3867086313899704346474496558231115543819790191040867008986244/966893014524284957965768152362480514948256313800811767578125` ≈ 3.99949762.

**Why `K_2'` is larger:**
- `K_2^+` (AW1) bounds the single observable W. W pairs only with the `{0,e_z}` sector, with multiplier `2||WΩ_R||=1`.
- `K_2'` bounds the trace norm over all of `B(H_R)`. It pays multiplier 2 and all three excited sectors.
- The AM2 remainder `rho=352JT` makes up 99.98% of `K_2^+` and 99.99% of `K_2'`, and it is not reduced by face restriction.
- So every trace-norm constant assembled from the AW1 items is at least `2rho/tau^2 = 47162500000/7030557` ≈ 6708.217, which exceeds `K_2^+`.

**How to read this:**
- This is a statement about constants built from the admitted items. It is not an impossibility theorem.
- The W-projected R-local analogue, ≈ 3354.4994, lies below `K_2^+`. It is a constant for W, not a density bound.
- `K_2^+` is uniform in N and specific to W, so "whole-box" is a misnomer. AY1's "(not the whole-box K_2^+)" means only "built from R-local face pins".
- The labelled variants may appear only as previews:

| Variant | Value |
|---|---|
| √2 sectors | ≈ 9487.945 (directed √2) |
| 288-majorant | ≈ 10978.18 |
| combined | ≈ 7763.06 |
| admitted-`eps` | ≈ 13417.81 |

## 8. The six obligations: missing premise, candidate route, and which constants exist

**Constants available** (checked exactly in `route_constants_*`):
- **AM2:**
  - `J_0=7/25000000`, `G(R)<148/7`, `G'(R)<352`, `R=1/64`;
  - `J_0G(R)=37/6250000`, `2J_0G'(R)=77/390625`;
  - full-space gap 1/2 (normalized) in every finite volume and for every interaction family that meets its hypotheses;
  - as written, AM2's two inequalities hold for real `|tau|<1/37888` (self-map) and `|tau|<1/19712` (exclusion), about 2639 and 5073 times the cap. That is a route constant, not an admitted extension.
- **AQ1:** Nachtergaele–Sims with `F(r)=(1+r)^-4` on the l1 metric. The l1 shells have exactly `4r²+2` sites (checked for r ≤ 9), giving `||F||<=7` and `C_F<=224`. Stars have l1 diameter 2, so `||Phi||_F<=81·28|tau|=2268|tau|`.
- **F2:** owner sets have l1 diameter at most 2 and `J'=49|tau|/3`, so `||Phi'||_F<=1323|tau|`.
- **Lieb–Robinson exponents** `2||Phi||_F C_F`: 3969/390625 ≈ 0.01016 (F1) and 9261/1562500 ≈ 0.00593 (F2) per unit `u=theta/8`.
- **The boundary shell.** F2 minus F1 is `28N(5N+1)` faces (616 at N = 2 and 1344 at N = 3), at l∞ distance N−1 from R.

**Constants not available:**
- the HTW/Yarotsky `c_1`, `c_2`, `c_HTW(1,1)` (AM2 gate limitation);
- quasi-adiabatic filter constants;
- a weighted or complex-τ AM2 estimate;
- a polymer normalization bound;
- any Euclidean or Dobrushin influence coefficients.

| # | Obligation | Missing premise | Candidate route (constants needed; available?) |
|---|---|---|---|
| 1 | **Uniqueness**: equality of any two subsequential limits of F1 and F2 as states on the quasi-local algebra | A non-perturbative estimate of boundary influence on local marginals that decays with distance. Every AY1 constant is uniform in N but does not decay | See the four routes U-a to U-d below |
| 2 | **Whole-sequence convergence** of each family | Uniqueness within the family, or a Cauchy estimate | Row 1 within one family plus AQ1 trace-norm compactness (every subsequence has a sub-subsequence tending to the unique limit); no rate. Available except row 1 |
| 3 | **Translation invariance**, under **coarse** translations `b∈Z³` only; the (4,2,1)-periodic face pattern breaks fine translations | Uniqueness across box sequences (`Lambda_N+b`) | Coarse-translation covariance, which holds by construction (`omega∘T_b` is a limit of the translated family), plus row 1 for all exhausting sequences. Partial step, not proved in any packet: rerun AY1 on the translated cover `R+b` for `N>=|b|_∞+2`. That gives `||rho_{R+b}−T_b(P_R+rho^(1)_R)T_b*||_1<=K_2'tau^2`, i.e. approximate invariance within `2K_2'tau^2` on every translated cover |
| 4 | **Rate in N** | Any N-dependent estimate | HTW `exp(c_1|Y|−c_2(N−O(1)))` (AN1's form was `min(2,exp(2C_1−C_2(n−2)))`); route U-b `(|tau|/r_0)^{c(N−1)}`. No constant evaluated |
| 5 | **Boundary independence of dynamics** on compact windows: the F1 and F2 limiting automorphism groups coincide | A written Duhamel/Lieb–Robinson comparison, and row 6 | The finite-volume Hamiltonians differ by the `28N(5N+1)` shell faces, each of norm `|tau|/3`. Duhamel gives `||tau^N_t(A)−tau'^N_t(A)|| <= Σ_f(|tau|/3)∫_0^{|t|}||[W_f,tau'^N_s(A)]||ds`. The Nachtergaele–Sims bound (as placed by AQ1) is `(2||A||/C_F)(e^{2||Phi'||_F C_F|s|}−1)Σ_{x,y}F(d(x,y))`; its right side increases in `C_F`, so `C_F<=224` may be used. Since `F<=N^{-4}` on the shell, the difference is expected to be O(N⁻²) and the limits equal (not proved). **All constants are available** (AQ1 plus AY1 reverse), and they are not AM2's. GNS-level generators of two possibly different states would need row 1 as well |
| 6 | **Dynamics of the padded family**: F2 dynamics, stationarity of F2 limits, GNS continuity, a nonnegative generator, and the AQ2 physical gap for F2 limits | AQ1 §3–5 and AQ2 re-executed for F2 | Repeat them with `Phi'` (supports at most 3, l1 diameter at most 2, `||Phi'||_F<=1323|tau|`; padded sites carry only `h_b` and decouple) and the AM2 gap for F2 boxes, admitted in AY1. **All constants are available**; the proof is not written |

**Row 1, the four candidate routes:**
- **U-a. HTW Thm 7** (Henheik–Teufel–Wessel LMP 2022, restating Yarotsky 2005 Thm 2). It needs `c_1`, `c_2` and `7|tau|<=c_HTW(1,1)` evaluated. None is available: AM2 states that it does not evaluate them, and Round29 AN1/AN2 used them only in existential form.
- **U-b. Analyticity (native to AM2).** It needs:
  - the creation fixed point and a normalization bound, extended to complex τ in a disk of radius `r_0` uniformly in N (at most the real self-map radius 1/37888 if the estimates extend);
  - order-by-order box locality of the Taylor coefficients of `rho_{N,R}`;
  - then Vitali/Cauchy estimates.

  Only the real AM2 constants are available.
- **U-c. A quasi-adiabatic bound on local perturbations.** It needs the AM2 gap 1/2 (available, also along the interpolation), an exponential F (derivable from finite range, not stated), the filter constants (not available) and control of the unbounded on-site terms.
- **U-d. Dobrushin-type.** It needs a Feynman–Kac Gibbs representation, heat-kernel mixing on SU(2)^24 against spatial couplings of about `49·(2|tau|/3)·L` per time block, and a block version, since conditional laws of path segments are singular. None is available.

**Ranking by availability.** Rows 6 and 5 have all their constants and need only writing. Row 2 reduces to row 1. Rows 3, 1 and 4 need constants that nobody has evaluated. None of the six is proved, and none may be called closed.

## 9. What I will require of the producer

1. **Constants.** Read `D`, `2D`, `K_2'`, `2K_2'tau^2` and `K_2^+` as exact rationals from the snapshotted AY1 gate, with its hash checked. Any recomputation must equal them. No labelled variant may appear in a headline or in the tier.
2. **Citation and convention.**
   - Cite the single-state remainder as the AY1 gate `accepted` item (2)–(3) with the AY1 proofs.
   - State the τ convention once: τ is inside `rho^(1)_R`.
   - Never use `2K_2'tau^2` as the half-width.
3. **First-order norm.** Derive `||rho^(1)_R||_1=sqrt(10)|tau|/72` by orthogonality and norm 1/2 of the ten vectors, not by the triangle `5|tau|/36`. Cite the 72-face vanishing.
4. **The tier.**
   - Give the `sqrt(10)` bracket, exact endpoints with the lower end from `s_lo` and the upper from `s_hi`, and the label `first_order_distance_from_product`.
   - State that it is static and not an interaction-shift, Euclidean-node or dynamical claim.
   - Draw the lower-end consequence (not the Haar product) and add "does not identify the limit".
   - Cover both signs and the scope in |τ|.
5. **Relative width.** Report it with its reading, as an exact decision, with its margin, and say that the target is met by construction.
6. **Scenario and ±tau.** Give the falsifying scenario with `2K_2'tau^2` exact and the reason it cannot be excluded. In the ±tau paragraph say "each within D of `P_R`", give the separation `>= sqrt(10)|tau|/36−2K_2'tau^2`, and state that the comparison content is the first-order match.
7. **`K_2'` versus `K_2^+`.**
   - State it with the qualification "constants assembled from the AW1 items with the admitted AM2 remainder".
   - Say that `K_2^+` is uniform in N and specific to W.
   - Correct the AY1 wording.
   - Give the variants as previews only.
8. **Obligations table.**
   - Use exactly these six rows, each with its missing premise, candidate route, the constants the route needs, and which of them are available.
   - Name the Lieb–Robinson constants as AQ1's.
   - Say that the HTW constants are unevaluated (AM2 gate).
   - No row may be called proved or closed by a route.
9. **Wording.** The template goes verbatim from the AY1 gate. Say "a chosen subsequential". The forbidden phrases may appear only negated.
10. **Exports.**
    - The five fields `uniqueness_claimed`, `whole_sequence_claimed`, `rate_claimed`, `translation_invariance_claimed` and `boundary_independence_of_dynamics_claimed`, together with `rate_in_N_claimed`, all false.
    - `states_compared`, `region`, `topology`, and `closeness_order` `[1,2]`.
    - `resolved_interaction_shift`, `euclidean_node_certified`, `dynamical_claim`, `continuum_claim`, `weak_coupling_claim` and `scientific_priority_verified`, all false.
11. **Controls.** All 21 controls as damaging mutations, with stated semantics for the two new ids.
12. **Protocol.**
    - The `check.py` sha256 recorded before evaluation.
    - Contract and gate hashes checked.
    - Byte-identical replays under normal and `-O` Python.
    - An inventory of exactly 23 files.

## 10. Predicted values (the post-comparison flags any difference)

| Quantity | Prediction |
|---|---|
| `D`, `2D` | gate rationals; 1.361245287e-8, 2.722490574e-8 |
| `K_2'`; `K_2'tau^2`; `2K_2'tau^2` | gate rational ≈ 13417.5275440; 1.341752754e-12; 2.683505509e-12 |
| `K_2^+`; ratio | ≈ 3354.80322946; 3.99949762 |
| Face counts | 7 anchors, 82 meeting R, 10 inside, 72 vanish |
| `||rho^(1)_R||_1` | `sqrt(10)|tau|/72` ≈ 4.392052305789e-10 (square `1/5184000000000000000` at the cap) |
| Tier (exact endpoints depend on the bracket) | [4.3786347782e-10, 4.4054698333e-10] |
| Relative width (full); half-width reading | 6.1099124554e-3 (margin 1.63668); 3.0549562e-3 |
| Failing `K_2'` threshold | ≈ 21960.26 |
| First-order/remainder | ≈ 327.34 |
| ±tau separation | ≥ 8.757269556e-10 |
| Upper end / D | ≈ 0.0324 |

## 11. Producer-error checklist

1. **Pair constant as the half-width.** The tier becomes [4.3652e-10, 4.4189e-10] and the relative width 1.222e-2, which fails the target.
2. **Triangle `5|tau|/36` at the lower end.** This is invalid (≈ 1.3875e-9).
3. **τ counted twice.** The lower end becomes vacuous.
4. **√10 rounded the wrong way** at either end.
5. **`K_2^+` in the tier.** It gives [4.38870e-10, 4.39541e-10], which is not a trace-norm bound. A labelled variant in the tier is the same kind of error.
6. **"Within 2D of `P_R`"** copied from the contract.
7. **"Lieb–Robinson with the AM2 constants"** with no AQ1 constants named.
8. **Obligations errors.** A row missing, or a row "closed" by HTW or AN2, whose constants are existential.
9. **The lower bound called** an interaction shift or a dynamical effect.
10. **Forbidden phrases:** "the AQ state", "the limit", or "unique" without "not".
11. **`K_2'` below `K_2^+`**, or "whole-box `K_2^+`" repeated.
12. **The ±tau pair called** a same-coupling boundary comparison.
13. **Floats** in admission.

## 12. Replay and source-edit mutations

**Command.** `python3 -B research/round32/skeptic/ay2_check.py --output <abs fresh dir>`.

**Replays.** The normal, `-O` and no-`-B` runs are byte-identical: `results.json` sha256 is recorded in `ay2-independent-freeze.json`. No `.pyc` is written. The run takes about 0.7 s.

**Source-edit mutations.** These ran on copies of the checker in private scratch. The unmutated copy reproduces the results, apart from its own `checker_sha256`.

**Seventeen must-abort edits all abort at the intended check:**
- the `eps_R` pin 82→66, the straddling pin 72→66 and `4rho→2rho`: all abort at `K2_prime_recomputed_from_gate_items`;
- `eps_F` without `T²`: aborts at `D_recomputed_tier_ii`;
- a changed selected pattern;
- the Haar moment denominator;
- the SU(2) entry sign: aborts at the Gram check;
- the `rho^(1)` amplitude 1/72 and the `rho^(1)` sign;
- the lower end computed with `s_hi`;
- the upper end with half the remainder;
- the fixture κ without slack;
- the boundary-shell formula;
- the contract hash;
- removal of the validator's pair-constant, obligation-status or static-label checks: each surfaces through its control.

**Two edits are undetectable by value:**
- the bracket-free Boolean with the constant 20000 instead of 14400, which still passes because the target is met with margin;
- W moved to another face of F_R, which gives the same readouts.

Both are recorded in §4 and §2.
