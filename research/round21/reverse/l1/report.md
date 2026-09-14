# Reverse L1: a third observable detects the hidden cubic

The three slopes identify the declared `(c,zeta,xi)` family at known `kappa=0`. The exact determinant is `27/262144`. The new cubic coefficient is an explicit dynamics extension, not a quantity inferred from static data or a physical lattice matching.

## 1. Check the extended operator before importing its bound

Use `m=1+zeta*x+xi*p3(x)`, `p3=x^3-3x/8`, and `|zeta|,|xi|<=1/4`. The polynomial is smooth on the compact SU(2) coordinate domain. Since `|x|<=1` and `|p3|<=11/8`,

\[
\boxed{m\ge1-\frac14-\frac{11}{32}=\frac{13}{32}>0.}
\]

Thus the weighted form `q_m[f]=integral rho m|grad f|^2` is closed with a smooth core, the divergence operator `A_m=-rho^-1 div(rho m grad)` has its nonnegative self-adjoint realization, and constants are its unique zero mode. K1's ground-state transformation applies with the actual derivative `grad m=[zeta+xi(3x^2-3/8)]grad x` retained. The static density is unchanged, while the mobility and generator are changed explicitly.

The density comparison and uniform ellipticity give, for the separate static interval `|kappa|<=1/8`,

\[
\Delta\ge\frac{3c}{4}\frac{13}{32}e^{-12|\kappa|}
\ge\boxed{\frac{13c}{192}}.
\]

The box is sufficient, not necessary. For example `zeta=1/2,xi=0` lies outside it but has mobility at least `1/2`. Leaving the box does not prove negative mobility or a closed spectral gap.

## 2. Derive the three rate rows from Haar moments

At known `kappa=0`, let `f=x`, `g=x+x^2/4`, `h=x^2+x^3`, and `G=Gamma(x)=(1-x^2)/4`. Initial centered imaginary-time slopes are

\[
r_j=-\hbar C_j'(0)=c\mathbb E_0[m(j'(x))^2G].
\]

Haar odd moments vanish and the even recurrence is `E x^(2n)=[(2n-1)/(2n+2)]E x^(2n-2)`. K2's first two rows therefore extend with zero cubic column. For the third observable, `h'(x)^2=4x^2+12x^3+9x^4`, giving

\[
\mathbb E[h'^2G]=59/256,\quad
\mathbb E[xh'^2G]=9/64,\quad
\mathbb E[p_3h'^2G]=9/512.
\]

Consequently

\[
\boxed{
\begin{pmatrix}r_f\\r_g\\r_h\end{pmatrix}=
\begin{pmatrix}
3/16&0&0\\25/128&1/32&0\\59/256&9/64&9/512
\end{pmatrix}
\begin{pmatrix}c\\c\zeta\\c\xi\end{pmatrix}.}
\]

The nonzero diagonal product is `27/262144`. It is the determinant in the linear parameters `(c,c*zeta,c*xi)`; the Jacobian in `(c,zeta,xi)` is `c^2` times this value. Thus it is nonzero for every `c>0`.

## 3. Reconstruct the model and detect the omitted term

Back substitution yields

\[
\boxed{c=16r_f/3,\quad
\zeta=32r_g/c-25/4,\quad
\xi=512r_h/(9c)-118/9-8\zeta.}
\]

Accept the chosen positivity-box certificate only when the recovered parameters satisfy its constraints. This exact inverse is derived at `kappa=0`; the nonzero-`kappa` gap certificate is not a justification for reusing these Haar rate coefficients there.

The first two rates remain unchanged when `xi` varies, while the third changes by `9c*delta(xi)/512`. In the exact fixture `c=2,zeta=1/8,xi=1/4`, discarding the cubic term leaves a nonzero third-rate residual `9/1024`. A wrong third observable `x^3` has an even squared derivative, so both odd mobility coefficients integrate to zero; its row is `(27/256,0,0)` and rank remains two. Thus the added observable must be selected to discriminate the missing coefficient.

Synthetic forward/inverse fixtures check these exact formulas. They are not empirical clock calibration. Dividing by `c` still produces sensitivity as `c` approaches zero, and unknown static coefficients or unrestricted noisy slopes require separate error analysis.

## 4. Identify the polynomial's established provenance

[NIST DLMF Eq.18.5.10](https://dlmf.nist.gov/18.5.E10) gives the finite Gegenbauer sum. Substitution of `n=3,lambda=2` has two terms: the degree-three coefficient is `(2)_3*2^3/3!=32`, and the degree-one coefficient is `-(2)_2*2=-12`. Hence

\[
C_3^{(2)}(x)=32x^3-12x,\qquad p_3=C_3^{(2)}/32.
\]

The checker reconstructs these coefficients from the finite sum. This is a classical polynomial, not a new orthogonal-polynomial family. The project-specific result is its use as a hidden mobility direction and the exact third-observable response that detects it; scientific priority for that application is unverified.

## 5. Keep the family boundary explicit

Three linear slope functionals cannot identify arbitrary smooth mobility functions. Their common kernel in an infinite-dimensional function space is nontrivial; small bounded kernel perturbations of a strictly positive baseline retain positivity. The admitted inverse concerns only the chosen three-parameter family. It does not identify a unique unrestricted dynamics, match the physical lattice Hamiltonian, or construct a continuum theory.

```bash
python -B research/round21/reverse/l1/check.py --output /tmp/ym21-reverse-l1
```
