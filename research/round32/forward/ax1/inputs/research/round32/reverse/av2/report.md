# Hruday window-kernel certificate — AV2 reverse (residue route)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted reverse production under premise isolation (contract control `reverse_premise_isolation`). I read the frozen contract snapshot `inputs/research/round32/contracts/av2.json` first (sha256 `686458cab7a4e6e65b63f0c6418d51496f66f1aada4897115ff14e8bbfad5687`). After that I read only the byte-identical snapshots in `inputs/` and the inherited files named in Section 14. I read no AV2 forward file and no skeptic file except the snapshotted AV1 review `skeptic/av1.md`. I also read no expert file, no deliberation record and none of the `forward_additional_premises`.

The window `g` and its transform are frozen in the contract as a **shared panel premise**. Independence is therefore claimed only for four things:
- the residue derivation of the transform and constants;
- the reconstruction of the window from the target;
- the restated comparison argument;
- the arithmetic and the checker.

All producers, reviewers and the advisor are correlated model agents. This is not human peer review.

**Attribution.** The following are established mathematics:
- L¹ Fourier inversion;
- residue calculus, including Jordan-type arc bounds and the keyhole contour;
- the bounded-perturbation Duhamel identity;
- trace duality.

The Poisson route and its constants come from AT4. The C² window proposal comes from the panel (see `selection-av2.md`). HNM labels are project aliases. Scientific priority is unverified.

## Verdict (reverse half)

The residue route proves the window lemma and the constants for the frozen C² window. These constants are
- `M_0 = ||ĝ||_1 = 2`,
- `M_1 = ∫|θ||ĝ| = 4s/π`,
- `M_2 = ∫θ²|ĝ| = 2s²`.

Together with the AV1-admitted tier-(ii) forward state bound `D`, every AQ1 subsequential state of the zero-selected model at `τ=+10^-8` and `s=1` satisfies

`|C(1) − e^{-3}/4| ≤ r = 2(D+D²) + 49·10^-8/π + r_arith ≈ 1.8319675034×10^-7 ≤ 10^-6.`

The result has these properties:
- **Target met.** The Boolean is decided on exact rationals. `euclidean_node_certified: true`.
- **Datum.** The certified datum is the exact rational midpoint `d = 497870683678639429793424156500617766317/(4·10^40)` of the directed enclosure of `e^{-3}/4`.
- **Interval.** `C(1) ∈ [0.012446583895215644…, 0.012446950288716326…]`.
- **Free reference.** `e^{-3}/4` lies inside the interval, so the sub-label is **`reference_unresolved`**. No interaction shift is claimed.
- **Mirrored coupling.** The `τ=−10^-8` radius is identical. It is a replay of the same `|τ|` formula at the mirrored coupling, not a second confirmation.
- **Retained failures.** The AT4 Poisson radius at `L=10^4` (`8.4151870439×10^-4`) is retained. So is the optimized Poisson floor, which is at least `1.2650882042×10^-6` for every `L`, even as `D→0`. Both are `insufficient`.
- **Crossover.** The certificate crosses `10^-6` at `s* ∈ [6.236863446, 6.236863447]`. No grid claim is made.

This producer proposes **`accepted_within_scope`** for the reverse half. Admission also requires the forward (half-line) route, the exchange and the skeptical review.

## 1. Model and frozen conventions

**Model.** The model is `AQ_patterned_zero_selected`:
- the SU(2) Kogut–Susskind form on Z³ at fixed spacing, with coarse 24-link factors;
- the selected triple exactly `(0,0,0)`, so the reference is the Haar product;
- 21 omitted faces per anchor, grouped into whole stars `φ_b=−(τ/3)ΣW_f`;
- the state is AQ1's centered whole-star subsequential construction; every subsequential limit is covered, and no uniqueness is claimed.

The observable is the original xz Wilson loop `W`. Its complete cover is `R={0,e_z}`, with 48 links, 36 endpoints and seven incident stars `R−S`. The clock is `s=αt_E/ħ` for Euclidean time and `θ=αt/ħ` for real time. The generator is `G=H/α ≥ 0`, the actual AQ1 GNS energy in α units. The positive scales α, ħ, E⋆ and the spacing are fixed.

**Frozen conventions** (contract item 1):

\[
c(\theta)=\langle\chi,e^{i\theta G}\chi\rangle,\qquad \chi=(\pi(W)-m)\Omega,\quad m=\omega(W),\qquad
\hat g(\theta)=\frac1{2\pi}\int_{\mathbb R} g(x)e^{-i\theta x}\,dx,
\tag{HNM-AV2-R01}
\]

\[
C(s)=\langle\chi,e^{-sG}\chi\rangle=\int_{[0,\infty)}e^{-sx}\,d\eta(x),\qquad
c(\theta)=\int e^{i\theta x}d\eta(x),\qquad \eta(\mathbb R)=\|\chi\|^2<\infty .
\tag{HNM-AV2-R02}
\]

Here `η` is the spectral measure of `χ` for `G`. It is supported in `[0,∞)` because AQ1 §5 proves `H_num ≥ 0`. **Only this nonnegativity is used; AQ2's gap is not.** The free reference has `c_0(θ)=e^{3iθ}/4`, since `W1_R` has energy `3α` and Haar variance `1/4` (AT4 F06), and `C_0(s)=e^{-3s}/4`.

## 2. Reverse analysis: from the target back to a kernel

Start from the desired conclusion:

\[
|C(s)-C_0(s)|\le M_0(D+D^2)+kM_1\ \le\ 10^{-6}\quad(s=1,\ \tau=\pm10^{-8}).
\tag{HNM-AV2-R03}
\]

**(a) What representation is needed.** The only dynamical information available is a real-time norm comparison that is linear in `|θ|` (AT4 F11). `C(s)` must therefore be written as an integral of `c(θ)`, that is, `C(s)=∫K(θ)c(θ)dθ` with `K∈L¹`. By Fubini (Section 4), `∫K c = ∫ǩ dη` with `ǩ(x)=∫K(θ)e^{iθx}dθ`. It is therefore necessary and sufficient that `ǩ(x)=e^{-sx}` on `supp η ⊂ [0,∞)`.

The values of `ǩ` on `x<0` are unconstrained. The inverse problem has a kernel, and we record it (Newton lens: the kernel of an inverse map must be stated). The even extension `e^{-s|x|}` gives the Poisson kernel. It is one choice, not a necessity.

**(b) What integrability is needed.** Integrating a bound `|c−c_0| ≤ k|θ|+D+m²` against `|K|` needs finite `M_0=∫|K|` and `M_1=∫|θ||K|`. A rational `K` has finite `M_1` iff it decays like `|θ|^{-3}` or faster. The decay of `K` is set by the smoothness of `ǩ` at the junction `x=0`: a jump in the j-th derivative gives `|θ|^{-(j+1)}`.

The Poisson extension has a kink, `g'(0+)−g'(0−)=−2s`. It therefore decays like `|θ|^{-2}` and `M_1=∞`. This divergence is exactly what forced AT4's cutoff `L`, its tail `s/(πL)` and the floor of Section 8.

**(c) Residue ansatz.** For `x>0`, close the contour in the upper half-plane; only upper-half-plane poles contribute. The value `e^{-sx}` requires exactly one simple pole at `θ=is` and no other upper pole. Put every remaining pole at one lower point `θ=−is`, with order n:

\[
K_n(\theta)=\frac{N_n}{(s+i\theta)(s-i\theta)^n},\qquad |K_n|\sim|\theta|^{-(n+1)},\qquad
M_j<\infty\iff j\le n-1 .
\tag{HNM-AV2-R04}
\]

**(d) Order.** Contract item 2 requires `M_0`, `M_1` and `M_2`. The minimal order is therefore `n=3`, and the checker derives this minimum from the decay orders. `n=1` gives Poisson, `n=2` the C¹ window, and `n=3` the frozen C² window.

## 3. Residue synthesis: the kernel family and the frozen window

**Normalization from the simple pole at `θ=is`.** Write `s+iθ=i(θ−is)`. Then

\[
\operatorname{Res}_{\theta=is}\big[K_n(\theta)e^{i\theta x}\big]=\frac{N_n e^{-sx}}{i(2s)^n},\qquad
\int K_n e^{i\theta x}d\theta=2\pi i\cdot\frac{N_n e^{-sx}}{i(2s)^n}=e^{-sx}\ (x\ge0)\iff N_n=\frac{(2s)^n}{2\pi}.
\tag{HNM-AV2-R05}
\]

The arcs vanish because `|K_n| = O(R^{-(n+1)})` with `n+1 ≥ 2`, so the case `x=0` is included. For `n=1`, `N_1=s/π` gives the Poisson kernel `s/(π(s²+θ²))`. For `n=3`, `N_3=4s³/π`.

**Triple pole at `θ=−is` (x<0, close below, clockwise).** Write `s−iθ=−i(θ+is)`, so `(s−iθ)³=i(θ+is)³`. Set `u=s+iθ`, so that `d/dθ = i d/du` and `u=2s` at the pole. Then

\[
\operatorname{Res}_{\theta=-is}\big[K_3e^{i\theta x}\big]
=\frac{4s^3}{\pi i}\cdot\frac{-1}{2}\,\frac{d^2}{du^2}\Big[\frac{e^{(u-s)x}}{u}\Big]_{u=2s}
=-\frac{1}{\pi i}\,e^{sx}\Big(s^2x^2-sx+\tfrac12\Big),
\]

\[
\int K_3e^{i\theta x}d\theta=-2\pi i\cdot\operatorname{Res}=e^{sx}\,(1-2sx+2s^2x^2)\qquad(x\le0).
\tag{HNM-AV2-R06}
\]

This is exactly the contract's frozen window. The checker computes these residues exactly with Gaussian-rational Laurent series, carrying `x` as a polynomial variable. At `s=1` the pole data are:
- `Res_{is}` of the rational part is `e^{-x}·(−i/8)`;
- `Res_{−is}` is `e^{x}·(i/8 − ix/4 + ix²/4)`.

The same engine gives the family:
- `n=1`: `e^{-s|x|}`;
- `n=2`: `e^{sx}(1−2sx)` for `x<0`, the C¹ window;
- `n=3`: `e^{sx}(1−2sx+2s²x²)`.

The contract's window, transform and constants are compared **only after** this derivation.

**Identification.** `K_3 ∈ L¹` and its inverse transform is the continuous function `g ∈ L¹`. The L¹ inversion theorem therefore gives `K_3(θ)=(2π)^{-1}∫g e^{-iθx}dx` almost everywhere, and hence everywhere by continuity:

\[
\hat g(\theta)=\frac{4s^3}{\pi(s-i\theta)^3(s+i\theta)},\qquad
|\hat g(\theta)|=\frac{4s^3}{\pi}\,\frac1{|s-i\theta|^3|s+i\theta|}=\frac{4s^3}{\pi}(s^2+\theta^2)^{-2}.
\tag{HNM-AV2-R07}
\]

The checker verifies `|ĝ|²` exactly at `θ ∈ {0, 1, −3/7, 5, −11/2}`.

**Regularity.** At `x=0` the one-sided derivatives of `g` are
- from the right: `(1, −s, s², −s³)`;
- from the left: `(1, −s, s², 7s³)`.

So `g ∈ C²`, and `g'''` jumps by `−8s³`. This jump matches the `|θ|^{-4}` decay: `(2π)^{-1}·8s³/θ⁴ = 4s³/(πθ⁴)`. The polynomial `1+2sy+2s²y²` has negative discriminant, so `g>0` everywhere. Laplace moments give `‖g‖₁ = 1/s+(1+2+4)/s = 8/s`, and `ĝ(0) = ‖g‖₁/(2π) = 4/(πs)`. Finally `g→0` at `±∞`, so `g ∈ L¹∩C_0`.

## 4. Window lemma (contract item 1)

\[
C(s)=\int_{\mathbb R}\hat g(\theta)\,c(\theta)\,d\theta,\qquad C_0(s)=\int\hat g(\theta)c_0(\theta)\,d\theta=\frac{g(3)}4=\frac{e^{-3s}}4 .
\tag{HNM-AV2-R08}
\]

*Proof.* The premises are:
- `g ∈ L¹∩C_0` and `ĝ ∈ L¹` (Sections 3 and 5);
- `η` is finite and supported in `[0,∞)` (AQ1 nonnegativity only).

The function `(θ,x) ↦ ĝ(θ)e^{iθx}` is jointly measurable, and `∫∫|ĝ(θ)| dθ dη(x) = M_0 η(ℝ) = 2‖χ‖² < ∞`. Fubini therefore gives

`∫ĝ(θ)c(θ)dθ = ∫[∫ĝ(θ)e^{iθx}dθ]dη(x) = ∫g(x)dη(x)`.

Pointwise inversion holds at every `x`, both from (R05)–(R06) directly and from the inversion theorem, since `g` is continuous. On `supp η` we have `g(x)=e^{-sx}`, so the integral equals `C(s)`. For the free reference, `η_0=δ_3/4` and `3>0`. ∎

**Nonnegativity is essential.** A spectral atom at `x=−1` would contribute `g(−1)=e^{-s}(1+2s+2s²)` (`=5/e` at `s=1`), not the heat value `e^{s}`. The mirrored convention `θ→−θ` evaluates `g(−3)/4=25e^{-3}/4` on the free atom. Both are executed damaging controls.

## 5. Constants by residues (contract item 2)

Write `|ĝ| = (4s³/π)(θ−is)^{-2}(θ+is)^{-2}`.

\[
M_0=\frac{4s^3}{\pi}\,2\pi i\operatorname{Res}_{is}\frac{1}{(\theta-is)^2(\theta+is)^2}
=8is^3\cdot\frac{-2}{(2is)^3}=8is^3\cdot\frac1{4is^3}=2 .
\tag{HNM-AV2-R09}
\]

`M_1` is not a full-line residue, because `|θ|` is not analytic. Use the keyhole contour, with the cut along `[0,∞)` and `arg ∈ (0,2π)`:

\[
\int_0^\infty\frac{\theta\,d\theta}{(s^2+\theta^2)^2}=-\sum_{z_0=\pm is}\operatorname{Res}\Big[\frac{z\log z}{(z^2+s^2)^2}\Big]
=-\Big(-\frac1{4s^2}-\frac1{4s^2}\Big)=\frac1{2s^2},\qquad
M_1=2\cdot\frac{4s^3}{\pi}\cdot\frac1{2s^2}=\frac{4s}{\pi}.
\tag{HNM-AV2-R10}
\]

At each pole the `log z_0` coefficient equals `Res f`. This is zero because `θ(s²+θ²)^{-2} = −½ d/dθ (s²+θ²)^{-1}` is an exact derivative, and the checker requires the cancellation pole by pole with a formal log symbol. A substitution cross-check, `u=θ²`, gives `½∫_0^∞(s²+u)^{-2}du = 1/(2s²)`.

\[
M_2=\frac{4s^3}{\pi}\,2\pi i\operatorname{Res}_{is}\frac{\theta^2}{(\theta-is)^2(\theta+is)^2}
=8is^3\cdot\Big(-\frac{i}{4s}\Big)=2s^2 .
\tag{HNM-AV2-R11}
\]

The checker computes these at `s ∈ {1/3, 1, 2, 7}`. It obtains `M_0=2`, `M_1·π/s=4` and `M_2/s²=2` exactly, then compares them with the contract's `||ghat||_1=2`, `4s/pi` and `2s^2`. The contract's `pi` is enclosed by Machin's formula with directed rounding at `10^-40`.

**Trap.** The signed integral `∫ĝ = g(0) = 1` is not the L¹ norm. Because `ĝ` is complex, `‖ĝ‖₁ = 2`. The state term is therefore charged at twice the Poisson kernel's mass.

**Moment ladder.** The residue engine refuses a moment whose integrand decays slower than `|θ|^{-2}`:
- Poisson: `M_0=1`, and `M_1` is refused;
- C² window: `M_0`, `M_1` and `M_2` exist, and `M_3` is refused;
- C¹ window: `|ĝ_1| = (2s²/π)(s²+θ²)^{-3/2}` is not rational, so this route refuses it (Section 11).

## 6. Real-time comparison (contract item 3)

**Seven-star splitting (restating AT4 F10–F11).** In a centered box `Λ_N` (N≥2) containing `R`, write

`G_N = A_N + B_N`, where `A_N = G_{0,R} + G_{outside,N}` and `B_N = Σ_{b ∈ R−S} V_b`.

Here `V_b = φ_b/8`, and `‖V_b‖ ≤ 7|τ|/8` in `G=H/α` units. Every star meeting `R` is assigned whole to `B_N`, including its faces that act outside `R`. `A_N` then evolves `W` exactly as the free `R` generator does, and the outside part commutes strongly. The seven incident anchors are `{0,−e_x,−e_y,−e_z,e_z,e_z−e_x,e_z−e_y}`. They are all retained for `N≥2`: the checker finds 7 of 7 at N=2 and N=3, and 4 at N=1. Hence

\[
\|B_N\|\le\frac{49|\tau|}8,\qquad k:=2\|B_N\|\|W\|=\frac{49|\tau|}4\quad(\text{uniform in }N).
\tag{HNM-AV2-R12}
\]

**Domain argument.** `A_N` and `G_N` share the domain of the finite Casimir sum because `B_N` is bounded. On that common domain, differentiate the relative unitary `K(θ) = e^{iθG_N}e^{-iθA_N}`. Its derivative `i e^{iθG_N}B_N e^{-iθA_N}` is bounded and strongly continuous. Integrate vectorwise and extend by density to obtain `‖K(θ)−I‖ ≤ |θ|‖B_N‖`.

Only after this step insert the bounded `W`. Since `α^N_θ(W) = K α^0_θ(W) K*`,

`‖α^N_θ(W) − α^0_θ(W)‖ ≤ 2‖K−I‖‖W‖ ≤ k|θ|`.

This argument uses no domain invariance of arbitrary bounded observables and no norm-Bochner derivative. AQ1's local norm dynamics convergence, uniform on compact θ-intervals (Nachtergaele–Sims placement), passes the bound to the actual AQ evolution at every real θ. The slope is local: an extensive star norm grows like `(2N)³`, which is 64 stars at N=2 and 216 at N=3, and it is rejected.

**Comparison (AT4 F12 with the AV1 state bound).** Since `c(θ) = ω(Wα_θ(W)) − m²` and `c_0(θ) = ω_0(Wα^0_θ(W))`,

\[
|c(\theta)-c_0(\theta)|\le\underbrace{|\omega(W[\alpha_\theta(W)-\alpha^0_\theta(W)])|}_{\le k|\theta|}
+\underbrace{|\operatorname{Tr}[(\rho_R-P_R)\,W\alpha^0_\theta(W)]|}_{\le D}+\underbrace{m^2}_{\le D^2}
\qquad(\theta\in\mathbb R).
\tag{HNM-AV2-R13}
\]

The terms rest on these facts:
- **State term.** `Wα^0_θ(W) ∈ B(H_R)` has norm at most 1, and trace duality gives `≤ D`. The operator is complex and not an effect, so the `D/2` effect refinement is **not** applied. A fixture shows that `D/2` fails for a non-effect: with `ρ−P = diag(−1/10, 1/10)` and `X = diag(1, (−7+24i)/25)`, `|Tr[(ρ−P)X]|² = 16/625 > (‖ρ−P‖₁/2)² = 1/100`.
- **Mean term.** `|m| = |ω(W)| ≤ D` by trace duality, since `ω_0(W)=0`, so `m² ≤ D²` is charged.
- **The value of D.** `D` is the AV1 tier-(ii) forward value read from the contract snapshot, `D = 585079838465912592144137406066050/42981220507576537932303142777593983768257 ≈ 1.3612452870×10^-8`. The checker confirms three things: it equals the value bound by the AV1 gate's decision; the AV1 formula (`t_1=49|τ|/144`, `J=28|τ|`, `T=t_1/(1−352J)`, `ε=2T+T²`, `D=2ε(1+ε)/(1+ε²)`) reproduces it exactly; and tier (i), the AT4 square-root bound and the reverse 82-face refinement are rejected.

## 7. Radius at the cap (contract item 4)

Integrating (R13) against `|ĝ|` and using (R08):

\[
|C(s)-C_0(s)|\le M_0(D+D^2)+kM_1=2(D+D^2)+\frac{49|\tau|s}{\pi},\qquad
C(s)\in[d-r,\ d+r],\quad r=\text{state}+\text{mean\_square}+\text{kernel\_dynamics}+\text{arithmetic}.
\tag{HNM-AV2-R14}
\]

At `τ=+10^-8` and `s=1`, with exact rationals from `output/results.json` and truncated decimal previews:

| term | exact rational (or directed bound) | preview |
|---|---|---|
| state `M_0·D` | `1170159676931825184288274812132100/42981220507576537932303142777593983768257` | `2.7224905741×10^-8` |
| mean_square `M_0·D²` | exact rational in `results.json` | `3.7059774629×10^-16` |
| kernel_dynamics `k·M_1` (π lower bound, rounded up) | `1559718442300574290535060881050641/10^40` | `1.5597184423×10^-7` |
| arithmetic (half-width of the `e^{-3}/4` enclosure) | `1/(4·10^40)` | `2.5×10^-41` |
| **radius r** | exact rational in `results.json` | **`1.8319675034×10^-7`** |
| datum d | `497870683678639429793424156500617766317/(4·10^40)` | `0.0124467670919659857448…` |
| interval | `[d−r, d+r]` exact | `[0.0124465838952156446…, 0.0124469502887163269…]` |
| target | `1/1000000` (read from `preregistration.target`) | met: `r ≤ 10^-6` (exact Boolean) |

The **`τ=−10^-8` replay** gives the identical datum and radius, because only `|τ|` enters `k` and `D`. The value `e^{-3}/4` is enclosed twice:
- the calculator uses the reciprocal of the positive Taylor series of `e^{3}`, with a geometric tail, halving and outward squaring;
- the checker uses alternating partial sums of `e^{-y}` on `[0,1/2]`.

The two enclosures agree to within `10^-35`, and they are consistent with `(e^{-1})³`.

Relative to the contract preview (about `1.83e-7`, acceptance band `1.7–2.0e-7`), the computed radius lies inside the band.

## 8. Retained failures (contract item 5)

\[
\mathcal E_{\rm Pois}(D,L)=D+D^2+\frac{ks}{\pi}\log(1+L^2/s^2)+\Big(\tfrac12+\tfrac D2\Big)\frac{2s}{\pi L}.
\tag{HNM-AV2-R15}
\]

All four cases below are at unchanged `τ=10^-8` and `s=1`.

- **AT4 at `L=10^4`, with `D_AT4 = 2√(49|τ|/3)`.** The terms are:
  - state: `8.0829037686×10^-4`;
  - mean square: `6.5333×10^-7`;
  - bulk: `7.1827688723×10^-7`;
  - tail: `3.1856717300×10^-5`.

  The total is `𝓔 = 8.4151870439×10^-4`, which matches the contract's `~0.000841519`. Outcome: `insufficient`, retained.
- **Poisson at `L=10^4` with the admitted `D`.** The radius is `3.2562878×10^-5`. The tail alone (`3.18×10^-5`) exceeds `10^-6`.
- **Optimized Poisson floor (`D→0`).** The function is `F(L) = (k/π)log(1+L²) + 1/(πL)`. Its derivative has the sign of `u(L) = 2kL³ − L² − 1`, which has exactly one positive root. `u` is negative on `(0, 1/(3k)]`, so `F` decreases up to `L*` and increases after it. Integer bisection gives `L* ∈ [4081632, 4081633]`. The resulting bounds hold for every `L>0`:

  \[
  1.2650882042\times10^{-6}\ \le\ \min_{L>0}F(L)\ \le\ 1.2650882234\times10^{-6},
  \tag{HNM-AV2-R16}
  \]

  which matches the contract's `~1.2651e-6 at L~4.08e6`. With the admitted `D` added, the floor is at least `1.2787×10^-6`. Outcome: `insufficient`, retained. The Poisson certificate cannot reach `10^-6` at any cutoff.
- **Divergent versus finite first moment.**

  \[
  \int_{-L}^{L}|\theta|\frac{s}{\pi(s^2+\theta^2)}d\theta=\frac{s}{\pi}\log\Big(1+\frac{L^2}{s^2}\Big)\xrightarrow[L\to\infty]{}\infty,\qquad
  \int_{-L}^{L}|\theta||\hat g|\,d\theta=\frac{4s}{\pi}\,\frac{L^2}{s^2+L^2}\ \uparrow\ \frac{4s}{\pi}.
  \tag{HNM-AV2-R17}
  \]

  The checker exhibits the divergence. `L=10^2` already exceeds the window's `4s/π`, and `L=10^{682190}` exceeds `10^6`. Every finite bound on the Poisson moment is rejected, while the window's truncated moments stay below `M_1`.

## 9. Crossover (contract item 6)

`E(s) = 2(D+D²) + 49|τ|s/π` is linear in `s`. Its crossover is

\[
s^*=\frac{(10^{-6}-2(D+D^2))\,\pi}{49|\tau|}\in[6.236863446,\ 6.236863447].
\tag{HNM-AV2-R18}
\]

The bracket uses the directed π enclosure and is rounded outward to `10^-9`. It lies in the contract's "about 6.1–6.3". Two witnesses confirm it:
- at `s = s*_lo − 10^-9`, the calculator certificate meets `10^-6`, with radius `9.999999998×10^-7`;
- at `s = s*_hi + 10^-9`, even the analytic lower value of `E` exceeds `10^-6`.

**No grid claim** is made beyond or below this single analysis. The certificate is evaluated at the frozen node `s=1` only; there is no `[0,128]` claim at the cap, and the flag is `grid_claim:false`. Using the crossover as a node is a changed-model relabelling and is rejected.

## 10. The reference stays unresolved (contract item 7)

The enclosure `[f⁻,f⁺]` of `e^{-3}/4` lies inside `[d−r, d+r]`. The datum is by construction the midpoint of the free-reference enclosure, and the interaction enters only through the radius. No interaction-induced shift, sign or coefficient of `C(s)` follows. The sub-label is `reference_unresolved`, with `resolved_interaction_shift:false`.

## 11. Calculator and the C¹ preview (contract items 8 and 10)

`calculator.py` exports `certify(...)` in the AT5 style, but uses the window formula (HNM-AV2-R14).

**Inputs.** Accepted inputs are exact only: int, `Fraction`, exact decimal text or `p/q` text. Floats, Booleans, NaN, Infinity, empty text, zero denominators, malformed text and unsupported objects are rejected.

**Domain.**
- the selected triple is exactly zero;
- `|τ| ≤ 10^-8`;
- `s > 0`;
- α, ħ, E⋆, the spacing and the target are positive;
- `state_tier='ii_forward'` only (control `av1_tier_bound`);
- `kernel='C2_window'` only.

**Fixed design.** `fixed_design=True` enforces `τ=+10^-8`, `s=1` and target `10^-6`.

**D and the constants.** `D` is computed from the AV1 tier-(ii) forward formula, and at the cap the calculator requires equality with the gate-bound rational. The constants `M_0=2` and `M_1=4s/π` are fixed in the calculator. The checker re-derives both by residues and requires every emitted cost to match them. The calculator also emits `physical_Euclidean_time = ħs/α`; for example, α=5 and ħ=7 give `7/5` with the same radius.

The checker runs 31 malformed or out-of-domain calls, and each must be rejected. They include:
- tier (i), the reverse tier (ii) and the AT4 square root;
- the C¹ and Poisson kernels;
- changes to the fixed design.

**C¹ window — preview only** (`preview_c1_window`, `certified:false`). The residue engine derives `g_1(x) = e^{sx}(1−2sx)` for `x<0`, the `n=2` member of (R04). For this window:
- negative-atom value: `g_1(−1) = 3/e`;
- sign-mutation value: `7e^{-3}/4`.

Its modulus `(2s²/π)(s²+θ²)^{-3/2}` is not rational, so this producer's residue route refuses it. The substitution `θ = s·tanφ` gives `M_0 = 4/π`, `M_1 = 4s/π` and `M_2 = ∞`, since `θ²|ĝ_1| ~ 1/|θ|`.

The preview radius is `(4/π)(D+D²) + 49|τ|s/π ≈ 1.7330×10^-7`. This is **smaller** than the frozen C² radius, because `4/π < 2`. The rejection of a post-hoc kernel switch is therefore not vacuous. A switch after `D` is known is rejected by the checker, by the calculator and by the residue engine.

## 12. Checker and controls (contract item 9)

`check.py --output <absolute fresh dir>` uses the standard library only and makes every admission decision in exact `Fraction`/Gaussian-rational arithmetic. Before any evaluation it:
- records its own sha256 and the calculator's sha256;
- verifies the contract snapshot's sha256;
- reads the target, reference, τ, s, `D`, window, transform, slope and retained-failure values from the contract;
- reads the gate decision and the selection record's "unchanged 10^-6" from the snapshots.

Results and outputs:
- It writes `results.json` with sorted keys and 50 checks: 26 positive exact checks and 24 contract controls. It also writes `source-manifest.json`.
- The claim flags are `continuum_claim:false`, `uniform_wilson_claim:false`, `resolved_interaction_shift:false`, `scientific_priority_verified:false`, `grid_claim:false` and `euclidean_node_certified:true`. The last is decided as `r ≤ 10^-6`.

Every control is a damaging mutation that must raise an explicit exception; `assert` is never used. The output is byte-identical under `python3 -B` and `python3 -B -O`.

| control | damaging mutations rejected |
|---|---|
| missing_incoming_stars | outgoing anchors {0,e_z}; origin star only |
| full_original_wilson_cover | origin factor only; four displayed links; extra factor |
| wrong_delta_alpha_hbar_clock | exponent 24 with the α clock; energy 3 with the δ clock; normalized star norm 7\|τ\| in α units; eightfold slope 98\|τ\| |
| vector_versus_scalar_centering | scalar subtraction; uncentered readout. Exact control +1/10000, −51/10000, 1/16; the window keeps `m²g(0)=m²` |
| first_order_mean_charged | mean-square term dropped; zero mean assumed |
| tau_scaling_exponent | AT4 square-root `D` in the window: ratio ≈10.008, not in [99,101]. Admitted ratio 100.00145 |
| changed_model_relabelled | nonzero triple; AT5 τ=10^-14 as the cap node; s=6 as the node; finite-graph id; finite-box provenance |
| coherent_evidence_tampering | rehashed contract with: target 10^-3; tier-(i) `D`; C¹ window; `‖ĝ‖₁=1`; two-star slope; τ=10^-14; control removed. Also a byte change without rehash |
| insufficient_verdict_retained | AT4 Poisson as accepted; Poisson floor as limited; tier (i) as accepted; lemma failure as limited |
| exact_arithmetic_admission | float τ; bool; NaN; float admission; zero denominator |
| root_n_misuse | root-sum-square of the four terms; seven stars in quadrature (`√7`) |
| no_priority_or_continuum_claim | continuum, priority, uniform Wilson, resolved shift and grid flags set true; node flag flipped |
| kernel_identity_on_support | doubled normalization; poles swapped (θ→−θ); poles at ±2is; real-axis pole |
| kernel_negative_atom_misread | atom at x=−1 read as `e^{s}` (actual `5e^{-1}`); negative support admitted |
| kernel_l1_and_first_moment | `∫ĝ=1` as `M_0`; probability mass 1; one-sided `M_1=2s/π`; `M_1` without π |
| poisson_kink_divergence | finite Poisson `M_1` (the engine refuses); Poisson moment bounded by `4s/π` or by 10^6 |
| window_linear_in_s | `M_1` independent of s; `M_1` quadratic in s |
| local_not_extensive_duhamel | extensive slope in boxes N=2 (64 stars) and N=3 (216) |
| tau_zero_null_replay | window at τ=0 with a Poisson tail floor; Poisson tail dropped; window bypass branch. At τ=0 the window radius equals the arithmetic term `1/(4·10^40)` alone, while Poisson keeps `s/(πL) ≈ 3.18×10^-5` |
| window_fourier_sign_convention | θ→−θ on the free atom gives `25e^{-3}/4`; θ→−θ kernel |
| state_term_not_effect | `D/2` on the complex operator; halved state term in the radius |
| av1_tier_bound | tier (i); AT4 square root; reverse 82-face value (admitted in AV1 but not bound for AV2); halved `D`; tier-(i) provenance |
| reverse_premise_isolation | skeptic triage added; deliberation added; forward AV2 added; a premise removed |
| c1_window_preview_only | switch after `D` is known; calculator C¹ certificate; residue modulus of the C¹ kernel |

The 12 universal ids are the first 12 rows. The remaining 12 rows are the AV2-specific controls.

## 13. Limitations and exclusions

**Claim exclusions, exactly as the contract lists them:**
- resolved interaction shift (free value inside)
- full [0,128] grid at the cap
- uniform Wilson magnetic theory
- AQ uniqueness or a rate in N
- continuum construction
- scientific priority
- the second-order Dyson refinement
- any shift of C(s)

**Preregistered exclusions,** also respected:
- free reference inside enclosure => no interaction claim
- uniqueness of the AQ state
- whole-sequence convergence or rate in N
- continuum or weak coupling
- transfer from a finite graph
- relabelling a static shift as dynamical
- scientific priority

**Scope and honest gaps:**
- **Model.** Only the zero-selected AQ subfamily, the cover `R`, fixed spacing and the single node `s=1` at `|τ|=10^-8` are covered. The bound holds for every AQ1 subsequential limit separately; the states are not identified with one another. Nothing transfers to nonzero selected triples (non-Haar `P_R`), uniform Wilson theory, weak coupling or the continuum.
- **Upper certificate only.** No lower bound on `|C(1)−e^{-3}/4|` is claimed.
- **Inherited without re-proof:**
  - AQ1 nonnegativity, trace-norm construction and local norm dynamics;
  - AT4 F10–F12, restated here, with the Nachtergaele–Sims placement;
  - the AV1 bound `D`, which is bound by its gate and not re-derived beyond reproducing its formula;
  - the I1 dictionary.
- **Shared premise.** The window and its transform are frozen panel premises. Independence covers only the residue derivation, the reconstruction, the arithmetic and the checker.
- **Mirrored coupling.** The `−τ` value is a replay of the same `|τ|` formula.
- **Calculator below the cap.** In reusable mode below the cap, the calculator evaluates the AV1 tier-(ii) formula at `|τ|`. The gate quotes the cap value and a scaling ratio computed from the same formula. The node certificate uses only the cap value.
- **Conservative constant term.** The constant term is charged at `‖ĝ‖₁ = 2`. No refinement of it was attempted, because post-hoc changes are excluded.

## 14. Findings for review, incomplete steps, inherited reads, reproduction

**Findings (non-blocking):**
1. The contract's tier-(i) preview "3.6–4.7e-5" is rounded. With the gate's `D_i`, the exact tier-(i) window radius is `4.7518×10^-5`, slightly above 4.7e-5. It is retained as `limited`.
2. The C¹ window would give a smaller radius (`1.733e-7`) than the frozen C² window (`1.832e-7`). The kernel-switch rejection therefore protects against a real post-hoc improvement.
3. The window doubles the state term relative to a positive kernel, since `‖ĝ‖₁=2` while `∫ĝ=1`. The dynamics term `49|τ|s/π` dominates the radius, at 85%.

**Incomplete steps.** None of contract items 1–10 is incomplete on the reverse route. Three steps remain outside this producer: the forward half-line route, the exchange, and the skeptical review with the gate.

**Inherited inputs read beyond `inputs/`:**
- `research/round32/tools/README.md` and `research/round32/tools/freeze.py`, for the protocol;
- `research/round31/forward/at5/check.py` and `research/round32/reverse/av1/check.py`, for code style only.

I also compared the repository contract with its snapshot by sha256 only. None of these files carries premise weight.

**Method lenses.** These are modern methodological uses of the frozen Round32 skills; no historical figure endorses anything here.
- *Newton:* the reverse analysis runs from the target to the kernel of the inverse map, and then forwards by residues.
- *Tesla:* the source is the seven incident stars, the load is the cover `R`, the clock is `θ=αt/ħ`, and the transfer element is the window kernel, with its exact constants stated before evaluation. The `±τ` mirror is a control, not a magnitude estimate. The Poisson cutoff was a proof resource that the window removes.
- *Historical panel:* the free reference inside the enclosure is `reference_unresolved`.

**Reproduce** into fresh absolute directories outside the checkout:

```bash
python3 -B research/round32/reverse/av2/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/reverse/av2/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/reverse/av2
```
