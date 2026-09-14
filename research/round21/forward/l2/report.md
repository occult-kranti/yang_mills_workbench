# L2 forward: any finite list of initial slopes leaves positive mobility freedom

Frozen before reverse-L2 comparison. Fix the known smooth positive conditional density rho on compact `SU(2)^3`, the energy coefficient c positive, and a smooth baseline mobility `m0>=m_star>0`. The observables are a finite list of smooth functions. The claim concerns **only their initial imaginary-time slopes**, not their complete correlation curves, the complete generator, or other data.

## 1. A constructive finite-dimensional nullspace

For N observables `f_1,...,f_N`, set

\[
L_j(P)=\int\rho\,P(x)\Gamma(f_j),\qquad
M_{jk}=L_j(x^k),\quad j=1,\ldots,N,\quad k=0,\ldots,N.
\]

This real matrix has N rows and N+1 columns, so its nullspace contains a nonzero vector b. A concrete construction is to find its rank and pivot columns, set one free coefficient to one, the other free coefficients to zero, and solve the pivot subsystem. Dependent equations then hold automatically. Define `P0(x)=sum b_k x^k`.

The marginal of x has full support on `[-1,1]`: its density is strictly positive in the interior relative to the Haar marginal. A nonzero polynomial cannot vanish on this whole interval. Thus P0 is nonzero as a function, not just as a formal coefficient vector. With `C=sum |b_k|>0`, the normalized polynomial

\[
P=P_0/C\quad\text{satisfies}\quad
\|P\|_\infty\le1,\qquad L_j(P)=0\ (1\le j\le N).
\tag{L2.1}
\]

This construction uses the exact moment matrix. If its entries are estimated numerically, deciding rank and solving a near-nullspace requires separate certified error bounds; small floating residuals do not prove exact invisibility. The checker executes exact rational elimination for the actual three Haar observables as a concrete instance. Finite fixtures check that instance; the dimension argument proves the general statement.

## 2. A whole interval of positive indistinguishable mobilities

For the nonzero normalized P, put

\[
m_\epsilon=m_0+\epsilon P,\qquad
|\epsilon|\le m_\star/2.
\]

Then `m_epsilon>=m_star/2>0`. Smoothness and compactness give the same divergence-form construction and Sobolev domains as K1. All these generators preserve rho, and their N initial slopes satisfy

\[
r_j(\epsilon)=c\int\rho m_\epsilon\Gamma(f_j)
=r_j(0)+c\epsilon L_j(P)=r_j(0).
\tag{L2.2}
\]

For every nonzero epsilon the generator actually changes. In any coordinate neighborhood where P is nonzero, the second-order symbol changes by `c epsilon P(x)|eta|²`; this cannot be canceled by lower-order terms. Such a neighborhood exists by the polynomial argument. Thus even at fixed c and known density, finitely many initial slopes do not uniquely determine unrestricted smooth positive mobility.

The result does not invalidate the full-rank inverses for the explicitly restricted affine or cubic families. Adding more coefficients without adding identifying information, however, does not supply uniqueness.

## 3. An exact fifth-degree hidden direction for the L1 observations

For kappa zero, baseline mobility one and the L1 observables
`f=x`, `g=x+x²/4`, `h=x²+x³`, define

\[
p_5=x^5-5x^3/6+x/8.
\tag{L2.3}
\]

The rate weights are `G(F')²`, with `G=(1-x²)/4`. Exact Haar integration shows

\[
\int p_5\Gamma(f)=\int p_5\Gamma(g)
=\int p_5\Gamma(h)=0.
\tag{L2.4}
\]

For transparency, parity eliminates every even derivative-square term. The remaining tests reduce to `integral p5*x*G=0` and `integral p5*x³*G=0`. Using `E x²=1/4`, `E x⁴=1/8`, `E x⁶=5/64`, `E x⁸=7/128`, and `E x¹⁰=21/512`, these are exact rational zeros. The checker integrates the full three rate polynomials independently rather than merely recording these asserted zeros.

The coefficient bound `|p5|<=1+5/6+1/8=47/24` proves

\[
1+\epsilon p_5\ge49/96>0
\qquad\text{for }|\epsilon|\le1/4.
\tag{L2.5}
\]

These mobilities preserve the same Haar density and all three L1 initial rates. At x zero, the operator difference on x is nevertheless

\[
(A_{1+\epsilon p_5}-A_1)x
=-\epsilon[p_5\Delta x+p_5'\Gamma(x)]
=-\epsilon/32\ne0\quad(\epsilon\ne0).
\tag{L2.6}
\]

Here `p5(0)=0`, `p5'(0)=1/8`, and `Gamma(x)(0)=1/4`. This supplies an explicit nonzero generator witness, not merely a different parameter label. In particular the epsilon-quarter fixture has residual `-1/128`.

There is also a direct control showing that complete time curves contain more information. On the whole coordinate interval, write

\[
T={(A_{1+\epsilon p_5}-A_1)x\over\epsilon}
=2x^6-\tfrac52x^4+\tfrac34x^2-\tfrac1{32}.
\]

Exact Haar integration gives `E[xT]=0` and `E[T²]=1/1024`. Since `A_1 x=3x/4`, the centered x correlation therefore has

\[
C_x''(0+)={c^2\over\hbar^2}\|A_{1+\epsilon p_5}x\|^2
={c^2\over\hbar^2}\left({9\over64}+{\epsilon^2\over1024}\right).
\tag{L2.7}
\]

Smooth x belongs to the generator domain, so the spectral second-derivative identity applies. The curvature changes for every nonzero epsilon, despite equality of all three initial slopes. Thus the explicit counterexample does **not** preserve the complete x time curve. This is a discriminating scope control and a possible held-out observation.

## 4. Classical polynomial provenance

The finite sum in [NIST DLMF 18.5.10](https://dlmf.nist.gov/18.5.E10), already inspected for L1, gives at n=5 and lambda=2

\[
C_5^{(2)}(x)=192x^5-160x^3+24x,
\qquad p_5=C_5^{(2)}/192.
\]

The shifted-factorial substitution is performed exactly in the checker. This is a classical Gegenbauer polynomial. The rate-blind direction is a concrete application of that existing family, not a new orthogonal-polynomial discovery.

## 5. What the result supports operationally

Declare a finite mobility basis before interpreting rates, require its actual coefficient matrix to have full rank over the intended parameter region, and reserve additional observations to challenge that basis. A held-out slope can expose one missing direction, as L1 did for the cubic; it does not establish that every other direction is absent. Full time curves and other dynamical data are additional information not covered by this obstruction. Matching any inferred conditional dynamics to the physical lattice model remains an independent task.

The exact checker records the general-construction instance, normalized nonzero null vector, all three p5 zeros, conservative positivity interval, explicit operator residual, and rejection of a wrong polynomial or wrong integration measure. Standard source/output hashes bind the proof and frozen contract. Scientific novelty of the broad finite-data linear-algebra obstruction is not claimed; the project contribution is its explicit evidence and applicability here. No later scientific goal was selected or executed.

```bash
python -B research/round21/forward/l2/check.py --output /tmp/ym21-forward-l2-replay
```
