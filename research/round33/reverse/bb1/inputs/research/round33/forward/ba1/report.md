# Hruday boundary decay of the AM2 creation coefficients — BA1 forward (diameter-weighted anchored norm)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production (a Claude model agent) under the frozen BA1 contract (`research/round33/contracts/ba1.json`, sha256 `2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9`). It is correlated model-agent work: not independent human review and not formal verification.

**What this producer read.**
- The contract snapshot first (its sha256 was checked before anything else), then only files under `inputs/`:
  - **read in full:** `AGENTS.md`; `selection-ba1.md`; the AM2 forward and reverse reports and `skeptic/am2.md`; the AM2 and AQ1 gates; the AQ1, AQ2 and I1 forward reports; the AV1 and AY1 forward reports; the AV1, AW1, AY1 and AY2 gates (every field except the `bindings` blocks, which were not printed); the Round32 lessons file; the paired-physics SKILL and its complete-residual reference; the Newton, Tesla and historical-panel SKILL files;
  - **read in part:** the AV1 reverse report and the AW1 forward report (headings; AW1 §§5.1–5.2), the AY1 reverse report (headings and §§1.1–1.5), the AY2 forward report (headings and a keyword search, which found the obligations rows O2, O4 and O5).
- **Outside `inputs/`, for protocol and conventions only:** `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py` (its round phrase list is copied into `check.py`), and `research/round32/forward/ay1/check.py` and `report.md` (checker and report conventions). None of these carries premise weight.
- **Not opened or listed:** `research/round33/reverse/`, `research/round33/skeptic/`, `research/round33/experts/`, `research/round33/advisor/` (other than the snapshot of `selection-ba1.md`), and every other agent's scratch folder.
- **Scratchpad disclosure.** My scratch work is in `/tmp/claude-0/ba1-forward-private/`. I created it directly with `mkdir -p` and did not list `/tmp/claude-0/` or the shared scratchpad root, so I saw no other agent's folder names. It holds an enumeration prototype, an exact-constant preview script, a harness that imports `check.py` with bytecode writing disabled, and development runs. **None of it is evidence.** I opened no file in any other agent's scratch folder. The Claude harness saved copies of two of my own long reads (the AV1 forward report and the AW1/AY1/AY2 gates) to its tool-results cache; those are my own reads.
- **Tooling note.** The agent file-writing tool refused to create this `.md` file with a generic rule against summary files. Because this report is a required protocol artifact that `check.py`, `phrase_scan.py` and `freeze.py` read, it was written with a shell heredoc instead. The content is unaffected.

**Attribution.** Exponentially weighted norms that pay a fixed loss per interaction are standard tools of convergent cluster and locality expansions; commuting nilpotent creation expansions are established mathematics (AM2 names its templates). This loop applies them to the admitted AM2 fixed point of the named families. No primary-source comparison was made here, so scientific priority is unverified. HNM labels are project aliases.

## Verdict (forward route)

Model: **`AQ_patterned_zero_selected`**, the AM2/AQ1 zero-selected patterned family, at both signs of `tau` with `|tau| ≤ 10^-8`. The two named construction families are F1 (AQ1 centered whole-star boxes `Lambda_N=[-N,N]^3`) and F2 (I1 §6 all-contained-face boxes with padding on the same `Lambda_N`), `N ≥ 2`, and the cover is `R={0,e_z}`.

1. **Item 1.** The AM2 multilinear estimate survives in the diameter-weighted anchored norm `||c||_w = max_u sum_{I∋u} w^{diam(I)} ||c_I||` (coarse l-infinity diameter). The loss is `w^{d_X} = w`, charged once per interaction term and never per creation: `||L_k(c_1..c_k)||_w ≤ w J L_k^num prod ||c_j||_w` (F03). The weighted self-map `J_0 w G(R) ≤ R` and the Lipschitz factor `Γ = J_0 w G'(R) ≤ 77/296` hold for every `w` in `[1, 390625/148]`. The weighted fixed point is AM2's fixed point.
2. **Item 2.** Order versus distance: a coefficient on a support meeting `R` depends on an interaction term at coarse distance `d` from `R` only at order at least `1 + ceil(d/diam)`, hence at least `ceil(d/diam)` (F08). The diameter convention is verified by enumeration: every star has l-infinity diameter 1 and l1 diameter 2. The proof uses l-infinity (`d_X = 1`). Tables for both conventions on `Lambda_2`, `Lambda_3`, `Lambda_4` are in §4.
3. **Item 3.** The boundary sources are the new terms only. For the nested comparisons they are the new whole stars (F1) or the new faces (F2), each meeting the shell `Lambda_{N+1} \ Lambda_N`, at l-infinity distance `N` from `e_z`. For F1 versus F2 they are the `28N(5N+1)` extra faces, charged face by face once; they lie in the outer layer, at distance `N-1` from `e_z`.
4. **Item 4.** For `u` in `R` and every comparison, `sum_{I∋u} ||c_I^{box1} - c_I^{box2}|| ≤ K q^(N-1)` in each on-site cutoff space `Q_L`, with `K` independent of `L`, at both signs:

| pair | tier / route | `q` | proved `K` (largest comparison) | preview | frozen target | margin |
|---|---|---|---|---|---|---|
| headline | exact_first_order / weighted_norm | `1/64` | `2734375/12204185915601` | `2.24052224286e-7` | `1/2000000` | about 2.23 |
| floor | exact_first_order / weighted_norm | `148/390625` | `708203125/43148545682688` | `1.64131400907e-5` | `1/12` | about 5077 |
| floor | crude_majorant / weighted_norm | `148/390625` | `14453125/684115704` | `2.11267259551e-2` | `1/12` | about 3.94 |
| crude, reported | crude_majorant / weighted_norm | `1/64` | `9472/24454143` | `3.87337229523e-4` | not a target | fails `1/2000000` |

   The global Lipschitz constant is never used as a decay factor. Decay comes only from the boundary-distance weight `e^{beta rho_B(I)}`.
5. **Item 5.** Coefficient decay is **not** decay of the reduced density on `R` (§9 has a fixture). The mandatory sentence and the gate fields are in §9.
6. **Item 6.** The `tau → tau/100` ratios lie in their brackets: headline `101.26`, floor `1.000375`, `q_min` exactly `100`. The traps have exact fixtures, and each of the 37 contract controls rejects at least one damaging mutation (§§10, 12).

**Proposed forward verdict: `accepted_within_scope` for the forward half**, with sub-labels `boundary_decay_rate_only` and `static_not_dynamic`. The contract's acceptance also requires the reverse (analytic-disc) route and skeptical review, which are outside this producer's work.

## 1. Model, families, metric and weights (item 1, naming)

**Model.** SU(2) in Kogut–Susskind form on `Z^3` at fixed spacing. Coarse factor `b` owns the 24 positive links with tails `(4b_x+r, 2b_y+s, b_z)`, `r=0..3`, `s=0,1`. The selected triple is exactly `(0,0,0)`, so in normalized units `delta=alpha/8` the on-site operator is `h_b = 8 sum_{e∈b} C_e ≥ 6Q_b ≥ Q_b`, with Haar vacuum `P_b`. Each anchor carries 21 omitted faces, and `phi_b = -(tau/3) sum_{f∈O_b} W_f`, `||phi_b|| = 7|tau|`, `S = {0,e_x,e_y,e_z}` (I1.5; AV1 F01–F02).

**The two families** (contract `model`):

- F1: `H^(1)_N = sum_{b∈Lambda_N} h_b + sum_{b+S⊂Lambda_N} phi_b`.
- F2: `H^(2)_N = sum_{b∈Lambda_N} h_b + sum_{b∈Lambda_N} phi_b^(Lambda_N)`, where `phi_b^(B) = -(tau/3) sum_{f∈O_b, M_f⊂B} W_f`.

The F2 padding sites carry no interaction, so the padded fixed point is supported in `Lambda_N` and coefficients on supports meeting the padding vanish (AY1 gate; AY1 reverse §1.3(h)). I therefore work on `Lambda_N` directly. Each F2 term acts on its actual support `X_b = union of retained M_f`, which lies in `(b+S) ∩ Lambda_N` (AY1 forward H2–H4).

**AM2 objects** (AM2 §§2–3; AV1 F03–F05). In each on-site cutoff space `Q_L = ⊗_x 1_[0,L](h_x)`:
- a creation vector is `c_I ∈ ⊗_{x∈I} Q_x Q_L H_x`, with `ĉ_I = |c_I⟩⟨Omega_I| ⊗ 1` and `C = sum_I ĉ_I`;
- the fixed point satisfies `c = Phi_Lambda(c) = sum_{k=0}^{8} L_k(c,…,c)/k!`, where `(L_k)_M = H_M^{-1} P_M ad_{C_1}…ad_{C_k}(V) Omega_0`;
- the constants are `J ≤ 28|tau| ≤ J_0 = 7/25000000`, `R = 1/64`, `G(t) = 16e^{8t}(1+10t)`, `G(R) ≤ 148/7`, `G'(R) ≤ 352`;
- AM2 gives the unique fixed point in the anchored ball `||c||_a ≤ R`.

The space of `c_I` depends only on `I` (and `L`), not on the box. So a box-1 collection embeds in box 2 by zero extension `ι`.

**Metric.** The metric is the coarse l-infinity distance `d(p,p') = max_i |p_i - p'_i|` on factor sites. Diameters are `diam(I) = max_{p,p'∈I} d(p,p')`, and `d_X = diam(X)` for an interaction support. Every star has `d_X = 1`; the l1 reading (`d_X = 2`) is a labelled alternative and is never mixed with it (§4). Conversion, if ever needed: `d_inf ≤ d_1 ≤ 3 d_inf`.

**Weights** (contract `parameters.weights`):

\[
\|c\|_w=\max_u\sum_{I\ni u}w^{\operatorname{diam}(I)}\|c_I\|,\qquad 1\le w\le w_{\max}=\tfrac{390625}{148},\qquad \text{headline } w=e^{\mu}=64,
\tag{HNM-BA1-F01}
\]
\[
\|\delta\|_{B,\beta}=\max_u\sum_{I\ni u}e^{\beta\rho_B(I)}\|\delta_I\|,\qquad \rho_B(I)=\max_{p\in I}d(p,B),\qquad 1\le e^{\beta}\le w .
\tag{HNM-BA1-F02}
\]

- `B` is the source set of the comparison (§5).
- The difference weight grows with distance from `B`, that is, towards `R`.
- The headline uses `e^beta = w = 64`. The floor pair uses `e^beta = w = 390625/148` (`beta = mu`, allowed by `beta ≤ mu`; wording note W2).
- The loss `w^{d_X} = w` is charged once per interaction term.
- The star-count weight `w^{n(I)}` and the cardinality weight `e^{mu|I|}` are labelled alternatives. Neither is used or mixed in.

## 2. The weighted multilinear estimate (item 1)

**Lemma (HNM-BA1-F03).** For collections `c_1,…,c_k` in one box with interaction `V = sum_X V_X`, `|X| ≤ p = 4`, `d_X ≤ 1`, and per-site sum `J = max_u sum_{X∋u} ||V_X||`:

\[
\|L_k(c_1,\ldots,c_k)\|_w\le w\,J\,L_k^{\rm num}\prod_j\|c_j\|_w,\qquad L_k^{\rm num}=16\cdot8^k(1+5k/4).
\]

**Mixed form (HNM-BA1-F04).** If slot `j*` holds a collection `δ` measured in `||·||_{B,beta}` and `e^beta ≤ w`, then `||L_k(c_1,…,δ,…,c_k)||_{B,beta} ≤ e^beta J L_k^num ||δ||_{B,beta} prod_{j≠j*} ||c_j||_w`.

**Source form (HNM-BA1-F05).** If `V` is replaced by `V_new`, each of whose terms meets `B`, then `||L_k^new(c_1,…,c_k)||_{B,beta} ≤ J_new^(B) L_k^num prod_j ||c_j||_w`. Here `J_new^(B) = max_u sum_{X new ∋ u} e^{beta rho_B(X)} ||V_X|| ≤ e^beta J_new`.

*Proof, itemized (not by analogy).* Fix an interaction term `V_X` and one creation support `I_j` per slot.

- **(a) Support localization** (AM2 §2, unchanged).
  - Every `I_j` meets `X`: a disjoint creation commutes innermost and kills the word. The fixture in §10 computes this word as exactly zero.
  - With `𝒩 = union_j I_j`, a nonzero term has output `M` with `𝒩 \ X ⊂ M ⊂ 𝒩 ∪ X`. There are at most `2^p = 16` output sets for given data, and `|I_j| ≤ |M| + p`.
  - The commutator has `2^k` products, each of norm at most `||V_X|| prod_j ||c_{j,I_j}||`.
- **(b) Diameter through the interaction** (new). `diam(M) ≤ d_X + sum_j diam(I_j)`. Take `p, p'` in `M`, which lies in `X ∪ 𝒩`, and choose `x_a` in `I_a ∩ X`, which is nonempty by (a):
  - `p, p'` both in `X`: `d ≤ d_X`;
  - `p` in `I_a`, `p'` in `X`: `d ≤ diam I_a + d_X`;
  - `p` in `I_a`, `p'` in `I_b`, `a ≠ b`: `d ≤ diam I_a + d_X + diam I_b`;
  - `a = b`: `d ≤ diam I_a`.

  The sum cannot be replaced by a maximum. The fixture of §10 has `M = 𝒩 \ X` disconnected, with `diam M = 3 = 1 + 1 + 1`, while `d_X + max = 2`. For `w ≥ 1` this gives `w^{diam M} ≤ w^{d_X} prod_j w^{diam I_j}`.
- **(b′) One-point versions.**
  - For the δ-slot, `rho_B(M) ≤ rho_B(I_{j*}) + d_X + sum_{j≠j*} diam I_j`: route every point through `y` in `I_{j*} ∩ X`.
  - For a source term `X` meeting `B`, `rho_B(M) ≤ rho_B(X) + max_j diam I_j ≤ rho_B(X) + sum_j diam I_j`, and `rho_B(X) ≤ d_X` (pick `y` in `X ∩ B`).

  A maximum is valid here because `rho_B` is a one-point quantity. It is not valid for diameters.
- **(c) Root in `X`.** `||H_M^{-1}|| ≤ 1`. Summing `X ∋ u` gives `sum_{X∋u} w^{d_X} ||V_X|| ≤ wJ`. Each collection is summed over supports meeting `X`: `sum_{I∩X≠∅} w^{diam I} ||c_I|| ≤ p ||c||_w`. The contribution is `2^p · 2^k · p^k · wJ = 16·8^k wJ`.
- **(d) Root in a creation `I_l`** (all `k` choices overcounted).
  - `1/|M| ≤ (p+1)/|I_l|`.
  - `sum_{X∩I_l≠∅} w^{d_X} ||V_X|| ≤ wJ|I_l|`, which cancels the denominator.
  - The other collections cost `p^{k-1}`, and `sum_{I_l∋u} w^{diam I_l} ||c_{l,I_l}|| ≤ ||c_l||_w`.

  The contribution is `2^p 2^k k (p+1) p^{k-1} wJ = 16·8^k (5k/4) wJ`.
- **(e) Total.** `wJ·16·8^k(1+5k/4)`. The loss `w^{d_X} ≤ w` enters once per term of `V` in (c)–(d), independent of `k` and of the number of creations. `check.py` verifies that the root-in-`X` and root-in-creation contributions add to `L_k^num` and equal `k!` times the Taylor coefficients of `G` for `k = 0..8`.
- **(f) Mixed and source forms.** (b′) replaces (b), `e^beta ≤ w` turns every creation weight `e^{beta diam}` into `w^{diam}`, and the δ-slot sums use `||δ||_{B,beta}` in (c)–(d). For a source term the loss is `e^{beta rho_B(X)} ≤ e^beta`.

Every sum is finite and dimension-free, so the lemma holds in each `Q_L`. Repeated terms and repeated histories are counted, never cancelled.

## 3. Weighted self-map, Lipschitz inequality and the two tiers (item 1)

Summing (F03) over `k` gives `||Phi(c)||_w ≤ J w G(||c||_w)`. Telescoping each `k`-linear term, with all `k` replacements counted, gives

\[
\|\Phi(c)-\Phi(c')\|_w\le \Gamma\,\|c-c'\|_w,\qquad \Gamma:=J\,w\,G'(R)\le 352\,J\,w\qquad(\|c\|_w,\|c'\|_w\le R).
\tag{HNM-BA1-F06}
\]

The inequalities are re-evaluated as exact rationals at the declared weights. The unweighted AM2 constants are never cited for the weighted ball.
- **Self-map.** `J_0 w G(R) ≤ J_0 w·148/7 ≤ R` if and only if `w ≤ w_max = R/(J_0·148/7) = 390625/148`.
  - At `w = 64` the value is `148/390625`, below `1/64`.
  - At `w_max` the bound equals `1/64` exactly. The true `G(R)` is strictly smaller: the series enclosure `e^{1/8} ≤ 53823253862885575661009/47498854821020880076800` gives `G(R) ≤ 20.9632…`.
- **Lipschitz.**
  - At `w = 64`: `Γ = 2464/390625` (about `6.30784e-3`).
  - At `w_max`: `Γ = 77/296` (about `0.260135`).
  - `Γ` is below 1 for every `w ≤ w_max`.
- **Identification.** For `w ≥ 1`, `||c||_a ≤ ||c||_w`, so the weighted ball `B_w(R)` lies inside AM2's ball `B_a(R)`. Banach's theorem gives a fixed point in `B_w(R)`. By AM2's uniqueness in `B_a(R)`, it is the AM2 fixed point. Hence `||c||_w ≤ R` for every `w` in `[1, w_max]`, both families, every box, every `Q_L` and both signs.

**Tiers** (closed vocabulary; route `weighted_norm` throughout):

- **crude_majorant.** `t_w := ||c||_w ≤ J w G(t_w) ≤ J w G(R) =: T^c_w`. This is `148/390625` at `w = 64` and `1/64` at `w_max`.
- **exact_first_order.** `c^(1) = L_0 = H^{-1} P V Omega_0 = -(tau/72) sum_f W_f Omega_0`, sorted by owner set (AV1 F15; AW1 gate). Every omitted owner set has l-infinity diameter exactly 1 (enumerated for all 21 classes). Hence `||c^(1)||_w = w ||c^(1)||_a ≤ w t_1`, with `t_1 = 49|tau|/144`. By (F03), convexity of `G` and `t_w ≤ R`, `||c - c^(1)||_w ≤ J w (G(t_w) - 16) ≤ Γ t_w`. So

\[
t_w\le w\,t_1+\Gamma\,t_w\quad\Longrightarrow\quad t_w\le T_w:=\frac{w\,t_1}{1-J\,w\,G'(R)},
\tag{HNM-BA1-F07}
\]

  which is the contract's self-consistent inequality, re-derived in the weighted norm. At the cap, `T_w = 49/223580736` (about `2.19160205287e-7`) at `w = 64`, and `49/4036608` (about `1.21389047437e-5`) at `w_max`.

An exact first-order source combined with the crude `t_w` would be labelled `crude_majorant`. `check.py` enforces this and rejects every mislabel.

## 4. The order-versus-distance lemma (item 2)

**Tree expansion.** For `H_0 + sV`, `|s| ≤ 1`, the fixed point solves `c = s Phi(c)`. The derivative `I - s DPhi(c)` is invertible because `||DPhi|| ≤ Γ`, which is below 1, so `c(s)` is real-analytic. Its Taylor coefficients satisfy

`c^[1] = L_0`, and `c^[n] = sum_{k≥1} (1/k!) sum_{n_1+…+n_k=n-1} L_k(c^[n_1],…,c^[n_k])`.

Each summand is multilinear in `n` interaction terms `V_{X_1},…,V_{X_n}`, arranged as a labelled tree. By induction on `n`, using (a):
- (i) every output support lies in `X_1 ∪ … ∪ X_n`;
- (ii) the family `{X_i}` is overlap-connected. Each `I_j` meets `X` and lies in the union of its subtree, so some subtree term meets `X`.

**Lemma (HNM-BA1-F08).** Let `I` meet `R`, and let a term `X_far` with `d(X_far, R) = d` occur in a tree that contributes to `c_I^[n]`. Then

\[
n\;\ge\;1+\Big\lceil \frac{d}{\delta_{\max}}\Big\rceil\;\ge\;\Big\lceil\frac{d}{\delta_{\max}}\Big\rceil,\qquad \delta_{\max}=\max d_X\ (=1\text{ in }\ell_\infty,\ 2\text{ in }\ell_1).
\]

*Proof.* Pick `p` in `I ∩ R`, which lies in the tree's union by (i). By (ii) there is a chain `X_{a_1} ∋ p, …, X_{a_m} = X_far` of consecutively intersecting terms. Stepping through the intersections gives `d ≤ d(p, X_far) ≤ sum_{j=1..m-1} diam X_{a_j} ≤ (m-1) δ_max`, and `n ≥ m`. ∎

Two interactions that differ only in terms at distance at least `d` from `R` therefore give coefficients on supports meeting `R` with equal Taylor coefficients through order `ceil(d/diam)` in `s`, equivalently in `tau`. **The proof uses the coarse l-infinity convention, with diameter 1.** The weighted norm of §§2–3 is the quantitative form of this lemma: the loss `w` per term converts each link of the chain into one factor `q = 1/w`.

**All-size argument and enumeration.**
- **All sizes.** `S - S ⊂ {0, ±e_i, ±(e_i - e_j)}`, whose l-infinity norms are at most 1 and l1 norms at most 2. So every star and every sub-support has l-infinity diameter at most 1 and l1 diameter at most 2, with both attained by whole stars. Also `u ∈ b+S` if and only if `b ∈ u-S`, so each site lies in at most four terms, incoming anchors included.
- **Enumeration on `Lambda_2` and `Lambda_3`** (`diameter_convention_and_order_versus_distance`):
  - every F1 term is a whole star with diameters 1 (l-infinity) and 2 (l1);
  - every owner set has l-infinity diameter 1 and l1 diameter 1 or 2;
  - every F2 term has l-infinity diameter at most 1;
  - at most four terms meet any site;
  - the bulk count of 49 faces per site is attained.

**Tables.** Each cell is "number of terms at distance `d` from `R` / least tree order". The least tree order is the least number of terms in an overlap-connected chain from a term meeting `R`, computed by breadth-first search over the actual terms of the box. The second column is the lemma's bound `1 + ceil(d/diam)`. `check.py` verifies that every cell is at least the bound. In l-infinity the bound is attained for every `d ≤ N-1`, along the chains of stars anchored at `(0,0,k)`.

Coarse l-infinity convention (`diam = 1`, used in the proof):

| d | 1+⌈d/1⌉ | F1 Λ_2 | F1 Λ_3 | F1 Λ_4 | F2 Λ_2 | F2 Λ_3 | F2 Λ_4 |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 7/1 | 7/1 | 7/1 | 7/1 | 7/1 | 7/1 |
| 1 | 2 | 47/2 | 62/2 | 62/2 | 62/2 | 62/2 | 62/2 |
| 2 | 3 | 10/4 | 131/3 | 166/3 | 55/3 | 166/3 | 166/3 |
| 3 | 4 | - | 16/6 | 255/4 | - | 107/4 | 318/4 |
| 4 | 5 | - | - | 22/8 | - | - | 175/5 |

Coarse l1 convention (`diam = 2`, labelled alternative, not used in the proof):

| d | 1+⌈d/2⌉ | F1 Λ_2 | F1 Λ_3 | F1 Λ_4 | F2 Λ_2 | F2 Λ_3 | F2 Λ_4 |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 7/1 | 7/1 | 7/1 | 7/1 | 7/1 | 7/1 |
| 1 | 2 | 19/2 | 22/2 | 22/2 | 22/2 | 22/2 | 22/2 |
| 2 | 2 | 20/2 | 42/2 | 45/2 | 37/2 | 45/2 | 45/2 |
| 3 | 3 | 12/3 | 51/3 | 73/3 | 35/3 | 68/3 | 76/3 |
| 4 | 3 | 5/4 | 45/3 | 90/3 | 19/3 | 74/3 | 107/3 |
| 5 | 4 | 1/6 | 29/4 | 92/4 | 4/4 | 64/4 | 121/4 |
| 6 | 4 | - | 14/5 | 78/4 | - | 40/4 | 119/4 |
| 7 | 5 | - | 5/6 | 54/5 | - | 18/5 | 101/5 |
| 8 | 5 | - | 1/9 | 31/6 | - | 4/6 | 69/5 |
| 9 | 6 | - | - | 14/7 | - | - | 39/6 |
| 10 | 6 | - | - | 5/8 | - | - | 18/7 |
| 11 | 7 | - | - | 1/12 | - | - | 4/8 |

The seven terms at distance 0 are the seven incident anchors `R - S = {0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y}`, all retained for `N ≥ 2` in both families.

**Why the convention matters.** In l1 each star costs `w^2`, so the self-map needs `w^2 ≤ 390625/148`. That gives `w ≤ 51.3746…`, a rate `q_1 ≥ sqrt(148/390625) ≈ 1.94648e-2` per l1 step. So `q = 1/64` does **not** close in l1: the self-map fails at `w = 64`. The verified l-infinity diameter 1 is what carries the headline rate. The distances that matter are the same in both conventions (§5), so the l1 route gives only the slower rate.

## 5. Boundary sources and exact distances (item 3)

In every comparison, box 1's interaction is contained in box 2's: `V_2 = ιV_1 + V_new`. The source set `B` is chosen so that **every new term meets `B`**, and the source consists of new terms only. All counts below are enumerated at `N = 2, 3, 4`, and the formulas are all-size.

| comparison | new terms (charged once) | count at N=2,3,4 | source set `B` | `rho_B` max | new faces per site (max) |
|---|---|---|---|---|---|
| F1 `Lambda_N` vs `Lambda_{N+1}` | whole stars `b+S ⊂ Lambda_{N+1}`, not inside `Lambda_N`: `(2N+2)^3-(2N)^3` | 152, 296, 488 stars | shell `Lambda_{N+1} \ Lambda_N` | 1 | 49 |
| F2 `Lambda_N` vs `Lambda_{N+1}` | faces with `M_f ⊂ Lambda_{N+1}`, `M_f ⊄ Lambda_N` | 3920, 7224, 11536 faces | shell | 1 | 45 |
| F1 vs F2 on `Lambda_N` | the extra faces kept by F2, `28N(5N+1)` | 616, 1344, 2352 faces | outer layer `max_i|b_i| = N` | 0 | 38 |

**Per-comparison details.**
- **F2 regrouping.** The F2 groups that gain faces from `N` to `N+1` (60, 126 and 216 of them) are charged face by face. At every anchor, the faces of the larger box are the disjoint union of the old faces and the new faces, so every face is charged exactly once. The per-site sum of new faces is at most `49|tau|/3 ≤ J`.
- **All-size count of the extra faces.** A star is clipped exactly when `b_i = N` for some `i`. For such an anchor, let `A(b) = {i : b_i = N}`. An F2 face at `b` must avoid `e_i` for every `i` in `A(b)`. The class table gives the number of classes avoiding each set:

  | avoided | `e_x` | `e_y` | `e_z` | `e_x, e_y` | `e_x, e_z` | `e_y, e_z` | all three |
  |---|---|---|---|---|---|---|---|
  | classes | 17 | 13 | 5 | 10 | 3 | 1 | 0 |

  There are `(2N)^{3-|A|}` anchors of each type. The total is `4N^2·35 + 2N·14 = 28N(5N+1)`; the formula is checked against the class table for `N = 2..29`.
- **Where the extra faces lie.** Every extra face keeps coordinate `i` equal to `N` at all its sites. So it lies inside the outer layer, which is why `rho_B = 0`.
- **Per-site sum of the mixed decomposition.** The larger interaction splits into the old terms and the new terms, faces charged once. Its per-site sum is at most `28|tau|` in all three comparisons (the enumerated maximum is 84 face units of `|tau|/3`). So the AM2 constants apply to box 2 in this decomposition. The fixed point does not depend on the decomposition, because `L_k` is linear in `V`.
- **General comparison.** Any two centered boxes `Lambda_M`, `Lambda_M'` with `M, M' ≥ N`, of F1 or F2, are compared by telescoping the nested comparisons plus one same-size F1/F2 comparison.
- **Two volumes of one prescription (labelled).** Two finite complete-factor volumes of one prescription that both contain `Lambda_N` are each compared with their union. The new terms then lie outside `Lambda_N`, at l-infinity distance at least `N` from `e_z`.

**Exact distances** (l-infinity; l1 gives the same values):

\[
d(e_z,\text{shell})=N,\quad d(0,\text{shell})=N+1,\qquad d(e_z,\text{layer})=N-1,\quad d(0,\text{layer})=N .
\]

- **Shell.** A shell point has `|x_i| = N+1` for some `i`. If `i ∈ {x,y}`, `d(e_z,x) ≥ N+1`. If `i = z`, `|x_z - 1| ≥ N`, with equality only at `x_z = N+1`, attained at `(0,0,N+1)`.
- **Layer.** The same argument with `N` in place of `N+1`, attained at `(0,0,N)`.
- **Enumeration.** The values are confirmed for `N = 2..5`.
- **Wording note W1.** The new F1 stars also meet 98, 218 and 386 outer-layer sites of `Lambda_N`, at distance `N-1` from `e_z`. The proof uses only that each new star meets the shell.

## 6. The coefficient-difference theorem (item 4)

**Theorem (HNM-BA1-F09).** Fix a comparison, a cutoff `L`, a sign of `tau` and `|tau| ≤ 10^-8`. Let `c` be box 1's fixed point, zero-extended, and `c'` box 2's fixed point, and put `δ = c' - ιc`. Let `1 ≤ e^beta ≤ w ≤ w_max`. Then, for every `u` in `R`,

\[
\sum_{I\ni u}\|c'_I-c_I\|\;\le\;e^{-\beta d(u,B)}\,\frac{S_B}{1-\Gamma_\beta},\qquad \Gamma_\beta=e^{\beta}J\,G'(R),
\]

where `S_B ≤ e^beta t_1 + Γ_beta T_w` (exact_first_order) or `S_B ≤ e^beta J G(R)` (crude_majorant).

*Proof.*
1. **Locality of the map.** `Phi_{Lambda'}(ιc) = ιPhi_Lambda(c) + Psi_new(ιc)`, where `Psi_new(c) = sum_k (1/k!) H^{-1} P ad_C^k(V_new) Omega_0`. The reason: `ad_{ιC}^k(ιV_Lambda) Omega = (ad_C^k(V_Lambda) Omega^Lambda) ⊗ Omega^{Lambda'\Lambda}`, so `P_M` returns box 1's value when `M ⊂ Lambda` and kills it otherwise. In `Q_L` the compressions `Q_L V_X Q_L` keep their supports and norms (AM2 §6).
2. **Difference equation.** Since `ιc = ιPhi_Lambda(c)`, we get `δ = [Phi_{Lambda'}(c') - Phi_{Lambda'}(ιc)] + S` with `S = Psi_new(ιc)`.
3. **Contraction of the difference.** By (F04), telescoped over the `k` slots and summed, and since `ιc` and `c'` lie in `B_w(R)` (§3), `||Phi_{Lambda'}(c') - Phi_{Lambda'}(ιc)||_{B,beta} ≤ Γ_beta ||δ||_{B,beta}`.
4. **Source bound.**
   - The first-order part is exact: `S^(0) = H^{-1} P V_new Omega_0 = -(tau/72) sum_{new f} W_f Omega_0`. Each owner set `M_f` lies in a new term meeting `B`, so `rho_B(M_f) ≤ 1`. At most 49 new faces meet a site. Hence `||S^(0)||_{B,beta} ≤ e^beta·49|tau|/144 = e^beta t_1`.
   - The remainder, by (F05) with `J_new ≤ J`: `||S - S^(0)||_{B,beta} ≤ e^beta J (G(t_w) - 16) ≤ Γ_beta T_w`.
   - In the crude tier the whole source is bounded by `e^beta J G(R)`.
5. **Absorption.** The volume is finite, so `||δ||_{B,beta} ≤ S_B/(1 - Γ_beta)`.
6. **Extraction.** For `I ∋ u`, `rho_B(I) ≥ d(u,B)`, so `sum_{I∋u} ||δ_I|| ≤ e^{-beta d(u,B)} ||δ||_{B,beta}`. ∎

**Consequences.**
- **The constants at `e^beta = w`** (both pairs). In the exact tier `S_B ≤ w t_1 + Γ T_w = T_w`, so the constant multiplying `q^{d(e_z,B)}` is

\[
K_{\rm own}=\frac{T_w}{1-\Gamma}=\frac{w\,t_1}{(1-\Gamma)^2},\qquad q=1/w .
\]

- **Per comparison**, using the §5 distances and the worst site `u = e_z` (at `u = 0` there is one extra factor `q`):
  - F1 vs F2: `K_12 = K_own` at exponent `N-1`;
  - nested (F1 or F2): `K_own q^N = (q K_own) q^{N-1}`, so `K_nest = q K_own`;
  - general: `K_gen = K_12 + K_nest/(1-q)`, from telescoping `sum_{n≥M} K_nest q^{n-1}`;
  - labelled variants: the direct nested comparison gives `K_12 + K_nest`, and the union comparison gives `2 K_nest`.
- **Where the decay comes from.** It comes only from the weight `e^{-beta d(u,B)}`. The Lipschitz factor enters only as `1/(1 - Γ)`. The global sup-norm bound `||c^{N+1} - c^N||_a ≤ J_0 G(R)/(1 - J_0 G'(R)) = 37/6249384` has no decay, and it is never used as a per-shell factor (§10).
- **Weight direction.** The extraction step needs `rho_B(I) ≥ d(u,B)` for `I ∋ u`. That holds for the max-distance `rho_B`, whose weight grows away from `B`, towards `R`. A weight growing from `R`, or a min-distance weight, fails (§10).
- **Coefficient Cauchy bound.** For each fixed family, the whole sequence `N ↦ c_I^{F,N}` (for `I ∋ u`, `u` in `R`, fixed `L`) satisfies `sum_{I∋u} ||c_I^{F,N} - c_I^{F,N'}|| ≤ K q^{min(N,N')-1}`. This whole-sequence Cauchy bound comes from the estimate itself, not from compactness. No limit object and no common limit is claimed. The gate field `common_limit_claimed` stays false.

## 7. Constants (item 4): both pairs, every comparison, both signs, crude tier

All values are at `|tau| = 10^-8`, with `J = 28|tau| = 7/25000000` and `t_1 = 49/14400000000`. Every formula depends on `|tau|` only, so the `tau = -10^-8` value replays the same exact rational; it is a replay, not a second confirmation. Every constant is increasing in `|tau|`, so at fixed `q` the cap value bounds every smaller `|tau|`.

**Headline pair**, `q = 1/64` (`w = e^beta = 64`), exact_first_order / weighted_norm:
- `Γ = 2464/390625` (about `6.30784e-3`) and `T_w = 49/223580736` (about `2.19160205287e-7`);
- source: first order `49/225000000` (about `2.17777777777e-7`) plus remainder `3773/2729257031250` (about `1.38242750931e-9`), total `T_w`.

| comparison | exponent at `e_z` / at `0` | `K` in `K q^(N-1)` | preview |
|---|---|---|---|
| F1 `N` vs `N+1` | `N` / `N+1` | `19140625/5554260612255744` | `3.44611575441e-9` |
| F2 `N` vs `N+1` | `N` / `N+1` | `19140625/5554260612255744` | `3.44611575441e-9` |
| F1 vs F2 on `Lambda_N` | `N-1` / `N` | `19140625/86785322066496` | `2.20551408282e-7` |
| any two centered boxes, `M, M' ≥ N` (telescoping) | — | `2734375/12204185915601` | `2.24052224286e-7` |
| labelled: direct nested | — | `1244140625/5554260612255744` | `2.23997524036e-7` |
| labelled: one prescription via the union | — | `19140625/2777130306127872` | `6.89223150882e-9` |

The largest constant, `2734375/12204185915601`, is at most `1/2000000`, with margin about 2.2316. **Target met at both signs.**

**Floor pair**, `q = 148/390625` (`w = e^beta = 390625/148`):
- `Γ = 77/296` and `T_w = 49/4036608` (about `1.21389047437e-5`);
- source: first order `49/5455872` (about `8.98114911786e-6`) plus remainder `3773/1194835968` (about `3.15775562591e-6`).

| comparison | exact_first_order `K` | preview | crude_majorant `K` | preview |
|---|---|---|---|---|
| F1 or F2 nested | `67081/10791225000000` | `6.21625441041e-9` | `1369/171093750` | `8.00146118721e-6` |
| F1 vs F2 | `1813/110502144` | `1.64069214801e-5` | `37/1752` | `2.11187214611e-2` |
| general (telescoping) | `708203125/43148545682688` | `1.64131400907e-5` | `14453125/684115704` | `2.11267259551e-2` |
| labelled: direct nested | `708471449/43164900000000` | `1.64131377345e-5` | — | — |
| labelled: via the union | `67081/5395612500000` | `1.24325088208e-8` | — | — |

- The named floor tier is exact_first_order: `K = 708203125/43148545682688`, at most `1/12` (margin about 5077).
- The crude_majorant floor tier, `14453125/684115704`, also meets `1/12` (margin about 3.94) and is reported separately.
- At the floor the crude self-map uses the whole ball: `T^c_w = 1/64 = R`.

**Crude tier at `q = 1/64`** (reported, not a target):
- `T^c_w = 148/390625`; F1 vs F2 `148/388161`; nested `37/6210576`; general `9472/24454143` (about `3.87337229523e-4`).
- It fails `1/2000000` and is retained as a limited-tier value. Nothing is retuned.

**Labelled refinements and alternatives** (valid, never the bound):
- **Refined source loss.** The extra F2 faces lie inside the outer layer (`rho_B = 0`), so their loss is 1 rather than `w`. This gives `K_12 ≤ 57270955/16662781836767232` (about `3.43705844324e-9`).
- **Proved family.** For every `w` in `[1, w_max]`, the rate `q = 1/w` holds with `K_gen(w) = [w t_1/(1-Γ(w))^2]/(1-q)`. `check.py` tabulates `w = 2, 8, 64, 512, w_max`. The headline and floor pairs are the two frozen members; no `q` is chosen per `N`.
- **l1 convention.** `w_1^2 ≤ 390625/148`, `q_1,min` in `[608276253/31250000000, 19464840097/1000000000000]` (about `1.9465e-2`), and it does not close at `1/64`.
- **Cardinality weight** `e^{mu|I|}`. The loss is `e^{4mu}` and the rate is at least `(148/390625)^{1/4}` (about `0.139516`, stated in the contract as 0.1395). It is never relabelled as the diameter rate `3.79e-4`, and not used.

## 8. Uniformity in the cutoff

Every estimate of §§2–6 is dimension-free and holds in each `Q_L`, with constants that do not depend on `L`.
- The compressed interactions keep their supports and do not increase `J` (AM2 §6).
- `Q_L c^(1)` keeps or annihilates each face vector `W_f Omega_0`: it lies in a tensor product of on-site eigenspaces with energies `6 j_x` (factor `x` owning `j_x` links of `f`), and the enumerated maximum is 18. All face vectors are kept for `L ≥ 24` (AV1 §7). The same holds for the first-order source.
- No cutoff removal is applied to coefficients, and no untruncated creation expansion is asserted. AM2 §6 removes the cutoff for eigenvalues and AV1 F20–F23 for the ground vector; neither defines untruncated coefficients.

## 9. Coefficient decay is not reduced-density decay; mandatory sentence; gate fields (item 5)

**Coefficient decay is not decay of the reduced density on `R`.** The ground vector `psi = e^{-C} Omega_0` depends on every coefficient. Its `R`-marginal couples all supports through the normalization and the straddling terms (AV1 F07–F11). A statement about coefficients on supports meeting `R` does not by itself control `rho_{N,R}`; that step is BB1.

The fixture `coefficient_decay_not_marginal_decay` (AV1 F13 type) has three qubit sites `r, o, o'` with creations `c_{r,o} = 1/3` (straddling, the only coefficient meeting `{r}`), `c_o = b` and `c_{o'} = 2/5`:
- `b = 1/2` gives `rho_r = [[45/49, 6/49], [6/49, 4/49]]`;
- `b = 0` gives `rho_r = [[9/10, 0], [0, 1/10]]`.

The coefficients meeting `R` are identical, yet the marginals differ. So state decay is not inferred from coefficient decay.

**Mandatory sentence** (quoted once, verbatim, as one unbroken span; the constants follow it):

> For the zero-selected patterned family at the same coupling |tau|<=10^-8, and for the named construction families F1 (centered whole-star boxes) and F2 (all-contained-face boxes with padding) on centered coarse cubes, the AM2 creation coefficients in each on-site cutoff space, on supports meeting the cover R, differ between two boxes of the named constructions by at most K q^(N-1) in the anchored norm, uniformly in the cutoff, where N is the smaller box size; this is decay of the coefficients of the named constructions at a rate in N, not decay of the reduced density, not a statement about untruncated creation coefficients, not uniqueness of any ground state, and not a statement uniform in the lattice spacing a.

The constants in it:
- `R = {0,e_z}`, and the norm is the anchored sum at `u` in `R`;
- headline: `q = 1/64`, `K = 2734375/12204185915601` (exact_first_order, weighted_norm);
- floor: `q = 148/390625`, `K = 708203125/43148545682688` (exact_first_order, weighted_norm); the crude_majorant floor value `14453125/684115704` also meets `1/12`;
- `N ≥ 2` is the smaller box size;
- both signs, `|tau| ≤ 10^-8`.

**Gate fields** (exported exactly as in `gate_fields_required`):

| field | value |
|---|---|
| `uniqueness_of_ground_state_claimed`, `whole_sequence_claimed`, `state_decay_claimed`, `rate_in_a_claimed`, `continuum_claim`, `scientific_priority_verified`, `translation_invariance_claimed`, `common_limit_claimed`, `weak_coupling_claim` | false |
| `rate_in_N_claimed`, `coefficient_cauchy_claimed` | true |
| `coefficient_cauchy_scope` | AM2 creation coefficients of F1 and F2 on supports meeting R, in each on-site cutoff space |

Also exported: `untruncated_coefficients_asserted: false`. `whole_sequence_claimed: false` refers to states. The whole-sequence Cauchy bound of §6 is about coefficients and is recorded under `coefficient_cauchy_claimed`.

## 10. Scaling and trap fixtures (item 6)

**Scaling `tau → tau/100`** (brackets read from the contract; same exact formula, no intermediate rounding):

| constant | ratio (exact in `results.json`) | bracket |
|---|---|---|
| headline `K` (every comparison and the pair) | about `101.260829` | `[95,105]` |
| floor `K_own`, `K_12` | exactly `1` | `[99/100, 101/100]` |
| floor pair `K` (general, factor `1/(1-q_min)`) | about `1.000375` | `[99/100, 101/100]` |
| `q_min = 37888|tau|` | exactly `100` | exactly 100 |
| crude headline `K` (reported) | about `100.628` | — |

At `w = 1/q_min` both `J w = 7/9472` and `w t_1` are invariant, which is why the floor constant is `tau`-independent. The nested floor constant written in the `q^(N-1)` form, `q_min K_own`, carries one factor of `q_min`, so its ratio is exactly 100 (wording note W5). It is not claimed to be in the floor bracket.

**Trap fixtures** (exact; finite models, not transferred):
- **A weight growing from `R` fails** (`weight_direction_toward_source`). On a chain `0..n`, take the local map `(A δ)_i = (1/10)(δ_{i-1} + δ_i + δ_{i+1})` with source at `n`.
  - The weight `2^{n-i}` (growing towards `R`) certifies `|δ_0| ≤ (5/2) 2^{-n}` and covers the exact solution for `n = 1..6`.
  - The reversed weight `2^i` only gives `(5/2) 2^n`, so no decay is certified.
  - The non-submultiplicative weight `2^{r^2}` breaks the fixed per-step loss, and the min-distance weight breaks extraction. Both are rejected.
- **A global Lipschitz bound does not decay** (`global_lipschitz_not_decay`).
  - The nonlocal contraction `(Aδ)_i = (1/2) δ_n` has sup-norm Lipschitz constant `1/2`, yet its exact fixed-point difference is `δ_0 = 1` for every `n`. The claim `δ_0 ≤ (1/2)^n/(1/2)` is false.
  - In the model, the global bound `37/6249384` is the same for every `N`.
- **A per-creation loss charge fails** (`loss_per_interaction_not_per_creation`).
  - First-order fixture: `X = R`, `V = σ^x ⊗ σ^x`, `L_0 = (1/2)|11⟩`. The output diameter 1 exceeds the creation-diameter sum 0 by `d_X`. Its weighted norm `32` at `w = 64` exceeds the per-creation bound `16`; the per-interaction bound is `1024`.
  - Second-order fixture: `X = {0,e_x}`, `I_1 = {-e_x,0}`, `I_2 = {e_x,2e_x}`, `ad_{C_1} ad_{C_2}(V) Omega = |{-e_x,2e_x}⟩`. This is the disconnected output `M = 𝒩 \ X` with diameter `3 = d_X + 1 + 1`. The max shortcut (2) is rejected, and a creation disjoint from `X` gives the zero word.
- **Metric mixing** (`coarse_metric_named`). For the star with `B = {e_x}` and `p = e_y`: `d_1(p,B) = 2`, which exceeds `rho_B + diam_inf = 1`. An l1 distance with an l-infinity diameter breaks (b′).

## 11. Error ledger (preregistered terms)

| term | headline (`q=1/64`) | floor (`q=148/390625`) | status |
|---|---|---|---|
| `weighted_contraction_loss` | `Γ = 2464/390625`; amplification `(1-Γ)^{-2} ≈ 1.012736` | `Γ = 77/296`; `(1-Γ)^{-2} ≈ 1.826818` | charged. The loss `w` per interaction lies inside `Γ = J w G'(R)`, paid in `t_w` and in the difference |
| `boundary_source_terms` | `49/225000000 + 3773/2729257031250 = T_w` | `49/5455872 + 3773/1194835968 = T_w` | charged. New terms only, at most 49 faces per site, `J_new ≤ 28|tau|`, loss `e^{beta rho_B} ≤ e^beta` |
| `order_versus_distance_count` | — | — | not_applicable, with reason: not a numeric cost. The enumeration fixes `d_X = 1` and the exact exponents `N-1`, `N`, `N+1`, which enter only as integers |
| `exact_first_order_remainder` | `Γ T_w = 3773/2729257031250` | `Γ T_w = 3773/1194835968` | charged. This is the weighted AM2 remainder `||c - c^(1)||_w` |
| `cutoff_uniformity` | — | — | not_applicable, with reason: every estimate is dimension-free in each `Q_L`, and `Q_L c^(1)` keeps or annihilates face vectors |
| `arithmetic` | — | — | not_applicable, with reason: exact Fractions. The only enclosures are directed upward: `e^{1/8} ≤ 8/7`, so `G(R) ≤ 148/7` and `G'(R) ≤ 352` |

Deterministic terms add linearly over faces, shells and nodes. A root-sum-of-squares combination and division by `sqrt(N)` or `sqrt(#faces)` are rejected (`root_n_misuse`).

## 12. Controls (each a damaging mutation in `check.py`)

| control | damaging mutations rejected |
|---|---|
| `coherent_evidence_tampering` | with the packet hash rebound: a control Boolean flipped; the AY1 gate snapshot removed; headline `K` halved; `state_decay_claimed` set true; one family only; mandatory sentence trimmed; a forbidden phrase added |
| `exact_arithmetic_admission` | float, bool, NaN and zero-denominator inputs |
| `no_priority_or_continuum_claim` | `continuum_claim` true; `scientific_priority_verified` true |
| `changed_model_relabelled` | `tau=10^-14`; nonzero triple; SU(3); 2D; finite-graph id; the matched route-B model id; l1 metric relabelled; `w=128` |
| `insufficient_verdict_retained` | the crude tier relabelled accepted; `tau` retuned to `10^-10` |
| `tau_scaling_exponent` | a square-root bound (ratio 10) labelled linear; a bracket chosen after evaluation; a narrowed bracket; the nested floor constant claimed `tau`-independent |
| `wrong_delta_alpha_hbar_clock` | `tau/576` and `tau/9` (mixed units); a window in `u = theta/8` labelled `theta` (fixture `alpha=5`, `hbar=7`, `t=7/5`) |
| `missing_incoming_stars` | `J = 7|tau|` from the outgoing star; outgoing-only `J` in the contraction; a source counted from the 21 outgoing faces |
| `root_n_misuse` | RSS over 49 aligned faces; division by `sqrt(49)`; the telescoping sum divided by `sqrt(4)` |
| `tier_mixing_rejected` | exact source with crude `t` labelled exact; `t = w t_1` without self-consistency; prospective id `weighted_ii` used as a tier; the forward constant labelled `analytic_disc`; a crude component inside an exact constant |
| `reverse_premise_isolation` | deliberation, the forward BA1 report or a skeptic triage added to the reverse inventory |
| `face_count_all_sites` | site-0-only counts; the bound 84 used as a count |
| `uniform_in_N_not_in_a` | a rate statement without "in N at fixed spacing"; a claim in the lattice spacing |
| `placeholder_span_rejected` | angle spans with whitespace, a bar, or "e.g." |
| `negation_aware_phrase_scan` | an affirmative forbidden phrase (two fixtures); report and results scanned with the template removed as one literal |
| `parameters_declare_metric_weights_window` | `weights`, `window` or `metric` removed from parameters |
| `global_lipschitz_not_decay` | Lipschitz-as-decay on the nonlocal chain (`n = 3, 6`); the global constant used as a per-shell factor |
| `weighted_norm_contraction_rechecked` | the unweighted AM2 self-map cited for the weighted ball; `w = 2 w_max` |
| `loss_per_interaction_not_per_creation` | loss charged per creation only (first-order fixture); the output weight omitted |
| `diameter_subadditivity_through_interaction` | the max-instead-of-sum shortcut on the disconnected output |
| `coarse_metric_named` | an l1 distance with an l-infinity diameter; an l1 star diameter read as 1 |
| `weight_direction_toward_source` | a weight growing from `R`; the weight `2^{r^2}`; a min-distance weight |
| `cardinality_weight_rate_labelled` | the diameter rate `148/390625` relabelled as a cardinality rate |
| `boundary_distance_exact` | the F1/F2 exponent `N` instead of `N-1`; the nested exponent off by one |
| `boundary_source_new_terms_only` | old F1 terms charged in the source; a source set one layer inside |
| `f2_regrouping_charged_once` | regrouped whole groups charged (old faces twice) |
| `rate_constant_pair_prefrozen` | `q` optimized after the constants and reported; weight retuned to 128 |
| `q_min_not_crossed` | half of `q_min`; a rate below `q_min` rejected with the lower bound `G(R) ≥ 20.96…` |
| `analytic_route_disc_radius` | disc radius `2 tau_star` (dictionary `w = rho/|tau|` checked; route not executed here) |
| `untruncated_coefficients_not_asserted` | `untruncated_coefficients_asserted` true; a coefficient statement after cutoff removal |
| `decay_rate_in_N_not_a` | rate per fm; rate per lattice spacing; `rate_in_a_claimed` true |
| `coefficient_decay_not_marginal_decay` | state decay inferred from equal coefficients (F13 fixture) |
| `two_families_named` | one family; literal vertex boxes (I1 §7) added |
| `subsequence_versus_whole_sequence` | an alternating sequence with convergent subsequences; a whole-sequence state claim |
| `full_original_wilson_cover` | the four drawn links as the cover; a single-factor cover (48 links, 36 endpoints verified) |
| `gate_fields_topic_specific` | `rate_in_N_claimed` dropped; `common_limit_claimed` flipped; Cauchy scope widened |
| `ball_radius_not_used_as_tree_decay_ratio` | the ball radius `R = 1/64` used as the per-step tree ratio |

**Positive checks** without a contract id: `contract_snapshot_sha256`, `premise_gates_pinned_and_parsed`, `am2_constants_reverified`, `weighted_multilinear_estimate_and_contraction`, `diameter_convention_and_order_versus_distance`, `boundary_sources_enumerated`, `coefficient_difference_headline_pair`, `coefficient_difference_floor_pair`, `crude_tier_reported_separately`, `labelled_refinements_and_alternatives`, `cutoff_uniformity`, `mandatory_sentence_and_gate_fields`, `report_bound_to_results`, `error_ledger_itemized`.

**Not executable inside `check.py`:**
- The reverse agent's actual reads are checked by `freeze.py` (reverse snapshot inventory) and the skeptic.
- Freeze and byte-identical replays are protocol steps of `research/round33/tools/freeze.py`.

## 13. Exclusions, limitations and contract wording defects

**Contract exclusions (verbatim):**
- `decay of the reduced density or of any state (BB1/BB2)`
- `whole-sequence convergence of any state`
- `uniqueness of every infinite-volume ground state`
- `any estimate uniform in the lattice spacing a`
- `any statement about untruncated creation coefficients (AM2 section 6 removes the cutoff for eigenvalues and AV1 F20-F23 for the ground vector; neither defines untruncated coefficients)`
- `continuum or weak coupling`
- `scientific priority`

The preregistration adds `equality of GNS dynamics or of correlation functions of different states`.

**Additional exclusions on this route:**
- no reduced-density or state statement;
- no dynamics;
- no limit object and no common limit;
- the rate is per coarse step `(4a,2a,a)` in `N` at fixed spacing and strong bare coupling, never per unit of the lattice spacing or per physical length.

**Limitations.**
1. **Scope.** Only the zero-selected patterned family, the cover `R`, the two named families on centered cubes (plus the labelled union statement), fixed spacing and `|tau| ≤ 10^-8`.
2. **Inherited without re-proof.**
   - AM2: fixed point, uniqueness in the ball, gap and §6 cutoff facts;
   - AV1: `c^(1)` and `t_1`;
   - AY1: verification of the AM2 hypotheses for F2;
   - I1: the dictionary.

   The weighted estimate, the order-versus-distance lemma, the source identification, the distances and the difference theorem are derived here.
3. **Upper bounds only.** The constants are conservative. The first-order source is charged at 49 faces per site with loss `w`; the refined variants are labelled.
4. **Fixtures** are exact finite audits (`transfers_to_aq: false`), not proofs of the lattice statements.
5. **Correlation.** The selection note and the contract name the mechanism (weighted norm, loss per interaction, boundary-distance weight). Independence from the reverse producer is limited to route, enumeration and code, and all agents are correlated model agents.
6. **Scientific priority is unverified.**

**Contract wording defects (non-blocking).**
- **W1.** `parameters.weights` calls `B` "the sites met by the interaction terms present in one box and not the other" and names the shell. New F1 stars also meet outer-layer sites of `Lambda_N` (98, 218, 386 at `N = 2,3,4`; distance `N-1` from `e_z`). The proof uses only that each new term meets the shell; the literal "sites met" set gives the same `K` after the weight bookkeeping.
- **W2.** `parameters.weights` fixes `e^beta = 64`. The floor pair needs `e^beta = w = 390625/148` (`beta = mu`), which `beta ≤ mu` allows.
- **W3.** `global_lipschitz_not_decay` calls `2J_0G'(R)` the sup-norm Lipschitz constant. The fixed-point map has Lipschitz constant `J_0G'(R) ≤ 77/781250`; `2J_0G'(R)` is AM2's exclusion constant. `37/6249384 = J_0G(R)/(1 - J_0G'(R))` uses the former.
- **W4.** Item 2's "order at least ceil(d/diam)" is implied by the sharper `1 + ceil(d/diam)`, since the far term is itself one order.
- **W5.** The nested comparisons have exponent `N`. In the `q^(N-1)` form their constant carries one factor `q`, so the nested floor constant scales with `q_min` (ratio 100), while the pair constant stays in the floor bracket.
- **W6.** `missing_incoming_stars` mentions a Lieb-Robinson norm; there is none in this loop (BA2).

## 14. Proposed verdict

**`accepted_within_scope` for the forward half**, with sub-labels `boundary_decay_rate_only` and `static_not_dynamic`:
- both frozen pairs are proved for every comparison at both signs, with each proved constant at most its target;
- the weighted contraction holds at the cap for every `w ≤ 390625/148`;
- no bound is derived from the global Lipschitz constant.

The contract's `accepted_within_scope` requires both routes. The reverse analytic-disc route and the skeptical review are outside this producer.

## 15. Map of required items and controls to proofs and checks

| contract item | report section | `check.py` check id(s) |
|---|---|---|
| 1 (metric, weights, loss, difference weight named) | §1 | `parameters_declare_metric_weights_window`, `coarse_metric_named` |
| 1 (weighted multilinear estimate, itemized) | §2 | `weighted_multilinear_estimate_and_contraction`, `am2_constants_reverified`, `loss_per_interaction_not_per_creation`, `diameter_subadditivity_through_interaction` |
| 1 (weighted self-map and Lipschitz for every `w ≤ w_max`) | §3 | `weighted_multilinear_estimate_and_contraction`, `weighted_norm_contraction_rechecked`, `q_min_not_crossed` |
| 2 (order versus distance, diameter by enumeration, tables in both conventions) | §4 | `diameter_convention_and_order_versus_distance`, `report_bound_to_results` |
| 3 (boundary sources, 28N(5N+1) charged once, exact distances) | §5 | `boundary_sources_enumerated`, `boundary_source_new_terms_only`, `f2_regrouping_charged_once`, `boundary_distance_exact`, `missing_incoming_stars` |
| 4 (headline pair, floor pair, both signs, every comparison) | §§6–7 | `coefficient_difference_headline_pair`, `coefficient_difference_floor_pair` |
| 4 (crude tier separately; no global Lipschitz decay) | §§7, 10 | `crude_tier_reported_separately`, `global_lipschitz_not_decay` |
| 4 (each `Q_L`, constants independent of `L`) | §8 | `cutoff_uniformity`, `untruncated_coefficients_not_asserted` |
| 5 (not reduced-density decay; sentence; gate fields) | §9 | `coefficient_decay_not_marginal_decay`, `mandatory_sentence_and_gate_fields`, `gate_fields_topic_specific` |
| 6 (scaling, trap fixtures, controls) | §§10, 12 | `tau_scaling_exponent`, `weight_direction_toward_source`, `global_lipschitz_not_decay`, `loss_per_interaction_not_per_creation`, all 37 control ids |
| preregistered error terms | §11 | `error_ledger_itemized` |
| contract binding and premises | header | `contract_snapshot_sha256`, `premise_gates_pinned_and_parsed` |
| labelled refinements, alternatives, proved family | §7 | `labelled_refinements_and_alternatives` |

**Methodological lenses** (modern use of the snapshotted skills):
- **Newton, analysis before synthesis.** The coefficient difference was analyzed into a locality identity (Step 1), a contraction and a source before any constant was synthesized.
- **Tesla, complete accounting.** Every source channel is charged: new terms only, faces once, incoming stars included, remainder at its positive majorant.

No historical figure endorses anything here, and no historical or occult material supplies a premise.

## 16. Reproduction

```bash
python3 -B research/round33/forward/ba1/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/forward/ba1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/freeze.py verify research/round33/forward/ba1
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/ba1.json research/round33/forward/ba1/report.md
```

`check.py` does the following:
- verifies the contract sha256 before any evaluation;
- pins the sha256 of every admitted gate and parsed report;
- reads every target, bracket and parameter from the contract;
- records its own sha256 before evaluation;
- writes `results.json` and `source-manifest.json`, which bind `check.py`, `report.md`, every `inputs/` file and `results.json`.

BA1 is investigation 1 of 8 in Round33. This producer executed only the forward half.
