# C2: repair of the finite cube's zero-margin sufficient bound

The common physical contract is the finite cube with untruncated L2(SU(2)) link Hilbert space, normalized Haar inner product, local Gauss invariance at all eight vertices, no external charges, alpha>0, and H=alpha*sum_e J_e^2-sum_p lambda_p*x_p. No Euclidean tilted density is substituted for its ground-state density. The original volume-uniform local-stability constant remains unevaluated.

## Derive the trial space from the accepted Haar identities

Take e0=Omega=1 and ep=chi_p=Tr(U_square_p), p=1,...,6. B1 proved their Gram matrix is the7x7 identity, every triple square character has zero Haar mean even with repeated indices, and H0 chi_p=delta chi_p with delta=3alpha. Thus

<Omega,H Omega>=0,
<Omega,H chi_p>=-lambda_p/2,
<chi_p,H chi_q>=delta*delta_pq.

Let Q=sum_p lambda_p^2. If Q>0, only the normalized bright vector Q^-1/2 sum_p lambda_p chi_p couples to the vacuum. The other five vectors have trial eigenvalue delta. The two remaining trial eigenvalues are (delta +/- sqrt(delta^2+Q))/2. If Q=0, the vacuum trial minimum is0 and no normalized bright vector is defined; the formula remains valid without dividing by Q.

By the variational principle, the smaller trial eigenvalue is an upper bound on the full operator's ground energy E0. C1 independently proves E1>=delta-L, L=sum_p|lambda_p|, for the second full physical eigenvalue counted with multiplicity. Combining these different one-sided bounds yields

Delta=E1-E0 >= B = (delta+sqrt(delta^2+Q))/2-L.

This is a lower bound on the full untruncated physical gap because E1 was controlled independently. The difference of two trial eigenvalues alone would not be such a bound. An interval around B encloses the value of this sufficient lower-bound formula; it is not an upper bound on the unknown actual gap.

For a radical enclosure lo<=sqrt(delta^2+Q)<=hi, use full_E0_upper=(delta-lo)/2, full_E1_lower=delta-L and certified_gap_lower=(delta+lo)/2-L. All square-root and gap-bound endpoint errors remain in the certificate. Exact perfect-square rational radicands are recognized before dyadic approximation; otherwise integer-square-root floors produce exact rational lower/upper endpoints whose squared inequalities are checked.

The analytic common-range classification and the computational enclosure status answer different questions. At the central ratio1/2, the exact algebra proves positivity, while a deliberately coarse0-bit radical enclosure gives only a nonpositive lower endpoint and must still report inconclusive. Likewise a positive computed lower endpoint does not satisfy the requested accuracy when its retained interval width exceeds the precision target. All three statuses are preserved separately.

## The formerly failed fixture and its scale

For alpha=1 and all six lambda=1/2, C1 gave only0. Here Q=3/2, so B=(sqrt(21/2)-3)/2, approximately0.120185174601965. The formula scales linearly with alpha when lambda_p/alpha is held fixed: delta=alpha*3, L=alpha*sum|r_p|, Q=alpha^2*sum r_p^2. Thus the central positive coefficient applies to every alpha>0 in the same finite-cube contract. It introduces no new physical mass term.

## Exact common-magnitude sufficient range

If every |lambda_p|=r*alpha, r>=0, then B/alpha=(3+sqrt(9+6r^2))/2-6r. For0<=r<=1/4, the lower estimate sqrt(9+6r^2)>=3 immediately gives B/alpha>=3-6r>0. For r>1/4, positivity is equivalent to sqrt(9+6r^2)>12r-3, where both sides are nonnegative. Squaring gives6r*(12-23r)>0, hence r<12/23. At r=12/23, sqrt(9+6r^2)=75/23 and the bound is exactly0. Beyond this value the sufficient bound is negative, which does not prove physical gap closure.

Consequently the common-magnitude sufficient interval expands from r<1/2 in C1 to r<12/23 in C2. Signs of the individual lambda_p do not change this bound because L and Q depend only on their magnitudes. Heterogeneous coefficients are handled by the general L,Q formula; the common-magnitude ratio label is withheld when magnitudes differ.

## What this does not repair

The exact variational improvement addresses a concrete finite-volume failure. It does not extract a local stability constant independent of volume, identify a continuum limit, or establish the four-dimensional Yang–Mills mass gap. The growing-box CSV retained from C1 demonstrates deterioration of a sufficient estimate; no new volume-uniform claim is inferred from the cube calculation.
