# BB1 skeptical review (post-comparison)

**Verdict: `accepted_within_scope`, sub-label `boundary_decay_rate_only`, secondary `static_not_dynamic`.** There are no blocking issues. The verdict carries one route-level limitation: the frozen forward packet cites the Kotecký–Preiss theorem without a committed excerpt (item 3 below). The bound values do not depend on that citation. After this review the advisor accepted the ruling and committed an Ueltschi excerpt. Checked post hoc against it, the cited statement and its use in Corollary 6.3 and Lemma 6.4 are covered, with no missing factor (`bb1-kp-repair.md`).

Both routes prove the frozen density bounds in the `exact_first_order` tier. They hold for every comparison of the contract, at both signs, in each on-site cutoff space `Q_L` with constants independent of `L`, and at fixed `N` for the untruncated finite-box ground vectors. The two frozen forms are:
- the **R form**: `||rho^box1_R - rho^box2_R||_1 <= C q^(N-1)`, with `q=1/64`;
- the **region form**: `||rho^box1_Y - rho^box2_Y||_1 <= c_site |Y| e^{|Y|/10^8} q^{d_Y}`.

The routes:
- **Forward (`polymer_kp`).** A hard-core polymer representation of the norm and of the Y-marginal. The marginal is written as Y-clusters weighted by vacuum probabilities `pi(S)=Z(Lambda\S)/Z(Lambda)`, each at most 1. The proof adds an exploration-tree majorant and a new mixed-weight contraction lemma (loss `w e^{4b}` charged once per interaction term). It verifies the Kotecký–Preiss condition with `a=taubar^2` and uses the real-parameter derivative along `c+lambda(c'-c)`.
- **Reverse (`iterated_split`).** Single-support telescoping. The influence of a support meeting `Y` is exactly 2 (`eta=0`). A far support is handled by the product-ordering split at the changed support (identity R07). Contracting with the excited `delta_J` keeps only coverings of `J` (R09/R10). Each level is charged per site through `h(x)=sum_y lambda^{d(x,y)}`, `lambda=2/W`, `W=1024`, `|I|<=8*2^{diam I}`. The recursion closes with `r <= beta* = c1/(1-c2)`.

Both routes use the same coefficient input. It is the BA1 gate's bound value `K=49/111790368` at every site of the union volume: `sum_{I contains u}||delta_I|| <= K q^{(N-|u|_inf)_+}`. This is form (b), and each packet proves it in full (forward Theorem 8.1, reverse Theorem B6).

**What the gate should bind.** The rule is to bind the larger valid constant per quantity and label the other route's value.

| quantity | bound value (exact) | preview | route, tier | target | margin | other route (labelled) |
|---|---|---|---|---|---|---|
| `C` (R form, `q=1/64`) | `578430793501182095316361404668712117814097366497488882433123687207743348935643590594947878052521565633072717772804866626438590065415931413647325/649548567473042337664409810664855266791889949984121342174530956201606073245694809426490159178862195173312829634280741896750749402941566759659762614272` | **8.905120e-7** | polymer_kp, exact_first_order | `1/250000` | 4.4918 | iterated_split `1649304957714574761387109521705122525/1852265838332370761358328329658687644475392` ≈ 8.904256e-7 |
| `c_site` (region form, `q=1/64`) | `207042404781481370031872233170526436180882031154261216585642344563461649618003876497888095865804915933/236130948514531640807035481765249880343283808663306771542081002582898728697162432799219796273340474330185728` | **8.768118e-7** | polymer_kp, exact_first_order | `1/500000` | **2.2810** | iterated_split `25373922426378073252109377257001885/28941653723943293146223880150916994444928` ≈ 8.767268e-7 |
| `C_2` (labelled secondary, `q_2=151552|tau|`) | `254713191786858884385903518855136871787/26288652445972361083565698627981857600000000` | 9.689093e-6 | iterated_split, exact_first_order, `K_2=49/10202112` | `1/20000` | 5.1604 | polymer_kp ≈ 9.644014e-6 |
| `c_site,2` (labelled secondary) | `651079047656055039494458366725211/67298950261689244373928188487633555456` | 9.674431e-6 | iterated_split | `1/40000` | 2.5841 | polymer_kp ≈ 9.629421e-6 |

Every bound value is at least the value that the **self-contained** iterated_split route proves for the same quantity. So each bound value is certified by the reverse alone, whatever is decided about the forward's cited theorem.

**Checks run.** The review program is `bb1_postreview_check.py`. Its output is `bb1-postreview/results.json` (sha256 `8d3c14ba…7cd32d`), byte-identical under `-B` and `-B -O`. It runs:
- **21 exact checks**, including `kp_citation_checked_against_committed_excerpt`, added for the repair: it pins the excerpt hash, checks that the excerpt is absent from both producer inventories, checks the anchored statements in the excerpt and in the forward report, and re-verifies the side conditions at every tier;
- **82 source-edit runs on temporary copies**:
  - 2 unmutated copies, each reproducing its frozen output byte for byte;
  - 74 validator weakenings, one per contract control per producer, each aborting with a damaging mutation of that same control;
  - 6 input edits, each aborting without output;
- **15 damaged packets**, each rejected by the review's own value validator for the expected reason.

Both producers replay byte for byte under normal and `-O` Python, and `tools/freeze.py verify` reports both closures verified (`bb1-replays.json`).

## What is proved, with quantifiers

**Model: `AQ_patterned_zero_selected`.**
- SU(2) in Kogut–Susskind form on Z^3 at fixed spacing, with coarse 24-link factors.
- Selected triple exactly (0,0,0), with the Haar product reference.
- 21 omitted faces per anchor, entering as `-(tau/3)W_f` in normalized units `delta=alpha/8`.
- Both signs, `|tau|<=10^-8`.
- The AM2 creation expansion, with `J<=28|tau|`, `R=1/64`, `G(t)=16e^{8t}(1+10t)`, `G(R)<148/7` and `G'(R)<352`.
- Cover `R={0,e_z}`, the coarse l∞ metric (star diameter 1), and the trace norm on `B(H_Y)`.

**Families.**
- F1: the AQ1 centered whole-star boxes `Lambda_N=[-N,N]^3`.
- F2: the I1 §6 all-contained-face boxes with padding, on the same `Lambda_N`.
- `N>=2`.

**Statement.** Let `N` be the smaller box size. For each of the five comparisons (c1–c5 below), both signs, every `Q_L`, and at fixed `N` the untruncated ground vectors:
- `||rho^box1_R - rho^box2_R||_1 <= C q^(N-1)`;
- for every finite complete-factor region `Y` inside `Lambda_N`: `||rho^box1_Y - rho^box2_Y||_1 <= c_site |Y| e^{|Y|/10^8} q^{d_Y}`, where `d_Y = N - max_{y in Y}|y|_inf`.

The reverse proves the stronger form `c_site sum_{y in Y} q^(N-|y|_inf)`, with no exponential factor.

**The five comparisons.**
- c1: F1 `Lambda_N` versus `Lambda_(N+1)`.
- c2: F2 `Lambda_N` versus `Lambda_(N+1)`.
- c3: the fixed-`N` comparison of F1 versus F2 on the same `Lambda_N`.
- c4: any two centered boxes of size at least `N`, of either family, compared directly.
- c5: two finite complete-factor volumes of one prescription, both containing `Lambda_N`, compared directly. The route through the union volume costs a factor 2 and is labelled only: `2C` ≈ 1.78102e-6 forward, 1.78085e-6 reverse.

**Scope.** This is locality of the reduced densities of the named constructions, at a rate in N per coarse l∞ step at fixed spacing.
- It is not uniqueness of any ground state.
- It is not whole-sequence convergence, not a common limit and not a translation statement (those are BB2's subject).
- It is not a statement about other boundary conditions, and not uniform in the lattice spacing a.
- No analyticity of the reduced density is claimed.

The 11 frozen gate fields hold exactly as prefrozen, in both packets and in this review. `state_decay_claimed` and `rate_in_N_claimed` are true, with the frozen scope. Every other Boolean is false.

## Predictions against producers

My pre-comparison package (`09d0bdb`, committed 00:28:59Z) came before both producer commits (forward 00:49:30Z, reverse 02:06:29Z).

| quantity | skeptic (pre) | forward (polymer_kp) | reverse (iterated_split) | status |
|---|---|---|---|---|
| every-site input `K`, `K_2`, crude `K` | 49/111790368, 49/10202112, 296/390625 | = | = | identical |
| near term `2K(1+q)` (q^N at 0, q^(N-1) at e_z; my R3) | 3185/3577291776 ≈ 8.90338e-7 | = (ledger item 1) | = (ledger item 1) | identical |
| `C` at q=1/64 | 8.903452e-7 | 8.905120e-7 | 8.904256e-7 | differ by far-site majorant only; rel. 1.9e-4 and 9.0e-5 |
| `c_site` | 8.766443e-7 (binding margin 2.2814) | 8.768118e-7 (2.2810) | 8.767268e-7 (2.2812) | same; the region margin binds in all three |
| `C` with the R-only gate input | 1.7533e-6 | not used | not used | both use form (b) at every site (R3) |
| secondary `C_2`, `c_site,2` | 9.6213e-6, 9.6063e-6 | 9.6440e-6, 9.6294e-6 | 9.6891e-6, 9.6744e-6 | all meet 1/20000, 1/40000 |
| crude `C` | 1.5624e-3 | 2.0529e-3 | 1.8006e-3 | all fail 1/250000; retained |
| crude `c_site` in the frozen form | "not writable" (my R8) | not writable ((1+t)^2-1 ≈ 1.18e-5); 2.0212e-3 reported outside the form | 1.7729e-3 in the frozen form (eta=0), fails | **self-correction below** |
| τ ratio, C / c_site | 100.629 | 100.64788 / 100.64788 | 100.63822 / 100.63822 | all in [95,105] |
| τ ratio, secondary / q_2 | 1.0015, 1.0000 / 100 | 1.00150, 1.00000 / 100 | 1.00150, 1.0000000001 / 100 | in [99/100,101/100]; q_2 exactly 100 |
| F1-vs-F2 extra faces | 28N(5N+1) = 616/1344/2352 | = | = | identical |

**Where the three values of `C` come from.** All three share the near term `2K(1+q)`, which is 99.98% of `C`. They differ only in how the far sites are charged:
- **Skeptic:** a truncated-correlation recursion with weight 64.
- **Forward:** the Y-cluster derivative (Term I, straddling, 8.683e-11) plus the vacuum-probability derivative (Term II, normalization, 8.683e-11), with KP clusters at 2.8e-20.
- **Reverse:** covering chains, `K S_lambda (1+q) 4t_W/(1-8t_W)` = 8.729e-11; its normalization term `4t_0t_W` is only O(1e-19).

The forward pays the far-site cost twice, once through the straddling families and once through the normalization. That is why it is the larger. All three are valid upper bounds of their own proofs, and the review re-derives each producer value exactly from its declared formula (`forward_values_reproduced_exactly`, `reverse_values_reproduced_exactly`).

**Self-correction (R8).** My pre-comparison said a crude region constant cannot be written in the frozen form. That holds for routes whose near term carries `(1+t)^{|Y|}` with the crude anchored norm. It fails for the reverse: its `eta=0` has no exponential factor, so its crude `c_site` ≈ 1.7729e-3 is in the frozen form. It fails the target and is retained.

## Items adjudicated

### 1. Headlines; identical constants across comparisons and signs; c3 and c5 proved

**Identical constants are justified.** The density lemma (forward F10 with F12–F13; reverse R12 with R13) sees a comparison only through two things:
- **the per-site coefficient differences `D(x)`.** The every-site input bounds these by `K q^{(N-|x|_inf)_+}` for any two volumes of either prescription containing `Lambda_N`. The common-core lemma (forward Lemma 8.6, reverse Lemma B5) says every omitted face within distance `N-|u|_inf-1` of `u` lies in a star `b+S` inside `Lambda_N`, so both prescriptions retain it on every volume containing `Lambda_N`. Every source term of every comparison therefore lies at distance at least `N-|u|_inf` from `u`.
- **the norms of the two fixed points** (`t`, `taubar`; `t_0`, `t_W`). These are bounded for every volume of either prescription (the AM2 majorant; the AY1 H1–H5 itemization for F2).

The constant therefore does not depend on which comparison is made. The `-tau` rows replay the same `|tau|` formula (every majorant depends on `|z|`), so they are a replay, not a second confirmation.

**c3 (fixed N, F1 versus F2 on the same `Lambda_N`) is proved, not only asserted.** It is a case of the general theorem, and its source set is enumerated separately by all three packets:
- The source is the `28N(5N+1)` extra F2 faces on the outer layer of `Lambda_N`: 616, 1344 and 2352 at N=2,3,4 (forward Corollary 9.2, reverse Lemma B5 enumeration, my rows `F1_N/F2_N`).
- These faces lie at distance `N-1` from `e_z` and `N` from `0`.
- The forward check `fixed_N_F1_versus_F2_item` and the reverse check `every_site_common_core_enumerated` pass.

**c5 (two one-prescription volumes containing `Lambda_N`, direct) is proved.** Both producers prove the every-site input for **any** two finite complete-factor volumes of prescriptions in {F1,F2} containing `Lambda_N` (forward Theorem 8.1, reverse Theorem B6). Each then runs the density lemma **once** on the union volume `V^A ∪ V^B`, which is only the embedding space: the fixed point of each volume is supported in that volume, and the padding sites are in the vacuum. So the comparison is direct, with the same constants.
- The union route (each volume against the union, then the triangle inequality) is labelled only, at `2C`.
- Enumeration audits:
  - forward: cuboids `[-2,3]x[-2,2]x[-2,4]` versus `[-3,2]x[-2,3]x[-2,2]`, for F1 and for F2;
  - reverse: F1 on `[-2,3]x[-2,2]x[-2,4]` versus F1 `Lambda_3`, and F2 on `[-3,2]x[-2,3]x[-2,2]` versus F2 `Lambda_2`;
  - mine: general F1/F2 volumes at N=2,3.
- In every audit, every source site has `|p|_inf >= N` (check `fixed_N_and_general_volume_source_distances`).

**c4** (any two centered boxes, direct) is the same theorem, with no telescoping.

### 2. R6: where each producer charges the normalization of intermediate regions

My R6 risk was specific. Re-splitting an intermediate region `S` and expanding over every family meeting it produces `prod_{s in S}(1+sum||c||)^2 ≈ e^{2taubar|S|}`, which overwhelms a diameter weight once `|S|` grows. Neither producer creates that factor.

**Forward.**
- **Normalization.** It enters only through the vacuum probabilities of the Y-cluster supports, `rho_Y = sum_eta rho_eta pi(supp eta)` (F06), with `pi<=1`. The vacuum probabilities come from `Z(Lambda\S) = <psi, P_S psi> >= 1`, which is proved directly.
- **Derivative.** For Term II the forward writes `pi'(S)/pi(S) = -sum_{gamma meets S} w'(gamma) pi_Lambda(gamma) + sum_{gamma in Lambda\S} w'(gamma)(pi_{Lambda\S}(gamma) - pi_Lambda(gamma))`. The truncated difference is bounded by the KP cluster sum (Lemma 6.4, F08), with no `e^{a|gamma|}` factor, because both probabilities are real, positive and at most 1.
- **Cardinality.** The cardinality factor of the KP tree majorant is carried by the mixed weight `W(I)=w^{diam I}e^{b|I|}` of the fixed points. The mixed-weight lemma (§5) gives the loss `w e^{4b}` once per interaction term, with `e^b=1001/1000`, `Gamma ≈ 1.900e-2` and `taubar ≈ 6.680e-7`.
- **Uniformity.** Every bound is a lattice sum over `Z^3` of the per-site data: `S_{v/w}=725` and `S_{1/(qv)}=147` at `v=2/q`, `w=3/q`. It is **uniform in N and in L**.

**Reverse.**
- **No intermediate normalization.** None is ever divided by. The split at the changed support `J` uses orthogonality at `J`, so `Z >= n^2` (R07–R08).
- **Coverings only.** The contraction with `delta_J`, which is excited at every site of `J`, keeps only families covering `J` (R09). The recursion (R10) keeps only coverings at every level, and the spectator families cancel exactly.
- **Covering bound and charging.** The covering sums obey `Cov(T) <= t_0` (P3). Support sizes are charged once per site through `|I| lambda^{-diam I} <= 8W^{diam I}` (P2), giving the per-level factor `8t_W = 196/3160809` at every depth.
- **Depth and closure.** The recursion depth is finite in each volume and unbounded in general, and no constant depends on it. The closure `r <= beta* = c1/(1-c2) ≈ 3.10066e-5` is **uniform in N and in L**.

**My own exact fixtures** (check `own_exact_fixtures_split_and_cluster_identities`) use a five-site qubit chain with eight supports:
- The reverse identity (R07) holds exactly at a **two-site** changed support `J={2,3}`, where non-covering families exist: 6 families meet `J`, 3 of them cover it, and the non-covering ones cancel exactly under the contraction.
- The forward Y-cluster formula (F06) with vacuum probabilities in (0,1] reproduces `rho_Y` for `Y={0}` (17 Y-clusters) and `Y={0,1}` (69).
- `Cov(T) <= t_0` for every region `T`.

**R6 is resolved by both producers.**

### 3. The forward cites Kotecký–Preiss without a committed excerpt

**Finding.** The forward states Theorem 6.1 (Kotecký–Preiss 1986, in Ueltschi's 2004 decay-function form) as **cited, not re-proved, not machine-checked**, and says the primary sources were not re-inspected. The theorem is used in Corollary 6.3 (site decay of cluster sums) and Lemma 6.4 (truncated vacuum probabilities, F08). Those feed the normalization Term II of Theorem 7.1.

**It is not discharged by the report's own lemmas.** Lemmas 4.1–4.3 (the exploration tree) bound sums over single polymers or Y-clusters of products of activities: `sum_{gamma contains x} prod u_K <= sigma^2`. That is the **hypothesis** side of KP. The **consequence** used in F08 is a bound on Ursell-weighted sums over clusters, which are connected multisets of polymers: `sum_{X not~ gamma}|Phi^T(X)|e^{d(X)} <= a(gamma)`. It needs the tree-graph inequality and the KP induction, and neither is proved in the packet. The checker's exact audit of F08 on a six-site chain is a finite check, not a proof. The step is load-bearing for uniformity in N:
- without F08, the far polymers' contribution to the vacuum-probability derivative would not decay with distance;
- numerically it is negligible (the KP-cluster ledger item is ≈ 2.8e-20 of `C`).

**Decision: a limitation, not a blocking issue.** Four reasons:
1. **The contract builds the theorem in.** Required item 2 asks the forward for "the Kotecky-Preiss condition with an explicit a, weights and tree majorant", that is, for verifying the hypotheses of a named external theorem. The forward does verify them with exact numbers: `a=taubar^2`, `a<=2b` with `b>=1/1001`, `v=128<=w=192`, and loss `w e^{4b} <= w_max`. The hypotheses match the standard statement as known to this reviewer, including the test-set device and the cardinality factor `a|supp gamma|`. That is equally not a check against the source.
2. **The excerpt rule never reached the contract.** The plan's contract rule (P4) says "an external theorem is quoted from a committed source excerpt with its PDF hash, never from a report that cites it". It was **not carried into the BB1 contract**, and neither `research/round33/sources/` nor the shared premises hold a KP or Ueltschi excerpt. The forward could only read its `inputs/`, so it had no excerpt to quote. This is contract defect **D2** of this review. My pre-freeze and pre-comparison reviews missed it.
3. **No bound value depends on the citation.** The headline values bound are the forward's, and they exceed the reverse's self-contained values. The secondary values bound are the reverse's.
4. **The same class of citation is already accepted.** Banach, Weierstrass and the maximum principle are accepted throughout Round33 (BA1 gate).

**Repair (post hoc, after the advisor's decision).** The advisor accepted this ruling and committed `research/round33/sources/ueltschi-math-ph-0304003v3.md` (sha256 `17b0b3ff…0eed66`). It excerpts Ueltschi, arXiv:math-ph/0304003v3 (PDF sha256 `2cc3e036…22bdbfc`): Theorems 1 and 3 with (3)–(5) and (16)–(19), and the hard-core §4.2. The excerpt is committed after the freeze and is not a premise of either packet. My comparison is in `bb1-kp-repair.md`:
- **Dictionary.** Hard-core `ζ ∈ {0,−1}` (so `|1+ζ_c| ≤ 1` holds identically), `c ≡ 0`, `b = d` (`d(γ) = ln(v)·Σ_{K∈γ} diam K ≥ 0`) and `a(γ) = a|supp γ|`.
- **Hypothesis.** Ueltschi (16) is exactly the forward's hypothesis.
- **Cluster expansion.** Theorem 1 gives `Z(Λ') = exp Σ Φ^T`, absolutely convergent, for every `Λ'`.
- **Conclusion.** (19) gives `Σ_{X≁γ} |Φ^T(X)| e^{d(X)} ≤ a(γ)`. The forward's `e^{d(X)} = Π_{γ'∈X} e^{d(γ')}` is exactly the `µ_b` weighting, counted with multiplicity. Ueltschi's incompatibility count `Σ_i |ζ(A,A_i)| ≥ 1` only strengthens the bound over the forward's indicator.
- **Test sets.** The test-set clause is the instance with finite site sets adjoined as atoms of `µ`-mass 0 and `a(S) = a|S|`. That needs one sentence, which is the forward's own parenthetical.
- **The use.** Corollary 6.3 and Lemma 6.4 add only the forward's own elementary steps: the sequence-to-multiset conversion, the connectivity bound `e^{d(X)} ≥ v^{d(z,s)}`, and the real positivity of the vacuum probabilities.
- **Result.** No factor is missing and there is no different hypothesis form. **The cited statement and its use are covered by the committed source.** The original Kotecký–Preiss paper is neither committed nor needed. The limitation stays, because the check is post hoc and outside the frozen packet, but it no longer reads "complete only modulo the cited theorem". The verdict stays `accepted_within_scope`.

**What the gate binds under each reading.**
- **As recommended (a limitation).** The bound values are those in the table above. The frozen packet is not edited. The repair I recommended has been applied (next paragraph), so the limitation text now records the post-hoc check and its result.
- **If the advisor holds P4 binding on the frozen producer itself.** This is retained as `conditional_alternative` in `bb1.json`, as the advisor asked; after the repair it is not recommended. Then the forward is incomplete as a proof, and the contract's acceptance text reads "only one route" → **`limited`**. The gate would bind the reverse constants: `C = 1649304957714574761387109521705122525/1852265838332370761358328329658687644475392` (≈ 8.904256e-7, margin 4.4922), `c_site = 25373922426378073252109377257001885/28941653723943293146223880150916994444928` (≈ 8.767268e-7, margin 2.2812), and the same secondary pair. The reverse is self-contained apart from the admitted premises and standard theorems. Its values equal the forward's to about 1e-4.

### 4. R7, R8, R10, R3, and the reverse's partial reading of the AV1 reverse report

- **R7** (the region-form near term against `e^{|Y|/10^8}`, especially at `d_Y<=1`). Neither producer uses the family expansion that produced my `e^{(taubar+Kq^{d_Y})|Y|}`.
  - **Forward.** The derivative form charges `(1+t)^{|Y|-1}` in the near term and `N_Y=(1+t)^{2|Y|}` in the far term. Both are absorbed into `e^{|Y|/10^8}` for **every** `Y` and every `d_Y`, because `2t+t^2 ≈ 6.806e-9 < 10^-8` (exact check).
  - **Reverse.** `eta=0`, and there is no exponential factor at all.
  - **Resolved.**
- **R8.** The forward reports no frozen-form crude `c_site` and says why. The reverse's crude `c_site` is in the frozen form and fails. Both are retained, and my R8 is self-corrected (above).
- **R10** (c5 for F2 volumes other than centred cubes; the untruncated passage there). The AY1 gate itemizes H1–H5 for F2 on `Lambda_N`. Both producers read every item as local and apply it verbatim to every F2 volume containing `Lambda_N` (forward R4, reverse "honest gaps"):
  - H1: the on-site `h_x`;
  - H2: grouping at the anchor inside `(b+S)∩V`;
  - H3: `|X_b|<=4`;
  - H4: the per-site sum through `b in u-S`;
  - H5: cutoff compression.

  I checked H1–H5 in the AY1 forward report §3.1: none uses the cube shape. I accept the reading, recorded as a limitation (not a gated statement). It affects the F2 branch of c5 in both regimes. For F1, AM2 §6 already covers every finite complete-factor volume.
- **R3.** Both producers charge the site 0 at `q^N` through form (b), which gives the factor `1+q`. The R-only gate input (factor 2 at exponent `N-1`) would give ≈ 1.7533e-6. Check `R3_both_use_q_to_the_N_at_u_0`.
- **The reverse read only §§1–8 of the AV1 reverse report.** What the reverse uses from AV1 is:
  - the product-ordering split (AV1 F07, in the AV1 forward report, which it read in full; AV1 reverse §3);
  - the normalization trap (§4);
  - the exact first-order coefficient (F17; AV1 reverse §6);
  - cutoff-vector removal F20–F23 (AV1 forward; AV1 reverse §7).

  The AV1 reverse §§9–11 hold consequences and scaling, targets and checker, and limitations. The BB1 reverse uses nothing from them. The AV1 gate's limitations concern AQ1 subsequential limits, tier (i), sign-blindness and control counts, and none restricts the BB1 use. **Nothing used lies outside the parts read.** The forward's partial reads (BA1 reverse §§0–7 and the start of §8, AV1 forward §§1–9, AY1 forward §§1–3) are likewise sufficient: it re-proves the BA1 input at every site (Theorem 8.1) instead of citing it.

### 5. D1 and the wording defects, reconciled

**D1 was found by all three of us.** The semantics of `normalization_couples_supports` say a support strictly containing `R` has a nonzero first-order `R`-marginal. It does not.
- At first order only supports **contained in** `R` move `rho_R`: the 10 faces whose owner set is exactly `R`.
- All 72 straddling faces among the 82 meeting `R` vanish at first order, including the 6 that strictly contain `R` (forward; AY1 gate). A support strictly containing `R` differs at second order.
- All three fixtures exhibit the three kinds.
- The clause is mine, from the pre-freeze review.

| reading / defect | skeptic (pre) | forward | reverse | outcome |
|---|---|---|---|---|
| D1 normalization_couples_supports clause | D1 | D1 (6 of 72 strictly contain R) | D1 (supports contained in R; 10 faces) | agree; read as recorded |
| sites of the union volume outside `Lambda_N` | R5 | R1 (exponent `(N-|u|)_+=0`) | D3 (per-box circle bound at the real point) | agree |
| lemma form `kappa(I)<=kappa_0 w'^{-d} p(|I|)` and the `|Y|` factor | R2 | R3 (`kappa_0(Y)=N_Y|Y|kappa_0`, `p(s)=s`, site form used) | D4 (`kappa_0=beta*|Y|`, `p(n)=n`) | agree; assembly linear in `|Y|` in both |
| `omega_O` region | — | R2 (the marginal on O or any larger region) | Lemma 1.1 definition | agree |
| F2 non-centred volumes (AY1 locality) | R10 | R4 | honest-gap reading | limitation (item 4) |
| reverse split weight value | — | — | D2 (read as `W<=1/(37888|tau|)`; W=1024) | agree |
| secondary radius `|tau|/q_2=1/151552` at every tau | R9 | K_2 proved at rho=1/151552 | D5 | agree |
| fixture ownership (polymer fixture in the reverse, split fixtures in the forward) | R11 | exhibits split fixtures | D6 | agree |
| tier/route/input vocabulary mixed in `tier_names_allowed` | — | one tier, one route, one input per constant | D7 | agree; three separate labels |
| near-term `eta` | R1 (`eta=0` by the variance bound) | `eta_Y=(1+t)^{|Y|-1}-1` (derivative with product bound) | `eta=0` (Lemma 1.3) | both fit `2(1+eta)` |
| mixed-weight loss `w e^{4b}` | R12 | used throughout; e^{3b}, per-creation loss rejected | Lemma W3 (proved, unused; `w e^b` insufficient) | agree |
| crude region constant | R8 | not in frozen form | in frozen form (eta=0), fails | R8 self-corrected |
| u=0 exponent | R3 | q^N | q^N | agree |
| **new D2 (this review)**: plan rule P4 (committed excerpts) not carried into the BB1 contract for KP | — | cites KP, discloses non-inspection | route avoids KP | limitation, repair recorded (item 3) |
| **new D3 (this review)**: the reverse exports comparison names truncated to 80 characters | — | full names | 80-character prefixes | each prefix is unique; the review's validator matches by prefix |

### 6. Heredoc report writes and name exposures

**Forward (disclosed in its packet).** The agent file-writing tool refused a report file, so `report.md` was written with a shell heredoc. One `git status --short` and one `git log --oneline | head -5` displayed three untracked BB2 path names and five commit subjects (one naming the BB2 forward freeze). None was opened.
- **Assessment: harmless.** The bytes are bound by `freeze.json`, the replays are byte-identical, and `report_bound_to_results` passes.
- The names concern BB2, and BB2 carries no BB1 route content.
- The reverse BB1 packet did not exist yet: its first scratch file is dated 01:35:53Z, and the forward committed at 00:49:30Z.

**Reverse (not disclosed in its frozen packet).** The coordinator reports that the reverse disclosed a heredoc write and a name exposure in its hand-back. The frozen report and results record neither: the report's disclosure section covers inputs and scratch only. This is a **non-blocking finding**, and the gate should record the disclosure.
- The write method does not affect the content: the bytes are frozen, the replays are byte-identical, `report_pins_exact_values` passes, and the phrase scan is clean.
- On the names: if a `git log` run by the reverse after 00:49:30Z showed the forward commit subject (33e0ae6), it displayed the forward previews `C ~8.905e-7`, `c_site ~8.768e-7`. Those previews carry almost no information beyond the frozen input, because 99.98% of each is the near term `2K(1+q)`, which follows from `K` and form (b).
- The reverse's far-site mechanism (covering chains, `beta*`, `W=1024`) and its far term (8.73e-11 against the forward's 1.74e-10) differ from the forward's. Its value is not derived from the forward's.
- Independence rests on disclosure and content.

**The review's own exposure.** After a context compaction, I searched my session transcript to recover the exact text of this request, and printed only that message. Incidental prints showed Round32 AY1/AY2 coordinator messages and the start of an AV1 hand-back, all historical and gated. `git log`, run for the timeline and for the repair, displayed the subjects of later expert-assistant commits (d5709f2, modern: "... KP side-condition preview and self-containment finding ..."; bffcb6f, Jung audit; f411abb, historical assistant) and of the advisor's excerpt commit (cca0584). I opened none of the expert files. The KP decision above was formed from the forward report before that display.

## Review against the contract items (both producers)

- **Item 1** (decomposition, `Tr N_c >= 1`, two Lipschitz bounds).
  - Forward: Lemmas 2.1–2.4, with the outside-state constant `2(2eps+eps^2)` and the coefficient constant `2(1+t)^{|Y|-1}`.
  - Reverse: Lemmas 1.1–1.4, with `eta=0` and exact mixed-state fixtures.
  - Neither uses a global Lipschitz constant as a decay factor.
- **Item 2** (forward): the polymer representation (Proposition 3.3), activity bounds, exploration counts (brute-forced on a five-site chain), the mixed-weight lemma in full (§5), the KP condition with `a=taubar^2` (cited theorem; item 3), and the real-parameter derivative. No analyticity is claimed.
- **Item 3** (reverse): the iterated split with per-site charging. The multi-support straddling families are bounded explicitly through coverings (R09/R10).
- **Item 4.** Form (b) is proved in full in each packet. The headline and region bounds hold for every comparison and both signs, in each `Q_L`, and at fixed `N` for the untruncated vectors (AV1 F20–F23; AY1 for F2). The secondary pair and the crude tier are reported separately.
- **Item 5.** The fixtures are labelled `model_is_finite_graph: true`, `transfers_to_aq: false`. The template appears once, as one unbroken span, in each report. The phrase scans are clean: `tools/phrase_scan.py` exits 0 on both reports, and my mirror agrees. The gate fields are exported exactly.
- **Item 6.** The τ ratios are within their brackets. All 37 controls are damaging mutations in each checker:
  - forward: 51 checks and 107 rejected mutations;
  - reverse: 78 checks and 132 rejected mutations.

## Replays, closures and isolation (`bb1-replays.json`)

- **Replays.** All four producer replays (forward/reverse × normal/`-O`, fresh external directories) reproduce `output/` byte for byte:
  - forward: `results.json` `98844257…78905`, manifest `26e88dbb…f7200`;
  - reverse: `results.json` `18532681…81e976`, manifest `5ac88add…378b1`.
- **Closures.** `tools/freeze.py verify` reports verified for both. Each closure has 39 files: `check.py`, `report.md`, 35 inputs and 2 outputs. The freeze records are `90ddc178…30e1d` (forward) and `0e9c41d8…26b3` (reverse). Each `check.py` records its own sha256 before evaluation, and the recorded hashes equal the frozen files.
- **Inventories.** Both are identical and equal `AGENTS.md` + `contracts/bb1.json` + the 33 shared premises. Every snapshot is byte-identical to its repository source.
- **Reverse isolation.** The only skeptic files are the declared gated reviews (Round29 `am2.md`, Round33 `ba1.md`, `ba2.md`). The only Round33 forward files are the gated BA1/BA2 reports. There is no BB1/BB2 producer, triage, experts, deliberation, plan, brief, panel or findings file.
- **Pre-comparison package.** Unchanged since its freeze (record `5ed6a971…2f3e`, results `2ab53449…129f`). It replays byte for byte under normal and `-O`.
- **Timeline** (UTC, 2026-09-25 unless stated):

  | time | event |
  |---|---|
  | 09-24 23:38:22 | contract frozen (45a87be) |
  | 00:26:36 | my `bb1_check.py` last written |
  | 00:28:59 | my pre-comparison commit (09d0bdb) |
  | 00:44:12 / 00:47:48 | forward `check.py` / `report.md` last written |
  | 00:49:30 | forward commit (33e0ae6) |
  | 01:35:53 | reverse scratch starts |
  | 01:59:56 / 02:05:15 | reverse `check.py` / `report.md` last written |
  | 02:06:29 | reverse commit (13ac349) |

  I read neither producer before the reverse commit.
- **Scratch audit** (names and mtimes only). The producers' private folders match their disclosures.

## Mutation harness

The review's source edits run on temporary copies (`<tmp>/repo/<producer path>`, holding `check.py`, `report.md` and `inputs/`). Each runs with `-B`, and also `-O` in the optimized run. The harness asserts that no interpreter cache is written.
- **Validator weakenings (74).** Each run must abort with `damaging mutation accepted: <label>`, where the label is a recorded mutation of the same control.
  - **The anchors were found empirically.** Every `require(` site in both checkers was weakened in turn (336 runs), and the sites whose weakening lets a mutation of the intended control through were retained.
  - **Two-site anchors.** Where two validators guard a mutation, both are weakened:
    - forward: cutoff-vector removal (the gap `require` and the Eckart `require`), reverse isolation (inventory equality and the forbidden-file rule), and the whole-sequence and common-limit pair;
    - reverse: the global-overlap route, the Lipschitz provenance pair, and the metric declaration pair.
  - **Exact arithmetic** (both producers): the float/bool branch returns `Fraction(value)` instead of raising.
  - **Negation-aware scans** (forward `negation_aware_phrase_scan`; reverse `named_construction_not_uniqueness`, whose phrase scan is shared with an earlier control): the non-negation word "gives" is added to the negation lexicon.
  - **Reverse premise isolation:** the forbidden-prefix rule is neutralized and inventory equality is relaxed to inclusion, so `snapshot_removed` (another control) is still rejected and `forward_bb1_added` is reached.
- **Input edits (6).** Each aborts without output:
  - a contract byte edit without rehash (both producers);
  - an undeclared skeptic triage in `inputs/` (both);
  - the forward BB1 report in the reverse inputs;
  - a BB2 reverse report in the forward inputs.
- **Damaged packets (15).**
  - Forward (7):
    - the headline `C` halved;
    - the `-` region `c_site` doubled;
    - the crude tier marked met;
    - the KP `a` halved;
    - the c3 secondary `c_site` replaced by the reverse value;
    - the `q_2` ratio set to 99;
    - the template trimmed.
  - Reverse (8):
    - the c3 `-` untruncated flag set false;
    - the c5 rows dropped;
    - `C` replaced by my prediction;
    - the secondary `c_site` scaled;
    - the crude `c_site` changed;
    - `eta` set nonzero;
    - the `C` ratio set to 100;
    - the template trimmed.

## Blocking issues

None.

## Non-blocking findings

- **N1. The KP citation** (item 3). This is a limitation plus contract defect D2. Repair applied: the advisor committed the Ueltschi excerpt (cca0584), and `bb1-kp-repair.md` finds the cited statement and its use covered, with no missing factor.
- **N2. The reverse packet omits its tooling and name-exposure disclosure** (item 6). The gate should record the hand-back disclosure.
- **N3. Isolation rests on disclosure and content, not on timing.** My package was committed 15 min before the forward last wrote `check.py` and about 1.5 h before the reverse. Both producers disclose not reading `skeptic/` beyond the declared BA1/BA2 reviews. The content agrees:
  - the forward's weights (`w=192`, `v=128`, `e^b=1001/1000`) and Y-cluster normalization differ from my KP-feasibility weights (`a=1/1000`, `W=1024`, `e^b=9/8`) and from my recursion;
  - the reverse's `W=1024` coincides with the `W` of my feasibility check (a power of two with `lambda/q = 1/8`), but its covering-chain closure is its own.
- **N4. The forward pays the far cost twice.** Straddling plus normalization is ≈ 1.74e-10, against the reverse's ≈ 8.73e-11. It is valid, and it is why the forward headline is the larger and is bound.
- **N5. Reverse comparison names are truncated to 80 characters** in `results.json` (D3). They are unambiguous as prefixes.
- **N6. Convention reads outside `inputs/`** (tools README, `freeze.py`, `phrase_scan.py`; `forward/ba1/check.py` or `reverse/ba1/check.py`) carry no premise weight. This matches Round32/BA1 practice.
- **N7. Self-correction R8** (above).

## Which constants the gate binds

The rule: for each quantity, bind the larger valid constant and label the other route's value.
- **Headline R form:** `C` = the polymer_kp value ≈ 8.905120e-7 (exact above), margin 4.4918.
- **Region form:** `c_site` = the polymer_kp value ≈ 8.768118e-7, margin 2.2810.
- **Labelled secondary pair** (`q_2=151552|tau|`): `C_2` ≈ 9.689093e-6 and `c_site,2` ≈ 9.674431e-6, both iterated_split.
- **Other route, labelled:**
  - iterated_split `C` ≈ 8.904256e-7 and `c_site` ≈ 8.767268e-7;
  - polymer_kp `C_2` ≈ 9.644014e-6 and `c_site,2` ≈ 9.629421e-6.
- **Crude tier, reported only:**
  - `C` ≈ 2.0529e-3 (polymer_kp) and 1.8006e-3 (iterated_split);
  - `c_site` ≈ 1.7729e-3 (iterated_split; the polymer_kp crude value is outside the frozen form).
- **τ ratios of the bound constants:**
  - `C` ≈ 100.64788 and `c_site` ≈ 100.64788, in [95,105];
  - `C_2` ≈ 1.0015003 and `c_site,2` ≈ 1.0000000001, in [99/100,101/100];
  - `q_2`: exactly 100.

`bb1.json` → `admitted_values` lists these per comparison (c1–c5), per form (R, region), per cutoff regime (each `Q_L` uniform in `L`; untruncated at fixed `N`) and per sign. Each entry carries the bound value, the other route's value and the labelled secondary pair. These are the entries from which the BB2 review discharges its hypotheses: `C<=1/250000` and `c_site<=1/500000` hold for every comparison, both regimes and both signs.

## Limitations

1. **Scope.** Only the zero-selected patterned family (triple (0,0,0), Haar reference) is covered, with:
   - fixed spacing and `|tau|<=10^-8`;
   - F1 and F2 on centered cubes, with `N>=2`;
   - one-prescription complete-factor volumes containing `Lambda_N`;
   - the cover `R` and regions inside `Lambda_N`.

   Nothing transfers to other boundary conditions, nonzero triples, literal vertex boxes, weak coupling or the continuum. The constants are uniform in N at fixed spacing and in the cutoff, never in the lattice spacing.
2. **Static only.** No dynamics, no limit object, no whole-sequence convergence or common limit (BB2), no translation statement, and no uniqueness of any ground state. No analyticity of the reduced density is claimed, and no zero-free region is proved.
3. **The polymer_kp route's KP step was checked post hoc against a committed source.** The frozen packet cites the theorem without an excerpt. The citation was checked against the Ueltschi excerpt committed after the freeze and is covered (item 3, `bb1-kp-repair.md`). The excerpt is not a premise of the packet, and the original Kotecký–Preiss paper is neither committed nor needed. Every bound value is at least the self-contained iterated_split value.
4. **F2 volumes other than centred cubes** rest on a reviewed local reading of AY1 H1–H5, not on a gated statement.
5. **Inherited without re-proof:**
   - the AM2 majorant, fixed point, uniqueness in the ball, and §6;
   - the AV1 split, the first-order coefficient and F20–F23;
   - the AY1 itemization;
   - the I1 dictionary.

   Banach, Weierstrass and the maximum principle are standard and not machine-checked. The every-site input and `K_2` are BB1 lemmas proved in both packets.
6. **Upper bounds only.** The `-tau` rows replay the same `|tau|` formula. The constant is governed by the BA1 input: the near term is 99.98% of `C`. The region margin (2.28) is the binding one.
7. **Contract wording read as reconciled above**, including D1.
8. **Independence is limited to derivations, constants and code:**
   - the contract and selection note name both mechanisms;
   - my triage and pre-freeze review shaped the parameters;
   - all agents are correlated model agents;
   - isolation is verified for repository inputs only;
   - the reverse packet omits its tooling and name disclosure.
9. **Scientific priority is unverified.**

## Advice (planning only)

- **Carry the excerpt rule into every contract.** The Ueltschi excerpt is now committed (cca0584). Any later contract that names an external theorem should list its committed excerpt among the shared premises before production, so that the producer quotes it instead of transcribing from memory.
- **The headline is set by the input.** The constant is governed by `2K(1+q)`. A later loop that needs more room should improve the coefficient input: the sharp exponent, or a larger disc radius at the same `q`. Sharpening the density lemma will not help.
- **The BB2 review.** It should discharge its hypotheses from `admitted_values` exactly as listed: per comparison, per regime, per sign, with the F2 non-centred reading (R10) carried along for c5.
