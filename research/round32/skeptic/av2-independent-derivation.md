# AV2 independent derivation before producer comparison

**Standing.** I wrote this after the AV2 contract froze (`frozen_at` 2026-09-23T22:10:41Z, sha256 `686458ca…5687`) and before opening, listing or reading `research/round32/forward/av2/` or `research/round32/reverse/av2/`. Sources: the frozen contract, `advisor/av1-gate.json`, `selection-av2.md`, my own `triage.md`, `loop2-response.md`, `loop3-signoff.md`, `av1.md` and `av1-independent-derivation.md`, AT4 forward §1–6 and the AT5 `calculator.py` primitives. I am a model-agent skeptic with correlated ancestry: the advisor, lenses and producers share my model family, and my triage proposed this window. So this is neither human peer review nor an independent discovery. Exact values come from `av2_check.py` (`av2-independent/results.json`, 69 checks, 24 contract controls). Every decimal is a preview. Human project author: Hruday N M (BUNZEEY).

**Route chosen: annihilator and jump, then Wallis.** Neither producer contract uses this route. The forward contract prescribes half-line transforms and the reverse contract prescribes residues. I get the transform from the differential operator that kills both branches of `g` and the single jump it leaves at `x=0`. I get the moments from `theta=s tan(phi)` and exact Wallis integrals, with a directed rational Riemann enclosure as a cross-check. The half-line formula is evaluated only as a comparator.

## 1. Conventions and the window lemma
Frozen conventions: `c(theta)=<chi,e^{i theta G}chi>` and `ghat(theta)=(2pi)^{-1} int g(x)e^{-i theta x}dx`, so that `g(x)=int ghat(theta)e^{i theta x}dtheta`. Here `chi=(pi(W)-m)Omega`, `m=omega(W)` and `G=H_phys/alpha`. Then `c(theta)=omega(W alpha_theta(W))-m^2`, and `c_0(theta)=e^{3i theta}/4` (AT4 F06, `m_0=0`).

**Hypotheses on g.** (a) `g` is continuous, since the C^2 matching at 0 is checked exactly. (b) `g` is in `L^1`: `||g||_1=1/s+7/s=8/s`. (c) `g(x)->0` as `|x|->inf`. (d) `g(x)=e^{-sx}` for every `x>=0`, `x=0` included.

**Hypothesis on ghat.** `|ghat|=(4s^3/pi)(s^2+theta^2)^{-2}`, so `ghat` is in `L^1` with `||ghat||_1=2`.

**Hypotheses on the measure.** `eta` is the spectral measure of `chi` for `G`. It is positive and finite, `eta(R)=||chi||^2<=1`. It is carried by `[0,inf)` because the AQ1 generator is nonnegative. Neither the AQ2 gap nor `[1/16,inf)` is used, and an atom at 0 is harmless because `g(0)=1=e^0`.

**Proof.**
1. **Inversion.** By the L^1 Fourier inversion theorem, `g` agrees a.e. with the continuous function `x->int ghat(theta)e^{i theta x}dtheta`. Both are continuous, so they agree at every `x`. Continuity alone gives the inversion; C^2 only buys the decay of `ghat`.
2. **Spectral form.** By the spectral theorem, `c(theta)=int e^{i theta x}d eta(x)`. The function `c` is continuous by dominated convergence.
3. **Fubini.** Tonelli gives `int int |ghat(theta)| d theta d eta = 2||chi||^2 < inf`, so the order of integration may be exchanged: `int ghat c dtheta = int (int ghat e^{i theta x}dtheta) d eta = int g d eta`.
4. **Nonnegativity.** `int g d eta = int_{[0,inf)} e^{-sx} d eta = <chi,e^{-sG}chi> = C(s)`. This is the only place AQ1 nonnegativity enters. With mass on `x<0` the window reads `g(x)`, not `e^{-sx}` (section 7).
5. **Free reference.** For the free atom `eta_0=delta_3/4`, `C_0(s)=g(3)/4=e^{-3s}/4`.

The two correlation functions are integrated against the same `ghat`, so `|C(s)-C_0(s)| <= int |ghat||c-c_0|`.

## 2. Transform by the annihilator–jump route
**Operator and jumps.** The left branch is `e^{sx}p(x)` with `p=1-2sx+2s^2x^2` (`d=deg p=2`). Take `P(D)=(D+s)(D-s)^{d+1}`. It kills `e^{-sx}` because `P(-s)=0`. It kills `e^{sx}p` because `(D-s)(e^{sx}q)=e^{sx}q'`; the checker verifies this at `d+3` points. Distributionally, `P(D)g=sum_r kappa_r delta^{(r)}` with `kappa_r=sum_{n>r} a_n J_{n-1-r}`, where `J_n=g^{(n)}(0+)-g^{(n)}(0-)`. The exact jumps are `J_0=J_1=J_2=0` and `J_3=-s^3-7s^3=-8s^3` (`g'''(0-)=s^3-6s^3+12s^3`). Hence `P(D)g=-8s^3 delta`.

**Transform.** Fourier transform gives `P(i theta)ghat=-8s^3/(2pi)`, and `P(i theta)=-(s+i theta)(s-i theta)^3` has no real zero. So

`ghat(theta) = 4s^3/(pi(s-i theta)^3(s+i theta))`, `|ghat| = (4s^3/pi)(s^2+theta^2)^{-2}`.

**Exact checks.**
- Gaussian-rational equality with the contract's formula at 21 `(s,theta)` pairs.
- Equality with the half-line comparator `2pi ghat=1/(s+i theta)+1/a+2s/a^2+4s^2/a^3`, where `a=s-i theta`.
- `pi ghat(0)=||g||_1/2=4/s`.

**The same route for the other two kernels.** Poisson (`p=1`) gives `J_1=-2s`, a kink, and `s/(pi(s^2+theta^2))`, which is AT4 F14 with the same convention. The C^1 window (`p=1-2sx`) gives `J_2=4s^2` and `2s^2/(pi(s-i theta)^2(s+i theta))`. The smoothness class `d` fixes the decay: `|ghat| ~ |theta|^{-(d+2)}`.

## 3. Moments (Wallis) and a directed cross-check
Substitute `theta=s tan phi`. Then `M_j=int|theta|^j|ghat| = (c/pi) s^j W(j,d-j)`, where `c=|kappa_0|/s^{d+1}` and `W(a,b)=int_0^{pi/2} sin^a cos^b`. `W` is infinite for `b<0`.

| Kernel | `M_0` | `M_1` | `M_2` |
|---|---|---|---|
| C^2 (`c=8`) | **2** | **4s/pi** | **2s^2** |
| C^1 (`c=4`) | 4/pi | 4s/pi | infinite |
| Poisson (`c=2`) | 1 | infinite (`W(1,-1)`) | infinite |

All nine entries are exact symbolic outputs, and the C^2 row equals the contract text.

**Cross-check at s=1.** Cellwise monotone rational bounds on `[0,64]`, plus a two-sided tail, give `M_0 in [1.99873,2.00128]`, `M_1 in [1.27108,1.27540]` (`4/pi=1.27324`) and `M_2 in [1.99601,2.00400]`.

## 4. Real-time comparison with the admitted D
**Slope.** `R={0,e_z}` and `R-S` has seven anchors (the orthant count is 2). The cover is 48 links and 36 endpoints, and the Wilson owners are `0,0,e_z,0`. Each star has norm `21·|tau|/3·1/8=7|tau|/8` in `G=H/alpha` units. So `||B_N||<=49|tau|/8`. The relative-unitary Duhamel estimate (AT4 F10–F11) gives `||alpha_theta(W)-alpha^0_theta(W)||<=2|theta|||B_N||=k|theta|`, with `k=49|tau|/4` for every real `theta`, independent of the box. An extensive norm would grow like `(2N)^3`.

**Bound on the difference.** Add and subtract `omega(W alpha^0_theta W)`, then use trace duality on `R`:

`|c-c_0| <= k|theta| + |Tr[(rho_R-P_R)W alpha^0_theta(W)]| + m^2 <= k|theta| + D + D^2`.

**Where D and m^2 come from.** `D` is the gate-bound forward tier (ii), `585079838465912592144137406066050/42981220507576537932303142777593983768257` (~1.36125e-8). It is recomputed from the AV1 formula at both signs and equals the contract and gate strings. `m^2<=D^2` because `|m|<=D`; AV1 does not exclude a first-order mean, so it is charged.

**No effect refinement.** `W alpha^0_theta(W)` is a complex contraction, not an effect, so the D/2 refinement does not apply. A labelled 2x2 toy shows this: `A=diag(u,conj u)`, `u=(3+4i)/5`, and `Delta=(D/2)diag(1,-1)` give `|Tr(Delta A)|=4D/5>D/2`.

## 5. Radius at the cap (tau=+10^-8, s=1)
`E = M_0(D+D^2) + k M_1 = 2D + 2D^2 + 49|tau|s/pi`, plus an arithmetic term. The terms, as exact rationals in `results.json`:

| Term | Value | Preview |
|---|---|---|
| state `2D` | `1170159676931825184288274812132100/42981220507576537932303142777593983768257` | 2.72249057e-8 |
| mean square `2D^2` | exact | 3.70598e-16 |
| kernel dynamics `49·10^-8/pi_lo` | exact | 1.559718442e-7 |
| arithmetic (half-width of the `e^{-3}/4` enclosure) | `1/(8·10^60)` | 1.25e-61 |

**Directed enclosures.**
- **pi:** Hutton `8atan(1/3)+4atan(1/7)`, rounded outward to `10^-60`, and checked for overlap with Machin. The pi rounding sits inside the kernel term (slack `5e-68`) and is not charged twice.
- **exp:** `e^{-3}` from Taylor with a geometric remainder, halving and outward squaring, then inversion.
- **Datum:** the midpoint of the `e^{-3}/4` bracket.

**Radius.** Exact rational (398 characters in `results.json`); outward to `10^-40` it is `1831967503411879425147166810021607/10^40`, about **1.8319675e-7**.
- It meets `10^-6`, with margin at least 5.4586.
- Interval: `C(1) in [0.0124465838952156, 0.0124469502887163]`.
- `e^{-3}/4` lies inside, so the result is `reference_unresolved`.
- `-10^-8` gives the exactly equal radius. It is a replay of the same `|tau|` formula (the `-tau` AQ state is separately chosen); it is not a second confirmation.
- `E(tau)/E(tau/100) in [100.00145,100.00146]`, against `[10.0081,10.0082]` if AT4's square-root D is substituted.

## 6. Crossover
The kernel term is linear in `s` and `M_0=2` is not, so `E(s)=2(D+D^2)+49|tau|s/pi` and `s*=pi(10^-6-2(D+D^2))/(49|tau|)`.

**Enclosure.** `s* in [6.236863446032, 6.236863446034]` (with `D->0` it would be `100pi/49 ~ 6.41141`). At the lower end the directed radius, including the arithmetic term, is at most `10^-6`; at the upper end the lower radius is at least `10^-6`.

**Scope.** This is the crossover of a formula, not a node certificate: s=1 is the only preregistered node. At `s*` the free value `e^{-3s*}/4<1.9e-9` is 500 times smaller than the radius, so the absolute bound carries no relative information there. There is no grid claim and no `[0,128]` claim.

## 7. Retained controls and fixtures
**AT4 Poisson certificate at L=10^4.** `D_AT4=2sqrt(49|tau|/3)` with a directed sqrt and log. The radius lies in `[8.41518704386266589e-4, …267]` and contains the AT4 report's `0.000841518704386267`. Insufficient.

**Optimized Poisson floor, D->0.** `log(1+L^2/s^2)>=2log(L/s)` gives, for **every** `L>0`, `F(L)>=(2ks/pi)(1+log(1/(2ks)))>=1.2650882233019e-6`. The value at `L=4081633` is at most `1.2650882233020e-6`. Insufficient; one evaluation at `L*` alone would not prove this.

**Poisson with the admitted D.** The bound is at least `D+D^2+floor>=1.27870e-6` for every `L`, so the state lemma alone does not rescue Poisson.

**Divergent Poisson first moment.** The truncated moment is `P_1(L)=(s/pi)log(1+L^2/s^2)>=(2s/pi)log(L/s)`, which is unbounded. Already `P_1(8)>4/pi>P_1(7)`, and `P_1(10^16)>23.45`. The window's `M_1=4s/pi` is finite for every truncation.

**Sign mutation (`theta->-theta`).** This conjugates `ghat`, so `|ghat|`, `M_0`, `M_1`, `M_2` and `E` are all unchanged. Only the datum exposes it: the free atom reads `g(-3)/4=25e^{-3}/4~0.31117`, against `e^{-3}/4`.

**Negative atom at x=-1.** The window reads `5/e~1.839`, the truth is `e`, and Poisson reads `1/e`. Also `sup_{x<0} g ~ 1.904` at `x=-(1+sqrt3)/(2s)` (preview), so the window amplifies negative spectrum.

**C^1 (preview only).** `M_0=4/pi`, `M_1=4s/pi`, `M_2` infinite; the negative atom reads `3/e` and the sign mutation reads `7e^{-3}/4`. Preview radius about 1.7330e-7 and preview crossover about 6.3003. Switching to it after `D` is known is rejected.

**tau=0.** The window radius equals the arithmetic term exactly. The Poisson radius keeps `s/(pi L)`. AT5's `exact_zero_reference_branch` zeroes every cost at `tau=0`; reusing it for the Poisson control breaks the amended control.

## 8. Checklist: where a producer is most likely to err
1. **Sign convention.** Using `e^{-i theta G}` or `ghat` with `e^{+i theta x}`. The moments and `E` are blind to it, so the checker must evaluate the free atom (`25e^{-3}/4` is the tell).
2. **Negative-atom misread.** Proving the lemma without citing AQ1 nonnegativity, or citing the AQ2 gap as needed. Or stating "inversion only on the support": inversion holds everywhere, and what needs the support is `g=e^{-sx}`.
3. **Dropping `m^2`.** `E=M_0D+kM_1`: the Boolean cannot see a `3.7e-16` omission, so the formula must be read.
4. **Tier (i), the AT4 square root, or the reverse 82-face `D`.** Tier (i) gives 4.75e-5 and fails. The AT4 square root gives 1.62e-3. The reverse `D_ii(rev)~1.139e-8` is admitted but not contract-bound; using it would be a post-hoc switch.
5. **The D/2 effect refinement on `W alpha^0_theta(W)`.** It yields 1.696e-7, still passing, so it is again invisible to the Boolean.
6. **Double-counting M_0 on D^2.**
   - Adding AT4's separate centering `D^2` on top of `M_0 D^2`.
   - Writing `M_0^2 D^2`.
   - Writing `M_0D+D^2` via `int ghat=g(0)=1`. This is a valid sharper form but not the frozen formula, so it must be labelled.
7. **Mislabelled C^1 preview.** Reporting 1.733e-7 as the radius, claiming a finite C^1 `M_2`, or omitting the preview label.
8. **L^1 norm.** Taking `||ghat||_1=|int ghat|=g(0)=1`, although `ghat` is complex.
9. **Slope and clock errors.**
   - Missing `s` in `M_1`.
   - Missing the factor 2 in `k`.
   - `7|tau|` per star without the `/8`.
   - Two stars instead of seven.
   - Exponent 24.
10. **Directed rounding.** Dividing by the upper end of pi in an upper bound; a float datum; an interval that does not contain `e^{-3}/4`.
11. **Crossover and Poisson scope.** Presenting `s*` as a certified range. Or showing Poisson failure at one `L`, with no all-`L` lower bound.
12. **Sign and calculator scope.** Presenting `-tau` as a second confirmation. A calculator accepting floats, `|tau|>10^-8`, nonzero triples, or `D` from anything but the admitted tier-(ii) formula.

**Replay.** `python3 -B research/round32/skeptic/av2_check.py --output <abs fresh dir>`. The normal and `-O` runs are byte-identical: `results.json` sha256 `b7852f23…d13c`. Nine source-mutation replays each aborted for the intended reason: `k` halved, orthant stars, `D/2` state, dropped `m^2`, pi direction, jump sign, a C^2 coefficient, a tier-(i) `D` and a halved floor.
