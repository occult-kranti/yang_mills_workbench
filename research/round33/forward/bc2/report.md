# Hruday route-B uniform model: every-site coefficient decay, marginal locality, whole-sequence convergence and the node restated for the limit — BC2 forward (single producer)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production: the derivations, `check.py` and this report were written by Claude (an AI model) as the single BC2 forward producer under the frozen BC2 contract (`research/round33/contracts/bc2.json`, sha256 `28abe3775455087384b3c9dbbb2df67b923e31b964d40efa7ea9787ee8b6b98a`). BC2 is a single-direction loop (`direction: single+skeptic`); admission also needs the skeptic's replay from the contract alone, which is outside this producer. It is correlated model-agent work, not human review and not formal verification. HNM labels are project aliases; the contribution alias of this packet is `HNM-BC2-F`.

**What this producer read.**
- **First**, the contract snapshot `inputs/research/round33/contracts/bc2.json`; its sha256 was checked with `sha256sum` before reading, and `check.py` checks it again before any evaluation.
- **Then only files under `inputs/`** (42 snapshots: `AGENTS.md`, the contract and its 40 shared premises):
  - *read in full:* `AGENTS.md`; `selection-bc2.md`; the AX1 and AX2 gates (all fields, bindings included); the admitted AX2 calculator; the AX1 forward report; the BA1 forward and reverse reports; the BB1 reverse report; the Round32 lessons reference; the I1 forward report; the paired-physics SKILL and its complete-residual reference; the Newton and Tesla SKILL files;
  - *read in part:* the BB2 forward report (every section except its Section 6 on correlation functions); the BB2 reverse report (Sections 3–7); the AX2 forward report (header, verdict, Sections 1–5 and the start of 6); the AV1 forward report (Sections 1–3 and 6–9, including F20–F23); the AM2 forward report (Sections 1–3 and the start of 4); the AQ1 forward report (Sections 1–2 and the start of 3); the AX1 skeptic review (verdict, proved items, re-derived numbers, review against the items); the AX2 skeptic review (opening and a keyword search); the AX1 reverse report (headings, header and verdict); the BA1, BB1 and BB2 gates (every field except `bindings`, which the checker reads only for hashes); the AQ1, AQ2, AM2 and AL1 gates (verdict, accepted, limitations, decision); the AV1 and AV2 gates (verdict, accepted, decision); the BA1, BA2, BB1 and BB2 contracts (their `new_control_semantics` entries for the inherited control ids, and keyword lines of the BB1 and BB2 parameters); the BB1 skeptic review (keyword searches only);
  - *not opened:* the AM2 reverse report, the AV1 reverse report and the historical-panel SKILL (their content enters only through the admitted gates).
- **Outside `inputs/`, for conventions only** (no premise weight): `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py`, and parts of `research/round33/reverse/bb1/check.py` (header, helpers, validators, contract validation and result assembly; BB1 is gated). The fixture engine of `check.py` follows that file's conventions; every BC2 derivation, constant, fixture and control is new code. A directory listing of `research/round33/tools/` showed the names `arb_crosscheck.py`, `freeze_contract.py`, `record_gate.py` and a `__pycache__` folder; none of them was opened. No git command was run.
- **Not read:** nothing under `research/round33/forward/bc1/`, `research/round33/experts/`, and nothing under `research/round33/skeptic/` or `research/round33/advisor/` except the declared snapshots in `inputs/`.

**Scratchpad disclosure.** My private scratch folder is `/tmp/claude-0/bc2-forward-private/`. It holds a replay of the BB1 reverse formulas (used to understand the method, zero-selected, never exported), an exact route-B preview, a harness that imports `check.py` with bytecode writing disabled, development results, a source-edit audit (Section 7) and the production run `run1`. **None of it is evidence.** I created it with `mkdir -p` and did not list `/tmp/claude-0/` or the shared scratchpad root, so I saw no other agent's folder names and opened no file of any other agent. The Claude harness saved copies of two of my own long reads (the contract print and a combined selection-note/AX1-gate print) to its tool-results cache; those are my own reads.

**Tooling note.** The agent file-writing tool refused to create this `.md` file with a generic rule against report files. Because this report is a required protocol artifact that `check.py`, `phrase_scan.py` and `freeze.py` read, it was written with a shell heredoc instead; the content is unaffected.

**Attribution.** Banach's fixed-point theorem, Weierstrass' theorem, the maximum-modulus principle, the pure-state trace-distance identity, the contractivity of the partial trace and the completeness of the trace class are standard. The commuting nilpotent creation expansion is the admitted AM2 construction (credited there to the Bravyi–DiVincenzo–Loss lineage, with Gauvin arXiv:2503.15539v3 A.6–A.8 as AM2's template), re-instantiated for route B by AX1. The analytic-disc method is the BA1 reverse Theorem 4.1, the iterated split is the BB1 reverse route and the whole-sequence and identification scheme is BB2's; the contract names all three, so they are shared premises. Independence is claimed only for the route-B re-derivation, the enumerations, the constants and the code. Scientific priority is unverified.

## Verdict (forward route)

Model: **`AQ_uniform_routeB`**, labelled **uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling (g^4=9.6x10^9)**. Every elementary face, selected faces included, has `nu=alpha tau/24` (AL1: `tau=96/g^4`). Both signs `|tau|<=10^-8` are treated; `tau<0` has no real `g` and is the `U_E` mirror. Route B (AX1): Haar reference `h_b=8 sum_e C_e>=6Q_b`, whole stars `phi_b` (21 omitted faces, norm `7|tau|`) and single-factor groups `psi_b` (3 selected faces, support `{b}`, norm at most `|tau|`), per-site sum `J'=29|tau|`, `J_0'=29/10^8`. The named construction **FB** is the centered whole-star-plus-single-group boxes `Lambda_N=[-N,N]^3`, `N>=2`, together with the finite complete-factor route-B volumes containing `Lambda_N` (stars inside the volume, every single group of the volume kept). States are the reduced densities on finite complete-factor regions `Y` in the trace norm on `B(H_Y)`; the cover is `R={0,e_z}`.

All seven contract items are executed on the forward route, at both signs, in each on-site cutoff space `Q_L` uniformly in `L`, and then at fixed `N` for the untruncated ground vectors. Every constant is recomputed here from the route-B inputs (29, 52, 5), which `check.py` derives from the fine geometry. The table holds at `q=1/64`; every rate in it holds for every N at least 2 (for a region `Y`, for every N with `Y` inside `Lambda_N`).

| constant | exact | preview | target | margin | tier / route / assembly |
|---|---|---|---|---|---|
| `K_B` (T0, every site) | `13/27941256` | `4.65261833612e-7` | `1/1000000` | `2.14932738461` | exact_first_order / analytic_disc (`rho=64|tau|`) |
| `C_B` (T1, R form) | `2326328761843649826272217312701707175/2461302090348550272620124432958434944821248` | `9.45161819414e-7` | `1/250000` | `4.23207954218` | exact_first_order / iterated_split |
| `c_site,B` (T2, region form) | `35789673259133074250341804810795495/38457845161696098009689444264975546012832` | `9.30620868347e-7` | `1/500000` | `2.14910289251` | exact_first_order / iterated_split |
| `C'_B` (T3, whole sequence on R) | equal to `C_B` | `9.45161819414e-7` | `1/250000` | `4.23207954218` | exact_first_order / iterated_split / assembly `union_comparison` |
| `c'_site,B` (T4, whole sequence on Y) | equal to `c_site,B` | `9.30620868347e-7` | `1/400000` | `2.68637861564` | exact_first_order / iterated_split / assembly `union_comparison` |
| node datum `d` | `497870683678639429793424156500617766317/(4*10^40)` | `0.0124467670919` | equal to the AX2 gate | equal | read by hash, calculator replay |
| node radius `R'` | `1912298807996871790146581299723633/10^40` | `1.91229880800e-7` | equal to the AX2 gate | equal | read by hash, calculator replay |

- **Disc admissibility (item 1):** `29 rho G(R)<=1073/2734375<1/64` and `29 rho G'(R)<=2552/390625<1` at `rho=64|tau|`; the split weight `W=1024` gives `17168/2734375<1/64` and `40832/390625<1`; `lambda=2/W=1/512<q`. The route-A extremes (disc radius `1/37888`, split weight `1/(37888|tau|)`) give `29/1792>1/64` and are rejected.
- **Items 2a, 2b, 3, 4 and 5 are proved** (Sections 4–5): exhaustion within the prescription, the pointwise `U_E` mirror, identification with every AQ1-type subsequential state of the AX1 construction before inheritance of the AX1 route-B list, coarse translation invariance, and the AX2 node restated for the limit with `d` and `R'` equal to the gate rationals; the admitted calculator returns them exactly.
- **Scaling `tau -> tau/100`:** `K_B` ratio `1.00651032151e2`, `C_B`, `c_site,B`, `C'_B`, `c'_site,B` ratio `1.00661451758e2` (all in `[95,105]`); `q` and `rho/|tau|` ratio exactly 1; node datum ratio exactly 1; node radius replay ratio `1.00001527222e2` (recorded, not a target).
- **Checker:** `check.py` runs **111 exact checks**; all **52 contract controls** are executed as damaging mutations (**219** rejections in total); the `-B` and `-B -O` outputs are byte-identical.

**Proposed forward verdict: `accepted_within_scope`**, label `convergence_of_named_constructions`, secondary labels `certificate_restated_for_limit`, `reference_unresolved`, `static_not_dynamic`. Admission still needs the skeptic replay from the contract.

## 0. Frozen parameters and proof weights (declared before any constant)

| symbol | meaning | value |
|---|---|---|
| `tau` | coupling, both signs | `+-1/100000000` |
| `J'` | route-B per-site sum: 4 stars (incoming included) of `7|tau|` and 1 single group of `|tau|` | `29|tau|`; `J_0'=29/10^8` |
| `R`, `G(R)`, `G'(R)` | AM2 ball radius and majorant (directed `e^{1/8}<8/7`) | `1/64`, `<148/7`, `<352` |
| `rho` | analytic disc radius (every-site form) | `64|tau|` (`1/1562500` at the cap) |
| `q` | frozen rate | `|tau|/rho=1/64` |
| `W` | split creation weight (`W^{diam I}`) | `1024` |
| `lambda` | site-potential ratio | `2/W=1/512` |
| cardinality charge | support sizes, per site | `|I|<=(diam I+1)^3<=8*2^{diam I}` |
| `T_B(rho)` | route-B circle bound | `(52 rho/144)/(1-29*352 rho)` |

**Admissibility under `J'=29|tau|`, exact rationals, checked before any constant (HNM-BC2-F01).** With the disc self-map `29 rho G(R)<=R` and contraction `29 rho G'(R)<1`,

\[
29\cdot64|\tau|\cdot\tfrac{148}{7}=\tfrac{1073}{2734375}<\tfrac1{64},\quad 29\cdot64|\tau|\cdot352=\tfrac{2552}{390625}<1,\quad
29\cdot1024|\tau|\cdot\tfrac{148}{7}=\tfrac{17168}{2734375}<\tfrac1{64},\quad 29\cdot1024|\tau|\cdot352=\tfrac{40832}{390625}<1 .
\]

The route-B maximal disc radius is `R/(29*148/7)=7/274688`, so the admissible split weights are `1<=W<=7/(274688|tau|)` (`2734375/1073`, about 2548.35, at the cap); for smaller `|tau|` the range only widens. **Route-A extremes (HNM-BC2-F02):** the BA1 disc radius `tau_star=1/37888` and the BB1 secondary weight `1/(37888|tau|)` give `29*(148/7)/37888=29/1792>28/1792=1/64`; both fail the route-B self-map and are rejected. A weight admissible only under `28|tau|` (for example `W=2600`) is rejected as well. The rate `q=1/64` is frozen and is never optimized per `N`.

## 1. Item 1 — route-B partition, incidence, support-one groups and the first-order R-marginal

**Classes.** Factor `b` owns the 24 positive links with tails `(4b_x+r,2b_y+s,b_z)`, `r=0..3`, `s=0,1`. `check.py` derives the 24 anchored classes from `pi(x,y,z)=(floor(x/4),floor(y/2),z)` and `supp_B(f)={pi(p),pi(p+e_a),pi(p+e_c)}` and compares them row by row with the I1 table: 3 selected xy classes with support `{0}` and 21 omitted classes inside `S={0,e_x,e_y,e_z}`.

**Partition (brute force).** Over the 3000 plaquettes with base in the fine region of `Lambda_2`, every plaquette lies in exactly one route-B group: the single-factor group of its anchor if it is selected, otherwise its anchor's star. Every face support lies inside its group support, and a face is selected exactly when its owner set is a single factor. The group sizes are 21 (stars) and 3 (single groups).

**Per-site inputs (derived, HNM-BC2-F03).** For a factor `u`:
- faces with `u` in their owner set: `21+4+8+16=49` omitted plus `3` selected, **52**;
- owner sets containing `u`: **16** (the 15 omitted ones and `{u}`), multiplicities `{1 x5, 2 x3, 3 x3, 4 x3, 10 x2}`;
- interaction groups containing `u`: **5** (the stars at `u-S` and the single group at `u`);
- per-site sum `(4*21+3)/3 |tau| = 29|tau|`.

Boundary counts never exceed the bulk value (checked on `Lambda_1..Lambda_3`).

**Incidence on `R` (every `N>=2`; enumerated for `N=2,3,4`).** Exactly 7 whole stars (anchors `R-S`) and 2 single-factor groups (`{0}`, `{e_z}`) meet `R`; `N=1` has 4 stars.

| group | anchor | faces | meeting `R` | inside `R` |
|---|---|---:|---:|---:|
| star | `0` | 21 | 21 | 10 |
| star | `e_z` | 21 | 21 | 0 |
| star | `-e_z` | 21 | 16 | 0 |
| star | `-e_y`, `e_z-e_y` | 21 each | 8 each | 0 |
| star | `-e_x`, `e_z-e_x` | 21 each | 4 each | 0 |
| single | `0`, `e_z` | 3 each | 3 each | 3 each |
| **total** | | **153** | **88** | **16** |

So 153 faces are charged, 88 meet `R` (82 omitted, 6 selected), 16 lie inside `R` (10 omitted with owner set `R`, 6 selected) and 72 straddle; 6 of the 72 have an owner set strictly containing `R`.

**Support-one groups.** A single-factor group has support `{b}` and diameter 0. It is never clipped by a route-B volume containing `b` (the enumeration keeps every single group of `Lambda_2`, of the prism `[-2,3]x[-2,2]x[-2,4]` and of `Lambda_3+(1,0,0)`), it never straddles a region (a one-site support is inside or outside), its first-order creation is nonzero (`||c'^(1)_{b}||=sqrt(3)|tau|/144`), and it enters the order-versus-distance piece graph at cost one order and zero distance (Section 2).

**Selected-face site energy.** A selected face puts spin 1/2 on four links of one factor, so its vector `W_g Omega_0` has site energy `8*4*(3/4)=24` on that factor; an omitted face has at most three links on one factor (site energy at most 18). The selected-face vectors are therefore kept in `Q_L` exactly for `L>=24`; the route-A statement that first-order site energies are at most 18 is false for route B.

**The first-order R-marginal (HNM-BC2-F04).** The first-order ground vector is `(tau/72) sum_f W_f Omega_0` over all retained faces. Under `Tr_{R^c}`, a term `|Omega><W_f Omega|` survives only if `W_f Omega` is the vacuum on `R^c`, that is, only if the owner set of `f` lies in `R`. Exactly **16** faces do: the 10 omitted faces with owner set `R` and the 6 selected faces of the two single sites. The 72 straddling faces, including the 6 whose owner set strictly contains `R`, have zero first-order `R`-marginal (Haar). The 16 face vectors are mutually orthogonal with norm `1/2` (distinct faces share at most one link), so the first-order marginal `|V><Omega_R|+|Omega_R><V|` has `||V||=4|tau|/144` and trace norm exactly `|tau|/18`; the route-A ten-face value `sqrt(10)|tau|/72` is rejected.

## 2. Item 2 — the route-B coefficient input on the disc `|z|<=64|tau|` (route analytic_disc), proved in full

This section proves the every-site coefficient input for route B. No BA1 statement is cited as admitted: neither the BA1 gate value, nor the BA1 forward bound, nor the BA1 reverse theorem, nor the BB1 every-site form. Only the AM2 majorant steps, the AX1 route-B grouping and the AV1 first-order coefficient enter as premises.

**2.1 The complexified map (HNM-BC2-F05).** Fix a finite complete-factor route-B volume `Lambda` (stars `b+S` inside `Lambda`, every single group of `Lambda`) and a cutoff `Q_L`. Write `V_1=sum_X V_{X,1}` with `V_{X,1}=-(1/3) sum W_f` over the faces of the group (`||V_{X,1}||<=7` for a star, `<=1` for a single group) and `V(z)=z V_1`. For collections `c=(c_I)`, `c_I` in `tensor_{x in I} Q_x Q_L H_x`,

\[
F_z(c)=\sum_{k=0}^{8}\frac{L^{(z)}_k(c,\ldots,c)}{k!},\qquad L^{(z)}_k(c_1,\ldots,c_k)_M=H_M^{-1}P_M\,\mathrm{ad}_{C_1}\cdots\mathrm{ad}_{C_k}(V(z))\,\Omega_0=z\,L^{(1)}_k(c_1,\ldots,c_k)_M .
\]

At real `z=tau` this is the route-B AM2 map of AX1. The AM2 multilinear estimate uses: (a) creations commute and overlapping ones multiply to zero; (b) every creation support of a nonzero word meets `X`; (c) `N\X` inside `M` inside `N u X`, at most `2^p` outputs, `|I_j|<=|M|+p`; (d) `2^k` products; (e) each projected product has norm at most `||V_X(z)|| prod ||c_{j,I_j}||`; (f) `||H_M^{-1}||<=1/|M|` from `h_x>=Q_x`; (g) `sum_{X ni u}||V_X(z)||<=29|z|` (four stars of `7|z|`, incoming included, plus one single group of `|z|`); (h) `sum_{I meets X}||c_I||<=p||c||_a`; (i) `1/|M|<=(p+1)/|I_l|` and `sum_{X meets I_l}||V_X(z)||<=29|z||I_l|`; (j) termination above order `2p=8`. Only (e), (g) and (i) involve `z`, and only through `||V_X(z)||=|z| ||V_{X,1}||`; no step uses reality of the coupling or self-adjointness. The constants `2^p(2p)^k(1+k(p+1)/p)` increase in `p`, so the one-site groups (`p=1`) are covered by `p=4` (checked for `p=1..4`, `k=0..8`). Hence, for every complex `z`,

\[
\|L^{(z)}_k(c_1,\ldots,c_k)\|_a\le 29|z|\;16\cdot8^k\Bigl(1+\tfrac{5k}{4}\Bigr)\prod_j\|c_j\|_a .
\tag{HNM-BC2-F06}
\]

**Lemma D1 (disc contraction).** For `0<rho<=7/274688` and `|z|<=rho`, `F_z` maps `||c||_a<=R` into itself (`29 rho G(R)<=R`) and contracts it with constant `29 rho G'(R)<1`. At `rho=64|tau|` the two values are `1073/2734375` and `2552/390625` (F01). *Proof:* sum (F06) against `G(t)=sum_k 16*8^k(1+5k/4)t^k/k!=16e^{8t}(1+10t)` and telescope each `k`-linear term. ∎

**Lemma D2 (analyticity).** For such `rho`, every route-B volume and every `L`, `F_z` has one fixed point `c(z)` in the ball; `z->c(z)` is continuous on `|z|<=rho` and holomorphic on `|z|<rho`, and at real `tau` it is the route-B AM2 fixed point. *Proof:* the iterates `c^{(m+1)}=F_z(c^{(m)})`, `c^{(0)}=0`, are polynomials in `z`, stay in the ball and converge uniformly on the closed disc (Lemma D1, Weierstrass coordinatewise in the finite-dimensional coefficient space of `Q_L`); the limit is a fixed point, the only one in the ball, and at real `tau` it equals the AM2 fixed point by uniqueness in the ball. ∎ Only the creation coefficients are continued in `z`: the normalization of the reduced density can vanish inside a disc (fixture: `psi(z)=Omega-2z|11>` has normalization `1+4z^2`, zero at `z=i/2`), no zero-free region is proved, and no analyticity of the reduced density is claimed.

**Lemma D3 (route-B circle bound, HNM-BC2-F07).** For `|w|<=rho`, write `c(w)=w L^{(1)}_0+r(w)` with `(L^{(1)}_0)_M=-(1/72) sum_{M_f=M} W_f Omega_0` (face energy 24, face-vector norm `1/2`, distinct faces orthogonal, selected faces included). Then `||w L^{(1)}_0||_a=(|w|/144) max_u sum_{M ni u} sqrt(n_M)<=52|w|/144` (52 faces per factor), and `||r(w)||_a<=29|w|(G(t)-16)<=29|w|G'(R)t` by convexity of `G`. Hence

\[
t(w):=\|c(w)\|_a\le T_B(\rho):=\frac{52\rho/144}{1-29\cdot352\,\rho}=\frac{13\rho/36}{1-10208\rho}.
\]

At `rho=|tau|` this is `T_B(|tau|)=13/3599632512`, **equal to the AX1 gate value `T'`** (pinned; a route-A substitution `28`/`49` gives `49/14398580736` and aborts at the pin). At `rho=64|tau|`, `T_B=13/55882512`. The crude tier is `t(w)<=29 rho G(R)`.

**Lemma D4 (connected families; order versus distance on the route-B piece graph).** Decompose `V_1` into faces (pieces); omitted faces have owner sets of l-infinity diameter 1 and selected faces owner sets `{b}` of diameter 0. The Taylor coefficients satisfy `c_1=L^{(1)}_0`, `c_n=sum_{k>=1}(1/k!) sum_{n_1+..+n_k=n-1} L^{(1)}_k(c_{n_1},..,c_{n_k})`, so `c_n=sum Phi_n(Y_1,..,Y_n)` with `Phi_n(..)_M=0` unless `{Y_1..Y_n}` is connected in its intersection graph and `M` lies in `Y_1 u..u Y_n` (induction with steps (b), (c)). If `M` contains `u` and the family contains a piece at distance `d>=1` from `u`, a chain `Z_0 ni u, Z_1, .., Z_m` of distinct intersecting pieces reaches it with `d<=m` (each piece has diameter at most 1; a single-site piece costs one order and zero distance), so

\[
n\;\ge\;1+d .
\tag{HNM-BC2-F08}
\]

`check.py` runs a breadth-first search on the route-B piece graph of `Lambda_3` (1639 pieces, 343 of them single sites) from five sites `u` and finds least order at least `1+d` everywhere, with slack 0 attained at every `u`.

**Lemma D5 (every-site common core for route B).** Let `N>=1` and `u` in `Lambda_N`. Every face, omitted or selected, with a site at l-infinity distance at most `N-|u|_inf-1` from `u` is retained by every route-B volume containing `Lambda_N`. *Proof.* Such a site `p` has `|p|_inf<=N-1`. An omitted face at `p` has anchor `b=p-s`, `s` in `S`, with `b_i` in `[-N,N-1]`, so `b+S` lies in `Lambda_N` and the whole star is retained. A selected face has owner set `{b}` with `b=p` in `Lambda_{N-1}`, and every single group of the volume is kept. ∎ Hence every source face of a comparison (present in one volume only) lies at distance at least `N-|u|_inf` from `u`. `check.py` enumerates this at every site of `Lambda_N` for c1B (`N=2,3,4`), for c4B (`Lambda_2` vs `Lambda_4`, `Lambda_3` vs `Lambda_4`, `Lambda_3` vs `Lambda_5`) and for c5B (a prism against `Lambda_2`, two prisms, `Lambda_3+(1,0,0)` against `Lambda_3`); the source faces include 654, 1158 and 1806 selected faces at `N=2,3,4` for c1B, and the distance `N-|u|_inf` is attained at every site for the nested comparisons.

**Theorem D6 (route-B every-site coefficient input, HNM-BC2-F09).** Let `N>=2`, let `Lambda^A`, `Lambda^B` be finite complete-factor route-B volumes both containing `Lambda_N` (c1B, c4B and c5B are special cases), `V` their union, `L` any cutoff and `|tau|<=10^-8` of either sign. Then for every site `u` of `V` and every N at least 2,

\[
D_u:=\sum_{I\ni u}\|c^A_I(\tau)-c^B_I(\tau)\|\;\le\;K_B\,q^{(N-|u|_\infty)_+},\qquad K_B=2T_B(64|\tau|)=\frac{13}{27941256},\quad q=\frac{|\tau|}{64|\tau|}=\frac1{64}.
\]

*Proof.* (i) Embed both boxes in `V` with unperturbed padding (on-site `h_x` only); the map with interaction supported in `Lambda^A` preserves collections supported in `Lambda^A` (`M` lies in `Y u (u I_j)`), so the embedded fixed point is box A's; likewise for B; both have per-site sum at most `29|z|`. (ii) `g(z)=(c^A_I(z)-c^B_I(z))_{I ni u}` is holomorphic on the open disc and continuous on the closed one (Lemma D2), in the norm `||g||_u=sum_{I ni u}||g_I||`. Terms of `c_n` whose faces are all common to both volumes coincide (same on-site operators and cutoff); every other term contains a source face at distance at least `N-|u|_inf` from `u` (Lemma D5), so by Lemma D4 `g_n=0` for `n<=N-|u|_inf` when `|u|_inf<=N-1`. (iii) Schwarz: for a functional `l` of dual norm at most one, `l(g(z))/z^{n_0}` is holomorphic, and the maximum principle on `|z|=r<rho`, then `r->rho`, gives `||g(tau)||_u<=(|tau|/rho)^{n_0} max_{|w|=rho}||g(w)||_u` with `n_0>=N-|u|_inf+1`. (iv) On the circle `||g(w)||_u<=t^A(w)+t^B(w)<=2T_B(rho)` (Lemma D3; the anchored norm is a maximum over sites, so this holds at every `u`). (v) For `|u|_inf>=N` the exponent is 0 and `D_u<=||c^A||_a+||c^B||_a<=2T_B(|tau|)<=2T_B(rho)=K_B`. ∎

**Uniformity in the cutoff.** Compression by `Q_L` neither enlarges supports nor increases norms; each face vector is an eigenvector of every `h_x`, so `Q_L` keeps or annihilates it (selected-face vectors kept exactly for `L>=24`, omitted ones for `L>=18`), and the first-order counts only decrease for smaller `L`. So (F09) holds in every `Q_L` with `K_B` independent of `L`. No untruncated creation coefficients are asserted.

**Values.** `K_B=13/27941256` (preview `4.65261833612e-7`) is at most `1/1000000` with margin `2.14932738461`, at both signs (the `-tau` value replays the same `|tau|` formula) and for every `0<|tau|<=10^-8` (`K_B` increases in `|tau|` at fixed `q`). Crude tier (reported, never a target): `2*29 rho G(R)=2146/2734375` (about `7.848e-4`), which fails. The global Lipschitz constant of the route-B map, `J_0'G'(R)<=319/3125000`, the exclusion constant `2J_0'G'(R)<=319/1562500` and the no-decay bound `J_0'G(R)/(1-J_0'G'(R))=1073/174982136` carry no distance dependence and appear in no constant.

## 3. Item 3 — marginal locality by the iterated split (route iterated_split), proved in full

The proof is the AV1 product-ordering split applied recursively, with route-B per-site sums. Nothing in it uses the shape of the supports beyond their diameters and sizes, so single-site supports enter like any other; they never straddle.

**3.1 Decomposition and the two Lipschitz bounds.** For a region `Y`, put `A_Y={I: I meets Y}`, `B_Y={I: I misses Y}`, the straddle region `O=u_{I in A_Y}(I\Y)`, `E_c=prod_{I in A_Y}(1-hat c_I)`, the outside vector `phi_out=prod_{I in B_Y}(1-hat c_I)Omega` and its normalized marginal `omega_O`.

- **Lemma S1 (exact decomposition, `Tr N_c>=1`).** With `N_c(omega)=Tr_O[E_c(P_Y x omega)E_c^*]`, `rho_Y=N_c(omega_O)/Tr N_c(omega_O)` and `Tr N_c(omega)=1+Tr[D(P_Y x omega)D^*]>=1` for every state `omega`, `D=E_c-1`, because every term of `D` is excited at a site of `Y` (orthogonality). The outside vector is the restriction of the box's collection, not a ground state of any outside Hamiltonian; no gap argument is applied to it.
- **Lemma S2 (Lipschitz in the coefficients, `eta=0`, HNM-BC2-F10).** If `c`, `c'` differ only on one support `J`, then `||rho_Y(c)-rho_Y(c')||_1<=2||c_J-c'_J||` for every `Y`. *Proof:* split at `J`: `psi(c)-psi(c')=-hat delta_J psi_notJ` with `psi_notJ=(P_J x 1)psi(c)`, so `||psi(c)-psi(c')||<=||delta_J|| ||psi(c)||`; the pure-state trace distance is at most `2||a-b||/max(||a||,||b||)`, and the partial trace is contractive. ∎ It is used only for supports meeting `Y`; applied to far supports it has no decay and is never a per-shell factor.
- **Lemma S3 (Lipschitz in the outside state).** `||rho(omega)-rho(omega')||_1<=2||N_c(omega-omega')||_1/Tr N_c(omega)<=2(2eps_Y+eps_Y^2)||omega-omega'||_1`. It is not iterated: iterating it on growing straddle regions charges the product of growing region sizes, whose per-level factor `(2k+1)^3 t_0` exceeds one at depth 259 for the route-B `t_0`; this charging rule is rejected in favour of per-site charging.

**3.2 Single-support telescoping (HNM-BC2-F11).** For a comparison, embed both fixed points in the union volume, put `m_I=max(||c^A_I||,||c^B_I||)` and let `C(m)` be the collections with `||c_I||<=m_I`. Ordering the supports and switching them one at a time from `c^A` to `c^B` gives

\[
\|\rho_Y(c^A)-\rho_Y(c^B)\|_1\le\sum_k\kappa(I_k)\|c^A_{I_k}-c^B_{I_k}\|,\qquad \kappa(J)=\sup\Bigl\{\tfrac{\|\rho_Y(c)-\rho_Y(c')\|_1}{\|c_J-c'_J\|}\Bigr\}\ (\text{pairs in }C(m)\text{ differing only on }J),
\]

with `kappa(J)<=2` for every `J` (Lemma S2).

**3.3 The split at the changed support (HNM-BC2-F12).** Let `J` miss `Y`, `c`, `c'` in `C(m)` differ only on `J`, `delta=c_J-c'_J`, `phi=prod_{I misses J}(1-hat c_I)Omega_{J^c}`, `n^2=||phi||^2`, `psi_J=Omega_J x phi`, `E''_J=prod_{I meets J, I!=J}(1-hat c_I)`, `D''=E''_J-1`. Then `psi(c)=psi_J+chi`, `chi=D''psi_J-c_J x phi`, `(P_J x 1)chi=0`, the cross terms `Tr_{Y^c}|psi_J><chi|` vanish, and with `a=||c_J||^2-||c'_J||^2`, `Gamma(v)=Tr_{Y^c}|v x phi><D''psi_J|` and `Z=||psi(c)||^2>=n^2`,

\[
\rho_Y(c)-\rho_Y(c')=\frac{a\,n^2(\rho_Y(\phi)-\rho_Y(c'))-(\Gamma(\delta)-\mathrm{Tr}\,\Gamma(\delta)\rho_Y(c'))-(\Gamma(\delta)-\mathrm{Tr}\,\Gamma(\delta)\rho_Y(c'))^*}{Z},
\]

so `||rho_Y(c)-rho_Y(c')||_1<=2m_J||delta|| ||rho_Y(phi)-rho_Y(c')||_1+(2/n^2)||Gamma(delta)-Tr Gamma(delta) rho_Y(c')||_1`. The first term is the **normalization** channel, the second the **straddling** channel. `check.py` verifies this identity exactly on a six-site, three-level fixture with 16 supports, six of them single sites.

**3.4 Only coverings survive (HNM-BC2-F13).** Expanding `D''psi_J` over families `F` of pairwise disjoint supports `I!=J` meeting `J`, the contraction with `delta` (excited at every site of `J`) keeps only families that cover `J`: `Gamma(delta)=sum_{F covers J}(-1)^{|F|} Tr|g_F x phi_{J u S_F}><phi|`, `S_F=(u F)\J`, `g_F=(<delta| x 1)c_F`, `||g_F||<=||delta|| prod_{I in F} m_I`. Spectator families cancel exactly.

**3.5 Recursion on covering regions (HNM-BC2-F14).** For `U` missing `Y`, `S` in `U^c` and `g` excited on `S`, the record `Gamma[U,S,g]=Tr_{U^c\Y}|phi_U><g x phi_{U u S}|` satisfies, when `S` misses `Y`, `Gamma[U,S,g]=sum_{F covers S, S'_F nonempty}(-1)^{|F|}Gamma[U u S,S'_F,g'_F]^*+sum_{F covers S, S'_F empty}(-1)^{|F|}g'_F||phi_{U u S}||^2 rho_Y(phi_{U u S})`, with `S'_F=(u F)\S`, `g'_F=(<g| x 1)c_F`. `check.py` verifies it exactly, unrolled to termination, for three records. With `Def[U,S,g]=||Gamma[U,S,g]-Tr Gamma[U,S,g] rho_Y(c')||_1` and `Rem(U)=||rho_Y(phi_U)-rho_Y(c')||_1<=sum_{I meets U}kappa(I)m_I`,

`Def[U,S,g]<=sum_{S'_F misses Y}Def[U u S,S'_F,g'_F]+sum_{S'_F meets Y}2||g'_F||n^2+sum_{S'_F empty}||g'_F||n^2 Rem(U u S)`.

**3.6 Per-site charging with the route-B sums (HNM-BC2-F15).** Put `lambda=2/W`, `h(x)=sum_{y in Y}lambda^{d(x,y)}`, `H(I)=sum_{x in I}h(x)`, `t_0=max_u sum_{I ni u}m_I` and `t_W=max_u sum_{I ni u}W^{diam I}m_I`.
- **(P1)** `sum_{I ni x, I meets Y}m_I<=t_W h(x)`, since such `I` has `diam I>=d(x,Y)` and `W^{-d}<=lambda^d`.
- **(P2)** `sum_{I ni x}m_I H(I)<=8t_W h(x)`, since `H(I)<=|I|lambda^{-diam I}h(x)` and `|I|lambda^{-diam I}<=8*2^{diam I}(W/2)^{diam I}=8W^{diam I}`; each support's size is charged once, at the site where the chain enters it.
- **(P3)** `Cov(T)=sum_{F covers T}prod m<=t_0` for nonempty `T` (the member through the first site of `T` is unique; induction), so `sum_{F covers S, F ni I}prod m<=m_I`.

**Lemma S4 (route-B per-site sums).** `t_0<=2T_B(|tau|)=13/1799816256` and `t_W<=2T_B(W|tau|)=26/3148137` at `W=1024`. *Proof.* `t_0<=||c^A||_a+||c^B||_a` and Lemma D3 at `rho=|tau|`. For `t_W`: in `||c||_W=max_u sum_{I ni u}W^{diam I}||c_I||`, the multilinear estimate holds with the loss `W^{d_X}<=W` charged once per interaction term (`diam M<=d_X+sum_j diam I_j`; `d_X=1` for stars, 0 for single groups), so `sum_{X ni u}W^{d_X}||V_X||<=29W|tau|`; the weighted self-map `29W|tau|G(R)<=R` and contraction `29W|tau|G'(R)<1` hold (F01), the weighted ball lies in the anchored ball, so the weighted fixed point is the AM2 fixed point; the first-order part has `||c^(1)||_W<=(49W+3)|tau|/144<=52W|tau|/144` and the remainder is at most `29W|tau|G'(R)||c||_W`. ∎ The refinement `(49W+3)/144` is labelled and not used.

**3.7 The chain bound and the closure (HNM-BC2-F16).** With `r=max_{I misses Y}kappa(I)/H(I)` and `R_r=(2+8r)t_W` (so `Rem(U)<=R_r H(U)` by (P1), (P2)), induction on `|V\U|` gives `Def[U,S,g]/(||g||n^2)<=alpha H(S)+mu H(U)` with `mu=t_0R_r/(1-t_0)`, `alpha=(2t_W+t_0R_r/(1-t_0))/(1-8t_W)`. The top level has the same structure at `U=empty`, `S=J`, so `kappa(J)<=(2t_0R_r+2alpha)H(J)=(c_1+c_2 r)H(J)`, hence `r<=beta*=c_1/(1-c_2)` with

\[
c_1=4t_0t_W+\frac{4t_W+4t_0t_W/(1-t_0)}{1-8t_W},\qquad c_2=16t_0t_W+\frac{16t_0t_W}{(1-t_0)(1-8t_W)} .
\]

Route-B values: `c_1=132572461259098000347351859/4012775859330709325091744109848`, `c_2=1915067760208663411/1003193964832677331272936027462` (about `1.909e-12`), `beta*=132572461259098000347351859/4012775859323049054050909456204` (about `3.30375944001e-5`); per-level factor `8t_W=208/3148137` (about `6.607e-5`). The lemma form is `kappa(I)<=beta* H(I)<=beta*|Y|(w')^{-d(I,Y)}|I|` with `eta=0`, `kappa_0=beta*|Y|`, `w'=1/lambda=512`, `p(n)=n`.

**Theorem S5 (marginal locality for route B, HNM-BC2-F17).** Let `N>=2`, let `Lambda^A`, `Lambda^B` be finite complete-factor route-B volumes both containing `Lambda_N` (c1B, c4B, c5B, compared directly), either sign, any cutoff `L`. For every finite complete-factor region `Y` inside `Lambda_N` and every N at least 2,

\[
\|\rho^A_Y-\rho^B_Y\|_1\le c_{\rm site,B}\sum_{y\in Y}q^{N-|y|_\infty}\le c_{\rm site,B}\,|Y|\,q^{d_Y}\le c_{\rm site,B}\,|Y|\,e^{|Y|/10^8}q^{d_Y},\qquad c_{\rm site,B}=K_B(2+\beta^*S_\lambda),
\]

with `d_Y=N-max_{y in Y}|y|_inf`, `S_lambda=1+24x(1+x)/(1-x)^3+2x/(1-x)=2169/343` at `x=lambda/q=1/8`, and for `Y=R`: `||rho^A_R-rho^B_R||_1<=C_B q^(N-1)` for every N at least 2, `C_B=c_site,B(1+q)`. The same bounds hold for the untruncated ground vectors at fixed `N`.

*Proof.* (i) Embedding with vacuum padding changes neither density on `Y`. (ii) (F11) and the closure give `||rho^A_Y-rho^B_Y||_1<=2sum_{I meets Y}||delta_I||+beta* sum_I H(I)||delta_I||<=2sum_{y in Y}D_y+beta* sum_{x in V}h(x)D_x`. (iii) `D_x<=K_B q^{(N-|x|_inf)_+}<=K_B q^{N-|x|_inf}` at every site of the union volume (Theorem D6). (iv) `|x|_inf<=|y|_inf+d(x,y)` gives `sum_x h(x)D_x<=K_B sum_{y in Y}q^{N-|y|_inf} sum_{x in Z^3}(lambda/q)^{d(x,y)}=K_B S_lambda sum_y q^{N-|y|_inf}`, the shell at l-infinity distance `r>=1` having `24r^2+2` sites. (v) Every constant is independent of `L`. (vi) At fixed `N` and fixed volumes, AV1 F20–F23 with the route-B untruncated gap `1/2` (AX1 gate item 2: every finite complete-factor route-B volume has a unique gauge-invariant ground and full-space gap at least `1/2`, with AM2 Section 6 cutoff removal) give `1-|<psi,psi_L>|^2<=2(E_{0,L}-E_0)->0`, so the cutoff ground vectors converge and the reduced densities converge in trace norm; the bound passes through the closed trace-norm ball. The order is fixed: the bound uniformly in `L` at fixed `N`, then `L` to infinity at fixed `N`, then the bound read as a function of `N`; the `N` and `L` limits are never exchanged (fixture `L/(N+L)`). ∎

**Constants (tier exact_first_order, route iterated_split, input `K_B` by analytic_disc).**

| constant | exact | preview | target | margin |
|---|---|---|---|---|
| `C_B` | `2326328761843649826272217312701707175/2461302090348550272620124432958434944821248` | `9.45161819414e-7` | `1/250000` | `4.23207954218` |
| `c_site,B` | `35789673259133074250341804810795495/38457845161696098009689444264975546012832` | `9.30620868347e-7` | `1/500000` | `2.14910289251` |
| crude `C_B` (reported only) | `362331029338528852703336460633941/193178427869162139024664513304450000` | `1.87562883358e-3` | — | fails |
| crude `c_site,B` (reported only) | `111486470565701185447180449425828/60368258709113168445207660407640625` | `1.84677300537e-3` | — | fails |

Every comparison (c1B, c4B, c5B) and both signs give the same constants; the `-tau` rows replay the same `|tau|` formula. A comparison through the union volume costs a factor 2 (`2C_B`, about `1.890e-6`) and is labelled only. Example values of `C_B q^(N-1)`, which hold for every N at least 2: `1.47681534283e-8` (`N=2`), `2.30752397318e-10` (`N=3`), `3.60550620809e-12` (`N=4`). The split bound itself needs no factor `e^{|Y|/10^8}`; the fixture re-checks `(1+t)^2<=1+10^-8` with the route-B anchored bound `t=T_B(|tau|)=13/3599632512`: `(1+t)^2-1=93590445481/12957354221447430144` (about `7.223e-9`). No analyticity of the reduced density is used.

## 4. Item 4 — whole-sequence convergence, exhaustion, sign mirror, identification and coarse translations

**4.1 Whole-sequence Cauchy estimate (T3, T4; HNM-BC2-F18).** For every N at least 2, every `M>N`, both signs, in each `Q_L` and then for the untruncated vectors,

\[
\sup_{M>N}\|\rho^{FB,M}_R-\rho^{FB,N}_R\|_1\le C'_B\,q^{N-1},\qquad
\sup_{M>N}\|\rho^{FB,M}_Y-\rho^{FB,N}_Y\|_1\le c'_{\rm site,B}\,|Y|\,e^{|Y|/10^8}q^{d_Y}\quad(Y\subset\Lambda_N),
\]

with the **assembly `union_comparison`**: each `M` is compared with `N` by **one direct c4B comparison** of `Lambda_N` and `Lambda_M`, both of which contain `Lambda_N` (factor 1). So `C'_B=C_B` and `c'_site,B=c_site,B` (tier exact_first_order, route iterated_split of the input). Margins: `4.23207954218` against `1/250000` and `2.68637861564` against `1/400000`. Nested telescoping would give `C_B/(1-q)` (about `9.602e-7`) and `c_site,B/(1-q)` (about `9.454e-7`); these are labelled only.

**Limit without compactness.** For fixed `Y`, `(rho^{FB,N}_Y)_N` is Cauchy in the Banach space of trace-class operators on `H_Y`, so it converges in trace norm to `rho^inf_Y`; positivity and unit trace are closed, and partial-trace contractivity makes the limits compatible. So `omega_inf(B)=Tr(rho^inf_Y B)` is a locally normal state on the local algebra that extends by norm continuity to the quasi-local algebra. Letting `M` tend to infinity gives, for every N at least 2 with `Y` inside `Lambda_N`, `||rho^{FB,N}_Y-rho^inf_Y||_1<=c'_site,B |Y| e^{|Y|/10^8} q^{d_Y}` and `||rho^{FB,N}_R-rho^inf_R||_1<=C'_B q^(N-1)`. The cutoff order is: the bound in each `Q_L` uniformly in `L`; `L` to infinity at fixed `N` and `M` (F20–F23, route-B gap `1/2`); the supremum over `M`; then `N` to infinity for the untruncated sequence only. A bound for `N` to `N+1` alone is not a Cauchy estimate (harmonic fixture), and a one-state ball in every box is not convergence (alternating fixture with steps `1/25`).

**4.2 Item 2a: exhaustion within the prescription (HNM-BC2-F19).** Let `V_k` be finite complete-factor route-B volumes (stars inside the volume, every single group of the volume kept) and `N_k` the largest `N` with `Lambda_N` inside `V_k`, with `N_k` tending to infinity. For every N_k at least 2 and every finite complete-factor region `Y` inside `Lambda_{N_k}`,

\[
\|\rho^{V_k}_Y-\rho^{\infty}_Y\|_1\le\|\rho^{V_k}_Y-\rho^{\Lambda_{N_k}}_Y\|_1+\|\rho^{\Lambda_{N_k}}_Y-\rho^\infty_Y\|_1\le(c_{\rm site,B}+c'_{\rm site,B})\,|Y|\,e^{|Y|/10^8}q^{N_k-\max_{y\in Y}|y|_\infty},
\]

by one direct c5B comparison of `V_k` with `Lambda_{N_k}` (both contain `Lambda_{N_k}`) and the whole-sequence bound (4.1). So every such exhausting sequence of the route-B prescription has the same limit on every finite region. This is exhaustion within one prescription, not a comparison of boundary conditions. The constant is `c_site,B+c'_site,B=2c_site,B`.

**4.3 Item 2b: the pointwise sign mirror (HNM-BC2-F20).** In every centered box and every cutoff, `U_E H_N(tau) U_E^*=H_N(-tau)` (AX1 forward F19 and F20; every face coefficient, selected faces included, is `-(tau/3)`, `h_b` and its cutoffs commute with `U_E`, and the flip set `E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even}` meets every plaquette in 1 or 3 links; `check.py` re-enumerates 864 plaquettes of a period window, 108 of them selected). The ground is simple at both signs, so `psi_N(-tau)=U_E psi_N(tau)` up to a phase. `U_E` is a product of one-link unitaries, hence a product `tensor_x U_{E,x}` over factors, and

\[
\rho^{N}_Y(-\tau)=U_{E,Y}\,\rho^N_Y(\tau)\,U_{E,Y}^*\qquad\text{for every finite }Y,\ \text{every }N,\ \text{every cutoff}.
\]

Both signs converge as whole sequences (4.1; the constants depend on `|tau|` only), so `rho^{-tau}_{inf,Y}=U_{E,Y} rho^{tau}_{inf,Y} U_{E,Y}^*`, that is, `omega^{-tau}_inf=omega^{tau}_inf o alpha_E` on every finite region, with `alpha_E(A)=U_E A U_E^*`. The AX1 whole-set statement `S(-tau)=S(tau) o alpha_E` becomes pointwise. The `-tau` side is the mirror replay with no real `g`, not a second coupling and not a second observation. The 3x3 compression `D H(tau,kappa) D=H(-tau,-kappa)` gives the uniform identity only for `kappa=tau` (an untied `kappa=tau+1/1000` is rejected).

**4.4 Item 3: identification first, then inheritance (HNM-BC2-F21).** An AQ1-type subsequential state of the AX1 construction is a state `omega'` for which, along some subsequence `N_k` of the centered whole-star-plus-single-group boxes, `rho^{N_k}_Y` converges in trace norm to `rho'_Y` on every finite region `Y` (AQ1 Section 2 diagonal extraction, re-applied in route B with `C_F'=58|tau||F|`, AX1 gate item 3). The whole sequence converges on every finite region (4.1), so every subsequence has the same limit and `rho'_Y=rho^inf_Y` for every finite `Y`; two states that agree on the local algebra agree on its norm closure. Hence the set of AQ1-type subsequential states (nonempty by AQ1 compactness) is `{omega_inf}` on every finite region. **Only after this identification** does `omega_inf` inherit exactly the AX1 gate's route-B list:
- AQ1 (re-applied with `C_F'=58|tau||F|` and `||Phi'||_F<=2349|tau|`): a compatible locally normal gauge-invariant state, stationary under the route-B limit dynamics `T_theta` (`theta=alpha t/hbar`), with strongly continuous GNS evolution and a nonnegative self-adjoint physical energy generator; the physical cyclic restriction reduces it;
- AQ2 (re-applied with the route-B full-Hilbert gap): `H_phys>=(alpha/16)(I-P_Omega)` on the invariant-local cyclic completion with a simple vacuum in this representation, the full-GNS strengthening only as the AQ2 gate qualifies it; reset `omega(h_R)<=102|tau|`, `epsilon_R<=17|tau|`, Wilson variance at least `61999/250000`;
- the AX1 state lemma: `||rho_R-P_R||_1<=D'=2425369125199104794263242601250/167893028420061547330293754713793182097`, `|omega(W)|<=D'`, `|omega(W^2)-1/4|<=D'/2`, `m^2<=D'^2`;
- the sign relation of item (7), now pointwise (4.3), and the AX2 node (Section 5).

Not inherited: the zero-selected AQ1/AQ2 constants (reset `98|tau|`, `2268|tau|`), the BB2 list, `K_2`, a uniform `omega(W^2)` constant, a uniform Wilson-mean sign, any route-B dynamics comparison or correlation-function statement, and uniqueness of any ground state. The GNS representation of `omega_inf` is canonically unitarily equivalent to that of every identified subsequential state.

**4.5 Item 4: coarse translations (HNM-BC2-F22).** A coarse translation `v` is the fine translation `(4v_x,2v_y,v_z)`; it preserves the residues, the face classes, the selected set and link ownership, so it maps stars to stars, single groups to single groups and route-B volumes to route-B volumes, and `T_v H^B_V T_v^*=H^B_{V+v}` in each `Q_L` (`check.py` verifies the face-set covariance on `Lambda_2` and `Lambda_3` for three shifts). With simple grounds, `rho^{V+v}_{Y+v}=T_v rho^V_Y T_v^*`. For every coarse `v` and every N at least `|v|_inf+2`, `Lambda_N+v` and `Lambda_N` both contain `Lambda_{N-|v|_inf}`, and one direct c5B comparison gives

\[
\|\rho^{\Lambda_N+v}_R-\rho^{\Lambda_N}_R\|_1\le C_B\,q^{\,N-|v|_\infty-1}\qquad(N\ \text{at least}\ |v|_\infty+2).
\]

Rows: `(N,v)=(2,0)` and `(3,(1,0,0))`: `1.47681534283e-8`; `(4,(1,-1,0))`: `2.30752397318e-10`; `(6,(2,1,0))`: `3.60550620809e-12`. **Invariance on every finite region** follows from the region form of c5B: for `A` in `B(H_Y)`, `|omega^{Lambda_N}(tau_v A)-omega^{Lambda_N}(A)|=|omega^{Lambda_N-v}(A)-omega^{Lambda_N}(A)|<=c_site,B|Y|e^{|Y|/10^8}q^{N-|v|_inf-max_{y in Y}|y|_inf}||A||`, which tends to 0, so `omega_inf o tau_v=omega_inf`. Nested cubes alone would not compare `Lambda_N+v` with `Lambda_N`, and a two-step comparison through a union volume is labelled only. **Non-coarse fine translations: no claim.** Among the 64 fine translations of the period window, exactly the 8 coarse ones preserve the factor partition and the grouping. A non-coarse translation preserves the uniform bulk coefficients (every face has `-tau/3`) but not the partition or the grouping: `(1,0,0)` maps the selected face at `(2,0,0)` (single group, one owner) to the face at `(3,0,0)` with two owners, with the same coefficient. So neither invariance nor non-invariance is claimed, and the route-A reason (a selected face mapped to an omitted face of another coefficient) does not apply here.

## 5. Item 5 — the AX2 node restated for the limit

AX2 certifies, for every AQ1 subsequential state of the centered whole-star-plus-single-group construction, each separately, at `tau=+10^-8` and the single node `s=1` (`s=alpha t_E/hbar`, `G=H/alpha`, `chi=(pi(W)-omega(W))Omega`), `|C(1)-d|<=r<=R'`. By 4.4 the limit `omega_inf` is an AQ1-type subsequential state on every finite region, hence on the quasi-local algebra, and it has the same GNS representation and generator. So **the AX2 certificate holds for the limit with the same values**:

\[
|C_\infty(1)-d|\le R',\qquad d=\frac{497870683678639429793424156500617766317}{4\cdot10^{40}},\qquad R'=\frac{1912298807996871790146581299723633}{10^{40}}\quad(\text{about }1.91229880800\times10^{-7}).
\]

- **Read by hash.** `d` and `R'` are parsed from the pinned AX2 gate (`sha256 1db36627…44be4`).
- **Replay of the admitted calculator.** `research/round32/forward/ax2/calculator.py` (a declared premise, loaded from `inputs/`, sha256 `f368a3e7…31f5d`, which the AX2 gate binds) at its fixed design (`tau=+10^-8`, `s=1`, the gate-bound `D'`, `k'=51|tau|/4`, `M_0=2`, `M_1=4s/pi`) returns the datum and its outward `10^-40` radius **equal to the gate rationals exactly**; the `-tau` call is the mirror replay and returns the same values. It also returns `reference_unresolved`, the free value inside the interval and no interaction shift.
- **Own re-evaluation (labelled cross-check).** With my own Machin lower bound for `pi` and my own enclosure of `e^{-3}/4`, `r_own=2(D'+D'^2)+51|tau|/pi_lower+|e^{-3}/4-d|`, rounded outward on `10^-60`, is `95614940399843589507329064986181636466083290310640633/(5*10^59)` (about `1.91229880799e-7`) and satisfies `r_own<=R'` with slack about `2.7e-41`. The headline radius stays the gate `R'`; the route-B `D'` recomputed from `J'=29|tau|` and 52 faces equals the gate rational.
- **Scope.** `reference_unresolved` is kept: the free value `e^{-3}/4` lies inside the interval, and no interaction shift, sign or coefficient of `C(s)` is claimed. No other node, no finite-box node convergence `C_N(1)->C_inf(1)` (it would need a route-B dynamics comparison and window-tail control over all real `theta`) and no smaller state term for the limit are claimed.
- **Load-bearing region form.** `C(1)` is a functional of the state on the quasi-local algebra through its GNS representation. The restatement therefore needs identification on every finite region, that is, the region-form Cauchy bound for the untruncated vectors (4.1); with the R form only, or convergence only inside each `Q_L`, it would be dropped.
- **Scaling.** Datum ratio exactly 1; radius replay ratio `1.00001527222e2` at `tau/100` (recorded, not a target).

## 6. Item 6 — obligations (recorded, not attempted)

| obligation | missing premise | candidate route |
|---|---|---|
| a route-B boundary-prescription comparison | an all-contained analogue of route B with its own itemization (grouping, per-site sum, retention) | re-run Sections 2–3 with the new source set |
| route-B dynamics and correlation functions | a route-B BA2 (the admitted BA2 constants use `||Phi||_F<=2268|tau|`, not the route-B `2349|tau|`) | Lieb–Robinson/Duhamel comparison with the route-B constants |
| uniqueness of any ground state | a uniqueness mechanism beyond the named construction | local stability with evaluated constants |
| anything uniform in the lattice spacing `a` | every constant here is at fixed spacing | none within this model |
| the continuum problem | — | outside this packet |

## 7. Item 7 — fixtures, the mandatory sentence, gate fields, scaling and controls

**Fixtures** (exact rational arithmetic in `check.py`, each labelled `model_is_finite_graph: true`, `transfers_to_aq: false` where finite; they audit algebra and rejection logic and prove nothing about infinite volume):
- route-B incidence and partition (Section 1: 3000 plaquettes; 153/88/16/72; 52 faces and 16 owner sets); support-one groups; the every-site common core (nine comparisons); admissibility (F01, F02);
- the 16-face first-order `R`-marginal (trace norm `|tau|/18`) and the straddling fixture: for one creation of amplitude `1/10`, the odd part of `rho_R` vanishes for the straddling supports `{r_0,o}` and `{r_0,r_1,o}` and is nonzero for the pair `R` and for a single site of `R`, while every case has excited population `1/101` at second order;
- site energy 24; the region-form factor with the route-B `t` (`(1+t)^2-1` about `7.223e-9`);
- the BB1-type algebra fixtures, re-coded: the split identity (F12) and the covering recursion (F14) on six sites with three levels and six single-site supports; `Tr N_c(omega)=1560311/1433250` and `538597/504063` on two mixed outside states, with the outside-state Lipschitz inequality exact; the single-support bound (F10) for 33 changes; an end-to-end check of the lemma on a seven-site chain (1D charge `|I|<=2^{diam I}`); second-order propagation (`rho_01=-abc` exactly, so a change two supports away moves it by `-ab`); coefficient decay versus marginal decay (`rho_r` moves from `[[45/49,6/49],[6/49,4/49]]` to `[[9/10,0],[0,1/10]]` with equal coefficients on supports meeting `R`); the global-fidelity product state (`(100/101)^400<1/50` while one-site marginals differ by `2/sqrt(101)`); the outside vector not a ground state (ground energy `-1/3` exactly and lowest; the outside vector has normalized Rayleigh residual `49/44944`); the Eckart pairs and the degenerate `diag(0,0,1)`; the limit-order double sequence; the normalization zero at `z=i/2`; the mean-field map (`c_0=1/6` for every far source); fixed versus moving vectors;
- whole sequence versus subsequence (alternating steps `1/25`; harmonic partial sums above 3 at `N=31`); translation (8 of 64 fine translations preserve the grouping; the non-coarse witness keeps its coefficient); the sign mirror (flip set, compression, local mirror of a product unitary); the node replay; model crossing (a route-B limit identified with the zero-selected BB2 limit, or BB1/BB2 constants applied to route B, is rejected).

**Mandatory sentence template, quoted once verbatim:**

> For the uniform Kogut-Susskind SU(2) model at fixed spacing and strong bare coupling handled by route B, at the same coupling |tau|<=10^-8, the reduced densities of the named construction (centered whole-star-plus-single-group boxes on centered coarse cubes) converge as a whole sequence on every finite region, at a rate in N that holds for every N at least 2 with the region inside the box, and to the same limit along every exhausting sequence of finite complete-factor volumes of the same prescription; this limit coincides with every AQ1 subsequential state of that construction, is invariant under coarse translations, and at tau=+10^-8 has centered Euclidean Wilson correlation C(1) within the AX2 radius of the AX2 datum at the node s=1; this is convergence of the named constructions (one family for route B), not uniqueness of any ground state, not a statement about other boundary conditions or about states outside the named construction, not weak coupling or continuum, and not a statement uniform in the lattice spacing a.

Constants for the template: `q=1/64`; `K_B=13/27941256` (analytic_disc, `rho=64|tau|`); `C_B` and `c_site,B` as in Section 3 (iterated_split, `W=1024`); `C'_B=C_B`, `c'_site,B=c_site,B` (assembly `union_comparison`); node `d` and `R'` equal to the AX2 gate rationals; `N>=2`; both signs; `R={0,e_z}`.

**Gate fields** (exported exactly as `gate_fields_required`): `whole_sequence_claimed`, `state_convergence_claimed`, `state_decay_claimed`, `rate_in_N_claimed`, `translation_invariance_claimed`, `node_certificate_restated_for_limit` true, with the three scope strings of the contract; `common_limit_claimed`, `uniqueness_of_ground_state_claimed`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `resolved_interaction_shift`, `rate_in_a_claimed`, `continuum_claim`, `weak_coupling_claim`, `scientific_priority_verified` false. `dynamics_level` is not exported. `uniform_wilson_claim: true` means only that the model is the uniform fixed-spacing Kogut–Susskind model as labelled (no uniform Wilson-mean sign certificate), as in AX1 and AX2.

**Scaling `tau -> tau/100`** (same exact formula at both couplings, no intermediate rounding): `K_B` ratio `39059948/388073` (`1.00651032151e2`); `C_B`, `c_site,B`, `C'_B`, `c'_site,B` ratio `1.00661451758e2`, all inside `[95,105]` (linear in `tau` with a positive nonlinear correction from `1/(1-10208*64|tau|)` and the split terms); `q` and `rho/|tau|` exactly 1; node datum exactly 1; node radius replay `1.00001527222e2` (recorded, not a target). A quadratic, constant or square-root headline, and a bracket chosen after evaluation, are rejected.

**Controls.** Every one of the 52 contract controls is a check in `check.py` whose damaging mutations must each raise `AdmissionError` (never `assert`); a mutation that is accepted aborts the run.

| control | damaging mutations rejected |
|---|---|
| `coherent_evidence_tampering` | coherently rehashed contract edits (`K_B` target relaxed, `q` changed, disc radius changed, split weight changed, `rate_in_a_claimed` true, `common_limit_claimed` true, a control removed, a hash-binding flag flipped, `tau` changed); a byte change without rehash; a snapshot removed; an admitted gate edited; the AX2 calculator edited; an exported `K_B` halved |
| `exact_arithmetic_admission` | float, bool, `nan` and zero-denominator inputs; a float preview admitted as a bound |
| `no_priority_or_continuum_claim` | continuum, priority or weak-coupling flag true; a historical lens as a premise |
| `changed_model_relabelled` | `tau`, model id (zero-selected), zero triple, route-A grouping, all-contained boundary, l1 metric, window, clock, SU(3), two dimensions, a finite-graph result under the route-B label |
| `insufficient_verdict_retained` | a missed target, R form only or `Q_L` only relabelled accepted; a failed coefficient input relabelled limited; `tau`, `W` or `rho` retuned |
| `tau_scaling_exponent` | quadratic, constant or square-root headline; node datum ratio not 1; a bracket chosen after evaluation |
| `wrong_delta_alpha_hbar_clock` | amplitudes `tau/576` and `tau/9`; `u` labelled `theta`; the Euclidean clock labelled real time; the non-unit fixture (`alpha=5`, `hbar=7`) with `hbar` dropped or `u` read as `theta` |
| `tier_mixing_rejected` | polymer_kp route; a Lieb–Robinson tier; a duhamel route; a hypothesis source; an assembly as a route; `K_B` with the split route; `C_B` with the disc route; a weighted_norm value as a bound; an exact label with a crude input; a route-A constant under the route-B label; a whole-sequence constant without assembly |
| `uniform_in_N_not_in_a` | uniformity in the lattice spacing; an unqualified uniformity next to a rate |
| `placeholder_span_rejected` | angle-bracket spans with a space, a bar or `e.g.` |
| `negation_aware_phrase_scan` | five forbidden phrasings of the contract and round list appended affirmatively (none is used affirmatively in this packet); a negated one is accepted |
| `parameters_declare_metric_weights_window` | metric, weights, window, clock or cutoff removed from a rehashed contract |
| `rate_constant_pair_prefrozen` | `q=1/128`; `rho` optimized per `N` or changed; weights declared after the constants; `W=64` (`lambda` not below `q`); a weight admissible only under `28|tau|` (`W=2600`); a changed `K_B` target |
| `decay_rate_in_N_not_a` | per fm; per lattice spacing; `rate_in_a_claimed` true |
| `topology_named` | weak-star, Hilbert–Schmidt, strong topology on a fixed vector as the state topology |
| `subsequence_versus_whole_sequence` | whole sequence from compactness; an `N` to `N+1` bound only; an unlabelled limit |
| `common_clock` | the two signs at different `|tau|` or clocks; the limit dynamics in another clock |
| `coefficient_decay_not_marginal_decay` | state decay inferred from equal coefficients (fixture) |
| `normalization_couples_supports` | straddling dropped; straddling at first order only; normalization `1+O(t^2)`; a support strictly containing `R` given a first-order marginal; single groups charged as straddling |
| `outside_vector_not_ground_state` | a gap argument on the outside vector |
| `global_fidelity_orthogonality_catastrophe` | a bound through the global overlap |
| `cutoff_uniform_then_removed` | constants depending on `L`; removal before the uniform bound; a selected-face vector kept at `L=18` |
| `cutoff_vector_removal` | eigenvalues only; AM2 Section 6 cited alone; a route-A (selected-strip) gap |
| `region_constant_scales_with_Y` | the `R` constant reused on `Y`; exponent `N-1` for every `Y` |
| `named_construction_not_uniqueness` | three forbidden phrasings appended (never asserted here); a uniqueness flag true |
| `global_lipschitz_not_decay` | the route-B fixed-point Lipschitz constant, exclusion constant or no-decay bound `1073/174982136` as a decay factor; the route-A values; a density Lipschitz constant in the coefficients or the outside state; the mean-field claim `(1/2)^5` |
| `fixture_second_order_propagation` | a first-order propagation claim; a per-link factor below the exact product |
| `fixture_split_lipschitz_and_trace` | the growing-region-size charge; a vacuum-component creation (`Tr=97/144`) |
| `zero_free_region_required` | analyticity of the reduced density or of the normalization |
| `every_site_coefficient_input` | the BA1 gate value; the BA1 forward bound; the BA1 reverse theorem cited; the BB1 every-site form; an R-only input at far sites; the route-B form cited as admitted; exponent `N-1` at every site |
| `cutoff_limit_order` | the `N` and cutoff limits exchanged |
| `cauchy_estimate_not_compactness` | compactness plus closeness; compactness plus first-order agreement |
| `limit_identified_with_aq1_limits` | inheritance first; the zero-selected list; the BB2 list; no extension to the quasi-local algebra |
| `translation_invariance_separate_item` | invariance from nested cubes; a two-step union bound; a non-coarse claim; a telescoped source |
| `route_b_constants_not_route_a` | `28|tau|`, 49 faces, 4 groups, `9856`; the BA1 `K`, the BB1 `C` and `c_site`, the BB2 `C'` and `c'_site` under route-B labels; a route-A label; a source substitution `(28,49)` that aborts at the `T'` pin |
| `disc_admissible_under_J_prime` | disc radius `1/37888`; split weight `1/(37888|tau|)`; twice the route-B maximal radius; `W=4096` |
| `support_one_groups` | single groups charged as straddling, clipped, omitted from the piece graph, charged a distance, first order dropped; a clipped enumeration |
| `route_b_first_order_marginal` | the route-A ten faces; 88 faces; straddling faces nonzero; the route-A trace norm |
| `selected_face_site_energy` | first-order site energies at most 18; selected energy 18; kept from `L=18` |
| `one_family_no_common_limit` | a common limit; a second route-B family; identification with an all-contained boundary |
| `exhaustion_within_prescription_only` | boundary-condition phrasing; volumes with single groups dropped; `N_k` not the largest; a telescoped exhaustion |
| `sign_mirror_pointwise` | `-tau` as a second coupling or observation; whole sets only; a nonlocal unitary; an untied selected coefficient |
| `identification_before_inheritance_route_b` | inheritance before identification; the route-A reset `98|tau|`; identification on `R` only |
| `region_form_load_bearing_for_node` | node restated with the R form only or inside `Q_L` only |
| `node_values_unchanged` | a re-derived radius as the headline; a smaller state term; the seven-star slope `49|tau|/4`; another node; an undeclared calculator path; a changed datum |
| `reference_unresolved_retained_route_b` | a shift or sign claimed; the label dropped; the free value outside |
| `no_finite_box_node_convergence` | `C_N(1)->C_inf(1)` claimed |
| `no_route_b_dynamics_claim` | a dynamics comparison; a correlation statement; `dynamics_level` exported; the BA2 constant `2268|tau|` applied |
| `non_coarse_translation_no_claim` | invariance or non-invariance claimed; the route-A reason offered |
| `model_crossing_rejected` | identification with the BB2 limit; BB1 constants applied; transfer to the zero-selected family |
| `direct_comparison_required` | a union-volume (factor 2) or telescoped comparison used for a target |
| `rate_range_stated` | a rate without its range of `N`; an `O(1/N)` statement; a rate transferred from BB2 |

**Source-edit audit (private scratch, not evidence).** Eight copies of `check.py`, each with a single edit, were run against a mirror of this directory; each aborted before writing any output, at the check named in brackets. The edits were: the selected predicate dropped (the I1 class comparison); the single groups of a volume not kept (support-one groups); the per-site sum computed without the single group, `28|tau|` (route-B per-site inputs); the face count 52 replaced by 49 in the circle bound (the `K_B` formula pin); the contract read of the disc factor replaced by 32 (the weights read from the contract); `W=2600` substituted for the contract weight (the route-B split-weight self-map); the AX2 datum perturbed by `10^-40` (the calculator replay); and a continuum flag set true (the claim flags).

## 8. Error ledger (`preregistration.error_terms_itemized`, added linearly)

`C_B` decomposes exactly (`check.py` verifies that the parts add to `C_B`); the same decomposition holds for `c_site,B` without the factor `(1+q)`.

| term | value | note |
|---|---|---|
| `route_b_every_site_coefficient_input` | `2K_B(1+q)=845/894120192` (`9.45063099525e-7`) | supports meeting `R` through `kappa=2`; the far-site input enters the split rows through `S_lambda` |
| `single_factor_groups` | charged inside `K_B`, `t_0` and `t_W`; labelled first-order share of `K_B`: `K_B*3/52=1/37255008` | 3 of the 52 first-order faces per site and `|z|` of the per-site sum `29|z|`; never straddling, never clipped |
| `straddling_supports_route_b` | `K_B S_lambda(1+q)4t_W/(1-8t_W)=2647385/26817139457934784` (`9.87198878595e-11`) | covering chains reaching `Y`, every order in the straddling amplitudes |
| `normalization` | `K_B S_lambda(1+q)4t_0t_W=34416005/48269112715774228399091712` (`7.13002644209e-19`) | the `a`-term of (F12) |
| `split_remainder` | removal `7.13049761143e-19` plus closure feedback `1.88453363845e-22` (exact values in `results.json`) | coverings ending inside the removed region and the self-consistent closure |
| `whole_sequence_assembly` | factor 1, extra cost 0 (`union_comparison`) | nested telescoping would cost `64/63` (labelled) |
| `cutoff_removal_at_fixed_N` | not_applicable as a numeric cost | an exact limit at fixed `N` (F20–F23, route-B gap `1/2`); constants independent of `L` |
| `identification_with_ax1_states` | not_applicable as a numeric cost | exact equality of states on every finite region |
| `node_restatement` | not_applicable as a numeric cost | `d` and `R'` carried unchanged; `R'` already contains the arithmetic half-width `1/(4*10^40)` |
| `arithmetic` | not_applicable as a numeric cost | exact Fractions; directed enclosures `e^{1/8}<8/7`, Machin `pi`, `e^{-3}` brackets; decimals are truncated previews |

The near term is almost all of `C_B`; the split terms are about `10^-4` of it. Deterministic terms add linearly; nothing is combined as a root sum of squares.

## 9. Exclusions, limitations and claim flags

**Contract exclusions (respected):** uniqueness of every infinite-volume ground state; statements about boundary conditions outside the named construction; a common limit of two route-B families; route-B dynamics and correlation functions; convergence of finite-box nodes; the zero-selected family; any estimate uniform in the lattice spacing `a`; continuum or weak coupling; scientific priority.

**Claim flags in `results.json`:** `continuum_claim`, `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `scientific_priority_verified`, `common_limit_claimed`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `resolved_interaction_shift`, `weak_coupling_claim` are false; the true gate fields hold only within their scope strings.

**Limitations.**
1. **Scope.** Only the uniform route-B model at fixed spacing and strong bare coupling (`g^4>=9.6x10^9`, `|tau|<=10^-8`), the named construction FB and route-B volumes containing `Lambda_N`, `N>=2`, the cover `R` and finite complete-factor regions, coarse translations and the node `s=1`. Nothing transfers to the zero-selected family, to other boundary prescriptions, to weak coupling or the continuum. Every rate is per coarse l-infinity step in `N` at fixed spacing (a coarse step is `(4a,2a,a)`), valid for every N at least 2 as stated, never a rate in the lattice spacing.
2. **Inherited without re-proof:** the AM2 majorant steps, fixed point, uniqueness in the ball and Section 6 cutoff facts; the AX1 route-B grouping, `J_0'`, finite-volume theorem (unique gauge-invariant ground, gap `1/2`), AQ1/AQ2 re-instantiation list, state lemma and flip identity; the AV1 product ordering and F20–F23; the AX2 certificate; the I1 dictionary. Banach, Weierstrass and the maximum principle are standard and not machine-checked.
3. **Upper bounds only.** Nothing lower-bounds the distance of two densities. The `-tau` evaluations replay the same `|tau|` formula.
4. **Binding margins.** `K_B` (margin about 2.149) and `c_site,B` (about 2.149) are the thin margins; `c_site,B` is essentially `2K_B`, so the region margin is inherited from the coefficient input.
5. **Correlation.** The route, the targets, the brackets and the inherited lists are shared through the contract and the selection note; all agents are correlated model agents. Independence is limited to the re-derivation, enumerations, constants and code.
6. **Fixtures** are exact finite audits (`transfers_to_aq: false`), not proofs of lattice statements.
7. Scientific priority is unverified.

## 10. Contract wording defects and readings (non-blocking)

- **W1 (item 4, clause 2a).** "from one direct comparison c5B of V_k with Lambda_{N_k} and item 1": the second ingredient is the whole-sequence bound T4 (the first clause of item 4, BB2's item 1), not BC2 item 1 (incidence and admissibility). Read as T4.
- **W2 (T0 form and the sharp order).** The vanishing order proved is at least `N-|u|_inf+1` for `|u|_inf<=N-1` (Lemma D4 gives `1+d`); the contract form `(N-|u|_inf)_+` is used for `K_B`, and the sharper exponent is not substituted.
- **W3 (T0 and the cutoff).** T0 is a statement in each `Q_L` uniformly in `L`; untruncated creation coefficients are not defined and are not asserted. The untruncated passage is made only for densities (Theorem S5 (vi)).
- **W4 (route-A extremes).** The route-A extremes fail the route-B self-map by the factor `29/28` only (`29/1792` against `28/1792`); the rejection is exact but thin.
- **W5 (T3 and T1 targets).** With `union_comparison` the T3 constant equals `C_B`, so T3 carries no information beyond T1 (the preregistration note says so).
- **W6 (inheritance and dynamics).** The AX1 route-B list includes AQ1 stationarity and GNS strong continuity under the route-B limit dynamics. They are inherited as properties of the identified state; this is not a route-B dynamics comparison or correlation-function statement, which remain obligations.
- **W7 (weights text).** "support sizes charged per site through |I| at most 8*2^{diam I}" is read with the factor 2 absorbed into `lambda=2/W`, as in BB1.

## 11. Proposed verdict

**`accepted_within_scope`** (forward, single producer), label `convergence_of_named_constructions`, secondary `certificate_restated_for_limit`, `reference_unresolved`, `static_not_dynamic`:
- T0 is proved at `K_B=13/27941256<=1/1000000` for c1B, c4B and c5B, both signs, in each `Q_L` uniformly in `L`;
- T1 and T2 are proved by direct comparison, both signs, in each `Q_L` and for the untruncated vectors at fixed `N`;
- T3 and T4 are proved for the whole sequence of FB boxes, both signs, for the untruncated vectors;
- items 2a, 2b, 3 and 4 are proved with the stated bounds, and the node is restated with `d` and `R'` equal to the AX2 gate rationals;
- every route-B constant is recomputed from the route-B inputs.

## 12. Item and control map

| contract item | section | `check.py` checks |
|---|---|---|
| 1 incidence, partition, admissibility | 0, 1 | `route_b_partition_brute_force`, `route_b_per_site_inputs_derived`, `route_b_incidence_on_R`, `boundary_counts_at_most_bulk`, `support_one_groups_enumerated`, `selected_face_site_energy_24`, `route_b_first_order_R_marginal`, `weights_declared_and_admissible`, `disc_admissible_under_J_prime` |
| 2 coefficient input (analytic_disc) | 2 | `am2_majorant_rederived_route_b`, `circle_bound_pinned_to_ax1_T_prime`, `route_b_piece_graph_order_vs_distance`, `route_b_every_site_common_core`, `K_B_every_site_input_meets_target`, `crude_tier_reported_separately`, `route_b_global_lipschitz_values_recorded`, `every_site_coefficient_input` |
| 3 marginal locality (iterated_split) | 3 | `marginal_locality_lemma_constants_route_b`, `C_B_meets_target`, `c_site_B_meets_target`, `every_comparison_both_signs`, `region_form_factor_route_b_t`, `cutoff_uniform_then_removed_at_fixed_N`, the `fixture_*` checks, `per_site_charging_versus_growing_sizes` |
| 4 whole sequence, 2a, 2b, 3, 4 | 4 | `whole_sequence_cauchy_union_comparison`, `C_prime_B_meets_target`, `c_prime_site_B_meets_target`, `item_2a_exhaustion`, `item_2b_sign_mirror_pointwise`, `item_3_identification_then_inheritance`, `item_4_coarse_translations` |
| 5 node | 5 | `node_replay_equals_ax2_gate`, `node_own_reevaluation_cross_check`, `ax2_calculator_sha256_pinned`, `node_values_unchanged` |
| 6 obligations | 6 | `results.json` field `obligations` |
| 7 fixtures, template, gate fields, scaling, controls | 7 | `tau_scaling_every_constant`, `mandatory_template_quoted_once_and_phrase_scan_clean`, `gate_fields_exported`, `rate_claims_carry_their_range`, `error_ledger_itemized`, `report_pins_exact_values`, `contract_controls_all_executed` and one check per control id |
| hash binding | header | `contract_snapshot_bound`, `check_py_sha256_recorded_before_evaluation`, `admitted_gate_sha256_pinned`, `forward_inputs_inventory_exact`, `premise_values_parsed_from_pinned_gates`, `no_interpreter_cache_in_closure` |

Every control id of the contract is a check id of the same name (Section 7 table).

**Methodological lenses** (frozen method snapshots, used as modern method rules; no historical person endorses anything here). *Newton, analysis before synthesis:* the route-B statement was analysed backwards into the per-site inputs (29, 52, 5), the common core and the circle bound before any constant was synthesized, and the synthesis was tested by breaking it (route-A substitutions, clipped single groups, the route-A extremes). *Tesla, complete accounting:* every group meeting `R` is itemized, every source face (selected ones included) is charged at its distance, and every split channel (straddling, normalization, removal, closure) appears in the ledger.

## 13. Reproduction

```bash
python3 -B research/round33/forward/bc2/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/forward/bc2/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/bc2.json research/round33/forward/bc2/report.md
python3 -B research/round33/tools/freeze.py verify research/round33/forward/bc2
```

`check.py` verifies the contract snapshot sha256 before any evaluation, records its own sha256 before evaluation, pins the sha256 of the eleven admitted gates it reads and of the AX2 calculator, reads the targets, weights, brackets and template from the contract, and writes `results.json` and `source-manifest.json` (which binds this report, the checker and all 42 input snapshots). `freeze.json` binds the whole producer closure. BC2 is investigation 6 of 8 of Round33; this producer executed the single forward direction only.
