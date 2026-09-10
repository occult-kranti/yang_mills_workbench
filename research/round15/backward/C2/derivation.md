# C2 independent full-operator variational improvement

Use the same untruncated all-Gauss cube Hamiltonian as C1. The B1 graph-matched Haar identities show that the seven vectors Omega,chi_1,...,chi_6 are orthonormal, H0 chi_p=3alpha chi_p, <Omega,W chi_p>=-lambda_p/2 and <chi_p,W chi_q>=0. The last identity includes coincident indices and relies on the proved missing-face character factorization, not merely on vanishing distinct-face products.

In this trial subspace the Hamiltonian is an arrowhead matrix with upper-left entry0, diagonal3alpha on the six character vectors, and vacuum-character entries-lambda_p/2. Let s2=sum_p lambda_p^2 and L=sum_p |lambda_p|. If s2>0, five character combinations orthogonal to the coupling vector have eigenvalue3alpha. The remaining two roots satisfy E^2-3alpha E-s2/4=0. Its lower root is

E_trial=(3alpha-sqrt(9alpha^2+s2))/2.

At zero couplings it is0 without dividing by the vanishing coupling-vector norm. The variational principle gives E0(full)<=E_trial; it does NOT give a lower bound on E0 or identify the other trial eigenvalues with full excitation levels.

Independently, C1's full-operator min-max result is E1(full)>=3alpha-L. Combining these two inequality directions gives

gap(full)>=B=(3alpha-2L+sqrt(9alpha^2+s2))/2.

If rational endpoints l<=sqrt(9alpha^2+s2)<=u are established, then the certified lower gap bound is(3alpha-2L+l)/2. Using u in that lower bound is invalid. The interval obtained by both endpoints encloses the expression B; it is NOT a two-sided enclosure of the true physical gap. Similarly the two-root endpoint interval encloses the trial eigenvalue, while only its upper endpoint gives an upper bound on the actual ground energy.

For common signed coefficients, r=|lambda|/alpha>=0 and B/alpha=(3-12r+sqrt(9+6r^2))/2. When r<=1/4 this is positive directly. For r>1/4, both sides of sqrt(9+6r^2)>12r-3 are positive, so squaring is equivalent and yields6r(12-23r)>0. Therefore B is positive exactly for0<=r<12/23, zero at12/23 and negative above that threshold. The zero of this sufficient bound does not assert gap closure.

At alpha=1 and all lambda_p=1/2, B=(sqrt(42)-6)/4>0 because42>36. This repairs the specific C1 zero-margin example with a new variational estimate while preserving the same physical Hamiltonian. It does not extract the original source-specific volume-uniform threshold. No volume extension is claimed here without a graph-matched repeated-moment/trial proof.
