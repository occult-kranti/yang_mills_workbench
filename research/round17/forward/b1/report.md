# B1: twelve physical trial states on the dense two-cube graph

## Post-A boundary and actual graph

Use the accepted two-cube complex with 12 vertices, 20 links and 11 distinct elementary faces, including the shared square once. Its signed words and normalized link-Haar measure are retained. H=alpha sum_e C_e-sum_(p=1)^11 lambda_p*x_p, alpha>0, has the untruncated Gauss-invariant link Hilbert space and no external charges. Lambda_p are physical energies, distinct from static Euclidean coefficients. With every face coefficient nonzero, supports overlap at links. A2's sparse factorization theorem is inapplicable even when these coefficients are small.

## Rebuild the full trial matrix

Take b0=Omega and bp=chi_p=2x_p for eleven ordinary fundamental face characters. The actual graph Haar functional computes every product, including repeated indices. Single-face holonomies are Haar, with <x>=0, <x^2>=1/4 and <x^3>=0. Distinct degree-two and all degree-three character products vanish: repeated degrees are added at each face before testing link-center parity, and the direct two-disk/fusion integral confirms their values. An assertion about distinct-face subsets alone would not cover these repeated products.

The Gram matrix is I12. Every chi_p occupies four distinct spin 1/2 links and lies in the physical electric domain; H0 chi_p=3alpha chi_p. Thus the electric matrix is diag(0,3alpha,...,3alpha). The magnetic entries are

<Omega,W Omega>=0,
<Omega,W chi_p>=-lambda_p/2,
<chi_p,W chi_q>=0 for all p,q.

The code reconstructs all 144 Gram entries and all 1584 individual face-insertion matrix elements, not only the final arrowhead shape. The expected nonzero insertions are <Omega,x_f chi_p>=delta_fp/2 and their transposes. Every other such insertion is 0. Copies of the previously accepted exact graph/Haar utility are local to this source package; no import depends on another scratch directory.

## Independent full-operator excited bound

The graph is bipartite and contains square loops, hence its girth is 4. A nonconstant physical spin network has nontrivial support with no degree-one vertex under all-vertex Gauss constraints. Its support contains a cycle of at least 4 excited links, each Casimir>=3/4. A fundamental square loop attains energy 3alpha. The exact physical free gap is therefore delta=3alpha.

The magnetic operator is bounded self-adjoint with norm<=L=sum_p|lambda_p|. The free elliptic operator and its bounded perturbation have compact resolvent on the finite compact link manifold; the Gauss-invariant subspace is reducing. Min-max gives the full second eigenvalue E1(H)>=delta-L. This is a bound on the full untruncated operator, not a trial-matrix eigenvalue.

## Variational ground bound and combination

Set Q=sum_p lambda_p^2. When Q>0, only the bright vector proportional to sum_p lambda_p chi_p couples to the vacuum. Ten orthogonal trial vectors retain eigenvalue delta; the bright two-dimensional block has offdiagonal magnitude sqrt(Q)/2. Its lowest eigenvalue is

e_trial=(delta-sqrt(delta^2+Q))/2.

For Q=0 the constant remains the trial ground; no division by sqrt(Q) is performed. The variational principle gives E0(H)<=e_trial. Therefore

Delta_physical=E1-E0 >= (delta+sqrt(delta^2+Q))/2-L.

Both ingredients are necessary. The gap between two trial eigenvalues is not a lower bound on the full physical gap. A rational radical bracket [lo,hi] gives E0<=(delta-lo)/2 and a certified full-gap lower endpoint (delta+lo)/2-L. The saved bracket encloses this sufficient lower-bound expression; its upper endpoint is not an upper bound on the actual gap.

## Exact common-magnitude threshold

For all |lambda_p|/alpha=r>=0, the sufficient bound divided by alpha is

B(r)=(3+sqrt(9+11r^2))/2-11r.

For 0<=r<=3/22, positivity follows without squaring. For r>3/22, both sides of sqrt(9+11r^2)>22r-3 are nonnegative. Squaring gives r*(132-473r)>0, which is equivalent to r<12/43. At r=12/43 the radical is exactly 135/43 and B=0; this is an insufficient boundary of the estimate, not physical gap closure. At the older global-bound endpoint r=3/11, delta-L=0 but the improved expression (sqrt(108/11)-3)/2 is strictly positive. Signs of individual coefficients do not change L and Q; unequal magnitudes use the general formula without claiming the common-ratio classification.

These are finite dense-graph conclusions. They neither extend A2's sparse theorem to overlaps nor establish a volume-independent dense interaction threshold. B2 has not been executed; its proposed additional shared-face representation must be selected after the actual zero-margin B1 endpoint is accepted.
