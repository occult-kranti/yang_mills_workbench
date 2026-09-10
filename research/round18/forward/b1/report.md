# B1: the complete physical complement and magnetic cross operator

## Fixed operator and complete projection

Use the actual two-cube graph with twelve vertices, twenty links and eleven distinct faces, including its shared face once. The saved graph/Haar utility retains its historical Euclidean metadata, including time_generator:none. B1 reuses only that actual geometry and the unweighted Haar inner products. The current physical contract is separately explicit: H=alpha sum C_e-sum lambda_p x_p on the full untruncated all-vertex Gauss-invariant SU(2) link Hilbert space, with no external charges, alpha>0, C_e=j(j+1), x_p=Tr(U_p)/2 and chi_p=2x_p. This Hamiltonian generator is not inferred from the earlier kappa labels, and no Euclidean coefficient is silently identified with a physical energy.

Let P project onto the vacuum Omega and all eleven ordinary fundamental face characters. Their Gram matrix is the identity, and H0 acts as zero on Omega and 3alpha on every face state. These are smooth physical states in the operator domain, so P reduces H0. The finite-graph electric Laplacian has compact resolvent and the standard elliptic domain; bounded real Wilson multiplication preserves its domain and closed form. Its gauge-invariant restriction is reducing. Q=1-P is an infinite-dimensional physical complement, not a representation cutoff.

## Completeness below 9alpha/2

In the Peter–Weyl spin-network decomposition, every nontrivial link has j>=1/2 and Casimir at least 3/4. A physical state of electric energy below 9alpha/2 therefore has at most five nontrivial links. A vertex with exactly one active incident link cannot carry an invariant intertwiner under its Gauss constraint. Hence active support has no degree-one vertex. The actual graph is simple and bipartite, so it has no odd cycles.

The code enumerates every one of the sum_(k=0)^5 binomial(20,k)=21700 edge supports. Apart from the empty support, exactly eleven pass the necessary no-leaf condition. Each is a four-cycle, and their edge masks are exactly the eleven elementary faces. This complete finite graph classification excludes disconnected multicycle supports, hidden short cycles and branched supports at this energy; a selected loop list alone would not suffice.

At every degree-two active vertex, the invariant in V_j tensor V_k* exists only for j=k and has multiplicity one. Thus an admitted four-cycle has one common spin on all four edges. Spin 1/2 gives energy 3alpha and precisely the corresponding fundamental face state. Any common spin at least one costs at least 8alpha, already above the threshold. The empty support is the vacuum. This exhausts the entire physical electric spectrum below 9alpha/2, not merely a finite family of trial vectors. Therefore

    Q H0 Q >= (9alpha/2) Q.

A six-edge elementary rectangle surrounding two coplanar adjacent squares supplies an exact state in Q. Its ordinary fundamental Wilson-loop character has norm one by one-link Haar integration, energy 6*(3alpha/4)=9alpha/2, and zero inner product with the vacuum and each P face by an odd-link center transformation. Its signed word is retained. This proves sharpness of the electric complement threshold and rejects any larger threshold unless the projection is changed. Omitting one face from P instead leaves an actual energy-3alpha state in Q.

## Entire repeated fourth-moment classification

The character functional is computed on the actual signed graph using the independently accepted two-disk gluing formula. For four indices, the complete classification is

    E[chi_p^4]=2,
    E[chi_p^2 chi_q^2]=1 for p!=q,
    every other fourth-index pattern has expectation zero.

All 1001 sorted multisets are retained with permutation multiplicities covering all 14641 ordered products. The complete mod-two boundary of each product is saved. In particular, every one of the 330 four-distinct-face subsets has a nonempty odd boundary, so its expectation vanishes. Patterns 3+1 and 2+1+1 also have an odd boundary.

Parity does not establish the repeated even cases. For one face, chi_1^2=chi_0+chi_2 and character orthogonality give E chi_1^4=2. For two distinct faces, an edge of the first absent from the second allows conditional Haar integration of chi_p^2 to one, leaving E chi_q^2=1. These facts justify the classification without assuming a general distributional independence of face holonomies.

The advisor's original B1 contract requested a false independent-fourth-moment model as a discriminator. The forward review found that genuinely independent one-face Haar variables do reproduce this degree-four classification. The accepted b1-amendment.md therefore corrects the control: Gaussian/Wick fourth moment three is wrong, while the low-degree Haar agreement is retained as true. General independent-face factorization is separately rejected by the already accepted six-face cube product: the ordinary-character moment is 1/16, whereas six independent zero-mean characters would give zero. No artificial fourth-order failure is claimed.

## Separate PV²P and projection subtraction

Write V=-sum_p lambda_p chi_p/2 and W=QVP. Since P is orthogonal,

    W*W = P V Q V P = P V² P - (P V P)².

Both matrices are reconstructed separately for every fixed coefficient vector. PVP only couples the vacuum and the individual faces, with entry -lambda_p/2. Its squared vacuum entry is sum lambda²/4 and its face block has entries lambda_p lambda_q/4. PV²P has the same vacuum entry and zero vacuum/face entries; its face diagonal is (sum lambda²+lambda_p²)/4 and its off-diagonal is lambda_p lambda_q/2. Thus the full cross Gram C=W*W has

    C_00=C_0p=C_p0=0,
    C_pp=sum_q lambda_q²/4,
    C_pq=lambda_p lambda_q/4 for p!=q.

Its positive form is a diagonal matrix with entries (sum lambda²-lambda_p²)/4 plus the rank-one matrix lambda lambda^T/4. For common magnitudes |lambda_p|=alpha r and sign vector s, the face block is alpha²r²(10I+s s^T)/4. The exact largest eigenvalue is 21alpha²r²/4; zero couplings are handled without division by r. For an arbitrary coefficient box |lambda_p|<=alpha r, the maximum absolute row sum gives the same safe norm-squared upper bound. The fixture matrices carry squared physical energy units.

Deleting P subtraction would falsely give W a nonzero vacuum component if PV²P were asserted to equal W*W, although V Omega already lies in P. A one-coefficient Gaussian substitute changes the true cross diagonal 1/256 to 1/128. These controls falsify the proposed exact identities, not every conservative inequality using a larger matrix. In particular PV²P>=W*W, so PV²P can still supply an explicitly labelled conservative upper bound. A Gaussian substitute failing the exact Haar data likewise does not by itself refute every conservative estimate constructed from it. No floating-point eigensolver is used for these comparisons.

The bounded magnetic norm also yields QHQ>=(9alpha/2-sum|lambda_p|)Q as a form bound. This loop does not optimize the resulting scalar block inequality or assert the proposed B2 gap interval. Those require their next sequential gate.

## Evidence and execution boundary

Nine frozen coefficient fixtures include zero, both global signs, alternating signs, one nonzero coefficient, unequal signed/zero coefficients, all 3/8 and two nonunit alpha scales. Each stores all Gram, PVP, PV²P, subtraction and cross matrices. Required support rows, physical channels and coefficient fixtures cannot be omitted during replay. Direct cached-moment inputs reject Boolean aliases, negative indices and unsupported degrees before cache lookup.

Run `python -B check.py --output ../b1-output`. The dependency chain is check.py to cross.py to the unchanged accepted haar.py and graph.json. Outputs include the complete collection and exact cross-norm CSV. The source manifest is separate from the output hashes. Normal and optimized runs must give identical semantic evidence bytes; independent scientific acceptance is separate.

The original contract and its accepted amendment remain in the advisor record. The result is a complete finite-graph complement and cross-operator calculation, not a volume-uniform dense threshold. B2 remains unexecuted.
