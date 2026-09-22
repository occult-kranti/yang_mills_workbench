# AN1 forward: HNM common-bulk boundary comparison

Human project author: **Hruday N M (BUNZEEY)**. Independent forward execution under the frozen contract, without current reverse or skeptic results. The theorem below applies an existing locality theorem to this exact boundary dictionary; scientific priority is unverified.

**Finite comparison:** write `A_n=[-n,n]^3`, the coarse translate of `[0,2n]^3`, and `B_n=[-2n,2n]^3`. For the contracted identical coarse-homogeneous selected coefficient triple and omitted tau, the actual whole-star ground states obey, for `Y={0,e_z}` and n>=3,

\[
\sup_{\|A\|\le1,\ A\in B(\mathcal H_Y)}
|\rho_{A_n}(A)-\rho_{B_n}(A)|
\le\min\{2,\exp(2C_1-C_2(n-2))\}.
\tag{HNM-AN1.1}
\]

This uses the **additional** source smallness `7|tau|<=c_HTW(1,1)`, with positive unevaluated source constants. They are not AM2's numerical radius or I1's c1,c2. Infinite-state identification is not this loop's result.

## 1. Common Hilbert space and canonical interior

Extend rho_(A_n) to B_n by the actual onsite vacuum product outside A_n; call the resulting normal state rho1. It is the ground state of

`H1=H_(A_n)+sum_{x in B_n\A_n}h_x`.

Let rho2 be the actual whole-star ground of `H2=H_(B_n)`. Both are trace-one densities on the **same** finite tensor Hilbert space. The original compact elliptic rotor ground exists and is unique/positive for the bounded real finite interaction; this assertion does not require guessing a theorem constant.

Set Lambda_*=A_n and define the source canonical restriction

\[
H_*=\sum_{x\in A_n}h_x+
\sum_{x:\operatorname{dist}_1(x,A_n^c)>1}\phi_x.
\tag{HNM-AN1.2}
\]

The retained source anchors are exactly `[-n+1,n-1]^3`. Each source phi_x is supported in the radius-one l1 ball about x because the whole star S is contained in that ball, even though S has l1 diameter two. Its norm is M=7|tau|, and the onsite normalized gap is at least one. This matches HTW Definition1 with R=1 and g=1; R=0 would discard actual neighboring factors.

The source bulk from Definition6 is the twice-eroded set

\[
D_n=A_n^\circ=\{x:\operatorname{dist}_1(x,A_n^c)>2\}
=[-n+2,n-2]^3.
\tag{HNM-AN1.3}
\]

Actual whole-star anchors of A_n are `[-n,n-1]^3`, not the canonical source anchors. Their extra groups have some base coordinate -n, and every point of their star has that coordinate at most -n+1; therefore their support misses D_n. For H2, every anchor not in the canonical set has a coordinate <=-n or >=n. Its star has that coordinate <=-n+1 or >=n, again outside D_n. Onsite terms outside A_n also miss D_n. Thus each `H_i-H_*` is supported outside D_n, including all missing/extra incoming stars. Equality of boundary Hamiltonians has not been assumed.

## 2. Unbounded-domain ground condition

It remains to prove the source's ground-in-the-bulk hypothesis, rather than equate states from a common gap. A source test operator T is bounded and supported in D_n, preserves `D(H_(0,D_n))`, and has bounded commutator with that local onsite sum. For a finite sum of nonnegative commuting tensor onsite operators,

`D(H_(0,B_n))=D(H_(0,D_n)) intersect D(H_(0,B_n\D_n))`.

Identity extension of T commutes with the exterior spectral projections and preserves the latter domain. It consequently preserves the full domain. Every finite interaction is bounded, so each H_i has that same onsite domain. Every interaction in `H_i-H_*` acts in the disjoint tensor factor outside D_n, and commutes with T; the exterior onsite terms commute on the stated domain as well. Hence

\[
[H_i,T]=[H_*,T]\quad\hbox{as bounded extensions},\qquad i=1,2.
\tag{HNM-AN1.4}
\]

Their genuine ground vectors Psi_i therefore give

`Tr rho_i T*[H_*,T]=<T Psi_i,(H_i-E_i)T Psi_i> >=0`.

This is exactly HTW Definition6's ground-in-the-common-bulk condition. It does not assume every bounded local T preserves an unbounded generator domain. The code retains a rank-one counterexample to that false universal domain claim. The output observable A in (HNM-AN1.1), in contrast, may be any bounded operator in the local factor, as allowed by the source theorem after the ground condition has been established.

## 3. The theorem and exact distance

Henheik–Teufel–Wessel, arXiv:2106.13780v3, Definitions1,2,6, Theorem7 and Lemma8, permit infinite-dimensional onsite factors and a bound on two normal states ground in a common weakly interacting bulk. The required interaction threshold c_HTW and decay constants C1,C2 are existential. Their Theorem7, attributed there to Yarotsky, applies to rho1,rho2 and H_* and gives

`|Tr((rho1-rho2)A)| <= exp(C1|Y| - C2 dist(Y,Z³\D_n)) ||A||`.

For Y={0,e_z}, |Y|=2 and the exact l1 distance to the complement of D_n is n-2 for n>=3 (the e_z point is nearest the upper z boundary). This proves (HNM-AN1.1). The bound is uniform over the full norm-one bounded local algebra, hence is also the trace-norm bound on the two Y-marginals and applies to its gauge-invariant subalgebra.

Y consists of **48 actual links and 36 distinct original endpoints**. Gauge actions at all those endpoints are preserved by the coarse translation `(4n,2n,n)` in fine coordinates and by both boundary prescriptions. Coarse translation invariance is essential: the same selected triple is used in every factor. Mere membership in coefficient ranges would not identify the translated interaction.

## 4. Controls and limits

The checker reconstructs both boundary inventories and all star supports for n=3,4,5, computes the eroded set and exact distance, and verifies that every boundary-difference group misses D_n. It reconstructs four incoming/outgoing anchors of an interior singleton and seven for Y; keeping only the two anchors in Y loses five groups. It also checks the 48-link/36-endpoint completion.

A near-boundary region with a point at `(-n,0,0)` has distance zero to the complement of D_n for all n; this comparison gives no vanishing enclosure there. A changed interaction at a bulk anchor generally fails (HNM-AN1.4); an exact matrix commutator demonstrates that support overlap cannot be dropped. Changing a translated selected coefficient also destroys the common model. The additional source smallness is retained symbolically; it cannot be deleted or replaced by the explicit AM2 gap radius without a new theorem.

The numerical fixtures are geometry and domain countercontrols, not simulated expectation values. We have proved a conditional finite comparison, and have not yet identified the actual inherited orthant state with any centered-box state. That requires a separate limit argument under the full simultaneous premises, including I1's `|tau|<tau_*` whenever that inherited state is invoked.

Reproduce: `python -B research/round29/forward/an1/check.py --output /absolute/new/output`.
