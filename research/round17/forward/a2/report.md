# A2: a volume-uniform gap for a sparse-support exception

## Statement and original target

Retain the original full open cubic link graph of any vertex extent n>=2, link Hilbert spaces L2(SU(2),normalized Haar), Casimirs C_e=j(j+1), Gauss law at every vertex, and no external charges. The Hamiltonian is H=alpha sum_e C_e-sum_p lambda_p x_p. Restrict the nonzero magnetic coefficients to plaquettes whose four-link supports are pairwise disjoint. They may meet at vertices. Every other plaquette coefficient is0; no link or electric term is removed.

For a family satisfying alpha>=alpha_min>0 in common energy units and max_p|lambda_p|/alpha<=rho<3/4, the physical spectral gap satisfies

Delta_physical >= alpha_min*(3/4-rho)>0,

uniformly in volume and the allowed signed coefficients. This is a sparse-support theorem for a restricted family of the original operator. The original dense, overlapping-interaction uniform stability target remains open.

## Full-space block decomposition and its domain

Pairwise link disjointness partitions the finite link tensor product into interacting four-link blocks and all remaining one-link free factors. On a block,

h_p=alpha sum_(e in p) C_e-lambda_p*x_p.

The electric operator has its standard self-adjoint elliptic domain on the compact group product; the magnetic term is bounded self-adjoint. Each block, each free factor and their finite tensor sum have compact resolvent and a lower-bounded spectrum. This is a factorization of the full link Hilbert space. The globally gauge-invariant physical Hilbert space is not asserted to factorize into plaquette Hilbert spaces.

The free four-link block has unique constant ground and first unprojected gap3alpha/4: only one link need occupy spin1/2 before imposing Gauss. It would be wrong to insert the isolated physical-loop energy3alpha here. Since ||lambda_p*x_p||<=|lambda_p|, min-max gives E1(h_p)>=3alpha/4-|lambda_p|. The normalized constant has zero magnetic expectation, so E0(h_p)<=0. Hence Delta(h_p)>=3alpha/4-|lambda_p|. For |lambda_p|/alpha<3/4 this is positive and the block ground is unique. Every free edge has unique constant ground and gap3alpha/4.

The full tensor sum has unique product ground, and its gap is the minimum of its block/free gaps. Thus it is at least alpha*(3/4-rho). At rho=3/4 this sufficient lower bound is0; no conclusion of uniqueness or gap closure is licensed by that bound.

## Why the product ground lies in the physical Gauss sector

Each block Hamiltonian commutes with independent SU(2) transformations at its four endpoints. A unique normalized ground spans an invariant one-dimensional space, so the induced action is a continuous unitary character of SU(2)^4. This group has no nontrivial continuous one-dimensional characters: a Lie-algebra homomorphism from each simple su(2) to the abelian Lie algebra of U(1) vanishes, and the connected group then acts trivially. The block ground is therefore invariant under every endpoint transformation. A free-edge constant is likewise invariant under both endpoint actions.

When two blocks share a vertex, the actual global gauge transformation acts simultaneously on their separate factors. Each factor ground is already invariant under that action, so their product remains invariant. This permits shared vertices while requiring disjoint links. The full Hamiltonian commutes with the global gauge group, and its physical restriction contains the same unique product ground. Restricting to that reducing subspace cannot introduce any lower excitation above this ground. Therefore the full-space lower gap also bounds the physical gap. Replacing this argument by an assumed factorization of the physical Hilbert space would be invalid.

Finally alpha>=alpha_min and rho<3/4 give the stated common physical bound. This conclusion uses a common energy unit and a common positive prefactor. An interacting lower estimate approaching0 under a shrinking prefactor would not by itself prove actual gap closure; the separate exact free-box shrinking-scale counterexample retains its own scope.

## An extensive support mask for every size

Select xy squares anchored at(x,y,z) with x,y even in0,...,n-2 and arbitrary z in0,...,n-1. There are floor(n/2) choices in each horizontal coordinate and n layers, giving exactly n floor(n/2)^2 active plaquettes. Distinct same-layer anchors differ by at least2 along x or y, so their square edge sets are disjoint. Different layers use different xy links. Every selected edge remains in the original graph; all other links are free factors. This argument proves the mask for arbitrary integer n>=2; sampled graph construction only checks the implementation.

At rho=1/2 and alpha_min=1, the theorem gives the common lower bound1/4. The global physical norm estimate3alpha-sum|lambda_p| deteriorates as the active count grows. A negative value of that estimate is insufficient, while the separate product theorem remains positive. It is not a negative physical gap measurement.

The implementation uses a lazy arbitrary-size anchor generator and a closed count formula. Canonical full graph and complete mask materialization retain the copied A1 cap n<=12; this is a program cap, not a theorem limit. The advisor caught that the first materialized-mask helper lacked this cap, even though full graphs were capped. The old source and first finite-fixture result are retained in history; no huge allocation was executed. The repaired helper rejects large materialization immediately, while the lazy iterator and exact count still handle arbitrary extent.

Signed and zero coefficients, a vertex-only meeting, a first overlapping-link bridge, rho=3/4 and missing energy-scale/coupling assumptions are explicit checks. No B/C experiment or dense local-stability proof is executed in A2.
