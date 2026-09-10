# A1: a bridge between two dressed sparse magnetic blocks

## Operator and actual signed support

The three-square strip has vertices (x,y,0), x=0,1,2,3 and y=0,1. Its complete graph has eight vertices, ten links and three elementary xy faces. The end squares have disjoint four-link supports. The middle square shares one vertical link with each end and has two additional horizontal links. Every one of the ten electric Casimirs is retained. The exact signed words, including inverse links, are saved.

Work first on the full untruncated Hilbert space L2(SU(2)^10, normalized product Haar). There are no external charges. The physical restriction imposes Gauss law at all eight vertices. The Hamiltonian and reference are

    H_s = alpha sum_e C_e - lambda_left x_left - lambda_right x_right,
    H   = H_s - mu x_middle,

where x=Tr(U_face)/2, C_e=j(j+1), alpha>0 and every coupling has physical energy units. These are not the Euclidean action coefficients of the earlier conditional integrals.

The reference is a tensor sum of the two nonzero end blocks and every remaining free link. If an end coefficient vanishes, it contributes only free electric links; an empty active end support is valid. The physical Hilbert space is not claimed to factor. The accepted sparse-block argument applies when rho=max(|lambda_left|,|lambda_right|)/alpha<3/4. It gives a unique full-space dressed product ground Psi_s, unknown absolute energy E_s, and a reference gap at least g=alpha(3/4-rho). No numerical wavefunction or value of E_s is supplied or needed.

## Domains and the conditional Haar identity

On the finite compact connected group product, the electric operator is a positive elliptic Laplacian with its Sobolev operator domain and closed H1 form domain. The real Wilson multipliers are smooth and bounded. Adding them preserves self-adjointness on the operator domain, the form domain, lower boundedness and compact resolvent. Ground eigenfunctions are smooth; multiplying them by a face character remains in the domain. These facts justify both min-max and the reference Rayleigh test without a representation cutoff.

In the dressed product Psi_s, either of the two middle horizontal links remains a constant free-link factor. Hold every other link fixed. Cyclicity of trace writes the bridge character as Tr(U^sign K)/2 for some unitary SU(2) matrix K independent of that link. Haar invariance under multiplication and inversion makes U^sign K Haar. Therefore

    E_U[x_middle] = 0,
    E_U[x_middle^2] = 1/4.

The normalization follows from the ordinary-character identity chi_1^2=chi_0+chi_2 and character orthogonality. These identities hold pointwise in all other links. They can therefore be integrated against the arbitrary normalized density of the dressed end-block ground states. They do not assume those densities are uniform, and they do not replace Psi_s by the bare vacuum.

It follows that <Psi_s,x_middle Psi_s>=0 and ||x_middle Psi_s||=1/2. For P_s=|Psi_s><Psi_s| and Q_s=1-P_s, the bridge V=-mu x_middle consequently has

    P_s V P_s = 0,
    ||Q_s V P_s|| = |mu|/2.

The code binds this inference to actual unused link support. If no such link is available, its moment fields are missing and the sharpened gate is blocked. A value of zero is not fabricated for an unproved moment. Exact quaternion and separate complex-matrix word checks illustrate the pointwise identity for fixed surrounding assignments; none is asserted to approximate the unknown dressed ground.

The off-diagonal term also prevents a purely relative form bound around the reference with no additive or dressing correction. The state xi=2x_middle Psi_s is normalized, orthogonal to Psi_s and in the electric domain. For (Psi_s+t xi)/sqrt(1+t^2), the reference excitation energy is quadratic in t, while the bridge expectation is -mu t/(1+t^2); the diagonal term in xi vanishes by the corresponding odd Haar moment. For nonzero mu the ratio diverges as t tends to zero. An off-diagonal control cannot be replaced by the diagonal Q_s V Q_s estimate alone.

## The one-norm improvement and Gauss restriction

The bridge norm is at most |mu|. Min-max gives the full second eigenvalue bound

    E1(H) >= E_s + g - |mu|.

The actual reference ground is a normalized trial for H. Its zero bridge expectation gives E0(H)<=E_s. Combining these separate directions yields

    Delta_full >= g-|mu| >= alpha(3/4-rho)-|mu|.

This is a sufficient lower estimate, not an actual computed gap. A positive value implies a unique full ground. H commutes with the continuous SU(2)^8 vertex gauge action. That unique ground carries a one-dimensional continuous unitary representation of this group. Since SU(2)^8 has no nontrivial continuous one-dimensional characters, the ground is gauge invariant. The Gauss-invariant subspace is reducing and contains the same unique ground; restricting to it cannot introduce a lower excitation. Thus the same positive lower estimate holds for the physical gap.

The generic perturbation argument only guarantees g-2|mu| if the reference expectation is not controlled. The difference is material: for the finite matrices H_s=diag(0,1) and V=diag(1/4,-1/4), the actual gap is 1/2. The two-norm bound equals 1/2, whereas the invalid generic one-norm claim would be 3/4. Here the reference expectation is 1/4 rather than zero. This counterexample blocks dropping the conditional-Haar premise.

## Primary family, endpoints and scope

For all |lambda_left|,|lambda_right|<=alpha/2 and |mu|<=alpha/8, the entire parameter family satisfies

    Delta_physical >= alpha/8.

If alpha>=alpha_min>0 in common physical units, this implies the common bound alpha_min/8. This is an exact endpoint inequality for the whole stated family; the parameter plot is illustrative. At its worst corner, the generic estimate is zero while the improved estimate is 1/8 for alpha=1.

The fixtures include zero and both signs of mu, signed and zero end coefficients, an empty active reference, alpha=2 and alpha=1/2, and separate declared lower energy scales. At rho=1/2, |mu|/alpha=1/4 gives a zero sufficient bound; a larger value gives a negative insufficient bound. Neither establishes actual gap closure or a physical instability. Couplings outside the reference theorem's rho<3/4 range are outside this certificate method; they are not thereby invalid Hamiltonians.

Run `python -B check.py --output ../a1-output` from the source directory. Outputs include the complete graph, fixed parameter inventory, exact mu scan, conditional-word diagnostics, the finite counterexample, named semantic checks and hashes. All implementation code is local and uses only the standard library. Normal and optimized executions must produce identical evidence bytes. Independent scientific acceptance remains separate from these author checks.

The result is a finite internally overlapping cluster estimate. It does not repeat clusters, add remaining interactions, or prove a homogeneous dense volume-uniform Yang-Mills bound. Those A2 possibilities remain unexecuted pending the advisor's next gate.
