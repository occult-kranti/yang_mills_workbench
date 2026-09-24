# Hruday first-order local state lemma — AV1 reverse (vacuum overlap / fidelity route)

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted reverse production under premise isolation. I read the frozen contract `inputs/research/round32/contracts/av1.json` first, then only the byte-identical snapshots in `inputs/` and the four inherited files named at the end. I read no Round32 forward, skeptic, expert or deliberation file.

The product-ordering idea and the location of the normalization trap are shared panel premises declared in contract item 3. Independence is claimed only for the inequality, the constants, the enumeration, the cutoff step and the passage step. HNM labels are project aliases.

Attribution: commuting creation-operator expansions are established mathematics. They are credited to Bravyi–DiVincenzo–Loss 2008 in the AM2 lineage, and the AM2 snapshots read here cite Gauvin arXiv:2503.15539v3 Supplement A.6–A.8 and Yarotsky. The pure-state trace-distance and fidelity inequalities are standard. Scientific priority is unverified.

**Verdict.** The setting is the zero-selected AQ subfamily, either sign of `|tau|<=10^-8` and every centered whole-star box `Lambda_N` with `N>=2`. On the complete cover `R={0,e_z}` of the original xz Wilson loop, the reverse route proves

\[
\|\rho_{N,R}-P_R\|_1\le \frac{2\varepsilon}{\sqrt{1+\varepsilon^2}},
\]

where `eps` is built only from the AM2 anchored creation norm. The bound is uniform in N. It survives removal of the on-site spectral cutoffs for the ground vector itself, not only for its eigenvalue. It passes to every subsequential AQ1 limit by local trace-norm convergence.

- **Tier (ii), exact first order:** `D_ii <= 113902305553947264976096174312887/10^40 ~ 1.1390231e-8` at `tau=+10^-8`, and the same value at `-10^-8`. This is below the frozen target `4/10^7` by a factor of about 35.1 and below the secondary `10^-6`.
- **Tier (i), crude:** `D_i ~ 2.3680070e-5`, or `1.7921485e-5` iterated. It meets neither target.

The proposed outcome of this producer is **accepted_within_scope**, with sub-label `uniform_local_closeness_not_uniqueness`. Admission still needs the forward route, the exchange and the skeptical review. Nothing here asserts:

- AQ uniqueness;
- whole-sequence convergence;
- a rate in N;
- a value or sign of `omega(W)` beyond `|omega(W)|<=D`.

## 1. Model, units and constants

The frozen model is `AQ_patterned_zero_selected`:

- SU(2) Kogut–Susskind form on Z³ at fixed spacing;
- coarse 24-link factors b, each owning the links whose tails lie in `{(4b_x+r, 2b_y+s, b_z)}`;
- selected triple exactly `(0,0,0)`;
- 21 omitted anchored faces per factor with coefficient `alpha*tau/24`;
- both signs of `|tau|<=10^-8`;
- fixed positive alpha, hbar, E_star and spacing.

In normalized units `delta=alpha/8`:

\[
H_N=\sum_{b\in\Lambda_N}h_b+\sum_{b+S\subseteq\Lambda_N}\phi_b,\quad
h_b=8\sum_{e\ \mathrm{owned\ by}\ b}C_e,\quad
\phi_b=-\frac{\tau}{3}\sum_{f\in O_b}W_f,\quad S=\{0,e_x,e_y,e_z\}.
\tag{HNM-AV1-R01}
\]

At the zero triple, the onsite ground is the constant Haar vector `Omega_b`, its ground scalar is zero, and `h_b>=6(1-P_b)>=1-P_b`. A nonzero selected plaquette `lambda` has Haar-plus-Wilson trial energy `-lambda^2/(12 alpha)<0`. Using the Haar reference there would therefore be a changed model, and the checker rejects that relabelling.

Each star norm obeys `||phi_b||<=21*(1/3)|tau|=7|tau|`, and a site lies in `|S|=4` stars, so

\[
J:=\max_u\sum_{X\ni u}\|V_X\|\le 28|\tau|,\qquad J_0=28\cdot10^{-8}=\tfrac{7}{25000000}.
\tag{HNM-AV1-R02}
\]

The AM2 majorant is `G(t)=sum_k L_k t^k/k! = 16 e^{8t}(1+10t)`, with `L_k=16*8^k(1+5k/4)` and `G'(t)=16e^{8t}(18+80t)`. The checker verifies the Taylor coefficients for k=0..8. It encloses `e^{1/8}` to within 10^-40, below 8/7, using a partial sum plus a geometric tail. With `R=1/64`:

\[
G(R)<\tfrac{148}{7},\quad G'(R)<352,\quad J_0G(R)=\tfrac{148}{25000000}<R,\quad 352J_0=\tfrac{77}{781250},\quad 2J_0G'(R)<1 .
\tag{HNM-AV1-R03}
\]

The contract's AM2 constants are re-derived and compared, not copied. A certified lower enclosure `G'(R)>349` rejects 288 (the value `G'(0)`) as an upper constant.

Physical scales cancel. A face vector has energy `24 delta = 3 alpha`. The per-face coefficient is `(tau/3)/24 = (tau/24)/3`, times the face norm 1/2, giving `|tau|/144` in either unit system. Mixing the two unit systems gives `|tau|/1152` or `|tau|/18`, an eightfold clock error, and is rejected. hbar and E_star do not enter a ground-state bound.

## 2. The AM2 objects; AQ1's boxes are AM2's family (item 1)

**Cutoffs and creators.** Impose finite-rank on-site spectral projections `Q_{x,n}` of `h_x` containing `Omega_x`. For `c_I` in `tensor_{x in I} Q_x H_x`, the creator is `hat c_I=|c_I><Omega_I| tensor 1`.

- Any two creators commute.
- Creators with overlapping supports multiply to zero, because the vacuum bra at a shared site annihilates the excited ket. In particular `hat c_I^2=0`.

**The fixed point.** With the anchored norm `||c||_a=max_u sum_{I contains u}||c_I||`, AM2 (admitted) proves the following. The unique fixed point

\[
c=\sum_{k=0}^{8}\frac{L_k(c,\ldots,c)}{k!},\qquad
L_k(c_1,\ldots,c_k)_M=H_M^{-1}P_M\,\mathrm{ad}_{C_1}\cdots\mathrm{ad}_{C_k}(V)\,\Omega_0,\qquad \|c\|_a\le R=\tfrac1{64},
\tag{HNM-AV1-R04}
\]

gives the ground vector `psi=e^{-C}Omega_0=prod_I(1-hat c_I)Omega_0`. This vector has vacuum coefficient one. The ground is simple, with full-space gap at least 1/2, uniformly in the cutoff and in the finite complete-factor volume. The multilinear bound is `||L_k(c_1..c_k)||_a <= J L_k prod ||c_j||_a`.

**AQ1's boxes are AM2 volumes.** AQ1's box is `Lambda_N=[-N,N]^3` with Hamiltonian `sum_{b in Lambda_N} h_b + sum_{b+S subset Lambda_N} phi_b`. This is (HNM-AM2.1) for the finite complete-factor set `Lambda=Lambda_N`: the retained interactions are the whole stars inside `Lambda_N`, and the onsite operator is the same selected-reference operator, here at the zero triple.

A coarse translation by `(N,N,N)`, which is `(4N,2N,N)` on the fine lattice, maps `Lambda_N` onto an orthant box. It preserves ownership, the I1 class table and every norm. AM2's volume-uniform statement therefore applies to each `Lambda_N`.

The checker enumerates `Lambda_2` and `Lambda_3`:

- every site lies in at most four retained stars;
- all seven incident anchors `R-S` are retained for `N>=2`, but only four are retained for `N=1`.

No Yarotsky, HTW or Gauvin constant is used.

## 3. Reverse route: from the desired inequality to a vacuum overlap

**Desired.** A bound on `||rho_{N,R}-P_R||_1` that is linear in tau and uniform in N. Here `rho_{N,R}=Tr_out|psi><psi|/||psi||^2` and `P_R=|Omega_R><Omega_R|`.

### Analysis, working backwards

(a) For any density `rho` and unit vector `Omega`, the pure-state-mixture inequality admitted in AT4 (HNM-AT4-F08; standard) gives

\[
\bigl\|\rho-|\Omega\rangle\langle\Omega|\bigr\|_1\le 2\sqrt{1-\langle\Omega,\rho\,\Omega\rangle}.
\tag{HNM-AV1-R05}
\]

Proof. Write `rho=sum_i p_i|u_i><u_i|`. For unit vectors the difference `|u><u|-|Omega><Omega|` has rank two with eigenvalues `+-sqrt(1-|<Omega,u>|^2)`. Its trace norm is therefore `2sqrt(1-|<Omega,u>|^2)`. Convexity of the trace norm and concavity of the square root finish the proof. So it suffices to bound the single number `1-Tr(rho_{N,R}P_R)`.

(b) `Tr(rho_{N,R}P_R)=||(P_R tensor 1)psi||^2/||psi||^2`. What is needed is an exact expression for `(P_R tensor 1)psi`, together with an orthogonal remainder controlled relative to that expression rather than relative to 1.

(c) The shared premise supplies this. Split `C=C_R+C_out`: `C_R` collects the creators whose support meets R, and `C_out` collects all others. The creators commute, so the R-meeting factors can act last:

\[
\psi=e^{-C_R}\psi_{\rm out},\qquad \psi_{\rm out}:=e^{-C_{\rm out}}\Omega_0=\Omega_R\otimes\varphi_{\rm out},\qquad \varphi_{\rm out}=e^{-C_{\rm out}}\Omega_{\rm out},\qquad \langle\Omega_0,\psi_{\rm out}\rangle=1 .
\tag{HNM-AV1-R06}
\]

### Synthesis, working forwards

**Pigeonhole.** Among three creators that each meet the two-site set R, two share a site of R. Hence

\[
C_R^3=0,\qquad \delta:=\psi-\psi_{\rm out}=-C_R\psi_{\rm out}+\tfrac12C_R^2\psi_{\rm out}.
\tag{HNM-AV1-R07}
\]

The quadratic term is the sum of `hat c_I hat c_J` over unordered pairs with `I contains 0`, `J contains e_z` and `I cap J` empty. This forces `e_z notin I` and `0 notin J`.

**The split is orthogonal.** Every term of `delta` contains a factor `c_I` with some `x` in `I cap R`. Because `c_I` is excited at `x`, `(P_x tensor 1)c_I=0`. Hence

\[
(P_R\otimes1)\psi=\psi_{\rm out},\qquad \langle\psi_{\rm out},\delta\rangle=0,\qquad \|\psi\|^2=\|\psi_{\rm out}\|^2+\|\delta\|^2,
\tag{HNM-AV1-R08}
\]

\[
\operatorname{Tr}(\rho_{N,R}P_R)=\frac{\|\psi_{\rm out}\|^2}{\|\psi_{\rm out}\|^2+\|\delta\|^2}=\frac1{1+e^2},\qquad e:=\frac{\|\delta\|}{\|\psi_{\rm out}\|}.
\tag{HNM-AV1-R09}
\]

**Size of δ relative to ψ_out.** For I meeting R,

`hat c_I psi_out = c_I tensor Omega_{R\I} tensor (<Omega_{I\R}| tensor 1)phi_out`.

The partial vacuum bra is a contraction, so `||hat c_I psi_out|| <= ||c_I|| ||phi_out||`. Likewise `||hat c_I hat c_J psi_out|| <= ||c_I|| ||c_J|| ||phi_out||`, and `||psi_out||=||phi_out||`. Therefore

\[
e\le\varepsilon:=\sum_{I\cap R\ne\varnothing}\|c_I\|+\sum_{I\ni0,\ J\ni e_z,\ I\cap J=\varnothing}\|c_I\|\,\|c_J\|\ \le\ 2t+t^2,\qquad t=\|c\|_a .
\tag{HNM-AV1-R10}
\]

Since `1-1/(1+e^2)=e^2/(1+e^2)` increases with e, combining (R05) with (R09) gives

\[
\|\rho_{N,R}-P_R\|_1\le\frac{2e}{\sqrt{1+e^2}}\le D(\varepsilon):=\frac{2\varepsilon}{\sqrt{1+\varepsilon^2}} .
\tag{HNM-AV1-R11}
\]

**Uniformity in N.** `eps` involves only anchored sums at the two sites of R. The AM2 fixed point bounds these independently of N and of the cutoff.

**Comparison with the contract's direct form.** `D(eps) <= 2eps(1+eps)/(1+eps^2)`, the direct-density form named in contract item 2, because `(1+eps)^2>=1+eps^2`. The forward work was neither read nor evaluated.

Every step is an exact identity except two. (R10) uses only the triangle inequality and the contraction property; (R05) is the standard mixture inequality.

## 4. The normalization trap and a three-site model-class counterexample

### The trap

`psi` is unnormalized, and `||psi||^2` grows exponentially with the number of sites, because every outside creator contributes. In

`Tr(rho_{N,R}P_R) = <psi,(P_R tensor 1)psi>/<psi,psi>`

the outside creators appear in both places:

- in the numerator, as `||phi_out||^2`;
- in the denominator, as `||phi_out||^2+||delta||^2`.

`delta` itself depends on them. A straddling creator, whose support meets both R and the outside, contracts its outside legs against `phi_out`. Two shortcuts therefore fail.

- **Deleting the normalization.**
  - Reading `<psi,(P_R tensor 1)psi>=||phi_out||^2` as an overlap gives a number above one that grows with volume.
  - Normalizing by the vacuum coefficient instead gives the global vacuum overlap `1/||psi||^2`, which decays with volume (the orthogonality catastrophe), not the local overlap.
- **Cancelling the outside naively.** This means dropping the creators that do not meet R and computing the R-marginal of `e^{-C_R}Omega_0` as if `phi_out` were a spectator. It is wrong, because the straddling contractions `<Omega_{I\R}|phi_out>` carry the outside creators into the R-marginal.

The only legitimate cancellation is inside the ratio `e=||delta||/||psi_out||`. It holds after each straddling contraction is bounded by `||phi_out||`, the same factor that normalizes `psi_out`.

### Counterexample (fixture A)

This is my own construction.

**Setup.**

- Three qubit sites 0, z and o, with `R={0,z}` and o outside.
- Vacuum `|0>` and excited `|1>` on each site. This is the AM2 creation algebra with one-dimensional excited spaces.
- Three creators: `a_{0}=1/2`, `a_{0o}=1/2` (straddling) and `a_{o}=-1` (outside).

**Actual ground vector.** With sites ordered 0, z, o:

- `psi=|000>+|001>-(1/2)|100>-|101>`, with `||psi||^2=13/4`;
- `psi_out=|00>_R tensor(|0>+|1>)_o`, with `||psi_out||^2=2`;
- `delta=-(1/2)|100>-|101>`.

This gives `e^2=5/8` and `Tr(rho_R P_R)=8/13=1/(1+5/8)`. In the basis `{|00>,|10>}`, `rho_R=[[8/13,-6/13],[-6/13,5/13]]`. Its trace distance to `P_R` is `2sqrt(61)/13 ~ 1.2016`, below `2sqrt(5/13) ~ 1.2403`.

**Naive restriction** (drop `a_o`). This gives `e^2=1/2`, overlap 2/3, `rho_R=[[2/3,-1/3],[-1/3,1/3]]` and trace distance `2sqrt(2)/3 ~ 0.9428`.

**What this shows.**

- The outside creator *increases* the R-excitation (5/8 > 1/2) and the trace distance. Naive restriction is therefore neither exact nor a bound.
- The fidelity bound (R11) still holds, with `eps=a_0+a_{0o}=1`.
- The deleted-normalization "overlap" is 2, and vacuum-coefficient normalization gives 4/13.

**Adding decoupled outside sites.** With k outside sites, each carrying `a_o=-1`:

- the unnormalized quantity is `2^k`;
- the global vacuum overlap is `(4/13)2^{1-k}`;
- the local overlap stays exactly 8/13 for k=1..4 (exact, in the checker).

### Adjoint and straddling fixtures

**Fixture B** uses all seven supports of `{0,z,o}`, with amplitudes 1/2, 1/3, −1, 1/5, 1/2, −1/4 and 1/7. It verifies (R06)–(R11) exactly, including `C_R^3=0` on every basis vector, and the explicit decomposition

\[
\operatorname{Tr}_{\rm out}|\psi\rangle\langle\psi|=\|\varphi_{\rm out}\|^2P_R+|\xi\rangle\langle\Omega_R|+|\Omega_R\rangle\langle\xi|+\operatorname{Tr}_{\rm out}|\delta\rangle\langle\delta|,\qquad \xi:=(1_R\otimes\langle\varphi_{\rm out}|)\delta,\quad \langle\Omega_R,\xi\rangle=0 .
\tag{HNM-AV1-R12}
\]

The fixture also carries an exact eigenvalue certificate. `rho_R-P_R` has exactly one negative eigenvalue, bracketed by Descartes sign counts on the exact characteristic polynomial, and its trace norm is at most `2sqrt(1-F)`.

- Dropping the adjoint term gives a non-Hermitian matrix, which is rejected.
- Dropping both cross terms, or the excited block, changes the matrix, which is rejected.
- The cross terms are first order in e and carry the trace distance; the excited block is second order.

**Fixture C** has only straddling creators: `a_{0o}=1/2`, `a_{zo}=1/3`, `a_o=1` and `a_{0zo}=1/5`. A budget restricted to supports inside R is zero, while `e^2=361/1800`, so straddling supports must be counted.

These fixtures audit the algebra. They are not rotor truncations and prove nothing about infinite volume.

## 5. Tier (i): crude anchored norm

The fixed point gives `t<=J G(t)<=J G(R)`. In tier (i) every term uses only this t:

\[
t\le 28|\tau|\cdot\tfrac{148}{7}=592|\tau|,\qquad \varepsilon_i=2t+t^2,\qquad D_i=D(\varepsilon_i).
\tag{HNM-AV1-R13}
\]

At `tau=+-10^-8`:

- `t<=148/25000000=5.92e-6`;
- `eps_i ~ 1.1840035e-5`;
- `D_i <= 236800700911401877571290493559933441/10^40 ~ 2.3680070e-5`.

**Optional iteration.** Iterate `t_{k+1}=J G^+(t_k)` with a directed exponential enclosure. This is valid because G is increasing, so `t<=t_k` implies `t<=J G(t_k)`. Four iterations give `t<=4.4803613e-6` and `D<=1.7921485e-5`.

Tier (i) meets neither `4/10^7` nor `10^-6`. On tier (i) alone the outcome would be *limited*.

## 6. Tier (ii): exact first-order collection

### First-order vector

The k=0 term of (R04) is `c^(1)_M=H_M^{-1}P_M V Omega_0`. By (I1.5), `V Omega_0=-(tau/3) sum_f W_f Omega_0`, summed over the omitted faces of retained stars.

**Eigenvalue.** On the constant Haar vacuum, `W_f=(1/2)Tr U_f` is a `j=1/2` matrix coefficient in each of its four links. So `W_f Omega_0` is an eigenvector of every link Casimir: eigenvalue 3/4 on its own links and 0 elsewhere. It is therefore an eigenvector of `H_0` with eigenvalue `8*4*(3/4)=24`.

**Sector.** Every factor owning one of its links is excited. So `W_f Omega_0` lies in the `P_{M_f}` sector, where `M_f` is the face's owner set, and `H_{M_f} W_f Omega_0=24 W_f Omega_0`.

**Norm.** `norm^2=E_Haar[W^2]=1/4`, because the trivial representation occurs once in `1/2 tensor 1/2`.

**Orthogonality.** Two distinct plaquettes share at most one link (checked on 144 faces). A link of f outside g therefore appears exactly once in `W_f W_g`. Its Haar integral vanishes, so the vectors are orthogonal. Hence

\[
c^{(1)}_M=-\frac{\tau}{72}\sum_{f:\,M_f=M}W_f\Omega_0,\qquad \|c^{(1)}_M\|=\frac{|\tau|}{144}\sqrt{n_M}\le\frac{|\tau|}{144}\,n_M .
\tag{HNM-AV1-R14}
\]

**Cutoff behaviour.** In a cutoff space the vectors `W_f Omega_0` are eigenvectors of every `h_x`. Each is either kept or removed, so every count only decreases.

### Enumeration by translation covariance

The checker encodes the I1 table: 8 rows, 24 classes, 21 of them omitted. It re-derives that table from pi and the link tails and requires the two to agree.

A face of class k anchored at b owns links of `b+S_k`. The faces owning a link of factor u are therefore the pairs `(u-v,k)` with `v` in `S_k`, and their number is `sum_k |S_k|`:

| class support | classes | owner-set size | faces owning a link of u |
|---|---:|---:|---:|
| {0,e_y} | 3 | 2 | 6 |
| {0,e_x} | 1 | 2 | 2 |
| {0,e_x,e_y} | 1 | 3 | 3 |
| {0,e_z} (6 xz + 4 yz) | 10 | 2 | 20 |
| {0,e_x,e_z} | 2 | 3 | 6 |
| {0,e_y,e_z} | 4 | 3 | 12 |
| **total** | **21** | | **49** |

**Owner sets.** The 49 faces fall into **15** distinct owner sets containing u (2+2+3+2+3+3). Their face multiplicities are `n_M` in `{3,3,1,1,1,1,1,10,10,2,2,2,4,4,4}`. Each owner set has a unique anchor, its componentwise minimum, so each belongs to exactly one star (checked).

**Faces meeting R.** There are 49+49−16 = **82**. The 16 faces own links of both 0 and e_z: owner sets {0,e_z} (10 faces), {0,e_x,e_z} (2) and {0,e_y,e_z} (4).

**Faces inside R.** There are **10**, all with owner set {0,e_z}. The original W is one of them. The anchors of the faces meeting R are exactly the seven incident anchors `R-S`.

**Explicit boxes.** The checker also enumerates two boxes:

| box | sites | stars | faces |
|---|---:|---:|---:|
| `Lambda_2` | 125 | 64 | 1344 |
| `Lambda_3` | 343 | 216 | 4536 |

In both boxes the maximum is 49, reached at every bulk site, with smaller counts on the boundary, and the counts 82 and 10 are reproduced. The contract's numbers were compared only after derivation. 84 = 4·21, the number of faces in the four stars containing u, is recorded only as a labelled bound.

\[
t_1:=\|c^{(1)}\|_a\le\frac{49|\tau|}{144},\qquad a_1:=\sum_{M\cap R\ne\varnothing}\|c^{(1)}_M\|\le\frac{82|\tau|}{144}.
\tag{HNM-AV1-R15}
\]

With orthogonality inside each owner set, the exact values are:

- `t_1=(11+2sqrt3+3sqrt2+2sqrt10)|tau|/144 ~ 25.0313|tau|/144`;
- `a_1 ~ 43.4861|tau|/144` (directed square roots).

The anchored norm stays an l1 sum over owner sets. Replacing it by `sqrt(49)` or `sqrt(82)` is the rejected root-n misuse.

### Self-consistent remainder

`c-c^(1)=sum_{k>=1} L_k(c,...,c)/k!`. By the AM2 multilinear bound and the convexity of G,

\[
\|c-c^{(1)}\|_a\le J\,(G(t)-16)\le J\,t\,G'(t)\le 352\,J\,t\qquad(t\le R).
\tag{HNM-AV1-R16}
\]

Hence `t<=t_1+352Jt`, and

\[
t\le T:=\frac{t_1}{1-352J},\qquad \rho:=352\,J\,T>0\quad(\text{never zero for }\tau\ne0).
\tag{HNM-AV1-R17}
\]

A sharper directed form is `rho'=J(G^+(T)-16) ~ 288.0 J T`.

Now insert `c=c^(1)+(c-c^(1))` into (R10). The remainder part of the first-order sum is at most `2||c-c^(1)||_a`, and the two-creation product is at most `T^2`. So

\[
\varepsilon_{ii}=a_1+2\rho+T^2,\qquad D_{ii}=D(\varepsilon_{ii}) .
\tag{HNM-AV1-R18}
\]

Every term is tier (ii): `a_1` is exact first order, and `rho` and `T` come from (R17). The checker rejects two tier mixtures: the exact `a_1` combined with the crude t, and `t_1` used without (R17).

**Values at `tau=+-10^-8`** (all exact):

| quantity | value |
|---|---|
| `J` | `7/25000000` |
| `352J` | `77/781250` |
| `t_1` | `49/14400000000` |
| `T` | `49/14398580736` |
| `rho` | `3773/11248891200000000 ~ 3.354e-13` |
| `a_1` | `41/7200000000` |
| `T^2` | `~1.158e-17` |
| `eps_ii` | `461213409663624001/80984034066839961600000000 ~ 5.6951153e-9` |

\[
D_{ii}\le \tfrac{113902305553947264976096174312887}{10^{40}}\approx1.1390231\times10^{-8}\quad(\text{both signs}).
\tag{HNM-AV1-R19}
\]

Variants:

- with the directed remainder, `D <= 1.1389987e-8`;
- with owner-set orthogonality, `D <= 6.0404220e-9`.

The headline uses the conservative per-face form.

## 7. Removing the on-site cutoff for the ground vector (item 6)

AM2 removed the cutoff for eigenvalues only; the reduced density needs the ground vector itself. Fix N.

**Setup.**

- H is the untruncated operator: self-adjoint on `D(H_0)`, with compact resolvent and a simple ground `psi` of energy E (AM2 §6).
- `Q_n = tensor_x Q_{x,n}` commutes with `H_0` and increases strongly to 1.
- `H_n=Q_n H Q_n` on `Q_n H` is the AM2 cutoff operator. It has normalized ground `psi_n`, energy `E_n` and gap at least 1/2, uniformly in n.

**The trial vector converges in energy.** Put `w_n=Q_n psi/||Q_n psi||`. Because `psi` lies in `D(H_0)` and `Q_n` commutes with `H_0^{1/2}`,

`<Q_n psi, H_0 Q_n psi> = ||Q_n H_0^{1/2} psi||^2 -> <psi,H_0 psi>`.

Since V is bounded, `<w_n,H_n w_n> -> E`. `Q_n H` lies in the form domain, so the variational principle gives `E<=E_n<=<w_n,H_n w_n>`, and therefore `E_n -> E`. The uniform cutoff gap then gives

\[
1-|\langle\psi_n,w_n\rangle|^2\le 2\bigl(\langle w_n,H_nw_n\rangle-E_n\bigr)\longrightarrow0 .
\tag{HNM-AV1-R20}
\]

**The ground vectors converge.** From (R20), `|<psi_n,Q_n psi>| -> 1`. With phases fixed, `psi_n -> psi`. The rank-one projections converge in trace norm, since `|| |psi_n><psi_n| - |psi><psi| ||_1 = 2sqrt(1-|<psi_n,psi>|^2)`. Partial trace is a trace-norm contraction, so `rho^(n)_{N,R} -> rho_{N,R}` in trace norm.

**The bound survives.** Each `rho^(n)_{N,R}` obeys (R11) with a cutoff-uniform `eps`: compressions do not increase J, and first-order face vectors are either kept or removed. By the triangle inequality,

\[
\|\rho_{N,R}-P_R\|_1\le D\quad\text{for the untruncated finite-volume ground state, every }N\ge2 .
\tag{HNM-AV1-R21}
\]

**Checker fixtures.**

- The gap inequality is checked on an exact Cayley-rational 3×3 example.
- A counterexample shows why the gap is essential. The alternating family `diag(0,1/n)`, `diag(1/n,0)` has converging eigenvalues but alternating ground vectors. A proof by eigenvalues alone is therefore rejected.

## 8. Passage to the AQ state (item 7)

AQ1 extracts subsequences `N_k` along which every local density converges in trace norm. For any such subsequence with limit density `rho_R`,

`||rho_R-P_R||_1 <= ||rho_R-rho_{N_k,R}||_1 + D -> D`.

\[
\text{For every subsequential limit of AQ1's centered whole-star construction (the chosen one included), at either sign of }|\tau|\le10^{-8}:\quad \|\rho_R-P_R\|_1\le D,\ \ D\in\{D_{ii},D_i\}.
\tag{HNM-AV1-R22}
\]

The quantifier is "every subsequential limit". This is not uniqueness, not whole-sequence convergence and not a rate in N. All the limits lie in the same trace-norm ball, but they are not identified with one another.

Trace-norm convergence is essential. A weak-* limit taken on finite-rank observables can lose mass. For example, `rho_n=(1-D/2)|e_0><e_0|+(D/2)|e_n><e_n|` has a weak limit of trace `1-D/2`. AQ1's energy tightness excludes this.

## 9. Consequences and scaling (item 8)

The `P_R` moments are `omega_0(W)=0` and `omega_0(W^2)=1/4`. They are read from the contract and re-derived from the Clebsch–Gordan series.

**Mean.** Trace duality with `||W||<=1` gives `|omega(W)|<=D`.

**Second moment.** For a trace-zero difference, the positive and negative parts have equal trace. So `|Tr[(rho-P)A]|<=||rho-P||_1/2` for every effect `0<=A<=I`. Applying this to `A=W^2`:

\[
|\omega_\tau(W)|\le D,\qquad |\omega_\tau(W^2)-\tfrac14|\le \tfrac D2,\qquad \tfrac14-\tfrac D2-D^2\le \operatorname{Var}(W)\le\tfrac14+\tfrac D2,
\tag{HNM-AV1-R23}
\]

for both tiers and both signs. The exact rationals are in `consequences` in the checker output.

- The variance bound charges `m^2<=D^2`. A centering shortcut that drops this charge is rejected.
- Neither the value nor the sign of `omega(W)` is claimed.
- The original W is itself one of the ten first-order faces inside R, so no parity argument removes a first-order mean. D is linear in tau and pays for that mean.

**Scaling.** Compare `tau=10^-8` with the contract's scaling-only point `10^-10`, using rational brackets on the ratio of the formula values:

\[
\frac{D_i(\tau)}{D_i(\tau/100)}\approx100.000293,\qquad \frac{D_{ii}(\tau)}{D_{ii}(\tau/100)}\approx100.0117\ \in[99,101];\qquad \text{AT4's }2\sqrt{49|\tau|/3}:\ \text{ratio exactly }10\in[9.9,10.1].
\tag{HNM-AV1-R24}
\]

At `tau=10^-8`, the AT4 square-root bound is about `8.0829e-4`. Tier (ii) is about 7.1×10⁴ times smaller.

## 10. Targets, AV2 relation and the checker (item 9)

**Targets.**

- The target read from the contract is `D_ii <= 1/2500000`. It is met at both signs, with a margin of about 35.1.
- The secondary comparison `10^-6` is met by tier (ii) only.

**AV2 relation.** The relation `2(D+D^2)+49*10^-8/pi <= 10^-6` is read from the contract and evaluated with a Machin lower bound on pi.

- It holds for `D_ii`, for the target itself, and for the contract's stated `4.22e-7`.
- It fails for `4.23e-7`, for `10^-6` and for `D_i`.

**The checker.** `check.py --output <absolute fresh directory>` uses only the standard library and exact Fractions.

- **Hashes:** it records the SHA-256 of the contract snapshot, and its own hash before evaluation.
- **Inputs:** it reads the target, the reference moments and the parameters from the contract snapshot.
- **Outputs:** every constant as a rational string; both tiers at both signs, with variants; the enumerations; the fixtures; the claim flags, all false; and `tier_ii_target_met: true`.
- **Checks:** 54 in total. Each of the 25 contract controls is implemented as one or more damaging mutations whose rejection is required. Rejections are explicit exceptions, never `assert`.

The 25 controls:

- missing_incoming_stars
- full_original_wilson_cover
- wrong_delta_alpha_hbar_clock
- vector_versus_scalar_centering
- first_order_mean_charged
- tau_scaling_exponent
- changed_model_relabelled
- coherent_evidence_tampering (five coherently rehashed contract tampers plus a byte change)
- insufficient_verdict_retained
- exact_arithmetic_admission
- root_n_misuse
- no_priority_or_continuum_claim
- deleted_normalization
- outside_creations_do_not_cancel_naively
- omitted_adjoint_terms
- straddling_supports_counted
- anchored_norm_restricted_to_cover
- am2_fixed_point_constants
- first_order_face_enumeration
- cutoff_vector_removal
- aq_passage_trace_norm_only
- tier_mixing_rejected
- face_count_all_sites (sites-0-and-e_z scope; orthant count 37; contract-copied and hard-coded counts)
- reverse_premise_isolation (the `inputs/` inventory is exactly AGENTS.md + contract + shared_premises)
- av2_feasibility_threshold

Output is byte-identical under `python3 -B` and `python3 -B -O`.

**Method notes.** These are the frozen Round32 method rules, used as modern lenses; no historical figure endorses anything here.

- *Newton analysis/synthesis:* §3 runs backwards from the inequality to its sufficient premise, then forwards.
- *Tesla (source, load, transfer):* the source is the seven incident stars (82 faces meeting R), the load is the cover R, and the transfer element is the partial vacuum contraction, with no clock because the bound is static. The +tau/−tau mirror is a control, not a magnitude estimate.
- *Historical-panel rule:* uniform local closeness is not called uniqueness.

## 11. Limitations and exclusions

**Claim exclusions, exactly as the contract lists them:**

- cap-level Euclidean certificate (AV2)
- interaction-induced shift or its sign (AW)
- uniform Wilson magnetic theory (AX)
- AQ uniqueness, whole-sequence convergence or a rate in N (AY)
- continuum construction (AZ)
- Yarotsky/HTW constant evaluation
- scientific priority
- the value or sign of omega(W) beyond |omega(W)|<=D
- the first-order coefficient 1/144
- vanishing of first-order C(s) or omega(W^2) (AW1)

**Preregistered exclusions,** also respected:

- free reference inside enclosure ⇒ no interaction claim;
- uniqueness of the AQ state;
- whole-sequence convergence or rate in N;
- continuum or weak coupling;
- transfer from a finite graph;
- relabelling a static shift as dynamical;
- scientific priority.

**Claim flags,** all `false`: `continuum_claim`, `uniform_wilson_claim`, `resolved_interaction_shift`, `scientific_priority_verified`, `euclidean_node_certified`, `first_order_parity_claim`.

**Scope and honest gaps.**

- **One route only.** This is the reverse route from one producer. The acceptance rule needs both routes in both producers plus review, so the outcome stated above is a proposal.
- **Inherited, not re-proved:**
  - AM2's multilinear estimate, fixed point, ground identification and cutoff eigenvalue passage;
  - AQ1's trace-norm compactness and subsequence;
  - I1's dictionary;
  - AT4-F08's inequality, which is re-proved in two lines above.
- **Fixtures.** They audit the algebra and the rejection logic. They do not prove the infinite-dimensional statements, which rest on the arguments above.
- **Arithmetic.** Square roots, exponentials and pi use outward directed rounding at 10^-40. Decimals are truncated previews.
- **Sign-blind bound.** The bound depends only on |tau|.
- **Model-specific.** It holds for the zero selected triple (Haar reference), this cover R and fixed spacing. Nothing transfers to other triples, to uniform Wilson theory or to the continuum.
- **Independence.** The product-ordering idea is shared. The contract's candidate counts and the `49|tau|/144` candidate were visible before derivation; the counts were re-derived and compared afterwards.

All eleven required items were executed on the reverse route, and no step is left incomplete. The step leaning hardest on inherited results is item 6: it uses AM2's uniform cutoff gap and the uniqueness of the untruncated ground exactly as admitted.

## Inherited inputs read

Beyond the snapshots in `inputs/`, I read four files:

- `research/round32/tools/README.md` and `research/round32/tools/freeze.py`, for the producer protocol;
- `research/round29/forward/am2/check.py` and `research/round31/forward/at5/check.py`, for code style and the admitted creation-algebra fixture.

The repository copy of the contract was compared with its snapshot by a byte comparison only.

## Reproduce

```bash
python3 -B research/round32/reverse/av1/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/reverse/av1/check.py --output /absolute/fresh/dir2
python3 -B research/round32/tools/freeze.py verify research/round32/reverse/av1
```
