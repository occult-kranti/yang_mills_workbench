# BA1 independent derivation before producer comparison

**Standing.** I wrote this after the BA1 contract froze (`frozen_at` 2026-09-24T21:56:46Z, sha256 `2c761366…32b9`). I have not opened, listed or read `research/round33/forward/ba1/`, `research/round33/reverse/ba1/`, `research/round33/forward/ba2/` or `research/round33/reverse/ba2/`. The one exception, which the task permits: I ran `find` on the two BA1 `inputs/` folders and hashed each file name there against the repository.

**Sources:**
- the frozen contract, `advisor/selection-ba1.md`, `advisor/deliberation-2.md` (the recorded previews) and `advisor/plan.json`;
- my Round33 record: `triage.md`, `prospective-controls.json`, `recommendation.json`, `loop2-review.md` and `.json`;
- my Round32 AY1 package (format only);
- the premises: AM2 forward, reverse, skeptic review and gate; AQ1 forward and gate; I1 forward; AV1 forward and gate; AW1 forward and gate; AY1 gate; AY2 gate; `AGENTS.md`.

**Scratch.** All scratch work stayed in the private folder `/tmp/claude-0/skeptic-ba1-private/`. I read nothing in any other agent's scratch folder. That includes my own loop-1 and loop-2 scratch folders: every number here was recomputed from scratch.

**Name-only exposures, disclosed.** None of these was opened:
- `git status` printed the untracked names `forward/ba1/check.py`, `forward/ba1/report.md`, `reverse/ba1/check.py`, `reverse/ba1/report.md` and the BA2 equivalents.
- `git log` printed the subject line of the BA2 skeptic commit 7daf273. I did not read that package.
- A listing of `/tmp/claude-0/` showed other agents' folder names, among them `ba2-forward-private`.

**Correlated ancestry.** I am a model-agent skeptic with correlated ancestry. My triage (a).2–(a).5 proposed both routes, and my loop-2 edits wrote the frozen weights, disc radii, floor target and brackets. What follows is a re-derivation, not independent discovery or human review.

**Exactness.** Exact values come from `ba1_check.py`: 101 checks, 37 of which are contract controls executing 90 damaging mutations. Every decimal below is a preview. Human project author: Hruday N M (BUNZEEY).

## 1. Model and the admitted objects used
The model is the zero-selected patterned family:
- SU(2) Kogut–Susskind form on Z³ at fixed spacing, with coarse 24-link factors;
- selected triple (0,0,0) with the Haar product reference;
- 21 omitted faces per anchor entering as `−(τ/3)W_f` (I1.5, δ=α/8);
- both signs, |τ|≤10⁻⁸;
- cover R={0,e_z}: 48 links, 36 endpoints, 7 incident anchors.

**Admitted objects.** The AM2 creation fixed point `c = Σ_k L_k(c,…,c)/k!` exists in each on-site cutoff space Q_L, with `‖L_k‖_a ≤ J·16·8^k(1+5k/4)∏‖c_j‖_a` and the following constants:

| constant | value |
|---|---|
| `J` | at most `J_0 = 28|τ| = 7/25000000` |
| `G(t)` | `16e^{8t}(1+10t)` |
| `G(R)` | below 148/7 |
| `G'(R)` | below 352 |
| `R` | 1/64 |

The exact first order is `c^(1)=L_0=−(τ/72)Σ_f W_fΩ_0` (AW1), with `‖c^(1)_M‖=√n_M|τ|/144` (AV1 F15). From it:
- `‖c^(1)‖_a ≤ t_1 = 49|τ|/144`;
- the remainder satisfies `‖c−c^(1)‖_a ≤ J(G(t)−16)`.

For L≥24 the first-order vector is exact. For smaller L some face vectors are annihilated, so the counts only decrease.

**Families.** Both families have `J≤28|τ|`, supports of size at most 4, and termination at order 8 (AY1 gate):
- F1: AQ1 whole stars on `Λ_N=[−N,N]³`.
- F2: I1 §6 faces whose owner set lies in `Λ_N`, grouped at their anchors. The padding carries no interaction, so coefficients on supports meeting the padding vanish.

**Geometry, enumerated.**
- The I1 table is parsed and matches the computed classes: 24 classes, 21 omitted.
- The star S has l∞ diameter 1 and l1 diameter 2.
- Every omitted owner set contains its anchor and has l∞ diameter 1 and l1 diameter 1 or 2.
- The counts 49/15/82/10 follow by translation covariance, with owner-set multiplicities {1×5, 2×3, 3×2, 4×3, 10×2}.
- On Λ_2 and Λ_3:
  - every star has diameters (1,2);
  - every F1 and F2 owner set has l∞ diameter 1;
  - each site lies in at most 4 stars and at most 49 faces;
  - 7 stars and 82 faces meet R.

## 2. The weighted contraction (forward route)
**Lemma W (subadditivity through the interaction).** In a nonzero word (X; I_1,…,I_k), every I_j meets X (a disjoint creation commutes innermost) and `N∖X ⊂ M ⊂ N∪X`, where `N=∪I_j`. Pick `x_j ∈ I_j∩X`. For p∈I_i and p'∈I_j,

`d(p,p') ≤ diam I_i + d(x_i,x_j) + diam I_j`.

Hence `diam M ≤ d_X + (sum of the two largest diam I_j) ≤ d_X + Σ_j diam I_j`.

The loss `d_X` is attained. The k=0 term has diameter 1 with no creation. Over all 13 881 admissible words of order at most 2 built from actual owner sets around the star at 0, the largest excess `diam M − Σ diam I_j` is exactly 1 in l∞ and 2 in l1. The shortcut `d_X + max_j diam I_j` fails on 2 112 of these words. A disconnected witness is `I_1={e_x,2e_x}`, `I_2={0,−e_x}`, `M=N∖X={2e_x,−e_x}`: here `diam_∞ M = 3 = 1+1+1`, while the max shortcut gives 2.

**Weighted estimate.** Define `‖c‖_w = max_u Σ_{I∋u} w^{diam_∞ I}‖c_I‖`. Lemma W gives `w^{diam M} ≤ w^{d_X}∏_j w^{diam I_j}`, so the AM2 counting passes through unchanged:
- 16 output sets;
- `|I_j| ≤ |M|+4`;
- the `1/|M|` cancellation;
- `2^k` products.

Therefore

`‖L_k(c_1,…,c_k)‖_w ≤ w^{d_X}·J·16·8^k(1+5k/4)·∏_j‖c_j‖_w`, with `d_X=1`.

**The loss is paid once per interaction, never per creation.**

**Self-map and fixed point.** Weights are at least 1, so the weighted ball `B_w(R)` lies inside the AM2 ball. If `J w G(R) ≤ R`, the AM2 iteration from 0 stays in `B_w(R)`, which is closed in finite dimension, so the unique AM2 fixed point lies there. With the rational bound, `J_0 w (148/7) ≤ 1/64` holds exactly when `w ≤ 390625/148` (≈2639.36). At the upper end this is an equality of the bound, and the inequality is strict in truth.

| weight | self-map `J_0 w G(R)` | Lipschitz `J_0 w G'(R)` | `T_w` (exact first order) | crude `t_w` |
|---|---|---|---|---|
| w=64 (headline) | 148/390625 | 2464/390625 | 49/223580736 ≈ 2.19160e-7 | 148/390625 |
| w=390625/148 (floor) | 1/64 | 77/296 | 49/4036608 ≈ 1.21389e-5 | 1/64 |

Here `T_w = w t_1/(1−J w G'(R))`. It follows from:
- `‖L_0‖_w = w‖L_0‖_a ≤ w t_1`, because every first-order owner set has diameter exactly 1;
- `G(t)−16 ≤ tG'(R)` for t≤R.

The weighted Lipschitz condition `J_0 w G'(R) < 1` needs only `w < 781250/77` and never binds. The coupling threshold for w=64 is `|τ| ≤ 1/2424832` (the cap lies 41 times inside it).

## 3. The order-versus-distance lemma
**Statement.** Let `V' = V + V^new` be two admissible interactions of the named constructions in one cutoff space. Let `𝒮` be the union of the supports of the new terms, and let `d_X` bound every term's diameter. Then

`[z^n](c'_I − c_I) = 0` unless `n ≥ 1 + max_{u∈I} ⌈d(u,𝒮)/d_X⌉`.

**Proof.** An order-n coefficient on M is a sum over rooted trees of n interaction terms, by induction on the recursion. The supports of those terms form an intersection-connected family whose union contains M:
- M lies in `X ∪ ∪I_j`;
- each `I_j` comes from a subtree whose union contains `I_j`;
- each `I_j` meets X.

Trees made only of old terms are identical in both boxes: they are the same operators on the same sectors, with the extra sites in vacuum. A tree that contains a new term X_new and reaches u ∈ M contains a chain `X_1∋u, X_2, …, X_m=X_new` in which consecutive terms intersect. Then `d(u,X_new) ≤ (m−1)d_X`, and `n ≥ m`.

**Convention.** The proof uses the coarse l∞ metric with `d_X=1`. The l1 reading (`d_X=2`) is a labelled alternative, never mixed with it.

**The contract's form.** The contract states the lemma as "order at least ⌈d/diam⌉". That is valid but **one order weaker**.

**Tables (full versions in `results.json`).** For every term X of the box, the chain order `1+d_G(R,X)` comes from breadth-first search on the site graph. The F1 face and star site graphs are identical (checked). In l∞, the minimum chain order equals `1+d` at every distance, in both families and all three boxes. The maximum exceeds it (corners need more steps).

| Λ_N, family | d_∞(R,X): terms (min order, max order) |
|---|---|
| Λ_2 F1 | 0: 82 (1,1) · 1: 737 (2,4) · 2: 525 (3,6) |
| Λ_2 F2 | 0: 82 (1,1) · 1: 800 (2,4) · 2: 1078 (3,6) |
| Λ_3 F1 | 0: 82 · 1: 962 (2,4) · 2: 2281 (3,7) · 3: 1211 (4,9) |
| Λ_3 F2 | 0: 82 · 1: 962 (2,4) · 2: 2436 (3,7) · 3: 2400 (4,9) |
| Λ_4 F1 | 0: 82 · 1: 962 (2,4) · 2: 2866 (3,7) · 3: 4665 (4,10) · 4: 2177 (5,12) |
| Λ_4 F2 | 0: 82 · 1: 962 (2,4) · 2: 2866 (3,7) · 3: 4952 (4,10) · 4: 4242 (5,12) |

In l1, the bound `1+⌈d_1/2⌉` holds everywhere and is slack at large d_1. For example, on Λ_4 F1:

| d_1 | min order | max order | bound `1+⌈d_1/2⌉` |
|---|---|---|---|
| 0 | 1 | 1 | 1 |
| 1 | 2 | 2 | 2 |
| 2 | 2 | 3 | 2 |
| 3 | 3 | 4 | 3 |
| 4 | 3 | 5 | 3 |
| 5 | 4 | 6 | 4 |
| 6 | 4 | 7 | 4 |
| 7 | 5 | 8 | 5 |
| 8 | 5 | 9 | 5 |
| 9 | 6 | 10 | 6 |
| 10 | 7 | 11 | 6 |
| 11 | 9 | 12 | 7 |

The l1 convention therefore gives roughly the square-root rate. It cannot realize q=1/64 per step: `J_0·64²·G(R) = 9472/390625 > 1/64`, and `q_min` per l1 step is `(148/390625)^{1/2} ≈ 0.019465`.

**Algebraic fixture.** The model is `FG(qubit chain, H = Σn_x + zΣX_iX_{i+1})`, with `transfers_to_aq:false`. I computed the creation fixed point exactly as Taylor polynomials, and the eigen-equation residual of `e^{−C}Ω` vanishes to the truncation order. Adding a bond at distance d from site 0 changes the coefficients through 0 first at order `1+d`:
- d=2: order 3, with `c_{0,3}: +5/8 z³`;
- d=3: order 4, with `c_{0,4}: −7/8 z⁴`.

The contract form ⌈d⌉ is one below.

## 4. Boundary sources and exact distances (all sizes)
Enumerated at N=2,3,4 (Λ_5 is used for the nested N=4 case), with formulas checked:

| comparison | new terms (count) | at N=2,3,4 | source set B | new supports inside B | max new faces/site | J_new |
|---|---|---|---|---|---|---|
| F1 N→N+1 | whole stars `b∈[−N−1,N]³∖[−N,N−1]³`: `8(3N²+3N+1)` stars, `168(3N²+3N+1)` faces | 152/296/488 stars | shell | no | 49 | 28\|τ\| (4 stars at (N,N,N)) |
| F2 N→N+1 | faces with owner set in Λ_{N+1}, not in Λ_N: `56(9N²+14N+6)` | 3920/7224/11536 | shell | no | 45 | 15\|τ\| (face level) |
| F1 vs F2 at N | extra F2 faces: `28N(5N+1)` | 616/1344/2352 | outer layer `max_i\|b_i\|=N` | **yes** | 38 | 38\|τ\|/3 (face level) |

**Distances (all three comparisons, every N):**
- `d_∞(e_z,𝒮) = d_1(e_z,𝒮) = d_G(e_z,𝒮) = N−1`;
- `d_∞(0,𝒮) = N`;
- shell: N from e_z and N+1 from 0;
- outer layer: N−1 from e_z and N from 0.

**All-size argument:**
- F1 nested: a new star has `b_i=N` for some i (its sites have `p_i≥N`) or `b_i=−N−1` (its sites have `p_i≤−N`).
- F2 nested: a new owner set contains a site with `|p_i|=N+1` and has diameter 1, so `|p_i|≥N`.
- F1 against F2: the anchor has `b_i=N`, and every site of the face shares `p_i=N`.

In every case the nearest site is `(0,0,N)`: it lies in the star anchored there, in the face `{(0,0,N),(0,0,N+1)}`, and in the five extra faces at anchor `(0,0,N)`. So by the lemma the sharp order is `N` at e_z and `N+1` at 0, while the contract form gives `N−1` and `N`.

**F1 against F2, regrouped at anchors and charged once.** The group size depends only on which coordinates of the anchor equal N:

| saturated coordinates | x | y | z | xy | xz | yz | xyz |
|---|---|---|---|---|---|---|---|
| group size | 17 | 13 | 5 | 10 | 3 | 1 | 0 |

The total is `(2N)²·35 + 2N·14 = 28N(5N+1)`, with each face once.

**F2 nested, face by face.** Charging whole regrouped anchors instead would recharge `56(9N²+14N+6) + 28N(5N+1)` faces (4536/8568/13888): the old clipped faces twice.

**Every pair of centered boxes is nested.** As face sets, `F1_N ⊂ F2_N ⊂ F1_{N+1} ⊂ F2_{N+1}`. All 15 pairs on Λ_2..Λ_4 have their new supports at distance N−1 from e_z and N from 0, with N the smaller size. So "any two centered boxes" needs neither telescoping nor a cross-family triangle.

**General volumes.** Every term of one volume missing from the other contains a site outside `Λ_N`, so it lies at distance at least N−1 from e_z and at least N from 0. I checked this on two non-centered cuboids at N=2,3, for both prescriptions, both directly and through the union.

## 5. The difference bound, forward route
**Setup.** Write `c = c^Λ`, extended by zero, and `c' = c^{Λ'}`. Linearity in V gives

`δ = c'−c = S + [F'(c')−F'(c)]`, where `S = Σ_k L_k^{V^new}(c,…,c)/k!`.

Use the difference norm `‖δ‖_{B,β} = max_u Σ_{I∋u} e^{βρ_B(I)}‖δ_I‖`, with `ρ_B(I) = max_{p∈I} d_∞(p,B)` and `e^β ≤ w`. Following Lemma W:
- **Source term.** `ρ_B(M) ≤ σ + Σ_j diam I_j`, where `σ = max_{X new} ρ_B(X)`. Here σ is at most `d_X` because X meets B, and `σ=0` when X⊂B.
- **Telescoped Lipschitz term** (δ-slot on `I_δ`). `ρ_B(M) ≤ ρ_B(I_δ) + d_X + Σ_{j≠δ} diam I_j`. The other creations must carry their diameter weights. A pure distance weight without them undercharges: the fixture word has excess 2 against the charged 1.

Hence, with `T=T_w`:

`‖δ‖_{B,β} ≤ e^{βσ}[t_1 + J(G(T)−16)] / (1 − J e^β G'(T))` for the exact first-order tier,

and the same with `e^{βσ}JG(T)` in the numerator for the crude tier. Then

`Σ_{I∋u}‖δ_I‖ ≤ e^{−β d(u,B)} ‖δ‖_{B,β}`.

**Direction.** The weight grows with distance from B, that is towards R. The reversed weight fails, as the chain fixture shows in §8.

**Contract form.** Take σ = d_X = 1 with the exponent N−1 in every comparison. For nested comparisons, `d(e_z,shell)=N` gives this with one factor q to spare. Call the result `K = e^β X`.

**Sharp form (labelled).** Two routes give the same constant `X q^{N−1}`:
- nested comparisons with B = shell: σ=1 and exponent N;
- F1 against F2: σ=0 and exponent N−1.

| forward constant (both signs identical) | exact | preview | vs target |
|---|---|---|---|
| headline, exact first order, contract form | 7334358121462324769859517388959775878989442259/33331249407719528571734905225718909908536586717145768 | 2.2004450e-7 | ≤1/2000000, margin 2.2723 |
| headline, sharp (÷64) | (in results) | 3.4382e-9 | margin 145.4 |
| headline, crude (t_w≤148/390625) | (in results) | 2.9018e-4 | fails, retained |
| floor, exact first order, contract form (e^β=w=390625/148) | (in results) | 1.4693e-5 | ≤1/12, margin 5672 |
| floor, crude (t_w≤R) | (in results) | 2.0877e-2 (rational bounds only: 37/1752≈2.1119e-2) | margin 3.99 |
| general volumes through the union | 2K | 4.4009e-7 | margin 1.136 |

**The global Lipschitz constant is not a decay factor.** In the sup norm, `‖c^{N+1}−c^N‖_a ≤ J_0G(R)/(1−J_0G'(R)) = 37/6249384` for every N, with no decay. Using `2J_0G'(R)=77/390625` as a per-shell factor would put the rate below `q_min = 148/390625`.

## 6. The analytic route (reverse)
**Contraction on the disc.** With `J=28|z|`:
- the self-map `28ρG(R) ≤ R` holds exactly when `ρ ≤ τ_* = 1/37888` (equality in the rational bound);
- the Lipschitz constant is at most `28ρ·352 ≤ 77/296`.

The polynomial iterates converge uniformly, so `c(z)` is analytic. It is analytic on the open disc of radius `R/(28G(R)) ≥ 2.66197e-5 > τ_* ≈ 2.63936e-5`, a neighbourhood of both closed discs. At real z it coincides with AM2's fixed point (uniqueness).

**Discs:**

| pair | radius ρ | q = \|τ\|/ρ |
|---|---|---|
| headline | 64\|τ\| = 1/1562500 | 1/64 |
| floor | τ_* | 148/390625 |

**Sup bounds.** In the exact first-order tier, `T(ρ) = (49ρ/144)/(1−9856ρ)`, which gives `T(64|τ|) = 49/223580736 = T_w(64)` and `T(τ_*) = 49/4036608 = T_w(w_max)`. The weight w and the radius w|τ| are the same majorant. The crude bound is `28ρG(R)`, which is 148/390625 on the headline disc and R on the floor disc. Then `Σ_{I∋u}‖δ_I(z)‖ ≤ 2T(ρ)` on the disc.

**Estimate.** The Schwarz form (maximum principle for `δ(z)/z^{n_0}`, a subharmonic norm) gives `Σ_{I∋u}‖δ_I(τ)‖ ≤ M q^{n_0}`. Coefficientwise Cauchy adds `1/(1−q)`.

| reverse constant (both signs) | exact | preview | vs target |
|---|---|---|---|
| headline, 2T(64\|τ\|), Schwarz, n_0=N−1 | 49/111790368 | 4.3832e-7 | margin **1.1407** |
| same, coefficientwise | 14/31441041 | 4.4528e-7 | margin 1.1229 |
| same, first-order cancellation (labelled) | (in results) | 2.2622e-9 | margin 221 |
| same, sharp count n_0=N (labelled) | 49/7154583552 | 6.8488e-9 | margin 73.0 |
| headline, crude 2·28ρG(R) | 296/390625 | 7.578e-4 | fails, retained |
| floor, 2T(τ_*), Schwarz | 49/2018304 | 2.4278e-5 | margin 3432 |
| floor, crude 2R | 1/32 | 3.125e-2 | margin 2.667 |
| floor, crude 2R/(1−q) (the loop-1 preview form) | 390625/12495264 | 3.1262e-2 | margin 2.666 |
| general volumes through the union | 49/55895184 | 8.7664e-7 | **misses**; the direct comparison gives 4.3832e-7 |

**First-order cancellation.** For N≥2, all 49 faces through 0 and through e_z lie in both boxes, so `c'^(1)_I = c^(1)_I` for I∋u∈R. The sup is then `2J(ρ)(G(T)−16)`.

**Remainder at the ball radius.** A remainder charged at the ball radius, `J(G(R)−16)`, gives a sup of about 1.85e-4 at ρ=64|τ|, which fails.

**No extension to ρ_R.** None of this extends to the reduced density ρ_R. The complexified normalization may vanish, and a zero-free region is BB1's problem, not BA1's.

## 7. Scaling τ → τ/100 (exact ratios, same formula, no intermediate rounding)
| constant | ratio | bracket |
|---|---|---|
| headline forward, contract or sharp | 101.0304 | [95,105] ✓ |
| headline reverse | 4340004/43129 ≈ 100.6284 | [95,105] ✓ |
| floor forward, contract form (and crude) | exactly 1 | [99/100,101/100] ✓ |
| floor reverse, Schwarz | exactly 1 | ✓ |
| floor reverse, 2R/(1−q) | 1.000375 | ✓ |
| floor, sharp forms (either route) | exactly 100 | **rejected by the frozen bracket** (contract review R3) |
| q_min | exactly 100 | exactly 100 ✓ |

## 8. Exact fixtures for the traps
All fixtures are labelled finite graphs or finite algebras (`transfers_to_aq:false`) unless they are actual owner sets.

- **Weight growing from R fails.** On the chain `δ = e_L + (1/10)Aδ` (A = nearest neighbour plus identity, q=1/2):
  - exact `δ_0 = 10/711, 10/6319, 1/5616, …, 10/350382231` for L=2..8;
  - the weight growing from the source towards R gives `(5/8)2^{2−L}`, which decays;
  - the weight growing from R gives `10·2^{L−2}`, which grows with L.
- **The global Lipschitz constant is not decay.** With the rank-one all-to-all coupling `jP` (Lipschitz j=1/10), `δ_0 = 1/(9(L+1))` (1/27, 1/36, …). The claim `j^L/(1−j)` (1/90, 1/900, …) is false.
- **Per-creation loss fails.** In the actual model, `‖c‖_w ≥ ‖c^(1)‖_w − ‖c−c^(1)‖_w ≥ 1.11250e-7 − 1.131e-9`. The per-creation claim `t_1/(1−JG'(t_1)) ≈ 3.4031e-9` is exceeded more than 30 times.
- **Disconnected output and the max shortcut.** See §2.
- **Pure distance weight.** With `B={(10,0,0)}`, the word `(S; {e_x,2e_x}, {0,−e_x})` gives `ρ_B(M) − ρ_B(I_δ) = 2`, against the charge `d_X = 1`.
- **Coefficient decay is not marginal decay** (AV1 F13 type). On three qubits, the coefficients meeting R stay fixed (a=1/3), yet `ρ_r` goes from `[[45/49,6/49],[6/49,4/49]]` at b=1/2 to `[[9/10,0],[0,1/10]]` at b=0. The decoupled g cancels.
- **Cardinality weights.** `q_min^{1/4} ∈ (0.1395, 0.1396)` per site.
- **Star-count weight.** The unit cube has l∞ diameter 1 but needs 4 stars for a connected cover.
- **Ball radius.** At `|τ|=1/2000000` (an arithmetic fixture), w=64 fails the self-map while R is unchanged. So q=1/64 comes from the weight, not from R.
- **Another radius.** At `r=29/400`, `J_0G(r)/r ≤ 1.904e-4 < q_min`. Such a rate is admissible only with its radius named.

## 9. What I will require of each producer
**Both producers:**
1. **Declared objects.** State the metric (coarse l∞, `d_X=1`, verified by enumeration on Λ_2 and Λ_3), the weights and the loss per interaction exactly as in `parameters`, with the l1 table as a labelled alternative. Give the order-versus-distance tables for both conventions on Λ_2..Λ_4. Say whether the lemma is used in the contract form (⌈d/diam⌉) or the sharp form (1+⌈d/diam⌉), and use it consistently.
2. **Boundary sources**, derived by enumeration plus an all-size argument:
   - F1 nested: `8(3N²+3N+1)` stars;
   - F2 nested: `56(9N²+14N+6)` faces, face by face, with the double charge excluded;
   - F1 against F2: `28N(5N+1)` faces regrouped once, 17/13/5/10/3/1/0;
   - general volumes.

   Give the exact distances: N−1 from e_z and N from 0 to the new supports; the shell at N and N+1; the outer layer at N−1 and N. No off-by-one.
3. **Every constant labelled.** Each constant carries one tier and one route, both signs, and the ratio against its bracket, computed from the same exact formula. The headline must be `exact_first_order` with `T` from the self-consistent inequality in its own norm. The crude tier is reported and retained. Sharp or grouped refinements are labelled, and a sharp floor constant is not tested against the frozen floor bracket.
4. **Every comparison** (four items) at both frozen pairs. General volumes are either direct or through the union with the factor 2 shown.
5. **Wording.**
   - the template quoted once, as one unbroken span;
   - the 12 gate fields exactly as frozen;
   - "coefficient decay is not decay of the reduced density", with the marginal fixture;
   - "in each Q_L, uniformly in L", with no untruncated coefficients;
   - "rate in N per coarse step at fixed spacing", with no rate in a.
6. **Controls.** All 37 contract controls as damaging mutations, with explicit exceptions under -O. Byte-identical replays.

**Forward, in addition:**
- Lemma W itemized, with the disconnected-output case.
- The weighted self-map re-evaluated as exact rationals at w=64 and at w=390625/148.
- `T_w` from `w t_1/(1−J w G'(R))`.
- The difference-weight direction, with the source and Lipschitz ρ_B bounds.
- Never `2J_0G'(R)` as a decay factor.

**Reverse, in addition:**
- The disc contraction and analyticity, including the closed disc at τ_*.
- The order count stated as a Taylor-coefficient lemma, with the tree-chain proof.
- The Schwarz or Cauchy form named.
- The headline sup from the exact first-order tier on the disc; the crude `R` or `28ρG(R)` gives the crude tier only.
- General volumes by direct comparison. The union misses the headline target in the contract form.
- No analyticity statement for ρ_R.
- The inventory equal to the 27 contract-derived files. I hashed them: they are.

## 10. Predictions (the post-comparison flags any difference)
| quantity | prediction |
|---|---|
| `w_max`, `q_min`, `τ_*` | 390625/148, 148/390625, 1/37888 |
| `T_w(64) = T(64\|τ\|)` | 49/223580736 ≈ 2.19160e-7 |
| `T_w(w_max) = T(τ_*)` | 49/4036608 ≈ 1.21389e-5 |
| forward headline K (contract form) | ≈ 2.20045e-7. Admissible variants: G'(R) in the Lipschitz gives 2.2030e-7; G'(R) in the Lipschitz plus `T·G'(R)` for the remainder gives 19140625/86785322066496 ≈ 2.2055e-7. Labelled refinements: sharp 3.4382e-9; grouped √n_M first order ≈ 1.124e-7; per-comparison counts 45 (F2 nested) ≈ 2.0217e-7 and 38 (F1 against F2) ≈ 1.7090e-7 |
| reverse headline K | 49/111790368 ≈ 4.3832e-7 (Schwarz) or 14/31441041 ≈ 4.4528e-7 (Cauchy); refinements 6.849e-9 (sharp count), 2.262e-9 (cancellation) |
| forward floor K | ≈ 1.4693e-5 (exact) or ≈ 2.088e-2 / 37/1752 ≈ 2.112e-2 (crude) |
| reverse floor K | 49/2018304 ≈ 2.4278e-5 (exact), or 1/32 and 390625/12495264 (crude) |
| crude headline | ≈ 2.90e-4 (forward, or 2.897e-4 with an iterated t_w); 296/390625 (reverse); both fail and are retained |
| general volumes | forward 2K ≈ 4.4009e-7 (union); reverse direct 4.3832e-7; reverse through the union 8.766e-7 fails |
| τ ratios | headline 101.030 (forward) and 100.628 (reverse); floor exactly 1 (1.000375 coefficientwise); q_min exactly 100; sharp floor exactly 100 |
| distances and counts | as in §4 |

A forward headline K below 2.2004e-7 without a named refinement is an error. So is a reverse headline below 4.38e-7 that uses the contract-form count and a 2T sup. So is any K meeting 1/2000000 with a crude-tier label.

## 11. Producer-error checklist
1. **Metric.**
   - l1 and l∞ mixed;
   - `d_X` omitted;
   - star-count or cardinality weights relabelled as diameter weights;
   - loss charged per creation, or omitted in the contract-form source.
2. **Direction.** A weight growing from R, or a distance weight without diameter weights on the other creations.
3. **Distances.** The shell taken at N−1 without charging σ, or the outer layer taken at N.
4. **Sources.**
   - old terms charged, for example all 1960 F2 faces at N=2;
   - F2 regrouped anchors recharged (4536 in place of 3920 at N=2);
   - outgoing-only 7|τ|.
5. **Global Lipschitz.** 77/390625, or 37/6249384, used as a decay.
6. **Tiers.** A crude t with an exact label, or a route/tier outside the closed vocabulary.
7. **Brackets.** A sharp floor constant tested against [99/100,101/100] and "failing", or a bracket changed after evaluation.
8. **Reverse.**
   - a crude sup presented as the headline;
   - general volumes through the union claimed within 1/2000000;
   - a zero-free-region-free extension to ρ_R.
9. **Scope.**
   - cutoff removed for coefficients;
   - a rate in a or a length in fm;
   - state decay, whole-sequence convergence of states, uniqueness, or "the thermodynamic limit".
10. **Arithmetic.** Floats in admission, or exp/√ without directed enclosures.
