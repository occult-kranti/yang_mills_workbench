# A scalar exception that preserves the missing fluctuation

The one-plaquette tilted-Haar model has an exact scalar response equation. The correction is to retain the susceptibility as the derivative of the mean with respect to the same Euclidean coupling. No arbitrary mass, adjustable closure constant or new quantum field is needed for this particular reduction. This is a compact probability model, not the interacting Hamiltonian ground state, real-time Yang–Mills dynamics or the four-dimensional continuum theory.

The study below constructs and checks the regular solution, identifies branches and closures that fail its defining conditions, and separates analytic error bounds from numerical agreement. It supplies a controlled benchmark for a future connected-plaquette hierarchy.

## 1. Definitions and assumptions

Let

\[
d\mu_\kappa(x)=Z(\kappa)^{-1}e^{\kappa x}\frac{2}{\pi}\sqrt{1-x^2}\,dx,
\quad -1\le x\le1,\quad \kappa\in\mathbb R,
\]

where \(Z(\kappa)>0\) normalizes the measure. Define

\[
m_n(\kappa)=\mathbb E_\kappa[x^n],\qquad
u(\kappa)=m_1(\kappa),\qquad
v(\kappa)=m_2(\kappa)-u(\kappa)^2.
\]

Here \(x=\tfrac12\operatorname{Tr}U\) for a single SU(2) group element under its normalized Haar measure. The coupling \(\kappa\) and observable \(x\) are dimensionless. Every real finite \(\kappa\) gives a positive density on the interior of the same compact interval; no regulator limit is taken.

On each compact coupling interval the exponential and every coupling derivative are uniformly bounded in \(x\). Dominated differentiation therefore gives

\[
\frac{d m_n}{d\kappa}=m_{n+1}-m_nm_1,
\qquad u'=v>0.
\]

Strict positivity follows because \(x\) is not almost surely constant under a positive interior density. It does not require a numerical positivity threshold. Symmetry gives \(Z(-\kappa)=Z(\kappa)\), odd \(u\), and even \(v\).

## 2. Forward and backward derivation meet at susceptibility

The compact integration-by-parts identity is

\[
0=\int_{-1}^{1}\frac{d}{dx}\left[x^n(1-x^2)^{3/2}e^{\kappa x}\right]dx,
\]

whose boundary term vanishes. Dividing by the normalizing integral yields

\[
n m_{n-1}-(n+3)m_{n+1}+\kappa(m_n-m_{n+2})=0.
\]

For \(n=0\), this is \(3u=\kappa(1-m_2)\). The forward construction has already proved \(m_2=u^2+u'\). Substituting it gives the closed equation

\[
\boxed{\kappa u'+3u=\kappa(1-u^2).}
\]

The backward question is whether a solution of this scalar equation represents the original measure. An arbitrary scalar solution is insufficient: it must belong to the bounded regular branch fixed by the origin. The mean of the normalized compact measure provides existence, and the difference equation below proves uniqueness among bounded branches. Thus the two directions meet through a proved derivative identity, rather than an independently fitted variable.

The origin is a regular point of the expectation and a singular point only of the divided formula \(u'=1-u^2-3u/\kappa\). Evaluating that divided formula as \(0/0\), replacing the division by an arbitrary small constant, or assigning the derivative zero changes the numerical problem. We use

\[
u(0)=0,\qquad u'(0)=\mathbb E_0[x^2]=\frac14.
\]

For \(\kappa>0\), two bounded solutions \(u_1,u_2\) have difference

\[
\delta'+\left(\frac3\kappa+u_1+u_2\right)\delta=0,
\qquad
\delta=C\kappa^{-3}\exp\left[-\int_0^\kappa(u_1+u_2)\,ds\right].
\]

The exponential has a finite nonzero limit at zero if both solutions are bounded. Boundedness of \(\delta\) therefore forces \(C=0\). Reflection determines the negative-coupling side.

## 3. Independent special-function identification and inadmissible constants

The modified-Bessel integral formula gives

\[
Z(\kappa)=\frac{2I_1(\kappa)}{\kappa},\qquad Z(0)=1,
\quad
u(\kappa)=\frac{I_2(\kappa)}{I_1(\kappa)}\quad(\kappa>0).
\]

This identification uses the integral in [NIST DLMF 10.32.2](https://dlmf.nist.gov/10.32.E2) and the derivative recurrence in [DLMF 10.29.2](https://dlmf.nist.gov/10.29.E2). The numerical comparator evaluates scaled \(I_1,I_2\) to avoid the common exponential growth; it uses the regular local polynomial only for \(|\kappa|<10^{-6}\), so the named Bessel comparator is not an independent special-function check in that tiny fallback region. The independently integrated Haar moments cover the origin separately.

Setting \(u=Y'/Y\) linearizes the Riccati equation:

\[
Y''+\frac3\kappa Y'-Y=0.
\]

For positive \(\kappa\), its general real solution is

\[
Y=\frac{A I_1(\kappa)+B K_1(\kappa)}{\kappa},\qquad
u=\frac{A I_2(\kappa)-B K_2(\kappa)}{A I_1(\kappa)+B K_1(\kappa)},
\]

on intervals where the denominator is nonzero. The reduction follows by substituting \(Y=w/\kappa\) into the [modified-Bessel equation, DLMF 10.25.1](https://dlmf.nist.gov/10.25.E1). The constants are not unconstrained physical additions. A nonzero \(B\) produces \(u\sim-2/\kappa\) near the origin; some mixed signs also produce a zero of the denominator and a pole. The small-argument form is supported by [DLMF 10.30.2](https://dlmf.nist.gov/10.30.E2). These branches violate boundedness and, near the origin, the compact-observable range \(|u|\le1\). Only \(B=0\) gives the regular normalized measure; the remaining multiplicative \(A\) cancels from \(u\) and is fixed in \(Z\) by \(Z(0)=1\).

The executable pure-\(K\) control uses \(-K_2/K_1\) at six positive couplings. It is less than \(-1\) in every tested case and \(\kappa u\) approaches \(-2\). This numerical control illustrates an already identifiable analytic failure; it does not establish admissibility by sampling.

## 4. A controlled launch near the origin

Write the local regular series as \(u=\sum_{n\ge0}a_n\kappa^{2n+1}\). Direct coefficient matching gives

\[
a_0=\frac14,\qquad
a_n=-\frac{\sum_{i+j=n-1}a_i a_j}{2n+4}\quad(n\ge1),
\]

and hence

\[
u=\frac\kappa4-\frac{\kappa^3}{96}+\frac{\kappa^5}{1536}
-\frac{\kappa^7}{23040}+\frac{13\kappa^9}{4423680}+O(\kappa^{11}).
\]

The code independently derives these coefficients with rational arithmetic. A local series is not evaluated as a global approximation at large coupling.

For a finite odd polynomial \(p\), form its exact residual

\[
R(\kappa)=\kappa p'(\kappa)+3p(\kappa)-\kappa[1-p(\kappa)^2]
=\sum_j R_j\kappa^j.
\]

If \(0<\epsilon\le1/2\), the sufficient rational witness

\[
a_0-\sum_{n\ge1}|a_n|\epsilon^{2n}>0
\]

proves \(p\ge0\) on \([0,\epsilon]\). Since the true regular \(u\) is also nonnegative there, \(e=u-p\) obeys

\[
e'+\left(\frac3\kappa+u+p\right)e=-\frac{R}{\kappa}.
\]

The integrating factor and \(e(0)=0\) then give

\[
\boxed{|u(\epsilon)-p(\epsilon)|
\le\epsilon^{-3}\int_0^\epsilon s^2|R(s)|\,ds
\le\sum_j\frac{|R_j|\epsilon^j}{j+3}.}
\]

Every term in this final bound is rational for rational \(\epsilon\). With the degree-seven polynomial and \(\epsilon=1/100\), the recorded exact bound is approximately \(2.9387393\times10^{-24}\). This controls the analytic launch polynomial. Converting that rational initial value to a floating number and subsequently integrating the ODE introduces additional errors. The tiny analytic launch bound is not a bound on the entire computed trajectory.

## 5. Why the zero-variance workaround fails

Dropping \(v\) from \(3u=\kappa(1-u^2-v)\) gives the stable algebraic expression

\[
u_{\rm point}(\kappa)=\frac{2\kappa}{3+\sqrt{9+4\kappa^2}}.
\]

Its slope is \(1/3\) at zero, contradicting the exact slope \(1/4\). It solves only the first moment identity with \(m_n=u_{\rm point}^n\). That moment sequence describes a point mass, whose variance vanishes, whereas the tilted-Haar measure has positive variance at every finite coupling.

A rational counterexample shows why checking positivity and one equation is insufficient. At

\[
\kappa=9/8,\quad u=1/3,\quad m_n=u^n,
\]

the first identity has zero residual. The moment matrix

\[
H_1=\begin{pmatrix}1&1/3\\1/3&1/9\end{pmatrix}
\]

is positive semidefinite, and \(L_0=1-m_2=8/9>0\). Nevertheless, the next Haar identity has residual

\[
1-4m_2+\kappa(m_1-m_3)=\frac89.
\]

The counterexample therefore passes those necessary positivity conditions while failing the defining model equation. At \(\kappa=0\), the first identity is even less discriminating; the next identity is required to recover \(m_2=1/4\).

The second deliberate wrong-model control changes the Riccati coefficient from 3 to 2, with its own consistently derived regular launch series. It differs from the correct mean by about 0.1064 on the recorded positive-coupling grid. It cannot pass merely because an inconsistent initial condition causes an obvious integration failure.

There is a useful exception: coefficient 2 is compatible with a different prior, the uniform measure on \([-1,1]\). Integration by parts of \((1-x^2)e^{\kappa x}\) then gives that coefficient, and its regular mean is \(\coth\kappa-1/\kappa\). Thus this control does not declare the altered equation meaningless; it identifies exactly which original assumption was changed. That uniform-prior result cannot be substituted into the SU(2) Haar model without changing the model.

## 6. Reproducible numerical experiments

The independent representations are: coefficient-matched ODE evolution, a scaled Bessel ratio, and direct quadrature in \(x=\cos\theta\) with the explicit \(\sin^2\theta\) Haar weight. The ODE uses SciPy DOP853. Both the mean and the reference diagnostics must be finite before any acceptance status is emitted. The origin is treated analytically, and negative-coupling ODE values are obtained by the proved odd reflection, not claimed as a separate integration run.

| Experiment | Quantity held fixed | Quantity varied | Recorded result |
|---|---|---|---|
| Launch refinement | Cubic polynomial, ODE relative tolerance \(2\times10^{-13}\), common comparison interval \([0.5,5]\) | \(\epsilon=1/2,1/4,1/8,1/16\) | Maximum differences decrease from \(2.0012\times10^{-5}\) to \(1.1412\times10^{-12}\) |
| ODE refinement | Degree-seven launch, \(\epsilon=1/100\), common grid \([0.05,5]\) | Relative tolerances \(10^{-5},10^{-8},10^{-11},2\times10^{-13}\) | Maximum differences from Bessel ratio: \(8.1126\times10^{-7},6.4029\times10^{-10},6.4704\times10^{-13},1.2768\times10^{-14}\) |
| Direct integral | Same compact density | Eleven couplings spanning \([-20,20]\), including zero | Bessel mean, positive variance and first two identities pass the declared floating thresholds |
| Symmetry | Same normalized density | Five positive/negative pairs | Odd means and independently integrated even variances agree |
| Wrong branches/models | Their own consistent definitions | Variance omitted, coefficient 2, pure \(K\) branch | Each exhibits a resolved contradiction |

The displayed errors are maximum differences at the declared sample grids. They are not sup-norm interval bounds. Neither a tolerance request nor matching two floating values at about \(10^{-14}\) proves fourteen-digit accuracy of the exact solution. Endpoint-only comparisons can also hide launch error: forward damping makes errors at \(\kappa=5\) much smaller than at the earliest common sample.

The producer suite has 100 checks, repeated in normal and optimized Python. Repetition under \(-O\) verifies that optimization does not delete the gates; it does not double the number of independent checks. Separate skeptic review is reported in its own artifact.

## 7. Next rigorous bridge: an envelope for the whole residual

Let \(q\ge0\) be a differentiable approximation on \([\kappa_0,K]\), with \(\kappa_0>0\), and define

\[
r=q'-\left(1-q^2-3q/\kappa\right).
\]

Since the true regular \(u\ge0\), the same integrating-factor argument gives

\[
\boxed{|q(\kappa)-u(\kappa)|
\le\left(\frac{\kappa_0}{\kappa}\right)^3|q(\kappa_0)-u(\kappa_0)|
+\kappa^{-3}\int_{\kappa_0}^{\kappa}s^3|r(s)|\,ds.}
\]

This is a proved conditional error-transport statement. A rigorous bound on the approximation over an entire interval would require a certified initial interval, a certified nonnegativity condition for \(q\), and an envelope for \(|r|\) between all sample points, including coefficient-rounding effects. Those last computational obligations are not implemented by the present floating solver. A piecewise rational polynomial with interval or Bernstein residual bounds is a concrete next experiment. Integrating backward toward zero reverses the favorable damping and can magnify error; a solver should not use backward agreement as an unchecked regularity certificate.

For connected plaquettes, the next mathematical object is the covariance matrix \(\partial u_p/\partial\kappa_q=\operatorname{Cov}(x_p,x_q)\), whose off-diagonal terms generally survive. The success of one scalar Riccati equation provides no proof that all those terms vanish or can be absorbed into one universal scalar. Uniform volume estimates, reconstruction of a physical quantum theory, a continuum limit and a positive mass gap remain separate obligations.

## 8. Code and evidence map

`response_checks.py` contains small named functions for the exact recursion and residual, controlled initialization, the two floating reference methods, the ODE, invalid-input gates and output generation. `initial_bound` accepts only integers or Fractions for exact inputs. The scalar helpers reject nonfinite values and Boolean substitutions; `rhs` refuses the singular divided origin. ODE grids must be nonempty, finite, strictly increasing and contained in the integration interval.

The output set includes:

- `initialization_bounds.json`: rational coefficients, residuals, positivity witnesses and analytic launch bounds.
- `wrong_closure_fixture.json`: exact rational counterexample.
- `response_curves.csv`: means, variance, two wrong-model curves and sampled differences.
- `epsilon_sweep.csv` and `tolerance_sweep.csv`: separate refinement axes.
- `reference_checks.csv` and `singular_branches.csv`: direct-integral and branch controls.
- `response_closure.png/.svg` and `response_refinement.png/.svg`: plots of those recorded data.
- `results.json`: explicit gate statuses, software versions and the hash of the source bytes run.
- `SHA256SUMS.json`: hashes of the generated evidence files.

The independent skeptic caught a public-input defect before acceptance: NumPy converted Boolean grid entries to floating coordinates before the strict scalar checks could see them. The implementation now runs every raw grid entry through the finite-real validator before conversion, with three Boolean regression cases and separate string and complex-entry rejections. The original source and reproducer are retained in `history/`; the scientific study grids contained no Booleans and their equations and data are unaffected.

The code checks source bytes before and after each complete run. A failed check raises an exception; unevaluated or empty check collections cannot receive a passing status. These implementation gates make the experiment reviewable. They do not substitute for the derivations or for an independently checked continuum theorem.
