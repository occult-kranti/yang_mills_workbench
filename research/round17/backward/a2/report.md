# A2 independent theorem: sparse link-disjoint magnetic support

The full spatial graph remains the open cubic graph with vertex extent n≥2. Every link has L²(SU(2), normalized Haar), every vertex obeys Gauss law, and H=αΣ_e C_e−Σ_p λ_p x_p with α>0, x_p=Tr(U_p)/2. Only the support of the existing real couplings is restricted: any two plaquettes with nonzero λ must have disjoint link sets. They may share vertices. This is a sparse family of the original Hamiltonian, not the dense overlapping family or a continuum construction.

**Full-space decomposition.** Partition the link set into four-link active blocks and the remaining individual links. The unprojected link Hilbert space is their tensor product and H is the finite tensor sum of its block operators and free-link Casimirs. This partition is by links, not vertices. No factorization of the gauge-invariant Hilbert space is assumed.

**Block gap and existence.** A four-link block has H₀,p=αΣ_(e∈p) C_e. It is a positive elliptic Laplacian on compact SU(2)^4 with compact resolvent; its ground is the constant function and its first unprojected excitation has energy 3α/4. Multiplication by −λ_p x_p is bounded self-adjoint with norm at most |λ_p|. The perturbed block has the same operator domain, is bounded below and has compact resolvent, so its lowest eigenvalues exist. The min–max principle gives E₁,p≥3α/4−|λ_p|. The normalized constant trial has mean magnetic energy zero, giving E₀,p≤0. Therefore

\[
\Delta_p=E_{1,p}-E_{0,p}\ge3\alpha/4-|\lambda_p|.
\]

For |λ_p|<3α/4 this proves uniqueness of the block ground: E₁,p>0≥E₀,p. The 3α/4 here is the unprojected block gap. Substituting the physical isolated-loop excitation 3α into this min–max bound would be an invalid strengthening.

**The full ground is physical.** Every block Hamiltonian commutes with the continuous SU(2)^4 action at its four endpoints. A unique ground spans a one-dimensional invariant subspace. Its group action must therefore be a continuous character SU(2)^4→U(1). Any such character is trivial: its differential maps the perfect Lie algebra su(2)^4 to the abelian Lie algebra of U(1), annihilating every commutator, hence the entire algebra; connectedness of SU(2)^4 then makes the character constant one. Thus each unique block ground is invariant under every endpoint transformation. Free-link constant ground states have the same invariance.

The product of all block and free-link grounds is consequently invariant under every global vertex transformation, even when several blocks meet at that vertex. The finite full-space tensor sum has a unique ground and its gap is the minimum of its component gaps. The physical Gauss subspace is closed and reducing because every Hamiltonian term commutes with the gauge action. Since it contains the full ground, its ground energy is the same and its first excitation cannot lie below the full-space first excitation. This restriction argument establishes the physical lower bound without factorizing the physical space.

If every nonzero coupling satisfies |λ_p|/α≤ρ<3/4, and all family members use common units with α≥α_min>0, then

\[
\Delta_{\rm physical}(n)\ge\alpha(3/4-\rho)
\ge\alpha_{\min}(3/4-\rho)>0
\]

for every finite n. Signs of the couplings are unrestricted. For ρ=1/2 and α_min=1 the bound is 1/4. The case with no active plaquettes is permitted; its exact physical free gap is 3α, while the weaker displayed bound remains valid. The exact free value follows from Gauss spin networks: nonempty active support has minimum degree two and contains a cycle; the cubic graph has girth four, and a fundamental square attains four times the link Casimir 3/4.

**An explicit extensive mask.** Use only xy plaquettes anchored at even x and even y, with 0≤x,y≤n−2, at every z=0,…,n−1. There are floor(n/2) choices in each anchor direction and n layers, hence n floor(n/2)^2 active plaquettes. Their one-step coordinate supports are disjoint within each layer, and distinct layers use distinct links. The proof works for arbitrary n, not just sampled sizes. Any assignment of signs to couplings bounded by αρ is allowed. This gives an extensive number of nonzero interactions even though their link supports are independent.

**Contrasts and stopping conditions.** At ρ=3/4 the displayed lower bound is zero and the certificate is insufficient. It does not prove gap closure or uniqueness at the endpoint. A smaller actual coupling could admit a stronger bound, but the stated family certificate retains its declared ρ. Negative sufficient bounds above the endpoint are likewise not physical gap values. An arbitrarily weak nonzero plaquette that shares a link with an active block violates the sparse factorization premise and must be rejected by this proof, without asserting that its true gap closes. A declared zero coefficient creates no active support and is ignored by that test.

The usual physical global-norm estimate 3α−Σ|λ_p| deteriorates with this extensive mask. Its failure does not contradict the positive block bound. Conversely, the exact free family α_n=1/n has gap 3/n→0 and shows why a common energy normalization is needed for the claimed uniform inference. An interacting *lower bound* tending to zero alone would not prove gap closure; these statements remain distinct.

No new field, mass or fitted constant is introduced. ρ bounds a declared Hamiltonian coupling family; the support mask selects zero coefficients of the existing action; α and λ have energy units. Euclidean κ is not identified with λ/α. The dense overlapping volume-uniform threshold remains open. This proof was derived independently before reviewing forward A2 evidence.

The completed standalone program passes 28 focused checks. A subsequent read-only comparison passes 14 gates covering all ten forward fixtures, actual block/free link partitions, signed coefficients, endpoint statuses and the entire volume ledger. Ordinary and optimized outputs are byte identical and count once. The independent geometry uses coordinate link sets; no forward source is imported. The forward source, runner, copied geometry and proof were read after the independent implementation. Its repaired materialization cap and retained pre-repair record were inspected; no additional discrepancy was found.

The independent materialized graph/mask program has a declared extent cap twelve. The theorem for arbitrary finite n follows from the given coordinate-mask and operator arguments, not extrapolation from the samples. The CLI is `python check.py --output NEW_OUTPUT_DIRECTORY`; outputs must be outside the frozen source directory. `compare.py` accepts explicit producer-source, producer-evidence and separate output directories. The manifest binds both source files, this proof, the 28-check results and the 14-check comparison. No B/C work has been executed in A2.
