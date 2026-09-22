# Hruday spectral-window and inverse-energy certificate — AT2 forward

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted forward derivation independently executed before reading any current AT2 reverse or skeptic solution. HNM tags are project aliases, not claims to have invented moment duality, Jensen/Cauchy inequalities or reciprocal polynomial identities. Model-specific application; scientific priority is unverified.

**Result in the actual AQ state.** The original centered Wilson spectral measure satisfies

\[
\nu([\alpha/16,8\alpha])\ge\frac{307992}{1984375},\qquad
\frac{3843876001}{47000000000\alpha}
\le\langle\chi,H_{phys}^{-1}\chi\rangle
\le\frac{28462237549}{7503125000\alpha}.
\tag{HNM-AT2-F01}
\]

The interval is a conservative certificate, not an optimal reconstruction. The lower inverse endpoint in (F01) uses the standard Cauchy baseline, which slightly improves the frozen c=3 tangent. None of these bounds identifies a particle pole or makes an infinite-volume susceptibility assertion.

## 1. Exact shared state, normalization and uncertainty

Take exactly the AQ numerical-cap state and physical reducing generator admitted in AQ2 and AT1, with the original centered Wilson vector chi. The inherited gap is `H_phys>=alpha/16` on the vacuum-orthogonal sector, and chi belongs to that sector. Define the dimensionless pushforward `eta(B)=nu(alpha B)`, `x=E/alpha`, `a=1/16`. With `w=omega_num(W)`, `q=omega_num(W^2)`, put

\[
s=\int d\eta=q-w^2,\quad u=\int x\,d\eta=1-q,
\quad v=\int x^2d\eta\le B=36+98|\tau|,
\quad\operatorname{supp}\eta\subseteq[a,\infty).
\tag{HNM-AT2-F02}
\]

These are actual AQ moments. The second moment is bounded, not evaluated. AQ2's trace-norm estimate on the actual 48-link cover gives `|w|<=1/500`, `|q-1/4|<=1/500`. Write `z=w^2`; the joint declared domain is

\[
q_-:=31/125\le q\le63/250=:q_+,\quad0\le z\le1/250000=:z_+,
\quad s=q-z\ge61999/250000,
\quad 187/250\le u\le94/125.
\tag{HNM-AT2-F03}
\]

Actual q and w are not replaced by Haar values. In particular s and u share q and must be propagated jointly. The rectangular q,z enclosure may include more points than the actual Hamiltonian realizes; bounds valid throughout it are conservative for the actual state. It is deterministic analytic uncertainty, not a sampling covariance.

The frozen L=8, c=3 and b=49 are dimensionless certificate choices; they change neither state nor Hamiltonian. Positive alpha,hbar,E_star and lattice spacing remain fixed. No AO/AQ state identification or continuum limit is used.

## 2. Full-half-line window minorant

For any L>a and x>=a, the affine function `p_L(x)=(L-x)/(L-a)` obeys

\[
\frac{L-x}{L-a}\le\mathbf1_{[a,L]}(x).
\tag{HNM-AT2-F04}
\]

For a<=x<=L its value lies between zero and one. For x>L it is negative while the indicator is zero. At x=L the minorant equals zero and the closed-window indicator equals one. Thus a possible atom at L is retained and never erroneously subtracted. Integrating this pointwise inequality is justified because eta has finite first moment. For L=8,

\[
\eta([a,8])\ge\frac{8s-u}{8-a}
=\frac{9q-8z-1}{127/16}
\ge\frac{307992}{1984375}.
\tag{HNM-AT2-F05}
\]

The last expression increases with q and decreases with z, so its minimum over (F03) is exactly at q=q_-, z=z_+. This certificate uses the mass, first moment and support bound only; it does not use v or B. It proves at least this much unnormalized spectral weight in the window. It is not a hard upper spectral cutoff, a probability of one, or an assertion that the true spectrum ends at 8alpha.

## 3. Meaning and units of the inverse-energy form

The physical vacuum-orthogonal subspace reduces the self-adjoint H_phys and its spectrum there lies in `[alpha/16,infinity)`. The spectral reciprocal on that subspace is a bounded positive operator with norm at most 16/alpha. Since chi is centered, its quadratic form is well-defined:

\[
R:=\langle\chi,(H_{phys}|_{\Omega^\perp})^{-1}\chi\rangle
=\int E^{-1}d\nu(E)=\alpha^{-1}I,
\quad I:=\int x^{-1}d\eta(x).
\tag{HNM-AT2-F06}
\]

One may extend the inverse by zero on the vacuum, but not call it an inverse of the full operator at zero. R has inverse-energy units. Hbar is absent from an energy inverse; a frequency inverse would carry a different factor. This is a mathematically defined inverse-energy quadratic form. Identifying 2R with a derivative of a thermodynamic ground-state expectation would require a separately specified deformation, existence and differentiability of its state branch, and an interchange of thermodynamic/differentiation limits. None is assumed here, so no static-susceptibility assertion is made.

## 4. Frozen tangent lower certificate

For any c>0 and x>0,

\[
\frac1x-\left(\frac2c-\frac{x}{c^2}\right)
=\frac{(x-c)^2}{c^2x}\ge0.
\tag{HNM-AT2-F07}
\]

The denominator is strictly positive throughout the support. This is an algebraic identity and a whole-half-line proof, not a positivity grid. With c=3, integration and joint uncertainty propagation give

\[
I\ge\frac23s-\frac19u
=\frac{7q-6z-1}{9}
\ge\frac{91997}{1125000}.
\tag{HNM-AT2-F08}
\]

Again the minimum is at q_-,z_+. No second-moment value is used. The tangent may be negative for large x; that does not spoil a lower bound.

## 5. Frozen quadratic upper certificate and correct moment sign

For a>0, b>=a and x>=a, define the quadratic numerator N_b(x)=`x^2-(2b+a)x+b^2+2ab`. Direct polynomial expansion gives

\[
\frac{N_b(x)}{ab^2}-\frac1x
=\frac{(x-a)(x-b)^2}{ab^2x}\ge0.
\tag{HNM-AT2-F09}
\]

The denominator is strictly positive, the first factor is nonnegative, and the last factor is a square. This proves the upper bound at every continuous x>=a, including x=a,b and the infinite tail. Integrating and using the **positive** x^2 coefficient gives

\[
I\le\frac{v-(2b+a)u+(b^2+2ab)s}{ab^2}
\le\frac{B-(2b+a)(1-q)+(b^2+2ab)(q-z)}{ab^2}.
\tag{HNM-AT2-F10}
\]

The replacement v<=B has the required direction only because `1/(ab^2)>0`. It is not an equality claim. For b=49, the numerator increases with B and q and decreases with z. Hence use `B_cap=1800000049/50000000`, q=q_+, z=0, obtaining

\[
I\le\frac{28462237549}{7503125000}.
\tag{HNM-AT2-F11}
\]

The declared q,w relation remains intact during this calculation. These coefficients were frozen before execution; there is no tuning on outputs or claim that b=49 is optimal.

## 6. Baseline comparisons

Cauchy-Schwarz applied to sqrt(x) and 1/sqrt(x) in L^2(eta), and the support reciprocal bound, give

\[
\frac{s^2}{u}\le I\le\frac{s}{a}.
\tag{HNM-AT2-F12}
\]

Both integrals needed for Cauchy are finite; u>0 follows explicitly from (F03). The function `(q-z)^2/(1-q)` decreases with z and increases with q throughout the declared domain: its q derivative is `2(q-z)/(1-q)+(q-z)^2/(1-q)^2>0`. Therefore the uniform Cauchy baseline is

\[
I\ge\frac{(61999/250000)^2}{94/125}
=\frac{3843876001}{47000000000}
>\frac{91997}{1125000},\qquad
I\le16q_+=\frac{504}{125}.
\tag{HNM-AT2-F13}
\]

The frozen quadratic upper bound is strictly smaller than 504/125. Combining the stronger of the two valid lower bounds with the stronger upper bound produces (F01). All numbers are exact rationals. No strong-duality theorem, extremizer existence or global optimality is asserted.

## 7. Equal moments do not identify an energy atom

The prescribed abstract controls are

\[
\eta_A=\frac{\delta_2+\delta_4}{8},\quad
\eta_B=\frac{\delta_1}{32}+\frac{3\delta_3}{16}+\frac{\delta_5}{32},\quad
\eta_C=\tfrac14\operatorname{Uniform}[3-\sqrt3,3+\sqrt3].
\tag{HNM-AT2-F14}
\]

For A and B, direct finite sums give `(s,u,v)=(1/4,3/4,5/2)`. For C, write x=3+y with y uniformly distributed on `[-sqrt3,sqrt3]`. Symmetry gives E[y]=0, and elementary integration gives E[y^2]=3/3=1. Multiplying the resulting moments 1,3,10 by 1/4 gives the same triple. The support of C lies strictly above one because sqrt3<2, hence all three supports are above a. All obey the moment relations at q=1/4,w=0 and satisfy v<=B. A and B have distinct atom sets; C has a bounded interval density and no atoms.

Their inverse moments are nevertheless different:

\[
I_A=\frac3{32},\qquad I_B=\frac1{10},\qquad
I_C=\frac{1}{8\sqrt3}\log\frac{3+\sqrt3}{3-\sqrt3}
=\frac1{12}\sum_{k=0}^{\infty}\frac{1}{3^k(2k+1)}.
\tag{HNM-AT2-F15}
\]

The integral formula follows by integrating 1/x against the uniform density `1/(8sqrt3)`. The series follows from integrating the geometric series for `1/(1-t^2)` from zero to 1/sqrt3, where it converges absolutely and uniformly on that closed interval. There is no uncontrolled logarithm evaluation. The first three terms are 17/180. For k>=3, `1/(2k+1)<=1/7` and the geometric sum of 3^-k is 1/18. Therefore

\[
\frac3{32}<\frac{17}{180}<I_C
\le\frac{17}{180}+\frac1{1512}
=\frac{719}{7560}<\frac1{10}.
\tag{HNM-AT2-F16}
\]

Strictness on the lower side follows from the positive remaining series. Thus even exact knowledge of all three contracted moments, stronger than AT1's second-moment ceiling, does not determine spectral atom structure or inverse-energy response. Each fixture is realized abstractly by multiplication by x on L^2(eta), with source vector 1; adding an orthogonal one-dimensional zero-energy vacuum realizes a centered nonnegative spectral problem. This is not a realization by the AQ lattice Hamiltonian. The controls establish insufficiency of the moment information, not actual thermodynamic-state nonuniqueness or multiple AQ phases.

## 8. Controls, source ancestry and scope

The exact checker expands the rational identities as polynomial coefficient arrays, checks endpoint propagation with rational arithmetic, and integrates the finite and uniform moment fixtures symbolically. Whole-half-line validity comes from the factorization and sign proofs, not the diagnostic sample evaluations. A polynomial `(x-3/2)^2-1/16` is positive at all integer sample nodes but negative at 3/2, exposing grid-only positivity. A negative-quadratic kernel control shows why replacing v by B in an upper bound with a negative coefficient is invalid. Further controls preserve an atom at x=8, distinguish a second-moment ceiling from equality, reject substituting q=1/4,w=0 for the allowed interacting unknowns, and verify the alpha^-1 scaling.

Bertsimas and Popescu, *SIAM J. Optim.* 15 (2005), Sections 2-3, supply classical ancestry for polynomial moment certificates and the upper-moment coefficient-sign rule. Abbott, Fields, Jay, Oare and Saccardi, arXiv:2605.20509v1, III.1, IV.1-IV.3 and VII.4, provide current spectral-kernel certificate context and explicitly distinguish extremal feasible spectra from the true spectrum. Selected passages and the panel's source record were consulted, not the entirety of either research program. The contribution here is this particular AQ dictionary, evaluated enclosure and exact controls; generic methods are not Hruday inventions.

Run `python -B research/round30/forward/at2/check.py --output /absolute/new/directory`. Normal and optimized results must match. The checker and report use only stdlib/exact arithmetic. No physical susceptibility, pole, exact mass, sharpness, state identification or continuum Yang-Mills result is claimed. Loop 3 awaits advisor selection after the separate skeptical review.
