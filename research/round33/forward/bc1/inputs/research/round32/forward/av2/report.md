# Hruday window-kernel certificate at the original cap — AV2 forward (half-line transforms)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production under the frozen AV2 contract (`research/round32/contracts/av2.json`, sha256 `686458cab7a4e6e65b63f0c6418d51496f66f1aada4897115ff14e8bbfad5687`). I read the contract first and then only the snapshots in `inputs/`. These are AGENTS.md, the contract, its 25 `shared_premises` and its three `forward_additional_premises`: the skeptic's triage, the skeptic's loop-2 response and deliberation-1.

The window `g`, its transform and the three constants are frozen in the contract as a **shared panel premise**. They first appear as a skeptic's sketch in triage (c)2 and loop-2 §2(a), and this producer read both. Independence is therefore claimed only for the forward derivation (half-line transforms and exact antiderivatives), the checker, the calculator, the retained-failure arithmetic and the controls. Even there, the work is correlated model-agent production, not independent human review.

**Other files read** outside `inputs/`, all for protocol or code style only and none carrying premise weight:
- `research/round32/tools/README.md` and `research/round32/tools/freeze.py` (protocol);
- `research/round31/forward/at5/check.py` and `research/round32/forward/av1/check.py` (code style).

The exact arithmetic routines in `calculator.py` come from the snapshotted premise `research/round31/forward/at5/calculator.py`, with the outward-rounding denominator changed to `10^40`. A directory listing showed that `research/round32/reverse/av2/` exists. No file under `research/round32/reverse/` and no other current AV2 work was opened.

**Attribution.** The following are established methods and are credited as such:
- the Fourier inversion theorem for `L^1` functions with `L^1` transforms;
- Fubini's theorem;
- Laplace transforms of polynomial exponentials;
- bounded-perturbation (relative-unitary) Duhamel estimates;
- trace duality;
- Machin's formula.

HNM labels are project aliases. Scientific priority is unverified.

**Verdict (forward route).** In the actual AQ zero-selected patterned model at **tau=+10^-8** and **s=1**, take the exact rational datum

\[
 d=\frac{497870683678639429793424156500617766317}{4\cdot10^{40}}
 =0.012446767091965985744835603912515444157925 .
\]

Its certified absolute error is

\[
 r\le 1.83196750342\times10^{-7}\quad(\text{exact rational in }\texttt{output/results.json}),
\]

which is below the unchanged `10^-6` target by a factor of about 5.4586. The actual centered Wilson correlation is enclosed outward as

\[
 C_\tau(1)\in[0.01244658389521564455,\ 0.01244695028871632694].
\]

The window kernel has no real-time cutoff and no tail. Its constants are `M_0=2`, `M_1=4s/pi` and `M_2=2s^2`, all proved here by half-line transforms. The value at `tau=-10^-8` comes from the same `|tau|` formula and is reported as a **replay at the mirrored coupling**, not as a second confirmation. The free reference `e^{-3}/4` lies inside the interval, so the result carries the sub-label **`reference_unresolved`** and claims no interaction shift.

The retained failures still stand at unchanged `tau` and `s`:
- the AT4 Poisson radius at `L=10^4`, about `8.4152e-4`;
- the optimized Poisson floor, which is at least `1.265088223e-6` for **every** `L`, even with `D->0`.

The forward producer proposes **accepted_within_scope for the forward half**. The contract's acceptance also needs the reverse residue route and skeptical review, which are outside this producer's work. The checker runs 50 exact checks. Each of the 24 contract controls rejects at least one damaging mutation, 68 in all, and each rejection is recorded in `results.json`.

## 1. Model, state and clock (items 1 and 3)

The model is exactly the contract's `AQ_patterned_zero_selected`:
- the SU(2) Kogut–Susskind form on `Z^3` at fixed spacing;
- coarse factors owning 24 links;
- the selected triple exactly `(0,0,0)`, so the reference `P_R` is the Haar product;
- 21 omitted anchored faces per factor, grouped into whole stars `phi_b=-(tau/3) sum W_f` (normalized units `delta=alpha/8`);
- `tau=+10^-8`, with `-10^-8` as the control;
- the original xz Wilson loop `W` with complete cover `R={0,e_z}` (48 links, 36 endpoints) and seven incident stars `R-S={0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y}`.

The state is AQ1's chosen centered-box subsequential state `omega`, with GNS vacuum `Omega` and actual nonnegative physical generator. Put `G=H_phys/alpha`. The clocks are `theta=alpha t/hbar` (real time) and `s=alpha t_E/hbar` (Euclidean). The older normalized clock is `u=s/8`, with the free Wilson energy written as 24 in that unit. The positive scales `alpha`, `hbar`, `E_star` and the lattice spacing are fixed.

Let `m=omega(W)` and `chi=(pi(W)-m)Omega`. With `alpha_theta(W)=e^{i theta G}We^{-i theta G}` and `G Omega=0`,

\[
 c(\theta):=\langle\chi,e^{i\theta G}\chi\rangle=\omega(W\alpha_\theta(W))-m^2,\qquad
 C(s):=\langle\chi,e^{-sG}\chi\rangle .
 \tag{HNM-AV2-F01}
\]

Let `eta` be the spectral measure of `G` in the vector `chi`. By **AQ1 §5 (nonnegativity only)**, `G>=0`, so `eta` is a positive measure on `[0,inf)`. It is finite: `eta([0,inf))=||chi||^2=omega(W^2)-m^2<=1`. By the spectral theorem,

\[
 c(\theta)=\int_{[0,\infty)}e^{i\theta x}\,d\eta(x),\qquad C(s)=\int_{[0,\infty)}e^{-sx}\,d\eta(x).
 \tag{HNM-AV2-F02}
\]

The AQ2 gap, which would give `supp eta` inside `{0} ∪ [1/16,inf)`, is **not used**.

**Free reference.** Each of the four original Wilson links carries Casimir `3/4`, so `G_{0,R}(W 1_R)=3W 1_R`. Haar gives `omega_0(W)=0` and `omega_0(W^2)=1/4`. Hence the free centered measure is `eta_0=delta_3/4`, and

\[
 c_0(\theta)=\tfrac14e^{3i\theta},\qquad C_0(s)=\tfrac14e^{-3s}.
 \tag{HNM-AV2-F03}
\]

In the normalized clock the same exponent reads `24u`. Using exponent 24 with `s` is an eightfold clock error, and the `wrong_delta_alpha_hbar_clock` control rejects it.

**State premise.** The state premise is the admitted AV1 forward tier-(ii) bound. The contract states it and the AV1 gate decision binds it:

\[
 \|\rho_R-P_R\|_1\le D=\frac{585079838465912592144137406066050}{42981220507576537932303142777593983768257}\approx1.36124528703\times10^{-8}.
 \tag{HNM-AV2-F04}
\]

The checker re-derives `D` exactly from the AV1 formula: `J=28|tau|`, `t_1=49|tau|/144`, `T=t_1/(1-352J)`, `eps=2T+T^2` and `D=2eps(1+eps)/(1+eps^2)`. It then compares the result with both the contract and the gate. Trace duality with `omega_0(W)=0` and `||W||=1` gives `|m|<=D`, hence `m^2<=D^2`. The following are **not used**: tier (i), the AT4 square-root bound, and the reverse 82-face refinement (valid in AV1, but not the premise this contract binds).

## 2. Window lemma (item 1)

The frozen conventions are `c(theta)=<chi,e^{i theta G}chi>` and

\[
 \hat g(\theta)=\frac1{2\pi}\int_{\mathbb R}g(x)e^{-i\theta x}\,dx,\qquad
 g(x)=\begin{cases}e^{-sx},&x\ge0,\\ e^{sx}(1-2sx+2s^2x^2),&x<0,\end{cases}\qquad s>0.
 \tag{HNM-AV2-F05}
\]

**`g` lies in `L^1 ∩ C_0`.** Write `y=|x|`. On `x<0`, `g=e^{-sy}(1+2sy+2s^2y^2)>0`, and both branches decay exponentially. At `x=0` both branches equal 1, so `g` is continuous, positive, bounded by `sup_y e^{-sy}(1+2sy+2s^2y^2)<inf` and tends to 0 at `±inf`. Its norm is

\[
 \|g\|_1=\int_0^\infty e^{-sx}dx+\int_0^\infty e^{-sy}(1+2sy+2s^2y^2)dy=\tfrac1s+\bigl(\tfrac1s+\tfrac2s+\tfrac4s\bigr)=\tfrac8s .
\]

**C² matching at 0.** On the left, `g=e^{sx}p(x)` with `p=1-2sx+2s^2x^2`.

| order | right, `e^{-sx}` | left, `e^{sx}p` |
|---|---|---|
| value | `1` | `p(0)=1` |
| first derivative | `-s` | `s+p'(0)=s-2s=-s` |
| second derivative | `s^2` | `s^2+2sp'(0)+p''(0)=s^2-4s^2+4s^2=s^2` |
| third derivative | `-s^3` | `s^3+3s^2p'(0)+3sp''(0)=7s^3` |

The jump `g'''(0+)-g'''(0-)=-8s^3` is nonzero. It is what fixes the `theta^-4` decay of `|ghat|`: `(1/2pi)·8s^3=4s^3/pi`.

**`ghat` lies in `L^1`.** This follows from the explicit modulus in (F11), `|ghat|=(4s^3/pi)(s^2+theta^2)^-2`, whose integral is `M_0=2`.

**Pointwise inversion.** For `g in L^1` with `ghat in L^1`, the Fourier inversion theorem gives `g(x)=∫ghat(theta)e^{i theta x}dtheta` for almost every `x`. Both sides are continuous: the left because `g` is, the right by dominated convergence with majorant `|ghat|`. So equality holds for **every** real `x`. On the spectral support, `x>=0`,

\[
 e^{-sx}=g(x)=\int_{\mathbb R}\hat g(\theta)e^{i\theta x}\,d\theta\qquad(x\ge0).
 \tag{HNM-AV2-F06}
\]

**Fubini.** `∫∫|ghat(theta)e^{i theta x}| dtheta deta(x) = M_0 eta([0,inf)) < inf`. Therefore

\[
 C(s)=\int e^{-sx}d\eta=\int g\,d\eta=\int_{\mathbb R}\hat g(\theta)\Bigl[\int e^{i\theta x}d\eta(x)\Bigr]d\theta=\int_{\mathbb R}\hat g(\theta)\,c(\theta)\,d\theta .
 \tag{HNM-AV2-F07}
\]

`c` is continuous and bounded by `||chi||^2`, so the last integral exists absolutely. The same argument applied to `eta_0=delta_3/4` gives

\[
 C_0(s)=\int\hat g(\theta)\tfrac14e^{3i\theta}d\theta=\tfrac14g(3)=\tfrac14e^{-3s}.
 \tag{HNM-AV2-F08}
\]

**Why the hypotheses matter.** The checker tests each one.
- **Nonnegativity is essential.** A spectral atom at `x=-1` would be read as `g(-1)=e^{-s}(1+2s+2s^2)`, which is `5/e` at `s=1`. The heat semigroup would give `e^{s}`, which is `e`. Since `e^{2s}>=1+2s+2s^2+(4/3)s^3`, the window under-reads **every** negative atom (`kernel_negative_atom_misread`).
- **The sign convention matters.** The mutation `theta->-theta` computes `∫ghat(-theta)c_0(theta)dtheta=g(-3)/4=25e^{-3}/4` at `s=1` (`window_fourier_sign_convention`).
- **The window must equal the heat function on all of `[0,inf)`,** including a neighbourhood of 0, because only AQ1's `G>=0` is used. A window matched only above an assumed gap is rejected (`kernel_identity_on_support`).

## 3. Constants by half-line transforms (item 2)

**Transform.** Put `a=s-i theta` and `b=s+i theta`, so `Re a=Re b=s>0`, `a+b=2s` and `ab=s^2+theta^2`. On `x>=0`, `∫_0^inf e^{-bx}dx=1/b`. On `x<0`, substitute `y=-x` and use `∫_0^inf y^n e^{-ay}dy=n!/a^{n+1}`. This gives

\[
 2\pi\hat g(\theta)=\frac1b+\frac1a+\frac{2s}{a^2}+\frac{4s^2}{a^3}
 =\frac{b(a^2+2sa+4s^2)+a^3}{a^3b}.
 \tag{HNM-AV2-F09}
\]

Since `b=2s-a`, `(2s-a)(a^2+2sa+4s^2)=8s^3-a^3`. The numerator therefore collapses to the constant `8s^3`, and

\[
 \hat g(\theta)=\frac{4s^3}{\pi(s-i\theta)^3(s+i\theta)} .
 \tag{HNM-AV2-F10}
\]

As a check, `ghat(0)=4/(pi s)=||g||_1/(2pi)`, which must hold because `g>=0`.

**Why the `theta^-2` and `theta^-3` terms cancel.** Take the general left polynomial `1+c_1y+c_2y^2` for `y=-x>0`. The same half-line calculation gives

\[
 2\pi\hat g\cdot a^3b=(2s-c_1)a^2+(2sc_1-2c_2)a+4sc_2 .
\]

Divided by `a^3b`, which is of order `theta^4`, the three terms produce the three decay rates.
- The `a^2` term makes `ghat` decay like `theta^-2`. It vanishes exactly when `c_1=2s`, which is the **C¹ matching** `g'(0-)=s-c_1=-s`.
- The `a` term makes `ghat` decay like `theta^-3`. It vanishes exactly when `c_2=sc_1=2s^2`, which is the **C² matching** `g''(0-)=s^2-2sc_1+2c_2=s^2`.
- With both matchings only the constant `8s^3` survives, so `ghat` decays like `theta^-4`.

Two members of the family are useful checks.
- The Poisson kernel is the case `c_1=c_2=0`, the kink `e^{-s|x|}`. It leaves `2s a^2/(a^3b)`, so `ghat=s/(pi(s^2+theta^2))`. Its `theta^-2` tail is exactly why its absolute first moment diverges (Section 6).
- The C¹ window, `c_1=2s` and `c_2=0`, leaves `4s^2a/(a^3b)`, so `ghat=2s^2/(pi a^2 b)`.

The checker verifies the numerator identity as a polynomial identity in `a`. It also evaluates it in exact Gaussian rationals at 7 values of `theta`, 4 values of `s` and 4 left polynomials.

**Modulus and parts.** Since `|a|=|b|=(s^2+theta^2)^{1/2}` and `1/(a^3b)=b^2/(s^2+theta^2)^3`,

\[
 |\hat g(\theta)|=\frac{4s^3}{\pi}(s^2+\theta^2)^{-2},\qquad
 \operatorname{Re}\hat g=\frac{4s^3}{\pi}\frac{s^2-\theta^2}{(s^2+\theta^2)^3},\qquad
 \operatorname{Im}\hat g=\frac{4s^3}{\pi}\frac{2s\theta}{(s^2+\theta^2)^3}\ (\text{odd}).
 \tag{HNM-AV2-F11}
\]

**Moments by exact antiderivatives.** Write `F=R+B·arctan(theta/s)` with `R` rational and `arctan'(theta/s)=s/(s^2+theta^2)`. The four antiderivatives are:

| integrand | antiderivative `F` |
|---|---|
| `(s^2+theta^2)^-2` | `theta/(2s^2(s^2+theta^2)) + arctan(theta/s)/(2s^3)` |
| `theta(s^2+theta^2)^-2` | `-1/(2(s^2+theta^2))` |
| `theta^2(s^2+theta^2)^-2` | `-theta/(2(s^2+theta^2)) + arctan(theta/s)/(2s)` |
| `(s^2-theta^2)(s^2+theta^2)^-3` | `theta/(2(s^2+theta^2)^2) + theta/(4s^2(s^2+theta^2)) + arctan(theta/s)/(4s^3)` |

The rational parts vanish at `±inf`, and the arctangent contributes `B·pi` over the whole line. Hence

\[
 M_0=\|\hat g\|_1=\frac{4s^3}{\pi}\cdot\frac{\pi}{2s^3}=2,\qquad
 M_1=\int|\theta||\hat g|=\frac{4s^3}{\pi}\cdot\frac1{s^2}=\frac{4s}{\pi},\qquad
 M_2=\int\theta^2|\hat g|=\frac{4s^3}{\pi}\cdot\frac{\pi}{2s}=2s^2,
 \tag{HNM-AV2-F12}
\]

and `∫ghat dtheta = (4s^3/pi)·pi/(4s^3) = 1 = g(0)`, which is inversion at `x=0`. Note that `∫ghat=1` while `∫|ghat|=2`: `ghat` is complex, not a positive mass-one kernel. Charging the state term with mass one, as for the Poisson kernel, would under-charge it by half. The `kernel_l1_and_first_moment` control rejects that mutation.

The checker verifies each `F'=f` as an exact rational-function identity at `s` in `{1/2,1,2,7/3}`. It then reads the integrals off as exact multiples of powers of `pi`. The scaling `|ghat_s(theta)|=s^{-1}|ghat_1(theta/s)|` is also checked: `M_0` is independent of `s`, `M_1` is proportional to `s`, and `M_2` to `s^2`.

**Directed pi.** Machin's formula `pi=16 arctan(1/5)-4 arctan(1/239)` with 80-term consecutive alternating brackets, rounded outward to `10^-40`, gives

`pi in [3.1415926535897932384626433832795028841956, 3.1415926535897932384626433832795028841976]`,

so `4/pi in [1.27323954473516268615, 1.27323954473516268616]`. Every certified quantity that divides by `pi` uses the lower bound.

**Numerical preview (not admission).** At `s=1`, a midpoint rule on `[0,200]` with step `1/20`, plus leading tails, gives `M_0≈2.0000001`, `M_1≈1.2735051` (against `4/pi≈1.2732395`) and `M_2≈2.0000003`. These are labelled previews in `results.json` and decide nothing.

## 4. Real-time comparison (item 3)

This section is inherited from AT4 F10–F12 and restated here with its domain argument. Fix a centered whole-star box `Lambda_N`, `N>=2`, and split

\[
 G_N=A_N+B_N,\qquad A_N=G_{0,R}\otimes1+1\otimes G_{\rm outside,N},\qquad
 B_N=\sum_{b\in R-S}V_b,\qquad \|B_N\|\le7\cdot\frac{7|\tau|}8=\frac{49|\tau|}8 .
 \tag{HNM-AV2-F13}
\]

The pieces are:
- `V_b=phi_b/8` is a whole star in `G=H/alpha` units, with `||V_b||<=7|tau|/8`;
- all seven stars meeting `R` are assigned in full to `B_N`, even where some of their faces act only outside;
- `G_outside,N` contains every other onsite term and every interaction disjoint from `R`.

**Domains.** `A_N` is self-adjoint: it is a finite sum of compact-group Casimir operators plus bounded interactions disjoint from `R`. `B_N` is bounded, so `G_N` is self-adjoint on `D(G_N)=D(A_N)`.

**Relative unitary.** Let `U(theta)=e^{i theta G_N}e^{-i theta A_N}`. For `psi` in `D(A_N)`, `e^{-i theta A_N}psi` stays in `D(A_N)=D(G_N)` and is norm-differentiable. The product rule for a uniformly bounded, strongly continuous group, differentiable on its domain, then gives the bounded, strongly continuous derivative

`dU(theta)psi/dtheta = i e^{i theta G_N} B_N e^{-i theta A_N} psi`.

Integrate vectorwise: `||U(theta)psi-psi|| <= |theta| ||B_N|| ||psi||`. By density and boundedness, `||U(theta)-I|| <= |theta| ||B_N||`.

Only **after** this estimate is the bounded `W` inserted. Since `alpha^N_theta(W)=U(theta) alpha^A_theta(W) U(theta)*` and `alpha^A_theta(W)=alpha^0_theta(W)⊗1` (the two tensor factors commute strongly),

\[
 \|\alpha^N_\theta(W)-\alpha^0_\theta(W)\|\le\|(U-I)XU^*\|+\|X(U^*-I)\|\le2|\theta|\|B_N\|\le k|\theta|,\qquad k=\frac{49|\tau|}4,
 \tag{HNM-AV2-F14}
\]

where `X=alpha^0_theta(W)` has norm at most 1. The following cautions apply.
- No domain invariance of arbitrary bounded local operators is assumed, and no norm-Bochner derivative is claimed.
- The factor 2 is needed. The exact fixture `U=diag(u, conj u)` with `u=(3+4i)/5` and `X=sigma_x` gives `||UXU*-X||^2/||U-I||^2=16/5`.
- The estimate is local: the seven incident stars are counted for `N=2,3,4`. The extensive norm over `(2N)^3` stars would make the slope depend on `N`, and the checker rejects it.

AQ1 supplies norm convergence of the finite-box bounded-local dynamics on compact `theta` intervals, and the free evolution is the same local operator in every box. So (F14) holds for the actual AQ evolution at **every real** `theta`.

**Comparison.** Add and subtract the free evolution inside the actual state, then the local reference state. The operator `W alpha^0_theta(W)` lies in `B(H_R)` and has norm at most 1. Hence

\[
 |c(\theta)-c_0(\theta)|
 \le|\omega(W[\alpha_\theta(W)-\alpha^0_\theta(W)])|+|\operatorname{Tr}[(\rho_R-P_R)W\alpha^0_\theta(W)]|+m^2
 \le k|\theta|+D+m^2\le k|\theta|+D+D^2 .
 \tag{HNM-AV2-F15}
\]

The state term uses full trace duality, `D`. The effect refinement `D/2` of AT4 F09 is **not** applied. `W alpha^0_theta(W)` has free expectation `e^{3i theta}/4`, which is non-real at `theta=pi/6`, so the operator is not self-adjoint and not an effect. The exact `2×2` fixture `Delta=diag(1/2,-1/2)`, `X=diag(1,-1)` shows `|Tr(Delta X)|=||Delta||_1>||Delta||_1/2` (`state_term_not_effect`).

## 5. Radius, datum and target (items 4 and 10)

Subtract (F08) from (F07) and integrate (F15) against `|ghat|`:

\[
 \Bigl|C(s)-\tfrac14e^{-3s}\Bigr|\le\int|\hat g|\,(k|\theta|+D+D^2)\,d\theta
 =M_0(D+D^2)+kM_1=2(D+D^2)+\frac{49|\tau|s}{\pi}=:E(s).
 \tag{HNM-AV2-F16}
\]

Every real `theta` is integrated: there is **no cutoff and no tail**. Enclose `e^{-3}/4` as `[f^-,f^+]`, using the alternating Taylor brackets `P_41<=e^{-z}<=P_40` on `[0,1/2]`, three halvings of `3`, and outward squaring to `10^-40`. Then export

\[
 d=\frac{f^-+f^+}2,\qquad r_{\rm arith}=\frac{f^+-f^-}2,\qquad r=E^+(1)+r_{\rm arith},\qquad C_\tau(1)\in[d-r,d+r],
 \tag{HNM-AV2-F17}
\]

where `E^+` uses `pi^-` in `kM_1`. Then `|d-C_tau(1)|<=|d-e^{-3}/4|+|e^{-3}/4-C_tau(1)|<=r` exactly.

At `tau=+10^-8` and `s=1`, with `k=49/400000000`, the itemized terms are below. Decimals are rounded **up**, and the exact rationals are in `results.json`.

| term (preregistered name) | exact rational | outward decimal |
|---|---|---:|
| `state` = `M_0 D` | `1170159676931825184288274812132100/42981220507576537932303142777593983768257` | `2.72249057406e-8` |
| `mean_square` = `M_0 D^2` | exact in `results.json` | `3.70597746291e-16` |
| `kernel_dynamics` = `k M_1^+` = `49|tau|/pi^-` | `1225000000000000000000000000000000/7853981633974483096156608458198757210489` | `1.55971844231e-7` |
| `arithmetic` (half-width of the `e^{-3}/4` enclosure) | `1/(4·10^40)` | `2.5e-41` |
| **complete radius `r`** | exact in `results.json` | **`1.83196750342e-7`** |

The remaining quantities are:
- the datum `d=0.012446767091965985744835603912515444157925`, exact;
- the interval `[0.01244658389521564455, 0.01244695028871632694]` (lower endpoint rounded down, upper rounded up), of width `2r≈3.66393500683e-7`;
- the free enclosure `[f^-,f^+]`, of width `5·10^-41`, lying inside it.

**Boolean.** `r<=1/1000000` is `true`, with ratio `10^-6/r>=5.4586121`. The contract preview "about 1.83e-7" agrees to `10^-9`.

**Mirrored coupling.** `certify(tau=-1/100000000, fixed_design=True)` returns the identical datum and radius, because every term depends only on `|tau|`. It is a replay of the certificate, not a second confirmation.

The interval is not clipped. Positivity `C(1)>=0` and `C(1)<=omega(W^2)<=1/4+D/2` are inactive here.

**Unused refinement.** Because `∫ghat=g(0)=1` exactly, the constant `m^2` in `c` could be charged once instead of `M_0 m^2`. This would save about `1.9e-16`. It is not used: the contract formula is frozen.

## 6. Retained failures (item 5)

All values below are at unchanged `tau=10^-8`, `s=1`, with directed `pi`, `log` and `sqrt`.

**AT4 Poisson certificate at `L=10^4`.** With `D_AT4=2 sqrt(49|tau|/3)`, the AT4 F16 radius

\[
 D+D^2+\frac{ks}{\pi}\log(1+L^2/s^2)+\Bigl(\frac12+\frac D2\Bigr)\frac{2s}{\pi L}
 \tag{HNM-AV2-F18}
\]

lies in `[8.41518704386e-4, 8.41518704387e-4]`. This matches the frozen AT4 decimal `0.000841518704386267` to `10^-15`. It fails `10^-6` and is retained as insufficient.

**Optimized Poisson floor.** Take `D->0`, keeping the forward tail `s/(pi L)`. For **every** `L>0`, since `log(1+L^2/s^2)>=2log(L/s)`,

\[
 \frac{ks}{\pi}\log\Bigl(1+\frac{L^2}{s^2}\Bigr)+\frac{s}{\pi L}\ \ge\ \frac s\pi\Bigl[2k\log\frac Ls+\frac1L\Bigr]\ \ge\ \frac{2ks}{\pi}\Bigl(1+\log\frac1{2ks}\Bigr).
 \tag{HNM-AV2-F19}
\]

The middle bracket is minimized at `L=1/(2k)` (one sign change of `2kL-1`). Directed evaluation gives:
- the lower bound `1.265088223e-6`;
- the value at `L=4081633`, which is at most `1.265088224e-6`.

The floor is therefore enclosed in `[1.265088223e-6, 1.265088224e-6]`, at `L≈4.08e6`, which matches the contract's `~1.2651e-6`. With the admitted `D` added, the Poisson certificate cannot fall below `1.278700676e-6`. **No choice of `L` meets `10^-6`** at `s=1`, and this insufficiency is retained.

**Divergent Poisson first moment against the window's finite one.** The Poisson member of the general family (`c_1=c_2=0`) has a kink, `g'(0-)=s` against `g'(0+)=-s`, and a nonzero `a^2` coefficient `2s`. Its partial absolute first moment is

\[
 \int_{-L}^{L}|\theta|\frac{s}{\pi(s^2+\theta^2)}d\theta=\frac s\pi\log\Bigl(1+\frac{L^2}{s^2}\Bigr)\ge\frac{2s}\pi\log\frac Ls\ \xrightarrow{L\to\infty}\ \infty .
 \tag{HNM-AV2-F20}
\]

Directed lower bounds at `s=1`:

| `L` | partial first moment, at least |
|---|---:|
| `10^4` | `5.8634847` |
| `10^8` | `11.726969` |
| `10^16` | `23.453939` |
| `10^32` | `46.907878` |

The window's full moment is `M_1=4/pi≈1.2732396`, and the Poisson partial moment already exceeds it at `L=8`, since `log 65>4`. At `L=10^32`, the Poisson dynamics term `k·(partial moment)` alone is at least `5.74621e-6>10^-6`. Extending `k|theta|` over the whole Poisson kernel therefore has no finite value, which is the AT4 reason for the cutoff and its tail. The window removes both.

**Tier-(i) window.** With `D_i≈2.36803504624e-5`, the window radius is at least `4.751667276e-5`. It fails `10^-6` and is retained as the limited-tier value. It is not the bound premise.

## 7. Crossover (item 6)

`E(s)=2(D+D^2)+(49|tau|/pi)s` is linear in `s`. Solving `E(s*)=10^-6` with `pi^∓`,

\[
 s^*\in[6.236863446033,\ 6.236863446034],\qquad E^+(s^{*-})=E^-(s^{*+})=10^{-6}\ \text{exactly}.
 \tag{HNM-AV2-F21}
\]

This lies inside the contract's "about 6.1–6.3". For orientation, the analytic radius is `1.0521e-7` at `s=1/2`, `3.3917e-7` at `s=2`, `9.6306e-7` at `s=6`, and more than `1.99916e-5` at `s=128`.

**No node other than `s=1` is evaluated or certified.** The preregistration forbids post-hoc node selection. `grid_claim` is false, and there is **no `[0,128]` claim at the cap**.

## 8. Free reference inside: no resolved shift (item 7)

The exact free enclosure `[f^-,f^+]` lies inside `[d-r,d+r]`, so the free value is not excluded. The result carries `reference_unresolved`, and `resolved_interaction_shift` is false. Centering the interval on the computable free value does not set the interacting correlation equal to it. Conversely, a radius of `1.83e-7` at `tau=10^-8` detects no interaction effect. The centered shift is expected to be `O(tau^2)` (triage (c)3), but that expectation is an AW1 target and is not used or claimed here.

## 9. Calculator (item 8)

`calculator.py` exports `certify(...)` in the AT5 style.
- **Inputs.** It accepts exact inputs only: integers, `Fraction`s, exact decimal strings and `p/q` strings. Binary floats, Booleans, NaN, Infinity, empty strings, zero denominators, malformed ratios and other objects are rejected.
- **Domain.** The selected triple must be exactly zero, rational `|tau|<=10^-8`, `s>0`, target `>0`, and `alpha`, `hbar`, `E_star` and the lattice spacing positive.
- **State bound.** `D` is **not an input**. It is computed by `av1_tier_ii_D(|tau|)`, the admitted AV1 forward tier-(ii) formula. `state_tier` must be `av1_forward_tier_ii`, and passing any other tier or a `D` keyword is rejected (`av1_tier_bound`).
- **Kernel.** `window` must be `C2`. A kernel switch is rejected.
- **Fixed design.** `fixed_design=True` enforces `|tau|=10^-8`, `s=1` and target `10^-6`. The negative sign is allowed and flagged `mirrored_coupling_replay`.
- **Zero coupling.** There is **no zero-coupling branch**. At `tau=0`, `D=k=0` and the radius equals the arithmetic term alone (`tau_zero_null_replay`).
- **Returns.** The datum, radius, interval, the four itemized costs, `M_0`, `M_1^±`, `M_2`, the `pi` bracket, `physical_Euclidean_time=hbar s/alpha`, `sub_label: reference_unresolved`, and false claim flags (`uniform_wilson_claim`, `continuum_claim`, `grid_claim`, `state_uniqueness_claim`, `scientific_priority_verified`).

`c1_window_preview(...)` is labelled `preview_only: true, used_for_certificate: false`. For the C¹ window `g=e^{sx}(1-2sx)` (`x<0`) it returns:
- `ghat=2s^2/(pi a^2 b)` and `|ghat|=(2s^2/pi)(s^2+theta^2)^{-3/2}`;
- `M_0=4/pi`, `M_1=4s/pi`, and `M_2` infinite, since the partial `M_2` at `L=10^8` already exceeds 6.51 and grows like `2^{-3/2}log L`;
- the negative-atom value `3/e` and the sign-mutation value `7e^{-3}/4`;
- the preview radius `1.733037578e-7`.

The C¹ window was registered before production as a preview. Switching to it after `D` is known is rejected, and its infinite `M_2` would also block the second-order refinement.

```python
from calculator import certify, c1_window_preview
r = certify(fixed_design=True)                 # tau=+10^-8, s=1: r['target_met'] is True
m = certify(tau='-1/100000000', fixed_design=True)   # mirrored-coupling replay, same radius
z = certify(tau='0')                           # radius == costs['arithmetic']
p = c1_window_preview()                        # preview only, never a certificate
```

## 10. Executed controls (item 9; 50 checks)

Every contract control is an exception-raising damaging mutation, recorded under `rejected_mutations` in its check. The checker requires this for all 24 ids and never uses `assert`.
- **`kernel_identity_on_support`:** `g=e^{-sx}` at sampled `x>=0` (including `x=1/32`), and `g(3)=e^{-3s}` on the free atom. The fixtures `eta_A` and `eta_B` read exactly. Rejected: a symmetric window, and a window matched only above the AQ2 gap.
- **`kernel_negative_atom_misread`:** `g(-1)=5/e<e` by directed enclosures. Rejected: admitting a negative atom.
- **`kernel_l1_and_first_moment`:** `M_0=2` and `M_1=4s/pi` at four values of `s`. Rejected: a positive mass-one kernel, the signed integral `∫ghat=1` used as the `L^1` norm, and `M_1` without `s`.
- **`poisson_kink_divergence`:** the kink and the `a^2` coefficient. Rejected: the window formula applied to the Poisson kernel, and a finite full-line Poisson Duhamel term.
- **`window_linear_in_s`:** `E(s)=A+Bs` exactly at `s=1/2,1,2,6`, plus the scaling identity. Rejected: a node at `s=7` using the `s=1` radius (post-hoc node selection), and a dropped dynamics term.
- **`local_not_extensive_duhamel`:** 7 incident stars for `N=2,3,4`, against 64, 216 and 512 retained, plus the conjugation fixture. Rejected: the extensive norm, and a dropped factor 2.
- **`tau_zero_null_replay`:** the window radius at `tau=0` is the arithmetic term alone. The Poisson radius at `tau=0` keeps `s/(pi L)`, `3.18e-5` at `L=10^4` and `3.18e-10` at `L=10^9`. Rejected: a `±3/(2·10^30)` Poisson criterion at both `L`, and a fictitious window tail.
- **`window_fourier_sign_convention`:** rejected: `theta->-theta`, which gives `25e^{-3}/4`.
- **`state_term_not_effect`:** rejected: the `D/2` state term.
- **`av1_tier_bound`:** `D` equals both the contract and the gate. Rejected: tier (i), the AT4 square root, the reverse 82-face refinement as a post-freeze switch, and the calculator given tier (i), the AT4 bound or a supplied `D`.
- **`reverse_premise_isolation`:** a positive check that the contract declares `reverse_premise_isolation: true`. The forward inventory is exactly AGENTS, the contract, the shared premises and the forward-additional premises (30 files). The reverse list (27) contains no forward-additional premise. Rejected: a reverse list containing `triage.md`, or the forward AV2 report.
- **`c1_window_preview_only`:** the C¹ identities and the values `3/e` and `7e^{-3}/4`. Rejected: a kernel switch in the packet, and C¹ or Poisson certificates in the calculator.
- **`missing_incoming_stars`:** rejected: the orthant count 2, and the truncated `N=1` box (4).
- **`full_original_wilson_cover`:** owners `0,0,e_z,0`, 48 links, 36 endpoints (22 per factor, 8 shared). Rejected: the four drawn links.
- **`wrong_delta_alpha_hbar_clock`:** energies 3 (G units) and 24 (normalized), `3s=24u`, and the non-unit fixture `alpha=5`, `hbar=7`, `t_E=3/2`. Rejected: exponent 24 with `s`, and the normalized star norm in the G clock.
- **`vector_versus_scalar_centering`:** residues `1/10000`, `-51/10000` and `1/16`. Rejected: scalar subtraction used as vector centering.
- **`first_order_mean_charged`:** `M_0D^2>0` is charged. Rejected: assuming zero mean.
- **`tau_scaling_exponent`:** `E(10^-8)/E(10^-10)≈100.0015`, which lies in `[99,101]`. Rejected: the square-root `D` radius (ratio `≈10.0008`) relabelled as linear.
- **`changed_model_relabelled`:** 8 relabellings rejected: `tau=10^-14`, `s=1/2`, a nonzero triple, the selected-strip reference, a finite graph, the C¹ kernel, the Poisson kernel, and a finite-volume state.
- **`coherent_evidence_tampering`:** 7 edits rejected after the packet hash is rebound: a control Boolean flipped, a snapshot removed, the radius halved, the tier-(i) `D`, the AT4 Boolean flipped, the grid flag set, and a kernel switch.
- **`insufficient_verdict_retained`:** the AT4, floor and tier-(i) failures are retained. Rejected: relabelling AT4 as met, and retuning `tau` to the Poisson threshold.
- **`exact_arithmetic_admission`:** no numerical-library imports. Rejected: float, bool, NaN and zero-denominator inputs, in both the checker and the calculator.
- **`root_n_misuse`:** the radius is the linear sum. Rejected: the root sum of squares (`1.583e-7`), division by `sqrt 4`, and division by 64.
- **`no_priority_or_continuum_claim`:** each of the five false flags, when set true, is rejected, as is flipping `euclidean_node_certified` against the radius.

The remaining 26 checks are positive exact checks:
- contract hash;
- C² matching;
- the half-line transform identity;
- `theta`-power cancellation;
- the modulus;
- the antiderivatives;
- the exact constants;
- inversion at the origin;
- Machin `pi`;
- the labelled numerical preview;
- the AV1 bound recomputation;
- the seven-star slope;
- the itemized radius;
- the mirrored replay;
- the target Boolean;
- the free reference inside;
- the datum and arithmetic;
- preview consistency;
- the AT4 radius;
- the Poisson floor;
- the divergence exhibit;
- the crossover;
- three calculator checks (fixed design, 28 domain rejections, exact input forms);
- the preregistered error-term names.

**Claim flags** are `continuum_claim:false`, `uniform_wilson_claim:false`, `resolved_interaction_shift:false`, `scientific_priority_verified:false`, `grid_claim:false` and `euclidean_node_certified:true`. The last flag is true because `r<=10^-6` for this forward certificate; admission needs the reverse route and review. Every number in `results.json` is a string.

## 11. Error ledger (preregistered `state`, `mean_square`, `kernel_dynamics`, `arithmetic`)

- **`state`:** `M_0 D`, using the AV1 tier-(ii) trace-distance bound and trace duality against the non-effect `W alpha^0_theta(W)`.
- **`mean_square`:** `M_0 m^2<=M_0 D^2`.
- **`kernel_dynamics`:** `kM_1=49|tau|s/pi`, with the `pi` lower bound, integrated over all `theta`. There is no cutoff or tail term to itemize.
- **`arithmetic`:** the half-width of the `e^{-3}/4` enclosure about the rational datum. The `pi` rounding is already inside `kernel_dynamics^+`.

No entry is `not_applicable`.

## 12. Scope, exclusions, limitations and incomplete steps

**Claim exclusions (contract, verbatim):**
- resolved interaction shift (free value inside)
- full [0,128] grid at the cap
- uniform Wilson magnetic theory
- AQ uniqueness or a rate in N
- continuum construction
- scientific priority
- the second-order Dyson refinement
- any shift of C(s)

**Preregistered claim exclusions (verbatim):**
- free reference inside enclosure => no interaction claim
- uniqueness of the AQ state
- whole-sequence convergence or rate in N
- continuum or weak coupling
- transfer from a finite graph
- relabelling a static shift as dynamical
- scientific priority

**Producer limitations and incomplete steps:**
1. **Forward half only.** The reverse residue route (simple pole at `theta=is`, triple pole at `theta=-is`) was not executed; it is assigned to the reverse producer. The contract's `accepted_within_scope` needs both routes and review.
2. **Shared window premise.** The window, its transform and its constants are a shared panel premise, and this producer read the skeptic's sketch. Independence covers only the derivation route, the code and the controls.
3. **Inherited without re-proof.** The following are inherited:
   - AQ1's construction, local trace-norm convergence, norm dynamics convergence on compact intervals and `H>=0`;
   - AT4's seven-star Duhamel comparison (restated with its domain argument);
   - AV1's `D` and its passage to every AQ1 subsequential limit;
   - the I1/AM2 model dictionary.

   The certificate holds for every state that AQ1's construction yields, without uniqueness, whole-sequence convergence or a rate in `N`.
4. **What the checker does not verify.** The Fourier inversion theorem is cited, not machine-checked. The checker verifies the transform algebra, the modulus, the antiderivatives and inversion at `x=0` exactly. Fixtures and previews are audits, not proofs of the infinite-dimensional statements.
5. **Upper certificate only.** `r` bounds the error of `d`. It is not a lower bound on `|C(1)-e^{-3}/4|`, and it says nothing about the sign or size of any interaction effect.
6. **Single node.** Only the node `s=1` is certified. The crossover `s*` describes the analytic formula, not evaluated nodes.
7. **Model scope.** Nothing transfers to nonzero selected triples (non-Haar `P_R`), uniform Wilson theory, weak coupling or the continuum.

**Methodological lenses.** Newton's analysis before synthesis is followed: the Poisson floor is analyzed back to the kink of `e^{-s|x|}`, that is, to the `a^2` coefficient of the transform numerator, before the C² window is synthesized. Tesla's complete accounting is followed too: all seven stars, the whole real-time axis, both centering costs and the arithmetic radius are charged. These are modern methodological uses of the snapshotted skills. No historical figure participates in or endorses this work, and no occult or historical material supplies a premise.

## 13. Reproduction

Output directories must be fresh, absolute and outside the checkout:

```bash
python3 -B research/round32/forward/av2/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/forward/av2/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/forward/av2
```

`check.py` does the following, in order:
- it verifies the contract snapshot's sha256 and reads the tau, s, target, `D`, window, constants, slope, retained values and crossover window from it, and the admitted `D` and tier values from the AV1 gate snapshot;
- it records its own sha256 and the calculator's before evaluation;
- it writes `results.json` (50 checks, sorted keys, string numbers) and `source-manifest.json`, which binds the report, the checker, the calculator and all 30 input snapshots.

`freeze.json` binds the whole producer closure. The producer directory contains no interpreter cache.
