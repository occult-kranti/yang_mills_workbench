# Hruday uniform-model window certificate for C(1) at the original cap — AX2 forward (single producer)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production under the frozen AX2 contract (`research/round32/contracts/ax2.json`, sha256 `da72afe377d7601e6b6ec3835ab69d05813cb26c4b46f67485a4d8e0c055992b`). AX2 is a **single-direction** loop: this is the only producer. Admission also requires the skeptic's independent replay from the contract alone, which is being written separately. No file `research/round32/skeptic/ax2*` was read. This is correlated model-agent work, not independent human review, and nothing here is a second route.

**What this producer read.**
- **The contract snapshot first.** After that, only files under `inputs/`:
  - **read in full:** AGENTS.md; `selection-ax2.md`; the AX1 gate (all fields); the AV2 gate (all fields except `bindings`, which the checker reads for hash comparison only); the AV2 contract; the AX1 contract (all fields except the `shared_premises` list); the AV2 forward report; the AV2 forward calculator; the AX1 forward report; `skeptic/ax1.md`; `skeptic/av2.md`; the AT4 forward report; the complete-residual reference note.
  - **read in part:** the AX1 reverse report (its first 60 lines, plus three one-line hits of a keyword search for "AX2" across `inputs/`); the AQ1 forward report (first 40 lines); the paired-physics SKILL (first 80 lines); the Newton and Tesla SKILL files (first 40 lines each); the historical-panel SKILL (first 30 lines).
  - **not opened:** the AM2 forward and reverse reports, `skeptic/am2.md`, the AM2 gate, the AQ2 and I1 reports, the AV2 reverse report, and the Newton, Tesla and historical-panel reference notes. The checker verifies all of their hashes.
- **Outside `inputs/`, for protocol and code style only:** `research/round32/tools/README.md`, `research/round32/tools/freeze.py` and `research/round32/forward/av2/check.py`. None of these carries premise weight.
- **Incidental exposures, disclosed.** These are directory and log listings only:
  - `ls research/round32/` and `ls research/round32/forward/`;
  - `git status --short`, which showed nothing;
  - `git log --oneline | head -5`, whose newest subject names an "AY1 draft";
  - the first ten entries of `/tmp/claude-0/`, which were the names of other agents' AV1/AV2 run folders.

  I opened no file in any other scratch folder.
- **My scratch.** It is in `/tmp/claude-0/ax2-private/`: development runs, and a private source-edit mutation harness that works on copies. The official run went to `/tmp/claude-0/ax2-run`. The Claude harness saved copies of three of my own reads (the AV2 and AX1 forward reports and part of the AV2 check.py) to its tool-results cache, and I re-read those copies. They are my own reads, not other agents' files.

**Established mathematics, credited as such:**
- the Fourier inversion theorem for `L^1` functions with `L^1` transforms, and Fubini's theorem;
- Laplace transforms of polynomial exponentials;
- relative-unitary (bounded-perturbation) Duhamel estimates and trace duality;
- Haar and Peter–Weyl character orthogonality, and Machin's formula.

The window lemma and its constants are **admitted AV2 results**, applied here verbatim. The route-B constants are **admitted AX1 results**. The contribution of this loop is only their combination for the named model, with exact constants. HNM labels are project aliases. Scientific priority is unverified.

## Verdict (forward, single producer)

**Model and label.** The model is uniform Kogut–Susskind SU(2) at fixed spacing and strong bare coupling (`g^4=9.6x10^9`), handled by route B of AX1. The cap is `tau=+10^-8` and the node is `s=1`. The observable is the original xz Wilson loop `W` with cover `R={0,e_z}`, taken in every AQ1 subsequential state of the centered whole-star-plus-single-group construction, each state separately.

**Exact datum.** It is the midpoint of the directed enclosure of `e^{-3}/4`, identical to AV2's datum, because the reference is unchanged in route B:

\[
 d=\frac{497870683678639429793424156500617766317}{4\cdot10^{40}}=0.012446767091965985744835603912515444157925 .
\]

**Certified absolute error.**

\[
 |C_\tau(1)-d|\le r,\qquad r\le 1.91229880800\times10^{-7}\quad(\text{outward on the }10^{-40}\text{ grid: }r\le\tfrac{1912298807996871790146581299723633}{10^{40}}).
\]

This meets the unchanged `10^-6` target: the margin `10^-6/r` is at least **5.22930**. The actual centered correlation therefore lies in

\[
 C_\tau(1)\in[0.012446575862085186,\ 0.012446958321846786]
\]

(lower endpoint rounded down, upper rounded up; exact rationals in `output/results.json`).

**What does not change the result:**
- The value at `tau=-10^-8` is the **U_E mirror**: it has no real `g`, and it is a replay of the same `|tau|` formula, not a second confirmation.
- The free value `e^{-3}/4` lies inside the interval. The sub-label is **`reference_unresolved`**, and no interaction shift, sign or coefficient of `C(s)` is claimed.
- No uniform Wilson-mean sign certificate or uniform-model `K_2` is attached (loop-2 veto).

**Proposed outcome:** `accepted_within_scope` against the contract clause "`E'<=10^-6` with the admitted AX1 exact tier". This is proposed only; **admission requires the skeptic's independent replay from the contract alone.**
- The checker runs **52 exact checks**.
- All **25 contract controls** reject explicit damaging mutations through exceptions: 98 rejections in the control checks, plus 31 calculator-domain rejections.
- The `-B` and `-B -O` outputs are byte-identical.

## 1. Model, dictionary and label (item 3)

The model is the AX1-admitted uniform Hamiltonian:

\[
 H_{KS}=\alpha\sum_eC_e+\lambda\sum_p(1-W_p),\quad \nu=\lambda=\frac{\alpha\tau}{24}\ \text{for every face (selected faces included)},\quad
 \tau=\frac{96}{g^4},\quad g^4\big|_{\tau=10^{-8}}=9.6\times10^{9}.
 \tag{HNM-AX2-F01}
\]

Route B splits it into three pieces:
- the tau-independent on-site operator `h_b=8 sum_e C_e>=6Q_b`, with the Haar vacuum;
- whole stars `phi_b` (21 omitted faces each, norm `7|tau|`);
- one single-factor group per factor, `psi_b=-(tau/3)(W_g1+W_g2+W_g3)`, holding the three selected xy faces (support `{b}`, norm at most `|tau|`).

The re-frozen `J_0'=29/10^8` is used. It satisfies `1073/175000000<1/64` and `319/1562500<1` (control `j0_resolution_declared`). It supplies the unique finite-volume ground, the gap `alpha/16`, and the uniform AQ1 construction with its nonnegative generator.

**Label (exported verbatim):** `uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling (g^4=9.6x10^9)`. The checker scans the label, the contract model and the verdict string, and rejects any weak-coupling or continuum wording. `tau<0` has no real `g`; it is the `U_E` image of `+|tau|`. The flag `uniform_wilson_claim:true` means **only** that the model is the uniform fixed-spacing model as labelled.

## 2. The lemma transfer (item 1)

**Frozen AV2 conventions, verbatim.** They are parsed from the hash-bound AV2 contract and gate and compared:

\[
 c(\theta)=\langle\chi,e^{i\theta G}\chi\rangle,\quad \hat g(\theta)=\frac1{2\pi}\int g(x)e^{-i\theta x}dx,\quad
 g(x)=\begin{cases}e^{-sx},&x\ge0\\ e^{sx}(1-2sx+2s^2x^2),&x<0\end{cases},\quad
 \hat g=\frac{4s^3}{\pi(s-i\theta)^3(s+i\theta)} .
 \tag{HNM-AX2-F02}
\]

Here `chi=(pi(W)-omega(W))Omega` and `G=H_phys/alpha`. The AV2 lemma needs four things:
1. `G>=0`, so that the centered spectral measure `eta` lives on `[0,inf)`;
2. `eta` finite;
3. `g in L^1 ∩ C_0` with `ghat in L^1`, which gives inversion at every `x`;
4. Fubini.

The last two depend on `g` only. The first two hold for the uniform route-B state, because AQ1's nonnegativity and GNS construction re-apply verbatim with the route-B constants (AX1 gate item 3). Hence, verbatim,

\[
 C(s)=\int_{\mathbb R}\hat g(\theta)\,c(\theta)\,d\theta,\qquad M_0=\|\hat g\|_1=2,\quad M_1=\int|\theta||\hat g|=\frac{4s}{\pi},\quad M_2=2s^2 .
 \tag{HNM-AX2-F03}
\]

The checker re-audits the constants in exact arithmetic:
- C² matching, with the third-derivative jump `-8s^3`;
- the half-line identity `2 pi ghat a^3b=8s^3` in Gaussian rationals;
- the modulus `(4s^3/pi)(s^2+theta^2)^-2`;
- exact antiderivatives giving `M_0=2`, `M_1=4s/pi`, `M_2=2s^2` and `∫ghat=1`.

The AQ2 gap is not used.

**Transfer checklist.** It is exported as `lemma_transfer` in `results.json`.

| hypothesis or ingredient | uniform route-B status |
|---|---|
| window, conventions, `M_0`, `M_1`, `M_2` | verbatim (AV2) |
| `G>=0`, finite `eta`, inversion, Fubini | verbatim (AQ1 nonnegativity re-applies, AX1 gate item 3) |
| reference `c_0(theta)=e^{3i theta}/4` | verbatim value (Section 3) |
| real-time slope | **new constant** `k'=51|tau|/4` (Section 4) |
| state term, mean square | **new constant** `D'` bound by the AX1 gate (Section 5) |
| passage to every AQ1 subsequential limit | verbatim with route-B constants (AX1 gate items 3 and 6) |
| AQ2 gap | not used |

The transfer holds, so the acceptance clause "insufficient: the transfer of the window lemma fails" is not triggered.

## 3. The reference is unchanged in route B (item 2)

In route B the reference state on `R` is the Haar product `P_R`, and the on-site generator is the tau-independent Casimir sum. Both single-factor groups meeting `R` (`psi_0` and `psi_{e_z}`, supports inside `R`) are put in `B_N` together with the seven stars. So `A_N` evolves `W` by the free Casimir generator on `R`, where each of the four links carries `3/4`:

\[
 G_{0,R}(W1_R)=3W1_R,\qquad \omega_0(W)=0,\qquad \omega_0(W^2)=\tfrac14,\qquad c_0(\theta)=\tfrac14e^{3i\theta},\qquad C_0(s)=\tfrac14e^{-3s}.
 \tag{HNM-AX2-F04}
\]

**The free z link.** `W` has two z links, `((0,0,0),z)` and `((1,0,0),z)`. The selected faces are xy faces and contain no z link. In `W·prod W_g` over any subset of the six selected faces of `R`, each z link of `W` therefore occurs exactly once. So the Haar mean vanishes by the AW1 grading: a Haar integral of spin-1/2 matrix elements is zero unless every link occurs an even number of times. The checker verifies this for all 64 subsets. Two selected faces share an x link with `W` (`(0,x)` and `(e_z,x)`). They enter only through `B_N`, never through the reference. As a check, the exact datum equals the AV2 gate datum rational for rational.

## 4. Real-time comparison with the uniform slope (item 1; controls `selected_incidence_count`, `local_not_extensive_duhamel`)

The route-B groups are re-derived by a fine-lattice brute force over 80 anchors. Each anchored face falls in exactly one group, a 21-face star or a 3-face single group, and its support lies inside the group's support. The groups meeting `R` are:
- **seven stars**, anchors `R-S={0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y}`, meeting `R` in 21, 21, 16, 8, 8, 4 and 4 faces;
- **two single-factor groups**, `{0}` and `{e_z}`, with 3 selected faces each.

Totals: 153 faces charged, 88 meeting `R` (82 omitted plus 6 selected) and 16 inside `R`, equal to the AX1 gate's itemized incidence. In `G=H/alpha` units:

\[
 G_N=A_N+B_N,\qquad \|B_N\|\le7\cdot\frac{7|\tau|}{8}+2\cdot\frac{|\tau|}{8}=\frac{51|\tau|}{8},\qquad
 \|\alpha^N_\theta(W)-\alpha^0_\theta(W)\|\le2|\theta|\|B_N\|\le k'|\theta|,\quad k'=\frac{51|\tau|}{4}.
 \tag{HNM-AX2-F05}
\]

The estimate is local. For `N=2,3,4` the box `Lambda_N` has exactly 7 stars and 2 single groups meeting `R`; `N=1` has only 4 stars. The damaging mutations are:
- **the extensive norm** (`(2N)^3` stars and `(2N+1)^3` groups), rejected because the slope would depend on the box;
- **the seven-star-only slope** `49|tau|/4`, rejected as a changed model: it drops the two groups, and it is AV2's zero-selected slope;
- **a dropped conjugation factor 2**, rejected.

AQ1's norm dynamics on compact `theta` intervals re-applies with `||Phi'||_F<=2349|tau|` (AX1 gate item 3), so (F05) holds for the actual AQ evolution at every real `theta`.

## 5. The state premise `D'` from the AX1 gate (controls `av1_tier_bound`, `tier_mixing_rejected`)

\[
 \|\rho_R-P_R\|_1\le D'=\frac{2425369125199104794263242601250}{167893028420061547330293754713793182097}\approx1.44459192142\times10^{-8}.
 \tag{HNM-AX2-F06}
\]

**How `D'` is bound.** The checker reads `D'` from the AX1 gate decision. The gate snapshot's sha256 is pinned (`1b8fb152…d177`). The value must equal all of the following:
- the contract parameter;
- the gate's accepted text;
- the calculator's pinned constant;
- the gate formula, recomputed at the cap: `J'=29|tau|`, `t_1'=52|tau|/144`, `T'=t_1'/(1-352J')=13/3599632512`, `eps=2T'+T'^2`, `D'=2eps(1+eps)/(1+eps^2)`.

**Rejected alternatives.** Each of these is a rejected damaging mutation:
- the AX1 reverse R-refinement (`~1.22237e-8`);
- the AX1 target `4/10^7`;
- the AV1 zero-selected `D` (`~1.36125e-8`);
- the mis-rounded contract note `4.19e-7`;
- tier (i) (`~2.45261e-5`);
- a recomputation with the pair term `T'^2` dropped (`1.4445919188e-8`);
- a recomputation with the density form replaced by `2eps` (`1.4445919110e-8`);
- a supplied `D` or an unadmitted tier in the calculator.

This closes the AX1 gate's N5 finding for AX2: a smaller recomputed value cannot run silently. Tier mixing is also rejected: a tier-(i) mean square, a reverse-refinement state term, an exact first-order `c^(1)` without the AM2 remainder, and a zero-selected state term with the uniform slope.

**Comparison.** By trace duality with the non-effect `W alpha^0_theta(W)` (no `D'/2`, control `state_term_not_effect`), and with `m^2<=D'^2`:

\[
 |c(\theta)-c_0(\theta)|\le k'|\theta|+D'+m^2\le k'|\theta|+D'+D'^2\qquad(\theta\in\mathbb R).
 \tag{HNM-AX2-F07}
\]

The finite-box first-order mean `omega(W)^(1)=+tau/144` is nonzero in the uniform model. It is **not** a uniform bound, because no uniform `K_2` is admitted. Replacing `m^2<=D'^2` by `(tau/144)^2` is therefore a rejected mutation (`first_order_mean_charged`).

## 6. Radius, datum, interval and Boolean (items 1–2)

Integrate (F07) against `|ghat|` over every real `theta`; there is no cutoff and no tail:

\[
 \Bigl|C(s)-\tfrac14e^{-3s}\Bigr|\le E'(s)=M_0(D'+D'^2)+k'M_1=2(D'+D'^2)+\frac{51|\tau|s}{\pi}.
 \tag{HNM-AX2-F08}
\]

Enclose `e^{-3}/4` as `[f^-,f^+]`, using `P_41<=e^{-z}<=P_40` on `[0,1/2]`, three halvings and outward squaring to `10^-40`. Then set

\[
 d=\frac{f^-+f^+}{2},\qquad r=E'^{+}(1)+\frac{f^+-f^-}{2},\qquad C_\tau(1)\in[d-r,\,d+r].
 \tag{HNM-AX2-F09}
\]

Here `E'^+` uses the Machin lower bound `pi^-` in `k'M_1`.

**Radius table** at `tau=+10^-8`, `s=1`, `k'=51/400000000`. Decimals are rounded up.

| term (preregistered name) | exact rational | outward decimal |
|---|---|---:|
| `state` = `M_0 D'` | `4850738250398209588526485202500/167893028420061547330293754713793182097` | `2.88918384286e-8` |
| `mean_square` = `M_0 D'^2` | exact in `results.json` | `4.17369163892e-16` |
| `kernel_dynamics` = `k'M_1^+` = `51\|tau\|/pi^-` | `425000000000000000000000000000000/2617993877991494365385536152732919070163` | `1.62338041954e-7` |
| `arithmetic` (half-width of the `e^{-3}/4` enclosure) | `1/(4·10^40)` | `2.5e-41` |
| **complete radius `r`** | exact in `results.json`; `<=1912298807996871790146581299723633/10^40` | **`1.91229880800e-7`** |

**Interval and Boolean.**
- **Interval:** `[0.012446575862085186, 0.012446958321846786]`, of width `2r`. The free enclosure (width `5·10^-41`) lies inside it.
- **Boolean:** `r<=1/1000000` is `true`, with margin `>=5.22930`.
- **Contract preview:** "~1.91e-7" agrees to within `10^-9`.

**Relation to AV2.** The uniform radius exceeds AV2's common bound `1.83196750341e-7` by at least `8.03e-9`. The source is the larger `D'` and the two extra groups in `k'`. It is a different model, not a refinement.

**Mirror replay** (item 1).

\[
 U_EH_N(\tau)U_E^*=H_N(-\tau)\ \Rightarrow\ C_{N,-\tau}=C_{N,\tau},\ S(-\tau)=S(\tau)\circ\alpha_E\ \text{(whole sets)};\quad
 \texttt{certify(tau=-1/10^8)}\ \text{returns the identical } d,\,r .
 \tag{HNM-AX2-F10}
\]

This is a replay at the `U_E` image, not a second observation. Every term depends only on `|tau|`.

## 7. Retained failures at the uniform slope (controls `insufficient_verdict_retained`)

All values are at unchanged `tau=10^-8` and `s=1`, with directed `pi`, `log` and `sqrt`.

**AT4-type Poisson certificate at `L=10^4`.** The AT4 F16 formula is

\[
 D+D^2+\frac{ks}{\pi}\log\Bigl(1+\frac{L^2}{s^2}\Bigr)+\Bigl(\frac12+\frac D2\Bigr)\frac{2s}{\pi L}.
 \tag{HNM-AX2-F11}
\]

With AT4's own inputs it reproduces the frozen AT4 decimal `0.000841518704386267` to `10^-15`. With the uniform inputs (the route-B square-root control `D=2sqrt(17|tau|)` and `k'=51|tau|/4`), it lies in `[8.5790595e-4, 8.5790596e-4]`. **Insufficient; retained.**

**Poisson floor at the uniform slope.** For every `L>0`,

\[
 \frac{k's}{\pi}\log\Bigl(1+\frac{L^2}{s^2}\Bigr)+\frac{s}{\pi L}\ \ge\ \frac{2k's}{\pi}\Bigl(1+\log\frac{1}{2k's}\Bigr),
 \tag{HNM-AX2-F12}
\]

which is minimized at `L=1/(2k')`.
- **The floor itself:** enclosed in `[1.313477283e-6, 1.313477284e-6]` (evaluated at `L=3921569`). No `L` meets `10^-6`, even with `D->0`.
- **With `D'` added:** it is at least `1.3279232e-6`.
- **The first moment:** the Poisson kernel's truncated absolute first moment `(s/pi)log(1+L^2/s^2)` is at least `46.907878` at `L=10^32`, so `k'` times it alone exceeds `10^-6`. The window's `M_1=4s/pi` is finite.
- **The rejected retuning:** at `tau=3739/500000000000` the D->0 floor would meet the target (upper value `9.9985841e-7`). Retuning to that coupling after the outcome is rejected.

**Insufficient; retained.**

**Tier (i) window.** With `D'_i=23002790096235779074916932482/937890625141038667264537458466241` (~2.45261e-5; recomputed from `t<=J'G(R)=1073/175000000` and equal to the AX1 forward F18), the radius is at least `4.921572155e-5`. This is a **limited-tier value, retained**; it is not the bound premise.

## 8. Crossover for the uniform model

`E'(s)=2(D'+D'^2)+(51|tau|/pi)s` is linear in `s` (control `window_linear_in_s`). Solving `E'(s*)=10^-6` with `pi^∓` gives

\[
 s^*\in[5.9820122841,\ 5.9820122842],\qquad E'^{+}(s^{*-})=E'^{-}(s^{*+})=10^{-6}\ \text{exactly}.
 \tag{HNM-AX2-F13}
\]

This lies below AV2's `[6.236863446, 6.236863447]`. For orientation, the analytic radius is:

| `s` | analytic radius |
|---|---:|
| `1/2` | `1.1006086e-7` |
| `2` | `3.5356793e-7` |
| `5` | `8.4058205e-7` |
| `128` | at least `2.08081e-5` |

**Only `s=1` is certified.** The preregistration forbids post-hoc nodes; the mutation "node `s=5` with the `s=1` radius" is rejected. `grid_claim` is false, and there is no `[0,128]` claim.

## 9. What is and is not claimed

**Claimed.** Take the uniform Kogut–Susskind SU(2) model at fixed spacing and strong bare coupling (`g^4=9.6x10^9`), route B, `tau=+10^-8` (with `-10^-8` as the U_E mirror replay), and the node `s=1`. For every AQ1 subsequential state of the centered construction, each separately, the centered Euclidean Wilson correlation satisfies `|C(1)-d|<=r` with `r<=1.9123e-7<=10^-6`. The flag `euclidean_node_certified` is true.

**Not claimed:**
- no resolved interaction shift: the free value is inside (`reference_unresolved`);
- no sign or coefficient of `C(s)`;
- no uniform Wilson-mean sign certificate (loop-2 veto);
- no uniform `K_2` and no uniform `omega(W^2)` constant;
- no AQ uniqueness, whole-sequence convergence or rate in `N`;
- no grid and no node other than `s=1`;
- no transfer from a finite graph;
- no weak-coupling or continuum statement;
- no scientific priority.

**Claim flags:**

| flag | value |
|---|---|
| `continuum_claim` | `false` |
| `uniform_wilson_claim` | `true` (scope string exported) |
| `weak_coupling_claim` | `false` |
| `resolved_interaction_shift` | `false` |
| `scientific_priority_verified` | `false` |
| `euclidean_node_certified` | `true` |
| `grid_claim` | `false` |
| `producers` | `["forward"]` |
| `single_direction_independent_replay_required` | `true` |

Also false: `wilson_mean_sign_certified`, `k2_uniform_claimed`, `state_uniqueness_claim`, `independent_review_claimed` and `mirror_is_second_confirmation`.

## 10. Calculator (item 5)

`calculator.py` exports `certify(...)`, restricted to the proved uniform domain.
- **Inputs.** Exact inputs only: integers, `Fraction`s, exact decimal strings and `p/q` strings. Floats, Booleans, NaN, Infinity, empty strings, zero denominators and other objects are rejected.
- **Domain:**
  - `model='uniform_KS_routeB'` only;
  - the selected triple must be uniform, `('tau/24',)*3` or the rational `tau/24` — the zero triple (AV2's model) and non-uniform triples are rejected;
  - `|tau|<=10^-8` at either sign;
  - `s>0`, target `>0`, and positive `alpha`, `hbar`, `E_star` and lattice spacing.
- **State bound.** `D'` is **not an input**:
  - at the cap it is the AX1 gate rational, pinned, so a formula edit such as a dropped pair term aborts;
  - below the cap it is the gate's admitted tier-(ii) `|tau|`-form, which is increasing and never above the gate value;
  - `state_tier` must be `ax1_forward_tier_ii`.
- **Kernel.** `window` must be `C2`; C¹ and Poisson are rejected.
- **Fixed design.** `fixed_design=True` enforces `|tau|=10^-8`, `s=1` and target `10^-6`. The negative sign is allowed and flagged `mirrored_coupling_replay` with the U_E note.
- **Returns:**
  - the datum, radius, outward `10^-40` radius, interval and the four itemized costs;
  - `D'`, `k'`, `M_0`, `M_1^±`, `M_2` and the incidence counts;
  - the label and `g^4`;
  - `physical_Euclidean_time=hbar s/alpha`;
  - the sub-label and the claim flags.

```python
from calculator import certify
r = certify(fixed_design=True)                       # tau=+10^-8, s=1: r['target_met'] is True
m = certify(tau='-1/100000000', fixed_design=True)   # U_E mirror replay, same radius
q = certify(s='2')                                   # reusable: analytic radius at s=2 (not a certified node of AX2)
```

## 11. Controls (item 4; 52 checks)

Every contract control is an exception-raising damaging mutation, recorded under `rejected_mutations` in its check. The run aborts if any of the 25 ids lacks a check or a rejection, and no check uses `assert`.
- **`kernel_identity_on_support`:** a symmetric window and a window matched only above the AQ2 gap are rejected.
- **`kernel_negative_atom_misread`:** `g(-1)=5/e<e`; a negative atom is rejected.
- **`kernel_l1_and_first_moment`:** a positive mass-one kernel, `∫ghat=1` used as the `L^1` norm, and `M_1` without `s` are rejected.
- **`window_linear_in_s`:** exact `E'(s)=A'+(51|tau|/pi)s` at `s=1/2,1,2,5`; the node `s=5` with the `s=1` radius and a dropped dynamics term are rejected.
- **`local_not_extensive_duhamel`:** the extensive norm, the seven-star-only slope (changed model) and a dropped factor 2 are rejected.
- **`uniform_label_strong_coupling`:** rejected are a weak-coupling label, continuum wording in the verdict, a label missing "fixed spacing" or "strong bare coupling", a negative `tau` read as a real `g`, and `tau` read in `delta` units.
- **`selected_incidence_count`:** rejected are groups forgotten (`49/8`), faces counted as groups (`55/8`), single groups at the seven star anchors (`56/8`), and the selected coefficient read in `delta` units.
- **`j0_resolution_declared`:** `exp(1/8)<8/7`, `G(R)<148/7` and `G'(R)<352` are checked. The old `J_0` at the cap, a missing resolution, and R2 under the cap label are rejected.
- **`av1_tier_bound`:** 10 rejections (Section 5).
- **`state_term_not_effect`:** the `D'/2` state term is rejected.
- **`window_fourier_sign_convention`:** `theta->-theta` (giving `25e^{-3}/4`) is rejected.
- **`tier_mixing_rejected`:** 4 rejections (Section 5).
- **`single_producer_declared`:** rejected are a claimed reverse route, a dropped replay requirement, self-review called independent, the mirror as a second confirmation, and a verdict without the pending replay.
- **`missing_incoming_stars`:** the orthant count 2 and the `N=1` count 4 are rejected.
- **`full_original_wilson_cover`:** the four drawn links are rejected. The cover has 48 links and 36 endpoints, and the 6 selected faces lie inside it.
- **`wrong_delta_alpha_hbar_clock`:** exponent 24 with `s` and normalized group norms in the `G` clock are rejected. The non-unit fixture `alpha=5`, `hbar=7` gives physical time `7/5`.
- **`vector_versus_scalar_centering`:** scalar subtraction (`-51/10000`) used as vector centering is rejected.
- **`first_order_mean_charged`:** a zero mean, and the finite-box `tau/144` used as a uniform bound, are rejected.
- **`tau_scaling_exponent`:** `E'(10^-8)/E'(10^-10)≈100.0015` lies in `[99,101]`. The square-root route-B bound (ratio `≈10.008`) relabelled as linear is rejected.
- **`changed_model_relabelled`:** 12 relabellings are rejected:
  - `tau=10^-14`;
  - the R2 cap;
  - `s=1/2`;
  - the zero triple;
  - the selected-strip reference;
  - route A;
  - the AV2 model id;
  - a finite-graph id;
  - the C¹ kernel;
  - the Poisson kernel;
  - the slope `49/4`;
  - a finite-volume provenance.
- **`coherent_evidence_tampering`:** 9 edits are rejected after the packet hash is rebound:
  - a control Boolean flipped;
  - the AX1 gate snapshot removed;
  - the radius halved;
  - the reverse `D'`;
  - the seven-star slope;
  - the AT4-type Boolean flipped;
  - the weak-coupling flag set;
  - a claimed reverse producer;
  - the zero-selected model.
- **`insufficient_verdict_retained`:** rejected are the AT4-type failure relabelled as met, tier (i) relabelled as met, and `tau` retuned to the Poisson-floor threshold.
- **`exact_arithmetic_admission`:** there are no numerical-library imports; float, bool, NaN and zero-denominator inputs are rejected in the checker and the calculator.
- **`root_n_misuse`:** the root sum of squares of the four terms, division by `sqrt 4`, the root sum of squares of the nine group norms (`sqrt(345)/8`) and division by `sqrt 9` are rejected.
- **`no_priority_or_continuum_claim`:** each of the eight false flags set true, `uniform_wilson_claim` without its fixed-spacing scope, and a flipped node flag are rejected.

**Positive checks (27).** The remaining checks are:
- **bindings:** contract hash; premise snapshots bound (30 files, each hash pinned here or bound by the hash-pinned AX1 gate or the AX1-bound AV2 gate); preregistration mirror equal (25 = 25);
- **window audit:** C² matching verbatim; half-line transform and modulus; window constants exact; Machin `pi`;
- **reference, incidence and state bound:** reference unchanged in route B; incidence enumerated; uniform Duhamel slope; the AX1-gate state bound;
- **certificate:** itemized radius; mirror replay; target Boolean; free reference inside; datum and arithmetic; preview consistency; comparison with AV2; lemma-transfer checklist;
- **retained failures and crossover:** three retained-failure checks; crossover;
- **calculator:** domain rejections (31 cases); exact input forms; fixed design;
- **ledger:** the preregistered error terms.

**Private source-edit audit (scratch, not evidence).** On copies of the closure, each of 17 source edits aborts at the intended check, with one exception:
- calculator pair term dropped, and density form `2eps` (both at the gate pin);
- single groups set to 0;
- state `D/2`;
- `M_1` with `pi^+`;
- `M_0=1`;
- exponent 24;
- a weak-coupling label;
- `uniform_wilson_claim` false;
- the zero triple accepted;
- the selected predicate changed;
- orthant stars;
- `continuum_claim` true;
- the sign convention flipped;
- contract and gate byte edits.

The exception is removing the box-dependence test from the Duhamel validator. That edit runs to completion, because the extensive norm is still rejected by the validator's second guard (the slope-value test). This is a redundant guard, not a gap.

## 12. Error ledger (preregistered `state`, `mean_square`, `kernel_dynamics`, `arithmetic`)

- **`state`:** `M_0 D'`, with `D'` the AX1-gate forward tier-(ii) trace-distance bound, by trace duality against the non-effect `W alpha^0_theta(W)`.
- **`mean_square`:** `M_0 m^2<=M_0 D'^2`.
- **`kernel_dynamics`:** `k'M_1=51|tau|s/pi` with `pi^-`, over all `theta`. There is no cutoff or tail.
- **`arithmetic`:** the half-width of the `e^{-3}/4` enclosure. The `pi` rounding is already inside `kernel_dynamics`.

No entry is `not_applicable`.

## 13. Limitations

**Contract claim exclusions (verbatim):**
- resolved interaction shift
- uniform Wilson-mean sign certificate
- weak coupling or continuum
- AQ uniqueness
- scientific priority

**Preregistered claim exclusions (verbatim):**
- free reference inside enclosure => no interaction claim
- uniqueness of the AQ state
- whole-sequence convergence or rate in N
- continuum or weak coupling
- transfer from a finite graph
- relabelling a static shift as dynamical
- scientific priority

**Contract `K_2_note` (verbatim):** no uniform-model K_2 is admitted; no sign certificate rider (loop-2 veto)

**Producer limitations:**
1. **Single producer.** There is no reverse route. The certificate is proposed, not admitted; admission requires the skeptic's independent replay from the contract alone. The `-tau` value is a replay at the U_E image, not a second confirmation.
2. **Inherited without re-proof:**
   - the AV2 window lemma, its constants and the relative-unitary argument (AT4 F10–F12);
   - AX1's route-B constants: `J_0'`, the gap, the reset, the incidence, `D'` and its passage to every AQ1 subsequential limit, and the flip identity;
   - AQ1's construction, nonnegativity and norm dynamics;
   - the AL1/I1 dictionary.

   Fourier inversion, Fubini, Peter–Weyl and Nachtergaele–Sims are cited, not machine-checked. The checker audits the window algebra, re-enumerates the incidence from the fine geometry, re-checks the `J_0'` rationals and reproduces `D'` from the gate formula. It does not re-prove the operator-theoretic premises.
3. **Model scope.** Only the uniform Kogut–Susskind SU(2) model at fixed spacing and strong bare coupling (`g^4>=9.6x10^9`, `|tau|<=10^-8`), with the whole-star-plus-single-group centered boxes (`N>=2`), the cover `R` and the node `s=1`. The boxes are not identified with AL1's all-contained-plaquette boundary.
4. **Upper certificate only.** `r` bounds the error of `d`. It is not a lower bound on `|C(1)-e^{-3}/4|`, and it detects no interaction effect.
5. **Crossover.** `s*` is the crossover of the analytic formula, not a node certificate.
6. **Fixtures are audits only.** The 2×2 trace fixture, the conjugation fixture and the centering fixture are finite algebra and prove no infinite-volume statement.

**Methodological lenses.**
- **Newton, analysis before synthesis.** The uniform radius is analysed into its four preregistered terms. The synthesis is then broken deliberately: dropped groups, the seven-star slope, the extensive norm, other `D` values and tier mixing.
- **Tesla, complete accounting.** All nine groups meeting `R`, the whole real-time axis, both centering costs and the arithmetic radius are charged.

These are modern methodological uses of the snapshotted skills. No historical figure participates in or endorses this work, and no historical or occult material supplies a premise.

## 14. Reproduction

Output directories must be fresh, absolute and outside the checkout:

```bash
python3 -B research/round32/forward/ax2/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/forward/ax2/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/forward/ax2
```

`check.py` does the following, in order:
1. it verifies the contract snapshot's sha256 and the AX1 gate snapshot's sha256 (both pinned), and verifies every other snapshot against the AX1 or AV2 gate bindings;
2. it reads `tau`, `s`, `k'`, `D'`, the target, the reference and the control list from the contract, and `D'`, the incidence and the `J_0'` rationals from the gate;
3. it records its own sha256 and the calculator's before evaluation;
4. it writes `results.json` (52 checks, sorted keys, every number a string) and `source-manifest.json`.

`freeze.json` binds the whole producer closure. The producer directory contains no interpreter cache.
