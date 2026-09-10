# Independent A2: repeated strips with a summable remainder

The accepted result is an explicitly inhomogeneous family of full finite-box SU(2) rotor Hamiltonians. For canonical strip couplings and a dyadic remaining-face schedule, its physical spectral gap is at least 7α_min/64, uniformly over all finite box sizes n≥2 and α≥α_min>0. The homogeneous dense model and a thermodynamic or continuum spectral limit are not established.

## Actual geometry, for every box size

Vertices are (x,y,z) with coordinates 0,…,n−1. The complete box has n³ vertices, 3n²(n−1) positive-axis links and 3n(n−1)² elementary faces. Every link retains its electric Casimir. Select three consecutive xy squares at each anchor (4i,2j,z), where i<n div 4, j<n div 2 and z<n. They fit exactly when all four consecutive x vertices and both y vertices exist. Their count is n(n div 4)(n div 2).

A strip's x links have intervals x=4i,4i+1,4i+2 and rows y=2j,2j+1; its y links have interval y=2j and columns x=4i,…,4i+3. Distinct i ranges have no common x interval or y-link column, distinct j ranges have no common x-link row or y interval, and distinct z have different links. Thus all ten-link strip supports are pairwise disjoint. Each strip contains the internally overlapping A1 geometry. The full link Hilbert space, not the Gauss-restricted space, factors by this partition.

Every remaining face has a link outside this entire cluster support. For xz or yz faces, choose a z link: no strip uses one. For a remaining xy face with odd y, its y links are unused. For even y, every admissible y interval belongs to a complete selected row. If x lies in one of the complete spans 4i,…,4i+2, that face is selected. Otherwise x≡3 modulo 4, or x lies in the incomplete right boundary block whose i is at least n div 4. In either case its x links are unused. These cases include n=2 and n=3, when no strip exists, and incomplete terminal blocks at every larger n. This proof does not extrapolate from sampled boxes.

## Reference Hamiltonian and conditional Haar identity

Give each strip left and right couplings of magnitude at most α/2 and middle coupling of magnitude at most α/8. Signs and zeros are allowed. A1 gives a unique full-space cluster ground and cluster gap at least α/8. Free links have unique constant grounds and gap 3α/4. Hence the full cluster-product reference H_s has a unique ground Ψ_s, some energy E_s, and gap at least α/8. When there are no clusters, the actual free gap is 3α/4; α/8 remains a valid conservative lower estimate.

For each remaining face f, fix its unused link U and all other links. The reference density is independent of U, even though the cluster factors themselves are dressed. Its signed face trace has the form Tr(AU^{±1}B)/2. The arbitrary-fixed-link Haar argument already proved in A1 gives conditional first moment zero and second moment 1/4. Integrating the remaining reference density therefore gives ⟨Ψ_s,x_fΨ_s⟩=0. This is termwise valid for arbitrary dressed cluster factors; different remaining faces need not be independent.

## Exact weight schedule and finite ledger

For each positive-orientation face with lower anchor (x,y,z), set

\[
w_f=\frac{2^{-x-y-z}}{24},\qquad \nu_f=\alpha\tau w_f.
\]

Each of the three orientations has orthant sum (1/24)(1−1/2)^{-3}=1/3. Consequently the sum of all face weights is one, and the finite remaining-face weight W_n is at most one. The norm of V=−Σ_remaining ν_fx_f is at most β_n=α|τ|W_n. This remains valid for negative τ; it never treats a signed cancellation as an operator-norm reduction.

Let S_m=Σ_{k=0}^{m−1}2^{-k}, G_4(i)=Σ_{k=0}^{i−1}2^{-4k}, G_2(j)=Σ_{k=0}^{j−1}2^{-2k}. Independent enumeration and exact geometric sums give

\[
T_n=\frac{S_{n-1}^{2}S_n}{8},\quad
B_n=\frac7{96}G_4(\lfloor n/4\rfloor)G_2(\lfloor n/2\rfloor)S_n,
\quad W_n=T_n-B_n.
\]

The second formula includes all three faces in each cluster, since 1+1/2+1/4=7/4. These are weight ledgers, not the actual cluster coefficient sum: selected faces instead carry their left, middle or right interaction coefficients. The optional limit of W_n is 107/135. It is not substituted for the independently proved upper bound one. Incomplete boundary faces can switch from the remainder to a cluster at a later volume; the finite family is therefore not literally a restriction of one infinite coefficient assignment at every boundary. Each fixed local coefficient eventually stabilizes. No infinite-volume operator or spectral-convergence result is inferred.

## One-norm estimate, domain and physical sector

The finite product manifold SU(2)^{E_n} is compact. Its positive Casimir sum is elliptic and has compact resolvent. The finite real bounded plaquette perturbations preserve the self-adjoint operator and quadratic form domains. Min–max gives

\[
E_1(H_s+V)\ge E_s+\alpha/8-\beta_n,
\qquad E_0(H_s+V)\le E_s,
\]

where the second inequality uses the actual zero reference expectation of every remaining face. Therefore

\[
\Delta_{\rm full}\ge\alpha/8-\beta_n
\ge\alpha(1/8-|\tau|).
\]

The corresponding generic estimate without that zero-expectation argument would lose 2β_n. At τ=1/64 the uniform sharp estimate is 7α/64, while the generic estimate is 3α/32. A positive sharp lower bound gives a unique full ground. Gauge symmetry acts on its one-dimensional eigenspace by a continuous character of SU(2)^{V_n}, which must be trivial. The full ground belongs to the reducing Gauss subspace; restricting to that subspace cannot decrease the excitation threshold above this ground. Hence

\[
\boxed{\Delta_{\rm physical}\ge7\alpha_{\min}/64}
\]

for all n≥2, α≥α_min>0 and the canonical τ=±1/64 family. This is a lower bound on the full, untruncated physical operator, not a gap between Ritz eigenvalues.

## Exceptions and acceptance limits

With nonzero strip coefficients and τ≠0, every actual face coefficient is nonzero. The unselected coefficients decay spatially: full support does not make the model homogeneous. At τ=0 the model is valid but has absent remaining-face interactions. A zero selected coefficient also prevents full support whenever a corresponding strip exists; the same unused parameter does not remove support in n=2 or n=3 boxes with no strips. All these distinctions are determined from actual geometry and coefficients.

At |τ|=1/8 the conservative uniform estimate is zero and is marked insufficient, even if β_n<α/8 makes a particular finite-box estimate positive. Beyond that value, a negative dimensionless lower estimate cannot be multiplied by α_min as though it supplied a uniform physical lower bound; that field is left unclaimed. A homogeneous nondecaying remainder has a total norm budget growing with face count and fails the summability premise. No conclusion about actual gap closure follows from that rejected premise.

## Independent verification and retained mistakes

The standalone verifier independently rebuilds all signed box graphs for n=2,…,9, partitions their links, supplies an actual unused-link witness for every remaining face and compares exact weight enumeration with the closed formulas. It checks all four geometric cases, canonical and signed coefficients, zero branches, the uniform-bound endpoint, nonunit scales and strict model-input validation. The all-n conclusion rests on the proof above, with finite fixtures checking implementation.

The first check draft incorrectly replaced “the limit has not been proved to be a uniform upper bound” with a claim that a finite fixture exceeds the limit. Exact arithmetic correctly failed that check: the n=2,…,9 values are below the limit. The initial source and failed premise are retained in history. The correction records the limit without using it in the accepted bound. This repaired an invalid test assumption, not a gap equation.

Boundary review also replaced an apparently lazy itertools.product generator, which pools its ranges on first iteration, with nested loops. A billion-scale first-anchor request now executes without materializing the graph. Strict face validation precedes arithmetic witnesses, weights and words; Boolean coordinates and out-of-box faces are rejected. The original helper source and the reasons for these repairs are retained. No intentionally huge allocation was executed.

The final independent suite passes 36 named checks. The focused producer comparison passes 32 separate checks: all eight signed graphs, all fifteen required certificates and their full coefficient ledgers, the distinct negative-uniform control, the volume CSV and its source bindings. Complete records are reconstructed with independent geometry and rational arithmetic; no producer module is imported. Deliberate mutations test missing volume fixtures and unused-link witnesses, incorrect common scaling, replacement of the orthant bound by the unproved limit, promotion of a uniform endpoint using finite positivity, incorrect full-support classification, Boolean signed-word aliases and forged pass metadata. Ordinary and optimized Python produce identical scientific and comparison output bytes. The producer source chain and report were read in full; no additional material producer defect was found. The manifest records the final files and hashes. The post-A advisory review is planning only and does not execute B or C.
