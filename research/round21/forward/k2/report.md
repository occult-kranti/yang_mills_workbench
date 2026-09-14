# K2 forward: a continuously certified two-observable inverse

Frozen before reverse-K2 comparison. Retain K1's conditional mobility `m=1+zeta x`, c positive, absolute zeta below one, and **known** absolute kappa at most 1/8. The new dimensionless coefficient `a` chooses the observable `g_a=x+a x²`; it changes neither the density nor the dynamics. No physical slopes are supplied.

## 1. Rate matrix and independent marginal copies

Set `f=x`, `G=Gamma(x)=(1-x²)/4`, `h_a=(1+2ax)²`. Let `nu_kappa` be the actual marginal law of x under the interacting three-link density. Define

\[
a_1=\int G\,d\nu,\quad b_1=\int xG\,d\nu,
\quad a_2=\int h_aG\,d\nu,\quad b_2=\int xh_aG\,d\nu.
\]

K1's initial imaginary-time slopes obey

\[
\binom{r_f}{r_g}=
\begin{pmatrix}a_1&b_1\\a_2&b_2\end{pmatrix}
\binom{c}{c\zeta},\qquad D=a_1b_2-a_2b_1.
\tag{K2.1}
\]

This is the determinant in linear variables `(c,c*zeta)`; the Jacobian in `(c,zeta)` has determinant cD. If D is positive, the inverse is

\[
c={b_2r_f-b_1r_g\over D},\qquad
c\zeta={a_1r_g-a_2r_f\over D}.
\tag{K2.2}
\]

An inverse result is admissible only when c is positive and absolute zeta is below one. Known kappa fixes the coefficient integrals; uncertain numerical integration of them would require an additional error budget.

## 2. Double-integral identity and all-finite-kappa positivity

Take X and X' to be independent copies **of this one marginal law**. They are an integration device, not a claim that the interacting U,V,W links are independent. Symmetrizing the determinant gives

\[
D={1\over2}\mathbb E\{G(X)G(X')(X-X')
                       [h_a(X)-h_a(X')]\}.
\]

Since `h_a(X)-h_a(X')=4a(X-X')[1+a(X+X')]`,

\[
\boxed{D=2a\iint G(X)G(X')(X-X')^2
 [1+a(X+X')]\,d\nu(X)d\nu(X').}
\tag{K2.3}
\]

For `0<a<1/2`, the bracket is at least `1-2a>0`. The marginal has a strictly positive density on the Haar interior for every finite kappa, and G is positive there. The non-diagonal region has positive product measure. Thus D is strictly positive for every finite kappa. This is an analytic proof over the complete interval, not a set of pointwise determinant samples.

## 3. Uniform explicit bound and the chosen design

F2 proves that the action oscillation is 12. The normalized joint density, and hence the x marginal relative to its Haar marginal, is at least `exp(-12|kappa|)`. The product marginal comparison therefore costs `exp(-24|kappa|)`. At Haar,

\[
\mathbb E G=3/16,\quad \mathbb E xG=0,\quad
\mathbb E x^2G=1/32,
\quad\mathbb E[GG'(X-X')^2]=3/256.
\]

Substitution into the nonnegative integrand bound yields

\[
D\ge {3a(1-2a)\over128}e^{-24|\kappa|}.
\tag{K2.4}
\]

Choose `a=1/4`. On absolute kappa at most 1/8, this gives `D>=3e^-3/1024`. A rational Taylor-plus-geometric-tail calculation in the checker proves `e³<21`, hence

\[
\boxed{D\ge1/7168>0.}
\tag{K2.5}
\]

At kappa zero the exact matrix and determinant are

\[
\begin{pmatrix}3/16&0\\25/128&1/32\end{pmatrix},
\qquad D=3/512.
\tag{K2.6}
\]

The selected quarter coefficient also maximizes the elementary sufficient factor `a(1-2a)` within the declared design interval. This optimizes this particular lower bound; it does not prove optimal statistical efficiency among observables.

At a zero the two observables coincide and D vanishes. Beyond the sufficient monotonicity range the present proof is unavailable, but rank need not fail: at a one, h decreases near x=-1 while the Haar determinant is still `3/128>0`. The checker retains both facts rather than claiming nonmonotonicity automatically destroys identification.

## 4. Sensitivity and what is identified

For a quarter, the simple bounds `a1,|b1|<=1/4`, `a2,|b2|<=9/16` and Equation K2.5 give an infinity-norm inverse bound of `5824`. Thus exact known matrix coefficients and rate errors at most epsilon imply errors in `(c,c*zeta)` at most `5824epsilon`. This is conservative. It is not a universal bound for recovering zeta: the final division by c becomes ill-conditioned as c approaches zero, and errors may cross the strict mobility boundary. Uncertain kappa, coefficient integration, and observational error need separate bounds.

The inverse is injective within the declared two-parameter family. Synthetic forward/inverse examples check its arithmetic. They do not constitute measured calibration, equivalence with the physical lattice generator, or stable inference under arbitrary noise.

## 5. Two rates do not identify arbitrary mobility

At kappa zero define the dimensionless cubic

\[
p_3(x)=x^3-3x/8.
\]

Parity gives `integral p3 G=0`. For the second rate only the odd term `4ax` in h contributes, and

\[
\int xp_3G={1\over4}\left[(\mathbb E x^4-\mathbb E x^6)
 -{3\over8}(\mathbb E x^2-\mathbb E x^4)\right]=0,
\]

using Haar moments `1/4,1/8,5/64`. Consequently `integral p3 h_a G=0` for every a.

At zeta zero the explicitly **out-of-family** mobility `m_xi=1+xi p3(x)` therefore preserves both chosen initial rates. The conservative estimate `|p3|<=11/8` implies `m_xi>=21/32>0` whenever absolute xi is at most 1/4. A nonzero xi changes the generator while keeping the stationary density and these two slopes unchanged. This is a counterexample to identifying arbitrary mobility from two rates; it does not contradict the positive determinant inside the affine family. No blindness at nonzero kappa is asserted.

## 6. Evidence and scope

The checker independently integrates Haar polynomials, evaluates the double-integral formula, certifies the exponential enclosure, verifies synthetic inverses, and tests the nonmonotone-design, sign, inadmissible-output and blind-cubic controls. Sources are [K1's rate derivation](../k1/report.md), [F2's action oscillation](../../../round20/forward/f2/report.md), and the admitted K1 gate. The project contribution is this explicit uniform rank certificate and its family-restriction counterexample; scientific priority is unverified. No L or M goal was selected or executed here.

```bash
python -B research/round21/forward/k2/check.py --output /tmp/ym21-forward-k2-replay
```
