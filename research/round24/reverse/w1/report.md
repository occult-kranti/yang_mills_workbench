# W1 reverse — the actual short-filter residual retains a cubic source

Independent reverse derivation before reading forward W1. The model is exactly the homogeneous complete-24-link S1/S2 initial diagonal G, not the canonical V/U model. Shared inherited source and form premises are correlated. Newton's reverse reconstruction asks what spectral information is necessary to remove the residual; Tesla's whole-system check keeps all crossing stars and the actual vacuum. We obtain an actual-source lower bound rather than substituting a generic resonant matrix.

## Source energy is computable without solving strip eigenfunctions

Use H=H0,Y on the origin star Y, with product ground o and gap at least one. S1 defines v=phi_0 o, u=H_Q^(-1)v, a=<u,v>, beta=||u||^2, sigma^2=||v||^2=7tau^2/12 and

    w= -a u -(beta/3)v,  r=||w||,
    A=(|w><o|+|o><w|) tensor I_ext.                    (W1.R1)

Every one of the 21 omitted faces in phi_0=-(tau/3)sum_f W_f has at least two free Haar links. Distinct such faces have an unmatched free link; the inherited S1 variance proof establishes this geometry, re-enumerated in the checker. Derivatives of a Wilson factor preserve its parity under central sign inversion on each link. Therefore, for f!=g and every differentiated link e, the cross gradient expectation <grad_e W_f,grad_e W_g> weighted by |o|^2 vanishes: if both derivatives are nonzero, an unmatched free link still supplies odd Haar parity. If e is absent from one face, that term vanishes directly.

In the frozen normalization H has electric coefficient alpha/delta=8 times the SU(2) Casimir on every link; the selected potentials and ground-energy shifts are multiplication operators. For any real smooth bounded multiplication F on these finitely many links, the local quadratic form obeys

    h[F o]=8 sum_e integral |grad_e F|^2 |o|^2.          (W1.R2)

This follows by expanding the kinetic form and subtracting the ground's weak eigenvalue equation tested against F^2 o. Smooth bounded F and its bounded derivatives preserve the form domain, so no unknown strip wavefunction or second-derivative estimate is needed. The finite-link tensor potentials are bounded. Only the local form domain, not an unjustified operator-domain assertion for arbitrary multipliers, is used.

For W_f=Tr(U_f)/2 and a participating link, the Casimir convention with spin-half eigenvalue 3/4 gives the pointwise identity

    sum_{a=1}^3 |X_e^a W_f|^2=(1-W_f^2)/4.

It follows by writing U_f as a unit quaternion: the generator is i sigma_a/2, so X_a q_0=-q_a/2 up to an orthogonal rotation of the generator basis. Inversion and orientation preserve the squared sum. A free Haar link in the face makes the loop holonomy Haar conditional on all other links, hence E W_f^2=1/4 and each participating link contributes 3/16. There are four links in each face. Equations (W1.R2) and the parity cancellation give the **actual exact first form moment**

    <v,H v>_form = (tau^2/9)*21*8*4*(3/16)
                =14 tau^2 =24 sigma^2.                (W1.R3)

This is a Haar/form identity on the untruncated Hilbert space. The quaternion design in the checker integrates only its needed second moments; it is not a replacement measure for the full dynamics. The source v is therefore in the form domain even though no new claim about ||Hv|| is needed.

## The inverse-weighted cubic source has mean energy at most 24

Let dnu(lambda)=d<v,E_H(lambda)v>, supported in [1,infinity). Its mass is sigma^2 and first moment is 24sigma^2. The positive numbers a=int lambda^-1 dnu and beta=int lambda^-2 dnu are defined by this actual source, not adjustable coefficients. Equation (W1.R1) reads w=-f(H)v with f(lambda)=a/lambda+beta/3, a positive decreasing function at nonzero tau.

For the probability measure dnu/sigma^2, the covariance of lambda and the decreasing function f(lambda)^2 is nonpositive: twice the covariance is the double integral of (lambda-mu)(f(lambda)^2-f(mu)^2), which is pointwise nonpositive. All integrals exist by the first moment and boundedness of f on [1,infinity). Thus

    h[w]/r^2 <= h[v]/sigma^2 =24.                     (W1.R4)

This supplies actual source spectral information without computing the full spectral measure. Jensen also gives a>=sigma^2/24 and beta>=sigma^2/24^2. S1's inner product <v,w>=-a^2-beta sigma^2/3 then yields

    r >= sigma^3/432 >0  (tau!=0).                    (W1.R5)

The inherited upper bound remains r<=4sigma^3/3. These estimates concern the selected indexed cubic term, not the entire cubic coefficient or a sum in which other indexed terms might cancel it.

## Actual full residual lower bound throughout the frozen filter interval

Let Omega=o tensor Omega_ext and w_full=w tensor Omega_ext. For the initial full retained diagonal, all D_b annihilate Omega and G Omega=0. Complete-star incidence gives the inherited form comparison

    (1-kappa)H0 <= G <=(1+kappa)H0,
    kappa=4M, M=7|tau|, kappa<=35/416<1.

It holds in every complete-star finite containing cuboid and in the admitted R2 infinite reference representation. The local vector w_full lies in its common form domain by (W1.R4), and

    <w_full,G w_full>_form <=24(1+4M)r^2.             (W1.R6)

Keep the complete S2 identity and its domain statement:

    [L_Theta(A),G]=-A+R_Theta(A),
    R_Theta(A)=(1/(2Theta))int_{-Theta}^{Theta} e^(isG) A e^(-isG) ds.

The residual acts on every exterior sector because A is identity-extended. Its vacuum column, which suffices for a lower bound on the full operator norm, is exactly

    R_Theta(A)Omega=sinc(Theta G)w_full.               (W1.R7)

For x>=0, 1-cos x<=x (integrate sin u<=1). Thus sinc x=int_0^1 cos(tx)dt>=1-x/2. Applying this scalar lower bound to the positive spectral measure of w_full, using only its first form moment, gives

    <w_full,R_Theta(A)Omega>
       >=r^2-(Theta/2)<w_full,G w_full>_form,
    ||R_Theta(A)|| >=[1-12Theta(1+4M)]r
                   >=(311/1664)r >0                 (W1.R8)

for every nonzero allowed tau and 0<Theta<=1/16. This is an actual SU(2) residual nonvanishing result, uniformly in the containing cuboid; the same argument applies to the admitted infinite G. Combining (W1.R5) gives a uniform lower coefficient

    ||R_Theta(A)|| >= (311/718848)(7/12)^(3/2)|tau|^3.

Consequently the frozen short triangular filter cannot reduce this selected source to a higher order than cubic by retaining only its commutator term. The residual cannot be silently deleted. At tau=0 the source and residual vanish; shortening Theta tends strongly to the source residual. The positive factor is a sufficient bound, not the exact residual ratio.

## What this proves about all sectors, and what it leaves open

The full-source identity is inherited and retained on D(G); the preceding lower bound uses one genuine vacuum column to prove nonvanishing of the full operator. It does not reconstruct all exterior-sector spectral blocks, prove an exact equal-energy block of A, or obstruct every possible inverse. In particular a source may have a large short-time average even with no zero-frequency component. A positive ground gap supplies no general lower bound on excited Bohr frequency differences. Replacing A by A tensor P_ext would change the operator and erase actual external excitations, as S1 already proved.

The connected-support expansions and positive weight-2 certificates from S2 remain valid for both L and R; their support labels include repeated anchors and incoming crossing stars. The full source split remains C=bI+A_gen+Q(C-bI)Q. Scalar and diagonal pieces cannot be discarded or reclassified from (W1.R8). The result is for initial G only. Later diagonals alter the vacuum, the source, spectral measure, form comparison and possibly the support decomposition. Reusing kappa, the exact energy 24 or the source's decreasing spectral form at later stages requires a proof for that stage.

The next loop should decide a useful retained-residual iteration or quantify an actual low-frequency/all-sector condition in a compatible interaction norm. Simply increasing Theta is outside the present connected-series guarantee; loss of that majorant's radius is not a theorem of dynamics divergence. For a claim of exact inverse, one still needs vanishing equal-energy source blocks and bounded division of the full spectral kernel, with support sums. For a contraction claim, one must track the actual residual, scalar and diagonal updates and show its retained leading order is harmless under a specified iteration.

Theta is a proof duration with energy resolution delta/Theta, delta=alpha/8; neither is fitted to this bound. Physical a,E_star,alpha/E_star,hbar stay positive and fixed. The exact Haar energy, monotone spectral reweighting and residual lower bound are modern calculations motivated by the method skills. No historical endorsement, homogeneous numerical gap, physical calibration, continuum construction, or verified scientific priority follows.

## Executable evidence

The standalone checker enumerates the 21 actual faces and their free-link parity, calculates the exact Haar gradient coefficient, proves the rational endpoint factor and samples an exact finite spectral measure only as a control of the monotone-reweight algebra. It distinguishes that fixture from the analytic actual-source theorem. Negative controls cover wrong Casimir normalization, missing cross-parity evidence, increasing rather than decreasing spectral weight, omission of the full form factor, zero coupling, and deleting the residual. Normal and optimized Python enforce explicit runtime checks.
