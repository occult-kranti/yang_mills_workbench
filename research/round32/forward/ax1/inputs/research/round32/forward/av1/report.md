# Hruday first-order local state lemma — AV1 forward (product ordering and explicit reduced density)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production under the frozen AV1 contract (`research/round32/contracts/av1.json`, sha256 `c7018519188b953e48e56715a72c90491389e42243ef691cb59dc5b038e91e40`). The product-ordering idea and the location of the normalization trap are **shared panel premises**, as the contract's `premise_note` says. They reached this producer through the snapshotted forward-additional premises: the skeptic's triage (c)1, the prospective controls, the skeptic's loop-2 response, deliberation-1, the historical and Jung loop-2 responses, and the AT4 reverse report. The forward producer read all of these and discloses them. Independence is claimed only for the inequality, the constants, the enumeration, the cutoff step and the passage step. Even there the work is correlated model-agent production, not independent human review. Nothing under `research/round32/reverse/`, any other Round32 producer directory, or any skeptic file outside the snapshots was read.

**Inherited inputs read** beyond `inputs/`: `research/round32/tools/README.md` and `research/round32/tools/freeze.py` (protocol only), `research/round29/forward/am2/check.py` (code style, plus the admitted four-qubit creation-termination fixture, which is re-run here as an audit), and `research/round31/forward/at5/check.py` (code style only).

HNM labels are project aliases. Commuting nilpotent creation-operator expansions are established mathematics. The project attributes them to Bravyi–DiVincenzo–Loss through its Gauvin diff record, which is not among this producer's inputs and was not read. AM2's reverse report names Gauvin arXiv:2503.15539v3, supplement A.6–A.8, as its inspected template. The trace-distance, pure-state and Eckart inequalities, Cauchy–Schwarz and the Weyl integration formula are standard. Scientific priority is unverified.

**Verdict (forward route).** The product-ordering route is proved for the AM2/AQ1 zero-selected patterned family at both signs of `|tau|<=10^-8`. Let `t=||c||_a` be the anchored norm of the AM2 creation collection. Then every centered whole-star box `Lambda_N`, `N>=2`, satisfies

`||rho_{N,R}-P_R||_1 <= D(t) := 2 eps(1+eps)/(1+eps^2)`, where `eps = 2t+t^2`.

The bound is uniform in `N`. It survives removal of the onsite spectral cutoff, which is proved here for the ground **vector**, and it passes to every subsequential AQ1 limit by local trace-norm convergence. There are two tiers:
- **Tier (i)**, the crude AM2 majorant: `D_i ≈ 2.36803504623×10^-5` at `tau=±10^-8`. This is about 34 times below AT4's square-root bound, but it fails both `4/10^7` and `10^-6`. The value is retained.
- **Tier (ii)**, the exact first-order coefficient with the self-consistent AM2 remainder: `D_ii ≈ 1.36124528702×10^-8` at both signs. This meets the preregistered target `D_ii<=4/10^7` with a factor of about 29.4, and it also meets `10^-6`.

Both tiers scale linearly in `tau`. Their exact ratios `D(10^-8)/D(10^-10)` lie in `[99,101]`, while the AT4 ratio is exactly 10. On the forward side every contract item assigned to this producer is complete, and every one of the 25 contract controls rejects its damaging mutation. The forward producer therefore proposes **accepted_within_scope for the forward half**. The contract's acceptance also requires the reverse (fidelity) route and independent skeptical review, which are outside this producer's work. A failed upper certificate would not have been a lower bound, and no lower bound on the actual distance is claimed.

## 1. Model, AM2 objects and constants (item 1)

The model is the SU(2) Kogut–Susskind form on `Z^3` at fixed spacing. Coarse factor `b` owns the 24 positive links whose tails are `(4b_x+r, 2b_y+q, b_z)`, with `r=0..3` and `q=0,1`. All original endpoint gauge actions are retained. The selected triple is exactly `(0,0,0)`, so in normalized units `delta=alpha/8` the onsite operator (I1.3 at zero selected coupling) is the pure Casimir sum

\[
 h_b=8\sum_{e\text{ owned by }b}C_e,\qquad h_b\ge 6Q_b\ge Q_b,\qquad
 P_b=|1_b\rangle\langle 1_b|\ (\text{Haar}),\qquad Q_b=I-P_b .
 \tag{HNM-AV1-F01}
\]

The ground scalar is zero. The gap is `8·(3/4)=6`, and AM2 uses only `h_b>=Q_b`. Each anchor carries 21 omitted faces with coefficient `alpha tau/24`. Grouped into whole stars (I1.5), they give

\[
 \phi_b=-\frac{\tau}{3}\sum_{f\in O_b}W_f,\qquad \|\phi_b\|=7|\tau|,\qquad
 \widehat H_N=\sum_{b\in\Lambda_N}h_b+\sum_{b+S\subset\Lambda_N}\phi_b=:H_0+V,
 \tag{HNM-AV1-F02}
\]

where `S={0,e_x,e_y,e_z}` and `Lambda_N=[-N,N]^3`. Each site lies in exactly four stars `b in u-S`, **incoming stars included**, so `J=max_u sum_{X ni u}||V_X|| <= 4·7|tau| = 28|tau| <= J_0 = 7/25000000`. The one-star value `7|tau|` is a rejected control.

**AM2 objects.** For every nonempty `I subset Lambda`, a creation vector satisfies `c_I in ⊗_{x in I} Q_x H_x` and defines `ĉ_I=|c_I><Omega_I| ⊗ 1`. Creations commute, and `ĉ_Iĉ_J=0` whenever `I cap J` is nonempty. Put `C=sum_I ĉ_I` and `||c||_a=max_{u in Lambda} sum_{I ni u}||c_I||`. In each onsite cutoff space `⊗_x 1_[0,L](h_x)H_x`, AM2 proves that there is a unique fixed point with

\[
 c=\sum_{k=0}^{8}\frac{L_k(c,\ldots,c)}{k!},\qquad \|c\|_a\le R=\tfrac1{64},\qquad
 \psi=e^{-C}\Omega_0\ \text{the unique ground, gap}\ \ge\tfrac12,
 \tag{HNM-AV1-F03}
\]

where `(L_k)_M = H_M^{-1}P_M ad_{C_1}...ad_{C_k}(V)Omega_0` and `||L_k|| <= J·16·8^k(1+5k/4)·prod||c_j||_a`. The constants are re-evaluated exactly. The series `sum_{k<=12}(1/8)^k/k!`, plus its geometric tail bound, gives `exp(1/8) < 53823253862885575661009/47498854821020880076800 < 8/7`. Hence

\[
 G(t)=16e^{8t}(1+10t),\quad G(R)<\tfrac{148}{7},\quad G'(R)<352,\quad
 J_0G(R)<\tfrac{148}{25000000}=\tfrac{37}{6250000}<R,\quad 2J_0G'(R)<\tfrac{77}{390625}<1 .
 \tag{HNM-AV1-F04}
\]

The coefficients `16·8^k(1+5k/4)` equal `k!` times the Taylor coefficients of `G` for `k<=8`. The re-run four-qubit fixture gives `ad_C^8(V)Omega=8!|1111>` and `ad_C^9(V)=0`. The fixed-point equation and (HNM-AM2.5) give the two majorant inequalities used below:

\[
 \|c\|_a\le J\,G(\|c\|_a),\qquad \|c-L_0\|_a\le J\,\bigl(G(\|c\|_a)-16\bigr).
 \tag{HNM-AV1-F05}
\]

**AQ1's boxes are AM2's family.** A coarse translation by `(N,N,N)` is the fine translation `(4N,2N,N)`. It preserves the residues `x mod 4` and `y mod 2`, the selected strips, link ownership and whole-star retention. So `Lambda_N` is unitarily a relabelled translate of the I1 complete-factor volume `Lambda_N+(N,N,N)` in the positive orthant, and every retained star `b+S subset Lambda_N` maps to a retained star there. The checker verifies this for `N=2,3`. At the zero triple the onsite reference is the Haar product of (F01) in both constructions. AM2's proof uses only `h_x>=Q_x`, star supports and `J`. No Yarotsky, HTW or Gauvin constant enters. AQ1's finite states are the unique full-Hilbert ground states of `Ĥ_N` that AM2 constructs. That ground is gauge invariant, so it is also the physical ground.

## 2. Product ordering, orthogonality and the two-creation term (item 2)

Because the creations commute and `ĉ_I^2=0`,

\[
 e^{-C}=\prod_{I}(1-\hat c_I).
 \tag{HNM-AV1-F06}
\]

Split the supports into `A={I: I cap R ≠ ∅}` and `B={I: I cap R=∅}`, with `R={0,e_z}`. Place the factors in `A` last:

\[
 \psi=\prod_{I\in A}(1-\hat c_I)\,\psi_{\rm out},\qquad
 \psi_{\rm out}:=\prod_{I\in B}(1-\hat c_I)\Omega_0=\Omega_R\otimes\phi_{\rm out}.
 \tag{HNM-AV1-F07}
\]

The factorization holds because every `ĉ_I` with `I in B` acts as the identity on `H_R`. Expand the first product. A product of creations with overlapping supports vanishes. A family of pairwise disjoint sets that each meet the two-site `R` has at most two members, and when it has two, one contains `0` but not `e_z` while the other contains `e_z` but not `0`. Hence

\[
 \delta:=\psi-\psi_{\rm out}
 =-\sum_{I\in A}\hat c_I\psi_{\rm out}
 +\sum_{I\ni0,\;J\ni e_z,\;I\cap J=\varnothing}\hat c_I\hat c_J\psi_{\rm out}.
 \tag{HNM-AV1-F08}
\]

The second sum is the **two-creation term**. Each unordered pair appears once, because disjointness forces `e_z ∉ I` and `0 ∉ J`.

**Orthogonality.** For `I in A` pick `x in I cap R`. The range of `ĉ_I` lies in `(Q_x ⊗ 1)H`, and `(P_R ⊗ 1)(Q_x ⊗ 1)=0` because `P_R=P_0 ⊗ P_{e_z}`. The same holds for the pair products. Therefore

\[
 (P_R\otimes1)\delta=0,\qquad (P_R\otimes1)\psi=\psi_{\rm out},\qquad
 \langle\psi_{\rm out},\delta\rangle=0 .
 \tag{HNM-AV1-F09}
\]

This uses the premise `c_I in ⊗Q_xH_x`. A "creation" with a vacuum component breaks it (Section 4).

**Relative norm.** `||ĉ_I||=||c_I||`, and `<Omega_0,psi_out>=1`, so `psi_out≠0`. Every support meeting `R` contains `0` or `e_z`. This includes the **straddling supports**, which meet both `R` and its complement. Hence `sum_{I in A}||c_I|| <= sum_{I ni 0} + sum_{I ni e_z} <= 2t`. A support that contains both sites is counted twice, which only enlarges the bound. The pair sum is at most `(sum_{I ni 0}||c_I||)(sum_{J ni e_z}||c_J||) <= t^2`. Thus

\[
 \|\delta\|\le(2t+t^2)\,\|\psi_{\rm out}\|=:\varepsilon\,\|\psi_{\rm out}\|,\qquad t=\|c\|_a .
 \tag{HNM-AV1-F10}
\]

The site maximum `t` is used only for the two sites of `R` (`|R| t = 2t`). A per-site maximum summed over the volume would be extensive, and it is a rejected control.

## 3. The explicit reduced density and the trace-distance inequality (item 2)

Put `n=||psi_out||=||phi_out||`, `d=||delta||` and `e=d/n <= eps`. Define the partial inner product

`xi := (1_R ⊗ <phi_out|) delta in H_R`, so that `<v,xi> = <v ⊗ phi_out, delta>`,

and the outside-traced excited block `sigma := Tr_out|delta><delta| >= 0`. Direct partial traces give `Tr_out|psi_out><psi_out| = n^2 P_R`, `Tr_out|psi_out><delta| = |Omega_R><xi|` and `Tr_out|delta><psi_out| = |xi><Omega_R|`. By (F09), `||psi||^2 = n^2+d^2`. Therefore, exactly,

\[
 \rho_{N,R}=\frac{n^2P_R+|\Omega_R\rangle\langle\xi|+|\xi\rangle\langle\Omega_R|+\sigma}{n^2+d^2}.
 \tag{HNM-AV1-F11}
\]

(F09) also gives `<Omega_R,xi>=<psi_out,delta>=0`, `P_R sigma=0` and `Tr sigma=d^2`. Cauchy–Schwarz gives `||xi|| <= n d`. On `span{Omega_R, xi}` the cross operator has eigenvalues `±||xi||`, so its trace norm is `2||xi||`. Since `rho-P_R = [|Omega_R><xi|+|xi><Omega_R|+sigma-d^2 P_R]/(n^2+d^2)`,

\[
 \|\rho_{N,R}-P_R\|_1\le\frac{2nd+d^2+d^2}{n^2+d^2}=\frac{2e(1+e)}{1+e^2}
 \le\frac{2\varepsilon(1+\varepsilon)}{1+\varepsilon^2}=:D(t).
 \tag{HNM-AV1-F12}
\]

For the last step, `f(e)=2e(1+e)/(1+e^2)` has `f'(e) ∝ 2+4e-2e^2 > 0` on `[0,1+sqrt 2]`. If `eps>=1`, then `f(eps)>=2`, which bounds every trace distance between states. The bound depends only on `t`, and Sections 5–6 bound `t` independently of `N`. The volume-dependent norm `n` and the outside vector `phi_out` multiply every term of the numerator and the denominator, so they cancel. At no point is a norm of an outside product estimated.

## 4. The normalization trap and a three-site model-class counterexample (item 3, parts required of each producer)

**Trap.** Both `<psi,A psi>` and `<psi,psi>=n^2(1+e^2)` contain every creation in the box, and `n^2=||phi_out||^2` grows with the volume. There are two tempting shortcuts, and both are wrong:
- Keep only the creations meeting `R` in the numerator and normalize by `1+O(t^2)`, or by the full norm. This gives a volume-dependent, wrong value.
- Drop the outside creations everywhere. This gives a volume-independent but wrong value, because straddling creations couple `R` to the outside excitation amplitudes of `phi_out`.

(F07)–(F11) resolve the trap. The outside vector is a common factor, and only the relative bound (F10) is needed.

**Counterexample (analytic).** Take qubit sites `r` (with `R={r}`), `o` and `o'`, vacuum `0`, and creations `c_{r,o}=a` (straddling), `c_o=b` and `c_{o'}=g`. Then

\[
 \psi=|000\rangle-b|010\rangle-g|001\rangle+bg|011\rangle-a|110\rangle+ag|111\rangle,\quad
 \|\psi\|^2=(1+g^2)(1+a^2+b^2),\quad
 \rho_r=\frac{1}{1+a^2+b^2}\begin{pmatrix}1+b^2&ab\\ab&a^2\end{pmatrix}.
 \tag{HNM-AV1-F13}
\]

This example shows three things:
- **(i) The decoupled creation cancels.** `rho_r` does not depend on `g`, while the unnormalized weight `<psi,P_r psi>=(1+g^2)(1+b^2)` does. At `a=1/3`, `b=1/2` it takes the values `5/4`, `29/20` and `5/2` for `g=0`, `2/5` and `1`. The numerator alone is therefore volume dependent.
- **(ii) Outside creations matter.** `rho_r` depends on the outside creation `b`: for `b=0` the off-diagonal vanishes. The statement "only creations meeting R matter" is false.
- **(iii) Straddling enters only at second order.** The straddling creation enters `e^2=a^2/(1+b^2)` at first order in `a`, but the off-diagonal matrix element only at second order (`ab`). At `a=1/3`, `b=1/2` the exact value is `rho_r=[[45/49,6/49],[6/49,4/49]]`.

A further counterexample shows that the excitedness premise is essential. Replace the creation by an operator with a vacuum component, `|0>_r -> (1/4)|0>+(1/3)|1>`, acting on `psi_out=|00>-(1/2)|01>`. This gives `<psi_out,delta>=-5/16 ≠ 0`, so the split (F09) fails.

**Checker fixture with `|R|=2`.** The three sites `r_0, r_1, o` carry all seven supports, with coefficients `1/60, 1/70, 1/50` inside `R`, `1/9, 1/10, 1/11` straddling and `-1/12` outside. Between zero and three decoupled spectators are added. The checker verifies the following exactly:
- (F06)–(F11), including the three two-creation pairs and `e^{-C}` as a terminating series.
- `rho_R` is identical for every number of spectators, while `<psi,P_R psi>` runs through `145/144, 5365/5184, 198505/186624, 7344685/6718464`.
- The W-like matrix element `<00|rho|11>` has first-order coefficient `-c_{r0r1}=-1/50`. Removing the straddling creations changes it first at order two (`-1/132`), yet they enter `e` at first order.

## 5. Tier (i): crude AM2 majorant (item 4)

From (F05), with `t<=R` and `G` increasing, `t <= J G(R) <= 28|tau|·148/7 = 592|tau|`. At `|tau|=10^-8`:

\[
 t_i=\tfrac{37}{6250000},\quad \varepsilon_i=\tfrac{462501369}{39062500000000},\quad
 D_i=\tfrac{36133347268157653748322}{1525878906463907516326874161}\approx2.36803504623\times10^{-5}
 \tag{HNM-AV1-F14}
\]

This value holds at both `tau=+10^-8` and `tau=-10^-8`, because only `|tau|` enters. Iterating once with the directed enclosure `e^{8t} <= 1/(1-8t)` gives `t <= J·16(1+10t_i)/(1-8t_i) = 4375259/976516250000`. Then `D_{i,iter} ≈ 1.79221103916×10^-5`; the exact rational is in `results.json`. Tier (i) fails `4/10^7` and `10^-6` at both signs. This limited-tier value is retained and is not retuned.

## 6. Tier (ii): exact first-order coefficient and self-consistent remainder (items 5 and 11)

**6.1 First-order coefficient.** `c^{(1)}:=L_0`, whose components are `c^{(1)}_M = H_M^{-1}P_M V Omega_0 = H_0^{-1}P_perp V Omega_0` restricted to sector `M`. For every omitted face `f`:
- (a) `<Omega_0, W_f Omega_0> = E_Haar[W] = 0`, because the face holonomy of four independent Haar links is Haar.
- (b) `W_f Omega_0` puts spin 1/2 on exactly the four distinct links of `f` and is constant elsewhere. It therefore lies in the sector `M_f = supp_B(f)`, the factors owning links of `f`. Every omitted face has `|M_f|>=2`.
- (c) Each of the four links carries the Casimir `3/4`, so `H_0 W_f Omega_0 = 8·4·(3/4) W_f Omega_0 = 24 W_f Omega_0`. This is `3` in `alpha` units.
- (d) `||W_f Omega_0||^2 = E[W^2] = 1/4`. By Weyl integration, `E[W^n] = 1, 0, 1/4, 0, 1/8` for `n=0..4`.
- (e) Distinct faces share at most one link. The checker verifies this over all 82 faces meeting `R`. Integrating over a link of `f` that is not in `g` gives `<W_f Omega_0, W_g Omega_0> = 0`.

Hence

\[
 c^{(1)}_M=-\frac{\tau}{72}\sum_{f:\,M_f=M}W_f\Omega_0,\qquad
 \|c^{(1)}_M\|=\frac{|\tau|\sqrt{n_M}}{144},
 \tag{HNM-AV1-F15}
\]

where `n_M` is the number of faces with owner set `M`. In `alpha` units, `V_b=phi_b/8=-(tau/24) sum W_f` and the energy is `3`, which gives the same `-tau/72`. Mixing the units would give `tau/576` or `tau/9`; both are rejected controls.

**6.2 Enumeration by translation covariance.** Omitted faces are pairs `(b,k)`, where `b` is the anchor and `k` is one of the 21 I1 classes, with relative support `K_k subset S` and owner set `b+K_k`. A face `(b,k)` contains the factor `u` if and only if `b=u-d` with `d in K_k`. Therefore

\[
 \#\{f:\ u\in M_f\}=\sum_{d\in S}\#\{k:\ d\in K_k\}=21+4+8+16=49 .
 \tag{HNM-AV1-F16}
\]

The class counts per offset come from the I1 table:
- `0` lies in all 21 classes.
- `e_x` lies in 4: xy with `r=3`, `s=0` and with `r=3`, `s=1`, plus the two xz classes with `r=3`.
- `e_y` lies in 8: xy with `s=1` and `r<=2`, xy with `r=3`, `s=1`, and the four yz classes with `s=1`.
- `e_z` lies in 16: every xz and yz class.

An owner set determines its anchor, which is its lexicographic minimum, and its class shape. The 15 owner sets containing `u=0` and their multiplicities are:

| shape | owner sets containing 0 | `n_M` each |
|---|---|---:|
| `{0,e_x}` | `{0,e_x}`, `{-e_x,0}` | 1 |
| `{0,e_y}` | `{0,e_y}`, `{-e_y,0}` | 3 |
| `{0,e_z}` | `{0,e_z}`, `{-e_z,0}` | 10 |
| `{0,e_x,e_y}` | three translates | 1 |
| `{0,e_x,e_z}` | three translates | 2 |
| `{0,e_y,e_z}` | three translates | 4 |

Other counts follow:
- **Faces meeting `R`:** `49+49-16=82`. The 16 faces containing both `0` and `e_z` are the classes containing `e_z`, anchored at `0`.
- **Faces inside `R`:** 10 (the xz classes with `r<=2` and the yz classes with `s=0`, anchored at `0`). The original Wilson face `W` is one of them.
- **Owner sets meeting `R`:** `15+15-3=27`, of which 26 straddle. Among the faces meeting `R`, 72 have straddling owner sets.
- **Boundary:** in a finite box only whole stars are retained, so every per-site count and every `n_M` is at most its bulk value. The checker verifies this for all sites of `N=1,2,3`.
- **Independent confirmation:** a brute-force fine-lattice enumeration, done without the class table, reproduces 49, the 15 multiplicities and 82.
- **Bounds:** `84=4·21` is used only as a labelled bound, and 168 bounds the faces meeting `R`.

The counts `(49, 15, 82, 10)` are derived and then compared with the contract candidates. A count function that ignores the table is rejected by a sensitivity test.

**6.3 Anchored norm, remainder, self-consistency.** From (F15) and (F16),

\[
 \|c^{(1)}\|_a=\frac{|\tau|}{144}\max_u\sum_{M\ni u}\sqrt{n_M}
 \le\frac{|\tau|}{144}\bigl(11+2\sqrt3+3\sqrt2+2\sqrt{10}\bigr)\le\frac{49|\tau|}{144}=:t_1 .
 \tag{HNM-AV1-F17}
\]

The grouped square-root sum is at most `25031297627/10^9`, a directed rational upper bound (about `0.173828|tau|` in total). `G` is convex and increasing and `t<=R`, so (F05) gives

\[
 \|c-c^{(1)}\|_a\le J\bigl(G(t)-16\bigr)\le J\,t\,G'(R)\le352\,J\,t ,\qquad
 t\le t_1+352Jt\ \Longrightarrow\ t\le\frac{t_1}{1-352J}.
 \tag{HNM-AV1-F18}
\]

The inequality `352J<1` holds with a large margin. The remainder budget is charged at its positive majorant value and is never set to zero. A sharper directed form uses `G(t)-16 <= 288t/(1-8t) <= 288t/(1-8t_i)`. Every component carries the tier label (ii). Combining `c^(1)` with the crude `t`, or using `t=t_1` without (F18), is rejected by the `tier_mixing_rejected` control.

**6.4 Values at `tau=±10^-8`** (both signs are identical; `c^(1)` is odd in `tau`, its norm even):

\[
\begin{aligned}
 t_1&=\tfrac{49}{14400000000},\quad t_{ii}=\tfrac{49}{14398580736},\quad
 \|c-c^{(1)}\|_a\le\tfrac{3773}{11248891200000000},\quad
 \varepsilon_{ii}=\tfrac{1411060914529}{207319127211110301696},\\
 D_{ii}&=\tfrac{585079838465912592144137406066050}{42981220507576537932303142777593983768257}\approx1.36124528702\times10^{-8}.
\end{aligned}
 \tag{HNM-AV1-F19}
\]

Three variants of tier (ii) are also evaluated:
- the grouped form: `D ≈ 6.95382362879×10^-9`;
- the sharper remainder: `D ≈ 1.36122089674×10^-8`;
- the labelled 84-bound: `D ≈ 2.33356336336×10^-8`.

All three are below `4/10^7`.

## 7. Cutoff-vector removal (item 6)

AM2 §6 removed the onsite cutoff for eigenvalues only. Fix `N`. For the admitted premises, AM2 §6 gives: `H=H_0+V` is self-adjoint on `D(H_0)`, bounded below and has compact resolvent; `E_0` is simple; and `E_1-E_0>=1/2` for the **untruncated** operator. Let `Q_L=⊗_{x in Lambda_N} 1_[0,L](h_x)`. It has finite rank, commutes with `H_0` and tends strongly to `1`. Let `psi_L` be the normalized ground vector of `Q_L H Q_L` on `Ran Q_L`. By AM2 in the cutoff space, `psi_L ∝ e^{-C_L}Omega_0`, and the rank-independent constants give the same tier bounds.

For `L>=24` each vector `W_f Omega_0` lies in the product of eigenspaces of energy `6k_x<=24`, so `Q_L W_f Omega_0 = W_f Omega_0` and `c_L^(1)=c^(1)` exactly. For smaller `L` each face vector is kept or annihilated, so the counts only decrease. Hence

\[
 \|\rho_{L,R}-P_R\|_1\le D\qquad\text{for every }L .
 \tag{HNM-AV1-F20}
\]

*Energies.* `E_{0,L}=<psi_L,H psi_L> >= E_0`, because `Ran Q_L subset D(H_0)`. For the upper limit: `Q_L` is a joint spectral projection of the commuting `h_x`, so `<Q_L psi, H_0 Q_L psi> = <psi, Q_L H_0 psi>` increases to `<psi,H_0 psi>` by monotone convergence. `V` is bounded in the fixed box, and `||Q_L psi|| -> 1`. Therefore

\[
 E_0\le E_{0,L}\le\frac{\langle Q_L\psi,HQ_L\psi\rangle}{\|Q_L\psi\|^2}\longrightarrow E_0 .
 \tag{HNM-AV1-F21}
\]

*Eckart-type vector bound.* Write `psi_L = a psi + phi` with `phi ⊥ psi`. Then `E_{0,L}-E_0 = <phi,(H-E_0)phi> >= (E_1-E_0)(1-|a|^2)`, so

\[
 1-|\langle\psi,\psi_L\rangle|^2\le\frac{E_{0,L}-E_0}{E_1-E_0}\le2(E_{0,L}-E_0)\longrightarrow0 .
 \tag{HNM-AV1-F22}
\]

This is stronger by a factor of two than the contract's admissible `2(E_{0,L}-E_0)/gap` form. The pure-state trace distance equals `2 sqrt(1-|<psi,psi_L>|^2)`, and partial trace is trace-norm contractive, so `rho_{L,R} -> rho_{N,R}` in trace norm. The closed trace-norm ball then gives

\[
 \|\rho_{N,R}-P_R\|_1\le D\quad\text{for the untruncated finite-volume ground state.}
 \tag{HNM-AV1-F23}
\]

The gap is essential. For `H'=diag(0,0,1)`, a cutoff "ground" vector `e_2` has the exact ground energy yet is orthogonal to `e_1`, so eigenvalue convergence alone proves nothing about vectors. The checker verifies (F22) exactly on a rational `3×3` fixture with gap `1/2`. Its Eckart pairs are `(8/9, 20/9)`, `(4/9, 32/45)` and `(0,0)`.

## 8. Passage to the AQ subsequential states (item 7)

AQ1 gives a subsequence `N_k` of centered boxes along which `rho_{N_k,F} -> rho_F` in trace norm for every finite complete-factor region `F`, in particular for `F=R`. By (F23), for every `k`,

\[
 \|\rho_R-P_R\|_1\le\|\rho_R-\rho_{N_k,R}\|_1+D\ \longrightarrow\ D .
 \tag{HNM-AV1-F24}
\]

**Quantifier.** The bound holds for every sequence of centered boxes `N_k>=2` along which the local density on `R` converges in trace norm. It therefore holds for AQ1's chosen state and for every state that AQ1's diagonal-extraction construction can produce, at either sign. It does not assert:
- uniqueness: two such limits may differ by up to `2D` on `R`, and the checker exhibits two distinct limits within the same bound;
- whole-sequence convergence;
- any rate in `N`.

Only local trace-norm convergence is used.

## 9. Consequences and scaling (item 8)

Trace duality with `||W||<=1`, and the effect refinement for the trace-zero difference with `0<=W^2<=I`, give

\[
 |\omega_\tau(W)|\le D,\qquad |\omega_\tau(W^2)-\tfrac14|\le \tfrac D2,\qquad m^2=\omega_\tau(W)^2\le D^2 .
 \tag{HNM-AV1-F25}
\]

The reference values `omega_0(W)=0` and `omega_0(W^2)=1/4` are read from the contract and re-derived by Weyl integration. The resulting bounds are:
- tier (ii): `|omega(W)| <= 1.3612×10^-8` and `|omega(W^2)-1/4| <= 6.806×10^-9`;
- tier (i): `2.368×10^-5` and `1.184×10^-5`.

The exact intervals for both signs are in `results.json`. No value or sign of `omega(W)` is claimed. The candidate first-order mean `|tau|/144 ≈ 6.94×10^-11` is consistent with the bound but is neither implied nor claimed; it belongs to AW1.

**Scaling.** The exact ratios `D(10^-8)/D(10^-10)` are `≈100.0014651` for tier (i) and `≈100.0097592` for tier (ii). Both lie in `[99,101]`, so the bounds are linear in `tau`. The AT4 bound `2 sqrt(49|tau|/3)` has a ratio of exactly `10`, which lies in `[9.9,10.1]`. Relabelling the square-root bound as linear is rejected. `D` is increasing in `|tau|` (compositions of increasing functions), so the cap values bound every `|tau|<=10^-8`.

## 10. Targets, error ledger and AV2 feasibility arithmetic (item 9)

| quantity | `tau=+10^-8` | `tau=-10^-8` | `<=4/10^7` | `<=10^-6` |
|---|---|---|---|---|
| `D_i` (tier i) | `2.36803504623e-5` | same | no | no |
| `D_i` iterated (tier i) | `1.79221103916e-5` | same | no | no |
| `D_ii` (tier ii, `t_1=49|tau|/144`) | `1.36124528702e-8` | same | **yes** | yes |
| `D_ii` grouped (tier ii) | `6.95382362879e-9` | same | yes | yes |
| AT4 `2sqrt(49|tau|/3)` | `8.08290376865e-4` | same | no | no |

The target `1/2500000` and the secondary `10^-6` are read from the contract (`preregistration.target` and item 9). The flag `tier_ii_target_met` is `true`.

**Itemized error terms** (preregistered list; decimals are previews at `+10^-8`):
- `am2_remainder`: `||c-c^(1)||_a <= 3773/11248891200000000 ≈ 3.35×10^-13` (tier ii). Not applicable to tier (i), which bounds the whole `c` directly.
- `two_creation`: `t^2 = 2401/207319127211110301696 ≈ 1.16×10^-17` (tier ii) and `1369/39062500000000` (tier i). Both are inside `eps`.
- `straddling`: counted inside the `2t` term. All supports meeting `R` are included; at first order the straddling faces contribute at most `72|tau|/144 = |tau|/2` to the `R`-sum.
- `density`: the `sigma` and `d^2P_R` part of `D`, `2eps^2/(1+eps^2) ≈ 9.3×10^-17` (tier ii).
- `onsite_cutoff_vector`: not a numeric cost. It is an exact limit in each fixed box, (F20)–(F23).
- `arithmetic`: not a numeric cost. All bounds are exact rationals. The only enclosures are directed upward: `exp(1/8)<8/7`, `e^{8t}<=1/(1-8t)`, and integer-square-root upper brackets.

**AV2 feasibility (arithmetic of the contract statement only).** Let `F(D)=2(D+D^2)+49·10^-8/pi`, with a Machin `pi` bracket rounded outward to `10^-30`. Then:
- `F(D_ii) <= 1.832×10^-7`;
- `F(4/10^7) <= 9.5597×10^-7 <= 10^-6`;
- `F(4.22×10^-7) <= 10^-6`, while `F(4.23×10^-7) > 10^-6`.

The AV2 window lemma itself is not proved here.

## 11. Executed controls (item 9; 43 checks, all contract ids)

Every control is a damaging mutation that must raise an explicit exception. The checks never use `assert` and remain active under `-O`.

- **`missing_incoming_stars`:** the seven anchors `R-S` are derived; the orthant count 2 and a one-star `J=7|tau|` are rejected.
- **`full_original_wilson_cover`:** 48 links, 36 endpoints (22 per factor, 8 shared) and owners `0,0,0,e_z` for `W`'s links; the four drawn links are rejected as a cover.
- **`wrong_delta_alpha_hbar_clock`:** the coefficient `-tau/72` is obtained in both unit systems; the mixed `tau/576` and `tau/9` and the eightfold clock exponent are rejected, using a non-unit fixture with `alpha=5`, `hbar=7`.
- **`vector_versus_scalar_centering`:** the residues `1/10000`, `-51/10000` and `1/16` are computed; scalar subtraction used as vector centering is rejected.
- **`first_order_mean_charged`:** `m^2<=D^2` is charged at every tier and sign; a zero-mean assumption is rejected.
- **`tau_scaling_exponent`:** the exact ratios are computed; a square-root bound relabelled linear is rejected.
- **`changed_model_relabelled`:** a coupling of `10^-14`, a nonzero triple, a selected-strip reference, a finite-graph model id and a finite-volume provenance are each rejected.
- **`coherent_evidence_tampering`:** flipping a control Boolean, removing a snapshot, halving `D_ii` or flipping the tier-(i) Boolean is rejected even after the packet hash is rebound.
- **`insufficient_verdict_retained`:** tier (i) and AT4 are retained as failing, and retuning `tau` is rejected.
- **`exact_arithmetic_admission`:** float, bool, `NaN` and zero-denominator inputs are rejected; there are no numerical-library imports.
- **`root_n_misuse`:** coherent addition gives `||delta||^2=13/100 > 9/100`, the root sum of squares; RSS, division by `sqrt(N)` and division by 64 are rejected.
- **`no_priority_or_continuum_claim`:** all claim flags are false.
- **`deleted_normalization`, `outside_creations_do_not_cancel_naively`, `omitted_adjoint_terms`, `straddling_supports_counted`:** the three-site fixtures of Section 4. Dropping `||delta||^2` from `Z`, numerator-only localization, dropping outside creations everywhere, dropping `|Omega_R><xi|`, dropping both cross terms, dropping `sigma`, and `eps` without straddling supports are each rejected.
- **`anchored_norm_restricted_to_cover`:** the fixture `R`-sum `2/5` lies in `(t, 2t]`; the one-site bound and extensive volume sums are rejected. On the actual data, the first-order `R`-sum `82/144` lies in `(49/144, 98/144]`.
- **`am2_fixed_point_constants`:** (F04) is verified exactly; a `G(R)` with the exponential dropped and a zero remainder are rejected.
- **`first_order_face_enumeration`:** energy 24, norm `1/2`, at most one shared link, `49<=84` and `82<=168` are verified.
- **`cutoff_vector_removal`:** the Eckart fixture is checked; citing AM2 §6 alone, or using a degenerate eigenvalue-only argument, is rejected.
- **`aq_passage_trace_norm_only`:** two distinct limits within the bound are exhibited; uniqueness and a rate claim are rejected.
- **`tier_mixing_rejected`:** see Section 6.
- **`face_count_all_sites`:** a hard-coded or copied count, anchors restricted to `R` (21 and 42) and a boundary count above the bulk are all rejected.
- **`reverse_premise_isolation`:** the forward inventory equals AGENTS plus the contract, the shared premises and the forward-additional premises. The derived reverse list contains no triage, deliberation, loop-2 or forward-AV file, and adding one is rejected.
- **`av2_feasibility_threshold`:** see Section 10.

## 12. Scope, exclusions, incomplete steps and reproduction

**Claim flags:** `continuum_claim:false`, `uniform_wilson_claim:false`, `resolved_interaction_shift:false`, `scientific_priority_verified:false`, `euclidean_node_certified:false`, `first_order_parity_claim:false`. The following are also false: `uniqueness_claimed`, `whole_sequence_convergence_claimed` and `rate_in_N_claimed`.

**Exclusions**, copied from the contract:
- the cap-level Euclidean certificate (AV2);
- the interaction-induced shift or its sign (AW);
- uniform Wilson magnetic theory (AX);
- AQ uniqueness, whole-sequence convergence or a rate in `N` (AY);
- continuum construction (AZ);
- Yarotsky/HTW constant evaluation;
- scientific priority;
- the value or sign of `omega(W)` beyond `|omega(W)|<=D`;
- the first-order coefficient `1/144`;
- any vanishing of the first-order `C(s)` or `omega(W^2)` (AW1).

The model is exactly the contract's `AQ_patterned_zero_selected` family with a Haar reference. Nothing here transfers to nonzero selected triples, where `P_R` is not Haar (AT4 F01).

**Not done, or limits of this producer's evidence:**
1. The reverse vacuum-overlap/fidelity route (item 3's inequality) was not executed. It is assigned to the reverse producer. Only the parts that item 3 requires of each producer, the trap and the three-site counterexample, are derived here. The contract's `accepted_within_scope` needs both routes and review.
2. The cutoff step relies on the admitted AM2 §6 facts: self-adjointness, compact resolvent and the untruncated gap `1/2`. The vector convergence, (F20)–(F23), is new here.
3. The anchored bound on `c-c^(1)` uses AM2's generic majorant (`h>=Q`, `16` output sets), not the reference gap 6. It is conservative. A sharper remainder was not attempted.
4. The first-order `R`-sum refinement (`82/144` instead of `2·49/144`) is recorded but not used in `eps`.
5. Fixtures are exact audits of algebra and of the necessity of hypotheses. They are not proofs of the infinite-dimensional statements, which rest on the arguments above.
6. The bounds are upper certificates. Nothing here lower-bounds the actual distance `||rho_R-P_R||_1`.

**Methodological lenses.** Newton's analysis before synthesis is followed: the reduced density is analyzed into its vacuum, cross and excited blocks before any bound is synthesized. Tesla's complete accounting is also followed: the source is the creations meeting `R`, straddling ones included; the load is the complete 48-link cover; and every channel is charged (cross terms, `sigma`, normalization). These are modern methodological uses of the snapshotted skills. They carry no historical endorsement, and no historical or occult material supplies a premise.

**Reproduce** (fresh absolute output directories outside the checkout):

```bash
python3 -B research/round32/forward/av1/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/forward/av1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/forward/av1
```

`check.py` verifies the contract snapshot hash and reads the target, reference and candidate values from the contract. It records its own sha256 before evaluation. It writes `results.json` (43 checks) and `source-manifest.json`, which binds the report, the checker and all 26 input snapshots. `freeze.json` binds the whole producer closure.
