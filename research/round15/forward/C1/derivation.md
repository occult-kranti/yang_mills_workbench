# C1 finite-graph physical operator bound

This side result does not extract the missing volume-independent constants in the original local-stability theorem. The advisor's source audit retains that original goal as open. No stochastic relaxation rate is used here.

Let G be a finite connected simple graph. Each oriented link has Hilbert space L2(SU(2),normalized Haar); reverse orientation uses the inverse link. Impose the local Gauss constraint at every vertex, with no external charges or matter. The electric Hamiltonian is H0=alpha*sum_e J_e^2, alpha>0. It is self-adjoint on its standard electric Sobolev domain, positive and has compact resolvent on the finite product of compact groups. The gauge-invariant closed subspace reduces it. The normalized constant function Omega is its unique zero-energy vector.

## Exact free physical gap from graph girth

Peter–Weyl decomposition and invariant vertex intertwiners give an orthogonal spin-network basis. Every occupied edge has spin j>=1/2 and energy at least3alpha/4. At any vertex, exactly one nontrivial incident representation cannot couple with trivial representations to the singlet. Therefore the active-edge support of a nonconstant physical spin network has no degree-one vertex. A finite nonempty graph with minimum active degree at least2 contains a cycle. If G has finite girth g, every such support contains at least g occupied edges. Its electric energy is at least delta_G=3alpha*g/4.

A fundamental Wilson character around a shortest simple cycle is gauge invariant, nonconstant and occupies exactly g spin1/2 links. It attains delta_G. Thus this is the exact free physical gap, not only a lower estimate. If G is a forest, no nonempty active support is possible; the physical Hilbert space contains only the vacuum. The code reports a trivial physical sector, not a numerical excitation gap.

The argument requires a simple graph and Gauss constraints at all vertices. Self-loops, parallel edges, external charges, matter intertwiners and different boundary gauge constraints require different contracts. The ungauged link-space gap3alpha/4 must not be confused with the constrained physical gap.

## One-norm perturbation bound

Choose declared simple closed loop words with distinct edges. For x_p=Tr(U_loop_p)/2, |x_p|<=1. The vacuum expectation of every x_p is zero because at least one distinct link appears once and its fundamental Haar integral vanishes. For real coefficients lambda_p,

W=-sum_p lambda_p*x_p,
L=sum_p|lambda_p|,
||W||<=L and <Omega,W Omega>=0.

W is bounded self-adjoint and gauge invariant. H=H0+W remains self-adjoint on D(H0), with compact resolvent in the physical subspace. Let E0<=E1 denote eigenvalues counted with multiplicity. The min-max principle gives E1(H)>=delta_G-L. The vacuum trial gives E0(H)<=0. Therefore Delta=E1-E0>=delta_G-L. Only one L is needed because the vacuum trial improves the generic E0<=L estimate. Whenever delta_G-L>0, the ground state is simple and its first physical excitation is separated by this positive bound.

When delta_G-L<=0, the sufficient bound is inconclusive. It does not prove degeneracy or a vanishing actual gap. In particular, one cube has girth4 and six square loops, giving delta_G=3alpha and Delta>=3alpha-6|lambda| for equal-magnitude couplings. At |lambda|=alpha/2 the lower bound is exactly zero and must report insufficient.

## Growing open boxes

An open cubic box with n vertices per axis has3n^2(n-1) edges and P=3n(n-1)^2 elementary square plaquettes. For n>=2 its girth remains4, so the free physical gap remains3alpha. The sufficient uniform-coupling estimate becomes3alpha-P|lambda|. Its deterioration with P shows a limitation of this global perturbation-norm estimate. It is not the volume-independent local stability theorem, and it is not proof that the physical gap closes as volume grows.

## Candidate feedback for C2, not executed here

At the failed cube boundary lambda=alpha/2, a variational trial can improve the ground-energy upper bound below0. B1 established orthonormal square characters chi_p, H0 chi_p=3alpha chi_p, <Omega,W chi_p>=-lambda_p/2 and <chi_p,W chi_q>=0. Thus the vacuum-plus-six-character matrix has a2x2 bright-state block with offdiagonal magnitude sqrt(sum_p lambda_p^2)/2. Its lower eigenvalue is (3alpha-sqrt(9alpha^2+sum_p lambda_p^2))/2. If its variational use and an exact rational square-root enclosure are independently accepted, combining this upper bound on E0 with the unchanged lower bound on E1 could repair the specific zero-margin fixture. A finite trial-space gap by itself is not a lower bound on the full operator gap.
