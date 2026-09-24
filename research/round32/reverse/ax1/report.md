# Hruday route-B re-derivation for the uniform Kogut–Susskind SU(2) Hamiltonian — AX1 reverse

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted reverse production under premise isolation (contract control `reverse_premise_isolation`). I read the frozen contract snapshot `inputs/research/round32/contracts/ax1.json` first (sha256 `bc834eec4f5377041cea9db42a8674cf1f3de0a43b7fef3696a461a011da7d8d`). After it I read only files under `inputs/`, plus the inherited protocol and code-style files named in Section 11. I did not read `skeptic/triage.md`, `skeptic/loop2-response.md`, any `advisor/deliberation-*.md`, any file under `research/round32/experts/`, or anything under `research/round32/forward/ax1/`.

HNM labels are project aliases. The following are established mathematics:
- commuting-creation expansions (the admitted AM2 construction; Bravyi–DiVincenzo–Loss 2008 as credited in the AM2 lineage; Gauvin arXiv:2503.15539v3, Supplement A.6–A.8, as AM2's template);
- the Nachtergaele–Sims unbounded-onsite dynamics theorem (arXiv:1410.8174v1, Section 3 and Theorem 4.1), as placed in AQ1;
- Peter–Weyl theory, SU(2) centre gradings and centre-flip symmetries of lattice gauge theory;
- the pure-state trace-distance and fidelity inequalities.

Scientific priority is unverified.

## Verdict (reverse half)

**Model.** The uniform Kogut–Susskind SU(2) Hamiltonian on Z³ at fixed spacing: every elementary face has coefficient `nu=alpha*tau/24`. The route-B split, the whole-star boxes, the cover `R={0,e_z}` and both signs of `|tau|<=10^-8` are as in the contract. The label is **"uniform Kogut-Susskind SU(2) at fixed spacing, strong bare coupling"**, with `g^4=96/tau=9.6x10^9` at the cap. It is never weak coupling or continuum.

**What the reverse route establishes.**

1. **Dictionary and box.** The uniform triple is `tau/24` on each selected face. At the cap its magnitude is `1/2400000000`, which lies far inside the box `|lambda_L|,|lambda_R|<=alpha/2`, `|mu|<=alpha/8`.
2. **Route B and grouping.** Haar forces the selected faces into the interaction. The single-factor grouping `psi_b=-(tau/3) sum_{3 selected faces of b} W_f` has `||psi_b||<=|tau|`. The per-site sum is `J'=4*7|tau|+|tau|=29|tau|`, the maximal support is 4 and the termination order is 8.
3. **J_0 re-freeze.** `J'` at the cap is `29/10^8`, above AM2's frozen `J_0=7/25000000`. The R1 re-freeze `J_0'=29/10^8` passes both exact contraction checks: `J_0'G(R)<1073/175000000<1/64` and `2J_0'G'(R)<319/1562500<1`. This gives a unique full-Hilbert ground and a normalized gap of at least 1/2 (at least `alpha/16` in physical units) in every finite complete-factor volume, at both signs.
4. **AQ1/AQ2 checklist.** Eighteen steps are itemized: ten are verbatim re-applications and eight need a new constant. The reset is `omega(h_R)<=102|tau|`. With the Haar reference gap six this gives `epsilon_R<=17|tau|`. No named constant is left unproved.
5. **Incidence on R.** Seven stars, two single-factor groups and six selected faces meet R. No face is charged twice. `||B_N||<=51|tau|/8` and `k'=51|tau|/4`.
6. **State lemma.** The exact counts are 52 faces owning a link of each factor, 88 meeting R and 16 inside R. The contract candidates 96 and 168 are reproduced only as the labelled anchor-group bounds `4x24` and `7x24`. The tier values are:
   - tier (i): `D'_i=375551151329/15312500000000000 ≈ 2.4526e-5`;
   - tier (ii): `D'_ii=30934916107401289/2530733246376451200000000 ≈ 1.2224e-8`.

   Both values hold at both signs. Tier (ii) meets `1/2500000` with a margin of about 32.7.
7. **Transfer (proved, not cited).** In the uniform model every face is tied to tau, so `U_E H(tau) U_E^*=H(-tau)` and `omega_{N,-tau}(W)=-omega_{N,tau}(W)`. The parity grading applies verbatim to the selected faces. At first order only f=W contributes, so `omega(W)^(1)=+tau/144` is unchanged.

**Proposed outcome of this producer:** `accepted_within_scope`, with sub-label `uniform_local_closeness_not_uniqueness`. Admission still needs the forward route, the exchange and the skeptical review.

## 1. Reverse analysis: start from the uniform Hamiltonian

**The uniform Hamiltonian and its dictionary.** Take the AL1 convention, `W_p=Tr U_p/2`:

\[
H_{KS}=\alpha\sum_eC_e+\lambda\sum_p(1-W_p),\qquad \alpha=\frac{g^2}{2a},\quad\lambda=\frac{2}{g^2a},\quad \nu:=\lambda=\frac{\alpha\tau}{24},\quad \tau=\frac{24\lambda}{\alpha}=\frac{96}{g^4}.
\tag{HNM-AX1-R01}
\]

At `|tau|=10^-8` this gives `g^4=9600000000`. The checker verifies `tau g^4=96`, `alpha tau/24=lambda` and `(alpha/8)(tau/3)=lambda` on three exact `(g^2,a)` pairs.

`tau=96/g^4` is positive for real g. The negative-sign model is the `U_E` image of the positive one (Section 8), so it is unitarily equivalent to it. It is not a real-g Kogut–Susskind coupling. The physical gap `alpha/16` equals `g^2/(32a)`.

**Normalized form and the complete face partition.** Divide by `delta=alpha/8` and drop the scalar `lambda N_p`:

\[
\frac{H_{KS}-\lambda N_p}{\delta}=8\sum_eC_e-\frac{\tau}{3}\sum_fW_f,\qquad \sum_f=\sum_b\Big(\sum_{f\in O_b}+\sum_{f\in S_b}\Big).
\tag{HNM-AX1-R02}
\]

Each face has a unique anchor `pi(base)` and a unique class among the 24 anchored classes of the I1 table: 21 omitted classes (`O_b`) and 3 selected classes (`S_b`, xy faces with r=0,1,2 and s=0, support `{b}`). This is a partition. The checker encodes the eight-row I1 table, expands it to 24 classes, and re-derives every row from `pi` and the link tails.

**The question.** The admitted chain needs a **Haar** reference for:
- the AV1 state lemma (face vectors `W_f Omega_0` at energy 24, the Haar moments of `P_R`);
- the AT4/AQ2 reset with gap six;
- the AW1 grading.

Which split of (R02) keeps Haar?

**Route A is not Haar.** Keeping `S_b` on site gives `h_b^A=8 sum C_e-(tau/3) sum_{S_b}W_f`. For one selected face with `k=tau/3`, the trial `Omega+(k/24)W Omega` has numerator `6t^2-kt/2` at `t=k/24`, which equals `-k^2/96=-tau^2/864`, strictly negative. So

\[
\langle h^A_b\rangle_{\rm trial}<0=\langle h^A_b\rangle_{\rm Haar}\qquad(\tau\ne0),
\tag{HNM-AX1-R03}
\]

and Haar is not the route-A reference (in alpha units this is AT4's `-lambda^2/(12 alpha)`). Route A does keep the triple in the box and `J=28|tau|`. AM2 as admitted therefore already gives the gap for this very operator, resting on the inherited A1 strip theorem, which I did not read. I record this only as a cross-check. None of the Haar-dependent steps can use route A.

**Route B.** Keep `h_b=8 sum_{e owned by b}C_e` with the Haar vacuum. The selected faces must then enter V. Four natural groupings of the three selected faces of b compare as follows (bulk per-site sums computed on the box `N=3`):

| grouping | per-site sum | support | box inventory |
|---|---:|---:|---|
| **single-factor group `psi_b` (route B)** | **29\|tau\|** | 1 | identical to AQ1's boxes |
| merged into the star `phi_b` | 32\|tau\| | 4 | selected faces lost outside whole stars |
| each face its own group | 52\|tau\|/3 | ≤3 | all-contained prescription: a changed boundary and changed AM2 constants |
| dropped (zero-selected) | 28\|tau\| | – | not the uniform model |

Only the single-factor grouping does all three of the following:
- keeps the Haar reference;
- retains exactly AQ1's inventory (whole stars inside `Lambda_N` plus every selected face of every factor in `Lambda_N`);
- keeps the AM2 support bound 4.

Routes A and B are two splits of the **same** finite operator, up to on-site scalars. Their unique finite grounds, and hence AQ1's boxes and states, coincide. The per-face grouping has a smaller J, but it changes the interaction decomposition and the boundary prescription. It is disclosed and not used, as AGENTS.md requires for changed support decompositions.

## 2. Route B: grouping, per-site sum, support (item 2)

\[
H=H_0+V,\quad H_0=\sum_bh_b,\ h_b=8\sum_{e\in b}C_e,\qquad V=\sum_{b+S\subseteq\Lambda}\phi_b+\sum_{b\in\Lambda}\psi_b,\quad \phi_b=-\tfrac{\tau}{3}\sum_{f\in O_b}W_f,\ \ \psi_b=-\tfrac{\tau}{3}\sum_{f\in S_b}W_f .
\tag{HNM-AX1-R04}
\]

**Norms.** Each `W_f` is a real multiplication operator with `|W_f|<=1`. So `||phi_b||<=21|tau|/3=7|tau|` and `||psi_b||<=3|tau|/3=|tau|`. Both are equalities: at the identity configuration every trace equals one, and continuity plus the full support of Haar measure pass this to the essential supremum.

**Per-site sum.** A site u lies in the four stars `b+S` with `b in u-S`, and in exactly one single-factor group, `{u}`. Hence

\[
J'=\max_u\sum_{X\ni u}\|V_X\|\le4\cdot7|\tau|+|\tau|=29|\tau|.
\tag{HNM-AX1-R05}
\]

The checker recomputes this from the explicit route-B group list of `Lambda_3`: the bulk maximum is 29 per `|tau|`, attained at the origin, and boundary sites are lower. It also checks that each of the 5565 retained faces of `Lambda_3` is charged exactly once.

**Support and termination.** The maximal support is `|S|=4` (stars); single-factor groups have support 1. In AM2's anchored estimate every creation support must meet X, and a nonzero product cannot contain two creations that share a site. One side of `V_X` therefore carries at most `|X|` creations, so

\[
\mathrm{ad}_{C_1}\cdots\mathrm{ad}_{C_k}(V_X)=0\quad(k>2|X|),\qquad \max_X 2|X|=8 .
\tag{HNM-AX1-R06}
\]

A four-qubit audit fixture (`model_is_finite_graph:true`) confirms the order:
- `ad_C^8(star)|0000>=8!|1111>` and `ad_C^9(star)=0`;
- `ad_C^2(single-site)` is nonzero and `ad_C^3(single-site)=0`;
- `ad_C^9` of the sum of both kinds vanishes.

`L_k=2^p(2p)^k(1+k(p+1)/p)` with `p=4`, that is `16*8^k(1+5k/4)`, and `G(t)=16e^{8t}(1+10t)` are unchanged.

## 3. The J_0 issue and the re-freeze (item 3)

AM2 froze `J<=28|tau|<=J_0=7/25000000`. At the cap, `J'=29/10^8>7/25000000`. **The AM2 theorem as frozen does not apply to route B**, and citing it with its admitted constants is rejected by the `am2_gap_reuse_justified` control.

There are two resolutions:
- **R2 keeps `J_0`** and lowers the cap to `|tau|<=J_0/29=7/725000000`. That is a changed coupling and is not selected.
- **R1 (selected) re-freezes `J_0'=29/10^8`.**

For R1, `e^{1/8}<1/(1-1/8)=8/7` (term-by-term comparison with the geometric series, strict from the second order). The checker also encloses `e^{1/8}` to `10^-40`. So

\[
G(R)=\tfrac{37}{2}e^{1/8}<\tfrac{148}{7},\qquad G'(R)=308\,e^{1/8}<352\qquad(R=\tfrac1{64}),
\]

\[
J_0'G(R)<\frac{29}{10^8}\cdot\frac{148}{7}=\frac{1073}{175000000}<\frac1{64},\qquad
J_0'G'(R)<\frac{319}{3125000},\qquad 2J_0'G'(R)<\frac{319}{1562500}<1 .
\tag{HNM-AX1-R07}
\]

The certified enclosures are `G(R) ≈ 20.963246` and `G'(R) ≈ 349.00972`. All four rationals are pinned in `results.json → j0_resolution` together with the contract source path and its sha256.

**On-site theorem.** By Peter–Weyl, `L^2(SU(2))` is the direct sum of spin-j blocks, and `C_e` acts on the spin-j block as `j(j+1)`. On the 24-link tensor product the kernel of `sum C_e` is the constants (spin 0 on every link), and the next eigenvalue is `3/4`. Therefore

\[
h_b=8\sum_{e\in b}C_e\ \ge\ 6\,Q_b\ \ge\ Q_b,\qquad Q_b=I-|1_b\rangle\langle1_b| .
\tag{HNM-AX1-R08}
\]

**Gauge invariance.** The constant function is invariant under left and right translations, so it is fixed by every endpoint gauge action. The Casimirs are bi-invariant, and every `W_f` is gauge invariant.

**Conclusion (AM2 with new constants).** AM2's argument uses only the following hypotheses:
- `h_x>=Q_x` with a unique vacuum;
- supports of at most 4;
- `J<=J_0` with the two contraction inequalities;
- V bounded, self-adjoint and gauge invariant in each finite volume;
- compact resolvent for the cutoff passage.

Route B satisfies all of them with `J_0'`. The fixed point, the scalar equation, the shifted-resolvent exclusion `||b||_a<=2J'G'(R)||b||_a<||b||_a` and the cutoff removal therefore re-apply unchanged. For every nonempty finite complete-factor volume and both signs of `|tau|<=10^-8`:

\[
\text{unique full-Hilbert ground},\qquad E_1-E_0\ge\tfrac12\ \text{(normalized)},\qquad \Delta_{\rm phys}\ge\frac{\alpha}{16}=\frac{g^2}{32a}.
\tag{HNM-AX1-R09}
\]

**Nonzero physical excited sector.** Every factor owns all four links of its three selected faces, and those faces are retained in `psi_b`. The full ground `Omega_H` is strictly positive: it is the Schrödinger ground of a Laplacian plus a bounded smooth real potential on a connected compact manifold. So `(W_g-<W_g>)Omega_H` is nonzero, gauge invariant and orthogonal to the ground. The empty volume is treated separately (vacuous).

## 4. AQ1/AQ2 re-instantiation checklist (item 4)

| # | step (source) | status | admitted constant | route-B constant |
|---|---|---|---|---|
| 1 | AM2 ground and centred gap (am2 §1–4) | new constant | `J<=28|tau|<=7/25000000` | `J'<=29|tau|<=J_0'=29/10^8`, (R07) |
| 2 | AM2 on-site hypothesis | verbatim | strip gap delta (normalized 1) | `h_b>=6Q_b>=Q_b` |
| 3 | AM2 majorant, termination, G | verbatim | support 4, order 8 | unchanged (stars 4, single-factor groups 1) |
| 4 | AM2 gauge covariance, physical restriction, excited sector | verbatim | selected square | selected face in each factor |
| 5 | AM2 cutoff removal | verbatim | compact resolvent | pure Casimir sum |
| 6 | AQ1 reset energy C_F (HNM-AQ1.1) | new constant | `56|tau||F|` | `2J'|F|=58|tau||F|` |
| 7 | AQ1 trace-norm compactness | verbatim | `C_F/L` tails | same, with `C_F=58|tau||F|` |
| 8 | AQ1 Nachtergaele–Sims placement (HNM-AQ1.3) | new constant | `||Phi||_F<=2268|tau|` | `||Phi||_F<=81J'=2349|tau|`; `||F||<=7`, `C<=224` unchanged |
| 9 | AQ1 stationarity, GNS continuity, Stone | verbatim | | same |
| 10 | AQ1 nonnegativity (Fourier on `(-inf,0)`) | verbatim | | same |
| 11 | AQ1/AQ2 gauge invariance, Haar projection, physical density | verbatim | | same |
| 12 | AQ2 physical gap alpha/16, simple vacuum | new constant (premise) | AM2 full-Hilbert gap at `J_0` | AX1 full-Hilbert gap at `J_0'` (value unchanged) |
| 13 | AQ2 Wilson-cover reset (HNM-AQ2.8) | new constant | `98|tau|` | `102|tau|` |
| 14 | AQ2 overlap and trace distance (HNM-AQ2.9) | new constant | `eps<=98|tau|`, gap one | `eps<=17|tau|`, gap six |
| 15 | AQ2 reference moments of W | verbatim | one free z link Haar | all 48 cover links Haar |
| 16 | AQ2 variance floor (HNM-AQ2.10) | verbatim | `61999/250000>1/5` | same |
| 17 | AT4 Duhamel slope (F10–F11) | new constant | `49|tau|/8`, `k=49|tau|/4` | `51|tau|/8`, `k'=51|tau|/4` |
| 18 | AV1 state-lemma tiers | new constant | `J=28`, `t_1=49`, `a_1=82` | `J'=29`, `t_1'=52`, `a_1'=88` (per `|tau|` or `|tau|/144`) |

Notes on the new constants:
- **AQ1 reset (row 6).** Resetting F to `P_F` changes only the groups meeting F. There are at most `4|F|` stars (anchors in `F-S`) and exactly `|F|` single-factor groups, each changing by at most twice its norm.
- **Nachtergaele–Sims (row 8).** Every group has l1 diameter at most 2, so `1/F(d)<=81`. A single-site group contributes only at `x=y`, where `F(0)=1`. The on-site operators stay unbounded self-adjoint Casimir sums, and `psi_b` is a bounded one-site interaction; equivalently, it may be absorbed as a bounded on-site perturbation.
- **AQ2 reset (rows 13–14).**

\[
\omega(h_R)\le2\big(7\cdot7|\tau|+2\cdot|\tau|\big)=102|\tau|,\qquad h_R\ge6(I-P_R)\Rightarrow \epsilon_R\le17|\tau|,\qquad \|\rho_R-P_R\|_1\le2\sqrt{17|\tau|}\le\tfrac1{500}.
\tag{HNM-AX1-R10}
\]

`h_R>=6(I-P_R)` follows from `Q_0 x I+I x Q_{e_z}-(I-P_0 x P_{e_z})=Q_0 x Q_{e_z}>=0`. **The gap six is load-bearing.** With the selected-strip gap one, `102|tau|=1.02x10^-6>10^-6`, and the verbatim AQ2 bound `1/500` would fail. The trace-distance bound is a square-root control only.

**Unproved named constants: none.** Route-B physical time, clock and centring are those of AQ1/AT4: `theta=alpha t/hbar`, `G=H/alpha`, and actual ground subtraction.

## 5. Incidence on R and no double counting (items 5 and 10)

**All sizes.** A group meets R iff its support meets R:
- for stars, iff `b in R-S={0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y}` (seven anchors);
- for single-factor groups, iff `b in R` (two).

`b+S` lies in `[-N,N]^3` iff `b` lies in `[-N,N-1]^3`. The anchors in `R-S` have coordinates in `{-1,0,1}`, so all seven are retained for every `N>=2`. The single-factor groups are retained for every `N>=1`. The checker verifies the coordinate condition for `N=2..11` and enumerates `Lambda_2` and `Lambda_3` (7 stars and 2 groups each). In `Lambda_1` only 4 of the 7 stars are retained.

**Itemized table** (every face is listed by class, anchor and fine base in `results.json → incidence.table`):

| group | anchor | faces | faces owning a link in R | faces inside R | norm (`G=H/alpha`, per `|tau|`) |
|---|---|---:|---:|---:|---:|
| single-factor `psi` | (0,0,0) | 3 | 3 | 3 | 1/8 |
| single-factor `psi` | (0,0,1) | 3 | 3 | 3 | 1/8 |
| star `phi` | (-1,0,0) | 21 | 4 | 0 | 7/8 |
| star `phi` | (-1,0,1) | 21 | 4 | 0 | 7/8 |
| star `phi` | (0,-1,0) | 21 | 8 | 0 | 7/8 |
| star `phi` | (0,-1,1) | 21 | 8 | 0 | 7/8 |
| star `phi` | (0,0,-1) | 21 | 16 | 0 | 7/8 |
| star `phi` | (0,0,0) | 21 | 21 | 10 | 7/8 |
| star `phi` | (0,0,1) | 21 | 21 | 0 | 7/8 |
| **total** | 9 groups | **153** | **88** | **16** | **51/8** |

**No double count.** A face `(b,k)` has one anchor and one class. Stars hold only the 21 omitted classes, and single-factor groups only the 3 selected classes. The two families are therefore disjoint, and the 153 charged faces are distinct. The checker verifies this across rows and requires that all 88 faces owning a link in R are charged. The 65 charged faces that do not touch R are charged in full, as in AT4.

\[
\|B_N\|\le7\cdot\frac{7|\tau|}{8}+2\cdot\frac{|\tau|}{8}=\frac{51|\tau|}{8},\qquad k'=2\|B_N\|\|W\|=\frac{51|\tau|}{4}\quad(G=H/\alpha).
\tag{HNM-AX1-R11}
\]

The cover is unchanged: 48 links, 36 endpoints (22 per factor, 8 shared). W is the omitted class xz with `r=0`, `s=0`, anchored at 0. Two selected faces share one link with W: the xy faces with `r=0`, `s=0` at 0 and at `e_z`. Both are charged in the two single-factor groups.

## 6. State-lemma constants for route B (item 6)

**Product ordering with the enlarged creation set.** The AV1 split is purely algebraic in the commuting creations `c_I`:
- `psi=psi_out+delta`, `(P_R x 1)psi=psi_out`, `<psi_out,delta>=0`;
- `Tr(rho_{N,R}P_R)=1/(1+e^2)` with `e<=eps`;
- `eps` sums the creations meeting R and the disjoint pairs `I∋0`, `J∋e_z`.

It holds verbatim. What is new is that selected faces create **single-site first-order creations** `c^(1)_{b}`. In the zero-selected model every first-order support had at least two sites. Those creations are counted in `a_1'` (the six faces inside R with owner sets `{0}` and `{e_z}`) and in the two-creation term `T'^2`.

**First-order vector.** Every face, omitted or selected, gives a vector `W_f Omega_0` with spin 1/2 on its four links. It is an `H_0` eigenvector with eigenvalue `8*4*3/4=24`, it lies in the sector of its owner set `M_f`, and it has norm 1/2. Distinct plaquettes share at most one link, so these vectors are orthogonal. Hence

\[
c^{(1)}_M=H_M^{-1}P_MV\Omega_0=-\frac{\tau}{72}\sum_{f:M_f=M}W_f\Omega_0,\qquad \|c^{(1)}_M\|=\frac{|\tau|}{144}\sqrt{n_M}\le\frac{|\tau|}{144}n_M .
\tag{HNM-AX1-R12}
\]

**Counts derived from the 24 classes.** Face `(b,k)` owns links of `b+K_k`. The faces owning a link of u are therefore `(u-v,k)` with `v in K_k`:

\[
\#\{f:u\in M_f\}=\sum_{k=1}^{24}|K_k|=\underbrace{24}_{0}+\underbrace{4}_{e_x}+\underbrace{8}_{e_y}+\underbrace{16}_{e_z}=52=49_{\rm omitted}+3_{\rm selected},\qquad \#\{f:M_f\cap R\ne\varnothing\}=52+52-16=88,\qquad \#\{f:M_f\subseteq R\}=16 .
\tag{HNM-AX1-R13}
\]

There are 16 owner sets per factor, with multiplicities `{1x5,2x3,3x3,4x3,10x2}`; the new owner set `{u}` holds 3 faces. A brute-force enumeration over fine plaquettes, without the class table, reproduces 52, 88, 16 and the 3 selected faces. So do the boxes `N=2,3`: the maximum is 52 at every bulk site, with smaller counts on the boundary.

**Finding on the contract candidates.** The contract's "96 per factor" and "168 for R" are the anchor-group bounds:
- 96 = 4 anchors × 24 anchored faces, since every face owning a link of u is anchored in `u-S`;
- 168 = 7 × 24.

As exact counts they are not reproduced; the exact values are 52 and 88. They are accepted only as labelled bounds, and the checker rejects 96 used as an exact enumeration.

**Tier (i), crude.**

\[
t\le J'G(R)<29|\tau|\cdot\tfrac{148}{7},\qquad \varepsilon_i=2t+t^2,\qquad D'_i:=2\varepsilon_i\ \ge\ \frac{2\varepsilon_i}{\sqrt{1+\varepsilon_i^2}} .
\tag{HNM-AX1-R14}
\]

At `tau=±10^-8`, `t<=1073/175000000`, which is the self-map rational. This gives `D'_i=375551151329/15312500000000000 ≈ 2.4526e-5`. Four directed majorant iterations give about `1.8562e-5`. Tier (i) fails `4/10^7` and is retained as a limited-tier value.

**Tier (ii), exact first order.** By the AM2 multilinear bound and the convexity of G,

\[
\|c-c^{(1)}\|_a\le J'(G(t)-16)\le 352J't\ (t\le R)\ \Rightarrow\ t\le T':=\frac{t_1'}{1-352J'},\qquad \rho':=352J'T'>0,
\tag{HNM-AX1-R15}
\]

\[
\varepsilon'_{ii}=a_1'+2\rho'+T'^2,\qquad t_1'=\frac{52|\tau|}{144},\quad a_1'=\frac{88|\tau|}{144},\qquad D'_{ii}:=2\varepsilon'_{ii}\ \ge\ \frac{2\varepsilon'_{ii}}{\sqrt{1+\varepsilon'^2_{ii}}} .
\tag{HNM-AX1-R16}
\]

Values at `tau=±10^-8` (all exact):

| quantity | value |
|---|---|
| `J'` | `29/100000000` |
| `352J'` | `319/3125000` |
| `t_1'` | `13/3600000000` |
| `T'` | `13/3599632512` |
| `rho'` | `4147/11248851600000000 ≈ 3.6866e-13` |
| `a_1'` | `11/1800000000` |
| `T'^2` | `≈1.3043e-17` |
| `eps'_ii` | `30934916107401289/5061466492752902400000000 ≈ 6.1118e-9` |
| **`D'_ii`** | **`30934916107401289/2530733246376451200000000 ≈ 1.22237e-8`** |

Both signs give the same value: only `|tau|` enters, so the `-tau` value is a replay. The margin against the target `1/2500000` is about 32.72.

Variants (all at both signs, all below `4/10^7`):

| variant | D' (preview) | backing |
|---|---:|---|
| headline: exact counts, `2eps` | 1.222370e-8 | fidelity inequality (exact rational) |
| exact counts, density form `2eps(1+eps)/(1+eps^2)` | 1.222370e-8 | both admitted inequalities (exact rational) |
| directed remainder `J'(G^+(T')-16)` | 1.222343e-8 | fidelity |
| owner-set orthogonal (`sqrt(n_M)`) | 6.521621e-9 | fidelity, directed square roots |
| global two-site `eps=2T'+T'^2` | 1.444592e-8 | fidelity; the density form of this variant is also below target |
| labelled bounds 96 / 168 | 2.333606e-8 | fidelity; the contract's "about 2–3e-8" |

All variants scale linearly: `D'(tau)/D'(tau/100) ≈ 100.012` for tier (ii) and `100.0003` for tier (i), against exactly 10 for the square-root reset `2sqrt(17|tau|)`.

**Consequences.** For both tiers and both signs:
- `|omega(W)|<=D'`;
- `|omega(W^2)-1/4|<=D'/2`, by the trace-zero effect bound;
- `1/4-D'/2-D'^2<=Var(W)`.

`D'_ii>=|tau|/144`, so the first-order mean is paid for.

**Error ledger** (the six preregistered names):

| term | treatment |
|---|---|
| `am2_remainder` | `2rho'=4147/5624425800000000` |
| `two_creation` | `T'^2`, which now includes the single-site selected creations at 0 and `e_z` |
| `straddling` | inside `a_1'` (72 of the 88 faces have owner sets straddling R) and `2rho'` |
| `density` | not applicable, with reason: the fidelity route bounds the whole distance through `Tr(rho_R P_R)=1/(1+e^2)` |
| `onsite_cutoff_vector` | 0: the AV1 R20–R21 uniform-gap argument with the re-frozen gap 1/2, and `Q_L W_f Omega_0=W_f Omega_0` for `L>=24` |
| `arithmetic` | 0 for the exact rational `2eps`; outward rounding at `10^-40` for the directed fidelity value |

**Cutoff and passage.** AV1's vector argument uses only a uniform cutoff gap (now from R09) and the uniqueness of the untruncated ground, so it applies verbatim. So does passage by local trace-norm convergence to **every** subsequential limit of AQ1's construction. This is not uniqueness, whole-sequence convergence or a rate in N.

**AX2 relation (read, not targeted).** The window budget is

\[
2(D'+D'^2)+\frac{51|\tau|}{\pi}\le10^{-6},
\tag{HNM-AX1-R17}
\]

where `k'M_1=(51|tau|/4)(4/pi)` at `s=1`. It holds for `D'_ii`, for every tier-(ii) variant and for the target `4/10^7`. It fails for `D'_i`. With Machin brackets on pi, the exact threshold lies in `[418830803603891331276477509463097/10^39, 4188308036038913312764775094630971/10^40]`, about `4.18831e-7`.

**Finding:** the contract's "`D'<=4.19x10^-7`" is rounded up, and `4.19x10^-7` itself is infeasible. This is non-blocking, because the tested target is `4/10^7`.

## 7. Transfer of the flip identity to the uniform model (item 9, proved)

**Grading unitaries.** For a link l, let `(Gamma_l psi)(U)=psi(...,-U_l,...)`. Haar measure is invariant under the central `-1`, so `Gamma_l` is unitary and fixes constants. On the spin-j Peter–Weyl block it acts as `(-1)^{2j}`, so it commutes with `C_l`. Because `-1` is central, it commutes with every left and right translation, and hence with every endpoint gauge action.

**Odd intersection.** Let `E={(p,x):p_y even} ∪ {(p,y):p_z even} ∪ {(p,z):p_x even}`, the AW1-admitted set. In an xy face, the two x links differ only in `p_y` and the two y links share `p_z`; this gives `1+{0,2}` links in E. The xz and yz orientations are analogous. Every plaquette of Z³ therefore meets E in 1 or 3 links. The checker verifies:
- all 24 residue cases;
- every plaquette of the fine box `[-6,6]^3`: 3042 meet E once, 3549 three times, and none evenly;
- all 1719 faces of the route-B box `Lambda_2` (1344 omitted and 375 selected).

**The uniform identity.** Put `U_E=prod_{l in E cap Lambda}Gamma_l`. It commutes with every `C_e`, hence with `h_b`, `P_b`, every on-site spectral cutoff `1_[0,L](h_b)` and every gauge action, and it maps each `W_f` to `-W_f`. In route B every face term is `-(tau/3)W_f`, **selected faces included**, because the selected coefficient is `nu=alpha*tau/24`, tied to tau. So

\[
U_EH_N(\tau)U_E^*=H_N(-\tau)\quad\text{in every centred box and every cutoff compression }Q_LH_NQ_L .
\tag{HNM-AX1-R18}
\]

Two differences from AW1:
- The patterned identity `(tau,kappa)->(-tau,-kappa)` becomes `tau->-tau` for the uniform model, because `kappa(tau)=tau/24` is odd.
- Unlike AW1's `kappa≠0` case, route B needs no inherited strip-operator form: the reference and cutoffs are Haar/Casimir objects that `U_E` fixes.

**Consequences.** The finite grounds are unique (R09). So `U_E psi_N(tau) ∝ psi_N(-tau)`, and:
- `omega_{N,-tau}(W)=-omega_{N,tau}(W)`;
- `omega_N(W^2)`, `C_N` and `c_N` are even in tau;
- for AQ limits, `S(-tau)=S(tau)∘alpha_E` as whole sets of subsequential limits, holding pointwise only along a common subsequence.

**Oddness gives no `O(tau^3)` remainder.**

**The tie is essential.** `U_E` always maps `(tau,kappa)` to `(-tau,-kappa)`. The checker applies it face by face on `Lambda_2` under five selected-coefficient rules:

| rule | `U_E H(tau)` equals the model's `H(-tau)` | status |
|---|---|---|
| `kappa=tau/24` (tied) | yes | the uniform model |
| `kappa=|tau|/24` (mixed sign) | no | identity breaks |
| `kappa=tau/24+1/7` (offset) | no | identity breaks |
| `kappa=tau/12` | yes | odd, but not uniform (rejected as uniform) |
| `kappa=0` | yes | the zero-selected model, not uniform |

A decoupled one-plaquette fixture (`j<=1/2` truncation, exact in `Q(sqrt d)`, a finite graph with `transfers_to_aq:false`) gives the selected-face ground mean `<W_g>=k/(2sqrt(576+k^2))` with `k=8kappa`. It is odd in tau for the tied rule and fails oddness for the mixed-sign and offset rules. For the uniform coefficient `k=tau/3` its sign is the sign of tau, and its first-order value is `k/48=tau/144`.

## 8. Transfer of the parity theorem and of +tau/144 (item 9, proved)

**Parity.** A Haar integral of a product of plaquette variables vanishes whenever some link carries an odd number of spin-1/2 factors. This is the `Gamma_l`-odd case: the trivial representation does not occur in a tensor product with an odd number of spin-1/2 factors at that link. A selected face is a single-face character `W_g=Tr U_g/2`, exactly like an omitted face. In route B, V is `-(tau/3)` times a sum of single-face characters, so the grading argument applies verbatim. Concretely:
- **`E[W^2 W_f]=0` for every face f**, selected faces and `f=W` included. For `f≠W`, the three or more links of f outside W each carry one spin-1/2 factor; for `f=W`, every link carries three. The checker verifies this for all 88 faces meeting R.
- **`E[W W_f]=0` for `f≠W`**, and `1/4` for `f=W`. So the state term `2Re<psi^(1),W^2 Omega_0>`, the Duhamel term and the energy term `E^(1)=<Omega_0,V Omega_0>` all vanish at first order, and first-order `omega(W^2)`, `c(theta)` and `C(s)` vanish in every finite box.
- **Degenerate multiplet.** For every face f, the odd-link set `W△f` has size 0 (only `f=W`), 6 (12 faces: 10 omitted and the 2 selected faces above) or 8 (all 1706 others in `Lambda_2`). Energy-24 vectors have exactly four odd links, so `P_24 V W Omega_0=0`. `E[W_gW_fW_h]=0` for all 117,480 multisets of faces meeting R, because each face meets E oddly and the Z_2 chain `g+f+h` therefore cannot vanish. The invariant multiplet has zero first-order splitting.

**First-order Wilson mean.** Rayleigh–Schrödinger with the I1.5 sign gives `psi^(1)=+(tau/72) sum_f W_f Omega_0 = -c^(1)`, where the sum now runs over omitted **and** selected faces. Then

\[
\omega_\tau(W)=2\,\mathrm{Re}\langle W\Omega_0,\psi^{(1)}\rangle+O(\tau^2)=-2\,\mathrm{Re}\langle W\Omega_0,c^{(1)}\rangle+O(\tau^2)=2\cdot\frac{\tau}{72}\cdot\mathbb E[W^2]+O(\tau^2)=+\frac{\tau}{144}+O(\tau^2),
\tag{HNM-AX1-R19}
\]

because only `f=W` pairs with W. The selected faces are distinct plaquettes and contribute zero. Kato analyticity holds per box: `H_N(tau)=H_0+tau V'` with V' bounded and gap at least 1/2 for `|tau|<=10^-8` (R09).

**Quantifiers that transfer verbatim:**
- the finite-box parity theorem, including that the `C_N(s)` `tau^2` constant stays unbounded and not uniform in N;
- the flip identity, now `H(tau)->H(-tau)`;
- finite-box antisymmetry and evenness;
- the set-level AQ statement;
- no `O(tau^3)` claim;
- the coefficient `+tau/144` and its orientation invariance.

**Quantifiers that need route-B constants (not done here):**
- the second-order remainder `K_2` (`J'=29|tau|`, `t_1'=52|tau|/144`, and single-site first-order creations now entering the two-creation and density terms);
- the supplementary `omega(W^2)` constant;
- the AW2 enclosure and its decade-grid coupling rule;
- every uniform-in-N `tau^2` constant.

The AW1 remark that "every first-order support has at least two sites" is **false in route B**.

## 9. Controls and checker (item 7)

`check.py --output <absolute fresh dir>` uses the standard library only.

- **Before evaluation.** It records its own sha256, verifies the contract snapshot hash, and reads the following from the contract:
  - the cap, the signs and the uniform triple;
  - the box bounds;
  - the target `1/2500000`;
  - the reference values `0 and 1/4` and the route `haar`;
  - the R1 texts;
  - the reset, incidence, first-order and dictionary texts;
  - the AX2 relation.
- **Comparison order.** Every contract number is compared only after the independent derivation.
- **Inherited gates.** It reads the AM2 cap, the AL1 dictionary, the AW1 flip set and coefficient, and the AV1 value from the snapshotted gates.
- **Output.** It writes `results.json` (sorted keys, 58 checks) and `source-manifest.json`, byte-identical under `python3 -B` and `python3 -B -O`.

All 28 contract controls are damaging mutations whose rejection is required; a rejection is an explicit exception, never an assert. `reverse_premise_isolation` is additionally a positive check that the inventory equals the declared premises.

| control | mutations rejected |
|---|---|
| missing_incoming_stars | outgoing anchors only; `J=8|tau|`; reset from two stars |
| full_original_wilson_cover | cover `{0}`; cover with an extra factor |
| wrong_delta_alpha_hbar_clock | unit-mixed face coefficients; energy 24 labelled alpha; normalized slope `102|tau|` as `k'`; slope in delta units |
| vector_versus_scalar_centering | variance bounds without `m^2`, for both tiers |
| first_order_mean_charged | second-order-only budget; zero budget |
| tau_scaling_exponent | the square-root reset labelled linear |
| changed_model_relabelled | zero or ends-only triple as uniform; coupling above the cap; route-A reference labelled B |
| coherent_evidence_tampering | 11 coherently rehashed contract tampers (J_0' old value, 28 split, reset 98, seven groups, bound 49, wrong g^4 decade, target 1/1000, cap 1e-7, triple tau/12, strip reference, control removed) and a byte change |
| insufficient_verdict_retained | crude-only, unproved-constant and over-target outcomes relabelled accepted; contraction failure relabelled limited |
| exact_arithmetic_admission | float, bool, NaN and `1/0` inputs; float admission |
| root_n_misuse | `sqrt(52)` and `sqrt(88)` as anchored sums |
| no_priority_or_continuum_claim | each forbidden flag set true; uniform claim without the fixed-spacing label |
| uniform_triple_in_box | ends-only triple; `tau=4` (bridge 1/6); `tau=16` (ends 2/3); two entries |
| selected_reference_not_haar | Haar claimed as the route-A on-site ground at `±tau` |
| reference_route_declared | undeclared route; route A with Haar; route B with the selected faces on site; route B without single-factor groups |
| per_site_sum_recomputed | 28, 32 (merged grouping), 7, 30 |
| reset_budget_recomputed | 98 (AQ2 verbatim), 100, 112; overlap with gap one |
| selected_incidence_count | 7, 0, 1 groups |
| first_order_faces_uniform | omitted-only 49; 96 copied as exact; hard-coded 52; bound 96 used as exact; count restricted to 0 and `e_z` |
| uniform_label_strong_coupling | weak-coupling and continuum labels; `g^4=96 tau` and `24/tau`; label without "fixed spacing" |
| am2_gap_reuse_justified | route B citing the frozen `J_0`; gapless on-site; support 5; copied order-six termination; route A with Haar; undercounted `J=28` |
| j0_resolution_declared | old `J_0` at the cap; R2 with the changed cap; contraction undeclared; stale self-map `148/25000000` |
| uniform_sign_convention | selected faces with `+tau/3`; alpha-unit magnitude in the normalized packet; omitted faces flipped |
| tier_mixing_rejected | exact `a_1` with the crude remainder; refined t without self-consistency; first order inside tier (i) |
| reverse_premise_isolation | triage, loop-2 response, expert file, forward AX1 report or deliberation added; a premise dropped |
| uniform_kappa_tied_to_tau | rules `|tau|/24` and offset (the flip identity breaks); `tau/12` and 0 (odd, but not uniform) |
| route_b_no_double_count | star plus single-factor duplicate in `Lambda_2`; double-counted sum 33; incidence table with a duplicate |
| incidence_table_itemized | asserted totals without a table; rows without faces; the `-e_x` star missing (4 faces touching R uncharged) |

**Claim flags:**
- `continuum_claim:false`
- `uniform_wilson_claim:true`, only for the fixed-spacing model as labelled
- `weak_coupling_claim:false`
- `resolved_interaction_shift:false`
- `scientific_priority_verified:false`
- `euclidean_node_certified:false`

## 10. Limitations and exclusions

**Claim exclusions, exactly as the contract lists them:**
- weak coupling or continuum
- a uniform-model Euclidean datum (AX2)
- a uniform Wilson-mean sign certificate
- AQ uniqueness or a rate in N
- scientific priority

**Preregistered exclusions, also respected:**
- free reference inside enclosure => no interaction claim;
- uniqueness of the AQ state;
- whole-sequence convergence or rate in N;
- continuum or weak coupling;
- transfer from a finite graph;
- relabelling a static shift as dynamical;
- scientific priority.

**Scope and honest gaps:**
- **Model and coupling.** Fixed spacing and strong bare coupling only: `|tau|<=10^-8`, `g^4>=9.6x10^9`. `tau<0` is the `U_E` image of the `tau>0` model, not a real-g coupling.
- **Boundary.** The whole-star box boundary keeps every selected face. It is not identified with the all-contained-plaquette boundary (AL1).
- **Finite volume and AQ limits.** The finite-volume gap is uniform over boxes. The AQ statements concern every subsequential limit; there is no uniqueness, whole-sequence convergence or rate in N.
- **Inherited without re-proof** (re-instantiated with the new constants):
  - AM2's multilinear majorant, fixed point, exclusion and cutoff passage;
  - AQ1's compactness and Nachtergaele–Sims dynamics;
  - AQ2's Fourier gap passage;
  - AV1's product split, cutoff-vector removal and AQ passage;
  - the I1 dictionary.
- **Route A.** The route-A cross-check of the gap rests on the inherited A1 strip theorem, which I did not read.
- **Upper certificates only.** There is no value or sign of `omega(W)` beyond `|omega(W)|<=D'`. The first-order coefficient transfers, but `K_2` is not re-derived.
- **Headline backing.** The headline `D'_ii=2eps` rests on the fidelity inequality. The density-form value, certified by both admitted inequalities, is also below target.
- **Visibility of the constants.** The contract text states the grouping, `29|tau|`, `J_0'`, the two rationals, `102|tau|`, the incidence counts and the candidates 96/168. My derivations recompute them and compare afterwards; they were not discovered blind. The reverse contribution is the independent reconstruction, the count correction (52/88 against 96/168) and the rounding finding on `4.19x10^-7`.
- **Fixtures.** They are finite graphs or algebras (`transfers_to_aq:false`). They audit the algebra and the rejection logic.
- **Arithmetic.** Arithmetic is exact rational, and decimals are truncated previews.
- **Priority.** Scientific priority is unverified.

**Steps not completed:** none of items 1–10 is left incomplete on the reverse route.

## 11. Reads, scratch and independence

**Inputs.** I read the contract first, then the snapshots in `inputs/`: AGENTS.md; the AV1/AV2/AW1/AW2 contracts and gates; the AV1/AV2/AW1 forward and reverse reports and skeptic reviews; the AM2 reports, review and gate; the AQ1, AQ2, AT4 and I1 reports; the AL1 report and gate; selection-ax1. The method-skill snapshots are declared premises; I applied their rules through this report's structure and did not rely on them for any mathematical step.

**Extra inherited files:**
- `research/round32/tools/README.md` and `research/round32/tools/freeze.py`, for the protocol;
- `research/round32/reverse/av1/check.py`, for code style;
- the line count of `research/round32/reverse/aw1/check.py`, without reading its content.

**Incidental exposure.** A `git status` call printed the names of four untracked files under `research/round32/experts/modern/assistant-2/`. I did not open them.

**Scratch.** My scratch work stayed in `/tmp/claude-0/ax1-reverse-private/`, and the checker ran in `/tmp/claude-0/ax1-reverse-run*`. **I read no other scratchpad file.**

**Method lenses** (modern lenses only; no historical figure endorses anything here):
- *Newton analysis/synthesis:* Section 1 runs backwards from "Haar is needed" to the grouping and the `J_0` issue, and then forwards.
- *Tesla source/load/transfer:* the sources are the seven stars and two single-factor groups, the load is the cover R, and the transfer element is the local Duhamel slope `k'`.

## Reproduce

```bash
python3 -B research/round32/reverse/ax1/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/reverse/ax1/check.py --output /absolute/fresh/dir2
python3 -B research/round32/tools/freeze.py verify research/round32/reverse/ax1
```
