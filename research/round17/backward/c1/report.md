# Independent C1: the actual central four-adjoint Haar tensor

This phase integrates one link conditional on fixed surrounding links. It does not integrate the twenty-face bulk action, prove a Hamiltonian mass gap, or execute a finite-coupling C2 experiment.

## Actual graph and boundary

The four cells have lower corners (0,0,0), (1,0,0), (0,1,0), (1,1,0). The independent constructor enumerates every positive-axis unit link and every geometric unit square of the 3×3×2 vertex array. A separate cell-to-face incidence calculation gives 18 vertices, 33 links and 20 faces, with four internal faces. The central link (1,1,0)→(1,1,1) belongs to all four internal faces. The boundary-only face inventory uses 18 vertices, 32 links and 16 faces and omits precisely this link. Counts alone are supplemented by validation of every signed face word, its closure and its actual endpoints.

Each central face can be reversed as a whole and cyclically rotated so that its word starts with the central link U in positive orientation. The other three links form a path with product Hᵢ. These four paths are edge-disjoint outside U. Each contains exactly one other vertical link. Setting that link to Hᵢ or Hᵢ⁻¹ according to its signed occurrence, with the other boundary links equal to the identity, realizes all four prescribed path products simultaneously. Vertex sharing creates no inconsistency in link assignments. The executable fixture verifies each complete product U Hᵢ and its gauge-invariant character after a noncommuting vertex gauge transformation.

## Independent quaternion Haar construction

Write a unit quaternion q=(w,x,y,z), distributed uniformly on S³. The real spin-one representation is

\[
R(q)=\begin{pmatrix}
w^2+x^2-y^2-z^2&2(xy-wz)&2(xz+wy)\\
2(xy+wz)&w^2-x^2+y^2-z^2&2(yz-wx)\\
2(xz-wy)&2(yz+wx)&w^2-x^2-y^2+z^2
\end{pmatrix}.
\]

For nonnegative integers kⱼ the normalized moment is

\[
\mathbb E\prod_{j=0}^3q_j^{2k_j}
=\frac{\prod_j(2k_j-1)!!}{4\cdot6\cdots(4+2K-2)},\qquad K=\sum_j k_j,
\]

with empty products one; any odd exponent gives zero. These moments follow, for example, by taking the angular factor of four independent centered equal-variance Gaussians. Every entry of

\[
P_{a_1a_2a_3a_4,b_1b_2b_3b_4}
=\int\prod_{j=1}^4R(q)_{a_jb_j}\,d\mu(q)
\]

is a polynomial moment of degree eight. The independent implementation expands and integrates all 6,561 entries. Its cache only identifies permutations of the same four scalar rotation entries; it does not substitute a Gram projector or a rank-three assumption.

Haar invariance makes P the orthogonal projection onto invariant tensors. The pairings

\[
B_1=\delta_{ab}\delta_{cd},\quad B_2=\delta_{ac}\delta_{bd},\quad B_3=\delta_{ad}\delta_{bc}
\]

are linearly independent. Completeness follows from 1⊗1=0⊕1⊕2: coupling the first and second pairs to a singlet requires equal intermediate spins, with one invariant for each of 0, 1 and 2. Thus the invariant dimension is exactly three. Independently, the quaternion integral of the fourth adjoint character is three, agreeing with the trace of the full Haar projector.

Direct contraction gives the Gram matrix with diagonal 9 and offdiagonal 3. Its inverse has diagonal 2/15 and offdiagonal −1/30. The separately computed quaternion tensor agrees entry by entry with B G⁻¹ Bᵀ. Exact matrix calculations verify symmetry, P²=P, rank three and trace three. The total tensor generators for all three rotation axes annihilate P on both sides. This verifies invariance under the full connected SO(3) action, not only a sampled finite set of rotations; the adjoint SU(2) action factors through SO(3).

## A realizable signed conditional correlation

Choose the four unit quaternions

\[
H_1=(1,1,1,1)/2,\quad H_2=(1,1,-1,-1)/2,
\quad H_3=(1,-1,1,-1)/2,\quad H_4=(1,-1,-1,1)/2.
\]

They are orthonormal as four-vectors and pairwise noncommuting as group elements. For xᵢ(q)=Tr(qHᵢ)/2, the four directions are still orthonormal after changing the sign of the vector components. A Haar-preserving orthogonal change of quaternion coordinates therefore gives

\[
\int\prod_i\chi_2(qH_i)\,d\mu(q)
=\mathbb E\prod_{i=0}^3(4q_i^2-1)
=1-4+4-\frac43+\frac2{15}=-\frac15.
\]

The four normalized adjoint insertions divide this by 3⁴, giving **−1/405**. Each individual normalized adjoint mean is zero. Their product therefore fails to reproduce the nonzero joint mean. This negative correlation does not violate positivity of Haar measure or of the projector: the inserted character product is not a positive observable.

The tensor contraction of the full independently integrated P with the four actual adjoint boundary matrices gives the same −1/405. Removing the offdiagonal inverse-Gram terms instead gives **+2/405** and a matrix that is not idempotent. Keeping the single normalized channel B₁B₁ᵀ/9 gives **+1/729**; that rank-one operator is a projector but is incomplete. These controls distinguish a full Haar tensor from a positive scalar, independent-marginal product or arbitrary single channel.

## Scope of the check

`geometry.py` is a fresh graph constructor, signed-word validator and quaternion boundary assignment. `projector.py` uses exact S³ moments as its primary oracle and exposes the separate Gram comparison only afterwards. `check.py` includes named positive tests and deliberately malformed graph, quaternion and moment controls. The finite-coupling action, Taylor bounds and any bulk integration remain for an advisor-authorized later phase.

The advisor found a real public-cache defect after the first 28-check run. Validation inside the cached `sphere_moment` function was bypassed when `(False,0,0,0)` matched an already cached `(0,0,0,0)` key. `entry_moment` also accepted Boolean and negative Python indices because it checked only tuple length. The exact initial source, passing test result and actual three accepted-invalid-input observations are retained under `history/`. The new public wrappers require a tuple, exact integer types, nonnegative exponents and rotation indices 0 through 8 before calling private cached functions. Immutable Fraction values remain cached. This was a previously documented validation lesson that the initial test missed: a cold Boolean-one probe did not exercise the warm Boolean-zero alias. The corrected controls explicitly warm matching valid keys first and test the public boundary, in addition to negative, oversized and wrong-container inputs. No accepted physical tensor entry changes.

The corrected independent suite passes **34 named checks**. The separate complete producer comparison passes **14 named checks**; normal and optimized Python outputs are byte-identical, with each check counted once. The comparison reconstructs the entire graph, every cell incidence and signed path, all boundary assignments, all 6,561 tensor entries, normalization, source binding and conditional scope. There is no remaining material discrepancy between the independent S³ and producer Gram-projector calculations. The retained cache failure concerns the independent implementation's input validation and remains visible rather than being overwritten by the corrected pass.

The focused source review covered the new graph constructors and validators, signed reorientation and boundary assignment, the public/private cache boundary, the full tensor construction, invariant dimensions and complete certificate replay. The producer's no-argument invariant-data cache returns immutable tuples; its certificate entry point checks current source bytes before reading the cached construction. This review does not claim to audit every historical repository file.

Run `python check.py --output ../c1-reproduced` from this source directory. The separate comparison command is `python compare.py --producer <forward-c1-source> --evidence <forward-c1-output> --output ../c1-comparison-reproduced`. Each output must be a new directory outside the frozen source directory. C2 remains unexecuted pending the next advisor gate.
