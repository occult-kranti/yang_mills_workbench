# Exact assessment of the SU(2) mobility observations

**The mobility is not identified.** Both supplied, strictly positive candidates produce exactly the same three initial slopes:

| Observable \(f\) | \(r_{m_0}(f)\) | \(r_{m_1}(f)\) |
|---|---:|---:|
| \(x\) | \(3/16\) | \(3/16\) |
| \(x+x^2/4\) | \(25/128\) | \(25/128\) |
| \(x^2+x^3\) | \(59/256\) | \(59/256\) |

Write \(a=(1-x^2)/4\), \(\rho=(2/\pi)\sqrt{1-x^2}\), and
\[
p=x^5-\frac56x^3+\frac18x,\qquad m_1=1+\frac14p.
\]
Exact Catalan-moment arithmetic gives
\[
\mathbb E[a p x^k]=0\quad(0\leq k\leq4),\qquad
\mathbb E[a p^2]=\frac1{12288}.
\]
The three derivative squares are \(1\), \(1+x+x^2/4\), and \(4x^2+12x^3+9x^4\); hence each slope difference is zero. This is more than odd/even cancellation: the odd terms in the latter two tests vanish by weighted orthogonality. As a control, the positive mobility \(1+x/4\) changes their slopes to \(13/64\) and \(17/64\).

The coefficient bound \(|p(x)|\leq1+5/6+1/8=47/24\) on \([-1,1]\) proves \(m_1\geq49/96>0\). More generally every \(m_\epsilon=1+\epsilon p\), with \(|\epsilon|<24/47\), gives these same slopes. The nonzero polynomial is nonzero on a set of positive Haar measure, since the marginal has full interval support.

Precisely, these measurements identify three linear functionals of \(m\). With \(W_k=\mathbb E[m a x^k]\), they fix
\[
W_0=\frac3{16},\qquad W_1+\frac14W_2=\frac1{128},\qquad
4W_2+12W_3+9W_4=\frac{59}{256}.
\]
They do not fix all five displayed weighted moments or the mobility. The executed coefficient map on degree-at-most-five mobilities has rank three and nullity three. No finite-dimensional membership assumption was supplied. More generally, any finite list of \(N\) such slopes has a polynomial null direction in the \((N+1)\)-dimensional space of degrees at most \(N\); scaling that polynomial preserves strict positivity around the baseline \(m=1\). This proves finite-slope nonidentification, not equality of full time curves.

**A follow-up using the existing observable:** measure the second derivative of its unnormalized stationary imaginary-time correlation. This requires a declared dynamical extension: the reversible diffusion associated with the quadratic form \(\mathbb E[m a f'g']\), with its natural no-flux realization and smooth bounded positive mobility. Its generator is
\[
L_m f=\rho^{-1}(\rho m a f')'
=m\left(a f''-\frac34x f'\right)+a m'f',\qquad H_m=-L_m.
\]
The derivative term is essential. The alternative \(m\Delta\) has \(\mathbb E[m_1\Delta x]=-1/1024\), violating stationarity. The boundary term vanishes because \(\rho a m\) tends to zero at both endpoints.

For \(C_m(t)=\langle x,e^{tL_m}x\rangle\), \(C_m(0)=1/4\), \(-C'_m(0)=r_m(x)\), and self-adjointness gives \(C_m''(0)=\|L_mx\|^2\). Direct differentiation yields
\[
L_{m_1}x=-\frac34x-\frac1{128}U_6(x),\qquad
U_6=64x^6-80x^4+24x^2-1.
\]
The supplied moments verify \(\mathbb E[U_6^2]=1\) and \(\mathbb E[xU_6]=0\). Therefore
\[
C_{m_0}''(0)=\frac9{64},\qquad
C_{m_1}''(0)=\frac{2305}{16384},\qquad
C_{m_1}''(0)-C_{m_0}''(0)=\frac1{16384}.
\]
The correlation difference starts at \(t^2/32768+o(t^2)\); the Taylor coefficient includes the factor \(1/2!\). Thus these candidates do not have identical full \(x\)-correlation curves under this generator contract. For \(m_\epsilon\), this curvature is \(9/64+\epsilon^2/1024\), so it is blind to the sign of \(\epsilon\).

**An alternative requiring only another initial slope:** choose \(g=x^3+x^4\). Since \((g')^2=9x^4+24x^5+16x^6\),
\[
r_{m_0}(g)=\frac{51}{256},\qquad r_{m_1}(g)=\frac{409}{2048},
\qquad \Delta r=6\mathbb E[a p^2]=\frac1{2048}.
\]
More generally \(r_{m_\epsilon}(g)=51/256+\epsilon/512\), identifying \(\epsilon\) if that one-parameter family is independently imposed. Degree four is minimal among polynomial observables that distinguish these two candidates by an initial slope: degree at most three has derivative square degree at most four. This extra slope still does not identify unrestricted mobility. With bounded absolute experimental error \(\eta\) around either candidate prediction, the two new-slope intervals are disjoint when \(\eta<1/4096\); for the curvature, \(\eta<1/32768\). No measurement-noise model or finite-time differentiation error was supplied.

The calculation applies known orthogonal-polynomial and reversible-form methods. Specifically, the checked [NIST DLMF finite-series formula 18.5.10](https://dlmf.nist.gov/18.5.E10) gives \(p=C_5^{(2)}/192\). Its orthogonality weight is \((1-x^2)^{3/2}\), exactly proportional to \(\rho a\); the Chebyshev \(U_n\) weight and squared norm are also tabulated in [DLMF Table 18.3.1](https://dlmf.nist.gov/18.3#T1). These are known methods applied to this case, not a new polynomial family or an established discovery. The exact rational follow-up values are derived here; scientific novelty has not been investigated.

The full skill and its `finite-observations-and-operator-limits.md`, `admission-and-matching.md`, and `reconstruction-lessons.md` references were read. Their finite-data, divergence-term, and derivative-versus-Taylor-coefficient cautions were applied. DLMF's displayed finite formula and the relevant orthogonality rows were checked; the older books cited by DLMF were not read. The state, coefficients, and moments are supplied synthetic premises. No physical clock calibration, Hamiltonian-energy matching, unrestricted inverse theorem from full time data, or real-time claim follows.

Reproduce with `python /workspace/scratch/e6d8077ee5fa/skill-task/result/check.py`. The standard-library-only script writes `exact_results.json`, checks both candidates using exact fractions, compares Catalan moments with a beta-integral recurrence, verifies curvature both as \(\langle Lx,Lx\rangle\) and \(\langle x,L^2x\rangle\), and executes the two wrong-model controls. No quadrature, truncation, or sampling approximation enters these polynomial results.
