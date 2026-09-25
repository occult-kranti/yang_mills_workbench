# Round33 independent skeptical triage (prospective, deliberation loop 1)

**Standing.** This is prospective review by a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and the producers. It is not human peer review and not formal verification. It was written on 2026-09-24, before any Round33 contract exists. Every derivation below is a skeptic's sketch that the producers must derive independently. Every decimal is a preview. Exact rationals come from my private scratch (`/tmp/claude-0/skeptic-r33-triage/`: `triage_numbers.py`, `derived.py` and their outputs, using `fractions.Fraction` with directed exponential bounds). They are not evidence, and they are not premises for any reverse producer. Human project author: Hruday N M (BUNZEEY). Nothing here is a Round33 result, a loop, or a fraction of the continuum problem.

**Read:**
- the advisor brief;
- my Round32 record: `triage.md`, `prospective-controls.json`, `loop2-response.md`, `loop3-signoff.md`, `ay1.md`, `ay2.md`, `az1.md` and `az2.md`;
- `HANDOFF.md`, `advisor/roadmap.json`, `advisor/panel-update-5.md` and the ten rules in `experts/jung/update-5.md` §3;
- the lessons file `round32-state-lemma-and-window.md`;
- the Round33 `tools/README.md` and the rule list of `freeze_contract.py`;
- the mathematical sources: AM2 forward, reverse and skeptic; AQ1 and AQ2 forward; AV1 forward §§1–8; AY1 forward §§1–3; AY2 forward §§1.5–3; AW1 forward §§1–3.

**Name-only exposure, disclosed.** Two Round33 lens memos already exist: `experts/historical/memo.md` and `recommendation.json`, and `experts/jung/memo.md` and `recommendation.json`. I did not open them. I saw their file names in `git status` and two commit subject lines in `git log`. One subject line reads: "historical lens memo (min-order-versus-distance lemma for boundary decay, sub-round proposal, gauge-group transfer table)". The analyticity route in §(a).5 below may resemble that lemma. I derived it from the AM2 inequalities alone, and its agreement with the weighted-norm rate is checked below. It is recorded here as a separate derivation, not as independent confirmation.

---

## (a) Boundary-influence decay, whole-sequence convergence and a common limit of F1 and F2

### (a).1 What the admitted contraction gives: global smallness, not locality

AM2 (HNM-AM2.4–2.9) solves `c = sum_k L_k(c,…,c)/k!` in the anchored sup norm `||c||_a = max_u sum_{I ∋ u} ||c_I||` on the ball of radius `R = 1/64`. Two facts decide what a boundary estimate needs.

1. **Box dependence.** The map `F_Λ(c) = sum_k L_k^{V^Λ}(c,…,c)/k!` depends on the box only through `V^Λ`. `H_M^{-1}` and `P_M` are site-local, and so are the cutoff compressions. For nested boxes of one family, `V^{Λ'} = V^Λ + V^new`. So the difference `δ := c^{Λ'} − c^{Λ}` (with `c^Λ` extended by zero) satisfies exactly

   `δ = S + [F_{Λ'}(c^{Λ'}) − F_{Λ'}(c^Λ)]`, where `S = sum_k L_k^{V^new}(c^Λ,…,c^Λ)/k!`.

   The source `S` contains only new interaction terms. For F1 these are new whole stars `X = b+S ⊄ Λ_N`, and every one of them meets the shell `B = Λ_{N+1}∖Λ_N`. For F2 they are new faces, whose owner sets meet `B`. For F1 against F2 at the same `N`, the source is the `28N(5N+1)` extra F2 faces, whose owners lie in the outer layer `|b|_∞ = N`.
2. **The sup norm gives no decay.** In the admitted norm, `||δ||_a ≤ J_0 G(R)/(1 − J_0 G'(R)) = 37/6249384 ≈ 5.92058e-6`, uniformly in `N`. This bound does not decay. `2J_0 G'(R) < 77/390625` is a **global** Lipschitz constant, and the AY2 obligation row O2 already says so. Supports are unbounded: the fixed point has components on arbitrarily large, possibly disconnected supports (`V_X` can de-excite sites of `X`, so `M = N∖X` is possible). The anchored norm permits all the weight to sit on large supports. **Conclusion: the admitted contraction yields global smallness only. Locality needs a weighted norm.**

### (a).2 The weighted norm: which weight, and whether the contraction survives

**The brief's weight points the wrong way.** A weight `e^{μ d(X,R)}` that *grows* with distance from `R` penalizes far supports. That is wrong for `δ`, which must be shown small *near `R`*, far from the source. A pure distance weight is also not submultiplicative under the union step, because `d(M,·)` can exceed `d(I_j,·)` by the diameters of the other supports. Two weights are needed:

- **(W) A diameter weight on the fixed point.** Define `||c||_μ := max_u sum_{I ∋ u} e^{μ diam(I)} ||c_I||`, with diameters in the **coarse ℓ∞ metric** on factor indices. Each creation support `I_j` of a nonzero word meets `X`, and `M ⊂ N ∪ X`. Hence `diam(M) ≤ d_X + sum_j diam(I_j)`: two points of `M` are joined through at most two supports and `X`. AM2's counting is unchanged (16 output sets, `|I_j| ≤ |M|+4`, the `1/|M|` cancellation), so

  `||L_k(c_1,…,c_k)||_μ ≤ e^{μ d_X} · J · 16·8^k(1+5k/4) · prod_j ||c_j||_μ`.

  **The loss factor `w = e^{μ d_X}` is paid once per interaction, not once per creation.** A star `b+S` has `d_X = 1` in ℓ∞ and `d_X = 2` in ℓ1. Weights are at least 1, so the μ-ball lies inside the AM2 ball. The AM2 iteration from `c = 0` stays in the μ-ball of radius `R` whenever `J w G(R) ≤ R`. Its limit, the unique AM2 fixed point, therefore satisfies `||c||_μ ≤ J w G(R)`. Only this self-map condition is needed. The exclusion argument is untouched.
- **(B) A boundary-distance weight on the difference.** Define `ρ_B(I) := max_{p ∈ I} d_∞(p, B)` and `||δ||_{B,β} := max_u sum_{I ∋ u} e^{β ρ_B(I)} ||δ_I||`, with `β ≤ μ`.
  - For a source term, `X` meets `B`, so `ρ_B(M) ≤ 1 + max_j diam(I_j)`.
  - For a telescoped Lipschitz term with its `δ`-slot on `I_δ`, `ρ_B(M) ≤ ρ_B(I_δ) + 1 + max_{j≠δ} diam(I_j)`.

  Both are products of the admissible weights. Hence

  `||δ||_{B,β} ≤ ||S||_{B,β} / (1 − J e^{β} G'(t_μ))`, with `||S||_{B,β} ≤ e^{β}·(exact first-order source) + J e^{β}(G(t_μ) − 16)`,

  and `sum_{I ∋ u} ||δ_I|| ≤ e^{−β d_∞(u,B)} ||δ||_{B,β}`.

**Does the contraction survive? Yes, with large slack.** Exact thresholds at `J_0 = 7/25000000`:

| condition | exact | preview |
|---|---|---|
| self-map `J_0 w G(R) ≤ R` | `w ≤ 390625/148` | 2639.36 |
| exclusion-strength `2J_0 w G'(R) < 1` (not needed) | `w < 390625/77` | 5073.05 |
| smallest per-step rate at `r = R` (ℓ∞, `d_X = 1`) | `q_min = 148/390625` | 3.7888e-4 |
| same in ℓ1 (`d_X = 2`) | `q_min^{1/2}` | 0.01946 per ℓ1 step |
| cardinality weight `e^{μ|I|}` (`|X| ≤ 4`) | `q_min^{1/4}` | 0.1395 per site |
| `q_min` optimized over the radius `r` (preview) | `J_0 min_r G(r)/r` | 1.90e-4 at `r ≈ 0.0725` |
| coupling threshold for `w = 64` (self-map) | `|tau| ≤ 1/2424832` | 4.124e-7 (the cap is 41 times inside) |

**The metric and the weight matter.** Diameter weights in coarse ℓ∞ give a per-step rate about 370 times better than cardinality weights. The brief's "each chain step costing a factor of order `J G(R) < 1/64`" leaves out the ball radius. The admissible per-step factor is `q ≥ J G(r)/r`, about `64 J_0 G(R) = 3.79e-4` at the cap, not `J_0 G(R) ≈ 5.9e-6`. The resource is the contraction slack `R/(J_0G(R)) ≈ 2639`.

### (a).3 Candidate coefficient constants at `|tau| = 10^-8` (both signs; same `|tau|` formula)

The headline pair is `w = e^β = e^μ = 64`, so `q = 1/64` per coarse ℓ∞ step.

- **Tier (i), crude majorant:** `t_μ ≤ 8783152/30425078125` (2.8868e-4), Lipschitz ≈ 5.18e-3, **`K_i = 683489176048/2359186627607241 ≈ 2.8971e-4`**.
- **Tier (ii), exact first-order source plus the self-consistent majorant remainder:**
  - `||L_0[V^new]||_{B,β} ≤ e^{β}·49|tau|/144`: new faces have owner sets within ℓ∞ distance 1 of `B`, and there are at most 49 faces per site;
  - `t_μ ≤ w t_1/(1 − J w G'(R)) = 49/223580736` (2.1916e-7);
  - **`K_ii = 534319943299975/2428235828306468180928 ≈ 2.2004e-7`**.

With `w = 1000` (`q = 10^-3`): `K_i ≈ 5.358e-3` and `K_ii ≈ 4.032e-6`.

**Statement.** For `u ∈ R`, `sum_{I ∋ u} ||c^{N+1}_I − c^N_I|| ≤ K q^N` for F1 and for F2. For F1 against F2 at the same `N`, the bound is `≤ K q^{N−1}`, because the outer layer lies at ℓ∞ distance `N−1` from `e_z`. The shell `Λ_{N+1}∖Λ_N` lies at distance `N` from `e_z` and `N+1` from `0`.

**τ-scaling trap (found in scratch).** For `K_ii` the exact ratio `K(10^-8)/K(10^-10)` is `51987410123326661621015808351208548/514571882794658415944198372286673 ≈ 101.030`. This lies **outside** AV1's `[99,101]` linear bracket, because the weight amplifies the `(1 − cτ)^{-1}` nonlinearity. The bound is still linear to leading order. Every contract must declare its scaling bracket per constant, for example `[95,105]` for linear against `[9.5,10.5]` for a square root, or must compare `τ/100` with `τ/10^4`. Reusing `[99,101]` would reject a valid linear bound.

### (a).4 The hard step: coefficient decay is not marginal decay

`ρ_R` is not a function of the coefficients `c_I` with `I ∩ R ≠ ∅` alone. In AV1 (F07–F11), `ψ = ψ_out + δ` with `ψ_out = Ω_R ⊗ φ_out`, and the reduced density

`ρ_R = [n² P_R + |Ω_R⟩⟨ξ| + h.c. + σ]/(n² + d²)`

depends on the normalized **outside state** `ω_out` of `φ_out` in three places:
- through `ξ`: a straddling `I` contributes `sum_k a_k ω_out(|b_k⟩⟨Ω_{I∖R}|)`;
- through the pair terms;
- through `σ` and `d²/n²`.

A change of the box changes `ω_out` near `R` through the whole chain of supports. This is where "the normalization of the ground vector couples all supports" really bites. The AV1 fixture (F13) already shows it: `ρ_r` depends on the outside coefficient `b`.

**What a correct statement needs (new lemma, "marginal locality").** For collections `c, c'` in a weighted ball, the lemma needs a bound of the form

`||ρ_R(c) − ρ_R(c')||_1 ≤ 2(1+η) sum_{I ∩ R ≠ ∅} ||c_I − c'_I|| + sum_{I ∩ R = ∅} κ(I) ||c_I − c'_I||`, with `κ(I) ≤ κ_0 w'^{−d_∞(I,R)}·poly(|I|)`.

Two routes are available, and they are genuinely different:
- **(M-f) Iterated R-vacuum ordering.** Apply the AV1 split to `φ_out` with `R` replaced by `Y = ∪(I∖R)` over straddling `I`, then recursively. Each level costs a straddling amplitude `O(t)`. `|ω_out(|b⟩⟨Ω_Y|)| ≤ ||b||·e_Y` by the off-diagonal block. The normalization is exact at every level. Regions grow by support diameters, which the weight `e^{μ diam}` absorbs, together with `|I| ≤ (1+diam I)³`, provided `μ > β`.
- **(M-r) Polymer or cluster expansion.** `ψ = sum_F (−1)^{|F|} ⊗_{I∈F} c_I ⊗ Ω` over families of disjoint supports, and components with different excitation sets are orthogonal. So `⟨ψ,ψ⟩` is a hard-core polymer gas whose polymers are connected pairs of partitions of a common excitation set, with activities at least quadratic in `c`. `⟨ψ, Aψ⟩` modifies only the polymers touching `R`. A Kotecký–Preiss criterion with the μ-weighted anchored norm then gives the ratio as a sum over clusters touching `R`. The influence of a support at distance `ℓ` from `R` comes only through clusters of length at least `ℓ`.

  An equivalent form differentiates along `c + λδ`: `∂_λ ω(A) = −[ω(A; δ̂) + ω(δ̂*; A)]`. This needs clustering of creation-product states, which is the same combinatorics.

**Candidate constant (sketch, to be derived).** First-order changes enter only through supports inside `R`. Straddling changes enter at relative order `O(t_μ)`. So `C_ρ = 2·|R|·K·(1+η) = 4K(1+η)` with `η = O(t_μ)`: about 1e-3 at tier (i) and about 1e-6 at tier (ii).

| tier, `q=1/64` | `C_ρ = 4K` (before η) | `C_∞ = (64/63)C_ρ` | tail N=2 | N=3 | N=4 | F1 vs F2, N=2 | N=3 |
|---|---|---|---|---|---|---|---|
| (i) | 1.1589e-3 | 1.1773e-3 | 2.874e-7 | 4.491e-9 | 7.02e-11 | 1.81e-5 | 2.83e-7 |
| (ii) | **8.8018e-7** | **8.9415e-7** | 2.183e-10 | 3.41e-12 | 5.3e-14 | 1.38e-8 | 2.15e-10 |

Compare AY1's `2D ≈ 2.7225e-8`. At tier (i) the Cauchy tail beats `2D` only from `N = 3`. At tier (ii) it beats it from `N = 2`.

### (a).5 A second route for the coefficients: analyticity and order against distance

The AM2 inequalities are norm inequalities, so the contraction holds for complex `τ` with `28|z| G(R) ≤ R`, that is `|z| ≤ τ_* = 1/37888` (the radius the AY2 review recorded). The fixed point is analytic on that disc, as a uniform limit of polynomial iterates.

By induction, an order-`n` Taylor term of `c_I` comes from a tree of `n` interaction terms. Its output lies in the union of their supports, each support meets its children's, and each has ℓ∞ diameter at most 1. So a term that contains a new interaction (which meets `B`) and has `u ∈ R` in its output needs `n ≥ d_∞(u,B) = N`. Hence `δ_I` vanishes to order at least `N` in `τ`. Both fixed points lie in the `R`-ball on the disc, so `||δ(z)||_a ≤ 2R` there. The maximum principle applied to `δ(z)/z^N` (Schwarz-lemma form) gives

`sum_{I ∋ u} ||δ_I(τ)|| ≤ 2R(|τ|/τ_*)^N`,

with `q = |τ|/τ_* = 148/390625`, exactly the weighted `q_min` above, and constant `2R = 1/32`. This is a fit **reverse route for BA1**.

**The trap for the marginal.** `ρ_R` involves `⟨ψ(τ̄), ψ(τ)⟩` in the denominator. For complex `τ`, this volume-extensive sum can vanish. Extending the route to `ρ_R` therefore needs a zero-free region for the complexified normalization, which is the cluster-expansion problem of (a).4 in another form. A claim that "`ρ_R` is analytic in the disc" without a zero-free proof is rejected.

### (a).6 Assembly, and what it would and would not give

**Assembly.** Lemmas W, B and M combine to give `||ρ^N_R − ρ^{N+1}_R||_1 ≤ C_ρ q^N`, and hence the Cauchy bound `||ρ^N_R − ρ^M_R||_1 ≤ C_∞ q^N`.

**The order of limits.**
- Every estimate holds in each on-site cutoff space `Q_L`, uniformly in `L`.
- For fixed `N`, AV1 (F20–F23: Eckart bound with the untruncated gap `1/2`) passes `ρ^{N,L}_R → ρ^N_R` in trace norm, so the bound survives `L → ∞`.
- No creation expansion of the untruncated vector is ever asserted; AM2 never admits one.

**Consequences:**
- **Whole-sequence convergence.** On every finite region `Y`, with constant about `2|Y|K(1+η)/(1−q)` and exponent `d_∞(Y, B_N)`, the densities converge. The trace class is complete, so the limit exists without compactness. It **coincides with every AQ1 subsequential limit**, and so it inherits AQ1's stationarity, GNS continuity and `H_num ≥ 0`, and AQ2's gap.
- **A common limit for F1 and F2**, since their same-`N` difference tends to zero.
- **Coarse translation invariance**, but only if a general-volume version is proved: two AM2-admissible volumes of the same rule, both containing `B_ℓ(R)`, compared through their union. It must be pre-registered as its own item.

**It would not give:**
- uniqueness of every infinite-volume ground state: states not arising from AM2-admissible finite-volume ground states, boundary conditions violating the per-site bound, and so on;
- a statement at other couplings or for the uniform model (`J' = 29|τ|` needs its own instance);
- a rate in `a`, or a physical correlation length. `q = 1/64` is per coarse ℓ∞ step, and a coarse step is `(4a, 2a, a)`, at strong bare coupling `g^4 = 9.6×10^9`;
- anything beyond the named rule or class.

**The roadmap's Dobrushin/HTW route (rank 1) is subsumed.** A Dobrushin influence matrix of the fixed-point map is exactly the weighted Lipschitz constant of Lemma B. Its row-sum condition is the weighted contraction. The literal roadmap-1 target ("any two subsequential limits of the named families agree on R") is met by Cauchy plus a common limit. I advise against a separate Dobrushin loop.

### (a).7 Where the argument can break

1. **Normalization:** a numerator-only or global-fidelity argument. The global overlap `|⟨ψ̂^N, ψ̂^{N+1}⟩|` is exponentially small in the shell size, so any route through it gives nothing.
2. **The outside vector `φ_out` is not the ground state of an outside Hamiltonian.** It is the restriction of the full box's coefficient family, so no gap argument applies to it.
3. **Coefficient decay stated as state decay** (Lemma M missing).
4. **The admitted global Lipschitz constant used as a decay factor.**
5. **Metric and weight:**
   - ℓ1 and ℓ∞ mixed;
   - `d_X` omitted;
   - loss charged per creation;
   - cardinality weights (rate 0.14);
   - the weight direction reversed.
6. **Distances:** `N` (shell to `e_z`), `N+1` (to `0`) and `N−1` (F2 outer layer) confused.
7. **F2 regrouping at the boundary.** Clipped groups gain faces from `N` to `N+1`. Charge the new faces individually (per-site face sum `49|τ|/3 ≤ J`) and never twice.
8. **Cutoffs:** statements about untruncated coefficients, or the order of the cutoff and `N` limits reversed.
9. **Region dependence hidden:** `|Y|` growth, or a constant stated for `R` and reused on `Y`.
10. **A post-hoc rate:** `q` optimized per `N` after the constants are seen and reported as "the rate". A proved family `q ∈ [q_min, 1)` is legitimate; the headline pair is frozen.
11. **Linear-scaling brackets** copied from AV1 (see (a).3).
12. **The uniform model or other couplings claimed by analogy.**
13. **The analyticity route extended to `ρ_R`** without a zero-free region.

### (a).8 Classification

| piece | classification | reason |
|---|---|---|
| W: weighted AM2 contraction (diameter weight, coarse ℓ∞) | **likely provable** | routine modification, slack about 2639 |
| B: boundary-source decay of coefficient differences (F1, F2, F1 vs F2, general volumes) | **likely provable** | two independent routes (weighted norm; analyticity) give the same `q_min` |
| M: marginal locality of normalized creation-product states | **provable with a new lemma** | the main risk; standard cluster-expansion mathematics (Kotecký–Preiss type), to be sourced and credited, never a premise |
| whole-sequence convergence with rate, common F1/F2 limit | **provable once W, B and M are admitted** | assembly; cutoff order as above |
| coarse translation invariance | provable with the general-volume version of B plus M | must be pre-registered |
| uniqueness of every infinite-volume ground state | **not provable with admitted tools** | outside this route |
| any rate or estimate uniform in `a` | not provable, and not meaningful here | fixed spacing |

---

## (b) Dynamics: Lieb–Robinson/Duhamel comparison of F1 and F2 on compact windows

**Setup (AQ1 §3).**
- ℓ1 metric; `F(r) = (1+r)^{-4}`; `||F|| ≤ 7`; `C ≤ 224`;
- `||Φ||_F ≤ 81J ≤ 2268|τ|` (whole stars, ℓ1 diameter 2) and `||Φ'||_F ≤ 1323|τ|` (owner-set indexing, AY1 reverse);
- unbounded on-site terms placed in Nachtergaele–Sims arXiv:1410.8174 through the interaction picture;
- normalized time `u = θ/8` with `θ = αt/ħ` (δ = α/8).

The candidate Lieb–Robinson form is `||[τ_u(A), B]|| ≤ (2||A|| ||B||/C)(e^{v|u|} − 1) sum_{x,y} F(d(x,y))` with `v = 2C||Φ||_F`. **The producers must quote the form verbatim from the source.** If the source's constant differs, every number below rescales.

**Duhamel.** The two finite Hamiltonians on `Λ_N` share `H_0`, and `ΔH = H^{F2}_N − H^{F1}_N = sum_{f ∈ extra} V_f` is bounded, with `||V_f|| = |τ|/3` and `28N(5N+1)` extra faces. So

`τ^{F2}_u(A) − τ^{F1}_u(A) = i ∫_0^u τ^{F2}_s([ΔH, τ^{F1}_{u−s}(A)]) ds`.

The outer evolution is isometric. Only the **inner** F1 evolution needs the Lieb–Robinson bound, so only `Φ`'s constants enter. Every extra face has all its owners on a layer `|b_i| = N`, so its ℓ1 distance from `R` is at least `N−1`. With `|R| = 2` and at most three owners,

`||τ^{F2,N}_u(A) − τ^{F1,N}_u(A)|| ≤ 2||A|| · 56|τ|(5N+1)N^{-3} · (e^{vU} − 1 − vU)/(vC)`,

for `|u| ≤ U`, with `v = 1016064/10^8 ≈ 0.01016` per unit `u` at the cap. The directed bound is `e^x − 1 − x ≤ (x²/2)/(1 − x/3)`. The leading form is `2||A||·56|τ|(5N+1)N^{-3}·||Φ||_F U²`, **quadratic in τ**: the exact ratio at `τ` against `τ/100` is 10033.6, inside `[9900,10100]`.

| window | N=2 | N=5 | N=10 | N=100 |
|---|---|---|---|---|
| `θ ≤ 1` (`U = 1/8`): F1 vs F2 | 5.46e-13 | 8.26e-14 | 2.03e-14 | 1.99e-16 |
| `θ ≤ 8` (`U = 1`): F1 vs F2 | 3.50e-11 | 5.30e-12 | 1.30e-12 | 1.28e-14 |
| `θ ≤ 64` (`U = 8`): F1 vs F2 | 2.30e-9 | 3.48e-10 | 8.52e-11 | 8.37e-13 |
| `θ ≤ 8`: F1 Cauchy (`N → ∞`) | 1.02e-10 | 2.55e-11 | 1.13e-11 | 1.03e-12 |

All entries are in units of `||A||`. The F1 Cauchy row uses `2||A||·|R|·28|τ|·4/(N−1)·(e^{vU}−1−vU)/(vC)`: the stars not in `Λ_N` meet only sites with `|y|_∞ ≥ N`, and the shell sum is `sum_{r≥N−1}(4r²+2)(1+r)^{-4} ≤ 4/(N−1)`.

**N-dependence.** With AQ1's **polynomial** `F`, the same-`N` comparison decays like `N^{-2}` and each family's Cauchy rate is `O(1/N)`. An exponential `F_μ(r) = e^{−μr}(1+r)^{-4}` is admissible for this finite-range interaction: `C_{F_μ} ≤ 224` by the triangle inequality, and `||Φ||_{F_μ} ≤ e^{2μ}·81J` in ℓ1. It would give `e^{−μ(N−1)}` with a velocity multiplied by `e^{2μ}`. That is a **new constant instance**, labelled as such and never mixed with AQ1's.

**What "boundary independence of dynamics" can honestly mean:**
1. **Algebraic (Heisenberg) dynamics.** For `A ∈ B(H_R)` and a compact window `|θ| ≤ Θ`, the F1 and F2 finite-volume evolutions differ by the explicit `O(τ²Θ²N^{-2})` above. Both converge, **as whole sequences** (dynamics needs no compactness), in norm, uniformly on the window, to one automorphism group of the quasi-local algebra. This closes AY2 row O5.
2. **Row O6.** The F2 finite dynamics converge to the AQ1 dynamics. Rerunning AQ1 §§4–5 with F2's own subsequences then gives stationarity, GNS continuity and `H ≥ 0` for F2's limits.
3. **What it does not mean:**
   - equal GNS dynamics or equal correlation functions `ω(A* τ_θ(B))` of *different* states; that needs (a);
   - uniformity in time (the bound grows like `Θ² e^{vΘ/8}`);
   - real-time decay, or a gap of the limit;
   - uniformity in `a`;
   - norm continuity in time on all of `B(H)` (AQ1 control).

**Classification: likely provable with admitted tools.** It is a known-theorem application with AQ1 constants and an elementary Duhamel sum. The risks are three: domain care with unbounded `H_0` (bounded `ΔH`, interaction picture); quoting the Lieb–Robinson constant form verbatim; and deriving the extra-face count and distance by enumeration plus an all-size argument.

---

## (c) Consequences if a limit exists

- **AV2 and AW2.** The certificates already quantify over *every* subsequential limit. A proved limit turns them into statements about one object, the limit of the named construction. **The radius and the enclosure do not change**, so this is a restatement, not a strengthening:
  - AV2: `|C(s) − e^{-3s}/4| ≤ 1.83e-7` at `s = 1`, `reference_unresolved`;
  - AW2: `ω(W) ∈ [6.91e-11, 6.98e-11]` at the AW2 coupling, `static_not_dynamic`.

  AV2 and AW2 concern F1 (AQ1 provenance). They cover F2 only through a proved common limit. The Round32 gates are immutable, so restatements go in new files.
- **AX2.** The uniform-model node transfers only after the chain is re-instantiated for route B. That instance has different constants: `J' = 29|τ|`, `J_0' = 29/10^8`, single-factor groups of diameter 0, 52 faces per factor, reset `102|τ|`, and a recomputed `||Φ||_F`.
- **AY1 and AY2.** For F1 and F2 the pair distance `2D` and the `2K_2'τ²` second-order difference collapse to 0. The AY2 falsifying pair is excluded for these two families, and only for them. Rows O1 (restricted to the named families), O2 and O4 close; O3 closes (coarse) with the general-volume item; O5 and O6 close through (b). What remains: uniqueness among all infinite-volume ground states, and everything uniform in `a`.
- **Correlation functions** `ω(A* τ_θ(B))` and the GNS dynamics of F1 and F2 coincide, once **both** (a) and (b) are admitted.
- **Optional derived item.** Finite-volume nodes converge, `C_N(s) → C(s)`, with an explicit rate. The window tail is `∫_{|θ|>Θ}|ĝ| ≤ 8s³/(3πΘ³)` (8.5e-4 at `Θ = 10`, 8.5e-7 at `Θ = 100`, `s = 1`). The dynamics error is `O(Θ²)`. The state difference must be taken on the region the Lieb–Robinson approximation of `τ_θ(W)` requires, not on `R`. This must be pre-registered if wanted.

---

## (d) Applications stage: transfers, with every obstruction retained

**Group transfer (exact checks in scratch, Weyl integration by constant-term extraction).**

The last two columns use the declared convention: `h = 8 sum C_e`, `V = −(τ/3) sum W_f`, `W = Re Tr U/dim`, face energy `32 C_F`. They are labelled illustrations; the transfer must freeze its own convention.

| group | central `z` acting as −1 on the Wilson representation | flip lemma | parity rule `E[W^3] = 0` | `E[W^2]` | first-order `ω(W)` coefficient |
|---|---|---|---|---|---|
| SU(2) (reference) | yes (`−1`) | yes | yes (`0`) | 1/4 | 1/144 (admitted, I1.5) |
| U(1) | yes (`e^{iπ}`) | yes | yes (`0`) | 1/2 | 1/96 |
| Z2 | yes | yes | yes (`0`) | 1 | 1/48 (with the electric term normalized to 1 on the odd state) |
| SU(4) (any SU(2k)) | yes (`−I`, `det = 1`) | yes | yes (`0`; `E[W^4] = 7/2048`) | 1/32 | 1/2880 |
| **SU(3)** | **no** (center Z3) | **no** | **no: `E[W^3] = 1/108`, `E[(Tr U)^3] = 1`** | 1/18 | 1/1152, not odd in τ |
| SO(3), G2 | no (trivial center) | no | no | — | — |

**The SU(3) obstruction is quantitative.** Only `f = W` survives, and `∂_τ ω(W²)|_0 = 2(1/3)E[W³]/(128/3) = 1/6912` under the convention. The Duhamel term `E[W W_f W]` is likewise nonzero. So for SU(3) the centered correlation *does* shift at first order. The Round32 statement that a first-order centered shift is "empty by representation theory" is an SU(2)/even-center fact.

**Traps:**
- **U(1):** one-dimensional irreps and the "Casimir" `n²`. At weak coupling it is in the Coulomb phase (gapless), so any gap or expansion statement is strong-coupling only and carries that label.
- **Z2:** a finite group with `W² = 1`, and the electric-term normalization is a convention.
- **SU(N ≥ 3):** `W²` contains two-index representations, so every second-order constant (`K_2^+`, `K_2'`) must be rederived.
- **The dictionary does not transfer.** `τ = 96/g⁴` and `α = g²/(2a)` are SU(2) Kogut–Susskind in 3+1D.
- **No gap or AM2 chain transfers without re-instantiation.** The onsite gap is `8 C_F` for SU(N) and 8 for U(1) under the convention, and every constant must be re-derived.

**Two spatial dimensions.** The flip set `E_2 = {(p,x): p_y even}` meets every square plaquette exactly once; this was checked on a box. Everything else must be recounted. The I1 coarse factor (`4×2×1`, 24 links, selected strips) has no fixed 2D analogue, so a 2D factorization must be declared. With single-site factors owning `(p,x), (p,y)`: owner sets `{p, p+e_x, p+e_y}`, 3 faces per site, stars `{p, p+e_x, p+e_y}`, and `J`, `d_X`, the incident anchors, the cover, the shell counts `4r` and the Nachtergaele–Sims constants all recomputed. `g²` has mass dimension in 2+1D, so the dictionary changes. The words "prediction" and "continuum" are forbidden.

**Other observables:**
- **Larger Wilson loops.** The first nonzero order is the minimal tiling area: order 2 for a `1×2` loop. The first-order mean is exactly 0. The admitted machinery gives only an upper bound `|ω(W_{1×2})| ≤ K(R')τ²` on a recounted cover `R'`, with its incident anchors and faces recounted. **The sign is obstructed**: it needs the exact `c^(2)` and a uniform third-order remainder, neither of which is admitted.
- **Electric energy on R.** `h_R ≥ 6Q_R` in the zero-selected family. Positivity of `ρ_R` with the AY2 off-diagonal gives a static two-sided band: `6(√10|τ|/144 − K_2'τ²)² ≈ 2.86e-19 ≤ ω(h_R) ≤ 98|τ| = 9.8e-7` (δ units). The second-order value is at most about `τ²/18 ≈ 5.6e-18`, but a tight enclosure is **obstructed**: `h_R` is unbounded, and a bounded-observable constant cannot be used.

**Finite graphs.** Round10's one square and Round11's two squares, possibly for U(1) or Z2. A one-link flip makes `⟨W⟩` odd in the coupling, as AZ2 used. Each graph carries its own model id, couplings named term by term (rule R3), its own free reference, `transfers_to_aq: false`, and no fitted coefficients.

**Site calculators.** They display gate-bound values only: tables of `C q^N` and the dynamics bounds. The domain is restricted to `N ≥ 2`, `|τ| ≤ 10^-8`, the declared window, and `s` below the crossover. They never compute an admission. Renderer tests use synthetic fixtures.

**No transfer is ever called a prediction.** An equation that does not transfer is recorded with its exact counterexample.

---

## (e) Traps across the round

1. **Named construction versus uniqueness.** "F1 and F2 converge to a common limit" is not "the ground state is unique". The gate must say "the limit of the named constructions", or name a pre-frozen AM2-admissible boundary class. It never says "the thermodynamic limit", "the infinite-volume ground state" or "the AQ state".
2. **A rate in N is not a rate in a.** It is per coarse ℓ∞ step, at fixed spacing and strong bare coupling. It is not a correlation length.
3. **Round32 contract-defect patterns.** The freezer rejects placeholders (R1), a missing template field (R2), unnamed finite-model couplings (R3), vocabulary copied across model families (R4), a missing statement-target note (R5) and a missing `selected_after` note (R8). I add:
   - the topic gate fields `whole_sequence_claimed`, `rate_in_N_claimed`, `common_limit_claimed`, `uniqueness_all_ground_states_claimed` and `dynamics_level`;
   - the metric, weight, `d_X`, window and clock declared in `parameters`;
   - a scaling bracket per constant.
4. **Tier mixing.** A closed tier vocabulary (rule R10): `crude_i`, `exact_first_order_ii`, `weighted_i`, `weighted_ii`, `lr_polynomial` and `lr_exponential`. A refined tier needs its own self-consistent inequality (`t_μ ≤ w t_1/(1 − J w G'(R))`). A crude Lipschitz constant with an exact source is fine only if labelled.
5. **The sentence-template span rule (R7).** Gates quote the template as one unbroken span. Phrase scans are whole-sentence and negation-aware (R6, `phrase_scan.py`).
6. **Isolation:**
   - Reverse producers for BA1 and BB1 must not receive this triage, the lens memos proposing the same route, the deliberations or the forward files.
   - Producers disclose their private scratch folders and any name-only exposures.
   - Commit order is recorded as it happened.
   - My own exposure (§Standing) is on record.
7. **Cross-coupling comparisons.** Every convergence statement holds at one coupling. The `±τ` limits differ by at least 8.76e-10 (AY2).
8. **Round32 wording lessons, amended.** "Uniqueness of any subsequential limit" is now provable only in the form "all subsequential limits of F1 and F2 coincide". It must be stated with the named families.

---

## Recommended plan (three research sub-rounds and applications)

Directions: `paired` means forward and reverse producers with genuinely different routes; `single+skeptic` means one producer plus the skeptic's pre-comparison replay; `statement+skeptic` is a statement loop. The machine-readable version is `recommendation.json`.

**Sub-round BA (foundations; the two loops are independent):**
- **BA1 (paired). Weighted AM2 contraction and boundary-source decay of creation coefficients.**
  - Forward: diameter-weight and boundary-weight norms.
  - Reverse: analyticity on `|z| ≤ τ_*` with order against distance.
  - Coverage: F1 with `N → N+1`, F2 with `N → N+1`, F1 against F2 at the same `N`, and general volumes through the union.
  - Candidate frozen target: tier (ii) `K ≤ 1/2000000` at `q = 1/64` in coarse ℓ∞, at `|τ| = 10^-8` and both signs (preview 2.2004e-7, margin 2.27). Tier (i) is reported (preview 2.897e-4).
- **BA2 (paired). Lieb–Robinson/Duhamel comparison of the F1 and F2 dynamics; whole-sequence convergence of the algebraic dynamics; O6.**
  - Forward: direct Duhamel over the extra faces.
  - Reverse: each family against its own Nachtergaele–Sims limit (`Φ`: 2268|τ|; `Φ'`: 1323|τ|), with a proof that the two limits are equal.
  - Candidate targets for `|θ| ≤ 8` and `N ≥ 2`: `≤ 6·10^-11 (5N+1)N^{-3}||A||` (preview 2.549e-11) and an F1 Cauchy bound `≤ 2.5·10^-10/(N−1)||A||` (preview 1.0195e-10).

**Sub-round BB:**
- **BB1 (paired). Marginal locality of normalized creation-product states** (the new lemma).
  - Forward: iterated R-vacuum ordering.
  - Reverse: polymer representation with a Kotecký–Preiss criterion.
  - Target: `η ≤ 1/100` at tier (ii) with the frozen weights; `κ_0` and `w'` exact.
- **BB2 (paired). Whole-sequence convergence on every finite region, a common F1/F2 limit, identification with every AQ1 subsequential limit, and coarse translation invariance** (pre-registered item).
  - Target: `C_∞(R) ≤ 2·10^-6` at `q = 1/64`, tier (ii) (preview 8.94e-7), with a mandatory template stating "named constructions, not uniqueness of every infinite-volume ground state".

**Sub-round BC:**
- **BC1 (statement+skeptic). Consequences:** AV2 and AW2 restated for the limit; AY1/AY2 and the obligations table updated; common correlation functions and GNS dynamics (needs BA2 and BB2); optional pre-registered finite-volume node-convergence rate.
- **BC2 (single+skeptic). Route-B uniform model:** BA1, BB1 and BB2 re-instantiated with its own constants, making AX2 a statement about the limit. The advisor may substitute a pre-frozen AM2-admissible boundary-class item if BB succeeds early.

**Sub-round BD (applications):**
- **BD1 (statement+skeptic, exact checks per cell). Group and dimension transfer ledger:** the parity theorem, the flip lemma, the first-order mean and the dictionary. Transfers: U(1), Z2, SU(4). Obstructions: SU(3), SO(3). Plus the 2D flip set and recounts.
- **BD2 (single+skeptic). Observables and finite graphs:** the first nonzero order of larger loops with upper bounds; the electric-energy band; the one-square and two-square graphs for U(1)/Z2. The calculators are a presentation deliverable.

**Fallbacks.**
- If BB1 fails, BB2 is `limited` (coefficient locality only) or `insufficient`, and it is retained. BA2 stands on its own.
- If BA1 fails, the analyticity route is kept as a labelled observation, and BB is re-planned under the goal-change rule.

**I will veto a freeze in these cases:**
- a veto condition listed in `recommendation.json` for that loop;
- a target with margin below 2;
- any reverse inventory containing this triage;
- any contract phrase "uniqueness of the ground state", "the thermodynamic limit" or "correlation length";
- a scaling bracket not declared per constant;
- the metric, weights or clock not in `parameters`.

## What I require of every producer

1. **Protocol.** Read AGENTS.md and the contract. Snapshot every premise byte for byte. Freeze with `freeze.py`. Run `check.py --output <fresh absolute dir>` under `-B`, with byte-identical normal and `-O` replays.
2. **Exact arithmetic.** Admission values use `Fraction` with directed enclosures (exp, log, π, √). Arb and mpmath are labelled previews and are never imported on the admission path.
3. **Constant labels.** Every constant names its tier, norm and topology, metric, weights, family, cutoff status, sign convention and clock (`θ = αt/ħ`; `u = θ/8` only internally, with the conversion shown).
4. **Admitted constants** are parsed from gate and report snapshots, with the gate sha256 pinned in `check.py` (AY2 N4). No retyping.
5. **Model label:** zero-selected patterned family (or route-B uniform), fixed spacing, `|τ| ≤ 10^-8` at both signs, centered cubes `N ≥ 2`, cover `R`.
6. **Quantifiers:** whole sequence or subsequence; "named construction(s)" or the frozen class. Never "the AQ state", "the thermodynamic limit" or "unique ground state".
7. **Controls.** Every contract control id is a damaging mutation, with explicit exceptions that stay active under `-O`, and the mirror equals the pre-registration.
8. **Failures are retained.** A missed target is reported as `limited` or `insufficient` with its dominating term. `q`, `μ`, `N_0` and `τ` are never retuned.
9. **Fixtures** for each trap, labelled `model_is_finite_graph: true` and `transfers_to_aq: false`:
   - normalization;
   - straddling dependence;
   - coefficient decay against marginal decay;
   - fixed vector against moving vector;
   - polynomial against exponential Lieb–Robinson tail.
10. **Claim flags exported:** `continuum_claim`, `uniqueness_all_ground_states_claimed`, `uniform_in_a_claimed`, `scientific_priority_verified`, `weak_coupling_claim` (all false); `whole_sequence_claimed`, `rate_in_N_claimed` and `common_limit_claimed` (true only if proved); `dynamics_level`; `transfers_to_aq`.
11. **Scaling.** A `τ → τ/100` scaling check of each headline constant against its declared bracket.
12. **Isolation.** Private scratch disclosed; the other producer and the skeptic's package are not read before freeze; the reverse inventory is validated; name-only exposures and commit order are disclosed.
13. **Template.** The mandatory template is quoted once and unbroken; `phrase_scan.py` is clean.
14. **Attribution.** Known theorems are credited (Nachtergaele–Sims; Kotecký–Preiss; creation expansions per the Gauvin diff record; Yarotsky). Scientific priority stays unverified.
15. **Authorship.** Human author: Hruday N M (BUNZEEY). AI assistance is disclosed.

## Numbers at a glance (previews; exact rationals in scratch, to be re-derived)

| quantity | value |
|---|---|
| admitted sup-norm coefficient difference (no decay) | `37/6249384 ≈ 5.92e-6` |
| weighted self-map limit / `q_min` (coarse ℓ∞) | `390625/148 ≈ 2639` / `148/390625 ≈ 3.79e-4` (= `|τ|/τ_*`, `τ_* = 1/37888`) |
| `q_min` in ℓ1; with cardinality weights | 0.0195; 0.1395 |
| `w = 64` coupling threshold | `1/2424832 ≈ 4.12e-7` |
| `K_i`, `K_ii` at `q = 1/64` | 2.8971e-4; 2.2004e-7 |
| `C_∞` tier (i), tier (ii) at `q = 1/64` | 1.1773e-3; 8.9415e-7 (before η) |
| `K_ii` scaling ratio (τ against τ/100) | 101.030 (outside `[99,101]`) |
| dynamics F1 vs F2, `θ ≤ 8` | `2.549e-11 (5N+1)N^{-3} ||A||` (quadratic in τ) |
| dynamics F1 Cauchy, `θ ≤ 8` | `1.0195e-10/(N−1) ||A||` |
| SU(3) `E[W^3]`, `∂_τ ω(W²)` | 1/108; 1/6912 (convention) |
| electric-energy band on R (δ units) | `[2.86e-19, 9.8e-7]` |
