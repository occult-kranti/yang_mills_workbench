# Independent B1: a complete electric complement and exact cross operator

This result concerns the full Gauss-invariant SU(2) link Hilbert space of the actual adjacent-two-cube graph. It verifies QH₀Q≥9α/2 and the exact bounded cross Gram (QVP)*QVP for a specified 12-dimensional physical subspace P. It does not yet execute B2's interacting gap estimate or supply a volume-uniform dense result.

## Graph, spectrum and the entire omitted space

The graph is independently rebuilt from vertices (x,y,z) with x=0,1,2 and y,z=0,1. It has 12 vertices, 20 positive-axis links and 11 elementary faces. Every signed face word is reconstructed from adjacent vertices. Let χ_p=Tr(U_p)=2x_p. The physical subspace P is the span of Ω=1 and all eleven fundamental face characters. Exact Haar orthogonality makes these twelve vectors orthonormal. Each χ_p has electric energy 4α(1/2)(3/2)=3α.

The Peter–Weyl spin-network basis of the full physical Hilbert space assigns irreducible spin j_e∈{0,1/2,1,…} to every link and invariant intertwiners at vertices. It diagonalizes H₀=αΣ_e C_e, with energy αΣ_e j_e(j_e+1). At a vertex with exactly one nontrivial incident representation, no invariant vector exists. Thus a nonempty active support must have minimum active degree at least two. This condition is necessary, not a claim that every larger support is automatically admissible.

An eigenstate with energy below 9α/2 has at most five active links, because each costs at least 3α/4. The graph is simple and bipartite. A nonempty component of minimum degree two contains a cycle, with at least four vertices and edges. With at most five edges there can be only one such component. Four active vertices in a simple bipartite graph admit at most four edges; five active vertices with at most five edges and minimum degree two force every degree to equal two, hence a five-cycle, which bipartiteness forbids. Fewer than four active vertices cannot contain a cycle. Therefore the only allowed nonempty support below the threshold is a four-cycle. This also explicitly excludes a hidden multicycle support.

Two independent finite graph checks substantiate this classification: all 21,700 subsets of at most five of the twenty links are enumerated, and a separate path-based cycle search finds every four-cycle. Only the empty support and the eleven actual face boundaries survive the necessary degree condition. On a degree-two cycle, Schur's lemma forces adjacent spins to agree and each two-valent intertwiner is unique up to scale. For a common fundamental spin, the state is exactly χ_p; for spin at least one, its energy is at least 4α·2=8α. The vacuum is the unique all-trivial state. Hence all physical eigenstates below 9α/2 lie in P.

The finite compact link manifold gives a self-adjoint electric Laplacian with compact resolvent. Its Gauss-invariant subspace is reducing, and the complete spin-network expansion extends the spectral inequality from basis vectors to the quadratic form domain. Thus

\[
QH_0Q\ge\frac92\alpha Q,\qquad Q=1-P.
\]

This is not a tail inferred from a sampled spin cutoff. A closed fundamental rectangle follows six actual links around the two coplanar squares. Its normalized character state has energy 6·3α/4=9α/2. Its support differs from every face support and from the vacuum; an odd exclusive-edge Haar integral proves each required orthogonality. It lies in Q and saturates the threshold. Raising the threshold for this same P is therefore false. Conversely, removing even one fundamental face from P leaves a Q state with energy 3α and invalidates the proposed 9α/2 lower bound.

## Complete moments through order four

Under a link center transformation U_e→−U_e, χ_p changes sign precisely when e belongs to that face. If the mod-two sum of the participating actual face boundaries has an odd link, the Haar product is zero. The program records an actual odd-edge witness whenever this argument is used. It checks every four-distinct-face combination, so no unexamined closed four-face surface is assumed away.

For repeated factors, hold every other link fixed and integrate an actual face-exclusive link. Its normalized trace is a unit linear form in a Haar quaternion q∈S³. Sphere symmetry gives E q₀²=1/4. At fourth order write a=E q₀⁴ and b=E q₀²q₁². A 45-degree rotation gives a=3b, while E(Σq_i²)²=1 gives 4a+12b=1. Hence a=1/8. Therefore Eχ_p²=1 and Eχ_p⁴=2. Distinct elementary faces have an exclusive link; integrating that link in χ_p²χ_q² gives one pointwise in the other links, and the remaining square also integrates to one. Thus Eχ_p²χ_q²=1 even for adjacent faces sharing links.

The resulting complete fourth classification is

\[
\mathbb E[\chi_p\chi_q\chi_f\chi_h]=
\begin{cases}
2,&p=q=f=h,\\
1,&\text{two distinct pairs},\\
0,&\text{all other multiplicity patterns on this graph}.
\end{cases}
\]

All 1,001 sorted four-index multisets are retained with their permutation multiplicities, accounting for all 11⁴=14,641 ordered products. Lower moments are reconstructed as well. Every mixed triple vanishes, and Eχ_pχ_q=δ_pq.

## The full cross operator, including the P subtraction

Let V=−Σ_f λ_fx_f=−(1/2)Σ_f λ_fχ_f with arbitrary real couplings. Finite rational fixtures are implementations, not restrictions of the mathematical statement. Put W=QVP. In the orthonormal P basis, the only nonzero PVP entries are (PVP)₀p=(PVP)p₀=−λ_p/2. The independent implementation first computes every entry of PV²P directly from the preceding moments, separately multiplies (PVP)², then subtracts:

\[
W^*W=PV^2P-(PVP)^2.
\]

With T=Σ_f λ_f², the electric-face block of PV²P has diagonal (T+λ_p²)/4 and off-diagonal λ_pλ_q/2. Its vacuum diagonal is T/4; mixed vacuum/face entries vanish. The P subtraction has vacuum diagonal T/4 and face entries λ_pλ_q/4. Consequently W*W has an identically zero vacuum row and column and

\[
C_{pp}=\frac T4,\qquad C_{pq}=\frac{\lambda_p\lambda_q}{4}\quad(p\ne q).
\]

This exact 12-by-12 matrix captures the full bounded operator W from P into the infinite-dimensional Q space; no finite list of Q states replaces the range. Positivity follows from the operator Gram identity. For |λ_p|≤αr, each absolute row sum is at most (11+10)α²r²/4, giving ||W||²≤21α²r²/4. If every magnitude equals αr, write λ_p=αr s_p with signs s_p. The face block is α²r²(10I+ssᵀ)/4; its exact largest eigenvalue is 21α²r²/4. The zero-coupling case is included without dividing by r. Separately, QHQ≥(9α/2−Σ|λ_f|)Q follows by a bounded-potential estimate. Neither statement alone is presented as B2's finished spectral-gap theorem.

## Corrected negative controls

The initial advisor request and the previous post-A review suggested that an independent-face model should already fail a fourth-order test. The forward researcher correctly challenged this. The actual joint moments through degree four agree with independent one-face Haar marginals. This independent implementation confirms that equality for the entire fourth inventory. A limitation of fourth-order information is not evidence of a failed fourth-order independence prediction. The frozen planning text is preserved and this correction is recorded explicitly.

Two genuinely discriminating fourth-order controls remain. Gaussian centered variables with the same second moment have same-variable fourth moment three rather than Haar two; substituting that value changes a face cross diagonal by λ_p²/4. Deleting the P subtraction falsely creates the vacuum cross diagonal Σλ²/4, although VΩ lies entirely in P and WΩ must vanish. Both controls are computed on declared nonzero fixtures.

These controls falsify the claimed exact moments or exact W*W identity. They do not invalidate every conservative estimate using a larger matrix: PV²P is itself a valid positive-semidefinite upper bound on W*W, since their difference is (PVP)²≥0. The exact subtraction is required for the sharper formula accepted here. A Gaussian discrepancy alone likewise does not disprove an independently justified conservative upper estimate.

Full face independence fails at a separately computed sixth-order observable. On the actual left cube, the program orients all six face words outward, verifies each of twelve links occurs once as U and once as U†, and integrates their fundamental matrix entries. Each link supplies the exact factor 1/2 and two Kronecker index identifications. Union of the actual trace-index pairings gives eight free index loops. Summing them yields 2⁸/2¹²=1/16 for the ordinary six-face character product. Independent centered face characters instead give zero. This is a fresh signed-index contraction, not a numerical estimate or an asserted Euler-characteristic shortcut, and it is kept separate from the fourth-order Gram.

## Verification boundary

The fixed fixture inventory contains zero, positive, negative, alternating, single-channel, mixed signed/zero and canonical 3/8 coupling vectors, together with two nonunit α scales. Full Gram, PVP, PV²P, P subtraction and cross matrices are retained for each. Electric thresholds scale with α; cross Grams scale with the square of the physical couplings. Exact model schemas, signed words and all eleven coefficient channels are required. The discarded-face and six-edge witnesses attack the full-complement premise directly.

No floating eigensolver is used as a full-space acceptance oracle. The interacting scalar lower bound, its signed coefficient box and radical enclosures belong to B2 and require a new advisor gate.

The completed standalone run has 34 named checks. A separate 27-check comparison reconstructs the full producer collection: all 21,700 support records, every fourth multiset, the six-edge witness, nine complete matrix fixtures, amended controls and the exact cross-norm CSV. It also reconstructs the producer's face-orientation convention; reversing an entire fundamental SU(2) face does not change its real trace. The inherited graph's Euclidean metadata is retained as provenance, while the certificate independently declares the physical α,λ Hamiltonian. Its old action labels do not define the new energy scale.

The active producer implementation, runner, graph and referenced Haar routines were read at function and file scope; no new material implementation defect was found. The substantive correction in this loop was the invalid requested fourth-order independence discriminator, retained in planning-correction.json and the advisor's amendment. The fresh six-face index result supplies a valid higher-order control. Deliberate schema mutations reject omitted supports, projection or coefficient channels, Gaussian moments presented as exact Haar values, unsubtracted PV²P presented as exact W*W, false tail thresholds, Boolean signed-word aliases, source changes and forged external pass flags. Both scientific and comparison outputs are byte-identical under ordinary and optimized Python. The manifest binds final sources and outputs; these counts represent separate checks, not a formal proof-assistant certification.
