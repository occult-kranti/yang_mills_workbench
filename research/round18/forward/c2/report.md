# C2: one actual surrounding-link integration

The complete six-weight conditional integral at \(\kappa=1/64\) gives a strictly positive normalized expectation near

\[
 \mathbb E_\kappa[O]\approx1.95552780972\times10^{-6},
\]

with an exact interval of width approximately \(3.11110\times10^{-15}\), below the frozen \(10^{-12}\) target. Degree8 succeeds; degrees0,2,4,6 remain as actual insufficient-width results. This integrates **two Haar links on the actual four-cube graph**, with all other31links fixed to identity. It is not the full twenty-face bulk integral or a Hamiltonian spectral-gap calculation.

## 1. Actual graph and conditional action

The graph has vertices \((x,y,z)\), \(x,y\in\{0,1,2\}\), \(z\in\{0,1\}\):18vertices,33positive-coordinate links,20elementary faces. Every face uses a signed four-link cycle. Unfreeze

\[
 U:(1,1,0)\to(1,1,1),\qquad V:(1,0,0)\to(1,0,1).
\]

There are four faces incident on \(U\), three incident on \(V\), and exactly one shared face. Thus the affected union has six faces. Reading the actual words gives three normalized traces \(x=\operatorname{Tr}U/2\), two \(y=\operatorname{Tr}V/2\), and one

\[
 w=\tfrac12\operatorname{Tr}(UV^\dagger).
\]

The shared face starts with an identity horizontal link, then \(U\), then an identity reverse horizontal link, then \(V^\dagger\). The other fourteen face terms are constant under this two-variable conditional integral. The factor \(e^{14\kappa}\) cancels from its normalized quotient; those terms must still be retained when constructing any larger surrounding marginal.

The full variable action and the original four-central-adjoint observable are therefore

\[
 S_2=3x+2y+w,\qquad
 O={ (4x^2-1)^3(4w^2-1)\over81},\qquad
 \langle O\rangle_{\kappa,2}={\int Oe^{\kappa S_2}\,dU\,dV\over\int e^{\kappa S_2}\,dU\,dV}.
\]

Both measures are independent normalized \(SU(2)\) Haar measures. The links themselves need not commute. An exact noncommuting rational quaternion fixture checks all20word reductions. The machine graph validator recognizes this fixed canonical graph and orientation; rejection of a different encoding is not a claim that every equivalent graph labeling is physically invalid.

For comparison only, retain \(S_d=3x+dy+w\) with \(d=1\) and0. These delete one and two surrounding-only face weights. They are explicitly different actions on the same observable, not alternative evaluations of the complete action.

## 2. A valid dagger exception and an invalid pointwise identification

At fixed \(U=V=(3/5,4/5,0,0)\), quaternion multiplication gives

\[
 \tfrac12\operatorname{Tr}(UV^\dagger)=1,
 \qquad\tfrac12\operatorname{Tr}(UV)=-7/25.
\]

This rejects a pointwise misstatement of the actual oriented word. It does **not** imply that a consistent replacement of \(w\) by \(w_+=\operatorname{Tr}(UV)/2\) changes this integrated joint law. The substitution \(V\mapsto V^\dagger\) preserves Haar measure and \(y\), and exchanges \(w_+\) with \(w\). Thus every joint integral of the declared \((x,y,w)\) functions is unchanged under that consistent convention change. The report preserves this valid exception. Integrated discriminators instead use omitted weights, the wrong moment measure, or a missing character dimension factor.

## 3. Exact character convolution

Let \(\chi_n\) denote the ordinary \(SU(2)\) character with dimension \(n+1\), so \(\chi_1=2x\). Its tensor-power multiplicity is

\[
 m(a,n)=\binom a{(a-n)/2}-\binom a{(a-n)/2-1},
\]

when \(a-n\) is even and \(0\leq n\leq a\); otherwise it is zero. A binomial coefficient outside its valid range is zero. Thus

\[
 x^a=2^{-a}\sum_n m(a,n)\chi_n(U).
\]

Character orthogonality and convolution give

\[
 \int\chi_n(U)\chi_\ell(UV^\dagger)dU
 ={\delta_{n\ell}\over n+1}\chi_n(V),
\]

and then integrating against \(\chi_m(V)\) gives a second Kronecker delta. Consequently,

\[
 \boxed{\mathbb E[x^a y^b w^c]=2^{-(a+b+c)}
       \sum_{n\geq0}{m(a,n)m(b,n)m(c,n)\over n+1}.}
\]

The dimension divisor is essential. The exact checks include

\[
 \mathbb E[xyw]=1/16,\qquad
 \mathbb E[x^2y^2w^2]=1/48.
\]

Treating the three trace coordinates as independent would give zero for the first expression. Deleting the divisor would give1/8. The second expression has both index0 and index2 contributions: \(2^{-6}(1+1/3)=1/48\). Independent Haar links therefore do not imply independent \(x,y,w\).

The producer computes all969nonnegative triples with \(a+b+c\leq16\), a complete superset of every moment used by the numerator and partition through degree8. The independent role instead expands

\[
 w=xy+\sqrt{(1-x^2)(1-y^2)}z,
\]

integrates even \(z\)-powers against uniform \([-1,1]\), and then uses independent semicircle moments for \(x,y\). It imports no producer character arithmetic. Endpoint degeneracy introduces no division by a vanishing sine in either exact method.

## 4. Hypothesis audit and changed weights

Write \(A(x)=(4x^2-1)^3\). One-coordinate Haar moments give

\[
 \mathbb E A=1,\qquad \mathbb E[A(4x^2-1)]=3.
\]

For example, the moments \(\mathbb E x^2=1/4\), \(\mathbb E x^4=1/8\), \(\mathbb E x^6=5/64\), \(\mathbb E x^8=7/128\) yield these identities by direct expansion. Character convolution then gives

\[
 \mathbb E[Ow^2]=\mathbb E[Oy^2]=1/324,\quad
 \mathbb E[Ox^2]=0,\quad\mathbb E[Oxyw]=1/324.
\]

For the last identity, \(4w^3-w=(\chi_3(w)+\chi_1(w))/2\), \(y=\chi_1(V)/2\), and the \(\chi_1\) coefficient of \(A(x)x\) is \(2\mathbb E[Ax^2]=2\). Only the common index1 survives, giving \(2\cdot(1/2)\cdot(1/2)/2=1/4\) before the observable's factor1/81.

The normalized expectation's numerator and partition have exact series

\[
 N_d(\kappa)=\sum_n N_{d,n}\kappa^n,\qquad
 Z_d(\kappa)=\sum_n Z_{d,n}\kappa^n,
\]

where the coefficients include all factorials from the exponential expansion. The first nonzero terms satisfy

\[
 N_{d,2}={d^2+1\over648},\quad N_{d,3}={d\over108},
 \qquad Z_{d,2}={10+d^2\over8},\quad Z_{d,3}={3d\over16}.
\]

In particular, the complete action has numerator quadratic5/648 and cubic1/54, and partition cubic3/8. The earlier planning estimate1/648 applied to the action missing both surrounding-only weights; it was not the complete integral. These values have now been derived and computed rather than accepted as planning constants.

At \(\kappa=0\), the two-link observable is exactly zero: integrating \(V\) annihilates the shared adjoint for each fixed \(U\). Freezing \(V=I\) instead produces \((4x^2-1)^4/81\), whose one-link mean is1/27. This provides an exact distinction between freezing and integrating the surrounding link.

## 5. The full normalized enclosure

Since \(x,y,w\in[-1,1]\), \(|\kappa S_d|\leq M=(4+d)|\kappa|\). Each normalized adjoint factor lies in \([-1/3,1]\), so \(|O|\leq1\). For the partial Taylor sum through degree \(N\), if \(M<N+2\), the full exponential remainder is bounded by

\[
 R_N={M^{N+1}\over(N+1)!}\,{1\over1-M/(N+2)}.
\]

The terms after the first omitted term have successively smaller ratios than \(M/(N+2)\), proving this exact geometric bound. The same \(R_N\) bounds both the integrated numerator remainder and partition remainder. If their partial sums are \(A_N,Z_N\), use

\[
 N_d\in[A_N-R_N,A_N+R_N],\qquad
 Z_d\in[\max(1,Z_N-R_N),Z_N+R_N].
\]

Jensen's inequality gives \(Z_d\geq1\), because the unweighted mean action is zero. Division compares all four endpoint quotients, retaining signed numerator intervals. The resulting interval encloses the **full normalized weighted integral**, rather than just a truncated series.

For the primary case \(d=2,\kappa=1/64\), \(M=3/32\):

| Degree | Approximate interval width | Sign result | Precision result |
|---:|---:|---|---|
|0|0.1967213|Unresolved|Insufficient|
|2|0.0002811694|Unresolved|Insufficient|
|4|\(1.22563\times10^{-7}\)|Positive|Insufficient|
|6|\(2.55466\times10^{-11}\)|Positive|Insufficient|
|8|\(3.11110\times10^{-15}\)|Positive|Target met|

The exact rational endpoints are authoritative in `refinement.csv`. No coarse stage is deleted or mislabeled as a failed physical model. Degree8 also certifies all nine final fixtures: \(d=2,1,0\) at \(\kappa=1/64,0,-1/64\).

The complete-action intervals for positive and negative coupling are disjoint, near \(1.95552781\times10^{-6}\) and \(1.81424704\times10^{-6}\). Thus the complete answer is not even in \(\kappa\). At positive coupling, the actions missing one and two weights give disjoint smaller values near \(7.89359175\times10^{-7}\) and \(3.77064878\times10^{-7}\). The \(d=0\) action has a valid separate evenness: \(U\mapsto-U\) flips \(3x+w\), preserves the observable, and leaves \(V\) untouched. Positive and negative \(d=0\) intervals therefore agree exactly. This symmetry must not be transferred to the complete action.

## 6. The common variable linking C1 to the surrounding measure

At fixed surrounding quaternion \(V\), let \(y=V_0\). Three central directions are \(e_0\), and the shared direction is \(V\). The central action vector is \(b(V)=\kappa(3e_0+V)\). Its complete joint Gram has

\[
 \|b\|^2=\kappa^2(10+6y),\quad b\cdot e_0=\kappa(3+y),\quad
 b\cdot V=\kappa(3y+1),\quad e_0\cdot V=y.
\]

All other Gram entries follow from the repeated unit directions. Both action cross and norm constraints are checked. The two-dimensional direction Gram has determinant \(1-y^2\geq0\); its rank is2 for \(|y|<1\) and1 at the endpoints. The executable cases \(y=-1,0,3/5,1\) compare every entry against explicit unit quaternions, including both rank-deficient endpoints.

C1's full-Gram sufficiency now justifies a one-variable description of the **central integral for this identity boundary**. It does not supply the surrounding measure. The actual Haar marginal is the semicircle density

\[
 \rho(y)={2\over\pi}\sqrt{1-y^2},\qquad -1\leq y\leq1,
\]

obtained by pushing uniform \(S^3\) measure onto its scalar coordinate. Its second moment is1/4, not the1/3 of a uniform scalar draw. With the two surrounding-only weights retained, the full conditional denominator and numerator are

\[
 \int\rho(y)e^{2\kappa y}Z_U(G(y))\,dy,
 \qquad\int\rho(y)e^{2\kappa y}N_U(G(y))\,dy.
\]

If the inner normalized quantity \(N_U/Z_U\) is used, its outer weight must include \(Z_U(G(y))\), as well as \(e^{2\kappa y}\). Dropping it changes the measure. Already the central partition's second-order term depends on \(10+6y\), so it cannot be silently treated as constant. The present direct two-link expansion computes the numerator and denominator without introducing a redundant nested numerical integrator.

This is the precise forward/backward connection: complete central coordinates meet the backward obligation of a correctly weighted actual outer integral. Arbitrary surrounding configurations would introduce more joint geometry; this special one-dimensional coordinate does not close the full bulk theory.

## 7. Code review and reproducibility

The implementation uses the standard library and canonical rational inputs. Public moment and multiplicity inputs are validated before caches; Boolean aliases, negative indices and unsupported total degrees reject. Cached moments are immutable Fractions, coefficient arrays are immutable tuples, and observable dictionaries are fresh defensive values. Graph, source, schema, normalization and required-fixture mutations are checked explicitly.

The early public `divide` helper used `Fraction` directly on endpoints and could accept Boolean endpoints as1, even when interval widths were omitted. Internally constructed scientific certificates were unaffected. Boundary review repaired the helper to require exact canonical lower/upper/width fields and a consistent width. The exact previous source was recovered by reversing that sole patch, and its incorrect admission was reproduced and preserved under `history/`; the retention method is documented there. Two direct public-helper controls now reject the malformed interval cases.

Run `python check.py --output ../c2-output` and `python -O check.py --output ../c2-output-optimized`. A dedicated child `output/` is also supported for relocation. `completecollection.json` stores the actual graph, all969moments, all coefficient arrays, all five refinement records, all nine signed/zero/omission fixtures, Gram cases and controls. `actualgraph.json`, `refinement.csv` and `weights.csv` provide inspectable geometry and exact plot data. Source and output manifests bind the evidence.

The **54 author checks** are separate from the independent angular derivation and complete comparison. Any floating quadrature supplied by the advisor is an additional labeled numerical cross-check; it does not replace these exact remainder bounds or add another research loop. This is the sixth and final authorized scientific loop of Round18.
