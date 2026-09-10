# C1: sufficient joint coordinates for the declared central integral

The complete joint Gram matrix of \(b,a_1,a_2,a_3,a_4\) is sufficient for the **central** integral in the family

\[
 Z(t)=\int_{S^3}e^{tq\cdot b}\,d\sigma(q),\qquad
 A(t)=\int_{S^3}{\prod_{i=1}^4(4(q\cdot a_i)^2-1)\over81}
                   e^{tq\cdot b}\,d\sigma(q),
 \quad b=\sum_i\kappa_i a_i,\quad \|a_i\|=1.
\]

Here \(d\sigma\) is normalized Haar/sphere probability measure. Equal full Grams give equal untruncated \(A(t),Z(t)\), and therefore equal normalized central expectations, for every real \(t\). This is an ordinary mathematical proof. The executable diagnostics independently test all Taylor coefficients through degree6; they are not a proof-assistant certificate or a finite-\(t\) truncation-error estimate.

The partition alone needs only \(\|b\|^2\), but the joint observable generally does not. The retained equal-action counterexample has \(A_T(0)=-1/405\) and \(A_C(0)=13/1215\). Introducing the complete Gram repairs that insufficient coordinate description for this declared central family. **It neither replaces the surrounding-link measure nor completes the full lattice problem.**

## 1. Conventions and frozen fixtures

Vectors are ordered \(v=(b,a_1,a_2,a_3,a_4)\), and \(G_{ij}=v_i\cdot v_j\). The observable uses the normalized adjoint character \((4x_i^2-1)/3\) four times, hence the denominator81. The action coefficients \(\kappa_i\) and the bookkeeping parameter \(t\) are dimensionless Euclidean quantities. They are separate from the physical Hamiltonian energy scale \(\alpha\) in GoalB. **\(t\) is a formal expansion parameter, not physical time.**

The current tetrahedral direction rows are

\[
 \tfrac12(1,1,1,1),\quad\tfrac12(1,1,-1,-1),\quad
 \tfrac12(1,-1,1,-1),\quad\tfrac12(1,-1,-1,1),
\]

and the commuting rows are \(e_0,e_0,e_1,-e_1\). Their common coefficients \(\kappa_i=1/16\) give the same \(b=(1/8,0,0,0)\), while their four-direction Grams differ.

**Round17 convention clarification.** The earlier report defined the trace directions from boundary quaternions as \(a=(h_0,-h_1,-h_2,-h_3)\). The present base fixtures use the listed \(h\) coordinates as direction vectors. They are not silently identified as the same coordinate arrays: the common orthogonal reflection

\[
 J=\operatorname{diag}(1,-1,-1,-1)
\]

maps every current direction and the action vector to the earlier convention. It preserves the complete Gram. For the common scalar-axis action, \(Jb=b\), so even those action coordinates are unchanged. For general coefficients the action must transform together with the directions. The code explicitly checks this relation and all degree-zero-through-six coefficients.

The eleven fixtures are:

| Fixture | Geometry or exception |
|---|---|
| tetra_common | Four orthonormal tetrahedral directions; common \(\kappa=1/16\) |
| commuting_common | \(e_0,e_0,e_1,-e_1\); same common coefficient |
| tetra_hadamard | A common Sylvester Hadamard rotation of all five tetrahedral vectors |
| commuting_hadamard | The same rotation applied to the commuting vectors |
| tetra_reflected | A common reflection negating coordinate0 |
| commuting_reflected | The same reflection applied to the commuting vectors |
| rank1_equal | Four equal \(e_0\) directions |
| rank2 | \(e_0,e_1,(3/5,4/5,0,0),(-4/5,3/5,0,0)\) |
| tetra_zero_kappa | All four coefficients vanish |
| tetra_signed_kappa | \((1/16,-1/32,1/8,-3/64)\) |
| commuting_zero_b_nonzero_kappa | \((1/16,-1/16,1/16,1/16)\), giving \(b=0\) |

The Hadamard rows are \((++++),(+-+-),(++--),(+--+)\), divided by2. Each transform acts on every vector together; rotating the action while keeping the observable fixed would not be the same operation.

## 2. Complete admissibility, including degenerate cases

For real data, require symmetry, positive semidefiniteness, \(\operatorname{rank}G\leq4\), and \(G_{ii}=1\) for \(i=1,\ldots,4\). Also require **both**

\[
 G_{0i}=\sum_{j=1}^4\kappa_jG_{ji}\quad(i=1,\ldots,4),\qquad
 G_{00}=\sum_{i,j=1}^4\kappa_i\kappa_jG_{ij}.
\]

A real PSD matrix of rank at most4 has a realization in \(\mathbb R^4\). In that realization, these constraints give

\[
 \left\|b-\sum_i\kappa_i a_i\right\|^2
 =G_{00}-2\sum_i\kappa_iG_{0i}+\sum_{i,j}\kappa_i\kappa_jG_{ij}=0,
\]

so the declared action relation really holds. No inverse Gram or division by \(\|b\|\) is required. Thus rank1, rank2, and \(b=0\) with nonzero cancelling coefficients are legitimate exceptions.

The executable algorithm accepts exact canonical rational Gram entries and coefficients. Its admissibility theorem is over real data; a rational Gram need not have a rational realization, and no such extra requirement is imposed by `validate`. Rational explicit vector fixtures are a separate way to produce test inputs.

PSD validation uses exact Schur elimination: select a strictly positive diagonal pivot; form its exact Schur complement; repeat. A negative diagonal rejects. If every remaining diagonal is zero, PSD requires every remaining entry to vanish; a nonzero off-diagonal rejects without division by a zero pivot. Positive pivot count gives the rank. This checks the complete matrix, including rank-deficient cases.

Testing only leading principal minors would fail. An explicit rejected Gram has a zero first row/column, unit direction diagonals, and \(G_{12}=G_{21}=2\). All leading principal minors vanish, but the directions1,2 principal minor is \(1-4=-3\). The independent reviewer instead uses all principal minors and a separate exact rank calculation.

## 3. Isometry proof: forward and backward obligations

**Backward obligation.** To prove equality of the central integrals, it suffices to find a common orthogonal transformation carrying all five vectors to the comparison vectors and then change the integration variable.

**Forward construction.** Suppose \(v_i\) and \(w_i\) have the same complete Gram. Define

\[
 T\left(\sum_i c_iv_i\right)=\sum_i c_iw_i.
\]

If the first combination vanishes, its squared norm is \(c^TGc=0\), and the second combination has the same squared norm and also vanishes. Thus \(T\) is well-defined despite linear dependence. Equality of the Grams preserves every inner product, so \(T\) is an isometry between the spans. Their equal-dimensional orthogonal complements can be matched with orthonormal bases, extending \(T\) to \(O\in O(4)\).

Normalized sphere measure is invariant under every such \(O\), including determinant-minus-one reflections. Substituting \(q\mapsto Oq\) preserves every dot product with the correspondingly transformed vector. It therefore preserves the full observable, exponential, and integral. The sphere is compact, so the integrals exist for all real \(t\), and the positive exponential gives \(Z(t)>0\).

The forward construction meets the backward requirement even in singular-rank and zero-action cases. This does not assert a change of variables on the surrounding link configurations with a known Jacobian, nor sufficient coordinates for undeclared orientation-sensitive observables. In particular, the Gram theorem cannot justify forgetting which surrounding configurations produced it or how they are weighted.

## 4. Exact Gram recurrence

Define

\[
 M(k)=\int_{S^3}\prod_{i=0}^4(q\cdot v_i)^{k_i}\,d\sigma(q).
\]

Then \(M(0)=1\), and odd total degree gives zero by the antipodal symmetry. For even \(D=|k|>0\), choose any \(i\) with \(k_i>0\). Gaussian integration by parts, followed by separating a four-dimensional standard Gaussian into its independent radius and unit direction, yields

\[
 M(k)={\sum_j(k_j-\delta_{ij})G_{ij}M(k-e_i-e_j)\over4+D-2}.
\]

The radial even moments obey \(E[R^D]=(4+D-2)E[R^{D-2}]\), supplying the denominator. The code skips a zero multiplicity **before constructing the reduced exponents**. Otherwise, a formal term with zero coefficient could unnecessarily generate a negative exponent and invalidate a correct recurrence branch.

The cached key is the complete immutable Gram together with the exponent tuple. All public entry points first check the full Gram constraints and exact exponent types, including rejection of Boolean aliases. Cached values are immutable `Fraction` objects. Coefficient arrays are returned as tuples; certificate dictionaries are defensive fresh objects and replay rejects changes.

For each subset \(S\subseteq\{1,2,3,4\}\), the declared product expansion has coefficient \(4^{|S|}(-1)^{4-|S|}/81\) and powers2 on the selected directions. Therefore

\[
 [t^n]A(t)={1\over81n!}\sum_S4^{|S|}(-1)^{4-|S|}
 M(n,2\mathbf1_{1\in S},\ldots,2\mathbf1_{4\in S}),
 \qquad[t^n]Z(t)={M(n,0,0,0,0)\over n!}.
\]

The observable degree8 plus \(n\leq6\) requires moments through degree14. Each of the eleven fixtures contains all112 primitive moments, so the exact evidence contains1232 values as well as the77 numerator and77 partition coefficients. Odd coefficients vanish because this observable is even under \(q\mapsto-q\). This parity must not be transferred to an unrelated surrounding action without proving that action's symmetry.

## 5. Findings and verification scope

The tetrahedral, commuting, rank1 and rank2 unweighted joint values are respectively

\[
 -{1\over405},\qquad {13\over1215},\qquad {1\over27},\qquad {1213\over759375}.
\]

Common Hadamard and reflected fixtures preserve every complete Gram, primitive moment, numerator coefficient and partition coefficient. The equal-action tetrahedral and commuting fixtures preserve the partition but retain different joint observables. Both zero-action branches have partition1 and all positive-degree coefficients zero, including the case with nonzero cancelling \(\kappa_i\).

The **37 author checks** cover the complete fixture inventory, every primitive reconstruction and factorial, low-order sphere identities, degenerate geometry, non-PSD/rank5/nonunit inputs, separate forged action cross and norm relations, malformed Boolean data after a cache is warm, negative powers, immutable results, source/schema changes and an omitted fixture. A temporary copy is modified after import to verify the source-change rejection; the active source is preserved. This loop inherited the prior mutable-metadata lesson and checks an immutable declaration snapshot before admission. No new observed implementation defect has been claimed; the historical quaternion convention correction is explicitly documented instead of being hidden or labeled a failed scientific calculation.

The independent role reconstructs coordinate polynomials and integrates their monomials over \(S^3\), without importing the Gram recurrence. Its complete comparison and the advisor gate are separate from these author checks.

## Reproduce and continue

Run `python check.py --output ../c1-output` and `python -O check.py --output ../c1-output-optimized` from the source directory. The accepted archival form with a dedicated child `output/` is also supported. Outputs cannot overwrite the source directory itself or an ancestor. `collection.json` preserves exact data and the historical convention; `coefficients.csv` exposes all77 coefficient pairs; source and output manifests bind the bytes. The first full collection took about0.06 seconds in this environment; timings are informational and are not included in reproducibility hashes.

The theorem supplies the complete central coordinates. The remaining backward obligation is a genuine surrounding-link integration that retains every dependence and normalization weight. C2 has not been executed in this loop.
