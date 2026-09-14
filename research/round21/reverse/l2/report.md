# Reverse L2: any finite initial-slope list leaves mobility directions unseen

The finite-data obstruction is constructive. For any fixed finite list of smooth initial correlation slopes, a nonzero polynomial mobility perturbation can preserve every slope, retain strict positivity, and change the generator. This statement concerns initial slopes, not complete time-correlation curves. The explicit example here is distinguishable already by a second derivative.

## 1. Build a null direction from the finite observation constraints

Fix the conditional density at known finite `kappa`, a positive smooth baseline mobility `m0`, fixed energy coefficient `c>0`, and `N` smooth observables `f_j`. Their mobility-dependent initial slopes are the finite linear functionals

\[
L_j(P)=\int\rho_\kappa P(x)\Gamma(f_j),\qquad j=1,\ldots,N.
\]

Restrict these functionals to polynomials of degree at most `N`, a vector space of dimension `N+1`. The exact matrix `M_(j,k)=L_j(x^k)`, `0<=k<=N`, has a nonzero null vector by rank-nullity. It constructs a nonzero polynomial `P0` with all `L_j(P0)=0`.

The marginal of `x` has full support in `[-1,1]` and positive interior density, because the original smooth density is strictly positive on compact `SU(2)^3`. A nonzero polynomial therefore is not zero almost everywhere and is nonzero on some open coordinate interval. Normalize its coefficients:

\[
P=P_0\Big/\sum_{k=0}^N|a_k|,\qquad P_0=\sum a_kx^k.
\]

The denominator is positive and `||P||_infinity<=1` on `[-1,1]`. This gives an explicit finite coefficient bound without solving a polynomial maximization problem. The moment matrix here is the exact mathematical matrix; a small numerical singular value in a noisy estimate does not establish an exact null identity.

## 2. Preserve positivity and stationary density while changing the dynamics

Let `m_star=inf m0>0`. For

\[
m_\epsilon=m_0+\epsilon P,\qquad |\epsilon|\le m_\star/2,
\]

we have `m_epsilon>=m_star/2`. Thus the same smooth uniformly positive divergence-form realization applies and the prescribed stationary density remains `rho_kappa`. Every selected initial slope is unchanged because its difference is `c epsilon L_j(P)=0`.

For nonzero `epsilon`, the generator changes. Its second-order principal coefficient changes by `epsilon P(x)` on an open set, so the two differential operators cannot coincide. This does not require identifying their spectra or their full time correlations. A null direction among finitely many measured functionals is fully consistent with distinct generators.

## 3. Exhibit an exact positive direction invisible to all three L1 slopes

At `kappa=0`, baseline `m0=1`, and the L1 observables `x`, `x+x^2/4`, `x^2+x^3`, choose

\[
\boxed{p_5(x)=x^5-\frac56x^3+\frac18x.}
\]

Let `G=(1-x^2)/4`. Oddness immediately gives `E p5 G=0`. The remaining odd parts of the squared observable derivatives reduce the other two conditions to

\[
\mathbb E[xp_5G]
=\frac3{512}-\frac56\frac3{256}+\frac18\frac1{32}=0,
\]

\[
\mathbb E[x^3p_5G]
=\frac7{2048}-\frac56\frac3{512}+\frac18\frac3{256}=0.
\]

Consequently all three exact initial rates agree between `m=1` and `m=1+epsilon p5`. The elementary coefficient bound is

\[
\|p_5\|_\infty\le1+5/6+1/8=47/24.
\]

Hence, for `|epsilon|<=1/4`,

\[
\boxed{1+\epsilon p_5\ge49/96>0.}
\]

These bounds are sufficient and conservative; no exact supremum claim is needed.

The polynomial is classical. Substituting `n=5,lambda=2` into the finite sum in [NIST DLMF Eq.18.5.10](https://dlmf.nist.gov/18.5.E10) gives coefficients `192,-160,24`, so `p5=C5^(2)/192`. The checker reconstructs this substitution directly. Neither this polynomial nor the Gegenbauer family is a new discovery.

## 4. Show that the generator and the complete correlation curve change

At `kappa=0`, applying the generator difference to `x` yields

\[
\frac{(A_{m_\epsilon}-A_1)x}{\epsilon}
=\frac{3xp_5-(1-x^2)p_5'}4
=2x^6-\frac52x^4+\frac34x^2-\frac1{32}=:T(x).
\]

At `x=0`, this is `-1/32`, so the operator difference is nonzero whenever `epsilon` is nonzero. There is also a stronger scope control using the **same** observable `f=x`. The baseline satisfies `A_1x=3x/4`, an odd function, while `T` is even. Exact Haar integration gives

\[
\mathbb E[(3x/4)T]=0,\qquad \mathbb E[T^2]=1/1024.
\]

For smooth `x`, the initial second correlation derivative is `C_x''(0)=c^2||A_mx||^2/hbar^2`. Therefore

\[
\boxed{C_{x,\epsilon}''(0)-C_{x,0}''(0)
=\frac{c^2\epsilon^2}{1024\hbar^2}>0\quad(\epsilon\ne0).}
\]

The selected first derivatives agree, but the full correlation curves are not identical. This explicitly rejects extending finite-initial-slope ambiguity to complete time traces.

## 5. What the operational workaround requires

Declare a finite mobility basis before calibration, derive a rate matrix for that basis, and require full rank with controlled coefficient and observation errors. Reserve additional observables or higher time derivatives to challenge the assumed model class. L1's successful finite-family inverse remains valid; it cannot select among unmodeled null directions without additional information. Adding variables alone does not establish uniqueness. Physical clock units and identification with the full lattice Hamiltonian remain separate requirements.

The exact checker verifies all three null moments, positivity at signed endpoints, the nonzero generator polynomial, its squared norm, a separate `3x4` nullspace construction with coefficient normalization, and rejection of a wrong cubic coefficient in `p5`. The general proof is rank-nullity plus positivity on compact support; finite fixtures do not replace it. The contribution is a constructive limitation and targeted derivative test within this conditional model, with scientific priority unverified.

```bash
python -B research/round21/reverse/l2/check.py --output /tmp/ym21-reverse-l2
```
