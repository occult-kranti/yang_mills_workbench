# Hruday boundary decay of the AM2 creation coefficients — BA1 reverse (complex-coupling analyticity, order-versus-distance count, Cauchy estimate)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted reverse production: the derivations, `check.py` and this report were written by Claude (an AI model) as the BA1 reverse producer, under reverse premise isolation (`reverse_premise_isolation: true`). It is correlated model-agent work. It is not human review and not formal verification. HNM labels are project aliases.

**What this producer read.**
- **First**, the frozen contract snapshot `inputs/research/round33/contracts/ba1.json`. Its sha256 `2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9` was checked with `sha256sum` before reading, and `check.py` checks it again before any evaluation.
- **Then**, only files under `inputs/` (27 snapshots):
  - *read in full:* `AGENTS.md`; `selection-ba1.md`; the AM2 forward and reverse reports and the AM2 skeptic review; the AM2 and AQ1 gates; the AQ1 forward report; the I1 forward report; the AV1 forward and reverse reports; the Round32 lessons reference; the paired-physics SKILL and its complete-residual reference; the Newton, Tesla and historical-panel SKILL files;
  - *read in part:* the AV1, AW1, AY1 and AY2 gates (every field except the `bindings` blocks, long fields truncated in display); the AY1 forward report (sections 1–8) and AY1 reverse report (sections 0–2); the AQ2 forward report (its first section); the AY2 forward report (lines found by a keyword search for `28N(5N+1)` and the O2–O4 obligation rows);
  - *not opened beyond that keyword search:* the AW1 forward report.
- **Outside `inputs/`, for conventions only** (no premise weight): `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py`, and the header, validators and result assembly of `research/round32/reverse/ay1/check.py`. The Round32 AY1 reverse report was read from its `inputs/` snapshot. A byte comparison (`cmp`) of each of the 27 snapshots with its declared repository path displayed no content; all 27 agree.
- **Not read:** nothing under `research/round33/forward/`, `research/round33/skeptic/`, `research/round33/experts/`, and nothing under `research/round33/advisor/` except the snapshot of `selection-ba1.md`. In particular no deliberation file, no loop-1 preview and no forward BA1 file was opened.

**Scratchpad disclosure.** My private scratch folder is `/tmp/claude-0/ba1-reverse-private/`. It holds geometry, constant and chain-fixture prototypes, the source text of this report and test runs of `check.py`. **None of it is evidence.** I created it with `mkdir -p` and did not list `/tmp/claude-0/`, so I saw no other agent's folder names. **I opened no file in any other agent's scratch folder** and no file in the shared session scratchpad root. The Claude harness saved copies of three of my own long tool outputs (the two AV1 report reads and a gate summary) to its tool-results cache; those are my own reads.

**Attribution.** Banach's fixed-point theorem, Weierstrass' theorem on uniform limits of holomorphic maps, the maximum-modulus principle and Cauchy's estimates are standard. So is the connected-cluster support property of perturbation expansions. The commuting nilpotent creation expansion is the admitted AM2 construction, credited there to the Bravyi–DiVincenzo–Loss lineage, with Gauvin arXiv:2503.15539v3 A.6–A.8 as AM2's template. The complex-coupling route and the order-versus-distance count were named by the advisor in the frozen contract (`direction_note`); they are shared premises, not inventions of this producer. Independence is claimed only for the derivations, the enumerations, the constants and the code. Scientific priority is unverified.

## Verdict (reverse half)

Model: **`AQ_patterned_zero_selected`**. It is SU(2) in Kogut–Susskind form on `Z^3` at fixed spacing, with coarse 24-link factors, the selected triple exactly `(0,0,0)` and the Haar product reference. There are 21 omitted faces per anchor, each entering with coefficient `-(tau/3)` in normalized units `delta=alpha/8`. Both signs of `tau` are covered, with `|tau|<=10^-8`, together with the AM2 creation expansion (`J<=28|tau|`, `R=1/64`, `G(t)=16e^{8t}(1+10t)`). The two named families are **F1**, the AQ1 centered whole-star boxes `Lambda_N=[-N,N]^3`, and **F2**, the I1 section-6 all-contained-face boxes with padding on the same `Lambda_N`, both with `N>=2`. The cover is `R={0,e_z}`.

1. **Item 1 (reverse form): proved.** The AM2 map, complexified in the coupling `z`, is a contraction of the anchored ball `||c||_a<=1/64` for every `|z|<=rho` at both declared disc radii. The contraction constants are `28 rho G'(R) < 2464/390625` (about `6.308e-3`) at `rho=64|tau|` and `< 77/296` (about `0.2601`) at `rho=tau_star=1/37888`. The coefficient map `z -> c(z)` is holomorphic on the open disc and continuous on the closed one, in every on-site cutoff space `Q_L`, uniformly in `L`. At real `z=tau` it is the AM2 fixed point. The multilinear estimate HNM-AM2.5 is re-derived step by step: only the interaction norm depends on `z`.
2. **Item 2: proved.** A coefficient on a support meeting `R` depends on an interaction term at coarse l-infinity distance `d>=1` from `R` only at order at least `1+ceil(d/diam)`, which implies the contract form `ceil(d/diam)`. The proof uses `diam=1` (coarse l-infinity). The stars' l-infinity diameter 1 and l1 diameter 2 are confirmed by enumeration on `Lambda_2`, `Lambda_3` and `Lambda_4` and by an all-size argument. Both tables (l-infinity and l1) are published, and an exact qubit-chain fixture shows that the sharp order is attained.
3. **Item 3: proved.** Every source term of every comparison lies at l-infinity distance **exactly** `N-1` from `R`. This is derived by enumeration for `N=2,3,4` and by an all-size common-core lemma. The F1-versus-F2 source is the `28N(5N+1)` extra faces, charged face by face once at their anchors.
4. **Item 4: proved** for every comparison (F1 nested, F2 nested, F1 versus F2 on the same `Lambda_N`, and any two complete-factor volumes containing `Lambda_N`), at both signs, in every `Q_L`:

   `sum_{I containing u} ||c^A_I - c^B_I|| <= K q^(N-1)`, for `u` in `R`,

   | pair | q | K (exact) | preview | frozen target | margin | tier / route | disc radius |
   |---|---|---|---|---|---|---|---|
   | headline | `1/64` | `49/111790368` | `4.38320410574e-7` | `1/2000000` | `1.1407` | exact_first_order / analytic_disc | `rho=64\|tau\|` |
   | floor | `148/390625` | `49/2018304` | `2.42778094875e-5` | `1/12` | `3432.49` | exact_first_order / analytic_disc | `rho=tau_star=1/37888` |

   The crude tier is reported separately. At `q=1/64` it gives `K=296/390625` (about `7.58e-4`), which fails `1/2000000`; this is reported and is not a target. At `q=148/390625` it gives `K=1/32`, which meets `1/12`. The global Lipschitz constant is never used as a decay factor.
5. **Item 5.** Coefficient decay is **not** decay of the reduced density on `R`: an exact fixture shows it. Analyticity is not extended to the reduced density, because no zero-free region of the complexified normalization is proved. The mandatory template is quoted once (Section 5), and the gate fields are exported.
6. **Item 6.** The `tau -> tau/100` ratios are `4340004/43129` (about `100.63`, inside `[95,105]`) for the headline `K`, exactly `1` (inside `[99/100,101/100]`) for the floor `K`, and exactly `100` for `q_min`. The exact trap fixtures are given in Section 6. All 37 contract controls are damaging mutations in `check.py`.

**Checker.** `check.py` runs **61 exact checks**. **37 of them are the contract controls**, each rejecting explicit damaging mutations (132 mutations in total). The `-B` and `-B -O` outputs are byte-identical.

**Proposed reverse verdict: `accepted_within_scope`**, with sub-labels `boundary_decay_rate_only` and `static_not_dynamic`. Admission still needs the forward route, the exchange and the skeptical review. The headline margin, `1.14`, is thin. It is reported unchanged; the labelled refinements in Section 4.5 are not substituted for it.

## 0. Frozen parameters, notation and exact constants

| symbol | meaning | value (exact) |
|---|---|---|
| `tau` | coupling, both signs | `+-1/100000000` |
| `J(z)` | per-site interaction sum at complex coupling (4 anchor groups, incoming included) | `28\|z\|`; `J_0=7/25000000` |
| `R` | AM2 ball radius (not a decay ratio) | `1/64` |
| `G, G'` | AM2 majorant and derivative at `R` (directed `e^{1/8}<8/7`) | `G(R)<148/7`, `G'(R)<352` |
| `tau_star` | largest disc radius with `28 rho G(R)<=R` | `R/(28*148/7)=1/37888` |
| `q_min` | `28\|tau\|G(R)/R = \|tau\|/tau_star` | `37888\|tau\|`; `148/390625` at the cap |
| `rho` | declared disc radius | headline `64\|tau\|` (`1/1562500` at the cap); floor `tau_star` |
| `q` | decay ratio `\|tau\|/rho` | headline `1/64`; floor `37888\|tau\|` |
| `t_1(rho)` | first-order anchored norm on the circle, `49 rho/144` | `49/225000000`; `49/5455872` |
| `T(rho)` | `t_1(rho)/(1-28 rho G'(R))` (exact_first_order tier) | `49/223580736`; `49/4036608` |
| `t_i(rho)` | crude circle bound `28 rho G(R)` | `148/390625`; `1/64` |

The contract parameters declare the **metric** (coarse l-infinity on factor sites, `d_X=1`), the **weights** (reverse: disc radii `rho=tau_star` and `rho=64|tau|`), the **window** (not applicable, static coefficients), the **clock**, `N_min=2` and the **cutoff**. `check.py` reads them from the contract and rejects a contract copy with any of these fields removed. `q=1/64` at the headline equals `R=1/64` numerically. This is a coincidence of the frozen choice `rho=64|tau|`: the rate is `|tau|/rho` for a checked disc radius, never the ball radius used as a per-step ratio.

## 1. Item 1 — the AM2 contraction at complex coupling and analyticity of the coefficients

### 1.1 The complexified map

Fix a finite complete-factor volume `Lambda` of either prescription (F1 whole stars `b+S` inside `Lambda`, or F2 clipped groups `X_b` inside `(b+S) cap Lambda`), and an on-site cutoff space `Q_L=tensor_x 1_[0,L](h_x)`. Write the interaction at unit coupling as `V_1=sum_X V_{X,1}`, where `V_{X,1}=-(1/3) sum W_f` over the faces of the group, so `||V_{X,1}||<=7`. Set `V(z)=z V_1`. For collections `c=(c_I)` with `c_I` in `tensor_{x in I} Q_x Q_L H_x` (complex vectors), define

\[
F_z(c)=\sum_{k=0}^{8}\frac{L^{(z)}_k(c,\ldots,c)}{k!},\qquad
L^{(z)}_k(c_1,\ldots,c_k)_M=H_M^{-1}P_M\,\mathrm{ad}_{C_1}\cdots\mathrm{ad}_{C_k}(V(z))\,\Omega_0=z\,L^{(1)}_k(c_1,\ldots,c_k)_M .
\tag{HNM-BA1-R01}
\]

At real `z=tau` this is exactly the AM2 map (HNM-AM2.7 at `s=1`). The coefficient equation does not involve the scalar `E(z)`, so nothing else has to be complexified.

### 1.2 HNM-AM2.5 at complex coupling, item by item

The AM2 forward proof of HNM-AM2.5 (section 2) uses the steps below. The table records where `z` enters.

| step | content | dependence on `z` |
|---|---|---|
| (a) | creations commute; overlapping supports multiply to zero | none (algebra of the `c`'s) |
| (b) | every creation support `I_j` meets `X` (a disjoint creation commutes with `V_X(z)`) | none (`V_X(z)` acts on `X`) |
| (c) | `N\X ⊂ M ⊂ N ∪ X`, at most `2^p=16` output sets, `\|I_j\|<=\|M\|+p` | none |
| (d) | the commutator expansion has `2^k` products | none |
| (e) | each projected product has norm at most `\|\|V_X(z)\|\| prod_j \|\|c_{j,I_j}\|\|` | `\|\|V_X(z)\|\|=\|z\| \|\|V_{X,1}\|\|` |
| (f) | `\|\|H_M^{-1}\|\|<=1/\|M\|` from `h_x>=Q_x` | none (the real on-site operator; no spectral shift) |
| (g) | `sum_{X ni u}\|\|V_X(z)\|\|<=J(z)=28\|z\|` (four anchor groups per site, incoming stars included) | through (e) |
| (h) | `sum_{I cap X nonempty}\|\|c_I\|\|<=p\|\|c\|\|_a` | none |
| (i) | `1/\|M\|<=(p+1)/\|I_l\|` and `sum_{X meets I_l}\|\|V_X(z)\|\|<=J(z)\|I_l\|` | through (g) |
| (j) | termination for `k>2p=8` (four-qubit fixture: `ad_C^8(V)Omega=8!\|1111>`, `ad_C^9(V)=0`, re-run) | none |

No step uses self-adjointness of `V` or reality of the coupling. Therefore, for every complex `z`,

\[
\|L^{(z)}_k(c_1,\ldots,c_k)\|_a\le 28|z|\;16\,8^k\bigl(1+\tfrac{5k}{4}\bigr)\prod_j\|c_j\|_a .
\tag{HNM-BA1-R02}
\]

For F2 the groups have `|X_b|<=4`, and the admitted AY1 item-by-item verification gives the same `J<=28|tau|`. Smaller supports only lower the counting constants.

### 1.3 Self-map and Lipschitz inequalities on the disc, re-evaluated exactly

For `||c||_a, ||c'||_a<=R` and `|z|<=rho`, summing (R02) against `G(t)=sum_k 16 8^k(1+5k/4)t^k/k!` and telescoping each `k`-linear term gives

\[
\|F_z(c)\|_a\le 28\rho\,G(R),\qquad \|F_z(c)-F_z(c')\|_a\le \kappa(\rho)\,\|c-c'\|_a,\quad \kappa(\rho):=28\rho\,G'(R).
\tag{HNM-BA1-R03}
\]

The enclosure `e^{1/8} < 1416435566333532896036259034764742340707/1250000000000000000000000000000000000000 < 8/7` (partial sum plus a geometric tail) gives `G(R)<148/7` and `G'(R)<352`. The inequalities are evaluated at the declared radius itself, never by citing the real-coupling AM2 constants:

| disc | `rho` at the cap | `28 rho G(R)` bound | vs `R=1/64` | `kappa(rho)` bound |
|---|---|---|---|---|
| headline | `64\|tau\| = 1/1562500` | `148/390625` (about `3.789e-4`) | `<R` | `2464/390625` (about `6.308e-3`) |
| floor | `tau_star = 1/37888` | `1/64` (with `148/7`; strict with the actual `G(R)`) | `<=R` | `77/296` (about `0.2601`) |

A radius above `tau_star` fails the self-map with the frozen `148/7` enclosure. `check.py` rejects `rho=2 tau_star`, and it rejects the disc radius `4 tau_star` that an outgoing-only `J=7|z|` would allow.

### 1.4 Analyticity of the coefficient map

**Lemma 1.1.** For `rho<=tau_star`, every finite complete-factor volume of F1 or F2 and every `L`, `F_z` has exactly one fixed point `c(z)` in the ball. The map `z -> c(z)` is continuous on `|z|<=rho` and holomorphic on `|z|<rho`, with values in the finite-dimensional coefficient space of `Q_L`. At real `z=tau` with `|tau|<=10^-8`, `c(tau)` is the AM2 fixed point.

*Proof.* Put `c^(0)=0` and `c^(m+1)(z)=F_z(c^(m)(z))`. Since `F_z` is `z` times a polynomial map, each iterate is a polynomial in `z`. By (R03) every iterate stays in the ball, and `sup_{|z|<=rho}||c^(m+1)(z)-c^(m)(z)||_a <= kappa^m R`. The iterates therefore converge uniformly on the closed disc. The limit is continuous there and holomorphic inside (Weierstrass, coordinatewise in finite dimensions). By continuity of `F_z` it is a fixed point, and the contraction makes it the only one in the ball. For real `tau`, `|tau|<rho`, and `c(tau)` is a fixed point of the real AM2 map in the AM2 ball, so it is the AM2 fixed point by AM2's uniqueness. ∎

Consequently the Taylor coefficients `c(z)=sum_{n>=1} z^n c_n` obey the formal recursion

\[
c_1=L^{(1)}_0,\qquad c_n=\sum_{k\ge1}\frac1{k!}\sum_{\substack{n_1+\cdots+n_k=n-1\\ n_j\ge1}}L^{(1)}_k(c_{n_1},\ldots,c_{n_k})\quad(n\ge2).
\tag{HNM-BA1-R04}
\]

### 1.5 Tiers on the circle

**Lemma 1.2.** For `|w|<=rho` and `t(w):=||c(w)||_a`:
- *crude_majorant:* `t(w)<=28|w|G(t(w))<=28 rho G(R)=:t_i(rho)`;
- *exact_first_order:* write `c(w)=w L^{(1)}_0+r(w)`, where `(L^{(1)}_0)_M=-(1/72) sum_{M_f=M} W_f Omega_0` is the exact AV1 first-order coefficient at unit coupling (face energy 24, face-vector norm `1/2`, distinct faces orthogonal). The number of faces through a factor is at most 49, derived from the I1 table by translation covariance and enumerated. Hence `||w L^{(1)}_0||_a<=49|w|/144=t_1(|w|)`, an l1 sum over faces. By AV1 F05 and convexity of `G`, `||r(w)||_a<=28|w|(G(t)-16)<=28|w|G'(R) t`. So `t<=t_1(rho)+kappa(rho)t`, that is

\[
t(w)\le T(\rho):=\frac{t_1(\rho)}{1-28\rho G'(R)} .
\tag{HNM-BA1-R05}
\]

**Identity with the tier rule.** With `J=28|tau|` and `w=rho/|tau|`, `T(rho)` is exactly `w t_1/(1-J w G'(R))`. This is the self-consistent inequality of the contract's `tier_label_rule`, re-derived in the norm in which it is stated here: the anchored norm at complex coupling on the circle `|w|=rho`.

### 1.6 Cutoff uniformity

Every statement holds in each `Q_L`, with constants independent of `L`. Compression does not enlarge supports or increase `J`. Each first-order face vector `W_f Omega_0` puts at most 3 of its links on one factor (site energy at most `18<=24`). It is therefore kept exactly for `L>=24` (AV1 section 7), and for smaller `L` the first-order counts only decrease. No cutoff removal is applied to coefficients, and no untruncated creation expansion is asserted.

### 1.7 What is not complexified

Only the creation coefficients are continued in `z`. The scalar `E(z)`, the AM2 gap and excited-sector exclusion, and the reduced density are not. The reduced density needs the normalization `sum_M psi_M(z)^2`, the analytic continuation of `||psi||^2`, and this can vanish inside the disc. Exact fixture: on two qubits, `psi(z)=Omega-2z|11>` has the entire coefficient `2z`, while its normalization `1+4z^2` vanishes at `z=i/2`, inside `|z|<=1`. No zero-free region is proved here. Extending the disc, or analyticity, to `rho_R` is rejected by `check.py`.

## 2. Item 2 — the order-versus-distance count

### 2.1 Connected families

Decompose `V_1=sum_{Y in P} V_Y` into **pieces**: bounded operators `V_Y` acting on the factors of `Y`. The pieces may be faces (`Y=M_f`), whole stars or clipped groups. The Taylor coefficients depend only on `V_1`, not on the decomposition. Expanding each `V`-slot of (R04) gives `c_n=sum_{(Y_1,...,Y_n)} Phi_n(Y_1,...,Y_n)`, where `Phi_n` is multilinear in `(V_{Y_1},...,V_{Y_n})` and built only from `H_M^{-1}P_M` and creation products.

**Lemma 2.1 (connected families).** `Phi_n(Y_1,...,Y_n)_M` vanishes unless (i) the family `{Y_1,...,Y_n}` is connected in its intersection graph, and (ii) `M ⊂ Y_1 ∪ ... ∪ Y_n`.

*Proof,* by induction on `n`. For `n=1`, `(L^{(1)}_0)_M=H_M^{-1}P_M V_Y Omega_0` vanishes unless `M ⊂ Y`. For `n>=2`, a term of (R04) has one piece `Y` in its `V`-slot and creations `c_{n_j,I_j}`. By step (b) each `I_j` meets `Y`, and by step (c) `M ⊂ Y ∪ (∪_j I_j)`. By induction each `c_{n_j,I_j}` comes from a connected family `F_j` of `n_j` pieces with `I_j ⊂ ∪F_j`. A point of `I_j ∩ Y` lies in some member of `F_j`, so `{Y} ∪ F_1 ∪ ... ∪ F_k` is connected. It has `1+sum n_j=n` pieces, and its union contains `M`. ∎

### 2.2 The count, the diameter convention and the charge per interaction term

**Lemma 2.2 (order versus distance).** Let `M` meet `R`, and let the family of a nonzero `Phi_n(...)_M` contain a piece `Y` with `d:=d_inf(R,Y)>=1`. Let `diam` bound the l-infinity diameters of the pieces. Then

\[
n\;\ge\;1+\Bigl\lceil \frac{d}{\mathrm{diam}}\Bigr\rceil\;\ge\;\Bigl\lceil \frac{d}{\mathrm{diam}}\Bigr\rceil .
\tag{HNM-BA1-R06}
\]

*Proof.* A point `p_0` of `M ∩ R` lies in some piece `Z_0`, by Lemma 2.1(ii). By connectivity there is a chain `Z_0, Z_1, ..., Z_m=Y` of distinct pieces of the family with consecutive members intersecting. Pick `q_i` in `Z_{i-1} ∩ Z_i`. Then `d(p_0,q_1)<=diam(Z_0)` and `d(q_i,q_{i+1})<=diam(Z_i)`, and `q_m` lies in `Y`. So `d<=d(p_0,q_m)<=m·diam`. Since `Y≠Z_0` (because `d>=1`), the family has at least `m+1` pieces. ∎

**The charge per interaction term.** Each piece crossed costs one `diam`, charged once per interaction term (one order in `z`) and never per creation. The terminal source piece need not be crossed, which gives the `+1`. The companion inequality for supports is **Lemma 2.3** (diameter subadditivity through an interaction): for a nonzero term with piece `X` and creations `I_j`, each of which meets `X`,

\[
\mathrm{diam}(M)\le \mathrm{diam}(X)+\sum_j\mathrm{diam}(I_j).
\tag{HNM-BA1-R07}
\]

Every point of `M` lies in `X` or in some `I_j`. For `p` in `I_a` and `q` in `I_b`, route through points of `I_a ∩ X` and `I_b ∩ X`. It follows that a connected family of `n` pieces has union diameter at most `n·diam`. The first-order coefficient on `M_f={0,e_z}` (one interaction, zero creations, diameter `1=d_X`) shows that a loss charged per creation would be wrong. On the disconnected fixture `X={0,e_x}`, `I_1={-e_x,0}`, `I_2={e_x,2e_x}`, `M=N\X={-e_x,2e_x}`, one has `diam(M)=3=d_X+1+1`. So the max-instead-of-sum shortcut (`d_X+max=2`) is invalid. `check.py` also verifies (R07) exhaustively on 64 supports meeting a star and on 3033 configurations.

**The metric.** The proof uses the **coarse l-infinity metric on factor indices, `diam=d_X=1`**. Every whole star `b+S` has `S-S={0,±e_i,±(e_i-e_j)}`, with l-infinity norms 0 and 1 and l1 norms 0, 1 and 2. So for every `b` the star has l-infinity diameter 1 and l1 diameter 2. Faces and clipped groups are subsets. Enumeration on `Lambda_2`, `Lambda_3` and `Lambda_4` confirms these values for all 64, 216 and 512 stars, and l-infinity diameter 1 for every F2 face. Each site lies in at most 4 stars or groups, and 7 stars meet `R` for `N>=2`. The l1 reading (`diam=2`) is a labelled alternative and is never mixed with the l-infinity reading. On the source distances found here, `N-1` along the z-axis in both metrics, it would give the exponent `ceil((N-1)/2)`.

### 2.3 Order-versus-distance tables (enumerated, both conventions)

Each entry is `d: least order / ceil(d/diam) / 1+ceil(d/diam) (number of pieces)`. The "least order" is the smallest connected-family size joining a piece meeting `R` to a piece at distance `d`, found by breadth-first search on the enumerated intersection graph. It is the least order at which Lemma 2.1 allows any dependence. The pieces are F1 whole stars. The F2 clipped-group tables are in `results.json` and satisfy the same inequalities.

| box | l-infinity (`diam=1`, **used**) | l1 (`diam=2`, labelled alternative) |
|---|---|---|
| `Lambda_2` | `0:1/0/1(7)`, `1:2/1/2(47)`, `2:4/2/3(10)` | `0:1/0/1(7)`, `1:2/1/2(19)`, `2:2/1/2(20)`, `3:3/2/3(12)`, `4:4/2/3(5)`, `5:6/3/4(1)` |
| `Lambda_3` | `0:1/0/1(7)`, `1:2/1/2(62)`, `2:3/2/3(131)`, `3:6/3/4(16)` | `0:1/0/1(7)`, `1:2/1/2(22)`, `2:2/1/2(42)`, `3:3/2/3(51)`, `4:3/2/3(45)`, `5:4/3/4(29)`, `6:5/3/4(14)`, `7:6/4/5(5)`, `8:9/4/5(1)` |
| `Lambda_4` | `0:1/0/1(7)`, `1:2/1/2(62)`, `2:3/2/3(166)`, `3:4/3/4(255)`, `4:8/4/5(22)` | `0:1/0/1(7)`, `1:2/1/2(22)`, `2:2/1/2(45)`, `3:3/2/3(73)`, `4:3/2/3(90)`, `5:4/3/4(92)`, `6:4/3/4(78)`, `7:5/4/5(54)`, `8:6/4/5(31)`, `9:7/5/6(14)`, `10:8/5/6(5)`, `11:12/6/7(1)` |

In every row the least order is at least `1+ceil(d/diam)`. With l-infinity it equals `1+d` for every `d<=N-1`, along the z-axis chain of stars `(0,0,1)+S, ..., (0,0,k)+S`, so the sharp count is attained. The larger values at the largest distance `d=N` come from the box walls. The all-size argument is Lemma 2.2.

**Sharpness fixture** (exact; `model_is_finite_graph: true`, `transfers_to_aq: false`). Take a qubit chain on sites `0..4` with `H_0=sum n_x`, bonds `X_iX_{i+1}` and `R={0}`. The creation coefficients are obtained from the intermediate-normalized Rayleigh–Schrödinger ground vector by exact cumulant inversion of `psi=prod_I(1-c_I a_I)Omega`, which is the AM2 fixed point of this algebra. Remove bond `(d,d+1)`. The first order at which a coefficient on a support containing 0 changes is exactly `1+d`:

| removed bond | `d` | first differing order | witness | box A / box B value |
|---|---|---|---|---|
| (1,2) | 1 | 2 | `c_{0,2}` | `-1/2` / `0` |
| (2,3) | 2 | 3 | `c_{0,3}` | `5/8` / `0` |
| (3,4) | 3 | 4 | `c_{0,4}` | `-7/8` / `0` |

This rejects an exponent taken from the far endpoint or the shell site (for bond (3,4), site 4 at distance 4). Combined with the sharp count, that choice would claim vanishing through order 4, but the difference is nonzero at order 4.

## 3. Item 3 — the boundary sources and their exact distances

**Lemma 3.1 (common core).** Let `N>=2`. Every omitted face at l-infinity distance at most `N-2` from `R` is retained by both F1 and F2 on every finite complete-factor volume containing `Lambda_N`.

*Proof.* Such a face has a point `q` with `d_inf(q,0)<=N-2`, or with `d_inf(q,e_z)<=N-2`. In both cases `q` lies in `Lambda_{N-1}`: in the second case `q_z` is in `[3-N,N-1]`. Its anchor is `b=q-s` with `s` in `S`, so `b_i` is in `[-N,N-1]` and `b+S ⊂ Lambda_N`. F1 therefore retains the whole star, and F2 retains every face whose owner set lies in `b+S`. ∎ The enumeration confirms this for `N=2,3,4` against all faces of F2 on `Lambda_5` (82, 1044 and 3910 faces within distance `N-2`).

**Corollary.** In every comparison between two such volumes, every source term (a term present in one and not the other) lies at distance at least `N-1` from `R`. The enumerated witnesses below attain `N-1` in all three named comparisons.

| comparison | source terms (N=2 / 3 / 4) | each meets | exact min l-infinity distance | witness |
|---|---|---|---|---|
| F1 `Lambda_N` vs `Lambda_{N+1}` | whole stars: 152 / 296 / 488 `=(2N+2)^3-(2N)^3`; faces `21x` (3192 / 6216 / 10248) | the shell `Lambda_{N+1}\Lambda_N` | `N-1` (l1 also `N-1`) | star `(0,0,N)+S` contains `(0,0,N)` |
| F2 `Lambda_N` vs `Lambda_{N+1}` | faces 3920 / 7224 / 11536, in 60 / 126 / 216 gaining groups | the shell | `N-1` | face at `(0,0,N)` with owner set `{(0,0,N),(0,0,N+1)}` |
| F1 vs F2 on `Lambda_N` | faces `28N(5N+1)` = 616 / 1344 / 2352, at 60 / 126 / 216 anchors with `max_i b_i=N` | the positive outer layer `{max_i p_i=N}` | `N-1` | face at `(0,0,N)` with owner set `{(0,0,N),(1,0,N)}` |
| general (examples) | F1(`Lambda_2`) vs F2(`Lambda_4`): 11760; F2(`Lambda_3`) vs F1(`Lambda_4`): 4872; F1(`[-2,3]x[-2,2]x[-2,4]`) vs F2(`Lambda_3`): 4000; F2(`[-3,2]x[-2,3]x[-2,2]`) vs F2(`Lambda_2`): 925 | — | at least `N-1` (1, 2, 2, 2) | Lemma 3.1 |

**The shell is not the controlling set.** The shell itself is at distance `N` from `e_z` and `N+1` from `0`. The new F1 stars, however, reach one site inward: `(0,0,N)+S` contains `(0,0,N)`, in `Lambda_N`, at distance `N-1` from `e_z`. Face by face, `28N(5N+1)` of the new F1 faces (616 / 1344 / 2352) lie **inside** `Lambda_N` on its positive outer layer. They are new only because their whole star was not retained, and `check.py` proves that they are exactly the extra F2 faces `F2(Lambda_N)\F1(Lambda_N)`. The sites met by the F1 nested source are the shell together with the positive outer layer of `Lambda_N`. For F1 the source terms are whole stars, each of which meets the shell. For F2 and for F1 versus F2 they are faces.

**The `28N(5N+1)` count, all sizes.** A face `(b,k)` of class support `b+K_k` is retained by F2 iff `b_i<=N-1` for each direction `e_i` in `K_k` (and `b` is in `Lambda_N`), and by F1 iff `b_i<=N-1` for all `i`. The I1 table has 14 single-direction classes and 7 two-direction classes. So `|F2|=14(2N+1)^2(2N)+7(2N+1)(2N)^2=28N(2N+1)(3N+1)`, `|F1|=21(2N)^3`, and the difference is `28N[(2N+1)^2+N(2N+1)-6N^2]=28N(5N+1)`. The extra faces sit at the `(2N+1)^3-(2N)^3-1` anchors with some `b_i=N`; the corner `(N,N,N)` carries none. Hence all of their sites satisfy `max_i p_i=N`.

**F2 regrouping, charged once.** The F2 nested source is charged face by face at the anchors. Each gained face appears exactly once, and no old face of a gaining group is charged. At most 45 new faces pass through any site (`N=2,3,4`), so the per-site face sum of the source is at most `45|tau|/3<=49|tau|/3<=J=28|tau|`. The reverse route charges the source only through its distance (Section 4), so this per-site sum is an audit and not a term of `K`.

## 4. Item 4 — Cauchy's estimate and the coefficient-difference bound

### 4.1 The theorem

**Theorem 4.1.** Let `N>=2`. Let `Lambda^A` and `Lambda^B` be finite complete-factor volumes containing `Lambda_N`, with prescriptions `P^A` and `P^B` in `{F1,F2}`. Let `L` be any cutoff, `0<rho<=tau_star`, and `tau` real with `0<|tau|<rho` and `|tau|<=10^-8`. Then, for `u` in `R`,

\[
\sum_{I\ni u}\bigl\|c^A_I(\tau)-c^B_I(\tau)\bigr\|\;\le\;2\,t(\rho)\,\Bigl(\frac{|\tau|}{\rho}\Bigr)^{n_0}\;\le\;2\,t(\rho)\,\Bigl(\frac{|\tau|}{\rho}\Bigr)^{N-1},
\qquad n_0\ge N,
\tag{HNM-BA1-R08}
\]

with `t(rho)=T(rho)` at the exact_first_order tier and `t(rho)=t_i(rho)` at the crude tier. For `u` in `R`, every `I` containing `u` meets `R`.

*Proof.*
1. **Common volume.** Embed both boxes in `Lambda^A ∪ Lambda^B`, putting unperturbed on-site factors on the padding. The fixed-point map with interaction supported in `Lambda^A` preserves the closed set of collections supported in `Lambda^A`, because `M ⊂ Y ∪ (∪ I_j)`. The fixed point therefore lives there, with the same coefficients as in `Lambda^A` alone. The same holds for `Lambda^B`. Both have `J<=28|z|`, so Lemma 1.1 applies to both.
2. **The difference is analytic and vanishes to high order.** `g(z):=(c^A_I(z)-c^B_I(z))_{I ni u}` is holomorphic on `|z|<rho` and continuous on `|z|<=rho`, with values in a finite-dimensional space normed by `||g||_u=sum_{I ni u}||g_I||`. Decompose both interactions face by face. Terms of (R04) whose faces are all common to both boxes coincide, because the on-site operators and the cutoff are the same. Every other term contains a source face, which lies at distance at least `N-1` from `R` (Lemma 3.1). By Lemmas 2.1–2.2 such a term contributes to supports containing `u` only at order `n>=1+(N-1)=N`. So `g_n=0` for `n<n_0` with `n_0>=N`. In the contract form, `n>=ceil((N-1)/1)=N-1`.
3. **Cauchy's estimate in maximum-modulus form (Schwarz lemma).** `h(z)=g(z)/z^{n_0}` is holomorphic on the open disc. For a linear functional `l` of dual norm at most 1, `l∘h` is scalar holomorphic. For `r<rho` and `|z|<=r`, the maximum principle gives `|l(h(z))|<=r^{-n_0} max_{|w|=r}||g(w)||_u`. Taking the supremum over `l` and letting `r` increase to `rho`, using continuity on the closed disc, gives `||g(tau)||_u<=(|tau|/rho)^{n_0} max_{|w|=rho}||g(w)||_u`.
4. **The circle bound.** For `|w|=rho`, `||g(w)||_u<=sum_{I ni u}||c^A_I(w)||+sum_{I ni u}||c^B_I(w)||<=t^A(w)+t^B(w)<=2t(rho)`, by Lemma 1.2. ∎

The decay comes from `|tau|/rho` and the vanishing order alone. No Lipschitz constant enters as a decay factor, and no source norm is charged. The source enters only through its distance.

### 4.2 The named comparisons and the frozen pairs

The four comparisons of `parameters.comparisons` are special cases of Theorem 4.1:
- F1 `Lambda_N` versus F1 `Lambda_{N+1}`;
- F2 `Lambda_N` versus F2 `Lambda_{N+1}`;
- F1 versus F2 on the same `Lambda_N`, with exponent `N-1` and the `28N(5N+1)` faces as the source;
- any two volumes containing `Lambda_N` of F1 or F2 (centered boxes `Lambda_M`, `Lambda_M'` with `M,M'>=N`, or any complete-factor volumes of one prescription), compared directly through their union.

Using the contract exponent `N-1`, the constants are `K=2t(rho)`:

| constant | tier | route | `rho` | `q` | `K` exact | preview | target | met |
|---|---|---|---|---|---|---|---|---|
| headline | exact_first_order | analytic_disc | `64\|tau\|` | `1/64` | `49/111790368` | `4.38320410574e-7` | `1/2000000` | yes (margin `3493449/3062500`, about `1.1407`) |
| floor | exact_first_order | analytic_disc | `1/37888` | `148/390625` | `49/2018304` | `2.42778094875e-5` | `1/12` | yes (margin about `3432.49`) |
| crude at `q=1/64` | crude_majorant | analytic_disc | `64\|tau\|` | `1/64` | `296/390625` | `7.5776e-4` | reported, not a target | fails `1/2000000` |
| crude at `q=148/390625` | crude_majorant | analytic_disc | `1/37888` | `148/390625` | `1/32` | `3.125e-2` | `1/12` | yes |

**Both signs.** The disc contains `±tau`, and `K` depends only on `|tau|`. The `-tau` evaluation is a replay of the same formula, not a second confirmation.

**Smaller `|tau|`.** `K(64|tau|)` is increasing in `|tau|`, and `q=1/64` is fixed, so the cap values bound every `0<|tau|<=10^-8`. For the floor pair, `q=37888|tau|<=148/390625` and `K` does not depend on `tau`. At `tau=0` both boxes have `c=0`.

**Example values** `K q^(N-1)` at the headline: `N=2`, about `6.849e-9`; `N=3`, about `1.070e-10`; `N=4`, about `1.672e-12`. `check.py` records the previews for every comparison, pair and `N=2,3,4`.

### 4.3 Why the global Lipschitz constant is not a decay factor

The contraction constant bounds sup-norm differences without any reference to distance. Applied to two boxes, it gives only the volume-independent

`||c^{N+1}-c^N||_a <= J_0G(R)/(1-J_0G'(R)) = 37/6249384`,

the same number for every `N`. Here `J_0G'(R)<77/781250` is the Lipschitz constant of the fixed-point map, while `2J_0G'(R)<77/390625` is AM2's shifted-inverse exclusion constant. An exact fixture shows that a small Lipschitz constant carries no locality. The linear map `T(c)_i=(1/2)mean(c)+s_i` on 6 sites has sup-norm Lipschitz constant `1/2`, yet `c_0=1/6` for every position of the unit source. A claimed decay `(1/2)^5` is therefore false. `check.py` rejects the Lipschitz constant, or the no-decay bound, used as the rate.

### 4.4 Rate in N and the coefficient Cauchy property

For `N<=M<=M'`, Theorem 4.1 with the direct union comparison gives `||c(Lambda_M)-c(Lambda_M')||_u<=K q^(N-1)`, uniformly in `N` at fixed spacing and uniformly in the cutoff. The **whole** coefficient sequence `N -> (c_I(Lambda_N))_{I ni u}` of F1, and likewise that of F2, is therefore Cauchy in each `Q_L`. This follows from a Cauchy bound, not from a subsequence argument. The F1 and F2 coefficient sequences have vanishing difference, with rate `K q^(N-1)`. The rate is **per coarse step at fixed spacing**; a coarse step is `(4a,2a,a)` in fine units. It is not a rate in the lattice spacing and has no physical length reading. No state, reduced density or untruncated coefficient limit follows. The gate fields `whole_sequence_claimed` and `common_limit_claimed` concern states and stay `false`.

### 4.5 Labelled refinements (not headline) and one route the contract names

| refinement | headline value | floor value | why it is not the headline |
|---|---|---|---|
| sharp exponent `n_0=N` (Lemma 2.2 with `+1`) | `K q = 49/7154583552` (about `6.849e-9`) | `K q_min = 1813/197100000000` (about `9.198e-9`) | absorbing `q_min` makes the floor constant linear in `tau`, outside the prefrozen bracket `[99/100,101/100]`; the contract statement freezes exponent `N-1` |
| first-order cancellation on `R` | `3773/1364628515625` (about `2.765e-9`) | `3773/597417984` (about `6.316e-6`) | the exact first-order parts on supports containing `u` coincide (Lemma 3.1 for the faces meeting `R`), so the circle bound is `2·28 rho G'(R) T(rho)`; it is quadratic in `tau` (ratio about `10062.8`), outside the prefrozen linear bracket `[95,105]` |
| Cauchy coefficient-sum form `M q^{n_0}/(1-q)` | `14/31441041` (about `4.453e-7`) | — | weaker than the maximum-modulus form |
| telescoped general comparison (the route the contract names) | `K(2-q)/(1-q) = 889/1006113312` (about `8.836e-7`) | — | **exceeds `1/2000000`** at exponent `N-1`; the direct union comparison gives `K`, and telescoping with the sharp exponent gives `889/64391251968` (about `1.381e-8`), which meets it |

All refinements use the same tier (exact_first_order) and the same route (analytic_disc). None of them replaces a headline constant.

## 5. Item 5 — coefficient decay is not decay of the reduced density; the mandatory sentence

**Plain statement.** Coefficient decay is not decay of the reduced density on `R`. The reduced density `rho_R=Tr_out|psi><psi|/||psi||^2` depends on every coefficient: through the normalization, and through the straddling contractions of AV1 (F07–F11), which carry outside creations into the `R`-marginal. Controlling `rho_R` is BB1. **Exact fixture** (AV1 F13 type): qubits `r`, `o`, `o'` with creations `c_{r,o}=1/3` (straddling), `c_o=b` and `c_{o'}=0`, and `R={r}`. Changing `b` from `1/2` to `0` leaves every coefficient on supports meeting `R` unchanged (difference 0). Yet `rho_r` moves from `[[45/49,6/49],[6/49,4/49]]` to `[[9/10,0],[0,1/10]]`, with trace-norm-squared difference `3681/60025`. `check.py` rejects the inference of state decay from coefficient decay. Section 1.7 records the separate fact that the analyticity of the coefficients does not extend to `rho_R`.

**The mandatory sentence template, quoted once verbatim:**

> For the zero-selected patterned family at the same coupling |tau|<=10^-8, and for the named construction families F1 (centered whole-star boxes) and F2 (all-contained-face boxes with padding) on centered coarse cubes, the AM2 creation coefficients in each on-site cutoff space, on supports meeting the cover R, differ between two boxes of the named constructions by at most K q^(N-1) in the anchored norm, uniformly in the cutoff, where N is the smaller box size; this is decay of the coefficients of the named constructions at a rate in N, not decay of the reduced density, not a statement about untruncated creation coefficients, not uniqueness of any ground state, and not a statement uniform in the lattice spacing a.

The constants for the template are:
- `K=49/111790368` at `q=1/64` (exact_first_order tier, analytic_disc route, `rho=64|tau|`);
- `K=49/2018304` at `q=148/390625` (exact_first_order tier, analytic_disc route, `rho=tau_star=1/37888`);
- crude tier, reported separately: `296/390625` at `q=1/64` and `1/32` at `q=148/390625`;
- `R={0,e_z}`, F1 and F2 on `Lambda_N`, `N>=2`, both signs, every `Q_L`, and every comparison of `parameters.comparisons`.

**Gate fields exported (the contract's topic-specific set).**
- `rate_in_N_claimed: true`;
- `coefficient_cauchy_claimed: true`, with `coefficient_cauchy_scope: "AM2 creation coefficients of F1 and F2 on supports meeting R, in each on-site cutoff space"`;
- `false`: `uniqueness_of_ground_state_claimed`, `whole_sequence_claimed`, `state_decay_claimed`, `rate_in_a_claimed`, `continuum_claim`, `scientific_priority_verified`, `translation_invariance_claimed`, `common_limit_claimed` and `weak_coupling_claim`.

`label: boundary_decay_rate_only`, with secondary label `static_not_dynamic`. No limit statement here concerns states. The only whole-sequence statement concerns coefficients and comes from a Cauchy bound; every state statement inherited from AQ1 remains subsequential.

## 6. Item 6 — scaling, trap fixtures and controls

**`tau -> tau/100` scaling.** Each ratio is computed from the same exact formula at `tau` and `tau/100` without intermediate rounding, and compared with the preregistered bracket:

| constant | ratio (exact) | preview | bracket | in bracket |
|---|---|---|---|---|
| `K` exact_first_order at `q=1/64` | `4340004/43129` | `100.628440260` | `[95,105]` | yes (linear, positive nonlinear correction `1/(1-28·64\|tau\|G'(R))`) |
| `K` floor pair | `1` | `1` | `[99/100,101/100]` | yes (`rho=tau_star` does not depend on `tau`) |
| `q_min` | `100` | `100` | exactly 100 | yes |

The crude-tier ratios are `100` at `q=1/64` and `1` at the floor. They are labelled and are not targets.

**Exact finite fixtures for the traps** (all labelled `model_is_finite_graph: true`, `transfers_to_aq: false`):
- **A weight growing from `R` fails.** Take the chain `0..4`, `T(Delta)_i=(1/4)(Delta_{i-1}+Delta_{i+1})+s_i`, with a unit source at site 4 and `R={0}`. The exact fixed point has `Delta_0=1/195`.
  - The weight growing toward `R` from the source, `2^(4-i)`, has weighted Lipschitz constant `5/8` and gives `|Delta_0|<=1/6` (decay).
  - The weight growing with distance from `R`, `2^i`, gives `128/3`, above the unweighted bound `2` (no decay), and is rejected.
  - The non-submultiplicative weight `2^((4-i)^2)` has weighted Lipschitz constant 32 and is rejected.
  - In the reverse route, the direction is the count from `R` to the source; an exponent taken from the observed support's own distance to `R` is rejected.
- **A global Lipschitz bound that does not decay.** The mean-field map of Section 4.3.
- **A per-creation loss charge that fails.** The first-order face vector on `{0,e_z}` has diameter `1=d_X` with zero creations. The chain's first-order `c_{0,1}=z/2` has diameter 1 with zero creations.
- **Order sharpness.** The qubit chain of Section 2.3.
- **Normalization zero.** Section 1.7.
- **Marginal.** The fixture of Section 5.
- **Subadditivity.** Section 2.2.

**Controls.** All 37 contract controls are implemented as damaging mutations, and each must raise `AdmissionError`. None uses `assert`. Section 10 lists them.

## 7. Error ledger (preregistered terms, added linearly)

| term | value | note |
|---|---|---|
| `weighted_contraction_loss` | reverse reading: the disc contraction. Headline `28 rho G(R)<148/390625`, `kappa<2464/390625`; floor `28 rho G(R)<=1/64`, `kappa<77/296`. The cost of the disc is the circle factor `rho/\|tau\|` inside `t(rho)`: 64 at the headline and `1/q` at the floor. | never the unweighted AM2 constants |
| `boundary_source_terms` | enters only through its distance `N-1`, as the vanishing order; no norm charge in `K` | audit: face-by-face per-site source sum at most `45\|tau\|/3<=49\|tau\|/3<=J` |
| `order_versus_distance_count` | exponent `N-1` (contract form, used); sharp `N` (labelled) | derived distances, enumerated and all-size |
| `exact_first_order_remainder` | `28 rho G'(R) T(rho)` per box: headline `3773/2729257031250` (about `1.382e-9`); floor `3773/1194835968` (about `3.158e-6`) | included in `T(rho)` and hence in `K` |
| `cutoff_uniformity` | not applicable as a numeric cost | constants do not depend on `L`; face vectors are kept exactly for `L>=24`, and first-order counts only decrease for `L<24` |
| `arithmetic` | not applicable as a numeric cost | exact Fractions throughout; the only enclosure is the directed `e^{1/8}<8/7`; decimals are truncated previews |

Deterministic terms add linearly. The circle bound is `t^A+t^B`, not a root sum of squares, and nothing is divided by `sqrt(N)` or by the square root of a face count.

## 8. Scope, exclusions and claim flags

**Exclusions** (the contract's, respected):
- decay of the reduced density or of any state (BB1/BB2);
- whole-sequence convergence of any state;
- uniqueness of every infinite-volume ground state;
- any estimate uniform in the lattice spacing `a`;
- any statement about untruncated creation coefficients;
- continuum or weak coupling;
- scientific priority.

**Preregistration exclusions,** also respected: equality of GNS dynamics or of correlation functions of different states.

**Claim flags,** all `false`: `continuum_claim`, `uniqueness_of_ground_state_claimed`, `state_decay_claimed`, `rate_in_a_claimed`, `scientific_priority_verified`, together with the other false gate fields. `rate_in_N_claimed` and `coefficient_cauchy_claimed` are `true`, within the scope stated.

**Scope and honest gaps.**
- **Coefficients only.** Everything here is a statement about AM2 creation coefficients, in each on-site cutoff space, at fixed spacing and extreme strong bare coupling (`|tau|<=10^-8`). No reduced density, state, dynamics, gap, untruncated coefficient or continuum statement follows.
- **Inherited without re-proof:**
  - AM2: the multilinear majorant, whose steps are re-derived in the table of Section 1.2 only for their dependence on `z`;
  - AV1: the exact first-order coefficient and the self-consistent remainder;
  - AY1: the F2 item-by-item premises;
  - I1: the dictionary.

  The maximum principle, Weierstrass' theorem and Banach's theorem are standard and are not machine-checked.
- **Fixtures** audit algebra and rejection logic. They do not prove the infinite-dimensional statements, which rest on the arguments above.
- **Thin headline margin.** The headline margin is about `1.14`. The margin of 2 is a freeze-time property of the target, not an acceptance condition. The labelled refinements show a large reserve, but they are not substituted, and nothing was retuned after the constants were seen.
- **Independence** is limited to derivation, enumeration and code. The route, the targets and the brackets are shared through the contract.

## 9. Contract wording defects and remarks (for the skeptic and advisor)

1. **Nested source set.** `parameters.weights` identifies the source set of a nested comparison with "the shell `Lambda_{N+1}` minus `Lambda_N`", and `boundary_distance_exact` quotes the shell distances (`N` from `e_z`, `N+1` from `0`). But the sites met by the new F1 stars include the positive outer layer of `Lambda_N`, and the new terms lie at distance **`N-1`**, not `N`. The frozen exponent `N-1` is consistent with the correct distance `N-1` and the contract form `ceil(d/diam)`. Using the shell distance with the sharp count would overclaim by one order; the chain fixture rejects that.
2. **F1-versus-F2 source set.** The source set is written as "`max_i |b_i| = N`". The extra faces lie only on the positive outer faces `max_i b_i=N`. The contract's set is a superset, which is harmless.
3. **General comparison "by telescoping".** The contract names telescoping for the general comparison. At exponent `N-1` telescoping costs `(2-q)/(1-q)` and would exceed the headline target (`8.84e-7` against `5e-7`). The analytic route compares any two volumes directly through their union and gets `K` itself. Telescoping with the sharp exponent also meets the target.
4. **"The admitted sup-norm Lipschitz constant `2J_0G'(R)`".** The number `37/6249384` in `global_lipschitz_not_decay` equals `J_0G(R)/(1-J_0G'(R))`. It uses the fixed-point Lipschitz constant `J_0G'(R)<77/781250`. The constant `2J_0G'(R)` is AM2's shifted-inverse exclusion constant. With it, the number would be `37/6248768`.
5. **Order lemma form.** The contract's `ceil(d/diam)` is not sharp: the source term need not be crossed, which gives `1+ceil(d/diam)`, attained here. The frozen floor bracket `[99/100,101/100]` presumes the contract form; with the sharp form, the floor constant would absorb `q_min` and become linear in `tau`. The headline therefore keeps the contract form.
6. **Exact first-order tier and linearity.** The headline bracket (linear in `tau`) presumes that the circle bound is charged at first order. With the exact first-order coefficients, the first-order parts cancel on supports containing `u` in `R`, which gives a quadratic, smaller bound. That bound is recorded as a labelled refinement, because the prefrozen bracket rejects a headline constant of the wrong `tau` order.

## 10. Item and control map

**Items.**
- Item 1: Sections 1.1–1.7.
- Item 2: Section 2.
- Item 3: Section 3.
- Item 4: Section 4.
- Item 5: Section 5.
- Item 6: Sections 6–7 and the list below.

**Controls.** Each is a check in `check.py` that rejects the listed mutations:

| control | damaging mutations rejected |
|---|---|
| `coherent_evidence_tampering` | seven coherently rehashed contract edits (headline `K` target relaxed, headline `q` changed, `rate_in_a_claimed` true, a control removed, isolation flag false, a hash-binding Boolean flipped, `tau` changed); a byte change without rehash; a declared snapshot removed; an admitted gate edited (pinned sha256) |
| `exact_arithmetic_admission` | float, bool, `NaN`, zero denominator, float bound admission |
| `no_priority_or_continuum_claim` | continuum, priority or weak-coupling flag true; historical lens or governmental record used as a premise |
| `changed_model_relabelled` | coupling above cap, nonzero triple, relabelled model id, uniform `J=29`, SU(3), 2D, finite-graph result, l1 metric, changed disc rule, changed window |
| `insufficient_verdict_retained` | floor only, crude only or l1 only relabelled accepted; global Lipschitz or failed disc relabelled limited; crude headline admitted; `tau` retuned |
| `tau_scaling_exponent` | quadratic refinement as headline; floor constant absorbing `q_min`; square-root `q_min`; bracket chosen after evaluation |
| `wrong_delta_alpha_hbar_clock` | amplitudes `tau/9` and `tau/576` from mixed units; `u`-window labelled `theta`; `delta` clock labelled `theta` (non-unit fixture `alpha=5`, `hbar=7`) |
| `missing_incoming_stars` | outgoing-only `J=7\|tau\|`; orthant 2 stars; source count 21 (outgoing anchor only); disc radius from `J=7\|z\|` |
| `root_n_misuse` | `sqrt(49)` and `sqrt(82)` sums; root-sum-square of the two balls; division by `sqrt(N)` |
| `tier_mixing_rejected` | exact label with crude `t`; `t_1` without self-consistency; tier or route outside the vocabulary; crude label on exact `t` |
| `reverse_premise_isolation` | forward BA1 report, skeptic triage, deliberation or lens memo added; a premise missing |
| `face_count_all_sites` | literal counts; site-0 anchor-only 21; anchors-in-`R` 42 as the faces meeting `R` |
| `uniform_in_N_not_in_a` | "uniform in the lattice spacing"; an unqualified "uniform" next to a rate |
| `placeholder_span_rejected` | angle-bracket spans with a space, a bar or `e.g.` in an exported statement |
| `negation_aware_phrase_scan` | affirmative forbidden phrasings appended to the report and statements (a negated one is accepted) |
| `parameters_declare_metric_weights_window` | metric, weights, window or clock removed from a coherently rehashed contract |
| `global_lipschitz_not_decay` | `2J_0G'(R)` as a decay factor; the mean-field fixture claim `(1/2)^5`; the no-decay bound `37/6249384` as a rate |
| `weighted_norm_contraction_rechecked` | real-cap constants cited for the disc; radius `2 tau_star`; unweighted Lipschitz `77/781250` claimed at `tau_star` |
| `loss_per_interaction_not_per_creation` | per-creation reach on the first-order face and on the chain `c_{0,1}` |
| `diameter_subadditivity_through_interaction` | the max rule on the disconnected fixture |
| `coarse_metric_named` | l1 distance with diameter 1; l-infinity distance with diameter 2 |
| `weight_direction_toward_source` | weight growing from `R` (bound `128/3` above `2`); quadratic weight (Lipschitz 32); exponent from the observed support |
| `cardinality_weight_rate_labelled` | cardinality rate relabelled as the diameter rate `148/390625`; cardinality loss `e^mu` (rate at least `q_min^(1/4)>=0.13951645099`) |
| `boundary_distance_exact` | nested distance `N` (shell); F2 outer layer at `N`; shell-site exponent in the chain fixture |
| `boundary_source_new_terms_only` | old star charged; a new star missing; a term not meeting the shell; old F2 face charged |
| `f2_regrouping_charged_once` | a gaining group charged whole (old faces included); a face charged twice |
| `rate_constant_pair_prefrozen` | `q=1/128`; floor `K` target changed; `rho` optimized per `N` |
| `q_min_not_crossed` | rate `q_min/2`; disc `2 tau_star` |
| `analytic_route_disc_radius` | reduced density or normalization claimed analytic on the disc; radius beyond `tau_star` |
| `untruncated_coefficients_not_asserted` | untruncated coefficients asserted; no cutoff named; cutoff removed for coefficients |
| `decay_rate_in_N_not_a` | per fm; per lattice spacing; physical length reading |
| `coefficient_decay_not_marginal_decay` | state decay inferred from zero coefficient difference (the AV1 F13-type fixture) |
| `two_families_named` | single family; unfrozen class; F2 collapsed onto F1 |
| `subsequence_versus_whole_sequence` | whole sequence of states; whole sequence without a Cauchy bound; unquantified limit |
| `full_original_wilson_cover` | four drawn links; a single factor |
| `gate_fields_topic_specific` | AY1 fields reused; `coefficient_cauchy_claimed` missing; `rate_in_N_claimed` false; `state_decay_claimed` true |
| `ball_radius_not_used_as_tree_decay_ratio` | ball radius `R=1/64` as the per-step ratio; unchecked disc |

**Newton, Tesla and panel lenses** (frozen snapshots, used as modern method rules; no historical person endorses anything here):
- *Newton:* analysis ran backwards from the desired bound to the vanishing order and the circle bound; synthesis ran forwards through Lemmas 1.1–3.1.
- *Tesla:* the complete accounting of source, load and transfer. The source is every term present in one box only, face by face or whole star. The load is the supports containing `u` in `R`. The transfer is a chain of pieces, charged one diameter per interaction term.
- *Historical-panel rule:* the "weight loss must be paid at every nonlinear step" is honoured by the per-interaction charge. Coefficient decay is not called state decay.

## 11. Reproduce

```bash
python3 -B research/round33/reverse/ba1/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/reverse/ba1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/freeze.py verify research/round33/reverse/ba1
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/ba1.json research/round33/reverse/ba1/report.md
```

`check.py` does the following:
- verifies the contract snapshot sha256 before evaluation and records its own sha256 before evaluation;
- pins the sha256 of the six admitted gates it reads;
- reads the targets, the brackets, the reference value and the template from the contract;
- writes `results.json` (61 checks) and `source-manifest.json`, which binds this report, the checker and all 27 input snapshots.

`freeze.json` binds the whole producer closure.
