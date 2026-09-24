# Hruday parity theorem, link-flip antisymmetry and the first-order Wilson mean — AW1 forward

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production under the frozen AW1 contract (`research/round32/contracts/aw1.json`, sha256 `c24bf7eb6a1c24034427c810a9c26c4c86d1f9c1d31b0fe36ea4cf2a796814ef`). It is correlated model-agent work, not independent human review.

**What this producer read.**
- The contract snapshot first. After that, only the files under `inputs/`: AGENTS.md, the shared premises and the four forward-additional premises.
- The forward-additional premises are the skeptic triage, the skeptic loop-2 response and the historical and modern loop-2 responses. They already state the parity rule, the flip set `E`, the 49/15/82/10/72 counts and the rough `K_2` structure. These are therefore **shared panel premises** for the forward route, and I disclose them as such.
- For protocol and code style only: `research/round32/tools/README.md`, `research/round32/tools/freeze.py` and `research/round32/forward/av1/check.py`.
- The two named assistant scripts `research/round32/experts/historical/assistant-1/haar_parity_exact.py` and `research/round32/experts/modern/assistant-1/flip_parity_k2.py`. I read them as inherited tooling but did not import them. Every quantity they compute is re-derived in `check.py`.

Nothing under `research/round32/reverse/`, no current skeptic AW1 file, and no other current AW1 work was read.

**Attribution.** The character-parity rule and the centre-flip argument are standard kinds of argument (Haar orthogonality of SU(2) matrix elements; a centre `Z_2` symmetry of the plaquette sum). The contribution here is their application to the named model, with exact constants. Scientific priority is unverified.

## Verdict (forward route)

All eight contract items are executed on the forward route.

1. **Parity theorem: complete, with the allowed caveat.**
   - In every centered whole-star box, every first-order term of `omega(W^2)`, of the real-time correlation `c(theta)` and of `C(s)` vanishes. The state, vector-centring, Duhamel and energy terms are each shown to vanish separately, from SU(2) tensor-power multiplicities.
   - `W Omega_0` is not mapped back into the energy-24 multiplet by any omitted face. The gauge-invariant multiplet has zero first-order splitting.
   - For `omega(W^2)` I also prove a second-order constant uniform in volume: `|omega(W^2)-1/4| <= K_W2 tau^2`, with `K_W2 ≈ 3354.567`.
   - For `C(s)` the `O(tau^2)` constant is **explicitly left unbounded** (not proved uniform in `N`), as the contract allows.
2. **Flip lemma: complete.**
   - Every plaquette of `Z^3` meets `E` in 1 or 3 links. All 24 (orientation, base parity) classes are enumerated, together with the full sets of 49 omitted faces of seven probed factors and every plaquette of the `N=2` box.
   - Consequently `U_E H_N(tau,kappa) U_E^* = H_N(-tau,-kappa)`, including every on-site cutoff compression.
   - At `kappa=0`: `omega(W)` is odd in `tau`, and `omega(W^2)`, `C_N` and `c_N` are even.
   - Passage to AQ is a statement about the whole set of subsequential limits. Oddness gives no `O(tau^3)` remainder.
3. **First-order coefficient.** `omega_tau(W) = +tau/144 + r(tau)` for either sign of `tau`. Only `f=W` contributes. The sign is re-derived twice from I1.5, and a one-plaquette finite fixture confirms it.
4. **K_2, uniform in volume (exact rationals).**
   - Exact tier: `K_2^+ = 81104877995836618199905135109761286809699489/24176936535511801466930759024724079017984 ≈ 3354.63832966`. The AM2 remainder term, `≈ 3354.108`, dominates.
   - Crude tier: `K_2^crude = 1937877026146766159414097129/244140625000000000000 ≈ 7.93754429909×10^6`.
5. **Feasibility.**
   - `K_2^+ tau = 3.3546×10^-5 <= 1/288` at `tau=10^-8`. The sign margin `1/(144 K_2^+ tau) ≈ 207.01` exceeds 2.
   - The frozen rule gives **`tau_AW2 = 10^-8`**.
   - The crude tier fails at the cap and is retained.
   - No enclosure of `omega(W)` is admitted here.
6. **Checker.** It runs 41 exact checks. All 30 contract controls reject at least one damaging mutation through an explicit exception. Replays under normal and `-O` Python are byte-identical.

**Proposed forward verdict:** `accepted_within_scope` for the forward half, with sub-label `static_not_dynamic`. The gate also needs the reverse route and skeptical review.

## 1. Model and conventions

The model is the AV1/AM2/AQ1 zero-selected patterned family:
- SU(2) Kogut–Susskind form on `Z^3` at fixed spacing, with coarse 24-link factors;
- selected triple exactly `(0,0,0)`;
- centered whole-star boxes `Lambda_N=[-N,N]^3` with `N>=2`;
- cover `R={0,e_z}` of the original xz Wilson loop `W=(1/2)Tr[U_{0,x}U_{e_x,z}U_{e_z,x}^{-1}U_{0,z}^{-1}]`, whose four links have owners `0,0,e_z,0`;
- both signs of `|tau|<=10^-8`;
- fixed positive `alpha`, `hbar`, `E_star` and lattice spacing.

In normalized units `delta=alpha/8`:

\[
 H_N=H_0+V,\quad H_0=\sum_b h_b,\quad h_b=8\sum_{e\in b}C_e,\quad
 V=\sum_{b+S\subset\Lambda_N}\phi_b,\quad \phi_b=-\tfrac{\tau}{3}\sum_{f\in O_b}W_f .
 \tag{HNM-AW1-F01}
\]

In `alpha` units, `G_N=H/alpha` has `V_b=phi_b/8=-(tau/24) sum W_f`. Each `W_f Omega_0` has energy 3 (`alpha` units), or 24 (normalized), and norm `1/2`.

AM2 constructs the unique ground `psi=e^{-C}Omega_0` in every box and on-site cutoff space, and AV1 admits its constants. With `L_0=H_0^{-1}P_perp V Omega_0`:

\[
 c=L_0+\sum_{k=1}^{8}\frac{L_k(c,\dots,c)}{k!},\qquad
 L_0=c^{(1)}=-\frac{\tau}{72}\sum_f W_f\Omega_0\ \ (\text{both unit systems}),\qquad \|W_f\Omega_0\|=\tfrac12 .
 \tag{HNM-AW1-F02}
\]

The admitted exact-tier constants are:
- `J=28|tau|`, from four incoming stars of norm `7|tau|`;
- `t_1=49|tau|/144`, from 49 faces per factor, each with `||c^(1)_f||=|tau|/144`;
- `t=||c||_a <= T := t_1/(1-352J)`;
- `rho := ||c-c^(1)||_a <= 352 J T`;
- `eps=2T+T^2`.

\[
 T=\tfrac{49}{14398580736},\quad \rho=\tfrac{3773}{11248891200000000},\quad
 \varepsilon=\tfrac{1411060914529}{207319127211110301696}\quad(\tau=\pm10^{-8}).
 \tag{HNM-AW1-F03}
\]

The checker recomputes `2eps(1+eps)/(1+eps^2)` and obtains exactly the AV1 gate's `D_ii`, which it reads from the snapshot. This binds the constants to AV1.

## 2. Parity theorem (item 1)

### 2.1 Centre grading and character multiplicities

For a link `e`, let `(Pi_e psi)(...,U_e,...)=psi(...,-U_e,...)`. On the Peter–Weyl block `V_j (x) V_j^*` of that link, `Pi_e=(-1)^{2j}`. Because `-1` is central, `Pi_e` has these properties:
- it commutes with left and right translations, and therefore with the electric generators, every Casimir, `H_0`, `P_perp`, `H_0^{-1}P_perp`, `e^{-sH_0}`, `e^{i theta H_0}` and every on-site spectral cutoff;
- it commutes with every original endpoint gauge action;
- it fixes `Omega_0`;
- `Pi_e W_f Pi_e = (-1)^{[e in f]} W_f`.

The character form of the same fact is as follows. The Haar integral over one link of a product of `k` spin-1/2 matrix elements is the projection onto the invariants of `V_{1/2}^{(x)k}`. That multiplicity is 0 for odd `k` and Catalan(`k/2`) for even `k`. The checker computes it by Clebsch–Gordan recursion, obtaining `1,0,1,0,2,0,5,0,14,0,42` for `k=0..10`. Hence:

\[
 \langle\Omega_0,A_0W_{f_1}A_1\cdots W_{f_k}A_k\Omega_0\rangle=0
 \ \text{unless every link lies in an even number of } f_1,\dots,f_k ,
 \tag{HNM-AW1-F04}
\]

where each `A_i` is centre-even (any function of the Casimirs). Two distinct plaquettes share at most one link, as checked over all pairs among the 82 faces meeting `R`. Therefore:
- `E[W W_f] = (1/4) delta_{f,W}`;
- `E[W^2 W_f] = 0` for every omitted `f`, including `f=W`, because `E[W^3]=0` (each of `W`'s links is covered three times);
- `E[W_g W_f W_h] = 0` for all plaquettes `g,f,h`, because `g xor h` is never a single face.

### 2.2 Haar moments by three routes

| n | character count `2^-n mult` | Weyl/Wallis `(2/pi) int cos^n sin^2` | free-link route (AQ2 §5) |
|---|---|---|---|
| 1 | 0 | 0 | 0 |
| 2 | 1/4 | 1/4 | 1/4 |
| 3 | 0 | 0 | 0 |
| 4 | 1/8 | 1/8 | 1/8 |

The routes agree through `n=8`, where all three give `7/128`. The free-link route is the named cross-check. `W`'s face contains a free z link, so the face holonomy is Haar under the reference, and `W=q_0` for `q` uniform on `S^3`, giving `E[q_0^{2m}]=prod_{i<m}(2i+1)/(4+2i)`. The contract's reference values `E[W]=0`, `E[W^2]=1/4`, `E[W^3]=0` and `E[W^4]=1/8` are read from the contract and reproduced.

### 2.3 First-order terms, each separately

In each box the interaction is bounded, and `E_0` is simple and isolated with gap at least `1/2` (AM2). Kato analytic perturbation theory therefore makes the ground projection, `omega_N(W^2)`, `c_N(theta)=<chi,e^{i theta(G-E)}chi>` and `C_N(s)=<chi,e^{-s(G-E)}chi>` real-analytic in `tau` near 0. Here `chi=(W-omega_N(W))psi/||psi||`. Write `psi_1=-L_0/tau=(1/72)sum_f W_f Omega_0` and `V_1=-(1/24)sum_f W_f` (`alpha` units). Using (F04):

\[
\begin{aligned}
 \partial_\tau\omega_N(W^2)|_0&=2\operatorname{Re}\langle(W^2-\tfrac14)\Omega_0,\psi_1\rangle=\tfrac1{36}\textstyle\sum_f\big(E[W^2W_f]-\tfrac14E[W_f]\big)=0,\\
 \text{state term of }C_N,\,c_N&=2e^{-3s}\operatorname{Re}\langle W^2\Omega_0,\psi_1\rangle\ \big(\text{resp. } e^{3i\theta}\big)=0,\\
 \text{vector-centring term}&=-m_1\,e^{-3s}\langle W\Omega_0,\Omega_0\rangle=-\tfrac1{144}e^{-3s}E[W]=0,\\
 \text{Duhamel term}&=-s\,e^{-3s}\langle W\Omega_0,(V_1-E_1)W\Omega_0\rangle=\tfrac{s e^{-3s}}{24}\textstyle\sum_fE[W\,W_f\,W]=0,\\
 \text{energy term } E_1&=\langle\Omega_0,V_1\Omega_0\rangle=-\tfrac1{24}\textstyle\sum_fE[W_f]=0 .
\end{aligned}
 \tag{HNM-AW1-F05}
\]

The real-time Duhamel term is `i theta e^{3i theta}<W Omega_0,(V_1-E_1)W Omega_0>=0`. The contract's "c^(1) against `W alpha^0_theta(W) Omega_0`" is `e^{3i theta}<c^(1),W^2 Omega_0>=0`.

The centring term needs care. The uncentered mean has a **nonzero** first-order coefficient, `m_1=1/144`. It drops out of `C` only because `W Omega_0` is orthogonal to `Omega_0`. The same face sum applied to the mean gives `1/144`, not 0. The checker evaluates every sum exactly, over all 1344 retained faces of the `N=2` box and over the 82 bulk faces meeting `R`.

### 2.4 The energy-24 multiplet

- **`W_f W Omega_0` has no energy-24 component.** The per-link representation content of `W_f W Omega_0` is fixed by the link counts:
  - `f=W`: every link has `j in {0,1}`, so the energy is a multiple of 16, in `{0,16,32,48,64}`;
  - `f` sharing one link with `W`: energy in `{36,52}`;
  - `f` disjoint from `W`: energy 48.

  So `P_24 W_f W Omega_0 = 0` for every omitted `f`. The only component with the vacuum's representation content is the identity component `E[W^2] Omega_0 = (1/4) Omega_0`, which occurs only for `f=W` and lies at energy 0.
- **The gauge-invariant multiplet.** `8 sum_e j_e(j_e+1)=24` forces exactly four `j=1/2` links. The checker enumerates Casimir sums: only `(1/2)^4` works. Gauge invariance needs even degree at every vertex, so the four links form a 4-cycle, and the 4-cycles of `Z^3` are exactly the plaquettes (the checker finds 12 through the origin). Each vertex of degree 2 carries a one-dimensional invariant. The gauge-invariant energy-24 multiplet is therefore `span{W_g Omega_0}`. By (F04), `<W_g Omega_0, V W_h Omega_0> = -(tau/3) sum_f E[W_g W_f W_h] = 0`, and the checker confirms `|g xor h| in {6,8}` over all 417 plaquettes of the `N=1` box.
- **Result.** The first-order splitting of the multiplet is zero.

\[
 P_{24}VW\Omega_0=0,\qquad P^{\rm phys}_{24}VP^{\rm phys}_{24}=0 .
 \tag{HNM-AW1-F06}
\]

On non-gauge-invariant energy-24 vectors, parity does *not* force the compression to vanish. An example is a set `p` of four `j=1/2` links with `|p cap f|=2`. The zero-splitting statement is therefore made only for the gauge-invariant multiplet, where `chi` and the dynamics live. A mutation claiming the full-space statement is rejected.

### 2.5 Conclusions of item 1

- **`C(s)`.** For every box, `C_N(s)=e^{-3s}/4+O_N(tau^2)`, and `c_N(theta)=e^{3i theta}/4+O_N(tau^2)` for every real `theta`. The `O(tau^2)` constant is **explicitly unbounded**: uniformity in `N`, and so an AQ-level second-order constant for `C(s)`, is not proved here. It would need second-order dynamics, meaning the 40-star relative-unitary step. In the AQ limits only the evenness of item 2 is inherited.
- **`omega(W^2)`: a uniform constant.** Put `A=W^2-1/4`. Then `<Omega_R,A Omega_R>=0`, `||A Omega_R||=(E[W^4]-E[W^2]/2+1/16)^{1/2}=1/4` and `||A||=3/4`. Insert the product-ordering split `psi=psi_out+delta` of AV1 into `<psi,A psi>/<psi,psi>`:
  - the first-order parts of `c_{0}` and `c_{e_z}` vanish, because no omitted face has single-factor support;
  - `<A Omega_R, c^(1)_R>=0` by (F04);
  - the remaining supports are bounded exactly as in Section 4.

  This gives

\[
 |\omega(W^2)-\tfrac14|\le 2\cdot\tfrac14\cdot2\rho+2\cdot\tfrac14\,T\big(72\,\tfrac{|\tau|}{144}+2\rho\big)
 +2\cdot\tfrac14\big(33\tfrac{|\tau|}{144}+\rho\big)^2+\tfrac34\varepsilon^2=:K_{W^2}\tau^2,\quad K_{W^2}\approx3354.5671 ,
 \tag{HNM-AW1-F07}
\]

  uniformly in `N`, the cutoff and every AQ subsequential limit. The exact rational is in `results.json`. The free value `1/4` lies inside, so no shift is resolved.

## 3. Link-flip antisymmetry lemma (item 2)

### 3.1 Odd intersection

The flip set, read from the contract, is

\[
 E=\{(p,x):p_y\ \text{even}\}\cup\{(p,y):p_z\ \text{even}\}\cup\{(p,z):p_x\ \text{even}\}.
 \tag{HNM-AW1-F08}
\]

Each link direction is keyed to the parity of the *next* coordinate. In a plaquette with directions `a<c`, the two parallel `a`-links are keyed to a coordinate that differs by one between them exactly when that coordinate is `c`'s:
- for `xy`, the x-links are keyed to `p_y`, so exactly one of them is in `E`, and the y-links, both keyed to `p_z`, are both in or both out;
- `xz` and `yz` work the same way.

So `|f cap E| in {1,3}`. Translation by any even vector preserves `E`. Hence `|f cap E|` depends only on the orientation and on `p mod 2`, and the checker enumerates all `3×8=24` classes, together with covariance under 16 even shifts per class. It also enumerates, in full:
- all 49 omitted faces of each of seven factors (`z`-parities 0 and 1, negative coordinates included);
- the three selected faces of each;
- all 1344 retained faces and all 2335 plaquettes of the `N=2` box (1082 meet `E` once, 1253 three times);
- the Wilson face, which meets `E` in 3 links.

The following mutations are rejected:
- `E` minus one link, which gives even plaquettes;
- a periodic box with an odd side, which gives an even plaquette at the wrap;
- a centre gauge transformation (a coboundary, even on every plaquette) presented as the flip;
- a spin-1 face term claimed to flip, since `(-1)^{2j|f cap E|}=+1`.

### 3.2 The unitary and the identity

`U_E=prod_{e in E cap Lambda} Pi_e` is diagonal in the Peter–Weyl basis with entries `(-1)^{2j_e}`. It commutes with every Casimir, with every original endpoint gauge action (`g(-U)h^{-1}=-(gUh^{-1})`) and with every on-site cutoff projection at `kappa=0`, and `U_E W_f U_E^* = -W_f` for every plaquette. The checker audits this on exact fixtures:
- **one link.** The `j<=1/2` compression of `L^2(SU(2))` in the basis `(1,U_11,U_12,U_21,U_22)`, with exact Haar moments. The grading `diag(1,-1,-1,-1,-1)` anticommutes with multiplication by each `U_ab` and commutes with the Casimir;
- **one plaquette.** The gauge-invariant character basis `chi_j(U_P)`, `j<=3`, with `U=diag((-1)^{2j})`, `UWU=-W` and `UH_0U=H_0`;
- **rational SU(2) holonomies.** Exact unit quaternions on 57 faces show that the trace flips under `E` and is gauge invariant.

With `kappa` the selected triple, the identity is

\[
 U_E\,H_N(\tau,\kappa)\,U_E^*=H_N(-\tau,-\kappa)\qquad\text{and}\qquad
 U_E\,Q_LH_N(\tau,\kappa)Q_L\,U_E^*=Q_L'H_N(-\tau,-\kappa)Q_L' ,
 \tag{HNM-AW1-F09}
\]

where `Q_L'` is the cutoff of `h_b(-kappa)`, which equals `Q_L` at `kappa=0`. For `kappa!=0` the identity relies on the inherited form of the strip operator (Casimirs, the three selected face traces and scalars). A scalar shift cancels in the ground-subtracted on-site operator (I1.3), because `E_strip` transforms with the same scalar.

**Positive nonzero-`kappa` demonstration.**
- An exact compression of `H_0-(tau/3)W-kappa W_g`, with `g` a selected face of factor 0, onto `span{Omega_0, W Omega_0, W_g Omega_0}` satisfies `U H(tau,kappa) U = H(-tau,-kappa)`. For `kappa!=0` it is not `H(-tau,kappa)`.
- Every selected face of every probed factor meets `E` oddly.

Claiming `tau`-antisymmetry from `U_E` at a nonzero triple is rejected.

### 3.3 Covariance, AQ passage, and no third-order claim

At `kappa=0`, AM2's grounds are unique for both signs. `U_E Omega_0=Omega_0`, and the intermediate normalization `<Omega_0,psi>=1` is unique. Together these give `e^{-C(-tau)}Omega_0 = U_E e^{-C(tau)}Omega_0`, so `c_I(-tau)=U_E c_I(tau)`. Consequently `c^(1)` is odd and `||c||_a` is even, and for every box and cutoff:

\[
 \omega_{N,-\tau}(W)=-\omega_{N,\tau}(W),\quad \omega_{N,-\tau}(W^2)=\omega_{N,\tau}(W^2),\quad
 C_{N,-\tau}(s)=C_{N,\tau}(s),\quad c_{N,-\tau}(\theta)=c_{N,\tau}(\theta),
 \tag{HNM-AW1-F10}
\]

because `chi_{-tau}=-U_E chi_tau` and `G_{-tau}-E=U_E(G_tau-E)U_E^*`.

**AQ passage.** Let `S(tau)` be the set of all local trace-norm limits of `omega_{N_k,tau}` along subsequences of centered boxes. `alpha_E` (local conjugation by `U_{E cap F}`) is a well-defined automorphism of the quasi-local algebra. For each subsequence, `omega_{N_k,-tau}=omega_{N_k,tau} o alpha_E`, so `S(-tau)=S(tau) o alpha_E` as sets. The AQ1 dynamics is the norm limit of finite-volume dynamics, hence `alpha_E o T^tau_t = T^{-tau}_t o alpha_E`. For each `omega in S(tau)`:
- `(omega o alpha_E)(W) = -omega(W)`;
- `omega o alpha_E` has the same `omega(W^2)`, `c(theta)` and `C(s)` as `omega`.

AQ1's *chosen* states at `+tau` and `-tau` come from `tau`-dependent diagonal extractions. They are related pointwise only along a common subsequence, and the pointwise claim without one is rejected.

**No third-order claim.** In each box, analyticity together with oddness removes the `tau^2` Taylor coefficient of `omega_N(W)`. It does not turn the uniform bound `K_2 tau^2` into `O(tau^3)`: `r(tau)=K tau|tau|` is odd and exactly second order. The checker rejects an `O(tau^3)` claim built on that counterexample. Any third-order remainder is a separate obligation, and `third_order_remainder_claim` is `false`.

**Remark (post-freeze forward observation, not claimed, outside AW1's model).** Let `E''={(p,x): p_x mod 4 in {0,1,2}, p_y mod 4 in {1,2}}`. Its mod-2 coboundary is exactly the indicator of the selected faces. Hence `E*=E xor E''` meets every omitted plaquette oddly and every selected plaquette evenly; the checker verifies this over the `N=2` box. If reviewed, `U_{E*} H(tau,kappa) U_{E*}^* = H(-tau,kappa)` would make `omega(W)` odd in `tau` at *every* selected triple. The contract's statement is correct for `U_E`, but the selection note's wording "antisymmetry in tau holds only at the zero selected triple" would then be too strong. I record this for the skeptic and advisor and make no claim.

## 4. First-order coefficient (item 3)

### 4.1 Derivation

Split `psi=psi_out+delta` as in AV1 (F07–F09):
- `psi_out=Omega_R (x) phi_out`, with `n=||phi_out||`;
- `delta=-sum_{I meets R} c_I psi_out + sum_{I ni 0, J ni e_z, disjoint} c_I c_J psi_out`, with `||delta||=en <= eps n`.

`W` acts on `H_R` and `<Omega_R,W Omega_R>=0`, so

\[
 \omega(W)=\frac{2\operatorname{Re}\langle W\Omega_R\otimes\phi_{\rm out},\delta\rangle+\langle\delta,W\delta\rangle}{n^2(1+e^2)} .
 \tag{HNM-AW1-F11}
\]

**Single-component overlap.** For `x in R`, the partial vacuum contraction `<Omega_x|W Omega_R>` vanishes. The reason is that each link of `W` owned by `x` carries one spin-1/2 factor, and `mult(1)=0`. Therefore:
- creations with `I={0}` or `I={e_z}` contribute exactly 0;
- straddling creations meeting `R` in one site (66 first-order faces) contribute exactly 0, since the other site of `R` stays in `Omega`.

Only `c_R` overlaps `W Omega_R`:

\[
 -2\operatorname{Re}\langle W\Omega_R,c_R\rangle=-2\langle W\Omega_0,L_0\rangle-2\operatorname{Re}\langle W\Omega_R,(c-c^{(1)})_R\rangle,\qquad
 -2\langle W\Omega_0,L_0\rangle=\tfrac{\tau}{36}\sum_{M_f=R}E[WW_f]=\frac{\tau}{144}.
 \tag{HNM-AW1-F12}
\]

Of the 10 faces with owner set exactly `R`, only `f=W` contributes (`E[W W_f]=0` otherwise). **In words:** `omega_tau(W) = 2<W Omega_0, psi^(1)> + O(tau^2)`, where `psi^(1)=-L_0` is the first-order correction of the ground vector.

**Contract display.** The contract writes `2<W Omega_0,c^(1)>`. That is correct if `c^(1)` means the vector correction `psi^(1)`. With AV1's creation convention (`c^(1)=L_0`, `psi=e^{-C}Omega_0`), the literal display gives `-tau/144`, and the checker rejects that as a sign error. Both readings give `+tau/144` once the convention is fixed.

### 4.2 Sign

The sign is re-derived twice from I1.5 (`phi_b=-(tau/3)sum W_f`).
- **Perturbation theory.** `L_0=-(tau/72)sum W_f Omega_0`, so `-2<W Omega_0,L_0>=+tau/144`. The per-face coefficient is `-(tau/3)/24=-(tau/24)/3=-tau/72` in both unit systems. Mixing the units gives `tau/1152` or `tau/18`, which are rejected.
- **Two-dimensional Rayleigh–Ritz.** On `span{Omega_0, W Omega_0}`, `<W Omega_0,V Omega_0>=-tau/12` and `<W Omega_0,H W Omega_0>=6`. The energy `6 eps^2-(tau/6)eps` is minimized at `eps=tau/72`, and then the mean is `2 eps E[W^2]=tau/144`. The physical reading: for `tau>0` the interaction lowers the energy where `W>0`.
- **Finite fixture.** On the one-plaquette character basis (`H_0=32j(j+1)`, `V=-(tau/3)W`), the exact Rayleigh–Schrödinger series is `<W>=tau/144+0·tau^2-(5/11943936)tau^3+...`, stable for `j_max=2, 5/2, 3`. The exact `j<=1/2` ground state at `tau=±10^-8` has `<W>` in rational brackets of sign `sign(tau)` (`≈±6.944444444e-11`). This fixture is labelled `FG(one_plaquette, ...)`, `transfers_to_aq:false`.

\[
 \omega_\tau(W)=+\frac{\tau}{144}+r(\tau),\qquad \omega^{(1)}_{\pm10^{-8}}=\pm\frac{1}{14400000000}.
 \tag{HNM-AW1-F13}
\]

### 4.3 Controls on the coefficient

- **Wrong face.** Each of the 9 other faces inside `R`, and every other face meeting `R`, contributes 0. Counting all 10 would give `10 tau/144`, which is rejected.
- **`f=W` separated.** `W` is the xz class `r=0,s=0` among the 21 omitted classes anchored at factor 0. The other 20 classes have `E[W W_f]=E[W^2 W_f]=0`, while `W` itself has `1/4` and `E[W^3]=0`. Merging all 21 (`21 tau/144`) and excluding `W` from the omitted set (`0`) are both rejected.
- **Orientation.** `(1/2)Tr` is invariant under reversal and under cyclic shift of the base point, checked on exact quaternion holonomies. Every omitted class at anchor 0, in each of the planes xy, xz and yz, used as the observable, gives first-order mean `+tau/144`. A selected face used as the observable gives 0 at the zero triple, because its own coefficient is 0.

## 5. Second-order remainder K_2 (item 4)

### 5.1 Amplitude lemma

For `u` outside `R`, order the creations of `phi_out` that contain `u` last. Only one of them can act, so `(Q_u (x) 1)phi_out = -sum_{J ni u} c_J phi'` and `(P_u (x) 1)phi_out = phi'`. Hence

\[
 \|(Q_u\otimes1)\phi_{\rm out}\|\le t\,\|\phi_{\rm out}\| .
 \tag{HNM-AW1-F14}
\]

### 5.2 Itemized bound

From (F11)–(F14), with `a=|tau|/144` the per-face first-order norm:

\[
 \Big|\omega(W)-\frac{\tau}{144}\Big|\le
 \underbrace{\rho}_{\rm am2\_remainder}
 +\underbrace{T\,(6a+\rho)}_{\rm straddling}
 +\underbrace{(33a+\rho)^2}_{\rm two\_creation}
 +\underbrace{\varepsilon^2}_{\rm density}
 +\underbrace{a\,\varepsilon^2}_{\rm normalization\ (3rd\ order)}
 =:K_2\tau^2 .
 \tag{HNM-AW1-F15}
\]

Each term, with its enumeration pin:
- **AM2 remainder, overlap multiplier 1.** The term is `|2Re<W Omega_R,(c-c^(1))_R>| <= 2||W Omega_R|| ||(c-c^(1))_R|| <= rho`, with `||W Omega_R||=1/2` as a positive exact control. The factor 4 (`2 Re × ||W||=1 × two sites`) is reported only as a variant labelled conservative.
- **Straddling.** Only supports strictly containing `R` pair with an outside excitation, of amplitude at most `t` by (F14). There are 6 such first-order faces, `6=16-10`, with owner sets `{0,e_x,e_z}` (2) and `{0,e_y,e_z}` (4). The 72 straddling faces split as 42+30 by the number of outside sites and as 66+6 by `|I cap R|`, and the 66 meeting `R` once contribute exactly 0.
- **Two-creation.** For disjoint pairs `I ni 0`, `J ni e_z`, the bound is `2·(1/2)·A_0 A_{e_z}` with `A_0=sum_{I ni 0, e_z notin I}||c_I|| <= 33a+rho`, where `33=49-16`, and the same for `A_{e_z}`.
- **Density.** `|<delta,W delta>| <= ||delta||^2`, which is `Tr_out|delta><delta|`, so the term is at most `e^2 <= eps^2`.
- **Normalization.** It enters only through the leading term, `(tau/144)(1-1/(1+e^2))`. It is **third order**, and it is still charged.
- **Arithmetic.** Not applicable as a numeric cost: exact Fractions throughout, and triangle bounds instead of square roots.

The pins are to the contract enumeration: 15 owner sets with multiplicities `{1x5,2x3,3x2,4x3,10x2}` (sum 49), 82 faces meeting `R`, 16 touching both factors. These are derived from the I1 table parsed from its snapshot, and every support is re-derived from I1.4. A fine-lattice brute force and the selection note's 49/15/82/10/72 confirm them. The grouped norm `sum sqrt(n_M)·a <= 0.17383·|tau|` is recorded but not used in the headline.

**Uniformity.** Every constant depends only on `t`, `rho`, `eps` and bulk counts. Finite-box counts are at most bulk counts, and `W`'s star is retained for `N>=2`. So (F15) holds for every centered box at every cutoff `L>=24`, where `c^(1)_L=c^(1)`. It passes to the untruncated ground vector (AV1 §7) and to every AQ subsequential limit, since `W` is local on `R`. The `-tau` value is the flip image of the `+tau` value, not a second confirmation.

### 5.3 Exact values at `tau=±10^-8`

| term | tier | exact value at `tau` | `/tau^2` (preview) | order |
|---|---|---|---|---|
| am2_remainder | exact | `3773/11248891200000000` | `3354.10835869` | 2 |
| two_creation | exact | `166184094520081/31634388307359360000000000000000` | `0.0525327352` | 2 |
| straddling | exact | `229849739/161968068133679923200000000` | `0.0141910527` | 2 |
| density | exact | `1991092904511417843291841/42981220507576535941210238266176140476416` | `0.463247177` | 2 |
| normalization_order | exact | (in `results.json`) | `3.217e-11` | 3 |
| **K_2^+ (exact)** | exact | `81104877995836618199905135109761286809699489/24176936535511801466930759024724079017984` | **`3354.63832966`** | |
| am2_remainder | crude | `2849/4882812500000` | `5834752` | 2 |
| two_creation | crude | `1369/39062500000000` | `350464` | 2 |
| straddling | crude | `1369/39062500000000` | `350464` | 2 |
| density | crude | `213907516326874161/1525878906250000000000000000` | `1401864.299` | 2 |
| normalization_order | crude | (in `results.json`) | `9.735e-5` | 3 |
| **K_2 (crude)** | crude | `1937877026146766159414097129/244140625000000000000` | **`7937544.29909`** | |

- **Crude tier.** It uses `t <= J G(R) = 37/6250000` for every term. No first-order enumeration enters, so there is no tier mixing.
- **Tier mixing.** Any `K_2` whose terms carry different tier labels is rejected, as is `t=t_1` without the self-consistent remainder.
- **Labelled variants (exact tier):**
  - the sharper directed AM2 form `G(t)-16<=288t/(1-8t)`: `2744.88122620`;
  - the conservative overlap multiplier 4: `13416.9634057`;
  - unpinned `t`-bounds: `3354.80322946`.
- **Scaling.** Under `tau -> tau/100`, each second-order term scales by a factor in `[9900,10100]`, the normalization term by `≈1.000195×10^6`, and the first-order coefficient by exactly 100.

## 6. Feasibility and the AW2 rule (item 5)

\[
 K_2^+\tau=\tfrac{81104877995836618199905135109761286809699489}{2417693653551180146693075902472407901798400000000}\approx3.3546\times10^{-5}\le\tfrac1{288},\qquad
 \frac{1}{144K_2^+\tau}\approx207.010\ge2 .
 \tag{HNM-AW1-F16}
\]

The rule is read from the contract: the largest element of `{10^-8, 10^-9, ...}` with `K_2^+ tau <= 1/288`. It gives **`tau_AW2 = 10^-8`**.

The crude tier gives `K_2 tau ≈ 0.0794 > 1/288`, so it fails at the cap and is retained. Its rule value `10^-10` is information only and is never substituted.

AV1 is compatible: `D_ii ≈ 1.3612×10^-8 >= tau/144 + K_2^+ tau^2`, a ratio of about 196 to `tau/144`.

**No enclosure of `omega(W)` is admitted in this loop.** The feasibility Boolean is not a sign certificate; AW2 instantiates the enclosure.

## 7. Checker and controls (items 6–7)

`check.py --output <absolute fresh dir>` uses the standard library only.
- It verifies the contract sha256 and reads the target `1/288`, the rule, the flip set, the reference values `0, 1/4, 0, 1/8` and every candidate count from the contract. The AV1 constants and `D_ii` come from the hash-bound AV1 snapshots, and the I1 table from its snapshot.
- It records its own sha256 before any evaluation.
- It writes `results.json` (41 checks, each listing the mutations it rejected) and `source-manifest.json`.

The 30 contract controls, each with at least one explicit damaging mutation:

| control | damaging mutations rejected |
|---|---|
| `haar_parity_exact` | odd tensor power given an invariant |
| `first_order_shift_of_C_vanishes` | parity applied to the uncentered mean; nonzero-triple reference |
| `degenerate_multiplet_first_order` | full-space multiplet claimed unsplit; identity component at 24 |
| `wilson_mean_first_order_coefficient` | `tau/72`; `tau/288`; the `+2<W,L_0>` display |
| `wrong_face_control` | all ten inside faces counted |
| `wilson_face_separated` | 21 classes merged; `W` excluded |
| `sign_convention_fixture` | display sign against the fixture |
| `sign_flip_tau` | sign-blind `abs(tau)` formula |
| `second_order_remainder_itemized` | a term set to zero; a term missing |
| `wilson_overlap_single_component` | factor 4 unlabelled; multiplier 1/2 |
| `tier_mixing_rejected` | crude straddling in the exact sum; `t=t_1`; rule fed the crude constant |
| `aw2_coupling_rule_prefrozen` | not the largest decade; off-grid value; crude constant |
| `flip_set_odd_intersection` | `E` minus one link; odd periodic side; centre gauge transformation; spin-1 term |
| `flip_breaks_at_nonzero_kappa` | tau-antisymmetry claimed at a nonzero triple |
| `flip_nonzero_kappa_positive_demonstration` | selected coefficient claimed invariant; selected face treated as `E`-even |
| `flip_no_third_order_claim` | `O(tau^3)` from oddness |
| `static_not_dynamic_effect` | dynamical or mass-gap relabel |
| `missing_incoming_stars` | one-star `J=7|tau|`; two-anchor orthant count |
| `full_original_wilson_cover` | the four drawn links as the cover |
| `wrong_delta_alpha_hbar_clock` | `tau/1152`; `tau/18`; eightfold clock (fixture `alpha=5`, `hbar=7`) |
| `vector_versus_scalar_centering` | scalar subtraction as vector centring |
| `first_order_mean_charged` | zero mean at first order |
| `tau_scaling_exponent` | second-order term relabelled first order; square root relabelled linear |
| `changed_model_relabelled` | `tau=10^-14`; nonzero triple; strip reference; finite-graph id; finite-volume provenance |
| `insufficient_verdict_retained` | crude tier reported feasible; crude retuned to a smaller `tau` under the cap label |
| `exact_arithmetic_admission` | float, bool, NaN, zero denominator |
| `root_n_misuse` | root sum of squares; division by `sqrt(N)`; division by 64 |
| `reverse_premise_isolation` | reverse reads the triage; reverse reads forward AW1 |
| `no_priority_or_continuum_claim` | continuum, priority or shift flag set true |
| `coherent_evidence_tampering` | control Boolean, snapshot, `K_2`, `tau_AW2`, first-order value or third-order flag changed with the hash rebound |

The eleven non-control checks are:
- `contract_binding` and `av1_premise_binding`;
- `face_enumeration_derived`;
- `flip_operator_fixtures`;
- `remark_selected_even_flip_set` (a remark only);
- `flip_covariance_and_aq_passage`;
- `orientation_invariance`;
- `k2_exact_tier` and `k2_crude_tier`;
- `omega_W2_second_order_bound`;
- `av1_compatibility`.

The claim flags are:
- `continuum_claim:false`, `uniform_wilson_claim:false`, `resolved_interaction_shift:false`, `scientific_priority_verified:false`;
- `first_order_parity_claim:true`, because item 1 is complete with the `C(s)` constant explicitly unbounded;
- `flip_lemma_claim:true`;
- `third_order_remainder_claim:false`, `omega_W_enclosure_admitted:false`, `sign_of_omega_W_admitted:false`, `euclidean_node_certified:false`.

## 8. Limitations and exclusions

The contract's claim exclusions, verbatim:
- an admitted enclosure of omega(W) (AW2);
- a dynamical or mass-gap correction (static_not_dynamic);
- any third-order remainder from oddness alone;
- uniform Wilson magnetic theory;
- AQ uniqueness or a rate in N;
- continuum construction;
- scientific priority.

The preregistration exclusions also apply:
- a free reference inside an enclosure means no interaction claim; this is why the `omega(W^2)` bound resolves nothing;
- no uniqueness, whole-sequence convergence or rate in `N`;
- no continuum or weak coupling;
- no transfer from a finite graph (the fixtures are audits);
- no relabelling of the static shift as dynamical;
- scientific priority is unverified.

**Incomplete or conditional, stated honestly:**
1. **`C(s)` and `c(theta)`.** The first-order vanishing is proved box by box, as a Taylor statement via Kato analyticity. The second-order constant is not proved uniform in `N`, so no AQ-level `O(tau^2)` bound for `C(s)` is claimed. In AQ only the evenness from the flip lemma is available, for paired states.
2. **The multiplet.** Zero first-order splitting is proved for the gauge-invariant energy-24 multiplet, not for the full-space one.
3. **The flip identity at `kappa!=0`.** It rests on the inherited form of the strip operator. The AQ passage for `C(s)` rests on AQ1's inherited dynamics, the norm limit of finite-volume evolutions, which I do not re-prove.
4. **`K_2^+` is conservative.** The AM2 generic majorant dominates it (99.98%). The parity grading would kill the second-order direct overlap `<W Omega_R,(c-c^(1))_R>` at order `tau^2`, but using that would need a separate third-order bound, and it is not used or claimed.
5. **Inherited without re-proof.** AM2's fixed point, majorant and gaps; AV1's product-ordering split, orthogonality and cutoff-vector convergence; AQ1's compactness and dynamics; I1's dictionary.
6. **Fixtures are exact finite audits:** one plaquette, one link, quaternion holonomies, the `kappa` compression and the qubit creation fixture. They are not proofs of the infinite-volume statements.
7. **Outside this producer.** The reverse route and skeptical review.
8. **Undeclared reads, disclosed above:** the tools README and `freeze.py`, AV1 forward `check.py` for code style, and the two assistant scripts as named tooling. None carries premise weight.
9. **The remark `E*`** in §3.3 is an unreviewed observation outside the model.

**Methodological lenses.**
- **Newton, analysis before synthesis.** The representation content of every first-order term is analysed before any budget is written. The first-order `C(s)` coefficient is shown to vanish and is not assumed.
- **Tesla, complete accounting.** Every channel is charged with its tier named: the source (all omitted faces and all supports meeting `R`), the load (the 48-link cover, `||W Omega_R||`), the normalization and the pairing with outside excitations.

These are modern uses of the snapshotted skills. No historical figure endorses anything here, and no historical or occult material supplies a premise.

## 9. Reproduction

```bash
python3 -B research/round32/forward/aw1/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/forward/aw1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/forward/aw1
```
