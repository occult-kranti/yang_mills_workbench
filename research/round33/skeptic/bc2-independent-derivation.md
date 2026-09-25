# BC2 independent derivation before producer comparison

**Standing.** I wrote this after the BC2 contract froze (`frozen_at` 2026-09-25T04:21:44Z, sha256 `28abe377…6b98a`) and before reading anything of the BC2 producer. BC2 is single+skeptic, so this replay is an admission input: my own code and derivation of every route-B constant from route-B inputs. I am a model-agent skeptic with correlated ancestry, not a human reviewer. Human project author: Hruday N M (BUNZEEY).

**Isolation, disclosed.**
- I did not open, list or read `research/round33/forward/bc2/` or `forward/bc1/`, except `find` on their `inputs/` (names only) and a sha256 comparison with the repository (42 and 40 files, all byte-identical, both equal to the contract-derived lists).
- Name-only exposures: `git status` printed the untracked `forward/bc2/check.py`, `forward/bc2/report.md`, `forward/bc1/check.py` and `forward/bc1/report.md`; I opened none. I also saw the subject of commit 1833023 (BD drafts) and the names and hashes of `contracts/bd1.json` and `bd2.json`, unread.
- After this package's values were final, a `git log` printed the subject of the BC1 forward commit 5816e0b (BC1 only; no BC2 producer content). Nothing was changed afterwards except this disclosure and the freeze hashes.
- **Proposal-blind in this session.** I did not read `experts/modern/bc2-targets-proposal.md`. In my pre-freeze review I did not read its §7 or its "Advisor only: previews" section, and I did not read `previews_recomputed` in its JSON. I read that review's JSON determinations and edit lists before computing, and its other markdown sections only after my values existed.
- **Prior exposure of the role.** My pre-freeze review (an earlier session of this role) read the proposal's §10 and recorded that "my later BC2 pre-comparison replay cannot claim ignorance of the proposal". This session did not see those previews. The code below is new, but the formula chain (the `T_B` formula; route A reproducing the BA1 and BB1 values) was already recorded in that review's determinations. Independence is limited to this derivation and this code.
- **Scratch.** Private folder `/tmp/claude-0/skeptic-bc-replay-private/`: a scratch script `routeb.py` for the route-B constants, run outputs and mutation copies. Not evidence, not a premise. No other agent's scratch was read.

**Sources.**
- The frozen contract, `advisor/selection-bc2.md` and `advisor/plan.json` (vocabulary, recorded).
- The premises:
  - AX1 gate, AX1 forward §§1–7, AX2 gate, and the AX2 calculator (executed, not edited);
  - the AV1, AV2, AM2, AQ1, AQ2 and AL1 gates;
  - the I1 class table;
  - the BA1 gate; the BB1 gate, the BB1 reverse report §§0–5 (the route this contract prescribes) and my BB1 review;
  - the BB2 gate;
  - the BA1/BA2/BB1/BB2 contracts, for the inherited control semantics.
- `bc2_check.py` reuses helpers of my own `bb1_check.py`/`bb2_check.py`. It imports nothing from any producer or tool.

**Exactness.** Every value is from `bc2_check.py`: 110 checks, 52 controls as 138 damaging mutations with 5 positives, byte-identical under `-B`, `-B -O` and plain `python3`. Decimals are previews.

## 1. Model and admitted route-B objects

**Model.** `AQ_uniform_routeB`: uniform Kogut–Susskind SU(2) at fixed spacing and strong bare coupling, labelled "(g^4=9.6x10^9)". Every face has `nu = alpha tau/24`, so the selected triple is `(tau/24, tau/24, tau/24)`. The coupling is `|tau| ≤ 10^-8` at both signs. `tau < 0` is the `U_E` mirror and has no real `g`. It is never weak coupling or continuum.

**Route B (AX1 gate).**
- The on-site part is the Haar reference `h_b = 8 sum_e C_e ≥ 6Q_b`, independent of `tau`.
- The interactions are whole stars `phi_b` (21 omitted faces, norm `7|tau|`) and single-factor groups `psi_b` (3 selected faces, support `{b}`, norm at most `|tau|`).
- `J' = 29|tau|` and `J_0' = 29/10^8`. The support is at most 4 and the termination order is 8.
- Every finite complete-factor route-B volume has a simple (nondegenerate) finite-volume ground and a gap of at least `1/2`.
- `T' = 13/3599632512`, and the state bound is `D'_ii`.

**Named construction.** FB: centered boxes `Lambda_N` (`N ≥ 2`), with stars inside the volume and every single group kept. The same prescription applies on general finite complete-factor volumes.

## 2. Item 1: incidence and admissibility

**Classes and grouping (enumerated).**
- The I1 table parsed from the report equals my class table: 24 classes per factor, 21 omitted and 3 selected. The selected classes are xy with `r = 0,1,2` and `s = 0`, owner set `{0}`.
- On a fine region of `12×6×3` sites (417 plaquettes), each plaquette goes to the group of its anchor `pi(base)`: the single group if it is selected, the star otherwise. Every interior group is complete (21 or 3 faces), and every face support lies in its group's support.

**Incidence on `R = {0, e_z}` (enumerated on `Lambda_3`).**
- 7 stars (anchors `R − S`) and 2 single groups meet `R`.
- 153 faces are charged, 88 meet `R`, 16 lie inside `R` (10 omitted with owner set `R`, 6 selected), and 72 straddle. Of those, 6 strictly contain `R`.
- Per site there are 52 first-order faces (`24 + 4 + 8 + 16`, i.e. 49 omitted plus 3 selected) and 5 groups (4 stars and 1 single). So `J' = 4·7 + 1 = 29` in units of `|tau|`.

**Support-one groups.** `{b}` meets a region only if it is contained in it, so single groups never straddle and are never clipped by a route-B volume containing `b`. The first-order R-marginal of a face term, `(tau/72)(|W_f Omega><Omega| + h.c.)`, vanishes after the partial trace unless the owner set lies in `R` (Haar mean zero on a spin-1/2 link outside `R`). So exactly the 16 faces inside `R` move `rho_R` at first order, and all 72 straddling faces have zero first-order R-marginal. **Selected-face site energy:** `8·4·(3/4) = 24` on one factor, so the first-order vector is kept in `Q_L` only for `L ≥ 24`.

**Admissibility (exact; `G(R) < 148/7`, `G'(R) < 352` from `e^{1/8} < 8/7`, checked against a 40-term bracket):**

| test | value | condition | outcome |
|---|---|---|---|
| disc `rho = 64|tau|`: self-map `29 rho G(R)` | `1073/2734375` ≈ 3.924e-4 | at most `R = 1/64` | pass |
| disc: contraction `29 rho G'(R)` | `2552/390625` ≈ 6.533e-3 | below 1 | pass |
| weight `W = 1024`: self-map `29 W|tau| G(R)` | `17168/2734375` ≈ 6.279e-3 | at most `1/64` | pass |
| weight: contraction `29 W|tau| G'(R)` | `40832/390625` ≈ 0.10453 | below 1 | pass |
| `lambda = 2/W` | `1/512` | below `q = 1/64` | pass |
| route-A disc `1/37888`: self-map / contraction | `29/1792` ≈ 0.01618 / `319/1184` ≈ 0.2694 | at most `1/64` / below 1 | **fails self-map**, passes contraction |
| route-A weight `1/(37888|tau|)`: self-map | `29/1792` | at most `1/64` | **fails** |
| largest route-B weight at the cap | `W ≤ 2734375/1073` ≈ 2548.35 | — | — |
| `W = 64` | `lambda = 1/32` | below `q` | fails (the lattice sum diverges) |

The route-A extremes sit exactly on route A's own boundary (`28 · (1/37888) · 148/7 = 1/64`). Under `J'` only the self-map rejects them.

## 3. Item 2: the route-B coefficient input (analytic disc, every site)

**Lemma D1 (complexified route-B map).** Decompose `V_1 = sum_X V_{X,1}` into route-B groups (stars and single groups). For complex `z` put `F_z(c) = sum_{k=0}^{8} L_k^{(z)}(c,…,c)/k!` with `L_k^{(z)} = z L_k^{(1)}`. AM2's multilinear estimate uses `|X| ≤ 4` only as an upper bound (AX1 F05), and uses the coupling only through `||V_X(z)|| = |z| ||V_{X,1}||`. So

`||L_k^{(z)}(c_1..c_k)||_a ≤ 29|z| · 16 · 8^k (1 + 5k/4) prod_j ||c_j||_a`,

with the per-site sum `29|z|` (four stars at `7|z|` and one single group at `|z|`) and termination above order 8 (at most `2|X|` creations; a single group terminates at order 2).

**Lemma D2 (disc).** For `|z| ≤ rho = 64|tau|`, `F_z` maps the anchored ball `||c||_a ≤ 1/64` into itself (`29 rho G(R) ≤ R`) and contracts it (`29 rho G'(R) < 1`), by §2. The iterates from 0 are polynomials in `z` that converge uniformly on the closed disc (Weierstrass). So `z ↦ c(z)` is holomorphic inside, continuous on the closed disc, and equal to the route-B AM2 fixed point at real `z = tau` (uniqueness in the ball).

**Lemma D3 (route-B circle bound).** `c(w) = w L_0 + r(w)`. The first order is `(L_0)_M = −(1/72) sum_{M_f = M} W_f Omega_0` over omitted and selected faces alike (energy 24, norm 1/2, distinct faces orthogonal). At most 52 faces pass through a factor, so `||w L_0||_a ≤ 52|w|/144`. The remainder satisfies `||r(w)||_a ≤ 29|w| G'(R) t`. Hence

`T_B(rho) = (52 rho/144)/(1 − 29·352 rho)`.

At `rho = |tau|` this is `13/3599632512`, **exactly the AX1 gate `T'`**. The program pins this value: every evaluation at `|tau|` re-checks it, so a source edit to 49 faces or `28|tau|` aborts.

**Lemma D4 (order versus distance on the route-B piece graph).** Pieces are faces, with support equal to their owner set: diameter at most 1, and 0 for selected faces. A nonzero order-`n` term on `M ∋ u` whose family contains a piece at l-infinity distance `d ≥ 1` from `u` has `n ≥ 1 + d`. A connected chain of pieces advances at most one coarse step per piece, and single-site pieces cost one order and advance zero. Checked by breadth-first search on the intersection graph of the 509 distinct pieces of `Lambda_2` (125 of them single sites) from five sites: the minimum slack is 0, so the bound is attained. The contract form uses the weaker `n ≥ d`.

**Lemma D5 (route-B every-site common core).** A source face is a face of a group (star or single) present in one volume only. For c1B, c4B and c5B (any two finite complete-factor route-B volumes containing `Lambda_N`), every site of every source face has `|p|_inf ≥ N`:
- a star `b+S` not inside the smaller volume has some coordinate with `b_i ≤ −N−1`, `b_i ≥ N+1`, or `b_i = N` with `b_i + 1 = N+1`, and all four sites then have `|p_i| ≥ N`;
- a single group `{b}` present in one volume only has `b ∉ Lambda_N`, so `|b|_inf ≥ N+1`.

Hence `d_inf(u, sources) ≥ N − |u|_inf` at every `u ∈ Lambda_N`. The enumeration covers c1B and c4B on `Lambda_2`, `Lambda_3` and two c5B cuboid pairs per `N`. The minimum source norm equals `N`, and the bound is attained at every site for the nested pairs.

**Theorem D6 (every-site coefficient differences).** For c1B, c4B and c5B, both signs, each `Q_L` uniformly in `L`, and every site `u` of the union volume:

`sum_{I ∋ u} ||c^A_I − c^B_I|| ≤ K_B q^((N−|u|_inf)_+)`, with `K_B = 2T_B(64|tau|) = 13/27941256` ≈ **4.65261834e-7** and `q = 1/64`.

*Proof.* Embed both fixed points in the union volume with vacuum padding. The difference is holomorphic on the disc, vanishes to order at least `N − |u|_inf` by D4–D5, and is bounded on the circle by `2T_B(rho)`, uniformly in `u`. Schwarz then gives the bound. Outside `Lambda_N` the anchored norm gives `2T_B(|tau|) ≤ K_B`. ∎

This is tier `exact_first_order`, route `analytic_disc`, target `1/1000000`, **margin ≈ 2.1493**. It is a coefficient statement per cutoff space; no untruncated coefficients are claimed. The crude tier `2·29·64|tau|·G(R)` ≈ 7.848e-4 fails and is retained. The same formulas with `(49, 28)` give `K = 49/111790368`, the BA1 gate value, which a route-B label rejects.

## 4. Item 3: marginal locality (iterated split, route-B inputs)

I follow the admitted BB1 reverse route and re-derive its closure. My code reproduces both BB1 gate `iterated_split` rationals exactly with route-A inputs, which anchors the implementation.

1. **Decomposition and orthogonality.** `rho_Y = N_c(omega_O)/Tr N_c(omega_O)` with `Tr N_c ≥ 1`. Every creation, single-site ones included, is excited at every site of its support (`c_I ∈ ⊗ Q_x H_x`). Fixture: `Tr N = 659/600` and `841/800` (both at least 1) on two mixed outside states, with the outside-state Lipschitz inequality checked by directed brackets.
2. **Single-support telescoping and the influence `kappa(J)`.** Consecutive collections of the majorant class differ on one support `J`. For `J` meeting `Y`, `kappa(J) ≤ 2` (the sine bound, `eta = 0`). For `J` missing `Y`, the split at `J` gives exactly a normalization channel (weight `2 m_J`) and a straddling channel. Only families covering the contracted region survive, so no factor `prod(1 + s_x)` ever appears.
3. **Per-site charging.** Take `lambda = 2/W = 1/512`, `h(x) = sum_{y∈Y} lambda^{d(x,y)}` and `H(I) = sum_{x∈I} h(x)`.
   - (P1) `sum_{I∋x, I meets Y} m_I ≤ t_W h(x)`.
   - (P2) `sum_{I∋x} m_I H(I) ≤ 8 t_W h(x)`, using `|I| ≤ (1+diam I)^3 ≤ 8·2^{diam I}`.
   - (P3) covering sums are at most `t_0`.

   Here `t_0 = 2T_B(|tau|) = 13/1799816256` and `t_W = 2T_B(1024|tau|) = 26/3148137` are the majorants of a comparison. The weighted loss is `W` per interaction, because `d_X ≤ 1` for stars and `d_X = 0` for single groups.
4. **Chain closure (re-derived).** With `R_r = (2 + 8r) t_W`, `mu = t_0 R_r/(1 − t_0)` and `alpha = (2 t_W + t_0 R_r/(1 − t_0))/(1 − 8 t_W)`, the three kinds of terms give coefficients of `H(S)` and `H(U)` that sum exactly to `alpha` and `mu`:
   - terms reaching `Y` cost `2 t_W H(S)`;
   - terminal terms cost `t_0 R_r (H(U) + H(S))`;
   - continuing terms cost `8 alpha t_W H(S) + mu t_0 (H(U) + H(S))`.

   I checked the algebra: `t_0 R_r + mu t_0 = t_0 R_r/(1 − t_0)`. The top level gives `kappa(J) ≤ (2 t_0 R_r + 2 alpha) H(J)`, so `r ≤ c_1 + c_2 r` with
   - `c_1 = 4 t_0 t_W + (4 t_W + 4 t_0 t_W/(1 − t_0))/(1 − 8 t_W)` ≈ 3.303759e-5;
   - `c_2 = 16 t_0 t_W + 16 t_0 t_W/((1 − t_0)(1 − 8 t_W))` ≈ 1.909e-12;
   - `beta* = c_1/(1 − c_2)` ≈ **3.30375944e-5**.

   The per-level factor is `8 t_W = 208/3148137` ≈ 6.607e-5.
5. **Lemma form (contract).** `eta = 0`, `kappa(I) ≤ beta* H(I) ≤ kappa_0 (w')^{−d_inf(I,Y)} p(|I|)`, with `kappa_0 = beta* |Y|`, `w' = 1/lambda = 512` and `p(n) = n`.
6. **Assembly (every comparison, both signs).**

   `||rho^A_Y − rho^B_Y||_1 ≤ 2 sum_{y∈Y} D_y + beta* sum_x h(x) D_x ≤ K_B (2 + beta* S_lambda) sum_{y∈Y} q^(N−|y|_inf)`.

   The lattice sum is `S_lambda = 1 + 24x(1+x)/(1−x)^3 + 2x/(1−x) = 2169/343` at `x = lambda/q = 1/8`. Hence:
   - **`c_site,B = K_B (2 + beta* S_lambda)` ≈ 9.30620868e-7** (target `1/500000`, **margin ≈ 2.1491**), in the frozen form `c_site,B |Y| e^{|Y|/10^8} q^{d_Y}` for every finite complete-factor region `Y ⊂ Lambda_N`;
   - **`C_B = c_site,B (1 + q)` ≈ 9.45161819e-7** (target `1/250000`, margin ≈ 4.2321), in the R form `C_B q^(N−1)`.

   The near term `2K_B` is `1 − 1.04e-4` of `c_site,B`. Tier `exact_first_order`, route `iterated_split`, direct comparisons c1B, c4B and c5B. The union-volume form `2C_B` is labelled only.
7. **Cutoff.** Every constant is independent of `L`, and selected-face vectors are kept for `L ≥ 24`. At fixed `N`, AV1 F20–F23 with the route-B gap `1/2` (AX1 gate item 2, valid on every route-B volume) give vector convergence. The `N` and `L` limits are never exchanged.
8. **Region-factor fixture.** `(1 + T')^2 − 1` ≈ 7.2230e-9 ≤ `10^-8`, while `(1 + 2T')^2 − 1` ≈ 1.4446e-8 is not (contract review R1). The split bound needs no such factor.
9. **Crude tier** (reported, never a target): `c_site,B` ≈ 1.847e-3 and `C_B` ≈ 1.876e-3. Both fail and are retained.

## 5. Item 4: whole sequence, exhaustion, mirror, identification, translations

- **T3 and T4 (every `N ≥ 2`; regions: every `N` with `Y ⊂ Lambda_N`).** Nested telescoping over all `M > N` (partial sums below the closed form) gives:
  - `C'_B = C_B/(1−q)` ≈ **9.60164388e-7** (margin 4.1660 against `1/250000`);
  - `c'_site,B = c_site,B/(1−q)` ≈ **9.45392628e-7** (margin 2.6444 against `1/400000`).

  The union assembly, meaning one direct c4B comparison, gives `C'_B = C_B` (margin 4.2321) and `c'_site,B = c_site,B` (margin 2.6864). The limit exists on every finite region by the Cauchy bound and trace-class completeness, without compactness.
- **2a, exhaustion within the prescription.** `||rho^{V_k}_Y − rho^inf_Y||_1 ≤ (c_site,B + c'_site,B)|Y| e^{|Y|/10^8} q^(N_k − max|y|_inf)`, from one direct c5B comparison of `V_k` with `Lambda_{N_k}` and item 1 with `M → ∞`. The constant is ≈ 1.87601e-6 nested (≈ 1.86124e-6 with the union assembly). This is not a comparison of boundary conditions.
- **2b, the pointwise sign mirror.** `E` meets every plaquette in 1 or 3 links (8 parity classes × 3 orientations, checked). AX1 F19–F20 and gate item (7) give `U_E H_N(tau) U_E^* = H_N(−tau)` in every centered box and cutoff, and the grounds are unique. So `rho^{−tau}_{N,Y} = U_{E,Y} rho^{tau}_{N,Y} U_{E,Y}^*`, where `U_{E,Y}` is the product over `E ∩ Y`, the same for every `N`. Whole-sequence convergence at both signs gives `omega^{−tau}_inf = omega^{tau}_inf ∘ alpha_E` on every finite region. It is a mirror replay, not a second coupling.
- **3, identification before inheritance.** Every AQ1-type subsequential state of the AX1 construction (untruncated, cutoff removed at fixed `N`) is a limit along a subsequence of a convergent sequence, so it equals `omega_inf` on every finite region. Only then is the AX1 gate's route-B list inherited. It is never the zero-selected AQ1/AQ2 list or the BB2 list.
- **4, coarse translations.** For every coarse `v` and `N ≥ |v|_inf + 2`, `Lambda_N + v` and `Lambda_N` are route-B volumes containing `Lambda_{N−|v|_inf}` (checked). One direct c5B comparison gives `||rho^{Lambda_N+v}_R − rho^{Lambda_N}_R||_1 ≤ C_B q^(N−|v|_inf−1)`, and the region form of c5B gives invariance of the limit on every finite region. **Non-coarse:** in a `4×4×4` fine window exactly 8 of 64 fine translations keep the factor partition (the coarse ones), while every fine translation keeps the uniform coefficient `tau/3`. So neither invariance nor non-invariance is claimed, and the route-A rejection reason is false here.

## 6. Item 5: the node restated for the route-B limit

- **Calculator replay.** The admitted calculator, executed from its pinned bytes at the fixed design (`tau = +10^-8`, `s = 1`, `D'` bound by the AX1 gate, `k' = 51|tau|/4`, `M_0 = 2`, `M_1 = 4s/pi`), returns exactly the AX2 gate values:
  - `d = 497870683678639429793424156500617766317/(4·10^40)`;
  - the outward radius `R' = 1912298807996871790146581299723633/10^40` ≈ 1.91229880800e-7.

  The interval `[99572606896681488461252714035083774357/(8·10^39), 497878332873871417280584742825816660849/(4·10^40)]` is exactly `[d − R', d + R']`. It reports `state_bound_D_prime = D'_ii` and `duhamel_slope_k_prime = 51/400000000`. At `-10^-8` it returns the same `d` and radius, flagged as the mirror replay. It refuses the zero triple, another window, the AV1 state tier and a changed fixed design.
- **Own labelled cross-check.** `r = 2(D' + D'^2) + 51|tau|/pi_lo + half-width`, with my own Machin `pi` from alternating partial sums and my own `e^{-3}` bracket, is ≈ 1.912298807997e-7. That is about `2.7e-41` below `R'`. It is labelled and not the headline.
- **Why it applies.** AX2 holds for every AQ1-type subsequential state of FB; by item 3 the route-B limit is one of them, and equals every one on every finite region. The region-form Cauchy bound at the proved constant carries the identification, so the node restatement needs no route-B dynamics, no rate in N and no uniqueness. `e^{-3}/4` lies inside the interval (`reference_unresolved`). No finite-box node convergence, no other node and no interaction shift is claimed.

## 7. Scaling `tau → tau/100` (same exact formulas)

| constant | ratio | bracket |
|---|---|---|
| `K_B` | `39059948/388073` ≈ 100.6510 | [95,105] ✓ |
| `C_B`, `c_site,B`, `C'_B`, `c'_site,B` (both assemblies) | ≈ 100.6615 | [95,105] ✓ |
| `q`, `rho/|tau|` | exactly 1 (frozen) | exactly 1 ✓ |
| node datum | exactly 1 | exactly 1 ✓ |
| node radius replay (recorded, not a target) | ≈ 100.0015 | [95,105] ✓ |

## 8. Exact finite fixtures (each `model_is_finite_graph: true`, `transfers_to_aq: false`)

The checker exhibits the following fixtures:
- **Coefficient decay is not marginal decay** (AV1 F13 type).
- **Second-order propagation.** Changing only `e` moves the off-diagonal R-marginal by exactly `−abe/Z`.
- **Straddling.** A creation inside `R` moves `rho_R` at first order; a straddling creation and a single-site creation outside `R` do not.
- **Normalization spectators and global fidelity.** `rho_R` is identical while the norm changes and the global infidelity grows.
- **Split trace and Lipschitz** on a mixed outside state; product charging against per-site charging.
- **Cutoff:** Eckart with gap `1/2`, and the limit-order double sequence.
- **Topology:** fixed versus moving vector.
- **Zero-free region.** `1 + 4z^2` vanishes at `z = i/2`.
- **Outside vector not a ground state.** Its number energy is `1/5`.
- **Support-one group.** A single-site creation inside `R` gives diagonal `1/50` at amplitude `1/7`; outside `R` it leaves `P_R`.
- **Whole sequence versus subsequence.**
- **Flip compression.** `D H(tau,tau) D = H(−tau,−tau)` with `D = diag(1,−1,−1)`, broken when the selected coefficient is not tied to `tau`.
- **Region factor** (§4).

## 9. Item 6: obligations (to be recorded)

- A route-B boundary-prescription comparison: an all-contained analogue with its own itemization. With one family there is no common limit.
- Route-B dynamics and correlation functions: a route-B BA2 with `||Phi'||_F ≤ 2349|tau|`.
- Uniqueness of any ground state.
- Anything uniform in the lattice spacing `a`.
- The continuum problem.

## 10. Predictions (the post-comparison flags any difference)

| quantity | prediction |
|---|---|
| `T_B(|tau|)` | `13/3599632512` (the AX1 `T'`) |
| `K_B` | `13/27941256` ≈ 4.65261834e-7; margin 2.1493 |
| `t_0`, `t_W`, `beta*` | `13/1799816256`, `26/3148137`, ≈ 3.30376e-5 (with the refinement `(49W+3)`: `t_W` ≈ 7.78e-6, labelled) |
| `c_site,B` | ≈ 9.30620868e-7; margin 2.1491 (binding, with T0) |
| `C_B` | ≈ 9.45161819e-7; margin 4.2321 |
| `C'_B` | nested ≈ 9.60164388e-7 (4.1660); union = `C_B` (4.2321) |
| `c'_site,B` | nested ≈ 9.45392628e-7 (2.6444); union = `c_site,B` (2.6864) |
| exhaustion constant | ≈ 1.87601e-6 (nested) or 1.86124e-6 (union) |
| crude tier | `K_B` ≈ 7.85e-4, `C_B` ≈ 1.88e-3; fail, retained |
| `tau/100` ratios | ≈ 100.651 (`K_B`), ≈ 100.662 (density constants) |
| node | `d` and `R'` equal to the AX2 gate rationals; own `r` about `2.7e-41` below `R'` |

A different split route or a different weight could legitimately give a slightly different far term; it is about `1e-4` of each constant.

**Flagged as errors:**
- a `K_B` below `4.6526e-7`, a `c_site,B` below the near term `2K_B` ≈ 9.30524e-7, or a `C_B` below `2K_B(1+q)` ≈ 9.45063e-7, labelled exact_first_order without a labelled refinement;
- any constant equal to its route-A counterpart (`4.3832e-7`, `8.7673e-7`, `8.9043e-7`, `4/984375`, `2/984375`).

## 11. What I will require of the producer

1. The route-B inputs stated before any constant (`J' = 29|tau|`, 52 faces, 5 groups, `T_B`, `rho = 64|tau|`, `W = 1024`, `lambda = 1/512`, the cardinality charge), and each weight checked under the route-B self-map and contraction. The route-A extremes rejected by the **self-map**.
2. The incidence enumerated, not asserted: 7 and 2 groups, 153/88/16/72, 52 and 5 per site, single groups of support one. The 16-face first-order marginal and the 72 zero straddling marginals shown.
3. The disc lemma proved in full: the complexified route-B map with `29|z|`, termination order 8, `T_B` pinned to `T'`, the piece graph with single sites, and the common core for c1B, c4B and c5B, at every site of the union volume. Never the BA1 or BB1 values or forms cited as admitted.
4. The split route proved in full with per-site charging and the normalization channel. `eta = 0` stated, and `kappa_0`, `w'` and `p` exact. Direct comparisons only. Both signs, each `Q_L`, and the untruncated vectors via AV1 F20–F23 with the route-B gap.
5. T3/T4 with the assembly in its field; 2a with its explicit bound; 2b with the AX1 F19–F20 premise; identification before inheritance; item 4 with one direct c5B comparison and no claim for non-coarse translations.
6. The calculator replayed from the declared premise at its fixed design, returning `d` and `R'` exactly, without writing a cache under `research/round32/`. An own re-evaluation only as a labelled cross-check.
7. The template once; the 18 gate fields exactly as frozen, with no `dynamics_level`; the `tau/100` ratios; all 52 controls as damaging mutations; byte-identical replays.

## 12. Producer-error checklist

1. **Silent route-A constants:** `28|tau|`, 49 faces, 4 groups, `9856 = 28·352`, `37888`, or the BA1/BB1/BB2 gate values under a route-B label.
2. **Selected faces mishandled:** dropped from the first order (49), counted at all four anchors (61), clipped, charged as straddling, or omitted from the piece graph.
3. **The 10-face route-A first-order marginal** used for route B.
4. **Admissibility tested by the contraction alone** (it accepts the route-A extremes).
5. **`polymer_kp`**, a union comparison or a telescoped coefficient input used as a target route.
6. **The global Lipschitz constant** (`J_0'G'(R) < 319/3125000`) or a density Lipschitz constant used as a decay factor.
7. **A common limit with another family**, or an identification with the zero-selected BB2 limit. A correlation-function rate in N or any route-B dynamics claim.
8. **The node:** a re-derived radius as the headline, the seven-star slope `49|tau|/4`, the zero-selected `D`, a node other than `s = 1`, or `-tau` presented as a second coupling.
9. **Wording:** a rate in N without its range, `O(1/N)`, or phrases on the forbidden list.
10. **Arithmetic:** floats in admission, or a bracket chosen after evaluation.

## 13. Replay

`python3 -B research/round33/skeptic/bc2_check.py --output <absolute fresh dir>`. The normal, `-O` and no-`-B` runs are byte-identical, and no `.pyc` is written anywhere, including `research/round32/forward/ax2/`. Eleven source-edit mutations of scratch copies all abort (contract review §5).
