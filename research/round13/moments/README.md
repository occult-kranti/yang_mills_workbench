# Certified bounds from the compact moment hierarchy

The previous round showed why setting the variance to zero loses a real term. This calculation keeps that term and bounds it using exact identities and positivity. The physical object is the explicitly specified one-plaquette **Euclidean probability measure**

\[
d\mu_\kappa(x)=Z(\kappa)^{-1}e^{\kappa x}\frac{2}{\pi}\sqrt{1-x^2}\,dx,
\quad -1\le x\le1,\quad \kappa\in\mathbb R.
\]

It is not the ground-state density of the two-plaquette Hamiltonian. A result about its mean is not a particle mass. The positivity-bootstrap strategy is established in lattice gauge research; this is a small exact-arithmetic implementation and audit, not a claim of inventing the method. See the primary [finite-rank lattice bootstrap study](https://arxiv.org/abs/2404.16925) and [SU(3) extension, version 2](https://arxiv.org/html/2502.14421v2), particularly the positivity setup. Those papers treat larger loop systems; their numerical results are not premises of these rational certificates.

## Equations and variables

Let \(m_n=\int x^n d\mu_\kappa\), \(u=m_1\), and \(v=m_2-u^2\). Integrating the derivative of \(x^n e^{\kappa x}(1-x^2)^{3/2}\) gives

\[
n m_{n-1}-(n+3)m_{n+1}+\kappa(m_n-m_{n+2})=0.
\]

The boundary contribution vanishes. For nonzero \(\kappa\), normalization \(m_0=1\) and the unknown mean \(m_1=u\) express every subsequent moment as an affine function \(a_n+b_n u\):

\[
m_{n+2}=m_n+\frac{n m_{n-1}-(n+3)m_{n+1}}{\kappa}.
\]

At zero coupling, do not use this division. The exact moments are \(m_{2j}=C_j/4^j\), \(m_{2j+1}=0\), where \(C_j\) is the Catalan number. In particular, \(u=0\) and \(v=1/4\).

For every polynomial \(p\), positivity of \(p^2\) and \((1-x^2)p^2\) on the support gives necessary conditions

\[
H_r(u)=[m_{i+j}]_{i,j=0}^{r}\succeq0,
\qquad L_{r-1}(u)=[m_{i+j}-m_{i+j+2}]_{i,j=0}^{r-1}\succeq0.
\]

Here \(r\) controls the number of checked moment identities, not physical volume, lattice spacing or a new field. Both matrices are affine in \(u\). Their feasible means form a nonempty compact interval. Higher levels add necessary constraints; they do not require a guessed factorization of moments.

## What the exact certificate proves

A negative matrix eigenvalue estimated in floating point is insufficient to reject a mean. The solver instead retains a **rational polynomial witness** \(w\), which produces

\[
w^T H_r(u)w=c+du\ge0
\quad\text{or}\quad w^T L_{r-1}(u)w=c+du\ge0.
\]

When \(d>0\), this proves \(u\ge-c/d\); when \(d<0\), it proves \(u\le-c/d\). The delivered endpoints are exact rational witness roots intersected with the known support interval. The verifier recomputes the recurrence, quadratic forms, signs and roots. A source hash, group/measure scope, parameter, hierarchy level, requested bisection precision and semantic result type are included in the contract.

The search uses a Bessel-series mean proposal only to locate an interior point. That proposal is not a premise of the bound. Every proposed interior point is checked by exact positive-semidefinite tests. Two retained feasible points and the dual outer endpoints certify that the optimization error is at most \(2/2^{b}\) on each side, where \(b\) is the requested bisection count. If proposal precision is inadequate, the program reports failure rather than declaring the measure inconsistent.

The congruence routine retains an original-coordinate witness through positive-pivot elimination. It explicitly handles zero pivots: a zero diagonal block with a nonzero off-diagonal entry is indefinite. It also handles the all-positive termination branch, which was missing in the first draft. The initial exception and repaired source are documented in `history/`.

The variance follows from the exact first recurrence,

\[
v(u)=1-3u/\kappa-u^2.
\]

The program propagates the whole certified mean interval through this concave quadratic, including its interior maximum when present. It then intersects with the independently known range \(0\le v\le1\). This is an analytic range intersection, not clipping an observed numerical defect. The full-support measure actually has strictly positive variance at every finite coupling; a weak finite certificate may still have zero as its lower endpoint.

## Recorded results

Twenty-eight exact certificates cover hierarchy levels 1–6 at \(\kappa=1,5,20\), plus zero, signed, small-coupling and large-coupling controls through \(|\kappa|=100\). At \(\kappa=1,r=6\), the mean interval has width approximately \(1.40631\times10^{-13}\). Its endpoints round to 0.24019372387000923 and 0.24019372387014987. At \(\kappa=5,r=6\), the width is approximately \(6.03663\times10^{-8}\). These are different parameter cases, so equal accuracy is not assumed.

The complete endpoints, polynomial witnesses, feasible points and uncertainty widths remain rational strings in `output/certificates.json`. `output/bounds.csv` includes logarithms of strictly positive widths for plotting; the exactly zero-width Haar case is omitted from logarithmic axes. Very long rational endpoints must not be converted with JavaScript `Number(numerator)/Number(denominator)`: both can overflow even when their ratio is finite. The website receives explicitly labeled floating display coordinates computed from the rational values.

The study also calculates independent SciPy Bessel and direct angular-quadrature values. Their agreement is a numerical diagnostic. A separate skeptic recomputes rational series intervals and checks containment; ordinary decimal agreement does not establish an enclosure.

## A simple assumption that fails exactly

At \(\kappa=9/8\), the point distribution at \(u=1/3\) has positive moment/support matrices and satisfies the first identity:

\[
3u=\kappa(1-u^2)=1.
\]

Its next identity has residual \(1-u^2=8/9\). Thus normalization, positivity and one exact equation can all pass for a false closure. Adding the next equation matters. The level-2 recurrence-generated moment matrices reject this proposed mean; introducing the variance as a free number alone would not repair the missing hierarchy.

## Why the complete compact hierarchy is sufficient

At all orders, moment positivity defines an inner product on polynomials. The support localizer makes multiplication by \(x\) a contraction. Its bounded self-adjoint extension has a spectral measure supported in \([-1,1]\). Normalization gives total mass one. This supplies a measure, not merely a sequence of fitted moments.

Polynomial integration-by-parts identities extend to \(C^1\) test functions by uniformly approximating the derivative and integrating that approximation. In distribution form they say

\[
D[(1-x^2)\mu]=[\kappa(1-x^2)-3x]\mu.
\]

In the open interval, the unique density up to normalization is \(e^{\kappa x}\sqrt{1-x^2}\). Endpoint atoms must be checked separately. Multiplication by \(1-x^2\) kills such atoms on the left, whereas the right contributes nonzero endpoint atoms with coefficients \(\mp3\). The interior weighted density vanishes at the endpoints, so it supplies no cancelling boundary delta. The endpoint atoms therefore vanish.

Consequently the complete normalized hierarchy identifies the specified measure. Nested compact finite feasible sets have a singleton intersection, so their mean-interval widths tend to zero. This theorem provides no convergence rate. For the implemented witness method, the same conclusion additionally requires successful computations at levels tending to infinity and certified optimization slack tending to zero. The delivered implementation deliberately supports only levels 1–6; these finite runs do not execute that limiting theorem.

## Run and inspect

From the repository root:

```bash
python research/round13/moments/test_moments.py
python -O research/round13/moments/test_moments.py
python research/round13/moments/run_study.py
```

The exact kernel uses Python's standard library. The study uses NumPy, SciPy and Matplotlib. The public API accepts exact integers, rational strings or `Fraction` objects; floats, booleans, nonfinite values and unsupported resource parameters are rejected explicitly. Its supported range is \(|\kappa|\le100\), levels 1–6 and bisection counts 8–96. These are implementation limits, not boundaries of the analytic measure or hierarchy theorem.

The next unresolved application is an interacting loop hierarchy with its actual shared-link identities and positivity constraints. One-plaquette success does not supply a connected-volume Hamiltonian vacuum, reflection positivity for a continuum field, or a physical mass gap.
