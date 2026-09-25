# Hruday marginal locality — BB1 reverse (iterated product-ordering split with per-site charging)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted reverse production: the derivations, `check.py` and this report were written by Claude (an AI model) as the BB1 reverse producer, under reverse premise isolation (`reverse_premise_isolation: true`). It is correlated model-agent work. It is not human review and not formal verification. HNM labels are project aliases; the contribution alias of this packet is `HNM-BB1-R`.

**What this producer read.**
- **First**, the frozen contract snapshot `inputs/research/round33/contracts/bb1.json`. Its sha256 `30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018` was checked with `sha256sum` before reading, and `check.py` checks it again before any evaluation.
- **Then**, only files under `inputs/` (35 snapshots: `AGENTS.md`, the contract and its 33 shared premises):
  - *read in full:* `AGENTS.md`; `selection-bb1.md`; the BA1 gate; the BA1 reverse report; the BA1 skeptic review; the AV1 forward report; the AM2 forward report; the Round32 lessons reference; the paired-physics complete-residual reference;
  - *read in part:* the AV1 reverse report (Sections 1–8); the BA1 forward report (its weighted-norm definitions and Sections 1–3, plus the lines found by a keyword search for its boundary-weighted bound); the AY1 forward report (Section 3, the F2 itemization); the I1 forward report (Section 6 and the class table); the AM2, AQ1, AV1, AW1, AY1, AY2, BA1 and BA2 gates (verdict, and a keyword search of the `accepted` and `decision` fields for the tau cap and the cutoff statements);
  - *not opened beyond listing and hashing:* the AQ1, AQ2, AM2-reverse, AW1, AY1-reverse, AY2, BA2-forward and BA2-reverse reports, the AM2 and BA2 skeptic reviews and the four method `SKILL.md` files; their content enters only through the admitted gates and the Round32 lessons reference.
- **Outside `inputs/`, for conventions only** (no premise weight): `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py`, and the header, helpers, contract validation and result assembly of `research/round33/reverse/ba1/check.py` (BA1 is gated). Some helpers of `check.py` (exceptions, exact-arithmetic helpers, the I1 class derivation, the F1/F2 face enumerators) follow that file's conventions; every BB1 derivation, fixture and control is new code.
- **Not read:** nothing under `research/round33/forward/bb1/`, `research/round33/forward/bb2/`, `research/round33/reverse/bb2/`, `research/round33/experts/`; nothing under `research/round33/skeptic/` or `research/round33/advisor/` except the declared snapshots in `inputs/`. No deliberation, plan, panel, triage, lens memo or preview file was opened.

**Scratchpad disclosure.** My private scratch folder is `/tmp/claude-0/bb1-reverse-private/`. It holds prototypes of the identities, the constant evaluation, a stub report used to test `check.py`, and test runs. **None of it is evidence.** I created it with `mkdir -p` and did not list `/tmp/claude-0/` or the shared session scratchpad root, so I saw no other agent's folder names. **I opened no file in any other agent's scratch folder.**

**Attribution.** The commuting nilpotent creation expansion is the admitted AM2 construction (credited there to the Bravyi–DiVincenzo–Loss lineage, with Gauvin arXiv:2503.15539v3 A.6–A.8 as AM2's template). The product-ordering split and the normalization trap are the admitted AV1 lemma. The pure-state trace-distance identity, the contractivity of the partial trace, Banach's fixed-point theorem, Weierstrass' theorem and the maximum-modulus principle are standard. The route (iterated split with per-site charging) and the frozen targets were named by the advisor in the contract; they are shared premises. Independence is claimed only for the derivations, the constants and the code. Scientific priority is unverified.

## Verdict (reverse half)

Model: **`AQ_patterned_zero_selected`** — SU(2) in Kogut–Susskind form on `Z^3` at fixed spacing, coarse 24-link factors, selected triple exactly `(0,0,0)` with the Haar product reference, 21 omitted faces per anchor entering as `-(tau/3)W_f` in normalized units `delta=alpha/8`, both signs `|tau|<=10^-8`, the AM2 creation expansion (`J<=28|tau|`, `R=1/64`, `G(t)=16e^{8t}(1+10t)`). Families: **F1**, the AQ1 centered whole-star boxes `Lambda_N=[-N,N]^3`; **F2**, the I1 section-6 all-contained-face boxes with padding on the same `Lambda_N`; `N>=2`. Observable: the reduced densities `rho^{box}_Y` of the normalized finite-box ground vectors on finite complete-factor regions `Y`, in trace norm on `B(H_Y)`; in particular the cover `R={0,e_z}`.

**Main theorem (proved here, route `iterated_split`).** For every comparison of the contract, at both signs, in every on-site cutoff space `Q_L` with constants independent of `L`, and then at fixed `N` for the untruncated ground vectors:

`||rho^{box1}_Y - rho^{box2}_Y||_1 <= c_site * sum_{y in Y} q^(N-|y|_inf) <= c_site |Y| q^(d_Y)` with `d_Y = N - max_{y in Y}|y|_inf`; for `Y=R`: `||rho^{box1}_R - rho^{box2}_R||_1 <= C q^(N-1)`.

| pair | q | constant (exact) | preview | frozen target | margin | tier / route / BA1 input |
|---|---|---|---|---|---|---|
| headline (R form) | `1/64` | `C = 1649304957714574761387109521705122525/1852265838332370761358328329658687644475392` | `8.90425620114e-7` | `1/250000` | `4.492` | exact_first_order / iterated_split / gate bound value `K=49/111790368`, every-site form (b) |
| region form | `1/64` | `c_site = 25373922426378073252109377257001885/28941653723943293146223880150916994444928` | `8.76726764420e-7` | `1/500000` | `2.281` | exact_first_order / iterated_split / same input |
| secondary (labelled) | `151552\|tau\|` | `C_2 = 254713191786858884385903518855136871787/26288652445972361083565698627981857600000000` | `9.68909274868e-6` | `1/20000` | `5.160` | exact_first_order / iterated_split / BA1 reverse Theorem 4.1 re-instantiated at `rho=1/151552`, `K_2=49/10202112` (proved here, labelled) |
| secondary region (labelled) | `151552\|tau\|` | `c_site,2 = 651079047656055039494458366725211/67298950261689244373928188487633555456` | `9.67443095507e-6` | `1/40000` | `2.584` | as above |
| crude tier (headline pair) | `1/64` | `C_crude = 1298461471817127563970468301/721137361964077630855837662500` | `1.80057439858e-3` | reported, never a target | fails | crude_majorant / iterated_split / crude BA1 input `296/390625` |

- **Items 1, 3, 4, 5, 6: proved or executed** for the reverse route. Item 2 is the forward route (polymer_kp); this producer does not execute it, but exhibits its fixture (the polymer identity and the cardinality factor), as item 5 requires.
- **Every comparison, both signs:** F1 `Lambda_N` versus `Lambda_(N+1)`; F2 `Lambda_N` versus `Lambda_(N+1)`; F1 versus F2 on the same `Lambda_N` (the fixed-`N` boundary-prescription item); any two centered boxes of size at least `N`, compared directly; any two finite complete-factor volumes of one prescription containing `Lambda_N`, compared directly. The same constants hold for all of them (Theorem 5.1). A comparison through the union volume would cost a factor 2 (`2C`, about `1.78085124022e-6`); it is labelled only.
- **Coefficient input:** the BA1 coefficient differences at **every** site of the union volume, in form (b) of `parameters.coefficient_input`, proved in full in Section 2 (the BA1 gate admits the bound for `u` in `R` only).
- **Marginal-locality lemma** in the contract form: `eta=0`, `kappa(I) <= kappa_0 (w')^(-d_inf(I,Y)) |I|` with `kappa_0 = beta* |Y|`, `beta* = 8027378053355287230305861131/258892194754590065811608028259796` (about `3.10066437536e-5`), `w' = 512`, `p(n)=n` (Section 4.7).
- **Scaling** `tau -> tau/100`: `C` and `c_site` ratio about `1.00638216785e2` (bracket `[95,105]`); secondary `C_2` ratio about `1.00150034215e0` and `c_site,2` ratio about `1.00000000009e0` (bracket `[99/100,101/100]`); `q_2` ratio exactly 100.
- **Checker:** `check.py` runs **78 exact checks**; **37 of them are the contract controls**, rejecting **132 damaging mutations** in total. The `-B` and `-B -O` outputs are byte-identical.

**Proposed reverse verdict: `accepted_within_scope`**, sub-label `boundary_decay_rate_only`, secondary `static_not_dynamic`. Admission still needs the forward route, the exchange and the skeptical review. This is locality of the reduced densities of the named constructions at a rate in `N`; it is not uniqueness of any ground state, not whole-sequence convergence and not a common limit (both are BB2's subject), not a statement about other boundary conditions, and not a statement uniform in the lattice spacing `a`.

## 0. Frozen parameters, notation and the proof weights (declared before any constant)

| symbol | meaning | value |
|---|---|---|
| `tau` | coupling, both signs | `+-1/100000000` |
| `J` | per-site interaction sum (four anchor groups, incoming included; F2 by AY1 H4) | `28\|tau\|`, `J_0 = 7/25000000` |
| `R`, `G(R)`, `G'(R)` | AM2 ball radius and majorant (directed `e^{1/8}<8/7`) | `1/64`, `<148/7`, `<352` |
| `T(rho)` | exact_first_order circle bound `(49 rho/144)/(1-28 rho G'(R)) = (49 rho/144)/(1-9856 rho)` | `T(\|tau\|)=49/14398580736` |
| `t_i(rho)` | crude_majorant circle bound `28 rho G(R)` | `592\|tau\|` at `rho=\|tau\|` |
| `\|y\|_inf`, `d_inf` | coarse l-infinity norm and metric on factor sites (star diameter 1) | — |
| `W` | **split creation weight** (diameter weight `W^{diam I}`) | headline and region form: `W=1024`; secondary: `W_2 = 1/(37888\|tau\|)` (`390625/148` at the cap) |
| `lambda = 2/W` | per-step ratio of the site potential | `1/512`; secondary `75776\|tau\| = q_2/2` |
| `w' = 1/lambda` | lemma weight | `512`; secondary `1/(75776\|tau\|)` |
| cardinality charge | `\|I\| <= (diam I + 1)^3 <= 8 * 2^{diam I}` | per site, never a product |
| disc radius (BA1 input) | analytic disc of the every-site form (b) | headline `64\|tau\|`; secondary `\|tau\|/q_2 = 1/151552` |

**Admissibility of the weights.** The weighted self-map needs `28 W|tau| G(R) <= R`, i.e. `W <= 1/(37888|tau|)`; the weighted contraction needs `28 W|tau| G'(R) < 1`. At the cap, `W=1024` gives the self-map value `2368/390625 < 1/64` and the contraction constant `39424/390625` (about `0.1009`); `W_2 = 1/(37888|tau|)` gives the self-map value `1/64` with the rational `148/7` bound (strict with the actual `G(R)`) and contraction `77/296`. Both weights were fixed before any constant was computed; they do not depend on `N` or on the cutoff, and for `|tau| < 10^-8` the admissible range only widens. The rate `q=1/64` is the frozen one and is never optimized per `N`. The lattice sums below need `lambda < q`, i.e. `W > 128` at the headline and `W_2 > 2/q_2` for the secondary pair; a split weight `W=64` is rejected by `check.py` (`rate_constant_pair_prefrozen`).

**Majorant of a comparison.** For a comparison of two volumes `Lambda^A`, `Lambda^B` (both containing `Lambda_N`) embedded in `V = Lambda^A u Lambda^B` with vacuum padding, put `m_I = max(||c^A_I||, ||c^B_I||)`. Its per-site sums are `t_0 := max_u sum_{I ni u} m_I <= 2T(|tau|) = 49/7199290368` and `t_W := max_u sum_{I ni u} W^{diam I} m_I <= 2T(W|tau|)`, which is `49/6321618` (about `7.75118015672e-6`) at `W=1024` (Lemma W2).

## 1. Item 1 — the AV1-type decomposition, orthogonality and the two Lipschitz bounds

Fix a finite complete-factor volume `V`, a cutoff `Q_L`, and a collection `c=(c_I)` with `c_I` in `tensor_{x in I} Q_x H_x`: every creation is **excited at every site of its support**. Write `hat c_I = |c_I><Omega_I| (x) 1`. Creations commute and overlapping ones multiply to zero, so `psi(c) = prod_I (1 - hat c_I) Omega_0` has vacuum coefficient one.

For a region `Y` put `A_Y = {I : I meets Y}`, `B_Y = {I : I misses Y}`, the **straddle region** `O = union_{I in A_Y}(I \ Y)`, `E_c := prod_{I in A_Y}(1 - hat c_I)` (acting on `Y u O`), the outside vector `phi_out = prod_{I in B_Y}(1 - hat c_I) Omega_{Y^c}` and its normalized marginal `omega_O = Tr_{(Y u O)^c}|phi_out><phi_out| / ||phi_out||^2`.

**Lemma 1.1 (exact decomposition).** With the completely positive map `N_c(omega) := Tr_O [ E_c (P_Y (x) omega) E_c^* ]` on states of `H_O`,

\[
\rho_Y=\frac{N_c(\omega_O)}{\operatorname{Tr}N_c(\omega_O)} .
\tag{HNM-BB1-R01}
\]

*Proof.* Place the factors of `A_Y` last (AV1 F07): `psi = E_c(Omega_Y (x) phi_out)`, because every `hat c_I` with `I` in `B_Y` acts as the identity on `H_Y`. `E_c` acts only on `Y u O`, so `Tr_{Y^c}|psi><psi| = Tr_O[E_c(P_Y (x) Tr_{(YuO)^c}|phi_out><phi_out|)E_c^*] = ||phi_out||^2 N_c(omega_O)`, and `||psi||^2` is its trace. ∎

**Lemma 1.2 (orthogonality, `Tr N_c >= 1`).** For every state `omega` on `H_O`, pure or mixed, `Tr N_c(omega) = 1 + Tr[D (P_Y (x) omega) D^*] >= 1`, where `D = E_c - 1`.

*Proof.* Every term of `D` contains a creation meeting `Y`, and a product of creations is excited at every site of every member; hence `(P_Y (x) 1) D = 0`, and the cross terms `Tr[D(P_Y (x) omega)]` vanish (write `omega` as a mixture of pure states `phi_i`: `<Omega_Y (x) phi_i, D(Omega_Y (x) phi_i)> = 0`). ∎

`check.py` verifies `Tr N_c >= 1` exactly on two **mixed** outside states (values `271121/226800` and `36056951/28058400`), and it verifies that a "creation" with a vacuum component breaks the lemma (`||(1-|v><0|)|0>||^2 = 97/144 < 1` for `v=(1/4)|0>+(1/3)|1>`).

**Lemma 1.3 (Lipschitz in the coefficients; `eta = 0`).** Let `c, c'` differ only on one support `J`, and put `delta_J = c_J - c'_J`. Then, for **every** region `Y`, whether or not `J` meets `Y`,

\[
\|\rho_Y(c)-\rho_Y(c')\|_1\le 2\,\|\delta_J\| .
\tag{HNM-BB1-R02}
\]

For `c, c'` that differ only on supports meeting `Y` (so the outside state is common), telescoping gives `2 sum_{I in A_Y} ||c_I - c'_I||`; the same bound holds for `N_c(omega)/Tr N_c(omega)` at every fixed mixed `omega` (apply the proof to `E_c(Omega_Y (x) Phi)` with a purification `Phi` of `omega` on `H_O (x) H_aux`).

*Proof.* Split at `J` itself: `prod_{I meets J}(1 - hat c_I) = E''_J - hat c_J` with `E''_J = prod_{I meets J, I != J}(1-hat c_I)`, because `hat c_J hat c_I = 0` whenever `I` overlaps `J`. Hence `psi(c) - psi(c') = -hat delta_J psi_{notJ}`, where `psi_{notJ} = prod_{I misses J}(1 - hat c_I) Omega_0 = (P_J (x) 1) psi(c)` (orthogonality at `J`, as in Lemma 1.2), and `hat delta_J = hat delta_J (P_J (x) 1)`. So `||psi(c) - psi(c')|| <= ||delta_J|| ||psi(c)||`. For nonzero vectors `a, b`, `|| |a><a|/||a||^2 - |b><b|/||b||^2 ||_1 = 2 (1 - |<a,b>|^2/(||a||^2||b||^2))^{1/2} = 2 dist(b, C a)/||b|| <= 2||a-b||/max(||a||,||b||)`, and the partial trace is trace-norm contractive. ∎

The constant is structural (`eta = 0`) and the same in every tier; the bound is used only for supports meeting `Y`. Applied to a far support, (R02) has no decay, and it is **never** used as a per-shell decay factor. It is a statement about one support at a time; summed over all changed supports, far ones included, it would grow with the number of changed supports (the shell), just as a bound through the global overlap of the two box vectors collapses (Section 6).

**Lemma 1.4 (Lipschitz in the outside state).** For states `omega, omega'` on `H_O`,

\[
\|\rho(\omega)-\rho(\omega')\|_1\le\frac{2\|N_c(\omega-\omega')\|_1}{\operatorname{Tr}N_c(\omega)}\le 2\|N_c(\omega-\omega')\|_1\le 2\,(2\varepsilon_Y+\varepsilon_Y^2)\,\|\omega-\omega'\|_1,
\tag{HNM-BB1-R03}
\]

with `epsilon_Y = sum_F prod_{I in F}||c_I|| <= prod_{y in Y}(1 + s_y) - 1`, the sum running over nonempty families `F` of pairwise disjoint supports meeting `Y`, and `s_y = sum_{I ni y}||c_I||`.

*Proof.* For positive `A, B` with `Tr A >= 1`: `A/TrA - B/TrB = (A-B)/TrA + B (TrB - TrA)/(TrA TrB)`, so the trace norm is at most `2||A-B||_1/TrA`; use Lemma 1.2. For traceless `Delta`, `N_c(Delta) = Tr_O[D(P_Y (x) Delta)] + Tr_O[(P_Y (x) Delta)D^*] + Tr_O[D(P_Y (x) Delta)D^*]`, and `||D(P_Y (x) 1)|| <= epsilon_Y`. A family of disjoint supports each meeting `Y` injects into a choice of distinct sites of `Y` with one support through each, which gives the product bound. ∎

Constants (tier exact_first_order, route iterated_split): for `Y=R`, `epsilon_R <= 2T + T^2 = 1411060914529/207319127211110301696` with `T=T(|tau|)`, so the outside-state Lipschitz constant is `2(2 epsilon_R + epsilon_R^2)`, about `2.72e-8`; for a general `Y`, `epsilon_Y <= (1+T)^{|Y|} - 1`. The crude tier replaces `T` by `592|tau|`. `check.py` verifies (R03) exactly on the mixed-state fixture.

**Why (R03) is not simply iterated.** `omega_O - omega'_O` is a difference of marginals of the two outside vectors on the straddle region `O`, which can be as large as the box. Iterating (R03) on `O`, then on the straddle region of `O`, and so on, multiplies factors `2(2 epsilon_{O_k} + epsilon_{O_k}^2)` with `epsilon_{O_k}` of order `|O_k| t_0` and `|O_k|` growing with the depth `k`: the product of growing region sizes. With `|O_k| = (2k+1)^3` the per-level factor `|O_k| t_0` exceeds one at depth `k = 264`, so that iteration gives no decay for large `N`; `check.py` rejects this charging rule (`fixture_split_lipschitz_and_trace`). The recursion of Section 4 applies the same product-ordering split, but at the changed support and at covering regions, where the non-covering families cancel exactly, and it charges each level per site.

## 2. The every-site coefficient input — form (b) of `parameters.coefficient_input`, proved in full

The BA1 gate admits the coefficient bound for `u` in `R` only. BB1 needs it at **every** site of the union volume. This section restates the BA1 reverse Theorem 4.1 for every `u` and proves it here; nothing in it is cited as an admitted BA1 statement except the AM2 majorant, the AV1 first-order coefficient and the I1/AY1 dictionaries, which are admitted premises of BA1 as well.

**2.1 The complexified map.** Fix a finite complete-factor volume `Lambda` of prescription F1 (whole stars `b+S` inside `Lambda`) or F2 (for each anchor, the faces whose owner set lies in `Lambda`, grouped into the clipped group `X_b` inside `(b+S) cap Lambda`), a cutoff `Q_L`, and `V_1 = sum_X V_{X,1}` with `V_{X,1} = -(1/3) sum W_f` over the faces of the group, so `||V_{X,1}|| <= 7`. For complex `z` put `V(z) = z V_1` and

`F_z(c) = sum_{k=0}^{8} L^{(z)}_k(c,...,c)/k!`, `L^{(z)}_k(c_1..c_k)_M = H_M^{-1} P_M ad_{C_1}...ad_{C_k}(V(z)) Omega_0 = z L^{(1)}_k(c_1..c_k)_M`.

At real `z=tau` this is the AM2 map. The steps of the AM2 multilinear estimate (HNM-AM2.5) are: (a) creations commute, overlapping ones multiply to zero; (b) every creation support in a nonzero word meets `X`; (c) `N\X ⊂ M ⊂ N u X`, at most `2^p=16` outputs, `|I_j| <= |M|+p`; (d) `2^k` products; (e) each projected product has norm at most `||V_X(z)|| prod_j ||c_{j,I_j}||`; (f) `||H_M^{-1}|| <= 1/|M|` from `h_x >= Q_x`; (g) `sum_{X ni u} ||V_X(z)|| <= 28|z|` (four anchor groups per site, incoming ones included; for F2 each group has at most 21 faces of norm `|z|/3` and `u in X_b` forces `b in u-S`, AY1 H4); (h) `sum_{I meets X} ||c_I|| <= p ||c||_a`; (i) `1/|M| <= (p+1)/|I_l|` and `sum_{X meets I_l} ||V_X(z)|| <= 28|z| |I_l|`; (j) termination above order `2p = 8`. Only (e), (g), (i) involve `z`, and only through `||V_X(z)|| = |z| ||V_{X,1}||`; no step uses self-adjointness or reality of the coupling. Hence, for every complex `z` and every volume of either prescription,

\[
\|L^{(z)}_k(c_1,\ldots,c_k)\|_a\le 28|z|\,16\,8^k\bigl(1+\tfrac{5k}{4}\bigr)\prod_j\|c_j\|_a .
\tag{HNM-BB1-R04}
\]

**Lemma B1 (disc contraction).** For `0 < rho <= tau_star = 1/37888` and `|z| <= rho`, `F_z` maps the ball `||c||_a <= R` into itself (`28 rho G(R) <= R`, using `G(R) < 148/7`) and is a contraction with constant `28 rho G'(R) < 1` (`G'(R) < 352`). *Proof:* sum (R04) against `G(t) = sum_k 16 8^k (1+5k/4) t^k/k!` and telescope each `k`-linear term. ∎

**Lemma B2 (analyticity of the coefficients).** For such `rho`, every volume of F1 or F2 and every `L`, `F_z` has one fixed point `c(z)` in the ball; `z -> c(z)` is continuous on `|z| <= rho` and holomorphic on `|z| < rho`, and at real `z = tau` it is the AM2 fixed point. *Proof:* the iterates `c^{(m+1)}(z) = F_z(c^{(m)}(z))` from `c^{(0)}=0` are polynomials in `z`, stay in the ball, and converge uniformly on the closed disc at the geometric rate of Lemma B1 (Weierstrass, coordinatewise in the finite-dimensional coefficient space of `Q_L`); the limit is a fixed point by continuity, the only one in the ball by the contraction, and at real `tau` it coincides with the AM2 fixed point by AM2's uniqueness. ∎

**Lemma B3 (circle bound, two tiers).** For `|w| <= rho`, `t(w) := ||c(w)||_a` satisfies
- crude_majorant: `t(w) <= 28|w| G(R) <= t_i(rho) = 28 rho G(R)`;
- exact_first_order: `c(w) = w L^{(1)}_0 + r(w)`, where `(L^{(1)}_0)_M = -(1/72) sum_{M_f = M} W_f Omega_0` is the exact AV1 first-order coefficient at unit coupling (face energy 24, face-vector norm `1/2`, distinct faces orthogonal); at most 49 omitted faces pass through a factor (I1 table, translation covariance; enumerated in `check.py`), so `||w L^{(1)}_0||_a <= 49|w|/144`; by the AM2 remainder inequality and the convexity of `G`, `||r(w)||_a <= 28|w|(G(t)-16) <= 28|w| G'(R) t`. Hence `t(w) <= T(rho) = (49 rho/144)/(1 - 28 rho G'(R))`. ∎

**Lemma B4 (connected families; order versus distance at a site `u`).** Decompose `V_1` into faces. Then `c(z) = sum_{n>=1} z^n c_n` with `c_n = sum_{(Y_1..Y_n)} Phi_n(Y_1..Y_n)`, `Phi_n` multilinear in the pieces; `Phi_n(...)_M = 0` unless the family `{Y_1..Y_n}` is connected in its intersection graph and `M ⊂ Y_1 u ... u Y_n`. If `M` contains `u` and the family contains a piece `Y` with `d := d_inf(u, Y) >= 1`, then `n >= 1 + d` (pieces have l-infinity diameter at most 1).

*Proof.* The Taylor recursion is `c_1 = L^{(1)}_0`, `c_n = sum_{k>=1} (1/k!) sum_{n_1+..+n_k = n-1} L^{(1)}_k(c_{n_1},..,c_{n_k})`. By induction on `n`: for `n=1`, `H_M^{-1} P_M V_Y Omega_0` vanishes unless `M ⊂ Y`; for `n >= 2`, a term has one piece `Y` in its `V`-slot and creations `c_{n_j, I_j}`, each `I_j` meets `Y` (step (b)) and `M ⊂ Y u (u_j I_j)` (step (c)); by induction each `c_{n_j, I_j}` comes from a connected family `F_j` whose union contains `I_j`, and a point of `I_j cap Y` joins `F_j` to `Y`. For the count: a point of `M` equal to `u` lies in some piece `Z_0`; a chain `Z_0, Z_1, .., Z_m = Y` of distinct intersecting pieces has consecutive intersection points `q_i`, so `d <= d_inf(u, q_m) <= m`, and the family has at least `m + 1 >= d + 1` pieces. ∎ The contract form uses the weaker `n >= d`. `check.py` verifies `n >= 1 + d` by breadth-first search on the enumerated star-intersection graph of `Lambda_3` at five sites `u` (minimum slack 0, so the count is attained).

**Lemma B5 (every-site common core).** Let `N >= 1` and `u` in `Lambda_N`. Every omitted face with a site at l-infinity distance at most `N - |u|_inf - 1` from `u` belongs to a star `b+S ⊂ Lambda_N`; hence it is retained by F1 and by F2 on every finite complete-factor volume containing `Lambda_N`, and every source term of every comparison (a face present in one volume only) lies at distance at least `N - |u|_inf` from `u`.

*Proof.* A site `q` with `d_inf(q, u) <= N - |u|_inf - 1` has `|q|_inf <= N - 1`. Its anchor is `b = q - s` with `s` in `S = {0, e_x, e_y, e_z}`, so each `b_i` lies in `[-N, N-1]` and `b + S ⊂ Lambda_N`. F1 on a volume containing `Lambda_N` retains the whole star; F2 retains every face whose owner set lies in the volume, and the owner set lies in `b+S ⊂ Lambda_N`. ∎ For `u` in `R` this is BA1's Lemma 3.1. `check.py` enumerates it for `N = 2, 3, 4` at every `u` of `Lambda_N`, for the three named comparisons (F1 `Lambda_N` vs `Lambda_(N+1)`, F2 `Lambda_N` vs `Lambda_(N+1)`, F1 vs F2 on `Lambda_N`, the latter with the `28N(5N+1)` = 616/1344/2352 extra faces) and for four general-volume examples (F1 `Lambda_2` vs F2 `Lambda_4`; F2 `Lambda_3` vs F1 `Lambda_4`; F1 on `[-2,3]x[-2,2]x[-2,4]` vs F1 `Lambda_3`; F2 on `[-3,2]x[-2,3]x[-2,2]` vs F2 `Lambda_2`). The distance `N - |u|_inf` is attained at every site for the nested comparisons (125, 343, 729 sites at `N = 2, 3, 4`).

**Theorem B6 (every-site coefficient differences, form (b)).** Let `N >= 2`, let `Lambda^A`, `Lambda^B` be finite complete-factor volumes of prescriptions in `{F1, F2}` both containing `Lambda_N`, `V = Lambda^A u Lambda^B`, `L` any cutoff, `0 < |tau| < rho <= tau_star`. Then for **every** site `u` of `V`,

\[
D_u:=\sum_{I\ni u}\|c^A_I(\tau)-c^B_I(\tau)\|\;\le\;2T(\rho)\Bigl(\frac{|\tau|}{\rho}\Bigr)^{N-|u|_\infty}\quad(u\in\Lambda_N),\qquad D_u\le 2T(|\tau|)\le\frac{2T(\rho)\,\rho}{|\tau|}\le 2T(\rho)\Bigl(\frac{|\tau|}{\rho}\Bigr)^{N-|u|_\infty}\quad(u\notin\Lambda_N).
\tag{HNM-BB1-R05}
\]

*Proof.* (i) Embed both fixed points in `V` with unperturbed padding; the map with interaction supported in `Lambda^A` preserves collections supported in `Lambda^A`, so the embedded fixed point is box A's (the same for B). (ii) `g(z) = (c^A_I(z) - c^B_I(z))_{I ni u}` is holomorphic on the open disc and continuous on the closed one (Lemma B2), in the finite-dimensional norm `||g||_u = sum_{I ni u} ||g_I||`. Terms of `c_n` whose faces are all common to both volumes coincide; every other term contains a source face, at distance at least `N - |u|_inf` from `u` (Lemma B5), so by Lemma B4 `g_n = 0` for `n <= N - |u|_inf` when `|u|_inf <= N-1`, and the vanishing order is `n_0 >= N - |u|_inf + 1 >= N - |u|_inf`; for `|u|_inf = N` the exponent is 0. (iii) Schwarz: `h(z) = g(z)/z^{n_0}` is holomorphic; for a functional `l` of dual norm at most one and `r < rho`, the maximum principle gives `|l(h(z))| <= r^{-n_0} max_{|w|=r}||g(w)||_u`; let `r -> rho`. (iv) On the circle `||g(w)||_u <= t^A(w) + t^B(w) <= 2T(rho)` (Lemma B3; the anchored norm is a maximum over sites, so this is uniform in `u`). (v) Outside `Lambda_N`, `|u|_inf >= N+1`; at the real point `D_u <= ||c^A||_a + ||c^B||_a <= 2T(|tau|)`, and `T(rho)/rho` is increasing, so `2T(|tau|) <= 2T(rho)|tau|/rho <= 2T(rho)(rho/|tau|)^{|u|_inf - N}`. ∎

**The instances used.**

| pair | disc radius `rho` | rate `q = \|tau\|/rho` | `K = 2T(rho)` exact | preview | crude `2 t_i(rho)` |
|---|---|---|---|---|---|
| headline and region form | `64\|tau\|` | `1/64` | `49/111790368` (the BA1 gate bound value) | `4.38320410574e-7` | `296/390625` |
| secondary (labelled) | `1/151552 = tau_star/4` | `151552\|tau\|` | `49/10202112` | `4.80292708019e-6` | `1/128` |

The headline input is the BA1 gate's bound value `K = 49/111790368`, now valid at every site of `V` in the form `D_u <= K q^(N-|u|_inf)`. The secondary input re-instantiates the same theorem at `rho = |tau|/q_2 = 1/151552`, computed exactly here and labelled (the BA1 gate binds only `64|tau|` and `tau_star`). Tier of both inputs: exact_first_order; route of the input: analytic_disc, recorded as the input and never as the BB1 route. All constants are uniform in `L` (compression neither enlarges supports nor increases `J`; the first-order face vectors are kept exactly for `L >= 24` and only removed for smaller `L`).

## 3. The diameter-weighted norm of the split (proved here)

For `W >= 1` put `||c||_W = max_u sum_{I ni u} W^{diam I} ||c_I||` (coarse l-infinity diameters).

**Lemma W1 (weighted multilinear estimate).** For one volume of F1 or F2, `||L_k(c_1..c_k)||_W <= W J 16 8^k (1 + 5k/4) prod_j ||c_j||_W`.

*Proof.* In a nonzero word with interaction `V_X` and creation supports `I_j` (each meeting `X`), every point of `M` lies in `X` or in some `I_j`; routing two points of `M` through points of `I_a cap X` and `I_b cap X` gives `diam M <= d_X + sum_j diam I_j` (the maximum rule fails: `X={0,e_x}`, `I_1={-e_x,0}`, `I_2={e_x,2e_x}`, `M={-e_x,2e_x}` has `diam M = 3 = 1+1+1`, verified in `check.py`). With `d_X <= 1` this gives `W^{diam M} <= W prod_j W^{diam I_j}`: the loss `W` is charged once per interaction term, never per creation. The counting of HNM-AM2.5 is unchanged: root in `X` contributes `2^p (2p)^k W J`, root in a creation contributes `2^p (2p)^k k (p+1)/p W J`, with `p = 4`; the sum is `W J 16 8^k (1+5k/4)`, and `check.py` verifies the two contributions add to `16 8^k (1+5k/4)` for `k = 0..8`. ∎

**Lemma W2 (weighted fixed point).** For `1 <= W <= 1/(37888|tau|)` the AM2 map sends the weighted ball `||c||_W <= R` into itself (`28 W|tau| G(R) <= R`) and contracts it (`28 W|tau| G'(R) < 1`); its fixed point is the AM2 fixed point (the weighted ball lies in the anchored ball) and satisfies `||c||_W <= T(W|tau|)` (exact_first_order: every owner set has diameter 1, so `||c^{(1)}||_W <= 49 W|tau|/144`, and the remainder is at most `28 W|tau| G'(R) ||c||_W`) and `||c||_W <= 28 W|tau| G(R)` (crude_majorant). ∎

At `W = 1024` this is `T(1024|tau|) = 49/12643236` per box, so `t_W <= 49/6321618` for the majorant of a comparison. At `W_2 = 1/(37888|tau|)` it is `T(tau_star) = 49/4036608` per box, `t_W <= 49/2018304`.

**Lemma W3 (mixed weight; proved for completeness, not used by this route).** For `w >= 1`, `b >= 0`: `w^{diam M} e^{b|M|} <= (w e^{4b}) prod_j w^{diam I_j} e^{b|I_j|}`, because `|M| <= |X| + sum_j |I_j| <= 4 + sum_j |I_j|`; with the same counting this gives the mixed-weight contraction with loss `w e^{4b}` per interaction. The loss `w e^{b}` is insufficient: for the four-site `X` with `I_1 = {3,4}`, `I_2 = {0,5}`, `|M| - sum |I_j| = 2 > 1` (`check.py`). The reverse route uses only the diameter weight, and charges support sizes through `|I| <= 8 * 2^{diam I}` (Section 4.5).

## 4. Item 3 — the iterated split with per-site charging

### 4.1 Telescoping over supports and the single-support influence

Fix a comparison: collections `c^A`, `c^B` on the union volume `V`, both AM2 fixed points (Theorem B6 (i)), and the majorant `m_I = max(||c^A_I||, ||c^B_I||)`. Let `C(m)` be the class of collections `c` with `||c_I|| <= m_I` for every `I` (vectors in the same coefficient spaces); `psi(c)` is never zero. Order the supports of `V` as `I_1, ..., I_K` and put `c^{(k)}` = `c^B` on the first `k` supports and `c^A` on the others. Every `c^{(k)}` lies in `C(m)`, consecutive ones differ on one support, and

\[
\|\rho_Y(c^A)-\rho_Y(c^B)\|_1\le\sum_{k}\kappa(I_k)\,\|c^A_{I_k}-c^B_{I_k}\|,\qquad
\kappa(J):=\sup\Bigl\{\tfrac{\|\rho_Y(c)-\rho_Y(c')\|_1}{\|c_J-c'_J\|}\Bigr\},
\tag{HNM-BB1-R06}
\]

the supremum over pairs in `C(m)` that differ only on `J`. By Lemma 1.3, `kappa(J) <= 2` for every `J`; this is the bound used for supports meeting `Y`. The remainder of this section bounds `kappa(J)` for `J` missing `Y` with decay in the distance and per-site charging.

### 4.2 The split at the changed support

Let `J` miss `Y`, `c, c'` in `C(m)` differ only on `J`, `delta = c_J - c'_J`. Apply the AV1 product-ordering split at the region `J`: with `phi := prod_{I misses J}(1-hat c_I) Omega_{J^c}` (common to `c` and `c'`), `n^2 = ||phi||^2`, `psi_J = Omega_J (x) phi`, `E''_J = prod_{I meets J, I != J}(1 - hat c_I)` and `D'' = E''_J - 1`,

`psi(c) = psi_J + chi(c)`, `chi(c) = D'' psi_J - c_J (x) phi`, `(P_J (x) 1) chi = 0`.

Because `J ⊂ Y^c` is traced out and `chi` is excited somewhere on `J`, `Tr_{Y^c}|psi_J><chi| = Tr_{Y^c}[|psi_J><chi|(P_J (x) 1)] = 0`: the cross terms vanish exactly. Expanding `|chi><chi|`,

`M(c_J) := Tr_{Y^c}|psi(c)><psi(c)| = (1 + ||c_J||^2) n^2 rho_Y(phi) + Tr_{Y^c}|D''psi_J><D''psi_J| - Gamma(c_J) - Gamma(c_J)^*`,

with `rho_Y(phi) = Tr_{(J u Y)^c}|phi><phi|/n^2` and the linear map `Gamma(v) := Tr_{J^c \ Y} |phi><(<v| (x) 1) D'' psi_J|`. With `a = ||c_J||^2 - ||c'_J||^2` and `Z = ||psi(c)||^2 = Tr M(c_J) >= n^2` (orthogonality at `J`, Lemma 1.2), the identity `M/TrM - M'/TrM' = (M-M')/TrM - rho'(TrM - TrM')/TrM` gives, **exactly**,

\[
\rho_Y(c)-\rho_Y(c')=\frac{a\,n^2\bigl(\rho_Y(\phi)-\rho_Y(c')\bigr)-\bigl(\Gamma(\delta)-\operatorname{Tr}\Gamma(\delta)\,\rho_Y(c')\bigr)-\bigl(\Gamma(\delta)-\operatorname{Tr}\Gamma(\delta)\,\rho_Y(c')\bigr)^*}{Z},
\tag{HNM-BB1-R07}
\]

\[
\|\rho_Y(c)-\rho_Y(c')\|_1\le 2m_J\|\delta\|\,\|\rho_Y(\phi)-\rho_Y(c')\|_1+\frac{2}{n^2}\bigl\|\Gamma(\delta)-\operatorname{Tr}\Gamma(\delta)\,\rho_Y(c')\bigr\|_1,
\tag{HNM-BB1-R08}
\]

using `|a| <= ||delta|| (||c_J|| + ||c'_J||) <= 2 m_J ||delta||`. The first term is the **normalization** channel (it carries the `||c_J||^2` weight of the `J`-excited component); `rho_Y(phi)` is `rho_Y(c')` with all supports meeting `J` removed. The second is the **straddling** channel. `check.py` verifies (R07) as an exact rational identity on a five-site fixture with two excited levels per site and 14 supports (`fixture_split_route_identities`).

### 4.3 Multi-support families: only coverings survive

`D'' psi_J = sum_F (-1)^{|F|} K_F psi_J` over nonempty families `F` of pairwise disjoint supports `I != J` meeting `J`, with `K_F psi_J = c_F (x) Omega_{J \ uF} (x) phi_{J u S_F}`, `S_F = (u F) \ J`, and `phi_U := (<Omega_U| (x) 1) phi` (the vector with all supports meeting `U` removed). Since `delta` is excited at **every** site of `J`, the contraction `(<delta| (x) 1)` kills every family that does not cover `J`. Hence

\[
\Gamma(\delta)=\sum_{F\ \text{covers}\ J}(-1)^{|F|}\,\operatorname{Tr}_{J^c\setminus Y}\bigl|\phi\bigr\rangle\bigl\langle g_F\otimes\phi_{J\cup S_F}\bigr|,\qquad g_F=(\langle\delta|\otimes1)c_F,\quad \|g_F\|\le\|\delta\|\prod_{I\in F}m_I .
\tag{HNM-BB1-R09}
\]

This is the explicit bound on multi-support straddling families: a family contributes only if it covers the region it is contracted against, and then with the **product** of its members' amplitudes; the spectator families (those not covering) cancel exactly, so no factor `prod_x (1 + s_x)` over a region ever appears.

### 4.4 The recursion on covering regions (the split applied to the outside state)

For a removed set `U` missing `Y`, a nonempty region `S ⊂ U^c` and a vector `g` excited at every site of `S`, define the record `Gamma[U,S,g] := Tr_{U^c \ Y} |phi_U><g (x) phi_{U u S}|`. If `S` misses `Y`, trace `S` first and split the outside vector `phi_U` at `S` (creations meeting `S` act last): `phi_U = E^U_S(Omega_S (x) phi_{U u S})`. The contraction with `g` again keeps only the coverings `F` of `S` by supports meeting `S` and missing `U`:

\[
\Gamma[U,S,g]=\sum_{\substack{F\ \text{covers}\ S\\ S'_F\neq\varnothing}}(-1)^{|F|}\,\Gamma[U\cup S,S'_F,g'_F]^{*}+\sum_{\substack{F\ \text{covers}\ S\\ S'_F=\varnothing}}(-1)^{|F|}\,g'_F\,\|\phi_{U\cup S}\|^2\rho_Y(\phi_{U\cup S}),
\tag{HNM-BB1-R10}
\]

with `S'_F = (u F) \ S` and `g'_F = (<g| (x) 1) c_F`, `||g'_F|| <= ||g|| prod_{I in F} m_I`. The top level is (R09): `Gamma(delta)` is the sum of the records `Gamma[J, S_F, g_F]` (and of scalar terms when `S_F` is empty). `check.py` verifies (R10) as an exact identity, unrolled to termination, for three records on the fixture of Section 4.2 (`covering_recursion_exact`).

Let `rho_* = rho_Y(c')` and `Def[U,S,g] := ||Gamma[U,S,g] - Tr Gamma[U,S,g] rho_*||_1`. Adjoints and traces commute with the sums, and `rho_*` is self-adjoint, so (R10) gives

- `Def[U,S,g] <= sum_{F: S'_F != 0, S'_F misses Y} Def[U u S, S'_F, g'_F] + sum_{F: S'_F meets Y} 2 ||g'_F|| n^2 + sum_{F: S'_F = 0} ||g'_F|| n^2 Rem(U u S)`,

where the middle terms use `||Tr_{..}|a><b| ||_1 <= ||a|| ||b||` and `||phi_U|| <= n` (vacuum projections decrease the norm), and `Rem(U) := ||rho_Y(phi_U) - rho_*||_1`. The removed set grows strictly at each level, so the recursion terminates in every finite volume; its depth is not bounded uniformly, and nothing below depends on it. Removing the supports meeting `U` one at a time (each step a single-support change inside `C(m)`, with `||delta|| = ||c'_I|| <= m_I`) gives

`Rem(U) <= sum_{I meets U} kappa(I) m_I`.

### 4.5 Per-site charging

Put `lambda = 2/W`, the site potential `h(x) = sum_{y in Y} lambda^{d_inf(x,y)}` and `H(I) = sum_{x in I} h(x)`. Three per-site facts carry the whole estimate:

- **(P1)** `sum_{I ni x, I meets Y} m_I <= t_W h(x)`. A support through `x` meeting `Y` has `diam I >= d_inf(x, Y)`, so the sum is at most `W^{-d_inf(x,Y)} t_W <= lambda^{d_inf(x,Y)} t_W <= h(x) t_W`.
- **(P2)** `sum_{I ni x} m_I H(I) <= 8 t_W h(x)`. For `x'` in `I ni x`, `d_inf(x', y) >= d_inf(x, y) - diam I`, so `H(I) <= |I| lambda^{-diam I} h(x)`, and `|I| lambda^{-diam I} <= 8 (2/lambda)^{diam I} = 8 W^{diam I}` by the cardinality charge `|I| <= (diam I+1)^3 <= 8*2^{diam I}` (checked for every diameter by induction, `((d+2)/(d+1))^3 <= 2` for `d >= 3`). The size of a support is charged once, at the site where the chain enters it: never as a product of growing region sizes.
- **(P3) coverings.** For a nonempty region `T`, `Cov(T) := sum_{F covers T} prod_{I in F} m_I <= t_0` (and `Cov(empty) = 1`): the member through the first site `x_0` of `T` is unique, and the other members cover `T` minus it, so `Cov(T) <= s_{x_0} max Cov(smaller) <= t_0` by induction. Consequently `sum_{F covers S, F ni I} prod m <= m_I`.

With the ansatz below, `Rem(U) <= R_r H(U)` with `R_r = (2 + 8r) t_W`, by (P1) and (P2).

### 4.6 The chain bound and the closure

Let `r := max_{I misses Y} kappa(I)/H(I)` (finite: finitely many supports, `h > 0`). Then `kappa(I) <= 2*1[I meets Y] + r H(I)` for every `I`. Let `Ch(U,S)` be the unrolled bound of `Def[U,S,g]/(||g|| n^2)`. **Claim:** `Ch(U,S) <= alpha H(S) + mu H(U)` with

`mu = t_0 R_r/(1 - t_0)`, `alpha = (2 t_W + t_0 R_r/(1 - t_0))/(1 - 8 t_W)`.

*Proof* by induction on `|V \ U|`. The terms reaching `Y` cost at most `2 sum_{I meets S, I meets Y} m_I <= 2 t_W H(S)` (by (P3) and (P1)); the terms with `S'_F` empty cost at most `Cov(S) R_r (H(U) + H(S)) <= t_0 R_r (H(U) + H(S))`; the continuing terms cost at most `alpha sum_F prod m H(S'_F) + mu t_0 (H(U) + H(S)) <= 8 alpha t_W H(S) + mu t_0 (H(U) + H(S))` (by (P3) and (P2)). The coefficients of `H(S)` and `H(U)` add to `alpha` and `mu` exactly by the definitions. ∎

The top level (R09) has the same structure as a record at `U = empty`, `S = J`, with `||g|| = ||delta||` and coverings of `J` by supports other than `J` (the next records are `[J, S_F, g_F]`), so `(2/n^2)||Gamma(delta) - Tr Gamma(delta) rho_*||_1 <= 2 alpha H(J) ||delta||`; with (R08) and `m_J <= t_0`,

`kappa(J) <= (2 t_0 R_r + 2 alpha) H(J) = (c_1 + c_2 r) H(J)`, hence `r <= c_1 + c_2 r` and `r <= beta* := c_1/(1 - c_2)`, with

\[
c_1=4t_0t_W+\frac{4t_W+4t_0t_W/(1-t_0)}{1-8t_W},\qquad c_2=16t_0t_W+\frac{16t_0t_W}{(1-t_0)(1-8t_W)} .
\tag{HNM-BB1-R11}
\]

At the headline weights (exact_first_order, `t_0 = 49/7199290368`, `t_W = 49/6321618`): `c_1 = 8027378053355287230305861131/258892194755027141473290690719232` (about `3.10066437535e-5`), `c_2 = 109268915420665614859/64723048688756785368322672679808` (about `1.69e-12`), `beta* = 8027378053355287230305861131/258892194754590065811608028259796` (about `3.10066437536e-5`). The straddling reach term `4 t_W/(1 - 8 t_W)` dominates `c_1`; the normalization term `4 t_0 t_W` and the removal terms are of order `t_0 t_W`.

### 4.7 The marginal-locality lemma (contract form)

**Lemma 4.1.** For every finite volume `V`, cutoff `L`, region `Y` and pair `c, c'` in `C(m)`:

\[
\|\rho_Y(c)-\rho_Y(c')\|_1\le 2(1+\eta)\sum_{I\cap Y\neq\varnothing}\|c_I-c'_I\|+\sum_{I\cap Y=\varnothing}\kappa(I)\,\|c_I-c'_I\|,\qquad \kappa(I)\le\beta^*H(I)\le\kappa_0\,(w')^{-d_\infty(I,Y)}\,p(|I|),
\tag{HNM-BB1-R12}
\]

with `eta = 0`, `kappa_0 = beta* |Y|`, `w' = 1/lambda = W/2`, `p(n) = n`. At the headline weights (tier exact_first_order, route iterated_split): `eta = 0`, `kappa_0 = beta* |Y|` (for `Y = R`: `2 beta* = 8027378053355287230305861131/129446097377295032905804014129898`), `w' = 512`, `p(|I|) = |I|`. At the crude tier (`t_0 = 37/3125000`, `t_W = 4736/390625`): `beta*_crude = 9033299703247100015296/168195303082000613610691` (about `5.37e-2`). `check.py` checks (R12) end to end, with the one-dimensional cardinality charge `|I| <= 2^{diam I}`, on a seven-site qubit chain with 23 supports: the observed `||rho_0(c) - rho_0(c')||_1^2` is `2.25350180146e-3` (a trace norm of about `4.75e-2`) against the bound `1.00349148556e-1` on the trace norm, and each of the 18 single far-support changes stays within `beta* H(J) ||delta_J||` (`fixture_end_to_end_marginal_lemma`).

### 4.8 Recursion depth and charging constants

- **Depth:** one level per covering region; finite in each finite volume, not bounded uniformly, and no constant depends on it.
- **Per-level factor:** `8 t_W = 196/3160809` (about `6.20094412538e-5`) at `W = 1024`, the same at every depth.
- **Decay per coarse step:** the site potential `lambda = 2/W = 1/512`; the rate of the density bound is the frozen `q = 1/64` of the coefficient input, and the split only needs `lambda < q`.
- **Rejected alternative:** charging `|S_k| t_0` with `|S_k| = (2k+1)^3` (the product of growing region sizes) gives a per-level factor that grows with the depth and exceeds one at depth `264`.
- **Second-order propagation** is built in: a change at `J` reaches `Y` only through a chain of coverings, each link carrying the amplitude of a straddling support; for a change two supports away the chain weight is the product of the two straddling amplitudes, exactly as in the fixture of Section 6.

## 5. Item 4 — the density bounds for every comparison, both signs, each cutoff space, and the untruncated vectors

**Theorem 5.1.** Let `N >= 2`, let `Lambda^A`, `Lambda^B` be finite complete-factor volumes of prescriptions in `{F1, F2}` both containing `Lambda_N`, `|tau| <= 10^-8` of either sign, and `L` any cutoff. Let `rho^A_Y`, `rho^B_Y` be the reduced densities of the normalized ground vectors of the two boxes in `Q_L`. For every finite complete-factor region `Y ⊂ Lambda_N`,

\[
\|\rho^A_Y-\rho^B_Y\|_1\le c_{\rm site}\sum_{y\in Y}q^{\,N-|y|_\infty}\le c_{\rm site}\,|Y|\,q^{\,d_Y}\le c_{\rm site}\,|Y|\,e^{|Y|/10^8}q^{\,d_Y},\qquad c_{\rm site}=K\,(2+\beta^*S_\lambda),
\tag{HNM-BB1-R13}
\]

with `d_Y = N - max_{y in Y}|y|_inf`, `q = 1/64`, `K = 49/111790368`, `S_lambda = 1 + sum_{r>=1}(24 r^2 + 2)(lambda/q)^r = 1 + 24x(1+x)/(1-x)^3 + 2x/(1-x)` at `x = lambda/q = 1/8`, i.e. `S_lambda = 2169/343`. For `Y = R` (`|0|_inf = 0`, `|e_z|_inf = 1`): `||rho^A_R - rho^B_R||_1 <= C q^(N-1)` with `C = c_site (1 + q)`. The same bounds hold for the untruncated ground vectors at fixed `N`.

*Proof.* (i) **Embedding.** Both boxes are embedded in `V` with vacuum padding; this changes neither reduced density on `Y ⊂ Lambda_N`. The I1 padding sites of an F2 box are decoupled reference sites in their vacuum, so they change no coefficient and no reduced density either. (ii) **Lemma 4.1** with `c = c^A`, `c' = c^B` and the majorant `m`: `||rho^A_Y - rho^B_Y||_1 <= 2 sum_{I meets Y} ||delta_I|| + beta* sum_I H(I) ||delta_I|| <= 2 sum_{y in Y} D_y + beta* sum_{x in V} h(x) D_x`, because `sum_I H(I)||delta_I|| = sum_x h(x) D_x` exactly. (iii) **Every-site input.** `D_x <= K q^(N-|x|_inf)` at every site `x` of `V` (Theorem B6). (iv) **Lattice sum.** `|x|_inf <= |y|_inf + d_inf(x,y)` and `q <= 1` give `q^(N-|x|_inf) <= q^(N-|y|_inf) q^(-d_inf(x,y))`, so `sum_x h(x) D_x <= K sum_{y in Y} q^(N-|y|_inf) sum_{x in Z^3}(lambda/q)^{d_inf(x,y)} = K S_lambda sum_{y in Y} q^(N-|y|_inf)`; the number of sites at l-infinity distance `r >= 1` is `(2r+1)^3 - (2r-1)^3 = 24 r^2 + 2`. (v) **Cutoff.** Every constant used (`K`, `t_0`, `t_W`, `beta*`) is independent of `L`, so (R13) holds in every `Q_L`. (vi) **Untruncated vectors at fixed `N`.** Fix `N` and the two volumes. AM2 section 6 gives, for each finite box, self-adjointness on `D(H_0)`, compact resolvent, a simple ground and the untruncated gap `E_1 - E_0 >= 1/2`; for F2 boxes (and every F2 volume containing `Lambda_N`) the AY1 item-by-item verification H1–H5 gives the same facts, including cutoff-vector removal. By AV1 F20–F23 (the trial vector `Q_L psi` converges in energy; the Eckart-type bound `1 - |<psi, psi_L>|^2 <= 2(E_{0,L} - E_0)` with the uniform gap), the cutoff ground **vector** converges to the untruncated ground vector, so `rho^{A,L}_Y -> rho^A_Y` and `rho^{B,L}_Y -> rho^B_Y` in trace norm (partial trace is contractive). The bound passes to the limit through the closed trace-norm ball. The order is fixed: bound uniformly in `L` at fixed `N`, then `L -> infinity` at fixed `N`, then read the bound as a function of `N`; the `N` and `L` limits are never exchanged (the double sequence `L/(N+L)` has iterated limits 0 and 1, `check.py`). ∎

**Constants and targets.**

| constant | tier / route / BA1 input | exact | preview | target | margin |
|---|---|---|---|---|---|
| `C` (R form, `q=1/64`) | exact_first_order / iterated_split / `K=49/111790368` (form b) | `1649304957714574761387109521705122525/1852265838332370761358328329658687644475392` | `8.90425620114e-7` | `1/250000` | `4.49223372468` |
| `c_site` (region form, `q=1/64`) | same | `25373922426378073252109377257001885/28941653723943293146223880150916994444928` | `8.76726764420e-7` | `1/500000` | `2.28121243831` |
| `C_2` (secondary, `q=151552\|tau\|`, labelled) | exact_first_order / iterated_split / `K_2=49/10202112` at `rho=1/151552` (form b, re-instantiated here) | `254713191786858884385903518855136871787/26288652445972361083565698627981857600000000` | `9.68909274868e-6` | `1/20000` | `5.16044188005` |
| `c_site,2` (secondary, labelled) | same | `651079047656055039494458366725211/67298950261689244373928188487633555456` | `9.67443095507e-6` | `1/40000` | `2.58413131646` |
| `C_crude` | crude_majorant / iterated_split / crude input `296/390625` | `1298461471817127563970468301/721137361964077630855837662500` | `1.80057439858e-3` | reported only | fails |
| `c_site,crude` | same | `1598106426851849309502114832/901421702455097038569797078125` | `1.77287325399e-3` | reported only | fails |
| `C_2,crude` / `c_site,2,crude` | crude_majorant / iterated_split / crude input `1/128` | `2429839579729080402559/11718449375821400000000` / `6210976465054127/29999230402102784` | `2.07351630049e-1` / `2.07037860031e-1` | reported only | fail |

The secondary pair uses the split weight `W_2 = 1/(37888|tau|)`, `lambda_2 = q_2/2`, `S = 147`, `t_W = 2T(tau_star) = 49/2018304`, `beta*_2 = 640725571941574538128888129/6596570422054692633635877403388` (about `9.71301041218e-5`). The crude tier at the headline is `2K_crude(1+q)` to leading order and misses its two targets by factors of about 450 and 886; it is retained, never relabelled. The global Lipschitz constant of the fixed-point map (`J_0 G'(R) < 77/781250`) and the volume-independent bound `37/6249384` appear nowhere in these constants.

**Every comparison, both signs.** Theorem 5.1 covers any two volumes containing `Lambda_N` of either prescription, so every comparison of `parameters.comparisons` has the same constants. The `-tau` rows replay the same `|tau|` formula (`check.py` compares them exactly); they are a replay, not a second confirmation.

| comparison | `+tau`: `C`, `c_site` | `-tau`: `C`, `c_site` | each `Q_L` | untruncated, fixed `N` |
|---|---|---|---|---|
| F1 `Lambda_N` vs F1 `Lambda_(N+1)` | `8.90425620114e-7`, `8.76726764420e-7` | same | yes | yes |
| F2 `Lambda_N` vs F2 `Lambda_(N+1)` | same | same | yes | yes |
| F1 vs F2 on the same `Lambda_N` (fixed-`N` change of boundary prescription; source: the `28N(5N+1)` extra faces) | same | same | yes | yes |
| any two centered boxes `Lambda_M`, `Lambda_M'`, `M, M' >= N`, compared directly | same | same | yes | yes |
| two one-prescription volumes containing `Lambda_N`, compared directly (union form `2C = 1.78085124022e-6`, labelled only) | same | same | yes | yes |

**Example values** of `C q^(N-1)`: `N=2`: `1.39129003142e-8`; `N=3`: `2.17389067410e-10`; `N=4`: `3.39670417829e-12`. The rate is per coarse l-infinity step in `N` at fixed spacing (a coarse step is `(4a, 2a, a)` in fine units); it has no physical-length reading.

**Smaller `|tau|`.** `K = 2T(64|tau|)`, `t_0`, `t_W` and `beta*` are increasing in `|tau|` while `q` is fixed, so the cap values bound every `0 < |tau| <= 10^-8`; at `tau = 0` both boxes have `c = 0` and equal densities.

## 6. Item 5 — the finite fixtures, the mandatory sentence and the gate fields

Every fixture below is exact rational arithmetic in `check.py`, labelled `model_is_finite_graph: true` and `transfers_to_aq: false`. The fixtures audit algebra and rejection logic; they prove nothing about infinite volume or about the AQ family.

1. **Coefficient decay is not marginal decay** (`coefficient_decay_not_marginal_decay`). Qubits `r, o, o'` with `c_{r,o} = 1/3` (straddling), `c_o = b`, `c_{o'} = 0`, `R = {r}`. Changing `b` from `1/2` to `0` leaves every coefficient on supports meeting `R` unchanged, yet `rho_r` moves from `[[45/49, 6/49],[6/49, 4/49]]` to `[[9/10, 0],[0, 1/10]]` (trace-norm squared difference `3681/60025`). Inferring state decay from coefficient decay is rejected.
2. **Second-order propagation** (`fixture_second_order_propagation`). Chain `r - o_1 - o_2` with supports `{r,o_1}: a`, `{o_1,o_2}: b`, `{o_2}: c` as polynomial variables. The unnormalized `R`-marginal is, as an exact polynomial, `rho_00 = 1 + b^2 + c^2`, `rho_01 = -a b c`, `rho_11 = a^2 + a^2 c^2`. A change of `c`, two supports away from `R`, moves the off-diagonal element by exactly `-a b` per unit change: the product of the two straddling amplitudes, with no first-order term. A first-order propagation claim, or per-link factors whose product is below `|a b|` (e.g. `a/2` and `b` at `a=1/3, b=1/5`), is rejected. The covering chain of Section 4 reproduces this structure: `{o_2}` is covered by `{o_1,o_2}`, whose outside site is covered by `{r,o_1}`, which reaches `R`.
3. **Normalization coupling, including the global fidelity** (`normalization_couples_supports`, `global_fidelity_orthogonality_catastrophe`). (a) With a straddling creation `a = 1/3` and an outside creation `b = 1/2`, the straddling amplitude enters the excited weight `e^2 = a^2/(1+b^2) = 4/45` at first order in `a`, while the off-diagonal element of `rho_r` is `a b/Z = 6/49`, of second order. Dropping the straddling supports from the split gives the budget `0` instead of `1/3`; normalizing by `1 + O(t^2)` without the product split is rejected. (b) Product states `(x)_{x=1}^{400} Omega_x` and `(x)_{x}(Omega_x + e_x/10)`: the global fidelity `(100/101)^400` is below `1/50`, so any bound through the global overlap exceeds `2 (39/40)^{1/2}` (its square exceeds `39/10`), while the one-site marginals differ by exactly `2/101^{1/2}` (square `4/101`) at every size. A bound through the global overlap of `psi^N` and `psi^(N+1)` is rejected.
4. **Straddling supports** (`normalization_couples_supports`). `R = {r_0, r_1}`, outside `o`, a single creation of amplitude `1/10`. The first-order part of the `R`-marginal is **zero** for the one-site straddling support `{r_0, o}` and also for the support `{r_0, r_1, o}` strictly containing `R`; it is nonzero only for the support `R` itself. At second order both straddling supports give the nonzero population `1/100`. Charging straddling supports only at first order (zero) or dropping them is rejected. (See wording defect D1.)
5. **Split-route trace and Lipschitz** (`fixture_split_lipschitz_and_trace`). (a) Mixed outside states on `H_{o_1} (x) H_{o_2}` (rank-two rational mixtures), with the four supports through `r`: `Tr N_c(omega) = 271121/226800` and `36056951/28058400`, both at least 1; `||rho(omega) - rho(omega')||_1 <= 2||N_c(omega - omega')||_1` and `||N_c(Delta)||_1 <= (2 epsilon + epsilon^2)||Delta||_2 <= (2 epsilon + epsilon^2)||Delta||_1` hold exactly (`epsilon = 57/60`, constant `1121/400`). (b) The identity (R07) and the recursion (R10) hold exactly on a five-site fixture with two excited levels per site; orthogonality at `J` is exact; Lemma 1.3 holds for all 14 single-support changes of a qubit chain. (c) The end-to-end lemma (R12) holds on a seven-site qubit chain (Section 4.7). (d) A split charge by the product of growing region sizes (`(2k+1)^3 t_0`) is rejected in favour of the per-site factor `8 t_W`; a "creation" with a vacuum component gives `Tr = 97/144 < 1` and is rejected.
6. **Polymer identity and cardinality factor** (`fixture_polymer_identity`; the forward route's fixture, exhibited here as item 5 requires). On a four-site qubit collection with nine supports, brute force gives `||psi||^2 = 933636298673/691558560000`, equal to the hard-core gas of 49 polymers (overlap-connected pairs of families with the same excitation set, activity the signed product of their amplitudes). A pair of families with different excitation sets has inner product zero. Cardinality factor: a four-site polymer of activity `z_0 = 1/100` incompatible with four single-site polymers of activity `-1/10`; the Kotecky–Preiss condition `s e^a <= a` holds at `a = 1/8`; the exact cluster sum over clusters containing the big polymer, `log(1 + z_0 (9/10)^{-4})`, lies in `[651100/43046721, 100/6561]`; the majorant with the cardinality factor, `z_0 e^{4a} >= 13/800`, covers it, while dropping the factor gives `z_0 e^{a} < 8 z_0/7 = 2/175`, below the lower end `651100/43046721` (about `1.5125e-2`) of the cluster sum; that majorant is rejected.
7. **Cutoff-limit order and cutoff-vector removal** (`cutoff_limit_order`, `cutoff_vector_removal`). The double sequence `L/(N+L)` has `lim_L lim_N = 0` and `lim_N lim_L = 1`. For `H = diag(0, 1/2, 1)` the Eckart pairs `(1 - |<psi_0, v>|^2, (<v,Hv> - E_0)/gap)` are `(2/11, 3/11)`, `(4/5, 4/5)`, `(1/26, 1/13)`, `(0, 0)`; for the degenerate `diag(0, 0, 1)` the trial vector `e_2` has the ground energy and zero overlap with `e_1`, so eigenvalue convergence alone proves nothing about vectors.

Further exact fixtures: **the outside vector is not a ground state** (three qubits, `H = n_1 + n_2 + n_3 + (7/12)(X_1X_2 + X_2X_3)`, exact ground energy `-1/3` with creations `c_12 = c_23 = 2/7`, `c_13 = -1/7`; for `R = {1}` the outside vector `|00> - (2/7)|11>` has Rayleigh residual squared `1/848` for `H_out = n_2 + n_3 + (7/12)X_2X_3`, so it is not an eigenvector, and no gap argument is ever applied to it); **zero-free region** (`psi(z) = Omega - 2z|11>` has an entire coefficient while its normalization `1 + 4z^2` vanishes at `z = i/2`: analyticity is never extended to the reduced density); **global Lipschitz is not decay** (the map `T(c)_i = (1/2) mean(c) + s_i` on six sites has Lipschitz constant `1/2`, yet `c_0 = 1/6` for every far source position, not `(1/2)^5`); **topology** (`A_k = |e_k><e_k|` tends to zero on the fixed vector `sum_j 2^{-j} e_j`, with `||A_k v||^2 = 4^{-k}`, but `||A_k e_k|| = 1` on the moving vector; the state topology here is the trace norm on `B(H_Y)`).

**The mandatory sentence template, quoted once verbatim:**

> For the zero-selected patterned family at the same coupling |tau|<=10^-8, and for every comparison of the named construction families F1 and F2 on centered coarse cubes, the reduced densities of the finite-box ground vectors on the cover R differ by at most C q^(N-1) in trace norm, in each on-site cutoff space and, at fixed N, for the untruncated ground vectors, where N is the smaller box size; this is locality of the reduced densities of the named constructions at a rate in N, not uniqueness of any ground state, not a statement about other boundary conditions, and not a statement uniform in the lattice spacing a.

Constants for the template: `C = 1649304957714574761387109521705122525/1852265838332370761358328329658687644475392` (about `8.90425620114e-7`) at `q = 1/64` (tier exact_first_order, route iterated_split, BA1 input the gate bound value `K = 49/111790368` used at every site in form (b)); region form `c_site = 25373922426378073252109377257001885/28941653723943293146223880150916994444928` (about `8.76726764420e-7`); both signs; every comparison of `parameters.comparisons`; each `Q_L`; the untruncated vectors at fixed `N`; `N >= 2`.

**Gate fields exported** (exactly `preregistration.gate_fields_required`): `state_decay_claimed: true` with `state_decay_scope` "reduced densities of F1/F2 finite-box ground vectors on R and on regions Y, per comparison"; `rate_in_N_claimed: true`; `false`: `whole_sequence_claimed`, `common_limit_claimed`, `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `continuum_claim`, `translation_invariance_claimed`, `weak_coupling_claim`, `scientific_priority_verified`. The two true fields are exported true only within the stated scope: per comparison of the named constructions, at a rate in `N`.

## 7. Item 6 — scaling and the controls

**`tau -> tau/100` scaling** (each ratio from the same exact formula at `tau` and `tau/100`, no intermediate rounding; the proof weights are the declared ones, `W = 1024` and `W_2 = 1/(37888|tau|)`; exact ratios in `results.json`):

| constant | ratio preview | prefrozen bracket | in bracket |
|---|---|---|---|
| `C` (headline) | `1.00638216785e2` | `[95,105]` (linear in tau with a positive nonlinear correction) | yes |
| `c_site` | `1.00638216785e2` | `[95,105]` | yes |
| `C_2` (secondary) | `1.00150034215e0` | `[99/100,101/100]` | yes |
| `c_site,2` (secondary) | `1.00000000009e0` | `[99/100,101/100]` | yes |
| `q_2 = 151552\|tau\|` | exactly `100` | exactly 100 | yes |

The headline constants are linear in `tau` because `K = 2T(64|tau|)` is; the correction `1/(1 - 9856*64|tau|)` and the split remainder make the ratio slightly above 100. The secondary constants are `tau`-independent to leading order (`K_2 = 2T(1/151552)` does not depend on `tau`); the residual `tau` dependence is `(1 + q_2)` and the order-`t_0` terms of `beta*_2`. The crude ratio (`1.16801910415e2`, labelled, not a target) reflects the factor `1/(1 - 8 t_W)` at `t_W` of order `10^-2`.

**Controls.** All 37 contract controls are executed in `check.py` as damaging mutations; each mutation must raise `AdmissionError` (never `assert`), and a mutation that is accepted aborts the run (`damaging mutation accepted: <label>`). The table lists the mutations (132 in total).

| control | damaging mutations rejected |
|---|---|
| `coherent_evidence_tampering` | seven coherently rehashed contract edits (C target relaxed, q changed, `rate_in_a_claimed` true, a control removed, isolation false, a hash-binding flag flipped, tau changed); a byte change without rehash; a snapshot removed; an admitted gate edited (pinned sha256); an exported `C` halved against its recomputation |
| `exact_arithmetic_admission` | float, bool, `nan`, zero denominator, float bound admission |
| `no_priority_or_continuum_claim` | continuum, priority or weak-coupling flag true; a historical lens used as a premise |
| `changed_model_relabelled` | coupling above the cap; nonzero triple; relabelled model id; SU(3); two dimensions; l1 metric; a finite-graph fixture presented as the AQ result |
| `insufficient_verdict_retained` | R form only, no untruncated passage, crude only, or some comparisons only relabelled accepted; crude headline admitted; tau retuned |
| `tau_scaling_exponent` | quadratic headline (ratio `10^4`); constant headline; linear secondary; `q_2` ratio not 100; a bracket chosen after evaluation |
| `wrong_delta_alpha_hbar_clock` | amplitudes `tau/576` and `tau/9`; `u = theta/8` labelled `theta`; Euclidean clock labelled real time |
| `root_n_misuse` | root-sum-of-squares combination; square-root face count; division by `sqrt N` |
| `tier_mixing_rejected` | exact label with a crude input; exact label with a crude `t`; the BA1 route label `analytic_disc` used as the BB1 route; a Lieb–Robinson tier; the forward route label; BA1 input unnamed |
| `reverse_premise_isolation` | a forward BB1 file, a BB2 reverse file, a skeptic triage, a lens memo or a deliberation file added; a premise missing |
| `uniform_in_N_not_in_a` | "uniform in the lattice spacing"; an unqualified "uniform" next to a rate |
| `placeholder_span_rejected` | angle-bracket spans with a space, a bar or `e.g.` in an exported statement |
| `negation_aware_phrase_scan` | five affirmative forbidden phrasings appended to the report (a negated one is accepted) |
| `parameters_declare_metric_weights_window` | metric, weights, window, clock or coefficient input removed from a coherently rehashed contract |
| `rate_constant_pair_prefrozen` | `q = 1/128`; C or c_site target changed; `q` optimized per `N`; split weight beyond `1/(37888|tau|)`; weights declared after the constants; secondary pair presented as the headline; secondary `q` changed; split weight `W = 64` too small for the rate (`lambda/q = 2`) |
| `decay_rate_in_N_not_a` | per fm; per lattice spacing; per physical length |
| `topology_named` | weak operator topology; Hilbert–Schmidt norm; strong topology on a fixed vector |
| `two_families_named` | single family; an unfrozen class; F2 collapsed onto F1 (zero extra faces) |
| `subsequence_versus_whole_sequence` | whole-sequence convergence claimed; a common limit claimed |
| `common_clock` | the two families at different couplings; a different clock |
| `coefficient_decay_not_marginal_decay` | state decay inferred from the zero coefficient difference of fixture 1 |
| `normalization_couples_supports` | straddling supports dropped; straddling supports charged at first order only; normalization `1 + O(t^2)` without the split |
| `outside_vector_not_ground_state` | a gap argument applied to the outside vector |
| `global_fidelity_orthogonality_catastrophe` | a bound through the global overlap |
| `marginal_locality_constants_explicit` | a criterion without activity bounds and counts; `eta` missing; a float `kappa_0`; an unstated polynomial |
| `cutoff_uniform_then_removed` | constants depending on `L`; removal before the uniform bound |
| `cutoff_vector_removal` | eigenvalue convergence only; AM2 section 6 cited alone |
| `region_constant_scales_with_Y` | the R constant reused without the `\|Y\|` factor; exponent `N-1` for every `Y` |
| `named_construction_not_uniqueness` | three forbidden phrasings appended to a statement (uniqueness of the infinite-volume ground state, the thermodynamic limit, the infinite-volume ground state), none of which is asserted anywhere in this packet |
| `global_lipschitz_not_decay` | fixed-point Lipschitz constant, the no-decay bound `37/6249384`, a density Lipschitz constant in the coefficients or in the outside state used as a decay factor; the mean-field claim `(1/2)^5` |
| `fixture_second_order_propagation` | a first-order propagation claim; a per-link factor below the exact one |
| `fixture_split_lipschitz_and_trace` | the growing-region-size charge; a vacuum-component creation (`Tr = 97/144`) |
| `fixture_polymer_identity` | the cardinality factor dropped; a polymer sum that differs from the brute-force norm |
| `zero_free_region_required` | analyticity claimed for the reduced density or the normalization without a zero-free region |
| `every_site_coefficient_input` | an R-only input used at far sites; the restated form cited as admitted without its proof; the exponent `N-1` at every site |
| `mixed_weight_lemma_proved` | the mixed-weight contraction cited from BA1; the loss `w e^{b}` instead of `w e^{4b}` |
| `cutoff_limit_order` | the `N` and cutoff limits exchanged |

## 8. Error ledger (`preregistration.error_terms_itemized`, added linearly)

The headline `C` decomposes exactly (`check.py`: the parts add to `C`):

| term | contribution to `C` (exact) | preview | note |
|---|---|---|---|
| `coefficient_input_every_site` | `2K(1+q) = 3185/3577291776` | `8.90338333978e-7` | supports meeting `R`, `kappa = 2`, `D_0 <= K q^N`, `D_{e_z} <= K q^(N-1)`; the far-site input enters the split rows through `S_lambda` |
| `straddling_supports` | `K S_lambda (1+q) 4 t_W/(1-8t_W) = 109655/1256270543557632` | `8.72861347918e-11` | covering chains that reach `Y` (Section 4.6), every order in the straddling amplitudes |
| `normalization` | `K S_lambda (1+q) 4 t_0 t_W = 5373095/9044817287902850127495168` | `5.94052353847e-19` | the `a`-term of (R08) (weight of the `J`-excited component); the normalizations cancel exactly otherwise (`Z >= n^2`) |
| `polymer_or_split_remainder` | removal terms `413315/695712027867640605858816` plus the closure feedback `beta* - c_1` (exact value in `results.json`, about `1.47e-22`) | `5.94089197030e-19` + `1.47361127187e-22` | split remainder: coverings ending inside the region (removal influence) and the self-consistent closure |
| `cutoff_removal_at_fixed_N` | not applicable as a numeric cost | — | an exact limit at fixed `N` (AV1 F20–F23; AY1 for F2): constants are independent of `L` and the bound passes to the untruncated vectors through the closed ball |
| `arithmetic` | not applicable as a numeric cost | — | exact `Fraction` arithmetic throughout; the only enclosure is the directed `e^{1/8} < 8/7`; decimals are truncated previews |

Deterministic terms add linearly; nothing is combined as a root sum of squares or divided by a root of a volume or face count. The same decomposition holds for `c_site` without the factor `(1+q)`.

## 9. Scope, exclusions, claim flags and honest gaps

**Exclusions** (the contract's, respected): whole-sequence convergence or a common limit (BB2); uniqueness of every infinite-volume ground state; boundary conditions outside the named constructions; analyticity of the reduced density in the coupling; any estimate uniform in the lattice spacing `a`; continuum or weak coupling; scientific priority.

**Claim flags** in `results.json`, all `false`: `continuum_claim`, `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `scientific_priority_verified`, `whole_sequence_claimed`, `common_limit_claimed`, `translation_invariance_claimed`, `weak_coupling_claim`. `state_decay_claimed` and `rate_in_N_claimed` are `true` only within the scope stated in Section 6.

**What this is not.** Theorem 5.1 bounds the difference of two reduced densities of the named constructions for each pair of boxes. It is not uniqueness of any ground state and says nothing about boundary conditions outside F1 and F2. Although the bound has the form of a Cauchy estimate in `N`, the whole-sequence consequence and any common limit are BB2's subject and are not claimed here. The constants are uniform in `N` at fixed spacing and uniform in the cutoff, not uniform in the lattice spacing `a`; the rate is per coarse step in `N`. The model is at fixed spacing and extreme strong bare coupling (`|tau| <= 10^-8`).

**Inherited without re-proof** (admitted premises): the AM2 multilinear majorant HNM-AM2.5, its fixed point, uniqueness in the ball, excited-sector exclusion and section 6 facts; the AV1 first-order coefficient, the first-order face counts and the cutoff-vector removal F20–F23; the AY1 item-by-item F2 verification H1–H5; the I1 dictionary and class table. Banach's theorem, Weierstrass' theorem and the maximum principle are standard and not machine-checked.

**Readings and honest gaps.**
- *F2 volumes other than centered cubes.* AY1 itemized H1–H5 for F2 on `Lambda_N`. Each hypothesis is local (on-site operator, grouping per anchor, `|X_b| <= 4`, per-site sum through `b in u-S`, cutoff compression), so the itemization applies verbatim to every finite F2 volume containing `Lambda_N`; this is used for the fifth comparison and stated here as a reading.
- *Fixtures* audit algebra and rejection logic. The infinite-dimensional statements rest on the arguments of Sections 1–5.
- *Upper bounds only.* Nothing here lower-bounds the actual distance of the two densities. The `-tau` rows replay the same `|tau|` formula.
- *Margins.* The headline margin is about `4.49` and the region margin about `2.28`; the near term `2K(1+q)` is essentially the whole constant, so the constants are governed by the BA1 input, not by the split. The split remainder is five orders of magnitude smaller at the declared weight.
- *Independence* is limited to derivation, constants and code. The route, the targets and the brackets are shared through the contract, and the coefficient input is BA1's analytic-disc theorem, restated and re-proved here for every site.

## 10. Contract wording defects and readings (for the skeptic and the advisor)

- **D1 (`normalization_couples_supports`).** The semantics say "a one-site straddling first-order face has zero R-marginal while a support strictly containing R does not". At first order **every** straddling support has zero `R`-marginal, including one strictly containing `R`: fixture 4 gives zero first-order marginal for `{r_0, r_1, o}`. The nonzero first-order marginal comes from supports **contained in** `R` (AY1: the 10 faces with owner set exactly `R`). Read as: straddling supports vanish at first order under the `R`-marginal but not at second order; the fixture exhibits both.
- **D2 (`parameters.weights`, reverse).** The reverse split weight is not given a value; "at most 1/(37888|tau|) after the cardinality loss" is read as: the declared `W` (which already contains the factor 2 of the cardinality charge through `lambda = 2/W`) must satisfy the weighted self-map, `W <= 1/(37888|tau|)`. The declared values are `W = 1024` and `W_2 = 1/(37888|tau|)`.
- **D3 (`coefficient_input` form (b)).** "Every source term of every comparison lies at l-infinity distance at least `N-|u|_inf` from `u`" is stated for `u` in the smaller box; for sites of the union volume outside `Lambda_N` the exponent `N - |u|_inf` is negative and the bound comes from the per-box circle bound at the real point (Theorem B6 (v)).
- **D4 (`marginal_locality_constants_explicit`).** The form `kappa(I) <= kappa_0 (w')^(-d_inf(I,Y)) p(|I|)` has no `|Y|`; for a region the constant scales with `|Y|` (`kappa_0 = beta* |Y|`), consistent with `region_constant_scales_with_Y`.
- **D5 (`rate_constant_pair.secondary`).** "rho = |tau|/q_2 (1/151552 at the cap)": since `q_2 = 151552|tau|`, the radius `|tau|/q_2 = 1/151552` at every `tau`, not only at the cap; this is why the secondary constants are `tau`-independent to leading order.
- **D6 (item 5 and `fixture_polymer_identity`).** The polymer identity and the cardinality factor belong to the forward route; the reverse exhibits the fixture as item 5 requires, labelled as the other route's fixture.
- **D7 (`tier_names_allowed`).** The list mixes the BB1 tiers, the BB1 routes and the BA1 input routes; `tier_label_rule` separates them, and each constant here carries exactly one tier (exact_first_order or crude_majorant), one route (iterated_split) and one BA1 input.

## 11. Item and control map

- **Item 1:** Lemmas 1.1–1.4 (Section 1); checks `fixture_trace_at_least_one_and_lipschitz`, `fixture_lemma_g`.
- **Item 2:** forward route, not executed here; its fixture is exhibited (fixture 6).
- **Item 3:** Section 4 (R06–R12); checks `fixture_split_route_identities`, `fixture_end_to_end_marginal_lemma`, `marginal_locality_lemma_constants`, `per_site_charging_versus_growing_sizes`.
- **Item 4:** Sections 2, 3 and 5; checks `ba1_every_site_input_constant`, `every_site_common_core_enumerated`, `order_versus_distance_every_site`, `f2_extra_faces_28N_5N_plus_1`, `headline_C_meets_target`, `region_c_site_meets_target`, `secondary_pair_meets_targets`, `crude_tier_reported_separately`, `every_comparison_both_signs`, `cutoff_uniform_then_removed_at_fixed_N`.
- **Item 5:** Section 6; checks `fixture_*`, `polymer_identity_fixture_values`, `mandatory_template_quoted_once_and_phrase_scan_clean`, `gate_fields_exported`.
- **Item 6:** Section 7; checks `tau_scaling_every_headline_constant`, the 37 control checks and `contract_controls_all_executed`.
- **Hash binding:** `contract_snapshot_bound` (before any evaluation), `check_py_sha256_recorded_before_evaluation`, `admitted_gate_sha256_pinned` (AM2, AQ1, AV1, AW1, AY1, AY2, BA1, BA2 gates), `reverse_inputs_inventory_exact`, `report_pins_exact_values`.

**Methodological lenses** (frozen method snapshots, used as modern method rules only; no historical person endorses anything here). *Newton:* analysis ran backwards from the density bound to the single-support influence and the covering chains; synthesis runs forwards through Lemmas B1–B6, W1–W2, 1.1–1.4 and 4.1. *Tesla:* complete accounting of source, load and transfer: the source is every support whose coefficient differs, the load is the reduced density on `Y`, and the transfer is a chain of coverings, each link charged once at the site where it is entered. *Historical panel:* a weight loss is paid at every step (the factor `8 t_W` per level), and coefficient decay is never called state decay.

## 12. Reproduce

```bash
python3 -B research/round33/reverse/bb1/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/reverse/bb1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/freeze.py verify research/round33/reverse/bb1
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/bb1.json research/round33/reverse/bb1/report.md
```

`check.py` verifies the contract snapshot sha256 before any evaluation, records its own sha256 before evaluation, pins the sha256 of the eight admitted gates it reads, reads the targets, brackets and template from the contract, and writes `results.json` (78 checks) and `source-manifest.json`, which binds this report, the checker and all 35 input snapshots. `freeze.json` binds the whole producer closure.
