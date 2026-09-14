# Reverse K2: continuous rank from an observable design

The two-rate inverse is identifiable throughout the declared known-`kappa` interval within the affine mobility family. For `a=1/4`, its linear rate determinant satisfies `D>=1/7168`. A positive cubic mobility perturbation outside this family preserves both rates at `kappa=0`, so the measurements do not identify arbitrary dynamics.

## 1. Derive the matrix from the actual marginal

Choose `f=x`, `g_a=x+a x^2`, `0<a<1/2`, and write `G=(1-x^2)/4`, `h_a=(1+2ax)^2`. The coefficient `a` designs an observable; it changes neither the action nor the mobility. Let `nu_kappa` be the true marginal of `x` under the interacting three-link density. Define

\[
a_1=\mathbb E_\nu G,\ b_1=\mathbb E_\nu xG,
\qquad a_2=\mathbb E_\nu h_aG,\ b_2=\mathbb E_\nu xh_aG.
\]

The dynamic rates obey

\[
\begin{pmatrix}r_f\\r_g\end{pmatrix}
=\begin{pmatrix}a_1&b_1\\a_2&b_2\end{pmatrix}
\begin{pmatrix}c\\c\zeta\end{pmatrix},\qquad D=a_1b_2-a_2b_1.
\]

This determinant concerns `(c,c*zeta)`. The Jacobian in `(c,zeta)` is `cD`.

## 2. Symmetrize over independent copies of the marginal

Let `X,Xprime` be two independent copies of **the same complete marginal** `nu_kappa`. They do not represent two independent interacting links. Expanding the determinant and exchanging the copies gives

\[
D=\frac12\mathbb E\left[GG'(X-X')[h_a(X)-h_a(X')]\right].
\]

Because `h_a(X)-h_a(X')=4a(X-X')[1+a(X+X')]`,

\[
\boxed{D=2a\mathbb E\left[GG'(X-X')^2[1+a(X+X')]\right].}
\]

For `0<a<1/2`, the last bracket is at least `1-2a>0`. The marginal has a strictly positive density in the interior `(-1,1)` for every finite `kappa`; `G` is positive there and two different values occur with positive measure. Thus `D>0` for every finite `kappa` under this design. No unproved decorrelation of the original links is used.

## 3. Quantify rank on the entire static interval

The action oscillation is twelve. Therefore the full density relative to Haar, and consequently the `x` marginal density relative to its Haar marginal, is at least `exp(-12|kappa|)`. Applying this comparison separately to the two copies is legitimate because the displayed integrand is nonnegative.

Under the Haar marginal, exact moments yield

\[
\mathbb E G=3/16,\quad\mathbb E xG=0,\quad\mathbb E x^2G=1/32,
\]

\[
\mathbb E_0[GG'(X-X')^2]
=2\left[(\mathbb E_0G)(\mathbb E_0x^2G)-(\mathbb E_0xG)^2\right]
=3/256.
\]

Hence

\[
\boxed{D\ge\frac{3a(1-2a)}{128}e^{-24|\kappa|}.}
\]

At `a=1/4` and `|kappa|<=1/8`, this becomes `D>=(3/1024)e^-3`. A rational Taylor-plus-geometric-tail enclosure of `exp(3/2)`, squared, is strictly below `21`. Thus

\[
\boxed{D\ge1/7168.}
\]

At `kappa=0`, direct independent polynomial integration instead gives the exact matrix

\[
\begin{pmatrix}3/16&0\\25/128&1/32\end{pmatrix},
\qquad D=3/512.
\]

The uniform lower bound is deliberately conservative. The checker reconstructs both this matrix determinant and the two-copy polynomial expectation separately.

## 4. Invert only within the declared family and admissible parameter region

For known `kappa` and the corresponding moment coefficients,

\[
\boxed{c=\frac{r_fb_2-r_gb_1}{D},\qquad
c\zeta=\frac{a_1r_g-a_2r_f}{D}.}
\]

The recovered result is admissible only when `c>0` and `|zeta|<1`. The checker explicitly rejects zero/negative `c` and both `|zeta|=1` boundary cases. Synthetic exact recoveries test the algebra, not measured calibration.

For rate errors bounded by `epsilon_f,epsilon_g`, exact coefficient knowledge gives

\[
|\delta c|\le\frac{|b_2|\epsilon_f+|b_1|\epsilon_g}{D},
\quad
|\delta(c\zeta)|\le\frac{|a_2|\epsilon_f+|a_1|\epsilon_g}{D}.
\]

When `|delta c|<c`, the mobility error is at most

\[
|\delta\zeta|\le
\frac{|\delta(c\zeta)|+|\zeta|\,|\delta c|}{c-|\delta c|}.
\]

Thus uniform determinant control does not make the ratio insensitive near `c=0`, nor does it cover arbitrary observational noise or uncertainty in `kappa`. At nonzero `kappa`, actual coefficient evaluation and its errors remain necessary before using measured rates.

## 5. Construct an explicit out-of-family ambiguity

At `kappa=0`, add `xi p3(x)` to the mobility, where

\[
p_3(x)=x^3-3x/8.
\]

Oddness gives `E_0 p3 G=0`. For the second observable, only the `4ax` term of `h_a` can survive parity, and

\[
\mathbb E_0[xp_3G]
=\mathbb E_0[x^4G]-\frac38\mathbb E_0[x^2G]
=\frac3{256}-\frac38\frac1{32}=0.
\]

Therefore `E_0 p3 h_aG=0` for every `a`: neither initial rate changes. At `zeta=0`, the crude bound `|p3|<=11/8` gives

\[
1+\xi p_3(x)\ge1-\frac14\frac{11}8=21/32>0
\qquad (|\xi|\le1/4).
\]

Nonzero `xi` produces a distinct positive reversible mobility with the same static density and the same two initial rates. This is a genuine family-limit counterexample, fully consistent with the proven invertibility inside `(c,zeta)`.

## 6. Retain the design exceptions

At `a=0`, the observables coincide and rank collapses. Outside the sufficient monotone range, the double-integral bracket can become negative; the proof above then cannot discard signs. The checker uses `a=1`, `X=-3/4`, `Xprime=-1/2` to expose that failure. Nevertheless the exact Haar determinant at `a=1` is positive, so failure of this sufficient argument is **not** universal rank failure. A reversed determinant sign is rejected by the independently positive Haar fixture.

The result is a conditional-model observable design, uniform rank bound, and explicit inverse-family limitation. It does not calibrate a physical clock or identify the full lattice theory. Scientific priority is unverified; the covariance symmetrization and inverse methods are established mathematical tools.

```bash
python -B research/round21/reverse/k2/check.py --output /tmp/ym21-reverse-k2
```
