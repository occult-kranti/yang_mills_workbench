# Hruday spectral-window and inverse-energy certificate — reverse AT2

Human author: **Hruday N M (BUNZEEY)**. AI-assisted independent reverse reconstruction; scientific priority unverified. HNM labels are traceable project aliases. No current forward or skeptic AT2 result was read. The shared prospective certificate choices and inherited admitted premises are disclosed and copied in `inputs/`.

## 1. Reverse reconstruction from the requested observable

The two target functionals are the mass of a fixed finite energy interval and the inverse-energy quadratic form. They are integrals against the same positive spectral measure. A complete pointwise minorant/majorant on its entire support therefore suffices. Only a second-moment upper bound is available, so the quadratic coefficient's sign must permit replacing that moment by its ceiling. This reverse argument determines the proof obligations before numerical evaluation. It does not reconstruct a unique spectrum from moments.

Use exactly AQ's chosen state and original centered Wilson vector, now with AT1's operator-domain and first-moment identity. Let eta be the pushforward of its positive spectral measure under x=E/alpha. Define

\[
 a=\frac1{16},\quad w=\omega_{num}(W),\quad q=\omega_{num}(W^2),\quad
 s=\int d\eta=q-w^2,\quad u=\int x\,d\eta=1-q,\quad
 v=\int x^2d\eta\le B=36+98|\tau|.\tag{HNM-AT2-R01}
\]

The support is contained in [a,infinity). AQ2 and |tau|<=10^-8 provide the convenient weak rational bounds

\[
 q_-:=\frac{31}{125}\le q\le q_+:=\frac{63}{250},\quad
 0\le z:=w^2\le z_+:=\frac1{250000},\quad
 B\le B_*:=\frac{1800000049}{50000000}.\tag{HNM-AT2-R02}
\]

These follow because 2sqrt(98|tau|)<1/500. The q,w uncertainty is deterministic analytic uncertainty, not sampled statistical error. We retain the joint relations s=q-z and u=1-q; independent optimization of unrelated moment intervals is not claimed. The rectangular q,z enclosure can contain points not realized by the actual model. Monotone endpoint substitution below gives valid uniform bounds, without asserting sharpness over its actual realizable states.

The frozen choices L=8,c=3,b=49 are dimensionless certificate parameters. They are not Hamiltonian couplings, regulators, fitted energies or predictions of pole locations. Alpha,hbar,spacing and E_star remain fixed positive.

## 2. A closed finite spectral window

For x>=a the affine function p_L(x)=(L-x)/(L-a) is at most one on [a,L], and is negative above L. Since L>a, this proves on the whole half-line

\[
 \frac{L-x}{L-a}\le\mathbf1_{[a,L]}(x),\qquad
 \eta([a,L])\ge\frac{Ls-u}{L-a}
 =\frac{(L+1)q-Lz-1}{L-a}.\tag{HNM-AT2-R03}
\]

At x=L the minorant is zero but the indicator is one. A possible endpoint atom is therefore retained rather than silently discarded. Finite first moment makes the affine function integrable even though it becomes negative without bound at large x.

The last expression increases with q and decreases with z. Insert q_-,z_+ and L=8 to obtain the exact Hruday window certificate

\[
 \boxed{\nu([\alpha/16,8\alpha])=\eta([1/16,8])
 \ge\frac{307992}{1984375}>\frac{31}{200}.}\tag{HNM-AT2-R04}
\]

The floor is approximately 0.15520857 of the unnormalized Wilson spectral weight. It is a mass guarantee, not a statement that all weight lies below 8alpha. This bound uses the gap and first moment, not the second-moment ceiling.

## 3. Inverse on the actual physical subspace and units

AQ2 makes the physical vacuum-orthogonal subspace reducing, and H restricted to it obeys H>=alpha a. Functional calculus thus defines a bounded positive inverse on the whole subspace, with norm at most 1/(alpha a), and also a bounded inverse square root. Since chi is centered, it lies in that subspace. Therefore

\[
 R:=\langle\chi,H^{-1}\chi\rangle
 =\|H^{-1/2}\chi\|^2
 =\frac1\alpha\int_a^\infty\frac1x\,d\eta(x),\qquad
 0\le R\le\frac{s}{\alpha a}.\tag{HNM-AT2-R05}
\]

The inverse is not defined by inverting the vacuum eigenvalue zero. It is the reduced inverse (or equivalently the bounded pseudoinverse set to zero on the vacuum). R has units inverse energy; alpha R is dimensionless. The inverse of the frequency generator H/hbar instead gives hbar R. No differentiability of a deformed infinite-volume ground state, or static susceptibility, follows from this functional calculus alone.

## 4. Entire-half-line reciprocal certificates

For every x>0, the tangent at c>0 has the exact positive residual

\[
 \ell_c(x)=\frac2c-\frac{x}{c^2},\qquad
 \frac1x-\ell_c(x)=\frac{(x-c)^2}{c^2x}\ge0.\tag{HNM-AT2-R06}
\]

For every x>=a>0 and b>=a the proposed quadratic satisfies

\[
 P_b(x)=\frac{x^2-(2b+a)x+b^2+2ab}{ab^2},\qquad
 P_b(x)-\frac1x=\frac{(x-a)(x-b)^2}{ab^2x}\ge0.\tag{HNM-AT2-R07}
\]

The denominators are strictly positive throughout the support. These factorizations prove global half-line domination, including arbitrarily large energies; a numerical grid is unnecessary. Integrating positive inequalities is weak duality. No strong duality or optimality theorem is used.

The coefficient of x^2 in P_b is +1/(ab^2)>0. Consequently v<=B may be substituted in the upper-bound direction. A negative coefficient would reverse that substitution inequality. The tangent has zero quadratic coefficient and uses no second-moment information. With c=3,b=49, let A=2b+a and D=b^2+2ab. Then

\[
 \frac{7q-6z-1}{9}
 \le\alpha R
 \le\frac{B-A+(A+D)q-Dz}{ab^2}.\tag{HNM-AT2-R08}
\]

Here A,D,A+D and ab^2 are positive. The lower expression is smallest at q_-,z_+; the upper expression is largest in this enclosure at B_*,q_+,z=0. Exact rational arithmetic gives

\[
 \boxed{\frac{91997}{1125000}\le\alpha R
 \le\frac{28462237549}{7503125000}.}\tag{HNM-AT2-R09}
\]

These are approximately 0.08177511 and 3.79338443. The second moment remains an upper bound throughout; no value v=B is assigned to the actual AQ measure.

## 5. Preserve and compare the elementary baselines

Cauchy–Schwarz applied to sqrt(x) and 1/sqrt(x) in L2(eta) yields s^2<=u integral x^-1 d eta. Both functions are square integrable: u is finite by AT1, and inverse integrability follows from a>0. Also u=1-q>=1-q_+>0. The support bound remains as in (R05):

\[
 \frac{s^2}{u}\le\alpha R\le\frac{s}{a}.\tag{HNM-AT2-R10}
\]

The lower expression (q-z)^2/(1-q) decreases with z, because q-z>0. Its q derivative is (q-z)(2-q-z)/(1-q)^2>0 throughout the declared box. Thus its uniform floor is attained at q_-,z_+ within that box. The upper support ceiling is at q_+,z=0. Therefore

\[
 \frac{3843876001}{47000000000}\le\alpha R\le\frac{504}{125}.\tag{HNM-AT2-R11}
\]

The Cauchy floor is slightly stronger than the frozen c=3 tangent, while the polynomial upper bound is stronger than the support ceiling. The certificate package consequently permits the combined interval

\[
 \boxed{\frac{3843876001}{47000000000\,\alpha}\le R
 \le\frac{28462237549}{7503125000\,\alpha}.}\tag{HNM-AT2-R12}
\]

Its lower endpoint is approximately 0.08178460/alpha. The tangent remains recorded as a independently checked frozen certificate, with its honest baseline comparison. No parameter was retuned to hide this comparison, and no globally optimal interval is claimed.

## 6. Equal moments do not specify spectral type or inverse energy

Consider the following abstract dimensionless positive measures, solely as information-content controls:

\[
 \eta_A=\frac{\delta_2+\delta_4}{8},\quad
 \eta_B=\frac{\delta_1}{32}+\frac{3\delta_3}{16}+\frac{\delta_5}{32},\quad
 \eta_C=\frac14\operatorname{Uniform}[3-\sqrt3,3+\sqrt3].\tag{HNM-AT2-R13}
\]

Their supports lie above a: 3-sqrt3>1>a because sqrt3<2. A and B have different finite atom sets. C has a bounded Lebesgue density on its interval and no atoms. Direct sums give the first three moments of A and B. For C, write X=3+Y with Y uniform on [-sqrt3,sqrt3]. Symmetry gives E Y=0 and E Y^2=(sqrt3)^2/3=1. Hence all three have

\[
 (\int d\eta,\int x\,d\eta,\int x^2d\eta)
 =\left(\frac14,\frac34,\frac52\right).\tag{HNM-AT2-R14}
\]

These match the contracted relation at q=1/4,w=0 and lie strictly below B even at tau=0. They show insufficiency even if the second moment were supplied exactly, more information than the actual AT1 ceiling.

Their inverse moments are

\[
 r_A=\frac3{32},\quad r_B=\frac1{10},\quad
 r_C=\frac1{8\sqrt3}\log\frac{3+\sqrt3}{3-\sqrt3}
 =\frac1{12}\sum_{k=0}^\infty\frac{3^{-k}}{2k+1}.\tag{HNM-AT2-R15}
\]

For the series identity, expand 1/(3+Y) in its uniformly convergent geometric series on |Y|<=sqrt3<3 and integrate: odd powers vanish and the even uniform moments are 3^k/(2k+1). The exact remainder after terms k=0,...,N-1 is positive and bounded by

\[
 0<r_C-\frac1{12}\sum_{k=0}^{N-1}\frac{3^{-k}}{2k+1}
 \le\frac{3^{-N}}{8(2N+1)}.\tag{HNM-AT2-R16}
\]

At N=8 the rational enclosure is

\[
 \frac3{32}<\frac{1872586}{19702683}<r_C
 \le\frac{254674699}{2679564888}<\frac1{10}.\tag{HNM-AT2-R17}
\]

Thus identical zeroth, first and second moments permit different inverse responses, and an atomic or atomless measure. Each fixture has an abstract self-adjoint multiplication realization on L2(eta), source vector 1, and an added vacuum summand. This construction does not realize the actual AQ Hamiltonian. It proves neither multiple AQ thermodynamic states nor any claim about which spectral type AQ actually possesses. In particular moments alone do not identify a particle pole, an exact mass, or b=49 as an energy atom.

## 7. Exact controls and provenance

The standard-library checker verifies polynomial coefficient identities, all rational endpoints, monotonicity coefficient signs and all equal-moment arithmetic. Its executed controls include:

- A negative quadratic coefficient with v<B reverses the putative upper-bound substitution. In contrast the actual P_b coefficient is positive, and the strict substitution slack is computed on eta_A.
- The polynomial (x-3/2)^2-1/16 is positive at the frozen sampled points a,1,2,3,8,49,100, but negative at x=3/2. This rejects a sampled-grid certificate. The actual certificates use exact factorizations instead.
- A permitted joint moment point q=q_-,w=1/500 has s and u different from the Haar values. A one-atom abstract measure of mass s at u/s realizes those moments with v=u^2/s<B. It invalidates an assignment of Haar values to unknown interacting moments; it does not claim every Haar-substituted numerical bound happens to fail.
- The endpoint atom delta_L has window mass one while p_L(L)=0. A separate measure with positive high-energy weight above L verifies that a mass floor is not a hard spectral cutoff.
- A/B/C have exactly equal moments and different inverse responses, including atomless C. The v ceiling is strictly larger than their exact second moments.
- Rescaling alpha changes R inversely, and replacing energy by frequency introduces hbar. Dimensionless inverse integrals cannot be presented as an energy inverse unchanged.
- In a two-state diagnostic H=diag(0,3), W=sigma_x/2, R=1/12. Perturbations H-fW and H-2fW have different derivatives of the W expectation, 2R and 4R, despite identical undeformed R. This demonstrates the missing source-calibration requirement. Even after fixing a source, existence and interchange of derivatives for an infinite-volume deformed AQ state remain unproved; this finite fixture does not establish that differentiability.

Bertsimas and Popescu, *SIAM J. Optim.* 15 (2005), Sections 2–3, provide the moment-duality and polynomial-positivity ancestry, including the upper-moment coefficient-sign condition. Abbott et al., arXiv:2605.20509v1, Sections III.1, IV.1–IV.3 and VII.4, give the current spectral-kernel certificate context and caution about interpreting extremal feasible measures as the true spectrum. Those primary passages were checked with the source panel and direct reading. Their general methods retain attribution. The Hruday/HNM contribution is this model-specific AQ application, exact physical interval and discriminating countercontrols; priority is unverified.

Reproduce with `python -B research/round30/reverse/at2/check.py --output /absolute/fresh-directory`. Every source, report, checker and output is hash-bound; normal and optimized Python output bytes are compared. Finite controls audit algebra and counter-inferences; the full-half-line proofs above establish certificate validity. No global optimization, actual susceptibility, unique spectrum or continuum conclusion is asserted. AT2 ends here; Loop 3 remains unselected pending its review.
